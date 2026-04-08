# AI Berkshire — 项目指令

## 项目概述

基于 Claude Code 的价值投资研究 Skill 合集。四大师框架：巴菲特、芒格、段永平、李录。
GitHub: xbtlin/ai-berkshire

## 项目结构

```
skills/          — 投研 Skill 定义（.md），复制到 ~/.claude/commands/ 使用
tools/           — 辅助工具（financial_rigor.py 精确计算）
reports/         — 投资研究报告输出
assets/          — 图片等静态资源
```

## 报告命名规范

| 类型 | 命名格式 | 示例 |
|------|---------|------|
| 单公司深度研究（/investment-team） | `reports/{公司名}-{YYYYMMDD}/` 目录 | `reports/拼多多-20260407/` |
| 单公司快速研究（/investment-research） | `reports/{公司名}投资研究报告_{YYYYMMDD}.md` | `reports/腾讯投资研究报告_20260408.md` |
| 多公司Checklist | `reports/巴菲特Checklist-{主题}.md` | `reports/巴菲特Checklist-多公司对比.md` |
| 持仓追踪 | `reports/大师持仓追踪-{YYYYMMDD}.md` | `reports/大师持仓追踪-20260408.md` |
| 行业研究 | `reports/{行业名}行业研究_{YYYYMMDD}.md` | |

## /investment-team 目录结构

```
reports/{公司名}-{日期}/
├── README.md                         — 研究框架概览+核心结论
├── 01-商业模式分析-段永平视角.md
├── 02-财务估值分析-巴菲特视角.md
├── 03-行业竞争分析-芒格视角.md
├── 04-风险管理层评估-李录视角.md
└── 最终报告.md                       — Team Lead 综合报告
```

## 报告语言与风格

- 所有报告使用**中文**
- 风格：直接、犀利、不说废话
- 数据必须标注来源，关键数据至少2个来源交叉验证
- 估计值必须注明"估计"
- 评分使用★符号（★1-5），不含半星
- 穿插巴菲特/芒格/段永平/李录的语录点评

## GitHub 操作

- 本地克隆路径：`/tmp/ai-berkshire-upload/`
- 远程仓库：`https://github.com/xbtlin/ai-berkshire.git`
- 推送前先 `git pull --rebase origin main`（远程经常有新提交）
- commit message 用中文，描述清楚改了什么
- 不要推送中间过程文件（如 data_collection.md），只推最终报告

## 常用命令

```bash
# 推送报告到GitHub
cd /tmp/ai-berkshire-upload
cp ~/报告文件.md reports/
git add reports/xxx.md
git commit -m "添加xxx报告"
git pull --rebase origin main
git push origin main
```

## 注意事项

- 市值必须手算校验：股价 × 总股本，与报告市值对比
- 货币单位要明确（港币/人民币/美元），防止混淆
- PE/ROE等指标用 tools/financial_rigor.py 精确计算
- 报告写完后主动询问是否推送到GitHub
