---
name: quality-screen
description: "AI Berkshire skill: Eliminate inferior companies: 7 indicators to quickly eliminate non-first-class companies. Source: skills/quality-screen.md."
---

## Codex adapter note

This skill is generated from `skills/quality-screen.md` so Claude Code and Codex users share one canonical workflow.

- Treat `$ARGUMENTS` as the user's request in the current Codex thread.
- When the source mentions Claude-only surfaces such as Task, Agent, WebSearch, Bash, Read, or Write, use the closest Codex capability available in this session: subagents when available, web search when needed, shell commands for local tools, and normal file edits for workspace files.
- Use shared project tools from `tools/` in this repository. Prefer running commands from the repository root with paths like `python3 tools/financial_rigor.py ...`; if the current thread starts outside the repo, locate the actual checkout path first instead of assuming a fixed home-directory path.
- Before starting research, run the `date` command to confirm today's date; treat it as the baseline for "latest" data and state the data cutoff date in the report header. Never assume the current date from training data.
- Preserve the research quality rules from `AGENTS.md`: cross-check financial data, use exact arithmetic tools for valuation/math, and clearly label uncertainty and source gaps.

# Eliminate inferior companies: 7 indicators to quickly eliminate non-first-class companies

Perform filtering on $ARGUMENTS to quickly eliminate targets that do not meet the standards of first-class companies.

**Supported input formats**:

| Input method | Example | Description |
|---------|------|------|
| Individual stocks | `Tencent, Meituan, Nvidia` | Screen by stock |
| Industry | `China Beer Industry` `Global Cloud Computing` `Hong Kong Sports Brands` | First search for the main listed companies in the industry (10-20 companies), and then filter them one by one |
| Market/Index | `Hang Seng Index Components` `CSI 300` `Nasdaq 100` | Pull the list of constituent stocks and filter them one by one |
| Topic | `China’s Top 50 High Dividend Companies` `Global AI Computing Power Chain` | Search for companies related to the theme first, and then filter them one by one |

In the industry/market/topic mode, the output additionally includes: pass rate statistics, ranking within the industry, and sector comparison summary.

## Design principles

- **Goal**: Kill any first-class good companies, but eliminate certain non-first-class companies
- **Logic**: 7 hard indicators + 2 exemption rules, it is better to slip through the net than to accidentally kill
- **Scope of application**: All listed companies (Bank/Insurance does not apply to Article 3 interest coverage ratio)

---

## 7 indicators to remove defects

| # | Metrics | Exclusions | What is measured |
|---|------|---------|-------------|
| 1 | 10-year average ROE | < 8% | Capital efficiency – can shareholders’ money outperform the opportunity cost |
| 2 | 5-year cumulative free cash flow | is negative | Real money - is profit "paper wealth" |
| 3 | Interest coverage ratio (EBIT/interest) | < 2 times | Debt repayment safety - the ability to repay interest |
| 4 | Long-term gross profit margin | < 15% | Pricing power - whether products/services are differentiated |
| 5 | Operating cash flow / net profit (5-year average) | < 0.7 | Profit quality - whether the profits earned can be recovered in cash |
| 6 | Long-term net interest rate | < 5% | Risk resistance - whether profits return to zero when income fluctuates |
| 7 | 5-year total equity expansion | > 20% (not due to mergers and acquisitions) | Shareholder interests - whether management is diluting your interests |

## 3 exemption rules

### Exemption A: Strategic investment period exemption (applicable to Article 1)

If the following three conditions are met at the same time, Article 1 ROE failure to meet the standard can be exempted:
1. Listed less than 10 years ago
2. Gross profit margin > 30% (proves that the business model itself has pricing power)
3. The operating cash flow in the last 2 years has been positive (proving that hematopoietic ability is already available)

**Logic**: High gross profit margin + positive cash flow shows that the business model is okay, and ROE is low just because it is still in the investment period. Typical case: Meituan.

### Exemption B: Active Low Margin Exemption (Applies to Article 6)

If the following two conditions are met at the same time, Article 6 can be exempted from non-compliance with the net interest rate standard:
1. Gross profit margin > 30% (able to earn but choose not to)
2. The net interest rate has risen to above 5% in the past two years, or is showing a clear upward trend

**Logic**: High gross profit margin indicates pricing power, while low net profit margin indicates strategic choice (reinvestment) rather than lack of capability. Case in point: Amazon.

### Exemption C: Exemption for high turnover and low profit model (applicable to Articles 4 and 6)

If the following three conditions are met at the same time, Article 4 gross profit margin and Article 6 net profit rate can be exempted from non-compliance:
1. ROE > 20% (proves that although profit margins are low, return on capital is extremely high)
2. Operating cash flow/net profit > 1.0 (no problem with profit quality)
3. The business model belongs to the "membership/platform commission/high turnover and small profit" type (profit is not reflected in product price increases)

