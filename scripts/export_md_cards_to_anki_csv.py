#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = ROOT / "outputs" / "anki_builds" / "full_expansion_20260521_003052"
AGG_DIR = BUILD_DIR / "aggregate"

FIELDS = [
    "deck",
    "note_type",
    "front",
    "back",
    "extra",
    "card_family",
    "card_type",
    "concept_name",
    "concept_aliases",
    "importance",
    "difficulty",
    "exam_use",
    "knowledge_domain",
    "chapter_id",
    "chapter_name",
    "source_topic_ids",
    "source_topic_names",
    "source_ids",
    "source_file",
    "source_heading",
    "related_question_ids",
    "related_topic_ids",
    "manual_review_status",
    "manual_review_note",
    "tags",
    "checksum",
]


CARD_HEADER_RE = re.compile(r"^##\s+Card\s+\d+｜([^｜]+)｜([^｜]+)｜(.+)$", re.M)
SOURCE_TOPIC_RE = re.compile(r"\b(T-[A-Z0-9-]+)\b")
REVIEW_STATUSES = {"keep", "needs_human_review", "revise", "reject"}


def checksum_for(front: str, back: str, source_file: str) -> str:
    raw = f"{source_file}|{front}|{back}"
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]
    return f"sha256:{digest}"


def htmlize_multiline(text: str) -> str:
    text = text.strip()
    if not text:
        return ""
    return text.replace("\n", "<br>")


def extract_field(block: str, name: str) -> tuple[str, int, int] | None:
    pattern = re.compile(
        rf"^{re.escape(name)}：\s*(.*?)(?=^\w[\w ]*：|\Z)",
        re.M | re.S,
    )
    m = pattern.search(block)
    if not m:
        return None
    return m.group(1).strip(), m.start(), m.end()


def parse_manual_review(value: str) -> tuple[str, str]:
    value = value.strip()
    if "。" in value:
        status, note = value.split("。", 1)
    else:
        status, note = value, ""
    return status.strip(), note.strip()


def parse_header_fields(part2: str, part3: str) -> tuple[str, str]:
    part2 = part2.strip()
    part3 = part3.strip()
    if part2 in REVIEW_STATUSES:
        return part2, part3
    if part3 in REVIEW_STATUSES:
        return part3, part2
    return "", part3


def detect_family(path: Path) -> str:
    path_str = str(path)
    if "question_cards" in path_str:
        return "question"
    if "calculation_topics" in path_str:
        return "calculation"
    if "chapters/by_chapter" in path_str:
        return "chapter_concept"
    return "topic_qa"


def detect_deck(path: Path, manual_review_status: str, exam_use: str) -> str:
    root = "软考::系统集成项目管理工程师"
    if manual_review_status == "needs_human_review":
        return f"{root}::待核验与复查"
    if "question_cards" in str(path):
        return f"{root}::真题刷题卡::下午案例题" if "案例" in exam_use else f"{root}::真题刷题卡::上午选择题"
    return root


def build_tags(
    family: str,
    card_type: str,
    importance: str,
    source_topic_ids: str,
    manual_review_status: str,
    exam_use: str,
    chapter_id: str,
) -> str:
    tags = [
        "ruankao",
        f"ruankao::family::{family}",
        f"ruankao::card_type::{normalize_tag(card_type)}",
        f"ruankao::importance::{importance}",
    ]
    if exam_use:
        tags.append(f"ruankao::exam_use::{normalize_tag(exam_use)}")
    if chapter_id:
        tags.append(f"ruankao::chapter::{chapter_id}")
    for topic_id in SOURCE_TOPIC_RE.findall(source_topic_ids):
        tags.append(f"ruankao::topic::{topic_id}")
    if manual_review_status == "needs_human_review":
        tags.extend(["ruankao::needs_review", "ruankao::not_for_main_review"])
    return " ".join(dict.fromkeys(tags))


def normalize_tag(text: str) -> str:
    return re.sub(r"\s+", "_", text.strip())


def chapter_meta(path: Path) -> tuple[str, str]:
    parts = path.parts
    if "by_chapter" not in parts:
        return "", ""
    idx = parts.index("by_chapter") + 1
    chapter_name = parts[idx]
    chapter_id = chapter_name.split("_", 1)[0]
    return chapter_id, chapter_name


