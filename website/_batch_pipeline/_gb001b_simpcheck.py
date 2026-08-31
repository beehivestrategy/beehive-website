#!/usr/bin/env python3
"""Detect residual Simplified Chinese in zh-TW article bodies.

Single characters such as 台/干/准/游 are valid Traditional in context, so a
char-level s2t check yields many false positives. We instead flag CONTIGUOUS RUNS
of >=2 characters that all change under s2t -- the reliable signature of a
Simplified phrase that was pasted in without conversion.
"""
import re, os, sys
from opencc import OpenCC

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
SLUGS = [l.strip() for l in open(os.path.join(ROOT, "_batch_pipeline/gap_batches/gbatch_001.txt")) if l.strip()]
_cc = OpenCC('s2t')
MINRUN = int(os.environ.get("MINRUN", "2"))

def body_text(html):
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', html, re.S)
    b = m.group(1) if m else ""
    b = re.sub(r'<script.*?</script>', ' ', b, flags=re.S)
    b = re.sub(r'<[^>]+>', ' ', b)
    return re.sub(r'\s+', ' ', b)

total = 0
for s in SLUGS:
    p = os.path.join(ROOT, "zh-tw/blog/articles/%s.html" % s)
    if not os.path.exists(p):
        print("MISSING", p); continue
    t = body_text(open(p, encoding="utf-8").read())
    flags = []
    i = 0
    while i < len(t):
        if '\u4e00' <= t[i] <= '\u9fff' and _cc.convert(t[i]) != t[i]:
            j = i
            while j < len(t) and '\u4e00' <= t[j] <= '\u9fff' and _cc.convert(t[j]) != t[j]:
                j += 1
            run = t[i:j]
            if len(run) >= MINRUN:
                flags.append((run, t[max(0, i - 25):j + 25]))
            i = j
        else:
            i += 1
    if flags:
        print(f"\n=== {s}  ({len(flags)} run(s)) ===")
        for run, ctx in flags:
            print(f"   SIMPL: {run!r}\n     ctx: …{ctx}…")
        total += len(flags)
print(f"\nTOTAL simplified runs (>= {MINRUN} chars) in zh-TW bodies: {total}")
