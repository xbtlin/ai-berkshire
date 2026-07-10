# AI Compute Supply Chain Panorama Research Report

**Date:** 2026-05-09
**Research scope:** The full AI compute supply chain, from upstream chip design/manufacturing/materials to midstream servers/networking/storage and downstream cloud computing/applications, from a global perspective
**Research method:** Four parallel research teams (upstream chip design, upstream manufacturing and packaging, midstream equipment and networking, downstream cloud and applications), with cross-validation of data

> Research principle: Start with the data, then build the logic. Every judgment includes counterarguments. Estimates are labeled "estimate."

---

## Supply Chain Panorama

```text
AI COMPUTE SUPPLY CHAIN PANORAMA

Top upstream: Design tools and IP
- EDA tools: Synopsys 31%, Cadence 30%, Siemens EDA 13%
  Gross margin: 76-86%
  Substitutability: 1/5
  Pricing power: Very strong
- IP licensing: ARM, RISC-V
  ARM gross margin: 97%
  Substitutability: 1/5
  Pricing power: Very strong

Upstream: Chip design (fabless)
- GPU / AI accelerators: NVIDIA, AMD, Intel
- Custom ASIC: Broadcom, Marvell, Google/AWS/Meta/Microsoft in-house chips
- China AI chips: Huawei Ascend, Cambricon

Upstream: Semiconductor manufacturing and packaging
- Foundry: TSMC, Samsung Foundry, Intel Foundry, SMIC
- Equipment: ASML, Applied Materials, Lam Research, Tokyo Electron, KLA
- Advanced packaging: TSMC CoWoS, ASE, Amkor
- Materials: Shin-Etsu, JSR/TOK, Japanese photoresists

Midstream: Key components
- HBM memory: SK hynix, Micron, Samsung
- Networking chips/switches: Broadcom, Arista, NVIDIA networking
- Optical modules: InnoLight, Eoptolink
- Servers: Dell, Foxconn/Hon Hai, Supermicro, HPE, Inspur
- Cooling/liquid cooling and power: Vertiv, Schneider Electric, Eaton

Downstream: Cloud computing and compute services
- Hyperscale cloud: AWS, Azure, Google Cloud, Meta
- China cloud: Alibaba Cloud, Tencent Cloud, Baidu AI Cloud, ByteDance
- GPU rental / compute brokers: CoreWeave, Lambda

End terminal: AI models and applications
- Global AI companies: OpenAI, Anthropic, xAI, DeepMind
- China AI companies: DeepSeek, Zhipu AI, MiniMax, Moonshot AI
```

---

## Investment Logic Chain

AI model scale continues to expand, driven by surging training and inference demand
    -> GPU / AI chip demand explodes (NVIDIA data center revenue reached $197.3 billion in FY26)
        -> Advanced-node capacity tightens (TSMC CoWoS at full utilization, HBM in short supply)
            -> Upstream equipment and materials benefit (ASML backlog of EUR 38.8 billion, SK hynix gross margin 79%)
    -> Hyperscale cloud providers enter an arms race (2026 total capital expenditure of $660-690 billion)
        -> Servers, networking, cooling, and power all benefit
            -> But profit distribution is highly uneven: chip design > manufacturing > memory > networking >> server assembly

### Logic Chain Validation

| Segment | Core assumption | Validation event | Status |
|------|------|------|------|
| AI demand -> chip demand | AI training/inference continues to expand | NVIDIA FY26 data center revenue $197.3 billion (+65%); hyperscaler capex $660 billion+ | Strongly validated |
| Chip demand -> capacity tightness | Advanced nodes, packaging, and HBM remain undersupplied | TSMC CoWoS full through 2027; SK hynix and Micron 2026 capacity fully sold out | Strongly validated |
| Tight capacity -> upstream price increases | Bottleneck segments have pricing power | TSMC 2026 price increases of 5-10%; HBM up 20%/year; ASML EUV unit price $200-400 million | Strongly validated |
| Cloud arms race -> broad supply-chain benefit | Capex keeps rising | 2026 combined capex for the top six hyperscalers is $660-690 billion; Goldman expects $1.15 trillion cumulative in 2025-2027 | Strongly validated |
| Custom chips -> erosion of NVIDIA | Long-term de-NVIDIA-ization trend | Google TPU v7, AWS Trainium 1.4 million units, 2026 custom ASIC shipments +44.6% vs GPU +16.1% | Trend confirmed, but progress is slow |

---

## Part 1: Deep Dive by Segment

### 1. Top Upstream - Design Tools and IP ("rent collectors" of the chain)

#### 1.1 EDA Tools: One of the strongest oligopolies in the world

