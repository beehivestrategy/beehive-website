# -*- coding: utf-8 -*-
"""
Phase 2 (final, idempotent): normalize FAQ + JSON-LD + question H2s for all 54
batch_002 article files. Never touches <head>, footer, share buttons, link paths,
or status.json. Re-runnable: deterministic output.
"""
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

def looks_cjk(s):
    return any('一' <= c <= '鿿' for c in s)

def looks_en(s):
    return not looks_cjk(s)

def slug_to_title(slug):
    t = re.sub(r'-\d{4}$','',slug)
    t = re.sub(r'-(a|part-\d+)$','',t)
    t = t.replace('-',' ').strip()
    return t

# ---------- FAQ building ----------
def build_faq(items, lang, json_ld=None):
    title = FAQ_TITLE[lang]
    inner=""
    for i,(q,a) in enumerate(items,1):
        qe=_html.escape(q, quote=True)
        ae=_html.escape(a, quote=True)
        inner += (f'                    <div class="faq-item">\n'
                  f'                        <button class="faq-question" aria-expanded="false">\n'
                  f'                            <span class="faq-question-text"><span class="faq-number">{i}</span><span>{qe}</span></span>\n'
                  f'                            {CHEV}\n'
                  f'                        </button>\n'
                  f'                        <div class="faq-answer" role="region"><div class="faq-answer-inner">{ae}</div></div>\n'
                  f'                    </div>\n')
    sec = (f'            <section class="faq-section" id="faq" aria-label="Frequently Asked Questions">\n'
           f'                <h2 class="faq-section-title">\n                    {FAQ_SVG}\n                    {title}\n                </h2>\n'
           f'                <div class="faq-list">\n{inner}                </div>\n'
           f'            </section>\n')
    if json_ld:
        return sec + json_ld + "\n"
    return sec

def build_json_ld(items):
    out = '<script type="application/ld+json">\n{\n  "@context": "https://schema.org",\n  "@type": "FAQPage",\n  "mainEntity": [\n'
    for i,(q,a) in enumerate(items,1):
        out += ('    {\n      "@type": "Question",\n      "name": '+json.dumps(q)+
                ',\n      "acceptedAnswer": {\n        "@type": "Answer",\n        "text": '+
                json.dumps(a)+'\n      }\n    }' + (',' if i<len(items) else '') + '\n')
    out += '  ]\n}\n</script>'
    return out

# ---------- head / on-page extraction ----------
def extract_head_faq(head):
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', head, re.S):
        if 'FAQPage' in b:
            pairs = re.findall(r'"name":\s*"([^"]*)"[\s\S]*?"text":\s*"([^"]*)"', b)
            if pairs:
                return [(_html.unescape(n), _html.unescape(t)) for n,t in pairs]
    return []

def extract_onpage_faq(html):
    items=[]
    for chunk in re.findall(r'<div class="faq-item">(.*?)(?=<div class="faq-item">|</div>\s*</section>)', html, re.S):
        qm=re.search(r'<span class="faq-number">.*?</span>\s*<span>(.*?)</span>', chunk, re.S)
        am=re.search(r'<div class="faq-answer-inner">(.*?)</div>', chunk, re.S)
        if qm and am:
            q=_html.unescape(re.sub(r'^\d+\s*','',qm.group(1)).strip())
            a=_html.unescape(am.group(1).strip())
            items.append((q,a))
    return items

def head_has_faq_match(head, lang):
    hf = extract_head_faq(head)
    if not hf: return []
    if lang=="en":
        ok = all(looks_en(q) for q,_ in hf)
    else:
        ok = all(looks_cjk(q) for q,_ in hf)
    return hf if (ok and len(hf)>=3) else []

