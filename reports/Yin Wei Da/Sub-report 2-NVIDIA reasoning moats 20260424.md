#In-depth study of NVIDIA inference market moat

*ai-berkshire NVIDIA Reasoning Moat Specialist | 2026-04-24*

---

## 1. Core judgment

**Moat Strength: High (Data Center Inference)/Medium (Edge)/Low-Medium (China)**. NVIDIA still accounts for **60-75% share** in the AI ​​inference market (FY2026 data center revenue $194B, total market share about 86%), but it has begun to differentiate compared with training (>90%). **The deepest moat comes from 18 years of software stack accumulation of CUDA + TensorRT-LLM + NIM** - the software stack contributes 2.6-10x performance gap on the same hardware. In the next three years, it will face a triple attack: AMD MI355X overtakes in TCO, ultra-large customer ASIC (Maia/TPU/Trainium/MTIA) is increasing at a 44.6% growth rate, and Huawei Ascend has climbed from 35% to 50%+ in China. **Expect NVIDIA 2030 inference share to drop to 50-55%, but still double absolute revenue**. The $20B acquisition of Groq (2025-12) is a key step in its defense against ASIC threats.

---

## 2. Panorama of NVIDIA inference products

### Data center reasoning (core battlefield)

| Products | Video Memory | FP8/FP4 Computing Power | Price | Positioning |
|------|------|------|------|------|
| H100 SXM | 80 GB HBM3 | 4 PFLOPS FP8 | $30-40k | General purpose training + inference |
| H200 | 141 GB HBM3e | 4 PFLOPS FP8 | $35-45k | Inference optimization (double the memory) |
| H20 (Special for China) | 96 GB | Castrated version | $12-15k | 2025 has been restricted by a new round |
| B200 | 192 GB HBM3e | 9 PFLOPS FP8 / 18 PFLOPS FP4 | $35-45k | Inference 4x H100 (Llama 70B) |
| GB200 NVL72 | 13.5 TB system memory | 720 PFLOPS FP8 / 1.4 EFLOPS FP4 | $3-3.5M/cabinet | **Trillion parameter inference 30x H100** |
| B300 / Blackwell Ultra | 288 GB | ~12 PFLOPS FP8 | $45-50k | 2025 Q4 mass production |
| Rubin (R100) | HBM4 | ~50 PFLOPS FP4 | TBD | 2026 H2 shipping |
| Rubin Ultra NVL576 | 365 TB/cabinet | **15 EFLOPS FP4** | TBD | 2027 H2, 600kW Kyber Cabinet |

**Key technical inflection points**: FP4 precision (introduced by Blackwell) doubles the inference computing power compared to FP8; the NVL72 NVLink domain allows trillion-parameter models to reside in a single cabinet in the video memory.

### Edge/Device-side reasoning

- **Jetson Thor (2025 mass production)**: Blackwell architecture, 2070 FP4 TFLOPS, 128 GB VRAM, 40-130W
- **Jetson T4000 + JetPack 7.1** (2026-01): Edge LLM/VLM/VLA inference
- **DGX Spark** (personal AI workstation, available in 2025)
- **2M+ robot developers** bound to NVIDIA Isaac/Holoscan software stack

---

## 3. NVIDIA inference software stack (deepest moat)

### TensorRT（2017）
Universal GPU inference optimizer, FP8/FP4 quantization, Kernel fusion, dynamic shapes. Performance is 5-10x better than PyTorch native.

### TensorRT-LLM（2023-09）
Designed specifically for LLM: In-flight batching, Paged KV cache, Speculative decoding, multi-GPU tensor/pipeline parallelism. Supports 100+ mainstream models.

### Triton Inference Server
Multi-model and multi-framework (PyTorch/TF/ONNX/TRT-LLM/vLLM) unified services.

### NIM（NVIDIA Inference Microservices，2024-03）
**The most important recent products**: containerization, one-line command deployment, including TensorRT/TensorRT-LLM/vLLM/SGLang multiple backends.
- **2025-12 data: NIM on H100 Llama 3.1 8B ran 1,201 tokens/s, compared to naked running 613 tokens/s (2.6x improvement)**
- AWS / Google Cloud / Azure are all available
- Enterprise customers: Lowe's, Siemens, Box, Cohesity, Dropbox, NetApp, Hippocratic AI, Glean

