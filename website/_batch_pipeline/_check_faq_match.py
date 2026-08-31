#!/usr/bin/env python3
"""Verify FAQPage JSON-LD questions match on-page <h3> FAQ questions for all 45
files. Reports whether JSON-LD is in head or body and match status."""
import os
import re
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def norm(s):
    return re.sub(r'\s+', '', s).strip()


def main():
    slugs = []
    with open(os.path.join(ROOT, "_batch_pipeline", "gap_batches", "gbatch_001.txt")) as fh:
        for line in fh:
            s = line.strip()
            if s:
                slugs.append(s)

    mismatches = []
    for slug in slugs:
        for lang, prefix in [("en", ""), ("zh-CN", "zh-cn/"), ("zh-TW", "zh-tw/")]:
            path = os.path.join(ROOT, prefix + "blog/articles/" + slug + ".html")
            if not os.path.exists(path):
                continue
            with open(path, encoding="utf-8") as fh:
                html = fh.read()

            # on-page FAQ h3 questions
            faq_block = re.search(r'class="faq-section".*?</section>', html, re.S)
            if not faq_block:
                mismatches.append(f"{slug}/{lang}: NO faq-section")
                continue
            h3s = re.findall(r'<h3>(.*?)</h3>', faq_block.group(0), re.S)
            onpage = [norm(re.sub(r'<[^>]+>', '', q)) for q in h3s]

            # FAQPage JSON-LD
            blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
            faq_ld = None
            loc = None
            head_end = html.find('</head>')
            for b in blocks:
                if '"@type": "FAQPage"' in b or '"@type":"FAQPage"' in b:
                    faq_ld = b
                    idx = html.find(b)
                    loc = 'head' if (head_end != -1 and idx < head_end) else 'body'
                    break
            if not faq_ld:
                mismatches.append(f"{slug}/{lang}: NO FAQPage LD")
                continue
            try:
                data = json.loads(faq_ld)
            except Exception as e:
                mismatches.append(f"{slug}/{lang}: JSON parse error {e}")
                continue
            qa = data.get("mainEntity", [])
            ld_qs = [norm(q.get("name", "")) for q in qa]

            if len(onpage) != len(ld_qs):
                mismatches.append(f"{slug}/{lang}: COUNT mismatch onpage={len(onpage)} ld={len(ld_qs)} (loc={loc})")
                continue
            for i, (a, l) in enumerate(zip(onpage, ld_qs)):
                if a != l:
                    mismatches.append(f"{slug}/{lang}: Q{i} mismatch loc={loc}\n   onpage={a[:30]}\n   ld    ={l[:30]}")
    if mismatches:
        print("MISMATCHES:")
        for m in mismatches:
            print(" -", m)
    else:
        print("ALL FAQPage JSON-LD match on-page FAQ; locations: head permitted per brief.")


if __name__ == "__main__":
    main()
