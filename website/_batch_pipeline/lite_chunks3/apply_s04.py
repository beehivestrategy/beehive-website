# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patch
from opencc import OpenCC

ROOT = '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website'
SLUG = 'ai-talent-strategy-hiring-vs-upskilling-may'

EN_TOC = [
    ('why-is-the-hiring-versus-upskilling-decision-so-often-guessed', 'Why Is the Hiring Versus Upskilling Decision So Often Guessed?'),
    ('what-does-ai-talent-actually-cost-on-each-path', 'What Does AI Talent Actually Cost on Each Path?'),
    ('which-roles-should-you-hire-and-which-should-you-grow', 'Which Roles Should You Hire and Which Should You Grow?'),
    ('how-do-you-build-a-talent-portfolio-instead-of-a-single-bet', 'How Do You Build a Talent Portfolio Instead of a Single Bet?'),
    ('how-fast-can-upskilling-realistically-close-the-gap', 'How Fast Can Upskilling Realistically Close the Gap?'),
    ('how-do-you-keep-the-people-you-just-trained', 'How Do You Keep the People You Just Trained?'),
]

EN_PROSE = """
<p class="article-lead"><strong>Most AI talent strategies are not strategies. They are a hiring plan with the word "transformation" attached, justified by a market salary benchmark that says scarce specialists are expensive and concluded with a hope that internal staff will catch up somehow.</strong> The decision between hiring and upskilling is not ideological, and it is not the same answer for every role. It is an arithmetic problem with three variables: how long you can wait, how much domain context the role requires, and whether the capability is durable or will be commoditised within two years. This article gives you a framework for splitting the decision role by role, a realistic cost and timeline model for each path, and a portfolio approach that survives the next budget cycle rather than the next headline.</p>
<h2 id="why-is-the-hiring-versus-upskilling-decision-so-often-guessed">Why Is the Hiring Versus Upskilling Decision So Often Guessed?</h2>
<p>Three forces push organisations toward guessing. The first is benchmark anxiety: published salary data for AI specialists is genuinely alarming, and it anchors the conversation on price rather than on value and timing. The second is that the two paths are championed by different functions with different incentives — talent acquisition has a mandate to fill requisitions, learning and development has a mandate to build capability, and neither owns the business outcome that would settle the argument. The third is that most organisations cannot name the capability they actually need, so they cannot compare two ways of acquiring it.</p>
<p>That last point is the fixable one. "We need AI talent" is not a requirement. "We need someone who can express our revenue recognition logic as a versioned, testable semantic model within one quarter, and who will own it for two years" is a requirement — and once stated that way, the answer is often obvious, because the binding constraint turns out to be domain knowledge rather than machine learning expertise.</p>
<p>The second reason decisions get guessed is that the two paths are compared on the wrong axis. Hiring is fast to start and slow to pay off: a new specialist typically takes two to three quarters to reach full productivity in an enterprise context, because the technical skill arrives on day one and the context takes months. Upskilling is slow to start and fast to pay off: an internal candidate already knows the definitions, the politics, and the systems, so what they learn is immediately applied. Comparing them on cost per head misses both curves.</p>
<p>There is one more reason the decision gets guessed, and it is the one executives find most uncomfortable: nobody has written down what the current team can already do. Before you can compare two acquisition paths, you need an inventory of existing capability — who can write production-grade SQL, who understands the semantic layer, who has shipped anything evaluated against a test suite rather than eyeballed. That inventory usually reveals a larger internal bench than the hiring plan assumes, and it takes about two weeks to build. Skipping it is why so many organisations buy capability they already own.</p>
<p>Finally, organisations systematically underweight the depreciation question. Some AI capabilities are becoming cheaper and more automated every quarter — baseline model integration, for example, is rapidly being absorbed into platforms. Others are appreciating: evaluation design, semantic modelling, and the governance judgement that decides where automation must stop. Paying a premium to hire a capability that will be commoditised within eighteen months is a poor trade; paying a premium for durable judgement is often a good one.</p>
<h2 id="what-does-ai-talent-actually-cost-on-each-path">What Does AI Talent Actually Cost on Each Path?</h2>
<p>The honest comparison has to include cost to productivity, not cost to offer acceptance. On the hiring path, budget for the salary premium over an equivalent senior engineer, recruiting fees or internal recruiter time, the vacancy period, and — the largest and least counted item — the two to three quarters of ramp before the hire is independently productive. Add the opportunity cost of the internal people who onboard them, which is easily a fifth of a senior engineer's time for the first month.</p>
<p>On the upskilling path, budget for the direct training cost, the protected capacity you must ring-fence for people to learn while still delivering, the temporary productivity dip as teams adopt new methods, and the cost of a mis-hire avoided. That last item is underrated: internal candidates have a known performance record, whereas external AI hires are being selected in a market where credentials are weakly correlated with enterprise delivery capability.</p>
<table class="article-table"><thead><tr><th>Cost and time factor</th><th>Hire externally</th><th>Upskill internally</th><th>Practical note</th></tr></thead><tbody><tr><td>Time to start contributing</td><td>4-8 weeks after offer</td><td>Immediate</td><td>Internal staff already hold context and access</td></tr><tr><td>Time to full productivity</td><td>2-3 quarters</td><td>1-2 quarters</td><td>Ramp on the hire path is context, not skill</td></tr><tr><td>Direct cost</td><td>Salary premium plus fees</td><td>Training plus backfill capacity</td><td>Premium is visible; protected capacity is not</td></tr><tr><td>Domain context required</td><td>Must be acquired</td><td>Already present</td><td>Decisive for governance and semantics roles</td></tr><tr><td>Retention risk</td><td>High; portable skill, hot market</td><td>Moderate; loyalty dividend</td><td>Newly upskilled staff are also newly marketable</td></tr><tr><td>Capability durability</td><td>Best for durable, deep specialisms</td><td>Best for capabilities being absorbed into platforms</td><td>Match the path to the depreciation curve</td></tr></tbody></table>
<p>When you build the model honestly, a clear pattern emerges. Roles requiring deep, durable, generalisable expertise favour hiring. Roles requiring domain context, definitional judgement, or capabilities that are converging into standard tooling favour upskilling. The mistake is applying one answer across an entire function.</p>
<h2 id="which-roles-should-you-hire-and-which-should-you-grow">Which Roles Should You Hire and Which Should You Grow?</h2>
<p>The most useful way to split the decision is by asking two questions about each role: does it require context that only exists inside your organisation, and will the underlying skill still command a premium in two years?</p>
<ol>
<li><strong>Hire: evaluation and AI quality leadership.</strong> This is a durable, method-heavy discipline with real craft — golden set design, regression strategy, sampling regimes, incident classification. It is also the discipline most enterprises have never built, so there is no internal bench to grow from. Hire one lead, then grow the team beneath them.</li>
<li><strong>Grow: data product ownership.</strong> The binding constraint is knowing which definitions are contested and why. That knowledge is internal by construction. Promote a senior analyst or engineer and give them explicit accountability, a contract template, and coaching.</li>
<li><strong>Hire: specialist infrastructure and platform engineering</strong> for capabilities you will run for years — model serving, vector infrastructure, observability. These are deep crafts with long depreciation curves.</li>
<li><strong>Grow: semantic modelling and analytics engineering.</strong> The tooling converges, the business logic does not. Your existing BI and analytics engineers are closer to this than any external hire who does not know your chart of accounts.</li>
<li><strong>Grow: AI enablement and adoption partners.</strong> These roles are 80% domain credibility and 20% technical fluency. Hiring externally for them reliably fails because business units do not trust someone who cannot discuss their operating rhythm.</li>
<li><strong>Hire selectively: research-grade machine learning.</strong> Only if you are genuinely building proprietary models. Most enterprises are not, and should not pretend otherwise in their hiring plan.</li>
</ol>
<p>One caveat on the grow list: growing capability requires a real curriculum, not a licence to a video library. The roles above become productive through apprenticeship on a live migration — converting an existing dashboard into a governed data product, building the evaluation suite for one domain, running the first conversational pilot. Budget for the work, not just the course.</p>
<h2 id="how-do-you-build-a-talent-portfolio-instead-of-a-single-bet">How Do You Build a Talent Portfolio Instead of a Single Bet?</h2>
<p>A portfolio approach treats hiring and upskilling as complementary instruments with different risk profiles, and allocates deliberately across three horizons. Horizon one covers the next two quarters: use contractors, managed services, or a platform partner to deliver capability you need immediately and may not need permanently. This is where most of the "we must hire" panic belongs, and it is often better solved with a services engagement than with a requisition.</p>
<p>Horizon two covers the next four to eight quarters: this is where permanent hiring belongs. By the time you reach this horizon you know which capabilities are actually durable in your environment, because you have run something real. Hiring into a proven need converts an expensive experiment into a reasonable investment.</p>
<p>Horizon three covers the eighteen-month-plus structural shift: this is where upskilling belongs. It is slow, it compounds, and it is the only path that changes the organisation's baseline rather than adding a few exceptional individuals. The failure mode is treating horizon three as urgent — declaring a reskilling programme and expecting results in a quarter, then concluding that upskilling does not work.</p>
<ul>
<li><strong>Fund horizons separately.</strong> Mixing them in one budget means the urgent always eats the structural.</li>
<li><strong>Set a ratio and defend it.</strong> A common starting allocation is roughly one external specialist hire for every four to six internal conversions, adjusted by role criticality.</li>
<li><strong>Write the depreciation assumption down.</strong> For every capability you plan to hire, state whether you believe it will still command a premium in two years. Revisit annually.</li>
<li><strong>Use services to buy time, not to avoid decisions.</strong> A managed engagement should have an explicit knowledge-transfer obligation attached to it.</li>
<li><strong>Track capability, not headcount.</strong> Measure the number of domains with a named data product owner and a passing evaluation suite, not the number of AI staff.</li>
<li><strong>Re-baseline every quarter.</strong> Capability depreciates and the market moves; a portfolio set once and left alone becomes a hiring plan with extra steps.</li>
</ul>
<p>Two portfolio mistakes deserve explicit warnings. The first is over-rotating to services: a managed engagement is excellent for speed and terrible as a permanent substitute for an internal decision. If after two quarters you still cannot name the internal owner of the capability, you have not bought time — you have rented a dependency. The second is treating the portfolio as fixed. Capability that was durable last year may be commoditised this year, and the correct response is to shift allocation, not to defend last year's logic. Review the split quarterly against evidence from your own delivery, and let the depreciating capabilities migrate from the hiring column to the upskilling column as the market absorbs them.</p>
<h2 id="how-fast-can-upskilling-realistically-close-the-gap">How Fast Can Upskilling Realistically Close the Gap?</h2>
<p>The honest answer is faster than most hiring plans and slower than most training vendors claim. A competent analytics engineer can become productive in semantic modelling and data product ownership within one quarter if — and this is the operative condition — the learning is attached to a live deliverable with a real deadline. A competent analyst can learn to design and run an evaluation suite in about six weeks under the same condition. Without a live deliverable, both take three times as long and half of it evaporates.</p>
<p>The sequencing that works is consistent across organisations. Start with evaluation, because it is the skill that makes delegation safe and it requires no new infrastructure. Move to semantic modelling, because expressing business logic as versioned models is the foundation everything else consumes. Then add retrieval and grounding concepts, which are largely a matter of understanding how your curated data products get used. Leave model training and fine-tuning until last, because most enterprises will discover they rarely need it.</p>
<p>The accelerating factor is a platform that removes the infrastructure burden. When teams can ask questions of governed data through a conversational interface in WeCom, DingTalk, Feishu, Teams, or WhatsApp without standing up a serving stack, the curriculum collapses to the parts that matter: definitions, evaluation, and judgement. This is why Beehive Strategy delivers conversational analytics as a managed service deployable in about two weeks on top of the warehouse you already run — it converts an eighteen-month capability build into a two-week starting point, and lets your team learn the durable skills on live work rather than on scaffolding they will later discard.</p>
<h2 id="how-do-you-keep-the-people-you-just-trained">How Do You Keep the People You Just Trained?</h2>
<p>There is an uncomfortable truth about upskilling: it makes your people more marketable. The standard response — hoping loyalty will do the work — is not a strategy. Three things actually retain newly skilled staff, and none of them is a counter-offer.</p>
<p>First, progression. Data product ownership and evaluation leadership must be written into the career framework as senior, compensated, and visible. If the new operating model reads as a lateral move from building to documenting, the people you trained will leave for organisations that recognise the seniority. Second, interesting work. People who have just learned to build evaluation suites want to build them for domains that matter, not to maintain a pilot nobody uses. Third, external profile: conference talks, published internal standards, and participation in communities give newly skilled staff a reason to stay that a salary match cannot.</p>
<p>Measure retention risk explicitly rather than discovering it in exit interviews. Track the share of critical capabilities held by a single person, the number of domains with only one qualified owner, and whether your newly trained staff are getting work that uses their new skills. Capability concentration is the risk that turns a successful upskilling programme into a liability: you have invested in people who are now both essential and highly portable. The mitigation is the same discipline that governs data products — document the contract, cross-train a second owner, and make the knowledge an asset of the organisation rather than of the individual.</p>
<p>Done well, the hiring-versus-upskilling question stops being an argument between two functions and becomes a quarterly allocation review with evidence attached. That is the point at which AI talent strategy becomes a strategy: not a plan to acquire scarce people, but a plan to build a capability that outlasts the market conditions that made it look scarce.</p>
"""

