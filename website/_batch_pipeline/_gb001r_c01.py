# -*- coding: utf-8 -*-
"""Content specs: vector-embeddings, cross-border, ai-regulation."""

VECTOR_EMBEDDINGS = {
    "en": {
        "h2fix": {
            "understanding-the-current-landscape": "Why Does Keyword Search Fail in the Enterprise?",
            "key-principles-and-strategic-framework": "What Are the Principles Behind Embedding-Based Search?",
            "implementation-approach-and-best-practices": "How Should You Implement Enterprise Vector Search?",
            "measuring-success-and-demonstrating-roi": "How Do You Measure the ROI of Enterprise Search?",
            "common-pitfalls-and-how-to-avoid-them": "What Are the Common Pitfalls and How Do You Avoid Them?",
            "conversational-search-and-the-knowledge-answer-layer": "How Does Conversational Search Change the Answer Layer?",
            "key-takeaways": "What Are the Key Takeaways?",
            "conclusion": "Conclusion",
        },
        "faq": [
            ("Do you need to rebuild your data platform before using vector embeddings?",
             "No. Embeddings are generated from content you already have — documents, tickets, wikis, product catalogues, and database records. A vector index sits alongside your existing systems, so the first production use case can ship in weeks rather than waiting for a warehouse migration."),
            ("When an embedding model is upgraded, must the whole index be rebuilt?",
             "Usually yes, because vectors from different models are not comparable in the same space. Plan for periodic full re-embedding, keep the corpus chunked and the pipeline idempotent, and version the index so you can roll back if quality metrics regress."),
            ("How does Beehive Strategy help enterprises deploy vector search?",
             "Beehive Strategy combines MCP-powered conversational BI with enterprise AI consulting, wiring vector retrieval into a governed semantic layer so answers are accurate, permission-aware, and traceable back to the source record."),
        ],
    },
    "zh-cn": {
        "replace": [
            ("向量嵌入在 enterprise 搜索", "企业搜索中的向量嵌入"),
            ("trs为ming 知识 retrievl 与语义搜索", "知识检索与语义搜索"),
        ],
        "h2fix": {
            "理解当前格局": "为什么企业搜索在 2026 年重新变得重要？",
            "关键原则与战略框架": "向量嵌入背后的核心原理是什么？",
            "实施方法与最佳实践": "企业应该如何落地向量检索？",
            "衡量成功与展示投资回报率": "如何衡量企业搜索的投资回报？",
            "常见陷阱及规避方法": "向量检索有哪些常见陷阱，如何规避？",
            "关键要点": "关键要点",
            "结论": "结论",
        },
        "sections": [
            ("why-keyword-search-fails", "为什么关键词检索在企业场景里会失效？",
             """<p>关键词检索假设用户知道正确的词。在企业里这个假设几乎从不成立。一份报销政策在财务系统里叫"费用报销管理办法"，在员工口中是"怎么报差旅"，在旧版文档里写作"费用请付流程"。三种说法指向同一份文件，但字面上没有任何重叠，倒排索引无法把它们关联起来。</p>
<p>失效的第二个来源是缩写与术语漂移。保险公司内部的"LB"可能指理赔准备金，也可能指理赔积压，取决于说话的是精算还是运营。关键词检索对这种歧义无能为力，只能把两种含义的文档混在一起返回，让使用者自己分辨。</p>
<p>第三个来源是长尾查询。企业搜索的绝大多数查询是低频的：一个具体的客户编号、一次特定事故的工单、某个季度某条产品线的毛利率。这些内容在文档里出现的措辞千差万别，任何同义词表都难以覆盖。</p>""",
             "关键要点"),
            ("how-embeddings-represent-meaning", "向量嵌入是如何把语义变成可计算距离的？",
             """<p>嵌入模型把一段文本映射成一个高维向量——通常是几百到几千个浮点数。语义相近的文本在这个空间里距离更近，因此"怎么报差旅"和"费用报销管理办法"虽然用词完全不同，向量夹角却很小。检索问题由此从字符串匹配转化为最近邻搜索。</p>
<p>理解这一点很重要，因为它决定了系统的行为边界：嵌入擅长表达"意思相近"，不擅长精确匹配。查询一个具体订单号时，向量检索可能返回一串语义相似但编号不同的记录。这就是为什么生产环境几乎总是把向量检索与关键词检索结合使用。</p>
<p>切分策略对效果的影响通常大于模型选择。把一份 80 页的操作手册整篇嵌入，得到的向量是多种主题的平均值，对任何具体问题都不够精确。按语义单元切分——章节、条款、问答对——并为每个片段保留原始出处与权限标签，召回质量才会有实质改善。</p>""",
             "关键要点"),
            ("hybrid-search-default", "为什么混合检索是企业搜索的默认答案？",
             """<p>混合检索同时运行关键词检索与向量检索，再把两路结果融合排序。它同时覆盖了两类需求：精确匹配处理编号、代码、人名、专有名词；向量检索处理描述性、含糊、跨措辞的提问。任何单独一路都会在另一类查询上明显退化。</p>
<p>融合方式通常有两条路。一是加权分数融合，实现简单、延迟低，适合对延迟敏感的场景。二是先用两路各自召回较大候选集，再用重排序模型统一打分，准确率更高但增加一次模型调用。多数团队从加权融合起步，在准确率成为瓶颈时再引入重排序。</p>
<p>权限过滤必须在检索阶段而不是生成阶段完成。如果先召回再过滤，敏感内容已经进入上下文，即使最终不展示，也存在泄漏风险。正确做法是把访问控制下推到向量数据库，让每个片段携带可见范围标签，检索时即完成过滤。</p>""",
             "关键要点"),
            ("vector-db-vs-warehouse", "向量数据库与现有数据仓库是什么关系？",
             """<p>两者解决的不是同一个问题，也不应该互相替代。数据仓库存储结构化的事实——订单、账目、库存，擅长精确聚合与联表计算。向量数据库存储非结构化内容的语义表示——文档、工单、通话记录，擅长模糊匹配与语义召回。</p>
<p>把它们对立起来通常是错误决策的来源。真正需要的是分工：结构化指标仍然由数据仓库回答，保证口径与可审计；非结构化知识的检索交给向量库；最终在语义层把两类结果统一成同一个答案。</p>
<p>选择向量数据库时重点看三点：是否支持在检索阶段做权限过滤、是否支持元数据过滤与混合检索、重建索引时能否不中断服务。第三点最容易被忽略——嵌入模型升级意味着周期性全量重建，如果每次重建都要停机，运维成本会长期累积。</p>""",
             "关键要点"),
            ("keeping-embeddings-fresh", "内容持续变化时，如何让嵌入保持新鲜？",
             """<p>知识库不是静态的。政策更新、产品下线、人员变动都会让一部分嵌入失效，检索结果指向已被替代的旧版本。用户只要发现一次，对整个系统的信任就会明显下降。</p>
<p>务实的做法是增量更新加生命周期管理。文档变更时只对受影响的片段重新嵌入，而不是全量重建；同时为每个片段记录源文档的更新时间，超过阈值仍未刷新的片段在检索时降权或加注提示。</p>
<p>权限变更也必须触发重新处理。一名员工调岗后，他此前可访问的文档片段如果仍留在向量库里且标签未更新，就构成实质性的越权风险。把权限同步做成事件驱动而不是依赖定期全量扫描，是控制这类风险的关键。</p>""",
             "关键要点"),
            ("evaluate-search-quality", "如何评估企业搜索的真实质量？",
             """<p>企业搜索最常见的评估错误是只看召回率的平均值。平均值会掩盖真正重要的失败：用户并不关心一百次查询的平均表现，只关心他这一次查不到答案时的挫败感。更有意义的指标是"首条命中率"和"前三条命中率"——正确来源出现在结果前几位的比例。</p>
<p>构建测试集不需要上千条数据。从真实的搜索日志里抽取 100 到 200 条高频查询，由业务专家标注期望答案来源，就足以支撑迭代。关键是测试集要包含失败案例：那些用户搜过、点过、又回到群里问同事的查询，才是最有价值的样本。</p>
<p>上线之后要持续追踪三个行为指标：零结果率、首条结果的点击率、以及"搜索后仍发起人工求助"的比例。第三个指标最能说明问题——它直接衡量搜索有没有真正解决问题，而不是有没有返回东西。</p>""",
             "关键要点"),
        ],
        "faq": [
            ("企业需要重建数据平台才能使用向量嵌入吗？",
             "不需要。嵌入是从已有内容生成的——文档、工单、维基、产品目录、数据库记录。向量索引并行部署在现有系统旁边，第一个生产用例可以在数周内上线，不必等待数据仓库迁移完成。"),
            ("嵌入模型升级后，向量索引需要全量重建吗？",
             "通常需要，因为不同模型产生的向量不在同一个空间里，无法直接比较。应当把全量重建作为周期性任务来规划，保持切分与管道幂等，并对索引做版本管理，一旦质量指标回退就能回滚。"),
            ("蜂启咨询如何帮助企业落地向量检索？",
             "蜂启咨询把 MCP 驱动的对话式分析与企业 AI 咨询结合，将向量检索接入受治理的语义层，使答案既准确、又符合权限，并且可以追溯回源记录。"),
        ],
        "excerpts": [
            "以語義層與治理框架為底座，說明企業 AI 平台該如何建立可問責的治理機制。",
            "從資料血緣自動化出發，解釋信任如何成為分析規模化的前提。",
            "拆解對話式 BI 的選型框架，協助買方在六個支柱上做可驗證的比較。",
        ],
    },
}

