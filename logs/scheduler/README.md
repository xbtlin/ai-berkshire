# logs/scheduler/

调度 Pipeline（`tools/scheduler/`）的运行日志目录。每次调 `claude -p /skill ...` 都会写一份 JSON 日志。

## 文件命名

```
{skill_name}-{YYYYMMDD-HHMMSS}.json
```

例如：
- `portfolio-review-20260705-200000.json`
- `industry-funnel-20260801-200000.json`

## 内容字段

| 字段 | 说明 |
|------|------|
| `skill` | skill 名（如 `portfolio-review`） |
| `args` | 传给 skill 的参数 |
| `command` | 完整命令（list 形式） |
| `started_at` / `ended_at` | ISO 时间戳 |
| `duration_sec` | 总耗时（秒） |
| `exit_code` | claude 进程 exit code（0=成功） |
| `ok` | exit_code == 0 |
| `stdout` | claude 输出（JSON 字符串，含 cost_usd / duration_ms） |
| `stderr` | 错误输出（排查用） |

## 不入 git

`.gitignore` 已配置 `logs/scheduler/*.json`，仅保留 `.gitkeep`。理由：
- stdout 可能含报告内容片段（持仓细节）
- 含 cost_usd 等运行数据，不需要进版本控制
- 排查问题时直接读文件即可

## 故障排查

```bash
# 查最近一次 portfolio-review 的结果
ls -t logs/scheduler/portfolio-review-*.json | head -1 | xargs cat | python -m json.tool

# 查所有失败的调度
for f in logs/scheduler/*.json; do
  python -c "import json,sys; d=json.load(open('$f',encoding='utf-8')); print('FAIL:', '$f') if not d.get('ok') else None"
done
```
