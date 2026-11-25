#!/usr/bin/env bash
# Comando de start usado no Render.
set -o errexit

# Garante que as tabelas existam (SQLite é criado do zero a cada deploy).
python manage.py migrate --noinput

# Garante os arquivos estáticos (rápido e idempotente).
python manage.py collectstatic --noinput || true

exec gunicorn projeto.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 1 \
    --timeout 120
