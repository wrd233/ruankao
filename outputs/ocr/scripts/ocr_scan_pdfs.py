#!/usr/bin/env python3
"""Render scanned PDFs, OCR each page, and build searchable page outputs."""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import statistics
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

import fitz
import pytesseract
from PIL import Image
from pypdf import PdfReader, PdfWriter


ROOT = Path(__file__).resolve().parents[3]
OUTPUTS = ROOT / "outputs" / "ocr"
PAGES_DIR = OUTPUTS / "pages"
PDF_DIR = OUTPUTS / "pdf"
LOGS_DIR = OUTPUTS / "logs"
TESSDATA_DIR = OUTPUTS / "tessdata"

DEFAULT_CONFIG = " --psm 6 "


def slugify(text: str) -> str:
    slug = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", "_", text).strip("_").lower()
    return slug or "document"


def contains_chinese(text: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", text))


def chinese_ratio(text: str) -> float:
    non_ws = [ch for ch in text if not ch.isspace()]
    if not non_ws:
        return 0.0
    chinese = sum(1 for ch in non_ws if "\u4e00" <= ch <= "\u9fff")
    return chinese / len(non_ws)


def weird_ratio(text: str) -> float:
    non_ws = [ch for ch in text if not ch.isspace()]
    if not non_ws:
        return 0.0
    weird = sum(
        1
        for ch in non_ws
        if not (
            ch.isalnum()
            or "\u4e00" <= ch <= "\u9fff"
            or ch in ".,;:!?()[]{}<>+-=*/%#&_~'\"，。；：！？（）《》、"
        )
    )
    return weird / len(non_ws)


def question_pattern(text: str) -> bool:
    patterns = [
        r"\(\d+\)",
        r"第\s*\d+\s*题",
        r"[A-DＡ-Ｄ][\.\s、]",
        r"答案",
        r"解析",
    ]
    return any(re.search(p, text) for p in patterns)


def normalize_preview(text: str, limit: int = 240) -> str:
    collapsed = re.sub(r"\s+", " ", text).strip()
    return collapsed[:limit]


def quality_flag(text: str) -> tuple[str, list[str]]:
    non_ws = len(re.sub(r"\s+", "", text))
    c_ratio = chinese_ratio(text)
    w_ratio = weird_ratio(text)
    notes: list[str] = []
    if non_ws == 0:
        return "empty", ["empty_text"]
    if non_ws < 40:
        notes.append("very_low_text")
    elif non_ws < 120:
        notes.append("low_text")
    if c_ratio < 0.05 and non_ws >= 40:
        notes.append("low_chinese_ratio")
    if w_ratio > 0.18 and non_ws >= 40:
        notes.append("high_weird_ratio")
    if notes:
        return "review", notes
    return "ok", []


@dataclass
class PageResult:
    page: int
    text_path: str
    char_count: int
    non_whitespace_count: int
    contains_chinese: bool
    chinese_ratio: float
    weird_ratio: float
    contains_question_pattern: bool
    quality_flag: str
    notes: str
    preview: str
    ocr_seconds: float


def render_page(page: fitz.Page, zoom: float) -> Image.Image:
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    return Image.frombytes("RGB", [pix.width, pix.height], pix.samples)


def image_to_pdf_page(img: Image.Image, lang: str, config: str) -> bytes:
    return pytesseract.image_to_pdf_or_hocr(img, extension="pdf", lang=lang, config=config)


def image_only_pdf_page(img: Image.Image) -> bytes:
    bio = io.BytesIO()
    img.save(bio, format="PDF", resolution=300.0)
    return bio.getvalue()


def iter_pages(page_count: int, start_page: int | None, end_page: int | None) -> Iterable[int]:
    start = 1 if start_page is None else max(1, start_page)
    end = page_count if end_page is None else min(page_count, end_page)
    return range(start, end + 1)


def process_page(
    pdf_path_str: str,
    pages_dir_str: str,
    temp_pdf_dir_str: str,
    page_number: int,
    lang: str,
    config: str,
    zoom: float,
    tessdata_dir_str: str,
) -> dict:
    os.environ.setdefault("TESSDATA_PREFIX", tessdata_dir_str)
    pdf_path = Path(pdf_path_str)
    pages_dir = Path(pages_dir_str)
    temp_pdf_dir = Path(temp_pdf_dir_str)
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_number - 1)
    ocr_started = time.time()
    try:
        img = render_page(page, zoom=zoom)
        text = pytesseract.image_to_string(img, lang=lang, config=config)
        try:
            page_pdf_bytes = image_to_pdf_page(img, lang=lang, config=config)
        except Exception:
            page_pdf_bytes = image_only_pdf_page(img)
    except Exception as exc:  # pragma: no cover
        text = ""
        page_pdf_bytes = image_only_pdf_page(render_page(page, zoom=zoom))
        flag = "error"
        note_text = f"ocr_exception:{type(exc).__name__}:{exc}"
    else:
        flag, note_items = quality_flag(text)
        note_text = "; ".join(note_items)

    page_txt_path = pages_dir / f"page_{page_number:03d}.txt"
    page_txt_path.write_text(text, encoding="utf-8")

    page_pdf_path = temp_pdf_dir / f"page_{page_number:03d}.pdf"
    page_pdf_path.write_bytes(page_pdf_bytes)

    non_ws_count = len(re.sub(r"\s+", "", text))
    result = PageResult(
        page=page_number,
        text_path=page_txt_path.name,
        char_count=len(text),
        non_whitespace_count=non_ws_count,
        contains_chinese=contains_chinese(text),
        chinese_ratio=round(chinese_ratio(text), 4),
        weird_ratio=round(weird_ratio(text), 4),
        contains_question_pattern=question_pattern(text),
        quality_flag=flag,
        notes=note_text,
        preview=normalize_preview(text),
        ocr_seconds=round(time.time() - ocr_started, 3),
    )
    return asdict(result)


