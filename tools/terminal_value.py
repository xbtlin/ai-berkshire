#!/usr/bin/env python3
"""终值倍数与十年 IRR 推演工具 (Terminal Value Toolkit for AI Berkshire).

把「7公司10年投资价值横评」第三节的估值框架做成可复用工具。核心是永续增长模型：

    PE(终值) = (1 - g/ROIC) / (r - g)

    分子 1 - g/ROIC  = 派息率。g/ROIC 是留存率——想每年长 g，每留存一块钱赚 ROIC，
                       就必须留下利润的 g/ROIC 再投，剩下的才能分给股东。
    分母 r - g       = 永续年金分母。你要 r 的回报，东西自己长 g，净差额就是 r-g。

三条必须记住的纪律（全部来自那份报告踩过的坑）：

  1. r 和 g 必须同币种。3% 的名义增长，在 2.5% 通胀的美国是 0.5% 实际增长（保守），
     在 1% 通胀的中国是 2% 实际增长（激进）。同一个数字换币种就换了含义。
     本工具用 --g-shift 显式表达币种换算，不允许隐式混用。
  2. 分母 r-g 至少要有 5 个百分点，戈登模型才有意义。低于 5pct 时 g 动一点点估值就翻天，
     那不是估值，是放大偏见。本工具对每一格做体检并显式警告。
  3. 离散风险（退市/VIE失效/地缘断供/监管重击）不能放进 r 或 beta。抬 r 三个百分点对第 10 年
     现金流的惩罚是第 1 年的 2.6 倍，而退市是大致均匀甚至前置的年度危害率——用折现率处理它
     会把风险的时间分布搞反。正确做法是单列一个尾部情景档。

零外部依赖，仅用 Python 标准库。要求 Python >= 3.7。

用法：

    # 单点退出 PE，打印完整算式
    python3 tools/terminal_value.py pe --roic 0.20 --g 0.02 --r 0.06

    # 单公司三档推演（用内置预设）
    python3 tools/terminal_value.py company --name 腾讯 --r 0.06 --g-shift -0.01

    # 七家横评表 + 排序
    python3 tools/terminal_value.py table --r 0.06 --g-shift -0.01 --rf 0.017

    # 多档 r 敏感性 + 排序稳定性检验
    python3 tools/terminal_value.py sweep --r 0.06,0.08,0.10,0.12 --g-shift -0.01 --rf 0.017

    # 分母宽度体检（哪些格子跌破 5pct 有效性下限）
    python3 tools/terminal_value.py check --r 0.06 --g-shift -0.01

    # 从零算 IRR（不依赖预设，给利润和市值即可）
    python3 tools/terminal_value.py irr --profit 5390 --mcap 34420 --pe 22.5 --years 10 --payout 0.015

    # 用自己的公司配置
    python3 tools/terminal_value.py table --r 0.08 --config my_companies.json
"""

import argparse
import json
import sys

# ---------------------------------------------------------------------------
# 输出编码：Windows 控制台默认 GBK，本工具的 ⚠ / ✓ 会抛 UnicodeEncodeError
# ---------------------------------------------------------------------------


def _force_utf8_stdio():
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8")
            except Exception:
                pass


_force_utf8_stdio()

# 戈登模型的有效性下限：分母 r-g 至少 5 个百分点
MIN_SPREAD = 0.05

# ---------------------------------------------------------------------------
# 内置预设：7公司10年投资价值横评（基准日 2026-08-14，口径修订 2026-08-17）
#
# roic  — 2036 年稳态增量 ROIC。报告 3.2 节的判断值，夹在存量 ROIC（77%-180%）
#         与派息反解的隐含增量 ROIC（2%-14.3%）之间。这是判断不是计算。
# g     — 永续增速三档 (悲/基/乐)，人民币口径「前」的原始取值。
#         规则：悲观 = 基准 - 1.5pct，乐观 = 基准 + 1.0pct（故意不对称，
#         因为下行侧有已入账的硬证据，上行侧多为未证实事项）。
#         注意这组 g 是报告 3.6 节三张表反解出来的，反算可完整复现原表。
# p     — 三档概率权重 (悲/基/乐)，来自第四节对抗验证后的调整。
# irr10 — 报告 3.6 节 r=10% 主口径下的三档 IRR，作为 rescale 模式的基准点。
# k     — 股息率 - 股权稀释率，年化。IRR 中不随退出倍数变化的那部分。
#         结果对 k 极不敏感（k 变动 3pct 只影响 IRR 约 0.07pct），故用估计值。
# ---------------------------------------------------------------------------