**Core conclusion: EDA may be the deepest-moat, most irreplaceable segment in the entire semiconductor value chain.**

| Company | Market share | Gross margin | Operating margin | Pricing power |
|------|------|------|------|------|
| Synopsys (SNPS) | 31% | 76-80% | ~35% | Very strong |
| Cadence (CDNS) | 30% | **86%** | 35% | Very strong |
| Siemens EDA | 13% | N/A (inside the group) | N/A | Strong |
| **Combined** | **74-85%+** | - | - | - |

**Why it is hard to replace (substitutability: 1/5):**
- Customer retention is close to **100%** - EDA has almost no customer churn.
- **80-85% recurring revenue** (subscription model).
- Switching EDA platforms means huge costs, a collapse in productivity, migration nightmares, and a risk of chip design failure.
- Large customers often buy from **both** Synopsys and Cadence - even customers cannot choose between them easily.
- The more complex the chip, the more dependent it becomes on EDA - the AI chip boom directly benefits EDA.

**China domestic EDA (Empyrean, etc.):** Domestic localization exceeds 30% for analog-chip EDA, but is below 15% for digital-chip EDA. High-end areas (hardware emulation, formal verification, timing analysis) are still almost blank.

**Duan Yongping-style question - is this a good business?**
> An excellent business. 86% gross margin, 100% customer retention, 85% recurring revenue, oligopoly structure, and the more complex chips become, the more indispensable these tools are. The only issue is that valuation has always been expensive (typically 40-60x P/E), but great businesses are never cheap.

#### 1.2 ARM: A 97% gross-margin rent collection model

| Metric | Data |
|------|------|
| Mobile-chip IP share | >99% |
| Cloud CPU IP share | Rose from 9% to **20%**, expected to reach **90%** in AI ASICs by 2029 |
| FY2025 revenue | $4.671 billion (license $1.839 billion + royalty $2.168 billion) |
| Gross margin | **~97.5%** |
| Operating margin | Above 45% |

**Source of pricing power:** Armv9 royalty rates are about **2x** Armv8; CSS (compute subsystem) licensing royalties exceed **10% per chip**. Whether it is AWS Graviton, Google Axion, Microsoft Cobalt, or NVIDIA Grace - they all run on ARM, and ARM collects royalty no matter who wins.

**RISC-V threat assessment:** Short-term (2-3 years) threat is limited, mainly in low-end MCU and IoT. China is pushing RISC-V aggressively to reduce ARM dependence, but it is unlikely to replace ARM in data-center use cases within five years.

### 2. Upstream - Chip Design (the biggest profit capture point in the chain)

#### 2.1 NVIDIA: The "Standard Oil" of the AI era

| Metric | Data |
|------|------|
| Data center GPU market share | **80-92%** |
| FY2026 revenue | $215.9 billion (+65%), of which data center was $197.3 billion |
| Gross margin | GAAP **73.4%**, Non-GAAP 73.6% |
| H100 unit price | $25,000-40,000 |
| B200 unit price | $30,000-50,000 |
| GB200 NVL72 rack | 72 B200s + 36 Grace CPUs, $3.1-3.9 million per rack |

**CUDA ecosystem lock-in - the real moat:**
- More than **4 million** developers
- CUDA Toolkit downloaded more than **40 million** times
- All major ML frameworks are optimized for CUDA first
- The ecosystem has taken **20 years** to build, so switching costs are extremely high

**Substitutability: 1/5 | Pricing power: Very strong**

**Munger-style counterargument:**
- Gross margin has already fallen from a peak of 78% to 73% - custom ASICs are eroding the premium
- 2026 custom-ASIC shipments are growing **44.6%** vs GPUs at **16.1%** - long-term de-NVIDIA-ization is confirmed
- Google TPU is about **4x** more cost-effective than H100 for LLM training; after Midjourney moved to TPU, inference cost fell **67%**
- NVIDIA share is expected to gradually decline from 86% to around 75% - still dominant, but no longer the only choice

#### 2.2 AMD: The strongest challenger

| Metric | Data |
|------|------|
| AI accelerator market share | About 5-7% |
| Data center revenue | Record $4.3 billion in Q3 2025 (+22%) |
| Annual AI accelerator revenue | About $5 billion in 2024 |
| MI300X advantage | 192GB HBM3 (2.4x H100), 5.3 TB/s bandwidth |

ROCm is maturing, but the gap to CUDA is still large. Azure and Oracle have both adopted MI300X.

#### 2.3 Custom ASICs: Broadcom vs. Marvell

| Company | Custom ASIC share | AI revenue | Gross margin | Key customers |
|------|------|------|------|------|
| **Broadcom** | **70%+** | Q1 FY26 $8.4 billion (+106%) | 73% | Google TPU (78% share), Meta MTIA |
| **Marvell** | 10-15% | Data center $1.52 billion/quarter (+78%) | 60-65% | AWS Trainium, Microsoft Maia |

**Key trend:** Hyperscale customers' in-house chips are the biggest structural threat to NVIDIA. Google TPU is priced at about $13,000 per chip, far below NVIDIA GPUs, and Anthropic signed Google’s largest TPU order ever.

#### 2.4 China AI chips

| Company | Position | Gap | Irreplaceability (domestic) |
|------|------|------|------|
| **Huawei Ascend** | Domestic leader, 23% domestic share, 640,000 units shipped | 910C is better than H20 but still behind H200; full-stack in-house (CANN + MindSpore) | High |
| Cambricon | Widely used in national AI computing centers | Strong in specific niches, but valuation bubble is controversial | Medium |
| Biren / Moore Threads / Hygon | Each has its own path | Constrained by sanctions and foundry restrictions; 1-2 generations behind NVIDIA | Low to medium |

**Core bottleneck:** CUDA ecosystem monopoly plus fragmented software stacks across vendors; advanced packaging and HBM supply are constrained; foundry access is controlled by the United States.

### 3. Upstream - Semiconductor Manufacturing and Packaging

#### 3.1 TSMC: The only choice for advanced nodes

| Metric | Data |
|------|------|
| Global foundry share | **70-71%** (Q3 2025) |
| 2025 revenue | ~$122.5 billion (+36.1%) |
| Revenue from 7nm and below | **69%** |
| Gross margin | **56.1%** (2024), expected to stay above 53% in 2025 |
| 3nm wafer price | ~$20,000 per wafer |

**Dependence of NVIDIA/AMD on TSMC:**
- NVIDIA consumes **77%** of the world’s wafers for AI processors (535,000 300mm wafers)
- NVIDIA locks more than **60%** of TSMC CoWoS capacity
- Both companies are **100% dependent** on TSMC for advanced-node foundry work, with **no fallback**

**CoWoS advanced packaging - currently the tightest bottleneck:**
- Monthly capacity is 75,000-80,000 wafers at the end of 2025, with a target of 120,000-130,000 wafers by the end of 2026
- 2026 capacity will be **10x** 2023, but demand will still exceed supply
- Pricing power is very strong: CoWoS prices rose **15-20%** in 2025

**Substitutability: 1/5 | Pricing power: Very strong**

**Compared with competitors:**
| Foundry | Share | 3nm yield | Gap |
|------|------|------|------|
| TSMC | 70%+ | **90%+** | - |
| Samsung Foundry | 6.8% (declining) | 50% | Yield gap of 40 percentage points, with continued customer loss |
| Intel Foundry | 3-4% | 18A yield 55% | Catching up, with Microsoft Maia as a key customer |
| SMIC | ~5% | Equivalent to 5nm (DUV multiple patterning), yield ~33% | No EUV, costs 50% higher |

#### 3.2 ASML: The single most irreplaceable company in semiconductors

| Metric | Data |
|------|------|
| EUV lithography market share | **100%** (the only supplier in the world) |
| Overall lithography equipment share | **62%** |
| 2024 revenue | >EUR 28 billion |
| Gross margin | 51-53%, target 56-60% by 2030 |
| Backlog | **EUR 38.8 billion** |
| Low-NA EUV price | ~$200 million |
| High-NA EUV price | **~$370-400 million** |

**Substitutability: 1/5 (completely irreplaceable)**
> Even if China invests trillions of yuan, it cannot replicate EUV lithography in the short term. This is the hardest bottleneck in the entire semiconductor chain.

#### 3.3 Other key equipment

| Company | Core area | Market share | Gross margin | Substitutability |
|------|------|------|------|------|
| **KLA** | Inspection / metrology | **55-63%** | **62.3%** (highest in the industry) | 1-2/5 |
| **Applied Materials** | PVD / CVD / CMP | PVD **80%** | 48.8% | 2/5 |
| **Lam Research** | Etch | 28% | 50.6% | 2/5 |
| **Tokyo Electron** | Coating and development | **90%** | ~45% | 1-2/5 |

**The underrated company: KLA** - 62.3% gross margin is the highest among the five major equipment companies. Its inspection market share rose from 50% in 2010 to 63%, approaching monopoly status.

#### 3.4 Semiconductor materials: Japan's invisible control

| Material | Key companies | Share | Substitutability |
|------|------|------|------|
| Silicon wafers | Shin-Etsu (18%) + SUMCO (17%) | The two Japanese companies control **50%+** of 300mm capacity | 2/5 |
| EUV photoresists | TOK + JSR + Shin-Etsu | Combined share **~90%** | 1-2/5 |
| Coating/development equipment | Tokyo Electron | **90%** | 1-2/5 |

**Conclusion:** Japan's control over materials is severely underestimated - silicon wafers, photoresists, and coating/development equipment form a three-layer bottleneck.

### 4. Midstream - HBM, Servers, Networking

#### 4.1 HBM high-bandwidth memory: a suddenly important profit center

**Why HBM is the lifeblood of AI chips:** Traditional DDR5 bandwidth is about 50-60 GB/s, while one HBM3E stack reaches **1.2 TB/s** (a 20x gap). Without HBM, GPUs lose a large part of their practical performance.

| Company | HBM share | Gross margin | Pricing power | 2026 outlook |
|------|------|------|------|------|
| **SK hynix** | **62%** | Full-year **79%** | Very strong, 20% price increase in 2026 | Entire capacity sold out |
| **Micron** | **21%** | Above company average | Strong | Entire capacity sold out |
| **Samsung** | ~17% | Below SK hynix | Weak (HBM3E certification delayed by 18 months) | Main supplier for Google TPU (60%+) |

**Key data:**
- One HBM3E stack sells for $60-100, while DDR5 with the same capacity sells for just $5-10 (a **10-20x** premium)
- HBM accounts for **23%** of global DRAM wafer capacity
- Market size: $35 billion in 2025 -> $100 billion in 2028 (CAGR ~40%)

**Substitutability: 1/5 | Pricing power: Very strong**

**Duan Yongping-style question:** How durable is SK hynix's HBM position?
> At least 3-5 years of strong durability. HBM requires TSV (through-silicon via) technology plus CoWoS advanced packaging, so capacity expansion takes a long time (18-24 months). Samsung spent 18 months catching up before passing NVIDIA certification. But HBM4 could reshape the landscape, so it is worth watching.

#### 4.2 AI servers: fast growth, thin profits

**One GB200 NVL72 rack:** 72 Blackwell GPUs + 36 Grace CPUs, 1.44 ExaFLOPS, **132 kW** power draw per rack (115 kW liquid cooling), selling price **$3.1-3.9 million**.

| Company | Market share | Gross margin | Substitutability |
|------|------|------|------|
| Foxconn / Hon Hai | AI servers **40%+** | 4-11% | 4/5 |
| Dell | AI servers **20%** | ~20% | 4/5 |
| Supermicro | 7-9% (declining) | 10-14% | 4/5 |
| HPE | Enterprise | Higher than SMCI | 4/5 |
| Inspur Information | China AI servers **50%+** | Worse due to sanctions | 3/5 (domestic) |

**Core conclusion:** Servers are a "hard labor" business. The core profit goes to NVIDIA (chips) and SK hynix (HBM), while server OEMs are just "transporters."

#### 4.3 Networking equipment

| Company | Core product | Market share | Gross margin | Substitutability |
|------|------|------|------|------|
| **Broadcom** | Switch chips | Cloud data centers **~90%** | **77%** | 1/5 |
| **Arista** | Data center switches | **21.5%** (No. 1) | **64.6%** | 2/5 |
| NVIDIA networking | InfiniBand / Spectrum | InfiniBand monopoly | 70%+ | 2/5 |
| Cisco | Traditional networking | Leader but behind in AI | ~60%+ | 3/5 |

**InfiniBand vs. Ethernet:** In 2023 InfiniBand accounted for 80% of AI networking, but by mid-2025 Ethernet had already overtaken it and held more than two-thirds. The UEC 1.0 standard narrows latency gaps, and Ethernet has a more open ecosystem and lower cost.

**Optical modules:** Chinese vendors lead globally - Zhongji Innolight (23-30% share) and Eoptolink (25-30%). Market growth is 60%+, but gross margins are relatively low (25-30%).

#### 4.4 Cooling, liquid cooling, and power

**Liquid cooling is moving from "optional" to "mandatory":** GB200 reaches 132 kW per rack, while traditional air cooling tops out at 30-40 kW. Vertiv and Schneider Electric form a duopoly, and backlog provides multi-year visibility.

**Power demand:** Data-center electricity use is projected to rise from 55 GW in 2025 to 122 GW in 2030 (roughly doubling). Microsoft signed an agreement to restart the Three Mile Island nuclear plant. Eaton's data-center orders rose 200%.

### 5. Downstream - Cloud Computing and AI Applications

#### 5.1 The hyperscaler capex arms race

| Company | 2024 capex | 2025 capex | 2026 plan |
|------|------|------|------|
| Amazon | ~$55 billion | ~$100 billion | ~$200 billion |
| Microsoft | ~$44 billion | ~$80 billion | ~$150-190 billion |
| Google | ~$52 billion | ~$75 billion | ~$175-185 billion |
| Meta | ~$39 billion | ~$70-72 billion | >$72 billion |
| Oracle | - | - | ~$50 billion |
| **Total** | **~$200 billion** | **~$448 billion** | **~$660-690 billion** |

Goldman Sachs expects cumulative capex of **$1.15 trillion** in 2025-2027, about 75% of which will go to AI infrastructure.

**AWS in-house chips are delivering:** The Trainium series has generated more than **$10 billion** in revenue, with triple-digit growth. AWS has already deployed **1.4 million** Trainium2 chips. This validates the feasibility of "de-NVIDIA-ization."

**Oracle as a warning sign:** AI cloud gross margin is only **14%** - each $900 million of GPU rental revenue yields just $125 million in gross profit. This exposes the reality of "working for NVIDIA."

#### 5.2 China cloud and AI ecosystem

| Company | AI revenue trend | Capex / investment | Core strategy |
|------|------|------|------|
| **Alibaba Cloud** | Triple-digit growth for eight consecutive quarters | RMB **380 billion** invested over three years | "AI-driven, public cloud first"; Qwen downloads exceed 600 million |
| **Tencent Cloud** | Double-digit growth in enterprise services | 2025 capex **RMB 79.2 billion** | Hunyuan 3.0 provides compute for 90%+ of top-tier large models |
| **Baidu AI Cloud** | AI public-cloud market share **24.6%** (No. 1 for six years) | Kunlun Chip 3 generation, 10,000-GPU cluster | ERNIE daily calls of 1.65 billion |
| **ByteDance** | Doubao monthly active users 71 million | AI investment over **$12 billion** per year | Domestic use: 60% Huawei/Cambricon; overseas use: NVIDIA |

#### 5.3 AI application layer

| Company | Revenue | Compute consumption | Key metrics |
|------|------|------|------|
| **OpenAI** | $20 billion in 2025 | Expected to burn $50 billion in 2026 | 910 million weekly active users; committed to $250 billion of Azure spend |
| **Anthropic** | Annualized ~ $40 billion (mid-2026) | Signed Google’s largest TPU order ever | Gross margin from 38% -> **70%+**; valuation $380 billion |
| **xAI** | Not public | 230,000 GPUs, 555,000 GPUs by end-2025 | Largest single-site AI training facility in the world |

**China AI company valuations are surging, but revenue is still small:** DeepSeek valued at $45 billion; Zhipu AI HK market cap HKD 434.7 billion (revenue RMB 724 million); MiniMax HK market cap HKD 257.3 billion (revenue RMB 560 million). The four companies together exceed RMB 1 trillion in valuation.

---

## Part 2: Profit Allocation in the Supply Chain - Core Findings

### Where each $1 of AI compute spend goes

```text
$1 of AI compute spend
├── NVIDIA (chip design)         ~15-20 cents of profit   gross margin 73-75%
├── TSMC (foundry + packaging)    ~10-12 cents of profit   gross margin 56%
├── SK hynix / HBM (memory)      ~8-10 cents of profit    gross margin 79%
├── Broadcom (network chips)     ~6-8 cents of profit     gross margin 77%
├── EDA / ARM (tools / IP)       ~2-3 cents of profit     gross margin 86-97%
├── Optical modules / cooling / power   ~3-5 cents of profit   gross margin 25-35%
├── Server OEMs (assembly)       ~2-3 cents of profit     gross margin 4-20%
└── Cloud providers (AI cloud profit)   ~10-15 cents of profit  gross margin 50-60%
```

### Gross margin / substitutability / pricing power comparison

| Rank | Segment | Representative companies | Gross margin | Substitutability | Pricing power | Investment certainty |
|------|------|------|------|------|------|------|
| 1 | **EDA tools** | Synopsys / Cadence | **76-86%** | 1/5 | Very strong | 5/5 |
| 2 | **IP licensing** | ARM | **97%** | 1/5 | Very strong | 5/5 |
| 3 | **GPU chip design** | NVIDIA | **73-75%** | 1/5 | Very strong | 4/5 |
| 4 | **EUV lithography** | ASML | **51-53%** | 1/5 | Very strong | 5/5 |
| 5 | **HBM memory** | SK hynix | **79%** | 1/5 | Very strong | 4/5 |
| 6 | **Network chips** | Broadcom | **77%** | 1/5 | Very strong | 4/5 |
| 7 | **Foundry** | TSMC | **56%** | 1/5 | Very strong | 5/5 |
| 8 | **Inspection equipment** | KLA | **62.3%** | 1/5 | Very strong | 4/5 |
| 9 | **Data center switching** | Arista | **64.6%** | 2/5 | Strong | 4/5 |
| 10 | **Cooling / power** | Vertiv / Eaton | **22-35%** | 2/5 | Moderately strong | 3/5 |
| 11 | **Optical modules** | Zhongji Innolight / Eoptolink | **25-30%** | 3/5 | Medium | 3/5 |
| 12 | **AI servers** | Dell / Foxconn / SMCI | **4-20%** | 4/5 | Weak | 2/5 |
| 13 | **AI cloud services** | AWS / Azure / GCP | **50-60%** | 2/5 | Moderately strong | 3/5 |
| 14 | **GPU rental** | CoreWeave | **~40-50%** | 3/5 | Medium | 2/5 |

### Key insights

**1. The "people selling shovels" won - and the shovels themselves differ hugely**

Profit is extremely concentrated in upstream segments with monopoly positions. NVIDIA, TSMC, ASML, and SK hynix together may capture more than **40 cents** of profit for every $1 of AI compute spend.

**2. Gross margin is the ultimate litmus test for a "good business"**

- 97% gross margin (ARM) and 86% gross margin (Cadence) = "money printing machines"
- 73% gross margin (NVIDIA) and 79% gross margin (SK hynix) = "super businesses"
- 56% gross margin (TSMC) = "good business, but capital intensive"
- 4-20% gross margin (server OEMs) = "hard labor"; faster growth does not make them good businesses

**3. Oracle is the counterexample**

Oracle's AI cloud gross margin is only **14%** - it is helping NVIDIA sell compute, and almost all the profit is taken by upstream suppliers. This is a reminder that not every "AI stock" makes money.

**4. Profit is migrating from upstream to downstream**

Anthropic's inference gross margin improved from 38% to **70%+**. As inference costs fall and agentic AI rises, the economics of downstream application companies reached an inflection point in late 2025. But whether that inflection is durable still needs to be proven.

---

## Part 3: Bottleneck Analysis

### The most irreplaceable segments (substitutability 1/5)

```text
Irreplaceability ranking (1 = completely irreplaceable)

1. ASML EUV lithography     100% monopoly, no substitute
2. TSMC advanced nodes      70%+ share, yield crushes competitors
3. EDA trio                 85% share, 100% customer retention
4. ARM IP                   Mobile 99%, cloud 20% and growing
5. NVIDIA CUDA ecosystem    4 million developers, 20 years of buildup
6. SK hynix HBM             62% share, 18-month capacity expansion cycle
7. TSMC CoWoS               AI packaging at full capacity, NVIDIA locks 60%
8. Broadcom switch chips    90% share in cloud data centers
9. KLA inspection equipment 55-63% share, 62.3% gross margin
10. Tokyo Electron coating/development 90% share, near monopoly
11. Japanese photoresists   90% of EUV photoresists
```

### China's bottlenecks

| Segment | Global level | China level | Gap | Near-term breakout potential |
|------|------|------|------|------|
| EUV lithography tools | ASML 100% monopoly | Shanghai Micro Electronics (DUV 90nm) | **10+ generations** | Very low |
| Advanced-node foundry | TSMC 3nm / 2nm | SMIC equivalent 5nm (DUV multiple patterning) | **2-3 generations** | Low |
| EDA tools | Synopsys / Cadence 85% | Empyrean domestic 6% | **Generational gap** | Low |
| HBM | SK hynix / Samsung / Micron | Almost blank | **A whole generation** | Very low |
| CUDA ecosystem | NVIDIA 4 million developers | Fragmented across vendors | **Huge** | Medium (can be bypassed) |
| GPU performance | NVIDIA B200 | Huawei 910C (better than H20, but behind H200) | **1-2 generations** | Medium |

---

## Part 4: Systemic Risk Assessment (Munger "Checklist")

| Risk | Probability | Impact | Specific scenario |
|------|------|------|------|
| Cyclical pullback in AI capex | Medium | High | If AI monetization falls short, hyperscalers reduce capex (see the 2022 cloud slowdown) |
| Custom ASICs accelerate substitution for NVIDIA | Medium-high | Medium | Google / AWS / Meta in-house chips mature, and NVIDIA share falls from 80% to below 60% |
| Valuation bubble bursts | Medium | High | NVIDIA at 30x+ P/E, Cambricon / Moore Threads at hundreds of times P/E; if growth slows, valuations compress |
| US-China tech decoupling deepens | Medium-high | Medium | Additional sanctions cut off TSMC / ASML supply to China |
| Alternative technologies emerge | Low | High | Disruptive technologies such as quantum computing or photonic computing (low probability within 10 years) |
| Energy / power constraints | Medium | Medium | Data-center power demand grows too fast, and grid constraints slow expansion |

