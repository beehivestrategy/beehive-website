#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixlib as F

SLUG = "conversational-analytics-energy-sector"

EN_NEW = """
<h2 id="how-do-governance-and-nerc-cip-compliance-work-in-practice">How Do Governance and NERC CIP Compliance Work in Practice?</h2>
<p>Energy is not a permissive environment, and a conversational interface that ignores that will be blocked in security review regardless of how useful it is. The compliance question is not whether operators can ask questions in plain language; it is whether every answer respects the same controls that govern direct system access.</p>
<p>Three controls do most of the work. First, identity propagation: the query runs under the asking user's entitlements rather than a service account, so a contractor sees contractor data and a control room operator sees operational data. Second, scope enforcement at the query layer: access rules are applied when the query is constructed, not filtered after results return, which means restricted rows never enter the answer. Third, complete audit logging: every question, the query it generated, the data it touched, and the answer returned are retained with the user and timestamp attached.</p>
<p>Mapped onto NERC CIP, those three controls cover the parts of the framework that conversational analytics actually touches — access management, electronic security perimeters, and logging — while leaving the physical and personnel security requirements untouched. The practical benefit is that an auditor asking "who accessed this data and what did they see" gets a system-generated answer instead of a reconstruction project.</p>
<p>Deployment model matters as much as control design. Most energy operators require the platform to run inside their own infrastructure or a dedicated tenancy, with data never leaving the controlled environment. Platforms that only offer multi-tenant SaaS struggle in this sector for reasons that have nothing to do with their analytics quality, and it is worth settling that question before evaluation rather than at the end of it.</p>
<h2 id="what-does-a-semantic-layer-for-energy-need-to-contain">What Does a Semantic Layer for Energy Need to Contain?</h2>
<p>The semantic layer is where most conversational analytics implementations in energy either succeed or quietly fail. It is the component that maps business language onto data models, and in a sector where the same word means different things to a geologist, a trader and an emissions analyst, that mapping is the product.</p>
<p>Four elements are non-negotiable. <strong>Entity resolution</strong>: "well 42", "well #42" and "WELL-0042" must resolve to the same asset before a user sees a result, because legacy systems in the same company will contain all three. <strong>Metric definitions with owners</strong>: production, availability, and emissions each need one agreed definition and one accountable owner, since a number with two definitions has no definition. <strong>Unit and terminology handling</strong>: barrels versus cubic metres, gross versus net, and regional naming conventions have to be normalised, or answers will be numerically correct and operationally wrong. <strong>Time semantics</strong>: production data, market prices, and emissions factors all carry different reporting lags, and "yesterday" means different things in each.</p>
<p>Building this layer is the honest majority of the work in weeks one to four, and it is the reason scoping matters more than licensing. Teams that skip it ship a system that answers fluently and wrongly, which is worse than no system because it is trusted for longer. Teams that do it well find that the same layer accelerates every downstream use case, from reporting to alerting to agentic workflows.</p>
<h2 id="how-does-conversational-analytics-change-daily-work-in-operations">How Does Conversational Analytics Change Daily Work in Operations?</h2>
<p>The abstract benefits — faster decisions, broader access — become real in specific moments. Four illustrate what changes.</p>
<ul>
<li><strong>Shift handover.</strong> An outgoing operator asks what deviated during the shift and receives a summarised exception list with links to the underlying readings, instead of passing on a verbal summary that omits the one anomaly that matters.</li>
<li><strong>Regulatory data request.</strong> An ESG analyst asks for Scope 1 emissions by facility for the reporting period and receives a figure with its source, calculation method and completeness status attached — which is the difference between a two-week evidence-gathering exercise and an afternoon.</li>
<li><strong>Trading desk question.</strong> A trader asks how current storage levels compare with the same week in the last three years and gets the comparison immediately, while the price signal is still actionable.</li>
<li><strong>Maintenance prioritisation.</strong> A reliability engineer asks which compressor stations showed pressure deviation more than three times in the last month and gets a ranked list, converting a scheduled inspection queue into a risk-ordered one.</li>
</ul>
<p>What all four share is that the question existed before the tool did. The difference is that it used to become a ticket, a meeting, or a guess, and now it becomes an answer in the seconds it takes to type. That is also why adoption in this sector outpaces conventional BI rollouts: the interface matches a question people were already asking out loud.</p>
<h2 id="what-should-energy-executives-measure-in-the-first-year">What Should Energy Executives Measure in the First Year?</h2>
<p>Activity metrics flatter the programme and persuade nobody. Four measures survive contact with a CFO.</p>
<p><strong>Time-to-answer on a defined question set.</strong> Pick twenty questions the organisation asks repeatedly, measure how long they take before deployment, and re-measure quarterly. A reduction from days to minutes is the single most credible number the programme can produce.</p>
<p><strong>Analyst hours returned.</strong> Energy operators spend up to 40 percent of analytical time locating and reconciling data rather than analysing it. Track the hours recovered on reporting and ad-hoc request fulfilment, and convert them at fully loaded cost.</p>
<p><strong>Adoption by role, not by headcount.</strong> Ninety-two percent overall adoption is less useful than knowing that control room operators adopted it and reservoir engineers did not. Segment adoption by discipline and investigate the gaps, because the gap is usually a semantic layer gap rather than a training gap.</p>
<p><strong>Decisions attributable to the tool.</strong> Record the operational decisions that changed because an answer arrived in time — a maintenance reorder, a hedging adjustment, an emissions intervention. Three or four documented cases with quantified impact do more for the next budget than any usage dashboard.</p>
<p>Establish the baseline before deployment starts. Programmes that begin measuring after go-live spend the rest of the year arguing about attribution instead of reporting results.</p>
"""

