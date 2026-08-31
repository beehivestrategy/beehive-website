#!/usr/bin/env python3
"""Apply h2map_gb003.json to the gbatch_003 files."""
import os, sys, json, importlib.util

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
spec = importlib.util.spec_from_file_location("fs", os.path.join(ROOT, "_batch_pipeline/fix_struct.py"))
fs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fs)

LANGS = [("EN", "blog/articles"), ("zh-CN", "zh-cn/blog/articles"), ("zh-TW", "zh-tw/blog/articles")]
slugs = [l.strip() for l in open(os.path.join(ROOT, "_batch_pipeline/gap_batches/gbatch_003.txt")) if l.strip()]
mp = json.load(open(os.path.join(ROOT, "_batch_pipeline/h2map_gb003.json"), encoding="utf-8"))

dry = "--dry" in sys.argv
only = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else None

for s in slugs:
    if only and s != only:
        continue
    for lang, d in LANGS:
        p = os.path.join(ROOT, d, s + ".html")
        if not os.path.exists(p):
            continue
        mapping = mp.get(f"{s}|{lang}", {})
        ch = fs.do_h2map(p, mapping, dry=dry)
        print(f"{s[:40]:42} {lang:6} changed={len(ch)}")
        for old, new, oid, nid in ch:
            print(f"    {old!r} -> {new!r}")
