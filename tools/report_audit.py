#!/usr/bin/env python3
"""Report Audit Tool for AI Berkshire.

数据抽检工具：从研究报告中抽取15%的财务数据点，与可靠信源比对，
通过则准出，不通过则打回并说明原因。

Zero external dependencies — uses only Python stdlib.
Requires Python >= 3.7.

工作流程（三步）：
  Step 1 — 提取数据点，随机抽样15%：
    python3 tools/report_audit.py extract --report reports/xxx.md

  Step 2 — Claude 对抽检清单中的每个数据点，从可靠信源（macrotrends/
            stockanalysis/aastocks/eastmoney）取数，填入 fetched_value

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
from decimal import Decimal, Context, ROUND_HALF_EVEN
from random import Random

_CTX = Context(prec=28, rounding=ROUND_HALF_EVEN)

# ---------------------------------------------------------------------------
# 数据点提取：从 Markdown 报告中识别财务数字
# ---------------------------------------------------------------------------

# 匹配模式：数字 + 单位，前面有上下文标签
# 例：收入：1,239亿元、PE 18.8x、毛利率 56%、市值 ~$5,670亿
_PATTERNS = [
    # 百分比
    (r'([\d,，\.]+)\s*%',                        '%',    'percent'),
    # 亿元/亿美元/亿港元
    (r'([\d,，\.]+)\s*亿(元|美元|港元|RMB|USD|HKD)?', '亿',    'hundred_million'),
    # 倍数 PE/PB/PS
    (r'([\d,，\.]+)\s*[xX倍]',                   'x',    'multiple'),
    # 万亿
    (r'([\d,，\.]+)\s*万亿',                      '万亿', 'trillion'),
    # 美元绝对值（B/T）
    (r'\$\s*([\d,，\.]+)\s*([BMT亿])',             '$',    'usd_abs'),
    # 纯整数（如市值、收入、用户数等，出现在表格 | 里）
    (r'\|\s*[~约]?\$?([\d,，\.]+)\s*\|',          '',     'table_num'),
]

_LABEL_RE = re.compile(
    r'(?P<label>[^\|\n：:]{2,25})[：:\s]+[~约]?\$?(?P<num>[\d,，\.]+)\s*(?P<unit>亿[元美港]?元?|万亿|[xX倍]|%|[BMT])?'
)

_TABLE_ROW_RE = re.compile(
    r'\|\s*(?P<label>[^|]{1,40})\s*\|\s*[~约]?\$?(?P<num>[\d,，\.]+)\s*(?P<unit>亿[元美港]?元?|万亿|[xX倍]|%|[BMT])?\s*\|'
)


def _clean_num(s: str) -> float:
    """把带逗号、中文逗号的数字字符串转为 float。"""
    s = s.replace(',', '').replace('，', '').strip()
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
    r'^\|\s*(?P<label>[^|*\n]{2,40}?)\s*\|\s*[~约]?\$?(?P<num>[\d,，\.]+)\s*'
    r'(?P<unit>亿[元美港]?元?|万亿|[xX倍]|%|[BMT亿])?\s*[\|（\(]'
)

# 带标签的 KV 行：标签：数值 单位
_KV_LABEL_RE = re.compile(
    r'(?P<label>[\u4e00-\u9fa5A-Za-z][^\|\n：:*]{1,30})[：:]\s*[~约]?\$?'
    r'(?P<num>[\d,，\.]+)\s*(?P<unit>亿[元美港]?元?|万亿|[xX倍]|%|[BMT])?'
)


def _parse_md_tables(lines: list) -> list:
    """解析 Markdown 中所有表格，返回 (row_label, col_header, value, unit, lineno, raw) 列表。"""
    results = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # 检测表头行（含 | 且不是分隔行）
        if '|' in line and not re.match(r'^\|[\-\s\|:]+\|$', line):
            headers_raw = [h.strip().strip('*_').strip() for h in line.split('|')]
            headers_raw = [h for h in headers_raw if h]
            # 下一行应是分隔行
            if i + 1 < len(lines) and re.match(r'^\|[\-\s\|:]+\|$', lines[i+1].strip()):
                i += 2  # 跳过分隔行
                # 读数据行
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
                        col_header = headers_raw[col_idx] if col_idx < len(headers_raw) else f'列{col_idx}'
                        # 提取 cell 中的数字+单位
                        m = re.search(
                            r'[~约]?\$?([\d,，\.]+)\s*(亿[元美港]?元?|万亿|[xX倍]|%|[BMT])?',
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
        if val is None or val == 0 or val > 1e15:
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


def sample_points(points: list, ratio: float = 0.15, seed: int = None) -> list:
    """随机抽取 ratio 比例的数据点，最少 3 个，最多 30 个。"""
    n = max(3, min(30, math.ceil(len(points) * ratio)))
    n = min(n, len(points))
    rng = Random(seed)
    sampled = rng.sample(points, n)
    # 按行号排序，方便人工比对
    return sorted(sampled, key=lambda p: p['line_number'])


# ---------------------------------------------------------------------------
# 准出/打回判决
# ---------------------------------------------------------------------------

_TOLERANCE = 0.01   # 1% 容差


def _pct_diff(reported: float, fetched: float) -> float:
    """相对偏差 (absolute)。"""
    if reported == 0:
        return 0.0 if fetched == 0 else float('inf')
    return abs(reported - fetched) / abs(reported)


def render_verdict(results: list, report_name: str = "") -> dict:
    """
    根据核验结果输出准出/打回判决。

    results: list of dict，每项包含：
      - id, label, reported_value, unit, fetched_value, fetched_source
      - (可选) fetched_value2, fetched_source2   ← 第二来源

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
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    print('=' * 70)
    print(f'{BOLD}报告数据抽检 — 准出/打回判决{RESET}')
    if report_name:
        print(f'报告：{report_name}')
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

        # --- 主来源比对 ---
        if fetched is None:
            # 没有提供核验值 → 跳过（不计入通过/失败）
            print(f'  ⬜ [{item["id"]:>2}] {label[:35]:35s} {reported:>12.2f} {unit}  →  [未提供核验值，跳过]')
            continue

        fetched = float(fetched)
        diff1 = _pct_diff(reported, fetched)

        # --- 第二来源比对（如有）---
        diff2 = None
        if fetched2 is not None:
            fetched2 = float(fetched2)
            diff2 = _pct_diff(reported, fetched2)

        # 判断
        pass1 = diff1 <= _TOLERANCE
        pass2 = (diff2 is None) or (diff2 <= _TOLERANCE)

        if pass1 and pass2:
            status = f'{GREEN}✅ 通过{RESET}'
            detail = f'{source}: {fetched:.2f} (偏差 {diff1*100:.2f}%)'
            if diff2 is not None:
                detail += f'  |  {source2}: {fetched2:.2f} (偏差 {diff2*100:.2f}%)'
        elif not pass1 and not pass2:
            status = f'{RED}❌ 不通过{RESET}'
            detail = f'{source}: {fetched:.2f} (偏差 {diff1*100:.2f}%)'
            if diff2 is not None:
                detail += f'  |  {source2}: {fetched2:.2f} (偏差 {diff2*100:.2f}%)'
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
            # 一个来源通过，一个不通过 → 警告，不计入失败
            status = f'{YELLOW}⚠️  警告{RESET}'
            detail = f'{source}: {fetched:.2f} (偏差 {diff1*100:.2f}%)'
            if diff2 is not None:
                detail += f'  |  {source2}: {fetched2:.2f} (偏差 {diff2*100:.2f}%)'
            warn_items.append({
                'id': item['id'], 'label': label,
                'reported': reported, 'unit': unit,
                'diff1_pct': round(diff1 * 100, 2),
                'diff2_pct': round(diff2 * 100, 2) if diff2 is not None else None,
            })

        print(f'  {status} [{item["id"]:>2}] {label[:35]:35s}  报告: {reported:>12.2f} {unit}')
        print(f'              {" " * 38}{detail}')

    print()
    print('-' * 70)

    total = len([r for r in results if r.get('fetched_value') is not None])
    fail_count = len(fail_items)
    warn_count = len(warn_items)
    pass_count = total - fail_count - warn_count

    print(f'  抽检总数: {total}  |  通过: {GREEN}{pass_count}{RESET}  |  警告: {YELLOW}{warn_count}{RESET}  |  不通过: {RED}{fail_count}{RESET}')
    print()

    if fail_count == 0:
        print(f'{BOLD}{GREEN}【准出】所有抽检数据通过，报告可发布。{RESET}')
        verdict = 'PASS'
    else:
        print(f'{BOLD}{RED}【打回】{fail_count} 个数据点核验不通过，报告需修正后重审。{RESET}')
        print()
        print(f'{BOLD}打回原因：{RESET}')
        for fi in fail_items:
            print(f'  ❌ 第 {fi["line_number"]} 行 | {fi["label"]}')
            print(f'     报告值：{fi["reported"]} {fi["unit"]}')
            print(f'     {fi["source"]}：{fi["fetched"]}  （偏差 {fi["diff1_pct"]}%）')
            if fi.get('fetched2') is not None:
                print(f'     {fi["source2"]}：{fi["fetched2"]}  （偏差 {fi["diff2_pct"]}%）')
            print(f'     原文：{fi["raw_text"][:80]}')
            print()
        verdict = 'FAIL'

    if warn_count > 0:
        print(f'{YELLOW}注意：{warn_count} 个数据点两来源结果不一致（超过1%），可能是口径差异（GAAP/Non-GAAP或汇率），请人工复核。{RESET}')
        for wi in warn_items:
            print(f'  ⚠️  {wi["label"]}  报告:{wi["reported"]} {wi["unit"]}  偏差: {wi["diff1_pct"]}% / {wi["diff2_pct"]}%')

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
# 来源充分性检查（Computational Sensor）
#   规则来自 CLAUDE.md：「数据必须标注来源，关键数据至少2个来源交叉验证」
#   纯静态扫描，无网络、无 LLM —— 把 prompt 规则变成确定性闸门。
# ---------------------------------------------------------------------------

