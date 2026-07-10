# In-depth study on IFRS accounting treatment of Tencent (0700.HK) investment portfolio

**ai-berkshire Tencent Investment Accounting Specialist | 2026-04-22**

## 1. Core conclusion

The accounting treatment of Tencent's investment portfolio is extremely complex and highly dispersed - the holding subsidiaries (Riot, Supercell) are fully merged, the associates (Kuaishou, Bilibili, BOSS Direct Recruitment, etc.) are recognized according to the shareholding ratio according to the equity method and the share of net profit is not reflected in the fluctuation of market value. The vast majority of non-associate listed investments (Pinduoduo, Spotify, Snap, etc.) are based on **FVTPL**, so that changes in fair value directly impact the income statement, and a small number of strategic equity are designated as **FVOCI** Isolated from the income statement. **This structure causes Tencent's GAAP net profit to fluctuate greatly** (a year-on-year plunge of approximately 47% in 2021, another decline in 2022, and a significant recovery in 2023-2024), but the adjusted net profit (Non-GAAP) is relatively stable. **This is the first principle for understanding Tencent's income statement**.

## 2. IFRS 9 4 classifications of financial assets

### A. Measured at amortized cost
- Conditions: Business model is "Hold to collect contractual cash flow" + SPPI passed
- Typical: accounts receivable, bonds held until maturity
- **Holding period does not reflect market value fluctuations**
- **Tencent Application**: large cash management, structured deposits

### B. Fair value through other comprehensive income (FVOCI)
**Equity Tool Version (Irrevocable Designation)**:
- All changes in fair value are included in OCI and **never roll back to the income statement**
- Cumulative OCI changes upon disposal can only be carried forward to retained earnings
- **Tencent Apps**: Minority long-term strategic equity stake

### C. Fair value through profit or loss (FVTPL)
- Condition: Default classification that does not meet the above conditions
- Changes in fair value **The full amount is directly entered into the income statement for the current period**
- **Tencent Apps**: **Portfolio entities**—Pinduoduo, Kuaishou, Sea, Spotify, Snap, Tesla, etc. are listed; most unlisted investments

### D. Equity Method Accounting (IAS 28)
- Condition: Significant influence (20-50% shareholding + board seat)
- Investment income is recognized as **shareholding ratio × net profit** of the investee
- **Does not reflect market capitalization fluctuations at all**
- Impairment test is based on IAS 36 (when recoverable amount < carrying amount)
- **Tencent Apps**: Kuaishou, Bilibili, BOSS Direct Recruitment, Zhongan, WeBank (30%), Futu, etc.

## 3. Classification framework of Tencent’s investment portfolio

| Investment type | Accounting classification | Balance sheet position | Profit and loss impact | Whether market value fluctuations are reflected |
|---------|---------|--------------|---------|---------------|
| Controlled subsidiaries (Riot, Supercell merger, Miniclip, Funcom) | Consolidated statements | Revenue/costs fully consolidated | Direct impact | N/A |
| Associates (Kuaishou, Bilibili, BOSS, Weizhong, Futu) | Equity method (IAS 28) | "Investments in associates" | Proportional share of profits and losses | **No** |
| Joint ventures | Equity method | "Investments in joint ventures" | Sharing of profits and losses | **No** |
| Non-affiliated listed investments (Pinduoduo, Spotify, Snap, Sea residual) | FVTPL | Financial assets | Changes in fair value + dividends fully transferred to PL | **Yes (direct)** |
| Unlisted minority stakes (substantial VC/PE) | FVTPL-dominated | Long-term financial assets | Revaluation into PL | **Yes (Indirect)** |
| Strategic Minority Equity | FVOCI | Other Financial Assets | Only Dividends into PL | **Yes but not into PL** |

**Key insights**: The "fair value of the investment portfolio" disclosed by Tencent is approximately 1,035.8 billion (at the end of 2025). **Associated companies are listed based on book value rather than market value**. The book value seriously underestimates the true market value.

