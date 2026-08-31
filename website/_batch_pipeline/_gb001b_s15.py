#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""slug 15: manufacturing-predictive-maintenance-ai
EN 1431 -> ~2600 ; CN/TW 2256 -> ~3600 ; H2 -> questions."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gb001b_lib import path_of, retitle_by_text, s2t_fixed

SLUG = "manufacturing-predictive-maintenance-ai"
ANCHOR = '            <section class="faq-section"'

EN_NEWS = """<h2 id="which-assets-should-you-start-with">Which Assets Should You Start With?</h2>
<p>Asset selection determines whether a pilot produces a result or a research project, and the ranking is an economic calculation rather than a data-quality one. Score each candidate asset class on three axes: the cost of an unplanned failure, the frequency of failure, and the lead time required to act on a warning. The product of the first two gives the annual cost of the problem; the third determines whether a prediction can actually change the outcome.</p>
<p>The trap is choosing the asset with the richest data rather than the asset with the most expensive failure. A well-instrumented turbine that fails rarely and cheaply will produce a beautiful model and a negligible return, while a poorly instrumented pump that fails monthly and stops a line will produce a harder model and a much larger one. When data quality is the constraint, the honest answer is often to add a sensor — vibration or current monitoring on a critical asset is inexpensive relative to the downtime it protects.</p>
<p>A second filter matters just as much: choose an asset where a warning changes the maintenance decision. If the only possible response to a prediction is "run it to failure anyway," because the spare part has a twelve-week lead time or the line cannot be stopped, then prediction creates anxiety rather than value. The best first assets are those with a genuine decision attached — defer, service at the next planned window, or intervene now — because that decision is what turns a probability into saved money.</p>
<h2 id="what-does-remaining-useful-life-mean">What Does Remaining Useful Life Mean in Practice?</h2>
<p>Remaining useful life is the prediction most plants ask for and the one most often misunderstood. An RUL model does not say when a component will fail; it estimates, with an interval, how much useful operating life remains given its current condition and duty cycle. That interval matters more than the point estimate, because the decision — service at the next window or intervene now — depends on where the interval sits relative to the next planned stop, not on a single number.</p>
<p>Two modelling approaches dominate, and the choice depends on the labels you have. If you have run-to-failure histories with known failure times, supervised regression can estimate life directly, and it produces the tightest intervals. If you do not — which is the common case, because components are replaced before they fail — anomaly detection and degradation-trend extrapolation are the practical alternative: establish what normal looks like for that asset under each operating mode, and measure how far and how fast the current trajectory departs from it. Less precise, but it works without failure labels and it is often good enough for the decision.</p>
<p>The operational caveat is that duty cycle changes everything. A pump running at eighty percent of rated load and the same pump at forty percent have different degradation trajectories, and a model that ignores operating mode will produce confident nonsense when the production mix changes. Conditioning the model on operating mode, and retraining when the plant's product mix shifts materially, is what keeps RUL estimates usable across a year rather than a quarter.</p>
<h2 id="how-do-you-close-the-loop">How Do You Close the Loop With Work Orders?</h2>
<p>A prediction that does not become a work order is a forecast nobody acted on, and closing that loop is where most programmes stall. The integration is conceptually simple: the model emits a ranked prediction, the CMMS receives it as a candidate work order with the evidence attached, and the planner accepts, defers, or rejects with a reason. Each outcome feeds back as a label — accepted and confirmed, accepted and found healthy, rejected — and those labels are what let the model improve.</p>
<p>Three details determine whether the loop actually turns. The prediction must arrive with its evidence — which sensors moved, over what window, and how far from normal — because a planner will not schedule work on an unexplained score, and rightly so. The work order must be pre-populated with the asset, the suspected failure mode, and the suggested action, so that accepting costs a planner seconds rather than minutes. And rejection must be easy and structured, with a small set of reasons, because a planner who has to write a paragraph will simply ignore the prediction instead.</p>
<p>The governance question is worth settling early: who is accountable if the model misses a failure? The answer that works is that the model is advisory and the planner remains accountable for the maintenance decision, exactly as with any other diagnostic input. Programmes that try to make the model authoritative lose planner trust immediately; programmes that position it as a second opinion, and then demonstrate that the second opinion is usually right, earn adoption without a mandate.</p>
<h2 id="how-do-you-avoid-alert-fatigue-on-the-floor">How Do You Avoid Alert Fatigue on the Plant Floor?</h2>
<p>Operators and planners tolerate false alarms far less than analysts expect, because every false alarm costs real work — a machine opened, a part pulled, a window spent. Precision therefore matters more than recall, and the target should be set explicitly: most successful programmes hold precision above roughly fifty percent on the alerts they escalate, and tune upwards from there. A model that catches nine of ten failures with twenty false alarms will be switched off; one that catches six of ten with two false alarms will be used.</p>
<p>Four practices protect precision. Escalate only predictions whose interval is tight enough to support a decision, and hold the rest as watch-list items rather than alerts. Require persistence — a degradation signal that holds for a defined window rather than a single anomalous reading. Suppress duplicates across sensors on the same asset, since correlated sensors will each report the same event. And review every false alarm monthly, which is the only mechanism that steadily improves precision rather than merely accepting it.</p>
<p>The measure to publish is the alert-to-work-order conversion rate: the share of escalated predictions that became accepted work with a confirmed finding. It is the single number that tells you whether the programme is trusted, and it moves before the downtime metrics do — which makes it the earliest signal available that a predictive maintenance programme is working, or quietly being ignored.</p>
"""

