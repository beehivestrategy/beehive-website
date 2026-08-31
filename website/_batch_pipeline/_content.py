# -*- coding: utf-8 -*-
"""Content injection spec for gbatch_003 (15 slugs). AUG[slug]['en'|'zh'].
h2: id -> question text (only statement H2s need mapping).
expand: list of (id, question_title, html) inserted before FAQ. html is ONE triple-quoted string.
faq: list of (question, answer) -> exactly the FAQPage content (>=3).
excerpts: list of 3 one-sentence recommended-card summaries.
zh-TW is assembled from zh-CN via OpenCC in fix_article.py.
"""
AUG = {}

AUG["from-sql-to-natural-language-the-evolution-of-data-queries"] = {
    "en": {
        "expand": [],
        "faq": [
            ('''How does conversational BI change who gets to use data?''',
             '''It moves data access from a small group of SQL specialists to anyone who can ask a question in plain language. Because the person with the question becomes the person with the answer, decisions happen closer to the customer, the factory floor, and the cash flow, and the organisation starts asking better questions, not just faster ones.'''),
            ('''Is natural language query less accurate than SQL?''',
             '''Not when a semantic layer is present. Modern conversational BI resolves questions against governed metrics and dimensions rather than guessing at raw column names, so the answer matches what finance would calculate and can be audited afterwards. Without that layer, natural language is riskier than SQL; with it, it is more reliable because definitions are shared.'''),
            ('''Should we retire dashboards after adopting conversational BI?''',
             '''No. The three generations are a stack, not a succession. SQL remains essential for engineers, dashboards stay valuable for continuously monitored metrics, and natural language serves ad-hoc questions. The best results come when all three read from one governed semantic layer so they never disagree.'''),
            ('''What should we build first to prepare for conversational analytics?''',
             '''Build the foundation before the interface. Define core metrics in a semantic layer, fix data quality issues that would surface as wrong answers, and establish governance for who can query what. Once that foundation is solid, the conversational interface becomes a force multiplier instead of a source of confident mistakes.'''),
        ],
        "excerpts": [
            '''How data querying evolved from SQL specialists to natural language for everyone, and why the foundation matters most.''',
            '''Why each generation of data access removed a barrier and multiplied the people who could act on data.''',
            '''How a semantic layer makes natural-language queries trustworthy enough to automate on.''',
        ],
    },
    "zh": {
        "expand": [],
        "faq": [
            ('''对话式 BI 如何改变谁能使用数据？''',
             '''它把数据访问从少数 SQL 专家扩展到任何能用自然语言提问的人。由于提出问题的人同时成为得到答案的人，决策更贴近客户、产线与现金流，组织也开始提出更好的问题，而不只是更快的问题。'''),
            ('''自然语言查询是否不如 SQL 准确？''',
             '''在有语义层的前提下并非如此。现代对话式 BI 会把问题解析到受治理的指标与维度，而非猜测原始字段含义，因此答案与财务口径一致且可审计。没有语义层时自然语言风险更高，有语义层时反而更可靠，因为定义是统一的。'''),
            ('''采用对话式 BI 后是否应放弃仪表盘？''',
             '''不应。三代技术是叠加而非更替。SQL 对工程师仍不可或缺，仪表盘适合持续监控的指标，自然语言擅长即席问题。三者都从同一语义层读取时，结论才不会互相矛盾。'''),
            ('''为对话式分析应优先建设什么？''',
             '''先建基础，再建界面。先在语义层定义核心指标，修复会表现为错误答案的数据质量问题，并确立谁能查询什么的治理规则。基础稳固后，对话界面会成为倍增器，而非制造自信错误的源头。'''),
        ],
        "excerpts": [
            '''数据查询如何从 SQL 专家演进到人人可用的自然语言，以及为何基础最为关键。''',
            '''为何每一代数据访问都在消除一层障碍，并让能用数据行动的人成倍增加。''',
            '''语义层如何让自然语言查询可靠到足以支撑自动化。''',
        ],
    },
}

AUG["insurance-automated-underwriting-with-ai-risk-models"] = {
    "en": {
        "expand": [
            ("exp-1", '''How Should Insurers Govern Models That Make Underwriting Decisions?''',
             '''<p>Governance is what separates a defensible automated underwriting program from a regulatory liability. Start by separating the model that scores risk from the rules that decide outcomes: the score is a recommendation, the decision policy is owned by the business and must be legible to auditors. Keep a versioned record of every model, the data it was trained on, and the exact thresholds in force on any given day, so a declined application can always be explained after the fact.</p>
<p>Build a human-in-the-loop path for edge cases. Straight-through processing should cover the clear majority where the model is confident and the stakes are reversible, while material, ambiguous, or high-value applications escalate to a senior underwriter with the model's reasoning attached. This keeps speed where it is safe and judgement where it is needed, and it produces the review trail that regulators and reinsurers now expect.</p>'''),
        ],
        "faq": [
            ('''What makes an underwriting model safe to automate?''',
             '''A model is safe to automate when its inputs are governed, its outputs are explainable, and a human can override it. That means clean training data, documented decision thresholds, and an audit trail linking every decision back to the factors that drove it. Without those controls, straight-through processing trades speed for exposure you cannot defend.'''),
            ('''Does AI underwriting replace the underwriter?''',
             '''No. It removes repetitive triage and surfaces the cases that need judgement. Confident, low-stakes applications flow through automatically, while ambiguous or high-value ones reach a senior underwriter faster and with the model's reasoning attached, so the team spends its time on decisions only humans should make.'''),
            ('''How do you avoid bias in automated underwriting?''',
             '''Test the model against protected attributes and proxy variables before launch, monitor approval rates across segments in production, and keep a challenge path for adverse decisions. Bias is managed by governance and monitoring, not by assuming the algorithm is neutral, because historical data encodes historical bias.'''),
            ('''What is the first step an insurer should take?''',
             '''Pick one narrow line or segment where data quality is already high and the decision is reversible, then automate the triage there end to end. Prove the explanation, the audit trail, and the override path on a small scale before expanding to material underwriting decisions.'''),
        ],
        "excerpts": [
            '''How AI risk models are reshaping automated underwriting, and where human judgement must stay in the loop.''',
            '''The governance and explainability controls that make straight-through processing defensible.''',
            '''Why starting narrow and reversible is the safe path to automated underwriting.''',
        ],
    },
    "zh": {
        "expand": [
            ("exp-1", '''保险公司应如何治理做出核保决策的模型？''',
             '''<p>治理是把可辩护的自动化核保项目与监管负债区分开的关键。首先把评估风险的模型与决定结果的规则分开：评分只是建议，决策策略由业务方拥有且必须对审计者可读。为每一个模型、其训练数据以及当日生效的阈值保留带版本的记录，这样一笔被拒申请随时都能事后解释。</p>
<p>为边缘案例建立人在回路的通道。直通处理应覆盖模型有信心且后果可逆转的多数清晰案件，而重大、模糊或高价值的申请则升级给资深核保人，并附上模型的推理。这样在安全处保持速度，在需要处保留判断，也产出监管与再保方如今所期望的审查轨迹。</p>'''),
        ],
        "faq": [
            ('''什么让核保模型可以安全地自动化？''',
             '''当输入受治理、输出可解释、且人类能够覆盖时，模型才可安全自动化。这意味着干净的训练数据、文档化的决策阈值，以及把每个决策回溯到驱动因素的审计轨迹。缺少这些控制，直通处理只是用速度换取无法辩护的风险敞口。'''),
            ('''AI 核保会取代核保人吗？''',
             '''不会。它消除了重复的初筛，并凸显需要判断的案件。有信心且低风险的申请自动通过，模糊或高价值的申请更快到达资深核保人手中，并附上模型推理，让团队把时间花在只有人类该做的决策上。'''),
            ('''如何避免自动化核保中的偏见？''',
             '''上线前用受保护属性与代理变量测试模型，在生产中监控各客群的通过率，并为不利决策保留申诉通道。偏见靠治理与监控来管理，而非假定算法中立，因为历史数据本身就编码了历史偏见。'''),
            ('''保险公司第一步该做什么？''',
             '''选一条数据质量已高、决策可逆转的窄业务线或客群，把其中的初筛端到端自动化。在小范围验证解释、审计轨迹与覆盖路径后，再扩展到重大核保决策。'''),
        ],
        "excerpts": [
            '''AI 风险模型如何重塑自动化核保，以及人类的判断必须留在何处。''',
            '''让直通处理可被辩护的治理与可解释性控制。''',
            '''为何从窄而可逆转的场景起步是自动化核保的安全路径。''',
        ],
    },
}

