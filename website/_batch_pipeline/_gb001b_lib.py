#!/usr/bin/env python3
"""Shared helpers for gbatch_001 content expansion.

Usage: write a spec JSON with ops and run:
    python3 _batch_pipeline/_gb001b_lib.py spec.json

spec = {
  "slug": "...",
  "ops": [
     {"file":"cn", "anchor":"<exact string in zh-cn file>", "pos":"before",
      "block":"<html to insert>"},
     {"file":"tw", "anchor":"<exact string in zh-tw file>", "pos":"before",
      "block":"<html to insert>", "from_cn": true}   # from_cn -> OpenCC s2t
  ]
}
For zh-TW ops, set "block_cn" to Simplified source and it will be converted s2t;
or set "block" directly if already Traditional.
"""
import re, os, sys, json
from opencc import OpenCC

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
_cc = None
def s2t(t):
    global _cc
    if _cc is None: _cc = OpenCC('s2t')
    return _cc.convert(t)

# OpenCC s2t over-conversions that are objectively wrong in zh-TW business prose.
# Applied only to text we newly insert (never rewrites existing page content).
POST_FIX = {
    "隻有": "只有",   # 只(zhǐ) -> 隻 is a measure-word error
    "籤核": "簽核",   # 簽核 (sign-off), not 籤 (bamboo slip)
    "是隻": "是只",
}
def s2t_fixed(t):
    t = s2t(t)
    for a, b in POST_FIX.items():
        t = t.replace(a, b)
    return t

PATHS = {"en": "blog/articles/%s.html",
         "cn": "zh-cn/blog/articles/%s.html",
         "tw": "zh-tw/blog/articles/%s.html"}

def path_of(slug, f):
    return os.path.join(ROOT, PATHS[f] % slug)

def ins(path, anchor, block, pos="before"):
    h = open(path, encoding="utf-8").read()
    n = h.count(anchor)
    if n != 1:
        raise SystemExit(f"ANCHOR COUNT {n} (need 1) in {path}:\n  {anchor[:120]!r}")
    if pos == "before":
        out = h.replace(anchor, block + anchor, 1)
    else:
        out = h.replace(anchor, anchor + block, 1)
    open(path, "w", encoding="utf-8").write(out)
    return True

FAQ_LABEL = {"en": "Frequently Asked Questions", "cn": "常见问题", "tw": "常見問題"}
CHEVRON = ('<svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
           'stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>')
TITLE_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
              '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>'
              '<line x1="12" y1="17" x2="12.01" y2="17"/></svg>')

def build_faq(pairs, lang):
    """pairs: list of (question, answer). Produces the site's canonical FAQ markup."""
    items = []
    for i, (q, a) in enumerate(pairs, 1):
        items.append(
            '                    <div class="faq-item">\n'
            '                        <h3 class="faq-question" aria-expanded="false">\n'
            f'                            <span class="faq-question-text"><span class="faq-number">{i}</span><span>{q}</span></span>\n'
            f'                            {CHEVRON}\n'
            '                        </h3>\n'
            f'                        <div class="faq-answer" role="region"><div class="faq-answer-inner">{a}</div></div>\n'
            '                    </div>')
    return ('            <section class="faq-section" id="faq" aria-label="' + FAQ_LABEL[lang] + '">\n'
            '                <h2 class="faq-section-title">\n'
            f'                    {TITLE_ICON}\n'
            f'                    {FAQ_LABEL[lang]}\n'
            '                </h2>\n'
            '                <div class="faq-list">\n'
            + "\n".join(items) + "\n"
            '                </div>\n'
            '            </section>\n')

