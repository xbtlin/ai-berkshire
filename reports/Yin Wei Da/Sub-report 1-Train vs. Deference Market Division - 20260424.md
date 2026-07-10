# AI Training vs. Logical Hardware Market Division Study

**ai-berkshire Training vs. Logic Commissioner ** 2026-04-24**

---

#1. Core judgement

The biggest structural change in the AI accelerator market in the coming 3-5 years is** the shift in emphasis from training to reasoning**: the weight of reasoning in 2026 has already taken about two thirds of AI's numeracy, and the market size of reasoning has for the first time exceeded training (approximately $118 billion vs training side of about $70-80 billion) to 2030, when the reasoning TAM may have reached 3-10 times the training level.NVIDIA maintains a 90% + share on the side of training, but** the share of reasoning has fallen from 90% in 2024 to about 65-75% in 2026** and will continue to erode over the next three years by three forces: (a) ASIC (TPU/Trainium/Maia/MTIA/Titan) for super-large clients, (b) AMD MI 350/MI400 on top of token-per-dollar, (c) a dedicated reasoning structure such as Groq/Cerrebras. NVIDIA 2030 shares in the medium scenario are about 45-55%, but absolute income has increased as the total plate has doubled,** but the Maori rate has been pushed from 75% to 60%.**

---

#2. Training vs. Arguing Market Size (2025-2030)

Year AI Main Market for Accelerators (B$)
|------|---------------------|-----------|-----------|-----------|---------|
| 2025 | ~210 | ~104 | ~106 | 1.0× | 50% |
~250-280 ~ 110-130 ~ 118-150 ~ 1.1-1.3 x ~ 55-65 per cent (caliber 2/3) ~
| 2027 | ~350-400 | ~130-150 | ~200-250 | 1.5-1.7× | ~60-65% |
~600-1,000 ~150-200 ~ 255-500 ~ 1.7-3 x (partial projection 10 x) ~65-80% ~ 65-80% ~

** Key data points**:
- 2025 The Insulation Market 106 B$ ~ 2030 255 B$ (CAGR 19.2%, MarketsandMarkets)
- Bloomberg Industry: AI accelerator 2024 116B ~ 2033 600B+
- 2026 is the first stop point ** where the theoretical cloud expenditure exceeds training** (55% vs 45%, approximately 20.6B vs 16.8B in cloud infrastructure calibre)
- The ratio of reasoning power: 2023 1/3 <unk> 2025 1/2 <unk> 2026 2/3 <unk> 2029 65% +
- The reasoning chip speciality, 50B in 2026.

---

#3. Special requirements for reasoning hardware

# Training hardware requirements
- **Super-Repeal + HBM bandwidth**: B200 192GB HBM3E, Rubin Ultra 365 TB/rack
- **Super-interconnect**: NVLink 5 1.8 TB/s, NVL72/NVL576 Mass Scale-up
- **FP16/FP8/BF16 Stabilization calculation**: Long step not capable of collapsing
- **Cluster communication**: NCCL, InfoBand 800G, flat-top
- **Reliability**: Training run 30-90 days, hardware failure rate must be extremely low
- **Customer Type Concentration**: Global 30 Frontier Lab + 20 Sovereign

# Logic hardware requirements
- ** Low delay**: Interactive < 100ms TTFT
- ** High-tungsten**: Tokens/ sec/$, tokens/ sec/W is KPI
- ** Multiprecision**: INT8/INT4/FP4/FP8 (B200 FP4 is the key selling point)
- ** Cost sensitivity**: Client bill token cost (B200: $0.02/M tokens vs H100: $0.09/M)
- ** Deployment varied**: single card to 8 card, small cluster, edge
- ** Server density**: Token capacity per aircraft / token
- ** Client fragmentation**: thousands of AI applications, SaaS, within firms worldwide

** Key differences**: Training for "performance plus reliability" and "price + delay" for reasoning. This means that the market is naturally more fragmented, price-sensitive, and ** easier to rip off by ASIC and challengers**.

---

# 4. Logic hardware competition (2026)