AUG["what-is-aiops"] = {
    "en": {
        "expand": [
            ("exp-1", '''How Do You Measure Whether AIOps Is Actually Working?''',
             '''<p>The honest signal is not the dashboard but the operational result: mean time to detect, mean time to resolve, and the share of incidents handled without a human waking up. Track change-failure rate and the volume of pages that turned out to be noise, because AIOps earns its budget only when it cuts both toil and false alarms. Pair those with engineer-sentiment signals, since a tool that reduces pages but destroys trust has failed.</p>
<p>Tie measurement to business outcomes, not telemetry volume. A good program reports fewer customer-impacting incidents, lower on-call burnout, and faster recovery during peak trading or campaign periods. Report these as a monthly trend so leadership sees compounding returns, and feed the wins back into the feedback loop that teaches the models which correlations actually predict failure.</p>'''),
        ],
        "faq": [
            ('''What is the difference between AIOps and traditional monitoring?''',
             '''Traditional monitoring shows individual symptoms and leaves the human to connect them. AIOps correlates signals across the stack using topology, names the root cause, and proposes or triggers a remedy, turning what is broken into what you should do next.'''),
            ('''How long does it take to see value from AIOps?''',
             '''Noise reduction and faster resolution often appear within the first single-service pilot, in weeks. Broader value, sharper explanations, lower burnout, compounds over months as the feedback loop absorbs engineer judgement.'''),
            ('''Does AIOps replace the operations team?''',
             '''No. It removes toil and autonomously handles small, reversible failures, while escalating material or ambiguous incidents to a human with full context and a recommended action. The team moves from firefighting to design and resilience.'''),
            ('''What data do I need before starting AIOps?''',
             '''Telemetry across infrastructure, containers, services, and business transactions, plus a topology or service-map model. Without topology, correlations fire false alarms, so the service map is the component that makes AIOps real rather than a faster dashboard.'''),
        ],
        "excerpts": [
            '''A plain-language definition of AIOps and how it differs from traditional monitoring.''',
            '''The components, use cases, and getting-started path for an AIOps platform.''',
            '''How to measure AIOps by operational outcomes rather than telemetry volume.''',
        ],
    },
    "zh": {
        "expand": [
            ("exp-1", '''如何衡量 AIOps 是否真的有效？''',
             '''<p>真正可信的信号不是仪表盘，而是运营结果：平均检测时间、平均修复时间，以及无需人类被叫醒就能处理的事件占比。追踪变更失败率，以及最终被证明是误报的告警量，因为只有当 AIOps 同时削减琐事与误报时，才值回投入。把这些与工程师感受信号结合，因为一个减少告警却摧毁信任的工具已经失败。</p>
<p>把衡量绑定到业务结果，而非遥测数据量。好的项目能报告更少的客户影响事件、更低的值守倦怠，以及在交易或活动高峰时更快的恢复。以月度趋势呈现，让管理层看到复利式回报，并把成效反馈给教模型识别真正预示故障的相关性的循环。</p>'''),
        ],
        "faq": [
            ('''AIOps 与传统监控有何不同？''',
             '''传统监控呈现孤立症状，由人类自行串联。AIOps 借助拓扑跨栈关联信号、定位根因，并提出或触发修复，把"什么坏了"变成"下一步该做什么"。'''),
            ('''多久能看到 AIOps 的价值？''',
             '''噪声削减与更快修复常出现在首个单服务试点中，数周即可。更广泛的价值、更精准的解释、更低的倦怠，会随反馈回路吸收工程师判断而在数月内复利增长。'''),
            ('''AIOps 会取代运维团队吗？''',
             '''不会。它消除琐事并自动处理小型、可逆转的故障，同时把重大或模糊的事件升级给具备完整上下文与建议动作的运维人。团队从救火转向设计与韧性建设。'''),
            ('''启动 AIOps 前需要什么数据？''',
             '''覆盖基础设施、容器、服务与业务交易的遥测，加上拓扑或服务地图模型。没有拓扑，关联就会误报，因此服务地图才是让 AIOps 成真、而非仅更快仪表盘的关键组件。'''),
        ],
        "excerpts": [
            '''用通俗语言解释 AIOps，以及它和传统监控的区别。''',
            '''AIOps 平台的组件、使用场景与起步路径。''',
            '''如何以运营结果而非遥测数据量来衡量 AIOps。''',
        ],
    },
}

AUG["impact-ai-enterprise-procurement"] = {
    "en": {
        "expand": [
            ("exp-1", '''How Does AI Change the Role of the Procurement Team?''',
             '''<p>AI does not shrink procurement; it upgrades it. Routine tasks, matching purchase orders to contracts, classifying spend, and screening suppliers, move to models, which frees the team for negotiation, supplier development, and risk strategy. The buyer becomes a curator of the system: defining the rules, validating the exceptions, and owning the decisions the model only recommends.</p>
<p>The organisations that gain most treat procurement data as a shared asset. When spend, contracts, and supplier signals sit in one governed layer, AI can answer questions a controller could not, such as which suppliers concentrate risk across regions or where maverick spend hides. That visibility is the real return, because it turns procurement from a cost centre into a lever on margin and resilience.</p>'''),
        ],
        "faq": [
            ('''What is the data challenge in enterprise procurement?''',
             '''Procurement data is fragmented across ERP, contract repositories, and supplier portals, and it is inconsistently coded, so spend is hard to see and risk is hard to price. AI only helps once that data is cleaned and connected into one governed layer.'''),
            ('''How does AI improve supplier intelligence and risk management?''',
             '''Models combine internal spend with external signals, sanctions, financial health, and news, to score supplier risk continuously and flag concentrations a spreadsheet would miss. That turns risk management from an annual review into a daily, queryable view.'''),
            ('''How can AI transform spend analysis and optimisation?''',
             '''Instead of static reports, teams ask natural-language questions and get the answer with the definition already agreed. AI finds duplication, off-contract buying, and negotiation leverage by category, and recommends where consolidation actually saves money.'''),
            ('''How do you build AI-enabled procurement processes?''',
             '''Start with one category where data is clean, connect it to the governed layer, and let the model handle classification and screening while humans own negotiation. Expand category by category, keeping a human approval on anything material.'''),
        ],
        "excerpts": [
            '''How AI turns fragmented procurement data into supplier intelligence and spend leverage.''',
            '''Why a governed data layer is the prerequisite for AI in procurement.''',
            '''How the procurement team's role upgrades from data entry to strategy.''',
        ],
    },
    "zh": {
        "expand": [
            ("exp-1", '''AI 如何改变采购团队的角色？''',
             '''<p>AI 不会缩小采购，而是升级它。把采购订单与合同匹配、支出分类、供应商筛查等例行任务交给模型，团队得以投入谈判、供应商发展与风险策略。采购员变成系统的策展人：定义规则、校验例外，并拥有模型只作建议的决策。</p>
<p>获益最多的企业把采购数据当作共享资产。当支出、合同与供应商信号同处一个受治理层，AI 能回答控制员答不了的问题，例如哪些供应商在各地区集中了风险，或长尾违规支出藏在何处。这种可见性才是真正的回报，因为它把采购从成本中心变成利润与韧性的杠杆。</p>'''),
        ],
        "faq": [
            ('''企业采购中的数据挑战是什么？''',
             '''采购数据散落在 ERP、合同库与供应商门户中，且编码不一致，因此支出难看清、风险难定价。只有先把数据清洗并接入统一治理层，AI 才能发挥作用。'''),
            ('''AI 如何提升供应商情报与风险管理？''',
             '''模型把内部支出与外部信号（制裁、财务健康、新闻）结合，持续给供应商风险打分，并标出表格会遗漏的集中风险。这让风险管理从年度审查变成每日可查询的视图。'''),
            ('''AI 如何变革支出分析与优化？''',
             '''团队不再看静态报告，而是用自然语言提问并直接得到已达成共识口径的答案。AI 按品类找出重复、违规采购与谈判杠杆，并建议整合真正省钱之处。'''),
            ('''如何构建 AI 赋能的采购流程？''',
             '''从数据干净的一个品类起步，接入治理层，让模型处理分类与筛查，人类保留谈判决策。按品类扩展，对任何重大事项保留人类审批。'''),
        ],
        "excerpts": [
            '''AI 如何把碎片化的采购数据变为供应商情报与支出杠杆。''',
            '''为何受治理的数据层是采购引入 AI 的前提。''',
            '''采购团队的角色如何从录单升级为战略。''',
        ],
    },
}

