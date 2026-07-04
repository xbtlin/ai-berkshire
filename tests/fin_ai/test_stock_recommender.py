"""stock_recommender 的 unit test。"""

import sys
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


def test_calc_dividend_yield_标准():
    """股息率 = TTM 每10股派息 ÷ 10 ÷ 当前价 × 100。"""
    # 每 10 股派 5 元，当前价 10 元 → 5%
    rate = calc_dividend_yield(dividend_per_10_ttm=5.0, price=10.0)
    assert abs(rate - 5.0) < 0.01


def test_calc_dividend_yield_零价格():
    """价格为 0 时返回 0（防除零）。"""
    assert calc_dividend_yield(dividend_per_10_ttm=5.0, price=0) == 0.0
