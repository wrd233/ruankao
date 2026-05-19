#!/usr/bin/env python3
"""06_secret_scan.py — Scan tracked files for credential/signature leakage."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
FULL_DIR = PROJECT_ROOT / "docmind_ocr_full"
REPORTS_DIR = FULL_DIR / "reports"

# Patterns to scan for
PATTERNS = [
    # Alibaba Cloud credentials
    r'ALIBABA_CLOUD_ACCESS_KEY',
    r'AccessKey\s*(Id|Secret)?\s*[:=]\s*["\']?\w{16,}',
    r'LTAI\w{16,}',  # Alibaba AK pattern
    # OSS temp URL tokens
    r'OSSAccessKeyId=',
    r'Signature=',
    r'SecurityToken=',
    r'Expires=',
    r'x-oss-',
    # Generic secrets
    r'secret\s*[:=]\s*["\']?\w{16,}',
    r'SECRET\s*[:=]',
]

# Paths to scan
SCAN_PATHS = [
    "docmind_ocr_full/reports/",
    "docmind_ocr_full/markdown_full/",
    "docmind_ocr_full/markdown_chunks/",
    "docmind_ocr_full/raw_outputs/",
    "docmind_ocr_full/scripts/",
    ".gitignore",
]


def log(msg: str) -> None:
    print(f"[{datetime.now(tz).strftime('%H:%M:%S')}] {msg}")


def scan_with_git_grep():
    """Use git grep to find secrets in tracked files."""
    results = []
    for pattern in PATTERNS:
        try:
            r = subprocess.run(
                ["git", "grep", "-nE", pattern, "--", "."],
                cwd=str(PROJECT_ROOT),
                capture_output=True, text=True, timeout=30,
            )
            output = r.stdout.strip()
            if output:
                results.append((pattern, output))
        except Exception as e:
            log(f"  git grep error for {pattern[:40]}: {e}")
    return results


def classify_hit(pattern: str, line: str) -> str:
    """Classify whether a hit is a real leak or a false positive."""
    line_lower = line.lower()
    # False positives: comments, documentation, code variable names
    if any(kw in line_lower for kw in ["os.getenv", "os.environ", "check_env", "env_path",
                                          "export ", "source .env", "never print", "gitignore",
                                          "安全", "脱敏", "redact", "redacted", "removed",
                                          "access_key_id", "access_key_secret",
                                          '"ALIBABA_CLOUD_ACCESS_KEY_ID"',
                                          '"ALIBABA_CLOUD_ACCESS_KEY_SECRET"',
                                          "'ALIBABA_CLOUD_ACCESS_KEY_ID'",
                                          "'ALIBABA_CLOUD_ACCESS_KEY_SECRET'"]):
        return "false_positive"
    # Check for actual key values
    if re.search(r'LTAI\w{16,}', line):
        return "REAL_LEAK"
    if re.search(r'OSSAccessKeyId=\w+', line):
        return "REAL_LEAK"
    if re.search(r'Signature=\w+', line):
        return "REAL_LEAK"
    return "uncertain"


def main():
    log("===== Secret Scan Start =====")

    # 1. Git grep scan
    log("Scanning tracked files via git grep...")
    hits = scan_with_git_grep()

    lines = [
        "# Security Scan Report",
        f"\nGenerated: {datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')}\n",
        "## Scan Summary\n",
    ]

    real_leaks = []
    false_positives = []
    uncertain = []

    for pattern, output in hits:
        for hit_line in output.split("\n"):
            if not hit_line.strip():
                continue
            classification = classify_hit(pattern, hit_line)
            if classification == "REAL_LEAK":
                real_leaks.append((pattern, hit_line))
            elif classification == "false_positive":
                false_positives.append((pattern, hit_line))
            else:
                uncertain.append((pattern, hit_line))

    lines.append(f"| Category | Count |")
    lines.append(f"|----------|-------|")
    lines.append(f"| Real leaks | {len(real_leaks)} |")
    lines.append(f"| False positives | {len(false_positives)} |")
    lines.append(f"| Uncertain | {len(uncertain)} |")
    lines.append("")

    if real_leaks:
        lines.append("## ⚠ REAL LEAKS — Fix Immediately")
        lines.append("")
        for pat, hit in real_leaks:
            # Redact sensitive parts
            safe = re.sub(r'=(\w{4})\w+', r'=\1***REDACTED***', hit)
            lines.append(f"- Pattern `{pat[:50]}`: `{safe[:150]}`")
        lines.append("")

    if false_positives:
        lines.append("## False Positives (Documented)")
        lines.append("")
        for pat, hit in false_positives[:10]:
            lines.append(f"- `{hit[:120]}`")
        if len(false_positives) > 10:
            lines.append(f"- ... and {len(false_positives) - 10} more")
        lines.append("")

    if uncertain:
        lines.append("## Uncertain — Review Manually")
        lines.append("")
        for pat, hit in uncertain[:10]:
            safe = re.sub(r'=(\w{4})\w+', r'=\1***REDACTED***', hit)
            lines.append(f"- `{safe[:150]}`")
        lines.append("")

    verdict = "PASS" if not real_leaks else "FAIL — real leaks found!"
    lines.append(f"## Verdict: {verdict}")
    lines.append("")

    report_path = REPORTS_DIR / "06_secret_scan.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    log(f"Real leaks: {len(real_leaks)}, False positives: {len(false_positives)}, Uncertain: {len(uncertain)}")
    log(f"Verdict: {verdict}")
    log(f"Report: {report_path}")
    log("===== Secret Scan Done =====")

    if real_leaks:
        sys.exit(1)


if __name__ == "__main__":
    main()
