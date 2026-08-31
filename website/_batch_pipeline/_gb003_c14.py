#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gbatch_003 slug 14 — ai-driven-demand-forecasting-q4-retail-nov2025"""
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb003_lib import process, stats, tw_renames
from _gb001_s2t import s2tw

SLUG = 'ai-driven-demand-forecasting-q4-retail-nov2025'

EN_RENAMES = {
    'Key Benefits and ROI Considerations':
        'What Is the Return on AI Demand Forecasting?',
    'Implementation Roadmap and Next Steps':
        'What Does a Q4 Forecasting Roadmap Look Like?',
}

EN_INSERTS = [
    ('Which Signals Actually Improve a Q4 Forecast?',
     'which-signals-actually-improve-a-q4-forecast',
     '<p>More data does not automatically mean a better forecast, and adding signals without testing them is how forecasting projects lose credibility. Five categories consistently earn their place in a holiday model, and two usually do not.</p>'
     '<ul>'
     '<li><strong>Promotion and price calendar.</strong> The single highest-value external signal. A forecast that does not know which week a SKU goes on promotion will misread the resulting spike as organic demand and repeat the error next year.</li>'
     '<li><strong>Weather.</strong> Materially improves short-horizon forecasts for weather-sensitive categories, and it is the signal most likely to change an allocation decision within the week.</li>'
     '<li><strong>Digital demand signals.</strong> Search interest, product page views, and add-to-cart rates lead transactions by days, which matters most for new products with no sales history.</li>'
     '<li><strong>Inventory and fulfilment constraints.</strong> Forecasts should know what can actually be delivered; unconstrained demand forecasts drive allocation decisions that cannot be executed.</li>'
     '<li><strong>Channel mix.</strong> Online and store demand behave differently under promotion, and a blended forecast hides both.</li>'
     '</ul>'
     '<p>The two that usually disappoint are social sentiment, which is noisy and rarely beats search or traffic data once both are in the model, and macroeconomic indicators, which move far too slowly to help within a quarter. Test every signal against a holdout period rather than adding it on intuition, and keep the feature set small enough that planners can still explain why the forecast moved.</p>'),

    ('How Should You Measure Forecast Accuracy Honestly?',
     'how-should-you-measure-forecast-accuracy-honestly',
     '<p>Forecast accuracy is the metric everyone quotes and nearly everyone computes differently. Three decisions determine whether the number means anything, and all three should be written down before the season starts.</p>'
     '<ol>'
     '<li><strong>Weighted, not average.</strong> A 10 percent error on a bestseller costs far more than a 40 percent error on a long-tail item. Weight by revenue or margin contribution so the metric reflects commercial impact, and report the unweighted figure alongside it so nobody can accuse anyone of cherry-picking.</li>'
     '<li><strong>At the level where decisions happen.</strong> Item-store-day accuracy is what allocation and replenishment act on. Category-level accuracy can look excellent while the store-level forecast driving a truck is badly wrong.</li>'
     '<li><strong>Against a real baseline.</strong> The comparison is the current process — last year plus lift, or the existing statistical model — measured on the same period and the same SKUs. "Twenty to fifty percent error reduction" only means something when the denominator is stated.</li>'
     '</ol>'
     '<p>Track bias separately from error. A forecast that is consistently 8 percent high is easier to fix and less damaging than one that is unbiased but volatile, and bias is invisible in an absolute-error metric. Then connect accuracy to the outcome that matters: stockout rate on top sellers, markdown depth in the final two weeks, and freight expediting cost. Those three are what the CFO sees, and they are the reason the forecasting programme keeps its budget.</p>'),

    ('What Goes Wrong in Q4 Forecasting, and How Do You Prevent It?',
     'what-goes-wrong-in-q4-forecasting-and-how-do-you-prevent-it',
     '<p>The holiday quarter fails in specific, repeatable ways. Six failure modes account for most of the damage, and each has a control that can be put in place before the season rather than during it.</p>'
     '<ul>'
     '<li><strong>Promotion leakage.</strong> The model learned last year\'s promotional spikes as baseline demand and over-forecasts the same weeks. Control: feed the promotion calendar as an explicit feature and hold out promotional weeks during validation.</li>'
     '<li><strong>New product cold start.</strong> Seasonal SKUs with no history get flat, conservative forecasts and sell out in week one. Control: forecast new items from attribute similarity to comparable products, and re-forecast weekly once sales begin.</li>'
     '<li><strong>Channel shift blindness.</strong> Demand moves between online and store and the blended forecast misses both. Control: forecast channel separately and reconcile to the total.</li>'
     '<li><strong>Forecast frozen too long.</strong> The plan is set in September and never revised, so October sell-through never reaches the allocation. Control: a weekly re-forecast cadence with a named owner and a defined cut-off for changing orders.</li>'
     '<li><strong>Planner override without feedback.</strong> Planners adjust the model and nobody measures whether the adjustment helped. Control: log overrides, compare override versus model accuracy, and feed the result back into both.</li>'
     '<li><strong>Unconstrained output.</strong> The forecast assumes fulfilment that does not exist. Control: constrain by available inventory and lead time before the plan reaches allocation.</li>'
     '</ul>'
     '<p>The retailers that handle these six well are not the ones with the most sophisticated models. They are the ones whose planners trust the number enough to act on it — which is why the feedback loop on overrides matters more than any algorithm choice.</p>'),

    ('How Does Conversational Access Change Forecasting Practice?',
     'how-does-conversational-access-change-forecasting-practice',
     '<p>Most forecasting value is lost after the number is produced. A planner who has to wait three days for a segmented view of the forecast will act on the summary they already have, and the nuance that would have changed the allocation never reaches the decision.</p>'
     '<p>Conversational access closes that gap. When a planner can ask, in the messaging tool they already use, "which stores are tracking above forecast for these five SKUs this week, and what is the cover remaining?" and receive a governed answer computed on the current data, the forecast becomes something they interrogate continuously rather than a file they receive monthly. Three requirements make this safe in a governed environment: the query runs against the same semantic definitions the planning team maintains, access is filtered by role and region, and every answer carries its source and timestamp so it can be reconciled later.</p>'
     '<p>The behavioural change is the point. Forecasts that are easy to question get questioned, and questioning is how bias, cold-start problems, and channel shifts surface early enough to act on. Deployed as a managed service on top of existing infrastructure, this layer can be live in about two weeks — which means it can be in place before the Q4 peak rather than after it.</p>'),
]