PRESET = {
    "腾讯": dict(roic=0.20, g=(0.015, 0.030, 0.040), p=(0.35, 0.50, 0.15),
                 irr10=(0.3, 9.3, 15.4), k=0.020),
    "阿里巴巴": dict(roic=0.15, g=(0.015, 0.030, 0.040), p=(0.35, 0.45, 0.20),
                     irr10=(-1.3, 7.8, 16.3), k=0.000),
    "拼多多": dict(roic=0.40, g=(0.005, 0.020, 0.030), p=(0.30, 0.55, 0.15),
                   irr10=(-9.7, 8.2, 15.0), k=0.000),
    "贵州茅台": dict(roic=0.25, g=(0.010, 0.025, 0.035), p=(0.35, 0.45, 0.20),
                     irr10=(-5.3, 3.4, 7.2), k=0.045),
    "泡泡玛特": dict(roic=0.25, g=(0.015, 0.030, 0.040), p=(0.38, 0.44, 0.18),
                     irr10=(-8.2, 4.9, 10.9), k=0.018),
    "美团": dict(roic=0.18, g=(0.015, 0.030, 0.040), p=(0.40, 0.45, 0.15),
                 irr10=(-12.1, 1.8, 8.7), k=0.000),
    "MiniMax": dict(roic=0.20, g=(0.025, 0.040, 0.050), p=(0.55, 0.30, 0.15),
                    irr10=(-30.8, -4.7, 9.6), k=-0.030),
}

BASE_R = 0.10  # 预设 irr10 对应的折现率

# 无风险利率实测值（2026-08），用于风险调整后回报的分子
RF = {
    "CNY": 0.0170,  # 中国 10 年期国债，2026-08-07
    "USD": 0.0470,  # 美国 10 年期国债，2026-08-14
}

LABELS = ("悲观", "基准", "乐观")

# ---------------------------------------------------------------------------
# 币种口径护栏（audit 子命令用）
#
# r 区间下沿 = 观测无风险利率 + 约 4.3pct 溢价，上沿 = 合成无风险利率 + 约 6pct 溢价。
# 两个币种的区间差的 3 个百分点全部是国债利差，不含任何风险判断差异。
# g 上限 = 该币种长期通胀 + 约 1pct 实际增长；超过等于假设公司长成整个经济体。
# 数据来源见 reports/7公司10年投资价值横评-确定性调整后回报-20260814.md 第 3.4 节。
# ---------------------------------------------------------------------------

CURRENCY_BANDS = {
    "CNY": dict(r=(0.06, 0.09), g_max=0.02, rf=0.0170,
                note="中国10年期国债 1.70%（观测）/ 2.5-3.0%（合成）+ ERP 5.18%"),
    "USD": dict(r=(0.09, 0.115), g_max=0.040, rf=0.0470,
                note="美国10年期国债 4.70% + 中国总ERP 5.18%（含1.01%国别溢价）"),
    "HKD": dict(r=(0.09, 0.115), g_max=0.040, rf=0.0470,
                note="港币与美元挂钩，口径同 USD"),
}

# 离散风险的合法归属。写进折现率或 beta 一律打回——抬 r 三个百分点对第 10 年现金流的
# 惩罚是第 1 年的 2.6 倍，而退市/断供是大致均匀甚至前置的年度危害率，会把时间分布搞反。
RISK_PLACEMENT_OK = {"情景", "尾部档", "概率"}
RISK_PLACEMENT_BAD = {"折现率", "r", "beta", "β"}
RISK_PLACEMENT_WARN = {"未建模"}

# ---------------------------------------------------------------------------
# 核心计算
# ---------------------------------------------------------------------------


