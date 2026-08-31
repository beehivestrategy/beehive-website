# -*- coding: utf-8 -*-
"""Top-up specs: one extra section per file still below the length floor."""

SPECS = {}

SPECS["predictions-enterprise-data-analytics-2026"] = {
    "EN": {"new": [
        ("how-do-you-tell-a-real-trend-from-a-vendor-narrative",
         "How Do You Tell a Real Trend From a Vendor Narrative?",
         ["<p>Prediction season produces a lot of confident claims, and the useful skill is not "
          "forecasting but discriminating. Four tests separate a trend that will shape your 2026 "
          "planning from one that will not, and they are cheap to apply.</p>",
          "<p>The first test is whether anyone is paying for it with their own budget. Adoption "
          "claims from vendor surveys measure intent; purchase orders measure commitment. Ask what "
          "share of the vendor's revenue comes from the capability being predicted, and whether that "
          "share is growing faster than the rest of the business. A prediction that is also a product "
          "roadmap is not worthless, but it should be weighted accordingly.</p>",
          "<p>The second is whether the constraint is technical or organisational. Trends blocked by "
          "organisational friction — data ownership disputes, unclear metric definitions, absent "
          "evaluation discipline — move far more slowly than the technology curve suggests, because "
          "the friction does not respond to better tooling. Trends blocked by a technical constraint "
          "that is actively being removed, such as inference cost, tend to arrive on schedule. Most "
          "over-optimistic AI forecasts fail this test.</p>",
          "<p>The third is whether early adopters are reporting second-order effects. First-order "
          "reports describe activity: we deployed, we trained, usage is up. Second-order reports "
          "describe structural change: we stopped building dashboards, the analyst role changed, the "
          "planning cycle compressed. Second-order effects are much harder to fake and much more "
          "predictive of what your organisation will experience.</p>",
          "<p>The fourth is reversibility. Favour commitments you can unwind cheaply — a protocol at "
          "the integration boundary, a semantic layer that outlives a particular tool — over ones you "
          "cannot: a three-year licence, a bespoke integration estate, a reorganisation. When a "
          "prediction turns out to be wrong, and some will, the cost should be a migration rather "
          "than a write-off.</p>"]),
    ]},
}

SPECS["vector-databases-enterprise-search-2025-comparison"] = {
    "EN": {"new": [
        ("how-should-you-chunk-documents-for-enterprise-retrieval",
         "How Should You Chunk Documents for Enterprise Retrieval?",
         ["<p>Chunking receives far less attention than model selection and has a larger effect on "
          "retrieval quality in most enterprise deployments. The reason is straightforward: a chunk is "
          "the unit that gets embedded and retrieved, so if the chunk does not contain the answer "
          "coherently, no amount of model quality will recover it.</p>",
          "<p>Fixed-size chunking with overlap is the default and it is usually the wrong choice for "
          "enterprise content, because it splits mid-argument. A policy document split every five "
          "hundred tokens will separate a rule from its exceptions, and the retrieved chunk will be "
          "confidently incomplete — which is worse than obviously truncated, because nothing signals "
          "the gap to the reader.</p>",
          "<p>Structure-aware chunking performs better on the content enterprises actually have. "
          "Split on document structure first — headings, sections, table boundaries, list items — "
          "and only fall back to size limits when a section exceeds the embedding model's practical "
          "window. Keep tables intact: a table split across chunks is unusable, and tabular content "
          "is often exactly what users are asking about.</p>",
          "<p>Three refinements help further. Prepend a short contextual header to each chunk derived "
          "from its position in the document, so that a chunk from section 4.2 of a policy knows it is "
          "from section 4.2 — this alone recovers a noticeable share of retrieval failures. Preserve "
          "metadata at chunk level: document type, effective date, owner, and the access-control list. "
          "And evaluate chunk size against your own data rather than adopting a default: test two or "
          "three configurations against the labelled evaluation set and keep the one that wins.</p>",
          "<p>The one thing to avoid is treating chunking as a one-time configuration. Chunk size is "
          "a parameter with the same status as the embedding model: when either changes, re-run the "
          "evaluation and re-embed, or the two will drift out of sync.</p>"]),
    ]},
}

