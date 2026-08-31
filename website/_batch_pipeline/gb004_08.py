#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gb004_lib as B

SLUG = "building-semantic-layer-self-service-analytics"

EN = {
 "lead": "A semantic layer is the quiet piece of enterprise data architecture that decides whether self-service analytics is trustworthy or chaotic. It is the agreed definition of business metrics, dimensions, and relationships, stored once and reused everywhere, so that a question asked in the boardroom, a dashboard, and a conversational assistant all resolve to the same number. Without it, every team rebuilds the same logic, disagreements multiply, and AI trained on inconsistent definitions inherits the inconsistency. With it, self-service and conversational analytics finally mean the same thing to everyone. Building it is less glamorous than buying a new dashboard tool, but it is the precondition for every dashboard, metric, and conversation agreeing on the same truth. Without it, even the most advanced model simply inherits and amplifies the organisation's existing contradictions, which is the failure mode most enterprises never see coming.",
 "sections": [
  ("what-is-a-semantic-layer", "What Is a Semantic Layer?",
   """<p>A semantic layer is a governed, centralised definition of how raw data maps to business meaning. It holds the canonical definitions of metrics like revenue, active customer, and churn; the dimensions they can be sliced by, such as region, product, and cohort; and the relationships between tables that make a join correct. Crucially, it sits between the physical warehouse and every consumer — BI tools, notebooks, and conversational agents — so that none of them redefines the metric locally. The metric is defined once and computed consistently wherever it is used.</p>
<p>The contrast with the status quo is stark. In most enterprises the definition of "revenue" lives in dozens of places: a SQL view here, a spreadsheet there, a dashboard calculation somewhere else, each subtly different. A semantic layer collapses that sprawl into one authoritative source, and it becomes the contract between data engineering and the business. When the business changes what "active customer" means, it is updated in one place, not in forty. That single property, definitions defined once, is what makes everything downstream reliable, and it is why the semantic layer is the foundation of trustworthy self-service.</p>
<p>It is worth being precise about what a semantic layer is not. It is not the warehouse itself, and it is not a visualization tool. It is the meaning layer on top of the warehouse, expressed in a way both machines and analysts can use, and it is deliberately independent of any single frontend so that every interface inherits the same truth. Treat it as the shared vocabulary of the organisation, written down and enforced.</p>"""),
  ("the-three-components-of-a-semantic-layer", "What Are the Three Components of a Semantic Layer?",
   """<p>The first component is the metric definition: the business logic that turns columns into a number people trust. This includes the base measure, any filters, the grain at which it is computed, and the aggregation rule. A well-specified metric leaves no ambiguity — "revenue" means recognised revenue in the reporting currency, not bookings, not collections — so two analysts asking the same question get the same answer by construction rather than by luck.</p>
<p>The second component is the dimensional model: the dimensions, hierarchies, and relationships that let a metric be sliced, diced, and drilled. Region rolls up to country rolls up to global; product belongs to category; customer has a lifecycle stage. These relationships are what make a metric explorable, and defining them once prevents the thousand small join errors that otherwise accumulate across teams. The third component is governance: ownership, versioning, and access control over the definitions themselves. A metric without an owner and a change history is just another undocumented query waiting to diverge.</p>
<p>Together these three components turn a pile of tables into a navigable business model. The metric definitions say what to compute, the dimensional model says how to explore it, and governance says who may change it and what changed. Build all three and the layer is a product; build only the first and it is a glossary that nobody enforces.</p>"""),
  ("why-this-matters-for-conversational-bi", "Why Does a Semantic Layer Matter for Conversational BI?",
   """<p>Conversational BI asks a person to type a question and get a number, which means the system must translate natural language into the correct metric and dimension without a human in the loop to catch a wrong definition. If the underlying definitions are inconsistent, the model will confidently return a number that disagrees with the dashboard the executive saw yesterday, and trust collapses on first contact. The semantic layer is what lets the model resolve "revenue last quarter in APAC" to one canonical computation rather than guessing at what a column means.</p>
<p>This is the difference between a demo and a deployment. A text-to-SQL demo pointed at raw tables will, often enough, join on the wrong key or use the wrong grain and produce a plausible wrong answer. The same question routed through a semantic layer resolves to the agreed metric and the correct relationships, so the answer is not only fast but defensible. Conversational analytics is only safe to put in front of executives when the meaning it queries is governed, and the semantic layer is that governance.</p>
<p>There is a second benefit that is easy to miss: the semantic layer makes the assistant explainable. Because the answer came from a named metric with a known definition and lineage, the system can show the user which definition it used and why, instead of presenting a number from an opaque query. That provenance is what turns a chatbot into a colleague you can question, and it is the property that separates tools organisations adopt from tools they abandon.</p>"""),
  ("building-your-semantic-layer-in-practice", "How Do You Build a Semantic Layer in Practice?",
   """<p>Start with the metrics that cause the most arguments, not the whole catalogue. Every organisation has a handful of definitions — revenue, active user, conversion — that are contested or duplicated, and those are where inconsistency is most expensive. Define those first, with the business owner in the room, and ship them behind a single interface. A narrow, authoritative layer beats a broad, half-finished one, because the narrow one is actually可信.</p>
<p>Use a declarative, code-based approach rather than embedding logic in dashboards. Define metrics in version-controlled files so changes are reviewed, tested, and reversible, exactly like software. This makes the layer a maintained product instead of a drifting set of calculations, and it lets data engineering enforce the same review discipline they apply to pipelines. Pair the definitions with automated tests that compare the layer's output against a golden set of known answers, so a regression in a metric is caught before a human sees it.</p>
<p>Connect the layer to every consumer through one governed access path. BI tools, notebooks, and conversational agents should all query through it, not around it, which is what keeps them consistent. And instrument usage so you can see which metrics are actually queried, which definitions are stale, and where the business is asking questions the layer cannot yet answer. That telemetry tells you where to expand next, turning the build into a roadmap rather than a guess.</p>"""),
  ("how-do-you-measure-the-roi-of-a-semantic-layer", "How Do You Measure the ROI of a Semantic Layer?",
   """<p>The ROI shows up in three places, and all three are measurable. The first is dispute resolution time: how long it takes to settle "whose number is right?" Today that question triggers meetings, ticket threads, and manual reconciliations; with a governed layer it is answered by pointing at the one definition, and the hours saved across an enterprise are large and recurring. Track the volume of metric-dispute tickets before and after, and the reduction is the first line of the business case.</p>
<p>The second is analyst productivity. When definitions are reused instead of rebuilt, analysts stop re-deriving revenue and start answering new questions; the layer converts duplicated effort into net-new analysis. Measure the share of analysis built on the layer versus rebuilt from scratch, and the trend is the productivity signal. The third is trust and adoption of self-service and conversational analytics. A semantic layer is what makes those tools safe enough for executives, and their adoption rate is the ultimate measure — a conversational assistant nobody trusts has negative ROI, while one anchored to governed definitions changes how decisions get made.</p>
<p>A practical scorecard tracks four numbers monthly: metric-dispute tickets, share of analysis reusing layer definitions, self-service query volume, and executive adoption of conversational analytics. Together they show whether the layer is paying for itself, and they keep the investment honest when the next platform arrives promising the same outcome without the foundation.</p>"""),
  ("common-semantic-layer-mistakes", "What Are the Most Common Semantic Layer Mistakes?",
   """<p>The first mistake is treating the layer as a documentation exercise rather than a product. A wiki of definitions that nobody enforces produces the same divergence it was meant to prevent, because the dashboard still computes its own number. The layer has to be the path every tool queries, or it is just a nicer spreadsheet.</p>
<p>The second mistake is boiling the ocean: attempting to define every metric in the catalogue before shipping anything, which guarantees the project dies in a backlog. The third is leaving definitions without an owner, so when a metric needs to change, no one is authorised and the stale definition quietly spreads. The fourth is coupling the layer to a single BI vendor, which re-creates lock-in and means conversational agents may not inherit it. The fix for all four is the same discipline that makes any platform trustworthy: ship narrowly, govern ownership, version everything, and keep the layer independent of any one frontend.</p>
<p>A subtle but expensive mistake is defining metrics at the wrong grain. A metric computed at the wrong level of detail looks correct in aggregate and is wrong in every slice, which is exactly the failure mode that destroys trust in conversational analytics. Specifying the grain explicitly, as part of the definition, is what prevents it, and it is the single most overlooked field in semantic-layer implementations.</p>"""),

 ],
 "takeaways_id": "key-takeaways",
 "takeaways_h2": "What Are the Key Takeaways?",
 "takeaways_intro": "Five points capture why the semantic layer is foundational.",
 "takeaways": [
  "<strong>A semantic layer defines metrics once and reuses them everywhere</strong>, ending the sprawl of contradictory definitions.",
  "<strong>It has three parts</strong>: metric definitions, a dimensional model, and governance over both.",
  "<strong>It is what makes conversational BI safe</strong>, resolving questions to one canonical computation instead of a guess.",
  "<strong>Build it narrowly and authoritatively first</strong>, with business owners and version-controlled definitions.",
  "<strong>Measure ROI in disputes avoided, analyst productivity, and adoption</strong> of self-service and conversational analytics.",
 ],
 "conclusion_id": "conclusion",
 "conclusion_h2": "What Should You Take Away?",
 "conclusion": """<p>A semantic layer is not a glamorous purchase, but it is the piece that decides whether self-service and conversational analytics can be trusted at all. It replaces dozens of contradictory definitions with one authoritative source, gives conversational agents a governed meaning to query, and makes every answer explainable by lineage. Organisations that skip it discover, usually after an expensive chatbot failure, that the problem was never the model; it was the undefined business behind it.</p>
<p>The practical path is unglamorous and effective: define the contested metrics first with their owners, express them in version-controlled code, connect every consumer through one governed path, and measure disputes, productivity, and adoption. Beehive Strategy's platform is built on exactly this discipline, so that asking the data a question returns the same trusted number everywhere. Do the foundation, and the interfaces on top of it stop fighting each other.</p>""",
 "faq_h2": "Frequently Asked Questions",
 "faq": [
  ("What is a semantic layer?",
   "A semantic layer is a governed, centralised definition of how raw data maps to business meaning. It holds the canonical definitions of metrics such as revenue and churn, the dimensions they can be sliced by, and the relationships between tables, sitting between the warehouse and every consumer so that no tool redefines a metric locally. It is the shared, enforced vocabulary of the organisation."),
  ("Why is a semantic layer important for conversational BI?",
   "Conversational BI translates a question into a metric with no human to catch a wrong definition, so if definitions are inconsistent the system returns a number that disagrees with what the executive saw, and trust collapses. A semantic layer resolves the question to one canonical computation and correct relationships, making the answer fast and defensible, and it provides the lineage that lets the assistant explain its result."),
  ("How should an enterprise start building a semantic layer?",
   "Start with the few metrics that cause the most arguments, define them with the business owner present, and ship them behind one governed interface. Use version-controlled, declarative definitions with automated tests against a golden set, connect every consumer through the layer rather than around it, and instrument usage to guide where to expand next."),
  ("How do you measure the ROI of a semantic layer?",
   "ROI appears in three measurable places: the time spent resolving metric disputes, analyst productivity from reusing definitions instead of rebuilding them, and the adoption of self-service and conversational analytics once they are safe to trust. A monthly scorecard of dispute tickets, reuse share, query volume, and executive adoption shows whether the layer is paying for itself."),
 ],
}

