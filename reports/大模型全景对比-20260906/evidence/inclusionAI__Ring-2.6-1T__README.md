---
pipeline_tag: text-generation
license: mit
library_name: transformers
---

<p align="center">
    <img src="https://mdn.alipayobjects.com/huamei_qa8qxu/afts/img/A*4QxcQrBlTiAAAAAAQXAAAAgAemJ7AQ/original" width="100"/>
</p>

<p align="center">🤗 <a href="https://huggingface.co/inclusionAI">Hugging Face</a>&nbsp;&nbsp; | &nbsp;&nbsp;🤖 <a href="https://modelscope.cn/organization/inclusionAI">ModelScope </a>&nbsp;&nbsp; | &nbsp;&nbsp;🐙 <a href="https://ling.tbox.cn/chat">ling.tbox.cn</a>&nbsp;&nbsp; | &nbsp;&nbsp; <a href="https://arxiv.org/abs/2606.15079">Tech Report </a></p>

# Ring-2.6-1T

Introducing Ring-2.6-1T: a trillion-parameter flagship reasoning model designed for real-world complex task scenarios, making it available to developers, researchers, and enterprise environments for validation, adaptation, and further development.

The goal of Ring-2.6-1T is not simply to pursue larger parameter scale , but to address the real production environments that large models are entering: agent workflows, engineering development, scientific research analysis, complex business systems, and enterprise automation processes. In these scenarios, models need not only to "answer questions," but also to understand context, plan steps, invoke tools, execute continuously, and maintain stability over long-horizon tasks.

Ring-2.6-1T has achieved key upgrade in three areas:

* Comprehensively enhanced Agent execution capability: Moving from "being able to answer" to "being able to execute," with more stable performance in multi-step tasks, tool collaboration, contextual planning, and advancing complex workflows.

* Reasoning Effort mechanism: Supporting two reasoning intensity levels, high and xhigh, allowing developers to flexibly adjust the depth of thinking according to task complexity, achieving a better balance among effectiveness, speed, and cost.

* Innovative asynchronous reinforcement learning training paradigm: Leveraging an Async RL architecture combined with the IcePop algorithm to improve the training efficiency and stability of long-horizon reinforcement learning for trillion-parameter models, providing foundational support for agent capabilities and complex reasoning.

<p align="center">
    <img src="https://mdn.alipayobjects.com/huamei_d2byvp/afts/img/SSFgSJxTFPgAAAAAgDAAAAgADod9AQFr/original" />
</p>

## Model Downloads

You can download Ring-2.6-1T from the following table. If you are located in mainland China, we also provide the model on ModelScope to speed up the download process.

<center>

