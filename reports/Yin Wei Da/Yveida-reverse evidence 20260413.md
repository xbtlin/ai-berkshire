# The NVDA's back-of-the-art evidence research

** Date of report: 13 April 2026**
** Purpose of the study: to supplement the evidence of the negative aspects of the study and to re-evaluate key risks**
** Methodology: Targeted Access to First-hand Sources (Official Corporate Bulletin, SEC Document, Bloomberg/Reuters/SemiAnalysis/CNBC, Official Blog)**
** Key constraints: all data with URL+ dates; no one-hand-sourced explicit "data missing" can be found; fabrication is prohibited**

> ** Statement**: This report is deliberately focused on "anti-evidence" to balance the possible consensus bias in the report.

---

# 1. Re-evaluation of the CUDA mound in the era of the AI code tool

# 1.1 Claude Code "30 Minutes Porting CUDA to ROCm"

** Fact**: In January 2026, developers johnytshi publicly demonstrated that a CUDA backend was transplanted to AMD ROCm in about 30 minutes. The process was not dependent on the middle layer such as HIPCFY, and it was close to the original. The case generated extensive discussion on X, HardForum, wccftech, which was partly commented on as the "end sign of the CUDA Protector River".
- Source: [Techstrong.ai 2026-01] (Techstrange.ai 2026-01]https://techstrong.ai/features/claude-code-ports-nvidia-cuda-to-amd-rocm-in-30-minutes/)、[wccftech 2026-01](https://wccftech.com/the-claude-code-has-managed-to-port-nvidia-cuda-backend-to-rocm-in-just-30-minutes/)、[GitHub gist johnnytshi](https://gist.github.com/johnnytshi/33d3cec152faf46ff36e91cbf36fd28a)

** Reverse/conditional**: Commentators generally point out that the case is simple kernel; complex coding libraries and cache hierarchy, warp scheming (a) agent is still not competent. The difference is mainly in the Data layout floor. This is evidence of "draw down the threshold" rather than "disappearing the moat."

#1.2 ROCm 7 / HIP 7 and translation tool progress

