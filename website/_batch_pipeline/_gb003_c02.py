#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gbatch_003 slug 02 — ai-customer-lifetime-value-prediction-retail"""
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb003_lib import process, stats
from _gb001_s2t import s2tw

SLUG = 'ai-customer-lifetime-value-prediction-retail'

EN_RENAMES = {
    'Industry Transformation Through AI in 2025':
        'How Is AI Changing Retail Customer Value Management in 2025?',
    'Financial Services: AI as a Competitive Differentiator':
        "What Can Retail Learn From Financial Services' Real-Time Scoring?",
    'The Human-AI Collaboration Imperative':
        'Where Should Humans Stay in the CLV Decision Loop?',
}

EN_INSERTS = [
    ('How Do You Choose the Right CLV Model for a Retail Portfolio?',
     'how-do-you-choose-the-right-clv-model-for-a-retail-portfolio',
     '<p>The model choice is less consequential than the target definition, but it still matters, and the three families behave very differently on retail data.</p>'
     '<ul>'
     '<li><strong>Probabilistic "buy-till-you-die" models</strong> (BG/NBD for purchase frequency plus a Gamma-Gamma spend layer) remain the workhorse for non-contractual retail. They need only transaction history, they are interpretable by a merchandising team, and they produce well-calibrated expected value over a defined horizon. Their weakness is that they ignore covariates: they cannot easily use engagement, browsing, or returns behaviour.</li>'
     '<li><strong>Gradient-boosted survival and regression models</strong> handle covariates natively, which is why most retailers with a mature data stack land here. They ingest engagement, returns, channel mix, and external signals, and they can be trained directly on contribution margin rather than revenue. The cost is a greater risk of leakage and a real requirement for holdout validation.</li>'
     '<li><strong>Sequence and deep-learning models</strong> earn their complexity only at very large scale or where the purchase pattern is genuinely sequential — grocery baskets, subscription boxes. For most specialty and general merchandise retailers, the incremental accuracy does not justify the engineering and explainability cost.</li>'
     '</ul>'
     '<p>Two rules cut through the choice. First, match the horizon to the decision: a retention campaign needs a 90-day value forecast, while a loyalty-tier redesign needs a multi-year view, and a single model rarely serves both well. Second, decide the target before the algorithm — revenue CLV is easier to explain but systematically overvalues discount-driven and high-return customers, while contribution-margin CLV costs more to compute and pays for itself the first time it stops the business from buying unprofitable volume.</p>'),

    ('How Should CLV Scores Reach the Systems That Touch the Customer?',
     'how-should-clv-scores-reach-the-systems-that-touch-the-customer',
     '<p>A CLV score that lives in a dashboard changes nothing. The value is unlocked when the score is written into the systems that make customer-facing decisions, at the latency those decisions require. Four destinations matter in retail.</p>'
     '<ol>'
     '<li><strong>Offer and discount engines.</strong> The score sets the ceiling on discount depth: high-CLV, low-churn-risk customers receive full-price offers, while at-risk high-value customers receive retention investment. Without the score, discounting is uniform and margin leaks to customers who would have paid anyway.</li>'
     '<li><strong>Loyalty tier management.</strong> Predicted value should drive tier assignment and soft benefits ahead of realised spend, because that is where the tier actually changes behaviour rather than merely rewarding it.</li>'
     '<li><strong>Service routing.</strong> Contact centres and store clienteling teams prioritise by value: a high-CLV customer with an open complaint is escalated automatically, which is usually the single fastest payback in the programme.</li>'
     '<li><strong>Paid media.</strong> Suppression and lookalike seeding both improve with value weighting — suppressing existing high-value customers from acquisition spend and building lookalikes from predicted rather than historical value.</li>'
     '</ol>'
     '<p>Three engineering disciplines keep this safe. Latency: define which decisions need real-time scoring (service routing, on-site offers) and which can run on a nightly batch (campaign audiences), because real-time everything is expensive and rarely necessary. Guardrails: hard caps on discount exposure and mandatory human approval for any offer above a threshold, so a model error cannot liquidate margin in an afternoon. Measurement: hold out a randomised control group permanently, so the incremental effect of CLV-driven decisions is measured rather than assumed.</p>'),

    ('What Does CLV Prediction Cost, and Which Mistakes Undermine It?',
     'what-does-clv-prediction-cost-and-which-mistakes-undermine-it',
     '<p>The cost profile is dominated by data work, not modelling. Expect roughly half the effort in identity resolution and feature pipelines, a quarter in model development and validation, and a quarter in integration and change management. Running costs are modest — batch scoring over a few million customers is inexpensive — but they rise sharply if every decision requires real-time inference.</p>'
     '<p>The mistakes that undermine CLV programmes are consistent across retailers:</p>'
     '<ul>'
     '<li><strong>Fragmented identity.</strong> Online and in-store purchases that cannot be reconciled produce two half-value customers, and every downstream number is wrong. Fix identity before the model, and treat unresolved identities as an explicit data-quality metric.</li>'
     '<li><strong>Target leakage.</strong> Training on features that already encode the outcome — a returns flag computed after the return window, a churn label derived from the same inactivity period used as a feature — produces spectacular offline accuracy that collapses in production. Time-box every feature to information available at the prediction date.</li>'
     '<li><strong>Revenue-blind discounting.</strong> Optimising revenue CLV drives the business to discount to the customers most likely to respond, which are frequently the least profitable. Measure value on contribution margin and validate on holdout customers, not historical cohorts.</li>'
     '<li><strong>Stale scores.</strong> A quarterly refresh is too slow for Q4, when behaviour changes weekly. Define the refresh cadence per decision and monitor feature drift.</li>'
     '<li><strong>No control group.</strong> Without a randomised holdout, the programme cannot separate model contribution from seasonality, and the business case collapses the first time someone asks for proof.</li>'
     '</ul>'
     '<p>Retailers that avoid these five build a compounding asset: every season of validated predictions improves the next, and the score becomes the shared language between merchandising, marketing, and finance.</p>'),
]

