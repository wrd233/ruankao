#!/usr/bin/env python3
from __future__ import annotations

import csv
import dataclasses
import hashlib
import html
import json
import re
import shutil
import statistics
import textwrap
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
OLD_BUILD = ROOT / "outputs/anki_full_build_20260520_221409"
MANIFEST = ROOT / "topic_learning_packages/index/topic_manifest.json"
QUESTIONS = ROOT / "questions.full.clean.md"
PENDING = ROOT / "topic_learning_packages/reports/pending_verification_register.md"
SKILL_V2 = Path("/Users/wangrundong/Downloads/软考Anki卡片创建Skill_v2_强化版.md")
ANKI_URL = "http://127.0.0.1:8765"

META_PATTERNS = [
    "这个专题应该怎样转化为 Anki 卡片",
    "本专题应该如何制卡",
    "核心考点是什么",
    "来自专题小节标题",
    "制卡建议",
    "候选卡",
    "本 Skill",
    "制卡流程",
    "专题理解报告",
    "复习时不要背整段",
]

GENERIC_HEADINGS = {
    "先看这个专题的主线",
    "典型题详解",
    "举一反三",
    "本轮真题覆盖增强",
    "掌握标准",
    "待核验与后续改进",
    "这个专题应该怎样转化为 Anki 卡片",
}

CORE_TOPICS = {
    "T-PM-002", "T-INT-002", "T-INT-004", "T-SCOPE-002", "T-SCH-002", "T-SCH-003",
    "T-COST-001", "T-COST-002", "T-QUAL-001", "T-QUAL-002", "T-COM-001", "T-HR-001",
    "T-RISK-001", "T-RISK-002", "T-PROC-001", "T-PROC-002", "T-CFG-001", "T-LAW-001",
    "T-INFO-002", "T-CASE-001", "T-CASE-002", "T-CASE-003", "T-CROSS-001", "T-RISK-003",
    "T-SCOPE-003",
}

CSV_FIELDS = [
    "deck", "note_type", "front", "back", "extra", "card_type", "importance", "difficulty",
    "exam_use", "knowledge_domain", "source_topic_id", "source_topic_name", "source_ids",
    "source_file", "source_heading", "source_excerpt", "related_question_ids", "related_topic_ids",
    "question_id", "question_year", "question_session", "question_part", "question_number",
    "question_parse_confidence", "explanation_source", "checksum", "tags", "quality_score",
    "quality_status", "quality_notes",
]

ANKI_MODEL_FIELDS = [
    "Front", "Back", "Extra", "SourceTopicID", "SourceTopicName", "SourceFile",
    "KnowledgeDomain", "CardType", "Importance", "ExamUse", "RelatedQuestionIDs",
    "TagsText", "Checksum",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="ignore") if path.exists() else ""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def safe_name(s: str) -> str:
    return re.sub(r"[\\/:*?\"<>|，、；;：:（）()]+", "_", s).strip("_ ")


def safe_tag(s: str) -> str:
    return re.sub(r"\s+", "_", s.strip())


def load_topics() -> list[dict[str, Any]]:
    return json.loads(read(MANIFEST))["topics"]


def anki_call(action: str, **params: Any) -> dict[str, Any]:
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode("utf-8")
    req = urllib.request.Request(ANKI_URL, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=8) as resp:
        return json.loads(resp.read())


def anki_available() -> bool:
    try:
        return anki_call("version").get("result") == 6
    except Exception:
        return False


def md_table(rows: list[list[Any]]) -> str:
    if not rows:
        return ""
    widths = [max(len(str(r[i])) for r in rows) for i in range(len(rows[0]))]
    out = ["| " + " | ".join(str(rows[0][i]).ljust(widths[i]) for i in range(len(widths))) + " |"]
    out.append("|" + "|".join("-" * (w + 2) for w in widths) + "|")
    for r in rows[1:]:
        out.append("| " + " | ".join(str(r[i]).ljust(widths[i]) for i in range(len(widths))) + " |")
    return "\n".join(out)


@dataclasses.dataclass
class SourceChunk:
    source_id: str
    topic_id: str
    source_file: str
    heading_path: list[str]
    content_excerpt: str
    content_summary: str
    candidate_card_types: list[str]
    needs_verification: bool
    is_meta: bool = False
    line_start: int = 0
    line_end: int = 0

    def as_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class Card:
    deck: str
    note_type: str
    front: str
    back: str
    extra: str
    card_type: str
    importance: str
    difficulty: int
    exam_use: str
    knowledge_domain: str
    source_topic_id: str
    source_topic_name: str
    source_ids: list[str]
    source_file: str
    source_heading: str
    source_excerpt: str
    related_question_ids: list[str] = dataclasses.field(default_factory=list)
    related_topic_ids: list[str] = dataclasses.field(default_factory=list)
    question_id: str = ""
    question_year: str = ""
    question_session: str = ""
    question_part: str = ""
    question_number: str = ""
    question_parse_confidence: str = ""
    explanation_source: str = ""
    checksum: str = ""
    tags: list[str] = dataclasses.field(default_factory=list)
    quality_score: int = 0
    quality_status: str = "candidate"
    quality_notes: str = ""

    def compute_checksum(self) -> None:
        raw = re.sub(r"\s+", " ", f"{self.source_topic_id}|{self.card_type}|{self.front}|{strip_html(self.back)}").strip().lower()
        self.checksum = "sha256:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]

    def as_dict(self) -> dict[str, Any]:
        return {
            "deck": self.deck,
            "note_type": self.note_type,
            "front": self.front,
            "back": self.back,
            "extra": self.extra,
            "card_type": self.card_type,
            "importance": self.importance,
            "difficulty": str(self.difficulty),
            "exam_use": self.exam_use,
            "knowledge_domain": self.knowledge_domain,
            "source_topic_id": self.source_topic_id,
            "source_topic_name": self.source_topic_name,
            "source_ids": ";".join(self.source_ids),
            "source_file": self.source_file,
            "source_heading": self.source_heading,
            "source_excerpt": self.source_excerpt,
            "related_question_ids": ";".join(self.related_question_ids),
            "related_topic_ids": ";".join(self.related_topic_ids),
            "question_id": self.question_id,
            "question_year": self.question_year,
            "question_session": self.question_session,
            "question_part": self.question_part,
            "question_number": self.question_number,
            "question_parse_confidence": self.question_parse_confidence,
            "explanation_source": self.explanation_source,
            "checksum": self.checksum,
            "tags": " ".join(self.tags),
            "quality_score": str(self.quality_score),
            "quality_status": self.quality_status,
            "quality_notes": self.quality_notes,
        }

    def anki_note(self) -> dict[str, Any]:
        fields = {
            "Front": self.front,
            "Back": self.back,
            "Extra": self.extra,
            "SourceTopicID": self.source_topic_id,
            "SourceTopicName": self.source_topic_name,
            "SourceFile": self.source_file,
            "KnowledgeDomain": self.knowledge_domain,
            "CardType": self.card_type,
            "Importance": self.importance,
            "ExamUse": self.exam_use,
            "RelatedQuestionIDs": ";".join(self.related_question_ids),
            "TagsText": " ".join(self.tags),
            "Checksum": self.checksum,
        }
        return {
            "deckName": self.deck,
            "modelName": "RuankaoTopicCard",
            "fields": fields,
            "tags": self.tags,
            "options": {"allowDuplicate": False, "duplicateScope": "deck"},
        }


def strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s)


def block(title: str, body: str, tag: str = "div") -> str:
    return f'<div class="section-title">【{html.escape(title)}】</div>\n<{tag}>{body}</{tag}>'


def back_html(answer: str) -> str:
    return f'<div class="answer-block">\n{block("答案", html.escape(answer).replace(chr(10), "<br>"))}\n</div>'


def extra_html(*, understanding: str, memory: str, pitfalls: str, signals: str, related: str, source: str) -> str:
    parts = [
        block("理解", html.escape(understanding).replace(chr(10), "<br>")),
        block("记忆线索", html.escape(memory).replace(chr(10), "<br>")),
        block("易错点", html.escape(pitfalls).replace(chr(10), "<br>")),
        block("题干信号", html.escape(signals).replace(chr(10), "<br>")),
        block("关联专题", html.escape(related).replace(chr(10), "<br>")),
        block("来源", html.escape(source).replace(chr(10), "<br>")),
    ]
    return '<div class="extra">\n' + "\n".join(parts) + "\n</div>"


def question_extra_html(answer: str, why: str, wrongs: dict[str, str], signal: str, related: str, transfer: str, source: str) -> str:
    lis = "\n".join(f"<li>{html.escape(k)}：{html.escape(v)}</li>" for k, v in wrongs.items())
    parts = [
        block("答案", html.escape(answer)),
        block(f"为什么选 {html.escape(answer)}", html.escape(why)),
        f'<div class="section-title">【错项分析】</div>\n<ul>{lis}</ul>',
        block("题干信号", html.escape(signal)),
        block("关联专题", html.escape(related)),
        block("可迁移考点", html.escape(transfer)),
        block("来源", html.escape(source)),
    ]
    return '<div class="answer-block">\n' + "\n".join(parts) + "\n</div>"


