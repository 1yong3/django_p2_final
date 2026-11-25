from django.db import migrations


# Novas imagens enviadas para media/servicos (ícones transparentes).
# O mapa usa o nome do produto como chave para atualizar os registros já
# existentes (tanto no SQLite local quanto no PostgreSQL do Render).
IMAGENS = {
    'palacio mental': 'servicos/images-removebg-preview (2).png',
    'palacio mental 2': 'servicos/pm_logo.png',
    'sdfsg': 'servicos/2232688-removebg-preview.png',
    'wsdgsdg': 'servicos/8832880-removebg-preview.png',
    'teste1': 'servicos/images-removebg-preview (1).png',
    'teste 3': 'servicos/2232688-removebg-preview.png',
    'teste 992': 'servicos/8832880-removebg-preview.png',
    'Site Institucional': 'servicos/8832880-removebg-preview.png',
    'Sistema de Gestão': 'servicos/2232688-removebg-preview.png',
    'Identidade Visual': 'servicos/images-removebg-preview (2).png',
    'Consultoria em TI': 'servicos/ic_ideia1-removebg-preview.png',
}


def atualizar_imagens(apps, schema_editor):
    Servico = apps.get_model('app', 'Servico')

    for nome, imagem in IMAGENS.items():
        Servico.objects.filter(nome=nome).update(imagem=imagem)


def reverter(apps, schema_editor):
    """Mantém as imagens atuais (as antigas foram removidas do projeto)."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_produtos_do_projeto'),
    ]

    operations = [
        migrations.RunPython(atualizar_imagens, reverse_code=reverter),
    ]
