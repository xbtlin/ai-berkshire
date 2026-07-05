---
name: investment-team
description: "AI Berkshire skill: 投研团队：四角色并行分析框架. Source: skills/investment-team.md."
---

## Codex adapter note

This skill is generated from `skills/investment-team.md` so Claude Code and Codex users share one canonical workflow.

- Treat `$ARGUMENTS` as the user's request in the current Codex thread.
- When the source mentions Claude-only surfaces such as Task, Agent, WebSearch, Bash, Read, or Write, use the closest Codex capability available in this session: subagents when available, web search when needed, shell commands for local tools, and normal file edits for workspace files.
- Use shared project tools from `tools/` in this repository. Commands that reference `~/ai-berkshire/tools/...` assume the repo is checked out at `~/ai-berkshire`; if needed, prefer the current workspace path.
- Preserve the research quality rules from `AGENTS.md`: cross-check financial data, use exact arithmetic tools for valuation/math, and clearly label uncertainty and source gaps.

# 投研团队：四角色并行分析框架

对 $ARGUMENTS 进行团队化投资研究分析。使用 Team 工具创建真正的多Agent并行研究团队。

## 执行流程

### 第一步：展示团队框架

向用户展示以下团队结构，确认后启动：

| 角色 | 职责 | 分析框架 |
|------|------|----------|
| **team-lead**（你自己） | 统筹协调、汇总研判、输出最终报告 | 四大师综合框架 |
| **business-analyst** | 商业模式 & 护城河分析 | 段永平视角 |
| **financial-analyst** | 财务报表 & 估值分析 | 巴菲特视角 |
| **industry-researcher** | 行业格局 & 竞争态势 | 芒格视角 |
| **risk-assessor** | 风险评估 & 管理层研判 | 李录视角 |

### 第一步半：AI研究偏见评估

在创建团队前，先向用户展示该公司的"AI可研究性"评估：

**信息丰富度评级**（决定研究策略）：
| 等级 | 特征 | 研究策略调整 |
|------|------|------------|
| A级（信息充裕） | 上市多年、券商覆盖广 | 团队重点放在**反面检验**和**非共识视角**，避免输出与市场一致的"正确的废话" |
| B级（信息适中） | 上市不久、覆盖有限 | 每个Agent的推算数据必须标注置信度，team-lead汇总时标注"数据充分度" |
| C级（信息稀缺） | 冷门/新上市/新兴市场 | 团队转为"第一性原理模式"：不追求报告完整性，聚焦商业本质的几个核心问题 |

**关键提醒**：资料多≠确定性高，资料少≠确定性低。AI能输出的置信度 ≠ 投资的真实确定性。确定性来自商业模式本身，不来自资料数量。

将评级结果告知每个Agent，影响其研究方式。

### 第二步：创建团队

使用 TeamCreate 创建团队：
- team_name: `{公司名}-research`（英文小写，如 `meituan-research`）
- agent_type: `team-lead`

### 第三步：创建4个任务

使用 TaskCreate 创建以下4个任务（每个都要有 subject、description、activeForm）：

#### 任务1：商业模式分析
- subject: `分析{公司名}商业模式、护城河与用户价值`
- description 包含：
  1. 商业模式本质：核心生意定义、收入结构拆解
  2. 平台/产品飞轮效应如何运转
  3. 护城河分析：品牌/转换成本/网络效应/规模效应/技术壁垒，逐一验证
  4. 用户/客户价值：为各方创造了什么独特价值
  5. 业务矩阵与协同效应
  6. 段永平"好生意"标准评估：差异化、定价权、可持续竞争优势
  7. 要求搜索最新财报、行业报告等公开信息

#### 任务2：财务与估值分析
- subject: `分析{公司名}财务数据、盈利能力与估值`
- description 包含：
  1. 近3-5年营收、净利润、经营利润趋势
  2. 盈利能力指标：ROE、ROA、毛利率、经营利润率
  3. 现金流分析：经营性现金流、自由现金流、资本开支
  4. 资产负债表健康度：现金储备、负债率、流动性
  5. 估值分析：PE/PS/PB/EV等，与历史及同业对比
  6. 安全边际评估：内在价值 vs 当前股价
  7. **金融严谨性验证（必须使用Bash调用工具，禁止心算）**：
     - 市值验算：`python3 ~/ai-berkshire/tools/financial_rigor.py verify-market-cap --price {价格} --shares {股本} --reported {报告市值} --currency {币种}`
     - 估值验算：`python3 ~/ai-berkshire/tools/financial_rigor.py verify-valuation --price {价格} --eps {EPS} --bvps {每股净资产}`
     - 关键数据交叉验证：`python3 ~/ai-berkshire/tools/financial_rigor.py cross-validate --field {字段} --values '{JSON}' --unit {单位}`
     - 三情景估值：`python3 ~/ai-berkshire/tools/financial_rigor.py three-scenario --price {价格} --eps {EPS} --shares {股本亿} --growth {乐观} {中性} {悲观} --pe {乐观PE} {中性PE} {悲观PE}`
     - 将工具输出结果直接嵌入报告中作为验证记录

