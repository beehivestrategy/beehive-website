#!/usr/bin/env python3
"""Deep-dive SEO/GEO audit across all 1061 slugs x 3 languages (3183 files).

Multi-dimensional checks (scanning the correct document regions):
  - title presence/length + known-broken (from broken_titles.json) + untranslated (zh with no CJK)
  - meta description presence/length (script-aware thresholds)
  - exactly one H1 (full document)
  - heading hierarchy (H2 exists, no H3 before H2) within article body
  - question-style H2 ratio (GEO signal)
  - canonical present + correct URL shape
  - hreflang set (en/zh-CN/zh-TW/x-default)  [case-insensitive]
  - OpenGraph + Twitter cards completeness
  - FAQ section present + >=3 Q/A (faq-item count, full document)
  - FAQPage JSON-LD: exactly one, valid JSON, matches FAQ count
  - all JSON-LD blocks parse
  - CTA card present
  - internal link integrity (target file exists)
  - image alt coverage
  - same-page anchor integrity
  - length floor (en>=2500 words, zh>=3500 CJK)
  - site-level duplicate H1 / title / meta-description per language

Outputs: deep_audit.json (machine) + prints aggregate. HTML report built separately.
Run: python3 deep_audit.py
"""
import os, re, json, glob
from collections import defaultdict

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
LANGS = {"en": "blog/articles", "cn": "zh-cn/blog/articles", "tw": "zh-tw/blog/articles"}
SITE = "https://www.beehivestrategy.com"

def read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None

def cjk_count(s):
    return len(re.findall(r"[\u4e00-\u9fff\u3400-\u4dbf]", s))

def word_count(s):
    return len(re.findall(r"[A-Za-z][A-Za-z'-]*", s))

def body_text(html):
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', html, re.S|re.I)
    return m.group(1) if m else html

def head_text(html):
    m = re.search(r'<head[^>]*>(.*?)</head>', html, re.S|re.I)
    return m.group(1) if m else ""

def get_meta(head, name):
    m = re.search(r'<meta\s+name=["\']'+re.escape(name)+r'["\'][^>]*content=["\'](.*?)["\']', head, re.I|re.S)
    if not m:
        m = re.search(r'<meta\s+property=["\']'+re.escape(name)+r'["\'][^>]*content=["\'](.*?)["\']', head, re.I|re.S)
    return m.group(1) if m else None

def get_title(head):
    m = re.search(r'<title[^>]*>(.*?)</title>', head, re.S|re.I)
    return m.group(1).strip() if m else None

def all_ld(html):
    blocks = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.S|re.I)
    out = []
    for b in blocks:
        try:
            out.append(json.loads(b))
        except Exception:
            out.append({"__invalid__": True})
    return out

def find_faqpage(ld_list):
    cnt = 0; questions = 0
    for obj in ld_list:
        if not isinstance(obj, dict) or obj.get("__invalid__"):
            continue
        def walk(o):
            nonlocal cnt, questions
            if isinstance(o, dict):
                t = o.get("@type")
                if isinstance(t, str) and "FAQPage" in t:
                    cnt += 1
                    me = o.get("mainEntity", [])
                    if isinstance(me, list): questions += len(me)
                elif isinstance(t, list) and any(isinstance(x,str) and "FAQPage" in x for x in t):
                    cnt += 1
                for v in o.values(): walk(v)
            elif isinstance(o, list):
                for v in o: walk(v)
        walk(obj)
    return cnt, questions

def extract_hrefs(body):
    return re.findall(r'href=["\']([^"\']+)["\']', body, re.I)

def extract_imgs(body):
    return re.findall(r'<img\b[^>]*>', body, re.I)

def extract_ids(body):
    return set(re.findall(r'\bid=["\']([^"\']+)["\']', body, re.I))

# load known broken titles
broken_path = os.path.join(os.path.dirname(__file__), "broken_titles.json")
broken_titles = {}
if os.path.exists(broken_path):
    try:
        broken_titles = json.load(open(broken_path, encoding="utf-8"))
    except Exception:
        broken_titles = {}

# Collect slugs
batch_dir = os.path.join(ROOT, "_batch_pipeline/batches")
slugs = []
seen = set()
for bf in sorted(glob.glob(os.path.join(batch_dir, "batch_*.txt"))):
    for line in open(bf, encoding="utf-8"):
        s = line.strip()
        if s and s not in seen:
            seen.add(s); slugs.append(s)

records = {}
site_h1 = defaultdict(lambda: defaultdict(list))
site_title = defaultdict(lambda: defaultdict(list))
site_desc = defaultdict(lambda: defaultdict(list))

