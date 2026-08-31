#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gbatch_003 slug 01 — ai-culture-enterprise-data-literacy-programs"""
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb003_lib import process, stats, tw_renames
from _gb001_s2t import s2tw

SLUG = 'ai-culture-enterprise-data-literacy-programs'

EN_RENAMES = {
    'The Strategic Context for Enterprise AI':
        'Why Does Data Literacy Decide Whether Enterprise AI Compounds or Stalls?',
    'Framework for Strategic Decision-Making':
        'How Should Leaders Prioritise Data Literacy Investment?',
    'Organizational Change and Capability Building':
        'How Do You Build Capability Without Turning Training Into Theatre?',
    'Measuring Strategic Impact':
        'How Should You Measure the Impact of a Data Literacy Program?',
}

EN_INSERTS = [
    ('What Does a Role-Based Data Literacy Curriculum Actually Contain?',
     'what-does-a-role-based-data-literacy-curriculum-contain',
     '<p>A single curriculum for the whole organisation is the fastest way to waste a training budget, because the literacy gap is different in every seat. Four audiences need four different curricula, and the differences are concrete rather than cosmetic.</p>'
     '<ul>'
     '<li><strong>Executives.</strong> They do not need to build a model; they need to set expectations and challenge outputs. Their curriculum covers how to read a variance, what a confidence interval is actually promising, which questions a dashboard can and cannot answer, and how to spot a metric that has been quietly redefined. Two half-day sessions, run on the company\'s own numbers, beat any generic leadership course.</li>'
     '<li><strong>Managers.</strong> They run the rituals where data is either used or ignored — the weekly operations review, the monthly business review, the quarterly plan. Their curriculum is about running a data-led meeting: opening on the metric, interrogating the driver, agreeing the action, and closing the loop next week.</li>'
     '<li><strong>Practitioners.</strong> Analysts, merchants, category managers, and finance business partners need tool-specific fluency — how to slice a cohort, how to build a defensible forecast, how to reconcile two reports that disagree, and how to document a definition so the next person does not rebuild it.</li>'
     '<li><strong>Frontline.</strong> Store associates, service agents, and sales staff need the least and benefit the most: what the number on their screen means, what to do when it looks wrong, and who to ask. Plain-language interfaces matter most here, because this group will never open a BI tool.</li>'
     '</ul>'
     '<p>One layer belongs in all four curricula: the habit of interrogating a number before acting on it. Where did it come from? Over what period and population? What is it compared against, and what would have to be true for it to be wrong? That three-question reflex is the actual product of a literacy program, and it is what makes AI outputs safe to act on.</p>'),

    ('How Do You Embed Data Literacy Into the Flow of Work?',
     'how-do-you-embed-data-literacy-into-the-flow-of-work',
     '<p>Knowledge decays fast when it is not used. Controlled studies of corporate training consistently find that most classroom content is forgotten within weeks unless it is applied on the job, which is why the delivery model matters more than the content. The programs that hold are the ones attached to a live initiative: a pricing review, a forecasting cycle, a churn analysis. Participants learn the skill on Tuesday and use it on Wednesday, and the business sees the result in the same quarter.</p>'
     '<p>Three mechanisms do most of the work. First, rituals: rewrite the standing meeting agenda so it opens on the metric and requires an owner to explain the driver — the skill is then practised weekly, not annually. Second, job aids: a one-page definition card for every metric in circulation, maintained by the data team, removes the friction that sends people back to instinct. Third, champions: one literate peer per team, recognised and given time, answers the hundred small questions that never reach the centre of excellence.</p>'
     '<p>Access design is the fourth mechanism and the most underrated. If asking a question requires logging into a BI tool, finding the right report, and remembering how filters work, literacy training loses to convenience every time. Putting a governed, conversational interface inside the chat tools people already use — where a merchant can type "which of my high-value customers are at risk this week?" — converts literacy from a skill people must schedule into a behaviour they perform by default. This is also where the program gets its evidence: every question asked is a signal of who is using data, on what, and where confidence is still missing.</p>'),

    ('Which Failure Modes Kill Data Literacy Programs?',
     'which-failure-modes-kill-data-literacy-programs',
     '<p>Gartner\'s projection that 60 percent of data literacy programs will fail to deliver measurable business impact through 2026 is not a statement about teaching quality. It is a statement about design. The failure modes are predictable, and each one has a detector you can run before the budget is spent.</p>'
     '<ul>'
     '<li><strong>Generic curriculum.</strong> One course for everyone, measured by completion rate. Detect it by asking what a store manager and a finance director each learned differently; if the answer is nothing, the program is a compliance exercise.</li>'
     '<li><strong>Event-based delivery.</strong> A training day with no follow-up. Detect it by looking for a practice cadence in the plan; if there is no weekly or monthly ritual attached, adoption will decay within a quarter.</li>'
     '<li><strong>Absent executive sponsorship.</strong> Programs owned only by HR or IT lose the link to business decisions. Detect it by naming the P&amp;L owner in the charter — and by checking whether that owner is scheduled to appear in the sessions.</li>'
     '<li><strong>No measurement.</strong> Completion rates are not outcomes. Detect it by asking what business metric the program is expected to move and how it will be attributed.</li>'
     '<li><strong>Tooling-first thinking.</strong> Buying a platform and calling it a literacy strategy. Detect it by checking whether anyone has assessed current skill levels before the rollout.</li>'
     '<li><strong>Punishing questions.</strong> In low-trust cultures, challenging a number is read as challenging a person, so people stop asking. Detect it in the tone of leadership when a metric is disputed — that reaction sets the ceiling for the entire program.</li>'
     '</ul>'
     '<p>The remedy is the same in every case: design backwards from the decision. Pick the decisions where better data use is worth the most, identify who makes them, teach exactly the skills those decisions require, and measure whether the decisions improved. Programs built that way rarely need to defend their budget.</p>'),
]

