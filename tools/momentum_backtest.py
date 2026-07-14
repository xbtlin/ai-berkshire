#!/usr/bin/env python3
"""
动量发现 + 价值验证 回测工具
回测标的：NVDA / AMD / MU（AI芯片三巨头）
时间范围：2022-01 ~ 2025-12
核心问题：这个框架能否在AI浪潮早期捕捉到这些股票？
"""

import json
import sys
from datetime import datetime, timedelta
from urllib.request import urlopen, Request
from collections import OrderedDict

# ============================================================
# 第一部分：获取历史价格数据（Yahoo Finance Chart API）
# ============================================================

def fetch_price_data(ticker, start_date="2021-06-01", end_date="2025-12-31"):
    """通过Yahoo Finance API获取日线数据"""
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
        print(f"  [WARN] 无法获取 {ticker} 价格数据: {e}")
        return None


# ============================================================
# 第二部分：手工输入关键季度基本面数据
# （API获取季度财务数据不可靠，核心数据手工录入更准确）
# ============================================================

FUNDAMENTALS = {
    "NVDA": {
        "name": "英伟达",
        "quarters": OrderedDict([
            # (财报发布日, {营收亿美元, 营收同比增速, 毛利率, EPS, EPS超预期%})
            # FY2023 = calendar 2022
            ("2022-05-25", {"rev": 82.9, "rev_yoy": 46.0, "gm": 65.5, "eps": 1.36, "eps_beat": 4.6, "label": "FY23Q1 (Apr22)"}),
            ("2022-08-24", {"rev": 67.0, "rev_yoy": -4.0, "gm": 43.5, "eps": 0.51, "eps_beat": -24.0, "label": "FY23Q2 (Jul22)"}),
            ("2022-11-16", {"rev": 59.3, "rev_yoy": -17.0, "gm": 53.6, "eps": 0.58, "eps_beat": 7.4, "label": "FY23Q3 (Oct22)"}),
            ("2023-02-22", {"rev": 60.5, "rev_yoy": -21.0, "gm": 63.3, "eps": 0.88, "eps_beat": 10.0, "label": "FY23Q4 (Jan23)"}),
            # FY2024 = calendar 2023 — AI爆发
            ("2023-05-24", {"rev": 71.9, "rev_yoy": -13.0, "gm": 64.6, "eps": 1.09, "eps_beat": 18.5, "label": "FY24Q1 (Apr23) ★ AI拐点"}),
            ("2023-08-23", {"rev": 135.1, "rev_yoy": 101.0, "gm": 70.1, "eps": 2.70, "eps_beat": 29.0, "label": "FY24Q2 (Jul23) ★★ 爆发"}),
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
            ("2024-01-30", {"rev": 61.7, "rev_yoy": 10.0, "gm": 47.0, "eps": 0.77, "eps_beat": 3.7, "label": "Q4 2023 ★ MI300发布"}),
            ("2024-04-30", {"rev": 54.7, "rev_yoy": 2.0, "gm": 47.0, "eps": 0.62, "eps_beat": 3.3, "label": "Q1 2024"}),
            ("2024-07-30", {"rev": 58.3, "rev_yoy": 9.0, "gm": 49.0, "eps": 0.69, "eps_beat": 1.5, "label": "Q2 2024"}),
            ("2024-10-29", {"rev": 68.2, "rev_yoy": 18.0, "gm": 50.0, "eps": 0.92, "eps_beat": 4.5, "label": "Q3 2024 ★ AI加速"}),
        ]),
    },
    "MU": {
        "name": "美光科技",
        "quarters": OrderedDict([
            ("2022-06-30", {"rev": 86.4, "rev_yoy": 16.0, "gm": 47.0, "eps": 2.59, "eps_beat": 4.0, "label": "FY22Q3 (May22)"}),
            ("2022-09-29", {"rev": 66.4, "rev_yoy": -20.0, "gm": 40.0, "eps": 1.45, "eps_beat": -5.0, "label": "FY22Q4 (Aug22)"}),
            ("2022-12-21", {"rev": 40.9, "rev_yoy": -47.0, "gm": 22.0, "eps": -0.04, "eps_beat": 22.0, "label": "FY23Q1 (Nov22)"}),
            ("2023-03-28", {"rev": 36.9, "rev_yoy": -53.0, "gm": 11.0, "eps": -1.91, "eps_beat": 5.0, "label": "FY23Q2 (Feb23)"}),
            ("2023-06-28", {"rev": 37.5, "rev_yoy": -57.0, "gm": -8.0, "eps": -1.43, "eps_beat": 15.0, "label": "FY23Q3 (May23)"}),
            ("2023-09-27", {"rev": 40.1, "rev_yoy": -40.0, "gm": -1.0, "eps": -1.07, "eps_beat": 18.0, "label": "FY23Q4 (Aug23) ★ HBM拐点"}),
            ("2023-12-20", {"rev": 47.3, "rev_yoy": 16.0, "gm": 20.0, "eps": -0.95, "eps_beat": 68.0, "label": "FY24Q1 (Nov23) ★★ 反转"}),
            ("2024-03-20", {"rev": 58.2, "rev_yoy": 58.0, "gm": 28.0, "eps": 0.42, "eps_beat": 82.0, "label": "FY24Q2 (Feb24) ★★★"}),
            ("2024-06-26", {"rev": 68.1, "rev_yoy": 82.0, "gm": 35.4, "eps": 0.62, "eps_beat": 6.9, "label": "FY24Q3 (May24)"}),
            ("2024-09-25", {"rev": 77.5, "rev_yoy": 93.0, "gm": 36.5, "eps": 1.18, "eps_beat": 5.4, "label": "FY24Q4 (Aug24)"}),
        ]),
    },
}


