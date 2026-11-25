#!/usr/bin/env bash
# Comando de start usado no Render.
set -o errexit

# Sem DATABASE_URL o Render usa SQLite efêmero: contas e sessões somem a cada
# deploy/reinício. Avisa no log para facilitar o diagnóstico.
if [ -n "${RENDER:-}" ] && [ -z "${DATABASE_URL:-}" ]; then
    echo "AVISO: DATABASE_URL nao definida. Contas e sessoes NAO serao persistidas."
    echo "Configure a Internal Database URL do PostgreSQL no painel do Render."
fi

# Garante que as tabelas existam.
python manage.py migrate --noinput

# Garante os arquivos estáticos (rápido e idempotente).
python manage.py collectstatic --noinput || true

exec gunicorn projeto.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 1 \
    --timeout 120
