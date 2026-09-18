# -*- coding: utf-8 -*-
"""Slug 2: build-enterprise-knowledge-graph-ai — EN expand + zh FAQ/H2/TOC fixes."""
import sys, re
sys.path.insert(0, "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline/tmp")
from common import (load, save, rep1, re_dl, build_faq_list, build_jsonld,
                    body_h1, fill_excerpts, integrity, FAQ_RX, JSONLD_RX)

W = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/"
EN = W + "blog/articles/build-enterprise-knowledge-graph-ai.html"
ZHCN = W + "zh-cn/blog/articles/build-enterprise-knowledge-graph-ai.html"
ZHTW = W + "zh-tw/blog/articles/build-enterprise-knowledge-graph-ai.html"

# ---------------- EN ----------------
EN_FAQ = [
    ("Why does enterprise AI need a knowledge graph when we already use RAG?",
     "RAG retrieves documents by semantic similarity, but it does not encode relationships between entities. A knowledge graph explicitly models how customers, products, suppliers, and regulations connect, letting AI agents answer multi-hop questions deterministically and traceably. The two are complementary: RAG supplies unstructured context, while the knowledge graph supplies the relational structure that turns retrieval into reasoning."),
    ("How long does it take to build a production enterprise knowledge graph?",
     "A focused first domain typically takes 8-12 weeks: schema design, MCP connectors to source systems, the initial data load, and validation with domain experts. Organizations that start with one high-value domain usually see 30-45% improvement in answer accuracy for complex questions before expanding to additional domains."),
    ("How does a knowledge graph stay accurate as the business changes?",
     "Through automated synchronization. MCP connectors watch source systems such as CRM, ERP, and regulatory databases, and update entities and relationships when source data changes. Combined with clear ownership of each entity's definition, this keeps the graph a living layer rather than a one-off project that drifts from reality."),
    ("Where should an enterprise start building a knowledge graph?",
     "Start with a single high-value domain where fragmented definitions cause real rework — for example client-risk-regulation relationships in financial services or product-supplier-component relationships in manufacturing. Model only the entities and relationships that domain needs, prove value with measurable accuracy gains, then extend one relationship at a time."),
]

SEC_A = '''<h2 id="what-do-knowledge-graphs-add-that-rag-cannot">What Do Knowledge Graphs Add That RAG Cannot?</h2>
<p>The clearest way to understand the difference is to look at what each system does when the answer is not in any single document. RAG treats the problem as a search problem: embed the question, find similar text, and let the model synthesize an answer. That works well when the answer exists, stated explicitly, somewhere in the corpus. It fails quietly when the answer exists only as the composition of facts scattered across systems — which is precisely the shape of most executive questions. A knowledge graph treats the problem as a structure problem: the relationships are stored as first-class data, so composition becomes traversal instead of guesswork.</p>
<p>Determinism and auditability follow from that difference. When an agent answers from a knowledge graph, the path it took — client to activity to region to regulation to exposure — is a recorded chain of edges that a reviewer can inspect, challenge, and correct. When an agent answers from retrieved documents, the reasoning chain is implicit in the model's generation, and two runs of the same question can weave different narratives from the same sources. For regulated industries, the ability to show why an answer was produced is becoming as important as the answer itself.</p>
<p>In practice, the strongest 2026 architectures are hybrids rather than replacements. The knowledge graph handles entity resolution and multi-hop structure; vector search supplies the unstructured context that no schema can fully capture — contract language, meeting notes, research reports. The semantic layer sits above both, ensuring that whichever component answers, 'top 20 clients' or 'regulatory exposure' means exactly one thing across the platform. Enterprises that combine all three consistently outperform those that bet on retrieval alone.</p>'''

