#!/usr/bin/env python3
"""03_quality_check.py — OCR 质量检查脚本

对生成的 Markdown 做基础质检，输出：
  - reports/ocr_quality_report.md
  - reports/full_run_recommendation.md
"""

from __future__ import annotations

import json
import os
import re
from collections import Counter
from pathlib import Path
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
TRIAL_DIR = PROJECT_ROOT / "docmind_ocr_trial"
MD_DIR = TRIAL_DIR / "markdown_outputs"
RAW_DIR = TRIAL_DIR / "raw_outputs"
INPUT_DIR = TRIAL_DIR / "input_samples"
REPORTS_DIR = TRIAL_DIR / "reports"

SAMPLES = [
    {"slug": "tutorial", "label": "教程样本", "type": "tutorial"},
    {"slug": "questions", "label": "题库样本", "type": "questions"},
]


def log(msg: str) -> None:
    timestamp = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")


def analyze_text(text: str) -> dict:
    """分析文本的各项指标。"""
    total_chars = len(text)
    total_non_ws = len(re.sub(r"\s", "", text))

    # 中文字符
    chinese_chars = len(re.findall(r"[一-鿿]", text))
    chinese_ratio = chinese_chars / total_non_ws if total_non_ws > 0 else 0

    # 乱码检测
    garbled = len(re.findall(r"[�]", text))  # �
    garbled_ratio = garbled / total_chars if total_chars > 0 else 0

    # 标题结构
    h1_count = len(re.findall(r"^# ", text, re.MULTILINE))
    h2_count = len(re.findall(r"^## ", text, re.MULTILINE))
    h3_count = len(re.findall(r"^### ", text, re.MULTILINE))

    # 表格
    table_lines = len(re.findall(r"^\|.*\|$", text, re.MULTILINE))
    has_table = table_lines > 0

    # 选择题选项
    option_letters_en = len(re.findall(r"[A-D][.、)]", text))
    option_letters_cn = len(re.findall(r"[Ａ-Ｄ][.、)]", text))

    # 题目关键词
    question_marks = text.count("？") + text.count("?")

    # 答案/解析关键词
    answer_count = len(re.findall(r"(答案|解析|参考答案)", text))

    # 页眉页脚重复检测 - 取前 500 和后 500 字符
    # 检查是否有重复出现的短句
    sentences = re.findall(r".{10,40}", text)
    if len(sentences) > 5:
        counter = Counter(sentences)
        repeated = [(s, c) for s, c in counter.most_common(10) if c >= 3]
    else:
        repeated = []

    # 孤立页码 - 单独一行的纯数字
    isolated_numbers = len(re.findall(r"^\s*\d{1,4}\s*$", text, re.MULTILINE))

    return {
        "total_chars": total_chars,
        "total_non_ws": total_non_ws,
        "chinese_chars": chinese_chars,
        "chinese_ratio": chinese_ratio,
        "garbled": garbled,
        "garbled_ratio": garbled_ratio,
        "h1_count": h1_count,
        "h2_count": h2_count,
        "h3_count": h3_count,
        "table_lines": table_lines,
        "has_table": has_table,
        "option_letters_en": option_letters_en,
        "option_letters_cn": option_letters_cn,
        "question_marks": question_marks,
        "answer_count": answer_count,
        "repeated_strings": repeated,
        "isolated_numbers": isolated_numbers,
    }


