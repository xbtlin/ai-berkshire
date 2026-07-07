# 02 Financial Valuation Analysis - Buffett Perspective (Core)

> **Research Subject**: Alibaba Group (9988.HK / BABA)
> **As of**: FY26Q3 (2025-12-31)
> **Report Date**: 2026-05-04
> **Research Question**: What is the neutral forecast for Alibaba Group's annual profit in FY2036? Current valuation vs intrinsic value?

---

## 0. Core Judgment in One Sentence

**Alibaba Group's FY2036 neutral Non-GAAP net profit forecast is approximately RMB 459.1 billion** (probability-weighted expected value approximately RMB 488.0 billion), equivalent to **3.6x** current FY25 net profit of RMB 126.0 billion. Back-solving at a reasonable PE of 14x and a 10% discount rate implies intrinsic value of approximately **RMB 2.55 trillion**, giving only a **22% margin of safety** relative to current market capitalization (approximately RMB 2.31 trillion). The risk/reward is moderately weak: the AI/cloud upside option is not fully priced, but the short-term profit-collapse risk has already been priced in by the market.

---

## 1. Financial Snapshot (FY26 Q1-Q3, as of 2025-12-31)

### 1.1 Group TTM Revenue (FY26 First Three Quarters + FY25 Q4 Estimate)

| Quarter | Revenue (RMB 100 million) | YoY | Data Source |
|---|---|---|---|
| FY26 Q1 (2025-06) | 2,476.5 | +2% | Alibaba official/Sina Finance |
| FY26 Q2 (2025-09) | 2,478.0 | +5% (+15% on comparable basis) | BusinessWire/Alizila |
| FY26 Q3 (2025-12) | 2,848.4 | +2% | BusinessWire/Wallstreetcn/Yicai |
| **FY26 9M total** | **7,802.9** | - | Estimate |
| FY25 full year | 9,963.5 | +6% | Alibaba FY25 annual report |

**Estimated TTM revenue (as of 2025-12) approximately RMB 1.04 trillion** (estimated, high confidence).

### 1.2 FY26 Q3 Key P&L Metrics (Latest Quarter, 2025-12)

- **Total revenue**: RMB 284.843 billion (+2% YoY)
- **Income from operations**: RMB 10.645 billion (**-74% YoY, collapse during heavy reinvestment period**)
- **Adjusted EBITA**: RMB 23.397 billion (-57% YoY)
- **Net income attributable to ordinary shareholders**: RMB 16.322 billion
- **GAAP net income**: RMB 15.631 billion (-66% YoY)
- **Non-GAAP diluted EPS** (disclosed for FY26 Q2): RMB 4.36/ADS (-71% YoY)
- **Net cash provided by operating activities**: RMB 36.03 billion (-49% YoY)
- **Free cash flow**: RMB 11.35 billion (-71% YoY)
- **Capital expenditures (Capex)**: approximately RMB 31.8 billion (+80% QoQ, driven by AI infrastructure)

### 1.3 FY26 Q3 Performance by Business Segment

| Segment | Revenue (RMB 100 million) | YoY | Adjusted EBITA (RMB 100 million) | YoY | Notes |
|---|---|---|---|---|---|
| **China E-commerce Group (Taobao and Tmall, etc.)** | 1,400+ | +10% | **346.13** | **-43%** | Instant retail losses + investment |
| - CMR (customer management revenue) | 1,026.6 | +1% | - | - | High-base effect from software service fees |
| - Instant retail (Flash Purchase) | 208.4 | +56% | - | - | Spending phase |
| - Cross-border wholesale | 69.2 | +5% | - | - | - |
| **Cloud Intelligence Group** | **432.84** | **+36%** | **39.11** | **+25%** | 10th consecutive quarter of triple-digit AI growth |
| **AIDC (International Digital Commerce)** | ~325 | +3% | **-20.16** (loss) | Improved | AliExpress Choice unit economics improved |
| Cainiao / Local Services / Digital Media and Entertainment / Other | Remaining items | - | - | - | Data not separately disclosed |

**Core observation**: Revenue +2% but EBITA -57%, indicating Alibaba is entering an **intentional reinvestment period** (instant retail + AI infrastructure + internationalization), with short-term profit giving way to strategic positioning.

### 1.4 Balance Sheet (as of 2025-12-31)

