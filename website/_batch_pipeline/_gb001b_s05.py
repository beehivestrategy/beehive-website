#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""slug 05: building-a-data-driven-culture-from-strategy-to-practice
EN 1357 -> ~2600 ; CN/TW 1992 -> ~3600 ; build FAQ section from scratch ; H2 -> questions."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gb001b_lib import path_of, retitle_h2, build_faq, s2t_fixed

SLUG = "building-a-data-driven-culture-from-strategy-to-practice"
NAV = '            <nav class="article-nav" aria-label="Article navigation">'

EN_NEWS = """<h2 id="why-do-data-driven-culture-programmes-fail">Why Do Most Data-Driven Culture Programmes Fail?</h2>
<p>The failure is rarely a lack of ambition. Most organisations that announce a data-driven transformation mean it, fund it, and staff it. They fail on a narrower point: they try to change behaviour without changing the conditions that produce behaviour. A team that is told to be data-driven, and then has to file a ticket and wait five days for an answer, will revert to intuition within a month — not because it resists data, but because the workflow punishes asking. Culture is not what people believe; it is what the system makes easy. Change the system and the belief follows.</p>
<p>The second failure mode is treating culture as a communications problem. Posters, town halls, and a slogan on the intranet produce awareness, not practice, and awareness without a changed workflow decays quickly. The programmes that work instrument the behaviour instead: they count how many decisions cite data, how many people can reach data unaided, and how many requests end in a usable answer. Numbers like these create accountability in a way that messaging cannot, because they make the gap between stated intent and daily practice visible to the people responsible for closing it.</p>
<p>The third failure mode is the initiative cliff. Culture programmes are launched with executive sponsorship, run for two or three quarters, and then dissolve when the sponsor changes role or the budget cycle turns. Because the underlying workflows were never rebuilt, the organisation snaps back to its prior equilibrium. Programmes that survive treat the first year as infrastructure building — access, definitions, literacy, and scorecards — rather than as a campaign with an end date, and they deliberately hand ownership to line managers rather than leaving it with a central team that will eventually be reorganised.</p>
<h2 id="how-should-you-sequence-the-change">How Should You Sequence a Culture Change Programme?</h2>
<p>Sequencing matters more than intensity, because the levers depend on each other. Access comes first: if people cannot reach data, literacy training has nothing to practise on and leadership exhortation rings hollow. But access without trusted definitions is worse than no access, because the first inconsistent number teaches the organisation to distrust everything downstream. So the real first step is a modest semantic foundation — the fifteen to thirty metrics that carry most decisions, defined once, with named owners, published where users can read them.</p>
<p>Once answers are trustworthy, democratise the interface. Put governed natural-language access into the channels people already use, so that asking costs nothing and waiting is unnecessary. Then, and only then, invest heavily in literacy — because literacy training lands when a learner can immediately apply it to a live question they actually have. Rewards and scorecards come last, not because they are least important but because recognising data-driven behaviour before the infrastructure supports it rewards people for working around the system.</p>
<p>A practical twelve-month sequence looks like this: months one to three, define the core metrics and stand up governed access for a pilot function; months four to six, extend access through conversational interfaces and begin literacy workshops tied to real questions; months seven to nine, publish the scorecard and tie recognition to evidence-based decisions; months ten to twelve, hand ownership to line managers and audit coverage gaps. Organisations that compress this sequence usually find that adoption stalls at exactly the step they skipped.</p>
<h2 id="what-does-this-look-like-in-practice">What Does a Data-Driven Culture Look Like in an Operational Function?</h2>
<p>The abstractions become concrete in an operational setting, and manufacturing supply planning is a useful example because the decisions are frequent, measurable, and expensive. In a plant where planners have historically sequenced production from experience, the shift begins by giving planners direct access to the same demand, inventory, and capacity data the central planning team uses — with one definition of available stock, agreed in advance. The first visible change is not a decision but a conversation: planners start challenging the schedule with specific numbers, and the schedule improves because the challenges are grounded.</p>
<p>The second change is the meeting. A weekly planning review that previously opened with status reports opens instead with exceptions — the lines where demand and capacity diverge beyond tolerance, ranked by cost of the gap. That reordering is the culture in miniature: attention goes first to where the data says something is wrong, rather than to whoever speaks most confidently. Within two quarters, the measurable outcomes follow — fewer expedited shipments, lower safety stock at the same service level, and a planning cycle that shortens because fewer questions require escalation.</p>
<p>The generalisable lesson is that culture change in an operating function is really a change in what the team looks at first. Any function with a recurring review — sales pipeline, claims triage, procurement spend, store operations — can make the same move: define the metrics once, surface the exceptions automatically, and require that the review starts with them. Functions that do this stop debating whose numbers are right, because there is only one set, and start debating what to do about them, which is the conversation the data was always meant to enable.</p>
<h2 id="how-do-you-sustain-the-culture">How Do You Sustain the Culture Through Leadership and Reorganisation?</h2>
<p>The most common question from executives who have built a data-driven culture once is how to keep it. Three mechanisms do most of the work. The first is embedding the practice in artifacts that outlive individuals: decision logs that record the data behind major calls, metric definitions with named owners that survive reorganisations, and review templates that require the exception list before the status update. Artifacts carry practice across leadership changes because a new executive inherits a working rhythm rather than a blank page.</p>
<p>The second is distributing ownership. A culture owned by a central analytics team is one reorganisation away from disappearing; a culture owned by line managers, who are measured on the same scorecard and trained in the same literacy programme, has dozens of carriers. The central team's role shifts from owner to enabler — maintaining the semantic layer, running the literacy programme, and publishing the scorecard — while the practice itself lives where the decisions are made.</p>
<p>The third is keeping the scorecard public. Publishing decision-citation rates, self-service access rates, and request satisfaction to the same leadership group every quarter makes regression visible early, and visibility is usually sufficient to correct it. Culture decays quietly, in the gap between two reorganisations, when nobody is measuring; a scorecard that nobody can quietly stop publishing is the cheapest insurance available.</p>
"""

