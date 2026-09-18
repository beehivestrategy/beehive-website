# -*- coding: utf-8 -*-
"""Slug 14: cross-functional-ai-teams-structure-and-governance-a-2026-update
EN: interrogative H2s + tldr + FAQ/JSON-LD insert + excerpts; zh full rewrite."""
import sys, re
sys.path.insert(0, "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline/tmp")
from common import (load, save, rep1, re_dl, build_faq_list, build_jsonld,
                    body_h1, fill_excerpts, integrity, FAQ_RX, JSONLD_RX)

W = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/"
S = "cross-functional-ai-teams-structure-and-governance-a-2026-update"
EN = W + "blog/articles/" + S + ".html"
ZHCN = W + "zh-cn/blog/articles/" + S + ".html"
ZHTW = W + "zh-tw/blog/articles/" + S + ".html"

# ---------------- EN ----------------
EN_FAQ = [
    ("Who should own an AI initiative — IT, data, or the business?",
     "No single function should own it outright. Delivery ownership belongs to a cross-functional product team — business, data, engineering, and design on one roadmap — while a slim central function provides platforms, standards, and guardrails. Keep the two separate: the team that sets the standards must not also be the team shipping features, or its standards quietly become optional."),
    ("How large should a cross-functional AI team be?",
     "Small enough to stay fast, complete enough to ship end-to-end. In our experience the effective core is five to nine people covering product, engineering, data, and design, with domain experts seconded in from the business. Beyond roughly ten people, coordination costs grow faster than throughput — at that point split by product line rather than grow the team."),
    ("Where should AI governance sit in the organisation?",
     "Close enough to delivery to be useful, senior enough to be binding. A quarterly governance review chaired by a senior executive, with data, risk, and compliance represented, works in most enterprises. Governance that sits too far from delivery becomes paperwork; governance without executive backing becomes a suggestion."),
    ("How often should AI governance reviews happen?",
     "Quarterly for full reviews, with a fast lane for routine decisions. Publish written decision rules so the team knows what it can approve itself, what needs the technical lead, and what must wait for the next governance review. Every review should produce a dated, reasoned decision that anyone in the organisation can find — the log is the evidence that governance is working."),
]

EN_TOC = [
    ("the-current-landscape", "What Does the 2026 Landscape for Cross-Functional AI Teams Look Like?"),
    ("who-should-own-an-ai-initiative-it-data-or-the-business", "Who Should Own an AI Initiative — IT, Data, or the Business?"),
    ("key-implementation-challenges", "What Are the Key Implementation Challenges?"),
    ("practical-approaches-that-work", "Which Practical Approaches Actually Work?"),
    ("governance-that-moves-at-the-speed-of-delivery", "How Do You Build Governance That Moves at the Speed of Delivery?"),
    ("key-takeaways", "What Are the Key Takeaways?"),
    ("conclusion", "What Should You Do Next?"),
]

EN_TLDR = '<div class="article-tldr"><strong>Key Statistics:</strong> Gartner projects that by the end of 2026 a large majority of enterprises will have moved generative AI capabilities into production. Roughly 70% of enterprise data requires significant preparation before it can support AI workloads. Organisations that invest in comprehensive change management achieve adoption rates three times higher than those that do not. The winning operating model is hybrid: a small central function setting standards, with delivery in cross-functional teams embedded in the business on a cadence of weekly delivery, monthly outcomes, and quarterly governance reviews.</div>'

FAQ_SECTION_EN = '''<section class="faq-section" id="faq" aria-label="Frequently Asked Questions">
    <h2 class="faq-section-title">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        Frequently Asked Questions
    </h2>
<div class="faq-list">
{FAQ_LIST}
</div>
</section>
{JSONLD}'''

