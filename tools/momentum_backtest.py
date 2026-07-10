#!/usr/bin/env python3
"""
\u52a8\u91cf\u53d1\u73b0 + \u4ef7\u503c\u9a8c\u8bc1 \u56de\u6d4b\u5de5\u5177
\u56de\u6d4b\u6807\u7684：NVDA / AMD / MU（AI\u82af\u7247\u4e09\u5de8\u5934）
\u65f6\u95f4\u8303\u56f4：2022-01 ~ 2025-12
\u6838\u5fc3\u95ee\u9898：\u8fd9\u4e2a\u6846\u67b6\u80fd\u5426\u5728AI\u6d6a\u6f6e\u65e9\u671f\u6355\u6349\u5230\u8fd9\u4e9b\u80a1\u7968？
"""

import json
import sys
from datetime import datetime, timedelta
from urllib.request import urlopen, Request
from collections import OrderedDict

# ============================================================
# \u7b2c\u4e00\u90e8\u5206：\u83b7\u53d6\u5386\u53f2\u4ef7\u683c\u6570\u636e（Yahoo Finance Chart API）
# ============================================================

def fetch_price_data(ticker, start_date="2021-06-01", end_date="2025-12-31"):
    """\u901a\u8fc7Yahoo Finance API\u83b7\u53d6\u65e5\u7ebf\u6570\u636e"""
    start_ts = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    end_ts = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        f"?period1={start_ts}&period2={end_ts}&interval=1d"
    )
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        resp = urlopen(req, timeout=15)
        data = json.loads(resp.read().decode())
        result = data["chart"]["result"][0]
        timestamps = result["timestamp"]
        quote = result["indicators"]["quote"][0]
        rows = []
        for i, ts in enumerate(timestamps):
            dt = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
            c = quote["close"][i]
            v = quote["volume"][i]
            o = quote["open"][i]
            h = quote["high"][i]
            l = quote["low"][i]
            if c and v:
                rows.append({"date": dt, "open": o, "high": h, "low": l, "close": c, "volume": v})
        return rows
    except Exception as e:
        print(f"  [WARN] \u65e0\u6cd5\u83b7\u53d6 {ticker} \u4ef7\u683c\u6570\u636e: {e}")
        return None


# ============================================================
# \u7b2c\u4e8c\u90e8\u5206：\u624b\u5de5\u8f93\u5165\u5173\u952e\u5b63\u5ea6\u57fa\u672c\u9762\u6570\u636e
# （API\u83b7\u53d6\u5b63\u5ea6\u8d22\u52a1\u6570\u636e\u4e0d\u53ef\u9760，\u6838\u5fc3\u6570\u636e\u624b\u5de5\u5f55\u5165\u66f4\u51c6\u786e）
# ============================================================

