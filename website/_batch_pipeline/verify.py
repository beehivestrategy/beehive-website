# -*- coding: utf-8 -*-
import re, json, os

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
paths = [l.strip() for l in open(os.path.join(ROOT, "_batch_pipeline/wo_faq_1.txt"), encoding='utf-8') if l.strip()]
base = json.load(open(os.path.join(ROOT, "_batch_pipeline/baseline.json")))
CJK = re.compile(r'[一-鿿]')

def txt(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()

fails = []
for rel in paths:
    fp = os.path.join(ROOT, rel)
    s = open(fp, encoding='utf-8').read()
    prob = []

    # 1. no visible undefined
    if re.search(r'>\s*undefined\s*<', s) or '">undefined' in s or 'undefined</' in s:
        prob.append('undefined visible')

    # 2a. tag integrity: no broken heading start tags
    if re.search(r'(?<![</])h[23](?:\s+class="recommended-card-title")?>', s):
        prob.append('broken h2/h3 tag')
    for tag in ('h2', 'h3'):
        o = len(re.findall(r'<%s\b' % tag, s)); c = len(re.findall(r'</%s>' % tag, s))
        if o != c:
            prob.append('%s open %d != close %d' % (tag, o, c))

    # 2. no pure-English h2/h3
    for m in re.finditer(r'<(h2|h3)([^>]*)>(.*?)</\1>', s, re.S):
        t = txt(m.group(3))
        if t and not CJK.search(t):
            prob.append('EN heading: ' + t[:60])

    # 3. FAQ count == JSON-LD mainEntity count, texts match
    vis = []
    ml = re.search(r'(<div class="faq-list">)(.*?)(\s*</div>\s*</section>)', s, re.S)
    if not ml:
        prob.append('no faq-list')
    else:
        for b in re.split(r'(?=<div class="faq-item">)', ml.group(2))[1:]:
            q = re.search(r'faq-question-text"[^>]*>(?:<span class="faq-number">\d+</span><span>)?(.*?)(?:</span></span>|</h3>)', b, re.S)
            a = re.search(r'faq-answer-inner">(.*?)</div>', b, re.S)
            if q and a:
                vis.append((txt(q.group(1)), txt(a.group(1))))
    if len(vis) != 4:
        prob.append('visible faq=%d' % len(vis))
    ld = None
    for lm in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            d = json.loads(lm.group(1))
        except Exception as e:
            prob.append('LD parse error: %s' % e)
            continue
        for o in (d if isinstance(d, list) else [d]):
            if isinstance(o, dict) and o.get('@type') == 'FAQPage':
                ld = o.get('mainEntity', [])
    if ld is None:
        prob.append('no FAQPage LD')
    else:
        if len(ld) != len(vis):
            prob.append('LD count %d != visible %d' % (len(ld), len(vis)))
        else:
            for i, (vq, va) in enumerate(vis):
                if ld[i].get('name') != vq:
                    prob.append('LD Q%d mismatch' % (i + 1))
                if ld[i].get('acceptedAnswer', {}).get('text') != va:
                    prob.append('LD A%d mismatch' % (i + 1))

    # 4. div / section balance unchanged
    d = len(re.findall(r'<div\b', s)) - len(re.findall(r'</div>', s))
    sc = len(re.findall(r'<section\b', s)) - len(re.findall(r'</section>', s))
    bd, bs, _ = base[rel]
    if d != bd or sc != bs:
        prob.append('balance div %d->%d section %d->%d' % (bd, d, bs, sc))

    # extra: FAQ questions must not duplicate H2 headings
    h2 = set()
    for m in re.finditer(r'<h2[^>]*>(.*?)</h2>', s, re.S):
        t = txt(m.group(1)).rstrip('？?')
        if t:
            h2.add(t)
    for vq, _ in vis:
        if vq.rstrip('？?') in h2:
            prob.append('Q duplicates H2: ' + vq)

    if prob:
        fails.append((rel, prob))

print("checked", len(paths), "files; failures:", len(fails))
for rel, p in fails:
    print(" FAIL", rel, "|", " ;; ".join(p))
