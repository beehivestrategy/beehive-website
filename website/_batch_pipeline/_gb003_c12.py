#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gbatch_003 slug 12 — ai-driven-customer-segmentation-retailers
Source article was padded with repeated statistic sentences (9x) and the zh body
contained untranslated English fragments => all three bodies rewritten cleanly."""
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb003_lib import process, stats
from _gb001_s2t import s2tw

SLUG = 'ai-driven-customer-segmentation-retailers'

EN_BODY = '''<p class="article-lead">AI-driven customer segmentation for retail has changed shape in 2026. Mature models, standardised data integration through the Model Context Protocol (MCP), and rising regulatory expectations have moved segmentation from a quarterly analytics exercise to a live capability: dynamic, behaviour-based segments that update as customers move, feed personalisation engines directly, and stay explainable to the teams that use them. For retail CMOs and customer analytics leaders, the question is no longer whether to adopt it but how to deploy it without creating operational chaos.</p>
<div class="article-tldr">
<p><strong>Key Insight:</strong> AI-driven segmentation improves campaign conversion rates by 35 to 45 percent, and retailers using it report roughly 28 percent higher customer lifetime value. The mechanism is cadence as much as accuracy: dynamic segments update in real time, while traditional approaches refresh quarterly — by which time the customer\'s behaviour has already changed.</p>
</div>
<h2 id="why-static-customer-segments-are-failing">Why Are Static Customer Segments Failing Retailers?</h2>
<p>Static segmentation sorts customers into demographic or RFM buckets and refreshes them on a reporting calendar. It worked when the customer relationship was stable and the number of channels was small. It fails now for three structural reasons, and none of them can be fixed by refreshing more often.</p>
<p>First, the cadence is wrong. A customer who lapsed nine days ago is invisible to a quarterly refresh, and a customer who just made their third purchase in a month is still being treated as a one-time buyer. The segment describes who the customer was at the last refresh, and the offer is built on that description. Second, the segments are not action-mapped: a bucket labelled "high value 25 to 34" does not tell a merchant what to do next, so the segment gets used for reporting rather than for decisions. Third, identity is fragmented — the same customer appears as two people because online and in-store purchases were never reconciled, which halves their apparent value and doubles the messages they receive.</p>
<p>The cost shows up in the two places retailers feel most: wasted discount, because offers go to customers who would have paid full price, and trust erosion, because customers receive win-back campaigns for products they bought last week in another channel. Meanwhile the upside for getting it right is well documented — personalisation built on AI segments drives around a 20 percent revenue increase, and Epsilon\'s research found that 80 percent of consumers are more likely to purchase when brands offer personalised experiences. Salesforce\'s connected-customer research puts the expectation side at 76 percent of customers expecting companies to understand their needs.</p>
<h2 id="which-ai-approaches-power-dynamic-segmentation">Which AI Approaches Power Dynamic Segmentation?</h2>
<p>Three techniques do the work, and the order in which they are applied matters more than the choice between them.</p>
<ul>
<li><strong>Clustering for discovery.</strong> K-means, DBSCAN, or hierarchical clustering over behavioural features reveals how many genuinely distinct groups exist in the base. Clustering is unstable across runs and hard to explain, so it belongs in the design phase: it tells you how many segments to build, not which customer belongs to which.</li>
<li><strong>Propensity and value models for assignment.</strong> Gradient-boosted models predict churn risk, category affinity, discount sensitivity, and predicted value. Because they output a score, thresholds can be set differently per channel without rebuilding anything, and the score can be explained in terms of the features that drove it.</li>
<li><strong>Sequence models where order matters.</strong> For grocery baskets, subscription curation, and browse-to-purchase paths, sequence models capture patterns that static features miss. For general merchandise, the incremental accuracy rarely justifies the engineering and explainability cost.</li>
</ul>
<p>The practical result is that AI identifies roughly three times more micro-segments than traditional methods — not because retailers should run three times as many campaigns, but because the model can see distinctions the RFM grid averages away. Those distinctions are valuable when they map to a different action. They are noise when they do not, which is why the next section on operating model matters as much as the modelling.</p>
<h2 id="how-should-retailers-integrate-data-for-segmentation-intelligence">How Should Retailers Integrate Data for Segmentation Intelligence?</h2>
<p>Segmentation quality is bounded by integration quality. Five sources carry most of the signal, and the combination is what makes the difference: point-of-sale transactions, loyalty activity, digital engagement (web, app, email), returns and service interactions, and external context such as weather and local events. MCP integration is what makes combining POS, loyalty, and digital engagement data tractable at enterprise scale: instead of building a bespoke connector for every system and re-implementing access control in each one, the retailer exposes governed data through a standard protocol and applies authentication, authorisation, masking, and logging once.</p>
<p>Two prerequisites sit underneath. Identity resolution must reconcile online and in-store behaviour to one customer, or every downstream number is wrong. And consent status must travel with the data — recorded per purpose, enforced at query time — so a segment built for service improvement cannot quietly be used for acquisition. Retailers that skip these two steps discover them during the first compliance review, by which time the segmentation logic has to be rebuilt rather than corrected.</p>
<h2 id="how-do-retailers-turn-segments-into-personalised-experiences">How Do Retailers Turn Segments Into Personalised Experiences?</h2>
<p>A segment creates value only at the moment it changes what a customer experiences. Five activation points matter, and each has a different latency requirement.</p>
<ol>
<li><strong>Offer and discount engines.</strong> The segment sets the ceiling on discount depth — full price for loyal, low-risk customers; retention investment for high-value customers showing lapse signals.</li>
<li><strong>On-site and in-app personalisation.</strong> Real-time scoring, because the session is happening now.</li>
<li><strong>Email and push audiences.</strong> Nightly rebuilds are sufficient and far cheaper.</li>
<li><strong>Store clienteling.</strong> The segment must reach the associate\'s device with a plain-language reason attached, or it will not be used.</li>
<li><strong>Paid media.</strong> Suppress existing high-value customers from acquisition spend and build lookalikes from predicted rather than historical value.</li>
</ol>
<p>Guardrails keep this safe: hard caps on discount exposure, mandatory approval above a threshold, and a permanent randomised holdout so the incremental effect can be measured rather than assumed. Then give merchants a way to interrogate the segments directly — when a category manager can ask "which high-value customers are trending toward lapse in this region this week?" in the messaging tool they already use, and receive a governed, real-time answer, segmentation stops being a quarterly deliverable and becomes part of how decisions get made.</p>
<h2 id="what-does-a-90-day-segmentation-deployment-look-like">What Does a 90-Day Segmentation Deployment Look Like?</h2>
<p>A focused first deployment fits into thirteen weeks if the scope is one category or one use case.</p>
<ul>
<li><strong>Weeks 1–3.</strong> Choose the use case — retention is the most forgiving — resolve identity for the population in scope, and baseline current conversion, retention, discount spend, and margin per customer.</li>
<li><strong>Weeks 4–7.</strong> Build the feature layer and models, then evaluate against held-out customers rather than historical cohorts. Involve merchants weekly; they know which distinctions are actionable.</li>
<li><strong>Weeks 8–10.</strong> Activate in one channel against a randomised control group, with guardrails on discount exposure.</li>
<li><strong>Weeks 11–13.</strong> Measure incremental margin, not engagement. Decide whether to extend coverage or narrow scope, and document the semantic definitions so the next segment inherits them.</li>
</ul>
<p>Organisations that follow this pattern typically see measurable results within 90 days and, more importantly, end the quarter with an architectural foundation — governed definitions, a working control group, and an activation path — that makes every subsequent segment cheaper to deploy.</p>
<h2 id="how-do-you-keep-micro-segments-from-becoming-unmanageable">How Do You Keep Micro-Segments From Becoming Unmanageable?</h2>
<p>Three times more micro-segments is an operational risk before it is an opportunity. Three disciplines keep the number useful.</p>
<p>First, the decision test: a segment exists only if it maps to a distinct action with an owner. If two segments trigger the same campaign, merge them. Second, a quarterly pruning review: retire segments with no activations in the period, because unused segments accumulate silently and make every downstream report harder to read. Third, a single governed definition per segment — one place where the logic, the owner, the refresh cadence, and the access rules live, consumed by every channel rather than copied into each.</p>
<p>The payoff of that discipline is explainability. When a campaign underperforms, the question "why was this customer in this segment?" must have an answer a merchant can act on, and that is only possible if segments are defined as rules over model scores rather than emitted as raw model output.</p>
<h2 id="how-do-you-measure-the-return-on-segmentation">How Do You Measure the Return on Segmentation?</h2>
<p>The headline numbers are the reason the business case gets approved: AI-driven segmentation improves campaign conversion rates by 35 to 45 percent, retailers using it report roughly 28 percent higher customer lifetime value, and personalisation built on those segments drives around a 20 percent revenue increase. But those are outcomes of measurement discipline, not replacements for it.</p>
<p>Track three tiers. Operational metrics: refresh latency, segment coverage, activation rate by channel. Business metrics: conversion lift, margin per customer, discount spend per retained customer — measured against the holdout, not against last quarter. Strategic metrics: share of campaigns running on governed segments, and time from segment definition to activation. Baseline all three before launch. Without the baseline and the control group, the 35 to 45 percent figure is an industry average, not a claim the retailer can make about its own programme — and the first time a CFO asks for attribution, the difference matters.</p>
<h2 id="should-retailers-build-or-buy-segmentation-capability">Should Retailers Build or Buy Their Segmentation Capability?</h2>
<p>The decision is not all-or-nothing, and splitting it correctly is usually the difference between a capability that arrives this quarter and one that arrives next year. The test is whether a competitor would build the component the same way.</p>
<p>What is genuinely specific to the retailer — the metric definitions, the category logic, the workflow integration, the thresholds that reflect its margin structure — must be built, because it encodes commercial judgement nobody else has. What is commodity — the governed access layer, the connectors, the permission model, the query interface — should be bought, because every retailer needs the same thing and building it consumes data engineering capacity that is already contested.</p>
<p>A managed approach shortens the calendar substantially: the governed data-access layer, monitoring, and audit can be stood up in roughly two weeks, without rebuilding the warehouse, and business teams get real-time answers from governed data through the tools they already use. The second-order effect matters more than the first deployment, because every quarter not spent building commodity infrastructure is a quarter spent on the decisions that create value.</p>
<h2 id="what-governance-and-privacy-rules-apply-to-retail-segmentation">What Governance and Privacy Rules Apply to Retail Segmentation?</h2>
<p>Four obligations shape a retail segmentation programme, and all four are easier to satisfy when they are encoded in the data layer rather than written in a policy document.</p>
<ul>
<li><strong>Purpose limitation.</strong> Data collected for service or fulfilment cannot automatically be used for marketing. Consent and purpose must travel with the data and be enforced at query time, so a segment built for one purpose cannot be repurposed by an analyst who did not check.</li>
<li><strong>Minimisation.</strong> Collect and retain only the fields the segmentation actually needs. Every extra attribute is exposure without benefit, and most segment models perform well on a short feature list.</li>
<li><strong>Access control with role filtering.</strong> A store associate querying segments should see only their store's customers; a regional manager only their region. Enforced at the data layer rather than in the application, because application-level rules are bypassed by the next integration.</li>
<li><strong>Auditability.</strong> Record which segment definition was used, by whom, for which campaign, and on which date. When a customer asks why they received an offer, the answer must be reconstructable months later.</li>
</ul>
<p>Handled this way, governance makes segmentation faster rather than slower: once the controls exist at the access layer, each new segment inherits them, and the marginal compliance cost of the next campaign approaches zero.</p>
<h2 id="which-mistakes-undermine-retail-segmentation-programs">Which Mistakes Undermine Retail Segmentation Programmes?</h2>
<p>Five patterns account for most programmes that stall, and each has an early warning sign that appears well before the results do.</p>
<ul>
<li><strong>Segment sprawl.</strong> New segments are added and none are retired, so operations drown. Warning sign: a segment list that grows every quarter and no record of last activation dates.</li>
<li><strong>Refresh without activation.</strong> Segments update in real time but feed only a dashboard. Warning sign: high segment coverage and no change in campaign construction.</li>
<li><strong>No control group.</strong> Lift is reported against last quarter, so seasonality is mistaken for segmentation. Warning sign: conversion improvements that appear in every campaign regardless of targeting.</li>
<li><strong>Identity left unresolved.</strong> The same customer receives contradictory offers through two channels. Warning sign: customer complaints about irrelevant or duplicated messages.</li>
<li><strong>Model-first scoping.</strong> The project starts by choosing an algorithm instead of choosing a decision. Warning sign: a data science workplan with no named business owner.</li>
</ul>
<p>Every one of these is cheaper to prevent than to fix, and all five share the same remedy: decide first what action will change, then build only the segmentation that action requires.</p>
'''

EN_FAQ = [
    ('What is AI-driven customer segmentation in retail?',
     'It is the practice of grouping customers continuously by behaviour — recency, frequency, category affinity, channel mix, returns, engagement trend — using machine learning, rather than sorting them periodically into demographic or RFM buckets. The segments update as behaviour changes, they are far more granular than manual grids, and each one is mapped to a specific action. Retailers using AI-driven segmentation report roughly 28 percent higher customer lifetime value and campaign conversion improvements of 35 to 45 percent, primarily because the offer is built on current behaviour rather than a quarterly snapshot.'),
    ('How is dynamic segmentation different from traditional RFM segmentation?',
     'RFM is a static grid recalculated on a reporting cycle, so the customer is described as they were at the last refresh. Dynamic segmentation scores customers continuously and reassigns them as events arrive, which is what makes real-time personalisation possible. RFM also cannot incorporate engagement, browsing, or returns signals, so it systematically misreads new customers with thin purchase history. The practical difference is cadence: dynamic segments update in real time, traditional approaches quarterly, and customer behaviour changes in between.'),
    ('What data is needed to start AI segmentation for retail?',
     'Start with two years of transaction history including order lines, returns, and margin, plus loyalty identifiers. Add digital engagement (web, app, email), service interactions, and external context such as weather to improve accuracy on newer customers. The two prerequisites that matter more than volume are identity resolution across online and in-store channels, and consent status recorded per purpose and enforced at query time. Without identity resolution, one customer appears as two and every value figure is wrong.'),
    ('How many segments should a retailer run?',
     'As many as there are distinct actions, and no more — typically five to twelve in production. AI identifies roughly three times more micro-segments than traditional methods, but that is a discovery capability rather than a campaign plan. Apply a decision test: if two segments trigger the same treatment, merge them. Then prune quarterly, retiring any segment with no activations, and keep one governed definition per segment so every channel reads the same logic.'),
    ('How long does it take to deploy AI segmentation and see results?',
     'A focused deployment on one category or use case takes about thirteen weeks: three weeks for identity resolution and baselining, four weeks for feature and model development, three weeks to activate against a control group, and three weeks to measure. Measurable movement in conversion and margin typically appears within that window. Enterprise-wide coverage across categories and channels is a twelve to eighteen month programme, sequenced by decision value, with each phase inheriting the definitions and controls built in the first.'),
]

ZH_BODY = '''<p class="article-lead">2026年，零售业的AI驱动客户细分已经改变了形态。成熟模型、以模型上下文协议（MCP）为代表的标准化数据集成方式，以及不断提高的监管期望，共同把细分从"按季度跑一次的分析任务"变成了实时能力：随客户行为变化而更新的动态细分，直接驱动个性化引擎，并且能向使用它的团队解释清楚。对零售首席营销官与客户分析负责人来说，问题不再是要不要采用，而是如何在不制造运营混乱的前提下把它落地。</p>
<div class="article-tldr">
<p><strong>关键洞察：</strong>AI驱动的细分可将营销活动转化率提升35%到45%，采用它的零售商报告的客户生命周期价值高出约28%。机制不仅在于更准确，更在于节奏：动态细分实时更新，而传统方法按季度刷新——等到刷新时，客户的行为早就变了。</p>
</div>
<h2 id="为什么静态客户细分正在失败">为什么静态客户细分正在失败？</h2>
<p>静态细分把客户按人口统计或RFM分桶，并按报表周期刷新。在客户关系稳定、渠道数量有限的年代，这种做法是有效的。今天它失效有三个结构性原因，而且没有一个是靠"刷新得更频繁"能解决的。</p>
<p>第一，节奏错位。一位九天前流失的客户，在季度刷新中是不可见的；一位刚刚完成本月第三次购买的客户，仍被当作一次性买家对待。细分描述的是客户在上次刷新时的样子，而优惠正是基于这个描述生成的。第二，细分没有映射到动作：一个标着"高价值25到34岁"的分桶，并不能告诉商品经理下一步该做什么，于是这个细分只被用于出报表，而不是用于做决策。第三，身份是碎裂的——同一位客户因为线上与门店购买从未打通而变成两个人，结果是价值被低估一半，而收到的营销信息多了一倍。</p>
<p>成本集中在零售商最有体感的两个地方：一是折扣浪费，优惠发给了本来就会原价购买的人；二是信任损耗，客户在另一个渠道刚买过的商品，这边又收到了召回活动。而做对的收益同样有据可查：建立在AI细分之上的个性化可带来约20%的收入增长；Epsilon的研究显示80%的消费者在品牌提供个性化体验时更愿意购买；Salesforce的调研则表明76%的客户期望企业理解自己的需求。</p>
<h2 id="动态细分的ai方法">动态细分的AI方法有哪些？</h2>
<p>有三类技术在发挥作用，而它们的应用顺序比选择哪一种更重要。</p>
<ul>
<li><strong>用聚类做发现。</strong>对行为特征运行k-means、DBSCAN或层次聚类，可以揭示客群中真实存在多少个不同群体。聚类结果在多次运行之间不稳定，也难以向业务解释，因此它属于设计阶段：它告诉你应该构建多少个细分，而不是某位客户属于哪一个。</li>
<li><strong>用倾向性与价值模型做归属。</strong>梯度提升模型预测流失风险、品类偏好、价格敏感度与客户价值。由于输出的是分数，各渠道可以设置不同阈值而无需重建模型，而且这个分数可以用驱动它的特征来解释。</li>
<li><strong>在顺序有意义的地方使用序列模型。</strong>对于生鲜购物篮、订阅制选品、以及"浏览到购买"的路径，序列模型能捕捉静态特征遗漏的模式。对于一般商品零售，由此带来的准确度提升通常不足以抵消工程与可解释性成本。</li>
</ul>
<p>实际结果是，AI能识别出比传统方法多约三倍的微细分——这并不是说零售商应该多开三倍的活动，而是模型能看到RFM网格被平均掉的差异。当这些差异对应不同的动作时，它们就有价值；当不对应时，它们只是噪声。这也正是为什么运营模型与建模同等重要。</p>
<h2 id="细分智能的数据集成">如何为细分智能打通数据集成？</h2>
<p>细分质量的上限由集成质量决定。五类数据源承载了绝大部分信号，而真正的差异来自它们的组合：POS交易、会员活动、数字互动（Web、App、邮件）、退货与客服交互，以及天气与本地事件等外部背景。MCP集成让"打通POS、会员与数字互动数据"在企业级规模上变得可行：零售商不必为每个系统定制连接器、也不必在每个系统里重复实现访问控制，而是通过标准协议暴露受治理的数据，把认证、授权、脱敏与留痕一次性做好。</p>
<p>其下还有两项前提。一是身份打通，必须把线上与门店行为归集到同一个客户，否则所有下游数字都是错的。二是授权状态要随数据流转——按用途记录、在查询时执行——使为服务改善构建的细分不会在不知不觉中被用于拉新。跳过这两步的零售商，往往在第一次合规评审时才发现问题，而此时细分逻辑已经不是修正，而是要推倒重建。</p>
<h2 id="从细分到个性化体验">如何从细分走向个性化体验？</h2>
<p>细分只有在改变客户体验的那一刻才创造价值。五个激活点很重要，且各自的时效要求不同。</p>
<ol>
<li><strong>优惠与折扣引擎。</strong>细分决定折扣力度的上限——对忠诚且低流失风险的客户给原价，对出现流失信号的高价值客户投入留存资源。</li>
<li><strong>站内与App内个性化。</strong>需要实时打分，因为会话正在发生。</li>
<li><strong>邮件与推送人群。</strong>每晚重建即可，成本低得多。</li>
<li><strong>门店导购。</strong>细分必须连同通俗解释一起到达导购的设备上，否则不会被使用。</li>
<li><strong>付费媒介。</strong>把已有高价值客户从拉新投放中排除，并基于预测价值而非历史价值构建相似人群。</li>
</ol>
<p>护栏保证安全：折扣敞口设上限、超过阈值强制审批、以及永久保留随机对照组，使增量效果可以被衡量而不是被假设。此外，要给商品团队直接查询细分的通道——当品类经理能在自己已在使用的即时通讯工具里问出"本区域本周有哪些高价值客户正在走向流失？"并得到受治理的实时答案时，细分就不再是一份季度交付物，而成为决策方式的一部分。</p>
<h2 id="90天落地计划">90天细分落地计划是什么样？</h2>
<p>如果范围限定在一个品类或一个用例，首次部署可以在十三周内完成。</p>
<ul>
<li><strong>第1到3周。</strong>选定用例（留存的容错空间最大），完成范围内人群的身份打通，并为当前转化率、留存率、折扣支出与单客毛利建立基线。</li>
<li><strong>第4到7周。</strong>构建特征层与模型，并用留出客户而非历史人群做验证。每周与商品团队对齐，因为他们知道哪些差异是可执行的。</li>
<li><strong>第8到10周。</strong>在单一渠道带随机对照组上线，并设置折扣敞口护栏。</li>
<li><strong>第11到13周。</strong>衡量增量毛利，而不是互动指标。决定扩大覆盖还是收窄范围，并把语义定义沉淀下来，让下一个细分可以直接继承。</li>
</ul>
<p>按这个节奏推进的组织，通常在90天内就能看到可度量的结果；更重要的是，季度结束时它们拥有了一套架构基础——受治理的定义、可用的对照组、以及一条激活通路——使之后每一个细分的部署成本都更低。</p>
<h2 id="微细分的运营治理">如何让微细分不失控？</h2>
<p>"三倍的微细分"在成为机会之前，首先是一项运营风险。三条纪律让数量保持可控且有用。</p>
<p>第一，决策检验：只有当细分对应一个有责任人的独特动作时，它才应该存在。如果两个细分触发的是同一个活动，就合并它们。第二，季度清理：把当期没有任何激活记录的细分下线，因为闲置细分会静默累积，并让每一份下游报表更难读懂。第三，每个细分只保留一份受治理的定义——逻辑、责任人、刷新节奏与访问规则集中在一处，由所有渠道消费，而不是复制进每个渠道。</p>
<p>这份纪律的回报是可解释性。当某个活动表现不佳时，"这位客户为什么落在这个细分"必须有一个商品经理能据此行动的答案；而只有当细分被定义为"模型分数之上的规则"，而不是直接把模型原始输出当作结果时，这一点才可能做到。</p>
<h2 id="细分的投资回报">如何衡量细分的投资回报？</h2>
<p>那些醒目的数字是商业论证获得通过的原因：AI驱动的细分可提升35%到45%的活动转化率，采用它的零售商报告的客户生命周期价值高出约28%，而建立在细分之上的个性化带来约20%的收入增长。但这些是度量纪律的结果，而不是度量纪律的替代品。</p>
<p>建议跟踪三个层次。运营指标：刷新延迟、细分覆盖率、各渠道的激活率。业务指标：转化提升、单客毛利、每留住一位客户的折扣支出——并且要与对照组比较，而不是与上季度比较。战略指标：在受治理细分上运行的活动占比，以及从定义细分到完成激活所需的时间。三层都要在上线前建立基线。没有基线与对照组，35%到45%这个数字只是行业均值，而不是零售商可以对自己的项目做出的主张——等到CFO第一次追问归因时，这个差别就至关重要。</p>
<h2 id="自建还是采购">零售商应该自建还是采购细分能力？</h2>
<p>这并非一道非此即彼的选择题，而拆分得是否正确，往往决定了能力是这一季度到位还是明年到位。检验标准是：竞争对手会不会以同样的方式构建这个组件。</p>
<p>真正专属于零售商的部分——指标定义、品类逻辑、工作流集成、反映其毛利结构的阈值——必须自建，因为它承载了别人没有的商业判断。而通用部分——受治理的数据访问层、连接器、权限模型、查询界面——应该采购，因为每家零售商需要的东西都一样，自建只会消耗本已紧张的数据工程产能。</p>
<p>托管式方案能大幅压缩周期：受治理的数据访问层、监控与审计大约两周即可上线，且不需要重建数据仓库，业务团队则能在自己已在使用的工具中获得基于受治理数据的实时答案。更重要的是二阶效应——每一个没有花在通用基础设施上的季度，都是花在创造价值的决策上的季度。</p>
<h2 id="治理与隐私规则">零售细分需要遵守哪些治理与隐私规则？</h2>
<p>四项义务塑造了零售细分项目的边界，而当它们被编码进数据层而不是写在政策文件里时，满足起来要容易得多。</p>
<ul>
<li><strong>目的限制。</strong>为履约或客服采集的数据，不能自动用于营销。授权与用途必须随数据流转，并在查询时执行，使为某一目的构建的细分不会被未加核对的分析师挪作他用。</li>
<li><strong>最小化。</strong>只采集与留存细分真正需要的字段。每一个多余属性都是无收益的风险敞口，而大多数细分模型用很短的特征清单就能取得效果。</li>
<li><strong>带角色过滤的访问控制。</strong>门店导购查询细分时只应看到本店客户，区域经理只应看到本区域。这一控制要在数据层执行，而不是在应用层，因为应用层规则会被下一个集成绕过。</li>
<li><strong>可审计。</strong>记录使用了哪个细分定义、由谁、用于哪个活动、在什么时间。当客户追问"为什么会收到这个优惠"时，答案必须可以被还原。</li>
</ul>
<p>按这种方式处理，治理会让细分变得更快而不是更慢：一旦控制存在于访问层，之后每一个新细分都会继承它们，下一次营销活动的边际合规成本就趋近于零。</p>
'''

ZH_FAQ = [
    ('什么是零售业的AI驱动客户细分？',
     '它指的是用机器学习按行为——最近购买时间、购买频率、品类偏好、渠道组合、退货率、互动趋势——持续对客户分群，而不是按周期把客户放进人口统计或RFM分桶。细分会随行为变化而更新，颗粒度远超人工网格，并且每个细分都对应一个具体动作。采用AI驱动细分的零售商报告的客户生命周期价值高出约28%，活动转化率提升35%到45%，主要原因在于优惠是基于当前行为生成的，而不是基于季度快照。'),
    ('动态细分与传统的RFM细分有什么不同？',
     'RFM是按报表周期重算的静态网格，描述的只是客户在上次刷新时的状态。动态细分则持续打分，并随新事件重新归属客户，这才让实时个性化成为可能。此外RFM无法纳入互动、浏览与退货信号，因此会系统性地误读购买记录稀薄的新客。最实际的差别在于节奏：动态细分实时更新，传统方法按季度更新，而客户的行为在两次更新之间已经改变。'),
    ('启动零售AI细分需要哪些数据？',
     '起步需要两年交易历史，包含订单明细、退货与毛利，以及会员标识。再加入数字互动（Web、App、邮件）、客服交互，以及天气等外部背景，可以提升对新客的准确度。比数据量更重要的两项前提是：线上线下渠道的身份打通，以及按用途记录并在查询时执行的授权状态。缺少身份打通，同一位客户会被算成两个人，所有价值数字都会出错。'),
    ('一家零售商应该运行多少个细分？',
     '有多少个不同动作就设多少个，不多于此——生产环境中通常五到十二个。AI能识别出比传统方法多约三倍的微细分，但那是发现能力，而不是活动计划。建议用决策检验：如果两个细分触发同一种处理，就合并。然后按季度清理，下线当期没有激活记录的细分，并为每个细分保留唯一一份受治理的定义，让所有渠道读到同一套逻辑。'),
    ('部署AI细分多久能看到成效？',
     '聚焦在一个品类或一个用例上的部署大约需要十三周：三周做身份打通与基线建立，四周做特征与模型开发，三周带对照组激活，三周做度量。转化率与毛利的可度量变化通常在这个时间窗内出现。覆盖全品类、全渠道的企业级落地则是十二到十八个月的项目，按决策价值排序推进，每个阶段都继承第一阶段已经建好的定义与控制。'),
]


def run():
    b = {lg: stats(SLUG, lg) for lg in ('en', 'zh-cn', 'zh-tw')}
    process(SLUG, 'en', new_body=EN_BODY, faq=EN_FAQ)
    process(SLUG, 'zh-cn', new_body=ZH_BODY, faq=ZH_FAQ)
    process(SLUG, 'zh-tw', new_body=s2tw(ZH_BODY), faq=[(s2tw(q), s2tw(a)) for q, a in ZH_FAQ])
    for lg in ('en', 'zh-cn', 'zh-tw'):
        print(lg, b[lg], '->', stats(SLUG, lg))


if __name__ == '__main__':
    run()
