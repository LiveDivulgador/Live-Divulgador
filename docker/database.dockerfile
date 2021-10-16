FROM mariadb

ADD ./dump.sql /docker-entrypoint-initdb.d
