# 02 Financial Valuation Analysis – Buffett’s Perspective

**Analyst: Warren Buffett (the father of value investing and a believer in "margin of safety")**
**Target: Qunhe Technology (00068.HK)/Kujiale** | **Date: April 9, 2026**

---

## 1. Revenue and profit trends (2022-2025)

### Revenue growth

| Year | Revenue (100 million RMB) | Year-on-year growth rate | Remarks |
|:----:|:----------:|:------:|------|
| 2022 | 6.01 | — | Impact of the epidemic |
| 2023 | 6.64 | +10.5% | Return to growth |
| 2024 | 7.55 | +13.7% | Overseas acceleration |
| 2025 | 8.20 | +8.6% | Slowing growth |

**Key findings: Revenue growth dropped from 14% to 9%, which is concerning for a SaaS company. **

Revenue in 2025 will be 820 million RMB (approximately 890 million HKD), with a three-year compound growth rate of only approximately 11%. Compared with the usual 20-30% growth rate of global excellent SaaS companies, Kujiale is no longer a high-growth company.

### Overseas business highlights

Overseas revenue will increase by 28% year-on-year in 2025, which is the main driving force for overall growth. The overseas version of Coohom is expanding into Southeast Asia, Latin America and other markets. However, the proportion of overseas revenue is still small and is not enough to reverse the overall slowdown in growth.

---

## 2. Gross profit margin quality analysis

| Year | Gross profit margin | Gross profit (100 million RMB) |
|:----:|:-----:|:----------:|
| 2023 | 76.8% | 5.09 |
| 2024 | 80.9% | 6.11 |
| 2025 | 82.2% | 6.74 |

**82% gross profit margin is an excellent level at the SaaS level**, comparable companies:

| Company | Gross Profit Margin | Type |
|------|:-----:|------|
| Autodesk | ~89% | Global leader in design software |
| Adobe | ~88% | Creative Software |
| Kingsoft Office | ~85% | Domestic SaaS |
| **Kujiale** | **82%** | **Space Design SaaS** |
| Glodon | ~70% | Building informatization |

Gross profit margin continues to increase, indicating that the scale effect is at work - cloud computing costs are diluted as users grow. But it should be noted that the gross profit margin of 82% ≠ makes money, because sales expenses and R&D expenses are extremely high.

> Buffett: "Gross profit margin tells you the quality of the business, and net profit margin tells you the capabilities of the management."

---

## 3. Profitability analysis

### IFRS caliber (actual net profit)

| Year | Net profit (100 million RMB) | Net profit rate |
|:----:|:------------:|:-----:|
| 2023 | -6.46 | -97.4% |
| 2024 | -5.13 | -68.0% |
| 2025 | -4.28 | -52.2% |

**According to IFRS standards, Qunhe Technology will still lose 428 million yuan in 2025! **

### Adjusted caliber (Non-IFRS)

| Year | Adjusted net profit (100 million RMB) |
|:----:|:----------------:|
| 2023 | -2.42 |
| 2024 | -0.70 |
| 2025 | +0.57 |

The main reason for the turnaround in adjusted net profit was the elimination of non-cash items such as share-based payment expenses. The adjusted net profit of RMB 57 million corresponds to revenue of RMB 820 million, and the adjusted net profit rate is only 7% - this shows that the company has just crossed the break-even line and its profit foundation is extremely fragile.

### Cash flow status

- Cash at the end of 2025: 357 million yuan
- Cash flow from operating activities in 2025: -19 million yuan (still negative!)

> Buffett: "Book profits are opinions, cash flow is reality. If a company with negative operating cash flow says it is profitable, I have reservations."

---

## 4. IPO Valuation Analysis

### Basic assumptions

| Parameter | Value | Source |
|------|------|------|
| Offer price range | 6.72 - 7.62 HKD | Prospectus |
| Mid-price | 7.17 HKD | Calculation |
| Pre-IPO valuation (E+ round) | HKD 17.5 billion | Financing in 2021 |
| IPO shares issued | ~161 million shares | Prospectus |
| Total pre-IPO equity (estimated) | ~1.539 billion shares | Media reports |
| Total equity after issuance (estimated) | ~1.70 billion shares | Estimate, including IPO new shares |
| Revenue in 2025 | 820 million RMB ≈ 890 million HKD | Prospectus |
| Adjusted net profit in 2025 | 57 million RMB ≈ 062 million HKD | Prospectus |