ZH_NEWS = """<h2 id="为什么多数数据驱动文化项目会失败">为什么多数数据驱动文化项目会失败？</h2>
<p>失败很少源于缺乏雄心。大多数宣布要做数据驱动转型的组织，是真的想做、也真的投了钱、配了人。它们失败在一个更窄的点上：试图在不改变行为产生条件的前提下改变行为。一个被要求"用数据说话"、却必须提工单、等五天才拿得到答案的团队，一个月内就会退回凭直觉决策——不是因为它抗拒数据，而是因为这套流程在惩罚提问。文化不是人们相信什么，而是系统让什么变得容易。改系统，信念自会跟上。</p>
<p>第二种失败模式是把文化当成传播问题。海报、全员大会、内网口号带来的是认知，而不是实践；没有工作流支撑的认知会很快衰减。真正奏效的项目是给行为装上仪表：统计有多少决策引用了数据、有多少人能独立取到数据、有多少数据请求最终得到了可用的答案。这类数字能创造出传播做不到的问责，因为它们把"宣称的意图"与"日常的实践"之间的差距，摆在了本该负责弥合它的人面前。</p>
<p>第三种失败模式是"项目悬崖"。文化项目带着高管发起人的支持启动，跑两三个季度，然后在发起人换岗或预算周期切换时解散。由于底层工作流从未被重建，组织会弹回原来的均衡点。能存活下来的项目把第一年当作基础设施建设——访问、口径、素养、计分卡——而不是一场有终点日的运动，并且会有意把所有权交给一线管理者，而不是留在一个终将被重组掉的中央团队手里。</p>
<h2 id="文化变革应当如何排序推进">文化变革应当如何排序推进？</h2>
<p>排序比力度更重要，因为这几根杠杆彼此依赖。访问排在第一位：如果人们拿不到数据，素养培训就没有可练的对象，领导的号召也显得空洞。但缺乏可信口径的访问比没有访问更糟，因为第一个对不上的数字会让组织从此怀疑下游的一切。所以真正的第一步是一个小规模的语义基础——承载大部分决策的那十五到三十个指标，一次性定义清楚，有具名负责人，并发布在用户可以查阅到的地方。</p>
<p>当答案变得可信之后，再把访问界面民主化。把受治理的自然语言访问放进人们已经在用的渠道里，让提问零成本、等待无必要。然后——也只有到这时——才大规模投入素养建设，因为只有当学习者能立刻把所学用在自己手上真实存在的问题上时，培训才落得下去。奖励与计分卡放在最后，不是因为它们最不重要，而是因为在基础设施尚未就位时就表彰"数据驱动行为"，等于在奖励那些绕开系统做事的人。</p>
<p>一个可操作的十二个月序列大致是：第一至三个月，定义核心指标，为试点职能搭建受治理的访问；第四至六个月，通过对话式界面扩展访问，并结合真实问题启动素养工作坊；第七至九个月，发布计分卡，并把表彰与循证决策挂钩；第十至十二个月，把所有权交给一线管理者，并审计覆盖缺口。压缩这个序列的组织通常会发现，采用率恰好停在它们跳过的那一步。</p>
<h2 id="数据驱动文化在业务职能中是什么样">数据驱动文化在一个业务职能中是什么样？</h2>
<p>这些抽象原则落到具体运营场景里才会变得清晰，制造业的供应计划是个好例子，因为那里的决策频繁、可度量、且代价高昂。在一个计划员历来凭经验排产的工厂里，转变始于让计划员直接取用中央计划团队所用的同一套需求、库存与产能数据——并且"可用库存"只有一个事先达成共识的口径。第一个看得见的变化不是某个决策，而是对话方式：计划员开始用具体数字挑战排程，而排程之所以改善，正因为这些挑战是有依据的。</p>
<p>第二个变化是会议。原本以状态汇报开场的周度计划评审，改为例外开场——需求与产能偏离超出容差的产线，按缺口成本排序。这个重排就是文化的缩影：注意力先投向数据指出有问题的地方，而不是投向说话最自信的那个人。两个季度之内，可度量的结果就会跟上：加急发运减少、在同等服务水平下安全库存下降、计划周期因为更少问题需要升级而缩短。</p>
<p>可以推广的经验是：运营职能里的文化变革，本质上就是"团队先看什么"的改变。任何有周期性评审的职能——销售管线、理赔分诊、采购支出、门店运营——都可以做同样的动作：一次性定义指标，自动浮现例外，并要求评审从例外开始。做到这一点的职能会停止争论"谁的数是对的"，因为数只有一套；转而争论"该怎么办"，而这才是一开始引入数据时想要促成的对话。</p>
<h2 id="如何让文化在领导更替中延续">如何让文化在领导更替与组织重组中延续？</h2>
<p>已经建成过一次数据驱动文化的管理者，最常问的是如何保持。三项机制承担了大部分工作。第一是把实践嵌入比个人更长寿的载体：记录重大决策背后数据的决策日志、在重组中依然有具名负责人的指标口径、以及要求在状态汇报之前先过例外清单的评审模板。载体让实践跨越领导更替，因为新任高管继承的是一套已经运转的节奏，而不是一张白纸。</p>
<p>第二是分散所有权。由中央分析团队拥有的文化，距离消失只差一次重组；由一线管理者拥有的文化则有几十个承载者——他们被同一张计分卡度量，受过同一套素养训练。中央团队的角色从所有者转为赋能者：维护语义层、运营素养项目、发布计分卡；而实践本身活在决策发生的地方。</p>
<p>第三是让计分卡保持公开。每季度向同一个管理层发布决策引用率、自助取数覆盖率与请求满意度，能让倒退在早期就变得可见，而可见性通常足以纠正它。文化是安静地衰败的，衰败发生在两次重组之间没人度量的那段时间里；一张谁都无法悄悄停发的计分卡，就是能买到的最便宜的保险。</p>
"""

