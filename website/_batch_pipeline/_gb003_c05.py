#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gbatch_003 slug 05 — ai-data-governance-evolution-2025-recap"""
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb003_lib import process, stats, tw_renames
from _gb001_s2t import s2tw

SLUG = 'ai-data-governance-evolution-2025-recap'

EN_RENAMES = {
    'The Regulatory Acceleration of 2025':
        'What Changed in AI Regulation During 2025?',
    'From Policy Documents to Runtime Governance':
        'Why Did Governance Move From Policy Documents to Runtime Enforcement?',
    'Key Benefits and ROI Considerations':
        'What Is the Return on Modern AI Data Governance?',
    'Implementation Roadmap and Next Steps':
        'What Should the 2026 Governance Roadmap Look Like?',
}

EN_INSERTS = [
    ('What Does AI Data Governance Maturity Look Like in Practice?',
     'what-does-ai-data-governance-maturity-look-like-in-practice',
     '<p>Through 2025, most enterprises moved along a recognisable maturity curve, and knowing where you sit determines what to fix next. Three stages describe the majority of organisations.</p>'
     '<ul>'
     '<li><strong>Ad-hoc.</strong> Governance is bolted onto AI pilots after they are built. Controls live in application code, there is no inventory of which data a model can reach, and audit is reconstructed from logs after an incident. The tell-tale sign: nobody can answer "which datasets did the assistant read last week?" without an engineering investigation.</li>'
     '<li><strong>Centralised.</strong> A single program covers all AI use cases. Data access is enforced at a governed layer, retrieval sources are catalogued, and every AI-to-data interaction is logged. The organisation can produce an audit trail on demand and can onboard a new use case in days rather than months, because the controls already exist.</li>'
     '<li><strong>Federated.</strong> Standards are set centrally but enforced in the domains that know the data best. Domain teams own classification, retention, and access decisions within a central policy framework, and the central function audits rather than approves. This is where governance stops being a bottleneck, and it is where the leaders were heading at the end of 2025.</li>'
     '</ul>'
     '<p>A five-question assessment places an organisation quickly: what share of data assets has a named owner? Can access policy be changed in one place and take effect everywhere? Is every AI-to-data interaction logged and searchable? Can the organisation prove what data a given answer was based on, months later? And how long does it take to approve a new AI use case? The answers are more useful than any maturity score, because each one maps to a specific control gap.</p>'),

    ('Which Controls Matter Most When AI Touches Regulated Data?',
     'which-controls-matter-most-when-ai-touches-regulated-data',
     '<p>Five controls carried most of the risk reduction in 2025, and each has a specific enforcement point. Getting the enforcement point wrong is the most common reason a control fails an audit.</p>'
     '<ol>'
     '<li><strong>Access control at the data layer.</strong> Applied where the data lives, not in application code. If the rule lives in the app, every new AI interface is a new way around it.</li>'
     '<li><strong>Retrieval filtering.</strong> Restricted content must be filtered before it enters model context, at the vector index or search layer. Filtering after retrieval has already leaked: result counts and snippet text are themselves information.</li>'
     '<li><strong>Output filtering.</strong> Models must be prevented from reproducing regulated data, personal information, or proprietary content in their answers, including through paraphrase.</li>'
     '<li><strong>Purpose limitation and retention.</strong> Data use must be tied to declared purposes, with retention windows enforced on training data, fine-tuning sets, and retrieval sources — not only on the source system.</li>'
     '<li><strong>Audit trails.</strong> Every AI-to-data interaction recorded, queryable by user, dataset, and time, retained long enough for regulatory review and incident forensics.</li>'
     '</ol>'
     '<p>The Model Context Protocol became the practical enforcement surface for most of these controls during 2025. By standardising how AI systems reach enterprise data, MCP allows authentication, authorisation, masking, and logging to be applied at one governed layer instead of re-implemented inside every application. That is the difference between a control that holds as the estate grows and one that silently decays with every new integration.</p>'),

    ('What Went Wrong in 2025, and What Should Enterprises Change?',
     'what-went-wrong-in-2025-and-what-should-enterprises-change',
     '<p>The recaps that matter are the failures, because they repeat. Five patterns accounted for most of the governance incidents and stalled AI programs observed through 2025.</p>'
     '<ul>'
     '<li><strong>Governance arrived after the pilot.</strong> Teams built a compelling assistant on a broad data extract, then discovered that production access required controls the prototype never had. Fix: stand up the governed access layer before the first pilot, not after it.</li>'
     '<li><strong>Retrieval sources were never inventoried.</strong> Organisations catalogued tables but not the documents, wikis, tickets, and chat histories that RAG systems actually read — the ungoverned long tail. Fix: inventory what the model can retrieve, not only what the warehouse stores.</li>'
     '<li><strong>Shadow AI spread faster than policy.</strong> Business teams connected assistants to SaaS data with personal credentials, outside every control. Fix: offer a governed path that is faster than the ungoverned one, because prohibition alone does not win.</li>'
     '<li><strong>Lineage stopped at the model boundary.</strong> Teams could trace a table but not which model version consumed it, or which answer was produced from it. Fix: extend lineage to model inputs and outputs, so an answer can be reconstructed months later.</li>'
     '<li><strong>The catalogue was mistaken for governance.</strong> Documenting data is not controlling it. A catalogue without enforcement at query time is documentation. Fix: measure enforcement coverage, not catalogue completeness.</li>'
     '</ul>'
     '<p>Enterprises that internalised these lessons entered 2026 with a compounding advantage: each new AI use case inherits controls that already exist, so the marginal cost of governing the next deployment approaches zero while the marginal cost for competitors stays where it was.</p>'),
]

