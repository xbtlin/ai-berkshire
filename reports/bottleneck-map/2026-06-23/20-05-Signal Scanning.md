# Bottleneck Hunter Signal Scan — 2026-06-23 20:05

**This round of scanning** (the 16th round, covering five super trends)

---

## Conclusion of this round

**There is no new independent bottleneck, but the S-level bottleneck has been tracked and has important status activation**:

1. **Helium S-Class - The buffer stock depletion window has arrived**: Today it has entered the Korean FAB buffer stock depletion range predicted by analysts (May-July 2026). The war ended on 6/17, but the Ras Laffan South Station will be repaired by the end of the year at the earliest and will be fully repaired in 3-5 years. "The crisis really begins only after the ceasefire" has become the consensus of analysts. The decline in South Korea's wafer production will affect the actual shipments of HBM/DRAM in Q3 2026. For the first time this round, this activation status was clearly recorded in today’s 15th round of scans.
2. **Transformer delivery time**: New data point - delivery time has been extended to **4 years** (further deteriorating from the "24-30 months" recorded in May), and only 5GW of the 12GW plan has started construction.
3. **EML/Optical Module**: There is a "serious shortage" of 200G EML. NVIDIA directly intervenes in suppliers to expand production - strengthening the InP S-level signal, but there is no new valuation qualified target.

---

## Signal 1: Helium S-level - status activation confirmation (tracked, major status changes)

### Known background (master-map 0a entry, established on 2026-05-26)

- **Triggering event**: 2026-02-28 Iranian missile strikes Ras Laffan, Qatar suspends production; in April of the same year, Russia implemented export controls on helium until the end of 2027
- **Supply Gap**: Qatar accounts for 33% of the world, and South Korea relies on Qatar for 65% of helium → the merger will remove about 40-45% of South Korea’s available helium
- **Irreplaceable**: EUV lithography machine cooling, ion implantation wafer cooling, vacuum leak detection - no commercially viable substitutes
- **Repair cycle**: 3-5 years (QatarEnergy CEO statement)

### New data in this round (2026-06-23)

**Status Activation Confirmation: We are now in the Buffer Exhaustion Window**

| Data Points | Content | Sources |
|--------|------|------|
| Buffer depletion window | Analysts predict South Korea's FAB buffer stock depletion range: **May-July 2026**. Today, 6/23, is in the middle of the window | Smith/Valuechainasia/J2 Sourcing |
| Post-war analysis | The war ended on 6/17/2026, but Ras Laffan South Station "will not restart before the end of summer 2026, and will be fully restored in 2029-2031" | QatarEnergy CEO |
| "The crisis begins only after the ceasefire" | Before the ceasefire: contracts and inventories protect production; after the ceasefire buffers are exhausted and physical shortages begin to show | Santiago & Company; Fortune |
| Impact mechanism of wafer production | Within 1-2 weeks after rationing starts → Wafer production decline → Appears in shipment data 8-12 weeks later → **Q3 2026 HBM/DRAM shipments are under pressure** | Valuates Reports; Semiconductors Insight |
| Supply substitution gap | Russia, the United States, and Australia can replace "about half" of the Qatar gap (master-map is known), and the other half has no solution | Previous records |

**War stops ≠ supply resumes, this is the biggest risk of misjudgment at present** (Multiple analyst reports have clearly pointed out)

### Deduction of downstream chain effects

```
Ras Laffan discontinued (2/28)
    ↓ About 90 days buffer stock (3-6 months for large factories, <1 month for small factories)
Korea Samsung/SK Hynix FAB rationing starts (~May)
    ↓ Wafer production output declines after 1-2 weeks
HBM4/HBM3E/DRAM wafer production reduced (~June)
    ↓ 8-12 weeks manufacturing cycle
Q3 2026 HBM/DRAM shipments are under pressure (July-September)
    ↓
NVIDIA/Microsoft/Google order fulfillment delays (possible)
```

### Valuation Qualified Target Inspection

| Company | Ticker | Market Cap | TTM Revenue | P/S | Status | Conclusion |
|------|------|------|---------|-----|------|------|
| Air Products | APD | ~$45 billion | ~$12 billion | 3.7x | Large market cap, already priced | ❌ Does not meet the initial screening (>$100B USD valuation, but $45B actual market cap) |
| Linde | LIN | ~$220 billion | ~$33 billion | 6.7x | Large market capitalization | ❌ Does not meet the initial screening |
| ASP Isotopes | ASPI | ~$978M | ~$23.8M | **41x** | Loss (Q1 2026 net loss $26.7M) | ⚠️ Valuation red light: PS>30x + loss |
| Chart Industries | GTLS | ~$8 billion | ~$4 billion | 2x | Equipment manufacturer, not manufacturer | ❌ Bottleneck Insufficient purity |

