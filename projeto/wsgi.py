"""
WSGI config for projeto project.

Inclui um bootstrap de produção: garante que as migrações sejam aplicadas
(mesmo que o comando de start do Render seja apenas o gunicorn) e cria o
superusuário a partir de variáveis de ambiente, quando informadas.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto.settings')

application = get_wsgi_application()


def _bootstrap():
    from django.core.management import call_command

    try:
        call_command('migrate', interactive=False, verbosity=0)
    except Exception as exc:  # pragma: no cover - apenas log em produção
        print(f'AVISO: falha ao aplicar migrações automaticamente: {exc}')

    username = os.getenv('DJANGO_SUPERUSER_USERNAME')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

    if username and password:
        try:
            from django.contrib.auth import get_user_model

            User = get_user_model()
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username,
                    email=os.getenv('DJANGO_SUPERUSER_EMAIL', ''),
                    password=password,
                )
                print(f'Superusuário "{username}" criado.')
        except Exception as exc:  # pragma: no cover
            print(f'AVISO: não foi possível criar o superusuário: {exc}')

    if os.getenv('SEED_DEMO', '').lower() in ('1', 'true', 'yes', 'sim'):
        try:
            call_command('seed_demo', verbosity=0)
        except Exception as exc:  # pragma: no cover
            print(f'AVISO: não foi possível popular dados de demonstração: {exc}')


if os.getenv('SKIP_AUTO_BOOTSTRAP', '0') != '1':
    _bootstrap()