**Moat logic**: CUDA → TensorRT → TensorRT-LLM → NIM forms an upward "performance + ease of use" flywheel. **The same NVIDIA software stack on H100 hardware makes the effective computing power 2-3 times higher than competing products**.

---

## 4. Five dimensions of NVIDIA reasoning moat

### 4.1 Hardware performance leadership (medium moat)
- B200 vs MI300X: 9 PFLOPS vs 5.2 PFLOPS on FP8 (1.7x)
- GB200 NVL72 vs any competing product: 72 GPU NVLink fully interconnected, trillion parameter inference 30x H100
- But AMD MI355X is already on par with B200 on FP8/FP4

### 4.2 Mature software stack (deepest moat)
- TensorRT has been iterating for 18 years, and TensorRT-LLM has been iterating 30+ versions in 13 months.
- vLLM CI data: AMD ROCm's vLLM test pass rate in 2025-11 was 37%, and increased to 93% in 2026-01
- Batch size 1-4 (low latency) H100 + TRT-LLM has 20-30% higher throughput than MI300X + vLLM

### 4.3 Model Ecology (High Moat)
HuggingFace defaults to NVIDIA, and all head open source models are first optimized for NVIDIA.

### 4.4 Customer inertia + installed base (high moat)
5M+ Hopper and 1M+ Blackwell GPUs have been deployed globally. **Switching cost: Millions of dollars per year. Migrating inference workloads to ROCm usually takes 6-12 months and results in a performance loss of 10-30%**.

### 4.5 Supply chain advantages (medium moat)
TSMC 4N/3nm priority production capacity, HBM3E/HBM4 SK Hynix and Samsung dual supply, CoWoS occupies 70%+ of global production capacity.

---

## 5. NVIDIA vs AMD real comparison of inference cost performance

| Indicators | H100 SXM | MI300X | B200 | MI355X |
|------|------|------|------|------|
| Video Memory | 80 GB HBM3 | 192 GB HBM3 | 192 GB HBM3E | 288 GB HBM3E |
| FP8 computing power | 4 PFLOPS | 5.2 PFLOPS | 9 PFLOPS | ~9 PFLOPS |
| FP4 computing power | N/A | N/A | 18 PFLOPS | ~18 PFLOPS |
| Whole machine price | $30-40k | $15-20k | $35-45k | $25-30k |
| Software stack | CUDA + TRT-LLM | ROCm + vLLM | CUDA + TRT-LLM | ROCm + vLLM |
| Batch 1-4 Cost per token | Baseline 1.0x | 0.85-0.95x | 0.5x | 0.45-0.55x |
| Batch 64+ Cost per token | Baseline 1.0x | 0.65-0.75x | 0.5x | **0.35-0.45x** |
| Tokens / megawatt | Benchmark | 1.5x | 2.5x | **3x** |

**Conclusion**:
- TensorWave 2026 actual measurement: MI355X continues to have better TCO than NVIDIA GPUs of the same level in vLLM workloads
- AMD’s 30-40% cost per token advantage offsets the 10% latency disadvantage
- But NVIDIA is still 20-30% ahead in the "Batch 1-4 low latency + multi-model + complex scheduling" scenario

---

## 6. NVIDIA vs inference dedicated chip

### Groq LPU
- Llama 2 70B runs 300 tokens/s, 10x faster than H100 single card
- **2025-12 NVIDIA $20B acquisition of Groq** (2.9x valuation premium), integrated into LPX rack (2026-03 release)

### Cerebras WSE-3
- Whole wafer, Llama 3.1-405B runs 1,000+ tokens/s
- **2026-04 OpenAI $20B procurement Cerebras** - the first large customer outsourcing

---

## 7. NVIDIA’s four strategies to deal with ASIC threats

### Strategy 1: Annual iteration rhythm
H100（2022）→ H200（2024）→ B100/B200（2024）→ B300（2025 Q4）→ Rubin R100（2026 H2）→ Rubin Ultra NVL576（2027 H2）→ Feynman（2028）

### Strategy 2: Attract ASIC players into the ecosystem
- 2025-12 Acquire Groq ($20B) and integrate LPX rack
- Cooperate with Broadcom on "NVIDIA Custom GPU" product line (NVL Custom Silicon)

### Strategy 3: Vertical integration + software lock-in
- Run:ai acquisition (GPU scheduling)
- DGX Cloud across Microsoft/Google/AWS/Oracle
- NIM standardized inference deployment

