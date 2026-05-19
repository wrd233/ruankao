#!/usr/bin/env python3
"""Build markdown reports for the OCR remediation pass."""

from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[3]
OCR_ROOT = ROOT / "outputs" / "ocr"
PAGES_ROOT = OCR_ROOT / "pages"
REPORTS_ROOT = OCR_ROOT / "reports"
LOGS_ROOT = OCR_ROOT / "logs"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(slug: str, page: int) -> str:
    return (PAGES_ROOT / slug / f"page_{page:03d}.txt").read_text(encoding="utf-8")


def preview(text: str, limit: int = 180) -> str:
    return re.sub(r"\s+", " ", text).strip()[:limit]


def stats(slug: str) -> tuple[list[dict], dict]:
    pages = load_json(PAGES_ROOT / slug / "pages_index.json")
    summary = load_json(PAGES_ROOT / slug / "run_summary.json")
    return pages, summary


def chapter_starts() -> list[tuple[int, str]]:
    starts: list[tuple[int, str]] = []
    seen = set()
    for page in range(1, 679):
        first = next((line.strip() for line in read_text("official_tutorial", page).splitlines() if line.strip()), "")
        match = re.match(r"第\s*(\d+)\s*章\s*(.+)", first)
        if not match:
            continue
        chapter_no = int(match.group(1))
        if chapter_no in seen:
            continue
        title = re.sub(r"[“”\"'`·,.，。:：;；\d]+$", "", match.group(2)).strip()
        title = re.sub(r"\s+", "", title)
        starts.append((page, f"第{chapter_no}章 {title}"))
        seen.add(chapter_no)
    return starts


def write_manifest() -> None:
    official_pages, _ = stats("official_tutorial")
    past_pages, _ = stats("past_papers_171")
    manifest = dedent(
        f"""
        # OCR 专项工作清单

        ## 目标 PDF
        | 编号 | 文件名 | 路径 | 页数 | 当前文本层情况 | 上轮缺口说明 |
        |---|---|---|---:|---|---|
        | PDF-01 | 《系统集成项目管理工程师教程》官方考试指定第二版.pdf | `./《系统集成项目管理工程师教程》官方考试指定第二版.pdf` | {len(official_pages)} | 原始 PDF 抽样页 `get_text()` 全为 0；已补生成 `outputs/ocr/pdf/官方教程_ocr.pdf` 与页级文本 | 上轮未能提取正文，缺少官方教材页级索引与权威引用锚点 |
        | PDF-02 | 历年系统集成项目管理工程师试题解析及答案-171页.pdf | `./历年系统集成项目管理工程师试题解析及答案-171页.pdf` | {len(past_pages)} | 原始 PDF 抽样页 `get_text()` 全为 0；已补生成 `outputs/ocr/pdf/历年题解析_171页_ocr.pdf` 与页级文本 | 上轮未能稳定 OCR，缺少更大覆盖面的真题题号、选项、解析映射 |

        ## OCR 工具环境
        | 工具 | 是否可用 | 版本 | 备注 |
        |---|---|---|---|
        | ocrmypdf | 是 | 15.4.4 | 运行于 `outputs/ocr/.venv`；样本可生成 PDF/A，但文本抽取稳定性不足 |
        | tesseract | 是 | 5.5.2 | Homebrew 安装 |
        | tesseract chi_sim | 是 | `chi_sim.traineddata` | 下载到 `outputs/ocr/tessdata/` |
        | pdftotext | 否 | - | 本机无该命令 |
        | python | 是 | 3.9.6 | OCR 脚本运行环境 |
        | pymupdf/fitz | 是 | 1.26.5 | 用于渲染页面与文本抽样 |
        | pdf2image | 是 | 1.17.0 | 已装，最终主流程未采用 |
        | pytesseract | 是 | 0.3.13 | 当前主 OCR 方案 |
        | paddleocr | 否 | - | 当前环境未安装，未强行改动系统 |

        ## 本轮计划
        - 第一阶段：核验目标 PDF、工具环境、文本层现状，并将命令输出落盘到 `outputs/ocr/logs/tool_check.log`。
        - 第二阶段：先试 `ocrmypdf + tesseract` 样本，再试 `PyMuPDF + pytesseract` 样本，比较是否能稳定得到可用文本与 OCR PDF。
        - 第三阶段：采用可重复的 Python 页级 OCR 流水线全量处理两份 PDF，输出 OCR PDF、页级文本、质量评估、复核页清单与索引补强报告。
        """
    ).strip() + "\n"
    (REPORTS_ROOT / "00_ocr_work_manifest.md").write_text(manifest, encoding="utf-8")