# 受信信源识别表：(正则, 规范名)。命中即记为一个「独立来源」。
_SOURCE_PATTERNS = [
    (r'macrotrends',                         'macrotrends'),
    (r'stockanalysis',                       'stockanalysis'),
    (r'aastocks|阿斯达克',                     'aastocks'),
    (r'eastmoney|东方财富',                    'eastmoney'),
    (r'cninfo|巨潮',                          'cninfo'),
    (r'雪球|xueqiu',                          'xueqiu'),
    (r'\bwind\b|万得',                        'wind'),
    (r'morningstar|晨星',                     'morningstar'),
    (r'bloomberg|彭博',                       'bloomberg'),
    (r'sec\.gov|10-?K|10-?Q|20-?F|8-?K',      'SEC备案'),
    (r'年报|季报|中报|财报|公司公告|业绩公告',    '公司财报/公告'),
    (r'gurufocus',                           'gurufocus'),
    (r'tikr',                                'tikr'),
    (r'ycharts',                             'ycharts'),
    (r'wsj|华尔街日报',                        'wsj'),
    (r'reuters|路透',                         'reuters'),
]

# 「已标注来源」的通用标记（满足 CLAUDE.md「数据必须标注来源」）
_CITATION_MARKER_RE = re.compile(
    r'来源|數據來源|数据来源|资料来源|資料來源|出处|出處|引用|参考|參考|'
    r'\bsource[s]?\b|https?://',
    re.IGNORECASE,
)


