#!/usr/bin/env python3
"""Shared helpers for bringing gbatch_003 articles to GEO/SEO standard."""
import re, os, json, sys
import opencc

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
LANGS = {"EN": "", "zh-CN": "zh-cn/", "zh-TW": "zh-tw/"}
CJK = re.compile(r'[\u4e00-\u9fff]')
WORD = re.compile(r"[A-Za-z][A-Za-z'\-]*")
S2TWP = opencc.OpenCC('s2twp')
T2S = opencc.OpenCC('t2s')

def path(slug, lang):
    return os.path.join(ROOT, LANGS[lang] + "blog/articles/" + slug + ".html")

def load(slug, lang):
    with open(path(slug, lang), encoding="utf-8") as f:
        return f.read()

def save(slug, lang, text):
    with open(path(slug, lang), "w", encoding="utf-8") as f:
        f.write(text)

def strip_tags(h):
    h = re.sub(r'<script.*?</script>', ' ', h, flags=re.S)
    h = re.sub(r'<style.*?</style>', ' ', h, flags=re.S)
    h = re.sub(r'<[^>]+>', ' ', h)
    return h

def words(t):
    return len(WORD.findall(strip_tags(t)))

def cjk(t):
    return len(CJK.findall(strip_tags(t)))

# ---------- body ----------
BODY_RE = re.compile(r'(<article[^>]*id="article-content"[^>]*>)(.*?)(</article>)', re.S)

def get_body(html):
    m = BODY_RE.search(html)
    return m.group(2) if m else None

def set_body(html, inner):
    return BODY_RE.sub(lambda m: m.group(1) + inner + m.group(3), html, count=1)

# ---------- TOC ----------
def h2_list(body):
    out = []
    for m in re.finditer(r'<h2([^>]*)>(.*?)</h2>', body, re.S):
        attrs = m.group(1)
        idm = re.search(r'id="([^"]+)"', attrs)
        if not idm:
            continue
        txt = re.sub(r'\s+', ' ', strip_tags(m.group(2))).strip()
        out.append((idm.group(1), txt))
    return out

def sync_toc(html):
    body = get_body(html)
    items = h2_list(body)
    # dedupe ids defensively
    seen, fixed = {}, []
    for i, (i_id, t) in enumerate(items):
        nid = i_id
        if nid in seen:
            nid = nid + "-" + str(seen[nid] + 1)
        seen[i_id] = seen.get(i_id, 0) + 1
        fixed.append((nid, t))
    mob = "\n".join('                    <a href="#%s" class="toc-mobile-link">%s</a>' % (i, t) for i, t in fixed)
    side = "\n".join('                    <a href="#%s" class="toc-link">%s</a>' % (i, t) for i, t in fixed)
    html = re.sub(r'(<div class="toc-mobile-links">)(.*?)(</div>)',
                  lambda m: m.group(1) + "\n" + mob + "\n                " + m.group(3), html, count=1, flags=re.S)
    html = re.sub(r'(<nav class="toc-links">)(.*?)(</nav>)',
                  lambda m: m.group(1) + "\n" + side + "\n                " + m.group(3), html, count=1, flags=re.S)
    return html

# ---------- FAQ ----------
def faq_span(qid=None):
    pass

def build_faq(qas, title="Frequently Asked Questions"):
    """qas: list of (question, answer)."""
    parts = []
    for i, (q, a) in enumerate(qas, 1):
        parts.append('''                    <div class="faq-item">
                        <h3 class="faq-question-heading" style="margin:0;font-weight:inherit;font-size:inherit;line-height:inherit;"><button class="faq-question" aria-expanded="false">
                            <span class="faq-question-text"><span class="faq-number">%d</span><span>%s</span></span>
                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                        </button></h3>
                        <div class="faq-answer" role="region"><div class="faq-answer-inner">%s</div></div>
                    </div>''' % (i, q, a))
    return '''            <section class="faq-section" id="faq" aria-label="%s">
                <h2 class="faq-section-title">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                    %s
                </h2>
                <div class="faq-list">
%s
                </div>
            </section>''' % (title, title, "\n".join(parts))

FAQ_SEC_RE = re.compile(r'<section[^>]*class="[^"]*faq-section[^"]*"[^>]*>.*?</section>', re.S)

