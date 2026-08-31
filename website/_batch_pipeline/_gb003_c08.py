#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gbatch_003 slug 08 — ai-data-quality-framework-year-end-nov2025"""
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb003_lib import process, stats, tw_renames
from _gb001_s2t import s2tw

SLUG = 'ai-data-quality-framework-year-end-nov2025'

EN_RENAMES = {
    'The Five Dimensions That Determine AI-Readiness':
        'Which Five Dimensions Determine Whether Your Data Is AI-Ready?',
    'Key Benefits and ROI Considerations':
        'What Is the Return on a Data Quality Framework?',
    'Implementation Roadmap and Next Steps':
        'What Should a Year-End Data Quality Roadmap Contain?',
}

EN_INSERTS = [
    ('How Do You Score Each Dimension Without Boiling the Ocean?',
     'how-do-you-score-each-dimension-without-boiling-the-ocean',
     '<p>A year-end review loses credibility when it tries to grade the entire estate. Score the data that AI actually touches: the tables, documents, and retrieval sources behind the use cases already in production or planned for next year. For each, a simple 0–3 rubric per dimension is enough, and the rubric should be written so two people reach the same score.</p>'
     '<ul>'
     '<li><strong>Completeness.</strong> 0 = critical fields largely empty; 1 = populated but with untracked nulls; 2 = nulls tracked and reported; 3 = nulls tracked, thresholded, and alerted with an owner.</li>'
     '<li><strong>Accuracy.</strong> 0 = never validated against source; 1 = validated once; 2 = spot-audited on a schedule; 3 = automated reconciliation against source with exception handling.</li>'
     '<li><strong>Consistency.</strong> 0 = conflicting definitions across systems; 1 = definitions documented but not enforced; 2 = enforced in the warehouse; 3 = enforced in a shared semantic layer used by every consumer including AI.</li>'
     '<li><strong>Timeliness.</strong> 0 = unknown freshness; 1 = batch with no SLA; 2 = SLA defined and monitored; 3 = SLA met at p95 with visible timestamps to end users.</li>'
     '<li><strong>Accessibility.</strong> 0 = manual extracts; 1 = queryable but ungoverned; 2 = governed with role-based access; 3 = governed, documented, and reachable through the same interface the AI uses.</li>'
     '</ul>'
     '<p>Any dimension scoring 0 or 1 on an asset that feeds a production AI system is a remediation item for next quarter, and it should be costed. The output of the review is not a report — it is a ranked list of specific defects with owners and a business consequence attached to each, which is the only form in which data quality work competes successfully for budget.</p>'),

    ('Which Data Quality Failures Cause the Most AI Damage?',
     'which-data-quality-failures-cause-the-most-ai-damage',
     '<p>Not all defects are equal once an AI system is in front of them. Five failure patterns account for most of the wrong answers enterprises saw in 2025, and each has a specific detector.</p>'
     '<ul>'
     '<li><strong>Silent nulls.</strong> A model does not ask for missing data; it substitutes an assumption and answers confidently. Detector: null-rate monitoring on every field in the retrieval or feature path, with a hard failure when a critical field exceeds threshold.</li>'
     '<li><strong>Conflicting definitions.</strong> "Active customer" means three things in three systems, so the same question returns different numbers depending on which table was reached. Detector: a single governed semantic layer, plus a reconciliation test that runs the same metric across sources and alerts on divergence.</li>'
     '<li><strong>Stale retrieval sources.</strong> The warehouse is fresh but the policy document the assistant quotes was superseded two quarters ago. Detector: freshness SLAs per source, with the last-updated timestamp shown alongside every AI answer.</li>'
     '<li><strong>Duplicate identities.</strong> The same customer or supplier appears twice, so aggregates double-count and per-customer values halve. Detector: match-rate monitoring on identity resolution, reported as a first-class data quality metric.</li>'
     '<li><strong>Broken lineage after change.</strong> An upstream schema change silently alters a metric and nobody notices until an answer looks wrong. Detector: contract tests on upstream schemas and automated lineage diffing on every deployment.</li>'
     '</ul>'
     '<p>What makes these expensive is not the error rate but the confidence of the delivery. A dashboard that looks odd triggers suspicion; an assistant that answers fluently does not. That is why the detectors must be automated rather than reviewed — human scepticism is the one control AI systems reliably defeat.</p>'),

    ('How Should the Year-End Review Feed Next Year\'s Plan?',
     'how-should-the-year-end-review-feed-next-years-plan',
     '<p>The review is only worth running if it changes the plan. Three outputs convert scores into budget and sequencing.</p>'
     '<ol>'
     '<li><strong>A ranked remediation backlog.</strong> Order defects by the business value of the decisions they corrupt, not by technical ease. A 2 percent error in the demand signal feeding Q4 replenishment outranks a 40 percent null rate in a field nobody queries.</li>'
     '<li><strong>A named owner per defect class.</strong> Data quality improves when someone is accountable for a metric, not for a project. Assign the recurring classes — nulls, definitions, freshness, identity — to the stewards who own those domains, and give them the monitoring to see regressions.</li>'
     '<li><strong>A baseline for next year\'s AI business case.</strong> Record the current scores and the current incident rate, because every AI investment next year will be judged against them. When a model performs better in March, the improvement attributable to upstream quality work becomes visible — and that attribution is what keeps the data foundation funded.</li>'
     '</ol>'
     '<p>Sequence the work in two waves. The first wave, in the first quarter, fixes the defects on assets that feed production AI — that is where the compounding damage is happening now. The second wave builds the preventive layer: semantic definitions, contract tests, and monitoring that make the next defect visible before a model consumes it. Organisations that run the review this way stop treating data quality as an annual clean-up and start treating it as the reason their AI answers can be trusted.</p>'),
]