def check_sources(md_text: str, min_sources: int = 2) -> dict:
    """静态检查报告的来源充分性。

    两条确定性规则：
      R1 报告必须含「来源标注」标记（来源/数据来源/Source/URL 之一）。
      R2 必须出现 >= min_sources 个相互独立的受信信源。

    返回 {'verdict': 'PASS'|'FAIL', 'found_sources': [...], 'has_marker': bool,
          'min_sources': int, 'reasons': [...]}。
    纯计算、无副作用，便于在 pre-commit / CI 中调用。
    """
    found = []
    for pat, name in _SOURCE_PATTERNS:
        if re.search(pat, md_text, re.IGNORECASE):
            found.append(name)
    found = sorted(set(found))

    has_marker = bool(_CITATION_MARKER_RE.search(md_text))

    reasons = []
    if not has_marker:
        reasons.append('未发现任何来源标注标记（来源/数据来源/Source/URL）')
    if len(found) < min_sources:
        reasons.append(
            f'仅识别到 {len(found)} 个独立信源（要求 >= {min_sources}）：'
            f'{found if found else "无"}'
        )

    verdict = 'PASS' if not reasons else 'FAIL'
    return {
        'verdict': verdict,
        'found_sources': found,
        'has_marker': has_marker,
        'min_sources': min_sources,
        'reasons': reasons,
    }


