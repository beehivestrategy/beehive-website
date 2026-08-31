#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify a slug (or all gbatch_003 slugs) against the brief standard."""
import os, re, sys, json
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb003_lib import (ROOT, PFX, path_for, ART_OPEN, H2_RE, clean, stats, meta_desc)

PHRASE = {'en': 'Book a Demo', 'zh-cn': '预约演示', 'zh-tw': '預約示範'}
Q_EN = re.compile(r'^(How|What|Why|When|Which|Where|Can|Do|Does|Is|Are|Should|Who|Will)\b', re.I)
Q_ZH = re.compile(r'(如何|什么是|为什么|為什|怎麼|怎么|是否|怎樣|怎样|哪些|哪個|哪个|誰|谁|何時|何时|要多|能否|該如何|该如何|[？?]$)')


def check(slug):
    issues = []
    for lang in ('en', 'zh-cn', 'zh-tw'):
        p = path_for(slug, lang)
        h = open(p, encoding='utf-8').read()
        ai = h.find(ART_OPEN); ae = h.find('</article>', ai)
        art = h[ai:ae]
        st = stats(slug, lang)
        if lang == 'en':
            if st['words'] < 2500:
                issues.append(f'{lang}: words {st["words"]} < 2500')
        else:
            if st['cjk'] < 3500:
                issues.append(f'{lang}: cjk {st["cjk"]} < 3500')
        if st['faq'] < 3:
            issues.append(f'{lang}: faq h3 count {st["faq"]} < 3')
        if st['ld'] != 1:
            issues.append(f'{lang}: FAQPage blocks {st["ld"]} != 1')
        # JSON-LD matches page
        m = re.search(r'<script type="application/ld\+json"[^>]*>(\{.*?"FAQPage".*?\})</script>', h, re.S)
        if m:
            try:
                obj = json.loads(m.group(1))
            except Exception as e:
                issues.append(f'{lang}: bad JSON-LD ({e})')
                obj = None
            if obj:
                jq = [x['name'] for x in obj['mainEntity']]
                pq = [clean(x) for x in re.findall(r'<h3 class="faq-question-text"[^>]*>(.*?)</h3>', art, re.S)]
                if jq != pq:
                    issues.append(f'{lang}: JSON-LD/page FAQ mismatch {len(jq)} vs {len(pq)}')
                pa = [clean(x) for x in re.findall(r'<div class="faq-answer-inner">(.*?)</div>', art, re.S)]
                ja = [x['acceptedAnswer']['text'] for x in obj['mainEntity']]
                if [re.sub(r'\s+', ' ', x) for x in ja] != [re.sub(r'\s+', ' ', x) for x in pa]:
                    issues.append(f'{lang}: JSON-LD answer mismatch')
        # CTA
        if PHRASE[lang] not in h:
            issues.append(f'{lang}: CTA phrase missing')
        # links
        for m in re.finditer(r'<a href="([^"]*)" class="(recommended-card|sidebar-related-card)">', h):
            href = m.group(1)
            want = '/' + PFX[lang] + 'blog/articles/'
            if not href.startswith(want):
                issues.append(f'{lang}: bad link {href}')
        for m in re.finditer(r'<a href="([^"]*?/blog/articles/[^"]*)" class="recommended-card">(.*?)</a>', h, re.S):
            ex = re.search(r'<p class="recommended-card-excerpt">(.*?)</p>', m.group(2), re.S)
            if not ex or not clean(ex.group(1)):
                issues.append(f'{lang}: empty excerpt {m.group(1)}')
        # H2 questions
        for m in H2_RE.finditer(art):
            t = clean(m.group(3))
            if not t:
                continue
            ok = Q_EN.match(t) if lang == 'en' else Q_ZH.search(t)
            if not ok:
                issues.append(f'{lang}: non-question H2 -> {t[:48]}')
        # guardrails
        if '/css/article.css?v=20260826' not in h or '/js/article.js?v=20260826' not in h:
            issues.append(f'{lang}: versioned asset link missing')
        if re.search(r'lorem ipsum|TODO|placeholder', h, re.I):
            issues.append(f'{lang}: placeholder text')
    return issues


if __name__ == '__main__':
    slugs = sys.argv[1:] or [l.strip() for l in open(os.path.join(ROOT, '_batch_pipeline/gap_batches/gbatch_003.txt')) if l.strip()]
    bad = 0
    for s in slugs:
        iss = check(s)
        if iss:
            bad += 1
            print('FAIL', s)
            for i in iss:
                print('   -', i)
        else:
            print('PASS', s)
    print('---', bad, 'failing of', len(slugs))
