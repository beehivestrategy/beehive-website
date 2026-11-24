#!/usr/bin/env python3
"""Rebuild the 2026-09-18 onward article window in the approved v9 format.

Reads threads/content_hub/REBUILD_QUEUE_2026-09-18.json, generates one English
source article per (date, slot), translates it to Simplified Chinese, derives
Traditional Chinese (Hong Kong) with OpenCC s2hk plus house-style corrections,
and renders three v9 article pages.

Rules enforced here:
  - EN is the structural source of truth; all three languages ship in one batch.
  - Author and publisher are always Beehive Strategy.
  - 8 visuals: content diagram, workflow, bar chart, matrix, donut, trend,
    90-day roadmap, plus the 1200x630 social card referenced by og:image.
  - 4 schema types: Article, BreadcrumbList, HowTo, FAQPage.
  - Answer-first block, four key takeaways, mid-article lead CTA, FAQ,
    three conversion paths, three related articles, share buttons.
  - No back-to-top control. No published prices. No internal codes in reader text.
  - Illustrative figures are labelled illustrative.

Usage:
    python3 scripts/rebuild_v9.py --limit-days 1        # first day only
    python3 scripts/rebuild_v9.py --from 2026-09-18 --to 2026-09-24
    python3 scripts/rebuild_v9.py --workers 6           # full queue
"""
from __future__ import annotations

import argparse
import copy
import html
import json
import os
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime
from pathlib import Path

try:
    from opencc import OpenCC
except ImportError:  # pragma: no cover
    OpenCC = None

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
QUEUE_PATH = REPO / "threads/content_hub/REBUILD_QUEUE_2026-09-18.json"
LEDGER_PATH = REPO / "threads/content_hub/rebuild_progress.jsonl"
REGISTRY_PATH = REPO / "threads/content_hub/CONTENT_PILLARS.json"
ASSET_V = "20261123.01"
SITE = "https://www.beehivestrategy.com"
MODEL = os.environ.get("REBUILD_MODEL", "deepseek/deepseek-chat-v3.1")
FALLBACK_MODELS = [m for m in os.environ.get(
    "REBUILD_FALLBACKS", "qwen/qwen3-30b-a3b-instruct-2507,deepseek/deepseek-chat-v3.1"
).split(",") if m]

DIRS = {
    "en": ROOT / "blog/articles",
    "zh-cn": ROOT / "zh-cn/blog/articles",
    "zh-hk": ROOT / "zh-hk/blog/articles",
}
DONOR = {
    "en": ROOT / "blog/articles/ai-roi-measurement-framework-enterprise-2026.html",
    "zh-cn": ROOT / "zh-cn/blog/articles/ai-roi-measurement-framework-enterprise-2026.html",
    "zh-hk": ROOT / "zh-hk/blog/articles/ai-roi-measurement-framework-enterprise-2026.html",
}
SVG_DIR = {k: ROOT / f"assets/blog/svg/{k}" for k in DIRS}
SOCIAL_DIR = {k: ROOT / f"assets/blog/social/{k}" for k in DIRS}

UI = {
    "en": {
        "html_lang": "en", "prefix": "",
        "insights": "Insights", "share": "Share",
        "share_items": ["LinkedIn", "X", "WhatsApp", "Facebook", "Copy link"],
        "copy_msg": "Link copied to clipboard!",
        "toc": "In this article",
        "rail_cta": "Not sure where you stand? Measure your AI readiness in 5 minutes →",
        "answer_tag": "In short · answer first",
        "takeaways": "Key takeaways",
        "flow_type": "Workflow · Process chart",
        "bar_type": "Chart · Illustrative model",
        "bar_note": "Illustrative model — replace each value with your own measured baseline before using it in a business case.",
        "matrix_type": "Matrix · Decision aid",
        "donut_type": "Chart · Illustrative mix",
        "donut_note": "Illustrative split only — substitute your own measured baseline before reuse.",
        "trend_type": "Graph · Illustrative trend",
        "trend_note": "Illustrative pattern showing how evidence quality matures; not a measured result.",
        "road_type": "Process chart · 90-day rollout",
        "lead_label": "From reading to doing",
        "lead_title": "Want this applied to your own data and delivery model?",
        "lead_text": "Fixed scope, two weeks, and your team owns the result after we leave.",
        "lead_btn": "Book a scoping call",
        "lead_link": "Or check your AI readiness →",
        "paths_title": "Three ways to move forward",
        "steps_title": "How the work runs",
        "faq_title": "Frequently asked questions",
        "words_unit": "words", "read_time": "min read",
        "related": "Related reading",
        "paths": [
            ("01 / SELF-SERVE", "Measure your readiness", "A 24-question self-assessment across six dimensions. No sign-up required to see your result.", "Start the assessment →", "/readiness"),
            ("02 / EVIDENCE", "See what you receive", "Deliverables, handover and systems already live, so you can judge fit before a call.", "Explore deliverables →", "/proof"),
            ("03 / TALK", "Discuss your use case", "Tell us the decision you want to speed up. We will scope a two-week pilot around it.", "Get in touch →", "/contact"),
        ],
        "figure_caption": "Content diagram derived from the workflow described in this article.",
    },
    "zh-cn": {
        "html_lang": "zh-CN", "prefix": "/zh-cn",
        "insights": "洞察", "share": "分享",
        "share_items": ["LinkedIn", "X", "WhatsApp", "Facebook", "复制链接"],
        "copy_msg": "链接已复制",
        "toc": "本文目录",
        "rail_cta": "不确定自己处于什么水平？5 分钟测一测 AI 就绪度 →",
        "answer_tag": "简答 · 先给答案",
        "takeaways": "核心要点",
        "flow_type": "工作流 · 流程图",
        "bar_type": "图表 · 示例模型",
        "bar_note": "以下为示例模型；用于商业论证前请用你自己的实测基线替换每个数值。",
        "matrix_type": "矩阵 · 决策辅助",
        "donut_type": "图表 · 示例结构",
        "donut_note": "仅为示例结构；再次使用前请以你自己的实测基线替换。",
        "trend_type": "图表 · 示例趋势",
        "trend_note": "示例趋势，说明证据质量如何逐步成熟；并非实测结果。",
        "road_type": "流程图 · 90 天落地",
        "lead_label": "从阅读到行动",
        "lead_title": "想把这套方法应用到自己的数据与交付模式？",
        "lead_text": "范围固定、两周交付；我们离开后由你的团队继续负责。",
        "lead_btn": "预约范围沟通",
        "lead_link": "或者测一测你的 AI 就绪度 →",
        "paths_title": "三种推进方式",
        "steps_title": "工作如何推进",
        "faq_title": "常见问题",
        "words_unit": "字", "read_time": "分钟阅读",
        "related": "相关阅读",
        "paths": [
            ("01 / 自助", "测一测就绪度", "24 道题、六个维度；无需注册即可查看结果。", "开始自评 →", "/readiness"),
            ("02 / 证据", "看看你会收到什么", "交付物、交接方式与已上线系统，让你在沟通前先判断是否匹配。", "查看交付物 →", "/proof"),
            ("03 / 沟通", "讨论你的用例", "告诉我们你想加速哪个决策，我们围绕它规划两周试点。", "联系我们 →", "/contact"),
        ],
        "figure_caption": "内容示意图，依据本文描述的工作流生成。",
    },
    "zh-hk": {
        "html_lang": "zh-HK", "prefix": "/zh-hk",
        "insights": "洞察", "share": "分享",
        "share_items": ["LinkedIn", "X", "WhatsApp", "Facebook", "複製連結"],
        "copy_msg": "連結已複製",
        "toc": "本文目錄",
        "rail_cta": "不確定自己處於甚麼水平？5 分鐘測一測 AI 就緒度 →",
        "answer_tag": "簡答 · 先給答案",
        "takeaways": "核心要點",
        "flow_type": "工作流 · 流程圖",
        "bar_type": "圖表 · 示例模型",
        "bar_note": "以下為示例模型；用於商業論證前請以你自己的實測基線取代每個數值。",
        "matrix_type": "矩陣 · 決策輔助",
        "donut_type": "圖表 · 示例結構",
        "donut_note": "僅為示例結構；再次使用前請以你自己的實測基線取代。",
        "trend_type": "圖表 · 示例趨勢",
        "trend_note": "示例趨勢，說明證據質素如何逐步成熟；並非實測結果。",
        "road_type": "流程圖 · 90 天落地",
        "lead_label": "從閱讀到行動",
        "lead_title": "想把這套方法應用到自己的數據與交付模式？",
        "lead_text": "範圍固定、兩週交付；我們離開後由你的團隊繼續負責。",
        "lead_btn": "預約範圍溝通",
        "lead_link": "或者測一測你的 AI 就緒度 →",
        "paths_title": "三種推進方式",
        "steps_title": "工作如何推進",
        "faq_title": "常見問題",
        "words_unit": "字", "read_time": "分鐘閱讀",
        "related": "相關閱讀",
        "paths": [
            ("01 / 自助", "測一測就緒度", "24 道題、六個維度；無需註冊即可查看結果。", "開始自評 →", "/readiness"),
            ("02 / 證據", "看看你會收到甚麼", "交付物、交接方式與已上線系統，讓你在溝通前先判斷是否匹配。", "查看交付物 →", "/proof"),
            ("03 / 溝通", "討論你的用例", "告訴我們你想加速哪個決策，我們圍繞它規劃兩週試點。", "聯絡我們 →", "/contact"),
        ],
        "figure_caption": "內容示意圖，依據本文描述的工作流生成。",
    },
}

