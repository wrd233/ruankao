# T-COST-002 Anki 试制卡片

## 1. 概念｜难度 2

**Front：** 挣值管理 EVM 试图同时回答哪三个问题？

**Back：** 按计划应该完成多少、实际完成了多少、实际花了多少钱。

**Extra：** 对应三个基础量：PV、EV、AC。EVM 的价值是把范围、进度、成本放到同一货币口径下比较。

**Tags：** `ruankao cost evm T-COST-002 concept`

## 2. 概念｜难度 2

**Front：** PV（Planned Value）是什么？

**Back：** 计划价值：到某一时点，按计划应该完成工作的预算价值。

**Extra：** 关键词是“计划应该”。PV 不看实际完成情况。项目完工时 PV 总额等于 BAC。

**Tags：** `ruankao cost evm T-COST-002 concept pv`

## 3. 概念｜难度 2

**Front：** EV（Earned Value）是什么？

**Back：** 挣值：实际完成工作的预算价值。

**Extra：** EV 不是实际花费，而是“已完成产出按预算值多少钱”。它是 EVM 中最关键也最容易混的量。

**Tags：** `ruankao cost evm T-COST-002 concept ev`

## 4. 概念｜难度 2

**Front：** AC（Actual Cost）是什么？

**Back：** 实际成本：完成与 EV 对应工作实际发生的成本。

**Extra：** AC 来自实际花费，但口径要和 PV/EV 保持一致，比如是否包含间接成本。

**Tags：** `ruankao cost evm T-COST-002 concept ac`

## 5. 概念｜难度 2

**Front：** BAC 在挣值管理中表示什么？

**Back：** 完工预算，即项目全部计划工作的总预算。

**Extra：** BAC 是预测 EAC、VAC、TCPI 的基准。

**Tags：** `ruankao cost evm T-COST-002 concept bac`

## 6. 概念｜难度 3

**Front：** 为什么说 EV 是 EVM 的核心？

**Back：** 因为 EV 把实际完成量转换成预算价值，使进度和成本都能用同一口径比较。

**Extra：** 进度比较 EV 与 PV；成本比较 EV 与 AC。没有 EV，很多绩效判断不能成立。

**Tags：** `ruankao cost evm T-COST-002 concept ev`

## 7. 概念｜难度 2

**Front：** SV 和 CV 的单位是什么？

**Back：** 货币单位，如元、万元。

**Extra：** SV/CV 是差值，不是天数或百分比。SPI/CPI 才是无量纲指数。

**Tags：** `ruankao cost evm T-COST-002 concept variance`

## 8. 概念｜难度 2

**Front：** SPI 和 CPI 的判断阈值是什么？

**Back：** 大于 1 通常表示好，等于 1 符合计划，小于 1 表示差。

**Extra：** SPI < 1 是进度效率低于计划；CPI < 1 是成本效率低于计划。

**Tags：** `ruankao cost evm T-COST-002 concept index`

## 9. 概念｜难度 3

**Front：** EAC 表示什么？

**Back：** 完工估算：根据当前绩效和假设预测项目完工总成本。

**Extra：** EAC 不是固定公式，公式取决于题干对未来绩效的假设。

**Tags：** `ruankao cost evm T-COST-002 concept forecast`

## 10. 概念｜难度 2

**Front：** ETC 表示什么？

**Back：** 完工尚需估算：从当前到完工还需要的成本。

**Extra：** 常用关系：ETC = EAC - AC。

**Tags：** `ruankao cost evm T-COST-002 concept forecast`

## 11. 概念｜难度 2

**Front：** VAC 表示什么？

**Back：** 完工偏差：预算 BAC 与完工估算 EAC 的差异。

**Extra：** VAC = BAC - EAC。VAC < 0 表示预计超预算。

**Tags：** `ruankao cost evm T-COST-002 concept forecast`

## 12. 概念｜难度 3

**Front：** TCPI 是回顾性指标还是前瞻性指标？

**Back：** 前瞻性指标。

