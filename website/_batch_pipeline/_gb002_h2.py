#!/usr/bin/env python3
"""
Body-only helpers for H2 editing on Beehive blog articles.

 - rename_h2(path, old_text, new_text)      : rename an H2 and its TOC entries (ids/hrefs untouched)
 - add_section(path, before_id, sec_id, title, body_html)
        : insert a new <h2 id="sec_id">…</h2> + body immediately before the H2 with id=before_id,
          and insert matching entries into BOTH the mobile TOC and the sidebar TOC.

Never touches <head>, <footer>, share buttons, or any href/path other than the added #fragment anchors.
"""
import re, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _read(p):
    return open(p, encoding='utf-8').read()


def _write(p, s):
    open(p, 'w', encoding='utf-8').write(s)


def rename_h2(path, old, new):
    raw = _read(path)
    pat = re.compile(r'(<h2 id="([^"]+)"[^>]*>)\s*' + re.escape(old) + r'\s*(</h2>)')
    m = pat.search(raw)
    if not m:
        return "H2-NOT-FOUND"
    hid = m.group(2)
    raw = pat.sub(lambda mm: mm.group(1) + new + mm.group(3), raw, count=1)
    toc = re.compile(r'(<a href="#' + re.escape(hid) + r'" class="toc-(?:mobile-)?link"[^>]*>)\s*'
                     + re.escape(old) + r'\s*(</a>)')
    raw, n = toc.subn(lambda mm: mm.group(1) + new + mm.group(2), raw)
    _write(path, raw)
    return "renamed (%d toc)" % n


def add_section(path, before_id, sec_id, title, body_html, toc_after=True):
    """Insert new section before the H2 whose id is `before_id` (or at end of article if None)."""
    raw = _read(path)
    anchor = re.search(r'<h2 id="' + re.escape(before_id) + r'"[^>]*>', raw)
    if not anchor:
        return "ANCHOR-NOT-FOUND:" + before_id
    block = ('<h2 id="%s">%s</h2>\n%s\n' % (sec_id, title, body_html))
    raw = raw[:anchor.start()] + block + raw[anchor.start():]

    # TOC entries
    for cls in ("toc-link", "toc-mobile-link"):
        a = re.search(r'<a href="#' + re.escape(before_id) + r'" class="' + cls + r'"[^>]*>', raw)
        if a:
            indent = raw[raw.rfind('\n', 0, a.start()) + 1:a.start()]
            entry = '<a href="#%s" class="%s">%s</a>\n%s' % (sec_id, cls, title, indent)
            raw = raw[:a.start()] + entry + raw[a.start():]
    _write(path, raw)
    return "added " + sec_id


def add_tail_section(path, sec_id, title, body_html):
    """Insert a new H2 section immediately before the FAQ section, and append it to both TOCs."""
    raw = _read(path)
    a = re.search(r'<section[^>]*class="faq-section"[^>]*>', raw)
    if not a:
        return "FAQ-ANCHOR-NOT-FOUND"
    block = '<h2 id="%s">%s</h2>\n%s\n' % (sec_id, title, body_html)
    raw = raw[:a.start()] + block + raw[a.start():]
    for cls in ("toc-link", "toc-mobile-link"):
        entries = list(re.finditer(r'<a href="#[^"]*" class="' + cls + r'"[^>]*>[^<]*</a>', raw))
        if not entries:
            continue
        last = entries[-1]
        indent = raw[raw.rfind('\n', 0, last.start()) + 1:last.start()]
        entry = '\n%s<a href="#%s" class="%s">%s</a>' % (indent, sec_id, cls, title)
        raw = raw[:last.end()] + entry + raw[last.end():]
    _write(path, raw)
    return "tail-added " + sec_id


def replace_faq_list(path, items, lang="en"):
    """Replace the whole FAQ list with `items` = [(q, a_html_or_text), ...]. Keeps wrapper + h2."""
    raw = _read(path)
    nxt = {"en": "Frequently Asked Questions", "zh-cn": "常见问题", "zh-tw": "常見問題"}
    blocks = []
    for i, (q, a) in enumerate(items, 1):
        blocks.append(
            '                    <div class="faq-item">\n'
            '                        <h3 class="faq-question-heading" style="margin:0"><button class="faq-question" aria-expanded="false">\n'
            '                            <span class="faq-question-text"><span class="faq-number">%d</span>%s</span>\n'
            '                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>\n'
            '                        </button></h3>\n'
            '                        <div class="faq-answer" role="region"><div class="faq-answer-inner">%s</div></div>\n'
            '                    </div>' % (i, q, a))
    new_list = ('                <div class="faq-list">\n' + "\n".join(blocks) + '\n                </div>\n')
    pat = re.compile(r'<div class="faq-list">.*?</div>\s*(?=</section>)', re.S)
    if not pat.search(raw):
        return "FAQ-LIST-NOT-FOUND"
    raw = pat.sub(lambda m: new_list, raw, count=1)
    _write(path, raw)
    return "faq-replaced %d" % len(items)


if __name__ == "__main__":
    print("import helpers from this module")


