"""stock_recommender 的 unit test。"""

import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.stock_recommender import load_index_constituents


def test_load_index_constituents_returns_unique_codes():
    """加载成分股：返回去重后的代码列表，格式为 6 位字符串。"""
    codes = load_index_constituents()
    # 中证红利 + 上证 50 去重后总数应在 70-100 之间
    assert 70 <= len(codes) <= 100, f"实际数量: {len(codes)}"
    # 全部是 6 位数字
    assert all(len(c) == 6 and c.isdigit() for c in codes), "代码必须是 6 位数字"
    # 无重复
    assert len(codes) == len(set(codes)), "代码必须去重"
    # 应包含招行（必在两个指数里）
    assert "600036" in codes, "应包含招行"


from tools.stock_recommender import _qq_code, _parse_qq_quote


def test_qq_code_上海():
    """6 开头代码 → sh 前缀。"""
    assert _qq_code("600036") == "sh600036"


def test_qq_code_深圳():
    """0/3 开头代码 → sz 前缀。"""
    assert _qq_code("000001") == "sz000001"
    assert _qq_code("300750") == "sz300750"


def test_qq_code_去除后缀():
    """带 .SH/.SZ 后缀的代码也要能处理。"""
    assert _qq_code("600036.SH") == "sh600036"


def test_parse_qq_quote_标准格式():
    """能解析腾讯行情返回的 ~ 分隔字符串。"""
    # 简化的样本：50+ 字段，关键字段在固定位置
    raw = '"招商银行~600036~35.50~35.00~36.00~100000~50000~50000~"'
    raw += "~" * 50  # 填充到 50+ 字段
    d = _parse_qq_quote(raw)
    assert d["name"] == "招商银行"
    assert d["code"] == "600036"
    assert d["price"] == "35.50"


def test_parse_qq_quote_真实线上格式():
    """腾讯线上真实格式：fields[0]=市场标识，需要偏移 1。"""
    # 真实格式：1~招商银行~600036~36.83~35.00~...
    raw = '"1~招商银行~600036~36.83~35.00~'
    raw += "~" * 50 + '"'  # 填充到 50+ 字段并闭合引号
    d = _parse_qq_quote(raw)
    assert d["name"] == "招商银行"
    assert d["code"] == "600036"
    assert d["price"] == "36.83"
    assert d["prev_close"] == "35.00"


from tools.stock_recommender import extract_roe_history


def test_extract_roe_history_正常数据():
    """从东财 API 响应里抽出近 N 年 ROE（按日期降序）。"""
    api_response = {
        "result": {
            "data": [
                # 故意打乱顺序，验证 sort 逻辑
                {"REPORT_DATE": "2022-12-31T00:00:00", "ROEJQ": 14.2, "REPORT_TYPE": "年报"},
                {"REPORT_DATE": "2024-12-31T00:00:00", "ROEJQ": 16.5, "REPORT_TYPE": "年报"},
                {"REPORT_DATE": "2021-12-31T00:00:00", "ROEJQ": 13.9, "REPORT_TYPE": "年报"},
                {"REPORT_DATE": "2023-12-31T00:00:00", "ROEJQ": 15.8, "REPORT_TYPE": "年报"},
            ]
        }
    }
    roes = extract_roe_history(api_response, years=3)
    assert roes == [16.5, 15.8, 14.2]


def test_extract_roe_history_空数据():
    """API 返回空数据时返回空列表。"""
    assert extract_roe_history({"result": {"data": []}}, years=3) == []
    assert extract_roe_history({}, years=3) == []


from tools.stock_recommender import (
    extract_dividends_ttm,
    calc_dividend_yield,
)


