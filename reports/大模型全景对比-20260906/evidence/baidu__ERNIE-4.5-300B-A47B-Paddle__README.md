---
license: apache-2.0
language:
- en
- zh
pipeline_tag: text-generation
tags:
- ERNIE4.5
library_name: PaddlePaddle
---

<div align="center" style="line-height: 1;">
  <a href="https://ernie.baidu.com/" target="_blank" style="margin: 2px;">
    <img alt="Chat" src="https://img.shields.io/badge/🤖_Chat-ERNIE_Bot-blue" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://huggingface.co/baidu" target="_blank" style="margin: 2px;">
    <img alt="Hugging Face" src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Baidu-ffc107?color=ffc107&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://github.com/PaddlePaddle/ERNIE" target="_blank" style="margin: 2px;">
    <img alt="Github" src="https://img.shields.io/badge/GitHub-ERNIE-000?logo=github&color=0000FF" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://ernie.baidu.com/blog/ernie4.5" target="_blank" style="margin: 2px;">
    <img alt="Blog" src="https://img.shields.io/badge/🖖_Blog-ERNIE4.5-A020A0" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://discord.gg/JPmZXDsEEK" target="_blank" style="margin: 2px;">
    <img alt="Discord" src="https://img.shields.io/badge/Discord-ERNIE-5865F2?logo=discord&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://x.com/PaddlePaddle" target="_blank" style="margin: 2px;">
    <img alt="X" src="https://img.shields.io/badge/X-PaddlePaddle-6080F0"?logo=x&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>

<div align="center" style="line-height: 1;">
  <a href="#license" style="margin: 2px;">
    <img alt="License" src="https://img.shields.io/badge/License-Apache2.0-A5de54" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>

# ERNIE-4.5-300B-A47B