EN_FAQ = [
    ('How is predicted customer lifetime value different from RFM segmentation?',
     'RFM (recency, frequency, monetary) describes what a customer has already done and is recalculated periodically, so it is always backward-looking and goes stale between refreshes. Predicted CLV estimates what a customer will be worth over a defined future horizon, is refreshed continuously as new signals arrive, and can be produced for customers with almost no purchase history by leaning on engagement and channel behaviour. In practice, predicted CLV delivers 20 to 30 percent better targeting efficiency than RFM rules, measured as lift on holdout data, because it ranks customers by future potential rather than past activity.'),
    ('How far ahead can CLV be predicted reliably?',
     'Match the horizon to the decision. Ninety-day value forecasts on customers with purchase history are tractable and routinely reach single-digit percentage error, which is enough for retention budgets and offer selection. Twelve to twenty-four month forecasts are usable for loyalty design and media planning but should be treated as calibrated ranges rather than point estimates. Multi-year "lifetime" estimates are directional only, because assortment, competition, and customer circumstances all change — and the honest output is a probability distribution the business can plan against.'),
    ('Should CLV be measured on revenue or contribution margin?',
     'Contribution margin wherever the data supports it. Revenue-based CLV systematically overvalues customers who buy heavily on promotion and return a large share of what they order, which leads the business to spend retention budget on customers who destroy margin. Where returns, discounts, and shipping cost cannot yet be attributed cleanly at line level, start with revenue CLV, but instrument margin data in parallel and switch as soon as the attribution holds up — this is usually the single highest-value data investment in a CLV programme.'),
    ('How do you prove a CLV model is actually working?',
     'Hold out a randomised control group permanently and measure incremental outcomes against it: retention rate, margin per customer, and discount spend per retained customer for the scored population versus the control. Track calibration separately from accuracy — if customers assigned a 70 percent churn probability actually churn at 70 percent, retention budget can be allocated proportionally. Then monitor drift: feature distributions, score distributions, and realised-versus-predicted value by cohort, re-validating the model whenever a seasonal shift moves them.'),
    ('What data is the minimum needed to start CLV prediction?',
     'Two years of transaction history with customer identifiers, order lines, and product margins is enough to build a defensible first model. Engagement signals (email, app, loyalty activity) and returns behaviour materially improve accuracy, especially for newer customers with thin purchase history, but they are enhancements rather than prerequisites. What is non-negotiable is identity resolution across channels: without it, the same customer appears twice and the model double-counts value, which no amount of additional data will fix.'),
]

