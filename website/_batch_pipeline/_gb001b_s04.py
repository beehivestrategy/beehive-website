#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""slug 04: anti-money-laundering-ai-detection
EN 1453 -> ~2800 ; CN/TW 2225 -> ~3750 ; H2 -> questions ; FAQ answers rewritten."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gb001b_lib import run, path_of, retitle_h2, s2t_fixed

SLUG = "anti-money-laundering-ai-detection"

EN_NEWS = """<h2 id="which-typologies-does-ai-detect-better">Which Laundering Typologies Does AI Detect Better Than Rules?</h2>
<p>Rules engines are good at what they are written for: a threshold, a velocity limit, a named-list match. They fail on typologies that are defined by shape rather than by amount, and that is exactly where machine learning earns its place. The clearest case is structuring — the deliberate splitting of transactions to stay below a reporting threshold. A rule catches the pattern it was configured for; a model catches the behavioural signature of an account whose transaction sizes have shifted toward the threshold, even when no individual transaction breaches one. Graph-based models extend the same logic across accounts, surfacing the hub-and-spoke patterns of mule networks where funds arrive from many unrelated sources and are rapidly forwarded onward.</p>
<p>Trade-based money laundering is the second area where models outperform, because the signal is relational and contextual rather than absolute: an invoice whose value sits far outside the range for that commodity and counterparty pair, a shipment route inconsistent with the stated trade relationship, repeated over- and under-invoicing concentrated in a small set of counterparties. Rules struggle here because the legitimate range varies by corridor and commodity; a model learns the range from the institution's own history and flags deviation from it. Correspondent and nested-account flows benefit similarly, since the risk inheres in the network position of the intermediary rather than in any single transaction.</p>
<p>The honest counterweight is that models are weaker where rules are strong. A sanctions screening match is deterministic, and a model should not sit in that path. A regulator-mandated threshold is a policy, not a prediction, and it should fire whether or not a model considers the case benign. The practical architecture keeps deterministic controls where compliance requires them and layers behavioural detection on top — not to replace the rules, but to find what the rules were never written to see.</p>
<h2 id="how-should-you-measure-aml-model-performance">How Should You Measure Whether an AML Model Is Actually Working?</h2>
<p>Model performance in AML is notoriously easy to measure wrongly, and the most common error is optimising the wrong metric. Accuracy is close to meaningless when confirmed cases are a fraction of a percent of alerts: a model that flags nothing is 99.9% accurate and worthless. The metrics that matter split into detection effectiveness and operational efficiency, and a deployment should be judged on both at once.</p>
<p>On detection, the useful measures are precision at the top of the queue — of the hundred highest-ranked alerts, how many were confirmed — and recall against a labelled holdout, expressed as the share of historical confirmed cases the model would have surfaced. Precision at top-of-queue is the more actionable of the two, because it maps directly onto how investigators actually work. Detection latency deserves a line as well: how quickly the model surfaces a case relative to the first transaction in the pattern, since a case identified after the funds have left is a case that will be written off.</p>
<p>On efficiency, the measures are false positive reduction against the incumbent rules engine, investigator hours per closed case, and SAR conversion rate — the share of investigated alerts that ultimately become filed reports. Together these three tell the honest story: a model that halves alert volume but also halves the conversion rate has not improved the programme, however good the headline reduction looks. The right frame is a single ratio — investigator hours per confirmed case — tracked monthly from the pre-deployment baseline, with alert volume and detection coverage reported alongside it so that neither efficiency nor coverage can be quietly traded away.</p>
<p>Two practices make those numbers trustworthy. Hold out a labelled evaluation set the model never trains on, refreshed periodically, so that performance claims are measured rather than asserted. And monitor input stability as well as score stability, because a shift in an input distribution — a new payment channel, a change in customer mix — will degrade a model months before the alert metrics move.</p>
<h2 id="what-features-matter-most">What Features Matter Most in an AML Detection Model?</h2>
<p>Feature engineering, not algorithm selection, is where most detection performance is won. The features that carry signal fall into four families. Velocity and deviation features compare an entity's recent behaviour against its own history: transaction count and value relative to a trailing baseline, changes in the mix of channels or counterparties, and the ratio of inbound to outbound flow. Network features describe position rather than behaviour — the number of distinct counterparties, the centrality of the account in a funds-flow graph, the share of value that passes through without being retained, and the graph distance to any known high-risk entity.</p>
<p>Peer-group features compare an entity against similar entities rather than against itself or a fixed threshold: this account against other accounts of the same segment, tenure, and declared purpose. This family is the most valuable and the most often missing, because it requires the segmentation work that fragmented data makes hard — yet it is what catches the anomaly that is unremarkable in absolute terms and suspicious only in context. Static risk features — geography, industry, product, customer due diligence rating, adverse media — supply the prior that the behavioural features then refine.</p>
<p>Two cautions apply. Features derived from fields whose meaning differs across source systems will leak those inconsistencies straight into the model, so every feature needs a documented definition and a lineage back to the source field. And features that encode protected characteristics, or close proxies for them, create fair-lending and discrimination exposure that no amount of detection performance justifies; these should be excluded deliberately and the exclusion documented, rather than discovered during an examination.</p>
<h2 id="what-does-model-risk-management-require">What Does Model Risk Management Require From an AML Deployment?</h2>
<p>Regulators do not ask whether a model works; they ask whether the institution can demonstrate that it knows how well it works. That distinction is the whole of model risk management, and it translates into four artefacts an examination will look for. The first is documented validation: an independent review of the model's development, data lineage, methodology, and performance, carried out by people who did not build it, with findings tracked to remediation. The second is explainability at the case level — every alert should carry the features and relationships that drove its score, in a form an investigator can read and a supervisor can audit.</p>
<p>The third is ongoing monitoring with pre-agreed thresholds. Accuracy, alert volume, and input stability should be tracked against expected ranges, with a defined action when a threshold is breached: investigate, recalibrate, retrain, or suspend and fall back to rules. A monitoring plan without a decision tree is documentation, not control. The fourth is change management: versioning of the model, the training data, and the feature definitions, with a record of every promotion to production and the evidence that supported it.</p>
<p>Beyond the four artefacts, two practices consistently distinguish programmes that satisfy supervisors from those that struggle. The first is a champion-challenger arrangement, in which an alternative approach runs in parallel and is periodically benchmarked, demonstrating that the incumbent was chosen on evidence rather than inertia. The second is treating investigator feedback as labelled training data in a governed loop — overrides recorded with reasons, fed back into retraining on a schedule, and the resulting performance change measured. That loop is what turns a model from a static artefact into a programme that improves, and it is the strongest single evidence an institution can offer that its deployment is under control.</p>
"""

ZH_NEWS = """<h2 id="哪些洗钱手法ai比规则更擅长">哪些洗钱手法是AI比规则更擅长识别的？</h2>
<p>规则引擎擅长它被写下来的东西：一个阈值、一个速度上限、一次名单命中。它处理不了那些由"形态"而非"金额"定义的手法，而这恰恰是机器学习立身之处。最典型的例子是拆分交易——为规避申报门槛而刻意拆分交易金额。规则只能抓住被配置过的形态；模型抓住的则是账户交易金额整体向阈值靠拢的行为特征，即使没有任何单笔交易真正触线。基于图的模型把同一逻辑扩展到账户之间，识别出马仔账户网络的中心—辐条结构：资金从多个互不相关的来源汇入，再被迅速转出。</p>
<p>贸易型洗钱是模型第二个明显占优的领域，因为这里的信号是关系性与情境性的，而非绝对的：一张发票的金额明显偏离该商品与该交易对手组合的正常区间；一条运输路线与申报的贸易关系不符；同一小撮交易对手之间反复出现的高开与低开发票。规则在这里力不从心，因为合理区间随通道与商品而变；模型则从机构自身的历史中学会这个区间，并对偏离发出预警。代理行与嵌套账户的资金流同样受益，因为风险存在于中介机构的网络位置，而非任何单笔交易之中。</p>
<p>需要诚实说明的是：在规则强大的地方，模型反而更弱。制裁名单命中是确定性的，模型不应出现在这条路径上。监管要求的阈值是政策而非预测，无论模型是否认为该笔交易良性，它都应当触发。可行的架构是：在合规要求之处保留确定性控制，再在其上叠加行为侦测——目的不是取代规则，而是发现那些从来没有被写进规则的东西。</p>
<h2 id="如何衡量反洗钱模型的真实效果">应当如何衡量反洗钱模型的真实效果？</h2>
<p>反洗钱领域的模型效果极容易被错误衡量，而最常见的错误是优化了错误的指标。当已确认案件在告警中占比不足千分之一时，准确率几乎没有意义：一个什么都不报的模型准确率高达99.9%，却毫无价值。真正重要的指标分为侦测有效性与运营效率两类，部署效果必须同时用这两类来评判。</p>
<p>在侦测方面，有用的度量是"队列顶部精确率"——排名最高的一百条告警中，最终被确认的有多少——以及针对留出标注集的召回率，即历史已确认案件中有多大比例会被模型找出来。两者之中，队列顶部精确率更具可操作性，因为它直接对应调查员的实际工作方式。侦测时延也值得单列一项：模型相对于该手法第一笔交易多快发现案件，因为资金已经转走之后才识别出的案件，基本只能核销。</p>
<p>在效率方面，度量项是相对现有规则引擎的误报下降幅度、每关闭一个案件所耗的调查工时，以及可疑交易报告转化率——即被调查的告警最终形成正式报告的比例。这三个数字合起来才能讲出诚实的故事：一个把告警量减半、同时把转化率也减半的模型，无论表面数字多漂亮，都没有真正改善项目。正确的框架是盯住一个比值——每确认一个案件所耗的调查工时——从部署前的基线开始按月追踪，同时并列报告告警量与侦测覆盖率，使效率与覆盖率都不被悄悄牺牲掉。</p>
<p>有两项实践能让这些数字变得可信。其一，保留一份模型从未训练过的留出评估集并定期更新，让效果主张是被测量出来的，而不是被宣称出来的。其二，既监控打分稳定性，也监控输入稳定性，因为输入分布的变化——新增的支付通道、客户结构的变化——会在告警指标发生变动之前数月就开始侵蚀模型。</p>
<h2 id="反洗钱模型中最关键的特征">反洗钱模型中最关键的特征有哪些？</h2>
<p>侦测效果的大部分收益来自特征工程，而非算法选择。有信号价值的特征分为四类。速度与偏离类特征把实体近期的行为与它自身的历史做比较：交易笔数与金额相对滚动基线的变化、渠道或交易对手构成的变化、以及资金流入与流出的比值。网络类特征刻画的是位置而非行为——不同交易对手的数量、账户在资金流图中的中心度、过账而不沉淀的价值占比、以及到任何已知高风险实体的图距离。</p>
<p>同侪群体类特征把实体与相似实体比较，而不是与它自己或某个固定阈值比较：把这个账户与同细分、同账龄、同申报用途的其他账户放在一起看。这一类最有价值，也最常缺失，因为它需要做客群分层，而碎片化的数据让这件事变得困难——然而正是这类特征才能抓住那些绝对数值上平平无奇、只有在情境中才可疑的异常。静态风险特征——地域、行业、产品、客户尽职调查评级、负面舆情——则提供先验，再由行为特征去修正。</p>
<p>两点提醒。如果特征来自那些在不同源系统中含义不一致的字段，这些不一致会直接渗漏进模型，因此每个特征都需要有书面定义，并能沿血缘追溯到源字段。此外，任何编码了受保护特征——或其紧密代理变量——的特征，都会带来公平放贷与歧视方面的风险敞口，再高的侦测效果也无法为此辩护；这类特征应当被有意排除，并把排除决定记录在案，而不是等到检查时才被发现。</p>
<h2 id="模型风险管理对反洗钱部署的要求">监管视角下的模型风险管理要求什么？</h2>
<p>监管方问的不是模型有没有效，而是机构能否证明自己知道它有多有效。这一区别就是模型风险管理的全部，并具体化为检查时必看的四类材料。第一类是书面验证：由未参与开发的人员，对模型的开发过程、数据血缘、方法论与表现做独立评审，并把发现的问题追踪到整改。第二类是案件级可解释性——每条告警都应附上驱动其评分的特征与关系，且呈现方式要让调查员看得懂、让监管方审得动。</p>
<p>第三类是带有预设阈值的持续监控。准确率、告警量与输入稳定性都应对照预期区间追踪，并在阈值被突破时触发既定动作：排查、重新校准、重训，或暂停并回退到规则。没有决策树的监控方案只是文档，不是控制。第四类是变更管理：对模型、训练数据与特征定义做版本管理，并记录每一次晋升到生产环境的决定及其支撑证据。</p>
<p>除这四类材料之外，有两项实践一贯地区分出"令监管满意"与"挣扎应对"的两类项目。其一是冠军—挑战者机制，即让一种替代方案并行运行并定期做基准比较，以此证明现有模型是基于证据而非惯性被选中的。其二是把调查员的反馈当作受治理的标注训练数据来经营——否决记录连同理由一起被保存，按计划回流到重训中，并度量由此带来的效果变化。正是这个闭环把模型从静态产物变成一个持续改进的项目，也是机构能够给出的、证明其部署处于受控状态的最有力证据。</p>
"""

