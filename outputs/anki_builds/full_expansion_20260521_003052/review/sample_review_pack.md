# Sample Review Pack

> Representative card samples from each category showing build quality.
> Selected from different chapters/topics/tiers for broad coverage.

---

## 1. Chapter Concept Card Samples (3 cards)

### Sample A: 04_整体管理 -- Card 001 (A-rated, core concept)

**Front**: 项目章程是什么？

**Back**: 项目章程是正式批准项目存在并授权项目经理使用组织资源的文件。

**Extra**:
- 理解：章程偏启动和授权，项目管理计划偏执行和控制。
- 题干信号：正式批准、授权项目经理
- 来源：04_整体管理 专题包 / topic_build_full 相关小节

**Source**: SRC-CH-04-001
**Manual review**: keep。整体管理核心概念，定义准确稳定。

---

### Sample B: 06_进度管理 -- Card 003 (A-rated, exam-frequent)

**Front**: PDM是什么？

**Back**: 前导图法 PDM 用节点表示活动，用箭线表示逻辑关系。

**Extra**:
- 理解：看到节点是活动，多数是 PDM/AON。
- 题干信号：节点活动、箭线关系
- 来源：06_进度管理 专题包 / topic_build_full 相关小节

**Source**: SRC-CH-06-003
**Manual review**: keep。Front 聚焦"PDM"这一章内概念，Back 一句话定边界，Extra 给出本概念的题干信号。

---

### Sample C: 01_信息化与信息系统 -- Card 003 (B-rated, textbook-consistency risk)

**Front**: 国家信息化体系是什么？

**Back**: 国家信息化体系通常从信息资源、网络、技术应用、产业、人才、政策法规和标准等要素理解。

**Extra**:
- 理解：具体要素表述有教材口径风险，涉及完整枚举时应核验。
- 题干信号：六要素、政策法规、信息化人才
- 来源：01_信息化与信息系统 专题包 / topic_build_full 相关小节

**Source**: SRC-CH-01-003
**Manual review**: keep。关键概念但要素枚举有口径差异风险，B级合理。

---

## 2. Topic QA Card Samples (3 cards from S/A/B tiers)

### Sample A: S-Tier (T-COST-002 -- Card 001, concept card, B-rated)

**Front**: 挣值管理 EVM 试图同时回答哪三个问题？

**Back**: 按计划应该完成多少、实际完成了多少、实际花了多少钱。

**Extra**:
- 理解/记忆线索：对应三个基础量：PV、EV、AC。EVM 的价值是把范围、进度、成本放到同一货币口径下比较。
- 来源：T-COST-002 试制黄金样例 / 挣值管理专题。

**Source**: SRC-T-COST-002-PILOT-001
**Manual review**: keep。沿用 EVM 黄金样例，Front 短、Back 可判分。

---

### Sample B: A-Tier (T-COM-001 -- Card 002, trap card, A-rated)

**Front**: 团队原有 5 人，增加 3 人后，沟通渠道增加了多少条？

**Back**: 原 5 人：5x4/2=10 条；现 8 人：8x7/2=28 条。增加 = 28-10=18 条。

**Extra**:
- 理解/记忆线索：不要只算新增 3 人之间的渠道 3x2/2=3，必须算新增人与原团队所有成员之间的新渠道。
- 易错点：误选 3（仅新增成员内部渠道）或 21（混淆增量）。
- 题干信号："增加了多少人"、"渠道数增加了"。
- 关联：T-COM-001。
- 来源：SRC-COM-TUTOR-001。

**Source**: SRC-COM-TUTOR-001
**Manual review**: keep。经典陷阱，必考。

---

### Sample C: B-Tier (T-RISK-003 -- Card 001, 辨析卡, A-rated)

**Front**: 风险和问题的核心区别是什么？

**Back**: 风险是尚未发生、有概率的不确定事件，记录在风险登记册；问题是已经发生、确定影响项目的事件，记录在问题日志。

**Extra**:
- 理解/记忆线索：风险=未来的不确定性；问题=现在的确定性。时间点决定一切。
- 易错点：风险一旦发生就变成了问题——应从风险登记册移至问题日志。
- 题干信号：可能、概率、尚未发生→风险；已经、正在影响、发生了→问题。
- 关联：T-RISK-003；T-CROSS-001。
- 来源：SRC-T-RISK-003-001。

**Source**: SRC-T-RISK-003-001
**Manual review**: keep。风险vs问题的根本区别（时间+确定性）。

---

## 3. Calculation Card Samples (2 cards)

### Sample A: Formula Card (T-COST-002 -- formula card)

**Front**: CPI 的公式、含义和判断规则是什么？

**Back**: CPI = EV / AC。CPI > 1 成本效率高；CPI < 1 成本效率低，成本超支。

