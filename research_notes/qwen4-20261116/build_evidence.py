"""Reproduce the report's arithmetic and figure; no inference API is called."""
from decimal import Decimal as D
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
ASSET = ROOT / "reports/AI产业研究/assets/qwen4-20261116"
ASSET.mkdir(parents=True, exist_ok=True)

# Values transcribed from the primary publishers on 2026-11-16.
rows = [
    ["Claude Fable 5.2", "71.31", "17.94", "43m42s"],
    ["Claude Sonnet 5.5", "70.85", "16.18", "1h26m"],
    ["Gemini 4 Carbon", "70.45", "10.51", "47m45s"],
    ["Claude Opus 5.5", "70.14", "24.77", "1h25m"],
    ["GPT-6 Astra", "65.02", "21.28", "33m39s"],
    ["GPT-6.1 Sol", "63.94", "3.61", "44m24s"],
    ["Qwen4-Max", "63.20", "9.33", "64m39s"],
    ["Kimi K3.1 Pro", "62.52", "6.44", "63m36s"],
    ["DeepSeek V4.1 Flash 1017", "61.26", "0.66", "39m55s"],
    ["GLM 5.3", "59.85", "8.52", "1h04m"],
    ["Hy4", "59.35", "1.72", "51m31s"],
    ["Qwen3.8-Max-0902", "59.05", "8.73", "105m46s"],
    ["MiMo V2.6 Pro", "57.81", "0.43", "1h13m"],
    ["Step 5 Preview", "54.76", "2.73", "1h05m"],
    ["MiniMax M3.1 Flash", "53.78", "0.66", "43m18s"],
]
prices = [
    ["Qwen4-Max", "1.5", "4.5"],
    ["Qwen3.8-Max-0902", "2", "6"],
    ["GPT-6.1 Sol", "2", "10"],
    ["Claude Fable 5.2", "8", "40"],
    ["Claude Opus 5.5", "4", "20"],
    ["Claude Sonnet 5.5", "2", "10"],
    ["Gemini 4 Carbon promotional", "2", "10"],
    ["Gemini 4 Carbon from 2026-12-01", "4", "20"],
    ["Kimi K3.1 Pro (Vals-listed price)", "2", "10"],
    ["GLM 5.3", "1.4", "4.4"],
    ["DeepSeek V4.1 Flash peak", "0.3", "1.2"],
    ["DeepSeek V4.1 Flash off-peak", "0.15", "0.6"],
    ["MiniMax M3.1 Flash", "0.15", "0.6"],
]

def pct(new, old):
    return str((D(str(new)) / D(str(old)) - 1) * 100)

calculations = {
    "active_parameter_change_pct": pct(71, 95),
    "cn_input_price_change_pct": pct(10, 12),
    "international_input_price_change_pct": pct("1.5", 2),
    "cn_implicit_cache_read_change_pct": pct("0.5", "1.5"),
    "vals_score_change_pp": str(D("63.20") - D("59.05")),
    "vals_cost_change_pct": pct("9.33", "8.73"),
    "vals_duration_change_pct": pct(64*60+39, 105*60+46),
    "terminal_score_change_pp": str(D("48.48") - D("38.89")),
    "terminal_cost_change_pct": pct("3.90", "12.15"),
    "terminal_duration_change_pct_rounded_inputs": pct(75, 143),
    "work360_score_change_pp": str(D("52.69") - D("47.74")),
    "work360_en_cost_change_pct": pct("1.67", "4.43"),
    "work360_cn_cost_change_pct": pct("11.16", "26.58"),
    "cache_example_no_cache_rmb": str(D("20") * D("0.1") * D("10")),
    "cache_example_5m_rmb": str(D("0.1")*D("12.5") + D("19")*D("0.1")*D("0.5")),
    "cache_example_savings_pct": str((1-D("2.2")/D("20"))*100),
    "future_base_scenario_cost_index": str(D("100")*D("0.6")**3),
    "future_fast_scenario_cost_index": str(D("100")*D("0.4")**3),
    "future_slow_scenario_cost_index": str(D("100")*D("0.85")**3),
}
data = {
    "retrieved_on": "2026-11-16",
    "vals_index_version": "2.2; publisher date 2026-11-15",
    "vals_source": "https://www.vals.ai/benchmarks/vals_index",
    "duration_detail_sources": ["https://www.vals.ai/models/alibaba_qwen4-max", "https://www.vals.ai/models/alibaba_qwen3.8-max-0902", "https://www.vals.ai/models/kimi_kimi-k3.1-pro"],
    "vals_columns": ["model", "score_pct", "cost_per_test_usd", "duration"],
    "vals_rows": rows,
    "price_columns": ["model", "uncached_input_usd_per_million", "output_usd_per_million", "hypothetical_100k_input_10k_output_usd"],
    "price_rows": [r+[str(D(r[1])*D("0.1")+D(r[2])*D("0.01"))] for r in prices],
    "calculations": calculations,
    "limitations": "No paid API calls or first-hand model tests. Prices are region/provider/time-specific. Equal-token arithmetic is not equal-work cost. Benchmark durations are not decode speeds. Future cost indices are illustrative assumptions, not forecasts from a source.",
}
(OUT / "evidence.json").write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n")

