# Bottleneck Hunter Signal Scan — 2026-06-25 21:00
**Scan 284**

---

## ♻️ Signal reactivation: Bromide/HBr — Semiconductor etching chain A-level bottleneck (master-map 0b, archived on 2026-05-26, real-time monitoring added in this round)

### Bottleneck location

**Layer 3 → Layer 2**: Liquid bromine (raw material) → Semiconductor grade hydrobromic acid HBr gas (process chemicals) → DRAM/NAND transistor structure etching

HBr is a key process gas for etching transistor trenches in DRAM and NAND Flash manufacturing and cannot be replaced. Every DRAM/NAND wafer requires high-purity HBr.

### Supply concentration (extreme concentration)

| Region | Proportion of global bromine production | Representative companies |
|------|------------|---------|
| Israel | ~46.5% | ICL Group (Dead Sea extraction, the world’s largest, 280,000 tons/year) |
| Jordan | ~25.6% | Jordan Bromine Company (ICL + Japanese joint venture, unlisted) |
| United States | ~15-20% | Albemarle, Lanxess United States Division |
| Rest | <15% | Dispersion |

**Israel + Jordan = approximately 72% of global production. **

Downstream semiconductor-grade HBr conversion capabilities: Resonac (Japan, formerly Showa Denko), Air Liquide, Adeka - but their total production capacity is 100% locked in the existing contracts of TSMC/Samsung/SK Hynix/SMIC. **There is no excess conversion capacity outside Israel that can be replaced. **

### Bottleneck determination (6 criteria)

| # | Criteria | Rating | Description |
|---|------|------|------|
| 1 | Supply concentration | 🔴 | Israel + Jordan = 72%, ICL Group is the largest single supplier |
| 2 | Expansion cycle | 🔴 | New bromine extraction/conversion capacity > 2 years certification + construction |
| 3 | Substitution difficulty | 🔴 | Semiconductor etching cannot bypass HBr, there is no equivalent substitute |
| 4 | Capacity Utilization Rate | 🟡 | Under the geopolitical pressure of the Iran war, Israeli factories are still operating but there is a risk of intermittent interruptions in production capacity |
| 5 | Demand growth rate | 🔴 | AI driven DRAM/HBM demand >50%/year |
| 6 | Customer Verification Cycle | 🔴 | New Supplier Certification>1 Year |

**→ 4 red lights: Level A bottleneck**

### Geographical risk quantification

- 97.5% of South Korea’s bromine imports come from Israel (Source: TrendForce/Digitimes, 2026-04-17)
- The Iranian missile landed within 35 kilometers of the ICL Dead Sea extraction complex** (Source: War on the Rocks)
- South Korea's Samsung+SK Hynix accounts for approximately 50% of global DRAM production capacity and is directly dependent on Israeli bromine
- Bromine prices have soared to **$12,000/MT** (Source: Manufacturing Dive 2026)
- Gasworld rates bromine risk as "more dangerous than helium" (Source: gasworld 2026)

### Why wasn’t it tracked before?

Bromide/HBr has been included in the master-map (0b entry) as a level A bottleneck on 2026-05-26, but it has not been included in active monitoring in the 280+ rounds of hourly scans. This round of searches touched on this signal again and added key new data: the Iranian missile landing point is 35km away from the ICL Dead Sea factory, the bromine price is $12,000/MT, and South Korea relies 97.5% on quantification (confirmed by TrendForce 2026-04-17). Along with helium (fab cooling/atmosphere), HBr is responsible for the DRAM/NAND etching step. **If both are stressed at the same time, AI chip manufacturing is doubly hindered**.

### Evaluation of investable targets

#### ICL Group (NYSE: ICL)

| Metrics | Data | Sources |
|------|------|------|
| Market Cap | ~$7.2-8.6B | stockanalysis.com (estimate) |
| 2025 Revenue | $7.15B | Company Financial Report |
| Q1 2026 Revenue | $2.02B (+14% YoY) | — |
| PS | ~0.9-1.2x | Estimate |
| PE | Not confirmed (need to be verified) | — |
| Bromine business share | ~30-35% (industrial products segment, estimated) | — |

**But ICL is not multi-standard**:
- ICL is an Israeli company and the facility itself is in a geo-risk zone. If Israel is hit, ICL is the victim, not the beneficiary
- ICL share price rises on higher bromine prices (operating profit expansion) but also faces factory disruption risk
- This is a double-edged sword, not the logic of traditional bottleneck suppliers benefiting