AUG["real-world-ai-roi-metrics-that-matter"] = {
    "en": {
        "expand": [
            ("exp-1", '''Which AI ROI Metric Is Easiest to Defend to the CFO?''',
             '''<p>The most defensible metric is a hard operational one tied to money: hours returned to the workforce, decisions made faster, or errors avoided, each translated into a cost or revenue line. These survive scrutiny because they come from system logs, not surveys. A time-to-insight drop from a day to a minute is real and auditable; a vague productivity gain is not.</p>
<p>Build the case as a chain, not a single number. Show the activity the AI changed, the unit value of that activity, and the before-and-after measured from production data. When the CFO can trace a returned million from a faster query loop, the programme funds itself, and the dashboard becomes the receipt rather than the pitch.</p>'''),
        ],
        "faq": [
            ('''Why do technical measures mislead when tracking AI ROI?''',
             '''Accuracy, model size, and query latency feel like progress but say nothing about value. A model can be 99 percent accurate on the wrong task. ROI lives in business outcomes, hours saved, decisions accelerated, and errors avoided, not in model metrics that stakeholders cannot trace to money.'''),
            ('''What is the right business-outcome framework for AI ROI?''',
             '''Anchor on a small set of outcomes with a clear unit value: time-to-insight, analyst hours returned, decision cycle time, and error or leakage reduced. Each links to a cost or revenue line and can be measured from system logs, so the number is defensible.'''),
            ('''How do you calculate ROI for conversational BI?''',
             '''Count the questions now answered in seconds that once waited a day, multiply by the loaded cost of the person asking, and add the value of faster decisions. Keep the formula visible so the CFO can trace every dollar back to a measured behaviour change.'''),
            ('''How do you build an AI ROI dashboard?''',
             '''Put the activity changed, its unit value, and the before-and-after from production data on one screen. Update it monthly. The dashboard is the receipt for the investment, not a marketing slide, so it must show source data anyone can audit.'''),
        ],
        "excerpts": [
            '''Why technical AI metrics mislead and which business outcomes actually prove ROI.''',
            '''A defensible framework for calculating conversational BI return on investment.''',
            '''How to build an AI ROI dashboard the CFO can audit.''',
        ],
    },
    "zh": {
        "expand": [
            ("exp-1", '''哪个 AI 投资回报指标最容易向 CFO 辩护？''',
             '''<p>最易辩护的是与钱挂钩的硬运营指标：返还给员工的工时、更快做出的决策、或被避免的错误，每一项都折算成成本或收入线。它们经得起推敲，因为来自系统日志而非问卷。洞察时间从一天降到一分钟是真实可审计的；模糊的"效率提升"则不是。</p>
<p>把论证建成链条而非单一数字。展示 AI 改变的活动、该活动的单位价值，以及来自生产数据的前后对比。当 CFO 能从更快的查询循环追溯出返还的百万成本，项目就自给自足，仪表盘也成了收据而非推销。</p>'''),
        ],
        "faq": [
            ('''为何技术衡量会误导 AI 投资回报？''',
             '''准确率、模型规模、查询延迟看似进步，却与价值无关。模型可能在错误的任务上达到 99% 准确率。ROI 存在于业务结果、节省的工时、加速的决策与避免的错误中，而非干系人无法折算成钱的模型指标。'''),
            ('''AI 投资回报的正确业务成果框架是什么？''',
             '''锚定少数具备清晰单位价值的成果：洞察时间、返还的分析师工时、决策周期、以及降低的错误或流失。每一项都连到成本或收入线，并可由系统日志衡量，因而数字可辩护。'''),
            ('''如何计算对话式 BI 的投资回报？''',
             '''把如今几秒答出、曾经要等一天的提问数量，乘以提问者的加权成本，再加上更快决策的附加值。让公式可见，CFO 就能把每块钱追溯到一个可测量的行为改变。'''),
            ('''如何构建 AI 投资回报仪表盘？''',
             '''把被改变的活动、其单位价值，以及生产数据的前后对比放在同一屏，每月更新。仪表盘是投资的收据而非营销幻灯片，必须展示任何人都可审计的源数据。'''),
        ],
        "excerpts": [
            '''为何技术 AI 指标会误导，以及哪些业务成果才真正证明 ROI。''',
            '''计算对话式 BI 投资回报的可辩护框架。''',
            '''如何构建 CFO 可审计的 AI 投资回报仪表盘。''',
        ],
    },
}