# Execute the repository-mandated calculation tool and retain its output too.
expressions = ["(71/95-1)*100", "(10/12-1)*100", "(1.5/2-1)*100", "63.20-59.05", "(9.33/8.73-1)*100", "((64*60+39)/(105*60+46)-1)*100", "48.48-38.89", "(3.9/12.15-1)*100", "(75/143-1)*100", "0.1*12.5+19*0.1*0.5"]
logs = []
for expr in expressions:
    result = subprocess.run([sys.executable, str(ROOT/"tools/financial_rigor.py"), "calc", "--expr", expr], capture_output=True, text=True, check=True)
    logs.append(result.stdout)
(OUT/"calculation-tool-output.txt").write_text("\n".join(logs))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(12, 7), dpi=170)
fig.set_facecolor("#f6f8fc")
ax.set_facecolor("#f6f8fc")
chosen = {"Claude Fable 5.2":(-8,12), "Gemini 4 Carbon":(-10,-17), "GPT-6.1 Sol":(-10,13), "Qwen4-Max":(10,5), "Kimi K3.1 Pro":(-5,-18), "DeepSeek V4.1 Flash 1017":(8,10), "Qwen3.8-Max-0902":(10,-4), "MiniMax M3.1 Flash":(8,9)}
for name, score, cost, duration in rows:
    if name not in chosen:
        continue
    color = "#6946cc" if name == "Qwen4-Max" else "#95a2b6" if name == "Qwen3.8-Max-0902" else "#197f91"
    ax.scatter(float(cost), float(score), s=125 if name=="Qwen4-Max" else 60, color=color, zorder=4)
    dx,dy = chosen[name]
    ax.annotate(name, (float(cost),float(score)), xytext=(dx,dy), textcoords="offset points", fontsize=10, ha="right" if dx<0 else "left", color="#182b43", weight="bold" if name=="Qwen4-Max" else "normal")
ax.annotate("", xy=(9.33,63.20), xytext=(8.73,59.05), arrowprops=dict(arrowstyle="->", color="#6946cc", lw=1.8))
ax.set_xscale("log")
ax.set_xlim(.45,35)
ax.set_ylim(51,74)
ax.set_xticks([.5,1,2,5,10,20])
ax.set_xticklabels(["$0.5","$1","$2","$5","$10","$20"])
ax.set_xlabel("Published cost / test (USD, logarithmic scale)", labelpad=12)
ax.set_ylabel("Vals Index score (%)", labelpad=10)
ax.grid(alpha=.20)
for spine in ax.spines.values():
    spine.set_visible(False)
fig.suptitle("Qwen4-Max: higher score, not the lowest task cost", x=.10, y=.96, ha="left", fontsize=19, weight="bold", color="#182b43")
fig.text(.10,.905,"Selected models | Vals Index v2.2 | Snapshot retrieved 16 Nov 2026",fontsize=11,color="#526079")
fig.text(.10,.03,"Source: Vals AI. Arrow: Qwen3.8-Max-0902 to Qwen4-Max. Model settings differ; this is not a universal quality ranking.",fontsize=9,color="#526079")
fig.subplots_adjust(left=.10,right=.96,top=.85,bottom=.14)
fig.savefig(ASSET/"quality-cost.png", facecolor=fig.get_facecolor())
plt.close(fig)
print(json.dumps(calculations, indent=2))
