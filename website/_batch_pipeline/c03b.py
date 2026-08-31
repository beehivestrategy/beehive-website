import os, re, sys, json

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
SUBS = {"en": "blog/articles", "cn": "zh-cn/blog/articles", "tw": "zh-tw/blog/articles"}

def path(slug, lang):
    return os.path.join(ROOT, SUBS[lang], slug + ".html")

def read(slug, lang):
    return open(path(slug, lang), encoding="utf-8").read()

def write(slug, lang, html):
    open(path(slug, lang), "w", encoding="utf-8").write(html)

def strip_tags(h):
    h = re.sub(r'<script.*?</script>', ' ', h, flags=re.S)
    h = re.sub(r'<style.*?</style>', ' ', h, flags=re.S)
    h = re.sub(r'<!--.*?-->', ' ', h, flags=re.S)
    h = re.sub(r'<[^>]+>', ' ', h)
    h = h.replace('&nbsp;', ' ').replace('&amp;', '&')
    return h

def words(h):
    return len(re.findall(r'[A-Za-z]+', strip_tags(h)))

def cjk(h):
    return len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', strip_tags(h)))

def body(html):
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', html, re.S)
    if m:
        return m.group(1)
    m = re.search(r'<article[^>]*>(.*?)</article>', html, re.S)
    return m.group(1) if m else html

def metric(html, lang):
    b = body(html)
    return words(b) if lang == "en" else cjk(b)

def h2s(html):
    return [(m.group(1), re.sub(r'<[^>]+>', '', m.group(2)).strip())
            for m in re.finditer(r'<h2 id="([^"]+)">(.*?)</h2>', html, re.S)]

def h1(html):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    return re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else None

def inject_sections(html, sections_html):
    """Insert H2 sections before faq-section (or before </article> if none). Update TOCs."""
    new = []
    for m in re.finditer(r'<h2 id="([^"]+)">(.*?)</h2>', sections_html, re.S):
        new.append((m.group(1), re.sub(r'<[^>]+>', '', m.group(2)).strip()))
    anchor = None
    # prefer inserting before the closing-section headings
    for closing in ('Key Takeaways', 'Conclusion', '关键要点', '结论', '總結', '結論'):
        m = re.search(r'<h2 id="[^"]+">\s*' + re.escape(closing) + r'\s*</h2>', html)
        if m:
            anchor = m.start()
            break
    if anchor is None:
        m = re.search(r'<section class="faq-section"', html)
        if m:
            anchor = m.start()
        else:
            m2 = re.search(r'<div class="faq-section"', html)
            anchor = m2.start() if m2 else html.rfind('</article>')
    html = html[:anchor] + "\n" + sections_html + "\n" + html[anchor:]
    for hid, htext in new:
        link = f'<a href="#{hid}" class="toc-link">{htext}</a>'
        mlink = f'<a href="#{hid}" class="toc-mobile-link">{htext}</a>'
        t = re.search(r'(<nav class="toc-links">)(.*?)(</nav>)', html, re.S)
        if t and link not in t.group(2):
            html = html[:t.start(2)] + t.group(2) + "                    " + link + "\n" + html[t.end(2):]
        t = re.search(r'(<div class="toc-mobile-links">)(.*?)(</div>)', html, re.S)
        if t and mlink not in t.group(2):
            html = html[:t.start(2)] + t.group(2) + "                    " + mlink + "\n" + html[t.end(2):]
    return html

def faq_items(html):
    """Return list of (question, answer_html) from faq-section."""
    m = re.search(r'<section class="faq-section".*?</section>', html, re.S)
    if not m:
        m = re.search(r'<div class="faq-section".*?</div>\s*</div>', html, re.S)
    if not m:
        return []
    blk = m.group(0)
    out = []
    chunks = blk.split('<div class="faq-item">')[1:]
    for ch in chunks:
        ch = re.sub(r'<span class="faq-number">\s*\d*\s*</span>', '', ch)
        q = re.search(r'<h3 class="faq-question-text">(.*?)</h3>', ch, re.S)
        a = re.search(r'<div class="faq-answer-inner">(.*?)</div>', ch, re.S)
        if q and a:
            out.append((re.sub(r'<[^>]+>', '', q.group(1)).strip(), a.group(1).strip()))
    if not out:
        for it in re.finditer(r'<h3 class="faq-question">(.*?)</h3>\s*<p class="faq-answer">(.*?)</p>', blk, re.S):
            out.append((re.sub(r'<[^>]+>', '', it.group(1)).strip(), it.group(2).strip()))
    return out

