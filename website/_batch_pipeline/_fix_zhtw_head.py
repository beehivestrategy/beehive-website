#!/usr/bin/env python3
"""Fix zh-TW <head>/structure language-prefix corruption introduced by full-file
OpenCC regeneration from zh-CN, and repair relative recommended-card hrefs in
both zh-CN and zh-TW.

Surgical: we must NOT touch the hreflang zh-CN alternate (points to zh-cn, correct)
nor the lang-switcher 简体中文 link (points to zh-cn, correct). We only flip the
page's OWN language signals from zh-cn -> zh-tw.

Run: python3 _fix_zhtw_head.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Known top-level nav paths that should follow the page language prefix.
NAV_PATHS = ["solution", "services", "industries", "case-studies", "pricing", "about", "blog"]


def fix_zhtw(html):
    # 1. <html lang="zh-cn"> -> zh-tw (only the document element)
    html = html.replace('<html lang="zh-cn"', '<html lang="zh-tw"')

    # 2. og:locale zh_CN -> zh_TW
    html = html.replace('og:locale" content="zh_CN"', 'og:locale" content="zh_TW"')

    # 3. JSON-LD inLanguage zh-CN -> zh-TW
    html = html.replace('"inLanguage": "zh-CN"', '"inLanguage": "zh-TW"')

    # 4. canonical (full URL) -> zh-tw
    html = re.sub(
        r'(rel="canonical" href="https://www\.beehivestrategy\.com/)zh-cn/',
        r'\1zh-tw/', html)

    # 5. og:url (full URL) -> zh-tw
    html = re.sub(
        r'(property="og:url" content="https://www\.beehivestrategy\.com/)zh-cn/',
        r'\1zh-tw/', html)

    # 6. og:image + twitter:image: domain prefix AND cover folder zh-cn -> zh-tw
    html = re.sub(
        r'(property="og:image" content="https://www\.beehivestrategy\.com/)zh-cn(/assets/blog/covers/)zh-cn/',
        r'\1zh-tw\2zh-tw/', html)
    html = re.sub(
        r'(name="twitter:image" content="https://www\.beehivestrategy\.com/)zh-cn(/assets/blog/covers/)zh-cn/',
        r'\1zh-tw\2zh-tw/', html)

    # 7. BlogPosting + BreadcrumbList JSON-LD: fix domain + cover folder.
    #    (FAQPage JSON-LD contains no zh-cn domain URL, so it is untouched.)
    def fix_ld(m):
        s = m.group(0)
        s = s.replace('https://www.beehivestrategy.com/zh-cn/',
                      'https://www.beehivestrategy.com/zh-tw/')
        s = s.replace('/assets/blog/covers/zh-cn/',
                      '/assets/blog/covers/zh-tw/')
        return s

    html = re.sub(r'<script type="application/ld\+json">.*?</script>',
                  fix_ld, html, flags=re.S)

    # 8. Home link (footer breadcrumb uses https://.../zh-cn/  with trailing /")
    html = html.replace(
        'https://www.beehivestrategy.com/zh-cn/"',
        'https://www.beehivestrategy.com/zh-tw/"')

    # 9. Known nav paths with leading slash + closing quote -> zh-tw.
    #    Boundary is the closing quote so /zh-cn/blog/articles/ (lang-switcher)
    #    is NOT matched (it is /zh-cn/blog/articles, not /zh-cn/blog").
    pat = r'/zh-cn/(%s)"' % "|".join(NAV_PATHS)
    html = re.sub(pat, lambda m: '/zh-tw/%s"' % m.group(1), html)

    # 10. Relative recommended-card / relative footer hrefs (no leading slash):
    #     href="zh-cn/... -> href="/zh-tw/...   (lang-switcher has leading slash, safe)
    html = re.sub(r'href="zh-cn/', 'href="/zh-tw/', html)

    return html


def fix_zhcn_relative(html):
    # zh-CN recommended cards / relative footer links are relative (no leading
    # slash): href="zh-cn/... -> href="/zh-cn/...  (root-relative, language-prefixed)
    html = re.sub(r'href="zh-cn/', 'href="/zh-cn/', html)
    return html


def main():
    slugs = []
    with open(os.path.join(ROOT, "_batch_pipeline", "gap_batches", "gbatch_001.txt")) as fh:
        for line in fh:
            s = line.strip()
            if s:
                slugs.append(s)

    for slug in slugs:
        tw = os.path.join(ROOT, "zh-tw", "blog", "articles", slug + ".html")
        cn = os.path.join(ROOT, "zh-cn", "blog", "articles", slug + ".html")
        if os.path.exists(tw):
            with open(tw, encoding="utf-8") as fh:
                h = fh.read()
            h2 = fix_zhtw(h)
            with open(tw, "w", encoding="utf-8") as fh:
                fh.write(h2)
            print("zh-tw  fixed:", slug, "(changed)" if h2 != h else "(no-op)")
        if os.path.exists(cn):
            with open(cn, encoding="utf-8") as fh:
                h = fh.read()
            h2 = fix_zhcn_relative(h)
            with open(cn, "w", encoding="utf-8") as fh:
                fh.write(h2)
            print("zh-cn  relfixed:", slug, "(changed)" if h2 != h else "(no-op)")


if __name__ == "__main__":
    main()
