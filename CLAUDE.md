# AI Berkshire — Istruzioni di Progetto (Versione EU/IT)

## Panoramica del Progetto

Raccolta di Skill per la ricerca sugli investimenti basata su Claude Code. Framework dei quattro maestri: Buffett, Munger, Duan Yongping, Li Lu.
Adattato per il mercato Europeo e Italiano.
GitHub: EngineerDogIta/ai-berkshire

## Struttura del Progetto

```
skills/          — Definizioni delle Skill (.md), copiare in ~/.claude/commands/ per l'uso
tools/           — Strumenti di supporto (financial_rigor.py per calcoli precisi)
reports/         — Output dei report di ricerca
assets/          — Immagini e risorse statiche
```

## Struttura della Directory dei Report

Tutti i report sono organizzati per **nome azienda**:

```
reports/
├── Ricerca_Settore_AI/
│   ├── AI_5_livelli_panorama-20260605.md
├── Ferrari/                 — Tutti i report su Ferrari
│   ├── Ferrari-research-20260408.md
│   ├── Ferrari-earnings-2025Q4.md
│   ├── Ferrari-management-20260409.md
│   └── Ferrari-thesis.md
├── Enel/                    — Tutti i report su Enel
├── LVMH/                    — Tutti i report su LVMH
├── Energia_Nucleare-industry-20260409.md
├── portfolio-latest.md      — Report del portafoglio nella root
```

## Principi Fondamentali di Analisi (Massima Priorità)

- **Oggettività assoluta** — Tutte le analisi devono basarsi su fatti e dati, vietate le speculazioni soggettive.
- Distinguere rigorosamente "fatti" e "opinioni": i fatti richiedono dati, le opinioni devono essere etichettate come tali.
- **Nessun pregiudizio**: non pre-impostare una visione rialzista o ribassista. Prima i dati, poi la logica, infine le conclusioni.
- **Mostrare entrambi i lati**: ogni giudizio chiave deve includere argomentazioni contrarie ("D'altra parte...").
- Essere onesti sull'incertezza: se mancano i dati, dire "dati insufficienti" piuttosto che inventare certezze.

## Lingua e Stile dei Report

- **TUTTI i report devono essere scritti in ITALIANO**.
- Stile: diretto, incisivo, senza giri di parole.
- I dati devono indicare la fonte, con validazione incrociata da almeno 2 fonti per i dati chiave.
- I valori stimati devono essere contrassegnati come "[Stima]".
- I punteggi usano il simbolo ★ (★1-5), senza mezze stelle.
- Includere citazioni di Buffett/Munger/Duan Yongping/Li Lu per commentare le situazioni.

## Attenzione

- La capitalizzazione di mercato deve essere verificata: Prezzo × Azioni totali.
- Chiarire sempre la valuta (EUR/USD/GBP) per evitare confusioni.
- Usare `tools/financial_rigor.py` per il calcolo preciso di indicatori come PE/ROE.