ZH = {
 "lead": "语义层是企业数据架构中那块安静却决定自助分析可信与否的拼图。它是业务指标、维度和关系的约定定义，只存一次、处处复用，从而让董事会议室、仪表盘和会话式助手提出的同一个问题，都解析到同一个数字。没有它，每个团队都重建同一套逻辑，分歧成倍增加，而基于不一致定义训练的 AI 也会继承这种不一致。有了它，自助分析与会话式分析才终于对所有人意味着同一件事。",
 "sections": [
  ("what-is-a-semantic-layer", "什么是语义层？",
   """<p>语义层是对“原始数据如何映射到业务含义”的受治理、集中式定义。它持有指标（如营收、活跃客户、流失）的规范定义、可被切片的维度（如地区、产品、队列），以及让连接正确的表间关系。关键在于，它位于物理仓库与每个消费者——BI 工具、笔记本、会话式代理——之间，使它们都不再本地重定义指标。指标只定义一次，在它被使用的任何地方都一致计算。</p>
<p>这与现状形成鲜明对比。在大多数企业，“营收”的定义散落在几十个地方：这里的 SQL 视图、那里的电子表格、别处的仪表盘计算，彼此微妙地不同。语义层把这种蔓延收敛为唯一权威来源，并成为数据工程与业务之间的契约。当业务改变“活跃客户”的含义，只在一处更新，而非四十处。这个“定义一次”的属性，正是让下游一切都可靠的原因，也是语义层成为可信自助分析基础的理由。</p>
<p>值得精确地说清语义层不是什么。它不是仓库本身，也不是可视化工具。它是仓库之上的含义层，以机器和分析师都能使用的方式表达，并刻意独立于任何单一前端，让每个接口都继承同一真相。把它当作组织共享的词汇表，写下来并强制执行。</p>"""),
  ("the-three-components-of-a-semantic-layer", "语义层由哪三部分组成？",
   """<p>第一部分是指标定义：把列变成人们信任的数字的业务逻辑。它包括基础度量、任何过滤条件、计算的粒度，以及聚合规则。一个良好定义的指标不留歧义——“营收”指报告币种下的已确认营收，而非预订、非收款——于是两个分析师问同一问题时，是靠构造而非运气得到同一答案。</p>
<p>第二部分是维度模型：让指标可被切片、切块、下钻的维度、层级和关系。地区上卷到国家再上卷到全球；产品属于品类；客户有生命周期阶段。这些关系让指标可被探索，而只定义一次能防止各团队间累积的无数小连接错误。第三部分是治理：对定义本身的所有权、版本控制和访问控制。没有所有者和变更历史的指标，只是另一个等待分歧的未文档化查询。</p>
<p>三者合在一起，把一堆表变成一个可导航的业务模型。指标定义说算什么，维度模型说如何探索，治理说谁可以改、改了什么。三者都建好，这一层才是产品；只建第一部分，它只是一个没人执行的术语表。</p>"""),
  ("why-this-matters-for-conversational-bi", "语义层为何对会话式 BI 重要？",
   """<p>会话式 BI 让人输入问题、得到数字，这意味着系统必须在没有人类捕捉错误定义的情况下，把自然语言翻译成正确的指标和维度。如果底层定义不一致，模型会自信地返回一个与高管昨天所见仪表盘相矛盾的数字，信任在第一接触就崩塌。语义层让模型把“上季度 APAC 营收”解析为一个规范计算，而非猜测某列的含义。</p>
<p>这正是演示与部署的区别。指向裸表的 text-to-SQL 演示，常常会用错连接键或用错粒度，给出看似合理却错误的答案。同一个问题经由语义层路由，则解析到约定指标和正确关系，答案不仅快，而且可辩护。会话式分析只有在所查询的含义被治理后，才敢放到高管面前。</p>
<p>还有第二个易被忽视的好处：语义层让助手可解释。因为答案来自带已知定义和血缘的命名指标，系统能向用户展示它用了哪个定义、为什么，而不是抛出一个来自不透明查询的数字。这种来源正是把聊天机器人变成可被追问的同事的关键，也是区分被采用与被弃用工具的性质。</p>"""),
  ("building-your-semantic-layer-in-practice", "实践中如何构建语义层？",
   """<p>从引发最多争论的指标开始，而非整个目录。每个组织都有少数定义——营收、活跃用户、转化——存在争议或被重复，那里不一致的成本最高。先与业务所有者一起定义这些，并通过单一接口发布。一个狭窄而权威的层，胜过一个宽泛却半成品的层，因为狭窄的那个真正可信。</p>
<p>用声明式、基于代码的方式，而非把逻辑嵌进仪表盘。在受版本控制的文件中定义指标，使变更像软件一样被评审、测试和回滚。这让该层成为被维护的产品，而非漂移的计算集合，并让数据工程施加与流水线相同的评审纪律。把定义与自动测试配对，对照已知答案的黄金集检查层的输出，从而在人类看到之前捕获指标的回归。</p>
<p>通过一个受治理的访问路径把该层连接到每个消费者。BI 工具、笔记本和会话式代理都应经由它查询，而非绕过它，这正是它们保持一致的原因。并对使用做埋点，让你看到哪些指标真被查询、哪些定义已过时、业务在哪里问该层尚不能答的问题。这些遥测告诉你下一步扩展到哪里，把构建变成路线图而非猜测。</p>"""),
  ("how-do-you-measure-the-roi-of-a-semantic-layer", "如何度量语义层的 ROI？",
   """<p>ROI 出现在三个地方，且都可度量。第一是争议解决时间：“谁的数字对？”这个问题今天会触发会议、工单线程和人工对账；有了受治理的层，只需指向那个唯一定义即可回答，全企业节省的工时巨大且持续。跟踪前后指标争议工单量，其下降就是商业案例的第一行。</p>
<p>第二是分析师生产力。当定义被复用而非重建，分析师不再重算营收，而是去回答新问题；该层把重复劳动转化为全新分析。度量基于该层的分析占比，其趋势就是生产力信号。第三是自助与会话式分析的信任与采用。语义层正是让这些工具对高管足够安全的东西，其采用率是最根本的度量——没人信任的会话式助手 ROI 为负，而锚定受治理定义的助手改变决策的制定方式。</p>
<p>一个务实的记分卡每月跟踪四个数字：指标争议工单、复用层定义的分析占比、自助查询量、高管对会话式分析的采用率。它们共同显示该层是否物有所值，并在下一个承诺同样结果却无基础的平台到来时，让投资保持诚实。</p>"""),
  ("common-semantic-layer-mistakes", "语义层最常见的错误有哪些？",
   """<p>第一个错误是把该层当作文档工作而非产品。一页没人执行的术语定义，产生它本要防止的同样分歧，因为仪表盘仍在算自己的数字。该层必须是每个工具都查询的路径，否则它只是一份更好看的电子表格。</p>
<p>第二个错误是煮大海：试图在发布任何东西之前定义目录中的每个指标，这保证项目死在积压里。第三个是定义没有所有者，于是当指标需要变更时无人有权，过时定义悄悄扩散。第四个是把该层耦合到单一 BI 厂商，重新制造锁定，并意味着会话式代理可能无法继承它。这四者的解药是同一种纪律：窄发布、治理所有权、一切版本化，并保持该层独立于任何单一前端。</p>
<p>一个微妙却昂贵的错误是在错误粒度上定义指标。在错误细节层级计算的指标，在聚合时看似正确、在每个切片里却错，而这正是摧毁会话式分析信任的失败模式。把粒度作为定义的一部分显式指定，正是防止它的方法，也是语义层实现中最被忽视的字段。</p>"""),

 ],
 "takeaways_id": "key-takeaways",
 "takeaways_h2": "关键要点是什么？",
 "takeaways_intro": "五个要点概括为何语义层是基础。",
 "takeaways": [
  "<strong>语义层把指标定义一次、处处复用</strong>，终结矛盾定义蔓延。",
  "<strong>它由三部分组成</strong>：指标定义、维度模型，以及对两者的治理。",
  "<strong>它让会话式 BI 变得安全</strong>，把问题解析为一个规范计算，而非猜测。",
  "<strong>先窄而权威地构建</strong>，由业务所有者参与，用受版本控制的定义。",
  "<strong>从避免的争议、分析师生产力与采用率度量 ROI</strong>：自助与会话式分析。",
 ],
 "conclusion_id": "conclusion",
 "conclusion_h2": "你应当记住什么？",
 "conclusion": """<p>语义层不是光鲜的采购，却是决定自助分析和会话式分析能否被信任的那块拼图。它用唯一权威来源取代几十个矛盾定义，给会话式代理一个受治理的含义去查询，并让每个答案都可经血缘解释。跳过它的组织，通常在一次昂贵的聊天机器人失败后才发现：问题从来不是模型，而是它背后未被定义的业务。</p>
<p>务实的路径不光鲜却有效：先与所有者定义有争议的指标，用受版本控制的代码表达，通过一个受治理路径连接每个消费者，并度量争议、生产力与采用率。Beehive Strategy 的平台正是建立在这种纪律之上，让向数据提问在任何地方都返回同一个可信数字。打好基础，其上的接口就不再互相打架。</p>""",
 "faq_h2": "常见问题",
 "faq": [
  ("什么是语义层？",
   "语义层是对“原始数据如何映射到业务含义”的受治理、集中式定义。它持有指标（如营收、流失）的规范定义、可切片的维度，以及表间关系，位于仓库与每个消费者之间，使任何工具都不再本地重定义指标。它是组织共享且被强制执行的词汇表。"),
  ("语义层为何对会话式 BI 重要？",
   "会话式 BI 在没有人类捕捉错误定义的情况下把问题翻译成指标，因此若定义不一致，系统会返回一个与高管所见矛盾的数字，信任崩塌。语义层把问题解析为一个规范计算和正确关系，使答案既快又可辩护，并提供让助手解释结果的血缘。"),
  ("企业应如何开始构建语义层？",
   "从引发最多争论的少数指标开始，在业务所有者参与下定义，并通过一个受治理接口发布。使用受版本控制、声明式的定义，并对照黄金集做自动测试；让每个消费者经由该层而非绕过它连接，并对使用做埋点以指导下一步扩展。"),
  ("如何度量语义层的 ROI？",
   "ROI 出现在三个可度量的地方：解决指标争议所花时间、复用定义而非重建带来的分析师生产力，以及自助与会话式分析在被信任后的采用率。每月记分卡跟踪争议工单、复用占比、查询量和高管采用率，即可显示该层是否物有所值。"),
 ],
}

if __name__ == "__main__":
    rep = B.build(SLUG, EN, ZH)
    print(rep)
