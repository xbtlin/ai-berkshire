#!/usr/bin/env python3
"""宏观背景数据工具 — FXMacroData API，零外部依赖（仅 stdlib）。

为 Claude Code Skills 提供公司所在国的宏观背景：政策利率、通胀、GDP、失业率、
未来的数据发布日程，以及汇率。估值研究里常见的几个问题——贴现率参照的利率处于
什么位置、通胀是否在侵蚀定价权、本币一年来升值还是贬值——都可以先用它看一眼。

数据源：FXMacroData (api.fxmacrodata.com)，数值来自各国央行/统计局官方发布，
覆盖 USD、EUR、GBP、JPY、CNY、AUD、CAD、CHF、KRW、TWD、BRL 等 22 种货币。
USD 数据无需注册即可访问（15 分钟延迟，近 90 天历史）；其他货币和汇率需要 API key，
按以下优先级读取（key 只存本机，严禁提交到 git）：
    1. 环境变量 FXMACRODATA_API_KEY
    2. 本地文件 local/fxmacrodata_key.txt（local/ 目录已被 .gitignore 永久排除）

用法（由 Skills 自动调用）：
    python3 tools/macro_data.py snapshot USD          # 政策利率/通胀/GDP/失业率最新值 + 未来30天发布日程
    python3 tools/macro_data.py indicator JPY inflation  # 单个指标近12期（可加 --n 24）
    python3 tools/macro_data.py calendar EUR          # 未来30天数据发布日程（可加 --days 60）
    python3 tools/macro_data.py fx USD JPY            # 最新汇率 + 一年前汇率及变动
    python3 tools/macro_data.py catalogue CNY         # 该货币可用的指标代码、单位、频率

注意：
    - 指标单位以 catalogue 为准（例如 gdp 各国口径不同：有的是水平值，有的是季环比）
    - 发布日程中的时间是官方计划发布时间（UTC），time_announced=false 的只有日期
    - 需要 Python >= 3.8，零外部依赖
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone

_API = "https://api.fxmacrodata.com/v1"
_TIMEOUT = 30
_KEY_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "local", "fxmacrodata_key.txt",
)
_SUBSCRIBE = "https://fxmacrodata.com/subscribe"

# snapshot 默认展示的核心指标（按 catalogue 实际可用的过滤）
_CORE = [
    ("policy_rate", "政策利率"),
    ("inflation", "通胀(CPI)"),
    ("core_inflation", "核心通胀"),
    ("gdp", "GDP"),
    ("unemployment", "失业率"),
]


def _api_key():
    """读取 API key：环境变量优先，其次本地文件；都没有则匿名访问（仅 USD）。"""
    k = os.environ.get("FXMACRODATA_API_KEY", "").strip()
    if k:
        return k
    try:
        with open(_KEY_FILE, encoding="utf-8") as f:
            return f.read().strip() or None
    except OSError:
        return None


def _get(path, **params):
    """请求 FXMacroData API，返回 JSON；指标不存在（404）返回 None。

    key 放在 X-API-Key 请求头里，不进 URL。
    """
    params = {k: v for k, v in params.items() if v is not None}
    url = f"{_API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {"User-Agent": "ai-berkshire-macro-data", "Accept": "application/json"}
    key = (_api_key() or "").strip()
    if any(ch.isspace() or not ch.isprintable() for ch in key):
        raise ValueError("FXMacroData API key contains whitespace or control characters")
    req = urllib.request.Request(url, headers=headers)
    if key:
        req.add_unredirected_header("X-API-Key", key)
    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        if e.code in (401, 402, 403):
            hint = (
                "key 无效或未开通该数据，请检查环境变量 FXMACRODATA_API_KEY 或 local/fxmacrodata_key.txt"
                if key else
                f"未配置 API key 时只能访问 USD 数据；其他货币和汇率需要 key（{_SUBSCRIBE}）"
            )
            raise ConnectionError(f"FXMacroData 拒绝请求（HTTP {e.code}）：{hint}") from None
        raise ConnectionError(f"FXMacroData 请求失败: HTTP {e.code} ({path})") from None
    except urllib.error.URLError:
        raise ConnectionError("FXMacroData 网络请求失败") from None
    except (ValueError, UnicodeError):
        raise ValueError("FXMacroData returned invalid JSON") from None
    if not isinstance(payload, dict) or "detail" in payload or "error" in payload:
        raise ValueError("FXMacroData returned an error or invalid response")
    return payload


def _series(currency, indicator, n=2):
    """取指标最近 n 期（API 按最新在前返回）。"""
    payload = _get(f"/announcements/{currency.lower()}/{indicator}", limit=n)
    if not payload:
        return []
    return payload.get("data") or []


def _catalogue(currency):
    return _get(f"/data_catalogue/{currency.lower()}") or {}


def _fmt(v):
    if v is None:
        return "-"
    return f"{v:,.4f}".rstrip("0").rstrip(".") if abs(v) < 1000 else f"{v:,.1f}"


def _fmt_time(row):
    """计划发布时间：有确切时间的显示 UTC 时刻，只公布日期的只显示日期。"""
    if row.get("time_announced") is False:
        return f"{row.get('announcement_date', '-')} (时间未公布)"
    ts = row.get("announcement_datetime")
    if ts is None:
        return "-"
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _days_ago(n):
    return (date.today() - timedelta(days=n)).isoformat()


# ---------------------------------------------------------------------------
# 命令实现
# ---------------------------------------------------------------------------

def cmd_snapshot(currency, days=30):
    """核心宏观指标最新值 + 上期值 + 未来发布日程。"""
    cur = currency.upper()
    cat = _catalogue(cur)
    core = [(s, label) for s, label in _CORE if not cat or s in cat]

    print("=" * 60)
    print(f"宏观背景: {cur}  数据源: FXMacroData（央行/统计局官方数据）")
    print("=" * 60)
    print(f"  {'指标':<10}{'最新':>12}{'上期':>12}  {'数据期':<12}单位")
    for slug, label in core:
        rows = _series(cur, slug, n=2)
        if not rows:
            continue
        latest = rows[0]
        prev = rows[1].get("val") if len(rows) > 1 else latest.get("previous_value")
        unit = (cat.get(slug) or {}).get("unit", "")
        print(f"  {label:<10}{_fmt(latest.get('val')):>12}{_fmt(prev):>12}  {latest.get('date', '-'):<12}{unit}")

    print(f"\n  未来{days}天数据发布日程:")
    _print_calendar(cur, days, limit=10)


def cmd_indicator(currency, indicator, n=12):
    """单个指标近 n 期。"""
    cur = currency.upper()
    rows = _series(cur, indicator, n=n)
    if not rows:
        print(f"未找到 {cur} 的指标 {indicator}（可用代码见 catalogue 子命令）")
        return
    unit = (_catalogue(cur).get(indicator) or {}).get("unit", "")
    print("=" * 60)
    print(f"{cur} {indicator}  单位: {unit or '-'}  数据源: FXMacroData")
    print("=" * 60)
    print(f"  {'数据期':<12}{'数值':>12}  官方来源")
    for r in rows:
        print(f"  {r.get('date', '-'):<12}{_fmt(r.get('val')):>12}  {r.get('source') or '-'}")


def _print_calendar(cur, days, limit=None):
    payload = _get(
        f"/calendar/{cur.lower()}",
        start_date=date.today().isoformat(),
        end_date=(date.today() + timedelta(days=days)).isoformat(),
    ) or {}
    rows = payload.get("data") or []
    if not rows:
        print("    （该区间无已公布的发布日程）")
        return
    for r in rows[:limit]:
        name = r.get("name") or r.get("release", "-")
        print(f"    {_fmt_time(r):<28}{r.get('release', '-'):<26} {name}")


def cmd_calendar(currency, days=30):
    cur = currency.upper()
    print("=" * 60)
    print(f"{cur} 未来{days}天数据发布日程（官方计划时间）  数据源: FXMacroData")
    print("=" * 60)
    _print_calendar(cur, days)


def cmd_fx(base, quote):
    """最新汇率 + 一年前汇率，用于判断本币升贬值和跨市场换算。"""
    base, quote = base.upper(), quote.upper()
    path = f"/forex/{base.lower()}/{quote.lower()}"
    latest = (_get(path, limit=1) or {}).get("data") or []
    if not latest:
        print(f"未找到 {base}/{quote} 的汇率数据")
        return
    year_ago = (_get(
        path, start_date=_days_ago(372), end_date=_days_ago(365), limit=1,
    ) or {}).get("data") or []

    now = latest[0]
    print("=" * 60)
    print(f"汇率: {base}/{quote}（1 {base} = ? {quote}）  数据源: FXMacroData")
    print("=" * 60)
    print(f"  日期:       {now.get('date')}")
    print(f"  汇率:       {_fmt(now.get('val'))}")
    if year_ago and year_ago[0].get("val") and now.get("val"):
        old = year_ago[0]
        chg = (now["val"] / old["val"] - 1) * 100
        print(f"  一年前:     {_fmt(old['val'])}（{old.get('date')}）")
        print(f"  一年变动:   {chg:+.2f}%（正数 = {base} 相对 {quote} 升值）")


def cmd_catalogue(currency):
    cur = currency.upper()
    cat = _catalogue(cur)
    if not cat:
        print(f"未找到 {cur} 的指标目录")
        return
    print("=" * 60)
    print(f"{cur} 可用指标  数据源: FXMacroData")
    print("=" * 60)
    for slug, meta in sorted(cat.items()):
        if not isinstance(meta, dict):
            continue
        print(f"  {slug:<28}{meta.get('frequency', ''):<11}{meta.get('unit', '')}  {meta.get('name', '')}")


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="宏观背景数据工具 — FXMacroData API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("snapshot", help="核心宏观指标 + 未来发布日程")
    p.add_argument("currency", help="货币代码，如 USD/CNY/JPY")
    p.add_argument("--days", type=int, default=30)

    p = sub.add_parser("indicator", help="单个指标近N期")
    p.add_argument("currency")
    p.add_argument("indicator", help="指标代码，如 inflation/policy_rate/gdp")
    p.add_argument("--n", type=int, default=12)

    p = sub.add_parser("calendar", help="数据发布日程")
    p.add_argument("currency")
    p.add_argument("--days", type=int, default=30)

    p = sub.add_parser("fx", help="汇率及一年变动")
    p.add_argument("base", help="基础货币，如 USD")
    p.add_argument("quote", help="报价货币，如 JPY")

    p = sub.add_parser("catalogue", help="可用指标目录")
    p.add_argument("currency")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "snapshot":
            cmd_snapshot(args.currency, args.days)
        elif args.command == "indicator":
            cmd_indicator(args.currency, args.indicator, args.n)
        elif args.command == "calendar":
            cmd_calendar(args.currency, args.days)
        elif args.command == "fx":
            cmd_fx(args.base, args.quote)
        else:
            cmd_catalogue(args.currency)
    except BrokenPipeError:
        # 输出被管道截断（如 | head），静默退出。
        # 注意 BrokenPipeError 是 ConnectionError 的子类，必须放在前面
        sys.stderr.close()
        sys.exit(0)
    except ConnectionError as e:
        print(f"错误: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
