# Quiz e slide dal vivo — Cartografia della Parola

Due quiz dal vivo e le slide delle due parti della catechesi su come leggere la Bibbia, da seguire sul telefono. Nessun account per i partecipanti.

| Pagina | Per chi | Indirizzo |
|---|---|---|
| Slide della parte 1 / 2, in diretta | partecipanti | `slides.html?deck=1`, `slides.html?deck=2` |
| Regia delle slide, parte 1 / 2 | chi presenta (serve il PIN) | `regia.html?deck=1`, `regia.html?deck=2` |
| Schermo per il proiettore, parte 1 / 2 | chi presenta | `slides.html?deck=1&schermo=1`, `slides.html?deck=2&schermo=1` |
| Quiz 1 (parte 1, 12 domande) | partecipanti | `vote.html?quiz=1` |
| Quiz 2 (parte 2, 7 domande) | partecipanti | `vote.html?quiz=2` |
| Pannello del quiz 1 / 2 | chi presenta (serve il PIN) | `presenter.html?quiz=1`, `presenter.html?quiz=2` |
| Risposte di tutti, quiz 1 / 2 | chi presenta (serve il PIN) | `admin.html?quiz=1`, `admin.html?quiz=2` |
| Numeri dei partecipanti | chi presenta (serve il PIN) | `numeri.html` |
| Pagina iniziale (slide e quiz) | tutti | `index.html` |
| Approfondisci un brano da solo, con Claude, ChatGPT o Gemini | tutti, senza nome | `approfondisci.html` (anche `approfondisci.html?brano=Lc 5,1-11`) |

## Approfondisci un brano (`approfondisci.html`)

Pagina aperta a tutti, senza nome e senza Supabase. Si scrive il brano e si sceglie l'app:

- **Claude** (`claude.ai/new?q=…`) e **ChatGPT** (`chatgpt.com/?q=…`): il prompt arriva già scritto nella casella, si preme invio. Claude è stato provato da telefono; ChatGPT non ancora.
- **Gemini**: non accetta il testo nel link. La pagina copia il prompt negli appunti e apre Gemini; la persona lo incolla.
- «Copia solo il testo» serve per qualsiasi altra app. Il telefono ricorda l'ultimo brano scritto.

Il prompt è nella pagina stessa (funzione `PROMPT`) ed è lo stesso della slide 11 della parte 2: se cambi l'uno, cambia anche l'altro. Il prompt chiede all'app di leggere prima `metodo-lettura-bibbia.md`: la catechesi unificata in italiano controllato (regole ispirate ad ASD-STE100), servita come testo semplice da GitHub Pages. Il QR code della slide 12 (`slides/src/assets/qr-approfondisci.svg`) lo genera `make_slides.py`.

## Come funziona

- **Nome**: al primo accesso il partecipante scrive il suo nome. Il telefono riceve un codice casuale, salvato nel browser (memoria locale e cookie per un anno): ricaricando o riaprendo la pagina sullo stesso telefono e browser, nome e risposte restano. Il nome si può cambiare con «cambia».
- **Per ogni domanda** il presentatore: avvia → chiude i voti e mostra le percentuali (e quante persone per risposta, senza nomi) → mostra la risposta giusta, con la nota. Il quiz è solo testo: nessuna domanda ha un'immagine (le pagine sanno ancora mostrarla, se in futuro si mette un indirizzo nel campo `image`).
- **Numero**: insieme al nome, ogni telefono riceve un numero da 1 in su, diverso per ognuno. Resta lo stesso anche se la persona cambia nome (è legato al telefono e al browser, come il nome). Il partecipante lo vede in alto accanto al nome e nella schermata d'attesa. «Azzera tutto» cancella nomi e numeri: si riparte da 1.
- **Punteggio**: dopo ogni risposta rivelata il partecipante vede quante ne ha indovinate finora.
- **Classifica**: a quiz concluso, sullo schermo e sui telefoni compaiono i primi tre. A parità di risposte giuste vince chi ha risposto più in fretta. Ogni quiz ha la sua classifica (due vincitori).
- **Interrompere**: durante le domande, «⏹ Interrompi e mostra la classifica» chiude il quiz e mostra il podio. Contano solo le domande di cui è già stata mostrata la risposta giusta (se si interrompe durante il voto, quella domanda non vale); sui telefoni compare «Hai indovinato X su N» con N = domande che contano.
- **Azzerare**: «↺ Azzera questo quiz» (sempre disponibile, anche durante le domande) cancella i voti di quel quiz e torna all'inizio; «Azzera tutto» cancella i voti di entrambi, i nomi e i numeri. Ogni azzeramento e l'interruzione chiedono conferma con due pulsanti («Annulla» è quello selezionato, così un Invio per sbaglio non cancella niente).
- **Numeri dei partecipanti** (`numeri.html`, con PIN, si apre dal pannello con «🔢 Numeri dei partecipanti»): elenco numero e nome, con ricerca, stampa e download CSV. Si aggiorna da sola ogni 5 secondi.
- **Risposte di tutti** (`admin.html`, con PIN, si apre dal pannello con «📋 Risposte di tutti»): una riga per persona con la risposta data a ogni domanda (verde giusta, rosso sbagliata, tratteggiata se la soluzione non è ancora stata mostrata), il totale delle giuste e i secondi per lo spareggio; in fondo quanti hanno indovinato ogni domanda. Si aggiorna da sola ogni 5 secondi e si scarica in CSV per Excel.