FUNDAMENTALS = {
    "NVDA": {
        "name": "\u82f1\u4f1f\u8fbe",
        "quarters": OrderedDict([
            # (\u8d22\u62a5\u53d1\u5e03\u65e5, {\u8425\u6536\u4ebf\u7f8e\u5143, \u8425\u6536\u540c\u6bd4\u589e\u901f, \u6bdb\u5229\u7387, EPS, EPS\u8d85\u9884\u671f%})
            # FY2023 = calendar 2022
            ("2022-05-25", {"rev": 82.9, "rev_yoy": 46.0, "gm": 65.5, "eps": 1.36, "eps_beat": 4.6, "label": "FY23Q1 (Apr22)"}),
            ("2022-08-24", {"rev": 67.0, "rev_yoy": -4.0, "gm": 43.5, "eps": 0.51, "eps_beat": -24.0, "label": "FY23Q2 (Jul22)"}),
            ("2022-11-16", {"rev": 59.3, "rev_yoy": -17.0, "gm": 53.6, "eps": 0.58, "eps_beat": 7.4, "label": "FY23Q3 (Oct22)"}),
            ("2023-02-22", {"rev": 60.5, "rev_yoy": -21.0, "gm": 63.3, "eps": 0.88, "eps_beat": 10.0, "label": "FY23Q4 (Jan23)"}),
            # FY2024 = calendar 2023 — AI\u7206\u53d1
            ("2023-05-24", {"rev": 71.9, "rev_yoy": -13.0, "gm": 64.6, "eps": 1.09, "eps_beat": 18.5, "label": "FY24Q1 (Apr23) ★ AI\u62d0\u70b9"}),
            ("2023-08-23", {"rev": 135.1, "rev_yoy": 101.0, "gm": 70.1, "eps": 2.70, "eps_beat": 29.0, "label": "FY24Q2 (Jul23) ★★ \u7206\u53d1"}),
            ("2023-11-21", {"rev": 181.2, "rev_yoy": 206.0, "gm": 74.0, "eps": 4.02, "eps_beat": 19.0, "label": "FY24Q3 (Oct23) ★★★"}),
            ("2024-02-21", {"rev": 221.0, "rev_yoy": 265.0, "gm": 76.0, "eps": 5.16, "eps_beat": 12.0, "label": "FY24Q4 (Jan24)"}),
            ("2024-05-22", {"rev": 260.4, "rev_yoy": 262.0, "gm": 78.4, "eps": 6.12, "eps_beat": 9.0, "label": "FY25Q1 (Apr24)"}),
            ("2024-08-28", {"rev": 300.4, "rev_yoy": 122.0, "gm": 75.1, "eps": 0.68, "eps_beat": 5.6, "label": "FY25Q2 (Jul24)"}),
        ]),
    },
    "AMD": {
        "name": "AMD",
        "quarters": OrderedDict([
            ("2022-05-03", {"rev": 58.9, "rev_yoy": 71.0, "gm": 48.0, "eps": 1.13, "eps_beat": 9.7, "label": "Q1 2022"}),
            ("2022-08-02", {"rev": 65.5, "rev_yoy": 70.0, "gm": 46.0, "eps": 1.05, "eps_beat": 5.0, "label": "Q2 2022"}),
            ("2022-11-01", {"rev": 55.7, "rev_yoy": 29.0, "gm": 42.0, "eps": 0.67, "eps_beat": 2.3, "label": "Q3 2022"}),
            ("2023-01-31", {"rev": 55.0, "rev_yoy": 16.0, "gm": 43.0, "eps": 0.69, "eps_beat": 6.2, "label": "Q4 2022"}),
            ("2023-05-02", {"rev": 53.5, "rev_yoy": -9.0, "gm": 44.0, "eps": 0.60, "eps_beat": 7.1, "label": "Q1 2023"}),
            ("2023-08-01", {"rev": 54.0, "rev_yoy": -18.0, "gm": 46.0, "eps": 0.58, "eps_beat": 1.8, "label": "Q2 2023"}),
            ("2023-10-31", {"rev": 58.0, "rev_yoy": 4.0, "gm": 47.0, "eps": 0.70, "eps_beat": 6.1, "label": "Q3 2023"}),
            ("2024-01-30", {"rev": 61.7, "rev_yoy": 10.0, "gm": 47.0, "eps": 0.77, "eps_beat": 3.7, "label": "Q4 2023 ★ MI300\u53d1\u5e03"}),
            ("2024-04-30", {"rev": 54.7, "rev_yoy": 2.0, "gm": 47.0, "eps": 0.62, "eps_beat": 3.3, "label": "Q1 2024"}),
            ("2024-07-30", {"rev": 58.3, "rev_yoy": 9.0, "gm": 49.0, "eps": 0.69, "eps_beat": 1.5, "label": "Q2 2024"}),
            ("2024-10-29", {"rev": 68.2, "rev_yoy": 18.0, "gm": 50.0, "eps": 0.92, "eps_beat": 4.5, "label": "Q3 2024 ★ AI\u52a0\u901f"}),
        ]),
    },
    "MU": {
        "name": "\u7f8e\u5149\u79d1\u6280",
        "quarters": OrderedDict([
            ("2022-06-30", {"rev": 86.4, "rev_yoy": 16.0, "gm": 47.0, "eps": 2.59, "eps_beat": 4.0, "label": "FY22Q3 (May22)"}),
            ("2022-09-29", {"rev": 66.4, "rev_yoy": -20.0, "gm": 40.0, "eps": 1.45, "eps_beat": -5.0, "label": "FY22Q4 (Aug22)"}),
            ("2022-12-21", {"rev": 40.9, "rev_yoy": -47.0, "gm": 22.0, "eps": -0.04, "eps_beat": 22.0, "label": "FY23Q1 (Nov22)"}),
            ("2023-03-28", {"rev": 36.9, "rev_yoy": -53.0, "gm": 11.0, "eps": -1.91, "eps_beat": 5.0, "label": "FY23Q2 (Feb23)"}),
            ("2023-06-28", {"rev": 37.5, "rev_yoy": -57.0, "gm": -8.0, "eps": -1.43, "eps_beat": 15.0, "label": "FY23Q3 (May23)"}),
            ("2023-09-27", {"rev": 40.1, "rev_yoy": -40.0, "gm": -1.0, "eps": -1.07, "eps_beat": 18.0, "label": "FY23Q4 (Aug23) ★ HBM\u62d0\u70b9"}),
            ("2023-12-20", {"rev": 47.3, "rev_yoy": 16.0, "gm": 20.0, "eps": -0.95, "eps_beat": 68.0, "label": "FY24Q1 (Nov23) ★★ \u53cd\u8f6c"}),
            ("2024-03-20", {"rev": 58.2, "rev_yoy": 58.0, "gm": 28.0, "eps": 0.42, "eps_beat": 82.0, "label": "FY24Q2 (Feb24) ★★★"}),
            ("2024-06-26", {"rev": 68.1, "rev_yoy": 82.0, "gm": 35.4, "eps": 0.62, "eps_beat": 6.9, "label": "FY24Q3 (May24)"}),
            ("2024-09-25", {"rev": 77.5, "rev_yoy": 93.0, "gm": 36.5, "eps": 1.18, "eps_beat": 5.4, "label": "FY24Q4 (Aug24)"}),
        ]),
    },
}


