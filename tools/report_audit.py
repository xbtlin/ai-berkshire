#!/usr/bin/env python3
"""Report Audit Tool for AI Berkshire.

\u6570\u636e\u62bd\u68c0\u5de5\u5177：\u4ece\u7814\u7a76\u62a5\u544a\u4e2d\u62bd\u53d615%\u7684\u8d22\u52a1\u6570\u636e\u70b9，\u4e0e\u53ef\u9760\u4fe1\u6e90\u6bd4\u5bf9，
\u901a\u8fc7\u5219\u51c6\u51fa，\u4e0d\u901a\u8fc7\u5219\u6253\u56de\u5e76\u8bf4\u660e\u539f\u56e0。

Zero external dependencies — uses only Python stdlib.
Requires Python >= 3.7.

\u5de5\u4f5c\u6d41\u7a0b（\u4e09\u6b65）：
  Step 1 — \u63d0\u53d6\u6570\u636e\u70b9，\u968f\u673a\u62bd\u683715%：
    python3 tools/report_audit.py extract --report reports/xxx.md

  Step 2 — Claude \u5bf9\u62bd\u68c0\u6e05\u5355\u4e2d\u7684\u6bcf\u4e2a\u6570\u636e\u70b9，\u4ece\u53ef\u9760\u4fe1\u6e90（macrotrends/
            stockanalysis/aastocks/eastmoney）\u53d6\u6570，\u586b\u5165 fetched_value

  Step 3 — \u8f93\u5165\u6838\u9a8c\u7ed3\u679c，\u8f93\u51fa\u51c6\u51fa/\u6253\u56de\u5224\u51b3：
    python3 tools/report_audit.py verdict --results '[...]'

  \u4e00\u6b65\u5b8c\u6210（\u4ec5\u63d0\u53d6+\u6253\u5370\u62bd\u68c0\u6e05\u5355，\u4e0d\u505a\u7f51\u7edc\u9a8c\u8bc1）：
    python3 tools/report_audit.py extract --report reports/xxx.md --dry-run
"""

import argparse
import json
import math
import os
import re
import sys
from decimal import Decimal, Context, ROUND_HALF_EVEN
from random import Random

_CTX = Context(prec=28, rounding=ROUND_HALF_EVEN)

# ---------------------------------------------------------------------------
# \u6570\u636e\u70b9\u63d0\u53d6：\u4ece Markdown \u62a5\u544a\u4e2d\u8bc6\u522b\u8d22\u52a1\u6570\u5b57
# ---------------------------------------------------------------------------

# \u5339\u914d\u6a21\u5f0f：\u6570\u5b57 + \u5355\u4f4d，\u524d\u9762\u6709\u4e0a\u4e0b\u6587\u6807\u7b7e
# \u4f8b：\u6536\u5165：1,239\u4ebf\u5143、PE 18.8x、\u6bdb\u5229\u7387 56%、\u5e02\u503c ~$5,670\u4ebf
_PATTERNS = [
    # \u767e\u5206\u6bd4
    (r'([\d,，\.]+)\s*%',                        '%',    'percent'),
    # \u4ebf\u5143/\u4ebf\u7f8e\u5143/\u4ebf\u6e2f\u5143
    (r'([\d,，\.]+)\s*\u4ebf(\u5143|\u7f8e\u5143|\u6e2f\u5143|RMB|USD|HKD)?', '\u4ebf',    'hundred_million'),
    # \u500d\u6570 PE/PB/PS
    (r'([\d,，\.]+)\s*[xX\u500d]',                   'x',    'multiple'),
    # \u4e07\u4ebf
    (r'([\d,，\.]+)\s*\u4e07\u4ebf',                      '\u4e07\u4ebf', 'trillion'),
    # \u7f8e\u5143\u7edd\u5bf9\u503c（B/T）
    (r'\$\s*([\d,，\.]+)\s*([BMT\u4ebf])',             '$',    'usd_abs'),
    # \u7eaf\u6574\u6570（\u5982\u5e02\u503c、\u6536\u5165、\u7528\u6237\u6570\u7b49，\u51fa\u73b0\u5728\u8868\u683c | \u91cc）
    (r'\|\s*[~\u7ea6]?\$?([\d,，\.]+)\s*\|',          '',     'table_num'),
]

