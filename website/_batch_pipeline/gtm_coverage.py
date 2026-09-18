#!/usr/bin/env python3
import os, glob
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sections = ["blog/articles", "zh-cn/blog/articles", "zh-tw/blog/articles"]
for s in sections:
    files = glob.glob(os.path.join(base, s, "*.html"))
    with_gtm = 0
    for f in files:
        try:
            with open(f, encoding="utf-8", errors="ignore") as fh:
                if "GTM-MFSTHW7" in fh.read():
                    with_gtm += 1
        except OSError:
            pass
    print("%s : %d / %d pages have GTM" % (s, with_gtm, len(files)))
# top-level + other html
all_html = glob.glob(os.path.join(base, "*.html"))
with_gtm = sum(1 for f in all_html if "GTM-MFSTHW7" in open(f, encoding="utf-8", errors="ignore").read())
print("top-level *.html : %d / %d have GTM" % (with_gtm, len(all_html)))
