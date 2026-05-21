# Manual Self-Review Report

> Generated: 2026-05-21
> Build: `full_expansion_20260521_003052`

## Overall Quality Assessment

This build represents a substantial expansion from the previous full_build_20260520_235046, growing total keep cards from 461 to 1,337 (+190%). The expansion was driven by a structured enrichment plan with clear tier-based targets, and all 31 topics plus 15 chapters are now covered.

**Overall quality grade: B+** (good foundation, known thin spots, ready for import after targeted human spot-check).

### What Works Well

- **Card structure is consistent**: Every keep card follows Front/Back/Extra/Source/Manual review format.
- **Extra fields are useful**: Understanding cues, exam signal words, and cross-references are present on most cards.
- **Calculation cards are well-organized**: Sub-categorized into formula, calculation, comprehensive, case, and trap variants.
- **needs_human_review isolation**: ~10 flagged cards are clearly tagged and can be excluded from the main review deck.
- **Scaling is systematic**: Topic tiers drove proportional card allocation rather than uniform distribution.

### What Needs Improvement

- **Three thin topic packages** (T-INFO-001, T-LAW-001, T-CLOSE-001) hit minimum targets but lack depth.
- **Calculation cards at 128 vs 150 target**: ~22 missing trap and comprehensive variants.
- **OCR-dependency in question cards**: ~5 cards depend on image-based content from OCR.
- **No cross-category deduplication**: Chapter concept cards and topic QA cards may have overlapping content.

## Card Design Principles Applied

1. **One concept per card**: Front asks a single, focused question; Back provides the minimal stable answer.
2. **Goldilocks Back length**: Short enough to be answerable, long enough to be discriminative.
3. **Extra is for enrichment, not answers**: Understanding cues, exam signals, common errors, cross-references.
4. **No quality_score field**: Per design principles, subjective scores are not embedded.
5. **Importance ratings (A/B/C)**: Chapter concept cards carry tier ratings; topic QA cards do not.
6. **Source tracking**: Every card has a Source field for traceability.
7. **Manual review annotation**: Every keep card has `Manual review: keep`; problem cards have `needs_human_review`.
8. **Calculation sub-categorization**: Formula cards test recall; calculation cards test application; trap cards test edge cases; case cards test exam-style scenarios.

## Quality Control Measures Taken

- Enrichment plan (01_topic_enrichment_plan.md) defined targets per topic before card generation.
- Card count targets (02_card_count_targets.md) set numeric goals per category.
- Topic tiering (S/A/B) ensured proportional effort allocation.
- needs_human_review flagging for OCR-dependent, ambiguous, or regulation-number cards.
- Meta-card rejection: ~15 cards identified as non-reviewable (process descriptions, templates, etc.) and excluded.
- Old build problems analyzed: rejection of low-quality calculation cards, consolidation of redundant T-COST-002 content.

### Measures NOT Taken (Known Gaps)

- No automated card-by-card quality review (scale: 1,337 cards).
- No cross-card duplicate detection between chapter and topic cards.
- No peer review or second-pass human editing.
- No Anki import test (format compatibility not verified).
- No spaced repetition schedule design.

## Known Quality Risks

### Risk 1: OCR Instability in Question Cards (Medium)

~5 question cards (out of 212) are flagged needs_human_review because OCR could not reliably capture exam diagrams or the question text was corrupted. These are isolated but represent a gap in exam coverage for image-dependent questions.

Affected files:
- `question_cards/morning_choice_cards.md`: Cards 001, 010, 021, 036, 056, 070
- `question_cards/morning_choice_cards_2010.md`: Suspected similar issues (not fully audited)

### Risk 2: Thin Topic Packages (Medium)

Three topic packages were identified in the enrichment plan as P0 priority for supplementation. They have been expanded from 6 to 15-22 cards but remain surface-level:

- **T-INFO-001** (20 cards): Covers basics but lacks depth in信息化六要素, e-government types, ITIL/ITSM.
- **T-LAW-001** (22 cards): Legal/regulatory content depends on textbook edition accuracy. IP law details, software copyright, and standard numbering need verification.
- **T-CLOSE-001** (15 cards): Coverage of closure ITTOs and administrative vs contract closure comparison is minimal.

### Risk 3: Calculation Formula Accuracy (Low-Medium)

