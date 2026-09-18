# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patch
from opencc import OpenCC

ROOT = '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website'
SLUG = 'preparing-data-team-ai-augmented-era'

EN_TOC = [
    ('what-does-an-ai-augmented-data-team-actually-look-like', 'What Does an AI-Augmented Data Team Actually Look Like?'),
    ('why-do-traditional-data-team-structures-struggle-in-the-ai-era', 'Why Do Traditional Data Team Structures Struggle in the AI Era?'),
    ('which-roles-and-skills-should-you-add-first', 'Which Roles and Skills Should You Add First?'),
    ('how-should-work-be-reorganised-between-humans-and-ai-agents', 'How Should Work Be Reorganised Between Humans and AI Agents?'),
    ('how-do-you-upskill-an-existing-team-without-stalling-delivery', 'How Do You Upskill an Existing Team Without Stalling Delivery?'),
    ('what-does-a-90-day-transition-plan-look-like', 'What Does a 90-Day Transition Plan Look Like?'),
]

EN_PROSE = """
<p class="article-lead"><strong>The data team that won the last decade was optimised for building pipelines and answering tickets. The team that wins the next one is optimised for curating trusted data products and supervising the systems that answer questions on their behalf.</strong> That shift is not a rebranding exercise and it is not, for most organisations, a headcount reduction. It is a change in what the team is accountable for: less time assembling data, more time deciding what the data means and whether the machine got it right. This article sets out what an AI-augmented data team actually looks like, why the traditional structure strains under AI-era demand, which capabilities to add first, and how to make the transition without putting delivery at risk.</p>
<h2 id="what-does-an-ai-augmented-data-team-actually-look-like">What Does an AI-Augmented Data Team Actually Look Like?</h2>
<p>An AI-augmented data team is one where a meaningful share of routine analytical and engineering work is performed by systems the team designs, supervises, and improves. The defining characteristic is not the tooling — most teams already have access to capable models — but the operating model. Work is delegated to agents with explicit contracts; outputs are verified against governed definitions; and the team's scarce human attention is spent on the parts that genuinely require judgement: semantics, ambiguity, exceptions, and trust.</p>
<p>In practice the shape of the team changes in three ways. First, the centre of gravity moves from pipeline construction to data product ownership. Someone must own the definition of a metric, its freshness, its lineage, and its access policy — and that someone is now accountable to both human consumers and machine consumers. Second, a verification function appears. When a system produces two hundred analyses a day, someone has to design the tests, the golden sets, and the sampling regime that decide whether those analyses are fit to ship. Third, the team acquires an enablement mandate: teaching the business to ask better questions of a system that answers instantly.</p>
<p>Consider what this looks like concretely. A retail analyst who previously spent three days assembling a promotional performance review now supervises a system that assembles it in seconds, and spends her time on the two things the system cannot do: deciding whether the promotional calendar definition still matches how the business actually runs promotions, and interpreting why a specific region diverged. Her output goes up by an order of magnitude, but her value moves entirely to judgement and semantics. Multiply that across a team and you get the real productivity story of enterprise AI — not headcount reduction, but the removal of the queue.</p>
<p>That last point matters politically. Teams that frame AI augmentation as efficiency-target-driven headcount reduction reliably destroy the cooperation they need. The analysts who know where the bodies are buried are exactly the people you need to define the semantics the system will be judged against.Frame the shift as removing the queue, not removing the person, and the same people who might have resisted become the authors of the new operating model.</p>
<h2 id="why-do-traditional-data-team-structures-struggle-in-the-ai-era">Why Do Traditional Data Team Structures Struggle in the AI Era?</h2>
<p>The traditional structure — a central data engineering team, a BI team, and a queue — was a rational response to scarcity. Engineering capacity was limited, so requests were triaged, prioritised, and delivered in sprints. Governance was achieved by making the central team the bottleneck: nothing shipped without passing through people who knew the definitions. This worked when demand was moderate and the cost of waiting was low.</p>
<p>Three pressures break it. The first is demand elasticity. When business users can ask a question in natural language and get an answer in seconds, they ask fifty questions instead of filing one ticket. Demand does not grow linearly with AI adoption; it grows by an order of magnitude, and a queue-based model simply cannot absorb that. The second is latency expectation. A two-week turnaround that was acceptable for a dashboard request is not acceptable when the competing experience is instantaneous. The third is that the bottleneck moves: the constraint stops being "can we build the pipeline" and becomes "do we agree on what this number means."</p>
<p>There is a subtler failure too. Centralised teams accumulate definitional knowledge tacitly — in people's heads, in Slack threads, in the memory of who built which model. AI systems cannot use tacit knowledge. They need explicit, machine-readable semantics: which table is authoritative, what "net revenue" excludes, how a customer is counted when they hold accounts in two regions. Making that knowledge explicit is a different kind of work from building pipelines, and teams organised around pipeline delivery consistently under-invest in it until an AI pilot exposes the gap.</p>
<table class="article-table"><thead><tr><th>Dimension</th><th>Traditional data team</th><th>AI-augmented data team</th><th>Why the change matters</th></tr></thead><tbody><tr><td>Primary output</td><td>Pipelines, dashboards, ad-hoc extracts</td><td>Governed data products and verified answers</td><td>Machines consume products, not dashboards</td></tr><tr><td>Demand handling</td><td>Triage, prioritise, sprint queue</td><td>Self-serve with guardrails and monitoring</td><td>AI makes demand elastic; queues cannot scale</td></tr><tr><td>Where knowledge lives</td><td>Tacit, in senior engineers' heads</td><td>Explicit, in catalogues and contracts</td><td>Models can only read explicit semantics</td></tr><tr><td>Quality control</td><td>Review before release</td><td>Continuous verification and sampling</td><td>Volume makes pre-release review impossible</td></tr><tr><td>Success metric</td><td>Tickets closed, sprints delivered</td><td>Answer accuracy, reuse, time-to-trusted-answer</td><td>Outcomes beat throughput once AI answers directly</td></tr></tbody></table>
<h2 id="which-roles-and-skills-should-you-add-first">Which Roles and Skills Should You Add First?</h2>
<p>Most organisations assume the answer is more machine learning engineers. In our experience the first three capabilities that pay off are considerably less glamorous, and two of them are usually sitting inside the team already.</p>
<ol>
<li><strong>Data product owner.</strong> A named individual accountable for a defined set of data products: their semantics, freshness SLAs, access policy, and consumers. This is the single highest-leverage role in an AI-augmented team, because it converts tacit knowledge into an explicit contract that both humans and machines can rely on.</li>
<li><strong>Analytics engineer with semantic-modelling depth.</strong> Someone who can express business logic as versioned, testable models rather than as SQL buried in a dashboard. In the AI era the semantic layer is the interface, and this is the person who builds it.</li>
<li><strong>Evaluation and quality lead.</strong> The person who owns the golden question set, the regression suite, the sampling regime, and the incident process for wrong answers. Without this role, teams ship fast and discover errors through users.</li>
<li><strong>AI enablement partner.</strong> A hybrid profile who sits with business teams, translates questions into well-formed requests, and feeds recurring ambiguity back to the product owners. This role is what turns adoption from a launch event into a habit.</li>
<li><strong>Platform engineer for the self-serve path.</strong> Someone accountable for the experience a non-engineer has when they try to get an answer unaided — measured in minutes, not in tickets.</li>
</ol>
<p>Notice that only one of those five is a modelling specialist. The skills that multiply AI value are definitional, evaluative, and enablement-oriented. When we run readiness assessments, the most common gap is not modelling capability — it is that nobody owns the definitions and nobody owns the evaluation. Both gaps are fillable by retraining existing staff, which is faster and cheaper than hiring into a market where AI talent commands a significant premium.</p>
<p>It is also worth being honest about the hiring-versus-upskilling economics, because the instinct to buy capability externally is usually wrong on the timeline. A specialist hired into an organisation with no governed data products spends their first two quarters discovering that the constraint is definitional rather than modelling, which is precisely the period during which an internal candidate with domain context would already have shipped something. The pragmatic split we recommend: hire one evaluation or semantic-modelling lead to set standards and transfer method, and backfill the remaining capacity by retraining people who already know where the definitions are contested. External hiring then becomes a way to accelerate a capability you have already proven you need, rather than an expensive experiment in whether you do.</p>
<h2 id="how-should-work-be-reorganised-between-humans-and-ai-agents">How Should Work Be Reorganised Between Humans and AI Agents?</h2>
<p>The cleanest way to think about the split is by consequence and by ambiguity. Work that is high-volume, well-specified, and low-consequence should be delegated to agents with verification. Work that is ambiguous, definitional, or high-consequence should remain human-led with AI assistance. Everything else sits on a spectrum, and the art is in placing the boundary deliberately rather than by accident.</p>
<p>Concretely, agents are well suited to: generating first-draft SQL against an established semantic model; monitoring data quality rules and raising incidents; documenting lineage and describing datasets for the catalogue; drafting the narrative summary of a known analysis; and answering recurring business questions within a defined answerable set. Humans remain accountable for: defining and changing metrics; resolving conflicting definitions across domains; approving high-impact automated actions; investigating anomalies the system flags; and deciding what the team should stop measuring.</p>
<p>Three mechanisms make delegation safe. The first is an explicit answerable set — a documented list of question types the system may answer, and an explicit refusal policy for everything else. The second is mandatory citation, so every answer names the governed source it came from and unverified claims never ship. The third is a verification step proportionate to consequence: a cheap deterministic reconciliation check for routine answers, and human confirmation for anything that commits the business externally.</p>
<p>This is the layer where a conversational analytics platform changes the team's daily reality. When business users ask questions in WeCom, DingTalk, Feishu, Teams, or WhatsApp and receive sourced answers drawn from governed data products, the data team stops being a queue and starts being a curator. At Beehive Strategy we deploy this as a managed service in roughly two weeks, connecting to the warehouse you already run, so the team's first experience of AI augmentation is that the interruptions stop — not that their roles are under review.</p>
<h2 id="how-do-you-upskill-an-existing-team-without-stalling-delivery">How Do You Upskill an Existing Team Without Stalling Delivery?</h2>
<p>The failure mode to avoid is the bootcamp: a two-week training programme pulled away from delivery, after which participants return to unchanged workflows and forget most of it. Upskilling works when it is attached to a real migration the team is accountable for. Pick one domain, commit to publishing its data products and grounding an AI interface on them, and let the learning happen inside that work.</p>
<ul>
<li><strong>Teach evaluation first.</strong> Before anyone touches a model, teach the team to build a golden question set and a regression suite. Evaluation is the skill that makes everything else safe.</li>
<li><strong>Pair, do not lecture.</strong> Embed one person with evaluation or semantic-modelling depth alongside two domain specialists for a full quarter, then rotate.</li>
<li><strong>Rewrite, do not retrain from scratch.</strong> Ask each engineer to convert one existing dashboard into a governed data product with a contract. The artefact is the lesson.</li>
<li><strong>Protect delivery capacity explicitly.</strong> Ring-fence a fixed share of each sprint for the transition. Programmes that treat upskilling as spare-time work stall within two months.</li>
<li><strong>Measure and publish.</strong> Track time-to-trusted-answer, reuse per data product, and defect escape rate. Visible movement keeps the investment funded.</li>
</ul>
<p>There is also a career-path question that determines whether your best people stay. If the new operating model is perceived as a lateral move — from building to documenting — you will lose the engineers you most need. Define the progression explicitly: data product ownership and evaluation leadership should be senior, visible, and compensated as such, because they now carry more business risk than pipeline construction ever did.</p>
<h2 id="what-does-a-90-day-transition-plan-look-like">What Does a 90-Day Transition Plan Look Like?</h2>
<p>A ninety-day plan is long enough to produce evidence and short enough to survive a budget cycle. In the first thirty days, run a capability audit across the five roles above, choose one pilot domain with real business pain, and build the golden question set for that domain before any AI interface goes live. Order matters here: the evaluation asset should exist before the thing it evaluates.</p>
<p>In days thirty-one to sixty, publish two or three governed data products with named owners and contracts, stand up the semantic layer that expresses their logic, and connect the conversational interface. Run the golden set weekly and publish the results to stakeholders, including the failures. Teams that share their error rates early build more trust than teams that announce perfect accuracy later.</p>
<p>In days sixty-one to ninety, hand the domain's routine questions to the self-serve path, redeploy the freed capacity into the next domain, and formalise the new accountabilities in job descriptions and performance objectives. Then repeat. The transition is not a project with an end date; it is a new operating rhythm in which the team curates, verifies, and enables rather than assembles and dispatches.</p>
<p>Expect three objections, and prepare for them in advance. Finance will ask why the team is not shrinking if AI is doing the work; the answer is that demand is elastic and the queue, not the headcount, was the problem. Business stakeholders will ask why the system refuses some questions; the answer is that refusal is the feature that makes the answers it does give worth acting on. And your best engineers will ask whether documentation work is a career dead end; the answer has to be a written progression path, not a reassurance. Teams that answer these three well keep their mandate; teams that answer them badly lose it in the second budget cycle regardless of their technical results.</p>
<p>One closing caution. Do not attempt this as a reorganisation first and a capability build second. Teams that redraw the org chart before they have a working pilot spend a quarter debating reporting lines and emerge with the same queue under new names. Build one working domain, let the evidence reorganise the conversation for you, and the structure will follow the work rather than the other way around.</p>
"""

