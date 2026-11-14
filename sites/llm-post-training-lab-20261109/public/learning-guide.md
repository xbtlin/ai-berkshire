# LLM 后训练系统学习导读

资料核验截止：2026-11-09。面向已有深度学习基础、希望掌握 SFT / DPO / RL 的学习者。

## 如何使用

以 RLHF Book 为主教材、Hugging Face 为实践入口、Stanford 为进阶补充。这里的“精选”是按一手性、系统性、可实践性和维护状况作出的编辑判断，不是客观全网排名。主线阅读资料免费，真实训练算力另计。

建议八周，每周约 6–10 小时，结课项目可能需要 8–12 小时；均为学习规划估计，不含长训练等待。先读本周导读，再到文末来源中查对应主题，完成验收任务与自测。

## 核心分类

- SFT / DPO / PPO / GRPO：训练目标或算法。
- LoRA / QLoRA：参数更新与显存策略，可搭配不同目标。
- RLHF / RLAIF / RLVR：人类反馈、AI 反馈与可验证奖励等反馈范式。
- 离线 DPO：固定偏好对；在线 RL：反复用当前或近期策略生成 rollout。异步生成、batch 内多次更新和引擎差异仍可能造成分布偏离。

## 第 1 周：SFT：把数据变成行为

**目标：**完成一个可复现的 SFT 基线，并能解释每个被优化的 token。（6–8 小时）

### 从条件概率开始

给定提示 x 和目标回答 y，SFT 最大化回答的条件似然。它适合教会模型任务格式、风格和领域行为；数据中的错误答案也会被当作目标。先选一个可评估的小任务，例如结构化信息抽取，再准备覆盖常见与困难输入的正确示范，并另留失败案例用于评估。

### 先检查数据，再启动训练

统一 system / user / assistant 角色，使用模型自己的 chat template，并核对 EOS 与结束轮次标记。把一条样本打印为 token、label、attention mask 三列。prompt-completion、全序列语言建模、仅 assistant 计算损失是不同设定，不能仅凭数据叫“对话数据”推断 mask 正确。

### 建立基线与对照

先固定测试集、解码方式和最大输出长度，记录原始模型结果。用小样本验证训练循环能过拟合，再扩大数据。追踪 validation loss、任务指标、输出格式合法率、长度和失败案例；训练 loss 降低只是过程信号，不能代替任务验证。

### 核心表达

L_SFT = − Σₜ mₜ log πθ(yₜ | x, y<ₜ) / Σₜ mₜ

mₜ ∈ {0,1} 为参与损失的 token 掩码；分母必须大于 0。此处按有效 token 平均。

**常见误区：**Prompt 不算 loss，并不意味着它从上下文里消失。attention mask 与 loss mask 解决的是不同问题。

### 验收任务

- [ ] 打印并核查 10 条样本的模板、EOS、labels
- [ ] 完成小样本过拟合检查，并记录原始模型基线
- [ ] 保存固定测试集、配置和第一张 SFT 对比表

### 自测

把 prompt 的 labels 设为 −100，通常意味着什么？

1. 模型看不到 prompt
2. 这些位置不直接贡献交叉熵损失
3. 这些 token 被从输入中删除

答案：2。忽略的是这些位置的监督损失。prompt 仍能通过注意力影响回答预测，前提是 attention mask 允许访问。

配套阅读：TRL · SFT Trainer；a smol course；RLHF Book；Training language models to follow instructions with human feedback。原始链接统一列于文末。

## 第 2 周：高效微调与数据工程

**目标：**知道显存花在哪里，能够区分数据改进与训练配置带来的收益。（6–8 小时）

### LoRA 是参数化方式

LoRA 用低秩更新 ΔW = BA 适配冻结权重，改变的是可训练参数与优化器状态，而不是学习目标。SFT、DPO 或 RL 都可以使用 LoRA。rank 越大不保证效果越好，目标模块、学习率、数据量和训练步数同样重要。

### QLoRA 的节省与边界

QLoRA 将冻结基础模型量化，并训练低秩适配器。量化权重不等于整个训练只用 4 bit：激活、梯度、优化器状态以及计算精度另有成本。长上下文、batch size 和 rollout 数量可能主导显存。先跑小 batch 实测，再决定算力。