_LABEL_RE = re.compile(
    r'(?P<label>[^\|\n：:]{2,25})[：:\s]+[~\u7ea6]?\$?(?P<num>[\d,，\.]+)\s*(?P<unit>\u4ebf[\u5143\u7f8e\u6e2f]?\u5143?|\u4e07\u4ebf|[xX\u500d]|%|[BMT])?'
)

_TABLE_ROW_RE = re.compile(
    r'\|\s*(?P<label>[^|]{1,40})\s*\|\s*[~\u7ea6]?\$?(?P<num>[\d,，\.]+)\s*(?P<unit>\u4ebf[\u5143\u7f8e\u6e2f]?\u5143?|\u4e07\u4ebf|[xX\u500d]|%|[BMT])?\s*\|'
)


def _clean_num(s: str) -> float:
    """\u628a\u5e26\u9017\u53f7、\u4e2d\u6587\u9017\u53f7\u7684\u6570\u5b57\u5b57\u7b26\u4e32\u8f6c\u4e3a float。"""
    s = s.replace(',', '').replace('，', '').strip()
    try:
        return float(s)
    except ValueError:
        return None


def _is_valid_label(label: str) -> bool:
    """\u5224\u65ad\u6807\u7b7e\u662f\u5426\u662f\u6709\u610f\u4e49\u7684\u8d22\u52a1\u5b57\u6bb5\u540d，\u8fc7\u6ee4\u566a\u58f0。"""
    label = label.strip()
    # \u592a\u77ed
    if len(label) < 2:
        return False
    # \u7eaf\u6570\u5b57\u6216\u7eaf\u5e74\u4efd
    if re.fullmatch(r'[\d\s\u5e74\u5b63\u5ea6Q]+', label):
        return False
    # \u4ee5\u7b26\u53f7/markdown\u6807\u8bb0\u5f00\u5934
    if re.match(r'^[+\-\*#\|~\$>_`]', label):
        return False
    # \u542b\u6709 markdown \u7c97\u4f53/\u4ee3\u7801\u6807\u8bb0
    if '**' in label or '`' in label or '__' in label:
        return False
    # \u6807\u7b7e\u542b\u6709\u7eaf\u589e\u901f\u7b26\u53f7（\u5982 +56%、-13% \u5355\u72ec\u4f5c\u6807\u7b7e）
    if re.fullmatch(r'[+\-]?\d+(\.\d+)?%', label):
        return False
    # \u5e38\u89c1\u65e0\u610f\u4e49\u6807\u7b7e
    _SKIP = {'\u6765\u6e90', 'sources', 'source', '\u8bf4\u660e', '\u6ce8\u610f', '\u5907\u6ce8', '\u6570\u636e\u6765\u6e90',
             'n/a', '—', '-', '/', '\u5408\u8ba1', 'total', '\u5355\u4f4d', '\u8d8b\u52bf'}
    if label.lower() in _SKIP:
        return False
    return True


# \u4e24\u5217\u8868\u683c\u884c：| \u6807\u7b7e | \u6570\u503c unit |（\u4e13\u4e3a\u8d22\u52a1\u62a5\u544a\u7684 KV \u8868\u8bbe\u8ba1）
_KV_TABLE_RE = re.compile(
    r'^\|\s*(?P<label>[^|*\n]{2,40}?)\s*\|\s*[~\u7ea6]?\$?(?P<num>[\d,，\.]+)\s*'
    r'(?P<unit>\u4ebf[\u5143\u7f8e\u6e2f]?\u5143?|\u4e07\u4ebf|[xX\u500d]|%|[BMT\u4ebf])?\s*[\|（\(]'
)