# ============================================================
# 第三部分：动量发现引擎（第一层筛选）
# ============================================================

def compute_momentum_signals(prices):
    """计算动量信号"""
    signals = []
    for i in range(60, len(prices)):
        row = prices[i]
        date = row["date"]
        close = row["close"]

        # 60日新高
        past_60_highs = [prices[j]["high"] for j in range(i - 60, i)]
        is_60d_high = close > max(past_60_highs)

        # 放量确认：近5日均量 > 20日均量的2倍
        vol_5 = sum(prices[j]["volume"] for j in range(i - 4, i + 1)) / 5
        vol_20 = sum(prices[j]["volume"] for j in range(i - 19, i + 1)) / 20
        is_volume_surge = vol_5 > vol_20 * 1.8  # 放宽到1.8倍

        # 30日涨幅
        close_30d_ago = prices[i - 30]["close"]
        pct_30d = (close - close_30d_ago) / close_30d_ago * 100

        # 综合判断
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
# 第四部分：价值验证引擎（第二层筛选）
# ============================================================

def find_latest_fundamental(ticker, signal_date):
    """找到信号日期之前最近的一个季度财报"""
    quarters = FUNDAMENTALS[ticker]["quarters"]
    latest = None
    latest_date = None
    for q_date, q_data in quarters.items():
        if q_date <= signal_date:
            latest = q_data
            latest_date = q_date
    return latest_date, latest


def verify_value(ticker, fund_data, prev_fund_data=None):
    """5维价值验证"""
    if not fund_data:
        return {"score": 0, "details": "无基本面数据"}

    checks = {}

    # 1. 营收加速（营收同比增速是否在改善）
    rev_yoy = fund_data.get("rev_yoy", 0)
    if prev_fund_data:
        prev_rev_yoy = prev_fund_data.get("rev_yoy", 0)
        rev_accelerating = rev_yoy > prev_rev_yoy
    else:
        rev_accelerating = rev_yoy > 20
    checks["营收加速"] = rev_accelerating

    # 2. 毛利率方向（>45%且不萎缩）
    gm = fund_data.get("gm", 0)
    if prev_fund_data:
        prev_gm = prev_fund_data.get("gm", 0)
        gm_expanding = gm > prev_gm or gm > 50
    else:
        gm_expanding = gm > 45
    checks["毛利率扩张"] = gm_expanding

    # 3. EPS超预期（>10%为强信号）
    eps_beat = fund_data.get("eps_beat", 0)
    checks["盈利惊喜"] = eps_beat > 10

    # 4. 营收增速本身（>15%）
    checks["营收高增长"] = rev_yoy > 15

    # 5. 毛利率绝对值（>40%，芯片行业标准）
    checks["毛利率健康"] = gm > 40

    score = sum(1 for v in checks.values() if v)
    return {"score": score, "max": 5, "details": checks, "fund": fund_data}


# ============================================================
# 第五部分：回测主逻辑
# ============================================================