EN_FAQ = [
    ("Should we hire AI specialists or upskill existing staff?",
     "Both, allocated role by role. Hire for durable, method-heavy disciplines with no internal bench — evaluation leadership, specialist platform engineering, research-grade machine learning if you truly build proprietary models. Grow roles where the binding constraint is internal context — data product ownership, semantic modelling, and AI enablement. Applying one answer across the whole function is the mistake."),
    ("How long does it take to upskill an existing data team for AI work?",
     "Roughly one quarter to productive in semantic modelling and data product ownership, and about six weeks to design and run an evaluation suite — provided the learning is attached to a live deliverable with a real deadline. Without a live deliverable, expect three times the duration and significantly lower retention of the material."),
    ("Is it cheaper to upskill than to hire?",
     "Usually on a cost-to-productivity basis, though not on headline salary. The hiring path carries a salary premium, recruiting fees, a vacancy period, and two to three quarters of ramp before independent productivity. The upskilling path carries training cost and the protected capacity you must ring-fence. When both are modelled honestly, upskilling wins for context-heavy roles and hiring wins for durable deep specialisms."),
    ("How do we stop newly upskilled staff from leaving?",
     "Three things work: written career progression that treats data product ownership and evaluation leadership as senior and compensated, genuinely interesting work on domains that matter, and external profile through talks, published standards and community participation. Also measure capability concentration — if one person is the sole owner of a critical capability, cross-train a second owner before you need to."),
    ("What is a sensible ratio between hiring and upskilling?",
     "A common starting point is roughly one external specialist hire for every four to six internal conversions, adjusted by role criticality. More useful than the ratio itself is funding the horizons separately: services for capability you need within two quarters, permanent hiring for proven needs over four to eight quarters, and upskilling for the structural shift over eighteen months and beyond."),
]