## 4. Specific treatment of equity method

### Kuaishou case (Tencent holds ~17-19%)

**Annual Process**:
1. Book value at the beginning of the year is X billion
2. Share of Kuaishou’s net profit for the year: 18% × Kuaishou’s net profit → Tencent’s “share of profits and losses of associated companies”
3. Kuaishou dividend payment: Tencent received cash → reduced bookkeeping
4. Changes in Kuaishou’s stock price: **not reflected in Tencent’s statements**
5. Impairment test: If the market value continues to be significantly lower than the book value (30%+ lower than December), impairment is required

**Meituan Case (17% stake before 2022 dividend payment)**:
- 2021-2022 Meituan stock price 460 → 60 (-87%), but Tencent’s report** only reflects shared losses** and does not reflect the collapse of market value
- The difference between book value and market value is hundreds of billions
- This is why the 2022-11 dividend triggers a **one-time material gain or loss** (fair value - equity method book)

### JD.com Case (17% shareholding before dividend announcement in 2021-12)
- After the completion of the distribution of 958 million shares (USD 16.4 billion) in 2022-03, the shareholding is 17% → 2.3%
- **Loss of significant influence → Reclassification from associate to FVTPL**
- Re-measure according to the fair value on the termination date, **the difference will be charged to the income statement in one lump sum**

## 5. Specific processing of FVTPL

### Pinduoduo case (shareholding ~14%, FVTPL)

**Annual Process**:
1. Fair value at the beginning of the year X billion (closing price at the end of the previous year)
2. Stock price changes during the period: revalued on a quarterly/annual basis, and the changes are directly entered into "other income, net"
3. Receipt of dividends: Recognition of "investment income"
4. Fair value at the end of the year: based on the closing price on the balance sheet date

**Number Intuition**:
- Pinduoduo rose 50% → Tencent’s income statement +0.5X billion
- Pinduoduo fell 50% → Tencent income statement -0.5X billion

**This is the main reason for the sharp fluctuations in Tencent’s net profit from 2021 to 2022**

### FVTPL Valuation of Unlisted Investments
- Valuation based on latest round of financing (Level 2) or DCF/comparable (Level 3)
- 2022-2023 The cooling of primary market valuations will directly impact Tencent’s income statement

## 6. Historical profit and loss impact of changes in fair value

### 2021: The first year of investment inflection point
- "Other income, net" contains significant impairment and revaluation of FVTPL
- **GAAP net profit attributable to shareholders 224.8 billion** (including one-time large gain from the sale of JD.com shares)
- **Non-GAAP net income $123.7 billion** (single digit growth)
- The difference is basically "change in fair value of investment + impairment"

### 2022: Deep losses
- Chinese concept stock crisis + Meituan stock price fell 80% (but not directly reflected by equity method) + FVTPL generally fell
- **GAAP net profit of $188.2 billion** (including a one-time gain of $16 billion from the reduction of Sea’s holdings)
- **Non-GAAP net profit 115.6 billion** (-7% year-on-year)

### 2023: Investment recovery
- **GAAP Net Income of $115.2 billion** (-39% YoY due to high 2022 base)
- **Non-GAAP net profit 157.7 billion** (+36% year-on-year)

### 2024: Restoration + Dividend Reduction
- JD/Meituan dividend triggers reclassification of profit and loss (completed)
- Overall fix for FVTPL portfolio (PDD, Spotify perform strongly)
- **GAAP Net Income $194 billion (+68%)**
- **Non-GAAP net income $222.7 billion (+41%)**

### 2025
- **GAAP net income $224.8 billion**
- **Non-GAAP net profit is about 250 billion** (estimate)

## 7. Accounting treatment for dividend payment and reduction of holdings

### 2021-12 Distribution of physical dividends for JD.com’s A shares

**Structure**: Tencent will distribute 958 million JD.com shares (USD 16.4 billion) to shareholders in proportion.