EN_FAQ = [
    ("How long does it take to build a data-driven culture?",
     "Most organisations see measurable behavioural change within nine to eighteen months, but the sequence matters more than the clock. Expect three to six months to establish governed access and a core set of agreed metrics, a further three months for conversational access and literacy to take hold, and six to twelve months before decision-citation rates shift durably. Programmes that promise transformation in a quarter usually produce a campaign rather than a culture."),
    ("Is a data-driven culture possible without a semantic layer?",
     "It is possible but unstable. Culture depends on people trusting the numbers they are asked to use, and trust collapses the first time two teams produce different answers to the same question. A semantic layer — metrics defined once, with named owners and governed filters — is what makes the same question return the same answer across dashboards, exports, and conversational interfaces. Without it, democratised access amplifies inconsistency instead of enabling decisions."),
    ("What is the single highest-leverage first step?",
     "Require a data point for every major decision in executive meetings, and make access to that data point fast and governed. The leadership habit creates permission and accountability at once, while the access removes the friction that otherwise punishes asking. Organisations that start with tools or training, without changing either the meeting or the workflow, tend to see enthusiasm decay after the first quarter."),
    ("How do you measure culture rather than activity?",
     "Track outcomes, not usage. Useful indicators include the share of major decisions that cite data, the share of employees who can answer a question without filing a ticket, and the share of data requests that end in a usable answer. Dashboard login counts and licence utilisation measure activity and are easy to inflate; decision-citation and self-service rates measure whether the culture has actually shifted."),
    ("What should you do when leaders bypass the data?",
     "Treat it as a signal about the system rather than the individual. Leaders bypass data when it is too slow, too ambiguous, or contradicts a definition they do not accept. Ask which of the three applied: if the answer is speed, invest in access; if ambiguity, invest in the semantic layer; if definition, escalate to the metric owner. Publicly correcting the behaviour without fixing the cause teaches the organisation that the data is theatre."),
]