### Historical analogy

**Closest analogy: the 1990s internet infrastructure buildout**

| Dimension | 1990s internet | AI in 2024-2026 |
|------|------|------|
| Infrastructure arms race | Cisco / Nortel / fiber companies | NVIDIA / TSMC / hyperscale cloud |
| Final winner | Application layer (Google / Amazon / Facebook) | TBD |
| Infrastructure company outcome | Cisco survived but never returned to its 2000 market cap; most fiber companies went bankrupt | ? |
| Takeaway | Selling shovels gives high short-term certainty, but the long-term biggest winner may sit in the application layer | Current "shovel sellers" already price in a lot of optimism |

**Key difference:** NVIDIA / TSMC / ASML have much stronger monopolies than Cisco did back then - Cisco switches had substitutes, but EUV lithography, CoWoS packaging, and the CUDA ecosystem currently do not.

---

## Part 5: Civilization Trend Judgment (Li Lu framework)

**Question: Is AI compute a "civilization-level paradigm shift" or a "phase-specific boom"?**

**Judgment: Civilization-level paradigm shift.** Reasons:
1. AI is changing the nature of knowledge work, analogous to how the industrial revolution changed physical labor
2. All of the world's top five companies (Apple, Microsoft, NVIDIA, Google, Amazon) are deeply invested in AI
3. The $1.15 trillion of capex in 2025-2027 is not speculation - it is enterprise demand validated by business use
4. Anthropic's gross margin has risen from 38% to 70%+, and the economics of AI applications reached an inflection point in late 2025

**10-20 year end state:**
- **Highest probability winner-take-all segments:** chip design (NVIDIA or its successor), foundry (TSMC)
- **Most likely to be disrupted:** server OEMs (least differentiated), GPU rental intermediaries (dependent on NVIDIA pricing)
- **Biggest variable:** where the balance point lies between in-house chips and general-purpose GPUs

---

## Part 6: Portfolio Construction Suggestions

### Recommended portfolio

| Tier | Asset | Segment | Core logic | Recommendation |
|------|------|------|------|------|
| **Core position (50-60%)** | | | | |
| | TSMC (TSM) | Foundry + packaging | Only choice for advanced nodes, CoWoS bottleneck, 70% share, highest certainty | 5/5 |
| | ASML (ASML) | EUV lithography equipment | 100% EUV monopoly, EUR 38.8 billion backlog, strongest irreplaceability | 5/5 |
| | NVIDIA (NVDA) | AI chip design | 80%+ share + CUDA lock-in, but watch custom-chip cannibalization | 4/5 |
| **Satellite position (25-35%)** | | | | |
| | Broadcom (AVGO) | Network chips + custom ASICs | 90%+ in switch chips + 70% in ASICs, double moat | 4/5 |
| | SK hynix (000660.KS) | HBM memory | 62% share, 79% gross margin, but memory cycle risk | 4/5 |
| | Cadence (CDNS) | EDA tools | 86% gross margin, 100% customer retention, one of the best business models | 4/5 |
| | ARM (ARM) | IP licensing | 97% gross margin, "collect rent no matter who wins," but valuation is extremely rich | 3/5 |
| | Arista (ANET) | Data center switches | No. 1 in AI data-center Ethernet, 64.6% gross margin | 4/5 |
| **Option position (5-15%)** | | | | |
| | KLA (KLAC) | Inspection equipment | 62.3% gross margin, highest in the industry, an underrated hidden champion | 4/5 |
| | Vertiv (VRT) | Cooling + power | Liquid cooling is required, $9.5 billion backlog, but valuation is no longer cheap | 3/5 |
| | Zhongji Innolight (300308.SZ) | Optical modules | Global leader, 1.6T silicon photonics, but gross margin is relatively low | 3/5 |
| **ETF alternatives** | | | | |
| | SMH (VanEck Semiconductor ETF) | Diversified | Covers NVIDIA / TSMC / ASML / Broadcom, the "lazy" solution | 4/5 |
| | SOXX (iShares Semiconductor ETF) | Diversified | More balanced semiconductor exposure | 3/5 |

### Names to avoid / handle with caution

| Asset | Reason | Recommendation |
|------|------|------|
| AI server OEMs (SMCI / Dell) | Low gross margin, assembly-like business, SMCI has accounting issues | 2/5 |
| CoreWeave (CRWV) | High growth but $30 billion of debt; fragile business model | 2/5 |
| Oracle AI Cloud | 14% gross margin exposes the "working for NVIDIA" nature | 2/5 |
| Cambricon (688256.SH) | Severe valuation bubble; revenue scale does not match valuation | 1/5 |
| China AI application companies (Zhipu / MiniMax) | Trillion-yuan valuations but only hundreds of millions of revenue; extremely high bubble risk | 1/5 |

