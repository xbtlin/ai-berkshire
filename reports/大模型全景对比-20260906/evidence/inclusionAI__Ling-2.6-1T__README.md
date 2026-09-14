---
license: mit
pipeline_tag: text-generation
library_name: transformers
---
<p align="center">
    <img src="https://mdn.alipayobjects.com/huamei_qa8qxu/afts/img/A*4QxcQrBlTiAAAAAAQXAAAAgAemJ7AQ/original" width="100"/>
</p>
<p align="center">🤗 <a href="https://huggingface.co/inclusionAI">Hugging Face</a>&nbsp;&nbsp; | &nbsp;&nbsp;🤖 <a href="https://modelscope.cn/organization/inclusionAI">ModelScope </a>&nbsp;&nbsp; | &nbsp;&nbsp;🐙 <a href="https://openrouter.ai/inclusionai/ling-2.6-1t:free">OpenRouter </a>&nbsp;&nbsp; | &nbsp;&nbsp; <a href="https://arxiv.org/abs/2606.15079">Tech Report </a></p>

## Ling-2.6-1T: A Trillion-Parameter Comprehensive Flagship Model for Complex Tasks

Today, we are thrilled to open-source **Ling–2.6–1T** from the Ling family.

Tailored for real–world, complex scenarios, this trillion–parameter model introduces targeted optimizations across inference efficiency, token overhead, and agentic capabilities, making it highly effective for **coding and daily workflows**.

Key upgrades in **Ling–2.6–1T** include:

* **High Inference Efficiency:** By adopting a hybrid architecture combining **MLA and Linear Attention**, we dramatically reduce latency and VRAM footprint for long contexts. It delivers superior throughput and lower per–token computational costs without sacrificing expressivity, ensuring real–time responsiveness for complex reasoning and tool calling.
* **Lower Token Overhead via "Fast Thinking":** We introduce a *Contextual Process Redundancy Suppression* reward strategy during post–training. This reduces reliance on verbose chains–of–thought (CoT), utilizing a "fast thinking" mechanism to reach answers directly and compress output costs while maintaining top–tier intelligence.
* **Reliable Multi–Step Execution:** With enhanced reasoning, agentic coding, and instruction following, Ling–2.6–1T achieves **open–source SOTA** on execution–heavy benchmarks, including AIME26, SWE–bench Verified, BFCL–V4, TAU2–Bench, and IFBench.
* **Production–Ready for Agent Workflows:** Designed for end–to–end engineering—from code generation to bug fixing—Ling–2.6–1T integrates seamlessly with mainstream agent frameworks like *Claude Code, OpenClaw, OpenCode, and CodeBuddy*, effortlessly handling multi–tool, multi–step constraints in enterprise environments.


