---
tags:
- compressed-tensors
license: other
license_name: modified-mit
library_name: transformers
pipeline_tag: image-text-to-text
paper: arxiv.org/abs/2602.02276
---
<div align="center">
  <picture>
      <img src="figures/kimi-logo.png" width="30%" alt="Kimi K2.5">
  </picture>
</div>
<hr>
<div align="center" style="line-height:1">
  <a href="https://www.kimi.com" target="_blank"><img alt="Chat" src="https://img.shields.io/badge/🤖%20Chat-Kimi%20K2.5-ff6b6b?color=1783ff&logoColor=white"/></a>
  <a href="https://github.com/moonshotai/Kimi-K2.5"><img alt="github" src="https://img.shields.io/badge/Github-Kimi%20K2.5-181717?logo=github&color=1783ff&logoColor=white"/></a>
  <a href="https://www.moonshot.ai" target="_blank"><img alt="Homepage" src="https://img.shields.io/badge/Homepage-Moonshot%20AI-white?logo=Kimi&logoColor=white"/></a>
</div>

<div align="center" style="line-height: 1;">
  <a href="https://huggingface.co/moonshotai" target="_blank"><img alt="Hugging Face" src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Moonshot%20AI-ffc107?color=ffc107&logoColor=white"/></a>
  <a href="https://twitter.com/kimi_moonshot" target="_blank"><img alt="Twitter Follow" src="https://img.shields.io/badge/Twitter-Kimi.ai-white?logo=x&logoColor=white"/></a>
    <a href="https://discord.gg/TYU2fdJykW" target="_blank"><img alt="Discord" src="https://img.shields.io/badge/Discord-Kimi.ai-white?logo=discord&logoColor=white"/></a>
</div>
<div align="center" style="line-height: 1;">
  <a href="https://huggingface.co/moonshotai/Kimi-K2.5/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/badge/License-Modified_MIT-f5de53?&color=f5de53"/></a>
</div>
<p align="center">
<b>📰&nbsp;&nbsp;<a href="https://www.kimi.com/blog/kimi-k2-5.html">Tech Blog</a></b> &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp; <b>📄&nbsp;&nbsp;<a href="https://arxiv.org/abs/2602.02276">Paper</a></b>
</p>  
</p>

## 0. Changelog
- 2026.1.29: 
    - The default system prompt might cause confusion to users and unexpected behaviours, so we remove it.
    - The token `<|media_start|>` is incorrect; it has been replaced with `<|media_begin|>` in the chat template.

## 1. Model Introduction

Kimi K2.5 is an open-source, native multimodal agentic model built through continual pretraining on approximately 15 trillion mixed visual and text tokens atop Kimi-K2-Base. It seamlessly integrates vision and language understanding with advanced agentic capabilities, instant and thinking modes, as well as conversational and agentic paradigms.

### Key Features
- **Native Multimodality**: Pre-trained on vision–language tokens, K2.5 excels in visual knowledge, cross-modal reasoning, and agentic tool use grounded in visual inputs.
- **Coding with Vision**: K2.5 generates code from visual specifications (UI designs, video workflows) and autonomously orchestrates tools for visual data processing.
- **Agent Swarm**: K2.5 transitions from single-agent scaling to a self-directed, coordinated swarm-like execution scheme. It decomposes complex tasks into parallel sub-tasks executed by dynamically instantiated, domain-specific agents.

## 2. Model Summary

<div align="center">


| | |
|:---:|:---:|
| **Architecture** | Mixture-of-Experts (MoE) |
| **Total Parameters** | 1T |
| **Activated Parameters** | 32B |
| **Number of Layers** (Dense layer included) | 61 |
| **Number of Dense Layers** | 1 |
| **Attention Hidden Dimension** | 7168 |
| **MoE Hidden Dimension** (per Expert) | 2048 |
| **Number of Attention Heads** | 64 |
| **Number of Experts** | 384 |
| **Selected Experts per Token** | 8 |
| **Number of Shared Experts** | 1 |
| **Vocabulary Size** | 160K |
| **Context Length** | 256K |
| **Attention Mechanism** | MLA |
| **Activation Function** | SwiGLU |
| **Vision Encoder** | MoonViT |
| **Parameters of Vision Encoder** | 400M |
</div>

## 3. Evaluation Results



