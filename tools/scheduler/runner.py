"""scheduler.runner — Claude Code headless 模式 skill 调用器。

设计要点：
- 不加 --bare：保留 CLAUDE.md 项目指令（金融 Decimal / 中文报告风格 / Codex 同步）
- --allowedTools 显式授权（避免 headless 模式弹权限确认卡住）
- --output-format json：stdout 是结构化 JSON（含 cost_usd/duration_ms）
- log 写到 logs/scheduler/{skill}-{YYYYMMDD-HHMMSS}.json，不入 git
- dry_run 模式：只返回命令、不调 subprocess（便于 smoke）
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
LOG_DIR_DEFAULT = REPO_ROOT / "logs" / "scheduler"

# 默认工具集：覆盖 skill 常用动作（读写文件 + 跑命令 + 联网搜索）
DEFAULT_ALLOWED_TOOLS = [
    "Read", "Edit", "Write",
    "Bash",
    "WebSearch", "WebFetch",
]


def _build_command(
    skill_name: str,
    args: str = "",
    extra_allowed_tools: list = None,
    max_turns: int = 60,
) -> list:
    """构造 claude headless 命令参数列表。

    返回：["claude", "-p", "/skill args", "--allowedTools", "...", "--output-format", "json", "--max-turns", "60"]

    max_turns: 防 skill 跑飞（spike 时 portfolio-review 是 40 turn，留 50% buffer）。
              传 None 则不加 --max-turns（特殊场景：长跑 skill）。
    """
    args = (args or "").strip()
    prompt = f"/{skill_name} {args}".rstrip()
    tools = list(DEFAULT_ALLOWED_TOOLS)
    if extra_allowed_tools:
        for t in extra_allowed_tools:
            if t not in tools:
                tools.append(t)
    cmd = [
        "claude",
        "-p", prompt,
        "--allowedTools", ",".join(tools),
        "--output-format", "json",
    ]
    if max_turns is not None:
        cmd.extend(["--max-turns", str(max_turns)])
    return cmd


def run_skill_headless(
    skill_name: str,
    args: str = "",
    repo_root: Path = None,
    log_dir: Path = None,
    extra_allowed_tools: list = None,
    dry_run: bool = False,
    max_turns: int = 60,
    timeout_sec: int = 1800,
) -> dict:
    """调 claude -p '/{skill} {args}'，返回执行结果。

    返回 dict：
        dry_run=True 时：{dry_run: True, command: [...]}
        否则：{ok, exit_code, stdout, stderr, log_path, command, started_at, duration_sec, timed_out}

    加固（基于 2026-07-05 spike vs 任务计划程序事故诊断）：
    - max_turns=60：防 skill 跑飞（subprocess 死循环时硬上限）
    - timeout_sec=1800：subprocess.run 30 分钟硬上限（防 LLM 单次调用 + 多 turn 叠加卡死）
    - stdin=DEVNULL：防 headless claude 等待 stdin 阻塞

    失败时（exit_code != 0 / timeout）ok=False，但仍写 log 便于排查。
    """
    repo_root = repo_root or REPO_ROOT
    log_dir = log_dir or LOG_DIR_DEFAULT
    command = _build_command(skill_name, args, extra_allowed_tools, max_turns=max_turns)

    if dry_run:
        return {"dry_run": True, "command": command}

    log_dir.mkdir(parents=True, exist_ok=True)
    started_at = datetime.now()
    timestamp = started_at.strftime("%Y%m%d-%H%M%S")
    log_path = log_dir / f"{skill_name}-{timestamp}.json"

    timed_out = False
    try:
        completed = subprocess.run(
            command,
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdin=subprocess.DEVNULL,
            timeout=timeout_sec,
        )
        exit_code = completed.returncode
        stdout = completed.stdout or ""
        stderr = completed.stderr or ""
    except subprocess.TimeoutExpired as e:
        timed_out = True
        exit_code = -1
        stdout = (e.stdout or "") if isinstance(e.stdout, str) else ""
        stderr = f"timeout: subprocess 超过 {timeout_sec}s 未结束（命令：{e.cmd}）"
    except Exception as e:
        exit_code, stdout, stderr = -1, "", f"subprocess.run 异常: {e}"

    ended_at = datetime.now()
    duration_sec = (ended_at - started_at).total_seconds()

    log_data = {
        "skill": skill_name,
        "args": args,
        "command": command,
        "started_at": started_at.isoformat(timespec="seconds"),
        "ended_at": ended_at.isoformat(timespec="seconds"),
        "duration_sec": duration_sec,
        "exit_code": exit_code,
        "ok": exit_code == 0,
        "timed_out": timed_out,
        "stdout": stdout,
        "stderr": stderr,
    }
    log_path.write_text(
        json.dumps(log_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {
        "ok": exit_code == 0,
        "exit_code": exit_code,
        "stdout": stdout,
        "stderr": stderr,
        "log_path": log_path,
        "command": command,
        "started_at": log_data["started_at"],
        "duration_sec": duration_sec,
        "timed_out": timed_out,
    }


# ---------------------------------------------------------------------------
# industry-funnel 主题队列操作
# ---------------------------------------------------------------------------

def _load_queue(queue_file: Path) -> dict:
    """读队列文件，不存在或格式错时返回空骨架。"""
    if not queue_file.exists():
        return {"queue": [], "history": []}
    try:
        data = json.loads(queue_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"queue": [], "history": []}
    data.setdefault("queue", [])
    data.setdefault("history", [])
    return data


def _save_queue(queue_file: Path, data: dict) -> None:
    queue_file.parent.mkdir(parents=True, exist_ok=True)
    queue_file.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def pop_next_theme(queue_file: Path) -> str:
    """返回 queue 头部的 theme 字符串（不修改文件）。

    文件由调用方在 skill 跑完后通过 mark_theme_done() 更新。
    空队列或文件不存在时返回 None。
    """
    data = _load_queue(queue_file)
    if not data["queue"]:
        return None
    return data["queue"][0]["theme"]


def mark_theme_done(queue_file: Path, theme: str, report_path: str) -> None:
    """把 theme 从 queue 移到 history（含完成时间 + 报告路径）。

    theme 不在 queue 里时抛 ValueError（暴露 caller bug）。
    """
    data = _load_queue(queue_file)
    idx = next(
        (i for i, item in enumerate(data["queue"]) if item["theme"] == theme),
        None,
    )
    if idx is None:
        raise ValueError(f"theme 不在队列中: {theme}")

    item = data["queue"].pop(idx)
    item["report"] = report_path
    item["completed"] = datetime.now().isoformat(timespec="seconds")
    data["history"].append(item)
    _save_queue(queue_file, data)


def add_theme(queue_file: Path, theme: str) -> None:
    """加主题到队列尾部。已存在则跳过。"""
    data = _load_queue(queue_file)
    if any(item["theme"] == theme for item in data["queue"]):
        return
    data["queue"].append({
        "theme": theme,
        "added": datetime.now().strftime("%Y-%m-%d"),
    })
    _save_queue(queue_file, data)
