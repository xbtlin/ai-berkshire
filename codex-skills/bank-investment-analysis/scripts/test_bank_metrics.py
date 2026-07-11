#!/usr/bin/env python3

import csv
from decimal import Decimal
from pathlib import Path
import re
import unittest

import bank_metrics as bm
import render_data_appendix as rda


class BankMetricsTest(unittest.TestCase):
    def test_growth_and_single_period(self) -> None:
        self.assertEqual(bm.growth_rate("110", "100"), Decimal("10.0"))
        self.assertEqual(bm.single_period_from_cumulative("300", "190"), Decimal("110"))

    def test_nii_round_trip(self) -> None:
        nii = bm.nii_from_average_earning_assets("10000", "2.4", "3")
        self.assertEqual(nii, Decimal("60.00"))
        self.assertEqual(bm.infer_average_earning_assets(nii, "2.4", "3"), Decimal("10000"))
        self.assertEqual(bm.infer_annualized_nim(nii, "10000", "3"), Decimal("2.400"))
        self.assertEqual(
            bm.incremental_average_from_cumulative("110", "6", "100", "3"), Decimal("120")
        )
        self.assertEqual(
            bm.rounded_value_bounds("1.52", 2), (Decimal("1.515"), Decimal("1.525"))
        )

    def test_tax_credit_cost_and_rorwa(self) -> None:
        self.assertEqual(bm.effective_tax_rate("100", "85"), Decimal("15.00"))
        self.assertEqual(bm.annualized_credit_cost("25", "10000", "3"), Decimal("1.00"))
        self.assertEqual(bm.annualized_rorwa("25", "5000", "3"), Decimal("2.00"))

    def test_capital_and_asset_generation(self) -> None:
        self.assertEqual(bm.risk_asset_generation_ratio("6000", "10000"), Decimal("60.0"))
        self.assertEqual(bm.capital_required_for_rwa_growth("1000", "11"), Decimal("110"))

    def test_npl_bridge_and_reconciliation(self) -> None:
        self.assertEqual(bm.new_npl_balance("120", "100", "30", "5"), Decimal("45"))
        self.assertEqual(bm.reconcile_components("100", ["40", "35", "25"]), Decimal("0"))

    def test_balance_sheet_mix(self) -> None:
        result = bm.balance_sheet_mix(
            {"loans": "72", "investments": "48"},
            {"loans": "65", "investments": "35"},
            "120",
            "100",
        )
        self.assertEqual(result["loans"]["current_share_pct"], Decimal("60.0"))
        self.assertEqual(result["loans"]["share_change_pp"], Decimal("-5.00"))
        self.assertEqual(
            result["investments"]["contribution_to_total_change_pct"], Decimal("65.00")
        )
        with self.assertRaises(ValueError):
            bm.balance_sheet_mix({"loans": "1"}, {"investments": "1"}, "1", "1")

    def test_npl_stock_bridge_with_residual(self) -> None:
        result = bm.npl_stock_bridge(
            opening_npl="682.06",
            new_npl="189.27",
            cash_recoveries="17.15",
            writeoffs="63.57",
            bulk_transfers_and_abs="83.36",
            other_disposals="7.84",
            reported_closing_npl="698.58",
        )
        self.assertEqual(result["calculated_closing_npl"], Decimal("699.41"))
        self.assertEqual(result["residual"], Decimal("-0.83"))

    def test_provision_rollforward_and_writeoff_range(self) -> None:
        bridge = bm.provision_rollforward(
            "1000", "100", "20", writeoffs_and_transfers_out="80", reported_closing_provision="1040"
        )
        self.assertEqual(bridge["calculated_closing_provision"], Decimal("1040"))
        self.assertEqual(bridge["residual"], Decimal("0"))
        estimated = bm.estimate_writeoff_range(
            "1000", "1040", "90", "110", recovery_low="10", recovery_high="20"
        )
        self.assertEqual(estimated, {"low": Decimal("60"), "midpoint": Decimal("75"), "high": Decimal("90")})
        proxy = bm.npl_generation_proxy("120", "100", estimated["low"], estimated["high"])
        self.assertEqual(
            proxy,
            {
                "low": Decimal("80"),
                "midpoint": Decimal("95"),
                "high": Decimal("110"),
                "raw_low": Decimal("80"),
                "raw_high": Decimal("110"),
            },
        )
        proxy_with_transfer = bm.npl_generation_proxy(
            "90", "100", "0", "20", transfers_in_low="5", transfers_in_high="15"
        )
        self.assertEqual(proxy_with_transfer["low"], Decimal("0"))
        self.assertEqual(proxy_with_transfer["high"], Decimal("5"))
        self.assertEqual(proxy_with_transfer["raw_low"], Decimal("-25"))
        with self.assertRaises(ValueError):
            bm.estimate_writeoff_range("1000", "1040", "110", "90")

    def test_confidence_grade(self) -> None:
        self.assertEqual(bm.confidence_grade("disclosed"), "A")
        self.assertEqual(bm.confidence_grade("calculated", residual="1", reference_amount="100"), "B")
        self.assertEqual(
            bm.confidence_grade(
                "estimated", assumption_count=2, residual="4", reference_amount="100"
            ),
            "C",
        )
        self.assertEqual(
            bm.confidence_grade(
                "estimated", assumption_count=2, residual="6", reference_amount="100"
            ),
            "D",
        )
        self.assertEqual(bm.confidence_grade("proxy"), "D")
        self.assertEqual(bm.confidence_grade("N/A"), "N/A")

    def test_fundamental_scorecard(self) -> None:
        weights = {
            "profit": "20",
            "alm": "20",
            "risk": "30",
            "capital": "15",
            "franchise": "10",
            "governance": "5",
        }
        items = {
            name: {"weight": weight, "raw_score": "4", "confidence": "A"}
            for name, weight in weights.items()
        }
        result = bm.fundamental_scorecard(items)
        self.assertEqual(result["score"], Decimal("80.0"))
        self.assertEqual(result["score_range"], (Decimal("80.0"), Decimal("80.0")))
        self.assertFalse(result["provisional"])
        self.assertTrue(result["publishable"])

        items["risk"] = {"weight": "30", "raw_score": "4", "confidence": "C"}
        provisional = bm.fundamental_scorecard(items)
        self.assertIsNone(provisional["score"])
        self.assertEqual(provisional["score_range"], (Decimal("74.0"), Decimal("86.0")))
        self.assertEqual(provisional["uncertain_weight"], Decimal("30"))
        self.assertTrue(provisional["provisional"])
        self.assertEqual(provisional["published_score_range"], provisional["score_range"])

    def test_scorecard_accepts_26_subitems(self) -> None:
        weights = [4, 4, 3, 3, 6, 5, 5, 4, 4, 2, 6, 7, 6, 4, 5, 2, 5, 4, 3, 3, 4, 3, 3, 2, 1, 2]
        items = {
            f"item_{index}": {"weight": weight, "raw_score": "3", "confidence": "A"}
            for index, weight in enumerate(weights, start=1)
        }
        result = bm.fundamental_scorecard(items)
        self.assertEqual(result["score"], Decimal("60.0"))
        self.assertEqual(len(result["breakdown"]), 26)

        missing_items = {
            f"item_{index}": {"weight": weight, "raw_score": None, "confidence": "N/A"}
            for index, weight in enumerate(weights, start=1)
        }
        missing_result = bm.fundamental_scorecard(missing_items)
        self.assertFalse(missing_result["publishable"])
        self.assertIsNone(missing_result["published_score_range"])
        self.assertEqual(missing_result["na_weight"], Decimal("100"))

    def test_scorecard_rejects_bad_weights_and_scores(self) -> None:
        with self.assertRaises(ValueError):
            bm.fundamental_scorecard(
                {"only": {"weight": "99", "raw_score": "3", "confidence": "A"}}
            )
        with self.assertRaises(ValueError):
            bm.fundamental_scorecard(
                {"only": {"weight": "100", "raw_score": "6", "confidence": "A"}}
            )

    def test_interval_validation(self) -> None:
        self.assertEqual(bm.validate_interval("1", "-1", "3"), [])
        self.assertIn("center lies outside interval", bm.validate_interval("4", "-1", "3"))
        self.assertIn("lower boundary exceeds upper boundary", bm.validate_interval("1", "3", "-1"))
        with self.assertRaises(ValueError):
            bm.scenario_midpoint("3", "-1")

    def test_complete_profit_bridge(self) -> None:
        result = bm.bank_profit_bridge(
            "100", "20", "10", "2", "30", "15", "1", "4", "1", "12", "-1"
        )
        self.assertEqual(result["revenue"], Decimal("130"))
        self.assertEqual(result["pre_tax_profit"], Decimal("79"))
        self.assertEqual(result["net_profit"], Decimal("67"))
        self.assertEqual(result["attributable_profit"], Decimal("68"))

        reversal = bm.bank_profit_bridge(
            "100", "20", "10", "2", "30", "15", "-1", "4", "1", "12", "0"
        )
        self.assertEqual(reversal["pre_tax_profit"], Decimal("81"))

    def test_internal_earnings_review_metric_contract(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]
        csv_path = skill_root / "assets" / "earnings-review-data-template.csv"
        with csv_path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(
            list(rows[0]),
            [
                "section",
                "metric",
                "value",
                "unit",
                "period",
                "comparison_period",
                "scope",
                "balance_type",
                "status",
                "confidence",
                "source_file",
                "page_note",
                "formula",
                "assumptions",
                "residual",
                "comment",
            ],
        )
        metrics = [row["metric"] for row in rows]
        self.assertEqual(len(metrics), len(set(metrics)))
        self.assertGreaterEqual(len(metrics), 140)
        self.assertEqual(sum(metric.startswith("评分-") for metric in metrics), 26)
        required = {
            "总资产",
            "公司贷款",
            "客户存款",
            "新生成不良",
            "不良处置合计",
            "不良余额核对差额",
            "估算核销与转出",
            "贷款减值准备核对差额",
            "RWA",
            "基本面总分",
        }
        self.assertFalse(required.difference(metrics))

        completed_rows = []
        for row in rows:
            completed = dict(row)
            completed.update(
                {
                    "period": "2026Q1",
                    "status": "N/A",
                    "confidence": "N/A",
                    "comment": "官方季报未披露；不影响核心结论。",
                }
            )
            completed_rows.append(completed)
        completed_rows[0].update(
            {
                "value": "123.45",
                "unit": "亿元",
                "comparison_period": "2025Q1",
                "scope": "集团",
                "balance_type": "累计",
                "status": "disclosed",
                "confidence": "A",
                "source_file": "某银行2026年一季报.pdf",
                "page_note": "第8页",
                "formula": "报告直接披露",
                "assumptions": "无",
                "residual": "0",
                "comment": "测试记录",
            }
        )
        rda.validate_rows(completed_rows, metrics)
        rendered = rda.render_appendix(completed_rows)
        self.assertEqual(rendered.count("| D"), 144)
        self.assertEqual(rendered.count("D001"), 1)
        self.assertEqual(rendered.count("D144"), 1)
        self.assertNotIn("### A.1", rendered)
        self.assertNotIn("### A.2", rendered)
        self.assertIn(
            "| 编号 | 分析模块·指标 | 数值·单位 | 数据期间·对比期 | 范围·统计口径 | 数据性质·可靠程度 | 证据文件·页码 | 计算方法·假设·限制 |",
            rendered,
        )
        packed_cells = rda.compact_record(completed_rows[0], 1)
        packed = "\n".join(packed_cells)
        self.assertEqual(rda.recover_compact_record(packed_cells), completed_rows[0])
        for field in rda.FIELDS:
            self.assertIn(f"{rda.FIELD_LABELS[field]}：", packed)
        self.assertIn("数据性质：财报直接披露", packed)
        self.assertIn("可靠程度：高（A级）", packed)
        self.assertNotIn("status:", rendered)
        self.assertNotIn("confidence:", rendered)
        self.assertNotIn("source_file:", rendered)
        self.assertIn("NIM（净息差）", rendered)
        self.assertIn("RWA（风险加权资产）", rendered)
        self.assertIn("财报基本面评分（score）", rendered)

        extension = dict(completed_rows[0])
        extension.update(
            {
                "section": "loans",
                "metric": "贷款平均余额",
                "value": "72634.98",
                "unit": "亿元",
                "balance_type": "日均",
                "page_note": "第5页",
                "comment": "可选量价扩展记录",
            }
        )
        extended_rows = [*completed_rows, extension]
        rda.validate_rows(extended_rows, metrics)
        extended_rendered = rda.render_appendix(extended_rows)
        self.assertEqual(extended_rendered.count("| D"), 144)
        self.assertEqual(extended_rendered.count("| E"), 1)
        self.assertEqual(extended_rendered.count("E001"), 1)
        self.assertIn("核心144项 + 扩展1项", extended_rendered)
        self.assertIn("补充披露及计算明细", extended_rendered)
        extension_cells = rda.compact_record(extension, 145)
        self.assertEqual(extension_cells[0], "E001")
        self.assertEqual(rda.recover_compact_record(extension_cells), extension)

        duplicate_extension = dict(extension)
        with self.assertRaises(ValueError):
            rda.validate_rows([*extended_rows, duplicate_extension], metrics)

        completed_rows[1]["comment"] = ""
        with self.assertRaises(ValueError):
            rda.validate_rows(completed_rows, metrics)

    def test_earnings_review_markdown_contract(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]
        template = (skill_root / "assets" / "earnings-review-template.md").read_text(
            encoding="utf-8"
        )
        required_sections = [
            "## 2. 资产结构",
            "## 3. 贷款结构",
            "## 4. 负债与存款结构",
            "## 7. 风险存量与前瞻信号",
            "## 8. 不良贷款余额变化及核对",
            "## 9. 贷款减值准备余额变化及核对",
            "## 10. 资本与增长质量",
            "## 13. 财报基本面评分（试行）",
            "## 15. 数据完整度与可信度",
            "## 附录A：可追溯数据底稿",
        ]
        for section in required_sections:
            self.assertIn(section, template)
        required_subsections = [
            "### 3.1 贷款量价总览",
            "### 3.2 贷款产品结构与风险",
            "### 4.2 付息负债量价",
            "### 4.3 存款细分量价（最近完整披露期）",
            "### 6.1 手续费及佣金",
            "### 6.2 其他非息收入",
            "### 6.3 费用与减值",
        ]
        for subsection in required_subsections:
            self.assertIn(subsection, template)
        self.assertEqual(template.count("pie showData"), 4)
        self.assertEqual(template.count("theme: base"), 4)
        self.assertEqual(template.count("background: '#F7FAFC'"), 4)
        self.assertEqual(template.count("pieStrokeColor: '#FFFFFF'"), 4)
        self.assertEqual(template.count("pieOpacity: 0.96"), 4)
        for color in ["#0B3B60", "#168AAD", "#2A9D8F", "#E9A23B", "#C44536"]:
            self.assertIn(color, template)
        for deposit_row in [
            "公司活期",
            "公司定期",
            "公司存款小计",
            "零售活期",
            "零售定期",
            "零售存款小计",
            "活期存款合计",
            "定期存款合计",
        ]:
            self.assertIn(f"| {deposit_row} |", template)
        loan_product_section = template.split("### 3.2 贷款产品结构与风险", 1)[1].split(
            "### 行业、区域和集中度（年报/中报）", 1
        )[0]
        loan_product_header = next(
            line for line in loan_product_section.splitlines() if line.startswith("| 类别")
        )
        self.assertNotIn("收益率", loan_product_header)

        appendix_columns = [
            "编号",
            "分析模块·指标",
            "数值·单位",
            "数据期间·对比期",
            "范围·统计口径",
            "数据性质·可靠程度",
            "证据文件·页码",
            "计算方法·假设·限制",
        ]
        for column in appendix_columns:
            self.assertIn(column, template)
        self.assertLess(
            template.index("## 15. 数据完整度与可信度"),
            template.index("## 附录A：可追溯数据底稿"),
        )
        self.assertNotIn("## 0. 数据完整度", template)
        self.assertNotIn("与此前预测或指引对比", template)
        self.assertNotIn("### A.1", template)
        self.assertNotIn("### A.2", template)
        for line in template.splitlines():
            if line.startswith("#"):
                self.assertNotIn("桥", line)
            if line.startswith("|"):
                self.assertLessEqual(line.count("|") - 1, 8, line)
        display_terms = {
            "QoQ": "环比",
            "YoY": "同比",
            "NIM": "净息差",
            "NII": "净利息收入",
            "RWA": "风险加权资产",
            "CET1": "核心一级资本",
            "RORWA": "风险加权资产收益率",
            "AUM": "管理客户总资产",
            "LCR": "流动性覆盖率",
            "NSFR": "净稳定资金比例",
            "ABS": "资产证券化",
            "OCI": "其他综合收益",
        }
        for term, meaning in display_terms.items():
            self.assertIn(f"{term}（{meaning}）", template)
            bare = re.compile(
                rf"(?<![A-Za-z]){re.escape(term)}(?![A-Za-z]|（{re.escape(meaning)}）)"
            )
            self.assertIsNone(bare.search(template), f"bare reader-facing term: {term}")
        self.assertIn("### 13.1 评分结果摘要", template)
        self.assertIn("评分发布状态", template)
        self.assertIn("证据充分度", template)
        self.assertIn("它不是第二份财报正文", template)
        self.assertIn("数据性质：", template)
        self.assertIn("可靠程度：", template)
        self.assertNotIn("status:", template)
        self.assertNotIn("confidence:", template)
        self.assertNotIn("source_file:", template)
        self.assertNotIn("数据附件", template)

    def test_single_markdown_delivery_contract(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]
        skill_text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
        agent_text = (skill_root / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("只交付一个 Markdown 文件", skill_text)
        self.assertIn("不保留独立CSV", skill_text)
        self.assertIn("E001", skill_text)
        self.assertIn("Mermaid", skill_text)
        self.assertIn("不产生外部图片附件", skill_text)
        self.assertIn("report-visual-design.md", skill_text)
        self.assertIn("存款细分", skill_text)
        self.assertIn("单一 Markdown 报告", agent_text)
        self.assertNotIn("Markdown 与 CSV 文件", agent_text)


if __name__ == "__main__":
    unittest.main()