**ASPI valuation detailed analysis (updated, vs. May 27 watchlist record)**:
- Market value: $978 million (end of May), an increase of +47% from $664 million on May 27 (nearly doubled within 60 days, signal strength should be downgraded)
- TTM revenue: $23.8 million; Q1 2026 quarter $4.2 million (annualized $16.8 million, but TTM is better)
- P/S: **41x** (further deterioration from 28x on May 27)
- Loss status: TTM net loss $159.8 million (including amortization of Renergen acquisition); Q1 2026 net loss $26.7 million
- Phase 1 helium production capacity: 58MCF/day ≈ ~3.6% of the global daily production gap (limited effect)
- Stock price within 60 days of listing: from $664M → $978M market value, +47%, meeting the red light downgrade condition of "nearly doubling within 60 days"
- **Comprehensive conclusion: P/S 41x + loss + 60-day surge = signal strength capped★★, no tracking**

**Conclusion**: The helium bottleneck is real (S-level confirmed), but there is no pure target that passes the valuation check. The large industrial gas companies have long since priced in, and the smaller pure play companies (ASPI) are overvalued.

---

## Signal 2: Transformer delivery time - 4 years (data update, S-level enhancement)

**Tracked Status**: Data Center Power/Transformer Class S (recorded by master-map)

**New quantitative data for this round**:

| Indicators | Previous records | Current round of data | Changes |
|------|---------|---------|------|
| Delivery time | 24-30 months | **4 years (48 months)** | ↑ Significant deterioration |
| Actual construction starts versus planned | — | **5GW / 12GW (42%)** | New data |
| China controls global production capacity | — | 60% | New data (geo-risk) |

Source: PwC analysts (PV Magazine USA, 2026-05-11); Sightline Climate (2026 tracking data)

**Impact**: 58% of the planned capacity of AI data centers in 2026 faces delays or cancellations. The root cause is the bottleneck of transformers/switching equipment/supporting batteries, not computing hardware.

**Qualified bids for valuation**: No new bids (Transformer manufacturers GE Vernova, ABB, and Siemens all have market values well over $10 billion and have been fully priced)

---

## Signal three: EML/optical module - 200G serious shortage, NVIDIA directly intervenes (A-level enhancement)

**Tracked status**: EML S level, InP substrate S level (master-map has been recorded)

**New data points for this round**:

- **200G EML severe shortage**: TrendForce (2026-04-20) confirmed that "the optical component supply chain is the main bottleneck in capacity expansion"; 200G EML "severe shortage"
- **NVIDIA directly intervenes**: NVIDIA "assisting suppliers" expanded production of 200G EML, indicating that the shortage has reached a level where customers have to intervene personally (Reference: NVIDIA has only done similar operations during severe CoWoS shortages in history)
- **1.6T transformation deepens InP gap**: During the 800G → 1.6T upgrade process, InP usage per unit further increases; McKinsey predicts that 800G transceiver production will reduce demand by 40-60% (before 2027), and 1.6T will decrease by 30-40% (before 2029)

**Impact on tracked signals**: The EML/InP S-level signal is further strengthened and does not affect the existing rating. However, NVIDIA's direct intervention is new verification evidence.

**Valuation qualified target**: refer to existing ratings (IQE ★★★★, AXT valuation red light ★★, Coherent/Lumentum large market capitalization)

---

## Other direction coverage confirmation

| Directions | Search Results | Conclusion |
|------|---------|------|
| LEU/HALEU | Latest 8-K: 6/18 Oklo LOI + Section 382 revision, no DOE Option 1b announcement | T-7 days (historical announcement window T-5=6/25, enter tomorrow) |
| WF6 | No new updates scanned at 19:05, countdown to discontinuation of production on 7/1 T-7 | Maintain S level, fully tracked |
| IQE/Tower | No updates scanned at 16:05 | ★★★★ Maintain, waiting for AGM (6/30) |
| Nittobo 3110.T | 5:1 stock split record date 6/29, T-6 days, no new news | ★★★★maintained, entry range is around ¥19,500 |
| ALM | Russell 1000 takes effect on 6/29 T-6, no new news | ★★★maintained, passive funding effect is approaching |
| Nuclear Power/SMR | No new signals | — |
| Defense/Ammunition | No new signals (Chemring backlog £1.4B, no new announcements) | — |
| Space Economy | No new signals | — |

---

## Watch list status changes

| Target | Change |
|------|------|
| Helium S-level (overall) | **Status activated**: 6/23 enters buffer depletion window, war ends on 6/17 but physical repair takes 3-5 years, Q3 2026 HBM/DRAM shipment risk rises |
| ASPI (ASPI) | Market cap $664M → $978M (+47%), P/S 41x (deterioration), nearly doubled in 60 days → signal downgraded to ★★, maintain "Do Not Track" |
| Transformer bottleneck | Delivery time updated to 4 years (new data), quantified gap between planned vs. actual construction (12GW vs. 5GW) |
| Remaining underlyings | No change |
