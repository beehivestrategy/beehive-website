# -*- coding: utf-8 -*-
"""gb004x_run.py <module_name> ...

Imports EN / ZH specs from gb004c/<module>.py and applies them in place.

Spec shape (per language):
{
  "retitle":   {h2_id: "Question-style H2?"},   # optional
  "drop":      [h2_id, ...],                    # optional, drop heading only
  "drop_sec":  [h2_id, ...],                    # optional, drop heading + body
  "sections":  [(id, "Question H2?", "<p>…</p>")],   # new prose, inserted
  "before":    "__AUTO__" | "__FAQ__" | "__NAV__" | "<h2 id>",
  "faq":       [("Q?", "A"), ...],              # >= 3
  "faq_title": "Frequently Asked Questions",
}
"""
import importlib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gb004x_lib as L
import opencc

CC = opencc.OpenCC("s2twp")


def paths(slug):
    return {
        "en": os.path.join(L.ROOT, "blog/articles", slug + ".html"),
        "zh-cn": os.path.join(L.ROOT, "zh-cn/blog/articles", slug + ".html"),
        "zh-tw": os.path.join(L.ROOT, "zh-tw/blog/articles", slug + ".html"),
    }


def apply_spec(h, spec, lang):
    h = L.repair_text(h)
    for sid in spec.get("drop_sec", []):
        h = L.drop_h2_section(h, [sid])
    if spec.get("retitle"):
        h = L.retitle_h2(h, spec["retitle"])
    if spec.get("drop"):
        h = L.drop_h2(h, spec["drop"])
    h = L.insert_sections(h, spec.get("sections", []), spec.get("before", "__AUTO__"))
    h = L.set_faq(h, spec["faq"], spec.get("faq_title", "Frequently Asked Questions"))
    h = L.ensure_ld(h, spec["faq"])
    h = L.rebuild_toc(h)
    h = L.fix_links(h, "" if lang == "en" else lang + "/")
    h = L.fill_cards(h, lang)
    h = L.fix_cta(h, lang)
    return h


def build_tw(cn_html, tw_html):
    """Rebuild the zh-TW content regions from the (already fixed) zh-CN file."""
    out = tw_html

    def grab(html, pattern):
        m = re.search(pattern, html, re.S)
        return m.group(0) if m else None

    def swap(html, pattern, new):
        m = re.search(pattern, html, re.S)
        if not m or new is None:
            return html
        return html[:m.start()] + new + html[m.end():]

    # 1. article inner
    cn_art = grab(cn_html, r'(?<=<article\b)[^>]*>.*?(?=</article>)')
    cn_art = "<article" + cn_art if cn_art else None
    if cn_art:
        inner = re.sub(r'^[^>]*>', '', cn_art, count=1)
        out = swap(out, r'(?<=<article\b)[^>]*>.*?(?=</article>)',
                   re.search(r'<article\b[^>]*>', out).group(0)[8:] + CC.convert(inner))

    # 2. recommended section + cta section
    for pat in [r'<section class="recommended-section".*?</section>',
                r'<section class="article-cta".*?</section>']:
        out = swap(out, pat, CC.convert(grab(cn_html, pat)))

    # 3. sidebar text blocks (share buttons untouched)
    for pat in [r'(?<=<div class="sidebar-heading">).*?(?=</div>)',
                r'(?<=<div class="sidebar-tags">).*?(?=</div>)',
                r'(?<=<div class="sidebar-related-list">).*?(?=</div>\s*</div>)']:
        out = swap(out, pat, CC.convert(grab(cn_html, pat)))
    return out


def run(slug, mod):
    P = paths(slug)
    for p in P.values():
        L.backup(p)
    before = {}

    # EN
    h = L.read(P["en"])
    before["en"] = L.metrics(h)[0]
    h = apply_spec(h, mod.EN, "en")
    L.write(P["en"], h)

    # zh-CN
    h = L.read(P["zh-cn"])
    before["zh-cn"] = L.metrics(h)[1]
    h = apply_spec(h, mod.ZH, "zh-cn")
    L.write(P["zh-cn"], h)

    # zh-TW derived from zh-CN
    htw = L.read(P["zh-tw"])
    before["zh-tw"] = L.metrics(htw)[1]
    htw = build_tw(L.read(P["zh-cn"]), htw)
    htw = L.rebuild_toc(htw)
    htw = L.fix_links(htw, "zh-tw/")
    htw = L.fill_cards(htw, "zh-tw")
    htw = L.fix_cta(htw, "zh-tw")
    L.write(P["zh-tw"], htw)

    after = {}
    for lang, p in P.items():
        hh = L.read(p)
        w, c = L.metrics(hh)
        after[lang] = w if lang == "en" else c
    n = len(mod.EN["faq"])
    print("%-62s EN %5d->%5d | zhCN %5d->%5d | zhTW %5d->%5d | faq=%d"
          % (slug, before["en"], after["en"], before["zh-cn"], after["zh-cn"],
             before["zh-tw"], after["zh-tw"], n))


if __name__ == "__main__":
    for name in sys.argv[1:]:
        mod = importlib.import_module("gb004c." + name)
        run(mod.SLUG, mod)
