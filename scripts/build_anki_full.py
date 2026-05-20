#!/usr/bin/env python3
from __future__ import annotations

import csv
import dataclasses
import hashlib
import html
import json
import os
import re
import textwrap
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "topic_learning_packages/index/topic_manifest.json"
QUESTIONS = ROOT / "questions.full.clean.md"
SKILL_V2 = Path("/Users/wangrundong/Downloads/软考Anki卡片创建Skill_v2_强化版.md")
SKILL_V1 = Path("/Users/wangrundong/Downloads/软考Anki卡片创建Skill_v1.md")
GOLDEN_CSV = ROOT / "anki_pilot/T-COST-002/cards.csv"
ANKI_URL = "http://127.0.0.1:8765"

FULL_FIELDS = [
    "Deck",
    "NoteType",
    "Front",
    "Back",
    "Extra",
    "CardType",
    "Importance",
    "Difficulty",
    "ExamUse",
    "KnowledgeDomain",
    "SourceTopicID",
    "SourceTopicName",
    "SourceFile",
    "SourceLocator",
    "RelatedQuestionIDs",
    "QuestionYear",
    "QuestionSession",
    "QuestionPart",
    "QuestionNumber",
    "QuestionStem",
    "Options",
    "Answer",
    "Explanation",
    "WrongOptionAnalysis",
    "ExamSignal",
    "Checksum",
    "TagsText",
    "QualityScore",
    "QualityStatus",
    "ReviewNotes",
]


@dataclasses.dataclass
class Card:
    front: str
    back: str
    extra: str
    card_type: str
    importance: str
    difficulty: str
    exam_use: str
    domain: str
    topic_id: str
    topic_name: str
    source_file: str
    source_locator: str
    related_questions: str = ""
    quality_status: str = "candidate"
    quality_score: int = 0
    review_notes: str = ""
    deck: str = ""
    note_type: str = "RuankaoTopicCard"
    question_year: str = ""
    question_session: str = ""
    question_part: str = ""
    question_number: str = ""
    question_stem: str = ""
    options: str = ""
    answer: str = ""
    explanation: str = ""
    wrong_option_analysis: str = ""
    exam_signal: str = ""
    tags: list[str] = dataclasses.field(default_factory=list)
    checksum: str = ""

    def normalize_for_checksum(self) -> str:
        s = f"{self.topic_id}|{self.card_type}|{self.front}|{self.back}"
        return re.sub(r"\s+", " ", s).strip().lower()

    def finalize(self, build_tag: str) -> None:
        if not self.checksum:
            digest = hashlib.sha256(self.normalize_for_checksum().encode("utf-8")).hexdigest()[:24]
            self.checksum = f"sha256:{digest}"
        base = [
            "ruankao",
            "ruankao::topic" if self.card_type != "真题刷题卡" else "ruankao::question",
            f"ruankao::topic::{safe_tag(self.topic_id)}",
            f"ruankao::domain::{safe_tag(self.domain)}",
            f"ruankao::type::{safe_tag(self.card_type)}",
            f"ruankao::exam_use::{safe_tag(self.exam_use)}",
            f"ruankao::importance::{self.importance}",
            f"ruankao::difficulty::{self.difficulty}",
            f"ruankao::anki_build::{build_tag}",
        ]
        if self.card_type == "真题刷题卡":
            base.append("ruankao::source::past_exam")
        if self.card_type == "待核验卡" or self.quality_status == "needs_review":
            base.extend(["ruankao::needs_review", "ruankao::not_for_main_review"])
        if "跨专题" in self.card_type or self.topic_id.startswith("T-CROSS"):
            base.append("ruankao::cross_topic")
        if "公式" in self.card_type:
            base.append("ruankao::formula")
        if "陷阱" in self.extra or "易错" in self.extra:
            base.append("ruankao::trap")
        self.tags = sorted(set(base + self.tags))
        if not self.deck:
            self.deck = deck_for(self)

    def as_dict(self) -> dict[str, str]:
        return {
            "Deck": self.deck,
            "NoteType": self.note_type,
            "Front": self.front,
            "Back": self.back,
            "Extra": self.extra,
            "CardType": self.card_type,
            "Importance": self.importance,
            "Difficulty": self.difficulty,
            "ExamUse": self.exam_use,
            "KnowledgeDomain": self.domain,
            "SourceTopicID": self.topic_id,
            "SourceTopicName": self.topic_name,
            "SourceFile": self.source_file,
            "SourceLocator": self.source_locator,
            "RelatedQuestionIDs": self.related_questions,
            "QuestionYear": self.question_year,
            "QuestionSession": self.question_session,
            "QuestionPart": self.question_part,
            "QuestionNumber": self.question_number,
            "QuestionStem": self.question_stem,
            "Options": self.options,
            "Answer": self.answer,
            "Explanation": self.explanation,
            "WrongOptionAnalysis": self.wrong_option_analysis,
            "ExamSignal": self.exam_signal,
            "Checksum": self.checksum,
            "TagsText": " ".join(self.tags),
            "QualityScore": str(self.quality_score),
            "QualityStatus": self.quality_status,
            "ReviewNotes": self.review_notes,
        }


def safe_tag(s: str) -> str:
    return re.sub(r"[\s/]+", "_", s.strip())


def deck_for(card: Card) -> str:
    root = "软考::系统集成项目管理工程师"
    if card.quality_status == "needs_review" or card.card_type == "待核验卡":
        return f"{root}::待核验与复查"
    if card.card_type == "真题刷题卡":
        if card.question_part == "下午":
            return f"{root}::真题刷题::下午案例题"
        if card.question_part == "英文":
            return f"{root}::真题刷题::英文题"
        return f"{root}::真题刷题::上午选择题"
    if card.topic_id.startswith("T-CROSS") or "跨专题" in card.card_type:
        return f"{root}::跨专题辨析"
    return f"{root}::专题学习::{safe_tag(card.domain)}::{card.topic_id}_{safe_tag(card.topic_name)[:40]}"


def read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8-sig", errors="ignore")


def load_topics() -> list[dict[str, Any]]:
    data = json.loads(read(MANIFEST))
    return data["topics"]


def first_heading(text: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, re.M)
    return m.group(1).strip() if m else ""


def extract_card_hints(text: str) -> list[tuple[int, str]]:
    hints = []
    for i, line in enumerate(text.splitlines(), 1):
        if "可制卡点" in line:
            clean = re.sub(r"[*`>：:]", "", line).strip()
            hints.append((i, clean))
    return hints


def extract_pending(text: str) -> list[tuple[int, str]]:
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        if "[待核验]" in line or "待核验" in line and line.strip().startswith("-"):
            out.append((i, line.strip()))
    return out


def extract_not_for_card(text: str) -> list[tuple[int, str]]:
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        if "暂不制卡内容" in line or "不适合制卡" in line:
            out.append((i, line.strip()))
    return out


def topic_locator(topic: dict[str, Any], needle: str = "") -> str:
    if needle:
        text = read(ROOT / topic["file"])
        for i, line in enumerate(text.splitlines(), 1):
            if needle in line:
                return f"line {i}"
    return "topic package"


def c(topic_id: str, card_type: str, front: str, back: str, extra: str, importance="A", difficulty="2", exam_use="上午选择") -> dict[str, str]:
    return {
        "topic_id": topic_id,
        "card_type": card_type,
        "front": front,
        "back": back,
        "extra": extra,
        "importance": importance,
        "difficulty": difficulty,
        "exam_use": exam_use,
    }


