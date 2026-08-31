#!/usr/bin/env python3
import re, os, json, sys

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"

def body(html):
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', html, re.S)
    return m.group(1) if m else ""

def strip_tags(s):
    s = re.sub(r'<script.*?</script>', ' ', s, flags=re.S)
    s = re.sub(r'<style.*?</style>', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'&[a-zA-Z#0-9]+;', ' ', s)
    return s

def en_words(s):
    return len(re.findall(r"[A-Za-z][A-Za-z'\-]*", s))

def cjk(s):
    return len(re.findall(r'[\u4e00-\u9fff]', s))

def h1(html):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    return re.sub(r'\s+', ' ', strip_tags(m.group(1))).strip() if m else "(none)"

def title(html):
    m = re.search(r'<title>(.*?)</title>', html, re.S)
    return re.sub(r'\s+', ' ', m.group(1)).strip() if m else "(none)"

def faq_count(html):
    m = re.search(r'class="faq-section"', html)
    if not m: return 0
    # count h3 within faq-section region (from match to end of that section-ish)
    seg = html[m.start():]
    # cut at recommended or cta
    for stop in ['class="recommended', 'article-cta', '</article>']:
        i = seg.find(stop)
        if i > 0:
            seg = seg[:i]
    return len(re.findall(r'<h3', seg))

def faqld(html):
    return len(re.findall(r'"@type"\s*:\s*"FAQPage"', html))

slugs = [l.strip() for l in open(os.path.join(ROOT, "_batch_pipeline/lite_chunks/chunk_03.txt")) if l.strip()]
only = sys.argv[1:] if len(sys.argv) > 1 else None
if only: slugs = only

for s in slugs:
    print("=" * 100)
    print("SLUG:", s)
    for lang, path in (("EN", f"blog/articles/{s}.html"),
                       ("CN", f"zh-cn/blog/articles/{s}.html"),
                       ("TW", f"zh-tw/blog/articles/{s}.html")):
        fp = os.path.join(ROOT, path)
        if not os.path.exists(fp):
            print(f"  {lang}: MISSING")
            continue
        h = open(fp, encoding="utf-8").read()
        b = body(h)
        t = strip_tags(b)
        n = en_words(t) if lang == "EN" else cjk(t)
        floor = 2500 if lang == "EN" else 3500
        h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', b, re.S)
        h2q = sum(1 for x in h2s if '?' in x or '？' in x)
        cta = 'article-cta-btn' in h
        phrase = {"EN": "Book a Demo", "CN": "预约演示", "TW": "預約示範"}[lang]
        print(f"  {lang}: len={n} (floor {floor}) {'OK' if n>=floor else 'SHORT'} | h2={len(h2s)} q={h2q} | faqH3={faq_count(h)} | faqLD={faqld(h)} | cta={cta} phrase={phrase in h} | bytes={len(h)}")
        print(f"      H1: {h1(h)[:110]}")
