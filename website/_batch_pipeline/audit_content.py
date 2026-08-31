#!/usr/bin/env python3
"""Content-based GEO/SEO compliance audit across all 1061 slugs x 3 langs.
Prints JSON summary + writes gaps list for fleet resume.
Run: python3 audit_content.py
"""
import os, re, glob, json
from collections import defaultdict

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
LANGS = {"en": "blog/articles", "cn": "zh-cn/blog/articles", "tw": "zh-tw/blog/articles"}

def read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""

def cjk_count(s):
    return len(re.findall(r"[\u4e00-\u9fff\u3400-\u4dbf]", s))

def body_text(html):
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', html, re.S|re.I)
    return m.group(1) if m else html

# Collect slugs from batch files
batch_dir = os.path.join(ROOT, "_batch_pipeline/batches")
batch_files = sorted(glob.glob(os.path.join(batch_dir, "batch_*.txt")))
slugs = []
seen = set()
for bf in batch_files:
    for line in open(bf, encoding="utf-8"):
        s = line.strip()
        if s and s not in seen:
            seen.add(s); slugs.append(s)

results = {}
for slug in slugs:
    rec = {}
    for lang, d in LANGS.items():
        html = read(os.path.join(ROOT, d, slug + ".html"))
        if not html:
            rec[lang] = {"err": "missing"}
            continue
        body = body_text(html)
        if lang == "en":
            wc = len(re.findall(r"\b\w+\b", body))
            rec[lang] = {"words": wc, "len_ok": wc >= 2500}
        else:
            cjk = cjk_count(body)
            rec[lang] = {"cjk": cjk, "len_ok": cjk >= 3500}
        faq = 'faq-section' in html
        jsonld = ('application/ld+json' in html) and ('"@type": "FAQPage"' in html or '"@type":"FAQPage"' in html)
        cta = 'article-cta-btn' in html
        rec[lang]["faq"] = faq
        rec[lang]["jsonld"] = jsonld
        rec[lang]["cta"] = cta
        # overall standard = length ok AND faq AND jsonld AND cta
        rec[lang]["ok"] = rec[lang]["len_ok"] and faq and jsonld and cta
    results[slug] = rec

# Aggregates
agg = {l: {"ok":0,"total":0,"len_fail":0,"faq_fail":0,"jsonld_fail":0,"cta_fail":0} for l in LANGS}
not_ok_slugs = []
for slug, rec in results.items():
    allok = True
    for l in LANGS:
        if rec[l].get("err"):
            allok = False; agg[l]["total"]+=1; continue
        agg[l]["total"] += 1
        if rec[l]["ok"]: agg[l]["ok"] += 1
        else:
            allok = False
            if not rec[l]["len_ok"]: agg[l]["len_fail"] += 1
            if not rec[l]["faq"]: agg[l]["faq_fail"] += 1
            if not rec[l]["jsonld"]: agg[l]["jsonld_fail"] += 1
            if not rec[l]["cta"]: agg[l]["cta_fail"] += 1
    if not allok:
        not_ok_slugs.append(slug)

print("=== AGGREGATE (per language) ===")
for l in LANGS:
    a = agg[l]
    print(f"  {l}: {a['ok']}/{a['total']} at standard | len_fail={a['len_fail']} faq_fail={a['faq_fail']} jsonld_fail={a['jsonld_fail']} cta_fail={a['cta_fail']}")
print(f"\nSlugs NOT fully at standard (any lang): {len(not_ok_slugs)} / {len(slugs)}")
print(f"Slugs fully at standard (all 3 langs): {len(slugs)-len(not_ok_slugs)} / {len(slugs)}")

# Sample the not-ok to sanity check
print("\n=== Sample of not-ok slugs (first 20) ===")
for s in not_ok_slugs[:20]:
    r = results[s]
    def flag(l):
        x = r[l]
        if x.get("err"): return "MISSING"
        return "+".join([t for t,(k) in [("LEN",x["len_ok"]),("FAQ",x["faq"]),("JSON",x["jsonld"]),("CTA",x["cta"])] if not k] or ["ok"])
    print(f"  {s}: en[{flag('en')}] cn[{flag('cn')}] tw[{flag('tw')}]")

with open(os.path.join(os.path.dirname(__file__), "gaps_audit.json"), "w", encoding="utf-8") as f:
    json.dump({"not_ok": not_ok_slugs, "results": results, "agg": agg}, f, ensure_ascii=False, indent=1)
print(f"\nWrote gaps_audit.json with {len(not_ok_slugs)} gap slugs.")
