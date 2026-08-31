import os, re, json

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slugs = [l.strip() for l in open(os.path.join(ROOT, "_batch_pipeline/gap_batches/gbatch_003.txt")) if l.strip()]

def body_of(t):
    m = re.search(r'<article id="article-content">(.*)', t, re.S)
    return m.group(1) if m else t

def en_words(t):
    txt = re.sub(r'<[^>]+>', ' ', body_of(t))
    return len(re.findall(r"[A-Za-z][A-Za-z'\-]+", txt))

def cjk(t):
    txt = re.sub(r'<[^>]+>', ' ', body_of(t))
    return len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', txt))

def faq_section(t):
    m = re.search(r'class="faq-section".*?(</section>|</div>)', t, re.S)
    return m.group(0) if m else None

def jsonld_head(t):
    head = t[:t.lower().find('</head>')] if '</head>' in t.lower() else t
    return '"@type":"FAQPage"' in head or '"@type": "FAQPage"' in head

def jsonld_body(t):
    b = t[t.lower().find('<body'):] if '<body' in t.lower() else t
    return '"@type":"FAQPage"' in b or '"@type": "FAQPage"' in b

def rel_hrefs(t):
    return re.findall(r'href="(blog/articles/[^"]+)"', t)

def empty_excerpt(t):
    # recommended-card-excerpt with empty or generic placeholder text
    ex = re.findall(r'class="recommended-card-excerpt">(.*?)</p>', t, re.S)
    bad = []
    for e in ex:
        s = e.strip()
        if not s or 'for a deeper look at what it means' in s:
            bad.append(s)
    return len(bad), len(ex)

def cta(t, phrase):
    return phrase in t

def has_undef(t):
    return 'undefined' in body_of(t).lower()

def h2s(t):
    bs = re.findall(r'<h2[^>]*id="([^"]+)">(.*?)</h2>', body_of(t), re.S)
    return [(i, re.sub(r'<[^>]+>','',x).strip()) for i,x in bs]

for slug in slugs:
    out = {"slug": slug}
    for lang, prefix, phrase in [("EN","blog/articles","Book a Demo"),
                                 ("zh-CN","zh-cn/blog/articles","预约演示"),
                                 ("zh-TW","zh-tw/blog/articles","預約示範")]:
        fp = os.path.join(ROOT, prefix, slug + ".html")
        if not os.path.exists(fp):
            out[lang] = "MISSING"; continue
        t = open(fp, encoding="utf-8").read()
        fs = faq_section(t)
        faq_items = len(re.findall(r'class="faq-item"', fs)) if fs else 0
        h3_in_faq = bool(fs and re.search(r'<h3', fs))
        h2 = h2s(t)
        q_h2 = sum(1 for _,x in h2 if x.rstrip().endswith('?'))
        ne, nt = empty_excerpt(t)
        out[lang] = {
            "words/cjk": en_words(t) if lang=="EN" else cjk(t),
            "faq_section": bool(fs),
            "faq_items": faq_items,
            "h3_in_faq": h3_in_faq,
            "jld_head": jsonld_head(t),
            "jld_body": jsonld_body(t),
            "rel_hrefs": len(rel_hrefs(t)),
            "excerpt_empty": f"{ne}/{nt}",
            "cta": cta(t, phrase),
            "undefined": has_undef(t),
            "h2_total": len(h2),
            "h2_question": q_h2,
        }
    print(json.dumps(out, ensure_ascii=False))