# ---- FAQ answer rewrites (EN) ----
EN_FAQ = [
    ("AI in Anti-Money Laundering Detection is How machine learning improves AML detection while cutting false positives.",
     "It is the use of machine learning models — typically trained on labelled historical cases and on the graph of relationships between accounts, customers, and counterparties — to score transactions and entities for laundering risk. Unlike a rules engine that fires on fixed thresholds, a model learns behavioural and network patterns, which lets it rank existing alerts by likelihood of genuine suspicion and surface typologies such as structuring and mule networks that thresholds miss."),
    ("It reduces friction in how Financial Services teams access, interpret, and act on information, leading to measurable productivity gains.",
     "Because rules-based monitoring generates an overwhelming volume of low-value alerts — studies consistently put false positives above 90% of AML alerts — while genuine risk hides in patterns no single threshold was written to catch. Machine learning concentrates investigator attention on the cases most likely to be real, which is the only sustainable way to raise detection coverage without proportionally raising headcount."),
    ("Start with one high-value decision, connect the minimum data needed, and iterate with business users until the output is trusted.",
     "Start with alert triage rather than full automation: rank the alerts your existing rules engine already produces by likelihood of genuine suspicion, and let investigators work the top of the queue first. Run the model in shadow mode against historical cases before it influences any decision, keep every alert explainable, and feed investigator overrides back into retraining. A meaningful triage pilot typically takes three to six months."),
]

