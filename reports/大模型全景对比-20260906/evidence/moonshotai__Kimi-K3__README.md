---
tags:
- compressed-tensors
- conversational
license: other
license_name: "kimi-k3"
library_name: transformers
pipeline_tag: image-text-to-text
---
<div align="center">
  <picture>
      <img src="assets/kimi-logo.png" width="30%" alt="Kimi K3">
  </picture>
</div>
<hr>
<div align="center" style="line-height:1">
  <a href="https://www.kimi.com" target="_blank"><img alt="Chat" src="https://img.shields.io/badge/🤖%20Chat-Kimi%20K3-ff6b6b?color=1783ff&logoColor=white"/></a>
  <a href="https://www.moonshot.ai" target="_blank"><img alt="Homepage" src="https://img.shields.io/badge/Homepage-Moonshot%20AI-white?logo=Kimi&logoColor=white"/></a>
</div>

<div align="center" style="line-height: 1;">
  <a href="https://huggingface.co/moonshotai" target="_blank"><img alt="Hugging Face" src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Moonshot%20AI-ffc107?color=ffc107&logoColor=white"/></a>
  <a href="https://twitter.com/kimi_moonshot" target="_blank"><img alt="Twitter Follow" src="https://img.shields.io/badge/Twitter-Kimi.ai-white?logo=x&logoColor=white"/></a>
  <a href="https://discord.gg/TYU2fdJykW" target="_blank"><img alt="Discord" src="https://img.shields.io/badge/Discord-Kimi.ai-white?logo=discord&logoColor=white"/></a>
  <a href="https://modelscope.cn/organization/moonshotai" target="_blank"><img alt="ModelScope" src="https://img.shields.io/badge/ModelScope-Moonshot%20AI-white?labelColor=rgb(99%2C%2074%2C%255)"/></a>
</div>
<div align="center" style="line-height: 1;">
  <a href="https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/badge/License-Kimi_K3-f5de53?&color=f5de53"/></a>
</div>


<p align="center">
📰&nbsp;&nbsp;<a href="https://www.kimi.com/blog/kimi-k3">Tech Blog</a> | &nbsp;&nbsp;&nbsp; <b>📄&nbsp;&nbsp;<a href="https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf">Full Report</a></b>
</p>



## 1. Model Introduction

Kimi K3 is an open-weight, native multimodal agentic model and our most capable model to date. It is a 2.8T-parameter model built on Kimi Delta Attention (KDA) and Attention Residuals (AttnRes), with native vision capabilities and a 1-million-token context window. It is the world's first open 3T-class model, designed for frontier intelligence across long-horizon coding, knowledge work, and reasoning.

### Key Features
- **New Architecture**: Kimi K3 is built on Kimi Delta Attention (KDA) and Attention Residuals (AttnRes), and scales up MoE sparsity with a Stable LatentMoE framework that activates 16 out of 896 experts — yielding an approximate 2.5× improvement in overall scaling efficiency over Kimi K2.
- **Long-Horizon Coding**: Operating with minimal human oversight, Kimi K3 sustains long engineering sessions, navigates massive repositories, and orchestrates terminal tools — from GPU kernel optimization and compiler development to vision-in-the-loop game dev, CAD, and even chip design.
- **Agentic Knowledge Work**: Kimi K3 advances end-to-end knowledge work, producing deep research with interactive visualizations, widgets and dashboards, and motion design and video editing, powered by its native multimodal architecture.
- **Native Multimodality & Long Context**: Kimi K3 understands text, images, and video within the same model, and supports a 1-million-token context window.
- **Open Frontier Weights**: We release the full Kimi K3 model weights under the Kimi K3 License, making frontier intelligence openly available for research, deployment, and further innovation.
## 2. Model Summary

