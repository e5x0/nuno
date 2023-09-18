from dataclasses import asdict
from logging.config import dictConfig
from typing import Callable
import json
import yaml
import logging

from fabric import Connection

from nuno.common import ReturnCode, TaskOutput, NunoArgs, compose


def init(f) -> Callable:
    """Decorator to initialize Nuno"""

    def _wrapper(c: Connection, args: NunoArgs) -> ReturnCode:
        return compose(set_exit, parse_ansible_vars, set_logger, set_task_output)(f)(
            c, args
        )

    return _wrapper


def set_task_output(f) -> Callable:
    """Decorator to add output to a fabric task"""

    def _wrapper(c: Connection, args: NunoArgs) -> ReturnCode:
        args.o = TaskOutput(f.__name__)
        return f(c, args)

    return _wrapper


def parse_ansible_vars(f) -> Callable:
    """Decorator to parse Ansible variables from a fabric task"""

    def _wrapper(c: Connection, args: NunoArgs) -> ReturnCode:
        d = json.loads(str(args.ansible_vars))
        if c.host not in d:
            print("No variables for host {}!".format(c.host))
        return f(c, args)

    return _wrapper


def set_logger(f) -> Callable:
    """Decorator to initialize logging from a yaml file"""

    def _wrapper(c: Connection, args: NunoArgs) -> ReturnCode:
        with open("./conf/logger.yaml") as yaml_file:
            config = yaml.safe_load(yaml_file)
            dictConfig(config)
            args.logger = logging.getLogger(__name__)
            return f(c, args)

    return _wrapper


def set_exit(f) -> Callable:
    """Decorator to exit on non-zero return code"""

    def _wrapper(c: Connection, args: NunoArgs):
        rc = f(c, args)
        if rc != 0:
            raise SystemExit(rc)

    return _wrapper