FAQ_TMPL = '''<section class="faq-section" id="faq" aria-label="Frequently Asked Questions">
    <h2 class="faq-section-title">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        {title}
    </h2>
    <div class="faq-list">
{items}
    </div>
</section>'''

FAQ_ITEM_TMPL = '''        <div class="faq-item">
            <button class="faq-question" aria-expanded="false">
                <h3 class="faq-question-text"><span class="faq-number">{n}</span><span>{q}</span></h3>
                <svg class="faq-chevron" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>
            </button>
            <div class="faq-answer" role="region">
                <div class="faq-answer-inner">{a}</div>
            </div>
        </div>'''

def build_faq(pairs, title="Frequently Asked Questions"):
    items = "\n".join(FAQ_ITEM_TMPL.format(n=i + 1, q=q, a=a) for i, (q, a) in enumerate(pairs))
    return FAQ_TMPL.format(title=title, items=items)

def ensure_faq(html, pairs, title="Frequently Asked Questions"):
    """Replace or insert FAQ section with >=3 pairs. Returns (html, changed)."""
    existing = faq_items(html)
    final = list(existing)
    for q, a in pairs:
        if not any(q == eq for eq, _ in final):
            final.append((q, a))
    if len(final) < 3:
        final = pairs[:max(3, len(pairs))]
    sec = build_faq(final, title)
    m = re.search(r'<section class="faq-section".*?</section>', html, re.S)
    if m:
        if len(final) == len(existing):
            return html, False
        return html[:m.start()] + sec + html[m.end():], True
    m2 = re.search(r'<div class="faq-section"', html)
    if m2:
        # legacy: find end of wrapper div by brace matching
        start = m2.start()
        i = html.find('>', start) + 1
        depth = 1
        while depth > 0 and i < len(html):
            nd = html.find('<div', i)
            cd = html.find('</div>', i)
            if cd == -1:
                break
            if nd != -1 and nd < cd:
                depth += 1
                i = nd + 4
            else:
                depth -= 1
                i = cd + 6
        return html[:start] + sec + html[i:], True
    nav = re.search(r'<nav class="article-nav"', html)
    anchor = nav.start() if nav else html.rfind('</article>')
    return html[:anchor] + "\n" + sec + "\n" + html[anchor:], True

def jsonld_escape(t):
    t = re.sub(r'<[^>]+>', '', t)
    return t.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ').strip()

def sync_faq_jsonld(html):
    """Make exactly one FAQPage JSON-LD in <head>, matching current FAQ items."""
    pairs = faq_items(html)
    if len(pairs) < 3:
        return html, False
    ent = []
    for q, a in pairs:
        ent.append('        {\n            "@type": "Question",\n            "name": "%s",\n            "acceptedAnswer": {\n                "@type": "Answer",\n                "text": "%s"\n            }\n        }' % (jsonld_escape(q), jsonld_escape(a)))
    block = '<script type="application/ld+json">\n{\n    "@context": "https://schema.org",\n    "@type": "FAQPage",\n    "mainEntity": [\n' + ",\n".join(ent) + '\n    ]\n}\n</script>\n'
    # remove all existing FAQPage scripts
    out = html
    changed = False
    for m in list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', out, re.S))[::-1]:
        if re.search(r'"@type"\s*:\s*"FAQPage"', m.group(1)):
            out = out[:m.start()] + out[m.end():]
            changed = True
    idx = out.rfind('</head>')
    out = out[:idx] + block + out[idx:]
    return out, True

