#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Directa dAPI Client — AI Berkshire Integration
===============================================
Client Python per le API di trading Directa SIM (dAPI).
Connessione via socket TCP/IP locale alla piattaforma Darwin.

Prerequisiti:
  - Piattaforma Darwin aperta e loggata
  - Abilitazione API attiva sul conto (info > 5a > 3h)
  - File di configurazione: ~/.directa/ai-berkshire-config.json

Porte di default (prima utenza):
  - 10001: DATAFEED  (quotazioni real-time)
  - 10002: TRADING   (portafoglio, liquidità, ordini)
  - 10003: STORICO   (candele OHLCV, tick-by-tick)

Utilizzo:
  python3 tools/directa_client.py portfolio
  python3 tools/directa_client.py liquidity
  python3 tools/directa_client.py orders
  python3 tools/directa_client.py account
  python3 tools/directa_client.py price ENI,STLAM,RACE
  python3 tools/directa_client.py candles RACE 1h 5
  python3 tools/directa_client.py tbt RACE 1
  python3 tools/directa_client.py status
  python3 tools/directa_client.py export-portfolio          # JSON per Claude
  python3 tools/directa_client.py export-full               # snapshot completo per Claude

Documentazione dAPI: https://app1.directatrading.com/trading-api-directa/index.html

Compatibilità: Python >= 3.9 (zero dipendenze esterne, solo stdlib)
"""

from __future__ import annotations  # compatibilità Python 3.9 per type hints

import argparse
import json
import os
import socket
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# Configurazione
# ---------------------------------------------------------------------------

CONFIG_PATH = Path.home() / ".directa" / "ai-berkshire-config.json"

DEFAULT_CONFIG: Dict = {
    "host": "127.0.0.1",
    "port_datafeed": 10001,
    "port_trading": 10002,
    "port_history": 10003,
    "timeout": 10,
    "heartbeat_interval": 8,
    "account_code": "",
}

# Codici errore dAPI informativi (non fatali) — non interrompono il loop di lettura
_ERR_INFORMATIVE = {"1018", "1019"}


def load_config() -> Dict:
    """Carica la configurazione utente, con fallback ai default."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            user_cfg = json.load(f)
        cfg: Dict = {**DEFAULT_CONFIG, **user_cfg}
    else:
        cfg = DEFAULT_CONFIG.copy()
    return cfg


# ---------------------------------------------------------------------------
# Client Socket Base
# ---------------------------------------------------------------------------

class DirectaSocket:
    """Connessione socket TCP/IP verso una porta Darwin."""

    def __init__(self, host: str, port: int, timeout: int = 10, label: str = ""):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.label = label or f":{port}"
        self._sock: Optional[socket.socket] = None
        self._file = None
        self._hb_thread: Optional[threading.Thread] = None
        self._hb_stop = threading.Event()

    def connect(self) -> bool:
        """Apre la connessione socket. Restituisce True se riuscita."""
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.settimeout(self.timeout)
            self._sock.connect((self.host, self.port))
            self._file = self._sock.makefile("r", encoding="utf-8")
            return True
        except (ConnectionRefusedError, OSError) as e:
            print(f"  ❌ Connessione a {self.label} fallita: {e}", file=sys.stderr)
            print("     → Assicurarsi che Darwin sia aperta e le API abilitate.", file=sys.stderr)
            return False

    def send(self, command: str) -> None:
        """Invia un comando al server (aggiunge \\n automaticamente)."""
        if self._sock is None:
            raise RuntimeError("Socket non connesso.")
        self._sock.sendall((command.strip() + "\n").encode("utf-8"))

    def readline(self) -> str:
        """Legge una riga dalla risposta del server."""
        if self._file is None:
            raise RuntimeError("Socket non connesso.")
        line = self._file.readline()
        return line.rstrip("\n\r")

    def read_flowpoint_list(self, begin_marker: str, end_marker: str,
                            max_lines: int = 2000) -> List[str]:
        """
        Legge righe tra BEGIN <marker> e END <marker> (FLOWPOINT mode).
        Restituisce le righe intermedie, escludendo i marcatori stessi.
        """
        lines: List[str] = []
        # Attendi il marcatore BEGIN
        deadline = time.time() + self.timeout
        while time.time() < deadline:
            try:
                line = self.readline()
            except socket.timeout:
                break
            if line.startswith(begin_marker):
                break
            # Scarta righe informative pre-BEGIN (es. DARWIN_STATUS, ERR;1018)
        # Leggi fino a END
        for _ in range(max_lines):
            try:
                line = self.readline()
            except socket.timeout:
                break
            if not line:
                break
            if line.startswith(end_marker):
                break
            lines.append(line)
        return lines

    def start_heartbeat(self, interval: int = 8) -> None:
        """Avvia un thread che invia H ogni `interval` secondi."""
        self._hb_stop.clear()

        def _hb() -> None:
            while not self._hb_stop.wait(interval):
                try:
                    self.send("H")
                except Exception:
                    break

        self._hb_thread = threading.Thread(target=_hb, daemon=True)
        self._hb_thread.start()

    def stop_heartbeat(self) -> None:
        self._hb_stop.set()

    def close(self) -> None:
        self.stop_heartbeat()
        try:
            if self._sock:
                self._sock.close()
        except Exception:
            pass
        self._sock = None
        self._file = None

    def __enter__(self) -> "DirectaSocket":
        return self

    def __exit__(self, *_) -> None:
        self.close()


