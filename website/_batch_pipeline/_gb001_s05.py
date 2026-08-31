#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb001_apply import apply

SLUG = "agriculture-precision-farming-with-satellite-and-sensor-data"

# ------------------------------------------------------------------ EN
EN_SECTIONS = [
 ("which-data-layers-matter-most-in-precision-farming",
  "Which Data Layers Matter Most in Precision Farming?",
  """<p>Four data layers make up a working precision farming stack, and each answers a different question. Satellite imagery is the coverage layer: it sees every field you operate on a predictable cadence and produces comparable vegetation indices across the whole estate. Its job is to tell you <em>where</em> something is happening. In-field sensing — soil moisture probes, weather stations, nutrient sensors — is the causal layer: it tells you <em>why</em>. Machinery telemetry and application records are the execution layer: they tell you <em>what was actually done</em>, which is the only way to attribute an outcome to an action. And the farm management system — field boundaries, varieties, planting dates, historical yield — is the context layer that makes the other three interpretable.</p>
<p>The failure mode is buying them in the wrong order. Operations that start with the highest-resolution imagery and the densest sensor network usually end up with expensive data and no decisions, because there is no context layer to interpret it against and no execution layer to close the loop. The sequence that works is context first, coverage second, causation third, execution telemetry throughout.</p>
<p>Resolution and cadence are also worth choosing deliberately rather than maximising. Ten-metre imagery every five days is sufficient for most broadacre decisions and costs a fraction of sub-metre daily tasking; sub-metre imagery earns its price when you need field boundaries, irrigation layout, or damage assessment, not as a default.</p>"""),

 ("how-do-you-build-management-zones-that-hold-up",
  "How Do You Build Management Zones That Actually Hold Up?",
  """<p>Management zones are the unit of decision in precision farming, and most of the disappointment in the field traces back to zones that were built badly. A zone is a sub-field area that behaves consistently enough to justify a different treatment — a different seeding rate, a different nitrogen prescription, a different irrigation schedule. The mistake is deriving zones from a single season's imagery, which captures that season's weather as much as the field's underlying character, so the map changes after every pass and prescriptions lose credibility.</p>
<p>The durable recipe uses three inputs that describe the field rather than the season. Multi-year yield history shows where the field consistently produces and where it consistently struggles. Soil information — electrical conductivity, texture, organic matter, depth — explains the physical basis of that pattern. Topography and drainage explain water movement, which in most fields drives a large share of within-field variability. Combine these, cluster into a small number of zones — three to five is usually right — and validate by checking that the zones actually differ in measured yield across several seasons.</p>
<p>Then treat zones as a slowly-moving asset: revise annually with the newest yield map, not continuously with every new image. Zones that are stable enough to be trusted are the precondition for variable-rate prescriptions; zones that shift every week are worse than a uniform treatment, because they add cost without adding confidence.</p>"""),

 ("how-do-you-keep-satellite-and-sensor-data-trustworthy",
  "How Do You Keep Satellite and Sensor Data Trustworthy Through a Season?",
  """<p>Precision farming advice is only as good as the data underneath it, and both sensing layers degrade in predictable ways. Optical satellite imagery is defeated by cloud: a fortnight of persistent cover at a critical growth stage can leave a programme blind precisely when intervention matters. The mitigation is a second source — radar imagery, which sees through cloud, or a second constellation with different revisit timing — plus a fallback decision rule driven by soil moisture and weather telemetry so irrigation scheduling never waits for a clear sky.</p>
<p>Raw reflectance is not a measurement until it is corrected. Atmospheric conditions, sun angle, and sensor differences all shift values, so indices must be atmospherically corrected and standardised before comparison; an uncorrected index from one date is not comparable with the same index from another. Sensor drift is the ground-side equivalent: soil-moisture probes drift with temperature and salinity, and a probe that is wrong by a few percentage points produces confidently wrong irrigation advice. Scheduled recalibration, plausibility checks against rainfall and evapotranspiration, and alerts on missing data rather than silent gaps are the minimum controls.</p>
<p>Finally, publish confidence with every recommendation. Growers do not need certainty; they need to know when a recommendation is well-evidenced and when it rests on a single cloudy observation. Systems that show their confidence earn more trust than systems that always sound sure.</p>"""),

 ("what-does-a-first-season-precision-farming-deployment-look-like",
  "What Does a First-Season Precision Farming Deployment Look Like?",
  """<p>The first season should be designed to produce evidence, not coverage. Pick one decision loop — irrigation scheduling or nitrogen application — and one representative set of fields; resist the temptation to instrument everything, because the value of the first season is the ground-truth record it creates, and that record is only clean if the comparison is controlled.</p>
<p>Weeks one to four build the foundation: consolidate field boundaries, confirm the management zones against multi-year yield data, connect the satellite and weather subscriptions, and install or validate the in-field sensors on representative zones. Establish the baseline before anything changes — record last season's input volumes, yield, and margin per block, because without a credible "before" the "after" is an argument rather than a result.</p>
<p>From the first growth stage, run the loop weekly: imagery and sensor data are fused into a recommendation, the agronomist confirms or overrides it, the action is executed, and the outcome is recorded. Keep a paired control block managed conventionally. Log every override and its reason — overrides are the most valuable training data the programme will produce, because they encode the agronomist's knowledge that the model lacks.</p>
<p>Close the season with a reconciliation: inputs applied, yield delivered, margin difference against the control, and the accuracy of each alert class. That single document is what turns a first season into a business case for the second.</p>"""),
]

