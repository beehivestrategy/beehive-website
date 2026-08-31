import os, re, glob, json, sys

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
BATCH = os.path.join(ROOT, "_batch_pipeline/gap_batches/gbatch_001.txt")

with open(BATCH) as f:
    slugs = [l.strip() for l in f if l.strip()]

def cjk_count(s):
    return len(re.findall(r'[\u3400-\u9fff\uf900-\ufaff]', s))

def en_words(s):
    return len(re.findall(r"[A-Za-z][A-Za-z'\-]*", s))

def check_file(path):
    issues = []
    with open(path, encoding='utf-8') as f:
        html = f.read()
    # head must not contain faq-section? Actually EN keeps JSON-LD in head.
    # Count JSON-LD blocks
    jsonld = re.findall(r'<script type="application/ld\+json"[^>]*>', html)
    n_jsonld = len(jsonld)
    # FAQ section
    faq = re.search(r'<section class="faq-section"[^>]*>', html)
    n_faq_q = len(re.findall(r'class="faq-question"', html))
    n_h3 = len(re.findall(r'<h3', html))
    # article content
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', html, re.S)
    body = m.group(1) if m else html
    cjk = cjk_count(body)
    enw = en_words(body)
    # empty excerpts
    empty_excerpt = bool(re.search(r'recommended-card-excerpt">\s*<', html))
    # version query intact
    version_ok = ('?v=20260826' in html)
    # CTA phrase
    cta = re.search(r'class="article-cta-btn"[^>]*>(.*?)</a>', html, re.S)
    cta_phrases = []
    if cta:
        t = re.sub(r'<[^>]+>', '', cta.group(1))
        cta_phrases.append(t.strip())
    # head protection markers
    return dict(path=path, n_jsonld=n_jsonld, has_faq=bool(faq), n_faq_q=n_faq_q,
                n_h3=n_h3, cjk=cjk, enw=enw, empty_excerpt=empty_excerpt,
                version_ok=version_ok, cta=cta_phrases)

for slug in slugs:
    print("="*70)
    print("SLUG:", slug)
    for lang, prefix in [("en",""), ("zh-CN","zh-cn/"), ("zh-TW","zh-tw/")]:
        p = os.path.join(ROOT, prefix+"blog/articles/"+slug+".html")
        if not os.path.exists(p):
            print(f"  [{lang}] MISSING")
            continue
        r = check_file(p)
        tag = os.path.basename(p)
        # thresholds
        if lang=="en":
            ok_len = r['enw']>=2500
        else:
            ok_len = r['cjk']>=3500
        ok_faq = r['n_faq_q']>=3 and r['n_h3']>=3
        ok_jsonld = r['n_jsonld']==1
        flags=[]
        if not ok_len: flags.append("LEN")
        if not ok_faq: flags.append("FAQ")
        if not ok_jsonld: flags.append("JSONLD")
        if r['empty_excerpt']: flags.append("EXCERPT")
        if not r['version_ok']: flags.append("VER")
        if not r['cta']: flags.append("CTA")
        print(f"  [{lang}] {r['enw']}w/{r['cjk']}cjk faqQ={r['n_faq_q']} h3={r['n_h3']} jsonld={r['n_jsonld']} cta={r['cta']} flags={flags if flags else 'OK'}")
