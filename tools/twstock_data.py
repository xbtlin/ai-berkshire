#!/usr/bin/env python3
"""台股数据工具 — FinMind 开放数据 API，零外部依赖（仅 stdlib）。

为 Claude Code Skills 提供台股行情、估值、财务、月营收等数据。
设计原则：独立模块，不影响现有工具；与 ashare_data.py 同风格。

数据源：FinMind (api.finmindtrade.com)，覆盖上市(twse)/上柜(tpex)全部股票。
未注册可直接使用（有小时级请求限额）。注册后的 API token 可提升额度，
按以下优先级读取（token 只存本机，严禁提交到 git）：
    1. 环境变量 FINMIND_TOKEN
    2. 本地文件 local/finmind_token.txt（local/ 目录已被 .gitignore 永久排除）

用法（由 Skills 自动调用）：
    python3 tools/twstock_data.py quote 2330        # 最新行情 + 估值 + 市值验算
    python3 tools/twstock_data.py valuation 2330    # PER/PBR/殖利率 + 52周高低
    python3 tools/twstock_data.py financials 2330   # 近5年年度核心财务 + 最新季度
    python3 tools/twstock_data.py revenue 2330      # 近13个月月营收及同比（台股独有月度披露）
    python3 tools/twstock_data.py dividend 2330     # 近年股利政策
    python3 tools/twstock_data.py search 台積        # 搜索股票代码（支持繁体/代码）

注意：
    - 所有金额单位为新台币（TWD）
    - FinMind 损益表为单季值，本工具已自动加总为年度值
    - 需要 Python >= 3.8，零外部依赖
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import date, timedelta

_API = "https://api.finmindtrade.com/api/v4/data"
_TIMEOUT = 30
_TOKEN_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "local", "finmind_token.txt",
)


def _token():
    """读取 FinMind token：环境变量优先，其次本地文件；都没有则匿名访问。"""
    t = os.environ.get("FINMIND_TOKEN", "").strip()
    if t:
        return t
    try:
        with open(_TOKEN_FILE, encoding="utf-8") as f:
            return f.read().strip() or None
    except OSError:
        return None


def _get(dataset, data_id=None, start_date=None, end_date=None):
    """请求 FinMind API，返回 data 列表。"""
    params = {"dataset": dataset}
    if data_id:
        params["data_id"] = data_id
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    token = _token()
    if token:
        params["token"] = token
    url = f"{_API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code in (400, 401, 402, 403) and token:
            raise ConnectionError(
                f"FinMind 拒绝请求（HTTP {e.code}），大概率是 token 无效或过期。"
                "请检查环境变量 FINMIND_TOKEN 或 local/finmind_token.txt 的内容；"
                "删除 token 可退回匿名访问（有小时级限额）"
            ) from e
        raise ConnectionError(f"FinMind 请求失败: HTTP {e.code} ({dataset})") from e
    except urllib.error.URLError as e:
        raise ConnectionError(f"FinMind 网络请求失败: {e.reason}") from e
    if payload.get("status") != 200:
        raise ConnectionError(f"FinMind 请求失败: {payload.get('msg')} ({dataset})")
    return payload.get("data", [])


def _fmt_yi(value):
    """新台币金额格式化为 亿/万。"""
    if value is None or value == "":
        return "-"
    try:
        v = float(value)
    except (ValueError, TypeError):
        return str(value)
    if abs(v) >= 1e8:
        return f"{v / 1e8:,.1f}亿"
    if abs(v) >= 1e4:
        return f"{v / 1e4:,.1f}万"
    return f"{v:,.2f}"


def _days_ago(n):
    return (date.today() - timedelta(days=n)).isoformat()


def _stock_name(stock_id):
    """从 TaiwanStockInfo 取股票名称与板块。"""
    try:
        rows = _get("TaiwanStockInfo", data_id=stock_id)
    except Exception:
        return stock_id, ""
    if not rows:
        return stock_id, ""
    board = {"twse": "上市", "tpex": "上柜"}.get(rows[0].get("type", ""), "")
    return rows[0].get("stock_name", stock_id), board


def _latest_shares(stock_id):
    """从 TaiwanStockShareholding 取最新发行股数。"""
    rows = _get("TaiwanStockShareholding", data_id=stock_id, start_date=_days_ago(14))
    if not rows:
        return None
    return rows[-1].get("NumberOfSharesIssued")


# ---------------------------------------------------------------------------
# 命令实现
# ---------------------------------------------------------------------------

def cmd_quote(stock_id):
    """最新行情快照 + 市值验算。"""
    name, board = _stock_name(stock_id)
    prices = _get("TaiwanStockPrice", data_id=stock_id, start_date=_days_ago(14))
    if not prices:
        print(f"❌ 未找到股票 {stock_id} 的行情数据")
        return
    p = prices[-1]
    prev_close = prices[-2]["close"] if len(prices) >= 2 else None

    pers = _get("TaiwanStockPER", data_id=stock_id, start_date=_days_ago(14))
    per = pers[-1] if pers else {}

    print("=" * 60)
    print(f"台股行情: {name} ({stock_id}) [{board}]  数据源: FinMind")
    print("=" * 60)
    print(f"  日期:       {p['date']}")
    print(f"  收盘价:     {p['close']} 新台币")
    if prev_close:
        chg = p["close"] - prev_close
        print(f"  涨跌:       {chg:+.2f} ({chg / prev_close * 100:+.2f}%)")
    print(f"  开/高/低:   {p['open']} / {p['max']} / {p['min']}")
    print(f"  成交量:     {_fmt_yi(p['Trading_Volume'])}股")
    print(f"  成交额:     {_fmt_yi(p['Trading_money'])}新台币")
    if per:
        print(f"  PER:        {per.get('PER', '-')}")
        print(f"  PBR:        {per.get('PBR', '-')}")
        print(f"  殖利率:     {per.get('dividend_yield', '-')}%")

    # 市值验算：收盘价 × 发行股数
    try:
        shares = _latest_shares(stock_id)
        if shares:
            cap = p["close"] * shares
            print(f"\n  发行股数:   {_fmt_yi(shares)}股")
            print(f"  总市值:     {_fmt_yi(cap)}新台币（= 收盘 {p['close']} × 股数，手算口径）")
    except Exception:
        print("\n  ⚠️ 发行股数获取失败，市值请另行验算")


def cmd_valuation(stock_id):
    """估值指标 + 52周高低。"""
    name, board = _stock_name(stock_id)
    prices = _get("TaiwanStockPrice", data_id=stock_id, start_date=_days_ago(370))
    if not prices:
        print(f"❌ 未找到股票 {stock_id} 的行情数据")
        return
    p = prices[-1]
    high_52w = max(r["max"] for r in prices)
    low_52w = min(r["min"] for r in prices)

    pers = _get("TaiwanStockPER", data_id=stock_id, start_date=_days_ago(370))
    per = pers[-1] if pers else {}
    per_vals = [r["PER"] for r in pers if r.get("PER")]

    print("=" * 60)
    print(f"估值指标: {name} ({stock_id}) [{board}]  数据源: FinMind")
    print("=" * 60)
    print(f"  日期:       {p['date']}")
    print(f"  收盘价:     {p['close']} 新台币")
    print(f"  PER:        {per.get('PER', '-')}")
    if per_vals:
        print(f"  PER一年区间: {min(per_vals)} ~ {max(per_vals)}")
    print(f"  PBR:        {per.get('PBR', '-')}")
    print(f"  殖利率:     {per.get('dividend_yield', '-')}%")
    print(f"  52周最高:   {high_52w}")
    print(f"  52周最低:   {low_52w}")

    try:
        shares = _latest_shares(stock_id)
        if shares:
            cap = p["close"] * shares
            print(f"  发行股数:   {_fmt_yi(shares)}股")
            print(f"  总市值:     {_fmt_yi(cap)}新台币")
    except Exception:
        pass


_IS_KEYS = {
    "Revenue": "营收",
    "GrossProfit": "毛利",
    "OperatingIncome": "营业利益",
    "EquityAttributableToOwnersOfParent": "归母净利",
    "EPS": "EPS",
}


def cmd_financials(stock_id):
    """近5年年度核心财务（单季加总）+ 年末权益推算 ROE。"""
    name, board = _stock_name(stock_id)
    start = f"{date.today().year - 5}-01-01"
    rows = _get("TaiwanStockFinancialStatements", data_id=stock_id, start_date=start)
    if not rows:
        print(f"❌ 未找到股票 {stock_id} 的财务数据")
        return

    # 按年份聚合单季值：{year: {指标: 累计值}}，并记录季度数
    years = {}
    for r in rows:
        if r["type"] not in _IS_KEYS:
            continue
        y = r["date"][:4]
        d = years.setdefault(y, {"_quarters": set()})
        d["_quarters"].add(r["date"])
        d[r["type"]] = d.get(r["type"], 0) + (r["value"] or 0)

    # 年末归母权益（Q4 资产负债表），用于简化 ROE
    equity_by_year = {}
    try:
        bs = _get("TaiwanStockBalanceSheet", data_id=stock_id, start_date=start)
        for r in bs:
            if r["type"] == "EquityAttributableToOwnersOfParent" and r["date"][5:7] == "12":
                equity_by_year[r["date"][:4]] = r["value"]
    except Exception:
        pass

    print("=" * 60)
    print(f"核心财务数据: {name} ({stock_id}) [{board}]  数据源: FinMind")
    print("=" * 60)
    print("  单位：新台币。FinMind 损益表为单季值，以下为年度加总。")

    for y in sorted(years, reverse=True):
        d = years[y]
        nq = len(d["_quarters"])
        suffix = "" if nq == 4 else f"（仅前{nq}季累计，非全年）"
        rev = d.get("Revenue")
        gp = d.get("GrossProfit")
        op = d.get("OperatingIncome")
        ni = d.get("EquityAttributableToOwnersOfParent")
        eps = d.get("EPS")
        print(f"\n  --- {y}年 {suffix} ---")
        if rev:
            print(f"  营收:       {_fmt_yi(rev)}")
        if gp and rev:
            print(f"  毛利率:     {gp / rev * 100:.1f}%")
        if op and rev:
            print(f"  营业利益率: {op / rev * 100:.1f}%")
        if ni:
            print(f"  归母净利:   {_fmt_yi(ni)}")
        if ni and rev:
            print(f"  净利率:     {ni / rev * 100:.1f}%")
        if eps:
            print(f"  EPS:        {eps:.2f}")
        eq = equity_by_year.get(y)
        if eq and ni and nq == 4:
            print(f"  ROE(简化):  {ni / eq * 100:.1f}%（归母净利/年末归母权益，非期初期末平均）")


def cmd_revenue(stock_id):
    """近13个月月营收及同比——台股独有的月度披露，跟踪基本面拐点。"""
    name, board = _stock_name(stock_id)
    rows = _get("TaiwanStockMonthRevenue", data_id=stock_id, start_date=_days_ago(800))
    if not rows:
        print(f"❌ 未找到股票 {stock_id} 的月营收数据")
        return

    by_month = {(r["revenue_year"], r["revenue_month"]): r["revenue"] for r in rows}

    print("=" * 60)
    print(f"月营收: {name} ({stock_id}) [{board}]  数据源: FinMind")
    print("=" * 60)
    print("  单位：新台币（台股每月10日前强制披露上月营收）")
    print(f"\n  {'月份':<10}{'营收':>14}{'同比':>10}")

    keys = sorted(by_month)[-13:]
    for y, m in keys:
        rev = by_month[(y, m)]
        prev = by_month.get((y - 1, m))
        yoy = f"{(rev / prev - 1) * 100:+.1f}%" if prev else "-"
        print(f"  {y}-{m:02d}   {_fmt_yi(rev):>14}{yoy:>10}")


def cmd_dividend(stock_id):
    """近年股利政策。"""
    name, board = _stock_name(stock_id)
    start = f"{date.today().year - 5}-01-01"
    rows = _get("TaiwanStockDividend", data_id=stock_id, start_date=start)
    if not rows:
        print(f"❌ 未找到股票 {stock_id} 的股利数据")
        return

    print("=" * 60)
    print(f"股利政策: {name} ({stock_id}) [{board}]  数据源: FinMind")
    print("=" * 60)
    print("  单位：新台币/股（台股常见按季配息，年度股利需自行加总）")
    print(f"\n  {'所属期间':<12}{'现金股利':>8}{'股票股利':>8}  {'除息日':<12}{'发放日':<12}")

    for r in rows:
        cash = (r.get("CashEarningsDistribution") or 0) + (r.get("CashStatutorySurplus") or 0)
        stock = (r.get("StockEarningsDistribution") or 0) + (r.get("StockStatutorySurplus") or 0)
        if not cash and not stock:
            continue
        ex_date = r.get("CashExDividendTradingDate") or "-"
        pay_date = r.get("CashDividendPaymentDate") or "-"
        print(f"  {r.get('year', ''):<12}{cash:>8.2f}{stock:>8.2f}  {ex_date:<12}{pay_date:<12}")


def cmd_search(keyword):
    """按名称/代码搜索台股（TaiwanStockInfo 全表过滤）。"""
    rows = _get("TaiwanStockInfo")
    seen = {}
    for r in rows:
        if keyword in r.get("stock_name", "") or keyword == r.get("stock_id", ""):
            sid = r["stock_id"]
            if sid not in seen:
                seen[sid] = {
                    "name": r["stock_name"],
                    "type": r.get("type", ""),
                    "industries": [],
                }
            cat = r.get("industry_category", "")
            if cat and cat not in seen[sid]["industries"]:
                seen[sid]["industries"].append(cat)

    if not seen:
        print(f"❌ 未找到匹配 '{keyword}' 的台股（提示：台股名称多为繁体，如 台積電）")
        return

    print("=" * 60)
    print(f"台股搜索结果: '{keyword}'  数据源: FinMind")
    print("=" * 60)
    for sid, d in sorted(seen.items()):
        board = {"twse": "上市", "tpex": "上柜"}.get(d["type"], d["type"])
        cats = "/".join(d["industries"][:3])
        print(f"  {sid} {d['name']} [{board}] {cats}")


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="台股数据工具 — FinMind 开放数据 API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command")

    for cmd, help_text in [
        ("quote", "最新行情 + 市值验算"),
        ("valuation", "估值指标（PER/PBR/殖利率/52周高低）"),
        ("financials", "近5年年度核心财务"),
        ("revenue", "近13个月月营收及同比"),
        ("dividend", "近年股利政策"),
    ]:
        p = sub.add_parser(cmd, help=help_text)
        p.add_argument("stock_id", help="股票代码，如 2330")

    p_search = sub.add_parser("search", help="搜索股票代码")
    p_search.add_argument("keyword", help="公司名（繁体）或代码")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "search":
            cmd_search(args.keyword)
        else:
            {
                "quote": cmd_quote,
                "valuation": cmd_valuation,
                "financials": cmd_financials,
                "revenue": cmd_revenue,
                "dividend": cmd_dividend,
            }[args.command](args.stock_id)
    except BrokenPipeError:
        # 输出被管道截断（如 | head），静默退出。
        # 注意 BrokenPipeError 是 ConnectionError 的子类，必须放在前面
        sys.stderr.close()
        sys.exit(0)
    except ConnectionError as e:
        print(f"❌ {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
