# Inferential Sensor 规范：「正反两面」LLM 判官

> 这是 Module 5（Inferential Sensor / harness 中最难的语义判断层）的首个 Sensor 规范。
> 配套的 Computational 前置过滤已实现：`python3 tools/report_audit.py balance --report <md>`。
> 本文规定其上层 **LLM 判官**：当报告通过/触发前置过滤后，由 LLM 逐条核验
> 「每个核心判断是否附带**实质**反面论据」（CLAUDE.md：呈现正反两面）。

## 1. 为什么必须是 Inferential（而非 Computational）

`balance` 子命令只能确定性地检测**反面标记是否存在**（grep「风险/另一方面/下行」）。
但它无法判断反面是否**实质**：一句敷衍的「当然也有风险」会命中标记却毫无信息量。
「论据是否实质、是否针对核心判断」是**语义判断** → 必须用 LLM 当裁判（Inferential，GPU，昂贵）。

**分层（Computational 先、Inferential 后，省 token）：**
1. `balance` 前置过滤：完全无反面标记的实质报告 → 直接标 REVIEW，无需调用 LLM。
2. 有标记但需判断深度 → 才送入本判官。

## 2. 三条铁律（来自 harness 框架，不可违背）

- **顾问，不自动阻断。** 判官输出是给人的信号，**不接 auto-merge 硬闸门**。
  框架明确：安全/质量不押注于概率；AI 永远不是最终验收签名。
- **人在环上（on the loop）。** 判官缩小检查范围、定位可疑段落；
  「这篇是否达标」由分析师本人定夺并署名负责。
- **判官自身须先校准（见 §6）。** 未经校准的判官 = 不可信，只能当草稿提示。

## 3. 判官 Prompt（投喂给 LLM）

```
你是投研报告的「正反两面」审稿人。严格、客观，只依据给定报告正文。

任务：
1. 抽取报告中所有【核心判断】（对公司/行业/估值的实质性结论，通常 3-8 条）。
2. 对每条核心判断，判断报告是否提供了【实质反面论据】——
   即针对该判断本身、有信息量的反方证据或下行情形（不是敷衍的「也有风险」）。
3. 对每条给出：has_substantive_counter (true/false) + 一句理由 + 原文定位（行/段关键词）。

判定标准（实质反面）：
- 必须针对该具体判断，而非泛泛而谈。
- 必须有证据/数据/机制，而非情绪化措辞。
- 与正方论据相比，篇幅与认真程度不应悬殊到可忽略。

只输出 JSON，符合下方 schema。不要输出任何额外文字。
若无法判断某条，has_substantive_counter 置 false 并在 reason 说明「证据不足以判断」。
```

## 4. 输出 Schema（结构化，强制）

```json
{
  "type": "object",
  "required": ["judgments", "overall"],
  "properties": {
    "judgments": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["claim", "has_substantive_counter", "reason", "locator"],
        "properties": {
          "claim": {"type": "string"},
          "has_substantive_counter": {"type": "boolean"},
          "reason": {"type": "string"},
          "locator": {"type": "string"}
        }
      }
    },
    "overall": {
      "type": "object",
      "required": ["verdict", "coverage_ratio"],
      "properties": {
        "verdict": {"enum": ["BALANCED", "PARTIAL", "ONE_SIDED"]},
        "coverage_ratio": {"type": "number"},
        "weakest_claims": {"type": "array", "items": {"type": "string"}}
      }
    }
  }
}
```

`coverage_ratio` = 有实质反面的核心判断数 / 核心判断总数。
建议人工关注线：BALANCED ≥ 0.8；PARTIAL 0.5–0.8；ONE_SIDED < 0.5。

## 5. 如何运行

- **方式 A（推荐，空气隔离友好）：在 Claude Code 会话内运行。**
  让当前 agent 读取报告 + 本 prompt + schema，直接产出 JSON 评审，附在 PR/复核笔记里。
  无需 API key，便于 MẬT/离线场景。
- **方式 B（自动化）：薄 Python wrapper 调 Anthropic API。**
  需 `ANTHROPIC_API_KEY`；用最新 Claude 模型 + 强制 schema 工具调用。
  仅在愿意把报告正文送出本机时使用（涉密报告禁用）。
  实现前先查 `claude-api` 技能确认模型 id / 结构化输出用法。

## 6. 判官校准 Eval（判官的 eval harness —— 不可跳过）

判官也是概率模型，必须先证明它与人一致才可信：

1. 取 8–12 篇历史报告，**人工**标注每篇 overall.verdict（BALANCED/PARTIAL/ONE_SIDED）。
   这是 ground truth（C：人工，不可委托）。
2. 跑判官，记录其判定。
3. 指标：与人工标签的一致率（agreement）。
   - 目标先达 ≥ 80% 一致再投入使用；
   - 关注**假阴性**（判官说 BALANCED 实则一面倒）——投研里这类漏报代价最高。
4. 每次改 prompt/模型 → 重跑校准集（回归 eval，pass^k 思路：关键样本须每次都对）。
5. 每出现一次判官与人不一致 → 把该样本加入校准集，让该错误不可重现（Improvement Engine）。

校准集与脚本建议放 `tools/eval/balance/`（ground truth + runner），与 `tools/eval_sources.py` 并列。

## 7. 与既有 harness 的关系

| 规则 | 类型 | 机制 | 阻断? |
|------|------|------|:----:|
| ≥2 独立信源 | Computational | `sources` + pre-commit + CI | 硬阻断 |
| 市值手算 | Computational | `financial_rigor.py` | 可硬阻断 |
| **正反两面（实质）** | **Inferential** | `balance` 前置 + 本 LLM 判官 | **顾问，人署名** |

通用原则：**能数的用 Computational 硬闸门；要判断的用 Inferential 顾问 + 人在环上。**
这套分层将原样复用于物理 harness（FEA/NDT 前置确定性校验 → 代理模型判可疑 → 工程师署名）。
