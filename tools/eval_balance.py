#!/usr/bin/env python3
"""Eval harness for the balance pre-filter (report_audit.check_balance).

回归测试：守护「正反两面/估计标注」Computational 前置过滤层的确定性行为。
注意：本 eval 只覆盖确定性前置层；上层 LLM 判官的校准是另一套流程，
见 docs/inferential-balance-judge.md §6（人工 ground truth）。

用法：
    python3 tools/eval_balance.py [-v]
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from report_audit import check_balance, force_utf8_stdout  # noqa: E402

force_utf8_stdout()

LONG = '这是一段足够长的实质分析。' * 30  # 触发 substantive 长度阈值

CASES = [
    {
        'name': '实质报告 + 有反面标记 → OK',
        'text': '核心判断：看多。' + LONG + '但另一方面，下行风险在于需求走弱。',
        'expect_verdict': 'OK', 'expect_note_substr': None,
    },
    {
        'name': '实质报告 + 无任何反面标记 → REVIEW',
        'text': '核心判断：强烈看多，护城河极深，估值便宜。' + LONG,
        'expect_verdict': 'REVIEW', 'expect_note_substr': '一面倒',
    },
    {
        'name': '过短非判断性 → SKIP',
        'text': '今天天气不错。',
        'expect_verdict': 'SKIP', 'expect_note_substr': None,
    },
    {
        'name': '判断性短文（含「结论」，无任何反面词）→ REVIEW',
        'text': '结论：看多。理由是增长强劲，护城河深，估值合理，前景光明。',
        'expect_verdict': 'REVIEW', 'expect_note_substr': '一面倒',
    },
    {
        # 已知局限：grep 无法理解否定。「没有提任何风险」含「风险」二字 → 误判 OK。
        # 保留为永久测试以记录该缺陷类——这正是上层必须用 Inferential 判官的原因。
        'name': '【已知局限】否定式假阳性：keyword 命中「风险」却实为一面倒',
        'text': '结论：看多。' + LONG + '报告中没有提到任何风险或下行情形。',
        'expect_verdict': 'OK', 'expect_note_substr': None,
    },
    {
        'name': '预测性表述但无估计标注 → 触发 note',
        'text': '核心判断：看多。' + LONG + '存在下行风险。预计未来三年 CAGR 20%，目标价翻倍。',
        'expect_verdict': 'OK', 'expect_note_substr': '估计',
    },
    {
        'name': '有估计标注 → 不触发估计 note',
        'text': '核心判断：看多。' + LONG + '风险在于竞争。我们估计未来增速放缓，假设保守。',
        'expect_verdict': 'OK', 'expect_note_substr': None,
    },
]


def run(verbose=False):
    passed = 0
    fails = []
    for i, c in enumerate(CASES, 1):
        r = check_balance(c['text'])
        ok = r['verdict'] == c['expect_verdict']
        if c['expect_note_substr'] is not None:
            ok = ok and any(c['expect_note_substr'] in n for n in r['notes'])
        if ok:
            passed += 1
        else:
            fails.append((i, c, r))
        mark = '✅' if ok else '❌'
        if verbose or not ok:
            print(f'{mark} [{i}] 期望={c["expect_verdict"]:6s} 实际={r["verdict"]:6s}  {c["name"]}')
            if verbose:
                print(f'        notes={r["notes"]}')

    print('-' * 70)
    print(f'balance 回归 eval：{passed}/{len(CASES)} 通过')
    if fails:
        for i, c, r in fails:
            print(f'   ❌ [{i}] {c["name"]}: 实际 verdict={r["verdict"]} notes={r["notes"]}')
        return 1
    print('✅ 全部通过。')
    return 0


if __name__ == '__main__':
    sys.exit(run('-v' in sys.argv or '--verbose' in sys.argv))