ANGLES = [
    "the cost of leaving it unchanged",
    "a practical implementation blueprint",
    "the objection buyers raise in the first meeting",
    "how to measure and prove the outcome",
    "governance and risk boundaries",
    "build versus buy",
    "the first 90 days",
    "the team and operating model",
    "data readiness prerequisites",
    "how to evaluate vendors",
    "failure modes and how to avoid them",
    "lessons from scaling beyond the pilot",
]

HK_FIX = {
    "数据": "數據", "质量": "質素", "信息": "資訊", "软件": "軟件",
    "网络": "網絡", "用户": "用戶", "项目": "項目", "实施": "實施",
    "优化": "優化", "运营": "營運", "水平": "水平", "视频": "影片",
    "打印": "打印", "屏幕": "螢幕", "排队": "排隊", "默认": "預設", "户": "戶", "门": "門",
}


# ---------------------------------------------------------------- utilities
def esc(value) -> str:
    return html.escape(str(value), quote=True)


def strip_tags(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", value)).strip()


def slugify(text: str, maxlen: int = 60) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    if len(s) > maxlen:
        s = s[:maxlen].rsplit("-", 1)[0].strip("-")
    stop = {"from", "to", "for", "the", "a", "an", "of", "in", "on", "and", "with",
            "that", "this", "is", "are", "why", "how", "what", "when", "your", "you"}
    words = s.split("-")
    while len(words) > 3 and words[-1] in stop:
        words.pop()
    return "-".join(words)


def count_en_words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:[’'\-][A-Za-z0-9]+)*", text))


def count_cjk(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def fmt_date(iso: str, lang: str) -> str:
    d = datetime.strptime(iso, "%Y-%m-%d").date()
    if lang == "en":
        return d.strftime("%d %b %Y").lstrip("0")
    return f"{d.year}年{d.month}月{d.day}日"


def load_key() -> str:
    env = REPO / "ai-geo-seo-mcp/.env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("OPENROUTER_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise SystemExit("OPENROUTER_API_KEY not found")
    return key


def call_model(key: str, prompt: str, max_tokens: int = 6000, temperature: float = 0.6) -> str:
    models = [MODEL] + [m for m in FALLBACK_MODELS if m != MODEL]
    errors = []
    for model in models:
        body = json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }).encode()
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=body,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        )
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=300) as resp:
                    data = json.loads(resp.read())
                choice = data["choices"][0]
                content = choice["message"].get("content") or ""
                if content.strip():
                    return content
                errors.append(f"{model}: empty content ({choice.get('finish_reason')})")
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{model}: {type(exc).__name__}: {exc}")
            time.sleep(2 + attempt * 3)
    raise RuntimeError("all models failed -> " + " | ".join(errors[-4:]))


def parse_json(raw: str) -> dict:
    text = raw.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("no JSON object in response")
    candidate = text[start:end + 1]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        candidate = re.sub(r",\s*([}\]])", r"\1", candidate)
        return json.loads(candidate)


# ---------------------------------------------------------------- prompt
SCHEMA_HINT = """{
  "title": "specific, 45-68 characters, no clickbait, no colon-only titles",
  "description": "140-160 characters, plain, states the reader benefit",
  "kicker": "Section · Topic, for example Strategy · Measurement",
  "answer": "55-80 words, answer-first: the direct answer to the title question",
  "takeaways": ["4 items, each 12-22 words, concrete and non-overlapping"],
  "sections": [
    {"h2": "5 to 7 sections in reading order",
     "paragraphs": ["2-3 paragraphs per section, each 70-120 words"],
     "bullets": ["0-4 bullets, optional"],
     "table": {"head": ["3-4 columns"], "rows": [["3-4 cells"]]},
     "steps": [{"label": "01 / NAME", "title": "short title", "desc": "20-30 words"}]}
  ],
  "flow": {"title": "name of the five-stage process", "steps": [{"name": "stage name", "text": "20-28 words"}]},
  "bar": {"title": "what the chart shows", "unit": "%", "rows": [{"label": "4-5 short labels", "value": 20}]},
  "matrix": {"title": "decision table title", "head": ["4 columns"], "rows": [["4 rows x 4 cells"]]},
  "donut": {"title": "mix title", "slices": [{"label": "4 labels", "value": 25}]},
  "trend": {"title": "four-period trend title", "labels": ["Q1", "Q2", "Q3", "Q4"], "values": [30, 45, 62, 78]},
  "roadmap": {"title": "90-day title", "phases": [{"period": "DAYS 1-30", "title": "phase name", "desc": "20-28 words"}]},
  "faq": [{"q": "6 buyer questions", "a": "40-70 words each"}],
  "category": "one of: Strategy, Data, Governance, Delivery, Industry",
  "keywords": ["5-8 search phrases a buyer would type"]
}"""


def build_prompt(pillar: dict, post_type: str, angle: str, iso: str) -> str:
    label = pillar["label"]["en"]
    offering = pillar.get("offering_link", "")
    return f"""You are the research and editorial lead at Beehive Strategy, a Hong Kong forward-deployed AI consultancy. Write one long-form English article for an enterprise buyer.

Topic pillar: {label}
Buyer context: {offering}
Editorial angle for this piece: {angle}
Post type: {post_type}
Publication date: {iso}

LENGTH BUDGET (mandatory): 8 sections. Each section has exactly 3 paragraphs. Each paragraph is 110 to 130 words. That is 2,640 to 3,120 words of section body, plus a 65-word answer, four takeaways and six FAQ answers. Do not write fewer sections and do not write shorter paragraphs.

Style: specific, practical, non-generic. Concrete steps, roles, artefacts and decision rules. No filler, no throat-clearing. British spelling. Plain English.
Never invent statistics and present them as measured; any non-definitional number must be framed as an illustrative example. No prices, no client names, no internal codes.

Return ONLY valid JSON matching this structure (no markdown fences, no commentary):
{SCHEMA_HINT}"""


