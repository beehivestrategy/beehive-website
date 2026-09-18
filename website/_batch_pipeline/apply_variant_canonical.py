#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Variant option A: rel=canonical consolidation (LOW RISK).
For each variant group in variant_pairs_enriched.json, point the "drop" pages'
<link rel="canonical> at the "keep" page. Pages stay live; no deletion.
DO NOT RUN without Kenneth's approval.
  python3 apply_variant_canonical.py           # dry-run
  python3 apply_variant_canonical.py --apply
"""
import json, os, re, shutil, sys, time

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(BASE)
PAIRS = os.path.join(os.path.dirname(os.path.dirname(BASE)), "gsc_out", "variant_pairs_enriched.json")

LANG_DIR = {"en": "", "cn": "zh-cn/", "tw": "zh-tw/"}
def art_path(lang, slug):
    return os.path.join(SITE, LANG_DIR[lang], "blog", "articles", slug + ".html")

def canonical_url(lang, slug):
    if lang == "en":
        return "https://www.beehivestrategy.com/blog/articles/" + slug
    return "https://www.beehivestrategy.com/%s/blog/articles/%s" % (lang, slug)

def main():
    apply = "--apply" in sys.argv
    with open(PAIRS, encoding="utf-8") as f:
        groups = json.load(f)
    ts = time.strftime("%Y%m%d-%H%M%S")
    bdir = os.path.join(BASE, "variant_canonical_backups", ts)
    n_ok = n_missing = n_already = 0
    for g in groups:
        keep = g["pages"][0]
        for drop in g["pages"][1:]:
            p = art_path(g["lang"], drop["slug"])
            if not os.path.exists(p):
                n_missing += 1
                print("MISSING %s" % p)
                continue
            with open(p, encoding="utf-8") as f:
                h = f.read()
            target = canonical_url(g["lang"], keep["slug"])
            new_h, cnt = re.subn(
                r'(<link rel="canonical" href=")[^"]*(")',
                lambda m: m.group(1) + target + m.group(2), h, count=1)
            if cnt == 0:
                print("NO-CANONICAL-TAG %s" % p)
                continue
            if "canonical" in h and target in h:
                n_already += 1
                continue
            if apply:
                os.makedirs(bdir, exist_ok=True)
                shutil.copy2(p, os.path.join(bdir, (g["lang"] + "__" + drop["slug"] + ".html")))
                with open(p, "w", encoding="utf-8") as f:
                    f.write(new_h)
            n_ok += 1
    print("canonical updates: %d | already-ok: %d | missing: %d | %s" % (
        n_ok, n_already, n_missing, "APPLIED" if apply else "DRY-RUN"))
    if apply:
        print("backup: %s" % bdir)

if __name__ == "__main__":
    main()
