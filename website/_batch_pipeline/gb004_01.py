#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gb004_lib as B

SLUG = "automated-data-cataloguing-with-ai-classification-part-2"

EN = {
 "lead": "In part two of this series, we go inside the machine: how AI classification actually assigns metadata to enterprise data assets, where it succeeds, where it silently fails, and how to design the human-in-the-loop review that keeps a catalogue trustworthy. The context from part one still applies — the scale problem is real, with enterprise data volumes typically growing 40% to 60% a year and knowledge workers spending a meaningful share of every week searching for information — but the operational question is now the one that decides whether a catalogue is an asset or a liability: how do you run classification that is accurate enough to govern, fast enough to keep pace, and honest enough to audit?",
 "sections": [
  ("the-current-landscape", "What Does the Current AI Classification Landscape Look Like?",
   """<p>Automated classification has become the default answer to catalogue maintenance because manual cataloguing simply cannot keep pace. A data team asked to tag thousands of tables, columns, files, and dashboards by hand will always fall behind the growth of the estate, and the catalogue — the very asset meant to make data findable — decays into a source of misinformation. AI classification changes the economics: models can process the entire estate in hours, assign business and technical metadata at scale, and flag what needs human judgment, shifting the human effort from doing the work to reviewing the work.</p>
<p>The technology stack has consolidated around three complementary approaches that most mature programmes now combine. Pattern-based rules remain valuable for the predictable cases — standard naming conventions, common data types, known systems of record — because they are transparent and easy to govern. Statistical and embedding-based methods generalise beyond rules, clustering similar assets by content and structure so that a new table resembling existing customer tables is proposed for customer classification even when no rule matches. Large language models bring the decisive capability: they read the semantics — column names, sample values, descriptions, and surrounding context — and assign classifications in the same vocabulary the business uses, including free-form descriptions, sensitivity labels, and ownership suggestions that rules could never produce.</p>
<p>Industry momentum reflects the shift. Analyst firms have projected that AI-enabled metadata management will become standard practice, with the majority of data catalogues incorporating automated classification and active metadata capabilities within the next few years. For the enterprises we work with across financial services, healthcare, retail, and manufacturing, the pattern is consistent: the catalogue stops being a documentation exercise and becomes a live, continuously updated map of the data estate — if, and only if, the classification pipeline is engineered with care rather than bolted on as a feature.</p>"""),
  ("key-implementation-challenges", "What Are the Key Implementation Challenges?",
   """<p>The first challenge is precision versus recall, and the direction of the error matters more than the average score. A classifier tuned to label everything will overwhelm reviewers with false positives — the review queue becomes the bottleneck it was meant to remove. A classifier tuned to label only what it is sure of will silently under-cover the estate, leaving the most obscure and often the most sensitive assets unclassified. Mature programmes set explicit targets: high precision for sensitive-data detection, where a missed label is a compliance exposure, and balanced precision and recall for business classification, where coverage matters more than perfection. In our assessments, organisations that define these targets before tuning — rather than accepting whatever the model produces — end up with review queues a fraction of the size.</p>
<p>The second challenge is vocabulary drift and organisational context. Classifiers inherit the labels they were trained on, and enterprise vocabularies are rarely stable: business units rename things, new products appear, regulations introduce new categories, and two teams may use the same term for different concepts. A classification system that cannot absorb organisational feedback — reviewers correcting labels, the corrections feeding the next iteration — will drift out of alignment with the business within months. The governance question is who owns the business glossary the classifier is trained against, and how changes to it propagate through the classification pipeline without a six-month re-implementation project.</p>
<p>The third challenge is validation and audit. A catalogue is only as trustworthy as the evidence behind its labels, and AI-generated labels need evidence attached: the model, the confidence score, the sample data that informed the classification, and the human review state. Regulators and internal auditors increasingly ask exactly this question — "how do you know this data is correctly classified as sensitive?" — and an unanswerable label is as bad as a wrong one. Organisations that instrument classification provenance from day one can defend their catalogue; those that treat labels as oracle output cannot, and they discover the gap at the worst possible moment.</p>
<p>The fourth challenge is scale and freshness. Classification is not a one-time batch job; it is a continuous process that must re-run as new assets appear and as existing assets change. Pipelines that cannot incremental-update efficiently end up either stale or prohibitively expensive, and both outcomes erode trust. The design answer is event-driven classification that triggers on schema and data change, with a cost model that keeps the always-on process affordable.</p>
<p>The fifth challenge is accountability and ownership, and it is the one most likely to sink an otherwise sound programme. Classification decisions affect who can see data, which reports are trustworthy, and what regulators are told; if no named owner can be challenged when a label is wrong, the catalogue drifts and blame diffuses. We recommend a single accountable owner for the business glossary, a clear escalation path when the model and a data steward disagree, and a quarterly review where sampled labels are checked against reality. Ownership is not bureaucracy — it is the difference between a catalogue that improves and one that quietly rots.</p>"""),
  ("how-accurate-is-ai-classification-in-practice", "How Accurate Is AI Classification in Practice?",
   """<p>The honest answer is that modern classifiers are very strong on well-defined categories and genuinely uncertain on the long tail, which is precisely why the review design matters more than the model choice. On standard categories — sensitive data types, common business domains, standard system-of-record identification — LLM-based classifiers routinely achieve precision in the mid-to-high 90s on real enterprise estates, comparable to or better than trained human annotators on the same workload. The accuracy falls off on ambiguous, novel, or context-dependent cases: a field named "amount" could be a transaction value, a limit, a balance, or an adjustment, and no model can know which without context the field itself does not carry.</p>
<p>The practical consequence is that accuracy is a property of the pipeline, not the model. The strongest designs we see combine model confidence with a stratified review strategy: high-confidence predictions flow straight to the catalogue with their evidence attached; medium-confidence predictions route to a review queue organised by category; low-confidence predictions surface to data owners, who know the business context no model has. This stratified design concentrates human effort where the model is weak, keeps the review queue manageable, and produces a catalogue whose labels carry documented confidence — the combination that makes automated classification defensible in front of auditors and business users alike.</p>
<p>It is worth quantifying the payoff. Teams that close the feedback loop — every human correction becoming a training or prompt-refinement example — typically report review effort dropping by 50% to 70% after two to three cycles, because the model learns the organisation's vocabulary and edge cases. Accuracy, in other words, is something you engineer into the loop, not something you buy from a vendor and forget.</p>"""),
  ("practical-approaches-that-work", "Which Practical Approaches Actually Work?",
   """<p>Design the classification pipeline as a learning system, not a one-off model run. The pipeline should include a feedback loop by default: every human correction in the review queue becomes a training or prompt-refinement example for the next iteration, so accuracy improves continuously on the categories that matter to your organisation. We treat this as the single most important design decision, ahead of model selection, because it is what makes the system get better instead of getting worse.</p>
<p>Run sensitive-data detection as a separate, stricter track. Business classification can tolerate a label being refined later; sensitivity classification cannot. Detect personal data, financial data, and regulated categories with a dedicated model and rule combination, set the precision threshold high, and require human confirmation for anything touching regulated categories. This separation of concerns — a permissive general classifier and a conservative sensitive-data detector — is the design that keeps the catalogue both useful and compliant, and it is the pattern we recommend to every regulated client.</p>
<p>Connect the catalogue to how data is actually governed and consumed. Classification creates metadata; the value is realised when that metadata drives behaviour: access decisions, retention rules, privacy reviews, and — critically — the analytics experience. At Beehive Strategy we connect governed catalogues to conversational analytics, so the classification work pays off where users feel it: the business user asking a natural-language question receives answers built from assets that are correctly classified, quality-tagged, and access-controlled, with lineage back to the source. When the catalogue and the analytics layer share one governed semantic foundation, automated classification stops being an IT hygiene project and becomes the reason data is findable, trusted, and safe to use.</p>
<p>Measure the catalogue like a product. Track coverage (share of assets classified), precision (sampled label accuracy), review throughput, and time-to-classify for new assets. These four numbers, reviewed monthly, tell you far more about catalogue health than any vendor dashboard, and they make the next tuning cycle a decision rather than a guess.</p>"""),
 ],
 "takeaways_id": "key-takeaways",
 "takeaways_h2": "What Are the Key Takeaways?",
 "takeaways_intro": "Five takeaways capture the pattern that separates catalogues teams trust from catalogues they quietly route around.",
 "takeaways": [
  "<strong>Set precision and recall targets per category.</strong> Sensitivity detection demands high precision; business classification needs balanced coverage, and mixing the two is the most common cause of unusable review queues.",
  "<strong>Design for the long tail.</strong> Stratify review by confidence so human effort concentrates where models are weak rather than where they are already right.",
  "<strong>Close the feedback loop.</strong> Every human correction should improve the next iteration; review effort drops by half or more within a quarter when this is wired in.",
  "<strong>Separate the sensitive-data track.</strong> A conservative, human-confirmed detector protects compliance while the general classifier stays permissive and useful.",
  "<strong>Attach evidence to every label.</strong> Model, confidence, sample data, and review state make the catalogue defensible in front of auditors and regulators.",
 ],
 "conclusion_id": "conclusion",
 "conclusion_h2": "What Should You Take Away?",
 "conclusion": """<p>Automated data cataloguing with AI classification works when it is engineered as a governed learning system rather than deployed as a black box. The models are genuinely capable — mid-90s precision on well-defined categories — but the value is captured in the pipeline: explicit targets, stratified review, closed feedback loops, and evidence attached to every label. The organisations that treat classification as a continuous, auditable process end up with a catalogue their people actually use; the ones that treat it as a one-time tagging sprint end up, eighteen months later, exactly where they started.</p>
<p>The practical takeaway for a data leader is unglamorous but decisive: do not buy a classifier and declare victory. Fund the pipeline, the glossary, the feedback loop, and the audit trail, and measure them. That is what turns automated cataloguing from a slide in a strategy deck into a system your organisation trusts enough to govern with.</p>
<p>In the next part of this series we turn to the organisational side: how to operationalise the catalogue, measure its impact, and connect it to the governance, access, and analytics workflows that turn metadata into business value. At Beehive Strategy we help enterprises build the whole chain — AI classification feeding a governed catalogue that powers conversational analytics — so that the data estate becomes findable, trustworthy, and safe, at a pace manual methods could never sustain.</p>""",
 "faq_h2": "Frequently Asked Questions",
 "faq": [
  ("What is AI classification in a data catalogue?",
   "AI classification is the use of machine learning — including rules, embedding models, and large language models — to automatically assign metadata such as business domain, data type, sensitivity, and ownership to data assets like tables, columns, files, and dashboards. It lets a catalogue stay current as the data estate grows, shifting human effort from tagging everything to reviewing the cases the model is unsure about."),
  ("How accurate is AI data classification in practice?",
   "On well-defined categories such as common sensitive-data types, standard business domains, and system-of-record identification, modern LLM-based classifiers typically reach precision in the mid-to-high 90s on real enterprise estates, comparable to trained human annotators. Accuracy falls on ambiguous or novel cases, which is why a stratified human review design matters more than the model choice itself."),
  ("Why should sensitive-data detection be a separate track?",
   "Sensitivity labels carry compliance and legal risk that a wrong business-domain tag does not. A missed sensitive-data label is an exposure, while a delayed business label is merely inconvenient. Running detection as a stricter, high-precision, human-confirmed track keeps the catalogue compliant while the general classifier stays permissive and useful."),
  ("How do you keep a classified catalogue trustworthy over time?",
   "Treat classification as a continuous, learning process: attach evidence to every label (model, confidence, sample data, review state), route low-confidence predictions to human reviewers, feed every correction back into the next iteration, and re-classify on data and schema change. Reviewing coverage, precision, and review throughput monthly keeps the catalogue defensible and current."),
 ],
}

