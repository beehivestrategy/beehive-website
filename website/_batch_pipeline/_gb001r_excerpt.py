#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Populate empty recommended-card excerpts with a 1-sentence summary taken
from the linked article itself (lead paragraph, else meta description)."""
import sys, os, re, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _gb001r_lib as L

SLUGS = [l.strip() for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
         "gap_batches/gbatch_001.txt")) if l.strip()]

def resolve(href, sub):
    if href.startswith("http"):
        i = href.find("beehivestrategy.com")
        if i < 0: return None
        href = href[i + len("beehivestrategy.com"):]
    if not href.startswith("/"): return None
    p = os.path.join(L.ROOT, href.lstrip("/"))
    for cand in (p, p + ".html"):
        if os.path.isfile(cand): return cand
    return None

def first_sentence(text, is_cjk):
    t = re.sub(r"\s+", " ", H.unescape(text)).strip()
    t = re.sub(r"<[^>]+>", "", t)
    if not t: return ""
    lim = 70 if is_cjk else 180
    if len(t) <= lim: return t
    m = re.search(r"[。！？]" if is_cjk else r"(?<=[.!?])\s", t)
    cut = m.end() if m and m.end() <= lim + 40 else lim
    return t[:cut].rstrip("，,、 ") + ("…" if cut < len(t) else "")

def summary_for(path, lang):
    h = open(path, encoding="utf-8").read()
    m = re.search(r'<p class="article-lead">([\s\S]*?)</p>', h)
    src = m.group(1) if m else None
    if not src:
        m = re.search(r'<meta name="description" content="([^"]*)"', h)
        src = m.group(1).strip() if m else ""
    if not src:
        a = L.article_block(h)
        ps = [re.sub(r"<[^>]+>", "", p).strip() for p in re.findall(r"<p\b[^>]*>([\s\S]*?)</p>", a)]
        src = next((p for p in ps if len(p) >= (40 if lang != "en" else 90)), "")
    return first_sentence(src, lang != "en")

def run():
    total = 0
    for s in SLUGS:
        for sub, lang, floor in L.LANGS:
            before = L.read(sub, s)
            m = re.search(r'<section class="recommended-section"[\s\S]*?</section>', before)
            if not m: continue
            blk = m.group(0)
            if not re.search(r'<p class="recommended-card-excerpt">\s*</p>', blk): continue
            # split into <a ...> card blocks
            out = blk
            cards = re.split(r'(?=<a href=")', blk)
            newcards = []
            for c in cards:
                if not re.search(r'<p class="recommended-card-excerpt">\s*</p>', c):
                    newcards.append(c); continue
                hm = re.match(r'<a href="([^"]*)"', c)
                p = resolve(hm.group(1), sub) if hm else None
                if not p:
                    newcards.append(c); continue
                try:
                    summ = summary_for(p, lang)
                except Exception:
                    summ = ""
                if not summ:
                    newcards.append(c); continue
                c = re.sub(r'<p class="recommended-card-excerpt">\s*</p>',
                           '<p class="recommended-card-excerpt">%s</p>' % H.escape(summ, quote=False), c, count=1)
                total += 1
                newcards.append(c)
            out = "".join(newcards)
            after = before[:m.start()] + out + before[m.end():]
            errs = L.guard(before, after, sub, s)
            if errs:
                print("GUARD FAIL", s, lang, errs); continue
            L.write(sub, s, after)
            print(f"{s[:44]:44} {lang:6} filled {len(re.findall(chr(60)+'p class="recommended-card-excerpt">'+chr(92)+'s*'+chr(60)+'/p>', out))}")
    print("total filled:", total)

if __name__ == "__main__":
    run()