# ---------------------------------------------------------------------------
# Parser dei messaggi dAPI
# ---------------------------------------------------------------------------

def parse_stock(line: str) -> Optional[Dict]:
    """
    STOCK;TICKER;HH:MM:SS;qty_portafoglio;qty_directa;qty_negoziazione;prezzo_medio;gain
    """
    parts = line.split(";")
    if len(parts) < 7 or parts[0] != "STOCK":
        return None
    return {
        "ticker": parts[1].strip(),
        "ora": parts[2].strip(),
        "qty_portafoglio": _safe_int(parts[3]),
        "qty_directa": _safe_int(parts[4]),
        "qty_negoziazione": parts[5].strip(),
        "prezzo_medio": _safe_float(parts[6]),
        "gain_teorico": _safe_float(parts[7]) if len(parts) > 7 else None,
    }


def parse_availability(line: str) -> Optional[Dict]:
    """
    AVAILABILITY;HH:MM:SS;disp_azioni;disp_azioni_marg;disp_derivati;disp_derivati_marg;liquidita_totale
    """
    parts = line.split(";")
    if len(parts) < 7 or parts[0] != "AVAILABILITY":
        return None
    return {
        "ora": parts[1].strip(),
        "disponibilita_azioni": _safe_float(parts[2]),
        "disponibilita_azioni_marginatura": _safe_float(parts[3]),
        "disponibilita_derivati": _safe_float(parts[4]),
        "disponibilita_derivati_marginatura": _safe_float(parts[5]),
        "liquidita_totale": _safe_float(parts[6]),
    }


def parse_infoaccount(line: str) -> Optional[Dict]:
    """
    INFOACCOUNT;HH:MM:SS;codice_conto;liquidita;gain_euro;open_pl;equity
    """
    parts = line.split(";")
    if len(parts) < 7 or parts[0] != "INFOACCOUNT":
        return None
    return {
        "ora": parts[1].strip(),
        "codice_conto": parts[2].strip(),
        "liquidita": _safe_float(parts[3]),
        "gain_euro": _safe_float(parts[4]),
        "open_profit_loss": _safe_float(parts[5]),
        "equity": _safe_float(parts[6]),
    }


def parse_order(line: str) -> Optional[Dict]:
    """
    ORDER;TICKER;HH:MM:SS;ID_ORDINE;TIPO_OP;PREZZO_LIMITE;PREZZO_SEGNALE;QTY;STATO
    """
    parts = line.split(";")
    if len(parts) < 9 or parts[0] != "ORDER":
        return None
    stato_map = {
        "2000": "In negoziazione",
        "2001": "Errore immissione",
        "2002": "In negoziazione (confermato)",
        "2003": "Eseguito",
        "2004": "Revocato",
        "2005": "In attesa di conferma",
        "2006": "Modificato",
    }
    stato_raw = parts[8].strip()
    return {
        "ticker": parts[1].strip(),
        "ora": parts[2].strip(),
        "id_ordine": parts[3].strip(),
        "tipo_operazione": parts[4].strip(),
        "prezzo_limite": _safe_float(parts[5]),
        "prezzo_segnale": _safe_float(parts[6]),
        "quantita": _safe_int(parts[7]),
        "stato_codice": stato_raw,
        "stato": stato_map.get(stato_raw, stato_raw),
    }


