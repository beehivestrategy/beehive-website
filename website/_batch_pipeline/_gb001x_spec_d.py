# -*- coding: utf-8 -*-
"""Content specs for gbatch_001 slugs 12-15."""

SPECS = {}

# -------------------------------------------------------------------------- 12
SPECS["predictive-maintenance-ai-roi-20260116"] = {
    "EN": {
        "rename": {
            "understanding-the-current-landscape":
                "What Is the Current State of AI Predictive Maintenance?",
            "key-principles-and-strategic-framework":
                "What Principles Should Guide a Predictive Maintenance Programme?",
            "implementation-approach-and-best-practices":
                "How Should You Implement Predictive Maintenance?",
            "measuring-success-and-demonstrating-roi":
                "How Do You Measure Predictive Maintenance ROI?",
            "common-pitfalls-and-how-to-avoid-them":
                "What Are the Most Common Predictive Maintenance Pitfalls?",
            "key-takeaways": "What Are the Key Takeaways?",
            "conclusion": "Where Should You Start?",
        },
        "new": [
            ("which-failure-modes-are-actually-predictable",
             "Which Failure Modes Are Actually Predictable?",
             ["<p>The single biggest determinant of predictive maintenance ROI is whether the failure "
              "mode you pick is predictable at all, and this is decided by physics before it is decided "
              "by data science. Failures that develop gradually and emit a signal — bearing wear, "
              "insulation degradation, seal leakage, filter clogging, tool wear — are predictable. "
              "Failures that arrive without a precursor — a forklift strike, a power surge, a "
              "software fault, an operator error — are not, no matter how much sensor data you "
              "collect.</p>",
              "<p>The practical test is to look at the historical record for each failure mode and ask "
              "whether the condition of the asset was measurably different in the weeks before failure. "
              "If the answer is no for a given mode, a model will find nothing, and the honest "
              "conclusion is to exclude it and address it through spares policy or design change instead. "
              "Programmes that skip this step spend a year learning the same lesson expensively.</p>",
              "<p>A second filter is frequency and consequence. The best early targets sit in a specific "
              "quadrant: frequent enough to generate training examples, and expensive enough that "
              "avoiding one instance pays for the work. Rare catastrophic failures are the ones "
              "executives ask for first and the ones with the least data; starting there usually "
              "produces a model that cannot be validated.</p>",
              "<p>A useful way to structure the first pass is a ranked table of failure modes with three "
              "columns — annual frequency, average consequence in downtime and repair cost, and whether "
              "a precursor signal exists in the data you already hold. Most organisations find two or "
              "three modes that are obviously worth attacking, and a long tail that is not. That ranking "
              "is the business case.</p>"]),
            ("how-much-history-do-you-need-before-a-model-is-credible",
             "How Much History Do You Need Before a Model Is Credible?",
             ["<p>The question is asked constantly and usually answered with a number — twelve months, "
              "eighteen months — that turns out to be almost meaningless without two qualifications. "
              "What matters is not calendar time but failure events, and not data volume but label "
              "quality.</p>",
              "<p>Supervised models need enough positive examples to learn from and enough to validate "
              "on. As a working rule, thirty to fifty well-labelled failure events for a given mode is "
              "the point at which a model becomes evaluable, and a hundred is where it becomes reliable. "
              "If a failure occurs four times a year, that is twenty-five years of calendar history, "
              "which is not available — so the mode needs a different approach, typically an "
              "unsupervised anomaly-detection model or a physics-based threshold rather than a "
              "classifier.</p>",
              "<p>Label quality is the harder constraint. Maintenance records are written for finance "
              "and compliance, not for modelling, so the failure timestamp is often the date the work "
              "order closed rather than the date the degradation began, and the cause code is frequently "
              "the default value. Investing a few weeks with a maintenance engineer to reconstruct "
              "accurate labels for the top failure modes typically improves model performance more than "
              "any amount of algorithm tuning.</p>",
              "<p>Where labels are thin, start with unsupervised methods and treat them as a triage tool "
              "rather than a prediction. Ranking assets by anomaly score gives technicians a shorter "
              "inspection list, which produces better labels, which eventually supports a supervised "
              "model. That bootstrap path is slower and far more reliable than training a classifier on "
              "codes nobody trusts.</p>"]),
            ("how-do-you-turn-a-prediction-into-a-work-order",
             "How Do You Turn a Prediction Into a Work Order?",
             ["<p>More predictive maintenance programmes fail at integration than at modelling. A "
              "prediction that appears in a dashboard nobody checks during a shift produces no value, "
              "and a prediction that generates alerts without context produces alarm fatigue within "
              "weeks. The last mile — getting the right instruction to the right technician at the "
              "right time, inside the system they already use — is where the return is actually "
              "realised.</p>",
              "<p>Three design decisions matter. Where the alert lands: it has to be in the CMMS or the "
              "mobility tool the technician already works in, not in a separate analytics portal. What "
              "the alert says: the specific component, the evidence behind the score, the recommended "
              "action, the parts required, and the consequence of deferring — not a probability alone. "
              "And what happens if nobody acts: alerts that silently expire teach the organisation that "
              "the system can be ignored.</p>",
              "<p>Threshold setting deserves real attention because it is a business decision "
              "disguised as a technical one. Every model trades false positives against missed failures, "
              "and the right operating point depends on the cost of each. A forged part where an "
              "unplanned stop costs six figures an hour justifies a high false-positive rate; a "
              "low-consequence component does not. Set the threshold with maintenance and operations in "
              "the room, and revisit it quarterly as precision data accumulates.</p>",
              "<p>Finally, close the feedback loop. Whether the technician found anything, what they "
              "found, and what they did should be captured in the same workflow. That feedback is the "
              "label source for the next model version, it is how precision improves over time, and it "
              "is the evidence that turns a pilot into a funded programme.</p>"]),
            ("what-does-a-credible-predictive-maintenance-business-case-look-like",
             "What Does a Credible Predictive Maintenance Business Case Look Like?",
             ["<p>Predictive maintenance business cases are routinely inflated, which is why so many of "
              "them are quietly shelved after the first year when the numbers do not appear. A credible "
              "case is narrower and more conservative than the vendor template, and it is built from "
              "four separately defensible benefit lines rather than one large number.</p>",
              "<p>Avoided downtime is the largest and the most overstated. The correct calculation is "
              "not the full cost of an unplanned stop times the number of predictions; it is the "
              "avoided portion — the difference between the cost of a planned intervention and the cost "
              "of the failure, multiplied by the number of failures actually prevented, discounted by "
              "the model's measured precision. Claiming all downtime cost assumes perfect prediction and "
              "immediate perfect action, neither of which happens.</p>",
              "<p>The other three lines are usually understated and more reliable. Maintenance "
              "efficiency: fewer routine inspections and less emergency call-out overtime. Spares "
              "optimisation: lower safety stock carried against failures you can now anticipate, and "
              "better timing on long-lead items. And asset life extension: catching degradation early "
              "converts a component replacement into a repair, and avoids the collateral damage that a "
              "catastrophic failure causes to adjacent components.</p>",
              "<p>Show the model's own numbers honestly — precision, recall, and lead time — and "
              "translate lead time into money, because lead time is what determines whether a prediction "
              "is actionable at all. A warning with two hours of lead time on an asset that takes eight "
              "hours to shut down safely is not a benefit. Then phase the case: a pilot with a measured "
              "baseline, a scale-up tied to achieved precision, and only then a fleet-wide "
              "projection.</p>"]),
        ],
    },
    "zh-CN": {
        "rename": {
            "理解当前格局": "AI 预测性维护的现状如何？",
            "关键原则与战略框架": "预测性维护项目应遵循哪些原则？",
            "实施方法与最佳实践": "应如何实施预测性维护？",
            "衡量成功与展示投资回报率": "如何衡量预测性维护的投资回报？",
            "常见陷阱及规避方法": "最常见的预测性维护陷阱有哪些？",
            "关键要点": "关键要点是什么？",
            "结论": "应从哪里开始？",
        },
        "new": [
            ("哪些失效模式真的可预测",
             "哪些失效模式真的可预测？",
             ["<p>决定预测性维护投资回报的首要因素，是你选的失效模式到底可不可预测——这由物理规律决定，而非由数据科学决定。渐进发展并会发出信号的失效是可预测的：轴承磨损、绝缘劣化、密封渗漏、滤芯堵塞、刀具磨损。没有前兆就到来的失效则不可预测：叉车撞击、电涌、软件故障、人为误操作——无论你采集多少传感器数据都不行。</p>",
              "<p>实用的检验方法是回看每一类失效的历史记录，问一问：失效前数周，资产的状态在数据中是否可测地不同？若某类失效的答案为否，模型什么也学不到，诚实的结论是把它排除，改用备件策略或设计变更来应对。跳过这一步的项目，会用一年时间昂贵地学到同一个教训。</p>",
              "<p>第二个筛选维度是频次与后果。最佳早期目标落在特定象限内：频次高到足以产生训练样本，后果重到避免一次就能收回投入。罕见的灾难性失效，恰恰是高管最先提出、而数据最少的那类；从那里起步，通常只能得到一个无法验证的模型。</p>",
              "<p>组织首轮筛选的有效方式，是做一张按三列排序的失效模式表——年发生频次、以停机与维修成本计的平均后果、以及你已有的数据中是否存在前兆信号。多数组织会找出两三个明显值得攻的模式，以及一条不值得的长尾。这张排序表本身就是商业论证。</p>"]),
            ("模型可信需要多少历史数据",
             "模型可信需要多少历史数据？",
             ["<p>这个问题被反复提出，通常得到一个数字——十二个月、十八个月——但在缺少两项限定条件时，这个数字几乎没有意义。关键不是日历时间而是失效事件数，不是数据量而是标签质量。</p>",
              "<p>有监督模型需要足够的正样本来学习、也需要足够的样本来验证。一条经验法则是：某类失效有 30 到 50 个标注良好的事件时，模型才可被评估；到 100 个才可靠。若某类失效一年只发生四次，那就需要二十五年的日历历史——这不可得——因此该类失效需要换方法，通常用无监督异常检测或基于物理的阈值，而非分类器。</p>",
              "<p>标签质量是更硬的约束。维修记录是为财务与合规而写的，不是为建模而写的：失效时间戳往往是工单关闭日而非劣化起始日，原因代码常常是默认值。花几周时间与维修工程师一起，为最主要的失效模式还原准确标签，通常比任何算法调优都更能提升模型表现。</p>",
              "<p>标签稀疏时，先用无监督方法，并把它当作分诊工具而非预测工具。按异常分数给资产排序，让技师拿到更短的检查清单，从而产生更好的标签，最终支撑有监督模型。这条自举路径更慢，却远比在无人信任的代码上训练分类器可靠。</p>"]),
            ("如何把预测变成工单",
             "如何把预测变成工单？",
             ["<p>预测性维护项目在集成环节失败的多于在建模环节失败的。一个出现在班次中无人查看的看板上的预测不产生价值；一个没有上下文、只会产生告警的预测，几周内就会造成告警疲劳。最后一公里——把正确的指令、在正确的时机、送达正确的技师、且进入他们已经在用的系统——才是回报真正兑现的地方。</p>",
              "<p>三个设计决策很关键。告警落在哪里：必须落在技师已在使用的 CMMS 或移动工具里，而不是另一个分析门户。告警说什么：具体部件、分数背后的证据、建议动作、所需备件，以及推迟的后果——而不只是一个概率。以及无人处理时会怎样：静默过期的告警，会教会组织这套系统可以被忽略。</p>",
              "<p>阈值设定需要真正重视，因为它是伪装成技术决策的业务决策。每个模型都在假阳性与漏检之间取舍，正确的运行点取决于两者的成本。非计划停机每小时造成六位数损失的关键部件，值得承受较高的假阳性率；低后果部件则不值得。阈值应与维修和运营部门一起在会议室里设定，并随precision数据积累按季度复评。</p>",
              "<p>最后，闭合反馈回路。技师是否发现问题、发现了什么、做了什么，都应在同一工作流中被采集。这份反馈是下一版模型的标签来源，是precision随时间提升的途径，也是把试点变成有资金支持的项目的证据。</p>"]),
            ("可信的预测性维护商业论证长什么样",
             "可信的预测性维护商业论证长什么样？",
             ["<p>预测性维护的商业论证普遍被夸大，这正是许多项目在第一年数字未兑现后被悄悄搁置的原因。可信的论证比厂商模板更窄、更保守，并且由四条可分别辩护的收益线构成，而非一个大数字。</p>",
              "<p>避免的停机是最大也最被高估的一条。正确的计算不是非计划停机的全部成本乘以预测次数，而是被避免的那一部分——计划性干预成本与失效成本之差，乘以实际被阻止的失效次数，再按模型实测precision打折。主张全部停机成本，等于假设预测完美且行动即时完美，而两者都不会发生。</p>",
              "<p>另外三条通常被低估，却更可靠。维修效率：减少例行巡检与紧急加班。备件优化：因可预见失效而降低的安全库存，以及长周期物料更好的下单时机。资产寿命延长：早期发现劣化，把更换部件变成修理，并避免灾难性失效对相邻部件的附带损伤。</p>",
              "<p>如实呈现模型自身的数字——precision、recall与提前量——并把提前量折算成金额，因为提前量决定了预测到底是否可执行。对一个安全停机需要八小时的资产，两小时提前量的告警不是收益。然后把论证分阶段：先做有实测基线的试点，再把规模化与实际达到的precision挂钩，最后才做全车队的外推。</p>"]),
        ],
    },
}

