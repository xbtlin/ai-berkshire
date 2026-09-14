---
license: mit
language:
- en
pipeline_tag: text-generation
---

<p align="center">
    <img src="https://mdn.alipayobjects.com/huamei_qa8qxu/afts/img/A*4QxcQrBlTiAAAAAAQXAAAAgAemJ7AQ/original" width="100"/>
</p>

<p align="center">🤗 <a href="https://huggingface.co/inclusionAI">Hugging Face</a>&nbsp;&nbsp; | &nbsp;&nbsp;🤖 <a href="https://modelscope.cn/organization/inclusionAI">ModelScope </a>&nbsp;&nbsp; | &nbsp;&nbsp;🐙 <a href="https://ling.tbox.cn/chat">ling.tbox.cn</a>&nbsp;&nbsp; | &nbsp;&nbsp; <a href="https://arxiv.org/abs/2606.15079">Tech Report </a></p>

## Ling-2.6-flash: Faster Responses, Stronger Execution, Higher Token Efficiency
### Introduction
Today, we announce the official open-source release of **Ling-2.6-flash**, an **instruct model** with **104B total parameters** and **7.4B active parameters**. 

As agent capabilities mature, skyrocketing **token consumption** has become a primary barrier to deployment. Unlike standard chat, agent workflows involve massive inputs and complex, multi-step execution, driving up both compute demand and user costs. While the industry is pivoting toward "long-reasoning" to push performance ceilings, a critical question remains: Are these excessive reasoning tokens truly necessary for high-frequency, everyday agent use cases?

Faced with mounting token pressure, Ling-2.6-flash takes a different path. Rather than relying on longer outputs to chase higher scores, it is systematically optimized for **inference efficiency, token efficiency, and agent performance**—aiming to stay highly competitive while being **faster, leaner, and better suited for real production workloads**.

At a high level, Ling-2.6-flash is built around three core strengths:

+ **Hybrid linear architecture for higher inference efficiency.**  
By introducing a hybrid linear architecture, we improve computational efficiency at the foundation level. On a 4× H20 setup, Ling-2.6-flash reaches inference speeds of up to **340 tokens/s**. In other words, it completes tasks with significantly better cost-performance efficiency.
+ **Token-efficiency optimization for a better intelligence-efficiency tradeoff.**  
During training, we specifically optimized for token efficiency, with the goal of accomplishing tasks using more concise outputs. On the full **Artificial Analysis** evaluation suite, Ling-2.6-flash uses only **15M tokens** while still delivering competitive performance. This translates into a meaningfully stronger intelligence-efficiency profile.
+ **Targeted improvements for agent scenarios.**  
For the agent use cases seeing the strongest demand today, we continuously refined Ling-2.6-flash in tool use, multi-step planning, and task execution. As a result, the model achieves performance that is competitive with, and in some cases reaches **SOTA level** against, models with larger active parameter counts on benchmarks including **BFCL-V4, TAU2-bench, SWE-bench Verified, Claw-Eval, and PinchBench**.

### Evaluation
We have conducted a comprehensive evaluation of Ling-2.6-flash across multiple authoritative benchmarks. **Ling-2.6-flash** performs strongly on representative agent benchmarks such as **BFCL-V4**, **TAU2-bench**, **SWE-bench Verified**, and **PinchBench**. In practice, Ling-2.6-flash delivers a strong user experience across frameworks including **Claude Code**, **Kilo Code**, **Qwen Code**, **Hermes Agent**, and **OpenClaw**, etc. 

Beyond agent tasks, Ling-2.6-flash also delivers strong performance across **general knowledge**,**mathematical reasoning**, **instruction following**, and **long-context understanding**, remains well aligned with SOTA models in the same size class.
<div align="center">
<img src="https://mdn.alipayobjects.com/huamei_3p6pd0/afts/img/KhFxSrxyF5IAAAAAgCAAAAgADryCAQFr/original" width="8001" title="" crop="0,0,1,1" id="u4a7a4034" class="ne-image">
</div>

<div align="center">
<img src="https://mdn.alipayobjects.com/huamei_3p6pd0/afts/img/4bI1SK8pNM8AAAAAgBAAAAgADryCAQFr/original" width="8001" title="" crop="0,0,1,1" id="uc95688f2" class="ne-image">
</div>