def parse_price(line: str) -> Optional[Dict]:
    """
    PRICE;TICKER;HH:MM:SS;prezzo;qty;prog_azioni;prog_contratti;min_giornata;max_giornata
    """
    parts = line.split(";")
    if len(parts) < 9 or parts[0] != "PRICE":
        return None
    return {
        "ticker": parts[1].strip(),
        "ora": parts[2].strip(),
        "prezzo": _safe_float(parts[3]),
        "quantita": _safe_int(parts[4]),
        "progressivo_azioni": _safe_int(parts[5]),
        "progressivo_contratti": _safe_int(parts[6]),
        "minimo_giornata": _safe_float(parts[7]),
        "massimo_giornata": _safe_float(parts[8]),
    }


def parse_anag(line: str) -> Optional[Dict]:
    """
    ANAG;TICKER;HH:MM:SS;ISIN;DESCRIZIONE;PREZZO_RIF;PREZZO_APERTURA;FLOTTANTE
    """
    parts = line.split(";")
    if len(parts) < 8 or parts[0] != "ANAG":
        return None
    return {
        "ticker": parts[1].strip(),
        "ora": parts[2].strip(),
        "isin": parts[3].strip(),
        "descrizione": parts[4].strip(),
        "prezzo_riferimento": _safe_float(parts[5]),
        "prezzo_apertura": _safe_float(parts[6]),
        "flottante": _safe_int(parts[7]),
    }


def parse_candle(line: str) -> Optional[Dict]:
    """
    Formato risposta CANDLE (dAPI porta 10003):
    CANDLE;TICKER;YYYYMMDD;HH:MM:SS;UFF;MIN;MAX;APE;VOLUME
    dove UFF=chiusura, MIN=minimo, MAX=massimo, APE=apertura
    """
    parts = line.split(";")
    if len(parts) < 9 or parts[0] != "CANDLE":
        return None
    return {
        "ticker": parts[1].strip(),
        "data": parts[2].strip(),
        "ora": parts[3].strip(),
        "close": _safe_float(parts[4]),   # UFF = prezzo ufficiale/chiusura
        "low": _safe_float(parts[5]),     # MIN
        "high": _safe_float(parts[6]),    # MAX
        "open": _safe_float(parts[7]),    # APE = apertura
        "volume": _safe_int(parts[8]),
    }


def parse_tbt(line: str) -> Optional[Dict]:
    """
    Formato risposta TBT (tick-by-tick):
    TBT;TICKER;YYYYMMDD;HH:MM:SS;PREZZO;QUANTITA
    """
    parts = line.split(";")
    if len(parts) < 6 or parts[0] != "TBT":
        return None
    return {
        "ticker": parts[1].strip(),
        "data": parts[2].strip(),
        "ora": parts[3].strip(),
        "prezzo": _safe_float(parts[4]),
        "quantita": _safe_int(parts[5]),
    }


# ---------------------------------------------------------------------------
# Funzioni di alto livello
# ---------------------------------------------------------------------------

def cmd_status(cfg: Dict) -> None:
    """Verifica lo stato della connessione Darwin."""
    print("=" * 60)
    print("Stato Connessione Darwin (DARWINSTATUS)")
    print("=" * 60)
    with DirectaSocket(cfg["host"], cfg["port_trading"], cfg["timeout"], "TRADING") as s:
        if not s.connect():
            return
        s.send("DARWINSTATUS")
        line = s.readline()
        print(f"  Risposta: {line}")
        parts = line.split(";")
        if len(parts) >= 3 and parts[0] == "DARWIN_STATUS":
            stato = parts[1].strip()
            datafeed = parts[2].strip()
            release = parts[3].strip() if len(parts) > 3 else "N/D"
            icona = "✅" if stato == "CONN_OK" else "⚠️" if "SLOW" in stato else "❌"
            print(f"\n  {icona} Connessione: {stato}")
            print(f"  DataFeed abilitato: {datafeed}")
            print(f"  Versione: {release}")


