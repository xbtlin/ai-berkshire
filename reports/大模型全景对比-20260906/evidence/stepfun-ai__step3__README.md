---
license: apache-2.0
library_name: transformers
pipeline_tag: image-text-to-text
---
<div align="center">
  <picture>
      <img src="https://github.com/stepfun-ai/Step3/blob/main/figures/stepfun-logo.png?raw=true" width="30%" alt="StepFun: Cost-Effective Multimodal Intelligence">
  </picture>
</div>

<hr>

<div align="center" style="line-height:1">
  <a href="https://stepfun.com/" target="_blank"><img alt="Chat" src="https://img.shields.io/badge/Chat-StepFun-ff6b6b?color=1783ff&logoColor=white"/></a>
  <a href="https://stepfun.com/" target="_blank"><img alt="Homepage" src="https://img.shields.io/badge/Homepage-StepFun-white?logo=StepFun&logoColor=white"/></a>
</div>

<div align="center" style="line-height: 1;">
  <a href="https://github.com/stepfun-ai/Step3" target="_blank"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-StepFun-white?logo=github&logoColor=white"/></a>
  <a href="https://www.modelscope.cn/models/stepfun-ai/step3" target="_blank"><img alt="ModelScope" src="https://img.shields.io/badge/🤖ModelScope-StepFun-ffc107?color=7963eb&logoColor=white"/></a>
  <a href="https://x.com/StepFun_ai" target="_blank"><img alt="Twitter Follow" src="https://img.shields.io/badge/Twitter-StepFun-white?logo=x&logoColor=white"/></a>
</div>

<div align="center" style="line-height: 1;">
<a href="https://discord.com/invite/XHheP5Fn" target="_blank"><img alt="Discord" src="https://img.shields.io/badge/Discord-StepFun-white?logo=discord&logoColor=white"/></a>
  <a href="https://huggingface.co/stepfun-ai/step3/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/badge/License-Apache%202.0-blue?&color=blue"/></a>
</div>

<div align="center">
<b>📰&nbsp;&nbsp;<a href="https://stepfun.ai/research/step3">Step3 Model Blog</a></b> &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp; <b>📄&nbsp;&nbsp;<a href="https://arxiv.org/abs/2507.19427">Step3 System Blog</a></b>
</div>

## Introduction

Step3 is our cutting-edge multimodal reasoning model—built on a Mixture-of-Experts architecture with 321B total parameters and 38B active. 
It is designed end-to-end to minimize decoding costs while delivering top-tier performance in vision–language reasoning. 
Through the co-design of Multi-Matrix Factorization Attention (MFA) and Attention-FFN Disaggregation (AFD), 
Step3 maintains exceptional efficiency across both flagship and low-end accelerators.

### Step3 model card:

|          Config        |  Value  |
|------------------------|---------|
| **Number of Layers (Dense layer included)**|61|
|**Number of Dense Layers**| 5|
| **Hidden Dimension**       | 7168    |
| **Attention Mechanism**    | MFA     |
| **Low-rank Query Dimension** | 2048  |
| **Number of Query Heads**          | 64      |
| **Head Dimension**        | 256     |
|**Number of Experts** |48|
|**Selected Experts per Token**|3|
|**Number of Shared Experts**| 1|
| **Max Context Length** | 65536 |
| **Tokenizer** | Deepseek V3 |
| **Total Parameters (LLM)** | 316B |
| **Activated Params per Token** | 38B |
| **Total Parameters (VLM)** | 321B |


## Evaluation Results
![](figures/step3_bmk.jpeg)

## Deployment

> [!Note]
> Step3's API is accessible at https://platform.stepfun.com/, where we offer OpenAI-compatible API for you.

### Inference with Hugging Face Transformers

We introduce how to use our model at inference stage using transformers library. It is recommended to use python=3.10, torch>=2.1.0, and transformers=4.54.0 as the development environment.We currently only support bf16 inference, and multi-patch for image preprocessing is supported by default. This behavior is aligned with vllm and sglang.


```python
from transformers import AutoProcessor, AutoModelForCausalLM

key_mapping = {
    "^vision_model": "model.vision_model",
    r"^model(?!\.(language_model|vision_model))": "model.language_model",
    "vit_downsampler": "model.vit_downsampler",
    "vit_downsampler2": "model.vit_downsampler2",
    "vit_large_projector": "model.vit_large_projector",
}

model_path = "stepfun-ai/step3"

processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_path, 
                device_map="auto", torch_dtype="auto",trust_remote_code=True, 
                key_mapping=key_mapping)

messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "image": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg"},
            {"type": "text", "text": "What's in this picture?"}
        ]
    },
]

inputs = processor.apply_chat_template(
    messages, add_generation_prompt=True, tokenize=True,
    return_dict=True, return_tensors="pt"
).to(model.device)

generate_ids = model.generate(**inputs, max_new_tokens=32768, do_sample=False)
decoded = processor.decode(generate_ids[0, inputs["input_ids"].shape[-1] :], skip_special_tokens=True)

print(decoded)

```


### Inference with vLLM and SGLang


Our model checkpoints are stored in bf16 and block-fp8 format, you can find it on [Huggingface](https://huggingface.co/collections/stepfun-ai/step3-688a3d652dbb45d868f9d42d).

Currently, it is recommended to run Step3 on the following inference engines:

* vLLM
* SGLang

Deployment and Request examples for vLLM and SGLang can be found in the [Model Deployment Guide](docs/deploy_guidance.md).

## Contact Us
If you have any questions, please reach out at [contact@stepfun.com](mailto:contact@stepfun.com) .

## License
Both the code repository and the model weights are released under the [Apache License (Version 2.0)](./LICENSE).

## Citation
```
@misc{step3system,
      title={Step-3 is Large yet Affordable: Model-system Co-design for Cost-effective Decoding}, 
      author={StepFun Team},
      year={2025},
      eprint={2507.19427},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2507.19427}, 
}

@misc{step3blog,
      title={Step3: Cost-Effective Multimodal Intelligence}, 
      author={StepFun Team},
      url={https://stepfun.ai/research/step3}, 
}
```