ZH_TOC = [
    ('为什么招聘与提升的决策常常靠拍脑袋', '为什么"招聘还是提升"的决策常常靠拍脑袋？'),
    ('两条路径上AI人才的真实成本是多少', '两条路径上 AI 人才的真实成本是多少？'),
    ('哪些角色该招、哪些角色该自己培养', '哪些角色该招、哪些角色该自己培养？'),
    ('如何构建人才组合而非押注单一方案', '如何构建人才组合而非押注单一方案？'),
    ('技能提升多快能补上缺口', '技能提升多快能补上缺口？'),
    ('如何留住你刚刚培养出来的人', '如何留住你刚刚培养出来的人？'),
]

ZH_PROSE = """
<p class="article-lead"><strong>大多数 AI 人才战略其实算不上战略。它们只是一份招聘计划，附上了"转型"这个词，用一份显示稀缺专家薪酬高企的市场基准来论证必要性，最后以"希望内部员工总有一天能跟上"收尾。</strong>"招聘还是提升"并不是一个意识形态问题，对每个角色的答案也并不相同。它是一道含三个变量的算术题：你能等多久、这个角色需要多少领域上下文、以及这项能力是持久的，还是两年内就会被商品化。本文给出按角色拆解这一决策的框架、两条路径各自真实的成本与时间模型，以及一种能撑过下一个预算周期、而不只是撑过下一篇头条的组合式打法。</p>
<h2 id="为什么招聘与提升的决策常常靠拍脑袋">为什么"招聘还是提升"的决策常常靠拍脑袋？</h2>
<p>有三股力量把组织推向拍脑袋。其一是基准焦虑：公开的 AI 专家薪酬数据确实令人心惊，它把对话锚定在价格上，而不是价值与时机上。其二是两条路径分别由职能不同、激励不同的部门主张——人才获取部门的使命是填满岗位需求，学习发展部门的使命是建设能力，而能终结这场争论的业务结果，两个部门都不拥有。其三是大多数组织说不清自己到底需要什么能力，因此也就无法比较获取它的两种方式。</p>
<p>最后一点是可以修的。"我们需要 AI 人才"不是需求；"我们需要一个能在一个季度内把我们的收入确认逻辑表达为版本化、可测试的语义模型，并为之负责两年的人"才是需求。而一旦这样表述，答案往往显而易见——因为真正的约束条件原来是领域知识，而不是机器学习专长。</p>
<p>决策被拍脑袋的第二个原因，是两条路径被放在了错误的坐标轴上比较。招聘是启动快、见效慢：一位新专家在企业语境下通常需要两到三个季度才能达到完全产出，因为技术能力第一天就到位，而上下文要花几个月。提升是启动慢、见效快：内部候选人对定义、政治与系统早已了然，所以他们学到的东西能立刻被应用。按人均成本比较，两条曲线都被漏掉了。</p>
<p>最后，组织还系统性地低估了"折旧"这个问题。有些 AI 能力每个季度都在变得更便宜、更自动化——例如基础模型集成正在迅速被平台吸收；而另一些能力在升值：评估设计、语义建模，以及决定"自动化必须在哪里停下"的治理判断。为一项十八个月内就会被商品化的能力支付溢价，是一笔糟糕的买卖；为持久的判断力支付溢价，往往是笔好买卖。</p>
<h2 id="两条路径上AI人才的真实成本是多少">两条路径上 AI 人才的真实成本是多少？</h2>
<p>诚实的比较必须计入"到产出为止"的成本，而不是"到接受 offer 为止"的成本。招聘路径上，要预算：相对同级资深工程师的薪酬溢价、猎头费用或内部招聘投入、岗位空缺期，以及——最大也最少被计入的一项——在独立产出之前两到三个季度的爬坡期。还要加上内部人员帮其入职的机会成本，头一个月这轻易就占掉一位资深工程师五分之一的时间。</p>
<p>提升路径上，要预算：直接的培训费用、为了让员工边交付边学习而必须圈留的产能、团队采用新方法期间暂时的产出下滑，以及"避免了一次错招"的价值。最后一项被严重低估：内部候选人有已知的绩效记录，而外部 AI 人才是在一个"证书与企业交付能力弱相关"的市场里被挑选出来的。</p>
<table class="article-table"><thead><tr><th>成本与时间因素</th><th>外部招聘</th><th>内部提升</th><th>实务提示</th></tr></thead><tbody><tr><td>开始贡献所需时间</td><td>发 offer 后 4-8 周</td><td>立即</td><td>内部员工已具备上下文与权限</td></tr><tr><td>达到完全产出所需时间</td><td>2-3 个季度</td><td>1-2 个季度</td><td>招聘路径上爬坡的是上下文，不是技能</td></tr><tr><td>直接成本</td><td>薪酬溢价 + 费用</td><td>培训 + 替补产能</td><td>溢价看得见，圈留的产能看不见</td></tr><tr><td>所需领域上下文</td><td>必须重新获取</td><td>已经具备</td><td>对治理与语义类角色具有决定性</td></tr><tr><td>留任风险</td><td>高；技能可迁移、市场火热</td><td>中等；有忠诚红利</td><td>刚被提升的员工同样刚变得更抢手</td></tr><tr><td>能力持久性</td><td>适合持久、深入的专业方向</td><td>适合正被平台吸收的能力</td><td>让路径匹配折旧曲线</td></tr></tbody></table>
<p>当你诚实地建好这个模型，一个清晰的规律就浮现出来：需要深厚、持久、可迁移专业能力的角色适合招聘；需要领域上下文、定义判断力，或正在向标准工具收敛的能力的角色适合内部提升。真正的错误，是把同一个答案套用到整个职能上。</p>
<h2 id="哪些角色该招、哪些角色该自己培养">哪些角色该招、哪些角色该自己培养？</h2>
<p>拆解这个决策最有用的方式，是对每个角色问两个问题：它是否需要只存在于你组织内部的上下文？其底层技能两年后是否仍享有溢价？</p>
<ol>
<li><strong>招聘：评估与 AI 质量负责人。</strong>这是一门持久且重方法论的学科，有真正的手艺含量——黄金集设计、回归策略、抽样机制、事故分类。它也是多数企业从未建立过的学科，因此没有内部人才储备可供培养。招一位负责人，再在其下培养团队。</li>
<li><strong>培养：数据产品负责人。</strong>其约束条件在于知道哪些定义存在争议、以及为什么。这种知识天然是内部的。提拔一位资深分析师或工程师，给予明确的问责、契约模板与辅导。</li>
<li><strong>招聘：专业基础设施与平台工程</strong>，针对那些你会持续运行多年的能力——模型服务、向量基础设施、可观测性。这些是手艺深厚、折旧曲线很长的方向。</li>
<li><strong>培养：语义建模与分析工程。</strong>工具会趋同，业务逻辑不会。你现有的 BI 与分析工程师，比任何不熟悉你科目表的外部人选都更接近这个岗位。</li>
<li><strong>培养：AI 赋能与采用伙伴。</strong>这类角色八成靠领域可信度、两成靠技术流利度。外部招聘在这个岗位上必然失败，因为业务单元不会信任一个聊不透他们运营节奏的人。</li>
<li><strong>选择性招聘：研究级机器学习。</strong>仅当你确实在构建自有模型时才需要。多数企业并没有，也不该在招聘计划里装作有。</li>
</ol>
<p>关于"培养"清单有一条提醒：培养能力需要真实的课程设计，而不是一个视频库的使用许可。上述岗位要通过"在真实迁移项目上做学徒"来变得高产——把一张现有看板改造成受治理的数据产品、为一个领域搭建评估套件、跑通第一个对话式试点。要为这件工作做预算，而不只是为课程做预算。</p>
<h2 id="如何构建人才组合而非押注单一方案">如何构建人才组合而非押注单一方案？</h2>
<p>组合式打法把招聘与提升视为风险特征互补的两种工具，并有意地在三个时间跨度上分配。跨度一覆盖未来两个季度：用承包商、托管服务或平台伙伴，交付你马上需要、但未必长期需要的能力。大部分"我们必须招人"的恐慌都落在这里，而它往往更适合用一次服务合作来解决，而不是用一个岗位需求。</p>
<p>跨度二覆盖未来四到八个季度：这才是长期招聘应当发生的地方。走到这个跨度时，你已经知道哪些能力在你的环境里真正持久，因为你已经跑过真东西了。向一个已被验证的需求招聘，能把一次昂贵的实验转化为一笔合理的投资。</p>
<p>跨度三覆盖十八个月以上的结构性转变：这才是内部提升的位置。它慢、它会复利，而且它是唯一能改变组织基线、而不是增加几个杰出个体的路径。典型的失败模式是把跨度三当成紧急事项——宣布一个再培训项目，指望一个季度见成效，然后得出"内部提升不管用"的结论。</p>
<ul>
<li><strong>分列预算。</strong>把三个跨度混在一个预算里，结果一定是紧急的吃掉结构性的。</li>
<li><strong>设定比例并为之辩护。</strong>常见的起始配比是每四到六名内部转化配一位外部专家招聘，再按角色关键性调整。</li>
<li><strong>把折旧假设写下来。</strong>对每一项计划招聘的能力，写明你是否相信它两年后仍享有溢价，并每年复核。</li>
<li><strong>用服务买时间，而不是用来回避决策。</strong>任何托管合作都应附带明确的知识转移义务。</li>
<li><strong>跟踪能力，而不是人数。</strong>衡量"有多少个领域具备了具名的数据产品负责人与通过的评估套件"，而不是"有多少名 AI 员工"。</li>
</ul>
<h2 id="技能提升多快能补上缺口">技能提升多快能补上缺口？</h2>
<p>诚实的答案是：比多数招聘计划快，比多数培训供应商宣称的慢。一位称职的分析工程师，可以在一个季度内在语义建模与数据产品 ownership 上变得高产——前提是（这正是关键条件）学习被挂在一个有真实截止日的在办交付物上。一位称职的分析师，在同样条件下大约六周就能学会设计并运行评估套件。没有在办交付物，两者耗时都要翻三倍，而且其中一半会蒸发掉。</p>
<p>行之有效的顺序在各组织间高度一致。从评估开始，因为它是让委派变得安全的技能，且不需要任何新基础设施；接着进入语义建模，因为把业务逻辑表达为版本化模型，是此后一切所消费的地基；然后再补充检索与依据相关的概念，这主要是理解你整理好的数据产品如何被使用；把模型训练与微调放到最后，因为多数企业最终会发现自己很少需要它。</p>
<p>能加速这一步的，是卸掉基础设施负担的平台。当团队无需搭建服务栈，就能通过企业微信、钉钉、飞书、Teams 或 WhatsApp 中的对话界面，对受治理的数据提问时，课程内容就塌缩到了真正重要的部分：定义、评估与判断力。这正是蜂启咨询以托管服务方式交付对话式分析的原因——约两周即可在你已在运行的仓库之上部署，它把十八个月的能力建设压缩成两周的起点，让你的团队在真实工作中学到那些持久的技能，而不是在日后会被丢弃的脚手架上学习。</p>
<h2 id="如何留住你刚刚培养出来的人">如何留住你刚刚培养出来的人？</h2>
<p>关于内部提升，有一个令人不安的事实：它让你的员工变得更抢手。标准应对——指望忠诚能解决问题——并不是战略。真正能留住刚被培养出来的员工的有三样东西，没有一样是临时加薪挽留。</p>
<p>第一，晋升通道。数据产品 ownership 与评估负责人，必须被写进职业发展框架，明确为高级别、有相应薪酬、且有可见度。如果新运营模式读起来像一次从"建设"到"写文档"的平调，你培养出来的人就会投奔那些认可这份资历的组织。第二，有意思的工作。刚学会搭建评估套件的人，想的是为真正重要的领域去搭建，而不是维护一个没人用的试点。第三，外部声望：会议演讲、公开发布的内部标准、以及参与专业社区，会给新晋员工一个薪资匹配给不了的留下理由。</p>
<p>要显式地度量留任风险，而不是等到离职面谈时才发现。跟踪：关键能力由单人掌握的比例、只有一名合格负责人的领域数量、以及你刚培养的员工是否拿到了能用到新技能的工作。能力集中，正是让一次成功的内培项目变成负债的风险——你投资的人如今既不可或缺，又高度可迁移。缓解办法与治理数据产品的是同一条纪律：把契约文档化，培养第二负责人，让知识成为组织的资产，而不是个人的资产。</p>
<p>做好之后，"招聘还是提升"就不再是一场两个部门之间的争论，而成了一场附有证据的季度配置评审。这也正是 AI 人才战略成为战略的时刻：它不是一份获取稀缺人才的计划，而是一份构建能力的计划——这份能力，要比当初让它显得稀缺的市场行情活得更久。</p>
"""

