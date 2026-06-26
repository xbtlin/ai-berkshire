#!/usr/bin/env python3
"""
Directa dAPI Setup — AI Berkshire
===================================
Configurazione guidata interattiva per l'integrazione con le API Directa SIM.

Cosa fa:
  1. Guida l'utente nella configurazione delle porte (auto-detect da APIPortSettings.txt)
  2. Verifica la connessione a Darwin
  3. Salva la configurazione in ~/.directa/ai-berkshire-config.json
  4. Installa le skill in ~/.claude/commands/

Utilizzo:
  python3 tools/directa_setup.py
  python3 tools/directa_setup.py --auto          # auto-detect porte, nessun input interattivo
  python3 tools/directa_setup.py --install-skills # solo installa le skill Claude
  python3 tools/directa_setup.py --show-config    # mostra la configurazione corrente
"""

import argparse
import json
import os
import platform
import shutil
import socket
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Percorsi
# ---------------------------------------------------------------------------

CONFIG_DIR = Path.home() / ".directa"
CONFIG_PATH = CONFIG_DIR / "ai-berkshire-config.json"
DARWIN_PORT_SETTINGS = Path.home() / ".directa" / "engine" / "APIPortSettings.txt"

REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
CLAUDE_COMMANDS_DIR = Path.home() / ".claude" / "commands"

DIRECTA_SKILLS = [
    "directa-portfolio.md",
    "directa-research.md",
]

DEFAULT_CONFIG = {
    "host": "127.0.0.1",
    "port_datafeed": 10001,
    "port_trading": 10002,
    "port_history": 10003,
    "timeout": 10,
    "heartbeat_interval": 8,
    "account_code": "",
    "note": "Configurazione AI Berkshire — Directa dAPI"
}

# ---------------------------------------------------------------------------
# Rilevamento automatico porte
# ---------------------------------------------------------------------------

