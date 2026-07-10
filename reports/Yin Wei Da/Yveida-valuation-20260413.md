# NVIDIA (NVDA) in-depth valuation report

**Date: 2026-04-13**
**Current stock price: $185.95 USD** (Yahoo Finance)
**Market Cap: ~$4.64 trillion USD**

> **Core pre-explanation**: The user decision-making criterion is "can understand the profit after 5-10 years". NVDA's 5-10-year profit forecast is low (the three black boxes of AI capex cycle, self-developed chip replacement, and China's sales ban). The valuation conclusion of this report is **low confidence** and is mainly used to demonstrate "why it is not suitable as a 6-select 1 heavy position" rather than to give precise buying and selling prices.

---

## 1. Factual basis (first-hand SEC data)

### 1.1 Financial Overview

| Indicators | FY2024 | FY2025 | FY2026 YTD | Source |
|------|--------|--------|-----------|------|
| Total Revenue | $60.9B | $130.5B (+114%) | Run Rate +94% | [SEC 10-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581025000023/nvda-20250126.htm) |
| Data Center | $47.0B | $115.2B (+145%) | $51.2B Single Q | [Q3 10-Q](https://www.sec.gov/Archives/edgar/data/1045810/000104581025000230/nvda-20251026.htm) |
| Gross profit margin | 64.7% | 65.1% | 73.4-73.6% | — |
| GAAP EPS | $1.19 | $2.94 (+147%) | ~$4.9 YTD Estimate | — |
| Free Cash Flow | $27.4B | $62.1B | Explosive Growth | — |

### 1.2 Current valuation level

| Indicators | Values | Historical comparison |
|------|------|---------|
| PE (based on FY2025 EPS $2.94) | **63.2x** | = Cisco 2000 Top |
| EV/Sales | **35.6x** | > Cisco 2000 (31x) |
| PEG | 0.57 | Seems cheap, with an implied growth rate of 70% + sustainability |

### 1.3 Customer concentration (Q3 FY26)

- Top 4 customers account for **61%** of revenue
- Customer A’s single share **22%**
- The four are actually AWS/Azure/GCP/Meta (through OEM)

---

## 2. Three unpredictable variables

### 2.1 AI CapEx cycle

**2026E hyperscaler CapEx total**: $6,200-7,000B (+58-78% year-on-year)
- Amazon $2,000B (+67%)
- Google $1,850B (+71%)
- Meta $1,150-1,350B (+53-80%)
- Microsoft $1,200B+ (+33%+)

**Historical Rule**: Hyperscaler CapEx has never maintained a +50% growth rate for three consecutive years.
**Current share price implications**: CapEx remains +50% from 2026-2028. **The probability of a pullback in 2027 is high**.

### 2.2 Self-developed chip replacement (has happened, not speculated)

| Vendors | Progress | NVDA Threats |
|------|------|---------|
| AWS Trainium2 | 500,000 online, 1 million by the end of the year | High (Anthropic has left NVDA) |
| Google Ironwood | Anthropic $100B rack contract | High (2027 launch) |
| Microsoft Maia | Deployed Services GPT-5.2 | Medium (Inference) |
| Meta MTIA | Hundreds of thousands for personal use | Medium (internal) |

**Source**: [Bloomberg 2026-04-06](https://www.bloomberg.com/news/articles/2026-04-06-broadcom-confirms-deal-to-ship-google-tpu-chips-to-anthropic), [AWS official](https://www.aboutamazon.com/news/aws/aws-project-rainier-ai-trainium-chips-compute-cluster)

### 2.3 Gross profit margin sustainability

- The current 73.4% is a high level as Blackwell’s supply exceeds demand.
- Normal water level should be 60-65%
- If it falls back to 65%, the net profit will be discounted by 16%**

---

## 3. CUDA moat status

| Moat Levels | 2020 | 2026 | Changes |
|-----------|------|------|------|
| Code Locked | Solid | Broken (AI Tools Automatically Migrate) | ⚠️ |
| Leading performance | 2-3 times | 10-30% (inference side) | ⚠️ |
| Ecological Network | Monopoly | Multiple Parallel | ⚠️ |
| 100,000 card system scale | Invincible | Still strong | ✅ |

- Claude Code implements CUDA→ROCm end-to-end migration in 30 minutes, with performance loss <10%
- ROCm 7.0 strategy: "Tighter alignment with CUDA semantics"
- Triton compiler supports AMD backend abstraction

---

## Four and three scenario valuations

### Agent original algorithm

| Scenario | Probability | FY28E EPS | Backward FY26 EPS | PE | Target Price |
|------|-----|----------|-------------|-----|--------|
| Cow | 20% | $11 | $2.67 | 40x | **$107** |
| Medium | 50% | $6.2 | $2.76 | 32x | **$88** |
| Bear | 30% | $3.0 | $1.77 | 20x | **$35** |

**Agent Weighted Goal: $75.9**

### ⚠️ Method objective correction

Agent folds FY28 EPS back to FY26 levels and then multiplies PE. This is **double discount** (compressing both growth and multiples), which is conservative.

**More standard algorithm**: directly use FY28E EPS × forward PE, and then discount it back to today.

| Scenario | FY28E EPS | Reasonable forward PE | FY28 target | Discounted to present (10%, 2 years) |
|------|----------|----------|---------|-----------------|
| Cow | $11 | 30x | $330 | **$273** |
| Medium | $6.2 | 22x | $136 | **$112** |
| Bear | $3.0 | 18x | $54 | **$45** |

**Correction Weighted (20/50/30)**: **$128**

The common conclusion of both algorithms is: **The current $186 is high by any reasonable standard**.
- Agent method: room for improvement -59%
- Correction method: upside space -31%

---

## 5. Historical Benchmark: Cisco 2000

| Dimensions | Cisco 2000 | NVDA 2026-04 |
|------|-----------|-------------|
| PE | 63x | 63.2x |
| EV/Sales | 31x | 35.6x |
| Market Cap | $569B | $4,640B (8x) |

**Cisco Ending**: 2000-03 high $79 → 2002-10 low $8.12 (-89.7%) → 22 years without returning to highs

**Warning**: Even great companies pay a heavy price for buying them at bubble prices.
(Disclaimer: History does not necessarily repeat itself, but it is worth being vigilant about)

---

## Six or five negative arguments

1. **Gross profit margin of 75% is unsustainable** - falling back to 65% means net profit -14%
2. **CUDA moat has been filled** - AI coding tools reduce migration costs from "months" to "hours"
3. **Customer concentration risk** - 22% comes from a single customer, and customers are accelerating self-research
4. **AI CapEx cyclicality is an iron law**——+70% for 3 consecutive years has never been seen in history
5. **Permanent Loss of China Market** – $17B (30%) is gone and will not come back

---

## 7. Buffett/Duan Yongping’s Perspective

### Why Buffett didn’t invest (meaning of many public statements)
> "Only invest in companies whose profits can be estimated for more than 5 years. NVDA cannot reasonably estimate it, so skip it directly."

### Duan Yongping (inference, based on Snowball’s speech)
> "The product is good, but the price is ridiculous. I dare not go short, but I won't take a heavy position at this price."

---

## 8. Predictability sorting (under 6-choose-1 criteria)

| Ranking | Company | Understand profits in 5-10 years |
|-----|------|-------------|
| 1 | Moutai | ⭐⭐⭐⭐⭐ |
| 2 | Tencent | ⭐⭐⭐⭐ |
| 3 | Meituan | ⭐⭐⭐ |
| 4 | Pinduoduo | ⭐⭐⭐ |
| 5 | Bubble Mart | ⭐⭐ |
| 6 | **NVIDIA** | **⭐** |

---

## 9. Conclusion

### Valuation interval (low confidence)

| Caliber | Reasonable price |
|------|-------|
| Strictly Conservative (Agent Law) | $76 |
| Standard DCF method | $128 |
| Optimistic | $200-270 |

### Choose 1 out of 6 suggestions for heavy positions

**❌ Not suitable for heavy positions**, reason:
1. Unpredictable profits in 5-10 years (violating the user first criterion)
2. Current prices include extremely optimistic assumptions
3. Downside risks far outweigh upside potential
4. There is a reason why Buffett/Duan Yongping do not invest.

### If it must be configured
- Position: <10%
- Holding period: 3-5 years (not permanent)
- Buy price: <$120 (may never be touched)
- Stop loss: Re-evaluation below $120

---

## Attachment: Data source
- [NVDA SEC 10-K FY2025](https://www.sec.gov/Archives/edgar/data/1045810/000104581025000023/nvda-20250126.htm)
- [NVDA Q3 FY26 10-Q](https://www.sec.gov/Archives/edgar/data/1045810/000104581025000230/nvda-20251026.htm)
- [Yahoo Finance NVDA](https://finance.yahoo.com/quote/NVDA/)
- [Bloomberg 2026-04-06 Ironwood](https://www.bloomberg.com/news/articles/2026-04-06-broadcom-confirms-deal-to-ship-google-tpu-chips-to-anthropic)
- [TechStrong - CUDA ROCm Migration](https://techstrong.ai/features/claude-code-ports-nvidia-cuda-to-amd-rocm-in-30-minutes/)
