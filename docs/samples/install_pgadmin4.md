# Install pgAdmin4

```
FABRIC_HOSTS='192.168.0.12'
FABRIC_USER='ubuntu'
FABRIC_SSH_KEY="${HOME}/.ssh/id_isucon12-qualify"
fab -r src/nuno -H "${FABRIC_HOSTS}" \
     -i ${FABRIC_SSH_KEY} \
     install-pgadmin4 \
     --email="dummy@xxx.io" --password="hoge" \
     | lltsv -k message -K | jq .
```