def _fetch_stocks(cfg: Dict) -> List[Dict]:
    """
    Recupera il portafoglio corrente via FLOWPOINT + INFOSTOCKS.
    Usa FLOWPOINT TRUE per ottenere marcatori BEGIN/END deterministici,
    evitando attese sul timeout.
    """
    stocks: List[Dict] = []
    with DirectaSocket(cfg["host"], cfg["port_trading"], cfg["timeout"], "TRADING") as s:
        if not s.connect():
            return stocks
        s.start_heartbeat(cfg["heartbeat_interval"])
        # Attiva FLOWPOINT per marcatori BEGIN/END deterministici (Q5)
        s.send("FLOWPOINT TRUE")
        s.readline()  # consuma risposta "FLOWPOINT;TRUE"
        s.send("INFOSTOCKS")
        lines = s.read_flowpoint_list("BEGIN STOCKLIST", "END STOCKLIST")
        for line in lines:
            # Salta codici errore informativi (BUG 4: non interrompere su ERR;1018)
            if line.startswith("ERR"):
                code = line.split(";")[2].strip() if line.count(";") >= 2 else ""
                if code not in _ERR_INFORMATIVE:
                    print(f"  ⚠️  Errore: {line}", file=sys.stderr)
                continue
            parsed = parse_stock(line)
            if parsed:
                stocks.append(parsed)
    return stocks


def _fetch_orders(cfg: Dict, command: str = "ORDERLIST") -> List[Dict]:
    """
    Recupera la lista ordini via FLOWPOINT + comando ordini.
    """
    orders: List[Dict] = []
    with DirectaSocket(cfg["host"], cfg["port_trading"], cfg["timeout"], "TRADING") as s:
        if not s.connect():
            return orders
        s.start_heartbeat(cfg["heartbeat_interval"])
        s.send("FLOWPOINT TRUE")
        s.readline()  # consuma "FLOWPOINT;TRUE"
        s.send(command)
        lines = s.read_flowpoint_list("BEGIN ORDERLIST", "END ORDERLIST")
        for line in lines:
            if line.startswith("ERR"):
                code = line.split(";")[2].strip() if line.count(";") >= 2 else ""
                if code == "1019":
                    break  # nessun ordine presente — normale
                if code not in _ERR_INFORMATIVE:
                    print(f"  ⚠️  Errore: {line}", file=sys.stderr)
                continue
            parsed = parse_order(line)
            if parsed:
                orders.append(parsed)
    return orders


def cmd_portfolio(cfg: Dict) -> List[Dict]:
    """Recupera e stampa il portafoglio corrente."""
    print("=" * 60)
    print("Portafoglio Directa (INFOSTOCKS)")
    print("=" * 60)
    stocks = _fetch_stocks(cfg)
    if not stocks:
        print("  ℹ️  Portafoglio vuoto o nessuna risposta.")
    else:
        print(f"\n  {'Ticker':<12} {'Qty':>6} {'Prezzo Medio':>14} {'In Negoz.':>12} {'Gain Teor.':>12}")
        print(f"  {'-'*12} {'-'*6} {'-'*14} {'-'*12} {'-'*12}")
        for stk in stocks:
            gain_val = stk["gain_teorico"]
            gain = f"{gain_val:.2f} €" if gain_val is not None and gain_val != -1 else "N/D"
            print(f"  {stk['ticker']:<12} {stk['qty_portafoglio']:>6} "
                  f"{stk['prezzo_medio']:>13.4f}€ {str(stk['qty_negoziazione']):>12} {gain:>12}")
        print(f"\n  Totale posizioni: {len(stocks)}")
    return stocks


def cmd_liquidity(cfg: Dict) -> Optional[Dict]:
    """Recupera la liquidità disponibile."""
    print("=" * 60)
    print("Liquidità Portafoglio (INFOAVAILABILITY)")
    print("=" * 60)
    result = None
    with DirectaSocket(cfg["host"], cfg["port_trading"], cfg["timeout"], "TRADING") as s:
        if not s.connect():
            return None
        s.send("INFOAVAILABILITY")
        line = s.readline()
        if line.startswith("ERR"):
            print(f"  ⚠️  Errore: {line}")
            return None
        result = parse_availability(line)
        if result:
            print(f"\n  Ora:                        {result['ora']}")
            print(f"  Disponibilità Azioni:       {result['disponibilita_azioni']:>12,.2f} €")
            print(f"  Disp. Azioni (marginatura): {result['disponibilita_azioni_marginatura']:>12,.2f} €")
            print(f"  Disponibilità Derivati:     {result['disponibilita_derivati']:>12,.2f} €")
            print(f"  Disp. Derivati (marg.):     {result['disponibilita_derivati_marginatura']:>12,.2f} €")
            print(f"  ─────────────────────────────────────────")
            print(f"  Liquidità Totale:           {result['liquidita_totale']:>12,.2f} €")
    return result


