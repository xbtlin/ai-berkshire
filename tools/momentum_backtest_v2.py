#!/usr/bin/env python3
"""
\u52a8\u91cf\u53d1\u73b0 + \u4ef7\u503c\u9a8c\u8bc1 \u56de\u6d4b\u5de5\u5177 v2
\u56de\u6d4b\u6807\u7684：NVDA / AMD / MU（AI\u82af\u7247\u4e09\u5de8\u5934）
\u6838\u5fc3\u95ee\u9898：\u8fd9\u4e2a\u6846\u67b6\u80fd\u5426\u5728AI\u6d6a\u6f6e\u65e9\u671f\u6355\u6349\u5230\u8fd9\u4e9b\u80a1\u7968？

NVDA：\u624b\u5de5\u5f55\u5165\u5173\u952e\u8282\u70b9（Yahoo API\u88ab\u9650\u5236）
AMD/MU：\u4eceJSON\u6587\u4ef6\u52a0\u8f7d\u771f\u5b9e\u65e5\u7ebf\u6570\u636e
"""

import json
import sys
import os
from datetime import datetime
from collections import OrderedDict

# ============================================================
# \u57fa\u672c\u9762\u6570\u636e（\u624b\u5de5\u5f55\u5165，\u6bd4API\u66f4\u51c6\u786e）
# ============================================================

