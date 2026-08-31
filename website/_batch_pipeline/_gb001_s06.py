#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb001_apply import apply

SLUG = "agriculture-precision-farming-with-satellite-and-sensor-data-a-2026-update"

# ------------------------------------------------------------------ EN
EN_SECTIONS = [
 ("what-changed-between-2025-and-2026-in-precision-farming",
  "What Changed Between 2025 and 2026 in Precision Farming?",
  """<p>Four things moved in the year to 2026, and together they changed what a good programme looks like. First, imagery became abundant rather than scarce. With several public and commercial constellations in operation, most broadacre operations now receive usable observations every two to five days, and the commercial price per hectare for high-resolution tasking has fallen to a fraction of earlier levels. The practical consequence is that acquisition stopped being the constraint and interpretation became it — the bottleneck moved from data to the agronomist's attention.</p>
<p>Second, in-field sensing crossed an affordability threshold. Soil-moisture, weather, and nutrient sensors are now cheap enough to instrument representative zones across an entire operation rather than a demonstration block, which is what makes causal explanations possible at scale instead of on a handful of showcase fields.</p>
<p>Third, delivery channels consolidated. Mobile and chat-based delivery — WeChat Work, DingTalk, WhatsApp, Microsoft Teams — became the default expectation rather than a nice-to-have, and programmes still relying on dashboards found their analytics unused regardless of accuracy.</p>
<p>Fourth, buyers started asking for evidence instead of demonstrations. Requests for proposals increasingly ask for last season's verified alert precision and forecast error on comparable fields. That single shift favours operations that built the ground-truth loop early, because a season of recorded outcomes cannot be bought retroactively.</p>"""),

 ("how-do-you-build-a-semantic-layer-for-an-agribusiness",
  "How Do You Build a Semantic Layer for an Agribusiness?",
  """<p>In agribusiness, a semantic layer is the shared, governed definition of the terms every system uses: what counts as a field, when a season starts, how yield is normalised to a standard moisture content, which crop stage names are canonical, and whose ownership record is authoritative. Without it, the same block appears under different names, areas, and owners in the satellite platform, the ERP, and the agronomist's mobile app, and every cross-system number becomes an argument.</p>
<p>Building one is unglamorous and high-leverage. Start with the identifiers: a canonical field registry with stable IDs, geometry, area, and owner, reconciled against every source system, plus a season calendar that every downstream model references. Then define the metrics — yield, water applied, nitrogen applied, crop health index — once, with units, calculation method, and an owner accountable for the definition. Finally, enforce it: ingestion pipelines should reject records that do not conform, and analytics should read from the governed layer rather than from source systems directly.</p>
<p>The payoff shows up in disputes that stop happening. When the definition of yield flows unchanged from satellite analytics to the ERP to the field team's alert, decisions become comparable across regions and seasons, and the conversation moves from reconciling numbers to acting on them.</p>"""),

 ("how-do-you-model-return-per-hectare-before-rollout",
  "How Do You Model Return per Hectare Before Rollout?",
  """<p>Return per hectare is brutally specific to crop, region, and season, which is why a generic business case fails in a board review. The model has four inputs on the benefit side and three on the cost side, and it should be built per crop-and-region combination rather than once for the whole estate.</p>
<p>Benefits: input savings valued at delivered prices (water and the energy to move it, nitrogen, crop protection), yield effect valued as gross margin on the incremental tonnes at the price actually received, avoided loss estimated from historical loss rates on comparable blocks, and — often forgotten — the value of better-timed marketing and logistics decisions enabled by in-season forecasts.</p>
<p>Costs: data acquisition per hectare (imagery, sensors, connectivity), the largely fixed cost of integration and analytics amortised across the hectare base, and the adoption cost of agronomist and field-team time spent reviewing and acting on recommendations. That third line is the one programmes omit, and it is why pilots with free expert attention look profitable and then disappoint at scale.</p>
<p>Model it for a conservative, a base, and an optimistic season, and state which variables drive the spread — usually weather realisation and adoption rate rather than model accuracy. A programme that can show what it earns in a bad season is far easier to defend than one that only works on a good year.</p>"""),

 ("how-should-apac-operations-handle-smallholder-networks",
  "How Should Asia-Pacific Operations Handle Smallholder and Contract-Farming Networks?",
  """<p>Asia-Pacific agriculture rarely has the single-owner, single-boundary structure that most precision farming software assumes. Large corporate plantations sit alongside dense networks of smallholders and contract farmers, and one platform often has to serve agronomists, extension officers, and field teams with very different levels of technical comfort. Designing for that heterogeneity is the difference between a system that scales and a system that works only on the estate's own blocks.</p>
<p>Three design principles follow. First, make the smallest viable unit explicit and flexible: a "field" may be a plantation block, a contracted plot, or a cluster of plots managed together, and the platform needs to handle all three with comparable analytics. Second, mediate through the people who already have trust — extension officers and field agents should receive aggregated, prioritised work lists rather than raw analytics, and their confirmation should feed the ground-truth record. Third, design for intermittent connectivity and low-end devices: offline-capable mobile delivery, compressed imagery, and plain-language recommendations matter more than analytical sophistication in the last mile.</p>
<p>The organisations that get this right treat the human workflow as part of the design. Analytics is only as good as the decision it changes, and in a contract-farming network that decision is made by an extension officer on a phone, not by an analyst at a desktop.</p>"""),
]