EN_FAQ = [
    ('Who should own an enterprise data literacy program?',
     'The most effective programs are co-owned by a business executive with P&L accountability and a data centre of excellence — not run by IT or HR alone. Business ownership keeps the curriculum tied to real decisions and guarantees the executive sponsorship Gartner identifies as the difference between programs that deliver impact and the 60 percent that do not; the centre of excellence supplies the standards, metric definitions, and reusable material that stop every team reinventing the same training.'),
    ('How long does it take to build a data-driven culture?',
     'Expect visible behaviour change within two to three quarters when the program is role-based and attached to live initiatives, and durable cultural change over two to three years of consistent reinforcement. The early signal is not test scores but behaviour: meetings that open on a metric, analysts receiving fewer ad-hoc requests, and business users answering their own questions. Executives should fund for the multi-year horizon and demand quarterly evidence of the behaviour shift.'),
    ('How should data literacy be assessed?',
     'Start with a role-based baseline assessment rather than a generic quiz, and test the skill each role actually needs: executives interpreting a variance chart, managers running a data-led review, practitioners reconciling two conflicting reports. Re-run the same assessment every two quarters and segment the results by function, because an organisation-wide average hides the one team whose literacy gap is blocking an AI rollout. Pair the assessment with behavioural data — tool adoption, self-service question volume — so self-reported confidence is checked against actual usage.'),
    ('Does data literacy training need to cover AI and generative tools?',
     'Yes, and it should be layered onto the data fundamentals rather than taught as a separate technical topic. The AI-specific skills are prompt literacy (how to ask a question so the answer is grounded), output interrogation (how to check whether an AI answer is supported by the data it cites), and calibrated trust (knowing when to act on a model recommendation and when to escalate). Without these, employees either over-trust AI outputs or reject them outright, and both responses waste the investment.'),
    ('How do you fund a data literacy program when budgets are tight?',
     'Attach it to a live AI or analytics rollout instead of funding it as standalone training. Literacy delivered alongside a deployment the business already funds pays for itself through adoption velocity — the rollout lands faster and the platform does not sit idle — and it gives program owners a business metric to report against. Standalone training budgets are the first cut in a downturn; embedded enablement survives because it is part of delivering the initiative.'),
]

