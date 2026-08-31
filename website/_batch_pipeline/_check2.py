#!/usr/bin/env python3
"""Accurate compliance measurement for article files.

Fixes over _check.py:
- Matches <article ...id="article-content"> with any attribute order (old regex
  only matched the bare form and silently fell back to scanning the whole file,
  including <head> JSON-LD text).
- Strips <script>/<style> content before counting so JSON-LD is never counted
  as prose.
- Reports prose both BEFORE the FAQ block and for the whole article body.
"""
import re, sys, os

SLUGS = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
BASE = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
LANGS = [
    ("en", "blog/articles"),
    ("zh-cn", "zh-cn/blog/articles"),
    ("zh-tw", "zh-tw/blog/articles"),
]
CTA = {"en": "Book a Demo", "zh-cn": "预约演示", "zh-tw": "預約示範"}

ART_RE = re.compile(r'<article\b[^>]*id="article-content"[^>]*>(.*?)</article>', re.S)
FAQ_RE = re.compile(r'<section\b[^>]*class="[^"]*faq-section[^"]*"[^>]*>.*?</section>', re.S)


def clean(s):
    s = re.sub(r"<script\b.*?</script>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<style\b.*?</style>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    return re.sub(r"<[^>]+>", " ", s)


def cjk(s):
    return len(re.findall(r"[\u3400-\u9fff\uf900-\ufaff]", s))


def words(s):
    return len(re.findall(r"[A-Za-z0-9']+", s))


rows = []
for slug in SLUGS:
    for lang, rel in LANGS:
        path = os.path.join(BASE, rel, slug + ".html")
        if not os.path.exists(path):
            rows.append((slug, lang, "MISSING", 0, 0, 0, False, False))
            continue
        html = open(path, encoding="utf-8").read()
        m = ART_RE.search(html)
        found = bool(m)
        body = m.group(1) if m else ""
        fm = FAQ_RE.search(body)
        before = body[: fm.start()] if fm else body
        count = words if lang == "en" else cjk
        floor = 2500 if lang == "en" else 3500
        n_before = count(clean(before))
        n_total = count(clean(FAQ_RE.sub(" ", body)))
        faq_items = 0
        if fm:
            blk = fm.group(0)
            faq_items = len(re.findall(r'class="faq-question"', blk)) or len(re.findall(r"<h3", blk))
        # FAQPage JSON-LD located in the BODY (after </head>)
        cut = html.find("</head>")
        bodypart = html[cut:] if cut != -1 else html
        jsonld = bool(re.search(r'"@type"\s*:\s*"FAQPage"', bodypart))
        # placement: immediately after FAQ section close
        placed_after = False
        if fm:
            tail = body[fm.end():]
            placed_after = bool(re.match(r'\s*<script[^>]*application/ld\+json[^>]*>\s*\{', tail))
        cta = CTA[lang] in html
        rows.append((slug, lang, "ok" if found else "NOART", n_before, n_total, faq_items, jsonld, cta, floor, placed_after))

fails = 0
for r in rows:
    if r[2] == "MISSING":
        print(f"{r[0][:46]:46} [{r[1]:5}] MISSING FILE")
        fails += 1
        continue
    slug, lang, st, nb, nt, faq, jl, cta, floor, pa = r
    ok = nt >= floor and faq >= 3 and jl and cta
    if not ok:
        fails += 1
    flag = "PASS" if ok else "FAIL"
    print(f"{slug[:46]:46} [{lang:5}] {flag} total={nt:5} (pre-faq={nb:5}, need>={floor}) faq={faq} jsonld={'y' if jl else 'n'} after-faq={'y' if pa else 'n'} cta={'y' if cta else 'n'} art={st}")
print(f"\n{len(rows)-fails}/{len(rows)} pass, {fails} fail")
