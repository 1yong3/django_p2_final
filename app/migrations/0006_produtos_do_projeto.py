from decimal import Decimal

from django.db import migrations


CATEGORIAS = [
    'Jogos',
    'Produto',
    'full stack',
    'Desenvolvimento',
    'Design',
    'Consultoria',
]

# Produtos que já existiam no banco local do projeto.
# (nome, descrição, preço, ativo, categoria, imagem)
PRODUTOS = [
    ('palacio mental', '', '0.00', True, None, 'servicos/fundo-mindpalace.png'),
    ('palacio mental 2', '', '12313.00', False, None, 'servicos/fundo-mindpalace_9hrWAnu.png'),
    ('sdfsg', '', '23423.00', False, None, 'servicos/Terry_Crews_by_Gage_Skidmore_5_uFVAzuF.jpg'),
    ('wsdgsdg', '', '3453.00', False, None, 'servicos/Fotos-de-Macacos-2_saq6sRU.jpg'),
    ('teste1', '', '2342.00', True, 'Jogos', 'servicos/werwr.jpg'),
    ('teste 3', '', '242.00', True, 'Produto', 'servicos/werwr_xAjQVRG.jpg'),
    ('teste 992', '', '5454.00', True, 'full stack', 'servicos/werwr_UKCuCNy.jpg'),
    (
        'Site Institucional',
        'Site responsivo com até 5 páginas, formulário de contato e SEO básico.',
        '1200.00',
        True,
        'Desenvolvimento',
        'servicos/fundo-mindpalace.png',
    ),
    (
        'Sistema de Gestão',
        'Aplicação web para controle de clientes, serviços e pedidos.',
        '3500.00',
        True,
        'Desenvolvimento',
        'servicos/mind_palace_logo.png',
    ),
    (
        'Identidade Visual',
        'Criação de logotipo, paleta de cores e manual de marca.',
        '800.00',
        True,
        'Design',
        'servicos/Terry_Crews_by_Gage_Skidmore_5.jpg',
    ),
    (
        'Consultoria em TI',
        'Diagnóstico da infraestrutura e plano de melhorias.',
        '450.00',
        True,
        'Consultoria',
        'servicos/Fotos-de-Macacos-2.jpg',
    ),
]


def criar_produtos(apps, schema_editor):
    """Recria no banco atual os produtos que existiam no projeto local."""
    Categoria = apps.get_model('app', 'Categoria')
    Servico = apps.get_model('app', 'Servico')

    categorias = {}
    for nome in CATEGORIAS:
        categoria, _ = Categoria.objects.get_or_create(
            nome=nome,
            defaults={'descricao': '', 'ativo': True},
        )
        categorias[nome] = categoria

    for nome, descricao, preco, ativo, categoria, imagem in PRODUTOS:
        Servico.objects.get_or_create(
            nome=nome,
            defaults={
                'descricao': descricao,
                'preco': Decimal(preco),
                'ativo': ativo,
                'categoria': categorias.get(categoria) if categoria else None,
                'imagem': imagem,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_categoria_options_alter_itempedido_options_and_more'),
    ]

    operations = [
        migrations.RunPython(
            criar_produtos,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
