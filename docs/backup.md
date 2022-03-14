# Backup

How to backup the database

## Docker container

Please, execute the following commands in a shell environment

```sh
# Define user name
export MARIADB_USERNAME=<user_name>

# Define user database password
export MARIADB_PASSWORD=<password>

# Execute the following
docker exec -it <container-name> mysqldump -u${MARIADB_USERNAME} -p${MARIADB_PASSWORD} --all-databases > yourdumpname.sql
```

Examplo:

```sh
docker exec -it livedivulgador_db mysqldump -ulivedivulgador -plivedevel123 --all-databases > mariadb-dump-$(date +%F_%H-%M-%S).sql
```
