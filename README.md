# Mind Palace — Projeto Final WEB III (Django)

Sistema web desenvolvido em Django atendendo aos requisitos do projeto final:
Home, Quem Somos (Supabase), Produtos (banco local + API externa), Contato,
login com perfis, recuperação de senha, dashboard por permissões, CRUD de
serviços, CRUD de equipe (Supabase), meus pedidos e relatórios com gráficos.

## Requisitos

- Python 3.12+
- Dependências em `requirements.txt` (inclui Pillow, WhiteNoise e Gunicorn)

## Rodando localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env        # preencha SUPABASE_URL / SUPABASE_KEY
python manage.py migrate
python manage.py seed_demo  # opcional: categorias e serviços de exemplo
python manage.py createsuperuser  # opcional: a migração já cria o admin padrão
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/`.

### Acesso inicial (criado pela migração)

| Usuário | Senha | Perfil |
|---|---|---|
| `admin` | `admin123` | Superusuário / Administrador |

> Troque essa senha em produção (Django admin → usuário `admin` → alterar senha).


## Funcionalidades

| Página | Descrição |
|---|---|
| Home | Menu com Quem Somos, Produtos, Contato e Entrar |
| Quem Somos | Texto institucional + integrantes consultados no Supabase |
| Produtos | Produtos locais (com botão **Comprar** apenas para logados) e produtos da API externa (Fake Store API) |
| Contato | Formulário público de contato |
| Entrar | Login, recuperação de senha e cadastro |
| Dashboard | Menu conforme permissão: Editar Perfil, Contatos, Serviços, Equipe, Meus Pedidos e Relatórios |
| Serviços | Filtros (nome, categoria, preço, ordem), estatísticas e CRUD |
| Equipe | CRUD de integrantes no Supabase |
| Meus Pedidos | Itens comprados, quantidades, subtotais e total |
| Relatórios | Gráficos (Chart.js) e indicadores dos serviços |

### Perfis

- **Administrador** (`is_staff`/`is_superuser` ou `Perfil.tipo_usuario = administrador`):
  ao logar é redirecionado para `/admin/`.
- **Cliente**: ao logar é redirecionado para `/login/dashboard/`.

## Supabase

Tabela esperada `integrantes`:

```sql
create table integrantes (
  id uuid primary key default gen_random_uuid(),
  nome text not null,
  cargo text,
  biografia text,
  foto_url text
);
```

O cliente Supabase é opcional: se `SUPABASE_URL`/`SUPABASE_KEY` não estiverem
definidas, o site continua funcionando e a equipe aparece vazia.

## Deploy no Render

Variáveis de ambiente:

```
DEBUG=False
SECRET_KEY=<chave longa e aleatória>
ALLOWED_HOSTS=<seu-servico>.onrender.com
CSRF_TRUSTED_ORIGINS=https://<seu-servico>.onrender.com
SUPABASE_URL=https://<projeto>.supabase.co
SUPABASE_KEY=<chave>

# PostgreSQL do Render (Internal Database URL)
DATABASE_URL=postgresql://usuario:senha@host-interno:5432/banco

# opcionais
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=<senha>
DJANGO_SUPERUSER_EMAIL=admin@exemplo.com
SEED_DEMO=1
```

> Use a **Internal Database URL** do PostgreSQL do Render (host interno, sem SSL).
> A senha **não deve** ser colocada no código nem no GitHub — apenas nas
> variáveis de ambiente do Render.
> Sem `DATABASE_URL`, o projeto usa SQLite automaticamente (desenvolvimento local).

Build Command:

```bash
./build.sh
```

Start Command:

```bash
./start.sh
```

O `projeto/wsgi.py` também aplica as migrações automaticamente ao iniciar,
garantindo que o banco (PostgreSQL ou SQLite) tenha as tabelas mesmo que o
Start Command seja apenas `gunicorn projeto.wsgi:application`.

> Com `DATABASE_URL` configurada, o SQLite deixa de ser usado e todos os dados
> (usuários, serviços, pedidos, contatos) ficam no PostgreSQL do Render.

### Problemas com login (usuário deslogado / conta desaparece)

Sintomas: ao criar uma conta o usuário volta para o login, ou precisa criar
outra conta depois de algum tempo.

Causas mais comuns:

1. O Render está usando **SQLite efêmero** (sem `DATABASE_URL`) → contas e
   sessões são apagadas a cada deploy/reinício.
2. A `SECRET_KEY` mudava a cada boot → todos os cookies de sessão deixavam de
   valer.

Para diagnosticar, abra o **Shell** do Render e rode:

```bash
python manage.py verificar_sessao
```

A saída esperada em produção:

```
Banco de dados.....: PostgreSQL (...)
DATABASE_URL.......: definida
SECRET_KEY.........: variavel de ambiente
Sessões............: django.contrib.sessions.backends.db
Duração da sessão..: 30.0 dias
```

Se aparecer **SQLite** ou **NÃO definida**, configure as variáveis no painel
do Render (`DATABASE_URL` e `SECRET_KEY`) e faça um novo deploy.

Detalhes da configuração aplicada:

- Sessões gravadas no banco (`SESSION_ENGINE = db`), válidas por **30 dias** e
  renovadas a cada acesso.
- Sem `SECRET_KEY`, o projeto gera uma chave **estável** derivada do
  `DATABASE_URL`, em vez de uma chave aleatória a cada reinício.
- Após o cadastro o usuário já entra **automaticamente** no Dashboard.

### Migrar dados do SQLite para o PostgreSQL (opcional)

```bash
# 1) exporta os dados do banco local
python manage.py dumpdata --natural-foreign --natural-primary \
  -e contenttypes -e auth.Permission -e admin.logentry -e sessions.session \
  -o dados.json

# 2) importa no PostgreSQL do Render (use a External Database URL na sua máquina)
DATABASE_URL="postgresql://...URL-externa..." python manage.py loaddata dados.json
```

> O SQLite no Render é **efêmero**: os dados são reiniciados a cada deploy.
> Para persistência use um Render Disk ou PostgreSQL.
