import os, re, json, glob

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slugs = [l.strip() for l in open(os.path.join(ROOT, "_batch_pipeline/gap_batches/gbatch_003.txt")) if l.strip()]

def count_en_words(t):
    # words inside article-content
    m = re.search(r'<article id="article-content">(.*)', t, re.S)
    body = m.group(1) if m else t
    # strip tags
    txt = re.sub(r'<[^>]+>', ' ', body)
    words = re.findall(r"[A-Za-z][A-Za-z'\-]+", txt)
    return len(words)

def count_cjk(t):
    m = re.search(r'<article id="article-content">(.*)', t, re.S)
    body = m.group(1) if m else t
    txt = re.sub(r'<[^>]+>', ' ', body)
    cjk = re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', txt)
    return len(cjk)

def faq_count(t):
    m = re.search(r'class="faq-section".*?</(div|section)', t, re.S)
    if not m: return 0
    seg = m.group(0)
    return len(re.findall(r'<h3', seg))

def jsonld_head(t):
    head = t[:t.find('<body')] if '<body' in t else t[:t.lower().find('</head>')]
    return '"FAQPage"' in head

def jsonld_body(t):
    return '"FAQPage"' in t and not jsonld_head(t)

for slug in slugs:
    row = {"slug": slug}
    for lang, prefix in [("EN","blog/articles"), ("zh-CN","zh-cn/blog/articles"), ("zh-TW","zh-tw/blog/articles")]:
        fp = os.path.join(ROOT, prefix, slug + ".html")
        if not os.path.exists(fp):
            row[lang] = "MISSING"
            continue
        t = open(fp, encoding="utf-8").read()
        if lang == "EN":
            row[lang] = {"words": count_en_words(t), "faq": faq_count(t),
                         "jld_head": jsonld_head(t), "jld_body": jsonld_body(t)}
        else:
            row[lang] = {"cjk": count_cjk(t), "faq": faq_count(t),
                         "jld_head": jsonld_head(t), "jld_body": jsonld_body(t)}
    print(json.dumps(row, ensure_ascii=False))
