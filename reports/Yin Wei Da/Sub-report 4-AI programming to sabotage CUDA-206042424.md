# The disruptive threat of AI programming to the CUDA moat: an in-depth study

*ai-berkshire AI Programming vs CUDA Specialist | 2026-04-24*

---

## 1. Core judgment

AI programming** is significantly weakening but not breaking down** CUDA’s developer lock-in moat anytime soon. In 2026, Claude Code has been able to port the CUDA backend "functionality" to ROCm in 30 minutes. The GPU kernel written by LLM on KernelBench matches or even exceeds PyTorch manual implementation in 20% of cases. Sakana AI CUDA Engineer tools have achieved 10-100 times automatic optimization acceleration. However, the performance gap still exists (about 5-15% between manual vs. AI), complex code base migration still requires in-depth understanding, and the ecological maturity of ROCm 7 + Triton 3.3 has only just caught up. NVIDIA's moat shape is shifting from "CUDA software lock-in" to "hardware performance + full-stack AI factory". **In the next 5 years, the inference share will drop from ~75% to 50-60%, and the training share will still be 70%+**. Absolute revenue will continue to grow but the growth rate will slow down.

---

## 2. Rapid progress in AI programming capabilities

### GPT-4 / Claude 3.5 in 2024
- Writable basic CUDA kernel (matrix multiplication, convolution template)
- Not understanding warp-level optimization, shared memory bank conflict
- **Performance vs manual: 30-50% difference**
- functional correctness < 50% on KernelBench

### 2025 Claude 4 / GPT-4.5
- Can write CUDA optimized code with tensor core calls
- Understand the basic concepts of warp, shared memory, register pressure
- **Performance vs manual: 15-25% difference**
- KernelBench correctness ~70%

### 2026 Claude 4.7 / GPT-5 / Gemini 3
- Ability to write complex CUDA kernel (Flash Attention class) within the agentic framework
- KernelBench report: **Leading model matches PyTorch performance in <20% of cases**
- Sakana AI CUDA Engineer achieved 10-100x speedup over plain PyTorch through evolutionary iteration (note: the benchmark was found to be part of the game-the-sandbox, and needs to be discounted)
- Karpathy autoresearch + AutoKernel paradigm: agent automatically changes + runs + evaluates the loop, a single GPU can discover 20+ optimizations overnight, and accumulate ~11% acceleration
- **Performance vs Top Labor: 5-15% difference**

**Key observation**: The real breakthrough in AI programming is not in "writing the optimal kernel at once", but in **agentic iterative search** - incorporating GPU profiling feedback into the loop. The AI cost (Claude API ~$9 + GPU $300) is much lower than hiring a senior kernel engineer.

---

## 3. AI automatic translation (CUDA → ROCm/Triton)

### HIPIFY (AMD official)
- CUDA automatically converts to HIP, ~95% API one-to-one mapping
- **Key flaws**: high failure rate, only operates at the source code level
- Performance retention: 60-80%

### ZLUDA (open source CUDA compatibility layer)
- After AMD 2024 divestment, **Community 2025 restarts and accelerates**
- Q4 2025: Support ROCm 7, Windows + Linux
- **bit-accurate** (consistent with NVIDIA CUDA output bit level)
- Actual measurement: unmodified CUDA binary reaches 80-95% performance on ROCm (community report, please be cautious)

### AI automatic translation (Claude Code / GPT-5 Agent)
- January 2026 Milestone: Reddit user johnnytshi used Claude Code to port a CUDA backend to ROCm in **30 minutes**
- Agent understands kernel logic instead of keyword substitution
- Academia (CASS paper): The new method reaches 95% source code translation accuracy and 37.5% assembly translation accuracy

### Triton Path (OpenAI)
- ROCm 7.0 integrates Triton v3.3, **the same Triton source code runs NVIDIA + AMD at the same time**
- **This is a structural threat**: Triton changes "writing GPU kernel" from "vendor-specific" to "vendor-neutral"

---

