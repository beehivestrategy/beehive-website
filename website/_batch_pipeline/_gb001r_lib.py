#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Worker library for gbatch_001 remediation run.

Guarantees (hard guardrails):
  - <head> byte-identical
  - <footer> block byte-identical
  - share-button markup byte-identical
  - ?v=20260826 preserved on /css/article.css and /js/article.js
  - root-relative / language-prefixed link paths unchanged (multiset)
"""
import re, os, json, html as htmlmod

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
LANGS = [
    ("blog/articles", "en", 2500),
    ("zh-cn/blog/articles", "zh-cn", 3500),
    ("zh-tw/blog/articles", "zh-tw", 3500),
]
CTA_PHRASE = {"en": "Book a Demo", "zh-cn": "预约演示", "zh-tw": "預約示範"}

# ---------------------------------------------------------------- io
def read(sub, slug):
    return open(os.path.join(ROOT, sub, slug + ".html"), encoding="utf-8").read()

def write(sub, slug, s):
    open(os.path.join(ROOT, sub, slug + ".html"), "w", encoding="utf-8").write(s)

# ---------------------------------------------------------------- metrics
def article_block(h):
    m = re.search(r'id="article-content"[\s\S]*?</article>', h, flags=re.I)
    if m: return m.group(0)
    m = re.search(r"<article\b[\s\S]*?</article>", h, flags=re.I)
    return m.group(0) if m else h

def plain(a):
    t = re.sub(r"<script[\s\S]*?</script>", " ", a, flags=re.I)
    t = re.sub(r"<style[\s\S]*?</style>", " ", t, flags=re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"&[a-zA-Z#0-9]+;", " ", t)
    return t

def wc_en(t): return len(re.findall(r"[A-Za-z0-9]+(?:['\-][A-Za-z0-9]+)*", t))
def cjk(t): return len(re.findall(r"[\u4e00-\u9fff\u3400-\u4dbf]", t))
def metric(h, lang):
    return wc_en(plain(article_block(h))) if lang == "en" else cjk(plain(article_block(h)))

# ---------------------------------------------------------------- guards
def head_of(h):
    i = h.lower().find("</head>")
    return h[:i + 7] if i >= 0 else ""

def footer_of(h):
    i = h.lower().find("<footer")
    return h[i:] if i >= 0 else ""

def share_of(h):
    i = h.find('class="sidebar-share"')
    if i < 0: return ""
    j = h.find("</div>", i)
    return h[i:j]

ROOTLINK = re.compile(r'(?:href|src)="(/[^"]*)"')

def rootlinks(h):
    return sorted(ROOTLINK.findall(h))

def guard(before, after, sub, slug, allow_link_add=False):
    errs = []
    if head_of(before) != head_of(after): errs.append("HEAD CHANGED")
    if footer_of(before) != footer_of(after): errs.append("FOOTER CHANGED")
    if share_of(before) != share_of(after): errs.append("SHARE CHANGED")
    if '/css/article.css?v=20260826' not in after: errs.append("CSS VERSION LOST")
    if '/js/article.js?v=20260826' not in after: errs.append("JS VERSION LOST")
    from collections import Counter
    cb, ca = Counter(rootlinks(before)), Counter(rootlinks(after))
    lost = {k: v for k, v in (cb - ca).items()}          # link paths that disappeared
    added = {k: v for k, v in (ca - cb).items()}         # link paths that appeared
    if lost:
        errs.append(f"LINKS LOST {sorted(lost)}")
    if added and not allow_link_add:
        errs.append(f"LINKS ADDED {sorted(added)}")
    return errs

# ---------------------------------------------------------------- FAQ
FAQ_RE = re.compile(r'<section class="faq-section"[\s\S]*?</section>', re.I)

def faq_items(fb):
    """Return list of (question_text, answer_text)."""
    out = []
    chunks = fb.split('<div class="faq-item">')[1:]
    for c in chunks:
        qm = re.search(r'class="faq-question-text"[^>]*>\s*(?:<span class="faq-number">\s*\d+\s*</span>)?\s*([\s\S]*?)\s*</(?:span|h3|h2|div|p)>', c)
        am = re.search(r'<div class="faq-answer-inner">([\s\S]*?)</div>', c)
        if qm and am:
            out.append((clean_txt(qm.group(1)), clean_txt(am.group(1))))
    return out

def clean_txt(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = htmlmod.unescape(s)
    s = re.sub(r"^\s*\d+\s+", "", s)   # strip duplicated leading "1 "
    return re.sub(r"\s+", " ", s).strip()

FAQ_TITLE = {"en": "Frequently Asked Questions", "zh-cn": "常见问题", "zh-tw": "常見問題"}

def replace_faq(html, items, lang):
    """Rebuild the .faq-section body with <h3> questions. Keeps wrapper attributes."""
    fb = FAQ_RE.search(html)
    if not fb: return None
    open_tag = fb.group(0)[:fb.group(0).index(">") + 1]
    open_tag = re.sub(r'aria-label="[^"]*"', f'aria-label="{FAQ_TITLE[lang]}"', open_tag)
    STYLE = 'margin:0;font-weight:inherit;font-size:inherit;line-height:inherit;'
    parts = [open_tag, f'                <h2 class="faq-section-title">',
             '                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
             '                    ' + FAQ_TITLE[lang],
             '                </h2>', '                <div class="faq-list">']
    for i, (q, a) in enumerate(items, 1):
        parts += [
            '                    <div class="faq-item">',
            f'                        <h3 class="faq-question-heading" style="{STYLE}"><button class="faq-question" aria-expanded="false">',
            f'                            <span class="faq-question-text"><span class="faq-number">{i}</span><span>{esc(q)}</span></span>',
            '                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>',
            '                        </button></h3>',
            f'                        <div class="faq-answer" role="region"><div class="faq-answer-inner">{esc(a)}</div></div>',
            '                    </div>',
        ]
    parts += ['                </div>', '            </section>']
    return html[:fb.start()] + "\n".join(parts) + html[fb.end():]

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def ensure_faq_h3(html):
    """Wrap each .faq-question button in <h3 class="faq-question-heading"> and strip
    the duplicated leading number in the visible question text."""
    fb = FAQ_RE.search(html)
    if not fb: return html, 0
    block = fb.group(0)
    if '<h3 class="faq-question-heading"' in block:
        new = block
    else:
        STYLE = 'margin:0;font-weight:inherit;font-size:inherit;line-height:inherit;'
        def wrap(m):
            indent, inner = m.group(1), m.group(2)
            return (f'{indent}<h3 class="faq-question-heading" style="{STYLE}">'
                    f'<button class="faq-question" aria-expanded="false">{inner}</button></h3>')
        new, n = re.subn(
            r'([ \t]*)<button class="faq-question" aria-expanded="false">([\s\S]*?)</button>',
            wrap, block)
        if n == 0: return html, 0
    # strip duplicated leading number inside question span
    def fixnum(m):
        return m.group(1) + re.sub(r'^\s*\d+\s+', '', m.group(2)) + m.group(3)
    new = re.sub(r'(<span class="faq-question-text"><span class="faq-number">\d+</span><span>)([\s\S]*?)(</span>)',
                 fixnum, new)
    if new == block: return html, 0
    return html[:fb.start()] + new + html[fb.end():], 1

# ---------------------------------------------------------------- JSON-LD
def build_faq_jsonld(items):
    ents = []
    for q, a in items:
        ents.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        })
    body = ",\n    ".join(json.dumps(e, ensure_ascii=False) for e in ents)
    return ('<script type="application/ld+json">\n{\n  "@context": "https://schema.org",\n'
            '  "@type": "FAQPage",\n  "mainEntity": [\n    ' + body + '\n  ]\n}\n</script>')

LD_RE = re.compile(r'<script type="application/ld\+json"[^>]*>((?:(?!</script>)[\s\S])*)</script>', re.I)

def _body_faq_scripts(out):
    he = out.lower().find("</head>")
    return [m for m in LD_RE.finditer(out)
            if m.start() >= he and '"FAQPage"' in m.group(1)]

def sync_jsonld(html, lang):
    """Ensure exactly one FAQPage JSON-LD exists in the BODY, placed immediately after
    the FAQ section's closing </section>. Never touches head."""
    fb = FAQ_RE.search(html)
    if not fb: return html, "no-faq"
    items = faq_items(fb.group(0))
    if len(items) < 3: return html, f"faq-items<3 ({len(items)})"
    script = build_faq_jsonld(items)
    he = html.lower().find("</head>")
    # remove EVERY FAQPage script that lives in the BODY (keep head untouched)
    out, removed = html, 0
    while True:
        hits = _body_faq_scripts(out)
        if not hits: break
        m = hits[0]
        out = out[:m.start()] + out[m.end():]
        removed += 1
    he3 = out.lower().find("</head>")
    tail = out[he3:]
    tail = re.sub(r"[ \t]*\n(?:[ \t]*\n)+", "\n\n", tail)
    out = out[:he3] + tail
    fb2 = FAQ_RE.search(out)
    if not fb2: return html, "faq-lost"
    end = fb2.end()
    out = out[:end] + "\n" + script + out[end:]
    # normalise: collapse accidental blank-line pileups around the script
    out = re.sub(r"\n{3,}<script", "\n\n<script", out)
    return out, ("updated" if removed else "added")