CN_BODY = """<h2 id="energy-data-challenge">能源行业的数据难题为什么这么难解？</h2>
<p>能源企业坐拥海量且持续增长的生产运营数据。上游地震勘探、中游管道传感、下游零售计量每天都在产生TB级的信息——大型运营商每天新增数据量通常在2.5PB的量级——但其中绝大部分仍被锁在彼此隔离的系统里：老旧的SCADA平台、基于Excel的报表链路，以及难以集成的碎片化数据库。</p>
<p>不作为的代价相当可观。行业分析机构估计，能源运营商在提取任何有价值的洞察之前，要花掉高达<strong>40%的分析时间</strong>用于定位和核对数据；而关于该行业数据互操作性不足的研究，把全球年度成本估在了数百亿美元的规模——常被引用的数字约为每年180亿美元。过去需要数周完成的手动报表周期，如今已经跟不上大宗商品市场波动和监管要求演进所带来的实时决策需求。</p>
<p>让这一挑战在2026年变得紧迫的，是多重压力的叠加。电力需求增长、排放披露义务和利润空间承压，正在迫使能源企业更快地回答更难的问题——而答案就藏在员工无法直接查询的数据里。数据量与查询能力之间的鸿沟，正是对话式分析存在的意义。</p>
<h2 id="what-is-conversational-analytics">什么是对话式分析？</h2>
<p>对话式分析是一层自然语言接口，让业务用户用日常语言查询企业数据系统。运营人员不必编写SQL、不必在多层标签页的仪表盘之间穿梭、也不必等待BI团队出报表，只需把问题打出来或说出来："上季度二叠纪盆地的井口压力趋势是怎样的？"</p>
<p>与呈现预置视图的传统BI工具不同，对话式分析平台会动态理解意图、识别相关数据源、构造查询并返回带上下文的答案。结果是决策更快、非技术角色也能触及数据，而且洞察带有用户岗位的场景——地质师看到的是油藏语境，交易员看到的是市场语境，财务控制者看到的是成本语境。</p>
<p>在架构层面，最好的实现由三层组成：把业务语言映射到数据模型和指标定义的语义层；把问题翻译成可执行查询的AI引擎；以及对每个答案执行访问控制与血缘追溯的治理层。最后一层正是可信的分析工具与聊天玩具的分界线——返回的每个数字都能追溯到源头，而这一点在受监管的行业里至关重要。</p>
<h2 id="key-use-cases">对话式分析在能源价值链上创造了哪些价值？</h2>
<p>在整个能源价值链上，对话式分析正在若干关键领域产生可衡量的成效——共同点在于，领域专家现在可以直接质询数据，问题与答案之间不再需要翻译者。</p>
<ul>
<li><strong>上游勘探：</strong>地质师与油藏工程师无需学习专门的查询语言，就能查询地震数据库、钻井日志和生产历史。</li>
<li><strong>中游监控：</strong>管道运营方可以实时掌握流量、压力异常和检修计划。</li>
<li><strong>下游零售：</strong>加油站经理与定价分析师可以查询成品油需求模式、竞争对手定价数据和季节性预测。</li>
<li><strong>可持续信息披露：</strong>ESG团队能够生成排放清单、碳强度指标和监管合规摘要。</li>
<li><strong>作业安全：</strong>HSE管理者可以用自然语言查询事故记录、未遂事件数据库和培训合规档案。</li>
</ul>
<p>当对话式访问与主动告警结合时，效果会进一步放大：一位运营人员既能问"昨天哪些压缩机站的压力偏离了基线？"，也能在今天同样的模式开始形成时收到通知。分析不再是一项检索工作，而变成了一种监控能力。</p>
<h2 id="implementation-roadmap">落地路线图应该是什么样的？</h2>
<p>在能源环境中部署对话式分析，通常遵循一个结构化的四步流程。企业一般在启动后两到四周内看到首个价值点，在所有主要数据源上完成全面集成则可在八到十二周内实现——前提是数据模型的工作在一开始就被诚实地界定清楚。</p>
<ol>
<li><strong>评估（第1-2周）</strong>——梳理现有数据源，识别高价值用例，定义成功指标。在能源行业，语义层正是在这一步诞生的：在任何人开始查询之前，先就"产量""可用率""排放量"的定义达成一致。</li>
<li><strong>集成（第2-4周）</strong>——把AI网关接入SCADA、历史数据库、ERP系统和物联网平台，把治理与血缘做在集成层上，而不是事后补救。</li>
<li><strong>试点（第4-6周）</strong>——面向一组受控的核心用户部署，并用真实提问来打磨自然语言理解模型——真实提问永远与规划阶段设想的不同。</li>
<li><strong>推广（第6-12周）</strong>——向更广泛的组织铺开，建立治理护栏、用户培训和用量分析，让采用率是被度量的，而不是被假设的。</li>
</ol>
<p>采用蜂启咨询所走路径的平台——领域调优模型加上受治理的访问层——会进一步压缩这个时间表，因为模型已经理解能源术语，访问层也已经执行了策略。过去吃掉BI项目大部分预算的集成工作被平台吸收，而不必为每个源系统重新造轮子。</p>
<h2 id="how-do-governance-and-nerc-cip-compliance-work-in-practice">治理与NERC CIP合规在实践中如何落地？</h2>
<p>能源行业不是一个宽松的环境，任何忽视这一点的对话式界面，无论多好用都会在安全评审中被拦下。合规问题不在于运营人员能否用自然语言提问，而在于每个答案是否遵守了与直接访问系统时相同的控制措施。</p>
<p>有三项控制承担了绝大部分工作。第一是身份传递：查询以提问用户自身的授权运行，而不是服务账号，因此承包商看到承包商的数据，中控室操作员看到运营数据。第二是查询层的作用域执行：访问规则在查询构造时生效，而不是在结果返回后再过滤，这意味着受限的数据行永远不会进入答案。第三是完整的审计日志：每一个问题、它生成的查询、它触达的数据，以及返回的答案，都连同用户和时间戳一并留存。</p>
<p>对应到NERC CIP，这三项控制覆盖了该框架中与对话式分析真正相关的部分——访问管理、电子安全边界和日志记录，而不触及物理与人员安全的要求。实际收益在于：当审计方问"谁访问了这些数据、看到了什么"时，得到的是系统生成的答案，而不是一次重建工程。</p>
<p>部署模式与控制设计同样重要。多数能源运营商要求平台运行在自有基础设施或专属租户内，数据绝不离开受控环境。只提供多租户SaaS的平台在这个行业里会碰壁，原因与它们的分析能力毫无关系——而这个问题值得在评估之前就澄清，而不是拖到最后。</p>
<h2 id="what-does-a-semantic-layer-for-energy-need-to-contain">面向能源行业的语义层需要包含什么？</h2>
<p>语义层正是能源行业多数对话式分析项目要么成功、要么悄然失败的地方。它是把业务语言映射到数据模型的组件，而在一个同一个词对地质师、交易员和排放分析师意味着不同含义的行业里，这份映射就是产品本身。</p>
<p>有四个要素不可或缺。<strong>实体解析</strong>："42号井""井#42"和"WELL-0042"必须在用户看到结果之前解析为同一个资产，因为同一家公司里的遗留系统会同时存在这三种写法。<strong>带责任人的指标定义</strong>：产量、可用率、排放量都需要唯一的一致定义和唯一的责任人，因为一个有两种定义的数字等于没有定义。<strong>单位与术语处理</strong>：桶与立方米、毛量与净量，以及各地区的命名习惯都必须归一化，否则答案会在数值上正确、在运营上错误。<strong>时间语义</strong>：生产数据、市场价格和排放因子各自带有不同的报送滞后，"昨天"在三者之中含义并不相同。</p>
<p>构建这一层占据了第1到4周工作量的绝大部分，也正是为什么范围界定比许可证选型更重要。跳过它的团队，会交付一个回答流畅但内容错误的系统——这比没有系统更糟，因为它会被信任得更久。做得好的团队则会发现，同一层会加速所有下游用例，从报表到告警再到智能体工作流。</p>
<h2 id="how-does-conversational-analytics-change-daily-work-in-operations">对话式分析如何改变日常运营工作？</h2>
<p>抽象的好处——更快的决策、更广的触及——只有在具体场景中才会变成真实。以下四个场景说明了到底改变了什么。</p>
<ul>
<li><strong>交接班。</strong>交班的操作员询问本班次发生了哪些偏离，得到一份带底层读数链接的异常摘要，而不是一段恰好漏掉最关键异常的口头交接。</li>
<li><strong>监管数据请求。</strong>ESG分析师要求按设施列出报告期内的范围一排放，得到的数字同时附带来源、计算方法和完整性状态——这正是"两周取证"与"一个下午"之间的差别。</li>
<li><strong>交易台提问。</strong>交易员询问当前库容与过去三年同周的对比，能在价格信号仍然可操作的时候立刻拿到对比结果。</li>
<li><strong>检修优先级排序。</strong>可靠性工程师询问过去一个月哪些压缩机站出现压力偏离超过三次，得到一份排序清单，把按计划的巡检队列变成按风险排序的队列。</li>
</ul>
<p>这四个场景的共同点在于：问题在工具出现之前就已经存在。区别在于，过去它会变成一张工单、一次会议或一个猜测，而现在它在把问题打出来的几秒钟内变成了一个答案。这也是为什么该行业的采用率高于传统BI推广——这个界面所匹配的，正是人们本来就大声问出的问题。</p>
<h2 id="what-should-energy-executives-measure-in-the-first-year">能源企业管理者第一年应该衡量什么？</h2>
<p>活动量指标会让项目看起来很好，却说服不了任何人。有四项指标经得起CFO的追问。</p>
<p><strong>一组既定问题的回答耗时。</strong>挑出组织反复提出的二十个问题，在部署前测量它们需要多久，之后每季度复测一次。从"数天"缩短到"数分钟"，是这个项目能拿出的最有说服力的数字。</p>
<p><strong>被释放的分析工时。</strong>能源运营商有多达40%的分析时间用于定位和核对数据，而不是分析数据。统计在报表和临时取数上节省的工时，并按全负荷成本折算。</p>
<p><strong>按岗位而非按人数的采用率。</strong>整体采用率92%这个数字，远不如"中控室操作员用起来了、油藏工程师没用起来"有价值。按专业拆分采用率并追查差距，因为差距通常出在语义层，而不是培训。</p>
<p><strong>可归因于该工具的决策。</strong>记录那些因为答案及时送达而改变的决策——一次检修重排、一次套保调整、一次排放干预。三到四个有量化影响的真实案例，对下一个预算的作用胜过任何用量仪表盘。</p>
<p>在部署开始之前就建立基线。上线之后才开始测量的项目，会把余下的一年都花在争论归因上，而不是汇报结果。</p>
<h2 id="measuring-roi">如何衡量投资回报与业务影响？</h2>
<p>实施对话式分析的能源企业，在三类核心KPI上都报告了可观的回报。首年投资回报率通常在<strong>3倍</strong>左右，由报表人力节省、运营响应加快和分析积压减少共同驱动。查询解决时间下降约<strong>78%</strong>——因为用户不再等待BI团队，而是自助取数；六个月内用户采用率约为<strong>92%</strong>，远高于传统BI推广的采用水平，原因在于这个界面契合人们本来的思考方式。</p>
<p>决策速度的提升，来自一线运营人员不再等待集中的分析团队来满足取数需求。在交易与生产运营中，一个关于价格或压力的洞察在数小时内就会失去价值，当天答复与当分钟答复之间的差别会直接反映在损益上。在可持续信息披露方面，更快地获取排放数据，把每季度的突击战变成了持续且可审计的流程。</p>
<p>度量的纪律与工具本身同样重要：部署前定义基线，跟踪查询量、回答耗时以及可归因于分析的下游决策，并每季度复评。会度量自身分析项目的企业才能改进它；不度量的企业甚至讲不出自己的成功故事。</p>
<h2 id="overcoming-barriers">常见的落地障碍如何跨越？</h2>
<p>尽管收益清晰，能源企业仍会面临三个反复出现的落地挑战——每一个都有经过验证的缓解策略。它们都不是技术上的死结，但三者都极易被低估。</p>
<ul>
<li><strong>数据质量与碎片化：</strong>遗留系统往往存在命名不一致、元数据缺失和记录重复的问题。解法是在集成层部署语义数据目录，让平台在用户看到结果之前，就把"42号井"和"井#42"解析为同一个资产。</li>
<li><strong>变革管理：</strong>习惯了既有报表工具的运营团队可能抵触采用。把推广与实操培训结合，在每个专业里指定内部倡导者，并公开快速见效的案例，让怀疑逐渐转化为需求。</li>
<li><strong>安全与合规：</strong>能源基础设施受制于严格的网络安全框架，包括NERC CIP和ISA/IEC 62443。应对方式是在查询层强制基于角色的访问控制、记录每一次交互，并把所有数据保留在受控环境中——这也是为什么运行于客户自有基础设施的部署模式在该行业被强烈偏好。</li>
</ul>
<h2 id="future-outlook">能源企业接下来应该期待什么？</h2>
<p>对话式分析与自主AI智能体的融合，将进一步改变能源运营。在未来两年内，可以预期AI智能体不只回答问题，还会主动提示异常、推荐运营调整，并执行预先批准过的纠正动作——人类负责复核，而不是亲自撰写响应。</p>
<p>对能源企业而言，战略含义是现在就打好对话式的基础。语义层、受治理的数据访问，以及通过对话式分析建立起来的用户信任，恰恰是2027年及以后的智能体系统所需要的资产。等待智能体成熟的企业，会发现自己正在把自主系统集成到毫无准备的数据基础之上；而现在就投入的企业，则已经具备了术语体系、血缘关系与运营信任。</p>"""

