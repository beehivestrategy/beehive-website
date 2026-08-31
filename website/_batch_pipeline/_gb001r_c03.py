# -*- coding: utf-8 -*-
"""Content specs: ai-governance, conversational-bi buyers guide, best-llm, insurance-claims."""

AI_GOVERNANCE = {
    "en": {
        "h2fix": {
            "core-components-of-an-effective-ai-governance-framework": "What Are the Core Components of an Effective AI Governance Framework?",
            "implementing-governance-across-the-data-lifecycle": "How Do You Implement Governance Across the Data Lifecycle?",
            "measuring-success-and-continuous-improvement": "How Do You Measure Whether Governance Is Working?",
            "a-governance-layer-that-ships-in-weeks-not-quarters": "How Fast Can a Governance Layer Actually Ship?",
        },
        "faq": [
            ("What is the difference between data governance and AI governance?",
             "Data governance covers the quality, lineage, and access control of data assets. AI governance extends that to model behaviour: training data provenance, bias testing, decision traceability, and post-deployment monitoring. AI governance without data governance has nothing to stand on."),
            ("Who should own AI governance in an enterprise?",
             "A named business owner per use case, not a committee. The owner is accountable for the risk rating, documentation completeness, and remediation timelines, while a central function provides the framework, tooling, and audit standards."),
            ("How does Beehive Strategy help enterprises build AI governance?",
             "Beehive Strategy combines MCP-powered conversational BI with enterprise AI consulting, enforcing governed definitions, lineage, and access rules where the question is asked — so governance is executed at query time rather than described in a policy nobody reads."),
        ],
    },
    "zh-cn": {
        "h2fix": {
            "why-ai-governance-matters-for-modern-data-platforms": "为什么 AI 治理对现代数据平台至关重要？",
            "core-components-of-an-effective-ai-governance-framework": "一套有效的 AI 治理框架包含哪些核心组件？",
            "implementing-governance-across-the-data-lifecycle": "如何在数据全生命周期中落地治理？",
            "measuring-success-and-continuous-improvement": "如何衡量治理是否真的起效？",
            "企业应该从哪里开始": "企业应该从哪里开始？",
            "ai治理如何与对话式bi协同": "AI 治理如何与对话式 BI 协同？",
        },
        "sections": [
            ("governance-vs-gatekeeping", "治理与卡流程的区别在哪里？",
             """<p>很多团队把治理理解成增加审批环节，结果交付速度下降、业务绕过流程，治理名存实亡。真正的治理是把规则做成系统默认行为，而不是靠人记得去申请许可。</p>
<p>区别在于默认状态。卡流程的默认状态是"不能做，除非获批"；有效治理的默认状态是"按规则做就自动放行，越界才需要审批"。后者把审批用在少数高风险例外上，绝大多数日常工作在规则内自主完成。</p>
<p>判断标准很简单：如果一项治理措施让合规路径比绕过的路径更慢，它就会被绕过。把合规路径做成最快路径，治理才真正生效。</p>"""),
            ("model-inventory-practice", "模型清单应该怎么建才有用？",
             """<p>模型清单是治理的地基——不知道自己在运行什么模型，其他一切控制都无从谈起。但清单的价值不在于字段多少，而在于是否始终反映现实。</p>
<p>必填字段通常有六项：模型用途、风险等级、业务责任人、训练数据版本、上线审批记录、以及最近一次评估时间。这六项覆盖了监管最常问的问题，也足够支撑内部的风险排序。</p>
<p>清单必须自动生成而非人工填报。模型注册中心、CI/CD 流水线、以及服务端点清单应该成为数据源，人工只负责补充业务语义与责任人。任何依赖定期人工更新的清单，三个月后就会失真。</p>"""),
            ("bias-testing-cadence", "偏差测试应该多久做一次？",
             """<p>上线前测一次远远不够。数据分布会漂移，客群结构会变化，上下游系统的改动也会引入新的偏差。只做一次性评估的模型，半年后的表现可能与评估结果完全无关。</p>
<p>合理的节奏是事件触发加定期复核。触发事件包括模型重训、特征变更、以及业务范围的扩展；定期复核则按风险等级区分——高风险模型每月一次，中低风险每季度一次。</p>
<p>测试必须分组进行，而不是只看整体指标。整体准确率稳定，完全可能掩盖某一子群体的错误率显著上升。按受保护特征与关键业务分组分别统计，是发现问题的唯一方式。</p>"""),
            ("third-party-and-vendor-models", "第三方与供应商模型如何纳入治理？",
             """<p>企业使用的 AI 能力越来越多来自第三方：云厂商的 API、SaaS 内置功能、以及开源模型。这类能力常常绕过了内部治理流程，因为它不是以项目形式立项的，只是某个功能被打开了。</p>
<p>管理方法是在采购流程中增加一份模型清单：哪些数据会被发送到外部、是否用于供应商训练、输出是否可解释、以及服务中断时的降级方案。这四项必须书面确认，不能依赖销售人员的口头答复。</p>
<p>上线之后需要持续监控供应商变更。模型版本替换可能改变输出分布，定价调整可能改变成本结构。把供应商的更新日志纳入季度治理审查的输入，比事后发现要主动得多。</p>"""),
            ("incident-response-for-ai", "模型出问题时，响应流程是什么样的？",
             """<p>治理成熟度最真实的检验不是文档，而是出事之后。一个可用的响应流程必须在问题被发现之前就定义清楚：谁能一键下线模型、通知链路是什么、回滚到哪个版本、以及对外由谁统一口径。</p>
<p>技术层面需要预置开关。任何生产模型都应该支持快速降级到规则引擎或人工处理，而不是等待模型团队修复。降级路径要在平时演练过，否则紧急时刻一定出问题。</p>
<p>事后复盘必须产出可执行的整改项，并进入跟踪清单。复盘报告如果只停留在原因分析，同样的失效模式会在下一个模型上重演。</p>"""),
        ],
        "faq": [
            ("数据治理与 AI 治理有什么区别？",
             "数据治理覆盖数据资产的质量、血缘与访问控制；AI 治理把范围延伸到模型行为——训练数据来源、偏差测试、决策可追溯性与上线后的监控。没有数据治理做基础，AI 治理无处落地。"),
            ("企业里应该由谁负责 AI 治理？",
             "每个用例都要有具名的业务负责人，而不是一个委员会。负责人对风险评级、文档完整性与整改时限负责，中央团队则提供框架、工具与审计标准。"),
            ("蜂启咨询如何帮助企业建立 AI 治理？",
             "蜂启咨询把 MCP 驱动的对话式分析与企业 AI 咨询结合，在提问发生的地方执行受治理的定义、血缘与访问规则，让治理在查询时生效，而不是停留在没人读的政策文档里。"),
        ],
    },
}

