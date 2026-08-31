import re, sys, json, os
ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def cjk(t):
    return len(re.findall(r'[\u4e00-\u9fff]', t))

def words(t):
    return len(re.findall(r"[A-Za-z][A-Za-z'\-]*", t))

def article_body(html):
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', html, re.S)
    if not m:
        m = re.search(r'<article[^>]*>(.*?)</article>', html, re.S)
    return m.group(1) if m else ""

def strip_tags(t):
    t = re.sub(r'<script.*?</script>', ' ', t, flags=re.S)
    t = re.sub(r'<style.*?</style>', ' ', t, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    return t

def faq_info(html):
    m = re.search(r'<[^>]*class="faq-section"[^>]*>(.*?)', html, re.S)
    if not m:
        return 0, []
    seg = html[m.start():]
    # cut at the closing of faq section: find next </section> or start of recommended/cta
    end = re.search(r'(<div[^>]*class="article-cta|<section[^>]*class="recommended|</main>)', seg)
    seg = seg[:end.start()] if end else seg[:20000]
    qs = re.findall(r'<h3[^>]*>(.*?)</h3>', seg, re.S)
    return len(qs), [re.sub(r'<[^>]+>','',q).strip() for q in qs]

def ld_blocks(html):
    out = []
    for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S):
        out.append((m.start(), m.group(1)))
    return out

def has_faqpage(html):
    for _, b in ld_blocks(html):
        if '"FAQPage"' in b:
            return True
    return False

slugs = [l.strip() for l in open(os.path.join(ROOT,'_batch_pipeline/gap_batches/gbatch_003.txt')) if l.strip()]
paths = {'EN':'blog/articles/%s.html','zh-CN':'zh-cn/blog/articles/%s.html','zh-TW':'zh-tw/blog/articles/%s.html'}
res = {}
for s in slugs:
    row = {}
    for lang, tpl in paths.items():
        p = os.path.join(ROOT, tpl % s)
        if not os.path.exists(p):
            row[lang] = {'missing': True}
            continue
        h = read(p)
        body = article_body(h)
        txt = strip_tags(body)
        nfaq, qlist = faq_info(h)
        row[lang] = {
            'words': words(txt),
            'cjk': cjk(txt),
            'faq': nfaq,
            'ld': has_faqpage(h),
            'cta': 'article-cta-btn' in h,
            'h2': len(re.findall(r'<h2[^>]*>', body)),
            'bytes': len(h),
        }
    res[s] = row

for s in slugs:
    r = res[s]
    parts = []
    for lang in ('EN','zh-CN','zh-TW'):
        d = r[lang]
        if d.get('missing'):
            parts.append(f"{lang}: MISSING")
        else:
            parts.append(f"{lang}: w={d['words']} cjk={d['cjk']} faq={d['faq']} ld={'Y' if d['ld'] else 'N'} cta={'Y' if d['cta'] else 'N'} h2={d['h2']}")
    print(s, '|', ' || '.join(parts))