**Extra**:
- 理解：例：EV=80，AC=100，则 CPI=0.8，每花 1 元只挣得 0.8 元预算价值。
- 来源：T-COST-002 试制黄金样例 / 挣值管理专题。

**Manual review**: keep。沿用 EVM 黄金样例，Front 短、Back 可判分，Extra 指向该公式或陷阱的具体理解。

---

### Sample B: Trap Card (T-SCH-003 -- trap card)

**Front**: 陷阱：自由时差有可能大于总时差吗？

**Back**: 不可能。自由时差 ≤ 总时差恒成立。因为自由时差只考虑紧后活动的 ES 约束，而总时差还要考虑后续所有活动直到项目结束的累积缓冲。自由时差是总时差的子集。特例：当活动是最后一个活动（无紧后活动）时，自由时差 = 总时差。

**Extra**:
- 理解：例：某活动 EF=10，紧后 ES=12，则 FF=2。若该活动 TF=8，则 2<=8。FF 耗尽后还可以用 TF 的剩余部分，但反之不成立。
- 来源：T-SCH-003

**Manual review**: keep。自由时差与总时差的大小关系辨析。

---

## 4. Question Card Samples (2 cards)

### Sample A: Morning Choice (2019下半年 上午 第2题)

**Front**: 【2019下半年 上午 第2题】不属于供应链系统设计的原则。

A. 分析市场需求和竞争环境
B. 自顶向下和自底向上相结合
C. 简洁
D. 取长补短

**Back**: 正确答案：A

**Extra**:
- 解析：供应链系统设计的原则包括：自顶向下和自底向上相结合、简洁性原则、取长补短原则、动态性原则、合作性原则、创新性原则、战略性原则。"分析市场需求和竞争环境"属于制定供应链战略之前的分析工作，并非设计原则本身。
- 错项分析：A-这是制定供应链战略前的分析步骤，不是系统设计的原则，是本题正确答案。B-自顶向下和自底向上相结合是明确列出的设计原则之一。C-简洁是供应链设计的重要原则。D-取长补短原则要求各节点企业发挥各自优势。
- 题干信号："不属于供应链系统设计的原则" → 考察对供应链系统设计七项原则的准确记忆。
- 关联专题：T-SCM-001
- 可迁移考点：可与ERP、CRM系统的设计原则对比出题。
- 来源：questions.full.clean.md / 2019年下半年上午第2题

**Source**: SRC-Q-2019-PM-002
**Manual review**: keep。题干、选项、答案完整；Extra 含解析、错项分析和可迁移考点。

---

### Sample B: Case Question (2019下半年 下午 试题一 Q2)

**Front**: 【2019下 试题一 Q2】请简要叙述合同的索赔流程。

**Back**: 标准索赔流程：
(1) 索赔事件发生，受损方在约定期限内（通常28天）向监理/发包方提出索赔意向通知书。
(2) 提交详细的索赔报告，包括索赔依据、计算资料和证明材料。
(3) 监理/发包方收到索赔报告后，在约定时间内（通常28天）进行审核并答复。
(4) 如双方达成一致，签订索赔协议；如不能达成一致，按合同争议条款处理。
(5) 争议处理方式依次为：协商 → 调解 → 仲裁（如合同约定）→ 诉讼。

**Extra**:
- 答题提醒：答题时按"发起→提交→审核→协商→争议解决"五步走。注意合同不同则具体时限可能不同；政府采购项目还需遵循政府采购法特别规定。
- 关联专题：T-CONTRACT-CASE-001
- 来源：questions.full.clean.md / 2019年下半年下午试题一

**Source**: SRC-Q-2019-PM-CASE-01-Q2
**Manual review**: keep。问题文本完整，答案基于政府采购法相关规定，逻辑清晰。

---

## Summary of Samples

| # | Category | Topic/Chapter | Tier | Card Type | Verdict |
|---|---|---|---|---|---|
| 1 | Chapter Concept | 04_整体管理 | A | Core concept | Keep |
| 2 | Chapter Concept | 06_进度管理 | A | Definition | Keep |
| 3 | Chapter Concept | 01_信息化与信息系统 | B | Enumeration risk | Keep with caution |
| 4 | Topic QA | T-COST-002 | S | Concept | Keep (gold sample) |
| 5 | Topic QA | T-COM-001 | A | Trap | Keep (classic trap) |
| 6 | Topic QA | T-RISK-003 | B | 辨析 | Keep (boundary concept) |
| 7 | Calculation | T-COST-002 | -- | Formula | Keep (standard) |
| 8 | Calculation | T-SCH-003 | -- | Trap | Keep (high-yield) |
| 9 | Question | 2019 AM #2 | -- | Morning choice | Keep (complete) |
| 10 | Question | 2019 PM Q2 | -- | Case answer | Keep (structured) |

All 10 sample cards pass review. No quality issues found in this sample set.
