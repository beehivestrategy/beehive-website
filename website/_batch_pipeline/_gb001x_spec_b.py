# -*- coding: utf-8 -*-
"""Content specs for gbatch_001 slugs 3-6."""

SPECS = {}

# --------------------------------------------------------------------------- 3
SPECS["vector-databases-enterprise-search-2025-comparison"] = {
    "EN": {
        "rename": {
            "understanding-the-current-technology-landscape":
                "What Does the Enterprise Vector Database Landscape Look Like Now?",
            "technical-architecture-and-integration-patterns":
                "How Should Vector Search Fit Into Your Existing Architecture?",
            "performance-benchmarks-and-optimization-strategies":
                "How Do You Tune Vector Search Performance?",
            "integrating-vector-search-with-conversational-bi":
                "How Does Vector Search Connect to Conversational BI?",
        },
        "new": [
            ("which-vector-database-should-you-actually-choose",
             "Which Vector Database Should You Actually Choose?",
             ["<p>The honest answer is that the published benchmarks will not decide this for you. Most "
              "comparisons measure recall against a public dataset at a fixed index configuration, which "
              "tells you something about the algorithm and almost nothing about your operating cost. The "
              "decision that actually matters sits between three architectural families: dedicated vector "
              "stores, vector extensions to an existing database, and search engines that added vector "
              "support.</p>",
              "<p>Dedicated stores give you the best control over index parameters, quantization, and "
              "sharding, which matters when you are pushing past tens of millions of vectors or need very "
              "low latency at high concurrency. Extensions such as pgvector win when your corpus is "
              "modest, your team already runs Postgres well, and you need transactional joins between "
              "vectors and relational rows — you trade some index sophistication for a dramatically "
              "smaller operational surface. Search engines with vector support win when lexical relevance "
              "matters as much as semantic similarity, because they let you run both in one query planner "
              "instead of stitching two systems together and reconciling scores.</p>",
              "<p>Score the options against four constraints rather than a leaderboard: the size your "
              "corpus reaches in two years, the concurrency profile (a handful of analysts is a different "
              "system from five thousand employees), the freshness requirement (near-real-time ingestion "
              "forces different index choices than nightly rebuilds), and what your team can operate at "
              "three in the morning. A platform your on-call engineer understands beats one that wins a "
              "benchmark by four percentage points of recall.</p>"]),
            ("how-do-you-evaluate-recall-and-precision-in-production",
             "How Do You Evaluate Recall and Precision in Production?",
             ["<p>Vector search quality is usually evaluated once, on launch, with a handful of hand-picked "
              "queries — and then never again. That is the single most common reason semantic search "
              "silently degrades: the embedding model gets upgraded, the chunking strategy changes, or the "
              "corpus doubles, and nobody notices because there is no regression baseline to compare "
              "against.</p>",
              "<p>The fix is a labelled evaluation set built from real usage. Take the questions your users "
              "actually ask, and for each one record a small set of documents that a domain expert agrees "
              "are relevant. Two hundred of these is enough to be useful. Then measure recall@k — the "
              "share of known-relevant documents that appear in the top k results — and re-run it on every "
              "change to the embedding model, chunk size, or index parameters. Track it as a build "
              "artefact, not a spreadsheet, so that a pull request that drops recall by eight points fails "
              "before it ships.</p>",
              "<p>Pair the offline metric with online signals. Click-through on the first result, "
              "zero-result rate, and the rate at which users rephrase or abandon a question all tell you "
              "things recall alone cannot: whether the answer was relevant to the question as asked, "
              "whether the ranking put it where a human would look, and whether the corpus is missing the "
              "content entirely. A zero-result rate that climbs while recall holds steady is almost always "
              "a content gap, not a tuning problem.</p>",
              "<p>Finally, evaluate the pipeline end to end rather than the index in isolation. In a "
              "conversational BI deployment the retrieved context is only one input; the semantic layer, "
              "the query the model generates, and the formatting of the answer all affect whether the user "
              "got what they needed. Logging the full trace — question, retrieved chunks, generated query, "
              "result — is what lets you attribute a bad answer to the right component.</p>"]),
            ("what-does-hybrid-search-change-about-the-equation",
             "What Does Hybrid Search Change About the Equation?",
             ["<p>Pure semantic retrieval has a specific and surprising failure mode: it is bad at exact "
              "tokens. Ask for invoice INV-2024-08871 or product SKU 4471-B and an embedding model will "
              "happily return documents about invoices and SKUs without the one you asked for, because "
              "those identifiers carry almost no semantic signal relative to their neighbours in vector "
              "space. Users notice immediately, and it damages trust in everything else the system "
              "returns.</p>",
              "<p>Hybrid search addresses this by running a lexical pass and a semantic pass and fusing "
              "the results. The practical question is how to fuse them, and the two common approaches have "
              "different operational properties. Reciprocal rank fusion combines the two ranked lists by "
              "position and needs no score calibration, which makes it robust when the two engines produce "
              "incomparable scores — it is the right default. Weighted score combination can be better "
              "when you have tuned the weights against a labelled set, but it requires normalising scores "
              "that live on different scales, and it drifts when either engine is upgraded.</p>",
              "<p>The second thing hybrid changes is the metadata discipline it demands. Once lexical and "
              "semantic results compete for the same slots, filtered retrieval — restricting candidates by "
              "region, business unit, or effective date before ranking — becomes the main lever for "
              "precision. That only works if the metadata is populated consistently at ingest, which is a "
              "pipeline concern rather than a search concern. Teams that treat metadata as an "
              "afterthought end up with a hybrid system that behaves like a semantic one.</p>"]),
            ("how-do-you-operate-vector-search-at-enterprise-scale",
             "How Do You Operate Vector Search at Enterprise Scale?",
             ["<p>Operating vector search is mostly about managing three costs: index build time, memory, "
              "and the operational burden of keeping embeddings current. Each of them gets worse in a way "
              "that is easy to underestimate during a pilot with a hundred thousand vectors.</p>",
              "<p>Index build time and memory are both driven by your choice of quantization and index "
              "type. Product quantization compresses vectors aggressively and cuts memory several-fold, at "
              "the cost of some recall; scalar quantization is gentler and often sufficient. The right "
              "test is not which is more accurate in the abstract but which configuration holds your "
              "recall target at your corpus size within your memory budget. Rebuild cadence follows from "
              "the same analysis: an index that takes six hours to rebuild constrains how often you can "
              "re-embed, which in turn constrains how quickly a model upgrade can reach production.</p>",
              "<p>Embedding freshness is the cost teams forget. Vectors are derived data, so any change to "
              "the source record, the chunking rule, or the embedding model invalidates part of the index. "
              "Treating embeddings as a managed artefact — versioned with the model and the chunking "
              "configuration, with a re-embedding job that can be run per source rather than globally — is "
              "what keeps a re-embed from becoming a two-week project.</p>",
              "<p>Access control is the fourth operational concern, and the one that blocks enterprise "
              "rollout most often. Vectors inherit the permissions of their source documents, and that "
              "inheritance has to be enforced at query time, not at index time, because permissions "
              "change. Practical implementations attach an access-control list to each chunk and filter "
              "candidates before ranking. Doing this behind a single governed interface — an MCP server "
              "that exposes approved retrieval tools and writes an audit record per call — means every "
              "consumer inherits the same policy instead of reimplementing it.</p>"]),
        ],
    },
    "zh-CN": {
        "rename": {
            "理解当前技术格局": "当前向量数据库的技术格局是怎样的？",
            "技术架构与集成模式": "向量搜索应如何融入现有技术架构？",
            "性能基准与优化策略": "如何调优向量搜索的性能？",
            "企业部署最佳实践与实施建议": "企业部署向量搜索有哪些最佳实践？",
            "企业实施路线图与成功因素": "企业实施向量搜索的关键成功因素是什么？",
            "战略实施路径与关键成功因素": "应选择哪条战略实施路径？",
        },
    },
}