def build_expand_prompt(payload: dict, deficit: int) -> str:
    skeleton = [{"index": i, "h2": s["h2"], "paragraphs": len(s["paragraphs"])}
                for i, s in enumerate(payload["sections"])]
    return f"""The article below is {deficit} words short of its mandatory 2,000-word minimum. Write additional paragraphs to close the gap.

Article title: {payload["title"]}
Existing sections: {json.dumps(skeleton, ensure_ascii=False)}

For each section index that needs depth, write 1 or 2 more paragraphs of 110-130 words that add concrete detail (roles, artefacts, checklists, decision rules, worked examples). Do not repeat existing text. Do not restate the heading.

Return ONLY JSON in this shape:
{{"sections":[{{"index":0,"paragraphs":["...","..."]}},{{"index":2,"paragraphs":["..."]}}]}}"""


def build_translate_prompt(chunk: dict, kind: str) -> str:
    scope = "article metadata, chart labels and FAQ" if kind == "meta" else "article sections"
    target = " Aim for a total of 4,000 to 4,500 Chinese characters across all sections; do not compress to a summary."
    return f"""Translate this English JSON ({scope}) into Simplified Chinese for a mainland enterprise audience. Keep the exact same JSON keys and array lengths. Translate every string value. Keep product and company names in Latin script. Use professional business Chinese, not literal translation. Do not add or remove fields.{target}

Return ONLY the translated JSON.

{json.dumps(chunk, ensure_ascii=False)}"""


# ---------------------------------------------------------------- validation
def _clean(value) -> str:
    text = html.unescape(str(value)).strip()
    return text.replace("§", "Section ").replace("  ", " ")


def normalise(payload: dict) -> dict:
    """Coerce the model output into the exact shape the renderer expects."""
    out = {}
    out["title"] = _clean(payload.get("title", ""))[:120]
    out["description"] = _clean(payload.get("description", ""))
    out["kicker"] = _clean(payload.get("kicker", "")) or "Strategy"
    out["answer"] = _clean(payload.get("answer", ""))
    out["takeaways"] = [_clean(x) for x in (payload.get("takeaways") or [])][:4]
    sections = []
    for sec in payload.get("sections") or []:
        if not isinstance(sec, dict):
            continue
        h2 = _clean(sec.get("h2", ""))
        if not h2:
            continue
        paragraphs = [_clean(p) for p in (sec.get("paragraphs") or []) if _clean(p)]
        bullets = [_clean(b) for b in (sec.get("bullets") or []) if _clean(b)]
        table = sec.get("table") if isinstance(sec.get("table"), dict) else None
        if table:
            head = [str(c).strip() for c in (table.get("head") or [])]
            rows = [[str(c).strip() for c in row] for row in (table.get("rows") or []) if isinstance(row, list)]
            table = {"head": head, "rows": rows} if head and rows else None
        steps = []
        for st in sec.get("steps") or []:
            if isinstance(st, dict) and st.get("title"):
                steps.append({
                    "label": str(st.get("label", "")).strip(),
                    "title": str(st.get("title", "")).strip(),
                    "desc": str(st.get("desc", "")).strip(),
                })
        sections.append({"h2": h2, "paragraphs": paragraphs, "bullets": bullets,
                         "table": table, "steps": steps})
    out["sections"] = sections

    flow = payload.get("flow") or {}
    flow_steps = []
    for st in flow.get("steps") or []:
        if isinstance(st, dict) and st.get("name"):
            flow_steps.append({"name": str(st["name"]).strip(), "text": str(st.get("text", "")).strip()})
    out["flow"] = {"title": str(flow.get("title", "")).strip() or "How the work runs",
                   "steps": flow_steps[:5]}

    bar = payload.get("bar") or {}
    bar_rows = []
    for row in bar.get("rows") or []:
        if isinstance(row, dict) and row.get("label") is not None:
            try:
                bar_rows.append({"label": str(row["label"]).strip(), "value": float(row.get("value", 0))})
            except (TypeError, ValueError):
                continue
    out["bar"] = {"title": str(bar.get("title", "")).strip(), "unit": str(bar.get("unit", "%")).strip(),
                  "rows": bar_rows[:5]}

    matrix = payload.get("matrix") or {}
    m_head = [str(c).strip() for c in (matrix.get("head") or [])]
    m_rows = [[str(c).strip() for c in row] for row in (matrix.get("rows") or []) if isinstance(row, list)]
    out["matrix"] = {"title": str(matrix.get("title", "")).strip(), "head": m_head, "rows": m_rows}

    donut = payload.get("donut") or {}
    slices = []
    for s in donut.get("slices") or []:
        if isinstance(s, dict) and s.get("label") is not None:
            try:
                slices.append({"label": str(s["label"]).strip(), "value": float(s.get("value", 0))})
            except (TypeError, ValueError):
                continue
    out["donut"] = {"title": str(donut.get("title", "")).strip(), "slices": slices[:4]}

    trend = payload.get("trend") or {}
    out["trend"] = {
        "title": str(trend.get("title", "")).strip(),
        "labels": [str(x).strip() for x in (trend.get("labels") or ["Q1", "Q2", "Q3", "Q4"])][:4],
        "values": [float(v) for v in (trend.get("values") or [40, 55, 70, 82]) if isinstance(v, (int, float))][:4],
    }

    road = payload.get("roadmap") or {}
    phases = []
    for ph in road.get("phases") or []:
        if isinstance(ph, dict) and ph.get("title"):
            phases.append({"period": str(ph.get("period", "")).strip(),
                           "title": str(ph["title"]).strip(),
                           "desc": str(ph.get("desc", "")).strip()})
    out["roadmap"] = {"title": str(road.get("title", "")).strip(), "phases": phases[:3]}

    faq = []
    for item in payload.get("faq") or []:
        if isinstance(item, dict) and item.get("q"):
            faq.append({"q": str(item["q"]).strip(), "a": str(item.get("a", "")).strip()})
    out["faq"] = faq[:6]
    out["category"] = str(payload.get("category", "Strategy")).strip() or "Strategy"
    out["keywords"] = [str(k).strip() for k in (payload.get("keywords") or [])][:8]
    return out


def body_text(payload: dict) -> str:
    chunks = [payload["answer"], " ".join(payload["takeaways"])]
    for sec in payload["sections"]:
        chunks.append(sec["h2"])
        chunks.extend(sec["paragraphs"])
        chunks.extend(sec["bullets"])
        if sec["table"]:
            chunks.extend(sec["table"]["head"])
            for row in sec["table"]["rows"]:
                chunks.extend(row)
        for st in sec["steps"]:
            chunks.extend([st["label"], st["title"], st["desc"]])
    chunks.extend([f'{f["q"]} {f["a"]}' for f in payload["faq"]])
    # Chart and process labels are rendered as reader-visible text, so they must
    # count towards the length budget or the rendered page overruns the cap.
    chunks.append(payload["flow"]["title"])
    chunks.extend([f'{s["name"]} {s["text"]}' for s in payload["flow"]["steps"]])
    chunks.append(payload["bar"]["title"])
    chunks.extend([r["label"] for r in payload["bar"]["rows"]])
    chunks.append(payload["matrix"]["title"])
    chunks.extend(payload["matrix"]["head"])
    chunks.extend([c for row in payload["matrix"]["rows"] for c in row])
    chunks.append(payload["donut"]["title"])
    chunks.extend([s["label"] for s in payload["donut"]["slices"]])
    chunks.append(payload["trend"]["title"])
    chunks.extend(payload["trend"]["labels"])
    chunks.append(payload["roadmap"]["title"])
    chunks.extend([f'{ph["period"]} {ph["title"]} {ph["desc"]}' for ph in payload["roadmap"]["phases"]])
    return " ".join(chunks)