# ============================================================
# \u7b2c\u4e09\u90e8\u5206：\u52a8\u91cf\u53d1\u73b0\u5f15\u64ce（\u7b2c\u4e00\u5c42\u7b5b\u9009）
# ============================================================

def compute_momentum_signals(prices):
    """\u8ba1\u7b97\u52a8\u91cf\u4fe1\u53f7"""
    signals = []
    for i in range(60, len(prices)):
        row = prices[i]
        date = row["date"]
        close = row["close"]

        # 60\u65e5\u65b0\u9ad8
        past_60_highs = [prices[j]["high"] for j in range(i - 60, i)]
        is_60d_high = close > max(past_60_highs)

        # \u653e\u91cf\u786e\u8ba4：\u8fd15\u65e5\u5747\u91cf > 20\u65e5\u5747\u91cf\u76842\u500d
        vol_5 = sum(prices[j]["volume"] for j in range(i - 4, i + 1)) / 5
        vol_20 = sum(prices[j]["volume"] for j in range(i - 19, i + 1)) / 20
        is_volume_surge = vol_5 > vol_20 * 1.8  # \u653e\u5bbd\u52301.8\u500d

        # 30\u65e5\u6da8\u5e45
        close_30d_ago = prices[i - 30]["close"]
        pct_30d = (close - close_30d_ago) / close_30d_ago * 100

        # \u7efc\u5408\u5224\u65ad
        momentum_triggered = is_60d_high and is_volume_surge

        if momentum_triggered:
            signals.append({
                "date": date,
                "close": round(close, 2),
                "pct_30d": round(pct_30d, 1),
                "vol_ratio": round(vol_5 / vol_20, 2),
                "is_60d_high": is_60d_high,
            })

    return signals