def cmd_account(cfg: Dict) -> Optional[Dict]:
    """Recupera lo stato patrimoniale del conto."""
    print("=" * 60)
    print("Stato Patrimoniale Conto (INFOACCOUNT)")
    print("=" * 60)
    result = None
    with DirectaSocket(cfg["host"], cfg["port_trading"], cfg["timeout"], "TRADING") as s:
        if not s.connect():
            return None
        s.send("INFOACCOUNT")
        line = s.readline()
        if line.startswith("ERR"):
            print(f"  ⚠️  Errore: {line}")
            return None
        result = parse_infoaccount(line)
        if result:
            print(f"\n  Ora:              {result['ora']}")
            print(f"  Codice Conto:     {result['codice_conto']}")
            print(f"  Liquidità:        {result['liquidita']:>12,.2f} €")
            print(f"  Gain (realizzato):{result['gain_euro']:>12,.2f} €")
            print(f"  Open P/L:         {result['open_profit_loss']:>12,.2f} €")
            print(f"  Equity:           {result['equity']:>12,.2f} €")
    return result


def cmd_orders(cfg: Dict, filter_mode: str = "all") -> List[Dict]:
    """
    Recupera la lista ordini.
    filter_mode: 'all' | 'pending' | 'norev'
    """
    cmd_map = {
        "all": "ORDERLIST",
        "pending": "ORDERLISTPENDING",
        "norev": "ORDERLISTNOREV",
    }
    command = cmd_map.get(filter_mode, "ORDERLIST")
    print("=" * 60)
    print(f"Lista Ordini ({command})")
    print("=" * 60)
    orders = _fetch_orders(cfg, command)
    if not orders:
        print("  ℹ️  Nessun ordine presente.")
    else:
        print(f"\n  {'Ticker':<10} {'Ora':>8} {'ID':>12} {'Tipo':>8} {'Prezzo':>8} {'Qty':>6} {'Stato'}")
        print(f"  {'-'*10} {'-'*8} {'-'*12} {'-'*8} {'-'*8} {'-'*6} {'-'*25}")
        for o in orders:
            print(f"  {o['ticker']:<10} {o['ora']:>8} {o['id_ordine']:>12} {o['tipo_operazione']:>8} "
                  f"{o['prezzo_limite']:>8.3f} {o['quantita']:>6} {o['stato']}")
        print(f"\n  Totale ordini: {len(orders)}")
    return orders


def cmd_price(cfg: Dict, tickers: List[str]) -> List[Dict]:
    """Sottoscrive e legge il prezzo corrente per una lista di ticker."""
    print("=" * 60)
    print(f"Prezzi Real-Time: {', '.join(tickers)}")
    print("=" * 60)
    prices: List[Dict] = []
    anags: List[Dict] = []
    ticker_str = ",".join(tickers)

    with DirectaSocket(cfg["host"], cfg["port_datafeed"], cfg["timeout"], "DATAFEED") as s:
        if not s.connect():
            return prices
        s.start_heartbeat(cfg["heartbeat_interval"])
        s.send(f"SUBPRZALL {ticker_str}")
        deadline = time.time() + cfg["timeout"]
        received: set = set()
        while time.time() < deadline:
            try:
                line = s.readline()
            except socket.timeout:
                break
            if not line:
                break
            if line.startswith("ERR"):
                print(f"  ⚠️  {line}")
                continue
            if line.startswith("PRICE;"):
                p = parse_price(line)
                if p:
                    prices.append(p)
                    received.add(p["ticker"])
            elif line.startswith("ANAG;"):
                a = parse_anag(line)
                if a:
                    anags.append(a)
            if received >= set(tickers):
                break
        s.send(f"UNS {ticker_str}")

    anag_map = {a["ticker"]: a for a in anags}
    if prices:
        print(f"\n  {'Ticker':<10} {'ISIN':<14} {'Prezzo':>10} {'Min':>8} {'Max':>8} {'Ora':>8}")
        print(f"  {'-'*10} {'-'*14} {'-'*10} {'-'*8} {'-'*8} {'-'*8}")
        for p in prices:
            isin = anag_map.get(p["ticker"], {}).get("isin", "N/D")
            print(f"  {p['ticker']:<10} {isin:<14} {p['prezzo']:>10.4f} {p['minimo_giornata']:>8.4f} "
                  f"{p['massimo_giornata']:>8.4f} {p['ora']:>8}")
    return prices


