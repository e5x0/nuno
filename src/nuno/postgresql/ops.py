from fabric import Connection, task

from nuno.common import sudo, ReturnCode, NunoArgs
import nuno.decorator


@nuno.decorator.init
def postgresql_version(c: Connection, args: NunoArgs) -> ReturnCode:
    """Get postgresql version on a host"""
    uname = sudo(c, "uname -s")
    args.o.output.append(uname)
    uname_stdout = uname.stdout.replace("\n", "")
    if "Linux" not in uname_stdout:
        err = "No idea how to get postgresql version on {}!".format(uname_stdout)
        args.logger.warning(err)
        return 1
    pgsql_version = sudo(c, "psql --version | awk '{print $3}'", user="isupg")
    pgsql_version.stdout = pgsql_version.stdout.replace("\n", "")
    args.o.output.append(pgsql_version)
    args.logger.info(args.o)
    return 0
