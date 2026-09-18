#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Variant option B prep: generate the _redirects block for 301 dedupe.
NOTE: 301 option has a bigger blast radius than canonical — after appending
redirects, the dropped pages should ALSO be removed from the 3 manifests and
sitemaps regenerated (generate_sitemap_full.py) + blog indexes rebuilt.
This script only emits the redirect lines (ready to append to website/_redirects).
Run anytime (writes gsc_out/variant_301_redirects.txt, does NOT touch the site).
"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
PAIRS = os.path.join(os.path.dirname(os.path.dirname(BASE)), "gsc_out", "variant_pairs_enriched.json")

def main():
    with open(PAIRS, encoding="utf-8") as f:
        groups = json.load(f)
    # collect unique (lang, drop_slug, keep_slug) — groups are per-lang already
    seen = set()
    lines = ["", "# === Variant dedupe 301s (2026-09-02, Kenneth approved) ==="]
    for g in groups:
        keep = g["pages"][0]["slug"]
        for drop in g["pages"][1:]:
            key = (g["lang"], drop["slug"])
            if key in seen:
                continue
            seen.add(key)
            if g["lang"] == "en":
                src = "/blog/articles/%s" % drop["slug"]
                dst = "/blog/articles/%s" % keep
            else:
                src = "/%s/blog/articles/%s" % (g["lang"], drop["slug"])
                dst = "/%s/blog/articles/%s" % (g["lang"], keep)
            lines.append("%s %s 301" % (src, dst))
            lines.append(src + ".html " + dst + " 301")
    out = os.path.join(os.path.dirname(os.path.dirname(BASE)), "gsc_out", "variant_301_redirects.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("redirect lines: %d (unique drop pages: %d) -> %s" % (len(lines) - 2, len(seen), out))

if __name__ == "__main__":
    main()
