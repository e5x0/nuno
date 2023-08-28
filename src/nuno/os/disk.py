from fabric import Connection, task


def disk_free(c: Connection):
    uname = c.run("uname -s", hide=True)
    if "Linux" in uname.stdout:
        command = "df -h / | tail -1 | awk '{print $5}'"
        print(c.run(command, hide=True).stdout.strip())
        return
    err = "No idea how to get disk space on {}!".format(uname)
    print(err)


if __name__ == "__main__":
    print(disk_free(Connection("localhost")))
