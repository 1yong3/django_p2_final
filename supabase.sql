-- Tabela usada pela página "Quem Somos" e pelo CRUD de Equipe.
-- Execute no SQL Editor do Supabase.

create table if not exists public.integrantes (
  id uuid primary key default gen_random_uuid(),
  nome text not null,
  cargo text,
  biografia text,
  foto_url text,
  created_at timestamptz not null default now()
);

alter table public.integrantes enable row level security;

-- Leitura pública (site)
create policy "integrantes_leitura_publica"
  on public.integrantes for select
  using (true);

-- Escrita liberada para a chave usada pelo servidor (ajuste conforme seu caso)
create policy "integrantes_escrita"
  on public.integrantes for all
  using (true)
  with check (true);