#### Resonac Holdings (4004.T)

- Japanese HBr conversion downstream supplier, semiconductor materials business
- However, HBr accounts for a very small proportion of Resonac’s total revenue and does not meet the >30% purity requirement
- ❌ Does not meet the initial screening criteria

#### Jordan Bromine Company

- ICL is a joint venture with a Japanese businessman, **unlisted**, and cannot be invested.

#### Albemarle Corporation (ALB)

- U.S. bromine + lithium chemicals, bromine business accounts for about 20%
- ❌ Insufficient purity, and US bromine production capacity cannot quickly replace Israel

**Conclusion: There is no pure target that meets the preliminary screening conditions (bottleneck business >30%+listed+investable). **

---

## Stock signal status (no change in this round)

| Bottleneck | Level | Status | Latest |
|------|------|------|------|
| WF6 tungsten fluoride | S grade | 🔴 unchanged | T=6 days (7/1 Kanto Denka+Central Glass permanently discontinued), Foosung CSSC certification in progress |
| LEU/Centrus Option 1b | ★★★ (binary event) | Highest priority | T=5 days (6/30), DOE still has zero announcements, stock price $171.80 |
| Helium (Barzan/Qatar) | S-level | 🔴 Unchanged | After the explosion (13 dead and 66 injured, restart delayed), S-level maintained |
| ABF substrate (Ajinomoto) | S grade | 🔴 unchanged | Q3+30% price increase, delivery time 28 weeks, gap extended to the end of 2027 |
| InP/EML laser | S-level | 🔴 Unchanged | Monthly demand for 700-800k wafers, supply only 400k, NVIDIA $4B locked in Lumentum+Coherent |
| PGME/PGMEA | Level A | 🟡 Unchanged | Downgraded to Level A (Horwuz will reopen on 6/18 + TOK Koriyama will restart to be confirmed) |
| Bromide/HBr | **Grade A** | 🟡Add real-time monitoring | master-map 0b (2026-05-26), ICL has no pure targets (the industrial products department accounts for only 17.3%), new additions in this round: missile 35km risk + price $12,000/MT confirmed |

---

## Watchlist target status (no change in this round)

| Target | Rating | Price | Change |
|------|------|------|------|
| LEU (Centrus) | ★★★ (binary) | $171.80 | No change, T=5 days highest priority |
| CHG (Chemring) | ★★★★ | GBX~500 | $300M-$345M DoW contract has been entered and remains unchanged |
| AAOI | ★★★ | $146-153 range | Slightly weaker today, no new catalyst; 7/1 1.6T shipment is a known event, 7/30 Q2 financial report is key |
| Nittobo (3110.T) | ★★★★ | Around ¥19,500 | T=4 days (6/29 5:1 split record day), unchanged |
| ALM (Almonty) | ★★★ | — | T=4 days (Russell 1000 inclusion takes effect on 6/29), unchanged |
| Foosung (093370) | ★★ | PE~93x🟡 | WF6 CSSC certification in progress, unchanged |
| KDK (4047.T) | Exit warning | ¥3,560 | T=6 days (7/1 WF6 discontinued → Exit) |
| COHR | ★★★(Observation) | — | Valuation yellow light, waiting for PE<40x |
| AXT | ★★(Observation) | — | InP S-level verification reference, valuation red light |

---

## Next step suggestions

1. **Bromide/HBr**: Added to the watchlist this round as a level A bottleneck signal. There are currently no pure investment targets. Follow-up research directions:
   - Looking for semiconductor materials companies with independent HBr production capacity outside Israel
   - Monitor ICL company announcements (whether there is a US/European capacity transfer plan)
   - If an acute interruption occurs → upgrade to S level immediately

2. **LEU T=5 days**: 6/30 DOE Option 1b is determined to be the highest priority binary risk. Monitor closely every hour.

3. **WF6 T=6 days**: The permanent suspension of production will actually occur on July 1, please pay attention to the Foosung CSSC certification progress announcement.

---

*Signal sources: gasworld, Digitimes (2026-04-15/17), TrendForce (2026-04-17), War on the Rocks, EE Times, Manufacturing Dive, Fortune*
