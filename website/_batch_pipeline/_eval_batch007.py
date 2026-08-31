import re, os, glob

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"

slugs = open(os.path.join(ROOT, "_batch_pipeline/batches/batch_007.txt"), encoding="utf-8").read().split()

CJK_RE = re.compile(r'[\u3400-\u9fff\uf900-\ufaff]')

def strip_tags(s):
    s = re.sub(r'<script.*?</script>', ' ', s, flags=re.S)
    s = re.sub(r'<style.*?</style>', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'&[a-z]+;', ' ', s)
    s = re.sub(r'&#\d+;', ' ', s)
    return s

def analyze(path):
    if not os.path.exists(path):
        return {"exists": False}
    h = open(path, encoding="utf-8").read()
    res = {"exists": True, "path": path}
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', h, re.S)
    body = m.group(1) if m else ''
    text = strip_tags(body)
    res["words"] = len(text.split())
    res["cjk"] = len(CJK_RE.findall(text))
    # FAQ
    faq_sec = re.search(r'class="faq-section"', h)
    res["faq_section"] = bool(faq_sec)
    res["faq_items"] = len(re.findall(r'class="faq-item"', h))
    res["h3_q"] = len(re.findall(r'<h3[^>]*faq-question-text', h))
    # JSON-LD FAQPage in body (after faq section) - count all FAQPage
    faq_jsons = re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    res["faqpage_ld"] = 0
    res["faqpage_mainentity"] = 0
    for j in faq_jsons:
        if '"FAQPage"' in j or '"@type":"FAQPage"' in j:
            res["faqpage_ld"] += 1
            me = re.search(r'"mainEntity"\s*:\s*\[(.*)\]', j, re.S)
            if me:
                res["faqpage_mainentity"] += len(re.findall(r'"@type"\s*:\s*"Question"', me.group(1)))
    # question H2s
    h2s = re.findall(r'<h2[^>]*id="[^"]+"[^>]*>(.*?)</h2>', body, re.S)
    h2s = [strip_tags(x).strip() for x in h2s]
    h2s = [x for x in h2s if x and 'faq-section-title' not in x.lower()]
    res["h2_count"] = len(h2s)
    res["h2_question"] = sum(1 for x in h2s if x.rstrip().endswith('?') or x.rstrip().endswith('？'))
    # CTA
    res["cta_btn"] = bool(re.search(r'class="article-cta-btn"', h))
    # recommended hrefs language check
    cards = re.findall(r'<a[^>]*(?:class="recommended-card"[^>]*href="([^"]+)"|href="([^"]+)"[^>]*class="recommended-card")', h)
    cards = [a or b for a,b in cards]
    res["rec_cards"] = len(cards)
    res["rec_bad_href"] = [c for c in cards if not (c.startswith('/blog/') or c.startswith('/zh-cn/') or c.startswith('/zh-tw/'))]
    return res

for slug in slugs:
    paths = {
        "en": os.path.join(ROOT, f"blog/articles/{slug}.html"),
        "zh-cn": os.path.join(ROOT, f"zh-cn/blog/articles/{slug}.html"),
        "zh-tw": os.path.join(ROOT, f"zh-tw/blog/articles/{slug}.html"),
    }
    print("="*80)
    print("SLUG:", slug)
    for lang, p in paths.items():
        r = analyze(p)
        if not r["exists"]:
            print(f"  [{lang}] MISSING")
            continue
        issues = []
        if lang == "en":
            if r["words"] < 2500: issues.append(f"WORDS {r['words']}<2500")
        else:
            if r["cjk"] < 3500: issues.append(f"CJK {r['cjk']}<3500")
        if r["faq_items"] < 3: issues.append(f"FAQitems {r['faq_items']}<3")
        if r["faqpage_ld"] < 1: issues.append("noFAQ-LD")
        elif r["faqpage_mainentity"] < 3: issues.append(f"LD-Q {r['faqpage_mainentity']}<3")
        if r["h2_count"] == 0: issues.append("noH2")
        elif r["h2_question"] < 1: issues.append("noQ-H2")
        if not r["cta_btn"]: issues.append("noCTA")
        if r["rec_bad_href"]: issues.append(f"badRecHref {r['rec_bad_href']}")
        status = "OK" if not issues else "FIX: " + "; ".join(issues)
        w = r["words"]; c = r["cjk"]
        print(f"  [{lang}] w={w} cjk={c} faq={r['faq_items']} h3q={r['h3_q']} ld={r['faqpage_ld']}(me={r['faqpage_mainentity']}) h2={r['h2_count']}(q={r['h2_question']}) cta={r['cta_btn']} rec={r['rec_cards']} -> {status}")
