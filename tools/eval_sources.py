#!/usr/bin/env python3
"""Eval harness for the source-sufficiency sensor (report_audit.check_sources).

回归测试（Regression eval）：一组固定场景 + 已知期望判决，目标 ~100% 通过。
作用：每次改动 _SOURCE_PATTERNS / 阈值 / 识别逻辑后运行，确保没有悄悄
破坏既有识别能力。属于 Improvement Engine 的一环——
每发现一个漏报/误报，就在 CASES 里新增一个场景，让该缺陷不可重现。

用法：
    python3 tools/eval_sources.py            # 运行全部场景，全过则 exit 0
    python3 tools/eval_sources.py -v         # 打印每个场景细节

零依赖、无网络。CI 与本地通用。
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from report_audit import check_sources, force_utf8_stdout  # noqa: E402

force_utf8_stdout()


# 每个场景：name / text / min / expect(PASS|FAIL) / why
CASES = [
    {
        'name': '两个英文独立信源',
        'text': '数据来源：macrotrends 与 stockanalysis 交叉验证。营收 1000 亿。',
        'min': 2, 'expect': 'PASS',
        'why': '>=2 独立信源 + 有来源标记',
    },
    {
        'name': '仅一个信源',
        'text': '数据来源：morningstar。营收 1000 亿。',
        'min': 2, 'expect': 'FAIL',
        'why': '只有 1 个独立信源',
    },
    {
        'name': '完全无来源',
        'text': '营收 1000 亿，利润 300 亿，增长强劲。',
        'min': 2, 'expect': 'FAIL',
        'why': '无来源标记，无任何识别信源',
    },
    {
        'name': '有来源标记但信源不足',
        'text': '来源：某券商研报。营收 1000 亿。',
        'min': 2, 'expect': 'FAIL',
        'why': '有“来源”二字但识别不到 >=2 个受信信源',
    },
    {
        'name': '中文别名信源（东方财富 + 雪球）',
        'text': '资料来源：东方财富、雪球。市值 5000 亿。',
        'min': 2, 'expect': 'PASS',
        'why': '中文别名应被识别为 eastmoney / xueqiu',
    },
    {
        'name': 'SEC备案 + macrotrends',
        'text': 'Source: 10-K filing on sec.gov, cross-checked with macrotrends.',
        'min': 2, 'expect': 'PASS',
        'why': 'SEC备案 与 macrotrends 为两个独立信源',
    },
    {
        'name': '同一信源出现两次仍算一个',
        'text': '来源：macrotrends。另据 macrotrends 数据，营收 1000 亿。',
        'min': 2, 'expect': 'FAIL',
        'why': '去重后只剩 1 个独立信源',
    },
    {
        'name': '财报 + 彭博',
        'text': '数据来源：公司年报；彭博 Bloomberg 终端复核。净利润 200 亿。',
        'min': 2, 'expect': 'PASS',
        'why': '公司财报/公告 与 bloomberg 两个独立信源',
    },
    {
        'name': 'min=1 放宽时单一信源可过',
        'text': '数据来源：eastmoney。营收 1000 亿。',
        'min': 1, 'expect': 'PASS',
        'why': '--min 参数应生效：放宽到 1 时单信源通过',
    },
    {
        'name': 'URL 作为来源标记 + 两信源',
        'text': '参考 https://stockanalysis.com 与 https://www.gurufocus.com。PE 18x。',
        'min': 2, 'expect': 'PASS',
        'why': 'URL 命中来源标记，且识别到 stockanalysis + gurufocus',
    },
]


def run(verbose: bool = False) -> int:
    passed = 0
    failed_cases = []
    for i, c in enumerate(CASES, 1):
        result = check_sources(c['text'], min_sources=c['min'])
        actual = result['verdict']
        ok = actual == c['expect']
        if ok:
            passed += 1
        else:
            failed_cases.append((i, c, actual, result))
        mark = '✅' if ok else '❌'
        line = f'{mark} [{i:>2}] min={c["min"]} 期望={c["expect"]:4s} 实际={actual:4s}  {c["name"]}'
        if verbose or not ok:
            print(line)
            if verbose:
                print(f'        识别信源={result["found_sources"]}  ({c["why"]})')

    total = len(CASES)
    print('-' * 70)
    print(f'回归 eval：{passed}/{total} 通过')
    if failed_cases:
        print(f'❌ {len(failed_cases)} 个场景判决与期望不符 —— 改动可能破坏了 Sensor：')
        for i, c, actual, result in failed_cases:
            print(f'   [{i}] {c["name"]}: 期望 {c["expect"]}，实际 {actual}，识别={result["found_sources"]}')
        return 1
    print('✅ 全部通过，Sensor 行为未退化。')
    return 0


if __name__ == '__main__':
    verbose = '-v' in sys.argv or '--verbose' in sys.argv
    sys.exit(run(verbose=verbose))