def exit_pe(roic, g, r):
    """永续增长模型的终值 PE。

    返回 (pe, 留存率, 分子, 分母)。分母 <= 0 时返回 pe=None（模型失效）。
    """
    spread = r - g
    retention = g / roic
    numerator = 1.0 - retention
    if spread <= 0:
        return None, retention, numerator, spread
    return numerator / spread, retention, numerator, spread


def irr_from_terminal(profit_2036, mcap_today, pe, years=10, payout=0.0):
    """从零算 IRR：终值市值 = 2036 利润 x 退出 PE。

    payout = 股息率 - 稀释率，年化，直接加在几何回报上（报告口径，未做再投资复利）。
    """
    return (profit_2036 * pe / mcap_today) ** (1.0 / years) - 1.0 + payout


def rescale_irr(irr_base, pe_base, pe_new, k, years=10):
    """把基准 r 下的 IRR 换算到新的退出倍数。

    IRR 中只有资本利得部分随退出倍数变化，k（股息-稀释）不变：
        (1 + IRR_new - k) = (1 + IRR_base - k) x (PE_new / PE_base)^(1/years)
    """
    return (1.0 + irr_base - k) * (pe_new / pe_base) ** (1.0 / years) - 1.0 + k


def weighted_stats(values, probs):
    """概率加权的期望值与标准差。"""
    mean = sum(v * p for v, p in zip(values, probs))
    var = sum(p * (v - mean) ** 2 for v, p in zip(values, probs))
    return mean, var ** 0.5


def evaluate(spec, r, g_shift=0.0, years=10):
    """算一家公司在给定 r 下的三档退出 PE 与 IRR。

    g_shift 是币种换算：把原始 g 平移到目标币种的通胀口径。
    人民币口径相对报告原值取 -0.01（中国长期通胀约 1% vs 美国约 2.5%）。
    """
    roic = spec["roic"]
    rows = []
    for label, g0, irr_b in zip(LABELS, spec["g"], spec["irr10"]):
        g = g0 + g_shift
        pe_new, retention, numerator, spread = exit_pe(roic, g, r)
        # 基准 PE 必须用「平移前」的 g：irr10 这个锚点对应的是 (BASE_R, 原始 g)。
        # 用平移后的 g 算基准会把币种换算的影响漏掉一半，IRR 被系统性高估。
        pe_base, _, _, _ = exit_pe(roic, g0, BASE_R)
        if pe_new is None or pe_base is None:
            irr = None
        else:
            irr = rescale_irr(irr_b / 100.0, pe_base, pe_new, spec["k"], years) * 100.0
        rows.append(dict(label=label, g=g, pe=pe_new, irr=irr,
                         retention=retention, numerator=numerator, spread=spread))
    return rows


def summarize(rows, probs, rf):
    """期望 IRR、标准差、风险调整后回报。任一档失效则整体不可用。"""
    irrs = [row["irr"] for row in rows]
    if any(x is None for x in irrs):
        return None, None, None
    mean, sd = weighted_stats(irrs, probs)
    ratio = (mean - rf * 100.0) / sd if sd > 0 else None
    return mean, sd, ratio


def load_companies(path):
    if not path:
        return dict(PRESET)
    with open(path, encoding="utf-8") as fh:
        raw = json.load(fh)
    out = {}
    for name, spec in raw.items():
        out[name] = dict(roic=spec["roic"], g=tuple(spec["g"]), p=tuple(spec["p"]),
                         irr10=tuple(spec["irr10"]), k=spec.get("k", 0.0))
    return out


def warn_spread(spread):
    """分母宽度体检标记。"""
    if spread <= 0:
        return "✗失效"
    if spread < MIN_SPREAD:
        return "⚠窄"
    return ""

# ---------------------------------------------------------------------------
# 子命令
# ---------------------------------------------------------------------------


