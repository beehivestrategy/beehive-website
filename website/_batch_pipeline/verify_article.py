#!/usr/bin/env python3
"""
verify_article.py — checks a single rewritten blog article against the design
standard. Returns exit code 0 if PASS, 1 if FAIL (with reasons printed).

Usage: python3 verify_article.py <path> [en|zh-cn|zh-tw]
"""
import re, sys, json

def main():
    if len(sys.argv) < 2:
        print("usage: verify_article.py <path> [lang]")
        sys.exit(2)
    path = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) > 2 else "en"
    h = open(path, encoding="utf-8").read()
    errors = []

    # 1. extract article region: from <article class="article"> to last </article>
    a_start = h.find('<article class="article">')
    if a_start == -1:
        a_start = h.find('<div class="article-content">')
    if a_start == -1:
        print("FAIL: no article block found")
        sys.exit(1)
    end = h.rfind('</article>')
    body = h[a_start:end]

    # 2. balanced divs inside body
    opens = len(re.findall(r'<div\b', body))
    closes = len(re.findall(r'</div>', body))
    if opens != closes:
        errors.append(f"unbalanced divs: {opens} open / {closes} close")

    # 3. CTA block present (case-insensitive)
    if 'class="cta' not in body and 'book a demo' not in body.lower():
        errors.append("missing CTA block / 'Book a demo'")

    # 4. FAQ block present
    if 'faq-section' not in body:
        errors.append("missing faq-section")

    # 5. FAQ JSON-LD present and valid
    lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    faq_ld = None
    for ld in lds:
        if '"FAQPage"' in ld or '"@type":"FAQPage"' in ld:
            faq_ld = ld
    if not faq_ld:
        errors.append("missing FAQPage JSON-LD")
    else:
        try:
            obj = json.loads(faq_ld)
            # unwrap @graph if present
            if isinstance(obj, dict) and "@graph" in obj:
                obj = [x for x in obj["@graph"] if x.get("@type") == "FAQPage"]
                obj = obj[0] if obj else {}
            me = obj.get("mainEntity", [])
            if not isinstance(me, list) or len(me) < 3:
                errors.append(f"FAQPage mainEntity too few ({len(me) if isinstance(me,list) else 'n/a'})")
        except Exception as e:
            errors.append(f"FAQPage JSON-LD invalid: {e}")

    # 6. hreflang alternates (en/zh-CN/zh-TW/x-default) — only check article heads
    for tag in ["en", "zh-CN", "zh-TW", "x-default"]:
        if f'hreflang="{tag}"' not in h:
            errors.append(f"missing hreflang {tag}")

    # 7. canonical correct for lang
    if lang == "zh-tw":
        if '/zh-tw/' not in re.search(r'rel="canonical"', h).group(0) if re.search(r'rel="canonical"', h) else True:
            # more robust: check canonical url contains zh-tw
            cm = re.search(r'<link[^>]*rel="canonical"[^>]*>', h)
            if cm and '/zh-tw/' not in cm.group(0):
                errors.append("zh-tw canonical not pointing to /zh-tw/")
    if lang == "zh-cn":
        cm = re.search(r'<link[^>]*rel="canonical"[^>]*>', h)
        if cm and '/zh-cn/' not in cm.group(0):
            errors.append("zh-cn canonical not pointing to /zh-cn/")

    # 8. og:locale for zh
    if lang in ("zh-cn", "zh-tw"):
        ol = re.search(r'og:locale"[^>]*content="([^"]+)"', h)
        expected = "zh_CN" if lang == "zh-cn" else "zh_TW"
        if not ol or ol.group(1) != expected:
            errors.append(f"og:locale should be {expected}")

    # 9. length floor
    if lang == "en":
        t = re.sub(r'<[^>]+>', ' ', body)
        t = re.sub(r'&[a-z]+;', ' ', t); t = re.sub(r'\s+', ' ', t)
        wc = len(t.split())
        if wc < 2500:
            errors.append(f"EN word count {wc} < 2500 floor")
    else:
        cjk = re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', body)
        if len(cjk) < 3500:
            errors.append(f"CJK count {len(cjk)} < 3500 floor")

    # 10. no placeholder text
    for bad in ["Lorem", "TODO", "TBD", "coming soon", "占位", "待补充"]:
        if bad.lower() in body.lower():
            errors.append(f"placeholder text found: {bad}")

    if errors:
        print(f"FAIL {path}")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print(f"PASS {path}")

if __name__ == "__main__":
    main()
