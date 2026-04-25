# AI 训练 vs 推理硬件市场分化研究

**ai-berkshire 训练vs推理专员 | 2026-04-24**

---

## 1. 核心判断

未来 3-5 年 AI 加速器市场最大的结构性变化是**重心从训练转向推理**：2026 年推理工作负载已占 AI 算力的约 2/3，推理市场规模首次超越训练（约 1,180 亿美元 vs 训练侧约 700-800 亿美元），到 2030 年推理 TAM 可能达训练的 3-10 倍。NVIDIA 在训练侧仍保持 90%+ 份额，但**推理侧份额已从 2024 年 90% 降至 2026 年约 65-75%**，未来三年将被三股力量持续侵蚀：(a) 超大客户自研 ASIC（TPU/Trainium/Maia/MTIA/Titan），(b) AMD MI350/MI400 在 token-per-dollar 上的领先，(c) Groq/Cerebras 等专用推理架构。中性情景下 NVIDIA 2030 年推理份额约 45-55%，但因总盘子翻 2-3 倍，绝对收入仍增长，**只是毛利率从 75% 区间被压向 60% 区间**。

---

## 2. 训练 vs 推理市场规模（2025-2030）

| 年份 | AI 加速器总市场（B$） | 训练（B$） | 推理（B$） | 推理/训练比 | 推理占比 |
|------|---------------------|-----------|-----------|-----------|---------|
| 2025 | ~210 | ~104 | ~106 | 1.0× | 50% |
| 2026 | ~250-280 | ~110-130 | ~118-150 | 1.1-1.3× | ~55-65%（算力口径 2/3）|
| 2027 | ~350-400 | ~130-150 | ~200-250 | 1.5-1.7× | ~60-65% |
| 2030 | ~600-1,000 | ~150-200 | ~255-500 | 1.7-3× （部分预测 10×）| ~65-80% |

**关键数据点**：
- 2025 推理市场 106 B$ → 2030 255 B$（CAGR 19.2%，MarketsandMarkets）
- Bloomberg Intelligence：AI 加速器 2024 116B → 2033 600B+
- 2026 是**推理云开支首次超过训练**的拐点（55% vs 45%，约 20.6B vs 16.8B 在云基础设施口径）
- 推理算力占比：2023 年 1/3 → 2025 年 1/2 → 2026 年 2/3 → 2029 年 65%+
- 推理芯片专用品类 2026 年单独可达 50B 美元

---

## 3. 推理硬件的特殊要求

### 训练硬件需求
- **超大显存 + HBM 带宽**：B200 192GB HBM3E、Rubin Ultra 365TB/rack
- **超高互联**：NVLink 5 1.8TB/s、NVL72/NVL576 大规模 scale-up
- **FP16/FP8/BF16 稳定计算**：长 step 不能数值崩
- **集群通信**：NCCL、InfiniBand 800G、扁平拓扑
- **可靠性**：训练一次跑 30-90 天，硬件故障率必须极低
- **客户类型集中**：全球 30 家 frontier lab + 20 家主权 AI

### 推理硬件需求
- **低延迟**：交互式 < 100ms TTFT
- **高吞吐**：tokens/sec/$、tokens/sec/W 才是 KPI
- **多精度**：INT8/INT4/FP4/FP8（B200 FP4 是关键卖点）
- **成本敏感**：客户算单 token 成本（B200: $0.02/M tokens vs H100: $0.09/M）
- **部署多样**：单卡到 8 卡、可以小集群、可以 edge
- **服务器密度**：每机架 token 产能 / 每瓦 token 数
- **客户极度分散**：全球数千家 AI 应用、SaaS、企业内部

**关键差异**：训练买"性能极致+可靠性"，推理买"性价比+延迟"。这意味着推理市场天然更分散、更价格敏感、**更容易被 ASIC 和挑战者撕开**。

---

## 4. 推理硬件竞争格局（2026）

### A. NVIDIA（GPU，市场领导）
- H100/H200：仍是 2026 全球推理主力（H200 141GB HBM3E 特别适合长上下文推理）
- B200/GB200 NVL72：FP4 性能 2× H100，单机架 1.4 ExaFLOPS FP4，inference cost 比 H100 低 4-6×
- TensorRT-LLM + Dynamo：软件栈是护城河
- **2026 推理份额估算：65-75%**（含云端外销 + 主权 AI）
- Rubin（2026 H2）/Rubin Ultra（2027 H2）：NVL576 推理 15 EF FP4，14× GB300

