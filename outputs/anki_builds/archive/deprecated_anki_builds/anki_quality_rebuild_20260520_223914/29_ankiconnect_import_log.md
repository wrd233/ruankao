# AnkiConnect Import Log

## Actual Replacement Run

- Timestamp: 2026-05-20 22:44-22:45 Asia/Shanghai
- User approval: explicit request to replace current soft-exam cards.
- Backup directory: `outputs/anki_quality_rebuild_20260520_223914/anki_replace_backup/`
- Metadata backup: `existing_ruankao_notes_20260520_224447.json`
- Note ID backup: `existing_ruankao_note_ids_20260520_224447.json`
- Card ID backup: `existing_ruankao_card_ids_20260520_224447.json`
- APKG backup: `existing_ruankao_deck_20260520_224447.apkg`

## Actions

1. Queried current soft-exam collection with `deck:"软考::*" OR tag:ruankao`.
2. Backed up 476 existing notes / 476 cards.
3. Exported the `软考` deck package with scheduling included.
4. Deleted the 476 old soft-exam notes.
5. Created/confirmed all target decks from `25_final_all_cards.csv`.
6. Imported 416 final notes from the quality rebuild.
7. Verified all 416 checksums exist after import.
8. Verified 33 target leaf decks have cards after import.

## Result

- Old notes removed: 476
- Old cards removed: 476
- New final notes imported: 416
- Failed imports: 0
- Soft-exam notes after import: 416
- Soft-exam cards after import: 416
- Missing checksums after import: 0
- Zero-card target leaf decks after import: 0

## Post-Import Counts

- `deck:"软考::*"`: 416 notes / 416 cards
- `tag:ruankao`: 416 notes / 416 cards
- Topic study decks: 345 notes / 345 cards
- Past-exam deck: 56 notes / 56 cards
- Cross-topic deck: 15 notes / 15 cards
- Legacy `刷题训练` decks: 0 notes / 0 cards

## Note

The first `addNotes` attempt was blocked by Anki's first-field duplicate check after the old notes had already been deleted. Recovery used the project Checksum field as the real idempotency key and enabled Anki-level duplicate Front allowance; the recovery import completed successfully with 416/416 notes added.