**Extra：** TCPI 表示为了实现 BAC 或 EAC，剩余工作必须达到的成本绩效水平。

**Tags：** `ruankao cost evm T-COST-002 concept tcpi`

## 13. 公式｜难度 2

**Front：** SV 的公式、含义和判断规则是什么？

**Back：** SV = EV - PV。SV > 0 进度提前；SV = 0 符合计划；SV < 0 进度滞后。

**Extra：** 例：EV=90，PV=100，则 SV=-10，进度滞后。

**Tags：** `ruankao cost evm T-COST-002 formula sv`

## 14. 公式｜难度 2

**Front：** CV 的公式、含义和判断规则是什么？

**Back：** CV = EV - AC。CV > 0 成本节约；CV = 0 符合预算；CV < 0 成本超支。

**Extra：** 例：EV=90，AC=110，则 CV=-20，成本超支。

**Tags：** `ruankao cost evm T-COST-002 formula cv`

## 15. 公式｜难度 2

**Front：** SPI 的公式、含义和判断规则是什么？

**Back：** SPI = EV / PV。SPI > 1 进度效率高于计划；SPI < 1 进度效率低于计划。

**Extra：** 例：EV=80，PV=100，则 SPI=0.8，进度滞后。

**Tags：** `ruankao cost evm T-COST-002 formula spi`

## 16. 公式｜难度 2

**Front：** CPI 的公式、含义和判断规则是什么？

**Back：** CPI = EV / AC。CPI > 1 成本效率高；CPI < 1 成本效率低，成本超支。

**Extra：** 例：EV=80，AC=100，则 CPI=0.8，每花 1 元只挣得 0.8 元预算价值。

**Tags：** `ruankao cost evm T-COST-002 formula cpi`

## 17. 公式｜难度 3

**Front：** 非典型偏差下 EAC 怎么算？

**Back：** EAC = AC + (BAC - EV)。

**Extra：** 题干信号：一次性、偶然、不会再出现、已纠正。例：AC=200，BAC=500，EV=180，则 EAC=520。

**Tags：** `ruankao cost evm T-COST-002 formula eac`

## 18. 公式｜难度 3

**Front：** 典型偏差会延续时 EAC 怎么算？

**Back：** EAC = BAC / CPI。

**Extra：** 题干信号：当前绩效将持续、按目前趋势、没有改善迹象。例：BAC=1000，CPI=0.8，则 EAC=1250。

**Tags：** `ruankao cost evm T-COST-002 formula eac`

## 19. 公式｜难度 3

**Front：** 重新估算剩余工作时 EAC 怎么算？

**Back：** EAC = AC + 自下而上重新估算的 ETC。

**Extra：** 适用：原估算假设严重失效，需要重新估算剩余工作。

**Tags：** `ruankao cost evm T-COST-002 formula eac`

## 20. 公式｜难度 4

**Front：** 同时考虑 CPI 和 SPI 的 EAC 扩展公式是什么？

**Back：** EAC = AC + (BAC - EV) / (CPI × SPI)。

**Extra：** 用于题干明确要求同时考虑成本和进度影响。本专题将该口径列为需回查教材的待核验项，制卡时应保留提醒。

**Tags：** `ruankao cost evm T-COST-002 formula eac pending`

## 21. 公式｜难度 2

**Front：** ETC 的常用公式是什么？

**Back：** ETC = EAC - AC。

**Extra：** 例：EAC=950，AC=380，则 ETC=570。

**Tags：** `ruankao cost evm T-COST-002 formula etc`

## 22. 公式｜难度 2

**Front：** VAC 的公式和判断规则是什么？

**Back：** VAC = BAC - EAC。VAC > 0 预计结余；VAC < 0 预计超预算。

**Extra：** 例：BAC=800，EAC=950，则 VAC=-150，预计超预算 150。

**Tags：** `ruankao cost evm T-COST-002 formula vac`

## 23. 公式｜难度 4

**Front：** 以 BAC 为目标的 TCPI 怎么算？

**Back：** TCPI = (BAC - EV) / (BAC - AC)。