> + **<font style="color:rgb(38, 38, 38);">PinchBench</font>**<font style="color:rgb(38, 38, 38);">: Comparative scores are retrieved directly from the official PinchBench leaderboard (as of April 20, 2026), adhering to their evaluation modes (potentially Reasoning Mode). </font>
> + **<font style="color:rgb(38, 38, 38);">Claw-Eval</font>**<font style="color:rgb(38, 38, 38);">: Comparative scores are sourced from the official Claw-Eval leaderboard (version dated 2026-03-25), adhering to their evaluation modes (potentially Reasoning Mode). Official scores for GPT-OSS-120B and GPT-5.4-mini are currently unavailable and have been omitted.</font>
> + **<font style="color:rgb(38, 38, 38);">TAU2-Bench</font>**<font style="color:rgb(38, 38, 38);">: Evaluations are conducted using official v1.0.0 code and datasets. Following the GLM-5 evaluation protocol, we applied minor prompt adjustments in the Retail and Telecom domains to ensure users express requests clearly and to prevent premature session termination. Additionally, GPT-5.2 was utilized as the User Agent across all evaluated domains.</font>
> + **<font style="color:rgb(38, 38, 38);">IFBench</font>**<font style="color:rgb(38, 38, 38);">: Scores for GPT-OSS-120B (low) and GPT-5.4-mini (Non-Reasoning) are sourced from the AA (Artificial Analysis) Leaderboard. All other model performance data are based on internal evaluation results.</font>
>

### Architecture
Ling-2.6-flash continues the architectural direction introduced in Ling 2.5. Building on the Ling 2.0 foundation, we incorporate a **hybrid linear attention mechanism**, upgrading the original **GQA attention** design into a **1:7 MLA + Lightning Linear** hybrid architecture through incremental training.
<div align="center">
<img src="https://mdn.alipayobjects.com/huamei_3p6pd0/afts/img/dZ9VS4RPjzAAAAAAgBAAAAgADryCAQFr/fmt.webp" width="650" title="" crop="0,0,1,1" id="u46a87a11" class="ne-image">
</div>

This combination of **hybrid attention** and a **highly sparse MoE architecture** gives Ling-2.6-flash a clear advantage in inference efficiency. Compared with mainstream SOTA models in a similar size class, Ling-2.6-flash not only delivers faster time-to-first-token, but also achieves substantially higher generation throughput in long-output scenarios. At peak, both **prefill throughput** and **decode throughput** can improve by up to **around 4×**.

As shown in the figure below, Ling-2.6-flash’s throughput advantage becomes more pronounced as both context length and generation length increase. More importantly, this is not just a benchmark-side gain on static metrics. In real deployment settings, the model continues to unlock stronger speed benefits as task complexity grows.

Whether the workload involves **long-context understanding** or **extended text generation**, Ling-2.6-flash preserves model capability while delivering **faster responses, higher throughput, and better real-world deployment efficiency**.
<div align="center">
  <img src="https://mdn.alipayobjects.com/huamei_3p6pd0/afts/img/Fa_fQrVD3hcAAAAAX7AAAAgADryCAQFr/original" width="600" alt="Decode Throughput Comparison">
  <p><em>Decode Throughput Comparison, 4× H20-3e, TP=4, Batch Size = 32</em></p>
</div>

<div align="center">
  <img src="https://mdn.alipayobjects.com/huamei_3p6pd0/afts/img/LRDBTILYEooAAAAAXdAAAAgADryCAQFr/original" width="600" alt="Prefill Throughput Comparison">
  <p><em>Prefill Throughput Comparison, 4× H20-3e, TP=4, Batch Size = 32</em></p>
</div>

### Quickstart
#### SGLang (Recommended)
##### Environment Preparation
```bash
pip install uv

uv venv ~/my_ling_env

source ~/my_ling_env/bin/activate

# uv pip "sglang-kernel>=0.4.1"
uv pip install "sglang[all]>=0.5.10.post1" --prerelease=allow
```

