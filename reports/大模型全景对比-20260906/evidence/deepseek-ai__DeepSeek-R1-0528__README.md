---
license: mit
library_name: transformers
---
# DeepSeek-R1-0528
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
    <img alt="Chat" src="https://img.shields.io/badge/🤖%20Chat-DeepSeek%20R1-536af5?color=536af5&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
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
  <a href="https://arxiv.org/pdf/2501.12948"><b>Paper Link</b>👁️</a>
</p>


## 1. Introduction

The DeepSeek R1 model has undergone a minor version upgrade, with the current version being DeepSeek-R1-0528. In the latest update, DeepSeek R1 has significantly improved its depth of reasoning and inference capabilities by leveraging increased computational resources and introducing algorithmic optimization mechanisms during post-training. The model has demonstrated outstanding performance across various benchmark evaluations, including mathematics, programming, and general logic. Its overall performance is now approaching that of leading models, such as O3 and Gemini 2.5 Pro.

<p align="center">
  <img width="80%" src="figures/benchmark.png">
</p>

Compared to the previous version, the upgraded model shows significant improvements in handling complex reasoning tasks. For instance, in the AIME 2025 test, the model’s accuracy has increased from 70% in the previous version to 87.5% in the current version. This advancement stems from enhanced thinking depth during the reasoning process: in the AIME test set, the previous model used an average of 12K tokens per question, whereas the new version averages 23K tokens per question.

Beyond its improved reasoning capabilities, this version also offers a reduced hallucination rate, enhanced support for function calling, and better experience for vibe coding.

## 2. Evaluation Results

### DeepSeek-R1-0528
 For all our models, the maximum generation length is set to 64K tokens. For benchmarks requiring sampling, we use a temperature of $0.6$, a top-p value of $0.95$, and generate 16 responses per query to estimate pass@1.
<div align="center">

| Category | Benchmark (Metric)               | DeepSeek R1     | DeepSeek R1 0528
|----------|----------------------------------|-----------------|---|
| General  |
|          | MMLU-Redux (EM)                   | 92.9            | 93.4
|          | MMLU-Pro (EM)                     | 84.0            | 85.0
|          | GPQA-Diamond (Pass@1)             | 71.5            | 81.0
|          | SimpleQA (Correct)                | 30.1            | 27.8
|          | FRAMES (Acc.)                     | 82.5            | 83.0
|          | Humanity's Last Exam (Pass@1)                     | 8.5            | 17.7
| Code |
|          | LiveCodeBench (2408-2505) (Pass@1)        | 63.5          | 73.3
|          | Codeforces-Div1 (Rating)          | 1530            | 1930
|          | SWE Verified (Resolved)           | 49.2            | 57.6
|          | Aider-Polyglot (Acc.)             | 53.3            | 71.6
| Math |
|          | AIME 2024 (Pass@1)                | 79.8            | 91.4
|          | AIME 2025 (Pass@1)                     | 70.0           | 87.5
|          | HMMT 2025 (Pass@1)            | 41.7 | 79.4 |
|          | CNMO 2024 (Pass@1)                | 78.8            | 86.9
| Tools |
|          | BFCL_v3_MultiTurn (Acc)     | -            | 37.0 |
|          | Tau-Bench   (Pass@1)       | -            | 53.5(Airline)/63.9(Retail)

</div>
Note: We use Agentless framework to evaluate model performance on SWE-Verified. We only evaluate text-only prompts in HLE testsets.  GPT-4.1 is employed to act user role in Tau-bench evaluation.

### DeepSeek-R1-0528-Qwen3-8B
Meanwhile, we distilled the chain-of-thought from DeepSeek-R1-0528 to post-train Qwen3 8B Base, obtaining DeepSeek-R1-0528-Qwen3-8B. This model achieves state-of-the-art (SOTA) performance among open-source models on the AIME 2024, surpassing Qwen3 8B by +10.0% and matching the performance of Qwen3-235B-thinking. We believe that the chain-of-thought from DeepSeek-R1-0528 will hold significant importance for both academic research on reasoning models and industrial development focused on small-scale models.

|                                | AIME 24 | AIME 25 | HMMT Feb 25 | GPQA Diamond | LiveCodeBench (2408-2505) |
|--------------------------------|---------|---------|-------------|--------------|---------------------------|
| Qwen3-235B-A22B	                | 85.7    | 81.5    | 62.5        | 71.1         | 66.5                  |
| Qwen3-32B                      | 81.4    | 72.9    | -           | 68.4         | -                         |
| Qwen3-8B                      | 76.0   | 67.3    | -           | 62.0       | -                         |
| Phi-4-Reasoning-Plus-14B       | 81.3    | 78.0    | 53.6        | 69.3         | -          |
| Gemini-2.5-Flash-Thinking-0520 | 82.3    | 72.0    | 64.2        | 82.8         | 62.3                  |
| o3-mini (medium)               | 79.6    | 76.7    | 53.3        | 76.8         | 65.9                     |
| DeepSeek-R1-0528-Qwen3-8B      | 86.0   | 76.3    | 61.5        | 61.1         | 60.5                      |

## 3. Chat Website & API Platform
You can chat with DeepSeek-R1 on DeepSeek's official website: [chat.deepseek.com](https://chat.deepseek.com/sign_in), and switch on the button "DeepThink"