ZH_RENAMES = {
    '2025年AI驱动的行业转型': '2025年AI如何重塑零售客户价值管理？',
    '金融服务：AI作为竞争差异化因素': '零售能从金融服务业的实时评分中学到什么？',
    '人机协作的必要性': '为什么CLV决策中必须保留人工判断？',
}

ZH_FAQ = [
    ('预测型客户生命周期价值与RFM细分有什么不同？',
     'RFM（最近一次消费、消费频率、消费金额）描述的是客户已经发生的行为，且通常按季度重算，因此在两次刷新之间必然过时。预测型CLV估计的是客户在未来一段确定时间内的价值，会随着新信号持续刷新，并且对几乎没有购买记录的新客也能通过互动与渠道行为给出估计。实践中，以留出集的提升度衡量，预测型CLV的定向效率比RFM规则高20%到30%，因为它按未来潜力排序，而不是按过去活跃度排序。'),
    ('CLV能够可靠地预测多远的未来？',
     '预测周期应该与决策匹配。对有购买记录的客户做90天价值预测是可解的，误差率通常可以控制在个位数百分比，足以支撑留存预算与优惠选择。12到24个月的预测可用于忠诚度设计与媒介规划，但应当作为经过校准的区间而非精确的点估计。跨年度的"终身"估计仅具方向性参考，因为商品结构、竞争与客户的个人情况都会变化——诚实的输出是一个可供业务规划的概率区间。'),
    ('CLV应该按收入还是按贡献毛利计算？',
     '只要数据支持，就应该用贡献毛利。基于收入的CLV会系统性地高估那些重度依赖促销购买、且退货比例很高的客户，导致企业把留存预算花在实际上侵蚀毛利的人群上。如果在订单行层面还无法干净地归因退货、折扣与履约成本，可以先用收入口径起步，同时并行为毛利数据埋点，一旦归因可靠就立即切换——这通常是CLV项目中回报最高的一项数据投入。'),
    ('如何证明CLV模型真的在发挥作用？',
     '永久保留一个随机对照组，并与之比较增量结果：被评分人群相对对照组在留存率、单客毛利、以及每留住一位客户所花费的折扣成本上的差异。校准度要与准确率分开跟踪——如果模型判定流失概率为70%的客户真的有70%流失，留存预算就能按比例分配。同时监控漂移：特征分布、分数分布以及各群组的实际值与预测值之比，一旦季节性变化让这些指标移动，就重新验证模型。'),
    ('启动CLV预测最少需要哪些数据？',
     '两年带有客户标识、订单明细与商品毛利的交易历史，就足以构建第一个站得住脚的模型。互动信号（邮件、App、会员活动）与退货行为会显著提升准确度，对购买记录稀薄的新客尤其明显，但这些是增强项而非前提条件。真正不可妥协的是跨渠道的身份打通：缺少它，同一位客户会被算成两个人，模型会重复计算价值，再多数据也无法弥补。'),
]

TW_RENAMES = {
    '2025年AI驱動的行業轉型': '2025年AI如何重塑零售客戶價值管理？',
    '金融服務：AI作为競爭差异化因素': '零售能從金融服務業的即時評分中學到什麼？',
    '人机协作的必要性': '為什麼CLV決策中必須保留人工判斷？',
}


def run():
    b = {lg: stats(SLUG, lg) for lg in ('en', 'zh-cn', 'zh-tw')}
    process(SLUG, 'en', h2_renames=EN_RENAMES, inserts=EN_INSERTS, faq=EN_FAQ)
    process(SLUG, 'zh-cn', h2_renames=ZH_RENAMES, faq=ZH_FAQ)
    process(SLUG, 'zh-tw', h2_renames=TW_RENAMES, faq=[(s2tw(q), s2tw(a)) for q, a in ZH_FAQ])
    for lg in ('en', 'zh-cn', 'zh-tw'):
        print(lg, b[lg], '->', stats(SLUG, lg))


if __name__ == '__main__':
    run()
