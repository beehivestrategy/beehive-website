#!/usr/bin/env python3
"""Non-destructive GEO repair pass (approved 2026-09-02, Q2).
Fixes ONLY: canonical_wrong, og/tw meta gaps, faqpage JSON-LD mismatch/multiple.
Holds: title rewrites, h1 injection, faq_lt3 content-gen, broken links/anchors (separate passes).
Re-detects each defect from raw HTML so targeting is exact. Idempotent. Logs every change.
"""
import os, re, json
from collections import defaultdict

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
LANGS = {"en": "blog/articles", "cn": "zh-cn/blog/articles", "tw": "zh-tw/blog/articles"}
SITE = "https://www.beehivestrategy.com"
LANGDIR = {"en": "en", "cn": "zh-cn", "tw": "zh-tw"}

def read(p):
    try: return open(p, encoding="utf-8").read()
    except: return None
def write(p, s):
    with open(p, "w", encoding="utf-8") as f: f.write(s)

def strip_tags(s):
    if not s: return ""
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def get_meta(head, name):
    m = re.search(r'<meta\s+(?:name|property)=["\']'+re.escape(name)+r'["\'][^>]*content=["\'](.*?)["\']', head, re.I|re.S)
    return m.group(1) if m else None
def get_title(head):
    m = re.search(r'<title[^>]*>(.*?)</title>', head, re.S|re.I)
    return m.group(1).strip() if m else ""

def self_url(slug, lang):
    pre = "/zh-cn" if lang=="cn" else "/zh-tw" if lang=="tw" else ""
    return f"{SITE}{pre}/blog/articles/{slug}"
def cover_url(slug, lang):
    return f"{SITE}/assets/blog/covers/{LANGDIR[lang]}/{slug}.jpg"

def fix_canonical_link(html, new_url):
    html = re.sub(r'(rel=["\']canonical["\'][^>]*?href=["\'])[^"\']+(["\'])',
                  lambda m: m.group(1)+new_url+m.group(2), html, flags=re.I)
    html = re.sub(r'(href=["\'])[^"\']+(["\'][^>]*?rel=["\']canonical["\'])',
                  lambda m: m.group(1)+new_url+m.group(2), html, flags=re.I)
    return html

def set_meta(html, attr, key, value):
    pat = re.compile(r'<meta\s+(?:name|property)=["\']'+re.escape(key)+r'["\'][^>]*content=["\'][^"\']*["\']', re.I)
    if pat.search(html):
        html = pat.sub(lambda m: re.sub(r'content=["\'][^"\']*["\']', f'content="{value}"', m.group(0), count=1), html, count=1)
    else:
        html = html.replace("</head>", f'<meta {attr}="{key}" content="{value}">\n</head>', 1)
    return html

# ---- FAQ DOM extraction (tolerant to two observed variants) ----
def extract_faq(html):
    # operate on full document: faq-item class is unique to the FAQ block
    region = html
    chunks = re.split(r'<div\b[^>]*class=["\'][^"\']*faq-item[^"\']*["\']', region)
    pairs = []
    for ch in chunks[1:]:
        # question
        q = None
        m = re.search(r'class=["\']faq-question-text["\'][^>]*>(?:<span[^>]*>\s*\d+\s*</span>)?\s*<span[^>]*>(.*?)</span>', ch, re.S|re.I)
        if m: q = m.group(1)
        else:
            m = re.search(r'<h3[^>]*>(.*?)</h3>', ch, re.S|re.I)
            if m: q = m.group(1)
        q = strip_tags(q)
        q = re.sub(r'^\d+[\.\)]?\s*', '', q).strip()
        # answer
        a = None
        m = re.search(r'class=["\']faq-answer-inner["\'][^>]*>(.*?)</div>', ch, re.S|re.I)
        if not m: m = re.search(r'class=["\']faq-answer["\'][^>]*>(.*?)</div>', ch, re.S|re.I)
        if not m: m = re.search(r'<p[^>]*>(.*?)</p>', ch, re.S|re.I)
        a = strip_tags(m.group(1)) if m else ""
        if q and a:
            pairs.append({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}})
    return pairs

LD_PAT = re.compile(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.S|re.I)

def _count_faq_questions(block_content):
    try:
        obj = json.loads(block_content)
    except Exception:
        return 0
    cnt = 0
    def walk(o):
        nonlocal cnt
        if isinstance(o, dict):
            if o.get("@type") == "FAQPage":
                me = o.get("mainEntity", [])
                if isinstance(me, list): cnt += len(me)
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(obj)
    return cnt

def repair_faqpage(html, slug, lang):
    pairs = extract_faq(html)
    matches = list(LD_PAT.finditer(html))
    fp_blocks = [m for m in matches if "FAQPage" in m.group(1)]
    if len(fp_blocks) == 0:
        return html, "skip:no-faqpage-block"
    # guard: never touch a block that also carries BlogPosting/BreadcrumbList
    for m in matches:
        if "FAQPage" in m.group(1) and ("BlogPosting" in m.group(1) or "BreadcrumbList" in m.group(1)):
            return html, "skip:combined-block"
    if len(fp_blocks) > 1:
        # consolidate duplicates -> DOM count
        if len(pairs) >= 3:
            return _inject_faqpage(html, matches, fp_blocks, pairs)
        return html, f"skip:extracted={len(pairs)}<3"
    # exactly one FAQPage block
    faq_q = _count_faq_questions(fp_blocks[0].group(1))
    if len(pairs) == faq_q:
        return html, "skip:already-correct"
    if len(pairs) > faq_q and len(pairs) >= 3:
        return _inject_faqpage(html, matches, fp_blocks, pairs)
    return html, f"skip:extracted({len(pairs)})!=jsonld({faq_q})"