<div align="center">
<table>
<tbody>
<tr>
<td align="center" style="vertical-align: middle; text-align: center"><strong>Architecture</strong></td>
<td align="center" style="vertical-align: middle; text-align: center">Mixture-of-Experts (MoE)</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center"><strong>Total Parameters</strong></td>
<td align="center" style="vertical-align: middle; text-align: center">2.8T</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center"><strong>Activated Parameters</strong></td>
<td align="center" style="vertical-align: middle; text-align: center">104B</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center"><strong>Number of Layers</strong></td>
<td align="center" style="vertical-align: middle; text-align: center">93</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center"><strong>Number of Dense Layers</strong></td>
<td align="center" style="vertical-align: middle; text-align: center">1</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center"><strong>Attention-Layer Composition</strong></td>
<td align="center" style="vertical-align: middle; text-align: center">69 KDA + 24 Gated MLA</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center"><strong>Attention Hidden Dimension</strong></td>
<td align="center" style="vertical-align: middle; text-align: center">7168</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center"><strong>Number of Attention Heads</strong></td>
<td align="center" style="vertical-align: middle; text-align: center">96</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center"><strong>Latent MoE Dimension</strong></td>
<td align="center" style="vertical-align: middle; text-align: center">3584</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center"><strong>MoE Hidden Dimension</strong> (per Expert)</td>
<td align="center" style="vertical-align: middle; text-align: center">3072</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center"><strong>Number of Experts</strong></td>
<td align="center" style="vertical-align: middle; text-align: center">896</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center"><strong>Selected Experts per Token</strong></td>
<td align="center" style="vertical-align: middle; text-align: center">16</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center"><strong>Number of Shared Experts</strong></td>
<td align="center" style="vertical-align: middle; text-align: center">2</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center"><strong>Vocabulary Size</strong></td>
<td align="center" style="vertical-align: middle; text-align: center">160K</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center"><strong>Context Length</strong></td>
<td align="center" style="vertical-align: middle; text-align: center">1048576</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center"><strong>Attention Mechanism</strong></td>
<td align="center" style="vertical-align: middle; text-align: center">KDA &amp; Gated MLA</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center"><strong>Activation Function</strong></td>
<td align="center" style="vertical-align: middle; text-align: center">SiTU-GLU</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center"><strong>Vision Encoder</strong></td>
<td align="center" style="vertical-align: middle; text-align: center">MoonViT-V2</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center"><strong>Parameters of Vision Encoder</strong></td>
<td align="center" style="vertical-align: middle; text-align: center">401M</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center"><strong>Quantization</strong></td>
<td align="center" style="vertical-align: middle; text-align: center">MXFP4 weights / MXFP8 activations<br>(quantization-aware training)</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center"><strong>Modality</strong></td>
<td align="center" style="vertical-align: middle; text-align: center">Text, Image</td>
</tr>
</tbody>
</table>
</div>


## 3. Evaluation Results