EN_FAQ = [
 ("What is precision farming with satellite and sensor data?",
  "It is the practice of managing fields at sub-field resolution by fusing satellite imagery, in-field sensor readings, weather data, and machinery telemetry into prescriptions rather than blanket treatments. Satellite data shows where variability exists, sensors explain why, and analytics convert the two into a specific action — variable-rate seeding, targeted irrigation, spot nitrogen — with the outcome recorded so the next cycle starts from evidence."),
 ("How much can precision farming reduce input costs?",
  "The consistent results are on inputs rather than yield. Precision irrigation driven by soil moisture and evapotranspiration typically reduces water use by 20–50% against calendar scheduling, and variable-rate nitrogen commonly cuts applied nitrogen by 10–20% while holding yield. Yield effects are real but smaller and more weather-dependent — usually 3–8% where a treatable limitation is caught inside the crop's response window."),
 ("What is the biggest challenge in implementing precision agriculture?",
  "Integration, not technology. A typical operation juggles satellite subscriptions, sensors from several vendors, weather feeds, machinery telemetry, and the farm management system, each with its own formats and cadences. Teams that build a single governed data layer with consistent field boundaries, crop stages, and units avoid the data-wrangling tax that quietly consumes most precision agriculture budgets."),
 ("Why do growers not act on precision farming recommendations?",
  "Because trust is calibrated at the moment of decision and most systems do not earn it. Recommendations arrive without a confidence estimate, without the reasoning, and without a verification path, so a grower who has been wrong once stops acting. Programmes that pair every recommendation with its evidence, its expected outcome, and a way to confirm it in the field keep adoption high."),
 ("How do you start a precision farming programme without a large upfront investment?",
  "Start with one decision loop on a subset of fields rather than a platform. Use imagery you already receive or can access at moderate resolution, place sensors on representative zones instead of everywhere, establish a baseline before changing anything, and keep a conventionally managed control block. A single season with a controlled comparison produces a defensible business case that funds the expansion."),
]

EN_RENAMES = {
 "the-current-landscape": "What Does the Current Precision Farming Landscape Look Like?",
 "key-implementation-challenges": "What Are the Key Implementation Challenges?",
 "practical-approaches-that-work": "Which Practical Approaches Actually Work?",
 "key-takeaways": "What Are the Key Takeaways?",
 "conclusion": "What Should Growers Conclude?",
}

EN = {"renames": EN_RENAMES, "sections": EN_SECTIONS, "faq": EN_FAQ,
      "excerpts": [
        "Why your data strategy needs a dedicated AI agent layer in 2026.",
        "Vector databases for enterprise search: a practical 2026 guide.",
        "How to architect enterprise AI agents: runtime, tools, and memory."]}

# ------------------------------------------------------------------ zh-CN
ZHCN_LEAD = ("精准农业是数据驱动农业从试点走向生产的最有力证据：把卫星影像与地面传感器数据融合起来的种植者，正在取得传统均一化管理无法企及的、可衡量的投入节约与产量增益。联合国粮农组织长期预测，到2050年全球粮食产量需提升约70%才能养活持续增长的人口，而耕地、水资源与劳动力同时在收紧。应对之道正在数据中被构建出来：具备数天级回访能力的卫星星座、廉价的田间传感器，以及把两者转化为决策的分析平台。本文解释这些环节如何协同、精准农业项目通常在何处受阻，以及如何建设一个能收回成本的项目。")

