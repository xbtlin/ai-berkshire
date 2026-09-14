---
license: mit
pipeline_tag: text-generation
library_name: transformers
---

<p align="center">
    <img src="https://mdn.alipayobjects.com/huamei_qa8qxu/afts/img/A*4QxcQrBlTiAAAAAAQXAAAAgAemJ7AQ/original" width="100"/>
</p>
<p align="center">🤗 <a href="https://huggingface.co/inclusionAI">Hugging Face</a>&nbsp;&nbsp; | &nbsp;&nbsp;🤖 <a href="https://modelscope.cn/organization/inclusionAI">ModelScope </a>&nbsp;&nbsp; | &nbsp;&nbsp; <a href="https://arxiv.org/abs/2606.15079">Tech Report </a>&nbsp;&nbsp; | &nbsp;&nbsp; 🐙 <a href="https://github.com/inclusionAI/Ling-V2.5">GitHub</a></p>

# Ling-2.6-1T-base

Ling-2.6-1T-base is the base checkpoint behind the Ling-2.6-1T and Ring-2.6-1T. It is a trillion-parameter Mixture-of-Experts language model retrofitted from Ling-2.0-1T-base with a hybrid linear attention design, continued pre-training, and long-context mid-training.

This release is intended for research, continued pre-training, distillation, and supervised or preference-based fine-tuning. It is not a chat-aligned assistant model. If you want an out-of-the-box instruction or reasoning model, use the corresponding Ling-2.6 or Ring-2.6 post-trained checkpoints instead.

## 1. Model Overview

Ling-2.6-1T-base is designed to preserve the capability of the Ling-2.0 trillion-scale backbone while making long-context training and inference materially more efficient. The core upgrade is a hybrid attention retrofit that combines Lightning Attention with MLA in a 7:1 ratio, together with a smooth migration pipeline from the original GQA-based architecture.

According to the technical report, the model is trained through approximately 9.6T tokens across migration pre-training, continued pre-training, and mid-training, with staged context extension from 4K to 256K. The same base checkpoint is later specialized into:

- Ling-2.6 for instant, token-efficient response
- Ring-2.6 for deeper reasoning and long-horizon agentic workflows

## 2. Key Features

- Hybrid linear attention architecture combining Lightning Attention and MLA in a 7:1 ratio
- Trillion-parameter MoE backbone upgraded from Ling-2.0-1T-base instead of retraining from scratch
- Long-context training pipeline extended to 256K context during mid-training
- Continued pre-training mixture covering agentic data, long-context data, knowledge-rich web data, math, code, and multilingual corpora
- Strong base-model quality across knowledge, math, code, reasoning, and long-context understanding benchmarks

## 3. Model Summary

| Item | Value |
| --- | --- |
| Architecture | Fine-grained MoE with hybrid linear attention |
| Parameter Scale | Totoal ~1T, Activated ~63B |
| Transformer layers | 80 |
| Attention heads | 64 |
| Hidden size | 8192 |
| Routed experts per MoE layer | 256 |
| Shared experts per MoE layer | 1 |
| Active routed experts per token | 8 |
| Dense FFN layers | First 4 transformer blocks |
| Expert intermediate size | 2048 |
| Dense intermediate size | 18432 |
| Vocabulary size | 157,184 |
| Positional encoding | Partial RoPE |
| Attention design | Lightning Attention + MLA, 7:1 ratio |
| Training recipe | Migration pre-training + continued pre-training + mid-training |
| Total training tokens | ~9.6T |
| Context training schedule | 4K -> 32K -> 256K |

## 4. Training Highlights

### Architecture Migration

The model starts from Ling-2.0-1T-base and is converted into the Ling-2.6-1T architecture through a multi-stage migration pipeline that includes:

1. Lightning Attention conversion
2. Linear warmup
3. MLA conversion
4. MLA warmup
5. Full continued pre-training

