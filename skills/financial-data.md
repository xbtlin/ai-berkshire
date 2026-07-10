# Financial data acquisition and cross-validation specifications

This specification applies to all research involving corporate financial data. **Each key data must come from two independent sources, and errors >1% must be marked. **

---

## Data source priority

### US stocks (PDD, Tencent ADR, NetEase ADR, etc.)

| Priority | Source | URL | How to obtain |
|--------|------|-----|---------|
| 1 (main) | **macrotrends** | macrotrends.net/stocks/charts/{ticker} | Direct access, no registration required |
| 2 (Deputy) | **stockanalysis** | stockanalysis.com/stocks/{ticker}/financials | Direct access, no registration required |
| Original First Hand | SEC EDGAR | sec.gov/cgi-bin/browse-edgar | 10-K / 10-Q Original Text |

### Hong Kong stocks (Tencent 0700, NetEase 9999, Meituan 3690, etc.)

| Priority | Source | URL | How to obtain |
|--------|------|-----|---------|
| 1 (main) | **aastocks** | aastocks.com/tc/stocks/analysis/company-fundamental | Direct access |
| 2 (Deputy) | **macrotrends** (ADR code) | Tencent uses TCEHY, NetEase uses NTES | Direct access |
| Original First Hand | HKEX Disclosure | hkexnews.hk | Annual Report PDF |

### A shares (Sanqi Interactive Entertainment, Gigabyte, etc.)

| Priority | Source | URL | How to obtain |
|--------|------|-----|---------|
| 1 (main) | **Eastern Wealth** | eastmoney.com → Search stock code → Financial statements | Direct access |
| 2 (Vice) | **Cninfo** | cninfo.com.cn | Original annual report/quarterly report PDF |

---

## Execution specifications

### Step one: Get data

For each financial indicator (revenue, net profit, gross profit margin, operating cash flow, asset-liability ratio, etc.), take the numbers from **Source 1** and **Source 2** respectively.

### Step 2: Error calculation and marking

```
Error rate = |Source 1 value - Source 2 value| / Source 1 value × 100%
```

| Error | Processing |
|------|---------|
| ≤ 1% | ✅ Consistent, take the value of source 1 and mark two sources |
| 1% ~ 5% | ⚠️ Mark "Data discrepancies", indicate two values, and explain the possible reasons (exchange rate/accounting standards) |
| > 5% | ❌ Marked "Major differences in data", the original financial report must be checked for verification and may not be used directly |

### Step 3: Data presentation format

Each key data must be labeled in the following format:

```
Revenue: 123.9 billion yuan ✅
  - macrotrends: 124.1 billion yuan
  - stockanalysis: 123.7 billion yuan
  - Error: 0.3%
```

Difference example:
```
Net profit: 24.5 billion yuan ⚠️ There are differences in data
  - macrotrends: 24.5 billion (GAAP)
  - stockanalysis: 27.8 billion yuan (Non-GAAP)
  - Error: 13.5% — Reason: different accounting standards (GAAP vs Non-GAAP)
```

---

## Common reasons for differences (not necessarily data errors)

| Reason | Description |
|------|------|
| GAAP vs Non-GAAP | Most common, especially profit data |
| Exchange rate conversion | Hong Kong dollar/renminbi/US dollar conversion time is different |
| Fiscal year definition | Calendar year vs fiscal year (such as Apple’s fiscal year ends in October) |
| Merger caliber | Whether minority shareholders’ interests are included |
| Data update lags | A certain platform has not updated the latest financial report |

---

## Special rules

1. **Unlisted companies** (MiHoYo, Lilith, etc.): When there are only primary data sources, mark `[estimate]` before the data, and no cross-validation is performed.
2. **Quarterly data vs. annual data**: Priority is given to using annual data for cross-validation. Some sources of quarterly data may be lagging behind.
3. **Original financial report takes precedence**: If both sources are inconsistent with the original financial report (10-K/annual report PDF), the original financial report shall prevail and the source will be marked as incorrect.

---

## Stock price and restoration of rights (must read for historical sequences)

There are three calibers of price. Mixing them will distort the historical stock price position, long-term growth rate, and historical valuation quantiles:

| Caliber | Meaning | Purpose |
|------|------|------|
| No restoration of rights | Actual transaction price, gap on ex-rights and ex-dividend days | Only used for "current point in time" snapshot |
| Pre-right restoration | Recall the historical price based on the latest price | Historical stock price comparison, N-year increase, historical PE band, always use it |
| Post-resumption of rights | Forward based on the first day of listing | Calculate historical total return/annualized return |

Rules:

1. For analysis involving historical prices, **previous reinstatement** shall be uniformly used, and **reinstatement and non-reinstatement sources shall not be mixed within the same analysis.
2. The current market value/current PE can be calculated by using **current actual stock price × current total equity**, which has nothing to do with re-righting - re-righting only affects the historical sequence.
3. Per-share indicators (historical EPS, historical stock price) that exceed stock splits/large-proportion transfers must be restored and then compared with the same period last year.
4. Total return/annualized income needs to be included in dividends (included in post-rights restoration), and it will be underestimated if you only look at the price increase.
5. The market value calculation after additional issuance/repurchase shall be based on the latest total share capital (`financial_rigor.py verify-market-cap` will prompt for verification if the deviation is >5%).

---

## Quick index

| Scenario | Primary Source | Alternate Source |
|------|---------|---------|
| PDD / Pinduoduo | macrotrends.net/stocks/charts/PDD | stockanalysis.com/stocks/pdd |
| Tencent | macrotrends.net/stocks/charts/TCEHY | aastocks (0700.HK) |
| NetEase | macrotrends.net/stocks/charts/NTES | aastocks (9999.HK) |
| Sanqi Interactive Entertainment | eastmoney.com (002555) | cninfo.com.cn |
| Gigabit | eastmoney.com (603444) | cninfo.com.cn |
| Nintendo | macrotrends.net/stocks/charts/NTDOY | stockanalysis.com/stocks/ntdoy |
| Capcom | macrotrends（CCOEY） | stockanalysis（CCOEY） |
