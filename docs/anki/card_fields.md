# 软考 Anki 字段规范

推荐字段顺序：

```text
deck,note_type,front,back,extra,card_family,card_type,concept_name,concept_aliases,
importance,difficulty,exam_use,knowledge_domain,chapter_id,chapter_name,
source_topic_ids,source_topic_names,source_ids,source_file,source_heading,
related_question_ids,related_topic_ids,manual_review_status,manual_review_note,tags,checksum
```

## 核心字段

- `card_family`：`chapter_concept`、`topic_qa`、`calculation`、`question`。
- `manual_review_status`：只允许 `keep`、`revise`、`needs_human_review`、`reject`。
- `manual_review_note`：自然语言审稿理由。
- `checksum`：幂等更新用，不代表质量。

## 禁止字段

不得输出 `quality_score`。不得使用自动质量分作为导入依据。

## 待核验隔离

`needs_human_review` 卡必须进入 `软考::系统集成项目管理工程师::待核验与复查`，并带 `ruankao::needs_review` 与 `ruankao::not_for_main_review`。