for slug in slugs:
    rec = {}
    for lang, d in LANGS.items():
        path = os.path.join(ROOT, d, slug + ".html")
        html = read(path)
        if html is None:
            rec[lang] = {"err": "missing"}
            continue
        head = head_text(html)
        body = body_text(html)
        issues = []

        # title (from head)
        title = get_title(head)
        if not title:
            issues.append("title_missing"); tl = 0
        else:
            tl = len(title)
            if lang in ("cn","tw"):
                has_cjk = bool(re.search(r"[\u4e00-\u9fff]", title))
                if not has_cjk:
                    issues.append("title_untranslated")
                elif slug in broken_titles and lang in broken_titles[slug]:
                    issues.append("title_known_broken")
            if lang == "en" and tl > 70:
                issues.append("title_long")
            if tl == 0:
                issues.append("title_empty")

        # meta description (script-aware)
        desc = get_meta(head, "description")
        if not desc:
            issues.append("desc_missing")
        else:
            dl = len(desc)
            if lang == "en":
                if dl < 50: issues.append("desc_short")
                if dl > 180: issues.append("desc_long")
            else:
                if dl < 35: issues.append("desc_short")
                if dl > 130: issues.append("desc_long")

        # H1 (full document)
        h1s = re.findall(r'<h1\b[^>]*>(.*?)</h1>', html, re.S|re.I)
        h1_texts = [re.sub(r"<[^>]+>","",h).strip() for h in h1s]
        h1_texts = [h for h in h1_texts if h]
        if len(h1_texts) == 0:
            issues.append("h1_missing")
        elif len(h1_texts) > 1:
            issues.append("h1_multiple")
        h1 = h1_texts[0] if h1_texts else ""

        # heading hierarchy (article body)
        h2s = re.findall(r'<h2\b', body, re.I)
        first_h = None
        m = re.search(r'<h[1-6]\b', body, re.I)
        if m: first_h = m.group(0).lower()
        if not h2s: issues.append("no_h2")
        if first_h and "h3" in first_h and h2s: issues.append("h3_before_h2")
        h2_all = re.findall(r'<h2\b[^>]*>(.*?)</h2>', body, re.S|re.I)
        h2_q = 0
        for h in h2_all:
            t = re.sub(r"<[^>]+>","",h).strip()
            if re.search(r"[?？]$", t) or re.match(r"^(how|what|why|when|which|where|can|do|does|is|are|will|should|who|whose|whom)\b", t, re.I) or re.match(r"^(如何|什么是|为什么|怎么|是否|怎样|哪|谁|何时|何)", t):
                h2_q += 1
        h2_ratio = round(h2_q/max(1,len(h2_all)), 2)

        # canonical
        can = None
        m = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', head, re.I)
        if m: can = m.group(1)
        else:
            m2 = re.search(r'<link[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\']canonical["\']', head, re.I)
            if m2: can = m2.group(1)
        if not can:
            issues.append("canonical_missing")
        else:
            expected_suffix = "/blog/articles/" + slug
            if lang == "cn": expected_suffix = "/zh-cn" + expected_suffix
            if lang == "tw": expected_suffix = "/zh-tw" + expected_suffix
            if not can.startswith(SITE) or not can.endswith(expected_suffix):
                issues.append("canonical_wrong")

        # hreflang (case-insensitive)
        alts = [a.lower() for a in re.findall(r'hreflang=["\']([^"\']+)["\']', head, re.I)]
        need = {"en","zh-cn","zh-tw","x-default"}
        have = set(alts)
        missing_hl = need - have
        if missing_hl:
            issues.append("hreflang_missing:"+",".join(sorted(missing_hl)))

        # OG + Twitter
        for og in ["og:type","og:title","og:description","og:url","og:image"]:
            if not get_meta(head, og): issues.append("og_missing:"+og)
        for tw in ["twitter:card","twitter:title","twitter:description","twitter:image"]:
            if not get_meta(head, tw): issues.append("tw_missing:"+tw)

        # FAQ section (full document) + item count
        faq_present = bool(re.search(r'class=["\'][^"\']*faq-section[^"\']*["\']', html, re.I))
        # NOTE: exclude faq-item-question / faq-item-answer etc. (substring collision)
        faq_items = len(re.findall(r'class=["\'][^"\']*faq-item(?!-)', html, re.I))
        if faq_items == 0:
            faq_items = len(re.findall(r'class=["\'][^"\']*faq-question[^"\']*["\']', html, re.I))
        if not faq_present and faq_items == 0:
            issues.append("faq_missing")
        elif faq_items < 3:
            issues.append("faq_lt3")

        # JSON-LD
        ld = all_ld(html)
        invalid = sum(1 for o in ld if isinstance(o,dict) and o.get("__invalid__"))
        if invalid: issues.append("jsonld_invalid")
        faq_cnt, faq_q = find_faqpage(ld)
        if faq_cnt == 0:
            issues.append("faqpage_jsonld_missing")
        elif faq_cnt > 1:
            issues.append("faqpage_jsonld_multiple")
        elif faq_present and faq_items >= 3 and faq_q != faq_items:
            issues.append("faqpage_jsonld_mismatch:%dvs%d"%(faq_q,faq_items))

        # CTA (full document)
        if "article-cta-btn" not in html:
            issues.append("cta_missing")

        # internal links integrity (body)
        hrefs = extract_hrefs(body)
        broken = 0
        for h in hrefs:
            if h.startswith("/blog/articles/") or h.startswith("/zh-cn/blog/articles/") or h.startswith("/zh-tw/blog/articles/"):
                clean = h.split("#")[0].split("?")[0]
                fpath = os.path.join(ROOT, clean.lstrip("/"))
                if not os.path.exists(fpath): broken += 1
        if broken: issues.append("broken_internal_links:%d"%broken)

        # image alt (body)
        imgs = extract_imgs(body)
        no_alt = sum(1 for im in imgs if not re.search(r'\balt=["\']', im, re.I))
        if no_alt: issues.append("img_no_alt:%d"%no_alt)

        # anchor integrity (body)
        ids = extract_ids(body)
        anchors = set(h[1:] for h in hrefs if h.startswith("#") and len(h) > 1)
        missing_anchor = anchors - ids
        if missing_anchor: issues.append("anchor_broken:%d"%len(missing_anchor))

        # length
        if lang == "en":
            wc = word_count(body); len_ok = wc >= 2500
            if not len_ok: issues.append("len_short:%d"%wc)
        else:
            cj = cjk_count(body); len_ok = cj >= 3500
            if not len_ok: issues.append("len_short:%d"%cj)

        # site-level dup tracking
        if h1: site_h1[lang][h1].append(slug)
        if title: site_title[lang][title].append(slug)
        if desc: site_desc[lang][desc].append(slug)

        rec[lang] = {
            "len_ok": len_ok,
            "faq_ok": faq_present and faq_items >= 3,
            "jsonld_ok": faq_cnt == 1,
            "cta_ok": "article-cta-btn" in html,
            "title_len": tl, "desc_len": len(desc) if desc else 0,
            "h1_count": len(h1_texts), "h2_count": len(h2s), "h2_q_ratio": h2_ratio,
            "faq_items": faq_items, "faqpage_jsonld_count": faq_cnt, "faqpage_questions": faq_q,
            "broken_links": broken, "img_no_alt": no_alt,
            "issues": issues,
        }
    records[slug] = rec

