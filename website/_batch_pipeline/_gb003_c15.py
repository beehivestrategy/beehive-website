#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gbatch_003 slug 15 — ai-driven-internal-audit-enterprise-2025"""
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb003_lib import process, stats, tw_renames
from _gb001_s2t import s2tw

SLUG = 'ai-driven-internal-audit-enterprise-2025'

EN_RENAMES = {
    'Key Benefits and ROI Considerations':
        'What Is the Return on AI in Internal Audit?',
    'Implementation Roadmap and Next Steps':
        'What Does an AI Adoption Roadmap Look Like for Internal Audit?',
}

EN_INSERTS = [
    ('Where Does AI Fit in the Audit Lifecycle?',
     'where-does-ai-fit-in-the-audit-lifecycle',
     '<p>AI earns its place at four points in the audit lifecycle, and the maturity of each application is very different — which is why sequencing matters more than ambition.</p>'
     '<ol>'
     '<li><strong>Risk assessment.</strong> AI scans the full population of transactions and external signals to rank entities, processes, and accounts by risk, replacing an annual judgement built largely on last year\'s plan. This is the highest-value and lowest-risk application, because it informs where auditors spend time rather than concluding anything.</li>'
     '<li><strong>Full-population testing.</strong> Every journal entry, approval, and payment is tested against the control rules, and only exceptions reach a human. This is where the sampling-to-coverage shift actually happens, and it requires well-defined control logic before it produces anything usable.</li>'
     '<li><strong>Continuous monitoring.</strong> Controls are tested on a schedule rather than at a point in time, so a control failure is detected in days instead of at the next audit cycle. This is the hardest to operationalise, because it needs stable data feeds and a defined response path for every alert.</li>'
     '<li><strong>Evidence assembly and workpaper support.</strong> AI retrieves and structures the documentation supporting each test. High value, low controversy, and usually the best place to start because it demonstrates benefit without touching audit conclusions.</li>'
     '</ol>'
     '<p>The pattern across successful functions is to start with risk assessment and evidence support, prove the data access model, then move to full-population testing, and treat continuous monitoring as a second-year objective. Functions that start with monitoring typically stall, because there is no proven data pipeline to monitor from.</p>'),

    ('What Evidence Does an AI-Assisted Audit Need to Withstand?',
     'what-evidence-does-an-ai-assisted-audit-need-to-withstand',
     '<p>An AI-assisted audit conclusion must be defensible to three audiences: the audit committee, the external auditor, and — increasingly — the regulator. That requirement produces four evidence obligations that are easier to satisfy if they are designed in rather than reconstructed later.</p>'
     '<ul>'
     '<li><strong>Reproducibility.</strong> The same inputs and the same model version must produce the same result, months later. That means versioned data snapshots, versioned model artefacts, and a record of the parameters used for each run.</li>'
     '<li><strong>Traceability.</strong> Every exception raised must be traceable to the specific records and the specific rule that flagged them. An auditor cannot escalate an anomaly they cannot reconstruct, and a control owner will not accept a finding that cannot be shown.</li>'
     '<li><strong>Complete coverage, honestly stated.</strong> If the test covered 94 percent of the population because two systems could not be reached, that gap belongs in the workpaper. Claiming full-population testing while silently excluding sources is the fastest way to lose an external auditor\'s trust.</li>'
     '<li><strong>Human judgement recorded.</strong> Where an auditor overrode or accepted a model output, the reasoning belongs in the file. The model proposes; the auditor concludes; and the record has to show which was which.</li>'
     '</ul>'
     '<p>Functions that meet these four obligations find the external audit relationship improves rather than complicates: the external auditor can test the audit function\'s own work more efficiently, because the population, the logic, and the exceptions are all evidence rather than narrative.</p>'),

    ('Which Risks Does AI Introduce Into the Audit Function Itself?',
     'which-risks-does-ai-introduce-into-the-audit-function-itself',
     '<p>Auditing with AI creates risks that the function is professionally obligated to manage, and the credibility cost of ignoring them is higher here than in any other function.</p>'
     '<ul>'
     '<li><strong>Automation bias.</strong> Auditors defer to the model\'s output because it looks rigorous. The countermeasure is structural: require a documented reason for accepting as well as for overriding an exception, and periodically re-test a sample of items the model cleared.</li>'
     '<li><strong>Alert fatigue.</strong> A poorly tuned detector produces thousands of exceptions, and the team learns to ignore them. Tune for precision first, then widen recall, and measure the exception-to-finding conversion rate as a first-class metric.</li>'
     '<li><strong>Opaque logic.</strong> A model that cannot explain why an item was flagged cannot support a finding. Prefer rules and transparent models over black-box scoring wherever a conclusion depends on the output, and keep the logic documented and versioned.</li>'
     '<li><strong>Data access over-reach.</strong> Audit needs broad access, which makes it a high-value target and a governance risk in its own right. Scope audit\'s AI access to the same entitlement framework as human auditors, log every query, and review the logs.</li>'
     '<li><strong>Dependence on a vendor.</strong> If the model is a black box owned by a third party, the function cannot fully explain its own conclusions. Retain ownership of the rules, the data definitions, and the evidence trail even where the tooling is bought.</li>'
     '</ul>'
     '<p>These are the same risks audit would raise in any function that deployed AI, which is precisely the point: the function is expected to hold itself to the standard it applies to others, and doing so is what makes its AI adoption credible rather than merely modern.</p>'),

    ('How Should an Audit Function Sequence AI Adoption?',
     'how-should-an-audit-function-sequence-ai-adoption',
     '<p>A twelve-month sequence that most functions can execute without adding headcount has four quarters, each with a deliverable the audit committee can see.</p>'
     '<ol>'
     '<li><strong>Quarter one — foundation.</strong> Establish governed read access to the two or three systems that carry the highest-risk transactions, document the control rules currently tested manually, and baseline exception volume and manual test hours. Deliverable: a data access model approved by IT security.</li>'
     '<li><strong>Quarter two — evidence and risk assessment.</strong> Automate evidence retrieval for one audit cycle and run AI-supported risk ranking for the annual plan. Deliverable: a plan built on full-population risk signals, with the prior year\'s plan as the comparison.</li>'
     '<li><strong>Quarter three — full-population testing.</strong> Convert one high-volume control test from sampling to full population, run both in parallel, and compare. Deliverable: measured coverage improvement and the exception-to-finding conversion rate.</li>'
     '<li><strong>Quarter four — continuous monitoring pilot.</strong> Move one stable control to scheduled testing with a defined alert response path. Deliverable: detection time measured in days rather than quarters.</li>'
     '</ol>'
     '<p>Throughout, keep the function\'s ownership explicit: the audit team defines the rules, owns the evidence, and draws the conclusions. Where tooling is bought, buy the infrastructure and keep the logic — because the moment a third party owns the reasoning, the function has outsourced the judgement that gives its work meaning.</p>'),
]

