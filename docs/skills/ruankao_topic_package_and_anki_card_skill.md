# 软考专题学习包与 Anki 双轨制卡 Skill

## 1. 项目目标与知识资产分层

本项目目标不是批量生成很多卡，而是把软考「系统集成项目管理工程师」资料转化为可维护、可审稿、可筛选、可导入、可复习、可反馈迭代的 Anki 学习资产。

知识资产分层：

1. 原始材料层：教程 OCR、真题 OCR、PDF、清洗文本。
2. 索引层：topic manifest、coverage matrix、exam question map、pending verification register。
3. 专题学习包层：面向理解的讲义、图、例题和待核验记录。
4. 制卡设计层：深度阅读笔记、source map、候选考点、卡片设计计划。
5. Anki 卡片层：章节概念卡、专题问答卡、真题刷题卡、跨专题辨析卡、待核验卡。
6. 反馈层：错题、连续遗忘卡、低质量卡、教材核验结果。

专题讲义负责“讲懂”，Anki 卡片负责“主动回忆”。不能把讲义直接切成卡片。

## 2. 原始材料、专题学习包、真题、Anki 卡片的关系

原始材料提供权威口径；专题学习包把原始材料组织成学习主线；真题暴露考试问法和陷阱；Anki 卡片只承载值得反复回忆的最小知识单元。

制卡时的链路必须清楚：

```text
原始来源或专题段落 -> 考点判断 -> 卡片 Front/Back/Extra -> 人工自评 -> 用户抽样验收
```

Source grounding 必须保留在字段中，但不能污染卡背。

## 3. 专题学习包制作标准

一个好的专题学习包应包含：

- 专题主线：这个专题解决什么问题。
- 考试方式：上午选择、下午案例、计算题或跨域辨析。
- 核心概念：定义、对象、边界。
- 流程或公式：能实际用于判断和计算。
- 易混点：与相邻专题的边界。
- 典型题或真题型训练：题干信号、错项分析。
- 待核验项：法规数字、标准编号、OCR 疑点、教材版本差异。

专题学习包可以长，可以解释背景；Anki 卡必须短、明确、稳定。

## 4. 专题问答卡制作标准

专题问答卡面向考试反应。它回答：

- 题干问这个场景时应想到什么？
- A 和 B 怎么区别？
- 遇到 X 场景按什么流程处理？
- 哪个错项为什么错？
- 案例题应从哪些维度诊断？

典型卡型：

- 概念理解卡
- 辨析卡
- 流程卡
- 关键词识别卡
- 陷阱卡
- 案例模板卡
- 公式/计算卡
- 真题反哺卡

Front 必须具体，禁止泛泛问“某专题的考试要点是什么”。Back 必须是最小稳定答案。Extra 必须服务本卡，不写通用套话。

## 5. 章节概念卡制作标准

章节概念卡面向章节内术语、文件、过程、角色、输出物和规则的稳定识别。它像“章节概念词典”，但不是百科摘抄。

可以进入：

- 项目建议书、可行性研究、项目评估等术语。
- 可研报告、项目章程、项目管理计划等文档。
- 机会研究、初步可研、详细可研等阶段。
- 审批部门、咨询评估机构等角色。
- 技术可行性、财务可行性、社会可行性等维度。
- 重大变更重新报批等规则。

不能进入：

- 小节标题。
- 专题导语。
- 制卡建议。
- 真题覆盖增强说明。
- 大段来源摘抄。

章节概念卡和专题问答卡允许合理冗余。例如“项目建议书是什么？”和“项目建议书 vs 项目章程的区别是什么？”可以共存；“项目建议书是什么？”和“项目建议书的定义是什么？”不应共存。

## 6. 真题刷题卡制作标准

真题卡必须保留：

- 年份、场次、题号。
- 完整题干。
- A/B/C/D 选项。
- 答案。
- 解析。
- 错项分析。
- 题干信号。
- 关联专题。
- 可迁移考点。

题干、选项、答案、解析边界不稳定时，不得进入正式卡。可以进入 `needs_human_review`，但必须隔离。

不能把真题改写成普通概念卡后丢掉选项。

## 7. 待核验卡与法规数字处理规则

涉及以下内容必须谨慎：

- 法规数字、年限、比例、金额。
- 标准编号和版本。
- 教材版本口径差异。
- OCR 疑似错字。
- 真题解析边界不稳。

处理方式：

```text
manual_review_status = needs_human_review
tags += ruankao::needs_review ruankao::not_for_main_review
```

Back 可以写稳定方向，不能强行让用户背未经核验的数字。

## 8. 卡组结构与标签体系

推荐卡组：

```text
软考::系统集成项目管理工程师
  03_立项管理
    专题问答卡
      T-FEA-001_立项管理_项目建议书_可行性研究与项目论证
    章节概念卡
      03_立项管理_概念卡
  真题刷题
  跨专题辨析
  待核验与复查
```

推荐标签：

```text
ruankao
ruankao::family::chapter_concept
ruankao::family::topic_qa
ruankao::chapter::03
ruankao::topic::T-FEA-001
ruankao::domain::立项管理
ruankao::needs_review
ruankao::not_for_main_review
```

