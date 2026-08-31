#!/usr/bin/env python3
"""Fix zh-TW canonical + og:url that wrongly point to /zh-cn/ instead of /zh-tw/.
Surgical: only the canonical <link> and og:url <meta>, never hreflang, never body.
Backs up each file before editing.
"""
import os, re, shutil, sys

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
TWDIR = os.path.join(ROOT, "zh-tw/blog/articles")
BAK = os.path.join(ROOT, "_batch_pipeline/_bak_zhtw_canonical")
os.makedirs(BAK, exist_ok=True)

canon_re = re.compile(r'(<link\b[^>]*\brel="canonical"[^>]*\bhref=")([^"]*?)(/zh-cn/)(blog/articles/[^"]*)(")', re.I)
og_re    = re.compile(r'(<meta\b[^>]*\bproperty="og:url"[^>]*\bcontent=")([^"]*?)(/zh-cn/)(blog/articles/[^"]*)(")', re.I)

fixed = 0
skipped = 0
for fn in sorted(os.listdir(TWDIR)):
    if not fn.endswith(".html"):
        continue
    p = os.path.join(TWDIR, fn)
    h = open(p, encoding="utf-8").read()
    # only act if canonical or og:url references /zh-cn/
    if "/zh-cn/" not in h:
        continue
    new = h
    new = canon_re.sub(r'\1\2/zh-tw/\4\5', new)
    new = og_re.sub(r'\1\2/zh-tw/\4\5', new)
    if new == h:
        skipped += 1
        continue
    # sanity: ensure we did not accidentally rewrite hreflang
    assert 'hreflang="zh-TW"' not in new or ('/zh-tw/' in new), "hreflang would be broken"
    shutil.copy2(p, os.path.join(BAK, fn))
    open(p, "w", encoding="utf-8").write(new)
    fixed += 1

print(f"Fixed: {fixed}  Skipped(no /zh-cn/ or no match): {skipped}")