def test_extract_dividends_ttm_近365天():
    """汇总近 365 天内所有"每10股派息"总额。"""
    today = "2026-07-04"
    api_response = {
        "result": {
            "data": [
                # 假设今天 2026-07-04
                {"EQUITY_REGISTRATION_DATE": "2026-06-15", "BEFORE_TAX_DIVIDEND": 3.0},  # 中期
                {"EQUITY_REGISTRATION_DATE": "2025-07-10", "BEFORE_TAX_DIVIDEND": 5.0},  # 上年年度（< 365 天）
                {"EQUITY_REGISTRATION_DATE": "2025-06-20", "BEFORE_TAX_DIVIDEND": 4.0},  # 超过 365 天，剔除
            ]
        }
    }
    total = extract_dividends_ttm(api_response, today=today)
    assert total == 8.0  # 3 + 5


def test_extract_dividends_ttm_空():
    assert extract_dividends_ttm({}, today="2026-07-04") == 0.0


def test_extract_dividends_ttm_过滤未来日期():
    """股权登记日 > today 的派息不计入 TTM（尚未实际派发）。

    场景：招行 2025 年报派息股权登记日 2026-07-09（today=2026-07-05，
    4 天后），不应计入；只算近 365 天内已派发的。
    """
    today = "2026-07-05"
    api_response = {
        "result": {
            "data": [
                {"EQUITY_REGISTRATION_DATE": "2025-07-10", "BEFORE_TAX_DIVIDEND": 20.0},   # ✅ 已派发
                {"EQUITY_REGISTRATION_DATE": "2026-01-15", "BEFORE_TAX_DIVIDEND": 10.13},  # ✅ 已派发
                {"EQUITY_REGISTRATION_DATE": "2026-07-09", "BEFORE_TAX_DIVIDEND": 10.03},  # ❌ 未来
            ]
        }
    }
    total = extract_dividends_ttm(api_response, today=today)
    assert abs(total - 30.13) < 0.01  # 20.0 + 10.13，不含未来


from tools.stock_recommender import _map_dividend_records


def test_map_dividend_records_过滤预披露():
    """ASSIGN_PROGRESS != '实施分配' 的记录被过滤（预披露/待审议等）。

    场景：东财返回 3 条记录，仅 1 条是「实施分配」，其余应剔除。
    """
    raw_records = [
        # 预披露：股权登记日/金额都未定
        {"EQUITY_RECORD_DATE": None, "PRETAX_BONUS_RMB": None,
         "ASSIGN_PROGRESS": "预披露"},
        # 实施分配：已实际派发
        {"EQUITY_RECORD_DATE": "2026-07-09 00:00:00", "PRETAX_BONUS_RMB": 10.03,
         "ASSIGN_PROGRESS": "实施分配"},
        # 待审议：跳过
        {"EQUITY_RECORD_DATE": "2026-08-15 00:00:00", "PRETAX_BONUS_RMB": 5.0,
         "ASSIGN_PROGRESS": "待审议"},
    ]
    mapped = _map_dividend_records(raw_records)
    assert len(mapped) == 1
    assert mapped[0]["EQUITY_REGISTRATION_DATE"] == "2026-07-09 00:00:00"
    assert mapped[0]["BEFORE_TAX_DIVIDEND"] == 10.03


def test_calc_dividend_yield_标准():
    """股息率 = TTM 每10股派息 ÷ 10 ÷ 当前价 × 100。"""
    # 每 10 股派 5 元，当前价 10 元 → 5%
    rate = calc_dividend_yield(dividend_per_10_ttm=5.0, price=10.0)
    assert abs(rate - 5.0) < 0.01


def test_calc_dividend_yield_零价格():
    """价格为 0 时返回 0（防除零）。"""
    assert calc_dividend_yield(dividend_per_10_ttm=5.0, price=0) == 0.0


from tools.stock_recommender import score_stable


def _fund(dividend_yield, pe, roe_history):
    """构造 score_stable 输入的工厂函数。"""
    return {
        "dividend_yield": dividend_yield,
        "pe": pe,
        "roe_history": roe_history,
    }


