#!/usr/bin/env python3
"""Report Audit Tool for AI Berkshire.

数据抽检工具：从研究报告中抽取15%的财务数据点，与可靠信源比对，
通过则准出，不通过则打回并说明原因。

Zero external dependencies — uses only Python stdlib.
Requires Python >= 3.7.

工作流程（三步）：
  Step 1 — 提取数据点，随机抽样15%：
    python3 tools/report_audit.py extract --report reports/xxx.md

  Step 2 — Claude 对抽检清单中的每个数据点，从两个独立可靠信源
            （macrotrends/stockanalysis/aastocks/eastmoney 等）取数，
            填入两组 fetched_value / fetched_source

  Step 3 — 输入核验结果，输出准出/打回判决：
    python3 tools/report_audit.py verdict --results '[...]'

  一步完成（仅提取+打印抽检清单，不做网络验证）：
    python3 tools/report_audit.py extract --report reports/xxx.md --dry-run
"""

import argparse
import json
import math
import os
import re
import sys
from contextlib import redirect_stdout
from decimal import Decimal, Context, ROUND_HALF_EVEN, InvalidOperation
from random import Random

_CTX = Context(prec=28, rounding=ROUND_HALF_EVEN)

# ---------------------------------------------------------------------------
# 数据点提取：从 Markdown 报告中识别财务数字
# ---------------------------------------------------------------------------

# 匹配模式：数字 + 单位，前面有上下文标签
# 例：收入：1,239亿元、PE 18.8x、毛利率 56%、市值 ~$5,670亿
_NUMBER_RE = r'[+\-−]?(?:\d[\d,，]*(?:\.\d*)?|\.\d+)'

_PATTERNS = [
    # 百分比
    (rf'({_NUMBER_RE})\s*%',                        '%',    'percent'),
    # 亿元/亿美元/亿港元
    (rf'({_NUMBER_RE})\s*亿(元|美元|港元|RMB|USD|HKD)?', '亿',    'hundred_million'),
    # 倍数 PE/PB/PS
    (rf'({_NUMBER_RE})\s*[xX倍]',                   'x',    'multiple'),
    # 万亿
    (rf'({_NUMBER_RE})\s*万亿',                      '万亿', 'trillion'),
    # 美元绝对值（B/T）
    (rf'\$\s*({_NUMBER_RE})\s*([BMT亿])',             '$',    'usd_abs'),
    # 纯整数（如市值、收入、用户数等，出现在表格 | 里）
    (rf'\|\s*[~约]?\$?({_NUMBER_RE})\s*\|',          '',     'table_num'),
]

_LABEL_RE = re.compile(
    rf'(?P<label>[^\|\n：:]{{2,25}})[：:\s]+[~约]?\$?(?P<num>{_NUMBER_RE})\s*(?P<unit>亿[元美港]?元?|万亿|[xX倍]|%|[BMT])?'
)

_TABLE_ROW_RE = re.compile(
    rf'\|\s*(?P<label>[^|]{{1,40}})\s*\|\s*[~约]?\$?(?P<num>{_NUMBER_RE})\s*(?P<unit>亿[元美港]?元?|万亿|[xX倍]|%|[BMT])?\s*\|'
)


def _clean_num(s: str) -> float:
    """把带逗号、中文逗号的数字字符串转为 float。"""
    s = s.replace(',', '').replace('，', '').replace('−', '-').strip()
    try:
        return float(s)
    except ValueError:
        return None


def _is_valid_label(label: str) -> bool:
    """判断标签是否是有意义的财务字段名，过滤噪声。"""
    label = label.strip()
    # 太短
    if len(label) < 2:
        return False
    # 纯数字或纯年份
    if re.fullmatch(r'[\d\s年季度Q]+', label):
        return False
    # 以符号/markdown标记开头
    if re.match(r'^[+\-\*#\|~\$>_`]', label):
        return False
    # 含有 markdown 粗体/代码标记
    if '**' in label or '`' in label or '__' in label:
        return False
    # 标签含有纯增速符号（如 +56%、-13% 单独作标签）
    if re.fullmatch(r'[+\-]?\d+(\.\d+)?%', label):
        return False
    # 常见无意义标签
    _SKIP = {'来源', 'sources', 'source', '说明', '注意', '备注', '数据来源',
             'n/a', '—', '-', '/', '合计', 'total', '单位', '趋势'}
    if label.lower() in _SKIP:
        return False
    return True