### 数据分割决定可信度

按来源、问题族或文档切分，而不只是随机切行；近似重复、同题改写和教师模型生成的测试答案可能泄漏。保存数据许可证、来源、清洗规则、随机种子、模型 revision 与依赖锁定文件。固定预算比较一项变化，避免多个因素一起改。

### 核心表达

W′ = W + (α/r) BA,  B ∈ ℝᵈˣʳ, A ∈ ℝʳˣᵏ

r 为低秩维度，α/r 是常见缩放约定；不同实现可能采用其他缩放。

**常见误区：**“消费级 GPU 可训练”不是硬件保证。模型、序列长度、量化支持、batch 和实现版本都会改变可行性。

### 验收任务

- [ ] 创建按问题族隔离的 train / validation / test 清单
- [ ] 实测一组 LoRA 配置的峰值显存和吞吐
- [ ] 只改变 rank 或数据质量，完成一次受控消融

### 自测

哪项最准确描述 LoRA？

1. 一种新的偏好学习损失
2. 只训练低秩更新的参数高效适配方式
3. 让所有训练张量都变成 4 bit

答案：2。LoRA 决定如何表示权重更新；SFT、DPO 等决定如何计算训练目标。QLoRA 还结合了冻结基础权重的量化。

配套阅读：LoRA: Low-Rank Adaptation of Large Language Models；QLoRA: Efficient Finetuning of Quantized LLMs；PEFT · LoRA guide；a smol course。原始链接统一列于文末。

## 第 3 周：偏好数据与奖励模型

**目标：**把“哪个回答更好”变成可审计的标签，而不是不透明的分数。（6–8 小时）

### 先定义“更好”

为正确性、指令遵循、信息完整度与简洁性写出可操作 rubric。成对比较必须使用同一 prompt，并明确平局和无法判断的处理。混合多个维度时保留分项标签，检查是否仅凭回答长度、措辞或格式就能预测 chosen。

### 奖励模型学的是代理指标

Bradley–Terry 模型把两个回答的奖励分差映射成偏好概率。奖励的绝对值通常没有直接含义；对于同一提示，加一个共同常数不改变偏好概率。验证应按提示分组划分，检查分领域准确率、标注一致性与长度偏差。

### 人工反馈与可验证反馈

开放式写作的质量可能需要人工或模型判断；算术答案、单元测试则可以构造程序反馈。LLM judge 也会有位置偏差、自偏好与提示敏感性。交换候选顺序、盲评并抽样人工复核，再把它作为辅助指标。

### 核心表达

P(yw ≻ yl | x) = σ(rφ(x,yw) − rφ(x,yl))

σ 是 sigmoid；yw / yl 为更好 / 更差回答。奖励模型常最小化该概率的负对数。

**常见误区：**奖励模型在训练分布上能排序，不代表策略优化后仍可靠。模型可能发现评分漏洞。

### 验收任务

- [ ] 手工复核 50 对偏好并写出标签规则
- [ ] 统计 chosen / rejected 长度与来源分布
- [ ] 写出 5 个能骗过当前奖励规则的反例

### 自测

同一 prompt 下，给所有回答奖励都加 10，Bradley–Terry 偏好概率会怎样？

1. 全部变大
2. 不变
3. 全部变成 1

答案：2。偏好概率只依赖奖励差；共同常数相减后消失。绝对奖励值不能脱离模型和任务解释。

配套阅读：RLHF Book；Training language models to follow instructions with human feedback；Tülu 3: Pushing Frontiers in Open Language Model Post-Training；Scaling Laws for Reward Model Overoptimization。原始链接统一列于文末。

## 第 4 周：DPO：从偏好直接更新策略

**目标：**手写 DPO loss，完成 SFT 与 SFT→DPO 的公平比较。（6–8 小时）

### 参考模型定义相对变化

对同一 prompt 的 chosen / rejected，分别计算策略与冻结参考模型的序列 log probability。DPO 优化两者 log-ratio 的差距。序列概率通常是回答 token 对数概率之和；不要未经说明改成平均值，那会改变目标及长度效应。