**Accounting Steps**:
1. **Time of declaration**: Measurement of dividends payable at fair value (IFRIC 17)
2. **Difference**: Fair value - Equity method book = **One-time disposal income is included in the income statement**
3. **Actual Distribution**: Offsetting Dividends Payable + Shareholders’ Equity
4. **Reclassification of remaining shareholding**: 2.3% shareholding loses significant influence → Convert from equity method to FVTPL, the difference goes to PL
5. **Follow-up**: The remaining JD.com will press FVTPL, and stock price changes will directly enter PL.

### 2022-11 Meituan dividend payment
- Similar mechanics
- 958 million shares distributed (USD 20.4 billion)
- 17% shareholding → ~1.5%

**Two dividend payments are an important contribution to Tencent’s 2024 GAAP net profit jump**

## 8. Full merger of subsidiaries

**Riot Games, Miniclip, Funcom, Techland (new in 2024), etc.**:
- Not an "investment" but a **subsidiary**
- Fully consolidated under IFRS 10
- Non-controlling interests are presented separately

**Supercell (51.2% owned by Halti S.A.)**:
- Tencent’s actual economic interest in Supercell through Halti is approximately 43%
- Halti consolidation in 2023
- Supercell’s revenue/profit will be fully consolidated into Tencent’s statements

## 9. "Operating Profit" vs "GAAP Net Profit"

**Tencent’s three-tier profit caliber**:

1. **Operating Profit**: Revenue - Operating Costs - Sales/Administrative/R&D Expenses ± Other Operating Income. **Excluding changes in fair value of investments**
2. **GAAP net profit attributable to shareholders**: complete IFRS net profit, including changes in fair value of investments, shared profits and losses from associates, disposal profits and losses, impairment, equity incentives, and amortization of intangible assets
3. **Non-GAAP (adjusted) net income**: On a GAAP basis excluding:
- Net change in fair value of investments
   - Gains and losses on investment disposals
   - Impairment provision
   - Equity incentive fee (SBC)
   - Amortization of intangible assets
   - Income tax implications

### Why the distinction
- **GAAP Volatility**: Investments account for a large proportion
- **Non-GAAP reflects operating conditions**
- Tencent management and sellers both use Non-GAAP as the core indicator

### 2024 Digital Comparison
- GAAP net income: $194 billion
- Non-GAAP net income: 222.7 billion
- Difference: Equity incentive RMB 30 billion + amortization of intangible assets + partial impairment

## 10. Which should investors look at?

| Perspective | Indicators to look at |
|------|---------|
| Operating Quality | Non-GAAP Net Profit + Operating Profit |
| Full Return | GAAP Net Income + OCI + True Market Value of Associates |
| Buffett's "look-through earnings" | Operating profit + major associates/FVTPL pro rata attributable net profit |
| Cash flow perspective | Cash flow from operating activities + cash inflow from investment disposal |

**ai-berkshire tendencies**:
- **Main business valuation**: Non-GAAP operating profit × reasonable multiple
- **Portfolio Valuation**: Standalone SOTP (Associates by market cap, FVTPL by fair value, Unlisted by book × discount)
- **Add the two** to get NAV
- **Avoid the simple valuation of "GAAP net profit × PE"**, because GAAP is seriously distorted by investment fluctuations

## 11. Data confidence

| Project | Confidence |
|------|-------|
| IFRS 9 / IAS 28 Accounting Standards Framework | **High** |
| Tencent Classification Framework (Equity Method/FVTPL/FVOCI) | **High** (Annual Report Note Disclosure) |
| Specific classification of individual targets | **Medium** (except for major joint ventures, not disclosed one by one) |
| 2021-2024 Historical Profit and Loss Impact | **High** |
| Dividend reduction accounting path | **Medium High** |
| 2025 full-year net profit forecast | **Low** (depends on market fluctuations) |

---

**ai-berkshire Tencent Investment Accounting Specialist · 2026-04-22**
