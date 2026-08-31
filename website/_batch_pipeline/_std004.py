#!/usr/bin/env python3
"""Structural helpers for batch 004 standardisation.

Commands:
  outline <path>            print H2 outline + FAQ questions + counts
  h3wrap <path>...          wrap accordion .faq-question buttons in <h3 style="margin:0">
  jsonld <path>...          inject FAQPage JSON-LD in BODY right after the faq-section
                            closing tag, built from the on-page FAQ. Skips if body
                            already has an FAQPage script (update in place instead).
Never touches <head>, <footer>, share markup, or link paths.
"""
import json
import os
import re
import sys

HEAD_END = "</head>"


def read(p):
    return open(p, encoding="utf-8").read()


def write(p, s):
    open(p, "w", encoding="utf-8").write(s)


def faq_block(html):
    """Return (start, end, text) of the faq-section element."""
    i = html.find('<section class="faq-section"')
    if i == -1:
        return None
    # find matching </section> allowing nested sections
    depth = 0
    for m in re.finditer(r"<section\b|</section>", html[i:]):
        if m.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                end = i + m.end()
                return (i, end, html[i:end])
        else:
            depth += 1
    return None


def clean(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<")
    s = s.replace("&gt;", ">").replace("&quot;", '"').replace("&#39;", "'")
    s = s.replace("&mdash;", "\u2014").replace("&rsquo;", "\u2019")
    return re.sub(r"\s+", " ", s).strip()


def extract_qa(block):
    """Extract [(question, answer)] from either FAQ markup style."""
    qa = []
    items = re.findall(r'<div class="faq-item".*?(?=<div class="faq-item"|\Z)', block, re.S)
    for it in items:
        q = None
        m = re.search(r"<h3[^>]*>(.*?)</h3>", it, re.S)
        if m and "<button" not in m.group(1):
            q = clean(m.group(1))
        if not q:
            m = re.search(r'<span class="faq-question-text">(.*?)</span>\s*</span>', it, re.S)
            if not m:
                m = re.search(r'<button class="faq-question"[^>]*>(.*?)</button>', it, re.S)
            if m:
                q = clean(m.group(1))
                q = re.sub(r"^(\d+)\s+(?=\S)", "", q)  # strip leading number badge
                q = re.sub(r"^(\d+)\s*\1\s+", "", q)
        a = None
        m = re.search(r'<div class="faq-answer(?:-inner)?"[^>]*>(.*?)</div>\s*</div>', it, re.S)
        if not m:
            m = re.search(r'<div class="faq-answer"[^>]*>(.*?)$', it, re.S)
        if m:
            a = clean(m.group(1))
        if q and a:
            qa.append((q, a))
    return qa


def body_has_faqpage(html):
    body = html[html.find(HEAD_END):] if HEAD_END in html else html
    return '"FAQPage"' in body.replace(" ", "").replace("'", '"')


def build_jsonld(qa, indent="                "):
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in qa
        ],
    }
    body = json.dumps(data, ensure_ascii=False, indent=2)
    body = "\n".join(indent + l for l in body.split("\n"))
    return (
        f'\n{indent}<script type="application/ld+json">\n'
        + body
        + f"\n{indent}</script>"
    )


def cmd_outline(paths):
    for p in paths:
        html = read(p)
        m = re.search(r'<article id="article-content">(.*?)</article>', html, re.S)
        art = m.group(1) if m else html
        fb = faq_block(html)
        prose = art[: art.find('<section class="faq-section"')] if '<section class="faq-section"' in art else art
        t = clean(prose)
        print("=" * 72)
        print(p)
        print("  EN words:", len(re.findall(r"[A-Za-z0-9']+", t)),
              "| CJK:", len(re.findall(r"[\u3400-\u9fff]", t)))
        for m2 in re.finditer(r"<h2[^>]*>(.*?)</h2>", prose, re.S):
            print("  H2:", clean(m2.group(1))[:95])
        for m2 in re.finditer(r"<h3[^>]*>(.*?)</h3>", prose, re.S):
            print("    h3:", clean(m2.group(1))[:85])
        if fb:
            for q, a in extract_qa(fb[2]):
                print("  FAQ Q:", q[:90], "|| A:", a[:60])
        else:
            print("  NO FAQ SECTION")
        print("  body FAQPage:", body_has_faqpage(html))
        tail = html[fb[1]:] if fb else ""
        print("  after-FAQ tail:", clean(tail)[:160])


def cmd_h3wrap(paths):
    for p in paths:
        html = read(p)
        fb = faq_block(html)
        if not fb:
            print("SKIP (no faq)", p)
            continue
        start, end, block = fb
        if re.search(r"<h3[^>]*>\s*<button class=\"faq-question\"", block):
            print("SKIP (already h3)", p)
            continue
        if 'class="faq-question"' not in block:
            print("SKIP (h3 style already)", p)
            continue
        new = re.sub(
            r'(<button class="faq-question".*?</button>)',
            r'<h3 style="margin:0">\1</h3>',
            block,
            flags=re.S,
        )
        n = len(re.findall(r'<h3 style="margin:0">', new))
        write(p, html[:start] + new + html[end:])
        print(f"h3wrap {n}", p)


def cmd_jsonld(paths):
    for p in paths:
        html = read(p)
        fb = faq_block(html)
        if not fb:
            print("SKIP (no faq)", p)
            continue
        start, end, block = fb
        qa = extract_qa(block)
        if len(qa) < 3:
            print(f"SKIP (only {len(qa)} qa parsed)", p)
            continue
        new_script = build_jsonld(qa)
        tail = html[end:]
        m = re.match(r'\s*<script type="application/ld\+json">.*?</script>', tail, re.S)
        if m and '"FAQPage"' in m.group(0).replace(" ", ""):
            html = html[:end] + new_script + tail[m.end():]
            print(f"updated in place ({len(qa)} qa)", p)
        elif body_has_faqpage(html):
            print("SKIP (body FAQPage elsewhere)", p)
            continue
        else:
            html = html[:end] + new_script + tail
            print(f"inserted ({len(qa)} qa)", p)
        write(p, html)


INSERT_MARKERS = [
    '<section class="faq-section"',
    '<nav class="article-nav"',
    '<footer class="article-footer"',
]


def cmd_insert(args):
    """insert <snippet_file> <path>...  -> insert snippet before FAQ/article-nav."""
    snippet = read(args[0]).rstrip("\n")
    for p in args[1:]:
        html = read(p)
        art_start = re.search(r"<article\b[^>]*>", html)
        base = art_start.end() if art_start else 0
        pos = -1
        for mk in INSERT_MARKERS:
            i = html.find(mk, base)
            if i != -1:
                pos = i
                break
        if pos == -1:
            print("FAIL (no marker)", p)
            continue
        line_start = html.rfind("\n", 0, pos) + 1
        indent = html[line_start:pos]
        block = "\n".join((indent + l if l.strip() else l) for l in snippet.split("\n"))
        write(p, html[:line_start] + block + "\n" + html[line_start:])
        print("inserted", len(snippet), "chars ->", p)


if __name__ == "__main__":
    cmd = sys.argv[1]
    paths = sys.argv[2:]
    {
        "outline": cmd_outline,
        "h3wrap": cmd_h3wrap,
        "jsonld": cmd_jsonld,
        "insert": cmd_insert,
    }[cmd](paths)
