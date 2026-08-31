#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gbatch_003 helpers: H2 renames, section inserts, FAQ rebuild, JSON-LD sync, TOC sync, link fix."""
import os, re, json, html as H

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
PFX = {'en': '', 'zh-cn': 'zh-cn/', 'zh-tw': 'zh-tw/'}
ART_OPEN = '<article class="article-content"'
H2_RE = re.compile(r'(<h2 id="([^"]*)"[^>]*>)(.*?)(</h2>)', re.S)
TAG = re.compile(r'<[^>]+>')
BODYFAQ_RE = re.compile(
    r'<h2 id="([^"]*)">(?:常见问题解答|常見問題解答|常见问题|常見問題|Frequently asked questions|Frequently Asked Questions)</h2>\s*((?:<p(?:\s[^>]*)?>.*?</p>\s*)+)',
    re.S)
LD_RE = re.compile(r'(<script type="application/ld\+json"[^>]*>)(.*?)(</script>)', re.S)


def path_for(slug, lang):
    return os.path.join(ROOT, PFX[lang], 'blog/articles', slug + '.html')


def clean(x):
    return re.sub(r'\s+', ' ', H.unescape(TAG.sub('', x))).strip()


def slugify_en(t):
    s = re.sub(r'[^a-z0-9]+', '-', t.lower())
    return s.strip('-')


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


# ---------------------------------------------------------------- FAQ markup
FAQ_ITEM = '''                    <div class="faq-item">
                        <div class="faq-question" aria-expanded="false">
                            <span class="faq-number">{n}</span>
                            <h3 class="faq-question-text" style="margin:0;font-size:inherit;font-weight:600;line-height:1.5">{q}</h3>
                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                        </div>
                        <div class="faq-answer" role="region"><div class="faq-answer-inner">{a}</div></div>
                    </div>'''


def build_faq_html(qa):
    items = []
    for i, (q, a) in enumerate(qa, 1):
        items.append(FAQ_ITEM.format(n=i, q=esc(q), a=esc(a)))
    return '<div class="faq-list">\n' + '\n'.join(items) + '\n                </div>'


