#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb001_apply import apply

SLUG = "agriculture-ai-precision-farming-sept-2025"

# ------------------------------------------------------------------ EN
EN_LEAD = ("September 2025 is the moment precision farming stops being a bet and starts being a line item. "
           "Across the Northern Hemisphere the harvest is coming in, and the operations that fused satellite "
           "imagery with in-field sensor data now have a season of hard evidence: where variable-rate application "
           "paid, where it did not, and what the difference was. This article reviews what the 2025 season "
           "actually delivered, quantifies the gains that held up, names the failure modes that cost the most, "
           "and sets out what to change before the 2026 season begins.")

EN_REPLACE = {
 "industry-landscape-and-market-trends": (
  "What Did the 2025 Season Reveal About Precision Farming?",
  """<p>The 2025 season settled an argument that ran for most of the last decade: precision agriculture works, but only where it is operated as a management discipline rather than purchased as a technology. The market signals agree. The precision agriculture market is estimated at roughly USD 10–12 billion in the mid-2020s and is forecast to more than double by the early 2030s, a compound growth rate in the low-to-mid teens. More interesting than the spending number is what the spending is on: the fastest-growing line items are no longer hardware but analytics, connectivity, and the services that turn imagery into a work order.</p>
<p>Three shifts defined the season. First, revisit frequency stopped being the constraint. With multiple public and commercial constellations in orbit, most broadacre operations now receive usable imagery every two to five days, which means the limiting factor is no longer data acquisition but interpretation speed. Second, in-field sensing became cheap enough to instrument representative zones rather than showcase blocks, which closed the gap between a satellite anomaly and its cause. Third, the buyer changed: as growers' associations and contract-farming networks aggregated demand, purchasing decisions moved from individual farms to regional programmes, raising the bar on evidence and support.</p>
<p>The consequence is that differentiation has moved downstream. Imagery is close to a commodity; the operations that gained in 2025 were the ones that compressed the path from detection to action, and that recorded what happened afterwards so the next season started from evidence instead of intuition.</p>"""),

 "implementation-patterns-and-best-practices": (
  "Which Implementation Patterns Delivered Results in 2025?",
  """<p>The programmes that produced measurable returns in 2025 shared a shape. They started from a short list of recurring decisions rather than from a platform, and they built backwards from those decisions to the data required.</p>
<ul>
<li><strong>Zone before prescription.</strong> Teams that invested first in stable management zones — derived from multi-year yield history, soil electrical conductivity, and topography — produced prescriptions that held up across a season. Those that re-zoned from a single season's imagery produced noisy maps that changed every pass and were quietly ignored.</li>
<li><strong>Satellite for coverage, sensors for cause, scouting for truth.</strong> The working pattern is a cascade: satellite flags where, probes and weather explain why, and scouting confirms what. Programmes that skipped the middle step generated alerts without explanations; programmes that skipped the last step never learned whether the alerts were right.</li>
<li><strong>Alerts with a recommendation and a deadline.</strong> An alert that says "field 12 north-east is stressed" is a data point. The same alert with "scout within 48 hours; if confirmed, irrigate before Thursday" changes behaviour. Every high-adoption programme we reviewed shipped recommendations, not just detections.</li>
<li><strong>Delivery inside the existing workflow.</strong> Adoption tracked the channel, not the accuracy. Alerts delivered to the phone or the farm's chat channel were acted on; the same alerts in a weekly PDF were not.</li>
<li><strong>A named owner per exception class.</strong> Water stress, nitrogen, disease risk, and equipment anomalies each had a person accountable for the decision. Unassigned alerts decayed.</li>
</ul>
<p>The corollary is that the highest-return first project is rarely the most ambitious one. Variable-rate nitrogen on a well-understood block, or irrigation scheduling on the highest-value fields, produced the clearest 2025 returns; fully autonomous intervention did not.</p>"""),

 "quantitative-impact-assessment": (
  "How Large Were the Measured Gains in 2025?",
  """<p>The gains that survived scrutiny in 2025 clustered into four categories, and the ranges below reflect what peer-reviewed trials and large commercial programmes consistently report rather than the best case on a showcase field.</p>
<ul>
<li><strong>Water.</strong> Precision irrigation driven by soil-moisture and evapotranspiration data reduced water use by roughly 20–50% against calendar-based scheduling, with the largest savings in regions where rainfall variability was highest. Energy cost fell alongside water volume because pumping fell.</li>
<li><strong>Nitrogen.</strong> Variable-rate nitrogen guided by in-season crop sensing typically cut total nitrogen applied by 10–20% while holding or slightly improving yield, because application moved to the zones and the timing where the crop could still respond.</li>
<li><strong>Yield.</strong> Yield effects were smaller and more variable than input savings — commonly 3–8% on fields where a treatable limitation was identified inside the response window, and close to zero where the season's constraint was weather rather than management. Programmes that promised double-digit yield uplift on every field lost credibility.</li>
<li><strong>Loss avoidance.</strong> The most under-reported return: earlier detection of disease or pest pressure protected yield that would otherwise have been lost. A single well-timed fungicide or irrigation pass on a high-value block often covered a season of monitoring across several hundred hectares.</li>
</ul>
<p>Stacked, these produced the payback numbers that justify the programme: most broadacre operations that ran a disciplined season reported the analytics and data costs recovered within one to two seasons, with the input savings carrying the case and yield providing the upside. The critical qualifier is discipline — the same spend spread across too many fields, or run without ground truth, produced dashboards rather than returns.</p>"""),

 "how-do-you-measure-precision-farming-roi": (
  "How Do You Measure Precision Farming ROI?",
  """<p>The cleanest ROI method is a paired comparison, because it isolates the intervention from the season. Choose comparable blocks — same soil type, variety, and planting date — manage one with the precision programme and one conventionally, and measure the difference in inputs applied, yield delivered, and margin per hectare. Where a true control is impractical, use a before-and-after comparison against a multi-year baseline for the same blocks, and be explicit that weather differences are inside the number.</p>
<p>Break the result into three lines so the number is defensible. Input savings are the easiest to verify: fertiliser, water, energy, and crop-protection volumes, valued at delivered prices. Yield effect is gross margin on the difference in tonnes, valued at the price actually received. Avoided loss requires an estimate, so state the assumption — typically the historical loss rate on comparable blocks in comparable seasons.</p>
<p>Then track the operational metrics that predict whether the financial result will repeat: share of fields with usable imagery each week, share of alerts acted on inside the recommended window, alert precision measured against scouting outcomes, and forecast error at defined points in the season. Farms that tracked only the money found out a season late that adoption had collapsed; farms that tracked adoption caught it in the first month.</p>"""),

 "challenges-and-risk-mitigation": (
  "What Went Wrong in 2025, and How Do You Mitigate It?",
  """<p>The 2025 failure modes were consistent enough to plan against.</p>
<ul>
<li><strong>Cloud gaps at the wrong moment.</strong> Persistent cloud during a critical growth stage left optical imagery unusable for weeks. Mitigation: contract for radar or a second constellation, and keep soil-moisture and weather telemetry as the always-available fallback so the irrigation decision never depends on a clear sky.</li>
<li><strong>Sensor drift and dead probes.</strong> A soil-moisture probe that drifts by a few percentage points produces confidently wrong irrigation advice. Mitigation: scheduled recalibration, automated plausibility checks against rainfall and evapotranspiration, and alerts on missing data rather than silent gaps.</li>
<li><strong>Alert fatigue.</strong> Systems tuned for sensitivity flooded agronomists in a wet season, and response rates collapsed. Mitigation: tune thresholds with the people who receive them, prioritise by economic consequence, and cap the number of alerts per field per week.</li>
<li><strong>Zone instability.</strong> Management zones rebuilt from a single season's data changed after every pass, so prescriptions lost credibility. Mitigation: build zones from multi-year history and revise them annually, not continuously.</li>
<li><strong>Connectivity and integration debt.</strong> Field teams could not reach the platform, or data landed in a silo the agronomist never opened. Mitigation: offline-capable mobile delivery, and integration into the farm management system rather than a parallel interface.</li>
<li><strong>No ground truth.</strong> Where scouting results and harvest yield were never recorded, nobody could prove the programme worked, and renewal conversations were lost on opinion.</li>
</ul>
<p>Every one of these is cheaper to design out than to fix mid-season. The common thread is that the failure is organisational before it is technical.</p>"""),

 "future-outlook-and-strategic-implications": (
  "What Should Farms Plan for in 2026?",
  """<p>Three developments will shape the next season. The first is richer sensing becoming routine: more spectral bands, more frequent commercial revisits, and cheaper in-field probes will make within-field variability visible at a resolution that turns zone management into something closer to plant-level management. The operational question shifts from "can we see it" to "who acts on it, and how fast".</p>
<p>The second is that models will be judged season over season rather than on demonstration. Buyers increasingly ask for last season's verified error rates on comparable fields, in comparable conditions. That favours operations that built the ground-truth loop early, because accumulated outcome data is the one asset that cannot be bought retroactively.</p>
<p>The third is consolidation of the delivery channel. As conversational interfaces mature, the practical difference between farms will not be which analytics platform they bought but whether an agronomist can ask "which blocks need scouting before the weekend" and get a grounded, cited answer in seconds. Precision farming is converging on the same pattern as enterprise analytics: the value sits in the speed and trust of the answer, not in the volume of the data behind it.</p>"""),
}