def test_score_stable_满分():
    """4 项全过 → 4 分。"""
    fund = _fund(dividend_yield=5.0, pe=10, roe_history=[14.0, 14.5, 13.8])
    result = score_stable(fund, min_dividend=4.0, max_pe=15.0, min_roe=12.0, max_roe_stddev=5.0)
    assert result["score"] == 4
    assert result["details"]["dividend_yield"] is True
    assert result["details"]["pe"] is True
    assert result["details"]["roe_mean"] is True
    assert result["details"]["roe_stable"] is True


def test_score_stable_股息率不达标():
    """股息率 3% < 4% → 该维 0 分。"""
    fund = _fund(dividend_yield=3.0, pe=10, roe_history=[14.0, 14.5, 13.8])
    result = score_stable(fund, min_dividend=4.0, max_pe=15.0, min_roe=12.0, max_roe_stddev=5.0)
    assert result["score"] == 3
    assert result["details"]["dividend_yield"] is False
    assert result["details"]["pe"] is True


def test_score_stable_PE过高():
    """PE 30 > 15 → 该维 0 分。"""
    fund = _fund(dividend_yield=5.0, pe=30, roe_history=[14.0, 14.5, 13.8])
    result = score_stable(fund, min_dividend=4.0, max_pe=15.0, min_roe=12.0, max_roe_stddev=5.0)
    assert result["score"] == 3
    assert result["details"]["pe"] is False


def test_score_stable_ROE低():
    """ROE 8% < 12% → 该维 0 分。"""
    fund = _fund(dividend_yield=5.0, pe=10, roe_history=[8.0, 8.5, 7.8])
    result = score_stable(fund, min_dividend=4.0, max_pe=15.0, min_roe=12.0, max_roe_stddev=5.0)
    assert result["score"] == 3
    assert result["details"]["roe_mean"] is False


def test_score_stable_ROE波动大():
    """ROE 序列 [8%, 15%, 22%]，stddev 7pp > 5pp → 稳定性 0 分。"""
    fund = _fund(dividend_yield=5.0, pe=10, roe_history=[8.0, 15.0, 22.0])
    result = score_stable(fund, min_dividend=4.0, max_pe=15.0, min_roe=12.0, max_roe_stddev=5.0)
    assert result["score"] == 3
    assert result["details"]["roe_stable"] is False


def test_score_stable_招行样本():
    """招行（股息 5.2%, PE 7, ROE 16%, stddev 0.8pp）→ 4 分。"""
    fund = _fund(dividend_yield=5.2, pe=7, roe_history=[16.0, 16.2, 15.8])
    result = score_stable(fund, min_dividend=4.0, max_pe=15.0, min_roe=12.0, max_roe_stddev=5.0)
    assert result["score"] == 4


def test_score_stable_茅台样本():
    """茅台（股息 1%, PE 30, ROE 30%, stddev 1.2pp）→ 股息 0 + PE 0 + ROE 1 + 稳定 1 = 2 分。"""
    fund = _fund(dividend_yield=1.0, pe=30, roe_history=[30.0, 30.5, 29.8])
    result = score_stable(fund, min_dividend=4.0, max_pe=15.0, min_roe=12.0, max_roe_stddev=5.0)
    assert result["score"] == 2
    assert result["details"]["dividend_yield"] is False
    assert result["details"]["pe"] is False
    assert result["details"]["roe_mean"] is True
    assert result["details"]["roe_stable"] is True


from tools.stock_recommender import sort_and_filter


def _scored(code, score, div_yield):
    """构造 sort_and_filter 输入的工厂。"""
    return {"code": code, "score": score, "dividend_yield": div_yield}


def test_sort_and_filter_按分数分组_同分组按股息率降序():
    items = [
        _scored("A", 4, 4.5),
        _scored("B", 4, 6.0),
        _scored("C", 3, 5.0),
        _scored("D", 4, 5.5),
        _scored("E", 2, 8.0),  # 被剔除
    ]
    strong, weak = sort_and_filter(items, min_score=3, top_n=5)
    # 强推荐（4 分），按股息率降序
    assert [x["code"] for x in strong] == ["B", "D", "A"]
    # 备选（3 分）
    assert [x["code"] for x in weak] == ["C"]


