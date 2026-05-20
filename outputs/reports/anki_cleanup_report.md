# Anki 清理报告

## 清理动作

已将旧的全量/脚本化 Anki build 从主输出路径移入归档目录：

```text
outputs/anki_builds/archive/deprecated_anki_builds/anki_full_build_20260520_221409/
outputs/anki_builds/archive/deprecated_anki_builds/anki_quality_rebuild_20260520_223914/
```

已将质量重建期遗留的未跟踪脚本归档：

```text
outputs/anki_builds/archive/deprecated_anki_builds/legacy_quality_rebuild_scripts_20260520_223914/
```

## 保留资产

- EVM 黄金样例：`anki_pilot/T-COST-002/`
- 单专题手工样例原目录：`outputs/anki_builds/archive/manual_single_topic_samples/anki_manual_single_topic_T-FEA-001_20260520_225554/`
- 当前样例入口：`outputs/anki_builds/current_samples/`
- 项目级 Skill：`docs/skills/ruankao_topic_package_and_anki_card_skill.md`
- Anki 规范：`docs/anki/`

## 新目录结构

```text
docs/
  anki/
    README.md
    deck_architecture.md
    chapter_concept_card_spec.md
    review_workflow.md
  skills/
    ruankao_topic_package_and_anki_card_skill.md

outputs/
  anki_builds/
    current_samples/
    archive/
      deprecated_anki_builds/
      manual_single_topic_samples/
  reports/
    anki_cleanup_report.md
    anki_structure_rebuild_report.md
```

## 当前样例入口

```text
outputs/anki_builds/current_samples/README.md
outputs/anki_builds/current_samples/03_立项管理_chapter_concept_cards.md
outputs/anki_builds/current_samples/T-FEA-001_topic_qa_cards.md
outputs/anki_builds/current_samples/sample_review_pack.md
```

## 不应继续使用的旧产物

归档目录中的两个旧 build 不应作为后续制卡质量基准：

- `anki_full_build_20260520_221409`：存在模板卡、元卡片和自动高分问题。
- `anki_quality_rebuild_20260520_223914`：虽然做过工程化修复并导入过 Anki，但仍依赖脚本化全量生成和自动评分思路，不作为新标准。

后续应以 EVM 黄金样例、T-FEA 手工样例和本轮双轨样例为基准。
