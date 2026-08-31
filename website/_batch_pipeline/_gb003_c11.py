#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gbatch_003 slug 11 — ai-driven-customer-segmentation-banking"""
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb003_lib import process, stats, tw_renames
from _gb001_s2t import s2tw

SLUG = 'ai-driven-customer-segmentation-banking'

EN_RENAMES = {
    'Putting Segments to Work: Pricing, Products, and Advice':
        'How Do Banks Put Segments to Work in Pricing, Products, and Advice?',
    'From Segments to Action with Conversational BI':
        'How Do Banks Move From Segments to Action With Conversational BI?',
}

EN_INSERTS = [
    ('Which Life Events Should a Bank Detect First?',
     'which-life-events-should-a-bank-detect-first',
     '<p>Life events are the highest-value segmentation signal a bank holds, because they change product needs within weeks and are visible in transaction behaviour long before they appear in a demographic profile. Five are worth detecting first, and each has a specific behavioural signature.</p>'
     '<ul>'
     '<li><strong>Employment change.</strong> Salary credits from a new payer, a gap in regular credits, or a change in credit amount and cadence. Detected early, this is the trigger for mortgage pre-approval, relocation services, or — where income has dropped — proactive hardship support rather than a collections call.</li>'
     '<li><strong>Relocation.</strong> Changed merchant geography, new recurring local payments, or a change in branch and ATM usage. This drives mortgage and insurance offers, and it is also a fraud and identity signal worth monitoring.</li>'
     '<li><strong>Family formation.</strong> New categories of spend — childcare, education, family health — plus a shift in basket composition. This is when protection products, education savings, and estate planning become relevant rather than intrusive.</li>'
     '<li><strong>Business formation.</strong> A personal account receiving merchant settlements, or new supplier payments. Early detection wins the business banking relationship before the customer takes it to a competitor.</li>'
     '<li><strong>Approaching retirement.</strong> A shift from accumulation to drawdown behaviour, reduced regular credits, and increased healthcare spend. This is the wealth-advice moment, and it is missed by demographic segments that treat everyone over 55 identically.</li>'
     '</ul>'
     '<p>Two rules keep this from becoming surveillance. Detect from transaction patterns and declared data the customer has already given, not from inferences the customer would find surprising. And attach a clear action to every event — a detected event with no corresponding offer or service is a privacy cost with no benefit, which is exactly the pattern that triggers complaints.</p>'),

    ('How Should Banks Govern AI Segmentation Under Model Risk Rules?',
     'how-should-banks-govern-ai-segmentation-under-model-risk-rules',
     '<p>Banking operates under model risk management expectations that most industries do not face, and segmentation is not exempt: if a model influences pricing, credit, or customer treatment, it is in scope. Four practices keep a segmentation programme defensible without slowing it to a halt.</p>'
     '<ol>'
     '<li><strong>Document the purpose and the population.</strong> Every segment model needs a written statement of what it is for, which customers it covers, and where it must not be used. Using a marketing segment to inform credit decisions is the most common and most serious scope breach.</li>'
     '<li><strong>Validate independently.</strong> Conceptual soundness, outcome analysis, and ongoing monitoring should be performed by someone other than the builder. For segmentation, the critical tests are stability over time and the absence of proxy discrimination — a behaviour-based segment can still correlate with protected characteristics.</li>'
     '<li><strong>Test for fairness explicitly.</strong> Measure segment outcomes and the treatments attached to them across protected groups. A segment that is neutral in construction can still produce disparate impact if the offer attached to it is not available or appropriate to all groups.</li>'
     '<li><strong>Keep the human decision legible.</strong> Where a segment informs an adverse or materially different outcome, the reason must be explainable in terms a customer and a regulator can follow — "recent transaction pattern indicates changed circumstances" rather than a model score.</li>'
     '</ol>'
     '<p>Handled this way, governance accelerates deployment rather than delaying it: once the validation pattern exists, each new segment inherits it, and the marginal cost of the next model falls while the institution\'s ability to answer an examiner improves.</p>'),

    ('What Does a Banking Segmentation Programme Cost and Deliver?',
     'what-does-a-banking-segmentation-programme-cost-and-deliver',
     '<p>The business case rests on three documented effects. Bain & Company\'s long-running research found that increasing retention by 5 percent lifts profits by 25 to 95 percent, because retained relationships compound through cross-sell and lower service cost. McKinsey\'s personalisation research estimates reductions in acquisition cost of up to 50 percent, revenue lifts of 5 to 15 percent, and marketing spend efficiency gains of 10 to 30 percent. Segmentation is the mechanism underneath all three: it decides who is offered what, at what price, through which channel.</p>'
     '<p>On the cost side, the dominant line item is data work rather than modelling. Expect roughly half the effort in identity resolution, consent status, and feature pipelines across core banking, cards, digital channels, and CRM; a quarter in model development and validation; and a quarter in integration with campaign, pricing, and relationship management systems. Running costs are modest but grow with the number of segments that require real-time assignment.</p>'
     '<p>The realistic sequencing is a single product line — cards or deposits — for the first deployment, measured against a holdout, then expansion to adjacent products. Institutions that sequence this way typically see the first measurable effect within one to two quarters, and the compounding effect in year two, when the validated segments carry over to pricing, collections, and advice rather than marketing alone.</p>'),
]

