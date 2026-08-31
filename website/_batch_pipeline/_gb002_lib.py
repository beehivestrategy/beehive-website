#!/usr/bin/env python3
"""Shared helpers for gbatch_002 body expansion: H2 renames + new H2 sections + TOC sync."""
import os
import re

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
SLUGS = [l.strip() for l in open(os.path.join(ROOT, '_batch_pipeline/gap_batches/gbatch_002.txt')) if l.strip()]

H2_RE = re.compile(r'(<h2 id="([^"]*)"[^>]*>)(.*?)(</h2>)', re.S)
TOC_RE = re.compile(r'<a href="#([^"]*)" class="toc-mobile-link">(.*?)</a>', re.S)
TAG = re.compile(r'<[^>]+>')


def clean(x):
    import html as H
    return re.sub(r'\s+', ' ', H.unescape(TAG.sub('', x))).strip()


def slugify_en(t):
    s = t.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')


def path_for(slug, lang):
    pfx = {'en': '', 'zh-cn': 'zh-cn/', 'zh-tw': 'zh-tw/'}[lang]
    return os.path.join(ROOT, pfx, 'blog/articles', slug + '.html')


def apply_ops(slug, lang, renames=None, inserts=None, before='__FAQ__'):
    """renames: {old_h2_text: new_h2_text}
       inserts: [(h2_text, body_html)] inserted before `before` (H2 text or '__FAQ__')
    """
    p = path_for(slug, lang)
    doc = open(p, encoding='utf-8').read()
    ai = doc.find('<article class="article-content"')
    ae = doc.find('</article>', ai)
    art = doc[ai:ae]
    orig_art = art

    toc_end = art.find('</div>', art.find('class="toc-mobile-links"'))

    renames = renames or {}
    if renames:
        def repl(m):
            open_tag, hid, inner, close = m.groups()
            txt = clean(inner)
            if txt in renames:
                lead = re.match(r'\s*', inner).group(0)
                trail = re.search(r'\s*$', inner).group(0)
                inner = lead + renames[txt] + trail
            return open_tag + inner + close
        art = H2_RE.sub(repl, art)
        # sync TOC link text
        ids = {m.group(2): clean(m.group(3)) for m in H2_RE.finditer(art)}

        def toc_repl(m):
            hid, inner = m.group(1), m.group(2)
            if hid in ids:
                return f'<a href="#{hid}" class="toc-mobile-link">{ids[hid]}</a>'
            return m.group(0)
        head, tail = art[:toc_end], art[toc_end:]
        head = TOC_RE.sub(toc_repl, head)
        art = head + tail

    inserts = inserts or []
    if inserts:
        # determine insertion point
        if before == '__FAQ__':
            m = re.search(r'<section class="faq-section"', art)
            assert m, f'no faq section in {slug}'
            pos = m.start()
            marker_id = None
        else:
            found = None
            for m in H2_RE.finditer(art):
                if clean(m.group(3)) == before:
                    found = m
                    break
            assert found, f'anchor H2 "{before}" not found in {slug} {lang}'
            pos = found.start()
            marker_id = found.group(2)

        chunks = []
        toc_items = []
        for h2_text, body in inserts:
            hid = slugify_en(h2_text) if lang == 'en' else h2_text
            if not hid or (lang == 'en' and not re.match(r'^[a-z0-9]', hid)):
                hid = 'section-' + str(abs(hash(h2_text)) % 100000)
            chunks.append(f'<h2 id="{hid}">{h2_text}</h2>\n{body}\n')
            toc_items.append(f'<a href="#{hid}" class="toc-mobile-link">{h2_text}</a>')
        block = '\n'.join(chunks)
        art = art[:pos] + block + art[pos:]

        # TOC: insert before marker link, else at end of toc-mobile-links
        toc_marker = re.search(r'\s*(<a href="#' + re.escape(marker_id) + r'" class="toc-mobile-link">)', art) if marker_id else None
        if toc_marker:
            ins = '\n                    ' + '\n                    '.join(toc_items)
            art = art[:toc_marker.start()] + ins + art[toc_marker.start():]
        else:
            end = art.find('</div>', art.find('class="toc-mobile-links"'))
            ins = '\n                    ' + '\n                    '.join(toc_items) + '\n                '
            art = art[:end] + ins + art[end:]

    if art != orig_art:
        doc = doc[:ai] + art + doc[ae:]
        open(p, 'w', encoding='utf-8').write(doc)
    return art != orig_art