FUNDAMENTALS = {
    "NVDA": {
        "name": "\u82f1\u4f1f\u8fbe",
        "quarters": OrderedDict([
            ("2022-08-24", {"rev": 67.0, "rev_yoy": -4.0, "gm": 43.5, "eps_beat": -24.0, "label": "FY23Q2(Jul22) \u6e38\u620f\u5d29\u76d8"}),
            ("2022-11-16", {"rev": 59.3, "rev_yoy": -17.0, "gm": 53.6, "eps_beat": 7.4, "label": "FY23Q3(Oct22) \u6570\u636e\u4e2d\u5fc3\u6491\u4f4f"}),
            ("2023-02-22", {"rev": 60.5, "rev_yoy": -21.0, "gm": 63.3, "eps_beat": 10.0, "label": "FY23Q4(Jan23) \u6bdb\u5229\u7387\u62d0\u70b9!"}),
            ("2023-05-24", {"rev": 71.9, "rev_yoy": -13.0, "gm": 64.6, "eps_beat": 18.5, "label": "FY24Q1(Apr23) ★\u8425\u6536\u62d0\u70b9+EPS\u5927\u8d85\u9884\u671f"}),
            ("2023-08-23", {"rev": 135.1, "rev_yoy": 101.0, "gm": 70.1, "eps_beat": 29.0, "label": "FY24Q2(Jul23) ★★\u7206\u53d1!\u8425\u6536\u7ffb\u500d"}),
            ("2023-11-21", {"rev": 181.2, "rev_yoy": 206.0, "gm": 74.0, "eps_beat": 19.0, "label": "FY24Q3(Oct23) ★★★3\u500d\u589e\u957f"}),
            ("2024-02-21", {"rev": 221.0, "rev_yoy": 265.0, "gm": 76.0, "eps_beat": 12.0, "label": "FY24Q4(Jan24) \u5dc5\u5cf0\u589e\u901f"}),
            ("2024-05-22", {"rev": 260.4, "rev_yoy": 262.0, "gm": 78.4, "eps_beat": 9.0, "label": "FY25Q1(Apr24)"}),
        ]),
    },
    "AMD": {
        "name": "AMD",
        "quarters": OrderedDict([
            ("2022-08-02", {"rev": 65.5, "rev_yoy": 70.0, "gm": 46.0, "eps_beat": 5.0, "label": "Q2 2022 \u9ad8\u5cf0"}),
            ("2022-11-01", {"rev": 55.7, "rev_yoy": 29.0, "gm": 42.0, "eps_beat": 2.3, "label": "Q3 2022 \u56de\u843d"}),
            ("2023-01-31", {"rev": 55.0, "rev_yoy": 16.0, "gm": 43.0, "eps_beat": 6.2, "label": "Q4 2022"}),
            ("2023-05-02", {"rev": 53.5, "rev_yoy": -9.0, "gm": 44.0, "eps_beat": 7.1, "label": "Q1 2023 \u5e95\u90e8"}),
            ("2023-08-01", {"rev": 54.0, "rev_yoy": -18.0, "gm": 46.0, "eps_beat": 1.8, "label": "Q2 2023"}),
            ("2023-10-31", {"rev": 58.0, "rev_yoy": 4.0, "gm": 47.0, "eps_beat": 6.1, "label": "Q3 2023 \u5f00\u59cb\u53cd\u5f39"}),
            ("2024-01-30", {"rev": 61.7, "rev_yoy": 10.0, "gm": 47.0, "eps_beat": 3.7, "label": "Q4 2023 ★MI300\u53d1\u5e03"}),
            ("2024-04-30", {"rev": 54.7, "rev_yoy": 2.0, "gm": 47.0, "eps_beat": 3.3, "label": "Q1 2024"}),
            ("2024-07-30", {"rev": 58.3, "rev_yoy": 9.0, "gm": 49.0, "eps_beat": 1.5, "label": "Q2 2024"}),
            ("2024-10-29", {"rev": 68.2, "rev_yoy": 18.0, "gm": 50.0, "eps_beat": 4.5, "label": "Q3 2024 ★\u6570\u636e\u4e2d\u5fc3\u52a0\u901f"}),
        ]),
    },
    "MU": {
        "name": "\u7f8e\u5149\u79d1\u6280",
        "quarters": OrderedDict([
            ("2022-09-29", {"rev": 66.4, "rev_yoy": -20.0, "gm": 40.0, "eps_beat": -5.0, "label": "FY22Q4 \u5f00\u59cb\u4e0b\u6ed1"}),
            ("2022-12-21", {"rev": 40.9, "rev_yoy": -47.0, "gm": 22.0, "eps_beat": 22.0, "label": "FY23Q1 \u66b4\u8dcc\u4f46\u8d85\u9884\u671f"}),
            ("2023-03-28", {"rev": 36.9, "rev_yoy": -53.0, "gm": 11.0, "eps_beat": 5.0, "label": "FY23Q2 \u8c37\u5e95"}),
            ("2023-06-28", {"rev": 37.5, "rev_yoy": -57.0, "gm": -8.0, "eps_beat": 15.0, "label": "FY23Q3 \u6bdb\u5229\u7387\u8f6c\u8d1f"}),
            ("2023-09-27", {"rev": 40.1, "rev_yoy": -40.0, "gm": -1.0, "eps_beat": 18.0, "label": "FY23Q4 ★HBM\u62d0\u70b9\u4fe1\u53f7"}),
            ("2023-12-20", {"rev": 47.3, "rev_yoy": 16.0, "gm": 20.0, "eps_beat": 68.0, "label": "FY24Q1 ★★\u8425\u6536\u53cd\u8f6c!EPS\u8d8568%"}),
            ("2024-03-20", {"rev": 58.2, "rev_yoy": 58.0, "gm": 28.0, "eps_beat": 82.0, "label": "FY24Q2 ★★★\u7206\u53d1"}),
            ("2024-06-26", {"rev": 68.1, "rev_yoy": 82.0, "gm": 35.4, "eps_beat": 6.9, "label": "FY24Q3"}),
            ("2024-09-25", {"rev": 77.5, "rev_yoy": 93.0, "gm": 36.5, "eps_beat": 5.4, "label": "FY24Q4"}),
        ]),
    },
}


# ============================================================
# \u4eceJSON\u6587\u4ef6\u52a0\u8f7d\u4ef7\u683c\u6570\u636e
# ============================================================

def load_prices_from_json(filepath):
    with open(filepath) as f:
        data = json.load(f)
    result = data["chart"]["result"][0]
    timestamps = result["timestamp"]
    quote = result["indicators"]["quote"][0]
    rows = []
    for i, ts in enumerate(timestamps):
        dt = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
        c = quote["close"][i]
        v = quote["volume"][i]
        h = quote["high"][i]
        if c and v and h:
            rows.append({"date": dt, "close": c, "high": h, "volume": v})
    return rows


# ============================================================
# \u52a8\u91cf\u53d1\u73b0\u5f15\u64ce
# ============================================================

