# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patch
from opencc import OpenCC

ROOT = '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website'
SLUG = 'building-an-ai-ready-workforce-training-vs-hiring'

EN_TOC = [
    ('what-does-an-ai-ready-workforce-actually-mean', 'What Does an AI-Ready Workforce Actually Mean?'),
    ('which-skills-does-each-group-in-the-organisation-need', 'Which Skills Does Each Group in the Organisation Need?'),
    ('is-it-faster-to-train-or-to-hire-for-ai-readiness', 'Is It Faster to Train or to Hire for AI Readiness?'),
    ('how-do-you-design-training-that-actually-changes-behaviour', 'How Do You Design Training That Actually Changes Behaviour?'),
    ('how-do-you-measure-workforce-ai-readiness', 'How Do You Measure Workforce AI Readiness?'),
    ('what-does-a-12-month-workforce-plan-look-like', 'What Does a 12-Month Workforce Plan Look Like?'),
]

EN_PROSE = """
<p class="article-lead"><strong>"AI-ready workforce" has become a phrase that means everything and therefore nothing: a one-day prompt workshop, a data science degree, and a company-wide licence to a chatbot have all been sold under the same label.</strong> The useful definition is behavioural rather than curricular. A workforce is AI-ready when the people doing the work can recognise which of their tasks are delegable, can supervise a system doing those tasks, know when to distrust an output, and change how they work as a result. That is a much narrower target than most programmes aim at, and a much harder one than a training video can hit. This article defines readiness in testable terms, splits the skill requirement by audience, compares the training and hiring paths honestly, and sets out a twelve-month plan that changes behaviour rather than attendance records.</p>
<h2 id="what-does-an-ai-ready-workforce-actually-mean">What Does an AI-Ready Workforce Actually Mean?</h2>
<p>Readiness is not familiarity with tools, and it is not the ability to write a clever prompt. Both are perishable: the tools change every quarter and prompt craft is rapidly being absorbed into the interfaces themselves. What persists is a set of four behaviours that can be observed and assessed.</p>
<ol>
<li><strong>Task decomposition.</strong> The person can break their own work into components and identify which components are specified, repetitive, and low-consequence — the delegable ones — and which require judgement, context, or accountability.</li>
<li><strong>Supervision.</strong> The person can review a machine output critically: check the source, spot a plausible but unsupported claim, and detect when an answer addresses a different question than the one asked.</li>
<li><strong>Calibrated trust.</strong> The person knows when to rely on the system and when to escalate, based on consequence rather than on how confident the output sounds.</li>
<li><strong>Workflow redesign.</strong> The person changes how the work is done once delegation is available, rather than using AI to do the same process marginally faster.</li>
</ol>
<p>That fourth behaviour is where most programmes fail, and it is worth dwelling on. Organisations routinely measure AI adoption by licence usage or prompt volume, then wonder why productivity has not moved. Usage is not adoption. If an analyst uses a chatbot to draft an email faster but still assembles the monthly review by hand because that is how the process works, capability has arrived and readiness has not. Readiness shows up in redesigned process: the review assembles itself, the human reviews exceptions, and the monthly cycle shortens from five days to one.</p>
<p>There is also a structural component that individuals cannot supply on their own. A workforce cannot be ready if the data it needs is ungoverned, if there is no sanctioned tool, or if the organisation has not decided what may and may not be delegated. Readiness is a property of the system — people plus data plus permissions plus process — not a property of the people alone. Programmes that train thousands of staff while leaving those conditions untouched produce frustrated employees and no measurable output change.</p>
<h2 id="which-skills-does-each-group-in-the-organisation-need">Which Skills Does Each Group in the Organisation Need?</h2>
<p>The single most common design error is delivering one curriculum to everyone. Readiness requirements differ sharply by group, and a programme optimised for the wrong audience wastes most of its budget. Three tiers cover most organisations, with a fourth that is frequently forgotten.</p>
<table class="article-table"><thead><tr><th>Audience</th><th>Core capability required</th><th>Depth</th><th>Typical time to competency</th></tr></thead><tbody><tr><td>All staff</td><td>Task decomposition, output scepticism, data handling rules</td><td>Awareness to working</td><td>2-4 weeks of applied practice</td></tr><tr><td>Business analysts and power users</td><td>Supervision, verification, question formulation, exception handling</td><td>Working to proficient</td><td>6-10 weeks on live work</td></tr><tr><td>Data and technical teams</td><td>Evaluation design, semantic modelling, grounding, governance enforcement</td><td>Proficient to expert</td><td>1-2 quarters on live migrations</td></tr><tr><td>Leaders and managers</td><td>Delegation decisions, consequence mapping, change sponsorship</td><td>Awareness to working</td><td>2-3 weeks plus ongoing cadence</td></tr></tbody></table>
<p>The forgotten tier is leadership, and its absence is why so many programmes stall after the first cohort. Managers make the delegation decisions: which tasks their teams hand to systems, which outputs require sign-off, and how performance is measured once the work changes. A manager who has not been trained will keep measuring yesterday's outputs — tickets closed, reports produced — and will therefore actively discourage the behaviour change the programme is trying to create. Train managers before the first cohort, not after.</p>
<p>There is also a naming problem worth fixing early. "AI literacy" sounds like a general education benefit and gets funded like one, which means it gets cut first. Frame the tiers as operational capability with named competencies and assessments attached, and it survives budget scrutiny because it can be tied to delivery outcomes.</p>
<h2 id="is-it-faster-to-train-or-to-hire-for-ai-readiness">Is It Faster to Train or to Hire for AI Readiness?</h2>
<p>At workforce scale, this is not a close call: training is faster, and hiring cannot work at all for the broad tiers. Consider the arithmetic. If readiness matters for two thousand employees and the market can supply you with fifty experienced people a year at a significant premium, the hiring path addresses 2.5% of the requirement annually while consuming most of the budget. Training is the only instrument that operates at the scale the problem actually has.</p>
<p>Hiring remains correct for a narrow set of needs. You hire for capabilities that are deep, durable, and absent internally: evaluation methodology, platform engineering for model serving, specialist security for AI systems. You also hire to import method, not just capacity — one experienced evaluator who establishes the standards and teaches them is worth more than three who simply execute. But hiring as a workforce readiness strategy is a category error.</p>
<p>The comparison also needs to account for a factor that hiring advocates rarely price in: context. An external hire spends their first two quarters learning how your business defines a customer, a completed sale, an at-risk account, and a valid exception. An internal candidate already knows these things and is limited only by method. For the supervision and verification skills that make up most of the readiness requirement, context is the larger part of the capability, which is precisely why internal development wins at scale.</p>
<ul>
<li><strong>Train at scale.</strong> Awareness, supervision, and verification across the whole workforce — these are context-heavy and method-light.</li>
<li><strong>Hire for depth.</strong> Evaluation leadership, platform and infrastructure specialism, AI security — durable crafts with no internal bench.</li>
<li><strong>Hire to transfer method.</strong> Every external specialist hire should carry an explicit obligation to establish standards and teach them.</li>
<li><strong>Buy time with services.</strong> Managed delivery for capability you need this quarter and may not need permanently.</li>
<li><strong>Re-baseline quarterly.</strong> Capabilities that were scarce last year may be commoditised now; move them from the hiring column to the training column.</li>
</ul>
<h2 id="how-do-you-design-training-that-actually-changes-behaviour">How Do You Design Training That Actually Changes Behaviour?</h2>
<p>The research on corporate training is unambiguous on one point: knowledge delivered without application decays within weeks. The design implication is that training must be built around a live deliverable, not around a syllabus. Four principles follow.</p>
<p>First, cohort and apprentice rather than broadcast and certify. Groups of six to ten people work on one real process — their own monthly close, their own claims triage queue, their own demand review — with a facilitator who has done the work before. They leave with a redesigned process and a measured before-and-after, not with a certificate. Second, sequence by consequence: start with the lowest-risk process that has real pain, so a failure is survivable and a success is visible. Third, teach scepticism explicitly. Include a session where participants are shown confidently wrong outputs drawn from their own domain and asked to find the error; this single exercise does more for supervision behaviour than any amount of tooling instruction.</p>
<p>Fourth, and most neglected: change the work immediately after training. If participants return to the same process, the same metrics, and the same queue, the training evaporates within a month. Assign the redesigned process as the new standard, update the performance measures to match, and give the cohort explicit permission to stop doing the old steps. Programmes that schedule the process change before the training ends have dramatically higher sustained adoption than programmes that treat adoption as a follow-up activity.</p>
<p>Two practical enablers accelerate this considerably. The first is a sanctioned, governed tool that works on the organisation's own data, so that what people learn in the cohort is what they can do at their desk the next morning. The second is a place to ask questions in the flow of work. This is where conversational analytics earns its place in a readiness programme: when staff can ask a business question in WeCom, DingTalk, Feishu, Teams, or WhatsApp and receive a sourced answer from governed data in seconds, practice becomes continuous rather than confined to a workshop. Beehive Strategy deploys that layer as a managed service in about two weeks on top of the warehouse you already run, which means cohorts train on the same system they will use daily.</p>
<h2 id="how-do-you-measure-workforce-ai-readiness">How Do You Measure Workforce AI Readiness?</h2>
<p>If you define readiness as behaviour, you can measure it — but not with the metrics most programmes use. Completion rates, licence usage, and satisfaction scores measure activity, not capability. Five indicators measure readiness.</p>
<ol>
<li><strong>Delegation rate.</strong> The share of eligible tasks in a process that are actually performed by a supervised system rather than by a human. This is the headline number for whether work has changed.</li>
<li><strong>Cycle time on the redesigned process.</strong> Measured before and after, per cohort, with the process named. This is the number finance will fund.</li>
<li><strong>Supervision quality.</strong> On a sampled basis, the share of machine outputs where the reviewer caught a material error, plus the share where they wrongly accepted one. This tells you whether scepticism training worked.</li>
<li><strong>Escalation precision.</strong> How often people escalate when they should, and do not escalate when they should not. Over-escalation indicates low calibrated trust; under-escalation is the risk that produces incidents.</li>
<li><strong>Process redesign count.</strong> The number of named processes formally changed as a result of the programme. If this is zero, nothing else matters.</li>
</ol>
<p>Publish these per cohort and per function, including the failures. Programmes that report only successes lose credibility with the finance function within two quarters, and the funding goes to something measurable instead. Programmes that report honestly get the second and third cohorts funded, because they have demonstrated that they can tell the difference between activity and outcome.</p>
<h2 id="what-does-a-12-month-workforce-plan-look-like">What Does a 12-Month Workforce Plan Look Like?</h2>
<p>A twelve-month horizon is long enough to change several processes and short enough to remain fundable. Quarter one: define readiness in behavioural terms, run a capability inventory, train the managers who will own delegation decisions, and select two pilot processes with real pain and measurable cycle times. Capture baselines before anything changes — this is the step that determines whether you can prove value later.</p>
<p>Quarter two: run the first two cohorts on those processes, with a facilitator and a mandated process change at the end. Deploy the sanctioned tool on governed data so that practice continues at the desk. Measure delegation rate, cycle time, and supervision quality, and publish the results including the parts that did not work. Quarter three: expand to four to six processes across different functions, promote the strongest cohort participants into facilitator roles, and hire the one or two external specialists whose job is to establish method rather than to add capacity.</p>
<p>One further design note saves a great deal of rework: decide, before the first cohort, what the organisation's position is on three questions participants will ask in the first hour. Which tools are sanctioned? Which data may be entered into them? And who is accountable if a delegated task produces a wrong result that reaches a customer? Ambiguity on the third question is the single most common reason capable people decline to delegate at all — they have worked out that the upside accrues to the business and the downside accrues to them. Answering it explicitly, in writing, with a named escalation path and an explicit statement that good-faith supervised delegation is not a disciplinary matter, does more for adoption than any amount of skills training.</p>
<p>Quarter four: formalise the operating model — write the new competencies into role profiles and performance objectives, publish the delegation and escalation standards, and run a readiness re-assessment against the quarter-one baseline. Then set next year's target in terms of processes changed rather than people trained. The organisations that get this right stop describing AI readiness as a training programme and start describing it as a measurable change in how work gets done — which is the only definition that survives contact with a budget review.</p>
"""