# 两列表格行：| 标签 | 数值 unit |（专为财务报告的 KV 表设计）
_KV_TABLE_RE = re.compile(
    rf'^\|\s*(?P<label>[^|*\n]{{2,40}}?)\s*\|\s*[~约]?\$?(?P<num>{_NUMBER_RE})\s*'
    rf'(?P<unit>亿[元美港]?元?|万亿|[xX倍]|%|[BMT亿])?\s*[\|（\(]'
)

# 带标签的 KV 行：标签：数值 单位
_KV_LABEL_RE = re.compile(
    rf'(?P<label>[\u4e00-\u9fa5A-Za-z][^\|\n：:*]{{1,30}})[：:]\s*[~约]?\$?'
    rf'(?P<num>{_NUMBER_RE})\s*(?P<unit>亿[元美港]?元?|万亿|[xX倍]|%|[BMT])?'
)


def _split_md_table_cells(line: str, formatting_chars: str) -> list:
    """Split a pipe table row without collapsing positional empty cells."""
    cells = line.split('|')
    if cells and not cells[0].strip():
        cells = cells[1:]
    if cells and not cells[-1].strip():
        cells = cells[:-1]
    return [cell.strip().strip(formatting_chars).strip() for cell in cells]


def _parse_md_tables(lines: list) -> list:
    """解析 Markdown 中所有表格，返回 (row_label, col_header, value, unit, lineno, raw) 列表。"""
    results = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # 检测表头行（含 | 且不是分隔行）
        if '|' in line and not re.match(r'^\|[\-\s\|:]+\|$', line):
            headers_raw = _split_md_table_cells(line, '*_')
            # 下一行应是分隔行
            if i + 1 < len(lines) and re.match(r'^\|[\-\s\|:]+\|$', lines[i+1].strip()):
                i += 2  # 跳过分隔行
                # 读数据行
                while i < len(lines):
                    dline = lines[i].strip()
                    if not dline or not dline.startswith('|'):
                        break
                    cells = _split_md_table_cells(dline, '*_~')
                    if len(cells) < 2:
                        i += 1
                        continue
                    row_label = cells[0]
                    for col_idx, cell in enumerate(cells[1:], start=1):
                        col_header = headers_raw[col_idx] if col_idx < len(headers_raw) else f'列{col_idx}'
                        # 提取 cell 中的数字+单位
                        m = re.search(
                            rf'[~约]?\$?({_NUMBER_RE})\s*(亿[元美港]?元?|万亿|[xX倍]|%|[BMT])?',
                            cell
                        )
                        if m:
                            val = _clean_num(m.group(1))
                            unit = (m.group(2) or '').strip()
                            if val is not None and abs(val) < 1e15:
                                results.append((row_label, col_header, val, unit, i + 1, dline))
                    i += 1
                continue
        i += 1
    return results


def extract_data_points(md_text: str) -> list:
    """从 Markdown 报告中提取所有可识别的财务数据点。

    覆盖三类结构：
      1. 多列 Markdown 表格（最主要的来源）：(行标签 + 列标题) → 数值
      2. 带冒号的 KV 行：标签：数值 单位
      3. 加粗数字行：**数值** 单位

    返回 list of dict：
      {id, label, reported_value, unit, raw_text, line_number}
    """
    points = []
    seen = set()

    def _add(label, val, unit, lineno, raw):
        label = re.sub(r'[\*_`]+', '', label).strip()
        if not _is_valid_label(label):
            return
        if val is None or abs(val) > 1e15:
            return
        # 过滤纯年份/季度
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

    # --- 1. 多列表格 ---
    for row_label, col_header, val, unit, lineno, raw in _parse_md_tables(lines):
        # 跳过无意义行标签
        if not _is_valid_label(row_label):
            continue
        # 跳过无意义列标题（YoY增速列单独标注，不作为待核验数据）
        if col_header.upper() in ('YOY', 'YOY增速', '增速', '同比', '变化', '趋势', '说明', '备注'):
            continue
        # label = "行标签 · 列标题"（若列标题是行标签的补充）
        if col_header and col_header != row_label:
            label = f"{row_label} · {col_header}"
        else:
            label = row_label
        _add(label, val, unit, lineno, raw)

    # --- 2. KV 冒号行 ---
    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            continue
        if in_code or stripped.startswith('> ') or re.match(r'^#{1,6}\s', stripped):
            continue
        if '|' in stripped:
            continue  # 表格已在上面处理

        for m in _KV_LABEL_RE.finditer(stripped):
            label = m.group('label')
            val = _clean_num(m.group('num'))
            unit = (m.group('unit') or '').strip()
            _add(label, val, unit, lineno, stripped)

    return points


