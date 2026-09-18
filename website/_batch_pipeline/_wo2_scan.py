import re, os, json

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
WO = os.path.join(ROOT, "_batch_pipeline/wo_faq_2.txt")
files = [l.strip() for l in open(WO, encoding="utf-8") if l.strip()]
CJK = re.compile(r"[\u4e00-\u9fff]")

def strip(t):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip()

def variant(s):
    if re.search(r'<h3 class="faq-question-text"><span class="faq-number">', s): return "V5"
    if re.search(r'<span class="faq-question-text"><span class="faq-number">\d+</span><span>', s): return "V1"
    if re.search(r'<h3 class="faq-question-text"[^>]*>', s): return "V2"
    if re.search(r'<span class="faq-question-text"><span class="faq-number">\d+</span><h3 class="faq-q"', s): return "V3"
    if re.search(r'<span class="faq-question-text"><span class="faq-number">\d+</span>', s): return "V4"
    return "?"

def questions(s, v):
    if v == "V1":
        return [strip(x) for x in re.findall(
            r'<span class="faq-question-text"><span class="faq-number">\d+</span><span>(.*?)</span>\s*</span>', s, re.S)]
    if v == "V2":
        return [strip(x) for x in re.findall(
            r'<h3 class="faq-question-text"[^>]*>(.*?)</h3>', s, re.S)]
    if v == "V3":
        return [strip(x) for x in re.findall(
            r'<span class="faq-question-text"><span class="faq-number">\d+</span><h3 class="faq-q"[^>]*>(.*?)</h3>', s, re.S)]
    if v == "V4":
        return [strip(x) for x in re.findall(
            r'<span class="faq-question-text"><span class="faq-number">\d+</span>(.*?)</span>', s, re.S)]
    if v == "V5":
        return [strip(x) for x in re.findall(
            r'<h3 class="faq-question-text"><span class="faq-number">\d+</span><span>(.*?)</span>\s*</h3>', s, re.S)]
    return []

out = {}
for rel in files:
    s = open(os.path.join(ROOT, rel), encoding="utf-8").read()
    d = {}
    m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    d["h1"] = strip(m.group(1)) if m else None
    m = re.search(r'class="[^"]*article-lead[^"]*"[^>]*>(.*?)</p>', s, re.S)
    d["lead"] = strip(m.group(1))[:600] if m else None

    hs = []
    for mm in re.finditer(r"<(h2|h3)([^>]*)>(.*?)</\1>", s, re.S):
        t = strip(mm.group(3))
        if not t or t in ("常见问题",): continue
        idm = re.search(r'id="([^"]*)"', mm.group(2))
        cls = re.search(r'class="([^"]*)"', mm.group(2))
        if cls and "faq" in cls.group(1): continue
        hs.append({"tag": mm.group(1), "id": idm.group(1) if idm else None,
                   "txt": t, "en": not CJK.search(t)})
    d["h"] = hs

    v = variant(s)
    d["v"] = v
    d["q"] = questions(s, v)
    d["a"] = [re.sub(r"\s+", " ", x).strip() for x in
              re.findall(r'<div class="faq-answer-inner">(.*?)</div>', s, re.S)]
    d["n_item"] = len(re.findall(r'<div class="faq-item"', s))

    ld = []
    for mm in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: j = json.loads(mm.group(1).strip())
        except Exception: continue
        for o in (j if isinstance(j, list) else [j]):
            if isinstance(o, dict) and o.get("@type") == "FAQPage":
                for it in o.get("mainEntity", []):
                    ld.append({"q": it.get("name"), "a": (it.get("acceptedAnswer") or {}).get("text")})
    d["ld"] = ld
    d["undef"] = s.count("undefined")
    d["ndiv_o"] = len(re.findall(r"<div\b", s)); d["ndiv_c"] = len(re.findall(r"</div>", s))
    out[rel] = d

json.dump(out, open(os.path.join(ROOT, "_batch_pipeline/_wo2_scan.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print(f"{'file':46} {'v':3}{'nQ':>3}{'nA':>3}{'nLD':>4}{'item':>5}{'und':>5}{'enH':>4}")
for rel, d in out.items():
    print(f"{rel.split('/')[-1][:44]:46} {d['v']:3}{len(d['q']):3}{len(d['a']):3}"
          f"{len(d['ld']):4}{d['n_item']:5}{d['undef']:5}{len([h for h in d['h'] if h['en']]):4}")