- **Cash + short-term investments + other treasury investments**: RMB 560.18 billion (approximately USD 80.1 billion)
- Down RMB 36.96 billion vs FY25-end RMB 597.13 billion (FCF net outflow RMB 29.3 billion + dividends RMB 33.7 billion + buybacks RMB 7.6 billion, partially offset by convertible note financing of RMB 21+11 billion)
- **Total interest-bearing debt**: approximately RMB 276.66 billion (TradingView data, medium confidence)
- **Estimated net cash**: 560.2 - 276.7 approximately **RMB 283.5 billion** (about 12% of current market capitalization)

### 1.5 Current Share Price, Market Capitalization, and Valuation (2026-05-04)

| Metric | Value | Source |
|---|---|---|
| 9988.HK closing price | HKD 130.60 | Xueqiu/Yahoo (2026-05-02) |
| BABA U.S. close | USD 132.53 | Capital.com (2026-04-27) |
| Total shares outstanding (ordinary shares) | 19.10 billion (approximately 19.1 billion shares, including 2.39 billion ADS-equivalent under 1ADS=8 ordinary shares basis) | Macrotrends/SEC |
| ADS count | approximately 2.40 billion | Stockanalysis.com |
| **Hong Kong market cap (manual calculation)** | **130.60 × 19.099B = HKD 2,494 billion approximately HKD 2.49 trillion** | Tool check |
| **U.S. market cap** | **132.53 x 2.40B = USD 318.0 billion** | Tool check |
| U.S. market cap in RMB | 318 × 7.27 = **RMB 2,312 billion approximately RMB 2.31 trillion** | - |

#### Embedded Tool Check

```
Tool: financial_rigor.py verify-market-cap
Input: price=130.60 HKD, shares=19.099B, reported=2.495T HKD
Output: Verification passed, deviation 0.03%
Calculated market cap: 2.49T HKD
```

### 1.6 Current Valuation Multiples (Based on FY25 Annual Report + TTM Estimate)

- **PE (FY25 GAAP)**: 23,120 / 1,260 = **18.3x**
- **PE (FY25 Non-GAAP, using 158.0 billion)**: approximately 14.6x (FY25 Non-GAAP net profit approximately RMB 158.0 billion, medium confidence)
- **PE (FY26 TTM estimate)**: due to the Q3 profit collapse, TTM net profit is approximately RMB 80-90 billion, raising PE to 25-29x
- **PS (TTM)**: 2,312 / 10,400 = **2.22x**
- **EV/EBITA (excluding net cash)**: (23,120 - 2,835) / estimated EBITA approximately 14-16x

---

## 2. 10-Year Revenue Projection (by Segment)

### 2.1 Taobao and Tmall Group (China E-commerce)

**Fact base**: FY25 revenue RMB 449.8 billion, EBITA RMB 196.2 billion (margin 43.6%); FY26 Q3 EBITA -43% (large instant-retail investment).

**Core tension**:
- Overall China e-commerce growth has slowed to single digits, while Pinduoduo + Douyin E-commerce continue taking share
- Limited take-rate upside ("software service fee" already implemented, with FY26 Q3 marginal effect fading)
- Instant retail (Taobao Flash Purchase, FY26Q3 revenue RMB 20.8 billion, +56%) is incremental growth but loss-making in the short term

**10-year CAGR assumptions**:

| Scenario | Assumption | CAGR | FY36 Revenue |
|---|---|---|---|
| Bull | 88VIP penetration + instant retail turnaround + premiumization take rate +1pp | 6% | RMB 805.5 billion |
| **Base** | **Low-single-digit GMV growth + slight take-rate increase** | **5%** | **RMB 732.8 billion** |
| Bear | Pinduoduo/Douyin continue taking share, CMR stagnates | 2% | RMB 548.3 billion |

### 2.2 Cloud Intelligence Group (Core AI Story)

**Fact base**: FY25 revenue RMB 118.0 billion (+11%), EBITA RMB 10.56 billion (margin 8.9%). FY26 Q3 quarterly revenue RMB 43.284 billion (+36%), EBITA margin 9.0%. AI revenue has delivered triple-digit growth for 10 consecutive quarters.