**Extra：** 例：BAC=800，EV=300，AC=360，则 TCPI=500/440≈1.14。

**Tags：** `ruankao cost evm T-COST-002 formula tcpi`

## 24. 计算｜难度 2

**Front：** PV=100，EV=90，AC=110。计算 SV 和 CV，并判断状态。

**Back：** SV=90-100=-10；CV=90-110=-20。进度滞后，成本超支。

**Extra：** 常见错法：把 PV 或 AC 当被减数。记住 EV 永远在前：SV=EV-PV，CV=EV-AC。

**Tags：** `ruankao cost evm T-COST-002 calculation sv cv`

## 25. 计算｜难度 2

**Front：** PV=200，EV=240，AC=220。计算 SPI、CPI，并判断状态。

**Back：** SPI=240/200=1.2，进度提前；CPI=240/220≈1.09，成本节约。

**Extra：** 指数大于 1 通常是好。

**Tags：** `ruankao cost evm T-COST-002 calculation spi cpi`

## 26. 计算｜难度 2

**Front：** SPI=0.8，CPI=1.2。如何判断项目状态？

**Back：** 进度滞后，成本节约。

**Extra：** SPI 管进度，CPI 管成本。两者可以一好一坏。

**Tags：** `ruankao cost evm T-COST-002 calculation judgment`

## 27. 计算｜难度 3

**Front：** BAC=500，AC=200，EV=180，偏差为一次性且不会再出现。EAC 是多少？

**Back：** EAC=AC+(BAC-EV)=200+(500-180)=520。

**Extra：** 题干“不会再出现”触发非典型偏差公式。

**Tags：** `ruankao cost evm T-COST-002 calculation eac`

## 28. 计算｜难度 3

**Front：** BAC=1000，EV=400，AC=500，当前成本绩效将持续。EAC 是多少？

**Back：** CPI=400/500=0.8；EAC=BAC/CPI=1000/0.8=1250。

**Extra：** 题干“将持续”触发典型偏差公式。

**Tags：** `ruankao cost evm T-COST-002 calculation eac`

## 29. 计算｜难度 4

**Front：** BAC=800，EV=300，AC=360。若仍要按 BAC 完工，TCPI 是多少？

**Back：** TCPI=(800-300)/(800-360)=500/440≈1.14。

**Extra：** TCPI > 1 表示剩余工作必须比预算效率更高。

**Tags：** `ruankao cost evm T-COST-002 calculation tcpi`

## 30. 计算｜难度 4

**Front：** PV=600，EV=540，AC=630，BAC=1200。计算 SPI/CPI 并判断状态。

**Back：** SPI=540/600=0.9，进度滞后；CPI=540/630≈0.857，成本超支。

**Extra：** 如果按当前 CPI 持续，EAC≈1200/0.857≈1400，预计超预算。

**Tags：** `ruankao cost evm T-COST-002 calculation comprehensive`

## 31. 计算｜难度 3

**Front：** PV=400，EV=320，AC=380。计算 SV、CV、SPI、CPI。

**Back：** SV=-80；CV=-60；SPI=0.8；CPI≈0.842。

**Extra：** 下午案例中还要写文字结论：进度滞后且成本超支。

**Tags：** `ruankao cost evm T-COST-002 calculation case`

## 32. 计算｜难度 3

**Front：** 只给 PV=25 万、AC=28 万，没有 EV。能否判断成本超支？

**Back：** 不能。信息不足。

**Extra：** 成本偏差 CV=EV-AC，缺 EV 就不知道完成工作的预算价值。

**Tags：** `ruankao cost evm T-COST-002 calculation insufficient`

## 33. 计算｜难度 2

**Front：** BAC=800，EAC=950。VAC 是多少？含义是什么？

**Back：** VAC=800-950=-150，表示预计超预算 150。

**Extra：** VAC 是预测偏差，不是当前偏差。

**Tags：** `ruankao cost evm T-COST-002 calculation vac`

## 34. 辨析｜难度 2

