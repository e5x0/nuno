from fabric import Connection, task

from nuno.common import sudo, ReturnCode, NunoArgs, Pipeline, replaceStdout
import nuno.decorator


@nuno.decorator.init
def createdb_pgsql(c: Connection, args: NunoArgs) -> ReturnCode:
    """Create a database"""
    args.o.output = (
        Pipeline(c, user="isupg")
        .pipe(
            "createdb --locale={0[locale]} -E {0[encoding]} --template={0[template]} --no-password {0[dbname]}".format(
                args.fabric_vars
            )
        )
        .execute()
    )
    args.logger.info(args.o)
    return 0


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


@nuno.decorator.init
def install_pgadmin4(c: Connection, args: NunoArgs) -> ReturnCode:
    environment_vars = (
        "PGADMIN_SETUP_EMAIL={0[email]} PGADMIN_SETUP_PASSWORD={0[password]} ".format(
            args.fabric_vars
        )
    )
    args.o.output = (
        Pipeline(c, user="root")
        .pipe(
            "curl -fsS https://www.pgadmin.org/static/packages_pgadmin_org.pub | gpg --dearmor -o /usr/share/keyrings/packages-pgadmin-org.gpg"
        )
        .pipe(
            'echo "deb [signed-by=/usr/share/keyrings/packages-pgadmin-org.gpg] https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'
        )
        .pipe("apt install -y pgadmin4-web")
        .pipe(environment_vars + "/usr/pgadmin4/bin/setup-web.sh --yes")
        .execute()
    )
    args.logger.info(args.o)
    return 0