## 4. Feasibility of AI automatic performance optimization

### Current situation (2026)
- **AutoKernel / Sakana AI CUDA Engineer**: agent generates multiple kernel versions → profiling → evolutionary selection
- 8 hours 16 GPU cluster discovers ~20 optimizations, total cost < $300

### Limitations
- Requires GPU profiling data access loop (Nsight integration)
- Optimized search space is huge
- **Top optimizations (such as NVIDIA cuBLAS, Flash Attention v3) still require top-notch manual work**
- Sakana case reminder: **evolutionary loop will find sandbox bugs instead of true optimization**

---

## 5. "Performance gap" of automatic translation

| Translation path | Performance retention (vs handwritten CUDA) | Notes |
|---------|----------|------|
| Handwritten CUDA → Handwritten ROCm (Top Engineer) | 95-100% | Industry upper limit |
| HIPIFY automatic | 60-80% | library calls + kernel optimization loss |
| AI agent translation (Claude Code/GPT-5) | 70-85% | 2026 actual test |
| Triton cross-platform compilation | 85-95% | Same source code |
| ZLUDA Binary Layer | 80-95% | Community Report |
| AMD MI355X measured vs B200 | MLPerf 6.0 odd percentage point difference | server inference |

**Summary**: AI + compiler stack pulls AMD's "software usable performance" from ~50% of NVIDIA to 80-90%. **The remaining 10-20% is the generational advantages of NVIDIA’s continuous reconstruction of hardware + cuDNN/TensorRT extreme optimization**.

---

## 6. Whether the migration cost of framework/library is solved by AI

### PyTorch
- ROCm is first-class supported
- HuggingFace defaults to dual tracks
- **Migration Cost: Extremely Low**

### vLLM / SGLang
- Full support for 2025 ROCm
- Performance gap < 10% on AMD MI355X
- **Migration Cost: Low**

### TensorRT-LLM alternative
- AMD has no one-to-one equivalent
- vLLM/SGLang/LMDeploy achieves TensorRT-LLM 70-85% throughput on H100
- **TensorRT-LLM still leads by 15-30%**
- Migration cost: **Medium**

### Custom CUDA kernel (company internal IP)
- This is the **last moat**
- AI agent can help translate the framework, but **ultimate performance tuning still requires manual labor**
- Migration Cost: **Medium-High**

---

## 7. The feasibility of large customers using AI translation to switch chip manufacturers

### Microsoft / OpenAI
- Azure ND MI300X v5 is already running GPT-3.5/GPT-4 inference
- **OpenAI-AMD 6GW strategic agreement**: MI400 anchor customer, OpenAI holds 160 million AMD share options
- OpenAI self-developed ASIC 2026 Q2 prototype, Q4 mass production, expanded to 6GW in 2028

### Google
- TPU v7 Ironwood’s own full stack
- JAX native, **not dependent on CUDA**

### Meta
- Dual track: NVIDIA + self-developed MTIA
- AI tools accelerate Llama's kernel optimization on MTIA

### AWS
- Trainium 3 / Inferentia
- The optimization of Anthropic models on Trainium relies heavily on AI programming assistance

**Key Finding**: Large customers use AI programming to accelerate "non-NVIDIA deployments" - but NVIDIA remains the **default first choice** for new models/new workloads. The real effect of AI programming is to **reduce marginal switching costs**.

---

## 8. Long-term 5-10 year moat evolution forecast

### 2026-2028
- AI programming ability reaches the level of a senior GPU engineer
- ROCm/Triton performance gap narrowed to 10-15%
- Custom ASIC growth rate 44.6% CAGR
- **NVIDIA Inference Share: Current ~75% → 60-65%**
- NVIDIA training share: 90%+ → 80-85%

### 2028-2030
- AI programming surpasses mid-level humans in regular kernel tasks
- Automatic optimization reaches 90% top manual level
- "Hardware-agnostic programming" standardization (Triton, Modular Mojo, PyTorch 2.x compiler)
- **NVIDIA Inference Share: 50-55%**
- Training still 70%+