AUG["supply-chain-carbon-tracking-ai-sustainability"] = {
    "en": {
        "expand": [
            ("exp-1", '''How Does AI Make Scope 3 Emissions Actually Measurable?''',
             '''<p>Scope 3 is the hard part because the data lives outside your systems, with suppliers you do not control. AI helps by estimating from proxies, spend categories, and activity data where primary measurement is impossible, then tightening those estimates as real data arrives. The result is a defensible range rather than a blank, and a way to prioritise which suppliers to engage first.</p>
<p>The payback is not only compliance. Teams that can see carbon by product, lane, and supplier make better sourcing and design choices, and they answer customer and regulator questions in minutes instead of months. AI turns sustainability from an annual reporting scramble into a continuous operational signal that feeds procurement and product decisions.</p>'''),
        ],
        "faq": [
            ('''What does the industry landscape for AI adoption look like?''',
             '''Adoption is uneven: leaders use AI to estimate and cut emissions continuously, while most firms still assemble annual spreadsheets. The gap is widening because regulators and customers now ask for product-level carbon data that manual processes cannot produce on time.'''),
            ('''What are the key use cases and implementation patterns?''',
             '''Primary use cases are spend-based Scope 3 estimation, supplier scorecards, anomaly detection in reported data, and scenario modelling for sourcing changes. The pattern is a governed data layer plus models, not a one-off report.'''),
            ('''How do you overcome implementation challenges?''',
             '''Start where you already have data, proxy the rest, and improve estimates as suppliers report. The blocker is rarely the model, it is data access and ownership, so secure a mandate and a single owner before tooling.'''),
            ('''How do you report Scope 3 emissions you cannot directly measure?''',
             '''Use recognised spend- and activity-based estimation methods, label them as estimates, and tighten them with primary data over time. AI makes this defensible by showing the assumption behind every number and updating it as evidence arrives.'''),
        ],
        "excerpts": [
            '''How AI makes Scope 3 emissions measurable and turns carbon into an operational signal.''',
            '''The use cases and implementation patterns for AI in supply-chain sustainability.''',
            '''Why starting with available data beats waiting for perfect measurement.''',
        ],
    },
    "zh": {
        "expand": [
            ("exp-1", '''AI 如何真正让范围三排放可测量？''',
             '''<p>范围三最难，因为数据在您系统之外、在您无法控制的供应商处。AI 借助代理、支出类别与活动数据，在无法直接测量处做估算，并在真实数据到来时收紧估算。结果是一段可辩护的区间而非空白，也让人知道该先撬动哪些供应商。</p>
<p>回报不止合规。能按产品、线路、供应商看到碳排的团队会做出更好的采购与设计选择，并在几分钟而非数月内回答客户与监管问题。AI 把可持续从年度填报的忙乱，变成支撑采购与产品决策的连续运营信号。</p>'''),
        ],
        "faq": [
            ('''AI 采用的行业格局如何？''',
             '''采用并不均衡：领先者用 AI 持续估算并削减排放，多数企业仍在拼年度表格。差距正在拉大，因为监管与客户现在要求产品级碳数据，手工流程无法按时产出。'''),
            ('''关键用例与实施模式有哪些？''',
             '''主要用例是基于支出的范围三估算、供应商记分卡、上报数据中的异常检测，以及采购变动的情景建模。模式是"受治理数据层加模型"，而非一次性报告。'''),
            ('''如何克服实施挑战？''',
             '''从已有数据处起步，其余用代理，并随供应商上报而改善估算。瓶颈很少在模型，而在数据访问与归属，所以先拿到授权与单一负责人，再上工具。'''),
            ('''无法直测的范围三排放如何报告？''',
             '''采用公认的基于支出与活动的估算方法，标注为估算，并随一手数据逐步收紧。AI 通过展示每个数字背后的假设并随证据更新，使估算可被辩护。'''),
        ],
        "excerpts": [
            '''AI 如何让范围三排放可测量，并把碳排变成运营信号。''',
            '''AI 在供应链可持续中的用例与实施模式。''',
            '''为何从已有数据起步胜过等待完美测量。''',
        ],
    },
}

AUG["ai-strategy-board-presentation"] = {
    "en": {
        "expand": [
            ("exp-1", '''How Do You Answer "What Does It Cost?" in the Boardroom?''',
             '''<p>Boards do not fund models, they fund outcomes with a known cost and a defensible return. Lead with the problem the AI removes, the value of solving it, and the investment as a range with milestones. Show the cost of inaction next to the cost of action, because the credible comparison is not the budget against zero, it is the budget against the risk of standing still.</p>
<p>Make the roadmap boring on purpose. A board trusts a staged plan with checkpoints and kill criteria more than a grand vision. Tie each phase to a metric they already care about, cycle time, margin, or risk, and commit to reporting against it. That discipline is what turns a strategy deck into an approved programme.</p>'''),
        ],
        "faq": [
            ('''How do you frame the current landscape for the board?''',
             '''Show where peers and regulators already treat AI as table stakes, and what inaction costs in margin and risk. The board needs context, not a feature list, so frame the landscape as a choice the company is already making by waiting.'''),
            ('''What are the key principles and strategic framework?''',
             '''Anchor on a few principles: one governed data foundation, use cases tied to value, and human oversight on material decisions. The framework is a portfolio of bets with milestones, not a single moonshot.'''),
            ('''What is the implementation approach and best practices?''',
             '''Run staged pilots with clear success metrics and kill criteria, fund the winners, and retire the losers. Best practice is to report against the metric promised, so credibility compounds with each phase.'''),
            ('''How do you measure success and demonstrate ROI?''',
             '''Tie every phase to a business metric the board already tracks, cycle time, margin, or risk, and report before-and-after from production data. ROI is proven by a traced chain from activity to value, not by a model score.'''),
        ],
        "excerpts": [
            '''How to present an AI strategy to the board around outcomes, cost, and defensible return.''',
            '''The principles and framework that make an AI strategy credible to non-technical directors.''',
            '''Why a staged roadmap with kill criteria beats a grand vision in the boardroom.''',
        ],
    },
    "zh": {
        "expand": [
            ("exp-1", '''如何在董事会上回答"要花多少钱？"''',
             '''<p>董事会不为模型买单，而为有明确成本与可辩护回报的结果买单。先讲 AI 消除了什么问题、解决它的价值，再把投入作为带里程碑的区间呈现。把"不作为的成本"与"行动的成本"并列，因为可信的比较不是预算对零，而是预算对原地不动的风险。</p>
<p>刻意把路线图做得"无趣"。董事会更信任带检查点与终止标准的分阶段计划，而非宏大愿景。把每个阶段绑定到他们本就关心的指标：周期、利润或风险，并承诺据此汇报。这种纪律才把战略幻灯片变成获批的项目。</p>'''),
        ],
        "faq": [
            ('''如何为董事会框定当前格局？''',
             '''展示同行与监管已把 AI 视为标配，以及不作为在利润与风险上的代价。董事会需要背景而非功能清单，所以把格局框定为"等待本身就是在做选择"。'''),
            ('''关键原则与战略框架是什么？''',
             '''锚定少数原则：一个受治理的数据基础、绑定价值的用例、以及对重大决策的人类监督。框架是一组带里程碑的押注组合，而非单一登月。'''),
            ('''实施方法与最佳实践有哪些？''',
             '''运行带明确成功指标与终止标准的分阶段试点，注资胜者、淘汰败者。最佳实践是按承诺的指标汇报，让可信度随每阶段复利。'''),
            ('''如何衡量成功并展示投资回报？''',
             '''把每个阶段绑定到董事会本就追踪的业务指标：周期、利润或风险，并用生产数据展示前后对比。ROI 由从活动到价值的可追溯链条证明，而非模型分数。'''),
        ],
        "excerpts": [
            '''如何围绕结果、成本与可辩护回报向董事会呈现 AI 战略。''',
            '''让 AI 战略在非技术董事眼中可信的原则与框架。''',
            '''为何分阶段、带终止标准的路线图胜过董事会里的宏大愿景。''',
        ],
    },
}