FAQ = {
 "EN": [
  ("How long does it take to implement conversational analytics in an energy company?",
   "Initial deployment typically takes two to four weeks, covering core data source connections and a pilot with a select group of users. Full integration across all major data sources is achievable within eight to twelve weeks, provided the semantic layer work is scoped honestly at the start."),
  ("Can conversational analytics integrate with existing SCADA and IoT systems?",
   "Yes. The platform connects to SCADA systems, IoT sensor networks, and operational historian databases through an AI Gateway layer that supports over fifty out-of-the-box data source adapters. Governance, lineage and access control are applied at the integration layer rather than after the fact."),
  ("What security measures are in place for energy sector data?",
   "The platform provides end-to-end encryption for data in transit and at rest, role-based access control aligned with NERC CIP requirements, and comprehensive audit logging for every query and response. Most energy operators also require deployment inside their own infrastructure or a dedicated tenancy."),
  ("How is this different from adding a chatbot to our existing BI tool?",
   "A chatbot on top of BI can only answer questions the pre-built dashboards already cover. Conversational analytics with a semantic layer resolves intent against the underlying data model, so questions nobody anticipated still return a governed, traceable answer - and the answer carries its source, definition and completeness status."),
 ],
 "zh-CN": [
  ("在能源企业落地对话式分析需要多长时间？",
   "首次部署通常需要两到四周，覆盖核心数据源接入和面向一组选定用户的试点。在所有主要数据源上完成全面集成，可在八到十二周内实现——前提是语义层的工作在一开始就被诚实地界定清楚。"),
  ("对话式分析能与现有的SCADA和物联网系统集成吗？",
   "可以。平台通过AI网关层接入SCADA系统、物联网传感网络和运营历史数据库，该网关支持五十种以上开箱即用的数据源适配器。治理、血缘与访问控制在集成层生效，而不是事后补救。"),
  ("面向能源行业数据，有哪些安全措施？",
   "平台为传输中和静态存储的数据提供端到端加密，提供符合NERC CIP要求的基于角色的访问控制，并对每一次查询与响应做完整的审计记录。多数能源运营商还会要求部署在自有基础设施或专属租户内。"),
  ("这与在现有BI工具上加一个聊天机器人有什么不同？",
   "构建在BI之上的聊天机器人只能回答预置仪表盘已经覆盖的问题。带语义层的对话式分析则针对底层数据模型解析意图，因此没有人预先想到的问题也能返回受治理、可追溯的答案——而且答案会携带来源、定义和完整性状态。"),
 ],
}

