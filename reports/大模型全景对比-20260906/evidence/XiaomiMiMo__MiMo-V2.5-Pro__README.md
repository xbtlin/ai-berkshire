---
license: mit
language:
- en
- zh
tags:
- text-generation
- agent
- long-context
- code
- transformers
library_name: transformers
---

<br/><br/>

<div align="center">
  <picture>
    <source srcset="https://github.com/XiaomiMiMo/MiMo/raw/main/figures/Xiaomi_MiMo_darkmode.png?raw=true" media="(prefers-color-scheme: dark)">
    <img src="https://github.com/XiaomiMiMo/MiMo/raw/main/figures/Xiaomi_MiMo.png?raw=true" width="60%" alt="Xiaomi-MiMo" />
  </picture>
</div>

<br/>

<div align="center" style="line-height: 1;">
  |
  <a href="https://huggingface.co/XiaomiMiMo" target="_blank">🤗 HuggingFace</a>
  &nbsp;|
  <a href="https://mimo.xiaomi.com/mimo-v2-5-pro" target="_blank">📰 Blog </a>
  &nbsp;|
  <a href="https://platform.xiaomimimo.com/" target="_blank">🎨 Xiaomi MiMo API Platform </a>
  &nbsp;|
  <a href="https://aistudio.xiaomimimo.com" target="_blank">🗨️ Xiaomi MiMo Studio </a>
  &nbsp;|
</div>

<br/>

<div align="center" style="line-height: 1.2;">
  <strong>Community</strong><br/>
  <a href="https://huggingface.co/XiaomiMiMo/MiMo-V2.5-Pro/blob/main/assets/wechat.jpg" target="_blank">WeChat Group</a>
  &nbsp;|&nbsp;
  <a href="https://discord.gg/kKC2kNnQEX" target="_blank">Discord</a>
  &nbsp;|&nbsp;
  <a href="https://t.me/+3T-I0pekOVIyNDBl" target="_blank">Telegram</a>
  &nbsp;|&nbsp;
  <a href="https://www.reddit.com/r/XiaomiMiMo_Official/" target="_blank">Reddit</a>
</div>

<br/>

# MiMo-V2.5-Pro

