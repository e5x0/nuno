from fabric import Connection, task
from dataclasses import dataclass, asdict

import nuno.os.disk
import nuno.postgresql.ops
from nuno.common import NunoArgs


@task
def disk_free(c: Connection, ansbile_vars: dict | str = "{}"):
    nuno.os.disk.disk_free(c, NunoArgs(fabric_vars={}, ansible_vars=ansbile_vars))


@task
def postgresql_version(c: Connection, ansbile_vars: dict | str = "{}"):
    nuno.postgresql.ops.postgresql_version(
        c, NunoArgs(fabric_vars={}, ansible_vars=ansbile_vars)
    )


if __name__ == "__main__":
    pass
