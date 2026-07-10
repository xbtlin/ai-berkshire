# Shovel seller in the AI era

> "Understanding NVIDIA" series · Part 01 · Beginning
> Reading time approx. 8 minutes

---

## Is a company that has grown 27 times in three years worth 5.4 trillion?

In May 2026, Nvidia's net profit was $58.3 billion - and that's a figure for just one quarter. The same period three years ago was $2.1 billion.

The world’s largest market capitalization, $5.4 trillion. But compared to the market capitalization itself, the following table is more worth reading:

| Indicators | FY2023 (trough) | FY2026 (latest full year) | Q1 FY2027 (May 2026) | Changes |
|------|---------------|-------------------|----------------------|------|
| Revenue | $27 billion | **$215.9 billion** | **$81.6 billion** (single quarter) | 8x in 3 years |
| Net Profit | $4.4 billion | **$120.1 billion** | **$58.3 billion** (single quarter) | 27x over 3 years |
| Gross profit margin | 56.9% | 71.1% | **74.9%** | +18pp |
| ROE | 17.9% | **124.4%** | — | 7x |
| Free Cash Flow | — | **$96.7 billion** | — | — |
| Data center share | 55.6% | 89.7% | **92.2%** | — |
| Stock price (after split) | ~$15 | ~$110 (year low) | **~$221** | 15x in 3 years |

> Data source: NVIDIA FY2026 annual report, Q1 FY2027 financial report press release, Yahoo Finance

**In three years, revenue increased 8 times, net profit increased 27 times, and stock price increased 15 times. ** Unprecedented among large-cap companies.

But the real question is not "by how much", but: How long can this growth rate last? What kind of future is needed to support a market capitalization of $5.4 trillion? **

---

## What kind of company is NVIDIA?

Many people say that NVIDIA is a "chip company." This is not accurate.

**NVIDIA is the "shovel seller" in the AI era - what it sells is not chips, but computing infrastructure. **

Specifically, NVIDIA does three things:

| Business | Nature | FY2026 Revenue | Proportion |
|------|------|-----------|------|
| Data center GPU + network | Core engine for AI training and inference | **$193.7 billion** | 89.7% |
| Gaming GPUs | Consumer graphics processing | $16 billion | 7.4% |
| Auto + Robots | Autonomous Driving/Industrial AI | $2.3 billion | 1.1% |
| Professional Visualization + Other | Design/Rendering | $3.8 billion | 1.8% |

> Data source: NVIDIA FY2026 Annual Report

See clearly - **90% of NVIDIA's revenue comes from data centers**, and the gaming business has become a supporting role.

NVIDIA does not make its own chips - the design is handed over to TSMC, and it is a fabless model company. This means:

| Indicators | Data |
|------|------|
| Asset-liability ratio | D/E is only 5.4%, almost zero leverage |
| Profit margin | Gross profit margin 71-75%, net profit margin 56% |
| Cash Flow | Annual Free Cash Flow $96.7 billion, FCF/Net Profit > 80% |

**The financial quality is closer to a luxury company (high gross profit, high ROE, light assets) than a traditional semiconductor company. **

---

## Three common misunderstandings about NVIDIA

### Misunderstanding 1: NVIDIA’s moat is “leading chip performance”

This is the most common perception and the most incomplete.

Chip performance leadership does matter - the Nvidia B200's FP8 computing power is 3.4 times that of the AMD MI300X. But performance leadership is only the first layer of the moat.

The real moat is the CUDA ecosystem - a five-layer software barrier accumulated over 19 years (2006-2026):

| Level | Content | AMD Benchmark Gap |
|------|------|------------|
| Hardware Abstraction Layer | CUDA Driver / Runtime | ROCm lags behind 30%+ |
| Core Math Library | cuDNN / cuBLAS / NCCL / TensorRT | MIOpen 30-50% worse |
| Domain libraries | cuDF / cuML / RAPIDS / Modulus | AMD almost zero coverage |
| Framework layer | PyTorch/JAX defaults to CUDA first | ROCm is a second-class citizen |
| Application layer | HuggingFace / vLLM / ComfyUI | 80% partially supported by mainstream models |

**CUDA is not a product, but an entire ecosystem. ** There are **5 million CUDA developers** in the world, and 99% of GPU code on the Internet is written in CUDA. It's like Windows' lock on the PC - you can build a better operating system, but you can't move the millions of apps on it.

**Opposite view**: AI programming tools (Claude Code, GPT-5) can already port simple CUDA code to AMD's ROCm platform in 30 minutes, and the migration threshold is falling rapidly. CUDA's code-locking layer is being eroded.

We will expand on this in detail in Chapter 02.