def quality_score(metrics: dict, sample_type: str) -> tuple[int, list[str]]:
    """计算质量评分（越低越好）和问题列表。"""
    score = 0
    issues: list[str] = []

    # 1. 文件大小
    if metrics["total_chars"] < 100:
        score += 5
        issues.append("Markdown 文本极短（<100 字符），可能 OCR 失败")
    elif metrics["total_chars"] < 500:
        score += 2
        issues.append("Markdown 文本较短（<500 字符），内容可能不完整")

    # 2. 中文字符比例
    if metrics["chinese_ratio"] < 0.3:
        score += 4
        issues.append(f"中文字符比例极低（{metrics['chinese_ratio']:.1%}），OCR 结果不可用")
    elif metrics["chinese_ratio"] < 0.5:
        score += 2
        issues.append(f"中文字符比例偏低（{metrics['chinese_ratio']:.1%}），含较多非中文内容")
    elif metrics["chinese_ratio"] < 0.7:
        score += 1
        issues.append(f"中文字符比例中等（{metrics['chinese_ratio']:.1%}），可接受但需注意")

    # 3. 乱码
    if metrics["garbled_ratio"] > 0.05:
        score += 5
        issues.append(f"乱码比例过高（{metrics['garbled_ratio']:.1%}），识别质量极差")
    elif metrics["garbled_ratio"] > 0.01:
        score += 2
        issues.append(f"存在乱码（{metrics['garbled']} 个替换字符）")

    # 4. 标题结构（教程）
    if sample_type == "tutorial":
        if metrics["h1_count"] == 0 and metrics["h2_count"] == 0:
            score += 1
            issues.append("未检测到标题结构（# / ##），缺少层级信息")

    # 5. 表格（教程）
    if sample_type == "tutorial":
        if not metrics["has_table"]:
            score += 1
            issues.append("未检测到表格结构，教材中应有表格，可能丢失")

    # 6. 选择题选项（题库）
    if sample_type == "questions":
        total_opts = metrics["option_letters_en"] + metrics["option_letters_cn"]
        if total_opts == 0:
            score += 3
            issues.append("未检测到选择题选项（A./B./C./D.），题库识别可能失败")
        elif total_opts < 4:
            score += 2
            issues.append(f"选择题选项极少（{total_opts} 个），可能不完整")

    # 7. 答案/解析（题库）
    if sample_type == "questions":
        if metrics["answer_count"] == 0:
            score += 2
            issues.append("未检测到「答案」或「解析」关键词，答案对齐可能失败")
        elif metrics["answer_count"] < 3:
            score += 1
            issues.append(f"答案/解析关键词较少（{metrics['answer_count']} 个）")

    # 8. 重复文本
    if metrics["repeated_strings"]:
        score += min(len(metrics["repeated_strings"]), 3)
        top_repeat = metrics["repeated_strings"][0]
        issues.append(f"检测到重复文本（如 \"{top_repeat[0]}\" 出现 {top_repeat[1]} 次），可能有页眉页脚污染")

    # 9. 孤立页码
    if metrics["isolated_numbers"] > 5:
        score += 1
        issues.append(f"检测到 {metrics['isolated_numbers']} 个孤立数字行，可能是页码噪声")

    return score, issues


def rating_label(score: int) -> str:
    if score <= 2:
        return "可用 ✓"
    elif score <= 5:
        return "勉强可用 △"
    else:
        return "不建议直接使用 ✗"


def main():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    now_str = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

    log("===== 质量检查开始 =====")

    all_metrics = {}

    # 分析每个样本
    for sample in SAMPLES:
        slug = sample["slug"]
        label = sample["label"]
        sample_type = sample["type"]

        md_path = MD_DIR / f"{slug}_pages_001_010.md"
        raw_path = RAW_DIR / f"{slug}_pages_001_010.raw.json"

        if not md_path.is_file():
            log(f"✗ {label} Markdown 文件不存在: {md_path}")
            all_metrics[slug] = {
                "label": label,
                "type": sample_type,
                "exists": False,
                "error": f"文件不存在: {md_path}",
            }
            continue

        text = md_path.read_text(encoding="utf-8")
        metrics = analyze_text(text)
        score, issues = quality_score(metrics, sample_type)

        raw_exists = raw_path.is_file()
        raw_size = raw_path.stat().st_size if raw_exists else 0

        all_metrics[slug] = {
            "label": label,
            "type": sample_type,
            "exists": True,
            "path": str(md_path),
            "text_len": len(text),
            "raw_exists": raw_exists,
            "raw_size_bytes": raw_size,
            "metrics": metrics,
            "score": score,
            "issues": issues,
            "rating": rating_label(score),
        }
        log(f"  {label}: 评分 {score} → {rating_label(score)}")

    # 生成质量报告
    generate_quality_report(all_metrics, now_str)

    # 生成全量建议
    generate_recommendation(all_metrics, now_str)

    log("===== 质量检查完成 =====")


