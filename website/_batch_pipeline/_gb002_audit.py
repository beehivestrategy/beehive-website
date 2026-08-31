#!/usr/bin/env python3
"""Audit script for GEO/SEO standard compliance on blog articles."""
import re, sys, json, os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CJK = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]')

def strip_tags(s):
    s = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<[^>]+>', ' ', s)
    return html.unescape(s)

def count_words(text):
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-]*", text))

def count_cjk(text):
    return len(CJK.findall(text))

def extract_article(raw):
    m = re.search(r'<article\b[^>]*id="article-content"[^>]*>(.*?)</article>', raw, re.S)
    if not m:
        m2 = re.search(r'<article\b[^>]*>(.*?)</article>', raw, re.S)
        return m2.group(1) if m2 else ""
    return m.group(1)


def audit(path, lang):
    if not os.path.exists(path):
        return {"missing": True}
    raw = open(path, encoding='utf-8').read()
    body = extract_article(raw)
    txt = strip_tags(body)
    words, cjk = count_words(txt), count_cjk(txt)

    # --- FAQ: locate faq-section wrapper, count faq-item blocks inside it
    fm = re.search(r'<section[^>]*class="faq-section"[^>]*>', raw) or \
         re.search(r'<div[^>]*class="faq-section"[^>]*>', raw)
    faq_items, faq_h3 = 0, 0
    faq_end = None
    if fm:
        start = fm.end()
        nxt = re.search(r'<section[^>]*class="recommended', raw[start:]) or \
              re.search(r'<div[^>]*class="recommended', raw[start:]) or \
              re.search(r'<h2[^>]*>\s*(?:Ready|準備好|准备好)', raw[start:])
        seg = raw[start:start + (nxt.start() if nxt else 30000)]
        faq_end = start + (nxt.start() if nxt else len(seg))
        faq_items = len(re.findall(r'class="faq-item"', seg))
        faq_h3 = len(re.findall(r'<h3[^>]*>\s*(?:<button)?', seg))

    # --- JSON-LD
    head_end = raw.find('</head>')
    body_ld, head_ld = None, None
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S):
        if '"FAQPage"' not in m.group(1):
            continue
        if head_end > 0 and m.start() > head_end:
            body_ld = m
        else:
            head_ld = m
    ld_ok = False
    ld_match = False
    if body_ld:
        ld_ok = True
        try:
            data = json.loads(body_ld.group(1))
        except Exception:
            data = None
        if data:
            ents = data.get("mainEntity", [])
            names = [html.unescape(e.get("name", "")) for e in ents]
            # compare against on-page questions
            pageq = []
            if fm:
                seg = raw[fm.end():faq_end]
                for q in re.findall(r'<span class="faq-question-text">(.*?)</span>\s*(?:<svg|</button)', seg, re.S):
                    q = re.sub(r'<span class="faq-number">.*?</span>', '', q, flags=re.S)
                    pageq.append(html.unescape(re.sub(r'<[^>]+>', '', q)).strip())
            if len(names) >= 3 and len(names) == len(pageq):
                ld_match = all(n.strip() in p or p.endswith(n.strip()) for n, p in zip(names, pageq))

    # --- CTA
    cta_phrases = {"en": "Book a Demo", "zh-cn": "预约演示", "zh-tw": "預約示範"}
    has_cta = ('class="article-cta-btn"' in raw) and (cta_phrases[lang] in raw)

    # --- H2 question check (exclude structural labels)
    STRUCT = {'frequently asked questions', 'recommended articles', 'related articles',
              '常見問題', '常见问题', '推荐文章', '推薦文章', '相關文章'}
    h2_clean = [strip_tags(h).strip() for h in re.findall(r'<h2[^>]*>(.*?)</h2>', raw, re.S)]
    def is_q(s):
        s = s.strip()
        if not s or s.lower() in STRUCT or s in STRUCT:
            return True
        return s.endswith('?') or s.endswith('？')
    non_q = [h for h in h2_clean if not is_q(h)]

    return {"words": words, "cjk": cjk, "faq_items": faq_items, "faq_h3": faq_h3,
            "ld_body": ld_ok, "ld_head": bool(head_ld), "ld_match": ld_match,
            "cta": has_cta, "h2": len(h2_clean), "h2_nonq": non_q,
            "vtag": ('?v=20260826' in raw)}


def verdict(r, lang):
    if r.get("missing"):
        return "MISSING"
    if lang == "en":
        ok_len = r["words"] >= 2500
    else:
        ok_len = r["cjk"] >= 3500
    probs = []
    if not ok_len:
        probs.append("len")
    if r["faq_items"] < 3:
        probs.append("faq<3")
    if r["faq_h3"] < 3:
        probs.append("faq-no-h3")
    if not r["ld_body"]:
        probs.append("no-body-LD")
    elif not r["ld_match"]:
        probs.append("LD-mismatch")
    if not r["cta"]:
        probs.append("cta")
    if r["h2_nonq"]:
        probs.append("h2-nonq")
    if not r["vtag"]:
        probs.append("vtag-LOST")
    return "OK" if not probs else ",".join(probs)


if __name__ == "__main__":
    slugs = [l.strip() for l in open(sys.argv[1], encoding='utf-8') if l.strip()]
    out = {}
    for s in slugs:
        row = {}
        for lang, rel in (("en", "blog/articles"), ("zh-cn", "zh-cn/blog/articles"),
                          ("zh-tw", "zh-tw/blog/articles")):
            p = os.path.join(ROOT, rel, s + ".html")
            r = audit(p, lang)
            row[lang] = r
        out[s] = row
        parts = []
        for lang in ("en", "zh-cn", "zh-tw"):
            r = row[lang]
            v = verdict(r, lang)
            parts.append(f"{lang}: {r.get('words')}w/{r.get('cjk')}cjk faq={r.get('faq_items')}/{r.get('faq_h3')}h3 LD={'B' if r.get('ld_body') else '-'}{'H' if r.get('ld_head') else ''}{'m' if r.get('ld_match') else ''} cta={int(bool(r.get('cta')))} -> {v}")
        print(f"{s}\n    " + "\n    ".join(parts))
    json.dump(out, open(os.path.join(ROOT, "_batch_pipeline", "_audit_gb002.json"), "w"),
              ensure_ascii=False, indent=1)
