#!/usr/bin/env python3
import re, sys, os

CJK = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]')

def article_html(path):
    s = open(path, encoding='utf-8').read()
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', s, re.S)
    if not m:
        m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*)$', s, re.S)
    if not m:
        return None, s
    return m.group(1), s

def en_words(html):
    t = re.sub(r'<script.*?</script>', ' ', html, flags=re.S)
    t = re.sub(r'<style.*?</style>', ' ', t, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'&[a-zA-Z#0-9]+;', ' ', t)
    return len(t.split())

def cjk(html):
    t = re.sub(r'<script.*?</script>', ' ', html, flags=re.S)
    t = re.sub(r'<style.*?</style>', ' ', t, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    return len(CJK.findall(t))

root = sys.argv[1]
slugs = [l.strip() for l in sys.stdin if l.strip()]
for slug in slugs:
    en = os.path.join(root, 'blog/articles/%s.html' % slug)
    zc = os.path.join(root, 'zh-cn/blog/articles/%s.html' % slug)
    zt = os.path.join(root, 'zh-tw/blog/articles/%s.html' % slug)
    out = [slug]
    for p, fn, label in ((en, en_words, 'EN'), (zc, cjk, 'CN'), (zt, cjk, 'TW')):
        if not os.path.exists(p):
            out.append('%s:MISSING' % label)
            continue
        h, full = article_html(p)
        if h is None:
            out.append('%s:NOART' % label)
        else:
            out.append('%s:%d' % (label, fn(h)))
        # faq + jsonld
        faqm = re.search(r'<div class="faq-list">(.*?)\n\s*</div>', full, re.S)
        faq = len(re.findall(r'<h3', faqm.group(1))) if faqm else 0
        jl = len(re.findall(r'"@type"\s*:\s*"FAQPage"', full))
        cta = 'y' if re.search(r'class="article-cta-btn"[^>]*>\s*(Book a Demo|预约演示|預約示範)\s*<', full) else 'n'
        h2 = re.findall(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', full, re.S)
        bad = sum(1 for i, t in h2 if not re.search(r'[?？]\s*$', t.strip()))
        out.append('(faqh3=%d,json=%d,cta=%s,h2notq=%d)' % (faq, jl, cta, bad))
    print(' '.join(out))
