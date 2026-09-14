---

language:
  - en
  - ko
  - es
  - de
  - ja
  - vi
  - fr
  - it
  - pl
  - pt
license: apache-2.0
license_link: LICENSE
library_name: transformers
pipeline_tag: text-generation
tags:
  - lg-ai
  - exaone
  - k-exaone
  - moe
---

# K-EXAONE-2.0-750B-A37B
<br>
<br>
<p align="center">
<img src="assets/K-EXAONE_logo_gray.png" width="400">
<br>
<br>
<br>

<div align="center">
  <a href="https://huggingface.co/collections/LGAI-EXAONE/k-exaone-20" style="text-decoration: none;">
    <img src="https://img.shields.io/badge/🤗-HuggingFace-FC926C?style=for-the-badge" alt="HuggingFace">
  </a>
  <a href="https://www.lgresearch.ai/news/view?seq=678" style="text-decoration: none;">
    <img src="https://img.shields.io/badge/📝-Blog-E343BD?style=for-the-badge" alt="Blog">
  </a>
  <a href="https://huggingface.co/papers/2608.04505" style="text-decoration: none;">
    <img src="https://img.shields.io/badge/📑-Technical_Report-684CF4?style=for-the-badge" alt="Technical Report">
  </a>
  <a href="https://github.com/LG-AI-EXAONE/K-EXAONE-2.0" style="text-decoration: none;">
    <img src="https://img.shields.io/badge/🖥️-GitHub-2B3137?style=for-the-badge" alt="GitHub">
  </a>
  <a href="https://friendli.ai/models/LGAI-EXAONE/K-EXAONE-2.0-750B-A37B" style="text-decoration: none;">
    <img src="https://img.shields.io/badge/✈️_API-FriendliAI-2649BC?style=for-the-badge" alt="FriendliAI">
  </a>
</div>



<div align="center">
<table><tr><td><span style="color: orange"> <b>Try K-EXAONE 2.0 now</b>! </span> <a href="https://k.exaone.ai/" style="text-decoration: none;"> ➡️ Open Demo</a> </td></tr></table>
</div>

## Introduction

We introduce **K-EXAONE 2.0**, a frontier-scale multilingual language model developed by LG AI Research. K-EXAONE 2.0 was scaled to more than three times the size of its predecessor through upcycling, followed by continual pretraining, difficulty-focused mid-training, and post-training. 
K-EXAONE 2.0 is broadly competitive with leading open-weight models, demonstrating substantial improvements over its predecessor and achieving particularly strong results in long-context retrieval and safety.

#### Highlights

