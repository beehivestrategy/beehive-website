#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, re
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
import _gb001_lib as L
slug = sys.argv[1]
for lang in ("en", "zh-CN", "zh-TW"):
    h = L.read(slug, lang)
    b = L.body_of(h)
    m = re.search(r'<article class="article-content" id="article-content">', h)
    print(f"--- {lang}  metric={L.metric(h,lang)}")
    for hid, t in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', h, re.S):
        t = re.sub(r'<[^>]+>', '', t).strip()
        mark = "Q " if t.endswith(('?', '？')) else "  "
        print(f"  {mark}{hid} :: {t}")
    print("  rec:", L.rec_hrefs(h))
    m = re.search(r'<p class="article-lead">(.*?)</p>', h, re.S)
    if m:
        print("  LEAD:", re.sub(r'<[^>]+>', '', m.group(1)).strip()[:160])
