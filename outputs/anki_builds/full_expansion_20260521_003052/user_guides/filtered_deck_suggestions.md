# 过滤卡组配置建议（Filtered Deck Suggestions）

## 概述

本文档提供 8 种不同学习场景的 Anki 过滤卡组（Filtered Deck）配置方案。这些配置直接使用 Anki 的"创建过滤卡组"功能，通过标签组合实现针对性的学习会话。

> 过滤卡组是临时卡组——学习完成后卡片会回到原卡组。建议设为"预览（Preview）"模式使用。

---

## 配置总览

| # | 场景 | 标签筛选 | 限制数量 | 适合阶段 |
|---|------|----------|----------|----------|
| 1 | 考前冲刺 | A 级卡 + 所有类别 | 100/天 | 考前 2-4 周 |
| 2 | 逐章学习 | 章节概念 + 关联专题 QA | 50-80/天 | 学习初期 |
| 3 | 计算强化 | 全部 7 个计算专题 | 30-50/天 | 中期巩固 |
| 4 | 上午模拟 | 真题上午选择题随机 | 75/天 | 考前 1-2 个月 |
| 5 | 案例练习 | 下午案例题 | 3-5 道/天 | 考前 2 个月 |
| 6 | 弱项攻坚 | 指定 1-2 个专题 | 30-50/天 | 任意阶段 |
| 7 | 跨域整合 | 多专题交叉训练 | 30-40/天 | 复习中期 |
| 8 | 新手入门 | A 级概念卡，限量 | 50（一次性） | 第 1 天 |

---

## 场景 1：考前冲刺

**目标：** 考前 2-4 周快速过所有 A 级（高频）卡片，覆盖概念、问答、计算、真题。

**过滤条件：**

```
tag:ruankao::importance::A
```

或更精确地组合：

```
tag:ruankao::importance::A -tag:ruankao::needs_review
```

| 设置项 | 推荐值 |
|--------|--------|
| 卡组 | 软考::系统集成项目管理工程师（或其子卡组） |
| 搜索 | `tag:ruankao::importance::A -tag:ruankao::needs_review` |
| 限制 | 100 张 |
| 顺序 | 到期时间递增（Due order） |
| 复习/新卡 | 仅复习（Reschedule based on my answers in this deck: ON） |

**学习策略：**
- 每天做 100 张 A 卡，约 1-1.5 小时
- 优先处理标记为 `flag:1`（红色）的困难卡
- 真题 A 卡重点看题干陷阱和干扰项设置方式

---

## 场景 2：逐章学习

**目标：** 在学习新章节时，同时复习该章的概念卡和关联专题问答卡，形成知识闭环。

**过滤条件（以第 4 章 整体管理为例）：**

```
tag:ruankao::chapter::04 OR tag:ruankao::topic::T-INT-002 OR tag:ruankao::topic::T-INT-004
```

| 设置项 | 推荐值 |
|--------|--------|
| 卡组 | 软考::系统集成项目管理工程师 |
| 搜索 | `tag:ruankao::chapter::04 OR tag:ruankao::topic::T-INT-002 OR tag:ruankao::topic::T-INT-004` |
| 限制 | 80 张 |
| 顺序 | 卡片类型排序（先概念后问答） |

**章节-专题映射参考：**

| 教材章节 | 关联专题 |
|----------|----------|
| 01_信息化与信息系统 | T-INFO-001, T-INFO-002 |
| 02_项目管理基础 | T-PM-002, T-ORG-001 |
| 03_立项管理 | T-FEA-001 |
| 04_整体管理 | T-INT-002, T-INT-004 |
| 05_范围管理 | T-SCOPE-002, T-SCOPE-003 |
| 06_进度管理 | T-SCH-002, T-SCH-003 |
| 07_成本管理 | T-COST-001, T-COST-002 |
| 08_质量管理 | T-QUAL-001, T-QUAL-002, T-QUAL-003 |
| 09_人力资源与沟通管理 | T-HR-001, T-COM-001, T-COM-002 |
| 10_干系人与风险管理 | T-RISK-001, T-RISK-002, T-RISK-003 |
| 11_采购与合同管理 | T-PROC-001, T-PROC-002 |
| 12_配置变更法律 | T-CFG-001, T-LAW-001 |
| 13_信息系统技术 | T-INFO-002 补充 |

---

## 场景 3：计算强化