def cmd_candles(cfg: Dict, ticker: str, timeframe: str, days: int) -> List[Dict]:
    """
    Scarica dati storici OHLCV tramite il comando CANDLE (porta 10003).

    BUG 1 FIX: il comando corretto è CANDLE, non HISTORY.
    Formato: CANDLE <TICKER> <GIORNI> <PERIODO_SECONDI>
    Risposta: CANDLE;TICKER;YYYYMMDD;HH:MM:SS;UFF;MIN;MAX;APE;VOLUME
              dove UFF=chiusura, MIN=minimo, MAX=massimo, APE=apertura

    Limiti dAPI:
      - 1s, 5s: max 1 giorno
      - 10s, 30s: max 3 giorni
      - 1m-4m: max 100 giorni
      - 1d (EndOfDay): fino a 15 anni

    timeframe: '1s','5s','10s','30s','1m','2m','3m','4m','5m','10m','15m','30m','1h','2h','4h','1d'
    """
    tf_map = {
        "1s": "1", "5s": "5", "10s": "10", "30s": "30",
        "1m": "60", "2m": "120", "3m": "180", "4m": "240",
        "5m": "300", "10m": "600", "15m": "900", "30m": "1800",
        "1h": "3600", "2h": "7200", "4h": "14400",
        "1d": "86400",
    }
    tf_code = tf_map.get(timeframe, "86400")
    print("=" * 60)
    print(f"Candele Storiche: {ticker} | Timeframe: {timeframe} | Giorni: {days}")
    print("=" * 60)

    candles: List[Dict] = []
    with DirectaSocket(cfg["host"], cfg["port_history"], cfg["timeout"] * 2, "STORICO") as s:
        if not s.connect():
            return candles
        # Formato corretto: CANDLE <TICKER> <GIORNI> <PERIODO_SECONDI>
        s.send(f"CANDLE {ticker} {days} {tf_code}")
        deadline = time.time() + cfg["timeout"] * 3
        while time.time() < deadline:
            try:
                line = s.readline()
            except socket.timeout:
                break
            if not line:
                break
            if line.startswith("END CANDLES") or line.startswith("END TBT"):
                break
            if line.startswith("ERR") or line.startswith("Wrong"):
                print(f"  ⚠️  {line}")
                break
            if line.startswith("BEGIN CANDLES"):
                continue
            parsed = parse_candle(line)
            if parsed:
                candles.append(parsed)

    if candles:
        print(f"\n  {'Data':<10} {'Ora':>8} {'Open':>10} {'High':>10} {'Low':>10} {'Close':>10} {'Volume':>12}")
        print(f"  {'-'*10} {'-'*8} {'-'*10} {'-'*10} {'-'*10} {'-'*10} {'-'*12}")
        for c in candles[-20:]:
            print(f"  {c['data']:<10} {c['ora']:>8} {c['open']:>10.4f} {c['high']:>10.4f} "
                  f"{c['low']:>10.4f} {c['close']:>10.4f} {c['volume']:>12,}")
        if len(candles) > 20:
            print(f"  ... ({len(candles) - 20} candele precedenti omesse)")
        print(f"\n  Totale candele: {len(candles)}")
    else:
        print("  ℹ️  Nessuna candela ricevuta.")
    return candles


