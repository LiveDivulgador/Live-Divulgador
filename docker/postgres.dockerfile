FROM postgres

ADD ./dump.sql /docker-entrypoint-initdb.d
