# -*- coding: utf-8 -*-
"""Slug 10: state-enterprise-llm-deployment-china — EN expand+interrogative+FAQ rebuild; zh full rewrite."""
import sys, re
sys.path.insert(0, "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline/tmp")
from common import (load, save, rep1, re_dl, build_faq_list, build_jsonld,
                    body_h1, fill_excerpts, integrity, FAQ_RX, JSONLD_RX)

W = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/"
EN = W + "blog/articles/state-enterprise-llm-deployment-china.html"
ZHCN = W + "zh-cn/blog/articles/state-enterprise-llm-deployment-china.html"
ZHTW = W + "zh-tw/blog/articles/state-enterprise-llm-deployment-china.html"

# ---------------- EN ----------------
EN_FAQ = [
    ("What is the current state of LLM deployment among Chinese SOEs?",
     "Deployment has moved from pilots to mandated rollout. SASAC's February 2024 \"AI+\" special action directs central SOEs to build industry-specific AI capabilities, with operational deployment targets through 2027. More than 300 domestic LLMs — Baidu's Ernie, Alibaba's Qwen, Tencent's Hunyuan, Huawei's Pangu — are registered with the Cyberspace Administration of China, and IDC forecasts China's AI spending will exceed USD 38 billion by 2027. The dominant use cases are document intelligence, knowledge management, customer service, operational optimisation, and compliance."),
    ("How do SOEs keep data inside China while still deploying AI?",
     "By localising everything that touches data: run the LLM on domestic cloud infrastructure or on-premises, keep MCP servers inside the enterprise network so data is queried in place and only pre-formatted results move, enforce access through a semantic layer with row- and role-level security, and log every interaction for audit. The chat bot employees talk to never receives raw records — only the synthesised answer. Sovereignty is preserved by architecture, not by policy documents."),
    ("Why has MCP become central to SOE AI integration?",
     "Because it delivers vendor neutrality at the integration layer. An SOE can pair one vendor's LLM for language understanding, a domestic cloud for deployment, and a conversational BI layer from a specialist partner — connecting all components through MCP connectors without lock-in. MCP is open-sourced, adopted by the major model vendors, and its SDKs see tens of millions of downloads a month. MCP servers deployed locally keep every query inside the enterprise's controlled environment."),
    ("How quickly can an SOE see value from conversational BI?",
     "Weeks, not years. Because a managed conversational BI layer connects to existing data sources rather than waiting for warehouse modernisation, the first use case — typically document intelligence or knowledge Q&A — can go live inside the IM platform employees already use within 4-8 weeks. Organisations that then execute the phased roadmap report meeting SASAC targets while delivering measurable operational improvements within 12-18 months."),
]

EN_TOC = [
    ("the-scale-of-soe-ai-transformation", "What Is the Scale of SOE AI Transformation in China?"),
    ("mcp-and-domestic-platform-integration", "How Does MCP Enable Domestic Platform Integration?"),
    ("conversational-bi-for-soe-decision-making", "Why Is Conversational BI Central to SOE Decision-Making?"),
    ("how-can-soes-deploy-llms-without-compromising-data-sovereignty", "How Can SOEs Deploy LLMs Without Compromising Data Sovereignty?"),
    ("how-do-you-measure-success-and-demonstrate-roi", "How Do You Measure Success and Demonstrate ROI?"),
    ("what-are-the-common-pitfalls-and-how-do-you-avoid-them", "What Are the Common Pitfalls and How Do You Avoid Them?"),
    ("implementation-roadmap-for-soes", "How Should SOEs Sequence Their Implementation Roadmap?"),
]

EN_TLDR = '<div class="article-tldr"><strong>Key Statistics:</strong> IDC forecasts China\'s AI spending will exceed USD 38 billion by 2027, and state-owned enterprises are a large share of that investment. SASAC\'s February 2024 "AI+" special action mandates industry-specific AI across central SOEs, more than 300 domestic LLMs are registered with the Cyberspace Administration of China, and McKinsey\'s State of AI research finds 72% of organisations worldwide now use AI in at least one business function. The deployment pattern that works: domestic models, MCP-based standardised integration, governed semantics, and answers delivered inside the IM tools employees already use.</div>'

EN_P_SCALE = 'The spending behind the mandate is already visible. IDC forecasts China\'s AI spending will exceed USD 38 billion by 2027, and SOEs — with their procurement scale and policy alignment — are a large share of it. That spend flows through a different channel than Western enterprise IT budgets: it follows five-year plans, SASAC assessment criteria, and sector-level pilot programmes, which means vendors and integration partners are selected for sovereign capability and standards alignment, not just model benchmarks. For technology leaders, the practical reading is that the SOE market rewards those who can operate inside its constraints — domestic platforms, in-country data, IM-native delivery — rather than those who ask it to bend.'

EN_P_MCP = 'Adoption discipline matters as much as protocol choice. SOEs evaluating MCP-based integration should insist on three things: connectors for the legacy systems that actually hold the data — ERP, OA, sector-specific platforms — not just modern SaaS; deployment options that keep servers inside the enterprise network so sovereignty is architectural; and a connector roadmap that survives model churn, so swapping Ernie for Qwen or Pangu does not mean rebuilding the integration layer. Vendors who demonstrate all three win pilots; vendors who demo a chatbot without them win nothing.'

