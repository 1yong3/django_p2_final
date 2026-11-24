from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordResetView
from .forms import CadastroForm
from .models import Perfil

def custom_login(request):
    """Login view with role-based redirect"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # Role-based redirect
            try:
                perfil = Perfil.objects.get(usuario=user)
                if perfil.tipo_usuario == 'administrador':
                    return redirect('/admin/')
                else:
                    return redirect('/login/dashboard/')
            except:
                return redirect('/login/dashboard/')
        else:
            return render(request, 'login.html', {'form': form, 'error': 'Usuário ou senha inválidos'})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    perfil = Perfil.objects.get(usuario=request.user)
    if perfil.tipo_usuario == 'administrador':
        return redirect("/admin/")

    return render(request, "dashboard.html")

# Create your views 
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