**Front：** CV 和 SV 的核心区别是什么？

**Back：** CV 比较 EV 与 AC，判断成本；SV 比较 EV 与 PV，判断进度。

**Extra：** 两者都是 EV 在前。CV 的对手是实际花费，SV 的对手是计划价值。

**Tags：** `ruankao cost evm T-COST-002 contrast cv sv`

## 35. 辨析｜难度 2

**Front：** CPI 和 SPI 的核心区别是什么？

**Back：** CPI=EV/AC 判断成本效率；SPI=EV/PV 判断进度效率。

**Extra：** CPI 看花钱效率，SPI 看完成计划效率。

**Tags：** `ruankao cost evm T-COST-002 contrast cpi spi`

## 36. 辨析｜难度 2

**Front：** PV、EV、AC 三者分别回答什么问题？

**Back：** PV：按计划应完成值多少；EV：实际完成值多少；AC：实际花了多少。

**Extra：** 不要把 EV 当 AC。EV 是产出价值，AC 是投入成本。

**Tags：** `ruankao cost evm T-COST-002 contrast pv ev ac`

## 37. 辨析｜难度 2

**Front：** 成本超支和进度落后一定同时出现吗？

**Back：** 不一定。

**Extra：** 可能进度落后但成本节约，也可能进度超前但成本超支。要分别看 CPI/CV 和 SPI/SV。

**Tags：** `ruankao cost evm T-COST-002 contrast status`

## 38. 辨析｜难度 3

**Front：** SV < 0 是否表示项目延误了具体多少天？

**Back：** 不是。SV 的单位是货币，表示完成的预算价值低于计划值。

**Extra：** 要判断关键路径和具体工期，还需结合进度网络。

**Tags：** `ruankao cost evm T-COST-002 contrast sv`

## 39. 辨析｜难度 4

**Front：** SPI > 1 是否保证项目一定按期或提前完工？

**Back：** 不保证。

**Extra：** SPI 是总体工作量效率，不专门测关键路径。关键路径活动仍可能延误。

**Tags：** `ruankao cost evm T-COST-002 contrast spi critical_path`

## 40. 辨析｜难度 3

**Front：** 典型偏差和非典型偏差如何区分？

**Back：** 典型偏差会持续影响后续；非典型偏差是一次性、偶然、已解决。

**Extra：** 典型常用 EAC=BAC/CPI；非典型常用 EAC=AC+(BAC-EV)。

**Tags：** `ruankao cost evm T-COST-002 contrast eac`

## 41. 辨析｜难度 2

**Front：** EAC 和 ETC 的区别是什么？

**Back：** EAC 是预计完工总成本；ETC 是从现在到完工还需要的成本。

**Extra：** ETC=EAC-AC。

**Tags：** `ruankao cost evm T-COST-002 contrast forecast`

## 42. 辨析｜难度 3

**Front：** VAC 和 CV 的区别是什么？

**Back：** CV 是当前成本偏差；VAC 是完工时预计偏差。

**Extra：** CV=EV-AC，VAC=BAC-EAC。一个看当前，一个看预测。

**Tags：** `ruankao cost evm T-COST-002 contrast variance`

## 43. 辨析｜难度 3

**Front：** 为什么只有 PV 和 AC 不能判断绩效？

**Back：** 因为缺少 EV，不知道实际完成工作的预算价值。

**Extra：** 没有 EV，就无法计算 SV、CV、SPI、CPI。

**Tags：** `ruankao cost evm T-COST-002 contrast insufficient`

## 44. 案例｜难度 3

**Front：** 下午案例中给出 PV、EV、AC，答题第一步写什么？

**Back：** 先列公式并计算 SV、CV、SPI、CPI。

**Extra：** 然后用文字判断：进度提前/滞后、成本节约/超支。不要只写数字。

**Tags：** `ruankao cost evm T-COST-002 case template`

## 45. 案例｜难度 3

**Front：** 案例题中如何判断“成本超支”？

**Back：** 优先看 CV<0 或 CPI<1。