**目标：** 集中练习全部 7 个计算专题，强化公式记忆和解题速度。

**总卡组配置：**

```
tag:ruankao::family::calculation
```

**分专题练习（逐个专题攻破）：**

| 计算专题 | 标签筛选 | 卡数 | 建议练习天数 |
|----------|----------|------|-------------|
| T-COST-002 挣值管理 | `tag:ruankao::topic::T-COST-002 tag:ruankao::family::calculation` | ~33 | 3 天 |
| T-SCH-003 关键路径 | `tag:ruankao::topic::T-SCH-003 tag:ruankao::family::calculation` | ~25 | 3 天 |
| T-RISK-002 EMV/决策树 | `tag:ruankao::topic::T-RISK-002 tag:ruankao::family::calculation` | ~20 | 2 天 |
| T-SCH-002 PERT | `tag:ruankao::topic::T-SCH-002 tag:ruankao::family::calculation` | ~16 | 2 天 |
| T-COM-001 沟通渠道 | `tag:ruankao::topic::T-COM-001 tag:ruankao::family::calculation` | ~13 | 1-2 天 |
| T-FEA-001 经济评价 | `tag:ruankao::topic::T-FEA-001 tag:ruankao::family::calculation` | ~13 | 1-2 天 |
| T-PROC-001 合同计算 | `tag:ruankao::topic::T-PROC-001 tag:ruankao::family::calculation` | ~8 | 1 天 |

**子类型筛选（进阶用法）：**

```
# 只看公式卡（先记公式）
tag:ruankao::card_type::formula tag:ruankao::family::calculation

# 只看陷阱卡（冲刺阶段攻防）
tag:ruankao::card_type::trap tag:ruankao::family::calculation

# 只看综合计算卡（检验综合运用能力）
tag:ruankao::card_type::comprehensive tag:ruankao::family::calculation
```

**学习策略：**
- 先做公式卡，确保每个公式的变量含义和适用场景清晰
- 再做基础计算卡，在草稿纸上完整演算
- 最后做陷阱卡，重点关注常见错误模式
- 计算卡不要隔太久复习——建议连续几天集中攻克一个专题

---

## 场景 4：上午模拟

**目标：** 随机抽取上午选择题，模拟真实考试的选择题部分。

**过滤条件：**

```
tag:ruankao::family::question tag:ruankao::question_type::morning_choice
```

| 设置项 | 推荐值 |
|--------|--------|
| 卡组 | 软考::系统集成项目管理工程师::真题刷题卡::上午选择题 |
| 搜索 | `tag:ruankao::family::question tag:ruankao::question_type::morning_choice` |
| 限制 | 75 张（一次模拟的量） |
| 顺序 | 随机（Random） |
| 复习/新卡 | 仅复习 |

**学习策略：**
- 设定 90 分钟完成 75 道题（模拟真实考试节奏）
- 每道题先用脑中选出答案，再看背面验证
- 记录错题和犹豫题，之后针对这些知识点返回专题问答卡复习
- 完成后用 `flag:2`（橙色）标记错题，下次模拟前先过一遍

---

## 场景 5：案例练习

**目标：** 集中练习下午案例题的审题-分析-答题框架训练。

**过滤条件：**

```
tag:ruankao::family::question tag:ruankao::question_type::case_question
```

或包含案例专题的更深层训练：

```
tag:ruankao::family::question tag:ruankao::question_type::case_question OR tag:ruankao::topic::T-CASE-001 OR tag:ruankao::topic::T-CASE-002 OR tag:ruankao::topic::T-CASE-003
```

| 设置项 | 推荐值 |
|--------|--------|
| 卡组 | 软考::系统集成项目管理工程师::真题刷题卡::下午案例题 |
| 搜索 | `tag:ruankao::question_type::case_question` |
| 限制 | 5 张 |
| 顺序 | 随机 |

**学习策略：**
- 案例卡需要"主动输出"——不要只看不写
- 对每道案例，在纸上列出"问题→知识点→解决措施"的框架
- 对比答案框架时，重点找自己的遗漏点和表述差异
- 同一个案例建议隔 2-3 天再做一次，检验是否真正掌握了答题框架

---

## 场景 6：弱项攻坚

**目标：** 针对模拟考试或复习中发现的薄弱专题，集中突破。

**过滤条件（示例：质量管理薄弱）：**