SEC_B = '''<h2 id="what-role-does-ai-play-in-automating-knowledge-graph-construction">What Role Does AI Play in Automating Knowledge Graph Construction?</h2>
<p>The historical objection to knowledge graphs was construction cost: someone had to model the schema, clean the entities, and maintain the edges by hand. AI has changed that economics substantially. Modern extraction pipelines use LLMs to read unstructured sources — contracts, policy documents, regulatory filings — and propose entities and relationships in the graph's schema. Entity resolution models deduplicate and merge records across systems, so that 'Customer A' in the CRM, 'Acme Corp' in the ERP, and 'ACME' in the legal repository unify into a single node with provenance attached.</p>
<p>AI also accelerates the schema design phase itself. Given a corpus of domain documents and a sample of source data, LLMs can draft candidate entity types, relationship types, and cardinality rules that domain experts then refine. This shifts the human role from drawing boxes and lines to reviewing and approving — a dramatically cheaper activity. Teams that once spent months on ontology design now spend weeks, and the schema improves continuously because every correction made during validation feeds back into the extraction prompts.</p>
<p>The critical discipline is keeping humans in the loop for anything that carries business or regulatory consequence. Automated extraction should be treated as a proposal engine, not an authority: high-impact relationships — ownership structures, exposure links, compliance obligations — pass through a lightweight review queue before they are trusted by production agents. Confidence scores attached to each extracted edge let agents weigh answers appropriately, and periodic audits sample low-confidence edges for expert verification. This human-supervised automation is what makes enterprise-grade graphs affordable without making them fragile.</p>'''

SEC_C = '''<h2 id="how-do-you-keep-an-enterprise-knowledge-graph-accurate-over-time">How Do You Keep an Enterprise Knowledge Graph Accurate Over Time?</h2>
<p>Freshness is the first pillar. A knowledge graph that was accurate at launch and unsupervised since is actively dangerous, because agents answer with stale confidence. The practical answer is event-driven synchronization: MCP connectors to CRM, ERP, and regulatory sources push changes into the graph as they happen, rather than waiting for quarterly reloads. Entities carry timestamps and source lineage, so an agent can distinguish a relationship verified this week from one last touched eight months ago.</p>
<p>Ownership is the second pillar. Every entity type and every high-value relationship type needs a named steward — someone accountable when two systems disagree about what a client's exposure actually is. The steward does not hand-maintain the data; they own the reconciliation rules and approve the automated merges. Graphs that skip this step drift quietly: edges accumulate that reflect last year's org chart or a supplier relationship that ended in a dispute, and the first symptom is usually a business user losing trust after one visibly wrong answer.</p>
<p>The third pillar is measurement. Graph health is measurable: the percentage of entities with confirmed lineage, the age distribution of edges, the rate of conflict between graph answers and source-system queries, and the volume of user-flagged corrections. Leading teams review these metrics monthly, the way they review data-quality dashboards, and treat a rising correction rate as an incident rather than background noise. A knowledge graph maintained this way compounds in value — every correction improves every future answer — while one maintained casually decays until it is quietly abandoned.</p>'''

PARA_D = '''<p>Finally, set an accuracy bar before you build, not after. Decide in advance what answer accuracy means for your domain, how it will be measured, and what threshold justifies expanding the graph to the next domain. Teams that define this upfront have an objective basis for investment decisions; teams that skip it end up debating anecdotes, and the knowledge graph becomes a matter of faith rather than a measured capability.</p>'''