def generate_quality_report(all_metrics: dict, now_str: str) -> None:
    """生成 ocr_quality_report.md。"""
    lines = [
        "# OCR 质量检查报告",
        "",
        f"生成时间：{now_str}",
        "",
        "---",
        "",
    ]

    for slug, data in all_metrics.items():
        label = data["label"]
        lines.append(f"## {label}（{slug}）")
        lines.append("")

        if not data["exists"]:
            lines.append(f"**状态**：{data.get('error', '未知错误')}")
            lines.append("")
            continue

        m = data["metrics"]
        lines.append(f"**状态**：文件存在 ✓")
        lines.append(f"**评分**：{data['score']} 分 — {data['rating']}")
        lines.append("")

        lines.append("### 基础指标")
        lines.append("")
        lines.append(f"| 指标 | 值 |")
        lines.append(f"|------|------|")
        lines.append(f"| 总字符数 | {m['total_chars']:,} |")
        lines.append(f"| 中文字符数 | {m['chinese_chars']:,} |")
        lines.append(f"| 中文比例 | {m['chinese_ratio']:.1%} |")
        lines.append(f"| 乱码字符 (�) | {m['garbled']} |")
        lines.append(f"| 乱码比例 | {m['garbled_ratio']:.1%} |")
        lines.append("")

        lines.append("### 结构指标")
        lines.append("")
        lines.append(f"| 指标 | 值 |")
        lines.append(f"|------|------|")
        lines.append(f"| 一级标题 (# ) | {m['h1_count']} |")
        lines.append(f"| 二级标题 (## ) | {m['h2_count']} |")
        lines.append(f"| 三级标题 (### ) | {m['h3_count']} |")
        lines.append(f"| 表格行 | {m['table_lines']} |")
        lines.append("")

        if data["type"] == "questions":
            lines.append("### 题库专项指标")
            lines.append("")
            lines.append(f"| 指标 | 值 |")
            lines.append(f"|------|------|")
            lines.append(f"| 选择题选项 (A.-D. 英文) | {m['option_letters_en']} |")
            lines.append(f"| 选择题选项 (Ａ-Ｄ 全角) | {m['option_letters_cn']} |")
            lines.append(f"| 问号数量 | {m['question_marks']} |")
            lines.append(f"| 答案/解析关键词 | {m['answer_count']} |")
            lines.append("")

        lines.append("### 噪声检测")
        lines.append("")
        lines.append(f"| 指标 | 值 |")
        lines.append(f"|------|------|")
        lines.append(f"| 孤立页码行 | {m['isolated_numbers']} |")
        lines.append(f"| 重复字符串组 | {len(m['repeated_strings'])} |")
        if m["repeated_strings"]:
            lines.append("")
            lines.append("**重复内容 Top 5**：")
            for s, count in m["repeated_strings"][:5]:
                lines.append(f"- 「{s.strip()}」— 出现 {count} 次")
        lines.append("")

        if data["issues"]:
            lines.append("### 发现的问题")
            lines.append("")
            for issue in data["issues"]:
                lines.append(f"- ⚠ {issue}")
        else:
            lines.append("### 发现的问题")
            lines.append("")
            lines.append("- 未发现明显问题 ✓")
        lines.append("")

        # 人工抽查建议
        lines.append("### 人工抽查建议")
        lines.append("")
        md_path = MD_DIR / f"{slug}_pages_001_010.md"
        lines.append(f"请打开 `{md_path}` ，重点检查：")
        lines.append("")
        if data["type"] == "tutorial":
            lines.append("- 目录页层级是否正确")
            lines.append("- 正文标题是否识别为 `#` / `##`")
            lines.append("- 表格结构是否保留")
            lines.append("- 图片/公式是否以文字说明形式出现")
            lines.append("- 页码和页眉页脚是否干扰正文")
        else:
            lines.append("- 题干是否完整")
            lines.append("- A/B/C/D 选项是否拆分正确")
            lines.append("- 答案是否与解析绑定")
            lines.append("- 多题之间是否串行")
            lines.append("- 选项编号是否统一")
        lines.append("")
        lines.append("---")
        lines.append("")

    report_path = REPORTS_DIR / "ocr_quality_report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    log(f"质量报告已生成: {report_path}")


