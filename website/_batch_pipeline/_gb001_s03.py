#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb001_apply import apply

SLUG = "agriculture-ai-crop-monitoring"

EN_SECTIONS = [
 ("which-data-sources-matter-most-for-crop-monitoring",
  "Which Data Sources Matter Most for Crop Monitoring?",
  """<p>Every sensing layer answers a different question, and buying them in the wrong order is the most common waste in agriculture AI programmes. Satellite imagery is the backbone: it covers every field you operate, revisits on a predictable cadence, and gives you comparable vegetation indices across the whole estate. Its limits are resolution and clouds — a satellite pass tells you a zone is stressed, not which plants are affected.</p>
<p>Drones answer the "show me exactly" question. Multispectral flights at centimetre resolution turn a satellite anomaly into a scouting target, and thermal imagery separates water stress from disease stress when the two look identical in a vegetation index. The trade-off is cost per hectare and pilot logistics, which is why drones are a targeting tool triggered by satellite, not a monitoring layer.</p>
<p>Soil moisture and weather stations supply the causal half of the picture. A vegetation index tells you that a field is underperforming; soil moisture, evapotranspiration, and local rainfall tell you why. In-field probes are expensive per point, so place them in representative zones and let the model interpolate rather than trying to instrument every block. Finally, the farm management system — planting dates, varieties, input records, historical yield — is what makes any of it interpretable: an index without variety and growth-stage context is a number without a reference.</p>"""),

 ("how-accurate-are-ai-yield-predictions-and-when",
  "How Accurate Are AI Yield Predictions, and When Do They Get Reliable?",
  """<p>Yield forecasting accuracy is a curve, not a number, and the shape of the curve is what buyers should ask about. Early in the season, before canopy closure, forecasts are dominated by planting date, variety, and weather scenarios; error bands are wide, typically plus or minus 15–25%. Their value at that stage is not precision but planning — input procurement, storage capacity, and contract positioning all improve with a directional estimate delivered early.</p>
<p>Accuracy tightens sharply after canopy closure, when satellite and drone indices start measuring actual biomass rather than potential. Mid-season estimates commonly narrow to within 8–12% of realised yield, and that is the point at which forecasts become operationally decisive: irrigation and nitrogen decisions still have time to change the outcome. In the final weeks before harvest, well-calibrated models on crops with good historical ground truth routinely land within 3–6%, which is accurate enough for logistics, marketing, and forward sales.</p>
<p>Two caveats matter more than the headline figure. First, accuracy is local: a model calibrated on your fields, varieties, and soils beats a regional model every time, which is another argument for the ground-truth loop. Second, accuracy is conditional on weather realisation — every forecast is a yield-to-date estimate plus a weather assumption, and honest systems publish that assumption rather than presenting a single number.</p>"""),

 ("how-do-you-build-the-ground-truth-loop-that-improves-accuracy",
  "How Do You Build the Ground-Truth Loop That Improves Accuracy?",
  """<p>A crop-monitoring system becomes a learning system only if what happened in the field is recorded in a form the model can consume. That sounds obvious and is almost universally done badly, because scouting notes live in notebooks, messaging apps, and PDF reports that no pipeline reads. The loop has four steps and each one has a failure mode.</p>
<ul>
<li><strong>Capture:</strong> record scouting findings, pest and disease confirmation, treatment applications, and final harvest yield per field or management zone. Failure mode: free-text notes with no field identifier, which cannot be joined to anything.</li>
<li><strong>Structure:</strong> store them against a stable field ID and a timestamp, with units and a measurement method. Failure mode: yield recorded in different units across regions.</li>
<li><strong>Compare:</strong> automatically reconcile every alert and forecast against the outcome — was the flagged stress real, was the disease confirmed, how far was the forecast from harvested yield. Failure mode: comparison done once in a consultant's slide deck rather than continuously.</li>
<li><strong>Feed back:</strong> retrain or recalibrate thresholds and models on the accumulated outcomes, and re-run the historical golden set to confirm the change improved rather than shifted the errors. Failure mode: retraining without a held-out season, which produces a model that memorises last year.</li>
</ul>
<p>Programmes that close this loop see alert precision and forecast error improve measurably season over season. Those that do not plateau after the first season, because the model keeps making the same mistakes at the same scale.</p>"""),

 ("what-does-ai-crop-monitoring-cost-per-hectare",
  "What Does AI Crop Monitoring Cost per Hectare?",
  """<p>Cost has three components, and the middle one is where budgets usually break. Data acquisition covers satellite subscriptions, drone flights, sensor hardware, and connectivity; on broadacre row crops this is typically the smallest line item per hectare, while on high-value horticulture the drone and sensor share rises sharply. Integration and analytics covers ingesting the sources into a common model, building the agronomic logic, and maintaining it — this is where most of the real spend sits, and it is largely fixed rather than per-hectare, which is why small pilots look disproportionately expensive.</p>
<p>Adoption cost is the one nobody budgets: the agronomist and grower time spent reviewing alerts, scouting flagged fields, and recording outcomes. If the system generates alerts faster than the team can validate them, you are paying twice — once for the alert and once for the credibility lost when it goes unacted.</p>
<p>The return side is easier to size: reduced crop loss from earlier pest and disease detection, input savings from variable-rate nitrogen and irrigation, yield uplift from interventions made inside the treatment window, and water savings that matter both financially and for licence to operate. A practical way to start is to value one avoided loss event on one high-value block; most programmes find that a single well-timed intervention covers a season of monitoring on several hundred hectares.</p>"""),
]

