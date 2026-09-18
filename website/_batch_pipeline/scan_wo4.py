#!/usr/bin/env python3
"""Scan article HTML for English visible text inside <article> and duplicate H2s."""
import re, sys, unicodedata

def has_cjk(s):
    return any('\u4e00' <= c <= '\u9fff' or '\u3400' <= c <= '\u4dbf' for c in s)

def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s).strip()

def latin_ratio(s):
    letters = [c for c in s if c.isalpha()]
    if not letters: return 0
    latin = [c for c in letters if c.isascii()]
    return len(latin)/len(letters)

path = sys.argv[1]
html = open(path, encoding='utf-8').read()

# isolate <article ...> ... </article>
m = re.search(r'<article\b.*?</article>', html, re.S)
if not m:
    print("NO ARTICLE FOUND"); sys.exit(1)
art = m.group(0)

print(f"== {path.split('/')[-1]} ==")

# 1. English headings (h1-h4)
print("-- EN headings --")
for tag, inner in re.findall(r'<(h[1-4])\b[^>]*>(.*?)</\1>', art, re.S):
    txt = strip_tags(inner)
    if not txt: continue
    if not has_cjk(txt) and (len(txt) >= 8 or (len(txt) >= 4 and latin_ratio(txt) > 0.9)):
        hid = re.search(r'<%s\b[^>]*\bid="([^"]+)"' % tag, inner)
        # get id from outer tag
        print(f"  [{tag}] id={hid.group(1) if hid else '?'} :: {txt[:80]}")

# also check h2/h3 titles that are mixed but long English
# 2. English paragraphs / list items
print("-- EN paragraphs/li --")
for tag, inner in re.findall(r'<(p|li)\b[^>]*>(.*?)</\1>', art, re.S):
    txt = strip_tags(inner)
    if len(txt) >= 60 and not has_cjk(txt) and latin_ratio(txt) > 0.85:
        print(f"  [{tag}] :: {txt[:100]}...")

# 3. TOC link texts (desktop + mobile)
print("-- EN TOC links --")
for cls in ('toc-link', 'toc-mobile-link'):
    for href, txt in re.findall(r'<a href="([^"]+)" class="%s"[^>]*>(.*?)</a>' % cls, art, re.S):
        t = strip_tags(txt)
        if not has_cjk(t) and t:
            print(f"  [{cls}] {href} :: {t[:80]}")

# 4. article-lead
print("-- EN article-lead --")
for inner in re.findall(r'<p class="article-lead"[^>]*>(.*?)</p>', art, re.S):
    t = strip_tags(inner)
    if len(t) >= 60 and not has_cjk(t) and latin_ratio(t) > 0.85:
        print(f"  :: {t[:120]}...")

# 5. duplicate H2 check (strip inner tags, whitespace)
print("-- duplicate H2 --")
titles = {}
for pos, inner in re.finditer(r'<h2\b[^>]*>(.*?)</h2>', art, re.S):
    t = re.sub(r'\s+', '', strip_tags(inner))
    titles.setdefault(t, []).append(inner[:60])
for t, occ in titles.items():
    if len(occ) > 1:
        print(f"  x{len(occ)} :: {t[:60]}")
        for o in occ: print(f"      {o[:60]}")
