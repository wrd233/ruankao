#!/usr/bin/env python3
"""Generate an Anki pilot deck for T-COST-002."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


OUT = Path("anki_pilot/T-COST-002")
DECK = "软考::系统集成项目管理工程师::成本管理::挣值管理"
TOPIC_ID = "T-COST-002"
TOPIC_TITLE = "挣值管理与成本绩效分析"
TAGS_BASE = "ruankao cost evm T-COST-002"


def c(note_type, front, back, extra, tags, card_type, difficulty):
    return {
        "deck": DECK,
        "note_type": note_type,
        "front": front,
        "back": back,
        "extra": extra,
        "tags": f"{TAGS_BASE} {tags}",
        "source_topic_id": TOPIC_ID,
        "source_topic_title": TOPIC_TITLE,
        "card_type": card_type,
        "difficulty": str(difficulty),
    }


CARDS = [
    # 概念卡 12
    c("Basic", "挣值管理 EVM 试图同时回答哪三个问题？", "按计划应该完成多少、实际完成了多少、实际花了多少钱。", "对应三个基础量：PV、EV、AC。EVM 的价值是把范围、进度、成本放到同一货币口径下比较。", "concept", "概念", 2),
    c("Basic", "PV（Planned Value）是什么？", "计划价值：到某一时点，按计划应该完成工作的预算价值。", "关键词是“计划应该”。PV 不看实际完成情况。项目完工时 PV 总额等于 BAC。", "concept pv", "概念", 2),
    c("Basic", "EV（Earned Value）是什么？", "挣值：实际完成工作的预算价值。", "EV 不是实际花费，而是“已完成产出按预算值多少钱”。它是 EVM 中最关键也最容易混的量。", "concept ev", "概念", 2),
    c("Basic", "AC（Actual Cost）是什么？", "实际成本：完成与 EV 对应工作实际发生的成本。", "AC 来自实际花费，但口径要和 PV/EV 保持一致，比如是否包含间接成本。", "concept ac", "概念", 2),
    c("Basic", "BAC 在挣值管理中表示什么？", "完工预算，即项目全部计划工作的总预算。", "BAC 是预测 EAC、VAC、TCPI 的基准。", "concept bac", "概念", 2),
    c("Basic", "为什么说 EV 是 EVM 的核心？", "因为 EV 把实际完成量转换成预算价值，使进度和成本都能用同一口径比较。", "进度比较 EV 与 PV；成本比较 EV 与 AC。没有 EV，很多绩效判断不能成立。", "concept ev", "概念", 3),
    c("Basic", "SV 和 CV 的单位是什么？", "货币单位，如元、万元。", "SV/CV 是差值，不是天数或百分比。SPI/CPI 才是无量纲指数。", "concept variance", "概念", 2),
    c("Basic", "SPI 和 CPI 的判断阈值是什么？", "大于 1 通常表示好，等于 1 符合计划，小于 1 表示差。", "SPI < 1 是进度效率低于计划；CPI < 1 是成本效率低于计划。", "concept index", "概念", 2),
    c("Basic", "EAC 表示什么？", "完工估算：根据当前绩效和假设预测项目完工总成本。", "EAC 不是固定公式，公式取决于题干对未来绩效的假设。", "concept forecast", "概念", 3),
    c("Basic", "ETC 表示什么？", "完工尚需估算：从当前到完工还需要的成本。", "常用关系：ETC = EAC - AC。", "concept forecast", "概念", 2),
    c("Basic", "VAC 表示什么？", "完工偏差：预算 BAC 与完工估算 EAC 的差异。", "VAC = BAC - EAC。VAC < 0 表示预计超预算。", "concept forecast", "概念", 2),
    c("Basic", "TCPI 是回顾性指标还是前瞻性指标？", "前瞻性指标。", "TCPI 表示为了实现 BAC 或 EAC，剩余工作必须达到的成本绩效水平。", "concept tcpi", "概念", 3),
    # 公式卡 11
    c("Basic", "SV 的公式、含义和判断规则是什么？", "SV = EV - PV。SV > 0 进度提前；SV = 0 符合计划；SV < 0 进度滞后。", "例：EV=90，PV=100，则 SV=-10，进度滞后。", "formula sv", "公式", 2),
    c("Basic", "CV 的公式、含义和判断规则是什么？", "CV = EV - AC。CV > 0 成本节约；CV = 0 符合预算；CV < 0 成本超支。", "例：EV=90，AC=110，则 CV=-20，成本超支。", "formula cv", "公式", 2),
    c("Basic", "SPI 的公式、含义和判断规则是什么？", "SPI = EV / PV。SPI > 1 进度效率高于计划；SPI < 1 进度效率低于计划。", "例：EV=80，PV=100，则 SPI=0.8，进度滞后。", "formula spi", "公式", 2),
    c("Basic", "CPI 的公式、含义和判断规则是什么？", "CPI = EV / AC。CPI > 1 成本效率高；CPI < 1 成本效率低，成本超支。", "例：EV=80，AC=100，则 CPI=0.8，每花 1 元只挣得 0.8 元预算价值。", "formula cpi", "公式", 2),
    c("Basic", "非典型偏差下 EAC 怎么算？", "EAC = AC + (BAC - EV)。", "题干信号：一次性、偶然、不会再出现、已纠正。例：AC=200，BAC=500，EV=180，则 EAC=520。", "formula eac", "公式", 3),
    c("Basic", "典型偏差会延续时 EAC 怎么算？", "EAC = BAC / CPI。", "题干信号：当前绩效将持续、按目前趋势、没有改善迹象。例：BAC=1000，CPI=0.8，则 EAC=1250。", "formula eac", "公式", 3),
    c("Basic", "重新估算剩余工作时 EAC 怎么算？", "EAC = AC + 自下而上重新估算的 ETC。", "适用：原估算假设严重失效，需要重新估算剩余工作。", "formula eac", "公式", 3),
    c("Basic", "同时考虑 CPI 和 SPI 的 EAC 扩展公式是什么？", "EAC = AC + (BAC - EV) / (CPI × SPI)。", "用于题干明确要求同时考虑成本和进度影响。本专题将该口径列为需回查教材的待核验项，制卡时应保留提醒。", "formula eac pending", "公式", 4),
    c("Basic", "ETC 的常用公式是什么？", "ETC = EAC - AC。", "例：EAC=950，AC=380，则 ETC=570。", "formula etc", "公式", 2),
    c("Basic", "VAC 的公式和判断规则是什么？", "VAC = BAC - EAC。VAC > 0 预计结余；VAC < 0 预计超预算。", "例：BAC=800，EAC=950，则 VAC=-150，预计超预算 150。", "formula vac", "公式", 2),
    c("Basic", "以 BAC 为目标的 TCPI 怎么算？", "TCPI = (BAC - EV) / (BAC - AC)。", "例：BAC=800，EV=300，AC=360，则 TCPI=500/440≈1.14。", "formula tcpi", "公式", 4),
    # 计算题 10
    c("Calculation", "PV=100，EV=90，AC=110。计算 SV 和 CV，并判断状态。", "SV=90-100=-10；CV=90-110=-20。进度滞后，成本超支。", "常见错法：把 PV 或 AC 当被减数。记住 EV 永远在前：SV=EV-PV，CV=EV-AC。", "calculation sv cv", "计算", 2),
    c("Calculation", "PV=200，EV=240，AC=220。计算 SPI、CPI，并判断状态。", "SPI=240/200=1.2，进度提前；CPI=240/220≈1.09，成本节约。", "指数大于 1 通常是好。", "calculation spi cpi", "计算", 2),
    c("Calculation", "SPI=0.8，CPI=1.2。如何判断项目状态？", "进度滞后，成本节约。", "SPI 管进度，CPI 管成本。两者可以一好一坏。", "calculation judgment", "计算", 2),
    c("Calculation", "BAC=500，AC=200，EV=180，偏差为一次性且不会再出现。EAC 是多少？", "EAC=AC+(BAC-EV)=200+(500-180)=520。", "题干“不会再出现”触发非典型偏差公式。", "calculation eac", "计算", 3),
    c("Calculation", "BAC=1000，EV=400，AC=500，当前成本绩效将持续。EAC 是多少？", "CPI=400/500=0.8；EAC=BAC/CPI=1000/0.8=1250。", "题干“将持续”触发典型偏差公式。", "calculation eac", "计算", 3),
    c("Calculation", "BAC=800，EV=300，AC=360。若仍要按 BAC 完工，TCPI 是多少？", "TCPI=(800-300)/(800-360)=500/440≈1.14。", "TCPI > 1 表示剩余工作必须比预算效率更高。", "calculation tcpi", "计算", 4),
    c("Calculation", "PV=600，EV=540，AC=630，BAC=1200。计算 SPI/CPI 并判断状态。", "SPI=540/600=0.9，进度滞后；CPI=540/630≈0.857，成本超支。", "如果按当前 CPI 持续，EAC≈1200/0.857≈1400，预计超预算。", "calculation comprehensive", "计算", 4),
    c("Calculation", "PV=400，EV=320，AC=380。计算 SV、CV、SPI、CPI。", "SV=-80；CV=-60；SPI=0.8；CPI≈0.842。", "下午案例中还要写文字结论：进度滞后且成本超支。", "calculation case", "计算", 3),
    c("Calculation", "只给 PV=25 万、AC=28 万，没有 EV。能否判断成本超支？", "不能。信息不足。", "成本偏差 CV=EV-AC，缺 EV 就不知道完成工作的预算价值。", "calculation insufficient", "计算", 3),
    c("Calculation", "BAC=800，EAC=950。VAC 是多少？含义是什么？", "VAC=800-950=-150，表示预计超预算 150。", "VAC 是预测偏差，不是当前偏差。", "calculation vac", "计算", 2),
    # 辨析 10
    c("Basic", "CV 和 SV 的核心区别是什么？", "CV 比较 EV 与 AC，判断成本；SV 比较 EV 与 PV，判断进度。", "两者都是 EV 在前。CV 的对手是实际花费，SV 的对手是计划价值。", "contrast cv sv", "辨析", 2),
    c("Basic", "CPI 和 SPI 的核心区别是什么？", "CPI=EV/AC 判断成本效率；SPI=EV/PV 判断进度效率。", "CPI 看花钱效率，SPI 看完成计划效率。", "contrast cpi spi", "辨析", 2),
    c("Basic", "PV、EV、AC 三者分别回答什么问题？", "PV：按计划应完成值多少；EV：实际完成值多少；AC：实际花了多少。", "不要把 EV 当 AC。EV 是产出价值，AC 是投入成本。", "contrast pv ev ac", "辨析", 2),
    c("Basic", "成本超支和进度落后一定同时出现吗？", "不一定。", "可能进度落后但成本节约，也可能进度超前但成本超支。要分别看 CPI/CV 和 SPI/SV。", "contrast status", "辨析", 2),
    c("Basic", "SV < 0 是否表示项目延误了具体多少天？", "不是。SV 的单位是货币，表示完成的预算价值低于计划值。", "要判断关键路径和具体工期，还需结合进度网络。", "contrast sv", "辨析", 3),
    c("Basic", "SPI > 1 是否保证项目一定按期或提前完工？", "不保证。", "SPI 是总体工作量效率，不专门测关键路径。关键路径活动仍可能延误。", "contrast spi critical_path", "辨析", 4),
    c("Basic", "典型偏差和非典型偏差如何区分？", "典型偏差会持续影响后续；非典型偏差是一次性、偶然、已解决。", "典型常用 EAC=BAC/CPI；非典型常用 EAC=AC+(BAC-EV)。", "contrast eac", "辨析", 3),
    c("Basic", "EAC 和 ETC 的区别是什么？", "EAC 是预计完工总成本；ETC 是从现在到完工还需要的成本。", "ETC=EAC-AC。", "contrast forecast", "辨析", 2),
    c("Basic", "VAC 和 CV 的区别是什么？", "CV 是当前成本偏差；VAC 是完工时预计偏差。", "CV=EV-AC，VAC=BAC-EAC。一个看当前，一个看预测。", "contrast variance", "辨析", 3),
    c("Basic", "为什么只有 PV 和 AC 不能判断绩效？", "因为缺少 EV，不知道实际完成工作的预算价值。", "没有 EV，就无法计算 SV、CV、SPI、CPI。", "contrast insufficient", "辨析", 3),
    # 案例模板 6
    c("CaseTemplate", "下午案例中给出 PV、EV、AC，答题第一步写什么？", "先列公式并计算 SV、CV、SPI、CPI。", "然后用文字判断：进度提前/滞后、成本节约/超支。不要只写数字。", "case template", "案例", 3),
    c("CaseTemplate", "案例题中如何判断“成本超支”？", "优先看 CV<0 或 CPI<1。", "表达模板：CV 为负、CPI 小于 1，说明实际花费超过已完成工作的预算价值，项目成本超支。", "case cost", "案例", 3),
    c("CaseTemplate", "案例题中如何判断“进度落后”？", "优先看 SV<0 或 SPI<1。", "表达模板：SV 为负、SPI 小于 1，说明实际完成工作的预算价值低于计划值，项目进度落后。", "case schedule", "案例", 3),
    c("CaseTemplate", "挣值案例题的完整答题链是什么？", "计算指标 → 判断状态 → 预测 EAC/ETC/VAC → 分析原因 → 提出措施。", "措施要对应原因，例如范围蔓延走变更控制，效率低做资源优化，关键路径延误考虑赶工/快速跟进。", "case flow", "案例", 4),
    c("CaseTemplate", "成本控制措施题应从哪些方面组织答案？", "影响成本基准变更因素、确保变更获批、监督绩效、记录偏差、防止未批准变更、通知干系人、采取纠偏措施。", "用自己的话写也可以，但要具体，避免只写“加强成本管理”。", "case control", "案例", 4),
    c("CaseTemplate", "EVM 指标如何回到管理动作？", "先判断偏差方向，再追根因，最后选择进度、成本、范围、变更和沟通措施。", "例：SPI<1 可查关键路径和资源效率；CPI<1 可查返工、采购成本、范围蔓延。", "case action", "案例", 4),
    # 陷阱 7
    c("Basic", "陷阱：AC 大于 PV 是否一定成本超支？", "不一定。", "成本是否超支看 EV 与 AC，不是 PV 与 AC。缺 EV 时无法判断。", "trap", "陷阱", 3),
    c("Basic", "陷阱：CPI < 1 的含义是什么？", "成本超支或成本效率低。", "不要理解成“完成了 1%”。CPI 是 EV/AC。", "trap cpi", "陷阱", 2),
    c("Basic", "陷阱：SPI < 1 的含义是什么？", "进度滞后或进度效率低。", "SPI 是 EV/PV，不是实际工期/计划工期。", "trap spi", "陷阱", 2),
    c("Basic", "陷阱：CV/SV 和 CPI/SPI 的量纲有什么不同？", "CV/SV 是货币差值；CPI/SPI 是无量纲指数。", "差值看绝对偏差，指数看效率比例。", "trap index", "陷阱", 2),
    c("Basic", "陷阱：EV 是否等于实际成本？", "不等于。EV 是实际完成工作的预算价值；AC 才是实际成本。", "这是挣值题最常见坑。", "trap ev ac", "陷阱", 2),
    c("Basic", "陷阱：EAC 公式是不是固定只有一个？", "不是。", "EAC 取决于未来绩效假设：非典型、典型、重新估算、同时考虑进度成本等。", "trap eac", "陷阱", 3),
    c("Basic", "陷阱：计算完 EVM 指标，案例题是否就答完了？", "没有。", "下午案例还要写状态判断、原因分析、预测和管理措施。只写公式通常不够。", "trap case", "陷阱", 3),
]


FIELDS = [
    "deck",
    "note_type",
    "front",
    "back",
    "extra",
    "tags",
    "source_topic_id",
    "source_topic_title",
    "card_type",
    "difficulty",
]


def write_text_outputs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "cards.tsv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, FIELDS, dialect="excel-tab")
        writer.writeheader()
        writer.writerows(CARDS)
    with (OUT / "cards.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, FIELDS)
        writer.writeheader()
        writer.writerows(CARDS)
    lines = ["# T-COST-002 Anki 试制卡片", ""]
    for i, card in enumerate(CARDS, 1):
        lines.extend(
            [
                f"## {i}. {card['card_type']}｜难度 {card['difficulty']}",
                "",
                f"**Front：** {card['front']}",
                "",
                f"**Back：** {card['back']}",
                "",
                f"**Extra：** {card['extra']}",
                "",
                f"**Tags：** `{card['tags']}`",
                "",
            ]
        )
    (OUT / "cards.md").write_text("\n".join(lines), encoding="utf-8")


def try_write_apkg() -> tuple[bool, str]:
    try:
        import genanki  # type: ignore
    except Exception as exc:
        return False, f"未生成 deck.apkg：当前环境未安装 genanki（{exc}）。"

    model = genanki.Model(
        2026052002,
        "Ruankao Basic Pilot",
        fields=[{"name": name} for name in FIELDS if name not in {"deck"}],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "<div class='front'>{{front}}</div>",
                "afmt": "{{FrontSide}}<hr id='answer'><div class='back'>{{back}}</div><div class='extra'>{{extra}}</div>",
            }
        ],
        css="""
        .card { font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif; font-size: 20px; line-height: 1.5; text-align: left; color: #202124; }
        .front { font-weight: 700; }
        .back { margin-top: 12px; }
        .extra { margin-top: 12px; color: #555; font-size: 16px; }
        """,
    )
    deck_id = int(hashlib.md5(DECK.encode("utf-8")).hexdigest()[:8], 16)
    deck = genanki.Deck(deck_id, DECK)
    for card in CARDS:
        guid = hashlib.md5((card["front"] + card["back"]).encode("utf-8")).hexdigest()
        note = genanki.Note(model=model, fields=[card[name] for name in FIELDS if name != "deck"], guid=guid, tags=card["tags"].split())
        deck.add_note(note)
    genanki.Package(deck).write_to_file(str(OUT / "deck.apkg"))
    return True, "已生成 deck.apkg。"


def write_readme_and_report(apkg_ok: bool, apkg_msg: str) -> None:
    counts = {}
    for card in CARDS:
        counts[card["card_type"]] = counts.get(card["card_type"], 0) + 1
    dist = "\n".join(f"- {k}：{v} 张" for k, v in sorted(counts.items()))
    readme = f"""# T-COST-002 Anki 试制包

选择专题：`T-COST-002｜挣值管理与成本绩效分析`

## 文件

- `cards.md`：人工审阅版。
- `cards.tsv`：Anki 导入推荐文件，字段用 Tab 分隔。
- `cards.csv`：表格软件查看版。
- `deck.apkg`：{'已生成，可直接导入 Anki。' if apkg_ok else '未生成，见 generation_report.md。'}
- `generation_report.md`：生成报告。

## 卡片分布

{dist}

## 导入方法

如果使用 `cards.tsv` 导入 Anki，请选择 UTF-8 编码、字段分隔符为 Tab，并按表头映射字段。若 `deck.apkg` 存在，可直接双击或通过 Anki 的“文件 → 导入”导入。
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")
    report = f"""# T-COST-002 Anki 试制生成报告

## 选择专题

- 专题：`T-COST-002｜挣值管理与成本绩效分析`
- 选择理由：公式体系完整，能检验概念卡、公式卡、计算卡、辨析卡、案例模板卡和陷阱卡。

## 输出结果

- 卡片总数：{len(CARDS)}
{dist}
- `deck.apkg`：{'是' if apkg_ok else '否'}
- APKG 状态：{apkg_msg}

## 字段

`deck`、`note_type`、`front`、`back`、`extra`、`tags`、`source_topic_id`、`source_topic_title`、`card_type`、`difficulty`

## 需要人工检查的卡片

- 同时考虑 `CPI × SPI` 的 EAC 扩展公式卡：专题中已标注教材口径待核验，卡片 extra 中保留提醒。
- 案例模板卡：建议结合近年下午题评分口径微调措辞。
- 所有计算卡：建议人工抽查数值和四舍五入口径。

## 后续建议

本试制包适合验证制卡粒度。若效果可接受，再扩展到进度、风险和沟通渠道等计算专题；全量制卡前应先处理高优先级 `[待核验]`。
"""
    (OUT / "generation_report.md").write_text(report, encoding="utf-8")


def main() -> None:
    write_text_outputs()
    ok, msg = try_write_apkg()
    write_readme_and_report(ok, msg)
    print(f"cards={len(CARDS)} apkg={ok}")


if __name__ == "__main__":
    main()

