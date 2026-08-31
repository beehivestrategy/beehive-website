import re, sys, json, os
ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"

def body(html):
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', html, re.S)
    return m.group(1) if m else ""

def strip_tags(s):
    s = re.sub(r'<script.*?</script>', ' ', s, flags=re.S)
    s = re.sub(r'<style.*?</style>', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'&nbsp;', ' ', s)

def en_words(h):
    return len(re.findall(r"[A-Za-z][A-Za-z'\-]*", strip_tags(body(h))))

def cjk(h):
    return len(re.findall(r'[\u4e00-\u9fff]', strip_tags(body(h))))

def faqsec(h):
    b = body(h)
    m = re.search(r'class="faq-section".*?</section>', b, re.S)
    return m.group(0) if m else ""

def faq_n(h):
    s = faqsec(h)
    return len(re.findall(r'<h3 class="faq-question-title"', s))

def faq_items(h):
    return len(re.findall(r'class="faq-item"', faqsec(h)))

def info(h):
    return {
        "w": en_words(h),
        "cjk": cjk(h),
        "faq": faq_n(h),
        "ld": len(re.findall(r'"@type"\s*:\s*"FAQPage"', h)),
        "cta": h.count('article-cta-btn'),
        "rec": len(re.findall(r'<a [^>]*class="recommended-card"', h)),
        "recbad": [a for a in re.findall(r'<a href="([^"]*)"[^>]*class="recommended-card"', h)
                   if not a.startswith('/blog/articles/') and not a.startswith('/zh-cn/blog/') and not a.startswith('/zh-tw/blog/')],
        "h2q": len(re.findall(r'<h2[^>]*>', body(h))),
    }

for slug in [l.strip() for l in open(sys.argv[1]) if l.strip()]:
    out = {"slug": slug}
    for lang, pref in (("EN",""), ("CN","zh-cn/"), ("TW","zh-tw/")):
        p = os.path.join(ROOT, pref + "blog/articles/" + slug + ".html")
        if not os.path.exists(p):
            out[lang] = "MISSING"; continue
        h = open(p, encoding="utf-8").read()
        d = info(h)
        d["fitem"] = faq_items(h)
        d["fsec"] = 1 if faqsec(h) else 0
        if lang == "EN": d.pop("cjk")
        else: d.pop("w")
        out[lang] = d
    print(json.dumps(out, ensure_ascii=False))
