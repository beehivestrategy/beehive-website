#!/usr/bin/env python3
"""Scan for files containing MORE THAN ONE FAQPage JSON-LD block (SEO-duplicate schema)."""
import os, re, glob, json
from collections import defaultdict

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
LANGS = {"en": "blog/articles", "cn": "zh-cn/blog/articles", "tw": "zh-tw/blog/articles"}

# all article html
files = []
for d in LANGS.values():
    files += glob.glob(os.path.join(ROOT, d, "*.html"))

ld_re = re.compile(r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>', re.S | re.I)
faq_re = re.compile(r'"@type"\s*:\s*"FAQPage"')

dupe = defaultdict(list)  # filepath -> count of faqpage blocks
for f in files:
    try:
        html = open(f, encoding="utf-8").read()
    except Exception:
        continue
    blocks = ld_re.findall(html)
    faq_count = sum(1 for b in blocks if faq_re.search(b))
    if faq_count > 1:
        dupe[f] = faq_count

print(f"Total article files scanned: {len(files)}")
print(f"Files with >1 FAQPage JSON-LD block: {len(dupe)}")
total_extra = sum(c - 1 for c in dupe.values())
print(f"Total redundant FAQPage blocks to remove: {total_extra}")
# breakdown by lang
by_lang = defaultdict(int)
for f in dupe:
    if "/blog/articles/" in f: by_lang["en"] += 1
    elif "/zh-cn/" in f: by_lang["cn"] += 1
    elif "/zh-tw/" in f: by_lang["tw"] += 1
print("By language:", dict(by_lang))
# sample
for i, (f, c) in enumerate(list(dupe.items())[:10]):
    print(f"  [{c}x] ...{f.split('website')[-1]}")