EN_SECTIONS = [
 ("which-precision-practices-paid-back-fastest-in-2025",
  "Which Precision Practices Paid Back Fastest in 2025?",
  """<p>Not every precision practice returns the same, and the ranking was stable across the operations we reviewed. Irrigation scheduling paid back first and most reliably, because water and the energy to move it are immediate, measurable costs and the response window is short and repeatable. Variable-rate nitrogen came next: material input savings, modest yield upside, and a decision that recurs several times per season, which multiplies the value of getting it right.</p>
<p>Variable-rate seeding paid back more slowly and only where historic yield variability within a field was genuinely large and stable; on uniform fields it mainly moved cost around. Disease and pest early warning had the highest variance — near zero value in a low-pressure season, and the single largest return in a high-pressure one — which argues for treating it as insurance and budgeting it that way rather than judging it on an average year.</p>
<p>Yield forecasting sat in a category of its own: it rarely produced an agronomic return directly, but it consistently improved marketing, storage, and logistics decisions. Operations that used mid-season forecasts to shape forward sales and harvest sequencing reported financial effects comparable to the input savings, from a capability that costs a fraction of the sensing stack.</p>"""),

 ("how-do-you-turn-one-season-of-data-into-next-seasons-advantage",
  "How Do You Turn One Season of Data into Next Season's Advantage?",
  """<p>The compounding asset in precision farming is not the imagery; it is the record of what happened. Turning one season into the next requires a deliberate close-out, and the best-run programmes treat it as a scheduled task rather than an afterthought.</p>
<p>Start by reconciling every alert against its outcome: of the stress alerts issued, how many were confirmed in the field, and of those, how many changed a decision that improved the result. That single ratio tells you whether to tighten or loosen thresholds next season. Then reconcile every forecast against harvested yield, by block and by forecast date, which tells you how early in the season your estimates become decision-grade.</p>
<p>Next, refresh the inputs that drive next year's prescriptions. Rebuild management zones using the yield map you just produced, because a zone map that ignores the most recent season is a map of the past. Record which fields underperformed their soil potential and investigate why — the answer is often a drainage, compaction, or pH issue that no amount of in-season intervention will fix, and that is far cheaper to correct between seasons than during one.</p>
<p>Finally, write down what you will stop doing. Programmes that only add practices accumulate cost faster than insight; the ones that compound are the ones that retire the alerts nobody acted on and the prescriptions that never changed an outcome.</p>"""),
]

