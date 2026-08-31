#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gb004_lib.py — build harness for gbatch_004 rewrites.

render_inner(): builds the full <article> inner HTML (no article tags) from a
content dict, including toc-mobile, lead, question-style H2 sections, takeaways,
conclusion, faq-section (>=3 <h3>), a FAQPage JSON-LD placed immediately after
the faq-section closing tag, and the article-nav (preserved markup).

build(): renders EN + zh-CN, derives zh-TW via OpenCC s2twp, splices all three
real article files via rewrite_lib.splice, then reports length/FAQ/JSON-LD.

Content dict shape (per language):
{
  "lead": "...",
  "sections": [ ("h2_id", "Question H2 text?", "html body"), ... ],
  "takeaways_id": "key-takeaways",
  "takeaways_h2": "What Are the Key Takeaways?",
  "takeaways": ["point", ...],          # rendered as <ul><li><strong>..</strong>..</li>
  "conclusion_id": "conclusion",
  "conclusion_h2": "What Should You Take Away?",
  "conclusion": "html body",
  "faq": [ ("Question?", "Answer plain text"), ... ],   # >=3
  "faq_h2": "Frequently Asked Questions",
}
"""
import re, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rewrite_lib as R
import opencc

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
CC = opencc.OpenCC("s2twp")

NAV = """            <nav class="article-nav" aria-label="Article navigation">
                <a href="https://www.beehivestrategy.com/blog" class="btn-back-to-blog">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><polyline points="15 18 9 12 15 6"/></svg>
                    Back to All Articles
                </a>
            </nav>"""


def _esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _faq_ld(faq):
    me = [{"@type": "Question",
           "name": q,
           "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]
    obj = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": me}
    return json.dumps(obj, ensure_ascii=False)


def render_inner(d):
    out = []
    # toc-mobile
    out.append('            <div class="toc-mobile" id="toc-mobile">')
    out.append('                <button class="toc-mobile-toggle" aria-expanded="false">Table of Contents <svg class="toc-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></button>')
    out.append('                <div class="toc-mobile-links">')
    for sid, stext, _ in d["sections"]:
        out.append(f'                    <a href="#{sid}" class="toc-mobile-link">{stext}</a>')
    out.append(f'                    <a href="#{d["takeaways_id"]}" class="toc-mobile-link">{d["takeaways_h2"]}</a>')
    out.append(f'                    <a href="#{d["conclusion_id"]}" class="toc-mobile-link">{d["conclusion_h2"]}</a>')
    out.append('                </div>')
    out.append('            </div>')
    # lead
    out.append(f'<p class="article-lead"><strong>{d["lead"]}</strong></p>')
    # sections
    for sid, stext, body in d["sections"]:
        out.append(f'<h2 id="{sid}">{stext}</h2>')
        out.append(body)
    # takeaways
    out.append(f'<h2 id="{d["takeaways_id"]}">{d["takeaways_h2"]}</h2>')
    out.append(f'<p>{d.get("takeaways_intro","The pattern is clearer when it is reduced to its load-bearing points.")}</p>')
    out.append('<ul>')
    for t in d["takeaways"]:
        out.append(f'<li>{t}</li>')
    out.append('</ul>')
    # conclusion
    out.append(f'<h2 id="{d["conclusion_id"]}">{d["conclusion_h2"]}</h2>')
    out.append(d["conclusion"])
    # faq-section
    out.append('<section class="faq-section" id="faq">')
    out.append(f'<h2 class="faq-title">{d["faq_h2"]}</h2>')
    out.append('<div class="faq-list">')
    for q, a in d["faq"]:
        out.append('<div class="faq-item">')
        out.append(f'<h3>{q}</h3>')
        out.append(f'<div class="faq-answer"><p>{a}</p></div>')
        out.append('</div>')
    out.append('</div>')
    out.append('</section>')
    # FAQPage JSON-LD immediately after faq-section
    out.append(f'<script type="application/ld+json">{_faq_ld(d["faq"])}</script>')
    # nav
    out.append(NAV)
    return "\n".join(out)


def _faq_block(faq_h2, faq):
    out = ['<section class="faq-section" id="faq">',
           f'<h2 class="faq-title">{faq_h2}</h2>',
           '<div class="faq-list">']
    for q, a in faq:
        out.append('<div class="faq-item">')
        out.append(f'<h3>{q}</h3>')
        out.append(f'<div class="faq-answer"><p>{a}</p></div>')
        out.append('</div>')
    out.append('</div>')
    out.append('</section>')
    out.append(f'<script type="application/ld+json">{_faq_ld(faq)}</script>')
    return "\n".join(out)


def _article_inner(path):
    h = open(path, encoding="utf-8").read()
    a = re.search(r'<article\b[^>]*>', h)
    e = h.rfind('</article>')
    return h, a, e


def patch_zh(slug, h2_map, faq, faq_h2="常见问题", paths=None, regen_tw=True):
    """Patch an already-length-compliant zh-CN article: convert listed H2 ids to
    question text and append a faq-section + FAQPage JSON-LD (idempotent). Then
    regenerate zh-TW from the patched zh-CN via OpenCC."""
    if paths is None:
        paths = {
            "zh-cn": os.path.join(ROOT, "zh-cn/blog/articles", slug + ".html"),
            "zh-tw": os.path.join(ROOT, "zh-tw/blog/articles", slug + ".html"),
        }
    h, a, e = _article_inner(paths["zh-cn"])
    inner = h[a.end():e]
    if "faq-section" in inner:
        pass  # already patched; still regenerate tw below if requested
    else:
        for hid, q in h2_map.items():
            inner = re.sub(r'(<h2 id="' + re.escape(hid) + r'">).*?(</h2>)',
                           lambda m: m.group(1) + q + m.group(2), inner,
                           flags=re.S, count=1)
        inner = inner.rstrip() + "\n" + _faq_block(faq_h2, faq) + "\n"
        R.splice(paths["zh-cn"], inner)
    if regen_tw:
        h2, a2, e2 = _article_inner(paths["zh-tw"])
        inner_tw = h2[a2.end():e2]
        # convert H2 question texts and append faq (idempotent)
        if "faq-section" not in inner_tw:
            for hid, q in h2_map.items():
                qt = CC.convert(q)
                inner_tw = re.sub(r'(<h2 id="' + re.escape(hid) + r'">).*?(</h2>)',
                                  lambda m: m.group(1) + qt + m.group(2), inner_tw,
                                  flags=re.S, count=1)
            inner_tw = inner_tw.rstrip() + "\n" + CC.convert(_faq_block(faq_h2, faq)) + "\n"
        R.splice(paths["zh-tw"], inner_tw)
    cjk = R._count_zh(open(paths["zh-cn"], encoding="utf-8").read()[a.end():e])
    twcjk = R._count_zh(open(paths["zh-tw"], encoding="utf-8").read()[a2.end():e2])
    return {"slug": slug, "patch": "zh", "zh_cjk": cjk, "tw_cjk": twcjk,
            "faq": len(faq), "jsonld": "y"}


def patch_lang(path, h2_map, faq, faq_h2="常见问题"):
    """Patch one zh file in place: convert listed H2 ids to question text (keeping
    ids/anchors) and replace any existing faq-section with the standard <h3>
    faq-section + a BODY FAQPage JSON-LD immediately after it. Idempotent: if no
    faq-section exists, append before the article-nav. Returns CJK count of inner.
    h2_map values: a string replaces the H2 text; None means append '？' to existing."""
    h, a, e = _article_inner(path)
    inner = h[a.end():e]
    for hid, q in h2_map.items():
        inner = re.sub(r'(<h2 id="' + re.escape(hid) + r'">)(.*?)(</h2>)',
                       lambda m: m.group(1) + (q if q is not None else m.group(2) + '？') + m.group(3),
                       inner, flags=re.S, count=1)
    block = _faq_block(faq_h2, faq)
    m = re.search(r'<section class="faq-section" id="faq".*?</section>', inner, re.S)
    if m:
        inner = inner[:m.start()] + block + inner[m.end():]
    else:
        navm = re.search(r'<nav class="article-nav"', inner)
        if navm:
            inner = inner[:navm.start()] + block + "\n" + inner[navm.start():]
        else:
            inner = inner.rstrip() + "\n" + block + "\n"
    R.splice(path, inner)
    # recompute CJK on the freshly spliced file
    h2 = open(path, encoding="utf-8").read()
    a2 = re.search(r'<article\b[^>]*>', h2)
    e2 = h2.rfind('</article>')
    return R._count_zh(h2[a2.end():e2])


def process_patch(slug, EN, zh_faq, h2_cn, h2_tw, paths=None):
    """EN: full rewrite via render_inner. zh-CN / zh-TW: patch (convert H2s to
    questions, replace faq-section with standard <h3> + body JSON-LD), preserving
    existing prose and ids. Returns report dict."""
    if paths is None:
        paths = {
            "en": os.path.join(ROOT, "blog/articles", slug + ".html"),
            "zh-cn": os.path.join(ROOT, "zh-cn/blog/articles", slug + ".html"),
            "zh-tw": os.path.join(ROOT, "zh-tw/blog/articles", slug + ".html"),
        }
    en_inner = render_inner(EN)
    R.splice(paths["en"], en_inner)
    en_w = R._count_en(en_inner)
    zh_cjk = patch_lang(paths["zh-cn"], h2_cn, zh_faq, "常见问题")
    tw_faq = [(CC.convert(q), CC.convert(a)) for q, a in zh_faq]
    tw_cjk = patch_lang(paths["zh-tw"], h2_tw, tw_faq, "常見問題")
    return {"slug": slug, "en_words": en_w, "zh_cjk": zh_cjk, "tw_cjk": tw_cjk,
            "faq": len(EN["faq"]), "jsonld": "y",
            "en_ok": en_w >= 2500, "zh_ok": zh_cjk >= 3500 and tw_cjk >= 3500,
            "faq_ok": len(EN["faq"]) >= 3}


def build(slug, EN, ZH, paths=None):
    if paths is None:
        paths = {
            "en": os.path.join(ROOT, "blog/articles", slug + ".html"),
            "zh-cn": os.path.join(ROOT, "zh-cn/blog/articles", slug + ".html"),
            "zh-tw": os.path.join(ROOT, "zh-tw/blog/articles", slug + ".html"),
        }
    en_inner = render_inner(EN)
    zhcn_inner = render_inner(ZH)
    zhtw_inner = CC.convert(zhcn_inner)

    R.splice(paths["en"], en_inner)
    R.splice(paths["zh-cn"], zhcn_inner)
    R.splice(paths["zh-tw"], zhtw_inner)

    # report
    en_w = R._count_en(en_inner)
    zh_cjk = R._count_zh(zhcn_inner)
    tw_cjk = R._count_zh(zhtw_inner)
    faq_n = len(EN["faq"])
    rep = {
        "slug": slug,
        "en_words": en_w,
        "zh_cjk": zh_cjk,
        "tw_cjk": tw_cjk,
        "faq": faq_n,
        "jsonld": "y",
        "en_ok": en_w >= 2500,
        "zh_ok": zh_cjk >= 3500 and tw_cjk >= 3500,
        "faq_ok": faq_n >= 3,
    }
    return rep


if __name__ == "__main__":
    print("gb004_lib harness loaded")
