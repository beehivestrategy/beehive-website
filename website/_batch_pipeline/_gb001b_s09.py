#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""slug 09: data-visualization-ai-insights
EN 1415 -> ~2600 ; CN/TW 2212 -> ~3600 ; H2 -> questions."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gb001b_lib import path_of, retitle_by_text, s2t_fixed

SLUG = "data-visualization-ai-insights"

EN_NEWS = """<h2 id="how-do-you-design-a-visual-specification">How Do You Design a Visual Specification?</h2>
<p>A visual specification is a short document that decides in advance how the organisation's recurring questions will be drawn, and it is the highest-leverage artefact in this entire discipline. For each of the five to ten decisions the business makes weekly, it records four things: the chart type, the comparison that matters, the target or threshold, and what counts as an alarm. A gross margin decision becomes "line chart, twelve trailing months, target band shaded, alarm when two consecutive months fall below the band." That single line removes dozens of ad-hoc design choices from every future conversation.</p>
<p>The specification works because it separates two decisions that are otherwise constantly conflated: what to show, and how to show it. What to show belongs to the business owner of the decision, who knows which comparison drives action. How to show it belongs to whoever owns the visual language, who knows that a truncated axis will mislead and that sixteen colours will not be read. Codifying both means the conversational system can produce a correct chart without a design debate each time, and it means two teams looking at the same metric see the same thing.</p>
<p>Two rules keep the specification from becoming shelfware. Keep it short enough to review in a quarterly meeting — if it takes a day to read, nobody will maintain it. And version it with named owners per decision, because the comparison that matters changes when the business changes, and an unowned specification is a stale one. Teams that follow this find the specification becomes the reference for onboarding new analysts and the fastest way to settle a chart argument: not taste, but the agreed rule.</p>
<h2 id="how-should-uncertainty-be-shown">How Should Uncertainty and Data Quality Be Shown?</h2>
<p>The most consequential design choice in enterprise visualisation is how the system behaves when it is not confident, and most systems get it wrong by saying nothing. A forecast rendered as a single confident line invites the reader to treat it as fact; the same forecast with a shaded confidence band invites the right question, which is how much the answer depends on assumptions. Showing uncertainty is not hedging — it is what allows a decision-maker to size the risk of acting.</p>
<p>Three patterns cover most cases. Confidence bands or error bars for anything estimated, with the band width doing the communicating rather than a footnote. Explicit sample-size annotation whenever a segment is small enough that the number is volatile, because a 40% swing on eleven records is noise and should look like noise. And staleness indicators showing when the underlying data was last refreshed, which matters enormously in conversational contexts where the user cannot see the pipeline behind the answer.</p>
<p>Data quality deserves the same treatment. If a source was partially unavailable for part of the period shown, the chart should say so where the gap is, not in a footer. If a definition changed mid-series, the chart should mark the break rather than presenting a smooth line across two incompatible regimes. These are not edge cases in enterprise data; they are the normal condition, and a system that hides them produces confident answers on broken foundations — which is the fastest way to lose the trust that took months to build.</p>
<h2 id="which-visual-mistakes-do-ai-systems-make">Which Visual Mistakes Do AI Systems Make Most Often?</h2>
<p>Generated charts fail in recognisable ways, and knowing the failure modes is most of the defence. The truncated y-axis is the classic: starting a scale at a value other than zero makes a trivial change look dramatic, and studies of chart literacy repeatedly find a substantial share of readers drawing the wrong conclusion from it. Related to it is dual-axis confusion, where two series on different scales appear to cross at a meaningful point that is purely an artefact of the scaling choice.</p>
<p>The second family is over-encoding: too many colours, too many series, a 3D effect, or a pie chart with nine slices. Each addition costs the reader working memory and returns nothing, and the failure is worse in a chat thread than in a report, because the chart is smaller and read faster. The third is the unlabelled axis or the missing unit, which turns a correct number into an ambiguous one — a margin shown as 4.3 could be a percentage or a currency amount, and the reader who has to ask has already lost the thread.</p>
<p>The fourth is the most insidious because it is not a drawing error at all: the correct chart of the wrong population. An answer that silently filters to a subset, applies a different date grain, or uses a metric that sounds right but is defined differently will produce a perfectly drawn, entirely misleading visual. This is why the semantic layer matters as much as the charting library, and why the good systems expose the query behind the visual. A user who can see what was actually computed can catch the error; a user who sees only the picture cannot.</p>
<h2 id="how-do-you-measure-whether-visuals-work">How Do You Measure Whether Visuals Are Actually Working?</h2>
<p>The instrumentation is simple and rarely built. For each recurring visual, track three numbers: how often it is generated, how often the answer leads to a documented action, and how often the user asks a follow-up question. High generation with low action is chart spam, and the fix is to make the visual conditional rather than automatic. High follow-up volume is more interesting: it usually means the chart raised the right question but did not answer it, which is a specification problem — the comparison chosen was not the comparison the decision needed.</p>
<p>Time-to-decision is the metric that matters to the business, and it can be measured roughly without heavy machinery: for the recurring decisions in the specification, record how long from the question being asked to the action being taken, before and after conversational visuals. Teams that do this consistently find the largest gain is not in reading speed but in the elimination of the follow-up cycle — the second meeting that existed only because the first one could not answer an unanticipated question.</p>
<p>The qualitative signal is worth capturing too, and it is easy: a standing question in the team's weekly review about which charts produced action and which were ignored. That review is what keeps the specification alive, and it makes the ownership question answerable. Organisations that run it end up with a small, sharp set of visuals that people rely on; organisations that do not accumulate charts the way they accumulate dashboards, and for the same reason.</p>
"""