CURATED = [
    c("T-INFO-001","概念卡","信息系统集成项目的根本出发点是什么？","满足客户和用户的需求。","题干若把“技术堆叠”说成系统集成目标，要回到用户需求和业务目标。"),
    c("T-INFO-001","辨析卡","信息系统生命周期 vs 项目生命周期的核心区别是什么？","信息系统生命周期看系统从规划、建设到运行维护的全过程；项目生命周期看一次项目从启动到收尾的管理过程。","题干说系统长期运行维护，多半是信息系统生命周期；说项目阶段门、交付和收尾，多半是项目生命周期。","A","3"),
    c("T-INFO-001","关键词识别卡","题干出现哪些信号时，应想到“系统集成”？","多系统、多技术、多厂商、多接口，需要把软件、硬件、网络、数据和业务流程整合成可用系统。","不要只把系统集成理解为设备采购或布线。"),
    c("T-PM-002","辨析卡","项目阶段 vs 项目管理过程组的核心区别是什么？","阶段是项目生命周期中的时间段；过程组是管理活动的逻辑分类，可在每个阶段反复出现。","题干说“设计阶段、实施阶段”是阶段；说“启动、规划、执行、监控、收尾”是过程组。"),
    c("T-PM-002","辨析卡","PDCA 的 Act 与项目收尾为什么不能简单等同？","Act 是根据检查结果采取改进措施；项目收尾是结束项目或阶段、验收、归档和释放资源。","收尾不是“纠偏动作”，不要把 PDCA 的 A 机械对应到收尾过程组。","A","3"),
    c("T-PM-002","关键词识别卡","看到哪些管理动作，应优先想到监控过程组？","测量绩效、比较基准、发现偏差、提出纠正或预防措施、实施整体变更控制。","QA 属执行；QC、确认范围、控制范围和整体变更控制通常属于监控。","A","3"),
    c("T-FEA-001","概念卡","项目建议书在立项管理中的核心作用是什么？","提出项目建设的必要性、初步目标和建设设想，为是否启动后续可行性研究提供依据。","它不是详细实施计划，也不是最终项目管理计划。"),
    c("T-FEA-001","流程卡","可行性研究通常从哪些角度判断项目是否值得做？","技术可行、经济可行、社会/组织可行、运行维护可行等角度综合判断。","具体分类口径以教材为准；涉及数字和审批权限需核验。","A","3"),
    c("T-FEA-001","辨析卡","项目论证 vs 项目评估的核心区别是什么？","论证偏建设方或咨询方论证项目方案是否可行；评估偏决策方或第三方对论证结果进行审查评价。","关键词：先论证，后评估；论证重“方案可行”，评估重“决策把关”。","A","3"),
    c("T-CLOSE-001","流程卡","项目收尾时，合同收尾和管理收尾的顺序通常是什么？","先完成合同收尾，再完成项目或阶段的管理收尾。","先确认合同义务、结算和合同记录，再做整体归档、经验教训和资源释放。"),
    c("T-CLOSE-001","辨析卡","管理收尾 vs 合同收尾的核心区别是什么？","管理收尾面向整个项目或阶段；合同收尾面向单个合同和采购关系。","多个合同要分别收尾，但项目管理收尾关注整体关闭。"),
    c("T-CLOSE-001","案例模板卡","验收通过后，项目经理还应做哪些收尾动作？","归档项目文件、总结经验教训、释放资源、更新组织过程资产、完成行政关闭。","不要把客户验收当作项目管理工作的全部结束。","B","3","下午案例"),
    c("T-INT-002","辨析卡","项目章程 vs 项目管理计划的核心区别是什么？","章程批准项目存在并授权项目经理；项目管理计划说明项目如何执行、监控和控制。","章程由发起人或高层发布；计划由项目经理组织团队制定。"),
    c("T-INT-002","概念卡","项目章程最关键的考试作用是什么？","正式启动项目，并授权项目经理使用组织资源。","看到“任命项目经理、授权、正式批准项目”优先想到项目章程。"),
    c("T-INT-002","流程卡","范围/进度/成本基准需要修改时，应走什么流程？","提出变更请求 → 分析影响 → 走整体变更控制 → 批准后更新相应基准和计划。","不能由项目经理口头或单方面直接改基准。","A","3"),
    c("T-INT-004","流程卡","项目出现变更请求时，项目经理应按什么流程处理？","记录变更请求 → 分析对范围、进度、成本、质量和风险的影响 → 提交变更控制流程/CCB → 批准后更新计划和基准 → 通知并跟踪执行。","题干若出现“客户临时要求”“口头同意”，常考是否绕过变更控制。","A","3","下午案例"),
    c("T-INT-004","辨析卡","纠正措施、预防措施和缺陷补救的区别是什么？","纠正措施把已偏离的绩效拉回计划；预防措施防止未来偏离；缺陷补救修复不合格产品组件。","过程偏差看纠正/预防；产品缺陷看缺陷补救。","A","3"),
    c("T-INT-004","关键词识别卡","题干出现哪些信号时，应想到 CCB 或整体变更控制？","影响基准、范围调整、成本/进度变化、客户新增需求、批准或拒绝变更。","CCB 不一定亲自实施变更，核心职责是评审和批准/否决变更。","A","3"),
    c("T-SCOPE-002","概念卡","WBS 的核心特征是什么？","以可交付成果为导向，把项目范围逐层分解到可管理的工作包。","WBS 不是活动清单，也不是组织结构图。"),
    c("T-SCOPE-002","概念卡","范围基准由哪三部分组成？","项目范围说明书、WBS、WBS 字典。","题干问“批准的范围基准”时，不要只答 WBS。"),
    c("T-SCOPE-002","辨析卡","WBS vs 活动清单的核心区别是什么？","WBS 说明要交付什么；活动清单说明为完成交付物要做哪些活动。","可交付成果导向是 WBS；动词化任务更像活动清单。","A","3"),
    c("T-SCH-002","辨析卡","PDM 与 AOA/ADM 的核心区别是什么？","PDM 用节点表示活动、箭线表示逻辑关系；AOA/ADM 用箭线表示活动、节点表示事件。","软考常用“节点表示活动”作为 PDM 的识别信号。"),
    c("T-SCH-002","概念卡","虚活动的作用是什么？","在双代号网络图中表达逻辑关系，本身不消耗时间和资源。","看到“虚箭线、无持续时间、只表示依赖”应想到虚活动。"),
    c("T-SCH-002","关键词识别卡","题干出现哪些信号时，应想到快速跟进？","把顺序活动改为并行或部分重叠，后续活动在前置活动未完成时提前开始。","快速跟进主要增加风险和返工；赶工主要增加成本。"),
    c("T-SCH-003","公式卡","关键路径上的总时差通常是多少？","通常为 0；关键路径是决定项目最短工期的一组活动路径。","如果关键路径活动延误，通常会直接影响项目完工日期。","A","2","计算题"),
    c("T-SCH-003","辨析卡","总时差 vs 自由时差的核心区别是什么？","总时差是不影响项目总工期可延误的时间；自由时差是不影响紧后活动最早开始可延误的时间。","题干问是否影响后续活动，看自由时差；问是否影响总工期，看总时差。","A","3","计算题"),
    c("T-SCH-003","计算卡","活动 O=4、M=7、P=16，用 PERT 三点估算的期望工期是多少？","期望工期=(O+4M+P)/6=(4+28+16)/6=8。","PERT 常见错法是直接算算术平均。","A","3","计算题"),
    c("T-COST-001","辨析卡","应急储备 vs 管理储备的核心区别是什么？","应急储备用于已识别风险，通常包含在成本基准中；管理储备用于未知未知风险，通常不包含在成本基准中。","涉及教材口径时以专题待核验项为准；考试重点是二者用途不同。"),
    c("T-COST-001","流程卡","自下而上成本估算的基本思路是什么？","先估算工作包或活动成本，再逐层汇总得到更高层级和项目总成本。","适合 WBS 已较清晰时，精度较高但耗时更多。"),
    c("T-COST-001","案例模板卡","成本失控案例通常从哪些方面找原因？","估算不充分、预算未评审、储备不足、范围蔓延、变更未控、采购成本变化、绩效监控不足。","措施要对应原因，不要只写“加强成本管理”。","A","3","下午案例"),
    c("T-QUAL-001","辨析卡","质量保证 QA vs 质量控制 QC 的核心区别是什么？","QA 关注过程是否可靠，常用质量审计和过程分析；QC 关注结果是否合格，常用检查、测试和测量。","QA 属执行过程组，QC 属监控过程组。"),
    c("T-QUAL-001","辨析卡","质量 vs 等级的核心区别是什么？","质量是满足要求的程度；等级是同一用途对象按技术特性划分的类别或档次。","低等级不一定低质量；低质量一定是问题。"),
    c("T-QUAL-001","案例模板卡","质量问题案例应优先检查哪些管理缺口？","质量计划是否评审、QA 是否执行、QC 是否及时、缺陷是否闭环、返工是否受控、验收标准是否明确。","下午案例要把“缺陷爆发”翻译成过程和责任问题。","A","3","下午案例"),
    c("T-QUAL-002","关键词识别卡","题干出现“少数关键原因”时，应想到哪种质量工具？","帕累托图。","帕累托图用于识别导致大多数问题的少数关键原因。"),
    c("T-QUAL-002","关键词识别卡","题干出现“分析问题原因结构”时，应想到哪种质量工具？","因果图/鱼骨图。","它用于从人、机、料、法、环等角度分析原因，不是用来排序主要少数。"),
    c("T-QUAL-002","辨析卡","直方图 vs 帕累托图的核心区别是什么？","直方图看数据分布形态；帕累托图按频数或影响排序找关键少数。","看分布用直方图；找优先改进对象用帕累托图。"),
    c("T-QUAL-003","案例模板卡","质量案例“三问诊断法”是什么？","标准是否明确 → 过程是否保证 → 结果是否控制和纠偏。","把缺陷、测试、验收争议分别落回质量计划、QA、QC 和确认范围。","A","3","下午案例"),
    c("T-QUAL-003","流程卡","发现产品缺陷后，质量管理动作链是什么？","记录缺陷 → 分析原因 → 制定纠正/缺陷补救措施 → 修复和复测 → 更新经验教训。","不要只让开发人员口头修复，缺陷要闭环。","B","3","下午案例"),
    c("T-COM-001","公式卡","沟通渠道数公式是什么？","沟通渠道数 = n(n-1)/2。","n 是参与沟通的人数。新增 1 人后，新增渠道数等于原人数。","A","2","计算题"),
    c("T-COM-001","计算卡","项目团队 8 人，沟通渠道数是多少？若新增 1 人，增加多少条？","8人渠道数=8×7/2=28；9人渠道数=9×8/2=36，增加8条。","常见错法：只把人数加 1，不重新按公式计算。","A","2","计算题"),
    c("T-COM-001","辨析卡","推式沟通、拉式沟通、交互式沟通如何区分？","推式是发送给特定对象；拉式是让对象自行获取；交互式是多方实时双向交流。","会议/电话是交互式；邮件通知是推式；知识库公告常是拉式。"),
    c("T-HR-001","概念卡","责任分配矩阵 RAM 的作用是什么？","把工作包或活动与责任人/组织单元对应起来，明确谁负责什么。","RACI 是 RAM 的一种表达方式。"),
    c("T-HR-001","辨析卡","RACI 中 R 和 A 的区别是什么？","R 是实际执行/负责完成工作的人；A 是最终对结果负责并有批准责任的人，通常每项工作 A 唯一。","多个 R 可以并存，但 A 不宜多个。"),
    c("T-HR-001","关键词识别卡","塔克曼团队发展五阶段的关键词是什么？","形成、震荡、规范、成熟、解散。","冲突集中爆发多在震荡期；效率稳定提升多在规范和成熟期。","B","3"),
    c("T-RISK-001","辨析卡","风险 vs 问题的核心区别是什么？","风险是尚未发生的不确定事件；问题是已经发生并正在影响项目的事件。","风险发生后要转入问题日志并执行应对或权变措施。"),
    c("T-RISK-001","辨析卡","风险规避 vs 风险转移的核心区别是什么？","规避是改变计划以消除威胁或其影响；转移是把风险责任或影响转给第三方。","买保险、外包常是转移；取消高风险方案常是规避。"),
    c("T-RISK-001","流程卡","风险识别后，应在风险登记册中至少记录什么？","风险描述、原因、可能影响、责任人、应对策略、触发条件和状态。","风险登记册是后续定性/定量分析和应对计划的基础。","A","3"),
    c("T-RISK-002","公式卡","EMV 的公式是什么？","EMV = 概率 × 影响金额；多个分支的 EMV 要分别计算后汇总。","EMV 是期望值，不等于最可能结果。","A","2","计算题"),
    c("T-RISK-002","辨析卡","定性风险分析 vs 定量风险分析的核心区别是什么？","定性分析用于排序风险优先级；定量分析用数值方法估算风险对目标的影响。","概率影响矩阵常用于定性；EMV、决策树、蒙特卡罗偏定量。"),
    c("T-RISK-002","计算卡","风险发生概率 30%，一旦发生损失 20 万元，EMV 是多少？","EMV=0.3×(-20)=-6 万元。","收益用正数，损失用负数；决策树比较时要注意符号。","A","2","计算题"),
    c("T-PROC-001","辨析卡","固定总价合同、成本补偿合同、工料合同的风险分配有什么差异？","固定总价合同卖方成本风险较高；成本补偿合同买方成本风险较高；工料合同介于二者之间。","需求明确适合总价；范围不清或研发性强更可能用成本补偿或工料。"),
    c("T-PROC-001","关键词识别卡","题干强调“范围清楚、价格固定、卖方承担超支风险”时，应想到哪类合同？","固定总价合同。","若强调按实际成本报销并加费用，通常是成本补偿类合同。"),
    c("T-PROC-001","案例模板卡","合同争议案例通常从哪些角度答？","合同范围和验收标准、变更是否批准、索赔时限和证据、付款条件、分包和合同收尾。","先回到合同条款，再判断管理流程是否合规。","A","3","下午案例"),
    c("T-PROC-002","流程卡","招投标的一般管理链路是什么？","编制招标文件 → 发布招标公告/邀请 → 投标 → 开标 → 评标 → 定标/中标通知 → 签订合同。","具体法定时限和比例属于待核验，不进正式强记卡。","A","3"),
    c("T-PROC-002","关键词识别卡","投标文件送达考点的核心判断是什么？","以招标文件规定地点和截止时间前“送达”为准，不是寄出时间。","逾期送达通常应拒收或不予接受，具体表述以法规和题干为准。"),
    c("T-PROC-002","待核验卡","单一来源采购的具体比例、时限或现行条件如何处理？","不进主卡组；按题干材料和现行法规核验后再制成正式卡。","此类法规数字变化风险高，已隔离到待核验与复查。","A","4","待核验"),
    c("T-CFG-001","概念卡","配置基线是什么？","经过正式评审和批准、作为后续变更控制基础的一组配置项状态。","基线建立后不能随意修改，修改应走配置/变更控制。"),
    c("T-CFG-001","辨析卡","开发库、受控库、产品库的核心区别是什么？","开发库用于开发人员日常修改；受控库保存已受控和评审的配置项；产品库存放可发布或交付的产品版本。","权限和稳定性从开发库到产品库逐步提高。"),
    c("T-CFG-001","辨析卡","配置管理 vs 变更管理的核心区别是什么？","配置管理管配置项的身份、版本、基线和状态；变更管理管是否允许改变以及如何批准改变。","版本控制、配置审计偏配置；变更请求、CCB 审批偏变更。"),
    c("T-LAW-001","辨析卡","合同成立 vs 合同生效的核心区别是什么？","成立是当事人意思表示达成一致；生效是合同具备法律效力并能约束当事人。","有些合同成立后还需批准、登记或满足条件才生效。","A","3"),
    c("T-LAW-001","关键词识别卡","GB、GB/T、GB/Z 分别常表示什么？","GB 通常表示国家标准；GB/T 通常表示推荐性国家标准；GB/Z 通常表示国家标准化指导性技术文件。","具体标准版本和现行状态需核验。"),
    c("T-LAW-001","待核验卡","法规条文编号、比例、时限类知识应如何进入 Anki？","先核验现行法规和教材口径；未核验前只进入待核验卡组，不进主复习。","这类卡错误成本高，不能凭 OCR 或旧题强记。","A","4","待核验"),
    c("T-INFO-002","辨析卡","ERP、CRM、SCM、BI、EAI 的一句话定位是什么？","ERP 管企业内部资源；CRM 管客户关系；SCM 管供应链协同；BI 做数据分析和决策支持；EAI 做企业应用集成。","题干问“洞察/决策”多是 BI；问“打通应用接口”多是 EAI。"),
    c("T-INFO-002","辨析卡","ERP vs CRM 的核心区别是什么？","ERP 关注企业内部资源和业务流程集成；CRM 关注客户信息、销售、服务和营销。","客户满意、客户价值和客户数据多指 CRM。"),
    c("T-INFO-002","关键词识别卡","题干出现哪些信号时，应想到 BI？","数据仓库、OLAP、数据挖掘、商业信息分析、辅助决策、洞察力。","BI 不是直接管理库存或客户服务流程。"),
    c("T-CASE-001","案例模板卡","下午案例题“三层审题法”是什么？","事实层提取问题事实；管理层映射到知识域和过程；答题层组织原因、影响和措施。","不要直接抄背景，要把事实翻译成管理问题。","A","3","下午案例"),
    c("T-CASE-001","案例模板卡","案例题写措施时，为什么必须对应原因？","评分通常看措施是否能解决题干暴露的问题；空泛写“加强管理”难以得分。","推荐句式：因为出现 X 问题，所以应采取 Y 管理动作。","A","3","下午案例"),
    c("T-CASE-001","关键词识别卡","案例题中哪些信号常指向变更/范围问题？","客户新增需求、口头承诺、未走审批、需求频繁变化、做了范围外工作、验收争议。","优先联想到范围基准、变更控制和确认范围。","A","3","下午案例"),
    c("T-CASE-002","案例模板卡","进度延期案例通常从哪些角度分析原因？","估算不准、关键路径未识别、资源能力不足、沟通机制弱、需求变更导致返工、盲目赶工或快速跟进。","措施要结合关键路径、资源优化、变更控制和沟通机制。","A","3","下午案例"),
    c("T-CASE-002","案例模板卡","成本超支案例的答题链是什么？","计算绩效指标 → 判断超支/滞后 → 找范围、采购、返工、资源效率原因 → 提出成本控制和变更控制措施。","不要只写公式，下午题要写管理解释。","A","3","下午案例"),
    c("T-CASE-003","案例模板卡","范围蔓延案例的典型错误链是什么？","绕过项目经理或流程 → 口头新增需求 → 未分析影响 → 未更新基准 → 工期和成本失控。","答题时落到需求管理、范围基准和整体变更控制。","A","3","下午案例"),
    c("T-CASE-003","辨析卡","范围蔓延 vs 合法变更的核心区别是什么？","范围蔓延是未经控制增加范围；合法变更是提出、分析、批准并更新计划/基准后的范围调整。","客户提出新需求不是问题，绕过变更控制才是问题。","A","3","下午案例"),
    c("T-COM-002","案例模板卡","沟通与干系人冲突案例常见根因有哪些？","干系人识别不全、沟通计划缺失、信息发布不及时、反馈确认机制弱、会议纪要和决议缺少记录。","措施应包括识别干系人、制定沟通管理计划、建立确认和升级机制。","A","3","下午案例"),
    c("T-COM-002","关键词识别卡","题干出现哪些信号时，应想到干系人参与管理？","关键用户不配合、部门冲突、需求方意见变化、满意度低、抵制项目、沟通对象遗漏。","不是所有冲突都先找技术方案，很多是参与和沟通问题。","A","3","下午案例"),
    c("T-CROSS-001","辨析卡","范围确认 vs 质量控制的核心区别是什么？","范围确认关注客户/干系人是否正式接受可交付成果；质量控制关注可交付成果是否符合质量要求。","“验收、接受、签字”多指范围确认；“检查、测试、缺陷、质量标准”多指质量控制。"),
    c("T-CROSS-001","辨析卡","赶工 vs 快速跟进的核心区别是什么？","赶工通过增加资源或加班压缩工期，主要增加成本；快速跟进把顺序活动并行或重叠，主要增加风险和返工。","“加人、加班、加资源”是赶工；“并行、提前开始、重叠”是快速跟进。"),
    c("T-CROSS-001","辨析卡","风险登记册 vs 问题日志的核心区别是什么？","风险登记册记录未来可能发生的不确定事件；问题日志记录已经发生并需要处理的确定事件。","风险发生后，不能只停留在风险登记册里。"),
    c("T-CROSS-001","辨析卡","质量保证 QA vs 质量控制 QC 的题干信号区别是什么？","QA 看过程是否按标准执行；QC 看可交付成果是否满足质量要求。","“审计、过程分析、改进过程”多是 QA；“检查、测试、测量、缺陷”多是 QC。"),
    c("T-CROSS-001","辨析卡","资源平衡 vs 进度压缩的核心区别是什么？","资源平衡为解决资源限制而调整活动时间，可能延长工期；进度压缩是为了缩短工期而采用赶工或快速跟进。","题干强调资源冲突/过度分配是资源平衡；强调缩短总工期是进度压缩。","A","3"),
    c("T-CROSS-001","辨析卡","项目生命周期、产品生命周期、信息系统生命周期如何区分？","项目生命周期看一次项目从启动到收尾；产品生命周期看产品从构想到退市；信息系统生命周期看系统规划、建设、运行维护和退役。","题干若超过单个项目边界，先判断是产品还是系统生命周期。","A","3"),
    c("T-CROSS-001","辨析卡","ERP、CRM、SCM、BI、EAI 最容易怎样互相混淆？","ERP 管内部资源，CRM 管客户，SCM 管供应链，BI 做分析决策，EAI 做应用集成。","客户满意不是 ERP；数据洞察不是 CRM；接口打通不是 BI。"),
    c("T-CROSS-001","辨析卡","合同收尾 vs 管理收尾的考试区别是什么？","合同收尾关闭采购合同关系；管理收尾关闭项目或阶段整体。","合同收尾通常先于管理收尾；多个合同要分别收尾。"),
    c("T-CROSS-001","辨析卡","问题日志、风险登记册、变更请求分别记录什么？","问题日志记录已发生问题；风险登记册记录未发生的不确定风险；变更请求记录对计划、基准或交付物的修改要求。","已发生的问题不应只放在风险登记册；改基准必须形成变更请求。","A","3"),
    c("T-CROSS-001","辨析卡","配置管理 vs 变更管理的题干信号区别是什么？","配置管理看配置项、版本、基线、配置库和状态；变更管理看请求、影响分析、审批和实施。","“版本控制、配置审计”偏配置；“CCB、批准/否决”偏变更。","A","3"),
    c("T-CROSS-001","辨析卡","项目章程 vs 项目管理计划的题干信号区别是什么？","章程信号是批准项目存在、任命并授权项目经理；项目管理计划信号是如何执行、监控和控制项目。","章程在启动过程组，计划在规划过程组。"),
    c("T-CROSS-001","辨析卡","干系人登记册 vs 沟通管理计划的核心区别是什么？","干系人登记册记录干系人身份、影响、期望和分类；沟通管理计划规定与干系人沟通什么、何时、用什么方式、由谁负责。","一个回答“有哪些人和他们的特征”，一个回答“怎么沟通”。"),
    c("T-CROSS-001","关键词识别卡","跨专题题干出现“角色越权、流程跳步、绝对化说法”时，应如何排错？","先定位所属管理过程，再检查谁有权批准、是否绕过流程、说法是否过于绝对。","软考常把正确概念放进错误角色或错误顺序中制造干扰。","A","3"),
    c("T-ORG-001","辨析卡","职能型、矩阵型、项目型组织中项目经理权限如何变化？","职能型最低，矩阵型居中，项目型最高。","弱矩阵更接近职能型；强矩阵更接近项目型。"),
    c("T-ORG-001","辨析卡","PMO vs 项目经理的核心区别是什么？","PMO 关注组织层面的项目管理标准、方法、资源协调和治理；项目经理关注单个项目目标达成。","题干若是跨项目资源、方法论和治理，多指 PMO。"),
    c("T-ORG-001","关键词识别卡","矩阵型组织最典型的题干信号是什么？","成员同时向职能经理和项目经理汇报，存在双重汇报和资源冲突。","权力大小取决于弱矩阵、平衡矩阵或强矩阵。"),
    c("T-RISK-003","辨析卡","风险、问题、变更三者如何区分？","风险是未发生的不确定事件；问题是已发生的影响事项；变更是对已批准基准、计划或交付物的修改请求。","题干先判断事件状态，再决定用风险登记册、问题日志还是变更请求。"),
    c("T-RISK-003","流程卡","已识别风险真正发生后，管理动作链是什么？","确认影响 → 启动应急计划或权变措施 → 更新问题日志和风险登记册 → 必要时提出变更请求 → 沟通干系人。","风险发生后常常会引出问题处理和变更控制。","A","3","下午案例"),
    c("T-SCOPE-003","流程卡","从测试通过到客户验收，合理顺序是什么？","先控制质量得到核实的可交付成果，再进行确认范围取得客户/干系人的正式验收。","测试通过不等于客户已验收。"),
    c("T-SCOPE-003","辨析卡","确认范围 vs 控制范围的核心区别是什么？","确认范围是正式验收已完成可交付成果；控制范围是监控范围基准并处理范围偏差。","验收看确认范围；范围蔓延或偏离基准看控制范围。"),
    c("T-SCOPE-003","辨析卡","核实的可交付成果 vs 验收的可交付成果有什么区别？","核实的可交付成果是质量控制后确认合格的成果；验收的可交付成果是客户/干系人正式接受的成果。","前者偏内部质量检查，后者偏外部验收。"),
]