# ============================================================
# \u7b2c\u56db\u90e8\u5206：\u4ef7\u503c\u9a8c\u8bc1\u5f15\u64ce（\u7b2c\u4e8c\u5c42\u7b5b\u9009）
# ============================================================

def find_latest_fundamental(ticker, signal_date):
    """\u627e\u5230\u4fe1\u53f7\u65e5\u671f\u4e4b\u524d\u6700\u8fd1\u7684\u4e00\u4e2a\u5b63\u5ea6\u8d22\u62a5"""
    quarters = FUNDAMENTALS[ticker]["quarters"]
    latest = None
    latest_date = None
    for q_date, q_data in quarters.items():
        if q_date <= signal_date:
            latest = q_data
            latest_date = q_date
    return latest_date, latest


def verify_value(ticker, fund_data, prev_fund_data=None):
    """5\u7ef4\u4ef7\u503c\u9a8c\u8bc1"""
    if not fund_data:
        return {"score": 0, "details": "\u65e0\u57fa\u672c\u9762\u6570\u636e"}

    checks = {}

    # 1. \u8425\u6536\u52a0\u901f（\u8425\u6536\u540c\u6bd4\u589e\u901f\u662f\u5426\u5728\u6539\u5584）
    rev_yoy = fund_data.get("rev_yoy", 0)
    if prev_fund_data:
        prev_rev_yoy = prev_fund_data.get("rev_yoy", 0)
        rev_accelerating = rev_yoy > prev_rev_yoy
    else:
        rev_accelerating = rev_yoy > 20
    checks["\u8425\u6536\u52a0\u901f"] = rev_accelerating

    # 2. \u6bdb\u5229\u7387\u65b9\u5411（>45%\u4e14\u4e0d\u840e\u7f29）
    gm = fund_data.get("gm", 0)
    if prev_fund_data:
        prev_gm = prev_fund_data.get("gm", 0)
        gm_expanding = gm > prev_gm or gm > 50
    else:
        gm_expanding = gm > 45
    checks["\u6bdb\u5229\u7387\u6269\u5f20"] = gm_expanding

    # 3. EPS\u8d85\u9884\u671f（>10%\u4e3a\u5f3a\u4fe1\u53f7）
    eps_beat = fund_data.get("eps_beat", 0)
    checks["\u76c8\u5229\u60ca\u559c"] = eps_beat > 10

    # 4. \u8425\u6536\u589e\u901f\u672c\u8eab（>15%）
    checks["\u8425\u6536\u9ad8\u589e\u957f"] = rev_yoy > 15

    # 5. \u6bdb\u5229\u7387\u7edd\u5bf9\u503c（>40%，\u82af\u7247\u884c\u4e1a\u6807\u51c6）
    checks["\u6bdb\u5229\u7387\u5065\u5eb7"] = gm > 40

    score = sum(1 for v in checks.values() if v)
    return {"score": score, "max": 5, "details": checks, "fund": fund_data}


# ============================================================
# \u7b2c\u4e94\u90e8\u5206：\u56de\u6d4b\u4e3b\u903b\u8f91
# ============================================================

