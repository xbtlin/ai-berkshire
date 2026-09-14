---
language:
- en
- ko
library_name: transformers
license: other
license_name: upstage-solar-license
pipeline_tag: text-generation
tags:
- upstage
- solar
- moe
- 100b
- llm
arxiv: 2601.07022
---

<p align="center">
  <img src="./Solar-Open-100B.png" alt="Solar Open Model" width="100%">
</p>

# **Solar Open**

**Solar Open** is Upstage's flagship **102B-parameter** large language model, trained **entirely from scratch** and released under the **Upstage Solar License** (see [LICENSE](#license) for details). As a **Mixture-of-Experts (MoE)** architecture, it delivers enterprise-grade performance in reasoning, instruction-following, and agentic capabilities—all while prioritizing transparency and customization for the open-source community.

[**Technical Report**](https://huggingface.co/papers/2601.07022) | [**Project Page**](https://upstage.ai)

## Highlights

* **MoE Architecture (102B / 12B):** Built on a Mixture-of-Experts architecture with **102B total / 12B active parameters**. This design delivers the knowledge depth of a massive model with the inference speed and cost-efficiency of a much smaller model.
* **Massive Training Scale:** Pre-trained on **19.7 trillion tokens**, ensuring broad knowledge coverage and robust reasoning capabilities across various domains.
* **Quantized Version Available:** An official INT4 quantized model is provided by NotaAI and available at [`nota-ai/Solar-Open-100B-NotaMoEQuant-Int4`](https://huggingface.co/nota-ai/Solar-Open-100B-NotaMoEQuant-Int4).

## Model Overview

* **Model Name:** Solar Open 100B
* **Hugging Face ID:** `Upstage/Solar-Open-100B`
* **Architecture:** Mixture-of-Experts (MoE)
    * **Total Parameters:** 102.6B
    * **Active Parameters:** 12B (per token)
    * **Experts:** 129 Experts (top 8 among 128 Routed + 1 Shared)
* **Pre-training Tokens:** 19.7 Trillion
* **Context Length:** 128k
* **Training Hardware:** NVIDIA B200 GPUs
* **License:** **Upstage Solar License** (See [LICENSE](#license))
* **Hardware Requirements:**
    * **Minimum:** 4x NVIDIA A100 (80GB)

For more details, please refer to the [Solar Open Technical Report](https://huggingface.co/papers/2601.07022).

## License
This repository contains both model weights and code,
which are licensed under different terms:

1. MODEL WEIGHTS (*.safetensors)
   Licensed under **Upstage Solar License**
   See: https://huggingface.co/upstage/Solar-Open-100B/blob/main/LICENSE

2. CODE (*.py, *.json, *.jinja files)
   Licensed under **Apache License 2.0**
   See: https://www.apache.org/licenses/LICENSE-2.0

## Performance

### Korean Benchmarks

| Category | Benchmarks | Solar Open (102B) | gpt-oss-120b (117B, high) | gpt-oss-120b (117B, medium) | GLM-4.5-Air (110B) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **General** | KMMLU | 73.0 | 72.7 | 70.3 | 70.2 |
| | KMMLU-Pro | 64.0 | 62.6 | 60.5 | 60.7 |
| | CLIcK | 78.9 | 77.2 | 72.9 | 48.3 |
| | HAE-RAE v1.1 | 73.3 | 70.8 | 69.6 | 42.6 |
| | KoBALT | 44.3 | 52.6 | 45.0 | 40.3 |
| **Finance** | KBankMMLU (in-house) | 65.5 | 62.5 | 61.5 | 64.7 |
| **Law** | KBL | 65.5 | 62.8 | 60.1 | 60.6 |
| **Medical** | KorMedMCQA | 84.4 | 75.8 | 76.3 | 80.5 |
| **Math** | Ko-AIME 2024 (in-house) | 80.3 | 90.0 | 76.7 | 80.0 |
| | Ko-AIME 2025 (in-house) | 80.0 | 90.0 | 70.0 | 83.3 |
| | HRM8K | 87.6 | 89.5 | 84.8 | 86.0 |
| **IF** | Ko-IFEval | 87.5 | 93.2 | 86.7 | 79.5 |
| **Preference** | Ko Arena Hard v2 (in-house) | 79.9 | 79.5 | 73.8 | 60.4 |


### English Benchmarks

| Category | Benchmarks | Solar Open (102B) | gpt-oss-120b (117B, high) | gpt-oss-120b (117B, medium) | GLM-4.5-Air (110B) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **General** | MMLU | 88.2 | 88.6 | 87.9 | 83.3 |
| | MMLU-Pro | 80.4 | 80.4 | 78.6 | 81.4 |
| | GPQA-Diamond | 68.1 | 78.0 | 69.4 | 75.8 |
| | HLE (text only) | 10.5 | 18.4 | 7.23 | 10.8 |
| **Math** | AIME 2024 | 91.7 | 94.3 | 77.7 | 88.7 |
| | AIME 2025 | 84.3 | 91.7 | 75.0 | 82.7 |
| | HMMT 2025 (Feb) | 73.3 | 80.0 | 63.3 | 66.7 |
| | HMMT 2025 (Nov) | 80.0 | 73.3 | 66.7 | 70.0 |
| **Code** | LiveCodeBench (v1–v6 cumul) | 74.2 | 89.9 | 82.8 | 71.9 |
| **IF** | IFBench | 53.7 | 70.8 | 61.2 | 37.8 |
| | IFEval | 88.0 | 91.4 | 86.5 | 86.5 |
| **Preference** | Arena Hard v2 | 74.8 | 79.6 | 72.7 | 62.5 |
| | Writing Bench | 7.51 | 6.61 | 6.55 | 7.40 |
| **Agent** | Tau² Airline | 52.4 | 56.0 | 52.8 | 60.8 |
| | Tau² Telecom | 55.6 | 57.7 | 47.4 | 28.1 |
| | Tau² Retail | 59.3 | 76.5 | 68.4 | 71.9 |
| **Long** | AA-LCR | 35.0 | 48.3 | 45.0 | 37.3 |

## Inference Quickstart

We recommend using the following generation parameters:

```
temperature=0.8
top_p=0.95
top_k=50
```

### Transformers

Install the required dependencies:

```bash
pip install -U "transformers>=5.0" kernels torch accelerate
```

Run inference with the following code:

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "upstage/Solar-Open-100B"

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

model = AutoModelForCausalLM.from_pretrained(
    pretrained_model_name_or_path=MODEL_ID,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

# Prepare input
messages = [{"role": "user", "content": "who are you?"}]
inputs = tokenizer.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_dict=True,
    return_tensors="pt",
)
inputs = inputs.to(model.device)

# Generate response
generated_ids = model.generate(
    **inputs,
    max_new_tokens=4096,
    temperature=0.8,
    top_p=0.95,
    top_k=50,
    do_sample=True,
)
generated_text = tokenizer.decode(generated_ids[0][inputs.input_ids.shape[1] :])
print(generated_text)
```

### vLLM

#### Option 1: Using Docker (Highly Recommended)
Docker is the **recommended deployment method** for running `Solar-Open-100B`.

```bash
# For 8 GPUs
docker run --gpus all \
    --ipc=host \
    -p 8000:8000 \
    upstage/vllm-solar-open:latest \
    upstage/Solar-Open-100B \
    --trust-remote-code \
    --enable-auto-tool-choice \
    --tool-call-parser solar_open \
    --reasoning-parser solar_open \
    --logits-processors vllm.model_executor.models.parallel_tool_call_logits_processor:ParallelToolCallLogitsProcessor \
    --logits-processors vllm.model_executor.models.solar_open_logits_processor:SolarOpenTemplateLogitsProcessor \
    --tensor-parallel-size 8
```

#### Option 2: Installing from Source
For development, debugging, custom modifications or offline inference, Solar Open can also be run
using a source installation of vLLM. We recommend using **[uv](https://docs.astral.sh/uv/)** for environment
management and dependency resolution.

Create and activate a Python virtual environment
```bash
uv venv --python 3.12 --seed
source .venv/bin/activate
```

Install Solar Open's optimized vLLM
```bash
VLLM_PRECOMPILED_WHEEL_LOCATION="https://github.com/vllm-project/vllm/releases/download/v0.12.0/vllm-0.12.0-cp38-abi3-manylinux_2_31_x86_64.whl" \
VLLM_USE_PRECOMPILED=1 \
uv pip install git+https://github.com/UpstageAI/vllm.git@v0.12.0-solar-open
```

Start the vLLM server (For 8 GPUs)
```bash
vllm serve upstage/Solar-Open-100B \
    --trust-remote-code \
    --enable-auto-tool-choice \
    --tool-call-parser solar_open \
    --reasoning-parser solar_open \
    --logits-processors vllm.model_executor.models.parallel_tool_call_logits_processor:ParallelToolCallLogitsProcessor \
    --logits-processors vllm.model_executor.models.solar_open_logits_processor:SolarOpenTemplateLogitsProcessor \
    --tensor-parallel-size 8
```

## Citation

If you use Solar Open in your research, please cite:

```bibtex
@article{park2025solar,
  title={Solar Open Technical Report},
  author={Sungrae Park and Sanghoon Kim and Jungho Cho and Gyoungjin Gim and Dawoon Jung and Mikyoung Cha and Eunhae Choo and Taekgyu Hong and Minbyul Jeong and SeHwan Joo and Minsoo Khang and Eunwon Kim and Minjeong Kim and Sujeong Kim and Yunsu Kim and Hyeonju Lee and Seunghyun Lee and Sukyung Lee and Siyoung Park and Gyungin Shin and Inseo Song and Wonho Song and Seonghoon Yang and Seungyoun Yi and Sanghoon Yoon and Jeonghyun Ko and Seyoung Song and Keunwoo Choi and Hwalsuk Lee and Sunghun Kim and Du-Seong Chang and Kyunghyun Cho and Junsuk Choe and Hwaran Lee and Jae-Gil Lee and KyungTae Lim and Alice Oh},
  journal={arXiv preprint arXiv:2601.07022},
  year={2025},
  url={https://huggingface.co/papers/2601.07022}
}
```