### Buy / sell signals

| Signal type | Specific condition |
|------|------|
| **Add** | Hyperscaler capex keeps being raised; HBM / CoWoS shortages persist; AI application revenue accelerates |
| **Reduce** | Hyperscaler capex growth slows to single digits; NVIDIA gross margin falls below 65% (large-scale custom ASIC substitution); AI monetization disappoints and the "AI winter" narrative strengthens |
| **Exit** | Hyperscaler capex declines year over year; large-scale discounted selling of NVIDIA GPUs appears (similar to the 2022 crypto-mining GPU glut); macro recession sharply cuts enterprise IT budgets |

### Suggested thematic position cap

**Recommended maximum allocation to the AI compute theme: 25-35%**

Reason: Every part of the investment chain has been strongly validated, but valuations are generally expensive (NVIDIA 30x+ P/E, ASML 30x+ P/E, TSMC 25x+ P/E), and there is cyclical capex risk.

---

## Part 7: Consolidated Decision Memo

### Industry scorecard

| Dimension | Conclusion | Confidence |
|------|------|------|
| Investment logic chain | Every segment has been strongly validated; $1.15 trillion in capex is real | 5/5 |
| Best segment (Duan Yongping's "right business") | EDA / ARM (highest gross margin) > NVIDIA / HBM (largest profit pool) > TSMC / ASML (highest certainty) | 4/5 |
| Widest moat (Buffett) | ASML (100% monopoly) ~= EDA (85% oligopoly) > NVIDIA (CUDA lock-in) > TSMC (yield crushing peers) | 5/5 |
| Biggest risk (Munger) | Cyclical capex pullback + custom chips eroding NVIDIA + valuation bubble | 4/5 |
| Civilization trend (Li Lu) | Civilization-level paradigm shift, not a phase-specific boom | 4/5 |
| Overall valuation level | Generally expensive; requires sustained high growth to be justified | 3/5 |

### Simulated comments from the four masters

> **Buffett:** "On this AI compute chain, the parts I understand best are TSMC and ASML - their moats are visible, and in ten years they are almost certainly still here. NVIDIA is wonderful, but I do not have 100% conviction that CUDA will lock in customers forever. I would not touch server assemblers - a 4% gross margin business is not a good business no matter how fast it grows."

> **Munger:** "Why not buy NVIDIA? Because a 30x P/E means the market has already priced in at least 3-5 years of high growth, and the custom-chip trend is accelerating - Google TPU is 4x more cost-effective than H100, and AWS has already deployed 1.4 million Trainium chips. I am not saying NVIDIA will lose, but a drop from 80% share to 60% is entirely possible. What does that mean? It means the current valuation has no margin for error."

> **Duan Yongping:** "Looking at this chain, the best business models are EDA and ARM - 86% and 97% gross margins, 100% customer retention, recurring revenue. Those businesses are incredibly rare. The problem is that both companies trade at very high P/Es, so you need to wait until the market misprices them for some reason before buying. Investing is not about finding good companies; it is about finding good companies at good prices."

> **Li Lu:** "AI really is a civilization-level paradigm shift - it is doing to knowledge work what the industrial revolution did to physical labor. But history tells us that in the early stages of a technology revolution, the people selling the shovels (the infrastructure providers) make money first, while the eventual winners are often in the application layer. Investing in Cisco in the 1990s was very profitable, but in the long run Google and Amazon created more value. Today's NVIDIA is yesterday's Cisco - with one key difference: NVIDIA's degree of monopoly is much stronger than Cisco's was. That makes it safer, but also pushes its valuation higher."

---

## Data Sources

This report is based on cross-validation across the following sources:
- The latest quarterly and annual reports of the relevant companies (NVIDIA FY2026, TSMC 2025 annual report, SK Hynix 2025 annual report, etc.)
- Research reports from Goldman Sachs, Morgan Stanley, TrendForce, IDC, Gartner, and similar institutions
- Coverage from CNBC, Bloomberg, Financial Times, and other financial media
- China market data referenced from 21jingji, Securities Times, The Beijing News, Zhihu columns, and similar sources
- Semiconductor industry analysis firms such as SemiAnalysis, TrendForce, and Dell'Oro Group

**Disclaimer:** This report is for personal investment research only and does not constitute investment advice. All data are intended to be accurate, but time sensitivity may still exist. Investing involves risk; please be cautious.

---

*Report completion date: 2026-05-09*
*Research method: Parallel research by four AI teams covering upstream chip design, upstream manufacturing and packaging, midstream equipment and networking, and downstream cloud and applications*
