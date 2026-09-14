---
language:
- en
pipeline_tag: text-generation
library_name: transformers

license: other
license_name: tencent-license
license_link: https://huggingface.co/tencent/Tencent-Hunyuan-Large/blob/main/LICENSE.txt
---

<p align="center">
 <img src="https://dscache.tencent-cloud.cn/upload/uploader/hunyuan-64b418fd052c033b228e04bc77bbc4b54fd7f5bc.png" width="400"/> <br>
</p><p></p>

<p align="center">
    &nbsp<a href="https://github.com/Tencent/Tencent-Hunyuan-Large"><b>GITHUB</b></a>&nbsp&nbsp |  &nbsp&nbsp🖥️&nbsp&nbsp<a href="https://llm.hunyuan.tencent.com/" style="color: blue;"><b>official website</b></a>&nbsp&nbsp｜&nbsp&nbsp🕖&nbsp&nbsp <a href="https://cloud.tencent.com/product/hunyuan" ><b>HunyuanAPI</b></a>｜&nbsp&nbsp🐳&nbsp&nbsp <a href="https://gitee.com/Tencent/Tencent-Hunyuan-Large" ><b>Gitee</b></a>
</p><p align="center">
    <a href="https://arxiv.org/abs/2411.02265" style="color: blue;"><b>Technical Report</b></a>&nbsp&nbsp｜&nbsp&nbsp <a href="https://huggingface.co/spaces/tencent/Hunyuan-Large"><b>Demo</b></a>&nbsp&nbsp&nbsp｜&nbsp&nbsp <a href="https://cloud.tencent.com/document/product/851/112032" style="color: blue;"><b>Tencent Cloud TI</b></a>&nbsp&nbsp&nbsp</p>



<p>
    <table align="center">
        <tbody>
            <tr align="center">
                <td align="center" colspan="3"><strong>Download Models</strong></td>
            </tr>
            <tr align="center">
                <td align="center" style="width: 200px;" ><strong>Models</strong></td>
                <td align="center" style="width: 400px;"><strong>Huggingface Download URL</strong></td>
                <td align="center" style="width: 400px;"><strong>Tencent Cloud Download URL</strong></td>
            </tr>
            <tr align="center">  
                <td align="center" style="width: 200px;">Hunyuan-A52B-Instruct-FP8</td>
                <td style="width: 400px;"><a href="https://huggingface.co/tencent/Tencent-Hunyuan-Large/tree/main/Hunyuan-A52B-Instruct-FP8" ;">Hunyuan-A52B-Instruct-FP8</a></td>
                <td style="width: 400px;"><a href="https://cdn-large-model.hunyuan.tencent.com/Hunyuan-A52B-Instruct-128k-fp8-20241116.zip" ;">Hunyuan-A52B-Instruct-FP8</a></td>
            </tr>
            <tr align="center">
                <td align="center" style="width: 200px;">Hunyuan-A52B-Instruct</td>
                <td style="width: 400px;"><a href="https://huggingface.co/tencent/Tencent-Hunyuan-Large/tree/main/Hunyuan-A52B-Instruct" ;">Hunyuan-A52B-Instruct</a></td>
                <td style="width: 400px;"><a href="https://cdn-large-model.hunyuan.tencent.com/Hunyuan-A52B-Instruct-128k-20241116.zip" ;">Hunyuan-A52B-Instruct</a></td>
            </tr>
            <tr align="center">
                <td align="center" style="width: 200px;">Hunyuan-A52B-Pretrain</td>
                <td style="width: 400px;"><a href="https://huggingface.co/tencent/Tencent-Hunyuan-Large/tree/main/Hunyuan-A52B-Pretrain" ;">Hunyuan-A52B-Pretrain</a></td>
                <td style="width: 400px;"><a href="https://cdn-large-model.hunyuan.tencent.com/Hunyuan-A52B-Pretrain-256k.zip" ;">Hunyuan-A52B-Pretrain</a></td>
            </tr>
        </tbody>
    </table>
</p>


### Model Introduction

With the rapid development of artificial intelligence technology, large language models (LLMs) have made significant progress in fields such as natural language processing, computer vision, and scientific tasks. However, as the scale of these models increases, optimizing resource consumption while maintaining high performance has become a key challenge. To address this challenge, we have explored Mixture of Experts (MoE) models. The currently unveiled Hunyuan-Large (Hunyuan-MoE-A52B) model is the largest open-source Transformer-based MoE model in the industry, featuring a total of 389 billion parameters and 52 billion active parameters. This is currently the largest open-source Transformer-based MoE model in the industry, featuring a total of 389 billion parameters and 52 billion active parameters. 

By open-sourcing the Hunyuan-Large model and revealing related technical details, we hope to inspire more researchers with innovative ideas and collectively advance the progress and application of AI technology. We welcome you to join our open-source community to explore and optimize future AI models together!
 
