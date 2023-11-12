## PostgreSQL createdb

```
FABRIC_HOSTS='192.168.0.12'
FABRIC_USER='ubuntu'
FABRIC_SSH_KEY="${HOME}/.ssh/id_isucon12-qualify"
fab -r src/nuno -H "${FABRIC_HOSTS}" \
     -i ${FABRIC_SSH_KEY} \
     createdb-pgsql \
     --dbname="nunodb" \
     | lltsv -k message -K | jq .

```
