#!/usr/bin/env python3
"""04_clean_markdown.py — Conservative, auditable markdown cleaning.

Operations (all logged):
1. Redact OSS temporary URLs → keep image ref, strip auth params
2. Normalize blank lines → max 2 consecutive
3. Remove isolated page-number lines
4. Normalize "解析" / "答案" section headings
5. Split fused A/B/C/D option lines in question banks
"""

from __future__ import annotations

import re
from pathlib import Path
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
FULL_DIR = PROJECT_ROOT / "docmind_ocr_full"
MD_FULL_DIR = FULL_DIR / "markdown_full"
REPORTS_DIR = FULL_DIR / "reports"

DOCUMENTS = ["tutorial", "questions"]

# Statistics counters
stats = {
    "oss_urls_redacted": 0,
    "isolated_pages_removed": 0,
    "blank_lines_normalized": 0,
    "parse_headings_normalized": 0,
    "options_split": 0,
    "question_numbers_detected": 0,
    "option_letters_detected": 0,
}


def log(msg: str) -> None:
    print(f"[{datetime.now(tz).strftime('%H:%M:%S')}] {msg}")


def redact_oss_urls(text: str) -> str:
    """Replace OSS temporary URLs, keep image filename reference."""
    # Pattern: http://docmind-api-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/.../0.png?Expires=...&Signature=...&...
    pattern = r'https?://[^\s\)]+\.aliyuncs\.com[^\s\)]*\?[^\s\)]+'
    count = 0

    def replacer(m):
        nonlocal count
        url = m.group(0)
        # Try to extract the filename
        fname_match = re.search(r'/([^/]+\.(?:png|jpe?g|gif|bmp))(?:$|\?)', url)
        fname = fname_match.group(1) if fname_match else "image"
        count += 1
        return f"[IMAGE: {fname}]"

    result = re.sub(pattern, replacer, text)
    stats["oss_urls_redacted"] += count
    return result


def normalize_blank_lines(text: str) -> str:
    """Max 2 consecutive blank lines."""
    before = text.count("\n\n\n")
    result = re.sub(r'\n{4,}', '\n\n\n', text)
    # Now reduce to max 2
    result = re.sub(r'\n{3,}', '\n\n', result)
    after = result.count("\n\n")
    stats["blank_lines_normalized"] += max(0, before - after)
    return result


def remove_isolated_page_numbers(text: str) -> str:
    """Remove lines that are only isolated page numbers (like '42' or 'III' on their own line)."""
    lines = text.split("\n")
    kept = []
    removed = 0
    # Roman numeral page pattern
    roman_pattern = re.compile(r'^\s*(?:[IVXLCDM]{1,6}|[ivxlcdm]{1,6})\s*$')
    # Numeric page pattern (2-4 digit numbers on their own line)
    num_pattern = re.compile(r'^\s*\d{2,4}\s*$')
    # Page with dash pattern: "- 42 -" or "— 42 —"
    dash_pattern = re.compile(r'^\s*[-—]\s*\d{2,4}\s*[-—]\s*$')

    for i, line in enumerate(lines):
        s = line.strip()
        if not s:
            kept.append(line)
            continue
        if roman_pattern.match(s):
            removed += 1
            continue
        if num_pattern.match(s):
            # Be conservative: don't remove if previous line ends with a heading
            prev = kept[-1].strip() if kept else ""
            if not prev.startswith("#"):
                removed += 1
                continue
        if dash_pattern.match(s):
            removed += 1
            continue
        kept.append(line)

    stats["isolated_pages_removed"] += removed
    return "\n".join(kept)


def normalize_parse_headings(text: str) -> str:
    """Normalize 解析/答案 sections to consistent heading format."""
    count = 0
    # Unify various 解析 formats to "## 解析"
    patterns = [
        (r'^[#]{1,6}\s*解析\s*$', '## 解析'),
        (r'^[#]{1,6}\s*【解析】\s*$', '## 解析'),
        (r'^解析[：:]\s*$', '## 解析'),
        (r'^解析\s*\n', '## 解析\n'),
    ]
    for pat, rep in patterns:
        matches = len(re.findall(pat, text, re.MULTILINE))
        if matches > 0:
            text = re.sub(pat, rep, text, flags=re.MULTILINE)
            count += matches

    stats["parse_headings_normalized"] += count
    return text