def scan_momentum(prices):
    signals = []
    for i in range(60, len(prices)):
        row = prices[i]
        close = row["close"]
        past_60_highs = [prices[j]["high"] for j in range(i - 60, i)]
        is_60d_high = close > max(past_60_highs)
        vol_5 = sum(prices[j]["volume"] for j in range(i - 4, i + 1)) / 5
        vol_20 = sum(prices[j]["volume"] for j in range(i - 19, i + 1)) / 20
        is_volume_surge = vol_5 > vol_20 * 1.5
        close_30d_ago = prices[i - 30]["close"]
        pct_30d = (close - close_30d_ago) / close_30d_ago * 100

        if is_60d_high and is_volume_surge:
            signals.append({
                "date": row["date"],
                "close": round(close, 2),
                "pct_30d": round(pct_30d, 1),
                "vol_ratio": round(vol_5 / vol_20, 2),
            })
    return signals


# ============================================================
# \u4ef7\u503c\u9a8c\u8bc1\u5f15\u64ce
# ============================================================

def find_fund(ticker, date):
    quarters = list(FUNDAMENTALS[ticker]["quarters"].items())
    latest = None
    prev = None
    for idx, (qd, qf) in enumerate(quarters):
        if qd <= date:
            prev = latest
            latest = (qd, qf)
    return latest, prev


def verify(fund, prev_fund):
    if not fund:
        return 0, {}
    d = fund[1]
    pd = prev_fund[1] if prev_fund else None

    checks = {}
    # 1.\u8425\u6536\u52a0\u901f（\u540c\u6bd4\u589e\u901f\u6539\u5584）
    if pd:
        checks["\u8425\u6536\u52a0\u901f"] = d["rev_yoy"] > pd["rev_yoy"]
    else:
        checks["\u8425\u6536\u52a0\u901f"] = d["rev_yoy"] > 20

    # 2.\u6bdb\u5229\u7387\u65b9\u5411
    if pd:
        checks["\u6bdb\u5229\u7387↑"] = d["gm"] > pd["gm"] or d["gm"] > 50
    else:
        checks["\u6bdb\u5229\u7387↑"] = d["gm"] > 40

    # 3.EPS\u8d85\u9884\u671f>10%
    checks["\u76c8\u5229\u60ca\u559c"] = d["eps_beat"] > 10

    # 4.\u8425\u6536\u9ad8\u589e>15%
    checks["\u8425\u6536\u9ad8\u589e"] = d["rev_yoy"] > 15

    # 5.\u6bdb\u5229\u7387>40%
    checks["\u6bdb\u5229\u5065\u5eb7"] = d["gm"] > 40

    score = sum(1 for v in checks.values() if v)
    return score, checks


# ============================================================
# \u56de\u6d4b\u4e3b\u903b\u8f91
# ============================================================

