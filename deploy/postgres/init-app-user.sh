#!/bin/sh
# Создаёт отдельного пользователя приложения с правами только на свою базу (SPEC 11.3).
# Выполняется образом postgres один раз — при инициализации пустого тома.
set -eu

: "${APP_DB_NAME:?не задана APP_DB_NAME}"
: "${APP_DB_USER:?не задана APP_DB_USER}"
: "${APP_DB_PASSWORD:?не задана APP_DB_PASSWORD}"

if [ "$APP_DB_USER" = "$POSTGRES_USER" ]; then
    echo "APP_DB_USER должен отличаться от суперпользователя POSTGRES_USER" >&2
    exit 1
fi

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
    -v app_db="$APP_DB_NAME" \
    -v app_user="$APP_DB_USER" \
    -v app_password="$APP_DB_PASSWORD" \
    -v maint_db="$POSTGRES_DB" <<'EOSQL'
CREATE ROLE :"app_user" LOGIN PASSWORD :'app_password'
    NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS;
CREATE DATABASE :"app_db" OWNER :"app_user";
REVOKE ALL ON DATABASE :"app_db" FROM PUBLIC;
REVOKE CONNECT ON DATABASE :"maint_db" FROM PUBLIC;
\connect :"app_db"
ALTER SCHEMA public OWNER TO :"app_user";
REVOKE ALL ON SCHEMA public FROM PUBLIC;
EOSQL