def process_en():
    s = load(EN)
    h1 = body_h1(s)
    assert "Knowledge Graph" in h1, "wrong file? h1=" + h1
    if 'what-do-knowledge-graphs-add-that-rag-cannot' in s:
        print("EN already processed, skip")
        return
    # 1) H2 question-form conversions (keep ids)
    s = rep1(s, '<h2 id="why-knowledge-graphs-matter-for-enterprise-ai">Why Knowledge Graphs Matter for Enterprise AI</h2>',
             '<h2 id="why-knowledge-graphs-matter-for-enterprise-ai">Why Do Knowledge Graphs Matter for Enterprise AI?</h2>', 'h2-1')
    s = rep1(s, '<h2 id="architecture-knowledge-graphs-with-mcp-and-semantic-layers">Architecture: Knowledge Graphs with MCP and Semantic Layers</h2>',
             '<h2 id="architecture-knowledge-graphs-with-mcp-and-semantic-layers">What Does a Knowledge Graph Architecture with MCP and Semantic Layers Look Like?</h2>', 'h2-2')
    s = rep1(s, '<h2 id="building-your-enterprise-knowledge-graph">Building Your Enterprise Knowledge Graph</h2>',
             '<h2 id="building-your-enterprise-knowledge-graph">How Do You Build Your Enterprise Knowledge Graph?</h2>', 'h2-3')
    s = rep1(s, '<h2 id="knowledge-graphs-and-conversational-bi">Knowledge Graphs and Conversational BI</h2>',
             '<h2 id="knowledge-graphs-and-conversational-bi">How Do Knowledge Graphs and Conversational BI Work Together?</h2>', 'h2-4')
    # 2) new sections
    anchor_a = 'the agent does not miss relationships because they were not mentioned in any single document.</p>'
    s = rep1(s, anchor_a, anchor_a + "\n" + SEC_A, 'secA')
    anchor_b = "the graph's value compounds as more domains and more relationships are added.</p>"
    s = rep1(s, anchor_b, anchor_b + "\n" + SEC_B, 'secB')
    anchor_c = 'questions that no combination of dashboards, reports, and document searches can adequately address today.</p>'
    s = rep1(s, anchor_c, anchor_c + "\n" + SEC_C, 'secC')
    anchor_d = 'which is the most common way these initiatives die.</p>'
    s = rep1(s, anchor_d, anchor_d + "\n" + PARA_D, 'paraD')
    # 3) remove head FAQPage (tempered regex — only the head block matches)
    s = re_dl(s, JSONLD_RX, '', 'head-faqpage-remove')
    # 4) replace FAQ list with topic Q&A (h3-wrapped)
    new_faq = '<div class="faq-list">\n' + build_faq_list(EN_FAQ) + '\n                </div>\n            </section>'
    s = re_dl(s, FAQ_RX, new_faq.replace('\\', '\\\\'), 'faq-list')
    # 5) place matching JSON-LD right after FAQ section
    old_nav = '</section>\n\n            <nav class="article-nav"'
    assert s.count(old_nav) == 1
    s = s.replace(old_nav, '</section>\n' + build_jsonld(EN_FAQ) + '\n\n            <nav class="article-nav"')
    # 6) TOC sync (mobile + sidebar)
    toc_entries = [
        ("why-knowledge-graphs-matter-for-enterprise-ai", "Why Do Knowledge Graphs Matter for Enterprise AI?"),
        ("what-do-knowledge-graphs-add-that-rag-cannot", "What Do Knowledge Graphs Add That RAG Cannot?"),
        ("architecture-knowledge-graphs-with-mcp-and-semantic-layers", "What Does a Knowledge Graph Architecture with MCP and Semantic Layers Look Like?"),
        ("building-your-enterprise-knowledge-graph", "How Do You Build Your Enterprise Knowledge Graph?"),
        ("what-role-does-ai-play-in-automating-knowledge-graph-construction", "What Role Does AI Play in Automating Knowledge Graph Construction?"),
        ("knowledge-graphs-and-conversational-bi", "How Do Knowledge Graphs and Conversational BI Work Together?"),
        ("how-do-you-keep-an-enterprise-knowledge-graph-accurate-over-time", "How Do You Keep an Enterprise Knowledge Graph Accurate Over Time?"),
        ("where-do-you-start-building-a-knowledge-graph", "Where Do You Start Building a Knowledge Graph?"),
    ]
    mob = "\n".join(f'                    <a href="#{i}" class="toc-mobile-link">{t}</a>' for i, t in toc_entries)
    side = "\n".join(f'                    <a href="#{i}" class="toc-link">{t}</a>' for i, t in toc_entries)
    s = re_dl(s, r'<div class="toc-mobile-links">.*?</div>', '<div class="toc-mobile-links">\n' + mob + '\n                </div>', 'toc-mobile')
    s = re_dl(s, r'<nav class="toc-links">.*?</nav>', '<nav class="toc-links">\n' + side + '\n                </nav>', 'toc-side')
    # 7) excerpts
    s = fill_excerpts(s, [
        "How to design the four-layer architecture — data, model, application, and interface — that production AI agents require.",
        "How AI-driven scenario planning helps supply chain teams prepare for disruption before it happens.",
        "How demand sensing with AI shortens forecast cycles and keeps supply chains aligned with real demand.",
    ], "EN-excerpt")
    # integrity BEFORE save
    integrity(s, [
        '?v=20260901', '"@type": "BlogPosting"', '"@type": "BreadcrumbList"',
        'id="what-do-knowledge-graphs-add-that-rag-cannot"',
        'id="what-role-does-ai-play-in-automating-knowledge-graph-construction"',
        'id="how-do-you-keep-an-enterprise-knowledge-graph-accurate-over-time"',
        '"@type": "FAQPage"', 'Book a Demo',
        '<h1 class="article-h1">How to Build an Enterprise Knowledge Graph with AI</h1>',
    ], 8, "EN")
    assert s[:s.index('</head>')].count('FAQPage') == 0, "head FAQPage still present"
    save(EN, s)
    print("EN done")