<div align="center">
<table>
<thead>
<tr>
<th align="center">Benchmark</th>
<th align="center"><sup>Kimi K2.5<br><sup>(Thinking)</sup></sup></th>
<th align="center"><sup>GPT-5.2 <br><sup>(xhigh)</sup></sup></th>
<th align="center"><sup>Claude 4.5 Opus <br><sup>(Extended Thinking)</sup></sup></th>
<th align="center"><sup>Gemini 3 Pro <br><sup>(High Thinking Level)</sup></sup></th>
<th align="center"><sup>DeepSeek V3.2 <br><sup>(Thinking)</sup></sup></th>
<th align="center"><sup>Qwen3-VL-<br>235B-A22B-<br>Thinking</sup></th>
</tr>
</thead>
<tbody>
<tr>
<td align="center" colspan=8><strong>Reasoning &amp; Knowledge</strong></td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">HLE-Full</td>
<td align="center" style="vertical-align: middle">30.1</td>
<td align="center" style="vertical-align: middle">34.5</td>
<td align="center" style="vertical-align: middle">30.8</td>
<td align="center" style="vertical-align: middle">37.5</td>
<td align="center" style="vertical-align: middle">25.1<sup>†</sup></td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">HLE-Full<br>(w/ tools)</td>
<td align="center" style="vertical-align: middle">50.2</td>
<td align="center" style="vertical-align: middle">45.5</td>
<td align="center" style="vertical-align: middle">43.2</td>
<td align="center" style="vertical-align: middle">45.8</td>
<td align="center" style="vertical-align: middle">40.8<sup>†</sup></td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">AIME 2025</td>
<td align="center" style="vertical-align: middle">96.1</td>
<td align="center" style="vertical-align: middle">100</td>
<td align="center" style="vertical-align: middle">92.8</td>
<td align="center" style="vertical-align: middle">95.0</td>
<td align="center" style="vertical-align: middle">93.1</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">HMMT 2025 (Feb)</td>
<td align="center" style="vertical-align: middle">95.4</td>
<td align="center" style="vertical-align: middle">99.4</td>
<td align="center" style="vertical-align: middle">92.9*</td>
<td align="center" style="vertical-align: middle">97.3*</td>
<td align="center" style="vertical-align: middle">92.5</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">IMO-AnswerBench</td>
<td align="center" style="vertical-align: middle">81.8</td>
<td align="center" style="vertical-align: middle">86.3</td>
<td align="center" style="vertical-align: middle">78.5*</td>
<td align="center" style="vertical-align: middle">83.1*</td>
<td align="center" style="vertical-align: middle">78.3</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">GPQA-Diamond</td>
<td align="center" style="vertical-align: middle">87.6</td>
<td align="center" style="vertical-align: middle">92.4</td>
<td align="center" style="vertical-align: middle">87.0</td>
<td align="center" style="vertical-align: middle">91.9</td>
<td align="center" style="vertical-align: middle">82.4</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">MMLU-Pro</td>
<td align="center" style="vertical-align: middle">87.1</td>
<td align="center" style="vertical-align: middle">86.7*</td>
<td align="center" style="vertical-align: middle">89.3*</td>
<td align="center" style="vertical-align: middle">90.1</td>
<td align="center" style="vertical-align: middle">85.0</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" colspan=8><strong>Image &amp; Video</strong></td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">MMMU-Pro</td>
<td align="center" style="vertical-align: middle">78.5</td>
<td align="center" style="vertical-align: middle">79.5*</td>
<td align="center" style="vertical-align: middle">74.0</td>
<td align="center" style="vertical-align: middle">81.0</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">69.3</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">CharXiv (RQ)</td>
<td align="center" style="vertical-align: middle">77.5</td>
<td align="center" style="vertical-align: middle">82.1</td>
<td align="center" style="vertical-align: middle">67.2*</td>
<td align="center" style="vertical-align: middle">81.4</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">66.1</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">MathVision</td>
<td align="center" style="vertical-align: middle">84.2</td>
<td align="center" style="vertical-align: middle">83.0</td>
<td align="center" style="vertical-align: middle">77.1*</td>
<td align="center" style="vertical-align: middle">86.1*</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">74.6</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">MathVista (mini)</td>
<td align="center" style="vertical-align: middle">90.1</td>
<td align="center" style="vertical-align: middle">82.8*</td>
<td align="center" style="vertical-align: middle">80.2*</td>
<td align="center" style="vertical-align: middle">89.8*</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">85.8</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">ZeroBench</td>
<td align="center" style="vertical-align: middle">9</td>
<td align="center" style="vertical-align: middle">9*</td>
<td align="center" style="vertical-align: middle">3*</td>
<td align="center" style="vertical-align: middle">8*</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">4*</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">ZeroBench<br>(w/ tools)</td>
<td align="center" style="vertical-align: middle">11</td>
<td align="center" style="vertical-align: middle">7*</td>
<td align="center" style="vertical-align: middle">9*</td>
<td align="center" style="vertical-align: middle">12*</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">3*</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">OCRBench</td>
<td align="center" style="vertical-align: middle">92.3</td>
<td align="center" style="vertical-align: middle">80.7*</td>
<td align="center" style="vertical-align: middle">86.5*</td>
<td align="center" style="vertical-align: middle">90.3*</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">87.5</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">OmniDocBench 1.5</td>
<td align="center" style="vertical-align: middle">88.8</td>
<td align="center" style="vertical-align: middle">85.7</td>
<td align="center" style="vertical-align: middle">87.7*</td>
<td align="center" style="vertical-align: middle">88.5</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">82.0*</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">InfoVQA (val)</td>
<td align="center" style="vertical-align: middle">92.6</td>
<td align="center" style="vertical-align: middle">84*</td>
<td align="center" style="vertical-align: middle">76.9*</td>
<td align="center" style="vertical-align: middle">57.2*</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">89.5</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">SimpleVQA</td>
<td align="center" style="vertical-align: middle">71.2</td>
<td align="center" style="vertical-align: middle">55.8*</td>
<td align="center" style="vertical-align: middle">69.7*</td>
<td align="center" style="vertical-align: middle">69.7*</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">56.8*</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle"><a href="https://github.com/MoonshotAI/WorldVQA">WorldVQA</a></td>
<td align="center" style="vertical-align: middle">46.3</td>
<td align="center" style="vertical-align: middle">28.0</td>
<td align="center" style="vertical-align: middle">36.8</td>
<td align="center" style="vertical-align: middle">47.4</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">23.5</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">VideoMMMU</td>
<td align="center" style="vertical-align: middle">86.6</td>
<td align="center" style="vertical-align: middle">85.9</td>
<td align="center" style="vertical-align: middle">84.4*</td>
<td align="center" style="vertical-align: middle">87.6</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">80.0</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">MMVU</td>
<td align="center" style="vertical-align: middle">80.4</td>
<td align="center" style="vertical-align: middle">80.8*</td>
<td align="center" style="vertical-align: middle">77.3</td>
<td align="center" style="vertical-align: middle">77.5</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">71.1</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">MotionBench</td>
<td align="center" style="vertical-align: middle">70.4</td>
<td align="center" style="vertical-align: middle">64.8</td>
<td align="center" style="vertical-align: middle">60.3</td>
<td align="center" style="vertical-align: middle">70.3</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">VideoMME</td>
<td align="center" style="vertical-align: middle">87.4</td>
<td align="center" style="vertical-align: middle">86.0*</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">88.4*</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">79.0</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">LongVideoBench</td>
<td align="center" style="vertical-align: middle">79.8</td>
<td align="center" style="vertical-align: middle">76.5*</td>
<td align="center" style="vertical-align: middle">67.2*</td>
<td align="center" style="vertical-align: middle">77.7*</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">65.6*</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">LVBench</td>
<td align="center" style="vertical-align: middle">75.9</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">73.5*</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">63.6</td>
</tr>
<tr>
<td align="center" colspan=8><strong>Coding</strong></td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">SWE-Bench Verified</td>
<td align="center" style="vertical-align: middle">76.8</td>
<td align="center" style="vertical-align: middle">80.0</td>
<td align="center" style="vertical-align: middle">80.9</td>
<td align="center" style="vertical-align: middle">76.2</td>
<td align="center" style="vertical-align: middle">73.1</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">SWE-Bench Pro</td>
<td align="center" style="vertical-align: middle">50.7</td>
<td align="center" style="vertical-align: middle">55.6</td>
<td align="center" style="vertical-align: middle">55.4*</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">SWE-Bench Multilingual</td>
<td align="center" style="vertical-align: middle">73.0</td>
<td align="center" style="vertical-align: middle">72.0</td>
<td align="center" style="vertical-align: middle">77.5</td>
<td align="center" style="vertical-align: middle">65.0</td>
<td align="center" style="vertical-align: middle">70.2</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">Terminal Bench 2.0</td>
<td align="center" style="vertical-align: middle">50.8</td>
<td align="center" style="vertical-align: middle">54.0</td>
<td align="center" style="vertical-align: middle">59.3</td>
<td align="center" style="vertical-align: middle">54.2</td>
<td align="center" style="vertical-align: middle">46.4</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">PaperBench</td>
<td align="center" style="vertical-align: middle">63.5</td>
<td align="center" style="vertical-align: middle">63.7*</td>
<td align="center" style="vertical-align: middle">72.9*</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">47.1</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">CyberGym</td>
<td align="center" style="vertical-align: middle">41.3</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">50.6</td>
<td align="center" style="vertical-align: middle">39.9*</td>
<td align="center" style="vertical-align: middle">17.3*</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">SciCode</td>
<td align="center" style="vertical-align: middle">48.7</td>
<td align="center" style="vertical-align: middle">52.1</td>
<td align="center" style="vertical-align: middle">49.5</td>
<td align="center" style="vertical-align: middle">56.1</td>
<td align="center" style="vertical-align: middle">38.9</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">OJBench (cpp)</td>
<td align="center" style="vertical-align: middle">57.4</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">54.6*</td>
<td align="center" style="vertical-align: middle">68.5*</td>
<td align="center" style="vertical-align: middle">54.7*</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">LiveCodeBench (v6)</td>
<td align="center" style="vertical-align: middle">85.0</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">82.2*</td>
<td align="center" style="vertical-align: middle">87.4*</td>
<td align="center" style="vertical-align: middle">83.3</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" colspan=8><strong>Long Context</strong></td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">Longbench v2</td>
<td align="center" style="vertical-align: middle">61.0</td>
<td align="center" style="vertical-align: middle">54.5*</td>
<td align="center" style="vertical-align: middle">64.4*</td>
<td align="center" style="vertical-align: middle">68.2*</td>
<td align="center" style="vertical-align: middle">59.8*</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">AA-LCR</td>
<td align="center" style="vertical-align: middle">70.0</td>
<td align="center" style="vertical-align: middle">72.3*</td>
<td align="center" style="vertical-align: middle">71.3*</td>
<td align="center" style="vertical-align: middle">65.3*</td>
<td align="center" style="vertical-align: middle">64.3*</td>
<td align="center" style="vertical-align: middle">-</td>
<tr>
<td align="center" colspan=8><strong>Agentic Search</strong></td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">BrowseComp</td>
<td align="center" style="vertical-align: middle">60.6</td>
<td align="center" style="vertical-align: middle" rowspan="2">65.8</td>
<td align="center" style="vertical-align: middle">37.0</td>
<td align="center" style="vertical-align: middle">37.8</td>
<td align="center" style="vertical-align: middle">51.4</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">BrowseComp<br>(w/ctx manage)</td>
<td align="center" style="vertical-align: middle">74.9</td>
<td align="center" style="vertical-align: middle">57.8</td>
<td align="center" style="vertical-align: middle">59.2</td>
<td align="center" style="vertical-align: middle">67.6</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">BrowseComp<br>(Agent Swarm)</td>
<td align="center" style="vertical-align: middle">78.4</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">WideSearch<br> (item-f1)</td>
<td align="center" style="vertical-align: middle">72.7</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">76.2*</td>
<td align="center" style="vertical-align: middle">57.0</td>
<td align="center" style="vertical-align: middle">32.5*</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">WideSearch<br> (item-f1 Agent Swarm)</td>
<td align="center" style="vertical-align: middle">79.0</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">DeepSearchQA</td>
<td align="center" style="vertical-align: middle">77.1</td>
<td align="center" style="vertical-align: middle">71.3*</td>
<td align="center" style="vertical-align: middle">76.1*</td>
<td align="center" style="vertical-align: middle">63.2*</td>
<td align="center" style="vertical-align: middle">60.9*</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">FinSearchCompT2&T3</td>
<td align="center" style="vertical-align: middle">67.8</td>
<td align="center" style="vertical-align: middle">-</td>
<td align="center" style="vertical-align: middle">66.2*</td>
<td align="center" style="vertical-align: middle">49.9</td>
<td align="center" style="vertical-align: middle">59.1*</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle">Seal-0</td>
<td align="center" style="vertical-align: middle">57.4</td>
<td align="center" style="vertical-align: middle">45.0</td>
<td align="center" style="vertical-align: middle">47.7*</td>
<td align="center" style="vertical-align: middle">45.5*</td>
<td align="center" style="vertical-align: middle">49.5*</td>
<td align="center" style="vertical-align: middle">-</td>
</tr>
</tbody>
</table>
</div>