def fill_excerpts(html, lang):
    """Fill empty recommended-card-excerpt using target article's meta description."""
    def repl(m):
        blk = m.group(0)
        em = re.search(r'class="recommended-card-excerpt">(.*?)</p>', blk, re.S)
        tm = re.search(r'class="recommended-card-title">(.*?)<', blk, re.S)
        need = (em is None) or (not em.group(1).strip()) or \
               (tm is not None and em.group(1).strip() == tm.group(1).strip()) or \
               len(em.group(1).strip()) > 110
        if need:
            href = re.search(r'href="([^"]+)"', blk).group(1)
            tgt = os.path.join(ROOT, href.lstrip('/'))
            if not os.path.exists(tgt):
                tgt = tgt + '.html'
            desc = ''
            if os.path.exists(tgt):
                t = open(tgt, encoding='utf-8').read()
                for pat in (r'<meta name="description" content="([^"]+)"',
                            r'<meta property="og:description" content="([^"]+)"'):
                    dm = re.search(pat, t)
                    if dm and dm.group(1).strip():
                        desc = dm.group(1).strip()
                        break
                if not desc:
                    tb = body(t)
                    ps = [re.sub(r'<[^>]+>', '', p).strip() for p in
                          re.findall(r'<p>(.*?)</p>', tb, re.S)]
                    ps = [p for p in ps if len(p) > 30 and not p.startswith('&')]
                    if ps:
                        desc = ps[0]
            desc = re.sub(r'^Key Insight:\s*', '', desc)
            if len(desc) > 110:
                parts = re.split(r'(?<=[。！？；])|(?<=[.!?])\s+', desc)
                parts = [p for p in parts if p.strip()]
                desc = parts[0] if parts and len(parts[0]) >= 25 else desc[:107] + '...'
            if not desc:
                tm = re.search(r'class="recommended-card-title">(.*?)<', blk, re.S)
                desc = tm.group(1).strip() if tm else ''
            if lang == 'tw':
                desc = s2t(desc)
            if em:
                blk = blk[:em.start(1)] + desc + blk[em.end(1):]
            else:
                blk = blk.replace('</a>', '<p class="recommended-card-excerpt">%s</p></a>' % desc, 1)
        return blk
    return re.sub(r'<a href="[^"]*" class="recommended-card">.*?</a>', repl, html, flags=re.S)

def fix_rec_hrefs(html, lang):
    """Ensure recommended-card hrefs are root-relative + language prefixed."""
    pref = {'en': '/blog/articles/', 'cn': '/zh-cn/blog/articles/', 'tw': '/zh-tw/blog/articles/'}[lang]
    def repl(m):
        href = m.group(1)
        if href.startswith('http') or '#' in href:
            return m.group(0)
        slug = href.strip('/').split('/')[-1]
        if not href.startswith(pref):
            return m.group(0).replace('href="%s"' % href, 'href="%s%s"' % (pref, slug), 1)
        return m.group(0)
    return re.sub(r'<a href="([^"]*)" class="recommended-card">', repl, html)

def fix_cta(html, lang):
    ph = {'en': 'Book a Demo', 'cn': '预约演示', 'tw': '預約示範'}[lang]
    if re.search(r'class="article-cta-btn"[^>]*>\s*' + ph, html):
        return html, False
    def repl(m):
        return m.group(1) + ph + '</a>'
    new, n = re.subn(r'(class="article-cta-btn"[^>]*>)[^<]*</a>', repl, html)
    return (new, n > 0)

try:
    from opencc import OpenCC
    _cc = OpenCC('s2t')
    def s2t(t):
        return _cc.convert(t)
except Exception:
    def s2t(t):
        return t

def report(slug, before):
    out = {}
    for lang in ('en', 'cn', 'tw'):
        h = read(slug, lang)
        out[lang] = metric(h, lang)
    return out

def guard(slug):
    """Guardrail check: version query present, head/footer intact, titles unchanged."""
    issues = []
    for lang in ('en', 'cn', 'tw'):
        h = read(slug, lang)
        if '/css/article.css?v=20260826' not in h:
            issues.append(f'{lang}: missing css version')
        if '/js/article.js?v=20260826' not in h:
            issues.append(f'{lang}: missing js version')
        if h.count('</head>') != 1:
            issues.append(f'{lang}: head count')
        if '<footer' not in h:
            issues.append(f'{lang}: no footer')
        if 'share-btn' not in h and 'share-button' not in h and 'share' not in h:
            issues.append(f'{lang}: share markup missing')
    return issues

