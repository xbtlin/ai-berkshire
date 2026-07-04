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
