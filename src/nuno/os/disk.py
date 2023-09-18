from dataclasses import asdict
import logging

from fabric import Connection

import nuno.decorator
from nuno.common import sudo, ReturnCode, NunoArgs, Pipeline, replaceStdout


@nuno.decorator.init
def disk_free(c: Connection, args: NunoArgs) -> ReturnCode:
    """Get disk space on a host"""
    args.o.output = (
        Pipeline(c)
        .pipe("df -h / | tail -1 | awk '{print $5}'")
        .pipe(replaceStdout("\n", ""))
        .execute()
    )
    args.logger.info(args.o)
    return 0


if __name__ == "__main__":
    print(disk_free(Connection("localhost")))