def sample_points(points: list, ratio=Decimal('0.15'), seed: int = None) -> list:
    """随机抽取 ratio 比例的数据点，最少 3 个，最多 30 个。"""
    ratio = ratio if isinstance(ratio, Decimal) else Decimal(str(ratio))
    n = max(3, min(30, math.ceil(Decimal(len(points)) * ratio)))
    n = min(n, len(points))
    rng = Random(seed)
    sampled = rng.sample(points, n)
    # 按行号排序，方便人工比对
    return sorted(sampled, key=lambda p: p['line_number'])


# ---------------------------------------------------------------------------
# 准出/打回判决
# ---------------------------------------------------------------------------

_TOLERANCE = Decimal('0.01')   # 1% 容差


def _as_decimal(value) -> Decimal:
    """Convert a JSON-compatible number to a finite Decimal."""
    if isinstance(value, bool) or value is None:
        raise InvalidOperation('not a number')
    result = value if isinstance(value, Decimal) else Decimal(str(value))
    if not result.is_finite():
        raise InvalidOperation('number must be finite')
    return result


def _pct_diff(reported, fetched) -> Decimal:
    """相对偏差 (absolute)。"""
    reported = _as_decimal(reported)
    fetched = _as_decimal(fetched)
    if reported == 0:
        return Decimal('0') if fetched == 0 else Decimal('Infinity')
    return abs(reported - fetched) / abs(reported)


def _json_number(value):
    """Return a JSON-serializable representation of a Decimal."""
    if value is None:
        return None
    value = value if isinstance(value, Decimal) else Decimal(str(value))
    if not value.is_finite():
        return str(value)
    if abs(value.adjusted()) > 308:
        return str(value)
    if value == value.to_integral_value():
        return int(value)
    return float(value)


def _percent_number(diff):
    """Render a ratio as a percentage rounded to two decimal places."""
    if diff is None:
        return None
    percentage = diff * Decimal('100')
    if percentage.is_finite():
        try:
            percentage = percentage.quantize(Decimal('0.01'), context=_CTX)
        except InvalidOperation:
            pass
    return _json_number(percentage)


def _source_name(value) -> str:
    """Normalize a source name; blank/placeholder values are unverified."""
    if not isinstance(value, str):
        return ''
    source = value.strip()
    placeholder_key = re.sub(r'\s+', ' ', source).casefold()
    if placeholder_key in {
        '', '?', '-', '—', 'n/a', 'none', 'null', 'unknown', 'tbd',
        'pending', 'not available', 'not provided', 'unverified',
        '未提供', '不明', '未验证', '未驗證', '未検証', '未确认', '未確認',
        '待确认', '待確認', '待核验', '待核驗',
    }:
        return ''
    return source


def _independence_key(source: str) -> str:
    return re.sub(r'\s+', ' ', source).strip().casefold()


