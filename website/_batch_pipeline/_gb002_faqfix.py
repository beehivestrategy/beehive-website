#!/usr/bin/env python3
"""
Idempotent fixer for FAQ sections on Beehive blog articles.

Does three things INSIDE THE BODY ONLY:
 1. Wraps every FAQ question button in <h3 class="faq-question-heading" style="margin:0">…</h3>
 2. Repairs duplicated leading numbers in question text (e.g. "1 1 What is …")
 3. Rebuilds/inserts the FAQPage JSON-LD immediately after the FAQ section's closing tag,
    generated from the on-page Q&A so it always matches.

NEVER touches <head>, <footer>, share buttons, or any link path.
"""
import re, sys, json, html, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def find_faq(raw):
    m = re.search(r'<section[^>]*class="faq-section"[^>]*>', raw)
    if not m:
        m = re.search(r'<div[^>]*class="faq-section"[^>]*>', raw)
        if not m:
            return None
        tag = 'div'
    else:
        tag = 'section'
    start = m.end()
    depth = 1
    i = start
    for mm in re.finditer(r'</?%s\b' % tag, raw[start:], re.I):
        depth += -1 if raw[start + mm.start():].startswith('</') else 1
        if depth == 0:
            i = start + mm.start()
            break
    close = raw.find('>', i) + 1
    return m.start(), close, m.group(0)


def clean_question(q_inner):
    """q_inner: content of <span class="faq-question-text">…</span>"""
    num = re.match(r'\s*<span class="faq-number">\s*(\d+)\s*</span>\s*', q_inner, re.S)
    rest = q_inner
    if num:
        rest = q_inner[num.end():]
    txt = html.unescape(re.sub(r'<[^>]+>', '', rest)).strip()
    txt = re.sub(r'^\d+\s+(?=\S)', '', txt)          # duplicated leading "1 "
    return txt


def get_pairs(seg):
    """Extract (question, answer_text) from a FAQ section segment."""
    pairs = []
    for m in re.finditer(r'<div class="faq-item"[^>]*>', seg):
        start = m.end()
        nxt = re.search(r'<div class="faq-item"[^>]*>', seg[start:])
        chunk = seg[start:start + (nxt.start() if nxt else len(seg))]
        qm = re.search(r'<span class="faq-question-text">(.*?)</span>\s*(?=<svg|</button)', chunk, re.S)
        am = re.search(r'<div class="faq-answer-inner">(.*?)</div>', chunk, re.S)
        if not qm or not am:
            continue
        a = html.unescape(re.sub(r'<[^>]+>', ' ', am.group(1)))
        a = re.sub(r'\s+', ' ', a).strip()
        pairs.append((clean_question(qm.group(1)), a))
    return pairs


def process(path, dry=False):
    raw = open(path, encoding='utf-8').read()
    orig = raw
    head_end = raw.find('</head>')
    if head_end < 0:
        return "NO-HEAD-CLOSING"

    loc = find_faq(raw)
    if not loc:
        return "NO-FAQ-SECTION"
    s, e, open_tag = loc

    # ---------- 1 & 2: h3 wrap + number repair (work on the FAQ segment) ----------
    seg_before = raw[s:e]
    seg = raw[s:e]

    # repair duplicated numbers
    def _fix(m):
        inner = m.group(1)
        nm = re.match(r'\s*(<span class="faq-number">\s*\d+\s*</span>)(\s*)', inner, re.S)
        if not nm:
            return m.group(0)
        rest = inner[nm.end():]
        rest2 = re.sub(r'^((?:\s|<span[^>]*>)*)\d+\s+', r'\1', rest, flags=re.S)
        if rest2 == rest:
            return m.group(0)          # nothing to repair -> byte-identical
        return '<span class="faq-question-text">' + nm.group(1) + nm.group(2) + rest2 + '</span>'
    seg = re.sub(r'<span class="faq-question-text">(.*?)</span>\s*(?=<svg|</button)', _fix, seg, flags=re.S)

    # h3 wrap (idempotent)
    def _wrap(m):
        before = seg[max(0, m.start() - 80):m.start()]
        if 'faq-question-heading' in before and '</h3>' not in before:
            return m.group(0)          # already wrapped
        return ('<h3 class="faq-question-heading" style="margin:0">' + m.group(0) + '</h3>')
    seg = re.sub(r'<button class="faq-question"[^>]*>.*?</button>',
                 lambda m: _wrap(m), seg, flags=re.S)

    raw = raw[:s] + seg + raw[e:]
    seg_changed = (seg != seg_before)

    # ---------- 3: JSON-LD ----------
    loc = find_faq(raw)
    s, e, open_tag = loc
    seg = raw[s:e]
    pairs = get_pairs(seg)
    if len(pairs) < 3:
        return "TOO-FEW-FAQ(%d)" % len(pairs)

    # If an existing BODY FAQPage LD already matches the page, leave it byte-for-byte alone.
    if head_end > 0:
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S):
            if m.start() <= head_end or '"FAQPage"' not in m.group(1):
                continue
            try:
                d = json.loads(m.group(1))
            except Exception:
                continue
            ents = d.get("mainEntity", [])
            if [html.unescape(x.get("name", "")).strip() for x in ents] == [p[0] for p in pairs] and \
               [html.unescape(x.get("acceptedAnswer", {}).get("text", "")).strip() for x in ents] == [p[1] for p in pairs]:
                if seg_changed or raw != orig:
                    if not dry:
                        open(path, 'w', encoding='utf-8').write(raw)
                    return "OK faq=%d (LD already valid)" % len(pairs)
                return "unchanged"

    # drop any pre-existing body FAQPage LD (head ones are left alone)
    def _drop(m):
        if m.start() > head_end and '"FAQPage"' in m.group(1):
            return ''
        return m.group(0)
    raw = re.sub(r'<script type="application/ld\+json">.*?</script>', _drop, raw, flags=re.S)
    loc = find_faq(raw)
    s, e, open_tag = loc

    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q,
                          "acceptedAnswer": {"@type": "Answer", "text": a}}
                         for q, a in pairs]}
    block = ('\n\n            <script type="application/ld+json">\n'
             + json.dumps(ld, ensure_ascii=False, indent=2)
             + '\n            </script>\n')
    raw = raw[:e] + block + raw[e:]

    if raw == orig:
        return "unchanged"
    if not dry:
        open(path, 'w', encoding='utf-8').write(raw)
    return "OK faq=%d" % len(pairs)


if __name__ == "__main__":
    dry = '--dry' in sys.argv
    targets = [a for a in sys.argv[1:] if not a.startswith('--')]
    for slug in targets:
        for rel in ("blog/articles", "zh-cn/blog/articles", "zh-tw/blog/articles"):
            p = os.path.join(ROOT, rel, slug + ".html")
            if not os.path.exists(p):
                print("MISSING", p)
                continue
            print(f"{rel.split('/')[0]:6s} {process(p, dry)}")
