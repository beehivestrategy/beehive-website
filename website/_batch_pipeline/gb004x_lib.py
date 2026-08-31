# -*- coding: utf-8 -*-
"""gb004x_lib.py — apply-harness for gbatch_004 (verified against _check004.py).

Guarantees:
  * never writes inside <head>
  * never touches <footer ...>...</footer>
  * never touches share-button markup (id="share-*")
  * never removes ?v=20260826
  * never rewrites an existing root-relative (/..., http...) link
"""
import json
import os
import re

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
CACHE = os.path.join(ROOT, "_batch_pipeline/.gb004x_backup")
os.makedirs(CACHE, exist_ok=True)

SHARE_RE = re.compile(r'<button class="article-share-btn" id="share-[^"]*".*?</button>', re.S)


# ---------------------------------------------------------------- io / regions
def read(p):
    return open(p, encoding="utf-8").read()


def write(p, s):
    open(p, "w", encoding="utf-8").write(s)


def backup(p):
    key = p.replace(ROOT, "").strip("/").replace("/", "__")
    dst = os.path.join(CACHE, key)
    if not os.path.exists(dst):
        write(dst, read(p))


def art_bounds(h):
    m = re.search(r"<article\b[^>]*>", h)
    a = m.end()
    b = h.rfind("</article>")
    return a, b


def article_inner(h):
    a, b = art_bounds(h)
    return h[a:b]


def set_article(h, inner):
    a, b = art_bounds(h)
    return h[:a] + inner + h[b:]