|  **Model**  | **Context Length** |                                                                     **Download**                                                                      |
| :---------: | :----------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------: |
| Ring-2.6-1T | 128K -> 256K (YaRN) | [🤗 HuggingFace](https://huggingface.co/inclusionAI/Ring-2.6-1T) &nbsp;&nbsp; [🤖 ModelScope](https://www.modelscope.cn/models/inclusionAI/Ring-2.6-1T) |
</center>

Note: If you are interested in the previous version, please visit the past model collections on [Huggingface](https://huggingface.co/inclusionAI) or [ModelScope](https://modelscope.cn/organization/inclusionAI).

## Agent Capability: From "Understanding Tasks" to "Continuously Executing Tasks"

In real business systems, models often face not isolated Q&A, but continuous, multi-turn, complex tasks that require tool collaboration. Ring-2.6-1T has been specifically enhanced for such scenarios, enabling more stable task decomposition, step planning, tool invocation, error correction, and context continuation.

Looking at benchmark results, Ring-2.6-1T high demonstrates outstanding performance in real-world task execution evaluations: achieving 87.60 on PinchBench, notably higher than GPT-5.4 xHigh and Gemini-3.1-Pro high; scoring 63.82 on ClawEval, ranking among the top comparable models; and reaching 95.32 on Tau2-Bench in the Telecom scenario, with a gap of less than 1 point from the highest-scoring model, demonstrating its stable execution capability in complex business processes, tool collaboration, and industry-specific tasks.

This means that Ring-2.6-1T not only understands user intent but can also continuously drive tasks forward in real workflows. Whether in personal assistant agents, enterprise process automation, or code generation, task decomposition, and engineering collaboration in coding agent scenarios, Ring-2.6-1T functions more like a workflow engine that is executable, responsive to feedback, and capable of iteration.

## Reasoning Effort: High and xHigh Configurations — Fast When Needed, Deep When Required

In practice, not all tasks require the same level of reasoning resources. A format conversion or information organization task has entirely different demands on the model's depth of thinking compared to a math competition problem or a complex system analysis.

To address this, Ring-2.6-1T introduces an adjustable Reasoning Effort mechanism, supporting two reasoning effort levels: high and xhigh.

* high is designed for high-frequency agent workflows, suitable for multi-turn interactions, tool collaboration, task decomposition, and production-grade default invocation. It maintains a high task completion rate while reducing unnecessary reasoning token overhead, making the model faster, more stable, and more cost-effective in real-world workflows.

* xhigh is tailored for high-difficulty tasks such as mathematics, scientific research, complex logical analysis, and multi-path exploration, granting the model more extensive reasoning space. In challenging reasoning benchmarks, Ring-2.6-1T xhigh demonstrates strong capability ceilings: scoring 66.18 on ARC-AGI-V2, surpassing Gemini-3.1-Pro high and Claude-Opus-4.7 xhigh; achieving 95.83 on AIME 26, on par with multiple leading models; and reaching 88.27 on GPQA Diamond, reflecting robust professional knowledge comprehension and complex reasoning capabilities.

With the high and xhigh configuration options, developers can dynamically allocate reasoning resources based on task characteristics: use high for everyday workflows to achieve greater efficiency, and switch to xhigh for complex reasoning tasks to unlock the model's full capability ceiling.

## Asynchronous Async RL Training + IcePop Algorithm: Supporting Stable Reinforcement Learning for Trillion-Parameter Models

Conducting reinforcement learning training on trillion-parameter models is itself an enormous engineering challenge. In traditional synchronous RL training, policy generation (rollout) and gradient updates are tightly coupled, leading to:

* GPU waiting: Low GPU resource utilization, with substantial computational power wasted on synchronization waits;

* Insufficient training throughput: Prolonged training cycles with limited iteration speed;

* Instability in long-horizon training: Prone to policy collapse or reward signal degradation during extended training.

Ring-2.6-1T adopts an asynchronous (Async) reinforcement learning training architecture, decoupling policy sampling and parameter updates into independent pipelines, achieving:

* Significantly improved training throughput and resource utilization: Sampling and updates execute in parallel, dramatically increasing GPU utilization and boosting training efficiency by several times;
* Support for longer training cycles: The decoupled architecture is inherently suited for large-scale, long-duration continuous training, eliminating training interruptions caused by synchronization bottlenecks.

Building on this, we apply the IcePop algorithm from Ring-1T to the async RL training process, addressing training instability. This innovation in the training paradigm enables us to conduct sufficient and stable reinforcement learning optimization on trillion-parameter models, pushing both agent execution capabilities and reasoning capabilities to new ceilings. We will release the details of the Stick-Breaking algorithm combined with Async architecture in our upcoming technical report.



## Quickstart

### 🚀 Try Online

[https://ling.tbox.cn/chat](https://ling.tbox.cn/chat)


## Deployment


### SGLang

#### Environment Preparation

We will later submit our model to SGLang official release, now we can prepare the environment following steps:
```shell
git clone -b ling_2_5 git@github.com:antgroup/sglang.git
cd sglang

# Install the python packages
pip install --upgrade pip
pip install -e "python"
```

#### Run Inference

Both BF16 and FP8 models are supported by SGLang now. It depends on the dtype of the model in ${MODEL_PATH}.

Here is the example to run Ring-2.6-1T with multiple GPU nodes, where the master node IP is ${MASTER_IP} and server port is ${PORT}:

- Start server:
```bash
# Node 0:
python -m sglang.launch_server --model-path $MODEL_PATH --tp-size 8 --pp-size 4 --dp-size 1 --trust-remote-code --dist-init-addr $MASTER_IP:2345 --port $PORT --nnodes 4 --node-rank 0 
# Node 1:
python -m sglang.launch_server --model-path $MODEL_PATH --tp-size 8 --pp-size 4 --dp-size 1 --trust-remote-code --dist-init-addr $MASTER_IP:2345 --port $PORT --nnodes 4 --node-rank 1 
# Node 2:
python -m sglang.launch_server --model-path $MODEL_PATH --tp-size 8 --pp-size 4 --dp-size 1 --trust-remote-code --dist-init-addr $MASTER_IP:2345 --port $PORT --nnodes 4 --node-rank 2 
# Node 3:
python -m sglang.launch_server --model-path $MODEL_PATH --tp-size 8 --pp-size 4 --dp-size 1 --trust-remote-code --dist-init-addr $MASTER_IP:2345 --port $PORT --nnodes 4 --node-rank 3

# This is only an example. Please adjust arguments according to your actual environment.
```

- Client:

```shell
curl -s http://${MASTER_IP}:${PORT}/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "auto", "messages": [{"role": "user", "content": "What is the capital of France?"}]}'
```


## License

This code repository is licensed under [the MIT License](https://github.com/inclusionAI/Ring-V2.5/blob/main/LICENSE).

![--](https://ospo-insights.oss-cn-hangzhou.aliyuncs.com/iai-hf-models/Ring-2.5-1T.gif)