EN_FAQ = [
 ("What did the 2025 season show about precision farming ROI?",
  "The gains that held up were concentrated in inputs rather than yield. Precision irrigation driven by soil-moisture and evapotranspiration data reduced water use by roughly 20–50% against calendar scheduling; variable-rate nitrogen typically cut applied nitrogen by 10–20% while holding yield; and yield effects were real but smaller and more weather-dependent, commonly 3–8% where a treatable limitation was caught inside the response window. Avoided loss from earlier disease and pest detection was the most under-reported contributor, and often the largest single-season return."),
 ("Which precision farming practice should a farm start with?",
  "Start with the practice that recurs most often and has the shortest, most measurable feedback loop — usually irrigation scheduling, followed by variable-rate nitrogen. Both produce a cost line that can be verified within a season, and both depend on data most operations already collect or can collect cheaply. Variable-rate seeding and fully autonomous intervention should wait until multi-year yield data supports stable management zones."),
 ("How do you measure precision farming ROI credibly?",
  "Use a paired comparison: two comparable blocks, one managed with the programme and one conventionally, measuring input volumes, yield, and margin per hectare. Where a control is impractical, compare against a multi-year baseline for the same blocks and state that weather sits inside the number. Report the three lines separately — input savings, yield effect, and avoided loss with its assumption — and pair the financial result with adoption metrics, because an unused system produces no return."),
 ("What are the most common reasons precision farming programmes fail?",
  "The recurring causes are organisational rather than technical: cloud gaps at critical growth stages with no fallback data source, drifting or dead soil-moisture sensors that are never recalibrated, alert thresholds tuned for sensitivity so response rates collapse, management zones rebuilt from a single season so prescriptions keep changing, insights delivered in a channel the field team never opens, and no recorded ground truth so the programme cannot be defended at renewal."),
 ("What should farms change before the 2026 season?",
  "Three things. Close out 2025 properly by reconciling every alert against its outcome and every forecast against harvested yield, then rebuild management zones from the new yield map. Secure a second data source so a cloudy fortnight cannot blind the programme at a critical growth stage. And move delivery into the channel the field team already uses, because adoption — not accuracy — is what converts a precision programme into a return."),
]

