# Bottleneck Hunter Signal Scan — 2026-06-20 10:00 (Round 247)

## New signal

| Link | Signal description | Source | Is there an investable target | Next step |
|------|---------|------|----------------|-------|
| InP substrate/EML laser (Layer 3/2) | Nvidia will lock in Lumentum+Coherent EML production capacity for $4 billion in March 2026; global monthly demand is 700-800K units vs Monthly supply is only 400K; EML yield is only 15-50% to amplify substrate demand; AXT has raised prices for some customers by nearly 70%; 800G+ optical module shipments are expected to jump 2.6 times in 2025→2026 (24M→63M units) | [TechTimes 2026-05-27](https://www.techtimes.com/articles/317281/20260527/ai-data-center-optical-component-shortage-nvidias-4b-laser-lockup-pushes-rivals-past-2027.htm) · [SDxCentral](https://www.sdxcentral.com/news/nvidias-aggressive-laser-procurement-spurs-supply-chain-fears/) · [TrendForce 2025-12](https://www.trendforce.com/presscenter/news/20251208-12823.html) | ⚠️ AXT (AXTI) The purest InP bid but the valuation is capped (PS 72x, double red light); there is no bidder that has passed the valuation check | Search whether Japanese suppliers (Sumitomo Electric, Mitsubishi Electric) have attainable standards |
| HALEU uranium fuel (Layer 3/SMR supply chain) | Centrus Energy (LEU), the only domestic HALEU producer in the United States; Phase III DOE contract extension ($110 million annual extension, June 2026); DOE commits to a $10 billion 10-year expansion plan; Russia's Tenex has been banned (May 2024); the United States has produced ~1 metric tons but demand in the 2030s is >40 metric tons | [Yahoo Finance - Centrus DOE](https://finance.yahoo.com/news/centrus-energy-secures-110m-haleu-041451652.html) · [ANS Nuclear News](https://www.ans.org/news/2025-06-25/article-7134/doe-extends-centruss-haleu-production-contract-by-one-year/) · [World Nuclear Assoc](https://world-nuclear.org/information-library/nuclear-fuel-cycle/conversion-enrichment-and-fabrication/high-assay-low-enriched-uranium-haleu) | 🆕 Centrus Energy (LEU) recommended to join the watch list ★★; PS ~8.6x (green light) but the HALEU business accounts for less than 5% of the revenue and does not meet the initial purity screening (>30%); it is a strategic option type | Track the SMR project timeline and monitor the improvement nodes of the HALEU business revenue share |

---

## InP substrate/EML laser – detailed analysis

### Bottleneck location

**Layer 3 → Layer 2 link**: InP (Indium Phosphide) substrate → EML laser chip → Optical module transceiver → AI data center interconnection

Bottleneck rating: **S level** (Structural shortage on the supply side, accelerated expansion on the demand side, the two will form the largest gap in 2026)

| Bottleneck Criteria | Score | Description |
|---------|------|------|
| Supply concentration | 🔴 | Major global InP substrate suppliers: AXT, Wafer Technology, Sumitomo (within 3); EML manufacturers <5 (Lumentum, Coherent, Mitsubishi, Sumitomo, Broadcom) |
| Production expansion cycle | 🔴 | InP epitaxial equipment (MOCVD) delivery time is 18-24 months; even if an order is placed today to expand production, new production capacity will not be available until the end of 2027 |
| Difficulty of substitution | 🔴 | The EML technology route cannot be 100% replaced by VCSEL or silicon photonics (silicon photonics requires an external light source and still requires an InP laser) |
| Capacity utilization rate | 🔴 | Monthly demand 700-800K vs monthly supply 400K → Supply gap is about 40-50% |
| Demand growth rate | 🔴 | 800G+ optical module shipments are expected to increase by 160% year-on-year; AI data center interconnection bandwidth demand continues to accelerate |
| Customer verification cycle | 🔴 | Optical module customers (such as Nvidia) verify the laser supplier's verification cycle > 1 year |

**Conclusion: 6/6 standard all red, S-level bottleneck confirmed. **

### Nvidia $4B Lockdown Event (Key Catalyst)

On March 2, 2026, Nvidia invested $2 billion each in Lumentum and Coherent (a total of $4 billion), and also invested in Scintil Photonics and Ayar Labs to lock in priority production capacity access. This move:

1. Directly causing competitors (AMD, Google, Microsoft) to be unable to find EML supply sources and being forced to wait until after 2027.
2. The production capacity of the remaining EML suppliers (MACOM, Sumitomo, Broadcom) was quickly seized by other AI chip manufacturers
3. As a result, the demand for InP substrates has further concentrated, and substrate manufacturers such as AXT have entered a rationing state.

### Related target valuation check

#### AXT Inc (AXTI)—the purest and authentic standard for InP substrates

| Metrics | Data | Sources |
|------|------|------|
| Market Cap | **~$6.4 billion USD** | companiesmarketcap.com, June 2026 |
| TTM Revenue | $88.3M | SEC 10-Q/StockAnalysis |
| PS | **~72x** | $6.4B ÷ $88.3M |
| PE | **Loss (TTM net loss $21.3M)** | SEC 10-Q |
| Q1 2026 Revenue Growth | +39% YoY | semiconductor-today.com |
| InP business proportion | About 60-70% (estimated) | Mainly engaged in InP+GaAs+Ge substrates |
| Expansion plan | Double InP production capacity by the end of 2026 | Company announcement |

**Valuation Red Light Check (required)**:

| Red light conditions | Results |
|---------|------|
| Market value > 20% of TAM? (InP wafer TAM ~$200 million/year, 20% threshold = $40 million) | 🚨 $6.4 billion >> $40 million, **severe trigger** (triggered even with larger caliber TAM) |
| PS > 30x and growth rate < 100%? | 🚨 PS=72x, growth rate 39% (much lower than the 100% immunity line), **trigger** |
| Market value > 10 times optimistic forecast in 5 years? (Optimistic annual revenue doubles to $200M × 5 years = $1 billion, × 10 = $10 billion) | ⚠️ $6.4 billion < $10 billion, boundary (relying on extremely optimistic assumptions) |

**Double red light trigger. The signal strength is capped at ★★, marked "⚠️ Valuation is seriously overdrawn". **

10-year 25xPE exit method: Buy with a market value of $6.4 billion. If the net profit reaches $100M after 10 years (from loss to profit, and then to $100M requires a huge assumption), 25xPE exit = $2.5 billion, 75% lower than the purchase market value, **no safety margin**. Even in an extremely optimistic scenario (net profit of $300M, corresponding revenue of $1.2B), 25xPE=$7.5 billion, the annualized rate in 10 years is only 1.6%. **There is absolutely no margin of safety at current prices. **

**Conclusion: The InP/EML bottleneck is a real S-level bottleneck, but AXT has been fully or even severely overpriced. Top rating ★★ (valuation red light). **

---

## HALEU Uranium Fuel Signal — Strategic Options Signal

### Background

Most SMR (Small Modular Reactor) designs require HALEU (High Abundance Low Enriched Uranium, 5-20% enrichment), while conventional nuclear power plants use 3-5% LEU. USA:
- Russian Tenex (previously the only commercial supplier) has been banned (May 2024)
- Centrus Energy (LEU) is the only U.S. company currently operating a HALEU production facility
- About 920 kilograms have been produced; annual demand after SMR commercialization in the 2030s may be >40 metric tons → huge supply gap

### Centrus Energy (LEU) Valuation Check

| Metrics | Data | Sources |
|------|------|------|
| Market Cap | **~$4.07 billion** | companiesmarketcap.com, May 2026 |
| 2026 Revenue Guidance | $450-500M | Company Guidance |
| PS | **~8.6x** | $4.07B ÷ $475M (median estimate) |
| PE | ~62x (estimate, 2025 data) | Yellow light, needs to be confirmed by the latest data in 2026 |
| HALEU business accounts for revenue | **<5% (estimate)** | HALEU contract $110 million/year vs total revenue $475M |
| Passed the preliminary screening of "bottleneck business >30% revenue" | ❌ **Failed**, main business is LEU nuclear fuel supply |

**Estimation light: PS ~8.6x green light, but failed the initial screening (bottleneck purity is insufficient). **

**Conclusion: Centrus is a strategic option for HALEU, but it is not the pure target of the current bottleneck. The commercialization of SMR will still take 3-5 years, and then the proportion of HALEU business may exceed the 30% threshold. Join the watch list ★★, tracking conditions: Re-evaluate when the proportion of HALEU business in revenue reaches 20%+. **

---

## Watch list status changes

| Subject | Code | Change | Reason |
|------|------|------|------|
| Centrus Energy | LEU | 🆕 **New ★★(Strategic Option)** | The only HALEU producer in the United States, DOE Phase III contract extension, SMR supply chain front-end layout |
| AXT Inc | AXTI | 🆕 **★★(Valuation red light)** | InP substrate S-level bottleneck confirmed, but PS 72x double red light is capped and cannot be bought; monitoring valuation pulls back to PS<10x |
| HEX.L | HEX.L | **No change** | The round has been upgraded to ★★★★ at 14:00, no new signals |
| All other underlyings | — | No change | — |

---

## Next research direction

1. **InP/EML Japanese alternative targets**: EML business proportion and valuation check of Sumitomo Electric (5802.T) and Mitsubishi Electric (6503.T) - if the EML business accounts for more than 30% and the valuation is reasonable, it may be a better investment entry point
2. **AXT valuation callback monitoring**: Trigger price: PS<15x (about $20/share), PS<10x (about $13/share); the current $88.59 does not have a safety margin
3. **HALEU contract size tracking**: The specific allocation of the next large DOE contract ($2.7 billion for 10 years), and whether there are more pure HALEU bids (such as Urenco and Orano building factories in the United States)

---

*Source: [TechTimes EML Shortage](https://www.techtimes.com/articles/317281/20260527/ai-data-center-optical-component-shortage-nvidias-4b-laser-lockup-pushes-rivals-past-2027.htm) · [SDxCentral Nvidia Laser](https://www.sdxcentral.com/news/nvidias-aggressive-laser-procurement-spurs-supply-chain-fears/) · [TrendForce Dec 2025](https://www.trendforce.com/presscenter/news/20251208-12823.html) · [StockAnalysis AXTI Market Cap](https://stockanalysis.com/stocks/axti/market-cap/) · [SEC AXTI 10-Q 2026](https://www.sec.gov/Archives/edgar/data/0001051627/000143774926017054/axti20260331_10q.htm) · [Yahoo Finance Centrus DOE](https://finance.yahoo.com/news/centrus-energy-secures-110m-haleu-041451652.html) · [ANS Nuclear Centrus](https://www.ans.org/news/2025-06-25/article-7134/doe-extends-centruss-haleu-production-contract-by-one-year/) · [InP Bottleneck Substack](https://yianisz.substack.com/p/indium-phosphide-inp-the-quiet-bottleneck)*