EN_P_CONVBI = 'Rollout should follow the communication fabric, not fight it. Because WeChat Work, DingTalk, and Feishu are where SOE work already happens, the conversational BI layer deploys as bots inside those platforms — same interface, same notifications, same approval threads. Adoption follows familiarity: employees who would never open a BI portal ask questions in the chat thread they already live in, and the semantic layer underneath ensures that the answer they get is the governed, permissioned, definitionally consistent one. Deployment in weeks, adoption in days — that asymmetry is the argument for conversational delivery.'

EN_NEW_SECTIONS = '''<h2 id="how-do-you-measure-success-and-demonstrate-roi">How Do You Measure Success and Demonstrate ROI?</h2>
<p>Measure the programme at three levels. Operational: document-processing cycle time for regulatory filings and internal reports, first-contact resolution in AI-assisted customer service, and the share of employee questions answered conversationally rather than through report requests. Adoption: weekly active users of the IM bots and the ratio of questions answered on first ask — a direct read on semantic-layer quality. Business: hours returned to knowledge workers, compliance-reporting preparation time, and the cost avoided by not standing up parallel data platforms for every initiative. Each metric needs a pre-deployment baseline, or the ROI story collapses into anecdote.</p>
<p>The ROI argument for SOEs is unusually clean because the mandate already exists: SASAC targets make deployment a given, so the comparison is not "AI versus nothing" but "well-architected AI versus scattered pilots." Organisations that standardise the integration layer and semantic layer once report that every subsequent use case inherits the foundations — the third deployment costs a fraction of the first. That compounding is the real return, and it is only visible if the measurement framework survives beyond the first press release.</p>
<h2 id="what-are-the-common-pitfalls-and-how-do-you-avoid-them">What Are the Common Pitfalls and How Do You Avoid Them?</h2>
<p>The most common failure is model-first procurement: selecting an LLM before mapping the data architecture, then discovering that sovereignty rules and legacy fragmentation — not model quality — determine whether anything ships. The second is dashboard-first delivery: standing up BI portals nobody opens because the workforce communicates in IM, not portals. The third is semantic drift: letting each subsidiary define "operational efficiency" its own way until cross-enterprise reporting becomes unverifiable. The fourth is treating compliance as paperwork rather than architecture, so audit trails are reconstructed after the fact. Each is avoided by the same sequence: integration layer first, semantic layer second, conversational delivery third — with every answer attributable, permissioned, and logged from day one.</p>
'''

def process_en():
    s = load(EN)
    h1 = body_h1(s)
    assert "LLM" in h1 or "State" in h1, "wrong file? h1=" + h1
    if 'What Is the Scale of SOE AI Transformation in China?' in s:
        print("EN already processed, skip")
        return
    # 1) add tldr after Key Insight paragraph
    anchor = 'SOEs are a large share of that spend.</p>'
    assert s.count(anchor) == 1
    s = s.replace(anchor, anchor + '\n' + EN_TLDR)
    # 2) H2 interrogative conversions (keep ids)
    s = rep1(s, '<h2 id="the-scale-of-soe-ai-transformation">The Scale of SOE AI Transformation</h2>',
             '<h2 id="the-scale-of-soe-ai-transformation">What Is the Scale of SOE AI Transformation in China?</h2>', 'h2-1')
    s = rep1(s, '<h2 id="mcp-and-domestic-platform-integration">MCP and Domestic Platform Integration</h2>',
             '<h2 id="mcp-and-domestic-platform-integration">How Does MCP Enable Domestic Platform Integration?</h2>', 'h2-2')
    s = rep1(s, '<h2 id="conversational-bi-for-soe-decision-making">Conversational BI for SOE Decision-Making</h2>',
             '<h2 id="conversational-bi-for-soe-decision-making">Why Is Conversational BI Central to SOE Decision-Making?</h2>', 'h2-3')
    s = rep1(s, '<h2 id="implementation-roadmap-for-soes">Implementation Roadmap for SOEs</h2>',
             '<h2 id="implementation-roadmap-for-soes">How Should SOEs Sequence Their Implementation Roadmap?</h2>', 'h2-4')
    # 3) section appends
    a1 = 'the foundation everything else stands on.</p>'
    assert s.count(a1) == 1
    s = s.replace(a1, a1 + '\n<p>' + EN_P_SCALE + '</p>')
    a2 = 'not an optional enhancement.</p>'
    assert s.count(a2) == 1
    s = s.replace(a2, a2 + '\n<p>' + EN_P_MCP + '</p>')
    a3 = 'every data point sourced.</p>'
    assert s.count(a3) == 1
    s = s.replace(a3, a3 + '\n<p>' + EN_P_CONVBI + '</p>')
    # 4) insert new sections before roadmap H2
    road = '<h2 id="implementation-roadmap-for-soes">How Should SOEs Sequence Their Implementation Roadmap?</h2>'
    assert s.count(road) == 1
    s = s.replace(road, EN_NEW_SECTIONS + road)
    # 5) remove head FAQPage
    s = re_dl(s, JSONLD_RX, '', 'head-faqpage-remove')
    # 6) rebuild FAQ list
    new_faq = '<div class="faq-list">\n' + build_faq_list(EN_FAQ) + '\n                </div>\n            </section>'
    s = re_dl(s, FAQ_RX, new_faq.replace('\\', '\\\\'), 'faq-list')
    old_nav = '</section>\n\n            <nav class="article-nav"'
    assert s.count(old_nav) == 1
    s = s.replace(old_nav, '</section>\n' + build_jsonld(EN_FAQ) + '\n\n            <nav class="article-nav"')
    # 7) TOC sync
    mob = "\n".join(f'                    <a href="#{i}" class="toc-mobile-link">{t}</a>' for i, t in EN_TOC)
    s = re_dl(s, r'<div class="toc-mobile-links">.*?</div>', '<div class="toc-mobile-links">\n' + mob + '\n                </div>', 'toc-mobile')
    # 8) excerpts
    s = fill_excerpts(s, [
        "How inclusive data teams catch the blind spots homogeneous hiring misses.",
        "Where the AI agent layer fits in a modern data strategy — and what to build first.",
        "A practical 2026 guide to vector databases and enterprise semantic search.",
    ], "EN-excerpt")
    integrity(s, [
        '?v=20260901', '"@type": "BlogPosting"', '"@type": "BreadcrumbList"',
        'id="how-do-you-measure-success-and-demonstrate-roi"',
        'id="what-are-the-common-pitfalls-and-how-do-you-avoid-them"',
        'What Is the Scale of SOE AI Transformation in China?',
        '"@type": "FAQPage"', 'Book a Demo', '38 billion',
    ], 7, "EN")
    assert "LLM" in body_h1(s) or "State" in body_h1(s)
    assert s[:s.index('</head>')].count('FAQPage') == 0
    save(EN, s)
    print("EN done")