def write_attempt_log() -> None:
    attempts = dedent(
        """
        # OCR 尝试日志

        ## Attempt 001｜环境核验：基础 OCR 工具检查

        - **时间**：2026-05-19
        - **目标文件**：工具环境
        - **命令**：

        ```bash
        which ocrmypdf || true
        ocrmypdf --version || true
        which tesseract || true
        tesseract --version || true
        tesseract --list-langs || true
        which pdftotext || true
        pdftotext -v || true
        python3 --version || true
        ```

        - **退出码**：0
        - **耗时**：< 1 min
        - **输出文件**：`outputs/ocr/logs/tool_check.log`
        - **日志文件**：`outputs/ocr/logs/tool_check.log`
        - **结果判断**：
          - 部分成功
        - **失败原因或警告**：
          - 初始环境无 `ocrmypdf`、`pdftotext`、`pdfinfo`
          - `tesseract` 初始仅有 `eng/osd/snum`，缺少 `chi_sim`
          - Python 初始无 `fitz`、`pytesseract`、`pdf2image`
        - **下一步处理**：
          - 建立隔离虚拟环境并补本地依赖与中文语言包

        ## Attempt 002｜本地依赖准备：venv + OCR 栈安装

        - **时间**：2026-05-19
        - **目标文件**：OCR 运行环境
        - **命令**：

        ```bash
        python3 -m venv outputs/ocr/.venv
        source outputs/ocr/.venv/bin/activate
        python -m pip install --upgrade pip setuptools wheel
        python -m pip install pymupdf pytesseract pypdf ocrmypdf pdf2image
        ```

        - **退出码**：0
        - **耗时**：约 3 min
        - **输出文件**：`outputs/ocr/.venv/`
        - **日志文件**：
          - `outputs/ocr/logs/pip_upgrade.log`
          - `outputs/ocr/logs/pip_install_ocr_stack.log`
        - **结果判断**：
          - 成功
        - **失败原因或警告**：
          - 无
        - **下一步处理**：
          - 下载本地 `chi_sim` / `chi_sim_vert` 语言包并复检环境

        ## Attempt 003｜语言包补强：chi_sim / chi_sim_vert

        - **时间**：2026-05-19
        - **目标文件**：本地 tessdata
        - **命令**：

        ```bash
        curl -L https://github.com/tesseract-ocr/tessdata_best/raw/main/chi_sim.traineddata -o outputs/ocr/tessdata/chi_sim.traineddata
        curl -L https://github.com/tesseract-ocr/tessdata_best/raw/main/chi_sim_vert.traineddata -o outputs/ocr/tessdata/chi_sim_vert.traineddata
        ```

        - **退出码**：0
        - **耗时**：约 1 min
        - **输出文件**：`outputs/ocr/tessdata/`
        - **日志文件**：
          - `outputs/ocr/logs/download_chi_sim.log`
          - `outputs/ocr/logs/download_chi_sim_vert.log`
        - **结果判断**：
          - 成功
        - **失败原因或警告**：
          - 无
        - **下一步处理**：
          - 试跑 `ocrmypdf + tesseract`

        ## Attempt 004｜ocrmypdf 样本 OCR：历年题解析（Ghostscript 缺失）

        - **时间**：2026-05-19
        - **目标文件**：`历年系统集成项目管理工程师试题解析及答案-171页.pdf`
        - **命令**：

        ```bash
        source outputs/ocr/.venv/bin/activate
        export TESSDATA_PREFIX="/Users/wangrundong/work/软考/outputs/ocr/tessdata"
        ocrmypdf -l chi_sim+eng --deskew --rotate-pages --skip-text --pages 1-3 \
          "历年系统集成项目管理工程师试题解析及答案-171页.pdf" \
          "outputs/ocr/pdf/past_papers_171_sample_ocr.pdf"
        ```

        - **退出码**：3
        - **耗时**：0.20 s
        - **输出文件**：未生成可用 PDF
        - **日志文件**：`outputs/ocr/logs/attempt_ocrmypdf_past_papers_sample.log`
        - **结果判断**：
          - 失败
        - **失败原因或警告**：
          - `gs` 不存在，`ocrmypdf` 直接退出
        - **下一步处理**：
          - 安装 Ghostscript 后重试

        ## Attempt 005｜系统依赖补充：Ghostscript

        - **时间**：2026-05-19
        - **目标文件**：OCR 系统依赖
        - **命令**：

        ```bash
        brew install ghostscript
        ```

        - **退出码**：0
        - **耗时**：约 4 min
        - **输出文件**：系统命令 `gs`
        - **日志文件**：`outputs/ocr/logs/brew_install_ghostscript.log`
        - **结果判断**：
          - 成功
        - **失败原因或警告**：
          - 无
        - **下一步处理**：
          - 重试 `ocrmypdf` 样本

        ## Attempt 006｜ocrmypdf 样本 OCR：历年题解析（成功生成 PDF/A）

        - **时间**：2026-05-19
        - **目标文件**：`历年系统集成项目管理工程师试题解析及答案-171页.pdf`
        - **命令**：

        ```bash
        source outputs/ocr/.venv/bin/activate
        export TESSDATA_PREFIX="/Users/wangrundong/work/软考/outputs/ocr/tessdata"
        ocrmypdf -l chi_sim+eng --deskew --rotate-pages --skip-text --pages 1-3 \
          "历年系统集成项目管理工程师试题解析及答案-171页.pdf" \
          "outputs/ocr/pdf/past_papers_171_sample_ocr.pdf"
        ```

        - **退出码**：0
        - **耗时**：18.50 s
        - **输出文件**：`outputs/ocr/pdf/past_papers_171_sample_ocr.pdf`
        - **日志文件**：`outputs/ocr/logs/attempt_ocrmypdf_past_papers_sample.log`
        - **结果判断**：
          - 部分成功
        - **失败原因或警告**：
          - PDF/A 成功生成，但随后用 `PyMuPDF` / `pypdf` 抽取文本层时得到 0 字符，无法作为稳定的后续引用基础
        - **下一步处理**：
          - 继续试跑官方教程样本，并同时准备 Python 页级 OCR 备用方案

        ## Attempt 007｜ocrmypdf 样本 OCR：官方教程（成功生成 PDF/A）

        - **时间**：2026-05-19
        - **目标文件**：`《系统集成项目管理工程师教程》官方考试指定第二版.pdf`
        - **命令**：

        ```bash
        source outputs/ocr/.venv/bin/activate
        export TESSDATA_PREFIX="/Users/wangrundong/work/软考/outputs/ocr/tessdata"
        ocrmypdf -l chi_sim+eng --deskew --rotate-pages --skip-text --pages 1-3 \
          "《系统集成项目管理工程师教程》官方考试指定第二版.pdf" \
          "outputs/ocr/pdf/official_tutorial_sample_ocr.pdf"
        ```

        - **退出码**：0
        - **耗时**：16.64 s
        - **输出文件**：`outputs/ocr/pdf/official_tutorial_sample_ocr.pdf`
        - **日志文件**：`outputs/ocr/logs/attempt_ocrmypdf_official_sample.log`
        - **结果判断**：
          - 部分成功
        - **失败原因或警告**：
          - 样本 OCR PDF 成功生成，但抽取文本层仍不稳定，无法作为正式页级索引来源
        - **下一步处理**：
          - 转为 `PyMuPDF + pytesseract` 主流程

        ## Attempt 008｜PyMuPDF + pytesseract 样本 OCR：两份 PDF 抽样页

        - **时间**：2026-05-19
        - **目标文件**：
          - `《系统集成项目管理工程师教程》官方考试指定第二版.pdf`
          - `历年系统集成项目管理工程师试题解析及答案-171页.pdf`
        - **命令**：

        ```bash
        source outputs/ocr/.venv/bin/activate
        python - <<'PY'
        # 渲染 page 1-3 / page 34，使用 pytesseract.image_to_string(lang="chi_sim+eng")
        PY
        ```

        - **退出码**：0
        - **耗时**：约 13 s
        - **输出文件**：
          - `outputs/ocr/logs/sample_texts/official_sample.txt`
          - `outputs/ocr/logs/sample_texts/past_sample.txt`
        - **日志文件**：上述样本文本文件
        - **结果判断**：
          - 成功
        - **失败原因或警告**：
          - 封面、图示与少量字符有误识别
        - **下一步处理**：
          - 将该路线写成可重复运行脚本，并在页级保留质量标记

        ## Attempt 009｜Python OCR 流水线样本：官方教程 / 历年题解析

        - **时间**：2026-05-19
        - **目标文件**：两份 PDF 的前 3 页
        - **命令**：

        ```bash
        source outputs/ocr/.venv/bin/activate
        python outputs/ocr/scripts/ocr_scan_pdfs.py --pdf "《系统集成项目管理工程师教程》官方考试指定第二版.pdf" --slug official_tutorial_sample_pipeline --output-pdf-name official_tutorial_sample_pipeline.pdf --start-page 1 --end-page 3
        python outputs/ocr/scripts/ocr_scan_pdfs.py --pdf "历年系统集成项目管理工程师试题解析及答案-171页.pdf" --slug past_papers_171_sample_pipeline --output-pdf-name past_papers_171_sample_pipeline.pdf --start-page 1 --end-page 3
        ```

        - **退出码**：0
        - **耗时**：
          - 官方教程样本：33.00 s
          - 历年题样本：31.92 s
        - **输出文件**：
          - `outputs/ocr/pages/official_tutorial_sample_pipeline/`
          - `outputs/ocr/pages/past_papers_171_sample_pipeline/`
        - **日志文件**：
          - `outputs/ocr/logs/attempt_python_pipeline_official_sample.log`
          - `outputs/ocr/logs/attempt_python_pipeline_past_sample.log`
        - **结果判断**：
          - 成功
        - **失败原因或警告**：
          - 生成的 OCR PDF 仍不适合作为唯一文本来源，因此页级 `.txt` 保持为权威产物
        - **下一步处理**：
          - 全量跑两份 PDF

        ## Attempt 010｜Python OCR 全量：历年题解析 171 页

        - **时间**：2026-05-19
        - **目标文件**：`历年系统集成项目管理工程师试题解析及答案-171页.pdf`
        - **命令**：

        ```bash
        source outputs/ocr/.venv/bin/activate
        python outputs/ocr/scripts/ocr_scan_pdfs.py \
          --pdf "历年系统集成项目管理工程师试题解析及答案-171页.pdf" \
          --slug past_papers_171 \
          --output-pdf-name 历年题解析_171页_ocr.pdf
        ```

        - **退出码**：0
        - **耗时**：727.40 s
        - **输出文件**：
          - `outputs/ocr/pdf/历年题解析_171页_ocr.pdf`
          - `outputs/ocr/pages/past_papers_171/`
        - **日志文件**：`outputs/ocr/logs/attempt_python_pipeline_past_full.log`
        - **结果判断**：
          - 成功
        - **失败原因或警告**：
          - 3 页 `review`、3 页 `empty`，已进入复核队列
        - **下一步处理**：
          - 全量跑官方教程并统一做质量评估

        ## Attempt 011｜Python OCR 全量：官方教程 678 页

        - **时间**：2026-05-19
        - **目标文件**：`《系统集成项目管理工程师教程》官方考试指定第二版.pdf`
        - **命令**：

        ```bash
        source outputs/ocr/.venv/bin/activate
        python outputs/ocr/scripts/ocr_scan_pdfs.py \
          --pdf "《系统集成项目管理工程师教程》官方考试指定第二版.pdf" \
          --slug official_tutorial \
          --output-pdf-name 官方教程_ocr.pdf
        ```

        - **退出码**：0
        - **耗时**：1939.45 s
        - **输出文件**：
          - `outputs/ocr/pdf/官方教程_ocr.pdf`
          - `outputs/ocr/pages/official_tutorial/`
        - **日志文件**：`outputs/ocr/logs/attempt_python_pipeline_official_full.log`
        - **结果判断**：
          - 成功
        - **失败原因或警告**：
          - 2 页 `review`、1 页 `empty`，已进入复核队列
        - **下一步处理**：
          - 生成质量报告、补强索引与质量更新
        """
    ).strip() + "\n"
    (REPORTS_ROOT / "01_ocr_attempt_log.md").write_text(attempts, encoding="utf-8")