def backtest_ticker(ticker):
    """\u5bf9\u5355\u4e2a\u6807\u7684\u8fdb\u884c\u5b8c\u6574\u56de\u6d4b"""
    print(f"\n{'='*70}")
    print(f"  \u56de\u6d4b\u6807\u7684：{FUNDAMENTALS[ticker]['name']} ({ticker})")
    print(f"{'='*70}")

    # \u83b7\u53d6\u4ef7\u683c\u6570\u636e
    print(f"\n  [1/3] \u83b7\u53d6\u5386\u53f2\u4ef7\u683c\u6570\u636e...")
    prices = fetch_price_data(ticker, "2021-06-01", "2025-06-30")
    if not prices:
        print("  ❌ \u65e0\u6cd5\u83b7\u53d6\u4ef7\u683c\u6570\u636e，\u8df3\u8fc7")
        return None

    print(f"  \u83b7\u53d6\u5230 {len(prices)} \u4e2a\u4ea4\u6613\u65e5\u6570\u636e ({prices[0]['date']} ~ {prices[-1]['date']})")

    # \u8ba1\u7b97\u52a8\u91cf\u4fe1\u53f7
    print(f"\n  [2/3] \u626b\u63cf\u52a8\u91cf\u4fe1\u53f7...")
    momentum_signals = compute_momentum_signals(prices)
    print(f"  \u53d1\u73b0 {len(momentum_signals)} \u4e2a\u52a8\u91cf\u89e6\u53d1\u70b9")

    # \u4ef7\u503c\u9a8c\u8bc1
    print(f"\n  [3/3] \u5bf9\u52a8\u91cf\u4fe1\u53f7\u8fdb\u884c\u4ef7\u503c\u9a8c\u8bc1...")

    buy_signals = []
    seen_months = set()

    for sig in momentum_signals:
        month_key = sig["date"][:7]
        if month_key in seen_months:
            continue  # \u540c\u6708\u53ea\u53d6\u7b2c\u4e00\u4e2a\u4fe1\u53f7
        seen_months.add(month_key)

        # \u627e\u57fa\u672c\u9762\u6570\u636e
        q_date, fund = find_latest_fundamental(ticker, sig["date"])
        if not fund:
            continue

        # \u627e\u524d\u4e00\u5b63\u5ea6\u6570\u636e\u505a\u5bf9\u6bd4
        quarters_list = list(FUNDAMENTALS[ticker]["quarters"].items())
        prev_fund = None
        for idx, (qd, qf) in enumerate(quarters_list):
            if qd == q_date and idx > 0:
                prev_fund = quarters_list[idx - 1][1]
                break

        verification = verify_value(ticker, fund, prev_fund)

        result = {
            "date": sig["date"],
            "close": sig["close"],
            "pct_30d": sig["pct_30d"],
            "vol_ratio": sig["vol_ratio"],
            "fund_date": q_date,
            "fund_label": fund.get("label", ""),
            "value_score": verification["score"],
            "value_max": verification["max"],
            "details": verification["details"],
            "rev_yoy": fund.get("rev_yoy", "N/A"),
            "gm": fund.get("gm", "N/A"),
            "eps_beat": fund.get("eps_beat", "N/A"),
        }

        # \u4e70\u5165\u4fe1\u53f7：\u4ef7\u503c\u9a8c\u8bc1>=3/5
        if verification["score"] >= 3:
            result["action"] = "✅ \u4e70\u5165\u4fe1\u53f7"
            buy_signals.append(result)
        else:
            result["action"] = "❌ \u4e0d\u901a\u8fc7"

    # \u8f93\u51fa\u7ed3\u679c
    print(f"\n  {'—'*60}")
    print(f"  \u52a8\u91cf\u53d1\u73b0 + \u4ef7\u503c\u9a8c\u8bc1\u7ed3\u679c：")
    print(f"  {'—'*60}")

    all_signals_with_action = []
    for sig in momentum_signals:
        month_key = sig["date"][:7]
        found = False
        for bs in buy_signals:
            if bs["date"][:7] == month_key:
                all_signals_with_action.append(bs)
                found = True
                break

    # \u53ea\u5c55\u793a\u5173\u952e\u65f6\u95f4\u7a97\u53e3\u7684\u4fe1\u53f7
    first_buy = None
    for bs in buy_signals:
        if bs["date"] >= "2022-06-01":
            if not first_buy:
                first_buy = bs
            print(f"\n  📅 {bs['date']} | \u6536\u76d8\u4ef7 ${bs['close']}")
            print(f"     \u52a8\u91cf：30\u65e5\u6da8\u5e45 {bs['pct_30d']}% | \u653e\u91cf\u500d\u6570 {bs['vol_ratio']}x")
            print(f"     \u57fa\u672c\u9762（{bs['fund_label']}）：")
            print(f"       \u8425\u6536\u540c\u6bd4 {bs['rev_yoy']}% | \u6bdb\u5229\u7387 {bs['gm']}% | EPS\u8d85\u9884\u671f {bs['eps_beat']}%")
            print(f"     \u4ef7\u503c\u9a8c\u8bc1：{bs['value_score']}/{bs['value_max']} ", end="")
            for k, v in bs["details"].items():
                print(f"{'✅' if v else '❌'}{k} ", end="")
            print(f"\n     \u5224\u65ad：{bs['action']}")

    # \u8ba1\u7b97\u5047\u8bbe\u6536\u76ca
    if first_buy and prices:
        buy_price = first_buy["close"]
        buy_date = first_buy["date"]
        # \u627e1\u5e74\u540e\u548c2\u5e74\u540e\u7684\u4ef7\u683c
        for p in prices:
            if p["date"] >= buy_date:
                final_price = p["close"]
        final_date = prices[-1]["date"]
        total_return = (final_price - buy_price) / buy_price * 100

        print(f"\n  {'='*60}")
        print(f"  📊 \u5047\u8bbe\u5728\u9996\u6b21\u4e70\u5165\u4fe1\u53f7\u6267\u884c：")
        print(f"     \u4e70\u5165\u65e5：{buy_date} @ ${buy_price}")
        print(f"     \u6700\u7ec8\u65e5：{final_date} @ ${round(final_price, 2)}")
        print(f"     \u603b\u56de\u62a5：{round(total_return, 1)}%")
        print(f"  {'='*60}")

    return {"ticker": ticker, "buy_signals": buy_signals, "first_buy": first_buy}


