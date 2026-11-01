#!/usr/bin/env python3
"""Validate recorded public-page data and report arithmetic, not source truth."""
import csv
from decimal import Decimal, getcontext
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import statistics
import subprocess

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ROOT = HERE.parents[2]
REPORT = PROJECT / '持械入宋研究报告-20261101.md'
getcontext().prec = 40


def save(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def clean(value):
    value = re.sub(r'\x1b\[[0-9;]*m', '', value)
    return '\n'.join(x.rstrip() for x in value.splitlines()).rstrip() + '\n'


def seconds(value):
    m, s = map(int, value.split(':'))
    assert 0 <= s < 60
    return 60 * m + s


def plays(value):
    return Decimal(value[:-1]) * (Decimal(10) ** (8 if value[-1] == '亿' else 4))


def main():
    report = REPORT.read_text()
    evidence = json.loads((PROJECT / 'evidence.json').read_text())
    catalog = list(csv.DictReader((PROJECT / 'data/creator-catalog.csv').open()))
    episodes = list(csv.DictReader((PROJECT / 'data/season10-episodes.csv').open()))
    assert len(catalog) == 43 and len({r['collection_id'] for r in catalog}) == 43
    assert sum(int(r['episodes']) > 0 for r in catalog) == 39
    assert sum(int(r['episodes']) == 0 for r in catalog) == 4
    assert [int(r['episode']) for r in episodes] == list(range(1, 101))
    assert len({r['video_id'] for r in episodes}) == 100
    assert all(re.fullmatch(r'\d{19}', r['video_id']) for r in episodes)
    assert [int(r['episode']) for r in episodes if r['paid_badge'] == 'true'] == list(range(16, 101))
    durations = [seconds(r['duration']) for r in episodes]
    total = sum(durations)
    assert total == evidence['direct_episodes']['total_seconds'] == 9830
    assert min(durations) == 57 and durations.index(57) + 1 == 80
    assert max(durations) == 160 and durations.index(160) + 1 == 98
    assert sum(durations[:15]) == 1267 and sum(durations[15:]) == 8563
    seasons = [r for r in catalog if r['title'].startswith('持械入宋：')]
    assert len(seasons) == 10 and sum(int(r['episodes']) for r in seasons) == 1000
    assert all(r['paid_badge'] == 'true' for r in seasons)
    total_plays = sum(plays(r['display_plays']) for r in seasons)
    assert total_plays == Decimal(evidence['direct_catalog']['display_sum_arithmetic_only'])
    derived = {
        'display_plays_sum_arithmetic_only': str(total_plays),
        'rounded_100m_plays': str((total_plays / 100000000).quantize(Decimal('.01'))),
        'season1_share_percent': str((Decimal(230000000) / total_plays * 100).quantize(Decimal('.1'))),
        'episode_count': len(episodes), 'total_seconds': total,
        'mean_seconds': str(Decimal(total) / len(episodes)),
        'median_seconds': str(statistics.median(durations)),
        'paid_badge_seconds': sum(durations[15:]), 'unmarked_seconds': sum(durations[:15]),
        'paid_runtime_percent': str((Decimal(sum(durations[15:])) / total * 100).quantize(Decimal('.1'))),
        'minimum_episode': 80, 'minimum_seconds': 57,
        'maximum_episode': 98, 'maximum_seconds': 160,
        'status': 'LOCAL_CONSISTENCY_PASS',
        'scope': '本地公开页面转录与算术；不认证平台真实流量或财务'
    }
    assert derived['rounded_100m_plays'] == '6.96'
    assert derived['season1_share_percent'] == '33.1'
    assert derived['paid_runtime_percent'] == '87.1'
    for r in seasons:
        assert '| {} | {} | {} | 有 |'.format(r['title'].split('：')[1],r['display_plays'],r['episodes']) in report
    for r in catalog:
        if '| {} |'.format(r['title']) in report:
            assert '| {} | {} | {} |'.format(r['title'],r['display_plays'],r['episodes']) in report
    save('decimal-calculations.json', derived)

    expressions = [' + '.join(str(plays(r['display_plays'])) for r in seasons),
                   ' + '.join(str(x) for x in durations), '9830 / 100',
                   '8563 / 9830 * 100', '230000000 / 695525000 * 100']
    logs = []
    for expression in expressions:
        out = subprocess.run(['python3', str(ROOT / 'tools/financial_rigor.py'), 'calc', '--expr', expression],
                             capture_output=True, text=True, check=True)
        logs.append(out.stdout)
    (HERE / 'financial-rigor-calculations.txt').write_text(clean('\n'.join(logs)))

    output = subprocess.run(['python3', str(ROOT / 'tools/report_audit.py'), 'extract', '--report',
                             str(REPORT), '--ratio', '1', '--seed', '20261102'],
                            check=True, capture_output=True, text=True)
    (HERE / 'report-audit-extract.txt').write_text(clean(output.stdout.replace(str(ROOT) + '/', '')))
    spec = importlib.util.spec_from_file_location('report_audit', ROOT / 'tools/report_audit.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    points = module.extract_data_points(report)  # CLI sample is capped at 30; inspect every extraction here.
    by_title = {r['title']:r for r in catalog}
    observations = {r['id']:r for r in evidence['observations']}
    results, exclusions = [], []
    expected = {
        '2026-10-08 · 数据及口径': ('40','S15'),
        '2026-10-18 · 数据及口径': ('8200','S16'),
        '2026-10-28 · 数据及口径': ('1098','S17'),
        '2026-10-28 · 能说明什么': ('40','S15'),
        '本次目录采集 · 数据及口径': (derived['rounded_100m_plays'],'S24/计算'),
        '随后打开付费集 · 数据及口径': ('3101.4','S26'),
        '随后打开付费集 · 能说明什么': ('3092.5','S24'),
        '完整目录 · 实测结果': (str(len(episodes)),'S25'),
        '总时长 · 实测结果': (str(total),'S25/计算'),
        '平均每集 · 实测结果': (derived['mean_seconds'],'S25/计算'),
        '中位数 · 实测结果': (derived['median_seconds'],'S25/计算'),
        '最短 · 实测结果': ('80','S25/集序号；57秒另由底表验证'),
        '最长 · 实测结果': ('98','S25/集序号；160秒另由底表验证'),
        '未显示付费标签 · 实测结果': ('1','S25/起始集序号'),
        '显示付费标签 · 实测结果': ('16','S25/起始集序号'),
        '付费区时长占比 · 实测结果': (derived['paid_runtime_percent'],'S25/计算'),
        '第16集购买页 · 实测结果': ('10','S26/钻起'),
        '人员 · 本剧实际披露': ('5','S01/主创陈述'),
        '生成 · 本剧实际披露': ('3','S01/主创陈述'),
        '我有一座神奇动物园 · 观察意义': ('100','S24'),
        '抖音付费 · 已有证据': ('16','S25/付费起始集'),
    }
    for point in points:
        label = point['label']
        if label.startswith('字节跳动：Seedance') or label.startswith('字节跳动：扣子'):
            exclusions.append(dict(point, reason='模型版本或年份，不是业务指标；按来源文字人工复核'))
            continue
        if label == '资料截止' or '最近更新17' in label or '现页显示10月23日00' in label:
            exclusions.append(dict(point, reason='年份或时间分量误识别；不作为业务数字审计'))
            continue
        prefix = label.split(' · ')[0]
        if '目录展示播放量' in label or '目录集数' in label:
            row = by_title['持械入宋：' + prefix]
            value = row['display_plays'][:-1] if '播放量' in label else row['episodes']
            basis = 'S24/原始展示单位，非独立流量审计'
        elif prefix in by_title and (' · 展示播放量' in label or ' · 集数' in label):
            row = by_title[prefix]
            value = row['display_plays'][:-1] if '播放量' in label else row['episodes']
            basis = 'S24/目录转录'
        else:
            value, basis = expected[label]
        assert Decimal(str(point['reported_value'])) == Decimal(value), (point, value)
        results.append(dict(point, comparison_value=str(value), recorded_basis=basis,
                            validation_scope='转录/计算一致性；不新增第二独立信源'))
    save('numeric-results.json', results)
    save('extraction-exclusions.json', exclusions)

    phrases = ['约170.3万字','系列收藏620万','首季收藏突破200万','43个条目','39个已有分集',
               '4个显示0集','2小时43分50秒','21分07秒','2小时22分43秒','98.3秒','97秒',
               '33.1%','87.1%','10钻起','5名编导、2名剪辑、1名总导演',
               '超过100万元','商业回报约千万元','软件harness仍缺项目级证据']
    for phrase in phrases:
        assert phrase in report, phrase
    save('manual-scope.json', {
        'manually_reviewed_additional_phrases':phrases,
        'scope':'短语检查防止编辑遗失；事实依据人工对照登记来源，不是自动验证事实真伪',
        'remaining_gaps':['实际模型与harness','法人和版权合同','跨平台流量拆分','实际财务与净利润'],
        'removed_from_revision':['假设单价成本场景','建议harness架构','口径混杂的第三方热度趋势'],
        'no_second_independent_financial_source':True})
    refs = report.split('## 参考资料与数据附件')[1]
    body = report.split('## 参考资料与数据附件')[0]
    for source_id in set(re.findall(r'S\d{2}',body)):
        assert '**' + source_id + '**' in refs, source_id
    for target in re.findall(r'\]\((\./[^)]+)\)',report):
        assert (PROJECT / target).exists(), target
    for f in [REPORT,PROJECT/'README.md',PROJECT/'sources.md']:
        for line in f.read_text().splitlines():
            assert line.rstrip() == line
    files = [REPORT,PROJECT/'evidence.json',PROJECT/'data/creator-catalog.csv',PROJECT/'data/season10-episodes.csv']
    summary = {'date':'2026-11-02','extracted_count':len(points),'classified_checked':len(results),
               'excluded_non_business_numbers':len(exclusions),'catalog_rows':len(catalog),
               'episode_rows':len(episodes),'numeric_scope':'本地转录与算术一致性',
               'status':'LOCAL_CONSISTENCY_PASS',
               'sha256':{str(f.relative_to(PROJECT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},
               'publication_condition':'正文保留相关工作室与本剧边界、财务自述及原始页面统计局限'}
    save('audit-summary.json',summary)
    save('verdict.json', {'status':'LOCAL_CONSISTENCY_PASS','scope':'不是平台流量、技术栈或财务认证',
                         'checked_extractions':len(results),'excluded':len(exclusions)})
    (HERE / 'report-audit-verdict.txt').write_text(
        'LOCAL_CONSISTENCY_PASS\n已检查{}个提取数字，{}个日期/时间/版本分量单列；43条目录及100集底表校验通过。\n'
        '只验证记录与报告、算术一致性；不认证平台真实流量、实际技术栈或财务。\n'.format(len(results),len(exclusions)))
    print('LOCAL_CONSISTENCY_PASS: {} points; {} exclusions; 43 catalog rows; 100 episodes.'.format(len(results),len(exclusions)))


if __name__ == '__main__':
    main()