# -------------------------------------------------------------------------- 13
SPECS["ai-roi-real-world-enterprise-case-studies-apr"] = {
    "EN": {
        "rename": {
            "the-strategic-imperative-for-enterprise-ai-in-2025":
                "Why Has Enterprise AI Become a Strategic Imperative?",
            "framework-for-ai-strategy-development":
                "What Framework Should You Use to Build an AI Strategy?",
            "measuring-success-and-demonstrating-roi":
                "How Do You Measure AI ROI Honestly?",
            "implementation-roadmap-and-key-success-factors":
                "What Does an Implementation Roadmap Actually Look Like?",
        },
        "new": [
            ("why-do-most-ai-business-cases-fail-finance-review",
             "Why Do Most AI Business Cases Fail Finance Review?",
             ["<p>AI business cases are rejected by finance for reasons that have little to do with "
              "scepticism about the technology. They fail because the arithmetic does not survive "
              "scrutiny, and the three failure modes are consistent enough to anticipate and "
              "avoid.</p>",
              "<p>The first is gross rather than net benefit. A case built on time saved — an analyst "
              "saves four hours a week, multiplied by headcount and loaded cost — assumes that saved "
              "time converts to cash. It usually converts to more analysis, which may be valuable but is "
              "not a cost reduction. Finance will ask what headcount or contractor spend actually "
              "reduces, and if the answer is nothing, the benefit should be presented as capacity "
              "created and valued accordingly, not as savings.</p>",
              "<p>The second is an uncosted denominator. Cases routinely include the licence and the "
              "implementation partner while omitting internal engineering time, data preparation, "
              "ongoing evaluation, change management, and the run cost of inference at scale. Inference "
              "cost in particular grows with adoption, so a case that looks sound at pilot volumes can "
              "invert at enterprise volumes.</p>",
              "<p>The third is an unattributable baseline. &quot;Improve forecast accuracy by 15 "
              "percent&quot; is not a benefit until someone states today's accuracy, the decisions that "
              "depend on it, and the value of those decisions improving. Without the baseline and the "
              "attribution chain, the number is unfalsifiable, and finance will treat it as such.</p>",
              "<p>The cases that pass have three properties: a named baseline measured before launch, a "
              "benefit that maps to a line in the P&L or to a documented cost avoidance, and a "
              "phasing where later tranches are contingent on earlier ones delivering. That last "
              "property is the most persuasive of all, because it converts an act of faith into a "
              "staged commitment.</p>"]),
            ("what-do-the-successful-deployments-have-in-common",
             "What Do the Successful Deployments Have in Common?",
             ["<p>Across the deployments that reached production and stayed there, the common factor is "
              "almost never the model. It is the sequence in which the work was done, and specifically "
              "that the unglamorous infrastructure came before the visible capability.</p>",
              "<p>Every one of them had a semantic layer or its equivalent — a governed, agreed set of "
              "business definitions — in place before the interface was exposed to users. This is the "
              "single strongest predictor of whether a deployment survives contact with real questions, "
              "because it is what makes an answer attributable to a definition. The deployments that "
              "skipped it produced fluent answers to ambiguous questions and lost credibility within "
              "weeks.</p>",
              "<p>They also shared a narrow start. Rather than launching enterprise-wide, each began "
              "with one function, one decision domain, and a small enough set of metrics that owners "
              "could genuinely certify them. Coverage expanded from a position of demonstrated "
              "reliability rather than from a launch announcement. The pattern is counter-intuitive to "
              "sponsors who want breadth, but the programmes that launched broadly are the ones now "
              "running remediation projects.</p>",
              "<p>Third, they invested in evaluation infrastructure early — a set of representative "
              "questions with known-correct answers, run on every change. This is what allowed them to "
              "upgrade models and refactor prompts without regressing, and it is why their improvement "
              "curves are monotonic rather than sawtoothed.</p>",
              "<p>Finally, they had an executive sponsor who used the system. Not one who funded it and "
              "read the status reports, but one who asked it questions in meetings. That single "
              "behaviour does more for adoption than any training programme, because it makes the "
              "capability visible and the expectation of using it explicit.</p>"]),
            ("how-long-does-it-take-to-see-return",
             "How Long Does It Take to See Return?",
             ["<p>The honest answer has two parts, and conflating them is why so many programmes are "
              "judged prematurely. Quick wins arrive in the first quarter; durable return arrives in the "
              "second year; and the shape of the curve in between is what determines whether the "
              "programme survives to collect it.</p>",
              "<p>First-quarter returns come from automation of well-defined, high-volume tasks: "
              "report generation, first-pass analysis, data quality triage, routine reconciliation. "
              "These are real but bounded, and they are best used to fund the next phase and to build "
              "credibility rather than to claim victory.</p>",
              "<p>The second-year return is larger and comes from a different mechanism: decision "
              "latency. Once questions are answered in minutes rather than days, the number of questions "
              "asked rises sharply, and decisions that previously proceeded on stale or partial "
              "information start proceeding on current information. This is difficult to attribute "
              "line-by-line, which is why programmes that only measure the first-quarter benefits tend "
              "to under-report their own value.</p>",
              "<p>The valley between the two is the risk period. Months four to nine typically show "
              "rising usage with flat measured benefit, because the semantic layer is being extended and "
              "the easy automation has already been captured. Programmes are often cut here. The "
              "defence is to have measured and agreed the leading indicators in advance — question "
              "volume, time-to-answer, adoption breadth, and semantic-layer coverage — and to report "
              "them alongside the lagging financial metrics, so that the curve is legible before the "
              "payoff lands.</p>"]),
        ],
    },
    "zh-CN": {
        "rename": {
                                    "衡量成功与展示投资回报": "如何诚实地衡量 AI 投资回报？",
            "实施路径与组织准备": "实施路径与组织准备应包含什么？",
            "战略实施路径与关键成功因素": "战略实施的关键成功因素是什么？",
            "战略实施路径与关键成功因素-2": "规模化阶段的关键成功因素是什么？",
            "企业实施路线图与成功因素": "企业实施路线图应如何设计？",
            "行业数字化转型深度分析": "行业数字化转型有哪些深层驱动力？",
        },
        "rename_text": {
            "2025年企业AI的战略紧迫性": "为什么企业 AI 已成为战略必选项？",
            "AI战略开发框架": "构建 AI 战略应采用什么框架？",
        },
    },
}