EN_FAQ = [
    ('How is AI changing internal audit?',
     'The defining change is the move from sampling to coverage. Traditional audit tests a sample because testing every transaction is impractical for humans; AI reads every journal entry, approval, and payment against the control rules and surfaces only the exceptions that warrant a human look. That inversion — from finding a few problems in a sample to finding all deviations and prioritising them — is what changes the nature of the work. AI adoption in internal audit is projected to roughly double, reaching around 80 percent of functions by 2026, and the functions that benefit most are those that keep ownership of the rules and the evidence.'),
    ('Does AI replace the judgement of internal auditors?',
     'No, and it should not. AI handles volume: testing entire populations, detecting anomalies, assembling evidence, and ranking risk. Auditors handle judgement: whether an exception is a control failure or a legitimate business exception, how to frame a finding, and what to recommend. The risk runs the other way — automation bias, where auditors defer to a model output because it looks rigorous. The structural countermeasure is to require a documented reason for accepting an exception as well as for dismissing one, and to re-test a sample of items the model cleared.'),
    ('What evidence is needed for an AI-assisted audit to hold up?',
     'Four things. Reproducibility: the same inputs and model version produce the same result months later, which requires versioned data and model artefacts. Traceability: every exception is traceable to the specific records and rule that flagged it. Honest coverage: if two systems could not be reached, the 94 percent coverage belongs in the workpaper rather than a claim of full-population testing. And recorded human judgement: where an auditor accepted or overrode a model output, the reasoning is in the file.'),
    ('Which audit applications should be adopted first?',
     'Start with risk assessment and evidence assembly. Risk ranking uses AI to inform where auditors spend time rather than to conclude anything, which makes it high value and low risk; evidence retrieval demonstrates benefit without touching audit conclusions. Then move to full-population testing on one high-volume control, running it in parallel with the existing sample test. Continuous monitoring is a second-year objective, because it requires stable data feeds and a defined response path for every alert — functions that start there stall.'),
    ('How should internal audit govern its own use of AI?',
     'To the standard it applies to everyone else. Scope the AI\'s data access within the same entitlement framework a human auditor would use, log every query, and review the logs. Prefer transparent rules over black-box scoring wherever a conclusion depends on the output. Tune detectors for precision first, because alert fatigue destroys the value of monitoring faster than poor recall does. And retain ownership of the rules, data definitions, and evidence trail even when the tooling is purchased, since a function that cannot explain its own reasoning has outsourced its judgement.'),
]

