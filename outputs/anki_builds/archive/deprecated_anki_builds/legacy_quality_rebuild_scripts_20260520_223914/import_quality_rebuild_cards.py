#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import os
import urllib.request
from pathlib import Path


ANKI_URL = "http://127.0.0.1:8765"
MODEL_FIELDS = [
    "Front", "Back", "Extra", "SourceTopicID", "SourceTopicName", "SourceFile",
    "KnowledgeDomain", "CardType", "Importance", "ExamUse", "RelatedQuestionIDs",
    "TagsText", "Checksum",
]


def call(action: str, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode("utf-8")
    req = urllib.request.Request(ANKI_URL, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())
    if result.get("error"):
        raise RuntimeError(result["error"])
    return result.get("result")


def row_to_note(row: dict[str, str]) -> dict:
    fields = {
        "Front": row["front"],
        "Back": row["back"],
        "Extra": row["extra"],
        "SourceTopicID": row["source_topic_id"],
        "SourceTopicName": row["source_topic_name"],
        "SourceFile": row["source_file"],
        "KnowledgeDomain": row["knowledge_domain"],
        "CardType": row["card_type"],
        "Importance": row["importance"],
        "ExamUse": row["exam_use"],
        "RelatedQuestionIDs": row.get("related_question_ids", ""),
        "TagsText": row.get("tags", ""),
        "Checksum": row["checksum"],
    }
    return {
        "deckName": row["deck"],
        "modelName": "RuankaoTopicCard",
        "fields": fields,
        "tags": row.get("tags", "").split(),
        # We dedupe by the stable Checksum field. Anki's built-in duplicate
        # check keys off the first field, which can legitimately repeat for
        # soft-exam cards that share a prompt pattern.
        "options": {"allowDuplicate": True, "duplicateScope": "deck"},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--dry-run", action="store_true", help="Preview only; do not write to Anki.")
    args = parser.parse_args()

    rows = [r for r in csv.DictReader(args.csv_path.open(encoding="utf-8-sig")) if r.get("quality_status") == "final"]
    notes = [row_to_note(r) for r in rows]
    print(f"final notes ready: {len(notes)}")
    print(f"decks: {len({n['deckName'] for n in notes})}")

    duplicates = 0
    for row in rows[:120]:
        duplicates += bool(call("findNotes", query=f'"Checksum:{row["checksum"]}"'))
    print(f"sample duplicate checksum hits among first 120: {duplicates}")

    if args.dry_run or os.environ.get("RUN_IMPORT") != "1":
        print("DRY RUN ONLY. Set RUN_IMPORT=1 and omit --dry-run to import.")
        print(json.dumps(notes[:2], ensure_ascii=False, indent=2))
        return

    for deck in sorted({n["deckName"] for n in notes}):
        call("createDeck", deck=deck)
    added = call("addNotes", notes=notes)
    ok = sum(1 for x in added if x)
    print(f"added={ok}; failed_or_duplicate={len(added)-ok}")


if __name__ == "__main__":
    main()
