#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""slug 06: enterprise-ai-adoption-roadmap-2025-midyear
EN 1559 -> ~2700 ; CN/TW already long enough ; H2 -> questions in all 3."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gb001b_lib import path_of, retitle_h2

SLUG = "enterprise-ai-adoption-roadmap-2025-midyear"

EN_NEWS = """<h2 id="how-do-you-run-an-honest-portfolio-triage">How Do You Run an Honest Portfolio Triage?</h2>
<p>Triage is conceptually simple and politically difficult, and the difficulty is the reason so few organisations do it properly. The mechanics are three columns: for every AI initiative, record the value it has delivered so far, the breadth of its current adoption, and its fully loaded cost including the people who keep it running. Then sort into three buckets — scale, fix, or kill. The discipline is that every initiative lands in exactly one bucket, and the list is published to the same leadership group that sponsored the initiatives in the first place.</p>
<p>The scoring rubric matters more than the meeting. On value, accept only outcomes that a named owner will sign for: cycle time reduced, cost avoided, revenue attributed, risk events prevented. On adoption, use weekly active usage against the intended population, not licences issued and not logins — a pilot used by eleven enthusiasts is a pilot, not a capability. On cost, include the hidden half: the data engineering that keeps the pipeline alive, the analyst time spent reconciling outputs, and the vendor spend that renews automatically. Initiatives that look cheap because an enthusiastic team absorbed the cost informally are the ones that surprise the budget later.</p>
<p>Two political failure modes recur. The first is the zombie pilot: no adoption, no measured value, but a senior sponsor who is fond of it. The remedy is to move the burden of proof — a zombie survives one more quarter only if its sponsor produces a named business owner and a baseline to measure against. The second is the pet project that is genuinely promising but sits outside any business unit's plan; these should be adopted by a function with a budget line or killed, because an initiative with no owning function has no path to production. Publishing the list is what makes both conversations possible without making them personal.</p>
<h2 id="what-does-minimum-viable-ai-governance-contain">What Does Minimum Viable AI Governance Actually Contain?</h2>
<p>Governance is where mid-year roadmaps most often stall, because teams picture a lengthy policy document and defer it. Minimum viable governance is much smaller than that, and it consists of five decisions that can be made in a fortnight. Who approves a new AI use case, and on what evidence. Which data may be used, and which is off limits regardless of the use case. How outputs are validated before they reach a decision — sampling, human review, or automated checks, and at what rate. How incidents are escalated, including who can switch a system off. And what is logged, so that a decision can be reconstructed months later.</p>
<p>None of these require new technology, and all of them are cheaper to establish now than after an incident. The approval decision is the keystone: a single intake route, with a lightweight review that scales scrutiny to risk — a low-risk internal summarisation tool passes in days, a customer-facing decisioning system goes through a fuller review. The data decision should be expressed as allowed categories rather than a list of systems, because system lists go stale immediately. Validation should be explicit about the human role, since regulators and internal audit will ask whether a person reviewed the output before it mattered.</p>
<p>The mistake to avoid is writing governance as a policy nobody reads and a committee that never meets. The test of minimum viable governance is throughput: how quickly a legitimate new use case gets approval. If the answer is weeks, teams will route around it, and the programme loses visibility of what is actually running. Governance that takes two days and is respected is worth far more than governance that takes two months and is evaded.</p>
<h2 id="why-do-successful-pilots-fail-to-scale">Why Do Pilots That Look Successful Fail to Scale?</h2>
<p>The pattern has a name in most enterprises: a pilot that demonstrated clear value in a controlled setting, won executive applause, received expansion funding — and then quietly plateaued. Four causes explain most of it. The first is that the pilot was subsidised. The two engineers who built it are not available to fifty business units, the data was hand-prepared in ways nobody documented, and the happy path was the only path tested. Remove the subsidy and the economics change completely, which is why production adoption never matches pilot enthusiasm.</p>
<p>The second cause is the absence of an operating model. A pilot is run by enthusiasts; a capability is run by a team with a rota, a support queue, a documented onboarding process, and a budget. Most pilots are promoted without any of these, and the first production incident has no owner. The third cause is data readiness: the pilot ran on a curated extract, and production requires the full pipeline with its quality problems, access controls, and refresh schedules. The fourth is change resistance that was never planned for — the pilot's users volunteered, while production users did not, and adoption programmes are routinely underfunded relative to the technology.</p>
<p>The countermeasure is to treat scale as a distinct phase with its own gate. Before an initiative is promoted, require a documented operating model with a named owner and support path, a production data lineage rather than an extract, a cost model at target scale, and an adoption plan for users who did not volunteer. Initiatives that clear that gate tend to scale; those that skip it tend to produce the exact plateau the Gartner abandonment statistic describes.</p>
"""

