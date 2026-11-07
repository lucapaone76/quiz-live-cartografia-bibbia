-- Slide dal vivo: stato condiviso (pagina e passo di animazione), una riga per presentazione.
-- Lo cambia solo chi conosce il PIN (lo stesso del quiz, tabella quiz_admin); tutti lo leggono.
create table if not exists public.slide_state (
  id int primary key,               -- 1 = parte 1, 2 = parte 2
  slide int not null default 0,      -- indice della pagina (da 0)
  step int not null default 0,       -- passo di animazione nella pagina
  updated_at timestamptz not null default now()
);
insert into public.slide_state (id) values (1), (2) on conflict do nothing;
alter table public.slide_state enable row level security;
drop policy if exists "read slide state" on public.slide_state;
create policy "read slide state" on public.slide_state for select to anon, authenticated using (true);
grant select on public.slide_state to anon, authenticated;

create or replace function public.slide_set(p_pin text, p_deck int, p_slide int, p_step int)
returns void language plpgsql security definer set search_path to '' as $$
begin
  if not exists (select 1 from public.quiz_admin where pin = p_pin) then raise exception 'pin errato'; end if;
  update public.slide_state set slide = greatest(p_slide, 0), step = greatest(p_step, 0), updated_at = now() where id = p_deck;
end $$;
revoke all on function public.slide_set(text, int, int, int) from public;
grant execute on function public.slide_set(text, int, int, int) to anon, authenticated;

-- Realtime: i telefoni ricevono subito ogni cambio di pagina.
do $$ begin
  if not exists (select 1 from pg_publication where pubname = 'supabase_realtime') then
    create publication supabase_realtime;
  end if;
  if not exists (select 1 from pg_publication_tables where pubname = 'supabase_realtime' and tablename = 'slide_state') then
    alter publication supabase_realtime add table public.slide_state;
  end if;
end $$;