# ---------------------------------------------------------------- zh-HK
def to_hk(cn: str, converter) -> str:
    out = converter.convert(cn) if converter else cn
    for simp, trad in HK_FIX.items():
        out = out.replace(simp, trad)
    return out


def walk_strings(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return [walk_strings(v) for v in value]
    if isinstance(value, dict):
        return {k: walk_strings(v) for k, v in value.items()}
    return value


def payload_to_hk(payload: dict, converter) -> dict:
    def conv(v):
        if isinstance(v, str):
            return to_hk(v, converter)
        if isinstance(v, list):
            return [conv(x) for x in v]
        if isinstance(v, dict):
            return {k: conv(x) for k, x in v.items()}
        return v
    return conv(payload)


# ---------------------------------------------------------------- render
def render_svg_diagram(payload: dict, lang: str, path: Path) -> None:
    steps = payload["flow"]["steps"][:5]
    if len(steps) < 3:
        steps = [{"name": s["h2"][:28], "text": ""} for s in payload["sections"][:5]]
    n = max(3, len(steps))
    width, height = 1000, 260
    box_w = (width - 40 - (n - 1) * 22) / n
    parts = []
    for i, st in enumerate(steps[:n]):
        x = 20 + i * (box_w + 22)
        name = (st.get("name") or "")[:26]
        parts.append(
            f'<rect x="{x:.0f}" y="60" width="{box_w:.0f}" height="120" rx="10" '
            f'fill="#F4F8FF" stroke="#0F62FE" stroke-opacity=".35"/>'
            f'<text x="{x + box_w/2:.0f}" y="92" text-anchor="middle" font-size="13" '
            f'font-weight="700" fill="#0F62FE">{i+1:02d}</text>'
            f'<text x="{x + box_w/2:.0f}" y="122" text-anchor="middle" font-size="15" '
            f'fill="#101828">{esc(name)}</text>'
        )
        if i < n - 1:
            ax = x + box_w + 4
            parts.append(f'<path d="M{ax:.0f} 120 L{ax+14:.0f} 120" stroke="#0F62FE" stroke-width="2"/>'
                         f'<path d="M{ax+10:.0f} 115 L{ax+16:.0f} 120 L{ax+10:.0f} 125" fill="none" stroke="#0F62FE" stroke-width="2"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
           f'role="img" aria-label="{esc(payload["flow"]["title"])}">'
           f'<rect width="{width}" height="{height}" fill="#FFFFFF"/>'
           f'<text x="20" y="32" font-size="16" font-weight="700" fill="#101828">{esc(payload["flow"]["title"][:70])}</text>'
           + "".join(parts) + '</svg>')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg)


def block_answer(payload, ui) -> str:
    return (f'\n<div class="ar-answer"><span class="ar-answer-tag">{esc(ui["answer_tag"])}</span>'
            f'<p>{esc(payload["answer"])}</p></div>\n')


def block_takeaways(payload, ui) -> str:
    items = "".join(f"    <li>{esc(x)}</li>\n" for x in payload["takeaways"])
    return (f'\n<div class="ar-takeaways"><span class="ar-takeaways-tag">{esc(ui["takeaways"])}</span>'
            f'<ul>\n{items}  </ul></div>\n')


def block_flow(payload, ui, heading_id) -> str:
    steps = payload["flow"]["steps"]
    if len(steps) < 3:
        return ""
    cells = ""
    for i, st in enumerate(steps):
        cells += (f'      <div class="ar-flow-step"><b>{i+1:02d} / STEP</b><strong>{esc(st["name"])}</strong>'
                  f'<p>{esc(st["text"])}</p></div>\n')
    return (f'\n<section class="ar-visual" id="{heading_id}" aria-label="{esc(ui["flow_type"])}">'
            f'<div class="ar-visual-hd"><span>{esc(ui["flow_type"])}</span>'
            f'<h3>{esc(payload["flow"]["title"])}</h3></div>'
            f'<div class="ar-visual-bd"><div class="ar-flow">\n{cells}    </div></div></section>\n')


def block_bars(payload, ui) -> str:
    rows = payload["bar"]["rows"]
    if not rows:
        return ""
    top = max((r["value"] for r in rows), default=1) or 1
    body = ""
    for r in rows:
        pct = min(100, round(r["value"] / top * 100))
        body += (f'      <div class="ar-bar-row"><span>{esc(r["label"])}</span>'
                 f'<div class="ar-bar-track"><div class="ar-bar-fill" style="width:{pct}%"></div></div>'
                 f'<b>{r["value"]:g}{esc(payload["bar"]["unit"])}</b></div>\n')
    return (f'\n<section class="ar-visual" aria-label="{esc(ui["bar_type"])}">'
            f'<div class="ar-visual-hd"><span>{esc(ui["bar_type"])}</span>'
            f'<h3>{esc(payload["bar"]["title"])}</h3></div>'
            f'<div class="ar-visual-bd"><p class="ar-visual-note">{esc(ui["bar_note"])}</p>'
            f'<div class="ar-bars">\n{body}    </div></div></section>\n')


def block_matrix(payload, ui) -> str:
    m = payload["matrix"]
    if not m["head"] or not m["rows"]:
        return ""
    head = "".join(f"<th>{esc(c)}</th>" for c in m["head"])
    rows = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in row) + "</tr>\n" for row in m["rows"])
    return (f'\n<section class="ar-visual" aria-label="{esc(ui["matrix_type"])}">'
            f'<div class="ar-visual-hd"><span>{esc(ui["matrix_type"])}</span>'
            f'<h3>{esc(m["title"])}</h3></div>'
            f'<div class="ar-visual-bd"><table class="ar-matrix"><thead><tr>{head}</tr></thead>'
            f'<tbody>{rows}</tbody></table></div></section>\n')


def block_donut(payload, ui) -> str:
    slices = payload["donut"]["slices"]
    if len(slices) < 2:
        return ""
    total = sum(s["value"] for s in slices) or 1
    colors = ["#0F62FE", "#0043CE", "#8FB0FF", "#C9D9FF"]
    gradient, cumulative, legend = [], 0.0, ""
    for i, s in enumerate(slices):
        pct = s["value"] / total * 100
        gradient.append(f"{colors[i % len(colors)]} {cumulative:.1f}% {cumulative + pct:.1f}%")
        cumulative += pct
        legend += (f'        <div><i style="background:{colors[i % len(colors)]}"></i>{esc(s["label"])} '
                   f'<b>{pct:.0f}%</b></div>\n')
    return (f'\n<section class="ar-visual" aria-label="{esc(ui["donut_type"])}">'
            f'<div class="ar-visual-hd"><span>{esc(ui["donut_type"])}</span>'
            f'<h3>{esc(payload["donut"]["title"])}</h3></div>'
            f'<div class="ar-visual-bd"><p class="ar-visual-note">{esc(ui["donut_note"])}</p>'
            f'<div class="ar-donut-wrap">'
            f'<div class="ar-donut" style="background:conic-gradient({", ".join(gradient)})" '
            f'role="img" aria-label="{esc(payload["donut"]["title"])}"></div>'
            f'<div class="ar-legend">\n{legend}      </div></div></div></section>\n')


