import re, json, sys, os

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
wo = open(os.path.join(ROOT, "_batch_pipeline/wo_faq_1.txt")).read().split()
paths = [p.strip() for p in wo if p.strip()]

def txt(s):
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\s+', ' ', s).strip()

for rel in paths:
    fp = os.path.join(ROOT, rel)
    src = open(fp, encoding='utf-8').read()
    print("="*100)
    print("FILE:", rel, "size", len(src))
    # H1
    for m in re.finditer(r'<h1[^>]*>(.*?)</h1>', src, re.S):
        print("H1:", txt(m.group(1))[:200])
    # lead
    for m in re.finditer(r'class="[^"]*article-lead[^"]*"[^>]*>(.*?)</p>', src, re.S):
        print("LEAD:", txt(m.group(1))[:400])
    # h2/h3
    for m in re.finditer(r'<(h2|h3)([^>]*)>(.*?)</\1>', src, re.S):
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        t = txt(inner)
        idm = re.search(r'id="([^"]+)"', attrs)
        has_cjk = bool(re.search(r'[一-鿿]', t))
        flag = "" if has_cjk else "  <<< ENGLISH"
        print(f"{tag.upper()} [id={idm.group(1) if idm else ''}]: {t[:160]}{flag}")
    # FAQ
    print("--- FAQ ---")
    for m in re.finditer(r'class="faq-item"[^>]*>(.*?)</div>\s*</div>\s*(?=<div class="faq-item"|<div class="faqcta|</section)', src, re.S):
        blk = m.group(1)
        qt = re.search(r'faq-question-text">(.*?)</span>\s*</span>', blk, re.S)
        qn = re.search(r'faq-number">(\d+)', blk)
        ans = re.search(r'faq-answer-inner">(.*?)</div>', blk, re.S)
        print(" Q", qn.group(1) if qn else "?", ":", txt(qt.group(1))[:150] if qt else "NONE")
        print(" A:", txt(ans.group(1))[:200] if ans else "NONE")
    # JSON-LD FAQPage
    print("--- JSONLD ---")
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', src, re.S):
        try:
            d = json.loads(m.group(1))
        except Exception as e:
            print("  parse error", e); continue
        objs = d if isinstance(d, list) else [d]
        for o in objs:
            if isinstance(o, dict) and o.get("@type") == "FAQPage":
                me = o.get("mainEntity", [])
                print("  mainEntity count:", len(me))
                for i, q in enumerate(me, 1):
                    print(f"   {i}. Q: {q.get('name','')[:120]}")
                    print(f"      A: {q.get('acceptedAnswer',{}).get('text','')[:200]}")
    # undefined check
    und = [m.start() for m in re.finditer(r'>undefined<', src)]
    if und:
        print("!!! 'undefined' visible count:", len(und))
