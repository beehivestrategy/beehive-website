#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""slug 14: alert-driven-analytics-proactive-insights-before-you-ask-a-2026-update
EN 1331 -> ~2600 ; CN/TW 1797 -> ~3600 ; build FAQ ; H2 -> questions."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gb001b_lib import path_of, retitle_by_text, build_faq, s2t_fixed

SLUG = "alert-driven-analytics-proactive-insights-before-you-ask-a-2026-update"
NAV = '            <nav class="article-nav" aria-label="Article navigation">'

EN_NEWS = """<h2 id="how-do-you-design-thresholds-that-work">How Do You Design Thresholds That Actually Work?</h2>
<p>Static thresholds are the default because they are easy to explain, and they are the most common cause of alert fatigue because they cannot distinguish a seasonal dip from a structural break. The alternative is not to abandon thresholds but to make them relative. A threshold expressed as a deviation from the expected value for this day of the week, in this season, for this product family, absorbs most of the variation that makes static rules noisy. The model supplies the expectation; the business supplies the tolerance; and the alert fires only when the gap between them exceeds what the owner is willing to accept.</p>
<p>Three refinements improve on that baseline. Use a tolerance band rather than a point threshold, and require the condition to persist for a minimum duration before firing — a single hour of anomalous traffic is noise, three consecutive hours outside the band is a signal. Combine magnitude with rate of change, because a slow drift and a sudden break have different causes and different owners even when the absolute deviation is the same. And express thresholds in business units wherever possible: a stock-out risk measured in days of cover is more actionable than the same risk expressed as a percentage deviation from forecast.</p>
<p>The tuning process matters as much as the design, and it should be empirical rather than deliberative. Take three months of history, run the candidate rule against it, and count how often it would have fired and how often firing would have been useful. A rule that would have fired forty times for three genuinely useful warnings will produce fatigue; adjust the threshold until the ratio is defensible. This backtest turns threshold design from an argument about numbers into a decision about the cost of a missed detection versus the cost of a false alarm — which is a business judgement the owner is qualified to make.</p>
<h2 id="how-should-alerts-be-routed-and-escalated">How Should Alerts Be Routed and Escalated?</h2>
<p>Routing is where most alert programmes lose their value, because the alert reaches someone who cannot act. The design principle is that routing follows the decision, not the data: an alert about margin compression on a product family goes to whoever owns pricing for that family, not to the analytics team that built the model and not to a distribution list. Every rule needs a primary owner with the authority to act, a backup for absence, and a defined escalation path if the condition persists.</p>
<p>Escalation should be tied to persistence and severity rather than to time alone. A condition that persists beyond a defined window, or that crosses a higher severity band, escalates to the next level with the history attached — what fired, when, what was done, and what changed. Attaching that history is what makes escalation useful rather than merely louder: the recipient at the second level should not have to reconstruct the story. Severity bands themselves should be few — three is usually enough — because a five-level scale is one nobody can calibrate consistently across teams.</p>
<p>Two failure modes recur. The first is the broadcast alert, sent to a wide group on the theory that someone will respond; in practice everyone assumes someone else has it, and nobody does. The second is the orphan alert, whose owner has changed roles; these accumulate silently and are the main reason alert catalogues decay. A monthly review that reassigns or retires orphan rules is unglamorous maintenance, and it is the single most effective thing an alert programme owner can do.</p>
<h2 id="what-does-the-programme-cost-to-run">What Does an Alert Programme Cost to Run?</h2>
<p>The costs are steadier and less visible than the build cost, and they are the reason alert programmes degrade. There are three. Rule maintenance is the first: every rule needs periodic revalidation as the business changes, and a catalogue of sixty rules consumes real analyst time each quarter — typically a few days per review cycle, which is affordable and must be budgeted rather than absorbed.</p>
<p>Second is the response cost, which is the one most business cases omit. If an alert programme generates two hundred alerts a month and each consumes fifteen minutes of someone's attention, that is fifty hours a month of skilled time spent on triage — a real operating cost that must be justified by the value of what gets caught. This is precisely why precision matters more than recall in alert design: a programme that catches everything and is acted on selectively is more expensive than one that catches less and is trusted completely.</p>
<p>Third is the platform cost: monitoring infrastructure, model retraining, and the integration with delivery channels. These are usually modest relative to the first two, and they are the easiest to forecast. The honest business case adds all three and compares them against the cost of late detection — the margin lost, the stock-out incurred, the compliance deadline missed. Programmes framed this way survive budget review; programmes framed as a technology upgrade tend not to.</p>
<h2 id="how-do-you-avoid-fatigue-over-time">How Do You Avoid Alert Fatigue Over Time?</h2>
<p>Fatigue is not a launch problem; it is a decay problem. Most alert programmes start well, with a small catalogue, engaged owners, and high action rates, and then degrade as rules are added for every new request and none are ever removed. The mechanism of decay is predictable: the action rate falls, users begin to skim rather than read, and eventually the channel is muted — at which point even a well-designed alert is worthless, because the delivery path itself has been trained out of the user's attention.</p>
<p>The countermeasure is a monthly catalogue review with three standing agenda items. Which rules fired but produced no action — these are candidates for redesign or retirement. Which conditions occurred that no rule caught — these are candidates for new rules, and this is the only legitimate way the catalogue should grow. And which alerts were acted on but turned out to be false alarms — these indicate threshold drift. Keeping the review short and recurring matters more than its rigour; a fifteen-minute monthly review that actually happens outperforms a quarterly deep-dive that gets cancelled.</p>
<p>Two metrics track fatigue directly and should be published to the alert owners: the action rate, meaning the share of alerts that led to a documented response, and the mute rate, meaning the share of recipients who have silenced the channel. The second is the honest leading indicator, because users mute a channel before they stop trusting it, and recovering a muted channel is far harder than fixing a noisy rule.</p>
"""

ZH_NEWS = """<h2 id="如何设计出真正奏效的阈值">如何设计出真正奏效的阈值？</h2>
<p>静态阈值之所以成为默认选项，是因为它容易解释；而它之所以成为告警疲劳最常见的成因，是因为它无法区分季节性回落与结构性断裂。替代方案不是放弃阈值，而是让阈值变成相对的：一个表示为"相对于该星期几、该季节、该产品族预期值的偏离"的阈值，会吸收掉让静态规则变得嘈杂的大部分变异。模型提供预期值，业务方提供容差，只有当两者之间的差距超出负责人愿意接受的范围时，告警才触发。</p>
<p>三项改进能在此基础上进一步提升效果。使用容差带而非点阈值，并要求条件持续一段最短时间才触发——一小时的流量异常是噪声，连续三小时落在带外才是信号。把幅度与变化率结合使用，因为缓慢漂移与突然断裂的成因不同、负责人也不同，即便绝对偏离量相同。并且在可能的情况下用业务单位来表达阈值：以"可供天数"衡量的缺货风险，比以"相对预测的偏离百分比"表达的同一风险更具可操作性。</p>
<p>调优过程与设计同等重要，而且它应当是经验性的，而不是靠开会讨论。取三个月的历史数据，让候选规则在上面跑一遍，统计它会触发多少次、其中有多少次触发是有用的。一条会触发四十次、却只带来三次真正有用预警的规则，必然造成疲劳；调整阈值，直到这个比例站得住脚。这种回测把阈值设计从一场关于数字的争论，变成一次关于"漏检代价"与"误报代价"之间权衡的决策——而这恰恰是负责人有资格做出的业务判断。</p>
<h2 id="告警应如何路由与升级">告警应当如何路由与升级？</h2>
<p>路由是多数告警项目失去价值的地方，因为告警到达了无法采取行动的人手上。设计原则是：路由跟着决策走，而不是跟着数据走。某产品族毛利率承压的告警，应当发给负责该产品族定价的人，而不是发给构建模型的分析团队，也不该发到一个群发列表。每条规则都需要一个有权采取行动的主负责人、一位缺席时的备份负责人，以及一条在状况持续时的既定升级路径。</p>
<p>升级应当与持续时长和严重度挂钩，而不只是与时间挂钩。当某个状况超出既定时间窗仍在持续，或跨入更高的严重度区间时，就带着完整历史升级到下一层级——触发了什么、何时触发、做过什么、有何变化。附上这段历史才让升级变得有用，而不只是变得更吵：第二级的接收者不该再去重构整个故事。严重度区间本身应当少而精——三个通常就够——因为五个等级的标尺，是没有团队能跨团队一致校准的。</p>
<p>有两种失败模式反复出现。其一是广播式告警，发到一个大群体，理论上"总会有人响应"；实践中每个人都以为别人已经在处理，结果谁都没动。其二是孤儿告警，其负责人已经调岗；这类规则会静默累积，也是告警目录衰败的主因。每月一次的评审重新分配或停用孤儿规则，是一项不起眼的维护工作，却是告警项目负责人能做的、最有效的一件事。</p>
<h2 id="告警项目的运行成本是多少">告警项目的运行成本是多少？</h2>
<p>运行成本比建设成本更稳定、也更不显眼，而这正是告警项目退化的原因。成本共有三项。其一是规则维护：随着业务变化，每条规则都需要定期重新验证；一个六十条规则的目录，每个评审周期会消耗可观的分析师时间——通常每次评审几天，这笔开销是可承受的，但必须被列入预算，而不是被悄悄吸收掉。</p>
<p>其二是响应成本，这也是多数商业论证会漏掉的一项。如果一个告警项目每月产生两百条告警，每条消耗某人十五分钟注意力，那么每月就有五十小时的熟练工时花在分诊上——这是一项真实的运营成本，必须用所捕获问题的价值来证明其合理性。这正是告警设计中"精确率比召回率更重要"的原因：一个什么都抓得住、却只被选择性响应的项目，比一个抓得更少、却被完全信任的项目更昂贵。</p>
<p>其三是平台成本：监控基础设施、模型重训、以及与交付渠道的集成。这部分通常相对前两项较小，也最容易预测。诚实的商业论证会把三项都加起来，再与"延迟发现的代价"做比较——损失的毛利、发生的缺货、错过的合规截止日。以这种方式构建论证的项目能通过预算评审；被包装成技术升级的项目往往过不了。</p>
<h2 id="如何长期避免告警疲劳">如何长期避免告警疲劳？</h2>
<p>疲劳不是上线时的问题，而是衰败问题。多数告警项目开局良好——目录小、负责人投入、行动率高——随后随着每个新需求都加规则、却从不移除任何规则而退化。衰败的机制是可预测的：行动率下降，用户从阅读转为扫视，最终频道被静音；到那时，再精心设计的告警也毫无价值，因为交付路径本身已经被用户训练出了忽略。</p>
<p>对策是每月一次的目录评审，议程固定三项。哪些规则触发了却没有产生行动——这些是重新设计或停用的候选。哪些发生了状况却没有规则捕捉到——这些是新增规则的候选，而且这是目录唯一正当的增长方式。以及哪些告警被响应了、事后却被证明是误报——这些说明阈值已经漂移。保持评审简短且持续，比追求严谨更重要：一次真正发生的十五分钟月度评审，胜过一场被取消的季度深度复盘。</p>
<p>有两项指标能直接度量疲劳，应当向告警负责人公开：其一是行动率，即带来有记录响应的告警占比；其二是静音率，即已将该频道设为免打扰的接收者占比。第二项才是诚实的先行指标，因为用户在停止信任之前会先静音频道，而挽回一个被静音的频道，远比修好一条嘈杂的规则困难得多。</p>
"""

