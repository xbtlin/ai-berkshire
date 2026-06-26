Di seguito la traduzione in italiano del README principale del progetto.

# AI Berkshire - Framework di Ricerca sul Value Investing nell'Era dell'AI

> "Il prezzo è quello che paghi, il valore è quello che ottieni." — Warren Buffett
> 
> Ridefinire la profondità e l'efficienza della ricerca sugli investimenti con l'AI.

**AI Berkshire** è una raccolta di Skill per la ricerca sugli investimenti basata su [Claude Code](https://claude.ai/code). Sistematizza e struttura le metodologie di quattro maestri del value investing — Buffett, Munger, Duan Yongping e Li Lu — fornendo una ricerca sugli investimenti di livello professionale attraverso Agenti AI.

Una persona + Claude = un intero team di ricerca sugli investimenti.

---

## Track Record Reale

> Non si tratta di teoria sulla carta. Questo framework è supportato da un sistema di investimento verificato con denaro reale.

### Rendimento per l'intero anno 2024: +69.29%
### Rendimento del 2025 ad oggi: +66.38%

### Confronto con i principali indici

| Indicatore | 2024 Intero Anno | 2025 Ad oggi |
| --- | --- | --- |
| **Questo framework (Reale)** | **+69.29%** | **+66.38%** |
| Indice Hang Seng | +17.67% | +27.77% |
| S&P 500 | +23.31% | +16.39% |
| CSI 300 | +14.68% | +17.66% |
| NASDAQ | +28.64% | +20.36% |

**Extra-rendimento 2024**: Ha battuto l'S&P 500 di **46 punti percentuali**, ha battuto l'Hang Seng di **52 punti percentuali**.

**Extra-rendimento 2025**: Ha battuto l'S&P 500 di **50 punti percentuali**, ha battuto l'Hang Seng di **39 punti percentuali**.

**I rendimenti reali cumulativi in due anni superano 1,46 milioni di RMB**, sovraperformando significativamente i principali indici globali per due anni consecutivi.

> *Disclaimer: I rendimenti storici non sono indicativi delle performance future. Gli screenshot provengono da un conto reale su Futu Securities.*

---

## Perché non si può semplicemente chiedere all'AI?

Certamente puoi chiedere direttamente a Claude: "Aiutami ad analizzare se vale la pena comprare Pinduoduo". Otterrai un'analisi equilibrata del tipo "da un lato... dall'altro...", che si concluderà con "gli investimenti comportano rischi, si prega di valutare autonomamente".

**Questo tipo di analisi sembra corretta, ma non può essere utilizzata per prendere decisioni.**

AI Berkshire non risolve il problema del "se si può analizzare", ma il problema della **qualità dell'analisi e della disciplina decisionale**. Ecco le differenze fondamentali:

### 1. Forza una conclusione, senza giri di parole

Chiedendo direttamente all'AI, ottieni un'"analisi" che cerca di accontentare tutti. AI Berkshire forza un output: **Passa / Non passa / Zona grigia**, con fasce di prezzo specifiche e raccomandazioni stratificate.

> Risposta di un'AI normale: *"Pinduoduo ha potenziale di crescita ma affronta anche pressioni competitive, gli investitori devono soppesare..."*
> 
> Output di AI Berkshire:

> | Strategia | Raccomandazione | Fascia di prezzo |
> | --- | --- | --- |
> | Aggressiva | Costruire una posizione del 20% al prezzo attuale | $95-105 |
> | Prudente | Attendere la chiarezza sulla politica di buyback | $85-95 |
> | Conservativa | Non soddisfa lo standard di certezza a 10 anni, osservare | — |
> 
> **Test dello specchio**: Se non riesci a dirlo compiutamente in 5 frasi = non comprare, senza eccezioni.

### 2. Scontro tra le prospettive di quattro maestri, non un'analisi singola

Non è semplice come "analizza usando il metodo di Buffett". Le quattro prospettive creano **vere contraddizioni e tensioni** —

Prendiamo Pinduoduo come esempio:
* **Duan Yongping** (Modello di business): Ottimo business, modello C2M difficile da replicare → Punteggio 3.7/5
* **Buffett** (Valutazione finanziaria): P/E al netto della cassa a solo 6.3x, una macchina da soldi → Punteggio 4.4/5
* **Munger** (Pensiero inverso): Il fossato economico (moat) è più superficiale del previsto, Douyin ha raggiunto 4 trilioni di GMV in 3 anni → Punteggio 3.5/5
* **Li Lu** (Certezza a lungo termine): Pericoli nascosti nella cultura del management, incertezza tra 10 anni → Punteggio 2.0/5

**Buffett dice "veramente economico", Li Lu dice "se non sei sicuro non comprare"** — questo conflitto è il vero stato delle decisioni di investimento. Un singolo prompt non può creare questo scontro multi-prospettiva, che è esattamente la chiave per evitare punti ciechi.

### 3. Meccanismi strutturati contro i bias

Il pericolo maggiore dell'AI non è dare una risposta sbagliata, ma dare una risposta **che sembra corretta ma non regge a un esame approfondito**. AI Berkshire ha integrato nel suo processo vari livelli di meccanismi "anti-inganno":

| Meccanismo | Problema risolto | Esempio |
| --- | --- | --- |
| **Valutazione della ricchezza informativa (A/B/C)** | Previene l'illusione "tanti dati = alta certezza" | Pop Mart valutato B: dati limitati, indicatori stimati contrassegnati con livello di confidenza |
| **Test inverso in stile Munger** | Forza a pensare agli scenari di fallimento | "In quali circostanze Pinduoduo morirebbe?" → Elenca 5 scenari e probabilità |
| **Lista di rifiuto rapido** | 8 linee rosse per il veto immediato | Macchia sull'integrità del management → rifiuto diretto, non importa quanto sia economica la valutazione |
| **Controllo anti-consenso** | Evita di pensare come il mercato | "Perché le persone intelligenti stanno vendendo allo scoperto?" → Scopre rischi trascurati |
| **Principio dello spazio bianco** | Meglio dire "non lo so" | Contrassegna "zona grigia" quando i dati sono insufficienti, senza usare supposizioni per simulare certezza |

### 4. Precisione dei dati finanziari

Il calcolo mentale dei LLM non è affidabile. Sbagliare un decimale nel calcolo del P/E o confondere i dollari di Hong Kong con i Renminbi per la capitalizzazione di mercato può portare a decisioni di investimento errate.

**Caso reale**: Analizzando Tencent, diverse fonti avevano dati di capitalizzazione di mercato in "miliardi di HKD" e "miliardi di RMB". L'approccio di AI Berkshire:

```bash
# Verifica manuale della capitalizzazione di mercato: Prezzo × Azioni totali, confrontato con i dati del report
python3 tools/financial_rigor.py verify-market-cap \
  --price 510 --shares 9.11e9 --reported 4.65e12 --currency HKD
# ✅ Verifica superata, deviazione solo dello 0.08%
```

Tutti i calcoli utilizzano `decimal.Decimal` (decimale preciso) di Python, non `float`. I dati chiave vengono sottoposti a validazione incrociata da almeno 2 fonti indipendenti.

### 5. Processo di ricerca riproducibile

Chiedendo direttamente all'AI, il formato, la profondità e la copertura dell'output sono diversi ogni volta — oggi l'analisi di Tencent ha un punteggio sul fossato economico, domani l'analisi di Meituan potrebbe dimenticarlo.

AI Berkshire garantisce: **Stesso input → output coerente nella struttura e nella profondità**. Questo significa che puoi:
* Confrontare orizzontalmente 7 aziende, con criteri di punteggio completamente coerenti
* Rianalizzare la stessa azienda dopo sei mesi, confrontando direttamente i cambiamenti
* Allineare i risultati della ricerca tra i membri del team

### 6. Multi-Agente in parallelo = Moltiplicazione della profondità di ricerca

`/investment-team` avvia 4 Agent indipendenti per studiare un'azienda **simultaneamente**. Ogni Agent esegue ricerche di rete, convalida incrociata dei dati e fornisce conclusioni in modo indipendente. Non si tratta di dividere un prompt in quattro parti — sono 4 "analisti" che fanno ciascuno una ricerca completa, sintetizzata poi dal Team Lead.

Chiedendo direttamente all'AI, hai una sola finestra di contesto. 4 Agent in parallelo equivalgono a 4 volte il volume di ricerca, 4 volte le fonti di informazione, 4 prospettive indipendenti.

```text
┌─────────────────────────────────────────────┐
│              Team Lead (Tu)                 │
│      Coordinamento · Sintesi e Giudizio     │
├──────┬──────┬──────────┬───────────┤
│ Agent 1    │ Agent 2    │ Agent 3        │ Agent 4         │
│ Modello di │ Finanza e  │ Settore e      │ Rischi e        │
│ Business   │ Valutazione│ Concorrenza    │ Management      │
│ (D.Yongping)│ (Buffett)  │ (Munger)       │ (Li Lu)         │
└──────┴──────┴──────────┴───────────┘
        ↓ Ricerca parallela, report in tempo reale ↓
              Report Sintetico Finale
```

### Sintesi in una frase

> **Le persone comuni che chiedono all'AI ottengono "analisi che sembrano corrette", usando AI Berkshire si ottengono "report di ricerca sugli investimenti che possono essere usati per prendere decisioni".**

---

## Architettura Generale

**Filosofia di design a tre livelli**:
* **Livello Skill**: Astrae "quello che vuoi fare" in 16 chiari punti di ingresso — ricerca profonda, analisi dei bilanci, screening del settore, gestione delle posizioni, strumenti di pensiero, selezionabili in base allo scenario.
* **Livello Agent**: All'interno di ogni skill ci sono 4 Agent in parallelo — cercano indipendentemente, giudicano indipendentemente, si sfidano a vicenda, e infine il Team Lead sintetizza.
* **Livello Tool**: Calcolo preciso, recupero in tempo reale, ispezione dei report — garantisce che il rigore dei dati di ogni report sia verificabile.

---

## Panoramica delle Skill (16 in totale)

### 🔬 Ricerca Profonda
* `/investment-research`: Analisi profonda sintetica dei quattro maestri
* `/investment-team`: Team di ricerca multi-Agent in parallelo
* `/management-deep-dive`: Ricerca approfondita sul management
* `/private-company-research`: Ricerca profonda su aziende non quotate
* `/deep-company-series`: Serie di 8 articoli lunghi per dissezionare un'azienda

### 📊 Analisi dei Bilanci
* `/earnings-review`: Lettura approfondita dei bilanci (fonti primarie)
* `/earnings-team`: Team per la lettura dei bilanci + pubblicazione articoli

### 🏭 Screening di Settore
* `/industry-research`: Scansione panoramica della catena industriale
* `/industry-funnel`: Screening a imbuto del settore
* `/quality-screen`: Screening per eliminare i peggiori (7 indicatori rigidi)
* `/investment-checklist`: Checklist di Buffett prima dell'acquisto

### 📈 Gestione del Portafoglio
* `/portfolio-review`: Gestione e ottimizzazione del portafoglio
* `/thesis-tracker`: Tracciamento della tesi di investimento
* `/news-pulse`: Attribuzione rapida delle fluttuazioni anomale del prezzo delle azioni

### 🧠 Strumenti di Pensiero
* `/dyp-ask`: Q&A in stile Duan Yongping
* `/financial-data`: Standard per l'acquisizione e la validazione incrociata dei dati finanziari

---

## Guida Rapida

### 1. Installa Claude Code
```bash
npm install -g @anthropic-ai/claude-code
```

### 2. Installa le Skill
Copia i file `.md` dalla directory `skills/` alla tua directory dei comandi di Claude Code:
```bash
# Clona la repository
git clone https://github.com/xbtlin/ai-berkshire.git

# Copia le skill nella directory globale dei comandi di Claude Code
cp ai-berkshire/skills/*.md ~/.claude/commands/
```

### 3. Utilizzo
Richiama direttamente in Claude Code:
```bash
# Ricerca profonda
/investment-research Tencent
/investment-team Meituan

# Analisi dei bilanci
/earnings-review Tencent 2025Q4

# Screening di settore
/industry-research Energia Nucleare
/investment-checklist Kweichow Moutai, NVIDIA, Apple

# Gestione del portafoglio
/portfolio-review Tencent 30%, Meituan 20%, Moutai 20%, Cash 30%
/news-pulse Tencent
```
