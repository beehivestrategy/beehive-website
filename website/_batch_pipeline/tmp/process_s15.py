# -*- coding: utf-8 -*-
"""Slug 15: snowflake-databricks-genie-conversational-ai
EN: interrogative H2s + tldr + FAQ rebuild (h3wrap) + JSON-LD to body + excerpts.
zh: full rewrite mirroring EN (6 sections + FAQ)."""
import sys, re
sys.path.insert(0, "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline/tmp")
from common import (load, save, rep1, re_dl, build_faq_list, build_jsonld,
                    body_h1, fill_excerpts, integrity, FAQ_RX, JSONLD_RX)

W = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/"
S = "snowflake-databricks-genie-conversational-ai"
EN = W + "blog/articles/" + S + ".html"
ZHCN = W + "zh-cn/blog/articles/" + S + ".html"
ZHTW = W + "zh-tw/blog/articles/" + S + ".html"

FAQ_SHELL = '''<section class="faq-section" id="frequently-asked-questions" aria-label="Frequently Asked Questions">
    <h2 class="faq-section-title">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        {TITLE}
    </h2>
<div class="faq-list">
{FAQ_LIST}
</div>
</section>
{JSONLD}'''

# ---------------- EN ----------------
EN_FAQ = [
    ("What is Genie in the context of Snowflake and Databricks?",
     "It is the name both platforms gave to their conversational analytics assistants — Databricks announced Genie in May 2024 and Snowflake launched its own Genie in June 2024. Both let users ask questions of their data in natural language and receive SQL-generated answers grounded in the warehouse."),
    ("How reliable are platform conversational assistants?",
     "On well-structured schemas with a curated semantic layer, teams report 80 to 90 percent success on routine questions, rising above 90 percent with good governance. Without the semantic layer, reliability drops sharply — sometimes below 60 percent — on complex, multi-table questions."),
    ("Do platform assistants replace the need for a semantic layer?",
     "No — the opposite. The assistant's reliability depends on the semantic layer, because natural-language questions must resolve to agreed definitions and join paths. Platforms provide the text-to-SQL engine; the semantic layer is what makes it dependable."),
    ("How should an enterprise evaluate a platform assistant before committing?",
     "Build a test set of real questions collected from business users in their own words, score the answers against it on the curated semantic surface, and fix definitional issues before rollout. Then run a feedback loop that feeds corrections back into the semantic layer so the same error does not recur."),
]

EN_TOC = [
    ("why-it-matters", "Why Does the Conversational AI Race Between Snowflake and Databricks Matter?"),
    ("common-challenges", "What Are the Common Challenges?"),
    ("what-separates-a-demo-from-a-dependable-assistant", "What Separates a Demo From a Dependable Assistant?"),
    ("how-to-get-started", "How Should You Get Started?"),
    ("key-takeaways", "What Are the Key Takeaways?"),
]

EN_TLDR = '<div class="article-tldr"><strong>Key Statistics:</strong> Databricks announced Genie in May 2024 and Snowflake launched its own Genie in June 2024, making conversational query a default warehouse feature. Teams report 80 to 90 percent answer success on routine questions when a curated semantic layer is in place — and above 90 percent with strong governance, versus below 60 percent on raw schemas. Analysts commonly spend 70 to 80 percent of their time servicing recurring report requests, which a dependable conversational layer can absorb.</div>'

