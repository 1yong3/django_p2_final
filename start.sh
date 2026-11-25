#!/usr/bin/env bash
# Comando de start usado no Render.
set -o errexit

# Garante que as tabelas existam (SQLite é criado do zero a cada deploy)
python manage.py migrate --noinput

exec gunicorn projeto.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 120