def test_sort_and_filter_top_n_截断():
    items = [
        _scored("A", 4, 6.0),
        _scored("B", 4, 5.5),
        _scored("C", 4, 5.0),
        _scored("D", 4, 4.5),
    ]
    strong, weak = sort_and_filter(items, min_score=4, top_n=2)
    assert len(strong) == 2
    assert [x["code"] for x in strong] == ["A", "B"]
    assert weak == []


from tools.stock_recommender import generate_report


def test_generate_report_含必要章节():
    """生成的 Markdown 含：标题 / 总结 / Top 推荐 / 备选 / fin_ai 观点层 / 方法论 / 数据来源。"""
    today = "2026-07-04"
    strong = [{
        "code": "600036", "name": "招商银行", "score": 4,
        "dividend_yield": 5.2, "pe": 7.0, "roe_mean": 16.0,
        "roe_history": [16.0, 16.2, 15.8],
    }]
    weak = [{
        "code": "601398", "name": "工商银行", "score": 3,
        "dividend_yield": 6.0, "pe": 5.5, "roe_mean": 12.5,
        "roe_history": [12.5, 12.8, 12.2],
    }]
    fin_ai_opinion = {"summary": "招行强烈推荐，工行警示不良贷款风险",
                      "warnings": {}, "ok": True, "error": ""}
    md = generate_report(
        today=today,
        strong=strong,
        weak=weak,
        fin_ai_opinion=fin_ai_opinion,
        scanned_count=80,
        thresholds={"min_dividend": 4.0, "max_pe": 15.0, "min_roe": 12.0, "max_roe_stddev": 5.0},
    )
    # 必须含的章节标题
    assert "# 稳定收益推荐" in md
    assert "## 总结" in md
    assert "## Top 推荐" in md
    assert "## 备选" in md
    assert "## fin_ai 观点层" in md
    assert "## 方法论" in md
    assert "## 数据来源" in md
    # 必须含的关键内容
    assert "2026-07-04" in md
    assert "招商银行" in md
    assert "工商银行" in md
    assert "扫描范围" in md  # 扫描数量


def test_generate_report_fin_ai_失败时含warning():
    """fin_ai 失败时报告顶部含 warning。"""
    fin_ai_opinion = {"summary": "", "warnings": {}, "ok": False,
                      "error": "配额不足（剩余 0/80）"}
    md = generate_report(
        today="2026-07-04", strong=[], weak=[],
        fin_ai_opinion=fin_ai_opinion, scanned_count=80,
        thresholds={"min_dividend": 4.0, "max_pe": 15.0, "min_roe": 12.0, "max_roe_stddev": 5.0},
    )
    assert "⚠️" in md or "warning" in md.lower() or "配额不足" in md


# ---------------------------------------------------------------------------
# run_stable 主流程：错误降级 / 短路 / 返回码
#
# 说明：spec §10 禁止 mock 外部 HTTP。这里用 monkeypatch 替换 run_stable 内部
# 调用的函数（load_index_constituents / fetch_quote / fetch_financials /
# fetch_dividends / ask_fin_ai_opinion），测的是 run_stable 自身的控制流
# （返回码、短路、降级、跳过），不是外部 API 行为。合规。
# ---------------------------------------------------------------------------

from tools.stock_recommender import run_stable


