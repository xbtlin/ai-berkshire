# 开源盘古 Ultra-MoE-718B
中文 | [English](README_EN.md)

## 1. 简介
openPangu-Ultra-MoE-718B 是基于昇腾NPU从零训练的大规模混合专家语言模型，总参数量为718B，激活参数量为39B。openPangu-Ultra-MoE-718B 训练了约19T tokens，具备快慢思考融合能力。

## 2. 模型架构
openPangu-Ultra-MoE-718B 的模型架构采用了业界主流的Multi-head Latent Attention (MLA)、Multi-Token Prediction (MTP)、大稀疏比等架构，以及一些特有的设计：

- Depth-Scaled Sandwich-Norm和TinyInit：通过调整层归一化结构与参数初始化，提升训练稳定性。
- 基于EP-Group的负载均衡策略：通过优化负载均衡损失函数，改善专家特化效果。

## 3. 测评结果

|       测评集        |             测评指标             |  慢思考  |
|:----------------:|:----------------------------:|:-----:|
|     **通用能力**     |                              |       |
|      C-Eval      |             Acc              | 91.06 |
|     CLUEWSC      |             Acc              | 94.67 |
|     MMLU-Pro     |         Exact Match          | 82.40 |
|  ArenaHard_v0.1  |      w/o Style Control       | 96.80 |
|   GPQA-Diamond   |            Avg@4             | 76.77 |
|    SuperGPQA     |             Acc              | 61.67 |
|     IF-Eval      |        Prompt Strict         | 80.59 |
|     SysBench     | Constraint Satisfaction Rate | 91.43 |
|     **数学能力**     |                              |       |
|    CNMO 2024     |            Avg@32            | 80.73 |
|      AIME25      |            Avg@16            | 75.21 |
|      AIME24      |            Avg@16            | 80.21 |
|     MATH-500     |            Avg@1             | 97.40 |
|     **代码能力**     |                              |       |
|   LiveCodeBench  |     Avg@3 (01/25~05/25)      | 61.14 |
|      MBPP+       |            Avg@2             | 81.48 |

**注：** 评测过程中，system prompt 为空。


## 4. 部署和使用
### 4.1 环境准备
#### 硬件规格
Atlas 800T A2 (64GB, >=32卡)，驱动与固件安装包获取请参照[[Atlas 800T A2](https://www.hiascend.com/hardware/firmware-drivers/community?product=4&model=26&cann=8.2.RC1.alpha003&driver=Ascend+HDK+25.0.RC1)]

#### 软件环境
- 方式一：基于裸机环境安装以下配套软件
  - 操作系统：Linux（推荐openEuler>=24.03）
  - CANN==8.1.RC1，安装准备及流程请参照[[CANN Install](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha002/softwareinst/instg/instg_0001.html?Mode=PmIns&OS=Ubuntu&Software=cannToolKit)]
  - python==3.10
  - torch==2.1.0
  - torch-npu==2.1.0.post12
  - transformers>=4.48.2

- 方式二：从docker镜像启动容器 
  
  参考[[Docker使用指南](doc/docker.md)]

以上软件配套经过验证，理论可以支持更高的版本，如有疑问，可以提交issue。

### 4.2 权重完整性校验
请参考以下方法对下载内容进行完整性校验，hash 值存储在 checklist.chk 文件中。

```
#!/usr/bin/env bash
ARCH=$(uname -m)
MODEL_PATH="${TARGET_FOLDER}/${MODEL_FOLDER_PATH}"
cd "$MODEL_PATH" || exit 1
if [ "$ARCH" = "arm64" ]; then
    sha256sum checklist.chk
else
    sha256sum -c checklist.chk
fi
```

### 4.3 推理权重转换
本次样例 openPangu-Ultra-MoE-718B 推理采用 Tensor Parallel 并行策略，叠加昇腾 NPU 融合大算子，需要提前对 safetensors 权重进行切分，下述内容提供32卡并行推理的权重切分示例，切分后的权重会保存在`model/`目录下：
```bash
cd inference
bash split_weight.sh
```

### 4.4 推理样例
openPangu-Ultra-MoE-718B 在 Atlas 800T A2 上4机32卡bfloat16推理示例，主节点选取节点IP0：
```bash
cd inference
# 主节点IP0:  ${NNODES} ${NODE_RANK} ${NPROC_PER_NODE} ${MASTER_ADDR} ${PROMPT}
bash generate.sh 4 0 8 IP0 "3*7=?"
# 从节点IP1
bash generate.sh 4 1 8 IP0 "3*7=?"
# 从节点IP2
bash generate.sh 4 2 8 IP0 "3*7=?"
# 从节点IP3
bash generate.sh 4 3 8 IP0 "3*7=?"
```
模型默认为慢思考模式，可以通过以下手段切换至快思考模式：如`generate.py`示例中`fast_thinking_template`所示，在用户输入结尾添加` /no_think`标记可以将当前轮次切换至快思考模式。

### 4.5 使用推理框架
vllm_ascend：参考[[vllm_ascend_for_openPangu_ultra_moe_718b](doc/vllm_ascend_for_openpangu_ultra_moe_718b.md)]

## 5. 模型许可证
除文件中对开源许可证另有约定外，openPangu-Ultra-MoE-718B 模型根据 OPENPANGU MODEL LICENSE AGREEMENT VERSION 1.0 授权，旨在允许使用并促进人工智能技术的进一步发展。有关详细信息，请参阅模型存储库根目录中的 [LICENSE](LICENSE) 文件。

## 6. 免责声明
由于 openPangu-Ultra-MoE-718B （“模型”）所依赖的技术固有的限制，以及人工智能生成的内容是由盘古自动生成的，华为无法对以下事项做出任何保证：
- 该模型的输出通过AI算法自动生成，不能排除某些信息可能存在缺陷、不合理或引起不适的可能性，生成的内容不代表华为的态度或立场； 
- 无法保证该模型100%准确、可靠、功能齐全、及时、安全、无错误、不间断、持续稳定或无任何故障； 
- 该模型的输出内容不构成任何建议或决策，也不保证生成的内容的真实性、完整性、准确性、及时性、合法性、功能性或实用性。生成的内容不能替代医疗、法律等领域的专业人士回答您的问题。生成的内容仅供参考，不代表华为的任何态度、立场或观点。您需要根据实际情况做出独立判断，华为不承担任何责任。

## 7. 反馈
如果有任何意见和建议，请提交issue或联系[openPangu@huawei.com](url)。