SPECS["conversational-bi-query-caching-optimization"] = {
    "EN": {"new": [
        ("what-breaks-when-you-cache-across-multiple-tenants",
         "What Breaks When You Cache Across Multiple Tenants?",
         ["<p>Multi-tenant caching introduces a failure mode that does not exist in single-tenant "
          "deployments and that is severe enough to warrant its own controls: a cache entry computed "
          "under one tenant's permissions being served to another. The performance incentive pushes "
          "toward sharing, and the security requirement pushes toward isolation, and the resolution "
          "has to be architectural rather than a configuration flag.</p>",
          "<p>The safe construction is to make tenant identity a mandatory component of every cache "
          "key, derived and validated server-side rather than taken from the request. Where row-level "
          "policies produce different visible slices for users in the same tenant, the effective "
          "permission set — not the tenant identifier alone — has to be part of the key. Deriving a "
          "stable hash of the resolved permission set is the usual implementation, and it has the "
          "useful side effect of keeping the key space manageable when there are only a handful of "
          "distinct roles.</p>",
          "<p>The second concern is memory pressure. Keying on identity multiplies the number of "
          "entries, so a cache sized for one tenant will thrash under fifty. Size the cache against "
          "the product of distinct intents and distinct permission sets, not against intents alone, "
          "and set an eviction policy that protects the entries with the highest recomputation cost "
          "rather than merely the most recent.</p>",
          "<p>Finally, test for it explicitly. Multi-tenant leakage is not something a functional test "
          "will catch, because the happy path works. Include cross-tenant access attempts in the "
          "automated suite — request a cached answer as tenant A, then request the same question as "
          "tenant B and assert that B cannot see A's rows — and run it whenever the caching layer or "
          "the permission model changes.</p>"]),
    ]},
}

SPECS["conversational-bi-dashboards-why-executives-switching"] = {
    "EN": {"new": [
        ("what-should-you-do-with-your-existing-dashboards",
         "What Should You Do With Your Existing Dashboards?",
         ["<p>The question every executive asks once a conversational layer is working is whether the "
          "dashboard estate should be retired. The answer is usually no, and the reasoning clarifies "
          "what each tool is actually for.</p>",
          "<p>Dashboards remain the better medium for monitoring — a fixed set of indicators you want "
          "to see at a glance, repeatedly, in a stable layout. The value of a dashboard is that it "
          "does not require you to formulate a question; the question has already been asked and "
          "encoded. An executive who checks the same six numbers every Monday morning does not want "
          "to type anything.</p>",
          "<p>The conversational layer is the better medium for investigation — the unanticipated "
          "follow-up, the anomaly that appeared in this morning's monitoring, the question that has "
          "no dashboard because nobody anticipated it. This is where dashboards are weakest and where "
          "the cost of the analyst round trip is highest.</p>",
          "<p>So the practical programme is not replacement but a change in the economics of "
          "proliferation. Keep the dashboards that are genuinely used for monitoring, and stop "
          "building new ones for questions that could be asked. Most estates contain a large number "
          "of dashboards built for a single request and viewed a handful of times; those are the ones "
          "whose marginal cost should collapse to zero.</p>",
          "<p>Measuring which is which is easier than it sounds. Pull the access logs, rank dashboards "
          "by distinct viewers per month, and review the bottom quartile with their owners. In "
          "practice a substantial share are retired without objection, because the team that "
          "commissioned them has already moved on. The remainder get a defined owner and a review "
          "date, and new requests default to a question rather than to a build.</p>"]),
    ]},
}

