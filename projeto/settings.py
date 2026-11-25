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

# Em produção no Render, se DEBUG não for informado, assume False para não
# expor tracebacks e configurações sensíveis nas páginas de erro.
if os.getenv("RENDER") and "DEBUG" not in os.environ:
    DEBUG = False

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "django-insecure-chave-apenas-para-desenvolvimento"
    else:
        import secrets

        SECRET_KEY = secrets.token_urlsafe(50)
        print(
            "AVISO: SECRET_KEY não definida. Usando uma chave temporária; "
            "defina SECRET_KEY nas variáveis de ambiente para manter as sessões."
        )

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
# Em produção (Render/PostgreSQL) configure a variável DATABASE_URL com a
# "Internal Database URL" do seu banco. Sem ela, o projeto usa SQLite, ideal
# para desenvolvimento local.

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()


def _database_from_url(url):
    """Converte postgres://usuario:senha@host:porta/banco em config do Django."""
    from urllib.parse import parse_qs, unquote, urlparse

    parsed = urlparse(url)

    if parsed.scheme not in ("postgres", "postgresql"):
        raise ValueError(
            "DATABASE_URL deve começar com postgres:// ou postgresql://"
        )

    config = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": unquote(parsed.path.lstrip("/")),
        "USER": unquote(parsed.username or ""),
        "PASSWORD": unquote(parsed.password or ""),
        "HOST": parsed.hostname or "",
        "PORT": parsed.port or "",
        "CONN_MAX_AGE": int(os.getenv("DB_CONN_MAX_AGE", "600")),
        "CONN_HEALTH_CHECKS": True,
    }

    query = parse_qs(parsed.query)
    options = {}

    if query.get("sslmode"):
        options["sslmode"] = query["sslmode"][0]

    if options:
        config["OPTIONS"] = options

    return config


if DATABASE_URL:
    DATABASES = {"default": _database_from_url(DATABASE_URL)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
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

# Permite que o WhiteNoise encontre arquivos estáticos nos app dirs mesmo
# quando o collectstatic não for executado no build.
WHITENOISE_USE_FINDERS = True

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

# =====================================================
# LOGGING (exibe erros nos logs do Render)
# =====================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}