# ---------------- zh-CN ----------------
CN_FAQ = [
    ("为什么企业AI需要知识图谱，而不能只靠RAG？",
     "RAG按语义相似度检索文档，但不会编码实体之间的关系。知识图谱显式建模客户、产品、供应商与监管之间的关联，让AI智能体能够确定性地回答多跳问题。两者互补：RAG提供非结构化上下文，知识图谱提供把检索变成推理的关系结构。"),
    ("构建一个生产级企业知识图谱需要多久？",
     "聚焦单一高价值域通常需要8-12周，包括图谱模式设计、MCP连接器对接源系统、初始数据加载和领域专家验证。组织在首个域通常就能看到复杂问题回答准确率提升30-45%，然后再扩展到更多域。"),
    ("业务持续变化时，知识图谱如何保持准确？",
     "依靠自动同步。MCP连接器监听CRM、ERP和监管数据库等源系统的变化，并在源数据变化时更新实体和关系。配合明确的实体定义归属机制，知识图谱才能成为持续演进的活层，而非偏离现实的一次性项目。"),
]

CN_H2 = [
    ('当前格局与关键趋势', '为什么企业知识图谱是2026年AI基础设施的关键层？'),
    ('实施框架与最佳实践', '如何搭建企业知识图谱的实施框架？'),
    ('衡量影响与展示价值', '如何衡量企业知识图谱的业务价值？'),
    ('克服常见挑战', '企业知识图谱落地的常见挑战如何克服？'),
    ('组织准备与能力建设', '企业知识图谱需要怎样的组织准备与能力建设？'),
    ('ROI衡量与商业论证', '如何计算企业知识图谱的ROI并构建商业论证？'),
]

def process_cn():
    s = load(ZHCN)
    h1 = body_h1(s)
    assert '知识图谱' in h1 or 'Knowledge Graph' in h1, "wrong file? h1=" + h1
    changed = False
    # 1) H2 question-form
    for old, new in CN_H2:
        if f'>{new}</h2>' not in s:
            s = rep1(s, f'>{old}</h2>', f'>{new}</h2>', 'cn-h2-' + old)
            changed = True
    # 2) TOC sync (keep hrefs, update text)
    toc_entries = [(old, new) for old, new in CN_H2]
    mob = "\n".join(f'                    <a href="#{o}" class="toc-mobile-link">{n}</a>' for o, n in toc_entries)
    side = "\n".join(f'                    <a href="#{o}" class="toc-link">{n}</a>' for o, n in toc_entries)
    def mob_repl(m):
        return '<div class="toc-mobile-links">\n' + mob + '\n                </div>'
    def side_repl(m):
        return '<nav class="toc-links">\n' + side + '\n                </nav>'
    if changed or 'toc-mobile-link">为什么' not in s:
        s2 = re.sub(r'<div class="toc-mobile-links">.*?</div>', mob_repl, s, count=1, flags=re.S)
        assert s2 != s or mob in s, "cn toc-mobile replace failed"
        s = s2
        s2 = re.sub(r'<nav class="toc-links">.*?</nav>', side_repl, s, count=1, flags=re.S)
        assert s2 != s or side in s, "cn toc-side replace failed"
        s = s2
    # 3) FAQ + JSON-LD
    if '为什么企业AI需要知识图谱' not in s:
        new_faq = '<div class="faq-list">\n' + build_faq_list(CN_FAQ) + '\n                </div>\n            </section>'
        s = re_dl(s, FAQ_RX, new_faq.replace('\\', '\\\\'), 'cn-faq')
        s = re_dl(s, JSONLD_RX, build_jsonld(CN_FAQ).replace('\\', '\\\\'), 'cn-jsonld')
    # 4) excerpts
    if 'recommended-card-excerpt"></p>' in s:
        s = fill_excerpts(s, [
            "数据质量自动化让数据治理从被动补救转向主动预防。",
            "CFO可以按业务价值分层分配AI预算，最大化2026年投资回报。",
        ], "CN-excerpt")
    integrity(s, [
        '?v=20260901', '预约演示', '"@type": "FAQPage"',
        '为什么企业AI需要知识图谱', '如何搭建企业知识图谱的实施框架',
        'id="roi衡量与商业论证"',
    ], 8, "zh-CN")
    assert s[:s.index('</head>')].count('FAQPage') == 0, "cn head FAQPage present"
    save(ZHCN, s)
    print("zh-CN done")

