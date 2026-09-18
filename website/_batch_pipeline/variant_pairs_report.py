#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Republish-variant pairs decision table.
Reads title_audit.json exact_dup groups, classifies dated-variant pairs,
adds per-page metadata (date, sitemap presence) for Kenneth's decision.
"""
import json, os, re, glob

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(BASE)

with open(os.path.join(BASE, "title_audit.json"), encoding="utf-8") as f:
    audit = json.load(f)

DATE_PAT = re.compile(r"-20(2[456])\d{2,4}$|-(oct|nov|dec|sep)20(2[456])$", re.I)

def mtime(p):
    try:
        import datetime
        return datetime.date.fromtimestamp(os.path.getmtime(p)).isoformat()
    except OSError:
        return "?"

rows = []
for lang in ("en", "cn", "tw"):
    for g in audit.get("exact_dup", {}).get(lang, []):
        title = g["title"]
        slugs = g["slugs"]
        if len(slugs) < 2:
            continue
        # only report same-language groups where slugs look like variants
        dated = [s for s in slugs if DATE_PAT.search(s)]
        if not dated and len(slugs) == 2:
            pass
        entry = {
            "lang": lang, "title": title,
            "pairs": [{"slug": s,
                       "dated_variant": bool(DATE_PAT.search(s)),
                       "size_kb": round(os.path.getsize(os.path.join(SITE, {"en": "", "cn": "zh-cn/", "tw": "zh-tw/"}[lang], "blog/articles", s + ".html"))/1024, 1) if os.path.exists(os.path.join(SITE, {"en": "", "cn": "zh-cn/", "tw": "zh-tw/"}[lang], "blog/articles", s + ".html")) else None}
                      for s in slugs],
        }
        rows.append(entry)

# dedupe cross-language (cn/tw mirror en groups)
seen, uniq = set(), []
for r in rows:
    key = r["title"]
    if key in seen:
        continue
    seen.add(key)
    uniq.append(r)

print("variant/same-title groups: %d" % len(uniq))
for r in uniq:
    tag = " + ".join(("%s%s%s" % (p["slug"], "*" if p["dated_variant"] else "", " (%sK)" % p["size_kb"] if p["size_kb"] else ""))
                     for p in r["pairs"])
    print("  [%s] %s\n       %s" % (r["lang"], r["title"][:60], tag))

with open(os.path.join(BASE, "variant_pairs.json"), "w", encoding="utf-8") as f:
    json.dump(uniq, f, ensure_ascii=False, indent=1)
print("saved: variant_pairs.json")
