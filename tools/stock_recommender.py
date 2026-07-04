#!/usr/bin/env python3
"""stock_recommender.py — A 股稳定收益推荐 CLI。

用法：
    python tools/stock_recommender.py stable
    python tools/stock_recommender.py stable --top 5 --min-dividend 4 --max-pe 15
    python tools/stock_recommender.py stable --dry-run
    python tools/stock_recommender.py stable --force

依赖：Python >= 3.8，仅 stdlib（urllib.request / json / argparse）。
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from decimal import Decimal, getcontext
from statistics import stdev

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
REPORTS_DIR = REPO_ROOT / "reports" / "股票推荐"
INDEX_FILE = DATA_DIR / "index_constituents.json"


def _http_get(url, timeout=15, encoding="utf-8"):
    """stdlib HTTP GET（无外部依赖，跨平台）。

    返回解码后的字符串。失败抛 ConnectionError。
    """
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            data = resp.read()
    except Exception as e:
        raise ConnectionError(f"HTTP 请求失败: {url} — {e}")
    try:
        return data.decode(encoding)
    except UnicodeDecodeError:
        return data.decode("gbk", errors="replace")


def _qq_code(code: str) -> str:
    """将股票代码转为腾讯行情格式（sh/sz/bj 前缀）。"""
    code = code.strip().replace(".SH", "").replace(".SZ", "").replace(".BJ", "")
    if code.startswith(("6", "9", "5")):
        return f"sh{code}"
    elif code.startswith(("0", "3", "2", "1")):
        return f"sz{code}"
    elif code.startswith(("4", "8")):
        return f"bj{code}"
    return f"sh{code}"


def _parse_qq_quote(raw: str) -> dict:
    """解析腾讯行情返回的 ~ 分隔字符串。

    格式：v_shXXXXXX="字段1~字段2~...~字段N";
    返回关键字段 dict。失败返回空 dict。
    """
    start = raw.find('"')
    end = raw.rfind('"')
    if start < 0 or end <= start:
        return {}
    fields = raw[start + 1:end].split("~")
    if len(fields) < 9:
        return {}

    # 腾讯行情有两种布局：
    #   真实线上：fields[0]=市场标识("1"/"51"), [1]=name, [2]=code, [3]=price, [4]=prev_close
    #   简化样本（无市场标识）：fields[0]=name, [1]=code, [2]=price, [3]=prev_close
    # 用 fields[2] 是否为 6 位数字代码判定偏移
    offset = 1 if (len(fields) > 2 and fields[2].isdigit() and len(fields[2]) == 6) else 0
    name_idx, code_idx, price_idx, prev_idx = 0 + offset, 1 + offset, 2 + offset, 3 + offset
    return {
        "name": fields[name_idx],
        "code": fields[code_idx],
        "price": fields[price_idx],
        "prev_close": fields[prev_idx],
        "pe": fields[39] if len(fields) > 39 else "-",
        "market_cap_yi": fields[45] if len(fields) > 45 else "-",  # 单位：亿
        "pb": fields[46] if len(fields) > 46 else "-",
    }


def fetch_quote(code: str) -> dict:
    """拉腾讯行情：PE / PB / 当前价 / 总市值（亿）。失败抛 ConnectionError。"""
    raw = _http_get(f"https://qt.gtimg.cn/q={_qq_code(code)}")
    return _parse_qq_quote(raw)


def extract_roe_history(api_response: dict, years: int = 3) -> list:
    """从东财 financials API 响应提取近 N 年 ROE（按日期降序）。

    输入：完整的 API JSON 响应。
    输出：[ROE_最新年, ROE_去年, ROE_前年]（单位 %）。
    无数据返回空列表。
    """
    data = (api_response.get("result") or {}).get("data") or []
    annual = [r for r in data if r.get("REPORT_TYPE") == "年报" and r.get("ROEJQ") is not None]
    annual.sort(key=lambda x: x.get("REPORT_DATE", ""), reverse=True)
    return [float(r["ROEJQ"]) for r in annual[:years]]


def fetch_financials(code: str, years: int = 3) -> dict:
    """拉东财近 5 年年报财务数据。返回 {roe_history: [...]}。失败抛异常。

    只取年报，按日期降序。
    """
    code = code.strip().replace(".SH", "").replace(".SZ", "").replace(".BJ", "")
    if code.startswith(("6", "9", "5")):
        market = "SH"
    elif code.startswith(("4", "8")):
        market = "BJ"
    else:
        market = "SZ"
    url = "https://datacenter.eastmoney.com/securities/api/data/get"
    params = {
        "type": "RPT_F10_FINANCE_MAINFINADATA",
        "sty": "ALL",
        "filter": f'(SECUCODE="{code}.{market}")(REPORT_TYPE="年报")',
        "p": "1", "ps": "5", "sr": "-1", "st": "REPORT_DATE",
        "source": "HSF10", "client": "PC",
    }
    full_url = f"{url}?{urlencode(params)}"
    raw = _http_get(full_url)
    api_response = json.loads(raw)
    return {"roe_history": extract_roe_history(api_response, years=years)}


def extract_dividends_ttm(api_response: dict, today: str = None) -> float:
    """汇总近 365 天内"每 10 股派息税前"总额。

    today: 'YYYY-MM-DD' 字符串，默认系统当天。
    返回单位：元（每 10 股）。
    """
    today_dt = datetime.strptime(today, "%Y-%m-%d") if today else datetime.now()
    cutoff = today_dt - timedelta(days=365)
    data = (api_response.get("result") or {}).get("data") or []
    total = 0.0
    for r in data:
        date_str = (r.get("EQUITY_REGISTRATION_DATE") or "")[:10]
        if not date_str:
            continue
        try:
            reg_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            continue
        if reg_date >= cutoff:
            amt = r.get("BEFORE_TAX_DIVIDEND")
            if amt is not None:
                total += float(amt)
    return total


def calc_dividend_yield(dividend_per_10_ttm: float, price: float) -> float:
    """TTM 股息率 %。

    dividend_per_10_ttm: 近 12 个月每 10 股派息合计（元）。
    price: 当前股价（元）。
    返回：股息率百分比（5.0 表示 5%）。
    """
    if not price or price <= 0:
        return 0.0
    return dividend_per_10_ttm / 10.0 / price * 100.0


def fetch_dividends(code: str) -> dict:
    """拉东财 F10 分红明细。返回 {dividend_per_10_ttm: float, raw_records: [...]}。"""
    code = code.strip().replace(".SH", "").replace(".SZ", "").replace(".BJ", "")
    if code.startswith(("6", "9", "5")):
        market = "SH"
    elif code.startswith(("4", "8")):
        market = "BJ"
    else:
        market = "SZ"
    url = "https://datacenter.eastmoney.com/securities/api/data/get"
    params = {
        "type": "RPT_SHAREBONUS_DET",
        "sty": "ALL",
        "filter": f'(SECUCODE="{code}.{market}")',
        "p": "1", "ps": "20", "sr": "-1", "st": "REPORT_DATE",
        "source": "HSF10", "client": "PC",
    }
    full_url = f"{url}?{urlencode(params)}"
    raw = _http_get(full_url)
    api_response = json.loads(raw)
    # 东财真实字段 EQUITY_RECORD_DATE / PRETAX_BONUS_RMB 映射到规格字段名
    # EQUITY_REGISTRATION_DATE / BEFORE_TAX_DIVIDEND（extract_dividends_ttm 使用）
    raw_records = (api_response.get("result") or {}).get("data") or []
    mapped = []
    for r in raw_records:
        mapped.append({
            "EQUITY_REGISTRATION_DATE": r.get("EQUITY_RECORD_DATE") or r.get("EQUITY_REGISTRATION_DATE"),
            "BEFORE_TAX_DIVIDEND": r.get("PRETAX_BONUS_RMB") if r.get("PRETAX_BONUS_RMB") is not None else r.get("BEFORE_TAX_DIVIDEND"),
        })
    mapped_response = {"result": {"data": mapped}}
    return {
        "dividend_per_10_ttm": extract_dividends_ttm(mapped_response),
        "raw_records": raw_records,
    }


def score_stable(
    fund: dict,
    min_dividend: float = 4.0,
    max_pe: float = 15.0,
    min_roe: float = 12.0,
    max_roe_stddev: float = 5.0,
) -> dict:
    """4 维硬指标打分。

    fund: {dividend_yield, pe, roe_history}
        roe_history: 近 3 年 ROE 序列（最新在前），单位 %。
    返回: {score: 0-4, details: {dividend_yield, pe, roe_mean, roe_stable}}
    """
    details = {}
    # 1. 股息率 > 4%
    details["dividend_yield"] = fund.get("dividend_yield", 0) >= min_dividend
    # 2. PE < 15
    pe = fund.get("pe")
    details["pe"] = (pe is not None and 0 < pe <= max_pe)
    # 3. ROE 均值 > 12%
    roe_history = fund.get("roe_history") or []
    if roe_history:
        roe_mean = sum(roe_history) / len(roe_history)
        details["roe_mean"] = roe_mean >= min_roe
        # 4. ROE 稳定性：近 3 年 stddev < 5pp
        if len(roe_history) >= 2:
            details["roe_stable"] = stdev(roe_history) < max_roe_stddev
        else:
            details["roe_stable"] = False
    else:
        details["roe_mean"] = False
        details["roe_stable"] = False
    score = sum(1 for v in details.values() if v)
    return {"score": score, "details": details}


def sort_and_filter(items: list, min_score: int = 3, top_n: int = 5):
    """分组 + 排序 + 截断（strong 与 weak 互斥）。

    items: [{code, score, dividend_yield, ...}]
    返回: (strong, weak)
        strong: score >= 4（强烈推荐）的前 top_n 只，按股息率降序
        weak:   min_score <= score < 4（备选，未达强烈推荐线）的前 top_n 只，
                按股息率降序

    说明：4 分项属于"强烈推荐"，不再计入"备选"。当 min_score >= 4 时
    weak 永远为空（备选线 >= 强烈推荐线，无中间地带）。
    """
    strong = sorted(
        [x for x in items if x["score"] >= 4],
        key=lambda x: x.get("dividend_yield", 0),
        reverse=True,
    )[:top_n]
    weak = sorted(
        [x for x in items if min_score <= x["score"] < 4],
        key=lambda x: x.get("dividend_yield", 0),
        reverse=True,
    )[:top_n]
    return strong, weak


def ask_fin_ai_opinion(candidates: list) -> dict:
    """调 fin_ai 批量问 top N 候选股的观点层。

    candidates: [{code, name, score, dividend_yield, pe, roe_mean}]
    返回: {summary: str, warnings: {code: str}, ok: bool, error: str}
        失败时 ok=False，error 描述原因（配额耗尽/超时/网络）。
    """
    if not candidates:
        return {"summary": "", "warnings": {}, "ok": True, "error": ""}
    try:
        from tools.fin_ai import ask, quota
    except ImportError as e:
        return {"summary": "", "warnings": {}, "ok": False,
                "error": f"fin_ai 模块不可用: {e}"}

    # 配额预检
    try:
        q = quota()
        if q is not None and (q.exceeded or q.remaining < 1):
            return {"summary": "", "warnings": {}, "ok": False,
                    "error": f"fin_ai 配额不足（剩余 {q.remaining}/{q.limit}）"}
    except Exception as e:
        # 配额接口失败时容错（不阻塞），但留痕便于排查
        print(f"[warn] fin_ai 配额预检失败，跳过预检: {e}", file=sys.stderr)

    lines = ["请评估以下 A 股稳定收益候选股（按稳定性排序）：\n"]
    for i, c in enumerate(candidates, 1):
        div_y = c.get('dividend_yield') or 0
        roe_m = c.get('roe_mean') or 0
        pe_v = c.get('pe')
        pe_str = f"{pe_v:.2f}" if isinstance(pe_v, (int, float)) else "N/A"
        lines.append(
            f"{i}. {c.get('name', c['code'])} ({c['code']}) — "
            f"股息率 {div_y:.2f}%, "
            f"PE {pe_str}, "
            f"ROE 均值 {roe_m:.2f}%"
        )
    lines.append("\n请输出：")
    lines.append("1. 按股息可持续性从高到低排序（仅代码）")
    lines.append("2. 每只股的 1 个核心风险（一句话）")
    lines.append("3. 强烈推荐的 top 3 + 应警惕的 bottom 2")
    query = "\n".join(lines)

    try:
        result = ask(query, ttl_hours=24)
        return {"summary": result.content, "warnings": {}, "ok": True, "error": ""}
    except Exception as e:
        return {"summary": "", "warnings": {}, "ok": False,
                "error": f"fin_ai 调用失败: {e}"}


def load_index_constituents():
    """加载中证红利 + 上证 50 成分股，返回去重后的 6 位代码列表。

    数据源：data/index_constituents.json（本地基线）。
    失败时抛异常，由 main() 统一处理。
    """
    with open(INDEX_FILE, encoding="utf-8") as f:
        data = json.load(f)
    seen = set()
    codes = []
    for key in ("csi_dividend", "sse_50"):
        for entry in data.get(key, []):
            code = entry["code"].strip()
            if code and code not in seen:
                seen.add(code)
                codes.append(code)
    return codes


def main():
    parser = argparse.ArgumentParser(description="A 股股票推荐 CLI")
    sub = parser.add_subparsers(dest="mode", required=True)
    p_stable = sub.add_parser("stable", help="稳定收益模式（高股息+低PE+稳定ROE）")
    p_stable.add_argument("--top", type=int, default=5, help="Top N 推荐（默认 5）")
    p_stable.add_argument("--min-dividend", type=float, default=4.0, help="股息率下限 %（默认 4.0）")
    p_stable.add_argument("--max-pe", type=float, default=15.0, help="PE 上限（默认 15.0）")
    p_stable.add_argument("--min-roe", type=float, default=12.0, help="ROE 下限 %（默认 12.0）")
    p_stable.add_argument("--dry-run", action="store_true", help="仅打印不写文件")
    p_stable.add_argument("--force", action="store_true", help="覆盖当日报告")
    args = parser.parse_args()
    print(f"[stub] mode={args.mode}", file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
