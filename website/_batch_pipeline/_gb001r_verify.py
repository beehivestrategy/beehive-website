#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final verification of the gbatch_001 run against the GEO/SEO standard."""
import sys, os, re, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _gb001r_lib as L

SLUGS = [l.strip() for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
         "gap_batches/gbatch_001.txt")) if l.strip()]
FLOOR = {"en": 2500, "zh-cn": 3500, "zh-tw": 3500}
QEN = re.compile(r"^(how|what|why|when|which|where|who|can|do|does|did|is|are|should|will|would|must|need)", re.I)
QZH = re.compile(r"(如何|什麼|什么|為什麼|为什么|怎麼|怎么|是否|怎樣|怎样|為何|为何|何時|何时|哪些|哪裡|哪里|為什|怎)")

problems = []
for s in SLUGS:
    for sub, lang, floor in L.LANGS:
        h = L.read(sub, s)
        p = []
        a = L.article_block(h)
        m = L.metric(h, lang)
        if m < FLOOR[lang]: p.append(f"LEN {m}<{floor}")
        # head integrity
        hd = L.head_of(h)
        for k in ("BlogPosting", "BreadcrumbList", "/css/article.css?v=20260826"):
            if k not in hd: p.append("HEAD:" + k)
        if "/js/article.js?v=20260826" not in h: p.append("JS VERSION LOST")
        # footer + share
        if '<footer' not in h: p.append("NO FOOTER")
        if h.count('class="article-share-btn"') < 3: p.append("SHARE MISSING")
        # faq
        fb = L.FAQ_RE.search(h)
        if not fb: p.append("NO FAQ SECTION")
        else:
            items = L.faq_items(fb.group(0))
            if len(items) < 3: p.append(f"FAQ {len(items)}")
            if 'class="faq-section"' not in fb.group(0): p.append("NO faq-section CLASS")
            if len(re.findall(r'<h3\b', fb.group(0))) < 3: p.append("FAQ h3<3")
        # json-ld in body, matches page
        he = h.lower().find("</head>")
        bodyld = [m2 for m2 in L.LD_RE.finditer(h) if m2.start() >= he and '"FAQPage"' in m2.group(1)]
        if len(bodyld) != 1: p.append(f"BODY LD={len(bodyld)}")
        else:
            try:
                d = json.loads(bodyld[0].group(1))
                qs = [q["name"] for q in d["mainEntity"]]
                page = [q for q, _ in L.faq_items(fb.group(0))] if fb else []
                if qs != page: p.append("LD MISMATCH")
            except Exception as e:
                p.append("LD INVALID JSON")
            # placement: immediately after FAQ closing tag
            if fb:
                between = h[fb.end():bodyld[0].start()]
                if between.strip(): p.append("LD NOT ADJACENT")
        # CTA
        if not re.search(r'class="[^"]*article-cta-btn[^"]*"', h): p.append("NO CTA BTN")
        elif L.CTA_PHRASE[lang] not in h: p.append("NO CTA PHRASE")
        # question H2 ratio
        hs = [re.sub(r"<[^>]+>", "", x).strip() for x in re.findall(r"<h2\b[^>]*>([\s\S]*?)</h2>", a, re.I)]
        q = sum(1 for x in hs if x.endswith("?") or x.endswith("？") or (QEN.match(x) if lang == "en" else QZH.search(x)))
        if q < max(3, len(hs) // 2): p.append(f"QH2 {q}/{len(hs)}")
        # duplicate h2 text
        dup = [k for k, v in collections.Counter(hs).items() if v > 1 and k]
        if dup: p.append("DUPH2:" + "|".join(d[:18] for d in dup))
        # empty excerpts
        if re.search(r'<p class="recommended-card-excerpt">\s*</p>', h): p.append("EMPTY EXCERPT")
        if p: problems.append((s, lang, p))

print("total problem files:", len(problems))
for s, lang, p in problems:
    print(f"{s[:46]:46} {lang:6} {p}")