def block_trend(payload, ui) -> str:
    labels, values = payload["trend"]["labels"], payload["trend"]["values"]
    if len(labels) < 3 or len(values) < 3:
        return ""
    n = min(len(labels), len(values))
    labels, values = labels[:n], values[:n]
    top = max(values) or 1
    coords = []
    for i, v in enumerate(values):
        x = 50 + i * (500 / max(1, n - 1))
        y = 180 - (v / top) * 130
        coords.append((x, y))
    poly = " ".join(f"{x:.0f},{y:.0f}" for x, y in coords)
    dots = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4" fill="var(--accent, #0F62FE)"/>' for x, y in coords)
    axis = "".join(f'<text x="{x:.0f}" y="205" text-anchor="middle" font-size="11" '
                   f'fill="var(--text-3, #8B94A8)">{esc(lb)}</text>' for (x, _), lb in zip(coords, labels))
    vals = "".join(f'<text x="{x:.0f}" y="{y-12:.0f}" text-anchor="middle" font-size="11" '
                   f'font-weight="700" fill="var(--accent-strong, #0043CE)">{v:g}</text>'
                   for (x, y), v in zip(coords, values))
    return (f'\n<section class="ar-visual" aria-label="{esc(ui["trend_type"])}">'
            f'<div class="ar-visual-hd"><span>{esc(ui["trend_type"])}</span>'
            f'<h3>{esc(payload["trend"]["title"])}</h3></div>'
            f'<div class="ar-visual-bd"><p class="ar-visual-note">{esc(ui["trend_note"])}</p>'
            f'<div class="ar-trend"><svg viewBox="0 0 600 220" role="img" '
            f'aria-label="{esc(payload["trend"]["title"])}">'
            f'<line x1="40" y1="50" x2="580" y2="50" stroke="var(--border, #DFE5F5)"/>'
            f'<line x1="40" y1="115" x2="580" y2="115" stroke="var(--border, #DFE5F5)"/>'
            f'<line x1="40" y1="180" x2="580" y2="180" stroke="var(--border, #DFE5F5)"/>'
            f'<polyline points="{poly}" fill="none" stroke="var(--accent, #0F62FE)" stroke-width="3" '
            f'stroke-linecap="round" stroke-linejoin="round"/>{dots}{axis}{vals}</svg>'
            f'</div></div></section>\n')


def block_roadmap(payload, ui) -> str:
    phases = payload["roadmap"]["phases"]
    if len(phases) < 2:
        return ""
    cells = "".join(f'      <div class="ar-phase"><b>{esc(p["period"])}</b><h4>{esc(p["title"])}</h4>'
                    f'<p>{esc(p["desc"])}</p></div>\n' for p in phases)
    return (f'\n<section class="ar-visual" aria-label="{esc(ui["road_type"])}">'
            f'<div class="ar-visual-hd"><span>{esc(ui["road_type"])}</span>'
            f'<h3>{esc(payload["roadmap"]["title"])}</h3></div>'
            f'<div class="ar-visual-bd"><div class="ar-roadmap">\n{cells}    </div></div></section>\n')


def block_lead(payload, ui) -> str:
    prefix = ui["prefix"]
    return (f'\n<div class="ar-lead-inline"><span class="ar-lead-label">{esc(ui["lead_label"])}</span>'
            f'<h3>{esc(ui["lead_title"])}</h3><p>{esc(ui["lead_text"])}</p>'
            f'<a class="ar-btn" href="{prefix}/contact">{esc(ui["lead_btn"])}</a>'
            f'<a class="ar-link-inline" href="{prefix}/readiness">{esc(ui["lead_link"])}</a></div>\n')


def block_faq(payload, ui) -> str:
    if not payload["faq"]:
        return ""
    items = ""
    for i, item in enumerate(payload["faq"], start=1):
        items += (f'<div class="faq-item"><button class="faq-question" aria-expanded="false">'
                  f'<span class="faq-question-text"><span class="faq-number">{i}</span>'
                  f'<span>{esc(item["q"])}</span></span></button>'
                  f'<div class="faq-answer" role="region"><div class="faq-answer-inner">'
                  f'{esc(item["a"])}</div></div></div>\n')
    return (f'\n<section class="ar-faq" id="frequently-asked-questions">'
            f'<h2>{esc(ui["faq_title"])}</h2>\n{items}</section>\n')


def block_sections(payload, ui) -> tuple[str, str]:
    """Render the body sections and the table of contents."""
    out, toc = "", ""
    for i, sec in enumerate(payload["sections"], start=1):
        hid = slugify(sec["h2"]) or f"section-{i}"
        toc += f'          <a href="#{hid}"><span>{i:02d}</span>{esc(sec["h2"])}</a>\n'
        out += f'\n<h2 id="{hid}">{esc(sec["h2"])}</h2>\n'
        for p in sec["paragraphs"]:
            out += f"<p>{esc(p)}</p>\n"
        if sec["bullets"]:
            out += "<ul>\n" + "".join(f"  <li>{esc(b)}</li>\n" for b in sec["bullets"]) + "</ul>\n"
        if sec["steps"]:
            for st in sec["steps"]:
                out += (f'<div class="ar-flow-step"><b>{esc(st["label"])}</b>'
                        f'<strong>{esc(st["title"])}</strong><p>{esc(st["desc"])}</p></div>\n')
        if sec["table"]:
            head = "".join(f"<th>{esc(c)}</th>" for c in sec["table"]["head"])
            rows = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in row) + "</tr>\n"
                           for row in sec["table"]["rows"])
            out += (f'<table class="ar-matrix"><thead><tr>{head}</tr></thead>'
                    f'<tbody>{rows}</tbody></table>\n')
    return out, toc


def block_paths(ui) -> str:
    cells = ""
    for num, title, text, go, href in ui["paths"]:
        cells += (f'<a class="ar-path" href="{ui["prefix"]}{href}"><span class="ar-path-num">{esc(num)}</span>'
                  f'<h4>{esc(title)}</h4><p>{esc(text)}</p><span class="ar-path-go">{esc(go)}</span></a>\n')
    return (f'\n<section class="ar-lead-end"><h3>{esc(ui["paths_title"])}</h3>'
            f'<div class="ar-paths">\n{cells}</div></section>\n')


def block_related(lang: str, slug: str, category: str) -> str:
    ui = UI[lang]
    folder = DIRS[lang]
    picks = []
    for p in sorted(folder.glob("*.html")):
        if p.stem == slug:
            continue
        text = p.read_text(errors="ignore")
        if f'data-category="{category}"' in text or (not picks and len(picks) < 3):
            title = re.search(r"<title>(.*?)</title>", text, re.S)
            picks.append((p.stem, html.unescape(title.group(1)).strip() if title else p.stem))
        if len(picks) >= 3:
            break
    if len(picks) < 3:
        for p in sorted(folder.glob("*.html")):
            if p.stem == slug or any(p.stem == s for s, _ in picks):
                continue
            title = re.search(r"<title>(.*?)</title>", p.read_text(errors="ignore"), re.S)
            picks.append((p.stem, html.unescape(title.group(1)).strip() if title else p.stem))
            if len(picks) >= 3:
                break
    cells = ""
    for s, title in picks:
        clean = re.sub(r"\s*\|\s*Beehive Strategy\s*$", "", title)
        cells += (f'<a href="{ui["prefix"]}/blog/articles/{s}">'
                  f'<img src="/assets/blog/social/{lang}/{s}.jpg?v={ASSET_V}" alt="{esc(clean)}" loading="lazy">'
                  f'<span>{esc(clean)}</span></a>\n')
    return (f'\n<section class="ar-related" id="related-articles"><h3>{esc(ui["related"])}</h3>'
            f'<div class="ar-related-grid">\n{cells}</div></section>\n')


