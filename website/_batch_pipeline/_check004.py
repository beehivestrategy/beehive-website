#!/usr/bin/env python3
"""Accurate compliance measurement for batch 004.

Handles both article wrappers (<article id="article-content"> and
<article class="article-content" id="...">), strips script/style/nav/toc,
and measures prose BEFORE the FAQ section.
"""
import os
import re
import sys

LANGS = [("en", "blog/articles"), ("zh-cn", "zh-cn/blog/articles"), ("zh-tw", "zh-tw/blog/articles")]
CTA = {"en": "Book a Demo", "zh-cn": "预约演示", "zh-tw": "預約示範"}
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def article_region(html):
    m = re.search(r"<article\b[^>]*>", html)
    if not m:
        return html
    start = m.end()
    end = html.find("</article>", start)
    return html[start: end if end != -1 else len(html)]


def prose_text(html):
    art = article_region(html)
    i = art.find('<section class="faq-section"')
    if i != -1:
        art = art[:i]
    art = re.sub(r"<script.*?</script>", " ", art, flags=re.S)
    art = re.sub(r"<style.*?</style>", " ", art, flags=re.S)
    art = re.sub(r"<aside.*?</aside>", " ", art, flags=re.S)
    art = re.sub(r"<nav.*?</nav>", " ", art, flags=re.S)
    art = re.sub(r"<[^>]+>", " ", art)
    return re.sub(r"\s+", " ", art)


def en_words(t):
    return len(re.findall(r"[A-Za-z0-9']+", t))


def cjk(t):
    return len(re.findall(r"[\u3400-\u9fff\uf900-\ufaff]", t))


def faq_info(html):
    i = html.find('<section class="faq-section"')
    if i == -1:
        return 0, False
    depth = 0
    end = len(html)
    for m in re.finditer(r"<section\b|</section>", html[i:]):
        if m.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                end = i + m.end()
                break
        else:
            depth += 1
    block = html[i:end]
    n = len(re.findall(r'<div class="faq-item', block))
    h3 = len(re.findall(r"<h3", block))
    return (n or h3), h3 >= 3


def main(listfile):
    slugs = [l.strip() for l in open(listfile, encoding="utf-8") if l.strip()]
    fails = 0
    for slug in slugs:
        rows = []
        for lang, rel in LANGS:
            p = os.path.join(BASE, rel, slug + ".html")
            if not os.path.exists(p):
                rows.append(f"  [{lang}] MISSING")
                fails += 1
                continue
            html = open(p, encoding="utf-8").read()
            t = prose_text(html)
            n = en_words(t) if lang == "en" else cjk(t)
            floor = 2500 if lang == "en" else 3500
            nfaq, has_h3 = faq_info(html)
            body = html[html.find("</head>"):] if "</head>" in html else html
            jb = '"FAQPage"' in body.replace(" ", "")
            cta = CTA[lang] in html
            ok = n >= floor and nfaq >= 3 and has_h3 and jb and cta
            if not ok:
                fails += 1
            rows.append(
                f"  [{lang}] {n}/{floor} {'OK ' if n >= floor else 'LOW'} | faq={nfaq} h3={'y' if has_h3 else 'n'}"
                f" | ld_body={'y' if jb else 'n'} | cta={'y' if cta else 'n'} | {'PASS' if ok else 'FAIL'}"
            )
        print(slug)
        print("\n".join(rows))
    print(f"\nTOTAL FAILING FILES: {fails}")


if __name__ == "__main__":
    main(sys.argv[1])
