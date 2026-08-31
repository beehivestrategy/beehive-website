#!/usr/bin/env python3
"""Final audit for gbatch_002 against the GEO/SEO standard."""
import json
import os
import re
import sys

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
CJK = re.compile(r'[\u3400-\u4dbf\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]')
TAG = re.compile(r'<[^>]+>')
SCRIPT_RE = re.compile(r'<script\b[^>]*>.*?</script>', re.S | re.I)
STYLE_RE = re.compile(r'<style\b[^>]*>.*?</style>', re.S | re.I)
ARTICLE_RE = re.compile(r'(<article\b[^>]*id="article-content"[^>]*>)(.*?)(</article>)', re.S | re.I)


def text_of(html):
    import html as H
    html = SCRIPT_RE.sub(' ', html)
    html = STYLE_RE.sub(' ', html)
    return H.unescape(TAG.sub(' ', html))


def en_words(t):
    return len(re.findall(r"[A-Za-z][A-Za-z'\-]*", t))


def cjk(t):
    return len(CJK.findall(t))


def audit(path, lang):
    doc = open(path, encoding='utf-8').read()
    m = ARTICLE_RE.search(doc)
    art = m.group(2) if m else ''
    t = text_of(art)

    fm = art.find('class="faq-section"')
    faq_html = art[fm:] if fm >= 0 else ''
    faq_q = len(re.findall(r'<h3[^>]*>', faq_html))
    # questions: text inside h3 (strip number span)
    qs = []
    for h in re.findall(r'<h3[^>]*>(.*?)</h3>', faq_html, re.S):
        txt = re.sub(r'\s+', ' ', text_of(h)).strip()
        txt = re.sub(r'^\d+\s*', '', txt).strip()
        qs.append(txt)
    ans = [re.sub(r'\s+', ' ', text_of(a)).strip()
           for a in re.findall(r'<div class="faq-answer-inner">(.*?)</div>', faq_html, re.S)]

    lds = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', doc, re.S | re.I)
    faqpage = [s for s in lds if 'FAQPage' in s]
    ld_ok = False
    if len(faqpage) == 1:
        try:
            d = json.loads(faqpage[0].strip())
            me = d.get('mainEntity', [])
            ld_pairs = [(re.sub(r'\s+', ' ', x.get('name', '')).strip(),
                         re.sub(r'\s+', ' ', x.get('acceptedAnswer', {}).get('text', '')).strip()) for x in me]
            ld_ok = len(me) >= 3 and len(ld_pairs) == len(qs) and all(
                a[0] == b[0] and a[1] == b[1] for a, b in zip(ld_pairs, list(zip(qs, ans))))
        except Exception as e:
            ld_ok = False

    h2s = [re.sub(r'\s+', ' ', text_of(h)).strip() for h in re.findall(r'<h2[^>]*>(.*?)</h2>', art, re.S)]
    h2s = [h for h in h2s if 'Frequently Asked' not in h and '常见问题' not in h and '常見問題' not in h]
    q = [h for h in h2s if h.endswith('?') or h.endswith('？')]

    want_cta = {'en': 'Book a Demo', 'zh-cn': '预约演示', 'zh-tw': '預約示範'}[lang]
    cta_ok = bool(re.search(r'<a href="[^"]*" class="article-cta-btn"[^>]*>\s*' + re.escape(want_cta) + r'\s*<', doc))

    pfx = {'en': '/blog/articles/', 'zh-cn': 'zh-cn/blog/articles/', 'zh-tw': 'zh-tw/blog/articles/'}[lang]
    hrefs = re.findall(r'<a href="([^"]*)" class="recommended-card"', doc)
    rec_ok = len(hrefs) > 0 and all(h.startswith(pfx) for h in hrefs)
    exc_ok = all(e.strip() for e in re.findall(r'<p class="recommended-card-excerpt">(.*?)</p>', doc, re.S))

    return {
        'en_words': en_words(t), 'cjk': cjk(t),
        'words_ok': en_words(t) >= 2500 if lang == 'en' else True,
        'cjk_ok': cjk(t) >= 3500 if lang != 'en' else True,
        'faq_n': faq_q, 'faq_ok': faq_q >= 3,
        'ld_n': len(faqpage), 'ld_match': ld_ok,
        'h2_q': len(q), 'h2_n': len(h2s), 'h2_ok': len(q) == len(h2s),
        'cta_ok': cta_ok, 'rec_ok': rec_ok, 'exc_ok': exc_ok,
        'h2s': h2s,
    }


def main():
    slugs = [l.strip() for l in open(os.path.join(ROOT, '_batch_pipeline/gap_batches/gbatch_002.txt')) if l.strip()]
    allok = True
    report = {}
    for s in slugs:
        report[s] = {}
        line = []
        for lang, pfx in (('en', ''), ('zh-cn', 'zh-cn/'), ('zh-tw', 'zh-tw/')):
            p = os.path.join(ROOT, pfx, 'blog/articles', s + '.html')
            r = audit(p, lang)
            report[s][lang] = r
            ok = r['words_ok'] and r['cjk_ok'] and r['faq_ok'] and r['ld_match'] and r['ld_n'] == 1 \
                and r['h2_ok'] and r['cta_ok'] and r['rec_ok'] and r['exc_ok']
            allok &= ok
            fails = []
            if lang == 'en' and not r['words_ok']:
                fails.append(f"words{r['en_words']}")
            if lang != 'en' and not r['cjk_ok']:
                fails.append(f"cjk{r['cjk']}")
            if not r['faq_ok']:
                fails.append(f"faq{r['faq_n']}")
            if r['ld_n'] != 1:
                fails.append(f"ldN{r['ld_n']}")
            elif not r['ld_match']:
                fails.append('ldMismatch')
            if not r['h2_ok']:
                fails.append(f"h2{r['h2_q']}/{r['h2_n']}")
            if not r['cta_ok']:
                fails.append('cta')
            if not r['rec_ok']:
                fails.append('rec')
            if not r['exc_ok']:
                fails.append('exc')
            line.append(f"{lang}:{'OK' if not fails else ','.join(fails)}")
        print(f"{s:55s} " + '  '.join(line))
    print('\nALL OK' if allok else '\nREMAINING GAPS')
    json.dump(report, open(os.path.join(ROOT, '_batch_pipeline/_gb002_final.json'), 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