<details>
<summary><b>Footnotes</b></summary>

1. General Testing Details
   - We report results for Kimi K2.5 and DeepSeek-V3.2 with thinking mode enabled, Claude Opus 4.5 with extended thinking mode, GPT-5.2 with xhigh reasoning effort, and Gemini 3 Pro with a high thinking level. For vision benchmarks, we additionally report results for Qwen3-VL-235B-A22B-Thinking.
   - Unless otherwise specified, all Kimi K2.5 experiments were conducted with temperature = 1.0, top-p = 0.95, and a context length of 256k tokens.
   - Benchmarks without publicly available scores were re-evaluated under the same conditions used for Kimi K2.5 and are marked with an asterisk (*).
   - We could not evaluate GPT-5.2 xhigh on all benchmarks due to service stability issues. For benchmarks that were not tested, we mark them as "-".
2. Text and Reasoning
   - HLE, AIME 2025, HMMT 2025 (Feb), and GPQA-Diamond were evaluated with a maximum completion budget of 96k tokens.
   - Results for AIME and HMMT are averaged over 32 runs (avg@32); GPQA-Diamond over 8 runs (avg@8).
   - For HLE, we report scores on the full set (text & image). Kimi K2.5 scores 31.5 (text) and 21.3 (image) without tools, and 51.8 (text) and 39.8 (image) with tools. The DeepSeek-V3.2 score corresponds to its text-only subset (marked with †) . Hugging Face access was blocked to prevent potential data leakage. HLE with tools uses simple context management: once the context exceeds a threshold, only the latest round of tool messages is retained.