def process_en():
    s = load(EN)
    h1 = body_h1(s)
    assert "Conversational AI" in h1, "wrong file? h1=" + h1
    if 'Why Does the Conversational AI Race' in s:
        print("EN already processed, skip")
        return
    # 1) remove old head FAQPage JSON-LD
    s = re_dl(s, JSONLD_RX, '', 'head-faqpage-remove')
    # 2) tldr after lead
    anchor = 'an expensive demo.</p>'
    assert s.count(anchor) == 1
    s = s.replace(anchor, anchor + '\n' + EN_TLDR)
    # 3) H2 interrogative conversions (keep ids)
    s = rep1(s, '<h2 id="why-it-matters">Why it matters</h2>',
             '<h2 id="why-it-matters">Why Does the Conversational AI Race Between Snowflake and Databricks Matter?</h2>', 'h2-1')
    s = rep1(s, '<h2 id="common-challenges">Common challenges</h2>',
             '<h2 id="common-challenges">What Are the Common Challenges?</h2>', 'h2-2')
    s = rep1(s, '<h2 id="how-to-get-started">How to get started</h2>',
             '<h2 id="how-to-get-started">How Should You Get Started?</h2>', 'h2-3')
    s = rep1(s, '<h2 id="key-takeaways">Key takeaways</h2>',
             '<h2 id="key-takeaways">What Are the Key Takeaways?</h2>', 'h2-4')
    # 4) replace legacy FAQ (plain-QA paragraphs + template faq-section) with rebuilt h3wrap FAQ + JSON-LD
    block = FAQ_SHELL.replace('{TITLE}', 'Frequently Asked Questions') \
                     .replace('{FAQ_LIST}', build_faq_list(EN_FAQ)) \
                     .replace('{JSONLD}', build_jsonld(EN_FAQ))
    rx = re.compile(r'<h2 id="frequently-asked-questions">.*?</section>(?=\s*\n\n            <nav class="article-nav")', re.S)
    assert len(rx.findall(s)) == 1, "legacy FAQ span not found"
    s = rx.sub(lambda m: block, s, count=1)
    # 5) TOC mobile sync
    mob = "\n".join(f'                    <a href="#{i}" class="toc-mobile-link">{t}</a>' for i, t in EN_TOC)
    s = re_dl(s, r'<div class="toc-mobile-links">.*?</div>', '<div class="toc-mobile-links">\n' + mob + '\n                </div>', 'toc-mobile')
    # 6) excerpts
    s = fill_excerpts(s, [
        "The reference architecture behind enterprise AI agents — and where the agent layer sits.",
        "How AI scenario planning builds resilience into supply chain decisions before disruption hits.",
        "Real-time demand sensing with AI: catching demand shifts before they become stockouts.",
    ], "EN-excerpt")
    integrity(s, [
        '?v=20260901', '"@type": "BlogPosting"', '"@type": "BreadcrumbList"',
        'Why Does the Conversational AI Race', 'What Are the Key Takeaways?',
        '"@type": "FAQPage"', 'Book a Demo', 'semantic layer',
    ], 6, "EN")
    assert "Conversational AI" in body_h1(s)
    assert s[:s.index('</head>')].count('FAQPage') == 0
    save(EN, s)
    print("EN done")

# ---------------- zh-CN ----------------
CN_FAQ = [
    ("Snowflake和Databricks语境下的Genie是什么？",
     "它是两家平台给各自对话式分析助手起的名字——Databricks于2024年5月发布Genie，Snowflake在2024年6月的峰会上发布了自己的Genie。两者都让用户用自然语言向数据提问，并得到以数仓为基础、由SQL生成的答案。"),
    ("平台对话式助手的可靠度如何？",
     "在有精心整理的语义层的良构模式上，团队报告例行问题的成功率为80%到90%，治理到位时可超过90%。没有语义层时，复杂多表问题的可靠度会骤降——有时低于60%。"),
    ("平台助手能取代语义层吗？",
     "不能——恰恰相反。助手的可靠性取决于语义层，因为自然语言问题必须解析到约定好的定义与联接路径上。平台提供的是text-to-SQL引擎；语义层才是让它可依赖的东西。"),
    ("企业应该怎样评估平台助手再决定采用？",
     "用业务用户自己的话收集真实问题，建立测试集；在整理过的语义层上对照测试集为答案打分，并在上线前先修复定义问题。然后运行反馈回路，把纠正写回语义层，让同样的错误不再复发。"),
]

CN_TOC = [
    ("为什么snowflake与databricks的对话式ai竞赛很重要", "为什么Snowflake与Databricks的对话式AI竞赛很重要？"),
    ("对话式数据助手面临哪些共同挑战", "对话式数据助手面临哪些共同挑战？"),
    ("什么把演示与可依赖的助手区分开", "什么把演示与可依赖的助手区分开？"),
    ("企业应该如何起步", "企业应该如何起步？"),
    ("核心要点有哪些", "核心要点有哪些？"),
    ("接下来应该怎么做", "接下来应该怎么做？"),
]

