#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.request
from pathlib import Path


URL = "http://127.0.0.1:8765"
ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV = ROOT / "outputs/anki_builds/full_expansion_20260521_003052/aggregate/import_preview_keep_only.csv"
BACKUP_DIR = ROOT / "outputs/anki_builds/full_expansion_20260521_003052/aggregate/anki_replace_backups"
MODEL_NAME = "RuankaoTopicCard"
MODEL_FIELDS = [
    "Front",
    "Back",
    "Extra",
    "SourceTopicID",
    "SourceTopicName",
    "SourceFile",
    "KnowledgeDomain",
    "CardType",
    "Importance",
    "ExamUse",
    "RelatedQuestionIDs",
    "TagsText",
    "Checksum",
]


def call(action: str, **params):
    data = json.dumps({"action": action, "version": 6, "params": params}).encode()
    req = urllib.request.Request(URL, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as response:
        result = json.loads(response.read())
    if result.get("error"):
        raise RuntimeError(f"{action}: {result['error']}")
    return result.get("result")


def chunks(items: list, size: int):
    for i in range(0, len(items), size):
        yield items[i : i + size]


def load_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    return [row for row in rows if row.get("manual_review_status") == "keep"]


def note_from_row(row: dict[str, str]) -> dict:
    fields = {
        "Front": row.get("front", ""),
        "Back": row.get("back", ""),
        "Extra": row.get("extra", ""),
        "SourceTopicID": row.get("source_topic_ids", ""),
        "SourceTopicName": row.get("source_topic_names", ""),
        "SourceFile": row.get("source_file", ""),
        "KnowledgeDomain": row.get("knowledge_domain", ""),
        "CardType": row.get("card_type", ""),
        "Importance": row.get("importance", ""),
        "ExamUse": row.get("exam_use", ""),
        "RelatedQuestionIDs": row.get("related_question_ids", ""),
        "TagsText": row.get("tags", ""),
        "Checksum": row.get("checksum", ""),
    }
    return {
        "deckName": row.get("deck") or "软考::系统集成项目管理工程师",
        "modelName": MODEL_NAME,
        "fields": {field: fields.get(field, "") for field in MODEL_FIELDS},
        "tags": [tag for tag in row.get("tags", "").split() if tag],
        "options": {"allowDuplicate": True, "duplicateScope": "deck"},
    }


def find_existing_ruankao_notes() -> list[int]:
    queries = [
        'deck:"软考"',
        'deck:"软考::*"',
        "tag:ruankao",
        "tag:ruankao::*",
    ]
    note_ids: set[int] = set()
    for query in queries:
        try:
            note_ids.update(call("findNotes", query=query))
        except RuntimeError:
            continue
    return sorted(note_ids)


def backup_notes(note_ids: list[int]) -> Path | None:
    if not note_ids:
        return None
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup_path = BACKUP_DIR / f"old_ruankao_notes_{time.strftime('%Y%m%d_%H%M%S')}.json"
    notes = []
    for group in chunks(note_ids, 100):
        notes.extend(call("notesInfo", notes=group))
    backup_path.write_text(json.dumps(notes, ensure_ascii=False, indent=2), encoding="utf-8")
    return backup_path


def preflight(notes: list[dict]) -> None:
    model_names = call("modelNames")
    if MODEL_NAME not in model_names:
        raise RuntimeError(f"Anki note type not found: {MODEL_NAME}")

    for deck in sorted({note["deckName"] for note in notes}):
        call("createDeck", deck=deck)

    failures = []
    for group in chunks(notes, 100):
        result = call("canAddNotesWithErrorDetail", notes=group)
        failures.extend(item for item in result if not item.get("canAdd"))
    if failures:
        sample = json.dumps(failures[:5], ensure_ascii=False, indent=2)
        raise RuntimeError(f"New notes failed preflight: {len(failures)}\n{sample}")


def replace(csv_path: Path, dry_run: bool) -> None:
    rows = load_rows(csv_path)
    notes = [note_from_row(row) for row in rows]
    old_note_ids = find_existing_ruankao_notes()

    print(f"new notes ready: {len(notes)}")
    print(f"old ruankao notes found: {len(old_note_ids)}")
    preflight(notes)
    print("preflight: ok")

    if dry_run:
        print(json.dumps(notes[:2], ensure_ascii=False, indent=2))
        return

    backup_path = backup_notes(old_note_ids)
    if backup_path:
        print(f"backup: {backup_path}")

    if old_note_ids:
        for group in chunks(old_note_ids, 100):
            call("deleteNotes", notes=group)
        print(f"deleted old notes: {len(old_note_ids)}")

    added = []
    for group in chunks(notes, 100):
        added.extend(call("addNotes", notes=group))
    ok = sum(1 for note_id in added if note_id)
    failed = len(added) - ok
    print(f"added new notes: {ok}")
    if failed:
        print(f"failed/skipped: {failed}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    replace(args.csv, args.dry_run)


if __name__ == "__main__":
    main()
