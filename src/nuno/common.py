from dataclasses import dataclass, asdict
from typing import List, Union, TypeAlias, Callable
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
) -> SudoOutput:
    """Run a command as root or another user"""
    su = "su - " + user + " -c "
    shell = "bash -l -c '" if source_profile else "bash -c '"
    cmd = cmd.replace("'", "'\\''")
    sudo_cmd = su + shell + cmd + "'"
    result = c.sudo(sudo_cmd, **settings_opts)
    return SudoOutput(cmd, user, result.stdout, result.stderr)


def compose(*func_list) -> Callable:
    """Compose a list of functions"""
    return functools.reduce(lambda f, g: lambda x: f(g(x)), func_list)