### 为什么不显式训练奖励模型

DPO 将 KL 正则奖励优化问题与偏好模型联系起来，得到直接作用于策略的二分类损失。经典离线 DPO 使用已有偏好对，训练循环不需要在线生成；偏好数据本身仍可能来自采样和标注。这与在线 RL 的数据分布不同。

### 正确理解 β

推导中 β 是相对参考策略的正则系数。对固定 log-ratio margin，DPO 损失中的 β 又会改变 sigmoid 斜率与梯度尺度。改变训练 β 之后实际 KL 怎样变化，需要实验观察；不能把固定输入的函数图直接当成训练结果。

### 核心表达

L_DPO = −log σ(β[(log πθ(yw|x) − log πref(yw|x)) − (log πθ(yl|x) − log πref(yl|x))])

πref 冻结；β > 0；yw 与 yl 必须来自同一 prompt。公式展示经典 sigmoid DPO。

**常见误区：**偏好准确率上升可能同时伴随 chosen 概率下降。监控 chosen / rejected log-prob、相对 margin、KL 估计和外部任务指标。

### 验收任务

- [ ] 手写并核对 DPO loss：相对 margin 为 0 时等于 ln 2
- [ ] 固定数据和预算，只扫描 2–3 个 β 值
- [ ] 盲评 SFT 与 DPO 输出，并报告长度与正确率

### 自测

经典离线 DPO 训练循环的关键输入是什么？

1. 同一 prompt 的 chosen / rejected 对与参考策略
2. 每一步必须在线采样的新 rollout
3. 人工给每个 token 标一个价值函数

答案：1。经典 DPO 在固定偏好对上计算策略与参考模型的 log probability。在线偏好学习是另外的数据收集与训练设置。

配套阅读：Direct Preference Optimization；TRL · DPO Trainer；Post-Training Course。原始链接统一列于文末。

## 第 5 周：PPO：理解在线 RL 的骨架

**目标：**画出在线 RL 数据流，区分 old policy、reference 与 value model。（8–10 小时）

### 一轮训练如何流动

用采样策略生成回答，计算奖励，再估计 advantage，最后更新策略。在线数据会随着策略变化，生成吞吐、奖励延迟和策略滞后都成为训练因素。先用小环境理解 REINFORCE 和 baseline，再阅读语言模型工程实现。

### 三种模型角色不要混淆

old policy 是产生当前批次 rollout 的策略，用来构造重要性比率；reference 通常是固定的基线，用来限制漂移；value model 估计回报，用来减少方差。在一些实现中模型共享或移除部分组件，但概念角色仍不同。

### Clipping 是局部代理目标

PPO 在重要性比率超出区间时截断某些方向的收益，降低单次更新过大的激励。它并不硬性保证实际 KL 小于某个值。看 policy KL、clip fraction、entropy、value loss 与输出长度，结合真实任务指标判断。

### 核心表达

J_clip = E[min(ρₜ Aₜ, clip(ρₜ,1−ε,1+ε) Aₜ)]

ρₜ = πθ(aₜ|sₜ) / πold(aₜ|sₜ)；此处最大化 J。完整实现还可能有价值损失、熵项和参考 KL 项。

**常见误区：**把 πref 放到 PPO 的 importance ratio 分母里会混淆两个角色。old policy 与 reference 一般不是同一个概念。

### 验收任务

- [ ] 画出 rollout → reward → advantage → update 流程
- [ ] 手算正 / 负 advantage 下的 clipping 行为
- [ ] 阅读一份实现，标出 old、reference、value 的位置

### 自测

PPO importance ratio 的分母对应什么？

1. 任意冻结的初始预训练模型
2. 生成当前 rollout 的采样策略
3. 奖励模型

答案：2。它衡量当前策略与生成该样本的旧策略之间的概率变化。约束整体偏移的 reference KL 是另一部分。

配套阅读：Proximal Policy Optimization Algorithms；The N Implementation Details of RLHF with PPO；CS224R · Deep Reinforcement Learning；Post-Training Course。原始链接统一列于文末。