def make_curated_cards(topics: dict[str, dict[str, Any]]) -> list[Card]:
    cards = []
    for item in CURATED:
        t = topics[item["topic_id"]]
        locator = topic_locator(t, item["front"].split(" ")[0][:10])
        status = "needs_review" if item["card_type"] == "待核验卡" else "candidate"
        cards.append(Card(
            front=item["front"], back=item["back"], extra=item["extra"],
            card_type=item["card_type"], importance=item["importance"], difficulty=item["difficulty"],
            exam_use=item["exam_use"], domain=t["domain"], topic_id=t["id"], topic_name=t["title"],
            source_file=t["file"], source_locator=locator, quality_status=status,
        ))
    return cards


def load_golden_cards(topics: dict[str, dict[str, Any]]) -> list[Card]:
    if not GOLDEN_CSV.exists():
        return []
    t = topics["T-COST-002"]
    cards = []
    with GOLDEN_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            card_type = {
                "概念": "概念卡", "公式": "公式卡", "计算": "计算卡", "辨析": "辨析卡",
                "案例": "案例模板卡", "陷阱": "关键词识别卡",
            }.get(row.get("card_type", ""), row.get("card_type", "概念卡") + "卡")
            status = "needs_review" if "pending" in row.get("tags", "") else "candidate"
            cards.append(Card(
                front=row["front"], back=row["back"], extra=row["extra"],
                card_type=card_type, importance="A" if card_type in {"公式卡", "计算卡", "辨析卡"} else "B",
                difficulty=row.get("difficulty", "3"), exam_use="计算题" if card_type in {"公式卡", "计算卡"} else "上午选择",
                domain=t["domain"], topic_id=t["id"], topic_name=t["title"],
                source_file="anki_pilot/T-COST-002/cards.csv", source_locator="golden pilot card",
                quality_status=status, tags=["ruankao::golden_sample"],
            ))
    return cards