## Slide dal vivo

- **Sincronia**: chi presenta va avanti e indietro dalla regia; i telefoni e lo schermo del proiettore restano sempre sulla stessa pagina e sullo stesso passo di animazione. Il cambio arriva subito (Supabase Realtime); se Realtime non risponde, i telefoni rileggono lo stato ogni 2 secondi (ogni 5 con Realtime attivo). Un telefono che si riaccende si rimette in pari da solo.
- **Passi di animazione**: nelle slide a schede, nell'iceberg, nei gradini, nella bussola e nelle tabelle gli elementi compaiono uno alla volta, a ogni «Avanti». In regia quelli non ancora mostrati si vedono in trasparenza.
- **Identità**: la stessa del quiz. Chi segue le slide scrive il nome una volta e riceve il suo numero fisso; nei quiz non deve riscriverlo.
- **Sul telefono**: in verticale la slide diventa una pagina che scorre, con il testo grande («🔤 Testo grande»); con «🖼️ Slide intera» si vede la slide com'è proiettata. Lo schermo resta acceso. I link nelle slide sono cliccabili. Sull'ultima slide di ogni parte compare il pulsante «Entra nel quiz».
- **Regia** (`regia.html`, stesso PIN del quiz): slide attuale, anteprima del prossimo clic, note per chi parla, pulsanti grandi Avanti/Indietro, salto a una slide, numero di telefoni collegati, QR code e link per i partecipanti, link allo schermo per il proiettore e, sull'ultima slide, al pannello del quiz. Funziona anche con la tastiera e con i telecomandi per presentazioni (→ ↓ Pagina giù Spazio = avanti; ← ↑ Pagina su = indietro). Si può aprire su più dispositivi insieme (per esempio portatile e telefono come telecomando): restano allineati.
- **Proiettore** (`slides.html?deck=N&schermo=1`): solo la slide, senza nome; doppio clic per lo schermo intero.

### Cambiare il testo delle slide

Il testo sta in `slides/src/parte-1.md` e `parte-2.md` (estratti del markdown delle slide del Project «Bibbia - come leggerla»: testo e note per chi parla). L'aspetto è `slides/src/slides.css`, identico a quello del PDF; le regole per il telefono sono in `slides/live.css`.

```
pip install markdown beautifulsoup4 qrcode
python3 slides/make_slides.py      # rigenera slides/deck-*.json, deck.css e i QR code
```

Per togliere i passi di animazione da una slide: `<!-- layout: cards; steps: no -->`.

## Dati (Supabase)

Tabelle `quiz_questions` (con `quiz` = 1 o 2), `quiz_keys` (risposta giusta, nota, immagine facoltativa: leggibili solo a risposta rivelata), `quiz_votes`, `quiz_players` (nome e numero fisso), `quiz_state` (una riga per quiz), `quiz_admin` (PIN), `slide_state` (pagina e passo attuali di ogni presentazione, si cambia con `slide_set` e il PIN; creata da `slides/slide-state.sql`).
Le domande si caricano con `quiz-seed.sql`, generato da `quiz-domande.md` (Project «Bibbia - come leggerla», cartella `cartografia-della-parola/quiz/`).