### B. AMD（GPU，性价比挑战者）
- MI300X（192GB HBM3）：Microsoft Azure / Meta / Oracle 大客户
- MI325X（256GB HBM3E）：2025
- MI350/MI355X（2026 H2，288GB HBM3E）：宣称 Llama 3.1 405B 推理快 B200 30%、tokens-per-dollar 高 40%
- MI400（2026 末/2027，432GB HBM4，19.6TB/s）：定位"为 inference 而生"
- **2026 整体 AI GPU 份额**：12-15%（推理侧约 15%）
- 软肋：ROCm 生态仍弱，长尾客户难触达

### C. Google TPU（ASIC，自用为主）
- TPU v5e（推理优化）/ v6e Trillium（2024）/ v7 Ironwood（2025）
- Gemini 75%+ 推理在 TPU 上跑
- 对外有限：Anthropic 是最大外部客户

### D. AWS Inferentia / Trainium
- Trainium 3（2026）+ Neuron SDK 持续成熟
- Anthropic 的 Project Rainier：数十万 Trainium 2 集群
- 2026 Amazon 内部 AI 工作负载约 30% 用自研芯片

### E. Microsoft Maia
- Maia 100（2024）/ Maia 200（2026）
- 主要承载 Azure OpenAI Service / Copilot 推理
- 2026 仍占 Microsoft AI 工作负载的少数（< 30%），但增速最快

### F. Meta MTIA
- MTIA v2（2025）已规模化部署在推荐系统 + Llama 推理
- 2026 三个代际并行

### G. Groq LPU（推理专用 ASIC）
- 500MB on-chip SRAM，150 TB/s 带宽（45× H100）
- Llama 2 70B 300 tokens/sec，10× H100
- 能效 35× H100（150 tokens/W vs 4.3 tokens/W）
- **2025 年 12 月被 NVIDIA 以 200 亿美元收购**

### H. Cerebras WSE-3
- 整片晶圆 44GB SRAM（880× H100），Llama 3.1 405B > 1000 tokens/sec
- **2026 年 4 月 OpenAI 下了 200 亿美元订单，Cerebras 已申报 IPO（350 亿估值）**

### I. 华为 Ascend
- 910C 推理性能约 H100 的 60%，2026 目标产能 60 万颗
- 920（2026 上市）：填补 H20 退出后的空白
- 950PR：1.56 PFLOP，对标更高端
- **中国市场份额：本土厂商合计 41%**（Bernstein/IDC，2026 Q1）

### J. Cambricon
- 2026 目标 50 万颗 Siyuan 系列（首次年度盈利）
- 限制：SMIC 7nm 良率 ~20%、HBM 受韩国厂商限制

---

## 5. ASIC vs GPU 在推理场景的优劣

### ASIC 优势
- 性能/瓦特比 GPU 高 2-5×
- 单位 token 成本低 30-50%
- 针对 transformer 推理 dataflow 优化
- 可与超大客户工作负载深度耦合

### ASIC 劣势
- 灵活性差：模型架构变化（如 MoE、状态空间模型）需要重新设计
- 设计周期 18-24 个月：跟不上模型迭代
- 软件生态弱：编译器、kernel 库需要自建
- 量产成本高：单颗 NRE 数亿美元
- 只适合超大客户

### GPU 优势
- 通用性：训练、推理、HPC、图形通吃
- CUDA 生态成熟 18 年
- 跟得上模型创新：Mamba、Diffusion、MoE 都能跑
- 租赁市场流动性强

### GPU 劣势
- 性价比相对差（vs 优化好的 ASIC）
- 利用率低（推理负载波动）
- HBM 成本高

**判断**：超大客户会持续 ASIC 化，**长尾市场 GPU 仍是默认选择**。

---

## 6. 大客户自研芯片冲击

