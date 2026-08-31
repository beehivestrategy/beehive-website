#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Helpers for gbatch_001 standardisation. Body-only edits: never touches <head>,
<footer>, or share-button markup."""
import os, re, json, html as ihtml

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"

LANGS = {
    "en":    ("blog/articles",      "en",    "Book a Demo", "Frequently Asked Questions", "Recommended Articles"),
    "zh-CN": ("zh-cn/blog/articles","zh-CN", "预约演示",    "常见问题",                   "推荐阅读"),
    "zh-TW": ("zh-tw/blog/articles","zh-TW", "預約示範",    "常見問題",                   "推薦閱讀"),
}

def path(slug, lang):
    return os.path.join(ROOT, LANGS[lang][0], slug + ".html")

def read(slug, lang):
    return open(path(slug, lang), encoding="utf-8").read()

def write(slug, lang, h):
    open(path(slug, lang), "w", encoding="utf-8").write(h)

# ---------- metrics ----------
def cjk(s): return len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', s))

def wc(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'&[a-z]+;', ' ', s); s = re.sub(r'&#\d+;', ' ', s)
    return len(s.split())

def body_of(h):
    m = re.search(r'<article class="article-content" id="article-content">(.*?)</article>', h, re.S)
    if m: return m.group(1)
    m = re.search(r'<article[^>]*>(.*?)</article>', h, re.S)
    return m.group(1) if m else h

def metric(h, lang):
    b = body_of(h)
    return wc(b) if lang == "en" else cjk(b)

# ---------- TOC sync ----------
def add_toc(h, hid, text):
    link = f'<a href="#{hid}" class="toc-link">{text}</a>'
    mlink = f'<a href="#{hid}" class="toc-mobile-link">{text}</a>'
    out = h
    for cls, lk in (("toc-link", link), ("toc-mobile-link", mlink)):
        m = re.search(r'(<nav class="%s">)(.*?)(</nav>)' % cls, out, re.S)
        if not m:
            m = re.search(r'(<div class="%s">)(.*?)(</div>)' % cls, out, re.S)
        if m and lk not in m.group(2):
            out = out[:m.end(2)] + "\n                    " + lk + out[m.end(2):]
    return out

def retitle_toc(h, hid, newtext):
    out = h
    for cls in ("toc-link", "toc-mobile-link"):
        pat = re.compile(r'(<a href="#%s" class="%s">)(.*?)(</a>)' % (re.escape(hid), cls), re.S)
        out = pat.sub(lambda m: m.group(1) + newtext + m.group(3), out)
    return out

def _norm_cjk(s):
    """Normalise an id for fuzzy matching: convert to traditional so that zh-CN and
    zh-TW ids (which are often inconsistent mixtures) compare equal."""
    try:
        import opencc
        return opencc.OpenCC('s2twp').convert(s)
    except Exception:
        return s


def resolve_h2_id(h, hid):
    """Find the real h2 id in the file, tolerating simplified/traditional drift."""
    ids = re.findall(r'<h2 id="([^"]+)"', h)
    if hid in ids:
        return hid
    target = _norm_cjk(hid)
    for i in ids:
        if _norm_cjk(i) == target:
            return i
    # last resort: near-identical ids (zh-CN / zh-TW files often differ by one
    # character, e.g. 战略 vs 策略)
    import difflib
    near = difflib.get_close_matches(target, [_norm_cjk(i) for i in ids], n=1, cutoff=0.75)
    if near:
        for i in ids:
            if _norm_cjk(i) == near[0]:
                return i
    return None


def retitle_h2(h, hid, newtext):
    """Change an <h2 id=hid> display text and sync both TOCs."""
    real = resolve_h2_id(h, hid)
    if real is None:
        return h, 0
    hid = real
    pat = re.compile(r'(<h2 id="%s"[^>]*>)(.*?)(</h2>)' % re.escape(hid), re.S)
    n = 0
    def rep(m):
        nonlocal n
        n += 1
        return m.group(1) + newtext + m.group(3)
    h = pat.sub(rep, h)
    if n:
        h = retitle_toc(h, hid, newtext)
    return h, n

# ---------- section insertion ----------
def insert_sections(h, sections):
    """sections: list of (h2_id, h2_title, inner_html). Inserted before FAQ (or article-nav)."""
    anchor = None
    m = re.search(r'<section class="faq-section"', h)
    if m:
        anchor = m.start()
    else:
        m = re.search(r'<nav class="article-nav"', h)
        if m:
            anchor = m.start()
        else:
            m = re.search(r'</article>', h)
            anchor = m.start() if m else None
    if anchor is None:
        raise RuntimeError("no insertion anchor")
    existing = set(re.findall(r'<h2 id="([^"]+)"', h))
    sections = [s for s in sections if s[0] not in existing]
    if not sections:
        return h
    block = ""
    for hid, title, inner in sections:
        block += f'<h2 id="{hid}">{title}</h2>\n{inner}\n'
    out = h[:anchor] + "\n" + block + "\n" + h[anchor:]
    for hid, title, _ in sections:
        out = add_toc(out, hid, title)
    return out

def replace_section_bodies(h, mapping):
    """mapping: {h2_id: (new_title, new_inner_html)}.

    Replaces the prose between each named <h2> and the next <h2> (or the FAQ section /
    end of the article).  Ids and TOC anchors are preserved.
    """
    out = h
    for hid, (title, inner) in mapping.items():
        real = resolve_h2_id(out, hid)
        if real is None:
            continue
        m = re.search(r'<h2 id="%s"[^>]*>.*?</h2>' % re.escape(real), out, re.S)
        if not m:
            continue
        start = m.end()
        # find the next boundary
        cands = [x.start() for x in re.finditer(r'<h2 id="|<section class="faq-section"|<nav class="article-nav"|</article>', out[start:])]
        end = start + (cands[0] if cands else len(out) - start)
        out = out[:start] + "\n" + inner + "\n" + out[end:]
        if title:
            out, _ = retitle_h2(out, real, title)
    return out


def replace_lead(h, new_lead_html):
    """Replace the <p class="article-lead"> … </p> content."""
    m = re.search(r'<p class="article-lead">(.*?)</p>', h, re.S)
    if not m:
        return h
    return h[:m.start()] + '<p class="article-lead">' + new_lead_html + '</p>' + h[m.end():]


# ---------- FAQ rebuild ----------
CHEVRON = ('<svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
           'stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>')

def build_faq(qa, lang, section_attrs='class="faq-section" id="faq"', title=None):
    if title is None:
        title = LANGS[lang][3]
    aria = {'en': 'Frequently Asked Questions', 'zh-CN': '常见问题', 'zh-TW': '常見問題'}[lang]
    if 'aria-label' not in section_attrs:
        section_attrs = f'class="faq-section" id="faq" aria-label="{aria}"'
    items = []
    for i, (q, a) in enumerate(qa, 1):
        # The number badge sits outside the <h3> so the heading text — and therefore the
        # FAQPage JSON-LD name — is exactly the question.
        items.append(
            '                    <div class="faq-item">\n'
            '                        <div class="faq-question" aria-expanded="false">\n'
            f'                            <span class="faq-number">{i}</span>\n'
            f'                            <h3 class="faq-question-text" style="margin:0;font-size:inherit;'
            f'font-weight:600;line-height:1.5">{q}</h3>\n'
            f'                            {CHEVRON}\n'
            '                        </div>\n'
            f'                        <div class="faq-answer" role="region"><div class="faq-answer-inner">{a}</div></div>\n'
            '                    </div>')
    return (
        f'            <section {section_attrs}>\n'
        '                <h2 class="faq-section-title">\n'
        '                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>'
        '<line x1="12" y1="17" x2="12.01" y2="17"/></svg>\n'
        f'                    {title}\n'
        '                </h2>\n'
        '                <div class="faq-list">\n'
        + "\n".join(items) + "\n"
        '                </div>\n'
        '            </section>')

def replace_or_add_faq(h, qa, lang):
    """Replace existing faq-section (or insert one before article-nav). Returns (html, added)."""
    m = re.search(r'[ \t]*<section class="faq-section".*?</section>', h, re.S)
    new = build_faq(qa, lang)
    if m:
        return h[:m.start()] + new + h[m.end():], False
    m = re.search(r'<nav class="article-nav"', h)
    if m:
        return h[:m.start()] + new + "\n\n            " + h[m.start():], True
    m = re.search(r'</article>', h)
    return h[:m.start()] + new + "\n" + h[m.start():], True

# ---------- JSON-LD ----------
def jsonld_block(qa):
    obj = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": ihtml.unescape(q),
                           "acceptedAnswer": {"@type": "Answer", "text": ihtml.unescape(a)}}
                          for q, a in qa]}
    return ('<script type="application/ld+json">\n'
            + json.dumps(obj, ensure_ascii=False, indent=2)
            + '\n</script>')

def put_jsonld_after_faq(h, qa):
    """Insert a FAQPage JSON-LD right after the FAQ section's closing tag (body, never head)."""
    m = re.search(r'<section class="faq-section".*?</section>', h, re.S)
    if not m:
        raise RuntimeError("no faq section to anchor JSON-LD")
    insert_at = m.end()
    # strip any previously body-inserted FAQPage LD immediately after
    tail = h[insert_at:]
    tail = re.sub(r'\s*<script type="application/ld\+json">\s*\{[^{}]*"FAQPage".*?</script>',
                  '', tail, count=1, flags=re.S)
    return h[:insert_at] + "\n            " + jsonld_block(qa) + "\n" + tail

