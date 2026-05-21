# Not Ready Items -- Needs Human Attention

> Items that require human verification, supplementation, or remediation before the deck can be considered fully production-ready.

## 1. Cards Marked `needs_human_review`

Approximately 10 cards across the build carry the `needs_human_review` tag. They are isolated from the main review deck and should not be included in Anki import until resolved.

### OCR-Vulnerable Question Cards (6 cards)

All in `question_cards/morning_choice_cards.md`:

| Card ID | Issue | Action Required |
|---|---|---|
| Card 001 | Diagram-dependent (国家信息化体系六要素关系图) | Confirm answer B is correct by viewing the original exam diagram |
| Card 010 | OCR lost the question stem entirely | Locate original exam question and re-add stem |
| Card 021 | Option labels corrupted/mixed between C and D | Verify original options and fix formatting |
| Card 036 | Diagram-dependent (前导图/PND四个图例) | Confirm which image matches SS relationship |
| Card 056 | Diagram-dependent (箭线图/ADM) | Confirm arrow diagram description matches A answer |
| Card 070 | OCR lost the question stem entirely | Locate original exam question and re-add stem |

### Ambiguous Knowledge Topic Cards (~4 cards)

Distributed across topic QA files. These cards present exam-conflicting or textbook-ambiguous information.

**T-FEA-001 (立项管理)** -- `topic_qa_cards.md`:

| Approx. Card | Issue | Action Required |
|---|---|---|
| (项目建议书内容) | 真题将"风险因素及对策"列为"不属于项目建议书核心内容"，但教程提纲列有"项目风险与风险对策"章节 | Decide whether to include or exclude based on exam trend analysis |
| (可行性研究精度) | 机会研究约±30%、初步可研约±20%、详细可研约±10% -- 数字频繁出现在不同教材版本中 | Verify against official textbook edition |
| (重大变更报批) | 教程写到"重大变更或投资超出已批复总投资额度10%时，应重新报批可行性研究报告" | Verify the 10% threshold against current regulations |

### Resolution Plan for needs_human_review Cards

| Priority | Cards | Action |
|---|---|---|
| P0 | OCR-stem-lost (Cards 010, 070) | Reconstruct from original exam; ~5 min each |
| P0 | Diagram-dependent (Cards 001, 036, 056) | View original exam and confirm answer; ~3 min each |
| P1 | Ambiguous numbers (FEA-001) | Check official 教程 3rd edition; ~10 min |
| P2 | Answer judgment calls | Make a keep/reject decision; ~5 min |

Estimated total: ~30-40 minutes of human review to resolve all ~10 flagged cards.

## 2. Topic Packages Needing Supplementation

Three topic packages (P0 priority from enrichment plan) have been expanded from the old build's 6 cards but remain below the depth needed for comprehensive exam coverage.

### T-INFO-001: 信息化/信息系统生命周期 (20 cards, A-tier)

**Current coverage**: Information definition, IS definition, informatization concept, basic lifecycle phases, national informatization system (6 elements -- surface level).

**Missing content**:
- 信息化体系六要素 detailed breakdown and inter-relationships
- 电子商务模式 (B2B/B2C/C2C/O2O) with exam-style distinctions
- 电子政务类型 (G2G/G2B/G2C/G2E)
- ITIL/ITSM 基础概念
- 信息系统生命周期 vs 产品生命周期 vs 项目生命周期 comparison
- 系统集成资质管理 basics

**Supplementation target**: 35-40 cards (current: 20)

### T-LAW-001: 法律法规/合同法/招投标法 (22 cards, A-tier)

**Current coverage**: Basic legal terms, contract types, bidding process steps, intellectual property overview.

**Missing/risky content**:
- 知识产权法细则 (著作权法、专利法、商标法 coverage is shallow)
- 软件著作权 vs 专利权 protection boundary
- 委托开发 vs 合作开发 权属规则 (exam-frequent)
- 标准代号体系 (国家标准 GB, 行业标准, 国际标准 ISO) -- numbers need verification
- 招标投标法实施条例 details (time limits, 废标 conditions)
- 政府采购法 key thresholds and procedures