<div align="center">
<table>
<thead>
<tr>
<th align="center" style="text-align: center">Benchmark</th>
<th align="center" style="text-align: center"><sup>Kimi K3<br><sup>(max)</sup></sup></th>
<th align="center" style="text-align: center"><sup>Claude Fable 5<br><sup>(max, w/ fallback)</sup></sup></th>
<th align="center" style="text-align: center"><sup>GPT-5.6 Sol<br><sup>(max)</sup></sup></th>
<th align="center" style="text-align: center"><sup>Claude Opus 4.8<br><sup>(max)</sup></sup></th>
<th align="center" style="text-align: center"><sup>GPT-5.5<br><sup>(xhigh)</sup></sup></th>
<th align="center" style="text-align: center"><sup>GLM-5.2<br><sup>(max)</sup></sup></th>
</tr>
</thead>
<tbody>
<tr>
<td align="center" colspan=7 style="text-align: center"><strong>Reasoning &amp; Knowledge</strong></td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">GPQA Diamond</td>
<td align="center" style="vertical-align: middle; text-align: center">93.5</td>
<td align="center" style="vertical-align: middle; text-align: center">92.6</td>
<td align="center" style="vertical-align: middle; text-align: center">94.1</td>
<td align="center" style="vertical-align: middle; text-align: center">91.0</td>
<td align="center" style="vertical-align: middle; text-align: center">93.5</td>
<td align="center" style="vertical-align: middle; text-align: center">91.2</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">CritPt</td>
<td align="center" style="vertical-align: middle; text-align: center">23.4</td>
<td align="center" style="vertical-align: middle; text-align: center">28.6</td>
<td align="center" style="vertical-align: middle; text-align: center">32.3</td>
<td align="center" style="vertical-align: middle; text-align: center">20.9</td>
<td align="center" style="vertical-align: middle; text-align: center">27.1</td>
<td align="center" style="vertical-align: middle; text-align: center">20.9</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">AA-LCR</td>
<td align="center" style="vertical-align: middle; text-align: center">74.7</td>
<td align="center" style="vertical-align: middle; text-align: center">70.0</td>
<td align="center" style="vertical-align: middle; text-align: center">73.7</td>
<td align="center" style="vertical-align: middle; text-align: center">67.7</td>
<td align="center" style="vertical-align: middle; text-align: center">74.3</td>
<td align="center" style="vertical-align: middle; text-align: center">71.3</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">HLE-Full</td>
<td align="center" style="vertical-align: middle; text-align: center">43.5 / 56.0</td>
<td align="center" style="vertical-align: middle; text-align: center">53.3 / 63.0</td>
<td align="center" style="vertical-align: middle; text-align: center">44.5 / 58.0</td>
<td align="center" style="vertical-align: middle; text-align: center">49.8 / 57.9</td>
<td align="center" style="vertical-align: middle; text-align: center">41.4 / 52.2</td>
<td align="center" style="vertical-align: middle; text-align: center">—</td>
</tr>
<tr>
<td align="center" colspan=7 style="text-align: center"><strong>Coding</strong></td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">DeepSWE</td>
<td align="center" style="vertical-align: middle; text-align: center">67.5</td>
<td align="center" style="vertical-align: middle; text-align: center">70.0</td>
<td align="center" style="vertical-align: middle; text-align: center">73.0</td>
<td align="center" style="vertical-align: middle; text-align: center">59.0</td>
<td align="center" style="vertical-align: middle; text-align: center">67.0</td>
<td align="center" style="vertical-align: middle; text-align: center">46.2</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">ProgramBench</td>
<td align="center" style="vertical-align: middle; text-align: center">77.8</td>
<td align="center" style="vertical-align: middle; text-align: center">76.8</td>
<td align="center" style="vertical-align: middle; text-align: center">77.6</td>
<td align="center" style="vertical-align: middle; text-align: center">71.9</td>
<td align="center" style="vertical-align: middle; text-align: center">70.8</td>
<td align="center" style="vertical-align: middle; text-align: center">63.7</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">Terminal-Bench 2.1</td>
<td align="center" style="vertical-align: middle; text-align: center">88.3</td>
<td align="center" style="vertical-align: middle; text-align: center">88.0</td>
<td align="center" style="vertical-align: middle; text-align: center">88.8</td>
<td align="center" style="vertical-align: middle; text-align: center">84.6</td>
<td align="center" style="vertical-align: middle; text-align: center">83.4</td>
<td align="center" style="vertical-align: middle; text-align: center">82.7</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">FrontierSWE</td>
<td align="center" style="vertical-align: middle; text-align: center">81.2</td>
<td align="center" style="vertical-align: middle; text-align: center">86.6</td>
<td align="center" style="vertical-align: middle; text-align: center">71.3</td>
<td align="center" style="vertical-align: middle; text-align: center">66.7</td>
<td align="center" style="vertical-align: middle; text-align: center">64.9</td>
<td align="center" style="vertical-align: middle; text-align: center">67.3</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">SWE-Marathon</td>
<td align="center" style="vertical-align: middle; text-align: center">42.0</td>
<td align="center" style="vertical-align: middle; text-align: center">35.0</td>
<td align="center" style="vertical-align: middle; text-align: center">39.0</td>
<td align="center" style="vertical-align: middle; text-align: center">40.0</td>
<td align="center" style="vertical-align: middle; text-align: center">14.0</td>
<td align="center" style="vertical-align: middle; text-align: center">13.0</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">PostTrainBench</td>
<td align="center" style="vertical-align: middle; text-align: center">36.6</td>
<td align="center" style="vertical-align: middle; text-align: center">41.4</td>
<td align="center" style="vertical-align: middle; text-align: center">34.6</td>
<td align="center" style="vertical-align: middle; text-align: center">34.1</td>
<td align="center" style="vertical-align: middle; text-align: center">28.4</td>
<td align="center" style="vertical-align: middle; text-align: center">34.3</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">MLS-Bench-Lite</td>
<td align="center" style="vertical-align: middle; text-align: center">48.3</td>
<td align="center" style="vertical-align: middle; text-align: center">49.9</td>
<td align="center" style="vertical-align: middle; text-align: center">46.2</td>
<td align="center" style="vertical-align: middle; text-align: center">42.8</td>
<td align="center" style="vertical-align: middle; text-align: center">35.5</td>
<td align="center" style="vertical-align: middle; text-align: center">40.4</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">SciCode</td>
<td align="center" style="vertical-align: middle; text-align: center">58.7</td>
<td align="center" style="vertical-align: middle; text-align: center">60.2</td>
<td align="center" style="vertical-align: middle; text-align: center">56.1</td>
<td align="center" style="vertical-align: middle; text-align: center">53.5</td>
<td align="center" style="vertical-align: middle; text-align: center">56.1</td>
<td align="center" style="vertical-align: middle; text-align: center">50.5</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">Kimi Code Bench 2.0</td>
<td align="center" style="vertical-align: middle; text-align: center">72.9</td>
<td align="center" style="vertical-align: middle; text-align: center">76.9</td>
<td align="center" style="vertical-align: middle; text-align: center">64.8</td>
<td align="center" style="vertical-align: middle; text-align: center">71.7</td>
<td align="center" style="vertical-align: middle; text-align: center">69.0</td>
<td align="center" style="vertical-align: middle; text-align: center">64.2</td>
</tr>
<tr>
<td align="center" colspan=7 style="text-align: center"><strong>Agentic</strong></td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">BrowseComp</td>
<td align="center" style="vertical-align: middle; text-align: center">91.2</td>
<td align="center" style="vertical-align: middle; text-align: center">88.0</td>
<td align="center" style="vertical-align: middle; text-align: center">90.4</td>
<td align="center" style="vertical-align: middle; text-align: center">84.3</td>
<td align="center" style="vertical-align: middle; text-align: center">84.4</td>
<td align="center" style="vertical-align: middle; text-align: center">—</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">DeepSearchQA (F1)</td>
<td align="center" style="vertical-align: middle; text-align: center">95.0</td>
<td align="center" style="vertical-align: middle; text-align: center">94.2</td>
<td align="center" style="vertical-align: middle; text-align: center">—</td>
<td align="center" style="vertical-align: middle; text-align: center">93.1</td>
<td align="center" style="vertical-align: middle; text-align: center">—</td>
<td align="center" style="vertical-align: middle; text-align: center">—</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">ResearchRubrics</td>
<td align="center" style="vertical-align: middle; text-align: center">76.2</td>
<td align="center" style="vertical-align: middle; text-align: center">—</td>
<td align="center" style="vertical-align: middle; text-align: center">73.8</td>
<td align="center" style="vertical-align: middle; text-align: center">73.5</td>
<td align="center" style="vertical-align: middle; text-align: center">64.0</td>
<td align="center" style="vertical-align: middle; text-align: center">71.1</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">GDPval-AA v2 (Elo)</td>
<td align="center" style="vertical-align: middle; text-align: center">1686</td>
<td align="center" style="vertical-align: middle; text-align: center">1747</td>
<td align="center" style="vertical-align: middle; text-align: center">1736</td>
<td align="center" style="vertical-align: middle; text-align: center">1593</td>
<td align="center" style="vertical-align: middle; text-align: center">1491</td>
<td align="center" style="vertical-align: middle; text-align: center">1510</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">Toolathlon-Verified</td>
<td align="center" style="vertical-align: middle; text-align: center">76.5</td>
<td align="center" style="vertical-align: middle; text-align: center">77.9</td>
<td align="center" style="vertical-align: middle; text-align: center">74.9</td>
<td align="center" style="vertical-align: middle; text-align: center">76.2</td>
<td align="center" style="vertical-align: middle; text-align: center">73.5</td>
<td align="center" style="vertical-align: middle; text-align: center">59.9</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">MCPMark-Verified</td>
<td align="center" style="vertical-align: middle; text-align: center">94.5</td>
<td align="center" style="vertical-align: middle; text-align: center">87.4</td>
<td align="center" style="vertical-align: middle; text-align: center">92.9</td>
<td align="center" style="vertical-align: middle; text-align: center">76.4</td>
<td align="center" style="vertical-align: middle; text-align: center">92.9</td>
<td align="center" style="vertical-align: middle; text-align: center">—</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">MCP-Atlas</td>
<td align="center" style="vertical-align: middle; text-align: center">84.2</td>
<td align="center" style="vertical-align: middle; text-align: center">84.7</td>
<td align="center" style="vertical-align: middle; text-align: center">83.6</td>
<td align="center" style="vertical-align: middle; text-align: center">83.6</td>
<td align="center" style="vertical-align: middle; text-align: center">82.8</td>
<td align="center" style="vertical-align: middle; text-align: center">82.6</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">AutomationBench</td>
<td align="center" style="vertical-align: middle; text-align: center">30.8</td>
<td align="center" style="vertical-align: middle; text-align: center">29.1</td>
<td align="center" style="vertical-align: middle; text-align: center">29.7</td>
<td align="center" style="vertical-align: middle; text-align: center">27.2</td>
<td align="center" style="vertical-align: middle; text-align: center">22.7</td>
<td align="center" style="vertical-align: middle; text-align: center">12.9</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">JobBench</td>
<td align="center" style="vertical-align: middle; text-align: center">54.3</td>
<td align="center" style="vertical-align: middle; text-align: center">57.4</td>
<td align="center" style="vertical-align: middle; text-align: center">45.4</td>
<td align="center" style="vertical-align: middle; text-align: center">48.4</td>
<td align="center" style="vertical-align: middle; text-align: center">38.3</td>
<td align="center" style="vertical-align: middle; text-align: center">43.4</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">AA-Briefcase (Elo)</td>
<td align="center" style="vertical-align: middle; text-align: center">1548</td>
<td align="center" style="vertical-align: middle; text-align: center">1583</td>
<td align="center" style="vertical-align: middle; text-align: center">1495</td>
<td align="center" style="vertical-align: middle; text-align: center">1354</td>
<td align="center" style="vertical-align: middle; text-align: center">1158</td>
<td align="center" style="vertical-align: middle; text-align: center">1260</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">Agents' Last Exam</td>
<td align="center" style="vertical-align: middle; text-align: center">28.3</td>
<td align="center" style="vertical-align: middle; text-align: center">25.7<sup>†</sup></td>
<td align="center" style="vertical-align: middle; text-align: center">29.6</td>
<td align="center" style="vertical-align: middle; text-align: center">27.0</td>
<td align="center" style="vertical-align: middle; text-align: center">26.6</td>
<td align="center" style="vertical-align: middle; text-align: center">20.4</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">APEX-Agents</td>
<td align="center" style="vertical-align: middle; text-align: center">41.0</td>
<td align="center" style="vertical-align: middle; text-align: center">43.3</td>
<td align="center" style="vertical-align: middle; text-align: center">39.9</td>
<td align="center" style="vertical-align: middle; text-align: center">39.4</td>
<td align="center" style="vertical-align: middle; text-align: center">38.5</td>
<td align="center" style="vertical-align: middle; text-align: center">35.6</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">OfficeQA Pro</td>
<td align="center" style="vertical-align: middle; text-align: center">63.3</td>
<td align="center" style="vertical-align: middle; text-align: center">69.9</td>
<td align="center" style="vertical-align: middle; text-align: center">63.2</td>
<td align="center" style="vertical-align: middle; text-align: center">63.9</td>
<td align="center" style="vertical-align: middle; text-align: center">60.9</td>
<td align="center" style="vertical-align: middle; text-align: center">41.4</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">SpreadsheetBench 2</td>
<td align="center" style="vertical-align: middle; text-align: center">34.8</td>
<td align="center" style="vertical-align: middle; text-align: center">34.7</td>
<td align="center" style="vertical-align: middle; text-align: center">32.4</td>
<td align="center" style="vertical-align: middle; text-align: center">31.6</td>
<td align="center" style="vertical-align: middle; text-align: center">29.1</td>
<td align="center" style="vertical-align: middle; text-align: center">28.1</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">OSWorld-Verified</td>
<td align="center" style="vertical-align: middle; text-align: center">84.8</td>
<td align="center" style="vertical-align: middle; text-align: center">85.0</td>
<td align="center" style="vertical-align: middle; text-align: center">83.0</td>
<td align="center" style="vertical-align: middle; text-align: center">83.4</td>
<td align="center" style="vertical-align: middle; text-align: center">79.0</td>
<td align="center" style="vertical-align: middle; text-align: center">—</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">OSWorld 2.0</td>
<td align="center" style="vertical-align: middle; text-align: center">58.3</td>
<td align="center" style="vertical-align: middle; text-align: center">66.1</td>
<td align="center" style="vertical-align: middle; text-align: center">62.6</td>
<td align="center" style="vertical-align: middle; text-align: center">55.7</td>
<td align="center" style="vertical-align: middle; text-align: center">49.5</td>
<td align="center" style="vertical-align: middle; text-align: center">—</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">SaaS-Bench</td>
<td align="center" style="vertical-align: middle; text-align: center">60.1</td>
<td align="center" style="vertical-align: middle; text-align: center">—</td>
<td align="center" style="vertical-align: middle; text-align: center">61.4</td>
<td align="center" style="vertical-align: middle; text-align: center">56.1</td>
<td align="center" style="vertical-align: middle; text-align: center">43.8</td>
<td align="center" style="vertical-align: middle; text-align: center">—</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">τ³-Banking</td>
<td align="center" style="vertical-align: middle; text-align: center">33.4</td>
<td align="center" style="vertical-align: middle; text-align: center">26.8</td>
<td align="center" style="vertical-align: middle; text-align: center">33.0</td>
<td align="center" style="vertical-align: middle; text-align: center">27.6</td>
<td align="center" style="vertical-align: middle; text-align: center">31.3</td>
<td align="center" style="vertical-align: middle; text-align: center">26.8</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">Harvey Lab-AA</td>
<td align="center" style="vertical-align: middle; text-align: center">94.6</td>
<td align="center" style="vertical-align: middle; text-align: center">93.6</td>
<td align="center" style="vertical-align: middle; text-align: center">87.2</td>
<td align="center" style="vertical-align: middle; text-align: center">91.1</td>
<td align="center" style="vertical-align: middle; text-align: center">86.3</td>
<td align="center" style="vertical-align: middle; text-align: center">91.0</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">CorpFin v2</td>
<td align="center" style="vertical-align: middle; text-align: center">71.6</td>
<td align="center" style="vertical-align: middle; text-align: center">71.8</td>
<td align="center" style="vertical-align: middle; text-align: center">64.4</td>
<td align="center" style="vertical-align: middle; text-align: center">66.7</td>
<td align="center" style="vertical-align: middle; text-align: center">68.4</td>
<td align="center" style="vertical-align: middle; text-align: center">66.1</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">Finance Agent v2</td>
<td align="center" style="vertical-align: middle; text-align: center">54.4</td>
<td align="center" style="vertical-align: middle; text-align: center">56.3</td>
<td align="center" style="vertical-align: middle; text-align: center">53.8</td>
<td align="center" style="vertical-align: middle; text-align: center">53.9</td>
<td align="center" style="vertical-align: middle; text-align: center">51.8</td>
<td align="center" style="vertical-align: middle; text-align: center">49.7</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">Legal Research Bench</td>
<td align="center" style="vertical-align: middle; text-align: center">44.2</td>
<td align="center" style="vertical-align: middle; text-align: center">49.5</td>
<td align="center" style="vertical-align: middle; text-align: center">48.1</td>
<td align="center" style="vertical-align: middle; text-align: center">43.8</td>
<td align="center" style="vertical-align: middle; text-align: center">40.4</td>
<td align="center" style="vertical-align: middle; text-align: center">31.3</td>
</tr>
<tr>
<td align="center" colspan=7 style="text-align: center"><strong>Vision</strong></td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">WorldVQA ForceAnswer</td>
<td align="center" style="vertical-align: middle; text-align: center">51.0</td>
<td align="center" style="vertical-align: middle; text-align: center">56.7</td>
<td align="center" style="vertical-align: middle; text-align: center">41.8</td>
<td align="center" style="vertical-align: middle; text-align: center">39.1</td>
<td align="center" style="vertical-align: middle; text-align: center">38.5</td>
<td align="center" style="vertical-align: middle; text-align: center">—</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">OmniDocBench</td>
<td align="center" style="vertical-align: middle; text-align: center">91.1</td>
<td align="center" style="vertical-align: middle; text-align: center">89.8</td>
<td align="center" style="vertical-align: middle; text-align: center">85.8</td>
<td align="center" style="vertical-align: middle; text-align: center">87.9</td>
<td align="center" style="vertical-align: middle; text-align: center">89.4</td>
<td align="center" style="vertical-align: middle; text-align: center">—</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">PerceptionBench</td>
<td align="center" style="vertical-align: middle; text-align: center">58.5</td>
<td align="center" style="vertical-align: middle; text-align: center">57.2</td>
<td align="center" style="vertical-align: middle; text-align: center">59.7</td>
<td align="center" style="vertical-align: middle; text-align: center">47.2</td>
<td align="center" style="vertical-align: middle; text-align: center">55.8</td>
<td align="center" style="vertical-align: middle; text-align: center">—</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">Video-MME (w. sub)</td>
<td align="center" style="vertical-align: middle; text-align: center">90.0</td>
<td align="center" style="vertical-align: middle; text-align: center">—</td>
<td align="center" style="vertical-align: middle; text-align: center">89.5</td>
<td align="center" style="vertical-align: middle; text-align: center">86.0</td>
<td align="center" style="vertical-align: middle; text-align: center">89.3</td>
<td align="center" style="vertical-align: middle; text-align: center">—</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">MMVU</td>
<td align="center" style="vertical-align: middle; text-align: center">82.1</td>
<td align="center" style="vertical-align: middle; text-align: center">—</td>
<td align="center" style="vertical-align: middle; text-align: center">81.2</td>
<td align="center" style="vertical-align: middle; text-align: center">79.2</td>
<td align="center" style="vertical-align: middle; text-align: center">81.7</td>
<td align="center" style="vertical-align: middle; text-align: center">—</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">BabyVision w/ python</td>
<td align="center" style="vertical-align: middle; text-align: center">85.7</td>
<td align="center" style="vertical-align: middle; text-align: center">90.5</td>
<td align="center" style="vertical-align: middle; text-align: center">88.9</td>
<td align="center" style="vertical-align: middle; text-align: center">81.2</td>
<td align="center" style="vertical-align: middle; text-align: center">83.6</td>
<td align="center" style="vertical-align: middle; text-align: center">—</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">MMMU-Pro</td>
<td align="center" style="vertical-align: middle; text-align: center">81.6 / 83.4</td>
<td align="center" style="vertical-align: middle; text-align: center">81.2 / 86.5</td>
<td align="center" style="vertical-align: middle; text-align: center">83.0 / 84.6</td>
<td align="center" style="vertical-align: middle; text-align: center">78.9 / 82.7</td>
<td align="center" style="vertical-align: middle; text-align: center">81.2 / 83.2</td>
<td align="center" style="vertical-align: middle; text-align: center">—</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">CharXiv (RQ)</td>
<td align="center" style="vertical-align: middle; text-align: center">84.8 / 91.3</td>
<td align="center" style="vertical-align: middle; text-align: center">88.9 / 93.5</td>
<td align="center" style="vertical-align: middle; text-align: center">84.6 / 89.1</td>
<td align="center" style="vertical-align: middle; text-align: center">80.5 / 89.9</td>
<td align="center" style="vertical-align: middle; text-align: center">84.1 / 89.0</td>
<td align="center" style="vertical-align: middle; text-align: center">—</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">MathVision</td>
<td align="center" style="vertical-align: middle; text-align: center">94.3 / 97.8</td>
<td align="center" style="vertical-align: middle; text-align: center">94.8 / 98.6</td>
<td align="center" style="vertical-align: middle; text-align: center">95.8 / 97.8</td>
<td align="center" style="vertical-align: middle; text-align: center">86.7 / 97.1</td>
<td align="center" style="vertical-align: middle; text-align: center">92.2 / 96.8</td>
<td align="center" style="vertical-align: middle; text-align: center">—</td>
</tr>
<tr>
<td align="center" style="vertical-align: middle; text-align: center">ZeroBench (pass@5)</td>
<td align="center" style="vertical-align: middle; text-align: center">23.0 / 41.0</td>
<td align="center" style="vertical-align: middle; text-align: center">23.0 / 46.0</td>
<td align="center" style="vertical-align: middle; text-align: center">17.0 / 35.0</td>
<td align="center" style="vertical-align: middle; text-align: center">17.0 / 34.0</td>
<td align="center" style="vertical-align: middle; text-align: center">22.0 / 41.0</td>
<td align="center" style="vertical-align: middle; text-align: center">—</td>
</tr>
</tbody>
</table>
</div>

