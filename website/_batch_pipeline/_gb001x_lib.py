#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Helpers for bringing gbatch_001 articles to the GEO/SEO standard, in place."""
import os
import re
import json
import html as _html
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gb001_s2t import s2tw  # noqa: E402

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
LANGS = [("EN", "blog/articles"), ("zh-CN", "zh-cn/blog/articles"), ("zh-TW", "zh-tw/blog/articles")]
PREFIX = {"EN": "/blog/articles", "zh-CN": "/zh-cn/blog/articles", "zh-TW": "/zh-tw/blog/articles"}
PHRASE = {"EN": "Book a Demo", "zh-CN": "预约演示", "zh-TW": "預約示範"}
CJK = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]')


def path(slug, sub):
    return os.path.join(ROOT, sub, slug + ".html")


def read(slug, sub):
    return open(path(slug, sub), encoding="utf-8").read()


def write(slug, sub, txt):
    open(path(slug, sub), "w", encoding="utf-8").write(txt)


def strip_tags(h):
    h = re.sub(r'<script[^>]*>.*?</script>', ' ', h, flags=re.S | re.I)
    h = re.sub(r'<style[^>]*>.*?</style>', ' ', h, flags=re.S | re.I)
    h = re.sub(r'<!--.*?-->', ' ', h, flags=re.S)
    h = re.sub(r'<[^>]+>', ' ', h)
    return _html.unescape(h)


def unescape(s):
    return _html.unescape(s)


# ---------------------------------------------------------------- article body
ART_RE = re.compile(r'<article[^>]*id=["\']article-content["\'][^>]*>(.*?)</article>', re.S | re.I)


def article_body(raw):
    m = ART_RE.search(raw)
    return m.group(1) if m else raw


def metrics(raw, lang):
    body = article_body(raw)
    txt = strip_tags(body)
    return {
        "words": len(re.findall(r"[A-Za-z][A-Za-z'\u2019\-]*", txt)),
        "cjk": len(CJK.findall(txt)),
    }


# ------------------------------------------------------------------- FAQ block
def faq_span(raw):
    m = re.search(r'<section[^>]*class="faq-section"', raw)
    if not m:
        return None
    s = m.start()
    e = raw.find('</section>', s)
    if e == -1:
        return None
    return s, e + len('</section>')


def extract_faq(raw):
    """[(question, answer_html_or_text), ...] from the on-page FAQ section."""
    sp = faq_span(raw)
    if not sp:
        return []
    blk = raw[sp[0]:sp[1]]
    out = []
    for item in re.findall(r'<div class="faq-item">(.*?)<div class="faq-answer"', blk, re.S):
        qm = re.search(r'<span class="faq-question-text">(.*?)</span>\s*</span>', item, re.S)
        if not qm:
            continue
        inner = re.sub(r'<span class="faq-number">.*?</span>', '', qm.group(1), flags=re.S)
        q = unescape(strip_tags(inner)).strip()
        q = re.sub(r'^\s*\d+\s+', '', q)
        out.append(q)
    ans = re.findall(r'<div class="faq-answer-inner">(.*?)</div>', blk, re.S)
    res = []
    for i, q in enumerate(out):
        a = unescape(strip_tags(ans[i])).strip() if i < len(ans) else ""
        res.append((q, a))
    return res


def wrap_faq_h3(raw):
    """Wrap each FAQ button in <h3 class="faq-question-heading"> and drop the
    duplicated leading number inside the question text."""
    sp = faq_span(raw)
    if not sp:
        return raw, 0
    blk = raw[sp[0]:sp[1]]
    if '<h3 class="faq-question-heading"' in blk:
        return raw, 0

    n = 0

    def _item(mo):
        nonlocal n
        inner = mo.group(1)
        if '<h3' in inner:
            return mo.group(0)
        # strip duplicate number prefix inside the question <span>
        def _q(m):
            return '<span>' + re.sub(r'^\s*\d+\s+', '', m.group(1)) + '</span>'
        inner = re.sub(r'<span>(?!<span class="faq-number")(.*?)</span>', _q, inner, count=1, flags=re.S)
        n += 1
        inner = inner.lstrip('\n\r \t')
        return ('<div class="faq-item">\n                        '
                '<h3 class="faq-question-heading" style="margin:0;font-weight:inherit;'
                'font-size:inherit;line-height:inherit;">' + inner + '</h3>')

    new_blk = re.sub(r'<div class="faq-item">(\s*<button class="faq-question".*?</button>)',
                     _item, blk, flags=re.S)
    return raw[:sp[0]] + new_blk + raw[sp[1]:], n