3. Tool-Augmented / Agentic Search
   - Kimi K2.5 was equipped with search, code-interpreter, and web-browsing tools for HLE with tools and all agentic search benchmarks.
   - Except for BrowseComp (where K2.5 and DeepSeek-V3.2 used the discard-all strategy), no context management was applied, and tasks exceeding the supported context length were directly counted as failed.
   - The test system prompts emphasize deep and proactive tool use, instructing models to reason carefully, leverage tools, and verify uncertain information. Full prompts will be provided in the technical report.
   - Results for Seal-0 and WideSearch are averaged over four runs (avg@4).
4. Vision Benchmarks
   - Max-tokens = 64k, averaged over three runs (avg@3).
   - ZeroBench (w/ tools) uses max-tokens-per-step = 24k and max-steps = 30 for multi-step reasoning.
   - MMMU-Pro follows the official protocol, preserving input order and prepending images.
   - GPT-5.2-xhigh had ~10% failure rate (no output despite 3 retries), treated as incorrect; reported scores likely underestimate true performance.
   - WorldVQA, a benchmark designed to evaluate atomic vision-centric world knowledge. Access WorldVQA at https://github.com/MoonshotAI/WorldVQA.
   - OmniDocBench Score is computed as (1 − normalized Levenshtein distance) × 100, where a higher score denotes superior accuracy.
