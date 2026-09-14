---
license: other
language:
- en
- fr
- de
- es
- pt
- it
- ja
- ko
- ru
- zh
- ar
- fa
- id
- ms
- ne
- pl
- ro
- sr
- sv
- tr
- uk
- vi
- hi
- bn
tags:
- vLLM
---

# Mistral Medium 3.5 128B

Mistral Medium 3.5 is our first flagship merged model. It is a dense 128B model with a 256k context window, handling instruction-following, reasoning,
and coding in a single set of weights. Mistral Medium 3.5 replaces its predecessor Mistral Medium 3.1 and Magistral in Le Chat. It also replaces Devstral 2 in our
coding agent Vibe. Concretely, expect better performance for instruct, reasoning and coding tasks in a new unified model in comparison with our previous released models.

Reasoning effort is configurable per request, so the same model can answer a quick chat reply or work through a complex agentic run. We trained the vision encoder from
scratch to handle variable image sizes and aspect ratios.

Find more information on our [blog](https://mistral.ai/news/vibe-remote-agents-mistral-medium-3-5).

> [!Note]
> To speed up local inference using vLLM or SGLang, check out our released [EAGLE model](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B-EAGLE).

> [!Warning]
> The Transformers config originally had an incorrect entry that caused long-context performance degradation. This has been fixed in this [commit](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B/commit/c4be198050fb5789774a55b92ed697becfbf20ae). GGUFs generated using the Transformers config prior to this commit are also affected. Please use the correct config for best performance.

## Key Features

Mistral Medium 3.5 includes the following architectural choices:

- **Dense 128B parameters**.
- **256k context length**.
- **Multimodal input**: Accepts both text and image input, with text output.
- **Instruct and Reasoning functionalities** with function calls (reasoning effort configurable per request).

Mistral Medium 3.5 offers the following capabilities:

- **Reasoning Mode**: Toggle between fast instant reply mode and reasoning mode, boosting performance with test-time compute when requested.
- **Vision**: Analyzes images and provides insights based on visual content, in addition to text.
- **Multilingual**: Supports dozens of languages, including English, French, Spanish, German, Italian, Portuguese, Dutch, Chinese, Japanese, Korean, and Arabic.
- **System Prompt**: Strong adherence and support for system prompts.
- **Agentic**: Best-in-class agentic capabilities with native function calling and JSON output.
- **Large Context Window**: Supports a 256k context window.

We release this model under a **[Modified MIT License](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B/blob/main/LICENSE)**: Open-source license for both commercial and non-commercial use with exceptions for companies with large revenue.

## Recommended Settings

- **Reasoning Effort**:
  - `'none'` → Do not use reasoning
  - `'high'` → Use reasoning (recommended for complex prompts and agentic usage)
  Use `reasoning_effort="high"` for complex tasks and agentic coding.
- **Temperature**: 0.7 for `reasoning_effort="high"`. Temp between 0.0 and 0.7 for `reasoning_effort="none"` depending on the task.
  Generally, lower means answer that are more to the point and higher allows the model to be more creative. It is a good practice to try different values in order to
  improve the model performance to meet your demands.
- **Top p**: 0.95 for `reasoning_effort="high"`. You can try different values but staying close should achieve best performance. Leave it to `None` (or `1.0`) for `reasoning_effort="none"`.

## Benchmarks

### Agentic Benchmarks

Mistral Medium 3.5 supersedes all our previous coding models, namely Devstral, across all benchmarks. It scores **91.4%** on τ³-Telecom and **77.6%** on SWE-Bench Verified. Due to its stronger agentic capabilities, Mistral Medium 3.5 replaces Devstral 2 in our coding agent, Vibe CLI.

![Mistral agentic benchmark](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B/resolve/main/images/image2.png)
![Mistral agentic benchmark SWE-bench](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B/resolve/main/images/image3.png)
![Mistral agentic vs competiting models benchmark](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B/resolve/main/images/image4.png)

### Instruction Following, Reasoning, and Coding Benchmarks

We compared Mistral Medium 3.5 with competing models on instruction following, reasoning (math), and coding benchmarks. Thanks to its unified capabilities, it achieves strong results across all these tasks and Mistral Medium 3.5 is now powering Le Chat.

![instruct reasoning and agentic benchmark](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B/resolve/main/images/image1.png)

## Usage

You can find Mistral Medium 3.5 support on multiple libraries for inference and fine-tuning.

We here **thank** every contributors and maintainers that helped us making it happen.

### Mistral-Vibe

Use `Mistral Medium 3.5` with [Mistral Vibe](https://github.com/mistralai/mistral-vibe). 

#### Install

Install the latest version:

```sh
uv pip install mistral-vibe --upgrade
```

#### API Usage

Mistral Medium 3.5 can be selected by starting `vibe`. If it is the first time you launch `vibe`, it will:

- Create a default configuration file at ~/.vibe/config.toml.
- Prompt you to enter your API key if it's not already configured.
- Save your API key to ~/.vibe/.env for future use.

Now select `mistral-medium-3.5` and start building !

#### Local server

If instead of pinging the Mistral API, you want to use a local vLLM server, you can do the following:
- 1. Spin up a vllm server as explained in [`Usage - vllm`](#vllm-recommended)
- 2. Add the model configuration in `~/.vibe/config.toml`:
 

```toml
display_name = "Mistral Medium 3.5 (local vLLM)"
description = "Mistral Medium 3.5 mode using local vLLM"
safety = "neutral"

active_model = "mistral-medium-3.5" # Make sure this is the only active_model entry
[[providers]]
name = "vllm"
api_base = "http://<your-host-url>:8000/v1"
api_key_env_var = ""
backend = "generic"
api_style = "reasoning"

[[models]]
name = "mistralai/Mistral-Medium-3.5-128B"
provider = "vllm"
alias = "mistral-medium-3.5"
thinking = "high"
temperature = 0.7
auto_compact_threshold = 168000

[tools.bash]
default_timeout = 1200
```

**Notes**:
- Make sure to overwrite `<your-host-url>` with your server's url.
- Other inference backends are also supported. Please look at [Mistral Vibe repo](https://github.com/mistralai/mistral-vibe) for more info.

Then restart `vibe` and "tab-shift" to "mistral-medium-3.5" mode.

Give it a try on some coding agentic tasks and start building some cool stuff !

### Inference

The model can be deployed with:
- [`vllm (recommended)`](https://github.com/vllm-project/vllm): See [here](#vllm-recommended).
- [`llama.cpp`](https://github.com/ggml-org/llama.cpp): See [here](https://huggingface.co/unsloth/Mistral-Medium-3.5-128B-GGUF) for Unsloth's GGUFs.
- [`LM studio`](https://lmstudio.ai/): WIP stay tuned !
- [`Ollama`](https://ollama.com//): See [here](https://ollama.com/library/mistral-medium-3.5).
- [`SGLang`](https://github.com/sgl-project/sglang): See [here](#sglang).
- [`transformers`](https://github.com/huggingface/transformers): See [here](#transformers).

> [!Note]
> For optimal performance, we recommend using the Mistral AI API if local serving is subpar.

> [!Warning]
> Make sure that frameworks relying on the Transformers configuration, including GGUF files, are up to date with the fixes introduced in this [commit](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B/commit/c4be198050fb5789774a55b92ed697becfbf20ae). Otherwise, you will experience subpar performance, especially in long-context sessions.

### Fine-Tuning

Fine-tune the model via:
- [`Axolotl`](https://github.com/axolotl-ai-cloud/axolotl): See [here](https://docs.axolotl.ai/docs/models/mistral-medium-3_5.html).
- [`Unsloth`](https://unsloth.ai/): See [here](https://unsloth.ai/docs/models/mistral-3.5).

## vLLM (Recommended)

We recommend using Mistral Medium 3.5 with the [vLLM library](https://github.com/vllm-project/vllm) for production-ready inference.

> [!Note]
> To speed up local inference using vLLM, check out our released [EAGLE model](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B-EAGLE)

### Installation

Make sure to install **vllm nightly**:

```
uv pip install -U vllm \
   --torch-backend=auto \
   --extra-index-url https://wheels.vllm.ai/nightly
```

Doing so should automatically install [`mistral_common >= 1.11.1`](https://github.com/mistralai/mistral-common/releases/tag/v1.11.0) and `transformers >= 5.4.0`.
  
To check:
```
python -c "import mistral_common; print(mistral_common.__version__)"
python -c "import transformers; print(transformers.__version__)"
```
  
You can also make use of a ready-to-go [docker image](https://github.com/vllm-project/vllm/blob/main/docker/Dockerfile) or on the [docker hub](https://hub.docker.com/layers/vllm/vllm-openai/nightly).

### Serve the Model

We recommend a server/client setup:

```bash
vllm serve mistralai/Mistral-Medium-3.5-128B --tensor-parallel-size 8 \
  --tool-call-parser mistral --enable-auto-tool-choice --reasoning-parser mistral --max_num_batched_tokens 16384 --max_num_seqs 128 \
  --gpu_memory_utilization 0.8
```

### Ping the Server

<details>
  <summary>Instruction Following</summary>

Mistral Medium 3.5 can follow your instructions to the letter.


```python
from datetime import datetime, timedelta

from huggingface_hub import hf_hub_download
from openai import OpenAI

# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

REASONING_EFFORT = "none" # Toggle reasoning with 'high'.

match REASONING_EFFORT:
    case "none":
        TEMP = 0.1
        TOP_P = None
    case "high":
        TEMP = 0.7
        TOP_P = 0.95
    case _:
        raise ValueError("Only REASONING_EFFORT in ['none', 'high'] are supported.")

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

models = client.models.list()
model = models.data[0].id


def load_system_prompt(repo_id: str, filename: str) -> str:
    file_path = hf_hub_download(repo_id=repo_id, filename=filename)
    with open(file_path, "r") as file:
        system_prompt = file.read()
    today = datetime.today().strftime("%Y-%m-%d")
    yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    model_name = repo_id.split("/")[-1]
    return system_prompt.format(name=model_name, today=today, yesterday=yesterday)


SYSTEM_PROMPT = load_system_prompt(model, "SYSTEM_PROMPT.txt")

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {
        "role": "user",
        "content": "Write me a sentence where every word starts with the next letter in the alphabet - start with 'a' and end with 'z'.",
    },
]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    reasoning_effort=REASONING_EFFORT,
    temperature=TEMP,
    top_p=TOP_P,
)

print("==============================================================")
print(f"Request with {REASONING_EFFORT=}, {TEMP=} and {TOP_P=}.")
print("==============================================================")
print("REASONING")
print("~~~~~~~~~")
print(response.choices[0].message.reasoning)
print("==============================================================")
print("CONTENT")
print("~~~~~~~")
print(response.choices[0].message.content)
```

</details>

<details>
  <summary>Tool Call</summary>

Let's solve some equations thanks to our simple Python calculator tool.


```python
import json
from datetime import datetime, timedelta

from openai import OpenAI
from huggingface_hub import hf_hub_download

# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

REASONING_EFFORT = "none" # Toggle reasoning with 'high'.

match REASONING_EFFORT:
    case "none":
        TEMP = 0.1
        TOP_P = None
    case "high":
        TEMP = 0.7
        TOP_P = 0.95
    case _:
        raise ValueError("Only REASONING_EFFORT in ['none', 'high'] are supported.")

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

models = client.models.list()
model = models.data[0].id


def load_system_prompt(repo_id: str, filename: str) -> str:
    file_path = hf_hub_download(repo_id=repo_id, filename=filename)
    with open(file_path, "r") as file:
        system_prompt = file.read()
    today = datetime.today().strftime("%Y-%m-%d")
    yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    model_name = repo_id.split("/")[-1]
    return system_prompt.format(name=model_name, today=today, yesterday=yesterday)


SYSTEM_PROMPT = load_system_prompt(model, "SYSTEM_PROMPT.txt")

image_url = "https://math-coaching.com/img/fiche/46/expressions-mathematiques.jpg"


def my_calculator(expression: str) -> str:
    return str(eval(expression))


tools = [
    {
        "type": "function",
        "function": {
            "name": "my_calculator",
            "description": "A calculator that can evaluate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to evaluate.",
                    },
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "rewrite",
            "description": "Rewrite a given text for improved clarity",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The input text to rewrite",
                    }
                },
            },
        },
    },
]

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Thanks to your calculator, compute the results for the equations that involve numbers displayed in the image.",
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": image_url,
                },
            },
        ],
    },
]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    tools=tools,
    tool_choice="auto",
    reasoning_effort=REASONING_EFFORT,
    temperature=TEMP,
    top_p=TOP_P,
)

tool_calls = response.choices[0].message.tool_calls

results = []
for tool_call in tool_calls:
    function_name = tool_call.function.name
    function_args = tool_call.function.arguments
    if function_name == "my_calculator":
        result = my_calculator(**json.loads(function_args))
        results.append(result)

messages.append({"role": "assistant", "tool_calls": tool_calls})
for tool_call, result in zip(tool_calls, results):
    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": tool_call.function.name,
            "content": result,
        }
    )


response = client.chat.completions.create(
    model=model,
    messages=messages,
    reasoning_effort=REASONING_EFFORT,
    temperature=TEMP,
    top_p=TOP_P,
)

print("==============================================================")
print(f"Request with {REASONING_EFFORT=}, {TEMP=} and {TOP_P=}.")
print("==============================================================")
print("REASONING")
print("~~~~~~~~~")
print(response.choices[0].message.reasoning)
print("==============================================================")
print("CONTENT")
print("~~~~~~~")
print(response.choices[0].message.content)
```

</details>

<details>
  <summary>Vision Reasoning</summary>

Let's see if the Mistral Medium 3.5 knows when to pick a fight !

```python
from datetime import datetime, timedelta

from openai import OpenAI
from huggingface_hub import hf_hub_download

# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

REASONING_EFFORT = "high" # Remove reasoning with 'none'.

match REASONING_EFFORT:
    case "none":
        TEMP = 0.1
        TOP_P = None
    case "high":
        TEMP = 0.7
        TOP_P = 0.95
    case _:
        raise ValueError("Only REASONING_EFFORT in ['none', 'high'] are supported.")

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

models = client.models.list()
model = models.data[0].id


def load_system_prompt(repo_id: str, filename: str) -> str:
    file_path = hf_hub_download(repo_id=repo_id, filename=filename)
    with open(file_path, "r") as file:
        system_prompt = file.read()
    today = datetime.today().strftime("%Y-%m-%d")
    yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    model_name = repo_id.split("/")[-1]
    return system_prompt.format(name=model_name, today=today, yesterday=yesterday)


SYSTEM_PROMPT = load_system_prompt(model, "SYSTEM_PROMPT.txt")
image_url = "https://static.wikia.nocookie.net/essentialsdocs/images/7/70/Battle.png/revision/latest?cb=20220523172438"

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What action do you think I should take in this situation? List all the possible actions and explain why you think they are good or bad.",
            },
            {"type": "image_url", "image_url": {"url": image_url}},
        ],
    },
]


response = client.chat.completions.create(
    model=model,
    messages=messages,
    reasoning_effort=REASONING_EFFORT,
    temperature=TEMP,
    top_p=TOP_P,
)

print("==============================================================")
print(f"Request with {REASONING_EFFORT=}, {TEMP=} and {TOP_P=}.")
print("==============================================================")
print("REASONING")
print("~~~~~~~~~")
print(response.choices[0].message.reasoning)
print("==============================================================")
print("CONTENT")
print("~~~~~~~")
print(response.choices[0].message.content)
```

</details>

## SGLang

Serve Mistral Medium 3.5 with the [SGLang library](https://github.com/sgl-project/sglang) for production-ready inference.

> [!Note]
> To speed up local inference using SGLang, check out our released [EAGLE model](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B-EAGLE).

### Installation

Day-zero support ships in dedicated docker tags:

```
docker pull lmsysorg/sglang:dev-mistral-medium-3.5         # H100 / H200 (Hopper, CUDA 12.9)
docker pull lmsysorg/sglang:dev-cu13-mistral-medium-3.5    # B200 / B300 (Blackwell, CUDA 13.0)
```

Or follow the [SGLang installation guide](https://docs.sglang.io/docs/get-started/install). Requires `transformers >= 5.4.0`.

### Serve the Model

```bash
python -m sglang.launch_server --model-path mistralai/Mistral-Medium-3.5-128B \
  --tp 8 --tool-call-parser mistral --reasoning-parser mistral
```

For the full deployment guide, benchmarks, and per-request examples (reasoning effort, tool calls, vision, streaming), see the [SGLang cookbook entry for Mistral Medium 3.5](https://docs.sglang.io/cookbook/autoregressive/Mistral/Mistral-Medium-3.5).

## Transformers

### Installation

First install the [Transformers framework](https://github.com/huggingface/transformers/) to use Mistral Medium 3.5:

```bash
uv pip install transformers
```

### Inference

<details>
<summary>Python Inference Snippet</summary>

```python
import torch
from transformers import AutoProcessor, Mistral3ForConditionalGeneration


REASONING_EFFORT = "high" # Remove reasoning with 'none'.

match REASONING_EFFORT:
    case "none":
        TEMP = 0.1
        TOP_P = 1.0
    case "high":
        TEMP = 0.7
        TOP_P = 0.95
    case _:
        raise ValueError("Only REASONING_EFFORT in ['none', 'high'] are supported.")

model_id = "mistralai/Mistral-Medium-3.5-128B"

processor = AutoProcessor.from_pretrained(model_id)
model = Mistral3ForConditionalGeneration.from_pretrained(
    model_id, device_map="auto"
)

image_url = "https://static.wikia.nocookie.net/essentialsdocs/images/7/70/Battle.png/revision/latest?cb=20220523172438"

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What action do you think I should take in this situation? List all the possible actions and explain why you think they are good or bad.",
            },
            {"type": "image_url", "image_url": {"url": image_url}},
        ],
    },
]


inputs = processor.apply_chat_template(messages, return_tensors="pt", tokenize=True, return_dict=True, reasoning_effort=REASONING_EFFORT)
inputs = inputs.to(model.device)

output = model.generate(
    **inputs,
    max_new_tokens=1024,
    do_sample=True,
    temperature=TEMP,
    top_p=TOP_P,
)[0]

# Setting `skip_special_tokens=False` to visualize reasoning trace between [THINK] [/THINK] tags.
decoded_output = processor.decode(output[len(inputs["input_ids"][0]):], skip_special_tokens=False) 
print(decoded_output)
```
</details>


## License

This model is licensed under a [Modified MIT License](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B/blob/main/LICENSE).

*You must not use this model in a manner that infringes, misappropriates, or otherwise violates any third party’s rights, including intellectual property rights.*