def cmd_tbt(cfg: Dict, ticker: str, days: int) -> List[Dict]:
    """
    Scarica dati tick-by-tick tramite il comando TBT (porta 10003).
    Formato: TBT <TICKER> <GIORNI>
    Risposta: TBT;TICKER;YYYYMMDD;HH:MM:SS;PREZZO;QUANTITA
    Limite: max 1 giorno per i tick.
    """
    print("=" * 60)
    print(f"Tick-by-Tick: {ticker} | Giorni: {days}")
    print("=" * 60)
    ticks: List[Dict] = []
    with DirectaSocket(cfg["host"], cfg["port_history"], cfg["timeout"] * 3, "STORICO") as s:
        if not s.connect():
            return ticks
        s.send(f"TBT {ticker} {days}")
        deadline = time.time() + cfg["timeout"] * 4
        while time.time() < deadline:
            try:
                line = s.readline()
            except socket.timeout:
                break
            if not line:
                break
            if line.startswith("END TBT"):
                break
            if line.startswith("ERR") or line.startswith("Wrong") or line.startswith("no delta"):
                if not line.startswith("no delta"):
                    print(f"  ⚠️  {line}")
                continue
            parsed = parse_tbt(line)
            if parsed:
                ticks.append(parsed)

    if ticks:
        print(f"\n  {'Data':<10} {'Ora':>8} {'Prezzo':>12} {'Quantità':>10}")
        print(f"  {'-'*10} {'-'*8} {'-'*12} {'-'*10}")
        for t in ticks[-30:]:
            print(f"  {t['data']:<10} {t['ora']:>8} {t['prezzo']:>12.5f} {t['quantita']:>10,}")
        if len(ticks) > 30:
            print(f"  ... ({len(ticks) - 30} tick precedenti omessi)")
        print(f"\n  Totale tick: {len(ticks)}")
    else:
        print("  ℹ️  Nessun tick ricevuto.")
    return ticks


def cmd_export_portfolio(cfg: Dict) -> Dict:
    """
    Esporta un snapshot JSON del portafoglio + liquidità + conto.
    Ottimizzato per essere passato a Claude come contesto.

    BUG 3 FIX: ogni chiamata usa una connessione socket separata,
    evitando race condition da multi-comando su stessa connessione.
    """
    snapshot: Dict = {
        "timestamp": datetime.now().isoformat(),
        "fonte": "Directa dAPI",
        "portafoglio": [],
        "liquidita": None,
        "conto": None,
        "ordini_pendenti": [],
    }

    # Portafoglio — connessione dedicata
    snapshot["portafoglio"] = _fetch_stocks(cfg)

    # Liquidità — connessione dedicata
    with DirectaSocket(cfg["host"], cfg["port_trading"], cfg["timeout"], "TRADING") as s:
        if s.connect():
            s.send("INFOAVAILABILITY")
            line = s.readline()
            if not line.startswith("ERR"):
                snapshot["liquidita"] = parse_availability(line)

    # Conto — connessione dedicata
    with DirectaSocket(cfg["host"], cfg["port_trading"], cfg["timeout"], "TRADING") as s:
        if s.connect():
            s.send("INFOACCOUNT")
            line = s.readline()
            if not line.startswith("ERR"):
                snapshot["conto"] = parse_infoaccount(line)

    # Ordini pendenti — connessione dedicata
    snapshot["ordini_pendenti"] = _fetch_orders(cfg, "ORDERLISTPENDING")

    return snapshot


def cmd_export_full(cfg: Dict, tickers_extra: Optional[List[str]] = None) -> tuple:
    """
    Esporta snapshot completo (portafoglio + prezzi real-time dei titoli posseduti)
    e lo salva in reports/directa-snapshot-{data}.json
    """
    snapshot = cmd_export_portfolio(cfg)

    owned_tickers = [s["ticker"] for s in snapshot["portafoglio"] if s["qty_portafoglio"] > 0]
    if tickers_extra:
        owned_tickers = list(set(owned_tickers + tickers_extra))

    if owned_tickers:
        prices = cmd_price(cfg, owned_tickers)
        snapshot["prezzi_realtime"] = prices
    else:
        snapshot["prezzi_realtime"] = []

    reports_dir = Path(__file__).parent.parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d_%H%M")
    out_path = reports_dir / f"directa-snapshot-{date_str}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)

    print(f"\n  ✅ Snapshot salvato in: {out_path}")
    print(f"  Titoli in portafoglio: {len(snapshot['portafoglio'])}")
    print(f"  Ordini pendenti:       {len(snapshot['ordini_pendenti'])}")
    if snapshot["conto"]:
        print(f"  Equity:                {snapshot['conto']['equity']:,.2f} €")
    return snapshot, str(out_path)


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def _safe_float(val: str) -> float:
    try:
        return float(str(val).strip().replace(",", "."))
    except (ValueError, AttributeError):
        return 0.0


