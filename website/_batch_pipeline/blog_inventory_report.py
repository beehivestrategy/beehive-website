#!/usr/bin/env python3
"""Local-source inventory: blog count, publish-day distribution, and character
counts per language (en=blog/articles, zh-cn=zh-cn/blog/articles, zh-tw=zh-tw/blog/articles)."""
import os, re, json, glob
from collections import defaultdict, Counter

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
LANGS = {
    "en":    os.path.join(ROOT, "blog/articles"),
    "zh-CN": os.path.join(ROOT, "zh-cn/blog/articles"),
    "zh-TW": os.path.join(ROOT, "zh-tw/blog/articles"),
}
DATE_RE = re.compile(r'<meta\s+property=["\']article:published_time["\']\s+content=["\']([^"\']+)', re.I)

def strip_tags(html):
    html = re.sub(r'<script.*?</script>', ' ', html, flags=re.S|re.I)
    html = re.sub(r'<style.*?</style>', ' ', html, flags=re.S|re.I)
    txt = re.sub(r'<[^>]+>', ' ', html)
    txt = re.sub(r'&[a-z]+;', ' ', txt)
    txt = re.sub(r'\s+', ' ', txt)
    return txt.strip()

report = {}
per_day_all = Counter()
per_day_lang = {l: Counter() for l in LANGS}
lang_stats = {}

for lang, d in LANGS.items():
    files = sorted(glob.glob(os.path.join(d, "*.html")))
    n = len(files)
    total_chars_file = 0
    total_chars_body = 0
    dates = []
    missing_date = 0
    for f in files:
        html = open(f, encoding="utf-8", errors="replace").read()
        total_chars_file += len(html)
        total_chars_body += len(strip_tags(html))
        m = DATE_RE.search(html)
        if m:
            ds = m.group(1)[:10]  # YYYY-MM-DD
            dates.append(ds)
            per_day_all[ds] += 1
            per_day_lang[lang][ds] += 1
        else:
            missing_date += 1
    lang_stats[lang] = {
        "count": n,
        "total_chars_file": total_chars_file,
        "avg_chars_file": total_chars_file // n if n else 0,
        "total_chars_body": total_chars_body,
        "avg_chars_body": total_chars_body // n if n else 0,
        "with_date": len(dates),
        "missing_date": missing_date,
        "date_min": min(dates) if dates else None,
        "date_max": max(dates) if dates else None,
    }

# serialize Counter keys (dates) to plain strings for JSON
per_day_all_s = {k: per_day_all[k] for k in sorted(per_day_all)}
per_day_lang_s = {l: {k: per_day_lang[l][k] for k in sorted(per_day_lang[l])} for l in LANGS}

summary = {
    "lang_stats": lang_stats,
    "per_day_all": per_day_all_s,
    "per_day_lang": per_day_lang_s,
    "total_articles": sum(s["count"] for s in lang_stats.values()),
    "distinct_publish_days": len(per_day_all_s),
}
out = os.path.join(ROOT, "_batch_pipeline/blog_inventory.json")
json.dump(summary, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# console summary
print("=== BLOG INVENTORY (LOCAL SOURCE) ===")
for lang in LANGS:
    s = lang_stats[lang]
    print(f"\n[{lang}]")
    print(f"  articles          : {s['count']:,}")
    print(f"  total chars (file): {s['total_chars_file']:,}  avg/article: {s['avg_chars_file']:,}")
    print(f"  total chars (body): {s['total_chars_body']:,}  avg/article: {s['avg_chars_body']:,}")
    print(f"  with date         : {s['with_date']:,}  missing: {s['missing_date']}")
    print(f"  date span         : {s['date_min']} -> {s['date_max']}")
print(f"\nTOTAL ARTICLES: {summary['total_articles']:,}  | distinct publish days: {len(per_day_all_s)}")
print(f"wrote {out}")
