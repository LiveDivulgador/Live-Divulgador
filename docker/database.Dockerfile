FROM mariadb

LABEL app="livedivulgador_db"

ADD ./dump.sql /docker-entrypoint-initdb.d