AUG["data-sharing-agreements-ai-training-legal"] = {
    "en": {
        "expand": [
            ("exp-1", '''What Should a Data-Sharing Agreement Cover Before Training Data Changes Hands?''',
             '''<p>Before any data moves, the agreement must name the exact purpose, the permitted models, the retention and deletion rules, and who owns the derived outputs. Specify that training use is bounded, that personal data is minimised or synthetic, and that the receiving party cannot resell or sub-license. The clause that matters most is audit rights, because without them you cannot prove compliance later.</p>
<p>Pair the contract with technical controls. Purpose limitation is unenforceable on paper if the data lake allows unrestricted use, so bind the agreement to access controls, usage logs, and a register of approved models. Legal and engineering must sign the same document, or the agreement will describe a world the systems cannot actually enforce.</p>'''),
        ],
        "faq": [
            ('''Why is data governance imperative for AI?''',
             '''AI amplifies whatever data it trains on, so weak governance becomes weak or unlawful models at scale. Governance sets the purpose, ownership, and limits that keep training data defensible and the outputs trustworthy.'''),
            ('''How do you design and implement a governance framework?''',
             '''Define data domains and owners, write purpose-limited sharing rules, and bind them to access controls and usage logs. Implementation is engineering as much as policy, because a rule no system enforces is not real.'''),
            ('''What are the operational challenges and solutions?''',
             '''Challenges are tracking lineage across teams and proving consent at audit. Solutions are a data register, automated logs, and contracts written in terms the systems can check, not just lawyers.'''),
            ('''How do you build a sustainable governance model?''',
             '''Make governance part of the delivery process, not a gatekeeping team. Assign domain owners, review on a schedule, and feed audit findings back into the rules, so the model improves instead of decaying.'''),
        ],
        "excerpts": [
            '''What a data-sharing agreement must cover before AI training data changes hands.''',
            '''Why governance is the difference between defensible and unlawful AI.''',
            '''How to bind legal agreements to systems that can actually enforce them.''',
        ],
    },
    "zh": {
        "expand": [
            ("exp-1", '''训练数据交接前，数据共享协议应涵盖什么？''',
             '''<p>数据移动前，协议必须写明确切目的、允许的模型、留存与删除规则，以及衍生成果归谁。须明确训练用途受限、个人数据最小化或合成化，且接收方不得转售或再许可。最关键的条款是审计权，因为没有它，事后无法证明合规。</p>
<p>让合同配上技术控制。若数据湖允许无限制使用，目的限制就只是一纸空文，因此要把协议绑定到访问控制、使用日志与已批准模型登记。法务与工程必须签署同一份文件，否则协议描述的是系统实际无法执行的世界。</p>'''),
        ],
        "faq": [
            ('''为何数据治理对 AI 不可或缺？''',
             '''AI 会放大其训练数据的一切，因此薄弱治理会在规模上变成薄弱或违法的模型。治理设定目的、归属与边界，使训练数据可辩护、产出可信。'''),
            ('''如何设计与实施治理框架？''',
             '''定义数据域与负责人，写下目的受限的共享规则，并将其绑定到访问控制与使用日志。实施既是工程也是政策，因为系统不执行的规则不算真规则。'''),
            ('''运营挑战与解决方案有哪些？''',
             '''挑战是跨团队追踪血缘、在审计时证明同意。解决方案是数据登记、自动化日志，以及用系统可校验的措辞写合同，而非只给律师看。'''),
            ('''如何构建可持续的治理模式？''',
             '''把治理变成交付流程的一部分，而非把关团队。指派域负责人、按期审查，并把审计发现回馈规则，使模型改进而非退化。'''),
        ],
        "excerpts": [
            '''AI 训练数据交接前，数据共享协议必须涵盖什么。''',
            '''为何治理是可辩护 AI 与违法 AI 的分水岭。''',
            '''如何让法律协议绑定到真正能执行的系统。''',
        ],
    },
}

AUG["automating-data-pipelines-ai-practical-guide"] = {
    "en": {
        "expand": [
            ("exp-1", '''How Does AI Automate Pipeline Development?''',
             '''<p>AI assists by generating connectors and transformation code from a description, suggesting schemas, and writing the tests that catch drift. It does not replace the data engineer; it removes the boilerplate so the engineer spends time on semantics and trust. The practical win is a first draft of a pipeline in minutes, reviewed and hardened by a human who owns the result.</p>
<p>Monitoring is where automation pays for itself. Models learn normal shapes and volumes per table, then flag anomalies, stuck jobs, or schema drift before the dashboard lies. Combined with self-repair for the small, known failures, this turns pipelines from a maintenance tax into a system that mostly looks after itself, freeing the team for modelling.</p>'''),
            ("exp-2", '''How Do You Move From Pilot to Scaled Production?''',
             '''<p>Scale by standardising on one platform and one pattern, not by letting each team invent its own. Start with the pipelines that break most often, prove the monitoring catches them, then roll the pattern out categorically. Keep a human approval on anything that touches a source of record, and keep the generated code in version control so every auto-fix is reviewable and reversible.</p>'''),
        ],
        "faq": [
            ('''What is the pipeline scaling challenge?''',
             '''As pipelines multiply, failures multiply faster, and the team spends its week firefighting instead of building. The challenge is keeping reliability while the number of pipelines and sources grows beyond what manual monitoring can cover.'''),
            ('''How does AI automate pipeline development?''',
             '''AI generates connectors and transformation code from descriptions, suggests schemas, and writes drift tests. It removes boilerplate so engineers focus on semantics and trust, with a human reviewing every generated pipeline.'''),
            ('''What does AI-powered monitoring and self-repair do?''',
             '''Models learn normal shapes per table, flag anomalies and schema drift before dashboards lie, and auto-fix small known failures. This turns pipelines from a maintenance tax into a system that largely maintains itself.'''),
            ('''How do you integrate pipeline automation with conversational BI?''',
             '''Clean, monitored pipelines feed the semantic layer that conversational BI queries. Automation keeps the data fresh and trustworthy, which is what makes a natural-language answer safe to act on.'''),
        ],
        "excerpts": [
            '''How AI generates and monitors data pipelines so engineers focus on trust.''',
            '''Why self-repair and anomaly detection turn pipelines into a managed system.''',
            '''How reliable pipelines feed the semantic layer behind conversational BI.''',
        ],
    },
    "zh": {
        "expand": [
            ("exp-1", '''AI 如何自动化管道开发？''',
             '''<p>AI 根据描述生成连接器与转换代码、建议schema，并编写捕获漂移的测试。它不取代数据工程师，而是消减样板，让工程师把时间花在语义与信任上。实际收益是数分钟得到管道初稿，由对结果负责的人类审查加固。</p>
<p>监控才是自动化回本之处。模型学习每张表的正常形态与体量，在仪表盘说谎前标出异常、卡住的任务或schema 漂移。结合对小型已知故障的自修复，管道从维护负担变成基本自治的系统，释放团队去做建模。</p>'''),
            ("exp-2", '''如何从试点走向规模化生产？''',
             '''<p>规模化要统一到一个平台、一种模式，而非各团队自创。从最易断裂的管道起步，证明监控能抓住它们，再按品类推广。对任何触及记录源的作业保留人类审批，并把生成代码纳入版本控制，使每次自动修复都可审查、可回退。</p>'''),
        ],
        "faq": [
            ('''管道规模化的挑战是什么？''',
             '''管道增多，故障增长更快，团队整周救火而非建设。挑战是在管道与数据源数量超出人工监控能力时，仍保持可靠性。'''),
            ('''AI 如何自动化管道开发？''',
             '''AI 按描述生成连接器与转换代码、建议schema、编写漂移测试。它消减样板，让工程师专注语义与信任，每个生成管道都由人类审查。'''),
            ('''AI 监控与自修复做什么？''',
             '''模型学习每张表的正常形态，在仪表盘说谎前标出异常与schema漂移，并自动修复小型已知故障。这让管道从维护负担变成基本自治的系统。'''),
            ('''如何将管道自动化与对话式 BI 集成？''',
             '''干净且受监控的管道供给对话式 BI 查询的语义层。自动化保持数据新鲜可信，这正是自然语言答案可被放心执行的前提。'''),
        ],
        "excerpts": [
            '''AI 如何生成并监控数据管道，让工程师专注信任。''',
            '''为何自修复与异常检测把管道变成受管系统。''',
            '''可靠的管道如何供给对话式 BI 背后的语义层。''',
        ],
    },
}