### Valuation calculation

Based on the mid-point of the offering price of HKD 7.17, the total share capital after the issuance is approximately 1.7 billion shares:

| Indicator | Value | Description |
|------|------|------|
| **IPO market capitalization** | **~12.2 billion HKD** | 7.17 x 1.7 billion shares (estimated) |
| **PS (price to sales ratio)** | **~13.7x** | 12.2 billion / 890 million |
| **PE (price-to-earnings ratio)** | **~197x** | 12.2 billion / 62 million (adjusted) |
| **IFRS PE** | **Loss, meaningless** | Still losing money according to IFRS standards |
| **Earnings per share (adjusted)** | **~0.036 HKD** | 062 million / 1.7 billion shares |
| **Net assets per share (estimated)** | **~1.0 HKD** | Estimate |
| **PB (price to book ratio)** | **~7.2x** | Estimate |

### Valuation tool verification

Manual verification based on the above parameters:
- IPO price 7.17 HKD / Earnings per share 0.036 HKD = **PE 199x**
- IPO price 7.17 HKD / Net assets per share 1.0 HKD = **PB 7.2x**

**Note: Since the financial_rigor.py tool cannot be run, the above is a manual calculation, and the estimated value may have errors. **

### Valuation comparison of comparable companies

| Company | PS | Revenue growth rate | Gross profit margin | Net profit margin |
|------|:--:|:------:|:-----:|:-----:|
| Autodesk | ~10x | ~12% | ~89% | ~22% |
| Kingsoft Office | ~12x | ~15% | ~85% | ~30% |
| Glodon | ~6x | ~10% | ~70% | ~15% |
| **Qunhe Technology** | **~14x** | **~9%** | **~82%** | **~7%** |

**Qunhe Technology’s PS multiple is higher than that of comparable companies, but its revenue growth rate and net profit margin are the lowest. **

---

## 5. Safety Margin Assessment

> Buffett: "For investors, buying at a price that is too high can offset a decade of favorable business development."

### DCF simple estimation

Assumptions:
- Revenue will grow by 15% annually in the next five years (optimistic assumption, consider overseas acceleration)
- Revenue will reach ~1.65 billion RMB after 5 years
- Steady-state net profit rate of 20% (maturity level for SaaS companies)
- Steady-state net profit ~330 million RMB ≈ 360 million HKD
- Give 25x PE = 9 billion HKD
- Discounted at 10% discount rate for 5 years = ~5.6 billion HKD

**Even under optimistic assumptions, the reasonable valuation is about HKD 5.6-9 billion, which is far lower than the IPO valuation of HKD 12.2 billion. **

### Safety margin judgment

| Scenario | Reasonable valuation (HKD) | Corresponding stock price | vs IPO price |
|------|:----------:|:------:|:---------:|
| Optimistic (15% growth, 20% net profit margin) | 9 billion | 5.3 | IPO price 26% high |
| Neutral (10% growth, 15% net profit margin) | 6 billion | 3.5 | IPO price 51% high |
| Pessimistic (5% growth, 10% net profit margin) | 3.5 billion | 2.1 | IPO price 71% too high |

---

## 6. Buffett’s general comments

| Dimensions | Ratings | Reviews |
|------|:----:|------|
| Revenue quality | ★★★★ | 97% subscription revenue, highly predictable |
| Earnings quality | ★★ | Just turned a loss, operating cash flow is still negative |
| Growth Prospects | ★★★ | 9% growth rate is low, overseas is the bright spot but the volume is small |
| Reasonable valuation | ★★ | PS 14x, PE 200x, serious lack of safety margin |
| Free cash flow | ★★ | Operating cash flow is negative, free cash flow is even worse |

**Buffett’s perspective overall rating: ★★☆ 2.5 / 5**

> "This company has good genes - 82% gross profit margin, pure SaaS model, industry leader status. But a good company does not mean a good investment. 200 times PE to buy a company with a growth rate of 9%? This is not investment, this is speculation. I would rather wait for it to prove that it can continue to make profits and have positive free cash flow, and then buy it at a reasonable price. Remember, we never pay for possibility, only for certainty."

---

Data source: Qunhe Technology Hong Kong stock prospectus (updated version in February 2026), Wind financial terminal, public media reports
Note: The total share capital is an estimate, and the actual data is subject to the prospectus. Currency conversion is based on 1 RMB ≈ 1.085 HKD.