# A. NVIDIA (GPU, Market Leader)
- H100/H200: Still 2026 the main force of global reasoning (H200 141GB HBM3E especially suited to long context reasoning)
- B200/GB200 NVL72: FP4 performance 2xH100, single-bed 1.4 ExafLOPS FP4, inference cost 4-6x less than H100
- TensorRT-LLM + Dynamo: Software store is the moat
- **2026 Estimated Logic Share: 65-75%** (including cloud-side sales + sovereign AI)
- Rubin (2026 H2)/Rubin Ultra (2027 H2): NVL 576 Rationale 15 EF FP4, 14 x GB 300

# B. AMD (GPU, Price Challenger)
- MI300X(192GB HBM3) Microsoft Azure / Meta / Oracle
- MI325X（256GB HBM3E）：2025
- MI350/MI355X (2026 H2,288GB HBM3E): declared Llama 3.1,405B reasoned fast B200 30%, tokens-per-dollar 40% high
- MI400 (end 2026, 2027, 432GB HBM4, 19.6 TB/s): Positioning "born for inference."
- **2026 Overall AI GPU share**: 12-15% (approx. 15%)
- Weakness: ROCm is still weak and long tail clients are hard to reach.

# C. Google TPU (AsIC, self-used)
- TPU v5e (pertinent)/ v6e Trillium (2024)/v7 Ironwood (2025)
Gemini 75% plus the reasoning is running on TPU.
- Externally limited: Anthropic is the largest external client.

### D. AWS Inferentia / Trainium
- Trainium 3 (2026) + Neuron SDK
Project Rainier: Hundreds of thousands of Trainium 2 clusters
- 2026 Amazon inside AI's work load is about 30%.

### E. Microsoft Maia
- Maia 100（2024）/ Maia 200（2026）
- Mainly carry Azure OpenAI Service / Copilot reasoning
- 2026 Still a small fraction of the Microsoft AI load (<30%) but the fastest increase

### F. Meta MTIA
- MTIA v2(2025) is scaled up in the recommended system + Llama reasoning
- 2026, three intergenerational parallels.

# G. Groq LPU (AsIC for reasoning)
-500MB on-chip SRAM, 150 TB/s bandwidth (45 x H100)
- Llama 2 70B 300 tokens/sec，10× H100
- Energy efficiency 35 x H100 (150 tokens/W vs 4.3 tokens/W)
- ** acquired by NVIDIA in December 2025 at $20 billion**

### H. Cerebras WSE-3
- Whole crystal circle 44GB SRAM (880 x H100), Llama 3.1 405B > 1000 tokens/sec
- **In April 2026 OpenAI placed $20 billion in orders, Cerebras has declared IPO (value 35 billion)**

# I. Wa's Ascend
- 910C, 60% of H100, 2026, target capacity 600,000.
- 920 (2026 listed): Filling the gap after H20 exit
- 950 PR: 1.56 PFLOP, higher end to mark
- **China market share: total of local producers 41%** (Bernstein/IDC, 2026 Q1)

### J. Cambricon
- 2026, target, 500,000 Siyuan series (first annual profit)
- Limit: SMIC 7nm good rate ~ 20%, HBM restricted by Korean manufacturers

---

# 5. ASIC vs GPU in the reasoning scene

# ASIC Advantages
- Performance/Watby GPU 2-5 x
- Unit token cost low 30-50%
- For transformer reasoning datufflow optimization
- Co-ordinated with the load depth of the super-large client's work.

# ASIC Disadvantaged
- Flexibility: model architecture changes (e.g. MoE, state space models) need to be redesigned
Design cycle 18-24 months: failure to keep up with modeling
- Software is ecologically weak: compilers, but the kernel library needs to be built on its own
- High production cost: single NRE billions of dollars
- Only for big clients.

# GPU Advantages
- Universality: training, reasoning, HPC, graphics
- CUDA Eco-mature 18 years
- Follow the model innovation: Mamba, Diffusion, MoE can run.
- The rental market is highly mobile

# GPU Disadvantaged
- Relatively poor value for money (vs optimized ASIC)
- Low utilization (inference load fluctuations)
- HBM high cost

** Sensitization**: Super-large customers will continue to ASIC,** Long-tail market GPU remains the default option**.

---

#6. Large client self-researching chip shocks