EN_FAQ = [
 ("What is new in precision farming for 2026?",
  "Imagery became abundant rather than scarce, with usable observations every two to five days on most broadacre operations; in-field sensing crossed an affordability threshold so representative zones can be instrumented across a whole operation; delivery consolidated onto mobile and chat channels that field teams actually use; and buyers began demanding verified alert precision and forecast error from the previous season instead of accepting demonstrations."),
 ("Why do precision farming pilots fail to scale?",
  "Mostly for economic and organisational reasons rather than agronomic ones. A pilot works in one field with a dedicated agronomist and hand-built data plumbing; at thousands of hectares the supporting systems — integration, alerting, training, support — do not scale at the same pace and adoption collapses under manual work. Fragmented data silos and unearned trust compound it: a recommendation that risks a season's output must show its reasoning and allow human override."),
 ("What is a semantic layer in agribusiness analytics?",
  "It is the shared, governed definition of the terms every system uses: what counts as a field, when a season starts, how yield is normalised, which crop-stage names are canonical, and whose ownership record is authoritative. Establishing one eliminates the situation where the same block appears under different names and areas in the satellite platform, the ERP, and the field app, and it makes decisions comparable across regions and seasons."),
 ("How do you calculate return per hectare for precision farming?",
  "Build it per crop and region. Benefits are input savings at delivered prices, gross margin on incremental yield, avoided loss estimated from historical rates on comparable blocks, and the value of better-timed marketing and logistics. Costs are data acquisition per hectare, the fixed cost of integration and analytics amortised across the hectare base, and the adoption cost of agronomist and field-team time — the line most business cases omit."),
 ("How should large estates work with smallholders and contract farmers?",
  "Design for heterogeneity. Let the smallest unit be a plantation block, a contracted plot, or a managed cluster, with comparable analytics for each. Route prioritised work lists through extension officers and field agents who already hold the growers' trust, and let their confirmations feed the ground-truth record. Finally, design for intermittent connectivity and low-end devices, because the last-mile decision is made on a phone, not a desktop."),
]

EN_RENAMES = {
 "the-current-landscape": "What Does the Precision Farming Landscape Look Like in 2026?",
 "key-implementation-challenges": "What Are the Key Implementation Challenges?",
 "practical-approaches-that-work": "Which Practical Approaches Actually Work at Scale?",
 "key-takeaways": "What Are the Key Takeaways for 2026?",
 "conclusion": "What Should Agribusiness Leaders Conclude?",
}

