# Quiz live — Cartografia della Parola

Due quiz dal vivo per la catechesi su come leggere la Bibbia, senza account per i partecipanti.

| Pagina | Per chi | Indirizzo |
|---|---|---|
| Quiz 1 (parte 1, 12 domande) | partecipanti | `vote.html?quiz=1` |
| Quiz 2 (parte 2, 7 domande) | partecipanti | `vote.html?quiz=2` |
| Pannello del quiz 1 / 2 | chi presenta (serve il PIN) | `presenter.html?quiz=1`, `presenter.html?quiz=2` |
| Scelta del quiz | tutti | `index.html` |

## Come funziona

- **Nome**: al primo accesso il partecipante scrive il suo nome. Il telefono riceve un codice casuale, salvato nel browser (memoria locale e cookie per un anno): ricaricando o riaprendo la pagina sullo stesso telefono e browser, nome e risposte restano. Il nome si può cambiare con «cambia».
- **Per ogni domanda** il presentatore: avvia → chiude i voti e mostra le percentuali (e quante persone per risposta, senza nomi) → mostra la risposta giusta, con la nota e, se c'è, un'immagine (domanda 2: il minatore di Prov 25,2).
- **Punteggio**: dopo ogni risposta rivelata il partecipante vede quante ne ha indovinate finora.
- **Classifica**: a quiz concluso, sullo schermo e sui telefoni compaiono i primi tre. A parità di risposte giuste vince chi ha risposto più in fretta. Ogni quiz ha la sua classifica (due vincitori).
- **Azzerare**: dal pannello, «Ricomincia questo quiz» o «Azzera i voti di questo quiz» cancella i voti di quel quiz; «Azzera tutto» cancella i voti di entrambi e i nomi.

## Dati (Supabase)

Tabelle `quiz_questions` (con `quiz` = 1 o 2), `quiz_keys` (risposta giusta, nota, immagine: leggibili solo a risposta rivelata), `quiz_votes`, `quiz_players`, `quiz_state` (una riga per quiz), `quiz_admin` (PIN).
Le domande si caricano con `quiz-seed.sql`, generato da `quiz-domande.md` (Project «Bibbia - come leggerla», cartella `cartografia-della-parola/quiz/`).