ZH_RENAMES = {
    '当前格局与关键趋势': '为什么数据素养决定企业AI是复利还是停滞？',
    '实施框架与最佳实践': '如何设计真正有效的数据素养项目？',
    '衡量影响与展示价值': '如何衡量数据素养项目的业务影响？',
    '克服常见挑战': '企业数据素养项目最常见的障碍是什么？',
    '风险管理与合规框架': '数据素养如何支撑风险管理与合规？',
    '价值实现与持续改进': '如何让数据素养能力持续创造价值？',
    '中国市场特有的实施优势': '中国市场在数据素养落地上的优势是什么？',
}

ZH_FAQ = [
    ('企业数据素养项目应该由谁负责？',
     '最有效的做法是由一位承担损益责任的业务高管与数据卓越中心共同负责，而不是由IT或人力资源部门单独推动。业务负责人保证课程始终围绕真实决策展开，也提供了Gartner所强调的、决定项目能否产生业务影响的执行层支持；卓越中心则负责统一指标定义、标准与可复用教材，避免每个团队重复造轮子。'),
    ('建立数据驱动的文化需要多长时间？',
     '当项目按角色设计并嵌入真实业务举措时，两到三个季度就能看到行为变化：会议开始从指标切入、分析师收到的临时取数需求下降、业务用户能自己回答一部分问题。但文化层面的稳固需要两到三年持续强化。建议按多年周期立项，同时按季度要求出示行为变化的证据，而不是等到年底才看考试成绩。'),
    ('如何评估员工的数据素养水平？',
     '先做基于角色的基线评估，而不是全员通用的测验：高管要会读差异分析，管理者要会主持以数据为核心的复盘，业务分析师要能核对两份口径冲突的报表。每两个季度复测一次，并按职能拆分结果——全员平均分往往掩盖了某一个团队的能力短板，而正是这个短板在拖慢AI项目的落地。同时把工具采用率、自助提问量等行为数据纳入评估，用实际使用行为校验主观信心。'),
    ('数据素养培训是否需要覆盖AI与生成式工具？',
     '需要，而且应该叠加在数据基础能力之上，而不是作为单独的技术课程。AI相关的三项能力是：提问素养（如何提问才能让答案有据可依）、结果核查（判断AI给出的答案是否被其引用的数据支持）、以及有分寸的信任（知道何时可以直接采纳模型建议、何时需要升级人工判断）。缺少这三项，员工要么盲目相信AI输出，要么一概排斥，两种反应都会让AI投资打折扣。'),
    ('预算紧张时，如何为数据素养项目争取资源？',
     '把它挂在一个正在进行的AI或分析平台落地项目上，而不是作为独立培训单独申请预算。与落地项目捆绑的赋能会通过加快采用速度自我回收成本——系统上线更快，平台也不会闲置——同时项目负责人在汇报时也有了明确的业务指标。独立的培训预算往往在经济下行时第一个被砍，而嵌入交付过程的赋能因为属于项目交付的一部分，通常能够保留。'),
]


def run():
    b = {lg: stats(SLUG, lg) for lg in ('en', 'zh-cn', 'zh-tw')}
    process(SLUG, 'en', h2_renames=EN_RENAMES, inserts=EN_INSERTS, faq=EN_FAQ, drop_body_faq=True)
    process(SLUG, 'zh-cn', h2_renames=ZH_RENAMES, faq=ZH_FAQ)
    TW_RENAMES = {
        'Framework for Strategic Decision-Making': '企業該如何排定數據素養投資的優先順序？',
        'Organizational Change and Capability Building': '如何建立能力而不讓培訓淪為形式？',
        'Measuring Strategic Impact': '該如何衡量數據素養專案的影響？',
        '常見問題': '常見問題',
        '規模化推廣的關鍵成功因素': '規模化推廣的關鍵成功因素是什麼？',
        '技術基礎設施與實施考量': '技術基礎設施與實施上有哪些考量？',
        '中國市場特有的實施優勢': '台灣與華語市場在數據素養落地上有哪些優勢？',
    }
    process(SLUG, 'zh-tw', h2_renames=TW_RENAMES, faq=[(s2tw(q), s2tw(a)) for q, a in ZH_FAQ],
            drop_body_faq=True)
    a = {lg: stats(SLUG, lg) for lg in ('en', 'zh-cn', 'zh-tw')}
    for lg in ('en', 'zh-cn', 'zh-tw'):
        print(lg, b[lg], '->', a[lg])


if __name__ == '__main__':
    run()
