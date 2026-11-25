import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.utils import timezone

from projeto.diagnostico import resumo


class Command(BaseCommand):
    help = (
        'Mostra onde estão o banco e as sessões e verifica se os logins '
        'vão sobreviver a um reinício do Render.'
    )

    def handle(self, *args, **options):
        dados = resumo()

        self.stdout.write('')
        self.stdout.write(self.style.MIGRATE_HEADING('=== Diagnóstico ==='))
        self.stdout.write(f"Banco de dados.....: {dados['banco']} ({dados['nome_banco']})")
        if dados['host']:
            self.stdout.write(f"Host...............: {dados['host']}")
        self.stdout.write(
            f"DATABASE_URL.......: {'definida' if dados['database_url'] else 'NÃO definida'}"
        )
        self.stdout.write(f"DEBUG..............: {dados['debug']}")
        self.stdout.write(f"SECRET_KEY.........: {dados['secret_key']}")
        self.stdout.write(f"Sessões............: {dados['sessao_engine']}")
        self.stdout.write(f"Duração da sessão..: {dados['sessao_dias']} dias")

        User = get_user_model()
        total_usuarios = User.objects.count()
        total_sessoes = Session.objects.filter(expire_date__gte=timezone.now()).count()

        self.stdout.write(f"Usuários...........: {total_usuarios}")
        self.stdout.write(f"Sessões ativas.....: {total_sessoes}")

        self.stdout.write('')
        self.stdout.write(self.style.MIGRATE_HEADING('=== Recomendações ==='))

        no_render = bool(os.getenv('RENDER'))

        if 'sqlite' in dados['banco'].lower():
            if no_render:
                self.stdout.write(self.style.ERROR(
                    'O Render usa SQLite sem disco persistente. Contas e sessões '
                    'são apagadas a cada deploy/reinício. Configure a variável '
                    'DATABASE_URL com a Internal Database URL do PostgreSQL.'
                ))
            else:
                self.stdout.write(
                    'Desenvolvimento local com SQLite: normal. No Render, '
                    'configure DATABASE_URL para persistir os dados.'
                )
        elif not dados['database_url']:
            self.stdout.write(self.style.ERROR(
                'DATABASE_URL não definida: o banco fica no SQLite efêmero do '
                'Render. Configure a Internal Database URL do PostgreSQL.'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                'Banco persistente configurado: contas e sessões sobrevivem ao deploy.'
            ))

        if 'derivada' in dados['secret_key']:
            self.stdout.write(self.style.WARNING(
                'SECRET_KEY não definida. Foi gerada uma chave estável a partir do '
                'DATABASE_URL, mas o ideal é definir SECRET_KEY nas variáveis de '
                'ambiente do Render.'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                'SECRET_KEY vinda das variáveis de ambiente (estável entre reinícios).'
            ))

        self.stdout.write('')
