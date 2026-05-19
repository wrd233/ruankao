#!/usr/bin/env python3
"""01_make_chunks.py — Split source PDFs into 50-page chunk PDFs."""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
FULL_DIR = PROJECT_ROOT / "docmind_ocr_full"
MANIFEST_PATH = FULL_DIR / "input_manifest.json"
CHUNKS_DIR = FULL_DIR / "chunks"
REPORTS_DIR = FULL_DIR / "reports"


def log(msg: str) -> None:
    print(f"[{datetime.now(tz).strftime('%H:%M:%S')}] {msg}")


def make_chunks(src_pdf: Path, doc: dict) -> list[dict]:
    """Split source PDF into chunk files. Returns list of chunk records."""
    from pypdf import PdfReader, PdfWriter

    reader = PdfReader(str(src_pdf))
    total = len(reader.pages)
    results = []

    for chunk in doc["chunks"]:
        start = chunk["start_page"]
        end = chunk["end_page"]
        chunk_id = chunk["chunk_id"]
        slug = doc["slug"]

        dst = CHUNKS_DIR / slug / f"{chunk_id}.pdf"
        dst.parent.mkdir(parents=True, exist_ok=True)

        if dst.exists():
            log(f"  Skip existing: {chunk_id}.pdf")
            results.append({**chunk, "file": str(dst), "pages_written": end - start + 1})
            continue

        writer = PdfWriter()
        # pypdf is 0-indexed
        for i in range(start - 1, end):
            writer.add_page(reader.pages[i])

        writer.write(str(dst))
        pages_written = end - start + 1
        log(f"  Created {chunk_id}.pdf ({pages_written} pages)")
        results.append({**chunk, "file": str(dst), "pages_written": pages_written})

    return results


def validate_chunks(doc: dict, results: list[dict]):
    """Validate chunk continuity and page counts."""
    expected_total = doc["pages"]
    actual_total = sum(r["pages_written"] for r in results)
    issues = []

    if actual_total != expected_total:
        issues.append(f"Page total mismatch: expected {expected_total}, got {actual_total}")

    for r in results:
        path = Path(r["file"])
        if not path.is_file() or path.stat().st_size == 0:
            issues.append(f"Chunk file empty or missing: {path.name}")

    start_pages = [r["start_page"] for r in results]
    for i in range(len(start_pages) - 1):
        if start_pages[i + 1] != results[i]["end_page"] + 1:
            issues.append(f"Gap between {results[i]['chunk_id']} and {results[i+1]['chunk_id']}")

    return issues


def main():
    log("===== Make Chunks Start =====")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    report_lines = [
        "# Chunk Manifest Report",
        f"\nGenerated: {datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')}\n",
    ]

    all_results = {}
    for doc in manifest["documents"]:
        slug = doc["slug"]
        src = PROJECT_ROOT / doc["source_pdf"]
        log(f"\n--- {slug}: {src.name} ({doc['pages']} pages) ---")

        results = make_chunks(src, doc)
        issues = validate_chunks(doc, results)

        report_lines.append(f"## {doc['title']}")
        report_lines.append(f"\n- Source: `{src.name}`")
        report_lines.append(f"- Pages: {doc['pages']}")
        report_lines.append(f"- Chunks: {len(results)}")
        report_lines.append(f"- Chunk size: {doc['chunk_size']}")
        report_lines.append(f"\n| Chunk ID | Pages | Size |")
        report_lines.append("|----------|-------|------|")

        for r in results:
            fsize = Path(r["file"]).stat().st_size / 1024
            report_lines.append(f"| {r['chunk_id']} | {r['start_page']}-{r['end_page']} | {fsize:.1f} KB |")

        if issues:
            report_lines.append(f"\n### Issues")
            for issue in issues:
                report_lines.append(f"- ⚠ {issue}")
                log(f"  ⚠ {issue}")
        else:
            report_lines.append(f"\nAll chunks validated OK.")
            log(f"  All {len(results)} chunks validated OK.")

        # Update manifest status
        for chunk in doc["chunks"]:
            chunk["status"] = "ready"
        all_results[slug] = results

    # Save updated manifest
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    report_path = REPORTS_DIR / "01_chunk_manifest.md"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    log(f"\nReport: {report_path}")
    log("===== Make Chunks Done =====")


if __name__ == "__main__":
    main()