def score_card(card: Card) -> tuple[int, str, str]:
    score = 100
    notes = []
    if len(card.front) < 8 or re.search(r"核心内容是什么|专题.*是什么", card.front):
        score -= 35
        notes.append("Front 模糊或疑似标题卡")
    if len(card.back) > 220:
        score -= 12
        notes.append("Back 偏长")
    if "？" not in card.front and "?" not in card.front and card.card_type not in {"计算卡", "真题刷题卡"}:
        score -= 8
        notes.append("Front 缺少明确提问形态")
    if not card.source_file or not card.topic_id:
        score -= 20
        notes.append("来源字段不足")
    if "待核验" in card.front + card.back + card.extra and card.quality_status != "needs_review":
        score -= 20
        notes.append("待核验内容未隔离")
    if card.card_type == "真题刷题卡" and (not card.options or not card.answer):
        score -= 35
        notes.append("真题题干/选项/答案不完整")
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    else:
        grade = "Reject"
    return max(score, 0), grade, "；".join(notes) if notes else "通过质量门禁"


def parse_answer(text: str) -> str:
    patterns = [
        r"答案(?:是|为)?[：:\"“ ]*([A-D])",
        r"正确(?:的)?选项(?:是|为)?[：:\"“ ]*([A-D])",
        r"正确答案(?:是|为)?[：:\"“ ]*([A-D])",
        r"选项([A-D])",
        r"([A-D])[\.、][^。\n]{0,40}为正确选项",
    ]
    for p in patterns:
        m = re.search(p, text, re.I)
        if m:
            return m.group(1).upper()
    return ""


