---
inference: false
library_name: transformers
language:
- en
- ar
- bg
- bn
- ca
- cs
- da
- de
- el
- es
- et
- fa
- fi
- fil
- fr
- ga
- he
- hi
- hr
- hu
- id
- is
- it
- ja
- ko
- lt
- lv
- ms
- mt
- nl
- 'no'
- pa
- pl
- pt
- ro
- ru
- sk
- sl
- sr
- sv
- ta
- te
- th
- tr
- uk
- ur
- vi
- zh
license: apache-2.0
pipeline_tag: image-text-to-text
tags:
- conversational
- chat
---

# **Model Card for Command A+**

## **Model Summary**

Command A+ is an open source model with 25 billion active parameters and 218B total parameters model optimized for agentic, multilingual, and reasoning-heavy tasks with a focus on enterprise performance, while also providing support for vision inputs for processing image inputs.

Developed by: [Cohere](https://cohere.com/) and [Cohere Labs](https://cohere.com/research)

* Point of Contact: [**Cohere Labs**](https://cohere.com/research)  
* License: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)  
* Model: command-a-plus-05-2026  
* Model Size: 25B active parameters, 218B total parameters  
* Context length: 128K input

For more details about this model, please check out our [blog post](http://cohere.com/blog/command-a-plus). 

You can try out Command A+ before downloading the weights in our hosted [Hugging Face Space](https://huggingface.co/spaces/CohereLabs/command-a-plus-05-2026).


**Available quantizations**

The following quantizations are available with example minimum GPU requirements

| Quantization | Blackwell | Hopper |
| :---- | :---- | :---- |
| [BF16 (16-bit)](https://huggingface.co/CohereLabs/command-a-plus-05-2026-bf16) | 4 x B200 | 8 x H100 |
| [FP8 (8-bit)](https://huggingface.co/CohereLabs/command-a-plus-05-2026-fp8) | 2 x B200 | 4 x H100 |
| [W4A4 (4-bit)](https://huggingface.co/CohereLabs/command-a-plus-05-2026-w4a4) | 1 x B200 | 2 x H100 |

All three quantizations show negligible differences in benchmark quality and performance. **Our recommended quantization for most uses is [W4A4](https://huggingface.co/CohereLabs/command-a-plus-05-2026-w4a4) which boasts superior speed and latency characteristics alongside a smaller hardware footprint.**

For more details, please check out our [blog post](http://cohere.com/blog/command-a-plus). 


**Usage**

**Transformers**

Please install transformers from the source repository that includes the necessary changes for this model.

```py
# pip install transformers
from transformers import AutoTokenizer, AutoModelForImageTextToText

model_id = "CohereLabs/command-a-plus-05-2026-bf16"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForImageTextToText.from_pretrained(model_id)

# Format message with the command-a-plus-05-2026-bf16 chat template
messages = [{"role": "user", "content": "What has keys but can't open locks?"}]
input_ids = tokenizer.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_tensors="pt",
)

gen_tokens = model.generate(
    input_ids, 
    max_new_tokens=4096, 
    do_sample=True, 
    temperature=0.6,
    top_p=0.95
)

gen_text = tokenizer.decode(gen_tokens[0])
print(gen_text)
```

As a result, you should get an output that looks like this, where the thinking is generated between the `<START_THINKING>` and `<END_THINKING>`:

```py
<|START_THINKING|>The user asks a riddle: "What has keys but can't open locks?" The answer is a piano (or keyboard). So respond with answer.<|END_THINKING|>
```

You can also use the model directly using transformers pipeline abstraction:

```py
from transformers import pipeline
import torch

model_id = "CohereLabs/command-a-plus-05-2026-bf16"
tokenizer = AutoTokenizer.from_pretrained(model_id)

pipe = pipeline(
    "text-generation",
    model=model_id,
    dtype="auto",
    device_map="auto",
)

messages = [
    {"role": "user", "content": "Explain the Transformer architecture"},
]

text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
)

outputs = pipe(
    messages,
    max_new_tokens=300,
)
print(outputs[0]["generated_text"][-1])


```

**vLLM**

You can also run the model in vLLM. `vllm>=0.21.0` is required for Command A+ and accurate response parsing also requires installing [Cohere’s `melody` library](https://pypi.org/project/cohere-melody/). 

```
uv pip install vllm>=0.21.0 
uv pip install transformers uv pip install cohere_melody>=0.9.0
```

Then the vllm server can be started with the following command:

```
# This is for B200, adjust tp for your device vllm serve CohereLabs/command-a-plus-05-2026-bf16 -tp 4 --tool-call-parser cohere_command4 --reasoning-parser cohere_command4 --enable-auto-tool-choice
```

## **Model Details**

**Input**: Text and images.

**Output**: Model generates text. 

**Model Architecture**: Command A+ is a decoder-only Sparse Mixture-of-Experts Transformer Model. With 25B active parameters and 218B total parameters, it has 128 experts, out of which 8 are active per token, and a single shared expert is applied to all tokens. The attention layers interleave sliding-window attention layers with Rotational Positional Embeddings and global attention layers without positional embeddings in a 3:1 ratio, as first introduced in Command A. The sparse MoE layer is trained in a fully dropless manner and uses a token-choice router. We use additive-bias-based load balancing to encourage balanced token load across all experts, and swap out the softmax router activation function with a normalized sigmoid over the topk expert logits per token. 

**Languages covered:** The model has been trained on 48 languages: English, Arabic, Bulgarian, Bengali, Catalan, Czech, Danish, German, Greek, Spanish, Estonian, Persian, Finnish, Filipino, French, Irish, Hebrew, Hindi, Croatian, Hungarian, Indonesian, Icelandic, Italian, Japanese, Korean, Lithuanian, Latvian, Malay, Maltese, Dutch, Norwegian, Punjabi, Polish, Portuguese, Romanian, Russian, Slovak, Slovenian, Serbian, Swedish, Tamil, Telugu, Thai, Turkish, Ukrainian, Urdu, Vietnamese, Chinese.

**Context Length:** Command A+ supports a context length of 128K & 64K output length.

### **Tool Use Capabilities:**

Command A+ has been specifically trained with conversational tool use capabilities. This allows the model to interact with external tools like APIs, databases, or search engines.

Tool use with Command A+ is supported through [chat templates](https://huggingface.co/docs/transformers/main/en/chat_templating#advanced-tool-use--function-calling) in Transformers. We recommend providing tool descriptions using JSON schema.

<details>
<summary><b>Tool Use Example [CLICK TO EXPAND]</b></summary>

```py
from transformers import AutoTokenizer

model_id = "CohereLabs/command-a-plus-05-2026-bf16"
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Define tools
tools = [{
    "type": "function",
    "function": {
        "name": "query_daily_sales_report",
        "description": "Connects to a database to retrieve overall sales volumes and sales information for a given day.",
        "parameters": {
            "type": "object",
            "properties": {
                "day": {
                    "description": "Retrieves sales data for this day, formatted as YYYY-MM-DD.",
                    "type": "string",
                }
            },
            "required": ["day"],
        },
    },
}]

# Define conversation input
conversation = [
    {"role": "user", "content": "Can you provide a sales summary for 29th September 2023?"}
]

# Tokenize the Tool Use prompt directly
input_ids = tokenizer.apply_chat_template(
    conversation=conversation,
    tools=tools,
    tokenize=True,
    add_generation_prompt=True,
    return_tensors="pt",
)
```

You can then generate from this input as normal.

If the model generates a plan and tool calls, you should add them to the chat history like so:

```py
tool_call = {"name": "query_daily_sales_report", "arguments": {"day": "2023-09-29"}}
thinking = "I will use the query_daily_sales_report tool to find the sales summary for 29th September 2023."
conversation.append({"role": "assistant", "tool_calls": [{"id": "0", "type": "function", "function": tool_call}], "thinking": thinking})
```

and then call the tool and append the result, as a dictionary, with the tool role, like so:

```py
api_response_query_daily_sales_report = {"date": "2023-09-29", "summary": "Total Sales Amount: 10000, Total Units Sold: 250"} # this needs to be a dictionary!!

# Append tool results
conversation.append({"role": "tool", "tool_call_id": "0", "content": api_response_query_daily_sales_report})
```

After that, you can generate() again to let the model use the tool result in the chat.

Note that this was a very brief introduction to tool calling \- for more information, see the Transformers [tool use documentation](https://huggingface.co/docs/transformers/main/chat_templating#advanced-tool-use--function-calling).
</details>

<details>
<summary><b>Tool Use With Citations [CLICK TO EXPAND]</b></summary>

Optionally, one can ask the model to include grounding spans (citations) in its response to indicate the source of the information, by using `enable_citations=True` in `tokenizer.apply_chat_template(*)`. The generation would look like this:

```
On 29th September 2023, the total sales amount was <co>10000</co: 0:[0]> and the total units sold were <co>250.</co: 0:[0]>
```

When citations are turned on, the model associates pieces of texts (called "spans") with those specific tool results that support them (called "sources"). Command A+ uses a pair of tags `<co>` and `</co>` to indicate when a span can be grounded onto a list of sources, listing them out in the closing tag. For example, `<co>span</co: 0:[1,2],1:[0]>` means that "span" is supported by result 1 and 2 from `tool_call_id=0` as well as result 0 from `tool_call_id=1`. Sources from the same tool call are grouped together and listed as `{tool_call_id}:[{list of result indices}]`, before they are joined together by ",".
</details>


## **Model Card Contact**

For errors or additional questions about details in this model card, contact \[[labs@cohere.com](mailto:labs@cohere.com)\].

**Try it now:**

You can try Command A+ in the [playground](https://dashboard.cohere.com/playground/chat?model=command-a-plus-05-2026). You can also use it in our dedicated [Hugging Face Space](https://huggingface.co/spaces/CohereLabs/command-a-plus-05-2026).