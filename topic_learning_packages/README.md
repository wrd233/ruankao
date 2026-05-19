# 软考专题学习包目录

本目录存放"系统集成项目管理工程师"正式专题学习包。每个专题学习包都是一篇可独立阅读的 Markdown 讲义，用于连接"全量 OCR/索引材料"和"后续 Anki 制卡"。

## 当前状态（2026-05-19 第二轮）

- **正式专题**：21 篇（A 级 9 / A- 级 2 / B+ 级 10）
- **覆盖看板**：`index/topic_coverage_dashboard.md`
- **下一轮优先**：人力资源管理、质量七工具、招投标与政府采购
- **详细总结**：`reports/final_summary.md`

## 目录结构

```
topic_learning_packages/
├── README.md                          ← 你正在看的文件
├── _standards/                        ← 建设标准与样例
│   ├── T007 样例（PERT 与进度压缩）
│   ├── 建设说明 v2（全项目规范）
│   └── Skill v1 生成规范
├── topics/                            ← 正式专题正文（主交付）
│   ├── 01_信息化与信息系统/
│   ├── 02_项目管理基础/
│   ├── 03_立项管理/
│   ├── 04_整体管理/
│   ├── 05_范围管理/
│   ├── 06_进度管理/
│   ├── 07_成本管理/
│   ├── 08_质量管理/
│   ├── 09_人力资源与沟通管理/
│   ├── 10_干系人与风险管理/
│   ├── 11_采购与合同管理/
│   ├── 12_配置变更知识产权与法律法规/
│   ├── 14_案例分析专题/
│   └── 99_综合专题与跨域辨析/
├── index/                             ← 索引与覆盖矩阵
│   ├── topic_manifest.json           ← 专题元数据（机器可读）
│   ├── topic_manifest.md             ← 专题总览（人可读）
│   ├── source_coverage_matrix.md     ← 素材覆盖矩阵
│   ├── question_coverage_matrix.md   ← 题型覆盖矩阵
│   ├── topic_dependency_map.md       ← 专题依赖与学习路径
│   └── topic_coverage_dashboard.md   ← 覆盖程度看板（新增）
├── reports/                           ← 建设报告
│   ├── topic_build_plan.md           ← 建设计划与仓库盘点
│   ├── topic_build_log.md            ← 专题结构调整记录
│   ├── topic_quality_report.md       ← 质量评分报告
│   ├── unfinished_or_low_confidence_topics.md ← 待建/低置信度
│   └── final_summary.md              ← 最终总结
└── archive/                           ← 历史归档
```

## 重要说明

- **`_standards/` 中的 T007 样例是正式专题正文标准。** 所有专题应模仿它的深度、结构（连续讲义、主线图、典型题详解、Anki 制卡建议、最小掌握标准）和文风。
- **`outputs/00-05` 和 `samples/00-05` 是索引层和规划层材料，不是正式专题正文。**
- **`topic_build_full/topics/` 中包含 95 个骨架文件（C/D 级）**，可作为导航但不可直接用于学习。

## 推荐学习路径

1. T-PM-002（过程组与知识域）→ 建立全局框架
2. T-INT-004（变更控制）→ T-SCOPE-002（WBS）→ T-SCH-003（关键路径）
3. T-COST-001（估算预算）→ T-COST-002（挣值管理）
4. T-QUAL-001（QA/QC）→ T-RISK-001（风险应对）→ T-RISK-002（EMV）
5. T-PROC-001（合同类型）→ T-COM-001（沟通渠道）
6. T-CASE-001（案例通用方法）→ T-CASE-002/003（案例模板）
7. T-CROSS-001（跨域辨析）→ 查漏补缺