def parse_faq(html):
    m = FAQ_SEC_RE.search(html)
    if not m:
        return []
    sec = m.group(0)
    qas = []
    for item in re.finditer(r'<div class="faq-item">(.*?)</div>\s*(?=<div class="faq-item">|</div>\s*</section>)', sec, re.S):
        blk = item.group(1)
        q = re.search(r'<span class="faq-question-text">.*?<span>(.*?)</span>\s*</span>', blk, re.S)
        a = re.search(r'<div class="faq-answer-inner">(.*?)</div>', blk, re.S)
        if q and a:
            qas.append((re.sub(r'\s+', ' ', strip_tags(q.group(1))).strip(),
                        re.sub(r'\s+', ' ', strip_tags(a.group(1))).strip()))
    if not qas:
        for item in re.finditer(r'<div class="faq-item">(.*?)(?=<div class="faq-item">|\Z)', sec, re.S):
            blk = item.group(1)
            q = re.search(r'<span class="faq-question-text">.*?<span>(.*?)</span>\s*</span>', blk, re.S)
            a = re.search(r'<div class="faq-answer-inner">(.*?)</div>', blk, re.S)
            if q and a:
                qas.append((re.sub(r'\s+', ' ', strip_tags(q.group(1))).strip(),
                            re.sub(r'\s+', ' ', strip_tags(a.group(1))).strip()))
    return qas

def set_faq(html, qas, title):
    """Replace existing FAQ section (or insert before article-nav) with a rebuilt one."""
    new = build_faq(qas, title)
    if FAQ_SEC_RE.search(html):
        return FAQ_SEC_RE.sub(lambda m: new, html, count=1)
    m = re.search(r'<nav class="article-nav"', html)
    if m:
        return html[:m.start()] + new + "\n\n            " + html[m.start():]
    raise RuntimeError("no FAQ anchor")

def wrap_faq_h3(html):
    """Ensure each faq-question button is wrapped in an <h3>."""
    def rep(m):
        inner = m.group(1)
        if '<h3' in inner:
            return m.group(0)
        return ('<h3 class="faq-question-heading" style="margin:0;font-weight:inherit;'
                'font-size:inherit;line-height:inherit;">' + inner + '</h3>')
    html = re.sub(r'(<div class="faq-item">\s*)(<button class="faq-question".*?</button>)',
                  lambda m: m.group(1) + rep(type('x', (), {'group': lambda s, i: [None, m.group(2)][i]})()),
                  html, flags=re.S)
    return html

def dedupe_number(html):
    """Remove duplicated leading number inside the question span (e.g. '1 1 What is...')."""
    def rep(m):
        txt = m.group(2)
        txt = re.sub(r'^\s*%s\s+' % re.escape(m.group(1)), '', txt)
        return m.group(0).replace('>' + m.group(1) + ' ', '>')
    def rep2(m):
        num, q = m.group(1), m.group(2)
        q2 = re.sub(r'^\s*%s\s+' % re.escape(num), '', q)
        if q2 == q:
            return m.group(0)
        return m.group(0)[:m.start(2) - m.start(0)] + q2 + m.group(0)[m.end(2) - m.start(0):]
    return re.sub(r'<span class="faq-number">(\d+)</span><span>(.*?)</span>', rep2, html, flags=re.S)

# ---------- JSON-LD ----------
LD_RE = re.compile(r'<script type="application/ld\+json"[^>]*>.*?</script>', re.S)