### Misunderstanding 2: NVIDIA is a "monopoly"

Judging from the data, NVIDIA does account for **90%+** of the AI ​​training chip market. But this "monopoly" has a fatal weakness - its four largest customers all make their own chips. **

NVIDIA 10-Q Disclosure (FY2026 Q3):

| Customers | Revenue share | Self-developed chips |
|------|---------|---------|
| Customer A | **22%** | All in-house research |
| Customer B | 15% | All in-house research |
| Customer C | 13% | All in-house research |
| Customer D | 11% | All in-house research |
| **Top 4 Total** | **61%** | — |

> Data source: NVIDIA 10-Q (FY2026 Q3, filed October 26, 2025), SEC

These four end customers are AWS, Microsoft Azure, Google Cloud and Meta. They account for 61% of Nvidia's revenue - and are also building Trainium, Maia, TPU and MTIA to replace Nvidia's chips.

**Your biggest customer is your biggest potential competitor. ** This is extremely rare in business history.

**Contrary view**: Google has been working on TPU for 10 years and is still a big customer of NVIDIA - the speed of self-developed replacement may be slower than imagined. Moreover, the total AI computing power is expanding rapidly, and even if the share declines, absolute revenue may still grow.

### Misunderstanding 3: NVIDIA = Cisco 2000

This is a favorite analogy of bears. At the peak of the Internet bubble in 2000, Cisco's market capitalization was $500 billion, and its PE exceeded 200 times. The stock price fell **88%** after that, and it took **25 years** to return to its previous high.

Compare this:

| Metrics | Cisco 2000 | NVIDIA 2026 |
|------|------------|-------------|
| PE | >200x | ~23x (Q1 FY2027 annualized) |
| EV/Sales | 31x | ~25x |
| Gross profit margin trend | Contraction | Expansion (71% → 75%) |
| Actual payment demand | Internet users do not pay | Anthropic **$30 billion** ARR |
| Market Cap | $500 billion | $5.4 trillion (10x) |

**Nvidia is not a clone of Cisco - it has real paying demand, a far healthier valuation multiple, and still-expanding profit margins. **

**But don’t dismiss the analogy too easily**: NVIDIA’s EV/Sales (~25x) is near the top of Cisco (31x). The $5.4 trillion market capitalization means that the market has priced in "sustainable AI prosperity" - any cracks could trigger a valuation reset.

---

## To understand NVIDIA, 4 questions need to be answered

Define NVIDIA in one sentence:

> **The de facto standard of global AI computing power (90% + training share) + CUDA moat accumulated in 19 years but being eroded + "no error" valuation under $5.4 trillion market capitalization. **

Someone has written about these three things separately, but few have evaluated them together. That’s exactly what the next 4 posts will do.

| Question | Corresponding article |
|------|---------|
| How deep is the CUDA moat? What is being eroded? | Chapter 02 |
| How does NVIDIA respond to the market differentiation of training vs. inference? | Chapter 03 |
| At what stage have the four major customers developed their own chips? What about AMD? | Chapter 04 |
| How big is the cyclical risk? Are current valuations reasonable? | Chapter 05 · Final Chapter |

---

## Is Nvidia expensive now?

Leave a set of valuation figures, which will be expanded in detail in Part 05. Remember the magnitude first:

| Indicators | Data |
|------|------|
| PE (Q1 FY2027 annualized) | **~23x** (not expensive for 85% growth) |
| PE (FY2026 full year) | **~45x** (growth is decelerating) |
| Free Cash Flow (FY2026) | **$96.7 billion** |
| Net Cash | **~$52 billion** |

The two PEs give very different signals - 23x looks cheap, 45x looks expensive. The difference is: **How ​​many quarters can 85% growth be sustained? **

At the same time, don’t forget the structural risks: 90% of revenue comes from a single business, 61% comes from 4 customers, and these 4 customers are all developing their own alternative chips. The $5.4 trillion market capitalization requires continued rapid growth for many years in AI computing power demand to support it.

**For the same data, bulls and bears read completely different conclusions. ** Let’s take a look at the next 4 articles.

---

## Next issue preview

Next article Tear down the CUDA moat - no one has breached it in 19 years, why are cracks starting to appear now?

Four tough questions:

- Jen-Hsun Huang said, "Other people's chips are more expensive than Nvidia's for free" - why?
- What are the 5 million CUDA developers locked up?
- AI Programming Tools 30 Minutes to Port CUDA Code – Is the Moat Really Collapse?
- What new form is the moat changing from "software lock-in"?

---

*This article is the 01st article in the "Understanding NVIDIA" series. *
*This series does not constitute any investment advice. *
