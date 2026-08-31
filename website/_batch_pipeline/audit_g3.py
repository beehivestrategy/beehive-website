#!/usr/bin/env python3
import re, os, sys, json

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
LANGS = {"EN": "", "zh-CN": "zh-cn/", "zh-TW": "zh-tw/"}

CJK = re.compile(r'[\u4e00-\u9fff]')
WORD = re.compile(r"[A-Za-z][A-Za-z'\-]*")

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def body_of(html):
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', html, re.S)
    return m.group(1) if m else ""

def body_of_any(html):
    m = body_of(html)
    if m: return m
    m = re.search(r'<main[^>]*>(.*?)</main>', html, re.S)
    return m.group(1) if m else ""

def strip_tags(h):
    h = re.sub(r'<script.*?</script>', ' ', h, flags=re.S)
    h = re.sub(r'<style.*?</style>', ' ', h, flags=re.S)
    h = re.sub(r'<[^>]+>', ' ', h)
    return h

def count_words(h):
    t = strip_tags(h)
    return len(WORD.findall(t))

def count_cjk(h):
    t = strip_tags(h)
    return len(CJK.findall(t))

def audit(slug):
    out = {"slug": slug, "langs": {}}
    for lang, pre in LANGS.items():
        p = os.path.join(ROOT, pre + "blog/articles/" + slug + ".html")
        if not os.path.exists(p):
            out["langs"][lang] = {"missing": True}
            continue
        html = read(p)
        b = body_of_any(html)
        faq = re.search(r'<div[^>]*class="faq-section".*?</div>\s*(?=<)', html, re.S)
        faq_h3 = len(re.findall(r'<h3', b)) if b else 0
        # faq section h3
        fm = re.search(r'class="faq-section"(.*?)(?=<div[^>]*class="(?:article-cta|recommended)|<section|<footer|$)', html, re.S)
        nq = 0
        if fm:
            nq = len(re.findall(r'<h3[^>]*>(.*?)</h3>', fm.group(1), re.S))
        ld = re.findall(r'"@type"\s*:\s*"FAQPage"', html)
        # where is jsonld
        inbody = False
        for m in re.finditer(r'<script type="application/ld\+json".*?</script>', html, re.S):
            if 'FAQPage' in m.group(0):
                head_end = html.find('</head>')
                inbody = m.start() > head_end if head_end>0 else True
        cta = re.findall(r'class="[^"]*article-cta-btn[^"]*"', html)
        h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', b, re.S)
        cards = re.findall(r'<a[^>]*class="[^"]*recommended-card[^"]*"[^>]*href="([^"]*)"', html)
        excerpts = re.findall(r'class="recommended-card-excerpt"[^>]*>(.*?)</', html, re.S)
        empty_ex = sum(1 for e in excerpts if len(re.sub(r'\s|&nbsp;', '', strip_tags(e)))==0)
        out["langs"][lang] = {
            "words": count_words(b),
            "cjk": count_cjk(b),
            "faq_q": nq,
            "h3_total": faq_h3,
            "jsonld": len(ld),
            "jsonld_in_body": inbody,
            "cta": len(cta),
            "h2": [re.sub(r'<[^>]+>','',h).strip()[:60] for h in h2s],
            "cards": len(cards),
            "bad_cards": [c for c in cards if not c.startswith('/')],
            "empty_excerpts": empty_ex,
            "undef": html.count('undefined'),
            "bytes": len(html),
        }
    return out

slugs = [l.strip() for l in open(os.path.join(ROOT,"_batch_pipeline/gap_batches/gbatch_003.txt")) if l.strip()]
res = [audit(s) for s in slugs]
for r in res:
    print("="*70)
    print(r["slug"])
    for lang in ["EN","zh-CN","zh-TW"]:
        d = r["langs"][lang]
        if d.get("missing"): print("  ",lang,"MISSING"); continue
        print(f"  {lang}: words={d['words']} cjk={d['cjk']} faqQ={d['faq_q']} h3={d['h3_total']} jsonld={d['jsonld']}(body={d['jsonld_in_body']}) cta={d['cta']} cards={d['cards']} bad={d['bad_cards']} emptyEx={d['empty_excerpts']} undef={d['undef']}")
        print(f"      H2({len(d['h2'])}): {d['h2']}")