EN_FAQ = [
 ("What is AI crop monitoring?",
  "AI crop monitoring combines satellite imagery, drone and soil-sensor data, weather feeds, and agronomic models to detect crop stress, disease, and yield variation at field or zone level, then turns those signals into a recommended action. The difference from conventional monitoring is speed and specificity: instead of a map that requires interpretation, a well-built system tells the agronomist which field is stressed, where within the field, why, and what to do within a defined window."),
 ("How early can AI detect crop disease or pest pressure?",
  "Detection lead time depends on the sensing layer and the crop. Satellite vegetation indices typically show a stress signal days to two weeks before it is visible to the naked eye from the ground, and models trained on historical outbreaks can flag risk before symptoms appear when weather conditions favour infection. Confirmation still requires scouting — the system's job is to tell the agronomist exactly where to look, so scouting effort is concentrated instead of spread."),
 ("Does AI crop monitoring work without drones or in-field sensors?",
  "Yes. Satellite imagery plus weather data plus the farm management system is enough to answer the highest-value weekly questions — which fields are stressed, how the season compares, what the yield forecast is. Drones and soil probes add resolution and causal detail, and are best added later, triggered by a satellite anomaly, rather than purchased before the basic layer is producing trusted answers."),
 ("How do you measure ROI on a crop-monitoring programme?",
  "Track three tiers. Agronomic metrics: time from stress onset to detection, alert precision and recall, and yield-forecast error at defined points in the season. Operational metrics: share of fields monitored weekly and share of alerts acted on inside the recommended window. Financial metrics: input cost saved per hectare, crop loss avoided, yield uplift, and water saved. The financial numbers only become credible once the ground-truth loop records what actually happened."),
 ("How long does it take to deploy an AI crop-monitoring system?",
  "A first deployment built on data the operation already collects typically takes one to three months: two to four weeks to connect satellite, weather, sensor, and farm-management sources, three to six weeks to build the agronomic logic and tune alert thresholds with the agronomists who will receive them, and the remainder to validate against scouting results before scaling. Adding new sensing hardware after that is a separate, smaller project."),
]

EN_RENAMES = {
 "understanding-the-current-landscape": "What Does the Current Crop-Monitoring Landscape Look Like?",
 "key-principles-and-strategic-framework": "Which Principles Should Guide a Crop-Monitoring Programme?",
 "implementation-approach-and-best-practices": "What Implementation Approach and Best Practices Work?",
 "measuring-success-and-demonstrating-roi": "How Do You Measure Success and Demonstrate ROI?",
 "common-pitfalls-and-how-to-avoid-them": "What Are the Common Pitfalls and How Do You Avoid Them?",
 "key-takeaways": "What Are the Key Takeaways?",
 "conclusion": "What Should Growers and Agronomists Conclude?",
}

EN = {"renames": EN_RENAMES, "sections": EN_SECTIONS, "faq": EN_FAQ,
      "excerpts": [
        "Building inclusive AI and data teams: what the evidence says actually changes outcomes.",
        "Why your data strategy needs a dedicated AI agent layer in 2026.",
        "Vector databases for enterprise search: a practical 2026 guide."]}