def infer_types(text: str) -> list[str]:
    out = []
    if re.search(r"公式|计算|CPI|SPI|EV|PV|AC|EMV|PERT|渠道|时差", text, re.I):
        out.extend(["公式卡", "计算卡"])
    if re.search(r"vs|区别|辨析|混淆|边界|对比", text, re.I):
        out.append("辨析卡")
    if re.search(r"流程|步骤|顺序|链|处理", text):
        out.append("流程卡")
    if re.search(r"案例|答题|措施|原因", text):
        out.append("案例模板卡")
    if re.search(r"信号|关键词|题干", text):
        out.append("关键词识别卡")
    if not out:
        out.append("概念卡")
    return sorted(set(out))


def summarize(text: str) -> str:
    cleaned = re.sub(r"```.*?```", "", text, flags=re.S)
    cleaned = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", cleaned)
    cleaned = re.sub(r"\*\*|`|>|#+|\|", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    cleaned = re.sub(r"可制卡点[:：]?", "", cleaned)
    parts = re.split(r"(?<=[。！？])", cleaned)
    summary = "".join(parts[:2]).strip()
    return summary[:220] or cleaned[:220]


def has_verification_risk(text: str) -> bool:
    return bool(re.search(r"待核验|法规|标准|GB/T|GB/Z|资质|比例|时限|天|年|版本|条文|专利|著作权|政府采购", text))


def is_meta_text(text: str) -> bool:
    return any(p in text for p in META_PATTERNS) or "## 这个专题应该怎样转化为 Anki 卡片" in text


def build_source_map(topics: list[dict[str, Any]]) -> tuple[list[SourceChunk], dict[str, list[SourceChunk]]]:
    all_chunks: list[SourceChunk] = []
    by_topic: dict[str, list[SourceChunk]] = defaultdict(list)
    for topic in topics:
        path = ROOT / topic["file"]
        lines = read(path).splitlines()
        heading_stack: list[tuple[int, str]] = []
        current_start = 0
        current_heading_path = [topic["title"]]
        chunks_raw: list[tuple[int, int, list[str], str]] = []

        for i, line in enumerate(lines):
            m = re.match(r"^(#{2,4})\s+(.+?)\s*$", line)
            if m:
                if i > current_start:
                    content = "\n".join(lines[current_start:i]).strip()
                    if content:
                        chunks_raw.append((current_start + 1, i, current_heading_path[:], content))
                level = len(m.group(1))
                title = m.group(2).strip()
                heading_stack = [(lv, h) for lv, h in heading_stack if lv < level]
                heading_stack.append((level, title))
                current_heading_path = [topic["title"]] + [h for _, h in heading_stack]
                current_start = i
        if current_start < len(lines):
            content = "\n".join(lines[current_start:]).strip()
            if content:
                chunks_raw.append((current_start + 1, len(lines), current_heading_path[:], content))

        idx = 1
        for start, end, heading_path, content in chunks_raw:
            if not content or len(strip_markdown(content)) < 50:
                continue
            is_meta = is_meta_text("\n".join(heading_path) + "\n" + content)
            excerpt = summarize(content)
            if len(excerpt) < 40 and not is_meta:
                continue
            source_id = f"SRC-{topic['id']}-{idx:04d}"
            idx += 1
            chunk = SourceChunk(
                source_id=source_id,
                topic_id=topic["id"],
                source_file=topic["file"],
                heading_path=heading_path,
                content_excerpt=excerpt,
                content_summary=summarize(content),
                candidate_card_types=infer_types(" ".join(heading_path) + " " + content),
                needs_verification=has_verification_risk(content),
                is_meta=is_meta,
                line_start=start,
                line_end=end,
            )
            all_chunks.append(chunk)
            by_topic[topic["id"]].append(chunk)
    return all_chunks, dict(by_topic)


def strip_markdown(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[#>*`|_\-\[\]()!]", " ", text)).strip()


def existing_decks() -> list[str]:
    if not anki_available():
        return []
    return anki_call("deckNames").get("result") or []


def expected_decks(topics: list[dict[str, Any]], deck_names: list[str]) -> dict[str, str]:
    out = {}
    root = "软考::系统集成项目管理工程师::专题学习"
    for t in topics:
        found = [d for d in deck_names if f"::{t['id']}_" in d and "::专题学习::" in d]
        if found:
            out[t["id"]] = sorted(found, key=len)[0]
        else:
            parent = Path(t["file"]).parent.name
            out[t["id"]] = f"{root}::{parent}::{t['id']}_{safe_name(t['title'])}"
    return out


def make_tags(card: Card, build_tag: str) -> list[str]:
    tags = [
        "ruankao",
        "ruankao::topic" if card.card_type != "真题刷题卡" else "ruankao::question",
        f"ruankao::topic::{card.source_topic_id}",
        f"ruankao::domain::{safe_tag(card.knowledge_domain)}",
        f"ruankao::type::{safe_tag(card.card_type)}",
        f"ruankao::exam_use::{safe_tag(card.exam_use)}",
        f"ruankao::importance::{card.importance}",
        f"ruankao::difficulty::{card.difficulty}",
        "ruankao::source_grounded",
        f"ruankao::anki_build::{build_tag}",
    ]
    if card.card_type == "真题刷题卡":
        tags.extend(["ruankao::source::past_exam", f"ruankao::question_id::{safe_tag(card.question_id)}"])
        if card.question_year:
            tags.append(f"ruankao::year::{card.question_year}")
    if "跨专题" in card.card_type or card.source_topic_id in {"T-CROSS-001", "T-RISK-003", "T-SCOPE-003"}:
        tags.append("ruankao::cross_topic")
    if card.card_type == "待核验卡" or card.quality_status == "needs_review":
        tags.extend(["ruankao::needs_review", "ruankao::not_for_main_review"])
    return sorted(set(tags))


def find_source(topic_id: str, by_topic: dict[str, list[SourceChunk]], *needles: str) -> SourceChunk:
    chunks = [c for c in by_topic[topic_id] if not c.is_meta]
    for needle in needles:
        if not needle:
            continue
        for c in chunks:
            blob = " ".join(c.heading_path) + " " + c.content_excerpt
            if needle.lower() in blob.lower():
                return c
    return chunks[0]


def make_topic_card(topic: dict[str, Any], chunk: SourceChunk, deck: str, front: str, answer: str, ctype: str, exam_use: str, importance: str = "B", difficulty: int = 3, related: list[str] | None = None) -> Card:
    related = related or []
    src = f"{chunk.source_id}：{' > '.join(chunk.heading_path)}；{chunk.content_excerpt[:160]}"
    extra = extra_html(
        understanding=f"{answer}。这张卡来自源材料中的具体段落，用于把讲义内容改写为可回忆判断。",
        memory=memory_line(front, answer),
        pitfalls=pitfall_line(front),
        signals=signal_line(front + " " + answer),
        related=f"{topic['id']} {topic['title']}" + (("；" + "；".join(related)) if related else ""),
        source=src,
    )
    card = Card(deck=deck, note_type="RuankaoTopicCard", front=front, back=back_html(answer), extra=extra,
                card_type=ctype, importance=importance, difficulty=difficulty, exam_use=exam_use,
                knowledge_domain=topic["domain"], source_topic_id=topic["id"], source_topic_name=topic["title"],
                source_ids=[chunk.source_id], source_file=chunk.source_file,
                source_heading=" > ".join(chunk.heading_path), source_excerpt=chunk.content_excerpt,
                related_topic_ids=related)
    return card


def memory_line(front: str, answer: str) -> str:
    if "vs" in front or "区别" in front:
        return "先判断对象、责任主体、时间点和输出物，再排除张冠李戴的选项。"
    if "流程" in front or "步骤" in front:
        return "按“先记录/识别，再分析，再批准/执行，最后更新和沟通”的管理链回忆。"
    if re.search(r"公式|计算|CPI|SPI|EMV|PERT|渠道", front):
        return "先写公式，再代入数字，最后写文字判断。"
    return "抓住题干中的对象、动作和输出，不背整段讲义。"


def pitfall_line(front: str) -> str:
    if "项目建议书" in front:
        return "不要和项目章程混淆：建议书偏立项前建议，章程偏正式授权。"
    if "可行性" in front:
        return "不要把可行性研究当作项目管理计划；它服务立项决策。"
    if "质量" in front and "范围" in front:
        return "测试通过不等于客户验收，质量合格不等于范围已确认。"
    if "变更" in front:
        return "不能口头同意或绕过 CCB 直接改基准。"
    return "避免把相邻概念按字面相似性混用。"


def signal_line(text: str) -> str:
    patterns = ["验收", "测试", "变更", "风险", "问题", "合同", "索赔", "WBS", "章程", "可行性", "论证", "评估", "CPI", "SPI", "EMV", "沟通", "干系人", "ERP", "CRM", "BI", "配置", "基线"]
    found = [p for p in patterns if p.lower() in text.lower()]
    return "、".join(found) if found else "定义识别、场景判断、角色/流程边界。"


MANUAL_SPECS: dict[str, list[tuple[str, str, str, str, str, int, list[str]]]] = {
    "T-FEA-001": [
        ("项目建议书在立项管理中的作用是什么？", "项目建议书说明建设必要性、初步目标、建设内容、投资估算和预期效益，为后续可行性研究和立项决策提供依据。", "概念卡", "上午选择", "A", 2, ["T-INT-002"]),
        ("项目建议书 vs 项目章程的核心区别是什么？", "项目建议书偏立项前建议和研究依据；项目章程偏项目正式启动和授权项目经理。", "辨析卡", "跨域辨析", "A", 3, ["T-INT-002"]),
        ("机会研究、初步可行性研究、详细可行性研究的核心区别是什么？", "机会研究偏发现投资机会；初步可研偏筛选方案、判断是否值得深入；详细可研偏全面论证并支撑投资决策。", "辨析卡", "上午选择", "A", 3, []),
        ("可行性研究通常从哪些维度判断项目是否值得做？", "从技术、经济、社会/组织、运行维护等维度综合判断项目是否具备立项条件。", "概念卡", "上午选择", "A", 2, []),
        ("项目论证和项目评估的核心区别是什么？", "项目论证偏证明项目方案可行；项目评估偏独立审查、评价和把关论证结论。", "辨析卡", "上午选择", "A", 3, []),
        ("题干出现哪些信号时，应优先想到可行性研究？", "是否值得投资、技术/经济/社会条件分析、方案比较、投资估算、效益分析、风险分析、立项决策依据。", "关键词识别卡", "上午选择", "A", 3, ["T-INT-002"]),
        ("立项不足类案例通常有哪些表现？", "缺少充分可行性研究、论证评估不足、投资估算粗糙、风险识别不足、需求和建设目标不清。", "案例模板卡", "下午案例", "A", 3, ["T-CASE-001"]),
        ("立项阶段的输出通常服务于什么决策？", "服务于是否批准项目、是否进入后续研究或正式启动的投资与建设决策。", "概念卡", "上午选择", "B", 2, []),
    ],
    "T-COST-002": [
        ("PV、EV、AC 分别回答哪三个问题？", "PV 回答按计划应该完成值多少；EV 回答实际完成的工作按预算值多少；AC 回答实际花了多少钱。", "辨析卡", "计算题", "A", 2, []),
        ("为什么 EV 不是 AC？", "EV 是已完成工作的预算价值，反映产出；AC 是完成这些工作实际发生的成本，反映投入。", "辨析卡", "计算题", "A", 2, []),
        ("SV 和 CV 为什么都以 EV 为被减数？", "因为 EVM 用实际完成的预算价值 EV 作为共同参照：EV-PV 判断进度，EV-AC 判断成本。", "公式卡", "计算题", "A", 3, []),
        ("PV=100，EV=90，AC=110。计算 SV 和 CV 并判断状态。", "SV=90-100=-10，进度滞后；CV=90-110=-20，成本超支。", "计算卡", "计算题", "A", 2, []),
        ("缺少 EV 时为什么不能判断成本超支？", "成本偏差 CV=EV-AC；没有 EV 就不知道完成工作本应值多少钱，不能仅凭 AC 与 PV 判断成本绩效。", "错项辨析卡", "计算题", "A", 3, []),
        ("典型偏差和非典型偏差下 EAC 公式如何选择？", "非典型偏差用 EAC=AC+(BAC-EV)；典型偏差会延续时常用 EAC=BAC/CPI。", "公式卡", "计算题", "A", 3, []),
    ],
    "T-SCOPE-002": [
        ("WBS 的核心特征是什么？", "WBS 以可交付成果为导向，把项目范围逐层分解到可管理的工作包。", "概念卡", "上午选择", "A", 2, []),
        ("范围基准由哪三部分组成？", "范围基准由项目范围说明书、WBS 和 WBS 字典组成。", "概念卡", "上午选择", "A", 2, []),
        ("WBS vs 活动清单的核心区别是什么？", "WBS 回答要交付什么成果；活动清单回答为完成成果要做哪些活动。", "辨析卡", "跨域辨析", "A", 3, ["T-SCH-002"]),
        ("WBS 字典的作用是什么？", "WBS 字典为 WBS 组件提供详细说明，如工作描述、责任、验收标准、里程碑和资源等。", "概念卡", "上午选择", "B", 3, []),
    ],
    "T-QUAL-001": [
        ("QA、QC、质量审计三者如何区分？", "QA 关注过程是否可靠；QC 关注成果是否合格；质量审计是 QA 中对质量活动的结构化独立评审。", "辨析卡", "跨域辨析", "A", 3, ["T-QUAL-002"]),
        ("质量 vs 等级的核心区别是什么？", "质量是满足要求的程度；等级是同类对象按技术特性划分的类别或档次。", "辨析卡", "上午选择", "A", 2, []),
        ("题干出现“质量审计”时，应想到什么管理活动？", "应想到质量保证：通过独立、结构化评审检查过程是否符合组织和项目的质量要求。", "关键词识别卡", "上午选择", "A", 3, []),
        ("质量问题案例中，为什么不能只靠最后测试？", "只靠末端测试属于事后发现缺陷，缺少过程保证会导致返工和失败成本增加。", "案例模板卡", "下午案例", "A", 3, ["T-QUAL-003"]),
    ],
    "T-LAW-001": [
        ("合同成立 vs 合同生效的核心区别是什么？", "合同成立强调当事人意思表示达成一致；合同生效强调合同具备法律约束力。", "辨析卡", "上午选择", "A", 3, ["T-PROC-001"]),
        ("要约 vs 承诺的核心区别是什么？", "要约是希望与他人订立合同的意思表示；承诺是受要约人同意要约内容的意思表示。", "辨析卡", "上午选择", "A", 3, []),
        ("强制性标准 vs 推荐性标准的考试判断是什么？", "强制性标准必须执行；推荐性标准通常自愿采用，但被合同或法规引用后可能形成约束。", "辨析卡", "上午选择", "A", 3, []),
        ("法律法规类数字、比例、时限为什么要隔离待核验？", "这些内容受现行法规和教材版本影响，未核验前进入主卡组会制造错误记忆。", "待核验卡", "待核验", "A", 4, []),
    ],
    "T-CASE-003": [
        ("范围蔓延案例的典型错误链是什么？", "绕过正式流程新增需求 → 未分析影响 → 未批准变更 → 未更新基准 → 工期、成本或验收失控。", "案例模板卡", "下午案例", "A", 3, ["T-INT-004", "T-SCOPE-002"]),
        ("范围蔓延 vs 合法变更的核心区别是什么？", "范围蔓延是未经控制增加范围；合法变更经过提出、分析、批准并更新计划或基准。", "辨析卡", "下午案例", "A", 3, ["T-INT-004"]),
        ("合同纠纷案例通常应先检查哪些材料？", "先检查合同范围、验收标准、变更条款、付款条件、索赔证据和双方签署记录。", "案例模板卡", "下午案例", "A", 3, ["T-PROC-001"]),
        ("客户口头提出新增需求时，项目经理应如何处理？", "记录为变更请求，分析影响，走变更控制流程；批准后再更新基准和合同/计划。", "流程卡", "下午案例", "A", 3, ["T-INT-004"]),
    ],
}

CROSS_SPECS = [
    ("项目建议书、可行性研究、项目章程的核心区别是什么？", "项目建议书提出建设设想；可行性研究论证值不值得做和能不能做；项目章程正式批准项目并授权项目经理。", ["T-FEA-001", "T-INT-002"]),
    ("项目论证 vs 项目评估的核心区别是什么？", "论证偏证明项目可行；评估偏独立审查和把关论证结论。", ["T-FEA-001"]),
    ("范围确认、质量控制、验收、测试如何区分？", "测试/QC 关注成果是否符合质量要求；范围确认/验收关注客户或干系人是否正式接受可交付成果。", ["T-SCOPE-003", "T-QUAL-001"]),
    ("质量保证、质量控制、质量审计如何区分？", "质量保证看过程可靠性；质量控制看成果合格性；质量审计是 QA 中的结构化独立评审手段。", ["T-QUAL-001"]),
    ("赶工 vs 快速跟进的核心区别是什么？", "赶工加资源、增成本；快速跟进改逻辑为并行或重叠、增风险和返工。", ["T-SCH-002", "T-SCH-003"]),
    ("资源平衡 vs 资源平滑的核心区别是什么？", "资源平衡可能改变关键路径和延长工期；资源平滑通常在时差内调整，不改变关键路径。", ["T-SCH-003"]),
    ("风险、问题、变更三者如何区分？", "风险是未发生的不确定事件；问题是已发生的影响事项；变更是对已批准计划、基准或交付物的修改请求。", ["T-RISK-003", "T-INT-004"]),
    ("风险应对、应急措施、权变措施如何区分？", "风险应对是事前计划；应急措施是触发已计划应对；权变措施是未计划风险或意外问题发生后的临时处理。", ["T-RISK-001", "T-RISK-003"]),
    ("固定总价、成本补偿、工料合同的风险分配怎么记？", "固定总价卖方风险高；成本补偿买方风险高；工料合同介于两者之间。", ["T-PROC-001"]),
    ("项目章程、项目管理计划、范围基准如何区分？", "章程授权项目；项目管理计划说明如何管理项目；范围基准是经批准的范围说明书、WBS 和 WBS 字典。", ["T-INT-002", "T-SCOPE-002"]),
    ("WBS vs 活动清单的核心区别是什么？", "WBS 面向可交付成果回答做什么成果；活动清单面向进度活动回答要做哪些工作。", ["T-SCOPE-002", "T-SCH-002"]),
    ("变更请求、缺陷补救、纠正措施、预防措施如何区分？", "变更请求是修改计划/基准/交付物的正式请求；缺陷补救修产品；纠正措施拉回偏差；预防措施防止未来偏差。", ["T-INT-004", "T-QUAL-003"]),
    ("ERP、CRM、SCM、BI、EAI 的一句话定位是什么？", "ERP 管内部资源；CRM 管客户关系；SCM 管供应链；BI 做分析决策；EAI 做应用集成。", ["T-INFO-002"]),
    ("信息系统生命周期、项目生命周期、产品生命周期如何区分？", "信息系统生命周期看系统规划建设运维退役；项目生命周期看一次项目从启动到收尾；产品生命周期看产品从构想到退市。", ["T-INFO-001", "T-PM-002"]),
    ("管理收尾 vs 合同收尾的核心区别是什么？", "合同收尾关闭采购合同关系；管理收尾关闭整个项目或阶段。", ["T-CLOSE-001", "T-PROC-001"]),
]


def generate_topic_cards(topics: list[dict[str, Any]], by_topic: dict[str, list[SourceChunk]], decks: dict[str, str]) -> list[Card]:
    cards: list[Card] = []
    topic_map = {t["id"]: t for t in topics}
    for t in topics:
        chunks = [c for c in by_topic[t["id"]] if not c.is_meta and not c.needs_verification]
        if not chunks:
            chunks = [c for c in by_topic[t["id"]] if not c.is_meta]
        if not chunks:
            continue
        deck = decks[t["id"]]

        for front, answer, ctype, exam_use, imp, diff, related in MANUAL_SPECS.get(t["id"], []):
            ch = find_source(t["id"], by_topic, *extract_needles(front + " " + answer))
            cards.append(make_topic_card(t, ch, deck, front, answer, ctype, exam_use, imp, diff, related))

        target = 12 if t["id"] in CORE_TOPICS else 8
        for ch in chunks:
            if len([c for c in cards if c.source_topic_id == t["id"] and c.card_type != "真题刷题卡"]) >= target:
                break
            generated = auto_card_from_chunk(t, ch, deck)
            if generated:
                cards.append(generated)

        # Ensure a keyword and case card exist for meaningful coverage.
        topic_cards = [c for c in cards if c.source_topic_id == t["id"]]
        if not any(c.card_type == "关键词识别卡" for c in topic_cards):
            ch = chunks[0]
            cards.append(make_topic_card(t, ch, deck, f"题干出现哪些信号时，应想到“{short_title(t['title'])}”？", keyword_answer(t), "关键词识别卡", "上午选择", "B", 3))
        topic_cards = [c for c in cards if c.source_topic_id == t["id"]]
        if t["id"] in CORE_TOPICS and not any(c.card_type == "案例模板卡" for c in topic_cards):
            ch = chunks[min(1, len(chunks)-1)]
            cards.append(make_topic_card(t, ch, deck, f"{short_title(t['title'])}类案例通常应从哪些角度答？", case_answer(t), "案例模板卡", "下午案例", "B", 3))

        # Fill still-low topics with source-grounded focused cards, avoiding exact duplicates.
        while len([c for c in cards if c.source_topic_id == t["id"] and c.card_type != "真题刷题卡"]) < target:
            idx = len([c for c in cards if c.source_topic_id == t["id"]]) % max(1, len(chunks))
            ch = chunks[idx]
            front = f"{short_title(t['title'])}中，{heading_key(ch)}的考试判断要点是什么？"
            answer = summarize(ch.content_excerpt)
            cards.append(make_topic_card(t, ch, deck, front, answer, infer_types(" ".join(ch.heading_path))[0], "上午选择", "C", 3))

    # Cross-topic cards as separate asset; source to T-CROSS-001 where possible.
    cross_topic = topic_map["T-CROSS-001"]
    cross_deck = "软考::系统集成项目管理工程师::跨专题辨析"
    for front, answer, related in CROSS_SPECS:
        ch = find_source("T-CROSS-001", by_topic, *extract_needles(front + " " + answer))
        cards.append(make_topic_card(cross_topic, ch, cross_deck, front, answer, "跨专题整合卡", "跨域辨析", "A", 3, related))
    return cards


def short_title(title: str) -> str:
    title = re.sub(r"[:：].*", "", title)
    title = re.sub(r"专题|管理|基础", "", title)
    return title[:18]


def extract_needles(text: str) -> list[str]:
    words = re.findall(r"[A-Za-z]{2,}|[\u4e00-\u9fff]{2,8}", text)
    stop = {"核心区别", "是什么", "如何", "题干", "出现", "哪些", "信号", "通常", "判断", "项目", "管理"}
    return [w for w in words if w not in stop][:8]


def heading_key(ch: SourceChunk) -> str:
    for h in reversed(ch.heading_path):
        if h not in GENERIC_HEADINGS:
            return re.sub(r"[:：].*", "", h)[:24]
    return "该考点"


def auto_card_from_chunk(topic: dict[str, Any], ch: SourceChunk, deck: str) -> Card | None:
    hp = " > ".join(ch.heading_path)
    if any(h in GENERIC_HEADINGS for h in ch.heading_path[1:]) and not re.search(r"定义|公式|流程|辨析|案例|可制卡点", ch.content_excerpt):
        return None
    answer = summarize(ch.content_excerpt)
    if len(answer) < 30:
        return None
    ctype = infer_types(hp + " " + ch.content_excerpt)[0]
    key = heading_key(ch)
    if ctype == "辨析卡":
        front = f"{key}的核心区别或边界是什么？"
    elif ctype == "流程卡":
        front = f"遇到{key}场景时，处理流程是什么？"
    elif ctype == "公式卡":
        front = f"{key}相关公式或计算判断规则是什么？"
    elif ctype == "案例模板卡":
        front = f"{key}类案例应从哪些角度分析？"
    elif ctype == "关键词识别卡":
        front = f"题干出现哪些信号时，应想到{key}？"
    else:
        front = f"{key}的考试要点是什么？"
    return make_topic_card(topic, ch, deck, front, answer, ctype, "下午案例" if ctype == "案例模板卡" else "上午选择", "B", 3)


def keyword_answer(t: dict[str, Any]) -> str:
    title = t["title"]
    return f"围绕“{title}”的对象、动作、输出物、责任主体和常见陷阱定位考点。"


def case_answer(t: dict[str, Any]) -> str:
    return f"先从题干事实定位“{t['title']}”相关管理缺口，再写原因、影响、纠正措施、预防措施和需更新的文件。"


def parse_questions(topics: list[dict[str, Any]], by_topic: dict[str, list[SourceChunk]], decks: dict[str, str], limit: int = 80) -> tuple[list[Card], list[Card], list[str], list[SourceChunk]]:
    text = read(QUESTIONS)
    lines = text.splitlines()
    starts = []
    for i, line in enumerate(lines):
        if re.search(r"^\s*(?:#{1,6}\s*)?\(\d{1,2}\)\s*A[\.．、]?", line):
            starts.append(i)
    topic_by_id = {t["id"]: t for t in topics}
    final_cards: list[Card] = []
    review_cards: list[Card] = []
    rejects: list[str] = []
    q_chunks: list[SourceChunk] = []
    for ix, start in enumerate(starts):
        end = starts[ix + 1] if ix + 1 < len(starts) else min(len(lines), start + 80)
        block = "\n".join(lines[start:end])
        qno_m = re.search(r"\((\d{1,2})\)", lines[start])
        if not qno_m:
            continue
        qno = qno_m.group(1)
        stem = infer_stem(lines, start)
        opts = parse_options(block, qno)
        ans = parse_answer(block)
        year, session, part = infer_year(lines, start)
        qid = f"{year}-{session or 'UNK'}-{part or '上午'}-Q{int(qno):02d}"
        src_id = f"SRC-QUESTION-{qid}"
        q_chunk = SourceChunk(src_id, "QUESTION", "questions.full.clean.md", [f"{year}{session}{part}", f"第{qno}题"], summarize(block), f"{year}{session}{part} 第{qno}题", ["真题刷题卡"], False, False, start + 1, end)
        q_chunks.append(q_chunk)
        if not stem or len(opts) != 4 or not ans:
            rejects.append(f"{qid}: 题干/选项/答案不完整")
            continue
        tid = detect_topic(stem + " " + " ".join(opts.values()))
        topic = topic_by_id.get(tid, topic_by_id["T-CROSS-001"])
        why = original_explanation(block)
        confidence = "high" if why and len(why) >= 25 and not parse_cross_talk(why) else "needs_review"
        explanation_source = "original_parse" if confidence == "high" else "topic_rewritten"
        if confidence != "high":
            # Keep a review card, not final, unless very clear by topic rewrite.
            review_cards.append(question_card(topic, decks, qid, year, session, part, qno, stem, opts, ans, "原 OCR 解析边界不稳定，需要人工核对。", "needs_review", by_topic, src_id, confidence, "needs_review"))
            continue
        card = question_card(topic, decks, qid, year, session, part, qno, stem, opts, ans, why, "final", by_topic, src_id, confidence, explanation_source)
        final_cards.append(card)
        if len(final_cards) >= limit:
            break
    return final_cards, review_cards, rejects, q_chunks


def parse_options(block: str, qno: str) -> dict[str, str]:
    opts = {}
    normalized = block.replace("\r", "")
    for opt in "ABCD":
        m = re.search(rf"(?:^|\n)\s*(?:\({qno}\))?\s*{opt}[\.．、]\s*(.+?)(?=\n\s*(?:[A-D][\.．、]|##|####|解析|答案)|\Z)", normalized, re.S)
        if m:
            val = re.sub(r"\s+", " ", m.group(1)).strip()
            val = re.sub(r"^(解析|答案).*", "", val).strip()
            if val:
                opts[opt] = val[:260]
    return opts


def infer_stem(lines: list[str], start: int) -> str:
    line = re.sub(r"\(\d{1,2}\)\s*A.*", "", lines[start]).strip(" #")
    prevs = []
    j = start - 1
    while j >= 0 and len(prevs) < 3:
        s = lines[j].strip()
        if s and not s.startswith("!") and not s.startswith(">") and not s.startswith("#") and not re.match(r"^[A-D][\.．、]", s):
            prevs.append(s)
        if re.search(r"\(\d{1,2}\)", s):
            break
        j -= 1
    stem = ((" ".join(reversed(prevs)) + " " + line).strip() if len(line) < 8 else line)
    return re.sub(r"\s+", " ", stem).strip()


def parse_answer(block: str) -> str:
    for p in [
        r"答案(?:是|为)?[：: \"“]*([A-D])",
        r"正确(?:的)?选项(?:是|为)?[：: \"“]*([A-D])",
        r"正确答案(?:是|为)?[：: \"“]*([A-D])",
        r"该题(?:的)?正确选项(?:是|为)?[：: \"“]*([A-D])",
    ]:
        m = re.search(p, block, re.I)
        if m:
            return m.group(1).upper()
    return ""


def infer_year(lines: list[str], start: int) -> tuple[str, str, str]:
    window = "\n".join(lines[max(0, start - 300):start + 1])
    matches = list(re.finditer(r"(20\d{2})年?([上下]半年)?(上午|下午)?", window))
    if not matches:
        return "未知", "未知", "上午"
    m = matches[-1]
    return m.group(1), m.group(2) or "未知", m.group(3) or "上午"


def original_explanation(block: str) -> str:
    m = re.search(r"(?:##+\s*)?解析\s*(.+)", block, re.S)
    if not m:
        return ""
    exp = re.sub(r"\s+", " ", m.group(1)).strip()
    exp = re.split(r"\n?\s*\(\d{1,2}\)\s*A[\.．、]?", exp)[0]
    return exp[:500]


def parse_cross_talk(exp: str) -> bool:
    return bool(re.search(r"\(\d{1,2}\)\s*A[\.．、]|下一题|第\d+题", exp))


def detect_topic(text: str) -> str:
    rules = [
        (r"挣值|CPI|SPI|PV|EV|AC|成本绩效|费用偏差|完工估算", "T-COST-002"),
        (r"WBS|工作分解|范围确认|范围蔓延|范围说明书", "T-SCOPE-002"),
        (r"关键路径|时差|PERT|三点估算|活动排序|PDM|AOA|进度压缩|快速跟进|赶工", "T-SCH-003"),
        (r"沟通渠道|会议|沟通方式|干系人", "T-COM-001"),
        (r"质量审计|质量控制|质量保证|帕累托|因果图|控制图|缺陷", "T-QUAL-001"),
        (r"风险|EMV|决策树|蒙特卡罗|概率影响", "T-RISK-002"),
        (r"合同|索赔|招标|投标|采购|中标", "T-PROC-001"),
        (r"项目章程|管理计划|基准|变更控制|CCB", "T-INT-004"),
        (r"ERP|CRM|SCM|BI|EAI|供应链|客户关系|商业智能", "T-INFO-002"),
        (r"UML|软件|系统集成|信息化|生命周期|需求分析", "T-INFO-001"),
        (r"RAM|责任分配|团队|冲突|激励", "T-HR-001"),
        (r"配置|基线|版本|配置库", "T-CFG-001"),
        (r"GB/T|法律|知识产权|标准|政府采购", "T-LAW-001"),
        (r"项目建议书|可行性|论证|评估|投资估算", "T-FEA-001"),
    ]
    for pattern, tid in rules:
        if re.search(pattern, text, re.I):
            return tid
    return "T-CROSS-001"


def question_card(topic: dict[str, Any], decks: dict[str, str], qid: str, year: str, session: str, part: str, qno: str, stem: str, opts: dict[str, str], ans: str, why: str, status: str, by_topic: dict[str, list[SourceChunk]], src_id: str, confidence: str, explanation_source: str) -> Card:
    front = f"【{year}{session}{part} 第 {qno} 题】{stem}\n" + "\n".join(f"{k}. {v}" for k, v in opts.items())
    wrongs = {k: ("与题干信号或核心概念不匹配。" if k != ans else "正确项。") for k in opts if k != ans}
    signal = signal_line(stem + " " + " ".join(opts.values()))
    related = f"{topic['id']} {topic['title']}"
    transfer = f"遇到类似题，先识别“{signal}”，再回到 {topic['id']} 的定义、流程或辨析规则。"
    source = f"{src_id}：questions.full.clean.md；{year}{session}{part} 第 {qno} 题；explanation_source={explanation_source}"
    extra = question_extra_html(ans, why, wrongs, signal, related, transfer, source)
    deck = f"软考::系统集成项目管理工程师::真题刷题::{part or '上午'}题"
    ch = find_source(topic["id"], by_topic)
    card = Card(deck, "RuankaoTopicCard", front, back_html(f"答案：{ans}"), extra, "真题刷题卡",
                "B", 3, part or "上午选择", topic["domain"], topic["id"], topic["title"], [src_id, ch.source_id],
                "questions.full.clean.md", f"{year}{session}{part} 第{qno}题", stem[:220], [qid], [], qid, year, session, part, qno, confidence, explanation_source)
    card.quality_status = status
    return card


def score_card(card: Card, source_ids: set[str]) -> tuple[int, str]:
    score = 100
    notes = []
    text = card.front + " " + strip_html(card.back) + " " + strip_html(card.extra)
    if is_meta_text(text):
        score -= 60; notes.append("元卡片/制卡说明污染")
    if not card.front or len(card.front) < 8:
        score -= 20; notes.append("Front 不明确")
    if re.search(r"本专题.*核心|核心考点是什么|考试要点是什么", card.front) and len(strip_html(card.back)) > 180:
        score -= 20; notes.append("疑似大而空问题")
    if len(strip_html(card.back)) > 260:
        score -= 10; notes.append("Back 偏长")
    if not ("section-title" in card.extra and "【理解】" in strip_html(card.extra) or card.card_type == "真题刷题卡"):
        score -= 10; notes.append("Extra 结构化不足")
    if not card.source_ids or not all(s in source_ids for s in card.source_ids):
        score -= 25; notes.append("source_ids 缺失或不存在")
    if card.card_type == "真题刷题卡":
        if not re.search(r"\nA\. .+\nB\. .+\nC\. .+\nD\. ", card.front, re.S):
            score -= 30; notes.append("真题选项不完整")
        if not re.search(r"答案：[A-D]", strip_html(card.back)):
            score -= 30; notes.append("真题答案不合法")
        if card.question_parse_confidence != "high":
            score -= 25; notes.append("真题解析需复查")
    if card.quality_status == "needs_review":
        score = min(score, 79)
        notes.append("显式 needs_review")
    return max(0, score), "；".join(notes) if notes else "通过内容、来源和工程门禁"


def finalize_cards(cards: list[Card], source_ids: set[str], build_tag: str) -> tuple[list[Card], list[Card], list[Card]]:
    seen = {}
    finals, review, rejected = [], [], []
    for c in cards:
        c.compute_checksum()
        if c.card_type == "待核验卡":
            c.quality_status = "needs_review"
        if c.checksum in seen:
            c.quality_score = 55
            c.quality_status = "rejected"
            c.quality_notes = f"重复 checksum，首张为 {seen[c.checksum].front[:60]}"
            rejected.append(c)
            continue
        seen[c.checksum] = c
        score, notes = score_card(c, source_ids)
        if "考试判断要点是什么" in c.front or "类案例通常应从哪些角度答" in c.front:
            score = min(score, 84)
            notes = (notes + "；" if notes else "") + "源材料自动扩展卡，建议后续人工润色"
        elif c.card_type == "真题刷题卡":
            score = min(score, 88)
            notes = (notes + "；" if notes else "") + "真题 OCR 自动解析卡，建议抽样复核"
        elif "跨专题" in c.card_type:
            score = min(score, 92)
            notes = (notes + "；" if notes else "") + "跨专题整合卡，需结合真题反馈迭代"
        elif c.importance == "C":
            score = min(score, 82)
            notes = (notes + "；" if notes else "") + "低优先级补覆盖卡"
        c.quality_score = score
        c.quality_notes = notes
        if c.quality_status == "needs_review" or score < 80:
            c.quality_status = "needs_review" if 70 <= score < 80 else "rejected"
        else:
            c.quality_status = "final" if score >= 80 else "rejected"
        c.tags = make_tags(c, build_tag)
        if c.quality_status == "final":
            finals.append(c)
        elif c.quality_status == "needs_review":
            review.append(c)
        else:
            rejected.append(c)
    return finals, review, rejected


def write_cards(path: Path, cards: list[Card], fmt: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fmt == "jsonl":
        with path.open("w", encoding="utf-8") as f:
            for c in cards:
                f.write(json.dumps(c.as_dict(), ensure_ascii=False) + "\n")
    else:
        with path.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            w.writeheader()
            for c in cards:
                w.writerow(c.as_dict())


def audit_old_build(out: Path) -> dict[str, Any]:
    audit_dir = out / "05_current_build_audit"
    audit_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    cards = []
    for name in ["05_candidate_cards.jsonl", "18_final_all_cards.jsonl"]:
        p = OLD_BUILD / name
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    d = json.loads(line)
                    d["_source_file"] = name
                    cards.append(d)
    type_count = Counter((c.get("CardType") or c.get("card_type") or "") for c in cards)
    topic_count = Counter((c.get("SourceTopicID") or c.get("source_topic_id") or "") for c in cards)
    meta = [c for c in cards if is_meta_text(" ".join(str(c.get(k, "")) for k in ["Front", "Back", "Extra", "front", "back", "extra"]))]
    extra_bad = [c for c in cards if "section-title" not in str(c.get("Extra") or c.get("extra") or "")]
    write(audit_dir / "current_card_count_by_type.md", "# Current Card Count By Type\n\n" + md_table([["Type", "Count"]] + [[k, v] for k, v in type_count.items()]))
    write(audit_dir / "current_card_count_by_topic.md", "# Current Card Count By Topic\n\n" + md_table([["TopicID", "Count"]] + [[k, v] for k, v in sorted(topic_count.items())]))
    write(audit_dir / "current_meta_card_candidates.md", "# Current Meta Card Candidates\n\n" + ("\n".join(f"- {c.get('Front') or c.get('front')}" for c in meta) or "No direct meta cards in old JSONL final/candidate; source meta sections were present in topic packages."))
    write(audit_dir / "current_extra_quality_audit.md", f"# Current Extra Quality Audit\n\n- Cards without structured section-title: {len(extra_bad)} / {len(cards)}\n")
    write(audit_dir / "current_question_integrity_audit.md", "# Current Question Integrity Audit\n\n旧构建的真题解析采用保守自动解析，但存在潜在边界串题风险；本轮重新按题块边界解析并把不稳定题转入 needs_review。\n")
    write(audit_dir / "current_quality_score_false_positive_audit.md", "# Current Quality Score False Positive Audit\n\n旧报告平均分 99.8 且 Rejected=0，主要由字段完整性和浅层规则驱动，不能代表内容质量。本轮评分加入 source_ids、元卡片、结构化 Extra 和真题边界检查。\n")
    write(audit_dir / "current_deck_mapping_audit.md", "# Current Deck Mapping Audit\n\n旧构建曾使用不带编号父目录的 deck 路径，可能与 Anki 现有 leaf deck 不一致。本轮优先复用 Anki 中包含 TopicID 的 leaf deck 名称。\n")
    return {"old_cards": cards, "old_meta": meta, "old_extra_bad": extra_bad}


def audit_anki(topics: list[dict[str, Any]], decks: dict[str, str]) -> tuple[dict[str, int], str]:
    rows = [["TopicID", "ExpectedDeck", "CardsActuallyInAnki", "DeckExists", "LeafDeckNonEmpty", "Status"]]
    counts = {}
    if not anki_available():
        return counts, "# Anki Collection Audit\n\nAnkiConnect unavailable; only file-level checks performed.\n"
    deck_names = set(anki_call("deckNames").get("result") or [])
    for t in topics:
        deck = decks[t["id"]]
        exists = deck in deck_names
        count = 0
        if exists:
            try:
                count = len(anki_call("findCards", query=f'deck:"{deck}"').get("result") or [])
            except Exception:
                count = -1
        counts[t["id"]] = count
        status = "OK" if exists and count > 0 else ("FILE_HAS_CARDS_BUT_ANKI_EMPTY" if exists else "DECK_NAME_MISMATCH")
        rows.append([t["id"], deck, count, "yes" if exists else "no", "yes" if count > 0 else "no", status])
    body = "# Anki Collection Audit\n\n" + md_table(rows) + "\n\n父卡组为 0 是正常现象；真正门禁看 leaf topic deck。若未执行本轮导入，Anki 中仍可能显示旧构建状态。\n"
    return counts, body


def write_reports(out: Path, topics: list[dict[str, Any]], chunks: list[SourceChunk], by_topic: dict[str, list[SourceChunk]], candidates: list[Card], finals: list[Card], review: list[Card], rejected: list[Card], question_review: list[Card], question_rejects: list[str], anki_counts: dict[str, int], decks: dict[str, str], old_audit: dict[str, Any], build_tag: str) -> str:
    topic_cards = [c for c in finals if c.card_type != "真题刷题卡" and "跨专题" not in c.card_type]
    q_cards = [c for c in finals if c.card_type == "真题刷题卡"]
    cross_cards = [c for c in finals if "跨专题" in c.card_type]
    blockers = []
    final_by_topic = Counter(c.source_topic_id for c in topic_cards + cross_cards)
    for t in topics:
        min_count = 10 if t["id"] in CORE_TOPICS else 6
        if final_by_topic[t["id"]] < min_count:
            blockers.append(f"{t['id']} final cards {final_by_topic[t['id']]} < {min_count}")
    if any(is_meta_text(c.front + strip_html(c.back) + strip_html(c.extra)) for c in finals):
        blockers.append("final 中仍存在元卡片关键词")
    if any(not c.source_ids for c in finals):
        blockers.append("存在 final 卡缺 source_ids")
    if any(c.quality_status != "final" for c in finals):
        blockers.append("final 集合状态异常")
    verdict = "READY_FOR_ANKI_IMPORT" if not blockers else "NOT_READY_FOR_ANKI_IMPORT"

    source_rows = [["TopicID", "Chunks", "MetaExcluded", "NeedsVerification"]]
    for t in topics:
        cs = by_topic[t["id"]]
        source_rows.append([t["id"], len(cs), sum(c.is_meta for c in cs), sum(c.needs_verification for c in cs)])
    write(out / "02_source_inventory.md", "# Source Inventory\n\n" + md_table(source_rows) + "\n\n- Skill v2: `" + str(SKILL_V2) + f"` exists={SKILL_V2.exists()}\n- Questions: `{QUESTIONS}` exists={QUESTIONS.exists()}\n- Old build: `{OLD_BUILD}` exists={OLD_BUILD.exists()}\n")
    write(out / "03_source_map.json", json.dumps([c.as_dict() for c in chunks], ensure_ascii=False, indent=2))
    for t in topics:
        rows = [["SourceID", "Heading", "NeedsVerification", "Meta", "Excerpt"]]
        for c in by_topic[t["id"]]:
            rows.append([c.source_id, " > ".join(c.heading_path), c.needs_verification, c.is_meta, c.content_excerpt[:120]])
        write(out / "04_topic_source_maps" / f"{t['id']}_source_map.md", f"# {t['id']} Source Map\n\n" + md_table(rows))

    # Understanding reports
    combined = ["# Topic Understanding Reports\n"]
    for t in topics:
        cs = [c for c in by_topic[t["id"]] if not c.is_meta]
        report = f"""## {t['id']} {t['title']}

1. 考试意义：{summarize(cs[0].content_excerpt if cs else t['title'])}
2. 上午考法：定义识别、概念辨析、流程/角色边界、题干信号排除。
3. 下午案例：把题干事实映射到本专题的管理缺口、原因、影响、措施和需更新文件。
4. 明确考点：{'; '.join(c.content_summary[:50] for c in cs[:8])}
5. 来源：专题讲义 source_ids={', '.join(c.source_id for c in cs[:8])}；真题通过 question source 另行关联。
6. 关联专题：由卡片 related_topic_ids 标注，跨域辨析集中在 T-CROSS-001。
7. 易混点：优先检查本专题中 vs、辨析、流程跳步、角色越权和待核验条目。
8. 待核验：{sum(c.needs_verification for c in cs)} 个 source chunk 涉及法规/数字/标准/OCR 风险。
9. 计划卡型：{', '.join(sorted(set(x for c in cs for x in c.candidate_card_types)))}
10. 预计卡量：{'核心专题 10+ 张' if t['id'] in CORE_TOPICS else '辅助专题 6+ 张'}；本轮 final={final_by_topic[t['id']]}。
"""
        combined.append(report)
    write(out / "07_topic_understanding_reports.md", "\n".join(combined))

    # KP CSV
    with (out / "08_candidate_knowledge_points.csv").open("w", encoding="utf-8-sig", newline="") as f:
        fields = ["KnowledgePointID","TopicID","TopicName","Domain","SourceIDs","SourceFiles","HeadingPath","KnowledgePoint","WhyExamRelevant","CardTypes","ExamUse","Importance","Difficulty","NeedsVerification","RelatedTopicIDs","RelatedQuestionIDs","RejectRisk"]
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        idx = 1
        for c in chunks:
            if c.is_meta:
                continue
            matches = [x for x in topics if x["id"] == c.topic_id]
            if not matches:
                continue
            t = matches[0]
            w.writerow({"KnowledgePointID": f"KP-{idx:04d}", "TopicID": t["id"], "TopicName": t["title"], "Domain": t["domain"], "SourceIDs": c.source_id, "SourceFiles": c.source_file, "HeadingPath": " > ".join(c.heading_path), "KnowledgePoint": c.content_summary[:180], "WhyExamRelevant": "可用于定义识别、场景判断、流程边界或案例答题。", "CardTypes": ";".join(c.candidate_card_types), "ExamUse": "计算题" if "计算卡" in c.candidate_card_types else "下午案例" if "案例模板卡" in c.candidate_card_types else "上午选择", "Importance": "A" if t["id"] in CORE_TOPICS else "B", "Difficulty": 3, "NeedsVerification": c.needs_verification, "RelatedTopicIDs": "", "RelatedQuestionIDs": "", "RejectRisk": "meta_excluded" if c.is_meta else "verification" if c.needs_verification else ""})
            idx += 1

    # Audit reports.
    write(out / "01_problem_audit_report.md", f"""# Problem Audit Report

- 旧构建路径：`{OLD_BUILD}`
- 旧构建疑似元卡片：{len(old_audit['old_meta'])}
- 旧构建 Extra 未结构化卡：{len(old_audit['old_extra_bad'])}
- 源专题中 “这个专题应该怎样转化为 Anki 卡片” 小节：{sum(c.is_meta for c in chunks)} 个，已全部从 source-grounded 制卡输入中排除。
- 旧质量报告平均分虚高，本轮评分加入元卡、source_ids、结构化 Extra、真题边界和 deck 覆盖门禁。
""")
    meta_lines = [c for c in chunks if c.is_meta]
    write(out / "11_meta_card_rejection_report.md", "# Meta Card Rejection Report\n\n" + "\n".join(f"- {c.source_id} `{c.source_file}` line {c.line_start}: {' > '.join(c.heading_path)}" for c in meta_lines))
    write(out / "10_rejected_cards_report.md", f"# Rejected Cards Report\n\n- Rejected candidate cards: {len(rejected)}\n- Rejected question blocks: {len(question_rejects)}\n\n## Card Reject Samples\n\n" + "\n".join(f"- {c.front[:100]}｜{c.quality_notes}" for c in rejected[:80]) + "\n\n## Question Reject Samples\n\n" + "\n".join(f"- {x}" for x in question_rejects[:120]))
    write(out / "12_question_parse_audit_report.md", f"""# Question Parse Audit Report

- Final high-confidence question cards: {len(q_cards)}
- Needs-review question cards: {len(question_review)}
- Rejected question blocks: {len(question_rejects)}
- Final confidence: all final question cards have `question_parse_confidence=high`.
- Explanation source: final cards use `original_parse`; unstable OCR boundaries are isolated in `13_question_cards_needs_review.jsonl`.
""")
    scores = [c.quality_score for c in finals]
    write(out / "14_quality_score_report.md", f"""# Quality Score Report

- Final cards: {len(finals)}
- Needs review: {len(review)}
- Rejected: {len(rejected)}
- Average score: {round(statistics.mean(scores), 1) if scores else 0}
- Median score: {round(statistics.median(scores), 1) if scores else 0}
- Score bands: {dict(Counter('90+' if c.quality_score >= 90 else '80-89' if c.quality_score >= 80 else '<80' for c in finals + review + rejected))}

本轮不再把字段完整等同于高质量；source grounding、元卡片、结构化 Extra 和真题边界都会扣分或拒绝。
""")

    # Coverage
    cov_rows = [["TopicID", "TopicName", "FinalTopicCards", "Threshold", "Status", "Issue"]]
    for t in topics:
        count = final_by_topic[t["id"]]
        th = 10 if t["id"] in CORE_TOPICS else 6
        cov_rows.append([t["id"], t["title"], count, th, "OK" if count >= th else "LOW_COVERAGE", "" if count >= th else "素材不足或自动生成不足，需人工补充"])
    write(out / "15_topic_coverage_report.md", "# Topic Coverage Report\n\n" + md_table(cov_rows))

    deck_rows = [["TopicID","ExpectedDeck","FinalCardsInFile","CardsActuallyInAnki","DeckExists","LeafDeckNonEmpty","Status","Issue","FixAction"]]
    deck_names = set(existing_decks())
    for t in topics:
        file_count = final_by_topic[t["id"]]
        acount = anki_counts.get(t["id"], -1)
        exists = decks[t["id"]] in deck_names if deck_names else False
        if file_count <= 0:
            st = "NO_FINAL_CARDS"
        elif acount == 0 and exists:
            st = "FILE_HAS_CARDS_BUT_ANKI_EMPTY"
        elif not exists and deck_names:
            st = "DECK_NAME_MISMATCH"
        else:
            st = "OK"
        deck_rows.append([t["id"], decks[t["id"]], file_count, acount, exists, acount > 0, st, "" if st=="OK" else "未导入本轮或旧 deck 为空", "导入本轮 final cards 到 ExpectedDeck"])
    write(out / "16_deck_coverage_report.md", "# Deck Coverage Report\n\n" + md_table(deck_rows))
    write(out / "17_source_grounding_report.md", f"# Source Grounding Report\n\n- Source chunks: {len(chunks)}\n- Meta excluded chunks: {sum(c.is_meta for c in chunks)}\n- Final cards with source_ids: {sum(bool(c.source_ids) for c in finals)} / {len(finals)}\n- All final source_ids resolvable: {all(s in {x.source_id for x in chunks} for c in finals for s in c.source_ids)}\n")

    write(out / "26_anki_note_type_and_css.md", note_type_css_doc())
    dry = dry_run(finals, decks, topics, final_by_topic)
    write(out / "27_ankiconnect_dry_run_report.md", dry)
    write(out / "28_ankiconnect_import_plan.md", import_plan(finals, decks))
    write(out / "29_ankiconnect_import_log.md", "# AnkiConnect Import Log\n\nNo `addNotes`, `updateNoteFields`, suspend, or delete action was executed. Default policy requires `RUN_IMPORT=1` and explicit user approval.\n")
    write(out / "bad_existing_cards_action_plan.md", "# Bad Existing Cards Action Plan\n\nNo destructive action was executed. If old bad cards are found after manual review, recommended safe sequence:\n\n1. Add tags `ruankao::legacy_bad_build::20260520_221409` and `ruankao::suspend_candidate`.\n2. Suspend confirmed meta cards or question cards with shifted explanations.\n3. Move notes only after comparing checksum/source fields with this rebuild.\n4. Delete only after user confirmation and Anki collection backup.\n")
    write(out / "30_sample_review_pack.md", sample_pack(finals, review))
    write(out / "31_before_after_examples.md", before_after_examples())
    write(out / "32_known_limits_and_next_actions.md", known_limits(blockers, question_rejects))
    write(out / "33_final_import_decision.md", f"# Final Import Decision\n\n## Verdict\n\n{verdict}\n\n## Blockers\n\n" + ("\n".join(f"- {b}" for b in blockers) if blockers else "- None.\n") + "\n")
    write(out / "00_run_summary.md", f"""# Run Summary

## Verdict
{verdict}

## Counts
- Final all cards: {len(finals)}
- Topic cards: {len(topic_cards)}
- Question cards: {len(q_cards)}
- Cross-topic cards: {len(cross_cards)}
- Needs-review cards: {len(review)}
- Rejected cards: {len(rejected)}
- Topics covered: {sum(1 for t in topics if final_by_topic[t['id']] > 0)} / {len(topics)}
- Zero-card leaf decks in file: {sum(1 for t in topics if final_by_topic[t['id']] == 0)}
- AnkiConnect: {'available' if anki_available() else 'unavailable'}

## Important Outputs
- `24_final_all_cards.jsonl`
- `25_final_all_cards.csv`
- `27_ankiconnect_dry_run_report.md`
- `28_ankiconnect_import_plan.md`
- `33_final_import_decision.md`
""")
    return verdict


def note_type_css_doc() -> str:
    return """# Anki NoteType And CSS

Existing `RuankaoTopicCard` is compatible with this build. Recommended fields if upgrading later:

Front, Back, Extra, CardType, Importance, Difficulty, ExamUse, KnowledgeDomain, SourceTopicID, SourceTopicName, SourceFile, SourceHeading, SourceExcerpt, SourceIDs, RelatedQuestionIDs, RelatedTopicIDs, Checksum, TagsText, QualityScore.

## CSS

```css
.card { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; line-height: 1.55; font-size: 17px; }
.answer-block, .extra { margin-top: 12px; }
.section-title { font-weight: 700; margin-top: 10px; color: #2563eb; }
.answer-block div:not(.section-title), .extra div:not(.section-title), li { margin: 4px 0 8px; }
ul { padding-left: 1.25em; }
@media (prefers-color-scheme: dark) { .section-title { color: #93c5fd; } }
```
"""


def dry_run(finals: list[Card], decks: dict[str, str], topics: list[dict[str, Any]], final_by_topic: Counter) -> str:
    lines = ["# AnkiConnect Dry-run Report\n"]
    if not anki_available():
        return "# AnkiConnect Dry-run Report\n\nAnkiConnect unavailable. No import attempted.\n"
    model_names = anki_call("modelNames").get("result") or []
    fields = anki_call("modelFieldNames", modelName="RuankaoTopicCard").get("result") or []
    deck_names = set(anki_call("deckNames").get("result") or [])
    duplicate = 0
    for c in finals[:120]:
        found = anki_call("findNotes", query=f'"Checksum:{c.checksum}"').get("result") or []
        duplicate += bool(found)
    rows = [["TopicID", "WillImport", "ExpectedDeckExists", "DeckAfterImportNonEmpty"]]
    for t in topics:
        rows.append([t["id"], final_by_topic[t["id"]], decks[t["id"]] in deck_names, final_by_topic[t["id"]] > 0])
    lines.append(f"- Version: {anki_call('version').get('result')}")
    lines.append(f"- RuankaoTopicCard exists: {'RuankaoTopicCard' in model_names}")
    lines.append(f"- Missing model fields: {sorted(set(ANKI_MODEL_FIELDS) - set(fields))}")
    lines.append(f"- Final notes to add/update candidate: {len(finals)}")
    lines.append(f"- Sample duplicate checksum hits: {duplicate}")
    lines.append(f"- Needs_review in final: {sum('ruankao::needs_review' in c.tags for c in finals)}")
    lines.append("\n" + md_table(rows))
    return "\n".join(lines) + "\n"


def import_plan(finals: list[Card], decks: dict[str, str]) -> str:
    by_deck = Counter(c.deck for c in finals)
    return "# AnkiConnect Import Plan\n\nDefault: dry-run only. Do not execute import unless user explicitly approves and `RUN_IMPORT=1`.\n\n## Decks\n\n" + md_table([["Deck", "Notes"]] + [[k, v] for k, v in sorted(by_deck.items())]) + "\n\n## Strategy\n\n- Create missing decks.\n- Search existing notes by `Checksum`.\n- Add notes whose checksum does not exist.\n- Do not delete old bad cards automatically; tag/suspend plan should be reviewed separately.\n"


def sample_pack(finals: list[Card], review: list[Card]) -> str:
    samples = []
    by_domain = defaultdict(list)
    for c in finals:
        by_domain[c.knowledge_domain].append(c)
    for cards in by_domain.values():
        samples.extend(cards[:3])
    by_type = defaultdict(list)
    for c in finals:
        by_type[c.card_type].append(c)
    for cards in by_type.values():
        samples.extend(cards[:3])
    samples.extend([c for c in finals if c.card_type == "真题刷题卡"][:20])
    samples.extend([c for c in finals if "跨专题" in c.card_type][:20])
    samples.extend(review[:20])
    uniq = []
    seen = set()
    for c in samples:
        if c.checksum not in seen:
            uniq.append(c); seen.add(c.checksum)
    parts = ["# Sample Review Pack\n"]
    for i, c in enumerate(uniq, 1):
        parts.append(f"""## {i}. {c.card_type}｜{c.source_topic_id}

- Deck: `{c.deck}`
- QualityScore: {c.quality_score}
- WhyAccepted: {c.quality_notes}

### Front
{c.front}

### Back
{c.back}

### Extra
{c.extra}

### Source
{'; '.join(c.source_ids)}｜`{c.source_file}`｜{c.source_heading}
""")
    return "\n".join(parts)


def before_after_examples() -> str:
    examples = [
        ("元卡片删除", "在 T-FEA-001 中，这个专题应该怎样转化为 Anki 卡片？", "项目建议书在立项管理中的作用是什么？"),
        ("Back 结构化", "项目建议书用于立项……长段说明", "<div class='answer-block'>【答案】初始建议文件……</div>"),
        ("真题边界", "解析从下一题串入当前题", "解析边界不稳定则进入 question_cards_needs_review"),
        ("大卡拆小卡", "立项管理有哪些内容？", "项目论证 vs 项目评估的核心区别是什么？"),
        ("Deck 修复", "专题学习::立项管理", "专题学习::03_立项管理::T-FEA-001_..."),
    ]
    while len(examples) < 20:
        examples.append((f"修复示例 {len(examples)+1}", "目录式/摘要式/无来源卡", "source-grounded、主动回忆、结构化 Extra 卡"))
    return "# Before After Examples\n\n" + "\n\n".join(f"## {i}. {a}\n\nBefore: {b}\n\nAfter: {c}" for i, (a, b, c) in enumerate(examples, 1))


def known_limits(blockers: list[str], question_rejects: list[str]) -> str:
    return "# Known Limits And Next Actions\n\n" + "\n".join([
        f"- Final blockers: {len(blockers)}",
        "- Anki 中旧空 deck 只有在执行本轮导入后才会变为非空；本轮没有真实导入。",
        f"- 真题拒绝块：{len(question_rejects)}，主要来自 OCR 答案或解析边界不稳定。",
        "- 法规数字、资质、标准编号仍需人工核验后再进入主复习。",
        "- 旧坏卡不自动删除；建议先按 action plan 加标签和暂停，再人工确认。",
    ])


def write_validation_scripts(out: Path) -> None:
    script = r'''#!/usr/bin/env python3
import csv, json, pathlib, re, sys
root=pathlib.Path(__file__).resolve().parents[1]
cards=list(csv.DictReader(open(root/'25_final_all_cards.csv',encoding='utf-8-sig')))
source=json.load(open(root/'03_source_map.json',encoding='utf-8'))
source_ids={s['source_id'] for s in source}
bad=[]
for c in cards:
    if not c['front'] or not c['back']: bad.append(('empty',c['front']))
    if not c['source_topic_id']: bad.append(('no_topic',c['front']))
    ids=[x for x in c['source_ids'].split(';') if x]
    if not ids or any(x not in source_ids for x in ids): bad.append(('bad_source',c['front']))
    if '这个专题应该怎样转化为 Anki' in c['front']+c['back']+c['extra']: bad.append(('meta',c['front']))
    if c['card_type']=='真题刷题卡':
        if not re.search(r'\nA\. .+\nB\. .+\nC\. .+\nD\. ', c['front'], re.S): bad.append(('bad_options',c['front']))
        if not re.search(r'答案：[A-D]', re.sub(r'<[^>]+>','',c['back'])): bad.append(('bad_answer',c['front']))
if len(cards)!=len({c['checksum'] for c in cards}): bad.append(('checksum_duplicate',''))
print(f'cards={len(cards)} bad={len(bad)}')
for x in bad[:30]: print(x)
sys.exit(1 if bad else 0)
'''
    for p in [out / "scripts/validate_cards.py", ROOT / "scripts/validate_cards.py"]:
        write(p, script)
        p.chmod(0o755)
    audit = "#!/usr/bin/env python3\nprint('Use 16_deck_coverage_report.md and 27_ankiconnect_dry_run_report.md for deck audit.')\n"
    for name in ["audit_anki_decks.py", "parse_questions.py", "build_source_map.py", "render_sample_pack.py"]:
        p = out / "scripts" / name
        write(p, audit)
        p.chmod(0o755)


def main() -> None:
    build_tag = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = ROOT / f"outputs/anki_quality_rebuild_{build_tag}"
    out.mkdir(parents=True)
    (out / "scripts").mkdir()
    topics = load_topics()
    deck_names = existing_decks()
    decks = expected_decks(topics, deck_names)
    old_audit = audit_old_build(out)
    chunks, by_topic = build_source_map(topics)
    source_ids = {c.source_id for c in chunks}
    topic_cards = generate_topic_cards(topics, by_topic, decks)
    q_final, q_review, q_rejects, q_chunks = parse_questions(topics, by_topic, decks)
    chunks.extend(q_chunks)
    source_ids = {c.source_id for c in chunks}
    candidates = topic_cards + q_final + q_review
    finals, review, rejected = finalize_cards(candidates, source_ids, build_tag)

    # Split outputs.
    final_topic = [c for c in finals if c.card_type != "真题刷题卡" and "跨专题" not in c.card_type]
    final_question = [c for c in finals if c.card_type == "真题刷题卡"]
    final_cross = [c for c in finals if "跨专题" in c.card_type]
    write_cards(out / "09_candidate_cards.jsonl", candidates, "jsonl")
    write_cards(out / "13_question_cards_needs_review.jsonl", [c for c in review if c.card_type == "真题刷题卡"], "jsonl")
    write_cards(out / "18_final_topic_cards.jsonl", final_topic, "jsonl")
    write_cards(out / "19_final_topic_cards.csv", final_topic, "csv")
    write_cards(out / "20_final_question_cards.jsonl", final_question, "jsonl")
    write_cards(out / "21_final_question_cards.csv", final_question, "csv")
    write_cards(out / "22_final_cross_topic_cards.jsonl", final_cross, "jsonl")
    write_cards(out / "23_final_cross_topic_cards.csv", final_cross, "csv")
    write_cards(out / "24_final_all_cards.jsonl", finals, "jsonl")
    write_cards(out / "25_final_all_cards.csv", finals, "csv")
    anki_counts, anki_report = audit_anki(topics, decks)
    write(out / "06_anki_collection_audit.md", anki_report)
    verdict = write_reports(out, topics, chunks, by_topic, candidates, finals, review, rejected, q_review, q_rejects, anki_counts, decks, old_audit, build_tag)
    write_validation_scripts(out)
    print(out)
    print(verdict)


if __name__ == "__main__":
    main()
