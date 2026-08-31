#!/usr/bin/env python3
"""Measure article body length inside <article id="article-content">."""
import re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def extract(path):
    s = open(path, encoding='utf-8').read()
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', s, re.S)
    if not m:
        m = re.search(r'<article[^>]*>(.*?)</article>', s, re.S)
    if not m:
        return None, s
    return m.group(1), s

def strip_tags(html):
    html = re.sub(r'<script.*?</script>', ' ', html, flags=re.S)
    html = re.sub(r'<style.*?</style>', ' ', html, flags=re.S)
    html = re.sub(r'<!--.*?-->', ' ', html, flags=re.S)
    html = re.sub(r'<[^>]+>', ' ', html)
    html = re.sub(r'&nbsp;', ' ', html)
    html = re.sub(r'&amp;', '&', html)
    html = re.sub(r'&[a-z]+;', ' ', html)
    return html

CJK = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]')
LATIN = re.compile(r'[A-Za-z]+')

def stats(path):
    body, full = extract(path)
    if body is None:
        return None
    text = strip_tags(body)
    cjk = len(CJK.findall(text))
    words = len(LATIN.findall(text))
    faqs = len(re.findall(r'<h3[^>]*>', body))
    faq_sec = 1 if 'faq-section' in body else 0
    ld = len(re.findall(r'"@type"\s*:\s*"FAQPage"', full))
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', body, re.S)
    cta = 1 if 'article-cta-btn' in body else 0
    return dict(cjk=cjk, words=words, faq_h3=faqs, faq_sec=faq_sec, ld=ld,
                h2=[re.sub(r'<[^>]+>', '', h).strip() for h in h2s], cta=cta,
                faqpage_in_body=len(re.findall(r'"@type"\s*:\s*"FAQPage"', body)))

if __name__ == '__main__':
    for slug in [l.strip() for l in open(sys.argv[1]) if l.strip()]:
        row = [slug]
        for lang, prefix in [('EN', 'blog'), ('CN', 'zh-cn/blog'), ('TW', 'zh-tw/blog')]:
            p = os.path.join(ROOT, prefix, 'articles', slug + '.html')
            if not os.path.exists(p):
                row.append(f'{lang}:MISSING')
                continue
            s = stats(p)
            row.append(f'{lang} w={s["words"]} cjk={s["cjk"]} h3={s["faq_h3"]} faqsec={s["faq_sec"]} ld={s["ld"]} cta={s["cta"]}')
        print(' | '.join(row))
