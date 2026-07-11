#!/usr/bin/env python3
"""Download a bounded selection of official bank-report PDFs with checksums."""

from __future__ import annotations

import argparse
import csv
import hashlib
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def valid_pdf(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < 1024:
        return False
    with path.open("rb") as handle:
        return handle.read(5) == b"%PDF-"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def destination_for(row: dict[str, str], output_dir: Path) -> Path:
    bank_dir = output_dir / row["bank"]
    bank_dir.mkdir(parents=True, exist_ok=True)
    return bank_dir / f"{row['report_year']}-{row['report_period']}-{row['a_code']}.pdf"


def download_one(row: dict[str, str], output_dir: Path, retries: int) -> dict[str, str]:
    destination = destination_for(row, output_dir)
    result = {
        "bank": row["bank"],
        "a_code": row["a_code"],
        "report_year": row["report_year"],
        "report_period": row["report_period"],
        "official_report_url": row["official_report_url"],
        "local_report_path": str(destination.resolve()),
        "selection_reasons": row.get("selection_reasons", ""),
        "expected_size_kb": row.get("announcement_size_kb", ""),
        "actual_bytes": "",
        "sha256": "",
        "status": "",
        "error": "",
    }
    if valid_pdf(destination):
        result["actual_bytes"] = str(destination.stat().st_size)
        result["sha256"] = sha256_file(destination)
        result["status"] = "existing"
        return result

    part_path = destination.with_suffix(destination.suffix + ".part")
    last_error = ""
    for attempt in range(1, retries + 1):
        try:
            request = urllib.request.Request(
                row["official_report_url"],
                headers={
                    "User-Agent": "Mozilla/5.0 (compatible; bank-research-corpus/1.0)",
                    "Referer": "https://www.cninfo.com.cn/",
                },
            )
            with urllib.request.urlopen(request, timeout=90) as response, part_path.open("wb") as handle:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    handle.write(chunk)
            if not valid_pdf(part_path):
                raise ValueError("downloaded payload is not a valid PDF")
            part_path.replace(destination)
            result["actual_bytes"] = str(destination.stat().st_size)
            result["sha256"] = sha256_file(destination)
            result["status"] = "downloaded"
            return result
        except Exception as exc:  # network endpoints can fail transiently
            last_error = f"attempt {attempt}: {type(exc).__name__}: {exc}"
            if part_path.exists():
                part_path.unlink()
            if attempt < retries:
                time.sleep(attempt)
    result["status"] = "error"
    result["error"] = last_error
    return result


def write_manifest(results: list[dict[str, str]], path: Path) -> None:
    fields = list(results[0]) if results else []
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(sorted(results, key=lambda row: (row["bank"], row["report_year"], row["report_period"])))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selection", type=Path, required=True, help="CSV from select_report_sample.py")
    parser.add_argument("--output-dir", type=Path, required=True, help="PDF root directory")
    parser.add_argument("--manifest", type=Path, required=True, help="Download manifest CSV")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--retries", type=int, default=3)
    args = parser.parse_args()

    rows = load_rows(args.selection.expanduser().resolve())
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, str]] = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {
            executor.submit(download_one, row, output_dir, max(1, args.retries)): row
            for row in rows
        }
        for index, future in enumerate(as_completed(futures), start=1):
            result = future.result()
            results.append(result)
            print(
                f"{index}/{len(rows)} {result['status']} "
                f"{result['bank']} {result['report_year']}-{result['report_period']}",
                flush=True,
            )

    write_manifest(results, args.manifest.expanduser().resolve())
    status_counts: dict[str, int] = {}
    for result in results:
        status_counts[result["status"]] = status_counts.get(result["status"], 0) + 1
    actual_mb = sum(int(result["actual_bytes"] or 0) for result in results) / 1024 / 1024
    print(f"status={status_counts} actual_mb={actual_mb:.1f}")
    if status_counts.get("error"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
