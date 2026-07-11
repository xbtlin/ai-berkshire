#!/usr/bin/env python3
"""Mine method-bearing paragraphs from the normalized expert corpus."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


TOPICS: dict[str, re.Pattern[str]] = {
    "net_interest_income": re.compile(r"净利息收入|利息净收入|生息资产.*净息差|净息差.*生息资产"),
    "asset_scale": re.compile(r"资产规模|规模增速|总资产增速|生息资产|资产负债表.*扩张|扩表"),
    "asset_yield_and_funding_cost": re.compile(r"资产收益率|贷款收益率|负债成本|存款成本|同业负债|付息负债"),
    "repricing_and_nim": re.compile(r"重定价|LPR|净息差|利率下调|存款利率|定期存款.*到期"),
    "fee_income": re.compile(r"手续费|佣金收入|银行卡|财富管理|代理业务|托管|理财手续费"),
    "other_noninterest_income": re.compile(r"其他非息|其它非息|投资收益|公允价值变动|汇兑|贵金属|交易性金融资产"),
    "operating_expense": re.compile(r"营运费用|业务及管理费|成本收入比|员工费用|营运开支"),
    "impairment_and_asset_quality": re.compile(r"信用减值|减值损失|不良生成|新生成不良|核销|拨备|关注类|逾期|资产质量"),
    "tax_and_net_profit": re.compile(r"所得税率|实际税率|利润总额|归母净利润|净利润增速"),
    "capital_and_rorwa": re.compile(r"RORWA|风险加权资产|资本充足率|内生增长|资本消耗|核心一级资本"),
    "accounting_and_disclosure": re.compile(r"会计准则|重分类|披露口径|信披|并表|保险业务|财务附录|附注"),
    "single_quarter_reconstruction": re.compile(r"单季|单季度|环比|累计.*还原|年化后除以|倒算|回测"),
    "peer_comparison": re.compile(r"横向对比|同业|可比银行|四大行|股份行|城商行|排名"),
    "money_credit_data": re.compile(r"M1|M2|社融|人民币贷款|金融数据|信贷增量|政府债"),
    "policy_language": re.compile(r"央行.*表述|政策.*措辞|删除|新增.*表述|货币执行报告|政治局会议|工作会议"),
    "macro_bank_transmission": re.compile(r"货币政策|流动性|降息|降准|资产荒|信用扩张|经济复苏|银行基本面"),
    "forecast_scenarios": re.compile(r"中性值|乐观|悲观|高概率区间|上下限|预测区间|±|正负"),
    "forecast_error_and_correction": re.compile(r"预测偏|评估偏|高估|低估|修正|错误认知|预判.*错误|没想到"),
    "writing_and_conclusion": re.compile(r"点评:|结论|综上|总体来看|总的来看|需要注意|核心问题|最重要"),
}


METHOD_CUES = re.compile(
    r"取决于|主要原因|主要是|计算|公式|方法是|可以通过|需要.*考虑|应该.*剔除|"
    r"评估|预测|推测|还原|倒算|对比|验证|意味着|说明|所以|因此|如果.*那么|"
    r"关键是|本质是|规律|适用于|不适用|高估|低估|修正"
)


def load_jsonl(path: Path) -> list[dict[str, object]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def split_paragraphs(text: str) -> list[str]:
    paragraphs = [re.sub(r"\s+", " ", part).strip() for part in re.split(r"\n\s*\n|\n", text)]
    return [paragraph for paragraph in paragraphs if 25 <= len(paragraph) <= 1200]


def evidence_score(text: str, emphasized: set[str]) -> int:
    score = 0
    if METHOD_CUES.search(text):
        score += 2
    if re.search(r"因为|由于|所以|因此|导致|带动|影响|贡献", text):
        score += 1
    if re.search(r"\d+(?:\.\d+)?%|\d+(?:\.\d+)?\s*(?:bps|BP|bp)|=|除以|乘以|同比|环比", text, re.IGNORECASE):
        score += 1
    if re.search(r"预测|评估|中性|乐观|悲观|区间", text):
        score += 1
    if any(fragment and (fragment in text or text in fragment) for fragment in emphasized):
        score += 2
    if re.search(r"个人认为|个人判断|个人猜测|大概率|可能", text):
        score += 1
    return score


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--articles", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--minimum-score", type=int, default=3)
    args = parser.parse_args()

    records = load_jsonl(args.articles.expanduser().resolve())
    evidence: list[dict[str, object]] = []
    seen: set[tuple[str, str, str]] = set()
    for record in records:
        if record.get("availability") != "full":
            continue
        paragraphs = split_paragraphs(str(record.get("body") or ""))
        emphasized = {re.sub(r"\s+", " ", str(item)).strip() for item in record.get("emphasized_passages") or []}
        for paragraph_index, paragraph in enumerate(paragraphs, start=1):
            topics = [topic for topic, pattern in TOPICS.items() if pattern.search(paragraph)]
            if not topics:
                continue
            score = evidence_score(paragraph, emphasized)
            if score < args.minimum_score:
                continue
            normalized_hash = hashlib.sha1(paragraph.encode("utf-8")).hexdigest()[:16]
            for topic in topics:
                dedupe_key = (str(record["article_id"]), topic, normalized_hash)
                if dedupe_key in seen:
                    continue
                seen.add(dedupe_key)
                evidence.append(
                    {
                        "evidence_id": f"{record['article_id']}-{paragraph_index}-{topic}",
                        "article_id": record["article_id"],
                        "title": record["title"],
                        "publish_date": record["publish_date"],
                        "source_path": record["source_path"],
                        "source_url": record["source_url"],
                        "banks": record.get("banks") or [],
                        "report_year": record.get("report_year") or "",
                        "report_period": record.get("report_period") or "",
                        "article_categories": record.get("categories") or [],
                        "paragraph_index": paragraph_index,
                        "topic": topic,
                        "method_score": score,
                        "text": paragraph,
                    }
                )

    evidence.sort(
        key=lambda item: (
            str(item["topic"]),
            -int(item["method_score"]),
            str(item["publish_date"]),
            str(item["title"]),
        )
    )
    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for item in evidence:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")

    topic_counts = Counter(str(item["topic"]) for item in evidence)
    article_counts = Counter(str(item["article_id"]) for item in evidence)
    summary = {
        "evidence_count": len(evidence),
        "source_article_count": len(article_counts),
        "topic_counts": dict(topic_counts),
        "minimum_score": args.minimum_score,
    }
    summary_path = args.summary.expanduser().resolve()
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
