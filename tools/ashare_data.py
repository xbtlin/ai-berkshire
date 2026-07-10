#!/usr/bin/env python3
"""A\u80a1\u6570\u636e\u5de5\u5177 — \u817e\u8baf\u884c\u60c5 + \u4e1c\u65b9\u8d22\u5bcc\u641c\u7d22/\u8d22\u52a1，\u96f6\u5916\u90e8\u4f9d\u8d56（\u4ec5 stdlib）。

\u4e3a Claude Code Skills \u63d0\u4f9b A \u80a1\u5b9e\u65f6\u884c\u60c5、\u8d22\u52a1\u6570\u636e\u7b49\u6570\u636e。
\u8bbe\u8ba1\u539f\u5219：\u72ec\u7acb\u6a21\u5757，\u4e0d\u5f71\u54cd\u73b0\u6709\u5de5\u5177；\u4f7f\u7528 curl \u76f4\u8fde\u7ed5\u8fc7\u7cfb\u7edf\u4ee3\u7406。

\u7528\u6cd5（\u7531 Skills \u81ea\u52a8\u8c03\u7528）：
    python3.11 tools/ashare_data.py quote 600519                    # \u5b9e\u65f6\u884c\u60c5
    python3.11 tools/ashare_data.py financials 600519               # \u6838\u5fc3\u8d22\u52a1\u6570\u636e（\u8fd15\u5e74）
    python3.11 tools/ashare_data.py valuation 600519                # \u4f30\u503c\u6307\u6807
    python3.11 tools/ashare_data.py search \u8305\u53f0                      # \u641c\u7d22\u80a1\u7968\u4ee3\u7801

\u9700\u8981 Python >= 3.8，\u96f6\u5916\u90e8\u4f9d\u8d56。
"""

import argparse
import json
import os
import subprocess
import sys
from decimal import Decimal, ROUND_HALF_EVEN

_TIMEOUT = 15


