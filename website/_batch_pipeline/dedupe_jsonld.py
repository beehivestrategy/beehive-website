#!/usr/bin/env python3
"""Remove redundant FAQPage JSON-LD blocks. Keep the LAST occurrence in document
order (the agent-maintained body block that matches the on-page FAQ); drop any
earlier duplicate (typically a stale head copy). Validates JSON; if the last
block fails to parse, keeps the earlier valid one instead. Reports anything
suspicious for manual review."""
import os, re, glob, json

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
LANGS = {"en": "blog/articles", "cn": "zh-cn/blog/articles", "tw": "zh-tw/blog/articles"}

ld_re = re.compile(r'<script\s+type="application/ld\+json"[^>]*>.*?</script>', re.S | re.I)
faq_re = re.compile(r'"@type"\s*:\s*"FAQPage"')

def valid_faq(block):
    try:
        data = json.loads(block)
    except Exception:
        return None
    if isinstance(data, dict) and data.get("@graph"):
        for n in data["@graph"]:
            if n.get("@type") == "FAQPage":
                return n
    if isinstance(data, dict) and data.get("@type") == "FAQPage":
        return data
    return None

def onpage_faq_questions(html):
    # pull .faq-question-text text
    q = re.findall(r'class="faq-question-text"[^>]*>(.*?)</', html, re.S)
    return [re.sub(r"\s+", " ", x).strip().lower() for x in q]

files = []
for d in LANGS.values():
    files += glob.glob(os.path.join(ROOT, d, "*.html"))

removed_total = 0
review = []
for f in files:
    try:
        html = open(f, encoding="utf-8").read()
    except Exception:
        continue
    matches = list(ld_re.finditer(html))
    faq_m = [m for m in matches if faq_re.search(m.group(0))]
    if len(faq_m) <= 1:
        continue
    # candidate blocks (the JSON inside) in doc order
    cand = []
    for m in faq_m:
        inner = m.group(0)
        js = re.search(r'>(.*)</script>', inner, re.S).group(1)
        cand.append((m.start(), m.end(), js))
    # prefer the LAST; fallback to first valid
    keep_idx = len(cand) - 1
    if valid_faq(cand[keep_idx][2]) is None:
        alt = [i for i, c in enumerate(cand) if valid_faq(c[2]) is not None]
        if alt:
            keep_idx = alt[-1]
    keep = cand[keep_idx]
    # remove all others
    to_remove = sorted([c for i, c in enumerate(cand) if i != keep_idx], key=lambda c: c[0], reverse=True)
    new_html = html
    for (s, e, _) in to_remove:
        new_html = new_html[:s] + new_html[e:]
    # light blank-line cleanup
    new_html = re.sub(r"\n{3,}", "\n\n", new_html)
    if new_html != html:
        open(f, "w", encoding="utf-8").write(new_html)
        removed_total += len(to_remove)
    # sanity: does kept block match on-page FAQ count?
    vf = valid_faq(keep[2])
    onp = onpage_faq_questions(html)
    kept_q = 0
    if vf and isinstance(vf.get("mainEntity"), list):
        kept_q = len(vf["mainEntity"])
    if onp and kept_q and abs(kept_q - len(onp)) > 1:
        review.append((f.split("website")[-1], kept_q, len(onp)))

print(f"Files deduplicated: {removed_total and 'yes' or 'check'}")
print(f"Total redundant blocks removed: {removed_total}")
print(f"Files needing manual FAQ-match review: {len(review)}")
for r in review[:20]:
    print("  ", r)
