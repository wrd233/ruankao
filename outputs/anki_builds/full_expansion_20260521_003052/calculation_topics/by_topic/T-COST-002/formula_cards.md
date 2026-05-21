# T-COST-002 formula_cards.md

## SV 的公式、含义和判断规则是什么？

Back：SV = EV - PV。SV > 0 进度提前；SV = 0 符合计划；SV < 0 进度滞后。

Extra：<div>理解：例：EV=90，PV=100，则 SV=-10，进度滞后。</div><div>来源：T-COST-002 试制黄金样例 / 挣值管理专题</div>

Manual review：沿用 EVM 黄金样例，Front 短、Back 可判分，Extra 指向该公式或陷阱的具体理解。

## CV 的公式、含义和判断规则是什么？

Back：CV = EV - AC。CV > 0 成本节约；CV = 0 符合预算；CV < 0 成本超支。

Extra：<div>理解：例：EV=90，AC=110，则 CV=-20，成本超支。</div><div>来源：T-COST-002 试制黄金样例 / 挣值管理专题</div>

Manual review：沿用 EVM 黄金样例，Front 短、Back 可判分，Extra 指向该公式或陷阱的具体理解。

## SPI 的公式、含义和判断规则是什么？

Back：SPI = EV / PV。SPI > 1 进度效率高于计划；SPI < 1 进度效率低于计划。

Extra：<div>理解：例：EV=80，PV=100，则 SPI=0.8，进度滞后。</div><div>来源：T-COST-002 试制黄金样例 / 挣值管理专题</div>

Manual review：沿用 EVM 黄金样例，Front 短、Back 可判分，Extra 指向该公式或陷阱的具体理解。

## CPI 的公式、含义和判断规则是什么？

Back：CPI = EV / AC。CPI > 1 成本效率高；CPI < 1 成本效率低，成本超支。

Extra：<div>理解：例：EV=80，AC=100，则 CPI=0.8，每花 1 元只挣得 0.8 元预算价值。</div><div>来源：T-COST-002 试制黄金样例 / 挣值管理专题</div>

Manual review：沿用 EVM 黄金样例，Front 短、Back 可判分，Extra 指向该公式或陷阱的具体理解。

## 非典型偏差下 EAC 怎么算？

Back：EAC = AC + (BAC - EV)。

Extra：<div>理解：题干信号：一次性、偶然、不会再出现、已纠正。例：AC=200，BAC=500，EV=180，则 EAC=520。</div><div>来源：T-COST-002 试制黄金样例 / 挣值管理专题</div>

Manual review：沿用 EVM 黄金样例，Front 短、Back 可判分，Extra 指向该公式或陷阱的具体理解。

## 典型偏差会延续时 EAC 怎么算？

Back：EAC = BAC / CPI。

Extra：<div>理解：题干信号：当前绩效将持续、按目前趋势、没有改善迹象。例：BAC=1000，CPI=0.8，则 EAC=1250。</div><div>来源：T-COST-002 试制黄金样例 / 挣值管理专题</div>

Manual review：沿用 EVM 黄金样例，Front 短、Back 可判分，Extra 指向该公式或陷阱的具体理解。

## 重新估算剩余工作时 EAC 怎么算？

Back：EAC = AC + 自下而上重新估算的 ETC。

Extra：<div>理解：适用：原估算假设严重失效，需要重新估算剩余工作。</div><div>来源：T-COST-002 试制黄金样例 / 挣值管理专题</div>

Manual review：沿用 EVM 黄金样例，Front 短、Back 可判分，Extra 指向该公式或陷阱的具体理解。

## ETC 的常用公式是什么？

Back：ETC = EAC - AC。

Extra：<div>理解：例：EAC=950，AC=380，则 ETC=570。</div><div>来源：T-COST-002 试制黄金样例 / 挣值管理专题</div>

Manual review：沿用 EVM 黄金样例，Front 短、Back 可判分，Extra 指向该公式或陷阱的具体理解。

## VAC 的公式和判断规则是什么？

Back：VAC = BAC - EAC。VAC > 0 预计结余；VAC < 0 预计超预算。

Extra：<div>理解：例：BAC=800，EAC=950，则 VAC=-150，预计超预算 150。</div><div>来源：T-COST-002 试制黄金样例 / 挣值管理专题</div>

Manual review：沿用 EVM 黄金样例，Front 短、Back 可判分，Extra 指向该公式或陷阱的具体理解。

## 以 BAC 为目标的 TCPI 怎么算？

Back：TCPI = (BAC - EV) / (BAC - AC)。

Extra：<div>理解：例：BAC=800，EV=300，AC=360，则 TCPI=500/440≈1.14。</div><div>来源：T-COST-002 试制黄金样例 / 挣值管理专题</div>

Manual review：沿用 EVM 黄金样例，Front 短、Back 可判分，Extra 指向该公式或陷阱的具体理解。