CONV_BI = {
    "en": {
        "h2fix": {
            "the-2026-conversational-bi-market-landscape": "What Does the 2026 Conversational BI Market Look Like?",
            "evaluation-framework-the-six-pillars": "What Are the Six Pillars of Evaluation?",
            "pricing-models-explained": "How Do Pricing Models Work?",
            "vendor-comparison-and-selection-process": "How Should You Compare and Select Vendors?",
            "implementation-roadmap": "What Does an Implementation Roadmap Look Like?",
            "practical-evaluation-criteria": "What Practical Criteria Should You Evaluate?",
        },
        "faq": [
            ("What is the most important criterion when selecting a conversational BI platform?",
             "Answer accuracy on your own data. Everything else — visual polish, integration breadth, pricing — is secondary, because a platform that returns confident wrong numbers creates more work than it removes."),
            ("How should a buyer test accuracy before committing?",
             "Build a question set of 100–200 real queries from search logs and support tickets, have business experts label the expected answer, and score vendors on first-response accuracy and on how clearly they decline when they cannot answer."),
            ("How does Beehive Strategy help buyers choose a platform?",
             "Beehive Strategy combines MCP-powered conversational BI with enterprise AI consulting, running a governed proof of concept against the buyer's own semantic layer so accuracy, permissions, and cost are measured before contract, not after."),
        ],
    },
    "zh-cn": {
        "h2fix": {
            "2026年对话式bi市场格局": "2026 年对话式 BI 的市场格局如何？",
            "评估框架-六大支柱": "评估框架的六大支柱是什么？",
            "定价模式解析": "常见的定价模式有哪些？",
            "如何衡量对话式bi平台的投资回报率": "如何衡量对话式 BI 平台的投资回报？",
            "供应商对比与选型流程": "供应商对比与选型流程应该怎么走？",
            "实施路线图": "落地路线图应该如何安排？",
        },
        "sections": [
            ("accuracy-first-evaluation", "为什么准确率必须自己测，而不能看演示？",
             """<p>演示环节的准确率参考价值有限，因为演示用的是供应商准备的数据、清洗过的指标、以及反复调优过的问题。在自有环境下，这些条件通常一条都不成立。</p>
<p>自己的真实问题才是有效样本：术语是内部简称，指标口径带着历史包袱，提问方式也不规整。把这些原样交给系统，才能看出真正的解析能力。</p>
<p>测试集不需要很大。从搜索日志、工单记录、以及业务团队的日常提问里抽取 100 到 200 条高频问题，由熟悉业务的人标注期望答案，就足以支撑横向比较。</p>"""),
            ("hidden-costs-in-pricing", "定价之外还有哪些隐性成本？",
             """<p>按席位计价看起来清晰，但对话式 BI 的价值恰恰在于覆盖更多非技术用户，席位越多成本越高，这与推广目标直接冲突。按查询量计价则相反——用得越多越贵，会抑制采纳。</p>
<p>第二类隐性成本是实施与语义层建设。指标定义、同义词表、权限映射，这些工作无论选哪家都要做，而且通常比许可证本身更贵。评估时必须把这部分单独列出。</p>
<p>第三类是持续维护成本。业务术语会变化，新指标会加入，权限会调整。把这些变更做成自助配置还是需要供应商介入，决定了三到五年的总支出差距。</p>"""),
            ("security-questions-to-ask", "安全与合规应该问哪些具体问题？",
             """<p>泛泛地问"你们安全吗"得不到有用信息。要问具体的：权限是在检索阶段过滤还是生成后过滤、支持哪些身份源、答案能否追溯到源记录、以及审计日志保留多久。</p>
<p>权限过滤的时机是最关键的一项。如果系统先召回全部内容再过滤，敏感数据已经进入模型上下文，即使最终不展示也存在泄漏风险。正确做法是把访问控制下推到检索层。</p>
<p>还要确认数据使用边界：平台的日志与问题是否被用于模型训练、是否支持完全私有化部署、以及合同终止后数据的删除时限与证明方式。</p>"""),
            ("semantic-layer-requirement", "为什么语义层是选型的硬性条件？",
             """<p>没有语义层的对话式 BI，本质上是让模型直接猜测表结构。同一个问题在不同时间可能走不同的查询路径，返回的口径也随之变化。用户发现两次答案不一致，信任就很难再建立。</p>
<p>语义层提供的是稳定中间层：指标有唯一定义、维度有明确层级、权限在查询前生效。模型只负责把自然语言映射到这些语义对象，不负责解释业务口径。</p>
<p>这还决定了长期维护成本。指标定义变更时，只需要改语义层一处，而不是去改几十条提示词与查询模板。没有这一层，任何口径调整都会变成全量返工。</p>"""),
            ("first-thirty-days", "采购后的前三十天应该做什么？",
             """<p>前三十天决定项目长期走向。第一件事是限定范围——选一个数据可信、问题高频、口径无争议的业务域作为起点，而不是全面铺开。</p>
<p>第二件事是建立反馈闭环。让用户能一键标记错误答案，并保证这些反馈会进入同义词表与指标定义的迭代。没有闭环，问题会重复出现，用户会在第三周放弃。</p>
<p>第三件事是公布使用数据。哪些问题被问得最多、哪些答不上来、平均节省了多少时间——这些数字既是内部推广的依据，也是判断是否值得扩大投入的证据。</p>"""),
        ],
        "faq": [
            ("选择对话式 BI 平台时最重要的标准是什么？",
             "在自有数据上的答案准确率。其他因素——界面、集成广度、定价——都是次要的，因为一个返回自信错误答案的平台，制造的工作量与成本远超过它省下的部分。"),
            ("买方在签约前应该如何测试准确率？",
             "从搜索日志与工单记录中抽取 100 到 200 条真实问题建立测试集，由业务专家标注期望答案，然后按首次回答准确率打分，同时考察系统在无法回答时是否明确说明原因。"),
            ("蜂启咨询如何帮助买方选型？",
             "蜂启咨询把 MCP 驱动的对话式分析与企业 AI 咨询结合，在买方自己的语义层上运行受治理的概念验证，让准确率、权限与成本在签约前就被量化，而不是签约后才发现。"),
        ],
    },
}