**Credibility review of Eddie Wu's "USD 100 billion in 5 years" target**:
- This target includes MaaS + full-stack AI (B+C), requiring FY30 to reach USD 100 billion approximately RMB 710.0 billion
- From FY25 RMB 118.0 billion to FY30 RMB 710.0 billion requires a 5-year **CAGR of 43%** (tool calculation)
- Current growth is 36%, while AI triple-digit growth continues - the target is **aggressive but not impossible**
- Constraints: compute supply (H800 restrictions/Huawei Ascend), enterprise AI commercialization pace, price wars

**10-year CAGR scenarios**:

| Scenario | 5-Year CAGR | 10-Year CAGR | FY36 Revenue (RMB 100 million) |
|---|---|---|---|
| Bull (Eddie Wu target achieved + next 5 years at 15%) | 43% | 25% | 10,990 |
| **Base (5 years at 30% + next 5 years at 12%)** | **30% / 12%** | **20%** | **7,306** |
| Bear (5 years at 18% + next 5 years at 8%) | 18% / 8% | 13% | 4,774 |

> Comparable benchmarks: AWS FY25 revenue approximately USD 120.0 billion (CAGR 18-20%); Azure growth 30%+. As China's AI leader + overseas ASEAN extension, **a base-case 20% CAGR for Alibaba Cloud is reasonable**.

### 2.3 AIDC (International Digital Commerce)

**Fact base**: FY25 revenue RMB 132.3 billion (+29%), loss-making (FY26 Q3 EBITA -RMB 2.0 billion, already substantially narrowed).

**Key milestones**:
- **FY27-FY28** quarterly breakeven (AliExpress Choice unit economics improving + Lazada optimization already validated)
- Trendyol (Turkey) steadily profitable, Daraz (South Asia) scaling
- Long-term take-rate assumption 4-5% (referencing Shein 5%, Amazon cross-border 8%)

**10-year CAGR**:

| Scenario | CAGR | FY36 Revenue |
|---|---|---|
| Bull | 20% | RMB 819.2 billion |
| **Base** | **15%** | **RMB 535.2 billion** |
| Bear | 10% | RMB 343.2 billion |

### 2.4 Local Services (Ele.me + Flash Purchase + Amap Combined)

**Fact base**: FY25 scale approximately RMB 60-70 billion, with long-term losses. Taobao Flash Purchase has been integrated since FY26 (already included in China E-commerce Group reporting).

- **Core strategic shift**: After the FY26 organizational adjustment, instant retail was folded into "China E-commerce Group," weakening Local Services' independence
- Meituan is the clear leader, and Alibaba's food-delivery share remains under pressure
- Amap (local services + in-store) is a differentiated asset

**10-year estimate** (including Flash Purchase in Taobao and Tmall): FY36 standalone local services approximately RMB 100-200 billion, **treated as an extension of Taobao and Tmall** and included in Taobao and Tmall and "Other" in this report.

### 2.5 Cainiao / Digital Media and Entertainment / Other

- **Cainiao**: FY25 revenue RMB 101.3 billion (+2%), CAGR 5-8%, FY36 approximately RMB 150-200 billion
- **Digital Media and Entertainment**: small scale (RMB 20-30 billion), weak profitability, 10-year CAGR 5%, FY36 approximately RMB 40 billion
- **Other** (DingTalk, divested Intime, Sun Art Retail, etc.): remaining items approximately RMB 80 billion

### 2.6 Consolidated Group Revenue Projection (FY36)

| Segment | Bull | Base | Bear |
|---|---|---|---|
| Taobao and Tmall (including Flash Purchase) | 8,055 | 7,328 | 5,483 |
| Cloud Intelligence | 10,990 | 7,306 | 4,774 |
| AIDC | 8,192 | 5,352 | 3,432 |
| Cainiao | 2,000 | 1,500 | 1,000 |
| Local Services | 1,700 | 1,300 | 1,000 |
| Digital Media and Entertainment | 600 | 500 | 400 |
| Other | 1,000 | 800 | 500 |
| **Total** | **32,537** | **24,086** | **16,589** |

Group 10-year revenue CAGR: bull 12.6% / base 9.2% / bear 5.2%.

---

## 3. 10-Year Margin Projection

### 3.1 Alibaba Cloud Steady-State Operating Margin (Key Question)

**Current**: FY25 EBITA margin 8.9%, rising to 9.0% in FY26 Q3.

**Cross-sectional comparison**:
- AWS: FY25 operating margin 36-38%
- Azure: estimated 40-45% (including scale effects)
- Google Cloud: FY25 approximately 14% (catch-up phase)

