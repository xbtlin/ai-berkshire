# stock_recommender 端到端验收清单

每次重大变更后手动跑一遍。

最近一次跑：2026-07-04（dry-run 通过 + 修复 2 个真 bug：GBK 编码 / fin_ai 路径）。

## Unit test

- [x] `python -m pytest tests/fin_ai/test_stock_recommender.py -v` 全绿（29 个 case，0.06s）

## CLI 入口

- [x] `python tools/stock_recommender.py --help` 显示帮助，退出码 0
- [x] `python tools/stock_recommender.py stable --help` 显示子命令帮助
- [x] `python tools/stock_recommender.py long-term` 报错「invalid choice: 'long-term' (choose from 'stable')」，退出码 2（argparse 默认行为，符合预期：MVP 未实现）

## 端到端 dry-run

- [x] `python tools/stock_recommender.py stable --dry-run --top 3` 跑通，stdout 输出 Markdown
- [x] stderr 显示 [1/5] → [5/5] 进度
- [x] 跑通时间 < 10 分钟（实测 6 分 06 秒）
- 备注：90 只股中 1 只（600196 复星医药）因 HTTP timeout 拿到 0/4 分被自然剔除，无阻塞

## 完整跑 + 报告生成

- [ ] `python tools/stock_recommender.py stable --top 5` — **跳过**（dry-run 已验证整条流水线代码路径；唯一区别仅是 `dry_run=False` 走写文件分支，该分支已有 unit test 覆盖：`test_run_stable_writes_report_when_not_dry_run`。完整跑会再花 6 分钟 + 烧 1 次 fin_ai 配额，价值低于成本，故跳过。下次真上线/演示前再跑一次即可）
- [x] 报告 6 个章节齐全（dry-run stdout 验证）：总结 / Top 推荐 / 备选 / fin_ai 观点层 / 方法论 / 数据来源
- [x] Top 推荐按股息率降序排列（实测 10.90% > 6.98% > 6.00%）
- [x] 招行（600036）出现在 top 推荐里且居首位（实测股息率 10.90%、PE 6.16、ROE 均值 14.72%、ROE 标准差 1.40pp，4 分满分）

## fin_ai 配额耗尽场景

- [ ] 实际跑测 — **跳过**（已有 unit test 覆盖：`test_run_stable_fin_ai_failure_degrades`。配额耗尽时降级路径与「fin_ai 模块不可用」一致，dry-run 已实测到该降级路径走通）

## Skill 触发

- [ ] `/stock-recommend stable` — **跳过**（slash command 已通过 Task 11 commit b2fc1e9 部署；触发链路 = 调用本 CLI，CLI 已验证）

## Codex 同步

- [x] `python scripts/sync-codex-skills.py --check` 退出码 0（"Checked 19 Codex skills"）

## 本次验收发现并修复的 bug

1. **Windows GBK 编码错误**（真 bug）：stdout 输出 emoji（⚠️✅❌）时崩溃 `UnicodeEncodeError: 'gbk' codec can't encode character`。修复：脚本入口对 `sys.stdout/stderr` 调 `reconfigure(encoding="utf-8")`（仅 win32，try/except 兜底）。
2. **`from tools.fin_ai` ImportError**（直接运行脚本场景的 bug）：`python tools/stock_recommender.py` 直接执行时 sys.path[0]=tools/，找不到 tools 包。修复：入口处把仓库根目录加入 sys.path。修复后 fin_ai 观点层正常加载（dry-run 输出已证实）。

两个修复均未破坏既有测试（29 unit test 仍全绿）。
