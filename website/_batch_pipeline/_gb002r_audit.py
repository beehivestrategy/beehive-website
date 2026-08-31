#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit gbatch_002 files against the GEO/SEO standard."""
import json
import os
import re
import sys

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
SLUGS = [l.strip() for l in open(os.path.join(ROOT, "_batch_pipeline/gap_batches/gbatch_002.txt")) if l.strip()]

LANGS = [
    ("EN", "blog/articles/%s.html"),
    ("zh-CN", "zh-cn/blog/articles/%s.html"),
    ("zh-TW", "zh-tw/blog/articles/%s.html"),
]

CJK = re.compile(r'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\u3040-\u30ff]')
WORD = re.compile(r"[A-Za-z][A-Za-z'\-]*")


def strip_tags(h):
    h = re.sub(r'<script\b.*?</script>', ' ', h, flags=re.S | re.I)
    h = re.sub(r'<style\b.*?</style>', ' ', h, flags=re.S | re.I)
    h = re.sub(r'<!--.*?-->', ' ', h, flags=re.S)
    return re.sub(r'<[^>]+>', ' ', h)


def article_html(h):
    m = re.search(r'(<article\b[^>]*id=["\']article-content["\'][^>]*>)(.*?)(</article>)', h, re.S | re.I)
    if m:
        return m.group(2), (m.start(2), m.end(2))
    return "", None


def body_html(h):
    m = re.search(r'<body[^>]*>(.*?)</body>', h, re.S | re.I)
    return m.group(1) if m else h


def metrics(path):
    if not os.path.exists(path):
        return {"exists": False}
    h = open(path, encoding="utf-8").read()
    art, span = article_html(h)
    scope = art if art else body_html(h)
    txt = strip_tags(scope)
    words = len(WORD.findall(txt))
    cjk = len(CJK.findall(txt))
    # FAQ
    faq_m = re.search(r'<div[^>]*class=["\'][^"\']*faq-section[^"\']*["\'][^>]*>', scope, re.I)
    faq = 0
    if faq_m:
        # find matching close by scanning simple: take next 40000 chars and count h3
        seg = scope[faq_m.end():faq_m.end() + 60000]
        faq = len(re.findall(r'<h3[^>]*>', seg, re.I))
    # JSON-LD
    b = body_html(h)
    lds = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', b, re.S | re.I)
    n_ld = len(lds)
    faq_ld = 0
    ld_ok = False
    for s in lds:
        try:
            d = json.loads(s.strip())
        except Exception:
            continue
        items = d.get("mainEntity") if isinstance(d, dict) else None
        if isinstance(d, dict) and d.get("@type") == "FAQPage":
            faq_ld = len(items or [])
            ld_ok = True
    # CTA
    cta = 'article-cta-btn' in b
    phrase = {"EN": "Book a Demo", "zh-CN": "预约演示", "zh-TW": "預約示範"}
    # H2s
    h2s = [re.sub(r'<[^>]+>', '', x).strip() for x in re.findall(r'<h2[^>]*>(.*?)</h2>', scope, re.S | re.I)]
    return {
        "exists": True, "words": words, "cjk": cjk, "faq": faq,
        "n_ld": n_ld, "faq_ld": faq_ld, "ld_ok": ld_ok,
        "cta": cta, "h2": h2s, "has_faq_wrap": bool(faq_m),
        "undefined": len(re.findall(r'\bundefined\b', txt)),
    }


out = {}
for slug in SLUGS:
    row = {}
    for lang, pat in LANGS:
        row[lang] = metrics(os.path.join(ROOT, pat % slug))
        row[lang]["path"] = pat % slug
    out[slug] = row

if __name__ == "__main__":
    for slug, row in out.items():
        print("=" * 100)
        print(slug)
        for lang, pat in LANGS:
            m = row[lang]
            if not m.get("exists"):
                print(f"  {lang:5s} MISSING")
                continue
            print(f"  {lang:5s} w={m['words']:5d} cjk={m['cjk']:5d} faq={m['faq']} ld={m['n_ld']}(faqQ={m['faq_ld']},ok={m['ld_ok']}) cta={m['cta']} und={m['undefined']} h2={len(m['h2'])}")
            if "-v" in sys.argv:
                for x in m["h2"]:
                    print("        H2:", x[:110])
