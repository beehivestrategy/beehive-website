#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Find pages missing GTM-MFSTHW7 and patch them (additive fix, local only).
Mode 1 (default): list missing pages.
Mode 2 (--patch):  insert GTM snippet after viewport meta, matching existing pattern.
"""
import os, glob, sys, re, io

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECTIONS = ["blog/articles", "zh-cn/blog/articles", "zh-tw/blog/articles"]

GTM_JS = "  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','GTM-MFSTHW7');</script>"
GTM_NOSCRIPT = '  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-MFSTHW7" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>'

def has_gtm(path):
    try:
        with io.open(path, encoding="utf-8", errors="ignore") as f:
            return "GTM-MFSTHW7" in f.read()
    except OSError:
        return True  # unreadable -> don't touch

def find_missing():
    missing = []
    for s in SECTIONS:
        for f in sorted(glob.glob(os.path.join(base, s, "*.html"))):
            if not has_gtm(f):
                missing.append(f)
    top = [f for f in sorted(glob.glob(os.path.join(base, "*.html"))) if not has_gtm(f)]
    return missing, top

def patch(path):
    with io.open(path, encoding="utf-8") as f:
        html = f.read()
    if "GTM-MFSTHW7" in html:
        return "skip"
    # insert JS after viewport meta (article pattern)
    m = re.search(r'([ \t]*)<meta name="viewport"[^>]*>\r?\n', html)
    if m:
        html = html[:m.end()] + GTM_JS + "\n" + html[m.end():]
    else:
        m2 = re.search(r'([ \t]*)<title>', html)
        if not m2:
            return "no-anchor"
        html = html[:m2.start()] + GTM_JS + "\n" + html[m2.start():]
    # insert noscript after <body> (article pattern)
    m3 = re.search(r'<body[^>]*>\r?\n', html)
    if m3:
        html = html[:m3.end()] + GTM_NOSCRIPT + "\n" + html[m3.end():]
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return "patched"

if __name__ == "__main__":
    missing, top = find_missing()
    print("blog missing GTM: %d" % len(missing))
    for f in missing:
        print("  " + os.path.relpath(f, base))
    print("top-level missing GTM: %d" % len(top))
    for f in top:
        print("  " + os.path.relpath(f, base))
    if "--patch" in sys.argv:
        ok = 0
        for f in missing + top:
            r = patch(f)
            if r == "patched":
                ok += 1
            else:
                print("FAILED %s -> %s" % (os.path.relpath(f, base), r))
        print("patched: %d" % ok)