def _inject_faqpage(html, matches, fp_blocks, pairs):
    new_fp = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":pairs},
                        ensure_ascii=False, indent=2)
    new_script = f'<script type="application/ld+json">\n{new_fp}\n</script>'
    parts = []; last = 0; inserted = False
    for m in matches:
        parts.append(html[last:m.start()])
        if m in fp_blocks:
            if not inserted:
                parts.append(new_script); inserted = True
        else:
            parts.append(m.group(0))
        last = m.end()
    parts.append(html[last:])
    return "".join(parts), f"ok:rebuilt-{len(pairs)}"

# ---- load targets ----
tgt = json.load(open(os.path.join(os.path.dirname(__file__),"repair_targets.json"), encoding="utf-8"))
def collect(cat):
    s=set()
    for lg in LANGS:
        for sl in tgt.get(cat,{}).get(lg,[]):
            s.add((sl,lg))
    return s
canon = collect("canonical_wrong")
ogmiss = collect("og_missing")
twmiss = collect("tw_missing")
fpmult = collect("faqpage_jsonld_multiple")
fpmis = collect("faqpage_jsonld_mismatch")
faqset = fpmult | fpmis

# TEST MODE: only the 4 representative slugs
if os.environ.get("REPAIR_TEST") == "1":
    canon = {("building-ai-chatbots-enterprise-customer-service","tw")}
    ogmiss = {(tgt["og_missing"]["en"][0],"en")}
    twmiss = {(tgt["tw_missing"]["en"][0],"en")}
    faqset = {("automated-data-classification-ai","en"),("dingtalk-and-feishu-ai-ecosystem-enterprise-integration","en")}
    print("*** TEST MODE ***")

log = {"canonical":[], "og_added":[], "tw_added":[], "faqpage":[], "skipped":[]}
changed_files = 0

for (slug, lang) in (canon | ogmiss | twmiss | faqset):
    path = os.path.join(ROOT, LANGS[lang], slug + ".html")
    html = read(path)
    if html is None: continue
    orig = html
    head = re.search(r'<head[^>]*>(.*?)</head>', html, re.S|re.I)
    head = head.group(1) if head else ""
    title = get_title(html)
    desc = get_meta(html, "description") or title

    # canonical + (for tw/cn wrong) normalize og:url + twitter:image
    if (slug, lang) in canon:
        new = self_url(slug, lang)
        html = fix_canonical_link(html, new)
        html = set_meta(html, "property", "og:url", new)
        html = set_meta(html, "name", "twitter:image", cover_url(slug, lang))
        log["canonical"].append(f"{lang}/{slug}")

    # og missing
    if (slug, lang) in ogmiss:
        added=[]
        if not get_meta(html,"og:type"): html=set_meta(html,"property","og:type","article"); added.append("og:type")
        if not get_meta(html,"og:title"): html=set_meta(html,"property","og:title",title); added.append("og:title")
        if not get_meta(html,"og:description"): html=set_meta(html,"property","og:description",desc); added.append("og:description")
        if not get_meta(html,"og:url"): html=set_meta(html,"property","og:url",self_url(slug,lang)); added.append("og:url")
        if not get_meta(html,"og:image"): html=set_meta(html,"property","og:image",cover_url(slug,lang)); added.append("og:image")
        if added: log["og_added"].append(f"{lang}/{slug}:{','.join(added)}")

    # twitter missing
    if (slug, lang) in twmiss:
        added=[]
        if not get_meta(html,"twitter:card"): html=set_meta(html,"name","twitter:card","summary_large_image"); added.append("twitter:card")
        if not get_meta(html,"twitter:title"): html=set_meta(html,"name","twitter:title",title); added.append("twitter:title")
        if not get_meta(html,"twitter:description"): html=set_meta(html,"name","twitter:description",desc); added.append("twitter:description")
        if not get_meta(html,"twitter:image"): html=set_meta(html,"name","twitter:image",cover_url(slug,lang)); added.append("twitter:image")
        if added: log["tw_added"].append(f"{lang}/{slug}:{','.join(added)}")

    # faqpage JSON-LD
    if (slug, lang) in faqset:
        html, status = repair_faqpage(html, slug, lang)
        if status.startswith("ok"): log["faqpage"].append(f"{lang}/{slug}:{status}")
        else: log["skipped"].append(f"{lang}/{slug}:{status}")

    if html != orig:
        write(path, html); changed_files += 1

json.dump(log, open(os.path.join(os.path.dirname(__file__),"repair_log.json"),"w"), ensure_ascii=False, indent=1)
print("CHANGED FILES:", changed_files)
print("canonical fixed:", len(log["canonical"]))
print("og added entries:", len(log["og_added"]))
print("tw added entries:", len(log["tw_added"]))
print("faqpage rebuilt:", len(log["faqpage"]))
print("faqpage skipped:", len(log["skipped"]))
for s in log["skipped"][:20]: print("  SKIP:", s)