def shell_parts(lang: str) -> tuple[str, str]:
    src = DONOR[lang].read_text(errors="ignore")
    body_start = src.find("<body")
    body_open_end = src.find(">", body_start) + 1
    main_start = src.find("<main")
    main_end = src.find("</main>", main_start) + len("</main>")
    before = src[body_open_end:main_start]
    after = src[main_end:]
    after = re.sub(r'<button class="back-to-top"[^>]*>.*?</button>', "", after, flags=re.S)
    after = re.sub(r'<a[^>]*class="back-to-top"[^>]*>.*?</a>', "", after, flags=re.S)
    if "article-layout.js" not in after:
        after = after.replace("</body>",
                              f'<script src="/js/article-layout.js?v={ASSET_V}"></script>\n</body>')
    return before, after


def render_html(lang: str, slug: str, iso: str, payload: dict, svg_path: Path) -> str:
    ui = UI[lang]
    prefix = ui["prefix"]
    canon = f"{SITE}{prefix}/blog/articles/{slug}"
    image = f"{SITE}/assets/blog/social/{lang}/{slug}.jpg?v={ASSET_V}"
    title, desc = payload["title"], payload["description"]
    body_html, toc = block_sections(payload, ui)
    flow = block_flow(payload, ui, "workflow")
    bars = block_bars(payload, ui)
    matrix = block_matrix(payload, ui)
    donut = block_donut(payload, ui)
    trend = block_trend(payload, ui)
    road = block_roadmap(payload, ui)
    faq = block_faq(payload, ui)

    # Visual order: diagram, workflow, bar, matrix, donut, trend, roadmap.
    # Chinese headings slug to an empty string, so the fallback id used by
    # block_sections ("section-N") must be mirrored here or the block is lost.
    sections = payload["sections"]

    def anchor(index: int) -> str:
        return slugify(sections[index]["h2"]) or f"section-{index + 1}"

    body_html = body_html  # keep name for clarity
    if len(sections) >= 2 and bars:
        marker = f'<h2 id="{anchor(1)}"'
        at = body_html.find(marker)
        body_html = (body_html[:at] + bars + body_html[at:]) if at > 0 else body_html + bars
    if len(sections) >= 4 and matrix:
        marker = f'<h2 id="{anchor(3)}"'
        at = body_html.find(marker)
        body_html = (body_html[:at] + matrix + body_html[at:]) if at > 0 else body_html + matrix

    figure = (f'<figure class="ar-figure"><img src="/assets/blog/svg/{lang}/{slug}.svg?v={ASSET_V}" '
              f'alt="{esc(payload["flow"]["title"])}" loading="lazy">'
              f'<figcaption>{esc(ui["figure_caption"])}</figcaption></figure>\n')

    assembly = (block_answer(payload, ui) + block_takeaways(payload, ui) + figure + flow +
                body_html + donut + trend + road + block_lead(payload, ui) + faq)

    words = count_en_words(body_text(payload)) if lang == "en" else count_cjk(body_text(payload))
    read_min = max(1, round(words / 220)) if lang == "en" else max(1, round(words / 400))
    count_label = f"{words:,} {ui['words_unit']}" if lang == "en" else f"{words:,} {ui['words_unit']}"

    org = {"@type": "Organization", "name": "Beehive Strategy", "url": SITE}
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": title, "description": desc,
         "mainEntityOfPage": canon, "author": org, "publisher": org, "image": image,
         "datePublished": iso, "dateModified": "2026-11-23",
         "inLanguage": ui["html_lang"], "wordCount": words},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Insights", "item": f"{SITE}{prefix}/blog"},
            {"@type": "ListItem", "position": 3, "name": title, "item": canon}]},
        {"@type": "HowTo", "name": payload["flow"]["title"], "description": payload["answer"],
         "step": [{"@type": "HowToStep", "position": i + 1, "name": s["name"], "text": s["text"]}
                  for i, s in enumerate(payload["flow"]["steps"])]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": f["q"],
             "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in payload["faq"]]},
    ]}

    share = "".join([
        f'<a id="share-linkedin" href="#">{esc(ui["share_items"][0])}</a>',
        f'<a id="share-x" href="#">{esc(ui["share_items"][1])}</a>',
        f'<a id="share-whatsapp" href="#">{esc(ui["share_items"][2])}</a>',
        f'<a id="share-facebook" href="#">{esc(ui["share_items"][3])}</a>',
        f'<button id="share-copy" type="button" data-copy-msg="{esc(ui["copy_msg"])}">{esc(ui["share_items"][4])}</button>',
    ])

    head = f'''<!DOCTYPE html>
<html lang="{ui["html_lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | Beehive Strategy</title>
<link rel="stylesheet" href="/css/accenture.css?v=20261118.06">
<link rel="stylesheet" href="/css/legacy-bridge.css?v=20261120.03">
<link rel="stylesheet" href="/css/article-layout.css?v={ASSET_V}">
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canon)}">
<link rel="alternate" hreflang="en" href="{SITE}/blog/articles/{slug}">
<link rel="alternate" hreflang="zh-cn" href="{SITE}/zh-cn/blog/articles/{slug}">
<link rel="alternate" hreflang="zh-hk" href="{SITE}/zh-hk/blog/articles/{slug}">
<link rel="alternate" hreflang="x-default" href="{SITE}/blog/articles/{slug}">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canon)}">
<meta property="og:image" content="{esc(image)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{esc(image)}">
<meta property="article:author" content="Beehive Strategy">
<meta property="article:published_time" content="{iso}">
<meta property="article:modified_time" content="2026-11-23">
<meta name="keywords" content="{esc(', '.join(payload["keywords"]))}">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</head>
'''
    main = f'''
<main role="main" class="ar-page">
  <div class="ar-wrap">
    <nav class="ar-eyebrow" aria-label="Section"><a href="{prefix}/blog">{esc(ui["insights"])}</a><span class="ar-sep">/</span><span>{esc(payload["category"])}</span></nav>
    <header class="ar-masthead">
      <span class="ar-kicker">{esc(payload["kicker"])}</span>
      <h1 class="ar-title">{esc(title)}</h1>
      <div class="ar-meta"><span class="ar-avatar">BS</span><span class="ar-author">Beehive Strategy</span>
        <span class="ar-dot">·</span><time datetime="{iso}">{esc(fmt_date(iso, lang))}</time>
        <span class="ar-dot">·</span><span>{esc(count_label)}</span>
        <span class="ar-dot">·</span><span>{read_min} {esc(ui["read_time"])}</span></div>
      <div class="ar-share" aria-label="{esc(ui["share"])}">
        <span class="ar-share-label">{esc(ui["share"])}</span>{share}</div>
    </header>
    <div class="ar-grid">
      <aside class="ar-rail">
        <nav class="ar-toc" aria-label="{esc(ui["toc"])}"><span class="ar-toc-label">{esc(ui["toc"])}</span>
{toc}        </nav>
        <a class="ar-rail-cta" href="{prefix}/readiness">{esc(ui["rail_cta"])}</a>
      </aside>
      <article class="ar-body">
{assembly}{block_paths(ui)}{block_related(lang, slug, payload["category"])}
      </article>
    </div>
  </div>
</main>
'''
    before, after = shell_parts(lang)
    return head + before + main + after


