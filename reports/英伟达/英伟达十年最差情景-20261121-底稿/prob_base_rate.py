"""历史基准率：站在利润峰值上的科技/半导体公司，十年后净利跌到多少？

用途：给"英伟达十年后最差情景"定概率。英伟达当前站在利润峰值上，
      最差情景是净利跌到峰值的 4.2%（仍盈利）。因此正确的历史对照是
      "从峰值出发、十年内跌到峰值的 5% 以内、且期间未转亏"。

方法：
  1. 样本：39 家可比公司（半导体 + 大型科技 + 工业对照）的年度净利，
     全部来自 SEC EDGAR XBRL companyconcept（NetIncomeLoss），一手。
  2. 起点：必须是该公司截至当时的利润峰值年；同公司起点间隔 ≥5 年。
  3. 观测：起点之后 5-10 年窗口内的净利谷底 ÷ 起点峰值。
  4. 关键口径拆分：谷底为负（公司转亏）与谷底为正（仍盈利）分开统计。
     英伟达最差情景是"利润极低但仍盈利"，只应与后者对照。

运行：python3 prob_base_rate.py
依赖：requests 不用，仅标准库；首次运行会向 SEC 拉取数据并缓存到 ./xbrl_cache/
"""
import datetime
import json
import math
import os
import subprocess
import time

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "xbrl_cache")
os.makedirs(CACHE, exist_ok=True)
UA = "ai-berkshire research"

CIKS = {
    "INTC": 50863, "AMD": 2488, "QCOM": 804328, "TXN": 97476, "MU": 723125,
    "ADI": 6281, "AVGO": 1730168, "NXPI": 1413447, "CSCO": 858877,
    "IBM": 51143, "ORCL": 1341439, "MSFT": 789019, "AAPL": 320193,
    "AMZN": 1018724, "GOOGL": 1652044, "META": 1326801, "DELL": 1571996,
    "HPQ": 47217, "WDC": 106040, "PFE": 78003, "JNJ": 200406, "KO": 21344,
    "XOM": 34088, "CVX": 93410, "BA": 12927, "GE": 40545, "T": 732717,
    "VZ": 732712, "NTAP": 1002047, "SNPS": 883241, "MCHP": 827054,
    "LRCX": 707549, "AMAT": 6951, "KLAC": 319201, "CIEN": 936395,
    "ADBE": 796343, "CRM": 1108524, "HPE": 1645590, "QRVO": 1383058,
}

GROUPS = {
    "半导体": {"INTC", "AMD", "QCOM", "MU", "ADI", "AVGO", "NXPI", "MCHP", "QRVO",
             "SNPS", "LRCX", "KLAC", "AMAT", "WDC", "TXN"},
    "大型科技/平台": {"MSFT", "AAPL", "AMZN", "GOOGL", "META", "ORCL", "CSCO", "IBM",
                "DELL", "HPQ", "HPE", "CIEN", "NTAP", "ADBE", "CRM"},
    "其他/对照": {"KO", "JNJ", "PFE", "XOM", "CVX", "BA", "GE", "T", "VZ"},
}


def fetch(cik, tag="NetIncomeLoss"):
    path = os.path.join(CACHE, f"{cik}_{tag}.json")
    if os.path.exists(path) and os.path.getsize(path) > 500:
        return json.load(open(path))
    url = (f"https://data.sec.gov/api/xbrl/companyconcept/"
           f"CIK{cik:010d}/us-gaap/{tag}.json")
    r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", UA, url],
                       capture_output=True, text=True)
    try:
        j = json.loads(r.stdout)
    except Exception:
        return None
    if "units" not in j:
        return None
    json.dump(j, open(path, "w"))
    time.sleep(0.2)
    return j


def annual(j):
    """取 10-K 里的年度观测，单位换算为百万美元。"""
    out = {}
    for rows in j.get("units", {}).values():
        for r in rows:
            if not r.get("start") or not r.get("end"):
                continue
            days = (datetime.date.fromisoformat(r["end"])
                    - datetime.date.fromisoformat(r["start"])).days
            if not (330 < days < 400):
                continue
            if r.get("form") not in ("10-K", "10-K/A"):
                continue
            key = r["end"]
            if key not in out or r.get("filed", "") > out[key][1]:
                out[key] = (r["val"], r.get("filed", ""))
    return {int(k[:4]): v[0] / 1e6 for k, v in out.items()}


