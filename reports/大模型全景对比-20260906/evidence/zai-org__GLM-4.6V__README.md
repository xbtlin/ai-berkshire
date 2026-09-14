---
language:
- zh
- en
library_name: transformers
license: mit
pipeline_tag: image-text-to-text
---

# GLM-4.6V

<div align="center">
<img src=https://raw.githubusercontent.com/zai-org/GLM-V/refs/heads/main/resources/logo.svg width="40%"/>
</div>

This model is part of the GLM-V family of models, introduced in the paper [GLM-4.1V-Thinking and GLM-4.5V: Towards Versatile Multimodal Reasoning with Scalable Reinforcement Learning](https://huggingface.co/papers/2507.01006).

-   **GLM-4.6V Blog**: [https://z.ai/blog/glm-4.6v](https://z.ai/blog/glm-4.6v)
-   **Paper**: [https://huggingface.co/papers/2507.01006](https://huggingface.co/papers/2507.01006)
-   **GitHub Repository**: [https://github.com/zai-org/GLM-V](https://github.com/zai-org/GLM-V)
-   **Online Demo**: [https://chat.z.ai/](https://chat.z.ai/)
-   **API Access**: [Z.ai Open Platform](https://docs.z.ai/guides/vlm/glm-4.6v)
-   **Desktop Assistant App**: [https://huggingface.co/spaces/zai-org/GLM-4.5V-Demo-App](https://huggingface.co/spaces/zai-org/GLM-4.5V-Demo-App)

## Introduction

GLM-4.6V series model includes two versions: GLM-4.6V (106B), a foundation model designed for cloud and high-performance
cluster scenarios,
and GLM-4.6V-Flash (9B), a lightweight model optimized for local deployment and low-latency applications.
GLM-4.6V scales its context window to 128k tokens in training,
and achieves SoTA performance in visual understanding among models of similar parameter scales.
Crucially, we integrate native Function Calling capabilities for the first time.
This effectively bridges the gap between "visual perception" and "executable action"
providing a unified technical foundation for multimodal agents in real-world business scenarios.

![GLM-4.6V Benchmarks](https://raw.githubusercontent.com/zai-org/GLM-V/refs/heads/main/resources/bench_46v.jpeg)

Beyond achieves SoTA performance across major multimodal benchmarks at comparable model scales. GLM-4.6V introduces
several key features:

- **Native Multimodal Function Calling** 
Enables native vision-driven tool use. Images, screenshots, and document pages can be passed directly as tool inputs without text conversion, while visual outputs (charts, search images, rendered pages) are interpreted and integrated into the reasoning chain. This closes the loop from perception to understanding to execution.

- **Interleaved Image-Text Content Generation**
Supports high-quality mixed media creation from complex multimodal inputs. GLM-4.6V takes a multimodal context—spanning documents, user inputs, and tool-retrieved images—and synthesizes coherent, interleaved image-text content tailored to the task. During generation it can actively call search and retrieval tools to gather and curate additional text and visuals, producing rich, visually grounded content.


- **Multimodal Document Understanding**
GLM-4.6V can process up to 128K tokens of multi-document or long-document input, directly interpreting richly formatted pages as images. It understands text, layout, charts, tables, and figures jointly, enabling accurate comprehension of complex, image-heavy documents without requiring prior conversion to plain text.
    
- **Frontend Replication & Visual Editing** 
Reconstructs pixel-accurate HTML/CSS from UI screenshots and supports natural-language-driven edits. It detects layout, components, and styles visually, generates clean code, and applies iterative visual modifications through simple user instructions.


**This Hugging Face repository hosts the `GLM-4.6V` model, part of the `GLM-V` series.**

## Usage

### Environment Installation

For `SGLang`:

```bash
pip install sglang>=0.5.6.post1
pip install nvidia-cudnn-cu12==9.16.0.29
sudo apt update
sudo apt install ffmpeg
```

For `vLLM`:

```bash
pip install vllm>=0.12.0
pip install transformers>=5.0.0rc0
```

### Quick Start with Transformers

```python
from transformers import AutoProcessor, Glm4vMoeForConditionalGeneration
import torch

MODEL_PATH = "zai-org/GLM-4.6V"
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "url": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Grayscale_8bits_palette_sample_image.png"
            },
            {
                "type": "text",
                "text": "describe this image"
            }
        ],
    }
]
processor = AutoProcessor.from_pretrained(MODEL_PATH)
model = Glm4vMoeForConditionalGeneration.from_pretrained(
    pretrained_model_name_or_path=MODEL_PATH,
    torch_dtype="auto",
    device_map="auto",
)
inputs = processor.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_dict=True,
    return_tensors="pt"
).to(model.device)
inputs.pop("token_type_ids", None)
generated_ids = model.generate(**inputs, max_new_tokens=8192)
output_text = processor.decode(generated_ids[0][inputs["input_ids"].shape[1]:], skip_special_tokens=False)
print(output_text)
```

## Evaluation Settings

We primarily use vLLM as the backend for model inference. For faster and more reliable performance on video tasks, we employ SGLang. To reproduce our leaderboard results, we recommend the following decoding parameters:

+	top_p: 0.6
+	top_k: 2
+	temperature: 0.8
+	repetition_penalty: 1.1
+	max_generate_tokens: 16K

For more usage details, please refer to Our [Github](https://github.com/zai-org/GLM-V).

## Fixed and Remaining Issues

Since the open-sourcing of GLM-4.1V, we have received extensive feedback from the community and are well aware that the model still has many shortcomings. In subsequent iterations, we attempted to address several common issues — such as repetitive thinking outputs and formatting errors — which have been mitigated to some extent in this new version.

However, the model still has several limitations and issues that we will fix as soon as possible:

1. Pure text QA capabilities still have significant room for improvement. In this development cycle, our primary focus was on visual multimodal scenarios, and we will enhance pure text abilities in upcoming updates.
2. The model may still overthink or even repeat itself in certain cases, especially when dealing with complex prompts.
3. In some situations, the model may restate the answer again at the end.
4. There remain certain perception limitations, such as counting accuracy and identifying specific individuals, which still require improvement.

Thank you for your patience and understanding. We also welcome feedback and suggestions in the issue section — we will respond and improve as much as we can!

## Citation

If you use this model, please cite the following paper:

```bibtex
@misc{vteam2025glm45vglm41vthinkingversatilemultimodal,
      title={GLM-4.5V and GLM-4.1V-Thinking: Towards Versatile Multimodal Reasoning with Scalable Reinforcement Learning}, 
      author={V Team and Wenyi Hong and Wenmeng Yu and Xiaotao Gu and Guo Wang and Guobing Gan and Haomiao Tang and Jiale Cheng and Ji Qi and Junhui Ji and Lihang Pan and Shuaiqi Duan and Weihan Wang and Yan Wang and Yean Cheng and Zehai He and Zhe Su and Zhen Yang and Ziyang Pan and Aohan Zeng and Baoxu Wang and Bin Chen and Boyan Shi and Changyu Pang and Chenhui Zhang and Da Yin and Fan Yang and Guoqing Chen and Jiazheng Xu and Jiale Zhu and Jiali Chen and Jing Chen and Jinhao Chen and Jinghao Lin and Jinjiang Wang and Junjie Chen and Leqi Lei and Letian Gong and Leyi Pan and Mingdao Liu and Mingde Xu and Mingzhi Zhang and Qinkai Zheng and Sheng Yang and Shi Zhong and Shiyu Huang and Shuyuan Zhao and Siyan Xue and Shangqin Tu and Shengbiao Meng and Tianshu Zhang and Tianwei Luo and Tianxiang Hao and Tianyu Tong and Wenkai Li and Wei Jia and Xiao Liu and Xiaohan Zhang and Xin Lyu and Xinyue Fan and Xuancheng Huang and Yanling Wang and Yadong Xue and Yanfeng Wang and Yanzi Wang and Yifan An and Yifan Du and Yiming Shi and Yiheng Huang and Yilin Niu and Yuan Wang and Yuanchang Yue and Yuchen Li and Yutao Zhang and Yuting Wang and Yu Wang and Yuxuan Zhang and Zhao Xue and Zhenyu Hou and Zhengxiao Du and Zihan Wang and Peng Zhang and Debing Liu and Bin Xu and Juanzi Li and Minlie Huang and Yuxiao Dong and Jie Tang},
      year={2025},
      eprint={2507.01006},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2507.01006}, 
}
```