SPECS["responsible-ai-operationalizing-ethics-in-production"] = {
    "EN": {"new": [
        ("how-do-you-handle-a-model-that-must-be-explained-to-a-customer",
         "How Do You Handle a Model That Must Be Explained to a Customer?",
         ["<p>Explanation requirements change the architecture, because they convert explainability "
          "from a research problem into a records problem. When a customer is told a decision was "
          "made by an automated system, regulators generally expect the institution to give the "
          "substance of the logic involved, the significance, and the consequences — not the internal "
          "weights.</p>",
          "<p>Three capabilities satisfy most such requirements, and all three are engineering rather "
          "than science. First, decision reconstruction: the ability to retrieve exactly what the "
          "system knew and did at the moment of the decision — inputs, retrieved context, tools "
          "invoked, policy applied, model version. Without this, any explanation is a "
          "reconstruction and will eventually contradict the record.</p>",
          "<p>Second, reason articulation in the terms the customer uses. &quot;Your application was "
          "declined because the declared income does not meet the threshold for the requested "
          "limit&quot; is an explanation; &quot;the model scored you 0.31&quot; is not. This requires "
          "the decision logic to be representable in business rules or in a rule-like layer over the "
          "model, which is a design constraint worth imposing early.</p>",
          "<p>Third, counterfactual capability: the ability to say what would have changed the "
          "outcome, within the limits of what is appropriate to disclose. This is both the most "
          "useful thing you can tell a customer and the one most likely to be gamed, so it needs a "
          "disclosure policy that says how much detail is provided and to whom.</p>",
          "<p>Build the appeals path alongside it. An explanation that cannot be contested is not an "
          "explanation in any meaningful regulatory sense, and the appeal outcome is itself the "
          "highest-quality signal you will get about whether the model is behaving as intended.</p>"]),
    ]},
}

SPECS["cross-border-data-transfer-framework-2025-compliance"] = {
    "EN": {"new": [
        ("what-should-be-in-a-cross-border-incident-response-plan",
         "What Should Be in a Cross-Border Incident Response Plan?",
         ["<p>Transfer compliance failures have a distinctive incident profile: they are usually "
          "discovered through a vendor notification, a customer questionnaire, or a regulatory "
          "inquiry rather than through monitoring, which means the organisation finds out late and "
          "without context. A plan built for that discovery pattern is materially different from a "
          "security incident plan.</p>",
          "<p>The first requirement is a decision log that can be queried in reverse. When a regulator "
          "asks about a specific flow, you need to produce the assessment, the mechanism, the "
          "approval, and the data categories within days. If those records live in email threads, the "
          "response becomes a reconstruction project under time pressure — and reconstructions "
          "invariably surface additional problems.</p>",
          "<p>The second is a pre-agreed severity model for transfer findings, because not every gap "
          "is an incident. Define in advance what constitutes a reportable breach versus a "
          "remediation item: transfers with no valid mechanism, transfers of special-category data "
          "outside the documented basis, and transfers to an importer that cannot evidence its "
          "commitments are typically reportable; missing documentation for a low-volume internal flow "
          "is typically not. Deciding this during an incident is how organisations end up "
          "over-reporting or under-reporting.</p>",
          "<p>The third is a containment playbook. For a transfer, containment means stopping the "
          "flow, which usually means disabling an integration or repointing an endpoint rather than "
          "isolating a host. Know in advance which controls can stop which flows, and test them, "
          "because the control that stops a flow in the architecture diagram and the control that "
          "stops it in production are sometimes different.</p>",
          "<p>Then rehearse. A tabletop on a single scenario — a vendor discloses that it has been "
          "processing your data in a jurisdiction you did not approve — will surface most of the "
          "plan's gaps in ninety minutes.</p>"]),
    ]},
}

