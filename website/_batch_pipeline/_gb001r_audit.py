#!/usr/bin/env python3
"""Audit gbatch_001 slugs against the GEO/SEO standard."""
import re, os, sys, json

BASE = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
LANGS = [
    ("blog/articles", "en", 2500),
    ("zh-cn/blog/articles", "zh-cn", 3500),
    ("zh-tw/blog/articles", "zh-tw", 3500),
]

def read(p):
    try: return open(p, encoding="utf-8").read()
    except Exception: return None

def article_block(h):
    m = re.search(r'id="article-content"[\s\S]*?</article>', h, flags=re.I)
    if m: return m.group(0)
    m = re.search(r"<article\b[\s\S]*?</article>", h, flags=re.I)
    return m.group(0) if m else h

def plain(a):
    t = re.sub(r"<script[\s\S]*?</script>", " ", a, flags=re.I)
    t = re.sub(r"<style[\s\S]*?</style>", " ", t, flags=re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"&[a-zA-Z#0-9]+;", " ", t)
    return t

def wc_en(t): return len(re.findall(r"[A-Za-z0-9]+(?:['\-][A-Za-z0-9]+)*", t))
def cjk(t): return len(re.findall(r"[\u4e00-\u9fff\u3400-\u4dbf]", t))

QH2_EN = re.compile(r"^(how|what|why|when|which|where|who|can|do|does|did|is|are|should|will|would|must|need)", re.I)
QH2_ZH = re.compile(r"(如何|什么是|為什麼|为什么|怎麼|怎么|是否|怎樣|怎样|為何|为何|何時|何时|哪些|哪裡|哪里|什麼|什么|為什)", re.I)

def h2s(a):
    return [re.sub(r"<[^>]+>", "", x).strip() for x in re.findall(r"<h2\b[^>]*>([\s\S]*?)</h2>", a, flags=re.I)]

def qmark(x, lang):
    if x.endswith("?") or x.endswith("？"): return True
    return bool(QH2_EN.match(x)) if lang == "en" else bool(QH2_ZH.search(x))

def faq_block(a):
    m = re.search(r'class="[^"]*faq-section[^"]*"[\s\S]*?\n\s*</section>', a, flags=re.I)
    if m: return m.group(0), m.end()
    m = re.search(r'<section class="faq-section"[\s\S]*?</section>', a, flags=re.I)
    if m: return m.group(0), m.end()
    return "", -1

def faq_qs(fb):
    n_h3 = len(re.findall(r"<h3\b[^>]*>", fb, flags=re.I))
    n_btn = len(re.findall(r'class="faq-question"', fb, flags=re.I))
    return n_h3, n_btn

def jsonld_locs(h):
    head_end = h.lower().find("</head>")
    out = []
    for m in re.finditer(r'<script type="application/ld\+json"[^>]*>([\s\S]*?)</script>', h, flags=re.I):
        t = re.search(r'"@type"\s*:\s*"([^"]+)"', m.group(1))
        if t and t.group(1).lower() == "faqpage":
            out.append("H" if (head_end >= 0 and m.start() < head_end) else "B")
    return out

def cta(h, lang):
    if not re.search(r'class="[^"]*article-cta-btn[^"]*"', h, flags=re.I): return "NO_BTN"
    phrase = {"en": "Book a Demo", "zh-cn": "预约演示", "zh-tw": "預約示範"}[lang]
    return "ok" if phrase in h else "NO_PHRASE"

slugs = [l.strip() for l in open(os.path.join(BASE, "_batch_pipeline/gap_batches/gbatch_001.txt")) if l.strip()]
n = 0
print(f"{'slug':50} {'lang':6} {'st':6} {'metric':>7} {'floor':>6} {'faqH3':>6} {'faqBtn':>7} {'ld':>10} {'h2':>10} {'cta':>10}")
for s in slugs:
    for sub, lang, floor in LANGS:
        p = os.path.join(BASE, sub, s + ".html")
        h = read(p)
        n += 1
        if h is None:
            print(f"{s[:50]:50} {lang:6} {'MISSING':6}"); continue
        a = article_block(h); t = plain(a)
        m = wc_en(t) if lang == "en" else cjk(t)
        hs = h2s(a)
        q = sum(1 for x in hs if qmark(x, lang))
        fb, fend = faq_block(a)
        h3, btn = faq_qs(fb)
        ld = "".join(jsonld_locs(h)) or "-"
        print(f"{s[:50]:50} {lang:6} {'OK' if m>=floor else 'BELOW':6} {m:7} {floor:6} {h3:6} {btn:7} {ld:>10} {str(q)+'/'+str(len(hs)):>10} {cta(h,lang):>10}")
print("rows:", n)