#### 任务3：行业与竞争分析
- subject: `分析{行业}行业格局与{公司名}竞争态势`
- description 包含：
  1. 行业规模与增长：市场规模、增速、渗透率
  2. 竞争格局：主要对手市场份额、竞争策略对比
  3. 核心竞争者威胁评估：逐个分析主要竞争对手
  4. 各细分赛道格局
  5. 行业趋势：技术变革、政策影响、新进入者
  6. 产业链分析：上中下游价值分配
  7. 要求搜索最新行业数据和竞争动态

#### 任务4：风险与管理层评估
- subject: `评估{公司名}投资风险与管理层质量`
- description 包含：
  1. 管理层评估：CEO能力圈、诚信度、战略眼光、资本配置能力、历史决策质量
  2. 监管风险：当前及潜在监管影响
  3. 竞争风险：各竞争对手威胁程度评估
  4. 业务风险：新业务亏损、扩张不确定性
  5. 宏观风险：经济周期、行业周期影响
  6. 治理结构：股权结构、关联交易、股东回报政策
  7. 长期确定性：10年后公司会怎样？什么可能颠覆其商业模式？
  8. 要求搜索最新监管动态、管理层言论等

### 第四步：启动4个并行Agent

使用 Task 工具同时启动4个Agent（**必须在同一条消息中并行调用**）：

每个Agent的配置：
- `subagent_type`: `general-purpose`
- `run_in_background`: `true`
- `team_name`: 对应团队名
- `name`: 对应角色名（business-analyst / financial-analyst / industry-researcher / risk-assessor）

每个Agent的prompt模板：

```
你是{公司名}投研团队中的"{角色中文名}"，负责从{大师名}投资视角分析{公司名}。

请完成任务 #{任务编号}：{任务subject}

具体要求：
{任务description的内容}

**研究方法**：
- 使用 tavily_search 搜索最新公开信息（财报、行业报告、新闻）
- **财务数据必须来自两个独立来源**，按 `skills/financial-data.md` 规范执行（美股：macrotrends+stockanalysis；港股：aastocks+macrotrends；A股：东方财富+巨潮资讯），两源误差>1%须标记
- 确保数据准确，关键数据标注来源
- 分析要深入，不流于表面

**输出要求**：
- 报告要详尽，使用Markdown表格呈现关键数据
- 每个分析维度要有明确结论和评分
- 报告末尾要有该维度的总体结论

**完成后**：
1. 使用 TaskUpdate 将任务 #{任务编号} 标记为 completed
2. 通过 SendMessage 把完整分析报告发送给 team-lead（type: "message", recipient: "team-lead"）
```

### 第五步：接收报告并跟踪进度

- 向用户实时展示进度表（哪些Agent已完成、哪些仍在研究中）
- 每收到一份报告，更新进度并展示该报告的核心要点（3-5条）
- 等待全部4份报告到齐

### 第六步：关闭团队成员

全部报告收到后，向4个Agent发送 shutdown_request（使用 SendMessage，type: "shutdown_request"）。

### 第七步：汇总最终报告

综合4份分析报告，输出以下结构的最终报告：

---

#### 1. 一句话结论
> 用一段话（50-100字）概括是否值得投资及核心逻辑

#### 2. 四维评分总表
| 维度 | 框架 | 评分(1-5星) | 核心判断 |
|------|------|------------|----------|

综合评分：X / 5

#### 3. 核心数据速览
关键财务和经营指标表格（近2年对比）

#### 4. 各维度分析摘要
每个维度摘取3-5条最重要的发现

#### 5. 投资论点（Bull vs Bear）
- 🟢 看多逻辑（5-7条）
- 🔴 看空逻辑（5-7条）

#### 6. 巴菲特买入前Checklist
| # | 检查项 | 通过? | 说明 |
10个核心检查项，逐一评估

#### 7. 最终投资建议
- 定性判断表（生意质量/管理层/估值/时机）
- 分层操作建议表（激进型/稳健型/保守型 → 建议+价格区间）
- 关键催化剂（加仓信号/减仓信号各3-5条）

