#!/usr/bin/env python3
# gap-measure v2: accurate body metrics for gbatch_001 slugs
import re, os, sys, json

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
SLUGS = [l.strip() for l in open(os.path.join(ROOT, "_batch_pipeline/gap_batches/gbatch_001.txt")) if l.strip()]

def body_of(html):
    m = re.search(r'<article[^>]*id="article-content"[^>]*>(.*?)</article>', html, re.S)
    if m: return m.group(1)
    m = re.search(r'<article[^>]*>(.*?)</article>', html, re.S)
    return m.group(1) if m else ""

def text_of(frag):
    frag = re.sub(r'<script.*?</script>', ' ', frag, flags=re.S)
    frag = re.sub(r'<style.*?</style>', ' ', frag, flags=re.S)
    frag = re.sub(r'<!--.*?-->', ' ', frag, flags=re.S)
    frag = re.sub(r'<[^>]+>', ' ', frag)
    frag = re.sub(r'&nbsp;', ' ', frag)
    frag = re.sub(r'&amp;', '&', frag)
    frag = re.sub(r'&#\d+;', ' ', frag)
    return frag

def en_words(t): return len(re.findall(r"[A-Za-z][A-Za-z'’\-]*", t))
def cjk(t): return len(re.findall(r'[\u4e00-\u9fff]', t))

# --- FAQ section extraction: balanced scan from 'class="faq-section"' ---
def faq_section(html):
    i = html.find('class="faq-section"')
    if i < 0: return None
    start = html.rfind('<', 0, i)
    # walk forward balancing div/section tags
    depth = 0
    j = start
    tag_re = re.compile(r'<(/?)(section|div)\b[^>]*>', re.I)
    while True:
        m = tag_re.search(html, j)
        if not m: return html[start:]
        depth += -1 if m.group(1) else 1
        j = m.end()
        if depth == 0:
            return html[start:j]

def faq_pairs(html):
    s = faq_section(html)
    if s is None: return []
    qs = [re.sub(r'<[^>]+>', '', m).strip()
          for m in re.findall(r'<h3[^>]*class="faq-question"[^>]*>(.*?)</h3>', s, re.S)]
    if not qs:
        qs = [re.sub(r'<[^>]+>', '', m).strip()
              for m in re.findall(r'<h3[^>]*>(.*?)</h3>', s, re.S)]
    # strip leading number spans
    out = []
    for q in qs:
        q = re.sub(r'^\s*\d+\s*[.、]\s*', '', q)
        q = re.sub(r'\s+', ' ', q)
        out.append(q)
    return out

def ld_faq(html):
    """return (count, list of (q,a)) of FAQPage JSON-LD blocks"""
    n = 0; pairs = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        raw = m.group(1).strip()
        if '"FAQPage"' not in raw: continue
        try:
            d = json.loads(raw)
        except Exception:
            n += 1; continue
        for ent in d.get('mainEntity', []):
            if ent.get('@type') == 'Question':
                pairs.append((ent.get('name',''), ent['acceptedAnswer']['text']))
        n += 1
    return n, pairs

def cta_phrase_state(html, lang):
    phrases = {"en": "Book a Demo", "cn": "预约演示", "tw": "預約示範"}
    p = phrases[lang]
    has_btn = 'class="article-cta-btn"' in html
    return has_btn and (p in html)

def h2_info(html):
    b = body_of(html)
    hs = re.findall(r'<h2[^>]*>(.*?)</h2>', b, re.S)
    txt = [re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', h)).strip() for h in hs]
    q = sum(1 for t in txt if t.endswith('?') or t.endswith('？'))
    return len(txt), q, txt

def title_h1(html):
    t = re.search(r'<title>(.*?)</title>', html, re.S)
    h = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    return (t.group(1).strip() if t else ""), (re.sub(r'<[^>]+>','',h.group(1)).strip() if h else "")

def simplified_in_tw(html):
    b = body_of(html)
    t = text_of(b)
    # common simplified-only chars that must not appear in zh-TW
    bad = re.findall(r'[数据据联网开发设计业务产量问题实际时间供应链预测维护检测报告管理机制优化价值网络数字智能企业产业产品项目运营数据]', t)
    return len(bad)

rows = []
for s in SLUGS:
    for lang, path in (("en", f"blog/articles/{s}.html"),
                       ("cn", f"zh-cn/blog/articles/{s}.html"),
                       ("tw", f"zh-tw/blog/articles/{s}.html")):
        fp = os.path.join(ROOT, path)
        if not os.path.exists(fp):
            print(f"MISSING {lang} {fp}"); continue
        h = open(fp, encoding="utf-8").read()
        b = body_of(h); t = text_of(b)
        metric = en_words(t) if lang == "en" else cjk(t)
        fq = faq_pairs(h); nld, ldp = ld_faq(h)
        nh2, nqh2, _ = h2_info(h)
        ti, h1 = title_h1(h)
        cta = cta_phrase_state(h, lang)
        flush = ""
        if lang == "en" and metric < 2500: flush = "  << EN SHORT"
        if lang in ("cn","tw") and metric < 3500: flush = "  << CJK SHORT"
        rows.append((s, lang, metric, len(fq), nld, nh2, nqh2, int(cta)))
        print(f"{s[:50]:52s} {lang:2s} m={metric:5d} faq={len(fq)} ld={nld} ldQ={len(ldp)} h2={nh2} qh2={nqh2} cta={int(cta)}{flush}")
print()
print("TOTAL files:", len(rows))
print("EN short:", sum(1 for r in rows if r[1]=='en' and r[2]<2500))
print("CN short:", sum(1 for r in rows if r[1]=='cn' and r[2]<3500))
print("TW short:", sum(1 for r in rows if r[1]=='tw' and r[2]<3500))
print("faq<3:", sum(1 for r in rows if r[3]<3))
print("ld!=1:", sum(1 for r in rows if r[4]!=1))
print("cta bad:", sum(1 for r in rows if not r[7]))
