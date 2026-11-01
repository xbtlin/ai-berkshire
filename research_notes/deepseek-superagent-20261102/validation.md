# DeepSeek Super-agent 技术报告核验记录

核验日期：2026-11-02，Asia/Shanghai。

主报告：`reports/DeepSeek/DeepSeek-Super-agent-深度技术研究-20261102.md`。

## 核验范围

固定上游仓库 `deepseek-ai/dsh-superagent-prototype` 的提交 `6337fc823ce20251c8de8085948165c81aaa701e`，读取官方文档、关键实现与测试，独立运行上游检查。没有配置真实模型提供方、飞书机器人或具有写入权限的 GitHub agent；没有执行真实任务或复现设计文章的四方案调度基准。

核验环境为 Darwin x86_64，Node.js 24.22.1、Python 3.12.14、pnpm 11.25.0。上游 packageManager 声明 pnpm 11.7.0，本次使用的版本不同；依赖安装采用 frozen lockfile，且执行后上游 tracked tree 干净。没有修改上游源码。

## 复跑上游检查

在已安装满足上游要求的 Node.js、Python 和 pnpm 的环境中执行。下列步骤只运行软件检查，不启动 agent 服务。

```sh
node --version
python3 --version
pnpm --version
git clone https://github.com/deepseek-ai/dsh-superagent-prototype.git dsh-superagent-audit
cd dsh-superagent-audit
git checkout --detach 6337fc823ce20251c8de8085948165c81aaa701e
pnpm install --frozen-lockfile --ignore-scripts
pnpm check
git status --short
```

结果：类型检查通过，59 个测试文件、1,197 项测试通过，构建通过。构建器输出建议使用 ESM 而非 CommonJS 的警告，成功日志完整保留该警告。软件测试包含模拟 host 和平台接口；测试通过不能当作真实模型质量、平台稳定性或安全认证。

首次运行时 PATH 中的 Python 是旧版 3.7，服务脚本测试出现 `shlex.join` 不存在等错误，结果为 58 个文件通过、1 个文件失败，1,187 项通过、10 项失败。将 Python 切到满足前置条件的 3.12.14 后重新执行完整 `pnpm check`，全部通过。此前已切换 Node 到 24.22.1；未通过修改测试或源码绕过错误。

## 报告审计工具与人工复核

运行仓库工具：

```sh
python3 tools/report_audit.py extract \
  --report reports/DeepSeek/DeepSeek-Super-agent-深度技术研究-20261102.md \
  --ratio 1 --seed 42
```

提取到 16 项，其中 12 项是实验表格数字，4 项是年份或时分片段造成的误识别。12 项逐一与实际查看的实验原表核对；4 项日期片段从实验核验中排除，完整日期另与 GitHub 元数据核对。调用同工具的 `render_verdict` 得到表格数值 PASS，详情见 `report-audit.json`。

**这个 PASS 仅表示表格转录一致。** 工具面向财务数字抽检，不能验证授权语义、异步状态、实验独立性或正文全部事实，也未自动提取全部派生百分比。本文没有伪造第二个独立实验来源；转载和原表属于同一原作者来源。

八项派生值另以 `financial_rigor.py calc` 和 40 位精度 Decimal 复核，包含 p50/p95 相对下降、缓存量倍数、启用直通的节省比例和移除直通的增加比例。不同分母分别保留，结果见 `calculations.json`。

对 26 项关键代码与文档声明建立固定提交的证据索引。`evidence.json` 包含说明、文件、行号锚点、URL 和 SHA-256。行号锚点用于定位相关实现，不把文本匹配本身视为完整语义证明。

## 源码审查重点

- `Intake` 的 Trigger 去重、Subscription 扇出、follow-up ownership。
- `Policy` 的 accept mode、gate 和 Mandate revalidation。
- `Tickets.policyChanged` 通知与 `Tickets.wake` 恢复之间的区别。
- `Engine` 事务边界、SQLite savepoint、WAL、提交后动作与状态目录锁。
- `Effects` 的 kind/key、generation、重试，以及 `Outbox` 的回执写入。
- GitHub 标记查重与飞书幂等键；不外推为任意工具的恰好一次执行。
- WorkerSlots 同步预留、人类唤醒额外槽位、后台任务生命周期。
- Session 的完整权限、Router 工具和等待 guard。
- 资源读取范围、分页、存储增长、暂停与停止的区别。
- 管理 HTTP 检查和部署文档中的外部 hourly check。

## 证据来源限制

官方公众号访问返回环境验证页，知乎原文返回 403。设计文章的实验数据来自署名原作者的全文转载及其中实验表图片；原文入口和实际读取入口均在主报告末尾列出。该表未在本仓库重新分发图片，`calculations.json` 保存其来源地址与图片 SHA-256，供识别核对版本。

在固定提交公开文件树中，没有定位到对应四方案实验的完整负载、逐次结果与统计程序。存在大量软件测试，不代表存在可复跑的性能实验包。有关任务正确率、长期收益、真实成本、语义监督和多租户安全的外推，均在报告中明确限制或标为建议。

## 附件

- `evidence.json`：26 项实现证据及文件校验值。
- `calculations.json`：作者自报表格转录、来源图校验值及 8 项算术复核。
- `report-audit.json`：12 项表格数字核验、4 项误识别排除与工具结果适用边界。
- `upstream-check.txt`：成功执行上游检查的日志，归一化临时目录路径并清理行尾空白。

所有参考来源链接集中在主报告末尾。此核验不向真实平台发送测试消息，不以模拟接口测试替代联机实测。
