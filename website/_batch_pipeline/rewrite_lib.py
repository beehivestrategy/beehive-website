#!/usr/bin/env python3
"""
rewrite_lib.py — reusable helpers for the blog batch rewrite program.

- fix_divs(): drop stray </div> tokens so div nesting is balanced.
- inject_faq(): insert a FAQPage JSON-LD <script> before </article>.
- topup_en()/topup_zh(): append a topical paragraph if below the length floor.
- splice(): replace the inner <article> region of a REAL article file with a
  new body, preserving the <head> (canonical/hreflang/og/JSON-LD) and the
  outer page chrome.

All paths are absolute under the website root.
"""
import re, os, json

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"

def fix_divs(h, max_iter=6):
    for _ in range(max_iter):
        tokens = list(re.finditer(r'<div\b[^>]*>|</div>', h))
        stack = 0
        drop = None
        for t in tokens:
            if t.group().startswith('<div'):
                stack += 1
            else:
                if stack > 0:
                    stack -= 1
                else:
                    drop = t  # first unmatched close
        if drop is None:
            break
        h = h[:drop.start()] + h[drop.end():]
    return h

def inject_faq(body, faq_script):
    """Insert faq_script (a <script type=application/ld+json>...</script>) before </article>.
    Skips if a FAQPage JSON-LD is already present."""
    if '"FAQPage"' in body or '"@type":"FAQPage"' in body:
        return body
    idx = body.rfind('</article>')
    if idx == -1:
        return body + "\n" + faq_script
    return body[:idx] + "\n" + faq_script + "\n" + body[idx:]

def _count_en(body):
    t = re.sub(r'<[^>]+>', ' ', body)
    t = re.sub(r'&[a-z]+;', ' ', t)
    t = re.sub(r'\s+', ' ', t)
    return len(t.split())

def _count_zh(body):
    return len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', body))

def topup_en(body, para, min_words=2500):
    wc = _count_en(body)
    if wc >= min_words:
        return body, wc
    idx = body.rfind('</article>')
    if idx == -1:
        body = body + "\n<p>" + para + "</p>\n"
    else:
        body = body[:idx] + "\n<p>" + para + "</p>\n" + body[idx:]
    return body, _count_en(body)

def topup_zh(body, para, min_cjk=3500):
    c = _count_zh(body)
    if c >= min_cjk:
        return body, c
    idx = body.rfind('</article>')
    if idx == -1:
        body = body + "\n<p>" + para + "</p>\n"
    else:
        body = body[:idx] + "\n<p>" + para + "</p>\n" + body[idx:]
    return body, _count_zh(body)

def splice(real_path, new_inner):
    """Replace everything between <article ...> and </article> with new_inner.
    new_inner may itself contain a trailing </article> (stripped)."""
    h = open(real_path, encoding='utf-8').read()
    a_open = re.search(r'<article\b[^>]*>', h)
    if not a_open:
        raise SystemExit("no <article> tag in " + real_path)
    a_close = h.rfind('</article>')
    ni = re.sub(r'\s*</article>\s*$', '', new_inner)
    new_h = h[:a_open.end()] + "\n" + ni + "\n" + h[a_close:]
    open(real_path, 'w', encoding='utf-8').write(new_h)
    return new_h

def update_manifest(lang_sub, slug, word_count):
    mpath = os.path.join(ROOT, lang_sub, 'manifest.json')
    m = json.load(open(mpath, encoding='utf-8'))
    by_slug = {a['slug']: a for a in m['articles']}
    if slug in by_slug:
        by_slug[slug]['wordCount'] = word_count
        by_slug[slug]['readingTime'] = max(1, round(word_count/200)) if lang_sub == 'blog/articles' else max(1, round(word_count/350))
        json.dump(m, open(mpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return by_slug.get(slug, {})