def cmd_pe(args):
    pe, retention, numerator, spread = exit_pe(args.roic, args.g, args.r)
    print(f"\nPE(终值) = (1 - g/ROIC) / (r - g)\n")
    print(f"  ROIC = {args.roic:.1%}   g = {args.g:.2%}   r = {args.r:.2%}\n")
    print(f"  留存率 g/ROIC   = {args.g:.4f} / {args.roic:.2f} = {retention:.4f}  ({retention:.1%})")
    print(f"  分子 1 - 留存率 = {numerator:.4f}                    （即派息率 {numerator:.1%}）")
    print(f"  分母 r - g      = {args.r:.4f} - {args.g:.4f} = {spread:.4f}  ({spread*100:.1f}pct)")
    if pe is None:
        print(f"\n  ✗ 分母 <= 0，模型失效。g 必须小于 r。\n")
        return 1
    print(f"\n  退出 PE = {numerator:.4f} / {spread:.4f} = {pe:.1f}x\n")
    if spread < MIN_SPREAD:
        print(f"  ⚠ 分母仅 {spread*100:.1f}pct，低于 {MIN_SPREAD*100:.0f}pct 有效性下限。")
        bumped, _, _, _ = exit_pe(args.roic, args.g + 0.005, args.r)
        if bumped:
            print(f"    g 只要再加 0.5pct，PE 就变成 {bumped:.1f}x（{bumped/pe-1:+.0%}）。")
        print(f"    这一格该当作方向性参考，不能当估值用。\n")
    return 0


def cmd_company(args):
    companies = load_companies(args.config)
    if args.name not in companies:
        print(f"未知公司：{args.name}。可选：{'、'.join(companies)}", file=sys.stderr)
        return 1
    spec = companies[args.name]
    rows = evaluate(spec, args.r, args.g_shift, args.years)
    rf = args.rf if args.rf is not None else RF["CNY"]

    print(f"\n{args.name}  |  r = {args.r:.1%}   ROIC = {spec['roic']:.0%}   "
          f"g平移 {args.g_shift:+.1%}   Rf = {rf:.2%}\n")
    print(f"{'档位':<6}{'概率':>6}{'g':>8}{'留存率':>8}{'分子':>8}{'分母':>9}{'退出PE':>9}{'IRR':>9}  体检")
    print("-" * 74)
    for row, p in zip(rows, spec["p"]):
        pe = f"{row['pe']:.1f}x" if row["pe"] else "—"
        irr = f"{row['irr']:+.1f}%" if row["irr"] is not None else "—"
        print(f"{row['label']:<6}{p:>6.0%}{row['g']:>8.1%}{row['retention']:>8.1%}"
              f"{row['numerator']:>8.3f}{row['spread']*100:>7.1f}pct{pe:>9}{irr:>9}  {warn_spread(row['spread'])}")

    mean, sd, ratio = summarize(rows, spec["p"], rf)
    print("-" * 74)
    if mean is None:
        print("\n期望值不可用：至少一档的分母 <= 0。\n")
        return 1
    print(f"{'期望IRR':<12}{mean:+.2f}%      标准差 {sd:.1f}%      风险调整后 {ratio:+.2f}\n")
    narrow = [r_["label"] for r_ in rows if 0 < r_["spread"] < MIN_SPREAD]
    if narrow:
        print(f"⚠ {'/'.join(narrow)} 档分母低于 {MIN_SPREAD*100:.0f}pct，退出倍数对 g 极度敏感。\n")
    return 0


