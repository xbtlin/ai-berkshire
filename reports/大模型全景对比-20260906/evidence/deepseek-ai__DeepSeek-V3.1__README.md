---
license: mit
library_name: transformers
base_model:
- deepseek-ai/DeepSeek-V3.1-Base
---
# DeepSeek-V3.1

<!-- markdownlint-disable first-line-h1 -->
<!-- markdownlint-disable html -->
<!-- markdownlint-disable no-duplicate-header -->

<div align="center">
  <img src="https://github.com/deepseek-ai/DeepSeek-V2/blob/main/figures/logo.svg?raw=true" width="60%" alt="DeepSeek-V3" />
</div>
<hr>
<div align="center" style="line-height: 1;">
  <a href="https://www.deepseek.com/" target="_blank" style="margin: 2px;">
    <img alt="Homepage" src="https://github.com/deepseek-ai/DeepSeek-V2/blob/main/figures/badge.svg?raw=true" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://chat.deepseek.com/" target="_blank" style="margin: 2px;">
    <img alt="Chat" src="https://img.shields.io/badge/🤖%20Chat-DeepSeek%20V3-536af5?color=536af5&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://huggingface.co/deepseek-ai" target="_blank" style="margin: 2px;">
    <img alt="Hugging Face" src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-DeepSeek%20AI-ffc107?color=ffc107&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>

<div align="center" style="line-height: 1;">
  <a href="https://discord.gg/Tc7c45Zzu5" target="_blank" style="margin: 2px;">
    <img alt="Discord" src="https://img.shields.io/badge/Discord-DeepSeek%20AI-7289da?logo=discord&logoColor=white&color=7289da" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://github.com/deepseek-ai/DeepSeek-V2/blob/main/figures/qr.jpeg?raw=true" target="_blank" style="margin: 2px;">
    <img alt="Wechat" src="https://img.shields.io/badge/WeChat-DeepSeek%20AI-brightgreen?logo=wechat&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://twitter.com/deepseek_ai" target="_blank" style="margin: 2px;">
    <img alt="Twitter Follow" src="https://img.shields.io/badge/Twitter-deepseek_ai-white?logo=x&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>

<div align="center" style="line-height: 1;">
  <a href="LICENSE" style="margin: 2px;">
    <img alt="License" src="https://img.shields.io/badge/License-MIT-f5de53?&color=f5de53" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>

## Introduction

DeepSeek-V3.1 is a hybrid model that supports both thinking mode and non-thinking mode. Compared to the previous version, this upgrade brings improvements in multiple aspects:

- **Hybrid thinking mode**: One model supports both thinking mode and non-thinking mode by changing the chat template. 

- **Smarter tool calling**: Through post-training optimization, the model's performance in tool usage and agent tasks has significantly improved.

- **Higher thinking efficiency**: DeepSeek-V3.1-Think achieves comparable answer quality to DeepSeek-R1-0528, while responding more quickly.

DeepSeek-V3.1 is post-trained on the top of DeepSeek-V3.1-Base, which is built upon the original V3 base checkpoint through a two-phase long context extension approach, following the methodology outlined in the original DeepSeek-V3 report. We have expanded our dataset by collecting additional long documents and substantially extending both training phases. The 32K extension phase has been increased 10-fold to 630B tokens, while the 128K extension phase has been extended by 3.3x to 209B tokens.

