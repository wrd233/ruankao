#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TRIAL_DIR = ROOT / "outputs" / "ocr_skill_trials"
PAGES_DIR = TRIAL_DIR / "pages"
MANIFEST_PATH = TRIAL_DIR / "reports" / "sample_pages_manifest.json"

CHINESE_RE = re.compile(r"[\u4e00-\u9fff]")
QUESTION_RE = re.compile(r"(\(\d+\)|[A-D][\.．]|答案|解析|试题)")


def summarize_text(path: Path) -> dict:
    if not path.exists():
        return {
            "exists": False,
            "char_count": 0,
            "non_whitespace_count": 0,
            "chinese_ratio": 0.0,
            "contains_question_pattern": False,
            "preview": "",
        }
    text = path.read_text(encoding="utf-8")
    non_ws = [ch for ch in text if not ch.isspace()]
    chinese = sum(1 for ch in non_ws if CHINESE_RE.match(ch))
    return {
        "exists": True,
        "char_count": len(text),
        "non_whitespace_count": len(non_ws),
        "chinese_ratio": round(chinese / len(non_ws), 4) if non_ws else 0.0,
        "contains_question_pattern": bool(QUESTION_RE.search(text)),
        "preview": re.sub(r"\s+", " ", text.strip())[:220],
    }


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    skills = [
        "current_baseline",
        "pdf_ocr_extraction",
        "paddleocr_text_recognition",
        "ocr_document_processor",
    ]
    result = {}
    for slug, groups in manifest.items():
        result[slug] = {}
        for group, pages in groups.items():
            result[slug][group] = []
            for item in pages:
                page_name = item["page_name"]
                page_result = {"page": item["page"], "page_name": page_name}
                for skill in skills:
                    path = PAGES_DIR / skill / slug / f"{page_name}.txt"
                    page_result[skill] = summarize_text(path)
                result[slug][group].append(page_result)
    out = TRIAL_DIR / "reports" / "sample_pages_comparison.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