ZH_NEWS = """<h2 id="应当从哪些资产开始">应当从哪些资产开始？</h2>
<p>资产选择决定了试点是产出结果，还是变成一个研究项目；而排序的依据是经济计算，不是数据质量。对每个候选资产类别按三个维度打分：非计划故障的代价、故障发生的频率、以及依据预警采取行动所需的提前期。前两项的乘积给出问题的年度成本，第三项则决定预测是否真能改变结果。</p>
<p>常见的陷阱是选择了数据最丰富的资产，而不是故障代价最高的资产。一台仪表齐全但很少故障、且故障代价很低的涡轮机，会产出一个漂亮的模型和可以忽略不计的回报；而一台仪表不足、却每月故障并导致停线的泵，模型更难做，回报却大得多。当数据质量成为约束时，诚实的答案往往是加装一只传感器——在关键资产上加装振动或电流监测，相对于它所保护的停机损失而言，成本是很低的。</p>
<p>第二个筛选条件同样重要：选择那些"收到预警会改变维护决策"的资产。如果对预测的唯一可能反应是"反正只能用到坏"，因为备件交期长达十二周、或者产线根本停不下来，那么预测制造的是焦虑，而不是价值。最合适的首批资产，是那些确实挂着一个真实决策的资产——延后、在下个计划窗口检修、还是立即介入——因为正是这个决策，把概率转化成了省下来的钱。</p>
<h2 id="剩余使用寿命在实践中意味着什么">剩余使用寿命在实践中意味着什么？</h2>
<p>剩余使用寿命是多数工厂会提出的要求，也是最容易被误解的一项预测。剩余寿命模型并不说明某个部件何时会坏；它估计的是——以区间的形式——在当前状态与负载工况下，还剩下多少可用运行寿命。这个区间比点估计更重要，因为"在下个窗口检修"还是"立即介入"的决策，取决于区间相对于下一次计划停机的位置，而不取决于一个单一数字。</p>
<p>有两种建模路线占主导，选择取决于你手上有什么标签。如果你拥有带已知失效时间的"运行至失效"历史，监督式回归可以直接估计寿命，并且能给出最窄的区间。如果你没有——这是常见情况，因为部件往往在失效前就被更换了——那么异常检测与退化趋势外推是更实用的替代方案：先确定该资产在每种运行模式下的正常状态，再衡量当前轨迹偏离了多远、偏离得多快。精度低一些，但在没有失效标签的条件下可用，而且通常足以支撑决策。</p>
<p>运维层面有一个前提值得注意：负载工况会改变一切。一台以额定负载八成运行的泵，与同一台以四成运行的泵，退化轨迹是不同的；一个忽略运行模式的模型，会在产品结构变化时给出自信的胡说。把模型以运行模式为条件来建模，并在工厂产品结构发生实质变化时重训，才是让剩余寿命估计在一年内、而不是一个季度内保持可用的关键。</p>
<h2 id="如何与工单系统形成闭环">如何与工单系统形成闭环？</h2>
<p>一个没有变成工单的预测，就是一条没人行动的预测；而正是这个闭环，卡住了多数项目。集成在概念上很简单：模型输出经过排序的预测，计算机化维护管理系统把它作为一条附带证据的候选工单接收，计划员选择接受、延后或拒绝并说明理由。每一种结果都作为标签回流——接受且确认、接受但检查正常、拒绝——而这些标签正是模型得以改进的原因。</p>
<p>三个细节决定了这个闭环是否真的转得起来。预测必须连同证据一起到达——哪些传感器发生变化、在什么时间窗口内、偏离正常有多远——因为计划员不会为一个无法解释的评分安排工作，而且这是对的。工单必须预填资产、疑似失效模式与建议动作，使接受一个预测只花计划员几秒钟，而不是几分钟。拒绝必须简单且结构化，只提供少量理由选项，因为需要写一段话才能拒绝的计划员，会干脆忽略预测。</p>
<p>治理问题值得尽早明确：如果模型漏掉了一次故障，谁负责？行得通的答案是：模型是建议性的，计划员仍然对维护决策负责，正如对待任何其他诊断输入一样。试图让模型具有权威性的项目，会立刻失去计划员的信任；把它定位为"第二意见"、然后用事实反复证明这个第二意见通常是对的，才能在没有强制命令的情况下赢得采用。</p>
<h2 id="如何避免车间里的告警疲劳">如何避免车间层面的告警疲劳？</h2>
<p>操作员与计划员对误报的容忍度远低于分析人员的预期，因为每一次误报都带来真实的工作量——拆一台机器、领一个备件、占用一个窗口。因此精确率比召回率更重要，而且目标应当被明确设定：多数成功的项目会把所升级告警的精确率维持在五成以上，并在此基础上继续调优。一个能抓住十次故障中的九次、却带来二十次误报的模型会被关掉；一个能抓住十次中的六次、只带来两次误报的模型会被用起来。</p>
<p>四项实践能保护精确率。只升级那些区间足够紧、足以支撑决策的预测，其余的作为观察项而不是告警。要求持续性——一个持续了既定时间窗的退化信号，而不是一次异常读数。抑制同一资产上传感器之间的重复告警，因为相关传感器会各自报告同一次事件。并且每月复盘每一次误报，这是唯一能让精确率稳步提升、而不是被被动接受的机制。</p>
<p>值得公开的度量是"告警转工单转化率"：被升级的预测中，最终形成已确认发现的工单的占比。这是能说明项目是否被信任的单一数字，而且它比停机指标更早发生变动——这使它成为判断一个预测性维护项目正在奏效、还是正被悄悄忽略的最早信号。</p>
"""

