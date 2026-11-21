"""基准率的分层检验：起点年代与宏观环境是最大混淆因素。

问题：40.5% 的观测跌到峰值 20% 以下，但其中不少起点在 2007-2010 年，
      紧接着就是全球金融危机加半导体超级周期崩塌。这批观测不能直接
      外推到"2026 年从一个 AI 周期高点出发"。

分层：
  甲. 全部观测
  乙. 排除 2007-2010 年起点（金融危机与周期顶）
  丙. 再排除 2020 年起点（疫情一次性冲击）
  丁. 只看 2011 年后起点的观测

数据：base_rate_rows.json，由 prob_base_rate.py 生成（SEC EDGAR XBRL 一手）。
运行顺序：先 python3 prob_base_rate.py，再 python3 prob_era.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, "base_rate_rows.json")))["rows"]

GROUPS = {
    "半导体": {"INTC", "AMD", "QCOM", "MU", "ADI", "AVGO", "NXPI", "MCHP", "QRVO",
             "SNPS", "LRCX", "KLAC", "AMAT", "WDC", "TXN"},
    "大型科技/平台": {"MSFT", "AAPL", "AMZN", "GOOGL", "META", "ORCL", "CSCO", "IBM",
                "DELL", "HPQ", "HPE", "CIEN", "NTAP", "ADBE", "CRM"},
    "其他/对照": {"KO", "JNJ", "PFE", "XOM", "CVX", "BA", "GE", "T", "VZ"},
}


def rate(sub, thr=0.20):
    if not sub:
        return 0.0, 0, 0
    hit = sum(1 for r in sub if r["ratio"] <= thr)
    return hit / len(sub) * 100, hit, len(sub)


def show(label, sub):
    a, h, n = rate(sub)
    p = [r for r in sub if r["trough"] > 0]
    b, h2, n2 = rate(p)
    print(f"  {label:<34} n={n:>3}   全部≤20%: {a:>5.1f}%   "
          f"仅仍盈利≤20%: {b:>5.1f}% (n={n2})")


print("=" * 92)
print("起点年代分层（谷底 ÷ 峰值 ≤ 20% 的命中率）")
print("=" * 92)
show("甲. 全部观测", rows)
show("乙. 排除 2007-2010 年起点", [r for r in rows if not (2007 <= r["peak_year"] <= 2010)])
show("丙. 再排除 2020 年起点",
     [r for r in rows if not (2007 <= r["peak_year"] <= 2010) and r["peak_year"] != 2020])
show("丁. 只看 2011 年后起点", [r for r in rows if r["peak_year"] >= 2011])

print("\n" + "=" * 92)
print("行业分层")
print("=" * 92)
for gname, members in GROUPS.items():
    sub = [r for r in rows if r["tic"] in members]
    if not sub:
        continue
    p = [r for r in sub if r["trough"] > 0]
    a, h, n = rate(sub)
    b, h2, n2 = rate(p)
    med = sorted(r["ratio"] for r in p)[len(p) // 2] if p else float("nan")
    print(f"  {gname:<16} 全部 n={n:>3} ≤20%: {a:>5.1f}%   "
          f"仅仍盈利 n={n2:>3} ≤20%: {b:>5.1f}%   中位谷底/峰值: {med*100:>6.1f}%")

print("\n" + "=" * 92)
print("结论：剔除金融危机与疫情起点后，基准率不下降，说明 40% 不是宏观偶然")
print("=" * 92)