def detect_ports_from_file() -> list[dict]:
    """
    Legge ~/.directa/engine/APIPortSettings.txt per rilevare le porte attive.
    Formato riga: codiceUtente;portaPrezzi;portaTrading;portaStorico
    """
    if not DARWIN_PORT_SETTINGS.exists():
        return []
    accounts = []
    with open(DARWIN_PORT_SETTINGS, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(";")
            if len(parts) >= 4:
                accounts.append({
                    "account_code": parts[0].strip(),
                    "port_datafeed": int(parts[1]),
                    "port_trading": int(parts[2]),
                    "port_history": int(parts[3]),
                })
    return accounts


def probe_port(host: str, port: int, timeout: float = 2.0) -> bool:
    """Verifica se una porta è raggiungibile."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (ConnectionRefusedError, OSError, socket.timeout):
        return False


def auto_detect_ports(host: str = "127.0.0.1") -> dict | None:
    """
    Tenta di rilevare automaticamente le porte Darwin attive.
    Prima legge il file di configurazione, poi fa un probe delle porte.
    """
    # 1. Prova dal file di configurazione Darwin
    accounts = detect_ports_from_file()
    if accounts:
        for acc in accounts:
            if probe_port(host, acc["port_trading"]):
                return acc

    # 2. Probe delle porte di default (utenza 1, 2, 3)
    for base in [10001, 10005, 10009]:
        trading_port = base + 1
        if probe_port(host, trading_port):
            return {
                "account_code": "",
                "port_datafeed": base,
                "port_trading": trading_port,
                "port_history": base + 2,
            }
    return None


# ---------------------------------------------------------------------------
# Verifica connessione
# ---------------------------------------------------------------------------

def verify_connection(cfg: dict) -> bool:
    """Invia DARWINSTATUS e verifica la risposta."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(cfg["timeout"])
        s.connect((cfg["host"], cfg["port_trading"]))
        s.sendall(b"DARWINSTATUS\n")
        response = s.recv(512).decode("utf-8", errors="replace").strip()
        s.close()
        if "DARWIN_STATUS" in response:
            if "CONN_OK" in response:
                return True
            elif "CONN_UNAVAILABLE" in response:
                print("  ⚠️  Darwin connessa ma server non raggiungibile (CONN_UNAVAILABLE).")
                return False
        return False
    except Exception as e:
        print(f"  ❌ Errore verifica: {e}")
        return False


# ---------------------------------------------------------------------------
# Installazione skill
# ---------------------------------------------------------------------------

def install_skills(force: bool = False) -> list[str]:
    """Copia le skill Directa in ~/.claude/commands/"""
    CLAUDE_COMMANDS_DIR.mkdir(parents=True, exist_ok=True)
    installed = []
    for skill_name in DIRECTA_SKILLS:
        src = SKILLS_DIR / skill_name
        dst = CLAUDE_COMMANDS_DIR / skill_name
        if not src.exists():
            print(f"  ⚠️  Skill non trovata: {src}")
            continue
        if dst.exists() and not force:
            print(f"  ℹ️  Già installata: {skill_name} (usa --force per sovrascrivere)")
            installed.append(str(dst))
            continue
        shutil.copy2(src, dst)
        print(f"  ✅ Installata: {skill_name} → {dst}")
        installed.append(str(dst))
    return installed


# ---------------------------------------------------------------------------
# Setup interattivo
# ---------------------------------------------------------------------------

def run_interactive_setup():
    """Procedura guidata di configurazione."""
    print("=" * 60)
    print("  AI Berkshire × Directa dAPI — Setup Guidato")
    print("=" * 60)
    print()
    print("  Questo script configura l'integrazione tra AI Berkshire")
    print("  e le API di trading Directa SIM (dAPI).")
    print()
    print("  Prerequisiti:")
    print("  1. Conto Directa attivo con API abilitate (info > 5a > 3h)")
    print("  2. Piattaforma Darwin aperta e loggata")
    print("  3. Claude Code installato")
    print()

    cfg = DEFAULT_CONFIG.copy()

    # --- Rilevamento automatico porte ---
    print("  [1/4] Rilevamento porte Darwin...")
    detected = auto_detect_ports()
    if detected:
        print(f"  ✅ Darwin rilevata!")
        print(f"     Codice conto: {detected.get('account_code', 'N/D')}")
        print(f"     DataFeed:     porta {detected['port_datafeed']}")
        print(f"     Trading:      porta {detected['port_trading']}")
        print(f"     Storico:      porta {detected['port_history']}")
        use_detected = input("\n  Usare queste porte? [S/n]: ").strip().lower()
        if use_detected != "n":
            cfg.update(detected)
        else:
            cfg = _ask_ports_manually(cfg)
    else:
        print("  ⚠️  Darwin non rilevata automaticamente.")
        print("     Assicurarsi che Darwin sia aperta e le API abilitate.")
        manual = input("\n  Inserire le porte manualmente? [S/n]: ").strip().lower()
        if manual != "n":
            cfg = _ask_ports_manually(cfg)
        else:
            print("  Uso porte di default (10001/10002/10003).")

    # --- Codice conto ---
    print("\n  [2/4] Codice conto Directa")
    if not cfg.get("account_code"):
        account = input("  Inserire il codice conto Directa (opzionale, premi Invio per saltare): ").strip()
        if account:
            cfg["account_code"] = account

    # --- Verifica connessione ---
    print("\n  [3/4] Verifica connessione a Darwin...")
    ok = verify_connection(cfg)
    if ok:
        print("  ✅ Connessione a Darwin verificata con successo!")
    else:
        print("  ❌ Connessione non riuscita.")
        print("     Verificare che Darwin sia aperta e le API abilitate.")
        proceed = input("  Continuare comunque? [s/N]: ").strip().lower()
        if proceed != "s":
            print("  Setup annullato.")
            sys.exit(1)

    # --- Salvataggio configurazione ---
    print("\n  [4/4] Salvataggio configurazione...")
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    print(f"  ✅ Configurazione salvata in: {CONFIG_PATH}")

    # --- Installazione skill ---
    print("\n  [Extra] Installazione skill Claude Code...")
    if CLAUDE_COMMANDS_DIR.parent.exists():
        install = input(f"  Installare le skill in {CLAUDE_COMMANDS_DIR}? [S/n]: ").strip().lower()
        if install != "n":
            installed = install_skills()
            if installed:
                print(f"  ✅ {len(installed)} skill installate.")
    else:
        print("  ℹ️  Claude Code non trovato. Installare le skill manualmente:")
        print(f"     cp skills/directa-*.md ~/.claude/commands/")

    print()
    print("=" * 60)
    print("  Setup completato!")
    print()
    print("  Comandi disponibili in Claude Code:")
    print("    /directa-portfolio   — Visualizza portafoglio e liquidità")
    print("    /directa-research    — Analisi approfondita degli asset posseduti")
    print()
    print("  Comandi CLI:")
    print("    python3 tools/directa_client.py portfolio")
    print("    python3 tools/directa_client.py export-full")
    print("=" * 60)


def _ask_ports_manually(cfg: dict) -> dict:
    """Chiede all'utente di inserire le porte manualmente."""
    print()
    for key, label, default in [
        ("port_datafeed", "DataFeed (default 10001)", 10001),
        ("port_trading", "Trading (default 10002)", 10002),
        ("port_history", "Storico (default 10003)", 10003),
    ]:
        val = input(f"  Porta {label}: ").strip()
        cfg[key] = int(val) if val.isdigit() else default
    return cfg


# ---------------------------------------------------------------------------
# Mostra configurazione corrente
# ---------------------------------------------------------------------------

def show_config():
    """Stampa la configurazione corrente."""
    print("=" * 60)
    print("  Configurazione AI Berkshire × Directa")
    print("=" * 60)
    if not CONFIG_PATH.exists():
        print(f"  ⚠️  Nessuna configurazione trovata in: {CONFIG_PATH}")
        print("  Eseguire: python3 tools/directa_setup.py")
        return
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    for k, v in cfg.items():
        print(f"  {k:<30}: {v}")
    print()
    print(f"  File: {CONFIG_PATH}")

    # Verifica connessione live
    print("\n  Verifica connessione live...")
    ok = verify_connection(cfg)
    print(f"  Stato Darwin: {'✅ CONNESSA' if ok else '❌ NON RAGGIUNGIBILE'}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Directa dAPI Setup — AI Berkshire",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--auto", action="store_true",
                        help="Auto-detect porte senza input interattivo")
    parser.add_argument("--install-skills", action="store_true",
                        help="Installa solo le skill Claude Code")
    parser.add_argument("--force", action="store_true",
                        help="Sovrascrive skill già installate")
    parser.add_argument("--show-config", action="store_true",
                        help="Mostra la configurazione corrente")

    args = parser.parse_args()

    if args.show_config:
        show_config()
        return

    if args.install_skills:
        print("Installazione skill Directa per Claude Code...")
        installed = install_skills(force=args.force)
        print(f"Installate: {len(installed)} skill")
        return

    if args.auto:
        print("Auto-setup Directa dAPI...")
        cfg = DEFAULT_CONFIG.copy()
        detected = auto_detect_ports()
        if detected:
            cfg.update(detected)
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(cfg, f, ensure_ascii=False, indent=2)
            print(f"✅ Configurazione salvata: {CONFIG_PATH}")
            ok = verify_connection(cfg)
            print(f"Connessione Darwin: {'✅ OK' if ok else '❌ FALLITA'}")
        else:
            print("❌ Darwin non rilevata. Aprire Darwin e riprovare.")
            sys.exit(1)
        install_skills(force=args.force)
        return

    # Setup interattivo di default
    run_interactive_setup()


if __name__ == "__main__":
    main()
