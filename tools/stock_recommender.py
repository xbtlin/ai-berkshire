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