# ---------------- zh-CN ----------------
CN_FAQ = [
    ("中国国企的大模型部署现状如何？",
     "部署已从试点走向全面铺开。国资委2024年2月的\"AI+\"专项行动要求中央国企构建行业专用AI能力，并在2027年前落地运营部署。超过300个国产大模型——百度的文心、阿里通义千问、腾讯混元、华为盘古——已在网信办备案，IDC预测到2027年中国AI支出将超过380亿美元。主导用例是文档智能、知识管理、客户服务、运营优化与合规。"),
    ("国企如何在部署AI的同时确保数据留在境内？",
     "办法是把一切触达数据的环节本地化：大模型部署在国产云或本地环境；MCP服务器运行在企业内网，数据就地查询、只有预格式化的结果向外移动；通过带行级与角色级权限的语义层控制访问；所有交互记录日志以供审计。员工对话的聊天机器人永远接触不到原始记录——只拿到带支撑数字的综合答案。主权由架构保障，而非由文件承诺。"),
    ("为什么MCP成为国企AI集成的核心标准？",
     "因为它在集成层提供了供应商中立性。国企可以让一家厂商的大模型负责语言理解、国产云负责部署、专业伙伴的对话式BI层负责交付——所有组件通过MCP连接器打通，集成层不被锁定。MCP开源、获主要模型厂商采纳，其SDK每月下载量以千万计。本地部署的MCP服务器让每一次查询都留在企业可控环境之内。"),
    ("国企从对话式BI中获得价值需要多长时间？",
     "以周计，而非以年计。托管对话式BI层直接连接现有数据源，无需等待数仓现代化，第一个用例——通常是文档智能或知识问答——可在4-8周内于员工已在使用的IM平台上线。随后按路线图分阶段推进的组织，报告在12-18个月内既达成国资委目标、又取得可衡量的运营改善。"),
]

CN_TOC = [
    ("国企ai转型的规模", "国企AI转型的规模有多大？"),
    ("mcp如何实现国产平台集成", "MCP如何实现国产平台集成？"),
    ("为什么对话式bi对国企决策至关重要", "为什么对话式BI对国企决策至关重要？"),
    ("如何在不牺牲数据主权的前提下部署大模型", "国企如何在不牺牲数据主权的前提下部署大模型？"),
    ("如何衡量成功并展示投资回报", "如何衡量成功并展示投资回报？"),
    ("常见陷阱及规避方法", "常见陷阱有哪些，如何规避？"),
    ("如何规划国企ai实施路线图", "如何规划国企AI实施路线图？"),
]