def rewrite_body(path, lead, sections, faq_items, lang="en"):
    """Replace the article body (lead + H2 sections + TOCs + FAQ) wholesale.

    sections: [(sec_id, title, body_html), ...]   faq_items: [(q, a), ...]
    Layout, ids/hrefs, class names and everything outside the body are preserved.
    """
    raw = _read(path)
    # 1. sidebar TOC
    nav = re.search(r'(<nav class="toc-links">)(.*?)(</nav>)', raw, re.S)
    if nav:
        links = "\n".join('                    <a href="#%s" class="toc-link">%s</a>' % (i, t)
                          for i, t, _ in sections)
        raw = raw[:nav.start(2)] + "\n" + links + "\n                " + raw[nav.end(2):]
    # 2. mobile TOC
    mt = re.search(r'(<div class="toc-mobile-links">)(.*?)(</div>)', raw, re.S)
    if mt:
        links = "\n".join('                    <a href="#%s" class="toc-mobile-link">%s</a>' % (i, t)
                          for i, t, _ in sections)
        raw = raw[:mt.start(2)] + "\n" + links + "\n                " + raw[mt.end(2):]
    # 3. body between the mobile-TOC block and the FAQ section
    art = re.search(r'<article\b[^>]*>', raw)
    mtoc = re.search(r'<div class="toc-mobile"[^>]*>.*?</div>\s*</div>', raw, re.S)
    start = mtoc.end() if mtoc else (art.end() if art else 0)
    fs = re.search(r'<section[^>]*class="faq-section"[^>]*>', raw)
    navm = re.search(r'<nav class="article-nav"', raw)
    art_end = raw.rfind('</article>')
    end = fs.start() if fs else (navm.start() if navm else art_end)
    if end < 0:
        return "BODY-END-NOT-FOUND"
    body = "\n".join('<h2 id="%s">%s</h2>\n%s\n' % (i, t, b) for i, t, b in sections)
    raw = raw[:start] + "\n" + lead + "\n" + body + "\n" + raw[end:]
    _write(path, raw)
    return ensure_faq_section(path, faq_items, lang)


FAQ_TITLE = {"en": "Frequently Asked Questions", "zh-cn": "常见问题", "zh-tw": "常見問題"}


def ensure_faq_section(path, items, lang="en"):
    """Insert a complete faq-section before </article> if the page has none; else replace its list."""
    raw = _read(path)
    if re.search(r'<section[^>]*class="faq-section"[^>]*>', raw):
        return replace_faq_list(path, items, lang)
    blocks = []
    for i, (q, a) in enumerate(items, 1):
        blocks.append(
            '                    <div class="faq-item">\n'
            '                        <h3 class="faq-question-heading" style="margin:0"><button class="faq-question" aria-expanded="false">\n'
            '                            <span class="faq-question-text"><span class="faq-number">%d</span>%s</span>\n'
            '                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>\n'
            '                        </button></h3>\n'
            '                        <div class="faq-answer" role="region"><div class="faq-answer-inner">%s</div></div>\n'
            '                    </div>' % (i, q, a))
    sec = (
        '\n            <section class="faq-section" id="faq" aria-label="%s">\n'
        '                <h2 class="faq-section-title">\n'
        '                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>\n'
        '                    %s\n'
        '                </h2>\n'
        '                <div class="faq-list">\n%s\n                </div>\n'
        '            </section>\n'
    ) % (FAQ_TITLE[lang], FAQ_TITLE[lang], "\n".join(blocks))
    nav = re.search(r'<nav class="article-nav"', raw)
    if nav:
        raw = raw[:nav.start()] + sec + "\n" + raw[nav.start():]
    else:
        e = raw.rfind('</article>')
        if e < 0:
            return "NO-ARTICLE-END"
        raw = raw[:e] + sec + raw[e:]
    _write(path, raw)
    return "faq-inserted %d" % len(items)


def rename_h2_by_id(path, hid, new):
    """Rename an H2 (and its TOC entries) matched by its id attribute."""
    raw = _read(path)
    pat = re.compile(r'(<h2 id="' + re.escape(hid) + r'"[^>]*>)(.*?)(</h2>)', re.S)
    m = pat.search(raw)
    if not m:
        return "H2-ID-NOT-FOUND:" + hid
    raw = pat.sub(lambda mm: mm.group(1) + new + mm.group(3), raw, count=1)
    toc = re.compile(r'(<a href="#' + re.escape(hid) + r'" class="toc-(?:mobile-)?link"[^>]*>)(.*?)(</a>)', re.S)
    raw, n = toc.subn(lambda mm: mm.group(1) + new + mm.group(3), raw)
    _write(path, raw)
    return "renamed-by-id (%d toc)" % n


def convert_tw(path, conv):
    """OpenCC-convert the article element and the sidebar TOC to Traditional Chinese."""
    raw = _read(path)
    a = re.search(r'<article\b[^>]*>', raw)
    e = raw.rfind('</article>')
    if a is None or e < 0:
        return "NO-ARTICLE"
    body = conv(raw[a.start():e])
    raw = raw[:a.start()] + body + raw[e:]
    nav = re.search(r'(<nav class="toc-links">)(.*?)(</nav>)', raw, re.S)
    if nav:
        raw = raw[:nav.start(2)] + conv(raw[nav.start(2):nav.end(2)]) + raw[nav.end(2):]
    _write(path, raw)
    return "converted"