ZHCN_REPLACE = {
 "理解当前格局": (
  "当前的精准农业格局是怎样的？",
  """<p>精准农业的技术栈在过去五年急剧成熟。在遥感侧，欧盟Sentinel-2等卫星计划以约10米分辨率、五天回访周期提供多光谱影像，使通过NDVI等植被指数对作物长势做持续监测成为可能；NDVI即归一化差异植被指数，已成为行业通行的作物活力代理指标。亚米级商业星座补充了地块边界测绘、灌溉布局与灾害评估所需的细节，而无人机飞行则按需补齐最高分辨率的复核。</p>
<p>在地面侧，感知层同样变得触手可及。土壤水分探头、气象站、养分传感器与农机遥测如今持续回传，田间传感器网络的成本相比十年前下降了一个数量级。这些层次的融合，正是现代农业精准化区别于早期仅靠GPS自动导航阶段的关键：卫星数据告诉你整块地哪里出现了胁迫，传感器数据告诉你具体点位上的成因，而分析把两者连接成一份处方——变量播种、定点灌溉、局部施氮——而不是均一化的处理。</p>
<p>经济证据相当扎实。同行评议研究与行业项目一致报告，精准灌溉相比常规排程减少用水20%到50%，变量施肥在保持产量的同时降低投入成本；精准农业整体市场在2023年前后约为100亿美元，预计到2030年代初将超过200亿美元。对于亚太地区从大规模稻麦经营到园艺与种植园的农业经营者而言，问题已经不再是数据是否划算，而是如何在运营规模上可靠地捕获这份价值。</p>"""),

 "关键原则与战略框架": (
  "哪些关键原则应该指导精准农业项目？",
  """<p>成功的精准农业项目建立在四条原则之上。第一条是先分区、后处方：管理区是精准农业的决策单元，必须来自地块本身的稳定特征——多年产量历史、土壤电导率与质地、地形与排水——而不是单季影像。用单季数据切出来的分区，捕捉的其实是那一季的天气，于是每次飞过地图都在变，处方也随之失去公信力。</p>
<p>第二条是卫星看范围、传感器看成因、巡查看真相。这是一个级联关系，三层缺一不可：只有范围没有成因，得到的是没有解释的预警；没有巡查确认，就永远不知道预警到底对不对，也就无法让模型在下一次变得更好。第三条是处方必须可执行：植被指数和土壤水分读数只是观测，不是决策，价值只有在它们驱动了一个人或一台设备去执行的操作时才被实现。</p>
<p>第四条是结果必须被记录。没有地面真值——巡查结果、实际执行记录、收获产量——就没有学习，也没有信任。把结果反哺进模型的项目，其建议会随季节推移持续改善；把模型当成静态产品采购的项目，则会在第一个可见的失误之后失去使用者的信任。</p>"""),

 "实施方法与最佳实践": (
  "什么样的实施方法与最佳实践有效？",
  """<p>从一个决策闭环起步，而不是从一个平台起步。最可靠的切入点是单一的高价值决策——通常是灌溉排程或氮肥施用——在一部分地块上做扎实，并用对照组衡量经济效益。一个聚焦的闭环能在一个生长季内证明价值，产生校准模型所需的地面真值数据，并建立组织向更大范围扩展的能力。一开始就横跨所有作物与区域建设完整平台的做法，几乎总是把预算消耗在数据整理上，而不是决策上。</p>
<ul>
<li><strong>先建上下文层：</strong>统一地块边界、品种、播种日期与历史产量，否则其他数据无法被解读。</li>
<li><strong>先建基准线：</strong>在改变任何做法之前记录上一季的投入量、产量与每块地的毛利，没有可信的"之前"，"之后"就只是争论。</li>
<li><strong>按周运行闭环：</strong>影像与传感器数据融合为建议，农艺师确认或覆盖，执行动作，记录结果。</li>
<li><strong>保留对照地块：</strong>一块按常规方式管理的对照地，是把相关性变成因果性的最廉价手段。</li>
<li><strong>记录每一次覆盖及其原因：</strong>人工覆盖是项目能产出的最有价值训练数据，因为它编码了模型所缺少的农艺师经验。</li>
</ul>
<p>把洞察嵌入工作流，而不是留在仪表板里——预警通过即时通讯工具送达田间农艺师与农场管理者，处方直接导出到变量作业设备，这才是被采用的方式。</p>"""),

 "衡量成功与展示投资回报率": (
  "如何衡量成功并展示投资回报？",
  """<p>最可信的衡量方法是配对比较：选择土壤类型、品种与播种日期相当的两块地，一块按项目方案管理，一块按常规方式管理，比较投入品用量、产量与每公顷毛利的差异。无法设置真实对照时，用同地块的多年基线做前后对比，并明确说明天气差异包含在数字之内。</p>
<p>把结果拆成三行，数字才站得住。投入品节约最易验证：肥料、水、能源与植保用量，按到岸价格计价。产量效应按实收吨数差异的毛利计算，用实际销售价格估值。避免损失需要估算，因此要把假设写清楚——通常采用可比地块在可比季节的历史损失率。</p>
<p>再配套跟踪那些能预测财务结果能否重复的运营指标：每周有可用影像的地块比例、在建议窗口内被执行的预警比例、对照巡查结果衡量的预警准确率，以及季内关键时点的产量预测误差。只跟踪金额的项目，往往要晚一整季才发现采纳率已经崩塌；同时跟踪采纳率的项目，第一个月就能发现问题。</p>"""),

 "常见陷阱及规避方法": (
  "常见的陷阱有哪些，如何规避？",
  """<p>反复出现的陷阱相当一致，值得在启动前就列入检查清单。</p>
<ul>
<li><strong>数据囤积：</strong>不断购买更高分辨率的影像和更多传感器，却没有人处理已经在流动的数据，最终产出的是仪表板而不是决策。规避方式：先让现有数据产出被使用的答案，再增加新的数据源。</li>
<li><strong>预警疲劳：</strong>为追求灵敏度而设置的阈值，在多雨季节会淹没农艺师，响应率随之崩塌。规避方式：与接收预警的人一起调校阈值，按经济后果排序，并限制每块地每周的预警条数。</li>
<li><strong>传感器漂移与失效：</strong>土壤水分探头漂移几个百分点，就会产出自信但错误的灌溉建议。规避方式：定期标定、对照降雨与蒸散量做自动合理性校验，并对数据缺失发出告警而非静默留空。</li>
<li><strong>云层缺口：</strong>关键生育期连续多云会让光学影像数周不可用。规避方式：签约雷达或第二套星座，并以土壤水分与气象遥测作为兜底。</li>
<li><strong>渠道错位：</strong>洞察被锁在农艺师从不打开的报表或专业工具里。规避方式：在田间团队已经在用的渠道交付。</li>
</ul>
<p>共同点是：这些失败首先是组织性的，其次才是技术性的，也因此在设计阶段排除比在季中补救便宜得多。</p>"""),

 "关键要点": (
  "有哪些关键要点？",
  """<ul>
<li>按上下文、覆盖范围、成因、执行四层顺序建设数据栈，而不是先买最高分辨率的影像</li>
<li>管理区必须来自地块本身的稳定特征，三到五个分区通常足够，每年随新产量图修订一次</li>
<li>从一个决策闭环和一组对照地块起步，一个生长季内就能产出可辩护的商业论证</li>
<li>每条建议都要带证据、预期结果与验证路径；展示置信度的系统比永远听起来很确定的系统更被信任</li>
<li>把结果记录下来：没有地面真值，就没有学习，也没有下一季的改善</li>
</ul>"""),

 "结论": (
  "种植者与农业企业可以得出什么结论？",
  """<p>精准农业已经越过了"是否可行"的阶段。影像在快速商品化，传感器在持续降价，真正的差异已经转移到下游：谁能把从发现到行动的路径压得最短，谁能把事后发生的情况记录下来，让下一季从证据而不是直觉出发。</p>
<p>对正在评估精准农业的经营者，建议按三步推进。先诚实评估当前的数据成熟度，明确优势与关键缺口；再制定分阶段路线图，优先高影响、低风险的用例，逐步走向更宏大的部署；最后投资组织能力，因为技术本身并不充分——采纳、人才与治理这些人的因素，最终决定成败。</p>
<p>那些能在几秒内问出"这个周末哪几块地需要巡查"并得到有依据、可溯源答案的经营者，将同时获得农艺、财务与可持续三重优势。技术已经验证；现在的分水岭在于洞察是否抵达了那个真正会采取行动的人。</p>"""),
}