EN_H2 = [
    ("Why it matters", "Why Does Predictive Maintenance Matter Now?"),
    ("Common challenges", "What Are the Most Common Challenges?"),
    ("How to get started", "How Should You Get Started With Predictive Maintenance?"),
    ("Key takeaways", "What Are the Key Takeaways?"),
    ("Frequently asked questions", "What Do Plant Teams Ask Most Often?"),
]
CN_H2 = [
    ("为什么重要", "为什么预测性维护如此重要？"),
    ("常见挑战", "最常见的挑战有哪些？"),
    ("如何开始", "应当如何着手引入预测性维护？"),
    ("核心要点", "核心要点是什么？"),
    ("常见问题", "工厂团队最常问的问题有哪些？"),
]
TW_H2 = [
    ("爲什麼重要", "爲什麼預測性維護如此重要？"),
    ("常見挑戰", "最常見的挑戰有哪些？"),
    ("如何開始", "應當如何着手引入預測性維護？"),
    ("核心要點", "核心要點是什麼？"),
    ("常見問題", "工廠團隊最常問的問題有哪些？"),
]

if __name__ == "__main__":
    en = path_of(SLUG, "en")
    h = open(en, encoding="utf-8").read()
    assert h.count(ANCHOR) == 1
    h = h.replace(ANCHOR, "\n" + EN_NEWS + "\n" + ANCHOR)
    open(en, "w", encoding="utf-8").write(h)
    print("EN body expanded")

    cn = path_of(SLUG, "cn")
    h = open(cn, encoding="utf-8").read()
    assert h.count(ANCHOR) == 1
    h = h.replace(ANCHOR, "\n" + ZH_NEWS + "\n" + ANCHOR)
    open(cn, "w", encoding="utf-8").write(h)
    print("CN body expanded")

    tw = path_of(SLUG, "tw")
    h = open(tw, encoding="utf-8").read()
    assert h.count(ANCHOR) == 1
    h = h.replace(ANCHOR, "\n" + s2t_fixed(ZH_NEWS) + "\n" + ANCHOR)
    open(tw, "w", encoding="utf-8").write(h)
    print("TW body expanded")

    for old, new in EN_H2:
        retitle_by_text(en, old, new)
    for old, new in CN_H2:
        retitle_by_text(path_of(SLUG, "cn"), old, new)
    for old, new in TW_H2:
        retitle_by_text(path_of(SLUG, "tw"), old, new)
    print("H2s converted in en/cn/tw")
