---
language:
- en
- zh
library_name: transformers
license: mit
pipeline_tag: text-generation
---

# GLM-5

<div align="center">
<img src=https://raw.githubusercontent.com/zai-org/GLM-5/refs/heads/main/resources/logo.svg width="15%"/>
</div>
<p align="center">
    👋 Join our <a href="https://raw.githubusercontent.com/zai-org/GLM-5/refs/heads/main/resources/wechat.png" target="_blank">WeChat</a> or <a href="https://discord.gg/QR7SARHRxK" target="_blank">Discord</a> community.
    <br>
    📖 Check out the GLM-5 <a href="https://z.ai/blog/glm-5" target="_blank">technical blog</a>.
    <br>
    📍 Use GLM-5 API services on <a href="https://docs.z.ai/guides/llm/glm-5">Z.ai API Platform. </a>
    <br>
    👉 One click to <a href="https://chat.z.ai">GLM-5</a>.
</p>

<p align="center">
    [<a href="https://huggingface.co/papers/2602.15763" target="_blank">Paper</a>] 
    [<a href="https://github.com/zai-org/GLM-5" target="_blank">GitHub</a>]
</p>

## Introduction

We are launching GLM-5, targeting complex systems engineering and long-horizon agentic tasks. Scaling is still one of the most important ways to improve the intelligence efficiency of Artificial General Intelligence (AGI). Compared to GLM-4.5, GLM-5 scales from 355B parameters (32B active) to 744B parameters (40B active), and increases pre-training data from 23T to 28.5T tokens. GLM-5 also integrates DeepSeek Sparse Attention (DSA), largely reducing deployment cost while preserving long-context capacity.