SPECS["secure-mcp-deployment"] = {
    "EN": {"new": [
        ("how-should-you-roll-out-mcp-access-without-losing-control",
         "How Should You Roll Out MCP Access Without Losing Control?",
         ["<p>MCP rollouts tend to follow one of two paths, and one of them produces a governance "
          "problem that is expensive to unwind. The permissive path — register every useful data "
          "source as a tool and let teams connect — is fast and produces broad adoption before "
          "anyone has assessed what the tools expose. The restrictive path — a central team reviews "
          "and approves each tool — is safe and produces a queue long enough that teams route around "
          "it, often by calling the underlying systems directly.</p>",
          "<p>The workable middle is a tiered catalogue. Tier one contains read-only tools over "
          "certified, low-sensitivity datasets, available to everyone by default, with standard "
          "logging. Tier two contains tools over sensitive or regulated data, available on request "
          "with a named approver and an audit review. Tier three contains tools with write or "
          "external-effect capability, requiring a documented use case, an approval threshold, and "
          "human confirmation above a defined value. Most consumption lands in tier one, most risk "
          "sits in tier three, and the review effort concentrates where it belongs.</p>",
          "<p>Pair the tiers with a registration process that is cheaper than bypassing it. A "
          "self-service form that captures the tool's purpose, data scope, owner, and retention, and "
          "that provisions logging and authorisation automatically, will be used. A process requiring "
          "a meeting will be avoided. The goal is not to make adding a tool difficult; it is to make "
          "adding an undocumented tool unnecessary.</p>",
          "<p>Finally, review the catalogue on a cadence. Tools outlive the projects that created "
          "them, and an unreviewed catalogue accumulates orphaned tools with live credentials. A "
          "quarterly attestation — does each tool still have an owner and a use case — is a small "
          "cost against a meaningful reduction in standing access.</p>"]),
    ]},
    "zh-CN": {"new": [
        ("如何在推广mcp访问的同时不失控",
         "如何在推广 MCP 访问的同时不失控？",
         ["<p>MCP 的推广往往沿着两条路径之一展开，其中一条会产生事后难以收拾的治理问题。宽松路径——把每个有用的数据源都注册成工具，让团队自由连接——速度快，在任何人评估这些工具暴露了什么之前就形成广泛采用。严格路径——由中央团队逐个评审批准——安全，但会形成长到让团队绕开的队列，而绕开的方式往往是直接调用底层系统。</p>",
          "<p>可行的中间道路是分层目录。第一层是对已认证、低敏感度数据集的只读工具，默认对所有人开放，并带有标准日志。第二层是对敏感或受管数据的工具，需申请、具名审批人与审计复核。第三层是具备写入或外部效应的工具，需有成文用例、审批阈值，以及超过既定金额时的人工确认。多数消费落在第一层，多数风险集中在第三层，评审精力也因此投在该投的地方。</p>",
          "<p>分层之外，还要配一个比绕开它更省事的注册流程。一份自助表单，采集工具用途、数据范围、负责人与留存期，并自动开通日志与授权，这样的流程会被使用；一个需要开会的流程会被规避。目标不是让新增工具变难，而是让新增未登记的工具变得没有必要。</p>",
          "<p>最后，按节奏复审目录。工具的寿命长于创建它的项目，未经复审的目录会积累持有有效凭据的孤儿工具。按季度做一次确认——每个工具是否仍有负责人与用例——投入很小，却能实质性削减常设访问权限。</p>"]),
    ]},
}

SPECS["ai-vendor-contract-negotiation-tips-nov2025"] = {
    "EN": {"new": [
        ("how-do-you-benchmark-a-vendor-before-you-negotiate",
         "How Do You Benchmark a Vendor Before You Negotiate?",
         ["<p>Your negotiating position is determined before the first call, by what you know about the "
          "alternatives. Most buyers enter an AI vendor negotiation having evaluated one product "
          "seriously, and the vendor can tell.</p>",
          "<p>Run a structured evaluation of at least three vendors against the same task, using the "
          "same data and the same scoring rubric. The rubric matters more than the number of vendors: "
          "define the ten to fifteen questions that represent your real workload, score answers for "
          "correctness against a known-good result, and record latency and cost per question. "
          "Anything less structured produces an impression rather than a comparison, and impressions "
          "do not survive contact with a procurement conversation.</p>",
          "<p>Include the operational criteria that are easy to overlook during evaluation but "
          "expensive later: how long onboarding actually takes, what the vendor needs from your team, "
          "whether the semantic layer or configuration is portable, what the support response time is "
          "under the proposed tier, and what happens to your configuration if you leave. Ask each "
          "vendor for two reference customers at a similar scale and in a similar sector, and take "
          "the calls.</p>",
          "<p>Then use the results explicitly. Sharing the evaluation criteria with vendors — not the "
          "scores — changes the conversation from a demonstration to a bid, and it surfaces which "
          "vendors are prepared to be measured. Vendors who decline to be evaluated on a defined task "
          "are telling you how the deployment will go.</p>",
          "<p>Keep the benchmark. It is the evidence base for the renewal negotiation in eighteen "
          "months, and it is the fastest way to answer the internal question of whether a competing "
          "proposal is genuinely better or merely better presented.</p>"]),
    ]},
}

