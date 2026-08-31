#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gb004_lib as B

SLUG = "what-is-text-to-sql-natural-language-query"

EN = {
 "lead": "Text-to-SQL is the capability that lets a person ask a business question in plain language and get back the correct SQL — and, more usefully, the correct answer — without writing a query. Under the hood it is a translation problem: map natural language onto a database schema, the business meaning of each table and column, and the exact SQL dialect the warehouse speaks. Done well, it collapses the distance between a question and its data from hours of analyst time to seconds, and it is the connective tissue between enterprise data and the conversational analytics that 2026 organisations increasingly expect.",
 "sections": [
  ("what-is-text-to-sql", "What Is Text-to-SQL?",
   """<p>Text-to-SQL is a subfield of semantic parsing where a model converts a natural-language question into a structured query language statement — almost always SQL — that can be executed against a database. The user does not need to know the table names, the join keys, or the syntax; they ask "what were last quarter's top five products by revenue in APAC?" and the system produces the query, runs it, and returns the result. The value is not the SQL itself but the removal of a bottleneck: the specialist knowledge required to get data out of a warehouse.</p>
<p>It matters because that bottleneck is expensive. In most enterprises the people who have the question are not the people who can write the query, so every question becomes a ticket, a queue, and a wait. Text-to-SQL turns the warehouse into something a business user can talk to, which is the precondition for the conversational BI that modern data teams are racing to deploy. It is also the most demanding test of an enterprise's data readiness, because a text-to-SQL system is only as good as the schema, the metadata, and the governance around it.</p>"""),
  ("how-does-text-to-sql-work", "How Does Text-to-SQL Work?",
   """<p>A robust text-to-SQL system has four stages. First, retrieval: the model is given the relevant schema — tables, columns, types, descriptions, and sample values — so it knows what data exists. Second, generation: a model composes a SQL statement that matches the question, often after decomposing a complex ask into sub-queries. Third, validation: the query is checked for syntax, for permission (can this user read these tables?), and for sanity (does the aggregation make sense?). Fourth, execution and explanation: the query runs, the result returns, and a plain-language summary explains what the numbers mean and which data supported them.</p>
<p>The retrieval and validation stages are what separate a demo from a product. A model that simply emits SQL from a question will, often enough, emit plausible-looking SQL that is wrong — joining on the wrong key, aggregating the wrong grain, or reading a stale table. The systems that work in production constrain generation with a governed schema and a semantic layer, validate the output before it runs, and refuse gracefully when confidence is low. Beehive Strategy's approach keeps the business definitions in a semantic layer so the generated SQL uses the same metrics humans use, not a guess at what a column means.</p>"""),
  ("why-it-matters-for-enterprises", "Why Does Text-to-SQL Matter for Enterprises?",
   """<p>It matters because analytics capacity is the constraint on most transformation programmes. Every self-service question a business user can answer directly is a question that does not consume an analyst, and the compound effect across a large organisation is large: faster decisions, fewer bottlenecks, and a data team freed to build rather than retrieve. For the first time, the people closest to a business problem can interrogate the data themselves, in the words they already use.</p>
<p>It also matters for consistency. When ten analysts write ten queries for "revenue," they get ten numbers; text-to-SQL bound to a semantic layer returns the one definition the business agreed on, so the warehouse stops being a source of disagreement. And it extends the reach of the warehouse to people who will never learn SQL — executives, operations staff, front-line managers — which is exactly the audience conversational analytics is built for. The strategic point is that text-to-SQL is not a feature; it is the interface layer that makes enterprise data broadly usable.</p>"""),
  ("challenges-and-solutions", "What Are the Challenges and How Are They Solved?",
   """<p>The first challenge is schema complexity. Real enterprise warehouses have thousands of tables with cryptic names and entangled relationships, and a model that cannot see the right tables will invent them. The solution is curated schema context: feed the model only the tables relevant to the question, with clear descriptions, rather than the entire catalogue. The second challenge is ambiguity — "revenue" might mean booked, recognised, or collected — and the solution is a semantic layer that resolves business terms to exact definitions before generation.</p>
<p>The third challenge is correctness on compound questions: multi-step reasoning, time comparisons, and "why did this change?" queries. The solution is query decomposition plus a validation loop that checks the draft SQL against the schema and the semantics before execution. The fourth challenge is access control: a text-to-SQL system must never read data the user may not see. The solution is permission-aware generation that plans queries through the same entitlements a human analyst uses. Each of these has a known pattern; the work is assembling them, not inventing them.</p>"""),
  ("what-are-the-current-limits-of-text-to-sql", "What Are the Current Limits of Text-to-SQL?",
   """<p>Text-to-SQL is strong on single-table and well-modelled questions and weaker on the long tail. It struggles when the schema is undocumented, when the question depends on context no column carries, when the required logic is unusually complex, or when the "right" answer depends on a business rule that lives only in a person's head. Published benchmarks on held-out schemas show high accuracy on standard questions but meaningful drops on adversarial or novel ones, which is why production systems pair the model with validation and human-in-the-loop review rather than shipping raw output.</p>
<p>The honest limit is trust, not syntax. A wrong query that runs and returns a number looks identical to a right one, so the differentiator is grounding: can the system show which tables and definitions it used, and can a human confirm them? Systems that surface provenance and confidence — and that decline when evidence is insufficient — are trusted; systems that always answer are quietly abandoned. The trajectory is clear: limits shrink every quarter as schemas, semantic layers, and feedback loops improve.</p>"""),
  ("beehive-strategy-and-text-to-sql", "How Does Beehive Strategy Approach Text-to-SQL?",
   """<p>Beehive Strategy's text-to-sql capability is built on a governed semantic layer rather than a raw schema. The model generates SQL against business-defined metrics — revenue, active customers, churn — so the output uses the definitions the organisation already agreed on, and every answer is consistent with every other. Generation is permission-aware, so a query can only touch data the requester is entitled to, and validation runs before execution, so malformed or dangerous queries never reach the warehouse.</p>
<p>The result is returned with a plain-language explanation and visible lineage back to source, so the user understands not just the number but the evidence. When confidence is low or the evidence insufficient, the system says so and can route to a human rather than guessing. This is what lets text-to-sql move from a impressive demo to a dependable service inside enterprise analytics.</p>"""),
  ("text-to-sql-security-and-governance", "What About Security and Governance?",
   """<p>Security is the make-or-break property. A text-to-SQL system that can read any table on behalf of any user is a privilege-escalation machine, so generation must inherit the access controls of the source system for the identity asking. That means filtering before ranking, re-indexing when entitlements change, and scoping the model's tool use so it cannot route around a restriction by calling a broader data source. Audit logs of every generated query and every result are non-negotiable for regulated industries.</p>
<p>Governance is the companion: versioned business definitions, an owner for each metric, and a review process for the prompts and models behind generation. The organisations that treat text-to-SQL as a governed service — not a prompt to a frontier model pointed at the warehouse — are the ones that can actually deploy it. Beehive Strategy enforces entitlement through the same semantic layer that defines the metrics, so permission and meaning are handled in one place.</p>"""),
  ("key-considerations-for-implementation", "What Should You Consider Before Implementing?",
   """<p>Start from data readiness, not model choice. The highest-leverage investments are a clean, documented schema and a semantic layer with agreed business definitions; without those, even the best model will guess. Pilot on a narrow, high-value domain where questions are repetitive and answers matter, instrument every generated query for correctness and refusal rate, and build a golden set of real questions to evaluate against. Treat the first deployment as a service with an SLA, not a chatbot experiment.</p>
<p>Plan for the human in the loop from day one: a review path for low-confidence queries, a feedback mechanism that improves the next iteration, and clear ownership of the metric definitions. Measure cost per trusted answer, not cost per query, because a cheap answer that users re-ask or ignore is more expensive than it looks. And keep the warehouse entitlement model as the single source of truth for access.</p>"""),
  ("beehive-strategy-comprehensive-approach", "What Is Beehive Strategy's Comprehensive Approach?",
   """<p>The comprehensive approach is to treat text-to-SQL as one component of a governed conversational analytics platform. The semantic layer provides consistent definitions and enforced entitlements; the generation and validation pipeline turns questions into safe, correct SQL; the explanation and lineage layer builds trust; and the feedback loop improves accuracy on the questions your organisation actually asks. None of this requires the business user to learn SQL, and all of it requires the data team to govern the foundation once.</p>
<p>For enterprises evaluating text-to-SQL, the practical recommendation is to start where the pain is sharpest, prove value on a narrow domain, and expand only as the semantic layer and governance mature. Beehive Strategy helps organisations stand that stack up so that asking the data a question becomes as natural — and as safe — as asking a colleague.</p>"""),
 ],
 "takeaways_id": "key-takeaways",
 "takeaways_h2": "What Are the Key Takeaways?",
 "takeaways_intro": "Five points capture what separates a demo from a deployment.",
 "takeaways": [
  "<strong>Text-to-SQL removes the query bottleneck</strong>, turning a warehouse into something a business user can talk to.",
  "<strong>Retrieval and validation are the product</strong>; raw generation is only a demo without governed schema and pre-execution checks.",
  "<strong>A semantic layer is the differentiator</strong>, resolving ambiguous terms like 'revenue' to one agreed definition.",
  "<strong>Security is make-or-break</strong>; generation must inherit source entitlements and log every query.",
  "<strong>Start narrow and govern the foundation</strong> before expanding across the estate.",
 ],
 "conclusion_id": "conclusion",
 "conclusion_h2": "What Should You Take Away?",
 "conclusion": """<p>Text-to-SQL is the interface that makes enterprise data broadly usable, and its maturity in 2026 is real — but only when it is built on a governed schema, a semantic layer, validation before execution, and entitlements inherited from the source system. The organisations that deploy it successfully treat it as a service with an SLA and a human in the loop, not as a prompt to a model pointed at the warehouse. Beehive Strategy's platform embodies that discipline, so the question "what happened to revenue in APAC last quarter?" gets one correct, explainable, access-controlled answer.</p>
<p>The next step for most enterprises is not a bigger model; it is a cleaner semantic layer and a defined ownership model for metrics. Do that, and text-to-SQL stops being experimental and starts being infrastructure.</p>""",
 "faq_h2": "Frequently Asked Questions",
 "faq": [
  ("What is text-to-SQL?",
   "Text-to-SQL is the capability that converts a natural-language question into a SQL query that can be executed against a database, returning the correct answer without the user writing any code. It works by mapping the question onto a database schema and the business meaning of its tables and columns, then validating and running the generated query. Its value is removing the specialist bottleneck between a business question and its data."),
  ("How accurate is text-to-SQL in practice?",
   "On well-modelled, single-table questions modern systems are highly accurate, but accuracy drops on undocumented schemas, ambiguous business terms, and complex multi-step reasoning. The realistic differentiator is not raw syntax accuracy but grounding: the system should show which tables and definitions it used and decline when evidence is insufficient. Production systems pair the model with validation and human review rather than shipping raw output."),
  ("Is text-to-SQL secure for enterprise data?",
   "It can be, but only if generation inherits the access controls of the source system for the identity asking — filtering before ranking, re-indexing when entitlements change, and scoping the model's tool use so it cannot bypass restrictions. Every generated query and result should be logged for audit. Without permission-aware generation, a text-to-SQL system is a privilege-escalation risk."),
  ("How should an enterprise get started with text-to-SQL?",
   "Start from data readiness, not model choice: a documented schema and a semantic layer with agreed business definitions matter more than the model. Pilot on a narrow high-value domain, instrument every query for correctness and refusal rate, keep a human in the loop for low-confidence questions, and measure cost per trusted answer. Expand only as governance matures."),
 ],
}

