FROM mysql:9

ENV MYSQL_ROOT_PASSWORD pass

COPY ./data.sql /docker-entrypoint-initdb.d/data.sql

EXPOSE 3306