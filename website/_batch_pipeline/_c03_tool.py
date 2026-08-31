#!/usr/bin/env python3
"""Chunk-03 body applier. Rebuilds article body + FAQ + TOC + recommended cards,
without touching <head>, <footer>, share markup, or any root-relative paths."""
import re, os, json, html as ihtml

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"

FAQ_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'
CHEV = '<svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>'

L = {
    "en": dict(faq_title="Frequently Asked Questions", toc="Table of Contents", prefix="/blog/articles/"),
    "cn": dict(faq_title="常见问题", toc="目录", prefix="/zh-cn/blog/articles/"),
    "tw": dict(faq_title="常見問題", toc="目錄", prefix="/zh-tw/blog/articles/"),
}


def path_for(lang, slug):
    return os.path.join(ROOT, {"en": "blog/articles", "cn": "zh-cn/blog/articles", "tw": "zh-tw/blog/articles"}[lang], slug + ".html")


def read(p):
    return open(p, encoding="utf-8").read()


def write(p, s):
    open(p, "w", encoding="utf-8").write(s)


def strip_tags(s):
    s = re.sub(r'<script.*?</script>', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    return ihtml.unescape(s)


def en_words(s):
    return len(re.findall(r"[A-Za-z][A-Za-z'\-]*", s))


def cjk(s):
    return len(re.findall(r'[\u4e00-\u9fff]', s))


def body_of(h):
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', h, re.S)
    return m.group(1) if m else ""


def measure(h, lang):
    t = strip_tags(body_of(h))
    return en_words(t) if lang == "en" else cjk(t)


def get_h1(h):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', h, re.S)
    return re.sub(r'\s+', ' ', strip_tags(m.group(1))).strip() if m else ""


def get_desc(h):
    m = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]*)"', h) or \
        re.search(r'<meta[^>]+content="([^"]*)"[^>]+name="description"', h)
    return ihtml.unescape(m.group(1)).strip() if m else ""


def head_faq_pairs(h):
    """Return (pairs, script_span) for the FAQPage JSON-LD if present."""
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        if '"FAQPage"' in m.group(1):
            try:
                d = json.loads(m.group(1))
            except Exception:
                return None, m.span()
            pairs = [(q["name"], q["acceptedAnswer"]["text"]) for q in d.get("mainEntity", [])]
            return pairs, m.span()
    return None, None


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("'", "&#x27;"))


def build_faq(pairs, lang, indent="            "):
    """pairs: list of (question, answer) with HTML entities already decoded."""
    i = indent
    out = [f'{i}<section class="faq-section" id="faq" aria-label="{L[lang]["faq_title"]}">',
           f'{i}    <h2 class="faq-section-title">',
           f'{i}        {FAQ_SVG}',
           f'{i}        {L[lang]["faq_title"]}',
           f'{i}    </h2>',
           f'{i}    <div class="faq-list">']
    for n, (q, a) in enumerate(pairs, 1):
        out += [f'{i}        <div class="faq-item">',
                f'{i}            <h3 class="faq-question-heading" style="margin:0;font-size:inherit;font-weight:inherit;">',
                f'{i}                <button class="faq-question" aria-expanded="false">',
                f'{i}                    <span class="faq-question-text"><span class="faq-number">{n}</span><span>{esc(q)}</span></span>',
                f'{i}                    {CHEV}',
                f'{i}                </button>',
                f'{i}            </h3>',
                f'{i}            <div class="faq-answer" role="region"><div class="faq-answer-inner">{esc(a)}</div></div>',
                f'{i}        </div>']
    out += [f'{i}    </div>', f'{i}</section>']
    return "\n".join(out)


def build_faq_ld(pairs, lang, indent="            "):
    d = {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q,
                         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}
    j = json.dumps(d, ensure_ascii=False)
    return f'{indent}<script type="application/ld+json">{j}</script>'


def build_toc(h2s, lang, mobile=True):
    """h2s: list of (id, text)."""
    if mobile:
        i = "                "
        rows = "\n".join(f'{i}    <a href="#{hid}" class="toc-mobile-link">{esc(t)}</a>' for hid, t in h2s)
        return ('            <div class="toc-mobile" id="toc-mobile">\n'
                f'                <button class="toc-mobile-toggle" aria-expanded="false">{L[lang]["toc"]} '
                '<svg class="toc-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></button>\n'
                '                <div class="toc-mobile-links">\n' + rows +
                '\n                </div>\n            </div>')
    i = "                    "
    return "\n".join(f'{i}<a href="#{hid}" class="toc-link">{esc(t)}</a>' for hid, t in h2s)


def h2_list(body):
    out = []
    for m in re.finditer(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', body, re.S):
        out.append((m.group(1), re.sub(r'\s+', ' ', strip_tags(m.group(2))).strip()))
    return out


def replace_body(h, lang, prose, faq_pairs=None, add_ld_if_missing=True):
    """prose = HTML string: lead paragraph + h2 sections (no FAQ, no toc)."""
    am = re.search(r'(<article[^>]*id="article-content"[^>]*>)(.*?)(</article>)', h, re.S)
    assert am, "no article-content"
    inner = am.group(2)

    # preserve trailing article-nav
    nm = re.search(r'(\s*<nav class="article-nav".*)$', inner, re.S)
    tail = nm.group(1) if nm else "\n"

    # FAQ pairs: prefer existing FAQPage JSON-LD (head) so page and schema match
    existing, span = head_faq_pairs(h)
    if existing and len(existing) >= 3:
        pairs = [(ihtml.unescape(q), ihtml.unescape(a)) for q, a in existing]
        ld_added = False
    else:
        assert faq_pairs and len(faq_pairs) >= 3, "need faq pairs"
        pairs = faq_pairs
        ld_added = True

    toc = build_toc(h2_list(prose), lang, mobile=True)
    faq = build_faq(pairs, lang)
    if ld_added and add_ld_if_missing:
        faq = faq + "\n" + build_faq_ld(pairs, lang)

    new_inner = "\n" + toc + "\n" + prose.strip() + "\n\n" + faq + "\n" + tail.strip("\n") + "\n        "
    h = h[:am.start(2)] + new_inner + h[am.end(2):]

    # duplicated <article ...> open tags (pre-existing defect) -> keep first only
    open_tag = am.group(1)
    if h.count(open_tag) > 1:
        first = h.find(open_tag) + len(open_tag)
        h = h[:first] + h[first:].replace(open_tag, "", h.count(open_tag) - 1)

    # sync sidebar TOC
    h = re.sub(r'(<nav class="toc-links">)(.*?)(</nav>)',
               lambda m: m.group(1) + "\n" + build_toc(h2_list(prose), lang, mobile=False) + "\n                " + m.group(3),
               h, count=1, flags=re.S)
    return h, ld_added


def fix_recommended(h, lang):
    """Root-relative + language-prefixed hrefs; real titles; filled excerpts."""
    pref = L[lang]["prefix"]
    subdir = {"en": "blog/articles", "cn": "zh-cn/blog/articles", "tw": "zh-tw/blog/articles"}[lang]

    def card(m):
        block = m.group(0)
        href = re.search(r'href="([^"]+)"', block).group(1)
        slug = href.rstrip("/").split("/")[-1]
        newhref = pref + slug
        block = block.replace(f'href="{href}"', f'href="{newhref}"', 1)
        tp = os.path.join(ROOT, subdir, slug + ".html")
        if os.path.exists(tp):
            th = read(tp)
            t, d = get_h1(th), get_desc(th)
            if t and (lang == "en" or cjk(t) >= 2):
                block = re.sub(r'(<h3 class="recommended-card-title">)(.*?)(</h3>)',
                               lambda x: x.group(1) + esc(t) + x.group(3), block, flags=re.S)
            if d:
                block = re.sub(r'(<p class="recommended-card-excerpt">)(\s*)(</p>)',
                               lambda x: x.group(1) + esc(d[:170]) + x.group(3), block, flags=re.S)
        return block

    return re.sub(r'<a[^>]*class="recommended-card"[^>]*>.*?</a>', card, h, flags=re.S)


def extract_prose(h):
    """Existing prose: from first lead/h2 up to FAQ section or article-nav."""
    inner = body_of(h)
    starts = [inner.find('<p class="article-lead"'), inner.find('<h2 id=')]
    starts = [s for s in starts if s >= 0]
    assert starts, "no prose start"
    s = min(starts)
    ends = [inner.find('<section class="faq-section"'), inner.find('<nav class="article-nav"')]
    ends = [e for e in ends if e > s]
    e = min(ends) if ends else len(inner)
    return inner[s:e].strip()


def rename_h2(prose, mapping):
    """mapping: {h2_id: new visible text}. Ids untouched."""
    def rep(m):
        hid = m.group(1)
        if hid in mapping:
            return f'<h2 id="{hid}">{mapping[hid]}</h2>'
        return m.group(0)
    out = re.sub(r'<h2 id="([^"]+)"[^>]*>.*?</h2>', rep, prose, flags=re.S)
    missing = [k for k in mapping if f'id="{k}"' not in out]
    assert not missing, f"h2 ids not found: {missing}"
    return out


def insert_before(prose, h2_id, new_html):
    m = re.search(r'<h2 id="%s"' % re.escape(h2_id), prose)
    assert m, f"anchor h2 not found: {h2_id}"
    return prose[:m.start()] + new_html.strip() + "\n" + prose[m.start():]


def drop_paragraph(prose, needle):
    """Remove a <p ...>...</p> containing needle (e.g. leftover English lead)."""
    for m in re.finditer(r'<p[^>]*>.*?</p>', prose, flags=re.S):
        if needle in m.group(0):
            return prose[:m.start()] + prose[m.end():]
    return prose


def to_tw(s):
    import opencc
    return opencc.OpenCC('s2twp').convert(s)


def apply_slug(lang, slug, prose, faq_pairs=None, expected_h1_contains=None):
    p = path_for(lang, slug)
    h = read(p)
    h1 = get_h1(h)
    before = measure(h, lang)
    if expected_h1_contains:
        assert expected_h1_contains.lower() in h1.lower(), f"H1 mismatch for {slug} [{lang}]: {h1!r}"
    h, ld_added = replace_body(h, lang, prose, faq_pairs)
    h = fix_recommended(h, lang)
    write(p, h)
    after = measure(read(p), lang)
    faqn = len(re.findall(r'faq-question-heading', h))
    ldn = len(re.findall(r'"FAQPage"', h))
    print(f"  {lang}: {before} -> {after} | faq={faqn} | FAQPage_count={ldn} | ld_added={'y' if ld_added else 'n'} | h1={h1[:70]}")
    return after