# --------------------------------------------------------------------------- 4
SPECS["conversational-bi-query-caching-optimization"] = {
    "EN": {
        "rename": {
            "the-evolving-landscape-of-natural-language-analytics":
                "How Is Natural Language Analytics Changing Enterprise Query Patterns?",
            "technical-architecture-and-performance":
                "What Does a Caching Architecture for Conversational BI Look Like?",
            "user-experience-and-adoption-patterns":
                "How Does Caching Change User Experience and Adoption?",
            "enterprise-integration-considerations":
                "What Should Enterprises Consider When Integrating Caching?",
            "how-a-managed-service-handles-optimization":
                "How Does a Managed Service Handle Cache Optimization?",
            "strategic-recommendations":
                "What Are the Strategic Recommendations for 2026?",
        },
        "new": [
            ("when-does-caching-actually-pay-off-in-conversational-bi",
             "When Does Caching Actually Pay Off in Conversational BI?",
             ["<p>Caching pays off in conversational BI for a reason that surprises people coming from "
              "traditional BI: question distribution is far more concentrated than dashboard distribution. "
              "In a dashboard estate, every view is a distinct query against a distinct slice, and "
              "personalised filters fragment the cache. In a conversational deployment, a relatively small "
              "number of questions accounts for a large share of traffic — last month's revenue by region, "
              "headcount by department, top customers by order value — because people ask the same things "
              "in slightly different words.</p>",
              "<p>That concentration is what makes a semantic cache effective. The cache key is not the "
              "SQL string but the resolved intent: once the question has been mapped through the semantic "
              "layer to a specific metric, dimension, and filter set, &quot;what was revenue last "
              "month&quot; and &quot;show me last month's total revenue&quot; collapse to the same key. "
              "That is also why caching without a semantic layer underperforms — two differently phrased "
              "questions produce two different SQL strings and two cache misses.</p>",
              "<p>The economics are straightforward once you measure them. If your median analytical query "
              "costs a few seconds of warehouse time and forty percent of questions map onto a resolvable "
              "repeat intent, a cache with a seventy percent hit rate removes roughly a quarter of "
              "warehouse spend and cuts median response time from seconds to tens of milliseconds. Those "
              "two numbers — hit rate and median latency — are the ones to put in front of a CFO, not the "
              "cache size.</p>",
              "<p>Caching does not pay off everywhere, and it is worth being explicit about where it does "
              "not. Ad-hoc exploratory questions with genuinely novel filter combinations are cache misses "
              "by construction. Questions against data that changes minute by minute have a useful TTL "
              "measured in seconds, which erodes the benefit. And questions whose answer depends on the "
              "identity of the asker need the identity in the cache key, which fragments it again. Design "
              "for the concentrated head of the distribution and let the tail miss.</p>"]),
            ("how-do-you-invalidate-a-cache-without-breaking-trust",
             "How Do You Invalidate a Cache Without Breaking Trust?",
             ["<p>Invalidation is where most caching implementations lose user trust, because a stale "
              "answer in analytics is worse than a slow one. The user has no way to tell that the number "
              "they received was correct an hour ago, and once they discover one stale answer they stop "
              "trusting every fast answer. Getting invalidation right is therefore a correctness problem "
              "before it is a performance problem.</p>",
              "<p>Three strategies cover most cases. Time-based expiry is simplest and works well when the "
              "source has a known refresh cadence: a nightly-loaded warehouse table can safely carry a TTL "
              "that expires shortly after the load window. Event-driven invalidation is stronger and "
              "cheaper in aggregate — when a pipeline completes, the cache entries whose keys depend on "
              "the affected tables are dropped explicitly. Dependency-tracking invalidation is the most "
              "precise: the cache records which tables and columns a result touched, so a change to an "
              "unrelated table does not force a flush.</p>",
              "<p>In practice, a production deployment layers all three: a conservative default TTL as a "
              "backstop, event-driven invalidation wired into the orchestration tool for the tables that "
              "matter, and dependency metadata captured at query time so that invalidation can be "
              "targeted. The dependency metadata also makes the system explainable — you can answer "
              "&quot;why did this number change&quot; by pointing at the pipeline run that invalidated "
              "it.</p>",
              "<p>One detail deserves emphasis: state the freshness to the user. Showing the as-of "
              "timestamp next to a cached answer, and offering an explicit refresh control, converts a "
              "correctness risk into an informed choice. Users are remarkably tolerant of a slightly "
              "stale answer they can see the age of, and remarkably intolerant of one that looks current "
              "and is not.</p>"]),
            ("what-should-you-measure-to-prove-caching-is-working",
             "What Should You Measure to Prove Caching Is Working?",
             ["<p>Four metrics tell the whole story, and two of them are routinely missing from caching "
              "dashboards. Hit rate is the obvious one, but it must be measured against resolvable intents "
              "rather than raw questions: a question the system could not map to a known metric is not a "
              "cache miss, it is a semantic-layer gap, and conflating the two hides both problems.</p>",
              "<p>The second is latency distribution, measured at the percentiles users actually "
              "experience. Mean latency hides the bimodality that makes caching valuable: most questions "
              "return in tens of milliseconds from cache, a minority take seconds from the warehouse, and "
              "the mean sits in the middle describing nobody's experience. Report p50 and p95 "
              "separately, and track the p95 of cache hits as its own number, because a cache that is "
              "slow to look up stops being worth having.</p>",
              "<p>The third, usually missing, is staleness incidents: the count of answers served whose "
              "as-of timestamp was older than the policy allows at the time they were served. This is a "
              "correctness metric and it should be zero, and any non-zero value should page someone. The "
              "fourth, also usually missing, is warehouse spend attributable to conversational traffic — "
              "credits consumed per week, normalised by active users — which is the number that converts "
              "a performance project into a cost project with a payback period.</p>",
              "<p>Together these also let you tune the policy with evidence rather than intuition. If hit "
              "rate is high but p95 is unchanged, the cache is serving the easy questions and the "
              "expensive ones are still missing. If staleness incidents climb after a TTL increase, the "
              "TTL was doing real work. If warehouse spend per user falls while adoption rises, you have "
              "the compounding effect that makes the case for the next phase of investment.</p>"]),
        ],
        "faq": [
            ("What is the biggest performance bottleneck in conversational BI?",
             "In most deployments it is not the language model but the round trip to the warehouse. "
             "Generating a query takes a few hundred milliseconds; executing an analytical scan can take "
             "seconds. Semantic caching and pre-aggregation in the semantic layer remove the warehouse "
             "round trip for the concentrated head of repeated questions, which is usually where the "
             "majority of traffic sits."),
            ("How does caching interact with row-level security?",
             "The requesting identity has to be part of the cache key, or a cached answer computed for "
             "one user can be served to another who should not see it. The practical pattern is to "
             "resolve the effective permission set first, derive a stable identifier for it, and key the "
             "cache entry on the combination of resolved intent and that permission identifier."),
            ("Should cached results be stored in the warehouse or a separate store?",
             "A separate low-latency store. Writing cached results back into the warehouse consumes the "
             "resource you were trying to protect and adds latency. A key-value or in-memory store close "
             "to the application tier gives the sub-100ms retrieval that makes caching visible to users."),
            ("What is a realistic cache hit rate for enterprise conversational BI?",
             "Mature deployments with a well-defined semantic layer typically run between 55% and 75% on "
             "business-hours traffic, because question distribution is heavily concentrated. Below 40% "
             "usually indicates a semantic layer gap rather than a caching problem: the system cannot "
             "recognise that two phrasings mean the same question."),
        ],
    },
    "zh-CN": {
        "rename": {
            "自然语言分析的发展格局": "自然语言分析如何改变企业查询模式？",
            "技术架构与性能": "对话式 BI 的缓存架构是怎样的？",
            "用户体验与采用模式": "缓存如何改变用户体验与采用率？",
            "企业整合考量": "企业集成缓存时需要考虑什么？",
            "战略建议": "2026 年的战略建议是什么？",
        },
    },
}

