#!/usr/bin/env python3
"""Check report transcriptions and calculations; does not verify source truth."""
import contextlib
from decimal import Decimal, getcontext
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ROOT = HERE.parents[2]
REPORT = PROJECT / "持械入宋研究报告-20261101.md"
EVIDENCE = PROJECT / "evidence.json"
getcontext().prec = 40


def save(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def clean_log(value):
    plain = re.sub(r"\x1b\[[0-9;]*m", "", value)
    return "\n".join(line.rstrip() for line in plain.splitlines()).rstrip() + "\n"


def main():
    report = REPORT.read_text()
    evidence = json.loads(EVIDENCE.read_text())
    extraction = subprocess.run(
        ["python3", str(ROOT / "tools/report_audit.py"), "extract", "--report", str(REPORT),
         "--ratio", "1", "--seed", "20261101"],
        check=True, capture_output=True, text=True,
    )
    (HERE / "report-audit-extract.txt").write_text(clean_log(extraction.stdout.replace(str(ROOT) + "/", "")))
    spec = importlib.util.spec_from_file_location("report_audit", ROOT / "tools/report_audit.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    points = module.extract_data_points(report)
    source_rows = {r["date"]: r for r in evidence["season10_series"]["rows"]}
    results, exclusions = [], []
    for point in points:
        label = point["label"]
        if "其他常见工具" in label:
            reason = "n8n工具名称中的8，不是业务数据"
        elif "最近更新时间" in label:
            reason = "17:03时间被误识别为数值3"
        elif label == "表中关联线索的出处需要逐条保留":
            reason = "2月是来源日期，不是业务指标"
        else:
            reason = None
        if reason:
            exclusions.append({**point, "reason": reason})
            continue
        date = label.split(" · ")[0]
        if "热播指数，单位" in label or "该站记录的名次" in label:
            value = source_rows[date]["heat" if "热播指数" in label else "rank"]
            url = evidence["season10_series"]["url"]
            grade = "C：第三方表格转录一致性；非平台原始值审计"
        elif "数据到底有多大" in label or date == "2026-10-08":
            value, url, grade = 40, evidence["observations"][0]["url"], "A：制作方海报声称超过此阈值"
        elif date == "2026-10-18":
            value, url, grade = 8200, evidence["observations"][3]["url"], "A：制作方标题声称超过此阈值"
        elif date == "2026-10-28":
            value, url, grade = 10, evidence["observations"][4]["url"], "B：报道中的已播季数"
        elif date == "2026-11-01检索":
            value, url, grade = 44.6, evidence["observations"][6]["url"], "A：账号主页显示值"
        else:
            raise ValueError(f"Unclassified extracted number: {point}")
        assert Decimal(str(point["reported_value"])) == Decimal(str(value)), point
        results.append({**point, "fetched_value": value, "fetched_source": url,
                        "validation_scope": grade,
                        "second_independent_measurement": False})
    save("numeric-results.json", results)
    save("extraction-exclusions.json", exclusions)
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        verdict = module.render_verdict(results, report_name=REPORT.name)
    (HERE / "report-audit-verdict.txt").write_text(clean_log(capture.getvalue()))
    assert verdict["verdict"] == "PASS"
    save("verdict.json", {**verdict, "scope": "仅检查报告与所录公开来源的数字一致性；不审计来源真实性、不验证技术栈"})

    formulae = [
        "60 / 5 * 2 * 3",
        "60 / 5 * 2 * (0.8 * 3 + 0.2 * 10)",
        "60 / 5 * 2 * (0.6 * 3 + 0.4 * 20)",
        "(5610 / 7921 - 1) * 100",
    ]
    calc_output = []
    for expression in formulae:
        out = subprocess.run(["python3", str(ROOT / "tools/financial_rigor.py"),
                              "calc", "--expr", expression], check=True,
                             capture_output=True, text=True)
        calc_output.append(out.stdout)
    (HERE / "financial-rigor-calculations.txt").write_text(clean_log("\n".join(calc_output)))
    decimal_checks = []
    settings = evidence["illustrative_scenarios"]
    for row in settings["scenarios"]:
        mean = (Decimal(row["ordinary_share"]) * Decimal(row["ordinary_attempts"])
                + Decimal(row["complex_share"]) * Decimal(row["complex_attempts"]))
        cost = Decimal(60) / Decimal(settings["shot_seconds"]) * Decimal(settings["price_per_attempt_yuan"]) * mean
        assert mean == Decimal(row["expected_mean_attempts"])
        assert cost == Decimal(row["expected_yuan_per_minute"])
        assert row["expected_yuan_per_minute"] in report
        decimal_checks.append({"scenario": row["id"], "mean_attempts": str(mean), "cost_yuan_per_minute": str(cost)})
    heat_change = (Decimal(5610) / Decimal(7921) - 1) * 100
    assert heat_change.quantize(Decimal("0.01")) == Decimal("-29.18")
    assert "下降29.18%" in report
    save("decimal-calculations.json", {"scenarios": decimal_checks, "heat_change_percent": str(heat_change),
                                     "rounded_percent": "-29.18", "status": "PASS"})
    # Explicitly cover meaningful figures the general financial extractor misses.
    manual_checks = ["系列累计收藏620万", "第一季收藏突破200万", "红果收藏1098万",
                     "获赞486.4万", "约170.3万字", "99集", "2小时41分钟",
                     "全团队30余人", "本剧核心10人", "5名编导", "2名剪辑", "1名总导演",
                     "累计算力投入超过100万元", "商业回报约千万元"]
    for phrase in manual_checks:
        assert phrase in report, phrase
    save("manual-scope.json", {
        "manually_reviewed_phrases": manual_checks,
        "basis": "见evidence.json逐项来源；短语存在检查只是防止编辑遗失，来源复核由研究者人工完成",
        "financial_claims_status": "保留主创自述，独立核验缺失，不做利润与回报率估算",
        "technical_claims_status": "实际模型、harness、供应商清单均未认定",
        "season11_status": "未确认上架，不作已播事实",
    })
    save("audit-summary.json", {"date": "2026-11-01", "extracted_count": len(points),
         "checked_transcriptions": len(results), "excluded_false_positives": len(exclusions),
         "manually_reviewed_additional_phrases": len(manual_checks),
         "report_sha256": hashlib.sha256(REPORT.read_bytes()).hexdigest(),
         "evidence_sha256": hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),
         "decision": "可以作为明确保留证据缺口的公开资料调研发布；非技术栈或财务认证"})
    print(f"PASS: {len(results)} numeric transcriptions; {len(exclusions)} extraction false positives excluded; Decimal checks passed.")


if __name__ == "__main__":
    main()