## 9. 字段规范与 checksum/幂等更新

推荐字段：

```text
deck,note_type,front,back,extra,card_family,card_type,concept_name,concept_aliases,
importance,difficulty,exam_use,knowledge_domain,chapter_id,chapter_name,
source_topic_ids,source_topic_names,source_ids,source_file,source_heading,
related_question_ids,related_topic_ids,manual_review_status,manual_review_note,tags,checksum
```

Checksum 可由以下稳定字段生成：

```text
chapter_id + card_family + card_type + front + back
```

Checksum 用于幂等更新，不用于判断质量。

## 10. Source grounding 规则

每张卡必须能回溯来源：

- `source_ids`
- `source_file`
- `source_heading`
- `related_question_ids`

但卡背只写极短来源提示，例如：

```text
来源：tutorial 5.2.1。
```

禁止把 source excerpt 大段塞入 Extra。来源字段服务审稿，不服务日常复习。

## 11. 人工自评规则

不得使用代码质量评分工具评价卡片质量。不得输出 `quality_score`。卡片质量由制卡者逐张自然语言自评，并接受人工抽样验收。

每张卡必须问：

1. Front 是否明确触发主动回忆？
2. Back 是否是最小稳定答案？
3. 是否只考一个点？
4. Extra 是否专属于本卡？
5. 是否能服务考试？
6. 是否只是标题、摘抄或元说明？
7. 是否和其他卡同义重复？
8. 是否存在来源冲突或待核验？

状态只能是：

```text
keep / revise / needs_human_review / reject
```

## 12. 黄金样例风格

黄金样例包括：

- T-COST-002 EVM 试制卡：短 Front、最小 Back、Extra 直指关键词和易错点。
- T-FEA-001 手工样例：具体问题、短答案、专属 Extra、自然语言自评。

目标风格：

```text
Front: PV 是什么？
Back: 计划价值：到某一时点，按计划应该完成工作的预算价值。
Extra: 关键词是“计划应该”。PV 不看实际完成情况。
```

迁移到立项管理：

```text
Front: 项目建议书是什么？
Back: 项目建议书是立项前提出拟建项目总体设想和立项申请的文件，为项目选择和后续可行性研究提供依据。
Extra: 易错点：不要和项目章程混淆。
```

## 13. 坏卡反例库

必须拒绝：

```text
Front: 某专题的考试要点是什么？
Front: 某标题的考试判断要点是什么？
Front: 本轮真题覆盖增强的考试要点是什么？
Front: 这个专题应该怎样转化为 Anki 卡片？
Back: 长篇教材摘抄。
Extra: 抓住题干中的对象、动作和输出。
Extra: 避免把相邻概念按字面相似性混用。
```

真题坏卡：

- 丢选项。
- 答案和题干错位。
- 解析串到上一题或下一题。
- OCR 不稳却写成确定答案。

## 14. 单专题验收流程

1. 选择一个章节/专题。
2. 阅读 Skill、方法论、黄金样例和失败样例。
3. 阅读专题包、教程 OCR、真题 OCR、索引和待核验登记。
4. 写深度阅读笔记和 source map。
5. 写候选考点。
6. 手工写卡。
7. 逐张自然语言自评。
8. 输出 CSV 和人类可读 Markdown。
9. 交给用户确认风格。

## 15. 全量扩展前的门禁

全量扩展前必须满足：

- 样例风格被用户接受。
- 章节概念卡和专题问答卡边界清楚。
- needs_human_review 隔离策略被确认。
- 真题解析边界有稳定解析方案。
- 不再依赖代码评分工具。

## 16. AnkiConnect 导入前检查

导入前只做检查：

- AnkiConnect 是否可用。
- NoteType 字段是否匹配。
- Deck 路径是否正确。
- Checksum 是否重复。
- needs_human_review 是否进入待核验卡组。
- 是否有旧坏卡需要暂停、移动或删除。

未获得用户明确同意前，不执行 addNotes/updateNoteFields/deleteNotes。

## 17. 复习反馈如何回流

用户复习中发现问题后，用标签标记：

```text
ruankao::feedback::too_hard
ruankao::feedback::ambiguous_front
ruankao::feedback::too_long_back
ruankao::feedback::wrong_answer
ruankao::feedback::needs_example
ruankao::feedback::from_wrong_question
```

反馈处理：

- 连续遗忘：拆卡、改 Front、补例子。
- 答案歧义：改 Back 为可判分答案。
- 真题错：回查原题和解析边界。
- 法规数字错：回到待核验登记。
- 某类题反复错：反推缺少辨析卡或题干信号卡。

## 18. 全量双轨构建补充规则

全量构建必须同时产出每章章节概念卡、每个 manifest 专题的专题问答卡、计算专题的公式/计算/陷阱/案例表达链条、真题刷题卡和解析待核验报告。

全量构建仍然不得使用代码质量评分。脚本只允许做目录遍历、CSV 写入、checksum、字段缺失检查和完全重复 Front 检查。卡片是否保留，必须由制卡者逐张阅读后写入自然语言 `manual_review_note`。