# -------------------------------------------------------------------------- 14
SPECS["data-privacy-compliance-audits-ai-systems"] = {
    "EN": {
        "rename": {
            "the-data-governance-imperative-for-ai":
                "Why Does AI Make Data Governance Non-Optional?",
            "framework-design-and-implementation":
                "How Should You Design an AI Privacy Audit Framework?",
            "operational-challenges-and-solutions":
                "What Are the Operational Challenges and How Do You Solve Them?",
            "measurement-and-continuous-improvement":
                "How Do You Measure a Privacy Programme?",
            "building-a-sustainable-governance-model":
                "How Do You Build a Sustainable Governance Model?",
            "key-takeaways": "What Are the Key Takeaways?",
            "conclusion": "Where Should You Start?",
        },
        "new": [
            ("what-is-different-about-auditing-an-ai-system",
             "What Is Different About Auditing an AI System?",
             ["<p>Privacy auditing was built for systems with a determinate data flow: you identify the "
              "collection point, the purpose, the recipients, and the retention period, and you verify "
              "each against the record. AI systems break each of those assumptions in ways that require "
              "a different method rather than a longer checklist.</p>",
              "<p>Purpose limitation is the first to go. A model trained on data collected for one "
              "purpose encodes that data in weights that serve any downstream purpose, and the original "
              "purpose limitation does not travel with it. Auditing therefore has to trace not just "
              "where data went but what the model can now do as a result, which is a materially harder "
              "question.</p>",
              "<p>Minimisation is the second. Standard practice is to collect only what a defined "
              "process needs. Machine learning inverts the logic: the value of a dataset often comes "
              "from fields whose relevance is discovered later. Auditors need to assess whether the "
              "organisation has a defensible process for deciding what goes into training, not just "
              "whether the collection was minimal at the time.</p>",
              "<p>Deletion and rectification are the third, and the hardest. Deleting a record from a "
              "source system does not remove its influence from a trained model, and in most cases there "
              "is no practical way to remove it short of retraining. An audit has to establish what the "
              "organisation actually does when an erasure request arrives, verify that it matches the "
              "published policy, and flag the gap if the policy promises more than the architecture can "
              "deliver. That gap is common and it is a finding worth writing down rather than "
              "smoothing over.</p>"]),
            ("how-do-you-test-whether-training-data-was-lawfully-obtained",
             "How Do You Test Whether Training Data Was Lawfully Obtained?",
             ["<p>Provenance testing is the core of an AI privacy audit, and it is more tractable than "
              "it first appears if you approach it as sampling rather than exhaustive verification. "
              "The question is not whether every record is lawful but whether the organisation has a "
              "system that makes unlawful inclusion unlikely and detectable.</p>",
              "<p>Start with the register. There should be a dataset inventory covering every corpus "
              "used for training, fine-tuning, evaluation, and retrieval, with source, acquisition date, "
              "licence or contract reference, lawful basis, and a named owner. Audit the register for "
              "completeness first — compare it against the data sources referenced in training code, "
              "pipeline configuration, and feature stores, because undocumented corpora are the most "
              "common finding.</p>",
              "<p>Then sample. Select datasets by risk: web-scraped content, third-party purchased "
              "data, user-generated content, and anything containing special-category or children's "
              "data. For each, trace the lawful basis to a document — a contract clause, a consent "
              "record, a licence, a legitimate-interest assessment. A lawful basis that cannot be "
              "produced is a finding regardless of whether one existed.</p>",
              "<p>Finally test the controls that should prevent recurrence: is there a review gate "
              "before a new corpus enters training, does the gate have a documented checklist, and is "
              "there logging that would show if it were bypassed. Auditing the control rather than only "
              "the outcome is what distinguishes a useful audit from a one-off inspection.</p>"]),
            ("what-evidence-should-an-audit-produce",
             "What Evidence Should an AI Privacy Audit Produce?",
             ["<p>The output of an audit matters as much as its method, because the artefact is what "
              "survives staff turnover, satisfies a regulator, and lets the next audit start from the "
              "previous one's position rather than from zero.</p>",
              "<p>Four artefacts cover it. A scope statement recording the model versions, data "
              "snapshots, and systems in scope, with the date — without this, findings cannot be "
              "reproduced or tracked. A findings register with each finding rated by severity, mapped to "
              "the specific obligation breached, and assigned an owner and a remediation date; "
              "unowned findings do not get fixed. Evidence attachments for each finding: the query run, "
              "the configuration reviewed, the document examined, sufficient that a reviewer could "
              "reproduce the conclusion independently.</p>",
              "<p>Then a remediation plan with dates and a re-test schedule, and a management summary "
              "written for a reader who will not read the rest. The summary should state the overall "
              "opinion plainly — whether the system is fit to operate in its current use case, "
              "subject to what conditions — because that is the sentence anyone senior will actually "
              "read.</p>",
              "<p>Two practices make these artefacts durable. Version the audit alongside the system it "
              "covers, so that a model release without a corresponding audit update is visible. And "
              "retain the evidence in a store whose access is controlled and logged, because audit files "
              "themselves contain sensitive information about where the organisation is exposed.</p>"]),
        ],
        "faq": [
            ("How often should an AI system be privacy-audited?",
             "At minimum annually, plus on any material change: a new training data source, a change of "
             "model provider, a new use case, or a change in the jurisdictions where the system is "
             "offered. High-risk systems affecting credit, health, employment, or children should be "
             "audited more frequently, typically quarterly for the first year after launch."),
            ("Can you audit a model you did not build?",
             "Yes, but the method shifts from inspection to contractual and documentary review. You "
             "audit what the vendor will evidence: the data provenance statements, the sub-processor "
             "list, the retention and deletion commitments, the evaluation results, and the security "
             "certifications. Where a vendor cannot evidence a claim, record it as an unmitigated risk "
             "rather than accepting it."),
            ("Does deleting source data remove it from a trained model?",
             "Usually not. Model weights encode statistical influence from training records, and there "
             "is no reliable way to remove a single record's contribution without retraining. Systems "
             "should therefore document what they actually do on an erasure request, and the published "
             "policy should match that behaviour rather than promising more than the architecture "
             "delivers."),
            ("What is the most common finding in AI privacy audits?",
             "Undocumented data. Training, evaluation, and retrieval corpora that entered the system "
             "without passing a review gate and do not appear in the dataset register — typically added "
             "during a proof of concept and never removed or recorded."),
        ],
    },
    "zh-CN": {
        "rename": {
                        "框架设计与实施": "AI 隐私审计框架应如何设计？",
            "运营挑战与解决方案": "运营挑战有哪些，如何解决？",
            "衡量与持续改进": "隐私项目应如何衡量？",
            "构建可持续的治理模式": "如何构建可持续的治理模式？",
        },
        "rename_text": {
            "AI时代的数据治理迫切性": "为什么 AI 让数据治理不再可选？",
        },
        "faq": [
            ("AI 系统应多久做一次隐私审计？",
             "至少每年一次；并在发生任何实质变更时追加：新增训练数据源、更换模型供应商、新增用例，或系统投放的司法辖区发生变化。影响信贷、健康、就业或儿童的高风险系统应更频繁，通常上线后第一年按季度审计。"),
            ("非自研的模型可以审计吗？",
             "可以，但方法从检查转为合同与文档审阅。审计厂商能够提供证据的部分：数据来源声明、次级处理者清单、留存与删除承诺、评估结果与安全认证。厂商无法提供证据的主张，应记为未缓释风险，而不是予以接受。"),
            ("删除源数据能否把它从已训练的模型中移除？",
             "通常不能。模型权重编码了训练记录的统计影响，没有可靠方法能在不重新训练的情况下移除单条记录的贡献。因此系统应如实记录它在收到删除请求时实际做了什么，且对外政策应与该行为一致，而非承诺架构无法交付的结果。"),
            ("AI 隐私审计中最常见的发现是什么？",
             "未登记的数据。未经评审关卡就进入系统、且未出现在数据集台账中的训练、评估与检索语料——通常在概念验证阶段加入，之后再未移除或记录。"),
        ],
    },
}