EN_RENAMES = {}

EN = {"lead": EN_LEAD, "replace": EN_REPLACE, "renames": EN_RENAMES, "sections": EN_SECTIONS, "faq": EN_FAQ,
      "excerpts": [
        "Building inclusive AI and data teams: what the evidence says actually changes outcomes.",
        "Why your data strategy needs a dedicated AI agent layer in 2026.",
        "Vector databases for enterprise search: a practical 2026 guide."]}

# ------------------------------------------------------------------ zh-CN
ZHCN_LEAD = ("2025年9月是精准农业从一场押注变成一行预算的时刻。北半球的收获季陆续到货，那些把卫星影像与田间传感器数据融合起来的经营主体，如今掌握了一整季的硬证据：变量施用在哪里产生了回报、在哪里没有，以及差别究竟出在哪里。本文回顾2025年这一季实际交付了什么，量化经得起检验的收益，指出代价最高的失败模式，并给出在2026年季前应当改变的做法。")

ZHCN_REPLACE = {
 "行业格局与市场趋势": (
  "2025年这一季揭示了精准农业的什么？",
  """<p>2025年这一季终结了一场持续近十年的争论：精准农业是有效的，但只有在被当作管理纪律来运营、而不是当作技术来采购时才成立。市场信号也印证了这一点。精准农业市场在2020年代中期估计约为100亿到120亿美元，预计到2030年代初将翻一番以上，复合增长率在十几个百分点区间。比支出规模更值得关注的是支出结构：增长最快的科目已经不是硬件，而是分析、连接服务，以及把影像转化为作业工单的服务。</p>
<p>有三个变化定义了这一季。第一，回访频次不再是瓶颈。随着多套公共与商业星座在轨运行，多数大田经营主体现在每两到五天就能拿到可用影像，限制因素已经从数据获取转为解读速度。第二，田间感知的成本下降到足以在代表性区域而非样板田上布设，从而弥合了"卫星发现异常"与"异常成因"之间的缺口。第三，采购主体发生了变化：随着种植者协会与订单农业网络聚合需求，采购决策从单个农场转向区域项目，对证据与服务能力的要求随之提高。</p>
<p>结果是竞争差异向下游转移。影像已接近商品化；2025年真正获益的，是那些压缩了从发现到行动之间路径、并把事后结果记录下来、让下一季从证据而非直觉出发的经营主体。</p>"""),

 "实施模式与最佳实践": (
  "哪些实施模式在2025年真正产出了结果？",
  """<p>2025年产出可衡量回报的项目有一个共同形态：它们从一份简短的高频决策清单出发，而不是从一个平台出发，再从这些决策反推所需的数据。</p>
<ul>
<li><strong>先分区，再处方。</strong> 先用多年产量历史、土壤电导率和地形建立稳定管理区的团队，做出的处方能稳定支撑一整季；只用单季影像重新分区的团队，产出的图每次飞过都在变，最终被悄悄搁置。</li>
<li><strong>卫星看范围，传感器看成因，巡查看真相。</strong> 有效的模式是级联：卫星指出在哪里，探头与气象解释为什么，巡查确认到底是什么。跳过中间环节的项目只能产生没有解释的预警；跳过最后一环的项目永远不知道预警到底对不对。</li>
<li><strong>预警必须带建议和时限。</strong> "12号地块东北角出现胁迫"只是一个数据点；同样一条预警加上"48小时内完成巡查，若确认则在周四前灌溉"，才能改变行为。我们看到的高采纳率项目，发出的都是建议，而不只是检测结果。</li>
<li><strong>在既有工作流中交付。</strong> 采纳率取决于渠道，而不是准确率。发到手机或农场日常沟通工具的预警会被执行；装进每周PDF的同一条预警不会。</li>
<li><strong>每类异常都有具名负责人。</strong> 水分胁迫、氮肥、病害风险、设备异常各有明确的决策责任人；无人认领的预警会自然衰减。</li>
</ul>
<p>推论是：回报最高的第一个项目，往往不是最有野心的那个。在充分理解的地块上做变量施氮，或在价值最高的地块上做灌溉排程，在2025年产生了最清晰的回报；完全自主的干预则没有。</p>"""),

 "量化影响评估": (
  "2025年经得起检验的收益有多大？",
  """<p>2025年经得起审视的收益集中在四类，以下区间反映的是同行评议试验与大型商业项目的一致结论，而不是样板田的最好情况。</p>
<ul>
<li><strong>水分。</strong> 以土壤水分与蒸散量驱动的精准灌溉，相比按日历排程的灌溉减少用水约20%到50%，在降雨变率最大的地区节约最显著。随着抽水量下降，能耗成本与用水量同步下降。</li>
<li><strong>氮肥。</strong> 以季内作物感知指导的变量施氮，通常把总施氮量降低10%到20%，同时产量持平或略有提升——因为肥料被转移到了作物仍能响应的区域和时点。</li>
<li><strong>产量。</strong> 产量效应比投入节约更小、也更不稳定：在响应窗口内识别出可处理限制因素的地块上通常为3%到8%；而当季的约束是天气而非管理时，则接近于零。承诺每块地都实现两位数增产的项目，最终都失去了公信力。</li>
<li><strong>避免损失。</strong> 这是最少被计入的回报：更早发现病害或虫害压力，保住了原本会损失的产量。在高价值地块上，一次时机得当的施药或灌溉，其收益往往足以覆盖数百公顷一整季的监控成本。</li>
</ul>
<p>叠加起来，就构成了支撑项目的回报数字：多数运行了规范一季的大田经营主体报告，分析与数据成本在一到两季内收回，其中投入品节约承担主要论证，产量提供上行空间。关键的限定条件是纪律——同样的投入摊薄到过多地块，或者没有地面真值支撑，产出的就只是仪表板，而不是回报。</p>"""),

 "挑战与风险缓解": (
  "2025年哪些地方出了问题，如何缓解？",
  """<p>2025年的失败模式足够一致，值得提前做预案。</p>
<ul>
<li><strong>关键时期的云层缺口。</strong> 关键生育期持续多云，会导致光学影像连续数周不可用。缓解方式：签约雷达或第二套星座，并把土壤水分与气象遥测作为始终可用的兜底数据源，让灌溉决策不依赖晴天。</li>
<li><strong>传感器漂移与探头失效。</strong> 土壤水分探头漂移几个百分点，就会产出自信但错误的灌溉建议。缓解方式：定期重新标定、对照降雨与蒸散量做自动合理性校验，并对数据缺失而非静默空值发出告警。</li>
<li><strong>预警疲劳。</strong> 为追求灵敏度而设置的阈值，在多雨季节会淹没农艺师，响应率随之崩塌。缓解方式：与接收预警的人一起调校阈值，按经济后果排序，并限制每块地每周的预警条数。</li>
<li><strong>管理区不稳定。</strong> 用单季数据重建的管理区每次飞过都在变，处方因此失去公信力。缓解方式：用多年历史建立管理区，每年修订一次，而不是持续重算。</li>
<li><strong>连接与集成欠账。</strong> 田间团队连不上平台，或者数据落进了农艺师从不打开的信息孤岛。缓解方式：支持离线的移动端交付，并集成进农场管理系统，而不是另建一套界面。</li>
<li><strong>没有地面真值。</strong> 如果巡查结果与收获产量从未被记录，就没有人能证明项目有效，续约讨论最终只能停留在主观判断上。</li>
</ul>
<p>每一项在设计阶段排除，都比在季中补救更便宜。共同点是：失败首先是组织性的，其次才是技术性的。</p>"""),

 "未来展望与战略意义": (
  "农场在2026年应当做哪些规划？",
  """<p>三个进展将塑造下一季。第一是更丰富的感知正在成为常态：更多光谱波段、更频繁的商业回访、更廉价的田间探头，会把田内变异性呈现到接近单株管理的分辨率。运营问题随之从"我们能不能看见"转向"谁来执行，以及多快执行"。</p>
<p>第二是模型将按季而非按演示被评判。采购方越来越频繁地要求提供上一季在可比地块、可比条件下的实测误差率。这有利于早早建立了地面真值闭环的经营主体，因为累积的结果数据是无法事后购买的唯一资产。</p>
<p>第三是交付渠道的集中化。随着对话式界面走向成熟，农场之间的实际差异将不再是买了哪套分析平台，而是农艺师能不能问出"周末之前哪几个地块需要巡查"，并在几秒内得到一个有依据、可溯源的答案。精准农业正在收敛到与企业分析相同的规律：价值在于答案的速度与可信度，而不在于背后数据量的大小。</p>"""),
}

