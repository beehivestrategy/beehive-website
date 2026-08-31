#!/usr/bin/env python3
# gap-measure: measure article body metrics for gbatch_001 slugs
import re, os, sys, json

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"

def body_of(html):
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', html, re.S)
    if m:
        return m.group(1)
    m = re.search(r'<article[^>]*>(.*?)</article>', html, re.S)
    if m:
        return m.group(1)
    return ""

def text_of(frag):
    frag = re.sub(r'<script.*?</script>', ' ', frag, flags=re.S)
    frag = re.sub(r'<style.*?</style>', ' ', frag, flags=re.S)
    frag = re.sub(r'<[^>]+>', ' ', frag)
    frag = re.sub(r'&nbsp;', ' ', frag)
    frag = re.sub(r'&amp;', '&', frag)
    frag = re.sub(r'&#\d+;', ' ', frag)
    return frag

def en_words(t):
    return len(re.findall(r"[A-Za-z][A-Za-z'’\-]*", t))

def cjk(t):
    return len(re.findall(r'[\u4e00-\u9fff]', t))

def title_of(html):
    m = re.search(r'<title>(.*?)</title>', html, re.S)
    return (m.group(1).strip() if m else "")

def h1_of(html):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    return re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else ""

def faq_count(html):
    m = re.search(r'class="faq-section"(.*?)(?:</section>|</div>\s*</div>\s*</div>)', html, re.S)
    frag = m.group(1) if m else ""
    return len(re.findall(r'<h3[^>]*>', frag))

def ld_count(html):
    return len(re.findall(r'"@type"\s*:\s*"FAQPage"', html))

def cta_ok(html, lang):
    phrase = {"en": "Book a Demo", "cn": "预约演示", "tw": "預約示範"}[lang]
    return ('class="article-cta-btn"' in html) and (phrase in html)

def h2s(html):
    body = body_of(html)
    return re.findall(r'<h2[^>]*>(.*?)</h2>', body, re.S)

slugs = [l.strip() for l in open(os.path.join(ROOT, "_batch_pipeline/gap_batches/gbatch_001.txt")) if l.strip()]
rows = []
for s in slugs:
    for lang, path in (("en", f"blog/articles/{s}.html"),
                       ("cn", f"zh-cn/blog/articles/{s}.html"),
                       ("tw", f"zh-tw/blog/articles/{s}.html")):
        fp = os.path.join(ROOT, path)
        if not os.path.exists(fp):
            rows.append((s, lang, "MISSING", 0, 0, 0, 0, False))
            continue
        h = open(fp, encoding="utf-8").read()
        b = body_of(h)
        t = text_of(b)
        rows.append((s, lang, cjk(t) if lang != "en" else en_words(t),
                     faq_count(h), ld_count(h), len(h2s(h)),
                     sum(1 for x in h2s(h) if ('?' in x or '？' in x)),
                     cta_ok(h, lang)))
for r in rows:
    print(f"{r[0][:52]:54s} {r[1]:2s} metric={r[2]:5d} faq={r[3]} ld={r[4]} h2={r[5]} qh2={r[6]} cta={int(r[7])}")