EN_FAQ = [
    ("Will AI replace data analysts and data engineers?",
     "In most enterprises, no — it changes what they do. AI absorbs the routine assembly, drafting, and monitoring work that currently fills the queue, while demand for judgement work rises: defining metrics, resolving ambiguity between domains, designing evaluation, and interpreting anomalies. The realistic risk is not replacement but stagnation: teams that keep a queue-based model while demand grows tenfold will be overwhelmed, not automated."),
    ("Which role should we hire first for an AI-augmented data team?",
     "A data product owner. This is the role accountable for the semantics, freshness SLAs, access policy and consumers of a defined set of data products, and it converts tacit knowledge into an explicit contract that both humans and machines can rely on. Close behind are an analytics engineer with semantic-modelling depth and an evaluation lead who owns the golden question set and regression suite."),
    ("How do we measure whether the transition is working?",
     "Track four indicators from a pre-transition baseline: time from business question to trusted answer, reuse count per data product, the share of routine questions answered without a ticket, and the defect escape rate on AI-generated answers. Review them monthly and publish them to stakeholders. Visible movement in these numbers is what keeps the programme funded beyond the pilot."),
    ("How do we keep AI answers accurate as the team delegates more work?",
     "Delegate with three mechanisms attached: an explicit answerable set that defines what the system may answer and must refuse, mandatory citation so every claim names its governed source, and verification proportionate to consequence — deterministic reconciliation for routine answers, human confirmation for anything that commits the business externally."),
    ("Should we reorganise the team before or after the first AI pilot?",
     "After. Teams that redraw the org chart first spend a quarter debating reporting lines and emerge with the same queue under new names. Build one working domain end to end — data products, semantic layer, conversational interface, evaluation suite — and let the evidence reorganise the conversation. Structure should follow the work, not precede it."),
]