def cmd_table(args):
    companies = load_companies(args.config)
    rf = args.rf if args.rf is not None else RF["CNY"]
    results = []
    for name, spec in companies.items():
        rows = evaluate(spec, args.r, args.g_shift, args.years)
        mean, sd, ratio = summarize(rows, spec["p"], rf)
        results.append((name, spec, rows, mean, sd, ratio))
    ok = [x for x in results if x[5] is not None]
    bad = [x for x in results if x[5] is None]
    ok.sort(key=lambda x: -x[5])

    print(f"\nr = {args.r:.1%}   g平移 {args.g_shift:+.1%}   Rf = {rf:.2%}   持有期 {args.years} 年\n")
    print(f"{'排名':<5}{'公司':<10}{'退出PE(悲/基/乐)':<24}{'IRR(悲/基/乐)':<30}"
          f"{'期望IRR':>9}{'σ':>8}{'风险调整后':>11}")
    print("-" * 98)
    for i, (name, spec, rows, mean, sd, ratio) in enumerate(ok, 1):
        pes = "/".join(f"{r_['pe']:.1f}" for r_ in rows)
        irrs = "/".join(f"{r_['irr']:+.1f}%" for r_ in rows)
        print(f"{i:<5}{name:<10}{pes:<26}{irrs:<32}{mean:>8.2f}%{sd:>7.1f}%{ratio:>11.2f}")
    for name, spec, rows, mean, sd, ratio in bad:
        print(f"{'—':<5}{name:<10}{'模型失效（分母 <= 0）':<26}")

    narrow = sum(1 for _, _, rows, _, _, _ in results
                 for r_ in rows if 0 < r_["spread"] < MIN_SPREAD)
    total = sum(len(rows) for _, _, rows, _, _, _ in results)
    print("-" * 98)
    if narrow:
        print(f"\n⚠ {total} 格里有 {narrow} 格的分母低于 {MIN_SPREAD*100:.0f}pct 有效性下限。"
              f"跑 `check --r {args.r}` 看明细。")
        if narrow > total / 2:
            print(f"  过半格子失效——这一档应当作「上行/下行情景」看，不能当另一个同等可信的估值。")
    print()
    return 0


def cmd_sweep(args):
    companies = load_companies(args.config)
    rf = args.rf if args.rf is not None else RF["CNY"]
    rates = [float(x) for x in args.r.split(",")]
    order = {}

    print(f"\ng平移 {args.g_shift:+.1%}   Rf = {rf:.2%}   持有期 {args.years} 年")
    print(f"\n期望IRR：\n")
    header = f"{'公司':<10}" + "".join(f"{'r=' + format(x, '.0%'):>11}" for x in rates)
    print(header)
    print("-" * len(header))
    for name, spec in companies.items():
        cells = []
        for r in rates:
            rows = evaluate(spec, r, args.g_shift, args.years)
            mean, sd, ratio = summarize(rows, spec["p"], rf)
            cells.append((mean, ratio))
            order.setdefault(r, []).append((name, ratio))
        line = f"{name:<10}" + "".join(
            f"{m:>10.1f}%" if m is not None else f"{'—':>11}" for m, _ in cells)
        print(line)

    print(f"\n风险调整后回报排序：\n")
    ranks = {}
    for r in rates:
        entries = [(n, x) for n, x in order[r] if x is not None]
        entries.sort(key=lambda t: -t[1])
        for pos, (n, _) in enumerate(entries, 1):
            ranks.setdefault(n, {})[r] = pos
    header = f"{'公司':<10}" + "".join(f"{'r=' + format(x, '.0%'):>11}" for x in rates)
    print(header)
    print("-" * len(header))
    for name in companies:
        cells = "".join(f"{ranks.get(name, {}).get(r, '—'):>11}" for r in rates)
        print(f"{name:<10}{cells}")

    moved = [n for n in companies
             if len({ranks.get(n, {}).get(r) for r in rates}) > 1]
    print()
    if moved:
        print(f"排序随 r 变动的公司：{'、'.join(moved)}")
        print(f"其余 {len(companies) - len(moved)} 家位次恒定——这是比绝对数字稳健得多的结论。\n")
    else:
        print(f"全部 {len(companies)} 家位次恒定，排序完全不受 r 影响。\n")
    return 0


