"""Popula o banco com categorias e serviços de demonstração."""

from decimal import Decimal

from django.core.management.base import BaseCommand

from app.models import Categoria, Servico


CATEGORIAS = [
    ('Desenvolvimento', 'Sites, sistemas e automações.'),
    ('Design', 'Identidade visual, UI e UX.'),
    ('Consultoria', 'Planejamento e apoio estratégico.'),
]

SERVICOS = [
    {
        'nome': 'Site Institucional',
        'descricao': 'Site responsivo com até 5 páginas, formulário de contato e SEO básico.',
        'preco': Decimal('1200.00'),
        'categoria': 'Desenvolvimento',
        'imagem': 'servicos/fundo-mindpalace.png',
    },
    {
        'nome': 'Sistema de Gestão',
        'descricao': 'Aplicação web para controle de clientes, serviços e pedidos.',
        'preco': Decimal('3500.00'),
        'categoria': 'Desenvolvimento',
        'imagem': 'servicos/mind_palace_logo.png',
    },
    {
        'nome': 'Identidade Visual',
        'descricao': 'Criação de logotipo, paleta de cores e manual de marca.',
        'preco': Decimal('800.00'),
        'categoria': 'Design',
        'imagem': 'servicos/Terry_Crews_by_Gage_Skidmore_5.jpg',
    },
    {
        'nome': 'Consultoria em TI',
        'descricao': 'Diagnóstico da infraestrutura e plano de melhorias.',
        'preco': Decimal('450.00'),
        'categoria': 'Consultoria',
        'imagem': 'servicos/Fotos-de-Macacos-2.jpg',
    },
]


class Command(BaseCommand):
    help = 'Cria categorias e serviços de demonstração (não duplica registros).'

    def handle(self, *args, **options):
        categorias = {}
        for nome, descricao in CATEGORIAS:
            categoria, _ = Categoria.objects.get_or_create(
                nome=nome,
                defaults={'descricao': descricao, 'ativo': True},
            )
            categorias[nome] = categoria

        criados = 0
        for dados in SERVICOS:
            _, criado = Servico.objects.get_or_create(
                nome=dados['nome'],
                defaults={
                    'descricao': dados['descricao'],
                    'preco': dados['preco'],
                    'categoria': categorias[dados['categoria']],
                    'imagem': dados['imagem'],
                    'ativo': True,
                },
            )
            criados += int(criado)

        self.stdout.write(
            self.style.SUCCESS(
                f'Dados de demonstração prontos ({criados} serviço(s) criado(s)).'
            )
        )