**Logic**: The profits of some first-class companies are not hidden in gross profit margin, but in membership fees, turnover efficiency or platform commissions. Their gross profit margin and net profit margin are naturally very low, but their extremely high ROE shows that their capital efficiency is first-class. Typical case: Costco (gross profit margin 12%, net profit margin 2.5%, but ROE 25%+, membership renewal rate 90%+).

---

## Execution process

### Step 1: Parse the input and determine the filtering range

**Mode Judgment**:
- If the input is a specific company name/code → **Individual stock mode**, go directly to the second step
- If the input is industry/market/topic → **Batch Mode**, perform the following operations first:
  1. Use WebSearch to search for major listed companies in this industry/market/topic
  2. Industry model: covering the top 15-20 listed companies in the industry by market capitalization
  3. Index mode: pull the complete list of constituent stocks
  4. Topic mode: Search related companies, covering 15-30 companies
  5. List the complete list of companies for confirmation (if the number of companies is >30, process it in batches in parallel)

Determine the full name, code, and exchange for each company.

### Step 2: Parallel data collection

Start an independent backend Agent for each company and use WebSearch to search the following data:

1. **ROE**: ROE year by year in the past 10 years (or since listing), calculate the average
2. **Free Cash Flow**: Operating cash flow and capital expenditures in the past 5 years, calculating the cumulative FCF in the 5 years
3. **Interest Coverage**: Latest annual EBIT and interest expense, calculated as a multiple
4. **Gross profit margin**: Gross profit margin trend in the past five years
5. **Operating cash flow/net profit**: the ratio in the past 5 years, calculate the average
6. **Net interest rate**: Net interest rate trend in the past 10 years, calculate the average
7. **Change in total share capital**: total share capital 5 years ago and now, calculating the expansion ratio

Data source priority: Company annual report > Brokerage research report > Financial data platform

### Step 3: Check item by item

For each company, 7 indicators are tested one by one:
- ✅ Passed
- ❌ Failed
- ⚠️ Boundary (with numerical description)

If a certain article is violated, check whether the corresponding exemption conditions are met.

### Step 4: Output the results

#### Output format

```markdown
# Remove bad filter results

**Filter Date**: {today’s date}
**Number of companies**: {N}

## Summary table

| Company | ①ROE | ②FCF | ③Interest Coverage | ④Gross Margin | ⑤OCF/NI | ⑥Net Margin | ⑦Dilution | Results |
|------|------|------|----------|---------|---------|---------|-------|------|
| xxx | ✅ 24% | ✅ | ✅ | ✅ 56% | ✅ | ✅ 30% | ✅ | **Passed** |
| yyy | ❌ 3% | ❌ | ❌ | ✅ 20% | ✅ | ❌ 2% | ✅ | **EXCLUDED** |
| zzz | ⚠️→✅ | ✅ | ✅ | ✅ 35% | ✅ | ⚠️→✅ | ✅ | **Exemption Passed** |

## Passed companies (N companies)
[list]

## Excluded companies (N companies)
| Company | Violation indicators | Specific data | Reasons for exclusion |
|------|---------|---------|---------|

## Companies that passed the exemption (N companies)
| Company | Exemption clauses | Specific data | Reasons for exemption |
|------|---------|---------|---------|

## Boundary dispute (if any)
[Additional explanation for companies near the threshold]

## Sector summary (specific to industry/market model)

**Pass rate**: {Number of passes}/{Total number} = {Percent}
**Industry Quality Judgment**: [The overall quality evaluation of the industry is given based on the pass rate]

| Quality Stratification | Company | Common Characteristics |
|---------|------|---------|
| First-class (all passed + high ROE) | xxx, yyy | ... |
| Passed (all passed but mediocre indicators) | aaa, bbb | ... |
| Elimination | ccc, ddd | ... |

**Industry stock selection conclusion**: [In one sentence, summarize whether the industry is worth digging into, and who are the 2-3 companies that deserve the most attention]
```

---

## Notes

1. **Bank/Insurance**: Article 3 (interest coverage) does not apply, and the essence of its business model is interest spread management
2. **REIT**: ROE may fluctuate greatly due to property revaluation, so use "core operating profit ROE" instead
3. **Insufficient data**: If a certain data cannot be obtained, it will be marked as "insufficient data" instead of directly determining pass/fail.
4. **Cyclical industries**: Use the average of a complete cycle (covering at least one high and one low), not a single year
5. **Short time to market**: Companies with less than 5 years old use all available data, but mark "insufficient data window" in the results

## Limitation statement

This set of indicators can eliminate companies that are "not sure", but screening does not mean "definitely good". Companies that have been approved still need further research:
- Is the business model sustainable?
- Is management trustworthy?
- Is the current valuation reasonable?
- Is the competitive landscape deteriorating?

Eliminating the bad is the first step, not the last.