EN_FAQ = [
    ('Why does data quality matter more for AI than for dashboards?',
     'Because AI multiplies the damage. A dashboard serving stale numbers causes one bad decision and usually looks suspicious enough to be questioned. A language model that ingests the same stale numbers restates them confidently to every employee who asks, hundreds of times a day, with no hesitation and no visible caveat. Gartner has estimated poor data quality costs organisations an average of $12.9 million per year, and that estimate predates the AI era — under conversational AI, the same defect becomes a systematic source of wrong answers across the organisation rather than an occasional forecast error.'),
    ('Which data quality dimension should be fixed first?',
     'Consistency, in most enterprises. Conflicting definitions of the same concept — a customer, a product, a region — cause joins to drop or duplicate records and make the same question return different answers depending on which system was reached. That is the defect most likely to produce a confidently wrong AI answer, and it is also the one with the clearest fix: a governed semantic layer that enforces one definition for every consumer, including AI systems. Completeness and accuracy are close behind and are usually cheaper to remediate once definitions are settled.'),
    ('How often should an AI-readiness data quality review be run?',
     'Formally, twice a year, with continuous monitoring in between. The year-end review sets the baseline and the remediation backlog for the coming year; a mid-year check confirms whether the scores moved. But the review should not be the primary detection mechanism — null rates, reconciliation results, freshness SLAs, and identity match rates should be monitored continuously with alerting and named owners, so that a regression is caught before an AI system consumes it rather than at the next review cycle.'),
    ('Is most enterprise "hallucination" actually a data quality problem?',
     'In enterprise settings, a large share of it is. When a model is grounded on retrieved data, the failure mode is usually that the retrieval returned incomplete, stale, duplicated, or inconsistent records — and the model faithfully and fluently reported them. That distinction matters commercially: prompt engineering and model swaps will not fix a broken retrieval source, while fixing null rates, definitions, and freshness usually will. Teams that instrument retrieval quality before tuning prompts see far larger improvements in answer correctness.'),
    ('How long does it take to make data AI-ready?',
     'For the assets behind one production use case, four to eight weeks is typical: one to two weeks to score the five dimensions on the assets in scope, two to four weeks to remediate the defects that affect live answers, and the remainder to automate the monitoring so regressions are caught. Enterprise-wide readiness is a twelve to eighteen month programme sequenced by decision value, which is why the year-end review should produce a ranked backlog rather than an estate-wide mandate.'),
]

ZH_RENAMES = {
    '核心收益与投资回报考量': '数据质量框架的回报体现在哪里？',
    '实施路线图与后续步骤': '年终数据质量路线图应该包含什么？',
    '案例分析与行业洞察': '有哪些值得借鉴的实践案例？',
    '未来展望与行动建议': '明年的数据质量工作该如何布局？',
    '关键成功因素与常见陷阱': '成功的关键因素与常见陷阱是什么？',
    '蜂启咨询的专业洞察': '蜂启咨询如何看待AI时代的数据质量？',
}

ZH_FAQ = [
    ('为什么数据质量对AI比对看板更重要？',
     '因为AI会把损害放大。看板展示了过期数字，通常只会导致一次错误决策，而且往往因为"看起来不对"而被质疑。但语言模型摄入同样的过期数据后，会自信地向每一个提问的员工复述它，一天成百上千次，没有迟疑，也没有任何提示。Gartner估算数据质量不佳每年给企业造成的损失平均为1290万美元，而这个估算还早于AI时代——在对话式AI之下，同一个缺陷不再是偶发的预测偏差，而是整个组织范围内系统性的错误答案来源。'),
    ('应该优先修复哪一个数据质量维度？',
     '大多数企业应该先解决一致性。同一个概念——客户、商品、区域——在不同系统中有不同定义，会导致关联时记录丢失或重复，并让同一个问题因命中的系统不同而给出不同答案。这是最可能导致AI给出"自信的错误答案"的缺陷，同时也是解法最清晰的：建立一个受治理的语义层，对所有消费方（包括AI系统）强制统一定义。完整性准确性紧随其后，而且一旦定义统一，这两项的修复成本通常会明显下降。'),
    ('AI就绪度的数据质量评估应该多久做一次？',
     '正式评估建议每半年一次，其间依靠持续监控。年终评估确立基线并生成来年的整改清单；年中复核确认分数是否移动。但评估不应是主要的发现机制——空值率、对账结果、新鲜度SLA与身份匹配率都应该持续监控，并设置告警与明确责任人，让回退在AI系统消费之前就被发现，而不是等到下一个评估周期。'),
    ('企业中的"幻觉"大部分其实是数据质量问题吗？',
     '在企业场景中，相当比例确实如此。当模型基于检索到的数据作答时，失败通常是因为检索返回了不完整、过期、重复或不一致的记录，而模型忠实且流畅地把它们复述出来。这个区分在商业上很重要：提示词工程和更换模型都修不好一个坏的检索源，而修复空值率、定义与新鲜度通常可以。先度量检索质量再调提示词的团队，答案正确率的提升要大得多。'),
    ('让数据达到AI就绪需要多长时间？',
     '就一个已上线用例背后的数据资产而言，通常需要四到八周：一到两周对范围内的资产按五个维度打分，两到四周修复影响当前答案的缺陷，其余时间用于把监控自动化以便捕捉回退。全企业范围的就绪是一个按决策价值排序、持续十二到十八个月的项目，这也正是年终评估应该产出"排序后的整改清单"而不是"全量整改令"的原因。'),
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