<details>
<summary><b>Footnotes</b></summary>

All Kimi K3 results are obtained with reasoning effort set to 'max' and temperature = 1.0. For single-step tasks, such as GPQA Diamond, HLE-Full, and vision benchmarks without tools, we set top-p = 0.95; for agentic tasks, we set top-p = 1.0. For HLE-Full, MMMU-Pro, CharXiv (RQ), MathVision, and ZeroBench, each cell reports the scores without and with tool augmentation (general tools for HLE-Full, Python for the vision benchmarks), in that order.

1. **Reasoning & knowledge benchmarks**
   - **CritPt and AA-LCR.** Scores are cited from [Artificial Analysis](https://artificialanalysis.ai/) as of July 23, 2026.
2. **Coding benchmarks**
   - **DeepSWE.** Kimi K3 is evaluated with the Kimi Code harness. The GLM-5.2 score is taken from the [GLM-5.2 release blog](https://z.ai/blog/glm-5.2); all remaining scores are from the official [DeepSWE leaderboard](https://deepswe.datacurve.ai/), under which Kimi K3 attains 67.3 with the mini-SWE-agent harness. We report the DeepSWE v1.1 tasks.
   - **Terminal-Bench 2.1.** Kimi K3 is evaluated with the Kimi Code harness. For all other models, we report the best score across harnesses: GLM-5.2 with Claude Code ([GLM-5.2 release blog](https://z.ai/blog/glm-5.2)); Claude Opus 4.8 and Claude Fable 5 with Terminus 2 ([Artificial Analysis](https://artificialanalysis.ai/evaluations/terminalbench-v2-1)); GPT-5.5 and GPT-5.6 Sol with Codex ([OpenAI](https://openai.com/index/previewing-gpt-5-6-sol/)).
   - **ProgramBench.** Kimi K3 is evaluated with the Kimi Code harness. The GLM-5.2 score is from the [GLM-5.2 release blog](https://z.ai/blog/glm-5.2); all other scores are from [Vals AI](https://www.vals.ai/benchmarks/programbench).
   - **SWE-Marathon.** Kimi K3, Claude Opus 4.8, and Claude Fable 5 are evaluated with the Claude Code harness; GPT-5.6 Sol is evaluated with the Codex harness. The GLM-5.2 score is from the [GLM-5.2 release blog](https://z.ai/blog/glm-5.2). Our evaluation is based on an H20-calibrated branch of the [official tasks](https://www.swe-marathon.org/) as of July 9, 2026, prior to the final v1.1 release: the Docker images, performance gates, and reference oracles for the GPU tasks have been recalibrated for H20, while the correctness and anti-cheat validators remain unchanged. Additionally, Claude Fable 5 hit fallbacks on 35% of the tasks in our evaluation, which may have negatively impacted its measured performance.
   - **FrontierSWE.** Kimi K3 is evaluated with the Kimi Code harness and GPT-5.6 Sol with the Codex harness; all other results are from [FrontierSWE](https://www.frontierswe.com/). Dominance scores are recomputed from the raw scores using the official evaluation script and are current as of July 16, 2026.
   - **PostTrainBench.** Scores for GLM-5.2, GPT-5.5, and Claude Opus 4.8 are adopted from the official [PostTrainBench](https://posttrainbench.com/) results. Kimi K3, Claude Fable 5, and GPT-5.6 Sol are evaluated with the official Harbor implementation at maximum reasoning effort, averaged over three runs on H20 GPUs (instead of H100 in the official setting) — Kimi K3 and Claude Fable 5 with the Claude Code harness, and GPT-5.6 Sol with the Codex harness.
   - **MLS-Bench-Lite.** Kimi K3 is evaluated with the Kimi Code harness; GLM-5.2 and the Claude models with the Claude Code harness; GPT-5.5 and GPT-5.6 Sol with the Codex harness.
   - **SciCode.** Scores are cited from [Artificial Analysis](https://artificialanalysis.ai/) as of July 23, 2026.
   - **Kimi Code Bench 2.0 (in-house).** Kimi K3 is evaluated with the Kimi Code harness (it attains 73.7 with the Claude Code harness); GLM-5.2, Claude Opus 4.8, and Claude Fable 5 with the Claude Code harness; GPT-5.5 and GPT-5.6 Sol with the Codex harness. All models are evaluated at maximum reasoning effort, except GPT-5.5, which uses the "xhigh" setting. As the benchmark includes cybersecurity and safety-related tasks, we also disclose the fraction of refused or fallback tasks: Claude Fable 5 hit 13 fallbacks and 1 refusal out of 80 tasks; 10 refusals out of 80 tasks entered GPT-5.6 Sol's cyber guard; GPT-5.5 had 3 refusals out of 80 tasks.
3. **Agentic benchmarks**
   - **OfficeQA Pro.** Each test case provides the agent with the entire PDF corpus, with all PDFs rendered as images and no machine-readable text available.
   - **OfficeQA Pro and SpreadsheetBench 2.** Kimi K3, GLM-5.2, Claude Opus 4.8, and Claude Fable 5 are evaluated with the Claude Code harness; GPT-5.5 and GPT-5.6 Sol are evaluated with the Codex harness.
   - **MCP-Atlas.** All models are evaluated on the 500-task public subset with a 100-turn limit, using Gemini 3.1 Pro as the judge.
   - **AutomationBench.** All models are evaluated on the 600-task public subset, following the official GitHub setup in all other respects.
   - **BrowseComp.** We adopt a context-compaction strategy triggered at 300K tokens. When evaluated with the full 1M-token context window and no context management, Kimi K3 achieves a score of 90.4. The results of Claude Fable 5, Claude Opus 4.8, GPT-5.6 Sol, and GPT-5.5 are cited from [Anthropic](https://www.anthropic.com/news/claude-fable-5-mythos-5) and [OpenAI](https://openai.com/index/gpt-5-6/).
   - **GDPval-AA v2, AA-Briefcase, τ³-Banking, Harvey Lab-AA, and APEX-Agents.** Scores are cited from [Artificial Analysis](https://artificialanalysis.ai/) and the [APEX-Agents leaderboard](https://www.mercor.com/apex/apex-agents-leaderboard/) as of July 23, 2026. For Harvey Lab-AA, we report the criterion pass rate.
   - **CorpFin v2, Finance Agent v2, and Legal Research Bench.** Scores are cited from [Vals AI](https://www.vals.ai/).
   - **Agents' Last Exam.** Scores are cited from the [official leaderboard](https://agents-last-exam.org/leaderboard) as of July 23, 2026; we report the leaderboard's primary pass-rate metric. On the leaderboard, each model is paired with a specific harness: Kimi K3 with Kimi Code; GPT-5.6 Sol and GPT-5.5 with Codex; Claude Fable 5, Claude Opus 4.8, and GLM-5.2 with Claude Code. <sup>†</sup> The Claude Fable 5 entry runs at xhigh effort with 40% of tasks annotated as downgraded.
4. **Multimodal benchmarks**
   - Except for ZeroBench, which follows the official setting and is run five times, all multimodal scores are averaged over three runs. MMMU-Pro is evaluated following the official protocol, preserving the original input order and prepending images to the text input.
   - **PerceptionBench** is an in-house benchmark that focuses on atomic visual perception capabilities.

</details>

## 4. Native MXFP4 Quantization

Kimi K3 applies quantization-aware training from the SFT stage onward, using MXFP4 weights with MXFP8 activations for broad hardware compatibility.

## 5. Deployment

> [!Note]
> You can access Kimi K3's API on https://platform.kimi.ai by selecting `kimi-k3`, and we provide OpenAI/Anthropic-compatible API for you. Currently, Kimi K3 is recommended to run on the following inference engines:

- [vLLM](https://github.com/vllm-project/vllm) — see [recipes](https://recipes.vllm.ai/moonshotai/Kimi-K3)
- [SGLang](https://github.com/sgl-project/sglang) — see [cookbook](https://docs.sglang.io/cookbook/autoregressive/Moonshotai/Kimi-K3)
- [TokenSpeed](https://github.com/lightseekorg/tokenspeed) — see [recipes](https://lightseek.org/tokenspeed/recipes/models#kimi-k3)

---
## 6. Model Usage

Kimi K3 always has thinking enabled, and will return `reasoning_content`. Thinking effort is configured with the top-level `reasoning_effort` request field, which supports `"low"`, `"high"`, and `"max"` (default `"max"`).

Kimi K3 was trained in the preserved thinking history mode. For multi-turn conversations and tool calls, Kimi K3 requires the complete assistant message returned by the API to be passed back to `messages` as-is — including `reasoning_content` and `tool_calls`, not just `content`:

```python
import openai

def chat_with_preserved_thinking(client: openai.OpenAI, model_name: str):
    messages = [
        {
            "role": "user",
            "content": "Tell me three random numbers."
        },
        {
            "role": "assistant",
            "reasoning_content": "I'll start by listing five numbers: 473, 921, 235, 215, 222, and I'll tell you the first three.",
            "content": "473, 921, 235"
        },
        {
            "role": "user",
            "content": "What are the other two numbers you have in mind?"
        }
    ]

    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        stream=False,
        max_tokens=4096,
        reasoning_effort="max",
    )
    # the assistant should mention 215 and 222 that appear in the prior reasoning content
    print(f"response: {response.choices[0].message.reasoning}")
    return response.choices[0].message.content
```

For full guides and examples (vision input, structured output, partial mode, tool choice, dynamic tool loading, context caching), see the [Kimi K3 Quickstart](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart) and [Thinking Effort](https://platform.kimi.ai/docs/guide/use-thinking-effort).

### Coding Agent Framework

Kimi K3 works best with [Kimi Code CLI](https://www.kimi.com/code) as its agent framework. We warmly invite you to give it a try — run Kimi Code in your terminal and select Kimi K3 using the `/model` command. We hope you enjoy building with Kimi K3, and we would love to hear your feedback!


---

## 7. License

Both the code repository and the model weights are released under the [Kimi K3 License](https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE).

---

## 8. Contact Us

If you have any questions, please reach out at [support@moonshot.ai](mailto:support@moonshot.ai).
