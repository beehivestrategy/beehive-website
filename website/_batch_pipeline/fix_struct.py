#!/usr/bin/env python3
"""Structural fixes for GEO/SEO standard.

Subcommands:
  h2map   -- rewrite content <h2> texts to question form (and TOC links)
  toc     -- regenerate TOC link lists (mobile + sidebar) from content <h2>s
  faq     -- wrap FAQ buttons in <h3>, ensure >=3 items
  ld      -- insert/update FAQPage JSON-LD immediately after </section> of faq-section
  all     -- faq + ld + toc
"""
import re, sys, os, json, html as H

H2RE = re.compile(r'<h2 id="([^"]*)">(.*?)</h2>', re.S)
TOC_CLASSES = ['toc-mobile-link', 'toc-link', 'toc-desktop-link']


def slugify(t):
    t = re.sub(r'<[^>]+>', '', t)
    t = t.strip().lower()
    t = t.replace('&', '')
    t = re.sub(r"['’]", '', t)
    t = re.sub(r'[^a-z0-9一-鿿]+', '-', t)
    t = re.sub(r'^-+|-+$', '', t)
    return t or 'section'


def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s).strip()


def read(p):
    return open(p, encoding='utf-8').read()


def write(p, s):
    open(p, 'w', encoding='utf-8').write(s)


def head_end(raw):
    return raw.find('</head>')


# ---------------- h2map ----------------
def do_h2map(path, mapping, dry=False):
    raw = read(path)
    hc = head_end(raw)
    out = raw
    changes = []

    def repl(m):
        hid, inner = m.group(1), m.group(2)
        text = strip_tags(inner)
        if text in mapping:
            new = mapping[text]
            nid = slugify(new)
            changes.append((text, new, hid, nid))
            return f'<h2 id="{nid}">{H.escape(new)}</h2>'
        return m.group(0)

    out = H2RE.sub(repl, out)
    # update TOC links by old id -> new id/new text
    for old_text, new_text, old_id, new_id in changes:
        for cls in TOC_CLASSES:
            out = out.replace(f'<a href="#{old_id}" class="{cls}">{H.escape(old_text)}</a>',
                              f'<a href="#{new_id}" class="{cls}">{H.escape(new_text)}</a>')
            out = out.replace(f'<a href="#{old_id}" class="{cls}">{old_text}</a>',
                              f'<a href="#{new_id}" class="{cls}">{new_text}</a>')
    if not dry:
        write(path, out)
    return changes


# ---------------- toc ----------------
def do_toc(path, dry=False):
    raw = read(path)
    h2s = [(m.group(1), strip_tags(m.group(2))) for m in H2RE.finditer(raw)]
    if not h2s:
        return 0
    out = raw
    n = 0
    for cls in TOC_CLASSES:
        m = re.search(r'(<div class="[^"]*' + cls + r's?"[^>]*>)(.*?)(</div>)', out, re.S)
        if not m:
            continue
        indent = '                    '
        items = '\n'.join(f'{indent}<a href="#{i}" class="{cls}">{H.escape(t)}</a>' for i, t in h2s)
        block = m.group(1) + '\n' + items + '\n' + indent[:-4] + m.group(3)
        out = out[:m.start()] + block + out[m.end():]
        n += 1
    if not dry and n:
        write(path, out)
    return n


# ---------------- faq h3 ----------------
def find_faq(raw):
    m = re.search(r'<section[^>]*class="faq-section"', raw)
    if not m:
        return None
    s = m.start()
    e = raw.find('</section>', s)
    return (s, e + len('</section>')) if e != -1 else None


def do_faq(path, dry=False):
    raw = read(path)
    rng = find_faq(raw)
    if not rng:
        return 'no-faq-section'
    s, e = rng
    blk = raw[s:e]
    n = 0
    # wrap each <button class="faq-question" ...>...</button> in h3, unless already wrapped
    pat = re.compile(r'(?<!Heading">)(<button class="faq-question"[^>]*>.*?</button>)', re.S)

    def w(m):
        nonlocal n
        n += 1
        return ('<h3 class="faq-question-heading" '
                'style="margin:0;font-weight:inherit;font-size:inherit;line-height:inherit;">'
                + m.group(1) + '</h3>')

    newblk = pat.sub(w, blk)
    out = raw[:s] + newblk + raw[e:]
    if not dry and n:
        write(path, out)
    return n


# ---------------- ld ----------------
def parse_faq_items(raw):
    rng = find_faq(raw)
    if not rng:
        return []
    blk = raw[rng[0]:rng[1]]
    items = []
    for m in re.finditer(r'class="faq-question"[^>]*>(.*?)</button>', blk, re.S):
        q = m.group(1)
        q = re.sub(r'<span class="faq-number">\s*\d+\s*</span>', '', q)
        q = re.sub(r'<svg.*?</svg>', '', q, flags=re.S)
        q = strip_tags(q).strip()
        rest = blk[m.end():]
        am = re.search(r'class="faq-answer-inner">(.*?)</div>', rest, re.S)
        a = strip_tags(am.group(1)).strip() if am else ''
        items.append((q, a))
    return items


def build_ld(items):
    ents = []
    for q, a in items:
        ents.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        })
    return ('\n<script type="application/ld+json">\n'
            + json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                          "mainEntity": ents}, ensure_ascii=False, indent=2)
            + '\n</script>\n')


def do_ld(path, dry=False):
    raw = read(path)
    rng = find_faq(raw)
    if not rng:
        return 'no-faq-section'
    items = parse_faq_items(raw)
    if len(items) < 3:
        return f'only-{len(items)}-items'
    s, e = rng
    hc = head_end(raw)
    ld = build_ld(items)
    # remove any existing body FAQPage script
    body = raw[hc:]
    m = re.search(r'\n?<script type="application/ld\+json">\s*\{.*?"FAQPage".*?</script>\n?', body, re.S)
    status = 'updated' if m else 'added'
    if m:
        body = body[:m.start()] + ld + body[m.end():]
        raw = raw[:hc] + body
    else:
        raw = raw[:e] + '\n' + ld + raw[e:]
    if not dry:
        write(path, raw)
    return status


if __name__ == '__main__':
    cmd = sys.argv[1]
    files = sys.argv[2:]
    mapfile = None
    if cmd == 'h2map':
        mapfile = files[0]
        files = files[1:]
    for f in files:
        if cmd == 'h2map':
            mp = json.load(open(mapfile, encoding='utf-8'))
            c = do_h2map(f, mp.get(os.path.basename(f), mp))
            print(f, 'h2map', len(c), [x[1] for x in c])
        elif cmd == 'toc':
            print(f, 'toc', do_toc(f))
        elif cmd == 'faq':
            print(f, 'faq', do_faq(f))
        elif cmd == 'ld':
            print(f, 'ld', do_ld(f))
        elif cmd == 'all':
            print(f, 'faq', do_faq(f), '| ld', do_ld(f), '| toc', do_toc(f))