# \u5e26\u6807\u7b7e\u7684 KV \u884c：\u6807\u7b7e：\u6570\u503c \u5355\u4f4d
_KV_LABEL_RE = re.compile(
    r'(?P<label>[\u4e00-\u9fa5A-Za-z][^\|\n：:*]{1,30})[：:]\s*[~\u7ea6]?\$?'
    r'(?P<num>[\d,，\.]+)\s*(?P<unit>\u4ebf[\u5143\u7f8e\u6e2f]?\u5143?|\u4e07\u4ebf|[xX\u500d]|%|[BMT])?'
)


def _parse_md_tables(lines: list) -> list:
    """\u89e3\u6790 Markdown \u4e2d\u6240\u6709\u8868\u683c，\u8fd4\u56de (row_label, col_header, value, unit, lineno, raw) \u5217\u8868。"""
    results = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # \u68c0\u6d4b\u8868\u5934\u884c（\u542b | \u4e14\u4e0d\u662f\u5206\u9694\u884c）
        if '|' in line and not re.match(r'^\|[\-\s\|:]+\|$', line):
            headers_raw = [h.strip().strip('*_').strip() for h in line.split('|')]
            headers_raw = [h for h in headers_raw if h]
            # \u4e0b\u4e00\u884c\u5e94\u662f\u5206\u9694\u884c
            if i + 1 < len(lines) and re.match(r'^\|[\-\s\|:]+\|$', lines[i+1].strip()):
                i += 2  # \u8df3\u8fc7\u5206\u9694\u884c
                # \u8bfb\u6570\u636e\u884c
                while i < len(lines):
                    dline = lines[i].strip()
                    if not dline or not dline.startswith('|'):
                        break
                    cells = [c.strip().strip('*_~').strip() for c in dline.split('|')]
                    cells = [c for c in cells if c != '']
                    if len(cells) < 2:
                        i += 1
                        continue
                    row_label = cells[0]
                    for col_idx, cell in enumerate(cells[1:], start=1):
                        col_header = headers_raw[col_idx] if col_idx < len(headers_raw) else f'\u5217{col_idx}'
                        # \u63d0\u53d6 cell \u4e2d\u7684\u6570\u5b57+\u5355\u4f4d
                        m = re.search(
                            r'[~\u7ea6]?\$?([\d,，\.]+)\s*(\u4ebf[\u5143\u7f8e\u6e2f]?\u5143?|\u4e07\u4ebf|[xX\u500d]|%|[BMT])?',
                            cell
                        )
                        if m:
                            val = _clean_num(m.group(1))
                            unit = (m.group(2) or '').strip()
                            if val and val != 0 and val < 1e15:
                                results.append((row_label, col_header, val, unit, i + 1, dline))
                    i += 1
                continue
        i += 1
    return results