CROSS_BORDER = {
    "en": {
        "h2fix": {
            "understanding-the-current-landscape": "Why Is the Cross-Border Data Landscape Shifting?",
            "key-principles-and-strategic-framework": "What Principles Should Anchor a Cross-Border Framework?",
            "implementation-approach-and-best-practices": "How Should You Implement Cross-Border Controls?",
            "measuring-success-and-demonstrating-roi": "How Do You Measure Cross-Border Governance ROI?",
            "common-pitfalls-and-how-to-avoid-them": "Which Pitfalls Break Cross-Border Data Programmes?",
            "key-takeaways": "What Are the Key Takeaways?",
            "conclusion": "Conclusion",
        },
        "faq": [
            ("What is the first step in building a cross-border data governance framework?",
             "Build a data inventory that maps which data categories sit in which country, which systems replicate them, and which legal basis covers each transfer. Without that map, every subsequent control is guesswork."),
            ("How do you keep global reporting consistent when local rules differ?",
             "Separate the metric definition from the storage location. Govern definitions centrally in a semantic layer, then apply local residency and access rules at the query layer, so a global number is computed once and reported consistently."),
            ("How does Beehive Strategy support cross-border data governance?",
             "Beehive Strategy combines MCP-powered conversational BI with enterprise AI consulting, so governed definitions, lineage, and residency rules are enforced where the question is asked rather than in a policy document nobody reads."),
        ],
    },
    "zh-cn": {
        "h2fix": {
            "理解当前格局": "为什么跨境数据环境正在持续收紧？",
            "关键原则与战略框架": "跨境治理框架应该以哪些原则为锚？",
            "实施方法与最佳实践": "跨境管控措施应该如何落地？",
            "衡量成功与展示投资回报率": "如何衡量跨境治理的回报？",
            "常见陷阱及规避方法": "哪些陷阱会让跨境数据项目失败？",
            "关键要点": "关键要点",
            "结论": "结论",
        },
        "sections": [
            ("what-is-a-cross-border-transfer", "什么构成一次跨境传输？",
             """<p>多数团队把跨境传输理解成"把文件传到另一个国家"，这个理解太窄，也是合规缺口的主要来源。远程访问同样构成传输：一名新加坡的分析师查询存放在法兰克福的数据，数据本身没有移动，但已经发生了跨境访问。</p>
<p>云端复制与备份同样算数。很多企业把主数据库放在本地，却没有意识到云厂商的灾备副本落在另一个司法辖区。还有一类容易被忽略的是支持与运维：海外技术支持团队为了排障登录生产系统查看客户数据，这也是一次跨境处理行为。</p>
<p>把定义写清楚之后，下一步是把数据流画出来。不是画架构图，而是画数据流图——哪个系统产生、哪个系统复制、谁在哪个国家访问、依据哪条合法性基础。这张图是后续所有控制措施的基础。</p>""",
             "关键要点"),
            ("data-residency-vs-data-localization", "数据本地化与数据驻留是一回事吗？",
             """<p>不是。数据本地化是法律要求——某些类别的数据必须存放在境内，通常不允许出境。数据驻留更多是技术或商业选择——企业出于延迟、成本或客户合同把数据放在某个区域，但法律并不强制。</p>
<p>混淆两者会导致两种浪费：一是把非强制的数据也强行本地化，为每个区域复制一套完整技术栈，成本成倍上升却没有任何合规收益；二是把强制本地化的数据当作普通数据，在跨境报表里自由流转，形成实质违规。</p>
<p>正确做法是按数据类别分级。个人身份信息、健康数据、金融账户数据通常属于高敏感类别，适用本地化或严格传输机制；聚合后的经营指标、脱敏后的趋势数据一般可以自由流动。分级表必须能追溯到具体法条，而不是凭经验判断。</p>""",
             "关键要点"),
            ("operationalizing-transfer-mechanisms", "传输机制如何落到日常运营里？",
             """<p>标准合同条款、约束性公司规则、以及各类合规认证，解决的是"能不能传"的问题。真正困难的是"每一次传的时候，系统怎么知道能不能传"。这需要把法律结论翻译成可执行的技术规则。</p>
<p>可执行的形态有三层。最上层是策略层，用人类可读的语言描述规则：某类数据在某个条件下可以流向某类主体。中间层是标签层，为数据与主体打上对应标记。最下层是执行层，在查询、导出、复制三个动作上强制检查。</p>
<p>三层之中最容易被跳过的是执行层。很多企业的策略写得很完善，但导出功能是一个不带任何检查的"导出 CSV"按钮，全部控制在人的自觉。把检查做进导出接口，比再写十份政策文件都有效。</p>""",
             "关键要点"),
            ("living-data-inventory", "数据清单怎样做才不会变成一次性工作？",
             """<p>多数数据清单项目失败的方式很一致：花三个月做出一份详尽的表格，半年后与现实完全脱节，从此无人再打开。问题不在表格质量，而在于它依赖人工维护。</p>
<p>可行的替代是把清单变成自动生成的副产品。数据来源应当是元数据扫描——数据库的表结构、ETL 作业的血缘、对象存储的桶与区域、日志中的跨境访问记录。系统每天自动汇总，人只负责校正例外与争议项。</p>
<p>还需要一个强制触发点：任何新系统上线、任何新的跨境接口，都必须先在数据清单里登记才能开通网络策略。把登记做成流程的必经环节，清单才能保持有效。</p>""",
             "关键要点"),
            ("third-party-processors", "供应商与第三方处理者如何纳入治理？",
             """<p>企业的数据很少只在自己系统里流动。云服务、SaaS 分析工具、外包客服、模型供应商，每一方都可能是数据处理者，也都可能把数据带到新的司法辖区。</p>
<p>管理第三方的关键是把要求写进合同的技术附件，而不只是通用条款。需要明确四项：数据存储在哪些区域、是否允许跨境访问、子处理者的变更通知机制、以及合同终止后数据的删除时限与证明方式。</p>
<p>之后要验证而不是相信。年度问卷在监管面前价值有限，更有效的是要求供应商提供独立的审计或认证报告，并对高风险供应商做一次技术核查——确认其实际存储区域与合同描述一致。</p>""",
             "关键要点"),
            ("proving-compliance-to-regulators", "如何向监管证明你是合规的？",
             """<p>监管询问通常只有两个问题：这批数据在哪里，谁在什么时候访问过它。如果这两个问题需要两周时间、三个人翻日志才能回答，说明证据链没有建立起来。</p>
<p>证据链的核心是留痕。每一次跨境查询、导出、复制都要记录操作者、时间、数据范围、依据的合法性基础。留痕必须是自动生成的，不能依赖人工登记——人工登记在监管面前没有可信度。</p>
<p>第二个要素是可复现。监管要求重现某次数据处理过程时，系统应该能调出当时的完整上下文，包括所用的数据版本与规则版本。这需要版本化的元数据管理，而不是事后的口头说明。做到这两点，合规从被动答辩变成主动举证。</p>""",
             "关键要点"),
        ],
        "faq": [
            ("建立跨境数据治理框架的第一步是什么？",
             "先建立数据清单：哪些类别的数据位于哪个国家、哪些系统在复制它们、每一次传输依据哪条合法性基础。没有这张地图，后续所有控制措施都只能靠猜测。"),
            ("各地规则不同时，如何保持全球报表口径一致？",
             "把指标定义与存储位置分离。定义集中在语义层统一管理，本地的驻留与访问规则在查询层执行，这样一个全球指标只计算一次，各地看到的口径始终一致。"),
            ("蜂启咨询如何支持跨境数据治理？",
             "蜂启咨询把 MCP 驱动的对话式分析与企业 AI 咨询结合，让受治理的定义、血缘和驻留规则在执行查询的地方生效，而不是停留在没人读的政策文档里。"),
        ],
        "excerpts": [
            "以語義層與治理框架為底座，說明企業 AI 平台該如何建立可問責的治理機制。",
            "從資料血緣自動化出發，解釋信任如何成為分析規模化的前提。",
            "拆解對話式 BI 的選型框架，協助買方在六個支柱上做可驗證的比較。",
        ],
    },
}