```
tag:ruankao::topic::T-QUAL-001 OR tag:ruankao::topic::T-QUAL-002 OR tag:ruankao::topic::T-QUAL-003
```

**过滤条件（示例：法律法规薄弱）：**

```
tag:ruankao::topic::T-LAW-001
```

| 设置项 | 推荐值 |
|--------|--------|
| 搜索 | 对应专题的标签组合 |
| 限制 | 40 张 |
| 顺序 | 按卡片类型顺序（概念→辨析→流程→案例） |

**如何识别弱项：**
1. 在 Anki 浏览窗口搜索 `rated:1`（得分为 1 的困难卡）
2. 按专题标签分组统计困难卡分布
3. 困难卡最集中的 2-3 个专题 = 你的弱项

---

## 场景 7：跨域整合

**目标：** 同时复习多个关联专题，训练知识迁移能力——这是考试中高分段的关键。

**过滤条件（跨域辨析示例）：**

```
tag:ruankao::topic::T-CROSS-001 OR tag:ruankao::topic::T-COST-001 OR tag:ruankao::topic::T-SCOPE-003
```

**推荐跨域组合训练：**

| 组合 | 涉及专题 | 训练目标 |
|------|----------|----------|
| 范围-成本-进度三角 | T-SCOPE-002, T-COST-001, T-SCH-003 | 三大基准的关联和权衡 |
| 质量-风险-变更 | T-QUAL-001, T-RISK-001, T-INT-004 | 问题发现→登记→变更控制流程 |
| 采购-合同-法律 | T-PROC-001, T-PROC-002, T-LAW-001 | 采购全流程法律风险点 |
| 组织-沟通-干系人 | T-ORG-001, T-COM-001, T-RISK-001 | 人的因素对项目的影响 |
| 信息化全貌 | T-INFO-001, T-INFO-002, T-CFG-001 | IT 基础知识综合 |

| 设置项 | 推荐值 |
|--------|--------|
| 搜索 | 组合中的专题标签 OR 连接 |
| 限制 | 40 张 |
| 顺序 | 随机 |

---

## 场景 8：新手入门

**目标：** 适用于刚开始接触软考的学习者——限量、精选、建立信心。

**过滤条件：**

```
tag:ruankao::family::chapter_concept tag:ruankao::importance::A (tag:ruankao::chapter::01 OR tag:ruankao::chapter::02)
```

| 设置项 | 推荐值 |
|--------|--------|
| 搜索 | `tag:ruankao::family::chapter_concept tag:ruankao::importance::A tag:ruankao::chapter::01` |
| 限制 | 50 张 |
| 顺序 | 随机 |

**后续扩展：**
- 第 1-3 天：完成 01-02 章 A 卡（约 50 张）
- 第 4-7 天：扩大到 01-03 章 A 卡 + B 卡（约 100 张）
- 第 2 周：加入 T-INFO-001 和 T-PM-002 专题 A 卡（约 30 张）
- 第 3 周起：按正常学习路线推进

---

## 进阶用法

### 组合多个条件

你可以将多个条件组合使用，创建更精细的过滤卡组：

```
# A级计算陷阱卡（考前计算重点攻防）
tag:ruankao::importance::A tag:ruankao::family::calculation tag:ruankao::card_type::trap

# 2019 年所有卡片（考前模拟该年份）
tag:ruankao::year::2019 -tag:ruankao::needs_review

# 近 7 天新增的卡片（检验最新学习内容）
added:7
```

### 配合 Flag 进行错题重做

1. 在卡片学习中，对答错的题按 `Ctrl+1` 标记为 flag:1（红色）
2. 创建过滤卡组搜索 `flag:1`，只复习错题
3. 每周做一次错题重做过滤卡组

### 考前 1 周的极限冲刺

```
# 第一天：A 卡全扫（200 张/天）
tag:ruankao::importance::A

# 第二天：计算卡全扫 + 陷阱卡专项
tag:ruankao::family::calculation

# 第三天：真题模拟（75 道选择 + 5 道案例）
tag:ruankao::family::question

# 第四天：错题重做（所有 flag 标记卡）
flag:1 OR flag:2

# 第五天：弱项专题扫尾
tag:ruankao::topic::T-CROSS-001 OR tag:ruankao::topic::T-COST-002

# 第六天：自由复习（到期卡复习）
is:due
```