### Introduction to Model Technical Advantages

#### Model
- **High-Quality Synthetic Data**: By enhancing training with synthetic data, Hunyuan-Large can learn richer representations, handle long-context inputs, and generalize better to unseen data.

- **KV Cache Compression**: Utilizes Grouped Query Attention (GQA) and Cross-Layer Attention (CLA) strategies to significantly reduce memory usage and computational overhead of KV caches, improving inference throughput.

- **Expert-Specific Learning Rate Scaling**: Sets different learning rates for different experts to ensure each sub-model effectively learns from the data and contributes to overall performance.

- **Long-Context Processing Capability**: The pre-trained model supports text sequences up to 256K, and the Instruct model supports up to 128K, significantly enhancing the ability to handle long-context tasks.

- **Extensive Benchmarking**: Conducts extensive experiments across various languages and tasks to validate the practical effectiveness and safety of Hunyuan-Large.


&nbsp;

## Benchmark Evaluation

**Hunyuan-Large pre-trained model** achieves the best overall performance compared to both Dense and MoE based 
competitors having similar activated parameter sizes.  For aggregated benchmarks such as MMLU, MMLU-Pro, and CMMLU, 
Hunyuan-Large consistently achieves the best performance, confirming its comprehensive abilities on aggregated tasks.
Hunyuan-Large also shows superior performance in commonsense understanding and reasoning, and classical NLP tasks 
such as QA and reading comprehension tasks (e.g., CommonsenseQA, PIQA and TriviaQA).  
For the mathematics capability, Hunyuan-Large outperforms all baselines in math datasets of GSM8K and MATH, 
and also gains the best results on CMATH in Chinese.We also observe that Hunyuan-Large achieves the overall 
best performance in all Chinese tasks (e.g., CMMLU, C-Eval).

| Model            | LLama3.1-405B | LLama3.1-70B | Mixtral-8x22B | DeepSeek-V2 | Hunyuan-Large |
|------------------|---------------|--------------|---------------|-------------|---------------|
| MMLU             | 85.2          | 79.3         | 77.8          | 78.5        | **88.4**          |
| MMLU-Pro         | **61.6**          | 53.8         | 49.5          | -           | 60.2          |
| BBH              | 85.9          | 81.6         | 78.9          | 78.9        | **86.3**          |
| HellaSwag        | -             | -            | **88.7**      | 87.8        | 86.8          |
| CommonsenseQA    | 85.8          | 84.1         | 82.4          | -           | **92.9**          |
| WinoGrande       | 86.7          | 85.3         | 85.0          | 84.9        | **88.7**          |
| PIQA             | -             | -            | 83.6          | 83.7        | **88.3**          |
| NaturalQuestions | -             | -            | 39.6          | 38.7        | **52.8**          |
| DROP             | 84.8          | 79.6         | 80.4          | 80.1        | **88.9**          |
| ARC-C            | **96.1**          | 92.9         | 91.2          | 92.4        | 95.0          |
| TriviaQA         | -             | -            | 82.1          | 79.9        | **89.2**          |
| CMMLU            | -             | -            | 60.0          | 84.0        | **90.2**          |
| C-Eval           | -             | -            | 59.6          | 81.7        | **91.9**          |
| C3               | -             | -            | 71.4          | 77.4        | **82.3**          |
| GSM8K            | 89.0          | 83.7         | 83.7          | 79.2        | **92.8**          |
| MATH             | 53.8          | 41.4         | 42.5          | 43.6        | **69.8**          |
| CMATH            | -             | -            | 72.3          | 78.7        | **91.3**          |
| HumanEval        | 61.0          | 58.5         | 53.1          | 48.8        | **71.4**          |
| MBPP             | **73.4**          | 68.6         | 64.2          | 66.6        | 72.6          |

**Hunyuan-Large-Instruct** achieves consistent improvements on most types of tasks compared to LLMs having similar 
activated parameters, indicating the effectiveness of our post-training.    Delving into the model performance 
in different categories of benchmarks, we find that our instruct model achieves the best performance on MMLU and MATH dataset.  
Notably, on the MMLU dataset, our model demonstrates a significant improvement, outperforming the LLama3.1-405B model by 2.6%.   
This enhancement is not just marginal but indicative of the Hunyuan-Large-Instruct’s superior understanding and reasoning 
capabilities across a wide array of language understanding tasks. The model’s prowess is further underscored in its performance 
on the MATH dataset, where it surpasses the LLama3.1-405B by a notable margin of 3.6%.  
Remarkably, this leap in accuracy is achieved with only 52 billion activated parameters, underscoring the efficiency of our model.