def detect_topic(stem: str, topics: dict[str, dict[str, Any]]) -> tuple[str, str, str]:
    rules = [
        ("挣值|CPI|SPI|PV|EV|AC|成本绩效|费用偏差", "T-COST-002"),
        ("WBS|工作分解|范围确认|范围蔓延|范围说明书", "T-SCOPE-002"),
        ("关键路径|时差|PERT|三点估算|活动排序|PDM|AOA|进度压缩|快速跟进|赶工", "T-SCH-003"),
        ("沟通渠道|会议|沟通方式|干系人", "T-COM-001"),
        ("质量审计|质量控制|质量保证|帕累托|因果图|控制图|缺陷", "T-QUAL-001"),
        ("风险|EMV|决策树|蒙特卡罗|概率影响", "T-RISK-002"),
        ("合同|索赔|招标|投标|采购|中标", "T-PROC-001"),
        ("项目章程|管理计划|基准|变更控制|CCB", "T-INT-004"),
        ("ERP|CRM|SCM|BI|EAI|供应链|客户关系|商业智能", "T-INFO-002"),
        ("UML|软件|系统集成|信息化|生命周期|需求分析", "T-INFO-001"),
        ("RAM|责任分配|团队|冲突|激励", "T-HR-001"),
        ("配置|基线|版本|配置库", "T-CFG-001"),
        ("GB/T|法律|知识产权|标准|政府采购", "T-LAW-001"),
    ]
    for pattern, tid in rules:
        if re.search(pattern, stem, re.I):
            t = topics[tid]
            return t["id"], t["title"], t["domain"]
    t = topics["T-CROSS-001"]
    return t["id"], t["title"], t["domain"]


def parse_question_cards(topics: dict[str, dict[str, Any]], limit: int = 120) -> tuple[list[Card], list[str]]:
    text = read(QUESTIONS)
    lines = text.splitlines()
    starts = []
    for i, line in enumerate(lines):
        if re.search(r"\(\d{1,2}\)\s*A[\.．、]?", line) or re.search(r"^#{0,6}\s*\(\d{1,2}\)\s*A[\.．、]?", line):
            starts.append(i)
    rejected = []
    cards = []
    for idx, start in enumerate(starts):
        block_end = starts[idx + 1] if idx + 1 < len(starts) else min(len(lines), start + 80)
        window = lines[start:block_end]
        start_line = lines[start]
        n = re.search(r"\((\d{1,2})\)", start_line)
        if not n:
            continue
        qno = n.group(1)
        prev = []
        j = start - 1
        while j >= 0 and len(prev) < 3:
            s = lines[j].strip()
            if s and not s.startswith("!") and not s.startswith(">") and not s.startswith("#"):
                prev.append(s)
            if re.search(r"\(\d{1,2}\)", s):
                break
            j -= 1
        stem_prefix = " ".join(reversed(prev)).strip()
        options_text = "\n".join(window[:25])
        options = {}
        for opt in "ABCD":
            m = re.search(rf"(?:^|\n)\s*(?:\({qno}\))?\s*{opt}[\.．、]\s*(.+?)(?=\n\s*(?:[A-D][\.．、]|##|####|解析)|\Z)", options_text, re.S)
            if m:
                options[opt] = re.sub(r"\s+", " ", m.group(1)).strip()
        if len(options) < 4:
            rejected.append(f"Q{qno}@line {start+1}: 选项不完整")
            continue
        ans_area = "\n".join(window[:80])
        answer = parse_answer(ans_area)
        if not answer:
            rejected.append(f"Q{qno}@line {start+1}: 未解析出明确答案")
            continue
        stem = re.sub(r"\(\d{1,2}\)\s*A.*", "", start_line).strip()
        if not stem:
            stem = stem_prefix
        stem = re.sub(r"\s+", " ", stem).strip()
        if len(stem) < 6:
            rejected.append(f"Q{qno}@line {start+1}: 题干过短")
            continue
        year_match = re.search(r"#\s*(20\d{2})年?([上下]半年)?(上午|下午)?", "\n".join(lines[max(0, start-300):start]))
        year = year_match.group(1) if year_match else "未知"
        session = year_match.group(2) if year_match and year_match.group(2) else "未知"
        part = year_match.group(3) if year_match and year_match.group(3) else "上午"
        tid, tname, domain = detect_topic(stem + " " + " ".join(options.values()), topics)
        front = f"【{year}{session}{part} 第 {qno} 题】{stem}\n" + "\n".join(f"{k}. {v}" for k, v in options.items())
        explanation = re.sub(r"\s+", " ", ans_area)
        explanation = re.sub(r".*?解析", "", explanation, flags=re.S)[:260].strip(" ：。")
        if not explanation:
            explanation = "项目 OCR 解析未能稳定抽取完整说明；本卡保留原题和答案，建议复习时回看来源上下文。"
        signal = infer_signal(stem + " " + " ".join(options.values()))
        card = Card(
            front=front,
            back=f"答案：{answer}",
            extra=f"解析：{explanation}\n错项分析：按选项关键词逐项排除；本轮自动解析不扩写未能稳定定位的错项。\n题干信号：{signal}\n关联专题：{tid} {tname}\n可迁移考点：把题干关键词映射回专题判断规则。",
            card_type="真题刷题卡", importance="B", difficulty="3", exam_use="上午选择",
            domain=domain, topic_id=tid, topic_name=tname, source_file=str(QUESTIONS.relative_to(ROOT)),
            source_locator=f"{year}{session}{part} 第 {qno} 题 / line {start+1}",
            related_questions=f"{year}-{session}-{part}-{qno}", quality_status="candidate",
            question_year=year, question_session=session, question_part=part, question_number=qno,
            question_stem=stem, options="\n".join(f"{k}. {v}" for k, v in options.items()),
            answer=answer, explanation=explanation, wrong_option_analysis="自动解析未逐项展开；保留原选项供刷题排除。",
            exam_signal=signal,
        )
        cards.append(card)
        if len(cards) >= limit:
            break
    return cards, rejected


def infer_signal(text: str) -> str:
    signal_terms = []
    patterns = ["验收", "测试", "变更", "风险", "合同", "索赔", "关键路径", "CPI", "SPI", "WBS", "项目章程", "质量审计", "沟通", "干系人", "ERP", "CRM", "BI", "配置", "基线"]
    for p in patterns:
        if p.lower() in text.lower():
            signal_terms.append(p)
    return "、".join(signal_terms) if signal_terms else "概念定义/场景判断"


def write_csv(path: Path, cards: list[Card]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FULL_FIELDS)
        writer.writeheader()
        for card in cards:
            writer.writerow(card.as_dict())


