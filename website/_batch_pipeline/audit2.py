#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit: article prose length (inside <article id=article-content>) + FAQ section/JSON-LD anywhere in doc."""
import re, sys, os, json

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
CJK = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]')
LATIN = re.compile(r"[A-Za-z][A-Za-z'\-]*")


def strip_tags(h):
    h = re.sub(r'<script[^>]*>.*?</script>', ' ', h, flags=re.S | re.I)
    h = re.sub(r'<style[^>]*>.*?</style>', ' ', h, flags=re.S | re.I)
    h = re.sub(r'<!--.*?-->', ' ', h, flags=re.S)
    h = re.sub(r'<[^>]+>', ' ', h)
    h = re.sub(r'&[a-zA-Z#0-9]+;', ' ', h)
    return h


def audit(path, lang):
    s = open(path, encoding='utf-8').read()
    # --- article prose ---
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', s, re.S | re.I)
    body = m.group(1) if m else ''
    text = strip_tags(body)
    w = len(LATIN.findall(text))
    cj = len(CJK.findall(text))

    # --- FAQ section (document level) ---
    fq = re.findall(r'<h3[^>]*>\s*<button class="faq-question".*?<span>(.*?)</span>', s, re.S | re.I)
    faq_answers = re.findall(r'<div class="faq-answer-inner">(.*?)</div>', s, re.S | re.I)
    if not fq:
        fm = re.search(r'<section class="faq-section".*?</section>', s, re.S | re.I)
        if fm:
            fq = [strip_tags(x).strip() for x in re.findall(r'<h3[^>]*>(.*?)</h3>', fm.group(0), re.S | re.I)]
            faq_answers = [x for x in re.findall(r'<div class="faq-answer-inner">(.*?)</div>', fm.group(0), re.S | re.I)]

    # --- FAQPage JSON-LD ---
    ld_blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S | re.I)
    faq_ld = 0
    ld_q = []
    for b in ld_blocks:
        if '"FAQPage"' in b:
            faq_ld += 1
            try:
                d = json.loads(b.strip())
                for it in d.get('mainEntity', []):
                    ld_q.append(it.get('name', ''))
            except Exception as e:
                ld_q.append('PARSE_ERR')
    # ld placed right after faq closing tag?
    ld_after_faq = bool(re.search(r'</section>\s*<script type="application/ld\+json">[^<]*"FAQPage"', s, re.I)) or \
        bool(re.search(r'</section>\s*<script type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema.org",\s*"@type":\s*"FAQPage"', s, re.S | re.I))

    # --- H2 question style ---
    h2s = [strip_tags(x).strip() for x in re.findall(r'<h2[^>]*>(.*?)</h2>', body, re.S | re.I)]

    # --- recs ---
    recs = re.findall(r'<a class="recommended-card"[^>]*href="([^"]*)"', s)
    exp = {'EN': '/blog/articles/', 'CN': '/zh-cn/blog/articles/', 'TW': '/zh-tw/blog/articles/'}[lang]
    bad = [r for r in recs if not r.startswith(exp)]

    phrase = {'EN': 'Book a Demo', 'CN': '预约演示', 'TW': '預約示範'}[lang]
    return dict(w=w, cjk=cj, faq=len(faq_answers), faqld=faq_ld, ld_after_faq=int(ld_after_faq),
                match=int([x.strip() for x in fq] == [x.strip() for x in ld_q]),
                h2=len(h2s), recs=len(recs), badrec=len(bad),
                cta=int('article-cta-btn' in s), phrase=int(phrase in s),
                vq=int('/css/article.css?v=20260826' in s) + int('/js/article.js?v=20260826' in s),
                h2s=h2s, fqs=[strip_tags(x).strip()[:70] for x in fq])


if __name__ == '__main__':
    for slug in [l.strip() for l in open(sys.argv[1]) if l.strip()]:
        print('==== ' + slug)
        for lang, pre in (('EN', ''), ('CN', 'zh-cn/'), ('TW', 'zh-tw/')):
            p = os.path.join(ROOT, pre + 'blog/articles', slug + '.html')
            if not os.path.exists(p):
                print(f'  {lang}: MISSING'); continue
            r = audit(p, lang)
            flag = ''
            if lang == 'EN' and r['w'] < 2500: flag += f" SHORT({r['w']})"
            if lang != 'EN' and r['cjk'] < 3500: flag += f" SHORT({r['cjk']})"
            if r['faq'] < 3: flag += ' FAQ<3'
            if r['faqld'] != 1: flag += f" LD={r['faqld']}"
            if not r['match']: flag += ' LD_MISMATCH'
            if r['badrec']: flag += f" BADREC{r['badrec']}"
            if not r['cta'] or not r['phrase']: flag += ' CTA'
            if r['vq'] != 2: flag += f" VQ={r['vq']}"
            print(f"  {lang}: w={r['w']} cjk={r['cjk']} h2={r['h2']} faq={r['faq']} ld={r['faqld']} afterfaq={r['ld_after_faq']} match={r['match']} rec={r['recs']} cta={r['cta']}/{r['phrase']} vq={r['vq']}{flag}")
            if flag:
                print(f"      h2s={r['h2s']}")
                print(f"      fqs={r['fqs']}")
