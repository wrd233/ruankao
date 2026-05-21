# 12_配置变更知识产权与法律法规 章节概念卡

## Card 001｜概念卡｜keep｜A

Front：配置项是什么？

Back：配置项是受配置管理控制的产品、文档或组件。

Extra：<div>理解：代码、需求文档、设计文档、测试用例都可能是配置项。</div><div>题干信号：受控对象、文档/组件</div><div>来源：tutorial 15.2.1。</div>

Source：SRC-CH-12-001

Manual review：概念定义清楚，Back 一句话定边界。

## Card 002｜概念卡｜keep｜A

Front：配置基线是什么？

Back：配置基线是经过正式评审和批准的一组配置项，作为后续变更的依据。

Extra：<div>理解：基线一旦建立，变更必须走控制流程。</div><div>易错点：基线不是单个配置项，而是一组配置项的逻辑集合。</div><div>题干信号：批准、变更依据</div><div>来源：tutorial 15.2.1。</div>

Source：SRC-CH-12-002

Manual review：概念定义清楚，Extra 补充基线与配置项的集合关系。

## Card 003｜概念卡｜keep｜A

Front：配置库是什么？

Back：配置库用于保存和管理配置项及其版本。

Extra：<div>理解：不同库权限不同，不能随意把受控库当个人目录。</div><div>题干信号：版本保存、权限</div><div>来源：tutorial 15.2.1。</div>

Source：SRC-CH-12-003

Manual review：概念定义清楚，Extra 提示权限差异。

## Card 004｜概念卡｜keep｜B

Front：开发库是什么？

Back：开发库用于开发人员日常修改和自测，控制相对宽松。

Extra：<div>理解：它不是正式发布库，开发人员可自行控制。</div><div>题干信号：个人/开发、较宽松</div><div>来源：tutorial 15.2.1。</div>

Source：SRC-CH-12-004

Manual review：概念定义清楚，Back 一句话定边界。

## Card 005｜概念卡｜keep｜A

Front：受控库是什么？

Back：受控库保存经过评审或基线化的配置项，变更受控制。

Extra：<div>理解：题干出现审批后入库，常指受控库。</div><div>题干信号：评审、受控变更</div><div>来源：tutorial 15.2.1。</div>

Source：SRC-CH-12-005

Manual review：概念定义清楚，Extra 给出题干信号。

## Card 006｜概念卡｜keep｜A

Front：产品库是什么？

Back：产品库保存可交付或已发布的软件产品版本。

Extra：<div>理解：它面向发布和交付，不是开发人员随意改动的地方。</div><div>题干信号：发布、交付版本</div><div>来源：tutorial 15.2.1。</div>

Source：SRC-CH-12-006

Manual review：概念定义清楚，Extra 说明用途边界。

## Card 007｜概念卡｜keep｜B

Front：配置审计是什么？

Back：配置审计检查配置项是否完整、一致并符合配置管理要求。

Extra：<div>理解：它不同于质量审计，关注配置项和版本状态而非过程。</div><div>题干信号：完整性、一致性</div><div>来源：tutorial 15.2.6。</div>

Source：SRC-CH-12-007

Manual review：概念定义清楚，Extra 与质量审计划清边界。

## Card 008｜概念卡｜keep｜B

Front：著作权是什么？

Back：著作权保护作品表达，如软件源代码、文档等表达成果。

Extra：<div>理解：著作权保护的是"表达"而非"思想"本身。</div><div>题干信号：表达成果、软件作品</div><div>来源：tutorial 20.2.1。</div>

Source：SRC-CH-12-008

Manual review：概念定义清楚，Extra 强调思想与表达二分法。

## Card 009｜概念卡｜keep｜B

Front：专利权是什么？

Back：专利权保护具有新颖性、创造性和实用性的技术方案。

Extra：<div>理解：不要把"代码表达"直接说成专利。</div><div>题干信号：技术方案</div><div>来源：tutorial 20.2.2。</div>

Source：SRC-CH-12-009

Manual review：概念定义清楚，Extra 与著作权划清边界。

## Card 010｜概念卡｜keep｜B

Front：要约是什么？

Back：要约是希望和他人订立合同的意思表示，内容应具体确定。