CN_FAQ = [
    ("AI在反洗钱检测中的应用是机器学习如何改进反洗钱检测并减少误报。。",
     "它指的是用机器学习模型——通常基于历史已确认案件的标注数据，以及账户、客户与交易对手之间的关系图谱训练而成——对交易与实体进行洗钱风险打分。与按固定阈值触发的规则引擎不同，模型学习的是行为模式与网络结构，因此既能对既有告警按真实可疑的可能性排序，也能发现拆分交易、马仔账户网络这类阈值无法覆盖的手法。"),
    ("它能减少金融服务团队获取、理解和运用信息时的摩擦，从而带来可衡量的效率提升。",
     "因为基于规则的监测系统会产生大量低价值告警——多项研究一致显示反洗钱告警中的误报比例超过90%——而真实风险往往藏在没有任何单一阈值被写到的模式里。机器学习把调查人员的注意力集中到最可能成立的案件上，这是在不大比例增加人力的前提下提升侦测覆盖率的唯一可持续路径。"),
    ("从一个高价值决策入手，连接所需的最少数据，并与业务用户迭代，直到输出获得信任。",
     "建议从告警分诊入手，而非一步到位做全自动化：先让模型对现有规则引擎已产生的告警按真实可疑的可能性排序，让调查员优先处理队列顶部。在影响任何决策之前，先用历史案件做影子测试；保证每条告警都可解释；并把调查员的否决理由回流进下一轮训练。一个有意义的告警分诊试点通常需要三到六个月。"),
]

