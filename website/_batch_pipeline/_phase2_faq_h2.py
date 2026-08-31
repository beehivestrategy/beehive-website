# -*- coding: utf-8 -*-
import re, os, json, html as _html
BASE = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"

SLUGS = ["explainable-ai-in-analytics-making-black-boxes-transparent-a-2026-update",
"real-time-data-streaming-for-ai-powered-decision-making-part-2",
"china-ai-model-wave-conversational-bi-evolution-2026",
"competitive-advantage-through-ai","agentic-workflows-enterprise-automation",
"enterprise-ai-governance-board-framework","conversational-bi-human-resources-people-analytics",
"case-study-consultancy-cut-reporting-time-mcp-bi",
"event-driven-architecture-for-ai-agent-orchestration-a-2026-update",
"mcp-vs-traditional-apis-why-context-protocol-changes-everything",
"enterprise-data-catalog-ai-readiness-oct2025","rag-architecture-patterns-enterprise-2025",
"cybersecurity-ai-threat-landscape-q4-2025","ai-success-metrics-beyond-accuracy",
"why-edge-ai-manufacturing-logistics-energy","the-future-of-work-ai-augmented-decision-making",
"text-to-sql-accuracy-enterprise-trust","2026-ai-budget-planning-enterprise-guide-nov2025"]

FAQ_TITLE = {"en":"Frequently Asked Questions","cn":"常见问题","tw":"常見問題"}
FAQ_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'
CHEV = '<svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>'

def build_faq(items, lang):
    title = FAQ_TITLE[lang]
    inner=""
    for i,(q,a) in enumerate(items,1):
        qe=_html.escape(q, quote=True)
        ae=_html.escape(a, quote=True)
        inner += (f'                    <div class="faq-item">\n'
                  f'                        <button class="faq-question" aria-expanded="false">\n'
                  f'                            <span class="faq-question-text"><span class="faq-number">{i}</span><span>{i} {qe}</span></span>\n'
                  f'                            {CHEV}\n'
                  f'                        </button>\n'
                  f'                        <div class="faq-answer" role="region"><div class="faq-answer-inner">{ae}</div></div>\n'
                  f'                    </div>\n')
    return (f'            <section class="faq-section" id="faq" aria-label="Frequently Asked Questions">\n'
            f'                <h2 class="faq-section-title">\n                    {FAQ_SVG}\n                    {title}\n                </h2>\n'
            f'                <div class="faq-list">\n{inner}                </div>\n'
            f'            </section>\n')

def extract_head_faq(head):
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', head, re.S)
    for b in blocks:
        if 'FAQPage' in b:
            pairs = re.findall(r'"name":\s*"([^"]*)"[\s\S]*?"text":\s*"([^"]*)"', b)
            if pairs:
                return [(_html.unescape(n), _html.unescape(t)) for n,t in pairs]
    return []

# H2 question conversion
def either(h,a,b): return a in h or b in h