> [!NOTE]
> Note: "**-Paddle**" models use [PaddlePaddle](https://github.com/PaddlePaddle/Paddle) weights, while "**-PT**" models use Transformer-style PyTorch weights.

## ERNIE 4.5 Highlights

The advanced capabilities of the ERNIE 4.5 models, particularly the MoE-based A47B and A3B series, are underpinned by several key technical innovations:

1. **Multimodal Heterogeneous MoE Pre-Training:** Our models are jointly trained on both textual and visual modalities to better capture the nuances of multimodal information and improve performance on tasks involving text understanding and generation, image understanding, and cross-modal reasoning. To achieve this without one modality hindering the learning of another, we designed a *heterogeneous MoE structure*, incorporated *modality-isolated routing*, and employed *router orthogonal loss* and *multimodal token-balanced loss*. These architectural choices ensure that both modalities are effectively represented, allowing for mutual reinforcement during training.

2. **Scaling-Efficient Infrastructure:** We propose a novel heterogeneous hybrid parallelism and hierarchical load balancing strategy for efficient training of ERNIE 4.5 models. By using intra-node expert parallelism, memory-efficient pipeline scheduling, FP8 mixed-precision training and finegrained recomputation methods, we achieve remarkable pre-training throughput. For inference, we propose *multi-expert parallel collaboration* method and *convolutional code quantization* algorithm to achieve 4-bit/2-bit lossless quantization. Furthermore, we introduce PD disaggregation with dynamic role switching for effective resource utilization to enhance inference performance for ERNIE 4.5 MoE models. Built on [PaddlePaddle](https://github.com/PaddlePaddle/Paddle), ERNIE 4.5 delivers high-performance inference across a wide range of hardware platforms.

3. **Modality-Specific Post-Training:** To meet the diverse requirements of real-world applications, we fine-tuned variants of the pre-trained model for specific modalities. Our LLMs are optimized for general-purpose language understanding and generation. The VLMs focuses on visuallanguage understanding and supports both thinking and non-thinking modes. Each model employed a combination of *Supervised Fine-tuning (SFT)*, *Direct Preference Optimization (DPO)* or a modified reinforcement learning method named *Unified Preference Optimization (UPO)* for post-training.

## Model Overview

ERNIE-4.5-300B-A47B is a text MoE Post-trained model, with 300B total parameters and 47B activated parameters for each token. The following are the model configuration details:

|Key|Value|
|-|-|
|Modality|Text|
|Training Stage|Pretraining|
|Params(Total / Activated)|300B / 47B|
|Layers|54|
|Heads(Q/KV)|64 / 8|
|Text Experts(Total / Activated)|64 / 8|
|Vision Experts(Total / Activated)|64 / 8|
|Context Length|131072|

## Quickstart

### Model Finetuning with ERNIEKit

[ERNIEKit](https://github.com/PaddlePaddle/ERNIE) is a training toolkit based on PaddlePaddle, specifically designed for the ERNIE series of open-source large models. It provides comprehensive support for scenarios such as instruction fine-tuning (SFT, LoRA) and alignment training (DPO), ensuring optimal performance.

Usage Examples:

```bash
# Download model
huggingface-cli download baidu/ERNIE-4.5-300B-A47B-Paddle --local-dir baidu/ERNIE-4.5-300B-A47B-Paddle
# SFT
erniekit train examples/configs/ERNIE-4.5-300B-A47B/sft/run_sft_wint8mix_lora_8k.yaml
# DPO
erniekit train examples/configs/ERNIE-4.5-300B-A47B/dpo/run_dpo_wint8mix_lora_8k.yaml
```

For more detailed examples, including SFT with LoRA, multi-GPU configurations, and advanced scripts, please refer to the examples folder within the [ERNIEKit](https://github.com/PaddlePaddle/ERNIE) repository.




### Using FastDeploy

Service deployment can be quickly completed using FastDeploy in the following command. For more detailed usage instructions, please refer to the [FastDeploy Repository](https://github.com/PaddlePaddle/FastDeploy).

**Note**: To deploy on a configuration with 4 GPUs each having at least 80G of memory, specify ```--quantization wint4```. If you specify ```--quantization wint8```, then resources for 8 GPUs are required.

```bash
python -m fastdeploy.entrypoints.openai.api_server \
       --model baidu/ERNIE-4.5-300B-A47B-Paddle \
       --port 8180 \
       --metrics-port 8181 \
       --quantization wint4 \
       --tensor-parallel-size 8 \
       --engine-worker-queue-port 8182 \
       --max-model-len 32768 \
       --max-num-seqs 32
```

To deploy the sparse attention version to speed up long context using FastDeploy, you can run the following command.
For more details about sparse attention, please refer to the [PLAS Attention](https://github.com/PaddlePaddle/FastDeploy/blob/develop/docs/features/plas_attention.md).

```bash
export FD_ATTENTION_BACKEND="PLAS_ATTN"

python -m fastdeploy.entrypoints.openai.api_server \
       --model baidu/ERNIE-4.5-300B-A47B-Paddle  \
       --port 8180 \
       --metrics-port 8181 \
       --quantization wint4 \
       --tensor-parallel-size 4 \
       --engine-worker-queue-port 8182 \
       --max-model-len 131072 \
       --max-num-seqs 32 \
       --max-num-batched-tokens 8192 \
       --enable-chunked-prefill \
       --plas-attention-config '{"plas_encoder_top_k_left": 50, "plas_encoder_top_k_right": 60,"plas_decoder_top_k_left": 100, "plas_decoder_top_k_right": 120}'
```

To deploy the W4A8C8 quantized version using FastDeploy, you can run the following command.

```bash
python -m fastdeploy.entrypoints.openai.api_server \
       --model baidu/ERNIE-4.5-300B-A47B-W4A8C8-TP4-Paddle \
       --port 8180 \
       --metrics-port 8181 \
       --engine-worker-queue-port 8182 \
       --tensor-parallel-size 4 \
       --max-model-len 32768 \
       --max-num-seqs 32
```

To deploy the WINT2 quantized version using FastDeploy on a single 141G GPU, you can run the following command.

```bash
python -m fastdeploy.entrypoints.openai.api_server \
       --model "baidu/ERNIE-4.5-300B-A47B-2Bits-Paddle" \
       --port 8180 \
       --metrics-port 8181 \
       --engine-worker-queue-port 8182 \
       --tensor-parallel-size 1 \
       --max-model-len  32768 \
       --max-num-seqs 128
```

The following contains a code snippet illustrating how to use ERNIE-4.5-300B-A47B-FP8 generate content based on given inputs.

```python
from fastdeploy import LLM, SamplingParams

prompts = [
    "Hello, my name is",
]

sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=128)

model = "baidu/ERNIE-4.5-300B-A47B-FP8-Paddle"
llm = LLM(model=model, tensor_parallel_size=8, max_model_len=8192, num_gpu_blocks_override=1024, engine_worker_queue_port=9981)

outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs.text
    print("generated_text", generated_text)
```

## Best Practices

### **Sampling Parameters**

To achieve optimal performance, we suggest using `Temperature=0.8`, `TopP=0.8`.

### Prompts for Web Search

For Web Search, {references}, {date}, and {question} are arguments.

For Chinese question, we use the prompt:

```python
ernie_search_zh_prompt = \
'''下面你会收到当前时间、多个不同来源的参考文章和一段对话。你的任务是阅读多个参考文章，并根据参考文章中的信息回答对话中的问题。
以下是当前时间和参考文章：
---------
#当前时间
{date}

#参考文章
{references}

---------
请注意：
1. 回答必须结合问题需求和当前时间，对参考文章的可用性进行判断，避免在回答中使用错误或过时的信息。
2. 当参考文章中的信息无法准确地回答问题时，你需要在回答中提供获取相应信息的建议，或承认无法提供相应信息。
3. 你需要优先根据百科、官网、权威机构、专业网站等高权威性来源的信息来回答问题。
4. 回复需要综合参考文章中的相关数字、案例、法律条文、公式等信息，使你的答案更专业。
5. 当问题属于创作类任务时，需注意以下维度：
   - 态度鲜明：观点、立场清晰明确，避免模棱两可，语言果断直接
   - 文采飞扬：用词精准生动，善用修辞手法，增强感染力
   - 有理有据：逻辑严密递进，结合权威数据/事实支撑论点
---------
下面请结合以上信息，回答问题，补全对话
{question}'''
```

For English question, we use the prompt:

```python
ernie_search_en_prompt = \
'''
Below you will be given the current time, multiple references from different sources, and a conversation. Your task is to read the references and use the information in them to answer the question in the conversation.
Here are the current time and the references:
---------
#Current Time
{date}

#References
{references}

---------
Please note:
1. Based on the question’s requirements and the current time, assess the usefulness of the references to avoid using inaccurate or outdated information in the answer.  
2. If the references do not provide enough information to accurately answer the question, you should suggest how to obtain the relevant information or acknowledge that you are unable to provide it.  
3. Prioritize using information from highly authoritative sources such as encyclopedias, official websites, authoritative institutions, and professional websites when answering questions.
4. Incorporate relevant numbers, cases, legal provisions, formulas, and other details from the references to make your answer more professional.
5. For creative tasks, keep these dimensions in mind:
   - Clear attitude: Clear views and positions, avoid ambiguity, and use decisive and direct language
   - Brilliant writing: Precise and vivid words, good use of rhetoric, and enhance the appeal
   - Well-reasoned: Rigorous logic and progressive, combined with authoritative data/facts to support the argument

---------
Now, using the information above, answer the question and complete the conversation:  
{question}'''
```

Parameter notes:

* {question} is the user’s question
* {date} is the current time, and the recommended format is “YYYY-MM-DD HH:MM:SS, Day of the Week, Beijing/China.”
* {references} is the references, and the recommended format is:

```text
##参考文章1
标题：周杰伦
文章发布时间：2025-04-20
内容：周杰伦(Jay Chou),1979年1月18日出生于台湾省新北市,祖籍福建省永春县,华语流行乐男歌手、音乐人、演员、导演、编剧,毕业于淡江中学。2000年,发行个人首张音乐专辑《Jay》。...
来源网站网址：baike.baidu.com
来源网站的网站名：百度百科

##参考文章2
...
```

## License

The ERNIE 4.5 models are provided under the Apache License 2.0. This license permits commercial use, subject to its terms and conditions. Copyright (c) 2025 Baidu, Inc. All Rights Reserved.

## Citation

If you find ERNIE 4.5 useful or wish to use it in your projects, please kindly cite our technical report:

```bibtex
@misc{ernie2025technicalreport,
      title={ERNIE 4.5 Technical Report},
      author={Baidu ERNIE Team},
      year={2025},
      eprint={},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={}
}
```