#### 8. 总结段落
100-200字的最终总结

---

### 第八步：保存报告

将完整最终报告写入 `~/{公司名}投资研究报告_{日期}.md`（日期格式 YYYYMMDD）。

### 第九步：数据抽检（准出流程）

```bash
# Step 1 — 提取抽检清单（15%随机抽样）
python3 ~/ai-berkshire/tools/report_audit.py extract \
  --report <报告文件路径>

# Step 2 — 对清单每项从可靠信源取数（参见 skills/financial-data.md）

# Step 3 — 输出准出/打回判决
python3 ~/ai-berkshire/tools/report_audit.py verdict \
  --results '<填好的JSON>' \
  --report <报告文件名>
```

**【准出】** 全部通过 → 报告可发布；**【打回】** 有不通过 → 修正后重审。

### 第十步：清理团队

使用 TeamDelete 清理团队资源。

## 重要注意事项

1. **4个Agent必须并行启动**——在同一条消息中调用4次Task工具
2. **Agent通过SendMessage汇报**——不是文件协作，是消息通信
3. **数据准确性**——要求Agent使用tavily_search搜索最新数据，关键数据交叉验证
4. **结论要明确**——不回避给出买入/观望/回避建议和具体价格区间
5. **所有分析必须有数据支撑**——附数据来源
6. **耐心等待**——4个Agent研究需要几分钟，实时向用户更新进度
7. **反偏见意识**——team-lead在汇总时必须评估：各Agent的分析是否受限于资料充裕度？是否与市场共识过度趋同？最终报告需包含"信息丰富度评级"和"AI研究局限性声明"
8. **信息稀缺时的诚实原则**——宁可在报告中留白标注"数据不足"，也不要用推测填满框架伪装确定性

---

## 数据源 + 观点层：金融 AI（gangtise-reason）

金融 AI（gangtise-reason）是**高价值数据源**，提供专业研报数据（业务结构/财务细节/机构评级/目标价）。**当 fin_ai 有数据时，以 fin_ai 为准确源**——B 级以下公司经验证比 tavily_search/东方财富更准（小商品城样本：fin_ai ROE 17.53% vs tavily_search 12.96%/4.15%，反推验证 fin_ai 数据自洽）。

### 调用方式（在数据收集阶段）

```bash
# 单次：拿最新数据/观点/事件解读
python -m tools.fin_ai ask "{公司名} 最新市场观点和研报解读" --ttl-hours 24

# 多轮 REPL：深入对话（4-5 轮覆盖业务/竞争/估值/风险）
python -m tools.fin_ai ask --multi "{公司名}"

# 查剩余配额（每日 80 次硬上限）
python -m tools.fin_ai quota
```

### 数据使用原则

| 数据类型 | 处理方式 |
|---------|---------|
| **事实数据**（EPS/BVPS/营收/业务结构/ROE 等）| **fin_ai 优先**——有数据则以 fin_ai 为准确源，写入报告 §1 数据收集 |
| **计算数据**（PE/PB/ROE 等估值指标）| **必走 `tools/financial_rigor.py`**——用 fin_ai 提供的输入数据计算（Decimal，禁用 float）|
| **机构观点**（评级/目标价/多空论点）| 写入「§X.X 金融 AI 观点补充」段落，作为投资决策参考，**不替代**三情景估值 |

### 报告段落结构

将 fin_ai 内容嵌入「§X.X 金融 AI 观点补充」段落，明确标注：
- 来源：金融 AI（gangtise-reason），{日期}
- **数据类型**：事实数据（已采纳为准确源）/ 机构观点（参考层）
- 与程序化验算的关系：fin_ai 提供输入数据，但 PE/PB/ROE 等指标仍走 `financial_rigor.py` 精确计算

### 配额管理

⚠️ **配额 80/天是硬约束**。
- 数据收集阶段：单次 ask 拿研报观点（缓存 24h TTL，重复查询不烧配额）
- 长公司研究：用 `quota` 命令监控剩余配额
- B 级以下公司：如果完整 query 超时（>5 分钟），改用最短 query（如直接"小商品城"）重试
- fin_ai 无数据/超时/无配额时 fallback 到 tavily_search + 年报

### Python 库调用方式（在脚本中复用）

```python
from tools.fin_ai import ask, ask_multi_turn

result = ask("茅台研报观点", ttl_hours=24)
print(result.content)

with ask_multi_turn("长城军工") as session:
    r1 = session.ask("2025 年报怎么看？")
    r2 = session.ask("和北方导航比谁更好？")  # 上下文延续
```