def retitle_by_text(path, old_text, new_text, which=0):
    """Rename an <h2> by its visible text (id auto-detected).
    `which` selects the nth occurrence when the same text appears more than once."""
    h = open(path, encoding="utf-8").read()
    pat = re.compile(r'(<h2 id="[^"]*">)' + re.escape(old_text) + r'(</h2>)')
    ms = list(pat.finditer(h))
    if not ms:
        raise SystemExit(f"H2 text not found: {old_text[:70]!r} in {path}")
    if which >= len(ms):
        raise SystemExit(f"H2 occurrence {which} not found for {old_text[:70]!r} in {path}")
    # apply from last to first so offsets stay valid when several share the text
    if old_text == new_text:
        return True
    m = ms[which]
    h = h[:m.start()] + m.group(1) + new_text + m.group(2) + h[m.end():]
    for cls in ("toc-mobile-link", "toc-link"):
        p2 = 'class="%s">%s</a>' % (cls, old_text)
        if h.count(p2) == 1:
            h = h.replace(p2, 'class="%s">%s</a>' % (cls, new_text))
        else:
            # TOC labels may be HTML-entity escaped (e.g. &#x27; for ')
            eo = old_text.replace("'", "&#x27;").replace("&", "&amp;")
            en_ = new_text.replace("'", "&#x27;").replace("&", "&amp;")
            p3 = 'class="%s">%s</a>' % (cls, eo)
            if h.count(p3) == 1:
                h = h.replace(p3, 'class="%s">%s</a>' % (cls, en_))
    open(path, "w", encoding="utf-8").write(h)
    return True

def retitle_h2(path, h2_id, old_text, new_text):
    """Rename an <h2 id=...> visible text, keeping the id (so TOC anchors still
    resolve) and updating the matching TOC link labels."""
    h = open(path, encoding="utf-8").read()
    pat = '<h2 id="%s">%s</h2>' % (h2_id, old_text)
    n = h.count(pat)
    if n != 1:
        raise SystemExit(f"H2 COUNT {n} (need 1) id={h2_id} old={old_text[:60]!r} in {path}")
    h = h.replace(pat, '<h2 id="%s">%s</h2>' % (h2_id, new_text))
    for cls in ("toc-mobile-link", "toc-link"):
        p2 = 'class="%s">%s</a>' % (cls, old_text)
        if h.count(p2) == 1:
            h = h.replace(p2, 'class="%s">%s</a>' % (cls, new_text))
    open(path, "w", encoding="utf-8").write(h)
    return True

def replace_once(path, old, new):
    h = open(path, encoding="utf-8").read()
    n = h.count(old)
    if n != 1:
        raise SystemExit(f"REPLACE COUNT {n} (need 1) in {path}:\n  {old[:120]!r}")
    open(path, "w", encoding="utf-8").write(h.replace(old, new, 1))
    return True

def run(spec):
    slug = spec["slug"]
    for i, op in enumerate(spec["ops"]):
        f = op["file"]
        p = path_of(slug, f)
        if "block_cn" in op:
            blk = s2t_fixed(op["block_cn"]) if f == "tw" else op["block_cn"]
        else:
            blk = op["block"]
        if op.get("mode") == "replace":
            old = op["old"] if f != "tw" or "old_cn" not in op else s2t(op["old_cn"])
            new = blk
            replace_once(p, old, new)
        else:
            ins(p, op["anchor"] if f != "tw" or "anchor_cn" not in op else s2t(op["anchor_cn"]),
                blk, op.get("pos", "before"))
    print(f"applied {len(spec['ops'])} ops -> {slug}")

def metrics(slug):
    out = {}
    for f in ("en", "cn", "tw"):
        p = path_of(slug, f)
        h = open(p, encoding="utf-8").read()
        m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', h, re.S)
        b = m.group(1) if m else ""
        i = b.find('<section class="faq-section"')
        if i < 0: i = b.find('<section class="faq-section"')
        seg = b[:i] if i >= 0 else b
        seg = re.sub(r'<script.*?</script>', ' ', seg, flags=re.S)
        seg = re.sub(r'<[^>]+>', ' ', seg)
        if f == "en":
            out[f] = len(re.findall(r"[A-Za-z][A-Za-z'’\-]*", seg))
        else:
            out[f] = len(re.findall(r'[\u4e00-\u9fff]', seg))
    return out

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    before = metrics(spec["slug"])
    run(spec)
    after = metrics(spec["slug"])
    print(f"  EN {before['en']} -> {after['en']} | CN {before['cn']} -> {after['cn']} | TW {before['tw']} -> {after['tw']}")