<unk> Client <unk> self-research chip <unk> 2026 ratio of home-based loads <unk> influence on NVIDIA <unk>
|------|---------|---------------------|----------------|
Google <unk> TPU v7 Ironwood <unk> 75-80% (Gemini) <unk>
<unk> Microsoft Maia 200<unk> 20-30% (Ribreament) <unk> remains the number one customer for NVIDIA
AWS Trainium 3 / Inforentia 30-35% (perhaps)
<unk> Meta <unk> MTIA v2/v3 <unk> 30-40% (Rictionation + +) <unk> still buys a lot of GB200 training Llama <unk>
OpenAI <unk> Titan(Broadcom) <unk> 0% (2026) <unk> Important (2027 H2) <unk> Maximum threat in the long term
<unk> Anthropic <unk> n/a (with TPU + Trade) <unk> 60% + in ASIC <unk> almost no NVIDIA <unk>
<unk> bytes <unk> self-research + China is ascension<unk> ~50% National (China) <unk> China market loss <unk>
<unk> Ali/Tong <unk> Light + Ascend + Cambricon <unk> 40-60% National product <unk> China market loss <unk>

** Key observations**:
- Top 5 US hyperscaler 60% of the world's AI capex+
- OpenAI Titan (volume production 2027) is the single largest long-term threat to NVIDIA.
- NVIDIA Counteraction: Acquisition of Groq, Spectrum-X Network, NVL72/NVL576 Scale-up, Sovereign AI Client Diversity

---

#7. Logic profit margins vs Training profitability

# NVIDIA training chip
- Māori 75% +
- ASP: H100 $30-40k, B200 $30-50k, GB200 NVL72, full cabinet of approximately $3 million
- Clients are extremely willing to pay premiums.

# NVIDIA reasoning chip
- Māori estimates 60-70 per cent
- Clients are highly price sensitive.
- AMD MI355X direct price
- ASIC, lower market reference price.

# Three years of trend
- NVIDIA Total Data Centre Māori ratio may be from **75% <unk> 65-68%** (2028)
- **Democracy of absolute income** (2026 ~ 190B ~ 2028 ~ 350B data centre)
- NVIDIA Response: Systemized sales (NVL72/NVL576/Spectrum-X); sell racks instead of chips

---

# 8. 3 scenario projection (2030)

# # optimism (NVIDIA reasoning share 55-60%)
- CUDA + TensorRT-LLM + Dynamo Eco-Treasures Persistence
- AMD ROCm stopped at 12-15%.
- NVIDIA data centre 2030 Income 500B+, Māori 70%+

# Neutral (NVIDIA reasoning 40-50%)
- AMD MI 400/MI500 takes 20-25% of the market of reasoning
- Top 5 hyperscaler self-compatibility 50-60% internal reasoning
- The Chinese market is largely lost.
- NVIDIA data centre 2030 Income 350-400B, Māori 65%

# Pessimism (NVIDIA reasoning 25-35%)
- Big client self-studyed all the time. OpenAI leaves NVIDIA.
- AMD MI500, performance reverse.
- ASIC Commercialization
- NVIDIA data centre 2030 Income 250-300B, Māori 55-60%

**ai-berkshire main baseline judgement**: neutral optimism. NVIDIA is still close to monopoly for the next 5 years on the training side; the reasoning side is eroded but absolute plate is three times the size.** The real risk is a structural 10-15 percentage point shift in the Māori rate.**

---

#9. Meaning of key investments

1. **NVIDIA is not "training chip unit" but "AI systems infrastructure unit"**: NVL576 + Spectrum-X + CUDA + Dynamo + Groq
2. **The reasoning that market segmentation is irreversible**: NVIDIA ' s share of reasoning will inevitably decline over the next 5 years, but the total plate x share = absolute income is still rising
3. **AMD is the real number two **: MI400 is the key product, and the financial statement is the validation window
4. **Broadcom is the "Seller of the Steak"**: all big clients ASIC are designed by Broadcom
** China AI Chip is parallel universe**: China is + Cambricon has split the autumn with NVIDIA in the domestic market
**OpenAI towards Broadcom is the largest crack in NVIDIA long-term narrative**: 2027-2028 is the observation point
** The profit of reasoning has been moved down = NVIDIA PE should be contracted ** From 35-40 x training to 25-30 x reasoning in the training era

---

*ai-berkshire Training vs. Logic Commissioner * Report completed *
