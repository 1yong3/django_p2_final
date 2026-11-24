from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.custom_login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("perfil/", views.perfil, name="perfil"),
    path("alterar-senha/", auth_views.PasswordChangeView.as_view(template_name="alterar_senha.html", success_url="/login/perfil/"), name="alterar_senha"),

    path('cadastro/', views.cadastro, name='cadastro'),
    path('recuperar-senha/', auth_views.PasswordResetView.as_view(template_name="recuperar_senha.html", success_url="/login/recuperar-senha/"), name="recuperar_senha"),
    path('redefinir-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="redefinir_senha.html"), name="redefinir_senha"),
]