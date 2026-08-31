#!/usr/bin/env python3
"""Insert a prose block before the FAQ section for one article, with optional
s2t conversion for zh-tw. Measures prose-before-FAQ (words for EN, CJK for zh)."""
import sys, re, os
import opencc

BASE = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
slug = sys.argv[1]
lang = sys.argv[2]          # en | zh-cn | zh-tw
prose_file = sys.argv[3]
rel = {"en": "blog/articles",
       "zh-cn": "zh-cn/blog/articles",
       "zh-tw": "zh-tw/blog/articles"}[lang]
path = os.path.join(BASE, rel, slug + ".html")
html = open(path, encoding="utf-8").read()
prose = open(prose_file, encoding="utf-8").read().strip()
if lang == "zh-tw":
    prose = opencc.OpenCC("s2t").convert(prose)

is_zh = lang in ("zh-cn", "zh-tw")
def cnt(s):
    return len(re.findall(r"[\u3400-\u9fff\uf900-\ufaff]", s)) if is_zh else len(re.findall(r"[A-Za-z0-9']+", s))

m = re.search(r'<article id="article-content">(.*?)</article>', html, re.S)
body = m.group(1) if m else html
idx = body.find('<section class="faq-section"')
before = cnt(re.sub(r"<[^>]+>", " ", body[:idx]))

marker = '<section class="faq-section"'
mi = html.find(marker)
assert mi != -1, "FAQ marker not found"
html = html[:mi] + "\n" + prose + "\n\n" + html[mi:]
open(path, "w", encoding="utf-8").write(html)

m2 = re.search(r'<article id="article-content">(.*?)</article>', html, re.S)
body2 = m2.group(1) if m2 else html
idx2 = body2.find('<section class="faq-section"')
after = cnt(re.sub(r"<[^>]+>", " ", body2[:idx2]))
unit = "CJK" if is_zh else "words"
print(f"[{lang}] {slug}: before={before} after={after} (+{after-before}) {unit}  -> {'OK' if after>=(3500 if is_zh else 2500) else 'STILL LOW'}")