This retrofit is designed to preserve pre-trained capability while reducing long-context compute cost and KV-cache pressure.

### Data Mixture

The continued pre-training and mid-training stages include:

- Agentic corpus built from tool-use and coding environments
- Long-context corpus covering mathematics, web parsing, summarization, retrieval, and multi-hop reasoning
- General web knowledge data with targeted STEM and factual augmentation
- Math and code corpora
- Multilingual data spanning 21 languages


## 5. Base Model Evaluation

The following numbers are selected from the technical report and reflect base-model evaluation rather than chat-aligned or instruction-tuned performance.

| Benchmark | Ling-2.0-1T-base | Ling-2.6-1T-base |
| --- | ---: | ---: |
| MMLU | 86.03 | 86.82 |
| MMLU-Pro | 67.91 | 67.79 |
| GPQA | 41.92 | 45.45 |
| SimpleQA | 20.87 | 38.26 |
| C-SimpleQA | 64.53 | 76.83 |
| MMMLU | 68.68 | 71.53 |
| GSM8K | 89.31 | 93.93 |
| OmniMath | 33.60 | 38.70 |
| HumanEval-Plus | 83.54 | 85.98 |
| LiveCodeBench | 40.09 | 44.27 |
| BIRD-SQL | 42.70 | 44.59 |
| BBH | 86.88 | 89.73 |
| AutoLogic | 65.76 | 67.43 |
| LEval | 72.30 | 76.21 |
| LongBenchv2 | 30.02 | 43.54 |

In the technical report, Ling-2.6-1T-base shows broad gains over Ling-2.0-1T-base, especially on factual knowledge, multilingual knowledge coverage, long-context understanding, and reasoning-oriented evaluations, while preserving or improving strong math and code capability. One notable exception in this selected subset is MMLU-Pro, where Ling-2.0-1T-base remains slightly higher.

## 6. Intended Use

Recommended use cases:

- Continued pre-training
- Supervised fine-tuning for domain adaptation
- Preference optimization and RL post-training
- Distillation research
- Long-context and MoE systems research

Not recommended as-is for:

- Direct end-user chat deployment
- Safety-critical applications without additional alignment and evaluation
- Single-GPU local inference


## 7. Limitations

- This is a base model and is not instruction-aligned.
- Outputs may be inaccurate, biased, incomplete, or unsafe without additional post-training.
- Long-context quality depends on the serving stack, positional scaling configuration, and prompt format used at inference time.
- The training mixture includes web-scale and synthetic data, so the model may reproduce factual errors or undesirable artifacts.
- Benchmark results in the technical report are collected under controlled internal evaluation settings and should not be treated as a guarantee of downstream production behavior.

## 8. Relationship to Other Releases

- [Ling-2.6-1T](https://huggingface.co/inclusionAI/Ling-2.6-1T): instruction and instant-response optimized model derived from this base
- [Ring-2.6-1T](https://huggingface.co/inclusionAI/Ring-2.6-1T): reasoning- and agent-optimized model derived from the same 2.6 generation

If your goal is interactive assistant use rather than research on base checkpoints, these post-trained models are usually the better starting point.

## 9. Usage

This is a base checkpoint. One can load it for simple generation or further post-training. Notably, real deployment of a trillion-parameter model typically requires multi-node distributed infrastructure. The example below illustrates the loading pattern only.

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "inclusionAI/Ling-2.6-1T-base"

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
		model_name,
		trust_remote_code=True,
		device_map="auto",
)

prompt = "Explain the difference between full attention and linear attention."
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

outputs = model.generate(
		**inputs,
		max_new_tokens=256,
		do_sample=False,
)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

For production inference, prefer distributed serving stacks such as SGLang or other engines that support the released architecture and model size. You can refer to our [instruction version](https://huggingface.co/inclusionAI/Ling-2.6-1T) for SGLang deployment.


## 10. License

This checkpoint and code repository is licensed under the MIT License.