CN_BODY = '''<p class="article-lead">Snowflake与Databricks在对话式AI上的竞赛，正在改变自然语言分析被期待的运行位置。两家平台在2024年年中先后发布各自的Genie助手，让对话式查询从利基附加品变成数仓的默认能力。对大型企业而言，这既是降低分析门槛的机会，也是一次对语义层、治理与评估纪律的全面检验——蜂启咨询在亚太区的项目经验是：助手的上限不由厂商决定，而由你自己的数据基础决定。</p>
<div class="article-tldr"><p><strong>核心要点：</strong>Databricks于2024年5月发布Genie，Snowflake于2024年6月发布自己的Genie，对话式查询成为数仓默认功能。在整理过的语义层之上，团队报告例行问题80%到90%的回答成功率——治理到位可超过90%，而裸模式上可能低于60%。分析师通常把70%到80%的时间花在重复报表请求上，可靠的对话层可以吸收这部分工作。</p></div>
<h2 id="为什么snowflake与databricks的对话式ai竞赛很重要">为什么Snowflake与Databricks的对话式AI竞赛很重要？</h2>
<p>这场竞赛之所以重要，是因为它改变了自然语言分析被期待的运行位置。当Snowflake和Databricks都自带助手——Databricks于2024年5月发布Genie，Snowflake在2024年6月的峰会上发布自己的Genie——对话式查询不再是利基附加品，而成为数仓本身的默认功能。对企业来说，对话式BI的起点不再是一个独立的产品选型问题，而是平台助手在你的真实数据、真实用户上表现如何的问题。</p>
<p>底层技术趋势已经确立。Text-to-SQL系统从新鲜事物走向主流：在元数据清晰的良构企业模式上，现代助手大多数时候都能正确回答，许多团队报告例行问题80%到90%的回答成功率。但当模式混乱、定义含糊、或问题需要多表联接与任何模式图都看不出的业务逻辑时，同样的技术会迅速退化。这场竞赛真正争夺的，就是弥合这道鸿沟。</p>
<p>还有一个工作流层面的论据。分析师把不成比例的时间花在服务临时请求上——常见的估计是，重复性报表请求占掉分析师70%到80%的时间。可依赖的对话层不会取代分析师，它吸收例行请求，让分析师去做真正需要判断力的问题。这是每个平台厂商都在卖的业务理由，当助手足够可靠时它是成立的。</p>
<h2 id="对话式数据助手面临哪些共同挑战">对话式数据助手面临哪些共同挑战？</h2>
<p>第一个挑战是元数据质量，它是决定一切的那个。平台助手的好坏取决于它对你的数仓的语义理解：表名、列含义、联接路径、业务定义。把助手指向一个列名晦涩、毫无文档的原始数仓，得到的是听起来头头是道、却错在用户无法察觉之处的答案。语义层不是可有可无的装饰；它是可靠助手与负债之间的分界线。</p>
<p>第二个挑战是治理与权限。平台助手默认继承数仓层级的访问权，除非另行配置；一个配置不当的助手会把敏感列暴露给任何能组织出问题的用户。企业需要助手遵守的行级与列级控制，加上每一次查询的审计日志。在受监管环境里，这是门槛要求，不是加分项。</p>
<p>第三个挑战是评估鸿沟。平台演示看起来无懈可击，因为它们跑在元数据完美的精选模式上。你的生产环境不同——没有在上线前构建任务专用测试集的团队，会以最难受的方式发现这道鸿沟：当着业务用户的面。在你自己的问题、自己的数据、自己的定义上做评估，才是对任何平台助手唯一有意义的检验。</p>
<h2 id="什么把演示与可依赖的助手区分开">什么把演示与可依赖的助手区分开？</h2>
<p>把演示与可依赖助手区分开的是三件事，没有一件是模型规模。第一是语义层：对每个术语的含义、每个指标如何计算做出显式、受治理的定义。当助手查询的是整理过的语义层而非裸模式，复杂问题的回答可靠性会大幅上升——治理良好的部署例行超过90%的正确率，而裸模式查询在同一问题集上可能低于60%。</p>
<p>第二是落地与验证。可依赖的助手展示它的过程：查了哪些表、用了哪些过滤、采用了哪个收入定义、数据最后刷新于何时。用户因此可以抽查答案而不是盲目信任，而信任随着每一次被验证的答案复利累积。第三是反馈回路：一个捕获错误答案、纠正它、并把纠正写回语义层的机制，让同样的错误不再复发。平台提供管道；反馈纪律是企业自己的功课。</p>
<p>这就是为什么平台选择只是决策的一部分。助手的上限由你的语义层、权限模型与评估实践决定——无论哪家厂商，这三样同样决定任何对话式BI部署的质量。弱语义层上的强助手，跑不过治理良好的语义层上的普通助手。</p>
<p>最后是助手与既有BI投资的关系。当平台助手补充而非替代分析师已经维护的语义层与受治理定义时，它最强大。把助手当作同一套受治理定义之上的新前端的团队，在各 surfaces 得到一致的答案；放任助手对裸模式自由发挥的团队，制造出一个平行且互相矛盾的真相。架构决策——助手架在语义层之上，而不是旁边——塑造所有下游结果。</p>
<h2 id="企业应该如何起步">企业应该如何起步？</h2>
<p>从数仓的精选切片开始，而不是整个数仓。选择业务最常问的表与指标——收入、销售管道、库存、人员编制——只为这些构建语义定义。把平台助手接到这个精选面上，并在任何其他人看到之前，先用从真实用户收集的问题集做测试。</p>
<p>尽早从真实业务用户那里收集问题集。请十几位运营负责人用他们自己的话写下今天在问的问题，把它们作为测试集。给助手的答案打分——正确、部分正确、错误——并在改进语义层的过程中跟踪分数。大多数团队发现第一轮修复是定义问题，不是技术问题：困惑的不是助手，是定义。</p>
<p>然后有节奏地扩展：更多表、更多指标、更多用户，每次扩展之前都先把权限模型与审计链路就位。蜂启咨询这样的合作伙伴可以帮你构建精选语义层、设计评估测试集、搭建反馈回路，让你的平台助手在生产环境中赢得信任，而不是停留在演示里。</p>
<h2 id="核心要点有哪些">核心要点有哪些？</h2>
<ul>
<li>Snowflake与Databricks都在2024年年中发布Genie助手，对话式查询成为数仓默认功能</li>
<li>决定回答可靠性的是语义层，不是模型——整理过的定义每次都胜过裸模式</li>
<li>权限与审计日志必须在助手到达用户之前配置好；数仓层级访问不是安全的默认值</li>
<li>从业务用户那里构建真实问题集，上线前先对照它给答案打分</li>
<li>治理良好的例行问题预期80%到90%的成功率——并验证复杂联接的长尾</li>
<li>运行反馈回路，把错误答案变成语义层修复，让错误不再复发</li>
</ul>
<h2 id="接下来应该怎么做">接下来应该怎么做？</h2>
<p>对话式AI竞赛的赢家不是选对平台的买家，而是把语义层、权限与评估做扎实的运营者。平台会继续迭代，助手会继续变强，但这三样决定答案质量的东西不会过时——它们是你无论选谁都需要建的资产。</p>
<p>蜂启咨询帮助亚太区企业评估平台对话能力、构建精选语义层与评估体系，并把助手接入既有BI治理框架。如果你正在Snowflake与Databricks之间做选型，或准备让平台助手在生产环境落地，欢迎预约演示，我们将结合你的数据现状给出可执行的路线图。</p>
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
    assert '对话式' in h1 or 'Genie' in h1, "wrong file? h1=" + h1
    if 'id="为什么snowflake与databricks的对话式ai竞赛很重要"' in s:
        print("CN already processed, skip")
        return
    body = CN_BODY.replace('{FAQ_LIST}', build_faq_list(CN_FAQ)).replace('{JSONLD}', build_jsonld(CN_FAQ))
    start = '<p>Snowflake与Databricks'
    assert s.count(start) == 1, f"CN body start: {s.count(start)}"
    rx = re.compile(re.escape(start) + r'.*?(?=\n\n            <nav class="article-nav")', re.S)
    assert len(rx.findall(s)) == 1, "CN body span not 1"
    s = rx.sub(lambda m: body, s, count=1)
    mob = "\n".join(f'                    <a href="#{o}" class="toc-mobile-link">{t}</a>' for o, t in CN_TOC)
    def mob_repl(m):
        return '<div class="toc-mobile-links">\n' + mob + '\n                </div>'
    s2 = re.sub(r'<div class="toc-mobile-links">.*?</div>', mob_repl, s, count=1, flags=re.S)
    assert s2 != s, "cn toc replace failed"
    s = s2
    if 'recommended-card-excerpt"></p>' in s:
        s = fill_excerpts(s, [
            "对话式BI把数据查询变成聊天里的一次提问，治理由语义层保障。",
        ], "CN-excerpt")
    integrity(s, [
        '?v=20260901', '预约演示', '"@type": "FAQPage"',
        'id="为什么snowflake与databricks的对话式ai竞赛很重要"', 'id="接下来应该怎么做"',
        '80%到90%', '语义层', '蜂启咨询',
    ], 7, "zh-CN")
    assert '对话式' in body_h1(s) or 'Genie' in body_h1(s)
    save(ZHCN, s)
    print("CN done")

# ---------------- zh-TW ----------------
TW_FAQ = [
    ("Snowflake和Databricks語境下的Genie是什麼？",
     "它是兩家平台給各自對話式分析助手起的名字——Databricks於2024年5月發布Genie，Snowflake在2024年6月的峰會上發布了自己的Genie。兩者都讓用戶用自然語言向資料提問，並得到以資料倉儲為基礎、由SQL生成的答案。"),
    ("平台對話式助手的可靠度如何？",
     "在有精心整理的語義層的良構模式上，團隊報告例行問題的成功率為80%到90%，治理到位時可超過90%。沒有語義層時，複雜多表問題的可靠度會驟降——有時低於60%。"),
    ("平台助手能取代語義層嗎？",
     "不能——恰恰相反。助手的可靠性取決於語義層，因為自然語言問題必須解析到約定好的定義與聯接路徑上。平台提供的是text-to-SQL引擎；語義層才是讓它可依賴的東西。"),
    ("企業應該怎樣評估平台助手再決定採用？",
     "用業務用戶自己的話收集真實問題，建立測試集；在整理過的語義層上對照測試集為答案打分，並在上線前先修復定義問題。然後運行反饋迴路，把糾正寫回語義層，讓同樣的錯誤不再復發。"),
]

TW_TOC = [
    ("為什麼snowflake與databricks的對話式ai競賽很重要", "為什麼Snowflake與Databricks的對話式AI競賽很重要？"),
    ("對話式資料助手面臨哪些共同挑戰", "對話式資料助手面臨哪些共同挑戰？"),
    ("什麼把示範與可依賴的助手區分開", "什麼把示範與可依賴的助手區分開？"),
    ("企業應該如何起步", "企業應該如何起步？"),
    ("核心要點有哪些", "核心要點有哪些？"),
    ("接下來應該怎麼做", "接下來應該怎麼做？"),
]

TW_BODY = '''<p class="article-lead">Snowflake與Databricks在對話式AI上的競賽，正在改變自然語言分析被期待的運行位置。兩家平台在2024年年中先後發布各自的Genie助手，讓對話式查詢從利基附加品變成資料倉儲的預設能力。對大型企業而言，這既是降低分析門檻的機會，也是一次對語義層、治理與評估紀律的全面檢驗——蜂啟諮詢在亞太區的專案經驗是：助手的上限不由廠商決定，而由你自己的資料基礎決定。</p>
<div class="article-tldr"><p><strong>核心要點：</strong>Databricks於2024年5月發布Genie，Snowflake於2024年6月發布自己的Genie，對話式查詢成為資料倉儲預設功能。在整理過的語義層之上，團隊報告例行問題80%到90%的回答成功率——治理到位可超過90%，而裸模式上可能低於60%。分析師通常把70%到80%的時間花在重複報表請求上，可靠的對話層可以吸收這部分工作。</p></div>
<h2 id="為什麼snowflake與databricks的對話式ai競賽很重要">為什麼Snowflake與Databricks的對話式AI競賽很重要？</h2>
<p>這場競賽之所以重要，是因為它改變了自然語言分析被期待的運行位置。當Snowflake和Databricks都自帶助手——Databricks於2024年5月發布Genie，Snowflake在2024年6月的峰會上發布自己的Genie——對話式查詢不再是利基附加品，而成為資料倉儲本身的預設功能。對企業來說，對話式BI的起點不再是一個獨立的產品選型問題，而是平台助手在你的真實資料、真實用戶上表現如何的問題。</p>
<p>底層技術趨勢已經確立。Text-to-SQL系統從新鮮事物走向主流：在元資料清晰的良構企業模式上，現代助手大多數時候都能正確回答，許多團隊報告例行問題80%到90%的回答成功率。但當模式混亂、定義含糊、或問題需要多表聯接與任何模式圖都看不出的業務邏輯時，同樣的技術會迅速退化。這場競賽真正爭奪的，就是彌合這道鴻溝。</p>
<p>還有一個工作流層面的論據。分析師把不成比例的時間花在服務臨時請求上——常見的估計是，重複性報表請求占掉分析師70%到80%的時間。可依賴的對話層不會取代分析師，它吸收例行請求，讓分析師去做真正需要判斷力的問題。這是每個平台廠商都在賣的業務理由，當助手足夠可靠時它是成立的。</p>
<h2 id="對話式資料助手面臨哪些共同挑戰">對話式資料助手面臨哪些共同挑戰？</h2>
<p>第一個挑戰是元資料品質，它是決定一切的那個。平台助手的好壞取決於它對你的資料倉儲的語義理解：表名、欄位含義、聯接路徑、業務定義。把助手指向一個欄位名晦澀、毫無文件說明的原始數倉，得到的是聽起來頭頭是道、卻錯在用戶無法察覺之處的答案。語義層不是可有可無的裝飾；它是可靠助手與負債之間的分界線。</p>
<p>第二個挑戰是治理與權限。平台助手預設繼承資料倉儲層級的存取權，除非另行配置；一個配置不當的助手會把敏感欄位暴露給任何能組織出問題的用戶。企業需要助手遵守的列級與欄位級控制，加上每一次查詢的稽核日誌。在受監管環境裡，這是門檻要求，不是加分項。</p>
<p>第三個挑戰是評估鴻溝。平台示範看起來無懈可擊，因為它們跑在元資料完美的精選模式上。你的生產環境不同——沒有在上線前構建任務專用測試集的團隊，會以最難受的方式發現這道鴻溝：當著業務用戶的面。在你自己的問題、自己的資料、自己的定義上做評估，才是對任何平台助手唯一有意義的檢驗。</p>
<h2 id="什麼把示範與可依賴的助手區分開">什麼把示範與可依賴的助手區分開？</h2>
<p>把示範與可依賴助手區分開的是三件事，沒有一件是模型規模。第一是語義層：對每個術語的含義、每個指標如何計算做出顯式、受治理的定義。當助手查詢的是整理過的語義層而非裸模式，複雜問題的回答可靠性會大幅上升——治理良好的部署例行超過90%的正確率，而裸模式查詢在同一問題集上可能低於60%。</p>
<p>第二是落地與驗證。可依賴的助手展示它的過程：查了哪些表、用了哪些過濾、採用了哪個收入定義、資料最後更新於何時。用戶因此可以抽查答案而不是盲目信任，而信任隨著每一次被驗證的答案複利累積。第三是反饋迴路：一個捕獲錯誤答案、糾正它、並把糾正寫回語義層的機制，讓同樣的錯誤不再復發。平台提供管道；反饋紀律是企業自己的功課。</p>
<p>這就是為什麼平台選擇只是決策的一部分。助手的上限由你的語義層、權限模型與評估實踐決定——無論哪家廠商，這三樣同樣決定任何對話式BI部署的品質。弱語義層上的強助手，跑不過治理良好的語義層上的普通助手。</p>
<p>最後是助手與既有BI投資的關係。當平台助手補充而非替代分析師已經維護的語義層與受治理定義時，它最強大。把助手當作同一套受治理定義之上的新前端的團隊，在各個介面得到一致的答案；放任助手對裸模式自由發揮的團隊，製造出一個平行且互相矛盾的真相。架構決策——助手架在語義層之上，而不是旁邊——塑造所有下游結果。</p>
<h2 id="企業應該如何起步">企業應該如何起步？</h2>
<p>從資料倉儲的精選切片開始，而不是整個數倉。選擇業務最常問的表與指標——收入、銷售管道、庫存、人員編制——只為這些構建語義定義。把平台助手接到這個精選面上，並在任何其他人看到之前，先用從真實用戶收集的問題集做測試。</p>
<p>儘早從真實業務用戶那裡收集問題集。請十幾位營運負責人用他們自己的話寫下今天在問的問題，把它們作為測試集。給助手的答案打分——正確、部分正確、錯誤——並在改進語義層的過程中跟蹤分數。大多數團隊發現第一輪修復是定義問題，不是技術問題：困惑的不是助手，是定義。</p>
<p>然後有節奏地擴展：更多表、更多指標、更多用戶，每次擴展之前都先把權限模型與稽核鏈路就位。蜂啟諮詢這樣的合作夥伴可以幫你構建精選語義層、設計評估測試集、搭建反饋迴路，讓你的平台助手在生產環境中贏得信任，而不是停留在示範裡。</p>
<h2 id="核心要點有哪些">核心要點有哪些？</h2>
<ul>
<li>Snowflake與Databricks都在2024年年中發布Genie助手，對話式查詢成為資料倉儲預設功能</li>
<li>決定回答可靠性的是語義層，不是模型——整理過的定義每次都勝過裸模式</li>
<li>權限與稽核日誌必須在助手到達用戶之前配置好；資料倉儲層級存取不是安全的預設值</li>
<li>從業務用戶那裡構建真實問題集，上線前先對照它給答案打分</li>
<li>治理良好的例行問題預期80%到90%的成功率——並驗證複雜聯接的長尾</li>
<li>運行反饋迴路，把錯誤答案變成語義層修復，讓錯誤不再復發</li>
</ul>
<h2 id="接下來應該怎麼做">接下來應該怎麼做？</h2>
<p>對話式AI競賽的贏家不是選對平台的買家，而是把語義層、權限與評估做紮實的營運者。平台會持續迭代，助手會持續變強，但這三樣決定答案品質的東西不會過時——它們是你無論選誰都需要建的資產。</p>
<p>蜂啟諮詢幫助亞太區企業評估平台對話能力、構建精選語義層與評估體系，並把助手接入既有BI治理框架。如果你正在Snowflake與Databricks之間做選型，或準備讓平台助手在生產環境落地，歡迎預約示範，我們將結合你的資料現狀給出可執行的路線圖。</p>
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
    assert '對話式' in h1 or 'Genie' in h1, "wrong file? h1=" + h1
    if 'id="為什麼snowflake與databricks的對話式ai競賽很重要"' in s:
        print("TW already processed, skip")
        return
    body = TW_BODY.replace('{FAQ_LIST}', build_faq_list(TW_FAQ)).replace('{JSONLD}', build_jsonld(TW_FAQ))
    start = '<p>Snowflake與Databricks'
    assert s.count(start) == 1, f"TW body start: {s.count(start)}"
    rx = re.compile(re.escape(start) + r'.*?(?=\n\n            <nav class="article-nav")', re.S)
    assert len(rx.findall(s)) == 1, "TW body span not 1"
    s = rx.sub(lambda m: body, s, count=1)
    mob = "\n".join(f'                    <a href="#{o}" class="toc-mobile-link">{t}</a>' for o, t in TW_TOC)
    def mob_repl(m):
        return '<div class="toc-mobile-links">\n' + mob + '\n                </div>'
    s2 = re.sub(r'<div class="toc-mobile-links">.*?</div>', mob_repl, s, count=1, flags=re.S)
    assert s2 != s, "tw toc replace failed"
    s = s2
    if 'recommended-card-excerpt"></p>' in s:
        s = fill_excerpts(s, [
            "對話式BI把資料查詢變成聊天裡的一次提問，治理由語義層保障。",
        ], "TW-excerpt")
    integrity(s, [
        '?v=20260901', '預約示範', '"@type": "FAQPage"',
        'id="為什麼snowflake與databricks的對話式ai競賽很重要"', 'id="接下來應該怎麼做"',
        '80%到90%', '語義層', '蜂啟諮詢',
    ], 7, "zh-TW")
    assert '對話式' in body_h1(s) or 'Genie' in body_h1(s)
    save(ZHTW, s)
    print("TW done")

if __name__ == "__main__":
    process_en()
    process_cn()
    process_tw()
    print("slug 15 all done")
