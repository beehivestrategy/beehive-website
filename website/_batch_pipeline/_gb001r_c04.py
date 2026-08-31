# -*- coding: utf-8 -*-
"""Content specs: data-lineage, semantic-layer-roi, knowledge-management."""

DATA_LINEAGE = {
    "en": {
        "h2fix": {
            "understanding-the-current-landscape": "What Does the Current Lineage Landscape Look Like?",
            "key-principles-and-strategic-framework": "What Are the Key Principles Behind Lineage Automation?",
            "implementation-approach-and-best-practices": "How Should You Implement Lineage Automation?",
            "measuring-success-and-demonstrating-roi": "How Do You Measure Success and Demonstrate ROI?",
            "how-lineage-automation-accelerates-ai-governance": "How Does Lineage Automation Accelerate AI Governance?",
            "lineage-and-the-semantic-layer": "How Does Lineage Work With the Semantic Layer?",
            "practical-first-steps": "What Are the Practical First Steps?",
            "key-takeaways": "What Are the Key Takeaways?",
        },
        "faq": [
            ("What is the difference between automated lineage and documented lineage?",
             "Documented lineage is a snapshot maintained by hand — accurate on the day it is written and stale shortly after. Automated lineage is parsed from queries, orchestration metadata, and transformation logic on every run, so it reflects what actually happened rather than what was intended."),
            ("How much of the pipeline can realistically be covered automatically?",
             "Most teams reach 80–90% coverage on SQL-based transformations quickly. The remaining gap is usually stored procedures, spreadsheet-based adjustments, and external SaaS extracts, which need lightweight manual annotation rather than a parser."),
            ("How does Beehive Strategy help enterprises automate lineage?",
             "Beehive Strategy combines MCP-powered conversational BI with enterprise AI consulting, exposing automated lineage where questions are asked — so impact analysis and data-trust checks happen in the flow of work instead of during a quarterly review."),
        ],
    },
    "zh-cn": {
        "replace": [
            ("u到maing 血缘 trcking cross complex 数据管道s", "跨复杂数据管道自动追踪血缘"),
        ],
        "h2fix": {
            "理解当前格局": "数据血缘自动化的当前格局如何？",
            "关键原则与战略框架": "数据血缘自动化需要遵循哪些原则？",
            "实施方法与最佳实践": "数据血缘应该如何分阶段实施？",
            "衡量成功与展示投资回报率": "如何衡量数据血缘的回报？",
            "常见陷阱及规避方法": "数据血缘项目有哪些常见陷阱？",
            "关键要点": "关键要点",
            "结论": "结论",
        },
        "sections": [
            ("column-level-vs-table-level", "列级血缘与表级血缘的差别有多大？",
             """<p>表级血缘只能告诉你"这张表来自哪几张表"，一旦下游指标出问题，它无法指出是哪一列出的问题。修复时只能逐列排查，耗时且容易遗漏。</p>
<p>列级血缘把映射关系精确到字段，问题定位直接指向具体的转换逻辑。对财务报表、监管报送这类场景，这个差别是能否在截止日期前完成核查的关键。</p>
<p>代价是解析复杂度更高。复杂 SQL、嵌套视图、以及存储过程都可能让列级解析失效。务实的做法是对核心链路要求列级精度，对边缘链路接受表级精度，而不是一刀切地追求全覆盖。</p>""",
             "关键要点"),
            ("where-lineage-efforts-stall", "血缘项目通常卡在哪里？",
             """<p>最常见的卡点是存储过程与手工调整。解析器能处理标准 SQL，却读不懂写在存储过程里的业务逻辑，也看不到分析师在表格里做的临时修改。这部分往往正是关键指标的来源。</p>
<p>第二个卡点是跨系统链路。数据从业务系统抽取、经过多个中间层、最终进入报表工具，任何一个环节没有埋点，链路就断了。因此覆盖率的提升更多依赖接入规范，而不是解析技术本身。</p>
<p>务实的目标是先覆盖关键链路，再逐步扩展。追求百分之百覆盖通常会让项目停留在试点阶段，而覆盖住财务报送与监管相关的核心链路，已经能产生绝大部分价值。</p>""",
             "关键要点"),
            ("lineage-for-impact-analysis", "血缘最有价值的应用场景是什么？",
             """<p>最有价值的场景是变更影响分析。任何人想要修改一个字段定义或调整一段转换逻辑，都先问一句"会影响什么"。没有血缘，这个问题的答案是凭记忆；有血缘，答案是几分钟内可查的清单。</p>
<p>第二高价值的场景是可信度追溯。当有人质疑一个数字时，能够一路追到来源系统与转换步骤，把争论从"我觉得不对"变成"这一步的口径是什么"。这直接减少了会议时间。</p>
<p>第三是合规举证。监管询问某项指标的数据来源时，能够提供完整的流转路径与变更历史。这类请求在有血缘的系统上是查询，在没有血缘的系统上是一次跨部门调查。</p>""",
             "关键要点"),
        ],
        "faq": [
            ("自动化血缘与人工文档式血缘有什么区别？",
             "文档式血缘是手工维护的快照——写下的当天准确，之后很快过时。自动化血缘在每次运行时从查询日志、编排元数据与转换逻辑中解析，反映的是实际发生了什么，而不是原本设计成什么。"),
            ("自动化的覆盖率实际能做到多少？",
             "多数团队在基于 SQL 的转换上能较快达到 80% 到 90% 的覆盖。剩下的缺口通常是存储过程、以表格形式进行的调整、以及外部 SaaS 数据抽取，这些需要轻量的人工标注，而不是继续写解析器。"),
            ("蜂启咨询如何帮助企业实现血缘自动化？",
             "蜂启咨询把 MCP 驱动的对话式分析与企业 AI 咨询结合，把自动化血缘暴露在提问发生的地方，让影响分析与数据可信度检查在日常工作中完成，而不是等到季度评审才做。"),
        ],
    },
}