def process_en():
    s = load(EN)
    h1 = body_h1(s)
    assert "Cross-Functional" in h1, "wrong file? h1=" + h1
    if 'What Does the 2026 Landscape' in s:
        print("EN already processed, skip")
        return
    # 1) tldr after lead
    anchor = 'governed like regulated functions.</p>'
    assert s.count(anchor) == 1
    s = s.replace(anchor, anchor + '\n' + EN_TLDR)
    # 2) H2 interrogative conversions (keep ids)
    s = rep1(s, '<h2 id="the-current-landscape">The Current Landscape</h2>',
             '<h2 id="the-current-landscape">What Does the 2026 Landscape for Cross-Functional AI Teams Look Like?</h2>', 'h2-1')
    s = rep1(s, '<h2 id="key-implementation-challenges">Key Implementation Challenges</h2>',
             '<h2 id="key-implementation-challenges">What Are the Key Implementation Challenges?</h2>', 'h2-2')
    s = rep1(s, '<h2 id="practical-approaches-that-work">Practical Approaches That Work</h2>',
             '<h2 id="practical-approaches-that-work">Which Practical Approaches Actually Work?</h2>', 'h2-3')
    s = rep1(s, '<h2 id="governance-that-moves-at-the-speed-of-delivery">Governance That Moves at the Speed of Delivery</h2>',
             '<h2 id="governance-that-moves-at-the-speed-of-delivery">How Do You Build Governance That Moves at the Speed of Delivery?</h2>', 'h2-4')
    s = rep1(s, '<h2 id="key-takeaways">Key Takeaways</h2>',
             '<h2 id="key-takeaways">What Are the Key Takeaways?</h2>', 'h2-5')
    s = rep1(s, '<h2 id="conclusion">Conclusion</h2>',
             '<h2 id="conclusion">What Should You Do Next?</h2>', 'h2-6')
    # 3) insert FAQ section + JSON-LD after conclusion tail
    tail = 'it is the organised effort around it.</p>'
    assert s.count(tail) == 1
    block = FAQ_SECTION_EN.replace('{FAQ_LIST}', build_faq_list(EN_FAQ)).replace('{JSONLD}', build_jsonld(EN_FAQ))
    s = s.replace(tail, tail + '\n' + block)
    # 4) TOC mobile sync
    mob = "\n".join(f'                    <a href="#{i}" class="toc-mobile-link">{t}</a>' for i, t in EN_TOC)
    s = re_dl(s, r'<div class="toc-mobile-links">.*?</div>', '<div class="toc-mobile-links">\n' + mob + '\n                </div>', 'toc-mobile')
    # 5) excerpts
    s = fill_excerpts(s, [
        "How inclusive data teams catch the blind spots homogeneous hiring misses.",
        "Where the AI agent layer fits in a modern data strategy — and what to build first.",
        "A practical 2026 guide to vector databases and enterprise semantic search.",
    ], "EN-excerpt")
    integrity(s, [
        '?v=20260901', '"@type": "BlogPosting"', '"@type": "BreadcrumbList"',
        'What Does the 2026 Landscape', 'What Are the Key Takeaways?',
        'What Should You Do Next?', '"@type": "FAQPage"', 'Book a Demo',
        'three times higher',
    ], 8, "EN")
    assert "Cross-Functional" in body_h1(s)
    assert s[:s.index('</head>')].count('FAQPage') == 0
    save(EN, s)
    print("EN done")

# ---------------- zh-CN ----------------
CN_FAQ = [
    ("AI项目应该由IT、数据还是业务部门主导？",
     "没有任何单一职能应该独占主导权。交付归属权属于跨职能产品团队——业务、数据、工程与设计共用一张路线图；而一个精简的中心职能提供平台、标准与护栏。两者必须分开：制定标准的团队不能同时是交付功能的团队，否则标准会悄悄变成可选项。"),
    ("跨职能AI团队的合理规模是多大？",
     "小到保持敏捷，大到能端到端交付。我们的经验是，有效的核心规模为五到九人，覆盖产品、工程、数据与设计，并由业务方借调领域专家。超过十人左右后，协调成本的增长会快过产出增长——此时应按产品线拆分团队，而不是继续扩张。"),
    ("AI治理应该放在组织的哪个位置？",
     "离交付足够近才有用，层级足够高才有约束力。在大多数企业里，由高管主持、数据、风险与合规共同参与的季度治理评审是可行的结构。离交付太远的治理会沦为文书工作；没有高管背书的治理只会沦为建议。"),
    ("AI治理评审多久进行一次？",
     "全面评审按季度进行，日常决策走快速通道。发布书面的决策规则，让团队清楚哪些可以自行批准、哪些需要技术负责人签字、哪些必须等下一次治理评审。每次评审都应产出一条注明日期、附理由、组织内任何人都能查到的决策记录——这份记录就是治理在起作用的证据。"),
]

