# A Review of Foundation Model Training Methodologies for 2025-2026: From DeepSeek V4 to Kimi K2.5

## 1. Introduction

2025-2026 were the two years in which the competitive landscape of foundation models changed structurally. If 2024 was about "the rise of MoE and open-source catch-up," then 2025-2026 is about "faster architectural divergence, a sharp shift in post-training paradigms, and agent capability becoming a core competitive dimension."

**Global landscape**: Anthropic's Claude family continued to dominate the top tier, with Claude Opus 4.8 taking first place on LMArena by a wide margin; OpenAI's GPT family remained highly competitive; Google's Gemini family kept pushing hard in multimodal directions. The capability ceiling of leading closed models kept rising rapidly.

**Domestic landscape**: Competition was even fiercer than expected. DeepSeek V4 pioneered a new "distillation instead of RL" paradigm with its CSA/HCA dual-attention mechanism and OPD online policy distillation; Qwen 3 reset expectations for training efficiency with extremely minimal RL (only 3,995 queries and 170 steps to substantially improve math reasoning); Kimi K2/K2.5 built a unique moat in agent training; GLM-5 differentiated itself through domestic-chip adaptation and asynchronous agent RL infrastructure; MiniMax M3's MSA sparse attention achieved a 28.4x reduction in attention computation; Hunyuan TurboS boldly adopted a Mamba-Transformer hybrid architecture; Step 3.5 Flash and MiMo-V2-Flash each carved out their own niches in the small-model segment.

**Latest LMArena ranking** (as of June 2026): Claude Opus 4.8 ranked first, GPT models followed, Qwen 3.7 ranked fifth, and domestic models as a whole had entered the global top tier. This ranking reflects two trends: first, top closed models still command a capability premium; second, domestic open-source models have become genuinely competitive with the world's best closed models.

**Models covered in this article**: DeepSeek V4 Pro/Flash, Qwen 3, Kimi K2, Kimi K2.5, GLM-5, MiniMax M3, Hunyuan TurboS, Step 3.5 Flash, MiMo-V2-Flash, 9 model families in total.

**Technical sources**: The official Technical Reports and arXiv papers for the models above, with uneven levels of detail. DeepSeek V4, GLM-5, and Qwen 3 have the most detailed reports; MiniMax M3 and Step 3.5 Flash come next; Hunyuan TurboS and MiMo-V2-Flash are moderately detailed; Kimi K2/K2.5 are the richest sources on agent training.

---

## 2. Model Overview

### 2.1 Overview Table

| Model | Total Params / Active Params | Architecture | Layers | Expert Configuration | Training Data | Attention Mechanism | Key Innovations | Detail Level |
|------|---------------|---------|------|---------|-----------|-----------|---------|-----------|
| **DeepSeek V4 Pro** | 1.6T/49B | MoE | 61 | 384 routers + 1 shared, Top-6 | 33T | CSA + HCA | mHC manifold constraint, OPD distillation replacing RL, FP4 quantization-aware training | ★★★★★ |
| **DeepSeek V4 Flash** | 284B/13B | MoE | 43 | 256 routers + 1 shared, Top-6 | 32T | CSA + HCA | Same architectural innovations as V4 Pro, smaller model version | ★★★★★ |
| **Qwen 3** | 235B/22B | MoE | — | 128 routers, Top-8 | 36T | QK-Norm | Minimal RL, thinking-mode fusion, strong-to-weak distillation | ★★★★☆ |
| **Kimi K2** | 1.04T/32.6B | MoE | 61 | 384 routers + 1 shared, Top-8 | 15.5T | MLA | MuonClip zero spike, agent data synthesis pipeline | ★★★★☆ |
| **Kimi K2.5** | Based on K2 | MoE + vision | — | Same as K2 | — | MLA | Vision agent, Agent Swarm/PARL, Toggle heuristic | ★★★★☆ |
| **GLM-5** | 744B/40B | MoE | 80 | 256 routers, MLA-256 | 28.5T | DSA | IcePop, asynchronous agent RL (Slime), domestic-chip adaptation | ★★★★★ |
| **MiniMax M3** | 428B/23B | MoE | 60 | 128 routers + 1 shared, Top-4 | — | MSA | 28.4x reduction in attention computation, native multimodality | ★★★★☆ |
| **Hunyuan TurboS** | 560B/56B | Mamba-Transformer hybrid | 128 | MoE | 16T | GQA (only 7 layers) | Mamba2 linear complexity, adaptive CoT | ★★★☆☆ |
| **Step 3.5 Flash** | 196B/11B | MoE | 45 | 289 (288 routers + 1 shared), Top-8 | 17.2T | MFA + SWA hybrid | AFD decoupled parallelism, MIS-PO filtered RL | ★★★★☆ |
| **MiMo-V2-Flash** | 309B/15B | MoE | 48 | 256 routers, Top-8 | 27T | SWA + GA hybrid | MOPD multi-teacher distillation, R3 routing consistency, MTP speculative decoding | ★★★★☆ |

### 2.2 Key Takeaways

Several core signals stand out from the overview table:

1. **MoE has become the overwhelming consensus**: among the 9 model families, only Hunyuan TurboS uses a Mamba-Transformer hybrid architecture; the other 8 all use MoE. Dense architectures have completely disappeared from next-generation flagship models.
2. **Parameter growth and restrained active parameters coexist**: total parameters range from 196B to 1.6T, but active parameters are generally kept between 11B and 56B, reflecting a shared pursuit of "large capacity, low inference cost."
3. **Training data scale has reached the 15T-36T range**: Qwen 3 leads with 36T tokens, closely followed by DeepSeek V4 at 33T. Data competition has entered the "tens of trillions of tokens" era.
4. **Each model introduces distinctive attention innovation**: from CSA/HCA to MSA, DSA, and MFA, attention innovation is the most clearly differentiated technical dimension in this round of competition.

---

## 3. Pretraining

### 3.1 Architectural Evolution

#### 3.1.1 MoE Has Become the Clear Mainstream

Among the 9 model families covered in this article, 8 use MoE architecture. Compared with 2024, when only a small number of models such as DeepSeek V3 and Qwen 2.5 MoE were early pioneers, this is a qualitative shift. The core advantage of MoE is that it uses a relatively small number of active parameters (11B-56B) to unlock a huge total parameter budget (196B-1.6T), achieving an optimal balance between inference cost and model capability.

Notable differences in detail:

