---
license: mit
library_name: transformers
base_model:
  - deepseek-ai/DeepSeek-V3.2-Exp-Base
base_model_relation: finetune
---
# DeepSeek-V3.2: Efficient Reasoning & Agentic AI

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

<p align="center">
  <a href="https://huggingface.co/deepseek-ai/DeepSeek-V3.2/blob/main/assets/paper.pdf"><b>Technical Report</b>👁️</a>
</p>

## Introduction

We introduce **DeepSeek-V3.2**, a model that harmonizes high computational efficiency with superior reasoning and agent performance. Our approach is built upon three key technical breakthroughs:

1. **DeepSeek Sparse Attention (DSA):** We introduce DSA, an efficient attention mechanism that substantially reduces computational complexity while preserving model performance, specifically optimized for long-context scenarios.
2. **Scalable Reinforcement Learning Framework:** By implementing a robust RL protocol and scaling post-training compute, *DeepSeek-V3.2* performs comparably to GPT-5. Notably, our high-compute variant, **DeepSeek-V3.2-Speciale**, **surpasses GPT-5** and exhibits reasoning proficiency on par with Gemini-3.0-Pro.
    - *Achievement:* 🥇 **Gold-medal performance** in the 2025 International Mathematical Olympiad (IMO) and International Olympiad in Informatics (IOI).
3. **Large-Scale Agentic Task Synthesis Pipeline:** To integrate **reasoning into tool-use** scenarios, we developed a novel synthesis pipeline that systematically generates training data at scale. This facilitates scalable agentic post-training, improving compliance and generalization in complex interactive environments.

<div align="center">
 <img src="assets/benchmark.png" >
</div>

We have also released the final submissions for IOI 2025, ICPC World Finals, IMO 2025 and CMO 2025, which were selected based on our designed pipeline. These materials are provided for the community to conduct secondary verification. The files can be accessed at `assets/olympiad_cases`.

## Chat Template

DeepSeek-V3.2 introduces significant updates to its chat template compared to prior versions. The primary changes involve a revised format for tool calling and the introduction of a "thinking with tools" capability.

To assist the community in understanding and adapting to this new template, we have provided a dedicated `encoding` folder, which contains Python scripts and test cases demonstrating how to encode messages in OpenAI-compatible format into input strings for the model and how to parse the model's text output.

A brief example is illustrated below:

```python
import transformers
# encoding/encoding_dsv32.py
from encoding_dsv32 import encode_messages, parse_message_from_completion_text

tokenizer = transformers.AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-V3.2")

messages = [
    {"role": "user", "content": "hello"},
    {"role": "assistant", "content": "Hello! I am DeepSeek.", "reasoning_content": "thinking..."},
    {"role": "user", "content": "1+1=?"}
]
encode_config = dict(thinking_mode="thinking", drop_thinking=True, add_default_bos_token=True)

# messages -> string
prompt = encode_messages(messages, **encode_config)
# Output: "<｜begin▁of▁sentence｜><｜User｜>hello<｜Assistant｜></think>Hello! I am DeepSeek.<｜end▁of▁sentence｜><｜User｜>1+1=?<｜Assistant｜><think>"

# string -> tokens
tokens = tokenizer.encode(prompt)
# Output: [0, 128803, 33310, 128804, 128799, 19923, 3, 342, 1030, 22651, 4374, 1465, 16, 1, 128803, 19, 13, 19, 127252, 128804, 128798]
```

Important Notes:

1. This release does not include a Jinja-format chat template. Please refer to the Python code mentioned above.
2. The output parsing function included in the code is designed to handle well-formatted strings only. It does not attempt to correct or recover from malformed output that the model might occasionally generate. It is not suitable for production use without robust error handling.
3. A new role named `developer` has been introduced in the chat template. This role is dedicated exclusively to search agent scenarios and is designated for no other tasks. The official API does not accept messages assigned to `developer`.

## How to Run Locally

The model structure of DeepSeek-V3.2 and DeepSeek-V3.2-Speciale are the same as DeepSeek-V3.2-Exp. Please visit [DeepSeek-V3.2-Exp](https://github.com/deepseek-ai/DeepSeek-V3.2-Exp) repo for more information about running this model locally.

Usage Recommendations:

1. For local deployment, we recommend setting the sampling parameters to `temperature = 1.0, top_p = 0.95`.
2. Please note that the DeepSeek-V3.2-Speciale variant is designed exclusively for deep reasoning tasks and does not support the tool-calling functionality.

## License

This repository and the model weights are licensed under the [MIT License](LICENSE).

## Citation

```
@misc{deepseekai2025deepseekv32,
      title={DeepSeek-V3.2: Pushing the Frontier of Open Large Language Models}, 
      author={DeepSeek-AI},
      year={2025},
}
```

## Contact

If you have any questions, please raise an issue or contact us at [service@deepseek.com](service@deepseek.com).