def _curl(url):
    """\u7528 curl --noproxy \u76f4\u8fde，\u7ed5\u8fc7\u7cfb\u7edf\u4ee3\u7406。"""
    result = subprocess.run(
        ["/usr/bin/curl", "-s", "--noproxy", "*",
         "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
         url],
        capture_output=True, timeout=_TIMEOUT,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise ConnectionError(f"\u8bf7\u6c42\u5931\u8d25: {url}")
    # \u817e\u8baf\u884c\u60c5 API \u8fd4\u56de GBK \u7f16\u7801，\u5176\u4ed6\u8fd4\u56de UTF-8
    try:
        return result.stdout.decode("utf-8")
    except UnicodeDecodeError:
        return result.stdout.decode("gbk")


def _curl_json(url, params=None):
    """curl \u83b7\u53d6 JSON。"""
    if params:
        from urllib.parse import urlencode
        url = f"{url}?{urlencode(params)}"
    return json.loads(_curl(url))


# ---------------------------------------------------------------------------
# \u817e\u8baf\u884c\u60c5 API（\u7a33\u5b9a\u53ef\u9760，\u65e0\u9700\u9274\u6743）
# ---------------------------------------------------------------------------

def _qq_code(code: str) -> str:
    """\u5c06\u80a1\u7968\u4ee3\u7801\u8f6c\u4e3a\u817e\u8baf\u884c\u60c5\u683c\u5f0f。"""
    code = code.strip().replace(".SH", "").replace(".SZ", "").replace(".BJ", "")
    if code.startswith(("6", "9", "5")):
        return f"sh{code}"
    elif code.startswith(("0", "3", "2", "1")):
        return f"sz{code}"
    elif code.startswith(("4", "8")):
        return f"bj{code}"
    return f"sh{code}"


def _parse_qq_quote(raw: str) -> dict:
    """\u89e3\u6790\u817e\u8baf\u884c\u60c5\u6570\u636e。\u683c\u5f0f：v_shXXXXXX="\u5b57\u6bb51~\u5b57\u6bb52~..."; """
    start = raw.find('"')
    end = raw.rfind('"')
    if start < 0 or end <= start:
        return {}
    fields = raw[start + 1:end].split("~")
    if len(fields) < 50:
        return {}
    return {
        "name": fields[1],
        "code": fields[2],
        "price": fields[3],
        "prev_close": fields[4],
        "open": fields[5],
        "volume": fields[6],         # \u624b
        "buy_vol": fields[7],
        "sell_vol": fields[8],
        "high": fields[33] if len(fields) > 33 else fields[3],
        "low": fields[34] if len(fields) > 34 else fields[3],
        "change_pct": fields[32],
        "change_amt": fields[31],
        "turnover_amt": fields[37] if len(fields) > 37 else "-",
        "turnover_rate": fields[38] if len(fields) > 38 else "-",
        "pe": fields[39] if len(fields) > 39 else "-",
        "market_cap": fields[45] if len(fields) > 45 else "-",    # \u603b\u5e02\u503c（\u4ebf）
        "float_cap": fields[44] if len(fields) > 44 else "-",     # \u6d41\u901a\u5e02\u503c（\u4ebf）
        "pb": fields[46] if len(fields) > 46 else "-",
        "high_52w": fields[47] if len(fields) > 47 else "-",
        "low_52w": fields[48] if len(fields) > 48 else "-",
        "total_shares": fields[38] if len(fields) > 38 else "-",  # will recalculate
    }


def _fmt_yi(value) -> str:
    if value is None or value == "-" or value == "":
        return "-"
    try:
        v = float(value)
    except (ValueError, TypeError):
        return str(value)
    if abs(v) >= 1e8:
        return f"{v / 1e8:.2f}\u4ebf"
    if abs(v) >= 1e4:
        return f"{v / 1e4:.2f}\u4e07"
    return f"{v:.2f}"


def _fmt_pct(value) -> str:
    if value is None or value == "-" or value == "":
        return "-"
    try:
        return f"{float(value):.2f}%"
    except (ValueError, TypeError):
        return str(value)


# ---------------------------------------------------------------------------
# \u547d\u4ee4\u5b9e\u73b0
# ---------------------------------------------------------------------------

def cmd_quote(code: str):
    """\u5b9e\u65f6\u884c\u60c5\u5feb\u7167。"""
    qq_code = _qq_code(code)
    raw = _curl(f"https://qt.gtimg.cn/q={qq_code}")
    d = _parse_qq_quote(raw)
    if not d:
        print(f"❌ \u672a\u627e\u5230\u80a1\u7968 {code}")
        return

    print("=" * 60)
    print(f"\u5b9e\u65f6\u884c\u60c5: {d['name']} ({d['code']})")
    print("=" * 60)
    print(f"  \u5f53\u524d\u4ef7:     {d['price']}")
    print(f"  \u6da8\u8dcc\u5e45:     {d['change_pct']}%")
    print(f"  \u6da8\u8dcc\u989d:     {d['change_amt']}")
    print(f"  \u4eca\u5f00:       {d['open']}")
    print(f"  \u6700\u9ad8:       {d['high']}")
    print(f"  \u6700\u4f4e:       {d['low']}")
    print(f"  \u6628\u6536:       {d['prev_close']}")
    print(f"  \u6210\u4ea4\u91cf:     {d['volume']} \u624b")
    print(f"  \u6210\u4ea4\u989d:     {d['turnover_amt']}\u4e07")
    print(f"  \u603b\u5e02\u503c:     {d['market_cap']}\u4ebf")
    print(f"  \u6d41\u901a\u5e02\u503c:   {d['float_cap']}\u4ebf")
    print(f"  PE(\u52a8):     {d['pe']}")
    print(f"  PB:         {d['pb']}")
    print(f"  \u6362\u624b\u7387:     {d['turnover_rate']}%")
    print(f"  52\u5468\u6700\u9ad8:   {d['high_52w']}")
    print(f"  52\u5468\u6700\u4f4e:   {d['low_52w']}")


def cmd_valuation(code: str):
    """\u4f30\u503c\u6307\u6807\u6c47\u603b。"""
    qq_code = _qq_code(code)
    raw = _curl(f"https://qt.gtimg.cn/q={qq_code}")
    d = _parse_qq_quote(raw)
    if not d:
        print(f"❌ \u672a\u627e\u5230\u80a1\u7968 {code}")
        return

    price = d["price"]
    market_cap_yi = d["market_cap"]

    print("=" * 60)
    print(f"\u4f30\u503c\u6307\u6807: {d['name']} ({d['code']})")
    print("=" * 60)
    print(f"  \u5f53\u524d\u4ef7:     {price}")
    print(f"  \u603b\u5e02\u503c:     {market_cap_yi}\u4ebf")
    print(f"  \u6d41\u901a\u5e02\u503c:   {d['float_cap']}\u4ebf")
    print(f"  PE(\u52a8):     {d['pe']}")
    print(f"  PB:         {d['pb']}")
    print(f"  52\u5468\u6700\u9ad8:   {d['high_52w']}")
    print(f"  52\u5468\u6700\u4f4e:   {d['low_52w']}")

    # \u5e02\u503c\u9a8c\u7b97
    try:
        p = Decimal(price)
        cap = Decimal(market_cap_yi) * Decimal("1e8")
        shares = cap / p
        print(f"\n  \u63a8\u7b97\u603b\u80a1\u672c: {_fmt_yi(float(shares))}\u80a1")
        calc_cap = p * shares
        reported_cap = Decimal(market_cap_yi) * Decimal("1e8")
        diff = abs(calc_cap - reported_cap) / reported_cap * 100
        print(f"  \u5e02\u503c\u9a8c\u7b97:   ✅ \u4e00\u81f4（\u63a8\u7b97\u6cd5，\u504f\u5dee {float(diff):.1f}%）")
    except Exception:
        pass


def cmd_financials(code: str):
    """\u8fd15\u5e74\u6838\u5fc3\u8d22\u52a1\u6570\u636e。"""
    qq_code = _qq_code(code)
    raw = _curl(f"https://qt.gtimg.cn/q={qq_code}")
    d = _parse_qq_quote(raw)
    name = d.get("name", code) if d else code

    code_clean = code.strip().replace(".SH", "").replace(".SZ", "").replace(".BJ", "")
    market = "SH" if code_clean.startswith(("6", "9", "5")) else "SZ"

    # \u4e1c\u65b9\u8d22\u5bcc datacenter API（\u5e74\u62a5\u6570\u636e）
    fin_url = "https://datacenter.eastmoney.com/securities/api/data/get"
    params = {
        "type": "RPT_F10_FINANCE_MAINFINADATA",
        "sty": "ALL",
        "filter": f'(SECUCODE="{code_clean}.{market}")(REPORT_TYPE="\u5e74\u62a5")',
        "p": "1",
        "ps": "5",
        "sr": "-1",
        "st": "REPORT_DATE",
        "source": "HSF10",
        "client": "PC",
    }
    reports = []
    try:
        data = _curl_json(fin_url, params)
        reports = data.get("result", {}).get("data", [])
    except Exception:
        pass

    # \u5982\u679c\u5e74\u62a5\u7b5b\u9009\u65e0\u7ed3\u679c，\u53bb\u6389\u5e74\u62a5\u9650\u5236
    if not reports:
        params["filter"] = f'(SECUCODE="{code_clean}.{market}")'
        try:
            data = _curl_json(fin_url, params)
            reports = data.get("result", {}).get("data", [])
        except Exception:
            pass

    print("=" * 60)
    print(f"\u6838\u5fc3\u8d22\u52a1\u6570\u636e: {name} ({code_clean})")
    print("=" * 60)

    if not reports:
        print("  ⚠️ \u672a\u80fd\u83b7\u53d6\u8d22\u52a1\u6570\u636e，\u5efa\u8bae\u901a\u8fc7 WebSearch \u8865\u5145")
        return

    for r in reports[:5]:
        date = r.get("REPORT_DATE", "")[:10]
        report_name = r.get("REPORT_DATE_NAME", "")
        revenue = r.get("TOTALOPERATEREVE")
        net_profit = r.get("PARENTNETPROFIT")
        eps = r.get("EPSJB")
        bps = r.get("BPS")
        roe = r.get("ROEJQ")
        rev_growth = r.get("TOTALOPERATEREVETZ")
        profit_growth = r.get("PARENTNETPROFITTZ")

        print(f"\n  --- {date} {report_name} ---")
        if revenue is not None:
            print(f"  \u8425\u6536:           {_fmt_yi(revenue)}")
        if rev_growth is not None:
            print(f"  \u8425\u6536\u589e\u901f:       {_fmt_pct(rev_growth)}")
        if net_profit is not None:
            print(f"  \u5f52\u6bcd\u51c0\u5229\u6da6:     {_fmt_yi(net_profit)}")
        if profit_growth is not None:
            print(f"  \u51c0\u5229\u6da6\u589e\u901f:     {_fmt_pct(profit_growth)}")
        if eps is not None:
            print(f"  \u57fa\u672c\u6bcf\u80a1\u6536\u76ca:   {eps}")
        if bps is not None:
            print(f"  \u6bcf\u80a1\u51c0\u8d44\u4ea7:     {bps:.2f}")
        if roe is not None:
            print(f"  ROE(\u52a0\u6743):      {_fmt_pct(roe)}")


def cmd_search(keyword: str):
    """\u641c\u7d22\u80a1\u7968\u4ee3\u7801。"""
    url = "https://searchadapter.eastmoney.com/api/suggest/get"
    # Use env var or fall back to the public eastmoney search token
    token = os.environ.get("EASTMONEY_SEARCH_TOKEN") or "D43BF722C8E33BDC906FB84D85E326E8"
    params = {
        "input": keyword,
        "type": "14",
        "token": token,
        "count": "10",
    }
    data = _curl_json(url, params)
    results = data.get("QuotationCodeTable", {}).get("Data", [])

    if not results:
        print(f"❌ \u672a\u627e\u5230\u5339\u914d '{keyword}' \u7684\u80a1\u7968")
        return

    print("=" * 60)
    print(f"\u641c\u7d22\u7ed3\u679c: '{keyword}'")
    print("=" * 60)
    for r in results:
        code = r.get("Code", "")
        name = r.get("Name", "")
        market = r.get("MktNum", "")
        mkt_label = {"1": "\u6caa", "2": "\u6df1", "3": "\u5317"}.get(str(market), "")
        print(f"  {code} {name} [{mkt_label}]")


# ---------------------------------------------------------------------------
# CLI \u5165\u53e3
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="A\u80a1\u6570\u636e\u5de5\u5177 — \u817e\u8baf\u884c\u60c5 + \u4e1c\u65b9\u8d22\u5bcc\u8d22\u52a1\u6570\u636e",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command")

    p_quote = sub.add_parser("quote", help="\u5b9e\u65f6\u884c\u60c5")
    p_quote.add_argument("code", help="\u80a1\u7968\u4ee3\u7801，\u5982 600519")

    p_fin = sub.add_parser("financials", help="\u6838\u5fc3\u8d22\u52a1\u6570\u636e（\u8fd15\u5e74）")
    p_fin.add_argument("code", help="\u80a1\u7968\u4ee3\u7801")

    p_val = sub.add_parser("valuation", help="\u4f30\u503c\u6307\u6807")
    p_val.add_argument("code", help="\u80a1\u7968\u4ee3\u7801")

    p_search = sub.add_parser("search", help="\u641c\u7d22\u80a1\u7968\u4ee3\u7801")
    p_search.add_argument("keyword", help="\u516c\u53f8\u540d\u6216\u5173\u952e\u8bcd")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmds = {
        "quote": lambda: cmd_quote(args.code),
        "financials": lambda: cmd_financials(args.code),
        "valuation": lambda: cmd_valuation(args.code),
        "search": lambda: cmd_search(args.keyword),
    }
    cmds[args.command]()


if __name__ == "__main__":
    main()