- ROCm 7.0/HIP 7.0 was released in the second half of 2025, with the clear strategy of "tighter alignment with the CUDA semantic" and simplified cross-plant transplantation. Source: [Phoronix 2025] (Phoronix 2025)https://www.phoronix.com/news/AMD-ROCm-7.0-HIP-Plans), [AMD Official ROCm Blog] (@Amdam_Blog)https://rocm.blogs.amd.com/ecosystems-and-partners/transition-to-hip-7.0-blog/README.html)
- Academic research CASS models have been translated to 95% accuracy at the source level, 37.5% in the compilation layer, exceeding the traditional HIPIFY. Source: [OpenReview CASS thesis] (https://openreview.net/pdf/8c2f640c9dbbefef7c1bd23020ae87e08c0e8648.pdf)
- Independent evaluation, April 2026: CUDA leads about 10-30% of ROCm in a calculated, intensive workload, with a significant narrowing of the gap (vs 2-3 times in 2023). Source: [Thunder Compute 2026-04] (Thunder Compute 2026-04)https://www.thundercompute.com/blog/rocm-vs-cuda-gpu-computing)

# 1.3 Triton compiler and PyTorch multiple backends

- Triton 3.6.0 released at 2026-01-20; Third Triton Developer Conference 2025-10-21 held at the Microsoft Silicon Valley Garden. AMD HIP AOT was introduced in 3.5.0. Compiled. Source: [GitHub triton-lang] (https://github.com/triton-lang/triton)、[NVIDIA GTC 2025 Triton Blackwell Session](https://www.nvidia.com/en-us/on-demand/session/gtc25-s72876/)
- TorchInductor became the mainstream compiler; vLLM has produced an environment using torch.compile. Source: [vLM Blog 2025-08] (vLLM Blog 2025-08]https://blog.vllm.ai/2025/08/20/torch-compile.html)
- TPU does not go to Triton/Inductor's, relying on PyTorch/XLA. Status 2025: "Who serves the Industor-Triton pipe, wins." Source: [State of PyTorch Hardware 2025]https://tunguz.github.io/PyTorch_Hardware_2025/)

#1.4 Contrary argument: 100 kCh of the moat is still in

- NCCL 2.29, under 100k+GPU training scene, AllGather/RedueScatter became a bottleneck; Meta expanded with NCCLX, fault detection + recovery takes 3 minutes. Source: [arXiv 2510.20171 Corporate for 100k+ GPUs].https://arxiv.org/html/2510.20171v1)、[Mycroft SOSP25](https://geraldleizhang.com/publications/Mycroft_SOSP25.pdf)
- This means that 100,000 card-level training missions remain highly dependent on CUDA/NVLink/InfiniBand ecology for better communication; the AI coding tool cannot be short-termly attacked by system level optimization.
- ** Not ** The case of a "non-CUDA" has been publicly attributed to the massive failure of the forward LLM training mission.

** Data confidence: high** (Claude Code event, Triton version, CASS papers; communication warehouse bottlenecks supported by academic papers)

** Ajudgmental update**: the CUDA layer mounds clearly experienced double erosion in 2026 of "AI Auxiliary Transplant Plus Open Source Editor"; but the system level (100,000 calories, HBM dispatch, NVLink Fabric) mounds have not yet been shaken.** The transplant threshold has been reduced from "a few months" to "one hour" of engineers, and requires a discount on the original report "CUDA flying wheel".**

---

#2. Clients as counter: hard data on the threat of self-research chips at four cloud plants

### 2.1 AWS Trainium2 + Anthropic "Project Rainier"

- 2025-11, AWS Officer Project Rainier online, deploying nearly 500,000 Trainium2s, which are used exclusively by Anthropic. Source: [AWS Official Bulletin 2025-11] (AWS Official Bulletin 2025-11)https://www.aboutamazon.com/news/aws/aws-project-rainier-ai-trainium-chips-compute-cluster)、[AWS Blogs 2025-11-03](https://aws.amazon.com/blogs/aws/aws-weekly-roundup-project-rainier-online-amazon-nova-amazon-bedrock-and-more-november-3-2025/)
- AWS CEO Matt Garman to CNBC: Anthropic will deploy more than 1 million on Trainium2 by the end of the year. Arithmetic is five times as much as Anthropic's predecessor.
2026-03 TechCrunch reported that Trainium won Anthropic and started to be used by OpenAI, Apple. Source: [TechCrunch 2026-03-22] (TechCrunch 2026-03-22)]https://techcrunch.com/2026/03/22/an-exclusive-tour-of-amazons-trainium-lab-the-chip-thats-won-over-anthropic-openai-even-apple/)

### 2.2 Google TPU Trillium/Ironwood + Anthropic

- 2025-10-23, Anthropic announced the extension of TPU use to "over 1GW capacity to be activated in 2026". Source: [Anthropic Official 2025-10-23] (https://www.anthropic.com/news/expanding-our-use-of-google-cloud-tpus-and-services)、[Google Cloud Press 2025-10-23](https://www.googlecloudpresscorner.com/2025-10-23-Anthropic-to-Expand-Use-of-Google-Cloud-TPUs-and-Services)
2026-04, Anthropic signed a new agreement with Google+Broadcom,** phase I consists of 400,000 TUv7 Ironwoods, approximately $10 billion in finished cabinets, sold directly to Anthropic** by Broadcom; total size "More GW", 2027 overlined. Source: [Bloomberg 2026-04-06] (Bloomberg 2026-04-06]https://www.bloomberg.com/news/articles/2026-04-06/broadcom-confirms-deal-to-ship-google-tpu-chips-to-anthropic), [Anthropic Official] (@Amsym)https://www.anthropic.com/news/google-broadcom-partnership-compute)、[Futurum Group](https://futurumgroup.com/insights/anthropics-gigawatt-scale-tpu-deal-with-broadcom-creates-a-structural-advantage/)

### 2.3 Microsoft Maia 200

- 2026-01-26, Microsoft Officer Maia 200 deployed to the Iowa data centre, next station Phoeenix.** For the latest GPS-5.2 model for OpenAI,** and for M365 Copilot. Source: [Microsoft Blog 2026-01-26] (see table 1 below).https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/)、[Microsoft EMEA News](https://news.microsoft.com/source/emea/features/maia-200-microsoft-ai-accelerator-azure-2/)
- Note: Maia 200 planned to produce in 2025 was delayed by about six months (the increase in OpenAI requirements has led to a simulation of instability). Source: [DDC report] (DCD report)https://www.datacenterdynamics.com/en/news/microsoft-delays-production-of-maia-100-ai-chip-to-2026-report/)
- ** Positioning is clearly a reasoning chip**, non-training replacement.

#2.4 Meta MTIA Road Map

- 2026-03-11 Meta announced the four generation plan MTIA 300/400/500. MTIA 300 was produced (for sequencing/recommend training); 450/500 main GenAI reasoning, 2027. Hundreds of thousands of MTIA have been deployed in the production environment. Source: [Meta Official 2026-03]https://about.fb.com/news/2026/03/expanding-metas-custom-silicon-to-power-our-ai-workloads/)、[Meta AI Blog](https://ai.meta.com/blog/meta-mtia-scale-ai-chips-for-billions/)
- Rhythm: every six months (typically 1-2 years of industry).

# # 2.5 Broadcom customizes the AI chip business

- SY2025 AI revenue is approximately $19.9 billion (+63% YoY, NY24 billion). Q1 EY26 guides AI revenue is about $19.1 billion (+28% YoY). Source: [CNBC 2025-12-11] (https://www.cnbc.com/2025/12/11/broadcom-avgo-q4-earnings-2025.html)
- ** Client list: Google TPU, Meta MTIA, ByteDance self-research, OpenAI (10GW agreement, potentially $200 billion in incremental revenue), Anthropic (Ironwood distribution).** Source: [Seeking Alpha] (Seking Alpha)https://seekingalpha.com/article/4854249-broadcom-121-billion-revenue-boost-potential-from-openai-and-anthropic)、[FinancialContent 2026-04-08](https://markets.financialcontent.com/stocks/article/marketminute-2026-4-8-broadcoms-3nm-revolution-how-custom-silicon-for-meta-and-bytedance-fueled-a-historic-breakout)
- Signing with Alphabet about 2031.

#2.6 NVDA client concentration (late 10-Q)

- **Q3 SY2026, four major direct clients, account for 61% of income: Custamer A 22%, B 15%, C 13%, D 11%**, all under the Compute & Networking Division. Source: [NVDA 10-Q 2025-10-26] (see table 1 below).https://www.sec.gov/Archives/edgar/data/1045810/000104581025000230/nvda-20251026.htm)、[Motley Fool 2025-11-27](https://www.fool.com/investing/2025/11/27/blackwell-off-charts-nvidia-customer-concentration/)
- Q2 SY26: A 23%, B 16%, and four others 14/11%, 11%, 10%, respectively.
- The four "direct customers" are, to a large extent, OEM/ODM/distributors (e.g. Foxconn, Wistron, SuperMicro), but ** eventually concentrated heavily in AWS/Azure/GCP/Meta**.

** Data confidence: high** (all in company official bulletins, SEC documents, Bloomberg)

** The underlying report: the argument that the self-research chip short-term threat is overestimated requires re-evaluation.** The evidence for the scale deployment of the three clouds has changed from "Abjection" to "GW-level contract + SEC disclosure"** – especially the fact that 1 million Trainium 2 + 400,000 Ironwoods in Anthropic mean that NVDA has lost Anthony as a large, incremental customer. Broadcom AI's income corresponds directly to the ASIC's market transfer of substitute GPUs for two years.

---

#3. Training vs. Precision of market differentiation

# 3.1 The point of reasoning beyond training has arrived

- Deloitte 2026 predicts:** The reasoning will account for about 2/3 of the total AI capacity in 2026** (2023 to 1/3 to 2025 to 1/2). Source: [Deloitte TMT Predictions 2026] (see table 1 below).https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/compute-power-ai.html)
- MarketsandMarkets: AI reasoning market $202.5 billion $106.2 billion – $20.3 billion $25.5 billion, CAGR 19.2 per cent.
- Gartner: 55% AI-IAAS expenditure in 2026 was used for reasoning, 65% in 2029.
- Rationale optimization of the chip market by 2026 > $50 billion.
- Source: [CES 2026 Computerworld] (Cyber_Cyber_Cyber_Cyber_Cyber_Cyber_Cyber_Cyber_Cyber_Cyber_Cymology]https://www.computerworld.com/article/4114579/ces-2026-ai-compute-sees-a-shift-from-training-to-inference)、[SDxCentral 2026](https://www.sdxcentral.com/analysis/ai-inferencing-will-define-2026-and-the-markets-wide-open/)

#3.2 Real price of the reasoning replacement chip

- **Groq**: Llama 3.1 70B $0.64/milliontokens, >240 tokens/s.
- **Cerrebras**: Llama 3.1 70B $0.60/milliontokens, 450 tokens/s/user@16-bit.
- **DeepInfra**: Llama 3.1 8B $0.03-0.05 million tokens (price floor).
- Source: [GopenAI Token Arbitrage Benchmark 2025] (Gopénée d ' Auxiliarye)https://blog.gopenai.com/the-token-arbitrage-groq-vs-deepinfra-vs-cerebras-vs-fireworks-vs-hyperbolic-2025-benchmark-ccd3c2720cc8)、[IntuitionLabs Cerebras vs SambaNova vs Groq](https://intuitionlabs.ai/articles/cerebras-vs-sambanova-vs-groq-ai-chips)
- The market of reasoning has changed from "GPU Monopoly" to "As-Scenario": low delay <unk> Groq/Cerebras; mass <unk> DeepInfra; agent <unk> Fireworks.

#3.3 NVDA Logic Product Positioning

- Blackwell Ultra (B300/GB300) 2025 H2 out of goods; Rubin CPX optimized the reasoning 'separable architecture' in the second half of 2026.** NVDA has strategically confronted the reasoning market division**, but Maia 200/MTIA/Inferentia2/Trainium2/TPU + Groq/Cerrebras together squeezed the NVDA reasoning share from below.

** Data confidence: high**

** A review**: The basic report "Rational relay training, total increase" is right; but the implicit assumption that "NVDA is still the reasoning king" needs to be weakened.** The reasoning is that the market is open to battlefields rather than NVDA extension**.

---

# 4. ROI perjury risk for the AI CapEx cycle

# 4.1 The Four Cloud Plants 2026 CapEx (latest hand)

Company 2026 CapEx Guidance
|---|---|---|
<unk> Amazon<unk> $200 billion<unk> CNBC 2026-02-06<unk>
<unk> Alphabet<unk> to $185 billion
<unk> Meta <unk> $1150-1350 billion (including Ohio 1GW, Louisiana final 5GW)
<unk> Microsoft <unk> NY26 + about $12 billion (recent quarter $37.5 billion) <unk> Ibid. <unk>

- Four totals** $635-70 billion** (+67% ~ 74%, $2025 billion). About 75% (~$45 billion) goes to AI infrastructure.
- Source: [CNBC 2026-02-06] (https://www.cnbc.com/2026/02/06/google-microsoft-meta-amazon-ai-cash.html)、[Futurum AI Capex 2026](https://futurumgroup.com/insights/ai-capex-2026-the-690b-infrastructure-sprint/)
- ** Cash flow shock**: Barclays estimates Microsoft FY26 FCF-28%, 2027 rebound; Amazon FCF or passback.

# 4.2 OpenAI Financial Reality

- $20 billion in income from 2025 (as confirmed by the CFO); $202.4 billion from $20.23 billion from $20.2 billion from the Fund.
- Net loss of H1 of $2025 has reached $13.5 billion; cash consumption of $2026 is projected at $17-25 billion, possibly $57 billion, for 2027. Source: [Sacra OpenAI] (see table).https://sacra.com/c/openai/)、[The Deep Dive](https://thedeepdive.ca/openai-closes-record-122-billion-funding-round-at-852-billion-valuation/)
- 2026-03-31 OpenAI completed $122 billion in financing valued at $852 billion (SoftBank, a16z pilot; Amazon to $50 billion, NVIDIA $30 billion, SoftBank $30 billion). Source: [CNBC 2026-03-31] (CNBC 2026-03-31]https://www.cnbc.com/2026/03/31/openai-funding-round-ipo.html)
- ** Cash flow was only reversed in 2030**

# 4.3 Recycled transaction dispute

OpenAI has committed to pay Oracle for five years**$300 billion** of the calculated resources (in the case of the $500 billion Stargate project).
- NVIDIA agreed to invest up to $100 billion in OpenAI** (2025-09) in exchange for OpenAI ' s commitment to purchase millions of NVIDIA GPUs.
- Source: [CNBC 2025-10-15 treaty] (CNBC 2025-15)https://www.cnbc.com/2025/10/15/a-guide-to-1-trillion-worth-of-ai-deals-between-openai-nvidia.html)、[The Register 2025-11-04](https://www.theregister.com/2025/11/04/the_circular_economy_of_ai/)、[Bloomberg AI Circular Deals Graphics 2026](https://www.bloomberg.com/graphics/2026-ai-circular-deals/)
- Criticism: NVDA, OpenAI, Microsoft, Oracle, AMD, CoreWeave, xAI, swapping funds/calculus/clouds in closed circles, "NVDA is paying for its future income." Bloomberg specifically produces interactive maps.

# 4.4 Cisco analogue

- Cisco 2000-03 market value $500 billion plus (ex-soft was the largest global); stock prices fell from $80 to $9.50 (88%) and took 25 years and 8 months to return to their previous height. Source: [CNBC 2025-12-10] (see table 1 below).https://www.cnbc.com/2025/12/10/ciscos-stock-closes-at-record-for-first-time-since-dot-com-peak-2000.html)、[Harding Loevner Cisco vs NVDA](https://www.hardingloevner.com/insights/nvidia-and-the-cautionary-tale-of-cisco-systems/)
- Key differences: Cisco PE > 200, margins continued to contract at peaks; NVDA is currently PE ~ 36-45, margins is still at historical highs.** However, <unk> V/Sales is still close to the top level of Cisco (~24 vs 31)**.

##4.5 Client side (demand side verification)

- Anthropic ARR: $202.5-08 $5 billion <unk> $90 billion late 2025 <unk> $2026-03 **$30 billion ** (Yoy + 1400%) ** of which Claude Code single product contributed $2.5 billion +. Commercial clients > 300,000, > $100,000/year, seven times more. Source: [SaaaStr] (https://www.saastr.com/anthropic-just-hit-14-billion-in-arr-up-from-1-billion-just-14-months-ago/)、[The AI Corner](https://www.the-ai-corner.com/p/anthropic-30b-arr-passed-openai-revenue-2026)
- Google Gemini Q4 2025 MAU 750 million (Pichai Disclosure).
- ** Real pay side demand is actually breaking** — this is a lot of arguments to counter the "pure bubble" narrative.

** Data confidence: high**

** A review**: The base report lists AI CapEx cyclicality as "the greatest undervalued risk" -- a judgement that is reinforced**. A $70 billion per year of expenditure + revolving transactions + Microsoft FCF - 28% is co-exist, **2027 was a key observation window**. But the demand side (Anthropic $30 billion ARR) shows a difference from Cisco 2000: there is real payback today.

---

5. Depletion of the demand for GPU by the algorithmic efficiency revolution

# 5.1 DeepSeek incident

- DeepSeek V3 training: 2.7880 million H800 GPU hours, base model costs approximately $5.6 million; and after R1 training GPU costs approximately $294,000. Compare GPT-4 estimates >100 million, Gemini Ultra $191 million. Source: [Stratechery DeepSeek FAQ]https://stratechery.com/2025/deepseek-faq/)、[Interconnects](https://www.interconnects.ai/p/deepseek-v3-and-the-actual-cost-of)
- Baseline: R1 MMLU 90.8% vs GPT - 87.2%; AIME 2024 79.8% vs 9.3%.
- ** Important warning**: DeepSeek himself explicitly states in his paper that the cost is "free of advanced research, architecture/arithmetic/data-diversion experiments". Bernstein openly questions $5.6M credibility.

#5.2 NVDA share price response

- 2025-01-27 NVDA ** 17% single-day decline, market value ~ $589 billion** ** largest single-day market value loss in US-owned history** (formerly Meta $240 billion). Source: [Bloomberg 2025-01-27] (Bloomberg **1 July 2007)https://www.bloomberg.com/news/articles/2025-01-27/asml-sinks-as-china-ai-startup-triggers-panic-in-tech-stocks)、[Yahoo Finance](https://finance.yahoo.com/news/nvidia-stock-plummets-loses-record-589-billion-as-deepseek-prompts-questions-over-ai-spending-135105824.html)
- Analysts reacted to the split: Bernstein maintained the target price of $175; Raymond James considered the counter-acceleration of the urgency of hyperscaler.
- NVDA-11% for the full month of January.

# 5.3 The rebuttal of Huang In-hoon/Altman

- Wong In-hoon CES 2025:** "Al scaling"** - Proclaims that three layers of scaling (pre-training, post-training, test-time) require a great deal of money for each layer. Source: [TechCrunch]https://techcrunch.com/snippet/2982546/jensen-huang-says-that-practically-the-entire-world-got-ai-scaling-wrong/)、[CDOTrends](https://www.cdotrends.com/story/4376/test-time-scaling-new-frontier-ai)
- Altman publicly stated: "Everything starts with company" (NVIDIA cooperation announcement). Source: [NVIDIA Newroom 2025-09]https://nvidianews.nvidia.com/news/openai-and-nvidia-announce-strategic-partnership-to-deploy-10gw-of-nvidia-systems)
- **Jevins paradoxal support**: After DeepSeek, Anthropic ARR triples five months, hyperscaler 2026 CapEx + 67%, efficiency gains do bring more demand than less in market behaviour.

** Data confidence: high**

** A diagnostic update**: The DeepSeek event proved that the market was extremely sensitive to "arithmic efficiency" (single day - 17%); but the demand side of the 12 months that followed countered the Evans paradox.** The risk is not "arithmetic efficiency per se" but "re-rating"** - the underlying report should add "re-rating" as an independent risk category.

---

#6. Chinese market + geopolitics

# 6.1 H20 embargo and release

- 2025-04 The Trump government ordered the suspension of H20-to-China shipments; NVDA Q1 NY26 **$4.5 billion in stock and procurement obligations ** impairments and Q1 loss of $2.5 billion in delivery. The initial trump ban resulted in $5.5 billion worth of write-off. Source: [Manufacturing Dive Q1 SY26] (https://www.manufacturingdive.com/news/nvidia-q1-2026-earnings-export-controls-china-trump/749261/)、[RCR Wireless](https://www.rcrwireless.com/20250529/business/nvidia-q1-fy2026)
- 2025-07 Trump reversed and allowed H20 to resume delivery.
- B30A: The castration Blackwell singledie, about six times the power of H20, about half of B200, is stuck at the new Performance Density threshold of the Common Sector Department. The sale price may be twice as high as H20. Source: [Tom's Hardware]https://www.tomshardware.com/tech-industry/artificial-intelligence/nvidias-next-gen-ai-chip-could-double-the-price-of-h20-if-china-export-is-approved-chinese-firms-still-consider-nvidias-b30a-a-good-deal)、[IFP B30A Decision](https://ifp.org/the-b30a-decision/)

# 6.2 # # We're chasing #

- Tapping of 910C 2026 production target **600,000** (about twice the level of 2025) and Assend dies target 1.6 million throughout the year. Source: [techblog.comsoc.org 2025-10] (https://techblog.comsoc.org/2025/10/02/huawei-to-double-output-of-ascend-ai-chips-in-2026-openai-orders-hbm-chips-from-sk-hynix-samsung-for-stargate-uae-project/)
- Atlas 900 A3 SuperPoD: 384 910Cs comprising a single computing module of 300 PFLOPS.
- 2025-09 Road map: Assend,950 PR (2026 Q1), 950 DT (2026 Q4), 960, 970. 950 DT SuperCluster: 550,000 950 DT <unk> 524 EFLOPS FP8 (2026 Q4). Source: [Trend Force 2025-09-18]https://www.trendforce.com/news/2025/09/18/news-huawei-unveils-ascend-950-with-in-house-hbm-in-2026-touts-superpod-to-rival-nvidia/), [HC keynote 2025] (Huawai Official HC Keynote 2025]https://www.huawei.com/en/news/2025/9/hc-xu-keynote-speech)
- CanN (CUDA countermarked) open source 2025-12-31; triggering significant domestic developers optimization of Llama-3, Qwen kenel. Source: [Tom's Hardware Huawai ecosystem]https://www.tomshardware.com/tech-industry/semiconductors/huaweis-ascend-ai-chip-ecosystem-scales)
- $2.1 billion per year for ecological inputs for 5 years.

** Data confidence: high**

** Ajurisdictional update**: The base report "China's impact has been absorbed by about 3% of income" underestimated** the risk of future growth of the embargo** — B30A still needs to be approved, and China's Ascend 950DT SuperCluster 524 EFLOPS size (2026 Q4) is approaching the H100 level cluster. The Chinese market is short-term (described) losses for NVDA, but for a long-term period the lost TAM (potentially $20-50 billion per year).

---

#7. Synthesis of judgement tables

# 7.1 NVDA Training end monopoly

- ** Current status**: >90% share, no substantive substitute
- **Maintenance time-zone estimates**: Training end monopolistic status ** maintained > 80% in 2026-2028**; the probability of accelerated laxity has increased significantly since 2029
- **3 key untied triggers**:
1. **Athropic Ironwood/TPU training ** (400,000+ since 2027) if performance/$ compares NVDA Rubin with 20% + advantage * Second/third front laboratory follow-up
2. **AI code agent attack 100,000 kcal NCCL/mall communication adjustment** (currently at the heart of the CUDA/NVLink barrier)
3. **MoE+ Low-precision training matures to FP4/FP6 mainstream** to bring ASIC (e.g. Trainium3, TPU v8) to TCO comparable to GPU in trading-specific workload

#7.2 NVDA Logic Share

- ** Current status**: estimated 60-70% (detailed figures missing)
- **Maintenance time-zone estimates** **: ** The share of the reasoning has been eroded since 2026 and may fall to 40-50 per cent in 2028**
- **3 key untied triggers**:
1. ** Maia 200 / Trainium2 / MTIA 450** The share of GPU in the workload within hyperscaler declined rapidly after deployment at 2026-2027 scale
2. ** Groq/Cerrebras type special reasoning chip** occupied the price floor in the low-delayed, high-steak segment market
**OpenAI self-research chip** (2027 cases) if used for home-based reasoning ** direct reduction of NVDA maximum single terminal requirements

#73 NVDA Total Needs

- ** Current status**: $216 billion for FY26 and $193.7 billion for data centres
- **Maintenance time-zone estimates**:** Total demand increased beyond consensus in 2026-2027; 2028 was the key turning point**
- **3 critical vertex triggers**:
** Hyperscaler CapEx first negative ** — currently 2026 + 67%, with history never lasting more than three years; 2027 guides <+ 20% > are major alerts
** OpenAI/Anthropic was the first signal of a broken cycle of trade chain **/ Folding 2026-2027
** Training arithmetic requirements to run faster by GPU 2 quarters** - means that ASIC replacements exceed the GPU additions

---

# 8. Proposed amendments to the 2026-04-08 base report

The original report judged that the direction of the correction was based on the principle of the right to life.
|---|---|---|
**CUDA River 4.25/5** Downward to **3.75-4.0/5** Claude Code 30-minute transplant event + Triton/HIP 7 mature + ROCm gap reduced to 10-30%.
** "The short-term threat of self-research chips is overestimated"** ** "The structural erosion has begun in the short term"** <unk> Project Rainier 500,000 active + Antipic Ironwood 400,000 contracts + Maia 200 service GPT-5.2, not "the future threat" **
<unk> "NVDA is still the ruler of reasoning" ** <unk> "The theory is open battlefield" ** <unk> Deloitte/Gartner data + Groq $0.64/M tokens price floor + 4 hyperscaler self-reflection chips are simultaneously online <unk>
**AI CapEx 'underest' ** maintained, but **Added "cycle transaction" independent risk category ** ** <unk> $100 billion NVDA-OpenAI + $300 billion OpenAI-Oracle + Bloomberg thematic map. MSFT FCF - 28% cash flow false signal <unk>
** "The impact of China has been absorbed by about 3%"** ** underestimating future TAM losses** <unk> H20$4.5 billion + $2.5 billion short-term losses have occurred; China's Assend 950DT 2026 Q4 524 EFTOPS cluster will cut most of the increase in the Chinese training end
**DCF $150-160 vs share price $178** Basic assumption requires sensitivity analysis: if the reasoned share is reduced to 45% in 2028, the Māori rate returns 65%, **DCF may be $110-130** Logic + Māori return + customer concentration risk compound
** Risk rating 3.05/5 (Library perspective)** Downward to **2.7-25.5** Cycle transaction risk, customer concentration Cstomer A 22% (one customer or nearly 1/4-centre collection), geo-tam loss three synchronous deterioration

# 8.1 Overestimated risk (base report may be too worried)

- **Annual risk**: limited impact on stock prices over 2026 and stable implementation levels such as Colette Kress, Jay Puri and others
- **Accuracy of Cisco analogue**: NVDA EVI/Sales (24x) close to the top of Cisco, but margins is expanding rather than shrinking, with $30 billion in real demand for ARR-class payments certified

# 8.2 Undervalued risk (suggested)

1. ** Narrative risk/simultaneousre-Rating**: DeepSeek single day-17% has demonstrated that the market is extremely sensitive to efficiency events; the next similar event may come from Anthropic Ironwood performance data, a Chinese-cann eco-breaker, or AI coded agent attack on 100,000 kcals of communications
2. ** Single client concentration**: 22% Custamer A - extreme scenario "if the client (presumably one of Microsoft/Meta/SuperMicró) develops a significant self-replacement" not fully discussed in the base report
3. **Round finance**: NVDA for OpenAI $100 billion <unk> OpenAI for GPU * recorded in NVDA revenue. The true proportion of this "self-financing income" to the FY26-27 increment is subject to independent measurement (** Data missing**: NVDA not separately disclosed)

# 8.3 Overestimated opportunities

- "Rubin CPX reasoning optimization" narrative: with a triangulation of Groq/Cerrebras/AsIC, it is difficult for a single product to reverse the downward trend in the share of reasoning

---

# Data missing details (honest records)

1. NVDA "Customer A/B/C/D" not disclosed in 10-Q, market speculation but no confirmation
2. No official first-hand figures on the market share of the NVDA reasoning (industry estimate 60-70 per cent)
3. The "actually paid GPU amount" of the $100 billion revolving investment of NVDA-OpenAI was not separately disclosed
4. Meta MTIA does not have a single-hand load ratio for replacing NVDA GPU
5. Sam Altman ' s specific public statement about test-time compute did not directly quote it in the search results (only "Everything starts with cooperation" in the cooperation announcement)
6. Meta AI payers/incomes not found first-hand data

---

* The report is based on a first-hand public information package accessible from 2026-04-13. All key data are attached to the URL+ date. The report is positioned to provide a supplementary evidence base report (2026-04-08) and does not constitute an independent investment recommendation.*