def render_sources_report(result: dict, report_name: str = '') -> None:
    BOLD, RED, GREEN, RESET = '\033[1m', '\033[91m', '\033[92m', '\033[0m'
    print('=' * 70)
    print(f'{BOLD}来源充分性检查（Computational Sensor）{RESET}')
    if report_name:
        print(f'报告：{report_name}')
    print('=' * 70)
    print(f'  来源标注标记：{"✅ 有" if result["has_marker"] else "❌ 无"}')
    print(f'  识别到独立信源（要求 >= {result["min_sources"]}）：'
          f'{result["found_sources"] if result["found_sources"] else "无"}')
    print('-' * 70)
    if result['verdict'] == 'PASS':
        print(f'{BOLD}{GREEN}【准出】来源充分。{RESET}')
    else:
        print(f'{BOLD}{RED}【打回】来源不达标：{RESET}')
        for r in result['reasons']:
            print(f'  ❌ {r}')
    print('=' * 70)


# ---------------------------------------------------------------------------
# 正反两面 / 估计标注检查（Inferential Sensor 的 Computational 前置过滤层）
#   规则来自 CLAUDE.md：「呈现正反两面」「估计值必须注明估计」。
#   语义判断（论点是否有「实质」反面）无法确定化 —— 本层只做廉价前置过滤：
#     · 完全没有任何反面标记的实质报告 → 高精度地标为 REVIEW（极可能一面倒）。
#     · 有反面标记 → OK（仅表示存在信号，深度仍需 Inferential 判官，见
#       docs/inferential-balance-judge.md）。
#   定位：顾问式 Sensor，默认不阻断（exit 0）。语义闸门的「批准」由人在环上做，
#   不交给概率自动 merge。--strict 时 REVIEW 退出 1，供愿意硬化的人选用。
# ---------------------------------------------------------------------------

# 反面/反方/下行论据标记（出现即视为「存在反面信号」）
_COUNTER_MARKERS = [
    '另一方面', '但另一方面', '然而', '不过', '反过来', '反面', '反方', '反驳',
    '质疑', '存疑', '争议', '风险', '下行', '看空', '空头', '隐患', '局限',
    '短板', '弱点', '缺陷', '不确定', '警惕', '反例', '悲观', 'bear case', 'bear',
]
# 「估计/不确定」标注标记
_ESTIMATE_MARKERS = ['估计', '估算', '假设', '推测', '大致', '约为', '左右']
# 预测性表述（出现这些却无估计标注 → 提示风险）
_PROJECTION_MARKERS = [
    '预计', '预测', 'CAGR', '复合增', '目标价', 'DCF', '展望', '未来三年',
    '到2027', '到2028', '到2029', '到2030',
]
# 「实质报告」信号（够长或含判断性章节，才值得检查正反两面）
_SUBSTANTIVE_MARKERS = ['判断', '结论', '估值', '投资', '逻辑', 'thesis', '评分', '★']


