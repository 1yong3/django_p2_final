"""
Django settings for projeto project.
Configuração para desenvolvimento local e produção no Render.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# =====================================================
# CAMINHOS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# =====================================================
# SEGURANÇA
# =====================================================

DEBUG = os.getenv("DEBUG", "True").lower() == "true"

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-chave-apenas-para-desenvolvimento"
)

if not DEBUG and SECRET_KEY == "django-insecure-chave-apenas-para-desenvolvimento":
    raise ValueError("Configure uma SECRET_KEY segura no Render.")

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "ALLOWED_HOSTS",
        "localhost,127.0.0.1,.onrender.com"
    ).split(",")
    if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CSRF_TRUSTED_ORIGINS",
        "https://*.onrender.com"
    ).split(",")
    if origin.strip()
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# =====================================================
# APLICATIVOS
# =====================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'app',
    'contato',
    'login',

    'rest_framework',
]

# =====================================================
# MIDDLEWARE
# =====================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =====================================================
# URLS E WSGI
# =====================================================

ROOT_URLCONF = 'projeto.urls'
WSGI_APPLICATION = 'projeto.wsgi.application'

# =====================================================
# TEMPLATES
# =====================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# =====================================================
# BANCO DE DADOS
# =====================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# =====================================================
# VALIDAÇÃO DE SENHAS
# =====================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# =====================================================
# INTERNACIONALIZAÇÃO
# =====================================================

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# =====================================================
# ARQUIVOS ESTÁTICOS - RENDER
# =====================================================

STATIC_URL = '/static/'

# Pasta onde o collectstatic reunirá os arquivos
STATIC_ROOT = BASE_DIR / 'staticfiles'

# =====================================================
# ARQUIVOS DE MÍDIA
# =====================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =====================================================
# E-MAIL
# =====================================================

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}

# =====================================================
# AUTENTICAÇÃO
# =====================================================

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/login/dashboard"
LOGOUT_REDIRECT_URL = "/login/"

# =====================================================
# REDIRECIONAMENTO POR TIPO DE USUÁRIO
# =====================================================

def get_role_based_redirect(user):
    try:
        from login.models import Perfil

        perfil = Perfil.objects.get(usuario=user)

        if perfil.tipo_usuario == 'administrador':
            return '/admin/'

        return '/login/dashboard/'

    except Exception:
        return '/login/dashboard/'

# =====================================================
# CONFIGURAÇÃO PADRÃO
# =====================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'