def cmd_check(args):
    companies = load_companies(args.config)
    print(f"\n分母宽度体检   r = {args.r:.1%}   g平移 {args.g_shift:+.1%}   "
          f"下限 {MIN_SPREAD*100:.0f}pct\n")
    print(f"{'公司':<10}{'档位':<6}{'g':>8}{'r-g':>9}{'退出PE':>9}"
          f"{'g+0.5pct后':>12}{'PE变化':>9}  体检")
    print("-" * 76)
    flagged = 0
    for name, spec in companies.items():
        for label, g0 in zip(LABELS, spec["g"]):
            g = g0 + args.g_shift
            pe, _, _, spread = exit_pe(spec["roic"], g, args.r)
            bumped, _, _, _ = exit_pe(spec["roic"], g + 0.005, args.r)
            mark = warn_spread(spread)
            if mark:
                flagged += 1
            pe_s = f"{pe:.1f}x" if pe else "—"
            bumped_s = f"{bumped:.1f}x" if bumped else "—"
            delta = f"{bumped/pe-1:+.0%}" if (pe and bumped) else "—"
            print(f"{name if label == '悲观' else '':<10}{label:<6}{g:>8.1%}"
                  f"{spread*100:>7.1f}pct{pe_s:>9}{bumped_s:>12}{delta:>9}  {mark}")
    print("-" * 76)
    total = len(companies) * 3
    print(f"\n{total} 格里 {flagged} 格触发警告。")
    print(f"「g+0.5pct后」那一列是这条规矩的意义所在：分母越窄，永续增速动一点点估值就翻天。\n")
    return 0


