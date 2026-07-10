# NVDA self-study chip threat depth

** Date of report: 19 April 2026**
** Research question: How is the competitiveness of the four major clients self-research chips vs. AMD? Impact on NVIDIA mounds and pricing rights? 3/5/10 outlook**
** Methodology: three-line parallel studies — hardware comparison, moat analysis, economics and historical precedents**
** Key constraints: distinguishing "fact confirmed" from "estimate", all data attached to source**

> ** Statement**: This report is intended to present both positive and negative aspects. The conclusions are not intended to be too much or too much empty from the data.

---

# One or four major clients self-researching the chip pans

#1.1 NVIDIA client concentration (first-hand data)

NVIDIA 10-Q (FY2026 Q3, as of 2025-10-26) discloses:
- **Customer A：22%**、B：15%、C：13%、D：11%
- Four major direct clients together accounted for 61%**
- The four direct clients, mainly OEM/ODM/distributors (Foxconn, Wistron, SuperMicro), eventually concentrated in a high concentration **AWS/Azure/GCP/Meta**

Source: [NVDA 10-Q 2025-10-26] (NVDA 10-Q)https://www.sec.gov/Archives/edgar/data/1045810/000104581025000230/nvda-20251026.htm)

** These four largest terminal clients, all in self-research chip.**

---

# 1.2 Status of four self-research chips (house-to-house dismantling)

#### Google TPU Ironwood (v7)