### Strategy 4: Enter the full-stack AI factory
DGX SuperPOD + NVL72/576 + Spectrum-X Network + BlueField DPU + Mission Control Software

---

## 8. Real data on the "dual-track" strategy of major customers

| Customers | 2025 NVIDIA purchases ($) | Self-developed chips | NVIDIA’s share of AI computing power | 2027 Trends |
|------|------|------|------|------|
| Microsoft | $50B+/year | Maia 100/200 | 60-70% | Down to 50-60% |
| Google | $5-10B/year (less) | TPU v7 Ironwood, 2026 shipped 4.3M pieces | 10-15% | Down to 5-10% |
| AWS | $20B+/year | Trainium 3 UltraClusters | 50-60% | Down to 40-50% |
| Meta | $40B+/year | MTIA 300/400/v3 (TSMC N3, 2026) | 60-70% | Down to 50-60% |
| OpenAI | Close to 100% | Titan / Broadcom (10 GW in 2026 H2) | 100% → 50% | Long term 50% |

**Key Findings**:
- The total ASIC production capacity of very large customers will increase by 44.6% in 2026, compared with 16.1% for GPU - the inflection point has been reached
- Bernstein/MS estimates that in-house ASICs will account for 40-45% of inference workloads in 2030
- But in terms of absolute volume: Very large customers continue to place additional NVIDIA orders - "dual-track" ≠ "replacement"

---

## 9. Impact on the Chinese market (Huawei Ascend)

### Current status (2026-04)
- Bernstein estimates: NVIDIA China’s AI chip share 2024 = 66% → 2025 = 54% → 2026 = 8%
- H20 will also be subject to a new round of restrictions in 2025
- Huawei Ascend 910C 2026 production target 600k pieces
- Ascend 910C inference performance = ~60% of H100; BF16 = 1/3 of B200
- Ascend 950PR (released in 2026-03): FP4 computing power is 2.87x that of H20
- 2026-04 China AI chip market: local manufacturers account for 41%

### Customer List
DeepSeek, Byte, Alibaba, Baidu, Tencent, and Huawei Cloud switched to Ascend in large numbers.

### Impact
- NVIDIA China data center revenue may drop from ~25% data center share in 2024 to 5-10% in 2026
- CUDA software barriers are being copied by MindSpore/CANN in China, but the ecosystem is still weak

---

## 10. Three-scenario forecast (2030 reasoning market)

| Scenario | Global Inference Market Size | NVIDIA Share | AMD | Very Large Customer ASIC | China Local | Long Tail |
|------|------|------|------|------|------|------|
| Optimistic | $300B+ | **60-65%** | 15% | 15% | 5% | 5% |
| Neutral | $250B | **45-50%** | 15-20% | 20-25% | 100% China | 5-10% |
| Pessimistic | $200B | **30-35%** | 20% | 30%+ | China full replacement | 10-15% |

**ai-berkshire neutral judgment**:
- NVIDIA 2030 Inference Share **45-50%** (Data Center) + 70%+ (Edge/Jetson)
- **Absolute revenue still doubles**: From 2025 inferred revenue ~$45B to 2030 ~$100-120B
- **Core profit margin** will be compressed: gross profit drops from current 75% to 65-70%
- Software + services revenue share increased from 5% to 15-20%

---

## 11. Investment Implications (Buffett’s Perspective)

**Moat Depth Ranking**: Software Ecology > Customer Inertia > Model Ecology > Hardware Performance > Supply Chain. **The software stack is the true cornerstone of NVIDIA's valuation** - 1-2 years ahead in hardware performance and 3-5 years ahead in software performance.

**Risk Points**:
1. Super large customer ASICs will increase their volume in 2027-2028
2. If AMD MI400 series pushes ROCm/vLLM to 100% TRT-LLM parity
3. The Chinese market is basically permanently lost
4. Price elasticity has emerged: B200 discounts enter cloud customer contracts

**Conclusion**: NVIDIA's status as the "leader in AI inference infrastructure" will be maintained until at least 2028-2029. **Vera Rubin / Rubin Ultra is key to watch** - If the 2027 H2 Rubin Ultra lands on time and performs as expected, the moat could be extended for another 3 years.

---

*ai-berkshire NVIDIA Reasoning Moat Specialist | End of report*
