#!/usr/bin/env python3
import os, re, sys, json
ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
SLUGS = [l.strip() for l in open(os.path.join(ROOT,"_batch_pipeline/gap_batches/gbatch_001.txt")) if l.strip()]

def cjk(s): return len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', s))
def wc(s):
    s=re.sub(r'<[^>]+>',' ',s); s=re.sub(r'&[a-z]+;',' ',s); s=re.sub(r'&#\d+;',' ',s)
    return len(s.split())

def body(html):
    m=re.search(r'<article class="article-content" id="article-content">(.*?)</article>', html, re.S)
    if m: return m.group(1)
    m=re.search(r'<article[^>]*>(.*?)</article>', html, re.S)
    return m.group(1) if m else html

def faqld(html):
    n=0; ok=False
    for ld in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        if '"FAQPage"' in ld:
            try:
                o=json.loads(ld)
                if isinstance(o,dict) and "@graph" in o:
                    o=[x for x in o["@graph"] if x.get("@type")=="FAQPage"]
                    o=o[0] if o else {}
                me=o.get("mainEntity",[])
                n=len(me) if isinstance(me,list) else 0
                ok=True
            except Exception as e:
                ok=False
    return ok, n

def cta(html):
    if 'class="article-cta-btn"' not in html: return "NOBTN"
    m=re.search(r'<a[^>]*class="article-cta-btn"[^>]*>(.*?)</a>', html, re.S)
    t=re.sub(r'<[^>]+>','',m.group(1)).strip() if m else ""
    return t or "EMPTY"

for s in SLUGS:
    row=[s]
    for lang,sub,phrase in (("EN","blog/articles","Book a Demo"),("zh-CN","zh-cn/blog/articles","预约演示"),("zh-TW","zh-tw/blog/articles","預約示範")):
        p=os.path.join(ROOT,sub,s+".html")
        if not os.path.exists(p):
            row.append(f"{lang}:MISSING"); continue
        h=open(p,encoding="utf-8").read()
        b=body(h)
        val = wc(b) if lang=="EN" else cjk(b)
        thr = 2500 if lang=="EN" else 3500
        faq_n = len(re.findall(r'<section class="faq-section"', h))
        h3 = len(re.findall(r'<h3', b))
        ok,ldn = faqld(h)
        ct = cta(h)
        h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', b, re.S)
        qh2 = sum(1 for x in h2s if re.sub(r'<[^>]+>','',x).strip().endswith(('?','？')))
        flags=[]
        if val<thr: flags.append("SHORT")
        if faq_n==0: flags.append("NOFAQ")
        if h3<3: flags.append(f"H3={h3}")
        if not ok: flags.append("NOLD")
        elif ldn<3: flags.append(f"LD={ldn}")
        if phrase not in ct: flags.append(f"CTA={ct}")
        if qh2 < len(h2s): flags.append(f"QH2 {qh2}/{len(h2s)}")
        row.append(f"{lang} {val} {'OK' if not flags else '|'.join(flags)}")
    print(" :: ".join(row))
