#!/usr/bin/env python3
"""
stock_screener.py — \u52a8\u91cf\u53d1\u73b0 + \u4ef7\u503c\u9a8c\u8bc1 \u9009\u80a1\u7b5b
\u7528\u6cd5：
  python3 stock_screener.py                   # \u626b\u63cf\u5168\u90e8 watchlist
  python3 stock_screener.py NVDA TSLA GOOG    # \u626b\u63cf\u6307\u5b9a\u6807\u7684
  python3 stock_screener.py --update MU       # \u66f4\u65b0 MU \u7684\u57fa\u672c\u9762\u6570\u636e

\u6846\u67b6：
  \u7b2c\u4e00\u5c42（\u52a8\u91cf\u53d1\u73b0）：60\u65e5\u65b0\u9ad8 + \u653e\u91cf\u786e\u8ba4 → \u8fdb\u5165\u5f85\u9009\u6c60
  \u7b2c\u4e8c\u5c42（\u4ef7\u503c\u9a8c\u8bc1）：6\u7ef4\u8bc4\u5206 ≥ 3/6 → \u4e70\u5165\u4fe1\u53f7
  \u4fe1\u53f7\u5206\u7ea7：3/6=\u8bd5\u63a2\u4ed33% | 4/6=\u6807\u51c6\u4ed35% | 5-6/6=\u786e\u4fe1\u4ed38%

\u6539\u8fdb\u70b9（\u6765\u81eaNVDA/AMD/MU\u56de\u6d4b）：
  1. \u6bdb\u5229\u7387\u8fde\u7eed2\u5b63\u6539\u5584 → \u72ec\u7acb\u4e70\u5165\u6761\u4ef6（\u89e3\u51b3NVDA 2023-01\u6f0f\u5224）
  2. EPS\u8d85\u9884\u671f>30% → \u5468\u671f\u80a1\u72ec\u7acb\u6761\u4ef6（\u89e3\u51b3MU\u5e95\u90e8\u4fe1\u53f7）
  3. \u4fe1\u53f7\u5206\u7ea7\u66ff\u4ee3\u4e8c\u5143\u5224\u65ad
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from collections import OrderedDict

# ============================================================
# \u914d\u7f6e
# ============================================================

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
FUND_FILE = os.path.join(DATA_DIR, "fundamentals.json")
WATCHLIST_FILE = os.path.join(DATA_DIR, "watchlist.json")

DEFAULT_WATCHLIST = {
    "us_ai_chip": ["NVDA", "AMD", "MU", "AVGO", "MRVL", "TSM"],
    "us_ai_app": ["GOOG", "META", "MSFT", "AMZN", "CRM", "NOW", "PLTR"],
    "us_ai_infra": ["ETN", "PWR", "VRT", "CRWV"],
    "us_crypto": ["COIN", "HOOD", "MSTR", "CRCL"],
    "hk_internet": ["0700.HK", "9888.HK", "1024.HK", "9992.HK"],
    "a_share": [],  # A\u80a1\u9700\u8981\u4e0d\u540c\u6570\u636e\u6e90，\u540e\u7eed\u6269\u5c55
}

# ============================================================
# \u4ef7\u683c\u6570\u636e\u83b7\u53d6（\u901a\u8fc7curl\u7ed5\u8fc7Python SSL\u95ee\u9898）
# ============================================================

def fetch_prices_curl(ticker, days=120):
    """\u7528curl\u83b7\u53d6Yahoo Finance\u65e5\u7ebf\u6570\u636e"""
    end_ts = int(datetime.now().timestamp())
    start_ts = int((datetime.now() - timedelta(days=days)).timestamp())
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        f"?period1={start_ts}&period2={end_ts}&interval=1d"
    )
    try:
        result = subprocess.run(
            ["curl", "-s", "-H", "User-Agent: Mozilla/5.0", url],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            return None
        data = json.loads(result.stdout)
        chart = data.get("chart", {}).get("result", [{}])[0]
        timestamps = chart.get("timestamp", [])
        quote = chart.get("indicators", {}).get("quote", [{}])[0]
        rows = []
        for i, ts in enumerate(timestamps):
            c = quote.get("close", [None] * len(timestamps))[i]
            v = quote.get("volume", [None] * len(timestamps))[i]
            h = quote.get("high", [None] * len(timestamps))[i]
            if c and v and h:
                dt = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                rows.append({"date": dt, "close": c, "high": h, "volume": v})
        return rows if len(rows) > 60 else None
    except Exception as e:
        return None


# ============================================================
# \u57fa\u672c\u9762\u6570\u636e\u7ba1\u7406
# ============================================================

def load_fundamentals():
    """\u52a0\u8f7d\u57fa\u672c\u9762\u6570\u636e"""
    if os.path.exists(FUND_FILE):
        with open(FUND_FILE) as f:
            return json.load(f)
    return {}


def save_fundamentals(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(FUND_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def update_fundamental_interactive(ticker):
    """\u4ea4\u4e92\u5f0f\u66f4\u65b0\u57fa\u672c\u9762\u6570\u636e"""
    funds = load_fundamentals()
    if ticker not in funds:
        funds[ticker] = {"quarters": {}}
    print(f"\n  \u66f4\u65b0 {ticker} \u57fa\u672c\u9762\u6570\u636e")
    print(f"  \u5df2\u6709\u5b63\u5ea6：{', '.join(funds[ticker]['quarters'].keys()) or '\u65e0'}")
    date = input("  \u8d22\u62a5\u53d1\u5e03\u65e5 (YYYY-MM-DD): ").strip()
    label = input("  \u6807\u7b7e (\u5982 Q1 2024): ").strip()
    rev_yoy = float(input("  \u8425\u6536\u540c\u6bd4\u589e\u901f (%): "))
    gm = float(input("  \u6bdb\u5229\u7387 (%): "))
    eps_beat = float(input("  EPS\u8d85\u9884\u671f (%): "))

    funds[ticker]["quarters"][date] = {
        "label": label, "rev_yoy": rev_yoy, "gm": gm, "eps_beat": eps_beat
    }
    save_fundamentals(funds)
    print(f"  ✅ \u5df2\u4fdd\u5b58 {ticker} {label}")


# ============================================================
# \u7b2c\u4e00\u5c42：\u52a8\u91cf\u53d1\u73b0
# ============================================================

def check_momentum(prices):
    """\u68c0\u67e5\u6700\u8fd1\u4ea4\u6613\u65e5\u662f\u5426\u89e6\u53d1\u52a8\u91cf\u4fe1\u53f7"""
    if len(prices) < 61:
        return None

    latest = prices[-1]
    close = latest["close"]

    # 60\u65e5\u65b0\u9ad8
    past_60_highs = [p["high"] for p in prices[-61:-1]]
    is_60d_high = close > max(past_60_highs)

    # \u653e\u91cf：\u8fd15\u65e5\u5747\u91cf > 20\u65e5\u5747\u91cf × 1.5
    vol_5 = sum(p["volume"] for p in prices[-5:]) / 5
    vol_20 = sum(p["volume"] for p in prices[-20:]) / 20
    vol_ratio = vol_5 / vol_20 if vol_20 > 0 else 0
    is_volume = vol_ratio > 1.5

    # 30\u65e5\u6da8\u5e45
    close_30d = prices[-31]["close"] if len(prices) > 30 else prices[0]["close"]
    pct_30d = (close - close_30d) / close_30d * 100

    # \u8fd15\u65e5\u6709\u7a81\u7834\u65e5（\u4e0d\u4e00\u5b9a\u662f\u4eca\u5929）
    recent_breakout = False
    for i in range(-5, 0):
        if prices[i]["close"] > max(p["high"] for p in prices[i-60:i]):
            recent_breakout = True
            break

    triggered = (is_60d_high or recent_breakout) and is_volume

    return {
        "triggered": triggered,
        "close": round(close, 2),
        "date": latest["date"],
        "is_60d_high": is_60d_high,
        "vol_ratio": round(vol_ratio, 2),
        "pct_30d": round(pct_30d, 1),
    }


# ============================================================
# \u7b2c\u4e8c\u5c42：\u4ef7\u503c\u9a8c\u8bc1（6\u7ef4，\u542b\u56de\u6d4b\u6539\u8fdb）
# ============================================================

def check_value(ticker, signal_date=None):
    """6\u7ef4\u4ef7\u503c\u9a8c\u8bc1"""
    funds = load_fundamentals()
    if ticker not in funds or not funds[ticker].get("quarters"):
        return None

    quarters = funds[ticker]["quarters"]
    sorted_q = sorted(quarters.items(), key=lambda x: x[0])

    # \u627e\u6700\u8fd1\u4e24\u4e2a\u5b63\u5ea6
    if signal_date:
        valid = [(d, q) for d, q in sorted_q if d <= signal_date]
    else:
        valid = sorted_q

    if not valid:
        return None

    latest = valid[-1]
    prev = valid[-2] if len(valid) >= 2 else None
    prev2 = valid[-3] if len(valid) >= 3 else None

    d = latest[1]
    pd = prev[1] if prev else None
    pd2 = prev2[1] if prev2 else None

    checks = {}

    # 1. \u8425\u6536\u52a0\u901f（\u540c\u6bd4\u589e\u901f\u5728\u6539\u5584）
    if pd:
        checks["\u8425\u6536\u52a0\u901f"] = d["rev_yoy"] > pd["rev_yoy"]
    else:
        checks["\u8425\u6536\u52a0\u901f"] = d["rev_yoy"] > 20

    # 2. \u6bdb\u5229\u7387\u65b9\u5411
    if pd:
        checks["\u6bdb\u5229\u7387\u6269\u5f20"] = d["gm"] > pd["gm"] or d["gm"] > 55
    else:
        checks["\u6bdb\u5229\u7387\u6269\u5f20"] = d["gm"] > 45

    # 3. EPS\u8d85\u9884\u671f > 10%
    checks["\u76c8\u5229\u60ca\u559c"] = d["eps_beat"] > 10

    # 4. \u8425\u6536\u9ad8\u589e\u957f > 15%
    checks["\u8425\u6536\u9ad8\u589e\u957f"] = d["rev_yoy"] > 15

    # 5. \u6bdb\u5229\u7387\u5065\u5eb7 > 40%
    checks["\u6bdb\u5229\u7387\u5065\u5eb7"] = d["gm"] > 40

    # 6. ★\u6539\u8fdb：\u6bdb\u5229\u7387\u8fde\u7eed2\u5b63\u6539\u5584（\u89e3\u51b3NVDA 2023-01\u6f0f\u5224）
    if pd and pd2:
        checks["\u6bdb\u5229\u8fde\u7eed\u6539\u5584"] = d["gm"] > pd["gm"] > pd2["gm"]
    elif pd:
        checks["\u6bdb\u5229\u8fde\u7eed\u6539\u5584"] = d["gm"] > pd["gm"]
    else:
        checks["\u6bdb\u5229\u8fde\u7eed\u6539\u5584"] = False

    score = sum(1 for v in checks.values() if v)

    # ★\u6539\u8fdb：\u72ec\u7acb\u901a\u8fc7\u6761\u4ef6
    independent_pass = False
    independent_reason = ""

    # \u6761\u4ef6A：\u6bdb\u5229\u7387\u8fde\u7eed2\u5b63\u6539\u5584 + \u6bdb\u5229>45%（NVDA 2023-01\u573a\u666f）
    if checks.get("\u6bdb\u5229\u8fde\u7eed\u6539\u5584") and d["gm"] > 45:
        independent_pass = True
        independent_reason = "\u6bdb\u5229\u7387\u8fde\u7eed\u6539\u5584+>45%"

    # \u6761\u4ef6B：EPS\u8d85\u9884\u671f>30%（MU\u5e95\u90e8\u573a\u666f）
    if d["eps_beat"] > 30:
        independent_pass = True
        independent_reason = "EPS\u8d85\u9884\u671f>30%（\u5468\u671f\u80a1\u4fe1\u53f7）"

    return {
        "score": score,
        "max": 6,
        "checks": checks,
        "fund": d,
        "fund_date": latest[0],
        "fund_label": d.get("label", ""),
        "independent_pass": independent_pass,
        "independent_reason": independent_reason,
    }


# ============================================================
# \u4fe1\u53f7\u5206\u7ea7
# ============================================================

def grade_signal(momentum, value):
    """\u7efc\u5408\u8bc4\u7ea7"""
    if not momentum or not momentum["triggered"]:
        return "SKIP", "\u65e0\u52a8\u91cf\u4fe1\u53f7", ""

    if not value:
        return "WATCH", "\u52a8\u91cf\u89e6\u53d1\u4f46\u65e0\u57fa\u672c\u9762\u6570\u636e", "\u8865\u5145\u57fa\u672c\u9762"

    score = value["score"]
    ind = value["independent_pass"]

    if score >= 5 or (score >= 4 and ind):
        return "BUY_8%", f"\u786e\u4fe1\u4ed3（{score}/6）", "\u5efa\u8bae8%\u4ed3\u4f4d"
    elif score >= 4 or (score >= 3 and ind):
        return "BUY_5%", f"\u6807\u51c6\u4ed3（{score}/6）", "\u5efa\u8bae5%\u4ed3\u4f4d"
    elif score >= 3:
        return "BUY_3%", f"\u8bd5\u63a2\u4ed3（{score}/6）", "\u5efa\u8bae3%\u4ed3\u4f4d"
    elif ind:
        return "BUY_3%", f"\u72ec\u7acb\u6761\u4ef6\u901a\u8fc7：{value['independent_reason']}", "\u5efa\u8bae3%\u4ed3\u4f4d"
    else:
        return "PASS", f"\u52a8\u91cf\u6709\u4f46\u57fa\u672c\u9762\u4e0d\u8db3（{score}/6）", "\u7ee7\u7eed\u89c2\u5bdf"


# ============================================================
# \u626b\u63cf\u4e00\u4e2a\u6807\u7684
# ============================================================

def scan_ticker(ticker, verbose=True):
    """\u626b\u63cf\u5355\u4e2a\u6807\u7684"""
    prices = fetch_prices_curl(ticker)
    if not prices:
        if verbose:
            print(f"  {ticker:<8} ⚠️  \u65e0\u6cd5\u83b7\u53d6\u4ef7\u683c\u6570\u636e")
        return None

    momentum = check_momentum(prices)
    value = check_value(ticker)
    grade, reason, advice = grade_signal(momentum, value)

    result = {
        "ticker": ticker,
        "grade": grade,
        "reason": reason,
        "advice": advice,
        "momentum": momentum,
        "value": value,
    }

    if verbose:
        # \u7d27\u51d1\u8f93\u51fa
        m = momentum
        symbol = {"BUY_8%": "🔴", "BUY_5%": "🟡", "BUY_3%": "🟢", "WATCH": "👀", "PASS": "⬜", "SKIP": "  "}
        s = symbol.get(grade, "  ")

        if grade.startswith("BUY"):
            print(f"  {s} {ticker:<8} ${m['close']:<8} 30\u65e5+{m['pct_30d']}% \u653e\u91cf{m['vol_ratio']}x  → {grade} {reason}")
            if value:
                v = value
                checks_str = " ".join(f"{'✅' if val else '❌'}{k}" for k, val in v["checks"].items())
                print(f"     \u57fa\u672c\u9762({v['fund_label']}): \u8425\u6536{v['fund']['rev_yoy']}% \u6bdb\u5229{v['fund']['gm']}% EPS\u8d85{v['fund']['eps_beat']}%")
                print(f"     {checks_str}")
                if v["independent_pass"]:
                    print(f"     ★\u72ec\u7acb\u901a\u8fc7：{v['independent_reason']}")
        elif grade == "WATCH":
            print(f"  {s} {ticker:<8} ${m['close']:<8} 30\u65e5+{m['pct_30d']}%  → \u52a8\u91cf\u89e6\u53d1！\u9700\u8865\u5145\u57fa\u672c\u9762\u6570\u636e")
        elif grade == "PASS":
            print(f"  {s} {ticker:<8} ${m['close']:<8}  → {reason}")
        # SKIP\u4e0d\u8f93\u51fa

    return result


# ============================================================
# \u4e3b\u7a0b\u5e8f
# ============================================================

def main():
    args = sys.argv[1:]

    # \u66f4\u65b0\u6a21\u5f0f
    if args and args[0] == "--update":
        ticker = args[1] if len(args) > 1 else input("  \u6807\u7684\u4ee3\u7801: ").strip().upper()
        update_fundamental_interactive(ticker)
        return

    # \u521d\u59cb\u5316\u9ed8\u8ba4watchlist
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(WATCHLIST_FILE):
        with open(WATCHLIST_FILE, "w") as f:
            json.dump(DEFAULT_WATCHLIST, f, indent=2)
        print(f"  \u5df2\u521b\u5efa\u9ed8\u8ba4watchlist: {WATCHLIST_FILE}")

    # \u786e\u5b9a\u626b\u63cf\u8303\u56f4
    if args:
        tickers = [t.upper() for t in args]
    else:
        with open(WATCHLIST_FILE) as f:
            wl = json.load(f)
        tickers = []
        for group, syms in wl.items():
            tickers.extend(syms)

    # \u6267\u884c\u626b\u63cf
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n{'='*70}")
    print(f"  \u52a8\u91cf\u53d1\u73b0 + \u4ef7\u503c\u9a8c\u8bc1 \u9009\u80a1\u7b5b  {today}")
    print(f"  \u626b\u63cf\u8303\u56f4：{len(tickers)} \u4e2a\u6807\u7684")
    print(f"{'='*70}\n")

    buy_signals = []
    watch_signals = []

    for ticker in tickers:
        result = scan_ticker(ticker)
        if result:
            if result["grade"].startswith("BUY"):
                buy_signals.append(result)
            elif result["grade"] == "WATCH":
                watch_signals.append(result)

    # \u6c47\u603b
    print(f"\n{'='*70}")
    print(f"  📋 \u626b\u63cf\u7ed3\u679c\u6c47\u603b")
    print(f"{'='*70}")

    if buy_signals:
        print(f"\n  🎯 \u4e70\u5165\u4fe1\u53f7：{len(buy_signals)} \u4e2a")
        for s in sorted(buy_signals, key=lambda x: x["grade"], reverse=True):
            m = s["momentum"]
            print(f"     {s['grade']:<8} {s['ticker']:<8} ${m['close']:<8} {s['reason']}")
    else:
        print(f"\n  \u65e0\u4e70\u5165\u4fe1\u53f7")

    if watch_signals:
        print(f"\n  👀 \u89c2\u5bdf（\u9700\u8865\u57fa\u672c\u9762）：{len(watch_signals)} \u4e2a")
        for s in watch_signals:
            m = s["momentum"]
            print(f"     {s['ticker']:<8} ${m['close']:<8} 30\u65e5+{m['pct_30d']}% — \u8bf7\u7528 --update {s['ticker']} \u8865\u5145")

    print(f"\n  \u57fa\u672c\u9762\u6570\u636e\u6587\u4ef6：{FUND_FILE}")
    print(f"  Watchlist\u6587\u4ef6：{WATCHLIST_FILE}")
    print(f"  \u7528 --update TICKER \u8865\u5145/\u66f4\u65b0\u57fa\u672c\u9762\n")


if __name__ == "__main__":
    main()
