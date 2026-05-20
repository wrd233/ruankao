# Anki Import Plan

- Target deck root: `软考::系统集成项目管理工程师`
- Preferred model: `RuankaoTopicCard`
- Existing model fields expected: Front, Back, Extra, SourceTopicID, SourceTopicName, SourceFile, KnowledgeDomain, CardType, Importance, ExamUse, RelatedQuestionIDs, TagsText, Checksum.
- Source file: `19_final_all_cards.csv`
- Duplicate strategy: search existing notes by Checksum; default importer skips existing checksum unless `--update-existing` is passed.
- Needs-review cards: not included in `18/19_final_all_cards`; they are available in candidate files and should go only to `待核验与复查` if imported manually.
- Safety: back up Anki collection before import; run `scripts/anki_connect_check.py`; review `21_ankiconnect_dry_run_report.md`; then run importer.

## Commands

```bash
python3 scripts/anki_connect_check.py
python3 scripts/import_anki_cards.py outputs/anki_full_build_<timestamp>/19_final_all_cards.csv --dry-run
python3 scripts/import_anki_cards.py outputs/anki_full_build_<timestamp>/19_final_all_cards.csv
```