def run_ocr(
    pdf_path: Path,
    doc_slug: str,
    output_pdf_name: str,
    lang: str,
    config: str,
    zoom: float,
    start_page: int | None,
    end_page: int | None,
) -> dict:
    pages_dir = PAGES_DIR / doc_slug
    pages_dir.mkdir(parents=True, exist_ok=True)
    page_index_path = pages_dir / "pages_index.json"
    run_summary_path = pages_dir / "run_summary.json"
    markdown_dump_path = pages_dir / f"{doc_slug}_pages.md"
    output_pdf_path = PDF_DIR / output_pdf_name
    temp_pdf_dir = pages_dir / "_page_pdf_parts"
    temp_pdf_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    writer = PdfWriter()
    page_results: list[PageResult] = []
    page_md_sections: list[str] = []
    processed = 0
    started_at = time.time()
    page_numbers = list(iter_pages(doc.page_count, start_page, end_page))
    futures = []
    workers = min(max(1, os.cpu_count() or 1), 4)
    with ProcessPoolExecutor(max_workers=workers) as executor:
        for page_number in page_numbers:
            futures.append(
                executor.submit(
                    process_page,
                    str(pdf_path),
                    str(pages_dir),
                    str(temp_pdf_dir),
                    page_number,
                    lang,
                    config,
                    zoom,
                    str(TESSDATA_DIR.resolve()),
                )
            )
        results_map = {}
        for future in as_completed(futures):
            result_dict = future.result()
            result = PageResult(**result_dict)
            results_map[result.page] = result
            processed += 1
            print(
                json.dumps(
                    {
                        "doc_slug": doc_slug,
                        "page": result.page,
                        "quality_flag": result.quality_flag,
                        "char_count": result.char_count,
                        "ocr_seconds": result.ocr_seconds,
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )

    for page_number in page_numbers:
        result = results_map[page_number]
        page_results.append(result)
        text = (pages_dir / result.text_path).read_text(encoding="utf-8")
        page_md_sections.append(
            f"## page_{page_number:03d}\n\n"
            f"- quality_flag: `{result.quality_flag}`\n"
            f"- char_count: `{result.char_count}`\n"
            f"- non_whitespace_count: `{result.non_whitespace_count}`\n"
            f"- notes: `{result.notes or 'none'}`\n\n"
            f"```text\n{text.strip()}\n```\n"
        )
        writer.append(PdfReader(temp_pdf_dir / f"page_{page_number:03d}.pdf"))

    with output_pdf_path.open("wb") as fh:
        writer.write(fh)

    page_index_path.write_text(
        json.dumps([asdict(item) for item in page_results], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    markdown_dump_path.write_text("\n".join(page_md_sections), encoding="utf-8")

    summary = {
        "pdf_path": str(pdf_path),
        "doc_slug": doc_slug,
        "page_count_total": doc.page_count,
        "page_count_processed": processed,
        "start_page": start_page,
        "end_page": end_page,
        "output_pdf": str(output_pdf_path),
        "pages_index": str(page_index_path),
        "average_char_count": round(statistics.mean([p.char_count for p in page_results]), 2)
        if page_results
        else 0,
        "average_non_whitespace_count": round(
            statistics.mean([p.non_whitespace_count for p in page_results]), 2
        )
        if page_results
        else 0,
        "quality_counts": {
            key: sum(1 for p in page_results if p.quality_flag == key)
            for key in ["ok", "review", "empty", "error"]
        },
        "elapsed_seconds": round(time.time() - started_at, 2),
    }
    run_summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", required=True, help="Source PDF path, relative to repo root or absolute")
    parser.add_argument("--slug", required=True, help="Directory name under outputs/ocr/pages")
    parser.add_argument("--output-pdf-name", required=True, help="Output PDF file name")
    parser.add_argument("--lang", default="chi_sim+eng")
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    parser.add_argument("--zoom", type=float, default=2.5)
    parser.add_argument("--start-page", type=int)
    parser.add_argument("--end-page", type=int)
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.is_absolute():
        pdf_path = ROOT / pdf_path
    os.environ.setdefault("TESSDATA_PREFIX", str(TESSDATA_DIR.resolve()))

    summary = run_ocr(
        pdf_path=pdf_path,
        doc_slug=args.slug or slugify(pdf_path.stem),
        output_pdf_name=args.output_pdf_name,
        lang=args.lang,
        config=args.config,
        zoom=args.zoom,
        start_page=args.start_page,
        end_page=args.end_page,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
