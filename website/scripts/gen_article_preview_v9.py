#!/usr/bin/env python3
"""Generate the v9 long-form article layout previews.

Reads the real trilingual article files, wraps their body in the shared
ar-* shell and injects the SEO/GEO blocks. Preview-only: it never writes
to the public article paths (that is a separate, approved batch).

Usage:
    python3 scripts/gen_article_preview_v9.py
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "ai-roi-measurement-framework-enterprise-2026"
ASSET_V = "20261122.01"
SITE = "https://www.beehivestrategy.com"

SRC = {
    "en": ROOT / "blog/articles" / f"{SLUG}.html",
    "zh-cn": ROOT / "zh-cn/blog/articles" / f"{SLUG}.html",
    "zh-hk": ROOT / "zh-hk/blog/articles" / f"{SLUG}.html",
}
OUT = {
    "en": ROOT / "_previews/_preview_article_v9_en.html",
    "zh-cn": ROOT / "_previews/_preview_article_v9_zh_cn.html",
    "zh-hk": ROOT / "_previews/_preview_article_v9_zh_hk.html",
}

I18N = {
    "en": {
        "html_lang": "en", "prefix": "", "date": "25 Apr 2026",
        "eyebrow_home": "Insights", "eyebrow_section": "Strategy",
        "kicker": "Strategy · Measurement framework", "share_label": "Share",
        "share": ["LinkedIn", "X", "WhatsApp", "Facebook", "Copy link"],
        "copy_msg": "Link copied to clipboard!",
        "toc_label": "In this article",
        "rail_cta": "Not sure where you stand? Measure your AI readiness in 5 minutes →",
        "answer_tag": "In short · GEO answer target",
        "answer": "AI ROI is measurable in 2026, but only when measurement is designed into the initiative before launch. Track three channels — revenue gained, cost avoided and decision-cycle time saved — and attribute each outcome with pre-agreed rules. The organisations that prove value are not the ones with the most advanced models; they are the ones with a disciplined baseline, a counterfactual and a quarterly review cadence.",
        "takeaways_tag": "Key takeaways",
        "takeaways": [
            "Set the baseline and attribution rules before the pilot starts, not after the results arrive.",
            "Measure revenue, cost and decision speed together — a single metric invites vanity reporting.",
            "Reject model accuracy, latency and adoption counts as ROI; they are inputs, not returns.",
            "Review quarterly with finance and the business owner, and retire initiatives that cannot show a credible counterfactual.",
        ],
        "flow_type": "Workflow · Process chart", "flow_title": "The five-stage AI ROI measurement loop",
        "flow": [
            ("01 / BASELINE", "Document the before", "Capture process cost, quality and cycle time before AI is introduced."),
            ("02 / ATTRIBUTE", "Agree the rules", "Define what share of an improvement counts as AI-driven and who validates it."),
            ("03 / INSTRUMENT", "Wire the telemetry", "Instrument the workflow so every decision or transaction has a measurable trail."),
            ("04 / COMPARE", "Test the counterfactual", "Compare against the baseline and a credible no-AI scenario, quarter by quarter."),
            ("05 / DECIDE", "Scale, fix or stop", "Convert evidence into a funding decision, not a retrospective slide."),
        ],
        "bar_type": "Chart · Illustrative model", "bar_title": "Where the return actually shows up",
        "bar_note": "Illustrative model for an enterprise pilot — replace each value with your measured baseline before use.",
        "bars": [("Decision-cycle time", 82, "22%"), ("Analyst rework", 64, "17%"),
                 ("Manual handling cost", 55, "15%"), ("Revenue per seller", 40, "11%")],
        "matrix_type": "Matrix · Decision aid", "matrix_title": "Match the use case to the metric that proves it",
        "matrix_head": ["Use case", "Primary ROI metric", "Leading indicator", "Accountable owner"],
        "matrix_rows": [
            ["Sales enablement", "Revenue per seller", "Proposal turnaround time", "Sales operations"],
            ["Finance close", "Close-cycle labour hours", "Variance-resolution time", "Finance controller"],
            ["Supply chain", "Stock-out cost avoided", "Forecast exception rate", "Planning lead"],
            ["Customer service", "Cost per resolved case", "First-contact resolution", "Service director"],
        ],
        "road_type": "Process chart · 90-day rollout", "road_title": "From baseline to board-ready evidence",
        "road": [
            ("DAYS 1–30", "Establish the baseline", "Agree the metric tree, capture pre-AI cost and quality, and lock the attribution rules with finance."),
            ("DAYS 31–60", "Run the instrumented pilot", "Deploy in one bounded domain, log every decision, and hold a fortnightly evidence review."),
            ("DAYS 61–90", "Convert evidence to decision", "Publish a board-ready ROI note: what changed, what is attributed to AI, and what happens next."),
        ],
        "lead_label": "From reading to doing", "lead_title": "Want this measurement framework applied to your own AI pipeline?",
        "lead_text": "Fixed scope, two weeks, and your team owns the instrumentation after we leave.",
        "lead_btn": "Book a scoping call", "lead_link": "Or check your AI readiness →",
        "paths_title": "Three ways to move forward",
        "paths": [
            ("01 / SELF-SERVE", "Measure your readiness", "A 24-question self-assessment across six dimensions. No sign-up required to see your result.", "Start the assessment →"),
            ("02 / EVIDENCE", "See what you receive", "Deliverables, handover and systems already live — so you can judge fit before a call.", "Explore deliverables →"),
            ("03 / TALK", "Discuss your use case", "Tell us the decision you want to speed up. We will scope a two-week pilot around it.", "Get in touch →"),
        ],
        "faq_extra": [
            ("Which metrics should never be counted as AI ROI?", "Model accuracy, latency, prompt volume and raw adoption counts are inputs or hygiene factors. They can explain why an ROI moved, but they are not a financial or decision-cycle return on their own."),
            ("How often should AI ROI be reviewed?", "Quarterly for funding decisions, with a monthly leading-indicator check during the first 90 days. Annual-only reviews are too slow for an investment whose economics can change within a quarter."),
            ("What is a credible counterfactual for an AI pilot?", "Either the pre-AI process baseline, a matched business unit that did not receive the tool, or a documented no-AI scenario agreed with finance before launch. Choose one in advance and do not change it after seeing results."),
        ],
        "words_unit": "words", "read_time": "min read", "answer_lead": "In short",
        "donut_type": "Chart · Illustrative mix", "donut_title": "How the measured return is distributed",
        "donut_note": "Illustrative split only — replace with your own measured baseline before using it in a business case.",
        "donut_segments": [("Revenue gained", 45, "#0F62FE"), ("Cost avoided", 35, "#0043CE"), ("Decision time saved", 20, "#8fb0ff")],
        "trend_type": "Graph · Illustrative trend", "trend_title": "How ROI confidence matures over four quarters",
        "trend_note": "Illustrative pattern showing how evidence quality improves as instrumentation settles. Not a measured result.",
        "trend_labels": ["Q1", "Q2", "Q3", "Q4"], "trend_values": [32, 48, 67, 85],
        "related_label": "Related reading",
        "related_slugs": ["ai-roi-measurement-board", "ai-roi-measurement-total-cost-ownership", "conversational-bi-roi-how-to-measure-prove-value"],
    },
    "zh-cn": {
        "html_lang": "zh-CN", "prefix": "/zh-cn", "date": "2026年4月25日",
        "eyebrow_home": "洞察", "eyebrow_section": "策略",
        "kicker": "策略 · 衡量框架", "share_label": "分享",
        "share": ["LinkedIn", "X", "WhatsApp", "Facebook", "复制链接"],
        "copy_msg": "链接已复制",
        "toc_label": "本文目录",
        "rail_cta": "不确定自己处于什么水平？5 分钟测一测 AI 就绪度 →",
        "answer_tag": "简答 · GEO 答案目标",
        "answer": "2026 年的 AI 投资回报是可以衡量的，但前提是在项目启动前就把衡量设计进去。需要同时追踪三条回报 channel：新增收入、避免的成本、节省的决策周期时间，并用事先约定的规则归因。真正能证明价值的组织，靠的不是最先进的模型，而是扎实的基线、可信的反事实情景，以及季度复核机制。",
        "takeaways_tag": "核心要点",
        "takeaways": [
            "在试点开始前确定基线与归因规则，而不是等结果出来后再补。",
            "收入、成本、决策速度要一起看——只看单一指标容易变成数字游戏。",
            "模型准确率、延迟和使用量不是 ROI，它们只是投入。",
            "每季度与财务和业务负责人复核；无法给出可信反事实的项目应当停止。",
        ],
        "flow_type": "工作流 · 流程图", "flow_title": "AI ROI 衡量的五阶段闭环",
        "flow": [
            ("01 / 基线", "记录现状", "在引入 AI 前记录流程成本、质量与周期时间。"),
            ("02 / 归因", "约定规则", "定义改善中有多少算 AI 驱动，以及由谁验证。"),
            ("03 / 埋点", "接通数据", "为流程埋点，让每个决策或交易都有可衡量的轨迹。"),
            ("04 / 对比", "检验反事实", "每季度与基线及无 AI 情景对比。"),
            ("05 / 决策", "扩大、修正或停止", "把证据转成预算决策，而不是事后汇报。"),
        ],
        "bar_type": "图表 · 示例模型", "bar_title": "回报真正出现在哪里",
        "bar_note": "以下为企业试点的示例模型；正式使用前请用你自己的基线替换每个数值。",
        "bars": [("决策周期时间", 82, "22%"), ("分析人员返工", 64, "17%"),
                 ("人工处理成本", 55, "15%"), ("每位销售收入", 40, "11%")],
        "matrix_type": "矩阵 · 决策辅助", "matrix_title": "让用例与能证明它的指标匹配",
        "matrix_head": ["用例", "主要 ROI 指标", "先行指标", "责任方"],
        "matrix_rows": [
            ["销售赋能", "每位销售收入", "方案周转时间", "销售运营"],
            ["财务结账", "结账周期人工小时", "差异处理时间", "财务总监"],
            ["供应链", "避免的缺货成本", "预测例外率", "计划负责人"],
            ["客户服务", "单个已解决案件成本", "首次解决率", "服务总监"],
        ],
        "road_type": "流程图 · 90 天落地", "road_title": "从基线到可向董事会汇报的证据",
        "road": [
            ("第 1–30 天", "建立基线", "确定指标树，记录实施前的成本与质量，并与财务锁定归因规则。"),
            ("第 31–60 天", "运行带埋点的试点", "在一个边界清晰的领域部署，记录每个决策，每两周复核证据。"),
            ("第 61–90 天", "把证据变成决策", "发布一页董事会可读的 ROI 说明：变了什么、哪些归因于 AI、下一步做什么。"),
        ],
        "lead_label": "从阅读到行动", "lead_title": "想把这套衡量框架应用到自己的 AI 流程？",
        "lead_text": "范围固定、两周交付；我们离开后由你的团队继续负责衡量。",
        "lead_btn": "预约范围沟通", "lead_link": "或者测一测你的 AI 就绪度 →",
        "paths_title": "三种推进方式",
        "paths": [
            ("01 / 自助", "测一测就绪度", "24 道题、六个维度的自评；无需注册即可查看结果。", "开始评估 →"),
            ("02 / 证据", "看看你会拿到什么", "交付物、移交与已上线系统——先判断是否合适，再约沟通。", "查看交付物 →"),
            ("03 / 沟通", "聊聊你的用例", "告诉我们你想加快哪个决策，我们据此设计一个两周试点。", "联系我们 →"),
        ],
        "faq_extra": [
            ("哪些指标不应算作 AI ROI？", "模型准确率、延迟、提示词数量和原始使用量都属于投入或卫生因素。它们可以解释 ROI 为什么变化，但本身不是财务回报或决策周期回报。"),
            ("AI ROI 应多久复核一次？", "预算决策按季度复核；前 90 天每月检查先行指标。对经济状况可能在一个季度内变化的投资来说，只做年度复核太慢。"),
            ("什么才算可信的 AI 试点反事实？", "可以是实施前的流程基线、未获得工具的可比业务单元，或上线前与财务约定的无 AI 情景。事先选定一种，看到结果后不要更换。"),
        ],
        "words_unit": "字", "read_time": "分钟阅读", "answer_lead": "简答",
        "donut_type": "图表 · 示例结构", "donut_title": "衡量到的回报如何分布",
        "donut_note": "仅为示例结构；用于商业论证前请用你自己的实测基线替换。",
        "donut_segments": [("新增收入", 45, "#0F62FE"), ("避免的成本", 35, "#0043CE"), ("节省的决策时间", 20, "#8fb0ff")],
        "trend_type": "图表 · 示例趋势", "trend_title": "ROI 可信度在四个季度中如何成熟",
        "trend_note": "示例趋势，说明随着埋点稳定、证据质量如何提升；并非实测结果。",
        "trend_labels": ["第 1 季度", "第 2 季度", "第 3 季度", "第 4 季度"], "trend_values": [32, 48, 67, 85],
        "related_label": "相关阅读",
        "related_slugs": ["ai-roi-measurement-board", "ai-roi-measurement-total-cost-ownership", "conversational-bi-roi-how-to-measure-prove-value"],
    },
    "zh-hk": {
        "html_lang": "zh-HK", "prefix": "/zh-hk", "date": "25 Apr 2026",
        "eyebrow_home": "洞察", "eyebrow_section": "策略",
        "kicker": "策略 · 衡量框架", "share_label": "分享",
        "share": ["LinkedIn", "X", "WhatsApp", "Facebook", "複製連結"],
        "copy_msg": "連結已複製",
        "toc_label": "本文目錄",
        "rail_cta": "不確定自己處於甚麼水平？5 分鐘測一測 AI 就緒度 →",
        "answer_tag": "簡答 · GEO 答案目標",
        "answer": "2026 年的 AI 投資回報是可以衡量的，但前提是項目開展前就把衡量設計進去。需要同時追蹤三條回報渠道：新增收入、避免的成本、節省的決策週期時間，並用事先約定的規則歸因。真正能證明價值的組織，靠的不是最先進的模型，而是紮實的基線、可信的無 AI 對照情景，以及季度覆核機制。",
        "takeaways_tag": "核心要點",
        "takeaways": [
            "在試點開始前確定基線與歸屬規則，而不是等結果出爐後再補。",
            "收入、成本、決策速度要一起看——只看單一指標容易淪為數字遊戲。",
            "模型準確率、延遲和使用量不是 ROI，它們只是投入。",
            "每季度與財務及業務負責人覆核；無法提出可信對照情景的項目應停止。",
        ],
        "flow_type": "工作流 · 流程圖", "flow_title": "AI ROI 衡量的五階段閉環",
        "flow": [
            ("01 / 基線", "記錄現狀", "在引入 AI 前記錄流程成本、質素與週期時間。"),
            ("02 / 歸屬", "約定規則", "定義改善中有多少算 AI 驅動，以及由誰驗證。"),
            ("03 / 埋點", "接通數據", "為流程埋點，讓每個決策或交易都有可衡量的軌跡。"),
            ("04 / 對比", "檢驗對照情景", "每季度與基線及無 AI 情景比較。"),
            ("05 / 決策", "擴大、修正或停止", "把證據轉成預算決策，而不是事後匯報。"),
        ],
        "bar_type": "圖表 · 示例模型", "bar_title": "回報真正出現在哪裡",
        "bar_note": "以下為企業試點的示例模型；正式使用前請以你自己的基線取代每個數值。",
        "bars": [("決策週期時間", 82, "22%"), ("分析人員返工", 64, "17%"),
                 ("人工處理成本", 55, "15%"), ("每位銷售收入", 40, "11%")],
        "matrix_type": "矩陣 · 決策輔助", "matrix_title": "讓用例與能證明它的指標配對",
        "matrix_head": ["用例", "主要 ROI 指標", "先行指標", "責任方"],
        "matrix_rows": [
            ["銷售賦能", "每位銷售收入", "方案周轉時間", "銷售營運"],
            ["財務結賬", "結賬週期人工小時", "差異處理時間", "財務總監"],
            ["供應鏈", "避免的缺貨成本", "預測例外率", "策劃主管"],
            ["客戶服務", "每個已解決個案成本", "首次解決率", "服務總監"],
        ],
        "road_type": "流程圖 · 90 天落地", "road_title": "從基線到可向董事會匯報的證據",
        "road": [
            ("第 1–30 天", "建立基線", "確定指標樹，記錄實施前的成本與質素，並與財務鎖定歸屬規則。"),
            ("第 31–60 天", "運行帶埋點的試點", "在一個邊界清晰的領域部署，記錄每個決策，每兩週覆核證據。"),
            ("第 61–90 天", "把證據變成決策", "發布一頁董事會可讀的 ROI 說明：改變了甚麼、哪些歸因於 AI、下一步做甚麼。"),
        ],
        "lead_label": "從閱讀到行動", "lead_title": "想把這套衡量框架應用到自己的 AI 流程？",
        "lead_text": "範圍固定、兩週交付；我們離開後由你的團隊繼續負責衡量。",
        "lead_btn": "預約範圍溝通", "lead_link": "或者測一測你的 AI 就緒度 →",
        "paths_title": "三種推進方式",
        "paths": [
            ("01 / 自助", "測一測就緒度", "24 題、六個維度的自評；無需註冊即可查看結果。", "開始評估 →"),
            ("02 / 證據", "看看你會拿到甚麼", "交付物、移交與已上線系統——先判斷是否合適，再約溝通。", "查看交付物 →"),
            ("03 / 溝通", "談談你的用例", "告訴我們你想加快哪個決策，我們據此設計一個兩週試點。", "聯絡我們 →"),
        ],
        "faq_extra": [
            ("哪些指標不應算作 AI ROI？", "模型準確率、延遲、提示詞數量和原始使用量都屬於投入或基本因素。它們可以解釋 ROI 為何變化，但本身不是財務回報或決策週期回報。"),
            ("AI ROI 應多久覆核一次？", "預算決策按季度覆核；首 90 天每月檢查先行指標。對經濟狀況可能在一個季度內變化的投資來說，只做年度覆核太慢。"),
            ("甚麼才算可信的 AI 試點對照情景？", "可以是實施前的流程基線、未獲得工具的可比業務單位，或開展前與財務約定的無 AI 情景。事先選定一種，看到結果後不要更換。"),
        ],
        "words_unit": "字", "read_time": "分鐘閱讀", "answer_lead": "簡答",
        "donut_type": "圖表 · 示例結構", "donut_title": "衡量到的回報如何分佈",
        "donut_note": "僅為示例結構；用於商業論證前請以你自己的實測基線取代。",
        "donut_segments": [("新增收入", 45, "#0F62FE"), ("避免的成本", 35, "#0043CE"), ("節省的決策時間", 20, "#8fb0ff")],
        "trend_type": "圖表 · 示例趨勢", "trend_title": "ROI 可信度在四個季度中如何成熟",
        "trend_note": "示例趨勢，說明隨着埋點穩定，證據質素如何提升；並非實測結果。",
        "trend_labels": ["第 1 季", "第 2 季", "第 3 季", "第 4 季"], "trend_values": [32, 48, 67, 85],
        "related_label": "相關閱讀",
        "related_slugs": ["ai-roi-measurement-board", "ai-roi-measurement-total-cost-ownership", "conversational-bi-roi-how-to-measure-prove-value"],
    },
}


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def build_blocks(lang: str) -> dict:
    t = I18N[lang]
    answer = f'''
<div class="ar-answer">
  <span class="ar-answer-tag">{esc(t["answer_tag"])}</span>
  <p>{esc(t["answer"])}</p>
</div>
'''
    takeaways = '<div class="ar-takeaways">\n  <span class="ar-takeaways-tag">' + esc(t["takeaways_tag"]) + '</span>\n  <ul>\n'
    for item in t["takeaways"]:
        takeaways += f'    <li>{esc(item)}</li>\n'
    takeaways += '  </ul>\n</div>\n'

    flow = f'''
<section class="ar-visual" aria-label="{esc(t["flow_type"])}">
  <div class="ar-visual-hd"><span>{esc(t["flow_type"])}</span><h3>{esc(t["flow_title"])}</h3></div>
  <div class="ar-visual-bd"><div class="ar-flow">
'''
    for code, title, desc in t["flow"]:
        flow += (f'    <div class="ar-flow-step"><b>{esc(code)}</b><strong>{esc(title)}</strong>'
                 f'<p>{esc(desc)}</p></div>\n')
    flow += '  </div></div>\n</section>\n'

    bars = f'''
<section class="ar-visual" aria-label="{esc(t["bar_type"])}">
  <div class="ar-visual-hd"><span>{esc(t["bar_type"])}</span><h3>{esc(t["bar_title"])}</h3></div>
  <div class="ar-visual-bd">
    <p class="ar-visual-note">{esc(t["bar_note"])}</p>
    <div class="ar-bars">
'''
    for label, width, value in t["bars"]:
        bars += (f'      <div class="ar-bar-row"><span>{esc(label)}</span>'
                 f'<div class="ar-bar-track"><div class="ar-bar-fill" style="width:{width}%"></div></div>'
                 f'<b>{esc(value)}</b></div>\n')
    bars += '    </div>\n  </div>\n</section>\n'

    matrix = f'''
<section class="ar-visual" aria-label="{esc(t["matrix_type"])}">
  <div class="ar-visual-hd"><span>{esc(t["matrix_type"])}</span><h3>{esc(t["matrix_title"])}</h3></div>
  <div class="ar-visual-bd"><table class="ar-matrix"><thead><tr>
'''
    for head in t["matrix_head"]:
        matrix += f'      <th>{esc(head)}</th>\n'
    matrix += '    </tr></thead><tbody>\n'
    for row in t["matrix_rows"]:
        matrix += '      <tr>' + ''.join(f'<td>{esc(cell)}</td>' for cell in row) + '</tr>\n'
    matrix += '    </tbody></table></div>\n</section>\n'

    road = f'''
<section class="ar-visual" aria-label="{esc(t["road_type"])}">
  <div class="ar-visual-hd"><span>{esc(t["road_type"])}</span><h3>{esc(t["road_title"])}</h3></div>
  <div class="ar-visual-bd"><div class="ar-roadmap">
'''
    for phase, title, desc in t["road"]:
        road += (f'      <div class="ar-phase"><b>{esc(phase)}</b><h4>{esc(title)}</h4>'
                 f'<p>{esc(desc)}</p></div>\n')
    road += '    </div></div>\n</section>\n'

    # Return-mix donut (illustrative, never presented as measured data).
    gradient = []
    cumulative = 0
    for _label, pct, color in t["donut_segments"]:
        gradient.append(f'{color} {cumulative}% {cumulative + pct}%')
        cumulative += pct
    donut = f'''
<section class="ar-visual" aria-label="{esc(t["donut_type"])}">
  <div class="ar-visual-hd"><span>{esc(t["donut_type"])}</span><h3>{esc(t["donut_title"])}</h3></div>
  <div class="ar-visual-bd">
    <p class="ar-visual-note">{esc(t["donut_note"])}</p>
    <div class="ar-donut-wrap">
      <div class="ar-donut" style="background:conic-gradient({", ".join(gradient)})" role="img" aria-label="{esc(t["donut_title"])}"></div>
      <div class="ar-legend">
'''
    for label, pct, color in t["donut_segments"]:
        donut += (f'        <div><i style="background:{color}"></i>{esc(label)} '
                  f'<b>{pct}%</b></div>\n')
    donut += '      </div>\n    </div>\n  </div>\n</section>\n'

    # Four-quarter confidence graph (illustrative trend).
    labels, values = t["trend_labels"], t["trend_values"]
    coordinates = []
    for idx, value in enumerate(values):
        x = 50 + idx * (500 / max(1, len(values) - 1))
        y = 180 - (value / 100) * 140
        coordinates.append((x, y))
    polyline = " ".join(f"{x:.0f},{y:.0f}" for x, y in coordinates)
    dots = "".join(
        f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4" fill="var(--accent, #0F62FE)"/>' for x, y in coordinates
    )
    axis_labels = "".join(
        f'<text x="{x:.0f}" y="205" text-anchor="middle" font-size="11" fill="var(--text-3, #8B94A8)">{esc(label)}</text>'
        for (x, _y), label in zip(coordinates, labels)
    )
    value_labels = "".join(
        f'<text x="{x:.0f}" y="{y - 12:.0f}" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-strong, #0043CE)">{value}</text>'
        for (x, y), value in zip(coordinates, values)
    )
    trend = f'''
<section class="ar-visual" aria-label="{esc(t["trend_type"])}">
  <div class="ar-visual-hd"><span>{esc(t["trend_type"])}</span><h3>{esc(t["trend_title"])}</h3></div>
  <div class="ar-visual-bd">
    <p class="ar-visual-note">{esc(t["trend_note"])}</p>
    <div class="ar-trend">
      <svg viewBox="0 0 600 220" role="img" aria-label="{esc(t["trend_title"])}">
        <line x1="40" y1="40" x2="580" y2="40" stroke="var(--border, #DFE5F5)" stroke-width="1"/>
        <line x1="40" y1="110" x2="580" y2="110" stroke="var(--border, #DFE5F5)" stroke-width="1"/>
        <line x1="40" y1="180" x2="580" y2="180" stroke="var(--border, #DFE5F5)" stroke-width="1"/>
        <polyline points="{polyline}" fill="none" stroke="var(--accent, #0F62FE)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
        {dots}
        {axis_labels}
        {value_labels}
      </svg>
    </div>
  </div>
</section>
'''

    lead = f'''
<div class="ar-lead-inline">
  <span class="ar-lead-label">{esc(t["lead_label"])}</span>
  <h3>{esc(t["lead_title"])}</h3>
  <p>{esc(t["lead_text"])}</p>
  <a class="ar-btn" href="{t["prefix"]}/contact">{esc(t["lead_btn"])}</a>
  <a class="ar-link-inline" href="{t["prefix"]}/readiness">{esc(t["lead_link"])}</a>
</div>
'''
    faq = ''
    for idx, (question, answer_text) in enumerate(t["faq_extra"], start=4):
        faq += (f'                    <div class="faq-item">\n'
                f'                        <button class="faq-question" aria-expanded="false"><span class="faq-question-text">'
                f'<span class="faq-number">{idx}</span><span>{esc(question)}</span></span></button>\n'
                f'                        <div class="faq-answer" role="region"><div class="faq-answer-inner">{esc(answer_text)}</div></div>\n'
                f'                    </div>\n')
    return {
        "answer": answer, "takeaways": takeaways, "flow": flow,
        "bars": bars, "matrix": matrix, "donut": donut, "trend": trend,
        "road": road, "lead": lead, "faq": faq,
    }


def prepare_body(lang: str, src: str) -> tuple[str, str, int]:
    t = I18N[lang]
    start = src.find('<article class="article-content" id="article-content">')
    if start == -1:
        raise RuntimeError(f"article container missing: {lang}")
    start = src.find('>', start) + 1
    end = src.find('</article>', start)
    body = src[start:end]

    # Remove legacy TOC block and in-body JSON-LD (the v9 head owns schema).
    body = re.sub(r'<div class="toc-mobile".*?</div>\s*</div>', '', body, flags=re.S)
    body = re.sub(r'<script type="application/ld\+json">.*?</script>', '', body, flags=re.S)
    body = re.sub(r'<div class="article-share".*?</div>', '', body, flags=re.S)

    blocks = build_blocks(lang)

    # Answer-first + takeaways + workflow after the first lead paragraph.
    lead_end = body.find('</p>')
    if lead_end == -1:
        raise RuntimeError(f"lead paragraph missing: {lang}")
    lead_end += 4
    body = body[:lead_end] + blocks["answer"] + blocks["takeaways"] + blocks["flow"] + body[lead_end:]

    # Insert contextual visuals by H2 ordinal, independent of translated IDs.
    h2_matches = list(re.finditer(r'<h2[^>]*>.*?</h2>', body, flags=re.S))
    if len(h2_matches) < 4:
        raise RuntimeError(f"not enough H2 sections: {lang} ({len(h2_matches)})")
    faq_index = None
    for idx, match in enumerate(h2_matches):
        heading = strip_tags(match.group())
        if any(marker in heading for marker in ('常见', '常見', 'FAQ', 'Frequently', 'questions', '问题', '問題')):
            faq_index = idx
            break
    if faq_index is None:
        faq_index = len(h2_matches) - 1

    insertion = {}

    def place(index: int, fragment: str) -> None:
        target = index if index < faq_index else faq_index
        position = h2_matches[target].start()
        insertion.setdefault(position, []).append(fragment)

    place(1, blocks["bars"])
    place(3, blocks["matrix"])
    if len(h2_matches) > 4:
        place(4, blocks["donut"])
    else:
        place(faq_index, blocks["donut"])
    if len(h2_matches) > 5:
        place(5, blocks["trend"])
    else:
        place(faq_index, blocks["trend"])
    place(faq_index, blocks["road"] + blocks["lead"])

    for position in sorted(insertion, reverse=True):
        body = body[:position] + "".join(insertion[position]) + body[position:]

    # Add three GEO answer targets to the visible FAQ.
    anchor = re.search(r'</section>\s*(?:<script|<nav class="article-nav")', body)
    if anchor:
        pos = anchor.start()
        body = body[:pos] + blocks["faq"] + body[pos:]
    else:
        body = body.replace('</article>', blocks["faq"] + '</article>')

    # TOC from the source article's own headings, so every language is native.
    h2_after = list(re.finditer(r'<h2([^>]*)>(.*?)</h2>', body, flags=re.S))
    toc_items = []
    for idx, match in enumerate(h2_after[:7], start=1):
        id_match = re.search(r'\bid="([^"]+)"', match.group(1))
        if not id_match:
            continue
        label = strip_tags(match.group(2))
        label = label if len(label) <= 46 else label[:43] + '…'
        toc_items.append((id_match.group(1), label, idx))
    toc_html = f'<span class="ar-toc-label">{esc(t["toc_label"])}</span>\n'
    for target_id, label, idx in toc_items:
        toc_html += f'          <a href="#{esc(target_id)}"><span>{idx:02d}</span>{esc(label)}</a>\n'

    plain = strip_tags(body)
    if lang == "en":
        count = len(re.findall(r"[A-Za-z0-9]+(?:[’'\-][A-Za-z0-9]+)*", plain))
        count_label = f'{count:,} {t["words_unit"]}'
    else:
        count = len(re.sub(r'\s', '', plain))
        count_label = f'{count:,} {t["words_unit"]}'
    read_min = max(1, round(count / 240 if lang == "en" else count / 420))
    return body, toc_html, count, count_label, read_min


def related_html(lang: str) -> str:
    t = I18N[lang]
    out = f'<section class="ar-related" id="related-articles"><h3>{esc(t["related_label"])}</h3><div class="ar-related-grid">\n'
    for slug in t["related_slugs"]:
        source = SRC[lang].parent / f"{slug}.html"
        if not source.exists():
            continue
        raw = source.read_text(errors="ignore")
        match = re.search(r'<title>(.*?)</title>', raw, re.S)
        title = html.unescape(match.group(1)).strip() if match else slug
        title = re.sub(r'\s*\|\s*Beehive Strategy\s*$', '', title).strip()
        image = f'/assets/blog/social/{lang}/{slug}.jpg?v={ASSET_V}'
        href = f'{t["prefix"]}/blog/articles/{slug}'
        out += (f'      <a href="{href}"><img src="{image}" alt="{esc(title)}" loading="lazy">'
                f'<span>{esc(title)}</span></a>\n')
    out += '    </div></section>\n'
    return out


def build(lang: str) -> Path:
    t = I18N[lang]
    source = SRC[lang].read_text(errors="ignore")
    body, toc_html, count, count_label, read_min = prepare_body(lang, source)

    raw_title = re.search(r'<title>(.*?)</title>', source, re.S)
    title = html.unescape(raw_title.group(1)).strip() if raw_title else SLUG
    title = re.sub(r'\s*\|\s*Beehive Strategy\s*$', '', title).strip()
    raw_desc = re.search(r'<meta name="description" content="(.*?)">', source, re.S)
    desc = html.unescape(raw_desc.group(1)).strip() if raw_desc else title
    date_raw = re.search(r'"datePublished"\s*:\s*"([^"]+)"', source)
    date_iso = date_raw.group(1)[:10] if date_raw else "2026-04-25"

    blog_url = f'{SITE}{t["prefix"]}/blog'
    canon = f'{SITE}{t["prefix"]}/blog/articles/{SLUG}'
    image = f'{SITE}/assets/blog/social/{lang}/{SLUG}.jpg?v={ASSET_V}'
    org = {"@type": "Organization", "name": "Beehive Strategy", "url": SITE}
    faq_questions = []
    for question, answer in t["faq_extra"]:
        faq_questions.append({"@type": "Question", "name": question,
                              "acceptedAnswer": {"@type": "Answer", "text": answer}})
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Article", "headline": title, "description": desc,
             "mainEntityOfPage": canon, "author": org, "publisher": org, "image": image,
             "datePublished": date_iso, "dateModified": "2026-11-22",
             "inLanguage": t["html_lang"], "wordCount": count},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Insights", "item": blog_url},
                {"@type": "ListItem", "position": 3, "name": title, "item": canon}]},
            {"@type": "HowTo", "name": t["flow_title"], "description": t["answer"],
             "step": [{"@type": "HowToStep", "position": i + 1, "name": step[1], "text": step[2]}
                      for i, step in enumerate(t["flow"])]},
            {"@type": "FAQPage", "mainEntity": faq_questions},
        ],
    }

    head = f'''<!DOCTYPE html>
<html lang="{t["html_lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | Beehive Strategy</title>
<link rel="stylesheet" href="/css/accenture.css?v=20261118.06">
<link rel="stylesheet" href="/css/legacy-bridge.css?v=20261120.03">
<link rel="stylesheet" href="/css/article-layout.css?v={ASSET_V}">
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canon)}">
<link rel="alternate" hreflang="en" href="{SITE}/blog/articles/{SLUG}">
<link rel="alternate" hreflang="zh-cn" href="{SITE}/zh-cn/blog/articles/{SLUG}">
<link rel="alternate" hreflang="zh-hk" href="{SITE}/zh-hk/blog/articles/{SLUG}">
<link rel="alternate" hreflang="x-default" href="{SITE}/blog/articles/{SLUG}">
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
<meta property="article:published_time" content="{date_iso}">
<meta property="article:modified_time" content="2026-11-22">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</head>
'''

    share_links = [
        f'<a id="share-linkedin" href="#">{esc(t["share"][0])}</a>',
        f'<a id="share-x" href="#">{esc(t["share"][1])}</a>',
        f'<a id="share-whatsapp" href="#">{esc(t["share"][2])}</a>',
        f'<a id="share-facebook" href="#">{esc(t["share"][3])}</a>',
        f'<button id="share-copy" type="button" data-copy-msg="{esc(t["copy_msg"])}">{esc(t["share"][4])}</button>',
    ]
    visual_count = body.count('class="ar-visual"') + body.count('class="article-figure"')
    main = f'''
<main role="main" class="ar-page">
  <div class="ar-wrap">
    <nav class="ar-eyebrow" aria-label="Section"><a href="{blog_url}">{esc(t["eyebrow_home"])}</a><span class="ar-sep">/</span><span>{esc(t["eyebrow_section"])}</span></nav>
    <header class="ar-masthead">
      <span class="ar-kicker">{esc(t["kicker"])}</span>
      <h1 class="ar-title">{esc(title)}</h1>
      <div class="ar-meta"><span class="ar-avatar">BS</span><span class="ar-author">Beehive Strategy</span>
        <span class="ar-dot">·</span><time datetime="{date_iso}">{esc(t["date"])}</time>
        <span class="ar-dot">·</span><span>{esc(count_label)}</span>
        <span class="ar-dot">·</span><span>{read_min} {esc(t["read_time"])}</span></div>
      <div class="ar-share" aria-label="{esc(t["share_label"])}">
        <span class="ar-share-label">{esc(t["share_label"])}</span>
        {''.join(share_links)}
      </div>
    </header>
    <div class="ar-grid">
      <aside class="ar-rail">
        <nav class="ar-toc" aria-label="{esc(t["toc_label"])}">
          {toc_html}
        </nav>
        <a class="ar-rail-cta" href="{t["prefix"]}/readiness">{esc(t["rail_cta"])}</a>
      </aside>
      <article class="ar-body">
{body}
        <section class="ar-lead-end">
          <h3>{esc(t["paths_title"])}</h3>
          <div class="ar-paths">
'''
    for num, title_path, text, go in t["paths"]:
        href = {
            0: f'{t["prefix"]}/readiness',
            1: f'{t["prefix"]}/proof',
            2: f'{t["prefix"]}/contact',
        }[t["paths"].index((num, title_path, text, go))]
        main += (f'            <a class="ar-path" href="{href}"><span class="ar-path-num">{esc(num)}</span>'
                 f'<h4>{esc(title_path)}</h4><p>{esc(text)}</p>'
                 f'<span class="ar-path-go">{esc(go)}</span></a>\n')
    main += '''          </div>
        </section>
'''
    main += related_html(lang)
    main += '''      </article>
    </div>
  </div>
</main>
'''

    body_start = source.find('<body')
    if body_start == -1:
        raise RuntimeError(f"body missing: {lang}")
    body_open_end = source.find('>', body_start) + 1
    main_start = source.find('<main')
    main_end = source.find('</main>', main_start) + len('</main>')
    shell_before = source[body_open_end:main_start]
    shell_after = source[main_end:]

    # v9 removes the floating back-to-top control from the article experience.
    shell_after = re.sub(
        r'<button class="back-to-top"[^>]*>.*?</button>', '', shell_after, flags=re.S
    )

    # Keep the native site header/footer of each language; add v9 layout JS.
    shell_after = shell_after.replace('</body>',
        '<script src="/js/article-layout.js?v=' + ASSET_V + '"></script>\n</body>')
    if '/js/article-layout.js' not in shell_after:
        shell_after = shell_after.replace('</html>',
            '<script src="/js/article-layout.js?v=' + ASSET_V + '"></script>\n</html>')

    final = head + source[body_start:body_open_end] + shell_before + main + shell_after
    out = OUT[lang]
    out.write_text(final)
    print(f'{lang:6} -> {out.name:34} bytes={len(final):6} words/chars={count:5} visuals={visual_count}')
    return out


if __name__ == "__main__":
    for language in ("en", "zh-cn", "zh-hk"):
        build(language)
