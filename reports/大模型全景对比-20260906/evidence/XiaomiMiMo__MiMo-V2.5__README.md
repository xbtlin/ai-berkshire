---
license: mit
language:
- en
- zh
tags:
- multimodal
- vision-language
- audio
- agent
- video-understanding
- long-context
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
  <a href="https://mimo.xiaomi.com/mimo-v2-5" target="_blank">📰 Blog </a>
  &nbsp;|
  <a href="https://platform.xiaomimimo.com" target="_blank">🎨 Xiaomi MiMo API Platform </a>
  &nbsp;|
  <a href="https://aistudio.xiaomimimo.com" target="_blank">🗨️ Xiaomi MiMo Studio </a>
  &nbsp;|
</div>

<br/>

<div align="center" style="line-height: 1.2;">
  <strong>Community</strong><br/>
  <a href="https://huggingface.co/XiaomiMiMo/MiMo-V2.5/blob/main/assets/wechat.jpg" target="_blank">WeChat Group</a>
  &nbsp;|&nbsp;
  <a href="https://discord.gg/kKC2kNnQEX" target="_blank">Discord</a>
  &nbsp;|&nbsp;
  <a href="https://t.me/+3T-I0pekOVIyNDBl" target="_blank">Telegram</a>
  &nbsp;|&nbsp;
  <a href="https://www.reddit.com/r/XiaomiMiMo_Official/" target="_blank">Reddit</a>
</div>

<br/>

<div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 12px 16px;">
  <b>⚠️ Important: Config Update Notice</b><br/><br/>
  The <code>config.json</code> and <code>tokenizer_config.json</code> files in this repository have been updated since the initial release. If you downloaded MiMo-V2.5 before this <a href="https://huggingface.co/XiaomiMiMo/MiMo-V2.5/commit/4da2748fc0a0123d817280b1b0cd3682a487a161">commit (4da2748)</a>, please re-pull or manually update these two files to ensure correct model behavior. Using the outdated config may lead to degraded model performance. We apologize for any inconvenience.<br/><br/>
  <b>Quick fix:</b>
<pre><code>hf download XiaomiMiMo/MiMo-V2.5 config.json tokenizer_config.json --local-dir ./MiMo-V2.5</code></pre>
</div>

<br/>

# MiMo-V2.5

## 1. Introduction 

MiMo-V2.5 is a native omnimodal model with strong agentic capabilities, supporting text, image, video, and audio understanding within a unified architecture. Built upon the MiMo-V2-Flash backbone and extended with dedicated vision and audio encoders, it delivers robust performance across multimodal perception, long-context reasoning, and agentic workflows. Key features include:

- **Hybrid Attention Architecture**: Inherits the hybrid design from MiMo-V2-Flash, interleaving Sliding Window Attention (SWA) and Global Attention (GA) with a 5:1 ratio and 128 sliding window. This reduces KV-cache storage by nearly 6× while maintaining long-context performance via learnable attention sink bias.

- **Native Omnimodal Encoders**: Equipped with a 729M-param Vision Transformer (ViT) featuring hybrid window attention and a dedicated audio encoder initialized from the weights of MiMo-Audio, enabling high-quality image, video, and audio understanding.

- **Multi-Token Prediction (MTP)**: Three lightweight MTP modules with dense FFNs accelerate inference via speculative decoding and improve RL training efficiency.

- **Efficient Pre-Training**: Trained on a total of ~48T tokens using FP8 mixed precision. The context window supports up to 1M tokens.

- **Agentic Capabilities**: Post-training incorporates SFT, large-scale agentic RL, and Multi-Teacher On-Policy Distillation (MOPD), achieving strong performance on agentic tasks and multimodal understanding benchmarks.

<div align="center">
  <img src="assets/architecture.svg" width="80%" alt="MiMo-V2.5 Architecture" />
</div>

## Model Summary

- **Architecture**: Sparse MoE (Mixture of Experts), 310B total / 15B activated parameters
- **Context Length**: Up to 1M tokens
- **Modalities**: Text, Image, Video, Audio
- **Vision Encoder**: 729M-param ViT (28 layers: 24 SWA + 4 Full)
- **Audio Encoder**: 261M-param Audio Transformer (24 layers: 12 SWA + 12 Full)
- **Multi-Token Prediction (MTP)**: 329M parameters, 3 layers

## 2. Downloads