# --------------------------------------------------------------------------- 5
SPECS["conversational-bi-dashboards-why-executives-switching"] = {
    "EN": {
        "rename": {
            "the-limits-of-traditional-bi-and-the-case-for-change":
                "Why Do Traditional Dashboards Stop Working for Executives?",
            "core-technology-components":
                "What Are the Core Components Behind Conversational BI?",
            "implementation-strategy-and-best-practices":
                "What Implementation Strategy Actually Works?",
            "the-executive-decision-workflow-reimagined":
                "How Does the Executive Decision Workflow Change?",
            "in-depth-analysis-of-conversational-bi-technical-architecture":
                "What Does the Technical Architecture Actually Look Like?",
        },
        "new": [
            ("what-do-executives-actually-do-that-dashboards-cannot-support",
             "What Do Executives Actually Do That Dashboards Cannot Support?",
             ["<p>The gap is not that executives dislike dashboards; it is that the work executives do is "
              "not the work dashboards were designed for. A dashboard answers a question someone "
              "anticipated and encoded in advance. Executive work is mostly the opposite: a number arrives "
              "in a meeting or an email, and the response is a sequence of unanticipated follow-ups — "
              "why did it drop, is it the same in the other region, did we see this last year, which "
              "customers drove it.</p>",
              "<p>Each of those follow-ups is a new query against a different slice, and each one "
              "traditionally costs a round trip through an analyst. The result is a well-documented "
              "pattern: the meeting ends with an action to &quot;get someone to look into it&quot;, the "
              "thread goes quiet, and the decision is made on the original number without the context. "
              "Dashboards are excellent at monitoring and poor at interrogation, and executive work is "
              "mostly interrogation.</p>",
              "<p>Conversational interfaces fit the shape of the work because they make the follow-up "
              "free. Asking &quot;why did APAC revenue drop 12% last quarter&quot; and then &quot;was it "
              "price or volume&quot; and then &quot;which customers&quot; is one continuous session "
              "rather than three tickets. The value is not that the first answer arrives faster; it is "
              "that the fifth question gets asked at all.</p>",
              "<p>There is a second, quieter gap: definitions. Executives rarely trust the number on "
              "screen enough to act, because three dashboards report three versions of revenue. A "
              "conversational layer sitting on a governed semantic model answers with the certified "
              "definition and can say which one it used. That removes the argument about whose number is "
              "right, which is often a larger tax on decision speed than the query latency ever "
              "was.</p>"]),
            ("how-do-you-roll-out-conversational-bi-to-an-executive-team",
             "How Do You Roll Out Conversational BI to an Executive Team?",
             ["<p>Executive rollouts fail for a predictable reason: the system is launched broadly with a "
              "thin semantic layer, an early high-profile wrong answer circulates, and credibility is lost "
              "before the coverage improves. Executives have very low tolerance for being wrong in front "
              "of peers, and unlike analysts they will not debug a query to work out whether the system "
              "or the data was at fault.</p>",
              "<p>The pattern that works starts narrow and deep rather than broad and shallow. Pick one "
              "executive and one decision domain — the CFO and weekly revenue performance, for example — "
              "and certify the twenty or so metrics that domain depends on. Define each with an owner, a "
              "business definition, and a data lineage. Publish the metric catalogue so that the assistant "
              "answers from it and refuses gracefully when a question falls outside it. Graceful refusal "
              "is a feature: &quot;I do not have a certified definition for that yet&quot; preserves "
              "trust; a plausible guess destroys it.</p>",
              "<p>Then instrument the first month closely. Log every question, whether it was answered, "
              "and whether the answer was corrected. Review the unanswered and corrected questions weekly "
              "with the metric owners. In practice, the first month's log is the most valuable artefact "
              "in the programme: it is a demand-driven backlog for the semantic layer, and it prioritises "
              "work by what executives actually asked rather than by what the data team assumed they "
              "would ask.</p>",
              "<p>Only after the first domain is solid should scope expand — to a second executive, then "
              "to their leadership teams. This sequence is slower at the start and much faster by month "
              "six, because each domain inherits a trusted catalogue and a team that has learned how to "
              "extend it. Programmes that launch broadly at once almost always spend their second quarter "
              "rebuilding trust rather than extending coverage.</p>"]),
            ("what-does-conversational-bi-cost-compared-with-dashboard-sprawl",
             "What Does Conversational BI Cost Compared With Dashboard Sprawl?",
             ["<p>The comparison is rarely made properly, because dashboard costs are distributed across "
              "licences, analyst time, and warehouse compute, while a conversational platform shows up as "
              "one line item. Putting them side by side usually reverses the intuitive answer.</p>",
              "<p>Start with the analyst time, which is the largest and least measured component. A "
              "typical enterprise BI estate has hundreds to thousands of dashboards, most of them built "
              "for a specific request and many of them unused. Maintaining them — fixing broken "
              "definitions after a schema change, answering ad-hoc follow-ups, reconciling two versions "
              "of the same metric — consumes a substantial share of analyst capacity. In deployments we "
              "have run, the shift to a conversational model did not eliminate dashboards but stopped "
              "their proliferation: the marginal request became a question the system answered rather "
              "than a dashboard someone built.</p>",
              "<p>Then add warehouse compute. Dashboards refresh on a schedule whether or not anyone looks "
              "at them, and interactive dashboards issue queries on every filter change. A conversational "
              "system with semantic caching and pre-aggregation serves the concentrated head of repeated "
              "questions from cache, so compute tracks actual demand rather than scheduled refresh. The "
              "saving is largest where dashboard sprawl is worst.</p>",
              "<p>Set against that are the real costs of the conversational approach: the semantic layer "
              "build, which is genuine engineering work and the main reason programmes underestimate; "
              "evaluation infrastructure to catch wrong answers before users do; and ongoing metric "
              "ownership. Budget for all three explicitly. The programmes that fail on cost are the ones "
              "that funded the interface and treated the semantic layer as an implementation detail.</p>"]),
            ("how-do-you-keep-the-assistant-from-answering-badly",
             "How Do You Keep the Assistant From Answering Badly?",
             ["<p>The risk profile of conversational analytics is specific: a wrong answer is fluent, "
              "confident, and plausible, and it reaches a decision faster than a wrong dashboard would. "
              "Controlling it requires defence at three layers, none of which is optional.</p>",
              "<p>The first layer is the semantic layer itself. When the assistant can only compose "
              "queries from certified metrics and defined dimensions, a large class of wrong answers "
              "becomes unrepresentable. This is the highest-leverage control available and it is why the "
              "semantic layer is a correctness investment, not a performance one. It also makes answers "
              "attributable: the response can cite the definition it used.</p>",
              "<p>The second is evaluation before release. Maintain a set of representative questions with "
              "known-correct answers, and run it on every change to prompts, tools, models, or metric "
              "definitions. Treat a regression as a build failure. This is the same discipline as unit "
              "testing, applied to a system whose output is prose, and it is what lets you upgrade an "
              "underlying model without re-litigating every question.</p>",
              "<p>The third is production feedback and traceability. Log the full trace — question, "
              "resolved intent, generated query, rows returned — so that a disputed answer can be "
              "reconstructed rather than argued about. Add a lightweight correction affordance, and route "
              "corrections to the metric owner. The organisations that do all three find that the "
              "conversation about adoption changes: the question is no longer whether to trust the "
              "assistant in general, but which specific domains have earned it.</p>"]),
        ],
    },
    "zh-CN": {
        "rename": {
            "核心技术组件": "对话式 BI 背后的核心组件有哪些？",
            "实施策略与最佳实践": "哪种实施策略真正有效？",
            "战略实施路径与关键成功因素": "战略实施路径与关键成功因素是什么？",
            "企业实施路线图与成功因素": "企业实施路线图应如何设计？",
            "行业数字化转型深度分析": "行业数字化转型有哪些深层驱动力？",
        },
        "rename_text": {
            "传统BI的局限性与变革的理由": "传统看板为何对高管失效？",
            "对话式BI的进阶能力与未来演进": "对话式 BI 的进阶能力与未来演进是什么？",
            "对话式BI技术架构深度解析": "对话式 BI 的技术架构究竟长什么样？",
        },
    },
}