## 第 6 周：GRPO 与可验证奖励

**目标：**构造一个可验证的小任务，并能诊断没有学习信号的 rollout。（8–10 小时）

### 组内比较代替价值模型

对于同一个问题采样多个回答，用组内奖励的相对差异构造优势信号。经典 GRPO 不需要独立 critic，但仍需模型生成、奖励计算和策略更新；没有 critic 并不等于低算力。组大小与输出长度会明显影响成本。

### 正确性奖励是一个程序

算术任务需要可靠解析最终答案；代码任务需要隔离环境与有覆盖率的测试。格式正确不等于语义正确，测试通过也不等于所有输入正确。把解析失败、超长输出、超时和异常情况纳入奖励定义，并保留原始回答便于审计。

### 论文与实现逐项对照

原始 GRPO、后续变体在长度归一化、标准差缩放、KL 与裁剪上可能不同。当前 TRL 文档默认 loss_type=dapo、beta=0.0；复现前应锁定版本并显式记录这些选项。网页实验只展示一种组相对标准化，不复刻完整 Trainer。

### 核心表达

Âᵢ = (rᵢ − mean(r₁…rG)) / (std(r₁…rG) + δ)

此处用总体标准差，δ 为数值稳定项。具体代码可能采用不同 std 校正、缩放或不做标准化。

**常见误区：**组内全对或全错时，相对优势为 0，不代表模型已学会任务；只是该组没有相对奖励差异。其他损失项仍可能产生更新。

### 验收任务

- [ ] 为 reward function 写出正确、错误、解析失败的测试
- [ ] 统计各组全对 / 全错比例与生成长度
- [ ] 在小任务上比较固定预算下的 SFT 与 RLVR

### 自测

同一题四个回答奖励都是 1，中心化组相对优势是多少？

1. 全部是 1
2. 全部是 0
3. 第一个一定最大

答案：2。每个奖励减去组均值后都是 0。加稳定项只避免除零，不会凭空创造相对学习信号。

配套阅读：DeepSeekMath；DeepSeek-R1；TRL · GRPO Trainer；verl。原始链接统一列于文末。

## 第 7 周：评估：证明提升来自哪里

**目标：**把“loss 下降了”升级为能经得起复查的模型改进证据。（6–8 小时）

### 三条指标线同时看

训练线看 loss、KL、entropy、梯度与长度；能力线看固定留出任务的正确率、格式合法率、拒答与通用回归；成本线看 GPU 时间、训练 token、rollout token 和推理延迟。任何一条单独变好都不足以下结论。

### 保持比较条件一致

同一模型家族、数据切分、prompt、解码参数和输出预算下比较。pass@1 与 best-of-N 不是同一个指标；训练更久或推理采样更多都可能解释收益。记录多个种子或报告不确定性，避免给很小的测试集附上过强结论。

### 主动寻找反例

构造长度变化、答案顺序交换、格式诱导、分布外问题和奖励漏洞。训练奖励上升但外部正确率下降，是过优化的典型警报。挑选 checkpoint 只能使用 validation；最终 test 只在方案冻结之后使用。

### 核心表达

Δ任务指标 = metric(适配后模型) − metric(固定基线)

比较须匹配测试集与推理预算，并报告样本数、种子和不确定性。训练奖励不是独立测试集指标。

**常见误区：**反复查看 test 并据此调参，相当于逐渐把 test 变成训练流程的一部分。

### 验收任务

- [ ] 建立训练 / 能力 / 成本三线实验表
- [ ] 设计至少 10 个奖励漏洞或分布外测试
- [ ] 写一页消融结论，明确支持与不支持的推断

### 自测

哪种比较最能支持方法改进的结论？

1. 新模型 best-of-64 对旧模型 pass@1
2. 固定测试与推理预算，并报告成本和波动
3. 只展示新模型最好的 3 个回答

答案：2。要控制混杂因素。不同采样预算和挑选案例会夸大方法收益，无法直接归因于训练算法。

配套阅读：Tülu 3: Pushing Frontiers in Open Language Model Post-Training；Scaling Laws for Reward Model Overoptimization；Language Model Evaluation Harness；DeepSeek-R1。原始链接统一列于文末。