# ------------------------------------------------------------------- JSON-LD
def build_faq_ld(pairs, lang):
    ents = []
    for q, a in pairs:
        ents.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        })
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                       "mainEntity": ents}, ensure_ascii=False, indent=2)


LD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)


def ensure_body_ld(raw, lang):
    """Ensure exactly one FAQPage JSON-LD exists in the BODY, immediately after
    the faq-section's closing tag. Never touches <head>."""
    sp = faq_span(raw)
    if not sp:
        return raw, "no-faq"
    pairs = extract_faq(raw)
    if len(pairs) < 3:
        return raw, "faq<3"
    script = ('\n<script type="application/ld+json">\n' + build_faq_ld(pairs, lang) +
              '\n</script>\n')

    # 1) update an existing body FAQPage in place
    for m in LD_RE.finditer(raw):
        if m.start() < sp[1] and m.start() > raw.find('</head>'):
            if '"FAQPage"' in m.group(1):
                raw = raw[:m.start()] + script.strip() + raw[m.end():]
                return raw, "updated-body"
    # 2) already one right after the FAQ section?
    tail = raw[sp[1]:sp[1] + 80]
    if 'FAQPage' in tail[:200]:
        return raw, "present"
    # 3) insert right after the faq-section closing tag
    return raw[:sp[1]] + script + raw[sp[1]:], "inserted"


