#Technical route - MoE architecture, open source strategy and training efficiency breakthrough

> "Understanding DeepSeek" Series·Part 02
> Reading time is about 10 minutes

---

## Why should we talk about technology first?

A team of 270 people spent US$5.6 million to train a global cutting-edge large model. If this is just luck, it has no research value; if it is structural - it changes the competitive logic of the entire AI industry.

There is only one way to judge this matter: understand the technical route. This article will try to explain the four core innovations clearly in non-technical language.

---

## Innovation 1: MoE architecture - use 1/10 of the electricity cost to perform calculations of the same magnitude

### What is MoE?

Traditional large models (such as early GPT-4) are "dense models" - for every inference, **all parameters** are involved in the calculation. A model with 1 trillion parameters requires all 1 trillion parameters to be used for each question.

MoE (Mixture of Experts) has a completely different idea: split the model into multiple "expert modules", and only activate a small part of them for each inference.

Analogy: In a law firm with 500 lawyers, when a client comes, not all 500 of them come together, but only the 5 most relevant experts are sent based on the type of case.

Data from DeepSeek V3:

| Indicators | Values |
|------|------|
| Total parameters | **671 billion** (671B) |
| Parameters for each activation | **37 billion** (37B) |
| Activation ratio | About **5.5%** |

V4-Pro goes one step further:

| Indicators | Values |
|------|------|
| Total parameters | **1.6 trillion** (1.6T) |
| Parameters for each activation | **49 billion** (49B) |
| Activation ratio | About **3%** |

(Source: DeepSeek technical paper, Hugging Face model page)

**What does this mean? ** V4-Pro has a "knowledge capacity" of 1.6 trillion parameters, but each calculation only consumes the computing power cost of 49 billion parameters. Breadth of knowledge and efficiency of reasoning, both achieved.

**Contrary view**: MoE is not DeepSeek’s invention—Google’s Switch Transformer (2021) and Mixtral (2024) all use MoE. DeepSeek's contribution is to achieve the ultimate engineering excellence in MoE on a very large scale, but this does not mean that other companies cannot copy it. In fact, within weeks of the release of V4, multiple laboratories were already working on similar architectures.

### Key advantages of MoE

| Advantages | Description |
|------|------|
| Low training cost | V3 training costs only **$5.6 million**, while a dense model with the same performance requires hundreds of millions of dollars |
| Low inference cost | Only 3-5% of parameters are activated each time, and the electricity cost of a single inference is greatly reduced |
| Good scalability | You can continue to add "experts" without increasing the cost of reasoning |

---

## Innovation 2: MLA attention mechanism - solving the memory bottleneck of long text

Large models have a technical bottleneck when processing long text: **KV-cache** (key-value cache) will grow linearly with the context length and consume a lot of GPU memory.

DeepSeek's **MLA (Multi-head Latent Attention)** significantly reduces the memory footprint of KV-cache by performing low-rank compression on the attention head.

On this basis, V4 further introduces **CSA (Compressed Sparse Attention)** and **HCA (Heavy Compressed Attention)** hybrid mechanisms:

| Indicators | Comparison V3 |
|------|--------|
| Single token inference calculation amount | Only **27%** of V3 |
| KV-cache usage | Only **10%** of V3 |
| Context window | Expanded from 128K to **1 million tokens** |

(Source: DeepSeek V4 technical paper)

**Why is this important? ** A context window of 1 million tokens means that an entire book and entire code base can be read in at once. The compression of KV-cache means that the hardware cost of this capability is greatly reduced - not by stacking more expensive GPUs, but by smarter algorithms.

---

## Innovation 3: FP8 mixed precision training and R1-Zero

### FP8 training

Traditional large models are trained with FP16 (16-bit floating point) or BF16. DeepSeek V3 is the first open source large model to successfully complete complete training with FP8 (8-bit floating point).

The number of digits is halved, and the direct effect is:

- Memory usage halved
- Computational throughput almost doubled
- The total training cost is further reduced

(Source: DeepSeek V3 arXiv paper)

**Opposite view**: FP8 training has been discussed in academic circles for many years, and NVIDIA's H100/H200 itself supports FP8 computing power. DeepSeek's contribution is the first to run through a complete pipeline of FP8 training on a very large-scale model, but this technology will be quickly followed by the industry.

### R1-Zero: A milestone in pure reinforcement learning

In January 2025, DeepSeek R1 was released with a research result-**R1-Zero**.

Traditionally training the reasoning ability of large models requires first using manually labeled "thinking chain" data for supervised fine-tuning (SFT), and then reinforcement learning (RL). This process relies on a lot of manual annotation.

The breakthrough of R1-Zero is: **Completely skipping supervised fine-tuning, using only reinforcement learning, the model spontaneously emerges an inference chain**.

This is regarded by the academic community as a landmark event - it implies that human reasoning may not need to be taught by humans, and AI can learn to "think" through self-play. **

**Contrary view**: The actual performance of R1-Zero is not as good as R1 that has gone through the complete SFT+RL process. Its academic significance is greater than its engineering significance. But it validates a theoretical path that could have long-term effects far beyond short-term benchmark scores.