- **Frontier-Class Scale**
To build a large-scale foundation model with frontier-level intelligence, we upcycled the [K-EXAONE](https://huggingface.co/collections/LGAI-EXAONE/k-exaone) model by expanding both its depth and width, resulting in a more favorable scaling curve. During this process, we found that clamping after two SwiGLU branches effectively mitigates the exploding activations in deeper layers, improving both training and inference stability.

- **Advanced Reasoning & Agentic Intelligence**
In response to the growth of agentic AI, we focused on expanding the model's capabilities in reasoning, agentic workflows, and long-context management. Through careful calibration of the training data and recipes, K-EXAONE 2.0 achieves consistent improvements in agentic coding and long-context understanding, with strong performance on long-context retrieval and safety.

- **Production-Ready Inference**
We support two speculative decoding methods to accelerate inference: MTP (Multi-Token Prediction) and DSpark. Both methods can speed up model generation by approximately 3–5×, reducing latency for long-horizon workloads such as agentic tasks.

- **Multilinguality & Openness**
We expanded multilingual coverage from six to ten languages: Korean, English, Spanish, German, Japanese, Vietnamese, French, Italian, Polish, and Portuguese. We also release K-EXAONE 2.0 under the [Apache license 2.0](https://huggingface.co/LGAI-EXAONE/K-EXAONE-2.0-750B-A37B/blob/main/LICENSE) so that the broader AI ecosystem can inspect, deploy, and build upon it.

![](assets/main_figure.png)

## Model Configurations

<div>
<table>
	<tr>
		<td align="center" style="vertical-align: middle; text-align: center"><strong>Number of Parameters</strong></td>
		<td align="center" style="vertical-align: middle; text-align: center">750B</td>
	</tr>
	<tr>
		<td align="center" style="vertical-align: middle; text-align: center"><strong>Active Parameters</strong></td>
		<td align="center" style="vertical-align: middle; text-align: center">37B</td>
	</tr>
	<tr>
		<td align="center" style="vertical-align: middle; text-align: center"><strong>Hidden Dimension</strong></td>
		<td align="center" style="vertical-align: middle; text-align: center">6,144</td>
	</tr>
	<tr>
		<td align="center" style="vertical-align: middle; text-align: center"><strong>Intermediate Size</strong></td>
		<td align="center" style="vertical-align: middle; text-align: center">18,432</td>
	</tr>
	<tr>
		<td align="center" style="vertical-align: middle; text-align: center"><strong>Number of Layers</strong></td>
		<td align="center" style="vertical-align: middle; text-align: center">78 (2 heading Dense + 76 Sparse) Main layers<br>
1 MTP layers<br>
</td>
	</tr>
	<tr>
		<td align="center" style="vertical-align: middle; text-align: center"><strong>Attention</strong></td>
		<td align="center" style="vertical-align: middle; text-align: center">1 x Global (NoPE)<br>
1 x 4096 SWA<br>
19 x [3 x 128 SWA + 1 x Global] Blocks
</td>
	</tr>
	<tr>
		<td align="center" style="vertical-align: middle; text-align: center"><strong>Attention Heads</strong></td>
		<td align="center" style="vertical-align: middle; text-align: center">64 Q-heads / 8 KV-heads</td>
	</tr>
	<tr>
		<td align="center" style="vertical-align: middle; text-align: center"><strong>Head Dimension</strong></td>
		<td align="center" style="vertical-align: middle; text-align: center">128</td>
	</tr>
	<tr>
		<td align="center" style="vertical-align: middle; text-align: center"><strong>Number of Experts</strong></td>
		<td align="center" style="vertical-align: middle; text-align: center">1 Shared Expert<br>
256 Total Experts<br>
8 Activated Experts
</td>
	</tr>
	<tr>
		<td align="center" style="vertical-align: middle; text-align: center"><strong>Expert Dimension</strong></td>
		<td align="center" style="vertical-align: middle; text-align: center">2,048</td>
	</tr>
	<tr>
		<td align="center" style="vertical-align: middle; text-align: center"><strong>Vocab Size</strong></td>
		<td align="center" style="vertical-align: middle; text-align: center">153,600</td>
	</tr>
	<tr>
		<td align="center" style="vertical-align: middle; text-align: center"><strong>Context Length</strong></td>
		<td align="center" style="vertical-align: middle; text-align: center">262,144</td>
	</tr>
	<tr>
		<td align="center" style="vertical-align: middle; text-align: center"><strong>Knowledge Cutoff</strong></td>
		<td align="center" style="vertical-align: middle; text-align: center">2025 2Q</td>
	</tr>

</table>
</div>

## Evaluation Results

The following table shows the benchmark results for the K-EXAONE 2.0 BF16 model.
Detailed evaluation results and configurations can be found in our [technical report](https://huggingface.co/papers/2608.04505).

<table>
	<tr>
		<th align="center" style="vertical-align: middle; text-align: center; background: rgba(128,128,128,0.1); text-align: center;"> </th>
		<th align="center" style="vertical-align: middle; text-align: center; background: rgba(128,128,128,0.1); text-align: center;">K-EXAONE 2.0</th>
		<th align="center" style="vertical-align: middle; text-align: center; background: rgba(128,128,128,0.1); text-align: center;">K-EXAONE</th>
		<th align="center" style="vertical-align: middle; text-align: center; background: rgba(128,128,128,0.1); text-align: center;">Qwen3.5</th>
		<th align="center" style="vertical-align: middle; text-align: center; background: rgba(128,128,128,0.1); text-align: center;">GLM-5.1</th>
		<th align="center" style="vertical-align: middle; text-align: center; background: rgba(128,128,128,0.1); text-align: center;">DSV4 Pro&nbsp;(max)</th>
	</tr>
	<tr>
		<td>Architecture</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">MoE</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">MoE</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">MoE</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">MoE</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">MoE</td>
	</tr>
	<tr>
		<td>Total Params</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">750B</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">236B</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">397B</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">754B</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">1.6T</td>
	</tr>
	<tr>
		<td>Active Params</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">37B</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">23B</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">17B</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">40B</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">49B</td>
	</tr>
	<tr>
		<td align="center" style="vertical-align: middle; text-align: center; background: linear-gradient(90deg, rgba(252,146,108,0.3) 0%, rgba(227,67,189,0.3) 50%, rgba(104,76,244,0.3) 100%); font-weight: bold; height:32px; padding-top:2px; padding-bottom:2px;" colspan='7'><i>World Knowledge</i></td>
	</tr>
	<tr>
		<td>MMLU-Pro</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">83.5</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">83.8</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">89.8</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">86.0</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">87.5</td>
	</tr>
	<tr>
		<td>GPQA-Diamond</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">82.2</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">79.1</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">88.4</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">86.2</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">90.1</td>
	</tr>
	<tr>
		<td>Humanity's Last Exam</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">18.3</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">13.6</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">28.7</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">31.0</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">37.7</td>
	</tr>
	<tr>
		<td align="center" style="vertical-align: middle; text-align: center; background: linear-gradient(90deg, rgba(252,146,108,0.3) 0%, rgba(227,67,189,0.3) 50%, rgba(104,76,244,0.3) 100%); font-weight: bold; height:32px; padding-top:2px; padding-bottom:2px;" colspan='7'><i>Math</i></td>
	</tr>
	<tr>
		<td>AIME 2026</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">92.3</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">92.2</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">91.3</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">95.3</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">95.2</td>
	</tr>
	<tr>
		<td>HMMT Feb 2026</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">78.4</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">80.7</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">84.6</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">82.6</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">95.2</td>
	</tr>
	<tr>
		<td>IMO Answer</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">78.6</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">76.3</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">80.9</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">83.8</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">89.8</td>
	</tr>
	<tr>
		<td align="center" style="vertical-align: middle; text-align: center; background: linear-gradient(90deg, rgba(252,146,108,0.3) 0%, rgba(227,67,189,0.3) 50%, rgba(104,76,244,0.3) 100%); font-weight: bold; height:32px; padding-top:2px; padding-bottom:2px;" colspan='7'><i>Coding / Agentic Coding</i></td>
	</tr>
	<tr>
		<td>SciCode</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">37.4</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">35.6</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">42.0</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">43.8</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">50.0</td>
	</tr>
	<tr>
		<td>SWE Bench Verified</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">68.2</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">49.4</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">76.4</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">73.6</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">80.6</td>
	</tr>
	<tr>
		<td>Terminal-Bench 2.1</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">43.8</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">30.3</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">51.3</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">61.8</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">64.0</td>
	</tr>
	<tr>
		<td align="center" style="vertical-align: middle; text-align: center; background: linear-gradient(90deg, rgba(252,146,108,0.3) 0%, rgba(227,67,189,0.3) 50%, rgba(104,76,244,0.3) 100%); font-weight: bold; height:32px; padding-top:2px; padding-bottom:2px;" colspan='7'><i>Agentic Tool Use</i></td>
	</tr>
	<tr>
		<td>τ<sup>3</sup>-Banking</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">14.2</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">14.2</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">13.4</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">11.5</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">25.8</td>
	</tr>
	<tr>
		<td>Claw-Eval</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">77.7</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">70.3</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">79.7</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">84.4</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">82.7</td>
	</tr>
	<tr>
		<td align="center" style="vertical-align: middle; text-align: center; background: linear-gradient(90deg, rgba(252,146,108,0.3) 0%, rgba(227,67,189,0.3) 50%, rgba(104,76,244,0.3) 100%); font-weight: bold; height:32px; padding-top:2px; padding-bottom:2px;" colspan='7'><i>Instruction Following</i></td>
	</tr>
	<tr>
		<td>IFEval</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">92.4</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">89.7</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">92.6</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">93.9</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">94.0</td>
	</tr>
	<tr>
		<td>IFBench</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">72.6</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">67.3</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">76.5</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">76.3</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">76.5</td>
	</tr>
	<tr>
		<td align="center" style="vertical-align: middle; text-align: center; background: linear-gradient(90deg, rgba(252,146,108,0.3) 0%, rgba(227,67,189,0.3) 50%, rgba(104,76,244,0.3) 100%); font-weight: bold; height:32px; padding-top:2px; padding-bottom:2px;" colspan='7'><i>Long Context Understanding</i></td>
	</tr>
	<tr>
		<td>OpenAI-MRCR</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">94.4</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">52.3</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">93.0</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">71.5</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">92.9</td>
	</tr>
	<tr>
		<td>AA-LCR</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">56.2</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">53.5</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">65.7</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">62.3</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">66.3</td>
	</tr>
	<tr>
		<td>Ko-LongBench</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">89.6</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">86.8</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">91.3</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">83.6</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">91.4</td>
	</tr>
	<tr>
		<td align="center" style="vertical-align: middle; text-align: center; background: linear-gradient(90deg, rgba(252,146,108,0.3) 0%, rgba(227,67,189,0.3) 50%, rgba(104,76,244,0.3) 100%); font-weight: bold; height:32px; padding-top:2px; padding-bottom:2px;" colspan='7'><i>Korean</i></td>
	</tr>
	<tr>
		<td>KMMLU-Pro</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">69.1</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">67.3</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">77.4</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">75.8</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">80.5</td>
	</tr>
	<tr>
		<td>Click</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">84.2</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">83.9</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">88.9</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">88.7</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">91.6</td>
	</tr>
	<tr>
		<td>HRM8K-KSM</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">91.1</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">91.9</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">91.2</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">89.4</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">94.3</td>
	</tr>
	<tr>
		<td align="center" style="vertical-align: middle; text-align: center; background: linear-gradient(90deg, rgba(252,146,108,0.3) 0%, rgba(227,67,189,0.3) 50%, rgba(104,76,244,0.3) 100%); font-weight: bold; height:32px; padding-top:2px; padding-bottom:2px;" colspan='7'><i>Multilinguality</i></td>
	</tr>
	<tr>
		<td>MMMLU</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">86.6</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">86.2</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">90.6</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">89.7</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">89.6</td>
	</tr>
	<tr>
		<td>GlobalMMLU-Lite</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">86.6</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">86.9</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">92.1</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">90.7</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">92.0</td>
	</tr>
	<tr>
		<td>PolyMath</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">71.3</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">57.4</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">73.3</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">73.8</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">80.9</td>
	</tr>
	<tr>
		<td align="center" style="vertical-align: middle; text-align: center; background: linear-gradient(90deg, rgba(252,146,108,0.3) 0%, rgba(227,67,189,0.3) 50%, rgba(104,76,244,0.3) 100%); font-weight: bold; height:32px; padding-top:2px; padding-bottom:2px;" colspan='7'><i>Safety</i></td>
	</tr>
	<tr>
		<td>KGC-Safety</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">99.8</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">96.1</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">92.0</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">69.3</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">82.8</td>
	</tr>
	<tr>
		<td>ROK-Fortress</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">89.5</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">60.9</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">86.1</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">73.2</td>
		<td align="center" style="vertical-align: middle; text-align: center; ">47.6</td>
	</tr>
</table>



## Quickstart

### Serving K-EXAONE 2.0

### SGLang

Install SGLang from [our fork](https://github.com/lkm2835/sglang/tree/add-k-exaone2) as follows:
```bash
uv venv
source .venv/bin/activate
uv pip install git+https://github.com/lkm2835/sglang@add-k-exaone2
uv pip install git+https://github.com/nuxlear/transformers@add-k-exaone2
```

The following script shows how to serve K-EXAONE 2.0 with SGLang on two nodes of 8 x NVIDIA H200 GPUs.
Before starting the server, set `$HEAD_ADDR` to the IP address of the head (rank-0) node including the port number, and set `$NODE_RANK` to the number index of the node.

Run the one of the following scripts on every node, according to your purpose.

- Low latency
    ```bash
    sglang serve \
        --model-path LGAI-EXAONE/K-EXAONE-2.0-750B-A37B \
        --served-model-name K-EXAONE-2.0-750B-A37B \
        --tp 16 \
        --dist-init-addr $HEAD_ADDR \
        --nnodes 2 \
        --node-rank $NODE_RANK \
        --reasoning-parser qwen3 \
        --tool-call-parser qwen3_coder \
        --host 0.0.0.0 \
        --port 8000 \
        --max-running-requests 128 \
        --speculative-algo EAGLE \
        --speculative-num-steps 4 \
        --speculative-eagle-topk 1 \
        --speculative-num-draft-tokens 5 \
        --mem-fraction-static 0.875 \
        --swa-full-tokens-ratio 0.3
    ```

- High throughput
    ```bash
    sglang serve \
        --model-path LGAI-EXAONE/K-EXAONE-2.0-750B-A37B \
        --served-model-name K-EXAONE-2.0-750B-A37B \
        --tp 8 \
        --dp 2 \
        --enable-dp-attention \
        --dist-init-addr $HEAD_ADDR \
        --nnodes 2 \
        --node-rank $NODE_RANK \
        --reasoning-parser qwen3 \
        --tool-call-parser qwen3_coder \
        --host 0.0.0.0 \
        --port 8000 \
        --max-running-requests 192 \
        --cuda-graph-max-bs 96 \
        --speculative-algo EAGLE \
        --speculative-num-steps 4 \
        --speculative-eagle-topk 1 \
        --speculative-num-draft-tokens 5 \
        --mem-fraction-static 0.875 \
        --swa-full-tokens-ratio 0.3
    ```


> [!NOTE]
> If you are using NVIDIA B200 GPUs, please add the `--disable-prefill-cuda-graph` option to prevent issues with model generation collapse.
> We will update this note once these issues have been resolved.

### vLLM

You should install the vLLM library from [our fork](https://github.com/lkm2835/vllm/tree/add-k-exaone2) as below:
```bash
uv venv
source .venv/bin/activate
uv pip install git+https://github.com/lkm2835/vllm@add-k-exaone2 --torch-backend auto
uv pip install git+https://github.com/nuxlear/transformers@add-k-exaone2
```

The following script shows how to serve K-EXAONE 2.0 with vLLM on two nodes of 8 x NVIDIA H200 GPUs.
Before starting the server, set `$HEAD_IP` to the IP address of the head (rank-0) node, and set `$NODE_RANK` to the number index of the node.

Run the below script on every server.
```bash
HEADLESS_ARG=''
if [ \"\$NODE_RANK\" -ne 0 ]; then
    HEADLESS_ARG='--headless'
fi

exec vllm serve LGAI-EXAONE/K-EXAONE-2.0-750B-A37B \
    --served-model-name K-EXAONE-2.0-750B-A37B \
    --trust-remote-code \
    --tensor-parallel-size 16 \
    --distributed-executor-backend mp \
    --nnodes 2 \
    --node-rank $NODE_RANK \
    --master-addr $HEAD_IP \
    --master-addr 30000 \
    --gpu-memory-utilization 0.9 \
    --max-num-seqs 256 \
    --reasoning-parser qwen3 \
    --enable-auto-tool-choice \
    --tool-call-parser qwen3_xml \
    --host 0.0.0.0 \
    --port 8000 \
    --speculative_config '{
        "method": "mtp", 
        "num_speculative_tokens": 4
    }' \
    $HEADLESS_ARG
```

> [!NOTE]
> Currently, serving K-EXAONE 2.0 with DSpark is not supported on vLLM.
> We will update this note once these issues have been resolved.



### Using K-EXAONE 2.0

> [!IMPORTANT]
> To achieve the expected performance, we recommend using the following configurations:
> - We recommend using `temperature=1.0` and `top_p=0.95` for better output quality in most cases.
> - K-EXAONE 2.0 uses `enable_thinking=True` by default. Thus, you need to set `enable_thinking=False` to use non-reasoning mode.
> - We recommend using `preserve_thinking=True` in long-running tasks, such as agentic use or deep research.


Once K-EXAONE 2.0 is running on an inference engine, you can access it using the OpenAI Python SDK.

#### Reasoning mode

For tasks that require high accuracy, you can use the K-EXAONE 2.0 model in reasoning mode. The K-EXAONE 2.0 model supports the `preserve_thinking` option, which allows it to track previous `reasoning_content` across subsequent conversations. For agentic workflows, it is recommended to use `preserve_thinking=True`.

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY",
)

messages = [
    {
        "role": "user",
        "content": "Implement fibonacci with python code.",
    }
]

response = client.chat.completions.create(
    model="LGAI-EXAONE/K-EXAONE-2.0-750B-A37B",
    messages=messages,
    max_tokens=32768,
    temperature=1.0,
    top_p=0.95,
    extra_body={
        "chat_template_kwargs": {
            "enable_thinking": True,  # default: True
            "preserve_thinking": True,  # default: False
        }
    }, 
)
print(response)
```
#### Non-reasoning mode

For tasks where latency matters more than accuracy, you can run the K-EXAONE 2.0 model in non-reasoning mode. 

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY",
)

messages = [
    {
        "role": "user",
        "content": "Explain how useful you are.",
    }
]

response = client.chat.completions.create(
    model="LGAI-EXAONE/K-EXAONE-2.0-750B-A37B",
    messages=messages,
    max_tokens=32768,
    temperature=1.0,
    top_p=0.95,
    extra_body={
        "chat_template_kwargs": {
            "enable_thinking": False,  # default: True
            "preserve_thinking": False,  # default: False
        }
    }, 
)
print(response)
```
#### Tool calling

For your AI-powered agent, you can leverage K-EXAONE 2.0’s tool calling capability. 

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY",
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "roll_dice",
            "description": "Roll the dice with the number 1 to N. User can select the number N.",
            "parameters": {
                "type": "object",
                "properties": {
                    "max_num": {
                        "type": "integer",
                        "description": "The maximum number on the dice."
                    }
                },
                "required": ["max_num"]
            },
        },
    }
]

messages = [
    {
        "role": "user",
        "content": "Roll a D20 twice and sum the results."
    }
]

response = client.chat.completions.create(
    model="LGAI-EXAONE/K-EXAONE-2.0-750B-A37B",
    messages=messages,
    tools=tools,
    max_tokens=32768,
    temperature=1.0,
    top_p=0.95,
    extra_body={
        "chat_template_kwargs": {
            "enable_thinking": True,  # default: True
            "preserve_thinking": True,  # default: False
        }
    },
)

print(response)
```

### Agentic Use

You can leverage K-EXAONE 2.0’s agentic capabilities by integrating it with agent frameworks and harnesses.

#### OpenCode

To use the deployed K-EXAONE 2.0 model, you may need to update your `opencode.json` file. Below is an example JSON configuration for setting up a custom server as your model provider.

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "local": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Local OpenAI-compatible server",
      "options": {
        "baseURL": "http://localhost:8000/v1",
        "extraBody": {
          "chat_template_kwargs": {
            "enable_thinking": true,
            "preserve_thinking": true
          }
        }
      },
      "models": {
        "K-EXAONE-2": {
          "name": "K-EXAONE 2.0",
          "limit": {
            "context": 262144,
            "output": 32768
          }
        }
      }
    }
  }
}
```




## Limitation

K-EXAONE 2.0 language models, like all existing language models, have certain limitations and may occasionally generate inappropriate responses. The language model generates responses based on the output probability of tokens, and it is determined during learning from training data. While we make every effort to exclude personal, harmful, and biased information from the training data, some problematic content may still be included, potentially leading to undesirable responses. Please note that the text generated by K-EXAONE 2.0 language models does not reflect the views of LG AI Research.
- Inappropriate answers may be generated, which contain personal, harmful or other inappropriate information.
- Biased responses may be generated, which are associated with age, gender, race, and so on.
- The generated responses rely heavily on statistics from the training data, which can result in the generation of semantically or syntactically incorrect sentences.
- Since the models do not reflect the latest information, the responses may be false or contradictory.

LG AI Research strives to reduce potential risks that may arise from K-EXAONE 2.0 language models. Users are not allowed to engage in any malicious activities (e.g., keying in illegal information) that may induce the creation of inappropriate outputs violating LG AI’s ethical principles when using K-EXAONE 2.0 language models.

## License

The model is licensed under [Apache License 2.0](https://huggingface.co/LGAI-EXAONE/K-EXAONE-2.0-750B-A37B/blob/main/LICENSE).


## Citation

```
@article{k-exaone-2.0,
  title={K-EXAONE 2.0 Technical Report},
  author={{LG AI Research}},
  journal={arXiv preprint arXiv:2608.04505},
  year={2026}
}
```


## Contact

LG AI Research Technical Support: contact_us@lgresearch.ai

