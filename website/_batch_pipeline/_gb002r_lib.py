#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mechanical editor helpers for gbatch_002 remediation.

All helpers operate on the FULL file HTML string and return a new full HTML
string. Nothing here touches <head>, <footer> or share-button markup.
"""
import html as _html
import json
import re

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
LANGS = [("EN", "blog/articles/%s.html"),
         ("zh-CN", "zh-cn/blog/articles/%s.html"),
         ("zh-TW", "zh-tw/blog/articles/%s.html")]

CJK = re.compile(r'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]')


# ---------------------------------------------------------------- io / guards
def read(rel):
    with open(ROOT + "/" + rel, encoding="utf-8") as f:
        return f.read()


def write(rel, s):
    with open(ROOT + "/" + rel, "w", encoding="utf-8") as f:
        f.write(s)


def guard(rel, before, after):
    """Hard invariants that must survive every edit."""
    errs = []
    if '/css/article.css?v=20260826' not in after:
        errs.append("css version link lost")
    if '/js/article.js?v=20260826' not in after:
        errs.append("js version link lost")
    if '<footer' not in after or '</footer>' not in after:
        errs.append("footer lost")
    for need in ('share-linkedin', 'share-x', 'share-copy'):
        if need not in after:
            errs.append("share button %s lost" % need)
    # head must be byte-identical
    hb = before.split('<body', 1)[0]
    ha = after.split('<body', 1)[0]
    if hb != ha:
        errs.append("HEAD CHANGED")
    if errs:
        raise SystemExit("GUARD FAIL %s: %s" % (rel, "; ".join(errs)))
    return True


def edit(rel, fn, *a, **kw):
    before = read(rel)
    after = fn(before, *a, **kw)
    if after == before:
        return False
    guard(rel, before, after)
    write(rel, after)
    return True


# ------------------------------------------------------------- article region
ART_RE = re.compile(r'(<article class="article-content"[^>]*>)(.*?)(</article>)', re.S)


def art_span(h):
    m = ART_RE.search(h)
    if not m:
        raise SystemExit("no article block")
    return m.start(2), m.end(2)


def art(h):
    return ART_RE.search(h).group(2)


def set_art(h, new):
    m = ART_RE.search(h)
    return h[:m.start(2)] + new + h[m.end(2):]


def map_art(h, fn):
    return set_art(h, fn(art(h)))


# ------------------------------------------------------------------- counting
def en_words(h):
    body = art(h)
    t = re.sub(r'<[^>]+>', ' ', body)
    t = re.sub(r'&[a-z]+;', ' ', t)
    return len(t.split())


def cjk(h):
    return len(CJK.findall(re.sub(r'<[^>]+>', ' ', art(h))))


# ------------------------------------------------------------------ insertion
def insert_before(inner, pat, block, required=True):
    m = re.search(pat, inner, re.S)
    if not m:
        if required:
            raise SystemExit("anchor not found: %r" % pat)
        return inner + "\n" + block
    return inner[:m.start()] + block + "\n\n" + inner[m.start():]


def append_before_nav(inner, block):
    """Insert block just before the trailing <nav class="article-nav">."""
    m = re.search(r'<nav class="article-nav"', inner)
    if not m:
        return inner + "\n" + block
    return inner[:m.start()] + block + "\n\n            " + inner[m.start():]


# ------------------------------------------------------------------------- H2
def slug_h2(t):
    t = _html.unescape(t).strip().lower()
    t = t.replace('—', ' ').replace('–', ' ')
    t = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", ' ', t)
    return re.sub(r'\s+', '-', t).strip('-')


def _find_h2(h, old, used=()):
    for mm in re.finditer(r'<h2 id="([^"]*)">\s*(.*?)\s*</h2>', h, re.S):
        if mm.start() in used:
            continue
        if re.sub(r'<[^>]+>', '', mm.group(2)).strip() == old:
            return mm
    return None


def retitle_h2(h, pairs):
    """pairs: list of (old_text, new_text). Updates h2 id/text + TOC anchors."""
    used = set()
    for old, new in pairs:
        m = _find_h2(h, old, used)
        if not m:
            raise SystemExit("h2 not found: %r" % old)
        used.add(m.start())
        oid = m.group(1)
        nid = slug_h2(new)
        h = (h[:m.start()] + '<h2 id="%s">%s</h2>' % (nid, new)
             + h[m.end():])
        h = re.sub(r'href="#%s"' % re.escape(oid), 'href="#%s"' % nid, h)
        h = re.sub(r'(class="toc-(?:mobile-)?link">)\s*%s\s*(</a>)' % re.escape(old),
                   lambda mm: mm.group(1) + new + mm.group(2), h, count=1)
    return h


# ------------------------------------------------------------------------ FAQ
FAQ_OPEN = re.compile(r'<section class="faq-section"[^>]*>')


def faq_bounds(inner):
    m = FAQ_OPEN.search(inner)
    if not m:
        return None
    end = inner.find('</section>', m.end())
    return m.start(), end


def faq_items(inner):
    """Return [(question, answer)] parsed from on-page FAQ markup."""
    b = faq_bounds(inner)
    if not b:
        return []
    seg = inner[b[0]:b[1]]
    out = []
    for m in re.finditer(
            r'<div class="faq-item">(.*?)<div class="faq-answer"[^>]*>(.*?)</div>\s*</div>\s*</div>',
            seg, re.S):
        item, ans = m.group(1), m.group(2)
        qm = re.search(r'<span class="faq-question-text">.*?<span>(.*?)</span>\s*</span>', item, re.S)
        q = re.sub(r'<[^>]+>', '', qm.group(1)).strip() if qm else ''
        q = re.sub(r'^\d+\s*', '', q).strip()
        am = re.search(r'<div class="faq-answer-inner">(.*?)</div>', ans, re.S)
        a = am.group(1) if am else ans
        a = re.sub(r'<[^>]+>', '', a).strip()
        out.append((_html.unescape(q), _html.unescape(a)))
    if not out:
        for m in re.finditer(r'<div class="faq-item">(.*?)</div>\s*</div>\s*</div>', seg, re.S):
            pass
    return out


def replace_faq(inner, qa, title):
    """Rebuild the on-page FAQ list from qa (list of (q,a)); keeps wrapper."""
    b = faq_bounds(inner)
    if not b:
        raise SystemExit("no faq-section")
    seg = inner[b[0]:b[1]]
    head = seg[:seg.find('<div class="faq-list">')]
    items = []
    for i, (q, a) in enumerate(qa, 1):
        items.append(
            '                    <div class="faq-item">\n'
            '                        <h3 class="faq-question-heading" style="margin:0">\n'
            '                        <button class="faq-question" aria-expanded="false">\n'
            '                            <span class="faq-question-text"><span class="faq-number">%d</span><span>%s</span></span>\n'
            '                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>\n'
            '                        </button>\n'
            '                        </h3>\n'
            '                        <div class="faq-answer" role="region"><div class="faq-answer-inner">%s</div></div>\n'
            '                    </div>' % (i, _html.escape(q), _html.escape(a)))
    new = head + '<div class="faq-list">\n' + '\n'.join(items) + '\n                </div>\n            '
    return inner[:b[0]] + new + inner[b[1]:]


def build_faq_section(qa, title, aria):
    items = []
    for i, (q, a) in enumerate(qa, 1):
        items.append(
            '                    <div class="faq-item">\n'
            '                        <h3 class="faq-question-heading" style="margin:0">\n'
            '                        <button class="faq-question" aria-expanded="false">\n'
            '                            <span class="faq-question-text"><span class="faq-number">%d</span><span>%s</span></span>\n'
            '                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>\n'
            '                        </button>\n'
            '                        </h3>\n'
            '                        <div class="faq-answer" role="region"><div class="faq-answer-inner">%s</div></div>\n'
            '                    </div>' % (i, _html.escape(q), _html.escape(a)))
    return (
        '            <section class="faq-section" id="faq" aria-label="%s">\n'
        '                <h2 class="faq-section-title">\n'
        '                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>\n'
        '                    %s\n'
        '                </h2>\n'
        '                <div class="faq-list">\n'
        '%s\n'
        '                </div>\n'
        '            </section>\n' % (aria, title, '\n'.join(items)))


def wrap_faq_h3(inner):
    """Wrap each <button class="faq-question">…</button> in an <h3>."""
    if 'faq-question-heading' in inner:
        return inner

    def rep(m):
        return ('<h3 class="faq-question-heading" style="margin:0">\n'
                '                        ' + m.group(0) + '\n'
                '                        </h3>')
    new, n = re.subn(r'<button class="faq-question"[^>]*>.*?</button>',
                     rep, inner, flags=re.S)
    return new


def faq_ld_block(qa):
    obj = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q,
                           "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}
    return ('\n            <script type="application/ld+json">\n'
            + json.dumps(obj, ensure_ascii=False, indent=2)
            + '\n            </script>\n')


def ensure_faq_ld(h):
    """(Re)build the body-level FAQPage JSON-LD right after the FAQ section."""
    inner = art(h)
    b = faq_bounds(inner)
    if not b:
        raise SystemExit("no faq-section for JSON-LD")
    qa = faq_items(inner)
    if len(qa) < 3:
        raise SystemExit("FAQ has %d items" % len(qa))
    close = b[1] + len('</section>')
    rest = inner[close:]
    m = re.match(r'\s*<script type="application/ld\+json">(.*?)</script>', rest, re.S)
    block = faq_ld_block(qa)
    if m:
        new_inner = inner[:close] + block + rest[m.end():]
    else:
        new_inner = inner[:close] + block + rest
    return set_art(h, new_inner)


# ------------------------------------------------------------ recommended etc
def fix_rec_hrefs(h, lang):
    pref = {"EN": "/blog/articles/", "zh-CN": "/zh-cn/blog/articles/",
            "zh-TW": "/zh-tw/blog/articles/"}[lang]

    def rep(m):
        href = m.group(1)
        rest = href.split('/blog/articles/', 1)[-1]
        return '<a href="%s%s" class="recommended-card">' % (pref, rest)
    return re.sub(r'<a href="([^"]*blog/articles/[^"]+)" class="recommended-card">', rep, h)


def fill_excerpts(h, mapping):
    """mapping: {href_suffix: excerpt}. Fills only empty <p class=…excerpt>."""
    def rep(m):
        open_tag, href, mid, title, p = m.group(1), m.group(1), m.group(2), m.group(3), m.group(4)
        if p.strip():
            return m.group(0)
        key = href.split('/blog/articles/', 1)[-1]
        ex = mapping.get(key)
        if not ex:
            return m.group(0)
        return ('<a href="%s" class="recommended-card">%s'
                '<h3 class="recommended-card-title">%s</h3>\n'
                '                    <p class="recommended-card-excerpt">%s</p>'
                % (href, mid, title, ex))
    return re.sub(r'<a href="([^"]*blog/articles/[^"]+)" class="recommended-card">(.*?)'
                  r'<h3 class="recommended-card-title">(.*?)</h3>\s*'
                  r'<p class="recommended-card-excerpt">(.*?)</p>',
                  rep, h, flags=re.S)


# ------------------------------------------------------------------ opencc s2twp
_OCC = None


def occ():
    global _OCC
    if _OCC is None:
        import opencc
        _OCC = opencc.OpenCC('s2twp')
    return _OCC


def opencc_inner(inner):
    """s2twp on text nodes only (never inside tags or <script>)."""
    out = []
    pos = 0
    for m in re.finditer(r'(<script\b.*?</script>)|(<[^>]+>)', inner, re.S | re.I):
        out.append(occ().convert(inner[pos:m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(occ().convert(inner[pos:]))
    return ''.join(out)


# ---------------------------------------------------------------- content pass
def drop_stray_faq_h2(h):
    """Remove a duplicate <h2 …>Frequently Asked Questions</h2> sitting right
    before the real <section class="faq-section">, plus its TOC entries."""
    m = re.search(r'\n?<h2 id="[^"]*"[^>]*>\s*(?:Frequently Asked Questions|常见问题|常見問題|常見問題解答)\s*</h2>\s*(?=<section class="faq-section")', h)
    if not m:
        return h
    seg = m.group(0)
    oid = re.search(r'id="([^"]+)"', seg).group(1)
    h = h[:m.start()] + '\n            ' + h[m.end():]
    h = re.sub(r'\s*<a href="#%s" class="toc-(?:mobile-)?link">[^<]*</a>' % re.escape(oid), '', h)
    return h


def add_toc(h, entries):
    """entries: [(id, text)] inserted before the FAQ/end of both TOCs."""
    anchor = None
    for pat in (r'<a href="#faq" class="toc-link">', r'<a href="#frequently-asked-questions" class="toc-link">'):
        m = re.search(pat, h)
        if m:
            anchor = m
            break
    for kind in ("toc-link", "toc-mobile-link"):
        blocks = ''.join('\n                    <a href="#%s" class="%s">%s</a>' % (i, kind, t)
                         for i, t in entries)
        if anchor and kind == "toc-link":
            m = re.search(r'<a href="#(?:faq|frequently-asked-questions)" class="toc-link">', h)
            h = h[:m.start()] + blocks.strip('\n') + '\n                    ' + h[m.start():]
        else:
            ms = list(re.finditer(r'<a href="#[^"]+" class="%s">[^<]*</a>' % kind, h))
            if not ms:
                continue
            last = ms[-1]
            h = h[:last.end()] + blocks + h[last.end():]
    return h


def ensure_faq_section(h, qa, title):
    """Insert faq-section before <h2 id="conclusion"> if none exists."""
    inner = art(h)
    if FAQ_OPEN.search(inner):
        return h
    block = build_faq_section(qa, title, title)
    m = re.search(r'<h2 id="[^"]*conclusion[^"]*"', inner)
    if not m:
        inner = append_before_nav(inner, block)
    else:
        inner = inner[:m.start()] + block + '\n            ' + inner[m.start():]
    return set_art(h, inner)


FAQ_TITLE = {"EN": "Frequently Asked Questions",
             "zh-CN": "常见问题",
             "zh-TW": "常見問題"}


def apply_slug(slug, data, add_toc_entries=True):
    """data keys: EN / zh-CN / zh-TW, each with h2, add, faq."""
    log = {}
    for lang, pat in LANGS:
        rel = pat % slug
        d = data.get(lang)
        if not d:
            continue
        h = read(rel)
        o = h
        title = FAQ_TITLE[lang]
        if d.get("h2"):
            h = retitle_h2(h, d["h2"])
        h = drop_stray_faq_h2(h)
        if d.get("add"):
            anchor = d.get("anchor")
            inner = art(h)
            if anchor:
                inner = insert_before(inner, anchor, d["add"])
            elif FAQ_OPEN.search(inner):
                m = FAQ_OPEN.search(inner)
                inner = inner[:m.start()] + d["add"] + '\n\n            ' + inner[m.start():]
            else:
                m = re.search(r'<h2 id="[^"]*conclusion[^"]*"', inner)
                if m:
                    inner = inner[:m.start()] + d["add"] + '\n\n            ' + inner[m.start():]
                else:
                    inner = append_before_nav(inner, d["add"])
            h = set_art(h, inner)
            if add_toc_entries:
                ids = [(m.group(1), m.group(2)) for m in
                       re.finditer(r'<h2 id="([^"]+)">(.*?)</h2>', d["add"], re.S)]
                if ids:
                    h = add_toc(h, ids)
        if d.get("faq"):
            h = ensure_faq_section(h, d["faq"], title)
            h = map_art(h, lambda s: replace_faq(s, d["faq"], title))
        h = map_art(h, wrap_faq_h3)
        h = ensure_faq_ld(h)
        if h != o:
            guard(rel, o, h)
            write(rel, h)
        log[lang] = (en_words(h) if lang == "EN" else cjk(h))
    return log
