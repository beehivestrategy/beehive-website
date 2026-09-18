import re, sys, os, json, html

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"

CJK = re.compile(r'[\u4e00-\u9fff]')

def strip_tags(s):
    s = re.sub(r'<[^>]+>', '', s)
    return html.unescape(s).strip()

def extract(rel):
    p = os.path.join(ROOT, rel)
    src = open(p, encoding='utf-8').read()
    out = {}
    m = re.search(r'<h1[^>]*>(.*?)</h1>', src, re.S)
    out['h1'] = strip_tags(m.group(1)) if m else None
    m = re.search(r'<p class="article-lead"[^>]*>(.*?)</p>', src, re.S)
    out['lead'] = strip_tags(m.group(1)) if m else None
    out['h2'] = [(strip_tags(x)) for x in re.findall(r'<h2[^>]*>(.*?)</h2>', src, re.S)]
    out['h3'] = [(strip_tags(x)) for x in re.findall(r'<h3[^>]*>(.*?)</h3>', src, re.S)]
    # raw heading tags (to see id/class) - english only
    out['raw_h'] = [t for t in re.findall(r'<h[23][^>]*>.*?</h[23]>', src, re.S) if not CJK.search(strip_tags(t))]
    out['toc'] = re.findall(r'<a[^>]*href="(#[^"]+)"[^>]*>(.*?)</a>', src, re.S)
    # english-only headings
    out['en_h'] = [(t, 'h2') for t in out['h2'] if t and not CJK.search(t)] + \
                  [(t, 'h3') for t in out['h3'] if t and not CJK.search(t)]
    # faq items: split on faq-item boundaries
    faqs = []
    for chunk in src.split('<div class="faq-item">')[1:]:
        q = re.search(r'<span class="faq-question-text"><span class="faq-number">\s*(\d+)\s*</span><span>(.*?)</span>', chunk, re.S)
        a = re.search(r'<div class="faq-answer-inner">(.*?)</div>', chunk, re.S)
        faqs.append({'n': q.group(1) if q else None,
                     'q': strip_tags(q.group(2)) if q else None,
                     'a': strip_tags(a.group(1)) if a else None})
    out['faq'] = faqs
    # json-ld FAQPage
    lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', src, re.S)
    out['ld_faq'] = None
    out['ld_types'] = []
    for l in lds:
        try:
            d = json.loads(l.strip())
        except Exception:
            out['ld_types'].append('PARSE_FAIL')
            continue
        ds = d if isinstance(d, list) else [d]
        for dd in ds:
            if isinstance(dd, dict):
                out['ld_types'].append(dd.get('@type'))
                if dd.get('@type') == 'FAQPage':
                    out['ld_faq'] = [{'name': e.get('name'),
                                      'text': (e.get('acceptedAnswer') or {}).get('text')}
                                     for e in dd.get('mainEntity', [])]
    # tags
    out['tags'] = sorted(set(strip_tags(x) for x in re.findall(r'<[^>]*class="[^"]*article-tag-pill[^"]*"[^>]*>(.*?)</', src, re.S)))
    out['en_tags'] = [t for t in out['tags'] if t and not CJK.search(t)]
    # rec card titles
    out['en_anchors'] = sorted(set(strip_tags(x) for x in re.findall(r'<a[^>]*href="[^"]*"[^>]*>(.*?)</a>', src, re.S)
                                   if x and not CJK.search(strip_tags(x)) and len(strip_tags(x)) > 2))
    out['div_delta'] = len(re.findall(r'<div\b', src)) - len(re.findall(r'</div>', src))
    out['undef'] = src.count('undefined')
    out['size'] = len(src)
    return out

if __name__ == '__main__':
    files = [l.strip() for l in open(os.path.join(ROOT, '_batch_pipeline/wo_faq_3.txt')) if l.strip()]
    if len(sys.argv) > 1:
        files = files[int(sys.argv[1]):int(sys.argv[2])]
    for f in files:
        d = extract(f)
        print('=' * 70)
        print('FILE:', f)
        print('SIZE:', d['size'], 'DIV_DELTA:', d['div_delta'], 'UNDEF_COUNT:', d['undef'])
        print('H1:', d['h1'])
        print('LEAD:', d['lead'])
        print('H2:', d['h2'])
        print('H3:', d['h3'][:15])
        print('EN_HEADINGS:', d['en_h'])
        print('EN_TAGS:', d['en_tags'])
        print('LD_TYPES:', d['ld_types'])
        print('FAQ_VISIBLE:', len(d['faq']))
        for i, x in enumerate(d['faq'], 1):
            print('  Q%d: %s' % (i, x['q']))
            print('  A%d: %s' % (i, (x['a'] or '')[:120]))
        print('LD_FAQ:', len(d['ld_faq']) if d['ld_faq'] is not None else None)
        if d['ld_faq']:
            for i, x in enumerate(d['ld_faq'], 1):
                print('  LQ%d: %s' % (i, x['name']))
                print('  LA%d: %s' % (i, (x['text'] or '')[:120]))
        print('EN_ANCHORS:', d['en_anchors'][:40])
        print('RAW_EN_HEADINGS:', d['raw_h'])
        print('TOC:', [(h, strip_tags(t)) for h, t in d['toc'] if not CJK.search(strip_tags(t))])