EN_FAQ = [
    ('How much can AI improve retail demand forecasting?',
     'McKinsey research found that machine-learning demand forecasting can reduce forecast error by 20 to 50 percent, cut lost sales from stockouts by up to 65 percent, and lower warehousing and freight costs by 5 to 10 percent. No other Q4 initiative moves all three simultaneously. The size of the improvement depends on the baseline: retailers still using last-year-plus-lift spreadsheets see the largest gains, while those with mature statistical forecasting see smaller but still material improvements, mostly from richer external signals and finer granularity.'),
    ('When should Q4 forecasting work start?',
     'The accuracy is earned in the months before Black Friday, not during it. Start signal integration and model validation in late summer, run the model in shadow mode alongside the existing process through September and October so its accuracy can be measured against reality, and move to primary use from November with a weekly re-forecast cadence. Retailers that begin in November are validating and operating simultaneously, which is when forecast errors become inventory mistakes.'),
    ('What data does AI demand forecasting need?',
     'At minimum: two to three years of item-store-day sales history with price and promotion flags, current inventory and lead times, and the forward promotion calendar. The signals that add the most on top of that are weather, digital demand indicators such as search and add-to-cart rates, and channel-level sales. Macroeconomic indicators and social sentiment usually add little within a quarter. Every additional signal should be tested against a holdout period rather than added on intuition.'),
    ('How should forecast accuracy be measured?',
     'Weight it by revenue or margin contribution, because a 10 percent error on a bestseller costs far more than a 40 percent error on a long-tail item. Measure at the granularity decisions are made — item, store, day — rather than at category level, where a good average can hide store-level errors. Compare against the current process on the same period and SKUs, and state the baseline, because a percentage improvement is meaningless without its denominator. Track bias separately from absolute error, and connect accuracy to stockouts, markdown depth, and expediting cost.'),
    ('Do AI forecasts replace demand planners?',
     'No. AI handles the volume and the signal processing — item-store-day forecasts across thousands of SKUs refreshed continuously — while planners contribute the judgement the model cannot see: a competitor opening nearby, a supplier change, or a marketing decision that has not been entered anywhere. The productive pattern is a model that produces the baseline and a planner who owns the exception, with every override logged and measured so the system learns which human adjustments actually improve accuracy.'),
]