ZH_NEWS = """<h2 id="如何设计可视化规范">应当如何设计可视化规范？</h2>
<p>可视化规范是一份简短文档，它提前约定组织内反复出现的问题应当如何被画出来，也是这一整套方法里杠杆率最高的产物。针对企业每周要做出的五到十个决策，它记录四件事：图表类型、真正重要的对比关系、目标或阈值、以及什么情况算警报。一个毛利率决策会变成这样一行："折线图、滚动十二个月、目标区间加底纹、连续两个月低于区间即触发警报。"就这一行，免掉了此后每一次对话中几十次临时的设计取舍。</p>
<p>规范之所以有效，是因为它把两件原本总被混在一起的事分开了：展示什么，与如何展示。展示什么属于该决策的业务负责人，因为他知道哪种对比能驱动行动；如何展示属于视觉语言的负责人，因为他知道截断坐标轴会误导读者、十六种颜色不会被真正读懂。把两者都固化下来，对话式系统就能在不做设计争论的前提下输出正确的图表，而且两个团队看同一个指标时看到的是同一个东西。</p>
<p>两条规则能防止规范变成摆设。保持它短到可以在一次季度会上审完——如果需要一整天才能读完，没人会维护它。并为它做版本管理、给每个决策指定具名负责人，因为真正重要的对比会随业务变化，而没有负责人的规范必然是过时的规范。遵循这一点的团队会发现，规范成了新分析师入职的参考材料，也是终结图表争论最快的方式：不靠审美，而靠事先约定的规则。</p>
<h2 id="不确定性与数据质量应如何呈现">不确定性与数据质量应当如何呈现？</h2>
<p>企业级可视化中最有后果的设计选择，是系统在"不确定"时如何表现，而多数系统错在什么都不说。一条自信的单线预测会诱使读者把它当成事实；同样的预测加上一层置信区间的阴影底纹，则引出了正确的问题——这个答案在多大程度上依赖假设。呈现不确定性不是推卸责任，它恰恰是让决策者能够衡量行动风险的前提。</p>
<p>三种模式覆盖了大多数场景。凡是估计值，都用置信带或误差线，让带宽本身去传达信息，而不是靠脚注说明。凡是样本量小到数字会剧烈波动的分段，都显式标注样本量，因为十一条记录上出现的百分之四十波动就是噪声，应当看起来像噪声。此外还要显示底层数据的刷新时间，这在对话场景中尤其重要，因为用户看不到答案背后的数据管道。</p>
<p>数据质量值得同等对待。如果某个数据源在所示区间的某段时间部分不可用，图表应当在缺口处直接说明，而不是放在页脚。如果口径在序列中途发生变更，图表应当标出断点，而不是画一条平滑的线跨越两个不可比的区段。这些在企业数据里不是边界情况，而是常态；一个把它们藏起来的系统，会在破损的地基上给出自信的答案——这正是失去数月才建立起来的信任的最快方式。</p>
<h2 id="ai系统最常犯哪些可视化错误">AI系统最常犯哪些可视化错误？</h2>
<p>生成的图表会以一些可识别的方式失败，而了解这些失败模式，防线就建立了一大半。首当其冲的是截断 Y 轴：让刻度不从零开始，会把微不足道的变化放大得触目惊心，而图表素养研究反复发现相当比例的读者会因此得出错误结论。与之相关的是双轴混淆——两条不同量纲的曲线看似在一个有意义的点交叉，而那纯粹是缩放选择的产物。</p>
<p>第二类是过度编码：颜色太多、序列太多、加了 3D 效果、或者一个九块的饼图。每加一样都在消耗读者的工作记忆，却不带来任何回报；而这种失败在对话线程中比在报告里更严重，因为图更小、读得更快。第三类是坐标轴没有标签或缺失单位，它把一个正确的数字变成了有歧义的数字——显示为 4.3 的毛利率，可能是百分比，也可能是金额，而一旦读者需要开口问，他已经跟不上上下文了。</p>
<p>第四类最隐蔽，因为它根本不是绘图错误：画了一张正确的图，对象却是错误的人群。一个答案静默地筛选到了子集、套用了不同的日期粒度、或者用了一个听起来对但口径不同的指标，就会产出一张绘制精美、却完全误导的图。正因为如此，语义层与图表库同等重要，也正因为如此，好的系统会暴露图表背后的查询。能看到实际算的是什么的用户，才可能发现错误；只看到一张图的用户，不可能。</p>
<h2 id="如何衡量可视化是否真的奏效">如何衡量可视化是否真的奏效？</h2>
<p>度量方法很简单，却很少有人真正去做。对每个反复出现的图表，跟踪三个数字：它被生成的频率、它带来有记录行动的频率、以及用户追问的频率。生成量高而行动率低，说明这是图表垃圾，解决办法是把可视化改为条件触发而非无条件附带。追问量高则更有意思：它通常意味着图提出了正确的问题却没回答它，而这属于规范问题——所选的对比并不是决策需要的那个对比。</p>
<p>对业务真正重要的指标是决策耗时，而且不需要重型工具也能粗略测量：针对规范中那些反复出现的决策，记录从提问到采取行动的时间，对比引入对话式可视化前后的差异。认真做这件事的团队会发现，最大的收益不在于阅读速度，而在于消除了后续循环——那种只因为第一次会议答不上一个未曾预料的问题才存在的第二次会议。</p>
<p>定性信号同样值得收集，而且很容易：在团队的周会上设一个固定问题，问哪些图表带来了行动、哪些被忽略了。正是这个评审让规范保持鲜活，也让"由谁负责"这个问题变得可回答。坚持做这件事的组织，最终会拥有一小组人们真正依赖的、锋利的可视化；不做的组织，则会像堆积仪表板那样堆积图表，原因也一模一样。</p>
"""