def backtest_ticker(ticker):
    """对单个标的进行完整回测"""
    print(f"\n{'='*70}")
    print(f"  回测标的：{FUNDAMENTALS[ticker]['name']} ({ticker})")
    print(f"{'='*70}")

    # 获取价格数据
    print(f"\n  [1/3] 获取历史价格数据...")
    prices = fetch_price_data(ticker, "2021-06-01", "2025-06-30")
    if not prices:
        print("  ❌ 无法获取价格数据，跳过")
        return None

    print(f"  获取到 {len(prices)} 个交易日数据 ({prices[0]['date']} ~ {prices[-1]['date']})")

    # 计算动量信号
    print(f"\n  [2/3] 扫描动量信号...")
    momentum_signals = compute_momentum_signals(prices)
    print(f"  发现 {len(momentum_signals)} 个动量触发点")

    # 价值验证
    print(f"\n  [3/3] 对动量信号进行价值验证...")

    buy_signals = []
    seen_months = set()

    for sig in momentum_signals:
        month_key = sig["date"][:7]
        if month_key in seen_months:
            continue  # 同月只取第一个信号
        seen_months.add(month_key)

        # 找基本面数据
        q_date, fund = find_latest_fundamental(ticker, sig["date"])
        if not fund:
            continue

        # 找前一季度数据做对比
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

        # 买入信号：价值验证>=3/5
        if verification["score"] >= 3:
            result["action"] = "✅ 买入信号"
            buy_signals.append(result)
        else:
            result["action"] = "❌ 不通过"

    # 输出结果
    print(f"\n  {'—'*60}")
    print(f"  动量发现 + 价值验证结果：")
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

    # 只展示关键时间窗口的信号
    first_buy = None
    for bs in buy_signals:
        if bs["date"] >= "2022-06-01":
            if not first_buy:
                first_buy = bs
            print(f"\n  📅 {bs['date']} | 收盘价 ${bs['close']}")
            print(f"     动量：30日涨幅 {bs['pct_30d']}% | 放量倍数 {bs['vol_ratio']}x")
            print(f"     基本面（{bs['fund_label']}）：")
            print(f"       营收同比 {bs['rev_yoy']}% | 毛利率 {bs['gm']}% | EPS超预期 {bs['eps_beat']}%")
            print(f"     价值验证：{bs['value_score']}/{bs['value_max']} ", end="")
            for k, v in bs["details"].items():
                print(f"{'✅' if v else '❌'}{k} ", end="")
            print(f"\n     判断：{bs['action']}")

    # 计算假设收益
    if first_buy and prices:
        buy_price = first_buy["close"]
        buy_date = first_buy["date"]
        # 找1年后和2年后的价格
        for p in prices:
            if p["date"] >= buy_date:
                final_price = p["close"]
        final_date = prices[-1]["date"]
        total_return = (final_price - buy_price) / buy_price * 100

        print(f"\n  {'='*60}")
        print(f"  📊 假设在首次买入信号执行：")
        print(f"     买入日：{buy_date} @ ${buy_price}")
        print(f"     最终日：{final_date} @ ${round(final_price, 2)}")
        print(f"     总回报：{round(total_return, 1)}%")
        print(f"  {'='*60}")

    return {"ticker": ticker, "buy_signals": buy_signals, "first_buy": first_buy}


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  动量发现 + 价值验证 回测系统")
    print("  标的：NVDA / AMD / MU | 时间：2022-2025")
    print("=" * 70)

    results = {}
    for ticker in ["NVDA", "AMD", "MU"]:
        result = backtest_ticker(ticker)
        if result:
            results[ticker] = result

    # 总结
    print(f"\n\n{'='*70}")
    print(f"  📋 回测总结")
    print(f"{'='*70}")
    print(f"\n  {'标的':<8} {'首次买入信号':<16} {'买入价':<12} {'触发基本面'}")
    print(f"  {'—'*65}")
    for ticker, r in results.items():
        if r["first_buy"]:
            fb = r["first_buy"]
            print(f"  {ticker:<8} {fb['date']:<16} ${fb['close']:<10} {fb['fund_label']}")
        else:
            print(f"  {ticker:<8} {'无买入信号':<16}")

    print(f"\n  关键问题回答：")
    print(f"  ┌─────────────────────────────────────────────────────────────┐")
    print(f"  │ 这个框架能否在AI浪潮早期捕捉到NVDA/AMD/MU？              │")
    print(f"  │ 答案见上方详细分析。                                       │")
    print(f"  └─────────────────────────────────────────────────────────────┘")