def _ld_block(qas, url):
    ent = []
    for q, a in qas:
        ent.append({"@type": "Question", "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a}})
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ent}
    return ('<script type="application/ld+json">\n' +
            json.dumps(data, ensure_ascii=False, indent=2) + '\n</script>')

def ensure_faq_ld(html, url):
    """Place FAQPage JSON-LD immediately after the FAQ section's closing tag.
    Never touches <head>. Replaces any existing body-level FAQPage block."""
    qas = parse_faq(html)
    if not qas:
        return html
    block = _ld_block(qas, url)
    m = FAQ_SEC_RE.search(html)
    if not m:
        return html
    he = html.find('</head>')
    # remove existing body-level FAQPage LD
    def drop(mm):
        if 'FAQPage' not in mm.group(0):
            return mm.group(0)
        if he > 0 and mm.start() < he:
            return mm.group(0)
        return ''
    html = LD_RE.sub(drop, html)
    m = FAQ_SEC_RE.search(html)
    end = m.end()
    return html[:end] + "\n            " + block + html[end:]

# ---------- recommended cards ----------
CARD_HREF = re.compile(r'(<a href=")([^"]*)(" class="recommended-card")')
CARD_HREF2 = re.compile(r'(<a[^>]*class="[^"]*recommended-card[^"]*"[^>]*href=")([^"]*)(")')

def _first_sentence(txt, limit=180):
    txt = re.sub(r'\s+', ' ', txt).strip()
    m = re.match(r'^(.*?[。．.!?！？])(?:\s|$)', txt)
    s = m.group(1) if m else txt
    if len(s) > limit:
        s = s[:limit].rstrip()
        cut = max(s.rfind('，'), s.rfind(','), s.rfind(' '))
        if cut > 60:
            s = s[:cut]
        s = s.rstrip('，, ') + '…'
    return s

def excerpt_for(slug_target, lang):
    p = path(slug_target, lang)
    if not os.path.exists(p):
        return None
    s = load(slug_target, lang)
    for pat in (r'<meta name="description" content="([^"]*)"',
                r'<meta content="([^"]*)" name="description"',
                r'"description":\s*"([^"]*)"'):
        m = re.search(pat, s)
        if m and m.group(1).strip() and 'undefined' not in m.group(1):
            return _first_sentence(strip_tags(m.group(1)))
    m = re.search(r'<p class="article-lead">(.*?)</p>', s, re.S)
    if m and strip_tags(m.group(1)).strip():
        return _first_sentence(strip_tags(m.group(1)))
    b = get_body(s) or ""
    m = re.search(r'<p>(.*?)</p>', b, re.S)
    if m and strip_tags(m.group(1)).strip():
        return _first_sentence(strip_tags(m.group(1)))
    return None

def _card_path(h, lang):
    pre = LANGS[lang].rstrip('/')
    h = re.sub(r'^(zh-cn/|zh-tw/)', '', h).lstrip('/')
    return '/' + (pre + '/' if pre else '') + h

def fix_cards(html, lang):
    def href_rep(m):
        h = m.group(2)
        if h.startswith('/') or h.startswith('http'):
            return m.group(0)
        if h.startswith('zh-cn/') or h.startswith('zh-tw/') or h.startswith('blog/'):
            return m.group(1) + _card_path(h, lang) + m.group(3)
        return m.group(0)
    html = CARD_HREF.sub(href_rep, html)
    # fallback pattern: class attribute before href
    def href_rep2(m):
        h = m.group(3)
        if h.startswith('/') or h.startswith('http'):
            return m.group(0)
        return m.group(1) + m.group(2) + _card_path(h, lang) + m.group(4)
    html = re.sub(r'(<a )([^>]*?href=")([^"]*)("[^>]*class="[^"]*recommended-card[^"]*")', href_rep2, html)
    # already-root-relative but missing the language prefix
    def href_rep3(m):
        h = m.group(2)
        pre = LANGS[lang].rstrip('/')
        if pre and h.startswith('/blog/'):
            return m.group(1) + '/' + pre + h + m.group(3)
        return m.group(0)
    html = CARD_HREF.sub(href_rep3, html)
    # class attribute before href (legacy template)
    def href_rep4(m):
        h = m.group(2)
        if h.startswith('/') or h.startswith('http'):
            return m.group(0)
        return m.group(1) + _card_path(h, lang) + m.group(3)
    html = CARD_HREF2.sub(href_rep4, html)

    # fill empty excerpts using target article meta description
    def block_rep(m):
        blk = m.group(0)
        em = re.search(r'(<p class="recommended-card-excerpt"[^>]*>)(.*?)(</p>)', blk, re.S)
        if not em:
            return blk
        if len(re.sub(r'\s|&nbsp;', '', strip_tags(em.group(2)))) > 0:
            return blk
        hm = re.search(r'href="([^"]*)"', blk)
        if not hm:
            return blk
        href = hm.group(1)
        tslug = href.rstrip('/').split('/')[-1].replace('.html', '')
        ex = excerpt_for(tslug, lang)
        if not ex:
            return blk
        return blk[:em.start(2)] + ex + blk[em.end(2):]
    html = re.sub(r'<a [^>]*class="[^"]*recommended-card[^"]*"[^>]*>.*?</a>', block_rep, html, flags=re.S)
    return html

# ---------- misc ----------
def kill_undefined(html, replacement=""):
    """Remove literal 'undefined' from the BODY only (head is off-limits)."""
    m = BODY_RE.search(html)
    if not m:
        return html
    inner = re.sub(r'\bundefined\b', replacement, m.group(2))
    inner = re.sub(r'\(\s*\)', '', inner)
    inner = re.sub(r'[ \t]{2,}', ' ', inner)
    return html[:m.start(2)] + inner + html[m.end(2):]

TAG_SPLIT = re.compile(r'(<[^>]*>)')

TW_FIXES = [
    ("擴充套件", "擴展"),     # OpenCC renders 扩展 as 擴充套件
    ("擴充套用", "擴充套用"),
    ("軟體開發套件", "軟體開發套件"),
    ("視頻", "影片"),
    ("内存", "記憶體"),
]

def s2twp_text(html):
    parts = TAG_SPLIT.split(html)
    out = []
    for p in parts:
        if p.startswith('<') and p.endswith('>'):
            out.append(p)
        else:
            t = S2TWP.convert(p)
            for a, b in TW_FIXES:
                t = t.replace(a, b)
            out.append(t)
    return "".join(out)

NAV_RE = re.compile(r'\s*<nav class="article-nav".*?</nav>\s*', re.S)

def process(slug, bodies=None, faq=None, h2map=None, tw_from_cn=False, faq_titles=None):
    """Apply the full standard to all three language files for one slug."""
    bodies = bodies or {}
    faq = faq or {}
    h2map = h2map or {}
    faq_titles = faq_titles or {}
    before = {}
    after = {}
    for lang in ("EN", "zh-CN", "zh-TW"):
        if not os.path.exists(path(slug, lang)):
            continue
        s = load(slug, lang)
        before[lang] = stats(s)
        if lang == "zh-TW" and tw_from_cn:
            cn = load(slug, "zh-CN")
            s = set_body(s, s2twp_text(get_body(cn) or ""))
        elif lang in bodies:
            nav = NAV_RE.search(get_body(s) or "")
            navhtml = nav.group(0) if nav else ""
            s = set_body(s, bodies[lang] + "\n\n            " + navhtml.strip() + "\n        ")
        # heading renames
        if lang in h2map:
            b = get_body(s)
            for old, new in h2map[lang].items():
                b = b.replace(old, new)
            s = set_body(s, b)
        # FAQ
        if lang in faq:
            title = faq_titles.get(lang) or {"EN": "Frequently Asked Questions",
                                              "zh-CN": "常见问题", "zh-TW": "常見問題"}[lang]
            s = set_faq(s, faq[lang], title)
        s = kill_undefined(s)
        s = ensure_faq_ld(s, "https://www.beehivestrategy.com/" + LANGS[lang] + "blog/articles/" + slug)
        s = fix_cards(s, lang)
        s = ensure_cta(s, lang)
        s = sync_toc(s)
        save(slug, lang, s)
        after[lang] = stats(s)
    return before, after

def cta_text_for(lang):
    return {"EN": "Book a Demo", "zh-CN": "预约演示", "zh-TW": "預約示範"}[lang]

def ensure_cta(html, lang):
    want = cta_text_for(lang)
    m = re.search(r'(<a[^>]*class="[^"]*article-cta-btn[^"]*"[^>]*>)(.*?)(</a>)', html, re.S)
    if not m:
        return html
    if want not in m.group(2):
        return html[:m.start(2)] + want + html[m.end(2):]
    return html

def tw_headings(html_zh_tw, html_zh_cn):
    """Force zh-TW headings to Traditional Chinese derived from zh-CN."""
    cb = get_body(html_zh_cn)
    tb = get_body(html_zh_tw)
    if cb is None or tb is None:
        return html_zh_tw
    cn_h = dict((i, t) for i, t in h2_list(cb))
    # build ordered list of cn headings to map positionally
    cn_ordered = h2_list(cb)
    def rep(m):
        idx = rep.i
        rep.i += 1
        txt = re.sub(r'\s+', ' ', strip_tags(m.group(2))).strip()
        if idx < len(cn_ordered):
            src = cn_ordered[idx][1]
            if CJK.search(src):
                new = S2TWP.convert(src)
            else:
                new = txt
        else:
            new = S2TWP.convert(txt)
        return '<h2%s>%s</h2>' % (m.group(1), new)
    rep.i = 0
    tb2 = re.sub(r'<h2([^>]*)>(.*?)</h2>', rep, tb, flags=re.S)
    return set_body(html_zh_tw, tb2)

def report_line(slug, lang, before, after_html):
    pass

def stats(html):
    b = get_body(html) or ""
    return words(b), cjk(b)