5. Coding Tasks
   - Terminal-Bench 2.0 scores were obtained with the default agent framework (Terminus-2) and the provided JSON parser. In our implementation, we evaluated Terminal-Bench 2.0 under non-thinking mode. This choice was made because our current context management strategy for the thinking mode is incompatible with Terminus-2.
   - For the SWE-Bench series of evaluations (including verified, multilingual, and pro), we used an internally developed evaluation framework. This framework includes a minimal set of tools—bash tool, createfile tool, insert tool, view tool, strreplace tool, and submit tool—along with tailored system prompts designed for the tasks. The highest scores were achieved under non-thinking mode.
   - The score of Claude Opus 4.5 on CyberGym is reported under the non-thinking setting.
   - All reported scores of coding tasks are averaged over 5 independent runs.
6. Long-Context Benchmarks
   - AA-LCR: scores averaged over three runs (avg@3).
   - LongBench-V2: identical prompts and input contexts standardized to ~128k tokens.
7. Agent Swarm
   - BrowseComp (Swarm Mode): main agent max 15 steps; sub-agents max 100 steps.
   - WideSearch (Swarm Mode): main and sub-agents max 100 steps.

</details>

## 4. Native INT4 Quantization
Kimi-K2.5 adopts the same native int4 quantization method as [Kimi-K2-Thinking](https://huggingface.co/moonshotai/Kimi-K2-Thinking#4-native-int4-quantization).

## 5. Deployment
> [!Note]
> You can access Kimi-K2.5's API on https://platform.moonshot.ai and we provide OpenAI/Anthropic-compatible API for you. To verify the deployment is correct, we also provide the  [Kimi Vendor Verifier](https://kimi.com/blog/kimi-vendor-verifier.html).
Currently, Kimi-K2.5 is recommended to run on the following inference engines:
* vLLM
* SGLang
* KTransformers

The minimum version requirement for `transformers` is `4.57.1`.

Deployment examples can be found in the [Model Deployment Guide](docs/deploy_guidance.md).


---
## 6. Model Usage

The usage demos below demonstrate how to call our official API. 

For third-party APIs deployed with vLLM or SGLang, please note that:
> [!Note]
> - Chat with video content is an experimental feature and is only supported in our official API for now.
> 
> - The recommended `temperature` will be `1.0` for Thinking mode and `0.6` for Instant mode.
> 
> - The recommended `top_p` is `0.95`.
> 
> - To use instant mode, you need to pass `{'chat_template_kwargs': {"thinking": False}}` in `extra_body`.

### Chat Completion

This is a simple chat completion script which shows how to call K2.5 API in Thinking and Instant modes.

```python
import openai
import base64
import requests
def simple_chat(client: openai.OpenAI, model_name: str):
    messages = [
        {'role': 'system', 'content': 'You are Kimi, an AI assistant created by Moonshot AI.'},
        {
            'role': 'user',
            'content': [
                {'type': 'text', 'text': 'which one is bigger, 9.11 or 9.9? think carefully.'}
            ],
        },
    ]
    response = client.chat.completions.create(
        model=model_name, messages=messages, stream=False, max_tokens=4096
    )
    print('====== Below is reasoning_content in Thinking Mode ======')
    print(f'reasoning content: {response.choices[0].message.reasoning_content}')
    print('====== Below is response in Thinking Mode ======')
    print(f'response: {response.choices[0].message.content}')

    # To use instant mode, pass {"thinking" = {"type":"disabled"}}
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        stream=False,
        max_tokens=4096,
        extra_body={'thinking': {'type': 'disabled'}},  # this is for official API
        # extra_body= {'chat_template_kwargs': {"thinking": False}}  # this is for vLLM/SGLang
    )
    print('====== Below is response in Instant Mode ======')
    print(f'response: {response.choices[0].message.content}')
```


### Chat Completion with visual content

K2.5 supports Image and Video input. 

The following example demonstrates how to call K2.5 API with image input:

```python
import openai
import base64
import requests

def chat_with_image(client: openai.OpenAI, model_name: str):
    url = 'https://huggingface.co/moonshotai/Kimi-K2.5/resolve/main/figures/kimi-logo.png'
    image_base64 = base64.b64encode(requests.get(url).content).decode()
    messages = [
        {
            'role': 'user',
            'content': [
                {
                    'type': 'image_url',
                    'image_url': {'url': f'data:image/png;base64, {image_base64}'},
                },
                {'type': 'text', 'text': 'Describe this image in detail.'},
            ],
        }
    ]

    response = client.chat.completions.create(
        model=model_name, messages=messages, stream=False, max_tokens=8192
    )
    print('====== Below is reasoning_content in Thinking Mode ======')
    print(f'reasoning content: {response.choices[0].message.reasoning_content}')
    print('====== Below is response in Thinking Mode ======')
    print(f'response: {response.choices[0].message.content}')

    # Also support instant mode if you pass {"thinking" = {"type":"disabled"}}
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        stream=False,
        max_tokens=4096,
        extra_body={'thinking': {'type': 'disabled'}},  # this is for official API
        # extra_body= {'chat_template_kwargs': {"thinking": False}}  # this is for vLLM/SGLang
    )
    print('====== Below is response in Instant Mode ======')
    print(f'response: {response.choices[0].message.content}')

    return response.choices[0].message.content
```

The following example demonstrates how to call K2.5 API with video input:

```python
import openai
import base64
import requests

def chat_with_video(client: openai.OpenAI, model_name:str):
    url = 'https://huggingface.co/moonshotai/Kimi-K2.5/resolve/main/figures/demo_video.mp4'
    video_base64 = base64.b64encode(requests.get(url).content).decode()
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "video_url",
                    "video_url": {"url": f"data:video/mp4;base64,{video_base64}"},
                },
                {"type": "text","text": "Describe the video in detail."},
            ],
        }
    ]

    response = client.chat.completions.create(model=model_name, messages=messages)
    print('====== Below is reasoning_content in Thinking Mode ======')
    print(f'reasoning content: {response.choices[0].message.reasoning_content}')
    print('====== Below is response in Thinking Mode ======')
    print(f'response: {response.choices[0].message.content}')

    # Also support instant mode if pass {"thinking" = {"type":"disabled"}}
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        stream=False,
        max_tokens=4096,
        extra_body={'thinking': {'type': 'disabled'}},  # this is for official API
        # extra_body= {'chat_template_kwargs': {"thinking": False}}  # this is for vLLM/SGLang
    )
    print('====== Below is response in Instant Mode ======')
    print(f'response: {response.choices[0].message.content}')
    return response.choices[0].message.content
```

### Interleaved Thinking and Multi-Step Tool Call

K2.5 shares the same design of Interleaved Thinking and Multi-Step Tool Call as K2 Thinking. For usage example, please refer to the [K2 Thinking documentation](https://platform.moonshot.ai/docs/guide/use-kimi-k2-thinking-model#complete-example).


### Coding Agent Framework

Kimi K2.5 works best with Kimi Code CLI as its agent framework — give it a try at https://www.kimi.com/code.


---

## 7. License

Both the code repository and the model weights are released under the [Modified MIT License](LICENSE).

---

## 8. Third Party Notices

See [THIRD PARTY NOTICES](THIRD_PARTY_NOTICES.md)

---

## 9. Contact Us

If you have any questions, please reach out at [support@moonshot.cn](mailto:support@moonshot.cn).

## 10. Reference

If you find K2.5 useful for your research, please kindly cite K2.5 technical report as follows:

```bibtex
@misc{kimiteam2026kimik25visualagentic,
      title={Kimi K2.5: Visual Agentic Intelligence}, 
      author={Kimi Team and Tongtong Bai and Yifan Bai and Yiping Bao and S. H. Cai and Yuan Cao and Y. Charles and H. S. Che and Cheng Chen and Guanduo Chen and Huarong Chen and Jia Chen and Jiahao Chen and Jianlong Chen and Jun Chen and Kefan Chen and Liang Chen and Ruijue Chen and Xinhao Chen and Yanru Chen and Yanxu Chen and Yicun Chen and Yimin Chen and Yingjiang Chen and Yuankun Chen and Yujie Chen and Yutian Chen and Zhirong Chen and Ziwei Chen and Dazhi Cheng and Minghan Chu and Jialei Cui and Jiaqi Deng and Muxi Diao and Hao Ding and Mengfan Dong and Mengnan Dong and Yuxin Dong and Yuhao Dong and Angang Du and Chenzhuang Du and Dikang Du and Lingxiao Du and Yulun Du and Yu Fan and Shengjun Fang and Qiulin Feng and Yichen Feng and Garimugai Fu and Kelin Fu and Hongcheng Gao and Tong Gao and Yuyao Ge and Shangyi Geng and Chengyang Gong and Xiaochen Gong and Zhuoma Gongque and Qizheng Gu and Xinran Gu and Yicheng Gu and Longyu Guan and Yuanying Guo and Xiaoru Hao and Weiran He and Wenyang He and Yunjia He and Chao Hong and Hao Hu and Jiaxi Hu and Yangyang Hu and Zhenxing Hu and Ke Huang and Ruiyuan Huang and Weixiao Huang and Zhiqi Huang and Tao Jiang and Zhejun Jiang and Xinyi Jin and Yu Jing and Guokun Lai and Aidi Li and C. Li and Cheng Li and Fang Li and Guanghe Li and Guanyu Li and Haitao Li and Haoyang Li and Jia Li and Jingwei Li and Junxiong Li and Lincan Li and Mo Li and Weihong Li and Wentao Li and Xinhang Li and Xinhao Li and Yang Li and Yanhao Li and Yiwei Li and Yuxiao Li and Zhaowei Li and Zheming Li and Weilong Liao and Jiawei Lin and Xiaohan Lin and Zhishan Lin and Zichao Lin and Cheng Liu and Chenyu Liu and Hongzhang Liu and Liang Liu and Shaowei Liu and Shudong Liu and Shuran Liu and Tianwei Liu and Tianyu Liu and Weizhou Liu and Xiangyan Liu and Yangyang Liu and Yanming Liu and Yibo Liu and Yuanxin Liu and Yue Liu and Zhengying Liu and Zhongnuo Liu and Enzhe Lu and Haoyu Lu and Zhiyuan Lu and Junyu Luo and Tongxu Luo and Yashuo Luo and Long Ma and Yingwei Ma and Shaoguang Mao and Yuan Mei and Xin Men and Fanqing Meng and Zhiyong Meng and Yibo Miao and Minqing Ni and Kun Ouyang and Siyuan Pan and Bo Pang and Yuchao Qian and Ruoyu Qin and Zeyu Qin and Jiezhong Qiu and Bowen Qu and Zeyu Shang and Youbo Shao and Tianxiao Shen and Zhennan Shen and Juanfeng Shi and Lidong Shi and Shengyuan Shi and Feifan Song and Pengwei Song and Tianhui Song and Xiaoxi Song and Hongjin Su and Jianlin Su and Zhaochen Su and Lin Sui and Jinsong Sun and Junyao Sun and Tongyu Sun and Flood Sung and Yunpeng Tai and Chuning Tang and Heyi Tang and Xiaojuan Tang and Zhengyang Tang and Jiawen Tao and Shiyuan Teng and Chaoran Tian and Pengfei Tian and Ao Wang and Bowen Wang and Chensi Wang and Chuang Wang and Congcong Wang and Dingkun Wang and Dinglu Wang and Dongliang Wang and Feng Wang and Hailong Wang and Haiming Wang and Hengzhi Wang and Huaqing Wang and Hui Wang and Jiahao Wang and Jinhong Wang and Jiuzheng Wang and Kaixin Wang and Linian Wang and Qibin Wang and Shengjie Wang and Shuyi Wang and Si Wang and Wei Wang and Xiaochen Wang and Xinyuan Wang and Yao Wang and Yejie Wang and Yipu Wang and Yiqin Wang and Yucheng Wang and Yuzhi Wang and Zhaoji Wang and Zhaowei Wang and Zhengtao Wang and Zhexu Wang and Zihan Wang and Zizhe Wang and Chu Wei and Ming Wei and Chuan Wen and Zichen Wen and Chengjie Wu and Haoning Wu and Junyan Wu and Rucong Wu and Wenhao Wu and Yuefeng Wu and Yuhao Wu and Yuxin Wu and Zijian Wu and Chenjun Xiao and Jin Xie and Xiaotong Xie and Yuchong Xie and Yifei Xin and Bowei Xing and Boyu Xu and Jianfan Xu and Jing Xu and Jinjing Xu and L. H. Xu and Lin Xu and Suting Xu and Weixin Xu and Xinbo Xu and Xinran Xu and Yangchuan Xu and Yichang Xu and Yuemeng Xu and Zelai Xu and Ziyao Xu and Junjie Yan and Yuzi Yan and Guangyao Yang and Hao Yang and Junwei Yang and Kai Yang and Ningyuan Yang and Ruihan Yang and Xiaofei Yang and Xinlong Yang and Ying Yang and Yi Yang and Yi Yang and Zhen Yang and Zhilin Yang and Zonghan Yang and Haotian Yao and Dan Ye and Wenjie Ye and Zhuorui Ye and Bohong Yin and Chengzhen Yu and Longhui Yu and Tao Yu and Tianxiang Yu and Enming Yuan and Mengjie Yuan and Xiaokun Yuan and Yang Yue and Weihao Zeng and Dunyuan Zha and Haobing Zhan and Dehao Zhang and Hao Zhang and Jin Zhang and Puqi Zhang and Qiao Zhang and Rui Zhang and Xiaobin Zhang and Y. Zhang and Yadong Zhang and Yangkun Zhang and Yichi Zhang and Yizhi Zhang and Yongting Zhang and Yu Zhang and Yushun Zhang and Yutao Zhang and Yutong Zhang and Zheng Zhang and Chenguang Zhao and Feifan Zhao and Jinxiang Zhao and Shuai Zhao and Xiangyu Zhao and Yikai Zhao and Zijia Zhao and Huabin Zheng and Ruihan Zheng and Shaojie Zheng and Tengyang Zheng and Junfeng Zhong and Longguang Zhong and Weiming Zhong and M. Zhou and Runjie Zhou and Xinyu Zhou and Zaida Zhou and Jinguo Zhu and Liya Zhu and Xinhao Zhu and Yuxuan Zhu and Zhen Zhu and Jingze Zhuang and Weiyu Zhuang and Ying Zou and Xinxing Zu},
      year={2026},
      eprint={2602.02276},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2602.02276}, 
}
```