ZHCN_SECTIONS = [
 ("哪些精准农业实践在2025年回本最快",
  "哪些精准实践在2025年回本最快？",
  """<p>不同精准实践的回报并不相同，而且在我们审阅的经营主体中排序相当稳定。灌溉排程回本最早、也最可靠，因为水以及输水的能耗是即时、可计量的成本，且响应窗口短而可重复。变量施氮紧随其后：投入品节约实实在在，产量上行有限，而这个决策每季会重复多次，从而放大做对的价值。</p>
<p>变量播种回本更慢，而且只在田内历史产量变异确实大且稳定的地块上成立；在均匀地块上，它主要只是把成本挪了个位置。病害与虫害早期预警的方差最大——低压力年份几乎不产生价值，高压力年份则贡献单季最大的一笔回报，因此应当按保险来对待和预算，而不是用平均年份来评判。</p>
<p>产量预测属于单独一类：它很少直接带来农艺回报，但持续改善了销售、仓储与物流决策。用季中预测来指导预售与收获排序的经营主体，其财务效果可与投入品节约相当，而这项能力的成本只占感知体系的一小部分。</p>"""),

 ("如何把一个季度的数据转化为下一季的优势",
  "如何把一季的数据转化为下一季的优势？",
  """<p>精准农业中可复利的资产不是影像，而是"实际发生了什么"的记录。把一季转化为下一季的优势需要一次有意识的收尾，而运行得最好的项目都把它当作计划内任务，而不是事后补做。</p>
<p>首先把每一条预警与实际结果核对：发出的胁迫预警中有多少在田间被确认，其中又有多少改变了决策并改善了结果。这一个比值就告诉你下一季该收紧还是放宽阈值。然后把每一次预测与实收产量按地块、按预测日期核对，从而知道你的估计在季内什么时点开始具备决策价值。</p>
<p>接着刷新驱动下一年处方的输入。用刚产出的产量图重建管理区，因为忽略最近一季的分区图只是过去的地图。记录哪些地块低于其土壤潜力并查明原因——答案往往是排水、压实或酸碱度问题，季内的任何干预都解决不了，而在季间处理则便宜得多。</p>
<p>最后，把"要停掉什么"写下来。只会增加实践的项目，成本累积快于洞察累积；真正能复利的项目，会淘汰那些从没人执行的预警，以及那些从未改变过结果的处方。</p>"""),
]

