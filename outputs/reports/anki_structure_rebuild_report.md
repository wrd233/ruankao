# Anki 结构重建报告

## Phase 1：审计当前目录和旧 Anki 输出

发现主输出路径包含：

- 旧全量 build：`outputs/anki_full_build_20260520_221409`
- 质量重建 build：`outputs/anki_quality_rebuild_20260520_223914`
- 手工单专题样例：`outputs/anki_manual_single_topic_T-FEA-001_20260520_225554`

旧 build 已不适合作为当前工作入口。

## Phase 2：清理/归档旧产物并建立新目录

已创建：

```text
outputs/anki_builds/current_samples/
outputs/anki_builds/archive/deprecated_anki_builds/
outputs/reports/
docs/anki/
docs/skills/
```

旧全量 build 和脚本化质量 build 已归档。

上一轮手工单专题样例也已迁移到：

```text
outputs/anki_builds/archive/manual_single_topic_samples/anki_manual_single_topic_T-FEA-001_20260520_225554/
```

其关键文件已复制到 `current_samples/` 作为当前入口。

## Phase 3：沉淀 Skill 和 Anki 规范文档

新增：

```text
docs/skills/ruankao_topic_package_and_anki_card_skill.md
docs/anki/deck_architecture.md
docs/anki/chapter_concept_card_spec.md
docs/anki/review_workflow.md
docs/anki/README.md
```

Skill 明确禁止代码质量评分工具，禁止输出 `quality_score` 字段，要求逐张自然语言自评。

## Phase 4：创建 03_立项管理章节概念卡样例

新增：

```text
outputs/anki_builds/current_samples/03_立项管理_chapter_concept_cards.csv
outputs/anki_builds/current_samples/03_立项管理_chapter_concept_cards.md
outputs/anki_builds/current_samples/03_立项管理_combined_sample_preview.csv
outputs/anki_builds/current_samples/import_preview.csv
```

数量：

- 章节概念卡：38 张
- keep：35 张
- needs_human_review：3 张

## Phase 5：自然语言自评和样例包输出

新增：

```text
outputs/anki_builds/current_samples/manual_self_review.md
outputs/anki_builds/current_samples/sample_review_pack.md
outputs/anki_builds/current_samples/README.md
```

样例包包含章节概念卡、专题问答卡、待核验卡和拒绝样例。

## Phase 6：最终报告

当前双轨样例已经可以进入用户人工验收，但不能直接全量导入。

```text
FINAL_DECISION: READY_FOR_USER_REVIEW_SAMPLE_ONLY
NOT_READY_FOR_FULL_IMPORT_UNTIL_USER_REVIEW
```