ZHCN_SECTIONS = [
 ("哪些数据层对精准农业最重要",
  "哪些数据层对精准农业最为重要？",
  """<p>一个可运转的精准农业栈由四层数据构成，每层回答不同的问题。卫星影像是覆盖层：它以可预期的周期覆盖经营的每一块地，并产出全园区可比的植被指数，职责是告诉你事情发生在<em>哪里</em>。田间感知——土壤水分探头、气象站、养分传感器——是成因层，负责告诉你<em>为什么</em>。农机遥测与作业记录是执行层，说明<em>实际做了什么</em>，这是把结果与动作关联起来的唯一途径。而农场管理系统——地块边界、品种、播种日期、历史产量——是上下文层，让前三层变得可被解读。</p>
<p>典型的失败模式是采购顺序错了。从最高分辨率影像和最密集传感器网络起步的经营者，通常最终得到昂贵的数据和零决策，因为没有上下文层可供解读，也没有执行层来闭合回路。有效的顺序是：上下文第一，覆盖第二，成因第三，执行遥测贯穿始终。</p>
<p>分辨率与回访周期也应当刻意选择，而不是一味拉满。10米影像、五天回访对多数大田决策已经足够，成本只是亚米级每日拍摄的一小部分；亚米级影像的价值出现在需要地块边界、灌溉布局或灾害评估时，而不是作为默认配置。</p>"""),

 ("如何建立站得住脚的管理区",
  "如何建立真正站得住脚的管理区？",
  """<p>管理区是精准农业的决策单元，田间大多数失望都可以追溯到分区做得不好。分区是地块内行为足够一致、因而值得差异化处理的子区域——不同的播种量、不同的施氮处方、不同的灌溉排程。常见错误是用单季影像推导分区，这样捕捉到的更多是那一季的天气而非地块本身的特性，于是地图每次飞过都在变，处方也随之失去公信力。</p>
<p>耐用的配方使用三个描述地块而非季节的输入。多年产量历史显示地块在哪里持续高产、在哪里持续吃力。土壤信息——电导率、质地、有机质、有效土层深度——解释这种格局的物理成因。地形与排水解释水分运移，而在多数地块中，水分运移驱动了田内变异的很大一部分。把三者结合，聚成少量分区——通常三到五个是合适的——并通过检查各分区在多个季节里实测产量是否确有差异来验证。</p>
<p>然后把分区当作缓慢移动的资产：每年用最新的产量图修订一次，而不是每来一张新影像就重算。稳定到可以被信任的分区，是变量处方的前提；每周都在变的分区，比均一化处理更糟，因为它增加了成本却没有增加信心。</p>"""),

 ("如何让卫星与传感器数据在整个季节保持可信",
  "如何让卫星与传感器数据在整个季节保持可信？",
  """<p>精准农业的建议质量上限取决于底层数据，而两层感知都会以可预测的方式退化。光学卫星影像会被云击败：关键生育期连续两周的云层覆盖，足以让项目在最需要干预的时刻失明。缓解方式是引入第二个数据源——能穿透云层的雷达影像，或回访时点不同的第二套星座——外加一条由土壤水分与气象遥测驱动的兜底决策规则，让灌溉排程永远不必等一个晴天。</p>
<p>原始反射率在被校正之前不构成测量。大气条件、太阳高度角与传感器差异都会改变数值，因此指数必须经过大气校正与标准化才能比较；未校正的某日指数与另一日的同款指数并不可比。传感器漂移是地面侧的对应问题：土壤水分探头会随温度和盐分漂移，偏差几个百分点的探头会产出自信但错误的灌溉建议。最低限度的控制包括定期标定、对照降雨与蒸散量做合理性校验，以及对数据缺失而非静默空值发出告警。</p>
<p>最后，把置信度与每条建议一起呈现。种植者不需要确定性，他们需要知道一条建议是证据充分，还是只建立在一张有云的观测之上。愿意展示置信度的系统，比永远听起来很确定的系统更能赢得信任。</p>"""),

 ("首个生长季的精准农业部署是什么样的",
  "首个生长季的精准农业部署是什么样的？",
  """<p>第一个生长季的设计目标应该是产出证据，而不是覆盖面积。选定一个决策闭环——灌溉排程或氮肥施用——和一组有代表性的地块；抑制把一切都装上设备的冲动，因为第一季的价值在于它创建的地面真值记录，而只有在比较受控的前提下，这份记录才是干净的。</p>
<p>前四周打基础：整理地块边界，用多年产量数据校验管理区，接入卫星与气象订阅，在代表性区域安装或校验田间传感器。在任何做法改变之前建立基准线——记录上一季的投入量、产量与每块地的毛利，因为没有可信的"之前"，"之后"就只是争论而不是结果。</p>
<p>从第一个生育期开始按周运行闭环：影像与传感器数据融合成建议，农艺师确认或覆盖，执行动作，记录结果。保留一块按常规方式管理的对照地。记录每一次覆盖及其原因——覆盖是项目能产出的最有价值训练数据，因为它编码了模型所缺少的农艺师知识。</p>
<p>用一次对账来收尾这一季：实际用量、实收产量、相对对照的毛利差异，以及每一类预警的准确率。这一份文件，就是把第一季转化为第二季商业论证的东西。</p>"""),
]