EN_FAQ = [
    ("What does it mean for a workforce to be AI-ready?",
     "It is a behavioural standard, not a training certificate. An AI-ready workforce can decompose its own work to identify delegable tasks, supervise machine outputs critically, calibrate trust according to consequence rather than confidence, and redesign processes once delegation is available. Usage metrics such as licence activation or prompt volume measure activity, not readiness — if the monthly review is still assembled by hand, capability has arrived but readiness has not."),
    ("Should we train existing staff or hire AI talent?",
     "Both, but at very different scales. Training is the only instrument that operates at workforce scale: if readiness matters for two thousand people and the market supplies fifty experienced hires a year, the hiring path addresses a small fraction of the need. Hire for depth instead — evaluation methodology, platform engineering, AI security — and require every specialist hire to establish standards and transfer them internally."),
    ("How long does it take to make a team AI-ready?",
     "For general staff, two to four weeks of applied practice on their own work is enough for awareness-to-working capability. Business analysts and power users need six to ten weeks on live processes to reach proficiency in supervision and verification. Data and technical teams need one to two quarters on live migrations to build evaluation and semantic modelling depth. None of these timelines hold if the training is not attached to a deliverable with a real deadline."),
    ("Why do AI training programmes fail to change behaviour?",
     "Three reasons dominate: the training is delivered as a syllabus rather than around a live process, managers are trained after the cohorts instead of before, and participants return to unchanged processes and metrics. Fix all three by running small cohorts on real work, training the managers who own delegation decisions first, and scheduling the process change to take effect before the training ends."),
    ("How should we measure AI readiness?",
     "Track five indicators: delegation rate (share of eligible tasks performed by supervised systems), cycle time on the redesigned process, supervision quality on sampled outputs, escalation precision, and the count of named processes formally changed. Report them per cohort and per function, including the failures — programmes that publish only successes lose funding credibility within two quarters."),
]