# ---------------- zh-TW ----------------
TW_FAQ = [
    ("為什麼企業AI需要知識圖譜，而不能只靠RAG？",
     "RAG按語義相似度檢索文件，但不會編碼實體之間的關係。知識圖譜顯式建模客戶、產品、供應商與監管之間的關聯，讓AI智能體能夠確定性地回答多跳問題。兩者互補：RAG提供非結構化上下文，知識圖譜提供把檢索變成推理的關係結構。"),
    ("構建一個生產級企業知識圖譜需要多久？",
     "聚焦單一高價值域通常需要8-12週，包括圖譜模式設計、MCP連接器對接源系統、初始資料載入和領域專家驗證。組織在首個域通常就能看到複雜問題回答準確率提升30-45%，然後再擴展到更多域。"),
    ("業務持續變化時，知識圖譜如何保持準確？",
     "依靠自動同步。MCP連接器監聽CRM、ERP和監管資料庫等源系統的變化，並在源資料變化時更新實體和關係。配合明確的實體定義歸屬機制，知識圖譜才能成為持續演進的活層，而非偏離現實的一次性專案。"),
]

TW_H2 = [
    ('architecture-knowledge-graphs-with-mcp-and-semantic-layers', 'MCP與語義層如何支撐企業知識圖譜架構？'),
    ('building-your-enterprise-knowledge-graph', '如何構建企業知識圖譜？'),
    ('knowledge-graphs-and-conversational-bi', '知識圖譜與對話式BI如何協同工作？'),
    ('規模化推廣的關鍵成功因素', '語義層如何消除企業AI的定義不一致問題？'),
    ('技術基礎設施與實施考量', '企業AI需要怎樣的技術基礎設施？'),
    ('中國市場特有的實施優勢', '為什麼中國企業能更快實現AI價值？'),
    ('規模化推廣的關鍵成功因素-2', '如何實現企業AI從試點到規模化推廣？'),
]

TW_LEAD_OLD = '企業需要建立AI卓越中心（CoE）來協調跨部門的AI initiatives。CoE的職責不是集中執行所有AI項目，而是建立標準、提供工具、分享最佳實踐、並確保治理合規。一個有效的CoE通常採用樞紐輻射模型——核心團隊負責平台建設和標準制定，各業務部門的AI冠軍負責具體用例的實施和推廣。這種模型既保證了組織級的一致性，又保持了業務部門的靈活性和自主性。CoE還應負責維護MCP連接器庫和語義層定義，確保這些共享資產的質量和一致性。'
TW_LEAD_NEW = '企業知識圖譜正在成為讓AI智能體理解業務脈絡、而不僅僅是檢索資料的缺失基礎設施層。向量資料庫和RAG系統幫助AI找到相關文件，而知識圖譜編碼概念之間的關係——客戶、產品、供應商、監管、風險因子——讓AI智能體能夠回答跨越多個業務領域的複雜多跳問題。本文深入分析企業知識圖譜的架構、構建方法和持續治理，幫助企業在相關領域做出明智的決策和投資。'
TW_TLDR_OLD = '行業研究表明，在How to Build an Enterprise Knowledge Graph with AI | 蜂啟諮詢|Why Knowledge Graphs Matter for Enterprise AI領域進行策略性投資的企業比延遲採用的組織價值實現速度快35%，投資回報率高28%，基於2026年企業基準資料。採用MCP標準化資料訪問和語義層治理的組織，平均部署時間縮短40%。'
TW_TLDR_NEW = '以知識圖譜驅動AI智能體的企業，複雜查詢回答準確率提升45%，跨職能問題解決速度提升3倍。知識圖譜結合MCP資料連接器和語義層，構成企業AI的推理基礎設施。'

