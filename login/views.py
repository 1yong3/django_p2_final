from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .decorators import is_admin
from .forms import CadastroForm
from .models import Perfil


def _redirect_for(user):
    """Administrador -> Django admin; cliente -> Dashboard."""
    if is_admin(user):
        return '/admin/'
    return '/login/dashboard/'


def _next_is_safe(request, next_url):
    return url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    )


def custom_login(request):
    """Login com redirecionamento por tipo de usuário."""
    if request.user.is_authenticated:
        return redirect(_redirect_for(request.user))

    next_url = request.POST.get('next') or request.GET.get('next') or ''

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            # Cliente que veio de uma página protegida volta para ela.
            if next_url and _next_is_safe(request, next_url) and not is_admin(user):
                return redirect(next_url)

            return redirect(_redirect_for(user))

        messages.error(request, 'Usuário ou senha inválidos.')

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form, 'next': next_url})


@login_required
def dashboard(request):
    """Dashboard do cliente com as seções disponíveis por permissão."""
    perfil, _ = Perfil.objects.get_or_create(
        usuario=request.user,
        defaults={'tipo_usuario': 'cliente'},
    )

    total_pedidos = request.user.pedidos.count()

    return render(request, 'dashboard.html', {
        'perfil': perfil,
        'e_admin': is_admin(request.user),
        'total_pedidos': total_pedidos,
    })


@login_required
def perfil(request):
    if request.method == 'POST':
        usuario = request.user

        usuario.first_name = (request.POST.get('nome') or '').strip()
        usuario.last_name = (request.POST.get('sobrenome') or '').strip()
        usuario.email = (request.POST.get('email') or '').strip()

        usuario.save()
        messages.success(request, 'Perfil atualizado com sucesso.')
        return redirect('dashboard')

    return render(request, 'perfil.html')


def logout_view(request):
    auth_logout(request)
    messages.success(request, 'Você saiu do sistema.')
    return redirect('/login/')


def cadastro(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CadastroForm(request.POST)

        if form.is_valid():
            usuario = form.save()
            Perfil.objects.get_or_create(
                usuario=usuario,
                defaults={'tipo_usuario': 'cliente'},
            )
            messages.success(request, 'Conta criada com sucesso. Faça login.')
            return redirect('login')
    else:
        form = CadastroForm()

    return render(request, 'cadastro.html', {'form': form})
