# 软考专题学习包目录

本目录存放"系统集成项目管理工程师"正式专题学习包。每个专题学习包都是一篇可独立阅读的 Markdown 讲义，用于连接"全量 OCR/索引材料"和"后续 Anki 制卡"。

## 目录结构

```
topic_learning_packages/
├── README.md                          ← 你正在看的文件
├── _standards/                        ← 建设标准与样例
│   ├── T007 样例（PERT 与进度压缩）
│   └── 建设说明 v2（全项目规范）
├── topics/                            ← 正式专题正文（主交付）
│   ├── 00_导学与考试结构/
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
│   ├── 13_信息系统技术基础/
│   ├── 14_案例分析专题/
│   └── 99_综合专题与跨域辨析/
├── index/                             ← 索引与覆盖矩阵
│   ├── topic_manifest.json           ← 专题元数据（机器可读）
│   ├── topic_manifest.md             ← 专题总览（人可读）
│   ├── source_coverage_matrix.md     ← 素材覆盖矩阵
│   ├── question_coverage_matrix.md   ← 题型覆盖矩阵
│   └── topic_dependency_map.md       ← 专题依赖与学习路径
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
- **`outputs/00-05` 和 `samples/00-05` 是索引层和规划层材料，不是正式专题正文。** 它们定义了专题边界和材料来源，但不要把它们误认为最终交付物。
- **`topic_build_full/topics/` 中包含 95 个骨架文件（C/D 级）**，它们是结构化大纲，可用来导航专题范围，但不能直接用于学习。本目录 `topics/` 中的文件是已升级的正式专题学习包。

## 当前建设状态

- **已建成 A 级专题**：11 篇
- **覆盖的核心知识域**：成本管理、进度管理、范围管理、整体管理、采购管理、质量管理、风险管理、沟通管理、案例分析、项目管理基础、综合辨析
- **总计字数**：~95,500 字
- **详见**：`reports/final_summary.md`

## 后续工作

1. 将 topic_build_full 中的高优先级骨架升级为 B 级以上专题
2. 建设案例专项模板
3. 补齐信息化基础、资质法规专题
4. 完成 [待核验] 标签的人工校对
5. 基于正式专题生成 Anki 卡片

## 使用方式

- **学习者**：按 `index/topic_dependency_map.md` 中的推荐学习路径阅读专题。
- **后续 Agent**：读取 `index/topic_manifest.json` 获取专题清单和状态，读取 `_standards/` 获取质量标准，读取 `reports/unfinished_or_low_confidence_topics.md` 获取待办清单。
- **Anki 制卡 Skill**：读取专题正文末尾的"后续制卡建议"部分，据此生成 Anki 卡片。
