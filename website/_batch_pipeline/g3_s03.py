#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixlib as F

SLUG = "measuring-ai-maturity-enterprise-assessment-model"

EN_NEW = """
<h2 id="how-do-you-score-an-enterprise-across-the-four-dimensions">How Do You Score an Enterprise Across the Four Dimensions?</h2>
<p>A maturity model is only useful if two people score the same organization the same way. That requires a rubric of observable behaviours rather than self-reported intent. Score each dimension from 1 to 5, and require named evidence for every claim before it counts.</p>
<table>
<thead>
<tr><th>Dimension</th><th>Level 1 signal</th><th>Level 3 signal</th><th>Level 5 signal</th></tr>
</thead>
<tbody>
<tr><td>Governance</td><td>No charter; AI use is informal</td><td>Published charter, named risk owner, coverage percentage reported quarterly</td><td>Governance shapes which products the company builds, not just which are allowed</td></tr>
<tr><td>Data readiness</td><td>Data extracted manually per project</td><td>Priority workflows sit on connected, current, quality-assured data with owners</td><td>Data products are published, versioned and consumed across the business</td></tr>
<tr><td>Workflow integration</td><td>AI lives in standalone tools</td><td>Named production workflows with measured baseline-to-current deltas</td><td>Core decisions cannot be made without the AI-supported process</td></tr>
<tr><td>Capability</td><td>A few enthusiasts</td><td>Defined roles, a training path, and a support model for production systems</td><td>Building AI capability is a standing organizational competency</td></tr>
</tbody>
</table>
<p>Two scoring conventions prevent the exercise from collapsing into optimism. First, score the organization at its <em>weakest</em> dimension for any claim that depends on all four — a level 4 workflow running on level 2 data is a level 2 outcome. Second, require the evidence to be checkable by someone outside the team making the claim: a dashboard URL, a charter document, a named owner, a measured number. If the evidence cannot be produced in the session, the dimension scores one level lower.</p>
<p>The output is not a single number. It is a profile — four scores, a written justification for each, and the identification of one binding constraint. The binding constraint is the dimension that, left unchanged, makes progress in the others irrelevant. Naming it is the entire point of the assessment.</p>
<h2 id="what-does-level-3-actually-look-like-in-a-real-enterprise">What Does Level 3 Actually Look Like in a Real Enterprise?</h2>
<p>Abstract level descriptions are easy to agree with and hard to act on. Three concrete profiles make the middle of the model tangible.</p>
<p><strong>A global manufacturer at level 3 in workflow integration.</strong> Demand sensing runs in production for four product families across two regions. There is a named business owner in supply planning, a documented baseline from the eighteen months before deployment, and a standing support rota. Forecast error on those families fell 22 percent and the number is reconciled quarterly with finance. Everything else the company does with AI remains at level 2 — and that is fine, because the organization knows exactly which workflows graduated and why.</p>
<p><strong>A regional bank at level 3 in governance, level 2 in data readiness.</strong> The bank has a published model risk charter, a named owner for every deployed model, and quarterly coverage reporting to the board. But priority credit workflows still depend on extracts assembled by hand each month. The binding constraint is unambiguous, and the bank's roadmap for the following year contains exactly one funded initiative: connect and quality-assure the credit data.</p>
<p><strong>A retailer at level 4 in capability, level 2 everywhere else.</strong> The retailer has excellent people — a mature ML engineering group, a training path, internal tooling. But no workflow has a named business owner or a measured outcome, so capability is being spent on pilots that never graduate. This is the most common and most frustrating profile in the field: strong supply, weak demand. The fix is not more training; it is choosing three workflows and holding them to production.</p>
<h2 id="how-do-you-avoid-the-most-common-assessment-errors">How Do You Avoid the Most Common Assessment Errors?</h2>
<p>Four errors account for most bad maturity assessments, and all four are social rather than technical.</p>
<ul>
<li><strong>Scoring intent instead of behaviour.</strong> "We plan to establish governance" is a level 1 answer. Ask what exists today, not what is funded for next quarter.</li>
<li><strong>Letting the enthusiast score the organization.</strong> The person who built the pilot will score it generously. Include at least one sceptic from the function that has to live with the result, plus someone from risk or internal audit.</li>
<li><strong>Averaging away the constraint.</strong> A 4, 4, 2, 3 profile is not a "3.25 organization." It is a level 2 organization with three good dimensions, and reporting an average hides the only thing that needs funding.</li>
<li><strong>Assessing once and filing the result.</strong> Maturity moves. An assessment that is not repeated on a fixed cadence becomes a historical artefact within two quarters, and the next planning cycle starts from memory.</li>
</ul>
<p>The correction for all four is the same: every score must be defended with something a newcomer could verify. That single rule does more for assessment quality than any refinement of the model.</p>
<h2 id="how-often-should-you-re-assess-ai-maturity">How Often Should You Re-Assess AI Maturity?</h2>
<p>Re-assess on a six-month cadence with a lightweight quarterly check-in. Six months is long enough for a funded initiative to change a dimension score, and short enough that the assessment still reflects reality when budget decisions are made. The quarterly check-in should touch only the two or three scores in motion — usually the binding constraint and whatever initiative is funded against it — and should take under an hour.</p>
<p>Run the full four-dimension assessment annually, with the same rubric and ideally the same facilitator, so scores are comparable year over year. Comparability matters more than precision: a consistent methodology that shows direction of travel is more useful to a board than a sophisticated model applied differently each time.</p>
<p>One caution on cadence. Re-assessing too frequently turns the exercise into reporting overhead and teams start gaming the numbers. Re-assessing too rarely means the assessment describes an organization that no longer exists. Six months is the interval that most enterprises find keeps the document alive without making it a burden.</p>
"""