Extra：<div>理解：招投标场景中，招标公告通常被视为要约邀请，投标文件是要约。</div><div>题干信号：订立合同、具体确定</div><div>来源：tutorial 13.1 / 合同法原理。</div>

Source：SRC-CH-12-010

Manual review：概念定义清楚，Extra 给出招投标场景应用。

## Card 011｜概念卡｜new｜A

Front：承诺在法律上的定义是什么？

Back：承诺是受要约人同意要约的意思表示，承诺生效时合同成立。

Extra：<div>理解：中标通知书通常被视为承诺，一旦发出合同即告成立。</div><div>易错点：承诺的内容应当与要约一致，实质性变更构成反要约而非承诺。</div><div>题干信号：同意、合同成立、中标</div><div>来源：tutorial 13.1 / 合同法原理。</div>

Source：SRC-CH-12-011

Manual review：与010 要约卡成对出现，Extra 说明与要约的衔接关系。

## Card 012｜概念卡｜new｜B

Front：配置库三种类型的核心区别是什么？

Back：开发库控制宽松供个人开发，受控库保存基线受严格变更控制，产品库保存正式发布版本。

Extra：<div>记忆线索：开发→个人工作，受控→基线管理，产品→发布交付。</div><div>题干信号：三类库区别、权限判断</div><div>关联：分别对应 Card 004/005/006。</div><div>来源：tutorial 15.2.1。</div>

Source：SRC-CH-12-012

Manual review：与004/005/006 互补，提供横向比较。

## Card 013｜概念卡｜new｜A

Front：配置项版本号有哪些规则？

Back：草稿版 0.YZ，正式版 X.Y，修改版 X.YZ。第一次正式发布版本号为 1.0。

Extra：<div>理解：草稿→正式→修改→正式的状态转换驱动版本号变化。</div><div>记忆线索：草稿从 0 开始，正式从 1 开始，修改增加 Z。</div><div>题干信号：版本号规则、配置项状态</div><div>来源：tutorial 15.2.1。</div>

Source：SRC-CH-12-013

Manual review：规则性概念卡，Extra 给出状态与版本号的对应链条。

## Card 014｜概念卡｜new｜B

Front：软件著作权保护的客体和内容是什么？

Back：客体是计算机程序及其有关文档；内容包括发表权、署名权、修改权等著作人身权和复制权、发行权等著作财产权。

Extra：<div>理解：程序包括源程序与目标程序，同一程序的两者为同一作品。</div><div>易错点：软件著作权自动取得，无需登记；但登记有助于维权举证。</div><div>题干信号：软件作品、开发者权利</div><div>来源：tutorial 20.2.1。</div>

Source：SRC-CH-12-014

Manual review：与008 著作权卡互补，008 更概念化，本卡深入软件著作权细节。

## Card 015｜概念卡｜new｜C

Front：知识产权的特性有哪些？

Back：知识产权具有无体性、专有性、地域性和时间性四大特性。

Extra：<div>理解：无体性是与有形财产权的核心区别；地域性意味着专利权只在授予国受保护。</div><div>记忆线索：无体、专有、地域、时间。</div><div>题干信号：知识产权特点、权利限制</div><div>来源：tutorial 20.1.2。</div>

Source：SRC-CH-12-015

Manual review：概念标准简明，Extra 给出易错点。

## Card 016｜概念卡｜new｜B

Front：违约责任的承担方式有哪些？

Back：违约责任的承担方式包括继续履行、采取补救措施、赔偿损失、支付违约金或定金。

Extra：<div>理解：继续履行是最基本方式；补救措施包括修理、更换、重作、减少价款等。</div><div>记忆线索：继续、补救、赔偿、违约金/定金。</div><div>题干信号：违约处理、法律后果</div><div>来源：tutorial 13.3.1。</div>

Source：SRC-CH-12-016

Manual review：规则性概念卡，列出四种方式，Extra 说明适用场景。

## Card 017｜概念卡｜new｜B

Front：配置管理包括哪六大活动？

Back：配置管理六大活动为：制定配置管理计划、配置标识、配置控制、配置状态报告、配置审计、发布管理和交付。

Extra：<div>记忆线索：计划→标识→控制→状态报告→审计→发布交付。</div><div>题干信号：配置管理过程、主要活动</div><div>来源：tutorial 15.2。</div>

Source：SRC-CH-12-017

Manual review：过程性概念卡，列出完整活动链条。