ZH_TOC = [
    ('AI就绪的团队究竟意味着什么', 'AI 就绪的团队究竟意味着什么？'),
    ('组织内不同群体分别需要哪些技能', '组织内不同群体分别需要哪些技能？'),
    ('为AI就绪度选择培训还是招聘更快', '为 AI 就绪度选择培训还是招聘更快？'),
    ('如何设计真正能改变行为的培训', '如何设计真正能改变行为的培训？'),
    ('如何衡量团队的AI就绪度', '如何衡量团队的 AI 就绪度？'),
    ('12个月的团队建设计划长什么样', '12 个月的团队建设计划长什么样？'),
]

ZH_PROSE = """
<p class="article-lead"><strong>"AI 就绪的团队"已经变成了一个什么都能指、因而什么都没指的词：一天提示词工作坊、一个数据科学学位、以及一次全员开通的聊天机器人许可，都被放在同一个标签下出售。</strong>有用的定义是行为层面的，而不是课程层面的。当做事的人能够识别出自己工作中哪些任务可以委派、能够监督一个正在执行这些任务的系统、知道何时应当质疑输出，并因此改变自己的工作方式时，这个团队就是 AI 就绪的。这个靶子比多数项目瞄准的要窄得多，也比一段培训视频能打中的要难得多。本文用可检验的术语定义就绪度，按受众拆分技能要求，诚实地比较培训与招聘两条路径，并给出一份改变行为而非改变出勤记录的十二个月计划。</p>
<h2 id="AI就绪的团队究竟意味着什么">AI 就绪的团队究竟意味着什么？</h2>
<p>就绪度不等于对工具的熟悉，也不等于写出一个巧妙提示词的能力。两者都会过期：工具每个季度都在变，而提示词技巧正在迅速被界面本身吸收。能够留存下来的是一组可以被观察和评估的四种行为。</p>
<ol>
<li><strong>任务分解。</strong>这个人能把自己的工作拆成组成部分，并识别出哪些部分是界定清晰、重复、低后果的（即可委派的部分），哪些需要判断力、上下文或问责。</li>
<li><strong>监督能力。</strong>这个人能批判性地审阅机器输出：核对来源、发现"看似合理但缺乏支撑"的陈述，并察觉答案所回应的其实不是被问的那个问题。</li>
<li><strong>校准过的信任。</strong>这个人知道何时可以依赖系统、何时应升级处理，判断依据是后果，而不是输出听起来有多自信。</li>
<li><strong>工作流重设计。</strong>一旦委派成为可能，这个人会改变做事的方式，而不是用 AI 把同一个流程做得稍微快一点。</li>
</ol>
<p>第四项行为正是多数项目失败的地方，值得多说几句。组织习惯用许可开通率或提示词使用量来衡量 AI 采用率，然后纳闷生产力为什么没有变化。使用量不是采用率。如果一位分析师用聊天机器人更快地起草了邮件，却仍然手工拼装月度复盘，因为流程就是这么规定的——那么能力已经到位，而就绪度没有。就绪度体现在流程被重新设计：复盘自己拼装自己，人类只处理例外，月度周期从五天缩短到一天。</p>
<p>还有一个结构性成分是个人无法自行提供的。如果所需数据未受治理、没有经过批准的工具、或者组织尚未决定什么可以委派什么不可以，那么团队不可能就绪。就绪度是系统的属性——人 + 数据 + 权限 + 流程——而不只是人的属性。在训练了数千名员工却对这些条件不闻不问的项目，产出的只有沮丧的员工，以及毫无变化的产出。</p>
<h2 id="组织内不同群体分别需要哪些技能">组织内不同群体分别需要哪些技能？</h2>
<p>最常见的设计错误，是给所有人同一套课程。就绪度需求因群体而差异巨大；一套为错误受众优化的课程，会浪费掉大部分预算。三个层级可以覆盖多数组织，此外还有第四个经常被遗忘的层级。</p>
<table class="article-table"><thead><tr><th>受众</th><th>所需核心能力</th><th>深度</th><th>达到胜任所需时间</th></tr></thead><tbody><tr><td>全体员工</td><td>任务分解、对输出保持怀疑、数据处理规则</td><td>认知到可用</td><td>2-4 周的应用练习</td></tr><tr><td>业务分析师与重度用户</td><td>监督、验证、问题表述、例外处理</td><td>可用到熟练</td><td>6-10 周的真实工作实践</td></tr><tr><td>数据与技术团队</td><td>评估设计、语义建模、依据接入、治理执行</td><td>熟练到专家</td><td>1-2 个季度的真实迁移实践</td></tr><tr><td>领导者与管理者</td><td>委派决策、后果映射、变革赞助</td><td>认知到可用</td><td>2-3 周加持续节奏</td></tr></tbody></table>
<p>被遗忘的层级是领导层，而它的缺席正是许多项目在第一批学员之后就停滞的原因。管理者做出的是委派决策：团队把哪些任务交给系统、哪些输出需要签字、以及工作改变之后如何衡量绩效。一位未受过训练的管理者会继续衡量昨天的产出——关闭了多少工单、产出了多少报告——因而会主动抑制项目试图创造的那种行为改变。在第一个 cohort 之前就培训管理者，而不是之后。</p>
<p>还有一个值得尽早修正的命名问题。"AI 素养"听起来像一项通识教育福利，也因此按福利被拨款，于是最先被砍。把各层级定义为附带具名能力与评估的运营能力，它就能在预算审查中存活下来，因为它可以被挂到交付结果上。</p>
<h2 id="为AI就绪度选择培训还是招聘更快">为 AI 就绪度选择培训还是招聘更快？</h2>
<p>在全员规模上，这根本不是势均力敌的比较：培训更快，而招聘对广泛的层级而言根本行不通。算一下：如果就绪度对两千名员工都有意义，而市场每年能以显著溢价供应五十位有经验的人，那么招聘路径每年只能解决需求的 2.5%，却消耗掉大部分预算。培训是唯一能在问题真实规模上运作的工具。</p>
<p>招聘对于一组狭窄的需求依然是正确的选择。你为那些深厚、持久、且内部没有人才储备的能力而招聘：评估方法论、模型服务的平台工程、AI 系统的专业安全。你也是为"引入方法"而招聘，而不只是为了产能——一位建立起标准并把标准教出去的资深评估负责人，比三位只会执行的人更有价值。但把招聘当成全员就绪度战略，是一种范畴错误。</p>
<p>这个比较还需要计入一个招聘倡导者很少定价的因素：上下文。一位外部新人在头两个季度里，要学习你的企业如何定义客户、成交、风险账户与有效例外；一位内部候选人对此早已了然，只受限于方法。而对于构成就绪度需求主体的监督与验证技能来说，上下文是这项能力中更大的那一部分，这也正是在规模上内部培养胜出的原因。</p>
<ul>
<li><strong>规模化靠培训。</strong>全员范围内的认知、监督与验证——这些是上下文密集、方法论轻量的能力。</li>
<li><strong>为深度而招聘。</strong>评估负责人、平台与基础设施专家、AI 安全——持久的手艺，内部没有储备。</li>
<li><strong>为转移方法而招聘。</strong>每一位外部专家的招聘，都应附带"建立标准并教会他人"的明确义务。</li>
<li><strong>用服务买时间。</strong>对"本季度就需要、但未必长期需要"的能力采用托管交付。</li>
<li><strong>每季度重新校准。</strong>去年稀缺的能力今年可能已被商品化；把它们从招聘栏移到培训栏。</li>
</ul>
<h2 id="如何设计真正能改变行为的培训">如何设计真正能改变行为的培训？</h2>
<p>关于企业培训的研究在一点上是明确的：没有被应用的知识会在数周内衰减。其设计含义是：培训必须围绕一件在办交付物来构建，而不是围绕一份教学大纲。由此产生四条原则。</p>
<p>第一，分组做学徒，而不是广播式发证。六到十人一组，围绕一个真实流程工作——他们自己的月结、自己的理赔分诊队列、自己的需求评审——配一位做过这项工作的引导者。他们带走的是一条被重新设计的流程和一份可对比的前后度量，而不是一张证书。第二，按后果排序：从风险最低、但确有痛点的流程开始，这样失败可以承受，成功可以被看见。第三，显式地教"怀疑"。安排一节这样的课：向学员展示若干条取材于他们自己领域、自信但错误的输出，请他们找出错误所在。仅这一项练习，对监督行为的塑造作用就超过任何数量的工具操作讲解。</p>
<p>第四，也是最被忽视的一条：培训结束后立刻改变工作。如果学员回到同样的流程、同样的指标、同样的队列，培训会在一个月内蒸发。把重新设计后的流程指定为新标准，相应更新绩效衡量口径，并明确允许这批学员停止执行旧步骤。那些在培训结束前就把流程变更排进日程的项目，其持续采用率远高于把采用当作后续活动来对待的项目。</p>
<p>有两个实操抓手能显著加速这一切。其一是有一款经过批准、且能作用于组织自身数据的受治理工具，让学员在 cohort 里学到的，就是第二天在工位上能做的事。其二是在工作流中随时提问的去处。这正是对话式分析在就绪度项目中的位置：当员工可以在企业微信、钉钉、飞书、Teams 或 WhatsApp 里提出业务问题，并在数秒内从受治理数据中拿到带来源的答案时，练习就从"局限于工作坊"变成了"持续发生"。蜂启咨询以托管服务方式、在你已在运行的仓库之上约两周即可部署这一层，这意味着学员在培训中用的就是他们日常要用的同一个系统。</p>
<h2 id="如何衡量团队的AI就绪度">如何衡量团队的 AI 就绪度？</h2>
<p>如果你把就绪度定义为行为，它就可被衡量——但不是用多数项目在用的那些指标。完成率、许可使用量与满意度衡量的是活动，不是能力。有五项指标衡量的是就绪度。</p>
<ol>
<li><strong>委派率。</strong>一个流程中合格任务里，实际由受监督系统而非人工完成的比例。这是"工作是否真的变了"的头号数字。</li>
<li><strong>被重设计流程的周期时间。</strong>按 cohort 测量前后变化，并明确流程名称。这是财务部门会为之掏钱的数字。</li>
<li><strong>监督质量。</strong>按抽样统计：审阅者抓出实质性错误的机器输出占比，以及错误接受的占比。这告诉你"怀疑训练"是否有效。</li>
<li><strong>升级精确度。</strong>该升级时升级了、不该升级时没有升级的频率。过度升级说明校准信任偏低；升级不足则会制造事故。</li>
<li><strong>流程重设计数量。</strong>因本项目而正式变更的具名流程数量。如果这项是零，其他都不重要。</li>
</ol>
<p>按 cohort 与按职能公开这些指标，包括失败的部分。只报成功的项目会在两个季度内失去财务部门的信任，预算会转而流向可衡量的事项；诚实报告的项目才能拿到第二、第三个 cohort 的预算，因为它们已经证明了自己能区分"活动"与"结果"。</p>
<h2 id="12个月的团队建设计划长什么样">12 个月的团队建设计划长什么样？</h2>
<p>十二个月的周期足够长到能改变若干流程，又足够短到仍能拿到预算。第一季度：用行为术语定义就绪度，做一次能力盘点，培训那些将拥有委派决策权的管理者，并选出两个痛点真实、周期时间可度量的试点流程。在任何变更发生之前采集基线——这一步决定了你日后能否证明价值。</p>
<p>第二季度：围绕这两个流程跑前两个 cohort，配引导者，并以一次强制的流程变更为收尾。在受治理数据上部署经批准的工具，让练习在工位上继续发生。度量委派率、周期时间与监督质量，并公开结果，包括那些没做成的部分。第三季度：扩张到跨职能的四到六个流程，把表现最强的学员提拔为引导者，并招聘一到两位外部专家——他们的职责是建立方法，而不是增加产能。</p>
<p>第四季度：把运营模式正式化——把新的能力项写进岗位说明书与绩效目标，发布委派与升级标准，并对照第一季度基线做一次就绪度复评。然后把明年的目标设定为"改变了多少流程"，而不是"培训了多少人"。做对这件事的组织，会不再把 AI 就绪度描述为一个培训项目，而开始把它描述为"工作方式发生了可度量的改变"——这也是唯一能在预算审查面前站得住的定义。</p>
"""

