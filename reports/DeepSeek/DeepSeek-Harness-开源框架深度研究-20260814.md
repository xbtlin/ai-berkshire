# 看懂 DeepSeek Harness：一切皆插件的开源智能体框架

> 写作日期：2026-08-14（开源后第 1 天）。本文所有事实经多信源交叉核实，19 个源站、90 条声明抽取、25 条进入三票对抗式验证（25 条确认、0 条被推翻）。项目 README 明确警告"将有破坏兼容性的变更"，本文所有架构细节锁定 v0.1（npm 0.1.0-rc.6）、取证日期 2026-08-14，数周内可能失效。

## 一句话总结

DeepSeek Harness（命令行名 `dsh`）是 DeepSeek 2026-08-13 首次开源的智能体执行框架（agent harness），MIT 许可、TypeScript 编写，核心设计是"一切皆插件"——模型适配器、工具注册表、会话日志乃至 agent 循环本身都可从配置替换，官方称"不存在可打补丁的特权内核"。它的目标受众是构建 agent harness 的开发者，而不是终端用户：官方零基准披露、零竞品对比，社区首日的主要批评是"只有架构、没有开箱即用能力"。

## 一、基本档案

| 项目 | 内容 |
| --- | --- |
| 发布时间 | 2026-08-13（官方 X 账号发布 v0.1 开发者预览版） |
| 仓库 | [github.com/deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) |
| 许可证 | MIT，无附加条款（Copyright (c) 2026 DeepSeek） |
| 主语言 | TypeScript，约 97%；47 个包的 monorepo |
| npm 包 | `@deepseek-ai/dsh`，latest = 0.1.0-rc.6，首发 2026-08-10（早于 GitHub 开源 3 天） |
| 仓库创建 | 2026-08-13T11:56:32Z（GitHub API 一手元数据） |
| 热度 | 约 34.3k → 34.7k star / 2.6k fork（核查当时仍在上涨，仅为时点快照） |
| 成熟度 | 开发者预览，Releases 页为空，无稳定 tag；仓库 issues 已关闭 |
| 基准成绩 | 官方零披露 |

README 首句原文：*"DeepSeek Harness (`dsh`) is an open-source agent harness developed by DeepSeek AI."* 仓库简介即 "Everything is a Plugin."

