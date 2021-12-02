FROM mariadb

LABEL app="livedivulgador_db"

ADD ./db_sample.sql /docker-entrypoint-initdb.d