def test_run_stable_dry_run_prints_no_write(monkeypatch, capsys, tmp_path):
    """dry-run 模式仅打印不写文件。"""
    monkeypatch.setattr("tools.stock_recommender.load_index_constituents", lambda: ["600036"])
    monkeypatch.setattr("tools.stock_recommender.fetch_quote", lambda c: {"name": "招行", "code": c, "price": "36.0", "pe": "7.0"})
    monkeypatch.setattr("tools.stock_recommender.fetch_financials", lambda c, years=3: {"roe_history": [16.0, 16.2, 15.8]})
    monkeypatch.setattr("tools.stock_recommender.fetch_dividends", lambda c: {"dividend_per_10_ttm": 19.0, "raw_records": []})
    monkeypatch.setattr("tools.stock_recommender.ask_fin_ai_opinion", lambda cands: {"summary": "", "warnings": {}, "ok": True, "error": ""})
    monkeypatch.setattr("tools.stock_recommender.REPORTS_DIR", tmp_path)

    exit_code = run_stable(
        today="20260704", date_iso="2026-07-04",
        top_n=5, min_dividend=4.0, max_pe=15.0, min_roe=12.0, max_roe_stddev=5.0,
        dry_run=True, force=False,
    )
    assert exit_code == 0
    # dry-run 不写文件
    assert not (tmp_path / "stable-20260704.md").exists()
    # stdout 含报告内容
    captured = capsys.readouterr()
    assert "# 稳定收益推荐" in captured.out


def test_run_stable_writes_report_when_not_dry_run(monkeypatch, tmp_path):
    """非 dry-run 模式正常写报告。"""
    monkeypatch.setattr("tools.stock_recommender.load_index_constituents", lambda: ["600036"])
    monkeypatch.setattr("tools.stock_recommender.fetch_quote", lambda c: {"name": "招行", "code": c, "price": "36.0", "pe": "7.0"})
    monkeypatch.setattr("tools.stock_recommender.fetch_financials", lambda c, years=3: {"roe_history": [16.0, 16.2, 15.8]})
    monkeypatch.setattr("tools.stock_recommender.fetch_dividends", lambda c: {"dividend_per_10_ttm": 19.0, "raw_records": []})
    monkeypatch.setattr("tools.stock_recommender.ask_fin_ai_opinion", lambda cands: {"summary": "", "warnings": {}, "ok": True, "error": ""})
    monkeypatch.setattr("tools.stock_recommender.REPORTS_DIR", tmp_path)

    exit_code = run_stable(
        today="20260704", date_iso="2026-07-04",
        top_n=5, min_dividend=4.0, max_pe=15.0, min_roe=12.0, max_roe_stddev=5.0,
        dry_run=False, force=False,
    )
    assert exit_code == 0
    report = tmp_path / "stable-20260704.md"
    assert report.exists()
    content = report.read_text(encoding="utf-8")
    assert "招行" in content
    assert "## Top 推荐" in content


def test_run_stable_existing_no_force_returns_1(monkeypatch, tmp_path):
    """报告已存在且无 --force 时返回 1。"""
    monkeypatch.setattr("tools.stock_recommender.load_index_constituents", lambda: ["600036"])
    monkeypatch.setattr("tools.stock_recommender.fetch_quote", lambda c: {"name": "招行", "code": c, "price": "36.0", "pe": "7.0"})
    monkeypatch.setattr("tools.stock_recommender.fetch_financials", lambda c, years=3: {"roe_history": [16.0, 16.2, 15.8]})
    monkeypatch.setattr("tools.stock_recommender.fetch_dividends", lambda c: {"dividend_per_10_ttm": 19.0, "raw_records": []})
    monkeypatch.setattr("tools.stock_recommender.ask_fin_ai_opinion", lambda cands: {"summary": "", "warnings": {}, "ok": True, "error": ""})
    monkeypatch.setattr("tools.stock_recommender.REPORTS_DIR", tmp_path)

    # 预先创建一个文件
    (tmp_path / "stable-20260704.md").write_text("old content", encoding="utf-8")

    exit_code = run_stable(
        today="20260704", date_iso="2026-07-04",
        top_n=5, min_dividend=4.0, max_pe=15.0, min_roe=12.0, max_roe_stddev=5.0,
        dry_run=False, force=False,
    )
    assert exit_code == 1
    # 文件未被覆盖
    assert (tmp_path / "stable-20260704.md").read_text(encoding="utf-8") == "old content"


