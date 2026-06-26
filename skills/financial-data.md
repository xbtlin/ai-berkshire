# Acquisizione Dati Finanziari e Standard di Validazione Incrociata

Questo standard si applica a tutte le ricerche che coinvolgono dati finanziari aziendali. **Ogni dato chiave deve provenire da due fonti indipendenti, e discrepanze >1% devono essere segnalate.**

---

## Priorità delle Fonti Dati

### Azioni Europee / Italiane (es. Ferrari, Enel, LVMH, ASML)

| Priorità | Fonte | URL | Metodo di Accesso |
|--------|------|-----|---------|
| 1 (Primaria) | **Morningstar IT** | morningstar.it | Accesso diretto |
| 2 (Secondaria) | **Marketscreener** | it.marketscreener.com | Accesso diretto |
| 3 (Alternativa) | **Borsa Italiana** | borsaitaliana.it | Accesso diretto (solo per titoli italiani) |
| Originale | Investor Relations | Sito ufficiale dell'azienda | Report annuali/trimestrali in PDF |

### Azioni USA (es. Apple, Microsoft, NVIDIA)

| Priorità | Fonte | URL | Metodo di Accesso |
|--------|------|-----|---------|
| 1 (Primaria) | **macrotrends** | macrotrends.net/stocks/charts/{ticker} | Accesso diretto |
| 2 (Secondaria) | **stockanalysis** | stockanalysis.com/stocks/{ticker}/financials | Accesso diretto |
| Originale | SEC EDGAR | sec.gov/cgi-bin/browse-edgar | 10-K / 10-Q originali |

---

## Standard di Esecuzione

### Passo 1: Acquisizione Dati
Per ogni metrica finanziaria (Ricavi, Utile Netto, Margine Lordo, Flusso di Cassa Operativo, ecc.), estrarre i dati sia dalla **Fonte 1** che dalla **Fonte 2**.

### Passo 2: Calcolo e Segnalazione dell'Errore
```
Tasso di Errore = |Valore Fonte 1 - Valore Fonte 2| / Valore Fonte 1 × 100%
```

| Errore | Azione |
|------|---------|
| ≤ 1% | ✅ Coerente. Usa il Valore 1 e cita entrambe le fonti. |
| 1% ~ 5% | ⚠️ Segnala "Discrepanza nei dati", annota entrambi i valori e spiega la possibile causa (es. differenze valutarie o contabili). |
| > 5% | ❌ Segnala "Grave discrepanza nei dati", devi verificare il report finanziario originale, non usare i dati ciecamente. |

### Passo 3: Formato di Presentazione dei Dati
Ogni dato chiave deve essere annotato in questo formato:

```
Ricavi: 12,39 miliardi di EUR ✅
  - Morningstar: 12,41 miliardi di EUR
  - Marketscreener: 12,37 miliardi di EUR
  - Errore: 0.3%
```

Esempio di discrepanza:
```
Utile Netto: 2,45 miliardi di EUR ⚠️ Discrepanza nei dati
  - Morningstar: 2,45 miliardi di EUR (GAAP)
  - Marketscreener: 2,78 miliardi di EUR (Non-GAAP)
  - Errore: 13.5% — Causa: Differenza contabile (GAAP vs Non-GAAP)
```

---

## Cause Comuni di Discrepanza (non necessariamente errori)

| Causa | Descrizione |
|------|------|
| GAAP vs Non-GAAP | Molto comune, specialmente per i dati di profitto |
| Tassi di cambio | I tassi EUR/USD/GBP presi in momenti diversi |
| Anno Fiscale | Anno solare vs Anno fiscale (es. l'anno fiscale di Apple finisce a settembre) |
| Consolidamento | Inclusione o meno di interessi di minoranza |
| Ritardo aggiornamenti | Una piattaforma potrebbe non aver ancora aggiornato l'ultimo report |

---

## Regole Speciali

1. **Aziende Non Quotate**: Quando c'è una sola fonte primaria, anteponi al dato `[Stima]`, nessuna validazione incrociata richiesta.
2. **Dati Trimestrali vs Annuali**: Dai priorità ai dati annuali per la validazione incrociata, alcune fonti potrebbero ritardare sui trimestrali.
3. **Priorità ai Report Originali**: Se entrambe le fonti differiscono dal report originale (PDF Annuale), prevale il report originale e si segnala l'errore delle fonti.
