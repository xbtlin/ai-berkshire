---
pipeline_tag: image-text-to-text
license: other
license_name: minimax-community
license_link: LICENSE
library_name: transformers
tags:
  - multimodal
  - moe
  - agent
  - coding
  - video
---

<div align="center">
  <img width="60%" src="figures/logo.svg" alt="MiniMax">
</div>
<hr>

<p align="center">
  <a href="https://agent.minimax.io/" target="_blank"><img src="https://img.shields.io/badge/MiniMax%20Agent-FF6C37?logo=minimax&logoColor=white" alt="MiniMax Agent"></a>
  <a href="https://platform.minimax.io/docs/guides/text-generation" target="_blank"><img src="https://img.shields.io/badge/API-FF6C37?logo=minimax&logoColor=white" alt="API"></a>
  <a href="https://www.minimax.io" target="_blank"><img src="https://img.shields.io/badge/MiniMax%20Website-FF6C37?logo=minimax&logoColor=white" alt="MiniMax Website"></a>
  <br>
  <a href="https://modelscope.cn/organization/minimax" target="_blank" rel="noopener noreferrer"><img alt="ModelScope MiniMax AI" src="https://img.shields.io/badge/ModelScope-MiniMax%20AI-white?labelColor=%23EF3D5D"></a>
  <a href="https://platform.minimaxi.com/docs/faq/contact-us" target="_blank"><img src="https://img.shields.io/badge/WeChat-07C160?logo=wechat&logoColor=white" alt="WeChat"></a>
  <a href="https://discord.com/invite/DPC4AHFCBw" target="_blank"><img src="https://img.shields.io/badge/Discord-5865F2?logo=discord&logoColor=white" alt="Discord"></a>
  <a href="https://huggingface.co/MiniMaxAI" target="_blank"><img src="https://img.shields.io/badge/Hugging%20Face-FFD21E?logo=huggingface&logoColor=black" alt="Hugging Face"></a>
  <a href="https://github.com/MiniMax-AI/MiniMax-M3" target="_blank"><img src="https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white" alt="GitHub"></a>
  <a href="https://arxiv.org/abs/2606.13392" target="_blank"><img src="https://img.shields.io/badge/arXiv-2606.13392-B31B1B?logo=arxiv&logoColor=white" alt="arXiv Paper"></a>
  <a href="https://huggingface.co/MiniMaxAI/MiniMax-M3/blob/main/LICENSE" target="_blank"><img src="https://img.shields.io/badge/LICENSE-4CAF50?logo=creativecommons&logoColor=white" alt="LICENSE"></a>
</p>

MiniMax-M3 is a native multimodal model with 1M context. It has ~428B parameters and ~23B activated parameters.

**Highlights:**
- **Native Multimodality:** M3 undergoes mixed-modality training from the very first step, enabling deeper semantic fusion across text, image, and video.
- **Context Scaling via Sparse Attention:** M3 introduces MiniMax Sparse Attention (MSA) to improve long context efficiency. M3 delivers 9× prefill and 15× decode speedups compared to M2 at 1M context, reducing per-token compute to 1/20.
- **Coding & Cowork Capability:** M3 achieves frontier-level performance across long-horizon agentic benchmarks, excelling in both coding and cowork.


<p align="center">
  <img width="100%" src="figures/benchmark.jpeg">
</p>

## MiniMax Sparse Attention (MSA)

M3 is powered by [**MiniMax Sparse Attention (MSA)**](https://github.com/MiniMax-AI/MSA), a high-performance sparse attention operator designed for million-token contexts. Compared with GQA, MSA dramatically reduces the attention compute and memory footprint while preserving model quality.

<p align="center">
  <img width="100%" src="figures/efficiency_gqa_vs_msa.png" alt="GQA vs MSA Efficiency Comparison">
</p>

> 📄 Read the technical report: [arXiv:2606.13392](https://arxiv.org/abs/2606.13392) · [Hugging Face Papers](https://huggingface.co/papers/2606.13392)

## How to Use

- [MiniMax Agent](https://agent.minimax.io/)
- [MiniMax API](https://platform.minimax.io/)

M3 supports three reasoning modes through the `thinking` parameter:
- **`enabled`** — Reasoning is always enabled.
- **`adaptive`** — M3 automatically determines when additional reasoning is beneficial.
- **`disabled`** — Reasoning is disabled to minimize latency and maximize throughput.

## Local Deployment

Download the model:

```bash
hf download MiniMaxAI/MiniMax-M3 --local-dir MiniMax-M3
```

We recommend the following inference frameworks to serve the model:

- [SGLang](https://docs.sglang.io/) - see  [SGLang cookbook](https://docs.sglang.io/cookbook/autoregressive/MiniMax/MiniMax-M3).

- [vLLM](https://github.com/vllm-project/vllm) - see [vLLM recipes](https://recipes.vllm.ai/MiniMaxAI/MiniMax-M3).

- [Transformers](https://github.com/huggingface/transformers) - see [Transformers docs](https://huggingface.co/docs/transformers/model_doc/minimax_m3_vl).

- [KTransformers](https://github.com/kvcache-ai/ktransformers) - see [KTransformers MiniMax-M3 tutorial](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/kt-kernel/MiniMax-M3-Tutorial.md).

- [unsloth](https://unsloth.ai) - see [tutorial](https://unsloth.ai/docs/models/minimax-m3)

- [ATOM](https://github.com/ROCm/ATOM/tree/main) - see [MiniMax-M3 MXFP4/MXFP8 Usage Guide](https://github.com/ROCm/ATOM/blob/main/recipes/MiniMax-M3.md)

### Inference Parameters

We recommend the following parameters for best performance: `temperature=1.0`, `top_p=0.95`.

## Contact Us

Contact us at [model@minimax.io](mailto:model@minimax.io).