## 第 8 周：综合项目：交付一次后训练实验

**目标：**交付能复跑、能解释、能指出局限的完整实验，而不只是一份 checkpoint。（8–12 小时）

### 选一个有限目标

推荐从结构化抽取或小规模数学题开始。先交付原始模型与 SFT 基线；如果偏好可可靠标注，走 DPO；如果答案可程序验证，走 RLVR。两条分支都理解，但不必在有限算力下强行把所有算法串在同一条流水线。

### 先有证据，再谈扩展

完成最小闭环后再选择分布式框架。TRL 适合学习和快速试验；verl、OpenRLHF 帮助研究更大规模 rollout / training 系统。阅读 Tülu 3 的配方，理解数据、阶段和评估如何组成系统。把蒸馏、合成数据和 agent RL 作为后续专题。

### 你的交付件

包含数据卡、训练配置、环境锁定、模型 revision、基线与消融表、reward tests、失败案例、硬件与成本记录、可复跑说明。负结果也有价值：例如数据质量改善胜过换算法，或训练收益在推理预算匹配后消失。

### 核心表达

可信结果 = 固定问题 + 可复跑流程 + 受控对比 + 失败分析

这是项目验收框架，不是数学等式；以证据质量而非模型尺寸评估学习成果。

**常见误区：**发布模型或数据前核对原始许可证、衍生使用条件与数据敏感性。网页学习不要求上传任何训练数据。

### 验收任务

- [ ] 完成 SFT + 一条偏好或 RL 分支的受控实验
- [ ] 整理配置、指标、失败案例和复跑命令
- [ ] 向同伴解释一次负结果及下一步实验设计

### 自测

什么时候更适合优先尝试 RLVR？

1. 有相对可靠、可执行的答案验证规则
2. 只有模糊的“看起来更好”偏好
3. 任何任务都应先做 RLVR

答案：1。RLVR 依赖可验证奖励。开放式质量偏好可以先考虑 SFT、偏好数据和 DPO，但仍需独立评估。

配套阅读：CS336 · Language Modeling from Scratch；Tülu 3: Pushing Frontiers in Open Language Model Post-Training；verl；OpenRLHF；a smol course。原始链接统一列于文末。

## 可复跑实验交付模板

1. 任务定义、模型与 tokenizer revision。
2. 数据来源、许可证、按问题族划分的 split、去重方法。
3. 环境锁定、训练配置、种子、硬件、峰值显存、训练与 rollout token 数。
4. 同测试集、同解码预算下的 base / SFT / DPO 或 RLVR 对照。
5. 消融与失败分析；报告样本数、波动和未能支持的推断。

## 版本边界

TRL 是滚动更新的实现。核验时 GRPO 默认 loss_type=dapo、beta=0.0，不等于原始 GRPO 配方。smol-course 单元开放程度不同，RL 实操以 TRL 和 LLM Course 第 12 章补足。CS336 当前主站为 Spring 2026，作业仓库主分支会更新。所有运行配置应锁定依赖与代码版本。

## 参考资料

以下为一手原始链接，访问核验日期均为 2026-11-09；本导读不复制第三方完整教材。

### RLHF Book

Nathan Lambert · 教材 · 主线

作为整条路线的主教材：把后训练目标、数据、算法与评估放进统一框架。

先读：按主题读 IFT、奖励建模、RL、DPO、推理和评估章节；不必从历史章节顺序通读。

边界：英文在线版免费；纸书付费。网页持续修订，应优先对照在线勘误。