# -------------------------------------------------------------------------- 15
SPECS["financial-services-ai-compliance-innovation"] = {
    "EN": {
        "rename": {
            "the-regulatory-landscape-for-ai-in-financial-services":
                "What Does the AI Regulatory Landscape Look Like in Financial Services?",
            "mcp-architecture-for-regulated-ai-deployment":
                "How Does MCP Architecture Support Regulated AI Deployment?",
            "ai-for-compliance-turning-the-paradox-inside-out":
                "How Can AI Serve Compliance Rather Than Only Complicate It?",
            "strategic-roadmap-for-financial-services-leaders":
                "What Should a Financial Services AI Roadmap Look Like?",
        },
        "new": [
            ("what-does-model-risk-management-require-of-generative-ai",
             "What Does Model Risk Management Require of Generative AI?",
             ["<p>Model risk management frameworks in financial services were built for statistical "
              "models with fixed inputs, stable behaviour, and a tractable validation surface. "
              "Generative models violate all three, and the resulting gap is the main reason regulated "
              "institutions stall between pilot and production.</p>",
              "<p>The first requirement that needs rethinking is validation. Traditional validation "
              "verifies that a model does what its documentation says on a held-out dataset. A "
              "foundation model's behaviour is contingent on prompts, retrieved context, and "
              "configuration, so the unit of validation is not the model but the system: prompt, "
              "retrieval, tools, guardrails, and the model together. Documentation has to describe that "
              "assembly, and validation has to test it end to end against a curated set of cases.</p>",
              "<p>The second is change management. A prompt edit or a tool description change can alter "
              "system behaviour as much as a retraining would, and under most frameworks it is a change "
              "requiring the same discipline: versioning, testing, approval, and a rollback path. "
              "Treating prompt changes as configuration tweaks is the most common control gap we see in "
              "institutions that have otherwise adapted their frameworks well.</p>",
              "<p>The third is explainability, and it needs to be reframed rather than solved. You "
              "cannot explain a foundation model's reasoning the way you can explain a logistic "
              "regression's coefficients, but you can explain the system: which context was retrieved, "
              "which tools were invoked with which arguments, which policy permitted them, and which "
              "definition produced the number. That trace is what a reviewer or regulator needs to "
              "reconstruct a decision, and it is achievable with architecture rather than with "
              "interpretability research.</p>"]),
            ("how-do-you-keep-customer-data-out-of-a-model-safely",
             "How Do You Keep Customer Data Out of a Model Safely?",
             ["<p>Financial institutions have a hard constraint that most industries do not: personal "
              "and confidential data generally cannot be sent to an external model endpoint without "
              "extensive documentation, and in many cases cannot be sent at all. That constraint is "
              "manageable, but it rules out the default integration pattern and forces a specific "
              "architecture.</p>",
              "<p>Three patterns cover most cases, in increasing order of data sensitivity. "
              "Redaction before transmission: detect and replace identifiers in the prompt, so the model "
              "reasons over structure rather than over real values. This works for drafting and "
              "summarisation tasks where the content matters more than the identities. Self-hosted or "
              "VPC-deployed models, where the endpoint is inside the institution's boundary and no data "
              "crosses to a third party — this is the pattern that unblocks the widest range of use "
              "cases and is where most institutions land for anything touching customer data.</p>",
              "<p>The third pattern is the one that preserves the most analytical value: never send the "
              "data, send the question and the schema, and let the model generate a query that runs "
              "inside the boundary. This is the conversational BI pattern, and it is why a governed "
              "interface such as an MCP server matters more in financial services than elsewhere — the "
              "model sees metadata and aggregate results rather than raw records, and every access is "
              "authorised and logged by the existing data platform.</p>",
              "<p>Whichever pattern applies, verify rather than assume. Test the deployment with "
              "canary records that should never leave, and monitor egress continuously. Configuration "
              "drift in a model integration is silent, and a periodic test is the only way to detect "
              "it.</p>"]),
            ("where-does-ai-actually-reduce-compliance-cost",
             "Where Does AI Actually Reduce Compliance Cost?",
             ["<p>The paradox of AI in regulated institutions is that every deployment adds a compliance "
              "obligation while AI is simultaneously the most credible tool for reducing compliance "
              "cost. Both are true, and the second is underexploited because the use cases are less "
              "visible than customer-facing ones.</p>",
              "<p>The largest and most reliable saving is evidence production. Regulatory reporting, "
              "audit responses, and due-diligence questionnaires consume enormous analyst hours "
              "reconstructing information the institution already holds. Retrieval over a governed "
              "corpus, with answers citing the source document and the as-of date, turns a two-week "
              "response into a day, and it produces a better audit trail than the manual process "
              "did.</p>",
              "<p>The second is control monitoring. Transaction monitoring, communications "
              "surveillance, and conduct risk review are all processes where a human reviews a large "
              "volume to find a small number of exceptions. Models are very good at the triage step — "
              "ranking the queue so reviewers spend their time on the genuinely ambiguous cases — and "
              "the saving is in analyst hours per alert rather than in alerts eliminated.</p>",
              "<p>The third is policy and regulatory change management. Mapping a new rule to the "
              "institutions' affected systems, policies, and controls is a retrieval and matching "
              "problem, and it is one where AI-assisted drafting with human sign-off is both faster and "
              "more consistent than the manual equivalent.</p>",
              "<p>In each case the control requirement does not disappear: a human still owns the "
              "output, the system still needs validation, and the trace still needs to be retained. The "
              "saving is in the cost of producing the evidence, not in the obligation to produce "
              "it.</p>"]),
        ],
    },
    "zh-CN": {
        "rename": {
            "规模化推广的关键成功因素": "规模化推广的关键成功因素是什么？",
            "技术基础设施与实施考量": "技术基础设施需要哪些实施考量？",
            "中国市场特有的实施优势": "中国市场有哪些特有的实施优势？",
            "规模化推广的关键成功因素-2": "第二阶段推广的关键成功因素是什么？",
        },
        "rename_text": {
            "MCP Architecture for Regulated AI Deployment": "MCP 架构如何支撑受监管的 AI 部署？",
            "AI for Compliance: Turning the Paradox Inside Out":
                "AI 如何服务合规，而不只是增加合规负担？",
            "Strategic Roadmap for Financial Services Leaders":
                "金融服务领导者的战略路线图应如何设计？",
        },
    },
}