EN_FAQ = [
    ('What is AI data governance, and how is it different from traditional data governance?',
     'AI data governance controls what AI systems may access, what they may do with it, and what they are allowed to emit — enforced continuously at the point of use. Traditional data governance focused on cataloguing data, documenting lineage, and defining stewardship, largely for human consumers. The difference is enforcement timing: a policy document governs a person who has read it, but an AI system consumes whatever it is given, so controls must execute at query time. In practice, AI data governance means access control at the data layer, retrieval and output filtering, purpose limitation with retention on training and retrieval sources, and complete audit trails of every AI-to-data interaction.'),
    ('Which 2025 regulatory developments mattered most for enterprise AI?',
     'The EU AI Act was the dominant one: entering into force in August 2024, it began staged application through 2025, placing obligations on general-purpose AI models and governance requirements on organisations deploying AI in the EU market. Alongside it, sectoral rules in financial services, health, and consumer protection created a patchwork that most multinationals had to reconcile before national AI laws matured. The practical consequence was that mapping obligations to existing controls — data inventory, retention, purpose limitation, transparency, human oversight — became a year-one requirement rather than a later refinement.'),
    ('How do you enforce governance at runtime instead of on paper?',
     'Move the control to the layer where data is accessed and apply it uniformly. Concretely: enforce authentication and authorisation at the data layer rather than in application code; filter restricted content out of the retrieval index before it can enter model context; filter model outputs before they reach the user; bind data use to declared purposes with retention windows; and log every AI-to-data interaction for review. Standardising AI access to enterprise data through a protocol such as MCP makes this tractable, because the controls are implemented once at a governed layer rather than re-implemented in every application.'),
    ('Which metrics should an AI governance program track?',
     'Track coverage and response, not document counts. Useful measures include the share of data assets with a named owner, policy enforcement coverage across AI use cases, completeness of audit trails, mean time to detect and respond to an AI data incident, approval cycle time for a new use case, and the number of shadow AI integrations discovered and remediated. Baseline them before the program matures and review quarterly — the trend line is what boards and regulators ultimately judge, and a policy document cannot substitute for it.'),
    ('How long does it take to implement AI data governance?',
     'A focused program covering critical data assets typically takes eight to twelve weeks: two to three weeks to inventory and classify what AI touches, three to five weeks to implement enforcement at a governed layer with retrieval and output filtering, and the remainder to stand up monitoring, audit, and the quarterly metrics cycle. Organisations that already have mature data governance move considerably faster because they are extending an existing framework to model inputs and retrieval sources. A managed deployment of the governed access layer and audit trail can be stood up in about two weeks, with coverage then expanded from critical assets outward.'),
]

