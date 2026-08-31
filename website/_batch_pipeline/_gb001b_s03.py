#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""slug 03: conversational-bi-market-report-mid-2025
EN 1504 -> target 2700+ ; zh already long enough, only H2 -> question form."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gb001b_lib import run, path_of, retitle_h2

SLUG = "conversational-bi-market-report-mid-2025"

EN_NEWS = """<h2 id="how-should-buyers-evaluate-vendors">How Should Buyers Evaluate Vendors in a Crowded Market?</h2>
<p>Vendor evaluation in 2025 is harder than the capability comparison suggests, because component-level capability has converged. NLU accuracy, chart generation, and multi-turn context are broadly comparable across serious vendors, which means the differentiating questions are the ones least visible in a demo. The first is semantic layer depth: can the vendor model a metric with conformed dimensions, row-level security, and a documented grain, or does it generate SQL directly against tables and hope the schema is self-explanatory? That answer predicts answer quality far better than any published benchmark, and it is testable in the first meeting — bring three of your own ambiguous business questions, with your own definitions, and see whether the vendor asks about the definitions or produces a number immediately. A vendor that produces a number immediately is showing you the failure mode, not the capability.</p>
<p>The second differentiating question is channel coverage and identity propagation: does the product follow your users into Teams, WeChat Work, Slack, or wherever decisions are actually made, and does it carry the same row-level permissions into that channel? A conversational interface that lives in a separate tab and enforces weaker permissions than the warehouse is a compliance incident waiting for a screenshot. The third is evaluation and governance tooling — can you see which questions were asked, which failed silently, and which answers users corrected? Buyers who cannot audit their own deployment cannot improve it, and the vendors that ship this tooling are the ones whose customers report durable adoption rather than a strong first month followed by quiet abandonment.</p>
<p>Finally, interrogate the deployment methodology rather than the licence. Ask for the reference architecture, the typical semantic layer effort for a first thirty-question release, and the named owners on both sides for the first ninety days. Vendors with a segment playbook — the FP&amp;A or sales operations patterns described above — can usually answer all three without preparation, and that fluency is the most reliable proxy available for whether the programme will still be in use a year later.</p>
<h2 id="what-do-the-unit-economics-look-like">What Do the Unit Economics of a Deployment Actually Look Like?</h2>
<p>The market's headline growth rates invite a question that most vendor material avoids: what does a deployment cost, and what does it return? The honest answer splits into three cost pools. The semantic layer is the largest and the least avoidable — scoping, defining, and testing the first twenty to thirty metrics with their dimensions and permissions is the bulk of the initial effort, and it is the work that determines whether the tool is trusted at all. Integration and security work is the second: identity propagation, row-level security testing, audit logging, and the channel integrations that place the assistant where users already work. The third is ongoing operating cost — evaluation, metric change management, and maintenance of the question catalogue as the business changes underneath it.</p>
<p>Against those costs sit three return lines, and putting them in the same units is what separates a funded programme from a stalled pilot. Analyst time returned is the most direct: if a team of eight analysts spends a measurable share of its week on repetitive questions, and conversational BI absorbs even half of that load, the recovered capacity is a hard number in the business case. Decision latency is the second and often the larger one — the three-to-five business day wait for an unanticipated question is a real cost when the decision is operational, and compressing it to minutes changes what the business can do, not merely what it spends. Adoption is the third, and it is the leading indicator: weekly active question askers as a share of the licensed population predicts renewal value better than any feature comparison.</p>
<p>The arithmetic that makes or breaks the business case is the ratio of question volume to semantic coverage. A deployment whose top thirty questions account for the large majority of inbound demand reaches break-even quickly, because a modest semantic investment absorbs a large share of the workload. A deployment facing a long tail of one-off questions does not, and the right response is to narrow the scope rather than to widen the licence. This is why the segment concentration described earlier matters commercially as well as technically: buyers should size the opportunity against their own question distribution before they size it against the market.</p>
<h2 id="why-do-deployments-disappoint-after-a-strong-pilot">Why Do Some Deployments Disappoint After a Strong Pilot?</h2>
<p>The pattern is consistent enough to be worth naming: a well-received pilot, enthusiastic early users, a licence expansion — and then flat or declining usage by month six. Three causes account for most of it. The first is the coverage ceiling. The pilot answered the twenty questions that were modelled, users discovered the boundary within weeks, and expansion of the semantic layer was never funded beyond the pilot. Adoption plateaus exactly where the question catalogue stops growing, because users who have been burned once by an out-of-scope question stop asking. The remedy is a funded coverage backlog with a published cadence, so that the boundary visibly moves rather than feeling fixed.</p>
<p>The second cause is unmanaged answer quality. A conversational tool that is right 85% of the time, with no visible provenance, will be distrusted about as quickly as one that is right half the time — because users cannot tell which 15% to doubt. Deployments that surface the definition behind a number, that let a user see a metric's grain and filters, and that make it easy to flag a wrong answer, retain trust through the errors that every system makes. The third cause is the absence of an owner. Conversational BI sits between data, IT, and the business, and when no single role is accountable for the question catalogue, the metric definitions, and the escalation path, the artefacts decay: definitions drift from the warehouse, unanswered questions pile up, and usage quietly returns to the old analyst queue.</p>
<p>Deployments that avoid all three share a simple operating rhythm: a weekly review of unanswered and low-confidence questions, a monthly release of new semantic coverage against a published backlog, and a named owner with the authority to ratify metric definitions. None of this is technically difficult; all of it is organisational. That is the real content of the mid-2025 market picture — the technology has crossed the credibility threshold, and what separates the winners of the next cycle is operating discipline rather than model quality.</p>
<h2 id="what-should-enterprises-do-with-this-report">What Should Enterprises Do With This Report?</h2>
<p>Three actions follow from the mid-2025 picture, and they are ordered deliberately. First, audit your question inventory before you evaluate vendors: pull three months of analyst tickets and internal data requests, bucket them by frequency, and identify the top twenty to thirty questions. That list is the specification for your semantic layer, the basis of your business case, and the only fair way to compare vendors — because a demo against a vendor's sample data tells you nothing about your own distribution.</p>
<p>Second, fund the semantic foundation as a programme rather than a project line. The organisations seeing durable adoption in 2025 treated metric definition as a continuing capability with an owner and a backlog, not as a one-off implementation task. Third, decide the channel question early. If your users live in WeChat Work, Teams, or Slack, the conversational interface should meet them there with full permission propagation, and that requirement belongs in the first vendor conversation rather than the second-year roadmap — retrofitting identity and row-level security into a channel integration costs far more than designing it in from the start.</p>
<p>Enterprises that take these three steps convert a market report into a plan. Those that skip them tend to buy capability they cannot operationalise, and the mid-2025 data suggests they will not be alone: the category's growth is real, but so is the gap between licence purchases and durable adoption, and that gap is where most of the disappointment in the next cycle will be concentrated.</p>
"""

