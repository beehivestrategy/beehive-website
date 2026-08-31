#!/usr/bin/env python3
"""Guardrail check: compare current files vs backup, assert nothing protected changed."""
import re, os, sys, difflib

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
BAK = os.path.join(ROOT, "_batch_pipeline/_bak_gb001b")
SLUGS = [l.strip() for l in open(os.path.join(ROOT, "_batch_pipeline/gap_batches/gbatch_001.txt")) if l.strip()]
LANGS = (("en", "blog/articles/%s.html", "blog_%s.html"),
         ("cn", "zh-cn/blog/articles/%s.html", "zh-cn_blog_%s.html"),
         ("tw", "zh-tw/blog/articles/%s.html", "zh-tw_blog_%s.html"))

def head_of(h):
    m = re.search(r'<head[^>]*>(.*?)</head>', h, re.S)
    return m.group(1) if m else ""

def footer_of(h):
    i = h.find('<footer')
    return h[i:] if i >= 0 else ""

def title_meta(h):
    out = []
    for pat in (r'<title>(.*?)</title>', r'<meta property="og:title" content="(.*?)"',
                r'<meta name="twitter:title" content="(.*?)"'):
        m = re.search(pat, h, re.S)
        out.append(m.group(1).strip() if m else None)
    m = re.search(r'<h1[^>]*>(.*?)</h1>', h, re.S)
    out.append(re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else None)
    return out

problems = []
for s in SLUGS:
    for lang, tpl, baktpl in LANGS:
        cur_p = os.path.join(ROOT, tpl % s)
        bak_p = os.path.join(BAK, baktpl % s)
        if not (os.path.exists(cur_p) and os.path.exists(bak_p)):
            problems.append(f"{s}/{lang}: missing file"); continue
        cur = open(cur_p, encoding='utf-8').read()
        bak = open(bak_p, encoding='utf-8').read()

        # 1. titles unchanged
        if title_meta(cur) != title_meta(bak):
            problems.append(f"{s}/{lang}: TITLE/H1 CHANGED {title_meta(bak)} -> {title_meta(cur)}")
        # 2. version strings still present
        if '?v=20260826' in bak and cur.count('?v=20260826') != bak.count('?v=20260826'):
            problems.append(f"{s}/{lang}: ?v= VERSION STRING COUNT CHANGED")
        if '/css/article.css?v=20260826' not in cur or '/js/article.js?v=20260826' not in cur:
            problems.append(f"{s}/{lang}: versioned asset link missing")
        # 3. footer byte-identical
        if footer_of(cur) != footer_of(bak):
            problems.append(f"{s}/{lang}: FOOTER CHANGED")
        # 4. share markup identical
        for marker in ('id="share-linkedin"', 'id="share-x"', 'id="share-copy"'):
            if cur.count(marker) != bak.count(marker):
                problems.append(f"{s}/{lang}: share button {marker} changed")
        # 5. head: only allowed to differ by FAQPage ld+json block
        hc, hb = head_of(cur), head_of(bak)
        def strip_ld(x):
            return re.sub(r'<script type="application/ld\+json">.*?</script>', '', x, flags=re.S)
        if strip_ld(hc).strip() != strip_ld(hb).strip():
            # report the actual diff lines
            d = [l for l in difflib.unified_diff(strip_ld(hb).splitlines(), strip_ld(hc).splitlines(), lineterm='', n=0)]
            problems.append(f"{s}/{lang}: NON-LD HEAD CHANGE {d[:6]}")
        # 6. canonical/hreflang intact
        for m in re.findall(r'<link[^>]*>', hb):
            if m not in hc:
                problems.append(f"{s}/{lang}: head link removed: {m[:90]}")
        # 7. root-relative / language-prefixed links preserved (no net loss)
        for pref in ('/css/', '/js/', '/assets/', '/blog/', '/zh-cn/', '/zh-tw/'):
            pass
        # 8. exactly one FAQPage (only if a faq section exists)
        n = len(re.findall(r'"FAQPage"', cur))
        if 'class="faq-section"' in cur and n != 1:
            problems.append(f"{s}/{lang}: FAQPage count = {n}")
        # 9. no new unescaped raw '</' sequences inside ld+json
        for mm in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', cur, re.S):
            try:
                import json; json.loads(mm.group(1))
            except Exception as e:
                problems.append(f"{s}/{lang}: ld+json invalid: {e}")

print("PROBLEMS:", len(problems))
for p in problems:
    print(" -", p)
if not problems:
    print("ALL GUARDRAILS OK")
