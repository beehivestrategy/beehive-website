# -*- coding: utf-8 -*-
"""Reusable safety verifier: usage: python3 verify_slug.py <slug>  (checks EN/zh-CN/zh-TW)"""
import re, io, sys

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
slug = sys.argv[1]
files = {
    "EN":   f"{ROOT}/blog/articles/{slug}.html",
    "zhCN": f"{ROOT}/zh-cn/blog/articles/{slug}.html",
    "zhTW": f"{ROOT}/zh-tw/blog/articles/{slug}.html",
}
ok = True
for tag, f in files.items():
    s = io.open(f, encoding="utf-8").read()
    head = s.split('</head>')[0]
    h1m = re.search(r'<h1 class="article-h1">(.*?)</h1>', s, re.S)
    res = [
        ("css ?v=20260901", '/css/article.css?v=20260901' in s),
        ("js ?v=20260901", '/js/article.js?v=20260901' in s),
        ("BlogPosting in head", 'BlogPosting' in head),
        ("Breadcrumb in head", 'BreadcrumbList' in head),
        ("no FAQPage in head", 'FAQPage' not in head),
        ("exactly 1 FAQPage total", s.count('"FAQPage"') == 1),
        ("3 share buttons", s.count('article-share-btn') == 3),
        ("footer intact", '<footer class="footer"' in s and '/privacy' in s),
        ("GTM intact", 'GTM-MFSTHW7' in head),
        ("h1 present", bool(h1m)),
        ("no empty excerpt", 'recommended-card-excerpt"></p>' not in s),
        ("faq h3 wrap >=3", s.count('<h3 style="margin:0;">') >= 3),
        ("no dup faq number", not re.search(r'<span class="faq-number">\d</span><span>\d', s)),
        ("article-content present", 'id="article-content"' in s),
    ]
    if tag == "EN":
        res.append(("CTA Book a Demo", 'class="article-cta-btn">Book a Demo' in s))
        res.append(("lang links", '/zh-cn/blog/articles/%s' % slug in s and '/zh-tw/blog/articles/%s' % slug in s))
    elif tag == "zhCN":
        res.append(("CTA 预约演示", 'class="article-cta-btn">预约演示' in s))
        res.append(("lang links", ('/blog/articles/%s' % slug) in s and ('/zh-tw/blog/articles/%s' % slug) in s))
    else:
        res.append(("CTA 預約示範", 'class="article-cta-btn">預約示範' in s))
        res.append(("lang links", ('/blog/articles/%s' % slug) in s and ('/zh-cn/blog/articles/%s' % slug) in s))
    ids = set(re.findall(r'<h2 id="([^"]+)"', s))
    anchors = set(re.findall(r'class="toc-(?:mobile-)?link" href="#([^"]+)"', s))
    bad = anchors - ids
    res.append(("toc anchors valid", not bad))
    if bad:
        print(tag, "BAD ANCHORS:", bad)
    # JSON-LD matches FAQ questions
    jl = re.search(r'<script type="application/ld\+json">(?:(?!</script>).)*?"@type":\s*"FAQPage"(?:(?!</script>).)*?</script>', s, re.S)
    if jl:
        qs_page = re.findall(r'<span class="faq-number">\d+</span><span>([^<]+)</span>', s)
        qs_json = re.findall(r'"name":\s*"([^"]+)"', jl.group(0))
        res.append(("FAQPage matches page Qs", [q.strip() for q in qs_json] == [q.strip() for q in qs_page]))
    else:
        res.append(("FAQPage jsonld exists", False))
    for name, passed in res:
        if not passed:
            ok = False
            print(f"FAIL [{tag}] {name}")
print("ALL PASS" if ok else "HAS FAILURES")