# ---------- generic fallback FAQ ----------
def fallback_faq(lang, topic):
    if lang=="en":
        return [(f"What is the strategic value of {topic} for enterprises?",
                 f"Enterprises gain a durable advantage by acting on live, proprietary data faster than competitors, with governance and a semantic layer that keep answers trustworthy. {topic.title()} turns raw signals into decisions leaders can defend."),
                (f"How should enterprises get started with {topic}?",
                 f"Start with one high-value decision, connect the data through a governed conversational layer, and measure against a real baseline within two weeks. Prove value on a narrow slice before scaling."),
                (f"What should leaders do next on {topic}?",
                 f"Treat the data loop and decision latency as the moat, fund a small centre of excellence, and expand only the workflows that prove measurable value. Avoid blanket platform bets without a business metric attached.")]
    elif lang=="cn":
        return [(f"企业应如何从{topic}获得战略价值？",
                 f"企业通过在竞争对手之前、以受治理的方式从实时专有数据中行动而建立持久优势，语义层与治理让答案值得信任。{topic}把原始信号转化为领导者可以支撑的决策。"),
                (f"企业应如何开始{topic}？",
                 f"从一个高价值决策开始，通过受治理的对话层接入数据，并在两周内对照真实基线衡量成效。先在窄场景证明价值，再扩展。"),
                (f"领导者下一步应当如何在{topic}上行动？",
                 f"把数据回路与决策延迟视为护城河，设立小型卓越中心，并只扩展已证明可衡量价值的流程。不要在没有业务指标支撑的情况下盲目铺开平台。")]
    else:
        return [(f"企業應如何從{topic}獲得戰略價值？",
                 f"企業透過在競爭對手之前、以受治理的方式從即時專有資料中行動而建立持久優勢，語意層與治理讓答案值得信任。{topic}把原始訊號轉化為領導者可以支撐的決策。"),
                (f"企業應如何開始{topic}？",
                 f"從一個高價值決策開始，透過受治理的對話層接入資料，並在兩週內對照真實基線衡量成效。先在窄場景證明價值，再擴展。"),
                (f"領導者下一步應當如何在{topic}上行動？",
                 f"把資料迴路與決策延遲視為護城河，設立小型卓越中心，並只擴展已證明可衡量價值的流程。不要在沒有業務指標支撐的情況下盲目鋪開平台。")]

# ---------- H2 question conversion ----------
def zh_question(h):
    if h.endswith('？') or h.endswith('?'): return h
    h2 = h.rstrip('。，：、')
    if '有何不同' in h2: return h2+'？'
    if '意味着' in h2 or '意味著' in h2: return h2+'？'
    if '为什么' in h2 or '為什麼' in h2: return h2+'？'
    if '如何' in h2 or '怎樣' in h2 or '怎么' in h2: return h2+'？'
    if '是否' in h2: return h2+'？'
    if '开始' in h2 or '開始' in h2: return h2+'？'
    if '帮助' in h2 or '幫助' in h2: return h2+'？'
    if '格局' in h2: return '如何理解'+h2+'？'
    if '原则' in h2 or '原則' in h2 or '框架' in h2: return '哪些'+h2+'最为关键？'
    if '最佳实践' in h2 or '最佳實踐' in h2 or '实施' in h2 or '實施' in h2 or '策略' in h2: return '企业应如何落实'+h2+'？'
    if '投资回报' in h2 or '投資回報' in h2 or '收益' in h2 or '益處' in h2: return '本主题能带来哪些'+h2+'？'
    if '路线图' in h2 or '路線圖' in h2 or '路径' in h2 or '路徑' in h2 or '步骤' in h2 or '步驟' in h2: return '企业应如何规划'+h2+'？'
    if '陷阱' in h2: return h2+'有哪些？'
    if '要点' in h2 or '要點' in h2: return h2+'有哪些？'
    if h2 in ('结论','結論'): return '企业下一步应当采取哪些行动？'
    if '演进' in h2 or '演進' in h2 or '兴起' in h2 or '興起' in h2 or '发展' in h2 or '發展' in h2 or '加速' in h2: return h2+'是如何发生的？'
    if '挑战' in h2 or '挑戰' in h2: return h2+'有哪些？'
    if '优势' in h2 or '優勢' in h2: return h2+'是什么？'
    if '启示' in h2 or '啟示' in h2: return h2+'是什么？'
    if '整合' in h2 or '整合' in h2: return h2+'意味着什么？'
    if '风险' in h2 or '風險' in h2 or '评估' in h2 or '評估' in h2: return '如何'+h2+'？'
    if '治理' in h2 or '治理' in h2: return '如何对'+h2+'？'
    if '现状' in h2 or '現狀' in h2 or '背景' in h2 or '动态' in h2 or '動態' in h2: return h2+'是怎样的？'
    if '决策' in h2 or '決策' in h2 or '因素' in h2: return h2+'有哪些？'
    if '就绪' in h2 or '就緒' in h2: return '如何'+h2+'？'
    if '洞察' in h2 or '分析' in h2: return '有哪些'+h2+'值得参考？'
    if '展望' in h2 or '建议' in h2 or '建議' in h2: return h2+'是什么？'
    if '重塑' in h2 or '原因' in h2: return h2+'是什么？'
    if 'vs' in h2 or '雲' in h2 or '云' in h2: return h2+'有何不同？'
    if '紧迫' in h2 or '緊迫' in h2 or '战略性' in h2: return '为何'+h2+'？'
    return '关于「'+h2+'」，企业应当了解什么？'