ZH_FAQ = [
    ("我们应该招聘 AI 专家，还是提升现有员工？",
     "两者都要，并按角色分配。为那些持久、重方法论且没有内部人才储备的学科而招聘——评估负责人、专业平台工程、以及（仅当你确实在构建自有模型时）研究级机器学习。为那些约束条件在于内部上下文的角色而培养——数据产品负责人、语义建模、AI 赋能伙伴。把同一个答案套用到整个职能，才是真正的错误。"),
    ("让现有数据团队具备 AI 工作能力需要多久？",
     "在语义建模与数据产品 ownership 上大约一个季度可以达到产出，在设计与运行评估套件上大约六周——前提是学习被挂在一个有真实截止日的在办交付物上。缺少在办交付物，耗时大约要翻三倍，而且所学内容的留存率会显著下降。"),
    ("内部提升是否比招聘更便宜？",
     "按「到产出为止」的成本计算通常是，尽管按表面薪酬未必。招聘路径要承担薪酬溢价、猎头费用、岗位空缺期，以及独立产出前两到三个季度的爬坡期；提升路径要承担培训费用与必须圈留的产能。当两者都被诚实建模后，上下文密集型的角色适合提升，而持久的深厚专业方向适合招聘。"),
    ("如何防止刚培养出来的员工离职？",
     "有三样东西有效：把数据产品 ownership 与评估负责人写进职业发展框架，明确为高级别且有相应薪酬；提供真正有意思的、作用于重要领域的工作；以及通过演讲、发布内部标准与参与社区来给予外部声望。同时要度量能力集中度——若某项关键能力只有一人掌握，在你需要之前就培养第二负责人。"),
    ("招聘与提升之间合理的配比是多少？",
     "常见的起点是每四到六名内部转化配一位外部专家招聘，再按角色关键性调整。比配比本身更有用的，是把时间跨度分开列支：两季度内需要的能力用服务解决；四到八个季度内已被验证的需求做长期招聘；十八个月以上的结构性转变靠内部提升。"),
]

cc = OpenCC('s2twp')
to_tw = cc.convert
TW_TOC = [(i, to_tw(t)) for i, t in ZH_TOC]

def main():
    patch.apply(os.path.join(ROOT, 'blog/articles/%s.html' % SLUG), EN_TOC, EN_PROSE, EN_FAQ, cta='Book a Demo')
    patch.apply(os.path.join(ROOT, 'zh-cn/blog/articles/%s.html' % SLUG), ZH_TOC, ZH_PROSE, ZH_FAQ, cta='预约演示')
    patch.apply(os.path.join(ROOT, 'zh-tw/blog/articles/%s.html' % SLUG), TW_TOC, to_tw(ZH_PROSE),
                [(to_tw(q), to_tw(a)) for q, a in ZH_FAQ], cta='預約示範')

if __name__ == '__main__':
    main()