def generate_recommendation(all_metrics: dict, now_str: str) -> None:
    """生成 full_run_recommendation.md。"""
    overall_ok = all(data["exists"] for data in all_metrics.values())
    scores = [data.get("score", 999) for data in all_metrics.values()]
    max_score = max(scores) if scores else 999
    avg_score = sum(scores) / len(scores) if scores else 999

    if max_score <= 2:
        verdict = "可用 — 建议全量处理"
        plan = ("1. 将完整 PDF 上传到阿里云 OSS（或确认 MCP 支持本地 file://）\n"
                "2. 分批调用 convert_to_markdown（建议每批 50-100 页）\n"
                "3. 运行清洗脚本清除页眉页脚、页码噪声\n"
                "4. 输出分章 Markdown，准备构建知识树和 Anki 卡片")
    elif max_score <= 5:
        verdict = "勉强可用 — 可以全量处理，但需要较多后处理"
        plan = ("1. 全量转换后需重点清洗页眉页脚和页码\n"
                "2. 题库需要人工校对选项拆分\n"
                "3. 建议全量前先用 50 页做第二轮验证")
    else:
        verdict = "不建议直接使用 — 应尝试备选方案"
        plan = ("1. 尝试阿里云文档解析（大模型版）增强链路\n"
                "2. 使用 Python SDK 直接调用 SubmitDocumentAnalyzeJob\n"
                "3. 备选：OCRmyPDF + PaddleOCR 本地方案\n"
                "4. 备选：ABBYY FineReader（如已购买）")

    lines = [
        "# 全量处理建议报告",
        "",
        f"生成时间：{now_str}",
        "",
        "---",
        "",
        "## 本轮试验结果",
        "",
        f"- MCP 调用成功：{'是' if overall_ok else '否（部分失败）'}",
        f"- Markdown 生成成功：{'是' if overall_ok else '否'}",
        f"- 质量评分：最高 {max_score} 分，平均 {avg_score:.1f} 分",
        "",
        "### 各样本评分",
        "",
        "| 样本 | 评分 | 评级 |",
        "|------|------|------|",
    ]
    for slug, data in all_metrics.items():
        if data["exists"]:
            lines.append(f"| {data['label']} | {data['score']} | {data['rating']} |")
        else:
            lines.append(f"| {data['label']} | - | 转换失败 |")

    lines.extend([
        "",
        "## 综合评价",
        "",
        f"**{verdict}**",
        "",
        "## 全量处理建议",
        "",
        plan,
        "",
        "## 费用估算（849 页）",
        "",
        "| 链路 | 单价 | 总费用 |",
        "|------|------|--------|",
        "| 基础链路（文档解析标准版） | ~0.02 元/页 | ~16.98 元 |",
        "| 增强链路（文档解析大模型版） | ~0.04 元/页 | ~33.96 元 |",
        "| 如有每月 3000 页免费额度 | 免费 | 0 元 |",
        "",
        "> 注意：实际价格以阿里云官方定价为准。请登录控制台确认当前计费规则和免费额度。",
        "",
        "## 备选方案",
        "",
        "如果 Document Mind 效果不理想：",
        "",
        "1. **阿里云 Python SDK 直接调用**：可以更精细地控制参数（如 DPI、语言模型）",
        "2. **OCRmyPDF + Tesseract**：开源免费，中文需额外配置中文语言包",
        "3. **PaddleOCR**：百度开源，中文识别效果好，可本地部署",
        "4. **ABBYY FineReader**：商业软件，识别精度高，但需购买授权",
        "",
        "## 全量处理前需确认",
        "",
        "- [ ] 使用基础链路还是增强链路？",
        "- [ ] 是否允许处理完整 678 + 171 页？",
        "- [ ] PDF 是否需要上传到 OSS 临时 URL？",
        "- [ ] 是否保留原始版面信息或只保留 Markdown 文本？",
        "- [ ] 是否需要分批处理（每批 50-100 页）？",
    ])

    report_path = REPORTS_DIR / "full_run_recommendation.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    log(f"全量建议已生成: {report_path}")


if __name__ == "__main__":
    main()
