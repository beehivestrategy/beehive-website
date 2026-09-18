# -*- coding: utf-8 -*-
# 12 个 undefined 文件的 4 组问答（简体中文）
FAQ = {

"real-estate-ai-market-analysis-2025.html": [
 ("房地产企业引入 AI，最先该在哪些业务环节落地？",
  "建议从估值与客源匹配、租约与合同审查、能耗与设施运维这三类高频且数据基础较好的环节切入。文中数据显示 72% 的企业已有 AI 试点进入生产环境，但仅 23% 跨部门扩展，先跑通单一场景再横向复制更为稳妥。"),
 ("为什么很多房地产 AI 试点停在单个部门推不动？",
  "瓶颈通常不在算法，而在数据口径与治理责任分散。文中提到设有专门职能团队的组织价值实现速度快 2.8 倍，说明把 AI 职责集中到明确的业务负责人、而不是散落在 IT 部门，是跨部门扩展的前提。"),
 ("房地产 AI 项目的投资回报周期该怎么设定预期？",
  "文中给出的行业参照是平均回本期已从 24 个月缩短至 14 个月。但那是成熟实践的均值，首个项目还需预留数据治理与流程改造的时间，不宜按成熟项目的时间表倒排里程碑。"),
 ("在香港与大湾区部署房地产 AI，合规上要优先注意什么？",
  "跨境数据传输与客户个人资料处理是首要门槛。建议在项目设计阶段就引入隐私保护与审计留痕，而不是上线后补救；文中强调提前建立框架的组织，后续合规成本明显低于事后整改的同行。"),
],

"real-time-data-pipelines-mcp-integration.html": [
 ("用 MCP 打通实时数据管道，现有架构要不要推翻重来？",
  "不需要。MCP 的价值在于用统一协议替代逐一点对点对接，企业可在保留既有仓库与流处理链路的前提下增加一层接入标准。改造重点在接口层与权限模型，而不是推翻数据底座重建。"),
 ("实时数据管道接入 MCP 后，性能瓶颈通常出现在哪里？",
  "多在并发查询的调度与权限校验环节，而非数据搬运本身。建议先压测典型的智能体并发读取场景，把限流、缓存与列级权限下沉到接入层，再考虑横向扩容计算资源。"),
 ("MCP 数据管道的权限与审计该怎么设计？",
  "建议把身份认证与权限校验放在 MCP 服务端统一执行，避免每个数据源各自实现一套。同时保留完整查询留痕，记录谁在什么时间、通过哪个智能体读取了哪些字段，以满足后续审计。"),
 ("评估 MCP 集成成效，该跟踪哪些指标？",
  "可看四层：新增数据源的接入耗时、智能体查询的首次返回时延、权限异常拦截率，以及业务侧取数请求的自助解决比例。文中提到企业 AI 平均回本期已从 24 个月降至 14 个月，指标应与回本节奏对齐。"),
],

"retail-back-to-school-ai-forecasting.html": [
 ("返校季需求预测，AI 比传统补货方法强在哪里？",
  "强在对短周期、多 SKU、强促销扰动的响应能力。传统方法依赖历史均值，AI 可纳入天气、校历、社媒热度与竞品定价等外部信号，把预测粒度细化到门店与周次，减少畅销款断货与滞销款积压。"),
 ("返校季窗口很短，预测模型来不及训练怎么办？",
  "建议复用往年同期的品类模型做冷启动，先用少量当期数据微调，再逐周滚动更新。把人工复核保留在促销与主推款上，让买手经验修正模型输出，通常比追求全自动更实际。"),
 ("返校季 AI 预测最常踩的坑是什么？",
  "把预测准确率当成唯一目标。零售商真正需要的是缺货率、周转天数与折扣深度的改善。若门店与电商的数据口径尚未统一，模型再准也无法指导调拨，建议先统一商品与库存主数据。"),
 ("零售商该怎么衡量返校季 AI 预测的价值？",
  "建议锁定三项：畅销款缺货率、季末滞销库存占比，以及被迫深度折扣的 SKU 比例。文中数据显示企业 AI 平均回本期已从 24 个月降至 14 个月，短期促销场景的回收通常更快。"),
],

"retail-q2-prep-conversational-bi-2025.html": [
 ("制定夏季商品策略时，对话式 BI 能替代原有报表吗？",
  "更现实的路径是互补。固定报表继续承担月度经营回顾，对话式 BI 处理临时性问题，例如某区域上周动销异常的原因。把两者分工讲清楚，能减少业务团队对口径不一致的疑虑。"),
 ("让门店与买手团队用起来，最大的阻力是什么？",
  "不是会不会提问，而是对答案不信任。建议先为销售额、毛利率、库存周转等高频指标建立受控定义与责任人，让自然语言查询只调用这些定义，再逐步扩大指标范围。"),
 ("夏季旺季临时改价或调货，对话式 BI 能支撑多快？",
  "取决于数据新鲜度而非对话界面。若库存与销售数据仍是按日批处理，提问再快也只能得到昨天的答案。建议先明确关键数据的更新频率承诺，再谈交互体验的优化。"),
 ("零售企业该从哪些维度验收对话式 BI？",
  "建议看取数等待时间、经营会上口径争议次数、以及非技术岗位自助提问占比三项。文中数据显示 72% 的企业已有 AI 试点进入生产环境，但仅 23% 实现跨部门扩展，采用广度比查询精度更值得关注。"),
],

"scaling-ai-pilots-to-production-2025.html": [
 ("AI 试点成功后，为什么多数企业卡在规模化这一步？",
  "因为规模化引入了新复杂度：更多用例、更多用户、更多数据源与集成点。文中数据显示 72% 的企业已有 AI 试点在生产环境运行，但仅 23% 扩展到单一部门之外，差距主要出在治理与运维而非模型能力。"),
 ("从试点走向规模化，应该先建平台还是先铺用例？",
  "建议平台优先，先沉淀统一的数据接入、权限与监控能力，再逐条扩展用例。文中总结的成功企业遵循四个原则：平台优先、价值驱动、增量扩展、反馈循环，一次扩展一个用例并验证后再继续。"),
 ("怎样判断组织是否具备规模化 AI 的就绪度？",
  "可从三方面自检：关键数据域是否有稳定口径与责任人、是否有能承接持续运维的工程团队、业务侧是否指定了明确的价值负责人。文中提到设有专门职能团队的组织，价值实现速度明显快于职责分散者。"),
 ("规模化阶段该如何衡量投入是否值得？",
  "建议把每个用例绑定到具体业务指标与回本周期，而不是只看模型准确率。文中给出的行业参照是企业 AI 平均回本期已从 24 个月降至 14 个月，可据此设定分阶段验收点。"),
],

"self-service-bi-maturity-model-2025.html": [
 ("怎么判断企业自助式 BI 处在哪个成熟度阶段？",
  "可看三个信号：业务人员能否在没有 IT 介入下完成常规取数、指标口径是否由专人维护、分析结果能否直接触发业务动作。多数企业仍停留在 IT 代取数阶段，真正的分水岭是口径治理而非工具功能。"),
 ("自助分析推不动，通常是工具问题还是治理问题？",
  "大多是治理问题。语义层缺失时，同一个销售额在不同报表有不同算法，业务人员自然会回到人工取数。建议先建指标目录与语义层，再谈工具替换，否则新工具只是复制旧的混乱。"),
 ("引入自然语言查询后，还需要保留语义层吗？",
  "需要，而且更重要。自然语言只是入口，答案的可信度取决于底层是否有受控的指标定义。没有语义层的自然语言查询，会把口径歧义放大成管理层对数据信任的流失。"),
 ("自助式 BI 的成效该用哪些指标验收？",
  "建议跟踪取数等待时间、IT 临时取数工单量，以及非技术岗位的自助完成率。文中数据显示 72% 的企业已有 AI 试点在生产环境运行，但仅 23% 实现跨部门扩展，采用广度是主要瓶颈。"),
],

"supply-chain-ai-optimization-summer-2025.html": [
 ("夏季需求波动大，AI 预测该如何应对季节性峰值？",
  "建议把天气、节假日与促销日历等外部信号纳入模型，并以周为单位滚动更新预测。对季节性强的品类，用去年同期数据做基线再叠加当期偏差，通常比完全依赖近期数据更稳。"),
 ("供应链 AI 项目最容易在哪个环节失效？",
  "多在预测与执行脱节。预测结果若不能自动进入补货与排产系统，就只是另一张报表。建议优先打通从预测到补货建议的链路，并保留计划员的人工覆写权，让系统建议接受实践检验。"),
 ("供应商与物流数据质量参差不齐，还能上 AI 吗？",
  "可以，但要先界定数据边界。建议先在数据较完整的环节试点，同时为缺失数据设置置信度标识，让模型输出附带可信区间，避免计划员把低置信度预测当成确定结论。"),
 ("供应链 AI 的价值该怎么向管理层证明？",
  "建议锁定库存周转天数、缺货率与紧急运输成本三项。文中数据显示 72% 的企业已有 AI 试点进入生产环境，但仅 23% 跨部门扩展；供应链涉及多方协同，更需要先在单一品类上验证。"),
],

"telecommunications-ai-network-optimization.html": [
 ("电信网络优化引入 AI，最先见效的场景是什么？",
  "通常是故障预测与容量调度。网络侧已有较完整的告警与性能数据，用 AI 识别异常模式并提前干预，比直接做全自动控制更容易验证价值，也更容易被网络运维团队接受。"),
 ("网络数据量大且实时性强，AI 模型该如何部署？",
  "建议分层部署：对时延敏感的异常检测放在靠近网元的边缘侧，模型训练与策略优化集中在中心平台。这样既控制回传带宽压力，也让策略更新不必逐点下发。"),
 ("运营商做 AI 网络优化，常见的风险有哪些？",
  "主要是自动化动作影响现网稳定性，以及告警数据本身存在标签噪声。建议先以建议模式运行，让 AI 输出处置建议由工程师确认，积累足够样本后再逐步放开自动执行。"),
 ("如何衡量 AI 网络优化带来的业务价值？",
  "建议看平均故障修复时长、告警压缩率，以及因容量不足导致的体验劣化投诉量。文中提到企业 AI 平均回本期已从 24 个月降至 14 个月，网络侧数据基础较好，回收节奏通常更快。"),
],

"united-kingdom-ai-safety-institute-report.html": [
 ("英国 AI 安全研究所的报告，对港股与内地企业有约束力吗？",
  "报告本身不具直接约束力，但其评估方法与模型安全要求正被其他司法辖区引用。若企业向英国客户提供服务或模型能力，提前对齐其安全评估口径，可避免后续重复整改与重复测评。"),
 ("报告中最需要企业提前准备的是哪部分？",
  "是模型评估与文档留存。企业需要能说明模型的训练数据边界、评测方法与已知局限，并保留可审计记录。这类证据链需要时间积累，临时补材料的成本远高于日常沉淀。"),
 ("同时面对英国、欧盟与内地规则，合规怎么避免重复投入？",
  "建议建立一套统一的 AI 资产清单与风险分级，再按各辖区要求映射差异项。把模型登记、评测记录、变更留痕等通用部分做成常设流程，只把辖区特有要求作为叠加层处理。"),
 ("下一波监管浪潮到来前，企业现在应该做什么？",
  "先把治理框架从文档转为可运营流程：指定模型责任人、建立上线前评审，并对高风险场景保留人工复核。文中提到提前建立框架的组织，其合规成本明显低于事后补救的同行。"),
],

"us-state-level-ai-legislation-tracker.html": [
 ("美国各州 AI 立法进度不一，企业该按哪个标准准备？",
  "建议按最严格辖区的共性要求建立基线，例如算法影响评估、自动化决策告知与人工复核通道。以共性要求打底、再针对特定州做增量适配，比逐州单独应对更节省合规成本。"),
 ("州级 AI 法案最常见的合规义务是什么？",
  "集中在透明告知与歧视防范两块：向消费者说明其正在与 AI 系统交互，对招聘、信贷等高风险场景保留人工复核，并能够说明模型的评测方法与偏差检验结果。"),
 ("业务只覆盖香港与大湾区，还需要关注美国州法吗？",
  "若服务涉及美国终端用户，或客户为在美运营的跨国企业，要求通常会通过合同条款传导过来。建议先梳理客户与数据流是否触及美国辖区，再决定投入范围，而不是默认忽略或全面铺开。"),
 ("立法仍在变动，怎样做合规投入才不浪费？",
  "把投入放在不易过时的能力上：AI 用例清单、风险分级、模型文档与变更留痕。这些是各法案的共同底座，具体条款变化时只需调整映射关系，不必重建整套体系。"),
],

"vendor-lock-in-risks-ai-platforms-2025.html": [
 ("选 AI 平台时，哪些条款最容易造成后期锁定？",
  "需重点关注数据导出的格式与费用、模型和提示词的可迁移性，以及按调用量计费的阶梯条款。若退出时需要重训模型或重建数据管道，切换成本会在续约谈判中直接转化为议价劣势。"),
 ("已经深度使用某个平台，还有降低锁定的办法吗？",
  "有。可把自有数据与语义层保留在企业可控的存储中，只让平台调用；并把提示词、评测集与业务流程文档化。这样即使更换供应商，核心资产仍然可以迁移。"),
 ("多云或多供应商策略值得投入吗？",
  "取决于切换成本是否低于风险敞口。对核心且高频的能力，保留一个经验证的备用方案通常值得；对边缘用例，过度分散反而增加集成与治理负担，往往得不偿失。"),
 ("该如何在合同层面提前设防？",
  "建议在签约时就约定数据可携与退出的时间、格式与费用，价格调整的提前通知期，以及服务中止时的过渡支持。文中提到企业 AI 平均回本期已从 24 个月降至 14 个月，退出条款应与这个节奏匹配。"),
],

"voice-interface-bi-query-adoption.html": [
 ("语音查询 BI 现在适合在哪些场景使用？",
  "更适合双手被占用或移动中的场景，例如巡店、仓储盘点与车间巡检，用语音快速询问货位状态或当日达成率。在需要精细对比的报表场景，图形界面仍然更高效。"),
 ("语音查数的准确率瓶颈主要在哪里？",
  "主要在口语转写与业务术语对齐，而不是后端查询。同一个指标在口语中可能有多种叫法，建议建立业务词表与别名映射，并在返回答案时回显所采用的指标定义供用户确认。"),
 ("在开放式办公环境用语音查数，数据安全怎么处理？",
  "涉及敏感指标时建议设置语音通道的二次校验，并对结果做字段级脱敏。同时明确哪些指标允许语音查询，避免财务与人事数据在公共区域被朗读出来。"),
 ("企业该怎么判断语音查询是否值得投入？",
  "先看目标岗位是否真的处于移动或不便打字的场景，再小范围试点。验收可用任务完成率与平均查询耗时衡量；文中提到企业 AI 平均回本期已从 24 个月降至 14 个月，投入应与回本节奏对齐。"),
],

}