EN_H2 = [
    ("Why it matters", "Why Does Visualisation Matter for AI Insights?"),
    ("Common challenges", "What Are the Most Common Obstacles?"),
    ("How to get started", "How Should You Get Started With AI-Driven Visuals?"),
    ("From Dashboards to Conversational Visuals", "How Do You Move From Dashboards to Conversational Visuals?"),
    ("Frequently asked questions", "What Do Teams Ask Most Often About AI Visualisation?"),
]
CN_H2 = [
    ("为什么重要", "为什么可视化对AI洞察如此重要？"),
    ("常见挑战", "最常见的障碍有哪些？"),
    ("如何开始", "应当如何着手引入AI驱动的可视化？"),
    ("核心要点", "核心要点是什么？"),
    ("常见问题", "团队最常问的问题有哪些？"),
]
TW_H2 = [
    ("爲什麼重要", "爲什麼視覺化對AI洞察如此重要？"),
    ("常見挑戰", "最常見的障礙有哪些？"),
    ("如何開始", "應當如何着手引入AI驅動的視覺化？"),
    ("核心要點", "核心要點是什麼？"),
    ("常見問題", "團隊最常問的問題有哪些？"),
]

if __name__ == "__main__":
    en = path_of(SLUG, "en")
    h = open(en, encoding="utf-8").read()
    anchor = '            <section class="faq-section"'
    assert h.count(anchor) == 1
    h = h.replace(anchor, "\n" + EN_NEWS + "\n" + anchor)
    open(en, "w", encoding="utf-8").write(h)
    print("EN body expanded")

    cn = path_of(SLUG, "cn")
    h = open(cn, encoding="utf-8").read()
    assert h.count(anchor) == 1
    h = h.replace(anchor, "\n" + ZH_NEWS + "\n" + anchor)
    open(cn, "w", encoding="utf-8").write(h)
    print("CN body expanded")

    tw = path_of(SLUG, "tw")
    h = open(tw, encoding="utf-8").read()
    assert h.count(anchor) == 1
    h = h.replace(anchor, "\n" + s2t_fixed(ZH_NEWS) + "\n" + anchor)
    open(tw, "w", encoding="utf-8").write(h)
    print("TW body expanded")

    for old, new in EN_H2:
        retitle_by_text(en, old, new)
    for old, new in CN_H2:
        retitle_by_text(path_of(SLUG, "cn"), old, new)
    for old, new in TW_H2:
        retitle_by_text(path_of(SLUG, "tw"), old, new)
    print("H2s converted in en/cn/tw")