# ---------------------------------------------------------------- pipeline
def repair_blocks(key: str, payload: dict) -> dict:
    """Fill any structural gap the first draft left behind."""
    need = []
    if len(payload["flow"]["steps"]) < 3:
        need.append("flow with exactly 5 steps")
    if len(payload["roadmap"]["phases"]) < 2:
        need.append("roadmap with exactly 3 phases")
    if len(payload["bar"]["rows"]) < 3:
        need.append("bar with 4 rows")
    if len(payload["matrix"]["head"]) < 3 or len(payload["matrix"]["rows"]) < 3:
        need.append("matrix with 4 columns and 4 rows")
    if len(payload["donut"]["slices"]) < 2:
        need.append("donut with 4 slices")
    if len(payload["trend"]["labels"]) < 3:
        need.append("trend with 4 labels and 4 values")
    if not need:
        return payload
    headings = [sec["h2"] for sec in payload["sections"]]
    prompt = f"""For the article "{payload['title']}" with sections {json.dumps(headings, ensure_ascii=False)}, produce the missing structural blocks: {', '.join(need)}.

Return ONLY JSON using these keys, each value matching the requested shape and grounded in the article's subject:
{{"flow":{{"title":"...","steps":[{{"name":"...","text":"..."}}]}},"roadmap":{{"title":"...","phases":[{{"period":"DAYS 1-30","title":"...","desc":"..."}}]}},"bar":{{"title":"...","unit":"%","rows":[{{"label":"...","value":20}}]}},"matrix":{{"title":"...","head":["...","...","...","..."],"rows":[["...","...","...","..."]]}},"donut":{{"title":"...","slices":[{{"label":"...","value":25}}]}},"trend":{{"title":"...","labels":["Q1","Q2","Q3","Q4"],"values":[30,45,60,75]}}}}"""
    try:
        raw = call_model(key, prompt, max_tokens=3000, temperature=0.4)
        patch = normalise({**payload, **parse_json(raw)})
        for key_name in ("flow", "roadmap", "bar", "matrix", "donut", "trend"):
            if len(str(patch.get(key_name))) > 40:
                payload[key_name] = patch[key_name]
    except Exception:  # noqa: BLE001
        pass

    # Deterministic fallbacks: a missing block is never acceptable, so derive
    # the remaining ones from content that is already in the article.
    if len(payload["roadmap"]["phases"]) < 2:
        picks = payload["sections"][1:6:2] or payload["sections"][:3]
        periods = ["DAYS 1-30", "DAYS 31-60", "DAYS 61-90"]
        phases = []
        for i, sec in enumerate(picks[:3]):
            first = (sec["paragraphs"][0].split(". ")[0] if sec["paragraphs"] else sec["h2"])
            phases.append({"period": periods[i], "title": sec["h2"][:70],
                           "desc": (first[:180] + ".") if not first.endswith(".") else first[:180]})
        payload["roadmap"] = {"title": "A 90-day route from decision to evidence", "phases": phases}
    if len(payload["donut"]["slices"]) < 2:
        rows = payload["bar"]["rows"][:4]
        if rows:
            payload["donut"] = {"title": "How the measured effect is distributed",
                                "slices": [{"label": r["label"], "value": max(1, r["value"])} for r in rows]}
    return payload


def generate_payload(key: str, pillar: dict, post_type: str, angle: str, iso: str) -> dict:
    prompt = build_prompt(pillar, post_type, angle, iso)
    last_err = None
    payload = None
    for attempt in range(4):
        try:
            raw = call_model(key, prompt, max_tokens=9000)
            payload = normalise(parse_json(raw))
            if len(payload["sections"]) >= 4:
                break
            last_err = f"only {len(payload['sections'])} sections"
        except Exception as exc:  # noqa: BLE001
            last_err = f"{type(exc).__name__}: {exc}"
        time.sleep(2)
    if payload is None:
        raise RuntimeError(f"generation failed: {last_err}")

    # Close any length gap with targeted paragraph expansion.
    for _ in range(2):
        words = count_en_words(body_text(payload))
        if words >= 2000:
            break
        try:
            raw = call_model(key, build_expand_prompt(payload, 2000 - words), max_tokens=6000)
            extra = parse_json(raw)
            for item in extra.get("sections") or []:
                idx = item.get("index")
                if not isinstance(idx, int) or not (0 <= idx < len(payload["sections"])):
                    continue
                for para in item.get("paragraphs") or []:
                    text = str(para).strip()
                    if text:
                        payload["sections"][idx]["paragraphs"].append(text)
        except Exception as exc:  # noqa: BLE001
            last_err = f"expand: {type(exc).__name__}: {exc}"

    words = count_en_words(body_text(payload))
    if words < 1900:
        raise RuntimeError(f"too short after expansion: {words} words ({last_err})")
    payload = repair_blocks(key, payload)
    payload = trim_to_limit(payload, 2880)
    return payload


def _chart_strings(payload: dict) -> list[str]:
    """Ordered list of every human-readable string inside the chart blocks."""
    out = [payload["flow"]["title"]]
    for st in payload["flow"]["steps"]:
        out += [st["name"], st["text"]]
    out.append(payload["bar"]["title"])
    out += [r["label"] for r in payload["bar"]["rows"]]
    out.append(payload["matrix"]["title"])
    out += payload["matrix"]["head"]
    for row in payload["matrix"]["rows"]:
        out += row
    out.append(payload["donut"]["title"])
    out += [s["label"] for s in payload["donut"]["slices"]]
    out.append(payload["trend"]["title"])
    out += payload["trend"]["labels"]
    out.append(payload["roadmap"]["title"])
    for ph in payload["roadmap"]["phases"]:
        out += [ph["period"], ph["title"], ph["desc"]]
    return out


def _apply_chart_strings(payload: dict, translated: list[str]) -> None:
    it = iter(translated)
    def take(n=1):
        return [next(it) for _ in range(n)]
    payload["flow"]["title"] = take()[0]
    for st in payload["flow"]["steps"]:
        st["name"] = take()[0]
        st["text"] = take()[0]
    payload["bar"]["title"] = take()[0]
    for r in payload["bar"]["rows"]:
        r["label"] = take()[0]
    payload["matrix"]["title"] = take()[0]
    payload["matrix"]["head"] = take(len(payload["matrix"]["head"]))
    for row in payload["matrix"]["rows"]:
        for i in range(len(row)):
            row[i] = take()[0]
    payload["donut"]["title"] = take()[0]
    for sl in payload["donut"]["slices"]:
        sl["label"] = take()[0]
    payload["trend"]["title"] = take()[0]
    payload["trend"]["labels"] = take(len(payload["trend"]["labels"]))
    payload["roadmap"]["title"] = take()[0]
    for ph in payload["roadmap"]["phases"]:
        ph["period"] = take()[0]
        ph["title"] = take()[0]
        ph["desc"] = take()[0]


def translate_labels(key: str, strings: list[str]) -> list[str]:
    prompt = ("Translate each string into Simplified Chinese for a mainland enterprise reader. "
              "Return ONLY a JSON array of the same length, in the same order, with no commentary. "
              "Keep product and company names in Latin script.\n\n" + json.dumps(strings, ensure_ascii=False))
    for _ in range(3):
        try:
            raw = call_model(key, prompt, max_tokens=6000, temperature=0.2)
            arr = parse_json_array(raw)
            if len(arr) == len(strings):
                return [str(x) for x in arr]
        except Exception:  # noqa: BLE001
            time.sleep(2)
    return strings


def parse_json_array(raw: str) -> list:
    text = raw.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    start, end = text.find("["), text.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("no JSON array in response")
    return json.loads(text[start:end + 1])


def trim_to_limit(payload: dict, limit: int = 2960) -> dict:
    """Drop the least essential paragraphs until the body fits the 3,000-word cap."""
    while count_en_words(body_text(payload)) > limit:
        sections = [i for i, sec in enumerate(payload["sections"]) if len(sec["paragraphs"]) > 1]
        if not sections:
            break
        idx = max(sections, key=lambda i: len(payload["sections"][i]["paragraphs"]))
        payload["sections"][idx]["paragraphs"].pop()
    return payload


