# Database

This section describes how to handle new database entries.

## How to handle database updates

The bot database is defined within a container. In order for the database production environment to be updated, you need to register its latest iteration in the official [livedivulgador registry](https://hub.docker.com/u/livedivulgador).

This can be done by executing the following command:

```sh
docker push livedivulgador/livedivulgador_db
```

## How to update the local environment database

Simply update the [docker-compose.yml](../docker-compose.yml#L18) declaration with the latest tag for the database container.

## How to backup the database

Please, execute the following commands in a shell environment

```sh
divulgador backup
```

This will create a backup record inside of the `backups` folder.

Otherwise you can create a new backup manually by executing the following commands:

```sh
# Define user name
export MARIADB_USERNAME=<user_name>

# Define user database password
export MARIADB_PASSWORD=<password>

# Execute the following
docker exec -it <container-name> mysqldump -u${MARIADB_USERNAME} -p${MARIADB_PASSWORD} --all-databases > yourdumpname.sql

```

Example:

```sh
docker exec -it livedivulgador_db mysqldump -ulivedivulgador -plivedevel123 --all-databases > mariadb-dump-$(date +%F_%H-%M-%S).sql
```
