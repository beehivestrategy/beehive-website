#!/usr/bin/env python3
"""Generate batch-what-is.json with all 20 What Is articles."""
import json, os, sys

WORK = "/Users/kennethkwok/.trae-cn/work/6a5bc5758319ac256488b1d8"
OUT = os.path.join(WORK, "batch-what-is.json")

def A(slug, date, section, tags, rt, t, d, k, b, tl, faq):
    return {"date":date,"slug":slug,"section":section,"tags":tags,"readingTime":rt,
            "title":t,"description":d,"keywords":k,"body":b,"tldr":tl,"faq":faq}

articles = []
sys.path.insert(0, WORK)
from what_is_parts import get_articles as get_rest
articles.extend(get_rest())

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)
print(f"Written {len(articles)} articles")
