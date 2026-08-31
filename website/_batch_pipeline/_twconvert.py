#!/usr/bin/env python3
"""Convert a Simplified-Chinese HTML prose snippet to Traditional (Taiwan) and
align each <h2 id> to the existing zh-TW TOC id by matching simplified forms.
Usage: _twconvert.py <src_snippet> <target_zhtw_html> <out_snippet>"""
import re, sys, opencc
cc = opencc.OpenCC('s2twp')
t2s = opencc.OpenCC('t2s')
src = open(sys.argv[1], encoding="utf-8").read()
target = open(sys.argv[2], encoding="utf-8").read()
out = cc.convert(src)

# zh-TW toc ids (from toc-mobile-links, and sidebar toc-links should match)
toc = re.search(r'<div class="toc-mobile-links">(.*?)</div>\s*</div>', target, re.S)
toc_ids = re.findall(r'href="#([^"]+)"', toc.group(1)) if toc else []
# also gather sidebar toc ids
side = re.search(r'<nav class="toc-links">(.*?)</nav>', target, re.S)
if side:
    toc_ids += re.findall(r'href="#([^"]+)"', side.group(1))
toc_norm = {t2s.convert(x): x for x in dict.fromkeys(toc_ids)}  # simplified -> original

def fix(m):
    hid = m.group(1)
    key = t2s.convert(hid)
    new = toc_norm.get(key, hid)  # align to existing toc id if matched
    return f'<h2 id="{new}"'

out = re.sub(r'<h2 id="([^"]+)"', fix, out)
open(sys.argv[3], "w", encoding="utf-8").write(out)
print("TW snippet ids aligned. toc count:", len(toc_ids))
