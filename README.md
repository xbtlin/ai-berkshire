中文 | [English](README_EN.md) | [日本語](README_JA.md)

[![GitHub Trending](https://trendshift.io/api/badge/repositories/63696)](https://trendshift.io/repositories/63696)

# AI Berkshire - AI 时代的价值投资研究框架

> "Price is what you pay, value is what you get." — Warren Buffett
>
> 用 AI 重新定义投资研究的深度与效率。

**AI Berkshire** 是一套同时兼容 Claude Code 与 Codex 的投资研究 Skill 合集，将巴菲特、芒格、段永平、李录四位价值投资大师的方法论系统化、结构化，通过 AI Agent 实现专业级投资研究。

一个人 + Claude Code / Codex = 一个投研团队。

> 📮 **仓库是全量框架，公众号是精选。** 真正值得深研的公司，加上报告之外我自己的判断与取舍，都在微信公众号「**复利炼丹炉**」——[扫码关注 ↓](#精选研究首发于公众号)

[实盘业绩](#real-track-record) · [为什么不能直接问AI](#为什么不能直接问-ai) · [Skills 一览](#skills-一览20个) · [快速开始](#快速开始) · [实战报告](#实战研究报告) · [设计理念](#设计理念) · [公众号](#精选研究首发于公众号)

---

## Real Track Record

> 不是纸上谈兵。这套框架背后是真金白银验证的投资体系。

### 2024 全年收益：+69.29%

<img src="assets/2024-returns.jpg" width="300" />

### 2025 全年收益：+66.38%

<img src="assets/2025-returns.jpg" width="300" />

### 与主要指数对比

| 指标 | 2024 全年 | 2025 全年 |
|------|----------|----------|
| **本框架实盘** | **+69.29%** | **+66.38%** |
| 恒生指数 | +17.67% | +27.77% |
| 标普500 | +23.31% | +16.39% |
| 沪深300 | +14.68% | +17.66% |
| 纳斯达克 | +28.64% | +20.36% |

**2024 年超额收益**：跑赢标普500 **46个百分点**，跑赢恒生指数 **52个百分点**

**2025 年超额收益**：跑赢标普500 **50个百分点**，跑赢恒生指数 **39个百分点**

**两年累计实盘收益超 146万元**，连续两年大幅跑赢全球主要指数。

> *免责声明：历史收益不代表未来表现。截图来自富途证券真实账户。*

### 精选研究首发于公众号

仓库里是完整的框架和全量报告，公众号里是**精选**——真正值得深研的公司，加上报告之外我自己的判断与取舍：

<img src="assets/wechat-qr.png" width="160" alt="微信公众号：复利炼丹炉" />

**复利炼丹炉** —— 用 AI 炼投研这颗丹。

---

## 为什么不能直接问 AI？

你当然可以直接问 Claude："帮我分析拼多多值不值得买"。你会得到一篇"一方面...另一方面..."的平衡分析，最后以"投资有风险，请自行判断"收尾。

**这种分析看起来对，但没法拿来做决策。**

AI Berkshire 解决的不是"能不能分析"的问题，而是**分析质量和决策纪律**的问题。以下是核心差异：

### 1. 强制给结论，不打太极

直接问AI，你得到的是两面讨好的"分析"。AI Berkshire 强制输出：**通过/不通过/灰色地带**，带具体价格区间和分层建议。

> 普通AI回答：*"拼多多有增长潜力但也面临竞争压力，投资者需要权衡..."*
>
> AI Berkshire 输出：

> | 策略 | 建议 | 价格区间 |
> |------|------|---------|
> | 激进型 | 当前价位可建仓20% | $95-105 |
> | 稳健型 | 等回购政策明确后建仓 | $85-95 |
> | 保守型 | 不符合10年确定性标准，观望 | — |
>
> **镜子测试**：5句话说不完整 = 不买，没有例外。

### 2. 四大师视角对抗，而非单一分析

不是"用巴菲特方法分析一下"这么简单。四个视角会产生**真实的矛盾和张力**——

以拼多多为例：
- **段永平**（商业模式）：好生意，C2M模式难以复制 → 评分 3.7/5
- **巴菲特**（财务估值）：扣现金PE仅6.3x，印钞机 → 评分 4.4/5
- **芒格**（逆向思考）：护城河比想象中浅，抖音3年做到4万亿GMV → 评分 3.5/5
- **李录**（长期确定性）：管理层文化有隐患，10年后不确定 → 评分 2.0/5

**巴菲特说"真便宜"，李录说"不确定就不买"**——这种冲突才是投资决策的真实状态。单一prompt无法制造这种多视角对抗，而这恰恰是避免盲点的关键。

### 3. 结构化反偏见机制

AI最危险的不是给错答案，而是给一个**看起来很对但经不起推敲**的答案。AI Berkshire 在流程中内置了多层"防骗"机制：

| 机制 | 解决什么问题 | 举例 |
|------|------------|------|
| **信息丰富度评级（A/B/C）** | 防止"资料多=确定性高"的幻觉 | 泡泡玛特评为B级：数据有限，推算指标标注置信度 |
| **芒格式逆向检验** | 强制思考失败场景 | "什么情况下拼多多会死？"→ 列出5大情景及概率 |
| **快速否决清单** | 8条红线一票否决 | 管理层诚信污点 → 直接否决，不管估值多便宜 |
| **反共识检查** | 避免和市场想法一样 | "聪明人为什么在做空？"→ 发现被忽视的风险 |
| **留白原则** | 宁可说"不知道" | 数据不足时标注"灰色地带"，不用推测伪装确定性 |

### 4. 金融数据的精确性

LLM心算不可靠。PE算错一个小数点、市值单位搞混港币和人民币，就可能导致错误的投资决策。

**真实案例**：分析腾讯时，不同来源的市值数据有"港币亿"和"人民币亿"两种单位。AI Berkshire 的处理方式：

```bash
# 市值手算校验：股价 × 总股本，与报告数据对比
python3 tools/financial_rigor.py verify-market-cap \
  --price 510 --shares 9.11e9 --reported 4.65e12 --currency HKD
# ✅ 验证通过, 偏差仅 0.08%
```

所有计算使用 Python `decimal.Decimal`（精确十进制），不用 `float`。关键数据至少2个独立来源交叉验证。

### 5. 可复现的研究流程

直接问AI，每次输出的格式、深度、覆盖面都不一样——今天分析腾讯有护城河评分，明天分析美团可能就忘了。

AI Berkshire 确保：**同样的输入 → 结构一致、深度一致的输出**。这意味着你可以：
- 7家公司横向对比，评分标准完全一致
- 同一家公司半年后重新分析，直接对比变化
- 团队成员之间的研究结果可以对齐

> 真实输出——7家公司用同一标准 Checklist 筛选：
>
> | 公司 | 通过? | 能力圈 | 好生意 | 护城河 | 管理层 | 安全边际 | 综合 |
> |------|:-----:|:------:|:------:|:------:|:------:|:-------:|:----:|
> | 茅台 | ✅ 通过 | ★★★★★ | ★★★★★ | ★★★★★ | ★★★☆☆ | ★★★★☆ | 4.7 |
> | 腾讯 | ✅ 通过 | ★★★★☆ | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ | 4.7 |
> | 英伟达 | ✅ 有条件 | ★★★★☆ | ★★★★★ | ★★★★★ | ★★★★★ | ★★★☆☆ | 4.3 |
> | 美团 | ✅ 有条件 | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | 4.0 |
> | 快手 | ✅ 有条件 | ★★★☆☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★★ | 4.0 |
> | 拼多多 | ❓ 灰色 | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | ★★★★★ | 3.8 |
> | 泡泡玛特 | ❓ 灰色 | ★★★☆☆ | ★★★★☆ | ★★★★☆ | ★★★★★ | ★★★☆☆ | 3.7 |

### 6. 多Agent并行 = 研究深度的倍增

`/investment-team` 启动4个独立Agent**同时**研究一家公司。每个Agent各自搜索网络、交叉验证数据、独立给出结论。这不是把一个prompt拆成四段——是4个"分析师"各自做了完整的研究，Team Lead再综合。

一个人直接问AI，上下文窗口是一个。4个Agent并行，等于4倍的搜索量、4倍的信息源、4个独立视角。

<p align="center">
  <img src="assets/team-core.svg" alt="Team Lead 并行调度四大师 Agent" width="720" />
</p>

### 一句话总结

> **普通人问AI得到的是"看起来对的分析"，用 AI Berkshire 得到的是"可以拿来做决策的投研报告"。**

---

## 整体架构

<p align="center">
  <img src="assets/architecture.svg" alt="AI Berkshire 整体架构" width="760" />
</p>


**三层设计哲学**：
- **Skill 层**：把"你要做什么"抽象成 20 个明确入口——深度研究、财报分析、行业筛选、持仓管理、思维工具，按场景选用
- **Agent 层**：团队型 skill（如 `/investment-team`、`/earnings-team`）由 Team Lead 并行调度 4 个大师视角 Agent——各自独立搜索、独立判断、互相挑战，最后综合研判；轻量 skill 不经过这一层，直连工具快进快出
- **工具层**：精确计算、实时检索、报告抽检——保证每份报告的数据严谨性可验证

---

## Skills 一览（20个）

### 🔬 深度研究类

| Skill | 用途 | 适合场景 |
|-------|------|---------|
| [`/investment-research`](skills/investment-research.md) | 四大师综合深度分析 | 对一家上市公司进行全方位投资研究 |
| [`/investment-team`](skills/investment-team.md) | 多Agent并行投研团队 | 4个Agent并行研究，最快速、最全面 |
| [`/management-deep-dive`](skills/management-deep-dive.md) | 管理层纵深研究 | "买股票就是买人"——当管理层是核心变量时深挖 |
| [`/private-company-research`](skills/private-company-research.md) | 未上市公司深度研究 | 研究蚂蚁、SpaceX等信息稀缺的未上市公司 |
| [`/deep-company-series`](skills/deep-company-series.md) | 8篇长文系列拆一家公司 | 公众号级深度系列，12万字从认知重置到决策闭环 |

### 📊 财报分析类

| Skill | 用途 | 适合场景 |
|-------|------|---------|
| [`/earnings-review`](skills/earnings-review.md) | 财报精读（一手资料） | 只读原始财报，不依赖二手研报，像巴菲特一样读年报 |
| [`/earnings-team`](skills/earnings-team.md) | 财报精读团队 + 公众号发布 | 四大师并行解读财报 → 编辑润色 → 读者评审 → 可发布文章 |

### 🏭 行业筛选类

| Skill | 用途 | 适合场景 |
|-------|------|---------|
| [`/industry-research`](skills/industry-research.md) | 产业链全景扫描 | 研究一个行业的全部投资机会（按产业链环节切片） |
| [`/industry-funnel`](skills/industry-funnel.md) | 行业漏斗筛选 | 全市场 → 粗筛 ≤10 家 → 终选 3 家深度分析 |
| [`/quality-screen`](skills/quality-screen.md) | 去劣筛选（7条硬指标） | 快速排除非一流公司，支持个股/行业/指数/主题批量筛 |
| [`/bottleneck-hunter`](skills/bottleneck-hunter.md) | 供应链瓶颈猎手 | 从超级趋势出发，寻找产业链物理瓶颈和套利机会 |
| [`/investment-checklist`](skills/investment-checklist.md) | 巴菲特买入前 Checklist | 六关快速筛选，10分钟决定是否值得深入 |

### 📈 持仓管理类

| Skill | 用途 | 适合场景 |
|-------|------|---------|
| [`/income-investment`](skills/income-investment.md) | 收益型股票分析 | 区分可持续收益、机会型高息与收益率陷阱 |
| [`/portfolio-review`](skills/portfolio-review.md) | 组合管理与优化 | 从"研究公司"升级到"管理组合"——仓位、集中度、再平衡 |
| [`/thesis-tracker`](skills/thesis-tracker.md) | 投资论文追踪 | 买入后的纪律系统：持续跟踪论文是否被证伪 |
| [`/thesis-drift`](skills/thesis-drift.md) | 投资论文漂移检测 | 对比两份论文/报告，区分事实变化、估值变化与措辞变化 |
| [`/news-pulse`](skills/news-pulse.md) | 股价异动快速归因 | 股价大涨/大跌时10分钟搞清"发生了什么" |

### 🧠 思维工具类

| Skill | 用途 | 适合场景 |
|-------|------|---------|
| [`/dyp-ask`](skills/dyp-ask.md) | 段永平问答 | 以段永平的方式思考任何问题——商业、投资、人生 |
| [`/financial-data`](skills/financial-data.md) | 财务数据获取与交叉验证规范 | 确保关键数据来自2个独立来源，误差>1%告警 |
| [`/wechat-article`](skills/wechat-article.md) | 微信公众号文章 | 作者、编辑、读者三Agent协作，产出可发布文章 |

---

## 快速开始

### 成本与模型选择

深度投研类 Skill 默认会进行多轮研究、交叉验证和多 Agent 综合判断，因此 token 消耗较高，这是为了换取更完整的商业、财务、行业和风险分析。

如果是真实投资决策中高风险、高重要性的判断，维护者的观点是：最强模型通常更可能带来更好的分析 ROI，不建议只为节省模型成本而牺牲关键判断质量。轻量模型更适合做初筛、摘要或低风险问题；涉及护城河、估值、管理层和风险交叉判断时，应预期分析质量会更依赖模型能力。

想控制成本时，优先调整 workflow，而不是期待完整深度研究变得便宜：快速排除公司可先用 [`/quality-screen`](skills/quality-screen.md)，股价异动归因可用 [`/news-pulse`](skills/news-pulse.md)。只有当结果值得继续深入时，再运行 [`/investment-research`](skills/investment-research.md) 或 [`/investment-team`](skills/investment-team.md)。

### 1. 安装 AI 客户端

本仓库保留同一套 canonical workflow，并分别提供 Claude Code commands 与 Codex skills。按你使用的客户端安装即可。

Claude Code 用户：

```bash
npm install -g @anthropic-ai/claude-code
```

Codex 用户：

```bash
# macOS / Linux
curl -fsSL https://chatgpt.com/codex/install.sh | sh

# 或使用 npm
npm install -g @openai/codex

# 或使用 Homebrew
brew install --cask codex

# 验证安装
codex --version
```

Windows 用户可使用官方 PowerShell 安装命令：`powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"`。

如果 `codex --version` 能正常输出版本号，就可以继续安装本项目的 Codex skills。

#### 减少授权确认

这些 skills 会频繁调用工具，Claude Code 默认会逐次请求授权确认。这个行为来自 Claude Code 客户端权限机制，不是本仓库可以修改的默认设置。

如果你信任当前 workflow，并且在可信环境中运行，可以用 Claude Code 的跳过权限确认模式启动：

```bash
claude --dangerously-skip-permissions
```

注意：该模式会关闭 Claude Code 的工具审批保护，只应在你信任仓库、命令和工作目录的情况下使用。

### 2. 安装 Skills

Claude Code 用户安装（macOS / Linux）：

```bash
# 克隆仓库
git clone https://github.com/xbtlin/ai-berkshire.git

# 复制 skills 到 Claude Code 全局 commands 目录
cd ai-berkshire
./scripts/install-claude-commands.sh
```

Claude Code 用户安装（Windows PowerShell / Command Prompt）：

```bat
git clone https://github.com/xbtlin/ai-berkshire.git
cd ai-berkshire
.\scripts\install-claude-commands.bat
```

Codex 用户安装（macOS / Linux）：

```bash
# 克隆仓库
git clone https://github.com/xbtlin/ai-berkshire.git

# 生成并安装 Codex skills 到 ~/.codex/skills
cd ai-berkshire
./scripts/install-codex-skills.sh

# 可选：安装 Codex slash prompts 到 ~/.codex/prompts
# 用于获得接近 Claude Code 的 /investment-research 体验
./scripts/install-codex-prompts.sh
```

Codex 用户安装（Windows PowerShell / Command Prompt）：

```bat
git clone https://github.com/xbtlin/ai-berkshire.git
cd ai-berkshire
.\scripts\install-codex-skills.bat

REM 可选：安装 Codex slash prompts
.\scripts\install-codex-prompts.bat
```

仓库同时维护三套入口：`skills/*.md` 是 Claude Code command 源文件；`codex-skills/*/SKILL.md` 是 Codex skill 包，由 `scripts/sync-codex-skills.py` 从 `skills/*.md` 生成；`codex-prompts/*.md` 是可选的 Codex slash prompt 兼容层。

### 3. 使用

在 Claude Code 中直接调用：

```bash
# 深度研究
/investment-research 腾讯
/investment-team 美团
/management-deep-dive 王兴 美团
/private-company-research SpaceX
/deep-company-series 拼多多

# 财报分析
/earnings-review 腾讯 2025Q4
/earnings-team PDD 2025年报

# 行业筛选
/industry-research 核电
/industry-funnel AI算力
/quality-screen 恒生指数成分股
/bottleneck-hunter AI基础设施
/investment-checklist 茅台, 英伟达, 苹果

# 持仓管理
/income-investment Verizon mode=existing role=core-income quantity=100 cost_basis=39.50 tax_residence=France horizon=5y
/portfolio-review 腾讯30%, 美团20%, 茅台20%, 现金30%
/thesis-tracker 拼多多
/thesis-drift 拼多多 reports/拼多多-thesis-2025Q4.md reports/拼多多-thesis-2026Q1.md
/news-pulse 腾讯

# 思维工具
/dyp-ask 拼多多的护城河到底在哪里？
/wechat-article 美团
```

在 Codex 中安装后重启 Codex，然后直接按 skill 名称描述任务，例如：

```text
使用 investment-research 研究腾讯
使用 earnings-review 分析 PDD 2025年报
使用 industry-funnel 筛选 AI算力
使用 bottleneck-hunter 扫描 AI基础设施瓶颈
使用 thesis-drift 对比拼多多两份投资论文
使用 wechat-article 写美团投研文章
```

如果安装了 Codex slash prompts，重启 Codex 后也可以在 `/` 菜单里搜索这些 prompt。Codex 官方的 custom prompt 入口通常显示为 `prompts:<name>`，例如：

```text
/prompts:investment-research 腾讯
```

---

## 各 Skill 详细介绍

### 1. `/investment-research` — 四大师综合分析

最全面的单公司深度研究框架。按七个模块顺序执行：

```
数据收集 → 生意本质(段永平) → 护城河(巴菲特) → 逆向思考(芒格)
    → 管理层评估(段永平+巴菲特) → 文明趋势(李录) → 估值与安全边际
```

**核心特色**：
- AI研究偏见自觉机制（A/B/C级信息丰富度评级）
- 关键数据多源交叉验证（市值手算校验、至少2个独立来源）
- 四位大师的"追问"贯穿全文
- 三情景估值（乐观/中性/悲观）+ 反向DCF

**输出示例摘录**：

> #### 综合决策备忘录
>
> | 维度 | 结论 | 信心度 |
> |------|------|--------|
> | 生意质量（段永平） | 极佳：平台型生意，双边网络效应，边际成本趋零 | ★★★★★ |
> | 护城河（巴菲特） | 宽阔且在变宽：网络效应+转换成本+规模效应三重叠加 | ★★★★☆ |
> | 管理层（段永平+巴菲特） | 优秀：创始人掌舵，资本配置纪律强 | ★★★★☆ |
> | 最大风险（芒格） | 监管政策不确定性，新业务亏损拖累整体利润 | ★★★☆☆ |
> | 文明趋势（李录） | 顺应数字化消费趋势，但非"文明级范式转移" | ★★★★☆ |
> | 估值（巴菲特+段永平） | 当前PE 18x，处于历史中位数偏低，有一定安全边际 | ★★★★☆ |
>
> **段永平**："这门生意的本质是连接消费者和商家，赚的是效率提升的钱。好生意的标志是：用户越多，商家越多；商家越多，用户越多。飞轮一旦转起来，很难停下。"
>
> **芒格**："反过来想——如果这家公司明天消失，用户和商家会怎么办？如果答案是'很快找到替代品'，那护城河就不够深。如果答案是'生活会变得非常不方便'，那就值得关注。"

---

### 2. `/investment-team` — 多Agent投研团队

启动4个AI Agent并行研究，模拟真实投研团队协作。每个Agent独立搜索、独立分析、独立给出评分，最后由Team Lead综合研判。

**输出示例摘录**：

> #### 一句话结论
> 美团是中国本地生活服务的绝对龙头，拥有多重网络效应护城河，当前估值处于历史较低水平，长期投资价值显著，建议逢低建仓。
>
> #### 四维评分总表
>
> | 维度 | 框架 | 评分 | 核心判断 |
> |------|------|------|----------|
> | 商业模式 & 护城河 | 段永平 | ★★★★☆ | 双边网络效应强劲，外卖+到店形成飞轮 |
> | 财务 & 估值 | 巴菲特 | ★★★★☆ | 核心业务利润率持续改善，估值处于历史低位 |
> | 行业 & 竞争 | 芒格 | ★★★☆☆ | 抖音入侵到店业务，竞争格局有恶化风险 |
> | 风险 & 管理层 | 李录 | ★★★★☆ | 王兴战略眼光出色，但新业务烧钱需警惕 |
>
> **综合评分：3.8 / 5**
>
> #### 投资建议
>
> | 策略 | 建议 | 价格区间(港元) |
> |------|------|---------------|
> | 激进型 | 当前价位可建仓30% | 120-140 |
> | 稳健型 | 等回调至100-110建仓 | 100-120 |
> | 保守型 | 等待季报验证利润率趋势后再介入 | <100 |

---

### 3. `/investment-checklist` — 巴菲特买入前 Checklist

六关快速筛选，帮你在10分钟内决定一家公司是否值得深入研究：

```
第一关：能力圈（我能理解吗？）
    ↓ 通过
第二关：好生意（经济特征如何？）
    ↓ 通过
第三关：护城河（竞争优势深不深？）
    ↓ 通过
第四关：管理层（值得信任吗？）
    ↓ 通过
第五关：安全边际（价格便宜吗？）
    ↓ 通过
第六关：决策纪律（是理性还是FOMO？）
    ↓ 通过
   ✅ 镜子测试
```

**支持多公司对比**——一次筛选多个标的：

```
/investment-checklist 腾讯, 阿里巴巴, 美团, 拼多多
```

**输出示例摘录**：

> #### 镜子测试
>
> "我以 380港元 买入 腾讯，因为：
> 1. 这门生意的本质是**社交网络+数字内容平台**，我理解它；
> 2. 它的护城河是**12亿用户的社交关系链**，而且在变宽；
> 3. 管理层**Pony Ma低调务实、资本配置优秀**，值得信赖；
> 4. 当前价格相当于内在价值的**8折**，有一定安全边际；
> 5. 即使我错了，下行风险可控，因为**账上净现金超2000亿、游戏现金流强劲**。"
>
> ✅ 通过镜子测试
>
> **5句话说不完整 = 不买。没有例外。**

---

### 4. `/industry-research` — 产业链全景扫描

从一个投资主题出发，完成产业链全景研究：

```
投资逻辑链构建 → 产业链全景图 → 全球上市公司扫描
    → 各环节头部公司四大师分析 → 投资组合配置建议
```

**输出示例摘录**：

> #### 投资逻辑链：核电
>
> 底层趋势：AI数据中心电力需求爆发 + 碳中和目标
> → 导致：稳定清洁基荷电源需求激增
> → 创造：核电重启/新建/SMR的确定性需求
> → 受益：铀矿 → 燃料加工 → 设备制造 → 运营商
>
> #### 推荐组合
>
> | 层级 | 仓位 | 标的 | 环节 | 核心逻辑 |
> |------|------|------|------|---------|
> | 核心 | 50% | 中国广核(CGN)、Cameco | 运营+铀矿 | 确定性最高 |
> | 卫星 | 30% | 中国核电、东方电气 | 运营+设备 | 国产替代受益 |
> | 期权 | 15% | NuScale、Nano Nuclear | SMR | 高风险高弹性 |
> | ETF | 替代 | URA、URNM | 全链 | 懒人方案 |

---

### 5. `/industry-funnel` — 行业漏斗筛选

从一个行业/方向出发，**全市场 → ≤10 家 → 3 家**逐层精选：

```
全市场扫描（活跃度 + 涨幅 + 市值前 30 并集，30-60 家）
    ↓ 价值投资 5 条硬指标
粗筛 ≤ 10 家
    ↓ 精细分析（每家 300-500 字）
精细分析 ≤ 10 家
    ↓ 终选（按组合互补性，不按打分前 3）
四大师深度分析 3 家（每家 800-1200 字）
    ↓
推荐组合（核心 / 卫星 / 期权）+ 操作信号
```

**核心特色**：
- 每层都有明确留/弃标准，被淘汰的标的留下淘汰理由（不是黑箱）
- 终选 3 家按"组合互补性"选（高确定性 + 中等弹性 + 高弹性），不按打分前 3 排序
- 强制列"未来 IPO 候选"，避免漏掉一级市场核心玩家
- AI 偏见自觉机制：应对龙头偏好 / 英文偏好 / 故事偏好 / 上市偏好

**与 `/industry-research` 的区别**：
- `industry-research` 偏重产业链结构与全景（按环节切片）
- `industry-funnel` 偏重个股筛选漏斗（从全市场逐层精选到 3 家）

**实测：AI 行业 4 子赛道并行（2026-05-09）**：

| 子赛道 | 终选 3 家 | 核心仓位推荐 |
|-------|---------|------------|
| AI 算力 | TSMC / NVIDIA / SK Hynix | TSMC ★★★★★ |
| AI 模型 | Alphabet / Meta / 阿里巴巴 | Alphabet ★★★★★ |
| AI 应用 | 微软 / Adobe / AppLovin | 微软 + Adobe ★★★★ |
| AI 基建电力 | Eaton / 特变电工 / Talen Energy | Eaton + 特变电工 ★★★★ |

**关键发现**：AI 应用层最大赢家不是 AI Native 公司，而是有渠道+数据+工作流嵌入度的成熟巨头——这呼应了 1995-2000 互联网泡沫"卖铲子"的历史规律（亚马逊和苹果赢，Pets.com 输）。

完整报告：[AI 算力](reports/AI算力-funnel-20260509.md) · [AI 模型](reports/AI模型-funnel-20260509.md) · [AI 应用](reports/AI应用-funnel-20260509.md) · [AI 基建电力](reports/AI基建电力-funnel-20260509.md)

---

### 6. `/private-company-research` — 未上市公司深度研究

专为信息稀缺的未上市公司设计的"侦探式"研究框架：

**核心差异化**：
- **财务数据拼凑**：从招股书、母公司财报、融资新闻、行业数据多源拼凑
- **置信度标注**：每个数据点标注 🟢高 / 🟡中 / 🔴低 置信度
- **多方法估值交叉**：融资估值法 + 可比公司法 + DCF + 终局倒推法
- **退出路径分析**：IPO/并购/二级转让全路径评估

**输出示例摘录**：

> #### 公司画像速览：SpaceX
>
> | 项目 | 内容 |
> |------|------|
> | 最新估值 | ~$350B (2025年二级市场) 🟡 |
> | 推算收入 | ~$130亿 (2024年) 🟡 |
> | Starlink用户 | 400万+ (2024年底) 🟢 |
> | 发射次数 | 100+ 次/年 (2024年) 🟢 |
>
> #### 估值判断
>
> | 方法 | 估值区间 | 说明 |
> |------|---------|------|
> | 最近融资 | $350B | 二级市场报价，有流动性溢价 |
> | 可比公司法 | $200-280B | 对标电信+航天+国防 |
> | DCF(中性) | $250-350B | 假设Starlink 2027年$300亿收入 |
> | 终局倒推 | $400-600B | 假设星链成为全球电信基础设施 |
>
> **综合合理估值区间：$250B - $400B**

---

### 7. `/news-pulse` — 股价异动新闻归因

专为"股价大涨/大跌时快速搞清发生了什么"设计的情报响应 Skill。**不是深度投研，是 10-15 分钟的快速归因**——避免持仓异动时陷入小作文焦虑或盲目止损。

**核心差异化**：
- **4 维并行侦察**：公司事件 / 监管政策 / 行业对手 / 市场情绪（卖方+大V+南向资金）
- **归因优先于罗列**：不是把所有新闻列一遍，而是判断"哪个事件配得上这次股价异动"
- **强制性质判断**：价值事件 / 情绪波动 / **真因不明** / 混合——其中"真因不明"是最有价值的输出（可能存在内幕抢跑）
- **明确行动建议**：是否触发深度研究、是否需要重审论文、是否仅观察等

**与其他 Skill 的区别**：
| 场景 | 用什么 |
|------|------|
| 完整投研（小时级） | `/investment-team` 或 `/investment-research` |
| 财报深读 | `/earnings-review` |
| 长期论文跟踪 | `/thesis-tracker` |
| **股价异动 10 分钟归因** | **`/news-pulse`** |

**输出示例摘录**（腾讯 4/17-5/01 实测，14 天 -10.47%）：

> #### 一句话归因
> 这次 -10.47% 跌幅约 70-80% 由资金面+情绪面驱动（回购静默期 + 南向减仓 + 板块 beta + AI 叙事被夺），20-30% 由 AI 投入翻倍的递延消化承担——**基本面无利空**，卖方维持买入共识，性质上属于"流动性+情绪型回调"，不是价值事件。
>
> #### 异动归因表
>
> | 候选解释 | 估算贡献 | 置信度 |
> |---------|--------|--------|
> | 回购静默期消失（结构性，5/13 财报前） | -3% ~ -4% | 高 |
> | 南向资金转向净卖腾讯 | -2% ~ -3% | 高 |
> | AI 叙事被竞品夺走（DeepSeek V4/Qwen3.6/月暗 1T） | -1% ~ -2% | 中 |
> | 板块/宏观 beta（油价+地缘+Fed Warsh 鹰派） | -2% ~ -3% | 高 |
> | 一季报前避险 | -1% ~ -2% | 中 |
> | 基本面恶化 | **0%** | 极高（排除） |
>
> #### 性质判断：✅ 混合型
> 70% 资金面/情绪面 + 20% AI 长期叙事担忧 + 10% 一季报前不确定性
>
> **关键反证**：段永平 4/8 卖腾讯 put（看多）；卖方 24 家共识 Strong Buy；网易 4/30 逆市涨 2%（排除游戏行业问题）；腾讯跑输恒科 7 个百分点（恒科月度反而涨 4%）。

调用方式：

```
/news-pulse 腾讯
/news-pulse 拼多多 跌12% 一周内
/news-pulse 米哈游
```

---

## 实战研究报告

> 以下是使用本框架生成的真实投资研究报告，展示 AI 投研的实际输出效果。

| 公司 | 使用 Skill | 核心结论 | 报告链接 |
|------|-----------|---------|---------|
| 拼多多 (PDD) | `/investment-team` | 综合3.4/5，极度便宜但10年确定性不足，适合中等仓位 | [查看报告](reports/拼多多/) |
| 腾讯控股 (0700.HK) | `/investment-research` | 社交垄断+资本配置卓越，14x前瞻PE合理偏低 | [查看报告](reports/腾讯/) |
| 7家公司对比 | `/investment-checklist` | 茅台、腾讯通过；英伟达、美团、快手有条件通过；拼多多、泡泡玛特灰色 | [查看报告](reports/多公司对比-checklist-20260408.md) |
| 大师持仓追踪 | 自定义研究 | 巴菲特/李录/段永平最新13F持仓+PDD成本分析 | [查看报告](reports/大师持仓追踪-research-20260408.md) |

> *更多报告将持续添加。欢迎 PR 提交你用本框架生成的研究报告。*

---

## 设计理念

### 四大师方法论融合

**段永平 · "对的生意"**——商业模式本质，是其余三个视角的共同起点：

| 巴菲特 | 芒格 | 李录 |
|:---:|:---:|:---:|
| 护城河<br>安全边际<br>管理层 | 逆向思考<br>风险清单<br>偏误自查 | 文明趋势<br>范式转移<br>产业价值 |

四位大师不是简单的分工，而是设计来**互相挑战**的：
- 段永平说"好生意"，芒格会问"怎么会死"
- 巴菲特说"够便宜"，李录会问"10年后还在吗"
- 你得到的不是四份报告的拼接，而是四种思维方式的碰撞

### 金融严谨性工具 (`tools/financial_rigor.py`)

| 功能 | 命令 | 解决的问题 |
|------|------|-----------|
| **市值验算** | `verify-market-cap` | 股价×总股本 精确计算，检测单位错误 |
| **估值验算** | `verify-valuation` | PE/PB/ROE/FCF Yield 精确十进制计算 |
| **多源交叉验证** | `cross-validate` | N个来源的同一数据自动比对，超过容差告警 |
| **三情景估值** | `three-scenario` | 乐观/中性/悲观精确计算目标价 |
| **Benford定律检测** | `benford` | 检测财务数据首位数字分布异常 |
| **精确计算器** | `calc` | 任意财务表达式精确计算，替代LLM心算 |

**设计原则**：所有计算使用 Python `decimal.Decimal`（精确十进制），非 `float`（浮点近似）。`0.1 + 0.2 = 0.3` 在金融场景中不允许失败。

---

## 未来方向

- [ ] 历史回测：AI研报 vs 实际股价表现
- [ ] 宏观经济周期分析框架
- [ ] 基于MCP的实时数据接入（Wind/Bloomberg/Yahoo Finance）

---

## 免责声明

本项目仅供学习和研究目的，不构成任何投资建议。投资有风险，决策需谨慎。请始终做好自己的尽职调查（DYOR）。

---

## License

MIT License

---

> "The best investment you can make is in yourself." — Warren Buffett
>
> AI Berkshire：让每个人都拥有自己的投研团队。

## Star History

如果这个项目对你有帮助，请给一个 Star 支持！精选公司研究与个人判断首发于微信公众号「**复利炼丹炉**」（二维码见[文首](#精选研究首发于公众号)）。

<a href="https://github.com/xbtlin/ai-berkshire/stargazers">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/star-history-dark.svg">
    <img alt="Star History Chart" src="assets/star-history.svg">
  </picture>
</a>
