---
library_name: transformers
license: other
license_name: nvidia-open-model-license
license_link: >-
  https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/

pipeline_tag: text-generation
language:
  - en
tags:
  - nvidia
  - llama-3
  - pytorch
---

# Llama-3.1-Nemotron-Ultra-253B-v1

## Model Overview 

![Accuracy Plot](./accuracy_plot.png)

Llama-3.1-Nemotron-Ultra-253B-v1 is a large language model (LLM) which is a derivative of [Meta Llama-3.1-405B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-405B-Instruct) (AKA the *reference model*). It is a reasoning model that is post trained for reasoning, human chat preferences, and tasks, such as RAG and tool calling. The model supports a context length of 128K tokens. This model fits on a single 8xH100 node for inference.

Llama-3.1-Nemotron-Ultra-253B-v1 is a model which offers a great tradeoff between model accuracy and efficiency. Efficiency (throughput) directly translates to savings. Using a novel Neural Architecture Search (NAS) approach, we greatly reduce the model’s memory footprint, enabling larger workloads, as well as reducing the number of GPUs required to run the model in a data center environment. This NAS approach enables the selection of a desired point in the accuracy-efficiency tradeoff. Furthermore, by using a novel method to vertically compress the model (see details [here](https://arxiv.org/abs/2503.18908)), it also offers a significant improvement in latency.

The model underwent a multi-phase post-training process to enhance both its reasoning and non-reasoning capabilities. This includes a supervised fine-tuning stage for Math, Code, Reasoning, Chat, and Tool Calling as well as multiple reinforcement learning (RL) stages using Group Relative Policy Optimization (GRPO) algorithms for reasoning, chat, and instruction-following. 

This model is ready for commercial use. 

For more details on how the model was trained, please see our [technical report](https://arxiv.org/abs/2505.00949) and [blog](https://developer.nvidia.com/blog/build-enterprise-ai-agents-with-advanced-open-nvidia-llama-nemotron-reasoning-models/).

![Training Flow](./training_flowchart.png)

This model is part of the Llama Nemotron Collection. You can find the other model(s) in this family here: 

- [Llama-3.1-Nemotron-Nano-8B-v1](https://huggingface.co/nvidia/Llama-3.1-Nemotron-Nano-8B-v1)  
- [Llama-3.3-Nemotron-Super-49B-v1](https://huggingface.co/nvidia/Llama-3\_3-Nemotron-Super-49B-v1)

## Feature Voting

We want to hear from you! Share your ideas, vote on what matters, and help [shape the future of Nemotron](https://nemotron.ideas.nvidia.com/).


## License/Terms of Use

GOVERNING TERMS: Your use of this model is governed by the [NVIDIA Open Model License.](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/) Additional Information: [Llama 3.1 Community License Agreement](https://www.llama.com/llama3\_1/license/). Built with Llama.

**Model Developer:** NVIDIA

**Model Dates:** Trained between November 2024 and April 2025

**Data Freshness:**  The pretraining data has a cutoff of 2023 per Llama-3.1-405B-Instruct

### Use Case:
Developers designing AI Agent systems, chatbots, RAG systems, and other AI-powered applications. Also suitable for typical instruction-following tasks. 

### Release Date: 
2025-04-07

## References

* [\[2505.00949\] Llama-Nemotron: Efficient Reasoning Models](https://arxiv.org/abs/2505.00949)
* [\[2502.00203\] Reward-aware Preference Optimization: A Unified Mathematical Framework for Model Alignment](https://arxiv.org/abs/2502.00203)  
* [\[2411.19146\]Puzzle: Distillation-Based NAS for Inference-Optimized LLMs](https://arxiv.org/abs/2411.19146)  
* [\[2503.18908\]FFN Fusion: Rethinking Sequential Computation in Large Language Models](https://arxiv.org/abs/2503.18908)

## Model Architecture  
**Architecture Type:** Dense decoder-only Transformer model  
**Network Architecture:** Llama-3.1-405B-Instruct, customized through Neural Architecture Search (NAS)

**This model was developed based on Llama-3.1-405B-Instruct <br> 
** This model has 253B model parameters. <br> 

The model is a derivative of Llama 3.1-405B-Instruct, using Neural Architecture Search (NAS). The NAS algorithm results in non-standard and non-repetitive blocks. This includes the following: 

* Skip attention: In some blocks, the attention is skipped entirely, or replaced with a single linear layer.  
* Variable FFN: The expansion/compression ratio in the FFN layer is different between blocks.   
* FFN Fusion: When several consecutive attention layers are skipped, which can result in a sequence of multiple FFNs, that sequence of FFNs are fused into a smaller number of wider FFN layers.

For each block of the reference model, we create multiple variants providing different tradeoffs of quality vs. computational complexity, discussed in more depth below. We then search over the blocks to create a model which meets the required throughput and memory while minimizing the quality degradation. To recover performance, the model initially undergoes knowledge distillation (KD) for 65 billion tokens. This is followed by a continual pretraining (CPT) phase for 88 billion tokens.

## Intended use

Llama-3.1-Nemotron-Ultra-253B-v1 is a general purpose reasoning and chat model intended to be used in English and coding languages. Other non-English languages (German, French, Italian, Portuguese, Hindi, Spanish, and Thai) are also supported. 

## Input  
- **Input Type:** Text  
- **Input Format:** String  
- **Input Parameters:** One-Dimensional (1D)  
- **Other Properties Related to Input:** Context length up to 131,072 tokens

## Output  
- **Output Type:** Text  
- **Output Format:** String  
- **Output Parameters:** One-Dimensional (1D)  
- **Other Properties Related to Output:** Context length up to 131,072 tokens

## Software Integration  
- **Runtime Engine:** Transformers  
- **Recommended Hardware Microarchitecture Compatibility:**   
  - NVIDIA Hopper  
  - NVIDIA Ampere  
- **Preferred Operating System(s):** Linux 

## Model Version  
1.0 (4/7/2025)

## Quick Start and Usage Recommendations:

1. Reasoning mode (ON/OFF) is controlled via the system prompt, which must be set as shown in the example below. All instructions should be contained within the user prompt  
2. We recommend setting temperature to \`0.6\`, and Top P to \`0.95\` for Reasoning ON mode  
3. We recommend using greedy decoding (temperature 0\) for Reasoning OFF mode  
4. We do not recommend to add additional system prompts besides the control prompt, all instructions should be put into user query  
5. We have provided a list of prompts to use for evaluation for each benchmark where a specific template is required
6. The model will include `<think></think>` if no reasoning was necessary in Reasoning ON model, this is expected behaviour

You can try this model out through the preview API, using this link: [Llama-3\_1-Nemotron-Ultra-253B-v1](https://build.nvidia.com/nvidia/llama-3\_1-nemotron-ultra-253b-v1).

### Use It with Transformers
See the snippet below for usage with [Hugging Face Transformers](https://huggingface.co/docs/transformers/main/en/index) library. Reasoning mode (ON/OFF) is controlled via system prompt. Please see the example below

We recommend using the *transformers* package with version 4.48.3.   
Example of reasoning on:

```py
import torch
import transformers

model_id = "nvidia/Llama-3_1-Nemotron-Ultra-253B-v1"
model_kwargs = {"torch_dtype": torch.bfloat16, "trust_remote_code": True, "device_map": "auto"}
tokenizer = transformers.AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token_id = tokenizer.eos_token_id

pipeline = transformers.pipeline(
   "text-generation",
   model=model_id,
   tokenizer=tokenizer,
   max_new_tokens=32768,
   temperature=0.6,
   top_p=0.95,
   **model_kwargs
)

thinking = "on"


print(pipeline([{"role": "system", "content": f"detailed thinking {thinking}"},{"role": "user", "content": "Solve x*(sin(x)+2)=0"}]))
```

Example of reasoning off:

```py
import torch
import transformers

model_id = "nvidia/Llama-3_1-Nemotron-ULtra-253B-v1"
model_kwargs = {"torch_dtype": torch.bfloat16, "trust_remote_code": True, "device_map": "auto"}
tokenizer = transformers.AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token_id = tokenizer.eos_token_id

pipeline = transformers.pipeline(
   "text-generation",
   model=model_id,
   tokenizer=tokenizer,
   max_new_tokens=32768,
   do_sample=False,
   **model_kwargs
)

thinking = "off"


print(pipeline([{"role": "system", "content": f"detailed thinking {thinking}"},{"role": "user", "content": "Solve x*(sin(x)+2)=0"}]))
```

### Use It with vLLM

```
pip install vllm==0.8.3
```
An example on how to serve with vLLM:
```
python3 -m vllm.entrypoints.openai.api_server \
  --model "nvidia/Llama-3_1-Nemotron-Ultra-253B-v1" \
  --trust-remote-code \
  --seed=1 \
  --host="0.0.0.0" \
  --port=5000 \
  --served-model-name "nvidia/Llama-3_1-Nemotron-Ultra-253B-v1" \
  --tensor-parallel-size=8 \
  --max-model-len=32768 \
  --gpu-memory-utilization 0.95 \
  --enforce-eager
```
## Inference:  
**Engine:**

- Transformers

**Test Hardware:**  
- BF16:   
  - 8x NVIDIA H100-80GB   
  - 4x NVIDIA B100  
- FP 8  
  - 4x NVIDIA H100-80GB  
   
## Training and Evaluation Datasets

## Training Datasets

A large variety of training data was used for the knowledge distillation phase before post-training pipeline, 3 of which included: FineWeb, Buzz-V1.2, and Dolma.

The data for the multi-stage post-training phases is a compilation of SFT and RL data that supports improvements of math, code, general reasoning, and instruction following capabilities of the original Llama instruct model.

Prompts have been sourced from either public and open corpus or synthetically generated. Responses were synthetically generated by a variety of models, with some prompts containing responses for both reasoning on and off modes, to train the model to distinguish between two modes. This model was improved with Qwen.

We have released our [Llama-Nemotron-Post-Training-Dataset](https://huggingface.co/datasets/nvidia/Llama-Nemotron-Post-Training-Dataset) to promote openness and transparency in model development and improvement.

**Data Collection for Training Datasets:**

- Hybrid: Automated, Human, Synthetic

**Data Labeling for Training Datasets:**

- Hybrid: Automated, Human, Synthetic

## Evaluation Datasets 

We used the datasets listed in the next section to evaluate Llama-3.1-Nemotron-Ultra-253B-v1. 

Data Collection for Evaluation Datasets:

- Hybrid: Human/Synthetic

Data Labeling for Evaluation Datasets:

- Hybrid: Human/Synthetic/Automatic

## Evaluation Results  
*These results contain both Reasoning On, and Reasoning Off. We recommend using temperature=\`0.6\`, top\_p=\`0.95\` for Reasoning On mode, and greedy decoding for Reasoning Off mode. All evaluations are done with 32k sequence length. We run the benchmarks up to 16 times and average the scores to be more accurate.*  
 

> NOTE: Where applicable, a Prompt Template will be provided. While completing benchmarks, please ensure that you are parsing for the correct output format as per the provided prompt in order to reproduce the benchmarks seen below. 

### GPQA

| Reasoning Mode | pass@1 |
|--------------|------------|
| Reasoning Off | 56.60 | 
| Reasoning On | 76.01 |

User Prompt Template: 

```
"What is the correct answer to this question: {question}\nChoices:\nA. {option_A}\nB. {option_B}\nC. {option_C}\nD. {option_D}\nLet's think step by step, and put the final answer (should be a single letter A, B, C, or D) into a \boxed{}"
```

### AIME25

| Reasoning Mode | pass@1 |
|--------------|------------|
| Reasoning Off | 16.67 | 
| Reasoning On | 72.50 |

User Prompt Template: 

```
"Below is a math question. I want you to reason through the steps and then give a final answer. Your final answer should be in \boxed{}.\nQuestion: {question}"
```

### BFCL V2 Live

| Reasoning Mode | Score |
|--------------|------------|
| Reasoning Off | 73.62 |
| Reasoning On | 74.10 | 

User Prompt Template:

```
You are an expert in composing functions. You are given a question and a set of possible functions. 
Based on the question, you will need to make one or more function/tool calls to achieve the purpose. 
If none of the function can be used, point it out. If the given question lacks the parameters required by the function,
also point it out. You should only return the function call in tools call sections.

If you decide to invoke any of the function(s), you MUST put it in the format of <TOOLCALL>[func_name1(params_name1=params_value1, params_name2=params_value2...), func_name2(params)]</TOOLCALL>

You SHOULD NOT include any other text in the response.
Here is a list of functions in JSON format that you can invoke.

<AVAILABLE_TOOLS>{functions}</AVAILABLE_TOOLS>

{user_prompt}
```

### LiveCodeBench (20240801-20250201)

| Reasoning Mode | pass@1 |
|--------------|------------|
| Reasoning Off | 29.03 | 
| Reasoning On | 66.31 |

User Prompt Template (without starter code):

````
"You will be given a question (problem specification) and will generate a correct Python program that matches the specification and passes all tests.

Question: {prompt}

Read the inputs from stdin solve the problem and write the answer to stdout (do not directly test on the sample inputs). Enclose your code within delimiters as follows. Ensure that when the python program runs, it reads the inputs, runs the algorithm and writes output to STDOUT.
```python
# YOUR CODE HERE
```
````

User Prompt Template (with starter code):

````
You will be given a question (problem specification) and will generate a correct Python program that matches the specification and passes all tests.

Question: {prompt}

You will use the following starter code to write the solution to the problem and enclose your code within delimiters.
```python
{starter_code}
```
````

### IFEval

| Reasoning Mode | Strict:Instruction |
|--------------|------------|
| Reasoning Off | 88.85 | 
| Reasoning On | 89.45 | 

### MATH500

| Reasoning Mode | pass@1 |
|--------------|------------|
| Reasoning Off | 80.40 | 
| Reasoning On | 97.00 |

User Prompt Template: 

```
"Below is a math question. I want you to reason through the steps and then give a final answer. Your final answer should be in \boxed{}.\nQuestion: {question}"
```

### JudgeBench

| Reasoning Mode | Knowledge Score | Reasoning Score | Math Score | Coding Score | Overall Score | 
|--------------|------------|------------|------------|------------|------------|
| Reasoning On | 70.13 | 81.63 | 89.29 | 92.86 | 79.14 | 

## Ethical Considerations:

NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications.  When downloaded or used in accordance with our terms of service, developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse. 

For more detailed information on ethical considerations for this model, please see the Model Card++ [Explainability](./EXPLAINABILITY.md), [Bias](./BIAS.md), [Safety & Security](./SAFETY_and_SECURITY.md), and [Privacy](./PRIVACY.md) Subcards.

Please report security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

## Citation
```
@misc{bercovich2025llamanemotronefficientreasoningmodels,
      title={Llama-Nemotron: Efficient Reasoning Models}, 
      author={Akhiad Bercovich and Itay Levy and Izik Golan and Mohammad Dabbah and Ran El-Yaniv and Omri Puny and Ido Galil and Zach Moshe and Tomer Ronen and Najeeb Nabwani and Ido Shahaf and Oren Tropp and Ehud Karpas and Ran Zilberstein and Jiaqi Zeng and Soumye Singhal and Alexander Bukharin and Yian Zhang and Tugrul Konuk and Gerald Shen and Ameya Sunil Mahabaleshwarkar and Bilal Kartal and Yoshi Suhara and Olivier Delalleau and Zijia Chen and Zhilin Wang and David Mosallanezhad and Adi Renduchintala and Haifeng Qian and Dima Rekesh and Fei Jia and Somshubra Majumdar and Vahid Noroozi and Wasi Uddin Ahmad and Sean Narenthiran and Aleksander Ficek and Mehrzad Samadi and Jocelyn Huang and Siddhartha Jain and Igor Gitman and Ivan Moshkov and Wei Du and Shubham Toshniwal and George Armstrong and Branislav Kisacanin and Matvei Novikov and Daria Gitman and Evelina Bakhturina and Jane Polak Scowcroft and John Kamalu and Dan Su and Kezhi Kong and Markus Kliegl and Rabeeh Karimi and Ying Lin and Sanjeev Satheesh and Jupinder Parmar and Pritam Gundecha and Brandon Norick and Joseph Jennings and Shrimai Prabhumoye and Syeda Nahida Akter and Mostofa Patwary and Abhinav Khattar and Deepak Narayanan and Roger Waleffe and Jimmy Zhang and Bor-Yiing Su and Guyue Huang and Terry Kong and Parth Chadha and Sahil Jain and Christine Harvey and Elad Segal and Jining Huang and Sergey Kashirsky and Robert McQueen and Izzy Putterman and George Lam and Arun Venkatesan and Sherry Wu and Vinh Nguyen and Manoj Kilaru and Andrew Wang and Anna Warno and Abhilash Somasamudramath and Sandip Bhaskar and Maka Dong and Nave Assaf and Shahar Mor and Omer Ullman Argov and Scot Junkin and Oleksandr Romanenko and Pedro Larroy and Monika Katariya and Marco Rovinelli and Viji Balas and Nicholas Edelman and Anahita Bhiwandiwalla and Muthu Subramaniam and Smita Ithape and Karthik Ramamoorthy and Yuting Wu and Suguna Varshini Velury and Omri Almog and Joyjit Daw and Denys Fridman and Erick Galinkin and Michael Evans and Katherine Luna and Leon Derczynski and Nikki Pope and Eileen Long and Seth Schneider and Guillermo Siman and Tomasz Grzegorzek and Pablo Ribalta and Monika Katariya and Joey Conway and Trisha Saar and Ann Guan and Krzysztof Pawelec and Shyamala Prayaga and Oleksii Kuchaiev and Boris Ginsburg and Oluwatobi Olabiyi and Kari Briski and Jonathan Cohen and Bryan Catanzaro and Jonah Alben and Yonatan Geifman and Eric Chung and Chris Alexiuk},
      year={2025},
      eprint={2505.00949},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2505.00949}, 
}
```