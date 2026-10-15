#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_en_links.py — Repair broken internal links.

The generator emitted internal article links as href="/en/blog/articles/..."
but the live site has no /en/ path segment (EN lives at /blog/articles/...).
Every such link 404s. This strips the spurious "/en" prefix.

Scope: website/blog/articles/*.html  (only the relative "/en/blog/articles/"
substring is touched; absolute URLs and other /en/ forms are left alone).
"""
import os, glob

ART = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/blog/articles"
OLD = '"/en/blog/articles/'
NEW = '"/blog/articles/'

def main():
    files = glob.glob(os.path.join(ART, "*.html"))
    total_files = 0
    total_repl = 0
    for path in files:
        with open(path, encoding="utf-8", errors="replace") as f:
            txt = f.read()
        if OLD in txt:
            n = txt.count(OLD)
            txt = txt.replace(OLD, NEW)
            with open(path, "w", encoding="utf-8") as f:
                f.write(txt)
            total_files += 1
            total_repl += n
    print(f"Files changed: {total_files}")
    print(f"Link occurrences repaired: {total_repl}")

if __name__ == "__main__":
    main()