def check_balance(md_text: str) -> dict:
    """正反两面 / 估计标注的廉价前置过滤（确定性，无网络、无 LLM）。

    返回 {'verdict': 'OK'|'REVIEW'|'SKIP', 'counter_markers': [...],
          'has_projection': bool, 'has_estimate_label': bool, 'notes': [...]}。
    'REVIEW' = 顾问级提示「极可能一面倒，请人工或 Inferential 判官复核」，非硬性失败。
    """
    found_counter = sorted({m for m in _COUNTER_MARKERS
                            if re.search(re.escape(m), md_text, re.IGNORECASE)})
    has_projection = any(re.search(re.escape(m), md_text, re.IGNORECASE)
                         for m in _PROJECTION_MARKERS)
    has_estimate = any(m in md_text for m in _ESTIMATE_MARKERS)
    substantive = (len(md_text) > 1500
                   or any(m in md_text for m in _SUBSTANTIVE_MARKERS))

    notes = []
    if not substantive:
        verdict = 'SKIP'
        notes.append('报告过短/非判断性，跳过正反两面检查')
    elif not found_counter:
        verdict = 'REVIEW'
        notes.append('未发现任何反面/风险/下行论据标记 —— 极可能一面倒，建议复核')
    else:
        verdict = 'OK'

    if has_projection and not has_estimate:
        notes.append('含预测性表述（如预计/CAGR/目标价）却未见「估计/假设」标注')

    return {
        'verdict': verdict,
        'counter_markers': found_counter,
        'has_projection': has_projection,
        'has_estimate_label': has_estimate,
        'notes': notes,
    }


def render_balance_report(result: dict, report_name: str = '') -> None:
    BOLD, RED, GREEN, YELLOW, RESET = (
        '\033[1m', '\033[91m', '\033[92m', '\033[93m', '\033[0m')
    print('=' * 70)
    print(f'{BOLD}正反两面 / 估计标注检查（Computational 前置过滤，顾问级）{RESET}')
    if report_name:
        print(f'报告：{report_name}')
    print('=' * 70)
    print(f'  反面论据标记：{result["counter_markers"] or "无"}')
    print(f'  预测性表述：{"有" if result["has_projection"] else "无"}'
          f'  |  估计标注：{"有" if result["has_estimate_label"] else "无"}')
    print('-' * 70)
    v = result['verdict']
    if v == 'OK':
        print(f'{BOLD}{GREEN}【OK】存在反面信号。深度是否实质，仍建议 Inferential 判官复核。{RESET}')
    elif v == 'SKIP':
        print(f'{BOLD}【跳过】{result["notes"][0]}{RESET}')
    else:
        print(f'{BOLD}{YELLOW}【REVIEW】顾问级提示（非硬性失败）：{RESET}')
    for n in result['notes']:
        print(f'  · {n}')
    if v != 'SKIP':
        print(f'\n  下一步（人在环上）：python3 见 docs/inferential-balance-judge.md '
              f'用 LLM 判官逐条核验核心判断是否有实质反面。')
    print('=' * 70)


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def force_utf8_stdout():
    """确保中文输出在任意终端代码页（如 Windows cp1252）下都不崩溃。

    供本模块及复用本模块的脚本（如 eval_sources.py）共同调用，
    避免在多处重复同一段编码修复（每个缺陷只修一次）。
    """
    for _stream in (sys.stdout, sys.stderr):
        try:
            _stream.reconfigure(encoding='utf-8')
        except Exception:
            pass