# ---- chrome translations (EN -> zh-CN), longest first ----
CHROME = [
  ("Conversational Analytics for the Energy Sector", "能源行业的对话式分析"),
  ("AI Agents in Manufacturing: From Predictive Maintenance to Production Optimisation", "制造业的AI智能体：从预测性维护到生产优化"),
  ("Semantic Layer Conversational BI Self Service Analytics", "语义层、对话式BI与自助分析"),
  ("Automating Data Quality So Analysts Stop Cleaning Data", "让分析师不再清洗数据的自动化数据质量"),
  ("Discover how factory operators are using conversational BI to reduce downtime and improve quality control.", "了解工厂运营方如何用对话式BI减少停机并改进质量控制。"),
  ("How a governed semantic layer makes self-service analytics trustworthy and scalable.", "受治理的语义层如何让自助分析变得可信且可扩展。"),
  ("Ready to transform your energy data strategy?", "准备好改变您的能源数据战略了吗？"),
  ("See how Beehive Strategy's conversational analytics platform unlocks real-time insights across your energy operations, from upstream exploration to downstream retail.", "了解蜂启咨询的对话式分析平台如何在您的能源运营中释放实时洞察——从上游勘探到下游零售。"),
  ("Typical first-year ROI", "典型首年投资回报"),
  ("Faster query resolution", "查询解决提速"),
  ("Table of Contents", "目录"),
  ("Share this article", "分享本文"),
  ("Related Articles", "相关文章"),
  ("Recommended Articles", "推荐文章"),
  ("View all", "查看全部"),
  ("Back to All Articles", "返回全部文章"),
  ("Frequently Asked Questions", "常见问题"),
  ("Energy Sector", "能源行业"),
  ("Conversational Analytics", "对话式分析"),
  ("Case Studies", "客户案例"),
  ("Industries", "行业方案"),
  ("Solution", "解决方案"),
  ("Services", "咨询服务"),
  ("Pricing", "定价"),
  ("Blog", "博客"),
  ("Home", "首页"),
  ("Topics", "主题"),
  ("Technology", "技术"),
  ("Industry", "行业"),
  ("Manufacturing", "制造业"),
  ("Data Quality", "数据质量"),
  ("Book a Demo", "预约演示"),
  ("Explore the Solution", "了解解决方案"),
  ("Privacy Policy", "隐私政策"),
  ("Terms of Service", "服务条款"),
  ("Cookie Preferences", "Cookie 设置"),
  ("Documentation", "文档"),
  ("Resources", "资源"),
  ("Company", "公司"),
  ("Products", "产品"),
  ("Contact", "联系我们"),
  ("About", "关于我们"),
  ("July 25, 2026", "2026年7月25日"),
  ("Jun 10, 2026", "2026年6月10日"),
  ("Apr 24, 2026", "2026年4月24日"),
]