def clean(s):
    s = re.sub(r"<[^>]+>", " ", s)
    for a, b in [("&nbsp;", " "), ("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                 ("&quot;", '"'), ("&#39;", "'"), ("&mdash;", "\u2014"),
                 ("&rsquo;", "\u2019"), ("&middot;", "\u00b7")]:
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()


def faq_bounds(h):
    """(start, end) of the <section class="faq-section"> element, or None."""
    i = h.find('<section class="faq-section"')
    if i == -1:
        return None
    depth = 0
    for m in re.finditer(r"<section\b|</section>", h[i:]):
        if m.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                return (i, i + m.end())
        else:
            depth += 1
    return None


# ------------------------------------------------------------------ measurements
def en_words(t):
    return len(re.findall(r"[A-Za-z0-9']+", t))


def cjk(t):
    return len(re.findall(r"[\u3400-\u9fff\uf900-\ufaff]", t))


def prose_region(h):
    art = article_inner(h)
    fb = faq_bounds(h)
    if fb:
        cut = fb[0] - len(h[:art_bounds(h)[0]]) if fb[0] > art_bounds(h)[0] else len(art)
        art = art[:max(0, cut)]
    art = re.sub(r"<script.*?</script>", " ", art, flags=re.S)
    art = re.sub(r"<style.*?</style>", " ", art, flags=re.S)
    art = re.sub(r"<[^>]+>", " ", art)
    return re.sub(r"\s+", " ", clean(art))


def metrics(h):
    t = prose_region(h)
    return en_words(t), cjk(t)


# ------------------------------------------------------------------ link fixing
def fix_links(h, prefix):
    """prefix: '' | 'zh-cn/' | 'zh-tw/'. Only rewrites RELATIVE hrefs (no leading
    '/' and no scheme) inside the recommended grid, the sidebar related list and
    the CTA card. Root-relative / absolute links are left untouched."""
    out = []
    pos = 0
    for m in re.finditer(r'<section class="recommended-section".*?</section>\s*</div>'
                         r'|<div class="sidebar-related-list">.*?</div>\s*</div>'
                         r'|<section class="article-cta".*?</section>', h, re.S):
        out.append(h[pos:m.start()])
        seg = m.group(0)

        def rep(mm):
            href = mm.group(1)
            if href.startswith("/") or href.startswith("#") or "://" in href:
                return mm.group(0)
            return 'href="/%s%s"' % (prefix, href)

        seg = re.sub(r'href="([^"]*)"', rep, seg)
        out.append(seg)
        pos = m.end()
    out.append(h[pos:])
    return "".join(out)


# ------------------------------------------------------------------- TOC rebuild
TOC_LINK = '                    <a href="#%s" class="toc-link">%s</a>'
TOC_M_LINK = '                    <a href="#%s" class="toc-mobile-link">%s</a>'


def rebuild_toc(h):
    inner = article_inner(h)
    fb = faq_bounds(h)
    if fb:
        a0 = art_bounds(h)[0]
        inner = inner[:max(0, fb[0] - a0)]
    items = []
    for m in re.finditer(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', inner, re.S):
        sid, txt = m.group(1), clean(m.group(2))
        if not txt:
            continue
        items.append((sid, txt))
    # FAQ entry
    fbt = faq_title(h)
    if fbt:
        items.append(("faq", fbt))
    if not items:
        return h
    new_links = "\n".join(TOC_LINK % (s, t) for s, t in items)
    new_mlinks = "\n".join(TOC_M_LINK % (s, t) for s, t in items)
    h = re.sub(r'(<nav class="toc-links">\s*).*?(\s*</nav>)',
               lambda m: m.group(1) + new_links + m.group(2), h, flags=re.S)
    h = re.sub(r'(<div class="toc-mobile-links">\s*).*?(\s*</div>)',
               lambda m: m.group(1) + new_mlinks + m.group(2), h, flags=re.S)
    return h


def faq_title(h):
    fb = faq_bounds(h)
    if not fb:
        return None
    blk = h[fb[0]:fb[1]]
    m = re.search(r'<h2 class="faq-section-title"[^>]*>(.*?)</h2>', blk, re.S)
    return clean(m.group(1)) if m else "FAQ"


# ------------------------------------------------------------------- H2 retitle
def retitle_h2(h, mapping):
    """mapping: {h2_id: new_text}"""
    def rep(m):
        sid = m.group(1)
        if sid in mapping:
            return '<h2 id="%s">%s</h2>' % (sid, mapping[sid])
        return m.group(0)
    return re.sub(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', rep, h, flags=re.S)


def drop_h2(h, ids):
    for sid in ids:
        h = re.sub(r'<h2 id="%s"[^>]*>.*?</h2>\s*' % re.escape(sid), "", h, count=1, flags=re.S)
    return h


def drop_h2_section(h, ids):
    """Remove an H2 plus every following sibling until the next h2 / section / nav.
    Used to delete the duplicate inline FAQ that sits before the real faq-section."""
    for sid in ids:
        m = re.search(r'<h2 id="%s"[^>]*>.*?</h2>' % re.escape(sid), h, re.S)
        if not m:
            continue
        end_m = re.search(r'<h2[\s>]|<section[\s>]|<nav[\s>]|</article>', h[m.end():])
        end = m.end() + (end_m.start() if end_m else len(h) - m.end())
        h = h[:m.start()] + h[end:]
    return h


# ------------------------------------------------------------------- sections
def insert_sections(h, sections, before="__AUTO__"):
    """sections: [(id, h2text, body_html)]"""
    if not sections:
        return h
    block = "\n".join(
        '<h2 id="%s">%s</h2>\n%s' % (sid, txt, body) for sid, txt, body in sections
    ) + "\n"
    a0 = art_bounds(h)[0]
    pos = None
    if before == "__AUTO__":
        for pat in [r'<h2 id="key-takeaways"', r'<h2 id="[^"]*takeaway[^"]*"',
                    '<section class="faq-section"', '<nav class="article-nav"']:
            m = re.search(pat, h[a0:])
            if m:
                pos = a0 + m.start()
                break
    elif before == "__FAQ__":
        fb = faq_bounds(h)
        pos = fb[0] if fb else None
    elif before == "__NAV__":
        m = re.search(r'<nav class="article-nav"', h[a0:])
        pos = a0 + m.start() if m else None
    else:
        m = re.search(r'<h2 id="%s"' % re.escape(before), h[a0:])
        pos = a0 + m.start() if m else None
    if pos is None:
        raise SystemExit("insert_sections: no anchor for " + before)
    line_start = h.rfind("\n", 0, pos) + 1
    indent = h[line_start:pos]
    indented = "\n".join((indent + l if l.strip() else l) for l in block.split("\n"))
    return h[:line_start] + indented + h[line_start:]


# ------------------------------------------------------------------- FAQ block
FAQ_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
           '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>'
           '<line x1="12" y1="17" x2="12.01" y2="17"/></svg>')
CHEVRON = ('<svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
           'stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>')


def render_faq(qa, title, indent="                "):
    o = []
    o.append('%s<section class="faq-section" id="faq" aria-label="%s">' % (indent, title))
    o.append('%s    <h2 class="faq-section-title">' % indent)
    o.append('%s        %s' % (indent, FAQ_SVG))
    o.append('%s        %s' % (indent, title))
    o.append('%s    </h2>' % indent)
    o.append('%s    <div class="faq-list">' % indent)
    for i, (q, a) in enumerate(qa, 1):
        o.append('%s        <div class="faq-item">' % indent)
        o.append('%s            <h3 style="margin:0"><button class="faq-question" aria-expanded="false">' % indent)
        o.append('%s                <span class="faq-question-text"><span class="faq-number">%d</span><span>%s</span></span>'
                 % (indent, i, q))
        o.append('%s                %s' % (indent, CHEVRON))
        o.append('%s            </button></h3>' % indent)
        o.append('%s            <div class="faq-answer" role="region"><div class="faq-answer-inner">%s</div></div>'
                 % (indent, a))
        o.append('%s        </div>' % indent)
    o.append('%s    </div>' % indent)
    o.append('%s</section>' % indent)
    return "\n".join(o)


def set_faq(h, qa, title):
    fb = faq_bounds(h)
    if fb:
        a0 = art_bounds(h)[0]
        if fb[0] < a0:      # FAQ outside the article — leave in place, still edit
            pass
        return h[:fb[0]] + render_faq(qa, title) + h[fb[1]:]
    # no FAQ yet -> insert before article-nav inside the article
    a0 = art_bounds(h)[0]
    m = re.search(r'<nav class="article-nav"', h[a0:])
    if not m:
        raise SystemExit("set_faq: no article-nav anchor")
    pos = a0 + m.start()
    line_start = h.rfind("\n", 0, pos) + 1
    indent = h[line_start:pos] or "            "
    return h[:line_start] + render_faq(qa, title, indent) + "\n\n" + h[line_start:]


# ------------------------------------------------------------------- JSON-LD
def build_ld(qa, indent="                "):
    data = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}
    body = json.dumps(data, ensure_ascii=False, indent=2)
    body = "\n".join(indent + l for l in body.split("\n"))
    return ('\n%s<script type="application/ld+json">\n%s\n%s</script>'
            % (indent, body, indent))


def ensure_ld(h, qa):
    fb = faq_bounds(h)
    if not fb:
        raise SystemExit("ensure_ld: no faq-section")
    end = fb[1]
    tail = h[end:]
    m = re.match(r'\s*<script type="application/ld\+json">.*?</script>', tail, re.S)
    if m and '"FAQPage"' in m.group(0).replace(" ", ""):
        return h[:end] + build_ld(qa) + tail[m.end():]
    return h[:end] + build_ld(qa) + tail


# ------------------------------------------------------------------- excerpts
_MANIFEST = {}


def manifest(lang):
    if lang not in _MANIFEST:
        sub = {"en": "blog", "zh-cn": "zh-cn/blog", "zh-tw": "zh-tw/blog"}[lang]
        data = json.load(open(os.path.join(ROOT, sub, "articles/manifest.json"), encoding="utf-8"))
        arts = data["articles"] if isinstance(data, dict) else data
        _MANIFEST[lang] = {a["slug"]: a for a in arts}
    return _MANIFEST[lang]


def fill_cards(h, lang):
    """Fill empty recommended-card-excerpt + fix untranslated (English) titles
    in non-English files using the language manifest."""
    man = manifest(lang)

    def card_rep(m):
        seg = m.group(0)
        hm = re.search(r'href="[^"]*?/([^/"]+)"', seg)
        slug = hm.group(1) if hm else None
        info = man.get(slug)
        if not info:
            return seg
        if lang != "en" and re.match(r"^[A-Za-z0-9 ,.'\-&]+$", info.get("title", "")):
            pass
        # excerpt
        ex = (info.get("excerpt") or info.get("description") or "").strip()
        if not ex:
            ex = (info.get("description") or "").strip()
        if ex:
            seg = re.sub(r'(<p class="recommended-card-excerpt">)\s*(</p>)',
                         lambda z: z.group(1) + ex + z.group(2), seg)
        # title: replace if it is still the slug-ised English string
        tm = re.search(r'<h3 class="recommended-card-title">(.*?)</h3>', seg, re.S)
        if tm:
            cur = tm.group(1).strip()
            want = info.get("title", "").strip()
            if want and cur != want:
                seg = seg.replace(tm.group(0),
                                  '<h3 class="recommended-card-title">%s</h3>' % want)
        # category
        cm = re.search(r'<span class="recommended-card-cat">(.*?)</span>', seg, re.S)
        if cm and info.get("category"):
            cur = cm.group(1).strip()
            want = info["category"].strip()
            if cur != want and re.match(r"^[A-Za-z ]+$", cur):
                seg = seg.replace(cm.group(0),
                                  '<span class="recommended-card-cat">%s</span>' % want)
        return seg

    return re.sub(r'<a href="[^"]*" class="recommended-card">.*?</a>', card_rep, h, flags=re.S)


# ------------------------------------------------------------------- CTA text
CTA_MAP = {
    "en": ("Book a Demo", "Explore the Solution"),
    "zh-cn": ("预约演示", "了解解决方案"),
    "zh-tw": ("預約示範", "了解解決方案"),
}


def fix_cta(h, lang):
    want_btn, want_sec = CTA_MAP[lang]
    m = re.search(r'<section class="article-cta".*?</section>', h, re.S)
    if not m:
        return h
    seg = m.group(0)
    seg = re.sub(r'(<a href="[^"]*" class="article-cta-btn">)[^<]*(</a>)',
                 lambda z: z.group(1) + want_btn + z.group(2), seg)
    seg = re.sub(r'(<a href="[^"]*" class="article-cta-secondary">)[^<]*(</a>)',
                 lambda z: z.group(1) + want_sec + z.group(2), seg)
    return h[:m.start()] + seg + h[m.end():]


# ------------------------------------------------------------------- repairs
def render_full(h, spec):
    """Rebuild the whole article inner from a spec:
    {"lead": html, "full": [(id, h2, body), ...], "faq": [...], "faq_title": str}
    Preserves the existing toc-mobile shell and article-nav markup."""
    m = re.search(r'<div class="toc-mobile" id="toc-mobile">.*?<div class="toc-mobile-links">.*?</div>\s*</div>',
                  h, re.S)
    toc = m.group(0) if m else ""
    if toc:
        toc = re.sub(r'(<div class="toc-mobile-links">).*?(</div>\s*</div>)',
                     lambda z: z.group(1) + "\n                    " + z.group(2), toc, flags=re.S)
    nm = re.search(r'<nav class="article-nav".*?</nav>', h, re.S)
    nav = nm.group(0) if nm else ""
    o = [toc]
    if spec.get("lead"):
        o.append(spec["lead"])
    for sid, txt, body in spec["full"]:
        o.append('<h2 id="%s">%s</h2>' % (sid, txt))
        o.append(body)
    o.append(render_faq(spec["faq"], spec.get("faq_title", "Frequently Asked Questions")))
    if nav:
        o.append(nav)
    return "\n".join(x for x in o if x)


def replace_article(h, inner):
    return set_article(h, inner)


def repair_text(h):
    """Remove literal 'undefined' left by a crashed templating pass."""
    h = re.sub(r'\bundefined\b(?![-\w])', '', h)
    h = re.sub(r'>\s*undefined\s*<', '><', h)
    return h


def strip_lead_strong(h):
    """zh files sometimes have <p class="article-lead"><strong>...</strong></p>; keep as-is."""
    return h
