import os, re

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
BATCH = os.path.join(ROOT, "_batch_pipeline/gap_batches/gbatch_001.txt")

with open(BATCH) as f:
    slugs = [l.strip() for l in f if l.strip()]

def cjk_count(s):
    return len(re.findall(r'[\u3400-\u9fff\uf900-\ufaff]', s))

def en_words(s):
    return len(re.findall(r"[A-Za-z][A-Za-z'\-]*", s))

def check_file(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()
    # Count FAQPage JSON-LD specifically
    blocks = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S)
    faqpage = sum(1 for b in blocks if 'FAQPage' in b)
    n_faq_q = len(re.findall(r'class="faq-question"', html))
    n_h3 = len(re.findall(r'<h3', html))
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', html, re.S)
    body = m.group(1) if m else html
    cjk = cjk_count(body)
    enw = en_words(body)
    empty_excerpt = bool(re.search(r'recommended-card-excerpt">\s*<', html))
    version_ok = ('?v=20260826' in html)
    cta = re.search(r'class="article-cta-btn"[^>]*>(.*?)</a>', html, re.S)
    cta_text = re.sub(r'<[^>]+>', '', cta.group(1)).strip() if cta else ""
    return dict(faqpage=faqpage, n_faq_q=n_faq_q, n_h3=n_h3, cjk=cjk, enw=enw,
                empty_excerpt=empty_excerpt, version_ok=version_ok, cta=cta_text)

print(f"{'slug':52} {'lang':5} {'enw':>5} {'cjk':>5} {'faqQ':>4} {'h3':>3} {'fp':>3} {'cta':>10} flags")
for slug in slugs:
    for lang, prefix in [("en",""), ("zh-CN","zh-cn/"), ("zh-TW","zh-tw/")]:
        p = os.path.join(ROOT, prefix+"blog/articles/"+slug+".html")
        if not os.path.exists(p):
            print(f"{slug:52} {lang:5} MISSING"); continue
        r = check_file(p)
        if lang=="en":
            ok_len = r['enw']>=2500
        else:
            ok_len = r['cjk']>=3500
        ok_faq = r['n_faq_q']>=3 and r['n_h3']>=3 and r['faqpage']==1
        flags=[]
        if not ok_len: flags.append("LEN")
        if not ok_faq: flags.append("FAQ/FP")
        if r['empty_excerpt']: flags.append("EXCERPT")
        if not r['version_ok']: flags.append("VER")
        if not r['cta']: flags.append("CTA")
        print(f"{slug[:52]:52} {lang:5} {r['enw']:5} {r['cjk']:5} {r['n_faq_q']:4} {r['n_h3']:3} {r['faqpage']:3} {r['cta'][:10]:10} {flags if flags else 'OK'}")
