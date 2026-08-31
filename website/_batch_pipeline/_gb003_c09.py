#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gbatch_003 slug 09 — ai-deployment-timeline-reality"""
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb003_lib import process, stats, tw_renames
from _gb001_s2t import s2tw

SLUG = 'ai-deployment-timeline-reality'

EN_RENAMES = {
    'Why it matters': 'Why Does the AI Deployment Timeline Matter So Much?',
    'Common challenges': 'What Actually Causes Deployment Timelines to Slip?',
    'How to get started': 'How Should You Start an AI Deployment?',
    'How to keep the timeline honest': 'How Do You Keep an AI Deployment Timeline Honest?',
    'Key takeaways': 'What Are the Key Takeaways About AI Deployment Timelines?',
}

EN_INSERTS = [
    ('Which Variables Actually Control the Deployment Calendar?',
     'which-variables-actually-control-the-deployment-calendar',
     '<p>Deployment duration is not a property of the model. It is a function of four variables that leaders can see before the project starts — and can change, if they choose to, before the first line of code is written.</p>'
     '<ol>'
     '<li><strong>Data readiness.</strong> The single largest driver. If the data the workflow needs is already governed, catalogued, and refreshed on a known schedule, weeks disappear from the plan. If it must be located, reconciled, and cleansed first, each additional ungoverned source adds two to six weeks, and the discovery usually happens after the schedule is already committed.</li>'
     '<li><strong>Ownership.</strong> A program with a named executive owner and a business metric moves at a different pace from one owned by a committee waiting for requirements. Ownership is the cheapest variable to fix and the one most often left ambiguous, because naming an owner means naming someone accountable for the date.</li>'
     '<li><strong>Integration scope.</strong> The model is rarely the project; wiring the output into ERP, CRM, case management, or messaging is. Scope one system and one workflow for the first deployment, and the integration estimate becomes credible. Scope a platform transformation and the estimate becomes fiction.</li>'
     '<li><strong>Operating discipline.</strong> Security review, compliance sign-off, monitoring, and retraining need dates in the plan at the start. Triggered late, at full scale, they add a quarter; scheduled up front, they run in parallel with build.</li>'
     '</ol>'
     '<p>The useful exercise before committing to any date is to grade each variable honestly — green, amber, or red — and to state the grade in the charter. When a date slips, the diagnosis is then a specific wrong assumption rather than a general failure of effort, and the recovery plan writes itself.</p>'),

    ('What Should the First 90 Days Look Like Week by Week?',
     'what-should-the-first-90-days-look-like-week-by-week',
     '<p>A well-scoped first deployment fits into roughly thirteen weeks. The sequence below assumes governed data and a named owner; add time where either is missing.</p>'
     '<ul>'
     '<li><strong>Weeks 1–2 — define done.</strong> Write down the decision the system will improve, the metric, the owner, and what "production" means. Connect the minimum data needed and confirm quality. Deliverable: a one-page charter with a definition of done that a non-technical executive can read.</li>'
     '<li><strong>Weeks 3–4 — build the retrieval or feature path.</strong> Stand up the pipeline on live data, not a curated sample. This is where hidden data defects surface, and surfacing them now is the point.</li>'
     '<li><strong>Weeks 5–8 — model, evaluate, and iterate with users.</strong> Run against a golden set of real questions, and put the output in front of the people who will use it twice a week. Adoption problems discovered in week six are cheap; discovered in week thirteen are the reason projects are called failures.</li>'
     '<li><strong>Weeks 9–11 — integrate and harden.</strong> Wire the output into the one workflow it serves, complete security and compliance review, add monitoring and a documented retraining schedule.</li>'
     '<li><strong>Weeks 12–13 — go live and measure.</strong> Launch with a control group or a clear before/after comparison, and report the outcome in business terms: the decision improved, by how much, at what cost.</li>'
     '</ul>'
     '<p>Two practices make the difference between this sequence and a slip. Hold a hard gate at the end of each phase: either the artefact exists or the scope shrinks. And report progress as outcomes — "forecast error fell 20 percent and the pricing team adopted it" — never as activity, because "we have built a great model" is not progress and everyone in the room knows it.</p>'),

    ('Where Does Build-versus-Buy Change the Deployment Timeline?',
     'where-does-build-versus-buy-change-the-deployment-timeline',
     '<p>Timeline is the most honest lens for the build-or-buy decision, because it exposes the cost that business cases usually hide: the months between starting and having anything in production.</p>'
     '<p>Building the analytics surface layer internally — the interface, the semantic layer, the connectors, the permissions model — is a multi-quarter programme that consumes data engineering capacity that is already contested. Buying it as a managed service compresses that portion of the calendar to about two weeks, because the work becomes configuration against data that already exists rather than construction. The distinction that matters is which parts are genuinely specific to your environment: the data model, the metric definitions, and the workflow integration must be built, but the governed access layer that sits on top of them does not have to be.</p>'
     '<p>The second-order effect is on the rest of the portfolio. Every quarter spent building the access layer is a quarter not spent on the decisions that create value, and the opportunity cost of delayed decisions compounds monthly. Organisations that buy the commodity layer and build only what differentiates them typically land their first deployment inside a quarter and their second in weeks, because the foundation now exists.</p>'
     '<p>The test to apply: for each component, ask whether a competitor would build it the same way. If the answer is yes, it is a commodity, and buying it is a schedule decision rather than a procurement one.</p>'),
]

