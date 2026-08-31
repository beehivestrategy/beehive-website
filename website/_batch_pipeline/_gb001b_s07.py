#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""slug 07: conversational-bi-manufacturing-year-end-nov2025
EN 1669 -> ~2700 ; CN/TW already long enough ; H2 -> questions in all 3."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gb001b_lib import path_of, retitle_by_text

SLUG = "conversational-bi-manufacturing-year-end-nov2025"

EN_NEWS = """<h2 id="how-do-you-get-oee-right-across-plants">How Do You Get OEE Right Across Multiple Plants?</h2>
<p>OEE is the metric that makes or breaks a manufacturing year-end review, and it is also the one most likely to be quietly inconsistent. The formula is standard — availability multiplied by performance multiplied by quality — but every one of the three terms hides a decision that plants make differently. Is planned maintenance counted as available time? Is the performance denominator the machine's nameplate rate or the historically achieved rate? Is a startup scrap counted against quality, or excluded as a changeover cost? Two plants can each be correct by their own convention and differ by eight or ten points, which is far more than the improvement any initiative is expected to deliver.</p>
<p>The consequence for a year-end review is severe: if OEE is not comparable, the review cannot compare plants, and the capital plan is allocated on numbers that would not survive scrutiny. This is precisely the problem a semantic layer exists to solve, and the reason it must come before the conversational interface rather than after. The work is unglamorous — sit down with the plant managers, write down the convention for each term, decide the exceptions, and encode all of it once. The output is a definition with a named owner and a documented grain, which every dashboard, export, and conversational answer then inherits.</p>
<p>Two practical rules make the exercise finish. First, define the exceptions explicitly rather than hoping they do not arise: what happens on a line that ran a trial, during a changeover, or after a maintenance window. Undocumented exceptions are how definitions drift back apart within a year. Second, publish the definition where users can read it, not only query it. A plant manager who can see how availability is calculated will argue about the convention in the definition review — where the argument belongs — instead of in the leadership meeting, where it derails the review.</p>
<h2 id="what-does-a-review-look-like-when-it-works">What Does a Year-End Review Look Like When It Works?</h2>
<p>The difference is easiest to see as a sequence. In the traditional version, an analyst assembles the deck over three weeks, the leadership meeting works through it slide by slide, and roughly a third of the questions raised cannot be answered in the room. Those questions become follow-up actions, the follow-ups take another week each, and by the time they are answered the review's momentum has gone. The output is a document that was accurate on the day it was assembled and a list of open items that nobody revisits.</p>
<p>In the conversational version, the same meeting runs on live data. The review opens with OEE by line for the year; someone asks why the packaging line dropped in October; the answer decomposes into availability and shows a specific failure mode concentrated on the night shift; the next question pulls the maintenance history for the asset involved; and within ninety seconds the meeting has a hypothesis, an owner, and a number attached to the cost of the downtime. The follow-up question is answered while the discussion is still about that topic, which changes what the review can cover in the time available.</p>
<p>The cultural effect is larger than the time saved. When answers are immediate and consistent, the review stops being a defence of each plant's numbers and becomes an examination of what the plants should do next. Plant managers arrive with questions rather than slides. Disagreements surface as definitional gaps to be fixed in the semantic layer, which is a productive outcome, rather than as accusations of cherry-picking. Reviews run this way tend to produce fewer, better-documented decisions — and because the questions are captured, next year's review starts with an established question catalogue instead of a blank page.</p>
<h2 id="how-do-you-extend-it-beyond-year-end">How Do You Extend Conversational BI Beyond the Year-End Review?</h2>
<p>Year-end is the entry point, not the destination, and the extension path is fairly standard across manufacturers. The first expansion is the monthly operating review, which uses the same metrics and the same definitions, and therefore requires no additional modelling — the only work is onboarding the next group of users. The second is the daily shift handover, where the questions are narrower and more operational: what ran short yesterday, what is down now, which work orders are overdue. This is the highest-frequency use and the one that changes daily behaviour most, because it puts the same governed numbers in front of the people who act on them within minutes.</p>
<p>The third expansion is planning and capital. Once a year of conversational traffic exists, the question log itself becomes an input to the capital plan: the assets that generated the most downtime questions, the lines whose yield questions recur, the product families that dominate quality enquiries. That evidence is more persuasive than a slide, because it reflects what the organisation actually needed to know rather than what a report template happened to include. The fourth is cross-plant benchmarking, which becomes reliable only after the definitions are aligned — and which is often the point at which the semantic layer work pays for itself a second time.</p>
<p>The risk in extending is scope creep in the semantic layer. Each new use case tempts the team to model more metrics before the existing ones are stable, and coverage breadth bought before depth produces the exact inconsistency that killed trust in the first place. The discipline that holds is simple: extend to a new audience on the metrics you already trust, and add new metrics only when a recurring question cannot be answered with what exists. Manufacturers who follow that order end the second year with a broad, trusted catalogue; those who invert it end up with a wide layer that nobody relies on.</p>
"""

EN_H2 = [
    ("Why the Year-End Review Is the Perfect Conversational BI Use Case",
     "Why Is the Year-End Review the Perfect Conversational BI Use Case?"),
    ("Key Benefits and ROI Considerations",
     "What Benefits and ROI Should Manufacturers Expect?"),
    ("Implementation Roadmap and Next Steps",
     "What Does the Implementation Roadmap Look Like?"),
]

CN_H2 = [
    ("核心收益与投资回报考量", "制造企业应当期待哪些收益与投资回报？"),
    ("实施路线图与后续步骤", "对话式BI的实施路线图应当如何安排？"),
    ("常见问题解答", "从业者最常问的问题有哪些？"),
    ("案例分析与行业洞察", "有哪些值得参考的案例与行业洞察？"),
    ("未来展望与行动建议", "未来展望与行动建议是什么？"),
    ("关键成功因素与常见陷阱", "关键成功因素与常见陷阱有哪些？"),
    ("蜂启咨询的专业洞察", "蜂启咨询有哪些专业洞察？"),
]

TW_H2 = [
    ("核心收益與投資回報考量", "製造企業應當期待哪些收益與投資回報？"),
    ("實施路線圖與後續步驟", "對話式BI的實施路線圖應當如何安排？"),
    ("常見問題解答", "從業者最常問的問題有哪些？"),
    ("案例分析與行業洞察", "有哪些值得參考的案例與行業洞察？"),
    ("未來展望與行動建議", "未來展望與行動建議是什麼？"),
    ("關鍵成功因素與常見陷阱", "關鍵成功因素與常見陷阱有哪些？"),
    ("蜂啓諮詢的專業洞察", "蜂啓諮詢有哪些專業洞察？"),
]

if __name__ == "__main__":
    en = path_of(SLUG, "en")
    h = open(en, encoding="utf-8").read()
    anchor = '            <section class="faq-section"'
    assert h.count(anchor) == 1
    h = h.replace(anchor, "\n" + EN_NEWS + "\n" + anchor)
    open(en, "w", encoding="utf-8").write(h)
    print("EN body expanded")

    for old, new in EN_H2:
        retitle_by_text(en, old, new)
    for old, new in CN_H2:
        retitle_by_text(path_of(SLUG, "cn"), old, new)
    for old, new in TW_H2:
        retitle_by_text(path_of(SLUG, "tw"), old, new)
    print("H2s converted in en/cn/tw")
