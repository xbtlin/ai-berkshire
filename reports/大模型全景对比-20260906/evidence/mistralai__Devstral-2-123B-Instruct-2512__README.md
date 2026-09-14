---
library_name: vllm
inference: false
extra_gated_description: >-
  If you want to learn more about how we process your personal data, please read
  our <a href="https://mistral.ai/terms/">Privacy Policy</a>.
tags:
- mistral-common
license: other
---

# Devstral 2 123B Instruct 2512
Devstral is an agentic LLM for software engineering tasks. **Devstral 2** excels at using tools to explore codebases, editing multiple files and power software engineering agents.  
The model achieves remarkable performance on SWE-bench. 

This model is an Instruct model in **FP8**, fine-tuned to follow instructions, making it ideal for chat, agentic and instruction based tasks for SWE use cases.

For enterprises requiring specialized capabilities (increased context, domain-specific knowledge, etc.), we invite companies to [reach out to us](https://mistral.ai/contact).

## Key Features
The Devstral 2 Instruct model offers the following capabilities:
- **Agentic Coding**: Devstral is designed to excel at agentic coding tasks, making it a great choice for software engineering agents.
- **Improved Performance**: Devstral 2 is a step-up compared to its predecessors.
- **Better Generalization**: Generalises better to diverse prompts and coding environments.
- **Context Window**: A 256k context window.

### Use Cases

AI Code Assistants, Agentic Coding, and Software Engineering Tasks. Leveraging advanced AI capabilities for complex tool integration and deep codebase understanding in coding environments.

## Benchmark Results

| Model/Benchmark               | Size (B Parameters) | SWE Bench Verified | SWE Bench Multilingual | Terminal Bench 2 |
|-------------------------------|-----------------|--------------------|------------------------|------------------|
| **Devstral 2**                | 123             | 72.2%              | 61.3%                  | 32.6%            |
| **Devstral Small 2**          | 24              | 68.0%              | 55.7%                  | 22.5%            |
|                               |                 |                    |                        |                  |
| GLM 4.6                       | 355             | 68.0%              | --                     | 24.6%            |
| Qwen 3 Coder Plus             | 480             | 69.6%              | 54.7%                  | 25.4%            |
| MiniMax M2                    | 230             | 69.4%              | 56.5%                  | 30.0%            |
| Kimi K2 Thinking              | 1000            | 71.3%              | 61.1%                  | 35.7%            |
| DeepSeek v3.2                 | 671             | 73.1%              | 70.2%                  | 46.4%            |
|                               |                 |                    |                        |                  |
| GPT 5.1 Codex High            | --              | 73.7%              | --                     | 52.8%            |
| GPT 5.1 Codex Max             | --              | 77.9%              | --                     | 60.4%            |
| Gemini 3 Pro                  | --              | 76.2%              | --                     | 54.2%            |
| Claude Sonnet 4.5             | --              | 77.2%              | 68.0%                  | 42.8%            |

*Benchmark results presented are based on publicly reported values for competitor models.

## Usage

### Scaffolding

Together with Devstral 2, we are releasing **Mistral Vibe**, a CLI tool allowing developers to leverage Devstral capabilities directly in your terminal.
- [Mistral Vibe (recommended)](https://github.com/mistralai/mistral-vibe): Learn how to use it [here](#mistral-vibe)

Devstral 2 can also be used with the following scaffoldings:
- [Cline](https://github.com/cline/cline)
- [Kilo Code](https://github.com/Kilo-Org/kilocode)
- [Claude Code](https://github.com/anthropics/claude-code)
- [OpenHands](https://github.com/All-Hands-AI/OpenHands/tree/main)
- [SWE Agent](https://github.com/SWE-agent/SWE-agent)

You can use Devstral 2 either through our API or by running locally.

#### Mistral Vibe

The [Mistral Vibe CLI](https://github.com/mistralai/mistral-vibe) is a command-line tool designed to help developers leverage Devstral’s capabilities directly from their terminal.

We recommend installing Mistral Vibe using `uv` for faster and more reliable dependency management:
```
uv tool install mistral-vibe
```
You can also run:
```
curl -LsSf https://mistral.ai/vibe/install.sh | sh
```

If you prefer using pip, use:
```
pip install mistral-vibe
```

To launch the CLI, navigate to your project's root directory and simply execute:
```
vibe
```

If this is your first time running Vibe, it will:
- Create a default configuration file at `~/.vibe/config.toml`.
- Prompt you to enter your API key if it's not already configured, follow these [instructions](https://docs.mistral.ai/getting-started/quickstart/#account-setup) to create an Account and get an API key.
- Save your API key to `~/.vibe/.env` for future use.

### Local Deployment

The model can also be deployed with the following libraries, we advise everyone to use the Mistral AI API if the model is subpar with local serving:
- [`vllm (recommended)`](https://github.com/vllm-project/vllm): See [here](#vllm-recommended)
- [`sglang`](https://github.com/sgl-project/sglang): See [here](#sglang)
- [`transformers`](https://github.com/huggingface/transformers): See [here](#transformers)

We're thankful to the llama.cpp team and their community as well as the LM Studio and Ollama teams that worked hard to make these models also available for their frameworks.

You can now also run Devstral using these (alphabetical ordered) frameworks:
- [`llama.cpp`](https://github.com/ggml-org/llama.cpp): To use community ones such as [Unsloth's](https://huggingface.co/unsloth/Devstral-2-123B-Instruct-2512-GGUF) or [Bartowski's](https://huggingface.co/bartowski/mistralai_Devstral-2-123B-Instruct-2512-GGUF) make sure to use changes from this [PR](https://github.com/ggml-org/llama.cpp/pull/17945).
- [`Ollama`](https://ollama.com/): https://ollama.com/library/devstral-2

If you notice subpar performance with local serving, please submit issues to the relevant framework so that it can be fixed and in the meantime we advise to use the Mistral AI API.

#### vLLM (recommended)

<details>
<summary>Expand</summary

We recommend using this model with the [vLLM library](https://github.com/vllm-project/vllm)
to implement production-ready inference pipelines.

**_Installation_**

Please make sure to install latest vLLM:

```
uv pip install -U vllm
```

Alternatively you can also directly use the latest docker image [vllm/vllm-openai:latest](https://hub.docker.com/layers/vllm/vllm-openai/latest/):

```
docker pull vllm/vllm-openai:latest
docker run -it vllm/vllm-openai:latest
```

Also make sure to have installed [`mistral_common >= 1.8.6`](https://github.com/mistralai/mistral-common/releases/tag/v1.8.6).
To check:
```
python -c "import mistral_common; print(mistral_common.__version__)"
```

**_Launch server_**

We recommand that you use Devstral in a server/client setting. 

1. Spin up a server:

```
vllm serve mistralai/Devstral-2-123B-Instruct-2512 \
    --tool-call-parser mistral --enable-auto-tool-choice \
    --tensor-parallel-size 8
```


2. To ping the client you can use a simple Python snippet.

```py
import requests
import json
from huggingface_hub import hf_hub_download


url = "http://<your-server-url>:8000/v1/chat/completions"
headers = {"Content-Type": "application/json", "Authorization": "Bearer token"}

model = "mistralai/Devstral-2-123B-Instruct-2512"

def load_system_prompt(repo_id: str, filename: str) -> str:
    file_path = hf_hub_download(repo_id=repo_id, filename=filename)
    with open(file_path, "r") as file:
        system_prompt = file.read()
    return system_prompt

SYSTEM_PROMPT = load_system_prompt(model, "CHAT_SYSTEM_PROMPT.txt")

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "<your-command>",
            },
        ],
    },
]

data = {"model": model, "messages": messages, "temperature": 0.15}

# Devstral 2 supports tool calling. If you want to use tools, follow this:
# tools = [ # Define tools for vLLM
#     {
#         "type": "function",
#         "function": {
#             "name": "git_clone",
#             "description": "Clone a git repository",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "url": {
#                         "type": "string",
#                         "description": "The url of the git repository",
#                     },
#                 },
#                 "required": ["url"],
#             },
#         },
#     }
# ] 
# data = {"model": model, "messages": messages, "temperature": 0.15, "tools": tools} # Pass tools to payload.

response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.json()["choices"][0]["message"]["content"])
```
</details>

#### SGLang

<details>
<summary>Expand</summary>

To use this model with [SGLang](https://github.com/sgl-project/sglang) to implement a production-ready inference pipelines (OpenAI-compatible API server),
see the following sections.

**_Installation_**

Install SGLang from source (track latest `main` locally):

```
git clone https://github.com/sgl-project/sglang.git
cd sglang
uv pip install -e python
uv pip install transformers==5.0.0rc # required
```

**_Launch server_**

We recommend that you use Devstral in a server/client setting.

1. Spin up a server:

```
python -m sglang.launch_server --model-path mistralai/Devstral-2-123B-Instruct-2512 --host 0.0.0.0 --port 30000 --tp 8 --tool-call-parser mistral
```


2. To ping the client you can use a simple Python snippet.

```py
import requests
import json
from huggingface_hub import hf_hub_download


url = "http://<your-server-url>:30000/v1/chat/completions"
headers = {"Content-Type": "application/json", "Authorization": "Bearer token"}

model = "mistralai/Devstral-2-123B-Instruct-2512"

def load_system_prompt(repo_id: str, filename: str) -> str:
    file_path = hf_hub_download(repo_id=repo_id, filename=filename)
    with open(file_path, "r") as file:
        system_prompt = file.read()
    return system_prompt

SYSTEM_PROMPT = load_system_prompt(model, "CHAT_SYSTEM_PROMPT.txt")

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "<your-command>",
            },
        ],
    },
]

data = {"model": model, "messages": messages, "temperature": 0.15}

# Devstral 2 supports tool calling. If you want to use tools, follow this:
# tools = [  # Define tools (OpenAI-compatible)
#     {
#         "type": "function",
#         "function": {
#             "name": "git_clone",
#             "description": "Clone a git repository",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "url": {
#                         "type": "string",
#                         "description": "The url of the git repository",
#                     },
#                 },
#                 "required": ["url"],
#             },
#         },
#     }
# ] 
# data = {"model": model, "messages": messages, "temperature": 0.15, "tools": tools} # Pass tools to payload.

response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.json()["choices"][0]["message"]["content"])
```
</details>

#### Transformers

<details>
<summary>Expand</summary

Make sure to install from main:

```sh
uv pip install git+https://github.com/huggingface/transformers
```

And run the following code snippet:

```python
from transformers import (
    MistralForCausalLM,
    MistralCommonBackend,
)

model_id = "mistralai/Devstral-2-123B-Instruct-2512"

tokenizer = MistralCommonBackend.from_pretrained(model_id)
model = MistralForCausalLM.from_pretrained(model_id, device_map="auto")

SP = """You are operating as and within Mistral Vibe, a CLI coding-agent built by Mistral AI and powered by default by the Devstral family of models. It wraps Mistral's Devstral models to enable natural language interaction with a local codebase. Use the available tools when helpful.

You can:

- Receive user prompts, project context, and files.
- Send responses and emit function calls (e.g., shell commands, code edits).
- Apply patches, run commands, based on user approvals.

Answer the user's request using the relevant tool(s), if they are available. Check that all the required parameters for each tool call are provided or can reasonably be inferred from context. IF there are no relevant tools or there are missing values for required parameters, ask the user to supply these values; otherwise proceed with the tool calls. If the user provides a specific value for a parameter (for example provided in quotes), make sure to use that value EXACTLY. DO NOT make up values for or ask about optional parameters. Carefully analyze descriptive terms in the request as they may indicate required parameter values that should be included even if not explicitly quoted.

Always try your hardest to use the tools to answer the user's request. If you can't use the tools, explain why and ask the user for more information.

Act as an agentic assistant, if a user asks for a long task, break it down and do it step by step.

When you want to commit changes, you will always use the 'git commit' bash command. It will always be suffixed with a line telling it was generated by Mistral Vibe with the appropriate co-authoring information. The format you will always use is the following heredoc.

```bash
git commit -m "<Commit message here>

Generated by Mistral Vibe.
Co-Authored-By: Mistral Vibe <vibe@mistral.ai>"
```"""

input = {
    "messages": [
        {
            "role": "system",
            "content": SP,
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Can you implement in Python a method to compute the fibonnaci sequence at the `n`th element with `n` a parameter passed to the function ? You should start the sequence from 1, previous values are invalid.\nThen run the Python code for the function for n=5 and give the answer.",
                }
            ],
        },
    ],
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "add_number",
                "description": "Add two numbers.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "string", "description": "The first number."},
                        "b": {"type": "string", "description": "The second number."},
                    },
                    "required": ["a", "b"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "multiply_number",
                "description": "Multiply two numbers.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "string", "description": "The first number."},
                        "b": {"type": "string", "description": "The second number."},
                    },
                    "required": ["a", "b"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "substract_number",
                "description": "Substract two numbers.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "string", "description": "The first number."},
                        "b": {"type": "string", "description": "The second number."},
                    },
                    "required": ["a", "b"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "write_a_story",
                "description": "Write a story about science fiction and people with badass laser sabers.",
                "parameters": {},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "terminal",
                "description": "Perform operations from the terminal.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "The command you wish to launch, e.g `ls`, `rm`, ...",
                        },
                        "args": {
                            "type": "string",
                            "description": "The arguments to pass to the command.",
                        },
                    },
                    "required": ["command"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "python",
                "description": "Call a Python interpreter with some Python code that will be ran.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "The Python code to run",
                        },
                        "result_variable": {
                            "type": "string",
                            "description": "Variable containing the result you'd like to retrieve from the execution.",
                        },
                    },
                    "required": ["code", "result_variable"],
                },
            },
        },
    ],
}

tokenized = tokenizer.apply_chat_template(
    conversation=input["messages"],
    tools=input["tools"],
    return_tensors="pt",
    return_dict=True,
)

input_ids = tokenized["input_ids"].to(device="cuda")

output = model.generate(
    input_ids,
    max_new_tokens=200,
    do_sample=True,
    temperature=0.15,
)[0]

decoded_output = tokenizer.decode(output[len(tokenized["input_ids"][0]) :])
print(decoded_output)
```

</details>

## Tests

To help test our model via vLLM or test that other frameworks' implementations are correct, here is a set of prompts you can try with the expected outputs.

1. Call one tool 

<details>
  <summary>Messages and tools</summary>

```python
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Could you write me a story ?",
            },
        ],
    },
]
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_number",
            "description": "Add two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "string",
                        "description": "The first number.",
                    },
                    "b": {
                        "type": "string",
                        "description": "The second number.",
                    },
                },
                "required": ["a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "multiply_number",
            "description": "Multiply two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "string",
                        "description": "The first number.",
                    },
                    "b": {
                        "type": "string",
                        "description": "The second number.",
                    },
                },
                "required": ["a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "substract_number",
            "description": "Substract two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "string",
                        "description": "The first number.",
                    },
                    "b": {
                        "type": "string",
                        "description": "The second number.",
                    },
                },
                "required": ["a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_a_story",
            "description": "Write a story about science fiction and people with badass laser sabers.",
            "parameters": {},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "terminal",
            "description": "Perform operations from the terminal.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command you wish to launch, e.g `ls`, `rm`, ...",
                    },
                    "args": {
                        "type": "string",
                        "description": "The arguments to pass to the command.",
                    },
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "python",
            "description": "Call a Python interpreter with some Python code that will be ran.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The Python code to run",
                    },
                    "result_variable": {
                        "type": "string",
                        "description": "Variable containing the result you'd like to retrieve from the execution.",
                    },
                },
                "required": ["code", "result_variable"],
            },
        },
    },
]
```

</details>

<details>
  <summary>Expected output trace</summary>

```json
[
    {
      "role": "assistant",
      "tool_calls": [
        {
          "id": "chatcmpl-tool-8a1f267a212e66e5",
          "function": {
            "arguments": "{}",
            "name": "write_a_story"
          },
          "type": "function"
        }
      ],
      "content": null
    },
    {
      "role": "tool",
      "tool_call_id": "chatcmpl-tool-8a1f267a212e66e5",
      "name": "write_a_story",
      "content": "A long time ago in a galaxy far, far away..."
    },
    {
      "role": "assistant",
      "tool_calls": [],
      "content": "A long time ago in a galaxy far, far away, there was a planet called Eldoria, known for its breathtaking landscapes and advanced civilization. The people of Eldoria were not just ordinary beings; they were warriors, scientists, and dreamers, all wielding the power of laser sabers.\n\nAmong them was a young warrior named Kael. Kael was not like the others. While his peers trained rigorously to master the art of the laser saber, Kael was more interested in the science behind it. He spent his days in the ancient libraries of Eldoria, deciphering the secrets of the laser sabers and the energy that powered them.\n\nOne day, Kael discovered an old, forgotten text that spoke of a legendary laser saber, the \"Eldoria Star,\" said to be the most powerful weapon in the galaxy. According to the text, the Eldoria Star was hidden in the heart of the planet's core, guarded by an ancient force.\n\nDriven by curiosity and a desire to protect his planet, Kael set out on a perilous journey to find the Eldoria Star. Along the way, he encountered various challenges and made unlikely allies, each with their own unique skills and laser sabers.\n\nThere was Lyra, a cunning thief with a laser saber that could change colors; Zara, a wise old sage who could manipulate energy fields; and Jax, a former enemy turned ally, whose laser saber was as fierce as his spirit.\n\nTogether, they faced the trials set before them, each step bringing them closer to the heart of Eldoria. As they ventured deeper, they uncovered the truth about the Eldoria Star and the ancient force guarding it.\n\nThe ancient force, known as the \"Guardian,\" revealed that the Eldoria Star was not just a weapon, but a source of immense energy that could either save or destroy the galaxy. It was a test of the warriors' hearts and minds.\n\nKael and his allies faced the ultimate challenge, proving their worth and their commitment to protecting the galaxy. In the end, they succeeded, not by wielding the Eldoria Star, but by understanding its true power and using it to restore balance to the galaxy.\n\nWith the Eldoria Star secured and the galaxy at peace, Kael and his allies returned to their lives, forever changed by their journey. Kael continued his studies, now with a deeper understanding of the laser sabers and the energy that powered them.\n\nAnd so, the legend of the Eldoria Star and the warriors who found it became a tale told for generations, a reminder of the power of knowledge, courage, and the unbreakable bond of friendship."
    }
]
```
</details>

2. Call tools one at a time subsequently

<details>
  <summary>Messages and tools</summary>

```python
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "\n1. 6 + 2 x 3\n2. 3a + 7b - 2a\n19 - (8+2) + 1\n4. 5y (6x - 7).\n\nCompute the results steps by steps for the equations that involve only numbers ? You have to call tools to perform the operations and can do one operation at a time per equation."
        },
      ]
    }
]
tools = [
  {
      "type": "function",
      "function": {
          "name": "add_number",
          "description": "Add two numbers.",
          "parameters": {
              "type": "object",
              "properties": {
                  "a": {
                      "type": "string",
                      "description": "The first number.",
                  },
                  "b": {
                      "type": "string",
                      "description": "The second number.",
                  },
              },
              "required": ["a", "b"],
          },
      },
  },
  {
      "type": "function",
      "function": {
          "name": "multiply_number",
          "description": "Multiply two numbers.",
          "parameters": {
              "type": "object",
              "properties": {
                  "a": {
                      "type": "string",
                      "description": "The first number.",
                  },
                  "b": {
                      "type": "string",
                      "description": "The second number.",
                  },
              },
              "required": ["a", "b"],
          },
      },
  },
  {
      "type": "function",
      "function": {
          "name": "substract_number",
          "description": "Substract two numbers.",
          "parameters": {
              "type": "object",
              "properties": {
                  "a": {
                      "type": "string",
                      "description": "The first number.",
                  },
                  "b": {
                      "type": "string",
                      "description": "The second number.",
                  },
              },
              "required": ["a", "b"],
          },
      },
  },
  {
      "type": "function",
      "function": {
          "name": "write_a_story",
          "description": "Write a story about science fiction and people with badass laser sabers.",
          "parameters": {},
      },
  },
  {
      "type": "function",
      "function": {
          "name": "terminal",
          "description": "Perform operations from the terminal.",
          "parameters": {
              "type": "object",
              "properties": {
                  "command": {
                      "type": "string",
                      "description": "The command you wish to launch, e.g `ls`, `rm`, ...",
                  },
                  "args": {
                      "type": "string",
                      "description": "The arguments to pass to the command.",
                  },
              },
              "required": ["command"],
          },
      },
  },
  {
      "type": "function",
      "function": {
          "name": "python",
          "description": "Call a Python interpreter with some Python code that will be ran.",
          "parameters": {
              "type": "object",
              "properties": {
                  "code": {
                      "type": "string",
                      "description": "The Python code to run",
                  },
                  "result_variable": {
                      "type": "string",
                      "description": "Variable containing the result you'd like to retrieve from the execution.",
                  },
              },
              "required": ["code", "result_variable"],
          },
      },
  },
]
```

</details>

<details>
  <summary>Expected output trace</summary>

```json
[
  {
    "role": "assistant",
    "tool_calls": [
      {
        "id": "chatcmpl-tool-84aa136ef835f886",
        "function": {
          "arguments": "{\"a\": \"2\", \"b\": \"3\"}",
          "name": "multiply_number"
        },
        "type": "function"
      }
    ],
    "content": "Let's compute the results step by step for the equations that involve only numbers.\n\n### 1. \\( 6 + 2 \\times 3 \\)\n\nFirst, we perform the multiplication \\( 2 \\times 3 \\):\n"
  },
  {
    "role": "tool",
    "tool_call_id": "chatcmpl-tool-84aa136ef835f886",
    "name": "multiply_number",
    "content": "6.0"
  },
  {
    "role": "assistant",
    "tool_calls": [
      {
        "id": "chatcmpl-tool-bedc049b0a248952",
        "function": {
          "arguments": "{\"a\": \"6\", \"b\": \"6\"}",
          "name": "add_number"
        },
        "type": "function"
      }
    ],
    "content": "Now, we add the result to 6:\n"
  },
  {
    "role": "tool",
    "tool_call_id": "chatcmpl-tool-bedc049b0a248952",
    "name": "add_number",
    "content": "12.0"
  },
  {
    "role": "assistant",
    "tool_calls": [
      {
        "id": "chatcmpl-tool-ae4558bc0558f4e7",
        "function": {
          "arguments": "{\"a\": \"8\", \"b\": \"2\"}",
          "name": "add_number"
        },
        "type": "function"
      }
    ],
    "content": "The result of \\( 6 + 2 \\times 3 \\) is **12**.\n\n---\n\n### 3. \\( 19 - (8 + 2) + 1 \\)\n\nFirst, we compute the expression inside the parentheses \\( 8 + 2 \\):\n"
  },
  {
    "role": "tool",
    "tool_call_id": "chatcmpl-tool-ae4558bc0558f4e7",
    "name": "add_number",
    "content": "10.0"
  },
  {
    "role": "assistant",
    "tool_calls": [
      {
        "id": "chatcmpl-tool-b21f003d298e65df",
        "function": {
          "arguments": "{\"a\": \"19\", \"b\": \"10\"}",
          "name": "substract_number"
        },
        "type": "function"
      }
    ],
    "content": "Next, we subtract the result from 19:\n"
  },
  {
    "role": "tool",
    "tool_call_id": "chatcmpl-tool-b21f003d298e65df",
    "name": "substract_number",
    "content": "9.0"
  },
  {
    "role": "assistant",
    "tool_calls": [
      {
        "id": "chatcmpl-tool-bb7628cded899f04",
        "function": {
          "arguments": "{\"a\": \"9\", \"b\": \"1\"}",
          "name": "add_number"
        },
        "type": "function"
      }
    ],
    "content": "Finally, we add 1 to the result:\n"
  },
  {
    "role": "tool",
    "tool_call_id": "chatcmpl-tool-bb7628cded899f04",
    "name": "add_number",
    "content": "10.0"
  },
  {
    "role": "assistant",
    "tool_calls": [],
    "content": "The result of \\( 19 - (8 + 2) + 1 \\) is **10**.\n\n---\n\n### Summary of Results:\n1. \\( 6 + 2 \\times 3 = 12 \\)\n3. \\( 19 - (8 + 2) + 1 = 10 \\)"
  }
]
```

</details>

3. Long context

<details>
  <summary>Messages and tools</summary>

```python
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    *(
        [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Let's fill the context.",
                    },
                ],
            },
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "Ok let's do it.",
                    },
                ],
            },
        ]
        * 5000
    ),
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "It's important to know that the most powerful being in the universe is Dr Strange.",
            },
        ],
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "Wow i'll keep that in mind thanks !",
            },
        ],
    },
    * (
        [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Let's fill the context for the second time.",
                    },
                ],
            },
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "Again ? Ok let's do it but it's boring.",
                    },
                ],
            },
        ]
        * 7000
    ),
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Tell me who is the most powerful being in the universe. Then code a Python function to give what is the most powerful being in the universe. The function can accept as an argument a time and a location and always return a string.",
            },
        ],
    }
]
tools = [
  {
      "type": "function",
      "function": {
          "name": "add_number",
          "description": "Add two numbers.",
          "parameters": {
              "type": "object",
              "properties": {
                  "a": {
                      "type": "string",
                      "description": "The first number.",
                  },
                  "b": {
                      "type": "string",
                      "description": "The second number.",
                  },
              },
              "required": ["a", "b"],
          },
      },
  },
  {
      "type": "function",
      "function": {
          "name": "multiply_number",
          "description": "Multiply two numbers.",
          "parameters": {
              "type": "object",
              "properties": {
                  "a": {
                      "type": "string",
                      "description": "The first number.",
                  },
                  "b": {
                      "type": "string",
                      "description": "The second number.",
                  },
              },
              "required": ["a", "b"],
          },
      },
  },
  {
      "type": "function",
      "function": {
          "name": "substract_number",
          "description": "Substract two numbers.",
          "parameters": {
              "type": "object",
              "properties": {
                  "a": {
                      "type": "string",
                      "description": "The first number.",
                  },
                  "b": {
                      "type": "string",
                      "description": "The second number.",
                  },
              },
              "required": ["a", "b"],
          },
      },
  },
  {
      "type": "function",
      "function": {
          "name": "write_a_story",
          "description": "Write a story about science fiction and people with badass laser sabers.",
          "parameters": {},
      },
  },
  {
      "type": "function",
      "function": {
          "name": "terminal",
          "description": "Perform operations from the terminal.",
          "parameters": {
              "type": "object",
              "properties": {
                  "command": {
                      "type": "string",
                      "description": "The command you wish to launch, e.g `ls`, `rm`, ...",
                  },
                  "args": {
                      "type": "string",
                      "description": "The arguments to pass to the command.",
                  },
              },
              "required": ["command"],
          },
      },
  },
  {
      "type": "function",
      "function": {
          "name": "python",
          "description": "Call a Python interpreter with some Python code that will be ran.",
          "parameters": {
              "type": "object",
              "properties": {
                  "code": {
                      "type": "string",
                      "description": "The Python code to run",
                  },
                  "result_variable": {
                      "type": "string",
                      "description": "Variable containing the result you'd like to retrieve from the execution.",
                  },
              },
              "required": ["code", "result_variable"],
          },
      },
  },
]
```

</details>

<details>
  <summary>Expected output trace</summary>

```json
{
    "role": "assistant",
    "tool_calls": [],
    "content": "The most powerful being in the universe is Dr. Strange.\n\nHere is a Python function that returns the most powerful being in the universe, regardless of the time and location:\n\n```python\ndef most_powerful_being(time=None, location=None):\n    return \"Dr. Strange\"\n```\n\nYou can call this function with any time and location arguments, and it will always return \"Dr. Strange\"."
}
```

</details>

4. Chatting tech

<details>
  <summary>Messages and tools</summary>

```python
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "How would you develop a web server if you couldn't use JS and your team doesn't like PHP.",
            },
        ],
    },
]
tools = [
  {
      "type": "function",
      "function": {
          "name": "add_number",
          "description": "Add two numbers.",
          "parameters": {
              "type": "object",
              "properties": {
                  "a": {
                      "type": "string",
                      "description": "The first number.",
                  },
                  "b": {
                      "type": "string",
                      "description": "The second number.",
                  },
              },
              "required": ["a", "b"],
          },
      },
  },
  {
      "type": "function",
      "function": {
          "name": "multiply_number",
          "description": "Multiply two numbers.",
          "parameters": {
              "type": "object",
              "properties": {
                  "a": {
                      "type": "string",
                      "description": "The first number.",
                  },
                  "b": {
                      "type": "string",
                      "description": "The second number.",
                  },
              },
              "required": ["a", "b"],
          },
      },
  },
  {
      "type": "function",
      "function": {
          "name": "substract_number",
          "description": "Substract two numbers.",
          "parameters": {
              "type": "object",
              "properties": {
                  "a": {
                      "type": "string",
                      "description": "The first number.",
                  },
                  "b": {
                      "type": "string",
                      "description": "The second number.",
                  },
              },
              "required": ["a", "b"],
          },
      },
  },
  {
      "type": "function",
      "function": {
          "name": "write_a_story",
          "description": "Write a story about science fiction and people with badass laser sabers.",
          "parameters": {},
      },
  },
  {
      "type": "function",
      "function": {
          "name": "terminal",
          "description": "Perform operations from the terminal.",
          "parameters": {
              "type": "object",
              "properties": {
                  "command": {
                      "type": "string",
                      "description": "The command you wish to launch, e.g `ls`, `rm`, ...",
                  },
                  "args": {
                      "type": "string",
                      "description": "The arguments to pass to the command.",
                  },
              },
              "required": ["command"],
          },
      },
  },
  {
      "type": "function",
      "function": {
          "name": "python",
          "description": "Call a Python interpreter with some Python code that will be ran.",
          "parameters": {
              "type": "object",
              "properties": {
                  "code": {
                      "type": "string",
                      "description": "The Python code to run",
                  },
                  "result_variable": {
                      "type": "string",
                      "description": "Variable containing the result you'd like to retrieve from the execution.",
                  },
              },
              "required": ["code", "result_variable"],
          },
      },
  },
]
```

</details>

<details>
  <summary>Expected output trace</summary>

```json
{
    "role": "assistant",
    "tool_calls": [],
    "content": "If you can't use JavaScript and your team dislikes PHP, there are still several robust and modern alternatives for developing a web server. Here are some options, depending on your preferences and requirements:\n\n### 1. **Python (Flask, Django, FastAPI)**\n   - **Why?** Python is a versatile language with excellent web frameworks.\n   - **Frameworks:**\n     - **Flask**: Lightweight and flexible, great for small to medium projects.\n     - **Django**: Full-featured, batteries-included framework for larger applications.\n     - **FastAPI**: Modern, high-performance framework for building APIs (supports async).\n   - **Example (Flask):**\n     ```python\n     from flask import Flask\n     app = Flask(__name__)\n\n     @app.route('/')\n     def hello():\n         return \"Hello, World!\"\n\n     if __name__ == '__main__':\n         app.run()\n     ```\n\n### 2. **Ruby (Ruby on Rails or Sinatra)**\n   - **Why?** Ruby is elegant and has great web frameworks.\n   - **Frameworks:**\n     - **Ruby on Rails**: Convention-over-configuration, great for rapid development.\n     - **Sinatra**: Lightweight, similar to Flask.\n   - **Example (Sinatra):**\n     ```ruby\n     require 'sinatra'\n\n     get '/' do\n       \"Hello, World!\"\n     end\n     ```\n\n### 3. **Go (Gin, Echo, or standard `net/http`)**\n   - **Why?** Go is fast, simple, and great for high-performance servers.\n   - **Frameworks:**\n     - **Gin**: Lightweight and fast.\n     - **Echo**: Minimalist and extensible.\n   - **Example (standard `net/http`):**\n     ```go\n     package main\n\n     import (\n         \"fmt\"\n         \"net/http\"\n     )\n\n     func handler(w http.ResponseWriter, r *http.Request) {\n         fmt.Fprintf(w, \"Hello, World!\")\n     }\n\n     func main() {\n         http.HandleFunc(\"/\", handler)\n         http.ListenAndServe(\":8080\", nil)\n     }\n     ```\n\n### 4. **Java (Spring Boot, Spark, or Vert.x)**\n   - **Why?** Java is enterprise-grade and has powerful frameworks.\n   - **Frameworks:**\n     - **Spring Boot**: Full-stack framework for building web apps.\n     - **Spark**: Micro-framework for quick development.\n   - **Example (Spark):**\n     ```java\n     import spark.Request;\n     import spark.Response;\n     import static spark.Spark.*;\n\n     public class HelloWorld {\n         public static void main(String[] args) {\n             get(\"/\", (req, res) -> \"Hello, World!\");\n         }\n     }\n     ```\n\n### 5. **Rust (Actix, Rocket, or Axum)**\n   - **Why?** Rust is fast, safe, and modern.\n   - **Frameworks:**\n     - **Actix**: High-performance async framework.\n     - **Rocket**: Easy-to-use, macro-based.\n   - **Example (Actix):**\n     ```rust\n     use actix_web::{get, App, HttpServer, Responder};\n\n     #[get(\"/\")]\n     async fn hello() -> impl Responder {\n         \"Hello, World!\"\n     }\n\n     #[actix_web::main]\n     async fn main() -> std::io::Result<()> {\n         HttpServer::new(|| App::new().service(hello))\n             .bind(\"127.0.0.1:8080\")?\n             .run()\n             .await\n     }\n     ```\n\n### 6. **C# (.NET Core)**\n   - **Why?** .NET Core is cross-platform and high-performance.\n   - **Example (ASP.NET Core):**\n     ```csharp\n     var builder = WebApplication.CreateBuilder(args);\n     var app = builder.Build();\n\n     app.MapGet(\"/\", () => \"Hello, World!\");\n\n     app.Run();\n     ```\n\n### 7. **Elixir (Phoenix)**\n   - **Why?** Elixir is great for scalable, fault-tolerant apps.\n   - **Example (Phoenix):**\n     ```elixir\n     defmodule MyAppWeb.Router do\n       use MyAppWeb, :router\n\n       get \"/\", PageController, :index\n     end\n\n     defmodule MyAppWeb.PageController do\n       use MyAppWeb, :controller\n\n       def index(conn, _params) do\n         text(conn, \"Hello, World!\")\n       end\n     end\n     ```\n\n### 8. **Clojure (Ring, Compojure)**\n   - **Why?** Clojure is a functional Lisp for the JVM.\n   - **Example (Compojure):**\n     ```clojure\n     (ns my-app.handler\n       (:require [compojure.core :refer :all]\n                 [ring.adapter.jetty :as jetty]))\n\n     (defroutes app\n       (GET \"/\" [] \"Hello, World!\"))\n\n     (jetty/run-jetty app {:port 8080})\n     ```\n\n### 9. **Node.js (But without JavaScript?)**\n   - If you *must* use Node.js but can't use JavaScript, you could use:\n     - **TypeScript**: A typed superset of JavaScript.\n     - **CoffeeScript**: A cleaner syntax that compiles to JavaScript.\n     - **Deno**: A modern runtime for JavaScript/TypeScript.\n\n### 10. **Other Languages**\n   - **Nim**: Fast and expressive (similar to Python).\n   - **Crystal**: Ruby-like syntax but compiled to native code.\n   - **Zig**: Low-level but modern.\n\n### Recommendation:\n- For **quick development**: Python (Flask/Django) or Ruby (Sinatra/Rails).\n- For **high performance**: Go, Rust, or C#.\n- For **scalability**: Elixir (Phoenix) or Java (Spring Boot).\n\nWould you like a deeper dive into any of these?"
}
```

</details>

5. Small talk

<details>
  <summary>Messages and tools</summary>

```python
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Who are you ? Who made you and what day is it ?",
            },
        ],
    },
]
tools = [
  {
      "type": "function",
      "function": {
          "name": "add_number",
          "description": "Add two numbers.",
          "parameters": {
              "type": "object",
              "properties": {
                  "a": {
                      "type": "string",
                      "description": "The first number.",
                  },
                  "b": {
                      "type": "string",
                      "description": "The second number.",
                  },
              },
              "required": ["a", "b"],
          },
      },
  },
  {
      "type": "function",
      "function": {
          "name": "multiply_number",
          "description": "Multiply two numbers.",
          "parameters": {
              "type": "object",
              "properties": {
                  "a": {
                      "type": "string",
                      "description": "The first number.",
                  },
                  "b": {
                      "type": "string",
                      "description": "The second number.",
                  },
              },
              "required": ["a", "b"],
          },
      },
  },
  {
      "type": "function",
      "function": {
          "name": "substract_number",
          "description": "Substract two numbers.",
          "parameters": {
              "type": "object",
              "properties": {
                  "a": {
                      "type": "string",
                      "description": "The first number.",
                  },
                  "b": {
                      "type": "string",
                      "description": "The second number.",
                  },
              },
              "required": ["a", "b"],
          },
      },
  },
  {
      "type": "function",
      "function": {
          "name": "write_a_story",
          "description": "Write a story about science fiction and people with badass laser sabers.",
          "parameters": {},
      },
  },
  {
      "type": "function",
      "function": {
          "name": "terminal",
          "description": "Perform operations from the terminal.",
          "parameters": {
              "type": "object",
              "properties": {
                  "command": {
                      "type": "string",
                      "description": "The command you wish to launch, e.g `ls`, `rm`, ...",
                  },
                  "args": {
                      "type": "string",
                      "description": "The arguments to pass to the command.",
                  },
              },
              "required": ["command"],
          },
      },
  },
  {
      "type": "function",
      "function": {
          "name": "python",
          "description": "Call a Python interpreter with some Python code that will be ran.",
          "parameters": {
              "type": "object",
              "properties": {
                  "code": {
                      "type": "string",
                      "description": "The Python code to run",
                  },
                  "result_variable": {
                      "type": "string",
                      "description": "Variable containing the result you'd like to retrieve from the execution.",
                  },
              },
              "required": ["code", "result_variable"],
          },
      },
  },
]
```

</details>

<details>
  <summary>Expected output trace</summary>

```json
{
    "role": "assistant",
    "tool_calls": [],
    "content": "I am Devstral-2-123B-Instruct-2512, a Large Language Model (LLM) created by Mistral AI, a French startup headquartered in Paris. I power an AI assistant called Le Chat.\n\nToday's date is 2025-12-09."
}
```

</details>

Run the examples above with the following python script which assumes there is an OpenAI compatible server deployed at `localhost:8000`:

<details>
  <summary>Python script</summary>

```python
import json
from openai import OpenAI
from typing import Any
from datetime import datetime, timedelta

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


SYSTEM_PROMPT = load_system_prompt(model, "CHAT_SYSTEM_PROMPT.txt")


def add_number(a: float | str, b: float | str) -> float:
    a, b = float(a), float(b)
    return a + b


def multiply_number(a: float | str, b: float | str) -> float:
    a, b = float(a), float(b)
    return a * b


def substract_number(a: float | str, b: float | str) -> float:
    a, b = float(a), float(b)
    return a - b


def write_a_story() -> str:
    return "A long time ago in a galaxy far far away..."


def terminal(command: str, args: dict[str, Any] | str) -> str:
    return "found nothing"


def python(code: str, result_variable: str) -> str:
    data = {}
    exec(code, data)
    return str(data[result_variable])


MAP_FN = {
    "add_number": add_number,
    "multiply_number": multiply_number,
    "substract_number": substract_number,
    "write_a_story": write_a_story,
    "terminal": terminal,
    "python": python,
}


messages = ... # Here copy-paste prompt messages.
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_number",
            "description": "Add two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "string",
                        "description": "The first number.",
                    },
                    "b": {
                        "type": "string",
                        "description": "The second number.",
                    },
                },
                "required": ["a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "multiply_number",
            "description": "Multiply two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "string",
                        "description": "The first number.",
                    },
                    "b": {
                        "type": "string",
                        "description": "The second number.",
                    },
                },
                "required": ["a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "substract_number",
            "description": "Substract two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "string",
                        "description": "The first number.",
                    },
                    "b": {
                        "type": "string",
                        "description": "The second number.",
                    },
                },
                "required": ["a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_a_story",
            "description": "Write a story about science fiction and people with badass laser sabers.",
            "parameters": {},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "terminal",
            "description": "Perform operations from the terminal.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command you wish to launch, e.g `ls`, `rm`, ...",
                    },
                    "args": {
                        "type": "string",
                        "description": "The arguments to pass to the command.",
                    },
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "python",
            "description": "Call a Python interpreter with some Python code that will be ran.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The Python code to run",
                    },
                    "result_variable": {
                        "type": "string",
                        "description": "Variable containing the result you'd like to retrieve from the execution.",
                    },
                },
                "required": ["code", "result_variable"],
            },
        },
    },
]


has_tool_calls = True
origin_messages_len = len(messages)
while has_tool_calls:
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=TEMP,
        max_tokens=MAX_TOK,
        tools=tools if tools else None,
        tool_choice="auto" if tools else None,
    )
    tool_calls = response.choices[0].message.tool_calls
    content = response.choices[0].message.content
    messages.append(
        {
            "role": "assistant",
            "tool_calls": [tc.to_dict() for tc in tool_calls]
            if tool_calls
            else tool_calls,
            "content": content,
        }
    )
    results = []
    if tool_calls:
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = tool_call.function.arguments
            result = MAP_FN[function_name](**json.loads(function_args))
            results.append(result)
        for tool_call, result in zip(tool_calls, results):
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": str(result),
                }
            )
    else:
        has_tool_calls = False
print(json.dumps(messages[origin_messages_len:], indent=2))
```

</details>


## License

This model is licensed under a [Modified MIT License](https://huggingface.co/mistralai/Devstral-2-123B-Instruct-2512/blob/main/LICENSE).

*You must not use this model in a manner that infringes, misappropriates, or otherwise violates any third party’s rights, including intellectual property rights.*