CN_BODY = '''<p class="article-lead"><strong>中国国企正在运转全球最大规模的企业AI部署之一——而且完全按照自己的规则运转：13万余家国企贡献了约30%的GDP，转型规模无可匹敌，附带硬性要求——数据留在境内、模型运行在国产平台、每一次部署都要同时服务商业目标与政策优先级。</strong>答案不是整体引进西方AI技术栈，而是国产大模型、标准化集成层与员工已在使用的IM工具内对话式交付的组合。本文拆解这一部署模式。</p>
<div class="article-tldr"><p><strong>核心要点：</strong>IDC预测到2027年中国AI支出将超过380亿美元，国企占其中很大份额；国资委2024年2月的"AI+"专项行动要求中央国企构建行业专用AI能力；超过300个国产大模型已在网信办备案；麦肯锡State of AI研究显示72%的全球组织已在至少一个业务职能中使用AI。行得通的部署模式：国产模型、基于MCP的标准化集成、受治理的语义层、以及在员工已在使用的IM工具内交付答案。</p></div>
<h2 id="国企ai转型的规模">国企AI转型的规模有多大？</h2>
<p>中国国企部门横跨能源、电信、银行、交通与制造业，企业数量超过13万家，政府与学术估算其经济贡献约占GDP的30%。国资委已发布指令，要求数字化转型与AI采用全面提速，并为2027年前在运营流程中部署AI设定了具体目标。2024年2月国资委"AI+"专项行动的启动让方向再无歧义：中央国企被期待构建并部署行业专用AI能力——从基于行业数据训练的大模型到覆盖全企业的AI辅助运营。</p>
<p>用例集中五大类。文档智能居首——国企产生并消化海量监管申报、内部报告与政策文件，大模型自动完成摘要、分类与信息抽取。知识管理让机构知识通过对话式界面变得可及。客户服务在电信、银行与公用事业部署AI对话。运营优化将AI应用于制造、电网管理与物流。合规与风险管理用AI监控监管义务并生成合规报告。这些都不需要奇异的技术——它们需要可靠地访问正确的数据，并交付到人们工作的地方。</p>
<p>数据架构才是国企部署的难点所在。数十年沉淀的遗留系统、格式与口径不一致的分布式数据、以及要求境内处理并运行在国产平台的数据主权规则，共同指向一个结论：标准化集成比模型选型更重要。一个抽象遗留复杂性的统一集成层、同时通过本地部署满足主权要求，是其余一切的地基。</p>
<p>授权背后的支出已经清晰可见。IDC预测到2027年中国AI支出将超过380亿美元，而凭借采购规模与政策对齐，国企占了其中很大份额。这笔支出走的渠道与西方企业IT预算不同：它跟随五年规划、国资委考核标准与行业级试点项目，这意味着厂商与集成伙伴的遴选标准是主权能力与标准对齐，而不仅是模型跑分。对技术决策者，实际的解读是：这个市场奖励能在其约束之内运营者——国产平台、境内数据、IM原生交付——而不是要求市场迁就自己的人。</p>
<h2 id="mcp如何实现国产平台集成">MCP如何实现国产平台集成？</h2>
<p>中国企业AI生态正围绕国产平台构建。基础模型来自百度（文心）、阿里（通义千问）、腾讯（混元）与华为（盘古）——网信办已备案超过300个面向公众服务的国产大模型，让国企在模型层拥有真实的选择权。云基础设施来自阿里云、华为云与腾讯云。缺的是把这些模型连接到企业数据的标准化方式——这正是模型上下文协议（MCP）成为核心的原因。MCP由Anthropic于2024年末开源、数月内获OpenAI与Google采纳，正迅速成为集成标准；其SDK每月全球下载量以千万计。</p>
<p>对国企而言，MCP的价值在于供应商中立。一家国企可以让百度大模型负责自然语言理解、华为云负责部署、再加一层来自专业伙伴（如Beehive Strategy）的对话式BI，全部组件通过MCP连接器打通——集成层不被任何一家锁定。在既偏好国产厂商又要求互操作性的采购政策下，这种灵活性至关重要。而且MCP服务器可以本地部署，数据留在企业可控环境之内——主权由架构保障，而非由文件承诺。</p>
<p>交付同样受到约束：企业微信、钉钉与飞书主导着国企的沟通场景，AI能力必须经由这些平台触达员工才能实现采纳。聊天线程里给出的答案会被使用；需要另开一个应用的仪表盘不会。这正是IM原生对话式接口成为国企AI部署模式、而非可选增强的原因。</p>
<p>采用纪律与协议选择同样重要。评估基于MCP的集成时，国企应坚持三点：连接真正承载数据的遗留系统——ERP、OA、行业专用平台——而非只连接现代SaaS的连接器；保持服务器在企业内网运行的部署选项，让主权成为架构属性；以及能扛住模型更替的连接器路线图——从文心换到通义或盘古不需要重建集成层。三条全占的厂商赢得试点；只演示一个聊天机器人的厂商什么都赢不到。</p>
<h2 id="为什么对话式bi对国企决策至关重要">为什么对话式BI对国企决策至关重要？</h2>
<p>国企的决策结构塑造了对话式BI的设计方式。权力分布于多个管理层级，审批流程同时涉及商业与政策考量，汇报必须同时对齐商业目标与政策优先级。面向国企的对话式BI层因此必须提供：分角色的数据访问——不同管理层看到不同数据；政策感知的分析——把洞察放在相关指令的语境中呈现；以及审批工作流集成——让数据驱动的建议流入既有流程而非绕开它。</p>
<p>语义层在这里分量尤其重，因为国企术语横跨商业与政策两个域。"运营效率"对商业化子公司和政策驱动的母公司可能含义不同；区域经营又在术语与口径上叠加更多差异。治理良好的语义层一致地消解这些差异——同一个问题在每一个团队得到同一个定义、同一组数字、同样的注意事项。它还提供监管者与审计者期望的审计轨迹：每一次查询可归因、每一个答案可解释、每一个数据点可溯源。</p>
<p>推广应沿沟通结构展开，而非与之对抗。因为企业微信、钉钉与飞书本就是国企工作发生的场所，对话式BI层以这些平台内的机器人形态部署——同样的界面、同样的通知、同样的审批线程。采纳来自熟悉：从不打开BI门户的员工，会在已经驻留的聊天线程里提问，而底层的语义层保证他们得到的答案是受治理、有权限、口径一致的。以周计的部署、以天计的采纳——这种不对称正是对话式交付的论据。</p>
<h2 id="如何在不牺牲数据主权的前提下部署大模型">国企如何在不牺牲数据主权的前提下部署大模型？</h2>
<p>简短的回答是：把一切触达数据的环节本地化。把大模型部署在国产云基础设施或本地环境；让MCP服务器运行在企业网络之内，数据就地查询、只有预格式化的结果向外移动；通过带行级与角色级权限的语义层控制访问；并为每一次交互记录审计日志。员工对话的聊天机器人永远接触不到原始记录——只拿到带支撑数字的综合答案。这与全球银行在受监管环境中使用的模式相同，并直接映射到中国的主权要求之上。</p>
<p>实际结果是，"主权AI"与"快速部署"并不冲突。因为集成层标准化了对遗留系统的访问，国企无需先重建数仓，AI就能回答问题。托管对话式BI部署可以连接现有数据源、通过语义层执行策略、在数周内交付价值——而多年的平台现代化按自己的节奏推进。主权在架构层得到满足，价值即刻抵达。</p>
<h2 id="如何衡量成功并展示投资回报">如何衡量成功并展示投资回报？</h2>
<p>在三个层级上衡量项目。运营层：监管申报与内部报告的文档处理周期、AI辅助客服的首次解决率、以及以对话方式（而非报表申请）得到解答的员工问题占比。采纳层：IM机器人的周活跃用户数，以及首次提问即得到回答的比例——这是语义层质量的直接读数。业务层：知识工作者被释放的小时数、合规报告的准备耗时、以及不为每个专项另建平行数据平台所避免的成本。每个指标都需要部署前的基线，否则ROI故事会退化成轶事。</p>
<p>国企的ROI论证格外干净，因为授权已然存在：国资委目标让部署成为定局，所以比较的不是"有AI还是没AI"，而是"架构良好的AI"与"分散的试点"。一次性标准化集成层与语义层的组织报告说，后续每个用例都继承地基——第三次部署的成本只是第一次的零头。这种复利才是真正的回报，而它只有在测量框架活过第一份新闻稿之后才可见。</p>
<h2 id="常见陷阱及规避方法">常见陷阱有哪些，如何规避？</h2>
<p>最常见的失败是模型优先的采购：先选大模型、后测绘数据架构，然后发现决定能否落地的其实是主权规则与遗留系统碎片化，而非模型质量。第二个是仪表盘优先的交付：搭建了无人打开的BI门户，因为员工的沟通发生在IM而非门户。第三个是语义漂移：放任每家子公司自行定义"运营效率"，直到跨企业汇报无从核验。第四个是把合规当文案而非架构，审计轨迹事后补录。每一个都由同一个顺序规避：集成层先行、语义层其次、对话式交付第三——并且从第一天起，每个答案都可归因、有权限、有日志。</p>
<h2 id="如何规划国企ai实施路线图">如何规划国企AI实施路线图？</h2>
<p>国企应按国资委指令对齐的三阶段推进AI转型。第一阶段聚焦文档智能与知识管理——影响最大、风险最低的用例，快速证明价值并建立用户信心。第二阶段扩展到客户服务与运营优化，它们要求与运营系统和实时数据集成。第三阶段处理合规与风险管理——数据集成与治理要求最复杂的用例。贯穿所有阶段：标准化连接器提供数据访问，语义层执行一致的口径与权限，对话式BI把结果经既有IM平台送达。</p>
<p>麦肯锡State of AI研究发现，全球72%的组织已在至少一个业务职能中使用AI——而中国国企从试验转向全面铺开的速度几乎快于任何其他板块。把这条路线图执行好的组织，报告在12-18个月内既达成国资委目标、又取得可衡量的运营改善。模式已被验证：国产模型、标准化集成、受治理的语义层、以及把答案送达工作真正发生的聊天线程。对中国国有部门而言，这不只是一套AI战略——这是未来十年企业技术的运营模型。</p>
<section class="faq-section" id="faq" aria-label="常见问题">
    <h2 class="faq-section-title">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        常见问题
    </h2>
<div class="faq-list">
{FAQ_LIST}
</div>
</section>
{JSONLD}'''