# ---------------------------------------------------------------- CTA
def ensure_cta(html, lang):
    phrase = CTA_PHRASE[lang]
    m = re.search(r'(<a\b[^>]*class="[^"]*article-cta-btn[^"]*"[^>]*>)([\s\S]*?)(</a>)', html)
    if not m: return html, "no-cta-btn"
    if phrase in m.group(2): return html, "ok"
    new = m.group(1) + phrase + m.group(3)
    return html[:m.start()] + new + html[m.end():], "fixed"

# ---------------------------------------------------------------- H2
def _norm_key(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"[\s？?。．.,，、:：]+", "", s)
    try:
        from _gb001r_s2t import s2tw
        s = s2tw(s)
    except Exception:
        pass
    return s.lower()


def set_h2_text(html, key, newtext):
    """Rename an <h2> identified by id, exact text, or s2tw-normalised id/text.
    Also syncs matching TOC link labels."""
    pat = re.compile(r'(<h2 id="' + re.escape(key) + r'"[^>]*>)([\s\S]*?)(</h2>)', re.I)
    m = pat.search(html)
    if not m:
        cands = []
        for mm in re.finditer(r'<h2\b(?:[^>]*?id="([^"]*)")?[^>]*>([\s\S]*?)</h2>', html, re.I):
            cands.append((mm.group(1) or "", re.sub(r"<[^>]+>", "", mm.group(2)).strip(), mm))
        nk = _norm_key(key)
        hit = None
        for hid, txt, mm in cands:
            if txt == key or (hid and hid == key):
                hit = mm; break
        if hit is None:
            for hid, txt, mm in cands:
                if _norm_key(txt) == nk or (hid and _norm_key(hid) == nk):
                    hit = mm; break
        if hit is None: return html, False
        m = re.match(r'(<h2\b[^>]*>)([\s\S]*?)(</h2>)', hit.group(0), re.I)
        full = hit.start()
        html = html[:full] + m.group(1) + newtext + m.group(3) + html[full + len(hit.group(0)):]
    else:
        html = html[:m.start()] + m.group(1) + newtext + m.group(3) + html[m.end():]
    for cls in ("toc-link", "toc-mobile-link"):
        p = re.compile(r'(<a href="#[^"]*" class="' + cls + r'">)([\s\S]*?)(</a>)')
        for mm in list(p.finditer(html)):
            if _norm_key(mm.group(2)) == _norm_key(key):
                html = html[:mm.start()] + mm.group(1) + newtext + mm.group(3) + html[mm.end():]
                break
    return html, True