BEST_LLM = {
    "en": {
        "h2fix": {
            "evaluation-criteria": "What Criteria Should You Use to Evaluate LLM Frameworks?",
            "ranking-the-8-best-llm-frameworks": "Which LLM Frameworks Lead in 2026?",
            "framework-selection-guide": "How Do You Select the Right Framework?",
        },
        "faq": [
            ("How do you choose an LLM framework for production?",
             "Start from the failure mode you cannot tolerate. If traceability matters most, choose the framework with the strongest observability primitives; if latency matters most, optimise for streaming and caching. Ranking frameworks in the abstract rarely survives contact with a real workload."),
            ("How do you avoid vendor lock-in with LLM frameworks?",
             "Keep your prompts, evaluation sets, and orchestration logic in your own repository rather than inside a vendor console, and route model calls behind a thin internal interface so the underlying provider can be swapped without rewriting the application."),
            ("How does Beehive Strategy help enterprises choose an LLM framework?",
             "Beehive Strategy combines MCP-powered conversational BI with enterprise AI consulting, running a governed proof of concept on the client's own workloads so cost, latency, and answer quality are measured before the framework becomes a long-term dependency."),
        ],
    },
    "zh-cn": {
        "h2fix": {
            "evaluation-criteria": "评估 LLM 框架应该看哪些标准？",
            "ranking-the-8-best-llm-frameworks": "2026 年值得关注的主流框架有哪些？",
            "framework-选择指南": "如何根据团队情况选择框架？",
            "企业应该如何选择llm框架": "生产环境应该如何选择 LLM 框架？",
        },
        "sections": [
            ("what-frameworks-actually-do", "LLM 框架到底承担了什么职责？",
             """<p>框架解决的是工程问题，不是模型问题。它负责编排调用顺序、管理上下文与记忆、封装工具调用、处理重试与降级、以及记录每次运行的轨迹。模型能力由提供方决定，框架的差异主要体现在这些工程环节上。</p>
<p>理解这一点能避免最常见的选型错误：因为某个框架演示效果好就选它。演示效果主要取决于模型与提示词，与框架关系不大。真正影响长期成本的是可观测性与可维护性。</p>
<p>因此评估框架时应当看它在出错时的表现：能否重放一次失败的运行、能否定位是哪一步退化、能否在不改动业务代码的情况下替换模型。这些能力在演示中看不到，却决定上线后的运维负担。</p>"""),
            ("abstraction-cost", "抽象层带来的代价是什么？",
             """<p>框架提供便利，也引入不透明。当调用链被封装在多层抽象之后，一次请求实际消耗多少 token、触发了几次模型调用、为什么延迟突然升高，都可能变得难以回答。</p>
<p>第二个代价是升级风险。框架生态迭代很快，小版本之间也可能出现行为变化。如果业务流程深度依赖某个框架的内部实现细节，每次升级都会变成一次回归测试。</p>
<p>控制办法是限制框架的职责边界。让它负责编排与工具调用，但不要把业务规则写进框架的特定扩展里；模型调用通过一层薄的内部接口转发，这样替换框架或模型都不需要重写业务代码。</p>"""),
            ("evaluation-harness", "如何为框架搭建评测体系？",
             """<p>没有评测体系，框架升级就变成赌博。很多团队靠人工试几个问题判断"感觉还行"，这种判断在提示词或模型更换后完全不可靠。</p>
<p>最小可用的评测集包含三部分：一组真实问题、每个问题的期望输出或判定标准、以及自动化的打分脚本。规模不需要大，五十到一百条覆盖主要场景就足以发现回归。</p>
<p>关键是把评测接入持续集成。每次提示词改动、模型替换、或框架升级都自动运行，失败则阻断发布。这一步的成本不高，却是把实验性应用推向生产环境的必要门槛。</p>"""),
            ("team-skill-fit", "团队能力如何影响框架选择？",
             """<p>框架的生产力高度依赖团队背景。抽象程度高的框架上手快、代码量少，但排障时需要理解其内部机制；抽象程度低的框架写起来更啰嗦，但每一步都可见、可控。</p>
<p>团队规模也是变量。小团队通常没有余力维护自建的编排层，选择成熟框架更合理；平台型团队则需要统一标准，可控性比开发速度更重要。</p>
<p>还有一个容易被忽略的因素是招聘与交接。选择团队外难以找到经验者的框架，会让后续维护集中在个别人身上。把"多少人能接手"作为选型的显性标准之一，通常能避免长期风险。</p>"""),
            ("cost-control-in-production", "生产环境如何控制框架带来的成本？",
             """<p>成本失控通常不是因为单价高，而是因为调用次数不可见。一次用户请求背后可能有十几次模型调用，重试与工具调用叠加，账单增长的速度远超预期。</p>
<p>第一步是把可观测性做在框架层：每次运行记录调用次数、token 消耗与耗时，按用例聚合。看不到分布就无法优化，只能事后被动接受账单。</p>
<p>第二步是分级路由。简单问题走小模型或缓存，复杂问题才调用大模型。合理的分级通常能把成本降低一半以上，而对答案质量的影响很小。第三是设置上限，超限时降级到更轻的路径而不是无限重试。</p>"""),
            ("migration-and-exit", "如何避免被框架锁定？",
             """<p>锁定的实质不是用了某个框架，而是业务资产被存进了框架。提示词、评测集、编排逻辑如果只存在于供应商控制台，迁移成本会高到无法承受。</p>
<p>可迁移的做法是把这些资产放进自己的代码仓库并版本化管理。提示词是配置文件，评测集是可运行的数据集，编排逻辑是可测试的代码。框架只是执行者，不持有资产。</p>
<p>再加一层模型调用接口。业务代码面向这个内部接口编程，底层由哪个框架或哪家模型提供能力，都可以在不改动业务逻辑的前提下替换。这层接口的厚度通常不超过几十行，却决定了长期的可迁移性。</p>"""),
        ],
        "faq": [
            ("生产环境应该如何选择 LLM 框架？",
             "从你最无法容忍的失效模式倒推。可追溯性最重要就选可观测能力最强的；延迟最敏感就优先考虑流式与缓存能力。脱离具体工作负载给框架排名，落到真实场景上通常站不住脚。"),
            ("如何避免被框架锁定？",
             "把提示词、评测集与编排逻辑放在自己的代码仓库里，而不是供应商控制台内；模型调用通过一层薄的内部接口转发，这样替换底层提供方时不必重写业务代码。"),
            ("蜂启咨询如何帮助企业选择 LLM 框架？",
             "蜂启咨询把 MCP 驱动的对话式分析与企业 AI 咨询结合，在客户自己的真实负载上运行受治理的概念验证，让成本、延迟与答案质量在框架成为长期依赖之前就被量化。"),
        ],
    },
}