<unk> Indicators <unk> Data <unk> Source <unk>
|------|------|------|
<unk> Publication April 2025, Claude Next 2025 <unk> Google Official <unk>
<unk> FP8 <unk> 4,614 TFLOPS/chip** <unk> Google Cloud Blog <unk>
<unk> HBM<unk> **192GB HBM3e** <unk> Ibid. <unk>
<unk> Memory bandwidth <unk> 7.2 TB/s**
<unk> Cluster size **9,216 chips/Pod**, cluster total 42.5 ExafLOPS <unk>
♪ The way I'm going ♪
Key contract <unk> 400,000 Ironwoods, ~10 billion, Broadcom Distribution, 2027 online [Bloomberg 2026-04-06] (Bloomberg 2026-04-06]https://www.bloomberg.com/news/articles/2026-04-06/broadcom-confirms-deal-to-ship-google-tpu-chips-to-anthropic) |
<unk> Front-line model validation <unk> Gemini 3 is fully trained on TPU and does not use NVIDIA GPU** <unk> [Google Blog] (https://blog.google/technology/google-deepmind/ironwood-tpu/) |

** Key facts**: Google is the only company that has proven to be able to **deficient to NVIDIA training large front-line models**. The core advantage of TPU is not single chip computing, but ** hyper-large interconnection** (9216 chip full-to-continue Pod).

Source: [Google Cloud Blog] (https://cloud.google.com/blog/products/ai-machine-learning/introducing-ironwood-our-7th-generation-tpu), [Anthropic Official] (@Amsym)https://www.anthropic.com/news/google-broadcom-partnership-compute)

---

#### AWS Trainium2 / Trainium3

Indicators
|------|-----------|-----------|
<unk> Status <unk> Deployments on scale** <unk> Released at the end of 2025 <unk>
<unk> BF16 Calculator ~760 TFLOPS (estimated, officially 4x Trainium1) <unk> FP8 ** 2,520 TFLOPS**(4.4x Trn2) <unk>
<unk> HBM<unk> 96-128GB HBM3**
Project Rainier: ** Nearly half a million**, Anthropic exclusive use of <unk> undisclosed
<unk> AWS pricing <unk> rn2.48xlarge ~ $21.50/hr(16 chip) <unk>
vs p5.48xlarge (8xH100) ~ $98.32/hr<unk>

** Key facts**:
- AWS CEO Matt Garman confirmed that Anthony would deploy on Trainium2 by the end of the year, over **1 million **
- TechCrunch 2026-03: Trainium won Anthropic, but started to be used by **OpenAI, Apple**
- AWS internal benchmark: Trainium2 at Llama 70B training better than H100 **30-40%**
- ** Never submitted MLPerf** without independent third party validation

Source: [AWS Official Project Rainier] (AWS Official)https://www.aboutamazon.com/news/aws/aws-project-rainier-ai-trainium-chips-compute-cluster)、[TechCrunch 2026-03](https://techcrunch.com/2026/03/22/an-exclusive-tour-of-amazons-trainium-lab-the-chip-thats-won-over-anthropic-openai-even-apple/)

---

#### Microsoft Maia 200

Indicators Data
|------|------|
<unk> 2026-01 deployed at the Iowa data centre, next station Phoeenix <unk>
♪ The power of the station 3 nm ♪
<unk> FLOPS<unk> ** Almost undisclosed**
<unk> Positioning <unk> Pure reasoning chip** (untrained replacement) <unk>
<unk> Purposes <unk> Services **OpenAI GPT-5.2**, supporting M365 Copilot <unk>
The planned volume production for 2025 was delayed by approximately six months (as a result of changes in OpenAI requirements)

** Key facts**:
- The Maia series is the most opaque of the four self-research chips** and there are no open baseline tests.
- Industry analysts assume that Maia 100 has roughly 50-70% of the reasoning performance of the H100 standard (** not substantiated**)
- Positioning is clearly ** sole to reasoning**, not a substitute for training in GPS

Source: [Microsoft Blog 2026-01-26] (https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/)

---

# Meta MTIA Road Map

The intergenerational process, the process, the algorithm, the power, the power, the positioning, the state, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the position, the power, the state, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the power, the state, the state, the state, the power, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means, the means
|------|------|------|------|------|------|
<unk> MTIA v1<unk> 7nm<unk> INT8102.4 TOPS<unk> 25W <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk>
<unk> MTIA v2<unk> 5nm<unk> 150 TFLOPS FP16 (estimate, 3xv1)<unk> 90W<unk>
<unk> MTIA 300<unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk>
<unk> MTIA 450/500 <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> 2027 <unk>

** Key facts**:
- 2026-03-11 Meta-Service MTIA 300/400/500 4 generation plan**, six-month succession** (business typical 1-2 years)
- MTIA** does not directly compete with GPU** - designed to be low-power reasoning ASIC, optimizing recommended/advertised ranking
- Meta estimates MTIA's value for sorting reasoning better than GPU ** 2-3 times**
- Meta still has over **600,000 H100** for training,** training end not replacing NVIDIA**
- Zuckerberg confirmed that MTIA would not replace NVIDIA GPU for training.

Source: [Meta Official 2026-03] (https://about.fb.com/news/2026/03/expanding-metas-custom-silicon-to-power-our-ai-workloads/)、[Meta AI Blog](https://ai.meta.com/blog/meta-mtia-scale-ai-chips-for-billions/)

---

# 1.3 Four master self-research chip capability overview

<unk> Google TPU<unk> AWS Tradeinium<unk> MS Maia<unk> Meta MTIA<unk>
|------|-----------|-------------|---------|-----------|
** Can replace NVIDIA training?** <unk> <unk> <unk> (Gemini 3) <unk> Partial (70B parameters) <unk>
** Can replace NVIDIA reasoning?**
** Size** GW class, 400,000 Ironwood contracts <unk> 5-1 million Trn2<unk> unknown <unk> 1 million
**Soft Ecology** <unk> JAX/XLA, TorchTPU Propulsion<unk> NeuronSDK<unk> Internal <unk>
<unk> Open benchmark** <unk> MLPERf<unk> MLPERf<unk>

** Conclusion**: Only Google has proved to be a complete substitute for NVIDIA for forward model training.

---

# Two, self-research chips vs. AMD -- who's more threatening?

#2.1 AMD Current Competitiveness

<unk> MI300X <unk> MI325X <unk> MI350X (projected 2025 H2) <unk>
|------|--------|--------|----------------------|
D.D.C. 3
<unk> HBM <unk> 192GB HBM3 ** 288GB HBM3e ** <unk> 288GB HBM3e (projected) <unk>
<unk> Swipe 5.3 TB/s<unk> 6 TB/s<unk> 8 TB/s (expected)
FP8<unk> 2,615 TFLOPS<unk> 2,600 TFLOPS<unk> Officially known as the reasoning 35x MI300X
<unk> Employer 750W<unk> E750W<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E<unk> E7FFFFFFFFFFFFFFFFF
<unk> Price pricing <unk> $10,000-15000 <unk> $15,000-20000 (estimate) <unk>

**Backfire NVIDIA**:

Indicator: AMD MI300X; NVIDIA H100; NVIDIA B200;
|------|-----------|-------------|-------------|
<unk> HBM capacity <unk> 192GB<unk> 80GB<unk> 192GB<unk>
<unk> Memory bandwidth 5.3 TB/s <unk> 3.35 TB/s <unk> 8 TB/s <unk>
FP8<unk> 2,615 TFLOPS<unk> 1,979 TFLOPS<unk> ~9,000 TFLOPS (short) <unk>
Cost $10-15K
Influence Fabric ~ 896 GB/s <unk> NVLink 4: 900 GB/s <unk> NVLink 5: 1.8 TB/s <unk>

** MLPerf results (limited but available)**:
- MLPerf Training v. 0 (2024-06): AMD MI300X** initial submission**, GPT-3 175B training is comparable to H100 but less extensive submission
- MLPerf Investment v4.1 (2024-09): MI300X deduces that certain scenarios in Llama 2 70B ** are close to or above H100** (benefiting from 192GB large memory)
- Overall, NVIDIA remains in the lead with TensorRT-LLLM optimization.

Source: [MLCommons] (https://mlcommons.org/benchmarks/training/), [AMD Official] (Ambassador)https://www.amd.com/en/products/accelerators/instinct/mi300x.html)

##2.2 AMD Market Share

<unk> NVIDIA <unk> AMD <unk> Intel <unk> self-research chip (Google/AWS etc.) <unk>
|------|--------|-----|-------|------------------------|
~92-98% ~2-3% ~ <1% ~ very small ~ ~2% ~2% ~2% ~2% ~2% ~2% ~2% ~2% ~2% ~2% ~1% ~1% ~1% ~1% ~1% ~1% ~1% ~2%
| 2024 | ~85-90% | ~5-8% | ~1-2% | ~3-5% |
| 2025E | ~80-85% | ~8-12% | ~2-3% | ~5-8% |

*Note: This is the share of the market for sale of AI accelerators, excluding internal self-use chips such as Google TPU. * Including self-use chips, NVIDIA 2024 "extended share" may be 70-80%.*

Source: Mercury Research, JPMorgan estimates (larger differences among agencies, above integrated calibres)

**AMD income scale**:
- 2024 data centre GPU contract ** $5 billion +**
- Target 2025 approximately **$70-$90 billion**
- Compare NVIDIA SY2025 data centre ** $11.59 billion** - AMD about NVIDIA **1/16**

**AMD Large Client** Microsoft Azure (Max), Meta, Oracle Claude, CoreWeave

# 2.3 AMD Core Bottle

** AMD's biggest problem is not hardware, but software**:
- ROCm and CUDA gap narrowed from 2-3 times in 2023 to **10-30% in 2026 ** Source: [ThunderCompute 2026-04] (G77-04-04-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-08-06-08-08-08-08-08-06-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-https://www.thundercompute.com/blog/rocm-vs-cuda-gpu-computing)
- However, the gap between long-tail library support, debugging tool (Nsight level), performance optimisation and closure** still needs to be filled over 3-5 years
- MI300X can run most standard PyTorch work loads, but ** extreme optimization and ease of deployment** is still far from CUDA
- Key references: The AI coding tool (Claude Code et al.) has been able to transplant simple CUDA kennel to ROCm in 30 minutes** but complex interconnection libraries and system level optimization are not yet possible**

#2.4 Self-research chips vs AMD: Who is more dangerous?

<unk> dimension <unk> self-research chip (TPU/Trainium/ Maia/ MTIA) <unk> AMD <unk>
|------|----------------------------------|-----|
** Economic motivation**
** Software ecology** <unk> Self-built (JAX/XLA/NeuronSDK) or PyTorch suitable for <unk> ROCm, less than CUDA <unk>
<unk> Training alternative capabilities** <unk> Google has been certified; AWS partially authenticated <unk> but ecologically immature <unk>
<unk> Alternatives** All available, partially deployed
<unk> Size** <unk> Total millions of grades <unk> much less than NVIDIA
** The real threat to NVIDIA** ** very high - direct reduction in procurement volume of the largest NVIDIA clients** medium - major marginal share **

** Judgement: The threat of self-research chips is much greater than the AMD.**

- AMD is a cheaper alternative to the same dimension - NVIDIA still has technical substitutes and software barriers to defend.
- The self-research chip is "Crowds turned into Compete." ** Your four biggest clients are making weapons for themselves. ** This is a structural threat that cannot be addressed with reduced prices.

---

# Three, NVIDIA's moat # # How far is it?

#3.1 Protector River Level Analysis

# First layer: CUDA ecosystem (the moat is being eroded)

<unk> Indicators <unk> Data <unk> Source <unk>
|------|------|------|
<unk> CUDA registered developer <unk> 4 million + (cumulative) active approximately 1.5-2 million <unk> NVIDIA GTC 2024 <unk>
<unk> GPU acceleration library/SDK <unk> 800+<unk> NVIDIA network <unk>
<unk> PyTorch Default Backend <unk> CUDA(>95% used) <unk> PyTorch Community <unk>
<unk> ROCm vs CUDA Gap <unk> Calculate intensive workload gap narrowed to 10-30% (2026) <unk> ThunderCompute <unk>

** Erosion signal**:
- Claude Code and other AI encoding tools can be transplanted in 30 minutes from simple CUDA to ROCm - threshold deviations
- Triton 3.6.0 (OpenAI open source compiler) has been introduced into the AMD HIP AOT compilation - cross-platform programming becomes a reality
- Google launched the TorchTPU project to work with Meta to achieve the birth support of PyTorch on TPU
- 95% accuracy of CASS model (academic research) source-level translation

** Evidence that the moat is still in place**
- 100,000-carat-class cluster training telecommunications counter (NCCL/NVLink/InfiniBand) with short-term success - AI code tool
- ** Not found ** publicly attributed to the massive failure of the forward LLM training due to "non-CUDA pit defects".
- Full tool chain integration (debug + performance analysis + deployment optimal closed loop) - ROCm gap remains wide

** Assessment: clear erosion of the mooring river at the code level; system-level mooring river (100,000 kcal of communications/movement) has not yet been moved**

---

## Second floor: NVLink/NVSwitch is connected (the hardest moat)

<unk> Interconnection technology <unk> bandwidth <unk> differences <unk>
|---------|------|------|
<unk> NVLink 5.0(B200)<unk> **1.8 TB/s Double-way** <unk> Industry leads
<unk> GB200 NVL72 <unk> 72 GPU Full Interconnection** (Unblocked) <unk> Unique
AMD Infinity Fabric ~896 GB/s <unk>
<unk> Google TPU ICI ~ 4.8 Tb/s/chip <unk> Pod strong, but closed ecological <unk>
Intel Gaudi3<unk> 300 GB/s<unk>

** Key insight**:
- 72-GPU full-to-back connectivity of GB200 NVL72 is the exclusive advantage of the large model training (all-reduce communication)**
- The gap between competitors in single-air connections has narrowed (advantages in AMD's unified memory), but ** Inter-air interconnection** remains the NVIDIA killer.
- Ultra Ethenet Consortium (AMD/Intel/Broadcom) tried to catch up and mature ** 2-3 years**

---

#3rd floor: pricing (still extremely strong)

** Māori rate trend**:

Quarterly Noon-GAAP Māori ratio
|------|---------------|------|
<unk> FY2024 Q1(2023-04) 66.8% <unk> H100 starts to release <unk>
<unk> SY2024 Q4(2024-01) <unk> 76.7% <unk> Peak
<unk> SY2025 Q1 (2024-04) **78.9% ** History
<unk> FY2025 Q3(2024-10) <unk> 75.0 <unk> Maintenance of height <unk>
<unk> SY2025 Q4(2025-01) ~73.5% <unk> Blackwell climbs the slopes ~

Source: [NVIDIA Investor Resources] (NVIDIA Investments)https://investor.nvidia.com)

**73-79% Māori is top in semiconductor industry** (Intel ~ 40-45%, AMD ~ 50-52%).

** Pricing strategy**: NVIDIA uses the "no downscaling" strategy - B200 value for money (perf/$) up from H100 ~4x, but ** absolute price ** unchanged. GB200 NVL72 full cabinet $2-3M, locking system-level purchases.

** Price-reducing pressure evidence**:
- Large cloud manufacturers have a certain bargaining power over H100 (cyclical switch before Blackwell is listed), but this is product exchange practice.
- Semi Analysis estimates that the actual discount for large clients is about 15-25% - industry practice does not represent a reduction in pricing authority
- ** None of the four major clients complained publicly about the overpriced NVIDIA** - but all of them were self-researching chips, which in itself was the biggest hidden response to the pricing power.

** Sensitization: pricing rights are still short (2-3 years), but the real purpose of client self-study is to get rid of the pricing rights**

---

# 3.2 Array River Rating

The moat level, the current strength, three years later, five years later, ten years later, and the next.
|-----------|---------|-------|-------|--------|
The CUDA level.
System level (100,000 kC/M)
NVLink/NVSwitch is connected.
I'm not sure what you're doing.
I'm not gonna be able to get you out of here.

---

# Four. Economics analysis: How powerful are the self-research chips?

##4.1 Cost comparison

The project is based on the following:
|------|---------|---------|------|
<unk> NVIDIA H100 (AWS p5 example) ~ $98.32/hr (8 x H100) <unk> Base <unk> AWS pricing <unk>
<unk> AWS Trainium2(trn2 example) ~ $21.50/hr (16 Trn2) <unk> cheaper than H100 <unk> 54% <unk> AWS pricing/internal base
<unk> Google TPU v5e (Riction) <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> (Riation) <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk>
<unk> Meta MTIA (sort reasoning) <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk>

Source: [CloudExpat comparison] (https://www.cloudexpat.com/blog/comparison-aws-trainium-google-tpu-v5e-azure-nd-h100-nvidia/)、[AI News Hub](https://www.ainewshub.org/post/nvidia-vs-google-tpu-2025-cost-comparison)

# 4.2 Super-scale cloud company capital expenditure

Company, CapEx 2025, CapEx 2026
|------|-----------|-------------------|
| Amazon | $100-118B | ~$200B |
| Alphabet | $75-85B | $175-185B |
| Microsoft | $80-121B | $110-120B |
| Meta | $64-72B | $115-135B |
** Total** **$380-450B** ** ~$600-630B** **

Source: [Introl] (https://introl.com/blog/hyperscaler-capex-600b-2026-ai-infrastructure-debt-january-2026)、[CNBC 2026-02-06](https://www.cnbc.com/2026/02/06/google-microsoft-meta-amazon-ai-cash.html)

About 75 per cent (~$450B) goes to AI infrastructure.** Assuming that self-research chips save 30 per cent of the cost, substitution alone means $50-100 billion annually — a very powerful economic motive**.

# 4.3 Broadcom -- self-research chip "arms dealer"

<unk> Indicators <unk> Data <unk> Source <unk>
|------|------|------|
<unk> Self-research chip clients ** 6 **: Google, Meta, OpenAI, Anthropic, +2 unpublished (presumably ByteDance, Apple) **
<unk> SY2025 AI Income **$19.9 billion** (+63% YoY) <unk> [CNBC 2025-12-11] (g)https://www.cnbc.com/2025/12/11/broadcom-avgo-q4-earnings-2025.html) |
<unk> SY2026 Q1 AI Income **$84 billion** (+106% YoY) <unk> Broadcom Financial Statement <unk>
<unk> FY2027 CEO Target <unk> $100 billion**<unk> [IO Fund] (https://io-fund.com/ai-stocks/broadcom-stock-silent-winner-ai-monetization) |
♪ The big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big,
<unk> Google TPU long from <unk> to **2031**<unk> [247Wallst] (https://247wallst.com/investing/2026/04/07/broadcoms-long-term-google-tpu-deal-is-bigger-than-it-looks-for-ai-infrastructure/) |
<unk> OpenAI Contract <unk> "Titan" XPU, **10GW** Calculator Target 2029 <unk> [Next Platform]https://www.nextplatform.com/2025/09/05/broadcom-lands-shepherding-deal-for-openai-titan-xpu/) |

**Broadcom AI income for two years from $12.2 billion <unk> target $100 billion + (~8 times) directly corresponds to the rate of market transfer by ASIC to replace GPU.**

** Core Insight**: Broadcom is not a direct competitor of NVIDIA, but ** Helps NVIDIA clients become competitor of NVIDIA. This is a more dangerous threat vector than AMD - AMD provides a replacement for GPU, and Broadcom helps clients build their own chips.

---

# V. Historical precedent: lessons from Intel

# 5.1 How long did Intel take from 98 to 73%?

Time, event, Intel x86 server share
|------|------|-------------------|
<unk> 2017 <unk> EPYC before release <unk> 98%**
<unk> 2020 <unk> Apple abandons Intel ~90% <unk>
<unk> 2021 Q4 <unk> AMD rise **77% **(AMD 18%) <unk>
| 2025 Q2 | — | **72.7%**（AMD 27.3%） |
<unk> 2025 <unk> ARM server <unk> extra <unk> 15-21%** <unk>

Source: [Semi Engineering]https://semiengineering.com/data-center-cpu-dominance-is-shifting-to-amd-and-arm/)、[Light Reading](https://www.lightreading.com/semiconductors/intel-is-losing-market-share-left-right-and-center-)

** From 98% to ~73% (in x86), about 8 years**. Adding to ARM erosion, Intel's "extended share" may have fallen to ~55-60%.

# 5.2 Similar to NVIDIA

<unk> dimension<unk> Intel current year
|------|----------|-----------|
<unk> Ecolocking <unk> x86 command set <unk> CUDA<unk>
<unk> Māori ~ 60% (peak), attraction of substitution ~ 75% (peak), ** higher** - more motivational alternatives <unk>
Client self-study: Apple M Series, AWS Graviton <unk> Google TPU, AWS Trainium, MS Maia, Meta MTIA
<unk> Implementation <unk> Failure ** (delayed process, missed movement) <unk> Extreme ** (annual succession, leading by NVLink) <unk>
<unk> Substitute time ~ 8 years of significantly declining share ~ <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk>

** Key differences**:
- Intel's decline is due to the failure of its own execution.
- NVIDIA is currently very strong in implementation - a new generation of new items each year (accelerating from two generations), active defense
- But the biggest risk is not "the other NVIDIA," but "every major customer is making his own NVIDIA." - This is closer to the ARM mode.

** Another case** AWS Graviton has already switched more than half of the AWS data centre CPUs to self-research ARM chips, claiming 40% higher value than x86. This path has been validated.

---

# VI, 3/5 and 10 years outlook

#6.1 Market share projections

** Training market**:

♪ The big challenger ♪
|------|-----------|-----------|---------|
<unk> Current (2026)<unk> 90%<unk> Google TPU<unk> Only Google has verified the entire TPU training <unk>
<unk> 3 years later (2029) <unk> 70-80%** <unk> TPU + Tradeinium3 <unk> Anthropic/OpenAI partial training moved to self-research chips
5 years later (2031) **55-65% ** Multiple ASIC <unk> AI coding tools to hit the communications store and the cost of relocation has dropped considerably <unk>
<unk> 10 years later (2036) <unk> 40-55% <unk>

** The market of reasoning** (more important — the scale is outpacing training):

<unk> Time <unk> NVIDIA share <unk> Key trends <unk>
|------|-----------|---------|
<unk> Current (2026) <unk> 60-70% <unk> Logic ~2/3 (Deloitte) <unk>
<unk> 3 years later (2029) **35-45% <unk> Maia/MTIA/Trainium massive replacement internal reasoning <unk>
<unk> 5 YEARS LATER (2031) ** 25-35% <unk> Groq/Cerrebras special chip in the low delayed market <unk>
<unk> 10 years later (2036) ** 20-30% ** ASIC dominates the reasoning <unk>

Source: [Deloitte TMT 2026] (https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/compute-power-ai.html)、[Counterpoint](https://counterpointresearch.com/en/insights/AI-Server-Compute-ASIC-Shipments-to-Triple-by-2027)、[Silicon Analysts](https://siliconanalysts.com/analysis/nvidia-ai-accelerator-market-share-2024-2026)

**Note: ** The above projections are based on a combination of multiple analysts and are highly divisive. Conservatively, Semi Analysis/Bernstein believes that NVIDIA still has a combined share of 65% after five years; radical ends (partially independent analysts) believe it is possible to fall below 40%.

#6.2 Analyst summary

<unk> Analyst/agency <unk> Core view <unk> Orientation <unk>
|------------|---------|------|
**Stancy Rasgon** <unk> NVIDIA platform values are underestimated, and even if the share falls, market size growth can support growth **
** Morgan Stanley** <unk> Data centre AI investment cycle until at least 2027, with NVIDIA being the largest beneficiary; after 2027, the reasoning of fragmentation is risk <unk> neutral multiplicity <unk>
<unk> Semi Analysis** <unk> Custom chip threat real, 20-30% in 2027; NVIDIA network+ software is the deepest moat
**Trendforce/Gartner** <unk> NVIDIA share from 90% + to 70-75%, but absolute income still rises *
<unk> ** Gaushem** <unk> Forecast 2026 Q4 TPU 35% in the reasoning market <unk> neutral emptiness (NVIDIA reasoning) <unk>

# 6.3 A combination of three temporal dimensions

#3 years later (2029): Still dominant, but slower

- ** Training end**: NVIDIA remains the preferred option for training (70-80% share) and NVLink/NVSwitch interlinkage advantages remain
- ** at the end of the reasoning**: the share decreased from 60-70 per cent to 35-45 per cent, the main share of which was lost to the battlefield
- ** Pricing rights**: maintained at 70% + Māori, but the increase shifted from "volume plus price" to "volume"
- **Risk signal**: Hyperscaler CapEx first negative - not at the present time, three years in a row.
- ** Confidence**: ** High**

# # 5 # (2031): Largest player but not monopoly

- ** Training end**: 55-65% TPU/Trainium has been able to train all scale models and CUDA migration costs have been significantly reduced
- ** at the end of the reasoning**: 25-35%, ASC dominated the reasoning market
- ** Pricing rights**: Māori rates may return to 65-70% - still good, but no longer "overconsumption of profits"
- ** Absolute income**: The decline in the share may be offset by the growth in the size of the AI market -** Total income may not necessarily fall, but the rate of increase will be significantly slower**
- ** Confidence**: ** Medium**

# # 10 years later (2036): High uncertainty

- If Transformer continues to dominate, NVIDIA may still maintain a 40-55% training share with continuous rotation.
- If there is a paradigm shift (non-Transformer structure), all current chip routes optimized for Transformer could be disrupted, and NVIDIA and ASIC would have to re-enter.
- ** Analog**: No one predicted Transformer 10 years ago, and the pattern of calculations after 10 years is equally unpredictable
- ** Confidence**: ** Low**

---

# VII. Illustrative conclusions (both sides)

# Look at the arguments

1. ** Market size growth > share **: Even if NVIDIA ' s share is reduced from 90% to 60%, if the AI Accelerator ' s total market is increased from $100 billion to $500 billion, NVIDIA ' s absolute income is still growing
2. **Experiently implemented**: New annual generation, NVLink 2-3 years apart, management discipline is rare in semiconductor industry
3. **CUDA system level barriers remain **: 100,000 KCL communications/movement optimization, no replacement for 3-5 years
4. ** "Reflexion alternative training" benefits NVIDIA**: The reasoning market is more fragmented but the total is larger - NVIDIA may earn more even if its share is reduced
5. **Blackwell/Rubin product cycle**: strong product rotations in 2026-2027

# Look at the empty arguments

** Four major clients, rivals**: all clients, which together account for 61 per cent of the revenue, are self-researching — a structural threat, not a cyclical one
2. ** The reasoning is the main battleground, and the NVIDIA ' s share has accelerated the loss**: from 2024 to ~70% to 2028, it may be less than 40%
3. **Broadcom AI income eight times greater than two years = direct evidence of ASIIC replacement acceleration**
**75% + Māori attract replacement**: History lessons (Intel ~ 60% is enough) and NVIDIA's excess profit is the biggest economic driver of self-study by clients
** Gemini 3 fully trained on TPU** - "NVIDIA is the only choice for training" narrative has been proven false
**Round transaction risk**: NVIDIA invests OpenAI $100 billion * OpenAI buys NVIDIA GPU * which is essentially "pay for its future income"
7. **CUDA layer mounds are being eroded by the AI coding tool + open source compiler** and the migration threshold has been reduced from "a few months of engineer team" to "one hour"

# A piece of Eun-hei question

"Do you plan to take 10 years? If the share of NVIDIA in 10 years is 40-55%, the Māori rate is 65-70% -- does this match today's valuation?"

> "The best business is that consumers ** do not want to change ** (show, apples). The problem with NVIDIA is that its clients ** want to change ** and have the money to build themselves."

"Don't assume that a company is always good because it's good today. The moat is gonna be filled up -- the problem is just speed."

# Barfitt's perspective

"When your biggest client is also your biggest potential competitor, your pricing is borrowed, not owned."

---

# Eight, the precise layer of the CUDA mound -- "Sweet code/hard system" is excessively simplified

The original judgement "CUDA's layer is eroded, the system-level moat still hard" needs correction. The moat is not dichotomy, but **6 levels **:

Level, level, content, current state, difficulty of replacement.
|------|---------|---------|-----------|
<unk> 1 single kernel port <unk> CUDA <unk> ROCm/HIP <unk> AI tool can complete simple kernel <unk> low** <unk>
<unk> 2 Core library <unk> cudnn, TensorRT <unk> AMD MIOpen over 70-80%
<unk> 3 frame integration <unk> PyTorch defaults that CUDA <unk> ROCm can run most of PyTorch; Google push TorchTPU ** in **
<unk> NCCL <unk> RCCL/Gloo is weaker than NCCL; but PCCL has surpassed RCCL 60-80% at 1024+GPU ** medium-high**
5 <unk> NVLink/NVSwitch <unk> Google ICI 3D torus independently solved (9,216 chip Pod); Ultra Ethenet 2-3 years behind ** high (but with alternatives)** <unk>
<unk> 6 Full-Stocking <unk> 100,000-cal-to-end training session <unk> Gemini3 completed; tolerance is being automated by Clockwork.io/AutoClusters and others <unk> High (but not insurmountable)**

Source: [Google TPU7x document] (https://docs.cloud.google.com/tpu/docs/tpu7x), [PCCL thesis arXiv] (https://arxiv.org/html/2504.18658v1)、[Clockwork.io TorchPass](https://www.morningstar.com/news/accesswire/1145681msn/clockworkio-introduces-a-new-class-of-fault-tolerance-to-end-failure-driven-gpu-waste-in-ai-training)

# "System-level moat still hard" what's right and wrong

** Correct part**: Only two entities worldwide can independently complete 100,000 plus chip scale training - NVIDIA (general programme) and Google (TPU). For the vast majority of AI companies, universities, start-ups, CUDA+NVLink remains the only viable option.

** The wrong part**: Google has proved that the problem is solved. TPU Ironwood ICI 1,200 GB/s two-way/chip, 3D torus pistol, 9,216 chip/Pod, Jupiter network supports 100,000 plus chip.** If the system-level moating river is still "hard," Google cannot do Gemini 3 full TPU training**

** More precise judgement**: The moat broke from the top — the largest 5-6 clients are crossing the walls; however, 99 per cent of the world's AI developers are still locked in the city.

♪ The CUDA moat ♪
|---------|-----------|------|
**Google**<unk> separated from <unk> Gemini 3 full TPU training, internal JAX/XLA complete <unk>
**AWS/Anthropic**<unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> forward trainings not fully authenticated <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk>
<unk> **Meta** <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk>
♪ The training is still dependent on NVIDIA ♪
**OpenAI**<unk> Medium-term exit <unk> Broadcom co-operation Titan XPU 2027 deployment <unk>
** Startup Company/University** <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> no one to study themselves without money <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> no no <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> no no no no no no <unk> <unk> <unk> <unk> <unk> <unk> <unk> no <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> no <unk> no no

---

# IX. Client concentration of first-hand data (SEC 10-Q)

# # # SY2026 quarter (2025)

Quarterly A Questmore B Questmore C Qustamer D Quest Total
|------|-----------|-----------|-----------|-----------|------|-------|
<unk> 2 (2025-07) <unk> 23%** <unk> 16%** <unk> 14% <unk> 11% ~ 64% <unk> $57 billion <unk>
<unk> (2025-10) ** 22% ** 15% ** 13% <unk> 11% ** 61% ** $57 billion **
♪ The world's greatest ♪

The same ratio worsened: only three clients each accounted for 12 per cent (36 per cent of the total) of Q3 SY2025.

Source: [NVDA 10-Q] (https://www.sec.gov/Archives/edgar/data/1045810/000104581025000230/nvda-20251026.htm)、[Motley Fool](https://www.fool.com/investing/2025/11/27/blackwell-off-charts-nvidia-customer-concentration/)

**Note: The four "direct clients" are OEM/ODM (Foxconn, Wistron, SuperMicro, etc.) and the terminal is concentrated in AWS/Azure/GCP/Meta. UBS assumes Custamer A (FY 2025 19%) as Microsoft.

# # Four major terminal buyers depending on NVIDIA sort

<unk> Company <unk> NVIDIA Dependence <unk> NVIDIA procurement estimates (2026) <unk> Source <unk>
|------|------|-------------|---------------------|------|
<unk> 1 <unk> Microsoft** <unk> High -- Maia only makes reasoning, training depths tied <unk> $40-50 billion
<unk> ** Meta** <unk> very high -- 600,000 plus H100 training, MTIA only sorted reasoning <unk> $35-45 billion (estimated) <unk> industry extrapolation <unk>
<unk> **Amazon** Medium and High - Trainium 2-scale deployment but training capacity to be validated
<unk> **Google** ** Minimum** - TPU has been fully replaced by a GPU for Claude's client $13-25 billion (estimated) <unk> Bloomberg "about 6% NVIDIA income" <unk>

**Google is the lowest procurement of NVIDIA in four households** ** because it is the only company that has proven to be completely free from the NVIDIA training frontier model.

---

# Ten, Google TPU Outlet - Paradigm shift

# History: No hardware until 2024, leased only through GCP

- 2015: TPU v1 is used internally only
- 2018: Claude TPU online GCP, client rents by hour, doesn't get the chip.
- 2020-2024: Continued rent- and-no-sale only

# 2025-2026: paradigm shift has taken place

**Anthropic - the first external customer to buy TPU directly**:

The amount of the money is the same as the amount of the money.
|------|------|------|------|
♪ The first phase of the GCP cloud rental ♪
<unk> Phase II <unk> Broadcom directly sells the Ironwood cabinet** **400,000 TPUv7** <unk> $10 billion** <unk>
<unk> Phase III, <unk> GCP+ Direct Purchase Mixed <unk> 600,000 ~ $42 billion RPO <unk>
** Total** <unk> ** ** Close to 1 million TPU** ** $50 billion + ** ** **

Source: [Bloomberg 2026-04-06] (https://www.bloomberg.com/news/articles/2026-04-06/broadcom-confirms-deal-to-ship-google-tpu-chips-to-anthropic), [Anthropic Official] (@Amsym)https://www.anthropic.com/news/google-broadcom-partnership-compute)

**Meta - Second external client**:
- Lease of TPU through Google Claude in 2026 (contracted)
- Negotiations for direct purchase of TPUs in 2027 for a data centre at Meta

Source: [Dataconomy 2026-02] (https://dataconomy.com/2026/02/27/meta-signs-multibillion-dollar-deal-to-rent-google-tpus-for-ai-training/)

# Why does Google want to sell now?

**TorchTPU** led PyTorch to run on TPU - a significant drop in the migration threshold
**Broadcom addressing manufacturing and marketing** — Google design only, Broadcom is responsible for manufacturing and selling
** Economic Motivation**: The Anthropics changed from cost centre to profit centre for $50 billion plus contract
4. **Competition strategy**: Help NVIDIA clients to escape from NVIDIA and to do all three things (earning money + weakening their rivals + tied to Google Chip Ecology)

# # The impact on NVIDIA pricing

Previously, TPU was locked inside Google = there was no market competition for NVIDIA. TPU is now a purchaseable commodity = ** a direct customer and order for NVIDIA **.

♪ Before, after, after ♪
|------|------|
<unk> Clients want to buy AI chips <unk> only NVIDIA <unk> NVIDIA ** or **Google TPU (through Broadcom) <unk>
The NVIDIA can make any price.
♪ The right to price comes from a monopoly ♪

** But pricing rights do not disappear overnight** - TPU capacity is limited (Broadcom/Team bottlenecks), relocation costs are real, NVLink still has technical substitutes and small and medium-sized customers do not buy TPUs.

> **Buffett perspective**: NVIDIA was previously ** toll bridge** (the only road, random pricing); then ** to the best bridge** (and other bridges, but I'm quick to reach the widest). The best bridge is still a good business, but it should not be valued in the same number as a toll bridge.

---

# Eleven, confidence and limitations of data

<unk> Data type <unk> Confidence <unk> Description <unk>
|---------|-------|------|
NVIDIA financial reporting figures (morigin rate, revenue collection, customer concentration)
<unk> TPU Ironwood specification <unk> <unk> Google official release <unk>
♪ The price of a Trainium2 ♪
♪ Broadcom AI Income ♪
Market share estimates
<unk> 3/5/10 share projection <unk> Analyst estimates, very divergent
The Maia 200 performances, the performance, the performance, the ability to make the records, the ability to make them public.
<unk> AMD vs NVIDIA Cost Comparison <unk> Mixed open pricing and industry estimates <unk>

---

* The present report is based on public available information available on 19 April 2026, all entities are identified.(Engineer) Invelda-research-20260413.mdCross-reading*.