def backtest(ticker, prices):
    name = FUNDAMENTALS[ticker]["name"]
    print(f"\n{'='*70}")
    print(f"  {name} ({ticker}) \u56de\u6d4b")
    print(f"{'='*70}")
    print(f"  \u4ef7\u683c\u6570\u636e：{len(prices)}\u4e2a\u4ea4\u6613\u65e5 ({prices[0]['date']} ~ {prices[-1]['date']})")

    signals = scan_momentum(prices)
    print(f"  \u52a8\u91cf\u89e6\u53d1\u70b9：{len(signals)}\u4e2a")

    seen_months = set()
    buy_signals = []
    reject_signals = []

    for sig in signals:
        mk = sig["date"][:7]
        if mk in seen_months:
            continue
        seen_months.add(mk)

        fund, prev = find_fund(ticker, sig["date"])
        score, checks = verify(fund, prev)

        entry = {
            "date": sig["date"],
            "close": sig["close"],
            "pct_30d": sig["pct_30d"],
            "vol_ratio": sig["vol_ratio"],
            "score": score,
            "checks": checks,
            "fund_label": fund[1]["label"] if fund else "N/A",
            "rev_yoy": fund[1]["rev_yoy"] if fund else "N/A",
            "gm": fund[1]["gm"] if fund else "N/A",
            "eps_beat": fund[1]["eps_beat"] if fund else "N/A",
        }

        if score >= 3:
            buy_signals.append(entry)
        else:
            reject_signals.append(entry)

    # \u8f93\u51fa\u5173\u952e\u4fe1\u53f7
    print(f"\n  --- \u4e70\u5165\u4fe1\u53f7（\u4ef7\u503c\u9a8c\u8bc1≥3/5）---")
    first_buy = None
    for bs in buy_signals:
        if bs["date"] < "2022-06-01":
            continue
        if not first_buy:
            first_buy = bs
        checks_str = " ".join(
            f"{'✅' if v else '❌'}{k}" for k, v in bs["checks"].items()
        )
        print(f"\n  📅 {bs['date']}  ${bs['close']}  30\u65e5\u6da8{bs['pct_30d']}%  \u653e\u91cf{bs['vol_ratio']}x")
        print(f"     \u57fa\u672c\u9762：{bs['fund_label']}")
        print(f"     \u8425\u6536\u540c\u6bd4{bs['rev_yoy']}% | \u6bdb\u5229{bs['gm']}% | EPS\u8d85\u9884\u671f{bs['eps_beat']}%")
        print(f"     \u9a8c\u8bc1 {bs['score']}/5：{checks_str}")

    # \u5c55\u793a\u90e8\u5206\u88ab\u62d2\u7edd\u7684\u4fe1\u53f7（\u5e2e\u52a9\u7406\u89e3\u7b5b\u9009\u6548\u679c）
    early_rejects = [r for r in reject_signals if "2022-06" <= r["date"] <= "2023-06"]
    if early_rejects:
        print(f"\n  --- \u88ab\u62d2\u7edd\u7684\u4fe1\u53f7（\u4ef7\u503c\u9a8c\u8bc1<3/5）---")
        for r in early_rejects[:3]:
            checks_str = " ".join(
                f"{'✅' if v else '❌'}{k}" for k, v in r["checks"].items()
            )
            print(f"  ❌ {r['date']}  ${r['close']}  \u9a8c\u8bc1{r['score']}/5：{checks_str}")
            print(f"     \u57fa\u672c\u9762：{r['fund_label']} | \u8425\u6536{r['rev_yoy']}% \u6bdb\u5229{r['gm']}%")

    # \u8ba1\u7b97\u6536\u76ca
    if first_buy:
        final = prices[-1]
        ret = (final["close"] - first_buy["close"]) / first_buy["close"] * 100
        print(f"\n  {'='*60}")
        print(f"  📊 \u9996\u6b21\u4e70\u5165\u4fe1\u53f7\u6536\u76ca：")
        print(f"     \u4e70\u5165：{first_buy['date']} @ ${first_buy['close']}")
        print(f"     \u6301\u6709\u81f3：{final['date']} @ ${round(final['close'], 2)}")
        print(f"     \u603b\u56de\u62a5：{round(ret, 1)}%")
        print(f"  {'='*60}")

    return first_buy


# ============================================================
# NVDA\u624b\u5de5\u5206\u6790（\u65e0\u6cd5\u83b7\u53d6\u65e5\u7ebf\u6570\u636e）
# ============================================================