AI_REGULATION = {
    "en": {
        "h2fix": {
            "understanding-the-current-landscape": "What Does the US AI Regulatory Landscape Look Like in 2026?",
            "key-principles-and-strategic-framework": "What Principles Should Guide US AI Compliance?",
            "implementation-approach-and-best-practices": "How Should You Build a US AI Compliance Programme?",
            "measuring-success-and-demonstrating-roi": "How Do You Demonstrate ROI on AI Governance?",
            "common-pitfalls-and-how-to-avoid-them": "What Are the Common Pitfalls in US AI Compliance?",
            "key-takeaways": "What Are the Key Takeaways?",
            "conclusion": "Conclusion",
        },
        "faq": [
            ("Is there a single US federal AI law enterprises must comply with?",
             "No. In 2026 the US picture remains a patchwork of sector regulators, state statutes, and enforcement actions rather than one omnibus federal statute. Practical compliance means mapping which regimes touch each AI use case and satisfying the strictest applicable requirement."),
            ("Which states are setting the AI compliance bar?",
             "Colorado, California, Texas, and Utah have moved furthest, with Colorado's consumer-facing automated decision rules and California's automated decision-making and frontier model provisions setting the practical template others copy."),
            ("How does Beehive Strategy help enterprises stay compliant?",
             "Beehive Strategy combines MCP-powered conversational BI with enterprise AI consulting, building the lineage, documentation, and access controls that turn an AI governance policy into evidence a regulator can actually review."),
        ],
    },
    "zh-cn": {
        "h2fix": {
            "理解当前格局": "2026 年美国 AI 监管格局是什么样的？",
            "关键原则与战略框架": "美国 AI 合规应该遵循哪些原则？",
            "实施方法与最佳实践": "企业应当如何建立美国 AI 合规体系？",
            "衡量成功与展示投资回报率": "如何证明 AI 治理的投入回报？",
            "常见陷阱及规避方法": "美国 AI 合规有哪些常见陷阱？",
            "关键要点": "关键要点",
            "结论": "结论",
        },
        "sections": [
            ("why-no-single-federal-law", "美国为什么没有一部统一的 AI 联邦法？",
             """<p>美国的监管路径与欧盟不同。欧盟选择了横向立法，一部《AI 法案》覆盖所有行业；美国则沿用分部门监管的传统——金融服务由消费者金融保护局与联邦贸易委员会约束，医疗由卫生与公众服务部约束，招聘由平等就业机会委员会约束。没有一部统一法典，也没有一个统一监管机构。</p>
<p>这带来一个直接后果：同一个 AI 系统可能同时落入三套规则。一个用于信贷审批的模型，既要满足信贷领域的公平 lending 要求，又要满足州层面的自动化决策披露要求，还要符合联邦贸易委员会关于算法公平的一般性执法立场。</p>
<p>对跨国企业而言，务实做法是取最严标准。为每个用例列出所有适用的规则，然后按最严格的一条执行——与其为每个辖区维护一套不同流程，不如建立一套可覆盖最高要求的基线。</p>""",
             "关键要点"),
            ("state-laws-setting-the-bar", "哪些州在设定实际的合规门槛？",
             """<p>科罗拉多州的人工智能法案聚焦面向消费者的自动化决策，要求企业在做出重大影响决策时提供说明、纠正机会与人工复核通道。它确立了"重大影响决策"这个关键概念，后续多个州的立法都在沿用类似的界定方式。</p>
<p>加利福尼亚州的路径略有不同，重点放在自动化决策工具的合规要求与前沿模型开发者的透明度义务上。得克萨斯州与犹他州则更偏向披露导向——要求企业在特定场景下告知用户正在与 AI 交互，并对政府使用 AI 设置限制。</p>
<p>值得注意的是趋同趋势。虽然条文各异，但"告知、说明、人工复核、留痕"这四项要求已经反复出现。按这四项建设能力，比逐州跟踪条文差异更稳健。</p>""",
             "关键要点"),
            ("what-regulators-actually-ask-for", "监管到场时究竟会问什么？",
             """<p>执法实践显示，监管的关注点高度集中在三件事上。第一，你能不能列出所有在用的人工智能系统，以及每个系统的用途与风险等级。第二，你能不能说明某个具体决策是怎么产生的——用了哪些数据、什么逻辑、谁批准上线。第三，出事之后你能不能追溯到当时的完整上下文。</p>
<p>第二点最难。很多企业部署了模型，却没有记录模型版本、训练数据快照与上线审批链。等到监管询问时，只能口头描述，无法提供证据。缺失的不是政策，而是可审计的技术记录。</p>
<p>因此合规工程的核心任务是建立证据链：模型清单、版本化的训练数据、决策留痕、以及定期的偏差测试结果。这些能力同时也是良好的工程实践，投入并不浪费。</p>""",
             "关键要点"),
            ("risk-tiers-for-ai-use-cases", "高风险用例与一般用例的合规要求有何不同？",
             """<p>并非所有 AI 用例承担同等义务。判断是否属于高风险，通常看两个维度：决策后果的严重程度，以及人工介入的实质程度。影响信贷、招聘、医疗、住房等重大利益且缺乏有效人工复核的自动化决策，几乎总是被归入高风险。</p>
<p>高风险用例通常需要四项额外能力：决策前的影响评估、面向个人的说明机制、纠正与申诉通道、以及定期的偏差测试。一般用例——例如内部文档摘要、会议纪要整理——通常只需基本的透明度与人工监督。</p>
<p>分级必须由业务负责人确认，而不是由技术团队自行判断。同一套模型在不同业务场景下的风险等级可能完全不同，只有掌握业务后果的人才能做出准确判断。</p>""",
             "关键要点"),
            ("governing-vendor-ai-features", "供应商提供的 AI 功能该怎么管？",
             """<p>企业使用的 AI 能力，越来越多来自现有供应商的内置功能，而不是自研模型。这类"嵌入式 AI"最容易被治理体系漏掉，因为它不是以项目形式立项的，只是某个软件版本更新后多了一个开关。</p>
<p>管理方法是在采购与续约流程中增加一个 AI 功能清单：该产品的哪些功能由模型驱动、模型处理哪些数据、数据是否被用于供应商的模型训练、以及能否关闭。这四项必须书面确认，而不是依赖销售人员的口头答复。</p>
<p>同时要建立变更监控。供应商更新功能或替换底层模型时，风险等级可能变化。把供应商的产品更新日志纳入季度合规审查的输入，比事后发现要主动得多。</p>""",
             "关键要点"),
            ("building-a-compliance-cadence", "合规工作应该以什么节奏运行？",
             """<p>一次性合规评估很快就会过期。模型会更新，数据分布会漂移，供应商会替换底层模型。合理的节奏是季度审查加事件触发：每季度复核一次模型清单与风险评级，每次重大模型更新或供应商变更后触发一次专项评估。</p>
<p>审查必须包含偏差测试。针对受保护特征分组比较错误率与通过率，是监管最常要求、也最容易发现问题的一种检查。把测试做成自动化任务，每次模型更新后自动运行并归档结果，比人工抽查可靠得多。</p>
<p>最后要明确责任人。合规不能挂在"AI 治理委员会"这样一个集体名下，每个在用的系统都必须有一个具名的业务负责人，对风险评级、文档完整性与整改时限负责。</p>""",
             "关键要点"),
        ],
        "faq": [
            ("美国是否有一部企业必须遵守的联邦 AI 法？",
             "目前没有。2026 年的美国监管格局仍然由分部门监管机构、各州立法与执法行动共同构成，而非一部统一的联邦法典。务实的做法是为每个 AI 用例梳理适用的规则，并满足其中最严格的一条。"),
            ("哪些州在设定 AI 合规门槛？",
             "科罗拉多州、加利福尼亚州、得克萨斯州与犹他州走得最远。科罗拉多针对面向消费者的自动化决策，加州覆盖自动化决策工具与前沿模型透明度，两者共同构成了其他州效仿的模板。"),
            ("蜂启咨询如何帮助企业保持合规？",
             "蜂启咨询把 MCP 驱动的对话式分析与企业 AI 咨询结合，建立血缘、文档与访问控制，把 AI 治理政策转化成监管可以实际审查的证据。"),
        ],
        "excerpts": [
            "以語義層與治理框架為底座，說明企業 AI 平台該如何建立可問責的治理機制。",
            "從資料血緣自動化出發，解釋信任如何成為分析規模化的前提。",
            "拆解對話式 BI 的選型框架，協助買方在六個支柱上做可驗證的比較。",
        ],
    },
}

SPECS = {
    "vector-embeddings-enterprise-search": VECTOR_EMBEDDINGS,
    "cross-border-data-governance-framework": CROSS_BORDER,
    "ai-regulation-united-states-2026": AI_REGULATION,
}
