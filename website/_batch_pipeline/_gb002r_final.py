#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final audit for gbatch_002."""
import html as H
import json
import os
import re
import sys

sys.path.insert(0, '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline')
import _gb002r_lib as L

SLUGS = [l.strip() for l in open('/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline/gap_batches/gbatch_002.txt') if l.strip()]
BK = '/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/_batch_pipeline/_backup_gb002r'
PREFIX = {"EN": "EN", "zh-CN": "CN", "zh-TW": "TW"}
DEMO = {"EN": "Book a Demo", "zh-CN": "预约演示", "zh-TW": "預約示範"}
QEN = re.compile(r'^(how|what|why|when|which|where|who|can|do|does|is|are|should|will|has|have)\b', re.I)
QZH = re.compile(r'(如何|甚|什|为什麼|為什麼|为何|為何|為什|怎么|怎樣|怎样|是否|哪些|哪些|多少|哪裡|哪里|該如|该如何|應該如|무)')

rows = []
problems = []
for slug in SLUGS:
    for lang, pat in L.LANGS:
        rel = pat % slug
        h = L.read(rel)
        body = re.search(r'<body[^>]*>(.*?)</body>', h, re.S | re.I).group(1)
        inner = L.art(h)
        wc = L.en_words(h) if lang == "EN" else L.cjk(h)
        # FAQ
        faq = L.faq_items(inner)
        h3 = len(re.findall(r'<h3 class="faq-question-heading"', inner))
        # JSON-LD in body
        lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', body, re.S)
        faq_lds = [s for s in lds if '"FAQPage"' in s]
        match = False
        if faq_lds:
            try:
                d = json.loads(faq_lds[0].strip())
                me = d.get("mainEntity", [])
                match = (len(me) == len(faq) and
                         all(m["name"] == q and
                             m["acceptedAnswer"]["text"] == a
                             for m, (q, a) in zip(me, faq)))
            except Exception as e:
                problems.append(f"{rel}: JSON-LD parse error {e}")
        # placement: JSON-LD right after FAQ section
        placed = False
        b = L.faq_bounds(inner)
        if b:
            tail = inner[b[1]:]
            m = re.match(r'</section>\s*<script type="application/ld\+json">', tail)
            placed = bool(m)
        # head unchanged
        ob = open(os.path.join(BK, "%s_%s.html" % (PREFIX[lang], slug)), encoding='utf-8').read()
        head_same = ob.split('<body', 1)[0] == h.split('<body', 1)[0]
        # CTA
        cta = ('class="article-cta-btn"' in h) and (DEMO[lang] in h)
        # H2 questions
        h2s = [re.sub(r'<[^>]+>', '', x).strip() for x in re.findall(r'<h2[^>]*>(.*?)</h2>', inner, re.S)]
        h2_body = [x for x in h2s if not x.startswith(('Frequently', '常见', '常見'))]
        notq = [x for x in h2_body if not (QEN.match(x) if lang == "EN" else (x.endswith(('？', '?')) or QZH.search(x)))]
        # defects
        und = len(re.findall(r'undefined', inner))
        txt = re.sub(r'<[^>]+>', ' ', inner)
        cjk_n = len(re.findall(r'[\u4e00-\u9fff]', txt))
        eng_head = []
        if lang != "EN":
            eng_head = [x for x in h2_body if cjk_n and not re.search(r'[\u4e00-\u9fff]', x)]
        rows.append(dict(slug=slug, lang=lang, wc=wc, faq=len(faq), h3=h3,
                         nld=len(lds), faqld=len(faq_lds), match=match, placed=placed,
                         head=head_same, cta=cta, notq=notq, und=und, eng_head=eng_head))
        if len(faq) < 3:
            problems.append(f"{rel}: FAQ {len(faq)}")
        if h3 != len(faq):
            problems.append(f"{rel}: h3 {h3} != faq {len(faq)}")
        if len(faq_lds) != 1:
            problems.append(f"{rel}: body FAQPage JSON-LD count {len(faq_lds)}")
        if not match:
            problems.append(f"{rel}: JSON-LD does not match on-page FAQ")
        if not placed:
            problems.append(f"{rel}: JSON-LD not right after FAQ section")
        if not head_same:
            problems.append(f"{rel}: HEAD CHANGED")
        if not cta:
            problems.append(f"{rel}: CTA/demo phrase missing")
        if und:
            problems.append(f"{rel}: undefined x{und} in body")
        if eng_head:
            problems.append(f"{rel}: non-Chinese H2 {eng_head}")
        floor = 2500 if lang == "EN" else 3500
        if wc < floor:
            problems.append(f"{rel}: {wc} < {floor}")

print("%-52s %-6s %6s %4s %4s %3s %5s %6s %5s %5s  %s" %
      ("slug", "lang", "count", "faq", "h3", "ld", "match", "placed", "head", "cta", "non-question H2"))
for r in rows:
    print("%-52s %-6s %6d %4d %4d %3d %5s %6s %5s %5s  %s" %
          (r["slug"][:52], r["lang"], r["wc"], r["faq"], r["h3"], r["faqld"],
           r["match"], r["placed"], r["head"], r["cta"], ("; ".join(r["notq"])[:90] or "-")))
print()
if problems:
    print("PROBLEMS (%d):" % len(problems))
    for p in problems:
        print("  -", p)
else:
    print("NO PROBLEMS")