SEMANTIC_LAYER_ROI = {
    "en": {
        "h2fix": {
            "why-it-matters": "Why Does Semantic Layer ROI Matter?",
            "common-challenges": "What Are the Common Challenges?",
            "how-to-get-started": "How Should You Get Started?",
            "where-does-semantic-layer-roi-actually-come-from": "Where Does Semantic Layer ROI Actually Come From?",
            "frequently-asked-questions": "Frequently Asked Questions",
            "key-takeaways": "What Are the Key Takeaways?",
        },
        "sections": [
            ("what-a-semantic-layer-actually-contains", "What Does a Semantic Layer Actually Contain?",
             """<p>Strip away the marketing and a semantic layer is three things: a metric definition store, a dimensional model that describes how those metrics can be sliced, and an access-control layer that decides who may see what. Everything else is tooling around those three.</p>
<p>The metric store is the part that pays for itself. One definition of revenue, one definition of active customer, one definition of churn — each with a named owner and a version history. Without it, every dashboard is a private negotiation about what the number means.</p>
<p>The access layer is the part that is usually discovered late. If permissions are applied after the query returns rather than before it runs, the semantic layer becomes a leak path rather than a control point. This is the single most common reason a well-designed layer fails review.</p>"""),
            ("how-to-build-the-business-case", "How Do You Build the Business Case?",
             """<p>Start by measuring the cost of the status quo, because that number is larger than most teams expect. Count the analyst hours spent answering repeat questions, the hours spent reconciling two dashboards that disagree, and the rework caused by a metric definition that changed without notice.</p>
<p>Then attach the semantic layer to those three buckets. Reuse removes repeat work, single definitions remove reconciliation, and versioned definitions remove silent rework. Each bucket has an owner who can estimate the hours involved, which makes the case defensible rather than aspirational.</p>
<p>Finally, name the second-order benefit honestly: faster decisions. This is real but hard to attribute, so present it as a directional indicator — decision cycle time on the questions the layer covers — rather than folding it into the headline savings figure.</p>"""),
            ("what-goes-wrong-with-semantic-layers", "What Goes Wrong With Semantic Layer Projects?",
             """<p>The most common failure is treating the semantic layer as a documentation exercise. A catalogue that describes metrics without enforcing them changes nothing: teams keep writing their own SQL, and the catalogue drifts from reality within a quarter.</p>
<p>The second failure is building for the tool rather than for the question. Layers designed around a specific BI vendor's object model tend to lock definitions into that vendor, which means a migration later costs as much as the original build. Keeping definitions in a tool-neutral form avoids this.</p>
<p>The third failure is underestimating the governance work. Agreeing on one definition of an active customer is a negotiation between sales, finance, and product. That conversation cannot be automated, and projects that skip it end up with a technically excellent layer nobody trusts.</p>"""),
        ],
        "faq": [
            ("What is a semantic layer, and how is it different from a data model?",
             "A data model describes how data is stored. A semantic layer describes how the business talks about it — metrics, dimensions, and permissions expressed in business language, independent of the underlying tables. The same data model can support several semantic layers; a good semantic layer should survive a warehouse migration."),
            ("How long does it take to see a return from a semantic layer?",
             "Most organisations see a measurable reduction in repeat analyst questions within one quarter if they start with a single domain. Enterprise-wide consistency takes longer, because it is as much a governance change as a technical one — the definitions have to be agreed before they can be enforced."),
            ("How does Beehive Strategy help enterprises realise semantic layer ROI?",
             "Beehive Strategy combines MCP-powered conversational BI with enterprise AI consulting, building the metric layer and wiring it into the tools people already use, so the return shows up as fewer repeated questions and faster decisions rather than another unused catalogue."),
        ],
    },
    "zh-cn": {
        "h2fix": {
            "为什么重要": "为什么语义层值得投入？",
            "常见挑战": "落地语义层常见的挑战有哪些？",
            "如何开始": "企业应该如何开始？",
            "语义层的回报到底能有多大": "语义层的回报到底能有多大？",
            "核心要点": "核心要点",
            "常见问题": "常见问题",
        },
        "sections": [
            ("what-is-in-a-semantic-layer", "语义层里到底装了什么？",
             """<p>去掉营销包装，语义层就是三样东西：指标定义库、描述指标可如何拆分的维度模型、以及决定谁能看什么的访问控制层。其余都是围绕这三者的工具。</p>
<p>指标定义库是最先产生回报的部分。收入只有一个定义，活跃客户只有一个定义，流失率只有一个定义——每个定义都有具名负责人与版本历史。没有它，每一张报表都是一次关于"这个数字到底指什么"的私下协商。</p>
<p>访问控制层往往最晚被发现。如果权限是在查询返回之后才生效，而不是在查询执行之前，语义层就从控制点变成了泄漏通道。这是设计良好的语义层在评审中被否掉的最常见原因。</p>""",
             "核心要点"),
            ("how-to-build-the-business-case", "如何构建语义层的商业论证？",
             """<p>先量化现状的成本，这个数字通常比团队预期的大得多。统计分析师花在重复问题上的工时、花在对齐两张口径不一致的报表上的工时、以及因为指标定义悄悄变更导致的返工。</p>
<p>然后把语义层对应到这三类成本：复用消除重复劳动，单一定义消除对齐成本，版本化定义消除隐性返工。每一类都有明确的负责人可以估算工时，论证因此可辩护而不是停留在愿景层面。</p>
<p>最后要诚实地处理间接收益——决策更快。这是真实的但难以归因，应当作为方向性指标呈现，比如被语义层覆盖的问题其决策周期缩短了多久，而不是把它算进头条的节省金额里。</p>""",
             "核心要点"),
        ],
        "faq": [
            ("什么是语义层，它与数据模型有什么不同？",
             "数据模型描述数据如何存储；语义层描述业务如何谈论数据——用业务语言表达的指标、维度与权限，独立于底层表结构。同一个数据模型可以支撑多套语义层，而一套好的语义层应当能在数据仓库迁移后继续存在。"),
            ("语义层多久能看到回报？",
             "如果从单一业务域切入，多数企业在一个季度内就能看到重复提问明显减少。全企业范围的口径一致需要更久，因为这既是技术变更也是治理变更——定义必须先被各方认可，才能被系统强制执行。"),
            ("蜂启咨询如何帮助企业实现语义层的投资回报？",
             "蜂启咨询把 MCP 驱动的对话式分析与企业 AI 咨询结合，建设指标层并接入团队已在使用的工具，让回报体现为更少的重复提问与更快的决策，而不是又一个无人使用的目录。"),
        ],
    },
}