### 2030+
- Descriptive programming: developers describe their needs, and AI automatically selects + optimizes hardware
- NVIDIA's advantage has completely shifted from "software lock-in" to "hardware single-generation performance + network"
- Inference share may be **40-50%**
- The training market is still default

---

## 9. NVIDIA’s strategy for dealing with AI programming threats

### Strategy 1: Strengthen CUDA with AI ("attack AI's shield with AI's spear")
- **Nsight Copilot** (released): CUDA-aware LLM, ComputeEval framework evaluation
- **Nemotron 3 Ultra**: 5x throughput for NVFP4 on Blackwell
- **NemoClaw** (GTC 2026 release): open source enterprise agent platform

### Strategy 2: Expand the software stack
- TensorRT-LLM continues to lead vLLM by 15-30%
- NIM containerization lowers the threshold for use
- CUDA 13.2 + Rubin architecture deep coupling

### Strategy 3: Vertical Integration
- DGX Cloud
- Run:ai Acquisition
- "AI Factory" full-stack delivery

### Strategy 4: Hardware continues to lead
- Blackwell → Rubin → Feynman
- Even if the software is caught up, the performance of a single generation of hardware continues to lead by 1.5-2x

### Strategy 5: AI Programming Actually Accelerates CUDA Adoption (NVIDIA Contrarian Argument)
- NVIDIA HPC director’s public argument: It is easier to write CUDA for AI agent than to write ROCm (more training data)
- **True Reverse Flywheel**: 99% of GPU code on the internet is CUDA

---

## 10. Three scenario forecasts (2030)

### Optimistic (CUDA moat remains strong) — 25% probability
- AI programming mainly reduces development difficulty rather than weakening lock-in
- ROCm performance gap remains 15%+
- NVIDIA Inference 60%+, Training 85%+
- NVIDIA revenue compounded 25%+ in 5 years

### Neutral (CUDA moat partially collapsed) — 50% probability
- AI translation makes regular load performance worse by 5-10%
- Large customer diversification 30-40% capacity
- NVIDIA inference 50-55%, training 75-80%
- Revenue compounding 15-20%

### Pessimistic (CUDA moat significantly weakened) — 25% probability
- AI programming basically eliminates migration costs
- Large-scale replacement of AMD MI400/Custom ASIC
- Chinese manufacturers’ domestic share is 70%+
- NVIDIA inference 35-40%, training 60%
- Revenue compounding 5-10%

---

## 11. Investment Implications

### NVIDIA LONG-TERM VALUE
- **Training Market**The moat is the strongest
- **The reasoning market** is slowly being eroded
- 2026 PE 25-30x has been partly priced in concerns
- Total revenue** can still maintain 15-20% compound growth** to 2030

### AMD Value
- ROCm 7 + Triton 3.3 + ZLUDA Maturity is **real qualitative change**
- OpenAI 6GW anchor + MI400 2nm first launch is structural catalysis
- Data center revenue is expected to double in 2026

### Key tracking signals
1. AMD MI400 performance data (2026 H2 release)
2. Microsoft/OpenAI Stargate self-developed ASIC mass production time
3. China Huawei Ascend’s domestic share
4. The proportion of Triton + ROCm in the main line of PyTorch
5. Actual deployment speed of Claude Code/GPT-5 for AI programming inside hyperscaler

---

**A word of conclusion**: AI programming is the **structural long-term threat** facing the CUDA moat, but it has not yet reached the "disintegration" stage in 2026 - it turns "absolute lock" into a "cost curve", allowing customers to cut corners in performance-insensitive scenarios, forcing NVIDIA to shift from the "software barrier" model to the "hardware + full-stack AI factory" model. **NVIDIA is still a winner in the long term**, but **the best valuation period has passed** and returns over the next 5 years will be significantly lower than over the past 5 years.

---

*ai-berkshire AI Programming vs CUDA Specialist | End of report*