**Extra：** 表达模板：CV 为负、CPI 小于 1，说明实际花费超过已完成工作的预算价值，项目成本超支。

**Tags：** `ruankao cost evm T-COST-002 case cost`

## 46. 案例｜难度 3

**Front：** 案例题中如何判断“进度落后”？

**Back：** 优先看 SV<0 或 SPI<1。

**Extra：** 表达模板：SV 为负、SPI 小于 1，说明实际完成工作的预算价值低于计划值，项目进度落后。

**Tags：** `ruankao cost evm T-COST-002 case schedule`

## 47. 案例｜难度 4

**Front：** 挣值案例题的完整答题链是什么？

**Back：** 计算指标 → 判断状态 → 预测 EAC/ETC/VAC → 分析原因 → 提出措施。

**Extra：** 措施要对应原因，例如范围蔓延走变更控制，效率低做资源优化，关键路径延误考虑赶工/快速跟进。

**Tags：** `ruankao cost evm T-COST-002 case flow`

## 48. 案例｜难度 4

**Front：** 成本控制措施题应从哪些方面组织答案？

**Back：** 影响成本基准变更因素、确保变更获批、监督绩效、记录偏差、防止未批准变更、通知干系人、采取纠偏措施。

**Extra：** 用自己的话写也可以，但要具体，避免只写“加强成本管理”。

**Tags：** `ruankao cost evm T-COST-002 case control`

## 49. 案例｜难度 4

**Front：** EVM 指标如何回到管理动作？

**Back：** 先判断偏差方向，再追根因，最后选择进度、成本、范围、变更和沟通措施。

**Extra：** 例：SPI<1 可查关键路径和资源效率；CPI<1 可查返工、采购成本、范围蔓延。

**Tags：** `ruankao cost evm T-COST-002 case action`

## 50. 陷阱｜难度 3

**Front：** 陷阱：AC 大于 PV 是否一定成本超支？

**Back：** 不一定。

**Extra：** 成本是否超支看 EV 与 AC，不是 PV 与 AC。缺 EV 时无法判断。

**Tags：** `ruankao cost evm T-COST-002 trap`

## 51. 陷阱｜难度 2

**Front：** 陷阱：CPI < 1 的含义是什么？

**Back：** 成本超支或成本效率低。

**Extra：** 不要理解成“完成了 1%”。CPI 是 EV/AC。

**Tags：** `ruankao cost evm T-COST-002 trap cpi`

## 52. 陷阱｜难度 2

**Front：** 陷阱：SPI < 1 的含义是什么？

**Back：** 进度滞后或进度效率低。

**Extra：** SPI 是 EV/PV，不是实际工期/计划工期。

**Tags：** `ruankao cost evm T-COST-002 trap spi`

## 53. 陷阱｜难度 2

**Front：** 陷阱：CV/SV 和 CPI/SPI 的量纲有什么不同？

**Back：** CV/SV 是货币差值；CPI/SPI 是无量纲指数。

**Extra：** 差值看绝对偏差，指数看效率比例。

**Tags：** `ruankao cost evm T-COST-002 trap index`

## 54. 陷阱｜难度 2

**Front：** 陷阱：EV 是否等于实际成本？

**Back：** 不等于。EV 是实际完成工作的预算价值；AC 才是实际成本。

**Extra：** 这是挣值题最常见坑。

**Tags：** `ruankao cost evm T-COST-002 trap ev ac`

## 55. 陷阱｜难度 3

**Front：** 陷阱：EAC 公式是不是固定只有一个？

**Back：** 不是。

**Extra：** EAC 取决于未来绩效假设：非典型、典型、重新估算、同时考虑进度成本等。

**Tags：** `ruankao cost evm T-COST-002 trap eac`

## 56. 陷阱｜难度 3

**Front：** 陷阱：计算完 EVM 指标，案例题是否就答完了？

**Back：** 没有。

**Extra：** 下午案例还要写状态判断、原因分析、预测和管理措施。只写公式通常不够。

**Tags：** `ruankao cost evm T-COST-002 trap case`
