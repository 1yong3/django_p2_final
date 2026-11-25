from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.custom_login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("perfil/", views.perfil, name="perfil"),

    path(
        "alterar-senha/",
        auth_views.PasswordChangeView.as_view(
            template_name="alterar_senha.html",
            success_url="/login/perfil/",
        ),
        name="alterar_senha",
    ),

    path("cadastro/", views.cadastro, name="cadastro"),

    # Recuperação de senha (mecanismo nativo do Django)
    path(
        "recuperar-senha/",
        auth_views.PasswordResetView.as_view(
            template_name="recuperar_senha.html",
            success_url="/login/recuperar-senha/enviado/",
        ),
        name="recuperar_senha",
    ),
    path(
        "recuperar-senha/enviado/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="recuperar_senha_enviado.html",
        ),
        name="password_reset_done",
    ),
    path(
        "redefinir-senha/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="redefinir_senha.html",
            success_url="/login/redefinir-senha/concluido/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "redefinir-senha/concluido/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="redefinir_senha_completo.html",
        ),
        name="password_reset_complete",
    ),
]
