#!/usr/bin/env python3
"""Backfill FAQPage JSON-LD from existing FAQ HTML (no LLM needed).
Replaces any existing FAQPage ld+json script, or inserts one before </article>
if none exists. Only acts on files that have a FAQ section."""
import re, json, os

BASE = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
LANGS = [
    ("blog/articles", "en"),
    ("zh-cn/blog/articles", "zh-cn"),
    ("zh-tw/blog/articles", "zh-tw"),
]
STATUS = os.path.join(BASE, "_batch_pipeline/status.json")

def faq_section(art):
    m = re.search(r'<section[^>]*class="[^"]*faq-section[^"]*"[^>]*>([\s\S]*?)</section>', art, re.I)
    if m: return m.group(1)
    m = re.search(r'<[^>]*id="faq"[^>]*>([\s\S]*?)</section>', art, re.I)
    return m.group(1) if m else ""

def extract_qa(art):
    seg = faq_section(art)
    if not seg: return []
    blocks = re.split(r'<div class="faq-item"', seg)
    qa = []
    for b in blocks[1:]:
        qm = re.search(r'faq-question-text"[^>]*>([\s\S]*?)(?:<svg|</button)', b)
        if not qm:
            qm = re.search(r'<h3[^>]*>([\s\S]*?)</h3>', b)
        if not qm: continue
        q = re.sub(r'<[^>]+>', '', qm.group(1))
        q = re.sub(r'^\s*\d+\s*', '', q).strip()
        am = re.search(r'faq-answer-inner"[^>]*>([\s\S]*?)</div>', b) or re.search(r'faq-answer"[^>]*>([\s\S]*?)</div>', b)
        a = re.sub(r'<[^>]+>', ' ', am.group(1)) if am else ""
        a = re.sub(r'\s+', ' ', a).strip()
        if q and a: qa.append((q, a))
    return qa

def build_jsonld(qa):
    main = [{"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]
    obj = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": main}
    s = json.dumps(obj, ensure_ascii=False, indent=2)
    s = s.replace("</", "<\\/")  # prevent </script> breakout
    return '<script type="application/ld+json">\n' + s + "\n</script>"

def replace_or_insert(h, new_script):
    # find existing FAQPage ld+json block
    for m in re.finditer(r'<script type="application/ld\+json">([\s\S]*?)</script>', h):
        if 'faqpage' in m.group(1).lower():
            return h[:m.start()] + new_script + h[m.end():]
    # else insert before </article>
    i = h.rfind("</article>")
    if i >= 0:
        return h[:i] + "\n" + new_script + "\n" + h[i:]
    # fallback before </body>
    i = h.rfind("</body>")
    if i >= 0:
        return h[:i] + "\n" + new_script + "\n" + h[i:]
    return h + "\n" + new_script

def main():
    status = json.load(open(STATUS))
    slugs = list(status["slugs"].keys())
    stats = {"added": 0, "replaced": 0, "skipped_no_faq": 0, "skipped_zero_qa": 0, "errors": 0}
    for s in slugs:
        for sub, lang in LANGS:
            p = os.path.join(BASE, sub, s + ".html")
            if not os.path.exists(p): continue
            try:
                h = open(p, encoding="utf-8").read()
            except Exception:
                stats["errors"] += 1; continue
            qa = extract_qa(h)
            if not qa:
                stats["skipped_no_faq"] += 1; continue
            if len(qa) < 1:
                stats["skipped_zero_qa"] += 1; continue
            new_script = build_jsonld(qa)
            had = 'faqpage' in h.lower()
            h2 = replace_or_insert(h, new_script)
            if h2 != h:
                open(p, "w", encoding="utf-8").write(h2)
                stats["replaced" if had else "added"] += 1
            else:
                stats["errors"] += 1
    print("JSON-LD backfill stats:", json.dumps(stats, ensure_ascii=False))

if __name__ == "__main__":
    main()