ZH_RENAMES = {
    '核心收益与投资回报考量': 'AI为内部审计带来的回报是什么？',
    '实施路线图与后续步骤': '内部审计的AI采用路线图应该如何设计？',
    '案例分析与行业洞察': '有哪些值得借鉴的实践案例？',
    '未来展望与行动建议': '下一步审计部门应该做什么？',
    '关键成功因素与常见陷阱': '成功的关键因素与常见陷阱是什么？',
    '蜂启咨询的专业洞察': '蜂启咨询如何看待AI驱动的内部审计？',
}

ZH_FAQ = [
    ('AI正在如何改变内部审计？',
     '最具决定性的变化是从抽样走向全量覆盖。传统审计之所以抽样，是因为让人工团队测试每一笔交易并不现实；而AI可以按控制规则读取每一笔分录、每一次审批与每一笔付款，只把值得人工关注的例外呈现出来。这一反转——从"在样本中发现几个问题"变为"找出所有偏差并排序"——改变了工作的性质。业内研究预计内部审计的AI采用率将翻倍，到2026年达到约80%；而受益最大的部门，是那些坚持掌握规则与证据所有权的部门。'),
    ('AI会取代内部审计师的判断吗？',
     '不会，也不应该。AI处理的是体量：测试全量、识别异常、整理证据、风险排序。审计师处理的是判断：某个例外究竟是控制失效还是合理的业务例外、发现应该如何表述、以及应该提出什么建议。真正的风险在相反方向——自动化偏误，即审计师因为模型输出"看起来很严谨"而直接采信。结构性的对策是：接受一个例外与驳回一个例外，都要求写下理由；并定期抽取模型判定为通过的项目进行复测。'),
    ('AI辅助审计需要哪些证据才能站得住？',
     '四件事。可复现性：相同的输入与模型版本在数月后能得出相同结果，这需要版本化的数据与模型产物。可追溯性：每一个例外都能追溯到具体的记录与触发它的规则。诚实的覆盖率：如果有两个系统无法接入，那么94%的覆盖率就应该写进工作底稿，而不是宣称做了全量测试。以及被记录的人工判断：审计师在何处采纳或推翻了模型输出，理由都应归档。'),
    ('应该优先采用哪些审计应用？',
     '建议从风险评估与证据整理入手。风险排序是用AI告诉审计师"把时间花在哪里"，而不是替审计师下结论，因此价值高、风险低；证据检索则能在不触及审计结论的前提下展示收益。随后再把一个高频控制测试从抽样转为全量，并与既有抽样测试并行对比。持续监控属于第二年目标，因为它需要稳定的数据供给和每条预警的明确响应路径——一开始就做这件事的部门往往会停滞。'),
    ('内部审计应该如何治理自身的AI使用？',
     '用它要求别人的同一套标准来要求自己。把AI的数据访问限制在人类审计师同等权限框架内，记录并复核每一次查询；凡是结论依赖模型输出的场景，优先使用透明规则而非黑箱打分；先调优精确率，因为预警疲劳比召回不足更快地摧毁监控价值。即便工具是采购的，也要保留规则、数据定义与证据链的所有权——一个无法解释自身推理过程的部门，本质上已经把判断外包了出去。'),
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