def translate_payload(key: str, payload: dict) -> dict:
    """Translate text, then rebuild chart blocks from the English structure.

    Numbers, ordering and array lengths always come from the English source, so a
    partial translation can never silently drop a chart from the Chinese pages.
    """
    meta_keys = ["title", "description", "kicker", "answer", "takeaways", "faq", "category", "keywords"]
    meta = {k: payload[k] for k in meta_keys}
    cn_meta = {}
    for _ in range(3):
        try:
            raw = call_model(key, build_translate_prompt(meta, "meta"), max_tokens=7000, temperature=0.25)
            cn_meta = parse_json(raw)
            if cn_meta.get("title") and cn_meta.get("answer"):
                break
        except Exception:  # noqa: BLE001
            time.sleep(2)

    sections = payload["sections"]
    cn_sections: list[dict] = []
    for gi in range(0, len(sections), 4):
        group = sections[gi:gi + 4]
        got = None
        for _ in range(3):
            try:
                raw = call_model(key, build_translate_prompt({"sections": group}, f"sections-{gi // 4 + 1}"),
                                 max_tokens=9000, temperature=0.25)
                parsed = parse_json(raw)
                if len(parsed.get("sections") or []) == len(group):
                    got = parsed["sections"]
                    break
            except Exception:  # noqa: BLE001
                time.sleep(2)
        if got is None:
            # Fall back to translating this block section by section so the
            # paragraph structure always stays aligned across languages.
            got = []
            for sec in group:
                single = None
                for _ in range(3):
                    try:
                        raw = call_model(key, build_translate_prompt({"sections": [sec]}, "section"),
                                         max_tokens=4000, temperature=0.25)
                        arr = parse_json(raw).get("sections") or []
                        if len(arr) == 1:
                            single = arr[0]
                            break
                    except Exception:  # noqa: BLE001
                        time.sleep(2)
                got.append(single if single else sec)
        cn_sections.extend(got)

    merged = copy.deepcopy(payload)
    for k, v in cn_meta.items():
        if k in meta_keys:
            merged[k] = v
    merged["sections"] = cn_sections

    labels = translate_labels(key, _chart_strings(payload))
    _apply_chart_strings(merged, labels)
    return normalise(merged)


def article_slug(pillar: dict, iso: str, title: str, taken: set) -> str:
    base = slugify(title) or slugify(pillar["label"]["en"])
    candidate = f"{base}-{iso.replace('-', '')}"
    if candidate in taken:
        candidate = f"{base}-{pillar['id'].lower()}-{iso.replace('-', '')}"
    return candidate


def process_slot(key: str, registry: dict, item: dict, converter) -> dict:
    pillar = next(p for p in registry["pillars"] if p["id"] == item["pillar"])
    angle = ANGLES[(date.fromisoformat(item["date"]).toordinal() + int(item["slot"][1:])) % len(ANGLES)]
    en = generate_payload(key, pillar, item["post_type"], angle, item["date"])
    cn = translate_payload(key, en)
    hk = payload_to_hk(cn, converter)
    slug = item.get("slug") or slugify(en["title"])
    return {"en": en, "zh-cn": cn, "zh-hk": hk, "slug": slug, "item": item}


def write_slot(result: dict) -> dict:
    slug, iso = result["slug"], result["item"]["date"]
    if os.environ.get("REBUILD_DEBUG"):
        dbg = Path("/tmp/rebuild_debug"); dbg.mkdir(parents=True, exist_ok=True)
        for lang in DIRS:
            (dbg / f"{lang}__{slug}.json").write_text(json.dumps(result[lang], ensure_ascii=False))
    written = []
    for lang in DIRS:
        payload = result[lang]
        payload["keywords"] = payload.get("keywords") or []
        svg_path = SVG_DIR[lang] / f"{slug}.svg"
        render_svg_diagram(payload, lang, svg_path)
        html_text = render_html(lang, slug, iso, payload, svg_path)
        target = DIRS[lang] / f"{slug}.html"
        target.write_text(html_text, encoding="utf-8")
        written.append({"lang": lang, "path": str(target), "words": count_en_words(body_text(payload))
                        if lang == "en" else count_cjk(body_text(payload))})
    return {"slug": slug, "date": iso, "slot": result["item"]["slot"], "pillar": result["item"]["pillar"],
            "files": written, "title": result["en"]["title"], "category": result["en"]["category"]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", default=None)
    ap.add_argument("--to", dest="end", default=None)
    ap.add_argument("--limit-days", type=int, default=None)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    queue = json.loads(QUEUE_PATH.read_text())
    registry = json.loads(REGISTRY_PATH.read_text())
    items = [q for q in queue["queue"] if q["language"] == "en"]
    if args.start:
        items = [q for q in items if q["date"] >= args.start]
    if args.end:
        items = [q for q in items if q["date"] <= args.end]
    if args.limit_days:
        days = sorted({q["date"] for q in items})[: args.limit_days]
        items = [q for q in items if q["date"] in days]
    items.sort(key=lambda q: (q["date"], q["slot"]))

    done = set()
    if LEDGER_PATH.exists():
        for line in LEDGER_PATH.read_text().splitlines():
            try:
                row = json.loads(line)
                done.add((row["date"], row["slot"]))
            except Exception:  # noqa: BLE001
                continue
    if done:
        before = len(items)
        items = [q for q in items if (q["date"], q["slot"]) not in done]
        print(f"resume: skipping {before - len(items)} completed slot(s)")

    taken = {p.stem for p in DIRS["en"].glob("*.html")}
    for q in items:
        if q.get("slug") and q["slug"] in taken:
            q["slug"] = None  # force a fresh slug to avoid clobbering a different article

    print(f"slots to build: {len(items)} | model: {MODEL} | workers: {args.workers}")
    if args.dry_run:
        print("dry run only")
        return 0

    key = load_key()
    converter = OpenCC("s2hk") if OpenCC else None
    results, failures = [], []
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(process_slot, key, registry, q, converter): q for q in items}
        for future in as_completed(futures):
            q = futures[future]
            try:
                res = future.result()
                if not res["item"].get("slug"):
                    res["slug"] = article_slug(next(p for p in registry["pillars"] if p["id"] == q["pillar"]),
                                               q["date"], res["en"]["title"], taken)
                taken.add(res["slug"])
                written = write_slot(res)
                results.append(written)
                with LEDGER_PATH.open("a") as fh:
                    fh.write(json.dumps({"date": q["date"], "slot": q["slot"], "slug": written["slug"]}) + "\n")
                print(f'  OK  {q["date"]} {q["slot"]} {q["pillar"]} {res["slug"]} '
                      f'({len(res["en"]["sections"])} sections)')
            except Exception as exc:  # noqa: BLE001
                failures.append({"date": q["date"], "slot": q["slot"], "pillar": q["pillar"],
                                 "error": f"{type(exc).__name__}: {exc}"})
                print(f'  FAIL {q["date"]} {q["slot"]} {q["pillar"]} -> {exc}')

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "model": MODEL,
        "requested": len(items),
        "written": len(results),
        "failed": failures,
        "elapsed_seconds": round(time.time() - t0, 1),
        "articles": sorted(results, key=lambda r: (r["date"], r["slot"])),
    }
    out = REPO / "threads/content_hub/rebuild_run_report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(f'\nwritten {len(results)} / {len(items)} in {report["elapsed_seconds"]}s; failures {len(failures)}')
    print("report:", out)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