def wilson(h, n, z=1.96):
    """二项比例的 Wilson 95% 置信区间。"""
    if n == 0:
        return (0.0, 0.0)
    p = h / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    hw = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - hw), min(1.0, c + hw))


def load_series():
    ni, rev = {}, {}
    for tic, cik in CIKS.items():
        j = fetch(cik)
        if not j:
            continue
        s = annual(j)
        if len(s) < 6:
            continue
        ni[tic] = s
        for tag in ("Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax"):
            b = fetch(cik, tag)
            if b:
                rev[tic] = annual(b)
                break
    return ni, rev


def observations(series, min_span=5):
    """起点须为截至当时的峰值年；同公司起点间隔 ≥5 年；窗口 ≥min_span 年。"""
    ys = sorted(series)
    out = []
    for s in ys:
        hist = [(y, series[y]) for y in ys if y <= s and series[y] > 0]
        if not hist:
            continue
        py, pv = max(hist, key=lambda kv: kv[1])
        if s != py or any(abs(s - o[0]) < 5 for o in out):
            continue
        win = [y for y in range(s + 1, s + 11) if y in series]
        if len(win) < min_span:
            continue
        tr = min(series[y] for y in win)
        out.append((s, pv, tr, tr / pv, len(win)))
    return out


def build(ni, min_span=5):
    rows = []
    for tic, series in sorted(ni.items()):
        for o in observations(series, min_span):
            rows.append({"tic": tic, "peak_year": o[0], "peak": o[1], "trough": o[2],
                         "ratio": o[3], "span": o[4]})
    return rows


def rate(rows, thr):
    if not rows:
        return (0.0, 0, 0)
    hit = sum(1 for r in rows if r["ratio"] <= thr)
    return (hit / len(rows) * 100, hit, len(rows))


ni, rev = load_series()
print(f"样本 {len(ni)} 家公司，{sum(len(v) for v in ni.values())} 个年度净利观测"
      f"（SEC EDGAR XBRL NetIncomeLoss）\n")
print("注：收入序列仅用于说明口径问题（第三节），不参与概率计算。\n")

r5 = build(ni, 5)
r10 = build(ni, 10)
pos5 = [r for r in r5 if r["trough"] > 0]
pos10 = [r for r in r10 if r["trough"] > 0]

print("=" * 92)
print("一、基准率与「谷底是否仍为正」的拆分")
print("=" * 92)
for label, rows, pos in (("窗口≥5年", r5, pos5), ("完整10年窗口", r10, pos10)):
    print(f"\n【{label}】观测 {len(rows)} 个，公司 "
          f"{len(set(r['tic'] for r in rows))} 家")
    neg = len(rows) - len(pos)
    print(f"  谷底为负（公司转亏）: {neg} = {neg/len(rows)*100:.1f}%")
    print(f"  谷底为正（仍盈利）  : {len(pos)} = {len(pos)/len(rows)*100:.1f}%")
    for thr in (0.20, 0.10, 0.05, 0.02):
        a, h, n = rate(rows, thr)
        b, h2, n2 = rate(pos, thr)
        lo, hi = wilson(h2, n2)
        print(f"    谷底≤峰值{thr*100:>4.0f}%   全样本 {h:>2}/{n:<2}={a:>5.1f}%"
              f"    仅仍盈利 {h2:>2}/{n2:<2}={b:>5.1f}%"
              f"  95%CI [{lo*100:>4.1f}%, {hi*100:>5.1f}%]")