KNOWLEDGE_MGMT = {
    "en": {
        "h2fix": {
            "understanding-the-current-landscape": "What Does the Current Knowledge Management Landscape Look Like?",
            "key-principles-and-strategic-framework": "What Are the Key Principles of Consulting Knowledge Management?",
            "implementation-approach-and-best-practices": "How Should Firms Implement Knowledge Management?",
            "measuring-success-and-demonstrating-roi": "How Do Firms Measure Knowledge Management ROI?",
            "common-pitfalls-in-consulting-knowledge-systems": "What Are the Common Pitfalls in Consulting Knowledge Systems?",
            "key-takeaways": "What Are the Key Takeaways?",
        },
        "faq": [
            ("Why do consultants not search the knowledge base they already have?",
             "Because searching usually costs more than asking a colleague. If retrieval takes four clicks and returns forty documents ranked by date, a senior colleague's answer is faster and more reliable. Adoption is a function of retrieval quality, not of how good the repository is."),
            ("What knowledge should a consulting firm manage first?",
             "Start with proposals and deliverables for the practice's highest-volume engagement type. That material is reused most often, has a clear owner, and produces visible time savings — which is what funds the next phase."),
            ("How does Beehive Strategy help consulting firms manage knowledge?",
             "Beehive Strategy combines MCP-powered conversational BI with enterprise AI consulting, turning accumulated engagement material into a governed, searchable answer layer — so consultants get a sourced answer in seconds instead of browsing a document library."),
        ],
    },
    "zh-cn": {
        "replace": [
            ("trs为ming 知识 管理 与 AI 在 consulting", "AI 时代的知识管理"),
            ("一座 pristine 的百科全书", "一座完美无瑕的百科全书"),
        ],
        "h2fix": {
            "理解当前格局": "咨询公司知识管理的现状如何？",
            "关键原则与战略框架": "咨询公司知识管理应遵循哪些原则？",
            "实施方法与最佳实践": "知识管理体系应该如何落地？",
            "衡量成功与展示投资回报率": "如何衡量知识管理的回报？",
            "常见陷阱及规避方法": "知识管理项目有哪些常见陷阱？",
            "关键要点": "关键要点",
            "结论": "结论",
        },
        "sections": [
            ("why-repositories-go-unused", "为什么建好的知识库没人用？",
             """<p>核心原因是检索成本高于问同事。如果找到一份可用材料需要四次点击、再从四十份按日期排序的结果里自己挑，那么直接问一位资深同事更快也更可靠。采纳率取决于检索质量，而不是库里存了多少东西。</p>
<p>第二个原因是材料的质量参差。没有标注适用范围与结论时效的旧方案，读起来风险很高——引用一个有过期结论的模板，后果比重新写一份更严重。使用者因此倾向于从零开始。</p>
<p>第三个原因是贡献没有回报机制。写材料的人得不到任何认可，也不计入绩效，那么理性选择就是不写。知识管理失败在这一步的情况比技术原因多得多。</p>""",
             "关键要点"),
            ("capture-without-extra-work", "如何让沉淀不变成额外工作？",
             """<p>要求顾问额外整理材料，几乎一定失败。项目交付期本就紧张，任何不直接服务于当前交付的工作都会被放到最后，然后不做了。</p>
<p>可行的做法是让沉淀成为交付的副产品。提案、报告、模型文件在交付流程中本来就会产生，需要做的只是自动归档、抽取关键信息、并打上项目类型与行业标签。</p>
<p>再往前一步，在项目收尾环节加入一个五分钟的结构化复盘：这个项目的核心方法是什么、哪些材料可以复用、有哪些坑。这个动作足够轻，能坚持；也足够结构化，能被检索。</p>""",
             "关键要点"),
        ],
        "faq": [
            ("为什么顾问不去检索公司已有的知识库？",
             "因为检索的成本通常高于问同事。如果找到答案需要四次点击、还要从四十份按日期排序的结果里自己挑，那么资深同事的回答更快也更可信。采纳率取决于检索质量，而不取决于知识库存了多少内容。"),
            ("咨询公司应该优先管理哪些知识？",
             "先从业务量最大的那一类项目的提案与交付物开始。这类材料复用频率最高、责任人清晰、节省的时间也最直观，能为下一阶段的投入提供依据。"),
            ("蜂启咨询如何帮助咨询公司管理知识？",
             "蜂启咨询把 MCP 驱动的对话式分析与企业 AI 咨询结合，把累积的项目材料转化为受治理、可检索的答案层，让顾问在几秒内拿到带出处的答案，而不是在文档库里翻找。"),
        ],
    },
}

SPECS = {
    "data-lineage-automation-tools": DATA_LINEAGE,
    "semantic-layer-roi-enterprise-analytics": SEMANTIC_LAYER_ROI,
    "knowledge-management-consulting-firms": KNOWLEDGE_MGMT,
}
