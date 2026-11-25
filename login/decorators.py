"""Utilidades de permissão usadas pelas views do projeto."""

from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def is_admin(user):
    """Retorna True para superusuário, staff ou usuário com perfil administrador."""
    if not user.is_authenticated:
        return False

    if user.is_staff or user.is_superuser:
        return True

    # getattr com default cobre o caso de usuário sem Perfil
    perfil = getattr(user, 'perfil', None)
    return bool(perfil and perfil.tipo_usuario == 'administrador')


def admin_required(view):
    """Restringe a view a administradores; redireciona clientes para a dashboard."""

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')

        if not is_admin(request.user):
            messages.error(
                request,
                'Você não tem permissão para acessar esta página.',
            )
            return redirect('dashboard')

        return view(request, *args, **kwargs)

    return wrapper