EN_FAQ = [
    ('How long does enterprise AI actually take to deploy?',
     'With governed data and a named owner, a first production deployment typically takes twelve to sixteen weeks: two to four weeks to define the decision and data scope, four to eight weeks to stand up the pipeline and model on live data, and two to four weeks for integration, security review, and go-live. Without data foundations, timelines stretch toward a year or more, and many stalled projects never arrive at all. The twelve-to-sixteen-week figure is for the parts that must be built for your environment; the commodity parts should be bought.'),
    ('Why do so many AI projects fail to reach production?',
     'The commonly cited failure rates — as high as 85 percent, with Gartner projecting 30 percent of generative AI projects abandoned after proof of concept — trace to four controllable variables: data readiness, unclear ownership, integration scope, and operating discipline. Technology is rarely the binding constraint. Projects fail because data reconciliation was discovered after modelling started, because no one owned the business metric, because integration quietly became a platform programme, or because security review was triggered at full scale at the end.'),
    ('Can any part of AI deployment be genuinely fast?',
     'Yes: the analytics surface. A governed, conversational BI layer can be deployed in about two weeks as a managed service, because it standardises the access layer rather than building bespoke integration for it. That is why conversational analytics is often the first AI deployment to land on time — it sits on governed data that already exists, and it delivers visible value while longer-cycle modelling programmes are still in their data phase.'),
    ('How should we set expectations with the board?',
     'Name the assumptions in the charter and report against them. State the data readiness level, the integration scope, and the owner explicitly, and revisit them at every checkpoint — when a date slips, the diagnosis should be which assumption was wrong. Then report outcomes rather than activity: a trained model is not progress, an improved decision is. Boards respond to a timeline framed as a sequence of business outcomes with gates between them, because that gives them a non-technical way to steer.'),
    ('What should we do in the first week?',
     'Write the definition of done, name the accountable owner, and audit the data the workflow needs. Those three steps take a week and determine the calendar more than any subsequent engineering decision. Specifically: one page stating the decision to be improved, the metric, the owner, and what counts as production; a named executive accountable for the date; and an honest assessment of whether the required data is governed, complete, and fresh enough to model on.'),
]

ZH_RENAMES = {
    '为什么重要': '为什么AI部署周期如此重要？',
    '常见挑战': '导致部署周期延期的真正原因是什么？',
    '如何开始': '企业应该如何启动AI部署？',
    '核心要点': '关于AI部署周期，有哪些核心要点？',
}

