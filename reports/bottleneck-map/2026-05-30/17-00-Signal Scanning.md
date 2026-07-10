# Bottleneck signal scan report — 2026-05-30 17:00

**Scan Round**: Round 66
**Scan time**: 2026-05-30 17:00
**Number of signals**: 1 new signal (missed in April 2026 to make up)
**Reason for triggering the report**: The dual supply impact of PGME/PGMEA, the key solvent for photoresist, was not included in the previous 65 rounds.

---

## 🔴 New signal: Dual supply impact of key photoresist solvents (PGME/PGMEA)

**Link**: Semiconductor re-industrialization → AI chip manufacturing chain → Advanced photoresist → Key solvent (Layer 3 material)
**Level Rating**: Level A (preliminary)
**First record**: 2026-05-30 17:00 (missed from 2026-04-24)

### Double Impact Description

**Shock ①: Blockade of the Strait of Hormuz → Naphtha +92% → Tightening of PGME/PGMEA supply**

- In early March 2026, the Iran war led to the partial blockade of the Strait of Hormuz
- Japan naphtha import price +92% (the main chemical precursor of PGME/PGMEA)
- PGME (propylene glycol methyl ether) and PGMEA (propylene glycol methyl ether acetate) are irreplaceable key solvents for EUV/ArF immersion photoresist, accounting for about 70-80% of the weight of the photoresist formula.
- Japan's major photoresist suppliers have notified downstream customers such as Samsung and SK Hynix of supply pressures

**Shock ②: Japan 2026-04-20 7.7 magnitude earthquake → TOK Koriyama Factory + Shin-Etsu Shirakawa Factory suspended production**

- On April 20, 2026, a magnitude 7.7 earthquake occurred in Miyagi Prefecture, Japan
- **TOK (Tokyo Chemical Industry, 4186.T) Koriyama Factory**: About 25% of the world's advanced photoresist production capacity, production will be suspended for 4-6 weeks
  - Note: TOK is also building a new ¥200 billion EUV photoresist factory there (put into production in H2 2026)
- **Shin-Etsu Chemical Shirakawa Plant**: Production suspended for 4-8 weeks
- Both companies have officially notified downstream customers of limited production capacity.

### Supply chain position (Layer analysis)

```
AI chip (GPU/HBM)
  └── Layer 1: TSMC/Samsung EUV process
       └── Layer 2: Advanced photoresist (TOK/JSR/Shin-Etsu/Sumitomo)★Bottleneck layer
            └── Layer 3: PGME/PGMEA solvent ← This impact point
                 └── Layer 4: Naphtha (Homuz blockade → price increase +92%)
```

### Timeline

| event | time | status |
|------|------|------|
| Hormuz blockade started | Early March 2026 | Already happening |
| Naphtha price +92% | March-April 2026 | Occurred (data source: Digitimes 2026-04-24) |
| Japan 7.7 magnitude earthquake | 2026-04-20 | Occurred |
| TOK/Shin-Etsu notifies downstream customers | Around 2026-04-24 | Already occurred |
| Safety stock expected to be depleted | Approximately September-October 2026 | Estimate (~6 months safety stock, TrendForce) |
| EUV photoresist replacement and re-certification | If you need to change suppliers: >1 year | The barriers are extremely high |

**Key Uncertainty**: The 6-month safety stock is an industry estimate from TrendForce and is unofficially disclosed and needs to be tracked continuously.

### Bottleneck assessment (preliminary assessment of 6 standards)

| Standard | Assessment | Description |
|------|------|------|
| Supply concentration | 🔴 | 4 Japanese suppliers account for >90% of global EUV photoresist |
| Production expansion cycle | 🔴 | EUV photoresist new production capacity + certification > 2 years |
| Difficulty of substitution | 🔴 | EUV re-certification >1 year, Samsung/TSMC will not easily change suppliers |
| Capacity utilization rate | 🔴 | It was close to full production before the earthquake, and the new production capacity H2 will not be put into operation until 2026 |
| Demand growth | 🔴 | AI chip production continues to expand, and the number of EUV layers increases to drive photoresist demand |
| Customer verification | 🟡 | Samsung/SK Hynix has received supply notification; TSMC status is not disclosed |

**Preliminary rating: Grade A** (5 red/1 yellow)
Reasons for not being rated S: There is a safety stock buffer of about 6 months, and the critical period is in September-October 2026 rather than immediately; and the supply side is in a competitive relationship with 4 companies, not a single source monopoly.

### Preliminary screening of investable targets

#### TOK (Tokyo Chemical Industry, 4186.T) — Status: Ready to track

