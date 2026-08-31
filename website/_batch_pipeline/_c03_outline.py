#!/usr/bin/env python3
import sys, re
sys.path.insert(0, "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline")
import _c03_tool as T

slug = sys.argv[1]
langs = sys.argv[2].split(",") if len(sys.argv) > 2 else ["en", "cn", "tw"]
for lang in langs:
    h = T.read(T.path_for(lang, slug))
    p = T.extract_prose(h)
    print("=" * 90)
    print(lang.upper(), "| H1:", T.get_h1(h), "| len:", T.measure(h, lang))
    print("DESC:", T.get_desc(h)[:160])
    lead = re.search(r'<p class="article-lead">(.*?)</p>', p, re.S)
    if lead:
        print("LEAD:", re.sub(r'\s+', ' ', T.strip_tags(lead.group(1)))[:400])
    for hid, t in T.h2_list(p):
        seg = p[p.find(f'id="{hid}"'):]
        nxt = seg.find('<h2 id=', 5)
        seg = seg[:nxt] if nxt > 0 else seg
        n = T.en_words(T.strip_tags(seg)) if lang == "en" else T.cjk(T.strip_tags(seg))
        print(f'  [{n:5d}] #{hid}  ::  {t}')
