#!/usr/bin/env python3
"""Mechanical pass over gbatch_001 files:
 1. <button class="faq-question"> -> <h3 class="faq-question">  (and </button> -> </h3>)
 2. strip duplicated leading ordinal inside the question text span
 3. zh-TW: CTA phrase 預約演示 -> 預約示範 (only inside the article-cta-btn anchor)
 4. ensure EXACTLY ONE FAQPage JSON-LD, Q/A verbatim-matched to on-page FAQ
    - if one exists in <head>: update in place
    - else: insert in BODY immediately after the FAQ section
Never touches <head> otherwise, footer, share markup, or ?v= version strings.
"""
import re, os, json, sys

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
SLUGS = [l.strip() for l in open(os.path.join(ROOT, "_batch_pipeline/gap_batches/gbatch_001.txt")) if l.strip()]
LANGS = (("en", "blog/articles/%s.html"),
         ("cn", "zh-cn/blog/articles/%s.html"),
         ("tw", "zh-tw/blog/articles/%s.html"))

def faq_span(html):
    """Return (start, end) char offsets of the <section class='faq-section'>...</section> block."""
    i = html.find('class="faq-section"')
    if i < 0: return None
    start = html.rfind('<', 0, i)
    depth = 0; j = start
    tag_re = re.compile(r'<(/?)(section|div)\b[^>]*>', re.I)
    while True:
        m = tag_re.search(html, j)
        if not m: return (start, len(html))
        depth += -1 if m.group(1) else 1
        j = m.end()
        if depth == 0: return (start, j)

def parse_pairs(sec):
    qs = re.findall(r'<(?:h3|button)[^>]*class="faq-question"[^>]*>(.*?)</(?:h3|button)>', sec, re.S)
    ans = re.findall(r'<div class="faq-answer-inner">(.*?)</div>', sec, re.S)
    out = []
    for k, q in enumerate(qs):
        qt = re.sub(r'<[^>]+>', ' ', q)
        qt = re.sub(r'&nbsp;', ' ', qt)
        qt = re.sub(r'&amp;', '&', qt)
        qt = re.sub(r'\s+', ' ', qt).strip()
        qt = re.sub(r'^\s*\d+\s*[.、]?\s+', '', qt)       # "1 What is..." -> "What is..."
        at = ''
        if k < len(ans):
            at = re.sub(r'<[^>]+>', ' ', ans[k])
            at = re.sub(r'&nbsp;', ' ', at)
            at = re.sub(r'&amp;', '&', at)
            at = re.sub(r'\s+', ' ', at).strip()
        out.append((qt, at))
    return out

def build_ld(pairs):
    ents = []
    for q, a in pairs:
        ents.append({"@type": "Question", "name": q,
                     "acceptedAnswer": {"@type": "Answer", "text": a}})
    return ('<script type="application/ld+json">\n'
            + json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                          "mainEntity": ents}, ensure_ascii=False, indent=2)
            + '\n</script>')

def strip_existing_ld(html):
    """Remove all FAQPage ld+json blocks. Returns (html, n_removed)."""
    n = 0
    def repl(m):
        nonlocal n
        if '"FAQPage"' in m.group(0):
            n += 1
            return ''
        return m.group(0)
    html = re.sub(r'<script type="application/ld\+json">.*?</script>', repl, html, flags=re.S)
    return html, n

report = []
for slug in SLUGS:
    for lang, tpl in LANGS:
        fp = os.path.join(ROOT, tpl % slug)
        if not os.path.exists(fp):
            report.append((slug, lang, "MISSING", "")); continue
        src = open(fp, encoding="utf-8").read()
        h = src
        notes = []

        # ---- 1. button -> h3 in FAQ ----
        sp = faq_span(h)
        if sp:
            s, e = sp
            sec = h[s:e]
            new_sec = sec.replace('<button class="faq-question"', '<h3 class="faq-question"')
            new_sec = new_sec.replace('</button>', '</h3>')
            if new_sec != sec:
                h = h[:s] + new_sec + h[e:]
                notes.append("btn->h3")
        # ---- 2. duplicated ordinal ----
        def dedup(m):
            return m.group(1) + re.sub(r'^\s*\d+\s+', '', m.group(2)) + m.group(3)
        h2 = re.sub(r'(<span class="faq-question-text"><span class="faq-number">)(\s*)(</span>)',
                    lambda m: m.group(1) + m.group(2).strip() + m.group(3), h)
        h2 = re.sub(r'(<span class="faq-question-text"><span class="faq-number">\s*\d+\s*</span><span>)\s*(\d+\s+)',
                    r'\1', h2)
        if h2 != h:
            h = h2; notes.append("dedup-num")

        # ---- 3. zh-TW CTA phrase ----
        if lang == "tw":
            def ctarep(m):
                inner = m.group(2)
                if '預約演示' in inner:
                    return m.group(1) + inner.replace('預約演示', '預約示範') + m.group(3)
                return m.group(0)
            h3 = re.sub(r'(<a [^>]*class="article-cta-btn"[^>]*>)(.*?)(</a>)', ctarep, h, flags=re.S)
            if h3 != h:
                h = h3; notes.append("tw-cta")

        # ---- 4. FAQPage JSON-LD: exactly one, verbatim ----
        sp = faq_span(h)
        pairs = parse_pairs(h[sp[0]:sp[1]]) if sp else []
        pairs = [(q, a) for q, a in pairs if q]
        if len(pairs) >= 3:
            had_in_head = bool(re.search(r'<head[^>]*>.*?"FAQPage"', src, re.S))
            h, nrm = strip_existing_ld(h)
            sp = faq_span(h)
            ld = build_ld(pairs)
            if had_in_head:
                # put back into head, before </head>
                i = h.rfind('</head>')
                h = h[:i] + ld + '\n' + h[i:]
                notes.append(f"ld-inplace(rm{nrm})")
            else:
                # insert in body right after FAQ section
                s, e = sp
                h = h[:e] + '\n\n            ' + ld + '\n' + h[e:]
                notes.append(f"ld-added(rm{nrm})")

        if h != src:
            open(fp, 'w', encoding='utf-8').write(h)
            # --- verify verbatim match after write ---
            chk = open(fp, encoding='utf-8').read()
            sp2 = faq_span(chk)
            pp = parse_pairs(chk[sp2[0]:sp2[1]]) if sp2 else []
            nld = len(re.findall(r'"FAQPage"', chk))
            ldnames = []
            for mm in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', chk, re.S):
                if '"FAQPage"' not in mm.group(1): continue
                try:
                    d = json.loads(mm.group(1))
                except Exception:
                    ldnames.append('PARSE-FAIL'); continue
                ldnames += [e['name'] for e in d.get('mainEntity', [])]
            onnames = [q for q, a in pp]
            if nld != 1 or ldnames != onnames:
                notes.append(f"!!VERIFY-FAIL ld={nld} ld={ldnames} on={onnames}")
        report.append((slug, lang, "OK" if h != src else "unchanged",
                       f"faq={len(pairs)} " + ",".join(notes)))

for r in report:
    print(f"{r[0][:46]:48s} {r[1]:2s} {r[2]:9s} {r[3]}")