def has_faqpage_ld(h):
    for ld in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        if '"FAQPage"' in ld:
            try:
                o = json.loads(ld)
                if isinstance(o, dict) and "@graph" in o:
                    o = [x for x in o["@graph"] if x.get("@type") == "FAQPage"]
                    o = o[0] if o else {}
                me = o.get("mainEntity", [])
                if isinstance(me, list) and len(me) >= 3:
                    return True
            except Exception:
                pass
    return False

# ---------- CTA ----------
def ensure_cta(h, lang):
    phrase = LANGS[lang][2]
    m = re.search(r'(<a[^>]*class="article-cta-btn"[^>]*>)(.*?)(</a>)', h, re.S)
    if not m:
        return h, False
    if phrase in m.group(2):
        return h, False
    return h[:m.start(2)] + phrase + h[m.end(2):], True

# ---------- recommended hrefs ----------
PREFIX = {"en": "/blog/articles/", "zh-CN": "/zh-cn/blog/articles/", "zh-TW": "/zh-tw/blog/articles/"}

def fix_recommended(h, lang):
    pre = PREFIX[lang]
    changed = 0
    def rep(m):
        nonlocal changed
        href = m.group(2)
        slug = href.rstrip("/").split("/")[-1]
        new = pre + slug
        if new != href:
            changed += 1
            return m.group(1) + 'href="' + new + '"' + m.group(3)
        return m.group(0)
    return re.sub(r'(<a )href="([^"]*)"(\s+class="recommended-card")', rep, h), changed

def rec_hrefs(h):
    return re.findall(r'<a href="([^"]*)" class="recommended-card"', h)

def fill_excerpts(h, excerpts):
    """excerpts: list of strings, one per recommended card (in order)."""
    def rep(m):
        nonlocal i
        s = excerpts[i] if i < len(excerpts) else ""
        i += 1
        if m.group(1).strip():
            return m.group(0)
        return '<p class="recommended-card-excerpt">' + s + '</p>'
    i = 0
    return re.sub(r'<p class="recommended-card-excerpt">(.*?)</p>', rep, h, flags=re.S)