ZH_TOC = [
    ('AI增强的数据团队究竟是什么样', 'AI 增强的数据团队究竟是什么样？'),
    ('为什么传统数据团队结构在AI时代会吃力', '为什么传统数据团队结构在 AI 时代会吃力？'),
    ('应该优先补充哪些角色与技能', '应该优先补充哪些角色与技能？'),
    ('人与AI智能体之间应如何重新分工', '人与 AI 智能体之间应如何重新分工？'),
    ('如何在不停滞交付的前提下提升团队能力', '如何在不停滞交付的前提下提升团队能力？'),
    ('90天转型计划长什么样', '90 天转型计划长什么样？'),
]

ZH_PROSE = """
<p class="article-lead"><strong>赢得过去十年的数据团队，是为"建管道、接工单"而优化的；赢得下一个十年的团队，则是为"经营可信的数据产品、并监督那些代替他们回答问题的系统"而优化的。</strong>对大多数组织来说，这个转变既不是换个名字，也不是削减编制。它改变的是团队的问责对象：花在拼装数据上的时间更少，花在判断"数据意味着什么"以及"机器答对了没有"上的时间更多。本文讲清楚 AI 增强的数据团队究竟长什么样、为什么传统结构在 AI 时代会吃力、应该优先补哪些能力，以及如何在不危及交付的前提下完成转型。</p>
<h2 id="AI增强的数据团队究竟是什么样">AI 增强的数据团队究竟是什么样？</h2>
<p>AI 增强的数据团队，指的是团队所设计、监督并持续改进的系统，承担了相当大一部分常规分析与工程工作。其决定性特征不是工具——多数团队早已能用到足够强的模型——而是运营模式：工作被连同明确契约一起委派给智能体；输出对照受治理的定义被校验；而团队稀缺的人类注意力，被投入到真正需要判断力的部分——语义、歧义、例外与信任。</p>
<p>实践中，团队的形态会发生三处变化。第一，重心从管道建设转向数据产品 ownership。必须有人对一个指标的定义、新鲜度、血缘与访问策略负责——而且这个人现在同时要对人类消费者和机器消费者负责。第二，出现了验证职能。当一个系统每天产出两百份分析时，必须有人设计测试、黄金集与抽样机制，来判断这些分析是否可以放行。第三，团队获得了赋能职责：教会业务方，向一个秒回的系统提出更好的问题。</p>
<p>具体是什么样？一位零售分析师过去要花三天拼出一份促销效果复盘，现在她监督一个几秒钟就能拼完的系统，把时间花在系统做不了的两件事上：判断"促销日历"的定义是否还匹配业务实际跑促销的方式，以及解释某个区域为什么跑偏了。她的产出提升了一个数量级，而她的价值几乎全部转移到了判断与语义上。把这个放大到整个团队，就是企业 AI 真实的生产力故事——不是减人，而是消灭排队。</p>
<p>最后这一点在政治上很关键。把 AI 增强包装成"以效率为目标的裁员"的团队，几乎必然摧毁自己所需要的配合。那些知道"坑埋在哪儿"的分析师，恰恰是你定义系统评判标准所依赖的人。把这次转变说成"消灭排队"而不是"消灭人"，原本可能抵触的同一批人，就会成为新运营模式的作者。</p>
<h2 id="为什么传统数据团队结构在AI时代会吃力">为什么传统数据团队结构在 AI 时代会吃力？</h2>
<p>传统结构——一个中心化的数据工程团队、一个 BI 团队，加一条工单队列——是对稀缺性的理性回应。工程产能有限，所以需求要被分诊、排序、按迭代交付；治理则通过让中心团队成为瓶颈来实现：任何东西不经过懂定义的人就不能上线。在需求温和、等待成本低廉的年代，这套做法运转良好。</p>
<p>有三重压力把它压垮。第一是需求弹性。当业务用户能用自然语言提问并在几秒内拿到答案时，他们会问五十个问题，而不是提一张工单。需求并不随 AI 采用线性增长，而是增长一个数量级；基于队列的模型根本吸收不了。第二是时延预期。对一张看板需求来说可接受的两周交付，在竞争对手的体验是"即时"时就不再可接受。第三是瓶颈发生了转移：约束不再是"我们能不能建这条管道"，而变成"我们对这个数字的口径是否达成一致"。</p>
<p>还有一种更隐蔽的失败：中心化团队把定义知识以隐性方式积累下来——存在于人的脑子里、聊天记录里、以及"谁建的哪个模型"的记忆里。AI 系统无法使用隐性知识。它们需要显式的、机器可读的语义：哪张表是权威的，"净收入"排除了什么，一位在两个区域都有账户的客户如何计数。把这些知识显式化，是一类与建管道截然不同的工作；而围绕管道交付组织起来的团队，往往会一直低估它，直到某个 AI 试点把缺口暴露出来。</p>
<table class="article-table"><thead><tr><th>维度</th><th>传统数据团队</th><th>AI 增强的数据团队</th><th>为何这种变化重要</th></tr></thead><tbody><tr><td>主要产出</td><td>管道、看板、临时提数</td><td>受治理的数据产品与经过验证的答案</td><td>机器消费的是产品，不是看板</td></tr><tr><td>需求处理</td><td>分诊、排序、迭代队列</td><td>带护栏与监控的自助服务</td><td>AI 让需求变得有弹性，队列无法扩展</td></tr><tr><td>知识存放位置</td><td>隐性，在资深工程师脑中</td><td>显式，在目录与契约中</td><td>模型只能读取显式语义</td></tr><tr><td>质量控制</td><td>发布前评审</td><td>持续验证与抽样</td><td>量级使发布前评审不再可能</td></tr><tr><td>成功指标</td><td>关闭工单数、交付迭代数</td><td>答案准确率、复用率、取信耗时</td><td>当 AI 直接作答，结果优于吞吐量</td></tr></tbody></table>
<h2 id="应该优先补充哪些角色与技能">应该优先补充哪些角色与技能？</h2>
<p>大多数组织默认答案是"多招机器学习工程师"。而在我们的经验里，最先产生回报的三项能力远没有那么光鲜，而且其中两项通常已经在团队里了。</p>
<ol>
<li><strong>数据产品负责人。</strong>对一组明确的数据产品负责的具名个人：其语义、新鲜度 SLA、访问策略与消费者。这是 AI 增强团队中杠杆最高的角色，因为它把隐性知识转化成了人类与机器都能依赖的显式契约。</li>
<li><strong>具备语义建模深度的分析工程师。</strong>能把业务逻辑表达为版本化、可测试的模型，而不是埋在看板里的 SQL。在 AI 时代，语义层就是接口，而这个人负责构建它。</li>
<li><strong>评估与质量负责人。</strong>拥有黄金问题集、回归套件、抽样机制，以及"答错了怎么办"的事故流程的人。没有这个角色，团队会发得很快，然后靠用户来发现错误。</li>
<li><strong>AI 赋能伙伴。</strong>一种混合型角色，坐进业务团队，把模糊问题翻译成表述良好的请求，并把反复出现的歧义反馈给产品负责人。这个角色决定了采用是一次上线活动，还是一种习惯。</li>
<li><strong>自助路径的平台工程师。</strong>对"非工程师独立取数时的体验"负责的人——以分钟衡量，而不是以工单衡量。</li>
</ol>
<p>请注意，这五项里只有一项是建模专家。能够放大 AI 价值的能力，是定义性、评估性与赋能性的。我们做就绪度评估时，最常见的缺口不是建模能力，而是"没有人拥有定义"以及"没有人拥有评估"。这两个缺口都可以通过再培训现有员工来填补，而这比在一个 AI 人才溢价显著的市场上招聘更快、更便宜。</p>
<h2 id="人与AI智能体之间应如何重新分工">人与 AI 智能体之间应如何重新分工？</h2>
<p>思考这条分界线最清晰的方式，是按"后果"和"歧义"两个维度切。高产量、界定清晰、低后果的工作，应当带着验证机制委派给智能体；含混、涉及定义或高后果的工作，应当在 AI 辅助下由人类主导。其余的落在中间光谱上，而诀窍在于有意识地划定边界，而不是让它偶然形成。</p>
<p>具体来说，智能体适合承担：针对已建立的语义模型生成 SQL 初稿；监控数据质量规则并触发事故；为目录编写血缘与数据集描述；为一项已知分析起草叙述性摘要；以及在既定可回答集合内回答重复出现的业务问题。人类仍需负责：定义与变更指标；解决跨域的定义冲突；批准高影响的自动化动作；调查系统标记出的异常；以及决定团队应该停止衡量什么。</p>
<p>有三种机制能让委派变得安全。其一是明确的可回答集合——一份文档化的清单，界定系统可以回答哪些类型的问题，并对其他一切给出明确的拒答策略。其二是强制引用，让每个答案都指明它所来自的受治理来源，未经证实的陈述绝不放行。其三是与后果相称的验证步骤：常规答案跑一次廉价的确定性对账，任何对外承诺的事项都要求人工确认。</p>
<p>正是对话式分析平台改变团队日常现实的这一层。当业务用户在企业微信、钉钉、飞书、Teams 或 WhatsApp 中提问，并从受治理的数据产品中拿到带来源的答案时，数据团队就不再是队列，而开始成为策展者。蜂启咨询以托管服务方式部署这一模式，约两周上线，对接你已经在跑的仓库——因此团队对 AI 增强的第一体验是"打扰终于停了"，而不是"岗位要被重新评估了"。</p>
<h2 id="如何在不停滞交付的前提下提升团队能力">如何在不停滞交付的前提下提升团队能力？</h2>
<p>要避免的失败模式是"集训营"：把人从交付里拉出来培训两周，然后他们回到毫无变化的工作流，并把大部分内容忘掉。能力提升只有挂在一项团队要负责的真实迁移上时才会奏效。选一个领域，承诺发布它的数据产品并把 AI 接口建立在上面，让学习发生在这件工作内部。</p>
<ul>
<li><strong>先教评估。</strong>在任何人碰模型之前，先教会团队搭建黄金问题集与回归套件。评估是让其他一切变得安全的那项技能。</li>
<li><strong>结对，而不是讲课。</strong>把一名具备评估或语义建模深度的人，与两名领域专家一起嵌进去整整一个季度，然后轮换。</li>
<li><strong>重写，而不是从零培训。</strong>让每位工程师把一张现有看板改造成带契约的受治理数据产品。产物本身就是课程。</li>
<li><strong>明确保护交付产能。</strong>为每个迭代固定划出一部分容量给转型。把能力提升当作"业余时间做的事"的项目，两个月内就会停滞。</li>
<li><strong>度量并公开。</strong>跟踪取信耗时、每个数据产品的复用次数、以及缺陷逃逸率。看得见的移动才能让这笔投资持续拿到预算。</li>
</ul>
<p>还有一个决定你能否留住最好的人的问题：职业发展路径。如果新运营模式被视为一次平调——从"建设"变成"写文档"——你会失去最需要的那批工程师。要把晋升路径明确定义出来：数据产品 ownership 与评估负责人，应当是高级别、高可见度并获得相应薪酬的岗位，因为它们现在承担的业务风险，超过了管道建设曾经承担过的任何风险。</p>
<h2 id="90天转型计划长什么样">90 天转型计划长什么样？</h2>
<p>九十天足够长到能拿出证据，又足够短到能撑过一个预算周期。前三十天：围绕上述五个角色做一次能力审计，选一个有真实业务痛点的试点领域，并在任何 AI 接口上线之前，先为该领域建好黄金问题集。这里的顺序很关键——评估资产应当先于它所评估的对象存在。</p>
<p>第三十一天到第六十天：发布两到三个带具名负责人与契约的受治理数据产品，搭建表达其逻辑的语义层，并接上对话式界面。每周跑一次黄金集，并把结果——包括失败——发给干系人。早早公开自己错误率的团队，比那些晚些时候宣称"百分之百准确"的团队，能建立更多信任。</p>
<p>第六十一天到第九十天：把该领域的常规问题交给自助路径，把释放出来的产能投向下一个领域，并把新的问责写入岗位说明书与绩效目标。然后重复。这次转型不是一个有截止日期的项目，而是一种新的运营节奏——在这个节奏里，团队做的是策展、验证与赋能，而不是拼装与派单。</p>
<p>最后一条提醒：不要"先重组、后建能力"。那些在还没有跑通试点之前就重画组织架构图的团队，会花一个季度争论汇报线，最后带着新名字下的同一条队列走出来。先做出一个能跑的领域，让证据替你重组这场对话，结构自然会随着工作而来，而不是反过来。</p>
"""

