---
license: apache-2.0
library_name: transformers
pipeline_tag: text-generation
tags:
- hunyuan
- hy3
- moe
- text-generation
---
<p align="left">
    <a href="https://huggingface.co/tencent/Hy3/blob/main/README_CN.md">中文</a>&nbsp;｜&nbsp;English
</p>
<br>

<p align="center">
 <img src="assets/logo-en.png" width="400"/> <br>
</p>

<div align="center" style="line-height: 1;">


[![License](https://img.shields.io/badge/License-Apache%202.0-blue)](#license)
&nbsp;&nbsp;
[![HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Tencent%20Hy-ffc107?color=ffc107&logoColor=white)](https://huggingface.co/tencent/Hy3)
&nbsp;&nbsp;
[![ModelScope](https://img.shields.io/badge/ModelScope-Tencent%20Hy-624aff)](https://modelscope.cn/models/Tencent-Hunyuan/Hy3)
&nbsp;&nbsp;
[![cnb.cool](https://img.shields.io/badge/cnb.cool-Tencent%20Hy-blue?logoColor=white)](https://cnb.cool/ai-models/tencent/Hy3)
&nbsp;&nbsp;
[![GitCode](https://img.shields.io/badge/GitCode-Tencent%20Hy-red?logoColor=white)](https://ai.gitcode.com/tencent_hunyuan/Hy3)

</div>

<p align="center">
    🖥️&nbsp;<a href="https://aistudio.tencent.com/"><b>Official Website</b></a>&nbsp;&nbsp;|&nbsp;&nbsp;
    💬&nbsp;<a href="https://github.com/Tencent-Hunyuan/Hy3"><b>GitHub</b></a></p>

---

## Table of Contents

- [Model Introduction](#model-introduction)
- [Stronger Agent Capabilities](#stronger-agent-capabilities)
- [More Reliable Product Experiences](#more-reliable-product-experiences)
- [Benchmark Appendix](#benchmark-appendix)
- [News](#news)
- [Model Links](#model-links)
- [Quickstart](#quickstart)
- [Deployment](#deployment)
  - [vLLM](#vllm)
  - [SGLang](#sglang)
- [Finetuning](#finetuning)
- [RL Post-training](#rl-post-training)
- [Quantization](#quantization)
- [License](#license)
- [Contact Us](#contact-us)

---

## Model Introduction

**Hy3** is a 295B-parameter Mixture-of-Experts (MoE) model with 21B active parameters and 3.8B MTP layer parameters, developed by the Tencent Hy Team. Following the Hy3 Preview launch in late April, we gathered feedback from 50+ products and scaled up post-training with higher quality data. Today, we introduce Hy3, which outperforms similar-size models and rivals flagship open-source models with 2-5x parameters. It also shows significant gains in utility across various products and productivity tasks.


| Property | Value |
|:---|:---|
| Architecture | Mixture-of-Experts (MoE) |
| Total Parameters | 295B |
| Activated Parameters | 21B |
| MTP Layer Parameters | 3.8B |
| Number of Layers (excluding MTP layer) | 80 |
| Number of MTP Layers | 1 |
| Attention Heads | 64 (GQA, 8 KV heads, head dim 128) |
| Hidden Size | 4096 |
| Intermediate Size | 13312 |
| Context Length | 256K |
| Vocabulary Size | 120832 |
| Number of Experts | 192 experts, top-8 activated |
| Supported Precisions | BF16 |

## Stronger Agent Capabilities

Building on Hy3 Preview, we further improved the quality and diversity of post-training data while scaling up RL training. Hy3 shows solid gains across reasoning, agentic, and long-context tasks, competitive with much larger flagship models.

<p align="center">
  <img src="assets/benchmark.png" width="100%"/>
</p>

In productivity scenarios such as coding, office work, financial modeling, frontend design, and game development, Hy3 has made remarkable progress and can now serve as a reliable, cost-effective model option.

We don't think public benchmark scores tell the full story. So we ran a blind evaluation with 270 experts using tasks from their work, and Hy3 scored 2.67/4, outperforming GLM-5.1 at 2.51/4. The advantage was most substantial in frontend development, data & storage, and CI/CD tasks.

## More Reliable Product Experiences

Model usefulness is not fully captured by benchmarks. Based on extensive product feedback, we identified and fixed the following issues, receiving consistently positive feedback from product teams.

**Stability of tool calls and output formats**: We fixed multiple baseline reliability issues, bringing the model to production-grade standards across tool configurations and output constraints. Tool-call error recovery and overall efficiency improved. Hy3 also generalizes across different agent scaffoldings. On SWE-Bench Verified, accuracy variance across scaffoldings like CodeBuddy, Cline, and KiloCode remains within 4%.

**Knowledge and anti-hallucination**: Guided by the ideal of "answer when grounded, state when evidence is missing, do not conflate sources or fabricate data," we implemented fine-grained data cleaning and training constraints. In internal evaluations based on real-world scenarios, Hy3's hallucination rate dropped from 12.5% to 5.4%, and commonsense error rates fell from 25.4% to 12.7%. These improvements materially reduce fact conflation, fabrication, and logical contradiction.

**Complex context retention and multi-turn intent tracking**: Through joint optimization of SFT and RL, Hy3 improved on operational pain points like coreference resolution, ellipsis recovery, and multi-turn constraint inheritance. On internal comprehensive multi-turn tests, the issue rate dropped from 17.4% to 7.9%. Hy3 also improved markedly on long-dialogue evals like MRCR. Its outputs are more concise while ensuring complex intents do not decay or drift over long-horizon interactions.

## Benchmark Appendix

<p align="center">
  <img src="assets/benchmark-appendix.png" width="100%"/>
</p>

## News


* 🔥 We open-source **Hy3** and **Hy3-FP8** model weights on [Hugging Face](https://huggingface.co/tencent/Hy3), [ModelScope](https://modelscope.cn/models/Tencent-Hunyuan/Hy3), [GitCode](https://ai.gitcode.com/tencent_hunyuan/Hy3), and [CNB](https://cnb.cool/ai-models/tencent/Hy3).

## Model Links


| Model Name | Description | Hugging Face | ModelScope | GitCode | CNB |
|:---|:---|:---:|:---:|:---:|:---:|
| Hy3 | Instruct model | 🤗 [Model](https://huggingface.co/tencent/Hy3) | [Model](https://modelscope.cn/models/Tencent-Hunyuan/Hy3) | [Model](https://ai.gitcode.com/tencent_hunyuan/Hy3) | [Model](https://cnb.cool/ai-models/tencent/Hy3) |
| Hy3-FP8 | FP8 quantized instruct model | 🤗 [Model](https://huggingface.co/tencent/Hy3-FP8) | [Model](https://modelscope.cn/models/Tencent-Hunyuan/Hy3-FP8) | [Model](https://ai.gitcode.com/tencent_hunyuan/Hy3-FP8) | [Model](https://cnb.cool/ai-models/tencent/Hy3-FP8) |

## Quickstart

Deploy Hy3 with [vLLM](#vllm) or [SGLang](#sglang) first, then call the OpenAI-compatible API:

```python
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="EMPTY")

response = client.chat.completions.create(
    model="hy3",
    messages=[
        {"role": "user", "content": "Hello! Can you briefly introduce yourself?"},
    ],
    temperature=0.9,
    top_p=1.0,
    # reasoning_effort: "no_think" (default, direct response), "low", "high" (deep chain-of-thought)
    extra_body={"chat_template_kwargs": {"reasoning_effort": "no_think"}},
)
print(response.choices[0].message.content)
```

> **Recommended parameters**: `temperature=0.9`, `top_p=1.0`.
>
> **Reasoning mode**: Set `reasoning_effort` to `"high"` for complex tasks (math, coding, reasoning) or `"no_think"` for direct responses.

See the [Deployment](#deployment) section below for how to start the API server.

## Deployment

Hy3 has 295B parameters in total. To serve it on 8 GPUs, we recommend using H20-3e or other GPUs with larger memory capacity.

For production serving, we recommend using vLLM or SGLang, both of which provide dedicated recipes for Hy3:

- [vLLM](https://github.com/vllm-project/vllm) - see [vLLM recipes](https://recipes.vllm.ai/tencent/Hy3)

- [SGLang](https://docs.sglang.io/) - see [SGLang cookbook](https://lmsysorg.mintlify.app/cookbook/autoregressive/Tencent/Hy3)

### vLLM

Build vLLM from source:
```bash
uv venv --python 3.12 --seed --managed-python
source .venv/bin/activate
git clone https://github.com/vllm-project/vllm.git
cd vllm
uv pip install --editable . --torch-backend=auto
```

Start the vLLM server with MTP enabled:

```bash
# Switch to trtllm backend to work-around mnnvl workspace size issue.
export VLLM_FLASHINFER_ALLREDUCE_BACKEND=trtllm
vllm serve tencent/Hy3 \
  --tensor-parallel-size 8 \
  --speculative-config.method mtp \
  --speculative-config.num_speculative_tokens 2 \
  --tool-call-parser hy_v3 \
  --reasoning-parser hy_v3 \
  --enable-auto-tool-choice \
  --port 8000 \
  --served-model-name hy3
```

### SGLang

Build SGLang from source:
```bash
git clone https://github.com/sgl-project/sglang
cd sglang
pip3 install pip --upgrade
pip3 install "transformers>=5.6.0"
pip3 install -e "python"
```

Launch SGLang server with MTP enabled:

```bash
python3 -m sglang.launch_server \
  --model tencent/Hy3 \
  --tp-size 8 \
  --tool-call-parser hunyuan \
  --reasoning-parser hunyuan \
  --speculative-num-steps 2 \
  --speculative-eagle-topk 1 \
  --speculative-num-draft-tokens 3 \
  --speculative-algorithm EAGLE \
  --port 8000 \
  --served-model-name hy3
```

## Finetuning

Hy3 provides a complete model finetuning pipeline. For detailed documentation, please refer to: [Finetuning Guide](https://huggingface.co/tencent/Hy3/blob/main/finetune/README.md)

## RL Post-training

Hy3 supports GRPO reinforcement learning training with [verl](https://github.com/volcengine/verl), training on Megatron-LM (model conversion via NVIDIA Megatron-Bridge) with vLLM rollout. For detailed documentation, please refer to: [RL Training Guide](https://huggingface.co/tencent/Hy3/blob/main/rl/README.md)

## Quantization

We provide [AngelSlim](https://github.com/tencent/AngelSlim), a more accessible, comprehensive, and efficient toolkit for large model compression. AngelSlim supports a comprehensive suite of compression tools for large-scale multimodal models, including common quantization algorithms, low-bit quantization, and speculative sampling.

## License


Hy3 is released under the **Apache License 2.0**. See [LICENSE](https://huggingface.co/tencent/Hy3/blob/main/LICENSE) for details.

## Contact Us

If you would like to leave a message for our R&D and product teams, welcome to contact us. You can also reach us via email:

📧 **hunyuan_opensource@tencent.com**

---

<p align="center">
  <i>Hy3 is developed by the Tencent Hy Team.</i>
</p>
