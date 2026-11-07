// Slide dal vivo — codice comune a slides.html (telefoni e proiettore) e regia.html (chi presenta).
// Lo stato (pagina e passo di animazione) sta su Supabase, tabella slide_state: una riga per presentazione.
// I telefoni lo ricevono subito con Realtime e, per sicurezza, lo rileggono ogni pochi secondi.
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

export const SUPABASE_URL = 'https://igadvmjzyrylaxpacrew.supabase.co';
export const SUPABASE_KEY = 'sb_publishable_fIO4K5Q3L63lnp4iuwn_hw_qZOc0NAb';
export const sb = createClient(SUPABASE_URL, SUPABASE_KEY, { auth: { persistSession: false } });

export const TITLES = { 1: 'Parte 1 · Cartografia della Parola', 2: 'Parte 2 · Come approcciare il testo biblico' };
export const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
export const W = 1376, H = 768;

// Il numero della presentazione dall'indirizzo: ?deck=1 oppure ?deck=2 (anche ?parte=2).
export function deckFromUrl() {
  const p = new URLSearchParams(location.search);
  return (p.get('deck') || p.get('parte')) === '2' ? 2 : 1;
}

const cache = {};
export async function loadDeck(deck, withNotes = false) {
  const key = deck + (withNotes ? 'n' : '');
  if (cache[key]) return cache[key];
  const url = f => new URL(`slides/${f}`, location.href).href + '?v=' + (window.SLIDES_VERSION || '');
  const d = await (await fetch(url(`deck-${deck}.json`))).json();
  if (withNotes) { try { d.notes = await (await fetch(url(`deck-${deck}-note.json`))).json(); } catch { d.notes = []; } }
  return (cache[key] = d);
}

// ---- disegno di una pagina ----------------------------------------------------------------
// host: elemento .deck. Ridisegna l'HTML solo se cambia pagina; per i passi accende i frammenti.
export function showPage(host, page, step, { scrollToNew = false } = {}) {
  if (!page) { host.innerHTML = ''; return; }
  const changed = host.dataset.page !== String(page.__i);
  if (changed) {
    host.innerHTML = page.html;
    host.dataset.page = String(page.__i);
    host.firstElementChild?.classList.add('enter');
  }
  let newest = null;
  host.querySelectorAll('.frag').forEach(el => {
    const on = Number(el.dataset.f) <= step;
    if (on && !el.classList.contains('on')) newest = el;
    el.classList.toggle('on', on);
  });
  if (changed && scrollToNew) window.scrollTo({ top: 0 });
  else if (newest && scrollToNew) setTimeout(() => newest.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 60);
  return changed;
}

// Mette la slide (1376×768) in scala dentro box, senza deformarla. Restituisce la scala.
export function fitFrame(frame, box, maxScale = 3) {
  const s = Math.min(box.clientWidth / W, (box.clientHeight || 1e9) / H, maxScale);
  frame.style.width = W * s + 'px';
  frame.style.height = H * s + 'px';
  frame.firstElementChild.style.transform = `scale(${s})`;
  return s;
}

export function numberPages(d) { d.pages.forEach((p, i) => { p.__i = i; }); return d; }

// ---- seguire lo stato --------------------------------------------------------------------
// onState({slide, step, updated_at}) a ogni cambiamento; onLink(true/false) per il pallino «in diretta».
export function follow(deck, onState, onLink = () => {}) {
  let last = '', lastT = 0, live = false, timer = null;
  const apply = row => {
    if (!row) return;
    const k = `${row.slide}|${row.step}`, t = Date.parse(row.updated_at) || 0;
    if (t < lastT) return;                                       // risposta vecchia arrivata tardi
    lastT = t;
    if (k === last) return;
    last = k;
    onState(row);
  };
  const poll = async () => {
    try {
      const { data, error } = await sb.from('slide_state').select('slide, step, updated_at').eq('id', deck).single();
      if (error) throw error;
      apply(data); onLink(true);
    } catch { onLink(false); }
  };
  const schedule = () => { clearInterval(timer); timer = setInterval(poll, live ? 5000 : 2000); };
  // Il timer si cambia solo quando Realtime si collega o si scollega: i tentativi di riconnessione,
  // che arrivano spesso, non devono azzerarlo (altrimenti la lettura di riserva non partirebbe mai).
  sb.channel(`slide-state-${deck}`)
    .on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'slide_state', filter: `id=eq.${deck}` }, p => { apply(p.new); onLink(true); })
    .subscribe(status => {
      const now = status === 'SUBSCRIBED';
      if (now === live) return;
      live = now; schedule(); poll();
    });
  poll(); schedule();
  document.addEventListener('visibilitychange', () => { if (!document.hidden) poll(); });   // telefono riacceso: si rimette in pari
  return { poll };
}

// ---- presenza: quanti telefoni stanno seguendo --------------------------------------------
export function presence(deck, key, meta, onCount) {
  const ch = sb.channel(`slide-presenza-${deck}`, { config: { presence: { key: key || 'regia' } } });
  ch.on('presence', { event: 'sync' }, () => onCount && onCount(Object.keys(ch.presenceState()).length));
  ch.subscribe(async status => { if (status === 'SUBSCRIBED' && meta) await ch.track(meta); });
  return ch;
}