CN_FAQ = [
    ("建立数据驱动文化需要多长时间？",
     "多数组织在九到十八个月内能看到可度量的行为变化，但排序比时间更重要。通常三到六个月用于搭建受治理的访问与一套达成共识的核心指标；再三个月让对话式访问与素养建设落地；六到十二个月之后，决策引用率才会发生持久变化。承诺一个季度完成转型的项目，产出的通常是一场运动，而不是一种文化。"),
    ("没有语义层，能建成数据驱动文化吗？",
     "可以，但不稳定。文化依赖人们信任被要求使用的数字，而当两个团队对同一个问题给出不同答案的那一刻，信任就崩塌了。语义层——指标一次性定义、有具名负责人、过滤器受治理——正是让同一个问题在仪表板、导出表格与对话式界面中返回同一个答案的机制。没有它，民主化的访问放大的是不一致，而不是决策能力。"),
    ("杠杆率最高的第一步是什么？",
     "要求高管会议上的每项重大决策都必须有数据支撑，并让这个数据的获取既快又受治理。领导的习惯同时创造了许可与问责，而访问消除了那些惩罚提问的摩擦。从工具或培训入手、却既不改会议也不改工作流的组织，往往在第一季度之后就看到热情衰减。"),
    ("如何度量文化而不是度量活动量？",
     "追踪结果，而非使用量。有用的指标包括：引用数据的重大决策占比、无需提工单即可回答问题的员工占比、以及最终得到可用答案的数据请求占比。仪表板登录次数与许可证利用率度量的是活动量，且容易被注水；决策引用率与自助服务率度量的才是文化是否真的转变了。"),
    ("当领导者绕过数据时该怎么办？",
     "把它当作关于系统的信号，而不是关于个人的信号。领导者绕过数据，通常是因为数据太慢、含义不清，或者与某个他们并不接受的口径相矛盾。先问是三者中的哪一种：如果是速度问题，就投资访问；如果是歧义问题，就投资语义层；如果是口径问题，就升级给指标负责人。只公开纠正行为却不修好根因，会让组织认为数据只是一场表演。"),
]

