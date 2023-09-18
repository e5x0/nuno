# nuno

## Usage

```bash
$ make pre
$ source .venv/bin/activate

$ fab -r src/nuno --list
Available tasks:

  ...
```

```bash
$ FABRIC_HOSTS='<host1>,<host2>,<host3>,...'
FABRIC_USER='<ssh_user>'
FABRIC_SSH_KEY="<ssh_key>"
TASK='disk-free'
fab -r src/nuno -H "${FABRIC_HOSTS}" \
     -i ${FABRIC_SSH_KEY} \
     ${TASK}
```