def _safe_int(val: str) -> int:
    """
    BUG 5 FIX: parsing robusto per campi interi dAPI.
    Gestisce formati come '70', '70> -70', '100>', '' senza eccezioni.
    """
    try:
        s = str(val).strip().replace("*", "")
        # Prendi solo la parte prima di '>' (quantità in negoziazione)
        if ">" in s:
            s = s.split(">")[0].strip()
        if not s:
            return 0
        return int(float(s))  # float() gestisce anche "70.0"
    except (ValueError, AttributeError):
        return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Directa dAPI Client — AI Berkshire Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  python3 tools/directa_client.py status
  python3 tools/directa_client.py portfolio
  python3 tools/directa_client.py liquidity
  python3 tools/directa_client.py account
  python3 tools/directa_client.py orders
  python3 tools/directa_client.py orders --filter pending
  python3 tools/directa_client.py price ENI,STLAM,RACE
  python3 tools/directa_client.py candles RACE 1h 5
  python3 tools/directa_client.py candles RACE 1d 30
  python3 tools/directa_client.py tbt RACE 1
  python3 tools/directa_client.py export-portfolio
  python3 tools/directa_client.py export-full
  python3 tools/directa_client.py export-full --tickers ENI,ENEL
        """
    )
    parser.add_argument("command", choices=[
        "status", "portfolio", "liquidity", "account",
        "orders", "price", "candles", "tbt",
        "export-portfolio", "export-full",
    ])
    parser.add_argument("args", nargs="*", help="Argomenti del comando (ticker, timeframe, giorni)")
    parser.add_argument("--filter", choices=["all", "pending", "norev"], default="all",
                        help="Filtro per il comando orders (default: all)")
    parser.add_argument("--tickers", default="",
                        help="Ticker aggiuntivi per export-full (es. ENI,ENEL)")
    parser.add_argument("--json", action="store_true", help="Output in formato JSON")
    parser.add_argument("--config", default=str(CONFIG_PATH),
                        help="Percorso file di configurazione")

    args = parser.parse_args()
    cfg = load_config()
    if args.config != str(CONFIG_PATH) and Path(args.config).exists():
        with open(args.config) as f:
            cfg.update(json.load(f))

    result = None

    if args.command == "status":
        cmd_status(cfg)

    elif args.command == "portfolio":
        result = cmd_portfolio(cfg)

    elif args.command == "liquidity":
        result = cmd_liquidity(cfg)

    elif args.command == "account":
        result = cmd_account(cfg)

    elif args.command == "orders":
        result = cmd_orders(cfg, args.filter)

    elif args.command == "price":
        if not args.args:
            print("Errore: specificare i ticker. Es: price ENI,STLAM", file=sys.stderr)
            sys.exit(1)
        tickers = [t.strip().upper() for t in args.args[0].split(",")]
        result = cmd_price(cfg, tickers)

    elif args.command == "candles":
        if len(args.args) < 3:
            print("Errore: candles <TICKER> <TIMEFRAME> <GIORNI>. Es: candles RACE 1d 30",
                  file=sys.stderr)
            sys.exit(1)
        result = cmd_candles(cfg, args.args[0].upper(), args.args[1], int(args.args[2]))

    elif args.command == "tbt":
        if len(args.args) < 2:
            print("Errore: tbt <TICKER> <GIORNI>. Es: tbt RACE 1", file=sys.stderr)
            sys.exit(1)
        result = cmd_tbt(cfg, args.args[0].upper(), int(args.args[1]))

    elif args.command == "export-portfolio":
        result = cmd_export_portfolio(cfg)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "export-full":
        extra = [t.strip().upper() for t in args.tickers.split(",") if t.strip()] \
            if args.tickers else None
        result, path = cmd_export_full(cfg, extra)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))

    if args.json and result is not None and args.command not in ("export-portfolio", "export-full"):
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