FAQ = {
 "EN": [
  ("How long does an AI maturity assessment take?",
   "A full four-dimension assessment takes four to six weeks: two to three weeks gathering evidence across functions, one workshop to score and challenge, and one to two weeks to write up the profile and agree the binding constraint. A quarterly check-in limited to the dimensions in motion should take under an hour."),
  ("Who should be involved in an AI maturity assessment?",
   "Include the function that owns each candidate workflow, someone from data or platform engineering, someone from risk or internal audit, and at least one sceptic who has to live with the result. The enthusiast who built the pilot should be in the room but should not score it. Facilitation by someone outside the AI team keeps scores honest."),
  ("What is the difference between an AI maturity model and an AI readiness assessment?",
   "A readiness assessment asks whether you could start: do you have data, skills, and sponsorship. A maturity model asks what you can currently do and how reliably, across governance, data readiness, workflow integration, and capability. Readiness is a gate before investment; maturity is a profile that guides where the next investment goes."),
  ("How do you stop a maturity assessment becoming a paperwork exercise?",
   "Require checkable evidence for every score, name one binding constraint, and convert it into a single funded initiative with a target level and a date. If the output is a slide deck with no funded change attached, the assessment produced documentation rather than a decision."),
 ],
 "zh-CN": [
  ("一次AI成熟度评估需要多长时间？",
   "一次完整的四维度评估需要四到六周：两到三周跨部门收集证据，一次工作坊进行评分与质询，一到两周撰写成熟度画像并确定约束性瓶颈。只针对正在变化的维度进行的季度检查，应控制在一小时以内。"),
  ("AI成熟度评估应该让谁参与？",
   "应包括每个候选工作流的业务归属部门、数据或平台工程团队的代表、风险或内审部门的代表，以及至少一位必须承受结果的质疑者。构建试点的热情推动者可以在场，但不应由其评分。由AI团队之外的人主持，有助于保持评分的诚实。"),
  ("AI成熟度模型与AI就绪度评估有什么区别？",
   "就绪度评估问的是“能不能开始”：是否有数据、人才和赞助方。成熟度模型问的是“现在能做什么、做得有多稳”，覆盖治理、数据就绪、工作流融合与组织能力四个方面。就绪度是投资前的门槛，成熟度是决定下一笔投资投向哪里的画像。"),
  ("如何避免成熟度评估沦为一次文档作业？",
   "要求每一项评分都有可核查的证据；明确指出唯一的约束性瓶颈；并把它转化为一个带目标等级和截止日期的、已获预算的举措。如果产出只是一份没有对应资金变更的幻灯片，那么这次评估生产的是文档，而不是决策。"),
 ],
}

def main():
    s = F.load(SLUG, "EN")
    b = F.get_body(s)
    anchor = '<section class="faq-section"'
    assert anchor in b
    b = b.replace(anchor, EN_NEW.strip() + "\n\n            " + anchor, 1)
    ren = {
        "The Strategic Imperative for Enterprise AI in 2025": "Why Does AI Maturity Need to Be Measured Now?",
        "Framework for AI Strategy Development": "What Framework Should an AI Maturity Assessment Use?",
        "Measuring Success and Demonstrating ROI": "How Do You Measure Success and Demonstrate ROI?",
        "Maturity Levels in Practice: From Experiments to Embedded": "What Do the Maturity Levels Look Like in Practice?",
        "Implementation Roadmap and Key Success Factors": "What Does an Implementation Roadmap Look Like?",
    }
    for old, new in ren.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    F.save(SLUG, "EN", F.set_body(s, b))

    s = F.load(SLUG, "zh-CN")
    b = F.get_body(s)
    pairs = [
        ("2025年企业AI的战略紧迫性", "为什么现在必须衡量AI成熟度？"),
        ("AI战略开发框架", "AI成熟度评估应该采用什么框架？"),
        ("衡量成功与展示投资回报", "如何衡量成效并展示投资回报？"),
        ("实施路径与组织准备", "实施路径与组织准备应该如何安排？"),
    ]
    for old, new in pairs:
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    dup = "战略实施路径与关键成功因素"
    b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(dup) + r'(</h2>)', r'\g<1>' + "战略实施路径与关键成功因素是什么？" + r'\g<2>', b, count=1)
    b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(dup) + r'(</h2>)', r'\g<1>' + "企业实施路线图与成功因素有哪些？" + r'\g<2>', b, count=1)
    b = re.sub(r'(<h2 id="[^"]+">)' + re.escape("企业实施路线图与成功因素") + r'(</h2>)', r'\g<1>' + "如何从试点走向规模化？" + r'\g<2>', b, count=1)
    b = re.sub(r'(<h2 id="[^"]+">)' + re.escape("行业数字化转型深度分析") + r'(</h2>)', r'\g<1>' + "不同行业的AI成熟度差异体现在哪里？" + r'\g<2>', b, count=1)
    F.save(SLUG, "zh-CN", F.set_body(s, b))

    before, after = F.process(SLUG, faq=FAQ, tw_from_cn=True,
                              faq_titles={"EN": "Frequently Asked Questions", "zh-CN": "常见问题", "zh-TW": "常見問題"})
    for lang in ("EN", "zh-CN", "zh-TW"):
        print(lang, "before", before[lang], "after", after[lang])

main()