EN_H2 = [
    ("why-it-matters", "Why it matters", "Why Does AI Matter for AML Detection Now?"),
    ("common-challenges", "Common challenges", "What Are the Most Common Obstacles to AI in AML?"),
    ("how-to-get-started", "How to get started", "How Should Institutions Get Started With AI-Based AML Detection?"),
    ("frequently-asked-questions", "Frequently asked questions", "What Do Practitioners Ask Most Often About AI in AML?"),
    ("key-takeaways", "Key takeaways", "What Are the Key Takeaways for AML Leaders?"),
]
CN_H2 = [
    ("为什么重要", "为什么重要", "为什么AI对反洗钱侦测如此重要？"),
    ("常见挑战", "常见挑战", "反洗钱AI落地最常见的障碍是什么？"),
    ("如何开始", "如何开始", "机构应如何着手引入AI反洗钱侦测？"),
    ("核心要点", "核心要点", "反洗钱负责人应记住哪些要点？"),
    ("常见问题", "常见问题", "从业者最常问的问题有哪些？"),
]
TW_H2 = [
    ("爲什麼重要", "爲什麼重要", "爲什麼AI對反洗錢偵測如此重要？"),
    ("常見挑戰", "常見挑戰", "反洗錢AI落地最常見的障礙是什麼？"),
    ("如何開始", "如何開始", "機構應如何着手引入AI反洗錢偵測？"),
    ("核心要點", "核心要點", "反洗錢負責人應記住哪些要點？"),
    ("常見問題", "常見問題", "從業者最常問的問題有哪些？"),
]

if __name__ == "__main__":
    en = path_of(SLUG, "en")
    h = open(en, encoding="utf-8").read()
    anchor = '            <section class="faq-section"'
    assert h.count(anchor) == 1
    h = h.replace(anchor, "\n" + EN_NEWS + "\n" + anchor)
    for old, new in EN_FAQ:
        assert h.count(old) >= 1, old[:60]
        h = h.replace(old, new)
    open(en, "w", encoding="utf-8").write(h)
    print("EN body + FAQ done")

    cn = path_of(SLUG, "cn")
    h = open(cn, encoding="utf-8").read()
    assert h.count(anchor) == 1
    h = h.replace(anchor, "\n" + ZH_NEWS + "\n" + anchor)
    for old, new in CN_FAQ:
        assert h.count(old) >= 1, old[:60]
        h = h.replace(old, new)
    open(cn, "w", encoding="utf-8").write(h)
    print("CN body + FAQ done")

    tw = path_of(SLUG, "tw")
    h = open(tw, encoding="utf-8").read()
    assert h.count(anchor) == 1
    h = h.replace(anchor, "\n" + s2t_fixed(ZH_NEWS) + "\n" + anchor)
    for old, new in CN_FAQ:
        o, n = s2t_fixed(old), s2t_fixed(new)
        assert h.count(o) >= 1, o[:60]
        h = h.replace(o, n)
    open(tw, "w", encoding="utf-8").write(h)
    print("TW body + FAQ done")

    for hid, old, new in EN_H2:
        retitle_h2(en, hid, old, new)
    for hid, old, new in CN_H2:
        retitle_h2(path_of(SLUG, "cn"), hid, old, new)
    for hid, old, new in TW_H2:
        retitle_h2(path_of(SLUG, "tw"), hid, old, new)
    print("H2s converted")