| Indicators | Data | Light Color |
|------|------|------|
| Market capitalization | ~¥1.35 trillion ≈ $8.7B USD | ✅ Below the $10B threshold |
| Annual income | ~¥260B (approximately $1.68B) | — |
| P/S (current) | ~5.2x | 🟡 Yellow light (>4x) |
| P/E | **To be verified** | ❓ |
| Photoresist segment revenue share | **To be verified (requires >30% threshold)** | ❓ |
| Business direction | Highly focused on semiconductor process materials/photoresist | ✅ |
| New production capacity | ¥200 billion Koriyama EUV factory (H2 2026) | ✅ Production expansion signal |

**TAM red light inspection**: The global EUV photoresist market is ~$3-4B, and TOK’s market value of $8.7B is close to 20% of the TAM red light warning zone ($3-4B × 20% = $0.6-0.8B trigger line) - but TOK’s revenue is not limited to EUV photoresist, and the segmentation ratio needs to be verified before making a judgment.

**Current conclusion**: P/S 5.2x is a yellow light (not a red light), P/E and segment proportion are missing, and a complete valuation test cannot be completed. **Marked as "preparatory tracking", it has not entered the official watchlist yet, and there is no buying recommendation. **

#### Target excluded

| Company | Reason for exclusion |
|------|----------|
| JSR (No. 2 in photoresist in Japan) | Privatized in 2023 (led by the Japanese government) |
| Shin-Etsu Chemical (4063.T) | Market value ~$44B, too large |
| Sumitomo Chemical (4005.T) | The proportion of photoresist is too low and it is not a pure target |
| Fujifilm (4901.T) | Market value ~$22B, comprehensive group |

### Source verification (6 independent sources)

1. **Seoul Economic Daily 2026-04-24**: The Japanese earthquake has impacted TOK/Shin-Etsu photoresist production capacity, and Samsung/SK Hynix received a supply notice
2. **Digitimes 2026-04-24**: Hormuz blockade → Naphtha +92% → Photoresist solvent supply pressure complete transmission chain
3. **The Elec**: Details of production suspension at TOK Koriyama factory (approximately 25% of global advanced photoresist production capacity)
4. **South China Morning Post (SCMP)**: Comprehensive report on the earthquake impact on the semiconductor material supply chain
5. **TrendForce 2026-04-21**: Double impact analysis of photoresist supply chain, safety stock estimate of about 6 months
6. **BigGo Finance**: TOK (4186.T) market capitalization and financial data

**Cross-validation results**: The date of the earthquake (April 20), the location of the TOK plant (near Koriyama, Fukushima), the time of the Hormuz blockade (early March), and the naphtha increase (+92%) are consistent across multiple sources.

### Relationship to tracked signals

| Tracked Signals | Relationships |
|----------|------|
| WF6/NF3 (item 3b) | Both are semiconductor process chemicals; PGME/PGMEA affects front-end lithography, WF6 affects back-end interconnection, and is an independent bottleneck |
| NF3 Japanese supply chain | Both belong to the Japanese specialty chemicals system, supplementing the verification of the overall vulnerability of Japan's specialized supply chain |
| InP/EML (entry 1/2) | Both belong to the AI chip manufacturing chain and have the same demand-side drivers |

---

## Existing signal status confirmation (round 66)

| Signal | Status | Notes |
|------|------|------|
| WF6 critical window | Day 5 (5/30 17:00), continuous and uninterrupted news | The highest risk window period continues |
| Almonty Phase 2 Voting | June 8 (**9 days**), no new announcements | — |
| Centrus DOE renewal | June 30 (**31 days**), June 15 (**16 days**) = cordon | No new announcements |
| UAMY Annual Meeting | June 12 (**13 days**) | 250M→500M additional decision |
| CHG Nobel Norway Public Consultation | Deadline June 15 (**16 days**) | FID timeline end of 2026 |
| Nittobo (3110.T) | Margin of safety for entry: ¥7,700-10,500 (before split); current price is still overvalued | Keep waiting |
| Kanto Denka (4047.T) | Forward P/S 2.19x / P/E 30.2x (after stock price +42%) | 🟡 Yellow light, ★★★★ maintain |

All S/A/B bottleneck ratings remain unchanged, and all watchlist official target ratings remain unchanged.

---

## Next action

1. **High priority**: Verify TOK (4186.T) P/E and photoresist segment revenue proportion (>30% is the threshold for pure standards)
2. **Continuous Monitoring**: Hormuz situation (naphtha price trend); Japanese TOK/Shin-Etsu plant recovery progress
3. **Time node**: Scanning of the encrypted photoresist supply chain starting from September 2026 (the critical period of safety stock is approaching)
4. **TAM Actuarial**: Accurate verification of TOK photoresist segment revenue, eliminating TAM 20% red light risk

---

*Scan scope: Five super trends (AI infrastructure, energy transition, defense modernization, semiconductor reindustrialization, space economy)*
*New entry in this round: 11d (key solvent for photoresist PGME/PGMEA, preliminary level A), see master-map.md*
*Number of sources: 6 independent sources (Seoul Economic Daily/Digitimes/The Elec/SCMP/TrendForce/BigGo Finance)*