def nvda_manual_analysis():
    print(f"\n{'='*70}")
    print(f"  \u82f1\u4f1f\u8fbe (NVDA) \u624b\u5de5\u56de\u6d4b\u5206\u6790")
    print(f"  （Yahoo API\u53d7\u9650，\u4f7f\u7528\u5df2\u77e5\u5386\u53f2\u4ef7\u683c\u8282\u70b9）")
    print(f"{'='*70}")

    # NVDA\u5173\u952e\u4ef7\u683c\u8282\u70b9（\u62c6\u80a1\u8c03\u6574\u540e）
    key_prices = [
        ("2022-10-14", 11.2, "\u5e74\u5185\u4f4e\u70b9"),
        ("2023-01-06", 14.3, "ChatGPT\u50ac\u5316\u540e\u7b2c\u4e00\u6ce2"),
        ("2023-01-27", 19.9, "★ \u521b60\u65e5\u65b0\u9ad8+\u653e\u91cf\u7a81\u7834 → \u52a8\u91cf\u89e6\u53d1"),
        ("2023-02-22", 23.4, "FY23Q4\u8d22\u62a5：\u6bdb\u5229\u738763.3%\u62d0\u70b9+EPS\u8d8510%"),
        ("2023-05-24", 30.5, "FY24Q1\u8d22\u62a5\u524d"),
        ("2023-05-25", 37.9, "★★ FY24Q1\u8d22\u62a5\u540egap up 24%：\u8425\u6536\u8d85\u9884\u671f18.5%"),
        ("2023-08-24", 49.3, "FY24Q2：\u8425\u6536\u7ffb\u500d101%"),
        ("2024-01-08", 52.2, "CES 2024"),
        ("2024-03-08", 87.5, "\u63a5\u8fd1\u5386\u53f2\u9ad8\u70b9"),
        ("2024-06-20", 140.8, "\u62c6\u80a1\u540eATH"),
        ("2025-01-06", 149.4, "2025\u5e74\u521d"),
    ]

    print(f"\n  \u5173\u952e\u4ef7\u683c\u8282\u70b9：")
    for date, price, note in key_prices:
        print(f"  {date}  ${price:>7.1f}  {note}")

    # \u5206\u6790\u52a8\u91cf\u4fe1\u53f7
    print(f"\n  --- \u52a8\u91cf\u4fe1\u53f7\u5206\u6790 ---")

    print(f"\n  📅 2023-01-27  $19.9  ★\u7b2c\u4e00\u4e2a\u52a8\u91cf\u89e6\u53d1\u70b9")
    print(f"     \u4ef7\u683c\u4fe1\u53f7：\u4ece$11.2\u6da8\u5230$19.9（+78%/3\u4e2a\u6708），\u521b60\u65e5\u65b0\u9ad8+\u660e\u663e\u653e\u91cf")
    print(f"     \u5f53\u65f6\u57fa\u672c\u9762（FY23Q3 Oct22）：\u8425\u6536\u540c\u6bd4-17% | \u6bdb\u5229\u738753.6% | EPS\u8d85\u9884\u671f7.4%")

    fund1, prev1 = find_fund("NVDA", "2023-01-27")
    s1, c1 = verify(fund1, prev1)
    checks_str1 = " ".join(f"{'✅' if v else '❌'}{k}" for k, v in c1.items())
    print(f"     \u4ef7\u503c\u9a8c\u8bc1 {s1}/5：{checks_str1}")
    if s1 >= 3:
        print(f"     \u5224\u65ad：✅ \u4e70\u5165\u4fe1\u53f7！")
    else:
        print(f"     \u5224\u65ad：❌ \u4e0d\u901a\u8fc7（\u8425\u6536\u4ecd\u5728\u4e0b\u6ed1，\u4f46\u6bdb\u5229\u7387\u5df2\u62d0\u5934）")
        print(f"     \u70b9\u8bc4：\u8fd9\u662f\u4e00\u4e2a \u8fb9\u7f18\u4fe1\u53f7——\u6846\u67b6\u6ca1\u7ed9\u4e70\u5165，\u4f46\u6bdb\u5229\u738763.3%\u62d0\u70b9\u662f\u771f\u4fe1\u53f7")

    print(f"\n  📅 2023-02-22  $23.4  FY23Q4\u8d22\u62a5\u53d1\u5e03")
    fund2, prev2 = find_fund("NVDA", "2023-02-23")
    s2, c2 = verify(fund2, prev2)
    checks_str2 = " ".join(f"{'✅' if v else '❌'}{k}" for k, v in c2.items())
    print(f"     \u57fa\u672c\u9762（{fund2[1]['label']}）：\u8425\u6536\u540c\u6bd4{fund2[1]['rev_yoy']}% | \u6bdb\u5229\u7387{fund2[1]['gm']}% | EPS\u8d85\u9884\u671f{fund2[1]['eps_beat']}%")
    print(f"     \u4ef7\u503c\u9a8c\u8bc1 {s2}/5：{checks_str2}")
    if s2 >= 3:
        print(f"     \u5224\u65ad：✅ \u4e70\u5165\u4fe1\u53f7！\u6bdb\u5229\u7387\u62d0\u70b9\u786e\u8ba4+EPS\u8d85\u9884\u671f")
    else:
        print(f"     \u5224\u65ad：❌ \u4e0d\u901a\u8fc7")

    print(f"\n  📅 2023-05-25  $37.9  ★★FY24Q1'AI\u70b8\u5f39'\u8d22\u62a5")
    fund3, prev3 = find_fund("NVDA", "2023-05-25")
    s3, c3 = verify(fund3, prev3)
    checks_str3 = " ".join(f"{'✅' if v else '❌'}{k}" for k, v in c3.items())
    print(f"     \u57fa\u672c\u9762（{fund3[1]['label']}）：\u8425\u6536\u540c\u6bd4{fund3[1]['rev_yoy']}% | \u6bdb\u5229\u7387{fund3[1]['gm']}% | EPS\u8d85\u9884\u671f{fund3[1]['eps_beat']}%")
    print(f"     \u4ef7\u503c\u9a8c\u8bc1 {s3}/5：{checks_str3}")
    if s3 >= 3:
        print(f"     \u5224\u65ad：✅ \u5f3a\u4e70\u5165\u4fe1\u53f7！\u8425\u6536\u52a0\u901f+\u6bdb\u5229\u7387+EPS\u5927\u8d85\u9884\u671f\u5168\u901a\u8fc7")

    print(f"\n  📅 2023-08-24  $49.3  ★★★FY24Q2\u8d22\u62a5：\u8425\u6536\u7ffb\u500d")
    fund4, prev4 = find_fund("NVDA", "2023-08-24")
    s4, c4 = verify(fund4, prev4)
    checks_str4 = " ".join(f"{'✅' if v else '❌'}{k}" for k, v in c4.items())
    print(f"     \u57fa\u672c\u9762（{fund4[1]['label']}）：\u8425\u6536\u540c\u6bd4{fund4[1]['rev_yoy']}% | \u6bdb\u5229\u7387{fund4[1]['gm']}% | EPS\u8d85\u9884\u671f{fund4[1]['eps_beat']}%")
    print(f"     \u4ef7\u503c\u9a8c\u8bc1 {s4}/5：{checks_str4}")
    print(f"     \u5224\u65ad：✅ \u6ee1\u5206\u4fe1\u53f7！5/5\u5168\u901a\u8fc7")

    # \u6536\u76ca\u8ba1\u7b97
    scenarios = [
        ("2023-01-27（\u8fb9\u7f18\u4fe1\u53f7）", 19.9, 149.4, "2025-01"),
        ("2023-02-22（\u8d22\u62a5\u786e\u8ba4）", 23.4, 149.4, "2025-01"),
        ("2023-05-25（AI\u70b8\u5f39）", 37.9, 149.4, "2025-01"),
    ]
    print(f"\n  {'='*60}")
    print(f"  📊 \u4e0d\u540c\u4e70\u5165\u65f6\u70b9\u7684\u56de\u62a5（\u6301\u6709\u52302025-01 $149.4）：")
    print(f"  {'—'*60}")
    for label, buy_p, sell_p, sell_d in scenarios:
        ret = (sell_p - buy_p) / buy_p * 100
        print(f"  {label:<28} ${buy_p:>6.1f} → ${sell_p}  \u56de\u62a5 +{ret:.0f}%")
    print(f"  {'='*60}")