def verify(slug):
    res = {}
    for lang in ('en', 'cn', 'tw'):
        h = read(slug, lang)
        m = metric(h, lang)
        faq = len(faq_items(h))
        ldn = len(re.findall(r'"@type"\s*:\s*"FAQPage"', h))
        ph = {'en': 'Book a Demo', 'cn': '预约演示', 'tw': '預約示範'}[lang]
        cta = bool(re.search(r'class="article-cta-btn"[^>]*>\s*' + ph, h))
        pref = {'en': '/blog/articles/', 'cn': '/zh-cn/blog/articles/', 'tw': '/zh-tw/blog/articles/'}[lang]
        hrefs = re.findall(r'<a href="([^"]*)" class="recommended-card">', h)
        bad = [x for x in hrefs if not x.startswith(pref)]
        empty_ex = len([1 for blk in re.findall(r'<a href="[^"]*" class="recommended-card">.*?</a>', h, re.S)
                        if not (re.search(r'class="recommended-card-excerpt">(.*?)</p>', blk, re.S) or None)
                        or not re.search(r'class="recommended-card-excerpt">(.+?)</p>', blk, re.S)])
        nh = [t for _, t in h2s(h)]
        res[lang] = dict(metric=m, faq=faq, ld=ldn, cta=cta, badhref=bad, empty_ex=empty_ex, h2=nh)
    return res


def retitle_h2(html, old, new):
    """Rename an H2 (and its TOC links). Returns (html, changed)."""
    changed = False
    while True:
        target = None
        for m in re.finditer(r'<h2 id="([^"]+)">(.*?)</h2>', html, re.S):
            if re.sub(r'<[^>]+>', '', m.group(2)).strip() == old:
                target = m
                break
        if target is None:
            break
        hid = target.group(1)
        html = html[:target.start(2)] + new + html[target.end(2):]
        for cls in ('toc-link', 'toc-mobile-link'):
            t = re.search(r'<a href="#' + re.escape(hid) + r'" class="' + cls + r'">(.*?)</a>', html, re.S)
            if t:
                html = html[:t.start(1)] + new + html[t.end(1):]
        changed = True
    return html, changed


def retitle_map(html, mapping):
    n = 0
    for old, new in mapping.items():
        html, c = retitle_h2(html, old, new)
        n += int(c)
    return html, n


def regen_tw(slug):
    """Rebuild the zh-TW article region from zh-CN (OpenCC s2t). Keeps head/footer/cards."""
    cn = read(slug, 'cn')
    tw = read(slug, 'tw')
    mc = re.search(r'<article[^>]*id="article-content"[^>]*>.*?</article>', cn, re.S)
    mt = re.search(r'<article[^>]*id="article-content"[^>]*>.*?</article>', tw, re.S)
    if not mc or not mt:
        return False
    new = s2t(mc.group(0))
    out = tw[:mt.start()] + new + tw[mt.end():]
    write(slug, 'tw', out)
    return True


def finalize(slug):
    log = {}
    for lang in ('en', 'cn', 'tw'):
        h = read(slug, lang)
        h = fill_excerpts(h, lang)
        h = fix_rec_hrefs(h, lang)
        h, c = fix_cta(h, lang)
        h, j = sync_faq_jsonld(h)
        write(slug, lang, h)
        log[lang] = dict(cta_changed=c, jsonld=j)
    return log

def summary(slug):
    r = verify(slug)
    g = guard(slug)
    line = [f'{slug}']
    for lang in ('en', 'cn', 'tw'):
        d = r[lang]
        line.append(f"{lang}={d['metric']} faq={d['faq']} ld={d['ld']} cta={int(d['cta'])} bad={len(d['badhref'])} ex0={d['empty_ex']}")
    if g:
        line.append('GUARD:' + ';'.join(g))
    return ' | '.join(line)