EN_H2 = [
    ("leadership-sets-the-tone", "Leadership Sets the Tone", "How Does Leadership Set the Tone for a Data-Driven Culture?"),
    ("democratise-data-access", "Democratise Data Access", "How Do You Democratise Data Access Without Losing Control?"),
    ("reward-data-driven-behaviour", "Reward Data-Driven Behaviour", "How Should You Reward Data-Driven Behaviour?"),
    ("build-data-literacy", "Build Data Literacy", "What Does Data Literacy Actually Require?"),
    ("key-takeaways", "Key Takeaways", "What Are the Key Takeaways?"),
    ("conclusion", "Conclusion", "Where Should You Start?"),
]
CN_H2 = [
    ("领导力定下基调", "领导力定下基调", "领导力如何为数据驱动文化定调？"),
    ("数据访问民主化", "数据访问民主化", "如何在不失控的前提下实现数据访问民主化？"),
    ("奖励数据驱动的行为", "奖励数据驱动的行为", "应当如何奖励数据驱动的行为？"),
    ("培养数据素养", "培养数据素养", "数据素养到底需要什么？"),
    ("要点", "要点", "核心要点是什么？"),
    ("结论", "结论", "你应该从哪里开始？"),
]
TW_H2 = [
    ("領導力定下基調", "領導力定下基調", "領導力如何爲數據驅動文化定調？"),
    ("數據訪問民主化", "數據訪問民主化", "如何在不失控的前提下實現數據訪問民主化？"),
    ("獎勵數據驅動的行爲", "獎勵數據驅動的行爲", "應當如何獎勵數據驅動的行爲？"),
    ("培養數據素養", "培養數據素養", "數據素養到底需要什麼？"),
    ("要點", "要點", "核心要點是什麼？"),
    ("結論", "結論", "你應該從哪裏開始？"),
]

if __name__ == "__main__":
    # EN: body + FAQ
    en = path_of(SLUG, "en")
    h = open(en, encoding="utf-8").read()
    assert h.count(NAV) == 1
    h = h.replace(NAV, "\n" + EN_NEWS + "\n" + build_faq(EN_FAQ, "en") + "\n" + NAV)
    open(en, "w", encoding="utf-8").write(h)
    print("EN body + FAQ done")

    # zh-CN
    cn = path_of(SLUG, "cn")
    h = open(cn, encoding="utf-8").read()
    assert h.count(NAV) == 1, h.count(NAV)
    h = h.replace(NAV, "\n" + ZH_NEWS + "\n" + build_faq(CN_FAQ, "cn") + "\n" + NAV)
    open(cn, "w", encoding="utf-8").write(h)
    print("CN body + FAQ done")

    # zh-TW (convert)
    tw = path_of(SLUG, "tw")
    h = open(tw, encoding="utf-8").read()
    assert h.count(NAV) == 1, h.count(NAV)
    tw_faq = [(s2t_fixed(q), s2t_fixed(a)) for q, a in CN_FAQ]
    h = h.replace(NAV, "\n" + s2t_fixed(ZH_NEWS) + "\n" + build_faq(tw_faq, "tw") + "\n" + NAV)
    open(tw, "w", encoding="utf-8").write(h)
    print("TW body + FAQ done")

    for hid, old, new in EN_H2:
        retitle_h2(en, hid, old, new)
    for hid, old, new in CN_H2:
        retitle_h2(path_of(SLUG, "cn"), hid, old, new)
    for hid, old, new in TW_H2:
        retitle_h2(path_of(SLUG, "tw"), hid, old, new)
    print("H2s converted")
