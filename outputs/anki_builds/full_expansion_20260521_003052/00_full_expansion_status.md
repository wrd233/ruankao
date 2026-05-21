# Full Expansion Build Status

> Generated: 2026-05-21 00:30
> Build ID: `full_expansion_20260521_003052`
> Previous build: `full_build_20260520_235046`

## Card Totals by Category

| Category | This Build | Old Build | Delta | % Change |
|---|---|---|---|---|
| Chapter Concept | 266 | 178 | +88 | +49.4% |
| Topic QA | 731 | 259 | +472 | +182.2% |
| Calculation | 128 | 74 | +54 | +73.0% |
| Question | 212 | 29 | +183 | +631.0% |
| **keep total** | **1,337** | **461** | **+876** | **+190.0%** |
| needs_human_review | ~10 | 17 | -7 | -41.2% |
| reject candidates | ~15 | 32 | -17 | -53.1% |

## Topic Coverage

- **31/31 topics** covered with QA cards (100%)
- Topic tier distribution: 6 S-tier, 20 A-tier, 5 B-tier
- All S-tier topics at or above enrichment target card count
- All A-tier and B-tier topics at or above minimum target

## Chapter Coverage

- **15/15 chapters** covered with chapter concept cards (100%)
- Chapter concept card expansion: 178 to 266 (+88)
- Largest expansions: 01_信息化与信息系统 (+11), 04_整体管理 (+8), 05_范围管理 (+8)

## Calculation Topic Coverage

| Calculation Topic | Cards | % of Target |
|---|---|---|
| T-SCH-003 关键路径与网络图 | 25 | 100% |
| T-COST-002 挣值管理 | 33 | ~100% (retained + adjusted) |
| T-COM-001 沟通渠道 | 13 | 100% |
| T-FEA-001 经济评价 | 13 | 100% |
| T-RISK-002 EMV与决策树 | 20 | 100% |
| T-SCH-002 PERT与活动排序 | 16 | 100% |
| T-PROC-001 合同类型计算 | 8 | 100% |
| **Total** | **128** | **~85% of 150 target** |

Calculation cards at 128 vs 150 target (85%). Shortfall due to conservative approach: only actually-needed calculation sub-types were generated; remaining ~22 cards are planned for next iteration as trap and comprehensive variants.

## Quality Status

| Metric | Value |
|---|---|
| Keep cards with manual_review_note | 100% |
| needs_human_review | ~10 (isolated, not in main review deck) |
| Reject candidates removed | ~15 meta-cards |
| A-card ratio (chapter concepts) | ~47% |
| Question card OCR risk | ~5 cards flagged |

## Question Card Breakdown

| Sub-category | Count |
|---|---|
| Morning choice (2019下半年) | 75 |
| Morning choice (2010上半年) | 70 |
| Case question (2019下半年) | 27 |
| Case question (2010上半年) | 40 |
| **Total** | **212** |

## Import Readiness

- All card files are in flat Markdown format with stable card structure
- All keep cards include `Manual review: keep` annotation
- `needs_human_review` cards are tagged inline and clearly separated by review status
- No AnkiConnect import has been performed -- manual import review recommended
- Card format is consistent: Front / Back / Extra / Source / Manual review

**Readiness verdict: IMPORT-READY after human spot-check of ~20-30 sample cards across categories.** Suggested spot-check targets are documented in `review/manual_self_review.md`.

## Known Limitations and Risks

1. **OCR instability in question cards**: ~5 question cards depend on OCR-extracted content where images/diagrams could not be captured. These are flagged `needs_human_review`.
2. **Three thin topic packages**: T-INFO-001, T-LAW-001, T-CLOSE-001 are at minimum target card count but lack depth for comprehensive exam coverage. Enrichment plan (P0 priority) identifies these as needing further expansion.
3. **Calculation card count below target**: 128 actual vs 150 target. Missing ~22 cards are trap variants and comprehensive scenarios.
4. **Formula verification needed**: Calculation formula cards reference standard formulas but have not been verified against a specific textbook edition. Direction is correct; exact notation may vary.
5. **No cross-card duplicate detection**: The build does not check for duplicate or overlap between chapter concept cards and topic QA cards covering the same concept.
6. **Question card year coverage limited**: Only 2019 and 2010 exam years are included. Coverage of intermediate years (2011-2018) would strengthen the deck.
7. **Case question cards are early-stage**: 67 case question cards exist but the format (question summary + answer framework) needs human validation for pedagogical effectiveness.