---

## Innovation 4: Full MIT open source - moat or digging your own grave?

All core models of DeepSeek - V3, R1, V4 - are all open source under the MIT license. This is one of the loosest open source licenses, meaning:

- Anyone can download model weights for free
- Can be used for commercial purposes
- No requirement to open source modified versions
- All training codes and tools are also made public

**38% of new AI papers in Q1 2025 cite DeepSeek's tools or data sets** (Source: DemandSage statistics). On Hugging Face, the DeepSeek model has been downloaded more than **800,000 times per month**.

### Pros and Cons of Open Source Strategy

| Dimension | Long (moat theory) | Short (self-destruction theory) |
|------|-----------------|---------------|
| Ecology | Once a developer ecosystem is established, it is extremely difficult to migrate | Others take away the code and train their own models |
| Talent attraction | The world's top researchers are willing to contribute to open source projects | Core intellectual property rights are given away for free |
| Brand | "Linux in AI" - huge influence | The Linux Foundation does not make money |
| Business | Low API price + open source = occupy the developer market | Competitors use your model to make competing products |
| Security | Code transparency → more complete security audit | Malicious users can remove security restrictions |

**A fact that cannot be ignored**: As of May 2026, DeepSeek ranks first in the world in the field of open source large models, and the GitHub warehouse has accumulated more than **70,000 stars** (Source: GitHub). On the track of "open source AI", DeepSeek has established a significant first-mover advantage.

**But another fact cannot be ignored**: Anthropic (Claude) and OpenAI are taking completely opposite closed-source routes, and both are far ahead of DeepSeek in commercialization. Whether the influence of open source can be transformed into sustainable competitive advantage is still unclear.

---

## V4 adapts to Huawei Ascend: a key turning point

On April 24, 2026, when DeepSeek V4 was released, there was an easily overlooked detail: ** it was simultaneously announced that it fully supports the Huawei Ascend 950 chip **.

This means:

| Changes | Before | After |
|------|------|------|
| Training dependencies | Mainly dependent on NVIDIA H800 | Start adapting to Huawei Ascend |
| Inference deployment | CUDA ecosystem (NVIDIA) | CANN framework (Huawei) |
| Supply chain risk | Extremely high (U.S. chip ban) | Have backup routes |

Huawei Ascend 950 super node achieved a single-card decoding throughput of **4,700 TPS** on V4-Pro, and the first token delay was about **20ms** (Source: Huawei Computing, Science Network).

**This is the first time that a world-class open source large model has been deployed full-stack from training to inference on a domestic chip**, without relying on any NVIDIA hardware.

**Contrary view**: There is still a performance gap between Ascend chips and NVIDIA's latest H200/B100. It will take time for Huawei's own production capacity to ramp up - V4-Pro's high-end inference service is currently limited by computing power, and the price is not expected to drop significantly until the Ascend 950 is mass-produced in the second half of 2026. "De-beautification" is the direction, but it is far from complete.

---

## How long can technological leadership last?

This is the hardest question to answer. Directly give the pros and cons:

### Reasons to be bullish

1. **Organizational capabilities for algorithm innovation**: A team of 270 people continues to produce three generations of breakthrough results, V3→R1→V4, indicating that the team’s "research density" is extremely high
2. **Cost advantage has compound interest effect**: low training cost → fast iteration speed → further reduction of cost
3. **Open source ecological barriers**: 38% of new papers globally are cited. Once the developer ecosystem is locked, it is difficult to migrate.
4. **Domestic chip adaptation first**: The experience in Ascend will become the benchmark for subsequent domestic substitution.

### Reasons to be bearish

1. **MoE architecture is not a secret**: All technical papers are made public, and competitors can quickly follow up.
2. **Brain drain is already happening**: From the end of 2025 to the beginning of 2026, many core members resigned to join Xiaomi, Tencent, and ByteDance (Source: 36 Krypton)
3. **No equity incentives**: The elite team of 270 people does not have the equity locking mechanism of listed companies.
4. **Chip Gap**: Ascend Adaptation reduces supply chain risks, but the efficiency of training cutting-edge models may still be limited

**A more prudent judgment is**: there is a high probability that technological leadership can be maintained for **1-2 years**. A lead of more than 3 years depends on team stability, chip supply and the speed of opponents catching up - all of which are highly uncertain.

---

## Next issue preview

Technology is just the starting point. In the next article, we will answer a more pointed question - where does the money for this laboratory come from? How far can you go? **

Questions to break down:

- What exactly is magic square quantification? How long can its profits support DeepSeek?
- What does the first round of financing of 50 billion yuan mean? Is "idealism" still there?
- In competition with OpenAI, Anthropic, and Google, where does DeepSeek stand?
- Is "not commercializing" a strategy or a necessity?

---

*This article is the 02nd article in the "Understanding DeepSeek" series. *
*This series does not constitute any investment advice. All data sources have been marked in the text. If there are any errors, please correct them. *