# ---------------------------------------------------------------- zh-CN
ZHCN_SECTIONS = [
 ("哪些数据源对作物监控最重要",
  "哪些数据源对作物监控最为重要？",
  """<p>每一种感知层回答的是不同的问题，采购顺序错了是农业AI项目中最常见的浪费。卫星影像是基础：它覆盖经营的每一块地，按可预期的周期回访，并能给出全园区可比的植被指数。它的局限在于分辨率与云层——卫星过境只能告诉你某个区域受到了胁迫，无法定位到具体植株。</p>
<p>无人机回答的是"让我看清楚"这一类问题。厘米级的多光谱飞行能把卫星发现的异常转化为可实地核查的目标；当水分胁迫与病害胁迫在植被指数上表现完全一致时，热成像可以把两者区分开。代价是每公顷成本与飞手调度，因此无人机是卫星触发后的定点工具，而不是监控层。</p>
<p>土壤水分与气象站提供的是因果的另一半。植被指数能告诉你某块地长势不佳，而土壤水分、蒸散量和局地降雨能告诉你原因。田间探头单点成本高，应布设在代表性区域、由模型插值推算，而不必逐块布点。最后，农场管理系统——播种日期、品种、投入品记录、历史产量——是让这一切可被解读的前提：没有品种和生育期作为参照，指数只是一个孤立数字。</p>"""),

 ("AI产量预测有多准，什么时候才可靠",
  "AI产量预测有多准确，什么时候才可靠？",
  """<p>产量预测准确率是一条曲线，而不是一个数字，采购方真正应该问的是曲线的形状。季前和冠层闭合之前，预测主要由播种日期、品种和天气情景决定，误差带较宽，通常在正负15%到25%之间。这一阶段的价值不在于精确，而在于规划——提前拿到方向性判断，就能改善投入品采购、仓储能力和合同安排。</p>
<p>冠层闭合之后，准确率会快速收窄，因为卫星与无人机指数开始测量实际生物量而非潜在产能。季中估计通常能收敛到实测产量的正负8%到12%，这也正是预测具备操作决策意义的时点：灌溉与氮肥决策此时仍来得及改变结果。收获前最后几周，在历史数据充分的作物上，校准良好的模型通常能落在正负3%到6%以内，足以支撑物流、营销与预售决策。</p>
<p>有两点比头条数字更重要。其一，准确率是本地化的：用自家地块、品种和土壤校准的模型始终优于区域模型，这也是必须建立地面真值闭环的原因。其二，准确率取决于天气是否按假设实现——每一个预测都是"当前长势估计 + 天气假设"，诚实的系统会公开这个假设，而不是只给一个数字。</p>"""),

 ("如何建立提升准确率的地面真值闭环",
  "如何建立提升准确率的地面真值闭环？",
  """<p>作物监控系统只有在田间实际发生的情况被记录下来、且能被模型消费时，才会进化成学习系统。这个道理很浅显，却几乎普遍做得很糟——因为巡查记录散落在笔记本、即时通讯软件和PDF报告里，没有任何数据管线能读取。闭环有四个步骤，每一步都有典型的失败模式。</p>
<ul>
<li><strong>采集：</strong>按地块或管理区记录巡查发现、病虫害确认、施药作业与最终收获产量。失败模式：只有自由文本、没有地块标识，无法与任何数据关联。</li>
<li><strong>结构化：</strong>以稳定的地块ID和时间戳存储，并注明单位与测量方法。失败模式：不同区域的产量单位不统一。</li>
<li><strong>比对：</strong>自动把每一次预警和预测与实际结果核对——预警的胁迫是否真实存在、病害是否被确认、预测与实收产量相差多少。失败模式：只在顾问的汇报材料里比对一次，而不是持续进行。</li>
<li><strong>反馈：</strong>用累积的结果数据重新训练或校准阈值与模型，并在历史黄金集上回归验证，确认改动是减少了误差而不是转移了误差。失败模式：用全部数据重训、没有留出独立季节，结果模型只是在背下去年的答案。</li>
</ul>
<p>把闭环做起来的项目，预警准确率和预测误差会随季节推移持续改善；做不起来的项目，往往在第一季之后就停滞——因为模型会持续以同样的规模犯同样的错误。</p>"""),

 ("AI作物监控每公顷成本是多少",
  "AI作物监控的每公顷成本是多少？",
  """<p>成本由三部分构成，预算通常是在中间那部分失控的。数据采集包括卫星订阅、无人机飞行、传感器硬件与通信；在大田作物上这通常是每公顷最小的一笔，而在高价值园艺作物上，无人机与传感器的占比会显著上升。集成与分析包括把各数据源纳入统一模型、构建农艺逻辑并持续维护——真正的花费大多在这里，而且基本是固定成本而非按公顷计，这也是为什么小范围试点看起来格外昂贵。</p>
<p>采纳成本是几乎没有人做预算的一项：农艺师与种植者花在查看预警、核查标记地块、记录结果上的时间。如果系统产生预警的速度超过团队能核实的速度，你就是在付两次钱——一次为预警买单，一次为预警被忽视而损失的公信力买单。</p>
<p>收益侧更容易量化：更早发现病虫害带来的减产损失减少、变量施肥与灌溉带来的投入品节约、在处理窗口内实施干预带来的产量提升，以及既关乎财务也关乎取水合规的水分节约。一个实用的起步算法是：先估算某块高价值地块上避免一次损失事件的价值——多数项目会发现，一次及时干预的收益就能覆盖数百公顷一整季的监控成本。</p>"""),
]