Additionally, DeepSeek-V3.1 is trained using the **UE8M0 FP8 scale data format on both model weights and activations** to ensure compatibility with microscaling data formats. Please refer to [DeepGEMM](https://github.com/deepseek-ai/DeepGEMM) for more details.

## Model Downloads

<div align="center">

| **Model** | **#Total Params** | **#Activated Params** | **Context Length** | **Download** |
| :------------: | :------------: | :------------: | :------------: | :------------: |
| DeepSeek-V3.1-Base | 671B | 37B | 128K | [HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-V3.1-Base) \| [ModelScope](https://modelscope.cn/models/deepseek-ai/DeepSeek-V3.1-Base) |
| DeepSeek-V3.1 | 671B | 37B | 128K | [HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-V3.1) \| [ModelScope](https://modelscope.cn/models/deepseek-ai/DeepSeek-V3.1) |

</div>

## Chat Template

The details of our chat template is described in `tokenizer_config.json` and `assets/chat_template.jinja`. Here is a brief description.

### Non-Thinking

#### First-Turn

Prefix:
`<｜begin▁of▁sentence｜>{system prompt}<｜User｜>{query}<｜Assistant｜></think>`

With the given prefix, DeepSeek V3.1 generates responses to queries in non-thinking mode. Unlike DeepSeek V3,  it introduces an additional token `</think>`.

#### Multi-Turn
Context:
`<｜begin▁of▁sentence｜>{system prompt}<｜User｜>{query}<｜Assistant｜></think>{response}<｜end▁of▁sentence｜>...<｜User｜>{query}<｜Assistant｜></think>{response}<｜end▁of▁sentence｜>`

Prefix:
`<｜User｜>{query}<｜Assistant｜></think>`

By concatenating the context and the prefix, we obtain the correct prompt for the query.

### Thinking

#### First-Turn
Prefix:
`<｜begin▁of▁sentence｜>{system prompt}<｜User｜>{query}<｜Assistant｜><think>`

The prefix of thinking mode is similar to DeepSeek-R1. 


#### Multi-Turn
Context:
`<｜begin▁of▁sentence｜>{system prompt}<｜User｜>{query}<｜Assistant｜></think>{response}<｜end▁of▁sentence｜>...<｜User｜>{query}<｜Assistant｜></think>{response}<｜end▁of▁sentence｜>`

Prefix:
`<｜User｜>{query}<｜Assistant｜><think>`

The multi-turn template is the same with non-thinking multi-turn chat template. It means the thinking token in the last turn will be dropped but the `</think>` is retained in every turn of context. 

### ToolCall
Toolcall is supported in non-thinking mode. The format is: 

`<｜begin▁of▁sentence｜>{system prompt}\n\n{tool_description}<｜User｜>{query}<｜Assistant｜></think>` where the tool_description is 

```
## Tools
You have access to the following tools:

### {tool_name1}
Description: {description}

Parameters: {json.dumps(parameters)}

IMPORTANT: ALWAYS adhere to this exact format for tool use:
<｜tool▁calls▁begin｜><｜tool▁call▁begin｜>tool_call_name<｜tool▁sep｜>tool_call_arguments<｜tool▁call▁end｜>{additional_tool_calls}<｜tool▁calls▁end｜>

Where:
- `tool_call_name` must be an exact match to one of the available tools
- `tool_call_arguments` must be valid JSON that strictly follows the tool's Parameters Schema
- For multiple tool calls, chain them directly without separators or spaces
```

### Code-Agent
We support various code agent frameworks. Please refer to the above toolcall format to create your own code agents. An example is shown in `assets/code_agent_trajectory.html`.

### Search-Agent
We design a specific format for searching toolcall in thinking mode, to support search agent. 

For complex questions that require accessing external or up-to-date information, DeepSeek-V3.1 can leverage a user-provided search tool through a multi-turn tool-calling process.

Please refer to the `assets/search_tool_trajectory.html` and `assets/search_python_tool_trajectory.html` for the detailed template.

## Evaluation
| Category | Benchmark (Metric)              | DeepSeek V3.1-NonThinking | DeepSeek V3 0324 | DeepSeek V3.1-Thinking     | DeepSeek R1 0528
|----------|----------------------------------|-----------------|---|---|---|
| General  |
|          | MMLU-Redux (EM)              | 91.8     | 90.5    | 93.7          | 93.4
|          | MMLU-Pro (EM)                  | 83.7  | 81.2    | 84.8          | 85.0
|          | GPQA-Diamond (Pass@1)           | 74.9   | 68.4   | 80.1            | 81.0
|          | Humanity's Last Exam (Pass@1)   | -    |       -            | 15.9         | 17.7
|Search Agent| 
|          | BrowseComp       | -      | -  | 30.0 | 8.9
|          | BrowseComp_zh       | -     | -  | 49.2      | 35.7
|          | Humanity's Last Exam (Python + Search)      |-   | -    | 29.8         | 24.8
|          | SimpleQA             | -      | -    | 93.4  | 92.3
| Code |
|          | LiveCodeBench (2408-2505) (Pass@1)     | 56.4    | 43.0    | 74.8          | 73.3
|          | Codeforces-Div1 (Rating)        | -   | -    | 2091            | 1930
|          | Aider-Polyglot (Acc.)           | 68.4    | 55.1   | 76.3           | 71.6
| Code Agent|
|          | SWE Verified (Agent mode)           | 66.0       | 45.4  | -    | 44.6
|          | SWE-bench Multilingual (Agent mode)         | 54.5    | 29.3   | -            | 30.5
|          | Terminal-bench (Terminus 1 framework)       | 31.3     | 13.3      | -         | 5.7
| Math |
|          | AIME 2024 (Pass@1)                | 66.3     | 59.4     | 93.1      | 91.4
|          | AIME 2025 (Pass@1)                     | 49.8  | 51.3 | 88.4          | 87.5
|          | HMMT 2025 (Pass@1)        | 33.5    | 29.2   | 84.2 | 79.4 |

Note: 
- Search agents are evaluated with our internal search framework, which uses a commercial search API + webpage filter + 128K context window. Seach agent results of R1-0528 are evaluated with a pre-defined workflow. 

- SWE-bench is evaluated with our internal code agent framework.

- HLE is evaluated with the text-only subset.

### Usage Example

```python
import transformers

tokenizer = transformers.AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-V3.1")

messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Who are you?"},
    {"role": "assistant", "content": "<think>Hmm</think>I am DeepSeek"},
    {"role": "user", "content": "1+1=?"}
]

tokenizer.apply_chat_template(messages, tokenize=False, thinking=True, add_generation_prompt=True)
# '<｜begin▁of▁sentence｜>You are a helpful assistant<｜User｜>Who are you?<｜Assistant｜></think>I am DeepSeek<｜end▁of▁sentence｜><｜User｜>1+1=?<｜Assistant｜><think>'

tokenizer.apply_chat_template(messages, tokenize=False, thinking=False, add_generation_prompt=True)
# '<｜begin▁of▁sentence｜>You are a helpful assistant<｜User｜>Who are you?<｜Assistant｜></think>I am DeepSeek<｜end▁of▁sentence｜><｜User｜>1+1=?<｜Assistant｜></think>'
```

## How to Run Locally

The model structure of DeepSeek-V3.1 is the same as DeepSeek-V3. Please visit [DeepSeek-V3](https://github.com/deepseek-ai/DeepSeek-V3) repo for more information about running this model locally.

**Usage Recommendations:**

1. **The `mlp.gate.e_score_correction_bias `parameters should be loaded and computed in FP32 precision.**
2. **Ensure that FP8 model weights and activations are formatted using the UE8M0 scale format.**

## License

This repository and the model weights are licensed under the [MIT License](LICENSE).

## Citation

```
@misc{deepseekai2024deepseekv3technicalreport,
      title={DeepSeek-V3 Technical Report}, 
      author={DeepSeek-AI},
      year={2024},
      eprint={2412.19437},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2412.19437}, 
}
```

## Contact

If you have any questions, please raise an issue or contact us at [service@deepseek.com](service@deepseek.com).