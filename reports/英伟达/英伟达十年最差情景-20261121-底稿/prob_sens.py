"""敏感性：最差情景参数变动对 2036 净利的影响。

单位统一为十亿美元（与报告底稿 verify_model.py 一致），输出换算为亿美元。
"""
from decimal import Decimal as D

B = D("1e9")   # 1 十亿美元 = 10 亿美元


def ni(pool_b, share, other_b, margin):
    """pool/other 单位：十亿美元；返回十亿美元"""
    return (D(pool_b) * D(str(share)) + D(other_b)) * D(str(margin))


def yi(x):
    """十亿美元 → 亿美元"""
    return x * D(10)


base = dict(pool=600, share=0.15, other=30, margin=0.08)
base_ni = ni(base["pool"], base["share"], base["other"], base["margin"])

print("=" * 94)
print("最差情景参数敏感性（2036 年常态年净利）")
print("=" * 94)
print(f"\n最差情景基准：池 {yi(base['pool']):.0f} 亿美元 × 份额 {base['share']:.0%} "
      f"+ 其他 {yi(base['other']):.0f} 亿美元，净利率 {base['margin']:.0%}")
print(f"  → 收入 {yi(base['pool']*D(str(base['share']))+base['other']):.0f} 亿美元，"
      f"净利 {yi(base_ni):.0f} 亿美元")

print("\n【单参数变动】其余保持最差情景取值")
print(f"  {'参数':<14}{'取值':>10}{'净利(亿美元)':>16}{'vs 基准':>12}")
for label, vals, key, fmt in [
    ("设备价值池", [1200, 900, 600, 300, 200], "pool", "亿"),
    ("价值份额", [0.40, 0.30, 0.15, 0.10, 0.05], "share", "pct"),
    ("其他收入", [100, 60, 30, 15], "other", "亿"),
    ("净利率", [0.30, 0.20, 0.12, 0.08, 0.04], "margin", "pct"),
]:
    print(f"  {label}")
    for v in vals:
        p = dict(base); p[key] = v
        r = ni(p["pool"], p["share"], p["other"], p["margin"])
        mark = "  ← 基准" if v == base[key] else ""
        shown = f"{v:.0%}" if fmt == "pct" else f"{yi(v):.0f}亿"
        print(f"    {'':<13}{shown:>10}{yi(r):>16.0f}{(r/base_ni-1):>11.0%}{mark}")

print("\n" + "=" * 94)
print("各档情景的 2036 净利与相对当前 TTM（2262.6 亿美元）的比例")
print("=" * 94)
ttm = D("226.26")
for label, pool, share, other, margin in [
    ("本文最差情景", 600, 0.15, 30, 0.08),
    ("本文次差情景", 900, 0.20, 50, 0.12),
    ("温和熊市", 1200, 0.30, 60, 0.25),
    ("中性熊市", 1500, 0.35, 80, 0.30),
    ("乐观熊市", 2000, 0.40, 100, 0.35),
    ("基准情景", 2000, 0.45, 100, 0.40),
]:
    r = ni(pool, share, other, margin)
    print(f"  {label:<10} 池{yi(pool):>6.0f}亿 份额{share:>5.0%} 其他{yi(other):>5.0f}亿 "
          f"净利率{margin:>5.0%}  →  净利 {yi(r):>7.0f} 亿  = 当前 TTM 的 {r/ttm:>6.1%}")

print("\n" + "=" * 94)
print("『打到最差』的参数门槛：哪些参数组合才等于或低于 96 亿美元")
print("=" * 94)
print("  在最差情景的池(6000亿)与份额(15%)下：")
for m in (0.04, 0.06, 0.08, 0.10, 0.12):
    r = ni(600, 0.15, 30, m)
    print(f"    净利率 {m:.0%}  →  净利 {yi(r):>5.0f} 亿")
print("  在最差情景的池(6000亿)与净利率(8%)下：")
for s in (0.05, 0.10, 0.15, 0.20, 0.30):
    r = ni(600, s, 30, 0.08)
    print(f"    份额 {s:.0%}  →  净利 {yi(r):>5.0f} 亿")
print("  在最差情景的份额(15%)与净利率(8%)下，池需要多大才等于 96 亿：")
pool_needed = (D("9.6") / D("0.08") - 30) / D("0.15")
print(f"    池 {yi(pool_needed):.0f} 亿美元（= 高盛口径 2026 年五家超大规模厂商 AI 基建开支 8000 亿的 {pool_needed/800*100:.0f}%）")