ZH_INSERTS = [
    ('一个现实的企业AI部署周期分为哪几个阶段？',
     '一个现实的企业AI部署周期分为哪几个阶段？',
     '<p>把周期拆开看，企业AI部署并不是一段无法预测的漫长时间，而是由几个边界清晰的阶段组成。理解每个阶段的输入与产出，是把"黑箱承诺"变成"可管理里程表"的第一步。</p>'
     '<ol>'
     '<li><strong>界定与对齐阶段（2到4周）。</strong>明确要改善的决策、指标、责任人，以及"什么算上线"。同时接入最少必需的数据，确认质量与权限现状。产出是一页纸的项目章程。</li>'
     '<li><strong>数据与管道阶段（4到8周）。</strong>在真实数据（而不是精心挑选的样本）上搭建管道。这一步的价值恰恰在于让隐藏的数据缺陷尽早暴露——数据清洗通常占据整个周期的40%以上，而这一比例在立项时几乎总是被低估30%到50%。</li>'
     '<li><strong>建模与验证阶段（3到6周）。</strong>用真实问题集验证输出，并让最终使用者每周至少看两次结果。第六周发现的采用问题成本很低，第十三周才发现则往往直接决定项目成败。</li>'
     '<li><strong>集成与加固阶段（2到4周）。</strong>把输出接进唯一的目标工作流，完成安全与合规评审，配置监控与再训练计划。系统集成中的权限与合规审批几乎总比计划更慢，建议在计划中预留15%到20%的缓冲。</li>'
     '<li><strong>上线与度量阶段（持续）。</strong>带对照组或明确的前后对比上线，并用业务语言汇报结果：哪个决策改善了多少、花了多少成本。</li>'
     '</ol>'
     '<p>把这几个阶段加总，在数据与治理基础具备的情况下，首次生产上线大致落在十二到十六周；基础不具备时，每个不受治理的数据源、每套缺失的治理框架，都会以"月"为单位追加时间。领导者如果把这些基础工作明确写进预算，就能保住信誉；如果把它藏起来，就会在时间线滑落时同时失去时间与信任。</p>'),

    ('哪些因素最常导致部署周期被低估？',
     '哪些因素最常导致部署周期被低估？',
     '<p>延期往往不是一次大失误，而是多次小误判的叠加。以下四类因素在实践中出现频率最高，也最容易被写进计划时忽略。</p>'
     '<ul>'
     '<li><strong>数据准备被低估。</strong>团队在干净样本上完成了原型，接上生产数据后才发现口径不一、到达时间不稳定、血缘不清。这类问题通常在建模开始之后才被发现，因此代价最大。</li>'
     '<li><strong>责任人不明确。</strong>有具名业务负责人与明确指标的项目，与由委员会"等待需求"的项目，推进速度完全不在一个量级。明确责任人几乎不花钱，却最常被搁置，因为具名意味着要为日期负责。</li>'
     '<li><strong>集成范围悄然扩大。</strong>试点在推进中变成平台转型，验收标准却始终没有被写下来。没有"做到什么程度算成功"的定义，项目就会在无限迭代中失去终点。</li>'
     '<li><strong>安全与合规评审被放在最后。</strong>在全量规模上触发评审，通常会追加一个季度；而如果一开始就排进计划，它可以与开发并行推进。</li>'
     '</ul>'
     '<p>对应的做法是在项目章程里把每一项标成绿、黄、红三档，并在每个检查点复核。一旦日期滑落，诊断就能落到"哪一项假设错了"，而不是笼统地要求团队"再加把劲"。麦肯锡的研究显示约70%的数字化转型项目未能达到预期目标，AI部署作为其中难度最高的环节，靠的不是更强的执行力，而是更早暴露假设错误的管理机制。</p>'),

    ('如何用门禁机制把部署周期管起来？',
     '如何用门禁机制把部署周期管起来？',
     '<p>管理部署周期最有效的工具不是更细的甘特图，而是阶段门禁：每一个阶段结束时，要么拿出约定的交付物，要么主动缩小范围。这个机制把"延期"从一个需要解释的事件，变成一个在设计内可控的选择。</p>'
     '<p>具体做法有三点。第一，为每个阶段定义可验证的交付物，而不是"完成度百分比"：章程一页纸、数据质量基线报告、真实问题集的评估结果、集成后的端到端演示、上线后的对照组数据。第二，把门禁评审固定在月度节奏上，由业务负责人而非技术团队主持，因为只有业务方有权在"扩大范围"与"保住日期"之间做出取舍。第三，为每个门禁准备一个预设的降级方案——如果这一阶段只交付了部分能力，缩小到哪个范围仍然可以上线。</p>'
     '<p>同时要维护一份风险登记册，每两周更新一次，并明确每项风险的应对措施。这样延期在发生之前就被识别，而不是发生之后被迫解释。经验表明，坚持门禁机制的项目，其首次上线时间未必最快，但按期交付的比例显著更高，而且每一次延期都能换来一个具体的、可复用的经验——这正是让第二个、第三个AI项目越做越快的复利所在。</p>'),
]