def render_verdict(results: list, report_name: str = "") -> dict:
    """
    根据核验结果输出准出/打回判决。

    results: list of dict，每项包含：
      - id, label, reported_value, unit, fetched_value, fetched_source
      - fetched_value2, fetched_source2   ← 必需的独立第二来源

    返回：
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
    RESET = '\033[0m'

    print('=' * 70)
    print(f'{BOLD}报告数据抽检 — 准出/打回判决{RESET}')
    if report_name:
        print(f'报告：{report_name}')
    print('=' * 70)
    print()

    valid_results = isinstance(results, list)
    audit_items = results if valid_results else []
    fail_items = []
    pass_count = 0

    if not valid_results:
        print(f'  {RED}❌ 核验结果必须是 JSON 数组。{RESET}')
    elif not audit_items:
        print(f'  {RED}❌ 核验结果为空；没有数据点可供准出判断。{RESET}')

    for index, item in enumerate(audit_items, start=1):
        if not isinstance(item, dict):
            fail_items.append({
                'id': index,
                'label': '?',
                'reported': None,
                'unit': '',
                'fetched': None,
                'source': '',
                'fetched2': None,
                'source2': '',
                'diff1_pct': None,
                'diff2_pct': None,
                'reason': '核验项必须是 JSON 对象',
                'raw_text': '',
                'line_number': 0,
            })
            print(f'  {RED}❌ 不通过{RESET} [{index:>2}] ?  →  核验项必须是 JSON 对象')
            continue

        item_id = item.get('id', index)
        label = str(item.get('label', '?'))
        unit = str(item.get('unit', ''))
        fetched_raw = item.get('fetched_value')
        fetched2_raw = item.get('fetched_value2')
        source = _source_name(item.get('fetched_source'))
        source2 = _source_name(item.get('fetched_source2'))
        reasons = []
        reported = None
        fetched = None
        fetched2 = None
        diff1 = None
        diff2 = None

        try:
            if 'reported_value' not in item:
                raise InvalidOperation('missing reported value')
            reported = _as_decimal(item['reported_value'])
        except (InvalidOperation, ValueError, TypeError):
            reasons.append('报告值缺失或不是有限数字')

        try:
            fetched = _as_decimal(fetched_raw)
        except (InvalidOperation, ValueError, TypeError):
            reasons.append('主来源核验值缺失或不是有限数字')

        try:
            fetched2 = _as_decimal(fetched2_raw)
        except (InvalidOperation, ValueError, TypeError):
            reasons.append('第二来源核验值缺失或不是有限数字')

        if not source:
            reasons.append('主来源名称缺失')
        if not source2:
            reasons.append('第二来源名称缺失')
        if source and source2 and _independence_key(source) == _independence_key(source2):
            reasons.append('两个核验来源不独立（来源名称相同）')

        if reported is not None and fetched is not None:
            diff1 = _pct_diff(reported, fetched)
            if diff1 > _TOLERANCE:
                reasons.append(f'主来源偏差 {_percent_number(diff1)}% 超过 1%')
        if reported is not None and fetched2 is not None:
            diff2 = _pct_diff(reported, fetched2)
            if diff2 > _TOLERANCE:
                reasons.append(f'第二来源偏差 {_percent_number(diff2)}% 超过 1%')

        if not reasons and diff1 is not None and diff2 is not None:
            pass_count += 1
            status = f'{GREEN}✅ 通过{RESET}'
        else:
            status = f'{RED}❌ 不通过{RESET}'
            fail_items.append({
                'id': item_id,
                'label': label,
                'reported': _json_number(reported),
                'unit': unit,
                'fetched': _json_number(fetched),
                'source': source,
                'fetched2': _json_number(fetched2),
                'source2': source2,
                'diff1_pct': _percent_number(diff1),
                'diff2_pct': _percent_number(diff2),
                'reason': '；'.join(reasons),
                'raw_text': item.get('raw_text', ''),
                'line_number': item.get('line_number', 0),
            })

        reported_display = f'{reported:.2f}' if reported is not None else '?'
        details = []
        if fetched is not None:
            details.append(
                f'{source or "[来源缺失]"}: {fetched:.2f}'
                + (f' (偏差 {diff1 * 100:.2f}%)' if diff1 is not None else '')
            )
        if fetched2 is not None:
            details.append(
                f'{source2 or "[来源缺失]"}: {fetched2:.2f}'
                + (f' (偏差 {diff2 * 100:.2f}%)' if diff2 is not None else '')
            )
        detail = '  |  '.join(details) if details else '未提供有效核验值'
        if reasons:
            detail += f'  |  原因: {"；".join(reasons)}'

        print(f'  {status} [{str(item_id):>2}] {label[:35]:35s}  报告: {reported_display:>12} {unit}')
        print(f'              {" " * 38}{detail}')

    print()
    print('-' * 70)

    total = len(audit_items)
    fail_count = len(fail_items)
    warn_count = 0
    warn_items = []

    print(f'  抽检总数: {total}  |  通过: {GREEN}{pass_count}{RESET}  |  不通过: {RED}{fail_count}{RESET}')
    print()

    if valid_results and total > 0 and fail_count == 0 and pass_count == total:
        print(f'{BOLD}{GREEN}【准出】所有抽检数据均由两个独立来源核验，且双方偏差均不超过1%。{RESET}')
        verdict = 'PASS'
    else:
        if total == 0:
            print(f'{BOLD}{RED}【打回】没有完整核验的数据点，报告不可发布。{RESET}')
        else:
            print(f'{BOLD}{RED}【打回】{fail_count} 个数据点核验不通过，报告需修正后重审。{RESET}')
        print()
        if fail_items:
            print(f'{BOLD}打回原因：{RESET}')
        for fi in fail_items:
            print(f'  ❌ 第 {fi["line_number"]} 行 | {fi["label"]}')
            print(f'     报告值：{fi["reported"]} {fi["unit"]}')
            if fi.get('fetched') is not None:
                print(f'     {fi["source"] or "[来源缺失]"}：{fi["fetched"]}  （偏差 {fi["diff1_pct"]}%）')
            if fi.get('fetched2') is not None:
                print(f'     {fi["source2"] or "[来源缺失]"}：{fi["fetched2"]}  （偏差 {fi["diff2_pct"]}%）')
            print(f'     原因：{fi["reason"]}')
            print(f'     原文：{fi["raw_text"][:80]}')
            print()
        verdict = 'FAIL'

    print('=' * 70)

    if verdict == 'PASS':
        summary = f'PASS: {pass_count}/{total} 个数据点通过双来源核验'
    elif total == 0:
        summary = 'FAIL: 核验结果为空或格式无效'
    else:
        summary = f'FAIL: {fail_count}/{total} 个数据点未满足双来源1%容差要求'

    return {
        'verdict': verdict,
        'pass_count': pass_count,
        'warn_count': warn_count,
        'fail_count': fail_count,
        'total': total,
        'fail_items': fail_items,
        'warn_items': warn_items,
        'summary': summary,
    }


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Report Audit Tool — 研究报告数据抽检工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
工作流程：

  Step 1 — 提取数据点并随机抽样 15%，输出抽检清单：
    python3 tools/report_audit.py extract --report reports/腾讯/腾讯-research-20260408.md

  Step 2 — Claude 对清单中每个数据点，从可靠信源取数，
            填入 fetched_value / fetched_source / fetched_value2 / fetched_source2
            （两个来源均为必填，且来源名称必须不同）

  Step 3 — 输入核验结果，输出准出/打回判决：
    python3 tools/report_audit.py verdict --results '[
      {"id":1,"label":"营业收入","reported_value":7518,"unit":"亿","fetched_value":7518,"fetched_source":"macrotrends","fetched_value2":7500,"fetched_source2":"stockanalysis"},
      ...
    ]'

  一步预览（只打印抽检清单，不核验）：
    python3 tools/report_audit.py extract --report reports/xxx.md --dry-run

  指定抽样比例（默认0.15）：
    python3 tools/report_audit.py extract --report reports/xxx.md --ratio 0.20

  固定随机种子（复现同一批样本）：
    python3 tools/report_audit.py extract --report reports/xxx.md --seed 42
        """)

    sub = parser.add_subparsers(dest='command')

    # extract
    ext = sub.add_parser('extract', help='从报告提取数据点并随机抽样')
    ext.add_argument('--report', required=True, help='报告文件路径（Markdown）')
    ext.add_argument('--ratio', default='0.15', help='抽样比例，默认 0.15')
    ext.add_argument('--seed', default=None, help='随机种子（可选，用于复现）')
    ext.add_argument('--dry-run', action='store_true', help='只打印，不输出 JSON')

    # verdict
    vrd = sub.add_parser('verdict', help='根据核验结果输出准出/打回判决')
    vrd.add_argument('--results', required=True, help='JSON 数组，含 fetched_value 等字段')
    vrd.add_argument('--report', default='', help='报告名称（可选，用于显示）')
    vrd.add_argument('--output-json', action='store_true', help='将判决结果以 JSON 输出到 stdout')

    args = parser.parse_args()

    if args.command == 'extract':
        try:
            ratio = _as_decimal(args.ratio)
        except (InvalidOperation, ValueError, TypeError):
            parser.error(f'--ratio 必须是有限数字: {args.ratio}')
        if ratio < 0:
            parser.error(f'--ratio 不能为负数: {args.ratio}')

        seed = None
        if args.seed is not None:
            try:
                seed_decimal = _as_decimal(args.seed)
            except (InvalidOperation, ValueError, TypeError):
                parser.error(f'--seed 必须是整数: {args.seed}')
            if seed_decimal != seed_decimal.to_integral_value():
                parser.error(f'--seed 必须是整数: {args.seed}')
            seed = int(seed_decimal)

        if not os.path.exists(args.report):
            print(f'❌ 文件不存在: {args.report}', file=sys.stderr)
            sys.exit(1)

        with open(args.report, 'r', encoding='utf-8') as f:
            text = f.read()

        all_points = extract_data_points(text)
        sampled = sample_points(all_points, ratio=ratio, seed=seed)

        print('=' * 70)
        print(f'报告数据抽检清单')
        print(f'文件：{args.report}')
        print(f'总提取数据点：{len(all_points)}  |  抽样比例：{ratio:.0%}  |  抽检数量：{len(sampled)}')
        if seed is not None:
            print(f'随机种子：{seed}（可用于复现同一批样本）')
        print('=' * 70)
        print()
        print(f'{"ID":>3}  {"行号":>5}  {"数据标签":<35}  {"报告值":>12}  {"单位"}')
        print(f'{"─"*3}  {"─"*5}  {"─"*35}  {"─"*12}  {"─"*6}')
        for p in sampled:
            print(f'{p["id"]:>3}  {p["line_number"]:>5}  {p["label"][:35]:<35}  {p["reported_value"]:>12.2f}  {p["unit"]}')
        print()
        print('↑ 请对上述每个数据点，从两个独立信源取数，填入两组 fetched_value / fetched_source：')
        print('  美股：macrotrends.net（主）+ stockanalysis.com（副）')
        print('  港股：aastocks.com（主）+ macrotrends ADR（副）')
        print('  A股： eastmoney.com（主）+ cninfo.com.cn（副）')
        print()

        if not args.dry_run:
            # 输出可填写的 JSON 模板
            template = []
            for p in sampled:
                template.append({
                    'id': p['id'],
                    'label': p['label'],
                    'reported_value': p['reported_value'],
                    'unit': p['unit'],
                    'line_number': p['line_number'],
                    'raw_text': p['raw_text'],
                    'fetched_value': None,       # ← 填入主来源核验值
                    'fetched_source': '',        # ← 填入主来源名称
                    'fetched_value2': None,      # ← 填入独立副来源核验值（必填）
                    'fetched_source2': '',       # ← 填入独立副来源名称（必填）
                })
            print('抽检清单 JSON（填入两组核验值与来源后，传给 verdict 命令）：')
            print()
            print(json.dumps(template, ensure_ascii=False, indent=2))

    elif args.command == 'verdict':
        try:
            results = json.loads(
                args.results, parse_float=Decimal
            )
        except (json.JSONDecodeError, InvalidOperation) as e:
            print(f'❌ JSON 解析失败: {e}', file=sys.stderr)
            sys.exit(1)

        if args.output_json:
            # Keep stdout machine-readable. Human-oriented diagnostics remain
            # available on stderr when JSON output is requested.
            with redirect_stdout(sys.stderr):
                outcome = render_verdict(results, report_name=args.report or '')
            print(json.dumps(outcome, ensure_ascii=False, indent=2))
        else:
            outcome = render_verdict(results, report_name=args.report or '')

        # 非零退出码表示打回，方便 CI/脚本判断
        sys.exit(0 if outcome['verdict'] == 'PASS' else 1)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