def write_official_outline() -> None:
    starts = chapter_starts()
    key_pages = [2, 6, 15, 17, 21, 244, 264, 317, 351, 395, 565, 635]
    lines = [
        "# 官方教程 OCR 目录与可用章节索引",
        "",
        "## 可识别目录",
        "",
        "- `page_007` 至 `page_021` 基本可识别目录结构，能够恢复章节边界与大部分节号。",
        "- 目录样本：",
        f"  - `page_015`：{preview(read_text('official_tutorial', 15), 140)}",
        f"  - `page_017`：{preview(read_text('official_tutorial', 17), 140)}",
        f"  - `page_021`：{preview(read_text('official_tutorial', 21), 140)}",
        "",
        "### 章节起始页（按 OCR 实体页）",
        "",
    ]
    for page, title in starts:
        lines.append(f"- `{title}`：`page_{page:03d}.txt`")
    lines.extend(["", "## 可用章节片段", ""])
    for page in key_pages:
        lines.append(f"### official_tutorial page_{page:03d}")
        lines.append(f"- 摘要：{preview(read_text('official_tutorial', page), 220)}")
        lines.append("")
    lines.extend(
        [
            "## 对专题树的补强建议",
            "",
            "- 官方目录页已足以校准 `第 1–23 章` 的顺序与章节分布，可作为上一轮专题树章节边界的官方锚点。",
            "- `page_244` 左右的立项管理、`page_264` 左右的整体管理、`page_317` 左右的进度管理、`page_351` 左右的成本管理、`page_565` 左右的风险管理，适合补进高频专题的“权威来源页码”。",
            "- `page_635` 之后进入案例分析章节，可作为下午案例专题素材的官方背景来源，而不仅是题库材料。",
            "- `page_022`、`page_423`、`page_678` 需人工复核；其中 `page_022` 大概率为空白/分隔页，`page_423` 可能为截断条目，`page_678` 接近末页尾注。",
            "",
        ]
    )
    (REPORTS_ROOT / "official_tutorial_outline_from_ocr.md").write_text("\n".join(lines), encoding="utf-8")


