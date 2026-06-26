> **ATTENZIONE / AVVISO**: Tutte le analisi, i report e gli output generati da questa skill DEVONO essere scritti in **ITALIANO (Italian)**.

# Directa Portfolio: Visualizzazione Portafoglio e Liquidità
Visualizza lo stato attuale del portafoglio e della liquidità sul conto Directa SIM.

## Prerequisiti
1. La piattaforma Darwin deve essere aperta e connessa.
2. Le API devono essere abilitate sul conto Directa (info > 5a > 3h).
3. Lo script Python `directa_client.py` deve essere presente nella directory `tools/`.

## Esecuzione

### Passo 1: Estrazione Dati
Esegui il comando Python per ottenere lo snapshot completo del portafoglio:
```bash
python3 tools/directa_client.py export-full --json
```

### Passo 2: Analisi dei Dati
Il comando restituirà un JSON contenente:
- **Portafoglio**: Elenco dei titoli posseduti, quantità, prezzo di carico e gain teorico.
- **Liquidità**: Liquidità totale e disponibilità per azioni/derivati.
- **Conto**: Equity totale, Open P/L e Gain realizzato.
- **Prezzi Real-Time**: Le quotazioni in tempo reale dei titoli posseduti.
- **Ordini Pendenti**: Gli ordini immessi ma non ancora eseguiti.

### Passo 3: Output del Report
Presenta all'utente un riepilogo chiaro e strutturato del suo conto.

#### Struttura del Report
1. **Sintesi del Conto**
   - Equity Totale
   - Liquidità Disponibile
   - Open Profit/Loss Totale
2. **Posizioni in Portafoglio**
   - Crea una tabella con: Ticker, Quantità, Prezzo Medio di Carico, Prezzo Attuale (se disponibile), Gain Teorico (in € e in %).
3. **Ordini Pendenti** (se presenti)
   - Elenco degli ordini in attesa di esecuzione.
4. **Avvisi e Considerazioni**
   - Segnala se ci sono titoli in forte perdita o in forte guadagno.
   - Segnala se la liquidità è molto bassa rispetto all'equity.

## Regole di Stile
- Non inventare dati: usa solo i numeri restituiti dal JSON.
- Formatta i valori monetari con il simbolo € (es. 1.250,00 €).
- Mantieni un tono professionale e oggettivo.