SPECS["audit-ai-models-bias-fairness"] = {
    "EN": {"new": [
        ("how-do-you-keep-a-bias-audit-from-becoming-a-one-off",
         "How Do You Keep a Bias Audit From Becoming a One-Off?",
         ["<p>Point-in-time audits are common and their value decays quickly, because the things that "
          "change outcomes — data, population mix, upstream pipelines, model versions — change "
          "continuously while the audit does not. Converting an audit into a standing capability is "
          "mostly an engineering problem, and it is more tractable than it appears.</p>",
          "<p>The core is to encode the audit as code. The metric definitions, the subgroup "
          "definitions, the thresholds, and the reporting format should live in version control "
          "alongside the model, and the audit should run as a job rather than as a project. Once it "
          "runs on every training or promotion event, the marginal cost of the tenth audit "
          "approaches zero and the audit stops being an event anyone can postpone.</p>",
          "<p>Then attach it to the gates that already exist. Promotion to staging, promotion to "
          "production, and scheduled retraining are the three natural triggers. A bias check that "
          "blocks promotion is enforced; one that produces a report is advisory, and advisory controls "
          "are the first thing dropped under deadline pressure.</p>",
          "<p>Third, monitor the same metrics in production. The audit evaluates a model on a "
          "snapshot; production monitoring evaluates it on live traffic, and drift between the two is "
          "itself a finding. Disaggregated outcome rates, override rates, and complaint rates by "
          "subgroup are the minimum viable set, and they need thresholds and owners in the same way "
          "the pre-release metrics do.</p>",
          "<p>Finally, close the loop with a periodic review by someone outside the delivery team. An "
          "automated check answers whether the numbers moved; it does not answer whether the "
          "trade-off the model encodes is still the one the organisation would choose. That question "
          "needs a human, on a schedule, with authority to change the threshold.</p>"]),
    ]},
}

SPECS["enterprise-architecture-ai-era"] = {
    "EN": {"new": [
        ("what-does-ai-change-about-data-modelling",
         "What Does AI Change About Data Modelling?",
         ["<p>Dimensional modelling was designed for a world where humans write the queries and the "
          "query patterns are known in advance. Star schemas, conformed dimensions, and carefully "
          "tuned aggregates all assume that someone can anticipate the question. AI consumers break "
          "that assumption, and the modelling implications are larger than most teams expect.</p>",
          "<p>The first change is that modelling shifts from optimising for known queries to "
          "constraining unknown ones. A human analyst who writes a wrong join gets a wrong number and "
          "notices; a model that composes a wrong join gets a plausible number and does not. The "
          "defence is to make incorrect compositions unrepresentable, which means fewer, better-"
          "defined conformed dimensions and explicit grain declarations rather than a wide surface of "
          "similarly-named tables.</p>",
          "<p>The second is that business metadata becomes load-bearing. A column comment that nobody "
          "read for five years becomes the difference between a correct and an incorrect answer, "
          "because it is what the model matches against. Modelling work now includes writing "
          "definitions, synonyms, and permitted aggregation semantics — and those artefacts need "
          "owners and review in the same way the schema does.</p>",
          "<p>The third is that denormalisation becomes more attractive. Wide, well-documented, "
          "business-shaped tables reduce the number of joins a model has to compose correctly, and "
          "joins are where composition errors concentrate. Storage is cheap relative to the cost of a "
          "wrong answer reaching a decision.</p>",
          "<p>None of this makes dimensional modelling obsolete. It means the deliverable of data "
          "modelling is no longer just a schema — it is a schema plus the semantic contract that "
          "makes it safely queryable by something that cannot ask for clarification.</p>"]),
    ]},
    "zh-CN": {"new": [
        ("ai改变了数据建模的什么",
         "AI 改变了数据建模的什么？",
         ["<p>维度建模所面向的世界，是由人来写查询、且查询模式可预先知晓的世界。星型模型、一致性维度与精心调优的聚合，都假设有人能预见到问题。AI 消费方打破了这一假设，其对建模的影响比多数团队预期的更大。</p>",
          "<p>第一个变化是：建模的目标从&quot;为已知查询优化&quot;转向&quot;为未知查询设限&quot;。人类分析师写出错误的关联，得到错误数字并会察觉；模型拼出错误的关联，得到看似合理的数字且不会察觉。防御手段是让错误的组合无法被表达——这意味着更少但定义更清晰的一致性维度、显式的粒度声明，而不是一大片名称相近的表。</p>",
          "<p>第二个变化是业务元数据成为承重结构。五年无人阅读的列注释，会成为答案正确与否的分界线，因为模型匹配的就是它。建模工作如今包含撰写定义、同义词与允许的聚合语义，而这些制品需要与模式一样拥有负责人与评审。</p>",
          "<p>第三个变化是反规范化的吸引力上升。宽表、文档完备、贴合业务形态的表，能减少模型需要正确拼出的关联数量，而关联正是组合错误的集中地。相对于错误答案进入决策的代价，存储是便宜的。</p>",
          "<p>这些都不意味着维度建模过时。它意味着数据建模的交付物不再只是一个模式——而是模式加上一份语义契约，使某个无法追问澄清的消费方能够安全地查询它。</p>"]),
    ]},
}