def test_run_stable_constituents_load_failure_returns_1(monkeypatch, capsys):
    """成分股加载失败时返回 1。"""
    def _raise():
        raise FileNotFoundError("找不到 index_constituents.json")
    monkeypatch.setattr("tools.stock_recommender.load_index_constituents", _raise)

    exit_code = run_stable(
        today="20260704", date_iso="2026-07-04",
        top_n=5, min_dividend=4.0, max_pe=15.0, min_roe=12.0, max_roe_stddev=5.0,
        dry_run=False, force=False,
    )
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "成分股加载失败" in captured.err


def test_run_stable_single_stock_failure_skipped(monkeypatch, capsys, tmp_path):
    """单股 fetch 失败时跳过，不影响其他股。"""
    monkeypatch.setattr("tools.stock_recommender.load_index_constituents", lambda: ["600036", "601398"])
    # 第一只股 fetch_quote 抛错，第二只正常
    def _fetch_quote(code):
        if code == "600036":
            raise ConnectionError("招行 fetch 失败")
        return {"name": "工行", "code": code, "price": "5.0", "pe": "5.5"}
    monkeypatch.setattr("tools.stock_recommender.fetch_quote", _fetch_quote)
    monkeypatch.setattr("tools.stock_recommender.fetch_financials", lambda c, years=3: {"roe_history": [12.5, 12.8, 12.2]})
    monkeypatch.setattr("tools.stock_recommender.fetch_dividends", lambda c: {"dividend_per_10_ttm": 3.0, "raw_records": []})
    monkeypatch.setattr("tools.stock_recommender.ask_fin_ai_opinion", lambda cands: {"summary": "", "warnings": {}, "ok": True, "error": ""})
    monkeypatch.setattr("tools.stock_recommender.REPORTS_DIR", tmp_path)

    exit_code = run_stable(
        today="20260704", date_iso="2026-07-04",
        top_n=5, min_dividend=4.0, max_pe=15.0, min_roe=12.0, max_roe_stddev=5.0,
        dry_run=False, force=False,
    )
    assert exit_code == 0
    captured = capsys.readouterr()
    # 第一只股跳过警告（含「跳过」或 ⚠️）
    assert "跳过" in captured.err or "⚠️" in captured.err
    # 报告生成（第二只股的工行可能进备选或剔除，但报告应存在）
    assert (tmp_path / "stable-20260704.md").exists()


def test_run_stable_fin_ai_failure_degrades(monkeypatch, tmp_path):
    """fin_ai 失败时降级，报告顶部含 warning。"""
    monkeypatch.setattr("tools.stock_recommender.load_index_constituents", lambda: ["600036"])
    monkeypatch.setattr("tools.stock_recommender.fetch_quote", lambda c: {"name": "招行", "code": c, "price": "36.0", "pe": "7.0"})
    monkeypatch.setattr("tools.stock_recommender.fetch_financials", lambda c, years=3: {"roe_history": [16.0, 16.2, 15.8]})
    monkeypatch.setattr("tools.stock_recommender.fetch_dividends", lambda c: {"dividend_per_10_ttm": 19.0, "raw_records": []})
    monkeypatch.setattr("tools.stock_recommender.ask_fin_ai_opinion", lambda cands: {
        "summary": "", "warnings": {}, "ok": False, "error": "fin_ai 配额不足（剩余 0/80）"
    })
    monkeypatch.setattr("tools.stock_recommender.REPORTS_DIR", tmp_path)

    exit_code = run_stable(
        today="20260704", date_iso="2026-07-04",
        top_n=5, min_dividend=4.0, max_pe=15.0, min_roe=12.0, max_roe_stddev=5.0,
        dry_run=False, force=False,
    )
    assert exit_code == 0  # fin_ai 失败不阻塞
    content = (tmp_path / "stable-20260704.md").read_text(encoding="utf-8")
    assert "⚠️" in content or "配额不足" in content
