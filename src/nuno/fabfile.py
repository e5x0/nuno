from fabric import Connection, task

import nuno.os.disk


@task
def disk_free(c: Connection):
    nuno.os.disk.disk_free(c)


if __name__ == "__main__":
    pass