EN_FAQ = [
    ("What is alert-driven analytics?",
     "It is an approach in which the analytics system continuously monitors governed data, detects anomalies and threshold breaches, and proactively pushes ranked, explainable alerts to the people who can act — through the messaging tools they already use — rather than waiting for someone to open a dashboard and ask."),
    ("How many alerts should a team receive?",
     "Far fewer than most catalogues produce. The useful measure is not volume but action rate: the share of alerts that lead to a documented response. Programmes in good health act on a clear majority of what they send; programmes generating dozens of alerts a day with low action rates are training users to ignore the channel."),
    ("Why do static thresholds cause alert fatigue?",
     "Because they cannot distinguish a seasonal dip from a structural break. A five percent drop may be normal in one month and serious in another, so a static rule either fires constantly or misses the event. Thresholds expressed as a deviation from the expected value for that day, season, and product family absorb the routine variation and fire only on the meaningful gap."),
    ("Who should own an alert-driven analytics programme?",
     "A named owner with a mandate to prune. Alert catalogues decay by accretion: rules are added for every request and rarely removed. The owner runs a monthly review of firing rules, action rates, and orphaned rules, and has the authority to retire anything that has not changed behaviour in three months."),
    ("How do you measure whether an alert programme is working?",
     "Track the action rate, the time from anomaly to action, and the downstream business impact of early intervention — margin protected, stock-outs avoided, deadlines met. Alongside them, watch the mute rate, because users silence a channel before they stop trusting it, and a muted channel is the clearest sign the programme has become noise."),
]

