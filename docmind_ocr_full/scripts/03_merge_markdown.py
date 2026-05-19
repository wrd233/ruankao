#!/usr/bin/env python3
"""03_merge_markdown.py — Merge chunk markdown files into full-document markdown."""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
FULL_DIR = PROJECT_ROOT / "docmind_ocr_full"
MANIFEST_PATH = FULL_DIR / "input_manifest.json"
MD_CHUNKS_DIR = FULL_DIR / "markdown_chunks"
MD_FULL_DIR = FULL_DIR / "markdown_full"
REPORTS_DIR = FULL_DIR / "reports"


def log(msg: str) -> None:
    print(f"[{datetime.now(tz).strftime('%H:%M:%S')}] {msg}")


def merge_chunks(doc: dict) -> str:
    """Merge all chunk markdown files for a document into one string."""
    slug = doc["slug"]
    parts = []
    missing = []

    for chunk in sorted(doc["chunks"], key=lambda c: c["start_page"]):
        chunk_id = chunk["chunk_id"]
        src = MD_CHUNKS_DIR / slug / f"{chunk_id}.md"
        if not src.exists():
            missing.append(chunk_id)
            parts.append(
                f"\n\n<!-- DOCMIND_CHUNK_START: {chunk_id}; source_pages={chunk['start_page']}-{chunk['end_page']} -->\n"
                f"\n[MISSING CHUNK: {chunk_id} — pages {chunk['start_page']}-{chunk['end_page']}]\n"
                f"\n<!-- DOCMIND_CHUNK_END: {chunk_id} -->\n"
            )
            continue

        text = src.read_text(encoding="utf-8")
        # Skip error-only responses
        if text.strip().startswith("Error executing tool"):
            missing.append(chunk_id)
            parts.append(
                f"\n\n<!-- DOCMIND_CHUNK_START: {chunk_id}; source_pages={chunk['start_page']}-{chunk['end_page']} -->\n"
                f"\n[ERROR CHUNK: {chunk_id} — pages {chunk['start_page']}-{chunk['end_page']}]\n"
                f"\n<!-- DOCMIND_CHUNK_END: {chunk_id} -->\n"
            )
            continue

        boundary = (
            f"\n\n<!-- DOCMIND_CHUNK_START: {chunk_id}; source_pages={chunk['start_page']}-{chunk['end_page']} -->\n"
        )
        end_boundary = f"\n<!-- DOCMIND_CHUNK_END: {chunk_id} -->\n"
        parts.append(boundary + text + end_boundary)

    result = f"# {doc['title']}\n\n"
    result += f"> Source PDF: {doc['source_pdf']}\n"
    result += f"> Pages: {doc['pages']} | Chunks: {len(doc['chunks'])} | Missing/Error: {len(missing)}\n"
    if missing:
        result += f"> Missing chunks: {', '.join(missing)}\n"
    result += "\n---\n"
    result += "".join(parts)

    return result, missing


def main():
    log("===== Merge Markdown Start =====")

    MD_FULL_DIR.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    for doc in manifest["documents"]:
        slug = doc["slug"]
        log(f"Merging {slug}...")
        merged, missing = merge_chunks(doc)

        raw_path = MD_FULL_DIR / f"{slug}.full.raw.md"
        raw_path.write_text(merged, encoding="utf-8")
        log(f"  Raw: {raw_path} ({len(merged):,} chars)")
        if missing:
            log(f"  ⚠ Missing chunks: {missing}")

    log("===== Merge Done =====")


if __name__ == "__main__":
    main()
