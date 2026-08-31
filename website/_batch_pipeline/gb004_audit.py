#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit gbatch_004 slugs against the GEO/SEO standard."""
import re, os, sys, json, html

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
LANGS = [("en", ""), ("zh-CN", "zh-cn/"), ("zh-TW", "zh-tw/")]

CJK = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]')

def strip_tags(s):
    s = re.sub(r'<script[^>]*>.*?</script>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<style[^>]*>.*?</style>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<!--.*?-->', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    return html.unescape(s)

def words(s):
    return len(re.findall(r"[A-Za-z][A-Za-z'\-]*", s))

def cjk(s):
    return len(CJK.findall(s))

def article_inner(path):
    src = open(path, encoding='utf-8').read()
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', src, re.S)
    if not m:
        m = re.search(r'<article[^>]*>(.*?)</article>', src, re.S)
    return src, (m.group(1) if m else '')

def audit(slug):
    row = {"slug": slug}
    for lang, pre in LANGS:
        p = os.path.join(ROOT, pre + "blog/articles/" + slug + ".html")
        if not os.path.exists(p):
            row[lang] = {"missing": True}
            continue
        src, inner = article_inner(p)
        txt = strip_tags(inner)
        w = words(txt); c = cjk(txt)
        h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', inner, re.S)
        h2s = [re.sub(r'<[^>]+>', '', x).strip() for x in h2s]
        faq_m = re.search(r'class="faq-section"', inner)
        # FAQ section block
        faq_h3 = 0
        if faq_m:
            start = faq_m.start()
            nxt = re.search(r'</section>', inner[start:])
            blk = inner[start:start + nxt.end()] if nxt else inner[start:]
            faq_h3 = len(re.findall(r'<h3[^>]*>', blk))
        # counts in whole body
        lds = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', src, re.S)
        ld_body = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', inner, re.S)
        faq_ld_body = any('FAQPage' in x for x in ld_body)
        faq_ld_head = any('FAQPage' in x for x in lds if x not in ld_body)
        cta = re.findall(r'class="article-cta-btn"[^>]*>(.*?)</a>', inner, re.S)
        cta_txt = [re.sub(r'<[^>]+>', '', x).strip() for x in cta]
        undef = src.count('undefined')
        # recommended cards
        cards = re.findall(r'<a\s+class="recommended-card"[^>]*href="([^"]*)"', src)
        empty_ex = inner.count('recommended-card-excerpt')
        row[lang] = {
            "words": w, "cjk": c, "h2": len(h2s),
            "h2_q": sum(1 for x in h2s if x.endswith('?') or x.endswith('？') or x.endswith('?')),
            "faq_wrap": bool(faq_m), "faq_h3": faq_h3,
            "ld_body": faq_ld_body, "ld_head": faq_ld_head,
            "ld_count_body": len(ld_body),
            "cta": cta_txt, "undef": undef,
            "cards": len(cards), "bad_cards": [c for c in cards if not c.startswith('/')],
            "bytes": len(src),
        }
    return row

if __name__ == "__main__":
    slugs = [s.strip() for s in open(os.path.join(ROOT, "_batch_pipeline/gap_batches/gbatch_004.txt")) if s.strip()]
    if len(sys.argv) > 1:
        slugs = sys.argv[1:]
    out = [audit(s) for s in slugs]
    for r in out:
        print("=" * 90)
        print(r["slug"])
        for lang, _ in LANGS:
            d = r.get(lang, {})
            if d.get("missing"):
                print(f"  {lang:6s} MISSING")
                continue
            print(f"  {lang:6s} w={d['words']:5d} cjk={d['cjk']:5d} h2={d['h2']:2d}/q{d['h2_q']:2d} "
                  f"faqwrap={int(d['faq_wrap'])} h3={d['faq_h3']} ld_body={int(d['ld_body'])}x{d['ld_count_body']} "
                  f"ld_head={int(d['ld_head'])} undef={d['undef']} cards={d['cards']}{d['bad_cards']} cta={d['cta']}")