ZH_RENAMES = {
    '核心收益与投资回报考量': '现代企业AI数据治理的回报体现在哪里？',
    '实施路线图与后续步骤': '2026年数据治理路线图应该包含哪些步骤？',
    '案例分析与行业洞察': '2025年有哪些值得借鉴的治理实践？',
    '未来展望与行动建议': '2026年AI数据治理将走向何方？',
    '关键成功因素与常见陷阱': '数据治理项目成功的关键因素与常见陷阱是什么？',
    '蜂启咨询的专业洞察': '蜂启咨询如何看待AI数据治理的演进？',
}

ZH_FAQ = [
    ('什么是AI数据治理，它与传统数据治理有什么不同？',
     'AI数据治理管控的是AI系统可以访问什么、可以对这些数据做什么、以及允许它输出什么，并且在使用发生的那一刻持续执行。传统数据治理主要面向人类使用者，关注的是数据编目、血缘记录与责任归属。两者的根本差别在于执行时机：政策文件能约束读过它的人，但AI系统只会消费它被给予的数据，因此控制必须在查询时执行。落到实践上，AI数据治理包含：数据层的访问控制、检索前过滤与输出过滤、绑定声明用途并落实留存期限、以及对每一次AI与数据的交互留痕。'),
    ('2025年哪些监管变化对企业AI影响最大？',
     '最主要的是欧盟《AI法案》：它于2024年8月生效，并在2025年分阶段适用，对通用AI模型提出义务，并对在欧盟市场部署AI的组织提出治理要求。与此同时，金融服务、医疗与消费者保护等领域的行业规则，共同构成了一整套在各国AI立法成熟之前就必须应对的拼图式要求。实际后果是：把义务映射到既有控制措施（数据清单、留存、目的限制、透明度、人工监督）变成了第一年的必修课，而不是后续的优化项。'),
    ('如何把治理从事后文档变成运行时执行？',
     '把控制点前移到数据被访问的位置，并统一执行。具体做法包括：在数据层而非应用代码中执行认证与授权；在检索索引阶段就把受限内容挡在模型上下文之外；在模型输出到达用户之前进行过滤；把数据使用绑定到声明用途并设置留存窗口；记录每一次AI与数据的交互以供审计。通过MCP之类的协议标准化AI访问企业数据的方式，可以让这些控制只在一个受治理的层实现一次，而不必在每个应用里重复实现——这是控制能否随规模扩张而保持有效的关键。'),
    ('AI治理项目应该跟踪哪些指标？',
     '应该跟踪覆盖率与响应能力，而不是文档数量。有效的指标包括：有明确责任人的数据资产占比、策略在AI用例中的执行覆盖率、审计留痕的完整性、AI数据事件的平均发现与响应时间、新用例的审批周期，以及被发现并处置的影子AI集成数量。在项目成熟之前先建立基线，之后按季度复盘——董事会与监管者最终看的是趋势线，任何政策文件都无法替代它。'),
    ('落地AI数据治理需要多长时间？',
     '一个覆盖关键数据资产的聚焦型项目通常需要八到十二周：两到三周盘点并分类AI所触及的数据，三到五周在受治理的层实现访问控制与检索、输出过滤，其余时间用于建立监控、审计与季度指标机制。已经有成熟数据治理体系的企业会快得多，因为它们只需要把既有框架延伸到模型输入与检索来源。若采用托管方式部署受治理的数据访问层与审计留痕，大约两周即可上线，之后再从关键资产向外逐步扩展覆盖范围。'),
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
