#!/usr/bin/env python3
"""Export ruankao topic learning package Markdown files to readable PDFs.

The script intentionally keeps dependencies light. It renders Markdown to a
self-contained-ish HTML page and asks Chrome headless to print that page to PDF.
Mermaid diagrams are rendered in the browser through Mermaid's CDN runtime.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List, Optional


MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"


@dataclass
class ExportResult:
    source: str
    target: str
    status: str
    reason: str = ""
    mermaid_blocks: int = 0


@dataclass
class Preflight:
    tools: dict = field(default_factory=dict)
    fonts: List[str] = field(default_factory=list)
    chrome: Optional[str] = None
    python: str = sys.version.split()[0]
    mermaid_mode: str = "browser_mermaid_cdn"


def run_command(cmd: List[str], cwd: Optional[Path] = None, timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, capture_output=True, timeout=timeout)


def which(name: str) -> Optional[str]:
    return shutil.which(name)


def find_chrome() -> Optional[str]:
    candidates = [
        which("google-chrome"),
        which("chromium"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ]
    for item in candidates:
        if item and Path(item).exists():
            return item
    return None


def collect_preflight() -> Preflight:
    pf = Preflight()
    for tool in ["pandoc", "xelatex", "wkhtmltopdf", "weasyprint", "node", "npx", "mmdc"]:
        pf.tools[tool] = which(tool) or "not found"
    pf.chrome = find_chrome()
    try:
        fc = run_command(["fc-list"], timeout=20)
        if fc.returncode == 0:
            for line in fc.stdout.splitlines():
                if re.search(r"Noto|Source Han|SimSun|Microsoft YaHei|PingFang|Songti|Heiti|STSong|STHeiti", line, re.I):
                    pf.fonts.append(line)
                if len(pf.fonts) >= 20:
                    break
    except Exception:
        pass
    return pf


def write_preflight_report(pf: Preflight, output: Path) -> None:
    reports = output / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    lines = [
        "# PDF 导出环境探测",
        "",
        f"> 生成脚本：`scripts/export_topic_packages_to_pdf.py`",
        "",
        "## 工具探测",
        "",
        "| 工具 | 路径/状态 |",
        "|---|---|",
    ]
    for k, v in pf.tools.items():
        lines.append(f"| `{k}` | `{v}` |")
    lines.extend(
        [
            f"| `chrome_headless` | `{pf.chrome or 'not found'}` |",
            f"| `python` | `{pf.python}` |",
            "",
            "## 中文字体候选",
            "",
        ]
    )
    if pf.fonts:
        lines.extend([f"- `{item}`" for item in pf.fonts])
    else:
        lines.append("- 未通过 `fc-list` 探测到明确中文字体；PDF CSS 将使用系统中文字体回退。")
    lines.extend(
        [
            "",
            "## 采用路线",
            "",
            "- 当前环境未发现 Pandoc/XeLaTeX、wkhtmltopdf、weasyprint 或 mmdc。",
            "- 实际采用：Markdown → HTML → Chrome headless print-to-pdf。",
            "- 中文字体处理：脚本通过 `@font-face` 强制加载 `/System/Library/Fonts/STHeiti Light.ttc`、`/System/Library/Fonts/STHeiti Medium.ttc` 和 `/System/Library/Fonts/Supplemental/Songti.ttc`，避免 Chrome headless 默认字体导致的中文正文缺失问题。",
            f"- Mermaid 处理：浏览器端加载 `{MERMAID_CDN}` 渲染，Chrome 使用 `--virtual-time-budget` 等待渲染。",
            "",
        ]
    )
    (reports / "pdf_export_preflight.md").write_text("\n".join(lines), encoding="utf-8")


def slug_pdf_name(md: Path) -> str:
    return md.with_suffix(".pdf").name


def inline_markdown(text: str) -> str:
    placeholders = []

    def keep_code(match: re.Match) -> str:
        placeholders.append(f"<code>{html.escape(match.group(1))}</code>")
        return f"@@CODE{len(placeholders)-1}@@"

    text = re.sub(r"`([^`]+)`", keep_code, html.escape(text))
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<span class="image-ref">[图片：\1]</span>', text)
    for i, value in enumerate(placeholders):
        text = text.replace(f"@@CODE{i}@@", value)
    return text


def parse_table(lines: List[str]) -> str:
    rows = []
    for line in lines:
        stripped = line.strip().strip("|")
        rows.append([cell.strip() for cell in stripped.split("|")])
    header = rows[0] if rows else []
    body = rows[2:] if len(rows) >= 2 and re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", lines[1]) else rows[1:]
    out = ["<div class=\"table-wrap\"><table>"]
    if header:
        out.append("<thead><tr>" + "".join(f"<th>{inline_markdown(c)}</th>" for c in header) + "</tr></thead>")
    if body:
        out.append("<tbody>")
        for row in body:
            if len(row) < len(header):
                row += [""] * (len(header) - len(row))
            out.append("<tr>" + "".join(f"<td>{inline_markdown(c)}</td>" for c in row[: len(header) or len(row)]) + "</tr>")
        out.append("</tbody>")
    out.append("</table></div>")
    return "\n".join(out)


def markdown_to_html(markdown_text: str) -> tuple[str, int]:
    lines = markdown_text.splitlines()
    out: List[str] = []
    i = 0
    mermaid_count = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue

        fence = re.match(r"^```(\w+)?\s*$", stripped)
        if fence:
            lang = fence.group(1) or ""
            block: List[str] = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            i += 1
            code = "\n".join(block)
            if lang.lower() == "mermaid":
                mermaid_count += 1
                out.append(f"<div class=\"mermaid\">{html.escape(code)}</div>")
            else:
                out.append(f"<pre><code>{html.escape(code)}</code></pre>")
            continue

        if re.match(r"^\s*\|.+\|\s*$", line) and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{3,}", lines[i + 1]):
            table_lines = [line, lines[i + 1]]
            i += 2
            while i < len(lines) and re.match(r"^\s*\|.+\|\s*$", lines[i]):
                table_lines.append(lines[i])
                i += 1
            out.append(parse_table(table_lines))
            continue

        h = re.match(r"^(#{1,6})\s+(.+)$", line)
        if h:
            level = len(h.group(1))
            out.append(f"<h{level}>{inline_markdown(h.group(2))}</h{level}>")
            i += 1
            continue

        if stripped.startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i].strip()[1:].strip())
                i += 1
            out.append("<blockquote>" + "\n".join(f"<p>{inline_markdown(q)}</p>" for q in quote_lines if q) + "</blockquote>")
            continue

        if re.match(r"^\s*[-*]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]))
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline_markdown(x)}</li>" for x in items) + "</ul>")
            continue

        if re.match(r"^\s*\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i]))
                i += 1
            out.append("<ol>" + "".join(f"<li>{inline_markdown(x)}</li>" for x in items) + "</ol>")
            continue

        para = [line.strip()]
        i += 1
        while i < len(lines):
            nxt = lines[i]
            if not nxt.strip() or nxt.strip().startswith(("```", ">", "#")):
                break
            if re.match(r"^\s*(?:[-*]|\d+\.)\s+", nxt) or re.match(r"^\s*\|.+\|\s*$", nxt):
                break
            para.append(nxt.strip())
            i += 1
        out.append(f"<p>{inline_markdown(' '.join(para))}</p>")

    return "\n".join(out), mermaid_count


def html_page(title: str, body: str) -> str:
    css = """
    @font-face {
      font-family: 'RuankaoSongti';
      src: url('file:///System/Library/Fonts/Supplemental/Songti.ttc') format('truetype');
      font-weight: 400;
    }
    @font-face {
      font-family: 'RuankaoHeiti';
      src: url('file:///System/Library/Fonts/STHeiti Light.ttc') format('truetype');
      font-weight: 400;
    }
    @font-face {
      font-family: 'RuankaoHeiti';
      src: url('file:///System/Library/Fonts/STHeiti Medium.ttc') format('truetype');
      font-weight: 700;
    }
    @page { size: A4; margin: 18mm 16mm; }
    body {
      font-family: 'RuankaoHeiti', 'RuankaoSongti', "STHeiti", "Songti SC", "STSong", sans-serif;
      font-size: 14px;
      line-height: 1.72;
      color: #202124;
      background: #fff;
    }
    h1, h2, h3, h4 {
      font-family: 'RuankaoHeiti', 'RuankaoSongti', "STHeiti", sans-serif;
      line-height: 1.28;
      page-break-after: avoid;
    }
    h1 { font-size: 30px; border-bottom: 2px solid #222; padding-bottom: 8px; }
    h2 { font-size: 22px; margin-top: 30px; border-bottom: 1px solid #ddd; padding-bottom: 4px; }
    h3 { font-size: 18px; margin-top: 24px; }
    h4 { font-size: 16px; margin-top: 20px; }
    p { margin: 10px 0; }
    blockquote {
      border-left: 4px solid #4c78a8;
      margin: 14px 0;
      padding: 8px 14px;
      background: #f6f8fa;
      color: #30363d;
      break-inside: avoid;
    }
    code {
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
      background: #f1f3f4;
      padding: 1px 4px;
      border-radius: 3px;
      font-size: 0.92em;
    }
    pre {
      background: #f6f8fa;
      border: 1px solid #d0d7de;
      border-radius: 6px;
      padding: 12px;
      overflow-wrap: anywhere;
      white-space: pre-wrap;
      break-inside: avoid;
    }
    pre code { background: transparent; padding: 0; }
    .table-wrap { overflow-x: hidden; margin: 14px 0; }
    table {
      border-collapse: collapse;
      width: 100%;
      table-layout: auto;
      font-size: 12px;
      break-inside: auto;
    }
    th, td {
      border: 1px solid #d0d7de;
      padding: 5px 7px;
      vertical-align: top;
      word-break: break-word;
    }
    th { background: #eef2f7; font-weight: 700; }
    .mermaid {
      font-family: 'RuankaoSongti', 'RuankaoHeiti', serif;
      text-align: center;
      margin: 18px auto;
      padding: 10px;
      border: 1px solid #e5e7eb;
      border-radius: 8px;
      background: #fff;
      break-inside: avoid;
      max-width: 100%;
    }
    .mermaid svg, .mermaid svg * {
      font-family: 'RuankaoSongti', 'RuankaoHeiti', serif !important;
    }
    .mermaid svg { max-width: 100%; height: auto; }
    a { color: #1a73e8; text-decoration: none; }
    .image-ref { color: #6a737d; }
    """
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{css}</style>
</head>
<body>
{body}
<script src="{MERMAID_CDN}"></script>
<script>
window.addEventListener('load', async () => {{
  if (window.mermaid) {{
    mermaid.initialize({{ startOnLoad: false, securityLevel: 'loose', theme: 'default' }});
    await mermaid.run({{ querySelector: '.mermaid' }});
  }}
  document.body.setAttribute('data-rendered', 'true');
}});
</script>
</body>
</html>
"""


def export_one(chrome: str, md: Path, pdf: Path, html_out: Path, source_root: Path) -> ExportResult:
    text = md.read_text(encoding="utf-8")
    body, mermaid_count = markdown_to_html(text)
    title_match = re.search(r"^#\s+(.+)$", text, re.M)
    title = title_match.group(1) if title_match else md.stem
    html_out.parent.mkdir(parents=True, exist_ok=True)
    pdf.parent.mkdir(parents=True, exist_ok=True)
    html_out.write_text(html_page(title, body), encoding="utf-8")

    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        "--allow-file-access-from-files",
        "--print-to-pdf-no-header",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=10000",
        f"--print-to-pdf={pdf}",
        html_out.resolve().as_uri(),
    ]
    proc = run_command(cmd, timeout=90)
    if proc.returncode != 0 or not pdf.exists() or pdf.stat().st_size == 0:
        return ExportResult(str(md), str(pdf), "failed", (proc.stderr or proc.stdout or "Chrome did not create PDF").strip(), mermaid_count)
    return ExportResult(str(md), str(pdf), "success", "", mermaid_count)


def discover_markdown(source: Path, include_topics: bool, include_index: bool, include_reports: bool) -> List[Path]:
    files: List[Path] = []
    if include_topics:
        files.extend(sorted((source / "topics").glob("**/*.md")))
    if include_index:
        for name in ["README.md"]:
            p = source / name
            if p.exists():
                files.append(p)
        files.extend(sorted((source / "index").glob("*.md")))
    if include_reports:
        files.extend(sorted((source / "reports").glob("*.md")))
    return files


def output_pdf_path(md: Path, source: Path, output: Path) -> Path:
    rel = md.relative_to(source)
    if rel.parts[0] == "README.md":
        return output / "README.pdf"
    return (output / rel).with_suffix(".pdf")


def output_html_path(md: Path, source: Path, output: Path) -> Path:
    rel = md.relative_to(source)
    return (output / "_html" / rel).with_suffix(".html")


def write_readme(output: Path, results: List[ExportResult]) -> None:
    ok = sum(1 for r in results if r.status == "success")
    lines = [
        "# 专题学习包 PDF 导出目录",
        "",
        f"- PDF 生成数量：{ok}/{len(results)}",
        "- `topics/`：正式专题 PDF，目录结构镜像 `topic_learning_packages/topics/`。",
        "- `index/`：导航、manifest、覆盖矩阵等 PDF。",
        "- `reports/`：环境探测与导出报告。",
        "- `_html/`：导出 PDF 前的 HTML 中间产物，用于人工排版复核。",
        "",
        "如需重新导出：",
        "",
        "```bash",
        "python scripts/export_topic_packages_to_pdf.py --source topic_learning_packages --output topic_learning_packages_pdf --include-topics --include-index",
        "```",
        "",
    ]
    (output / "README.md").write_text("\n".join(lines), encoding="utf-8")


def write_export_report(output: Path, source: Path, results: List[ExportResult], pf: Preflight, study_plan: Optional[Path] = None, anki_report: Optional[Path] = None) -> None:
    ok = [r for r in results if r.status == "success"]
    failed = [r for r in results if r.status != "success"]
    mermaid_total = sum(r.mermaid_blocks for r in results)
    lines = [
        "# 本轮交付总结",
        "",
        "## 1. PDF 导出结果",
        "",
        f"- 扫描 Markdown 数量：{len(results)}",
        f"- 成功生成 PDF 数量：{len(ok)}",
        f"- 失败数量：{len(failed)}",
        f"- 使用的导出工具：Chrome headless (`{pf.chrome or 'not found'}`)",
        "- 中文字体：强制加载 macOS `STHeiti` 与 `Songti.ttc`，避免 Chrome headless 中文正文缺字",
        f"- Mermaid 处理方式：浏览器端 Mermaid CDN 渲染，累计 Mermaid 代码块 {mermaid_total} 个",
        "",
        "### 失败文件列表",
        "",
    ]
    if failed:
        for item in failed:
            lines.append(f"- `{item.source}` → `{item.target}`：{item.reason}")
    else:
        lines.append("- 无")
    lines.extend(
        [
            "",
            "## 2. 学习路线",
            "",
            f"- 输出文件：`{study_plan or 'topic_learning_packages/study_plan/学习路线与打卡TODO.md'}`",
            "- 覆盖阶段：准备与总览、项目管理主线、计算题专项、下午案例专项、上午零散考点补漏、真题回流与复盘",
            "- TODO 数量：见学习路线文件中的复选框",
            "- 建议使用方式：按阶段打卡，错题回流到专题和零散题库，待核验点不直接制成稳定记忆卡",
            "",
            "## 3. Anki 试制",
            "",
        ]
    )
    if anki_report and Path(anki_report).exists():
        lines.append(f"- 详见：`{anki_report}`")
    else:
        lines.append("- 尚未写入 Anki 试制报告。")
    lines.extend(
        [
            "",
            "## 4. 后续建议",
            "",
            "- PDF 导出流程在当前环境下可复用；若后续需要离线 Mermaid，可安装 `mmdc` 并扩展脚本。",
            "- 建议人工抽查表格较宽、公式较多、Mermaid 图较多的 PDF。",
            "- Anki 试制通过后，再扩展到全量专题；扩展前先处理高优先级 `[待核验]`。",
            "",
        ]
    )
    (output / "export_report.md").write_text("\n".join(lines), encoding="utf-8")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="topic_learning_packages")
    parser.add_argument("--output", default="topic_learning_packages_pdf")
    parser.add_argument("--include-topics", action="store_true")
    parser.add_argument("--include-index", action="store_true")
    parser.add_argument("--include-reports", action="store_true")
    args = parser.parse_args(argv)

    source = Path(args.source)
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    pf = collect_preflight()
    write_preflight_report(pf, output)

    files = discover_markdown(source, args.include_topics, args.include_index, args.include_reports)
    if not files:
        print("No markdown files selected.", file=sys.stderr)
        return 2
    if not pf.chrome:
        results = [ExportResult(str(f), str(output_pdf_path(f, source, output)), "failed", "Chrome headless not found", 0) for f in files]
        write_readme(output, results)
        write_export_report(output, source, results, pf)
        return 3

    results: List[ExportResult] = []
    for md in files:
        pdf = output_pdf_path(md, source, output)
        html_file = output_html_path(md, source, output)
        try:
            result = export_one(pf.chrome, md, pdf, html_file, source)
        except Exception as exc:
            result = ExportResult(str(md), str(pdf), "failed", repr(exc), 0)
        results.append(result)
        print(f"{result.status}: {md} -> {pdf}")

    write_readme(output, results)
    write_export_report(output, source, results, pf)
    return 1 if any(r.status != "success" for r in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
