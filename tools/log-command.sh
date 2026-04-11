#!/bin/bash
# 记录用户指令到日志文件
# 由 user_prompt_submit hook 调用，stdin 接收用户输入

LOG_DIR="$HOME/ai-berkshire/logs"
LOG_FILE="$LOG_DIR/command-log.jsonl"
COUNTER_FILE="$LOG_DIR/.counter"

mkdir -p "$LOG_DIR"

# 读取用户输入
PROMPT=$(cat)

# 跳过空输入
[ -z "$PROMPT" ] && exit 0

# 时间戳精确到秒
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# 截取前200字符作为记录（避免超长输入）
PROMPT_SHORT=$(echo "$PROMPT" | head -c 200 | tr '\n' ' ' | tr '"' "'")

# 追加到日志（JSONL格式）
echo "{\"time\":\"$TIMESTAMP\",\"prompt\":\"$PROMPT_SHORT\"}" >> "$LOG_FILE"

# 计数器
if [ -f "$COUNTER_FILE" ]; then
    COUNT=$(cat "$COUNTER_FILE")
else
    COUNT=0
fi
COUNT=$((COUNT + 1))
echo "$COUNT" > "$COUNTER_FILE"

# 每10条输出提醒（hook stdout 会显示给 Claude）
if [ $((COUNT % 10)) -eq 0 ]; then
    TOTAL=$(wc -l < "$LOG_FILE" | tr -d ' ')
    echo "[指令日志] 已累计记录 ${TOTAL} 条指令。建议运行 /command-log 补充近期指令的背景摘要。"
fi