def extract_data_points(md_text: str) -> list:
    """\u4ece Markdown \u62a5\u544a\u4e2d\u63d0\u53d6\u6240\u6709\u53ef\u8bc6\u522b\u7684\u8d22\u52a1\u6570\u636e\u70b9。

    \u8986\u76d6\u4e09\u7c7b\u7ed3\u6784：
      1. \u591a\u5217 Markdown \u8868\u683c（\u6700\u4e3b\u8981\u7684\u6765\u6e90）：(\u884c\u6807\u7b7e + \u5217\u6807\u9898) → \u6570\u503c
      2. \u5e26\u5192\u53f7\u7684 KV \u884c：\u6807\u7b7e：\u6570\u503c \u5355\u4f4d
      3. \u52a0\u7c97\u6570\u5b57\u884c：**\u6570\u503c** \u5355\u4f4d

    \u8fd4\u56de list of dict：
      {id, label, reported_value, unit, raw_text, line_number}
    """
    points = []
    seen = set()

    def _add(label, val, unit, lineno, raw):
        label = re.sub(r'[\*_`]+', '', label).strip()
        if not _is_valid_label(label):
            return
        if val is None or val == 0 or val > 1e15:
            return
        # \u8fc7\u6ee4\u7eaf\u5e74\u4efd/\u5b63\u5ea6
        if re.fullmatch(r'(20\d{2}|Q[1-4]|\d{4}\s*Q[1-4])', label.strip()):
            return
        key = f"{label}|{round(val,4)}|{unit}"
        if key in seen:
            return
        seen.add(key)
        points.append({
            'id': len(points) + 1,
            'label': label,
            'reported_value': val,
            'unit': unit,
            'raw_text': raw[:120],
            'line_number': lineno,
        })

    lines = md_text.split('\n')
    in_code = False

    # --- 1. \u591a\u5217\u8868\u683c ---
    for row_label, col_header, val, unit, lineno, raw in _parse_md_tables(lines):
        # \u8df3\u8fc7\u65e0\u610f\u4e49\u884c\u6807\u7b7e
        if not _is_valid_label(row_label):
            continue
        # \u8df3\u8fc7\u65e0\u610f\u4e49\u5217\u6807\u9898（YoY\u589e\u901f\u5217\u5355\u72ec\u6807\u6ce8，\u4e0d\u4f5c\u4e3a\u5f85\u6838\u9a8c\u6570\u636e）
        if col_header.upper() in ('YOY', 'YOY\u589e\u901f', '\u589e\u901f', '\u540c\u6bd4', '\u53d8\u5316', '\u8d8b\u52bf', '\u8bf4\u660e', '\u5907\u6ce8'):
            continue
        # label = "\u884c\u6807\u7b7e · \u5217\u6807\u9898"（\u82e5\u5217\u6807\u9898\u662f\u884c\u6807\u7b7e\u7684\u8865\u5145）
        if col_header and col_header != row_label:
            label = f"{row_label} · {col_header}"
        else:
            label = row_label
        _add(label, val, unit, lineno, raw)

    # --- 2. KV \u5192\u53f7\u884c ---
    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            continue
        if in_code or stripped.startswith('> ') or re.match(r'^#{1,6}\s', stripped):
            continue
        if '|' in stripped:
            continue  # \u8868\u683c\u5df2\u5728\u4e0a\u9762\u5904\u7406

        for m in _KV_LABEL_RE.finditer(stripped):
            label = m.group('label')
            val = _clean_num(m.group('num'))
            unit = (m.group('unit') or '').strip()
            _add(label, val, unit, lineno, stripped)

    return points


def sample_points(points: list, ratio: float = 0.15, seed: int = None) -> list:
    """\u968f\u673a\u62bd\u53d6 ratio \u6bd4\u4f8b\u7684\u6570\u636e\u70b9，\u6700\u5c11 3 \u4e2a，\u6700\u591a 30 \u4e2a。"""
    n = max(3, min(30, math.ceil(len(points) * ratio)))
    n = min(n, len(points))
    rng = Random(seed)
    sampled = rng.sample(points, n)
    # \u6309\u884c\u53f7\u6392\u5e8f，\u65b9\u4fbf\u4eba\u5de5\u6bd4\u5bf9
    return sorted(sampled, key=lambda p: p['line_number'])


# ---------------------------------------------------------------------------
# \u51c6\u51fa/\u6253\u56de\u5224\u51b3
# ---------------------------------------------------------------------------

_TOLERANCE = 0.01   # 1% \u5bb9\u5dee


def _pct_diff(reported: float, fetched: float) -> float:
    """\u76f8\u5bf9\u504f\u5dee (absolute)。"""
    if reported == 0:
        return 0.0 if fetched == 0 else float('inf')
    return abs(reported - fetched) / abs(reported)