TAG_RE = re.compile(r'(<[^>]*>)')

def s2tw_body(html, conv):
    """Convert simplified->traditional in TEXT NODES only, between </head> and <footer>."""
    he = html.lower().find("</head>")
    if he < 0: he = 0
    fe = html.lower().find("<footer")
    if fe < 0: fe = len(html)
    head, body, tail = html[:he], html[he:fe], html[fe:]
    parts = TAG_RE.split(body)
    out = [p if p.startswith("<") else conv(p) for p in parts]
    return head + "".join(out) + tail

def h2_list(html):
    return [(m.group(1) or "", re.sub(r"<[^>]+>", "", m.group(2)).strip())
            for m in re.finditer(r'<h2\b[^>]*?(?:id="([^"]*)")?[^>]*>([\s\S]*?)</h2>', html, re.I)]

# ---------------------------------------------------------------- insertion
def insert_before_h2(html, anchor, block):
    """Insert block immediately before the <h2> identified by anchor.
    anchor may be an id or a substring of the heading text."""
    m = re.search(r'[ \t]*<h2 id="' + re.escape(anchor) + r'"', html, re.I)
    if not m:
        for mm in re.finditer(r'<(h2)\b[^>]*>([\s\S]*?)</h2>', html, re.I):
            txt = re.sub(r"<[^>]+>", "", mm.group(2)).strip()
            if anchor in txt:
                # back up to the start of the line containing the h2
                ls = html.rfind("\n", 0, mm.start()) + 1
                m = re.compile(re.escape(html[ls:mm.start()]) + r"<h2").match(html, ls) or mm
                return html[:ls] + block.rstrip() + "\n\n" + html[ls:]
    if not m: return None
    return html[:m.start()] + block.rstrip() + "\n\n" + html[m.start():]