def write_question_index() -> None:
    entries = [
        {
            "id": "OCR-Q-001",
            "page": 1,
            "title": "国家信息化体系六要素定位题",
            "main": "T-INFO-001",
            "related": "T-INFO-002",
            "answer": "A（从解析图示判断）",
        },
        {
            "id": "OCR-Q-002",
            "page": 2,
            "title": "ERP 物流模块与 CRM 定位题",
            "main": "T-INFO-002",
            "related": "T-INFO-001",
            "answer": "页内可识别解析，但建议人工核对选项字母",
        },
        {
            "id": "OCR-Q-003",
            "page": 3,
            "title": "开发模型与监理职责边界题",
            "main": "T-INFO-003",
            "related": "T-INFO-004",
            "answer": "监理题可识别为“评测单位不属于三方”；开发模型题可识别为瀑布模型",
        },
        {
            "id": "OCR-Q-004",
            "page": 9,
            "title": "WBS 描述错误项与范围确认题",
            "main": "T-SCOPE-002",
            "related": "T-SCOPE-003",
            "answer": "能识别题干与解析摘要，细节建议人工校对",
        },
        {
            "id": "OCR-Q-005",
            "page": 34,
            "title": "范围确认 / 资源平衡 / CPI 综合页",
            "main": "T-SCOPE-003",
            "related": "T-SCH-005、T-COST-002",
            "answer": "可识别“范围确认可能产生变更申请”“资源平衡不一定最优”“CPI=0.91 表示每 100 元仅创造 91 元价值”",
        },
        {
            "id": "OCR-Q-006",
            "page": 50,
            "title": "监理单位职责与信息管理题",
            "main": "T-INFO-003",
            "related": "T-CFG-001",
            "answer": "可识别监理例会/开工令保存等选项与解析摘要",
        },
        {
            "id": "OCR-Q-007",
            "page": 108,
            "title": "PMO 作用与组织级管理题",
            "main": "T-PM-003",
            "related": "T-INT-001",
            "answer": "可识别“企业可通过 PMO 实施组织级项目管理”",
        },
        {
            "id": "OCR-Q-008",
            "page": 152,
            "title": "范围确认定义、依据与方法题",
            "main": "T-SCOPE-003",
            "related": "T-QUAL-001",
            "answer": "定义、依据、方法均可识别，但仍建议人工核对术语细节",
        },
    ]
    lines = ["# 历年题解析 OCR 题目索引", ""]
    for item in entries:
        text = read_text("past_papers_171", item["page"])
        lines.append(f"## {item['id']}｜{item['title']}")
        lines.append("")
        lines.append(f"- **页码**：`page_{item['page']:03d}`")
        lines.append("- **题号**：同页包含 1 题或题组，需结合原页定位")
        lines.append(f"- **题干**：{preview(text, 220)}")
        lines.append("- **选项**：OCR 可识别出 A/B/C/D 结构，但个别字母与标点仍需人工校验")
        lines.append(f"- **答案**：{item['answer']}")
        lines.append(f"- **解析摘要**：{preview(text[120:], 220)}")
        lines.append(f"- **主专题映射**：`{item['main']}`")
        lines.append(f"- **关联专题**：{item['related']}")
        lines.append("- **OCR 质量**：中高；建议在纳入正式题库前人工复核答案字母与个别术语")
        lines.append("- **是否建议并入 04**：建议并入，但标记“需人工校验”")
        lines.append("")
    lines.extend(
        [
            "## 低质量题目页提醒",
            "",
            "- `page_014`：英语内容较多，命中 `low_chinese_ratio`，但并非无效页，适合单独人工复核。",
            "- `page_025`：文本过短，疑似截断页或图表页。",
            "- `page_084`、`page_093`、`page_171`：空页或封底类页面。",
            "- `page_086`：仅识别出极少字符，建议多模态复核。",
            "",
        ]
    )
    (REPORTS_ROOT / "past_papers_question_index_from_ocr.md").write_text("\n".join(lines), encoding="utf-8")


