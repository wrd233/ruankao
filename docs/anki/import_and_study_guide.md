# 软考 Anki 导入与学习指南

## 导入前

先人工抽查 full build 中的：

- `review/sample_review_pack.md`
- `aggregate/import_preview_keep_only.csv`
- `aggregate/all_needs_human_review_cards.csv`

本项目默认不直接调用 AnkiConnect `addNotes`。确认后再导入。

## 推荐导入文件

优先导入：

```text
outputs/anki_builds/full_build_<timestamp>/aggregate/import_preview_keep_only.csv
```

不要把 `all_needs_human_review_cards.csv` 导入主复习卡组。

## 学习顺序

1. 新章节：先刷章节概念卡。
2. 进入专题：刷专题问答卡。
3. 计算题：单独刷计算专题卡。
4. 做题阶段：刷真题刷题卡。
5. 考前：筛选 A 级、计算、跨域辨析和错题回炉卡。

## 筛选示例

```text
tag:ruankao::chapter_concept
tag:ruankao::topic_qa
tag:ruankao::calculation
tag:ruankao::question
tag:ruankao::importance::A
tag:ruankao::needs_review
```

## 反馈闭环

连续遗忘的卡优先拆分、改写 Front 或补充例子。不要靠 FSRS 硬背坏卡。
