#!/bin/bash
# Record user instructions to the log file
# Called by user_prompt_submit hook, stdin receives user input

LOG_DIR="$HOME/ai-berkshire/logs"
LOG_FILE="$LOG_DIR/command-log.jsonl"
COUNTER_FILE="$LOG_DIR/.counter"

mkdir -p "$LOG_DIR"

# Read user input
PROMPT=$(cat)

# Skip empty input
[ -z "$PROMPT" ] && exit 0

# Timestamp is accurate to seconds
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

#Truncate the first 200 characters as a record (avoid over-long input)
PROMPT_SHORT=$(echo "$PROMPT" | head -c 200 | tr '\n' ' ' | tr '"' "'")

#Append to log (JSONL format)
echo "{\"time\":\"$TIMESTAMP\",\"prompt\":\"$PROMPT_SHORT\"}" >> "$LOG_FILE"

# counter
if [ -f "$COUNTER_FILE" ]; then
    COUNT=$(cat "$COUNTER_FILE")
else
    COUNT=0
fi
COUNT=$((COUNT + 1))
echo "$COUNT" > "$COUNTER_FILE"

# Every 10 output reminders (hook stdout will be displayed to Claude)
if [ $((COUNT % 10)) -eq 0 ]; then
    TOTAL=$(wc -l < "$LOG_FILE" | tr -d ' ')
    echo "[Command log] A total of ${TOTAL} commands have been recorded. It is recommended to run /command-log to supplement the background summary of recent commands."
fi