| Model             | Context Length |                               Download                                |
| :---------------- | :------------: | :-------------------------------------------------------------------: |
| **MiMo-V2.5-Base** |     256K       | [🤗 HuggingFace](https://huggingface.co/XiaomiMiMo/MiMo-V2.5-Base) <br> [🤖 ModelScope](https://modelscope.cn/models/XiaomiMiMo/MiMo-V2.5-Base) |
| **MiMo-V2.5**     |      1M        | [🤗 HuggingFace](https://huggingface.co/XiaomiMiMo/MiMo-V2.5) <br> [🤖 ModelScope](https://modelscope.cn/models/XiaomiMiMo/MiMo-V2.5) |

## 3. Evaluation Results

### Multimodal Benchmarks

<div align="center">
  <img src="assets/mimo-v2.5-multimodal-bench.png" width="80%" alt="MiMo-V2.5 Multimodal Benchmark Results" />
</div>

### Coding & Agent Benchmarks

<div align="center">
  <img src="assets/mimo-v2.5-coding-bench.png" width="80%" alt="MiMo-V2.5 Coding and Agentic Benchmark Results" />
</div>

### Long Context Benchmarks 


<div align="center">
  <img src="assets/mimo-v2.5-graphwalks.jpeg" width="80%" alt="MiMo-V2.5 Graphwalks" />
</div>

## 4. Model Architecture

### LLM Backbone

MiMo-V2.5's core language backbone inherits from the [MiMo-V2-Flash](https://github.com/XiaomiMiMo/MiMo-V2-Flash) architecture, a sparse MoE model with hybrid sliding window attention.

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

### Vision Encoder

We train a dedicated MiMo ViT that adopts sliding-window attention to enable efficient visual encoding.

| Configuration | Value |
| :--- | :--- |
| Total Layers | 28 |
| SWA Layers | 24 |
| Full Attention Layers | 4 |
| Window-Attention Pattern | [-1] + [0,0,0,0,1,1,1,1,-1] × 3 |
| Attention Heads (Q / KV) | 32 / 8 |
| Head Dimensions (QK / V) | 64 / 64 |
| Sliding Window Size (L / R) | 64 / 64 |

Window pattern notation: `-1` = full attention, `0` = 1-D row window, `1` = 1-D column window.

### Audio Encoder

Our audio encoder is initialized from the weights of [MiMo-Audio-Tokenizer](https://huggingface.co/XiaomiMiMo/MiMo-Audio-Tokenizer) and further finetuned to support high-quality audio understanding.

| Configuration | Value |
| :--- | :--- |
| Total Layers | 24 |
| SWA Layers | 12 |
| Full Attention Layers | 12 |
| Sliding Window Size | 128 |
| Attention Heads (Q / KV) | 16 / 16 |
| Head Dimensions (QK / V) | 64 / 64 |

## 5. Training Process

MiMo-V2.5 is trained on a total of ~48T tokens.

1. **Text Pre-training**: We collect diverse text data for pre-training the LLM backbone.
2. **Projector Warmup**: Short-duration warmup of multimodal projectors (audio and visual MLP projectors).
3. **Multimodal Pre-training**: High-quality multimodal data collected for large-scale pretraining.
4. **SFT & Agentic Post Training**: Supervised fine-tuning with diverse agentic data. During this stage, the context window is progressively extended from 32K → 256K → 1M.
5. **RL & MOPD Training**: Reinforcement learning for improving perception, reasoning, and agentic capabilities.

## 6. Deployment

Since inference engines are continuously being updated and optimized, this guide only provides deployment examples for reference. For the best performance, we strongly recommend following our referenced approach to get the latest best practices and optimal performance.

### SGLang Deployment

For the best performance, we strongly recommend deploying using this approach, which is officially supported by the SGLang community. Please refer to [SGLang MiMo-V2.5 Cookbook](https://docs.sglang.io/cookbook/autoregressive/Xiaomi/MiMo-V2.5) for the latest deployment guide.

The following is an example of running the model with SGLang, referenced from [sgl-project/sglang#23811](https://github.com/sgl-project/sglang/pull/23811):

```bash
python3 -m sglang.launch_server \
    --model-path XiaomiMiMo/MiMo-V2.5 \
    --served-model-name mimo-v2.5 \
    --log-level-http warning \
    --enable-cache-report \
    --pp-size 1 \
    --dp-size 2 \
    --tp-size 8 \
    --enable-dp-attention \
    --moe-a2a-backend deepep \
    --deepep-mode auto \
    --decode-log-interval 1 \
    --page-size 1 \
    --host 0.0.0.0 \
    --port 9001 \
    --trust-remote-code \
    --watchdog-timeout 1000000 \
    --mem-fraction-static 0.65 \
    --chunked-prefill-size 16384 \
    --reasoning-parser qwen3 \
    --tool-call-parser mimo \
    --context-length 262144 \
    --collect-tokens-histogram \
    --enable-metrics \
    --load-balance-method round_robin \
    --allow-auto-truncate \
    --enable-metrics-for-all-schedulers \
    --quantization fp8 \
    --skip-server-warmup \
    --moe-dense-tp-size 1 \
    --enable-dp-lm-head \
    --disable-tokenizer-batch-decode \
    --mm-enable-dp-encoder \
    --attention-backend fa3 \
    --mm-attention-backend fa3
```

### vLLM Deployment

For the best performance, we strongly recommend deploying using this approach, which is officially supported by the vLLM community. Please refer to [vLLM MiMo-V2-Flash Cookbook](https://recipes.vllm.ai/XiaomiMiMo/MiMo-V2-Flash) for the latest deployment guide.

For local deployment, we recommend setting the sampling parameters to `temperature=1.0`, `top_p=0.95`.

## Citation

```bibtex
@misc{mimov25,
  title={MiMo-V2.5},
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