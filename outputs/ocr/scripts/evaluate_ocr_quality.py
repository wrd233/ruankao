#!/usr/bin/env python3
"""Evaluate OCR page outputs and write markdown reports."""

from __future__ import annotations

import json
import re
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OCR_ROOT = ROOT / "outputs" / "ocr"
PAGES_ROOT = OCR_ROOT / "pages"
REPORTS_ROOT = OCR_ROOT / "reports"
REVIEW_ROOT = OCR_ROOT / "review_queue"

DOCS = [
    {
        "name": "官方教程",
        "slug": "official_tutorial",
        "pdf_name": "官方教程_ocr.pdf",
        "source_pdf": "《系统集成项目管理工程师教程》官方考试指定第二版.pdf",
    },
    {
        "name": "历年题解析",
        "slug": "past_papers_171",
        "pdf_name": "历年题解析_171页_ocr.pdf",
        "source_pdf": "历年系统集成项目管理工程师试题解析及答案-171页.pdf",
    },
]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_page_text(slug: str, page: int) -> str:
    return (PAGES_ROOT / slug / f"page_{page:03d}.txt").read_text(encoding="utf-8")


def preview(text: str, limit: int = 160) -> str:
    return re.sub(r"\s+", " ", text).strip()[:limit]


def pick_middle_pages(total: int) -> list[int]:
    mid = max(1, total // 2)
    return sorted({max(1, mid - 1), mid, min(total, mid + 1)})


def select_review_pages(entries: list[dict], limit: int = 6) -> list[int]:
    pages = [item["page"] for item in entries if item["quality_flag"] in {"review", "empty", "error"}]
    return pages[:limit]


def select_question_pages(entries: list[dict], limit: int = 4) -> list[int]:
    pages = [item["page"] for item in entries if item.get("contains_question_pattern")]
    return pages[:limit]


def write_quality_report() -> None:
    rows = []
    samples = []
    review_lines = ["# 需人工/多模态复核页清单", ""]

    for doc in DOCS:
        slug = doc["slug"]
        index_path = PAGES_ROOT / slug / "pages_index.json"
        entries = load_json(index_path)
        total = len(entries)
        success = sum(1 for item in entries if item["quality_flag"] == "ok")
        low = sum(1 for item in entries if item["quality_flag"] == "review")
        empty = sum(1 for item in entries if item["quality_flag"] == "empty")
        avg_chars = round(statistics.mean(item["char_count"] for item in entries), 2) if entries else 0
        rows.append((doc["name"], total, success, low, empty, avg_chars, "按页 OCR 与页级质量标记已生成"))

        sample_pages = []
        sample_pages.extend(list(range(1, min(5, total) + 1)))
        sample_pages.extend(pick_middle_pages(total))
        sample_pages.extend(range(max(1, total - 4), total + 1))
        sample_pages.extend(select_question_pages(entries))
        sample_pages.extend(select_review_pages(entries))
        seen = set()
        deduped_pages = []
        for page in sample_pages:
            if 1 <= page <= total and page not in seen:
                seen.add(page)
                deduped_pages.append(page)

        samples.append(f"## {doc['name']}")
        for page in deduped_pages:
            entry = entries[page - 1]
            text = read_page_text(slug, page)
            samples.append(f"### {slug} page_{page:03d}")
            samples.append(f"- 字符数：{entry['char_count']}")
            samples.append(f"- 非空白字符数：{entry['non_whitespace_count']}")
            samples.append(f"- 中文比例：{entry['chinese_ratio']}")
            samples.append(f"- 是否识别题号/题目模式：{'是' if entry['contains_question_pattern'] else '否'}")
            samples.append(f"- 质量判断：`{entry['quality_flag']}`")
            samples.append(f"- 问题：{entry['notes'] or '无明显规则触发'}")
            samples.append(f"- 主要识别内容：{preview(text)}")
            samples.append("")

        review_lines.append(f"## {doc['name']}")
        flagged = [item for item in entries if item["quality_flag"] in {"review", "empty", "error"}]
        if not flagged:
            review_lines.append("- 无规则命中的低质量页")
        else:
            for item in flagged:
                note = item["notes"] or "规则命中但无补充说明"
                review_lines.append(f"- page_{item['page']:03d}：{note}")
        review_lines.append("")

    report_lines = [
        "# OCR 质量报告",
        "",
        "## 总体统计",
        "",
        "| 文件 | 页数 | 成功 OCR 页 | 低质量页 | 空文本页 | 平均字符数 | 备注 |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        report_lines.append(
            f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} |"
        )
    report_lines.extend(
        [
            "",
            "## 质量规则",
            "",
            "- `empty`：页面 OCR 文本去空白后长度为 0。",
            "- `review`：非空白字符过少（<40 记为 `very_low_text`，<120 记为 `low_text`）、中文比例过低（<0.05）、或异常符号比例过高（>0.18）。",
            "- `ok`：未命中上述规则，但仍不代表完全无误；图表、表格、公式页依旧建议抽检。",
            "- `contains_question_pattern`：通过 `(1)`、`A.`、`答案`、`解析` 等模式粗判题目页，用于历年题抽样。",
            "",
            "## 抽样检查",
            "",
        ]
    )
    report_lines.extend(samples)
    (REPORTS_ROOT / "02_ocr_quality_report.md").write_text("\n".join(report_lines), encoding="utf-8")
    (REVIEW_ROOT / "low_quality_pages.md").write_text("\n".join(review_lines), encoding="utf-8")


if __name__ == "__main__":
    write_quality_report()