| 客户 | 自研芯片 | 2026 自家工作负载占比 | 对 NVIDIA 影响 |
|------|---------|---------------------|----------------|
| Google | TPU v7 Ironwood | 75-80%（Gemini）| 推理上几乎不买 |
| Microsoft | Maia 200 | 20-30%（推理）| 仍是 NVIDIA 头号客户 |
| AWS | Trainium 3 / Inferentia | 30-35%（推理）| Anthropic 部分迁移 |
| Meta | MTIA v2/v3 | 30-40%（推理 + 推荐）| 仍买大量 GB200 训练 Llama |
| OpenAI | Titan（Broadcom）| 0%（2026）→ 重要（2027 H2）| 长期最大威胁 |
| Anthropic | 无（用 TPU + Trainium）| 60%+ 在 ASIC | 几乎不买 NVIDIA |
| 字节 | 自研 + 华为 Ascend | ~50% 国产（中国）| 中国市场失去 |
| 阿里/腾讯 | 含光 + Ascend + Cambricon | 40-60% 国产 | 中国市场失去 |

**关键观察**：
- Top 5 美国 hyperscaler 占全球 AI capex 60%+
- OpenAI Titan（2027 量产）是 NVIDIA 单一最大长期威胁
- NVIDIA 反制：收购 Groq、Spectrum-X 网络、NVL72/NVL576 scale-up、主权 AI 客户多样化

---

## 7. 推理利润率 vs 训练利润率

### NVIDIA 训练芯片
- 毛利率 75%+
- ASP：H100 $30-40k，B200 $30-50k，GB200 NVL72 整柜约 300 万美元
- 客户极度愿付溢价

### NVIDIA 推理芯片
- 毛利率估算 60-70%
- 客户高度价格敏感
- AMD MI355X 直接压价
- ASIC 拉低市场参考价

### 三年趋势
- NVIDIA 整体数据中心毛利率可能从 **75% → 65-68%**（2028）
- **绝对收入翻倍**（2026 ~190B → 2028 ~350B 数据中心）
- NVIDIA 应对：靠系统化销售（NVL72/NVL576/Spectrum-X 全栈）维持溢价；卖 racks 而非卖 chips

---

## 8. 三情景预测（2030）

### 乐观（NVIDIA 推理份额 55-60%）
- CUDA + TensorRT-LLM + Dynamo 生态壁垒持续
- AMD ROCm 停在 12-15%
- NVIDIA 数据中心 2030 收入 500B+，毛利 70%+

### 中性（NVIDIA 推理份额 40-50%）
- AMD MI400/MI500 抢下 20-25% 推理市场
- Top 5 hyperscaler 自研覆盖 50-60% 内部推理
- 中国市场基本失去
- NVIDIA 数据中心 2030 收入 350-400B，毛利 65%

### 悲观（NVIDIA 推理份额 25-35%）
- 大客户自研全部成功，OpenAI 离开 NVIDIA
- AMD MI500 性能反超
- ASIC 商品化
- NVIDIA 数据中心 2030 收入 250-300B，毛利 55-60%

**ai-berkshire 主基线判断**：中性偏乐观。NVIDIA 在训练侧未来 5 年仍是接近垄断；推理侧虽被侵蚀但绝对盘子翻 3 倍。**真正风险是毛利率结构性下移 10-15 个百分点。**

---

## 9. 关键投资含义

1. **NVIDIA 不是"训练芯片股"，是"AI 系统化基础设施股"**：买的是 NVL576 + Spectrum-X + CUDA + Dynamo + Groq 的全栈定价权
2. **推理市场分化是不可逆的**：未来 5 年 NVIDIA 推理份额必然下降，但总盘子 × 份额 = 绝对收入仍在涨
3. **AMD 是真正二号选手**：MI400 是关键产品，2027 财报是验证窗口
4. **Broadcom 是"卖铲人的卖铲人"**：所有大客户 ASIC 都靠 Broadcom 设计
5. **中国 AI 芯片是平行宇宙**：华为 + Cambricon 在国内市场已与 NVIDIA 平分秋色
6. **OpenAI 走向 Broadcom 是 NVIDIA 长期叙事的最大裂痕**：2027-2028 是观察点
7. **推理利润下移 = NVIDIA PE 应该收缩**：从训练时代的 35-40× → 推理时代的 25-30×

---

*ai-berkshire 训练vs推理专员 | 报告完*
