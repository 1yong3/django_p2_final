from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView
from .forms import CadastroForm
from .models import Perfil


def custom_login(request):
    """Login com redirecionamento por tipo de usuário."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            # Administradores (superuser/staff/perfil admin) vão para o admin
            if user.is_superuser or user.is_staff:
                return redirect('/admin/')

            perfil = Perfil.objects.filter(usuario=user).first()
            if perfil and perfil.tipo_usuario == 'administrador':
                return redirect('/admin/')

            return redirect('/login/dashboard/')

        return render(
            request,
            'login.html',
            {'form': form, 'error': 'Usuário ou senha inválidos'}
        )

    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def dashboard(request):
    perfil, _ = Perfil.objects.get_or_create(
        usuario=request.user,
        defaults={'tipo_usuario': 'cliente'}
    )

    if (perfil.tipo_usuario == 'administrador'
            or request.user.is_superuser
            or request.user.is_staff):
        return redirect('/admin/')

    return render(request, "dashboard.html")


@login_required
def perfil(request):
    if request.method == "POST":
        usuario = request.user

        usuario.first_name = request.POST.get("nome")
        usuario.last_name = request.POST.get("sobrenome")
        usuario.email = request.POST.get("email")

        usuario.save()
        return redirect("dashboard")

    return render(request, "perfil.html")


def logout_view(request):
    auth_logout(request)
    return redirect('/login/')


def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)

        if form.is_valid():
            usuario = form.save()
            Perfil.objects.create(usuario=usuario, tipo_usuario='cliente')
            return redirect('login')
    else:
        form = CadastroForm()

    return render(request, 'cadastro.html', {'form': form})