def render_verdict(results: list, report_name: str = "") -> dict:
    """
    \u6839\u636e\u6838\u9a8c\u7ed3\u679c\u8f93\u51fa\u51c6\u51fa/\u6253\u56de\u5224\u51b3。

    results: list of dict，\u6bcf\u9879\u5305\u542b：
      - id, label, reported_value, unit, fetched_value, fetched_source
      - (\u53ef\u9009) fetched_value2, fetched_source2   ← \u7b2c\u4e8c\u6765\u6e90

    \u8fd4\u56de：
      {
        'verdict': 'PASS' | 'FAIL',
        'pass_count': int,
        'fail_count': int,
        'total': int,
        'fail_items': [...],
        'summary': str,
      }
    """
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    print('=' * 70)
    print(f'{BOLD}\u62a5\u544a\u6570\u636e\u62bd\u68c0 — \u51c6\u51fa/\u6253\u56de\u5224\u51b3{RESET}')
    if report_name:
        print(f'\u62a5\u544a：{report_name}')
    print('=' * 70)
    print()

    fail_items = []
    warn_items = []

    for item in results:
        label = item.get('label', '?')
        reported = float(item.get('reported_value', 0))
        unit = item.get('unit', '')
        fetched = item.get('fetched_value')
        source = item.get('fetched_source', '?')
        fetched2 = item.get('fetched_value2')
        source2 = item.get('fetched_source2', '')

        # --- \u4e3b\u6765\u6e90\u6bd4\u5bf9 ---
        if fetched is None:
            # \u6ca1\u6709\u63d0\u4f9b\u6838\u9a8c\u503c → \u8df3\u8fc7（\u4e0d\u8ba1\u5165\u901a\u8fc7/\u5931\u8d25）
            print(f'  ⬜ [{item["id"]:>2}] {label[:35]:35s} {reported:>12.2f} {unit}  →  [\u672a\u63d0\u4f9b\u6838\u9a8c\u503c，\u8df3\u8fc7]')
            continue

        fetched = float(fetched)
        diff1 = _pct_diff(reported, fetched)

        # --- \u7b2c\u4e8c\u6765\u6e90\u6bd4\u5bf9（\u5982\u6709）---
        diff2 = None
        if fetched2 is not None:
            fetched2 = float(fetched2)
            diff2 = _pct_diff(reported, fetched2)

        # \u5224\u65ad
        pass1 = diff1 <= _TOLERANCE
        pass2 = (diff2 is None) or (diff2 <= _TOLERANCE)

        if pass1 and pass2:
            status = f'{GREEN}✅ \u901a\u8fc7{RESET}'
            detail = f'{source}: {fetched:.2f} (\u504f\u5dee {diff1*100:.2f}%)'
            if diff2 is not None:
                detail += f'  |  {source2}: {fetched2:.2f} (\u504f\u5dee {diff2*100:.2f}%)'
        elif not pass1 and not pass2:
            status = f'{RED}❌ \u4e0d\u901a\u8fc7{RESET}'
            detail = f'{source}: {fetched:.2f} (\u504f\u5dee {diff1*100:.2f}%)'
            if diff2 is not None:
                detail += f'  |  {source2}: {fetched2:.2f} (\u504f\u5dee {diff2*100:.2f}%)'
            fail_items.append({
                'id': item['id'],
                'label': label,
                'reported': reported,
                'unit': unit,
                'fetched': fetched,
                'source': source,
                'fetched2': fetched2,
                'source2': source2,
                'diff1_pct': round(diff1 * 100, 2),
                'diff2_pct': round(diff2 * 100, 2) if diff2 is not None else None,
                'raw_text': item.get('raw_text', ''),
                'line_number': item.get('line_number', 0),
            })
        else:
            # \u4e00\u4e2a\u6765\u6e90\u901a\u8fc7，\u4e00\u4e2a\u4e0d\u901a\u8fc7 → \u8b66\u544a，\u4e0d\u8ba1\u5165\u5931\u8d25
            status = f'{YELLOW}⚠️  \u8b66\u544a{RESET}'
            detail = f'{source}: {fetched:.2f} (\u504f\u5dee {diff1*100:.2f}%)'
            if diff2 is not None:
                detail += f'  |  {source2}: {fetched2:.2f} (\u504f\u5dee {diff2*100:.2f}%)'
            warn_items.append({
                'id': item['id'], 'label': label,
                'reported': reported, 'unit': unit,
                'diff1_pct': round(diff1 * 100, 2),
                'diff2_pct': round(diff2 * 100, 2) if diff2 is not None else None,
            })

        print(f'  {status} [{item["id"]:>2}] {label[:35]:35s}  \u62a5\u544a: {reported:>12.2f} {unit}')
        print(f'              {" " * 38}{detail}')

    print()
    print('-' * 70)

    total = len([r for r in results if r.get('fetched_value') is not None])
    fail_count = len(fail_items)
    warn_count = len(warn_items)
    pass_count = total - fail_count - warn_count

    print(f'  \u62bd\u68c0\u603b\u6570: {total}  |  \u901a\u8fc7: {GREEN}{pass_count}{RESET}  |  \u8b66\u544a: {YELLOW}{warn_count}{RESET}  |  \u4e0d\u901a\u8fc7: {RED}{fail_count}{RESET}')
    print()

    if fail_count == 0:
        print(f'{BOLD}{GREEN}【\u51c6\u51fa】\u6240\u6709\u62bd\u68c0\u6570\u636e\u901a\u8fc7，\u62a5\u544a\u53ef\u53d1\u5e03。{RESET}')
        verdict = 'PASS'
    else:
        print(f'{BOLD}{RED}【\u6253\u56de】{fail_count} \u4e2a\u6570\u636e\u70b9\u6838\u9a8c\u4e0d\u901a\u8fc7，\u62a5\u544a\u9700\u4fee\u6b63\u540e\u91cd\u5ba1。{RESET}')
        print()
        print(f'{BOLD}\u6253\u56de\u539f\u56e0：{RESET}')
        for fi in fail_items:
            print(f'  ❌ \u7b2c {fi["line_number"]} \u884c | {fi["label"]}')
            print(f'     \u62a5\u544a\u503c：{fi["reported"]} {fi["unit"]}')
            print(f'     {fi["source"]}：{fi["fetched"]}  （\u504f\u5dee {fi["diff1_pct"]}%）')
            if fi.get('fetched2') is not None:
                print(f'     {fi["source2"]}：{fi["fetched2"]}  （\u504f\u5dee {fi["diff2_pct"]}%）')
            print(f'     \u539f\u6587：{fi["raw_text"][:80]}')
            print()
        verdict = 'FAIL'

    if warn_count > 0:
        print(f'{YELLOW}\u6ce8\u610f：{warn_count} \u4e2a\u6570\u636e\u70b9\u4e24\u6765\u6e90\u7ed3\u679c\u4e0d\u4e00\u81f4（\u8d85\u8fc71%），\u53ef\u80fd\u662f\u53e3\u5f84\u5dee\u5f02（GAAP/Non-GAAP\u6216\u6c47\u7387），\u8bf7\u4eba\u5de5\u590d\u6838。{RESET}')
        for wi in warn_items:
            print(f'  ⚠️  {wi["label"]}  \u62a5\u544a:{wi["reported"]} {wi["unit"]}  \u504f\u5dee: {wi["diff1_pct"]}% / {wi["diff2_pct"]}%')

    print('=' * 70)

    return {
        'verdict': verdict,
        'pass_count': pass_count,
        'warn_count': warn_count,
        'fail_count': fail_count,
        'total': total,
        'fail_items': fail_items,
        'warn_items': warn_items,
    }


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Report Audit Tool — \u7814\u7a76\u62a5\u544a\u6570\u636e\u62bd\u68c0\u5de5\u5177',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
\u5de5\u4f5c\u6d41\u7a0b：

  Step 1 — \u63d0\u53d6\u6570\u636e\u70b9\u5e76\u968f\u673a\u62bd\u6837 15%，\u8f93\u51fa\u62bd\u68c0\u6e05\u5355：
    python3 tools/report_audit.py extract --report reports/\u817e\u8baf/\u817e\u8baf-research-20260408.md

  Step 2 — Claude \u5bf9\u6e05\u5355\u4e2d\u6bcf\u4e2a\u6570\u636e\u70b9，\u4ece\u53ef\u9760\u4fe1\u6e90\u53d6\u6570，
            \u586b\u5165 fetched_value / fetched_source / fetched_value2 / fetched_source2

  Step 3 — \u8f93\u5165\u6838\u9a8c\u7ed3\u679c，\u8f93\u51fa\u51c6\u51fa/\u6253\u56de\u5224\u51b3：
    python3 tools/report_audit.py verdict --results '[
      {"id":1,"label":"\u8425\u4e1a\u6536\u5165","reported_value":7518,"unit":"\u4ebf","fetched_value":7518,"fetched_source":"macrotrends","fetched_value2":7500,"fetched_source2":"stockanalysis"},
      ...
    ]'

  \u4e00\u6b65\u9884\u89c8（\u53ea\u6253\u5370\u62bd\u68c0\u6e05\u5355，\u4e0d\u6838\u9a8c）：
    python3 tools/report_audit.py extract --report reports/xxx.md --dry-run

  \u6307\u5b9a\u62bd\u6837\u6bd4\u4f8b（\u9ed8\u8ba40.15）：
    python3 tools/report_audit.py extract --report reports/xxx.md --ratio 0.20

  \u56fa\u5b9a\u968f\u673a\u79cd\u5b50（\u590d\u73b0\u540c\u4e00\u6279\u6837\u672c）：
    python3 tools/report_audit.py extract --report reports/xxx.md --seed 42
        """)

    sub = parser.add_subparsers(dest='command')

    # extract
    ext = sub.add_parser('extract', help='\u4ece\u62a5\u544a\u63d0\u53d6\u6570\u636e\u70b9\u5e76\u968f\u673a\u62bd\u6837')
    ext.add_argument('--report', required=True, help='\u62a5\u544a\u6587\u4ef6\u8def\u5f84（Markdown）')
    ext.add_argument('--ratio', type=float, default=0.15, help='\u62bd\u6837\u6bd4\u4f8b，\u9ed8\u8ba4 0.15')
    ext.add_argument('--seed', type=int, default=None, help='\u968f\u673a\u79cd\u5b50（\u53ef\u9009，\u7528\u4e8e\u590d\u73b0）')
    ext.add_argument('--dry-run', action='store_true', help='\u53ea\u6253\u5370，\u4e0d\u8f93\u51fa JSON')

    # verdict
    vrd = sub.add_parser('verdict', help='\u6839\u636e\u6838\u9a8c\u7ed3\u679c\u8f93\u51fa\u51c6\u51fa/\u6253\u56de\u5224\u51b3')
    vrd.add_argument('--results', required=True, help='JSON \u6570\u7ec4，\u542b fetched_value \u7b49\u5b57\u6bb5')
    vrd.add_argument('--report', default='', help='\u62a5\u544a\u540d\u79f0（\u53ef\u9009，\u7528\u4e8e\u663e\u793a）')
    vrd.add_argument('--output-json', action='store_true', help='\u5c06\u5224\u51b3\u7ed3\u679c\u4ee5 JSON \u8f93\u51fa\u5230 stdout')

    args = parser.parse_args()

    if args.command == 'extract':
        if not os.path.exists(args.report):
            print(f'❌ \u6587\u4ef6\u4e0d\u5b58\u5728: {args.report}', file=sys.stderr)
            sys.exit(1)

        with open(args.report, 'r', encoding='utf-8') as f:
            text = f.read()

        all_points = extract_data_points(text)
        sampled = sample_points(all_points, ratio=args.ratio, seed=args.seed)

        print('=' * 70)
        print(f'\u62a5\u544a\u6570\u636e\u62bd\u68c0\u6e05\u5355')
        print(f'\u6587\u4ef6：{args.report}')
        print(f'\u603b\u63d0\u53d6\u6570\u636e\u70b9：{len(all_points)}  |  \u62bd\u6837\u6bd4\u4f8b：{args.ratio:.0%}  |  \u62bd\u68c0\u6570\u91cf：{len(sampled)}')
        if args.seed is not None:
            print(f'\u968f\u673a\u79cd\u5b50：{args.seed}（\u53ef\u7528\u4e8e\u590d\u73b0\u540c\u4e00\u6279\u6837\u672c）')
        print('=' * 70)
        print()
        print(f'{"ID":>3}  {"\u884c\u53f7":>5}  {"\u6570\u636e\u6807\u7b7e":<35}  {"\u62a5\u544a\u503c":>12}  {"\u5355\u4f4d"}')
        print(f'{"─"*3}  {"─"*5}  {"─"*35}  {"─"*12}  {"─"*6}')
        for p in sampled:
            print(f'{p["id"]:>3}  {p["line_number"]:>5}  {p["label"][:35]:<35}  {p["reported_value"]:>12.2f}  {p["unit"]}')
        print()
        print('↑ \u8bf7\u5bf9\u4e0a\u8ff0\u6bcf\u4e2a\u6570\u636e\u70b9，\u4ece\u4ee5\u4e0b\u4fe1\u6e90\u53d6\u6570，\u586b\u5165 fetched_value：')
        print('  \u7f8e\u80a1：macrotrends.net（\u4e3b）+ stockanalysis.com（\u526f）')
        print('  \u6e2f\u80a1：aastocks.com（\u4e3b）+ macrotrends ADR（\u526f）')
        print('  A\u80a1： eastmoney.com（\u4e3b）+ cninfo.com.cn（\u526f）')
        print()

        if not args.dry_run:
            # \u8f93\u51fa\u53ef\u586b\u5199\u7684 JSON \u6a21\u677f
            template = []
            for p in sampled:
                template.append({
                    'id': p['id'],
                    'label': p['label'],
                    'reported_value': p['reported_value'],
                    'unit': p['unit'],
                    'line_number': p['line_number'],
                    'raw_text': p['raw_text'],
                    'fetched_value': None,       # ← \u586b\u5165\u4e3b\u6765\u6e90\u6838\u9a8c\u503c
                    'fetched_source': '',        # ← \u586b\u5165\u4e3b\u6765\u6e90\u540d\u79f0
                    'fetched_value2': None,      # ← \u586b\u5165\u526f\u6765\u6e90\u6838\u9a8c\u503c（\u53ef\u9009）
                    'fetched_source2': '',       # ← \u586b\u5165\u526f\u6765\u6e90\u540d\u79f0（\u53ef\u9009）
                })
            print('\u62bd\u68c0\u6e05\u5355 JSON（\u586b\u5165 fetched_value \u540e，\u4f20\u7ed9 verdict \u547d\u4ee4）：')
            print()
            print(json.dumps(template, ensure_ascii=False, indent=2))

    elif args.command == 'verdict':
        try:
            results = json.loads(args.results)
        except json.JSONDecodeError as e:
            print(f'❌ JSON \u89e3\u6790\u5931\u8d25: {e}', file=sys.stderr)
            sys.exit(1)

        report_name = args.report or ''
        outcome = render_verdict(results, report_name=report_name)

        if args.output_json:
            print(json.dumps(outcome, ensure_ascii=False, indent=2))

        # \u975e\u96f6\u9000\u51fa\u7801\u8868\u793a\u6253\u56de，\u65b9\u4fbf CI/\u811a\u672c\u5224\u65ad
        sys.exit(0 if outcome['verdict'] == 'PASS' else 1)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
