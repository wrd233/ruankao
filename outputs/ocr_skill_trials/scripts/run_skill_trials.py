#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[3]
BASELINE_DIR = ROOT / "outputs" / "ocr" / "pages"
TRIAL_DIR = ROOT / "outputs" / "ocr_skill_trials"
PAGES_DIR = TRIAL_DIR / "pages"

PDFS = {
    "official_tutorial": ROOT / "《系统集成项目管理工程师教程》官方考试指定第二版.pdf",
    "past_papers_171": ROOT / "历年系统集成项目管理工程师试题解析及答案-171页.pdf",
}

SAMPLES = {
    "official_tutorial": {
        "mandatory_low_quality": [22, 423, 678],
        "chart_table_formula": [338, 339, 340],
        "normal_text": [2, 6, 675],
    },
    "past_papers_171": {
        "mandatory_low_quality": [14, 25, 84, 86, 93, 171],
        "normal_question": [1, 3, 167],
        "question_dense": [34, 85],
    },
}


def page_name(page_num: int) -> str:
    return f"page_{page_num:03d}"


def copy_baseline(slug: str, page_num: int) -> dict:
    src = BASELINE_DIR / slug / f"{page_name(page_num)}.txt"
    dest = PAGES_DIR / "current_baseline" / slug / f"{page_name(page_num)}.txt"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    text = dest.read_text(encoding="utf-8")
    return {
        "text_path": str(dest.relative_to(TRIAL_DIR)),
        "char_count": len(text),
        "non_whitespace_count": sum(1 for ch in text if not ch.isspace()),
    }


def render_page(slug: str, page_num: int, dpi: int = 220) -> str:
    pdf_path = PDFS[slug]
    doc = fitz.open(pdf_path)
    try:
        page = doc.load_page(page_num - 1)
        matrix = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        out = PAGES_DIR / "source_images" / slug / f"{page_name(page_num)}.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        pix.save(out)
        return str(out.relative_to(TRIAL_DIR))
    finally:
        doc.close()


def main() -> None:
    manifest: dict[str, dict[str, list[dict]]] = {}
    for slug, groups in SAMPLES.items():
        manifest[slug] = {}
        for group, page_nums in groups.items():
            manifest[slug][group] = []
            for page_num in page_nums:
                baseline = copy_baseline(slug, page_num)
                image_path = render_page(slug, page_num)
                manifest[slug][group].append(
                    {
                        "page": page_num,
                        "page_name": page_name(page_num),
                        "baseline": baseline,
                        "source_image_path": image_path,
                    }
                )

    manifest_path = TRIAL_DIR / "reports" / "sample_pages_manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