CN_TOC = [
    ("2026年跨职能ai团队的格局是什么样的", "2026年跨职能AI团队的格局是什么样的？"),
    ("ai项目应该由谁主导it数据还是业务", "AI项目应该由谁主导——IT、数据还是业务？"),
    ("跨职能ai团队的关键实施挑战有哪些", "跨职能AI团队的关键实施挑战有哪些？"),
    ("哪些实践方法真正有效", "哪些实践方法真正有效？"),
    ("如何构建跟上交付速度的治理机制", "如何构建跟上交付速度的治理机制？"),
    ("核心要点有哪些", "核心要点有哪些？"),
    ("接下来应该怎么做", "接下来应该怎么做？"),
]

CN_BODY = '''<p class="article-lead"><strong>2026年，决定AI试点生死的不再是模型，而是组织模型。</strong>跨职能AI团队——交付AI计划的那群人的结构与治理——已经成为试点坟场与生产价值之间的分水岭。模型已经充裕，平台已经成熟，稀缺的资源是有组织的人力投入。本文剖析成功企业如何搭建AI团队、治理应该放在哪里，以及蜂启咨询的推荐做法。简短的答案是：AI是一个运营模型问题，成功的团队像产品团队一样组建、像受监管职能一样治理。</p>
<div class="article-tldr"><p><strong>核心要点：</strong>Gartner预计到2026年底，绝大多数企业将把生成式AI能力推向生产环境。约70%的企业数据需要大量治理准备才能支撑AI工作负载。投入全面变革管理的组织，采纳率高出三倍。制胜的运营模型是混合式——小型中心职能制定标准，交付由嵌入业务的跨职能团队完成，节奏为每周交付、每月复盘成果、每季度治理评审。</p></div>
<h2 id="2026年跨职能ai团队的格局是什么样的">2026年跨职能AI团队的格局是什么样的？</h2>
<p>2026年的格局由AI卓越中心垄断的瓦解定义。早期计划把AI集中在一个团队里；当前的模式是混合式：一个小型中心职能制定标准，交付则发生在嵌入业务的跨职能团队中。分析师的预测对方向毫不含糊——Gartner预计到2026年底，绝大多数企业将把生成式AI能力推向生产环境——而我们在亚太区零售、金融服务、制造与专业服务的项目经验表明，团队结构是这些生产系统能否活过第一年的最强预测因子。</p>
<p>第二个模式是治理的职业化。AI项目越来越像资本项目一样接受评审：模型上线前必须通过数据、风险与合规检查点，上线后按计划被监控与退役。在我们的经验里，把治理当事后补充的组织，恰恰是最容易在第一次事故后就放弃自己项目的那些。</p>
<h2 id="ai项目应该由谁主导it数据还是业务">AI项目应该由谁主导——IT、数据还是业务？</h2>
<p>诚实的答案是：没有任何单一职能应该主导，试图指定单一所有者的组织恰恰是举步维艰的那些。交付归属权应放在跨职能产品团队——业务、数据、工程与设计朝同一张路线图努力；赋能归属权则放在精简的中心职能，由它提供平台、标准与护栏。业务定义成果，数据提供原料，工程提供手艺，中心职能让大家保持诚实。</p>
<p>归属权还需要在每一层都显式化：对业务成果负责的产品负责人、对架构负责的技术负责人、对质量与数据血缘负责的数据负责人、对资源与扫清障碍负责的高管保荐人。我们的经验显示，责任分配清晰达到生产的概率显著更高——归属权模糊是AI计划停摆最可靠的预测因子之一。</p>
<p>在具名角色之下，有两个结构性选择最重要。第一是贴近：交付团队应与所服务的业务职能坐在一起——或至少一次对话就能够到——因为当业务优先级变化时，贴近性是路线图保持诚实的保证。第二是分离：制定标准的中心职能不能同时是交付功能的团队，否则它的标准会悄悄变成可选项。尊重这两个选择的组织，避开了两种经典失败模式——没人用的孤立科学项目，和没人解释得清的不受治理的影子AI。</p>
<h2 id="跨职能ai团队的关键实施挑战有哪些">跨职能AI团队的关键实施挑战有哪些？</h2>
<p>第一个挑战是角色定义。数据工程师、分析师、机器学习工程师与业务翻译并不天然认同谁负责什么；没有显式定义，工作就会漏掉或重复。我们的评估同时显示，约70%的企业数据需要大量准备才能支撑AI工作负载——这个现实把数据所有权从抽象概念变成日常运营问题。</p>
<p>第二个挑战是跟上节奏的治理。每月开会的委员会审不动每周的模型变更，太慢的治理反而成为计划失控的理由而非安全的理由。答案是分层治理：小变更走轻量检查，只有高风险变更才升级。</p>
<p>第三个挑战是度量。当团队无法就成功长什么样达成一致时就会失败——业务要成果、工程要延迟、数据要质量，三者都对。缺少与业务价值绑定的共享成功指标，团队的精力就会消耗在优先级争吵上。变革管理在这里同样关键：我们的经验显示，投入全面变革管理计划的组织，采纳率比不投入的高出三倍。</p>
<h2 id="哪些实践方法真正有效">哪些实践方法真正有效？</h2>
<p>行得通的方法并不花哨。围绕成果而非技术定义团队：定价团队、履约团队、反欺诈团队——各自有自己的数据、模型与业务对接人——而不是一支泛泛的AI小队。按成果定义的团队有天然的所有者、天然的指标和天然的用户。</p>
<p>建立节奏：每周交付站会、每月成果复盘、每季度治理评审——后者按公开议程检视风险、模型表现与数据问题。节奏是把结构从组织架构图变成行为的东西。</p>
<p>发布护栏。数据质量阈值、模型评估标准、安全要求与升级路径都应写下来、公之于众，让团队清楚自己为什么负责、中心职能会检查什么。书面护栏还能挺过人员流动——那才是AI计划安静的杀手。</p>
<p>最后，投资团队的数据素养。跨职能协作只有在业务成员读得懂数据、数据成员说得了业务时才成立。把团队结构与结构化素养计划配对的组织，建立起能就权衡有效争论的团队——争论的是取舍，而不是词汇。</p>
<p>还值得定义团队如何做决策。一小组常设决策规则——什么需要保荐人、什么可以授权技术负责人、什么必须等下一次治理评审——消除了跨职能摩擦最常见的来源：不是关于数据的分歧，而是关于流程的分歧。书面的决策规则让团队变快，因为例行事务无须请示，重要事项也不会漏过。</p>
<h2 id="如何构建跟上交付速度的治理机制">如何构建跟上交付速度的治理机制？</h2>
<p>跨职能AI团队的治理应按风险分层。例行模型更新与低影响分析变更通过自动检查与授权评审人放行；触及受监管数据、客户决策或重大预算的变更升级到常设评审委员会。正是这种分层让团队每周都能发布，同时组织保持受保护。</p>
<p>治理的产出应是决策日志，而不是官僚流程。每次评审产出一条注明日期、附理由、组织内任何人都能查到的决策；每起事故产出一份书面复盘，喂养下一次评审。在我们的经验里，采用这种模式的组织随着信任积累，审批速度反而越来越快——日志就是治理在起作用的证据。</p>
<h2 id="核心要点有哪些">核心要点有哪些？</h2>
<p>六项实践把能交付的跨职能AI团队与那些解散的区分开来：</p>
<ul>
<li>围绕业务成果而非技术组织——用团队改善的那个决策来定义团队</li>
<li>在每一层显式化归属权，从产品负责人到高管保荐人</li>
<li>发布数据质量、安全与评估的护栏——并执行它们</li>
<li>运行每周交付、每月成果、每季度治理评审的节奏</li>
<li>用与业务价值绑定的共享指标度量成功</li>
<li>投资数据素养与变革管理；做了采纳率就是三倍</li>
</ul>
<h2 id="接下来应该怎么做">接下来应该怎么做？</h2>
<p>跨职能AI团队既是重大机遇，也是现实的挑战。成功的组织把技术卓越与战略清晰、治理纪律和深思熟虑的变革管理结合起来——并把团队结构当作与任何架构选择同样郑重的设计决策来对待。</p>
<p>蜂启咨询帮助亚太区企业塑造围绕AI的运营模型——团队、节奏、护栏与指标。2026年，把结构做对的组织将把更多试点转化为生产价值，因为稀缺的资源不再是模型，而是围绕模型的有组织投入。如果你正准备重组AI团队或建立跟上交付速度的治理，欢迎预约演示，我们将结合你的行业与数据现状给出可落地的建议。</p>
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
    assert '跨职能' in h1 or 'AI' in h1, "wrong file? h1=" + h1
    if 'id="2026年跨职能ai团队的格局是什么样的"' in s:
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
            "跨职能AI团队的结构设计，决定AI试点能否活过第一年。",
        ], "CN-excerpt")
    integrity(s, [
        '?v=20260901', '预约演示', '"@type": "FAQPage"',
        'id="2026年跨职能ai团队的格局是什么样的"', 'id="接下来应该怎么做"',
        '采纳率高出三倍', '蜂启咨询',
    ], 8, "zh-CN")
    assert '跨职能' in body_h1(s)
    save(ZHCN, s)
    print("CN done")

# ---------------- zh-TW ----------------
TW_FAQ = [
    ("AI專案應該由IT、資料還是業務部門主導？",
     "沒有任何單一職能應該獨佔主導權。交付歸屬權屬於跨職能產品團隊——業務、資料、工程與設計共用一張路線圖；而一個精簡的中心職能提供平台、標準與護欄。兩者必須分開：制定標準的團隊不能同時是交付功能的團隊，否則標準會悄悄變成可選項。"),
    ("跨職能AI團隊的合理規模是多大？",
     "小到保持敏捷，大到能端到端交付。我們的經驗是，有效的核心規模為五到九人，覆蓋產品、工程、資料與設計，並由業務方借調領域專家。超過十人左右後，協調成本的增長會快過產出增長——此時應按產品線拆分團隊，而不是繼續擴張。"),
    ("AI治理應該放在組織的哪個位置？",
     "離交付足夠近才有用，層級足夠高才有約束力。在大多數企業裡，由高階主管主持、資料、風險與法遵共同參與的季度治理評審是可行的結構。離交付太遠的治理會淪為文書工作；沒有高階背書的治理只會淪為建議。"),
    ("AI治理評審多久進行一次？",
     "全面評審按季度進行，日常決策走快速通道。發布書面的決策規則，讓團隊清楚哪些可以自行批准、哪些需要技術負責人簽核、哪些必須等下一次治理評審。每次評審都應產出一條註明日期、附理由、組織內任何人都能查到的決策記錄——這份記錄就是治理在起作用的證據。"),
]

TW_TOC = [
    ("2026年跨職能ai團隊的格局是什麼樣的", "2026年跨職能AI團隊的格局是什麼樣的？"),
    ("ai專案應該由誰主導it資料還是業務", "AI專案應該由誰主導——IT、資料還是業務？"),
    ("跨職能ai團隊的關鍵實施挑戰有哪些", "跨職能AI團隊的關鍵實施挑戰有哪些？"),
    ("哪些實務方法真正有效", "哪些實務方法真正有效？"),
    ("如何構建跟上交付速度的治理機制", "如何構建跟上交付速度的治理機制？"),
    ("核心要點有哪些", "核心要點有哪些？"),
    ("接下來應該怎麼做", "接下來應該怎麼做？"),
]

TW_BODY = '''<p class="article-lead"><strong>2026年，決定AI試點生死的不再是模型，而是組織模型。</strong>跨職能AI團隊——交付AI計畫的那群人的結構與治理——已經成為試點墳場與生產價值之間的分水嶺。模型已經充裕，平台已經成熟，稀缺的資源是有組織的人力投入。本文剖析成功企業如何搭建AI團隊、治理應該放在哪裡，以及蜂啟諮詢的推薦做法。簡短的答案是：AI是一個營運模型問題，成功的團隊像產品團隊一樣組建、像受監管職能一樣治理。</p>
<div class="article-tldr"><p><strong>核心要點：</strong>Gartner預計到2026年底，絕大多數企業將把生成式AI能力推向生產環境。約70%的企業資料需要大量治理準備才能支撐AI工作負載。投入全面變革管理的組織，採納率高出三倍。制勝的營運模型是混合式——小型中心職能制定標準，交付由嵌入業務的跨職能團隊完成，節奏為每週交付、每月復盤成果、每季度治理評審。</p></div>
<h2 id="2026年跨職能ai團隊的格局是什麼樣的">2026年跨職能AI團隊的格局是什麼樣的？</h2>
<p>2026年的格局由AI卓越中心壟斷的瓦解定義。早期計畫把AI集中在一個團隊裡；當前的模式是混合式：一個小型中心職能制定標準，交付則發生在嵌入業務的跨職能團隊中。分析師的預測對方向毫不含糊——Gartner預計到2026年底，絕大多數企業將把生成式AI能力推向生產環境——而我們在亞太區零售、金融服務、製造與專業服務的專案經驗表明，團隊結構是這些生產系統能否活過第一年的最強預測因子。</p>
<p>第二個模式是治理的職業化。AI專案越來越像資本專案一樣接受評審：模型上線前必須通過資料、風險與法遵檢查點，上線後按計畫被監控與退役。在我們的經驗裡，把治理當事後補充的組織，恰恰是最容易在第一次事故後就放棄自己專案的那些。</p>
<h2 id="ai專案應該由誰主導it資料還是業務">AI專案應該由誰主導——IT、資料還是業務？</h2>
<p>誠實的答案是：沒有任何單一職能應該主導，試圖指定單一所有者的組織恰恰是舉步維艱的那些。交付歸屬權應放在跨職能產品團隊——業務、資料、工程與設計朝同一張路線圖努力；賦能歸屬權則放在精簡的中心職能，由它提供平台、標準與護欄。業務定義成果，資料提供原料，工程提供手藝，中心職能讓大家保持誠實。</p>
<p>歸屬權還需要在每一層都顯式化：對業務成果負責的產品負責人、對架構負責的技術負責人、對品質與資料血緣負責的資料負責人、對資源與掃清障礙負責的高階保薦人。我們的經驗顯示，責任分配清晰達到生產的概率顯著更高——歸屬權模糊是AI計畫停擺最可靠的預測因子之一。</p>
<p>在具名角色之下，有兩個結構性選擇最重要。第一是貼近：交付團隊應與所服務的業務職能坐在一起——或至少一次對話就能夠到——因為當業務優先級變化時，貼近性是路線圖保持誠實的保證。第二是分離：制定標準的中心職能不能同時是交付功能的團隊，否則它的標準會悄悄變成可選項。尊重這兩個選擇的組織，避開了兩種經典失敗模式——沒人用的孤立科學專案，和沒人解釋得清的不受治理的影子AI。</p>
<h2 id="跨職能ai團隊的關鍵實施挑戰有哪些">跨職能AI團隊的關鍵實施挑戰有哪些？</h2>
<p>第一個挑戰是角色定義。資料工程師、分析師、機器學習工程師與業務翻譯並不天然認同誰負責什麼；沒有顯式定義，工作就會漏掉或重複。我們的評估同時顯示，約70%的企業資料需要大量準備才能支撐AI工作負載——這個現實把資料所有權從抽象概念變成日常營運問題。</p>
<p>第二個挑戰是跟上節奏的治理。每月開會的委員會審不動每週的模型變更，太慢的治理反而成為計畫失控的理由而非安全的理由。答案是分層治理：小變更走輕量檢查，只有高風險變更才升級。</p>
<p>第三個挑戰是度量。當團隊無法就成功長什麼樣達成一致時就會失敗——業務要成果、工程要延遲、資料要品質，三者都對。缺少與業務價值綁定的共享成功指標，團隊的精力就會消耗在優先級爭吵上。變革管理在這裡同樣關鍵：我們的經驗顯示，投入全面變革管理計畫的組織，採納率比不投入的高出三倍。</p>
<h2 id="哪些實務方法真正有效">哪些實務方法真正有效？</h2>
<p>行得通的方法並不花俏。圍繞成果而非技術定義團隊：定價團隊、履約團隊、反詐欺團隊——各自有自己的資料、模型與業務對接人——而不是一支泛泛的AI小隊。按成果定義的團隊有天然的所有者、天然的指標和天然的使用者。</p>
<p>建立節奏：每週交付站會、每月成果復盤、每季度治理評審——後者按公開議程檢視風險、模型表現與資料問題。節奏是把結構從組織架構圖變成行為的東西。</p>
<p>發布護欄。資料品質閾值、模型評估標準、安全要求與升級路徑都應寫下來、公之於眾，讓團隊清楚自己為什麼負責、中心職能會檢查什麼。書面護欄還能挺過人員流動——那才是AI計畫安靜的殺手。</p>
<p>最後，投資團隊的資料素養。跨職能協作只有在業務成員讀得懂資料、資料成員說得了業務時才成立。把團隊結構與結構化素養計畫配對的組織，建立起能就權衡有效爭論的團隊——爭論的是取捨，而不是詞彙。</p>
<p>還值得定義團隊如何做決策。一小組常設決策規則——什麼需要保薦人、什麼可以授權技術負責人、什麼必須等下一次治理評審——消除了跨職能摩擦最常見的來源：不是關於資料的分歧，而是關於流程的分歧。書面的決策規則讓團隊變快，因為例行事務無須請示，重要事項也不會漏過。</p>
<h2 id="如何構建跟上交付速度的治理機制">如何構建跟上交付速度的治理機制？</h2>
<p>跨職能AI團隊的治理應按風險分層。例行模型更新與低影響分析變更通過自動檢查與授權評審人放行；觸及受監管資料、客戶決策或重大預算的變更升級到常設評審委員會。正是這種分層讓團隊每週都能發布，同時組織保持受保護。</p>
<p>治理的產出應是決策日誌，而不是官僚流程。每次評審產出一條註明日期、附理由、組織內任何人都能查到的決策；每起事故產出一份書面復盤，餵養下一次評審。在我們的經驗裡，採用這種模式的組織隨著信任累積，審批速度反而越來越快——日誌就是治理在起作用的證據。</p>
<h2 id="核心要點有哪些">核心要點有哪些？</h2>
<p>六項實務把能交付的跨職能AI團隊與那些解散的區分開來：</p>
<ul>
<li>圍繞業務成果而非技術組織——用團隊改善的那個決策來定義團隊</li>
<li>在每一層顯式化歸屬權，從產品負責人到高階保薦人</li>
<li>發布資料品質、安全與評估的護欄——並執行它們</li>
<li>運行每週交付、每月成果、每季度治理評審的節奏</li>
<li>用與業務價值綁定的共享指標度量成功</li>
<li>投資資料素養與變革管理；做了採納率就是三倍</li>
</ul>
<h2 id="接下來應該怎麼做">接下來應該怎麼做？</h2>
<p>跨職能AI團隊既是重大機遇，也是現實的挑戰。成功的組織把技術卓越與策略清晰、治理紀律和深思熟慮的變革管理結合起來——並把團隊結構當作與任何架構選擇同樣鄭重的設計決策來對待。</p>
<p>蜂啟諮詢幫助亞太區企業塑造圍繞AI的營運模型——團隊、節奏、護欄與指標。2026年，把結構做對的組織將把更多試點轉化為生產價值，因為稀缺的資源不再是模型，而是圍繞模型的有組織投入。如果你正準備重組AI團隊或建立跟上交付速度的治理，歡迎預約示範，我們將結合你的產業與資料現狀給出可落地的建議。</p>
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
    assert '跨職能' in h1 or 'AI' in h1, "wrong file? h1=" + h1
    if 'id="2026年跨職能ai團隊的格局是什麼樣的"' in s:
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
            "跨職能AI團隊的結構設計，決定AI試點能否活過第一年。",
        ], "TW-excerpt")
    integrity(s, [
        '?v=20260901', '預約示範', '"@type": "FAQPage"',
        'id="2026年跨職能ai團隊的格局是什麼樣的"', 'id="接下來應該怎麼做"',
        '採納率高出三倍', '蜂啟諮詢',
    ], 8, "zh-TW")
    assert '跨職能' in body_h1(s)
    save(ZHTW, s)
    print("TW done")

if __name__ == "__main__":
    process_en()
    process_cn()
    process_tw()
    print("slug 14 all done")