def cmd_audit(args):
    """三条硬约束的准出检查。任一条不过 → 【打回】，退出码 1。"""
    band = CURRENCY_BANDS.get(args.currency.upper())
    if band is None:
        print(f"未知币种 {args.currency}，可选：{'、'.join(CURRENCY_BANDS)}", file=sys.stderr)
        return 1
    gs = [float(x) for x in args.g.split(",")]
    fails, warns = [], []

    print(f"\n{'='*72}\n估值口径准出检查   币种={args.currency.upper()}   r={args.r:.2%}   "
          f"ROIC={args.roic:.0%}   g={'/'.join(f'{x:.1%}' for x in gs)}\n{'='*72}")

    # --- C1 币种一致性：r 与 g 必须同币种 -----------------------------------
    lo, hi = band["r"]
    print(f"\n【C1】币种一致性 — r 与 g 必须用同一个币种")
    print(f"     {args.currency.upper()} 口径基准：{band['note']}")
    print(f"     r 合理区间 [{lo:.1%}, {hi:.1%}]   g 上限 {band['g_max']:.1%}   Rf {band['rf']:.2%}")
    if not (lo <= args.r <= hi):
        other = [c for c, b in CURRENCY_BANDS.items()
                 if c != args.currency.upper() and b["r"][0] <= args.r <= b["r"][1]]
        hint = f"（这个 r 落在 {'/'.join(other)} 的区间里——是不是拿错币种了？）" if other else ""
        fails.append(f"C1: r={args.r:.2%} 不在 {args.currency.upper()} 的 [{lo:.1%},{hi:.1%}] 区间内 {hint}")
    # g 上限卡在基准档。乐观档按设计是基准 +1pct，故额外放宽 1pct。
    g_base = gs[1] if len(gs) >= 2 else gs[0]
    if g_base > band["g_max"] or max(gs) > band["g_max"] + 0.01:
        other = [c for c, b in CURRENCY_BANDS.items()
                 if c != args.currency.upper() and g_base <= b["g_max"]]
        hint = (f"（这是 {'/'.join(other)} 的量级——r 用了本币而 g 用了外币，"
                f"正是最常见的口径混用）") if other else ""
        fails.append(f"C1: 基准档 g={g_base:.1%} 超过 {args.currency.upper()} 上限 "
                     f"{band['g_max']:.1%}（乐观档另放宽 1pct 至 {band['g_max']+0.01:.1%}）{hint}")
    if args.rf is not None and abs(args.rf - band["rf"]) > 0.005:
        fails.append(f"C1: 无风险利率 {args.rf:.2%} 与 {args.currency.upper()} 的 {band['rf']:.2%} 不符")
    print(f"     → {'✗ 不通过' if any(f.startswith('C1') for f in fails) else '✓ 通过'}")

    # --- C2 分母宽度 ---------------------------------------------------------
    print(f"\n【C2】分母宽度 — r-g 至少 {MIN_SPREAD*100:.0f} 个百分点")
    narrow = []
    for label, g in zip(LABELS, gs):
        pe, _, _, spread = exit_pe(args.roic, g, args.r)
        bumped, _, _, _ = exit_pe(args.roic, g + 0.005, args.r)
        tag = warn_spread(spread)
        delta = f"  g+0.5pct → {bumped:.1f}x ({bumped/pe-1:+.0%})" if (pe and bumped) else ""
        pe_s = f"{pe:.1f}x" if pe else "模型失效"
        print(f"     {label}  g={g:>5.1%}  r-g={spread*100:>4.1f}pct  PE={pe_s:>10}{delta}  {tag}")
        if spread <= 0:
            fails.append(f"C2: {label}档 r-g={spread*100:.1f}pct <= 0，模型失效")
        elif spread < MIN_SPREAD:
            narrow.append(label)
    if narrow:
        if args.upside_only:
            warns.append(f"C2: {'/'.join(narrow)}档分母不足 {MIN_SPREAD*100:.0f}pct，"
                         f"已声明 --upside-only，仅可作情景参考")
        else:
            fails.append(f"C2: {'/'.join(narrow)}档分母不足 {MIN_SPREAD*100:.0f}pct。"
                         f"要么调窄 g，要么加 --upside-only 声明这是情景而非估值")
    print(f"     → {'✗ 不通过' if any(f.startswith('C2') for f in fails) else '✓ 通过'}")

    # --- C3 离散风险归属 -----------------------------------------------------
    print(f"\n【C3】离散风险归属 — 退市/VIE/地缘/监管必须归情景，不得进 r 或 β")
    if args.beta != 1.0 and not args.beta_justification:
        fails.append(f"C3: β={args.beta} 偏离 1.0 但未给 --beta-justification。"
                     f"回归 β 的标准误就有 ±0.2-0.3，调它必须说明用的是自下而上的基本面 β")
    for item in [x for x in args.discrete_risks.split(",") if x.strip()]:
        if ":" not in item:
            fails.append(f"C3: '{item}' 格式应为 风险名:归属")
            continue
        name, place = (p.strip() for p in item.split(":", 1))
        if place in RISK_PLACEMENT_BAD:
            fails.append(f"C3: 「{name}」被放进了 {place}。抬 r 对第10年现金流的惩罚是第1年的 2.6 倍，"
                         f"而这类风险是均匀甚至前置的年度危害率——会把风险的时间分布搞反")
            mark = "✗"
        elif place in RISK_PLACEMENT_WARN:
            warns.append(f"C3: 「{name}」未建模，必须写进报告的「限制」章节")
            mark = "⚠"
        elif place in RISK_PLACEMENT_OK:
            mark = "✓"
        else:
            fails.append(f"C3: 「{name}」的归属 '{place}' 无法识别，"
                         f"合法值：{'/'.join(sorted(RISK_PLACEMENT_OK | RISK_PLACEMENT_WARN))}")
            mark = "✗"
        print(f"     {mark} {name} → {place}")
    if args.beta == 1.0:
        print(f"     β = 1.0（默认值，无需理由）")
    else:
        print(f"     β = {args.beta}（理由：{args.beta_justification or '未给出'}）")
    print(f"     → {'✗ 不通过' if any(f.startswith('C3') for f in fails) else '✓ 通过'}")

    # --- 判决 ----------------------------------------------------------------
    print(f"\n{'='*72}")
    for w in warns:
        print(f"⚠ {w}")
    if fails:
        print(f"\n【打回】{len(fails)} 项不通过：\n")
        for i, msg in enumerate(fails, 1):
            print(f"  {i}. {msg}")
        print(f"\n修正后重跑本命令，通过才能把估值写进报告。\n")
        return 1
    print(f"\n【准出】三条硬约束全部通过，可以把估值写进报告。")
    if warns:
        print(f"       但上述 {len(warns)} 条警告必须在报告里显式写出。")
    print()
    return 0


