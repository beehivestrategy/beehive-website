import os, re, json
ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slugs = [l.strip() for l in open(os.path.join(ROOT, "_batch_pipeline/gap_batches/gbatch_003.txt")) if l.strip()]
FAIL = []
def body_of(t):
    m = re.search(r'<article id="article-content">(.*)', t, re.S)
    return m.group(1) if m else t
def cjk(t):
    return len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', re.sub(r'<[^>]+>',' ', body_of(t))))
def enw(t):
    return len(re.findall(r"[A-Za-z][A-Za-z'\-]+", re.sub(r'<[^>]+>',' ', body_of(t))))
for slug in slugs:
    row = {"slug": slug}
    ok = True
    for lang, pref, phrase in [("EN","blog/articles","Book a Demo"),
                               ("zh-CN","zh-cn/blog/articles","预约演示"),
                               ("zh-TW","zh-tw/blog/articles","預約示範")]:
        fp = os.path.join(ROOT, pref, slug+".html")
        t = open(fp, encoding="utf-8").read()
        n = enw(t) if lang=="EN" else cjk(t)
        faq = bool(re.search(r'class="faq-section"', t))
        items = len(re.findall(r'class="faq-item"', t))
        h3 = bool(re.search(r'class="faq-section".*?<h3', t, re.S))
        jld = len(re.findall(r'"@type"\s*:\s*"FAQPage"', t))
        rel = len(re.findall(r'href="blog/articles/', t))
        ex = re.findall(r'class="recommended-card-excerpt">(.*?)</p>', t, re.S)
        ex_bad = sum(1 for e in ex if not e.strip() or 'for a deeper look at what it means' in e)
        cta = phrase in t
        undef = bool(re.search(r'(?i)\bundefined\b', t))
        # h2 questions (exclude faq title which has no id)
        h2 = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', t, re.S)
        q = sum(1 for i,x in h2 if (x.rstrip().endswith('?') or x.rstrip().endswith('？')))
        row[lang] = dict(n=n, faq=faq, items=items, h3=h3, jld=jld, rel=rel, ex_bad=ex_bad, cta=cta, undef=undef, h2q=q, h2tot=len(h2))
        if lang=="EN" and n < 2500: ok=False; FAIL.append((slug,"EN<%d"%n))
        if lang!="EN" and n < 3500: ok=False; FAIL.append((slug,"%s<%d"%(lang,n)))
        if not faq: ok=False; FAIL.append((slug,"%s no faq"%lang))
        if items < 3: ok=False; FAIL.append((slug,"%s faq_items=%d"%(lang,items)))
        if not h3: ok=False; FAIL.append((slug,"%s no h3"%lang))
        if jld != 1: ok=False; FAIL.append((slug,"%s jld=%d"%(lang,jld)))
        if rel != 0: ok=False; FAIL.append((slug,"%s rel=%d"%(lang,rel)))
        if ex_bad>0: ok=False; FAIL.append((slug,"%s ex_bad=%d"%(lang,ex_bad)))
        if not cta: ok=False; FAIL.append((slug,"%s no cta"%lang))
        if undef: ok=False; FAIL.append((slug,"%s undefined"%lang))
        if q < len(h2): ok=False; FAIL.append((slug,"%s h2q=%d/%d"%(lang,q,len(h2))))
        # guardrails
        if '?v=20260826' not in t: ok=False; FAIL.append((slug,"%s missing v=20260826"%lang))
    print(json.dumps(row, ensure_ascii=False))
print("\nFAILURES:", len(FAIL))
for f in FAIL: print("  ", f)
