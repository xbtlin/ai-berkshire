#DeepSeek——The Chinese laboratory that shocked the global AI industry

> "Understanding DeepSeek" series · Part 01 · Beginning
> Reading time approx. 8 minutes

---

## A set of facts that will help you re-understand the competitive landscape of AI

On January 27, 2025, a name that no one had heard of - DeepSeek - ranked first in the US App Store. It's not OpenAI, it's not Google, it's not any Silicon Valley company. It comes from Hangzhou, was founded less than two years ago, and has never raised a penny of external funds.

Then, the largest single-day evaporation of market value in the history of the U.S. stock market occurred:

- Nvidia plummeted 17% in a single day, and its market value evaporated by approximately **$600 billion** - the largest single-day market value loss in the history of U.S. stocks (Source: Bloomberg)
- The total evaporation of the AI sector on that day was approximately **1 trillion US dollars**
- Called the "Sputnik moment" in the field of AI by Western media (Source: MIT Technology Review)
- The global technology industry begins to re-examine the belief that "AI can only be done by burning money"

What did all this is a Chinese company that was established less than two years ago and has never raised a penny of external funds.

---

## What exactly is DeepSeek?

Let’s lay out the most basic information first:

| Project | Content |
|------|------|
| Full name | DeepSeek |
| Founder | Liang Wenfeng, born in 1985, graduated from Zhejiang University |
| Date of establishment | July 2023, Hangzhou |
| Team size | About **270 people**, average age** 28 years old** |
| External Financing | From establishment to April 2026: **Zero** (all from Magic Square Quantitative’s own funds) |
| Parent company | Magic Square Quantitative (quantitative hedge fund, management scale **70 billion+**) |
| Valuation in May 2026 | About **350 billion** (~$45 billion) (Source: Wall Street News, Sina Finance) |

In one sentence: **DeepSeek is an AI research laboratory supported by profits from quantitative funds. It uses very few people and extremely low costs to create large models at the global cutting-edge level. **

---

## Three things you must know

### The first thing: it is not a company, more like a laboratory

Liang Wenfeng, the founder of DeepSeek, has repeatedly emphasized that the goal of DeepSeek is not to make money, but "unrestricted research."

This sentence is not a slogan. Look at the evidence:

- API pricing is extremely low: V4 input price **$0.30/million tokens**, which is about **1/20** of GPT-5.4 (Source: DeepSeek official API pricing)
- All core models are open source under MIT protocol - weights and training codes are all open to the public
- The founder has never publicly conducted a commercial road show
- Founded two and a half years ago, relying on the quantified profits of the parent company Huanfang, without looking for external investors

**Contrary view**: In May 2026, DeepSeek finally launched its first round of financing, with a target of **50 billion**. Liang Wenfeng personally invested **20 billion**, and a large national fund negotiated to lead the investment (source: Sina Finance, 36 Krypton). This means that "unfunded idealism" is turning. As for whether it is forced by reality or an active choice, it remains to be seen.

### Second item: It achieves first-class performance at 1/20 the cost

The training cost of DeepSeek V3 (released in December 2024) is only **$5.6 million**, which is approximately **1/20** of the training cost of GPT-4 (source: DeepSeek technical paper).

V4-Pro, released in April 2026, goes one step further:

| Metrics | DeepSeek V4-Pro | GPT-5.4 | Claude Opus 4.6 |
|------|----------------|---------|-----------------|
| Total parameters | **1.6 trillion** | Undisclosed | Undisclosed |
| Activation parameters | **49 billion** | Undisclosed | Undisclosed |
| Context window | **1 million tokens** | 1 million+ | 1 million |
| LiveCodeBench | **93.5** (highest score) | Unpublished | Unpublished |
| SWE-bench | **80.6%** | Close | Close |
| Codeforces | **3206** | 3168 | Unpublished |
| API input price | **$0.30/M tokens** | ~$6/M | ~$15/M |

(Source: DeepSeek official, NoteLM, OfficeChai)

The data makes it clear: **DeepSeek V4 has entered the first echelon in the world in terms of programming and inference benchmarks, while the price is only 1/10 to 1/50 of competing products. **

**Contrary view**: In mathematical reasoning (HMMT 2026), Claude Opus 4.6 scored **96.2**, GPT-5.4 scored **97.7**, and V4-Pro scored **95.2** - the difference is not big but it does exist. On MMLU-Pro, V4-Pro (**87.5%**) also lags behind Gemini 3.1 Pro (**91.0%**). The term "comprehensive surpass" is not accurate. A more accurate judgment is "leading in specific fields and entering the first echelon as a whole."

### The third item: "DeepSeek shock" changed the narrative of the entire AI industry

Before the release of R1 in January 2025, the core belief of the global AI industry was that scale is everything: more GPUs, more data, and more funds can make better models.

R1 falsified this belief with facts:

- **671B parameters, only 37B activated** - the calculation amount is reduced by about 90%
- Training cost **5.6 million USD** (V3) + additional **~294,000 USD** (R1 pure RL training)
- Performance comparable to GPT-4 first generation model

How big is the impact? Just look at Nvidia's stock price - $600 billion disappeared in a single day, because the market suddenly realized: "Maybe AI companies don't need to buy so many GPUs."

**But what happened 11 months later? ** Nvidia shares fully recovered. The reason is **Jevons Paradox** (Jevons Paradox): Cost reduction → Lower threshold → More companies and scenarios use AI → The total demand for computing power increases instead.

This paradox currently appears to be true. But it cannot obliterate what DeepSeek proved: **Algorithmic innovation can bridge the computing power gap. **

---

## Why use a series to write about DeepSeek?

Because DeepSeek is a multi-layered nested evaluation problem:

| Layers | Problem | Complexity |
|---|------|--------|
| Technology | How far can MoE architecture + open source strategy go? | Need to understand the technical route |
| Business | How long can "not making money" last? What does first-round financing mean? | Need to see business logic clearly |
| Geopolitics | What is the impact of the chip ban + overseas ban on it? | Need to assess external risks |
| Parent Company | How long can Magic Square Quantitative’s profitability be sustained? | Need to analyze funding sources |
| Talent | Is an elite team of 270 people stable? | Need to look at the turnover of core personnel |

These issues are so intertwined that no layer can be viewed in isolation.

The next three articles will be broken down in order:

| # | Title | Core Question |
|---|------|---------|
| 02 | Technical route - MoE, open source and training efficiency | How deep is the technical moat? |
| 03 | Business and Competition - Magic Square Background, Realization and Opponents | How far can a non-profit model go? |
| 04 | Risk and Judgment - Chips, Regulation and Long-term Value | Is this laboratory worth paying attention to? |

---

## Next issue preview

In the next article, we will dismantle the core thing of DeepSeek - **technical route**.

A few tough questions to answer:

- What exactly is the MoE architecture? Why does it allow DeepSeek to catch up with the first-line level at 1/20 the cost?
- Is "all open source" a moat or a self-destructive Great Wall for DeepSeek?
- Why is R1-Zero's "Pure Reinforcement Learning Training" considered a milestone in AI research?
- What does it mean for V4 to adapt to Huawei Ascend chip?

---

*This article is the 01st article in the "Understanding DeepSeek" series. The next 3 articles will be released one after another. *
*This series does not constitute any investment advice. All data sources have been marked in the text. If there are any errors, please correct them. *
