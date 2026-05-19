#!/usr/bin/env python3
"""01_make_sample_pdfs.py — Extract first 10 pages from source PDFs using pypdf."""

from __future__ import annotations

import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
TRIAL_DIR = PROJECT_ROOT / "docmind_ocr_trial"
INPUT_DIR = TRIAL_DIR / "input_samples"
LOGS_DIR = TRIAL_DIR / "logs"

SAMPLE_PAGES = 10


def log(msg: str) -> None:
    timestamp = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")


def match_tutorial(name: str) -> bool:
    return ("教程" in name) and "试题" not in name and "历年" not in name


def match_questions(name: str) -> bool:
    return ("历年" in name and "试题" in name) or "试题解析及答案" in name


def find_source_pdf(matcher) -> Path | None:
    for f in PROJECT_ROOT.iterdir():
        if f.is_file() and f.suffix.lower() == ".pdf" and matcher(f.name):
            return f
    return None


def extract_sample(src: Path, dst: Path, num_pages: int = SAMPLE_PAGES) -> int:
    from pypdf import PdfReader, PdfWriter

    reader = PdfReader(str(src))
    total = len(reader.pages)
    actual = min(num_pages, total)

    writer = PdfWriter()
    for i in range(actual):
        writer.add_page(reader.pages[i])

    dst.parent.mkdir(parents=True, exist_ok=True)
    writer.write(str(dst))
    return actual


def main():
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)

    log("===== Sample Extraction Start =====")

    tasks = [
        ("tutorial", match_tutorial, "Tutorial"),
        ("questions", match_questions, "Questions"),
    ]

    for slug, matcher, label in tasks:
        src = find_source_pdf(matcher)
        if src is None:
            log(f"FAIL: {label} PDF not found")
            log(f"  Put the PDF in {PROJECT_ROOT}")
            continue

        dst = INPUT_DIR / f"{slug}_pages_001_010.pdf"
        log(f"Source: {src.name}")
        actual = extract_sample(src, dst)
        log(f"Extracted {actual} pages -> {dst.name}")

    log("===== Sample Extraction Done =====")


if __name__ == "__main__":
    main()