EN_H2 = [
    ("the-strategic-imperative-for-enterprise-ai-in-2025",
     "The Strategic Imperative for Enterprise AI in 2025",
     "Why Is Mid-2025 the Moment to Consolidate Rather Than Experiment?"),
    ("framework-for-ai-strategy-development", "Framework for AI Strategy Development",
     "What Does a Mid-Year AI Strategy Framework Contain?"),
    ("measuring-success-and-demonstrating-roi", "Measuring Success and Demonstrating ROI",
     "How Should You Measure Success and Demonstrate ROI?"),
    ("the-conversational-analytics-fast-track", "The Conversational Analytics Fast Track",
     "Why Does Conversational Analytics Deserve a Fast Track?"),
    ("implementation-roadmap-and-key-success-factors",
     "Implementation Roadmap and Key Success Factors",
     "What Does the Implementation Roadmap Require in Q3 and Q4?"),
]

CN_H2 = [
    ("2025年企业ai的战略紧迫性", "2025年企业AI的战略紧迫性", "为什么2025年年中是整合而非试点的时刻？"),
    ("ai战略开发框架", "AI战略开发框架", "年中AI战略框架应包含哪些内容？"),
    ("衡量成功与展示投资回报", "衡量成功与展示投资回报", "应当如何衡量成功并证明投资回报？"),
    ("实施路径与组织准备", "实施路径与组织准备", "实施路径与组织准备应包含什么？"),
    ("战略实施路径与关键成功因素", "战略实施路径与关键成功因素", "战略实施路径的关键成功因素是什么？"),
    ("战略实施路径与关键成功因素-2", "战略实施路径与关键成功因素", "哪些关键成功因素决定整合成效？"),
    ("企业实施路线图与成功因素", "企业实施路线图与成功因素", "企业应如何规划AI实施路线图？"),
    ("行业数字化转型深度分析", "行业数字化转型深度分析", "行业数字化转型的深层动力是什么？"),
]

TW_H2 = [
    ("2025年企業ai的戰略緊迫性", "2025年企業AI的戰略緊迫性", "爲什麼2025年年中是整合而非試點的時刻？"),
    ("ai戰略開發框架", "AI戰略開發框架", "年中AI戰略框架應包含哪些內容？"),
    ("衡量成功與展示投資回報", "衡量成功與展示投資回報", "應當如何衡量成功並證明投資回報？"),
    ("實施路徑與組織準備", "實施路徑與組織準備", "實施路徑與組織準備應包含什麼？"),
    ("戰略實施路徑與關鍵成功因素", "戰略實施路徑與關鍵成功因素", "戰略實施路徑的關鍵成功因素是什麼？"),
    ("戰略實施路徑與關鍵成功因素-2", "戰略實施路徑與關鍵成功因素", "哪些關鍵成功因素決定整合成效？"),
    ("企業實施路線圖與成功因素", "企業實施路線圖與成功因素", "企業應如何規劃AI實施路線圖？"),
    ("行業數位轉型深度分析", "行業數位轉型深度分析", "行業數位轉型的深層動力是什麼？"),
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
