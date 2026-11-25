#!/usr/bin/env bash
# Script de build usado no deploy do Render.
# Execute com: chmod +x build.sh  (se necessário)

set -o errexit  # encerra em caso de erro

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput
