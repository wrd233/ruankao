#!/usr/bin/env python3
"""00_preflight.py — Environment preflight check for docmind OCR trial."""

from __future__ import annotations

import os
import sys
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path

tz = timezone(timedelta(hours=8))
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
TRIAL_DIR = PROJECT_ROOT / "docmind_ocr_trial"
REPORTS_DIR = TRIAL_DIR / "reports"
LOGS_DIR = TRIAL_DIR / "logs"


def log(msg: str) -> None:
    timestamp = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)


def match_tutorial(name: str) -> bool:
    return ("教程" in name) and "试题" not in name and "历年" not in name


def match_questions(name: str) -> bool:
    return ("历年" in name and "试题" in name) or "试题解析及答案" in name


def find_pdfs(search_dirs):
    results = {"tutorial": None, "questions": None}
    for d in search_dirs:
        if not d.is_dir():
            continue
        try:
            files = list(d.iterdir())
        except PermissionError:
            log(f"  skip (permission denied): {d}")
            continue
        for f in files:
            if not f.is_file() or f.suffix.lower() != ".pdf":
                continue
            name = f.name
            if results["tutorial"] is None and match_tutorial(name):
                results["tutorial"] = f
                log(f"Found tutorial PDF: {f}")
            if results["questions"] is None and match_questions(name):
                results["questions"] = f
                log(f"Found questions PDF: {f}")
    return results


def get_page_count(path: Path) -> int:
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        return len(reader.pages)
    except Exception as e:
        log(f"Cannot read page count from {path.name}: {e}")
        return -1


def main():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)

    log("===== Preflight Start =====")

    # 1. Python
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    py_path = sys.executable
    log(f"Python {py_version} @ {py_path}")

    # 2. uvx / uv
    uvx_path = shutil.which("uvx")
    uv_path = shutil.which("uv")
    log(f"uvx: {'OK' if uvx_path else 'MISSING'} {uvx_path or ''}")
    log(f"uv : {'OK' if uv_path else 'MISSING'} {uv_path or ''}")

    # 3. AK/SK
    ak = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    sk = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    ak_status = "PRESENT" if ak else "MISSING"
    sk_status = "PRESENT" if sk else "MISSING"
    log(f"AK_ID: {ak_status}")
    log(f"AK_SECRET: {sk_status}")

    # 4. PDFs
    search_dirs = [
        PROJECT_ROOT,
        Path.home() / "Downloads",
        Path.home() / "Desktop",
    ]
    pdfs = find_pdfs(search_dirs)

    tutorial_info = ""
    questions_info = ""
    verdicts = []

    for key, label in [("tutorial", "Tutorial"), ("questions", "Questions")]:
        path = pdfs.get(key)
        if path and path.is_file():
            pages = get_page_count(path)
            size_mb = path.stat().st_size / (1024 * 1024)
            info = f"| {label} | Found ({path.name}) | {pages} pages | {size_mb:.1f} MB |"
            if key == "tutorial":
                tutorial_info = info
            else:
                questions_info = info
            if pages < 0:
                verdicts.append(f"{label} PDF exists but cannot read page count")
        else:
            info = f"| {label} | NOT FOUND | - | - |"
            if key == "tutorial":
                tutorial_info = info
            else:
                questions_info = info
            verdicts.append(f"{label} PDF not found, set PDF_TUTORIAL / PDF_QUESTIONS env var")

    if not uvx_path:
        verdicts.append("uvx not found, run: brew install uv")
    if not ak:
        verdicts.append("AK not set, run: export ALIBABA_CLOUD_ACCESS_KEY_ID=...")

    verdict_text = "\n".join(f"- {v}" for v in verdicts) if verdicts else "- All checks passed"

    now_str = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

    report = f"""# Preflight Report

Generated: {now_str}

## Python

- Version: {py_version}
- Path: `{py_path}`

## Tools

- uvx: {'Available' if uvx_path else 'Missing'} `{uvx_path or ''}`
- uv: {'Available' if uv_path else 'Missing'} `{uv_path or ''}`

## Credentials

- ALIBABA_CLOUD_ACCESS_KEY_ID: {ak_status}
- ALIBABA_CLOUD_ACCESS_KEY_SECRET: {sk_status}

## Source PDFs

| Category | Status | Pages | Size |
|----------|--------|-------|------|
{tutorial_info}
{questions_info}

## Verdict

{verdict_text}
"""

    report_path = REPORTS_DIR / "preflight_report.md"
    report_path.write_text(report, encoding="utf-8")
    log(f"Preflight report saved: {report_path}")

    if verdicts:
        log("Issues found, please fix before continuing.")
    else:
        log("All checks passed, ready for next step.")


if __name__ == "__main__":
    main()