AUG["ai-platform-build-vs-buy-decision-framework"] = {
    "en": {
        "expand": [
            ("exp-1", '''When Does Building an AI Platform Actually Pay Off?''',
             '''<p>Building pays off only when the capability is your differentiator and you can staff it for the long run. If the platform is table stakes, buying frees your team for the models and data that actually separate you from competitors. The honest test is whether the build creates a moat or just recreates a commodity that a vendor ships cheaper every quarter.</p>
<p>Most enterprises should assemble instead of pure build or buy: buy the hardened infrastructure, build the thin layer of logic that encodes your domain and governance, and integrate with MCP so agents can reach your data safely. That keeps you differentiated where it counts while avoiding the maintenance tax of reinventing the substrate.</p>'''),
        ],
        "faq": [
            ('''Why is enterprise AI a strategic imperative in 2025?''',
             '''By 2025 AI is a cost of entry in most functions, and the gap is widening between firms that query their data conversationally and those that still file tickets. The imperative is to build the foundation before competitors compound the advantage.'''),
            ('''What should you always buy?''',
             '''Buy the commodity substrate: vector stores, orchestration, evaluation harnesses, and connectors. These are expensive to build well, converge across vendors, and are not where your differentiation lives, so buying them is cheaper and faster.'''),
            ('''What is the framework for AI strategy development?''',
             '''Map capabilities into buy, build, or assemble. Buy commodities, build only the domain logic that is your moat, and assemble the two through open integration. Decide per capability, not as a single religious choice.'''),
            ('''When does building an AI platform actually pay off?''',
             '''Only when the platform itself is your differentiator and you can staff it for years. Otherwise building recreates a commodity a vendor ships cheaper, and you pay the maintenance tax without the moat.'''),
        ],
        "excerpts": [
            '''A decision framework for build, buy, or assemble when choosing an AI platform.''',
            '''Why most enterprises should assemble the thin differentiating layer, not rebuild the substrate.''',
            '''How to tell whether building an AI platform creates a moat or a commodity.''',
        ],
    },
    "zh": {
        "expand": [
            ("exp-1", '''何时自建 AI 平台才真正划算？''',
             '''<p>只有当该能力是您的差异化优势、且能长期配备人手时，自建才划算。若平台只是标配，购买能把团队解放出来，去做真正把您与对手区分开的模型与数据。诚实的检验是：自建究竟筑起护城河，还是只是在重造供应商每季度更便宜地交付的商品。</p>
<p>多数企业应当"组装"而非纯粹自建或购买：买下成熟的基础设施，自建编码您领域与治理的薄逻辑层，并用 MCP 集成，让智能体能安全触达数据。这样在关键处保持差异，又避免重造底层基座的维护负担。</p>'''),
        ],
        "faq": [
            ('''为何 2025 年企业 AI 是战略紧迫性？''',
             '''到 2025 年，AI 已是多数职能的入场成本，能用自然语言查数据的企业与仍在填工单的企业差距正在拉大。紧迫性在于在对手复利式领先前打好基础。'''),
            ('''什么应该永远购买？''',
             '''购买商品化底座：向量库、编排、评测框架与连接器。这些建好很贵、跨供应商趋同，且非差异化所在，购买更省更快。'''),
            ('''AI 战略开发的框架是什么？''',
             '''把能力映射到购买、自建或组装。买商品，只自建作为护城河的领域逻辑，用开放集成把两者组装起来。按能力决策，而非一句宗教式口号。'''),
            ('''何时自建 AI 平台才真正划算？''',
             '''只有当平台本身就是差异化优势且能多年配备人手时。否则自建只是在重造商品，您付出维护负担却没得到护城河。'''),
        ],
        "excerpts": [
            '''选择 AI 平台时，自建、购买或组装的决策框架。''',
            '''为何多数企业应组装差异化的薄层，而非重建底层。''',
            '''如何判断自建 AI 平台是筑起护城河还是造出商品。''',
        ],
    },
}

AUG["ai-powered-financial-risk-control-real-time-monitoring"] = {
    "en": {
        "expand": [
            ("exp-1", '''What Are the Three Layers of AI-Powered Risk Control?''',
             '''<p>The data layer unifies signals from transactions, ledgers, and market feeds into one governed view. The model layer scores risk, detects anomalies, and explains them in plain language. The action layer routes decisions to a human or, for small reversible cases, acts within a tight policy. The layer that matters most is the data one, because every false alert upstream is a real cost downstream.</p>
<p>Real time changes the economics of risk. Instead of a batch report reviewed after the loss, the system flags a stray payment or a concentration breach as it happens, with the reason attached. That compresses the loop from days to seconds and lets a small risk team cover a far larger book than a report-driven one ever could.</p>'''),
            ("exp-2", '''Why Is MCP the Missing Link for Risk Data Integration?''',
             '''<p>Risk data lives in core banking, fraud, market, and CRM systems that rarely speak to each other. MCP gives the AI a standard, governed way to reach each source on demand, with access controls enforced at the boundary. That means the model answers from live data instead of a stale extract, and auditors can see exactly which systems a decision touched.</p>'''),
        ],
        "faq": [
            ('''Why is financial risk control moving to real time?''',
             '''Losses are cheapest to stop at the moment they happen, not in a report reviewed days later. Real-time control flags stray payments and concentration breaches as they occur, with the reason attached, compressing the loop from days to seconds.'''),
            ('''What are the three layers of AI-powered risk control?''',
             '''A data layer that unifies signals, a model layer that scores and explains risk, and an action layer that routes decisions to a human or acts within policy. The data layer matters most, because upstream errors become downstream cost.'''),
            ('''Why is MCP the missing link for risk data integration?''',
             '''Risk data sits in siloed systems that rarely connect. MCP gives the AI a standard, governed, access-controlled way to reach each source live, so answers come from current data and auditors see which systems a decision touched.'''),
            ('''How do you measure ROI in speed, accuracy, and compliance?''',
             '''Track time-to-flag, false-positive rate, and the share of decisions auto-documented for audit. Faster flags and fewer false alarms are measurable from logs, and compliance becomes a by-product of the trail rather than a separate exercise.'''),
        ],
        "excerpts": [
            '''The three layers of real-time, AI-powered financial risk control.''',
            '''Why MCP is the integration link that makes risk data live and auditable.''',
            '''How real-time control turns compliance into a by-product of the audit trail.''',
        ],
    },
    "zh": {
        "expand": [
            ("exp-1", '''人工智能风控的三层架构是什么？''',
             '''<p>数据层把交易、总账与市场馈送的信号统一成一个受治理视图。模型层为风险打分、检测异常并用通俗语言解释。行动层把决策路由给人类，或在小型可逆转案件里按严格策略执行。最关键是数据层，因为上游每个误报都是下游的真实成本。</p>
<p>实时改变了风险的经济学。系统不再在损失发生后才看批量报告，而是在异常付款或集中度突破发生的当下就标出，并附上原因。这让闭环从数天压到数秒，使小团队能覆盖比报告驱动模式大得多的账本。</p>'''),
            ("exp-2", '''为何 MCP 是风险数据集成缺失的一环？''',
             '''<p>风险数据散落在核心银行、反欺诈、市场与 CRM 等彼此很少对话的系统里。MCP 给 AI 一条标准、受治理、带边界访问控制的按需触达路径。于是模型用实时数据作答，而非陈旧抽取，审计也能看清某决策究竟触碰了哪些系统。</p>'''),
        ],
        "faq": [
            ('''为何金融风险控制走向实时？''',
             '''损失在最发生的当下制止最便宜，而非数天后看报告。实时控制在异常付款与集中度突破发生时就标出并附原因，把闭环从数天压到数秒。'''),
            ('''人工智能风控的三层架构是什么？''',
             '''数据层统一信号，模型层打分并解释风险，行动层把决策路由给人类或按策略执行。数据层最关键，因为上游错误会变成下游成本。'''),
            ('''为何 MCP 是风险数据集成缺失的一环？''',
             '''风险数据位于彼此割裂的系统。MCP 给 AI 一条标准、受治理、带边界访问控制的实时触达路径，使答案来自当前数据，审计也能看清决策触碰了哪些系统。'''),
            ('''如何衡量速度、准确性与合规上的投资回报？''',
             '''追踪标警时长、误报率，以及自动留档供审计的决策占比。更快标警与更少误报可由日志衡量，合规成为审计轨迹的副产品而非单独工作。'''),
        ],
        "excerpts": [
            '''实时人工智能风控的三层架构。''',
            '''为何 MCP 是让风险数据实时且可审计的集成环节。''',
            '''实时控制如何把合规变成审计轨迹的副产品。''',
        ],
    },
}

