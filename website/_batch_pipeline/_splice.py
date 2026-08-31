#!/usr/bin/env python3
"""In-place splice helper for blog GEO/SEO rewrite fleet.
Modes:
  expand : file already has <section class="faq-section"> ; replace prose between
           toc-mobile end and faq-section start with NEW prose (HTML snippet file).
  full   : file has NO faq-section ; replace region between toc-mobile end and
           <nav class="article-nav" with NEW prose + NEW faq + NEW jsonld.
Never touches <head>, <footer>, share buttons, recommended, CTA, versioned links.
"""
import re, sys

def splice(path, mode, prose_file, faq_file=None, jsonld_file=None):
    html = open(path, encoding="utf-8").read()
    aopen = re.search(r'<article[^>]*id="article-content"[^>]*>', html)
    if aopen is None:
        raise SystemExit("NO_ARTICLE_TAG " + path)
    aend = aopen.end()

    prose = open(prose_file, encoding="utf-8").read().strip()

    if mode == "expand":
        faq_start = html.index('<section class="faq-section"')
        region = html[aend:faq_start]
        p_idx = region.index('<p')
        toc = region[:p_idx]  # includes toc-mobile block closing </div>
        new_inner = toc + "\n" + prose + "\n"
        html = html[:aend] + new_inner + html[faq_start:]
    elif mode == "full":
        nav_start = html.index('<nav class="article-nav"')
        region = html[aend:nav_start]
        p_idx = region.index('<p')
        toc = region[:p_idx]
        faq = open(faq_file, encoding="utf-8").read().strip() if faq_file else ""
        jsonld = open(jsonld_file, encoding="utf-8").read().strip() if jsonld_file else ""
        new_inner = toc + "\n" + prose + "\n" + faq + "\n" + jsonld + "\n"
        html = html[:aend] + new_inner + html[nav_start:]
    else:
        raise SystemExit("BAD_MODE " + mode)

    # safety: must still contain head, footer, versioned links
    assert "/css/article.css?v=20260826" in html, "CSS link lost!"
    assert "/js/article.js?v=20260826" in html, "JS link lost!"
    assert '<footer' in html, "Footer lost!"
    open(path, "w", encoding="utf-8").write(html)
    print("OK", path)

if __name__ == "__main__":
    mode = sys.argv[1]
    path = sys.argv[2]
    prose_file = sys.argv[3]
    faq_file = sys.argv[4] if len(sys.argv) > 4 else None
    jsonld_file = sys.argv[5] if len(sys.argv) > 5 else None
    splice(path, mode, prose_file, faq_file, jsonld_file)