SPECS["predictive-maintenance-ai-roi-20260116"] = {
    "EN": {"new": [
        ("what-sensor-infrastructure-do-you-actually-need",
         "What Sensor Infrastructure Do You Actually Need?",
         ["<p>Sensor strategy is where predictive maintenance programmes most often over-invest, and "
          "the over-investment happens early enough to undermine the business case. The assumption is "
          "that more sensing produces better predictions; in practice the binding constraint is almost "
          "always label quality and failure-mode selection, and additional sensors frequently add cost "
          "without adding signal.</p>",
          "<p>Start by asking what the existing systems already record. Modern PLCs, SCADA historians, "
          "and CMMS records typically hold far more than anyone has examined — vibration, temperature, "
          "current draw, cycle counts, alarm histories, and maintenance events. Auditing that data "
          "against the ranked failure modes usually identifies two or three signals that already "
          "correlate with degradation, at zero marginal instrumentation cost.</p>",
          "<p>Add instrumentation only where there is a specific, evidenced gap: a failure mode that "
          "is high-consequence, known to have a precursor, and for which no existing channel captures "
          "that precursor. Even then, instrument a subset of assets rather than the fleet, validate "
          "that the signal carries information, and only then scale. Retrofitting the whole fleet "
          "before validation is the most expensive way to discover that a channel is noisy.</p>",
          "<p>Two infrastructure properties matter more than sensor count. Sampling rate and "
          "alignment: the sampling frequency has to be high enough to capture the degradation "
          "signature, and timestamps have to be aligned across sources, or features computed across "
          "channels will be subtly wrong. And connectivity and retention: edge buffering so that a "
          "network outage does not erase the record of a failure event, and retention long enough to "
          "span several failure cycles.</p>",
          "<p>Treat the historian as part of the model. A model is only as good as the data it was "
          "trained on, and a historian with gaps during exactly the periods that matter — shutdowns, "
          "upsets, maintenance windows — will systematically underperform.</p>"]),
    ]},
}

SPECS["ai-roi-real-world-enterprise-case-studies-apr"] = {
    "EN": {"new": [
        ("which-metrics-should-go-to-the-board",
         "Which AI Metrics Should Go to the Board?",
         ["<p>Board reporting on AI tends to fail in one of two directions: activity metrics that "
          "imply progress without evidencing it, or financial metrics too immature to defend. The "
          "constructive version separates the two and reports them together, explicitly, with the "
          "relationship between them stated.</p>",
          "<p>Lead with the three leading indicators that predict financial return. Adoption breadth: "
          "weekly active users as a share of the eligible population, because licences issued measures "
          "procurement rather than value. Depth: median questions or tasks per active user per week, "
          "which distinguishes a tool people tried from one they rely on. And coverage: the share of "
          "questions in each domain that the system answers without escalation, which is the "
          "constraint on everything else.</p>",
          "<p>Then report the lagging indicators with honest attribution. Time-to-answer for a "
          "defined set of recurring questions, measured before and after. Cost per question, including "
          "inference and infrastructure, so that the board can see the unit economics move as adoption "
          "grows. And named financial benefits tied to specific decisions or processes, with the "
          "baseline stated, rather than an aggregate productivity claim.</p>",
          "<p>Add one risk metric, because boards fund what they can see and govern what they can "
          "measure: the rate of answers that required correction, or the share of decisions where the "
          "system's output was overridden. This number going down is what makes the adoption numbers "
          "credible.</p>",
          "<p>Finally, state the sequence. Present the report as a curve — leading indicators now, "
          "financial return in the stated period — rather than as a single number. Boards that "
          "understand the shape of the curve fund through the valley; boards that were promised "
          "immediate return cut at month six.</p>"]),
    ]},
}