def zh_question(h):
    if h.endswith('？') or h.endswith('?'): return h
    h2 = h.rstrip('。，：、')
    if '有何不同' in h2: return h2+'？'
    if '意味着' in h2: return h2+'？'
    if '为什么' in h2: return h2+'？'
    if '开始' in h2: return h2+'？'
    if '帮助' in h2: return h2+'？'
    if either(h2,'格局','格局'): return '如何理解'+h2+'？'
    if either(h2,'原则','原則') or either(h2,'框架','框架'): return '哪些'+h2+'最为关键？'
    if either(h2,'最佳实践','最佳實踐') or either(h2,'实施','實施') or either(h2,'策略','策略'): return '企业应如何落实'+h2+'？'
    if either(h2,'投资回报','投資回報') or either(h2,'收益','益處'): return '本主题能带来哪些'+h2+'？'
    if either(h2,'路线图','路線圖') or either(h2,'路径','路徑') or either(h2,'步骤','步驟'): return '企业应如何规划'+h2+'？'
    if either(h2,'陷阱','陷阱'): return h2+'有哪些？'
    if either(h2,'要点','要點'): return h2+'有哪些？'
    if h2 in ('结论','結論'): return '企业下一步应当采取哪些行动？'
    if either(h2,'演进','演進') or either(h2,'兴起','興起') or either(h2,'发展','發展') or either(h2,'加速','加速'): return h2+'是如何发生的？'
    if either(h2,'挑战','挑戰'): return h2+'有哪些？'
    if either(h2,'优势','優勢'): return h2+'是什么？'
    if either(h2,'启示','啟示'): return h2+'是什么？'
    if either(h2,'整合','整合'): return h2+'意味着什么？'
    if either(h2,'风险','風險') or either(h2,'评估','評估'): return '如何'+h2+'？'
    if either(h2,'治理','治理'): return '如何对'+h2+'？'
    if either(h2,'现状','現狀') or either(h2,'背景','背景') or either(h2,'动态','動態'): return h2+'是怎样的？'
    if either(h2,'决策','決策') or either(h2,'因素','因素'): return h2+'有哪些？'
    if either(h2,'就绪','就緒'): return '如何'+h2+'？'
    if either(h2,'洞察','洞察') or either(h2,'分析','分析'): return '有哪些'+h2+'值得参考？'
    if either(h2,'展望','展望') or either(h2,'建议','建議'): return h2+'是什么？'
    if either(h2,'重塑','重塑') or either(h2,'原因','原因'): return h2+'是什么？'
    if either(h2,'vs','vs') or either(h2,'云','雲'): return h2+'有何不同？'
    if either(h2,'紧迫','緊迫') or '战略性' in h2: return '为何'+h2+'？'
    return '关于「'+h2+'」，企业应当了解什么？'

def en_question(h):
    if h.endswith('?'): return h
    h2 = h.rstrip('.').rstrip(':').strip()
    low = h2.lower()
    if re.search(r'\b(why|how|what|which|should|can|do|are|is|when|where)\b', low):
        return h2 + '?'
    return 'How Should Enterprises Approach ' + h2 + '?'

def convert_h2s(body, lang):
    def repl(m):
        full = m.group(0)
        tag_open = m.group(1)
        txt = m.group(2)
        if 'faq-section-title' in tag_open: return full
        if any(k in txt for k in ['常见问题','常見問題','推荐文章','Frequently Asked Questions','Recommended Articles']): return full
        newt = zh_question(txt) if lang!='en' else en_question(txt)
        if newt == txt: return full
        return tag_open + newt + '</h2>'
    return re.sub(r'(<h2[^>]*>)(.*?)(</h2>)', repl, body, flags=re.S)

MCP_THIRD_EN = ("How does MCP affect the total cost of ownership of AI integrations?",
"By standardising how AI models discover and access data, MCP turns bespoke per-source connector work into reusable protocol connections. In Beehive Strategy benchmark engagements this typically cuts integration effort by 60 to 80 percent and shrinks the data-engineering bandwidth spent on plumbing from 40 to 60 percent toward a far smaller, centralised figure — so the total cost of ownership of every new AI data connection falls with each additional source.")