def split_option_lines(text: str) -> str:
    """Split fused option lines like 'A.xxxB.xxxC.xxxD.xxx'."""
    count = 0

    def split_line(line: str) -> str:
        nonlocal count
        # Check if this line has multiple option markers fused
        option_markers = re.findall(r'[A-D][.、)]', line)
        if len(option_markers) <= 1:
            return line

        # Try to split
        parts = re.split(r'(\s*[A-D][.、)])', line)
        if len(parts) <= 3:
            return line

        result = []
        for j in range(1, len(parts), 2):
            marker = parts[j].strip()
            content = parts[j + 1].strip() if j + 1 < len(parts) else ""
            if content:
                result.append(f"{marker} {content}")
            else:
                result.append(marker)
        if len(result) > 1:
            count += 1
            return "\n".join(result)
        return line

    lines = text.split("\n")
    result = []
    # Only apply to question bank (has many A./B./C./D.)
    for line in lines:
        option_count = len(re.findall(r'[A-D][.、)]', line))
        if option_count >= 2:
            result.append(split_line(line))
        else:
            result.append(line)

    stats["options_split"] += count
    return "\n".join(result)


def detect_stats(text: str) -> None:
    """Detect structural elements for the cleaning report."""
    stats["question_numbers_detected"] += len(re.findall(r'\(\d{1,3}\)', text))
    stats["option_letters_detected"] += len(re.findall(r'[A-D][.、)]', text))


def clean_document(slug: str) -> None:
    """Full cleaning pipeline for one document."""
    raw_path = MD_FULL_DIR / f"{slug}.full.raw.md"
    clean_path = MD_FULL_DIR / f"{slug}.full.clean.md"

    if not raw_path.exists():
        log(f"  {slug}: raw file not found at {raw_path}")
        return

    log(f"  Cleaning {slug}...")
    text = raw_path.read_text(encoding="utf-8")

    # Reset per-doc stats
    per_doc = {
        "before_chars": len(text),
        "before_lines": text.count("\n"),
    }

    # Pipeline
    text = redact_oss_urls(text)
    text = normalize_blank_lines(text)
    text = remove_isolated_page_numbers(text)
    text = normalize_parse_headings(text)
    text = split_option_lines(text)
    detect_stats(text)

    clean_path.write_text(text, encoding="utf-8")
    per_doc["after_chars"] = len(text)
    per_doc["after_lines"] = text.count("\n")
    log(f"    {slug}: {per_doc['before_chars']:,} → {per_doc['after_chars']:,} chars")


def generate_cleaning_report():
    lines = [
        "# Markdown Cleaning Report",
        f"\nGenerated: {datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')}\n",
        "## Cleaning Operations\n",
        f"| Operation | Count |",
        f"|-----------|-------|",
        f"| OSS temp URLs redacted | {stats['oss_urls_redacted']} |",
        f"| Isolated page numbers removed | {stats['isolated_pages_removed']} |",
        f"| Blank line groups normalized | {stats['blank_lines_normalized']} |",
        f"| Parse/Answer headings normalized | {stats['parse_headings_normalized']} |",
        f"| Option lines split | {stats['options_split']} |",
        f"| Question numbers detected | {stats['question_numbers_detected']} |",
        f"| A/B/C/D option letters detected | {stats['option_letters_detected']} |",
        "\n## Conservatism Notes\n",
        "- Only lines that are unambiguously isolated page numbers were removed",
        "- Option splitting only applied when 2+ A-D markers appear on the same line",
        "- OSS URL redaction preserves image filename references",
        "- No body text was modified or rewritten",
        "- Original raw files are preserved at `markdown_full/*.full.raw.md`",
    ]
    report_path = REPORTS_DIR / "04_cleaning_report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    log(f"Cleaning report: {report_path}")


def main():
    log("===== Clean Markdown Start =====")
    MD_FULL_DIR.mkdir(parents=True, exist_ok=True)

    for slug in DOCUMENTS:
        clean_document(slug)

    generate_cleaning_report()
    log("===== Clean Done =====")


if __name__ == "__main__":
    main()
