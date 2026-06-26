> **ATTENZIONE / AVVISO**: Tutte le analisi, i report e gli output generati da questa skill DEVONO essere scritti in **ITALIANO (Italian)**.

# Directa Research: Analisi degli Asset Posseduti
Esegue un'analisi approfondita sui titoli attualmente presenti nel portafoglio Directa dell'utente.

## Scopo
A differenza di `directa-portfolio` che fa solo una fotografia del conto, questa skill prende i titoli posseduti dall'utente e avvia una mini-ricerca su ciascuno di essi, per capire se è il momento di tenere, incrementare o vendere.

## Esecuzione

### Passo 1: Estrazione del Portafoglio
Esegui il comando Python per ottenere i titoli posseduti:
```bash
python3 ~/ai-berkshire/tools/directa_client.py export-portfolio --json
```

### Passo 2: Selezione dei Titoli
Estrai l'elenco dei `ticker` dalla risposta JSON. Se il portafoglio è vuoto, avvisa l'utente e termina l'esecuzione.

### Passo 3: Analisi di Mercato (per ogni titolo)
Per ogni titolo in portafoglio, esegui una rapida ricerca web (WebSearch) per trovare le notizie più recenti, gli ultimi utili (earnings) e il sentiment generale.

**Cosa cercare:**
- Ultima trimestrale: ha battuto le stime o ha deluso?
- Notizie rilevanti degli ultimi 30 giorni.
- Rating degli analisti (es. Morningstar, Marketscreener).

### Passo 4: Output del Report
Genera un report strutturato che unisce la situazione reale del portafoglio (prezzo di carico, gain/loss) con l'analisi fondamentale.

#### Struttura del Report
1. **Panoramica del Portafoglio**
   - Quanti titoli sono posseduti.
   - Situazione generale del gain/loss.
2. **Analisi per Titolo** (per ogni ticker)
   - **Situazione Contabile**: Quantità, Prezzo di Carico, Gain/Loss Attuale.
   - **Catalizzatori Recenti**: Sintesi delle ultime notizie o trimestrali.
   - **Prospettive**: L'azienda sta mantenendo il suo "fossato economico"?
   - **Verdetto**: Tieni / Incrementa / Valuta Vendita (basato su logiche value investing).
3. **Conclusioni**
   - Il portafoglio è bilanciato?
   - Ci sono rischi di concentrazione eccessiva su un singolo titolo o settore?

## Regole di Analisi
- Applica i principi del Value Investing (Buffett, Munger). Non consigliare vendite solo per un calo temporaneo del prezzo se i fondamentali sono intatti.
- Distingui sempre tra i dati reali del conto (fatti) e le prospettive di mercato (opinioni/stime).
EOF