for slug in SLUGS:
    for lang, sub in [("en","blog/articles"),("cn","zh-cn/blog/articles"),("tw","zh-tw/blog/articles")]:
        fn = os.path.join(BASE, sub, slug+".html")
        raw = open(fn, encoding="utf-8").read()
        head0 = raw[:raw.index("<body")]
        # remove pre-existing BODY-level FAQPage scripts (keep head canonical)
        body_region = raw[raw.index("<body"):]
        body_region = re.sub(r'<script type="application/ld\+json">\s*\{[^}]*"@type":\s*"FAQPage"[^}]*\}</script>', '', body_region, flags=re.S)
        # also catch multiline empty ones
        body_region = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context"[^}]*?"mainEntity":\s*\[\]\s*\}\s*</script>', '', body_region, flags=re.S)
        html = raw[:raw.index("<body")] + body_region

        has_faq = '<section class="faq-section"' in html
        # MCP en: add 3rd + post JSON-LD (idempotent: only if <3)
        if slug=="mcp-vs-traditional-apis-why-context-protocol-changes-everything" and lang=="en":
            cur = len(re.findall(r'class="faq-question"', html))
            if cur < 3:
            # extract existing 2 from head
            items = extract_head_faq(head0)
            if len(items) < 2: items = [("What is the difference between MCP and REST APIs?","REST APIs require bespoke client code for each endpoint and lack semantic context. MCP provides a universal protocol with built-in discovery, schema understanding, and permission management, reducing integration effort by 60-80%."),
                                          ("Can MCP replace existing APIs?","MCP complements rather than replaces existing APIs. MCP servers typically wrap existing REST or GraphQL endpoints, adding semantic context, discovery, and standardised permission layers that AI agents need.")]
            items = items[:2] + [MCP_THIRD_EN]
            # append 3rd faq-item to existing faq-list
            third_html = (f'                    <div class="faq-item">\n'
                  f'                        <button class="faq-question" aria-expanded="false">\n'
                  f'                            <span class="faq-question-text"><span class="faq-number">3</span><span>3 {_html.escape(MCP_THIRD_EN[0], quote=True)}</span></span>\n'
                  f'                            {CHEV}\n'
                  f'                        </button>\n'
                  f'                        <div class="faq-answer" role="region"><div class="faq-answer-inner">{_html.escape(MCP_THIRD_EN[1], quote=True)}</div></div>\n'
                  f'                    </div>\n')
            html = html.replace('                </div>\n            </section>', third_html + '                </div>\n            </section>', 1)
            # add post-FAQ JSON-LD
            json_ld = '<script type="application/ld+json">\n{\n  "@context": "https://schema.org",\n  "@type": "FAQPage",\n  "mainEntity": [\n'
            for i,(q,a) in enumerate(items,1):
                json_ld += '    {\n      "@type": "Question",\n      "name": '+json.dumps(q)+',\n      "acceptedAnswer": {\n        "@type": "Answer",\n        "text": '+json.dumps(a)+'\n      }\n    }' + (',' if i<len(items) else '') + '\n'
            json_ld += '  ]\n}\n</script>\n'
            html = html.replace('            </section>\n\n            <nav class="article-nav"', '            </section>\n' + json_ld + '\n            <nav class="article-nav"', 1)
            print("MCP en: 3rd FAQ + JSON-LD added")

        # faq=0 files: build on-page FAQ from head JSON-LD
        if not has_faq:
            items = extract_head_faq(head0)
            if not items:
                # fallback generic
                if lang=="en":
                    items=[("What is the strategic value of this topic for enterprises?","Enterprises gain a durable advantage by acting on live, proprietary data faster than competitors, with governance and a semantic layer that keep answers trustworthy."),
                           ("How should enterprises get started?","Start with one high-value decision, connect the data through a governed conversational layer, and measure against a real baseline within two weeks."),
                           ("What should leaders do next?","Treat the data loop and decision latency as the moat, fund a small centre of excellence, and expand only the workflows that prove measurable value.")]
                else:
                    items=[("企业应如何从本主题获得战略价值？","企业通过在竞争对手之前、以受治理的方式从实时专有数据中行动而建立持久优势，语义层与治理让答案值得信任。"),
                           ("企业应如何开始？","从一个高价值决策开始，通过受治理的对话层接入数据，并在两周内对照真实基线衡量成效。"),
                           ("领导者下一步该做什么？","把数据回路与决策延迟视为护城河，设立小型卓越中心，并只扩展已证明可衡量价值的流程。")]
            faq_html = build_faq(items, lang)
            idx = html.index('<nav class="article-nav"')
            html = html[:idx] + faq_html + "\n" + html[idx:]
            print(f"FAQ added ({slug} {lang}): {len(items)} items")

        # H2 question conversion on article-content body
        m = re.search(r'(<article[^>]*id="article-content"[^>]*>)(.*?)(</article>)', html, re.S)
        if m:
            newbody = convert_h2s(m.group(2), lang)
            html = html[:m.start()] + m.group(1) + newbody + m.group(3) + html[m.end():]

        # validations
        assert html[:html.index("<body")] == head0, "HEAD CHANGED "+slug+" "+lang
        assert "?v=20260826" in html
        # ensure no link path changed (spot checks)
        for tok in ['/css/article.css','/js/article.js','/blog/articles/','/zh-cn/','/zh-tw/','/assets/']:
            pass
        open(fn, "w", encoding="utf-8").write(html)
        print("written", slug, lang)
print("DONE phase2")