ZH = {
 "lead": "在本系列的第二部分，我们深入系统内部：AI 分类实际上如何为企业数据资产分配元数据、它在哪里表现优异、在哪里会悄然失误，以及如何设计人机协同的审核机制让数据目录保持可信。第一部分的背景仍然成立——规模问题是真实的，企业数据量通常每年增长 40% 到 60%，知识工作者每周都要花相当多的时间寻找信息——但现在真正决定数据目录是资产还是负担的操作性问题是：你如何运行一种既足够准确以用于治理、足够快速以跟上节奏、又足够透明以接受审计的分类？",
 "sections": [
  ("the-current-landscape", "当前的 AI 分类格局是怎样的？",
   """<p>自动化分类之所以成为数据目录维护的默认答案，是因为人工编目根本跟不上节奏。让数据团队手动为数千张表、列、文件和仪表板打标签，永远会落后于数据资产的增长，而目录——本应让数据可被发现的资产——会退化成错误信息的来源。AI 分类改变了成本结构：模型可以在数小时内处理整个数据资产，规模化地分配业务和技术元数据，并标记出需要人工判断的内容，把人力从“做标注”转移到“审核标注”。</p>
<p>技术栈已经围绕三种互补的方法收敛，成熟的团队通常会把它们组合起来。基于规则的模式匹配在可预测的场景中仍然很有价值——标准命名规范、常见数据类型、已知的记录系统——因为它们透明且易于治理。基于统计和向量的方法超越了规则，能够按内容和结构对相似资产聚类，因此一张与现有客户表相似的新表会被建议归类为“客户”，即使没有规则匹配。大语言模型带来了决定性的能力：它们能读懂语义——列名、样本值、描述和上下文——并用业务实际使用的词汇进行分类，包括自由描述、敏感度标签，以及规则永远无法生成的归属建议。</p>
<p>行业的势头反映了这种转变。分析机构预测，AI 赋能的元数据管理将成为标准实践，未来几年内大多数数据目录都会纳入自动化分类和主动元数据能力。在我们服务的金融、医疗、零售和制造业客户中，规律是一致的：目录不再是一份文档工作，而成为数据资产实时、持续更新的地图——前提是，且仅当，分类流水线是被精心设计的，而不是被当作一个功能简单叠加。</p>"""),
  ("key-implementation-challenges", "关键的实施挑战有哪些？",
   """<p>第一个挑战是精确率与召回率的权衡，而错误的方向比平均分数更关键。一个被调成“什么都打标签”的分类器会用大量误报淹没审核者——审核队列变成了它本应消除的瓶颈。一个只给确定内容打标签的分类器则会悄然漏掉大批资产，把最冷门、往往也最敏感的资产留在未分类状态。成熟的团队会设定明确的目标：对敏感数据检测要求高精确率（漏标就是合规敞口），对业务分类要求精确率和召回率平衡（覆盖率比完美更重要）。在我们的评估中，那些在调优前就定义好目标、而不是接受模型默认输出的组织，最终的审核队列规模只有几分之一。</p>
<p>第二个挑战是词汇漂移和组织上下文。分类器继承的是训练时所用的标签，而企业词汇很少稳定：业务单元会重命名，新产品会出现，法规会引入新类别，两个团队可能用同一个词表达不同概念。一个无法吸收组织反馈的分类系统——审核者修正标签、修正内容反馈到下一次迭代——会在几个月内与业务脱节。治理问题是：谁拥有分类器所依据的业务词汇表，词汇表的变更如何在不重启半年实施项目的情况下传导到分类流水线。</p>
<p>第三个挑战是验证与审计。目录的可信度只取决于标签背后的证据，而 AI 生成的标签需要附带证据：模型、置信度分数、影响分类的样本数据，以及人工审核状态。监管者和内部审计者越来越频繁地问一个确切的问题——“你如何确认这条数据被正确归类为敏感？”——一个无法回答的标签和错误的标签一样糟糕。从第一天起就为分类来源建立可追溯机制的组织能够捍卫自己的目录；把标签当作神谕输出的组织则不能，而且它们会在最糟糕的时刻才发现这个缺口。</p>
<p>第四个挑战是规模与时效性。分类不是一次性的批处理任务，而是一个必须随新资产出现、随现有资产变化而持续运行的流程。无法高效增量更新的流水线最终要么过时、要么成本高到无法承受，两种结果都会侵蚀信任。设计的答案是事件驱动的分类：在 schema 和数据变化时触发，并以可负担的成本模型支撑常驻运行。</p>"""),
  ("how-accurate-is-ai-classification-in-practice", "AI 数据分类在实际中有多准确？",
   """<p>诚实的答案是：现代分类器在定义清晰的类别上非常强，在长尾上则确实不确定，而这正是为什么审核设计比模型选择更重要。在标准类别上——敏感数据类型、常见业务域、标准记录系统识别——基于大语言模型的分类器在真实企业资产上通常能达到中高 90 分的精确率，与训练有素的人工标注者在同一工作量上相当或更好。准确率会在模糊、新颖或依赖上下文的案例中下降：一个名为“amount”的字段可能是交易金额、限额、余额或调整项，而模型在字段本身不携带上下文时无法判断是哪一种。</p>
<p>实际的结果是：准确率流水线的属性，而非模型的属性。我们见过最强的设计把模型置信度与分层审核策略结合起来：高置信度的预测直接流入目录并附带证据；中等置信度的预测进入按类别组织的审核队列；低置信度的预测提交给数据负责人，他们掌握模型所没有的业务上下文。这种分层设计把人力集中在模型薄弱处，保持审核队列可控，并产出带可证明置信度的标签——这正是让自动化分类在监管者和业务用户面前都站得住脚的组合。</p>
<p>值得量化这个回报。那些闭环反馈的组织——每一次人工修正都成为训练或提示优化的样本——通常在两到三个周期后报告审核工作量下降 50% 到 70%，因为模型学会了组织的词汇和边界案例。换句话说，准确率是你在循环中“工程化”出来的，而不是从供应商那里买来就忘的。</p>"""),
  ("practical-approaches-that-work", "哪些实践方法真正有效？",
   """<p>把分类流水线设计成一个学习型系统，而不是一次性的模型运行。流水线默认应包含反馈闭环：审核队列中的每一次人工修正都成为下一次迭代的训练或提示优化样本，从而在你组织关心的类别上持续提升准确率。我们把这视为最重要的设计决策，优先于模型选择，因为它决定了系统是变得更好还是更差。</p>
<p>把敏感数据检测作为一条独立、更严格的轨道运行。业务分类可以容忍标签稍后 refinement；敏感度分类不能。用专门的模型和规则组合检测个人数据、财务数据和受监管类别，把精确率阈值设高，并对任何触及受监管类别的内容要求人工确认。这种职责分离——一个宽松的通用分类器加一个保守的敏感数据检测器——是让目录既好用又合规的设计，也是我们向每个受监管客户推荐的模式。</p>
<p>把目录连接到数据实际被治理和消费的方式。分类产生元数据；只有当元数据驱动行为时价值才实现：访问决策、留存规则、隐私审查，以及——关键的——分析体验。在 Beehive Strategy，我们把受治理的目录连接到会话式分析，让分类工作的回报体现在用户能感知的地方：提出自然语言问题的业务用户得到的答案，来自被正确分类、打了质量标签、受访问控制约束、并可追溯到源头的资产。当目录和分析层共享同一个受治理的语义基础时，自动化分类就不再是一次 IT 卫生项目，而成为数据可被发现、可信、安全使用的理由。</p>
<p>像对待产品一样度量目录。跟踪覆盖率（已分类资产占比）、精确率（抽样标签准确率）、审核吞吐量和新资产的分类耗时。这四项数字按月审视，比任何供应商仪表盘都能说明目录健康度，并让下一次调优成为决策而非猜测。</p>"""),
 ],
 "takeaways_id": "key-takeaways",
 "takeaways_h2": "关键要点是什么？",
 "takeaways_intro": "五个要点概括了那些被团队信任的目录与那些被悄悄绕开的目录之间的区别。",
 "takeaways": [
  "<strong>按类别设定精确率和召回率目标。</strong>敏感检测要求高精确率；业务分类需要平衡覆盖，把两者混为一谈是审核队列不可用的最常见原因。",
  "<strong>为长尾而设计。</strong>按置信度分层审核，让人力集中在模型薄弱处，而不是已经正确的地方。",
  "<strong>闭环反馈。</strong>每一次人工修正都应改进下一次迭代；接上闭环后，一个季度内审核工作量下降一半以上。",
  "<strong>分离敏感数据轨道。</strong>一个保守、需人工确认的检测器保护合规，而通用分类器保持宽松和有用。",
  "<strong>为每个标签附带证据。</strong>模型、置信度、样本数据和审核状态，让目录在监管者和审计者面前站得住脚。",
 ],
 "conclusion_id": "conclusion",
 "conclusion_h2": "你应当记住什么？",
 "conclusion": """<p>基于 AI 分类的自动化数据编目，只有在被设计成一个受治理的学习系统时才能发挥作用，而不是作为一个黑盒部署。模型确实有能力——在定义清晰的类别上达到中高 90 分精确率——但价值是在流水线中被捕获的：明确的目标、分层审核、闭环反馈，以及为每个标签附带证据。把分类当作持续、可审计流程的组织，最终会得到一个人们真正使用的目录；把它当作一次性打标冲刺的组织，十八个月后会发现自己又回到了起点。</p>
<p>在本系列的下一部分，我们转向组织层面：如何把目录运营化、度量其影响，并将其连接到把元数据转化为业务价值的治理、访问和分析工作流。在 Beehive Strategy，我们帮助企业构建整条链路——AI 分类为受治理的目录供能，目录再驱动会话式分析——让数据资产以人工方法永远无法维持的节奏，变得可被发现、可信且安全。</p>""",
 "faq_h2": "常见问题",
 "faq": [
  ("什么是数据目录中的 AI 分类？",
   "AI 分类是指利用机器学习（包括规则、向量模型和大型语言模型）自动为表、列、文件和仪表板等数据资产分配业务域、数据类型、敏感度和归属等元数据。它让目录能随数据资产增长而保持更新，把人力从“给所有东西打标签”转移到“审核模型不确定的案例”。"),
  ("AI 数据分类在实际中有多准确？",
   "在敏感数据类型、标准业务域、记录系统识别等定义清晰的类别上，现代基于大语言模型的分类器在真实企业资产上通常能达到中高 90 分的精确率，与训练有素的人工标注者相当。在模糊或新颖案例上准确率会下降，所以分层人工审核的设计比模型选择本身更重要。"),
  ("为什么敏感数据检测应作为独立轨道？",
   "敏感度标签带有合规与法律风险，而错误的业务域标签没有。漏掉一个敏感标签是敞口，而延迟一个业务标签只是不便。把检测作为一条更严格、高精确率、需人工确认的轨道，能在通用分类器保持宽松有用的同时保护合规。"),
  ("如何让分类后的目录长期保持可信？",
   "把分类当作持续的学习过程：为每个标签附带证据（模型、置信度、样本数据、审核状态），把低置信度预测交给人工审核，把每次修正反馈到下一次迭代，并在数据和 schema 变化时重新分类。按月审视覆盖率、精确率和审核吞吐量，让目录保持可辩护和最新。"),
 ],
}

if __name__ == "__main__":
    rep = B.build(SLUG, EN, ZH)
    print(rep)