def process_cn():
    s = load(ZHCN)
    h1 = body_h1(s)
    assert '国企' in h1 or '部署' in h1, "wrong file? h1=" + h1
    if 'id="mcp如何实现国产平台集成"' in s:
        print("CN already processed, skip")
        return
    body = CN_BODY.replace('{FAQ_LIST}', build_faq_list(CN_FAQ)).replace('{JSONLD}', build_jsonld(CN_FAQ))
    n = len(re.findall(r'<p class="article-lead">.*?(?=\n\n            <nav class="article-nav")', s, re.S))
    assert n == 1, f"CN body span: {n}"
    s = re.sub(r'<p class="article-lead">.*?(?=\n\n            <nav class="article-nav")',
               lambda m: body, s, count=1, flags=re.S)
    mob = "\n".join(f'                    <a href="#{o}" class="toc-mobile-link">{t}</a>' for o, t in CN_TOC)
    def mob_repl(m):
        return '<div class="toc-mobile-links">\n' + mob + '\n                </div>'
    s2 = re.sub(r'<div class="toc-mobile-links">.*?</div>', mob_repl, s, count=1, flags=re.S)
    assert s2 != s, "cn toc replace failed"
    s = s2
    if 'recommended-card-excerpt"></p>' in s:
        s = fill_excerpts(s, [
            "对话式BI把国企的数据查询变成聊天里的一次提问。",
        ], "CN-excerpt")
    integrity(s, [
        '?v=20260901', '预约演示', '"@type": "FAQPage"',
        'id="国企ai转型的规模"', 'id="mcp如何实现国产平台集成"',
        'id="如何在不牺牲数据主权的前提下部署大模型"', '380亿', '托管对话式BI',
    ], 7, "zh-CN")
    assert '国企' in body_h1(s) or '部署' in body_h1(s)
    save(ZHCN, s)
    print("CN done")