EN = {"renames": EN_RENAMES, "sections": EN_SECTIONS, "faq": EN_FAQ,
      "excerpts": [
        "Building inclusive AI and data teams: what the evidence says actually changes outcomes.",
        "Why your data strategy needs a dedicated AI agent layer in 2026.",
        "Vector databases for enterprise search: a practical 2026 guide."]}

# ------------------------------------------------------------------ zh-CN
ZHCN_LEAD = ("精准农业已经不再属于早期采用者的技术试验；到2026年，它是一项董事会级别的运营战略。把卫星影像、田间传感器与AI驱动的分析结合起来，正在亚太地区交付可衡量的收益。我们与该地区农业企业的合作表明，真正的赢家是那些把数据当作农场核心资产、而不是附加项目来经营的主体。本文更新了2026年的市场与技术格局，剖析实施过程中的真实障碍，解释为什么试点难以规模化，并给出在亚太复杂经营环境下能够落地的做法。")

ZHCN_REPLACE = {
 "理解当前格局": (
  "2026年精准农业的格局是怎样的？",
  """<p>底层压力已有充分记录。联合国粮农组织的预测显示，到2050年全球粮食产量需提升约70%，才能养活预计达到97亿的人口，而耕地与淡水供给持续收紧。作为回应，精准农业市场快速增长：行业估计其规模在2024年约为105亿美元，到2030年将超过230亿美元，年复合增长率约14%。</p>
<p>技术栈在2025到2026年间走向成熟。卫星星座如今提供优于10米分辨率、回访周期以天计的影像，商业高分辨率影像的每公顷成本已降到很低的水平，而土壤水分、气象与农机传感器的价格也大幅下降。在亚太地区，大型种植园与订单农业网络正在把这些数据源与ERP及产量数据结合起来，过去凭经验工作的农艺师，如今依靠地图、地块分区与异常预警工作。</p>
<p>区域特性对执行至关重要。亚太农业把大型公司化种植园与密集的小农户、订单农户网络混合在一起，因此同一套平台往往需要同时服务农艺师、推广员和现场团队，而他们的技术舒适度差异极大。这正是我们看到的最成功的项目都把人的工作流纳入设计的原因：分析的价值等于它改变了多少决策，而决策的质量取决于在田间执行它的那个人。</p>"""),

 "关键原则与战略框架": (
  "哪些关键原则应该指导2026年的项目？",
  """<p>第一条原则是把数据当作核心资产来经营，而不是一次性采购。土壤图、品种试验与历史产量值得投入多年；其他数据流则可以按季租用或购买。把数据质量视为有可衡量回报的经常性运营成本、而不是一次性的清洗项目的团队，最终会胜出。</p>
<p>第二条原则是先建立语义层。农业术语与指标应当只定义一次并在各处共享——什么算一块地、季从何时开始、产量如何折算到标准含水率、谁的权属记录是权威的。当同一个产量定义从卫星分析贯通到ERP再到现场团队的移动端预警时，争论就会消失，跨区域、跨季节的决策也就具备了可比性。</p>
<p>第三条原则是为田间而非为办公室设计。预警与建议应当用朴素的语言送达现场管理者，附上置信水平，并允许对建议提出质疑，让人始终是最终决策者。第四条原则是从第一天就做监控与可观测性，在传感器漂移和模型退化损害信任之前就发现它们。</p>"""),

 "实施方法与最佳实践": (
  "什么样的实施方法能在规模化时真正有效？",
  """<p>从单一作物与单一高价值决策起步——灌溉排程、病虫害预警或收获时机。在试点前测量基准线，然后量化产量、投入成本或用水量的变化。这种聚焦的做法能在一个季度内证明价值，创造扩大推广所需的内部证据，同时在假设需要调整时把风险控制在可接受范围。</p>
<ul>
<li><strong>建立语义层：</strong>让农业术语与指标只定义一次并在各处共享，消除跨系统的口径之争。</li>
<li><strong>为田间设计：</strong>用朴素语言、带置信水平地送达建议，并保留人工覆盖的通道。</li>
<li><strong>从第一天起做监控：</strong>传感器漂移与模型退化要在损害信任之前被发现。</li>
<li><strong>像管理资产组合一样规划数据路线图：</strong>有些数据值得多年投入，有些应按季租用。</li>
<li><strong>对分析供应商施加同样的纪律：</strong>明确的服务水平、文档化的定义，以及质疑数字的能力。</li>
</ul>
<p>这套方法也正是我们在农业企业客户中实践的方式：受治理的数据、一致的定义，以及在人们实际工作的地方交付分析——无论是企业微信、钉钉、WhatsApp还是Microsoft Teams。</p>"""),

 "衡量成功与展示投资回报率": (
  "如何在推广前建模每公顷回报？",
  """<p>每公顷回报高度依赖于作物、区域与季节，这正是通用商业论证在董事会评审中失败的原因。模型应当按"作物×区域"组合分别建立，而不是为整个经营主体只做一次。</p>
<p>收益侧有四项：按到岸价格计价的投入品节约（水及输水能耗、氮肥、植保）；按实际销售价格计算的增产吨数毛利；依据可比地块历史损失率估算的避免损失；以及最常被遗漏的一项——季内预测带来的更好的销售与物流决策价值。</p>
<p>成本侧有三项：每公顷的数据获取成本（影像、传感器、连接）；按公顷基数摊销的集成与分析固定成本；以及农艺师与现场团队审阅并执行建议的采纳成本。第三项正是多数项目会漏掉的一行，也是试点在专家免费投入时看起来盈利、规模化后却令人失望的原因。</p>
<p>按保守、基准与乐观三种季节情形建模，并说明是什么驱动了区间——通常是天气实现情况与采纳率，而不是模型准确率。一个能说明在坏年份赚多少的项目，远比一个只在大年成立的项目更容易被批准。</p>"""),

 "常见陷阱及规避方法": (
  "常见的陷阱有哪些，如何规避？",
  """<p>数据质量是第一道关卡。我们的评估显示，约70%的企业数据在支撑AI负载之前需要大量准备工作，农业数据也不例外：传感器会失效，云层会遮蔽影像，不同区域与供应商的单位不一致，历史记录往往不完整。清洁、受治理的数据是每个下游模型的基础，通常也是项目预算中最大的一笔支出。</p>
<ul>
<li><strong>集成复杂度：</strong>产量、气象、灌溉与财务数据必须在一致的作物、地块与季节标识上关联，且管线要能容忍偏远地区的连接中断。规避方式：先建规范的田间注册表与季节日历，再接入分析。</li>
<li><strong>变革管理缺位：</strong>农艺师与田间团队会信任自己参与校准过的建议，也会忽略自己看不懂的建议。投入充分变革管理的项目，采纳率是只关注技术部署的项目的三倍。</li>
<li><strong>规模化时支撑体系掉队：</strong>试点靠手工搭建的数据管线和专家解读成立，推广到数千公顷时支撑体系跟不上。规避方式：在试点阶段就按规模化设计集成、预警、培训与支持。</li>
<li><strong>信任不可转移：</strong>改变灌溉或施药的建议，本质上是建议农户用一季的产出为模型冒险。系统必须展示推理、引用证据并允许人工覆盖。</li>
</ul>"""),

 "关键要点": (
  "2026年有哪些关键要点？",
  """<ul>
<li>影像已经丰裕化，瓶颈从数据获取转移到农艺师的注意力与解读速度</li>
<li>传感成本下降使代表性区域的规模化布设成为可能，因果解释因此可在全园区实现</li>
<li>先在语义层上统一口径，再谈模型与平台；争论消失之后决策才具备可比性</li>
<li>按作物与区域建模每公顷回报，并把采纳成本纳入，否则试点好看、规模失利</li>
<li>在亚太的订单农业网络中，把人的工作流纳入设计：决策发生在推广员的手机上</li>
</ul>"""),

 "结论": (
  "农业企业领导者可以得出什么结论？",
  """<p>2026年，精准农业的竞争差异已经不在技术本身。影像在商品化，模型在趋同，真正的分水岭在于三件事：谁拥有多年累积的地面真值记录，谁把口径统一到了语义层，以及谁把洞察送达到了真正会采取行动的那个人手中。</p>
<p>对正在规划下一阶段的农业企业，建议按三步推进。先在最清晰的"作物×区域"组合上建立受控的对照试验，把一个季度做成可辩护的商业论证；再把语义层与数据治理作为基础设施投资，因为它决定了后续每一个用例的边际成本；最后按资产组合的思路管理数据与分析供应商，用服务水平与文档化定义替代一次性采购。</p>
<p>那些能在几秒内问出"本周哪几个地块需要优先巡查"并得到有依据、可溯源答案的组织，将在产量、成本与可持续三条线上同时领先。技术已经不再是问题；执行节奏才是。</p>"""),
}