ZH_RENAMES = {
    '核心收益与投资回报考量': 'AI需求预测的回报体现在哪里？',
    '实施路线图与后续步骤': 'Q4预测路线图应该包含哪些步骤？',
    '案例分析与行业洞察': '有哪些值得借鉴的实战案例？',
    '未来展望与行动建议': '下一个旺季企业应该做什么？',
    '关键成功因素与常见陷阱': '成功的关键因素与常见陷阱是什么？',
    '蜂启咨询的专业洞察': '蜂启咨询如何看待AI需求预测？',
}

ZH_FAQ = [
    ('AI能把零售需求预测改善多少？',
     '麦肯锡的研究发现，机器学习需求预测可将预测误差降低20%到50%，将缺货造成的销售损失最多降低65%，并把仓储与运输成本降低5%到10%。没有任何其他Q4举措能同时改善这三个数字。改善幅度取决于基线：仍在使用"去年加提升系数"表格的零售商收益最大，而已经具备成熟统计预测的企业收益较小但仍然显著，主要来自更丰富的外部信号与更细的颗粒度。'),
    ('Q4预测工作应该什么时候启动？',
     '准确度是在黑色星期五之前的几个月里挣来的，而不是在旺季期间。建议在夏末启动信号接入与模型验证，九到十月让模型以影子模式与现有流程并行运行，以便用实际结果检验其准确度；从十一月起转为主用，并保持每周重新预测的节奏。到了十一月才开始的企业，等于把验证与上线压在同一时间，而此时预测错误已经会直接变成库存错误。'),
    ('AI需求预测需要哪些数据？',
     '至少需要：两到三年带有价格与促销标记的单品-门店-日销售历史、当前库存与提前期、以及未来的促销日历。在此基础上增益最大的信号包括天气、搜索与加购率等数字需求指标，以及分渠道销售。宏观指标与社交情绪在一个季度之内通常帮助有限。每一个新增信号都应该针对留出期进行检验，而不是凭直觉加入。'),
    ('预测准确度应该如何衡量？',
     '要按收入或毛利贡献加权，因为畅销品10%的误差，其代价远高于长尾商品40%的误差。要在决策发生的颗粒度上衡量——单品、门店、日——而不是在品类层面，因为良好的平均值可能掩盖门店层面的严重错误。要在相同时间段与相同SKU上与现有流程对比，并明确写出基线，因为缺少分母的百分比改善没有意义。此外要把偏差与绝对误差分开跟踪，并把准确度关联到缺货率、降价深度与加急运输成本。'),
    ('AI预测会取代需求计划人员吗？',
     '不会。AI处理的是规模与信号处理——覆盖数千个SKU、持续刷新的单品-门店-日预测；而计划人员贡献的是模型看不到的判断：附近新开的竞争对手、供应商的变更、或还没有被录入任何系统的营销决策。高效的模式是：模型产出基线，计划人员负责例外，并且每一次人工调整都被记录与衡量，让系统逐渐学会哪些人工干预确实提升了准确度。'),
]


def run():
    b = {lg: stats(SLUG, lg) for lg in ('en', 'zh-cn', 'zh-tw')}
    process(SLUG, 'en', h2_renames=EN_RENAMES, inserts=EN_INSERTS, faq=EN_FAQ)
    process(SLUG, 'zh-cn', h2_renames=ZH_RENAMES, faq=ZH_FAQ, drop_body_faq=True)
    process(SLUG, 'zh-tw', h2_renames=tw_renames(SLUG, ZH_RENAMES, s2tw),
            faq=[(s2tw(q), s2tw(a)) for q, a in ZH_FAQ], drop_body_faq=True)
    for lg in ('en', 'zh-cn', 'zh-tw'):
        print(lg, b[lg], '->', stats(SLUG, lg))


if __name__ == '__main__':
    run()