All calculation formula cards (T-SCH-003 total/float, T-SCH-002 PERT, T-RISK-002 EMV, T-FEA-001 NPV/IRR) follow standard PM formulas. However, exact textual presentation has not been cross-checked against a specific textbook edition. Direction is correct; minor notation differences may exist.

### Risk 4: Case Question Card Format (Medium)

67 case question cards use a summary + answer framework format. This format has not been validated for pedagogical effectiveness. Early feedback may lead to restructuring.

### Risk 5: Topic-Chapter Cross-Mapping (Low)

Some topics span chapter boundaries (e.g., T-CROSS-001 covers concepts from multiple chapters). The by-chapter card count assigns each topic to its primary chapter, which may undercount cross-domain contributions.

## Recommended Human Sampling Areas

For a spot-check, review these files first (estimated 20-30 minutes total):

### Priority 1 (Core Quality)
1. **`chapters/by_chapter/01_信息化与信息系统/chapter_concept_cards.md`** -- First 10 cards (most expanded chapter, representative of chapter card quality)
2. **`topics/by_topic/T-CASE-001/topic_qa_cards.md`** -- First 5 cards (S-tier, largest expansion from 6 to 40)
3. **`calculation_topics/by_topic/T-SCH-003/formula_cards.md`** -- All 5 formula cards (calculation accuracy check)

### Priority 2 (Risk Areas)
4. **`topics/by_topic/T-INFO-001/topic_qa_cards.md`** -- Sample 5 cards (thin topic package, representative of P0 supplements)
5. **`topics/by_topic/T-LAW-001/topic_qa_cards.md`** -- Sample 5 cards (legal accuracy risk)
6. **`question_cards/morning_choice_cards.md`** -- Cards 001, 010, 056 (OCR needs_human_review)

### Priority 3 (Edge Cases)
7. **`topics/by_topic/T-RISK-003/topic_qa_cards.md`** -- All 10 cards (smallest topic, B-tier, boundary-focused)
8. **`chapters/by_chapter/99_综合专题与跨域辨析/chapter_concept_cards.md`** -- All 12 cards (cross-domain chapter)

## Confidence Level by Card Category

| Category | Confidence | Rationale |
|---|---|---|
| Chapter Concept Cards | High | Stable textbook content; conservative A/B/C ratings; manageable scope (266 cards) |
| S-Tier Topic QA Cards | High | Deep topic packages (35-55 cards); enrichment targets met or exceeded |
| A-Tier Topic QA Cards | Medium-High | Good depth (18-25 cards); most topics well-covered |
| B-Tier Topic QA Cards | Medium | Smaller packages (10-15 cards); case templates need usage feedback |
| Calculation Formula Cards | Medium | Standard formulas correct; notation not textbook-verified |
| Calculation Trap/Comprehensive Cards | Medium | Edge cases covered but depth varies by topic |
| Question Cards (Morning Choice) | Medium | OCR quality is the main variable; answer accuracy is high |
| Question Cards (Case) | Medium-Low | Format unvalidated; pedagogical effectiveness unknown |
| T-INFO-001 Topic Cards | Low-Medium | Known thin; P0 supplement identified but not yet executed |
| T-LAW-001 Topic Cards | Low-Medium | Legal accuracy requires domain expert verification |
| T-CLOSE-001 Topic Cards | Low-Medium | Minimal depth; needs conceptual expansion |

## Recommendations for Next Iteration

### Must Fix
1. **Supplement P0 topic packages**: Execute the T-INFO-001, T-LAW-001, T-CLOSE-001 enrichment plan.
2. **Complete missing calculation cards**: Add ~22 trap and comprehensive cards to reach 150 target.
3. **Reconcile OCR-dependent question cards**: Manually verify and fix the ~5 flagged question cards.

### Should Fix
4. **Add more exam years**: Process 2011-2018 morning choice questions for fuller coverage.
5. **Cross-category deduplication**: Check for overlapping content between chapter concept and topic QA cards.
6. **Anki import test**: Verify card format compatibility with Anki (suggest using a small sample first).

### Nice to Have
7. **Case question format review**: Gather feedback on the summary + answer framework format.
8. **Spaced repetition schedule**: Recommend interval settings for different card categories.
9. **Progress tracking**: Add a simple tracking table for review completion across categories.