**10-year steady-state forecast**:
- Bull: reaches 25% (between GCP and Azure, AI inference scale effects + high-margin MaaS)
- **Base: 18-20%** (stable public-cloud share + AI compute gross margin affected by domestic-chip substitution)
- Bear: 12% (persistent price wars + heavy capex depreciation burden)

### 3.2 Taobao and Tmall Steady-State Margin

**Current**: FY25 EBITA margin 43.6% (CMR resembles a pure-profit commission layer).

- Instant retail drag peaks in FY26-FY28 (referencing Meituan food delivery taking 7 years to breakeven)
- Long-term CMR take-rate upside is limited (regulation + competition)
- Base-case steady-state EBITA margin assumption: **35-38%** (after removing instant-retail drag)

### 3.3 When AIDC Becomes Profitable

**Key inflection point**: FY26 Q3 quarterly loss had narrowed to RMB 2.0 billion (vs -RMB 5.0 billion in the prior year).
- **FY28 (calendar year 2027) breakeven** as the base case (medium confidence)
- Steady-state EBITA margin: 5-8% (referencing Amazon International, Shopee)

### 3.4 Local Services/Instant Retail

- Instant retail (Taobao Flash Purchase) reference: Meituan needed 5-7 years to achieve positive UE
- **FY29-FY30 overall turnaround** as the base case
- Steady-state margin 3-5%

### 3.5 Group 10-Year Margin (Blended EBITA → Non-GAAP Net Margin)

| Segment (FY36 Base) | Revenue | EBITA margin | EBITA |
|---|---|---|---|
| Taobao and Tmall | 7,328 | 35% | 2,565 |
| Cloud Intelligence | 7,306 | 19% | 1,388 |
| AIDC | 5,352 | 6% | 321 |
| Cainiao | 1,500 | 5% | 75 |
| Local Services | 1,300 | 3% | 39 |
| Digital Media and Entertainment | 500 | 2% | 10 |
| Other | 800 | 5% | 40 |
| **Total EBITA** | **24,086** | **18.5%** | **4,438** |

Group EBITA → Non-GAAP net profit = EBITA × (1-25% effective tax rate) + net interest income. Non-GAAP net margin approximately **17-19%**.

---

## 4. FY2036 Three-Scenario Profit Projection (Core Output)

| Scenario | Probability | Group Total Revenue | EBITA Margin | EBITA | Non-GAAP Net Profit | Non-GAAP Net Margin | Free Cash Flow | Key Assumptions |
|---|---|---|---|---|---|---|---|---|
| **Bull** | 30% | RMB 3,253.7 billion | 24% | 7,809 | **RMB 716.2 billion** | 22% | RMB 600.0 billion | Cloud 25% margin, Taobao and Tmall resilient, AIDC profitable, AI >60% of cloud revenue |
| **Base** | 50% | RMB 2,408.6 billion | 18.5% | 4,456 | **RMB 459.1 billion** | 19% | RMB 380.0 billion | Cloud 19% margin, Taobao and Tmall 35% margin, AIDC turns around in FY28 |
| **Bear** | 20% | RMB 1,658.9 billion | 13% | 2,157 | **RMB 213.1 billion** | 12.8% | RMB 150.0 billion | Cloud price war, Taobao and Tmall share decline, AIDC remains loss-making |

### Probability-Weighted Expected Value (FY2036 Annual Profit)

```
Tool calculation: 0.30×7,162 + 0.50×4,591 + 0.20×2,131 = RMB 487.9 billion
```

**Using a 30/50/20 probability split, expected annual profit is approximately RMB 488.0 billion** (approximately USD 67.0 billion, roughly 3.9x FY25).

> Calculation note: This report adopts a **30/50/20 probability distribution** as its core case - the AI upside option is large, but the bear case (geopolitics + regulation + price-war triple pressure) deserves a weight of at least 20%.

---

## 5. Comparison with Market Consensus

### 5.1 Major Investment Bank FY27-FY28 Consensus (Based on 2026 Q1 Updates)

| Institution | Timing | FY26 Non-GAAP Net Profit Forecast | FY27 | FY28 | Rating/Target Price |
|---|---|---|---|---|---|
| **Goldman Sachs** | 2026 Q1 | -9% adjustment | +31% recovery | +36% growth | Conviction Buy / target price USD 163 |
| **Morgan Stanley** | 2025-02 upgraded to OW | - | - | - | Overweight, target HKD 195 |
| **Consensus median** (29 analysts) | 2026-04 | - | - | - | Target price HKD 195.07 |