Reinforcement learning aims to bridge the gap between competence and excellence in pre-trained models. However, deploying it at scale for LLMs is a challenge due to the RL training inefficiency. To this end, we developed [slime](https://github.com/THUDM/slime), a novel **asynchronous RL infrastructure** that substantially improves training throughput and efficiency, enabling more fine-grained post-training iterations. With advances in both pre-training and post-training, GLM-5 delivers significant improvement compared to GLM-4.7 across a wide range of academic benchmarks and achieves best-in-class performance among all open-source models in the world on reasoning, coding, and agentic tasks,  closing the gap with frontier models.

## Benchmark

|                                  | GLM-5                  | GLM-4.7   | DeepSeek-V3.2 | Kimi K2.5 | Claude Opus 4.5 | Gemini 3 Pro | GPT-5.2 (xhigh) |
| -------------------------------- | ---------------------- | --------- | ------------- |-----------| --------------- | ------------ | --------------- |
| HLE                              | 30.5                   | 24.8      | 25.1          | 31.5      | 28.4            | 37.2         | 35.4            |
| HLE (w/ Tools)                   | 50.4                   | 42.8      | 40.8          | 51.8      | 43.4*           | 45.8*        | 45.5*           |
| AIME 2026 I                      | 92.7                   | 92.9      | 92.7          | 92.5      | 93.3            | 90.6         | -               |
| HMMT Nov. 2025                   | 96.9                   | 93.5      | 90.2          | 91.1      | 91.7            | 93.0         | 97.1            |
| IMOAnswerBench                   | 82.5                   | 82.0      | 78.3          | 81.8      | 78.5            | 83.3         | 86.3            |
| GPQA-Diamond                     | 86.0                   | 85.7      | 82.4          | 87.6      | 87.0            | 91.9         | 92.4            |
| SWE-bench Verified               | 77.8                   | 73.8      | 73.1          | 76.8      | 80.9            | 76.2         | 80.0            |
| SWE-bench Multilingual           | 73.3                   | 66.7      | 70.2          | 73.0      | 77.5            | 65.0         | 72.0            |
| Terminal-Bench 2.0 (Terminus 2)  | 56.2 / 60.7 † | 41.0      | 39.3          | 50.8      | 59.3            | 54.2         | 54.0            |
| Terminal-Bench 2.0 (Claude Code) | 56.2 / 61.1 †  | 32.8      | 46.4          | -         | 57.9            | -            | -               |
| CyberGym                         | 43.2                   | 23.5      | 17.3          | 41.3      | 50.6            | 39.9         | -               |
| BrowseComp                       | 62.0                   | 52.0      | 51.4          | 60.6      | 37.0            | 37.8         | -               |
| BrowseComp (w/ Context Manage)   | 75.9                   | 67.5      | 67.6          | 74.9      | 67.8            | 59.2         | 65.8            |
| BrowseComp-Zh                    | 72.7                   | 66.6      | 65.0          | 62.3      | 62.4            | 66.8         | 76.1            |
| τ²-Bench                         | 89.7                   | 87.4      | 85.3          | 80.2      | 91.6            | 90.7         | 85.5            |
| MCP-Atlas (Public Set)           | 67.8                   | 52.0      | 62.2          | 63.8      | 65.2            | 66.6         | 68.0            |
| Tool-Decathlon                   | 38.0                   | 23.8      | 35.2          | 27.8      | 43.5            | 36.4         | 46.3            |
| Vending Bench 2                  | $4,432.12              | $2,376.82 | $1,034.00     | $1,198.46 | $4,967.06       | $5,478.16    | $3,591.33       |

> *: refers to their scores of full set.
> 
> †: A verified version of Terminal-Bench 2.0 that fixes some ambiguous instructions.
See footnote for more evaluation details.

### Footnote

* **Humanity’s Last Exam (HLE) & other reasoning tasks**: We evaluate with a maximum generation length of 131,072 tokens (`temperature=1.0, top_p=0.95, max_new_tokens=131072`). By default, we report the text-only subset; results marked with * are from the full set. We use GPT-5.2 (medium) as the judge model. For HLE-with-tools, we use a maximum context length of 202,752 tokens.
* **SWE-bench & SWE-bench Multilingual**: We run the SWE-bench suite with OpenHands using a tailored instruction prompt. Settings: `temperature=0.7, top_p=0.95, max_new_tokens=16384`, with a 200K context window.
* **BrowserComp**: Without context management, we retain details from the most recent 5 turns. With context management, we use the same discard-all strategy as DeepSeek-v3.2 and Kimi K2.5.
* **Terminal-Bench 2.0 (Terminus 2)**: We evaluate with the Terminus framework using `timeout=2h, temperature=0.7, top_p=1.0, max_new_tokens=8192`, with a 128K context window. Resource limits are capped at 16 CPUs and 32 GB RAM.
* **Terminal-Bench 2.0 (Claude Code)**: We evaluate in Claude Code 2.1.14 (think mode, default effort) with `temperature=1.0, top_p=0.95, max_new_tokens=65536`. We remove wall-clock time limits due to generation speed, while preserving per-task CPU and memory constraints. Scores are averaged over 5 runs. We fix environment issues introduced by Claude Code and also report results on a verified Terminal-Bench 2.0 dataset that resolves ambiguous instructions (see: [https://huggingface.co/datasets/zai-org/terminal-bench-2-verified](https://huggingface.co/datasets/zai-org/terminal-bench-2-verified)).
* **CyberGym**: We evaluate in Claude Code 2.1.18 (think mode, no web tools) with (`temperature=1.0, top_p=1.0, max_new_tokens=32000`) and a 250-minute timeout per task. Results are single-run Pass@1 over 1,507 tasks.
* **MCP-Atlas**: All models are evaluated in think mode on the 500-task public subset with a 10-minute timeout per task. We use Gemini 3 Pro as the judge model.
* **τ²-bench**: We add a small prompt adjustment in Retail and Telecom to avoid failures caused by premature user termination. For Airline, we apply the domain fixes proposed in the Claude Opus 4.5 system card.
* **Vending Bench 2**: Runs are conducted independently by [Andon Labs](https://andonlabs.com/evals/vending-bench-2).


## Serve GLM-5 Locally

### Prepare environment

The following open-source frameworks support local deployment of GLM-5:

- [vLLM](https://github.com/vllm-project/vllm) (v0.19.0+)
- [SGLang](https://github.com/sgl-project/sglang) (v0.5.10+)
- [KTransformers](https://github.com/kvcache-ai/ktransformers) (v0.5.3+)
- [Transformers](https://github.com/huggingface/transformers) (v0.5.4+)
- [xLLM](https://github.com/jd-opensource/xllm) (v0.8.0+)

### Deploy

+ vLLM

    ```shell
    vllm serve zai-org/GLM-5 \
         --tensor-parallel-size 8 \
         --gpu-memory-utilization 0.85 \
         --speculative-config.method mtp \
         --speculative-config.num_speculative_tokens 3 \
         --tool-call-parser glm47 \
         --reasoning-parser glm45 \
         --enable-auto-tool-choice \
         --served-model-name glm-5
    ```

    Check the [recipes](https://github.com/vllm-project/recipes/blob/main/GLM/GLM5.md) for more details.

+ SGLang

    ```shell
    sglang serve \
      --model-path zai-org/GLM-5 \
      --tp-size 8 \
      --tool-call-parser glm47  \
      --reasoning-parser glm45 \
      --speculative-algorithm EAGLE \
      --speculative-num-steps 3 \
      --speculative-eagle-topk 1 \
      --speculative-num-draft-tokens 4 \
      --mem-fraction-static 0.85 \
      --served-model-name glm-5
    ```
  
    Check the [sglang cookbook](https://cookbook.sglang.io/autoregressive/GLM/GLM-5) for more details.

+ xLLM and other Ascend NPU

    Please check the deployment guide [here](https://github.com/zai-org/GLM-5/blob/main/example/ascend.md).

+ KTransformers

    Please check the deployment guide [here](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/kt-kernel/GLM-5-Tutorial.md).

## Citation

If you find GLM-5 useful in your research, please cite our technical report:

```bibtex
@misc{glm5team2026glm5vibecodingagentic,
      title={GLM-5: from Vibe Coding to Agentic Engineering},
      author={GLM-5-Team and : and Aohan Zeng and Xin Lv and Zhenyu Hou and Zhengxiao Du and Qinkai Zheng and Bin Chen and Da Yin and Chendi Ge and Chenghua Huang and Chengxing Xie and Chenzheng Zhu and Congfeng Yin and Cunxiang Wang and Gengzheng Pan and Hao Zeng and Haoke Zhang and Haoran Wang and Huilong Chen and Jiajie Zhang and Jian Jiao and Jiaqi Guo and Jingsen Wang and Jingzhao Du and Jinzhu Wu and Kedong Wang and Lei Li and Lin Fan and Lucen Zhong and Mingdao Liu and Mingming Zhao and Pengfan Du and Qian Dong and Rui Lu and Shuang-Li and Shulin Cao and Song Liu and Ting Jiang and Xiaodong Chen and Xiaohan Zhang and Xuancheng Huang and Xuezhen Dong and Yabo Xu and Yao Wei and Yifan An and Yilin Niu and Yitong Zhu and Yuanhao Wen and Yukuo Cen and Yushi Bai and Zhongpei Qiao and Zihan Wang and Zikang Wang and Zilin Zhu and Ziqiang Liu and Zixuan Li and Bojie Wang and Bosi Wen and Can Huang and Changpeng Cai and Chao Yu and Chen Li and Chengwei Hu and Chenhui Zhang and Dan Zhang and Daoyan Lin and Dayong Yang and Di Wang and Ding Ai and Erle Zhu and Fangzhou Yi and Feiyu Chen and Guohong Wen and Hailong Sun and Haisha Zhao and Haiyi Hu and Hanchen Zhang and Hanrui Liu and Hanyu Zhang and Hao Peng and Hao Tai and Haobo Zhang and He Liu and Hongwei Wang and Hongxi Yan and Hongyu Ge and Huan Liu and Huanpeng Chu and Jia'ni Zhao and Jiachen Wang and Jiajing Zhao and Jiamin Ren and Jiapeng Wang and Jiaxin Zhang and Jiayi Gui and Jiayue Zhao and Jijie Li and Jing An and Jing Li and Jingwei Yuan and Jinhua Du and Jinxin Liu and Junkai Zhi and Junwen Duan and Kaiyue Zhou and Kangjian Wei and Ke Wang and Keyun Luo and Laiqiang Zhang and Leigang Sha and Liang Xu and Lindong Wu and Lintao Ding and Lu Chen and Minghao Li and Nianyi Lin and Pan Ta and Qiang Zou and Rongjun Song and Ruiqi Yang and Shangqing Tu and Shangtong Yang and Shaoxiang Wu and Shengyan Zhang and Shijie Li and Shuang Li and Shuyi Fan and Wei Qin and Wei Tian and Weining Zhang and Wenbo Yu and Wenjie Liang and Xiang Kuang and Xiangmeng Cheng and Xiangyang Li and Xiaoquan Yan and Xiaowei Hu and Xiaoying Ling and Xing Fan and Xingye Xia and Xinyuan Zhang and Xinze Zhang and Xirui Pan and Xu Zou and Xunkai Zhang and Yadi Liu and Yandong Wu and Yanfu Li and Yidong Wang and Yifan Zhu and Yijun Tan and Yilin Zhou and Yiming Pan and Ying Zhang and Yinpei Su and Yipeng Geng and Yong Yan and Yonglin Tan and Yuean Bi and Yuhan Shen and Yuhao Yang and Yujiang Li and Yunan Liu and Yunqing Wang and Yuntao Li and Yurong Wu and Yutao Zhang and Yuxi Duan and Yuxuan Zhang and Zezhen Liu and Zhengtao Jiang and Zhenhe Yan and Zheyu Zhang and Zhixiang Wei and Zhuo Chen and Zhuoer Feng and Zijun Yao and Ziwei Chai and Ziyuan Wang and Zuzhou Zhang and Bin Xu and Minlie Huang and Hongning Wang and Juanzi Li and Yuxiao Dong and Jie Tang},
      year={2026},
      eprint={2602.15763},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2602.15763},
}
```