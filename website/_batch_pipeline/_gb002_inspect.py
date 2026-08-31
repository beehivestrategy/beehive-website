#!/usr/bin/env python3
"""Dump H2 outline (+ short body preview) for a slug across all three languages."""
import re, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for slug in sys.argv[1:]:
    print("=" * 20, slug)
    for rel in ("blog/articles", "zh-cn/blog/articles", "zh-tw/blog/articles"):
        p = os.path.join(ROOT, rel, slug + ".html")
        if not os.path.exists(p):
            print("MISSING", p); continue
        raw = open(p, encoding='utf-8').read()
        print("--", rel)
        ms = list(re.finditer(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', raw, re.S))
        for i, m in enumerate(ms):
            nxt = ms[i + 1].start() if i + 1 < len(ms) else raw.find('faq-section')
            seg = raw[m.end():nxt]
            t = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', seg)).strip()
            print("   %-45s | %s" % (m.group(1)[:45], re.sub(r'<[^>]+>', '', m.group(2)).strip()))
            print("       ~", t[:150])
