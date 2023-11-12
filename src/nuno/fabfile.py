from fabric import Connection, task
from dataclasses import dataclass, asdict

import nuno.os.disk
import nuno.postgresql.ops
import nuno.postgresql.deploy
from nuno.common import NunoArgs


@task
def disk_free(c: Connection, ansbile_vars: dict | str = "{}"):
    nuno.os.disk.disk_free(c, NunoArgs(fabric_vars={}, ansible_vars=ansbile_vars))


@task
def postgresql_version(c: Connection, ansbile_vars: dict | str = "{}"):
    nuno.postgresql.ops.postgresql_version(
        c, NunoArgs(fabric_vars={}, ansible_vars=ansbile_vars)
    )


@task
def createdb_pgsql(c: Connection, dbname="nunodb", ansbile_vars: dict | str = "{}"):
    nuno.postgresql.deploy.createdb_pgsql(
        c, NunoArgs(fabric_vars={"dbname": dbname}, ansible_vars=ansbile_vars)
    )


@task
def install_sqlite_fdw(c: Connection, ansbile_vars: dict | str = "{}"):
    nuno.postgresql.deploy.install_sqlite_fdw(
        c, NunoArgs(fabric_vars={}, ansible_vars=ansbile_vars)
    )


@task
def install_mysql_fdw(c: Connection, ansbile_vars: dict | str = "{}"):
    nuno.postgresql.deploy.install_mysql_fdw(
        c, NunoArgs(fabric_vars={}, ansible_vars=ansbile_vars)
    )


@task
def install_pgadmin4(
    c: Connection,
    email: str = "dummy@hoge.io",
    password: str = "dummy",
    ansbile_vars: dict | str = "{}",
):
    nuno.postgresql.deploy.install_pgadmin4(
        c,
        NunoArgs(
            fabric_vars={
                "email": email,
                "password": password,
            },
            ansible_vars=ansbile_vars,
        ),
    )


if __name__ == "__main__":
    pass