READ_RE = re.compile(r'(\d+)\s+min read')

def make_zh(en_html, lang):
    s = en_html
    pre = "zh-cn" if lang == "zh-CN" else "zh-tw"
    # 1. language attribute + locale
    s = s.replace('lang="en"', 'lang="%s"' % pre)
    s = s.replace('content="en_US"', 'content="%s"' % ("zh_CN" if lang == "zh-CN" else "zh_TW"))
    # 2. URLs
    s = s.replace('https://www.beehivestrategy.com/blog', 'https://www.beehivestrategy.com/%s/blog' % pre)
    s = s.replace('href="/blog', 'href="/%s/blog' % pre)
    s = s.replace('href="/solution"', 'href="/%s/solution"' % pre)
    s = s.replace('href="/contact"', 'href="/%s/contact"' % pre)
    s = s.replace('href="/about"', 'href="/%s/about"' % pre)
    s = s.replace('href="/services"', 'href="/%s/services"' % pre)
    s = s.replace('href="/industries"', 'href="/%s/industries"' % pre)
    s = s.replace('href="/case-studies"', 'href="/%s/case-studies"' % pre)
    s = s.replace('href="/pricing"', 'href="/%s/pricing"' % pre)
    s = s.replace('href="/"', 'href="/%s/"' % pre)
    # 3. reading time
    s = READ_RE.sub(lambda m: "%s 分钟阅读" % m.group(1), s)
    # 4. article body
    b = F.get_body(s)
    newb = re.sub(r'</div>\s*<html><body>.*?</body></html>', lambda m: '</div>' + CN_BODY, b, flags=re.S)
    assert newb != b, "body region not replaced"
    s = F.set_body(s, newb)
    # 5. chrome strings
    for a, bb in CHROME:
        s = s.replace(a, bb)
    # 6. byline author
    s = s.replace('Beehive Strategy <span aria-hidden="true" class="article-meta-dot">',
                  '蜂启咨询 <span aria-hidden="true" class="article-meta-dot">')
    return s