[原始来源](https://rlhfbook.com/)

### Post-Training Course

Nathan Lambert · 课程 · 主线

主教材的配套讲解，适合已经懂深度学习、需要打通 RL 数学与工程的人。

先读：Lectures 2–6 对应 IFT、奖励模型、RL、推理与 DPO；7–10 扩展数据与过优化。

边界：免费英文视频与讲义。用于理解推导，仍需配合代码实验。

[原始来源](https://rlhfbook.com/course)

### a smol course

Hugging Face · 实操 · 主线

以小模型组织后训练实践，适合作为每周实验的主入口。

先读：选择 SFT、偏好对齐与评估单元；RL 实验改用 TRL GRPO 文档和 LLM Course 第 12 章。

边界：材料免费；真实训练需要算力，云端运行可能收费。

[原始来源](https://huggingface.co/learn/smol-course/en/unit0/1)

### TRL · SFT Trainer

Hugging Face · 文档 · 必查

核对数据格式、模板、loss masking 与 SFT 配置的首选实现文档。

先读：Expected dataset format、loss 配置、PEFT integration。

边界：滚动版本文档；先固定安装版本，再切到对应文档。

[原始来源](https://huggingface.co/docs/trl/sft_trainer)

### TRL · DPO Trainer

Hugging Face · 文档 · 必查

将论文目标落到偏好数据字段、参考模型和训练指标。

先读：数据格式、beta、loss_type 与记录指标。

边界：包含多种 loss 变体，不应全部称为经典 DPO。

[原始来源](https://huggingface.co/docs/trl/dpo_trainer)

### TRL · GRPO Trainer

Hugging Face · 文档 · 必查

理解生成、reward function、优势缩放和不同损失归一化的实现。

先读：查看 loss_type、beta、scale_rewards、num_generations。

边界：核验时默认 dapo loss、beta=0.0；与原论文 GRPO 有差异。

[原始来源](https://huggingface.co/docs/trl/grpo_trainer)

### CS336 · Language Modeling from Scratch

Stanford · 2026 · 课程 · 进阶

用从头实现的方式理解语言模型系统，后训练部分可选修。

先读：重点看 2026 的 L15–16 和 alignment 作业；其余按知识缺口补。

边界：不是纯后训练课；完整作业耗时和算力明显高于本路线。

[原始来源](https://cs336.stanford.edu/)

### CS224R · Deep Reinforcement Learning

Stanford · 课程 · 进阶

补齐 policy gradient、actor–critic 与 RL 的通用理论。

先读：优先看策略梯度与 LLM reinforcement learning 相关讲次。

边界：涉及机器人等其他场景；已有 RL 基础者可跳读。

[原始来源](https://cs224r.stanford.edu/)

### 机器学习 2025 · 后训练专题

李宏毅 · 台湾大学 · 课程 · 中文辅助

用中文串起 alignment、post-training、forgetting 与 reasoning。

先读：3/28 Pretrain/Alignment；4/18 Post-training/Forgetting；4/25 Reasoning。

边界：部分材料英文；适合概念复习，不替代实现文档。

[原始来源](https://speech.ee.ntu.edu.tw/~hylee/ml/2025-spring.php)

### LLM Course · Chapters 11–12

Hugging Face · 课程 · 补基础

用较缓的节奏补 fine-tuning，随后进入 reasoning models。

先读：先快速诊断 Chapter 11 的知识缺口，再看 Chapter 12。

边界：你已有深度学习基础，可以跳过熟悉内容。

[原始来源](https://huggingface.co/learn/llm-course/en/chapter11/1)

### Training language models to follow instructions with human feedback

Ouyang et al. · 2022 · 论文 · 经典

理解 SFT → reward model → PPO 这条经典 RLHF 配方。

先读：训练流程、数据构造、评估方法与局限。

边界：历史配方，不代表今天所有模型都采用同一流水线。

[原始来源](https://arxiv.org/abs/2203.02155)

### Direct Preference Optimization

Rafailov et al. · 2023 · 论文 · 必读

从 KL 正则奖励目标推导到直接偏好损失。

先读：Section 4 推导；写出 reference log-ratio，再看附录。

边界：理论关系有假设；不意味着固定离线偏好覆盖所有在线状态。

[原始来源](https://arxiv.org/abs/2305.18290)

### Proximal Policy Optimization Algorithms

Schulman et al. · 2017 · 论文 · 经典

理解 clipping surrogate 的原始定义，避免只背训练框架术语。

先读：先手算正负 advantage 下的 clipped objective。

边界：原文非 LLM 专用，需配合后训练实现解读。

[原始来源](https://arxiv.org/abs/1707.06347)

### LoRA: Low-Rank Adaptation of Large Language Models

Hu et al. · 2021 · 论文 · 经典

理解低秩更新为何能减少可训练参数与优化器负担。

先读：参数化公式、目标矩阵、rank 实验。

边界：不承诺所有任务与全参训练相同效果。

[原始来源](https://arxiv.org/abs/2106.09685)

### QLoRA: Efficient Finetuning of Quantized LLMs

Dettmers et al. · 2023 · 论文 · 进阶

理解冻结权重量化与低秩训练结合的机制。

先读：NF4、double quantization、paged optimizers 的动机。

边界：论文硬件结果不应直接外推到任意模型、长度或设备。

[原始来源](https://arxiv.org/abs/2305.14314)

### PEFT · LoRA guide

Hugging Face · 文档 · 必查

核对 LoRA 目标模块、缩放与量化适配实践。

先读：结合你的模型结构查 target_modules 与 quantized model 相关说明。

边界：具体配置随模型架构与库版本变化。

[原始来源](https://huggingface.co/docs/peft/developer_guides/lora)

### DeepSeekMath

DeepSeek-AI · 2024 · 论文 · 必读

GRPO 的原始来源，用于理解组相对优势与 critic 的取舍。

先读：GRPO 方法章节和训练配置，对照现有库的差异。

边界：完整数学模型训练流程远大于一个 GRPO loss。

[原始来源](https://arxiv.org/abs/2402.03300)

### DeepSeek-R1

DeepSeek-AI · 2025 · 论文 · 必读

区分 R1-Zero 与完整 R1 的多阶段训练，以及蒸馏。

先读：奖励信号、冷启动数据、训练阶段和局限。

边界：不应把 R1 概括成完全不使用 SFT，也不代表个人算力可复现。

[原始来源](https://arxiv.org/abs/2501.12948)

### The N Implementation Details of RLHF with PPO

Hugging Face / CleanRL 作者 · 实操 · 进阶

展示实现细节怎样影响复现：归一化、采样、奖励与优化。

先读：挑 3 项细节追到代码，解释为何会影响结果。

边界：针对特定历史复现设置；代码接口需按版本适配。

[原始来源](https://huggingface.co/blog/the_n_implementation_details_of_rlhf_with_ppo)

### Tülu 3: Pushing Frontiers in Open Language Model Post-Training

Allen Institute for AI · 2024 · 论文 · 综合

观察数据、SFT、偏好优化与 RLVR 如何组成开放配方。

先读：各阶段职责、数据配方、消融与评估，而非只看排行榜。

边界：大规模配方不等于学习者最低复现成本。

[原始来源](https://arxiv.org/abs/2411.15124)

### verl

verl project · 框架 · 进阶

深入分布式后训练与 rollout / training 系统的工程入口。

先读：先读 quickstart 与单个 PPO / GRPO 示例，再看架构。

边界：版本和硬件耦合较强；先在小模型上把算法闭环跑通。

[原始来源](https://github.com/verl-project/verl)

### OpenRLHF

OpenRLHF community · 框架 · 进阶

比较基于 Ray 等组件的 RLHF 系统组织方式。

先读：研究 rollout、actor、reward、critic 的资源布局。

边界：适合系统进阶；不建议作为首次理解损失函数的入口。

[原始来源](https://github.com/OpenRLHF/OpenRLHF)

### Language Model Evaluation Harness

EleutherAI · 框架 · 必查

标准化部分任务评估，记录任务配置与模型适配方式。

先读：选择与你项目目标相符的任务并固定版本、shot 与解码配置。

边界：通用 benchmark 不能替代领域留出集与人工失败分析。

[原始来源](https://github.com/EleutherAI/lm-evaluation-harness)

### Scaling Laws for Reward Model Overoptimization

Gao, Schulman & Hilton · 2022 · 论文 · 进阶

理解代理奖励提升为什么可能伴随真实目标退化。

先读：对比 proxy reward 与 gold reward 曲线，思考你的独立验证。

边界：研究设置中的规律不能当作任意任务的通用定量定律。

[原始来源](https://arxiv.org/abs/2210.10760)
