# Fabric tasks for foreign data wrapper of PostgreSQL

## Install sqlite_fdw for PostgreSQL
```
FABRIC_HOSTS='192.168.0.12'
FABRIC_USER='ubuntu'
FABRIC_SSH_KEY="${HOME}/.ssh/id_isucon12-qualify"
TASK='install-sqlite-fdw'
fab -r src/nuno -H "${FABRIC_HOSTS}" \
     -i ${FABRIC_SSH_KEY} \
     ${TASK} | lltsv -k message -K | jq .
```

## Install mysql_fdw for PostgreSQL
```
FABRIC_HOSTS='192.168.0.12'
FABRIC_USER='ubuntu'
FABRIC_SSH_KEY="${HOME}/.ssh/id_isucon12-qualify"
TASK='install-mysql-fdw'
fab -r src/nuno -H "${FABRIC_HOSTS}" \
     -i ${FABRIC_SSH_KEY} \
     ${TASK} | lltsv -k message -K | jq .
```