ZHCN_FAQ = [
 ("2025年这一季显示了精准农业怎样的投资回报？",
  "经得起检验的收益集中在投入品而非产量上。以土壤水分与蒸散量驱动的精准灌溉，相比按日历排程减少用水约20%到50%；变量施氮通常把施氮量降低10%到20%而产量持平；产量效应真实存在但更小、也更依赖天气，在响应窗口内识别出可处理限制因素的地块上通常为3%到8%。更早发现病害与虫害所避免的损失是最少被计入的贡献，也往往是单季最大的一笔回报。"),
 ("农场应该从哪一项精准实践起步？",
  "从重复频率最高、反馈回路最短且最容易计量的实践起步——通常是灌溉排程，其次是变量施氮。两者都会在一个季度内产生可验证的成本项，而且都依赖多数经营主体已经采集或可以廉价采集的数据。变量播种和完全自主的干预，应当等到多年产量数据足以支撑稳定管理区之后再考虑。"),
 ("如何可信地衡量精准农业的投资回报？",
  "采用配对比较：选取两块条件相当的地块，一块按项目方案管理、一块按常规方式管理，计量投入品用量、产量与每公顷毛利。无法设置对照时，用同地块的多年基线做前后对比，并明确说明天气差异包含在数字之内。把投入品节约、产量效应、避免损失（连同其假设）三项分开列示，并配套跟踪采纳率指标——没人使用的系统不会产生任何回报。"),
 ("精准农业项目失败的最常见原因是什么？",
  "反复出现的原因主要不是技术性的：关键生育期遇到云层缺口且没有兜底数据源；土壤水分探头漂移或失效却从不重新标定；阈值一味追求灵敏导致响应率崩塌；用单季数据重建管理区导致处方不断变化；洞察被交付到田间团队从不打开的渠道；以及没有记录地面真值，导致续约时无法证明项目价值。"),
 ("在2026年季前，农场应当改变什么？",
  "三件事。认真收尾2025年：把每条预警与实际结果核对、把每次预测与实收产量核对，并用新的产量图重建管理区。落实第二个数据源，避免关键生育期连续两周多云就让项目失明。以及把交付迁移到田间团队已经在用的渠道——决定精准项目能否转化为回报的是采纳率，而不是准确率。"),
]

ZHCN_RENAMES = {}

ZHCN = {"lead": ZHCN_LEAD, "replace": ZHCN_REPLACE, "renames": ZHCN_RENAMES,
        "sections": ZHCN_SECTIONS, "faq": ZHCN_FAQ,
        "excerpts": [
          "建立包容的AI与数据团队：证据表明什么才真正改变结果。",
          "为什么2026年的数据战略需要一个专门的AI智能体层。",
          "向量数据库在企业搜索中的应用：2026年实用指南。"]}

# ------------------------------------------------------------------ zh-TW (converted)
import _gb001_s2t as T
ZHTW = T.spec_s2tw(ZHCN)

if __name__ == "__main__":
    for lang, spec in (("en", EN), ("zh-CN", ZHCN), ("zh-TW", ZHTW)):
        b, a, n = apply(SLUG, lang, spec)
        print(f"{SLUG} {lang}: {b} -> {a}  [{', '.join(n)}]")