# --------------------------------------------------------------------------- 6
SPECS["responsible-ai-operationalizing-ethics-in-production"] = {
    "EN": {
        "rename": {
            "data-collection-consent-and-minimisation":
                "How Does Consent and Minimisation Work at Collection Time?",
            "training-bias-detection-and-mitigation":
                "How Do You Detect and Mitigate Bias During Training?",
            "deployment-transparency-and-override":
                "What Does Transparency and Override Require at Deployment?",
            "monitoring-continuous-ethical-assessment":
                "How Do You Monitor Models Continuously After Release?",
            "key-takeaways": "What Are the Key Takeaways?",
            "conclusion": "Where Should You Start?",
        },
        "new": [
            ("what-does-operationalising-ai-ethics-actually-mean",
             "What Does Operationalising AI Ethics Actually Mean?",
             ["<p>Most organisations that publish AI ethics principles have not operationalised them, and "
              "the gap is definitional. A principle is a statement about values; an operational control is "
              "a check that runs, produces a record, and has a named owner who acts when it fails. "
              "Operationalising ethics means converting each principle into the second kind of thing, and "
              "accepting that some principles will not convert cleanly.</p>",
              "<p>Take fairness. As a principle it is uncontroversial. As a control it requires choosing a "
              "metric — demographic parity, equalised odds, or predictive parity — and those metrics are "
              "mathematically incompatible with one another except in narrow cases. Choosing one is a "
              "value judgement made concrete, and it has to be made by someone accountable rather than "
              "defaulted into by a library. The operational artefact is a documented decision: for this "
              "model, in this context, we optimise for equalised odds on this protected attribute, and "
              "here is why.</p>",
              "<p>Three mechanisms do most of the conversion work. Gates, which stop a model from "
              "advancing until a check passes — a bias metric below a threshold before promotion to "
              "production. Monitors, which run continuously after release and alert on drift in the same "
              "metrics. And records, which capture the decision, the evidence, and the owner at the point "
              "of decision, so that the choice can be reviewed months later by someone who was not "
              "present.</p>",
              "<p>The organisational half matters as much. Every control needs a named owner with "
              "authority to act, an escalation path when a threshold is breached, and a review cadence. "
              "Controls without owners degrade quickly, because the first time a gate blocks a release "
              "under deadline pressure, an unowned control gets overridden and an owned one gets a "
              "documented exception.</p>"]),
            ("how-do-you-run-a-model-ethics-review-before-release",
             "How Do You Run a Model Ethics Review Before Release?",
             ["<p>A pre-release review works when it is a checklist with evidence rather than a meeting "
              "with opinions. The distinction matters: a meeting produces a discussion that is hard to "
              "audit six months later, while a checklist produces artefacts — a completed impact "
              "assessment, a bias evaluation report, a documented override path — that survive staff "
              "changes and satisfy an external auditor.</p>",
              "<p>The review should cover six things. Intended use and reasonably foreseeable misuse, "
              "written down, because most ethics failures are use-case drift rather than model defects. "
              "Data provenance and lawful basis for every training source. Metric definitions and the "
              "trade-off chosen between competing fairness criteria, with the rationale. Measured "
              "performance disaggregated by relevant subgroups, not just aggregate accuracy. The human "
              "override path, including who can exercise it and how quickly. And the monitoring plan: "
              "which signals, at what threshold, owned by whom.</p>",
              "<p>Two practices make the review proportionate rather than bureaucratic. Tier it by risk — "
              "a model that ranks content for internal search does not need the same review as one that "
              "affects credit or hiring decisions, and pretending otherwise means the high-risk reviews "
              "get rushed. And run it in parallel with development rather than at the end: a review that "
              "starts after the model is built can only approve or block, whereas one that starts at "
              "problem framing can shape the design.</p>",
              "<p>Finally, decide in advance what happens on a failed check. A review whose only outcome "
              "is approval is not a gate. Document the possible outcomes — proceed, proceed with "
              "mitigation and monitoring, restrict to a narrower use case, or do not ship — and make sure "
              "the reviewers have the authority to choose the last one.</p>"]),
            ("what-should-you-monitor-after-a-model-ships",
             "What Should You Monitor After a Model Ships?",
             ["<p>Post-release monitoring is where most responsible AI programmes are thinnest, and it is "
              "where the risk actually accumulates, because models degrade quietly. Data drifts, upstream "
              "pipelines change semantics without changing schemas, and population mix shifts — none of "
              "which produces an error log.</p>",
              "<p>Monitor four families of signal. Input drift: has the distribution of features moved "
              "away from the training distribution, and specifically has it moved for the subgroups you "
              "care about. Prediction drift: has the distribution of outputs changed, including the rate "
              "at which the model declines to answer or routes to a human. Outcome metrics where "
              "ground truth eventually arrives — approval rates, error rates, complaint rates — "
              "disaggregated by the same subgroups used in the bias evaluation. And operational override "
              "rate: how often humans reverse the model, which is the single best early indicator that "
              "something has changed.</p>",
              "<p>Thresholds and ownership matter more than the metrics themselves. A metric nobody watches "
              "is decoration. Each signal needs a threshold that triggers a defined action — investigate, "
              "roll back to the previous version, or restrict the use case — and a named owner who "
              "receives the alert. Recalibration should be a scheduled activity with a documented trigger, "
              "not an ad-hoc response to a complaint.</p>",
              "<p>Keep the evidence as you go. A monitoring log with the metric history, the alerts "
              "raised, and the actions taken is what turns a retrospective audit from a reconstruction "
              "exercise into a report run. Regulators increasingly ask for exactly this, and the "
              "organisations that can produce it find the conversation far shorter.</p>"]),
            ("who-should-own-responsible-ai-inside-the-organisation",
             "Who Should Own Responsible AI Inside the Organisation?",
             ["<p>The most common structural mistake is placing responsible AI solely with a central "
              "ethics function. Central teams are good at setting standards, building tooling, and "
              "running reviews for the highest-risk cases. They are bad at context: they do not know that "
              "a particular feature is a proxy for tenure, or that a subgroup matters in one market and "
              "not another. That knowledge sits with the teams building and operating the models.</p>",
              "<p>The model that works in practice is a federated one with three roles. A central function "
              "owns the framework, the shared tooling, the templates, and the escalation path, and it "
              "holds the authority to block a high-risk release. Delivery teams own the application of "
              "the framework to their models: the impact assessment, the metric choice, the subgroup "
              "definitions, and the monitoring. A second-line reviewer — risk, compliance, or legal, "
              "depending on the sector — provides independent challenge on the highest tier.</p>",
              "<p>Make the accountability explicit at the model level. Every production model should have "
              "a named business owner who is accountable for its outcomes and can take it out of service, "
              "separate from the technical owner who maintains it. When something goes wrong, the "
              "question &quot;who decided this model should do this&quot; should have a documented "
              "answer, and the answer should not be a committee.</p>",
              "<p>Two practices keep the structure from becoming ceremonial. Include responsible AI "
              "objectives in delivery teams' performance measures, so that the work is resourced rather "
              "than volunteered. And run periodic exercises — a tabletop on a plausible failure — so that "
              "the escalation path is tested before it is needed rather than invented during an "
              "incident.</p>"]),
        ],
        "faq": [
            ("What is the first concrete step in operationalising AI ethics?",
             "Build a model inventory. You cannot apply controls to systems you have not identified. "
             "Record every model in production, its purpose, its business owner, its data sources, and a "
             "risk tier. That inventory then drives which models need full impact assessments and which "
             "need only lightweight review, which is what makes the programme proportionate."),
            ("How do you choose between competing fairness metrics?",
             "You cannot satisfy all of them simultaneously, so the choice is a contextual value "
             "judgement rather than a technical one. Document which metric you selected for each model, "
             "why it fits the harm you are most concerned about, and who approved the trade-off. The "
             "documentation matters as much as the selection."),
            ("Who should be accountable when a model causes harm?",
             "A named business owner per model, with authority to take it out of service, separate from "
             "the technical owner. The central AI ethics function owns the framework and escalation path; "
             "delivery teams own applying it. Accountability that rests with a committee is accountability "
             "that will not survive an incident."),
            ("How often should a deployed model be re-reviewed?",
             "Tier it by risk: high-impact models affecting credit, hiring, healthcare, or safety should "
             "be reviewed at least quarterly and on any material change to data, model, or use case. "
             "Lower-risk models can follow an annual cycle triggered by drift alerts or significant "
             "changes."),
        ],
    },
    "zh-CN": {
        "rename": {
                                                                        "要点": "关键要点是什么？",
            "结论": "应从哪里开始？",
        },
        "rename_text": {
            "数据收集：同意和最小化": "采集环节的同意与最小化如何落地？",
            "培训：偏差检测和缓解": "训练阶段如何检测与缓解偏差？",
            "部署：透明度和覆盖": "部署环节的透明度与人工覆盖要求什么？",
            "监控：持续道德评估": "模型发布后如何持续监控？",
        },
        "new": [
            ("落地ai伦理到底意味着什么",
             "落地 AI 伦理到底意味着什么？",
             ["<p>多数发布了 AI 伦理原则的组织并未真正落地，落差首先来自定义。原则是关于价值观的陈述；运营控制是一项会运行、会留下记录、并在失败时由具名负责人处置的检查。落地伦理，就是把每一条原则转化为后者，并接受有些原则无法干净地转化。</p>",
              "<p>以公平为例。作为原则它毫无争议；作为控制，它要求选定一个指标——人口统计均等、机会均等或预测均等——而这些指标除个别特例外在数学上互不相容。选定其一，就是把价值判断具体化，必须由承担责任的人做出，而不是被某个代码库默认值决定。运营制品是一份成文决策：就此模型、在此场景下，我们针对该受保护属性优化机会均等，理由如下。</p>",
              "<p>三项机制承担大部分转化工作。闸门：在检查通过前阻止模型进入下一阶段——晋升生产前偏差指标须低于阈值。监控：发布后持续运行，对同样指标的漂移发出告警。记录：在决策时点保存决策内容、证据与负责人，使数月后未在场的人也能复核。</p>",
              "<p>组织侧同等重要。每项控制都需要具名且有权处置的负责人、阈值被突破时的升级路径，以及固定复审节奏。没有负责人的控制会迅速退化：当闸门第一次在交付压力下阻断发布时，无主的控制被绕过，有主的控制则留下成文的例外。</p>"]),
            ("发布前应如何开展模型伦理评审",
             "发布前应如何开展模型伦理评审？",
             ["<p>发布前评审之所以有效，是因为它是一份附证据的清单，而非一场交换意见的会议。区别很关键：会议产出的是半年后难以审计的讨论，清单产出的是可持续的制品——已完成的影響评估、偏差评估报告、成文的人工覆盖路径，它们能经受人员变动并满足外部审计。</p>",
              "<p>评审应覆盖六项。预期用途与可合理预见的误用，须落笔写明，因为多数伦理失败源自用例漂移而非模型缺陷。每一个训练来源的数据出处与合法性基础。指标定义以及在相互竞争的公平准则之间所做的取舍及其理由。按相关子群体分列（而非仅汇总）的实测表现。人工覆盖路径，包括谁可以行使、多快可行。以及监控计划：监控哪些信号、阈值多少、由谁负责。</p>",
              "<p>两项实践让评审保持相称而非官僚。按风险分层：为内部搜索排序的模型，不需要与影响信贷或招聘决策的模型同等评审，假装同等反而会让高风险评审被压缩。以及与开发并行而非在末端开展：模型建成后才开始的评审只能批准或否决，而在问题界定阶段就介入的评审能够塑造设计。</p>",
              "<p>最后，预先约定检查未通过时的处置。只有批准这一结果的评审不是闸门。把可能结果写清楚——放行、附带缓释与监控后放行、收缩至更窄用例、或不予发布——并确保评审者有权选择最后一项。</p>"]),
            ("模型上线后应监控什么",
             "模型上线后应监控什么？",
             ["<p>发布后监控是多数负责任 AI 项目最薄弱的环节，而风险恰恰在此累积，因为模型的退化是静默的。数据在漂移；上游流水线的语义可能在模式不变的情况下改变；人群构成在移动——这些都不会产生错误日志。</p>",
              "<p>监控四类信号。输入漂移：特征分布是否偏离训练分布，尤其在你关注的子群体上是否偏离。预测漂移：输出分布是否变化，包括模型拒答或转人工的比例。结果指标（当真实标签最终可得时）——批准率、错误率、投诉率——按偏差评估中使用的同种子群体分列。以及运营覆盖比例：人工推翻模型的频率，这是&quot;情况已经变化&quot;最好的单一早期指标。</p>",
              "<p>阈值与归属比指标本身更重要。无人查看的指标只是装饰。每个信号都需要触发既定动作的阈值——排查、回滚至上一版本、或收缩用例——以及接收告警的具名负责人。再校准应是有成文触发条件的计划性活动，而非接到投诉后的临时反应。</p>",
              "<p>过程中持续留存证据。包含指标历史、已触发告警与所采取行动记录的监控日志，能把回溯性审计从还原工程变成一次报表运行。监管方正越来越多地要求这一点，能够提供它的组织会发现沟通过程短得多。</p>"]),
            ("组织内部应由谁负责负责任ai",
             "组织内部应由谁负责负责任 AI？",
             ["<p>最常见的结构性错误，是把负责任 AI 完全交给中央伦理团队。中央团队擅长制定标准、建设工具、以及为最高风险案例做评审；却不掌握上下文——他们不知道某个特征是从业年限的代理变量，也不知道某个子群体在一个市场重要而在另一个市场不重要。这些知识在构建与运营模型的团队手里。</p>",
              "<p>实践中有效的模式是三角色联邦式。中央职能负责框架、共享工具、模板与升级路径，并保有阻断高风险发布的权力。交付团队负责把框架落到自己的模型上：影响评估、指标选择、子群体定义与监控。第二道防线评审者——依行业不同为风险、合规或法务——对最高层级提供独立挑战。</p>",
              "<p>在模型层面明确问责。每一个生产模型都应有对其结果负责、并有权下线的具名业务负责人，与负责维护的技术负责人分离。当问题发生时，&quot;谁决定让这个模型做这件事&quot;应当有成文的答案，而且答案不应是一个委员会。</p>",
              "<p>两项实践防止结构流于形式。把负责任 AI 目标纳入交付团队的绩效衡量，使这项工作获得资源而非靠志愿投入。并定期开展演练——针对一个可信的失败场景做桌面推演——使升级路径在需要之前就被检验，而不是在事故中临时发明。</p>"]),
        ],
        "faq": [
            ("落地 AI 伦理的第一步是什么？",
             "建立模型清单。无法对尚未识别的系统施加控制。记录生产环境中的每一个模型、其用途、业务负责人、数据来源与风险层级。这份清单进而决定哪些模型需要完整影响评估、哪些只需轻量评审，这正是项目保持相称性的基础。"),
            ("如何在相互竞争的公平指标之间选择？",
             "无法同时满足所有指标，因此选择是情境化的价值判断而非技术判断。就每个模型记录所选指标、它与你最关注的危害如何对应、以及谁批准了该取舍。文档记录与选择本身同等重要。"),
            ("模型造成损害时应由谁负责？",
             "每个模型由具名业务负责人担责，并有权将其下线，与负责维护的技术负责人分离。中央 AI 伦理职能负责框架与升级路径；交付团队负责落地执行。落在委员会身上的问责，是无法在事故中存续的问责。"),
            ("已部署模型应多久复审一次？",
             "按风险分层：影响信贷、招聘、医疗或安全的高影响模型，至少每季度复审一次，并在数据、模型或用例发生实质变更时复审。较低风险模型可采用年度周期，由漂移告警或重大变更触发。"),
        ],
    },
}