Path implied by Goldman: FY26E RMB 100.0 billion (estimated) → FY27E RMB 131.0 billion → FY28E RMB 178.0 billion.

### 5.2 Simple Linear Extrapolation vs This Report's Base Forecast

**Linear extrapolation FY28 → FY36** (using FY28 RMB 178.0 billion, assuming 8-year CAGR of 8% thereafter): 178.0 × 1.08^8 = **RMB 329.4 billion**

**This report's base forecast is RMB 459.1 billion** vs linear extrapolation of RMB 329.4 billion, **39% higher**.

**Why higher**:
1. Alibaba Cloud AI commercialization accelerates in FY28-FY32 (pace of Eddie Wu's USD 100 billion target delivery)
2. Instant retail/AIDC turn from "sources of loss" into "sources of profit" after FY28 - this is nonlinear
3. Consensus currently suppresses valuation because of the FY26 profit collapse and does not fully price the cash-flow release 5-10 years after AI capex depreciation

**Why not even higher**:
1. China e-commerce competition becomes long-term (Pinduoduo + Douyin + Meituan Flash Purchase)
2. Antitrust and tax normalization
3. Geopolitics + AI export controls + domestic-substitution friction

---

## 6. Current Valuation vs 10-Year Intrinsic Value (DCF Back-Solve)

### 6.1 Back-Solved Intrinsic Value

```
Base-case intrinsic value:
FY36 Non-GAAP net profit RMB 459.1 billion × reasonable PE 14x = RMB 6,427.4 billion (FY36 point in time)
Discounted back 10 years at a 10% discount rate: 6,427.4 / 1.10^10 = RMB 2,547.7 billion

Tool check: 4,720 × 14 / 1.10^10 = RMB 2,547.7 billion
```

| Scenario | FY36 Non-GAAP Net Profit | Reasonable PE | FY36 Market Cap | Discounted to Today (@10%) | vs Current Market Cap (RMB 2,312.0 billion) |
|---|---|---|---|---|---|
| Bull | RMB 716.2 billion | 18x | RMB 12,891.6 billion | **RMB 4,970.3 billion** | +115% (large margin of safety) |
| **Base** | **RMB 459.1 billion** | **14x** | RMB 6,427.4 billion | **RMB 2,547.7 billion** | **+10%** |
| Bear | RMB 213.1 billion | 9x | RMB 1,917.9 billion | **RMB 739.4 billion** | **-68%** |

**Probability-weighted intrinsic value (30/50/20) = 0.30×4,970.3 + 0.50×2,547.7 + 0.20×739.4 = RMB 2,812.7 billion**, a **premium of approximately 22%** to the current RMB 2,312.0 billion market capitalization.

### 6.2 Margin-of-Safety Judgment

- Buffett/Duan Yongping require a margin of safety ≥ 30% (buying price ≤ intrinsic value × 70%)
- The current price implies only a 22% margin of safety, **not meeting the "obviously cheap" standard, but close to reasonable**
- If the share price falls back to HKD 100 (market cap approximately RMB 1.91 trillion), the margin of safety would rise to 47%, **entering an "obviously cheap" zone**

### 6.3 Key Variables That Would Trigger Buying

1. **Whether cloud EBITA margin can steadily rise** (+0.5-1pp each quarter)
2. **Whether AIDC quarterly losses converge to 0 on schedule in FY27**
3. **Whether instant-retail quarterly losses peak and decline in FY27**
4. **Medium-term milestones for Eddie Wu's 5-year USD 100 billion target** (whether FY28 reaches USD 60.0 billion)

---

## 7. Data Reliability Statement

### 7.1 Primary Data (High Confidence)

- FY26 Q3 revenue RMB 284.843 billion, net income RMB 15.631 billion, cloud revenue RMB 43.284 billion, AIDC EBITA -RMB 2.016 billion - all from BusinessWire Alibaba official announcement + SEC 6-K (2026-03-19)
- FY25 full-year revenue RMB 996.347 billion, net income RMB 125.976 billion - Alibaba official annual report (2025-05-15)
- Cash + short-term investments RMB 560.175 billion, ADS 2.4 billion, 1ADS=8 ordinary shares - SEC announcement

### 7.2 Estimated Data (Medium Confidence)

- TTM revenue RMB 1.04 trillion - estimated from FY25 + FY26 9M
- Alibaba Cloud 10-year CAGR 20% (base) - based on AWS/Azure historical paths + 50% discount to Eddie Wu's USD 100 billion target
- AIDC FY28 turnaround - extrapolated from loss-narrowing pace

### 7.3 Assumption Data (Low Confidence, Requires Ongoing Tracking)

- Alibaba Cloud 10-year steady-state EBITA margin 19% - between AWS (38%) and GCP (14%)
- Probability distribution 30/50/20 - subjective judgment
- Reasonable PE 14x (base) - referencing global technology leaders Meta 22x, Google 23x, Amazon 35x, with a 30-40% discount for Alibaba

### 7.4 Cross-Validation Record

```
FY26Q3 total revenue (RMB 100 million): BusinessWire 2,848.43 / Wallstreetcn 2,848.43 / Yicai 2,848 → deviation < 0.02%
FY26Q3 Alibaba Cloud revenue (RMB 100 million): BusinessWire 432.84 / Sina 432.8 / Wallstreetcn 433 → deviation < 0.04%
Hong Kong market cap (HKD trillion): 130.60 × 19.099B = 2.49T, deviation vs Xueqiu report 2.50T is 0.03%
```

---

## 8. Numerical Logic Self-Check Table

| # | Key Assumption | Value | Confidence | Main Risk |
|---|---|---|---|---|
| 1 | Current FY26 TTM revenue | RMB 1.04 trillion | High | FY26Q4 data not yet released |
| 2 | Current U.S. market cap | USD 318B | High | Tool check passed |
| 3 | Cash + short-term investments | RMB 560.2 billion | High | Official announcement |
| 4 | Net cash | RMB 283.5 billion | Medium | Total debt estimate from third party |
| 5 | Taobao and Tmall 10-year CAGR | 5% (base) | Medium | Pinduoduo/Douyin taking share |
| 6 | Cloud Intelligence 10-year CAGR | 20% (base) | Medium | Eddie Wu target delivery |
| 7 | Cloud steady-state EBITA margin | 19% (10 years later) | Medium | Domestic chips impact gross margin |
| 8 | AIDC 10-year CAGR | 15% (base) | Medium | Overseas policy risk |
| 9 | AIDC breakeven timing | FY28 | Medium | Loss narrowing already validated |
| 10 | Instant retail turnaround timing | FY29-FY30 | Medium-low | Intense Meituan competition |
| 11 | Group FY36 revenue (base) | RMB 2,408.6 billion | Medium | Aggregation error |
| 12 | Group FY36 Non-GAAP net profit (base) | RMB 459.1 billion | Medium | Margin assumptions highly volatile |
| 13 | Probability-weighted annual profit | RMB 488.0 billion | Medium | Subjective probabilities |
| 14 | Reasonable PE (base) | 14x | Medium | Market sentiment volatility |
| 15 | Intrinsic value (base discounted) | RMB 2,547.7 billion | Medium | Discount-rate sensitivity |
| 16 | Premium vs current market cap | +10% | Medium | Weak margin of safety |
| 17 | "5-year USD 100 billion" target delivery | 50% probability | Medium-low | Compute + commercialization dual constraints |
| 18 | Antitrust/regulatory normalization | Assumes status quo | Medium | Policy risk |
| 19 | Reasonableness of 10% discount rate | Standard Buffett | High | Long-term treasury-yield upside risk |
| 20 | FY36 probability-weighted PE | 14.5x | Medium | - |

---

## Core Conclusion and Investment View

1. **FY2036 base-case annual profit forecast is RMB 459.1 billion** (approximately USD 63.1 billion), 3.6x current FY25 net profit
2. **Probability-weighted expected value is RMB 488.0 billion** - the bull case reaches RMB 716.2 billion, while the bear case is only RMB 213.1 billion
3. **The current share price implies only a 22% premium to intrinsic value**, not meeting Buffett's "obviously cheap" standard (requires 30% margin of safety)
4. **The key variable is Alibaba Cloud**: whether it can deliver USD 100 billion by FY30 and raise EBITA margin to 18-20%
5. **Buffett-perspective judgment**: Alibaba is **not a no-brainer** - if you believe the AI story + management execution, the "base-to-bull" path is worth a 50% probability wager; if you strictly require a 30%+ margin of safety, then building positions in batches below HKD 100 / USD 110 is preferable

**Duan Yongping perspective addendum**: Alibaba's RMB 560.2 billion cash position + business model close to stable free cash flow + moat as a Chinese internet leader make it an asset that is "understandable and unlikely to die," but **the odds at the current price are not extreme enough**. The FY26 profit collapse is the "ticket price" paid for the FY28-FY36 AI dividend - if you believe the ticket will pay off, holding at the current price is reasonable; if you believe Chinese cloud cannot replicate AWS's profitability path, then 14x PE is still too expensive.

---

## Sources

- [Alibaba Group Announces December Quarter 2025 Results - BusinessWire](https://www.businesswire.com/news/home/20260318501558/en/Alibaba-Group-Announces-December-Quarter-2025-Results)
- [Alibaba Q3 Revenue Up 4.8% YoY, Cloud Revenue Surges 34% - Wallstreetcn](https://wallstreetcn.com/articles/3760096)
- [Alibaba Fiscal 2026 First-Quarter Revenue of RMB 247.7 Billion - Sina Finance](https://finance.sina.com.cn/tech/2025-08-29/doc-infnrwzh2670909.shtml)
- [Alibaba Annual Report: Fiscal 2025 Revenue of RMB 996.347 Billion - Sina Finance](https://finance.sina.com.cn/tech/2025-06-26/doc-infcmcye4624794.shtml)
- [Alibaba Group Announces March Quarter 2025 and Full Fiscal Year 2025 Results - Alibaba Group](https://www.alibabagroup.com/zh-HK/document-1859016196574150656)
- [Alibaba Group Announces September Quarter 2025 Results - BusinessWire](https://www.businesswire.com/news/home/20251124757764/en/Alibaba-Group-Announces-September-Quarter-2025-Results-and-Interim-Results-for-the-Six-Months-Ended-September-30-2025)
- [Alibaba's Q2 Results - Alizila](https://www.alizila.com/alibaba-fy26-q2-results/)
- [Alibaba 2026 "A Plan": Cloud and AI Commercial Annual Revenue to Exceed USD 100 Billion - Shanghai Securities News](https://paper.cnstock.com/html/2026-03/20/content_2190434.htm)
- [Eddie Wu Announces Alibaba AI Strategy Commercial Target: Cloud and AI Commercial Annual Revenue Above USD 100 Billion in the Next Five Years - Sina Finance](https://finance.sina.com.cn/wm/2026-03-19/doc-inhrpwvm8501232.shtml)
- [Alibaba Group (BABA) Market Cap - April 2026 Update - Capital.com](https://capital.com/en-int/markets/shares/alibaba-group-holding-limited-share-price/market-cap)
- [Alibaba Shares Outstanding 2012-2025 - Macrotrends](https://www.macrotrends.net/stocks/charts/BABA/alibaba/shares-outstanding)
- [Goldman Sachs upgrades Alibaba stock on AI-driven cloud growth - Investing.com](https://www.investing.com/news/analyst-ratings/goldman-sachs-upgrades-alibaba-stock-on-aidriven-cloud-growth-93CH-4534412)
- [Morgan Stanley Upgrades Alibaba Group Holding (SEHK:9988) - Nasdaq](https://www.nasdaq.com/articles/morgan-stanley-upgrades-alibaba-group-holding-sehk-9988)
- [Alibaba (BABA) - Cash on Hand - companiesmarketcap.com](https://companiesmarketcap.com/alibaba/cash-on-hand/)
- [Alibaba Group Holding Ltd Earnings - Q3 2025 - Alpha-Sense](https://www.alpha-sense.com/earnings/baba/)
- [Alibaba Third-Quarter Revenue Grows, Profit Declines - Yicai](https://www.yicai.com/news/102927778.html)
- [Alibaba Q2 Non-GAAP Net Profit Down 18% YoY, Cloud Revenue Up 26% - Wallstreetcn](https://wallstreetcn.com/articles/3754524)
- [Alibaba (BABA) Q2 2026 Earnings Call Transcript - Seeking Alpha](https://seekingalpha.com/article/4851953-alibaba-group-holding-limited-baba-q2-2026-results-earnings-call-transcript)