CN_FAQ = [
    ("什么是预警驱动分析？",
     "它指的是这样一种方式：分析系统持续监控受治理的数据，检测异常与阈值突破，并主动把经过排序、可解释的预警推送给能够采取行动的人——通过他们已经在用的即时通讯工具——而不是等待某人打开仪表板去提问。"),
    ("一个团队应当收到多少条预警？",
     "远少于多数目录所产生的数量。有意义的度量不是数量，而是行动率：带来有记录响应的预警占比。健康的项目对其发出的大部分预警都会采取行动；每天产生几十条、行动率却很低的项目，正在训练用户忽略这个频道。"),
    ("为什么静态阈值会导致告警疲劳？",
     "因为它无法区分季节性回落与结构性断裂。百分之五的下滑在某个月可能正常，在另一个月可能严重，于是静态规则要么频繁触发，要么漏掉事件。把阈值表示为相对于该日期、季节与产品族预期值的偏离，就能吸收掉常规波动，只在出现有意义的差距时触发。"),
    ("预警驱动分析项目应当由谁负责？",
     "应当由一位有修剪权限的具名负责人负责。告警目录是靠堆积而衰败的：每个需求都加规则，却极少移除。负责人每月评审触发情况、行动率与孤儿规则，并有权停用任何三个月内没有改变过行为的规则。"),
    ("如何衡量预警项目是否奏效？",
     "跟踪行动率、从异常发生到采取行动的时间，以及早期干预带来的下游业务影响——保住的毛利、避免的缺货、赶上的截止期限。同时关注静音率，因为用户会在停止信任之前先静音频道，而一个被静音的频道，是项目已经沦为噪声的最清晰信号。"),
]

EN_H2 = [
    ("The Current Landscape", "What Is the Current Landscape for Alert-Driven Analytics?"),
    ("Key Implementation Challenges", "What Are the Key Implementation Challenges?"),
    ("Practical Approaches That Work", "Which Practical Approaches Actually Work?"),
    ("Key Takeaways", "What Are the Key Takeaways?"),
    ("Conclusion", "Where Should You Start?"),
]
CN_H2 = [
    ("理解当前格局", "当前的企业分析格局是怎样的？"),
    ("关键原则与战略框架", "预警驱动分析的关键原则与战略框架是什么？"),
    ("实施方法与最佳实践", "实施预警驱动分析的最佳实践有哪些？"),
    ("衡量成功与展示投资回报率", "应当如何衡量成功并证明投资回报？"),
    ("常见陷阱及规避方法", "有哪些常见陷阱、又该如何规避？"),
    ("关键要点", "核心要点是什么？"),
    ("结论", "应当从哪里开始？"),
]
TW_H2 = [
    ("理解當前格局", "當前的企業分析格局是怎樣的？"),
    ("關鍵原則與策略框架", "預警驅動分析的關鍵原則與策略框架是什麼？"),
    ("實施方法與最佳實踐", "實施預警驅動分析的最佳實踐有哪些？"),
    ("衡量成功與展示投資回報率", "應當如何衡量成功並證明投資回報？"),
    ("常見陷阱及規避方法", "有哪些常見陷阱、又該如何規避？"),
    ("關鍵要點", "核心要點是什麼？"),
    ("結論", "應當從哪裏開始？"),
]

if __name__ == "__main__":
    en = path_of(SLUG, "en")
    h = open(en, encoding="utf-8").read()
    assert h.count(NAV) == 1
    h = h.replace(NAV, "\n" + EN_NEWS + "\n" + build_faq(EN_FAQ, "en") + "\n" + NAV)
    open(en, "w", encoding="utf-8").write(h)
    print("EN body + FAQ done")

    cn = path_of(SLUG, "cn")
    h = open(cn, encoding="utf-8").read()
    assert h.count(NAV) == 1
    h = h.replace(NAV, "\n" + ZH_NEWS + "\n" + build_faq(CN_FAQ, "cn") + "\n" + NAV)
    open(cn, "w", encoding="utf-8").write(h)
    print("CN body + FAQ done")

    tw = path_of(SLUG, "tw")
    h = open(tw, encoding="utf-8").read()
    assert h.count(NAV) == 1
    tw_faq = [(s2t_fixed(q), s2t_fixed(a)) for q, a in CN_FAQ]
    h = h.replace(NAV, "\n" + s2t_fixed(ZH_NEWS) + "\n" + build_faq(tw_faq, "tw") + "\n" + NAV)
    open(tw, "w", encoding="utf-8").write(h)
    print("TW body + FAQ done")

    for old, new in EN_H2:
        retitle_by_text(en, old, new)
    for old, new in CN_H2:
        retitle_by_text(path_of(SLUG, "cn"), old, new)
    for old, new in TW_H2:
        retitle_by_text(path_of(SLUG, "tw"), old, new)
    print("H2s converted in en/cn/tw")
