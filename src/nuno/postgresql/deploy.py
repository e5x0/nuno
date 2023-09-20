from fabric import Connection, task

from nuno.common import sudo, ReturnCode, NunoArgs, Pipeline, replaceStdout
import nuno.decorator


@nuno.decorator.init
def install_sqlite_fdw(c: Connection, args: NunoArgs) -> ReturnCode:
    """Install sqlite_fdw on a host"""
    args.o.output = Pipeline(c, user="root").pipe("systemctl stop postgresql").execute()
    args.o.output.extend(
        Pipeline(c, user="isupg")
        .pipe("git clone https://github.com/pgspider/sqlite_fdw.git")
        .execute()
    )
    args.o.output.extend(
        Pipeline(c, user="isupg", chdir="${HOME}/sqlite_fdw")
        .pipe("make USE_PGXS=1")
        .pipe("make install USE_PGXS=1")
        .execute()
    )
    args.o.output.extend(
        Pipeline(c, user="root").pipe("systemctl start postgresql").execute()
    )
    args.o.output.extend(
        Pipeline(c, user="isupg", chdir="${HOME}/sqlite_fdw")
        .pipe('psql postgres -c "CREATE EXTENSION sqlite_fdw"')
        .execute()
    )
    args.logger.info(args.o)
    return 0


@nuno.decorator.init
def install_mysql_fdw(c: Connection, args: NunoArgs) -> ReturnCode:
    args.o.output = Pipeline(c, user="root").pipe("systemctl stop postgresql").execute()
    args.o.output.extend(
        Pipeline(c, user="isupg")
        .pipe("git clone https://github.com/EnterpriseDB/mysql_fdw.git")
        .execute()
    )
    args.o.output.extend(
        Pipeline(c, user="isupg", chdir="${HOME}/mysql_fdw")
        .pipe("make USE_PGXS=1")
        .pipe("make USE_PGXS=1 install")
        .execute()
    )
    args.o.output.extend(
        Pipeline(c, user="root").pipe("systemctl start postgresql").execute()
    )
    args.o.output.extend(
        Pipeline(c, user="isupg", chdir="${HOME}/mysql_fdw")
        .pipe('psql postgres -c "CREATE EXTENSION mysql_fdw"')
        .execute()
    )
    args.logger.info(args.o)
    return 0
