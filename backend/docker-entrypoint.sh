#!/bin/sh
set -eu

python manage.py collectstatic --noinput --verbosity 0

# Миграции автоматически — только в dev (флаг в docker-compose.override.yml).
# В prod они запускаются вручную при деплое (SPEC, раздел 10.3).
if [ "${DJANGO_MIGRATE_ON_START:-0}" = "1" ]; then
    python manage.py migrate --noinput
fi

exec "$@"
