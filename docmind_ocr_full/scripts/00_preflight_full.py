#!/usr/bin/env python3
"""00_preflight_full.py — Full-run preflight: verify env, PDFs, and chunk plan."""

from __future__ import annotations

import json
import os
import shutil
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

tz = timezone(timedelta(hours=8))
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
FULL_DIR = PROJECT_ROOT / "docmind_ocr_full"
REPORTS_DIR = FULL_DIR / "reports"
MANIFEST_PATH = FULL_DIR / "input_manifest.json"


def log(msg: str) -> None:
    print(f"[{datetime.now(tz).strftime('%H:%M:%S')}] {msg}")


def main():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    log("===== Full Preflight Start =====")

    lines = [
        "# Full-Run Preflight Report",
        f"\nGenerated: {datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')}\n",
        "## Environment\n",
    ]

    # Python
    py_v = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    lines.append(f"- Python: {py_v} @ `{sys.executable}`")
    log(f"Python {py_v}")

    # uvx / uv
    uvx = shutil.which("uvx")
    uv = shutil.which("uv")
    lines.append(f"- uvx: {'OK' if uvx else 'MISSING'}")
    lines.append(f"- uv: {'OK' if uv else 'MISSING'}")
    log(f"uvx: {'OK' if uvx else 'MISSING'}")

    # Credentials
    ak = bool(os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"))
    sk = bool(os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"))
    lines.append(f"- AK_ID: {'PRESENT' if ak else 'MISSING'}")
    lines.append(f"- AK_SECRET: {'PRESENT' if sk else 'MISSING'}")
    log(f"AK: {'PRESENT' if ak else 'MISSING'}")

    if not ak or not sk:
        lines.append("\n**STOP: Credentials missing.** Run `source .env` first.\n")
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        (REPORTS_DIR / "00_preflight_full.md").write_text("\n".join(lines), encoding="utf-8")
        sys.exit(1)

    # Manifest
    if not MANIFEST_PATH.exists():
        lines.append(f"\n**STOP: Manifest not found at {MANIFEST_PATH}**\n")
        (REPORTS_DIR / "00_preflight_full.md").write_text("\n".join(lines), encoding="utf-8")
        sys.exit(1)

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    lines.append("\n## Source PDFs\n")
    lines.append("| Document | Pages | Chunks | Status |")
    lines.append("|----------|-------|--------|--------|")

    all_ok = True
    for doc in manifest["documents"]:
        src = PROJECT_ROOT / doc["source_pdf"]
        exists = src.is_file()
        size_mb = src.stat().st_size / (1024 * 1024) if exists else 0
        chunks_n = len(doc["chunks"])
        status = "OK" if exists else "MISSING"
        lines.append(f"| {doc['title'][:30]} | {doc['pages']} ({size_mb:.1f}MB) | {chunks_n} chunks | {status} |")
        log(f"{doc['slug']}: {doc['pages']}pp, {size_mb:.1f}MB, {chunks_n} chunks, {status}")
        if not exists:
            all_ok = False

    lines.append("")
    if all_ok:
        total_pages = sum(d["pages"] for d in manifest["documents"])
        total_chunks = sum(len(d["chunks"]) for d in manifest["documents"])
        lines.append(f"**Verdict**: All checks passed. {total_pages} total pages, {total_chunks} total chunks.\n")
        log(f"All OK: {total_pages} pages, {total_chunks} chunks")
    else:
        lines.append("**Verdict**: Some PDFs missing.\n")

    report_path = REPORTS_DIR / "00_preflight_full.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    log(f"Report: {report_path}")
    log("===== Full Preflight Done =====")


if __name__ == "__main__":
    main()