| Model                | LLama3.1 405B Inst. | LLama3.1 70B Inst. | Mixtral 8x22B Inst. | DeepSeekV2.5 Chat | Hunyuan-Large Inst. |
|----------------------|---------------------|--------------------|---------------------|-------------------|---------------------|
| MMLU                 | 87.3                | 83.6               | 77.8                | 80.4              | **89.9**            |
| CMMLU                | -                   | -                  | 61.0                | -                 | **90.4**            |
| C-Eval               | -                   | -                  | 60.0                | -                 | **88.6**            |
| BBH                  | -                   | -                  | 78.4                | 84.3              | **89.5**            |
| HellaSwag            | -                   | -                  | 86.0                | **90.3**          | 88.5                |
| ARC-C                | **96.9**            | 94.8               | 90.0                | -                 | 94.6                |
| GPQA_diamond         | **51.1**            | 46.7               | -                   | -                 | 42.4                |
| MATH                 | 73.8                | 68.0               | 49.8                | 74.7              | **77.4**            |
| HumanEval            | 89.0                | 80.5               | 75.0                | 89.0              | **90.0**            |
| AlignBench           | 6.0                 | 5.9                | 6.2                 | 8.0               | **8.3**             |
| MT-Bench             | 9.1                 | 8.8                | 8.1                 | 9.0               | **9.4**             |
| IFEval strict-prompt | **86.0**            | 83.6               | 71.2                | -                 | 85.0                |
| Arena-Hard |  69.3            | 55.7               |  -                | 76.2                 | **81.8**            |
| AlpacaEval-2.0 | 39.3            | 34.3               | 30.9                | 50.5                 | **51.8**            |


## Quick Start

You can quickly get started by referring to the content in the <a href="https://github.com/Tencent/Tencent-Hunyuan-Large/tree/main/examples">Quick Start Guide</a>.


## Inference and Deployment

HunyuanLLM uses TRT-LLM and vLLM for deployment. We are open sourcing the vLLM deployment (see Reasoning with vLLM), and the TRT-LLM deployment (see Reasoning with TRT-LLM) will be available in the near future.

Learn More at <a href="https://github.com/Tencent/Tencent-Hunyuan-Large">Tencent-Hunyuan-Large</a>.


### Citation
If you find our work helpful, feel free to give us a cite.

```
@misc{sun2024hunyuanlargeopensourcemoemodel,
      title={Hunyuan-Large: An Open-Source MoE Model with 52 Billion Activated Parameters by Tencent}, 
      author={Xingwu Sun and Yanfeng Chen and Yiqing Huang and Ruobing Xie and Jiaqi Zhu and Kai Zhang and Shuaipeng Li and Zhen Yang and Jonny Han and Xiaobo Shu and Jiahao Bu and Zhongzhi Chen and Xuemeng Huang and Fengzong Lian and Saiyong Yang and Jianfeng Yan and Yuyuan Zeng and Xiaoqin Ren and Chao Yu and Lulu Wu and Yue Mao and Tao Yang and Suncong Zheng and Kan Wu and Dian Jiao and Jinbao Xue and Xipeng Zhang and Decheng Wu and Kai Liu and Dengpeng Wu and Guanghui Xu and Shaohua Chen and Shuang Chen and Xiao Feng and Yigeng Hong and Junqiang Zheng and Chengcheng Xu and Zongwei Li and Xiong Kuang and Jianglu Hu and Yiqi Chen and Yuchi Deng and Guiyang Li and Ao Liu and Chenchen Zhang and Shihui Hu and Zilong Zhao and Zifan Wu and Yao Ding and Weichao Wang and Han Liu and Roberts Wang and Hao Fei and Peijie She and Ze Zhao and Xun Cao and Hai Wang and Fusheng Xiang and Mengyuan Huang and Zhiyuan Xiong and Bin Hu and Xuebin Hou and Lei Jiang and Jiajia Wu and Yaping Deng and Yi Shen and Qian Wang and Weijie Liu and Jie Liu and Meng Chen and Liang Dong and Weiwen Jia and Hu Chen and Feifei Liu and Rui Yuan and Huilin Xu and Zhenxiang Yan and Tengfei Cao and Zhichao Hu and Xinhua Feng and Dong Du and Tinghao She and Yangyu Tao and Feng Zhang and Jianchen Zhu and Chengzhong Xu and Xirui Li and Chong Zha and Wen Ouyang and Yinben Xia and Xiang Li and Zekun He and Rongpeng Chen and Jiawei Song and Ruibin Chen and Fan Jiang and Chongqing Zhao and Bo Wang and Hao Gong and Rong Gan and Winston Hu and Zhanhui Kang and Yong Yang and Yuhong Liu and Di Wang and Jie Jiang},
      year={2024},
      eprint={2411.02265},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2411.02265}, 
}
```


