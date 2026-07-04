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
from datetime import datetime
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