ZH = {
 "lead": "Text-to-SQL 是一种能力：让人用自然语言提出业务问题，就能得到正确的 SQL——更有用的是，得到正确的答案——而无需自己写查询。其本质是翻译问题：把自然语言映射到数据库 schema、每张表和每列的业务含义，以及数据仓库所用的具体 SQL 方言。做得好，它能把“从问题到数据”的距离从分析师的数小时压缩到数秒，也是企业数据与 2026 年组织日益期待的会话式分析之间的连接组织。",
 "sections": [
  ("what-is-text-to-sql", "什么是 Text-to-SQL？",
   """<p>Text-to-SQL 是语义解析的一个分支，模型把自然语言问题转换成可在数据库上执行的结构化查询语言语句——几乎总是 SQL。用户不需要知道表名、连接键或语法；他们问“上季度 APAC 营收最高的五个产品是什么？”，系统生成查询、执行并返回结果。价值不在 SQL 本身，而在于消除了获取数据仓库数据的专家知识瓶颈。</p>
<p>它之所以重要，是因为这个瓶颈很贵。在大多数企业里，提问题的人不是会写查询的人，所以每个问题都变成一张工单、一个队列、一段等待。Text-to-SQL 把数据仓库变成业务用户能对话的对象，这也是现代数据团队竞相部署的会话式 BI 的前提。它也是对企业数据就绪度最严苛的考验，因为 Text-to-SQL 系统的好坏，只取决于它周围的 schema、元数据和治理。</p>"""),
  ("how-does-text-to-sql-work", "Text-to-SQL 是如何工作的？",
   """<p>一个稳健的 Text-to-SQL 系统有四个阶段。第一，检索：把相关的 schema——表、列、类型、描述和样本值——提供给模型，让它知道有哪些数据。第二，生成：模型组合出与问题匹配的 SQL 语句，通常先把复杂问题拆成子查询。第三，验证：检查查询的语法、权限（该用户能否读取这些表？）和合理性（聚合是否有意义？）。第四，执行与解释：查询运行、返回结果，并用自然语言摘要说明数字的含义以及哪些数据支撑了它。</p>
<p>检索和验证阶段，是把演示和产品区分开的地方。一个只从问题生成 SQL 的模型，常常会生成看似合理却错误的 SQL——用错连接键、用错粒度聚合，或读取过时的表。在生产中真正有效的系统，会用受治理的 schema 和语义层约束生成、在执行前验证输出，并在置信度低时优雅拒绝。Beehive Strategy 的做法是把业务定义保留在语义层中，使生成的 SQL 使用与人类相同的指标，而非猜测某列的含义。</p>"""),
  ("why-it-matters-for-enterprises", "Text-to-SQL 为何对企业重要？",
   """<p>它重要，因为分析能力是多数转型项目的约束。业务用户能直接自助回答的每个问题，都是一个不再消耗分析师的问题，而这在大型组织中的复利效应是巨大的：决策更快、瓶颈更少，数据团队从“取数”中解放出来去建设。第一次，离业务问题最近的人可以用自己熟悉的语言直接追问数据。</p>
<p>它也关乎一致性。十个分析师写十个“营收”查询，会得到十个数字；绑定语义层的 Text-to-SQL 返回的是业务约定的那个定义，于是数据仓库不再是分歧的来源。它还把数据仓库的触达扩展到永远不会学 SQL 的人——高管、运营人员、一线经理——而这正是会话式分析服务的对象。战略要点是：Text-to-SQL 不是一项功能，而是让企业数据被广泛使用的接口层。</p>"""),
  ("challenges-and-solutions", "有哪些挑战，又如何解决？",
   """<p>第一个挑战是 schema 复杂度。真实的企业数据仓库有成千上万张表，名字晦涩、关系纠缠，看不到正确表的模型会“发明”它们。解决方案是精选的 schema 上下文：只把与问题相关的表及其清晰描述提供给模型，而非整个目录。第二个挑战是歧义——“营收”可能指记账、确认或收款——解决方案是在生成前用语义层把业务术语解析为精确定义。</p>
<p>第三个挑战是复合问题的正确性：多步推理、时间对比、“为什么变了？”类查询。解决方案是查询分解加验证循环，在执行前对照 schema 和语义检查草稿 SQL。第四个挑战是访问控制：Text-to-SQL 系统绝不能读取用户无权看的数据。解决方案是权限感知的生成，让查询通过人类分析师所用的同一套权限规划。每一项都有成熟模式；工作在于把它们组装起来，而非发明它们。</p>"""),
  ("what-are-the-current-limits-of-text-to-sql", "Text-to-SQL 当前的局限是什么？",
   """<p>Text-to-SQL 在单表、建模良好的问题上很强，在长尾上较弱。当 schema 无文档、问题依赖某列未携带的上下文、所需逻辑异常复杂，或“正确”答案取决于只存在于某人心中的业务规则时，它会吃力。在保留 schema 上的公开基准显示，标准问题准确率高，但在对抗性或新颖问题上明显下降——这正是为什么生产系统把模型与验证、人机协同审核结合，而非直接输出原始结果。</p>
<p>诚实的局限是信任，而非语法。一个错误却运行并返回数字的查询，看起来和正确的毫无区别，所以差异在于可追溯：系统能否展示它用了哪些表和定义，人类能否确认？能呈现来源与置信度、并在证据不足时拒绝的系统会被信任；永远回答的系统会被悄悄弃用。趋势很清楚：随着 schema、语义层和反馈循环的改进，局限每季度都在缩小。</p>"""),
  ("beehive-strategy-and-text-to-sql", "Beehive Strategy 如何看待 Text-to-SQL？",
   """<p>Beehive Strategy 的 Text-to-SQL 能力建立在受治理的语义层之上，而非裸 schema。模型针对业务定义的指标——营收、活跃客户、流失——生成 SQL，因此输出使用的是组织已约定的定义，每个答案都彼此一致。生成是权限感知的，查询只能触及请求者有权访问的数据，验证在执行前运行，因此畸形或危险的查询永远不会到达仓库。</p>
<p>结果随自然语言解释和可追溯到源的血缘一起返回，让用户不仅理解数字，也理解证据。当置信度低或证据不足时，系统会明说，并可路由给人类而非猜测。这正是让 Text-to-SQL 从惊艳演示变成企业分析内部可靠服务的关键。</p>"""),
  ("text-to-sql-security-and-governance", "安全与治理如何保障？",
   """<p>安全是决定成败的属性。一个能代表任何用户读取任何表的 Text-to-SQL 系统，是一台权限提升机器，所以生成必须继承源系统对提问者身份的访问控制。这意味着排序前先过滤、权限变化时重新索引、并对模型的工具使用做范围限定，使其无法通过调用更广的数据源绕过限制。对每个生成查询和结果的审计日志，对受监管行业是不可妥协的。</p>
<p>治理是配套：版本化的业务定义、每个指标的所有者，以及针对生成背后提示和模型的评审流程。把 Text-to-SQL 当作受治理的服务——而非指向仓库的 frontier 模型的一个提示——的组织，才真正能部署它。Beehive Strategy 通过定义指标的同一语义层强制执行权限，让权限与含义在同一处处理。</p>"""),
  ("key-considerations-for-implementation", "实施前应考虑什么？",
   """<p>从数据就绪度而非模型选择开始。杠杆率最高的投资是干净、有文档的 schema 和带有约定业务定义的语义层；没有这些，再好的模型也会猜测。在一个问题重复、答案关键的狭窄高价值领域试点，对每个生成查询的准确率和拒绝率做埋点，并构建真实问题的黄金集用于评估。把首次部署当作有 SLA 的服务，而非聊天机器人实验。</p>
<p>从第一天起就规划人机协同：低置信度查询的审核路径、改进下一次迭代的反馈机制，以及指标定义的清晰所有权。度量“每个可信答案的成本”，而非“每次查询的成本”，因为一个被用户重复问或忽略的廉价答案，其实更贵。并让仓库权限模型作为访问的唯一真相来源。</p>"""),
  ("beehive-strategy-comprehensive-approach", "Beehive Strategy 的整体方案是什么？",
   """<p>整体方案是把 Text-to-SQL 当作受治理的会话式分析平台的一个组件。语义层提供一致的定义和可强制的权限；生成与验证流水线把问题变成安全、正确的 SQL；解释与血缘层建立信任；反馈循环提升对组织真实问题的准确率。这些都不要求业务用户学 SQL，而要求数据团队一次性治理好基础。</p>
<p>对正在评估 Text-to-SQL 的企业，务实建议是：从痛点最尖锐处开始，在狭窄领域证明价值，只在语义层和治理成熟后再扩展。Beehive Strategy 帮助企业把这套架构搭起来，让向数据提问变得像问同事一样自然——且一样安全。</p>"""),
 ],
 "takeaways_id": "key-takeaways",
 "takeaways_h2": "关键要点是什么？",
 "takeaways_intro": "五个要点概括了演示与部署的区别。",
 "takeaways": [
  "<strong>Text-to-SQL 消除了查询瓶颈</strong>，把数据仓库变成业务用户能对话的对象。",
  "<strong>检索与验证才是产品</strong>；没有受治理 schema 和执行前检查，原始生成只是演示。",
  "<strong>语义层是差异点</strong>，把“营收”这类歧义术语解析为一个约定定义。",
  "<strong>安全是决定成败的</strong>；生成必须继承源权限，并记录每次查询。",
  "<strong>先窄后广、治理基础</strong>，再向全资产扩展。",
 ],
 "conclusion_id": "conclusion",
 "conclusion_h2": "你应当记住什么？",
 "conclusion": """<p>Text-to-SQL 是让企业数据被广泛使用的接口，它在 2026 年的成熟度是真实的——但只有当它建立在受治理的 schema、语义层、执行前验证，以及从源系统继承的权限之上时才成立。成功部署它的组织把它当作有 SLA、有人机协同的服务，而非指向仓库的模型提示。Beehive Strategy 的平台体现了这种纪律，所以“上季度 APAC 营收发生了什么？”能得到唯一正确、可解释、受访问控制的答案。</p>
<p>对多数企业来说，下一步不是更大的模型，而是更干净的语义层和指标的所有权模型。做到这点，Text-to-SQL 就不再是实验，而成了基础设施。</p>""",
 "faq_h2": "常见问题",
 "faq": [
  ("什么是 Text-to-SQL？",
   "Text-to-SQL 是把自然语言问题转换成可在数据库上执行的 SQL 查询的能力，用户无需编写任何代码即可得到正确答案。它通过把问题映射到数据库 schema 及其表列的业务含义，再验证并执行生成的查询来工作。其价值在于消除了业务问题与数据之间的专家瓶颈。"),
  ("Text-to-SQL 在实际中有多准确？",
   "在建模良好、单表的问题上，现代系统准确率很高；但在无文档 schema、歧义业务术语、复杂多步推理上会下降。现实中的差异点不是原始语法准确率，而是可追溯：系统应展示它用了哪些表和定义，并在证据不足时拒绝。生产系统把模型与验证、人机协同结合，而非直接输出原始结果。"),
  ("Text-to-SQL 对企业数据安全吗？",
   "可以安全，但前提是生成继承源系统对提问者身份的访问控制——排序前过滤、权限变化时重新索引、对模型工具使用做范围限定以防绕过。每次生成的查询和结果都应记录以审计。没有权限感知的生成，Text-to-SQL 系统就是权限提升风险。"),
  ("企业应如何开始使用 Text-to-SQL？",
   "从数据就绪度而非模型选择开始：有文档的 schema 和带约定业务定义的语义层，比模型更重要。在狭窄高价值领域试点，对每个查询的准确率和拒绝率做埋点，对低置信度问题保留人机协同，并度量每个可信答案的成本。只在治理成熟后再扩展。"),
 ],
}

if __name__ == "__main__":
    rep = B.build(SLUG, EN, ZH)
    print(rep)
