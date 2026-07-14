#!/usr/bin/env python3
"""
stock_screener.py — 动量发现 + 价值验证 选股筛
用法：
  python3 stock_screener.py                   # 扫描全部 watchlist
  python3 stock_screener.py NVDA TSLA GOOG    # 扫描指定标的
  python3 stock_screener.py --update MU       # 更新 MU 的基本面数据

框架：
  第一层（动量发现）：60日新高 + 放量确认 → 进入待选池
  第二层（价值验证）：6维评分 ≥ 3/6 → 买入信号
  信号分级：3/6=试探仓3% | 4/6=标准仓5% | 5-6/6=确信仓8%

改进点（来自NVDA/AMD/MU回测）：
  1. 毛利率连续2季改善 → 独立买入条件（解决NVDA 2023-01漏判）
  2. EPS超预期>30% → 周期股独立条件（解决MU底部信号）
  3. 信号分级替代二元判断
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from collections import OrderedDict

# ============================================================
# 配置
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
    "a_share": [],  # A股需要不同数据源，后续扩展
}

# ============================================================
# 价格数据获取（通过curl绕过Python SSL问题）
# ============================================================

def fetch_prices_curl(ticker, days=120):
    """用curl获取Yahoo Finance日线数据"""
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
# 基本面数据管理
# ============================================================

def load_fundamentals():
    """加载基本面数据"""
    if os.path.exists(FUND_FILE):
        with open(FUND_FILE) as f:
            return json.load(f)
    return {}


def save_fundamentals(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(FUND_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def update_fundamental_interactive(ticker):
    """交互式更新基本面数据"""
    funds = load_fundamentals()
    if ticker not in funds:
        funds[ticker] = {"quarters": {}}
    print(f"\n  更新 {ticker} 基本面数据")
    print(f"  已有季度：{', '.join(funds[ticker]['quarters'].keys()) or '无'}")
    date = input("  财报发布日 (YYYY-MM-DD): ").strip()
    label = input("  标签 (如 Q1 2024): ").strip()
    rev_yoy = float(input("  营收同比增速 (%): "))
    gm = float(input("  毛利率 (%): "))
    eps_beat = float(input("  EPS超预期 (%): "))

    funds[ticker]["quarters"][date] = {
        "label": label, "rev_yoy": rev_yoy, "gm": gm, "eps_beat": eps_beat
    }
    save_fundamentals(funds)
    print(f"  ✅ 已保存 {ticker} {label}")


# ============================================================
# 第一层：动量发现
# ============================================================

def check_momentum(prices):
    """检查最近交易日是否触发动量信号"""
    if len(prices) < 61:
        return None

    latest = prices[-1]
    close = latest["close"]

    # 60日新高
    past_60_highs = [p["high"] for p in prices[-61:-1]]
    is_60d_high = close > max(past_60_highs)

    # 放量：近5日均量 > 20日均量 × 1.5
    vol_5 = sum(p["volume"] for p in prices[-5:]) / 5
    vol_20 = sum(p["volume"] for p in prices[-20:]) / 20
    vol_ratio = vol_5 / vol_20 if vol_20 > 0 else 0
    is_volume = vol_ratio > 1.5

    # 30日涨幅
    close_30d = prices[-31]["close"] if len(prices) > 30 else prices[0]["close"]
    pct_30d = (close - close_30d) / close_30d * 100

    # 近5日有突破日（不一定是今天）
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
# 第二层：价值验证（6维，含回测改进）
# ============================================================

def check_value(ticker, signal_date=None):
    """6维价值验证"""
    funds = load_fundamentals()
    if ticker not in funds or not funds[ticker].get("quarters"):
        return None

    quarters = funds[ticker]["quarters"]
    sorted_q = sorted(quarters.items(), key=lambda x: x[0])

    # 找最近两个季度
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

    # 1. 营收加速（同比增速在改善）
    if pd:
        checks["营收加速"] = d["rev_yoy"] > pd["rev_yoy"]
    else:
        checks["营收加速"] = d["rev_yoy"] > 20

    # 2. 毛利率方向
    if pd:
        checks["毛利率扩张"] = d["gm"] > pd["gm"] or d["gm"] > 55
    else:
        checks["毛利率扩张"] = d["gm"] > 45

    # 3. EPS超预期 > 10%
    checks["盈利惊喜"] = d["eps_beat"] > 10

    # 4. 营收高增长 > 15%
    checks["营收高增长"] = d["rev_yoy"] > 15

    # 5. 毛利率健康 > 40%
    checks["毛利率健康"] = d["gm"] > 40

    # 6. ★改进：毛利率连续2季改善（解决NVDA 2023-01漏判）
    if pd and pd2:
        checks["毛利连续改善"] = d["gm"] > pd["gm"] > pd2["gm"]
    elif pd:
        checks["毛利连续改善"] = d["gm"] > pd["gm"]
    else:
        checks["毛利连续改善"] = False

    score = sum(1 for v in checks.values() if v)

    # ★改进：独立通过条件
    independent_pass = False
    independent_reason = ""

    # 条件A：毛利率连续2季改善 + 毛利>45%（NVDA 2023-01场景）
    if checks.get("毛利连续改善") and d["gm"] > 45:
        independent_pass = True
        independent_reason = "毛利率连续改善+>45%"

    # 条件B：EPS超预期>30%（MU底部场景）
    if d["eps_beat"] > 30:
        independent_pass = True
        independent_reason = "EPS超预期>30%（周期股信号）"

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
# 信号分级
# ============================================================

def grade_signal(momentum, value):
    """综合评级"""
    if not momentum or not momentum["triggered"]:
        return "SKIP", "无动量信号", ""

    if not value:
        return "WATCH", "动量触发但无基本面数据", "补充基本面"

    score = value["score"]
    ind = value["independent_pass"]

    if score >= 5 or (score >= 4 and ind):
        return "BUY_8%", f"确信仓（{score}/6）", "建议8%仓位"
    elif score >= 4 or (score >= 3 and ind):
        return "BUY_5%", f"标准仓（{score}/6）", "建议5%仓位"
    elif score >= 3:
        return "BUY_3%", f"试探仓（{score}/6）", "建议3%仓位"
    elif ind:
        return "BUY_3%", f"独立条件通过：{value['independent_reason']}", "建议3%仓位"
    else:
        return "PASS", f"动量有但基本面不足（{score}/6）", "继续观察"


# ============================================================
# 扫描一个标的
# ============================================================

def scan_ticker(ticker, verbose=True):
    """扫描单个标的"""
    prices = fetch_prices_curl(ticker)
    if not prices:
        if verbose:
            print(f"  {ticker:<8} ⚠️  无法获取价格数据")
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
        # 紧凑输出
        m = momentum
        symbol = {"BUY_8%": "🔴", "BUY_5%": "🟡", "BUY_3%": "🟢", "WATCH": "👀", "PASS": "⬜", "SKIP": "  "}
        s = symbol.get(grade, "  ")

        if grade.startswith("BUY"):
            print(f"  {s} {ticker:<8} ${m['close']:<8} 30日+{m['pct_30d']}% 放量{m['vol_ratio']}x  → {grade} {reason}")
            if value:
                v = value
                checks_str = " ".join(f"{'✅' if val else '❌'}{k}" for k, val in v["checks"].items())
                print(f"     基本面({v['fund_label']}): 营收{v['fund']['rev_yoy']}% 毛利{v['fund']['gm']}% EPS超{v['fund']['eps_beat']}%")
                print(f"     {checks_str}")
                if v["independent_pass"]:
                    print(f"     ★独立通过：{v['independent_reason']}")
        elif grade == "WATCH":
            print(f"  {s} {ticker:<8} ${m['close']:<8} 30日+{m['pct_30d']}%  → 动量触发！需补充基本面数据")
        elif grade == "PASS":
            print(f"  {s} {ticker:<8} ${m['close']:<8}  → {reason}")
        # SKIP不输出

    return result


# ============================================================
# 主程序
# ============================================================

def main():
    args = sys.argv[1:]

    # 更新模式
    if args and args[0] == "--update":
        ticker = args[1] if len(args) > 1 else input("  标的代码: ").strip().upper()
        update_fundamental_interactive(ticker)
        return

    # 初始化默认watchlist
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(WATCHLIST_FILE):
        with open(WATCHLIST_FILE, "w") as f:
            json.dump(DEFAULT_WATCHLIST, f, indent=2)
        print(f"  已创建默认watchlist: {WATCHLIST_FILE}")

    # 确定扫描范围
    if args:
        tickers = [t.upper() for t in args]
    else:
        with open(WATCHLIST_FILE) as f:
            wl = json.load(f)
        tickers = []
        for group, syms in wl.items():
            tickers.extend(syms)

    # 执行扫描
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n{'='*70}")
    print(f"  动量发现 + 价值验证 选股筛  {today}")
    print(f"  扫描范围：{len(tickers)} 个标的")
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

    # 汇总
    print(f"\n{'='*70}")
    print(f"  📋 扫描结果汇总")
    print(f"{'='*70}")

    if buy_signals:
        print(f"\n  🎯 买入信号：{len(buy_signals)} 个")
        for s in sorted(buy_signals, key=lambda x: x["grade"], reverse=True):
            m = s["momentum"]
            print(f"     {s['grade']:<8} {s['ticker']:<8} ${m['close']:<8} {s['reason']}")
    else:
        print(f"\n  无买入信号")

    if watch_signals:
        print(f"\n  👀 观察（需补基本面）：{len(watch_signals)} 个")
        for s in watch_signals:
            m = s["momentum"]
            print(f"     {s['ticker']:<8} ${m['close']:<8} 30日+{m['pct_30d']}% — 请用 --update {s['ticker']} 补充")

    print(f"\n  基本面数据文件：{FUND_FILE}")
    print(f"  Watchlist文件：{WATCHLIST_FILE}")
    print(f"  用 --update TICKER 补充/更新基本面\n")


if __name__ == "__main__":
    main()
