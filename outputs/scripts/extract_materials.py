#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List

from pypdf import PdfReader


ROOT = Path("/Users/wangrundong/work/软考")
OUT_DIR = ROOT / "outputs" / "extracted_text"


@dataclass
class FileMeta:
    source: str
    kind: str
    output: str | None
    parseable: bool
    note: str
    page_count: int | None = None
    char_count: int | None = None


def safe_name(path: Path) -> str:
    return path.name.replace("/", "_")


def write_text(path: Path, text: str) -> int:
    path.write_text(text, encoding="utf-8")
    return len(text)


def extract_pdf(src: Path) -> FileMeta:
    try:
        reader = PdfReader(str(src))
        pages: List[str] = []
        non_empty = 0
        for idx, page in enumerate(reader.pages, start=1):
            try:
                text = page.extract_text() or ""
            except Exception as exc:  # pragma: no cover
                text = f"[PAGE {idx} EXTRACT ERROR] {exc}"
            if text.strip():
                non_empty += 1
            pages.append(f"\n\n===== Page {idx} =====\n{text.strip()}\n")
        full_text = "".join(pages).strip() + "\n"
        out = OUT_DIR / f"{safe_name(src)}.txt"
        chars = write_text(out, full_text)
        note = "文本提取完成"
        parseable = True
        if non_empty == 0:
            note = "未提取到正文文本，疑似扫描版或受保护 PDF"
            parseable = False
        elif non_empty < len(reader.pages):
            note = f"部分页面提取为空（{non_empty}/{len(reader.pages)} 页有文本），需校验是否为扫描页"
        return FileMeta(
            source=src.name,
            kind="pdf",
            output=str(out.relative_to(ROOT)),
            parseable=parseable,
            note=note,
            page_count=len(reader.pages),
            char_count=chars,
        )
    except Exception as exc:
        return FileMeta(
            source=src.name,
            kind="pdf",
            output=None,
            parseable=False,
            note=f"PDF 解析失败：{exc}",
        )


def extract_via_textutil(src: Path) -> FileMeta:
    out = OUT_DIR / f"{safe_name(src)}.txt"
    cmd = [
        "/usr/bin/textutil",
        "-convert",
        "txt",
        "-stdout",
        str(src),
    ]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True)
        text = result.stdout.decode("utf-8", errors="ignore")
        chars = write_text(out, text)
        parseable = bool(text.strip())
        note = "textutil 转换完成" if parseable else "textutil 转换成功但文本为空"
        return FileMeta(
            source=src.name,
            kind=src.suffix.lower().lstrip("."),
            output=str(out.relative_to(ROOT)),
            parseable=parseable,
            note=note,
            char_count=chars,
        )
    except Exception as exc:
        return FileMeta(
            source=src.name,
            kind=src.suffix.lower().lstrip("."),
            output=None,
            parseable=False,
            note=f"textutil 转换失败：{exc}",
        )


def extract_text_file(src: Path) -> FileMeta:
    out = OUT_DIR / f"{safe_name(src)}.txt"
    text = src.read_text(encoding="utf-8", errors="ignore")
    chars = write_text(out, text)
    return FileMeta(
        source=src.name,
        kind=src.suffix.lower().lstrip("."),
        output=str(out.relative_to(ROOT)),
        parseable=True,
        note="文本文件直接复制",
        char_count=chars,
    )


def collect_sources() -> List[Path]:
    root_files = [
        p
        for p in ROOT.iterdir()
        if p.is_file()
        and p.name not in {".DS_Store"}
        and not p.name.endswith("_深度样例.md")
    ]
    anki_files = [
        p for p in (ROOT / "anki").rglob("*") if p.is_file() and p.name != ".DS_Store"
    ]
    return sorted(root_files + anki_files)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    metas: List[FileMeta] = []
    for src in collect_sources():
        suffix = src.suffix.lower()
        if suffix == ".pdf":
            meta = extract_pdf(src)
        elif suffix in {".doc", ".docx"}:
            meta = extract_via_textutil(src)
        elif suffix in {".md", ".txt"}:
            meta = extract_text_file(src)
        else:
            meta = FileMeta(
                source=src.name,
                kind=suffix.lstrip("."),
                output=None,
                parseable=False,
                note="暂不支持的文件类型",
            )
        metas.append(meta)

    manifest = {
        "generated_at": subprocess.run(
            ["date", "+%Y-%m-%d %H:%M:%S"], capture_output=True, text=True, check=True
        ).stdout.strip(),
        "files": [asdict(m) for m in metas],
    }
    (OUT_DIR / "_extraction_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