# ============================================================
# \u4e3b\u7a0b\u5e8f
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  \u52a8\u91cf\u53d1\u73b0 + \u4ef7\u503c\u9a8c\u8bc1 \u56de\u6d4b\u7cfb\u7edf")
    print("  \u6807\u7684：NVDA / AMD / MU | \u65f6\u95f4：2022-2025")
    print("=" * 70)

    results = {}
    for ticker in ["NVDA", "AMD", "MU"]:
        result = backtest_ticker(ticker)
        if result:
            results[ticker] = result

    # \u603b\u7ed3
    print(f"\n\n{'='*70}")
    print(f"  📋 \u56de\u6d4b\u603b\u7ed3")
    print(f"{'='*70}")
    print(f"\n  {'\u6807\u7684':<8} {'\u9996\u6b21\u4e70\u5165\u4fe1\u53f7':<16} {'\u4e70\u5165\u4ef7':<12} {'\u89e6\u53d1\u57fa\u672c\u9762'}")
    print(f"  {'—'*65}")
    for ticker, r in results.items():
        if r["first_buy"]:
            fb = r["first_buy"]
            print(f"  {ticker:<8} {fb['date']:<16} ${fb['close']:<10} {fb['fund_label']}")
        else:
            print(f"  {ticker:<8} {'\u65e0\u4e70\u5165\u4fe1\u53f7':<16}")

    print(f"\n  \u5173\u952e\u95ee\u9898\u56de\u7b54：")
    print(f"  ┌─────────────────────────────────────────────────────────────┐")
    print(f"  │ \u8fd9\u4e2a\u6846\u67b6\u80fd\u5426\u5728AI\u6d6a\u6f6e\u65e9\u671f\u6355\u6349\u5230NVDA/AMD/MU？              │")
    print(f"  │ \u7b54\u6848\u89c1\u4e0a\u65b9\u8be6\u7ec6\u5206\u6790。                                       │")
    print(f"  └─────────────────────────────────────────────────────────────┘")
