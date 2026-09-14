---
license: apache-2.0
base_model:
- stepfun-ai/step-3.5-flash
library_name: transformers
---

# Step 3.5 Flash

<div align="center">
  
<div align="center" style="display: flex; justify-content: center; align-items: center;">
  <img src="stepfun.svg" width="25" style="margin-right: 10px;"/>
  <h1 style="margin: 0; border-bottom: none;">Step 3.5 Flash</h1>
</div>

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/stepfun-ai/Step-3.5-Flash)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20HF-StepFun/STEP3p5-preview)](https://huggingface.co/stepfun-ai/Step-3.5-Flash)
[![ModelScope](https://img.shields.io/badge/ModelScope-StepFun/STEP3p5-preview)](https://modelscope.cn/models/stepfun-ai/Step-3.5-Flash)
[![Discord](https://img.shields.io/badge/Discord-Join-5865F2?logo=discord&logoColor=white)](https://discord.gg/RcMJhNVAQc)
[![Webpage](https://img.shields.io/badge/Webpage-Blog-blue)](https://static.stepfun.com/blog/step-3.5-flash/)
[![Paper](https://img.shields.io/badge/Arxiv-TechReport-red)](https://arxiv.org/abs/2602.10604)
[![License](https://img.shields.io/badge/License-Apache%202.0-green)]()
[![Chat with the model on OpenRouter](https://img.shields.io/badge/Chat%20with%20the%20model-OpenRouter-5B3DF5?logo=chatbot&logoColor=white)](https://openrouter.ai/chat?models=stepfun/step-3.5-flash:free)
[![Chat with the model on HuggingfaceSpace](https://img.shields.io/badge/Chat%20with%20the%20model-HuggingfaceSpace-5B3DF5?logo=chatbot&logoColor=white)](https://huggingface.co/spaces/stepfun-ai/Step-3.5-Flash)
</div>



## 1. Introduction 

**Step 3.5 Flash** ([visit website](https://static.stepfun.com/blog/step-3.5-flash/)) is our most capable open-source foundation model, engineered to deliver frontier reasoning and agentic capabilities with exceptional efficiency. Built on a sparse Mixture of Experts (MoE) architecture, it selectively activates only 11B of its 196B parameters per token. This "intelligence density" allows it to rival the reasoning depth of top-tier proprietary models, while maintaining the agility required for real-time interaction.

## 2. Key Capabilities

- **Deep Reasoning at Speed**: While chatbots are built for reading, agents must reason fast. Powered by 3-way Multi-Token Prediction (MTP-3), Step 3.5 Flash achieves a generation throughput of **100–300 tok/s** in typical usage (peaking at **350 tok/s** for single-stream coding tasks). This allows for complex, multi-step reasoning chains with immediate responsiveness.

- **A Robust Engine for Coding & Agents**: Step 3.5 Flash is purpose-built for agentic tasks, integrating a scalable RL framework that drives consistent self-improvement. It achieves **74.4% on SWE-bench Verified** and **51.0% on Terminal-Bench 2.0**, proving its ability to handle sophisticated, long-horizon tasks with unwavering stability.

- **Efficient Long Context**: The model supports a cost-efficient **256K context window** by employing a 3:1 Sliding Window Attention (SWA) ratio—integrating three SWA layers for every full-attention layer. This hybrid approach ensures consistent performance across massive datasets or long codebases while significantly reducing the computational overhead typical of standard long-context models.

- **Accessible Local Deployment**: Optimized for accessibility, Step 3.5 Flash brings elite-level intelligence to local environments. It runs securely on high-end consumer hardware (e.g., Mac Studio M4 Max, NVIDIA DGX Spark), ensuring data privacy without sacrificing performance.

## 3. Performance

Step 3.5 Flash delivers performance parity with leading closed-source systems while remaining open and efficient.

![](step-bar-chart.png)

Performance of Step 3.5 Flash measured across **Reasoning**, **Coding**, and **Agentic Abilities**. Open-source models (left) are sorted by their total parameter count, while top-tier proprietary models are shown on the right. xbench-DeepSearch scores are sourced from [official publications](https://xbench.org/agi/aisearch) for consistency. The shadowed bars represent the enhanced performance of Step 3.5 Flash using [Parallel Thinking](https://arxiv.org/pdf/2601.05593).

### Detailed Benchmarks

| Benchmark | Step 3.5 Flash | DeepSeek V3.2 | Kimi K2 Thinking / K2.5 | GLM-4.7 | MiniMax M2.1 | MiMo-V2 Flash |
| --- | --- | --- | --- | --- | --- | --- |
| # Activated Params | 11B | 37B | 32B | 32B | 10B | 15B |
| # Total Params (MoE) | 196B | 671B | 1T | 355B | 230B | 309B |
| Est. decoding cost @ 128K context, Hopper GPU** | **1.0x**<br>100 tok/s, MTP-3, EP8 | **6.0x**<br>33 tok/s, MTP-1, EP32 | **18.9x**<br>33 tok/s, no MTP, EP32 | **18.9x**<br>100 tok/s, MTP-3, EP8 | **3.9x**<br>100 tok/s, MTP-3, EP8 | **1.2x**<br>100 tok/s, MTP-3, EP8 |
| | | | **Agent** | | | |
| τ²-Bench | 88.2 | 80.3 (85.2*) | 74.3*/85.4* | 87.4 | 86.6* | 80.3 (84.1*) |
| BrowseComp | 51.6 | 51.4 | 41.5* / 60.6 | 52.0 | 47.4 | 45.4 |
| BrowseComp (w/ Context Manager) | 69.0 | 67.6 | 60.2/74.9 | 67.5 | 62.0 | 58.3 |
| BrowseComp-ZH | 66.9 | 65.0 | 62.3 / 62.3* | 66.6 | 47.8* | 51.2* |
| BrowseComp-ZH (w/ Context Manager) | 73.7 | — | —/— | — | — | — |
| GAIA (no file) | 84.5 | 75.1* | 75.6*/75.9* | 61.9* | 64.3* | 78.2* |
| xbench-DeepSearch (2025.05) | 83.7 | 78.0* | 76.0*/76.7* | 72.0* | 68.7* | 69.3* |
| xbench-DeepSearch (2025.10) | 56.3 | 55.7* | —/40+ | 52.3* | 43.0* | 44.0* |
| ResearchRubrics | 65.3 | 55.8* | 56.2*/59.5* | 62.0* | 60.2* | 54.3* |
| | | | **Reasoning** | | | |
| AIME 2025 | 97.3 | 93.1 | 94.5/96.1 | 95.7 | 83.0 | 94.1 (95.1*) |
| HMMT 2025 (Feb.) | 98.4 | 92.5 | 89.4/95.4 | 97.1 | 71.0* | 84.4 (95.4*) |
| HMMT 2025 (Nov.) | 94.0 | 90.2 | 89.2*/— | 93.5 | 74.3* | 91.0* |
| IMOAnswerBench | 85.4 | 78.3 | 78.6/81.8 | 82.0 | 60.4* | 80.9* |
| | | | **Coding** | | | |
| LiveCodeBench-V6 | 86.4 | 83.3 | 83.1/85.0 | 84.9 | — | 80.6 (81.6*) |
| SWE-bench Verified | 74.4 | 73.1 | 71.3/76.8 | 73.8 | 74.0 | 73.4 |
| Terminal-Bench 2.0 | 51.0 | 46.4 | 35.7*/50.8 | 41.0 | 47.9 | 38.5 |

**Notes**:
1. "—" indicates the score is not publicly available or not tested.
2. "*" indicates the original score was inaccessible or lower than our reproduced, so we report the evaluation under the same test conditions as Step 3.5 Flash to ensure fair comparability.
3. **BrowseComp (with Context Manager)**: When the effective context length exceeds a predefined threshold, the agent resets the context and restarts the agent loop. By contrast, Kimi K2.5 and DeepSeek-V3.2 used a "discard-all" strategy.
4. **Decoding Cost**: Estimates are based on a methodology similar to, but more accurate than, the approach described arxiv.org/abs/2507.19427

### Recommended Inference Parameters
1. For general chat domain, we suggest: `temperature=0.6, top_p=0.95`
2. For reasoning / agent scenario, we recommend: `temperature=1.0, top_p=0.95`.

## 4. Architecture Details

Step 3.5 Flash is built on a **Sparse Mixture-of-Experts (MoE)** transformer architecture, optimized for high throughput and low VRAM usage during inference.

### 4.1 Technical Specifications

| Component | Specification |
| :--- | :--- |
| **Backbone** | 45-layer Transformer (4,096 hidden dim) |
| **Context Window** | 256K |
| **Vocabulary** | 128,896 tokens |
| **Total Parameters** | **196.81B** (196B Backbone + 0.81B Head) |
| **Active Parameters** | **~11B** (per token generation) |

### 4.2 Mixture of Experts (MoE) Routing

Unlike traditional dense models, Step 3.5 Flash uses a fine-grained routing strategy to maximize efficiency:
- **Fine-Grained Experts**: 288 routed experts per layer + 1 shared expert (always active).
- **Sparse Activation**: Only the Top-8 experts are selected per token.
- **Result**: The model retains the "memory" of a 196B parameter model but executes with the speed of an 11B model. 

### 4.3 Multi-Token Prediction (MTP)

To improve inference speed, we utilize a specialized MTP Head consisting of a sliding-window attention mechanism and a dense Feed-Forward Network (FFN). This module predicts 4 tokens simultaneously in a single forward pass, significantly accelerating inference without degrading quality.

## 5. Quick Start

You can get started with Step 3.5 Flash in minutes using Cloud API via our supported providers.

### 5.1 Get Your API Key.

Sign up at [OpenRouter](https://openrouter.ai) or [platform.stepfun.ai](https://platform.stepfun.ai), and grab your API key. 

> OpenRouter now offers free trial for Step 3.5 Flash.

| Provider | Website | Base URL |
| :--- | :--- | :--- |
| OpenRouter | https://openrouter.ai | https://openrouter.ai/api/v1 |
| StepFun | https://platform.stepfun.ai | https://api.stepfun.ai/v1 |

### 5.2 Setup

Install the standard OpenAI SDK (compatible with both platforms).

```bash
pip install --upgrade "openai>=1.0"
```

Note: OpenRouter supports multiple SDKs. Learn more [here](https://openrouter.ai/docs/quickstart).

### 5.3 Implementation Example

This example shows starting a chat with Step 3.5 Flash.

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.stepfun.ai/v1", # or "https://openrouter.ai/api/v1"
    # Optional: OpenRouter headers for app rankings
    default_headers={
        "HTTP-Referer": "<YOUR_SITE_URL>", 
        "X-Title": "<YOUR_SITE_NAME>",
    }
)

completion = client.chat.completions.create(
    model="step-3.5-flash", # Use "stepfun/step-3.5-flash" for OpenRouter
    messages=[
        {
            "role": "system",
            "content": "You are an AI chat assistant provided by StepFun. You are good at Chinese, English, and many other languages.",
        },
        {
            "role": "user",
            "content": "Introduce StepFun's artificial intelligence capabilities."
        },
    ],
)

print(completion.choices[0].message.content)
```

## 6. Local Deployment

Step 3.5 Flash is optimized for local inference and supports industry-standard backends including vLLM, SGLang, Hugging Face Transformers and llama.cpp.

### 6.1 vLLM 
We recommend using the latest nightly build of vLLM.
1. Install vLLM.

```bash
# via Docker
docker pull vllm/vllm-openai:nightly

# or via pip (nightly wheels)
pip install -U vllm --pre \
  --index-url https://pypi.org/simple \
  --extra-index-url https://wheels.vllm.ai/nightly
```
2. Launch the server.

**Note**: Full MTP3 support is not yet available in vLLM. We are actively working on a Pull Request to integrate this feature, which is expected to significantly enhance decoding performance.

  - For fp8 model
```bash  
vllm serve <MODEL_PATH_OR_HF_ID> \
  --served-model-name step3p5-flash \
  --tensor-parallel-size 8 \
  --enable-expert-parallel \
  --disable-cascade-attn \
  --reasoning-parser step3p5 \
  --enable-auto-tool-choice \
  --tool-call-parser step3p5 \
  --hf-overrides '{"num_nextn_predict_layers": 1}' \
  --speculative_config '{"method": "step3p5_mtp", "num_speculative_tokens": 1}' \
  --trust-remote-code \
  --quantization fp8
```

  - For bf16 model
```bash
vllm serve <MODEL_PATH_OR_HF_ID> \
  --served-model-name step3p5-flash \
  --tensor-parallel-size 8 \
  --enable-expert-parallel \
  --disable-cascade-attn \
  --reasoning-parser step3p5 \
  --enable-auto-tool-choice \
  --tool-call-parser step3p5 \
  --hf-overrides '{"num_nextn_predict_layers": 1}' \
  --speculative_config '{"method": "step3p5_mtp", "num_speculative_tokens": 1}' \
  --trust-remote-code    
```
You can also refer to the [Step-3.5-Flash](https://github.com/vllm-project/recipes/blob/main/StepFun/Step-3.5-Flash.md) recipe.

### 6.2 SGLang

1. Install SGLang.
```bash
# via Docker
docker pull lmsysorg/sglang:dev-pr-18084
# or from source (pip)
pip install "sglang[all] @ git+https://github.com/sgl-project/sglang.git"
```

2. Launch the server.
  - For bf16 model

```bash
sglang serve --model-path <MODEL_PATH_OR_HF_ID> \
  --served-model-name step3p5-flash \
  --tp-size 8 \
  --tool-call-parser step3p5 \
  --reasoning-parser step3p5 \
  --speculative-algorithm EAGLE \
  --speculative-num-steps 3 \
  --speculative-eagle-topk 1 \
  --speculative-num-draft-tokens 4 \
  --enable-multi-layer-eagle \
  --host 0.0.0.0 \
  --port 8000
```
  - For fp8 model
```bash
sglang serve --model-path <MODEL_PATH_OR_HF_ID> \
  --served-model-name step3p5-flash \
  --tp-size 8 \
  --ep-size 8 \
  --tool-call-parser step3p5 \
  --reasoning-parser step3p5 \
  --speculative-algorithm EAGLE \
  --speculative-num-steps 3 \
  --speculative-eagle-topk 1 \
  --speculative-num-draft-tokens 4 \
  --enable-multi-layer-eagle \
  --host 0.0.0.0 \
  --port 8000
```

### 6.3 Transformers (Debug / Verification)

Use this snippet for quick functional verification. For high-throughput serving, use vLLM or SGLang.
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_PATH = "<MODEL_PATH_OR_HF_ID>"

# 1. Setup
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    trust_remote_code=True,
    torch_dtype="auto",
    device_map="auto",
)

# 2. Prepare Input
messages = [{"role": "user", "content": "Explain the significance of the number 42."}]
inputs = tokenizer.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_dict=True,
    return_tensors="pt",
).to(model.device)

# 3. Generate
generated_ids = model.generate(**inputs, max_new_tokens=128, do_sample=False)
output_text = tokenizer.decode(generated_ids[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)

print(output_text)
```

### 6.4 llama.cpp

#### System Requirements
- GGUF Model Weights(int4): 111.5 GB
- Runtime Overhead: ~7 GB
- Minimum VRAM: 120 GB (e.g., Mac studio, DGX-Spark, AMD Ryzen AI Max+ 395)
- Recommended: 128GB unified memory
#### Steps
1. Use official llama.cpp:
> the folder `Step-3.5-Flash/tree/main/llama.cpp` is **obsolete**
```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
```
2. Build llama.cpp on Mac:
```bash
cmake -S . -B build-macos \
  -DCMAKE_BUILD_TYPE=Release \
  -DGGML_METAL=ON \
  -DGGML_ACCELERATE=ON \
  -DLLAMA_BUILD_EXAMPLES=ON \
  -DLLAMA_BUILD_COMMON=ON \
  -DGGML_LTO=ON
cmake --build build-macos -j8
```
3. Build llama.cpp on DGX-Spark:
```bash
cmake -S . -B build-cuda \
  -DCMAKE_BUILD_TYPE=Release \
  -DGGML_CUDA=ON \
  -DGGML_CUDA_GRAPHS=ON \
  -DLLAMA_CURL=OFF \
  -DLLAMA_BUILD_EXAMPLES=ON \
  -DLLAMA_BUILD_COMMON=ON
cmake --build build-cuda -j8
```
4. Build llama.cpp on AMD Windows:
```bash
cmake -S . -B build-vulkan \
  -DCMAKE_BUILD_TYPE=Release \
  -DLLAMA_CURL=OFF \
  -DGGML_OPENMP=ON \
  -DGGML_VULKAN=ON
cmake --build build-vulkan -j8
```
5. Run with llama-cli
```bash
./llama-cli -m step3.5_flash_Q4_K_S.gguf -c 16384 -b 2048 -ub 2048 -fa on --temp 1.0 -p "What's your name?"
```
6. Test performance with llama-batched-bench:
```bash
./llama-batched-bench -m step3.5_flash_Q4_K_S.gguf -c 32768 -b 2048 -ub 2048 -npp 0,2048,8192,16384,32768 -ntg 128 -npl 1
```

## 7. Using Step 3.5 Flash on Agent Platforms

### 7.1 Claude Code & Codex
It's straightforward to add Step 3.5 Flash to the list of models in most coding environments. See below for the instructions for configuring Claude Code and Codex to use Step 3.5 Flash.

#### 7.1.1 Prerequisites
Sign up at StepFun.ai or OpenRouter and grab an API key, as mentioned in the Quick Start.

#### 7.1.2 Environment setup
Claude Code and Codex rely on Node.js. We recommend installing Node.js version > v20. You can install Node via nvm.

**Mac/Linux**:
```bash
# Install nvm on Mac/Linux via curl：
# Step 1
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Copy the full command
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

# Users in China can set up npm mirror
config set registry https://registry.npmmirror.com

# Step 2
nvm install v22

# Make sure Node.js is installed
node --version

npm --version
```

**Windows**:
You can download the installation file (`nvm-setup.exe`) from [https://github.com/coreybutler/nvm-windows/releases](https://github.com/coreybutler/nvm-windows/releases). Follow the instructions to install nvm. Run nvm commands to make sure it is installed.

#### 7.1.3 Use Step 3.5 Flash on Claude Code

1. Install Claude Code.
```bash
# install claude code via npm
npm install -g @anthropic-ai/claude-code

# test if the installation is successful
claude --version 
```

2. Configure Claude Code.

  To accommodate diverse workflows in Claude Code, we support both **Anthropic-style** and **OpenAI-style** APIs. 

  **Option A: Anthropic API style**:

  > If you intend to use the **OpenRouter** API, refer to the OpenRouter integration guide.  

  Step 1: Edit Claude Settings. Update `~/.claude/settings.json`.
  > You only need to modify the fields shown below. Leave the rest of the file unchanged.

  ```json
  {
  "env": {
    "ANTHROPIC_API_KEY": "API_KEY_from_StepFun",
    "ANTHROPIC_BASE_URL": "https://api.stepfun.ai/"
  },
  "model": "step-3.5-flash"
  }
  ```
  Step 2: Start Claude Code.
  
  Save the file, and then start Claude Code. Run `/status` to confirm the model and base URL.

  ```txt
  ❯ /status
  ─────────────────────────────────────────────────────────────────────────────────
  Settings:  Status   Config   Usage  (←/→ or tab to cycle)

  Version: 2.1.1
  Session name: /rename to add a name
  Session ID: 676dae61-259d-4eef-8c2f-0f1641600553
  cwd: /Users/step-test/
  Auth token: none
  API key: ANTHROPIC_API_KEY
  Anthropic base URL: https://api.stepfun.ai/

  Model: step-3.5-flash
  Setting sources: User settings
  ```

  **Option B: OpenAI API style**

  > Note: OpenAI API style here refers to the `chat/completions/` format.

  > We recommend using `claude-code-router`. For details, see [https://github.com/musistudio/claude-code-router](https://github.com/musistudio/claude-code-router).

  After Claude Code is installed, install `claude-code-router` :

  ```bash
  # install ccr via npm
  npm install -g @musistudio/claude-code-router

  # validate it is installed
  ccr -v
  ```

  Add the following configurations to `~/.claude-code-router/config.json`.

  ```json
  {
  "PORT": 3456,
  "Providers": [
    {
      "name": "stepfun-api",
      "api_base_url": "https://api.stepfun.com/v1/chat/completions",
      "api_key": "StepFun_API_KEY",
      "models": ["step-3.5-flash"],
      "transformer":{
           "step-3.5-flash": { "use": ["OpenAI"]}
      }
    }
  ],
  "Router": {
    "default": "stepfun-api,step-3.5-flash",
    "background": "stepfun-api,step-3.5-flash",
    "think": "stepfun-api,step-3.5-flash",
    "longContext": "stepfun-api,step-3.5-flash",
    "webSearch": "stepfun-api,step-3.5-flash"
  }
  }
  ```
  You can now start Claude Code:

  ```bash
  # Start Claude
  ccr code 

  # restart ccr if configs are changed
  ccr restart 
  ```

#### 7.1.4 Use Step 3.5 Flash on Codex
1. Install Codex
```bash
# Install codex via npm
npm install -g @openai/codex

# Test if it is installed
codex --version
```

2. Configure Codex
Add the following settings to `~/.codex/config.toml`, keeping the rest of the settings as they are.

```json
model="step-3.5-flash"
model_provider = "stepfun-chat"
preferred_auth_method = "apikey"

# configure the provider
[model_providers.stepfun-chat]
name = "OpenAI using response"
base_url = "https://api.stepfun.com/v1"
env_key = "OPENAI_API_KEY"
wire_api = "chat"
query_params = {}
```

For Codex, `wire_api` only supports `chat` . If you use the `responses` mode, you'll need to change to `chat`. Please also switch `model_provider` to the newly configured `stepfun-chat`.

When finishing the configuration, run codex in a new Terminal window to start Codex. Run `/status` to check the configuration.

```bash
/status
📂 Workspace
  • Path: /Users/step-test/
  • Approval Mode: on-request
  • Sandbox: workspace-write
  • AGENTS files: (none)

🧠 Model
  • Name: step-3.5-flash
  • Provider: Stepfun-chat

💻 Client
  • CLI Version: 0.40.0
```

#### 7.1.5 Use Step 3.5 Flash on Step-DeepResearch (DeepResearch)
1. Use the reference environment setup below and configure `MODEL_NAME` to `Step-3.5-Flash`. [https://github.com/stepfun-ai/StepDeepResearch?tab=readme-ov-file#1-environment-setup](https://github.com/stepfun-ai/StepDeepResearch?tab=readme-ov-file#1-environment-setup)


## 8. Known Issues and Future Directions

1. **Token Efficiency**. Step 3.5 Flash achieves frontier-level agentic intelligence but currently relies on longer generation trajectories than Gemini 3.0 Pro to reach comparable quality.
2. **Efficient Universal Mastery**. We aim to unify generalist versatility with deep domain expertise. To achieve this efficiently, we are advancing variants of on-policy distillation, allowing the model to internalize expert behaviors with higher sample efficiency.
3. **RL for More Agentic Tasks**. While Step 3.5 Flash demonstrates competitive performance on academic agentic benchmarks, the next frontier of agentic AI necessitates the application of RL to intricate, expert-level tasks found in professional work, engineering, and research.
4. **Operational Scope and Constraints**. Step 3.5 Flash is tailored for coding and work-centric tasks, but may experience reduced stability during distribution shifts. This typically occurs in highly specialized domains or long-horizon, multi-turn dialogues, where the model may exhibit repetitive reasoning, mixed-language outputs, or inconsistencies in time and identity awareness.

## 9. Co-Developing the Future

We view our roadmap as a living document, evolving continuously based on real-world usage and developer feedback.
As we work to shape the future of AGI by expanding broad model capabilities, we want to ensure we are solving the right problems. We invite you to be part of this continuous feedback loop—your insights directly influence our priorities.

- **Join the Conversation**: Our Discord community is the primary hub for brainstorming future architectures, proposing capabilities, and getting early access updates 🚀
- **Report Friction**: Encountering limitations? You can open an issue on GitHub or flag it directly in our Discord support channels.

## 📜 Citation

If you find this project useful in your research, please cite our technical report:

```tex
@misc{huang2026step35flashopen,
      title={Step 3.5 Flash: Open Frontier-Level Intelligence with 11B Active Parameters}, 
      author={Ailin Huang and Ang Li and Aobo Kong and Bin Wang and Binxing Jiao and Bo Dong and Bojun Wang and Boyu Chen and Brian Li and Buyun Ma and Chang Su and Changxin Miao and Changyi Wan and Chao Lou and Chen Hu and Chen Xu and Chenfeng Yu and Chengting Feng and Chengyuan Yao and Chunrui Han and Dan Ma and Dapeng Shi and Daxin Jiang and Dehua Ma and Deshan Sun and Di Qi and Enle Liu and Fajie Zhang and Fanqi Wan and Guanzhe Huang and Gulin Yan and Guoliang Cao and Guopeng Li and Han Cheng and Hangyu Guo and Hanshan Zhang and Hao Nie and Haonan Jia and Haoran Lv and Hebin Zhou and Hekun Lv and Heng Wang and Heung-Yeung Shum and Hongbo Huang and Hongbo Peng and Hongyu Zhou and Hongyuan Wang and Houyong Chen and Huangxi Zhu and Huimin Wu and Huiyong Guo and Jia Wang and Jian Zhou and Jianjian Sun and Jiaoren Wu and Jiaran Zhang and Jiashu Lv and Jiashuo Liu and Jiayi Fu and Jiayu Liu and Jie Cheng and Jie Luo and Jie Yang and Jie Zhou and Jieyi Hou and Jing Bai and Jingcheng Hu and Jingjing Xie and Jingwei Wu and Jingyang Zhang and Jishi Zhou and Junfeng Liu and Junzhe Lin and Ka Man Lo and Kai Liang and Kaibo Liu and Kaijun Tan and Kaiwen Yan and Kaixiang Li and Kang An and Kangheng Lin and Lei Yang and Liang Lv and Liang Zhao and Liangyu Chen and Lieyu Shi and Liguo Tan and Lin Lin and Lina Chen and Luck Ma and Mengqiang Ren and Michael Li and Ming Li and Mingliang Li and Mingming Zhang and Mingrui Chen and Mitt Huang and Na Wang and Peng Liu and Qi Han and Qian Zhao and Qinglin He and Qinxin Du and Qiuping Wu and Quan Sun and Rongqiu Yang and Ruihang Miao and Ruixin Han and Ruosi Wan and Ruyan Guo and Shan Wang and Shaoliang Pang and Shaowen Yang and Shengjie Fan and Shijie Shang and Shiliang Yang and Shiwei Li and Shuangshuang Tian and Siqi Liu and Siye Wu and Siyu Chen and Song Yuan and Tiancheng Cao and Tianchi Yue and Tianhao Cheng and Tianning Li and Tingdan Luo and Wang You and Wei Ji and Wei Yuan and Wei Zhang and Weibo Wu and Weihao Xie and Wen Sun and Wenjin Deng and Wenzhen Zheng and Wuxun Xie and Xiangfeng Wang and Xiangwen Kong and Xiangyu Liu and Xiangyu Zhang and Xiaobo Yang and Xiaojia Liu and Xiaolan Yuan and Xiaoran Jiao and Xiaoxiao Ren and Xiaoyun Zhang and Xin Li and Xin Liu and Xin Wu and Xing Chen and Xingping Yang and Xinran Wang and Xu Zhao and Xuan He and Xuanti Feng and Xuedan Cai and Xuqiang Zhou and Yanbo Yu and Yang Li and Yang Xu and Yanlin Lai and Yanming Xu and Yaoyu Wang and Yeqing Shen and Yibo Zhu and Yichen Lv and Yicheng Cao and Yifeng Gong and Yijing Yang and Yikun Yang and Yin Zhao and Yingxiu Zhao and Yinmin Zhang and Yitong Zhang and Yixuan Zhang and Yiyang Chen and Yongchi Zhao and Yongshen Long and Yongyao Wang and Yousong Guan and Yu Zhou and Yuang Peng and Yuanhao Ding and Yuantao Fan and Yuanzhen Yang and Yuchu Luo and Yudi Zhao and Yue Peng and Yueqiang Lin and Yufan Lu and Yuling Zhao and Yunzhou Ju and Yurong Zhang and Yusheng Li and Yuxiang Yang and Yuyang Chen and Yuzhu Cai and Zejia Weng and Zetao Hong and Zexi Li and Zhe Xie and Zheng Ge and Zheng Gong and Zheng Zeng and Zhenyi Lu and Zhewei Huang and Zhichao Chang and Zhiguo Huang and Zhiheng Hu and Zidong Yang and Zili Wang and Ziqi Ren and Zixin Zhang and Zixuan Wang},
      year={2026},
      eprint={2602.10604},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2602.10604}, 
}
```

## License
This project is open-sourced under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).