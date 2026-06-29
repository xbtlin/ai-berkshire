# Harness 主权审计与演进路线

> Module 6（主权与路线）的产出：盘点本仓库 harness 的主权属性（离线能力、
> 模型可插拔、模块化），并给出三阶段 earned-autonomy 路线。
> 原则（harness 框架 §8-§11）：harness 是主权层；假设 harness 会过期，故模块化、
> 模型可插拔；自治是用证据「挣来」的，不预先打开。

## 1. 主权审计（离线能力）

| 组件 | 类型 | 联网? | 主权说明 |
|------|------|:----:|---------|
| `report_audit.py sources` | Computational | 否 | 纯静态扫描，可 air-gapped 运行 |
| `report_audit.py balance` | Computational | 否 | 纯静态扫描，可 air-gapped 运行 |
| `financial_rigor.py` | Computational | 否 | 精确算术，可 air-gapped 运行 |
| `eval_sources.py` / `eval_balance.py` | Computational | 否 | 回归 eval，可 air-gapped 运行 |
| `.githooks/pre-commit` | Gate | 否 | 本地闸门，离线可用 |
| `report-gate.yml` (CI) | Gate | 云 | 逻辑离线；可迁至自托管/内网 runner |
| `sources verdict` 取数 | 人/agent 操作 | 是 | 工具本身离线；取数由 agent 联网完成 |
| 「正反两面」LLM 判官 | Inferential | 视实现 | **模型可插拔**：会话内 agent / API / 未来本地模型 |

**结论：确定性核心（Sensor + Gate + eval）完全 air-gappable。** 唯一的模型依赖是
Inferential 判官，且其规范已声明模型为可替换组件（见 `inferential-balance-judge.md` §5）。

## 2. 模型可插拔（不锁定 vendor）

- harness 不在任何 Sensor/Gate 里硬编码模型 id。
- Inferential 判官通过 prompt + JSON schema 定义**接口**，底层模型（Claude / 本地 LLM）
  可替换而不改动 harness 其余部分——符合「模型是插拔件，harness 是主权层」。

## 3. 假设 harness 会过期（模块化）

- 每个 Sensor 是 `report_audit.py` 里独立的 `check_*` 函数 + 独立子命令；
  某条规则过时可单独移除，不牵动其余。
- 规则识别表（`_SOURCE_PATTERNS` / `_COUNTER_MARKERS`）数据化，便于增删。
- 闸门逻辑与检测逻辑分离：hook/CI 只调用子命令，检测演进不改闸门。

## 4. Earned-autonomy 三阶段路线

自治分级——每升一级都要先用 eval/实绩证明，而非一开始就放开。

| 阶段 | Computational 闸门 | Inferential 判官 | 人的角色 |
|:----:|--------------------|------------------|----------|
| **GĐ1（现在）** | sources 硬阻断；balance 顾问 | 会话内按需运行，未校准 | 在环内：审每篇报告 |
| **GĐ2** | + market-cap / 命名规范 Sensor 进 CI | 判官完成 §6 校准（≥80% 一致）后常态出顾问意见 | 在环上：只复核被 flag 的 |
| **GĐ3** | 全部 Computational 闸门 CI 强制、不可绕过 | 判官稳定后自动出评审，仍**只顾问** | 在环上：维护 harness + 对关键结论署名 |

**红线（任何阶段不变）：** Inferential 判官永不升级为自动阻断/自动发布；
关键投资结论的最终判断与署名始终在人。

## 5. 下一个待建 Sensor（Improvement Engine 待办）

- **命名规范 Sensor**：校验 `reports/**` 文件名/目录符合 `report-conventions.md`
  （Module 2 留下的缺口：progressive disclosure 让规范「可得」，但还需机制「保证」）。
- **货币单位 Sensor**：报告内混用港币/人民币/美元时告警（CLAUDE.md 注意事项）。
- **判官校准集**：`tools/eval/balance/` ground truth + runner（见判官规范 §6）。
