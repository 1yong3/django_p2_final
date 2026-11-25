from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations


def criar_superusuario_admin(apps, schema_editor):
    """Cria (ou garante) o superusuário admin/admin123 e seu perfil."""
    User = apps.get_model('auth', 'User')
    Perfil = apps.get_model('login', 'Perfil')

    usuario, _ = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@exemplo.com'},
    )

    usuario.email = usuario.email or 'admin@exemplo.com'
    usuario.is_staff = True
    usuario.is_superuser = True
    usuario.is_active = True
    usuario.password = make_password('admin123')
    usuario.save()

    perfil, _ = Perfil.objects.get_or_create(
        usuario_id=usuario.pk,
        defaults={'tipo_usuario': 'administrador'},
    )

    if perfil.tipo_usuario != 'administrador':
        perfil.tipo_usuario = 'administrador'
        perfil.save(update_fields=['tipo_usuario'])


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_servico'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(
            criar_superusuario_admin,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