##### Run Inference
Both BF16 and FP8 models are supported by SGLang now. It depends on the dtype of the model in `${MODEL_PATH}`. Here is the example to run Ling-2.6-flash with 4 GPUs, where the master node IP is `${MASTER_IP}` and server port is `${PORT}`:

**Server**

**1. Standard Inference (Without MTP)**
```bash
python -m sglang.launch_server \
    --model-path $MODEL_PATH \
    --tp-size 4 \
    --pp-size 1 \
    --dp-size 1 \
    --trust-remote-code \
    --context-length 262144 \
    --tool-call-parser qwen25 \
    --json-model-override-args '{"rope_scaling": {"rope_type": "yarn", "factor": 2.0, "rope_theta": 6000000, "partial_rotary_factor": 0.5, "original_max_position_embeddings": 131072}}' \
    --dist-init-addr $MASTER_IP:2345 \
    --port $PORT \
    --nnodes 1
```

**2. Inference with MTP (Multi-Token Prediction)**  
_The current official SGLang implementation of MTP contains a bug. For better inference performance, we recommend installing our patched version. Our fix is currently under review and is expected to be merged into the official SGLang library shortly._

**Install our SGLang**
```bash
git clone -b ling_2_6 git@github.com:antgroup/sglang.git
cd sglang

pip install --upgrade pip
pip install -e "python"
```
Start server
```bash
python -m sglang.launch_server \
    --model-path $MODEL_PATH \
    --tp-size 4 \
    --pp-size 1 \
    --dp-size 1 \
    --context-length 262144 \
    --mamba-scheduler-strategy extra_buffer \
    --speculative-algorithm NEXTN \
    --speculative-num-steps 3 \
    --speculative-eagle-topk 1 \
    --speculative-num-draft-tokens 4 \
    --mem-fraction-static 0.75 \
    --max-running-requests 64 \
    --max-mamba-cache-size 256 \
    --tool-call-parser qwen25 \
    --json-model-override-args '{"rope_scaling": {"rope_type": "yarn", "factor": 2.0, "rope_theta": 6000000, "partial_rotary_factor": 0.5, "original_max_position_embeddings": 131072}}' \
    --trust-remote-code \
    --dist-init-addr $MASTER_IP:2345 \
    --port $PORT \
    --nnodes 1
```

**Client**

```bash
curl -s http://${MASTER_IP}:${PORT}/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "auto", "messages": [{"role": "user", "content": "What is the capital of France?"}]}'
```

#### vLLM
##### Environment Preparation
```bash
pip install uv

uv venv ~/my_ling_env

source ~/my_ling_env/bin/activate

git clone https://github.com/vllm-project/vllm.git

cd vllm

VLLM_USE_PRECOMPILED=1 uv pip install --editable . --torch-backend=auto
```

#### Run inference

**Server**
```bash
vllm serve $MODEL_PATH \
    --port $PORT \
    --served-model-name my_model \
    --trust-remote-code --tensor-parallel-size 4 \
    --gpu-memory-utilization 0.85
```

**Client**

```bash
curl -s http://${MASTER_IP}:${PORT}/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "auto", "messages": [{"role": "user", "content": "What is the capital of France?"}]}'
```

### Limitations & Future Plans
Ling-2.6-flash has already made meaningful progress in our pursuit of an extreme intelligence-efficiency tradeoff. The model has improved substantially in key areas such as **tool use, multi-step planning, and long-horizon task execution**. Combined with systematic optimizations in inference efficiency and interaction experience, Ling-2.6-flash is now better equipped to handle **large-scale, high-frequency automated workloads**, delivering stronger real-world value in production settings.

At the same time, we are fully aware that pushing intelligence efficiency to the limit comes with tradeoffs. In some highly complex scenarios, the model can still exhibit **tool hallucinations** due to limited reasoning depth. In addition, there is still room for improvement in areas such as **natural bilingual switching between Chinese and English** and **compliance with highly complex instructions**.

Looking ahead, we will continue exploring the frontier of intelligence efficiency. While preserving the model’s high-efficiency inference characteristics, we aim to further improve the balance between **output quality** and **token efficiency**, and to continuously strengthen the model’s **stability, usability, and interaction experience across a wider range of real-world scenarios**.