**Critical risk**: Legal numbers (time limits for bid submission, objection periods, copyright duration) vary across exam editions. Every legal number in these cards should be verified against the current 教程.

**Supplementation target**: 30-35 cards (current: 22)

### T-CLOSE-001: 项目收尾/管理收尾/合同收尾 (15 cards, A-tier)

**Current coverage**: Basic closure concepts, admin vs contract closure distinction, closure checklist items.

**Missing content**:
- 管理收尾 vs 合同收尾完整对比 (full dimension-by-dimension comparison)
- 收尾 ITTO (inputs, tools/techniques, outputs) for Close Project or Phase
- 项目验收流程 and 验收报告 structure
- 项目后评价 (post-project evaluation) types and methods
- 知识转移/经验教训总结库
- 组织过程资产更新 in closure context

**Supplementation target**: 25-30 cards (current: 15)

## 3. OCR-Unstable Question Cards

Beyond the 6 needs_human_review flags, the following question cards may have latent OCR issues:

- **`question_cards/morning_choice_cards_2010.md`**: 70 cards processed from 2010 exam. OCR quality assessment was not done at the individual card level for this file. Recommend scanning cards that reference "diagram", "figure", or contain fragmented text.
- **`question_cards/case_question_cards.md`** and **`question_cards/case_question_cards_2010.md`**: 67 case cards. OCR quality for case questions is generally lower because case narratives can span multiple lines with formatting loss.

## 4. Legal/Regulatory Numbers Needing Verification

The following cards contain hard numbers that should be verified against the official 软考教程 (3rd edition or current):

| Topic | Number | Card Location |
|---|---|---|
| T-LAW-001 | 投标截止时间(开标时间) | topic QA cards |
| T-LAW-001 | 中标通知书发出后合同签订期限(30日) | topic QA cards |
| T-LAW-001 | 招标文件澄清/修改截止期限 | topic QA cards |
| T-LAW-001 | 质疑答复期限 | topic QA cards |
| T-LAW-001 | 软件著作权保护期限 | topic QA cards |
| T-FEA-001 | 可行性研究精度范围(±30%/±20%/±10%) | topic QA cards (needs_human_review flagged) |
| T-FEA-001 | 重大变更重新报批阈值(10%) | topic QA cards (needs_human_review flagged) |

## 5. Calculation Formulas Needing Textbook Verification

The following formula cards use standard PM formulas that are directionally correct but have not been textbook-verified:

| File | Formulas |
|---|---|
| `calculation_topics/by_topic/T-SCH-003/formula_cards.md` | TF=LS-ES=LF-EF, FF=min(后续ES)-EF, PERT 期望值=(O+4M+P)/6, 标准差=(P-O)/6 |
| `calculation_topics/by_topic/T-SCH-002/formula_cards.md` | PERT variance, 依赖关系类型 |
| `calculation_topics/by_topic/T-RISK-002/formula_cards.md` | EMV=Σ(P×I), 决策树计算 |
| `calculation_topics/by_topic/T-FEA-001/formula_cards.md` | NPV, IRR, 投资回收期 |
| `calculation_topics/by_topic/T-COST-002/formula_cards.md` | EVM 指标(CV, SV, CPI, SPI, EAC, ETC, TCPI) |

These formulas are well-established PM standards; the risk is not accuracy but presentation wording matching the exam.

## Summary of Human Effort Required

| Item | Est. Effort | Priority |
|---|---|---|
| Resolve 6 OCR question cards | 30 min | Before Anki import |
| Resolve 3-4 ambiguous topic cards | 20 min | Before Anki import |
| Supplement T-INFO-001 (15-20 cards) | 60-90 min | Next iteration |
| Supplement T-LAW-001 (8-13 cards) | 45-60 min | Next iteration |
| Supplement T-CLOSE-001 (10-15 cards) | 30-45 min | Next iteration |
| Verify legal/regulatory numbers | 30 min | Before Anki import (or flag all as needs_human_review) |
| Verify calculation formulas | 20 min | Optional (low risk) |
| **Total** | **~4-5 hours** | |