ZHCN_SECTIONS = [
 ("2025到2026年精准农业发生了什么变化",
  "2025到2026年精准农业发生了哪些变化？",
  """<p>到2026年为止的一年里有四件事发生了变化，它们共同改变了"好项目"的定义。第一，影像从稀缺变为丰裕。随着多套公共与商业星座在轨运行，多数大田经营主体现在每两到五天就能获得可用观测，商业高分辨率拍摄的每公顷价格已降至先前水平的很小一部分。实际后果是：获取不再是瓶颈，解读才是——瓶颈从数据转移到了农艺师的注意力。</p>
<p>第二，田间感知跨过了可负担性门槛。土壤水分、气象与养分传感器如今便宜到可以在整个经营主体的代表性区域布设，而不只是样板田，这正是因果解释得以规模化、而不只存在于少数展示地块上的原因。</p>
<p>第三，交付渠道趋于集中。移动端与即时通讯交付——企业微信、钉钉、WhatsApp、Microsoft Teams——已成为默认预期而非加分项，仍然依赖仪表板的项目，无论准确率多高，其分析都无人使用。</p>
<p>第四，采购方开始要求证据而非演示。招标文件中越来越频繁地出现"上一季在可比地块上的实测预警准确率与预测误差"这类要求。这一转变有利于早早建立地面真值闭环的经营主体，因为一整季的结果记录无法事后购买。</p>"""),

 ("如何为农业企业建立语义层",
  "如何为农业企业建立语义层？",
  """<p>在农业企业中，语义层是各系统共同使用的术语的受治理定义：什么算一块地、季从何时开始、产量如何折算到标准含水率、哪些生育期名称是规范名称、谁的权属记录是权威的。没有它，同一个地块会在卫星平台、ERP和农艺师的移动应用中以不同的名称、面积和权属出现，于是每一个跨系统的数字都会变成一场争论。</p>
<p>建立语义层的工作并不光鲜，但杠杆极高。先从标识入手：建立规范的田间注册表，包含稳定的ID、几何边界、面积与权属人，并与各源系统核对，再配一份所有下游模型都会引用的季节日历。然后定义指标——产量、用水量、施氮量、作物健康指数——每个都只定义一次，注明单位、计算方法与对该定义负责的负责人。最后强制执行：接入管线应拒绝不合规的记录，分析应从受治理层读取，而不是直接读源系统。</p>
<p>回报体现在那些不再发生的争论上。当同一个产量定义从卫星分析贯通到ERP再到现场团队的预警时，跨区域、跨季节的决策就具备了可比性，讨论也会从核对数字转向采取行动。</p>"""),

 ("亚太业务应如何对待小农户与订单农业网络",
  "亚太业务应如何对待小农户与订单农业网络？",
  """<p>亚太农业很少具备多数精准农业软件所假设的"单一权属人、单一边界"结构。大型公司化种植园与密集的小农户、订单农户网络并存，同一套平台往往需要同时服务农艺师、推广员和现场团队，而他们的技术舒适度差异极大。为这种异质性做设计，正是系统能否规模化、还是只能在集团自有地块上运转的分水岭。</p>
<p>三条设计原则随之而来。第一，让最小管理单元明确且灵活：一个"地块"可以是种植园分区、一块订单田，或一组被统一管理的小块地，平台需要对三者提供可比的分析能力。第二，通过已经建立信任的人来传递：推广员与田间代理人应当收到经过聚合与排序的作业清单，而不是原始分析；他们的确认应当回流进地面真值记录。第三，为断断续续的连接与低端设备做设计：支持离线的移动端交付、压缩影像、朴素语言的建议，在最后一公里比分析的精密程度更重要。</p>
<p>把这些做对的组织，都把人的工作流当作设计的一部分。分析的价值等于它改变了多少决策，而在订单农业网络中，那个决策是推广员在手机上做出的，而不是分析师在电脑前做出的。</p>"""),
]

