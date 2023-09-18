from dataclasses import asdict
import logging

from fabric import Connection

import nuno.decorator
from nuno.common import sudo, ReturnCode, NunoArgs


@nuno.decorator.init
def disk_free(c: Connection, args: NunoArgs) -> ReturnCode:
    """Get disk space on a host"""
    args.o.output.append(sudo(c, "uname -s"))
    args.o.output[0].stdout = args.o.output[0].stdout.replace("\n", "")
    release = args.o.output[0].stdout.replace("\n", "")
    if "Linux" not in release:
        err = "No idea how to get disk space on {}!".format(release)
        args.logger.warning(err)
        return 1
    command = "df -h / | tail -1 | awk '{print $5}'"
    args.o.output.append(sudo(c, command))
    args.o.output[1].stdout = args.o.output[1].stdout.replace("\n", "")
    args.logger.info(args.o)
    return 0


if __name__ == "__main__":
    print(disk_free(Connection("localhost")))