print("\n" + "=" * 92)
print("二、分行业（仅仍盈利口径）")
print("=" * 92)
for gname, members in GROUPS.items():
    sub = [r for r in pos5 if r["tic"] in members]
    if not sub:
        continue
    print(f"\n  {gname}（n={len(sub)}）")
    for thr in (0.05, 0.10, 0.20, 0.40):
        b, h2, n2 = rate(sub, thr)
        lo, hi = wilson(h2, n2)
        print(f"    ≤峰值 {thr*100:>3.0f}%: {h2:>2}/{n2:<2} = {b:>5.1f}%"
              f"   95% CI [{lo*100:>4.1f}%, {hi*100:>5.1f}%]")
    med = sorted(r["ratio"] for r in sub)[len(sub) // 2]
    print(f"    中位谷底/峰值: {med*100:.1f}%")
    deep = [r for r in sub if r["ratio"] <= 0.20]
    if deep:
        print("    跌到 20% 以内的案例: " +
              ", ".join(f"{r['tic']} {r['peak_year']}→{r['ratio']*100:.1f}%"
                        for r in sorted(deep, key=lambda r: r["ratio"])))

print("\n" + "=" * 92)
print("三、按峰值净利率分层 —— 已弃用（口径不可靠，见下）")
print("=" * 92)
print("""
净利率分层本来想回答"英伟达 55.6% 的峰值净利率在样本之外，是更抗跌还是更脆弱"。
结论：无法用 SEC XBRL 的收入标签可靠构建，故不采用。

原因：us-gaap:Revenues 对不同公司含义不同。对 AAPL（FY2016 215,639 百万）、
GOOGL（FY2023 307,394 百万）、META（FY2016 27,638 百万）它是公司总收入，
数字与公开财报一致；但对 CRM 是分部口径——CRM FY2016 总收入公开值为 10,014 百万，
而 XBRL 的 Revenues 给出 6,667 百万（FY2017 为 8,392，而公开值为 11,996）。
同一标签混着"公司总收入"和"某个分部收入"，用它算净利率会系统性高估分母缺失公司的利润率。

同时 us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax 只在 ASC 606
之后的公司有（AMZN/INTC/NXPI/TXN/WDC），与 Revenues 无交集，无法交叉校验。

因此本报告不用净利率分层作为概率证据。英伟达"不会像 31.1% 的历史样本那样转亏"
这一判断改由资产负债表支撑：净现金 211 亿美元、fabless 模式下 9M FY2027 资本开支
仅 88.56 亿美元（占收入 3.0%），这些数字取自 SEC 8-K，不依赖分部的收入口径。
""")

print("三之二、附：口径异常的样例（供复核）")
print("=" * 92)
for tic, cik, tag in (("CRM", 1108524, "Revenues"),
                      ("AAPL", 320193, "Revenues"),
                      ("GOOGL", 1652044, "Revenues")):
    j = fetch(cik, tag)
    if not j:
        continue
    s = annual(j)
    last = sorted(s)[-3:]
    print(f"  {tic:6s} {tag}: " +
          ", ".join(f"{y}={s[y]:,.0f}M" for y in last))
print("  CRM 的公开总收入 FY2016 为 10,014M、FY2017 为 11,996M，"
      "与上表 6,667M / 8,392M 不符 → 该公司的 Revenues 是分部口径")

print("\n" + "=" * 92)
print("四、与英伟达最差情景同类的历史案例（仍盈利且谷底≤峰值 20%）")
print("=" * 92)
for r in sorted([x for x in r5 if x["trough"] > 0 and x["ratio"] <= 0.20],
                key=lambda r: r["ratio"]):
    print(f"  {r['tic']:6s} 峰值 {r['peak_year']}年 {r['peak']:>10,.0f}M → "
          f"谷底 {r['trough']:>10,.0f}M = {r['ratio']*100:>6.1f}%  (窗口{r['span']}年)")

print("\n" + "=" * 92)
print("五、写入报告的最终口径")
print("=" * 92)
for thr in (0.05, 0.10, 0.20, 0.40):
    b, h2, n2 = rate(pos5, thr)
    lo, hi = wilson(h2, n2)
    print(f"  仍盈利样本 谷底≤峰值{thr*100:>3.0f}%: {h2}/{n2} = {b:.1f}%"
          f"   95% CI [{lo*100:.1f}%, {hi*100:.1f}%]")
print(f"\n  英伟达最差情景 = 当前 TTM 净利 2262.6 亿美元的 4.2%")
print(f"  → 对应「仍盈利样本中谷底 ≤ 峰值 5%」这一档")
b, h2, n2 = rate(pos5, 0.05)
lo, hi = wilson(h2, n2)
print(f"  → 历史频率 {b:.1f}%（{h2}/{n2}），95% CI [{lo*100:.1f}%, {hi*100:.1f}%]")

out = {"rows": r5, "rows_10y": r10,
       "still_profitable_5y": pos5, "still_profitable_10y": pos10}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "base_rate_rows.json"), "w"), indent=1)
print("\n底稿已写出：base_rate_rows.json")