MiMo-V2.5-Pro is an open-source Mixture-of-Experts (MoE) language model with 1.02T total parameters and 42B active parameters. It utilizes the hybrid attention architecture and 3-layers Multi-Token Prediction (MTP) introduced in [MiMo-V2-Flash](https://github.com/XiaomiMiMo/MiMo-V2-Flash), with up to 1M tokens context length.

<div align="center">
  <img src="assets/benchmark.jpg" width="90%" alt="Benchmark Results" />
</div>

## 1. Introduction

MiMo-V2.5-Pro is our most capable model to date, designed for the most demanding agentic, complex software engineering, and long-horizon tasks. It sustains complex trajectories spanning thousands of tool calls with strong instruction following and coherence over a 1M-token context window. Key features include:

- **Hybrid Attention Architecture**: Interleaves Sliding Window Attention (SWA) and Global Attention (GA) with a 6:1 ratio and 128 sliding window. This reduces KV-cache storage by nearly 7x while maintaining long-context performance via learnable attention sink bias.
- **Multi-Token Prediction (MTP)**: Equipped with three lightweight MTP modules using dense FFNs. This triples output speed during inference and will be good to accelerate rollout in RL training.
- **Efficient Pre-Training**: Trained on 27T tokens using FP8 mixed precision and native 32k seq length. The context window supports up to 1M tokens.
- **Agentic Capabilities**: Post-training utilizes SFT, large-scale agentic RL and Multi-Teacher On-Policy Distillation (MOPD), achieving superior performance on the most demanding agentic, complex software engineering, and long-horizon tasks.

## 2. Model Downloads

| Model | Total Params | Active Params | Context Length | Precision | Download |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **MiMo-V2.5-Pro** | 1.02T | 42B | 1M | FP8 (E4M3) Mixed | [🤗 HuggingFace](https://huggingface.co/XiaomiMiMo/MiMo-V2.5-Pro) <br> [🤖 ModelScope](https://modelscope.cn/models/XiaomiMiMo/MiMo-V2.5-Pro) |
| **MiMo-V2.5-Pro-Base** | 1.02T | 42B | 256K | FP8 (E4M3) Mixed | [🤗 HuggingFace](https://huggingface.co/XiaomiMiMo/MiMo-V2.5-Pro-Base) <br> [🤖 ModelScope](https://modelscope.cn/models/XiaomiMiMo/MiMo-V2.5-Pro-Base) |

## 3. Evaluation Results

### Base Model Evaluation

| Category | Benchmark | Setting | MiMo-V2.5-Pro Base | MiMo-V2.5 Base | DeepSeek-V4-Pro Base | DeepSeek-V4-Flash Base | Kimi-K2 Base |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Params** | #Activated / #Total | - | 42B / 1.02T | 15B / 310B | 49B / 1.6T | 13B / 284B | 32B / 1.04T |
| **General** | BBH | 3-shot | 88.4 | 87.2 | 87.5 | 86.9 | 88.7 |
| | MMLU | 5-shot | 89.4 | 86.3 | 90.1 | 88.7 | 87.8 |
| | MMLU-Redux | 5-shot | 92.8 | 89.8 | 90.8 | 89.4 | 90.2 |
| | MMLU-Pro | 5-shot | 68.5 | 65.8 | 73.5 | 68.3 | 69.2 |
| | DROP | 3-shot | 86.3 | 83.7 | 88.7 | 88.6 | 83.6 |
| | ARC-Challenge | 25-shot | 97.2 | 96.5 | - | - | 96.2 |
| | HellaSwag | 10-shot | 89.8 | 88.6 | 88.0 | 85.7 | 94.6 |
| | WinoGrande | 5-shot | 85.6 | 84.7 | 81.5 | 79.5 | 85.3 |
| | TriviaQA | 5-shot | 81.3 | 80.7 | 85.6 | 82.8 | 85.1 |
| | GPQA-Diamond | 5-shot | 66.7 | 58.1 | - | - | 48.1 |
| **Math** | GSM8K | 8-shot | 99.6 | 83.3 | 92.6 | 90.8 | 92.1 |
| | MATH | 4-shot | 86.2 | 67.7 | 64.5 | 57.4 | 70.2 |
| | AIME 24&25 | 2-shot | 37.3 | 36.9 | - | - | 31.6 |
| **Code** | HumanEval+ | 1-shot | 75.6 | 71.3 | - | - | 84.8 |
| | MBPP+ | 3-shot | 74.1 | 70.9 | - | - | 73.8 |
| | LiveCodeBench v6 | 1-shot | 39.6 | 35.5 | - | - | 26.3 |
| | SWE-Bench (AgentLess) | 3-shot | 35.7 | 30.8 | - | - | 28.2 |
| **Chinese** | C-Eval | 5-shot | 91.5 | 88.6 | 93.1 | 92.1 | 92.5 |
| | CMMLU | 5-shot | 90.2 | 88.2 | 90.8 | 90.4 | 90.9 |
| **Multilingual** | GlobalMMLU | 5-shot | 83.6 | 77.4 | - | - | 80.7 |

### Long-context Evaluation

<div align="center">
  <img src="assets/post_training_evaluation.jpg" width="80%" alt="Post-training Evaluation" />
</div>

GraphWalks is a long-context benchmark from OpenAI that fills the prompt with a directed graph of hex-hash nodes and asks the model to run a breadth-first search (nodes exactly at depth *N*) or list a node's parents. We evaluate across the full 32k–1M input-token span and apply the same evaluation fixes described by Anthropic.

MiMo V2.5 Pro delivers a major leap in long-context reasoning. Past 128k, V2 Pro degrades rapidly and collapses to 0.00 at 1M on both subtasks, while V2.5 Pro still scores 0.56 BFS / 0.92 Parents at 512k and 0.37 / 0.62 at 1M.

## 4. Model Architecture & Training Process

MiMo-V2.5-Pro addresses the quadratic complexity of long contexts by interleaving Local Sliding Window Attention (SWA) and Global Attention (GA). Unlike traditional speculative decoding, our MTP module is natively integrated for training and inference.

<div align="center">
  <img src="assets/architecture.png" width="60%" alt="Model Architecture" />
</div>

### Model Summary

| Component | MiMo-V2.5-Pro | MiMo-V2.5 |
| :--- | :---: | :---: |
| **Total Parameters** | 1.02T | 310B |
| **Activated Parameters** | 42B | 15B |
| **Hidden Size** | 6144 | 4096 |
| **Num Layers** | 70 (1 dense + 69 MoE) | 48 (1 dense + 47 MoE)|
| **Full Attention Layers** | 10 | 9 |
| **SWA Layers** | 60 | 39 |
| **Num Attention Heads** | 128 | 64 |
| **Num KV Heads** | 8 (GQA) | 8 (GA) / 4 (SWA) |
| **Head Dim (QK / V)** | 192 / 128 | 192 / 128 |
| **Routed Experts** | 384 | 256 |
| **Experts per Token** | 8 | 8 |
| **MoE Intermediate Size** | 2048 | 2048 |
| **Dense Intermediate Size** | 16384 (layer 0 only) | 16384 (layer 0 only) |
| **SWA Window Size** | 128 | 128 |
| **Max Context Length** | 1M | 1M |
| **MTP Layers** | 3 | 3 |

### Training Process

For post-training, MiMo-V2.5-Pro adopts the three-stage post-training paradigm introduced in [MiMo-V2-Flash](https://github.com/XiaomiMiMo/MiMo-V2-Flash) to achieve exceptional performance. The paradigm begins with Supervised Fine-Tuning (SFT) to build strong, foundational instruction-following skills using curated data pairs. Next, in the Domain-Specialized Training stage, diverse teacher models — ranging from math and safety to complex agentic tool-use — are individually optimized using domain-specific RL rewards. Finally, the process culminates in Multi-Teacher On-Policy Distillation (MOPD). Through dynamic on-policy RL, the single student model iteratively learns from its own outputs, continuously receiving precise token-level guidance from the expert teachers to seamlessly integrate broad capabilities.

## 5. Deployment

Since inference engines are continuously being updated and optimized, this guide only provides deployment examples for reference. For the best performance, we strongly recommend following our referenced approach to get the latest best practices and optimal performance.

### SGLang Deployment

For the best performance, we strongly recommend deploying using this approach, which is officially supported by the SGLang community. Please refer to [SGLang MiMo-V2.5-Pro Cookbook](https://docs.sglang.io/cookbook/autoregressive/Xiaomi/MiMo-V2.5) for the latest deployment guide.

The following is an example of running the model with SGLang, referenced from [sgl-project/sglang#23808](https://github.com/sgl-project/sglang/pull/23808):

```bash
SGLANG_ENABLE_SPEC_V2=1
SGLANG_DEEPEP_NUM_MAX_DISPATCH_TOKENS_PER_RANK=256
python3 -m sglang.launch_server \
              --model-path XiaomiMiMo/MiMo-V2.5-Pro \
              --trust-remote-code \
              --pp-size 1 \
              --dp-size 2 \
              --ep-size 16 \
              --tp-size 16 \
              --moe-dense-tp-size 1 \
              --enable-dp-attention \
              --moe-a2a-backend deepep \
              --dist-init-addr ${LWS_LEADER_IP}:20000 \
              --node-rank ${LWS_WORKER_INDEX} \
              --nnodes ${LWS_GROUP_SIZE} \
              --page-size 64 \
              --attention-backend fa3 \
              --quantization fp8 \
              --mem-fraction-static 0.7 \
              --max-running-requests 128 \
              --cuda-graph-max-bs 64 \
              --chunked-prefill-size 32768 \
              --context-length 1048576 \
              --tokenizer-worker-num 64 \
              --speculative-algorithm EAGLE \
              --speculative-num-steps 3 \
              --speculative-eagle-topk 1 \
              --speculative-num-draft-tokens 4 \
              --enable-multi-layer-eagle \
              --host 0.0.0.0 \
              --port 9001 \
              --reasoning-parser mimo \
              --tool-call-parser mimo \
              --watchdog-timeout 3600 \
              --model-loader-extra-config '{"enable_multithread_load": "true","num_threads": 64}'
```

### vLLM Deployment

For the best performance, we strongly recommend deploying using this approach, which is officially supported by the vLLM community. Please refer to [vLLM MiMo-V2.5-Pro Cookbook](https://recipes.vllm.ai/XiaomiMiMo/MiMo-V2.5-Pro) for the latest deployment guide.

For local deployment, we recommend setting the sampling parameters to `temperature=1.0`, `top_p=0.95`.

## Citation

```bibtex
@misc{mimo2026v25pro,
  title={MiMo-V2.5-Pro},
  author={{Xiaomi MiMo Team}},
  year={2026},
  howpublished={\url{https://huggingface.co/collections/XiaomiMiMo/mimo-v25}},
}
```

## Contact

For questions or feedback, reach us at [mimo@xiaomi.com](mailto:mimo@xiaomi.com) or join our community:

- [WeChat Group](https://work.weixin.qq.com/apph5/external_room/join/group_mng?plg_id=c417f99bd9014b5dd894daa8bfe19790&)
- [Discord](https://discord.gg/WX2R2uNp)
- [Telegram](https://t.me/+3T-I0pekOVIyNDBl)
- [Reddit](https://www.reddit.com/r/XiaomiMiMo_Official/)