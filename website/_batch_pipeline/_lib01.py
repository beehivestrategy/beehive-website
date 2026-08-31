import re, os, json

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"

def path(slug, lang):
    pref = {"EN": "", "CN": "zh-cn/", "TW": "zh-tw/"}[lang]
    return os.path.join(ROOT, pref + "blog/articles/" + slug + ".html")

def load(slug, lang):
    return open(path(slug, lang), encoding="utf-8").read()

def save(slug, lang, html):
    open(path(slug, lang), "w", encoding="utf-8").write(html)

def body(html):
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', html, re.S)
    return m.group(1) if m else ""

def strip_tags(s):
    s = re.sub(r'<script.*?</script>', ' ', s, flags=re.S)
    s = re.sub(r'<style.*?</style>', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'&nbsp;', ' ', s)

def en_words(h):
    return len(re.findall(r"[A-Za-z][A-Za-z'\-]*", strip_tags(body(h))))

def cjk(h):
    return len(re.findall(r'[\u4e00-\u9fff]', strip_tags(body(h))))

def h2s(h):
    """list of (id, text) for body h2 excluding faq-section-title"""
    out = []
    for m in re.finditer(r'<h2([^>]*)>(.*?)</h2>', body(h), re.S):
        attrs, txt = m.group(1), strip_tags(m.group(2)).strip()
        if 'faq-section-title' in attrs:
            continue
        idm = re.search(r'id="([^"]*)"', attrs)
        out.append((idm.group(1) if idm else None, txt))
    return out

def set_h2_text(html, hid, new_text):
    """Change visible text of body h2 with given id, plus TOC link texts."""
    old = re.search(r'<h2 id="%s"[^>]*>(.*?)</h2>' % re.escape(hid), html, re.S)
    if not old:
        return html, False
    html = html[:old.start()] + '<h2 id="%s">%s</h2>' % (hid, new_text) + html[old.end():]
    # TOC entries referencing this id
    def repl(m):
        return m.group(0).replace('>' + m.group(1) + '<', '>' + new_text + '<')
    html = re.sub(r'<a href="#%s" class="(toc-link|toc-mobile-link)">(.*?)</a>' % re.escape(hid),
                  lambda m: '<a href="#%s" class="%s">%s</a>' % (hid, m.group(1), new_text), html)
    return html, True

def insert_before_faq(html, content):
    """Insert content right before the FAQ section, or before article-nav fallback."""
    m = re.search(r'<article[^>]*id="article-content"[^>]*>', html)
    a0 = m.end()
    fm = re.search(r'<section class="faq-section"', html[a0:])
    nm = re.search(r'<nav class="article-nav"', html[a0:])
    if fm:
        pos = a0 + fm.start()
        anchor = '<section class="faq-section"'
    elif nm:
        pos = a0 + nm.start()
        anchor = '<nav class="article-nav"'
    else:
        end = html.index('</article>', a0)
        pos = end
        anchor = '</article>'
    assert html[pos:pos+len(anchor)] == anchor
    return html[:pos] + content + html[pos:]

def wrap_faq_h3(html):
    """Wrap each faq question button in <h3 class="faq-question-title">."""
    def repl(m):
        if '<h3 class="faq-question-title">' in m.group(0):
            return m.group(0)
        inner = m.group(1)
        return ('<h3 class="faq-question-title">\n' + inner.strip('\n') +
                '\n</h3>')
    pat = re.compile(r'<div class="faq-item">\s*(<button class="faq-question".*?</button>)', re.S)
    return pat.sub(repl, html)

def fix_rec_hrefs(html):
    def repl(m):
        href = m.group(1)
        if not href.startswith('/'):
            href = '/' + href
        return m.group(0).replace('href="%s"' % m.group(1), 'href="%s"' % href)
    return re.sub(r'<a href="((?:blog|zh-cn|zh-tw)[^"]*)"([^>]*class="recommended-card")', repl, html)

def faq_after_ld(html, qa):
    """Insert FAQPage ld+json right after faq section's closing </section>."""
    m = re.search(r'class="faq-section".*?</section>', html, re.S)
    assert m, "no faq section"
    end = m.end()
    ent = []
    for q, a in qa:
        ent.append({"@type": "Question", "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a}})
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ent}
    js = json.dumps(data, ensure_ascii=False)
    js = js.replace('</', '<\\/')
    block = '\n            <script type="application/ld+json">%s</script>\n' % js
    return html[:end] + block + html[end:]

FAQ_ITEM_TMPL = """                    <div class="faq-item">
                        <h3 class="faq-question-title">
<button class="faq-question" aria-expanded="false">
                            <span class="faq-question-text"><span class="faq-number">{n}</span><span>{q}</span></span>
                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                        </button>
</h3>
<div class="faq-answer" role="region"><div class="faq-answer-inner">{a}</div></div>
                    </div>
"""

def build_faq_section(title, qa):
    items = "".join(FAQ_ITEM_TMPL.format(n=i+1, q=q, a=a) for i, (q, a) in enumerate(qa))
    return f"""
            <section class="faq-section" id="faq" aria-label="Frequently Asked Questions">
                <h2 class="faq-section-title">{title}</h2>
                <div class="faq-list">
{items}                </div>
            </section>

"""


def process(slug, h2fix, adds=None, wrap=True, fix_rec=True,
            add_faq=None, cta_fix=None, tag=""):
    adds = adds or {}
    out = {}
    for lang in ("EN", "CN", "TW"):
        html = load(slug, lang)
        before = en_words(html) if lang == "EN" else cjk(html)
        if fix_rec:
            html = fix_rec_hrefs(html)
        if wrap:
            html = wrap_faq_h3(html)
        html = sync_toc(html)
        for hid, new in h2fix.get(lang, []):
            html, ok = set_h2_text(html, hid, new)
            if not ok:
                print("  !! H2 NOT FOUND", slug, lang, hid)
        add = adds.get(lang)
        if add:
            html = insert_before_faq(html, add)
        if add_faq and lang in add_faq:
            title, qa = add_faq[lang]
            html = insert_before_faq(html, build_faq_section(title, qa))
            html = faq_after_ld(html, qa)
        if cta_fix and lang in cta_fix:
            old, new = cta_fix[lang]
            if old in html:
                html = html.replace(old, new, 1)
            else:
                print("  !! CTA NOT FOUND", slug, lang)
        save(slug, lang, html)
        after = en_words(html) if lang == "EN" else cjk(html)
        out[lang] = (before, after)
        print("   %s %s %d -> %d" % (tag, lang, before, after))
    return out


def sync_toc(html):
    """Make every TOC entry text match its target h2's visible text."""
    texts = {}
    for m in re.finditer(r'<h2 id="([^"]*)"[^>]*>(.*?)</h2>', body(html), re.S):
        texts[m.group(1)] = strip_tags(m.group(2)).strip()
    def repl(m):
        hid, cls = m.group(1), m.group(2)
        t = texts.get(hid)
        if not t:
            return m.group(0)
        return '<a href="#%s" class="%s">%s</a>' % (hid, cls, t)
    return re.sub(r'<a href="#([^"]*)" class="(toc-link|toc-mobile-link)">(.*?)</a>', repl, html)
