"""tools.scheduler.runner 的单元测试。

不真跑 claude —— 用 monkeypatch 替换 subprocess.run，测的是 runner 自身的
控制流（命令构造、log 写入、错误处理、队列操作），不是 claude CLI 行为。
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.scheduler.runner import (
    _build_command,
    run_skill_headless,
    pop_next_theme,
    mark_theme_done,
)


# ---------------------------------------------------------------------------
# _build_command
# ---------------------------------------------------------------------------

def test_build_command_无参数():
    """无 args 时仍能构造合法命令，含 /skill、--allowedTools、--output-format."""
    cmd = _build_command("portfolio-review", "")
    assert cmd[0] == "claude"
    prompt = cmd[cmd.index("-p") + 1]
    assert prompt == "/portfolio-review"
    assert "--allowedTools" in cmd
    assert "--output-format" in cmd


def test_build_command_带参数():
    """args 拼接到 slash command 后（用空格分隔）。"""
    cmd = _build_command("news-pulse", "拼多多 跌12%")
    prompt = cmd[cmd.index("-p") + 1]
    assert prompt == "/news-pulse 拼多多 跌12%"


def test_build_command_默认工具集():
    """默认 allowedTools 含 Read/Edit/Bash/WebSearch/WebFetch."""
    cmd = _build_command("portfolio-review", "")
    tools_str = cmd[cmd.index("--allowedTools") + 1]
    for tool in ("Read", "Edit", "Bash", "WebSearch", "WebFetch"):
        assert tool in tools_str, f"默认应含 {tool}"


def test_build_command_额外工具合并():
    """extra_allowed_tools 合并到默认工具集（去重）。"""
    cmd = _build_command("news-pulse", "",
                         extra_allowed_tools=["mcp__http-tools__http_request"])
    tools_str = cmd[cmd.index("--allowedTools") + 1]
    assert "mcp__http-tools__http_request" in tools_str
    # 默认工具不丢
    assert "Read" in tools_str


# ---------------------------------------------------------------------------
# pop_next_theme / mark_theme_done
# ---------------------------------------------------------------------------

def test_pop_next_theme_取头部(tmp_path):
    """从 queue 头部取主题，剩余保留。"""
    queue_file = tmp_path / "queue.json"
    queue_file.write_text(json.dumps({
        "queue": [
            {"theme": "AI算力", "added": "2026-07-05"},
            {"theme": "创新药", "added": "2026-07-05"},
        ],
        "history": [],
    }), encoding="utf-8")

    theme = pop_next_theme(queue_file)
    assert theme == "AI算力"


def test_pop_next_theme_空队列返回_None(tmp_path):
    """空队列返回 None，调用方应据此跳过。"""
    queue_file = tmp_path / "queue.json"
    queue_file.write_text(json.dumps({"queue": [], "history": []}),
                          encoding="utf-8")

    assert pop_next_theme(queue_file) is None


def test_pop_next_theme_文件不存在返回_None(tmp_path):
    """队列文件不存在时返回 None（视为空队列）。"""
    assert pop_next_theme(tmp_path / "nonexistent.json") is None


def test_mark_theme_done_移到_history(tmp_path):
    """theme 从 queue 移除，加到 history（含 report 路径 + completed 时间戳）。"""
    queue_file = tmp_path / "queue.json"
    queue_file.write_text(json.dumps({
        "queue": [
            {"theme": "AI算力", "added": "2026-07-05"},
            {"theme": "创新药", "added": "2026-07-05"},
        ],
        "history": [],
    }), encoding="utf-8")

    mark_theme_done(queue_file, "AI算力",
                    "reports/AI算力-funnel-20260705.md")
    data = json.loads(queue_file.read_text(encoding="utf-8"))
    assert len(data["queue"]) == 1
    assert data["queue"][0]["theme"] == "创新药"
    assert len(data["history"]) == 1
    h = data["history"][0]
    assert h["theme"] == "AI算力"
    assert h["report"] == "reports/AI算力-funnel-20260705.md"
    assert "completed" in h  # ISO 时间戳


def test_mark_theme_done_主题不在队列_抛_ValueError(tmp_path):
    """theme 不在 queue 里时抛 ValueError（防御：暴露 caller bug）。"""
    queue_file = tmp_path / "queue.json"
    queue_file.write_text(json.dumps({
        "queue": [{"theme": "AI算力", "added": "2026-07-05"}],
        "history": [],
    }), encoding="utf-8")

    try:
        mark_theme_done(queue_file, "不存在的主题", "reports/x.md")
    except ValueError:
        return
    raise AssertionError("应抛 ValueError")


# ---------------------------------------------------------------------------
# run_skill_headless
# ---------------------------------------------------------------------------

def test_run_skill_headless_dry_run_不调_subprocess(monkeypatch, tmp_path):
    """dry_run=True 时只返回命令、不调 subprocess、不写 log。"""
    called = {"count": 0}

    def _fake_run(*args, **kwargs):
        called["count"] += 1
        return None

    monkeypatch.setattr("subprocess.run", _fake_run)

    result = run_skill_headless(
        skill_name="portfolio-review",
        args="",
        log_dir=tmp_path,
        dry_run=True,
    )
    assert called["count"] == 0
    assert result["dry_run"] is True
    assert isinstance(result["command"], list)
    assert result["command"][0] == "claude"
    # 不写 log
    assert not list(tmp_path.glob("*.json"))


class _FakeCompletedProcess:
    """模拟 subprocess.CompletedProcess。"""

    def __init__(self, returncode, stdout, stderr):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def test_run_skill_headless_成功_写_log(monkeypatch, tmp_path):
    """subprocess 返回 0 时 ok=True，写 log 文件。"""

    def _fake_run(cmd, **kwargs):
        return _FakeCompletedProcess(
            returncode=0,
            stdout=json.dumps({"cost_usd": 0.05, "duration_ms": 12000}),
            stderr="",
        )

    monkeypatch.setattr("subprocess.run", _fake_run)

    result = run_skill_headless(
        skill_name="portfolio-review",
        args="我的持仓",
        log_dir=tmp_path,
    )
    assert result["ok"] is True
    assert result["exit_code"] == 0
    log_files = list(tmp_path.glob("portfolio-review-*.json"))
    assert len(log_files) == 1
    log_data = json.loads(log_files[0].read_text(encoding="utf-8"))
    assert log_data["skill"] == "portfolio-review"
    assert log_data["ok"] is True


def test_run_skill_headless_失败_写_error_log(monkeypatch, tmp_path):
    """subprocess 返回非零时 ok=False，log 含 stderr 便于排查。"""

    def _fake_run(cmd, **kwargs):
        return _FakeCompletedProcess(
            returncode=1,
            stdout="",
            stderr="skill not found: /nonexistent",
        )

    monkeypatch.setattr("subprocess.run", _fake_run)

    result = run_skill_headless(
        skill_name="nonexistent-skill",
        log_dir=tmp_path,
    )
    assert result["ok"] is False
    assert result["exit_code"] == 1
    log_files = list(tmp_path.glob("nonexistent-skill-*.json"))
    assert len(log_files) == 1
    log_data = json.loads(log_files[0].read_text(encoding="utf-8"))
    assert log_data["ok"] is False
    assert "skill not found" in log_data["stderr"]
