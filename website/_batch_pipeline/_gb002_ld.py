#!/usr/bin/env python3
"""Regenerate the single FAQPage JSON-LD per file so it exactly matches the on-page FAQ."""
import html as H
import json
import os
import re
import sys

sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb002_lib import path_for, SLUGS

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
LD_RE = re.compile(r'(<script type="application/ld\+json"[^>]*>)(.*?)(</script>)', re.S | re.I)
TAG = re.compile(r'<[^>]+>')


def clean(x):
    return re.sub(r'\s+', ' ', H.unescape(TAG.sub('', x))).strip()


def extract_faq(doc):
    ai = doc.find('<article class="article-content"')
    ae = doc.find('</article>', ai)
    art = doc[ai:ae]
    fi = art.find('class="faq-section"')
    if fi < 0:
        return []
    faq = art[fi:]
    out = []
    for h3 in re.findall(r'<h3[^>]*>(.*?)</h3>', faq, re.S):
        m = re.search(r'<span class="faq-question-text">.*?<span class="faq-number">\s*\d+\s*</span>\s*<span>(.*?)</span>',
                      h3, re.S)
        q = clean(m.group(1)) if m else clean(h3)
        q = re.sub(r'^\d+\s*', '', q).strip()
        out.append(q)
    ans = [clean(a) for a in re.findall(r'<div class="faq-answer-inner">(.*?)</div>', faq, re.S)]
    n = min(len(out), len(ans))
    return list(zip(out[:n], ans[:n]))


def build(faq, indent='  '):
    ents = []
    for q, a in faq:
        ents.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        })
    d = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ents}
    body = json.dumps(d, ensure_ascii=False, indent=2)
    return '\n' + '\n'.join(indent + ln for ln in body.split('\n')) + '\n' + indent[:-2]


def main():
    stats = {}
    for slug in SLUGS:
        stats[slug] = {}
        for lang in ('en', 'zh-cn', 'zh-tw'):
            p = path_for(slug, lang)
            doc = open(p, encoding='utf-8').read()
            faq = extract_faq(doc)
            assert len(faq) >= 3, f'{slug} {lang}: only {len(faq)} FAQ pairs'
            new_json = build(faq)

            blocks = list(LD_RE.finditer(doc))
            faq_blocks = [m for m in blocks if 'FAQPage' in m.group(2)]
            if len(faq_blocks) > 1:
                # drop duplicates, keeping the first
                first = faq_blocks[0]
                for m in reversed(faq_blocks[1:]):
                    doc = doc[:m.start()] + doc[m.end():]
                faq_blocks = [first]
            if faq_blocks:
                m = faq_blocks[0]
                old_json = m.group(2)
                if old_json == new_json:
                    stats[slug][lang] = 'unchanged'
                    continue
                doc = doc[:m.start(2)] + new_json + doc[m.end(2):]
                stats[slug][lang] = 'updated'
            else:
                # insert right after the FAQ section closing tag
                ae = doc.find('</article>')
                fs = doc.find('</section>', doc.find('class="faq-section"'))
                assert fs > 0 and fs < ae
                ins = f'\n<script type="application/ld+json">{new_json}</script>'
                doc = doc[:fs + len('</section>')] + ins + doc[fs + len('</section>'):]
                stats[slug][lang] = 'inserted'
            open(p, 'w', encoding='utf-8').write(doc)
    for slug, row in stats.items():
        print(slug, row)


if __name__ == '__main__':
    main()