def cmd_irr(args):
    irr = irr_from_terminal(args.profit, args.mcap, args.pe, args.years, args.payout)
    terminal = args.profit * args.pe
    mult = terminal / args.mcap
    print(f"\nIRR = (2036市值 / 今日市值)^(1/{args.years}) - 1 + 股息率 - 稀释率\n")
    print(f"  2036 市值 = {args.profit:,.0f} x {args.pe:.1f}x = {terminal:,.0f}")
    print(f"  今日市值 = {args.mcap:,.0f}")
    print(f"  总倍数   = {mult:.4f}")
    print(f"  几何年化 = {mult ** (1.0/args.years) - 1:+.2%}")
    print(f"  股息-稀释 = {args.payout:+.2%}")
    print(f"\n  IRR = {irr:+.2%}\n")
    return 0

# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="终值倍数与十年 IRR 推演（永续增长模型）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("用法：")[-1])
    sub = parser.add_subparsers(dest="cmd")

    def add_common(p, need_r=True):
        if need_r:
            p.add_argument("--r", type=float, required=True, help="资本成本，小数（如 0.06）")
        p.add_argument("--g-shift", type=float, default=0.0,
                       help="g 的币种平移，小数。人民币口径相对报告原值取 -0.01")
        p.add_argument("--years", type=int, default=10, help="持有期年数，默认 10")
        p.add_argument("--config", help="自定义公司配置 JSON，缺省用内置 7 家预设")

    p = sub.add_parser("pe", help="单点退出 PE，打印完整算式")
    p.add_argument("--roic", type=float, required=True)
    p.add_argument("--g", type=float, required=True)
    p.add_argument("--r", type=float, required=True)
    p.set_defaults(func=cmd_pe)

    p = sub.add_parser("company", help="单公司三档推演")
    p.add_argument("--name", required=True)
    p.add_argument("--rf", type=float, help="无风险利率，缺省用人民币 1.70%%")
    add_common(p)
    p.set_defaults(func=cmd_company)

    p = sub.add_parser("table", help="多公司横评表 + 排序")
    p.add_argument("--rf", type=float, help="无风险利率，缺省用人民币 1.70%%")
    add_common(p)
    p.set_defaults(func=cmd_table)

    p = sub.add_parser("sweep", help="多档 r 敏感性 + 排序稳定性检验")
    p.add_argument("--r", required=True, help="逗号分隔，如 0.06,0.08,0.10,0.12")
    p.add_argument("--rf", type=float, help="无风险利率，缺省用人民币 1.70%%")
    add_common(p, need_r=False)
    p.set_defaults(func=cmd_sweep)

    p = sub.add_parser("check", help="分母宽度体检")
    add_common(p)
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("audit", help="三条硬约束准出检查（【准出】/【打回】）")
    p.add_argument("--currency", required=True, help="现金流币种：CNY / USD / HKD")
    p.add_argument("--r", type=float, required=True, help="资本成本，小数")
    p.add_argument("--roic", type=float, required=True, help="2036 稳态增量 ROIC，小数")
    p.add_argument("--g", required=True, help="三档永续增速，逗号分隔，如 0.005,0.02,0.03")
    p.add_argument("--rf", type=float, help="无风险利率，小数。给了就校验与币种是否匹配")
    p.add_argument("--beta", type=float, default=1.0, help="股票风险系数，默认 1.0")
    p.add_argument("--beta-justification", help="β 偏离 1.0 时必填")
    p.add_argument("--discrete-risks", default="",
                   help="离散风险归属，格式 风险名:归属，逗号分隔。"
                        "合法归属：情景/尾部档/概率（通过）、未建模（警告）。"
                        "写成 折现率/r/beta 一律打回")
    p.add_argument("--upside-only", action="store_true",
                   help="声明本档仅作上行/下行情景参考，允许分母不足 5pct")
    p.set_defaults(func=cmd_audit)

    p = sub.add_parser("irr", help="从零算 IRR（给利润与市值）")
    p.add_argument("--profit", type=float, required=True, help="终值年利润")
    p.add_argument("--mcap", type=float, required=True, help="今日市值，与利润同单位同币种")
    p.add_argument("--pe", type=float, required=True, help="退出 PE")
    p.add_argument("--years", type=int, default=10)
    p.add_argument("--payout", type=float, default=0.0, help="股息率 - 稀释率，年化小数")
    p.set_defaults(func=cmd_irr)

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
