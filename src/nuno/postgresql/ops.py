from fabric import Connection, task

from nuno.common import sudo, ReturnCode, NunoArgs, Pipeline, replaceStdout
import nuno.decorator


@nuno.decorator.init
def postgresql_version(c: Connection, args: NunoArgs) -> ReturnCode:
    """Get postgresql version on a host"""
    args.o.output = (
        Pipeline(c, user="isupg")
        .pipe("psql --version | awk '{print $3}'")
        .pipe(replaceStdout("\n", ""))
        .execute()
    )
    args.logger.info(args.o)
    return 0