ZHCN_FAQ = [
 ("什么是基于卫星与传感器数据的精准农业？",
  "它是指在亚地块分辨率上管理农田的做法：把卫星影像、田间传感器读数、气象数据与农机遥测融合成处方，而不是做均一化处理。卫星数据指出变异存在于哪里，传感器解释成因，分析把两者转化为具体动作——变量播种、定点灌溉、局部施氮——并把结果记录下来，让下一个循环从证据出发。"),
 ("精准农业能降低多少投入成本？",
  "成效稳定体现在投入品而非产量上。以土壤水分与蒸散量驱动的精准灌溉，通常比按日历排程减少用水20%到50%；变量施氮通常把施氮量降低10%到20%而产量持平。产量效应真实存在但更小、也更依赖天气——在作物响应窗口内识别出可处理限制因素的地块上通常为3%到8%。"),
 ("实施精准农业最大的挑战是什么？",
  "是集成，而不是技术。一个典型的经营主体要同时应对卫星订阅、来自多个供应商的传感器、气象数据、农机遥测和农场管理系统，各自格式与节奏都不同。从一开始就建立统一受治理的数据层、统一地块边界、生育期定义与单位的团队，就能避开那笔悄悄吃掉大部分精准农业预算的数据整理税。"),
 ("为什么种植者不按精准农业的建议行动？",
  "因为信任是在决策那一刻被校准的，而多数系统没有赢得它。建议到达时没有置信度、没有推理过程、也没有验证路径，于是被误导过一次的种植者就不再行动。把每条建议连同其证据、预期结果与田间验证方式一起呈现的项目，能保持较高的采纳率。"),
 ("如何以较低的先期投入启动精准农业项目？",
  "从一个决策闭环和一部分地块起步，而不是从平台起步。使用你已经能获取的、中等分辨率的影像，只在代表性区域而非处处布设传感器，在改变任何做法之前建立基准线，并保留一块按常规方式管理的对照地。一个设置了对照的单季试验，就能产出支撑后续扩张的可辩护商业论证。"),
]

ZHCN_RENAMES = {}

ZHCN = {"lead": ZHCN_LEAD, "replace": ZHCN_REPLACE, "renames": ZHCN_RENAMES,
        "sections": ZHCN_SECTIONS, "faq": ZHCN_FAQ,
        "excerpts": [
          "用AI驱动的数据可视化，让洞察真正被看见。",
          "数据质量自动化：从被动响应走向主动治理。",
          "CFO指南：AI预算应如何在业务单元之间分配。"]}

# ------------------------------------------------------------------ zh-TW (converted)
import _gb001_s2t as T
ZHTW = T.spec_s2tw(ZHCN)

if __name__ == "__main__":
    for lang, spec in (("en", EN), ("zh-CN", ZHCN), ("zh-TW", ZHTW)):
        b, a, n = apply(SLUG, lang, spec)
        print(f"{SLUG} {lang}: {b} -> {a}  [{', '.join(n)}]")