def build_faq_json(qa):
    ent = [{"@type": "Question", "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]
    obj = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ent}
    s = json.dumps(obj, ensure_ascii=False, indent=2)
    return s.replace('</', '<\\/')


# ---------------------------------------------------------------- main op
def h2_texts(slug, lang, doc=None):
    if doc is None:
        doc = open(path_for(slug, lang), encoding='utf-8').read()
    ai = doc.find(ART_OPEN); ae = doc.find('</article>', ai)
    return [clean(m.group(3)) for m in H2_RE.finditer(doc[ai:ae])]


def tw_renames(slug, cn_renames, convert):
    """Map zh-CN H2 renames onto the zh-TW file by heading position (files drift in conversion)."""
    cn_bk = os.path.join(ROOT, '_batch_pipeline/_backup_gb003/zh-cn/blog/articles', slug + '.html')
    cn_src = cn_bk if os.path.exists(cn_bk) else path_for(slug, 'zh-cn')
    cn = h2_texts(slug, 'zh-cn', open(cn_src, encoding='utf-8').read())
    tw = h2_texts(slug, 'zh-tw')
    if len(cn) == len(tw):
        out = {}
        for c, t in zip(cn, tw):
            if c in cn_renames:
                out[t] = convert(cn_renames[c])
        return out
    return {convert(k): convert(v) for k, v in cn_renames.items()}


def replace_body(art, body_html):
    """Replace everything between the mobile-TOC block and the FAQ section with body_html."""
    start = art.find('</div>', art.find('class="toc-mobile-links"'))
    assert start > 0, 'toc-mobile-links not found'
    start = art.find('>', start) + 1
    end = art.find('<section class="faq-section"')
    if end < 0:
        end = len(art)
    return art[:start] + '\n' + body_html + '\n' + art[end:]


def process(slug, lang, h2_renames=None, inserts=None, faq=None, excerpts=None,
            drop_body_faq=False, cta_fix=None, insert_after=None, new_body=None):
    """h2_renames: {old_text: new_text}  inserts: [(h2_text, h2_id, body_html)]
       faq: [(q,a)]  excerpts: {target_slug: sentence}"""
    p = path_for(slug, lang)
    doc = open(p, encoding='utf-8').read()
    orig = doc
    ai = doc.find(ART_OPEN)
    ae = doc.find('</article>', ai)
    assert ai > 0 and ae > ai, slug
    art = doc[ai:ae]

    # 0. full body replacement (garbled zh bodies)
    if new_body is not None:
        art = replace_body(art, new_body)

    # 1. H2 renames (keep ids)
    if h2_renames:
        def repl(m):
            op, hid, inner, cl = m.groups()
            txt = clean(inner)
            if txt in h2_renames:
                lead = re.match(r'\s*', inner).group(0)
                trail = re.search(r'\s*$', inner).group(0)
                inner = lead + esc(h2_renames[txt]) + trail
            return op + inner + cl
        art = H2_RE.sub(repl, art)

    # 2. drop duplicated body FAQ block
    if drop_body_faq:
        art = BODYFAQ_RE.sub('', art)

    # 3. insert new sections
    inserts = inserts or []
    if inserts:
        if insert_after:
            anchor = None
            for m in H2_RE.finditer(art):
                if clean(m.group(3)) == insert_after:
                    anchor = m
                    break
            assert anchor, 'anchor not found: %s %s' % (slug, insert_after)
            # insert after this section: before the next <h2 or before faq-section
            nxt = H2_RE.search(art, anchor.end())
            fq = art.find('<section class="faq-section"', anchor.end())
            pos = nxt.start() if (nxt and (fq < 0 or nxt.start() < fq)) else (fq if fq > 0 else len(art))
        else:
            fq = art.find('<section class="faq-section"')
            assert fq > 0, 'no faq section ' + slug
            pos = fq
        chunks, toc = [], []
        for h2_text, h2_id, body in inserts:
            hid = h2_id or (slugify_en(h2_text) if lang == 'en' else h2_text)
            chunks.append('<h2 id="%s">%s</h2>\n%s\n' % (hid, esc(h2_text), body))
            toc.append('<a href="#%s" class="toc-mobile-link">%s</a>' % (hid, esc(h2_text)))
        art = art[:pos] + '\n'.join(chunks) + art[pos:]

    # 4. rebuild FAQ list
    if faq:
        m = re.search(r'<section class="faq-section".*?<div class="faq-list">.*?</div>\s*</section>', art, re.S)
        if not m:
            m = re.search(r'<section class="faq-section".*?</section>', art, re.S)
            assert m, 'no faq section ' + slug
        newsec = re.sub(r'<div class="faq-list">.*?</div>\s*</section>',
                        lambda _m: build_faq_html(faq) + '\n            </section>', m.group(0), flags=re.S)
        art = art[:m.start()] + newsec + art[m.end():]

    # 5. sync TOCs from article H2s (mobile + sidebar)
    pairs = [(m.group(2), clean(m.group(3))) for m in H2_RE.finditer(art)]
    pairs = [x for x in pairs if x[0]]
    if pairs:
        mobile = '\n                    ' + '\n                    '.join(
            '<a href="#%s" class="toc-mobile-link">%s</a>' % (i, esc(t)) for i, t in pairs) + '\n                '
        new_art = re.sub(r'(<div class="toc-mobile-links">).*?(</div>)',
                         lambda m: m.group(1) + mobile + m.group(2), art, flags=re.S)
        art = new_art
    doc = doc[:ai] + art + doc[ae:]

    # sidebar TOC (outside article)
    if pairs:
        side = '\n                    ' + '\n                    '.join(
            '<a href="#%s" class="toc-link">%s</a>' % (i, esc(t)) for i, t in pairs) + '\n                '
        doc = re.sub(r'(<nav class="toc-links">).*?(</nav>)',
                     lambda m: m.group(1) + side + m.group(2), doc, flags=re.S)

    # 6. links: recommended-card / sidebar-related-card -> root-relative + lang prefix
    pfx = PFX[lang]
    doc = re.sub(r'<a href="([^"]*)" class="(recommended-card|sidebar-related-card)">',
                 lambda m: '<a href="/%s%s" class="%s">' % (pfx, re.sub(r'^(zh-cn|zh-tw)/', '', m.group(1)), m.group(2))
                 if not (m.group(1).startswith('/') or m.group(1).startswith('http') or m.group(1).startswith('#')) else m.group(0),
                 doc)

    # 7. excerpts
    excerpts = excerpts or {}
    doc = re.sub(r'<a href="([^"]*?/blog/articles/[^"]*)" class="(recommended-card)">(.*?)</a>',
                 lambda m: '<a href="%s" class="%s">%s</a>' % (m.group(1), m.group(2), fill_inner(m.group(3), m.group(1), excerpts, lang)),
                 doc, flags=re.S)

    # 8. CTA phrase fix
    if cta_fix:
        old, new = cta_fix
        doc = re.sub(r'(<a href="[^"]*" class="article-cta-btn">)[^<]*(</a>)',
                     lambda m: m.group(1) + new + m.group(2), doc)

    # 9. JSON-LD FAQPage (update in place, never duplicate)
    if faq:
        newjson = build_faq_json(faq)
        blocks = list(LD_RE.finditer(doc))
        faqblocks = [b for b in blocks if '"FAQPage"' in b.group(2)]
        if faqblocks:
            b = faqblocks[0]
            doc = doc[:b.start(2)] + '\n' + newjson + '\n' + doc[b.end(2):]
        else:
            m = re.search(r'</section>\s*(?=<nav class="article-nav")', doc)
            assert m, 'no insert point ' + slug
            doc = doc[:m.end()] + '\n            <script type="application/ld+json">\n' + newjson + '\n</script>' + doc[m.end():]

    changed = doc != orig
    if changed:
        open(p, 'w', encoding='utf-8').write(doc)
    return changed


META_RE = re.compile(r'<meta name="description" content="([^"]*)"')


def _clip(s, n=150):
    s = re.sub(r'\s+', ' ', s).strip()
    if len(s) <= n:
        return s
    cut = s[:n]
    if ' ' in cut:
        cut = cut[:cut.rfind(' ')]
    return cut.rstrip(' ,;:、，；：') + '…'


def meta_desc(tgt_slug, lang):
    """1-sentence summary from the target article: meta description, else its opening paragraph."""
    for lg in (lang, 'en'):
        p = os.path.join(ROOT, PFX[lg], 'blog/articles', tgt_slug + '.html')
        if not os.path.exists(p):
            continue
        doc = open(p, encoding='utf-8').read()
        d = ''
        m = META_RE.search(doc)
        if m:
            d = clean(m.group(1))
        if not d:
            ai = doc.find(ART_OPEN)
            if ai < 0:
                continue
            body = doc[ai:doc.find('</article>', ai)]
            body = re.sub(r'<div class="toc-mobile".*?</div>\s*</div>', '', body, flags=re.S)
            pm = re.search(r'<p(?: class="article-lead")?>(.*?)</p>', body, re.S)
            if pm:
                d = clean(pm.group(1))
        if not d:
            continue
        # first sentence
        m2 = re.split(r'(?<=[。．.!?！？])\s+', d)
        if m2 and 12 <= len(m2[0]) <= 220:
            d = m2[0]
        return _clip(d)
    return None


def fill_inner(inner, href, excerpts, lang):
    """Fill empty recommended-card-excerpt; manual excerpts override, else use target meta description."""
    tgt = href.split('/blog/articles/')[-1]
    manual = tgt in excerpts
    exc = excerpts.get(tgt)
    m = re.search(r'(<p class="recommended-card-excerpt">)(.*?)(</p>)', inner, re.S)
    if m is not None:
        if not manual and clean(m.group(2)):
            return inner
        if exc is None:
            exc = meta_desc(tgt, lang)
        if not exc:
            return inner
        return inner[:m.start(2)] + esc(exc) + inner[m.end(2):]
    if exc is None:
        exc = meta_desc(tgt, lang)
    if not exc:
        return inner
    if '<div class="recommended-card-meta">' in inner:
        return inner.replace('<div class="recommended-card-meta">',
                             '<p class="recommended-card-excerpt">%s</p>\n                    <div class="recommended-card-meta">' % esc(exc), 1)
    return inner


def stats(slug, lang):
    p = path_for(slug, lang)
    h = open(p, encoding='utf-8').read()
    ai = h.find(ART_OPEN); ae = h.find('</article>', ai)
    art = h[ai:ae]
    txt = re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>', ' ', art, flags=re.S))
    n = len(re.findall(r'[\u4e00-\u9fff]', txt))
    w = len(re.findall(r"[A-Za-z][A-Za-z'\-]*", txt))
    faq = len(re.findall(r'<h3 class="faq-question-text"', art))
    ld = len(re.findall(r'"FAQPage"', h))
    return {'words': w, 'cjk': n, 'faq': faq, 'ld': ld}
