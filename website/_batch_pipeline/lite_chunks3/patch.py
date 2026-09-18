#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Targeted body patcher for Beehive blog article files.
Only touches: TOC links, article prose, FAQ list, FAQ JSON-LD, recommended excerpts.
Never touches <head> (except removing a legacy FAQPage script), footer, or share markup.
"""
import re, json, sys, os

SCRIPT_OPEN = '<script type="application/ld+json">'
SCRIPT_CLOSE = '</script>'

FAQ_ITEM = '''                    <div class="faq-item">
                        <h3 class="faq-question-heading" style="margin:0;font-size:inherit;font-weight:inherit;line-height:inherit"><button class="faq-question" aria-expanded="false">
                            <span class="faq-question-text"><span class="faq-number">%(n)d</span><span>%(q)s</span></span>
                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
                        </button></h3>
                        <div class="faq-answer" role="region"><div class="faq-answer-inner">%(a)s</div></div>
                    </div>'''


def load(p):
    return open(p, encoding='utf-8').read()


def save(p, s):
    open(p, 'w', encoding='utf-8').write(s)


def set_toc(s, items):
    """items: list of (anchor_id, label). Rewrites mobile TOC and sidebar TOC."""
    m = re.search(r'(<div class="toc-mobile-links">)(.*?)(\n\s*</div>)', s, re.S)
    if m:
        links = '\n'.join('                    <a href="#%s" class="toc-mobile-link">%s</a>' % (i, t) for i, t in items)
        s = s[:m.start(2)] + '\n' + links + s[m.start(3):]
    m = re.search(r'(<nav class="toc-links">)(.*?)(\n\s*</nav>)', s, re.S)
    if m:
        links = '\n'.join('                    <a href="#%s" class="toc-link">%s</a>' % (i, t) for i, t in items)
        s = s[:m.start(2)] + '\n' + links + s[m.start(3):]
    return s


def _prose_start(s):
    if '<p class="article-lead">' in s:
        return s.index('<p class="article-lead">')
    # No lead paragraph: start right after the closing tag of the mobile TOC block.
    k = s.index('<div class="toc-mobile"')
    depth = 0
    for m in re.finditer(r'<div\b|</div>', s[k:]):
        depth += 1 if m.group(0) == '<div' else -1
        if depth == 0:
            i = k + m.end()
            while i < len(s) and s[i] in '\r\n \t':
                i += 1
            return i
    raise RuntimeError('toc-mobile block not balanced')


FAQ_SECTION = """
            <section class="faq-section" id="faq" aria-label="%(label)s">
                <h2 class="faq-section-title">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                    %(title)s
                </h2>
                <div class="faq-list">
                </div>
            </section>
"""


def ensure_faq_section(s, title, label):
    if 'faq-section' in s:
        return s
    block = FAQ_SECTION % {'title': title, 'label': label}
    i = s.index('<nav class="article-nav"')
    k = s.rindex('\n', 0, i) + 1
    return s[:k] + block.lstrip('\n') + '\n' + s[k:]


def set_prose(s, html):
    i = _prose_start(s)
    j = s.index('<section class="faq-section"')
    k = s.rindex('\n', 0, j) + 1
    return s[:i] + html.rstrip() + '\n' + s[k:]


def set_faq(s, qa):
    inner = '\n'.join(FAQ_ITEM % {'n': n, 'q': q, 'a': a} for n, (q, a) in enumerate(qa, 1))
    m = re.search(r'(<div class="faq-list">)(.*?)(\n\s*</div>\s*\n\s*</section>)', s, re.S)
    if not m:
        raise RuntimeError('faq-list not found')
    return s[:m.start(2)] + '\n' + inner + s[m.start(3):]


def strip_faq_jsonld(s):
    pat = re.compile(r'"@type"\s*:\s*"FAQPage"')
    while True:
        m = pat.search(s)
        if not m:
            break
        a = s.rindex(SCRIPT_OPEN, 0, m.start())
        a = s.rindex('\n', 0, a) + 1  # include the line's indentation
        b = s.index(SCRIPT_CLOSE, m.start()) + len(SCRIPT_CLOSE)
        # consume trailing whitespace/newline
        while b < len(s) and s[b] in '\r\n \t':
            b += 1
        s = s[:a] + s[b:]
    return s


def add_faq_jsonld(s, qa):
    s = strip_faq_jsonld(s)
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa
        ]
    }
    body = json.dumps(data, ensure_ascii=False, indent=2)
    block = '\n            ' + SCRIPT_OPEN + '\n' + body + '\n' + SCRIPT_CLOSE + '\n'
    i = s.index('<section class="faq-section"')
    j = s.index('</section>', i) + len('</section>')
    return s[:j] + block + s[j:]


FILL_EN = 'A practical guide to the decisions, trade-offs and measurement behind this topic.'
FILL_ZH = '深入解析这一主题背后的决策要点、权衡与衡量方法。'


def fill_excerpts(s, specific=None):
    specific = specific or {}

    def repl(m):
        head = m.group(1)
        href = re.search(r'href="([^"]+)"', head)
        slug = ''
        if href:
            slug = href.group(1).rsplit('/', 1)[-1].replace('.html', '')
        body = m.group(2)
        if re.search(r'<p class="recommended-card-excerpt">\s*</p>', body):
            txt = specific.get(slug)
            if not txt:
                title = re.search(r'<h3 class="recommended-card-title">(.*?)</h3>', body, re.S)
                t = title.group(1).strip() if title else ''
                cjk = re.search(r'[\u4e00-\u9fff]', t)
                txt = FILL_ZH if cjk else FILL_EN
            body = re.sub(r'(<p class="recommended-card-excerpt">)\s*(</p>)',
                          lambda mm: mm.group(1) + txt + mm.group(2), body)
        return head + body + '</a>'

    return re.sub(r'(<a href="/[^"]*" class="recommended-card">)(.*?)</a>', repl, s, re.S)


def fix_tail_h2(s, new_text):
    """Rename a trailing non-question H2 after the article nav (e.g. 'Key takeaways')."""
    i = s.index('</article>')
    j = s.rindex('</nav>', 0, i)
    tail = s[j:i]
    m = re.search(r'<h2\b[^>]*>.*?</h2>', tail, re.S)
    if m:
        tail = tail[:m.start()] + re.sub(r'(<h2\b[^>]*>).*?(</h2>)',
                                         lambda mm: mm.group(1) + new_text + mm.group(2),
                                         tail[m.start():m.end()], flags=re.S) + tail[m.end():]
        return s[:j] + tail + s[i:]
    return s


def fix_cta(s, phrase):
    """Force the CTA button label to the required phrase for the language."""
    m = re.search(r'(class="article-cta-btn"[^>]*>)(.*?)(</a>)', s, re.S)
    if m and m.group(2).strip() != phrase:
        s = s[:m.start(2)] + phrase + s[m.start(3):]
    return s


def apply(path, toc, prose, faq, excerpts=None, tail_h2=None, cta=None,
          faq_title='Frequently Asked Questions', faq_label='Frequently Asked Questions'):
    s = load(path)
    s = set_toc(s, toc)
    s = ensure_faq_section(s, faq_title, faq_label)
    s = set_prose(s, prose)
    s = set_faq(s, faq)
    s = add_faq_jsonld(s, faq)
    if tail_h2:
        s = fix_tail_h2(s, tail_h2)
    if cta:
        s = fix_cta(s, cta)
    s = fill_excerpts(s, excerpts)
    save(path, s)
    return s