# --------------------------------------------------------------------- headings
def h2_list(raw):
    return [(m.group(1), m.start(), m.end(), m.group(2))
            for m in re.finditer(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', raw, re.S)]


def rename_h2(raw, hid, new_text):
    """Rename an <h2 id=...> and keep TOC anchors in sync. Returns (raw, ok)."""
    m = re.search(r'(<h2 id="' + re.escape(hid) + r'"[^>]*>)(.*?)(</h2>)', raw, re.S)
    if not m:
        return raw, False
    raw = raw[:m.start(2)] + new_text + raw[m.end(2):]
    # sync TOC / mobile TOC / any anchor pointing at this id
    def _anchor(mo):
        return mo.group(1) + new_text + mo.group(3)
    raw = re.sub(r'(<a href="#' + re.escape(hid) + r'"[^>]*>)(.*?)(</a>)',
                 _anchor, raw, flags=re.S)
    return raw, True


def rename_h2_text(raw, old_text, new_text):
    """Rename by visible text (first match) + TOC sync."""
    m = re.search(r'(<h2 id="([^"]+)"[^>]*>)' + re.escape(old_text) + r'(</h2>)', raw)
    if not m:
        return raw, False
    return rename_h2(raw, m.group(2), new_text)


# ------------------------------------------------------------------ recommended
def fix_recommended(raw, lang, excerpts=None):
    """Force root-relative language-prefixed hrefs on recommended cards."""
    pref = PREFIX[lang]
    n = 0
    i = raw.find('recommended-grid')
    if i == -1:
        return raw, 0
    j = raw.find('</div>', i)
    seg = raw[i:raw.find('</section>', i)]
    new = seg
    for m in list(re.finditer(r'<a href="([^"]*)" class="recommended-card"', new)):
        h = m.group(1)
        if not h.startswith('/'):
            base = h.split('/')[-1]
            new = new[:m.start(1)] + pref + '/' + base + new[m.end(1):]
            n += 1
    raw = raw.replace(seg, new, 1)
    return raw, n


def fill_excerpts(raw, excerpts):
    """Fill empty <p class="recommended-card-excerpt"></p> in order."""
    out = raw
    idx = [0]

    def _r(mo):
        if idx[0] < len(excerpts) and excerpts[idx[0]]:
            v = excerpts[idx[0]]
            idx[0] += 1
            return '<p class="recommended-card-excerpt">' + v + '</p>'
        idx[0] += 1
        return mo.group(0)
    out = re.sub(r'<p class="recommended-card-excerpt">\s*</p>', _r, out)
    return out, idx[0]


def convert_text_nodes(h, fn):
    """Apply fn to text nodes only; never touches tags, attributes, script or style."""
    out = []
    i = 0
    for m in re.finditer(r'(<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->|<[^>]+>)', h, re.S | re.I):
        out.append(fn(h[i:m.start()]))
        out.append(m.group(0))
        i = m.end()
    out.append(fn(h[i:]))
    return "".join(out)


def sync_zh_tw(slug):
    """Rebuild the zh-TW article body from the zh-CN body (OpenCC s2tw) and
    regenerate the desktop TOC. Head, footer, share buttons and the sections
    outside <article> are untouched."""
    cn = read(slug, LANGS[1][1])
    tw = read(slug, LANGS[2][1])
    cn_body = article_body(cn)
    if not cn_body.strip():
        return None
    new_body = convert_text_nodes(cn_body, s2tw)
    m = ART_RE.search(tw)
    if not m:
        return None
    tw2 = tw[:m.start(1)] + new_body + tw[m.end(1):]
    return rebuild_toc(tw2)


def rebuild_toc(raw, unused=None):
    """Regenerate <nav class="toc-links"> from the body's <h2 id=...> headings."""
    body = article_body(raw)
    hs = [(m.group(1), unescape(strip_tags(m.group(2))).strip())
          for m in re.finditer(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', body, re.S)]
    links = "".join('                    <a href="#%s" class="toc-link">%s</a>\n'
                    % (i, t) for i, t in hs)
    m = re.search(r'(<nav class="toc-links">)(.*?)(</nav>)', raw, re.S)
    if not m:
        return raw
    return raw[:m.start(2)] + "\n" + links + "                " + raw[m.end(2):]


# ------------------------------------------------------------------ content ops
def faq_item_html(i, q, a):
    return (
        '                    <div class="faq-item">\n'
        '                        <h3 class="faq-question-heading" style="margin:0;font-weight:inherit;'
        'font-size:inherit;line-height:inherit;"><button class="faq-question" aria-expanded="false">\n'
        '                            <span class="faq-question-text"><span class="faq-number">%d</span>'
        '<span>%s</span></span>\n'
        '                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>\n'
        '                        </button></h3>\n'
        '                        <div class="faq-answer" role="region"><div class="faq-answer-inner">%s'
        '</div></div>\n'
        '                    </div>\n' % (i, q, a))


def replace_faq(raw, pairs):
    sp = faq_span(raw)
    if not sp:
        return raw, False
    blk = raw[sp[0]:sp[1]]
    m = re.search(r'(<div class="faq-list">\n)(.*?)(\s*</div>\s*</section>)', blk, re.S)
    if not m:
        return raw, False
    items = "".join(faq_item_html(i + 1, q, a) for i, (q, a) in enumerate(pairs))
    new_blk = blk[:m.start(2)] + items + blk[m.end(2):]
    return raw[:sp[0]] + new_blk + raw[sp[1]:], True


FAQ_SECTION_TPL = {
    "EN": ('Frequently Asked Questions', 'Frequently Asked Questions'),
    "zh-CN": ('常见问题', '常见问题'),
    "zh-TW": ('常見問題', '常見問題'),
}


def ensure_faq_section(raw, pairs, lang):
    """Create the faq-section (before the article-nav) if missing."""
    if faq_span(raw):
        return raw, False
    label, title = FAQ_SECTION_TPL[lang]
    items = "".join(faq_item_html(i + 1, q, a) for i, (q, a) in enumerate(pairs))
    sec = (
        '            <section class="faq-section" id="faq" aria-label="%s">\n'
        '                <h2 class="faq-section-title">\n'
        '                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>'
        '<line x1="12" y1="17" x2="12.01" y2="17"/></svg>\n'
        '                    %s\n'
        '                </h2>\n'
        '                <div class="faq-list">\n%s                </div>\n'
        '            </section>\n\n            ' % (label, title, items))
    anchor = raw.find('<nav class="article-nav"')
    if anchor == -1:
        m = ART_RE.search(raw)
        anchor = m.end(1) - len('</article>')
    return raw[:anchor] + sec + raw[anchor:], True


def drop_body_ld(raw):
    """Remove any FAQPage JSON-LD in the BODY (never touches head)."""
    hc = raw.find('</head>')
    out = raw
    for m in reversed(list(LD_RE.finditer(raw))):
        if m.start() > hc and '"FAQPage"' in m.group(1):
            out = out[:m.start()] + out[m.end():]
    return out


def regen_ld(raw, lang):
    raw = drop_body_ld(raw)
    return ensure_body_ld(raw, lang)


def remove_h2_section(raw, hid):
    """Delete an <h2 id=hid> and everything up to the next <h2>/<section>."""
    m = re.search(r'<h2 id="' + re.escape(hid) + r'"[^>]*>.*?</h2>', raw, re.S)
    if not m:
        return raw, False
    nxt = re.search(r'<(h2|section)\b', raw[m.end():])
    end = m.end() + (nxt.start() if nxt else 0)
    raw = raw[:m.start()] + raw[end:]
    # drop matching TOC anchors
    raw = re.sub(r'\s*<a href="#' + re.escape(hid) + r'"[^>]*>.*?</a>', '', raw, flags=re.S)
    return raw, True


def section_html(hid, title, blocks):
    """Build an <h2> + body block. blocks: list of '<p>..</p>' / '<ul>..</ul>' strings."""
    return ('            <h2 id="%s">%s</h2>\n' % (hid, title) +
            "".join("            " + b + "\n" for b in blocks) + "\n")


# ------------------------------------------------------------------------- CTA
def ensure_cta_phrase(raw, lang):
    if PHRASE[lang] in raw:
        return raw, False
    m = re.search(r'(<a href="[^"]*" class="article-cta-btn">)(.*?)(</a>)', raw)
    if not m:
        return raw, False
    return raw[:m.start(2)] + PHRASE[lang] + raw[m.end(2):], True


# --------------------------------------------------------------------- insert
def insert_before_faq(raw, block):
    sp = faq_span(raw)
    if sp:
        return raw[:sp[0]] + block + "\n            " + raw[sp[0]:]
    m = ART_RE.search(raw)
    if m:
        # m.end(1) is already the position of "</article>" (group 1 is the body)
        anchor = m.end(1)
        return raw[:anchor] + block + "\n            " + raw[anchor:]
    return raw


def insert_before_section(raw, block, hid):
    """Insert a block immediately before the <h2 id=hid> section."""
    m = re.search(r'<h2 id="' + re.escape(hid) + r'"', raw)
    if not m:
        return insert_before_faq(raw, block)
    return raw[:m.start()] + block + "\n            " + raw[m.start():]


def add_toc_entries(raw, hid, text):
    """Append TOC anchors for a new section (sidebar + mobile)."""
    link = '<a href="#%s" class="toc-link">%s</a>' % (hid, text)
    mlink = '<a href="#%s" class="toc-mobile-link">%s</a>' % (hid, text)
    toc = re.search(r'(<nav class="toc-links">)(.*?)(</nav>)', raw, re.S)
    if toc and ('#' + hid) not in toc.group(2):
        raw = raw[:toc.end(2)] + "                    " + link + "\n                " + raw[toc.end(2):]
    tm = re.search(r'(<div class="toc-mobile-links">)(.*?)(</div>)', raw, re.S)
    if tm and ('#' + hid) not in tm.group(2):
        raw = raw[:tm.end(2)] + "                    " + mlink + "\n                " + raw[tm.end(2):]
    return raw


def add_toc_before(raw, hid, text, before_hid):
    """Insert TOC anchors immediately before the anchor for before_hid (fallback: append)."""
    link = '<a href="#%s" class="toc-link">%s</a>' % (hid, text)
    mlink = '<a href="#%s" class="toc-mobile-link">%s</a>' % (hid, text)
    for container, cls in (('nav', 'toc-links'), ('div', 'toc-mobile-links')):
        pat = re.compile(r'(<%s class="%s">)(.*?)(</%s>)' % (container, cls, container), re.S)
        m = pat.search(raw)
        if not m or ('#' + hid) in m.group(2):
            continue
        inner = m.group(2)
        lnk = link if cls == 'toc-links' else mlink
        b = re.search(r'<a href="#' + re.escape(before_hid) + r'"[^>]*>.*?</a>', inner, re.S)
        if b:
            new_inner = inner[:b.start()] + lnk + "\n                    " + inner[b.start():]
        else:
            new_inner = inner.rstrip() + "\n                    " + lnk + "\n                "
        raw = raw[:m.start(2)] + new_inner + raw[m.end(2):]
    return raw


TAIL_IDS = ('key-takeaways', 'conclusion', 'key-takeaways-2')


def prose_anchor_id(raw):
    """Id of the first trailing section (takeaways/conclusion) or None -> use FAQ."""
    for hid in TAIL_IDS:
        if re.search(r'<h2 id="' + hid + r'"', raw):
            return hid
    return None


def insert_prose(raw, html, before_hid=None):
    hid = before_hid or prose_anchor_id(raw)
    if hid:
        return insert_before_section(raw, html, hid)
    return insert_before_faq(raw, html)


def guard_ok(raw, before):
    """Verify hard guardrails survived an edit."""
    probs = []
    if '/css/article.css?v=20260826' not in raw and '/css/article.css?v=20260826' in before:
        probs.append('css-version')
    if '/js/article.js?v=20260826' not in raw and '/js/article.js?v=20260826' in before:
        probs.append('js-version')
    bh = before[:before.find('</head>')]
    ah = raw[:raw.find('</head>')]
    if bh != ah:
        probs.append('head-changed')
    return probs