def main():
    # ---------- EN ----------
    s = F.load(SLUG, "EN")
    b = F.get_body(s)
    anchor = '<h2 id="measuring-roi">Measuring ROI and Impact</h2>'
    assert anchor in b
    b = b.replace(anchor, EN_NEW.strip() + "\n" + anchor, 1)
    ren = {
        "The Energy Data Challenge": "Why Is Energy Data So Hard to Use?",
        "Key Use Cases in Energy": "Where Does Conversational Analytics Create Value in Energy?",
        "Implementation Roadmap": "What Does an Implementation Roadmap Look Like?",
        "Measuring ROI and Impact": "How Do You Measure ROI and Business Impact?",
        "Overcoming Barriers": "How Do You Overcome the Common Barriers?",
        "Future Outlook": "What Should Energy Companies Expect Next?",
    }
    for old, new in ren.items():
        b = re.sub(r'(<h2 id="[^"]+">)' + re.escape(old) + r'(</h2>)', r'\g<1>' + new + r'\g<2>', b)
    F.save(SLUG, "EN", F.set_body(s, b))

    before, after = F.process(SLUG, faq=FAQ,
                              faq_titles={"EN": "Frequently Asked Questions"})
    print("EN", before["EN"], "->", after["EN"])

    # ---------- zh-CN / zh-TW ----------
    en = F.load(SLUG, "EN")
    cn = make_zh(en, "zh-CN")
    with open(F.path(SLUG, "zh-CN"), "w", encoding="utf-8") as f:
        f.write(cn)
    tw = F.s2twp_text(cn)
    tw = tw.replace('lang="zh-cn"', 'lang="zh-tw"')
    tw = tw.replace('content="zh_CN"', 'content="zh_TW"')
    with open(F.path(SLUG, "zh-TW"), "w", encoding="utf-8") as f:
        f.write(tw)

    before, after = F.process(SLUG, faq=FAQ,
                              faq_titles={"zh-CN": "常见问题", "zh-TW": "常見問題"})
    for lang in ("zh-CN", "zh-TW"):
        print(lang, before[lang], "->", after[lang])

if __name__ == "__main__":
    main()