来源：[README](https://github.com/deepseek-ai/deepseek-harness/blob/master/README.md)、[官网](https://www.deepseek.com/harness/en/)、[官方 X 公告](https://x.com/deepseek_ai/status/2087887408440164663)、[GitHub API](https://api.github.com/repos/deepseek-ai/deepseek-harness)、[npm registry](https://registry.npmjs.org/@deepseek-ai%2Fdsh)

## 二、架构：一切皆插件

### 2.1 核心断言

官方架构文档 [architecture.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md) 原文：

> "Every part of the product is a plugin, including the model adapter, the tool registry, the session log, and the agent loop itself, so every part is replaceable from configuration."
>
> "There is no privileged core to patch: you extend dsh by mounting a plugin beside the others, and registrations are effects that unwind when their plugin unloads."

关键点在于 agent 循环本身也是插件。多数 agent 框架把"循环"写死在内核里，只开放工具和提示词两个口子；`dsh` 的设计是把循环也放进可替换清单，扩展方式是在旁边挂插件而非给内核打补丁。

### 2.2 三个支撑机制

**上下文即服务容器。** 每个服务占据一个稳定的 `ctx.<key>`，架构文档给出的真实服务键包括 `ctx.sessions`、`ctx.tools`、`ctx.llm`、`ctx.systemPrompt`、`ctx.agents`、`ctx.agentLoop`、`ctx.commands`、`ctx.jobs`、`ctx.fs`、`ctx.shell`、`ctx.sandbox`、`ctx.goals`、`ctx.sessionTitle`。官方中文文档 [cordis-primer](https://deepseek-harness.github.io/deepseek-harness/reference/cordis-primer) 逐字表述："其他插件通过 key 查找服务，而非导入具体实现"、"加载顺序通过服务依赖表达，而非手动编排启动序列"。

**注册即可逆副作用。** 提示词片段、工具 schema、适配器、监听器统一通过 `ctx.effect()` 或 `ctx.on()` 安装，文档称"reload 和 teardown 时会按预期撤销"。这决定了热重载和插件卸载不会留下残留状态。

**分层组合出插件树。** 启动时按序叠加：bundles → profile 的 `cordis.patch.yml` → home 级 → `--patch` 覆盖。官方三个 bundle：`@deepseek-ai/dsh-base`（模型适配器、工具、持久化、沙箱与审批策略、设置、凭证、遥测）、`dsh-web-app`（浏览器应用）、`dsh-headless`（无服务器的一次性运行器）。扩展点抽象为 seam（接缝），文档定义 seam = Service Definition（接口）+ Service Provider（实现）+ Consumer（消费方）；接入模型提供方即把适配器注册到 `ctx.llm`，接入工具即注册到 `ctx.tools`。

代码结构佐证这不只是口号：`packages/` 下 47 个包，含 `llm`、`core`（内含 agent-loop 默认实现）、`skill`、`session`、`sandbox`、`e2b`、`fs`、`storage`、`workflow`、`schedule`、`jobs`、`subagent`、`web`、`terminal`、`acp`、`mcp`、`shell`、`lsp`、`hooks`、`extensions` 等。

### 2.3 底座 Cordis：第三方项目，源码内嵌

README 写明框架"is powered by Cordis"。证据显示 [cordiverse/cordis](https://github.com/cordiverse/cordis) 是独立第三方项目，GitHub API 显示创建于 2022-05-17，比 Harness 早四年，自述为 "Meta-Framework of Spatiotemporal Composability"。

引入方式不是 npm 依赖，而是 vendor（源码内嵌）。[vendor/README.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/vendor/README.md) 明确写道该目录存放 Cordis 及其基础库的源码副本，理由是让 harness "fully owns its framework layer (auditable, patchable, pinned)"。清单含 cordis 4.0.0-rc.7、`@cordisjs/plugin-loader` 1.0.0-rc.5、plugin-include/group/timer/hmr/logger-console、cosmokit 1.8.1、schemastery 3.18.0 共 9 个包，附上游 commit、5 步同步流程与 18 条本地改动记录。根 `package.json` 的 workspaces 首项即 `vendor/*`，无 cordis 的 npm 依赖；`AGENTS.md` 设有 vendor 清单守卫（改 `vendor/*/src` 必须同步更新清单）。各包 `package.json` 仍以 peerDependency 形式声明 cordis，但解析到 vendor 工作区副本而非 registry。

值得注意的信号：cordis 仓库的 GitHub homepage 字段直接指向 DeepSeek 的文档站，证据表明双方存在紧密协作而非单方面搬用。

### 2.4 两处必要的精度修正

- README 引用的"论文"仓库 [cordiverse/paper](https://github.com/cordiverse/paper) 创建于 2026-08-13，与 harness 同日，应描述为设计文档而非同行评审论文。框架本体则确有四年历史，两者需分开表述。
- "不存在特权内核"不涵盖 Cordis 本体与 boot 流程，这两层是不可替换的底座；同时"加载顺序完全由服务依赖表达"也需补充——bundle/profile 层仍有显式的组合顺序。

## 三、模型支持与工具调用

### 3.1 模型无关，不绑定自家模型

官方文档 [providers.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/providers.md) 显示：内置目录直接支持 Anthropic、OpenAI 等提供方，填 API Key 即可，目录自带端点、协议与模型列表。Bedrock、Vertex、Azure、Codex 需各自原生鉴权（AWS 凭证 + region、ADC project、`api-version`、OAuth），文档明确写道"filling only the API-key field does not configure them"。还支持添加任意 OpenAI 兼容协议的企业网关或自托管端点（走 `GET /models` 发现模型），并可对具体模型做能力覆写，文档示例用的是 `claude-sonnet-4-5`。

包级佐证：`packages/llm` 下有 `llm`、`llm-deepseek`、`llm-pi-ai`、`llm-retry`、`token-meter`。`@deepseek-ai/dsh-llm-pi-ai` 自述为 pi-ai 驱动的通用多厂商适配器，示例中同时挂载 openai / anthropic / deepseek 路由。VentureBeat 独立称其为 Claude Code / Codex 底层基础设施的"模型无关替代品"。

反面证据（不对称之处）：界面上 DeepSeek 有专属卡片、其他提供方需走"Add provider"；且 providers.md 承认 DeepSeek 自家的 chat-completions 路由仅支持纯文本，无法另行配置。

### 3.2 工具调用是一条事件流水线

```
tool/call* → tools/pre-execute → tools/execute → tools/post-execute → tool/result*
```

架构文档写明三个 `tools/*` 是瀑布式事件，监听器必须调用 `next()` 才能向下传递；带星号的两端属于发出/流式的通知事件——不应把整条五段链路统称为瀑布式。更细的 [tool-execution-pipeline.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/tool-execution-pipeline.md) 显示：`pre-execute` 负责钩子、权限、沙箱，可拒绝或触发审批提示；`post-execute` 支持接受、阻断、替换、追加上下文；文档称"hooks span tool families without coupling the tools to one policy service"。

含义：权限校验、参数改写、审计日志全部以监听器插入，不需要改动执行核心。文档同时定义"一个 step = 一次模型请求加它调用的工具"。

## 四、部署方式

```bash
npx @deepseek-ai/dsh web       # 默认 Web 界面在 http://127.0.0.1:3080
```

源码方式：`pnpm install` → `pnpm run build` → `pnpm dsh web`（根 package.json 为 `@deepseek-ai/dsh-root` 0.1.0-rc.5，packageManager 为 pnpm@11.7.0）。另有 `dsh-headless` bundle 提供无服务器的一次性运行器。

需要限定的是：一条命令部署字面成立，但那只是本地起一个 Web 预览，不等于生产可用部署。

## 五、基准表现：官方零披露

这是本次研究最重要的否定性结论，需要单独强调。

抓取 README 完整原始 Markdown（非页面摘要）确认，全文小节仅为：标题段、Developer preview、Run、Community and support、Contributing、Development、License，**全文没有任何基准分数或性能表格**。官网落地页同样无基准数据。README 与官网均未出现 OpenHands、SWE-agent、Claude Code 等任何竞品名称，唯一引用的外部项目是底层 Cordis（依赖说明而非竞品对比）。

所有"开源版 Claude Code 竞品"的定位均出自第三方媒体（VentureBeat 标题、CryptoBriefing 报道），不是 DeepSeek 自身的主张。

**关键防混淆提示：** 网上流传的 SWE-bench 数字（如 DeepSeek V4-Pro 96.4% SWE-bench Verified、DeepSWE 54.4）属于模型侧成绩且多为厂商自报，与本仓库无关，不能挪用作 harness 的成绩。截至取证日期，不存在"同一模型下 dsh vs OpenHands vs SWE-agent vs Claude Code"的可比实测，任何关于 dsh 基准表现的结论目前都无一手依据。

## 六、局限与社区反馈

### 6.1 官方自述局限

README 设有独立小节，原文即全大写加粗：

> "DeepSeek Harness is currently in _developer preview_ and is iterating rapidly. **THERE WILL BE COMPATIBILITY-BREAKING CHANGES.**"

官网同口径："core plugins and APIs will continue to evolve"、"remains in developer preview and is still being tested"。GitHub Releases 页返回 "There aren't any releases here"，无任何 GA 或稳定 tag；仓库 issues 已关闭（`has_issues=false`），社区支持走 Discussions、`dsh-plugin` 话题与 Discord。

措辞精度：官方从未写"禁止用于生产"。"不适合生产"是基于 v0.1 + 零 release + 破坏性变更警告 + "still being tested" 四项的合理推论，属推测而非官方主张。Cordis 上游自身也自述 API 尚未稳定。

### 6.2 社区首日反馈（信心：中）

[Hacker News 讨论帖](https://news.ycombinator.com/item?id=49285244) 372 分 / 173 评论，项目作者本人现身（"Hi I'm one of the authors of DeepSeek Harness"，并回应"It's just an early developer preview version"）。GitHub API 于 2026-08-14 多次核查，star 从 34292 涨到 34689，fork 约 2633–2660，commits 约 12293（仓库仅创建 1 天，说明为内部历史导入，属正常代码外放，非归属疑点）。

主要批评原话：

- *"For me the problem is not that it has a plugin based architecture. It's that it ONLY has that. If there are no batteries included what's the point?"*——只有架构、缺开箱即用能力
- *"47mb downloaded, 1.5gb after build"*——安装与构建体积
- *"it looked just like every other harness"*——差异化不明显
- 第三方指出 `/memory`、`/tasks` 等命令尚不可用，skills 生态不完整
- Cordis 论文的"时空可组合性"表述被讥为堆砌辞藻

反面观察：这些批评全部是价值判断或成熟度问题，**没有人对"一切皆插件"、"基于 Cordis"这类事实性描述提出反驳**。争议在"值不值"，不在"是不是"。

### 6.3 两个必须避开的引用陷阱

1. 同名第三方仓库 [github.com/HenryZ838978/deepseek-harness](https://github.com/HenryZ838978/deepseek-harness)（附带 pip 包与另一个 npm 包 `@deepseek-harness/mcp`）与官方项目无关。另有低质站点 deepseek-harness.org 于 2026-08-03 声称"未找到官方安装器或公开仓库"，以及个人博客称其 agent 循环不可替换、技术栈为 Async Rust/Python——两者均与实际的 TypeScript/npm 仓库及官方架构文档矛盾，不可引用。
2. 历史上"DeepSeek 许可证不算真开源"的批评针对的是**模型权重**的 DeepSeek Model License（含使用限制），与本次 harness 代码库的标准 MIT 是两回事。第三方分析（Black Duck 等）明确区分过两者。

## 七、定位判断

证据指向一个结论：这不是 DeepSeek 版 Claude Code，而是 DeepSeek 版"造 Claude Code 的地基"。

支撑该判断的事实有三条：官方一次都没提竞品，一次都没放跑分；目标受众被明确写为"面向全球构建 agent harness 的开发者"；README 只有 Run 一节涉及使用，其余全是架构与贡献指引。它卖的是可组合性（连 agent 循环都能换），不是开箱即用。

由此推出两条实用结论：

- **作为日常编码智能体用**：现在还早。v0.1、部分命令缺失、skills 生态不完整、破坏性变更已被官方预告。
- **作为自研内部 agent 平台的参考或底座**：值得读。"服务挂在上下文 + 注册即可逆副作用 + 工具流水线可插监听器"这套设计，把权限、沙箱、审计做成插件而不动执行核心——这恰是多数自研 harness 到中后期最痛的地方。

但另一方面，反向风险同样明确：整套架构结论几乎全部来自项目自身文档（README、architecture.md、cordis-primer、官网），属于官方设计自述加仓库结构佐证，**不是第三方独立审计**。"可自由混搭、替换"的工程成熟度——生态插件数量、跨版本兼容、真实可替换性——目前没有任何外部验证。HN 上"只有架构没有内容"的批评，本质上就是在质疑这套抽象的兑现能力。

## 八、待解问题

1. **实测表现**：dsh 在 SWE-bench Verified / Terminal-Bench 等公开基准上的表现如何？官方零披露、第三方无独立复现，缺一个 harness 层面的可比评测。
2. **插件生态成熟度**：`dsh-plugin` 话题下目前有多少可用第三方插件？MCP（`packages/mcp` 已存在）、subagent、workflow、skills 的完成度与 Claude Code 生态差距多大？HN 上的"缺开箱即用能力"批评是否会在后续版本被补齐？
3. **沙箱与权限强度**：`pre-execute` 阶段的权限、沙箱与审批策略如何落地？`e2b` 包与 `native/` 目录起什么作用？是容器/系统级隔离还是仅进程内策略？这对企业部署是关键，本轮未深入。
4. **DeepSeek 与 Cordis 的实际关系**：cordis 仓库 homepage 反指 DeepSeek 文档站，vendor 内含 18 条本地改动并重新发布到 `@deepseek-ai` scope——两者是雇佣、共建还是松散协作？上游演进与 vendor 分叉未来如何同步，会否形成事实分叉？
5. **技术选型**：为何选 TypeScript/Node 而非 Python（主流 agent 生态语言）？这对与 Python 侧 SWE-bench 评测框架、现有 agent 工具链的集成成本有何影响？

## 九、方法论与引用须知

- 研究方法：5 个搜索角度并行（官方发布事实 / 架构与插件机制 / 模型支持与工具调用 / 同类框架横评 / 社区反馈与局限）→ 抓取 19 个源站 → 抽取 90 条声明 → 25 条进入三票对抗式验证（需 2/3 票推翻才淘汰）→ 合并语义重复后保留 11 条核心结论。验证结果：25 条确认、0 条推翻、0 条存疑。
- **star / fork / commit 数为时点快照**，核查过程中 star 就从 34292 涨到 34689，任何引用必须带时间戳。
- 社区反馈部分主要来自 Hacker News 单帖，样本窄且是发布首日，代表性有限。
- 与 OpenHands / SWE-agent / Claude Code 的对比在本轮无任何可靠一手或第三方实测材料，只有媒体的定位式表述，不构成能力对比结论。
- 官方 X 帖的引文在检索中出现过带 Markdown 粗体的疑似二次加工版本，建议优先引用 GitHub 仓库与 deepseek.com/harness 页面作为来源。
- 搜索阶段有一条未进入验证环节的线索：官网疑似列出四种运行模式（Standard / Code / Minimal / Creator，部分媒体把 Code Mode 称作 PTC 程序化工具调用）。该条未经三票验证，仅供参考，不作结论。
