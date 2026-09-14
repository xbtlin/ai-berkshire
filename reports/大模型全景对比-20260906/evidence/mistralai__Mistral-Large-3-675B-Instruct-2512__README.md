---
library_name: vllm
language:
- en
- fr
- es
- de
- it
- pt
- nl
- zh
- ja
- ko
- ar
license: apache-2.0
inference: false
extra_gated_description: >-
  If you want to learn more about how we process your personal data, please read
  our <a href="https://mistral.ai/terms/">Privacy Policy</a>.
base_model:
- mistralai/Mistral-Large-3-675B-Base-2512
tags:
- mistral-common
- compressed-tensors
---

# Mistral Large 3 675B Instruct 2512
From our family of large models, **Mistral Large 3** is a state-of-the-art general-purpose **Multimodal granular Mixture-of-Experts** model with **41B active parameters** and **675B total parameters** trained from the ground up with 3000 H200s.

This model is the instruct post-trained version in **FP8**, fine-tuned for instruction tasks, making it ideal for chat, agentic and instruction based use cases.  
Designed for reliability and long-context comprehension - It is engineered for production-grade assistants, retrieval-augmented systems, scientific workloads, and complex enterprise workflows.

Learn more in our blog post [here](https://mistral.ai/news/mistral-3).

Mistral Large 3 is deployable on-premises in:
- **FP8** on a single node of B200s or H200s.
- [NVFP4](https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512-NVFP4) on a single node of H100s or A100s.

We provide a [BF16](https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512-BF16) version if needed.

## Key Features
Mistral Large 3 consists of two main architectural components:
- **A Granular MoE Language Model with 673B params and 39B active**
- **A 2.5B Vision Encoder**

The Mistral Large 3 Instruct model offers the following capabilities:
- **Vision**: Enables the model to analyze images and provide insights based on visual content, in addition to text.
- **Multilingual**: Supports dozens of languages, including English, French, Spanish, German, Italian, Portuguese, Dutch, Chinese, Japanese, Korean, Arabic.
- **System Prompt**: Maintains strong adherence and support for system prompts.
- **Agentic**: Offers best-in-class agentic capabilities with native function calling and JSON outputting.
- **Frontier**: Delivers best-in-class performance.
- **Apache 2.0 License**: Open-source license allowing usage and modification for both commercial and non-commercial purposes.
- **Large Context Window**: Supports a 256k context window.

## Use Cases
With powerful long-context performance, stable and consistent cross-domain behavior, Mistral Large 3 is perfect for:
- Long Document Understanding
- Powerful Daily-Driver AI Assistants
- State-of-the-Art Agentic and Tool-Use Capabilities
- Enterprise Knowledge Work
- General Coding Assistant

And enterprise-grade use cases requiring frontier capabilities.

## Recommended Settings

We recommend deploying Large 3 in a client-server configuration with the following best practices:

- **System Prompt**: Define a clear environment and use case, including guidance on how to effectively leverage tools in agentic systems.
- **Sampling Parameters**: Use a temperature below 0.1 for daily-driver and production environments ; Higher temperatures may be explored for creative use cases - developers are encouraged to experiment with alternative settings.
- **Tools**: Keep the set of tools well-defined and limit their number to the minimum required for the use case - Avoiding overloading the model with an excessive number of tools.
- **Vision**: When deploying with vision capabilities, we recommend maintaining an aspect ratio close to 1:1 (width-to-height) for images. Avoiding the use of overly thin or wide images - crop them as needed to ensure optimal performance.

### Known Issues / Limitations

- **Not a dedicated reasoning model**: Dedicated reasoning models can outperform Mistral Large 3 in strict reasoning use cases.
- **Behind vision-first models in multimodal tasks**: Mistral Large 3 can lag behind models optimized for vision tasks and use cases.
- **Complex deployment**: Due to its large size and architecture, the model can be challenging to deploy efficiently with constrained resources or at scale.

## Benchmark Results

We compare Mistral Large 3 to similar sized models.

![image](https://cdn-uploads.huggingface.co/production/uploads/64161701107962562e9b1006/IrPlvUUD-5-Phwi9QSevh.png)

![image](https://cdn-uploads.huggingface.co/production/uploads/64161701107962562e9b1006/fDFEymz4HZNsqFARB4u9Y.png)

![image](https://cdn-uploads.huggingface.co/production/uploads/64161701107962562e9b1006/eMdaAPcjOo8VyoGyFKxrE.png)

## Usage

The model can be used with the following frameworks;
- [`vllm`](https://github.com/vllm-project/vllm): See [here](#vllm)

> [!Note]
> We sadly didn't have enough time to add Mistral Large 3 to transformers, but we would be very happy for a community contribution by opening a PR to [huggingface/transformers](https://github.com/huggingface/transformers).

### vLLM

We recommend using this model with [vLLM](https://github.com/vllm-project/vllm).

#### Installation

Make sure to install **vllm >= 1.12.0**:

```
pip install vllm --upgrade
```

Doing so should automatically install [`mistral_common >= 1.8.6`](https://github.com/mistralai/mistral-common/releases/tag/v1.8.6).

To check:
```
python -c "import mistral_common; print(mistral_common.__version__)"
```

You can also make use of a ready-to-go [docker image](https://github.com/vllm-project/vllm/blob/main/docker/Dockerfile) or on the [docker hub](https://hub.docker.com/layers/vllm/vllm-openai/latest).

#### Serve

The Mistral Large 3 Instruct FP8 format can be used on one 8xH200 node. We recommend to use this format if you plan to fine-tuning as it can be more precise than NVFP4 in some situations.

**Simple**

A simple launch command is:

```bash
vllm serve mistralai/Mistral-Large-3-675B-Instruct-2512 \
  --max-model-len 262144 --tensor-parallel-size 8 \
  --tokenizer_mode mistral --config_format mistral --load_format mistral \
  --enable-auto-tool-choice --tool-call-parser mistral
```

Key parameter notes:

* enable-auto-tool-choice: Required when enabling tool usage.
* tool-call-parser mistral: Required when enabling tool usage.


Additional flags:

* You can set `--max-model-len` to preserve memory. By default it is set to `262144` which is quite large but not necessary for most scenarios.
* You can set `--max-num-batched-tokens` to balance throughput and latency, higher means higher throughput but higher latency.

**Accelerated with speculative decoding**

For maximum performance we recommend serving the checkpoint with its customized draft model [Mistral-Large-3-675B-Instruct-2512-Eagle](https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512-Eagle):

```bash
vllm serve mistralai/Mistral-Large-3-675B-Instruct-2512 \
  --tensor-parallel-size 8 \
  --load-format mistral \
  --tokenizer-mode mistral \
  --config-format mistral \
  --enable-auto-tool-choice \
  --tool-call-parser mistral \
  --limit-mm-per-prompt '{"image": 10}' \
  --speculative_config '{
    "model": "mistralai/Mistral-Large-3-675B-Instruct-2512-Eagle",
    "num_speculative_tokens": 3,
    "method": "eagle",
    "max_model_len": "16384"
  }'
```

For more information on the draft model, please have a look at [Mistral-Large-3-675B-Instruct-2512-Eagle](https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512-Eagle).


#### Usage of the model

Here we asumme that the model `mistralai/Mistral-Large-3-675B-Instruct-2512` is served and you can ping it to the domain `localhost` with the port `8000` which is the default for vLLM.

<details>
  <summary>Vision Reasoning</summary>

Let's see if Mistral Large 3 knows when to pick a fight !

```python
from datetime import datetime, timedelta

from openai import OpenAI
from huggingface_hub import hf_hub_download

# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

TEMP = 0.15
MAX_TOK = 262144

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
    temperature=TEMP,
    max_tokens=MAX_TOK,
)

print(response.choices[0].message.content)
```
</details>

<details>
  <summary>Function Calling</summary>

Let's solve some equations thanks to our simple Python calculator tool.

```python
import json
from openai import OpenAI
from huggingface_hub import hf_hub_download

# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

TEMP = 0.15
MAX_TOK = 262144

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
    return system_prompt


SYSTEM_PROMPT = load_system_prompt(model, "SYSTEM_PROMPT.txt")

image_url = "https://math-coaching.com/img/fiche/46/expressions-mathematiques.jpg"


def my_calculator(expression: str) -> str:
    return str(eval(expression))


tools = [
    {
        "type": "function",
        "function": {
            "name": "my_calculator",
            "description": "A calculator that can evaluate a mathematical equation and compute its results.",
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
    temperature=TEMP,
    max_tokens=MAX_TOK,
    tools=tools,
    tool_choice="auto",
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
    temperature=TEMP,
    max_tokens=MAX_TOK,
)

print(response.choices[0].message.content)
```

</details>

<details>
  <summary>Text-Only Request</summary>

Mistral Large 3 can follow your instructions down to the letter.

```python
from openai import OpenAI
from huggingface_hub import hf_hub_download

# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

TEMP = 0.15
MAX_TOK = 262144

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
    return system_prompt


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
    temperature=TEMP,
    max_tokens=MAX_TOK,
)

assistant_message = response.choices[0].message.content
print(assistant_message)
```

</details>

## License

This model is licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0.txt).

*You must not use this model in a manner that infringes, misappropriates, or otherwise violates any third party’s rights, including intellectual property rights.*