ZH_FAQ = [
    ("团队达到 AI 就绪意味着什么？",
     "它是一个行为标准，而不是培训证书。AI 就绪的团队能够分解自己的工作以识别可委派的任务，能够批判性地监督机器输出，能够按后果而非置信度来校准信任，并能在委派成为可能后重新设计流程。许可开通率或提示词使用量这类指标衡量的是活动，不是就绪度——如果月度复盘仍需手工拼装，那么能力已经到位，而就绪度没有。"),
    ("我们应该培训现有员工还是招聘 AI 人才？",
     "两者都要，但规模完全不同。培训是唯一能在全员规模上运作的工具：如果就绪度对两千人都有意义，而市场每年只能供应五十位有经验的人，招聘路径只能覆盖需求的一小部分。应当为深度而招聘——评估方法论、平台工程、AI 安全——并要求每一位专家招聘都承担建立标准并在内部转移标准的义务。"),
    ("让一支团队达到 AI 就绪需要多久？",
     "对普通员工，在自身工作上做两到四周的应用练习，足以达到从认知到可用的能力；业务分析师与重度用户需要在真实流程上实践六到十周，才能在监督与验证上达到熟练；数据与技术团队需要一到两个季度的真实迁移实践，才能建立起评估与语义建模的深度。如果培训没有挂在一个有真实截止日的交付物上，这些时间表都不成立。"),
    ("为什么 AI 培训项目无法改变行为？",
     "主要有三个原因：培训按教学大纲交付，而不是围绕真实流程；管理者在学员之后才受训，而不是之前；学员回到毫无变化的流程与指标中去。要同时修好这三点：围绕真实工作组织小组，先培训拥有委派决策权的管理者，并把流程变更安排在培训结束之前生效。"),
    ("我们应该如何衡量 AI 就绪度？",
     "跟踪五项指标：委派率（合格任务中由受监督系统完成的比例）、被重设计流程的周期时间、抽样输出的监督质量、升级精确度、以及正式变更的具名流程数量。按 cohort 与按职能公开这些指标，包括失败的部分——只报成功的项目会在两个季度内失去预算上的可信度。"),
]

cc = OpenCC('s2twp')
to_tw = cc.convert
TW_TOC = [(i, to_tw(t)) for i, t in ZH_TOC]

def main():
    patch.apply(os.path.join(ROOT, 'blog/articles/%s.html' % SLUG), EN_TOC, EN_PROSE, EN_FAQ, cta='Book a Demo')
    patch.apply(os.path.join(ROOT, 'zh-cn/blog/articles/%s.html' % SLUG), ZH_TOC, ZH_PROSE, ZH_FAQ,
                cta='预约演示', faq_title='常见问题', faq_label='常见问题')
    patch.apply(os.path.join(ROOT, 'zh-tw/blog/articles/%s.html' % SLUG), TW_TOC, to_tw(ZH_PROSE),
                [(to_tw(q), to_tw(a)) for q, a in ZH_FAQ],
                cta='預約示範', faq_title='常見問題', faq_label='常見問題')

if __name__ == '__main__':
    main()
