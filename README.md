# Quiz live — Cartografia della Parola

Due quiz dal vivo per la catechesi su come leggere la Bibbia, senza account per i partecipanti.

| Pagina | Per chi | Indirizzo |
|---|---|---|
| Quiz 1 (parte 1, 12 domande) | partecipanti | `vote.html?quiz=1` |
| Quiz 2 (parte 2, 7 domande) | partecipanti | `vote.html?quiz=2` |
| Pannello del quiz 1 / 2 | chi presenta (serve il PIN) | `presenter.html?quiz=1`, `presenter.html?quiz=2` |
| Risposte di tutti, quiz 1 / 2 | chi presenta (serve il PIN) | `admin.html?quiz=1`, `admin.html?quiz=2` |
| Numeri dei partecipanti | chi presenta (serve il PIN) | `numeri.html` |
| Scelta del quiz | tutti | `index.html` |

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

## Dati (Supabase)

Tabelle `quiz_questions` (con `quiz` = 1 o 2), `quiz_keys` (risposta giusta, nota, immagine facoltativa: leggibili solo a risposta rivelata), `quiz_votes`, `quiz_players` (nome e numero fisso), `quiz_state` (una riga per quiz), `quiz_admin` (PIN).
Le domande si caricano con `quiz-seed.sql`, generato da `quiz-domande.md` (Project «Bibbia - come leggerla», cartella `cartografia-della-parola/quiz/`).