TW_PARA1_NEW = '企業知識圖譜的架構圍繞三個系統展開。知識圖譜本身以圖資料庫儲存實體和關係——客戶、產品、供應商、監管、風險因子，以及它們之間的業務邏輯，例如「客戶A透過活動C暴露於監管B」。MCP連接器負責讓圖譜保持最新：當CRM、ERP或監管資料來源發生變化時，連接器自動觸發圖譜更新，避免圖譜因資料過期而產生不可靠的答案。語義層則定義圖譜使用的業務詞彙——「風險敞口」的含義、「前二十大客戶」的口徑——確保圖譜、AI智能體和資料來源說同一種業務語言。三者協同，構成企業AI的推理基礎設施。'

def process_tw():
    s = load(ZHTW)
    h1 = body_h1(s)
    assert '知識圖譜' in h1 or 'Knowledge Graph' in h1, "wrong file? h1=" + h1
    # 1) lead + tldr (lead text is duplicated as first body paragraph — replace both)
    if TW_LEAD_OLD in s:
        n = s.count(TW_LEAD_OLD)
        assert n == 2, f"[tw-lead] expected 2 occurrences, got {n}"
        s = s.replace(TW_LEAD_OLD, TW_LEAD_NEW, 1)
        s = rep1(s, TW_LEAD_OLD, TW_PARA1_NEW, 'tw-para1')
    if TW_TLDR_OLD in s:
        s = rep1(s, TW_TLDR_OLD, TW_TLDR_NEW, 'tw-tldr')
    # 2) H2 question-form (keep ids)
    for hid, new in TW_H2:
        if f'id="{hid}">{new}</h2>' not in s:
            s = re_dl(s, r'<h2 id="' + re.escape(hid) + r'">(?:(?!</h2>).)*?</h2>',
                      f'<h2 id="{hid}">{new}</h2>'.replace('\\', '\\\\'), 'tw-h2-' + hid)
    # 3) TOC sync
    mob = "\n".join(f'                    <a href="#{h}" class="toc-mobile-link">{n}</a>' for h, n in TW_H2)
    side = "\n".join(f'                    <a href="#{h}" class="toc-link">{n}</a>' for h, n in TW_H2)
    s = re_dl(s, r'<div class="toc-mobile-links">.*?</div>',
              ('<div class="toc-mobile-links">\n' + mob + '\n                </div>').replace('\\', '\\\\'), 'tw-toc-mobile')
    s = re_dl(s, r'<nav class="toc-links">.*?</nav>',
              ('<nav class="toc-links">\n' + side + '\n                </nav>').replace('\\', '\\\\'), 'tw-toc-side')
    # 4) FAQ + JSON-LD
    if '為什麼企業AI需要知識圖譜' not in s:
        new_faq = '<div class="faq-list">\n' + build_faq_list(TW_FAQ) + '\n                </div>\n            </section>'
        s = re_dl(s, FAQ_RX, new_faq.replace('\\', '\\\\'), 'tw-faq')
        s = re_dl(s, JSONLD_RX, build_jsonld(TW_FAQ).replace('\\', '\\\\'), 'tw-jsonld')
    # 5) excerpts
    if 'recommended-card-excerpt"></p>' in s:
        s = fill_excerpts(s, [
            "資料質量自動化讓資料治理從被動補救轉為主動預防。",
            "CFO可以按業務價值分層分配AI預算，最大化2026年投資回報。",
        ], "TW-excerpt")
    integrity(s, [
        '?v=20260901', '預約示範', '"@type": "FAQPage"',
        '為什麼企業AI需要知識圖譜', 'id="規模化推廣的關鍵成功因素-2"',
        'MCP與語義層如何支撐企業知識圖譜架構',
    ], 9, "zh-TW")
    assert s[:s.index('</head>')].count('FAQPage') == 0, "tw head FAQPage present"
    save(ZHTW, s)
    print("zh-TW done")

process_en()
process_cn()
process_tw()
print("SLUG 2 COMPLETE")