# ---- 英文标题翻译（简体中文）----
# (英文原文, 译文, 该标题的 id)  —— id 为 None 表示推荐卡片 h3（按文本替换）
HEADS = {

"edge-ai-retail-processing-data-decisions.html": [
 ("Edge AI Applications in Retail", "边缘 AI 在零售的应用场景", "edge-ai-applications-in-retail"),
 ("Integrating Edge AI with Enterprise Data Architecture", "边缘 AI 与企业数据架构整合", "integrating-edge-ai-with-enterprise-data-architecture"),
 ("Implementation Roadmap", "实施路线图", "implementation-roadmap"),
],

"enterprise-ai-adoption-metrics-benchmarking.html": [
 ("Framework for Strategic Decision-Making", "战略决策框架", "framework-for-strategic-decision-making"),
 ("Organizational Change and Capability Building", "组织变革与能力建设", "organizational-change-and-capability-building"),
 ("Measuring Strategic Impact", "衡量战略影响", "measuring-strategic-impact"),
],

"enterprise-ai-august-2026-month-ahead-trends.html": [
 ("Framework for Strategic Decision-Making", "战略决策框架", "framework-for-strategic-decision-making"),
 ("Organizational Change and Capability Building", "组织变革与能力建设", "organizational-change-and-capability-building"),
 ("Measuring Strategic Impact", "衡量战略影响", "measuring-strategic-impact"),
],

"enterprise-ai-risk-management-framework-proactive.html": [
 ("Framework for Strategic Decision-Making", "战略决策框架", "framework-for-strategic-decision-making"),
 ("Organizational Change and Capability Building", "组织变革与能力建设", "organizational-change-and-capability-building"),
 ("Measuring Strategic Impact", "衡量战略影响", "measuring-strategic-impact"),
],

"enterprise-ai-security-threat-landscape-2026.html": [
 ("What Technical Architecture and Implementation Are Required?", "需要哪些技术架构与实施能力？", "technical-architecture-and-implementation"),
 ("How Do You Integrate with Enterprise Systems?", "如何与企业现有系统集成？", "integration-with-enterprise-systems"),
 ("How Do You Optimize Performance and Manage Cost?", "如何优化性能并管控成本？", "performance-optimization-and-cost-management"),
],

"enterprise-ai-southeast-asia-opportunities-challenges.html": [
 ("Regulatory Fragmentation Challenge", "监管碎片化挑战", "regulatory-fragmentation-challenge"),
 ("Strategic Recommendations", "战略建议", "strategic-recommendations"),
],

"eu-ai-act-compliance-enterprise-checklist-2026.html": [
 ("Building a Compliant AI Program", "构建合规的 AI 体系", "building-a-compliant-ai-program"),
 ("Cross-Border Data and AI Compliance", "跨境数据与 AI 合规", "cross-border-data-and-ai-compliance"),
 ("Preparing for Future Regulation", "为未来监管做准备", "preparing-for-future-regulation"),
],

"evaluate-ai-vendors-enterprise-deployment.html": [
 ("A Framework for Enterprise AI Vendor Evaluation", "企业 AI 供应商评估框架", "a-framework-for-enterprise-ai-vendor-evaluation"),
 ("Common Evaluation Mistakes", "常见评估误区", "common-evaluation-mistakes"),
 ("Red Flags and Green Flags", "危险信号与积极信号", "red-flags-and-green-flags"),
],

"evolution-enterprise-search-keywords-to-context.html": [
 ("Context-Aware Search: How AI Changes the Game", "情境感知搜索：AI 如何改变规则", "context-aware-search-how-ai-changes-the-game"),
 ("From Search to Answers: The Conversational Interface", "从搜索到答案：对话式界面", "from-search-to-answers-the-conversational-interface"),
 ("Implementation Strategy", "实施策略", "implementation-strategy"),
],

"finance-ai-regulatory-reporting-automation.html": [
 ("Domain-Specific Implementation Patterns", "领域专属实施模式", "domain-specific-implementation-patterns"),
 ("ROI Measurement and Value Realization", "ROI 衡量与价值实现", "roi-measurement-and-value-realization"),
 ("Overcoming Industry-Specific Barriers", "克服行业特有障碍", "overcoming-industry-specific-barriers"),
],

"financial-services-ai-fraud-detection-real-time.html": [
 ("What Are the Domain-Specific Implementation Patterns?", "有哪些领域专属实施模式？", "domain-specific-implementation-patterns"),
 ("How Is ROI Measured and Value Realized?", "如何衡量 ROI 并实现价值？", "roi-measurement-and-value-realization"),
 ("How Do You Overcome Industry-Specific Barriers?", "如何克服行业特有障碍？", "overcoming-industry-specific-barriers"),
],

"interplay-data-privacy-ai-innovation.html": [
 ("What Is a Privacy-by-Design AI Architecture?", "什么是隐私优先的 AI 架构？", "privacy-by-design-ai-architecture"),
 ("What Is the Business Case for Privacy-First AI?", "隐私优先 AI 的商业价值是什么？", "the-business-case-for-privacy-first-ai"),
 ("What Actionable Recommendations Apply?", "有哪些可执行的建议？", "actionable-recommendations"),
],

"llm-deployment-production-enterprise-best-practices.html": [
 ("Technical Architecture and Implementation", "技术架构与实施", "technical-architecture-and-implementation"),
 ("Integration with Enterprise Systems", "与企业系统集成", "integration-with-enterprise-systems"),
 ("Performance Optimization and Cost Management", "性能优化与成本管理", "performance-optimization-and-cost-management"),
],

"manufacturing-ai-predictive-quality-analytics-2026.html": [
 ("Domain-Specific Implementation Patterns", "领域专属实施模式", "domain-specific-implementation-patterns"),
 ("ROI Measurement and Value Realization", "ROI 衡量与价值实现", "roi-measurement-and-value-realization"),
 ("Overcoming Industry-Specific Barriers", "克服行业特有障碍", "overcoming-industry-specific-barriers"),
],

"manufacturing-analytics-oee-to-business-intelligence.html": [
 ("Bridging OEE and Business Intelligence", "打通 OEE 与商业智能", "bridging-oee-and-business-intelligence"),
 ("Real-World Applications", "实际应用案例", "real-world-applications"),
 ("Implementation Approach", "实施路径", "implementation-approach"),
],

}

# 推荐卡片英文标题（与英文猫标签）翻译
CARDS = [
 ("Data Quality Automation From Reactive To Proactive Part 2", "数据质量自动化：从被动到主动（二）"),
 ("Cfo Guide Ai Budget Allocation", "首席财务官指南：AI 预算分配"),
]
CATS = [("Technology", "技术")]