# ---------------- zh-TW ----------------
TW_FAQ = [
    ("中國國企的大模型部署現況如何？",
     "部署已從試點走向全面鋪開。國資委2024年2月的「AI+」專項行動要求中央國企構建行業專用AI能力，並在2027年前落地營運部署。超過300個國產大模型——百度的文心、阿里通義千問、騰訊混元、華為盤古——已在網信辦備案，IDC預測到2027年中國AI支出將超過380億美元。主導用例是文檔智能、知識管理、客戶服務、營運優化與合規。"),
    ("國企如何在部署AI的同時確保資料留在境內？",
     "辦法是把一切觸達資料的環節在地化：大模型部署在國產雲或本地環境；MCP伺服器運行在企業內網，資料就地查詢、只有預格式化的結果向外移動；透過帶列級與角色級權限的語義層控制存取；所有互動記錄日誌以供稽核。員工對話的聊天機器人永遠接觸不到原始記錄——只拿到帶支撐數字的綜合答案。主權由架構保障，而非由文件承諾。"),
    ("為什麼MCP成為國企AI整合的核心標準？",
     "因為它在整合層提供了供應商中立性。國企可以讓一家廠商的大模型負責語言理解、國產雲負責部署、專業夥伴的對話式BI層負責交付——所有元件透過MCP連接器打通，整合層不被鎖定。MCP開源、獲主要模型廠商採納，其SDK每月下載量以千萬計。本地部署的MCP伺服器讓每一次查詢都留在企業可控環境之內。"),
    ("國企從對話式BI中獲得價值需要多長時間？",
     "以週計，而非以年計。託管對話式BI層直接連接現有資料源，無需等待資料倉儲現代化，第一個用例——通常是文檔智能或知識問答——可在4-8週內於員工已在使用的IM平台上線。隨後按路線圖分階段推進的組織，報告在12-18個月內既達成國資委目標、又取得可衡量的營運改善。"),
]

TW_TOC = [
    ("國企ai轉型的規模", "國企AI轉型的規模有多大？"),
    ("mcp如何實現國產平台整合", "MCP如何實現國產平台整合？"),
    ("為什麼對話式bi對國企決策至關重要", "為什麼對話式BI對國企決策至關重要？"),
    ("如何在不犧牲資料主權的前提下部署大模型", "國企如何在不犧牲資料主權的前提下部署大模型？"),
    ("如何衡量成功並展示投資回報", "如何衡量成功並展示投資回報？"),
    ("常見陷阱及規避方法", "常見陷阱有哪些，如何規避？"),
    ("如何規劃國企ai實施路線圖", "如何規劃國企AI實施路線圖？"),
]