ZH_FAQ = [
    ('企业AI部署到底需要多长时间？',
     '在数据已受治理且有具名负责人的情况下，首次生产上线通常需要十二到十六周：两到四周界定决策与数据范围，四到八周在真实数据上搭建管道与模型，两到四周完成集成、安全评审与上线。如果缺乏数据基础，周期会拉长到一年甚至更久，而大量停滞的项目从未真正上线。需要注意的是，十二到十六周是为你的环境"必须自建"的部分预留的；通用部分应该直接采购。'),
    ('为什么这么多AI项目无法进入生产？',
     '常被引用的失败率（最高达85%，Gartner曾预测30%的生成式AI项目会在概念验证后被放弃）可以归因到四个可控变量：数据就绪度、责任归属、集成范围与运营纪律，技术本身很少是约束条件。项目失败的典型路径是：建模开始后才发现数据对账问题、没有人真正拥有业务指标、集成在无声无息中变成平台工程、或者安全评审在全量规模上才被触发。'),
    ('AI部署中有没有哪一部分是真的可以很快？',
     '有——分析表层。受治理的对话式BI层以托管服务方式部署，通常两周即可上线，因为它标准化的是访问层，而不是为每个场景做定制集成。这也是为什么对话式分析往往是第一个按时落地的AI应用：它建立在已经存在的受治理数据之上，并且在长周期建模项目还在处理数据阶段时，就已经交付了可见的业务价值。'),
    ('应该如何向董事会设定预期？',
     '把假设写进章程，并按假设汇报。明确写出数据就绪度、集成范围与责任人，在每个检查点复核——一旦日期滑落，诊断应该落到"哪一项假设错了"。同时按结果而非活动汇报：模型训练完成不是进展，决策被改善才是。董事会对"一串带门禁的业务结果"这种表述反应最好，因为它提供了不依赖技术细节的抓手来进行方向调整。'),
    ('第一周应该做什么？',
     '写下"完成的定义"、指定责任人、并审计工作流所需的数据。这三件事一周内可以完成，却比之后任何工程决策都更能决定整个周期。具体来说：一页纸说明要改善的决策、指标、责任人以及什么算生产上线；一位对日期负责的业务高管；以及对所需数据是否已受治理、是否完整、是否足够新鲜以支撑建模的诚实评估。'),
]


def run():
    b = {lg: stats(SLUG, lg) for lg in ('en', 'zh-cn', 'zh-tw')}
    process(SLUG, 'en', h2_renames=EN_RENAMES, inserts=EN_INSERTS, faq=EN_FAQ, drop_body_faq=True)
    process(SLUG, 'zh-cn', h2_renames=ZH_RENAMES, inserts=ZH_INSERTS, faq=ZH_FAQ, drop_body_faq=True)
    tw_ins = [(s2tw(h), i, s2tw(bd)) for h, i, bd in ZH_INSERTS]
    process(SLUG, 'zh-tw', h2_renames=tw_renames(SLUG, ZH_RENAMES, s2tw), inserts=tw_ins,
            faq=[(s2tw(q), s2tw(a)) for q, a in ZH_FAQ], drop_body_faq=True,
            cta_fix=('預約演示', '預約示範'))
    for lg in ('en', 'zh-cn', 'zh-tw'):
        print(lg, b[lg], '->', stats(SLUG, lg))


if __name__ == '__main__':
    run()