def write_index_supplement() -> None:
    lines = [
        "# OCR 后索引补强",
        "",
        "## 对 01_全资料细粒度索引与专题素材映射.md 的补充建议",
        "",
        "### A01-OCR-P002｜官方教程内容简介页",
        "- **来源**：A01 官方教程",
        "- **位置**：`outputs/ocr/pages/official_tutorial/page_002.txt`",
        "- **OCR 质量**：`ok`",
        "- **内容类型**：教材内容范围说明 / 权威边界页",
        f"- **核心内容摘要**：{preview(read_text('official_tutorial', 2), 220)}",
        "- **可服务专题**：`T-INFO-001`、`T-INT-001`、`T-SCOPE-001`、`T-SCH-001` 等全局专题",
        "- **素材用途**：用于证明官方教材覆盖信息化、整体/范围/进度/成本/质量/风险/收尾等章节，是专题树的权威总目录锚点",
        "- **是否建议并入 01**：是",
        "",
        "### A01-OCR-P015｜官方教程目录页组",
        "- **来源**：A01 官方教程",
        "- **位置**：`page_015`、`page_017`、`page_021`",
        "- **OCR 质量**：`ok`",
        "- **内容类型**：目录 / 章节边界",
        f"- **核心内容摘要**：{preview(read_text('official_tutorial', 15), 220)}",
        "- **可服务专题**：章节边界校准相关全部专题",
        "- **素材用途**：为上一轮专题树补齐官方章节顺序与案例章分布",
        "- **是否建议并入 01**：是",
        "",
        "### A01-OCR-P264｜整体管理起始页",
        "- **来源**：A01 官方教程",
        "- **位置**：`outputs/ocr/pages/official_tutorial/page_264.txt`",
        "- **OCR 质量**：`ok`",
        "- **内容类型**：章节起始页",
        f"- **核心内容摘要**：{preview(read_text('official_tutorial', 264), 200)}",
        "- **可服务专题**：`T-INT-001`、`T-INT-002`、`T-INT-003`、`T-INT-004`",
        "- **素材用途**：为整体管理专题补入官方页码锚点",
        "- **是否建议并入 01**：是",
        "",
        "### A01-OCR-P317｜进度管理起始页",
        "- **来源**：A01 官方教程",
        "- **位置**：`outputs/ocr/pages/official_tutorial/page_317.txt`",
        "- **OCR 质量**：`ok`",
        "- **内容类型**：章节起始页",
        f"- **核心内容摘要**：{preview(read_text('official_tutorial', 317), 200)}",
        "- **可服务专题**：`T-SCH-001` 至 `T-SCH-005`",
        "- **素材用途**：强化进度管理专题的官方教材入口引用",
        "- **是否建议并入 01**：是",
        "",
        "## 对 03_专题素材索引库.md 的补充建议",
        "",
        "### T-INFO-002｜ERP、CRM、SCM、EAI、BI 的对象、边界与常见混淆",
        "- 新增来源：`past_papers_171/page_002.txt`、`past_papers_171/page_022.txt`、`past_papers_171/page_057.txt`",
        "- 新增必须覆盖知识点：ERP 物流模块 vs 生产控制模块、CRM 定位、ERP 相比 MRP/MRP II 的边界扩展",
        "- 新增图示建议：企业管理系统谱系图（MRP -> MRP II -> ERP；CRM/SCM/BI 并列比较）",
        "- 新增典型题素材：`OCR-Q-002`",
        "- 是否改变专题重要度：是，建议提升为高频易混专题",
        "",
        "### T-INFO-003｜信息系统工程监理：职责边界、四控三管一协调与错误说法",
        "- 新增来源：`past_papers_171/page_003.txt`、`past_papers_171/page_050.txt`",
        "- 新增必须覆盖知识点：监理三方分工、评测单位不在三方控制框架内、监理例会与信息管理边界",
        "- 新增图示建议：建设方 / 承建方 / 监理单位职责边界图",
        "- 新增典型题素材：`OCR-Q-003`、`OCR-Q-006`",
        "- 是否改变专题重要度：是",
        "",
        "### T-SCOPE-003｜范围确认、范围控制、产品范围 vs 项目范围、范围蔓延",
        "- 新增来源：`past_papers_171/page_034.txt`、`page_069.txt`、`page_152.txt`、`page_153.txt`、`page_169.txt`",
        "- 新增必须覆盖知识点：范围确认定义、与质量控制的先后关系、变更申请触发点、验收材料",
        "- 新增图示建议：范围确认 vs 质量控制对照表",
        "- 新增典型题素材：`OCR-Q-004`、`OCR-Q-005`、`OCR-Q-008`",
        "- 是否改变专题重要度：是",
        "",
        "### T-COST-002｜挣值管理：PV/EV/AC、CV/SV/CPI/SPI",
        "- 新增来源：`past_papers_171/page_034.txt`、`page_019.txt`、`page_067.txt`、`page_113.txt`、`page_166.txt`",
        "- 新增必须覆盖知识点：CPI 语义解释、ETC 公式、CPI/SPI 联动判断",
        "- 新增图示建议：挣值指标判读表 + 公式关系图",
        "- 新增典型题素材：`OCR-Q-005`",
        "- 是否改变专题重要度：是",
        "",
        "## 对 04_真题考法与题目映射索引.md 的补充建议",
        "",
        "### OCR-Q-001｜国家信息化体系六要素定位题",
        "- 来源：`past_papers_171/page_001.txt`",
        "- 页码：`page_001`",
        "- 题干：国家信息化体系六要素关系图定位题",
        "- 选项：可识别 A/B/C/D 结构",
        "- 答案：根据页内解析图，可读出 A",
        "- 解析摘要：解析页直接给出六要素关系图与位置判断",
        "- 主专题映射：`T-INFO-001`",
        "- 关联专题：`T-INFO-002`",
        "- OCR 可信度：中高，建议并入时人工核对选项字母",
        "",
        "### OCR-Q-005｜范围确认 / 资源平衡 / CPI 综合页",
        "- 来源：`past_papers_171/page_034.txt`",
        "- 页码：`page_034`",
        "- 题干：同页连续覆盖范围确认、资源平衡、CPI 判读",
        "- 选项：可识别 A/B/C/D 结构",
        "- 答案：解析能读出“范围确认可能产生变更申请”“资源平衡不一定最优”“CPI=0.91 的语义”",
        "- 解析摘要：适合拆成三个子题索引",
        "- 主专题映射：`T-SCOPE-003`",
        "- 关联专题：`T-SCH-005`、`T-COST-002`",
        "- OCR 可信度：高",
        "",
    ]
    (REPORTS_ROOT / "03_ocr_index_supplement.md").write_text("\n".join(lines), encoding="utf-8")