| Model | Total Experts | Shared Expert | Active Experts | Special Design |
|------|---------|---------|-----------|---------|
| DeepSeek V4 Pro | 384 routers | 1 shared | Top-6 | — |
| DeepSeek V4 Flash | 256 routers | 1 shared | Top-6 | — |
| Qwen 3 | 128 routers | None | Top-8 | Shared expert removed |
| Kimi K2 | 384 routers | 1 shared | Top-8 | Dense in the first layer, MoE in the remaining 60 layers |
| GLM-5 | 256 routers | — | — | MLA-256 + Muon Split |
| MiniMax M3 | 128 routers | 1 shared | Top-4 | — |
| Step 3.5 Flash | 288 routers | 1 shared | Top-8 | 3 dense layers + 42 MoE layers |
| MiMo-V2-Flash | 256 routers | None | Top-8 | No shared expert |

One interesting point of divergence is the **presence or absence of shared experts**: Qwen 3 and MiMo-V2-Flash chose to remove shared experts, arguing that increasing the number of routed experts is more effective than retaining a small number of shared experts; DeepSeek V4, Kimi K2, MiniMax M3, and Step 3.5 Flash kept one shared expert. This design choice is still unresolved.

**Hunyuan TurboS's outlier path** deserves special discussion. It uses a 128-layer Mamba-Transformer hybrid architecture: 57 Mamba2 layers + 7 attention layers + 64 FFN/MoE layers, arranged into alternating AMF (Attention-Mamba-FFN) and MF (Mamba-FFN) blocks. Across all 128 layers, only 7 are attention layers, or 5.5%. The core bet of this aggressive design is that Mamba2's O(n) linear complexity can deliver a fundamental efficiency advantage in long-sequence settings, at the cost of needing a very small number of attention layers to compensate for Mamba's limitations in exact position retrieval. Given LMSYS Arena rank #7 and a score of 1356, this architecture is clearly viable, but whether it is better than a pure Transformer + MoE stack still needs more evidence.

#### 3.1.2 Attention Innovation: A Richly Divergent Landscape

In this round of model competition, attention innovation is the most exciting technical dimension. Different teams approached the problem from different angles and proposed their own sparse-attention schemes.

**DeepSeek V4's dual CSA + HCA mechanism**

On top of MLA (Multi-head Latent Attention, first introduced by DeepSeek V2), DeepSeek V4 proposed two complementary attention mechanisms:

- **CSA (Compressed Sparse Attention)**: every m = 4 adjacent token KV pairs are compressed into one via a learnable linear layer, and then a lightweight "Lightning Indexer" performs top-k sparse selection on the compressed KVs (k = 1024 for V4 Pro). This means that in a 1M context, the number of tokens actually participating in attention is compressed from the million scale down to the thousand scale.
- **HCA (Hierarchical Compressed Attention)**: uses a higher compression ratio (m' = 128) but does not perform sparse selection; instead, it applies full dense attention to all compressed KVs. This preserves global information integrity.

CSA and HCA are used alternately across Transformer layers, forming a complementary pattern of "locally precise selection + globally coarse coverage." The inference efficiency gains are substantial: V4 Pro's KV cache is only 10% of V3's, and FLOPs are only 27% of V3.2's.

**MiniMax M3's MSA (Mixed Sparse Attention)**

MSA uses a dual-branch design:
- **Index branch**: a lightweight selector quickly determines which KV blocks are relevant to the current query
- **Main branch**: performs exact block-sparse attention over the selected KV blocks

Concrete settings: block size 128, 16 blocks selected per query. In a 1M context, attention computation is reduced by 28.4x, prefill is accelerated by 9x, and decoding is accelerated by 15x. The associated GPU kernel optimizations include exponent-free Top-k (2.5-5.1x faster than `torch.topk`) and a KV outer-loop kernel.

**GLM-5's DSA (Dynamic Sparse Attention)**

DSA stands out because of its extremely low adaptation cost: it only takes 20B continued-training tokens to migrate from full attention to sparse attention, compared with DeepSeek V4's 943.7B-token from-scratch training cost. DSA uses deterministic top-k selection, avoiding the training instability that randomization can introduce.

**Step 3.5 Flash's MFA + SWA hybrid**

Step 3.5 Flash combines sliding-window attention (SWA) and global attention in a 3:1 ratio (3 SWA layers, 1 global layer every 4 layers). The SWA window size is 512 tokens. Its distinctive feature is **head-level gated attention**: each attention head can learn its own gating weights to decide the mixing ratio between SWA and global attention.

**MiMo-V2-Flash's SWA + GA hybrid**

MiMo-V2-Flash also mixes SWA with global attention, but with a more extreme ratio: 5:1 (39 SWA layers and 9 GA layers out of 48). The SWA window is only 128 tokens, the smallest window among all models. To prevent attention collapse caused by such a small window, MiMo introduces a **learnable sink bias**: a learnable bias is added to specific positions such as the BOS token, allowing the model to dump "garbage attention" onto sink tokens and avoid attention-weight degeneration.

**Hunyuan TurboS's extreme design**

Only 7 of its 128 layers are attention layers (GQA, 64 Query / 8 KV heads); the rest are all Mamba2 and FFN/MoE. Mamba2 uses d_state = 128 and chunk_size = 128, delivering O(n) linear complexity. This is the lowest attention-layer ratio among all models.

**Summary of attention innovation**

| Model | Scheme | Core Idea | Compression / Sparsity Ratio | Adaptation Cost |
|------|---------|---------|-------------|---------|
| DeepSeek V4 | CSA + HCA | Compression + top-k selection / high compression + dense | KV cache only 10% of V3 | From-scratch training |
| MiniMax M3 | MSA | Index branch + block-sparse dual branch | 28.4x reduction in attention computation | From-scratch training |
| GLM-5 | DSA | Deterministic top-k | — | Only 20B token adaptation |
| Step 3.5 Flash | MFA + SWA 3:1 | Head-level gated mixing | — | From-scratch training |
| MiMo-V2-Flash | SWA + GA 5:1 | Very small window + sink bias | — | From-scratch training |
| Hunyuan TurboS | Mamba2 + GQA | Linear complexity + very sparse attention | O(n) linear | From-scratch training |

#### 3.1.3 mHC Manifold-Constrained Hyper-Connection

DeepSeek V4's **mHC (manifold-constrained Hyper-Connection)** is a fundamental redesign of residual connections. The problem with a traditional residual connection (y = x + f(x)) is that as depth increases, the contribution gradients from different layers to the final output can become imbalanced.

The core idea of mHC:
1. Replace residual connections with a **doubly stochastic matrix** (each row and each column sums to 1) to control the mixing weights of layer inputs and outputs
2. Enforce the doubly stochastic constraint using the **Sinkhorn-Knopp algorithm** (20 iterations) by alternately normalizing rows and columns of a learnable matrix so that it converges onto the doubly stochastic matrix manifold
3. Parameterize the matrix dynamically rather than treating it as a fixed value, so it can adapt during training

The elegance of this design lies in the fact that the doubly stochastic matrix guarantees the "conservation" of information flow, so no layer's contribution is excessively amplified or suppressed. Measurements show that mHC adds only 6.7% extra compute time, while delivering significant gains in training stability and performance for deep networks.

#### 3.1.4 MTP (Multi-Token Prediction)

MTP is widely adopted in this round of models:

- **GLM-5**: 3 shared MTP layers; average accepted length during inference is 2.76
- **Step 3.5 Flash**: 3 MTP heads, introducing **Fast-MTP position-aware loss** so that each prediction head uses different loss weights based on its predicted position (1st, 2nd, or 3rd future token)
- **MiMo-V2-Flash**: MTP speculative decoding reaches an accepted length of 3.6, delivering a 2.6x inference speedup

MTP has a dual value: it provides richer gradient signals during training by predicting multiple future tokens at each position, and it significantly improves throughput during inference through speculative decoding.

#### 3.1.5 AFD Attention-FFN Decoupled Parallelism

Step 3.5 Flash's **AFD (Attention-FFN Decoupling)** is an engineering-oriented architectural innovation. In a traditional Transformer, the attention layer and the FFN layer execute serially. AFD decouples them into parallel execution: attention and FFN are computed at the same time, and their results are merged when the layer output is produced. This reduces per-layer serial latency and makes better use of GPU parallel compute during inference.

### 3.2 Data Engineering

#### 3.2.1 Data Scale Comparison

| Model | Pretraining Data | Language Coverage | Notes |
|------|-----------|---------|------|
| Qwen 3 | 36T tokens | 119 languages | Largest data volume in this round |
| DeepSeek V4 Pro | 33T tokens | — | — |
| DeepSeek V4 Flash | 32T tokens | — | — |
| GLM-5 | 28.5T tokens | — | Five-stage training |
| MiMo-V2-Flash | 27T tokens | — | Three-stage training |
| Step 3.5 Flash | 17.2T tokens | — | — |
| Hunyuan TurboS | 16T tokens | — | — |
| Kimi K2 | 15.5T tokens | — | Two-stage training |

The competition in data scale has entered the "tens of trillions of tokens" era. Importantly, more data does not automatically mean a better model: DeepSeek V4, with 33T tokens, outperformed Qwen 3, which used 36T tokens, on several benchmarks, showing that data quality and training strategy matter at least as much as raw scale.

#### 3.2.2 Scaling Synthetic Data Usage

Synthetic data has moved from "auxiliary supplement" to "core component." The most typical examples:

- **Kimi K2's knowledge rewriting strategy**: uses a large model to rewrite raw web text into a more structured format that is better suited to training; this strategy is already used at scale during pretraining
- **Kimi K2's agent data synthesis pipeline**: starts from 3,000+ GitHub MCP (Model Context Protocol) tool repositories, synthesizes 20,000+ tool definitions, and then generates multi-turn agent interaction trajectories. This is the largest publicly described agent training data synthesis pipeline to date
- **Qwen 3's reasoning enhancement stage**: out of the 36T total tokens, 5T are reserved specifically for reasoning enhancement, including large amounts of synthetic math and code reasoning data

#### 3.2.3 Data Rewriting Strategy

One of Kimi K2's defining data-engineering traits is **knowledge rewriting**. The core idea is that raw internet text is often full of ads, navigation bars, irrelevant links, and other noise, which makes it inefficient for direct training. Kimi K2 uses a trained model to "rewrite" such text, preserving the core knowledge while reorganizing it into a format that is easier for language models to learn. The trade-off between the cost of rewriting (inference compute) and the benefit (training efficiency gains) is a question worth deeper study.

### 3.3 Training Strategy

#### 3.3.1 Long-Context Training

Long-context capability has become a standard requirement, and most models use multi-stage context expansion strategies:

| Model | Expansion Path | Final Context Length |
|------|---------|-------------|
| DeepSeek V4 | 4K → 1M (multi-stage) | 1M |
| Qwen 3 | Three stages (general 30T → reasoning enhancement 5T → long context) | — |
| Kimi K2 | Two-stage pretraining + annealing 400B + long-context 60B | — |
| GLM-5 | Five-stage pretraining | — |
| MiniMax M3 | — | 1M |
| Hunyuan TurboS | Two-stage long-context expansion | 256K |
| MiMo-V2-Flash | Three stages (general 22T → code enhancement 4T → long context 1T) | — |

The shared pattern is: first fully train the core capabilities on short sequences, then expand progressively through dedicated long-context stages. The reason is that long-sequence training is much more expensive than short-sequence training (because self-attention is quadratic), so it is more economical to build core competence early with short sequences.

#### 3.3.2 FP8 / FP4 Mixed Precision

Low-precision training was pushed further in this round:

- **DeepSeek V4**: first to introduce **FP4 quantization-aware training**, reducing MoE expert weights and the QK path of the CSA indexer to FP4 precision. This is the first report in the industry to use FP4 during pretraining, rather than only for inference quantization. Training in low precision from the start means the model learns to live with quantization error from day one.
- **Other models**: FP8 mixed precision is already standard practice and is no longer highlighted as a standalone technical novelty.

#### 3.3.3 Training Stability

Training stability is a core engineering challenge in large-scale pretraining. Innovations in this dimension are especially notable in this round:

**Kimi K2's MuonClip - zero loss spikes**

MuonClip adds a stability constraint on top of the Muon optimizer: it sets a threshold τ = 100 on the QK inner product in attention layers and clips values above that threshold. This simple but elegant design allowed Kimi K2 to achieve **zero loss spikes** during the entire 15.5T-token pretraining run - a milestone result. By contrast, most large-scale training runs go through several to dozens of loss spikes, each of which wastes time recovering from a degraded training state.

**DeepSeek V4's foresight routing + SwiGLU clamping**

DeepSeek V4 uses a two-layer stability guarantee:
1. **Foresight Routing**: decouples the updates to the MoE router and the model backbone. Under normal training, the router and backbone are updated together; when a potential loss-spike signal is detected, router updates are paused (frozen) and only the backbone is updated. This adds about 20% compute overhead, but because it is activated only when spike risk appears, the average cost is far lower than 20%.
2. **SwiGLU clamping**: clamps the output of the SwiGLU activation function to the range [-10, 10] to prevent extreme activations from propagating.

**Step 3.5 Flash's Polar Express**

Step 3.5 Flash made a specialized precision optimization for the Muon optimizer, called Polar Express, and experienced only 1 loss spike during training on 17.2T tokens.

**Summary of stability techniques**

| Model | Stability Scheme | Loss Spike Count | Extra Overhead |
|------|-----------|--------------|---------|
| Kimi K2 | MuonClip (QK-Clip τ = 100) | 0 | Very low |
| Step 3.5 Flash | Polar Express | 1 | — |
| DeepSeek V4 | Foresight Routing + SwiGLU clamping | — | About 20% (peak) |

#### 3.3.4 Optimizer: Muon Replaces AdamW

The adoption of Muon is a notable trend in this round:

| Model | Optimizer | Special Configuration |
|------|-------|---------|
| DeepSeek V4 | Muon | 10 Newton-Schulz iterations (fast first 8 + precise last 2), mixed-bucket allocation |
| Kimi K2 | MuonClip | Muon + QK-Clip stability constraint |
| GLM-5 | Muon Split | MLA-256 head splitting |
| Step 3.5 Flash | Muon + Polar Express | Precision optimization |

Muon's key advantage is that it does not rely on first- and second-moment estimates of momentum, which are the core of AdamW. Instead, it orthogonalizes gradient matrices through Newton-Schulz iterations, making better use of the geometry of gradients in theory. DeepSeek V4's implementation is especially elegant: the first 8 Newton-Schulz steps use a faster but lower-precision mode to accelerate convergence, while the final 2 steps switch to high precision to ensure orthogonalization quality; mixed-bucket allocation assigns parameter matrices to different compute buckets according to size, improving parallel efficiency.

### 3.4 Training Infrastructure and Cost

#### 3.4.1 GPU Scale and Cost Comparison

| Model | GPU Scale | Notes |
|------|--------|------|
| Step 3.5 Flash | 4,096 H800 GPUs | Explicitly disclosed |
| Other models | Not explicitly disclosed | Estimated at the 2,000-16,000 GPU scale |

GPU scale and training cost are among the least transparent aspects of most technical reports. Only Step 3.5 Flash explicitly disclosed a training scale of 4,096 H800 GPUs. But based on training data volume and model size, DeepSeek V4 Pro (1.6T parameters, 33T tokens) almost certainly trained on more than 10,000 GPUs.

#### 3.4.2 Communication Optimization

The core communication bottleneck in large-scale MoE training is All-to-All communication between experts. Each model addresses this differently:

- **DeepSeek V4**: mixed-bucket allocation and expert-parallel optimization are important sources of its training efficiency
- **GLM-5**: adaptation across domestic chips (7 hardware platforms) faces a more complex communication challenge, because interconnect topologies and bandwidth differ sharply across chips, requiring platform-specific communication strategies
- **MiMo-V2-Flash**: its R3 (Rollout Routing Replay) technique indirectly solves a communication-related issue in MoE training: during RL, rollout generation and training updates use different model versions, which leads to inconsistent routing decisions. R3 removes this inconsistency by replaying rollout-stage routing decisions during training

---

## 4. Post-Training

### 4.1 SFT Strategy

#### 4.1.1 Comparing Thinking-Mode Design

"Thinking mode" - the model performs internal reasoning before producing its final answer - has become a standard feature in 2025-2026 models. But the design philosophies vary significantly across teams:

**Qwen 3's /think and /no_think**

Qwen 3 uses the simplest binary design: users control whether the model reasons internally by adding `/think` or `/no_think` in the prompt. This is enabled by a "thinking-mode fusion" stage in post-training, where datasets with and without thinking are mixed so the same model can switch modes based on instruction.

One of Qwen 3's important findings is that **thinking budget emerges naturally**: after RL training, the model automatically learns to allocate different reasoning lengths depending on problem difficulty, without any explicit length-control mechanism.

**DeepSeek V4's three reasoning intensities**

DeepSeek V4 provides finer-grained control:
- **Non-think**: no internal reasoning, answer directly (suitable for simple questions)
- **Think High**: standard-depth internal reasoning
- **Think Max**: maximum-depth internal reasoning (for very hard math/coding tasks)

The three levels are triggered through different system prompts, and the model learns to distinguish them during OPD distillation.

**GLM-5's three modes**

GLM-5 also offers three reasoning modes, but its design is more about "scenario adaptation" than "intensity gradients" - it provides different thinking strategies for different task types, such as math reasoning, code generation, and general dialogue.

**Hunyuan TurboS's adaptive CoT**

Hunyuan TurboS is the most aggressive design: **adaptive long/short CoT** - the model decides automatically whether to use long-chain or short-chain thinking based on task difficulty, without requiring the user to switch manually. Measurements show that this strategy allows Hunyuan TurboS to achieve comparable reasoning performance using only 52.8% of DeepSeek-R1's token budget, nearly halving inference cost while preserving performance.

**Summary of thinking modes**

| Model | Mode Count | Control Method | Distinctive Feature |
|------|-------|---------|---------|
| Qwen 3 | 2 | `/think` / `/no_think` markers | Thinking budget emerges naturally |
| DeepSeek V4 | 3 | Non-think / Think High / Think Max | Three-level intensity gradient |
| GLM-5 | 3 | Scenario adaptation | — |
| Hunyuan TurboS | Adaptive | No manual switching | Uses only 52.8% of R1's tokens |

#### 4.1.2 Multi-Round Deliberative Learning

Hunyuan TurboS's **Multi-round Deliberative Learning** is a distinctive SFT strategy with three steps:
1. **Judging stage**: the model evaluates its own answer and identifies weaknesses
2. **Weakness deliberation**: the model generates an improved answer targeting the identified weaknesses
3. **Iterative SFT**: the original answer, the critique, and the improvement are used as a training triple, and SFT is repeated iteratively

The essence of this strategy is to let the model learn from its own mistakes - similar to a human "error notebook."

### 4.2 Reinforcement Learning

#### 4.2.1 GRPO Remains the Mainstream Algorithm

GRPO (Group Relative Policy Optimization, first introduced by DeepSeek) remains the most widely used RL algorithm in this round. Hunyuan TurboS explicitly reports a two-stage GRPO setup: 300,000 reasoning-stage samples + 160,000 general-stage samples.

But the more interesting developments are the improvements and replacements built on top of GRPO.

#### 4.2.2 DeepSeek V4's OPD - Distillation Fully Replaces RL

**OPD (Online Policy Distillation)** is DeepSeek V4's major post-training innovation, with a core idea of **using distillation to fully replace traditional RL**.

OPD workflow:
1. **Train domain experts independently**: train separate expert models for different domains (math, code, general, etc.), each going through a full SFT + GRPO process
2. **Merge through online policy distillation**: instead of a naive model merge such as parameter averaging, use **reverse KL divergence** to distill the full-vocabulary logit distribution - the student model (the final V4) generates samples from its own policy distribution and then matches the logit distributions of 10+ teacher models

The deeper logic is that traditional RL uses a scalar reward signal (one number that measures answer quality), whereas distillation's "reward signal" is the probability distribution over the entire vocabulary - several orders of magnitude richer in information. That explains why OPD can reach better results in fewer training steps.

Even more elegantly, DeepSeek V4 also introduces a **Generative Reward Model (GRM)**: traditional reward models are discriminative (input an answer, output a score), whereas GRM is generative (generate an evaluation text, then extract a score from that evaluation). DeepSeek V4 also **applies RL to the GRM itself**, using RL to improve the quality of reward judgments and forming a nested optimization loop.

#### 4.2.3 Qwen 3's Minimal RL

Qwen 3's RL result is one of the most surprising findings in this round:

- Only **3,995 queries** (fewer than 4,000 questions)
- Only **170 GRPO steps**
- The AIME math benchmark improved from 70.1 to 85.1 (+15 points)

This result challenges the common belief that RL requires huge data and long training. Qwen 3's team explained it as follows: if pretraining and SFT have already built a sufficiently strong base, RL is more about "activation" than "instruction" - a small amount of high-quality RL signal is enough to trigger reasoning capabilities that the model already possesses but has not fully released.

Qwen 3's post-training follows four stages:
1. **Long-CoT cold start**: use long-chain reasoning data for SFT to establish the habit of thinking
2. **Reasoning RL**: the minimal GRPO run above (3,995 queries, 170 steps)
3. **Thinking-mode fusion**: mix `/think` and `/no_think` training data
4. **General RL**: apply RL to a broader set of tasks

#### 4.2.4 GLM-5's IcePop

**IcePop** is GLM-5's solution to a long-neglected RL problem: **train-inference distribution mismatch**.

The core issue is that during RL training, the model samples from its own distribution (on-policy), while the reward model used in training is evaluated from another distribution (off-policy). As RL proceeds, the gap between the model's distribution and the reward model's training distribution grows, making the reward signal less reliable.

IcePop's solution:
1. **Explicitly model the mismatch** between the current policy and the reward model's training distribution
2. **Pop operator clipping**: when the mismatch exceeds a threshold, clip the influence of the reward signal
3. **Remove KL regularization**: traditional RL uses KL regularization to constrain policy updates; IcePop argues that this can block useful exploration, so it removes it directly

#### 4.2.5 Step 3.5 Flash's MIS-PO

**MIS-PO (Multi-level Importance Sampling Policy Optimization)** is Step 3.5 Flash's discrete filtered RL method. Its core innovation is **two-level filtering**:

1. **Trajectory-level filtering**: at the full-answer level, filter out trajectories with low quality according to the reward signal
2. **Token-level filtering**: at the token level, further filter out abnormal tokens according to importance-sampling weights

The benefit of this two-level filtering is that it prevents a small number of abnormal tokens or low-quality trajectories from exerting excessive influence on policy updates, making RL training more stable.

#### 4.2.6 Hunyuan TurboS's Two-Stage GRPO

Hunyuan TurboS uses a standard two-stage GRPO setup:
- **Reasoning stage**: 300,000 reasoning-related samples (math, code, logic reasoning)
- **General stage**: 160,000 general task samples

This design reflects a "reason first, then generalize" post-training paradigm: first build strong thinking ability on reasoning tasks, then preserve general conversational ability through a broader stage.

### 4.3 Distillation

Distillation has changed in status in this round - from an optional efficiency trick to a core training paradigm.

#### 4.3.1 MiMo-V2-Flash's MOPD (Multi-Teacher Online Distillation)

**MOPD (Multi-teacher Online Policy Distillation)** is the core post-training method for MiMo-V2-Flash. Compared with DeepSeek V4's OPD, MOPD has several distinctive characteristics:

1. **Multi-teacher architecture**: different domains use different expert teacher models, and each teacher provides the highest-quality guidance in its own domain
2. **Token-level reward signal**: traditional RL uses trajectory-level rewards (one score per full answer), while MOPD uses the teacher model's token-level logits as the reward signal, increasing information granularity by 1-2 orders of magnitude
3. **Reverse KL + clipped importance sampling + ORM outcome reward**: a mixture of three signals - reverse KL distillation provides distribution-matching signals, clipped importance sampling prevents excessive distribution shift, and the ORM (Outcome Reward Model) outcome reward supervises final-answer correctness

A key engineering challenge in MOPD is that during RL training of an MoE model, rollout generation and parameter updates may use different model versions, causing inconsistent routing decisions. MiMo-V2-Flash solves this with **R3 (Rollout Routing Replay)**: during the parameter-update stage, it replays the routing decisions made during rollout so that training signals stay consistent.

#### 4.3.2 Qwen 3's Strong-to-Weak Distillation

Qwen 3 uses a highly efficient strategy for training small models: use the logit distribution of the large 235B model as teacher signal and distill the small model from it. The key number: **only 1/10 of the large model's GPU training time** is needed to obtain a small model that is close to large-model quality.

The practical significance is huge: it shows that, once you have a strong teacher model, the marginal cost of training smaller models from the same family is very low. This explains why Qwen 3 could release multiple model sizes across both Dense and MoE product lines.

#### 4.3.3 DeepSeek V4's OPD

As noted in section 4.2.2, OPD is based on reverse-KL full-vocabulary logit distillation using 10+ teacher models. What makes OPD distinctive in the distillation setting is that it is "online" - the student model generates samples from its own distribution rather than using teacher-generated samples, which avoids the distribution-shift problem common in offline distillation.

#### 4.3.4 GLM-5's Cross-Stage Distillation

GLM-5 introduces a **cross-stage distillation anti-forgetting** mechanism in its multi-stage post-training pipeline. The background problem is that post-training is usually split into multiple stages (SFT → RL → alignment, etc.), and later stages can cause previously learned abilities to degrade (catastrophic forgetting). GLM-5's solution is to keep the model from the previous stage as a "teacher" at every stage, using distillation signals to prevent the current stage from drifting too far from the previous stage's knowledge.

#### 4.3.5 Distillation Method Comparison

| Model | Distillation Method | Teacher Source | Distillation Granularity | Core Value |
|------|---------|---------|---------|---------|
| DeepSeek V4 | OPD | 10+ domain experts | Full-vocabulary logit | Replaces RL |
| MiMo-V2-Flash | MOPD | Multi-domain teachers | Token-level logit + ORM | Multi-signal fusion |
| Qwen 3 | Strong-to-weak distillation | 235B large model | Logit | Train small models with 1/10 GPU time |
| GLM-5 | Cross-stage distillation | Previous-stage model | — | Prevent catastrophic forgetting |

### 4.4 Agent Capability Training

Agent capability - the model's ability to use tools, interact with environments, and complete complex multi-step tasks - has moved from an "extra feature" to a "core competitive dimension" in this round. Kimi K2/K2.5 invested the most heavily here.

#### 4.4.1 Kimi K2's Large-Scale Agent Data Synthesis Pipeline

Kimi K2 built the most complete publicly described agent training data synthesis pipeline:

1. **Tool collection**: extract real tool definitions from 3,000+ GitHub MCP tool repositories
2. **Tool expansion**: based on real tools, synthesize 20,000+ tool definitions by transforming parameters, combining functions, and simulating new tools to broaden coverage
3. **Trajectory generation**: use an already strong model to generate multi-turn interaction trajectories on synthetic tools - including tool calls, result parsing, error handling, and multi-step reasoning
4. **Quality filtering**: run multi-dimensional quality filters over the generated trajectories and keep the high-quality training data

The key insight in this pipeline is that the bottleneck for agent capability training is not the algorithm - RL methods such as GRPO are already mature enough - but the data: high-quality agent interaction data is extremely scarce and must be synthesized at scale.

#### 4.4.2 Kimi K2.5's Agent Swarm and PARL Framework

Kimi K2.5 pushes agent capability further on top of K2, introducing two key innovations:

**Agent Swarm architecture**

Agent Swarm is a multi-agent collaboration architecture:
- **Orchestrator**: responsible for task decomposition and sub-agent scheduling
- **Sub-agents**: each focuses on tool use in a specific domain such as code execution, file operations, or search
- **Decoupled design**: the orchestrator is trainable, while sub-agents are frozen

The main advantage is that training the orchestrator does not require training every sub-agent at the same time, which greatly reduces complexity. New sub-agents can also be plugged in without retraining the orchestrator.

**PARL (Parallel Agent Reinforcement Learning) framework**

PARL addresses the efficiency problem in agent RL training: traditional agent RL executes tool calls and environment interaction serially, leaving GPUs underutilized because they spend much of their time waiting for the environment. PARL parallelizes the rollout process across multiple agents, overlapping waiting time with compute and significantly increasing training throughput.

Measured effect: latency reduced by 3-4.5x.

**Toggle heuristic**

Kimi K2.5 also proposes a Toggle heuristic: during inference, the model dynamically decides whether to enable thinking mode based on task characteristics. This reduces token usage by 25-30% with almost no performance loss.

**Vision agent capability**

Kimi K2.5's vision ability is based on the **MoonViT-3D vision encoder**: it uses 4-frame spatiotemporal cubes, treating 4 consecutive image/video frames as one 3D input, which achieves 4x compression along the temporal dimension. A surprising finding is **zero-shot vision SFT**: simply using text data for SFT is enough to activate visual reasoning capability, without any vision labels. This suggests that the cross-modal representation built during pretraining is already strong enough.

Further cross-modal RL augmentation experiments show that vision RL not only improves visual-task performance, but also feeds back into pure text tasks - MMLU-Pro +1.7, GPQA +2.1. This hints at a positive transfer effect from cross-modal training signals.

#### 4.4.3 GLM-5's Asynchronous Agent RL Infrastructure (Slime)

GLM-5 built a dedicated infrastructure called Slime for agent RL training:
- **1,000+ concurrent rollouts**: more than 1,000 agents interacting with environments at the same time
- **TITO gateway**: Token-In-Token-Out gateway that manages communication between agents and environments
- **DP-aware routing**: request routing optimized according to the data-parallel topology

The core problem Slime solves is agent RL efficiency: because agents must interact with real or simulated environments, every step has IO latency, and traditional synchronous RL leaves GPUs heavily underutilized in agent settings. Slime uses asynchronous design and large-scale concurrency to raise GPU utilization to an acceptable level.

#### 4.4.4 MiniMax M2's Forge RL System

Although MiniMax M3's technical report focuses mainly on architectural innovation, the **Forge RL system** developed in its predecessor M2 provides useful engineering reference for agent RL training. Forge is a general-purpose RL training platform that supports flexible combinations of reward signals and training algorithms.

---

## 5. Inference Efficiency

Inference efficiency directly determines deployment cost and user experience. The innovations in this round can be organized as follows:

### 5.1 DeepSeek V4's KV Cache Compression

The inference gains from DeepSeek V4's CSA + HCA dual-attention mechanism are comprehensive:
- **KV cache**: only 10% of V3's. In a 1M-context scenario, this means memory requirements shrink from the hundreds-of-GB range to the tens-of-GB range
- **FLOPs**: V4 Pro is only 27% of V3.2's
- This allows V4 to keep pace with or even surpass V3 performance while cutting inference cost substantially

### 5.2 MSA's Reduction in Attention Computation

MiniMax M3's MSA achieves the following in a 1M context:
- **28.4x** reduction in attention computation
- **9x** faster prefill
- **15x** faster decoding

The associated GPU kernel work is also worth noting:
- **Exponent-free Top-k**: traditional `torch.topk` needs to compute exponentials and sort all elements; MiniMax's exponent-free Top-k bypasses the exponential step and runs 2.5-5.1x faster than `torch.topk`
- **KV outer-loop kernel**: treats KV as the outer loop rather than the traditional query outer loop, better matching GPU memory access patterns

### 5.3 MTP Speculative Decoding

MTP's main inference benefit is speculative-decoding acceleration:

| Model | MTP Heads | Average Accepted Length | Speedup |
|------|--------|------------|-------|
| MiMo-V2-Flash | Multi-head | 3.6 | 2.6x |
| GLM-5 | 3 shared heads | 2.76 | — |
| Step 3.5 Flash | 3 heads | — | — |

MiMo-V2-Flash's average accepted length of 3.6 means that, on average, out of the 3.6 tokens it speculatively generates each time, all 3.6 are accepted (i.e. they match the autoregressive result), yielding a 2.6x increase in inference throughput. This is the best publicly reported number at the moment.

### 5.4 Hunyuan TurboS's Mamba Linear Complexity

Hunyuan TurboS's Mamba2 layers provide O(n) linear complexity, which in theory has a fundamental advantage in long-sequence settings: when sequence length grows from 4K to 256K, Transformer attention computation grows by about 4,096x (quadratic), while Mamba grows by only 64x (linear). That said, Hunyuan TurboS still retains 7 attention layers (GQA), so its overall complexity is not strictly linear.

### 5.5 Inference Efficiency Summary

| Model | Core Optimization | Key Metric |
|------|-----------|---------|
| DeepSeek V4 | CSA + HCA compression | KV cache only 10% of V3, FLOPs only 27% of V3.2 |
| MiniMax M3 | MSA sparse attention | 28.4x reduction in attention computation |
| MiMo-V2-Flash | MTP speculative decoding | 2.6x speedup |
| Hunyuan TurboS | Mamba2 linear complexity | O(n) theoretical advantage |
| Step 3.5 Flash | AFD parallelism + MTP | Reduced serial latency |

---

## 6. Head-to-Head Comparison of Key Technical Innovations

The following table compares the 9 models across six dimensions: architecture, attention, optimizer, data, post-training, and inference efficiency:

| Dimension | DeepSeek V4 Pro | DeepSeek V4 Flash | Qwen 3 | Kimi K2 | Kimi K2.5 | GLM-5 | MiniMax M3 | Hunyuan TurboS | Step 3.5 Flash | MiMo-V2-Flash |
|------|----------------|-------------------|--------|---------|-----------|-------|------------|-----------|---------------|---------------|
| **Total / Active Params** | 1.6T/49B | 284B/13B | 235B/22B | 1.04T/32.6B | Based on K2 | 744B/40B | 428B/23B | 560B/56B | 196B/11B | 309B/15B |
| **Architecture** | MoE | MoE | MoE | MoE | MoE + vision | MoE | MoE | Mamba-TF hybrid | MoE | MoE |
| **Attention** | CSA + HCA | CSA + HCA | QK-Norm | MLA | MLA | DSA | MSA | GQA (7 layers) | MFA + SWA 3:1 | SWA + GA 5:1 |
| **Optimizer** | Muon | Muon | — | MuonClip | — | Muon Split | — | — | Muon + Polar | — |
| **Residual Connection** | mHC manifold constraint | mHC manifold constraint | Standard | Standard | Standard | Standard | Standard | Standard | Standard | Standard |
| **MTP** | — | — | — | — | — | 3 shared heads | — | — | 3 heads | Multi-head |
| **Data Volume** | 33T | 32T | 36T | 15.5T | — | 28.5T | — | 16T | 17.2T | 27T |
| **Training Stability** | Foresight routing + SwiGLU | Same as Pro | — | MuonClip zero spike | — | — | — | — | Polar Express (1 spike) | — |
| **Core Post-Training** | OPD distillation replacing RL | OPD | Minimal RL (3,995q / 170 steps) | Agent data synthesis | PARL + Swarm | IcePop + asynchronous agent RL | — | Adaptive CoT + deliberative learning | MIS-PO | MOPD multi-teacher distillation |
| **Thinking Mode** | Three levels | Three levels | `/think` / `/no_think` | — | Toggle heuristic | Three modes | — | Adaptive CoT | — | — |
| **Distillation** | OPD full-vocabulary logit | OPD | Strong-to-weak (1/10 GPU) | — | — | Cross-stage anti-forgetting | — | — | — | MOPD token-level reward |
| **Agent Training** | — | — | — | 3,000+ MCP → 20,000+ tools | Agent Swarm/PARL | Slime asynchronous RL | Forge RL | — | — | — |
| **Inference Optimization** | KV cache is 10% of V3 | Same as Pro | — | — | 25-30% token reduction | Accepted length 2.76 | 28.4x reduction in attention computation | O(n) linear | AFD parallelism | 2.6x MTP acceleration |
| **Representative Benchmark** | SWE-bench 80.6% | — | — | — | — | First open-source model to score 50 on AA Intelligence v4 | — | LMSYS #7, 1356 | — | SWE-bench 73.4% |

---

## 7. Trends and Implications

### 7.1 Six Clear Trends

#### Trend 1: MoE Has Become the Only Real Architecture Choice

Eight of the 9 models use MoE; the only exception, Hunyuan TurboS's Mamba-Transformer hybrid, still includes MoE expert layers. Dense architecture has completely exited flagship models.

The winning logic of MoE is clear: under constrained inference cost (API pricing pressure and edge deployment needs), MoE can deliver capability comparable to Dense large models with far fewer active parameters (11B-56B versus hundreds of billions of active parameters). When DeepSeek V4 reaches 1.6T total parameters with only 49B active parameters, it becomes very hard for any team to justify training a 1.6T Dense model.

An important implication of this trend is that **MoE engineering capability - routing stability, expert load balancing, and All-to-All communication optimization - is becoming a core competitive strength for large-model teams**.

#### Trend 2: Sparse Attention Is Blossoming in Many Directions

CSA/HCA, MSA, DSA, MFA, SWA + GA - every major model has proposed its own sparse-attention scheme. This shows that the efficiency bottleneck of standard full attention in long-context scenarios is widely recognized, but the best replacement has not yet converged.

The design philosophies differ fundamentally:
- **Compression camp** (CSA/HCA): compress KV first, then select or use all of it
- **Selection camp** (MSA, DSA): do not compress; directly select the most relevant KV
- **Window camp** (SWA + GA, MFA): use sliding windows for local coverage and a small number of global layers for long-range coverage
- **Linear camp** (Mamba2): replace attention entirely with a state-space model

These approaches each have trade-offs, and they are unlikely to converge to a single paradigm in the short term.

#### Trend 3: Muon Is Replacing AdamW

DeepSeek V4, Kimi K2, GLM-5, and Step 3.5 Flash - four models explicitly use Muon or a variant of it. AdamW has dominated deep-learning optimization for the last decade, and Muon is the first alternative to prove its superiority at scale in pretraining.

Muon's core advantage is that Newton-Schulz orthogonalization helps exploit gradient geometry better, especially in large-batch training. Custom enhancements built on Muon (MuonClip, Muon Split, Polar Express) show that the basic Muon framework is now accepted, and the competition has shifted to implementation-level optimization.

#### Trend 4: Distillation Is Replacing Traditional RL

DeepSeek V4's OPD and MiMo-V2-Flash's MOPD represent a trend that could reshape post-training: **use distillation to replace (or substantially reduce) traditional RL**.

The underlying logic is:
- RL rewards are scalar (one score), so they carry low information density
- Distillation "rewards" are probability distributions over the whole vocabulary, so they carry orders of magnitude more information
- RL training is unstable (reward hacking, distribution shift, etc.), while distillation is more stable
- RL requires extensive rollout computation, while distillation is computationally more efficient

But distillation has one fundamental limitation: it requires a teacher model that is stronger than the student. If you are training the "strongest model," where does the teacher come from? DeepSeek V4's answer is "domain experts" - expert models trained to the extreme in specific domains, which may not be stronger than the final model in aggregate, but can still provide useful guidance in their own domains.

#### Trend 5: Thinking Mode Is Now Standard

All major models support some form of thinking mode. The difference is in control:
- Manual control (Qwen 3's `/think` / `/no_think`)
- Multi-level control (DeepSeek V4's three intensities)
- Fully adaptive control (Hunyuan TurboS)

The essence of this trend is that users have different trade-offs between inference cost (token count) and inference quality. Simple questions do not need long-chain thought, while complex questions do. Thinking-mode design directly affects user experience and API cost.

From a technical perspective, Qwen 3's finding that "thinking budget emerges naturally" is an important signal: after sufficient training, the model can automatically learn how to allocate reasoning resources, without an explicit length-control mechanism. That suggests thinking mode may eventually become fully adaptive.

#### Trend 6: Agent Capability Has Become a Core Competitive Dimension

Kimi K2/K2.5's agent data synthesis pipeline (3,000+ MCP tools → 20,000+ synthetic tools), GLM-5's Slime asynchronous agent RL infrastructure (1,000+ concurrent rollouts), and MiniMax M2's Forge RL system - multiple teams have invested heavily in agent training.

The importance of agent capability comes from application demand: as large models evolve from "answer questions" to "complete tasks," they need to use tools (search, code execution, API calls, etc.), interact with environments (browsers, file systems, etc.), and handle multi-step tasks (decompose → execute → verify → revise). These abilities cannot be obtained from language modeling alone; they require dedicated training methods and data.

Kimi K2's strong performance on agent benchmarks such as SWE-bench (and Kimi K2.5's expansion of agent capability into vision) validates this investment direction. DeepSeek V4's results on SWE-bench Verified (80.6%), Codeforces (3206), and LiveCodeBench (93.5%) likewise reflect the intensity of competition in agent and coding capability.

### 7.2 Open Questions

#### Question 1: Will Sparse Attention Converge to a Single Paradigm?

Current sparse-attention methods span at least five design philosophies (compression, selection, window, linear, hybrid). Will they eventually converge on a single best approach, the way MoE unified model architecture?

**Arguments for "probably not"**: different methods optimize different objectives - CSA/HCA optimize KV cache size, MSA optimizes compute, SWA optimizes implementation simplicity, and Mamba optimizes theoretical complexity. There are fundamental trade-offs among these objectives.

**Arguments for "probably yes"**: the market will eventually pick the method with the best overall efficiency, just as Transformer unified the competition between RNNs, CNNs, and attention. DeepSeek V4's CSA + HCA currently seems to strike the best balance between "KV cache compression + compute efficiency," and it may become the de facto standard.

#### Question 2: Can Distillation Fully Replace RL?

DeepSeek V4's OPD has already replaced traditional RL with distillation in practice. But that raises a fundamental question: if even the strongest model relies on distillation, where do the teachers come from?

Possible answers:
1. **Domain-expert route** (already being pursued by DeepSeek V4): train multiple domain experts, each pushed to the limit in its own area, and then distill them together. Teachers do not need to be stronger than the student in every dimension; they only need to provide useful signals in specific dimensions
2. **Self-distillation route**: the model uses its own historical versions as teachers and improves iteratively through self-refinement
3. **RL + distillation hybrid route**: RL explores the boundary of capability and finds new knowledge that the teacher models do not have, while distillation efficiently spreads existing knowledge

Qwen 3's minimal RL result (3,995 queries, 170 steps) suggests another possibility: perhaps a small amount of high-quality RL is enough, and distillation handles most of the rest. The future post-training paradigm may be a combination of "a little RL exploration + a lot of distillation propagation."

#### Question 3: Is the Mamba-Transformer Hybrid the Future?

Hunyuan TurboS shows the feasibility of the Mamba-Transformer hybrid architecture by using only 7 attention layers (5.5%) in a 128-layer model, and its LMSYS Arena rank #7 with 1356 points shows that it can compete with pure Transformers.

But a few facts still matter:
1. Hunyuan TurboS is the **only** one of the 9 models covered here to use a Mamba-Transformer hybrid; the other 8 teams all chose pure Transformer + MoE
2. Mamba still has theoretical limitations on exact position retrieval tasks such as "what is the 327th token?" - which is why Hunyuan TurboS keeps 7 attention layers
3. Mamba's linear-complexity advantage is not obvious on short sequences, and only becomes visible in long-sequence settings (>64K)

The Mamba-Transformer hybrid is likely a valuable alternative path, especially for long-context and low-latency scenarios. But whether it can replace pure Transformer + MoE as the mainstream choice is still unsupported by current evidence.

---

## 8. References

1. DeepSeek V4 Technical Report, DeepSeek, 2025.
2. Qwen 3 Technical Report, Alibaba Qwen Team, 2025.
3. Kimi K2 Technical Report, Moonshot AI, 2025.
4. Kimi K2.5 Technical Report, Moonshot AI, 2025-2026.
5. GLM-5 Technical Report, Zhipu AI, 2025.
6. MiniMax M3 Technical Report, MiniMax, 2025.
7. Hunyuan TurboS Technical Report, Tencent Hunyuan, 2025.
8. Step 3.5 Flash Technical Report, StepFun, 2025.
9. MiMo-V2-Flash Technical Report, Xiaomi MiMo Team, 2025.
10. DeepSeek V3: Mixture-of-Experts Language Model, DeepSeek, 2024. arXiv:2412.19437
11. DeepSeek R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning, DeepSeek, 2025. arXiv:2501.12948
12. Qwen2.5 Technical Report, Alibaba Qwen Team, 2024. arXiv:2412.15115
13. Muon: An optimizer for hidden layers in neural networks, Jordan et al., 2024.
14. MLA: Multi-head Latent Attention, introduced in DeepSeek V2 Technical Report, 2024. arXiv:2405.04434
15. Mamba: Linear-Time Sequence Modeling with Selective State Spaces, Gu and Dao, 2023. arXiv:2312.00752
16. Mamba-2: The Structured State Space Duality, Dao and Gu, 2024. arXiv:2405.21060
17. GRPO: Group Relative Policy Optimization, introduced in DeepSeek Math, 2024. arXiv:2402.03300

---

*This article is based on public technical reports. All data and technical details come from the original sources. The level of detail varies across model technical reports, so the depth of coverage differs from section to section.*