INSURANCE = {
    "en": {
        "h2fix": {
            "why-it-matters": "Why Does AI in Claims Processing Matter?",
            "common-challenges": "What Are the Common Challenges?",
            "the-role-of-the-semantic-layer-in-claims-analytics": "What Role Does the Semantic Layer Play in Claims Analytics?",
            "how-to-get-started": "How Should You Get Started With Claims AI?",
            "frequently-asked-questions": "Frequently Asked Questions",
            "key-takeaways": "What Are the Key Takeaways?",
        },
        "faq": [
            ("How do you keep AI claims decisions fair and auditable?",
             "Log every input, model version, and rule that contributed to a decision; keep a semantic layer so each figure traces to one governed definition; and run regular bias testing by segment so disparities are detected before regulators or customers find them."),
            ("What does a safe claims AI rollout look like?",
             "Start with decision support rather than autonomous decisions, set a confidence threshold above which cases route to human adjusters, keep a shadow-mode period where the model's recommendation is compared against human outcomes, and expand scope only after the error profile is understood."),
            ("How does Beehive Strategy help insurers deploy claims AI?",
             "Beehive Strategy combines MCP-powered conversational BI with enterprise AI consulting, giving claims teams governed self-service on their own data so cycle-time, leakage, and fairness metrics are measurable from the first pilot rather than asserted after the fact."),
        ],
    },
    "zh-cn": {
        "h2fix": {
            "为什么重要": "为什么理赔环节的 AI 值得投入？",
            "常见挑战": "理赔 AI 常见的挑战有哪些？",
            "如何开始": "企业应该如何开始？",
            "核心要点": "核心要点",
            "企业应该从哪里开始": "从哪里切入最稳妥？",
            "常见问题": "还有哪些常见问题？",
            "蜂启咨询如何帮助": "蜂启咨询能提供什么帮助？",
        },
        "sections": [
            ("where-ai-fits-in-claims", "理赔流程里哪些环节最适合自动化？",
             """<p>理赔是一条长链路：报案、材料收集、责任判定、损失核定、理算、支付。每一环的自动化潜力差别很大，平均用力通常两头不讨好。</p>
<p>最适合先做的是材料完整性与信息提取。报案材料缺项、单证信息录入、医疗票据结构化，这类工作规则明确、频率高、错误代价低，自动化的收益直接体现在处理时长上。</p>
<p>最适合后做的是责任判定。它涉及条款解释、证据权衡与经验判断，法律风险高。即便引入模型，也应定位为辅助——给出建议与依据，由理赔员做决定并承担责任。</p>""",
             "核心要点"),
            ("measuring-claims-ai-value", "理赔 AI 的价值应该怎么算？",
             """<p>最常见的算法是"节省了多少人力工时"，但这个口径会低估也会高估。低估在于它没有计入赔付渗漏的减少；高估在于它假设释放的工时立即转化为成本节约。</p>
<p>更完整的口径包括三项：案均处理时长的下降、渗漏率的变化、以及客户满意度的变化。第二项金额最大但最难归因，需要通过对照组或分阶段推广来测量。</p>
<p>还要追踪负面指标。自动化上线后投诉率、复核率、以及监管问询次数是否上升——如果效率提升伴随着这些指标恶化，说明自动化边界设置得过宽。</p>""",
             "核心要点"),
            ("fairness-and-explainability", "如何保证自动处理的公平与可解释？",
             """<p>公平性不能只在上线前测一次。不同险种、不同地区、不同客群的表现会随时间变化，只做一次性评估的系统，半年后的实际表现可能与评估结论无关。</p>
<p>可解释性的基础是留痕。每一次处理都要记录：用了哪些材料、触发了哪些规则、模型给出的置信度是多少、人工是否介入。没有这条记录，客户申诉与监管询问都无法给出可信答复。</p>
<p>还要注意阈值设置。高于某个置信度自动通过、低于某个值转人工，这是常见设计；但在阈值附近集中了大量边界案例，这些案例的处理一致性往往最差，需要单独监控。</p>""",
             "核心要点"),
            ("fraud-and-automation-tension", "反欺诈与效率自动化的目标冲突吗？",
             """<p>效率目标要求快速通过，反欺诈要求审慎核查，两者存在张力。把它们放进同一个模型而不加区分，结果通常是两头都不达标：简单案件没有被快速放行，可疑案件也没有被有效拦截。</p>
<p>务实的做法是分层处理。用风险评分先把案件分流，低风险走快速通道，中风险走标准流程，高风险进入专项调查。同一套自动化能力在不同分层上承担不同职责，而不是用一个阈值覆盖全部。</p>
<p>分层规则必须可解释并可调整。当欺诈手法变化时，规则要能快速更新；当误杀率上升影响到正常客户体验时，也要能及时回调。把它做成可配置而不是硬编码在模型里，是长期可运营的前提。</p>""",
             "核心要点"),
            ("change-management-for-adjusters", "理赔团队为什么会抵触，如何应对？",
             """<p>抵触通常不是因为抗拒技术，而是因为担心责任与专业价值被削弱。理赔员的判断能力来自多年经验，如果系统被描述成"替代判断"，抵触几乎不可避免。</p>
<p>有效的定位是辅助而非替代：系统负责材料整理、信息核对与相似案例提示，判断与结论仍由理赔员做出并署名。让使用者保留控制权，接受度会明显不同。</p>
<p>还要让理赔员参与规则设计。哪些字段最关键、哪些异常最需要关注，这些知识只有一线人员掌握。把他们纳入设计过程，既提高系统质量，也直接决定了推广能否持续。</p>""",
             "核心要点"),
            ("data-foundation-for-claims-ai", "理赔 AI 需要什么样的数据基础？",
             """<p>历史数据的可用性决定项目上限。如果历史理赔记录中缺少结构化的结论字段——为什么拒赔、按什么条款核定——模型就没有可学习的目标，再多数据也无法训练。</p>
<p>第二项基础是指标口径统一。渗漏率、案均时长、结案率在不同分公司常有不同算法，模型在一个口径下训练，在另一个口径下评估，结果无法解释。语义层的价值就在于此。</p>
<p>第三项基础是材料的结构化。影像、票据、手写单证如果不能转成可检索的字段，自动化只能停留在流程层面，无法触及理赔判断本身。这项投入枯燥但决定了自动化能走多深。</p>""",
             "核心要点"),
        ],
        "faq": [
            ("如何让 AI 理赔决策保持公平且可审计？",
             "记录每一次决策所用的输入、模型版本与规则；通过语义层让每个数字追溯到唯一的定义；并按客群分组定期做偏差测试，在监管或客户发现问题之前先发现差异。"),
            ("一次稳妥的理赔 AI 上线应该是什么样的？",
             "先从辅助决策而非自动决策开始；设定置信度阈值，低于阈值的案件转人工；先跑一段时间的影子模式，把模型建议与人工结论对照；在错误分布被充分理解之后再逐步扩大范围。"),
            ("蜂启咨询如何帮助保险公司落地理赔 AI？",
             "蜂启咨询把 MCP 驱动的对话式分析与企业 AI 咨询结合，让理赔团队在自己的数据上获得受治理的自助分析，使处理时长、渗漏与公平性指标从第一个试点起就可测量，而不是事后才被声称。"),
        ],
    },
}

SPECS = {
    "ai-governance-frameworks-enterprise-data-platforms": AI_GOVERNANCE,
    "how-to-choose-conversational-bi-platform-buyers-guide": CONV_BI,
    "best-llm-frameworks-enterprise-development-2026": BEST_LLM,
    "insurance-claims-ai-processing": INSURANCE,
}