# ---- zh-CN H2 -> question form (ids preserved) ----
CN_H2 = [
    ("传统bi的局限性与变革的理由", "传统BI的局限性与变革的理由", "传统BI仪表板为何走到了极限？"),
    ("核心技术组件", "核心技术组件", "2025年对话式BI的核心技术组件有哪些？"),
    ("实施策略与最佳实践", "实施策略与最佳实践", "什么样的实施策略能带来成功？"),
    ("对话式bi的进阶能力与未来演进", "对话式BI的进阶能力与未来演进", "对话式BI的进阶能力将如何演进？"),
    ("对话式bi技术架构深度解析", "对话式BI技术架构深度解析", "对话式BI的技术架构是如何构成的？"),
    ("战略实施路径与关键成功因素", "战略实施路径与关键成功因素", "战略实施路径上的关键成功因素是什么？"),
    ("企业实施路线图与成功因素", "企业实施路线图与成功因素", "企业应如何规划对话式BI的实施路线图？"),
    ("行业数字化转型深度分析", "行业数字化转型深度分析", "行业数字化转型的深层动力是什么？"),
]

# ---- zh-TW H2 -> question form (ids preserved) ----
TW_H2 = [
    ("傳統bi的局限性與變革的理由", "傳統BI的局限性與變革的理由", "傳統BI儀表板為何走到了極限？"),
    ("核心技術組件", "核心技術組件", "2025年對話式BI的核心技術組件有哪些？"),
    ("實施策略與最佳實踐", "實施策略與最佳實踐", "什麼樣的實施策略能帶來成功？"),
    ("對話式bi的進階能力與未來演進", "對話式BI的進階能力與未來演進", "對話式BI的進階能力將如何演進？"),
    ("對話式bi技術架構深度解析", "對話式BI技術架構深度解析", "對話式BI的技術架構是如何構成的？"),
    ("戰略實施路徑與關鍵成功因素", "戰略實施路徑與關鍵成功因素", "戰略實施路徑上的關鍵成功因素是什麼？"),
    ("企業實施路線圖與成功因素", "企業實施路線圖與成功因素", "企業應如何規劃對話式BI的實施路線圖？"),
    ("行業數位轉型深度分析", "行業數位轉型深度分析", "行業數位轉型的深層動力是什麼？"),
]

# ---- EN H2 -> question form (ids preserved) ----
EN_H2 = [
    ("the-limits-of-traditional-bi-and-the-case-for-change",
     "The Limits of Traditional BI and the Case for Change",
     "Why Are Traditional BI Dashboards Hitting Their Limits?"),
    ("core-technology-components", "Core Technology Components",
     "What Core Technology Components Define Conversational BI in 2025?"),
    ("implementation-strategy-and-best-practices", "Implementation Strategy and Best Practices",
     "What Implementation Strategy Separates Success From Disappointment?"),
    ("segment-by-segment-where-growth-is-concentrated",
     "Segment-by-Segment: Where Growth Is Concentrated",
     "Which Market Segments Are Driving Growth?"),
    ("in-depth-analysis-of-conversational-bi-technical-architecture",
     "In-Depth Analysis of Conversational BI Technical Architecture",
     "How Is Conversational BI Architecture Evolving?"),
]

if __name__ == "__main__":
    en = path_of(SLUG, "en")
    h = open(en, encoding="utf-8").read()
    anchor = '            <section class="faq-section"'
    assert h.count(anchor) == 1
    h = h.replace(anchor, "\n" + EN_NEWS + "\n" + anchor)
    open(en, "w", encoding="utf-8").write(h)
    print("EN body expanded")

    for hid, old, new in EN_H2:
        retitle_h2(en, hid, old, new)
    for hid, old, new in CN_H2:
        retitle_h2(path_of(SLUG, "cn"), hid, old, new)
    for hid, old, new in TW_H2:
        retitle_h2(path_of(SLUG, "tw"), hid, old, new)
    print("H2s converted in en/cn/tw")
