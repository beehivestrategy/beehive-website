#!/usr/bin/env python3
import re, os, sys, json, html as H

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
LANGS = {"EN": "", "zh-CN": "zh-cn/", "zh-TW": "zh-tw/"}
CJK = re.compile(r'[\u4e00-\u9fff]')
WORD = re.compile(r"[A-Za-z][A-Za-z'\-]*")

def read(p):
    with open(p, encoding="utf-8") as f: return f.read()

def strip_tags(h):
    h = re.sub(r'<script.*?</script>', ' ', h, flags=re.S)
    h = re.sub(r'<style.*?</style>', ' ', h, flags=re.S)
    h = re.sub(r'<[^>]+>', ' ', h)
    return h

def audit(slug):
    row = {"slug": slug}
    for lang, pre in LANGS.items():
        p = os.path.join(ROOT, pre + "blog/articles/" + slug + ".html")
        if not os.path.exists(p):
            row[lang] = "MISSING"; continue
        s = read(p)
        body = ""
        m = re.search(r'(<article[^>]*id="article-content"[^>]*>)(.*?)(</article>)', s, re.S)
        if m: body = m.group(2)
        he = s.find('</head>')
        faq = re.search(r'(<section class="faq-section".*?</section>)', s, re.S)
        nq = 0; h3 = 0; qlist=[]
        if faq:
            qlist = re.findall(r'faq-question-text"><span class="faq-number">\d+</span><span>(.*?)</span>', faq.group(1), re.S)
            if not qlist:
                qlist = re.findall(r'<h3[^>]*>(.*?)</h3>', faq.group(1), re.S)
            nq = len(qlist)
            h3 = len(re.findall(r'<h3', faq.group(1)))
        # jsonld
        bodyld = 0; headld = 0; afterfaq = False
        for mm in re.finditer(r'<script type="application/ld\+json"[^>]*>.*?</script>', s, re.S):
            if 'FAQPage' not in mm.group(0): continue
            if he > 0 and mm.start() < he: headld += 1
            else:
                bodyld += 1
                if faq and mm.start() > faq.start(): afterfaq = True
        cards = re.findall(r'<a[^>]*class="[^"]*recommended-card[^"]*"[^>]*href="([^"]*)"', s)
        if not cards:
            cards = re.findall(r'<a href="([^"]*)"[^>]*class="[^"]*recommended-card[^"]*"', s)
        ex = re.findall(r'(<p class="recommended-card-excerpt"[^>]*>)(.*?)(</p>)', s, re.S)
        empty_ex = sum(1 for a,b,c in ex if len(re.sub(r'\s|&nbsp;','',strip_tags(b)))==0)
        undef = len(re.findall(r'>\s*undefined\s*<', s)) + len(re.findall(r'undefined', s))
        cta = re.findall(r'<a[^>]*class="[^"]*article-cta-btn[^"]*"[^>]*>(.*?)</a>', s, re.S)
        h2 = [re.sub(r'\s+',' ',strip_tags(x)).strip() for x in re.findall(r'<h2[^>]*>(.*?)</h2>', body, re.S)]
        row[lang] = {
            "words": len(WORD.findall(strip_tags(body))),
            "cjk": len(CJK.findall(strip_tags(body))),
            "faqQ": nq, "faqH3": h3, "headLD": headld, "bodyLD": bodyld, "ldAfterFaq": afterfaq,
            "cards": len(cards), "relCards": [c for c in cards if not c.startswith('/')],
            "emptyEx": empty_ex, "undef": undef, "cta": [strip_tags(c).strip() for c in cta],
            "h2n": len(h2),
        }
    return row

slugs = [l.strip() for l in open(os.path.join(ROOT,"_batch_pipeline/gap_batches/gbatch_003.txt")) if l.strip()]
for s in slugs:
    r = audit(s)
    print("="*78); print(r["slug"])
    for lang in ["EN","zh-CN","zh-TW"]:
        d = r[lang]
        if d == "MISSING": print(f"  {lang}: MISSING"); continue
        print(f"  {lang}: words={d['words']:5d} cjk={d['cjk']:5d} faqQ={d['faqQ']} faqH3={d['faqH3']} headLD={d['headLD']} bodyLD={d['bodyLD']} afterFaq={d['ldAfterFaq']} cards={d['cards']} rel={d['relCards']} emptyEx={d['emptyEx']} undef={d['undef']} h2={d['h2n']} cta={d['cta']}")