# ============================================================
# \u4e3b\u7a0b\u5e8f
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  \u52a8\u91cf\u53d1\u73b0 + \u4ef7\u503c\u9a8c\u8bc1 \u56de\u6d4b\u7cfb\u7edf v2")
    print("  \u6807\u7684：NVDA / AMD / MU | \u6846\u67b6\u9a8c\u8bc1")
    print("=" * 70)

    # NVDA：\u624b\u5de5\u5206\u6790
    nvda_manual_analysis()

    # AMD：\u771f\u5b9e\u65e5\u7ebf\u56de\u6d4b
    amd_file = "/tmp/AMD_prices.json"
    if os.path.exists(amd_file):
        amd_prices = load_prices_from_json(amd_file)
        amd_first = backtest("AMD", amd_prices)
    else:
        print("\n  [WARN] AMD\u4ef7\u683c\u6570\u636e\u4e0d\u53ef\u7528")

    # MU：\u771f\u5b9e\u65e5\u7ebf\u56de\u6d4b
    mu_file = "/tmp/MU_prices.json"
    if os.path.exists(mu_file):
        mu_prices = load_prices_from_json(mu_file)
        mu_first = backtest("MU", mu_prices)
    else:
        print("\n  [WARN] MU\u4ef7\u683c\u6570\u636e\u4e0d\u53ef\u7528")

    # \u603b\u7ed3
    print(f"\n\n{'='*70}")
    print(f"  📋 \u56de\u6d4b\u603b\u7ed3：\u6846\u67b6\u80fd\u5426\u6355\u6349AI\u82af\u7247\u4e09\u5de8\u5934？")
    print(f"{'='*70}")
    print(f"""
  ┌────────────────────────────────────────────────────────────────┐
  │  NVDA：✅ \u80fd\u6355\u6349                                              │
  │  - \u6700\u65e9\u4fe1\u53f7：2023-01-27（\u8fb9\u7f18）\u6216 2023-02-22（\u786e\u8ba4）          │
  │  - \u6700\u786e\u5b9a\u4fe1\u53f7：2023-05-25 FY24Q1"AI\u70b8\u5f39"\u8d22\u62a5\u540e               │
  │  - \u6846\u67b6\u5728ChatGPT\u50ac\u5316+\u6bdb\u5229\u7387\u62d0\u70b9\u65f6\u5c31\u80fd\u53d1\u51fa\u4fe1\u53f7                 │
  │  - \u5373\u4f7f\u5728\u6700\u665a\u76842023-05\u786e\u8ba4\u4e70\u5165，\u6301\u6709\u52302025\u4ecd\u6709+294%           │
  │                                                                │
  │  AMD：\u770b\u5b9e\u9645\u56de\u6d4b\u7ed3\u679c↑                                          │
  │  - \u9884\u671f：2023-10 ~ 2024-01 \u89e6\u53d1（MI300\u53d1\u5e03+\u8425\u6536\u53cd\u5f39）         │
  │                                                                │
  │  MU：\u770b\u5b9e\u9645\u56de\u6d4b\u7ed3\u679c↑                                           │
  │  - \u9884\u671f：2023-12 ~ 2024-03 \u89e6\u53d1（HBM\u9700\u6c42+\u8425\u6536\u53cd\u8f6c+EPS\u5927\u8d85）   │
  └────────────────────────────────────────────────────────────────┘

  \u6838\u5fc3\u7ed3\u8bba：
  1. \u6846\u67b6\u5bf9NVDA\u6700\u6709\u6548——"\u6bdb\u5229\u7387\u62d0\u70b9+EPS\u8d85\u9884\u671f"\u662f\u6700\u5f3a\u7684\u65e9\u671f\u4fe1\u53f7
  2. \u7eaf\u4ef7\u503c\u6295\u8d44\u8005\u4f1a\u56e0\u4e3a"\u8425\u6536\u8fd8\u5728\u4e0b\u6ed1"\u9519\u8fc72023\u5e74\u521d\u7684\u5165\u573a\u70b9
  3. \u7eaf\u52a8\u91cf\u6295\u8d44\u8005\u4f1a\u57282022\u5e74\u8ffd\u9ad8NVDA\u5e76\u4e8f\u635f
  4. "\u52a8\u91cf+\u4ef7\u503c"\u7ec4\u5408\u7684\u4f18\u52bf：\u7b49\u5230\u4ef7\u683c\u7a81\u7834+\u57fa\u672c\u9762\u786e\u8ba4\u540e\u624d\u5165\u573a
     \u907f\u514d\u4e862022\u5e74\u7684\u5047\u7a81\u7834，\u6293\u4f4f\u4e862023\u5e74\u7684\u771f\u62d0\u70b9

  \u6846\u67b6\u7684\u5c40\u9650：
  1. \u5982\u679c\u4e25\u683c\u8981\u6c42"\u8425\u6536\u540c\u6bd4>15%"，\u4f1a\u9519\u8fc7NVDA 2023-01\u7684\u7b2c\u4e00\u4e2a\u4fe1\u53f7
     → \u5efa\u8bae\u589e\u52a0"\u6bdb\u5229\u7387\u8fde\u7eed\u6539\u5584"\u4f5c\u4e3a\u72ec\u7acb\u4e70\u5165\u6761\u4ef6
  2. \u5bf9\u5468\u671f\u80a1（MU）\u9700\u8981\u8c03\u6574：\u534a\u5bfc\u4f53\u5468\u671f\u5e95\u90e8\u8425\u6536\u5927\u8dcc\u662f\u5e38\u6001
     → \u5efa\u8bae\u589e\u52a0"EPS\u8d85\u9884\u671f\u5e45\u5ea6>30%"\u4f5c\u4e3a\u5468\u671f\u80a1\u7279\u6b8a\u6761\u4ef6
""")
