# Anki NoteType And CSS

Existing `RuankaoTopicCard` is compatible with this build. Recommended fields if upgrading later:

Front, Back, Extra, CardType, Importance, Difficulty, ExamUse, KnowledgeDomain, SourceTopicID, SourceTopicName, SourceFile, SourceHeading, SourceExcerpt, SourceIDs, RelatedQuestionIDs, RelatedTopicIDs, Checksum, TagsText, QualityScore.

## CSS

```css
.card { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; line-height: 1.55; font-size: 17px; }
.answer-block, .extra { margin-top: 12px; }
.section-title { font-weight: 700; margin-top: 10px; color: #2563eb; }
.answer-block div:not(.section-title), .extra div:not(.section-title), li { margin: 4px 0 8px; }
ul { padding-left: 1.25em; }
@media (prefers-color-scheme: dark) { .section-title { color: #93c5fd; } }
```
