#!/usr/bin/env python3
"""05_quality_check_full.py — Full quality check on clean markdown outputs."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
FULL_DIR = PROJECT_ROOT / "docmind_ocr_full"
MANIFEST_PATH = FULL_DIR / "input_manifest.json"
MD_FULL_DIR = FULL_DIR / "markdown_full"
MD_CHUNKS_DIR = FULL_DIR / "markdown_chunks"
REPORTS_DIR = FULL_DIR / "reports"


def log(msg: str) -> None:
    print(f"[{datetime.now(tz).strftime('%H:%M:%S')}] {msg}")


def analyze(text: str) -> dict:
    total = len(text)
    non_ws = len(re.sub(r"\s", "", text))
    chinese = len(re.findall(r"[一-鿿]", text))
    garbled = len(re.findall(r"[�]", text))  # U+FFFD replacement char
    h1 = len(re.findall(r"^# ", text, re.MULTILINE))
    h2 = len(re.findall(r"^## ", text, re.MULTILINE))
    h3 = len(re.findall(r"^### ", text, re.MULTILINE))
    images = len(re.findall(r"!\[.*?\]\(.*?\)", text))
    tables = len(re.findall(r"^\|.*\|$", text, re.MULTILINE))
    # Question bank specific
    qnums = len(re.findall(r"\(\d{1,3}\)", text))
    opts = len(re.findall(r"[A-D][.、)]", text))
    answer_kw = len(re.findall(r"(答案|解析|正确答案|参考答案)", text))
    # Fused options
    fused_count = 0
    for line in text.split("\n"):
        if len(re.findall(r"[A-D][.、)]", line)) >= 2:
            fused_count += 1

    # Top 20 repeated lines (ignoring blank)
    nonblank = [l.strip() for l in text.split("\n") if l.strip()]
    top20 = Counter(nonblank).most_common(20)

    # OSS URL remnants
    oss_remnant = len(re.findall(r'aliyuncs\.com', text)) + len(re.findall(r'OSSAccessKeyId', text))
    oss_remnant += len(re.findall(r'Signature=', text)) + len(re.findall(r'SecurityToken=', text))

    return {
        "total_chars": total,
        "chinese_chars": chinese,
        "chinese_ratio": chinese / non_ws if non_ws > 0 else 0,
        "garbled": garbled,
        "h1": h1, "h2": h2, "h3": h3,
        "images": images,
        "table_lines": tables,
        "question_numbers": qnums,
        "option_letters": opts,
        "answer_keywords": answer_kw,
        "fused_option_lines": fused_count,
        "top20_repeated": top20,
        "oss_remnant": oss_remnant,
    }


def check_chunks(doc: dict) -> dict:
    slug = doc["slug"]
    total = len(doc["chunks"])
    success = 0
    failed = 0
    empty = 0
    char_counts = []

    for chunk in doc["chunks"]:
        md_path = MD_CHUNKS_DIR / slug / f"{chunk['chunk_id']}.md"
        if chunk.get("status") == "success" or (md_path.exists() and not md_path.read_text(encoding="utf-8").strip().startswith("Error")):
            success += 1
            chars = len(md_path.read_text(encoding="utf-8"))
            char_counts.append(chars)
            if chars < 200:
                empty += 1
        else:
            failed += 1

    return {
        "total_chunks": total,
        "success": success,
        "failed": failed,
        "empty_or_short": empty,
        "min_chars": min(char_counts) if char_counts else 0,
        "max_chars": max(char_counts) if char_counts else 0,
        "avg_chars": sum(char_counts) / len(char_counts) if char_counts else 0,
    }


def generate_report(analyses: dict, chunk_stats: dict, manifest: dict):
    lines = [
        "# Full Quality Report",
        f"\nGenerated: {datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')}\n",
        "---\n",
    ]

    for doc in manifest["documents"]:
        slug = doc["slug"]
        data = analyses.get(slug, {})
        cs = chunk_stats.get(slug, {})

        if not data:
            lines.append(f"## {doc['title']} — NO DATA\n")
            continue

        score = 0
        issues = []

        lines.append(f"## {doc['title']} ({slug})")
        lines.append(f"\n### Chunk Summary")
        lines.append(f"\n| Metric | Value |")
        lines.append(f"|--------|-------|")
        lines.append(f"| Total chunks | {cs.get('total_chunks', '?')} |")
        lines.append(f"| Successful | {cs.get('success', '?')} |")
        lines.append(f"| Failed | {cs.get('failed', '?')} |")
        lines.append(f"| Empty/short (<200 chars) | {cs.get('empty_or_short', '?')} |")
        lines.append(f"| Min chunk chars | {cs.get('min_chars', 0):,} |")
        lines.append(f"| Max chunk chars | {cs.get('max_chars', 0):,} |")
        lines.append(f"| Avg chunk chars | {cs.get('avg_chars', 0):,.0f} |")

        lines.append(f"\n### Text Metrics")
        lines.append(f"\n| Metric | Value |")
        lines.append(f"|--------|-------|")
        lines.append(f"| Total chars | {data['total_chars']:,} |")
        lines.append(f"| Chinese chars | {data['chinese_chars']:,} |")
        lines.append(f"| Chinese ratio | {data['chinese_ratio']:.1%} |")
        lines.append(f"| Garbled chars (�) | {data['garbled']} |")

        if data["garbled"] > 0:
            score += 3
            issues.append(f"Garbled chars found: {data['garbled']}")
        if data["chinese_ratio"] < 0.4:
            score += 3
            issues.append(f"Low Chinese ratio: {data['chinese_ratio']:.1%}")
        elif data["chinese_ratio"] < 0.6:
            score += 1
            issues.append(f"Moderate Chinese ratio: {data['chinese_ratio']:.1%}")

        lines.append(f"\n### Structure")
        lines.append(f"\n| Metric | Value |")
        lines.append(f"|--------|-------|")
        lines.append(f"| H1 headings | {data['h1']} |")
        lines.append(f"| H2 headings | {data['h2']} |")
        lines.append(f"| H3 headings | {data['h3']} |")
        lines.append(f"| Images | {data['images']} |")
        lines.append(f"| Table lines | {data['table_lines']} |")

        if data['h1'] + data['h2'] < 5:
            score += 1
            issues.append("Few headings — structure may be lost")

        lines.append(f"\n### Question/Answer Metrics ({slug})")
        lines.append(f"\n| Metric | Value |")
        lines.append(f"|--------|-------|")
        lines.append(f"| Question numbers detected | {data['question_numbers']} |")
        lines.append(f"| A/B/C/D options | {data['option_letters']} |")
        lines.append(f"| Answer/解析 keywords | {data['answer_keywords']} |")
        lines.append(f"| Fused option lines | {data['fused_option_lines']} |")

        if data['fused_option_lines'] > 10:
            score += 2
            issues.append(f"Many fused options: {data['fused_option_lines']}")

        lines.append(f"\n### Security Check")
        lines.append(f"\n| Metric | Value |")
        lines.append(f"|--------|-------|")
        lines.append(f"| OSS signature remnants | {data['oss_remnant']} |")
        if data['oss_remnant'] > 0:
            score += 5
            issues.append(f"OSS signature URLs found in output — security issue!")

        if data['top20_repeated']:
            lines.append(f"\n### Top 20 Repeated Lines")
            lines.append("```")
            for line, cnt in data['top20_repeated'][:20]:
                if cnt >= 3:
                    lines.append(f"[{cnt}x] {line[:100]}")
            lines.append("```")

        lines.append(f"\n### Issues & Score: {score}")
        for issue in issues:
            lines.append(f"- ⚠ {issue}")
        if not issues:
            lines.append("- No issues detected ✓")

        lines.append(f"\n### Manual Review Suggestions")
        if doc['slug'] == 'tutorial':
            lines.append("- Pages 1-10: Title page, preface, TOC")
            lines.append("- Chapter start pages")
            lines.append("- Table-heavy pages")
        else:
            lines.append("- Pages 1-10: Early questions")
            lines.append("- Pages 50, 100, 150: Chunk boundaries")
            lines.append("- Last pages")
        lines.append("")

    report_path = REPORTS_DIR / "03_quality_report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    log(f"Quality report: {report_path}")


def main():
    log("===== Quality Check Start =====")
    REPORT_DIR = REPORTS_DIR  # shorthand

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    analyses = {}
    chunk_stats = {}
    for doc in manifest["documents"]:
        slug = doc["slug"]
        clean_path = MD_FULL_DIR / f"{slug}.full.clean.md"
        raw_path = MD_FULL_DIR / f"{slug}.full.raw.md"
        target = clean_path if clean_path.exists() else raw_path

        if target.exists():
            analyses[slug] = analyze(target.read_text(encoding="utf-8"))
            log(f"  {slug}: {analyses[slug]['total_chars']:,} chars, {analyses[slug]['chinese_ratio']:.1%} Chinese")
        else:
            log(f"  {slug}: no markdown found")
            analyses[slug] = {"total_chars": 0, "chinese_chars": 0, "chinese_ratio": 0}

        chunk_stats[slug] = check_chunks(doc)

    generate_report(analyses, chunk_stats, manifest)
    log("===== Quality Check Done =====")


if __name__ == "__main__":
    main()