dup_h1 = {l: {h:s for h,s in d.items() if len(s)>1} for l,d in site_h1.items()}
dup_title = {l: {t:s for t,s in d.items() if len(s)>1} for l,d in site_title.items()}
dup_desc = {l: {t:s for t,s in d.items() if len(s)>1} for l,d in site_desc.items()}

agg = {}
severity = defaultdict(lambda: defaultdict(int))
for slug, rec in records.items():
    for lang in LANGS:
        r = rec.get(lang, {})
        if "err" in r: continue
        a = agg.setdefault(lang, {"total":0,"clean":0})
        a["total"] += 1
        if not r.get("issues"): a["clean"] += 1
        for code in r["issues"]:
            severity[lang][code.split(":")[0]] += 1

summary = {
    "total_slugs": len(slugs),
    "per_lang": agg,
    "severity_counts": {l: dict(severity[l]) for l in LANGS},
    "dup_h1": {l: len(d) for l,d in dup_h1.items()},
    "dup_title": {l: len(d) for l,d in dup_title.items()},
    "dup_desc": {l: len(d) for l,d in dup_desc.items()},
}
out = {
    "summary": summary,
    "dup_h1_examples": {l: dict(list(d.items())[:15]) for l,d in dup_h1.items()},
    "dup_title_examples": {l: dict(list(d.items())[:15]) for l,d in dup_title.items()},
    "records": records,
}
with open(os.path.join(os.path.dirname(__file__), "deep_audit.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False)

print("=== DEEP AUDIT SUMMARY ===")
for l in LANGS:
    a = agg.get(l, {})
    print(f"  {l}: {a.get('clean',0)}/{a.get('total',0)} fully clean (no issue)")
print("\n=== Issue frequency (by language) ===")
for l in LANGS:
    print(f"  [{l}]")
    for code, c in sorted(severity[l].items(), key=lambda x:-x[1]):
        print(f"      {code}: {c}")
print("\n=== Site-level duplicates ===")
for l in LANGS:
    print(f"  {l}: dup_H1={summary['dup_h1'].get(l,0)} dup_title={summary['dup_title'].get(l,0)} dup_desc={summary['dup_desc'].get(l,0)}")
print("\nWrote deep_audit.json")