### **Unlocking Robust Intelligence with Superior Efficiency**
On [Artificial Analysis](https://artificialanalysis.ai/), **Ling-2.6-1T** achieved an **Intelligence Index of 34** with approximately 16M output tokens, representing a significant generational leap over the previous Ling-1T. This positioning underscores its ability to deliver high-tier intelligence with optimized token consumption.

<p align="center">
    <img src="https://mdn.alipayobjects.com/huamei_fst7or/afts/img/48cCTY8XJgUAAAAAZvAAAAgADpRXAQJr/original" />
</p>


<p align="center">
    <img src="https://mdn.alipayobjects.com/huamei_fst7or/afts/img/AmTNT5tQHDYAAAAAaSAAAAgADpRXAQJr/original " width="48%"/>
    <img src="https://mdn.alipayobjects.com/huamei_fst7or/afts/img/Wv_8Toxbl7IAAAAAaRAAAAgADpRXAQJr/original"  width="48%"/>
</p>


### **Enhancing Execution Stability for Complex Multi-Step Tasks**

Ling-2.6-1T demonstrates balanced excellence across reasoning, coding, and tool-calling, achieving **open-source SOTA** status on multiple execution-heavy benchmarks:

*   **Advanced Reasoning:** Significantly leads non-thinking models on *AIME26*, showcasing superior complex problem-solving capabilities.
*   **First-Tier Agent Execution:** Ranks among the top models on *SWE-bench Verified, TAU2-Bench, Claw-Eval, BFCL-V4, and PinchBench*, proving high reliability in real-world workflows.
*   **Context & Constraints:** Strong performance on *MRCR (16K–256K)* and *IFBench* ensures logical consistency and precision under complex instructions and long contexts.

<p align="center">
    <img src="https://mdn.alipayobjects.com/huamei_fst7or/afts/img/Ykl9QZamkj0AAAAAgBAAAAgADpRXAQJr/original" />
</p>


Note: If you are interested in the previous version, please visit the past model collections on [Huggingface](https://huggingface.co/inclusionAI) or [ModelScope](https://modelscope.cn/organization/inclusionAI).

## Quickstart

### 🔌 API Usage

https://openrouter.ai/inclusionai/ling-2.6-1t:free

https://zenmux.ai/inclusionai/ling-2.6-1t 

## Deployment

### SGLang

#### Environment Preparation

```shell
pip install uv

uv venv ~/my_ling_env

source ~/my_ling_env/bin/activate

# uv pip "sglang-kernel>=0.4.1"
uv pip install "sglang[all]>=0.5.10.post1" --prerelease=allow
```

#### Run Inference

Here is the example to run Ling-1T with 8 GPUs, where the server port is ${PORT}:

**Server**

**1. Standard Inference (Without MTP)**
```bash
sglang serve \
  --model-path inclusionAI/Ling-2.6-1T \
  --tp-size 8 \
  --max-running-requests 32 \
  --mem-fraction-static 0.92 \
  --chunked-prefill-size 8192 \
  --context-length 262144 \
  --trust-remote-code \
  --model-loader-extra-config '{"enable_multithread_load":"true","num_threads":64}' \
  --tool-call-parser qwen25
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
sglang serve \
  --model-path inclusionAI/Ling-2.6-1T \
  --tp-size 8 \
  --max-running-requests 32 \
  --mem-fraction-static 0.92 \
  --chunked-prefill-size 8192 \
  --context-length 262144 \
  --trust-remote-code \
  --speculative-algorithm EAGLE \
  --speculative-num-steps 3 \
  --speculative-eagle-topk 1 \
  --speculative-num-draft-tokens 4 \
  --mamba-scheduler-strategy extra_buffer \
  --mamba-full-memory-ratio 1.4 \
  --model-loader-extra-config '{"enable_multithread_load":"true","num_threads":64}' \
  --tool-call-parser qwen25
```

**Client**

```bash
curl -s http://${MASTER_IP}:${PORT}/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "auto", "messages": [{"role": "user", "content": "What is the capital of France?"}]}'
```

More usage can be found [here](https://docs.sglang.io/cookbook/autoregressive/InclusionAI/Ling-2.6#3-2-ling-2-6-1t)

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
    --trust-remote-code --tensor-parallel-size 8 \
    --gpu-memory-utilization 0.85
```

**Client**

```bash
curl -s http://${MASTER_IP}:${PORT}/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "auto", "messages": [{"role": "user", "content": "What is the capital of France?"}]}'
```


## Limitations & Future Plans

While Ling-2.6-1T excels in reasoning and agentic efficiency, our future development will focus on:

*   **Intelligence-Efficiency Balance:** Further optimizing token efficiency for knowledge-intensive tasks.
*   **Long-Range Consistency:** Enhancing global consistency in long-term planning and complex information retrieval.
*   **Dynamic Alignment:** Refining cross-lingual alignment to eliminate occasional language-switching offsets under complex instructions.

We remain committed to pushing the boundaries of model performance to enhance delivery efficiency across all complex scenarios.

## License

This code repository is licensed under [the MIT License](https://github.com/inclusionAI/Ling-V2/blob/main/LICENSE).