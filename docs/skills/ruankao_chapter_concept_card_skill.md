# 软考章节概念卡 Skill

章节概念卡用于建立每章的术语底座，覆盖概念、文档、过程、角色、输出物、指标、规则和稳定边界。它不是专题摘要，也不是教材目录卡。

## 制卡流程

1. 读取本章所有正式专题包。
2. 回查 `topic_build_full/topics/` 中同章细分材料。
3. 必要时回查 `tutorial.full.clean.md` 和 `questions.full.clean.md`。
4. 抽取本章必须稳定识别的概念。
5. 为每个概念写短 Front、短 Back、针对性 Extra。
6. 写自然语言 `manual_review_note`，不用代码打分。

## 写法

Front 优先使用 `X 是什么？`、`X 主要解决什么问题？`、`X 和 Y 最容易混淆的边界是什么？`。禁止使用“本章的考试要点是什么”或“这个专题应该怎样转化为 Anki 卡片”。

Back 一般 1 句话，最多 2 句话。Extra 只放理解、易错点、题干信号、关联和极短来源，不放大段原文。

## 审稿

状态只允许 `keep`、`revise`、`needs_human_review`、`reject`。不得使用代码质量评分工具，不得输出 `quality_score` 字段。
