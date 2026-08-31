#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Make every <a class="recommended-card"> href root-relative and language-prefixed,
then fill empty excerpts from the linked article."""
import sys, os, re, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _gb001r_lib as L
from _gb001r_excerpt import summary_for, first_sentence

PREFIX = {"blog/articles": "/blog/articles",
          "zh-cn/blog/articles": "/zh-cn/blog/articles",
          "zh-tw/blog/articles": "/zh-tw/blog/articles"}

REC_RE = re.compile(r'(<a href=")([^"]*)(" class="recommended-card")', re.I)
EXC_RE = re.compile(r'<p class="recommended-card-excerpt">\s*</p>')


def norm_href(href, sub):
    h = href.split("beehivestrategy.com")[-1] if "beehivestrategy.com" in href else href
    h = h.split("?")[0].rstrip("/")
    slug = h.split("/")[-1]
    if not slug or slug.endswith(".html") is False and "." in slug:
        return None
    slug = slug[:-5] if slug.endswith(".html") else slug
    return PREFIX[sub] + "/" + slug


def run():
    slugs = [l.strip() for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
             "gap_batches/gbatch_001.txt")) if l.strip()]
    nlink = nfilled = 0
    for s in slugs:
        for sub, lang, floor in L.LANGS:
            before = L.read(sub, s)
            changed = False
            out, pos = [], 0
            for m in REC_RE.finditer(before):
                new = norm_href(m.group(2), sub)
                if not new or new == m.group(2): continue
                out.append(before[pos:m.start(2)]); out.append(new); pos = m.end(2)
                changed = True
            out.append(before[pos:])
            after = "".join(out)

            # fill excerpts from the (now root-relative) target article
            cards = re.split(r'(?=<a href=")', after)
            nc = []
            for c in cards:
                if not EXC_RE.search(c):
                    nc.append(c); continue
                hm = re.match(r'<a href="([^"]*)"', c)
                p = os.path.join(L.ROOT, hm.group(1).lstrip("/")) if hm else None
                if p and os.path.isfile(p + ".html"): p += ".html"
                if not p or not os.path.isfile(p):
                    nc.append(c); continue
                try:
                    summ = summary_for(p, lang)
                except Exception:
                    summ = ""
                if not summ:
                    nc.append(c); continue
                c = EXC_RE.sub('<p class="recommended-card-excerpt">%s</p>'
                               % H.escape(summ, quote=False), c, count=1)
                nfilled += 1; changed = True
                nc.append(c)
            after = "".join(nc)

            if not changed: continue
            errs = L.guard(before, after, sub, s, allow_link_add=True)
            if errs:
                print("GUARD FAIL", s, lang, errs); continue
            L.write(sub, s, after)
            nlink += 1
    print("files changed:", nlink, "excerpts filled:", nfilled)


if __name__ == "__main__":
    run()
