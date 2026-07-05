"""scheduler CLI 入口 — 调度任务的命令行接口。

用法：
    python -m tools.scheduler portfolio-review [--dry-run]
    python -m tools.scheduler industry-funnel --from-queue [--dry-run]
    python -m tools.scheduler news-pulse "拼多多 跌12%" [--dry-run]
    python -m tools.scheduler list-queue
    python -m tools.scheduler add-theme "AI算力"

设计：
- portfolio-review：固定输入"我的持仓"，从 reports/portfolio-latest.md 读
- industry-funnel：从 data/industry_funnel_queue.json 取头部主题，跑完弹出
- news-pulse：留接口（本期不绑定调度任务），需显式传 args
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

from tools.scheduler.runner import (
    REPO_ROOT,
    add_theme,
    mark_theme_done,
    pop_next_theme,
    run_skill_headless,
)

QUEUE_FILE = REPO_ROOT / "data" / "industry_funnel_queue.json"
REPORTS_DIR = REPO_ROOT / "reports"


def _emit(msg: str) -> None:
    """统一的 stderr 输出（stdout 留给 claude JSON）。"""
    print(msg, file=sys.stderr)


def cmd_portfolio_review(args) -> int:
    """周度任务：portfolio-review 我的持仓。"""
    _emit("[portfolio-review] 启动 Claude headless...")
    result = run_skill_headless(
        skill_name="portfolio-review",
        args="我的持仓",
        dry_run=args.dry_run,
    )
    return _report_result(result, args.dry_run)


def cmd_industry_funnel(args) -> int:
    """月度任务：industry-funnel --from-queue。"""
    if not args.from_queue:
        _emit("❌ industry-funnel 子命令必须配 --from-queue（本期不直接传主题）")
        return 2

    theme = pop_next_theme(QUEUE_FILE)
    if not theme:
        _emit(f"⚠️ 队列为空：{QUEUE_FILE}（用 `add-theme` 加主题）")
        return 0  # 空队列不算失败

    _emit(f"[industry-funnel] 取主题: {theme}")
    if args.dry_run:
        result = run_skill_headless(
            skill_name="industry-funnel",
            args=theme,
            dry_run=True,
        )
        return _report_result(result, True)

    result = run_skill_headless(
        skill_name="industry-funnel",
        args=theme,
    )
    if not result["ok"]:
        return _report_result(result, False)

    # 跑成功后，把 theme 移到 history（按命名规范猜报告路径）
    today = datetime.now().strftime("%Y%m%d")
    report_path = REPORTS_DIR / f"{theme}-funnel-{today}.md"
    try:
        mark_theme_done(QUEUE_FILE, theme, str(report_path.relative_to(REPO_ROOT)))
        _emit(f"✅ 已把 '{theme}' 移到 history（报告：{report_path}）")
    except ValueError as e:
        _emit(f"⚠️ mark_theme_done 失败: {e}")
    return _report_result(result, False)


def cmd_news_pulse(args) -> int:
    """通用接口：news-pulse 带显式参数（本期不绑定调度）。"""
    if not args.params:
        _emit("❌ news-pulse 需要参数，例如：python -m tools.scheduler news-pulse \"拼多多 跌12%\"")
        return 2
    result = run_skill_headless(
        skill_name="news-pulse",
        args=" ".join(args.params),
        dry_run=args.dry_run,
    )
    return _report_result(result, args.dry_run)


def cmd_list_queue(args) -> int:
    """查看主题队列。"""
    from tools.scheduler.runner import _load_queue
    data = _load_queue(QUEUE_FILE)
    _emit(f"📋 主题队列（{QUEUE_FILE}）")
    _emit("")
    if data["queue"]:
        _emit("待跑（顺序）：")
        for i, item in enumerate(data["queue"], 1):
            _emit(f"  {i}. {item['theme']}  (added {item.get('added', '-')})")
    else:
        _emit("（空）")
    _emit("")
    if data["history"]:
        _emit(f"已完成 {len(data['history'])} 个：")
        for item in data["history"][-5:]:  # 最近 5 个
            _emit(f"  - {item['theme']} → {item.get('report', '?')}  ({item.get('completed', '-')})")
    return 0


def cmd_add_theme(args) -> int:
    """加主题到队列尾部。"""
    if not args.params:
        _emit("❌ add-theme 需要主题参数")
        return 2
    theme = " ".join(args.params)
    add_theme(QUEUE_FILE, theme)
    _emit(f"✅ 已加主题：{theme}")
    return 0


def _report_result(result: dict, dry_run: bool) -> int:
    """统一的结果打印 + exit code 推导。"""
    if dry_run:
        _emit("[dry-run] 命令：")
        _emit("  " + " ".join(result["command"]))
        return 0
    if result["ok"]:
        _emit(f"✅ 成功（用时 {result['duration_sec']:.0f}s，log: {result['log_path']}）")
        return 0
    _emit(f"❌ 失败 exit={result['exit_code']}")
    _emit(f"   log: {result['log_path']}")
    if result["stderr"]:
        _emit(f"   stderr: {result['stderr'][:300]}")
    return result["exit_code"] if result["exit_code"] != 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="tools.scheduler",
        description="AI Berkshire 调度 Pipeline（Windows 任务计划程序 + Claude headless）",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_pr = sub.add_parser("portfolio-review",
                          help="周度任务：基于 reports/portfolio-latest.md 跑 portfolio-review")
    p_pr.add_argument("--dry-run", action="store_true", help="只打印命令、不调 claude")
    p_pr.set_defaults(func=cmd_portfolio_review)

    p_if = sub.add_parser("industry-funnel",
                          help="月度任务：从 data/industry_funnel_queue.json 取头部主题跑")
    p_if.add_argument("--from-queue", action="store_true",
                      help="从主题队列取（本期必填）")
    p_if.add_argument("--dry-run", action="store_true")
    p_if.set_defaults(func=cmd_industry_funnel)

    p_np = sub.add_parser("news-pulse",
                          help="通用接口：news-pulse 带显式参数（本期不绑定调度）")
    p_np.add_argument("params", nargs="*")
    p_np.add_argument("--dry-run", action="store_true")
    p_np.set_defaults(func=cmd_news_pulse)

    p_lq = sub.add_parser("list-queue", help="查看主题队列")
    p_lq.set_defaults(func=cmd_list_queue)

    p_at = sub.add_parser("add-theme", help="加主题到队列尾部")
    p_at.add_argument("params", nargs="*")
    p_at.set_defaults(func=cmd_add_theme)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