def write_quality_update() -> None:
    update = dedent(
        """
        # OCR 专项后质量更新

        ## 上一轮缺口

        - 官方教程为扫描/图片型 PDF，无法建立可靠的官方页级索引。
        - 171 页历年题解析未能稳定 OCR，真题题号、选项、解析映射缺失。

        ## 本轮已解决

        - 两份扫描 PDF 均完成全量页级 OCR，并保留到 `outputs/ocr/pages/`。
        - 已生成两份 OCR PDF：
          - `outputs/ocr/pdf/官方教程_ocr.pdf`
          - `outputs/ocr/pdf/历年题解析_171页_ocr.pdf`
        - 官方教程已可恢复目录页、章节起始页、案例章节入口，可为专题树与素材库提供官方锚点。
        - 历年题解析已可恢复大部分题干、选项结构、解析摘要，可为真题考法映射提供新增样本。
        - 低质量页、空页、疑难页已单独进入 `outputs/ocr/review_queue/low_quality_pages.md`。

        ## 本轮部分解决

        - `ocrmypdf + tesseract` 样本能够生成 PDF/A，但文本层抽取稳定性不足，因此未作为主产物，仅保留为尝试记录。
        - OCR PDF 已生成，但真正用于后续专题生成的权威文本来源仍是页级 `.txt` 与 `pages_index.json`。
        - 表格、图示、封面与极个别尾页仍有误识别或低文本量，需人工复核。

        ## 仍未解决

        - 官方教程 `page_022`、`page_423`、`page_678` 需人工确认是否为空白页、截断页或尾页噪声。
        - 历年题解析 `page_014`、`page_025`、`page_084`、`page_086`、`page_093`、`page_171` 仍需人工或多模态复核。
        - 英文较多、图形较多或版式压缩严重的页面，虽然未被规则命中，也仍建议在正式纳入题库前抽检。

        ## 对后续专题生成的影响

        - 之后生成专题讲义时，已经可以引用官方教程 OCR 页码作为权威出处，不必再只依赖压缩笔记或题库。
        - 真题专题生成时，可直接从 `past_papers_171/pages_index.json` 筛出题号密集页，再人工复核后并入 `04_真题考法与题目映射索引.md`。
        - 对于低质量页，应明确打上“需人工校验”标签，避免把 OCR 噪声误当成标准答案或术语定义。

        ## 建议下一步

        - 先使用 `03_ocr_index_supplement.md` 中标出的高价值页补进 `01 / 03 / 04` 的正式版本。
        - 对 `review_queue` 中页面做人工复核，必要时再用多模态 OCR 或更高 DPI 重跑局部页。
        - 若后续要做“按官方教材页码引用”的讲义或卡片，请优先使用 `outputs/ocr/pages/official_tutorial/page_*.txt` 作为文本底稿。
        """
    ).strip() + "\n"
    (REPORTS_ROOT / "04_ocr_quality_check_update.md").write_text(update, encoding="utf-8")

    quality_path = ROOT / "outputs" / "_quality_check.md"
    original = quality_path.read_text(encoding="utf-8")
    marker = "## 2026-05-19 OCR 专项更新"
    if marker not in original:
        original += (
            "\n\n"
            "## 2026-05-19 OCR 专项更新\n\n"
            "- 已补齐两份扫描 PDF 的全量 OCR 页级文本与 OCR PDF，见 `outputs/ocr/`。\n"
            "- 官方教程 OCR：678 页，`ok` 675 页，`review` 2 页，`empty` 1 页。\n"
            "- 历年题解析 OCR：171 页，`ok` 165 页，`review` 3 页，`empty` 3 页。\n"
            "- 低质量页已单独列入 `outputs/ocr/review_queue/low_quality_pages.md`，后续正式并入索引前应人工校验。\n"
        )
        quality_path.write_text(original, encoding="utf-8")


def main() -> None:
    write_manifest()
    write_attempt_log()
    write_official_outline()
    write_question_index()
    write_index_supplement()
    write_quality_update()


if __name__ == "__main__":
    main()