def en_question(h):
    if h.endswith('?'): return h
    h2 = h.rstrip('.').rstrip(':').strip()
    low = h2.lower()
    if re.search(r'\b(why|how|what|which|should|can|do|are|is|when|where|does|will)\b', low):
        return h2 + '?'
    return 'How Should Enterprises Approach ' + h2 + '?'

GUARD_KW = ['常见问题','常見問題','推荐文章','推薦文章','Recommended Articles','Recommended',
            'Book a Demo','预约演示','預約示範','Book','Demo','演示','示範','CTA','相关','相關',
            'Frequently Asked Questions','faq-section-title']

def convert_h2s(body, lang):
    def repl(m):
        full = m.group(0); tag_open = m.group(1); txt = m.group(2).strip()
        if 'faq-section-title' in tag_open: return full
        if any(k in txt for k in GUARD_KW): return full
        newt = zh_question(txt) if lang!='en' else en_question(txt)
        if newt == txt: return full
        return tag_open + newt + '</h2>'
    return re.sub(r'(<h2[^>]*>)(.*?)(</h2>)', repl, body, flags=re.S)

# ---------- counting helpers ----------
def article_region(html):
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', html, re.S)
    return m.group(1) if m else html

def en_words(html):
    txt = re.sub(r'<[^>]+>',' ', article_region(html))
    txt = _html.unescape(txt)
    return len(re.findall(r"[A-Za-z0-9']+", txt))

def zh_cjk(html):
    txt = re.sub(r'<[^>]+>',' ', article_region(html))
    txt = _html.unescape(txt)
    return sum(1 for c in txt if '一'<=c<='鿿')

def faq_count(html):
    return len(re.findall(r'class="faq-question"', html))

# ---------- main ----------
report = []
for slug in SLUGS:
    topic = slug_to_title(slug)
    for lang, sub in [("en","blog/articles"),("cn","zh-cn/blog/articles"),("tw","zh-tw/blog/articles")]:
        fn = os.path.join(BASE, sub, slug+".html")
        raw = open(fn, encoding="utf-8").read()
        head0 = raw[:raw.index("<body")]
        before_words = en_words(raw) if lang=="en" else zh_cjk(raw)
        before_faq = faq_count(raw)
        before_body_ld = ('FAQPage' in raw[raw.index('<body'):])

        body_region = raw[raw.index("<body"):]
        # strip any body-level FAQPage scripts (will re-add correct one if needed)
        def _strip_faq(m):
            return '' if 'FAQPage' in m.group(1) else m.group(0)
        body_region = re.sub(r'<script type="application/ld\+json">(.*?)</script>', _strip_faq, body_region, flags=re.S)
        html = head0 + body_region

        has_faq = '<section class="faq-section"' in html
        hf = head_has_faq_match(head0, lang)

        # canonical FAQ source
        if hf:
            items = hf
            add_body_ld = False
        elif has_faq:
            items = extract_onpage_faq(html)
            if len(items) < 3:
                items = fallback_faq(lang, topic)
            add_body_ld = True
        else:
            items = fallback_faq(lang, topic)
            add_body_ld = True

        # ensure >=3
        if len(items) < 3:
            items = fallback_faq(lang, topic)

        json_ld = build_json_ld(items) if add_body_ld else None
        faq_html = build_faq(items, lang, json_ld)

        if has_faq:
            html = re.sub(r'<section class="faq-section"[^>]*>.*?</section>', faq_html, html, count=1, flags=re.S)
        else:
            rec = re.search(r'<section class="recommended-section"', html)
            if rec:
                idx = rec.start()
            else:
                idx = html.index('<nav class="article-nav"')
            html = html[:idx] + faq_html + "\n" + html[idx:]

        # H2 question conversion inside article-content
        m = re.search(r'(<article[^>]*id="article-content"[^>]*>)(.*?)(</article>)', html, re.S)
        if m:
            newbody = convert_h2s(m.group(2), lang)
            html = html[:m.start()] + m.group(1) + newbody + m.group(3) + html[m.end():]

        # validations
        assert html[:html.index("<body")] == head0, "HEAD CHANGED "+slug+" "+lang
        assert "?v=20260826" in html, "?v missing "+slug+" "+lang

        open(fn, "w", encoding="utf-8").write(html)

        after_words = en_words(html) if lang=="en" else zh_cjk(html)
        after_faq = faq_count(html)
        report.append((slug, lang, before_words, after_words, before_faq, after_faq, ("Y" if add_body_ld else "N")))
        print(f"{slug} [{lang}] words {before_words}->{after_words} faq {before_faq}->{after_faq} ld={'Y' if add_body_ld else 'N'}")

print("\n===== REPORT =====")
for r in report:
    print(r)
print("DONE phase2_final")
