#!/usr/bin/env python3
"""Final validation + report data for gbatch_001 (45 files)."""
import os
import re
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def cjk_count(s):
    return len(re.findall(r'[\u3400-\u9fff\uf900-\ufaff\u3000-\u303f\uff00-\uffef]', s))

def en_words(s):
    return len(re.findall(r"[A-Za-z][A-Za-z'\-]*", s))

def main():
    slugs = []
    with open(os.path.join(ROOT, "_batch_pipeline", "gap_batches", "gbatch_001.txt")) as fh:
        for line in fh:
            s = line.strip()
            if s:
                slugs.append(s)

    rows = []
    failures = []
    for slug in slugs:
        row = {"slug": slug}
        for lang, prefix in [("en", ""), ("zh-CN", "zh-cn/"), ("zh-TW", "zh-tw/")]:
            path = os.path.join(ROOT, prefix + "blog/articles/" + slug + ".html")
            row[lang] = {}
            if not os.path.exists(path):
                failures.append(f"{slug}/{lang}: MISSING FILE")
                continue
            with open(path, encoding="utf-8") as fh:
                html = fh.read()

            # body article content
            m = re.search(r'<article id="article-content">(.*?)</article>', html, re.S)
            body = m.group(1) if m else html

            if lang == "en":
                row[lang]["words"] = en_words(body)
            else:
                row[lang]["cjk"] = cjk_count(body)

            # FAQ section + h3 questions
            faq_secs = re.findall(r'class="faq-section"', html)
            h3_faq = len(re.findall(r'<h3>[^<]', html))  # rough; refine below
            # count h3 strictly inside faq-section
            faq_block = re.search(r'class="faq-section".*?</section>', html, re.S)
            h3_in_faq = 0
            if faq_block:
                h3_in_faq = len(re.findall(r'<h3>', faq_block.group(0)))
            row[lang]["faq_h3"] = h3_in_faq
            row[lang]["faq_sec"] = len(faq_secs)

            # FAQPage JSON-LD count + location
            ld_all = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
            faq_ld_count = 0
            faq_ld_in_head = False
            faq_ld_in_body = False
            for i, block in enumerate(ld_all):
                if '"@type": "FAQPage"' in block or '"@type":"FAQPage"' in block:
                    faq_ld_count += 1
                    # determine head vs body by position relative to </head>
                    head_end = html.find('</head>')
                    idx = html.find(block)
                    if head_end != -1 and idx < head_end:
                        faq_ld_in_head = True
                    else:
                        faq_ld_in_body = True
            row[lang]["faq_ld"] = faq_ld_count
            row[lang]["faq_ld_head"] = faq_ld_in_head
            row[lang]["faq_ld_body"] = faq_ld_in_body

            # CTA phrase
            cta = "Book a Demo" if lang == "en" else ("预约演示" if lang == "zh-CN" else "預約示範")
            row[lang]["cta_ok"] = (cta in html)

            # undefined text
            row[lang]["undefined"] = ('undefined' in html.lower())

            # ?v=20260826 preserved
            row[lang]["cssv"] = ('/css/article.css?v=20260826' in html)
            row[lang]["jsv"] = ('/js/article.js?v=20260826' in html)

            # recommended card hrefs root-relative / language-prefixed
            recs = re.findall(r'class="recommended-card"[^>]*href="([^"]*)"', html)
            bad_rec = [r for r in recs if not r.startswith('/') and not r.startswith('http')]
            row[lang]["rec_bad"] = len(bad_rec)

            # lang attribute for zh files
            if lang != "en":
                ml = re.search(r'<html lang="([^"]*)"', html)
                row[lang]["html_lang"] = ml.group(1) if ml else "?"

        rows.append(row)

    # Print concise validation
    print("SLUG | ENw | zhCN-cjk | zhTW-cjk | FAQ(h3/ld) | CTA | undef | recbad | css/js v")
    for r in rows:
        en = r["en"]; cn = r["zh-CN"]; tw = r["zh-TW"]
        flag = ""
        if en["words"] < 2500: flag += " EN<2500"
        if cn["cjk"] < 3500: flag += " CN<3500"
        if tw["cjk"] < 3500: flag += " TW<3500"
        if not (en["cta_ok"] and cn["cta_ok"] and tw["cta_ok"]): flag += " CTA!"
        if en["undefined"] or cn["undefined"] or tw["undefined"]: flag += " UNDEF!"
        if en["rec_bad"] or cn["rec_bad"] or tw["rec_bad"]: flag += " REC!"
        if not (en["cssv"] and cn["cssv"] and tw["cssv"] and en["jsv"] and cn["jsv"] and tw["jsv"]): flag += " VER!"
        if tw["html_lang"] != "zh-tw": flag += " TWlang!"
        if not (tw["faq_ld"] == 1 and tw["faq_ld_body"]): flag += " TWLD!"
        print(f"{r['slug'][:38]:38} | {en['words']:5} | {cn['cjk']:5} | {tw['cjk']:5} | "
              f"{en['faq_h3']}/{en['faq_ld']} {cn['faq_h3']}/{cn['faq_ld']} {tw['faq_h3']}/{tw['faq_ld']} | "
              f"{'Y' if en['cta_ok'] and cn['cta_ok'] and tw['cta_ok'] else 'N'} | "
              f"{'Y' if en['undefined'] or cn['undefined'] or tw['undefined'] else 'N'} | "
              f"{en['rec_bad']+cn['rec_bad']+tw['rec_bad']} | {flag}")

    print("\nFAILURES:", failures if failures else "none")

if __name__ == "__main__":
    main()