ZH_FAQ = [
    ("AI 会取代数据分析师和数据工程师吗？",
     "在大多数企业中不会——它改变的是他们做什么。AI 吸收了当前填满工单队列的常规拼装、起草与监控工作，而对判断力工作的需求反而上升：定义指标、解决跨域歧义、设计评估、解释异常。真正的风险不是被取代，而是停滞：一边维持队列模式、一边面对十倍增长的需求的团队，会被淹没，而不是被自动化。"),
    ("AI 增强的数据团队应该先招哪个角色？",
     "先招数据产品负责人。这个角色对一组明确的数据产品的语义、新鲜度 SLA、访问策略与消费者负责，并把隐性知识转化为人类与机器都能依赖的显式契约。紧随其后的是具备语义建模深度的分析工程师，以及拥有黄金问题集与回归套件的评估负责人。"),
    ("我们如何判断这次转型是否有效？",
     "从转型前的基线出发跟踪四项指标：从业务提问到可信答案的耗时、每个数据产品的复用次数、无需工单即可回答的常规问题占比、以及 AI 生成答案的缺陷逃逸率。按月复盘并向干系人公开。这些数字上可见的移动，正是让项目在试点之后继续拿到预算的原因。"),
    ("随着团队委派更多工作，如何保证 AI 答案依然准确？",
     "委派时必须附带三种机制：明确的可回答集合，界定系统可答什么、必须拒绝什么；强制引用，让每条陈述都指明其受治理来源；以及与后果相称的验证——常规答案做确定性对账，任何对外承诺的事项都要求人工确认。"),
    ("应该在第一个 AI 试点之前还是之后重组团队？",
     "之后。先重画组织架构图的团队，会花一个季度争论汇报线，最后带着新名字下的同一条队列走出来。先把一个领域端到端跑通——数据产品、语义层、对话式界面、评估套件——再让证据重组这场对话。结构应当跟随工作，而不是先行于工作。"),
]

cc = OpenCC('s2twp')
to_tw = cc.convert
TW_TOC = [(i, to_tw(t)) for i, t in ZH_TOC]

def main():
    patch.apply(os.path.join(ROOT, 'blog/articles/%s.html' % SLUG), EN_TOC, EN_PROSE, EN_FAQ, cta='Book a Demo')
    patch.apply(os.path.join(ROOT, 'zh-cn/blog/articles/%s.html' % SLUG), ZH_TOC, ZH_PROSE, ZH_FAQ, cta='预约演示')
    patch.apply(os.path.join(ROOT, 'zh-tw/blog/articles/%s.html' % SLUG), TW_TOC, to_tw(ZH_PROSE),
                [(to_tw(q), to_tw(a)) for q, a in ZH_FAQ], cta='預約示範')

if __name__ == '__main__':
    main()
