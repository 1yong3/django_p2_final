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
python manage.py createsuperuser
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/`.

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
# opcionais
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=<senha>
DJANGO_SUPERUSER_EMAIL=admin@exemplo.com
SEED_DEMO=1
```

Build Command:

```bash
./build.sh
```

Start Command:

```bash
./start.sh
```

O `projeto/wsgi.py` também aplica as migrações automaticamente ao iniciar,
garantindo que o SQLite tenha as tabelas mesmo que o Start Command seja apenas
`gunicorn projeto.wsgi:application`.

> O SQLite no Render é **efêmero**: os dados são reiniciados a cada deploy.
> Para persistência use um Render Disk ou PostgreSQL.