We also provide OpenAI-Compatible API at DeepSeek Platform: [platform.deepseek.com](https://platform.deepseek.com/)

## 4. How to Run Locally

Please visit [DeepSeek-R1](https://github.com/deepseek-ai/DeepSeek-R1) repository for more information about running DeepSeek-R1-0528 locally.

Compared to previous versions of DeepSeek-R1, the usage recommendations for DeepSeek-R1-0528 have the following changes:

1. System prompt is supported now.
2. It is not required to add "\<think\>\n" at the beginning of the output to force the model into thinking pattern.

The model architecture of DeepSeek-R1-0528-Qwen3-8B is identical to that of Qwen3-8B, but it shares the same tokenizer configuration as DeepSeek-R1-0528. This model can be run in the same manner as Qwen3-8B.

### System Prompt
In the official DeepSeek web/app, we use the same system prompt with a specific date.
```
该助手为DeepSeek-R1，由深度求索公司创造。
今天是{current date}。
```
For example,
```
该助手为DeepSeek-R1，由深度求索公司创造。
今天是2025年5月28日，星期一。
```
### Temperature
In our web and application environments, the temperature parameter $T_{model}$ is set to 0.6. 
### Prompts for File Uploading and Web Search
For file uploading, please follow the template to create prompts, where {file_name}, {file_content} and {question} are arguments.
```
file_template = \
"""[file name]: {file_name}
[file content begin]
{file_content}
[file content end]
{question}"""
```
For Web Search, {search_results}, {cur_date}, and {question} are arguments.
For Chinese query, we use the prompt:
```
search_answer_zh_template = \
'''# 以下内容是基于用户发送的消息的搜索结果:
{search_results}
在我给你的搜索结果中，每个结果都是[webpage X begin]...[webpage X end]格式的，X代表每篇文章的数字索引。请在适当的情况下在句子末尾引用上下文。请按照引用编号[citation:X]的格式在答案中对应部分引用上下文。如果一句话源自多个上下文，请列出所有相关的引用编号，例如[citation:3][citation:5]，切记不要将引用集中在最后返回引用编号，而是在答案对应部分列出。
在回答时，请注意以下几点：
- 今天是{cur_date}。
- 并非搜索结果的所有内容都与用户的问题密切相关，你需要结合问题，对搜索结果进行甄别、筛选。
- 对于列举类的问题（如列举所有航班信息），尽量将答案控制在10个要点以内，并告诉用户可以查看搜索来源、获得完整信息。优先提供信息完整、最相关的列举项；如非必要，不要主动告诉用户搜索结果未提供的内容。
- 对于创作类的问题（如写论文），请务必在正文的段落中引用对应的参考编号，例如[citation:3][citation:5]，不能只在文章末尾引用。你需要解读并概括用户的题目要求，选择合适的格式，充分利用搜索结果并抽取重要信息，生成符合用户要求、极具思想深度、富有创造力与专业性的答案。你的创作篇幅需要尽可能延长，对于每一个要点的论述要推测用户的意图，给出尽可能多角度的回答要点，且务必信息量大、论述详尽。
- 如果回答很长，请尽量结构化、分段落总结。如果需要分点作答，尽量控制在5个点以内，并合并相关的内容。
- 对于客观类的问答，如果问题的答案非常简短，可以适当补充一到两句相关信息，以丰富内容。
- 你需要根据用户要求和回答内容选择合适、美观的回答格式，确保可读性强。
- 你的回答应该综合多个相关网页来回答，不能重复引用一个网页。
- 除非用户要求，否则你回答的语言需要和用户提问的语言保持一致。
# 用户消息为：
{question}'''
```
For English query, we use the prompt:
```
search_answer_en_template = \
'''# The following contents are the search results related to the user's message:
{search_results}
In the search results I provide to you, each result is formatted as [webpage X begin]...[webpage X end], where X represents the numerical index of each article. Please cite the context at the end of the relevant sentence when appropriate. Use the citation format [citation:X] in the corresponding part of your answer. If a sentence is derived from multiple contexts, list all relevant citation numbers, such as [citation:3][citation:5]. Be sure not to cluster all citations at the end; instead, include them in the corresponding parts of the answer.
When responding, please keep the following points in mind:
- Today is {cur_date}.
- Not all content in the search results is closely related to the user's question. You need to evaluate and filter the search results based on the question.
- For listing-type questions (e.g., listing all flight information), try to limit the answer to 10 key points and inform the user that they can refer to the search sources for complete information. Prioritize providing the most complete and relevant items in the list. Avoid mentioning content not provided in the search results unless necessary.
- For creative tasks (e.g., writing an essay), ensure that references are cited within the body of the text, such as [citation:3][citation:5], rather than only at the end of the text. You need to interpret and summarize the user's requirements, choose an appropriate format, fully utilize the search results, extract key information, and generate an answer that is insightful, creative, and professional. Extend the length of your response as much as possible, addressing each point in detail and from multiple perspectives, ensuring the content is rich and thorough.
- If the response is lengthy, structure it well and summarize it in paragraphs. If a point-by-point format is needed, try to limit it to 5 points and merge related content.
- For objective Q&A, if the answer is very brief, you may add one or two related sentences to enrich the content.
- Choose an appropriate and visually appealing format for your response based on the user's requirements and the content of the answer, ensuring strong readability.
- Your answer should synthesize information from multiple relevant webpages and avoid repeatedly citing the same webpage.
- Unless the user requests otherwise, your response should be in the same language as the user's question.
# The user's message is:
{question}'''
```

## 5. License
This code repository is licensed under [MIT License](LICENSE). The use of DeepSeek-R1 models is also subject to [MIT License](LICENSE). DeepSeek-R1 series (including Base and Chat) supports commercial use and distillation.

## 6. Citation
```
@misc{deepseekai2025deepseekr1incentivizingreasoningcapability,
      title={DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning}, 
      author={DeepSeek-AI},
      year={2025},
      eprint={2501.12948},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2501.12948}, 
}
```

## 7. Contact
If you have any questions, please raise an issue or contact us at [service@deepseek.com](service@deepseek.com).