TW_BODY = '''<p class="article-lead"><strong>中國國企正在運轉全球最大規模的企業AI部署之一——而且完全按照自己的規則運轉：13萬餘家國企貢獻了約30%的GDP，轉型規模無可匹敵，附帶硬性要求——資料留在境內、模型運行在國產平台、每一次部署都要同時服務商業目標與政策優先級。</strong>答案不是整體引進西方AI技術棧，而是國產大模型、標準化整合層與員工已在使用的IM工具內對話式交付的組合。本文拆解這一部署模式。</p>
<div class="article-tldr"><p><strong>核心要點：</strong>IDC預測到2027年中國AI支出將超過380億美元，國企佔其中很大份額；國資委2024年2月的「AI+」專項行動要求中央國企構建行業專用AI能力；超過300個國產大模型已在網信辦備案；麥肯錫State of AI研究顯示72%的全球組織已在至少一個業務職能中使用AI。行得通的部署模式：國產模型、基於MCP的標準化整合、受治理的語義層、以及在員工已在使用的IM工具內交付答案。</p></div>
<h2 id="國企ai轉型的規模">國企AI轉型的規模有多大？</h2>
<p>中國國企部門橫跨能源、電信、銀行、交通與製造業，企業數量超過13萬家，政府與學術估算其經濟貢獻約佔GDP的30%。國資委已發布指令，要求数位轉型與AI採用全面提速，並為2027年前在營運流程中部署AI設定了具體目標。2024年2月國資委「AI+」專項行動的啟動讓方向再無歧義：中央國企被期待構建並部署行業專用AI能力——從基於行業資料訓練的大模型到覆蓋全企業的AI輔助營運。</p>
<p>用例集中五大類。文檔智能居首——國企產生並消化海量監管申報、內部報告與政策文件，大模型自動完成摘要、分類與資訊抽取。知識管理讓機構知識透過對話式介面變得可及。客戶服務在電信、銀行與公用事業部署AI對話。營運優化將AI應用於製造、電網管理與物流。合規與風險管理用AI監控監管義務並生成合規報告。這些都不需要奇異的技術——它們需要可靠地存取正確的資料，並交付到人們工作的地方。</p>
<p>資料架構才是國企部署的難點所在。數十年沉澱的遺留系統、格式與口徑不一致的分散式資料、以及要求境內處理並運行在國產平台的資料主權規則，共同指向一個結論：標準化整合比模型選型更重要。一個抽象遺留複雜性的統一整合層、同時透過本地部署滿足主權要求，是其餘一切的地基。</p>
<p>授權背後的支出已經清晰可見。IDC預測到2027年中國AI支出將超過380億美元，而憑藉採購規模與政策對齊，國企佔了其中很大份額。這筆支出走的管道與西方企業IT預算不同：它跟隨五年規劃、國資委考核標準與行業級試點專案，這意味著廠商與整合夥伴的遴選標準是主權能力與標準對齊，而不僅是模型跑分。對技術決策者，實際的解讀是：這個市場獎勵能在其約束之內營運者——國產平台、境內資料、IM原生交付——而不是要求市場遷就自己的人。</p>
<h2 id="mcp如何實現國產平台整合">MCP如何實現國產平台整合？</h2>
<p>中國企業AI生態正圍繞國產平台構建。基礎模型來自百度（文心）、阿里（通義千問）、騰訊（混元）與華為（盤古）——網信辦已備案超過300個面向公眾服務的國產大模型，讓國企在模型層擁有真實的選擇權。雲基礎設施來自阿里雲、華為雲與騰訊雲。缺的是把這些模型連接到企業資料的標準化方式——這正是模型上下文協定（MCP）成為核心的原因。MCP由Anthropic於2024年末開源、數月內獲OpenAI與Google採納，正迅速成為整合標準；其SDK每月全球下載量以千萬計。</p>
<p>對國企而言，MCP的價值在於供應商中立。一家國企可以讓百度大模型負責自然語言理解、華為雲負責部署、再加一層來自專業夥伴（如Beehive Strategy）的對話式BI，全部元件透過MCP連接器打通——整合層不被任何一家鎖定。在既偏好國產廠商又要求互操作性的採購政策下，這種靈活性至關重要。而且MCP伺服器可以本地部署，資料留在企業可控環境之內——主權由架構保障，而非由文件承諾。</p>
<p>交付同樣受到約束：企業微信、釘釘與飛書主導著國企的溝通場景，AI能力必須經由這些平台觸達員工才能實現採納。聊天對話串裡給出的答案會被使用；需要另開一個應用的儀表板不會。這正是IM原生對話式介面成為國企AI部署模式、而非可選增強的原因。</p>
<p>採用紀律與協定選擇同樣重要。評估基於MCP的整合時，國企應堅持三點：連接真正承載資料的遺留系統——ERP、OA、行業專用平台——而非只連接現代SaaS的連接器；保持伺服器在企業內網運行的部署選項，讓主權成為架構屬性；以及能扛住模型更替的連接器路線圖——從文心換到通義或盤古不需要重建整合層。三條全佔的廠商贏得試點；只演示一個聊天機器人的廠商什麼都贏不到。</p>
<h2 id="為什麼對話式bi對國企決策至關重要">為什麼對話式BI對國企決策至關重要？</h2>
<p>國企的決策結構塑造了對話式BI的設計方式。權力分佈於多個管理層級，審批流程同時涉及商業與政策考量，匯報必須同時對齊商業目標與政策優先級。面向國企的對話式BI層因此必須提供：分角色的資料存取——不同管理層看到不同資料；政策感知的分析——把洞察放在相關指令的語境中呈現；以及審批工作流整合——讓資料驅動的建議流入既有流程而非繞開它。</p>
<p>語義層在這裡分量尤其重，因為國企術語橫跨商業與政策兩個域。「營運效率」對商業化子公司和政策驅動的母公司可能含義不同；區域經營又在術語與口徑上疊加更多差異。治理良好的語義層一致地消解這些差異——同一個問題在每一個團隊得到同一個定義、同一組數字、同樣的注意事項。它還提供監管者與稽核者期望的稽核軌跡：每一次查詢可歸因、每一個答案可解釋、每一個資料點可溯源。</p>
<p>推廣應沿溝通結構展開，而非與之對抗。因為企業微信、釘釘與飛書本就是國企工作發生的場所，對話式BI層以這些平台內的機器人形態部署——同樣的介面、同樣的通知、同樣的審批對話串。採納來自熟悉：從不打開BI入口網站的員工，會在已經駐留的聊天對話串裡提問，而底層的語義層保證他們得到的答案是受治理、有權限、口徑一致的。以週計的部署、以天計的採納——這種不對稱正是對話式交付的論據。</p>
<h2 id="如何在不犧牲資料主權的前提下部署大模型">國企如何在不犧牲資料主權的前提下部署大模型？</h2>
<p>簡短的回答是：把一切觸達資料的環節在地化。把大模型部署在國產雲基礎設施或本地環境；讓MCP伺服器運行在企業網路之內，資料就地查詢、只有預格式化的結果向外移動；透過帶列級與角色級權限的語義層控制存取；並為每一次互動記錄稽核日誌。員工對話的聊天機器人永遠接觸不到原始記錄——只拿到帶支撐數字的綜合答案。這與全球銀行在受監管環境中使用的模式相同，並直接映射到中國的主權要求之上。</p>
<p>實際結果是，「主權AI」與「快速部署」並不衝突。因為整合層標準化了對遺留系統的存取，國企無需先重建資料倉儲，AI就能回答問題。託管對話式BI部署可以連接現有資料源、透過語義層執行策略、在數週內交付價值——而多年的平台現代化按自己的節奏推進。主權在架構層得到滿足，價值即刻抵達。</p>
<h2 id="如何衡量成功並展示投資回報">如何衡量成功並展示投資回報？</h2>
<p>在三個層級上衡量專案。營運層：監管申報與內部報告的文檔處理週期、AI輔助客服的首次解決率、以及以對話方式（而非報表申請）得到解答的員工問題佔比。採納層：IM機器人的週活躍使用者數，以及首次提問即得到回答的比例——這是語義層質量的直接讀數。業務層：知識工作者被釋放的小時數、合規報告的準備耗時、以及不為每個專項另建平行資料平台所避免的成本。每個指標都需要部署前的基線，否則ROI故事會退化成軼事。</p>
<p>國企的ROI論證格外乾淨，因為授權已然存在：國資委目標讓部署成為定局，所以比較的不是「有AI還是沒AI」，而是「架構良好的AI」與「分散的試點」。一次性標準化整合層與語義層的組織報告說，後續每個用例都繼承地基——第三次部署的成本只是第一次的零頭。這種複利才是真正的回報，而它只有在測量框架活過第一份新聞稿之後才可見。</p>
<h2 id="常見陷阱及規避方法">常見陷阱有哪些，如何規避？</h2>
<p>最常見的失敗是模型優先的採購：先選大模型、後測繪資料架構，然後發現決定能否落地的是主權規則與遺留系統碎片化，而非模型質量。第二個是儀表板優先的交付：搭建了無人打開的BI入口網站，因為員工的溝通發生在IM而非入口網站。第三個是語義漂移：放任每家子公司自行定義「營運效率」，直到跨企業匯報無從核驗。第四個是把合規當文案而非架構，稽核軌跡事後補錄。每一個都由同一個順序規避：整合層先行、語義層其次、對話式交付第三——並且從第一天起，每個答案都可歸因、有權限、有日誌。</p>
<h2 id="如何規劃國企ai實施路線圖">如何規劃國企AI實施路線圖？</h2>
<p>國企應按國資委指令對齊的三階段推進AI轉型。第一階段聚焦文檔智能與知識管理——影響最大、風險最低的用例，快速證明價值並建立使用者信心。第二階段擴展到客戶服務與營運優化，它們要求與營運系統和即時資料整合。第三階段處理合規與風險管理——資料整合與治理要求最複雜的用例。貫穿所有階段：標準化連接器提供資料存取，語義層執行一致的口徑與權限，對話式BI把結果經既有IM平台送達。</p>
<p>麥肯錫State of AI研究發現，全球72%的組織已在至少一個業務職能中使用AI——而中國國企從試驗轉向全面鋪開的速度幾乎快於任何其他板塊。把這條路線圖執行好的組織，報告在12-18個月內既達成國資委目標、又取得可衡量的營運改善。模式已被驗證：國產模型、標準化整合、受治理的語義層、以及把答案送達工作真正發生的聊天對話串。對中國國有部門而言，這不只是一套AI戰略——這是未來十年企業技術的營運模型。</p>
<section class="faq-section" id="faq" aria-label="常見問題">
    <h2 class="faq-section-title">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        常見問題
    </h2>
<div class="faq-list">
{FAQ_LIST}
</div>
</section>
{JSONLD}'''

