from dataclasses import dataclass, asdict
from typing import List, Union, TypeAlias, Callable, Optional, Tuple
import logging
import functools

from fabric import Connection, task

ReturnCode: TypeAlias = int  # Return code of a fabric task


@dataclass
class SudoOutput:
    """Output of a sudo command"""

    cmd: str
    user: str
    stdout: str
    stderr: str


Command = str | Callable[[Optional[SudoOutput]], Optional[SudoOutput]]


@dataclass
class TaskOutput:
    """Output of a fabric task"""

    task: str
    output: List[SudoOutput]

    def __init__(self, task):
        self.task = task
        self.output = []

    def __repr__(self) -> str:
        return str(asdict(self))


@dataclass
class NunoArgs:
    """Arguments for a fabric task"""

    o: TaskOutput
    logger: logging.Logger
    fabric_vars: dict
    ansible_vars: Union[str, dict]

    def __init__(self, fabric_vars: dict, ansible_vars: Union[str, dict]):
        self.o = TaskOutput("")
        self.logger = logging.getLogger(__name__)
        self.fabric_vars = fabric_vars
        self.ansible_vars = ansible_vars


class Pipeline:
    """Command to run on a host"""

    def __init__(
        self,
        c: Connection,
        user: str = "root",
        source_profile: bool = True,
        settings_opts: dict = {
            "echo": True,
            "hide": True,
            "warn": True,
            "pty": False,
        },
    ):
        self.connection = c
        self.cmd_list: List[Command] = []
        self.user = user
        self.source_profile = source_profile
        self.setting_opts = settings_opts

    def pipe(self, f: Command) -> "Pipeline":
        """Pipe a function to the output of a command"""
        self.cmd_list.append(f)
        return self

    def execute(self) -> List[SudoOutput]:
        """Execute the pipeline"""

        def exec_command(c: Command, x: Optional[SudoOutput]) -> Optional[SudoOutput]:
            if isinstance(c, str):
                return sudo(
                    self.connection,
                    source_profile=self.source_profile,
                    cmd=c,
                    user=self.user,
                    settings_opts=self.setting_opts,
                )
            elif callable(c):
                return c(x)
            else:
                return None

        output_list: List[SudoOutput] = []
        result = None
        for cmd in self.cmd_list:
            result = exec_command(cmd, result)
            if result is not None:
                output_list.append(result)
        return output_list


@task
def sudo(
    c: Connection,
    cmd: str,
    user: str = "root",
    source_profile: bool = True,
    settings_opts: dict = {
        "echo": True,
        "hide": True,
        "warn": True,
        "pty": False,
    },
    f: Callable = lambda x: x,
) -> SudoOutput:
    """Run a command as root or another user"""
    su = "su - " + user + " -c "
    shell = "bash -l -c '" if source_profile else "bash -c '"
    cmd = cmd.replace("'", "'\\''")
    sudo_cmd = su + shell + cmd + "'"
    result = c.sudo(sudo_cmd, **settings_opts)
    return f(SudoOutput(cmd, user, result.stdout, result.stderr))


def compose(*func_list) -> Callable:
    """Compose a list of functions"""
    return functools.reduce(lambda f, g: lambda x: f(g(x)), func_list)


def replaceStdout(
    old: str, new: str
) -> Callable[[Optional[SudoOutput]], Optional[SudoOutput]]:
    """Replace a string in the stdout of a command"""

    def _f(x: Optional[SudoOutput]):
        if x is None:
            return None
        else:
            return SudoOutput(
                replaceStdout.__name__, x.user, x.stdout.replace(old, new), x.stderr
            )

    return _f