SPECS["data-privacy-compliance-audits-ai-systems"] = {
    "EN": {"new": [
        ("who-should-perform-the-audit-and-how-independent-must-they-be",
         "Who Should Perform the Audit, and How Independent Must They Be?",
         ["<p>Audit independence is a spectrum rather than a binary, and placing an AI privacy audit "
          "correctly on it depends on what the output will be used for. Getting this wrong is 常见 "
          "and it undermines otherwise competent work.</p>",
          "<p>First-line review is performed by the team that built the system, against a standard "
          "checklist. It is fast, cheap, and necessary, and it is not an audit in any sense a "
          "regulator would recognise. Its value is that it catches the majority of gaps before anyone "
          "else looks, and it should run continuously rather than annually.</p>",
          "<p>Second-line review is performed by a function independent of delivery — privacy, risk, "
          "or compliance — using the first line's work as input and sampling behind it. This is the "
          "appropriate level for most internal AI privacy audits, and it is what most governance "
          "frameworks actually require. The reviewer needs enough technical fluency to test claims "
          "rather than accept them, and enough independence to escalate a finding over a delivery "
          "team's objection.</p>",
          "<p>Third-line or external review is appropriate where the audit output will be shown to a "
          "regulator, used in litigation, or relied on by a third party. The credibility of an audit "
          "is partly a function of who signed it, and an internal second-line report rarely carries "
          "the same weight externally. Budget for this deliberately for the small number of systems "
          "where it matters rather than applying it broadly.</p>",
          "<p>Whichever level applies, two conditions determine whether the work is worth doing. The "
          "auditor must have access — to systems, to configuration, to the people who built them — "
          "and the findings must go somewhere with authority to require remediation. An audit whose "
          "findings are advisory is a survey, and teams learn to treat it as one.</p>"]),
    ]},
}

SPECS["financial-services-ai-compliance-innovation"] = {
    "EN": {"new": [
        ("how-do-you-build-an-ai-use-case-intake-process",
         "How Do You Build an AI Use-Case Intake Process?",
         ["<p>Regulated institutions rarely fail because they lacked a control; they fail because a "
          "use case entered production without passing through one. Shadow AI adoption is the "
          "predictable response to a slow central process, so the intake process has to be both a "
          "control and a service, and the design goal is throughput with triage rather than "
          "thoroughness on every case.</p>",
          "<p>Start with a single front door. One form, one queue, one published service level. Every "
          "proposed use case — whether from a business team, a vendor, or an internal platform team "
          "— enters the same way and is classified by risk tier on the answers. Typical tiers: "
          "prohibited or restricted, high risk (affects customers, credit, or regulatory "
          "reporting), medium (internal decision support with human review), and low (internal "
          "productivity with no customer data).</p>",
          "<p>Then calibrate the review to the tier, and make the low tier genuinely fast. If a "
          "low-risk use case clears in three days, teams will use the process. If everything takes "
          "eight weeks regardless of tier, they will not, and the institution loses both the control "
          "and the visibility. Publishing the service level and hitting it is the most effective "
          "anti-shadow-AI measure available.</p>",
          "<p>Each tier needs a defined checklist that produces the artefacts the model risk framework "
          "will later require: intended use and foreseeable misuse, data sources and lawful basis, "
          "human oversight design, evaluation approach, and monitoring plan. Producing these at intake "
          "rather than at validation is what compresses the overall timeline, because the validation "
          "team receives a file rather than a request.</p>",
          "<p>Finally, log the decisions, including the rejections. An intake register showing what "
          "was proposed, what tier it received, and what conditions were imposed is itself a "
          "regulatory artefact, and it is the fastest way to answer the question a supervisor will "
          "ask: how do you know what AI you are running?</p>"]),
    ]},
}