AUG["conversational-analytics-metrics-20260114"] = {
    "en": {
        "expand": [
            ("exp-1", '''What Should a Conversational BI Scorecard Contain?''',
             '''<p>A useful scorecard tracks adoption, not just usage: active question-askers, questions per session, and self-service resolution rate, the share answered without a ticket. Add answer quality signals, thumbs on answers and repeat questions, and the time-to-insight the loop actually delivers. Together these show whether people trust the system enough to rely on it.</p>
<p>The metric that predicts renewal is self-service resolution. If conversational BI keeps deflecting tickets to the data team, it is a toy; if the share of questions answered in-product keeps rising, it is infrastructure. Report that trend to the board and the programme funds itself on the backlog it retires.</p>'''),
        ],
        "faq": [
            ('''How do you understand the current landscape?''',
             '''The landscape has shifted from dashboards to conversational, queryable data, and buyers now expect natural-language answers backed by governed metrics. Understanding it means seeing where your peers already treat this as baseline.'''),
            ('''What is the implementation approach and best practices?''',
             '''Connect a semantic layer, launch on the highest-volume questions, and watch answer quality. Best practice is to start narrow, prove trust, then broaden, keeping a human fallback for anything material.'''),
            ('''What should a conversational BI scorecard contain?''',
             '''Track active askers, questions per session, self-service resolution rate, answer quality, and time-to-insight. The predictor of renewal is self-service resolution, the share of questions answered without a ticket.'''),
            ('''How fast can a conversational analytics program deliver value?''',
             '''Pilot value, faster answers and fewer tickets, appears in weeks on a narrow domain. Broader value compounds over months as trust and the metric layer grow, so report a monthly trend rather than a launch-day number.'''),
        ],
        "excerpts": [
            '''The metrics that show whether conversational analytics is trusted, not just used.''',
            '''What a conversational BI scorecard should track to predict renewal.''',
            '''Why self-service resolution rate is the metric that funds the programme.''',
        ],
    },
    "zh": {
        "expand": [
            ("exp-1", '''对话式 BI 记分卡应包含什么？''',
             '''<p>有用的记分卡追踪采用而非仅使用：活跃提问者、每次会话的问题数，以及自助解决率（不工单即答出的占比）。加入答案质量信号：对答案的点赞、重复提问，以及该闭环真正交付的洞察时间。这些共同显示人们是否足够信任系统而依赖它。</p>
<p>预测续费的关键指标是自助解决率。若对话式 BI 不断把工单推回数据团队，它只是玩具；若产品内自行答出的问题占比持续上升，它才是基础设施。把这个趋势报给董事会，项目便凭其消灭的积压而自给自足。</p>'''),
        ],
        "faq": [
            ('''如何理解当前格局？''',
             '''格局已从仪表盘转向可对话、可查询的数据，买家如今期待由受治理指标支撑的自然语言答案。理解它意味着看清同行已把此视为基线之处。'''),
            ('''实施方法与最佳实践有哪些？''',
             '''连接语义层，从最高频的问题启动，并盯答案质量。最佳实践是窄处起步、证明信任再扩展，对任何重大事项保留人类兜底。'''),
            ('''对话式 BI 记分卡应包含什么？''',
             '''追踪活跃提问者、每次会话问题数、自助解决率、答案质量与洞察时间。预测续费的是自助解决率，即不工单即答出的问题占比。'''),
            ('''对话式分析项目多快能交付价值？''',
             '''在窄领域的试点价值（更快答案、更少工单）数周即现。更广价值随信任与指标层增长在数月内复利，因此报告月度趋势而非上线当天数字。'''),
        ],
        "excerpts": [
            '''表明对话式分析被信任而非仅被使用的指标。''',
            '''对话式 BI 记分卡为预测续费应追踪什么。''',
            '''为何自助解决率是养活项目的关键指标。''',
        ],
    },
}

AUG["conversational-bi-security-considerations"] = {
    "en": {
        "expand": [
            ("exp-1", '''Which Security Controls Are Non-Negotiable?''',
             '''<p>Start with identity and least privilege: every query runs as the asking user, scoped to what they may see, enforced at the data boundary, not in the prompt. Add row- and column-level controls, full audit of who asked what and which systems answered, and a guard that blocks exfiltration of data the user cannot normally reach. Without these, a conversational interface is just a wider front door.</p>
<p>Treat the model as untrusted at the boundary. Prompt injection is not a future risk, it is daily, so the system must validate intent against policy before any data moves, and never let the model decide access. The secure pattern is governance in the semantic layer and enforcement in the connector, so the language model orchestrates but never authorises.</p>'''),
        ],
        "faq": [
            ('''How is the landscape of natural language analytics evolving?''',
             '''It is moving from keyword search to governed conversational answers, and buyers now expect the same access controls they had on dashboards. The evolution is less about the model and more about the guardrails around it.'''),
            ('''What should the technical architecture and performance look like?''',
             '''A semantic layer for governed metrics, connectors that enforce access at the boundary, and a model that orchestrates rather than authorises. Performance comes from caching definitions and pre-agreed queries, not from re-deriving logic per question.'''),
            ('''What are the user experience and adoption patterns?''',
             '''Adoption follows trust: users adopt when answers are consistent and they can see why. Patterns that win are short loops, visible sources, and a clear path to a human when the answer is material.'''),
            ('''Which security controls are non-negotiable?''',
             '''Identity and least privilege per query, row- and column-level controls, full audit of questions and sources, and a guard against data the user cannot normally reach. The model must never decide access; policy enforced at the connector does.'''),
        ],
        "excerpts": [
            '''The security controls that are non-negotiable for conversational BI.''',
            '''Why the model should orchestrate but never authorise access.''',
            '''How governance in the semantic layer enforces security at the boundary.''',
        ],
    },
    "zh": {
        "expand": [
            ("exp-1", '''哪些安全控制不可妥协？''',
             '''<p>从身份与最小权限起步：每个查询以提问者身份运行，限定在其可见范围，并在数据边界而非提示词里强制执行。加上行级与列级控制、谁问了什么及哪些系统作答的完整审计，以及一道拦截用户通常无法触达数据外泄的闸门。没有这些，对话界面只是更宽的前门。</p>
<p>在边界处把模型视为不可信。提示注入不是未来风险而是日常，因此系统必须在数据移动前按策略校验意图，绝不让模型决定访问。安全模式是：治理在语义层、强制在连接器，语言模型只编排、不授权。</p>'''),
        ],
        "faq": [
            ('''自然语言分析的格局如何演进？''',
             '''它正从关键词搜索走向受治理的对话答案，买家如今期待与仪表盘同等的访问控制。演进重点不在模型，而在其周围的护栏。'''),
            ('''技术架构与性能应如何设计？''',
             '''用语义层承载受治理指标，用连接器在边界强制执行访问，模型只编排不授权。性能来自缓存定义与预约定查询，而非每问重新推导逻辑。'''),
            ('''用户体验与采用模式有哪些？''',
             '''采用随信任而来：答案一致且可解释时用户才用。胜出的模式是短闭环、可见来源，以及对重大答案清晰转人工的路径。'''),
            ('''哪些安全控制不可妥协？''',
             '''按查询的身份与最小权限、行级与列级控制、对问题与来源的完整审计，以及拦截用户通常无法触达数据的闸门。模型绝不能决定访问，由连接器执行的策略来决定。'''),
        ],
        "excerpts": [
            '''对话式 BI 中不可妥协的安全控制。''',
            '''为何模型应编排却绝不可授权访问。''',
            '''语义层中的治理如何在边界强制安全。''',
        ],
    },
}

