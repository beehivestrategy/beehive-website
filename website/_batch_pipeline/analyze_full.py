import json, re, os, sys
from collections import Counter

BASE = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
STATUS = os.path.join(BASE, "_batch_pipeline/status.json")

with open(STATUS) as f:
    status = json.load(f)

slugs = list(status["slugs"].keys())

def read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None

def extract_article(html):
    if not html: return ""
    h = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    h = re.sub(r"<style[\s\S]*?</style>", " ", h, flags=re.I)
    # Preferred: the real prose container used by the harness
    m = re.search(r'id="article-content"[\s\S]*?</article>', h, flags=re.I)
    if m: return m.group(0)
    m = re.search(r'<article\b[^>]*class="article-content"[\s\S]*?</article>', h, flags=re.I)
    if m: return m.group(0)
    m = re.search(r"<article\b[\s\S]*?</article>", h, flags=re.I)
    if m: return m.group(0)
    m = re.search(r"<main\b[\s\S]*?</main>", h, flags=re.I)
    if m: return m.group(0)
    return h

def plain_text(art):
    t = re.sub(r"<[^>]+>", " ", art)
    t = re.sub(r"&[a-z]+;", " ", t)
    return t

def count_en(t):
    return len(re.findall(r"[A-Za-z0-9]+(?:['\-][A-Za-z0-9]+)*", t))

def count_zh(t):
    return len(re.findall(r"[一-鿿]", t))

def analyze_lang(html, lang):
    art = extract_article(html)
    t = plain_text(art)
    if lang == "en":
        wc = count_en(t)
        floor = 2500
    else:
        wc = count_zh(t)
        floor = 3500
    low = (html or "").lower()
    # FAQ section: harness uses class="faq-section" or Chinese heading
    has_faq_sec = ("faq-section" in low) or ("id=\"faq\"" in low) or ("常见问题" in (html or "")) or ("常見問題" in (html or ""))
    # FAQPage JSON-LD
    has_faq_json = ("\"@type\":\"faqpage\"" in low) or ("\"@type\": \"faqpage\"" in low)
    # CTA button
    has_cta = ("article-cta-btn" in low) or ("class=\"cta" in low) or ("cta-button" in low) or ("cta-section" in low)
    # demo phrase
    if lang == "en":
        has_demo = ("book a demo" in low) or ("book a personalised demo" in low) or ("book a personalized demo" in low)
    elif lang == "zh-cn":
        has_demo = ("预约演示" in (html or ""))
    else:
        has_demo = ("預約示範" in (html or "")) or ("预约演示" in (html or ""))
    # hreflang x4
    has_href = all(x in low for x in ['hreflang="en"', 'hreflang="zh-cn"', 'hreflang="zh-tw"', 'hreflang="x-default"'])
    # canonical
    has_canon = '<link rel="canonical"' in low or "<link rel='canonical'" in low
    # question-style H2
    h2s = re.findall(r"<h2\b[^>]*>([\s\S]*?)</h2>", art, flags=re.I)
    h2txt = " ".join(re.sub(r"<[^>]+>", "", h) for h in h2s)
    has_qh2 = ("?" in h2txt) or ("？" in h2txt)
    return dict(wc=wc, floor=floor, meet=wc>=floor, faq_sec=has_faq_sec, faq_json=has_faq_json,
                cta=has_cta, demo=has_demo, href4=has_href, canon=has_canon, qh2=has_qh2,
                h2count=len(h2s))

languages = ["en", "zh-cn", "zh-tw"]
subdir = {"en":"blog/articles", "zh-cn":"zh-cn/blog/articles", "zh-tw":"zh-tw/blog/articles"}

results = {s:{} for s in slugs}
per_lang = {l: dict(n=0, meet=0, wcs=[], faq_sec=0, faq_json=0, cta=0, demo=0, href4=0, canon=0, qh2=0) for l in languages}

for s in slugs:
    for l in languages:
        p = os.path.join(BASE, subdir[l], s + ".html")
        html = read(p)
        if html is None:
            results[s][l] = None
            continue
        a = analyze_lang(html, l)
        results[s][l] = a
        d = per_lang[l]
        d["n"] += 1
        d["wcs"].append(a["wc"])
        if a["meet"]: d["meet"] += 1
        if a["faq_sec"]: d["faq_sec"] += 1
        if a["faq_json"]: d["faq_json"] += 1
        if a["cta"]: d["cta"] += 1
        if a["demo"]: d["demo"] += 1
        if a["href4"]: d["href4"] += 1
        if a["canon"]: d["canon"] += 1
        if a["qh2"]: d["qh2"] += 1

def stats(wcs):
    wcs2 = sorted(wcs)
    n = len(wcs2)
    if n == 0: return dict(avg=0, median=0, mn=0, mx=0)
    avg = sum(wcs2)/n
    mid = wcs2[n//2]
    return dict(avg=round(avg), median=mid, mn=wcs2[0], mx=wcs2[-1])

summary = {}
for l in languages:
    d = per_lang[l]
    n = d["n"]
    st = stats(d["wcs"])
    geo = dict(faq_sec=round(100*d["faq_sec"]/n) if n else 0,
               faq_json=round(100*d["faq_json"]/n) if n else 0,
               cta=round(100*d["cta"]/n) if n else 0,
               demo=round(100*d["demo"]/n) if n else 0,
               href4=round(100*d["href4"]/n) if n else 0,
               canon=round(100*d["canon"]/n) if n else 0,
               qh2=round(100*d["qh2"]/n) if n else 0,
               meet=round(100*d["meet"]/n) if n else 0)
    summary[l] = dict(n=n, wc_stats=st, geo=geo)

# all-3-language GEO full pass (faq_sec+faq_json+cta+demo+href4+canon+qh2 all true AND all meet floor)
all3_pass = 0
all3_geo_pass = 0
for s in slugs:
    rs = results[s]
    if any(rs.get(l) is None for l in languages):
        continue
    meet_all = all(rs[l]["meet"] for l in languages)
    geo_all = all(rs[l]["faq_sec"] and rs[l]["faq_json"] and rs[l]["cta"] and rs[l]["demo"] and rs[l]["href4"] and rs[l]["canon"] and rs[l]["qh2"] for l in languages)
    if meet_all: all3_pass += 1
    if geo_all: all3_geo_pass += 1

out = dict(total=len(slugs), summary=summary, all3_floor_pass=all3_pass, all3_geo_pass=all3_geo_pass)
print(json.dumps(out, ensure_ascii=False, indent=2))