def add_toc(html, hid, text):
    """Append a TOC entry (sidebar + mobile) if not already present."""
    for cls in ("toc-link", "toc-mobile-link"):
        if f'href="#{hid}"' in html and cls in html:
            if re.search(r'<a href="#' + re.escape(hid) + r'" class="' + cls + r'">', html):
                continue
        p = re.compile(r'(<nav class="toc-links">)([\s\S]*?)(</nav>)' if cls == "toc-link"
                       else r'(<div class="toc-mobile-links">)([\s\S]*?)(</div>)')
        m = p.search(html)
        if not m: continue
        indent = "                    " if cls == "toc-link" else "                    "
        link = f'{indent}<a href="#{hid}" class="{cls}">{text}</a>\n'
        html = html[:m.end(2)] + link + html[m.end(2):]
    return html

def insert_section(html, hid, title, body, toc=True):
    """Insert an <h2 id="hid">title</h2> + body just before the FAQ section."""
    fb = FAQ_RE.search(html)
    if not fb: return None
    block = f'<h2 id="{hid}">{title}</h2>\n{body.strip()}\n'
    out = html[:fb.start()] + block + "\n" + html[fb.start():]
    if toc: out = add_toc(out, hid, title)
    return out

# ---------------------------------------------------------------- excerpts
def fill_excerpts(html, excerpts):
    """Fill empty <p class="recommended-card-excerpt"></p> in order."""
    idx = [0]
    def rep(m):
        if idx[0] < len(excerpts) and excerpts[idx[0]]:
            v = excerpts[idx[0]]
            idx[0] += 1
            return f'<p class="recommended-card-excerpt">{v}</p>'
        idx[0] += 1
        return m.group(0)
    return re.sub(r'<p class="recommended-card-excerpt">\s*</p>', rep, html)