def topic_meta(path: Path) -> tuple[str, str]:
    parts = path.parts
    if "by_topic" not in parts:
        return "", ""
    idx = parts.index("by_topic") + 1
    topic_id = parts[idx]
    return topic_id, topic_id


def parse_cards(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8-sig")
    matches = list(CARD_HEADER_RE.finditer(text))
    if not matches:
        return []

    chapter_id, chapter_name = chapter_meta(path)
    inferred_topic_id, inferred_topic_name = topic_meta(path)
    family = detect_family(path)
    source_heading = text.splitlines()[0].lstrip("#").strip() if text else ""
    rows: list[dict[str, str]] = []

    for i, match in enumerate(matches):
        block_start = match.start()
        block_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[block_start:block_end].strip()

        card_type = match.group(1).strip()
        manual_status_from_header, third_value = parse_header_fields(match.group(2), match.group(3))
        importance = third_value if third_value in {"A", "B", "C"} else ""
        exam_use = "" if importance else third_value

        front_data = extract_field(block, "Front")
        back_data = extract_field(block, "Back")
        extra_data = extract_field(block, "Extra")
        source_data = extract_field(block, "Source")
        manual_data = extract_field(block, "Manual review")
        if not (front_data and back_data and extra_data and source_data and manual_data):
            continue

        front = front_data[0]
        back = back_data[0]
        extra = extra_data[0]
        source_ids = source_data[0]
        manual_review_status, manual_review_note = parse_manual_review(manual_data[0])
        if manual_status_from_header and not manual_review_status:
            manual_review_status = manual_status_from_header

        related_topics = ",".join(dict.fromkeys(SOURCE_TOPIC_RE.findall(extra)))
        source_topic_ids = inferred_topic_id or related_topics
        source_topic_names = inferred_topic_name or related_topics
        deck = detect_deck(path, manual_review_status, exam_use)
        tags = build_tags(
            family=family,
            card_type=card_type,
            importance=importance,
            source_topic_ids=source_topic_ids,
            manual_review_status=manual_review_status,
            exam_use=exam_use,
            chapter_id=chapter_id,
        )

        rows.append(
            {
                "deck": deck,
                "note_type": "Basic",
                "front": htmlize_multiline(front),
                "back": htmlize_multiline(back),
                "extra": htmlize_multiline(extra),
                "card_family": family,
                "card_type": card_type,
                "concept_name": "",
                "concept_aliases": "",
                "importance": importance,
                "difficulty": "",
                "exam_use": exam_use,
                "knowledge_domain": "",
                "chapter_id": chapter_id,
                "chapter_name": chapter_name,
                "source_topic_ids": source_topic_ids,
                "source_topic_names": source_topic_names,
                "source_ids": source_ids,
                "source_file": str(path.relative_to(ROOT)),
                "source_heading": source_heading,
                "related_question_ids": "",
                "related_topic_ids": related_topics,
                "manual_review_status": manual_review_status,
                "manual_review_note": manual_review_note,
                "tags": tags,
                "checksum": checksum_for(front, back, str(path.relative_to(ROOT))),
            }
        )
    return rows


def collect_card_files() -> list[Path]:
    patterns = [
        "topics/by_topic/*/topic_qa_cards.md",
        "calculation_topics/by_topic/*/*cards.md",
        "chapters/by_chapter/*/chapter_concept_cards.md",
        "question_cards/*cards*.md",
    ]
    paths: list[Path] = []
    for pattern in patterns:
        paths.extend(BUILD_DIR.glob(pattern))
    return sorted(set(p for p in paths if p.is_file()))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    all_rows: list[dict[str, str]] = []
    for path in collect_card_files():
        all_rows.extend(parse_cards(path))

    keep_rows = [row for row in all_rows if row["manual_review_status"] == "keep"]
    review_rows = [row for row in all_rows if row["manual_review_status"] == "needs_human_review"]

    write_csv(AGG_DIR / "import_preview_all.csv", all_rows)
    write_csv(AGG_DIR / "import_preview_keep_only.csv", keep_rows)
    write_csv(AGG_DIR / "all_needs_human_review_cards.csv", review_rows)

    print(f"all={len(all_rows)} keep={len(keep_rows)} needs_review={len(review_rows)}")
    print(AGG_DIR / "import_preview_all.csv")
    print(AGG_DIR / "import_preview_keep_only.csv")
    print(AGG_DIR / "all_needs_human_review_cards.csv")


if __name__ == "__main__":
    main()