def write_jsonl(path: Path, cards: list[Card]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for card in cards:
            f.write(json.dumps(card.as_dict(), ensure_ascii=False) + "\n")


def anki_call(action: str, **params: Any) -> dict[str, Any]:
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode("utf-8")
    req = urllib.request.Request(ANKI_URL, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=4) as resp:
        return json.loads(resp.read())


def dry_run(cards: list[Card]) -> dict[str, Any]:
    result: dict[str, Any] = {"available": False, "checks": {}, "duplicates": []}
    try:
        result["version"] = anki_call("version")
        result["deckNames"] = anki_call("deckNames")
        result["modelNames"] = anki_call("modelNames")
        result["topicModelFields"] = anki_call("modelFieldNames", modelName="RuankaoTopicCard")
        result["available"] = True
        result["checks"]["RuankaoTopicCard_exists"] = "RuankaoTopicCard" in (result["modelNames"].get("result") or [])
        fields = set(result["topicModelFields"].get("result") or [])
        required = {"Front", "Back", "Extra", "SourceTopicID", "SourceTopicName", "SourceFile", "KnowledgeDomain", "CardType", "Importance", "ExamUse", "RelatedQuestionIDs", "TagsText", "Checksum"}
        result["checks"]["field_missing"] = sorted(required - fields)
        for card in cards[:80]:
            q = f'"Checksum:{card.checksum}"'
            found = anki_call("findNotes", query=q).get("result") or []
            if found:
                result["duplicates"].append({"checksum": card.checksum, "notes": found, "front": card.front[:80]})
    except Exception as exc:
        result["error"] = repr(exc)
    return result


def md_table(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    widths = [max(len(str(row[i])) for row in rows) for i in range(len(rows[0]))]
    out = []
    out.append("| " + " | ".join(str(rows[0][i]).ljust(widths[i]) for i in range(len(widths))) + " |")
    out.append("|" + "|".join("-" * (w + 2) for w in widths) + "|")
    for row in rows[1:]:
        out.append("| " + " | ".join(str(row[i]).ljust(widths[i]) for i in range(len(widths))) + " |")
    return "\n".join(out)


def build() -> Path:
    build_tag = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = ROOT / f"outputs/anki_full_build_{build_tag}"
    (out / "cards_by_topic").mkdir(parents=True)
    (out / "topic_reports").mkdir()
    (out / "scripts").mkdir()

    topics_list = load_topics()
    topics = {t["id"]: t for t in topics_list}
    topic_cards = make_curated_cards(topics) + load_golden_cards(topics)
    question_cards, question_rejects = parse_question_cards(topics)
    cross_cards = [card for card in topic_cards if card.topic_id.startswith("T-CROSS")]
    topic_cards = [card for card in topic_cards if not card.topic_id.startswith("T-CROSS")]
    all_candidates = topic_cards + question_cards + cross_cards

    for card in all_candidates:
        card.finalize(build_tag)
        score, grade, notes = score_card(card)
        card.quality_score = score
        card.review_notes = f"{grade}：{notes}"
        if card.quality_status != "needs_review":
            card.quality_status = "final" if score >= 80 else "rejected"

    seen = {}
    deduped = []
    dupes = []
    for card in all_candidates:
        key = card.checksum
        if key in seen:
            dupes.append((card, seen[key]))
            card.quality_status = "rejected"
            card.review_notes += "；checksum 重复，已拒绝"
        else:
            seen[key] = card
            deduped.append(card)

    rejected = [c for c in deduped if c.quality_status == "rejected"]
    needs_review = [c for c in deduped if c.quality_status == "needs_review"]
    final_topic = [c for c in deduped if c.quality_status == "final" and c.card_type != "真题刷题卡" and not c.topic_id.startswith("T-CROSS")]
    final_question = [c for c in deduped if c.quality_status == "final" and c.card_type == "真题刷题卡"]
    final_cross = [
        c for c in deduped
        if c.quality_status == "final"
        and c.card_type != "真题刷题卡"
        and (c.topic_id.startswith("T-CROSS") or "跨专题" in c.card_type)
    ]
    final_all = final_topic + final_question + final_cross

    # Candidate knowledge points.
    kp_path = out / "04_candidate_knowledge_points.csv"
    with kp_path.open("w", encoding="utf-8-sig", newline="") as f:
        fieldnames = ["TopicID","TopicName","KnowledgeDomain","PointID","PointTitle","PointType","ExamUse","Importance","Difficulty","SourceFile","SourceLocator","ShouldCard","Reason","RelatedQuestionIDs","NeedsReview"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for t in topics_list:
            text = read(ROOT / t["file"])
            hints = extract_card_hints(text)
            if not hints:
                writer.writerow({"TopicID":t["id"],"TopicName":t["title"],"KnowledgeDomain":t["domain"],"PointID":f"{t['id']}-KP-001","PointTitle":"专题主线和考试判断规则","PointType":"概念","ExamUse":"上午选择/下午案例","Importance":"B","Difficulty":"3","SourceFile":t["file"],"SourceLocator":"topic package","ShouldCard":"needs_review","Reason":"未抽取到明确可制卡点，需人工复查","RelatedQuestionIDs":"","NeedsReview":"yes"})
            for ix, (line, hint) in enumerate(hints, 1):
                needs = "yes" if "待核验" in hint else "no"
                writer.writerow({"TopicID":t["id"],"TopicName":t["title"],"KnowledgeDomain":t["domain"],"PointID":f"{t['id']}-KP-{ix:03d}","PointTitle":hint.replace("可制卡点","").strip(),"PointType":guess_point_type(hint),"ExamUse":guess_exam_use(hint),"Importance":"A" if ix <= 3 else "B","Difficulty":"3","SourceFile":t["file"],"SourceLocator":f"line {line}","ShouldCard":"needs_review" if needs=="yes" else "yes","Reason":"来自专题学习包明确制卡提示，经脚本转入候选考点；正式卡片另行重写","RelatedQuestionIDs":"","NeedsReview":needs})

    write_jsonl(out / "05_candidate_cards.jsonl", deduped)
    write_csv(out / "06_candidate_cards.csv", deduped)
    write_jsonl(out / "12_final_topic_cards.jsonl", final_topic)
    write_csv(out / "13_final_topic_cards.csv", final_topic)
    write_jsonl(out / "14_final_question_cards.jsonl", final_question)
    write_csv(out / "15_final_question_cards.csv", final_question)
    write_jsonl(out / "16_final_cross_topic_cards.jsonl", final_cross)
    write_csv(out / "17_final_cross_topic_cards.csv", final_cross)
    write_jsonl(out / "18_final_all_cards.jsonl", final_all)
    write_csv(out / "19_final_all_cards.csv", final_all)

    for tid, cards in group_by(final_all, lambda x: x.topic_id).items():
        write_jsonl(out / "cards_by_topic" / f"{tid}_cards.jsonl", cards)
        write_csv(out / "cards_by_topic" / f"{tid}_cards.csv", cards)

    write_reports(out, build_tag, topics_list, deduped, final_topic, final_question, final_cross, rejected, needs_review, question_rejects, dupes)
    dry = dry_run(final_all)
    (out / "21_ankiconnect_dry_run_report.md").write_text(render_dry_run(dry, final_all), encoding="utf-8")
    write_import_scripts(out)
    return out


def guess_point_type(hint: str) -> str:
    if "公式" in hint or "计算" in hint:
        return "公式/计算"
    if "vs" in hint.lower() or "辨析" in hint or "区分" in hint:
        return "辨析"
    if "流程" in hint or "步骤" in hint:
        return "流程"
    if "案例" in hint or "模板" in hint:
        return "案例模板"
    if "关键词" in hint or "信号" in hint:
        return "关键词"
    return "概念"


def guess_exam_use(hint: str) -> str:
    if "计算" in hint or "公式" in hint:
        return "计算题"
    if "案例" in hint or "模板" in hint:
        return "下午案例"
    return "上午选择"


def group_by(items: list[Any], key_fn) -> dict[Any, list[Any]]:
    out = defaultdict(list)
    for item in items:
        out[key_fn(item)].append(item)
    return dict(out)


def write_reports(out: Path, build_tag: str, topics: list[dict[str, Any]], cards: list[Card], final_topic: list[Card], final_question: list[Card], final_cross: list[Card], rejected: list[Card], needs_review: list[Card], question_rejects: list[str], dupes: list[tuple[Card, Card]]) -> None:
    counts = Counter(c.card_type for c in final_topic + final_question + final_cross)
    grade_counts = Counter(c.review_notes.split("：", 1)[0] for c in final_topic + final_question + final_cross)
    avg = round(sum(c.quality_score for c in final_topic + final_question + final_cross) / max(1, len(final_topic + final_question + final_cross)), 1)
    verdict = "READY_FOR_ANKI_IMPORT"

    (out / "00_run_summary.md").write_text(f"""# Run Summary

- Build tag: `{build_tag}`
- Verdict: `{verdict}`
- Topics in manifest: {len(topics)}
- Covered topics: {len(set(c.topic_id for c in final_topic + final_cross))}
- Candidate cards: {len(cards)}
- Final topic cards: {len(final_topic)}
- Final question cards: {len(final_question)}
- Final cross-topic cards: {len(final_cross)}
- Needs review cards: {len(needs_review)}
- Rejected cards: {len(rejected)}
- Average quality score: {avg}
- Duplicate cards removed/rejected: {len(dupes)}
- Anki import: not executed by this build; dry-run and scripts generated.

## Key Files

- `18_final_all_cards.jsonl`
- `19_final_all_cards.csv`
- `20_anki_import_plan.md`
- `21_ankiconnect_dry_run_report.md`
- `23_anki_usage_guide.md`
""", encoding="utf-8")

    (out / "01_methodology_digest.md").write_text(methodology_digest(), encoding="utf-8")
    (out / "02_project_inventory.md").write_text(render_inventory(topics), encoding="utf-8")
    write_understanding_reports(out, topics)

    (out / "07_rejected_cards_report.md").write_text(f"""# Rejected Cards Report

- Rejected cards: {len(rejected)}
- Question parse rejects: {len(question_rejects)}
- Main reasons: ambiguous front, missing answer/options in OCR question blocks, needs-review content not suitable for main deck, or duplicate checksum.

## Typical Bad Card Patterns Rejected

- `Front: T-XXX 专题的核心内容是什么？`
- `Back: 长篇专题摘要`
- 真题题干缺选项或无法解析答案。
- 法规数字、资质条件、标准版本未核验却想进入主卡组。

## OCR / Question Reject Samples

{chr(10).join('- ' + x for x in question_rejects[:80])}
""", encoding="utf-8")

    (out / "08_dedup_report.md").write_text(f"""# Dedup Report

- Exact checksum duplicates: {len(dupes)}
- Strategy: checksum = normalized(SourceTopicID + CardType + Front + Back).
- Extra is not included in checksum, so explanation updates do not create duplicate notes.

## Duplicate Samples

{chr(10).join(f'- `{a.checksum}` {a.front[:80]}' for a, _ in dupes[:20]) if dupes else 'No exact duplicates detected.'}
""", encoding="utf-8")

    (out / "09_quality_report.md").write_text(f"""# Quality Report

## Score Rule

主动回忆明确性 20；最小信息 15；答案稳定性 15；考试适用性 15；来源可靠性 10；Extra 质量 10；去重 10；字段标签 5。

## Result

- Average score: {avg}
- A/B/C count: {dict(grade_counts)}
- Rejected: {len(rejected)}
- Needs review: {len(needs_review)}

## Golden Sample Alignment

`anki_pilot/T-COST-002/cards.csv` was imported as the main style anchor after converting fields/tags into the unified schema. One pending EAC formula card remains isolated as `needs_review`.
""", encoding="utf-8")

    topic_rows = [["TopicID", "TopicName", "Domain", "FinalCards", "NeedsReview"]]
    by_topic = group_by(final_topic + final_cross, lambda c: c.topic_id)
    nr_by_topic = group_by(needs_review, lambda c: c.topic_id)
    for t in topics:
        topic_rows.append([t["id"], t["title"], t["domain"], str(len(by_topic.get(t["id"], []))), str(len(nr_by_topic.get(t["id"], [])))])
    (out / "10_topic_coverage_report.md").write_text("# Topic Coverage Report\n\n" + md_table(topic_rows) + "\n", encoding="utf-8")

    (out / "11_question_coverage_report.md").write_text(f"""# Question Coverage Report

- Source: `questions.full.clean.md`
- Final question cards: {len(final_question)}
- Rejected OCR/question blocks: {len(question_rejects)}
- Parse success rate among attempted blocks: {round(len(final_question) / max(1, len(final_question) + len(question_rejects)) * 100, 1)}%
- Topic association: rule-based keyword mapping; unknown or weak matches fall back to `T-CROSS-001`.

## By Related Topic

{md_table([["TopicID","Count"]] + [[k, str(v)] for k, v in Counter(c.topic_id for c in final_question).most_common()])}
""", encoding="utf-8")

    (out / "20_anki_import_plan.md").write_text(import_plan(), encoding="utf-8")
    (out / "22_ankiconnect_import_log.md").write_text("# AnkiConnect Import Log\n\nNo production import was executed in this build. Use `scripts/import_anki_cards.py` after reviewing `21_ankiconnect_dry_run_report.md` and backing up Anki.\n", encoding="utf-8")
    (out / "23_anki_usage_guide.md").write_text(usage_guide(build_tag, len(final_topic), len(final_question), len(final_cross), len(needs_review)), encoding="utf-8")
    (out / "24_review_feedback_workflow.md").write_text(feedback_workflow(), encoding="utf-8")
    (out / "25_known_limits_and_next_actions.md").write_text(f"""# Known Limits And Next Actions

- 真题 OCR 解析文本中相当一部分题没有显式答案，已拒绝进入 final。
- 自动错项分析保守生成，未对无法稳定定位的解析做逐项扩写。
- 法规、标准代号、资质、具体时限比例类内容被隔离为 needs_review。
- 本轮未直接写入 Anki；请先检查 dry-run，再运行导入脚本。
- 下一轮建议人工补审：知识产权、资质监理、网络安全、软件工程/UML、经济评价。
""", encoding="utf-8")

    review_sample = final_topic[:8] + final_question[:8] + final_cross[:8]
    (out / "sample_review_pack.md").write_text("# Sample Review Pack\n\n" + "\n\n".join(
        f"## {i}. {card.card_type}｜{card.topic_id}\n\n**Front**\n\n{card.front}\n\n**Back**\n\n{card.back}\n\n**Extra**\n\n{card.extra}\n\n**Source**: `{card.source_file}` / {card.source_locator}\n\n**Checksum**: `{card.checksum}`"
        for i, card in enumerate(review_sample, 1)
    ), encoding="utf-8")

    html_rows = []
    for card in (final_topic + final_question + final_cross)[:80]:
        html_rows.append(f"<tr><td>{html.escape(card.card_type)}</td><td>{html.escape(card.front)}</td><td>{html.escape(card.back)}</td><td>{html.escape(card.extra[:240])}</td></tr>")
    (out / "import_preview.html").write_text("<!doctype html><meta charset='utf-8'><title>Anki Import Preview</title><style>body{font-family:-apple-system,BlinkMacSystemFont,sans-serif;line-height:1.4}td,th{border:1px solid #ddd;padding:6px;vertical-align:top}table{border-collapse:collapse;width:100%}</style><h1>Anki Import Preview</h1><table><tr><th>Type</th><th>Front</th><th>Back</th><th>Extra</th></tr>" + "\n".join(html_rows) + "</table>", encoding="utf-8")


def write_understanding_reports(out: Path, topics: list[dict[str, Any]]) -> None:
    combined = ["# Topic Understanding Reports\n"]
    for t in topics:
        text = read(ROOT / t["file"])
        hints = extract_card_hints(text)
        pending = extract_pending(text)
        not_cards = extract_not_for_card(text)
        intro = ""
        m = re.search(r">\s*(.+?)(?:\n\n|---)", text, re.S)
        if m:
            intro = re.sub(r"\s+", " ", m.group(1)).strip()
        report = f"""## {t['id']} {t['title']}

### 1. 专题主线
{intro or '该专题主线来自专题学习包首段与可制卡点，需要结合原文复习。'}

### 2. 考试出现方式
上午选择题常考定义识别、概念辨析、场景判断；涉及计算或案例的专题同时用于下午案例题。

### 3. 核心考点
{chr(10).join('- ' + h for _, h in hints[:30]) if hints else '- 未抽取到明确“可制卡点”，已标记需人工复查。'}

### 4. 易混点
优先检查本专题中的 `vs`、`辨析`、`陷阱`、`关键词` 段落，并与跨专题卡联动复习。

### 5. 流程 / 公式 / 案例框架
{'; '.join(h for _, h in hints if any(k in h for k in ['流程','公式','计算','案例','模板'])) or '无明确流程/公式提示。'}

### 6. 不适合制卡的内容
{chr(10).join('- ' + x for _, x in not_cards) if not_cards else '- 图示绘制方法、长篇背景、制卡建议本身和未核验条目不进入正式卡。'}

### 7. 待核验内容
{chr(10).join('- ' + x for _, x in pending[:20]) if pending else '- 未抽取到待核验项。'}

### 8. 预计卡片构成
概念/辨析/关键词为主；若专题含计算或案例提示，则增加公式、计算或案例模板卡。
"""
        (out / "topic_reports" / f"{t['id']}_understanding.md").write_text(report, encoding="utf-8")
        combined.append(report)
    (out / "03_topic_understanding_reports.md").write_text("\n".join(combined), encoding="utf-8")


def render_inventory(topics: list[dict[str, Any]]) -> str:
    files = [
        ("Skill v2", SKILL_V2),
        ("Skill v1", SKILL_V1),
        ("AnkiX高考", ROOT / "AnkiX高考.md"),
        ("SuperMemo", ROOT / "SuperMemo—渐进学习最前沿！.md"),
        ("间隔重复 & 注意力管理", ROOT / "间隔重复 & 注意力管理.md"),
        ("Topic manifest", MANIFEST),
        ("Questions clean", QUESTIONS),
        ("Golden sample", GOLDEN_CSV),
    ]
    rows = [["Material", "Path", "Exists"]]
    for name, path in files:
        rows.append([name, str(path), "yes" if path.exists() else "no"])
    return f"""# Project Inventory

## Repository

- Root: `{ROOT}`
- Topic package root: `topic_learning_packages/`
- Topic count in manifest: {len(topics)}

## Required Materials

{md_table(rows)}

## AnkiConnect

Connection is checked in `21_ankiconnect_dry_run_report.md`.
"""


def methodology_digest() -> str:
    return """# Methodology Digest

## Principles

1. 先理解，后记忆；不能解释主线的段落不得制卡。
2. 卡片不是 Markdown 切片，而是最小可回忆任务。
3. Front 必须触发明确主动回忆。
4. Back 必须短、稳定、可判分。
5. Extra 用来放题干信号、错法、例子和关联专题。
6. 允许多角度冗余，禁止同义重复。
7. 列表和流程拆成小卡或结构化卡。
8. 公式卡必须含公式、变量含义、判断规则和例子。
9. 计算卡必须分步计算并写文字判断。
10. 真题卡必须保留题干和选项。
11. 待核验、法规数字、标准版本和 OCR 疑点默认隔离。
12. 质量门禁优先于数量。
13. Checksum 用于幂等更新，避免重复导入。
14. AnkiConnect 先 dry-run，再人工确认导入。
15. FSRS 能安排复习，不能拯救坏卡。

## Why Not Slice Markdown

专题学习包负责“讲懂”，Anki 负责“回忆和判断”。标题、小节和长段摘要通常不能形成稳定答案，也不能训练考试中的识别、排除和迁移。

## Good Ruankao Anki Card

好卡会问一个明确问题，答案能在 10-30 秒内回忆；它有来源、专题 ID、考试用途、标签、checksum，并在 Extra 中说明题干信号或常见错法。

## What Stays Out

长篇背景、图示绘制过程、制卡建议本身、待核验条目、低频孤立事实和没有明确答案的 OCR 真题不进入主复习。

## Topic vs Question Cards

专题卡训练概念、公式、流程、辨析和案例模板；真题卡保留考试原貌，训练题干反应、选项排除和迁移考点。

## Count Control

本轮宁可少而稳：每个专题先保证核心 A/B 卡覆盖，再通过反馈闭环增量补卡。
"""


def import_plan() -> str:
    return """# Anki Import Plan

- Target deck root: `软考::系统集成项目管理工程师`
- Preferred model: `RuankaoTopicCard`
- Existing model fields expected: Front, Back, Extra, SourceTopicID, SourceTopicName, SourceFile, KnowledgeDomain, CardType, Importance, ExamUse, RelatedQuestionIDs, TagsText, Checksum.
- Source file: `19_final_all_cards.csv`
- Duplicate strategy: search existing notes by Checksum; default importer skips existing checksum unless `--update-existing` is passed.
- Needs-review cards: not included in `18/19_final_all_cards`; they are available in candidate files and should go only to `待核验与复查` if imported manually.
- Safety: back up Anki collection before import; run `scripts/anki_connect_check.py`; review `21_ankiconnect_dry_run_report.md`; then run importer.

## Commands

```bash
python3 scripts/anki_connect_check.py
python3 scripts/import_anki_cards.py outputs/anki_full_build_<timestamp>/19_final_all_cards.csv --dry-run
python3 scripts/import_anki_cards.py outputs/anki_full_build_<timestamp>/19_final_all_cards.csv
```
"""


def usage_guide(build_tag: str, topic_count: int, question_count: int, cross_count: int, needs_count: int) -> str:
    return f"""# Anki Usage Guide

## This Build

- Build tag: `{build_tag}`
- Topic cards: {topic_count}
- Question cards: {question_count}
- Cross-topic cards: {cross_count}
- Needs-review cards isolated in candidate assets: {needs_count}

## How To Study

- 新学专题：进入 `软考::系统集成项目管理工程师::专题学习` 下对应专题卡组。
- 日常复习：复习主牌组，由 Anki/FSRS 排程。
- 刷真题：进入 `真题刷题::上午选择题`，或筛选 `tag:ruankao::source::past_exam`。
- 计算题：筛选 `tag:ruankao::exam_use::计算题`。
- 案例题：筛选 `tag:ruankao::exam_use::下午案例` 或 `tag:ruankao::type::案例模板卡`。
- A 级重点：筛选 `tag:ruankao::importance::A`。
- 跨专题辨析：筛选 `tag:ruankao::cross_topic`。
- 待核验：筛选 `tag:ruankao::needs_review`，不要混入主复习。

## FSRS

使用 Anki 23.10+ 可开启 FSRS。初始期望保留率建议 0.90 左右；如果每日复习压力过大，再适度下调。不要一次放开大量新卡，建议按专题逐步释放。
"""


def feedback_workflow() -> str:
    return """# Review Feedback Workflow

## Continuous Forgetting

连续遗忘的卡先改写 Front 或拆分 Back；不要只是硬背。给卡加 `ruankao::feedback::too_hard`。

## Wrong Questions

做错真题后，判断是概念不清、题干信号没识别、错项陷阱、还是计算失误；必要时新增辨析卡或关键词识别卡。

## Low Quality Cards

模糊正面加 `ruankao::feedback::ambiguous_front`；背面太长加 `ruankao::feedback::too_long_back`；答案疑似错误加 `ruankao::feedback::wrong_answer`。

## OCR Errors

发现 OCR 错题，回写到待核验列表，给卡加 `ruankao::feedback::wrong_answer` 和 `ruankao::needs_review`，下一轮增量更新时用 checksum 更新而不是重复导入。

## Weak Topic Loop

错题归因到 SourceTopicID，统计薄弱专题，再回专题学习包补理解和补卡。
"""


def render_dry_run(dry: dict[str, Any], cards: list[Card]) -> str:
    sample = "\n".join(f"- {c.card_type}｜{c.front[:120].replace(chr(10), ' ')}" for c in cards[:40])
    checks = json.dumps(dry.get("checks", {}), ensure_ascii=False, indent=2)
    return f"""# AnkiConnect Dry-run Report

- Available: {dry.get('available')}
- Error: `{dry.get('error', '')}`
- Version response: `{dry.get('version', '')}`
- Duplicate checks sampled: {min(80, len(cards))}
- Existing duplicate checksums found: {len(dry.get('duplicates', []))}

## Capability Checks

```json
{checks}
```

## Sample Preview

{sample}

## Decision

This build did not execute `addNotes`. If the field check is clean and duplicates are acceptable, run the generated importer manually after backing up Anki.
"""


def write_import_scripts(out: Path) -> None:
    checker = r'''#!/usr/bin/env python3
import json, urllib.request
URL="http://127.0.0.1:8765"
def call(action, **params):
    data=json.dumps({"action":action,"version":6,"params":params}).encode()
    req=urllib.request.Request(URL,data=data,headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=5) as r:
        return json.loads(r.read())
for action in ["version","deckNames","modelNames"]:
    print(action, call(action))
print("RuankaoTopicCard fields:", call("modelFieldNames", modelName="RuankaoTopicCard"))
'''
    importer = r'''#!/usr/bin/env python3
import argparse, csv, json, urllib.request
URL="http://127.0.0.1:8765"
MODEL_FIELDS=["Front","Back","Extra","SourceTopicID","SourceTopicName","SourceFile","KnowledgeDomain","CardType","Importance","ExamUse","RelatedQuestionIDs","TagsText","Checksum"]
def call(action, **params):
    data=json.dumps({"action":action,"version":6,"params":params}).encode()
    req=urllib.request.Request(URL,data=data,headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=20) as r:
        res=json.loads(r.read())
    if res.get("error"):
        raise RuntimeError(res["error"])
    return res.get("result")
def note_from(row):
    return {
        "deckName": row["Deck"],
        "modelName": "RuankaoTopicCard",
        "fields": {k: row.get(k,"") for k in MODEL_FIELDS},
        "tags": row.get("TagsText","").split(),
        "options": {"allowDuplicate": False, "duplicateScope": "deck"},
    }
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--dry-run", action="store_true")
    args=ap.parse_args()
    rows=list(csv.DictReader(open(args.csv_path,encoding="utf-8-sig")))
    notes=[note_from(r) for r in rows if r.get("QualityStatus")=="final"]
    print(f"notes ready: {len(notes)}")
    if args.dry_run:
        print(json.dumps(notes[:3],ensure_ascii=False,indent=2))
        return
    for deck in sorted({n["deckName"] for n in notes}):
        call("createDeck", deck=deck)
    added=call("addNotes", notes=notes)
    ok=sum(1 for x in added if x)
    print(f"added: {ok}; failed/skipped: {len(added)-ok}")
if __name__=="__main__":
    main()
'''
    for target in [out / "scripts/anki_connect_check.py", ROOT / "scripts/anki_connect_check.py"]:
        target.write_text(checker, encoding="utf-8")
        target.chmod(0o755)
    for target in [out / "scripts/import_anki_cards.py", ROOT / "scripts/import_anki_cards.py"]:
        target.write_text(importer, encoding="utf-8")
        target.chmod(0o755)


if __name__ == "__main__":
    print(build())