ZHCN_FAQ = [
 ("2026年精准农业有哪些新的变化？",
  "影像从稀缺变为丰裕，多数大田经营主体现在每两到五天就能获得可用观测；田间传感跨过了可负担性门槛，使代表性区域可在整个经营主体上布设；交付渠道集中到现场团队真正使用的移动端与即时通讯工具；采购方开始要求上一季经核实的预警准确率与预测误差，而不再接受演示。"),
 ("为什么精准农业试点难以规模化？",
  "主要是经济与组织原因，而非农艺原因。试点在一块地上靠专职农艺师和手工搭建的数据管线成立；推广到数千公顷时，集成、预警、培训与支持这些支撑体系跟不上同一节奏，采纳率在手工工作量之下崩塌。数据孤岛与尚未建立的信任会进一步加剧问题——一条可能让一季产出冒险的建议，必须展示推理过程并允许人工覆盖。"),
 ("农业企业分析中的语义层是什么？",
  "它是各系统共同使用的术语的受治理定义：什么算一块地、季从何时开始、产量如何折算、哪些生育期名称是规范名称、谁的权属记录是权威的。建立语义层可以消除同一个地块在卫星平台、ERP与现场应用中以不同名称和面积出现的状况，并使跨区域、跨季节的决策具备可比性。"),
 ("如何计算精准农业的每公顷回报？",
  "按作物与区域分别建模。收益侧包括按到岸价格计价的投入品节约、按实际售价计算的增产毛利、依据可比地块历史损失率估算的避免损失，以及常被遗漏的季内预测带来的销售与物流价值。成本侧包括每公顷数据获取成本、按公顷摊销的集成与分析固定成本，以及农艺师与现场团队审阅执行建议的采纳成本——多数商业论证漏掉的正是这一行。"),
 ("大型种植园应如何与小农户和订单农户协作？",
  "为异质性做设计。让最小单元可以是种植园分区、单块订单田或统一管理的小块地组，并对三者提供可比的分析能力。把排序后的作业清单通过已经赢得农户信任的推广员与田间代理人传递，并让他们的确认回流进地面真值记录。最后为断断续续的连接与低端设备做设计，因为最后一公里的决策是在手机上做出的。"),
]

ZHCN_RENAMES = {}

ZHCN = {"lead": ZHCN_LEAD, "replace": ZHCN_REPLACE, "renames": ZHCN_RENAMES,
        "sections": ZHCN_SECTIONS, "faq": ZHCN_FAQ,
        "excerpts": [
          "生成式AI在企业搜索中的应用：从检索到可信答案。",
          "用AI驱动的数据可视化，让洞察真正被看见。",
          "数据质量自动化：从被动响应走向主动治理。"]}

# ------------------------------------------------------------------ zh-TW (converted)
import _gb001_s2t as T
ZHTW = T.spec_s2tw(ZHCN)

if __name__ == "__main__":
    for lang, spec in (("en", EN), ("zh-CN", ZHCN), ("zh-TW", ZHTW)):
        b, a, n = apply(SLUG, lang, spec)
        print(f"{SLUG} {lang}: {b} -> {a}  [{', '.join(n)}]")