def main():
    force_utf8_stdout()

    parser = argparse.ArgumentParser(
        description='Report Audit Tool — 研究报告数据抽检工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
工作流程：

  Step 1 — 提取数据点并随机抽样 15%，输出抽检清单：
    python3 tools/report_audit.py extract --report reports/腾讯/腾讯-research-20260408.md

  Step 2 — Claude 对清单中每个数据点，从可靠信源取数，
            填入 fetched_value / fetched_source / fetched_value2 / fetched_source2

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
    ext.add_argument('--ratio', type=float, default=0.15, help='抽样比例，默认 0.15')
    ext.add_argument('--seed', type=int, default=None, help='随机种子（可选，用于复现）')
    ext.add_argument('--dry-run', action='store_true', help='只打印，不输出 JSON')

    # sources（来源充分性静态检查 —— 无网络、可用于 pre-commit/CI）
    src = sub.add_parser('sources', help='静态检查报告来源充分性（>=N 个独立信源）')
    src.add_argument('--report', required=True, help='报告文件路径（Markdown）')
    src.add_argument('--min', type=int, default=2, help='最少独立信源数，默认 2')
    src.add_argument('--output-json', action='store_true', help='以 JSON 输出结果')

    # balance（正反两面/估计标注前置过滤 —— 顾问级，默认不阻断）
    bal = sub.add_parser('balance', help='正反两面/估计标注的确定性前置过滤（顾问级）')
    bal.add_argument('--report', required=True, help='报告文件路径（Markdown）')
    bal.add_argument('--strict', action='store_true',
                     help='REVIEW 时也退出 1（默认顾问级，始终 exit 0）')
    bal.add_argument('--output-json', action='store_true', help='以 JSON 输出结果')

    # verdict
    vrd = sub.add_parser('verdict', help='根据核验结果输出准出/打回判决')
    vrd.add_argument('--results', required=True, help='JSON 数组，含 fetched_value 等字段')
    vrd.add_argument('--report', default='', help='报告名称（可选，用于显示）')
    vrd.add_argument('--output-json', action='store_true', help='将判决结果以 JSON 输出到 stdout')

    args = parser.parse_args()

    if args.command == 'extract':
        if not os.path.exists(args.report):
            print(f'❌ 文件不存在: {args.report}', file=sys.stderr)
            sys.exit(1)

        with open(args.report, 'r', encoding='utf-8') as f:
            text = f.read()

        all_points = extract_data_points(text)
        sampled = sample_points(all_points, ratio=args.ratio, seed=args.seed)

        print('=' * 70)
        print(f'报告数据抽检清单')
        print(f'文件：{args.report}')
        print(f'总提取数据点：{len(all_points)}  |  抽样比例：{args.ratio:.0%}  |  抽检数量：{len(sampled)}')
        if args.seed is not None:
            print(f'随机种子：{args.seed}（可用于复现同一批样本）')
        print('=' * 70)
        print()
        print(f'{"ID":>3}  {"行号":>5}  {"数据标签":<35}  {"报告值":>12}  {"单位"}')
        print(f'{"─"*3}  {"─"*5}  {"─"*35}  {"─"*12}  {"─"*6}')
        for p in sampled:
            print(f'{p["id"]:>3}  {p["line_number"]:>5}  {p["label"][:35]:<35}  {p["reported_value"]:>12.2f}  {p["unit"]}')
        print()
        print('↑ 请对上述每个数据点，从以下信源取数，填入 fetched_value：')
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
                    'fetched_value2': None,      # ← 填入副来源核验值（可选）
                    'fetched_source2': '',       # ← 填入副来源名称（可选）
                })
            print('抽检清单 JSON（填入 fetched_value 后，传给 verdict 命令）：')
            print()
            print(json.dumps(template, ensure_ascii=False, indent=2))

    elif args.command == 'sources':
        if not os.path.exists(args.report):
            print(f'❌ 文件不存在: {args.report}', file=sys.stderr)
            sys.exit(2)
        with open(args.report, 'r', encoding='utf-8') as f:
            text = f.read()
        result = check_sources(text, min_sources=args.min)
        if args.output_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            render_sources_report(result, report_name=args.report)
        # 非零退出码 = 打回，供 pre-commit / CI 闸门判断
        sys.exit(0 if result['verdict'] == 'PASS' else 1)

    elif args.command == 'balance':
        if not os.path.exists(args.report):
            print(f'❌ 文件不存在: {args.report}', file=sys.stderr)
            sys.exit(2)
        with open(args.report, 'r', encoding='utf-8') as f:
            text = f.read()
        result = check_balance(text)
        if args.output_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            render_balance_report(result, report_name=args.report)
        # 顾问级：默认 exit 0；--strict 时 REVIEW 退出 1
        if args.strict and result['verdict'] == 'REVIEW':
            sys.exit(1)
        sys.exit(0)

    elif args.command == 'verdict':
        try:
            results = json.loads(args.results)
        except json.JSONDecodeError as e:
            print(f'❌ JSON 解析失败: {e}', file=sys.stderr)
            sys.exit(1)

        report_name = args.report or ''
        outcome = render_verdict(results, report_name=report_name)

        if args.output_json:
            print(json.dumps(outcome, ensure_ascii=False, indent=2))

        # 非零退出码表示打回，方便 CI/脚本判断
        sys.exit(0 if outcome['verdict'] == 'PASS' else 1)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