def process_tw():
    s = load(ZHTW)
    h1 = body_h1(s)
    assert '國企' in h1 or '部署' in h1, "wrong file? h1=" + h1
    if 'id="mcp如何實現國產平台整合"' in s:
        print("TW already processed, skip")
        return
    body = TW_BODY.replace('{FAQ_LIST}', build_faq_list(TW_FAQ)).replace('{JSONLD}', build_jsonld(TW_FAQ))
    n = len(re.findall(r'<p class="article-lead">.*?(?=\n\n            <nav class="article-nav")', s, re.S))
    assert n == 1, f"TW body span: {n}"
    s = re.sub(r'<p class="article-lead">.*?(?=\n\n            <nav class="article-nav")',
               lambda m: body, s, count=1, flags=re.S)
    mob = "\n".join(f'                    <a href="#{o}" class="toc-mobile-link">{t}</a>' for o, t in TW_TOC)
    def mob_repl(m):
        return '<div class="toc-mobile-links">\n' + mob + '\n                </div>'
    s2 = re.sub(r'<div class="toc-mobile-links">.*?</div>', mob_repl, s, count=1, flags=re.S)
    assert s2 != s, "tw toc replace failed"
    s = s2
    if 'recommended-card-excerpt"></p>' in s:
        s = fill_excerpts(s, [
            "對話式BI把國企的資料查詢變成聊天裡的一次提問。",
        ], "TW-excerpt")
    integrity(s, [
        '?v=20260901', '預約示範', '"@type": "FAQPage"',
        'id="國企ai轉型的規模"', 'id="mcp如何實現國產平台整合"',
        'id="如何在不犧牲資料主權的前提下部署大模型"', '380億', '託管對話式BI',
    ], 7, "zh-TW")
    assert '國企' in body_h1(s) or '部署' in body_h1(s)
    save(ZHTW, s)
    print("TW done")

if __name__ == "__main__":
    process_en()
    process_cn()
    process_tw()
    print("ALL DONE")
