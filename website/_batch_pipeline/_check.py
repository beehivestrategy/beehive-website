#!/usr/bin/env python3
"""Measure compliance of target article files.
For each file: prose words (EN) or CJK chars (zh) in the article body BEFORE the FAQ marker,
FAQ item count, JSON-LD presence in <head> and in <body>, CTA phrase presence.
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

def cjk_count(s):
    return len(re.findall(r"[\u3400-\u9fff\uf900-\ufaff]", s))

def en_count(s):
    return len(re.findall(r"[A-Za-z0-9']+", s))

def strip_tags(s):
    return re.sub(r"<[^>]+>", " ", s)

for slug in SLUGS:
    print("="*70)
    print("SLUG:", slug)
    for lang, rel in LANGS:
        path = os.path.join(BASE, rel, slug + ".html")
        if not os.path.exists(path):
            print(f"  [{lang}] MISSING {path}")
            continue
        html = open(path, encoding="utf-8").read()
        # article body region
        m = re.search(r'<article id="article-content">(.*?)</article>', html, re.S)
        body = m.group(1) if m else html
        idx = body.find('<section class="faq-section"')
        prose = body[:idx] if idx != -1 else body
        text = strip_tags(prose)
        if lang == "en":
            n = en_count(text)
            metric = f"{n} words (need >=2500)"
            ok = n >= 2500
        else:
            n = cjk_count(text)
            metric = f"{n} CJK (need >=3500)"
            ok = n >= 3500
        # FAQ count: count faq-question buttons or h3 within faq-section
        faq_block = ""
        fm = re.search(r'<section class="faq-section".*?</section>', html, re.S)
        if fm:
            faq_block = fm.group(0)
        faq_items = len(re.findall(r'class="faq-question"', faq_block)) or len(re.findall(r"<h3", faq_block))
        # JSON-LD in head
        head = html[:html.find("</head>")] if "</head>" in html else ""
        jsonld_head = ('"@type":"FAQPage"' in head.replace(" ", "")) or ('"@type": "FAQPage"' in head)
        # JSON-LD in body (after </head>)
        body_part = html[html.find("</head>"):] if "</head>" in html else html
        jsonld_body = ('"@type":"FAQPage"' in body_part.replace(" ", "")) or ('"@type": "FAQPage"' in body_part)
        cta = CTA[lang] in html
        print(f"  [{lang}] {metric}  {'OK' if ok else 'NEED'} | FAQitems={faq_items} | JSONLD head={jsonld_head} body={jsonld_body} | CTA={cta}")