AUG["the-rise-of-ai-agent-marketplaces"] = {
    "en": {
        "expand": [
            ("exp-1", '''How Do You Evaluate Marketplace Agents Before Trusting Them?''',
             '''<p>Evaluate like you would a vendor, not a plugin. Check provenance: who built it, what data it was trained on, and what it is allowed to touch. Run it in a sandbox against your own tasks, watch what it calls and what it changes, and require a human approval step for anything that writes or spends. An agent you cannot watch is an agent you cannot onboard.</p>
<p>Governance is the difference between a marketplace and a liability. Keep an agent registry, version every agent, log each action, and bind permissions to the least the task needs. With provenance and audit in place, marketplaces let a small team deploy capability that once needed a build project, and the risk stays bounded instead of hidden.</p>'''),
            ("exp-2", '''What Is the Future of Composable AI?''',
             '''<p>Composable AI means assembling capabilities from a catalogue of vetted agents instead of building monoliths. The organisation declares intent, the platform composes the agents, and governance tracks the result. This shrinks time-to-capability from quarters to days, and it turns the marketplace from a gadget store into the wiring diagram of the enterprise.</p>'''),
        ],
        "faq": [
            ('''What does an AI agent marketplace provide?''',
             '''It provides ready-made agents you can deploy for specific tasks, from research to workflow execution, without building from scratch. The value is speed and a managed catalogue, the risk is onboarding agents you have not vetted.'''),
            ('''How do you decide between build, buy, and assemble?''',
             '''Build only the logic that is your moat, buy the commodity substrate, and assemble vetted marketplace agents for the rest. Assemble wins when the task is common and a maintained agent already exists.'''),
            ('''How do you evaluate marketplace agents?''',
             '''Treat them as vendors: check provenance, training data, and permissions, sandbox them on your tasks, and require human approval for anything that writes or spends. An agent you cannot observe is one you cannot trust.'''),
            ('''Why do governance, security, and agent provenance matter?''',
             '''Because an agent acts, not just answers. Without provenance and audit, a marketplace is a liability; with a registry, versioning, and least-permission bonds, it becomes a safe way to deploy capability fast.'''),
        ],
        "excerpts": [
            '''How to evaluate and govern agents from an AI agent marketplace.''',
            '''Build, buy, or assemble: the decision that bounds marketplace risk.''',
            '''Why provenance and audit turn a marketplace into safe composable AI.''',
        ],
    },
    "zh": {
        "expand": [
            ("exp-1", '''如何在信任市场代理商前评估它们？''',
             '''<p>像评估供应商而非插件那样评估。查来源：谁构建、训练数据是什么、被允许触达什么。在沙箱里用您自己的任务跑它，观察它调用了什么、改了什么，并对任何会写入或花费的动作要求人类审批。一个您无法观察的代理，就是无法接纳的代理。</p>
<p>治理是市场与负债的分野。保留代理登记、为每个代理版本化、记录每次动作，并把权限绑定到任务所需最小集。有了来源与审计，市场让小团队部署曾需建设项目的能力，而风险受界而非隐秘。</p>'''),
            ("exp-2", '''可组合人工智能的未来如何？''',
             '''<p>可组合 AI 意味着从已审查代理目录组装能力，而非构建单体。组织声明意图，平台组合代理，治理追踪结果。这让能力交付时间从季度缩到天，并把市场从杂货铺变成企业的接线图。</p>'''),
        ],
        "faq": [
            ('''人工智能代理市场提供什么？''',
             '''它提供现成、可部署于特定任务的代理，从研究到工作流执行，无需从零构建。价值在速度与管理目录，风险在接纳未审查的代理。'''),
            ('''构建、购买、组装如何权衡？''',
             '''只自建作为护城河的逻辑，购买商品底座，其余组装已审查的市场代理。任务常见且已有受维护代理时，组装胜出。'''),
            ('''如何评估市场代理商？''',
             '''视其为供应商：查来源、训练数据与权限，在沙箱用自有任务验证，对任何写入或花费动作要求人类审批。无法观察的代理即不可信任。'''),
            ('''为何治理、安全与代理来源至关重要？''',
             '''因为代理会行动而非仅作答。没有来源与审计，市场是负债；有登记、版本化与最小权限绑定，它才成为快速部署能力的安全方式。'''),
        ],
        "excerpts": [
            '''如何评估并治理来自 AI 代理市场的代理。''',
            '''构建、购买或组装：界定市场风险的决策。''',
            '''为何来源与审计把市场变成安全的可组合 AI。''',
        ],
    },
}

AUG["mcp-multi-cloud-integration-2025-dec"] = {
    "en": {
        "expand": [
            ("exp-1", '''What Does MCP Change About Cross-Cloud Data Access?''',
             '''<p>MCP gives every AI client a standard way to reach a data source, so the same agent can query across clouds without a bespoke integration per connection. Access control stays at the source boundary, and each call is logged. That turns multi-cloud from an integration project into a configuration, and it lets conversational analytics sit on top of data that never leaves its region.</p>
<p>The ROI is in removed glue and regained trust. Teams stop maintaining fragile connectors and start asking questions across clouds in one chat. Because policy is enforced where the data lives, compliance and latency both improve, and a single audit view replaces a maze of point-to-point links.</p>'''),
        ],
        "faq": [
            ('''What is the 2025 state of multi-cloud integration?''',
             '''Most enterprises run several clouds but stitch them with fragile point-to-point links. In 2025 the pressure is to query across them in one place without copying data, and standards like MCP are what make that practical.'''),
            ('''What does MCP change about cross-cloud data access?''',
             '''MCP gives every AI client a standard way to reach a source, so one agent queries across clouds without per-connection code. Access control stays at the boundary and every call is logged, turning integration into configuration.'''),
            ('''What are the key benefits and ROI considerations?''',
             '''Benefits are fewer bespoke connectors, policy enforced at the source, and one audit view. ROI comes from removed maintenance glue and the ability to ask across clouds in a single conversational surface.'''),
            ('''How does Beehive Strategy connect your clouds in chat?''',
             '''Our MCP-based layer connects AI to each cloud through governed connectors, so your team asks in natural language and gets answers from live data in place, with access and audit handled at the boundary.'''),
        ],
        "excerpts": [
            '''How MCP turns multi-cloud integration from a project into configuration.''',
            '''Why cross-cloud access control belongs at the source boundary.''',
            '''The ROI of querying every cloud from one conversational surface.''',
        ],
    },
    "zh": {
        "expand": [
            ("exp-1", '''MCP 如何改变跨云数据访问？''',
             '''<p>MCP 给每个 AI 客户端一条触达数据源的标准路径，于是同一代理能跨云查询，无需为每个连接写定制集成。访问控制留在源头边界，每次调用都有日志。这让多云从集成项目变成配置，并让对话式分析架在从不离开本区域的数据之上。</p>
<p>投资回报在于移除胶水代码与重获信任。团队不再维护脆弱连接器，而能在一次对话里跨云提问。由于策略在数据所在处强制执行，合规与延迟同时改善，单一审计视图取代了点对点链接的迷宫。</p>'''),
        ],
        "faq": [
            ('''2025 年多云集成处于什么状态？''',
             '''多数企业运行多个云，却用脆弱的点对点链接拼接。2025 年的压力是在不复制数据的前提下于一处跨云查询，而 MCP 这类标准使之可行。'''),
            ('''MCP 如何改变跨云数据访问？''',
             '''MCP 给每个 AI 客户端一条触达源的标准路径，于是同一代理能跨云查询而无需逐连接的代码。访问控制留在边界、每次调用有日志，把集成变成配置。'''),
            ('''核心收益与投资回报考量有哪些？''',
             '''收益是更少的定制连接器、在源头强制的策略，以及单一审计视图。ROI 来自移除维护胶水，以及能在同一对话界面跨云提问的能力。'''),
            ('''蜂启咨询如何把您的云连进对话？''',
             '''我们基于 MCP 的层通过受治理连接器把 AI 连到每个云，团队用自然语言提问，便从就地实时数据得到答案，访问与审计都在边界处理。'''),
        ],
        "excerpts": [
            '''MCP 如何把多云集成从项目变成配置。''',
            '''为何跨云访问控制应归属源头边界。''',
            '''从单一对话界面查询每个云的投资回报。''',
        ],
    },
}
