import re, os, json

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
WO = os.path.join(ROOT, "_batch_pipeline/wo_faq_2.txt")
files = [l.strip() for l in open(WO, encoding="utf-8") if l.strip()]
CJK = re.compile(r"[\u4e00-\u9fff]")

out = {}
for rel in files:
    p = os.path.join(ROOT, rel)
    s = open(p, encoding="utf-8").read()
    d = {"size": len(s)}

    m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    d["h1"] = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else None

    m = re.search(r'class="[^"]*article-lead[^"]*"[^>]*>(.*?)</p>', s, re.S)
    d["lead"] = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()[:500] if m else None

    hs = []
    for mm in re.finditer(r"<(h2|h3)([^>]*)>(.*?)</\1>", s, re.S):
        txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", mm.group(3))).strip()
        if not txt or txt == "常见问题":
            continue
        idm = re.search(r'id="([^"]*)"', mm.group(2))
        hs.append({"tag": mm.group(1), "id": idm.group(1) if idm else None,
                   "txt": txt, "en": not CJK.search(txt)})
    d["h"] = hs

    # faq: style A = h3.faq-question-text ; style B = span.faq-question-text > span
    faq, style = [], None
    qa = re.findall(r'<h3 class="faq-question-text"[^>]*>(.*?)</h3>', s, re.S)
    if qa:
        style = "A"
        for q in qa:
            faq.append({"q": re.sub(r"<[^>]+>", "", q).strip(), "a": None})
        ai = 0
        for mm in re.finditer(r'<div class="faq-answer-inner">(.*?)</div>', s, re.S):
            if ai < len(faq):
                faq[ai]["a"] = mm.group(1).strip()
            ai += 1
    else:
        style = "B"
        for q in re.findall(r'<span class="faq-question-text"><span class="faq-number">\d+</span><span>(.*?)</span>\s*</span>', s, re.S):
            faq.append({"q": re.sub(r"<[^>]+>", "", q).strip(), "a": None})
        ai = 0
        for mm in re.finditer(r'<div class="faq-answer-inner">(.*?)</div>', s, re.S):
            if ai < len(faq):
                faq[ai]["a"] = mm.group(1).strip()
            ai += 1
    d["faq"], d["style"] = faq, style
    d["n_ans"] = len(re.findall(r'<div class="faq-answer-inner">', s))

    ld = []
    for mm in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            j = json.loads(mm.group(1).strip())
        except Exception:
            continue
        for obj in (j if isinstance(j, list) else [j]):
            if isinstance(obj, dict) and obj.get("@type") == "FAQPage":
                for it in obj.get("mainEntity", []):
                    ld.append({"q": it.get("name"), "a": it.get("acceptedAnswer", {}).get("text")})
    d["ld"] = ld

    d["undef_faq"] = ("undefined" in json.dumps(faq, ensure_ascii=False))
    d["n_undef"] = s.count("undefined")
    d["enh"] = [h for h in hs if h["en"]]
    out[rel] = d

json.dump(out, open(os.path.join(ROOT, "_batch_pipeline/_wo2_extract.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print(f"{'file':46} {'sty':3} {'nQ':>3} {'nLD':>4} {'undef':>6} {'enH':>4} {'matches':>8}")
for rel, d in out.items():
    ok = (len(d["faq"]) == len(d["ld"]) == d["n_ans"]) and not d["undef_faq"]
    print(f"{rel.split('/')[-1][:44]:46} {d['style']:3} {len(d['faq']):3} {len(d['ld']):4} "
          f"{d['n_undef']:6} {len(d['enh']):4} {'OK' if ok else 'NEED':>8}")