ZHCN_FAQ = [
 ("什么是AI作物监控？",
  "AI作物监控把卫星影像、无人机与土壤传感器数据、气象数据和农艺模型结合起来，在地块或管理区层面识别作物胁迫、病害与产量差异，并把这些信号转化为可执行建议。它与传统监控的区别在于速度和精度：传统方式产出的是需要专家解读的地图，而一套成熟的系统会直接告诉农艺师哪块地受到了胁迫、在地块的具体什么位置、原因是什么，以及在什么时间窗口内应该采取什么措施。"),
 ("AI能提前多久发现作物病害或虫害压力？",
  "提前量取决于感知层与作物类型。卫星植被指数通常能比地面肉眼观测提前数天到两周发现胁迫信号；而在气象条件有利于发病时，基于历史暴发数据训练的模型甚至能在症状出现之前提示风险。但最终确认仍需要实地巡查——系统的作用是告诉农艺师该去哪里看，把有限的巡查力量集中起来，而不是平均铺开。"),
 ("没有无人机和田间传感器，AI作物监控还能用吗？",
  "可以。卫星影像加上气象数据再加农场管理系统，已经足以回答最高频的每周问题：哪些地块受到了胁迫、本季与往年相比如何、产量预测是多少。无人机与土壤探头能增加分辨率和因果细节，但更好的做法是后置——由卫星发现异常后再触发定点飞行，而不是在基础层还没有产出可信答案之前就先采购硬件。"),
 ("如何衡量作物监控项目的投资回报？",
  "分三层跟踪。农艺指标：从胁迫发生到被识别的时间、预警的准确率与召回率、季内关键时点的产量预测误差。运营指标：每周被覆盖的地块比例、在建议窗口内被处理的预警比例。财务指标：每公顷节约的投入品成本、避免的产量损失、产量提升与节水效益。只有当地面真值闭环把实际发生的情况记录下来之后，财务数字才具备可信度。"),
 ("部署一套AI作物监控系统需要多长时间？",
  "基于农场已有的数据做首次部署通常需要一到三个月：两到四周接入卫星、气象、传感器与农场管理系统的数据源，三到六周构建农艺逻辑并与将接收预警的农艺师一起调校阈值，其余时间用于在扩大规模之前用巡查结果验证。此后再增加新的感知硬件，是一个独立的、更小的项目。"),
]

ZHCN_RENAMES = {
 "理解当前格局": "当前的作物监控格局是怎样的？",
 "关键原则与战略框架": "哪些原则应该指导作物监控项目？",
 "实施方法与最佳实践": "什么样的实施方法与最佳实践有效？",
 "衡量成功与展示投资回报率": "如何衡量成功并展示投资回报？",
 "常见陷阱及规避方法": "常见的陷阱有哪些，如何规避？",
 "关键要点": "有哪些关键要点？",
 "结论": "种植者与农艺师可以得出什么结论？",
}

ZHCN = {"renames": ZHCN_RENAMES, "sections": ZHCN_SECTIONS, "faq": ZHCN_FAQ,
        "excerpts": [
          "生成式AI在企业搜索中的应用：从检索到可信答案。",
          "AI驱动的数据可视化：让洞察真正被看见。",
          "数据质量自动化：从被动响应走向主动治理。"]}

# ---------------------------------------------------------------- zh-TW (converted)
import _gb001_s2t as T

ZHTW_RENAMES = {k: T.s2tw(v) for k, v in ZHCN_RENAMES.items()}
ZHTW = T.spec_s2tw(ZHCN)
ZHTW["renames"] = ZHTW_RENAMES

if __name__ == "__main__":
    for lang, spec in (("en", EN), ("zh-CN", ZHCN), ("zh-TW", ZHTW)):
        b, a, n = apply(SLUG, lang, spec)
        print(f"{SLUG} {lang}: {b} -> {a}  [{', '.join(n)}]")
