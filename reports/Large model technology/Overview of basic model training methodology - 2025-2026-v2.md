# Overview of basic model training methodology 2025-2026: from DeepSeek V4 to Kimi K2.5

I. Introduction

The years 2025-2026 were two years of structural change in the patterns of competition in the large-scale models. If the theme for 2024 was "MoE rise and open-source catch-up," the theme for 2025-2026 was "Structural innovation accelerates fragmentation, post-training paradigm shifts, and Agent capabilities become the core dimension of competition."

** In international pattern**, the Claude series of Anthropic continues to be at the top of the list; the GPS series of OpenAI remains highly competitive; the Gemini series of Google continues to function in a multi-modular direction. The capacity ceiling of the head closed model is still rising rapidly.

** Domestic patterns**, competition is far more intense than expected. DeepSeek V4 has made simultaneous breakthroughs in the direction of concentration compression and dilution, online strategy distillation, creating a new paradigm of "distillation instead of RL"; Qwen 3 has updated the understanding of training efficiency with a very simple RL (3995 query, 170 moves, a significant increase in mathematical reasoning); Kimi K2/K2.5 has established unique barriers in Agent capacity training; GLM-5 has explored differences in the adaptation of national chips and agt RL infrastructure; MiniMax M3 has achieved a 28.4-fold reduction in focus; and the hybrid TurboS has boldly adopted the Manba-Transformer mix;Step 3.5 Flash and MiMo-V2-Flash have their own unique features on the small model track.

** This document covers the list of models**: DeepSeek V4 Pro/Flash, Qwen 3, Kimi K2, Kimi K2.5, GLM-5, MiniMax M3, mixed Turbos, Step 3.5 Flash, MiMo-V2-Flash, with nine model series.

** Technical source** Official technical report on the above model and the arXiv paper. The level of detail varies - the most detailed technical reports are those for DeepSeek V4, GLM-5, Qwen 3, the next for MiniMax M3 and Step 3.5 Flash, the mixed TurboS and MiMo-V2-Flash report is in moderate density and the Kimi K2/K2.5 report is the most informative in Agent training.

** What will you get from reading this article**: an overview of the technical course of the design of the nine representative base models for 2025-2026 in architecture, attention mechanisms, training strategies, post-training methodology, Agent training five dimensions; an in-depth understanding of the core trends of "deeply focused" "distillate instead of RL"" "Muon instead of AdamW"; and a reference to the technical directions that are worth following and which are the conclusive judgements for practitioners.

---

# II. Overview of models

<unk> Models Total parameters/activating parameters <unk> Structure type <unk> Layer number <unk> Expert configuration <unk> Training data volume <unk> Focus mechanism <unk> Context length <unk> Key innovations <unk> Information level <unk>
|------|---------------|---------|------|---------|-----------|-----------|-----------|---------|-----------|
**DeepSeek V4 Pro** <unk> 1.6T/49B<unk> MoE<unk> 61 <unk> 384 by +1, Top-6 <unk> 33T <unk> CCSA+HCA<unk> 1M <unk> mHC current binding, OPD distillation replacement RL, FP4 quantitative perception training <unk>
**DeepSeek V4 Flash**<unk> 284B/13B<unk> MoE<unk> 43<unk> 256 by +1, Top-6<unk> 32T<unk> CSA+HCA<unk> 1M<unk> and V4Pro structural innovation, small model version<unk>
**Qwen 3** <unk> 235B/22B<unk> MoE<unk> <unk> 128 route, Top-8<unk> 36T<unk> GQA+QK-Nom<unk> Unpublished <unk> very simple RL, confluence of thinking patterns, strong to weak distillation <unk>
**K1** <unk> 1.04T/32.6B<unk> MoE<unk> 61 <unk> 384 by +1, Top-8<unk> 15.5T<unk> MLA<unk> Unpublished <unk> MuonClip zerospike, Agent Data Synthetic Waterline<unk>
<unk> Kii K2.5** <unk> based on K2<unk> MoE+ Visual <unk> <unk> <unk> <unk> <unk> MLA<unk> Unpublished <unk> Visual Agent, Agent Swarm/PARL, Togle Inspired <unk>
**GLM-5** <unk> 744B/40B<unk> MoE<unk> 80<unk> 256, MLA-256<unk> 28.5T<unk> DSA<unk> Unpublished <unk> IcePop, Agent RL(Slime), National Chip Matching <unk>
**MiniMax M3** <unk> 428B/23B<unk> MoE<unk> 60 <unk> 128 by +1, Top-4 <unk> undisclosed <unk> MSA 1M <unk> 28.4 times less attention calculation, native multimodel <unk>
**Mamba-Transformer 560B <unk> Mamba-Transformer mixed <unk> 128 <unk> MoE <unk> 16T <unk> GQA (Team 7 only) <unk> 256K <unk> Mamba2 linear complexity, self-adaptation to CoT <unk>
**Step 3.5 Flash**<unk> 196B/11B<unk> MoE<unk> 45<unk> 289 (shared by 288 route +1), Top-8<unk> 17.2T<unk> MFA+SWA mix<unk> unpublished<unk> AFD parallel, MIS-PO filter RL<unk>
**MiMo-V2-Flash**<unk> 309B/15B<unk> MoE<unk> 48<unk> 256 route, Top-8<unk> 27T<unk> SWA+GA mix<unk> unpublished <unk> MOPD multi-teacher distillation, R3 route consistency, MTP presumably decoding

> Table '- 'since ' indicates not applicable, 'unpublished' indicates that the technical report does not disclose this information.

** Horizontal comparison of core Benchmark**

| Benchmark | DeepSeek V4-Pro | Qwen 3-235B | Kimi K2 | GLM-5 | Claude Opus 4.6 | GPT-5.4 |
|-----------|----------------|-------------|---------|-------|-----------------|---------|
<unk> MMLU-Pro <unk> 87.5 <unk> 82.8 (non-thinking) <unk> 81.1 <unk> 86.0 ~91.3 ~87.5 <unk>
*GPQA Diamond <unk> 90.1 77.2 (non-thinking) 75.1 <unk> 86.2 <unk> 91.3 <unk> 93.0 <unk>
| LiveCodeBench | 93.5 | 70.7（v5） | 53.7 | — | 88.8 | — |
SWE-Bench Verified <unk> 80.6 <unk> 34.4 (third party) <unk> 65.8 <unk> <unk> 80.8 <unk> <unk> <unk>
| Codeforces | 3206 | 2056 | — | — | — | 3168 |
| HMMT 2026 | 95.2 | — | — | — | 96.2 | 97.7 |

> Note: The DeepSeek V4 score is mostly self-reported (self-reported) and is not fully re-reproduced by third parties, and it is recommended that it be carefully quoted. Qwen 3 score distinguishes between thinking/non-thinking patterns, and the above table is non-thinking. Closed-source model scores are derived from the respective Systemcard Card and third-party evaluation platforms (e.g. TAC 2026, CodeSOTA), and unofficial Tech Report self-reporting data may differ in the assessment settings. GPT-5.4 is the OpenAI version published in March 2026, with a reasoning of xHigh.

---

# Three, pre-training

#3.1 Architecture Evolution

## 3.1.1 MoE has become absolute mainstream

Eight of the nine model series use a MoE architecture. Dense architecture is completely lost in the new generation flagship model.

Details of the differences that deserve attention:

<unk> Models, <unk> Total experts, <unk> Shared experts, <unk> Activists, <unk> Special design, <unk>
|------|---------|---------|-----------|---------|
DeepSeek V4 Pro 384 route 1 shared Top-6 <unk>
DeepSeek V4 Flash <unk> 256 route <unk> 1 shared Top-6 <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk>
<unk> wen 3 <unk> 128 route <unk> Top-8 <unk> Remove shared expert <unk>
<unk> Ki K2<unk> 384 by <unk> 1 shared Top-8<unk> by Dense on the first floor, with the remaining 60 floors of MoE <unk>
<unk> GLM-5<unk> 256 route <unk> <unk> <unk> <unk> <unk> <unk> MLA-256+Muon Split <unk>
MiniMax M3 <unk> 128 route <unk> 1 shared Top-4 <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk>
Step 3.5 Flash <unk> 288 route <unk> 1 shared <unk> Top-8 <unk> 3 floor Dense+42 floor MoE <unk>
<unk> MiMo-V2-Flash <unk> 256 route <unk> Top-8 <unk> shared expert <unk>

An interesting differentiation is the retention** of shared experts: Qwen 3 and MiMo-V2-Flash chose to remove shared experts on the grounds that increasing the number of experts by way was more effective than retaining a small number of shared experts; DeepSeek V4, Kimi K2, MiniMax M3, Step 3.5 Flash retained a shared expert. This design option is currently open.

** Detailed route mechanism**

MoE route is a core design choice that affects model capabilities and training stability, and there are significant differences in route functions and load balance strategies among models:

** Route function**: DeepSeek V4 changes the Sigmoid of V3 to Sqrt (Softplus(.)), while Qwen 3 uses standard Softmax door controls. The Sigmoid/Softplus route allows for independent ratings of each expert (inflexible and variable points between experts), while the Softmax route allows for the re-allocation of all experts into probabilities (and 1. The former theoretically allows a more flexible mix of experts, while the latter provides a clearer competitive signal.

**Backload balance strategy comparison**:

The core mechanism.
|------|------|---------|
<unk> DeepSeek V4 <unk> Unassisted loss + sequence-level loss <unk> Learning-based bias in the lead balance (not participating in door-controlled weight calculation), balancing loss weight 0.0001 <unk>
<unk> Qwen 3 <unk> Global mass load balance loss <unk> Cross-micro-batch synchronisation expert frequencyf_i, formula N_Ex<unk> (f_ixp_i) (of which N_E is the total number of experts, f_i is the frequency selected by expert i in the current batch, p_i is the average door control probability assigned to expert i) to promote specialization in the field
<unk> Ki K2<unk> Standard auxiliary loss <unk>

** Expert particle selection**: Research has shown (arXiv:2505.06839), increasing the ability of MoE specialists to index the expression of networks without changing their thinness. This explains why DeepSeek V4 used 384 small experts (2048 per intermediate dimension) instead of 64 major experts - fine particle experts - allowed a narrower specialization. DeepSeek V4 also used Hash route (targeting experts based on the predefined Hashi map entered totoken (specific Hash characteristics not disclosed in the report) to replace the Dense FFN layer in V3.

** The mixed TurboS off-the-shelf** deserves special discussion. It uses a 128-storey Mamba-Transformer mix of structures, consisting of seven AMF blocks (Attention & Mamba2 & FFN) and several MF blocks (Mamba2 & FFNN) which are 128 layers, consisting of 7-storey Attention, approximately 57-storey Mamba2 and 64-storey FFN/MoE (interlaced distribution, non-sequencial stacking). In the 128-storey, the attention layer is only 7 layers, accounting for 5.5%. The central bet of this radical design is that the O (n) linear complexity of Mamba2 has the essential efficiency advantage of a long sequence scenario, at the cost of requiring a minimal layer of attention to compensate for the lack of Mamba's search for precise locations.This structural option is feasible from the 7th score of LMSYS Arena, 1356, but more evidence is still needed to compare it to simply Transformer+MoE.

One reference to the efficiency of reasoning: Transformer's concentration count increased by about 4096 times (second complexity) when the sequence length increased from 4K to 256K, while Mamba grew by only 64 times (linear complexity). But it needs to be noted that the hybrid Turbos still retains seven layers of GQA attention, and therefore its overall complexity is not strictly linear.

##3.1.2 Attention mechanism: from total to dilution

In this round of model competition, the innovation of attention mechanisms is the most excellent technological dimension. Programmes can be divided into four schools by design philosophy:

- ** Compression ** - KV is compressed downwidth and then attention is calculated.
- **Selection** - Instead of compressing KV, the most relevant subsets are selected for the calculations.
- **window pie** - Locally covered with slide windows with a small global layer covering remote dependency. Representing program: MFA+SWA of Step 3.5 Flash, SWA+GA of MiMo-V2-Flash
- **linear** - A state space model to replace the attention mechanism completely.

Each of these four genres has merit and is unlikely to be uniform to a paradigm in the short term.

**CSA+HCA dual mechanism for DeepSeek V4 (compressive)**

DeepSeek V4 proposes two complementary focus mechanisms based on MLA (Multi-head Latent Attention, pioneered by DeepSeek V2).

- **CSA: KV per m=4 adjacent totoken compressed to 1 by linear projection of adjacent totoken in the MLA sub-spire, then to a lightweight " Lighting Indexer" to a compressed KV totop-k thinner (V4Pro k=1024). This means that the number of token actually involved in attention calculation is compressed from million to thousands in the context of 1M.
- **HCA: Higher compression rate (m'=128), but not diluted choice, but focused on all compressed KVs. This ensures the integrity of global information.

CSA and HCA are used interchangeably in the Transformer layer, creating a complementary pattern of "local precision selection plus global gross particle coverage". The efficiency of reasoning is significant: V4Pro's KV cache is only 10% of V3 and FLOPs is only 27% of V3.2.

The other way to move from a compressed to a selective one is not to do KV compression but to choose directly the most relevant KV subset.

** MSA of MiniMax M3**

The MSCA uses two-part design:
- **Indication branch**: Lightweight Selector quickly determines which KV blocks are relevant to the current query
- ** Main branch**: A precise piece of KV block selected to distract attention

Specific parameters: Block size 128, with 16 blocks selected for each query. In the 1M context, the focus calculation is reduced by 28.4 times, the prefilling acceleration nine times and the decoding acceleration 15 times. The accompanying GPU inner core optimization includes the de-index Top-k (2.5-51 times faster than the torch.topk) and the KV external cycle kernel.

The same choice but a lighter route was taken by the GLM-5.

**DSA of GLM-5 (optional, low-cost matching)**

The salient advantage of DSA is that it is a very low fit cost: 20B token training alone can shift from total attention to dilution (comparable the 943.7B token cost of DeepSeek V4). DSA uses the determinative tok choice to avoid the uncertainty of training that randomness brings.

**MLA improvement for GLM-5: Muon Split**

GLM-5 uses the MLA-256 (the head size is raised from standard 192 to 256, and the attention head is reduced by one third), but it is found that the direct application of the Muon optimiser to MLAs, orientation of the unified KV projection matrix, can interfere with the gradient signals between different attention points. The solution for Muon Split is to make the matrix turn separately for each independent focus in the MLA, rather than the single matrix. The absorption experiment shows that MLA + Muon Split has reached 62.5 on MMLU (61.5 of vs standard MLA and 61.2 of GQA-8), and 51.8 (48.9 of vs MLA) on BBH, effectively compensating for the ability limit in the MoE structure.

Unlike compressed and selection pies, the idea of window pie is more simple: to use slide windows to handle local contexts, with only a small layer of attention being given to the whole picture.

**Step 3.5 Flash MFA+SWA mix (window pie)**

Step 3.5 Flash uses a combination of SWA and global attention at a ratio of 3:1 (3 SCWA, 1st floor, 3rd floor, 4th floor). The SWA window is 512 token size. The unique thing is that** top-level door control attention** - each attention head can learn his own door-control weight to determine the mix of SWA and global attention.

MiMo-V2-Flash also took the window-sending route, but the parameters were more radical.

**SWA+GA mix of MiMo-V2-Flash (window pie, extreme parameters)**

MiMo-V2-Flash also uses SWA and global attention mix, but at a much more extreme rate: 5:1 (39th floor of 48th floor of SWA, 9th floor of GA). SWA window only 128 token -- the smallest window in all models. To prevent the collapse of attention caused by tiny windows, MiMo introduced **learning sink bias**: add learning-based deviations to specific locations (e.g. BOS token) so that the model can allocate "waste attention" to sink token and avoid a deterioration of attention weight.

Finally, the most radical option: direct substitution of the state space model with linear complexity.

** Extreme design of the hybrid TurboS (linear)**

Only 7 layers of attention are available in 128 layers (GQA, 64 Query/8 KV headlines), with the rest composed of Mamba2 and FFN/MoE. Mamba2 provides the O(n) linear complexity using the parameter configuration of d_state=128, chunk_size=128. This is the lowest concentration layer in all models.

** Qwen 3: representative of the conservative route**

It is worth mentioning that Qwen 3 has chosen a conservative route to the focus structure – standard GQA – without introducing any distraction mechanism. The QK-Nom mentioned in its technical report is a training stability technique (to standardize the Query and Key vectors to prevent an explosion of the focus score) rather than an innovation at the attention structure level. In the context of other models that are exploring distraction, Qwen 3 has achieved a competitive outcome using standard GQA+36T data volume + very simple RL, suggesting that attention architecture innovation is not the only way to increase.

** Overview of the attention programme**

<unk> Model <unk> Genre <unk> Program name <unk> Core idea <unk> compression/relative ratio <unk> Fit cost <unk>
|------|------|---------|---------|-------------|---------|
<unk> DeepSeek V4 <unk> Compressed pie <unk> CSA+HCA <unk> Compressed+top-k Select/ High Compression +IDense <unk> KV cache only 10% of V3 <unk> Training from the top <unk>
<unk> MiniMax M3 <unk> Selecting pie <unk> MSCA <unk> index + thin double branch <unk> 28.4 times less attention calculation <unk> training from the beginning <unk>
<unk> GLM-5 <unk> Selecting pie <unk> DSA <unk> Determinable top-k<unk> Unpublished <unk> 20B token only
Step 3.5 Flash <unk> MFA+SWA 3:1
<unk> MiMo-V2-Flash <unk> SWA+GA 5:1<unk> Small window +sink bias <unk> Unpublished <unk> training from the top <unk>
<unk> Mamba2+GQA<unk> Linear Complexity+Little Attention <unk> O(n) Linear <unk> Training from the beginning
<unk> Kimi K2<unk> MLA (responsible to DeepSeek V2) <unk> Low KV compression, non-sleep selection <unk> KV cache compression to about 3% <unk> Follow mature formula <unk>
<unk> wen 3 <unk> Conservative route <unk> GQA+QK-Nom <unk> Standard GQA, do not do thin <unk> not applicable<unk> not applicable <unk>

##3.1.3 Re-engineering of the residual connection: from V3 HydroConnect to V4 mHC

The problem with traditional residual connections (y = x + f (x)) is that, as the layer numbers deepen, the gradient of the contribution of the layers to the final output may be uneven. DeepSeek V3 has introduced the concept of HyperConnection, which allows for a more balanced contribution of the layers by replacing simple added-repairs by a learning weight matrix. V4 builds on this by introducing **mHC (manifold-constrated Hyper-Connection)**, adding double-smogical matrix flow constraints, and achieving stricter mathematical controls on the link.

mHC practices:
1. Replace the residue link with a **two random matrix** (all in each row and 1 in each row) to control the mixed weights of input/outputs at each layer
The constraints of the two-random matrix are achieved through the Sinkhorn-Knopp algorithm** (20 overlaps) - the process of reclassification and reclassification of a learning matrix to a double-random matrix flow
3. Matrix parameters are dynamic parameterized (rather than fixed values) and can be adapted to training

The double-random matrix guarantees the "sustainability" of the information flow - there is no situation where certain layers of contributions are over-magnified or discouraged. The measurements show that the mHC only increases the extra calculation time by 6.7%, but there is a significant improvement in the stability and performance of the training of the deep network.

##3.14 Multitoken Forecast (MTP)

MTP is widely used in this round model:

- **GLM-5**: 3 floor shared MTP head with an average acceptance length of 2.76 per day for reasoning
- **Step 3.5 Flash**: 3 MTP head, introducing **Fast-MTP location perception loss** - Allow each projection head to use different loss weights depending on its projected location (1, 2 or 3 future token)
- **MiMo-V2-Flash**: The model is able to receive 3.6 tokens in a continuous manner on average per presumably decoding step, compared to 2.6 times the token self-retroactivity increase

The value of MTP is twofold: training provides a richer gradient signal (for more than one future token per location) and reasoning significantly increases through extrapolation.

##3.1.5 Attention-FFN Coding Parallel (AFD)

The AfD, as proposed by Step 3.5 Flash, is a structural engineering innovation. The traditional Transformer center-level attention layer and FFN layer are executed in a combination of execution. The AfD decouples both in parallel: attention and FFN are calculated simultaneously, results are combined at the layer output, reducing the delay in the chain of each layer, and the GPU parallel computing capability can be better utilized in reasoning.

#3.2 Data engineering

##3.2.1 Data scale comparison

<unk> Model <unk> Pre-training data volume <unk> Language overlay <unk> Note <unk>
|------|-----------|---------|------|
<unk> en 3<unk> 36T token <unk> 119 languages <unk> Maximum data volume for the current round <unk>
DeepSeek V4 Pro 33T token<unk> Unpublished<unk>
DeepSeek V4 Flash 32T token<unk> Unpublished <unk>
GLM-5 <unk> 28.5 T token <unk> undisclosed <unk> 5 stage training <unk>
<unk> MiMo-V2-Flash <unk> 27T token <unk> Unpublished <unk> 3-stage training <unk>
Step 3.5 Flash <unk> 17.2 T token <unk> Unpublished <unk>
<unk> The hybrid TurboS 16T token<unk> Unpublished <unk>
<unk> K2<unk> 15.5T token<unk> Unpublished <unk> 2-stage training

The size of the data has entered the era of "Billions of Token." It is worth noting that larger data volumes do not directly equal better models: DeepSeek V4 exceeds the use of 36T token Qwen 3 on multiple benchmarks, suggesting that data quality and training strategies are as important as data size.

** Data matching and course learning**

The technical reports of DeepSeek V4 and Qwen 3 do not disclose the exact ratio of training data in English/Chinese/code/mathematics (this is commercially sensitive information), but a common model of course learning can be seen from the published training strategy:

- **Qwen 3**: Three-stage course - Phase I (30T) has a wide coverage of universal knowledge in 119 languages; Phase II (5T) has significantly increased the weight of STEM/code/resumption data (composing data using Qwen2.5-Math and Qwen2.5-Coder); Phase III (thousands of billions) has focused on long-term contexts (75% in length at 16K-32K and 25% at 4K-16K)
- **DeepSeek V4**: Serial length incremental (4K ~ 16K ~ 64K ~ 1M), formerly 1T token uses dense attention preheat, 64K introduces diffusing. Data with special emphasis on long files (scientific papers, technical reports) and Agent execution tracks
- **MiMo-V2-Flash**: Phase III - Universal 22T<unk> Sampling + 5% Synthesis 4T<unk> Spand 1T

##3.2.2 Scaled use of synthetic data

Synthetic data have been changed from "supplementary" to "core component".

- **Ki K2 knowledge rewriting strategy**: the original web text is recast through a larger model into a more structured and training-friendly format, which is used on a large scale during the pre-training phase
- **Kii K2 Agent data synthesis stream**: from 3,000+ GitHub MCP tools, 2000+ tool definition is synthesized to generate multiple rounds of Agent interactive trajectories. This is the largest Agent training data synthesis programme in the current public information
- **Qwen 3 stage of reasoning enhancement**: 5T is earmarked for reasoning enhancement in 36T total data, containing a large number of synthetic mathematical and code reasoning data

##3.2.3 Data rewriting policy

Kimi K2 has a distinctive feature in data engineering: **Knowledge Reworking**. The original text on the Internet is often full of noises like advertising, navigation bars, and unrelated links, which are not used directly for training purposes. Kimi K2 has rewrited these texts using trained models — retaining core knowledge content, but reorganizing them as formats for learning more appropriate to language models. The trade-off between the reasoning required for rewritement and the efficiency of training is an issue that deserves to be studied in depth.

#3.3 Training strategy

##3.3.1 Long context training

Long-term contextual capacity has become a requirement for labelling, and models generally use multi-phase contextual extension strategies:

<unk> Model, <unk> Extension path, <unk> Final context length <unk>
|------|---------|-------------|
<unk> DeepSeek V4<unk> 4K <unk> 1M (multi-stage) <unk> 1M <unk>
<unk> <unk> en 3 <unk> 3 stage 3 (general 30T <unk> reasoning plus 5T <unk> long context) <unk> unpublished
<unk> Ki K2<unk> Two-stage pre-training + 400B + 60B long-term context <unk> unpublished
GLM-5 Pre-training Phase V Unpublished
MiniMax M3 Unpublished 1M
<unk> Mixed TurboS <unk> 2nd stage extension <unk> 256K <unk> 2nd stage
<unk> MiMo-V2-Flash <unk> Phase 3 (General 22T <unk> Code Enhancement 4T <unk> Long Context 1T) <unk> Unpublished

**RoPE base frequency versus extension method**

<unk> Model <unk> RoPE base frequency <unk> extension method <unk> final context <unk> special technology <unk>
|------|---------|---------|----------|---------|
<unk> DeepSeek V4 <unk> Unpublished (Partial RoPE, only for the last 64 dimensions of Q/KV) <unk> YaRN + CSA/HCA difficultate <unk> 1M sample level mask to prevent cross-document association <unk>
<unk> Qwen 3 <unk> 1,000,000 (ABF technology) <unk> ABF + YaRN + DCA <unk> 128K (four times the reasoning) <unk>
Llama 4 <unk> iRope (3x4 floor) iRoPE architecture <unk> Scout 10M / Maverick 1M <unk> 256K after training
GLM-5 – <unk> DSA continuing training (only 20B token) <unk> 200K <unk> Final Top-k avoids RL training instability <unk>

##3.3.2 FP8/FP4 mix accuracy

Low-precision training has deepened in the current round of models. The FP8 mix is a common practice and no longer serves as a stand-alone technology flashpoint. DeepSeek V4 goes further, introducing the FP4 QATP for the first time in the trillion-dollar pre-training, as follows:

** Numerical format**: A zoom factor in E8M0 format is shared for every 32 elements using MXFP4(E2M1) - 1-bit symbol + 2-bit index + 1-digit tail. The counterquantification of FP4 to FP8 is non-destructive (FP8 E4M3 is 2-bit more than FP4 E2M1).

**Quantified position**: (1) MoE route by expert weight (the main source of GPU visible consumption); (2) CSA indexer QK path (accelerated long-term context attention fraction calculation).

** Training process**: FP32 sovereignty requantifies to FP4 = counter-quantified back to FP8 for forward calculation. The gradient is calculated on FP8 weights and directly transmits back to FP32 by Straight-Through Estimator (STE). Forward transmission uses round-to-nearest, reverse transmission uses stochastic rotation, which combines improved training stability.

**Efficiencies**: Top-k Selector has obtained a double acceleration, while the return rate for KV entries has remained at 99.7 per cent, but detailed dissipation comparison data for FP4 vs FP8 vs BF16 are not available in the technical report.

## 3.3.3 Training stability

Training stability is a core engineering challenge for large-scale pre-training. This round of models is particularly innovative in this dimension.

**MuonClip of Kimi K2 -- zerolos piece**

MuonClip is the stability constraint added to the Muon optimist: a threshold for QK internal build-up in the attention layer is set =100, and is cropped when it exceeds the threshold. This design enabled Kimi K2 to achieve **zerolos spice** throughout the 15.5 T token pre-training process — by contrast, most large-scale training is subjected to several to dozens of Loss spike, each of which means a degradation of the training state and a waste of time.

**DeepSeek V4 foreseeive route + SwiGLU plier**

DeepSeek V4 uses the double stability guarantee:
1. **Foresight Roading**: Update of the modem MoE router and update of the model bone. The two are updated simultaneously at normal training; when potential Los Spike signals are detected, the router is suspended and only the bone stem is updated. This increases the calculation cost by about 20%, but the actual average cost is well below 20% as it is activated only at the time of the spinke risk.
2. **SwiGLU plier**: Control the output of the SwiGLU activation function within [-10, 10] range to prevent the dissemination of extreme activation values

**Pup 3.5 Flash Polar Express**

Step 3.5 Flash performed a special optimization of the accuracy of the Muon optimiser (known as Polar Express), which only occurred once in 17.2 T token training.

** Technical comparison of stability**

♪ The way you're going ♪
|------|-----------|--------------|---------|
<unk> Ki K2<unk> MuonClip (QK-Clip and =100) <unk> 0<unk> very low
Step 3.5 Flash <unk> Pollar Express <unk> Unpublished <unk>
<unk> DeepSeek V4 <unk> Predictive route +SwigLU plier <unk> Unpublished <unk> about 20% (peak) <unk>

##33.4 Optimizer: Muon replaces AdamW

The use of the Muon optimizer is a significant trend in the current round:

♪ The model, the optimizer, the special configuration, the ♪
|------|-------|---------|
DeepSeek V4 Muon <unk> 10 Newton-Schulz turns (first eight steps fast + two steps precise), mixed barrel distribution
<unk> Ki K2<unk> MuonClip<unk> Muon+QK-Clip Stability Constraint
<unk> GLM-5 <unk> Muon Split <unk> MLA-256 head cutting <unk>
Step 3.5 Flash <unk> Muon+Polar Express <unk>

Muon retains the dynamic mechanism, but replaces the AdamW's element-by-element second-order estimate with Newton-Schulz's tectonics for the dynamic buffer matrix, which is being interwoven, allowing the update to be more evenly distributed in the odd-value space of the parameter matrix. DeepSeek V4 is particularly refined in its realization: the first eight steps Newton-Schulz has accelerated the recovery in a fast but less precise way, the second steps have been switched to a high-precision mode to ensure final straight mass; the distribution of the mixed barrels optimizes parallel efficiency by assigning them to different calculators according to the size of the parameter matrix.

#3.4 Training infrastructure and costs

##3.4 GPU size versus cost

Models, gPU sizes, comments, etc.
|------|--------|------|
Step 3.5 Flash 4096 H800
<unk> Other models, <unk> not explicitly public, <unk> , presumably 2,000-16000 calc.

The size of the GPU and the cost of training are the most opaque parts of most technical reports. Step 3.5 Flash alone has clearly disclosed the scale of training of 4096 KH800. However, from the volume of training data and model size, it is likely that DeepSeek V4 Pro (1.6 T parameter, 33T token) will have more than 10,000 Kcal.

##3.4.2 Communication optimization

The core communication bottleneck for the large-scale MoE training is the All-to-All communication between experts. The models respond with different strategies:

- The mixed barrel distribution and parallel optimization of experts in **DeepSeek V4** are important sources of efficiency in their training
- **GLM-5 ' s national chip-basket fit**: GLM-5 is the only large model currently in the public report that completes the full-scale fit of the Seven Power Chip Platform, covering the Ascend, Moore Threads, Hygon, Cambricon, Kunlunxin, MetaX and Enflame. The adaptation techniques include the blending of W4A8 quantification, high-performance integration algorithms and special reasoning engines. GLM-5.1 goes further, complete process training on the entire 100,000 pieces of chips, achieving zero NVIDIA dependence. This engineering practice is indicative of supply chain security in China ' s large model industry.The interconnection of the different chips and the communications bandwidth vary widely and require individual optimization of the communications strategy for each platform.
- R3 (Rollout Roading Replay) technology **MiMo-V2-Flash** indirectly addresses a communication-related issue in MoE training: RL phase rollout generates and updates training using different model versions, leading to inconsistent decision-making by route. R3 removes this inconsistency by replaying the rollout phase by route decision-making during training

# 3.5 Summary of the efficiency of reasoning

<unk> Models <unk> Core optimization tools <unk> Key indicators <unk>
|------|-----------|---------|
<unk> DeepSeek V4<unk> CSA+HCA compression <unk> KV cache only 10% of V3 and FLOPs only 27% of V3.2 <unk>
MiniMax M3 <unk> MSC is distracted, 28.4 times less, prefills 9 times faster, decoding 15 times faster
<unk> MiMo-V2-Flash <unk> MTP decoding, <unk> acceptance of 3.6 token, 2.6 times the volume of throughput
The theoretically, in the pure Mamba layer, the 256K series only increases 64 times (linear) vs. 4096 times (twice), but the hybrid Turbos retains 7 layers of GQA attention, and the overall complexity is not strictly linear.
Step 3.5 Flash <unk> AFPD parallel + MTP <unk> Reduction of serial delay
<unk> GLM-5<unk> MTP Pseudo decoding <unk> Average acceptance length 2.76 <unk>

---

# Four, after training

# 4.1 SFT strategy

## 4.1.1 Thinking about patterns against designs

"Think mode" -- that is, models are internal reasoning before they generate a final answer -- has become a label function. But there are clear differences in the design concepts of households.

**/think and/no_think**

Qwen 3 uses the most concise binary design: the user controls whether the model is internally reasoned by adding the `/think ' or `/no_think ' markers to the hint. The "thinking mode integration" phase, which depends on post-training training, will be combined with a combination of reflective and non-thinking training data, allowing the same model to switch patterns according to instructions.

One of the important findings of Qwen 3 is that:** thinking about budgets is a natural surge in capacity** - the model, after training RL, automatically learns to divide the thinking process over different lengths according to the difficulty of the problem, without the need for a visible long-range control mechanism.

** Three lines of reasoning for DeepSeek V4**

DeepSeek V4 provides more sophisticated gradient control:
- **Non-think**: No internal reasoning, direct generation of answers (appropriate for simple questions)
- **Think High**: Internal reasoning of standard depth
- **Think Max**: A maximum depth of internal reasoning (adapted to extremely difficult mathematics/programming issues)

The three forces were triggered by different system tips, and the models learned to distinguish between the three models at the OPD distillation stage.

** Three models for GLM-5**

GLM-5 also provides three modes of reasoning, but the design concept is more inclined to "scenario fit" than "strength gradient" - providing different strategies for thinking about different types of tasks (e.g. mathematical reasoning, code generation, universal dialogue).

** Cot-Assemble Cot**

The design of the hybrid TurboS is the most radical:** CoT**, which is the length of adaptation, - the model automatically determines whether to use long-chain or short-chain thinking, depending on the difficulty of the problem, without requiring manual switching. The actual results show that this strategy enables the hybrid TurboS to achieve comparable reasoning performance by using only DeepSeek-R1, 52.8% of the token volume, with the cost of reasoning being almost halved.

** Comparison of reflection patterns**

<unk> Model, <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> ,<unk> , <unk> , <unk> ,<unk> , <unk> ,<unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk>
|------|-------|---------|---------|
<unk> 3<unk> 2<unk> /think/no_think tags <unk>
<unk> DeepSeek V4 <unk> Non-think/Think High/Think Max <unk> Level 3 Gradient
GLM-5<unk> 3<unk> Scope
<unk> The hybrid TurboS <unk> Self-adaptation <unk> No manual switching <unk> 52.8% token to R1 only

### 4.1.2 Multi-round review learning

The hybrid TurboS proposes ** Multi-round Review Learning** in three steps:
1. **The evaluation stage**: allow models to self-judge their responses and identify weaknesses
2. **Vulnerability review**: improved responses to the identified weaknesses to allow models to generate improved responses
3. **Eddie SFT**: use original answer-judge-improvement of the triad as training data and conduct of SFT iteratively

Essentially, it is to let models learn from their mistakes — a way that is similar to the "fault-print" approach in human learning.

# 4.2 Post-training methodology: RL, distillation and hybrid paradigm

The methodology for post-training has been significantly differentiated in the current round: pure RL routes, distillation alternative RL routes, and the RL-distillation mix. This section is organized according to technical paradigms, rather than model-by-model.

## 4.2.1 RL route: GRPO and its improvements

GRPO (Group Real Policy Implementation, pioneered by DeepSeek) remains the most widely used RL algorithm in the current round of models, but on this basis, improvements have been made in different directions.

**Expressive GRPO of Qwen 3**

The RL results of Qwen 3 are one of the most surprising findings of the round: using only **3995 query** (less than 4,000 questions), training only **170 steps GRPO**, the AIME mathematical competition benchmark was raised from 70.1 to 85.1 points (+15).

This result challenges the general perception that "RL needs a lot of data and long training." The Qwen 3 team explained that if pre-training and SFT have built up enough basic capacity, RL has a much more "activated" rather than "professor" role – a small number of high-quality RL signals are sufficient to trigger the reasoning that the model has, but not fully released.

Qwen 3 post-training follows a four-stage process:
1. ** Long Cot cold start**: long-chain thinking data for SFT, building habits of thinking
2. **RL**: very simple GRPO (3995 query, 170 moves) above
3. **Configuring Modes**: mixed/think and/no_think training data
4. **General RL**: RL on a broader mandate

** Icepop of GLM-5 - Solving training - Disparity of reasoning distribution**

The core insight of IcePop is that the strategy used by standard RL (e.g. GRPO) in training _train and reasoning _ is a systemic difference _ infer — training usually uses lower temperatures, different sampling strategies or batch optimization. The mismatch between the IcePop modeling:

1. ** Calculate mismatch **: Old = <unk> train (y<unk> x) / <unk> infer (y<unk> x)
2. **Pop calculation**: When the range [1/beta, beta] is consistently exceeded (beta=2), the gradient of the sample is completely blocked by the pop calculation
3. ** Remove KL regularization**: IcePop believes that KL is being used to limit the strategy deviation from the reference model, and that it also prevents its effective exploration in new areas and direct removal

This design allowed GLM-5 to maintain stability in the three stages of the training of the reasoning RL, Agent RL and the generic RL, and to improve RL faster as KL was removed.

**Step 3.5 Flash MIS-PO - Double-Stair Filter RL**

The core innovation of the MIS-PO (Multi-level Importation Summer Policy Implementation) is:** Double-level filtering**:
1. **Trail layer filter**: at the full response level, filtering off low quality tracks based on incentive signals
**Token tier filter**: at token level, further filtering the anomaly token according to weight of importance

Double-tier filtering avoids the excessive impact of a few abnormal token or low-quality tracks on strategy updates, and makes RL training more stable.

** Two stages of the hybrid Turbos GRPO**

The hybrid TurboS uses two phases of GRPO: 300,000 data for the reasoning phase + 160,000 data for the generic phase, reflecting the "prejudicing reasoning, post-conversion" post-training paradigm - building a strong capacity for thinking on the reasoning task and ensuring that the generic dialogue capability is not lost through the generic phase.

## 4.2.2 Distillation alternative RL route: OPD and MOPD

The distillation has changed qualitatively in the position of the models in this round - from "optional efficiency optimization" to "core training paradigm".

** DeepSeek V4 OPD - Complete replacement of traditional RL with distillation**

The OPD is a major innovation in the post-training paradigm of DeepSeek V4.
1. **Independent training of experts in the field**: training of expert models for different fields (mathematics, codes, generics, etc.) with each expert model following a complete SFT+GRPO process
** Online strategy distillation merge**: instead of simple model consolidation (e.g., parameter average), logit distribution of the full term table is distilled using **reverse KL dispersion** - student models (final V4) generate samples under their own strategy distribution and then match the logit distribution of 10+ teacher models

The underlying logic of this design is that the traditional RL reward signal is a metric (a numerical measure is good and bad), while the distilled "reward signal" is a probabilities distribution of the entire vocabulary -- the amount of information is several orders of magnitude. This explains why the OPD can achieve better results with fewer training steps.

The meaning of "online" in OPD is crucial: student models generate samples under their own distribution (rather than using samples from teachers), which avoids the problem of dissimilar distribution in traditional offline distillation.

More specifically, DeepSeek V4 has also introduced the ** Generational Incentive Model (GRM)**: the traditional incentive model is differentiated (input one answer, output one score), the GM is generated (genuine the evaluation text, then extract the score from the evaluation). And, DeepSeek V4** does RL optimization for the GM itself** - RL is used to enhance the judgement quality of the incentive model and form an embedded optimization loop.

**Mo-V2-Flash MOPD - Multi-Teacher Online Distillation**

MOPD (Multi-teacher Online Policy Distillation) is an online strategy distillation paradigm with OPD, but there are several unique features:
1. ** Multi-teacher structure**: Different expert teacher models are used in different fields, each teacher provides the highest quality of guidance in his or her own field
2. **Token level incentive signal**: Traditional RL rewards are trajectories (one full answer to one score), MOPD uses the teacher model token level logit as an incentive signal, and the information particles are in 1 to 2 orders of magnitude
** Three signals mix**: Reverse distribution matching signal for KL distillation, tailoring importance to prevent excessive distribution, ortcome Reward Model reward for providing supervision of final answer correctness

A key engineering challenge for MOPD is that the MoE model is being developed and the parameters updated in different versions of the model in RL training, resulting in inconsistent MoE route decisions. MiMo-V2-Flash addresses this through technology **R3 (Rollout Roading Replay)**: replaying route decision-making at the rollout stage during the parameter updating phase to ensure consistency of training signals.

##4.2.3 Strong to weak distillation and cross-stage distillation

**The power of Qwen 3 to weak distillation**

Qwen 3 used a very efficient strategy for small model training: using the big model (235B) logit distribution as a teacher's signal, distilling small models. Key data: ** Small models close to large model levels can be obtained only if the big model takes 1/10 of the GPU training time**.

This result means that the marginal cost of training small models of the same series is extremely low, given the existence of a powerful teacher model. This explains why Qwen 3 can publish multiple scale models of both Dense and MoE product lines simultaneously.

**The GLM-5 cross-stage distillation anti-forgotten**

GLM-5 introduces a mechanism for cross-stage distillation against oblivion in many stages of post-stage training. After training, which usually takes place in multiple phases (SFT<unk> RL, etc.), the latter phase of training may lead to a deterioration of the capacity built in the previous phase (disasteralization).

## 4.2.4 Post-training methodology comparison

<unk> Models, paradigms, methods, core values, <unk>
|------|------|------|---------|
<unk> DeepSeek V4 <unk> Distillation to replace RL <unk> OPD (10+ field expert, full wordlogit) <unk> Information density far exceeds RL values reward <unk>
<unk> MiMo-V2-Flash <unk> Distillation to replace RL <unk> MOPD (multi-teacher, token level logit+ORM) <unk> Multi-signal integration <unk>
<unk> <unk> 3 <unk> RL as main + distillation aid <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk>
<unk> GLM-5 <unk> RL+ Diffusion against Forgotten <unk> IcePop + Cross-Phase Distillation <unk> Solving Distribution Disparities + Disaster-Responding Forgotten <unk>
Step 3.5 Flash <unk> Pure RL <unk> MIS-PO (double-level filter) <unk> Stable discrete filter RL <unk>
<unk> The hybrid Turbos <unk> The pure RL <unk> The two stages of GRPO (300,000 reasoning plus 160,000 general) <unk> The first step of reasoning is the first step of reasoning.

###4.2.5 Incentive function design

The incentive function is the core component of RL training that determines the direction of optimization, and the models employ different incentive strategies:

** Rules-based and verifiable awards** (mathematics/codes):
- Mathematics: requires final answers to be placed in \boxed{}, automatically matching the standard answers (one point correct, zero points error)
- Code: executed through compilers and compared to predefined test cases, is a binary reward
- Formatting incentives: mandatory model output contains labels `<think> and </think> to ensure that the reasoning process is synthesic
- GRPO 's intra-group advantage estimate A_i=(R_i - mean)/ std, without additional Critic models

** Generating incentive model for DeepSeek V4 (GMM)**:
The core difference between the training of GM using SPCT methods and traditional RM methods is that the output form - the differential RM direct output mark - and the GM generates a text pipeline of the "principle RM comment score" - is 69.9% of the RewardBench accuracy rate (based on the RewardBech standard assessment set, which is not the advantage of the GM to be absolute above the RM, but of being expanded in cross-cutting generalization and reasoning - sustainable upscaling through multiple sampling, which is impossible for the RM to achieve), which can be increased to 71.0% through 32 rounds of voting aggregation, and more importantly, the RM filtering of 72.8% by MetaRM itself, which also creates an optimized circle of the RL (rule-based RL) by V4.

# 4.3 Agent Competency Training

Agent capabilities (i.e. the ability to use models, interact with the environment, and perform complex multistep tasks) have risen from "additional functions" to "core competition dimensions" in the current cycle. Kimi K2/K2.5 is the deepest investment in this direction.

##4.3.1 Large-scale Agent data synthesizing waterlines for Kimi K2

Kimi K2 has built the most complete Agent training data synthesis pipe in the current open message:

1. ** Tool collection**: extracting the true tool definition from 3,000+ GitHub MCP tool libraries
** Tool extensions**: Synthetic generation of 2000+ tool definitions based on real tools - expanding coverage through changing parameters, combination functions, simulation of new tools
**Trail generation**: Multiple rounds of interactive tracks on synthesis tools, using strong models already in place - including complex scenarios such as tool calls, result resolution, bug processing, multistep reasoning etc.
4. **Quality filter**: Multidimensional quality filter of the orbits generated and retention of high-quality training data

The key insight of this stream is that the training bottlenecks in Agent's capabilities are not algorithms, but rather data — high quality Agent interactive data are extremely scarce and must be manufactured on a large scale through synthetic methods.

##4.3.2 Agent Swarm and PARL framework for Kimi K2.5

Kimi K2.5 further advanced Agent capabilities on K2, introducing two key innovations.

**Agent Swarm**

A few days ago, a group of bloggers from the United States of America, Agent Swarm, was created to work with a multi-Agent collaboration structure:
- **Orchestor**: task decomposition and sub-Agent dispatch
- **SubAgent**: Use of tools (e.g. code execution, file operation, search, etc.) with specific focus on specific areas
- ** Decoder design**: Arranger trained, subAgent frozen

The layouts do not need to train all sub-Agents simultaneously, which significantly reduces the complexity of the training.

**Parlel Agent DevelopmentLarning**

PARL addresses efficiency issues in the Agent RL training: the traditional Agent RL requires a serial execution tool to be used and interacts with the environment, resulting in extremely low utilization of GPU (a significant amount of time waiting for environmental return). PARL, by paralleling multiple Agent rollout processes, duplicates waiting time with calculation time, and the actual delay is reduced by 3 to 4.5 times.

**Togle Inspired**

Kimi K2.5 also proposed an inspirational strategy for Toggle: whether to activate the reflection model in the light of mission characteristics or not, in reasoning, a reduction of 25-30 per cent in token was achieved, with little loss of performance.

** Visual Agent ability**

Kimi K2.5 visual ability is based on **MoonViT-3D visual encoder**: four frames of space are used to achieve four times the time dimension compression. One surprising finding is **0 samples of visual SFT**: using text data alone to activate visual reasoning without visual labelling. This suggests that the trans-models created during the pre-training phase are strong enough.

Further cross-moderated RL enhancements show that visual RL not only enhances visual performance, but also reverses the pure text task — MMLU-Pro + 1.7, GPQA +2.1. This suggests potential positive migration effects of trans-module training signals.

## 4.3.3 Slime RL infrastructure for GLM-5

Slime, a dedicated asymmetric framework built by GLM-5 for the Agent RL training, addresses the core efficiency bottleneck of Agent RL - Agent needs interact with the environment (code sandboxes, terminals, browsers, etc.), each with IO delays and a very low utilization of GPUs for traditional synchronized RLs.

Slime's key design:
- **Limentation-training complete decoupling**: Logic engines continue to generate Agent tracks, and when the number of tracks reaches the threshold, batches are sent to the training engine, and the training engine is re-returned to the reasoning engine after each K update
- **1000+ and Rollout**: Joint training of the hesitancy load through micro-service task registration for more than 1,000 Agent interactions with the environment
- **TIO Gateway (Token-In-Token-Out)** Intercept all requests for the generation of reasoning engines, record token IDs and metadata from each trajectory, ensure accurate tokenization from the use of reasoning engines at the training end, and avoid re-aligning errors resulting from tokenization
- **DP perceptive route**: Using Consistency Hash to route the same rollout request to the same data parallel rank to maximize KV-cache reuse

GLM-5 covers over 10,000 verifiable environments (GitHub warehouses across nine programming languages), installs and relies on the RepoLaunch framework to analyse the warehouse automatically and generates test cases through LLM-driven log-slating.

# 4.3.4 Forge RL system for MiniMax M2

Although the technical report of MiniMax M3 focuses mainly on structural innovation, the **Forge RL system, developed in its predecessor version M2,** provides engineering references for Agent RL training. Forge is a common RL training platform that supports a flexible mix of incentive signals and training algorithms.

---

# V. Horizontal contrast of key technological innovations

#5.1 Structure dimensions

<unk> DeepSeek V4 Pro <unk> Kwen 3<unk> Ki K2<unk> GLM-5<unk> MiniMax M3<unk> M3<unk> TurboS<unk>
|------|----------------|--------|---------|-------|------------|-----------|
**Total/activating ** <unk> 1.6T/49B<unk> 235B/22B<unk> 1.04T/32.6B<unk> 744B/40B<unk> 428B/23B<unk> 56B<unk>
**Arrangement** <unk> MoE<unk> MoE<unk> MoE<unk> MoE<unk> ME<unk> Mamba-TF mix
**CSA+HCA<unk> GQA+QK-Nom<unk> MLA<unk> DSA<unk> MSA<unk> GQA(7th Floor)<unk>
<unk> ** Optimizer** <unk> Muon<unk> Unpublished <unk> MuonClip<unk> Muon Split<unk> Unpublished <unk>
<unk> **Deficiency connection** <unk> mHC current binding <unk> Standard <unk> Standard <unk> Standard <unk> Standard <unk> Standard <unk> Standard <unk> Standard <unk> Standard <unk> Standard <unk>
**MTP**<unk> not applicable<unk> not applicable<unk> not applicable<unk> not applicable<unk> 3 head sharing<unk> not applicable<unk> not applicable
** Data volume** <unk> 33T <unk> 36T <unk> 15.5T <unk> 28.5T <unk> unpublished <unk> 16T <unk>

> Supplementary: DeepSeek V4 Flash (284B/13B), Step 3.5 Flash (196B/11B, MFA+SWA, Muon+Polar, 3 MTP, 17.2T), MiMo-V2-Flash (309B/15B, SWA+GA, multiple head MTP, 27T) parameters are detailed in the general table.

#5.2 Post-training dimensions

<unk> DeepSeek V4<unk> <unk> wen 3<unk> GLM-5<unk> TurboS<unk> Step 3.5 Flash<unk> MiMo-V2-Flash<unk>
|------|------------|--------|-------|-----------|---------------|---------------|
<unk> ** Post-training core** <unk> OPD distillation replacing RL <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk>
<unk> **Consumption mode** <unk> Level 3 Strength <unk> / think/no_think <unk> 3 modes <unk> since the application of CoT <unk> unpublicized <unk>
<unk> ** Distillation** <unk> OPD hyphenated tablelogit(10+ teacher) <unk> strong to weak (1/10 GPU) <unk> cross-stage anti-forgotten <unk> <unk> <unk> <unk> MVPD token level reward <unk>
<unk> Training stability** <unk> Predictive route +SwiGLU<unk> Unpublished <unk> Unpublished <unk> Pollar Express (1 stepke) <unk> Unpublished

# 5.3 Logic efficiency versus Agent dimension

<unk> DeepSeek V4<unk> Ki K2/K2.5<unk> GLM-5<unk> MiniMax M3<unk> Turbos<unk> MiMo-V2-Flash<unk>
|------|------------|-------------|-------|------------|-----------|---------------|
<unk> ** Rationale** <unk> KV cache 10% of V3 <unk> 25-30% token reduction (Togle) <unk> Acceptance of 2.76 length <unk> 28.4 times less attention <unk> O(n) linear <unk> 2.6 times MTP acceleration <unk>
<unk> Agent training** <unk> not applicable <unk> 30+MCP/20000+ tool; <unk> Agent Swarm/PARL<unk> Slime appetizer RL(1,000+)<unk> Forge RL<unk> not applicable <unk> not applicable <unk>
** representative base** <unk> SWE-bnch 80.6%, Codeforces 326% <unk> unpublished AA Intellity v4 first 50% separated <unk> LMSYS #7156 <unk> SWE-bench 73.4% <unk>

> "Not applicable" in the table indicates that the model does not address the direction of the technology, and "not publicly" indicates that the technical report does not provide relevant data.

** GLM-5 assessment supplement**: GLM-5 reached 50 points on Artificial Analysis Intelligence Index v.0, becoming the first open source weight model to reach this score. Its subsequent version GLM-5.2 ranks first in the global available model in Code Arena, Terminal-Bench 2.1 to 81, SWE-bench Pro 62.1, narrows the gap to 1 to 4 per cent with Claude Opus 4.8.

---

# VI. TRENDS AND ASPECTS

#6.1 Five definitive trends

Trends I: MoE engineering capabilities become core competitiveness

Eight of the nine models use MoE, with the only exception (Mamba-Transformer mix of the hybrid TurboS) containing the MoE layer itself. The Dense structure has completely withdrawn from the stage in the flagship model. When DeepSeek V4 behaves as the 49B activation parameter for the 1.6T total parameter, it is difficult for any team to train a 1.6T Dense model.

This means that MoE's engineering capacity — road stability, expert load balance, All-to-All communications optimization — is becoming a core competitive barrier for large model teams.

# Trend two: focus on the flowers

CSA/HCA, MSCA, DSA, MFA, SWA+GA - each major model has presented its own unique distraction options. The standard full attention mechanism has been agreed on in a long context, but the best alternatives have not yet been reduced.

Trends III: Muon Optimizer replaces AdamW

DeepSeek V4, Kimi K2, GLM-5, Step 3.5 Flash – four models explicitly adopted Muon or its variants. AdamW ruled the map of the deep learning optimiser over the last decade, and Muon was the first alternative to proven superiority in large-scale pre-training.

Trend four: Distillation is replacing traditional RL

The OPD of DeepSeek V4 and MOPD of MiMo-V2-Flash represent a trend towards a possible change in the training paradigm:** the replacement (or significant reduction) of traditional RL** with distillation.

Bottom logic is clear: RL rewards are measured and information density is low; distilled "reward signals" are the probability distribution of the entire table, with several orders of magnitude with information density; RL training is unstable and distillation is more stable; RL requires a large number of rollout calculations and distillation calculations are more efficient.

But distillation has a fundamental limitation: it requires a stronger teacher model than the student. Where does the teacher come when the "best model" is trained? DeepSeek V4 answers "field specialists" - training to a highly skilled expert model in a given field, and even if the overall capacity is less than the final model, it provides an effective teacher signal in their respective fields.

## Trend V: Agent ability becomes the core dimension of competition

Agent data synthesizing waterlines (3,000+ MCP tools <unk> 20++ synthesis tools) of Kimi K2/K2.5, Slime agt RL infrastructure (1,000+roundout) of GLM-5, and Forge RL system of MiniMax M2 — teams invested a great deal of engineering resources in Agent training.

The importance of Agent capabilities stems from the demand-driven demands at the application level: the big model evolves from "answer questions" to "delivering tasks" and uses tools, interactions with the environment, and multistep tasks. These capabilities cannot be obtained through simple language modelling, and require specific training methods and data. Kimi K2's strong performance on Agent benchmarks such as SWE-bench, and DeepSeek V4's 80.6% success on SWE-Bench Verified, all attesting to this direction.

# 6.2 Open issues

# Will a distraction be a uniform paradigm?

At least five different design philosophys (compression, selection, window, linear, blending) are currently available. Will they eventually absorb one of the best options, as MoE has harmonized model architecture?

** Arguments that tend not to be **: different programmes have different objectives - CSA/HCA optimizes KV cache size, MSC optimizes calculations, SWA optimizes simplicity, Mamba optimizes theory complexity. There is a fundamental trade-off between these objectives.

** The argument in favour of **: the final market will choose the most efficient option in combination, as Transformer has harmonized RNN/CNN/Attenion competition. The CSA+HCA of DeepSeek V4 now has the best integrated balance on KV Creaking + Calculating Efficiency, and it is likely to become a de facto standard.

# # Can distillation completely replace RL?

DeepSeek V4 OPD has completely replaced traditional RL with distillation in practice. If the strongest models also rely on distillation, where does "teacher" come from?

Possible answers:
1. ** Course of experts in the field** (DeepSeek V4 is on the move): training of experts in a number of fields, each reaching extreme levels in its own field and then distilling together
2. ** Self-distillation route**: model is being upgraded through iterative improvements using its own historical version as a teacher
3. **RL+ Diffusion mixed route**: RL used to explore capability boundaries and distillation used to efficiently disseminate existing knowledge

The very simple RL result of Qwen 3 suggests another possibility: maybe a small amount of high quality RL is enough, distilling most of the remaining work. The future training paradigm may be a combination of "a small amount RL exploration plus substantial distillation."

#Mamba-Transformer mix is the future?

The hybrid TurboS uses only 7 layers of attention (5.5%) of 128 layers to prove the feasibility of the Mamba-Transformer hybrid structure. But it needs to be noted that the hybrid TurboS is the only one in nine models to use this structure; Mamba still has theoretical limitations on tasks such as location search; and the linear complexity advantage is not apparent in short sequence scenarios, and only in long sequences (>64K).

The Mamba-Transformer mix is likely to be a valuable alternative route, especially in long contexts and low-delay scenarios. Whether it will replace the purely Transformer+MoE mainstream is not sufficiently substantiated to conclude.

---

# Final remarks

Looking back at the 2025-2026 fundamental model competition, three judgements surfaced. First, the architecture-level innovation space was far from closed -- attention was scarce, Mamba mix, mHC disability connection were fast evolving, and the "Transformer is the end state" assumption was broken. Second, the post-training paradigm was undergoing a shift from "RL-led" to "distillated-led" and the extremes of DeepSeek V4 OPD and Qwen 3 demonstrated that. Third, Agent capabilities were becoming the core delivery vehicle for model values, and input from data synthesis and the off-the-road RL infrastructure would determine the next stage of competition.

For practitioners, the recommendations focus on three directions: the low-profile engineering landing (which will directly affect the upper limit of the reasoning costs and the length of the context), the practical methodology of online strategy distillation (especially the training and portfolio strategy of field experts) and the construction of Agent data synthesis waterlines (the biggest bottleneck in the current Agent capacity enhancement).

** Practice recommendations for teams of different sizes**:
- **kcal team**: Qwen 3 route (Standard GQA+Extra-Simplified RL) recommended, with minimal technical risk, engineering complexity controlled, open source weights and adequate community validation
- **Hanka team**: The DeepSeek V4 route (CSA/HCA+OPD) could be considered, but significant engineering resources would be required to invest in a dilution and distillation infrastructure, with engineering thresholds for road stability and FP4 quantitative perception training not low
- **Agent orientation**: Synthetic waterlines (3,000+MCP tools ~2000+ synthesis tools) with reference to Kimi K2/K2.5, which is the most complete option in the current public information; while the Slime antagonism RL infrastructure of GLM-5 provides a frame of reference for the engineering of Agent RL

---

# References

1. DeepSeek V4 Technical Report, DeepSeek, 2025.
2. Qwen 3 Technical Report, Alibaba Qwen Team, 2025.
3. Kimi K2 Technical Report, Moonshot AI, 2025.
4. Kimi K2.5 Technical Report, Moonshot AI, 2025-2026.
5. GLM-5 Technical Report, Zhipu AI, 2025.
6. MiniMax M3 Technical Report, MiniMax, 2025.
7. The hybrid Turbos Technical Report, Tencent Hunyuan, 2025.
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
18. DeepSeek-GRM: Advancing Generative Reward Models, DeepSeek, 2025. arXiv:2504.02495
19. Fine-grained MoE: Exponential Expressivity Growth via Expert Granularity, 2025. arXiv:2505.06839

---

* This paper is based on the open technical report, which draws all data and technical details from the source.
