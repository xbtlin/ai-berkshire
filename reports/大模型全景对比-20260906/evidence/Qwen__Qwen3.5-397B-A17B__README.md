---
library_name: transformers
license: apache-2.0
license_link: https://huggingface.co/Qwen/Qwen3.5-397B-A17B/blob/main/LICENSE
pipeline_tag: image-text-to-text
---

# Qwen3.5-397B-A17B

<img width="400px" src="https://qianwen-res.oss-accelerate.aliyuncs.com/logo_qwen3.5.png">

[![Qwen Chat](https://img.shields.io/badge/%F0%9F%92%9C%EF%B8%8F%20Qwen%20Chat%20-536af5)](https://chat.qwen.ai)

> [!Note]
> This repository contains model weights and configuration files for the post-trained model in the Hugging Face Transformers format. 
>
> These artifacts are compatible with Hugging Face Transformers, vLLM, SGLang, KTransformers, etc.

> [!Tip]
> For users seeking managed, scalable inference without infrastructure maintenance, the official Qwen API service is provided by [Alibaba Cloud Model Studio](https://modelstudio.alibabacloud.com/).
>
> In particular, **Qwen3.5-Plus** is the hosted version corresponding to Qwen3.5-397B-A17B with more production features, e.g., 1M context length by default, official built-in tools, and adaptive tool use.
> For more information, please refer to the [User Guide](https://www.alibabacloud.com/help/en/model-studio/text-generation).

Over recent months, we have intensified our focus on developing foundation models that deliver exceptional utility and performance. Qwen3.5 represents a significant leap forward, integrating breakthroughs in multimodal learning, architectural efficiency, reinforcement learning scale, and global accessibility to empower developers and enterprises with unprecedented capability and efficiency.

## Qwen3.5 Highlights

Qwen3.5 features the following enhancement:

- **Unified Vision-Language Foundation**: Early fusion training on multimodal tokens achieves cross-generational parity with Qwen3 and outperforms Qwen3-VL models across reasoning, coding, agents, and visual understanding benchmarks.

- **Efficient Hybrid Architecture**: Gated Delta Networks combined with sparse Mixture-of-Experts deliver high-throughput inference with minimal latency and cost overhead.

- **Scalable RL Generalization**: Reinforcement learning scaled across million-agent environments with progressively complex task distributions for robust real-world adaptability.

- **Global Linguistic Coverage**: Expanded support to 201 languages and dialects, enabling inclusive, worldwide deployment with nuanced cultural and regional understanding.

- **Next-Generation Training Infrastructure**: Near-100% multimodal training efficiency compared to text-only training and asynchronous RL frameworks supporting massive-scale agent scaffolds and environment orchestration.


![Benchmark Results](https://qianwen-res.oss-accelerate.aliyuncs.com/Qwen3.5/Figures/qwen3.5_397b_a17b_score.png)

For more details, please refer to our blog post [Qwen3.5](https://qwen.ai/blog?id=qwen3.5).


## Model Overview

- Type: Causal Language Model with Vision Encoder
- Training Stage: Pre-training & Post-training
- Language Model
    - Number of Parameters: 397B in total and 17B activated
    - Hidden Dimension: 4096
    - Token Embedding: 248320 (Padded)
    - Number of Layers: 60
        - Hidden Layout: 15 \* (3 \* (Gated DeltaNet -> MoE) -> 1 \* (Gated Attention -> MoE))
    - Gated DeltaNet:
        - Number of Linear Attention Heads: 64 for V and 16 for QK
        - Head Dimension: 128
    - Gated Attention:
        - Number of Attention Heads: 32 for Q and 2 for KV
        - Head Dimension: 256
        - Rotary Position Embedding Dimension: 64
    - Mixture Of Experts
        - Number of Experts: 512
        - Number of Activated Experts: 10 Routed + 1 Shared
        - Expert Intermediate Dimension: 1024
    - LM Output: 248320 (Padded)
    - MTP: trained with multi-steps  
- Context Length: 262,144 natively and extensible up to 1,010,000 tokens.

## Benchmark Results

### Language

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:900px;margin:0 auto;padding:16px 0">
<table style="width:100%;border-collapse:collapse;font-size:13px">
<thead><tr>
<th style="padding:10px 12px;text-align:left;font-weight:600;border-bottom:2px solid #7c3aed;color:#7c3aed"></th>
<th style="padding:10px 12px;text-align:center;font-weight:500;border-bottom:2px solid #7c3aed;color:#7c3aed;font-size: 14px;">GPT5.2</th>
<th style="padding:10px 12px;text-align:center;font-weight:500;border-bottom:2px solid #7c3aed;color:#7c3aed;font-size: 14px;">Claude 4.5 Opus</th>
<th style="padding:10px 12px;text-align:center;font-weight:500;border-bottom:2px solid #7c3aed;color:#7c3aed;font-size: 14px;">Gemini-3 Pro</th>
<th style="padding:10px 12px;text-align:center;font-weight:500;border-bottom:2px solid #7c3aed;color:#7c3aed;font-size: 14px;">Qwen3-Max-Thinking</th>
<th style="padding:10px 12px;text-align:center;font-weight:500;border-bottom:2px solid #7c3aed;color:#7c3aed;font-size: 14px;">K2.5-1T-A32B</th>
<th style="padding:10px 12px;text-align:center;font-weight:500;border-bottom:2px solid #7c3aed;color:#7c3aed;font-size: 14px;">Qwen3.5-397B-A17B</th>
</tr></thead>
<tbody>
<tr><td colspan="7" style="padding:8px 12px;font-weight:600;color:#7c3aed;border-bottom:1px solid rgba(124, 58, 237, 0.2);background:rgba(124, 58, 237, 0.1)">Knowledge</td></tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">MMLU-Pro</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">87.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">89.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">89.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">85.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">87.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">87.8</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">MMLU-Redux</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">95.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">95.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">95.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">92.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">94.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">94.9</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">SuperGPQA</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">67.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">70.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">74.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">67.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">69.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">70.4</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">C-Eval</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">90.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">92.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">93.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">93.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">94.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">93.0</td>
</tr>
<tr><td colspan="7" style="padding:8px 12px;font-weight:600;color:#7c3aed;border-bottom:1px solid rgba(124, 58, 237, 0.2);background:rgba(124, 58, 237, 0.1)">Instruction Following</td></tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">IFEval</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">94.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">90.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">93.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">93.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">93.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">92.6</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">IFBench</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">75.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">58.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">70.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">70.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">70.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">76.5</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">MultiChallenge</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">57.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">54.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">64.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">63.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">62.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">67.6</td>
</tr>
<tr><td colspan="7" style="padding:8px 12px;font-weight:600;color:#7c3aed;border-bottom:1px solid rgba(124, 58, 237, 0.2);background:rgba(124, 58, 237, 0.1)">Long Context</td></tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">AA-LCR</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">72.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">74.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">70.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">68.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">70.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">68.7</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">LongBench v2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">54.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">64.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">68.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">60.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">61.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">63.2</td>
</tr>
<tr><td colspan="7" style="padding:8px 12px;font-weight:600;color:#7c3aed;border-bottom:1px solid rgba(124, 58, 237, 0.2);background:rgba(124, 58, 237, 0.1)">STEM</td></tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">GPQA</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">92.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">87.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">91.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">87.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">87.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">88.4</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">HLE</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">35.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">30.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">37.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">30.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">30.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">28.7</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">HLE-Verified¹</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">43.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">38.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">48</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">37.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">37.6</td>
</tr>
<tr><td colspan="7" style="padding:8px 12px;font-weight:600;color:#7c3aed;border-bottom:1px solid rgba(124, 58, 237, 0.2);background:rgba(124, 58, 237, 0.1)">Reasoning</td></tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">LiveCodeBench v6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">87.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">84.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">90.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">85.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">85.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">83.6</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">HMMT Feb 25</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">99.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">92.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">97.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">98.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">95.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">94.8</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">HMMT Nov 25</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">100</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">93.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">93.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">94.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">91.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">92.7</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">IMOAnswerBench</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">86.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">84.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">83.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">83.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">81.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">80.9</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">AIME26</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">96.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">93.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">90.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">93.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">93.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">91.3</td>
</tr>
<tr><td colspan="7" style="padding:8px 12px;font-weight:600;color:#7c3aed;border-bottom:1px solid rgba(124, 58, 237, 0.2);background:rgba(124, 58, 237, 0.1)">General Agent</td></tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">BFCL-V4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">63.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">77.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">72.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">67.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">68.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">72.9</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">TAU2-Bench</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">87.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">91.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">85.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">84.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">77.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">86.7</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">VITA-Bench</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">38.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">56.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">51.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">40.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">41.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">49.7</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">DeepPlanning</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">44.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">33.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">23.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">28.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">14.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">34.3</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">Tool Decathlon</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">43.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">43.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">36.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">18.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">27.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">38.3</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">MCP-Mark</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">57.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">42.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">53.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">33.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">29.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">46.1</td>
</tr>
<tr><td colspan="7" style="padding:8px 12px;font-weight:600;color:#7c3aed;border-bottom:1px solid rgba(124, 58, 237, 0.2);background:rgba(124, 58, 237, 0.1)">Search Agent³</td></tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">HLE w/ tool</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">45.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">43.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">45.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">49.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">50.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">48.3</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">BrowseComp</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">65.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">67.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">59.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">53.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--/74.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">69.0/78.6</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">BrowseComp-zh</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">76.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">62.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">66.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">60.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">70.3</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">WideSearch</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">76.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">76.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">68.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">57.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">72.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">74.0</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">Seal-0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">45.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">47.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">45.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">46.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">57.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">46.9</td>
</tr>
<tr><td colspan="7" style="padding:8px 12px;font-weight:600;color:#7c3aed;border-bottom:1px solid rgba(124, 58, 237, 0.2);background:rgba(124, 58, 237, 0.1)">Multilingualism</td></tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">MMMLU</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">89.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">90.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">90.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">84.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">86.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">88.5</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">MMLU-ProX</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">83.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">85.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">87.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">78.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">82.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">84.7</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">NOVA-63</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">54.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">56.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">56.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">54.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">56.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">59.1</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">INCLUDE</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">87.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">86.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">90.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">82.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">83.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">85.6</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">Global PIQA</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">90.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">91.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">93.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">86.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">89.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">89.8</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">PolyMATH</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">62.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">79.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">81.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">64.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">43.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">73.3</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">WMT24++</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">78.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">79.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">80.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">77.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">77.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">78.9</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">MAXIFE</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">88.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">79.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">87.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">84.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">72.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">88.2</td>
</tr>
<tr><td colspan="7" style="padding:8px 12px;font-weight:600;color:#7c3aed;border-bottom:1px solid rgba(124, 58, 237, 0.2);background:rgba(124, 58, 237, 0.1)">Coding Agent</td></tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">SWE-bench Verified</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">80.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">80.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">76.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">75.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">76.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">76.4</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">SWE-bench Multilingual</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">72.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">77.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">65.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">66.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">73.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">69.3</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">SecCodeBench</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">68.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">68.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">62.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">57.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">61.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">68.3</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">Terminal Bench 2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">54.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">59.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">54.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">22.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">50.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">52.5</td>
</tr>
</tbody>
</table>

<p style="margin-top:12px;font-size:11px;opacity:0.7">
* HLE-Verified: a verified and revised version of Humanity’s Last Exam (HLE), accompanied by a transparent, component-wise verification protocol and a fine-grained error taxonomy. We open-source the dataset at https://huggingface.co/datasets/skylenage/HLE-Verified.<br>
* TAU2-Bench: we follow the official setup except for the airline domain, where all models are evaluated by applying the fixes proposed in the Claude Opus 4.5 system card.<br>
* MCPMark: GitHub MCP server uses v0.30.3 from api.githubcopilot.com; Playwright tool responses are truncated at 32k tokens.<br>
* Search Agent: most search agents built on our model adopt a simple context-folding strategy(256k): once the cumulative Tool Response length reaches a preset threshold, earlier Tool Responses are pruned from the history to keep the context within limits.<br>
* BrowseComp: we tested two strategies, simple context-folding achieved a score of 69.0, while using the same discard-all strategy as DeepSeek-V3.2 and Kimi K2.5 achieved 78.6.<br>
* WideSearch: we use a 256k context window without any context management.<br>
* MMLU-ProX: we report the averaged accuracy on 29 languages.<br>
* WMT24++: a harder subset of WMT24 after difficulty labeling and rebalancing; we report the averaged scores on 55 languages using XCOMET-XXL.<br>
* MAXIFE: we report the accuracy on English + multilingual original prompts (totally 23 settings).<br>
* Empty cells (--) indicate scores not yet available or not applicable.<br>
</p>

</div>

### Vision Language

<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:900px;margin:0 auto;padding:16px 0">
<table style="width:100%;border-collapse:collapse;font-size:13px">
<thead><tr>
<th style="padding:10px 12px;text-align:left;font-weight:600;border-bottom:2px solid #7c3aed;color:#7c3aed"></th>
<th style="padding:10px 12px;text-align:center;font-weight:500;border-bottom:2px solid #7c3aed;color:#7c3aed;font-size: 14px;">GPT5.2</th>
<th style="padding:10px 12px;text-align:center;font-weight:500;border-bottom:2px solid #7c3aed;color:#7c3aed;font-size: 14px;">Claude 4.5 Opus</th>
<th style="padding:10px 12px;text-align:center;font-weight:500;border-bottom:2px solid #7c3aed;color:#7c3aed;font-size: 14px;">Gemini-3 Pro</th>
<th style="padding:10px 12px;text-align:center;font-weight:500;border-bottom:2px solid #7c3aed;color:#7c3aed;font-size: 14px;">Qwen3-VL-235B-A22B</th>
<th style="padding:10px 12px;text-align:center;font-weight:500;border-bottom:2px solid #7c3aed;color:#7c3aed;font-size: 14px;">K2.5-1T-A32B</th>
<th style="padding:10px 12px;text-align:center;font-weight:500;border-bottom:2px solid #7c3aed;color:#7c3aed;font-size: 14px;">Qwen3.5-397B-A17B</th>
</tr></thead>
<tbody>
<tr><td colspan="7" style="padding:8px 12px;font-weight:600;color:#7c3aed;border-bottom:1px solid rgba(124, 58, 237, 0.2);background:rgba(124, 58, 237, 0.1)">STEM and Puzzle</td></tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">MMMU</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">86.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">80.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">87.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">80.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">84.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">85.0</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">MMMU-Pro</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">79.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">70.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">81.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">69.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">78.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">79.0</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">MathVision</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">83.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">74.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">86.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">74.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">84.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">88.6</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">Mathvista(mini)</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">83.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">80.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">87.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">85.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">90.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">90.3</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">We-Math</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">79.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">70.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">86.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">74.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">84.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">87.9</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">DynaMath</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">86.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">79.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">85.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">82.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">84.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">86.3</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">ZEROBench</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">10</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">12</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">ZEROBench_sub</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">33.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">28.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">39.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">28.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">33.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">41.0</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">BabyVision</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">34.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">14.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">49.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">22.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">36.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">52.3/43.3</td>
</tr>
<tr><td colspan="7" style="padding:8px 12px;font-weight:600;color:#7c3aed;border-bottom:1px solid rgba(124, 58, 237, 0.2);background:rgba(124, 58, 237, 0.1)">General VQA</td></tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">RealWorldQA</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">83.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">77.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">83.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">81.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">81.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">83.9</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">MMStar</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">77.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">73.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">83.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">78.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">80.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">83.8</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">HallusionBench</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">65.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">64.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">68.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">66.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">69.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">71.4</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">MMBench<sub><small>EN-DEV-v1.1</small></sub></td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">88.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">89.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">93.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">89.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">94.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">93.7</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">SimpleVQA</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">55.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">65.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">73.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">61.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">71.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">67.1</td>
</tr>
<tr><td colspan="7" style="padding:8px 12px;font-weight:600;color:#7c3aed;border-bottom:1px solid rgba(124, 58, 237, 0.2);background:rgba(124, 58, 237, 0.1)">Text Recognition and Document Understanding</td></tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">OmniDocBench1.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">85.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">87.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">88.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">84.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">88.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">90.8</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">CharXiv(RQ)</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">82.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">68.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">81.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">66.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">77.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">80.8</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">MMLongBench-Doc</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">61.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">60.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">56.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">58.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">61.5</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">CC-OCR</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">70.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">76.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">79.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">81.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">79.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">82.0</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">AI2D_TEST</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">92.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">87.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">94.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">89.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">90.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">93.9</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">OCRBench</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">80.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">85.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">90.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">87.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">92.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">93.1</td>
</tr>
<tr><td colspan="7" style="padding:8px 12px;font-weight:600;color:#7c3aed;border-bottom:1px solid rgba(124, 58, 237, 0.2);background:rgba(124, 58, 237, 0.1)">Spatial Intelligence</td></tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">ERQA</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">59.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">46.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">70.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">52.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">67.5</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">CountBench</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">91.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">90.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">97.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">93.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">94.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">97.2</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">RefCOCO(avg)</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">84.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">91.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">87.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">92.3</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">ODInW13</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">46.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">43.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">47.0</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">EmbSpatialBench</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">81.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">75.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">61.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">84.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">77.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">84.5</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">RefSpatialBench</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">65.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">69.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">73.6</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">LingoQA</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">68.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">78.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">72.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">66.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">68.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">81.6</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">V*</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">75.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">67.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">88.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">85.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">77.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">95.8/91.1</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">Hypersim</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">11.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">12.5</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">SUNRGBD</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">34.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">38.3</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">Nuscene</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">13.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">16.0</td>
</tr>
<tr><td colspan="7" style="padding:8px 12px;font-weight:600;color:#7c3aed;border-bottom:1px solid rgba(124, 58, 237, 0.2);background:rgba(124, 58, 237, 0.1)">Video Understanding</td></tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">VideoMME<sub><small>(w sub.)</sub></small></td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">86</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">77.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">88.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">83.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">87.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">87.5</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">VideoMME<sub><small>(w/o sub.)</sub></small></td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">85.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">81.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">87.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">79.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">83.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">83.7</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">VideoMMMU</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">85.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">84.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">87.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">80.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">86.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">84.7</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">MLVU (M-Avg)</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">85.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">81.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">83.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">83.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">85.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">86.7</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">MVBench</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">78.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">67.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">74.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">75.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">73.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">77.6</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">LVBench</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">73.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">57.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">76.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">63.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">75.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">75.5</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">MMVU</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">80.8</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">77.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">77.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">71.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">80.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">75.4</td>
</tr>
<tr><td colspan="7" style="padding:8px 12px;font-weight:600;color:#7c3aed;border-bottom:1px solid rgba(124, 58, 237, 0.2);background:rgba(124, 58, 237, 0.1)">Visual Agent</td></tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">ScreenSpot Pro</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">45.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">72.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">62.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">65.6</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">OSWorld-Verified</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">38.2</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">66.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">38.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">63.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">62.2</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">AndroidWorld</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">63.7</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">--</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">66.8</td>
</tr>
<tr><td colspan="7" style="padding:8px 12px;font-weight:600;color:#7c3aed;border-bottom:1px solid rgba(124, 58, 237, 0.2);background:rgba(124, 58, 237, 0.1)">Medical VQA</td></tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">SLAKE</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">76.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">76.4</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">81.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">72.5</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">81.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">79.9</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">PMC-VQA</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">58.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">59.9</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">62.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">56.1</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">63.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">64.2</td>
</tr>
<tr>
<td style="padding:7px 12px;padding-left:20px;border-bottom:1px solid rgba(128, 128, 128, 0.15);">MedXpertQA-MM</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">73.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">63.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">76.0</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">47.6</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">65.3</td>
<td style="padding:7px 12px;text-align:center;border-bottom:1px solid rgba(128, 128, 128, 0.15)">70.0</td>
</tr>
</tbody>
</table>

<p style="margin-top:12px;font-size:11px;opacity:0.7">
* MathVision：our model’s score is evaluated using a fixed prompt, e.g., “Please reason step by step, and put your final answer within \boxed{}.” For other models, we report the higher score between runs with and without the \boxed{} formatting.<br>
* BabyVision: our model’s score is reported with CI (Code Interpreter) enabled; without CI, the result is 43.3.<br>
* V*: our model’s score is reported with CI (Code Interpreter) enabled; without CI, the result is 91.1.<br>
* Empty cells (--) indicate scores not yet available or not applicable.<br>
</p>

</div>


## Quickstart

> [!Important]
> Qwen3.5 models operate in thinking mode by default, generating thinking content signified by `<think>\n...</think>\n\n` before producing the final responses.
> To disable thinking content and obtain direct response, refer to the examples [here](#instruct-or-non-thinking-mode).


For streamlined integration, we recommend using Qwen3.5 via APIs. Below is a guide to use Qwen3.5 via OpenAI-compatible API. 

### Serving Qwen3.5

Qwen3.5 can be served via APIs with popular inference frameworks.
In the following, we show example commands to launch OpenAI-Compatible API servers for Qwen3.5 models.


> [!Important]
> Inference efficiency and throughput vary significantly across frameworks. 
> We recommend using the latest framework versions to ensure optimal performance and compatibility.
> For production workloads or high-throughput scenarios, dedicated serving engines such as SGLang, KTransformers or vLLM are strongly recommended.

> [!Important]
> The model has a default context length of 262,144 tokens.
> If you encounter out-of-memory (OOM) errors, consider reducing the context window. 
> However, because Qwen3.5 leverages extended context for complex tasks, we advise maintaining a context length of at least 128K tokens to preserve thinking capabilities.

#### SGLang

[SGLang](https://github.com/sgl-project/sglang) is a fast serving framework for large language models and vision language models.
SGLang from the main branch of the open-source repository is required for Qwen3.5, which can be installed using the following command in a fresh environment:
```shell
uv pip install 'git+https://github.com/sgl-project/sglang.git#subdirectory=python&egg=sglang[all]'
```
See [its documentation](https://docs.sglang.ai/get_started/install.html) for more details.

The following will create API endpoints at `http://localhost:8000/v1`:

- **Standard Version**: The following command can be used to create an API endpoint with maximum context length 262,144 tokens using tensor parallel on 8 GPUs.
    
    ```shell
    python -m sglang.launch_server --model-path Qwen/Qwen3.5-397B-A17B --port 8000 --tp-size 8 --mem-fraction-static 0.8 --context-length 262144 --reasoning-parser qwen3
    ```

- **Tool Use**: To support tool use, you can use the following command.
    
    ```shell
    python -m sglang.launch_server --model-path Qwen/Qwen3.5-397B-A17B --port 8000 --tp-size 8 --mem-fraction-static 0.8 --context-length 262144 --reasoning-parser qwen3 --tool-call-parser qwen3_coder
    ```

- **Multi-Token Prediction (MTP)**: The following command is recommended for MTP:
    
    ```shell
    python -m sglang.launch_server --model-path Qwen/Qwen3.5-397B-A17B --port 8000 --tp-size 8 --mem-fraction-static 0.8 --context-length 262144 --reasoning-parser qwen3 --speculative-algo NEXTN --speculative-num-steps 3 --speculative-eagle-topk 1 --speculative-num-draft-tokens 4
    ```

#### vLLM

[vLLM](https://github.com/vllm-project/vllm) is a high-throughput and memory-efficient inference and serving engine for LLMs.
vLLM from the main branch of the open-source repository is required for Qwen3.5, which can be installed using the following command in a fresh environment:
```shell
uv pip install vllm --torch-backend=auto --extra-index-url https://wheels.vllm.ai/nightly
```
See [its documentation](https://docs.vllm.ai/en/stable/getting_started/installation/index.html) for more details. 

For detailed Qwen3.5 usage guide, see the [vLLM Qwen3.5 recipe](https://docs.vllm.ai/projects/recipes/en/latest/Qwen/Qwen3.5.html).

The following will create API endpoints at `http://localhost:8000/v1`:

- **Standard Version**: The following command can be used to create an API endpoint with maximum context length 262,144 tokens using tensor parallel on 8 GPUs.

    ```shell
    vllm serve Qwen/Qwen3.5-397B-A17B --port 8000 --tensor-parallel-size 8 --max-model-len 262144 --reasoning-parser qwen3 
    ```

- **Tool Call**: To support tool use, you can use the following command.
    
    ```shell
    vllm serve Qwen/Qwen3.5-397B-A17B --port 8000 --tensor-parallel-size 8 --max-model-len 262144 --reasoning-parser qwen3 --enable-auto-tool-choice --tool-call-parser qwen3_coder 
    ```

- **Multi-Token Prediction (MTP)**: The following command is recommended for MTP:

    ```shell
    vllm serve Qwen/Qwen3.5-397B-A17B --port 8000 --tensor-parallel-size 8 --max-model-len 262144 --reasoning-parser qwen3 --speculative-config '{"method":"qwen3_next_mtp","num_speculative_tokens":2}'
    ```

- **Text-Only**: The following command skips the vision encoder and multimodal profiling to free up memory for additional KV cache:
    
    ```shell
    vllm serve Qwen/Qwen3.5-397B-A17B --port 8000 --tensor-parallel-size 8 --max-model-len 262144 --reasoning-parser qwen3 --language-model-only
    ```

#### KTransformers
 
[KTransformers](https://github.com/kvcache-ai/ktransformers) is a flexible framework for experiencing cutting-edge LLM inference optimizations with CPU-GPU heterogeneous computing.
For running Qwen3.5 with KTransformers, see the [KTransformers Deployment Guide](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/Qwen3.5.md).
 
#### Hugging Face Transformers

Hugging Face Transformers contains a _lightweight_ server which can be used for quick testing and moderate load deployment.
The latest `transformers` is required for Qwen3.5:
```shell
pip install "transformers[serving] @ git+https://github.com/huggingface/transformers.git@main"
```
See [its documentation](https://huggingface.co/docs/transformers/main/serving) for more details. Please also make sure torchvision and pillow are installed.

Then, run `transformers serve` to launch a server with API endpoints at `http://localhost:8000/v1`; it will place the model on accelerators if available:
```shell
transformers serve --force-model Qwen/Qwen3.5-397B-A17B --port 8000 --continuous-batching
```

### Using Qwen3.5 via the Chat Completions API

The chat completions API is accessible via standard HTTP requests or OpenAI SDKs.
Here, we show examples using the OpenAI Python SDK.

Before starting, make sure it is installed and the API key and the API base URL is configured, e.g.:
```shell
pip install -U openai

# Set the following accordingly
export OPENAI_BASE_URL="http://localhost:8000/v1"
export OPENAI_API_KEY="EMPTY"
```

> [!Tip]
> We recommend using the following set of sampling parameters for generation
> - Thinking mode: `temperature=0.6, top_p=0.95, top_k=20, min_p=0.0, presence_penalty=0.0, repetition_penalty=1.0`
> - Instruct (or non-thinking) mode: `temperature=0.7, top_p=0.8, top_k=20, min_p=0.0, presence_penalty=1.5, repetition_penalty=1.0`
>
> Please note that the support for sampling parameters varies according to inference frameworks.

#### Text-Only Input

```python
from openai import OpenAI
# Configured by environment variables
client = OpenAI()

messages = [
    {"role": "user", "content": "Type \"I love Qwen3.5\" backwards"},
]

chat_response = client.chat.completions.create(
    model="Qwen/Qwen3.5-397B-A17B",
    messages=messages,
    max_tokens=81920,
    temperature=0.6,
    top_p=0.95,
    extra_body={
        "top_k": 20,
    }, 
)
print("Chat response:", chat_response)
```


#### Image Input

```python
from openai import OpenAI
# Configured by environment variables
client = OpenAI()

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://qianwen-res.oss-accelerate.aliyuncs.com/Qwen3.5/demo/CI_Demo/mathv-1327.jpg"
                }
            },
            {
                "type": "text",
                "text": "The centres of the four illustrated circles are in the corners of the square. The two big circles touch each other and also the two little circles. With which factor do you have to multiply the radii of the little circles to obtain the radius of the big circles?\nChoices:\n(A) $\\frac{2}{9}$\n(B) $\\sqrt{5}$\n(C) $0.8 \\cdot \\pi$\n(D) 2.5\n(E) $1+\\sqrt{2}$"
            }
        ]
    }
]

chat_response = client.chat.completions.create(
    model="Qwen/Qwen3.5-397B-A17B",
    messages=messages,
    max_tokens=81920,
    temperature=0.6,
    top_p=0.95,
    extra_body={
        "top_k": 20,
    }, 
)
print("Chat response:", chat_response)
```

#### Video Input

```python
from openai import OpenAI
# Configured by environment variables
client = OpenAI()

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "video_url",
                "video_url": {
                    "url": "https://qianwen-res.oss-accelerate.aliyuncs.com/Qwen3.5/demo/video/N1cdUjctpG8.mp4"
                }
            },
            {
                "type": "text",
                "text": "How many porcelain jars were discovered in the niches located in the primary chamber of the tomb?"
            }
        ]
    }
]

# When vLLM is launched with `--media-io-kwargs '{"video": {"num_frames": -1}}'`,
# video frame sampling can be configured via `extra_body` (e.g., by setting `fps`).
# This feature is currently supported only in vLLM.
#
# By default, `fps=2` and `do_sample_frames=True`.
# With `do_sample_frames=True`, you can customize the `fps` value to set your desired video sampling rate.
chat_response = client.chat.completions.create(
    model="Qwen/Qwen3.5-397B-A17B",
    messages=messages,
    max_tokens=81920,
    temperature=0.6,
    top_p=0.95,
    extra_body={
        "top_k": 20,
        "mm_processor_kwargs": {"fps": 2, "do_sample_frames": True},
    }, 
)

print("Chat response:", chat_response)
```

#### Instruct (or Non-Thinking) Mode

> [!Important]
> Qwen3.5 does not officially support the soft switch of Qwen3, i.e., `/think` and `/nothink`.

Qwen3.5 will think by default before response.
You can obtain direct response from the model without thinking by configuring the API parameters. 
For example,
```python
from openai import OpenAI
# Configured by environment variables
client = OpenAI()

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://qianwen-res.oss-accelerate.aliyuncs.com/Qwen3.5/demo/RealWorld/RealWorld-04.png"
                }
            },
            {
                "type": "text",
                "text": "Where is this?"
            }
        ]
    }
]

chat_response = client.chat.completions.create(
    model="Qwen/Qwen3.5-397B-A17B",
    messages=messages,
    max_tokens=32768,
    temperature=0.7,
    top_p=0.8,
    presence_penalty=1.5,
    extra_body={
        "top_k": 20,
        "chat_template_kwargs": {"enable_thinking": False},
    }, 
)
print("Chat response:", chat_response)
```

> [!Note]
> If you are using APIs from Alibaba Cloud Model Studio, in addition to changing `model`, please use `"enable_thinking": False` instead of `"chat_template_kwargs": {"enable_thinking": False}`.


## Agentic Usage

Qwen3.5 excels in tool calling capabilities.

### Qwen-Agent

We recommend using [Qwen-Agent](https://github.com/QwenLM/Qwen-Agent) to quickly build Agent applications with Qwen3.5. 

To define the available tools, you can use the MCP configuration file, use the integrated tool of Qwen-Agent, or integrate other tools by yourself.
```python
import os
from qwen_agent.agents import Assistant

# Define LLM
# Using Alibaba Cloud Model Studio
llm_cfg = {
    # Use the OpenAI-compatible model service provided by DashScope:
    'model': 'Qwen3.5-397B-A17B',
    'model_type': 'qwenvl_oai',
    'model_server': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    'api_key': os.getenv('DASHSCOPE_API_KEY'),

    'generate_cfg': {
        'use_raw_api': True,
        # When using Dash Scope OAI API, pass the parameter of whether to enable thinking mode in this way
        'extra_body': {
            'enable_thinking': True
        },
    },
}

# Using OpenAI-compatible API endpoint.
# functionality of the deployment frameworks and let Qwen-Agent automate the related operations.
#
# llm_cfg = {
#     # Use your own model service compatible with OpenAI API by vLLM/SGLang:
#     'model': 'Qwen/Qwen3.5-397B-A17B',
#     'model_type': 'qwenvl_oai',
#     'model_server': 'http://localhost:8000/v1',  # api_base
#     'api_key': 'EMPTY',
#
#     'generate_cfg': {
#         'use_raw_api': True,
#         # When using vLLM/SGLang OAI API, pass the parameter of whether to enable thinking mode in this way
#         'extra_body': {
#             'chat_template_kwargs': {'enable_thinking': True}
#         },
#     },
# }

# Define Tools
tools = [
    {'mcpServers': {  # You can specify the MCP configuration file
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/xxxx/Desktop"]
            }
        }
    }
]

# Define Agent
bot = Assistant(llm=llm_cfg, function_list=tools)

# Streaming generation
messages = [{'role': 'user', 'content': 'Help me organize my desktop.'}]
for responses in bot.run(messages=messages):
    pass
print(responses)

# Streaming generation
messages = [{'role': 'user', 'content': 'Develop a dog website and save it on the desktop'}]
for responses in bot.run(messages=messages):
    pass
print(responses)
```

### Qwen Code


[Qwen Code](https://github.com/QwenLM/qwen-code) is an open-source AI agent for the terminal, optimized for Qwen models. It helps you understand large codebases, automate tedious work, and ship faster.

For more information, please refer to [Qwen Code](https://qwenlm.github.io/qwen-code-docs/).

## Processing Ultra-Long Texts

Qwen3.5 natively supports context lengths of up to 262,144 tokens. 
For long-horizon tasks where the total length (including both input and output) exceeds this limit, we recommend using RoPE scaling techniques to handle long texts effectively., e.g., YaRN.

YaRN is currently supported by several inference frameworks, e.g., `transformers`, `vllm`, `ktransformers` and `sglang`. 
In general, there are two approaches to enabling YaRN for supported frameworks:

- Modifying the model configuration file:
  In the `config.json` file, change the `rope_parameters` fields in `text_config` to:
    ```json
    {
        "mrope_interleaved": true,
        "mrope_section": [
            11,
            11,
            10
        ],
        "rope_type": "yarn",
        "rope_theta": 10000000,
        "partial_rotary_factor": 0.25,
        "factor": 4.0,
        "original_max_position_embeddings": 262144,
    }
    ```

- Passing command line arguments:

  For `vllm`, you can use
    ```shell
    VLLM_ALLOW_LONG_MAX_MODEL_LEN=1 vllm serve ... --hf-overrides '{"text_config": {"rope_parameters": {"mrope_interleaved": true, "mrope_section": [11, 11, 10], "rope_type": "yarn", "rope_theta": 10000000, "partial_rotary_factor": 0.25, "factor": 4.0, "original_max_position_embeddings": 262144}}}' --max-model-len 1010000  
    ```

  For `sglang` and `ktransformers`, you can use
    ```shell
    SGLANG_ALLOW_OVERWRITE_LONGER_CONTEXT_LEN=1 python -m sglang.launch_server ... --json-model-override-args '{"text_config": {"rope_parameters": {"mrope_interleaved": true, "mrope_section": [11, 11, 10], "rope_type": "yarn", "rope_theta": 10000000, "partial_rotary_factor": 0.25, "factor": 4.0, "original_max_position_embeddings": 262144}}}' --context-length 1010000
    ```

> [!NOTE]
> All the notable open-source frameworks implement static YaRN, which means the scaling factor remains constant regardless of input length, **potentially impacting performance on shorter texts.**
> We advise modifying the `rope_parameters` configuration only when processing long contexts is required. 
> It is also recommended to modify the `factor` as needed. For example, if the typical context length for your application is 524,288 tokens, it would be better to set `factor` as 2.0. 

## Best Practices

To achieve optimal performance, we recommend the following settings:

1. **Sampling Parameters**:
   - We suggest using `Temperature=0.6`, `TopP=0.95`, `TopK=20`, and `MinP=0` for thinking mode and using `Temperature=0.7`, `TopP=0.8`, `TopK=20`, and `MinP=0` for non-thinking mode.
   - For supported frameworks, you can adjust the `presence_penalty` parameter between 0 and 2 to reduce endless repetitions. However, using a higher value may occasionally result in language mixing and a slight decrease in model performance.

2. **Adequate Output Length**: We recommend using an output length of 32,768 tokens for most queries. For benchmarking on highly complex problems, such as those found in math and programming competitions, we suggest setting the max output length to 81,920 tokens. This provides the model with sufficient space to generate detailed and comprehensive responses, thereby enhancing its overall performance.

3. **Standardize Output Format**: We recommend using prompts to standardize model outputs when benchmarking.
   - **Math Problems**: Include "Please reason step by step, and put your final answer within \boxed{}." in the prompt.
   - **Multiple-Choice Questions**: Add the following JSON structure to the prompt to standardize responses: "Please show your choice in the `answer` field with only the choice letter, e.g., `"answer": "C"`."

4. **No Thinking Content in History**: In multi-turn conversations, the historical model output should only include the final output part and does not need to include the thinking content. It is implemented in the provided chat template in Jinja2. However, for frameworks that do not directly use the Jinja2 chat template, it is up to the developers to ensure that the best practice is followed.

5. **Long Video Understanding**: To optimize inference efficiency for plain text and images, the `size` parameter in the released `video_preprocessor_config.json` is conservatively configured. It is recommended to set the `longest_edge` parameter in the video_preprocessor_config file to 469,762,048 (corresponding to 224k video tokens) to enable higher frame-rate sampling for hour-scale videos and thereby achieve superior performance. For example,
    ```json
    {"longest_edge": 469762048, "shortest_edge": 4096}
    ```

    Alternatively, override the default values via engine startup parameters. For implementation details, refer to: [vLLM](https://github.com/vllm-project/vllm/pull/34330) / [SGLang](https://github.com/sgl-project/sglang/pull/18467).


### Citation

If you find our work helpful, feel free to give us a cite.

```bibtex
@misc{qwen3.5,
    title  = {{Qwen3.5}: Towards Native Multimodal Agents},
    author = {{Qwen Team}},
    month  = {February},
    year   = {2026},
    url    = {https://qwen.ai/blog?id=qwen3.5}
}
```