#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Print article body (no TOC/nav/FAQ) with wrapped lines: python3 _gb003_show.py <slug> <lang>"""
import re, sys, textwrap
sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
from _gb003_lib import path_for, ART_OPEN

slug, lang = sys.argv[1], sys.argv[2]
h = open(path_for(slug, lang), encoding='utf-8').read()
ai = h.find(ART_OPEN); ae = h.find('</article>', ai)
art = h[ai:ae]
art = re.sub(r'<div class="toc-mobile".*?</div>\s*</div>', '', art, flags=re.S)
art = re.sub(r'<nav class="article-nav".*?</nav>', '', art, flags=re.S)
art = re.sub(r'<section class="faq-section".*?</section>', '', art, flags=re.S)
out = []
for line in art.split('\n'):
    line = line.rstrip()
    if not line:
        continue
    if len(line) <= 160:
        out.append(line)
    else:
        m = re.match(r'^(<[a-z0-9]+[^>]*>)(.*)(</[a-z0-9]+>)$', line, re.S)
        if m:
            body = textwrap.fill(m.group(2), 150)
            out.append(m.group(1) + ('\n   ' + body).replace('\n   ', '\n   ', 1) + m.group(3))
        else:
            out.append(textwrap.fill(line, 150))
print('\n'.join(out))
