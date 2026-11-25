"""Diagnóstico de persistência (banco de dados e sessões).

Usado pelo bootstrap do WSGI e pelo comando `python manage.py verificar_sessao`.
Nunca imprime senhas nem a SECRET_KEY.
"""

import os
from pathlib import Path

from django.conf import settings


def resumo():
    db = settings.DATABASES.get('default', {})
    engine = db.get('ENGINE', '?')

    if 'postgresql' in engine:
        tipo_banco = 'PostgreSQL'
    elif 'sqlite3' in engine:
        tipo_banco = 'SQLite'
    else:
        tipo_banco = engine

    nome = db.get('NAME')
    if isinstance(nome, Path):
        nome = str(nome)

    session_engine = settings.SESSION_ENGINE
    if 'db' in session_engine or 'cached_db' in session_engine:
        tipo_sessao = 'banco de dados (persistente quando o banco é persistente)'
    elif 'file' in session_engine:
        tipo_sessao = 'arquivo (efêmero no Render)'
    elif 'cache' in session_engine:
        tipo_sessao = 'cache (efêmero no Render)'
    else:
        tipo_sessao = session_engine

    return {
        'banco': tipo_banco,
        'nome_banco': nome,
        'host': db.get('HOST', ''),
        'database_url': bool(os.getenv('DATABASE_URL', '').strip()),
        'debug': settings.DEBUG,
        'secret_key': getattr(settings, 'SECRET_KEY_SOURCE', '?'),
        'sessao_engine': session_engine,
        'sessao_tipo': tipo_sessao,
        'sessao_dias': round(settings.SESSION_COOKIE_AGE / 86400, 1),
    }


def linha_bootstrap():
    dados = resumo()
    return (
        "[bootstrap] banco={banco} ({nome_banco}) | DATABASE_URL={database_url} "
        "| DEBUG={debug} | SECRET_KEY={secret_key} | sessoes={sessao_tipo} "
        "por {sessao_dias} dias"
    ).format(**dados)