EN_FAQ = [
    ('How is AI segmentation different from traditional bank segmentation?',
     'Traditional segmentation sorts customers by who they are — age, income, geography, product holdings — and refreshes the groups periodically, so the view is always somewhat out of date. AI segmentation clusters customers by what they do: transaction patterns, digital journeys, channel usage, life-event signals, and how those change over time. The segments update as behaviour changes, they are far more granular, and they support risk-based pricing and next-best-action decisions that demographic buckets cannot. The shift is from describing a customer base to predicting what each customer will need next.'),
    ('What data does AI customer segmentation need in banking?',
     'Five categories, in descending order of importance: transaction history with merchant and category detail, product holdings and balances, digital engagement across app and web, life-event signals inferred from behaviour, and external context such as macroeconomic indicators. What matters more than volume is that the data is resolved to one customer across products and channels, and that consent status is recorded per use — a segment built on data the bank is not permitted to use for marketing is a compliance incident waiting to happen.'),
    ('Can behavioural segmentation create fairness or compliance problems?',
     'Yes, and this is the most common reason banking segmentation programmes are stopped. A model that is neutral in construction can still produce disparate impact if the offer attached to a segment is not appropriate or available to all groups, and behaviour-based clusters can correlate with protected characteristics even when those characteristics are excluded. The controls are explicit fairness testing across protected groups, independent validation, a documented purpose that prevents a marketing segment from informing credit decisions, and explainability in terms a customer and a regulator can follow.'),
    ('How do relationship managers actually use AI segments day to day?',
     'Through the tools they already use. Segments delivered as a quarterly PDF are ignored; segments that a relationship manager can query before a client meeting — "which of my clients show relocation signals this quarter?" — change behaviour immediately. The practical requirements are governed access with role-based filtering so a manager sees only their own book, an answer in seconds rather than a data request, and a plain-language reason for each assignment so the manager can explain it to the client.'),
    ('How long does it take to deploy AI segmentation in a bank?',
     'For one product line, expect ten to sixteen weeks: three to five weeks for data and consent mapping across the relevant systems, three to five weeks for model development and independent validation, and four to six weeks for integration with campaign and relationship management tools plus the monitoring setup. Validation and model risk review are the steps most often underestimated. Institutions with an existing customer data foundation and a proven validation pattern move considerably faster, because each subsequent segment inherits the controls already built.'),
]

ZH_RENAMES = {
    '2025年AI驱动的行业转型': '2025年AI如何改变银行业的客户细分？',
    '金融服务：AI作为竞争差异化因素': 'AI细分为何成为银行业的竞争差异化因素？',
    '人机协作的必要性': '为什么银行细分必须保留人工判断？',
}

TW_RENAMES = {
    '2025年AI驱動的行業轉型': '2025年AI如何改變銀行業的客戶細分？',
    '金融服務：AI作为競爭差异化因素': 'AI細分為何成為銀行業的競爭差異化因素？',
    '人机协作的必要性': '為什麼銀行細分必須保留人工判斷？',
}

ZH_FAQ = [
    ('AI细分与银行传统的客户细分有什么不同？',
     '传统细分按客户"是谁"分群——年龄、收入、地域、持有产品——并按周期刷新，因此视图总是滞后于现实。AI细分按客户"做什么"聚类：交易模式、数字渠道旅程、渠道使用习惯、生命周期事件信号，以及这些行为随时间的变化。细分会随行为变化而更新，颗粒度显著更细，并且能够支撑风险定价与下一步最佳动作，这是人口统计分群做不到的。本质区别在于：从描述客群，转向预测每一位客户接下来需要什么。'),
    ('银行业的AI客户细分需要哪些数据？',
     '按重要性递减，共五类：带有商户与类目标签的交易历史、产品持有情况与余额、App与Web端的数字互动行为、从行为中推断的生命周期事件信号，以及宏观经济指标等外部背景。比数据量更重要的是两件事：数据能否跨产品与渠道归集到同一个客户，以及每个用途的授权状态是否被记录——建立在不允许用于营销的数据之上的细分，本质上是一次等待发生的合规事故。'),
    ('行为细分会带来公平性或合规风险吗？',
     '会，而且这是银行的细分项目被叫停最常见的原因。即使模型在构建上是中立的，如果挂在某个细分上的优惠并不适合或不对所有群体开放，仍然可能产生差别性影响；即便排除了受保护特征，基于行为的聚类仍可能与这些特征相关。相应的控制措施包括：跨受保护群体的公平性测试、独立验证、用书面用途说明防止营销细分被用于信贷决策，以及用客户与监管者都能理解的方式解释结论。'),
    ('客户经理在日常工作中如何真正用上AI细分？',
     '通过他们已经在用的工具。以季度PDF形式交付的细分会被忽略；而客户经理能在客户会面之前直接查询的细分——"本季度我的客户中有哪些出现了搬迁信号？"——会立刻改变行为。要落地需要三个条件：带角色过滤的受治理访问，让经理只看到自己的客户群；秒级返回的答案，而不是提交数据需求；以及每个细分归属的通俗解释，让经理可以向客户说明原因。'),
    ('在银行部署AI细分需要多长时间？',
     '就一条产品线而言，通常需要十到十六周：三到五周完成相关系统的数据与授权映射，三到五周完成模型开发与独立验证，四到六周完成与营销活动及客户关系管理工具的集成并配置监控。验证与模型风险评审是最常被低估的环节。已有客户数据基础、且验证模式成熟机构会快得多，因为后续每个细分都能继承既有控制。'),
]


def run():
    b = {lg: stats(SLUG, lg) for lg in ('en', 'zh-cn', 'zh-tw')}
    process(SLUG, 'en', h2_renames=EN_RENAMES, inserts=EN_INSERTS, faq=EN_FAQ)
    process(SLUG, 'zh-cn', h2_renames=ZH_RENAMES, faq=ZH_FAQ)
    process(SLUG, 'zh-tw', h2_renames=TW_RENAMES, faq=[(s2tw(q), s2tw(a)) for q, a in ZH_FAQ])
    for lg in ('en', 'zh-cn', 'zh-tw'):
        print(lg, b[lg], '->', stats(SLUG, lg))


if __name__ == '__main__':
    run()
