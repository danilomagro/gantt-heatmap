# PM Workload Board — Prompt di Handoff per Claude Aziendale

## Contesto

Questo file è un prompt da dare in pasto a Claude (o altro AI) per continuare lo sviluppo
del tool `pm-workload-board.html` allegato.

---

## Cosa è questo tool

Un'applicazione web **standalone** (singolo file HTML, niente server, niente installazioni)
per visualizzare il carico di lavoro di un team di sviluppo su più progetti in parallelo.

**Problema che risolve:** un PM gestisce 7-8 progetti in manutenzione + implementazioni
massicce (durata 1-2+ settimane). Quando il management chiede perché i developer sono lenti,
serve un artefatto visivo **oggettivo e inattaccabile** che mostri le sovrapposizioni reali.

---

## Architettura tecnica

- **Stack:** HTML + React 18 (via CDN) + Babel standalone (compila JSX nel browser)
- **Storage:** `localStorage` del browser — i dati persistono tra sessioni
- **Zero dipendenze locali:** funziona offline dopo il primo caricamento, doppio click per aprire
- **Export/Import JSON:** per sincronizzare dati tra dispositivi diversi

---

## Struttura dati (localStorage, chiave `pm-gantt-v2`)

```json
{
  "t": [
    {
      "id": "timestamp string",
      "taskName": "Nome attività",
      "projectName": "Nome progetto",
      "resourceId": "id della risorsa",
      "startDate": "YYYY-MM-DD",
      "endDate": "YYYY-MM-DD"
    }
  ],
  "r": [
    { "id": "timestamp string", "name": "Nome risorsa" }
  ],
  "c": {
    "Nome progetto": "#HEX colore assegnato automaticamente"
  }
}
```

---

## Funzionalità attuali

**Sidebar sinistra:**
- Gestione risorse (persone): aggiungi / elimina
- Legenda progetti con colori auto-assegnati
- Form aggiunta/modifica attività (task name, progetto, risorsa, date inizio/fine)
- Lista attività con edit e delete
- Bottoni Export JSON / Import JSON

**Main area:**
- Toggle tre view: Gantt / Heatmap / Entrambi
- **Gantt:** timeline inter-progetto, raggruppato per risorsa, barre colorate per progetto,
  linea rossa = oggi, badge colorato sul nome risorsa (blu/giallo/rosso in base al numero task),
  click sulla barra = edit
- **Heatmap:** griglia risorsa × settimana, numero di attività parallele per cella,
  colori da blu (1) → giallo (2) → arancione (3) → rosso (4+), hover = tooltip con dettaglio

**Timeline:** calcolata automaticamente dalle date dei task (con padding di almeno 8 settimane).

---

## Decisioni di design rilevanti

- I colori dei progetti vengono assegnati automaticamente da una palette di 10 colori fissi
  (`COLORS` array), senza intervento dell'utente
- La heatmap è **derivata** dal Gantt, non compilata manualmente — questo è il punto chiave
  per la credibilità verso il management ("il rosso non lo decido io, lo decidono le barre")
- Dark theme: sfondo `#0A0F1E`, sidebar `#111827`
- Font: Segoe UI / system-ui (niente CDN font per funzionare offline)

---

## Possibili step di sviluppo futuro

Elencati in ordine di priorità suggerita:

1. **Stampa / export PDF** — bottone "Stampa" che apre il dialogo di stampa del browser
   ottimizzato (print CSS, sfondo dark preservato, sidebar nascosta)
2. **Filtro per risorsa** — mostrare nel Gantt solo una risorsa selezionata
3. **Milestone** — marker verticale con etichetta (es. "Go-live Progetto X") sovrapposto al Gantt
4. **Percentuale completamento** — barra con fill parziale + campo % nella card attività
5. **Note attività** — campo testo libero aggiuntivo, visibile nel tooltip hover della barra
6. **Multi-risorsa per task** — assegnare più risorse allo stesso task (attualmente 1:1)
7. **Settimane di zoom** — slider per allargare/restringere la timeline (attualmente fissa)
8. **Drag & drop date** — trascinare le barre per spostare le date (richiede libreria esterna
   o implementazione custom, complessità alta)

---

## Come usare questo prompt

1. Allega questo file `.md` + il file `pm-workload-board.html` a Claude
2. Scrivi: *"Leggi il file di handoff e il codice HTML allegato, poi implementa [feature X]"*
3. Claude restituirà il file HTML aggiornato da sostituire al precedente

**Nota:** il file HTML è self-contained, quindi ogni modifica produce un nuovo file completo
da sostituire integralmente — non patch parziali.
