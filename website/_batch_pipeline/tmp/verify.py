# -*- coding: utf-8 -*-
import re, os, sys, json, html

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
CJK = re.compile(r'[\u4e00-\u9fff]')

def clean(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()

def check(rel):
    p = os.path.join(ROOT, rel)
    src = open(p, encoding='utf-8').read()
    errs = []
    # 1 undefined visible
    n = len(re.findall(r'>undefined<', src))
    if n:
        errs.append('visible undefined x%d' % n)
    if 'undefined' in src:
        errs.append('undefined in source x%d' % src.count('undefined'))
    # 2 english h2/h3
    for m in re.finditer(r'<h([23])\b[^>]*>((?:(?!</h[23]\b).)*?)</h\1>', src, re.S):
        t = clean(m.group(2))
        if t and not CJK.search(t) and re.search(r'[A-Za-z]{3}', t):
            errs.append('EN h%s: %s' % (m.group(1), t))
        if len(t) > 20:
            errs.append('LONG h%s (%d): %s' % (m.group(1), len(t), t))
    # 3 faq vs jsonld
    vis = len([1 for c in src.split('<div class="faq-item">')[1:]])
    ld = 0
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', src, re.S):
        try:
            d = json.loads(m.group(1).strip())
        except Exception as e:
            errs.append('LD PARSE FAIL: %s' % e)
            continue
        if isinstance(d, dict) and d.get('@type') == 'FAQPage':
            ld = len(d.get('mainEntity', []))
    if vis != ld:
        errs.append('FAQ mismatch visible=%d ld=%d' % (vis, ld))
    # 4 div delta vs git
    return errs, vis, ld, len(re.findall(r'<div\b', src)) - len(re.findall(r'</div>', src))

if __name__ == '__main__':
    files = [l.strip() for l in open(os.path.join(ROOT, '_batch_pipeline/wo_faq_3.txt')) if l.strip()]
    bad = 0
    for f in files:
        errs, vis, ld, dd = check(f)
        if dd != 0:
            errs.append('DIV DELTA %d' % dd)
        if errs:
            bad += 1
            print('FAIL', f)
            for e in errs:
                print('   -', e)
    print('checked %d files, %d with issues' % (len(files), bad))
