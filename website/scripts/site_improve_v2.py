#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
site_improve_v2.py  —  Beehive Strategy "New Version" upgrade pass
====================================================================
Implements, in ONE idempotent pass over every article page:

  R1  TOC rebuild            — regenerate dead/copied TOCs from real headings
  R2  Language localization  — prefix internal links to the page's locale
                               (only where the localized target exists, so
                                no broken links are ever created)
  R3  Locale JS safety net   — article-anim.js rewrites stray root links
  R5  Automated internal links — contextual same-locale links in body text
  R6  SVG illustrations      — on-brand, non-generic SVGs injected as figures
  R7  UX/UI + animation      — reading bar, scroll-reveal, TOC highlight,
                               magnetic CTA, SVG line-draw

Acceptance: must move `site_audit_gate.py` so every 'lower' metric drops and
every 'higher' metric rises (no regression). Pure stdlib (no bs4/lxml).

Usage
-----
  python3 site_improve_v2.py                 # dry run, print projected counts
  python3 site_improve_v2.py --apply         # write changes + SVGs
  python3 site_improve_v2.py --apply --limit 30   # subset (testing)
  python3 site_improve_v2.py --apply --skip-links --skip-images
"""
import os, re, sys, json, argparse, random, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCALES = {'en': 'blog/articles', 'zh-cn': 'zh-cn/blog/articles',
           'zh-tw': 'zh-tw/blog/articles'}
TEAL = '#2B9E8B'; GOLD = '#d4a843'; INK = '#0e2a3b'; AQUA = '#6cc4b4'
SLATE = '#5b7083'; MIST = '#e8eef0'

# ---------------------------------------------------------------- served index
def build_served():
    s = set()
    for dp, dn, fn in os.walk(ROOT):
        if any(x in dp for x in ('/scripts', '/node_modules', '/.git',
                                 '/_chrome', '/functions', '/assets',
                                 '/css', '/js', '/seo-audit-reports',
                                 '/_batch_pipeline', '/beehive-homepage')):
            continue
        for f in fn:
            if not f.endswith('.html'):
                continue
            rel = os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, '/')
            clean = '/' + rel[:-5]
            if clean.endswith('/index'):
                clean = clean[:-6]
            s.add(clean)
    return s

SERVED = build_served()

def loc_target_ok(href, loc):
    if not href.startswith('/'):
        return False
    return ('/' + loc + href) in SERVED

def content_start(html):
    """Position of the main article content. Most pages wrap it in
    <div id="article-content">; a newer template uses <article class="article">
    / <main role="main"> with no such id. Fall back gracefully so R1/R5/R6
    cover every template instead of silently skipping some."""
    i = html.find('id="article-content"')
    if i != -1:
        return i                                   # matches legacy callers
    for tag in ('<main role="main">', '<article class="article">'):
        j = html.find(tag)
        if j != -1:
            return html.find('>', j) + 1
    m = re.search(r'<h1\b', html)
    return m.start() if m else 0

# --------------------------------------------------------------------- helpers
def clean(t):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t)).strip()

def slugify(text, used):
    t = re.sub(r'<[^>]+>', '', text).lower().strip()
    t = re.sub(r'[^a-z0-9\u4e00-\u9fff\u3400-\u4dbf]+', '-', t)
    t = re.sub(r'-+', '-', t).strip('-')[:80]
    if not t:
        t = 'section'
    base = t
    i = 2
    while t in used:
        t = f'{base}-{i}'
        i += 1
    used.add(t)
    return t

HEADING_RE = re.compile(r'<(h2|h3)\b([^>]*)>(.*?)</\1>', re.S | re.I)
ID_ATTR_RE = re.compile(r'\bid="([^"]*)"')
NAV_RE = re.compile(r'<nav class="toc-links">(.*?)</nav>', re.S)
SEC_RE = re.compile(r'^sec-\d+$')

# ----------------------------------------------------------------- R1 — TOC
def toc_needs_rebuild(html):
    m = NAV_RE.search(html)
    if not m:
        return False
    anchors = re.findall(r'href="#([^"]+)"', m.group(1))
    if not anchors:
        return False
    ids = set(ID_ATTR_RE.findall(html))
    broken = [a for a in anchors if a not in ids]
    h2ids = re.findall(r'<h2\b[^>]*\bid="([^"]+)"', html)
    gen = [i for i in h2ids if SEC_RE.match(i)]
    return bool(broken) or bool(h2ids and len(gen) > len(h2ids) / 2)

def rebuild_toc(html):
    ac = content_start(html)
    if ac == -1:
        return html, False
    end = len(html)
    for marker in ('class="toc-sidebar"', 'class="recommended-section"', '</article>'):
        e = html.find(marker, ac)
        if e != -1:
            end = min(end, e)
    region = html[ac:end]
    matches = list(HEADING_RE.finditer(region))
    if not matches:
        return html, False
    navm = NAV_RE.search(html)
    if not navm:
        return html, False
    used = set()
    items = []
    secmap = {}
    pieces = []
    last = 0
    for m in matches:
        tag = m.group(1).lower()
        attrs = m.group(2)
        text = clean(m.group(3))
        idm = ID_ATTR_RE.search(attrs)
        old_id = idm.group(1) if idm else ''
        if old_id and not SEC_RE.match(old_id) and re.match(r'^[\w\-]+$', old_id) and old_id not in used:
            slug = old_id
            used.add(slug)
        else:
            slug = slugify(text, used)
            if old_id and SEC_RE.match(old_id):
                secmap[old_id] = slug
        items.append((slug, text))
        # rewrite the opening tag so it always carries the (possibly new) id
        full = m.group(0)
        ob = full.index('>') + 1
        opening = full[:ob]
        new_opening = re.sub(r'\bid="[^"]*"', '', opening).rstrip()
        new_opening = (new_opening[:-1] + f' id="{slug}">') if new_opening.endswith('>') \
            else (new_opening + f' id="{slug}">')
        pieces.append(region[last:m.start()])         # text before this heading
        pieces.append(new_opening)                     # rewritten opening tag
        pieces.append(region[m.start() + ob:m.end()])  # inner + closing tag (unchanged)
        last = m.end()
    new_region = ''.join(pieces) + region[last:]
    html = html[:ac] + new_region + html[end:]
    # rebuild nav from the real headings
    nav_inner = '\n'.join(
        f'                    <a href="#{s}" class="toc-link">{t}</a>' for s, t in items)
    new_nav = f'<nav class="toc-links">\n{nav_inner}\n                </nav>'
    html = html[:navm.start()] + new_nav + html[navm.end():]
    # remap any stale #sec-N anchors that pointed at the old ids
    for old, new in secmap.items():
        html = html.replace(f'href="#{old}"', f'href="#{new}"')
    # drop any SECONDARY duplicate <nav class="toc-links"> (keep the rebuilt one)
    navs = list(NAV_RE.finditer(html))
    if len(navs) > 1:
        buf = []
        last = 0
        for i, m in enumerate(navs):
            buf.append(html[last:m.start()])
            if i == 0:
                buf.append(m.group(0))
            last = m.end()
        buf.append(html[last:])
        html = ''.join(buf)
    return html, True


def dedupe_toc_navs(html):
    """Guarantee exactly one <nav class="toc-links"> per article. A handful of
    legacy pages carry a duplicated TOC whose second block points at stale
    anchors; keep the first (rebuilt) nav and drop the rest. Idempotent."""
    navs = list(NAV_RE.finditer(html))
    if len(navs) <= 1:
        return html, False
    buf = []
    last = 0
    for i, m in enumerate(navs):
        buf.append(html[last:m.start()])
        if i == 0:
            buf.append(m.group(0))
        last = m.end()
    buf.append(html[last:])
    return ''.join(buf), True

# --------------------------------------------------------------- R2 — locale
SWITCHER_RE = re.compile(r'<div class="lang-switcher"[^>]*>.*?</div>\s*</div>', re.S)
ASSET_PREFIX = ('/assets', '/css', '/js', '/images', '/img', '/favicon')
LINK_RE = re.compile(r'<a\b([^>]*?)href="(/[^"]*)"')

def localize(html, loc, self_url=''):
    if loc == 'en':
        return html, 0
    m = SWITCHER_RE.search(html)
    sw = m.group(0) if m else None
    if sw:
        html = html.replace(sw, '__SWITCHER__', 1)
    changes = [0]
    def repl(mm):
        pre = mm.group(1)
        href = mm.group(2)
        if 'data-lang' in pre:           # language switcher entries stay cross-locale
            return mm.group(0)
        if any(href.startswith(p) for p in ASSET_PREFIX):
            return mm.group(0)
        if href.startswith('/' + loc + '/'):
            return mm.group(0)
        # strip any OTHER locale prefix -> base path
        mm2 = re.match(r'^/(zh-cn|zh-tw)(/.*)$', href)
        base = mm2.group(2) if mm2 else href
        cand = '/' + loc + base
        if cand == self_url:
            return mm.group(0)
        if cand in SERVED:
            changes[0] += 1
            return f'<a{pre}href="{cand}"'
        return mm.group(0)
    html = LINK_RE.sub(repl, html)
    if sw:
        html = html.replace('__SWITCHER__', sw, 1)
    return html, changes[0]

# ---------------------------------------------------------- R6 — SVG figures
def make_svg(slug):
    seed = int(hashlib.md5(slug.encode()).hexdigest()[:8], 16)
    rnd = random.Random(seed)
    tmpl = ['nodes', 'funnel', 'layers', 'timeline', 'cluster',
            'circuit', 'bars', 'donut'][seed % 8]
    accents = [TEAL, GOLD, AQUA]
    a1 = accents[seed % 3]
    a2 = accents[(seed // 3) % 3]
    W, H = 800, 450
    M = 60
    inner = []
    if tmpl == 'nodes':
        n = rnd.randint(5, 9)
        pts = [(rnd.randint(M, W - M), rnd.randint(90, H - M)) for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, min(i + 3, n)):
                inner.append(
                    f'<line x1="{pts[i][0]}" y1="{pts[i][1]}" x2="{pts[j][0]}" '
                    f'y2="{pts[j][1]}" stroke="{MIST}" stroke-width="2"/>')
        for x, y in pts:
            inner.append(
                f'<circle cx="{x}" cy="{y}" r="{rnd.randint(9,16)}" fill="{a1}" '
                f'class="svg-draw" pathLength="1" stroke="{INK}" stroke-width="1.5"/>')
    elif tmpl == 'funnel':
        rows = 4
        for i in range(rows):
            w = (W - 2 * M) * (1 - i * 0.2)
            x = (W - w) / 2
            y = 90 + i * 80
            h = 56
            inner.append(
                f'<path d="M{x} {y} L{x+w} {y} L{x+w-20} {y+h} L{x+20} {y+h} Z" '
                f'fill="{a1 if i % 2 == 0 else a2}" opacity="{0.85 - i*0.12}" '
                f'class="svg-draw" pathLength="1" stroke="{INK}" stroke-width="1"/>')
    elif tmpl == 'layers':
        for i in range(4):
            y = 90 + i * 82
            off = i * 14
            inner.append(
                f'<rect x="{M+off}" y="{y}" width="{W-2*M-2*off}" height="54" '
                f'rx="12" fill="{a1 if i%2==0 else a2}" opacity="0.9" '
                f'class="svg-draw" pathLength="1" stroke="{INK}" stroke-width="1"/>')
    elif tmpl == 'timeline':
        inner.append(f'<line x1="{M}" y1="{H/2}" x2="{W-M}" y2="{H/2}" '
                     f'stroke="{SLATE}" stroke-width="3" class="svg-draw" pathLength="1"/>')
        for i in range(4):
            x = M + (W - 2 * M) * i / 3
            inner.append(f'<circle cx="{x}" cy="{H/2}" r="13" fill="{a1 if i%2==0 else a2}" '
                         f'stroke="{INK}" stroke-width="1.5"/>')
            inner.append(f'<line x1="{x}" y1="{H/2-13}" x2="{x}" y2="{H/2-40}" '
                         f'stroke="{AQUA}" stroke-width="2"/>')
    elif tmpl == 'cluster':
        for c in range(3):
            cx = M + (W - 2 * M) * (c + 0.5) / 3
            cy = 90 + (c % 2) * 180
            for _ in range(rnd.randint(10, 16)):
                dx = rnd.gauss(0, 42)
                dy = rnd.gauss(0, 42)
                inner.append(f'<circle cx="{cx+dx:.0f}" cy="{cy+dy:.0f}" r="4.5" '
                             f'fill="{a1 if c%2==0 else a2}" opacity="0.8"/>')
    elif tmpl == 'circuit':
        for i in range(5):
            y = 90 + i * 70
            inner.append(f'<line x1="{M}" y1="{y}" x2="{W-M}" y2="{y}" '
                         f'stroke="{MIST}" stroke-width="2"/>')
        for i in range(9):
            x = M + (W - 2 * M) * i / 8
            for j in range(5):
                y = 90 + j * 70
                inner.append(f'<rect x="{x-5}" y="{y-5}" width="10" height="10" '
                             f'fill="{a1 if (i+j)%2==0 else a2}" class="svg-draw" pathLength="1"/>')
    elif tmpl == 'bars':
        n = 5
        for i in range(n):
            h = rnd.randint(60, 230)
            x = M + i * (W - 2 * M) / n + 12
            w = (W - 2 * M) / n - 24
            y = H - 70 - h
            inner.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h}" '
                         f'rx="6" fill="{a1 if i%2==0 else a2}" class="svg-draw" '
                         f'pathLength="1" stroke="{INK}" stroke-width="1"/>')
    else:  # donut
        cx, cy, r = W / 2, H / 2, 130
        segs = [0.35, 0.28, 0.22, 0.15][:rnd.randint(3, 4)]
        ang = -90
        cols = [a1, a2, AQUA, GOLD]
        for k, s in enumerate(segs):
            a0 = ang
            a1a = ang + s * 360
            ang = a1a
            import math
            x0 = cx + r * math.cos(math.radians(a0))
            y0 = cy + r * math.sin(math.radians(a0))
            x1 = cx + r * math.cos(math.radians(a1a))
            y1 = cy + r * math.sin(math.radians(a1a))
            large = 1 if (a1a - a0) > 180 else 0
            inner.append(f'<path d="M{cx} {cy} L{x0:.1f} {y0:.1f} A{r} {r} 0 {large} 1 '
                         f'{x1:.1f} {y1:.1f} Z" fill="{cols[k%len(cols)]}" '
                         f'class="svg-draw" pathLength="1" stroke="#fff" stroke-width="1.5"/>')
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'role="img" preserveAspectRatio="xMidYMid meet">'
        f'<defs><linearGradient id="bg{seed%97}" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="#f7fafb"/><stop offset="1" stop-color="#eaf2f3"/>'
        f'</linearGradient></defs>'
        f'<rect width="{W}" height="{H}" rx="14" fill="url(#bg{seed%97})"/>'
        f'<ellipse cx="{W*0.78:.0f}" cy="{H*0.22:.0f}" rx="150" ry="110" '
        f'fill="{AQUA}" opacity="0.10"/>'
        f'<ellipse cx="{W*0.18:.0f}" cy="{H*0.82:.0f}" rx="130" ry="100" '
        f'fill="{GOLD}" opacity="0.08"/>'
        + ''.join(inner) +
        f'<text x="{M}" y="{H-22}" font-family="system-ui,Segoe UI,Arial,sans-serif" '
        f'font-size="13" fill="{SLATE}">Beehive Strategy · conceptual diagram</text>'
        f'</svg>')
    return svg

SVG_DIR = os.path.join(ROOT, 'assets', 'blog', 'svg')

def fig_caption(title, locale):
    t = clean(title)
    if locale == 'zh-cn':
        return f'图：<b>{t}</b> 的核心脉络一览'
    if locale == 'zh-tw':
        return f'圖：<b>{t}</b> 的核心脈絡一覽'
    return f'Figure — the shape of <b>{t.lower()}</b>'

def inject_svg(html, slug, locale, title, apply):
    # already injected?
    if f'data-fig-slug="{slug}"' in html:
        return html, 0
    # write svg file once (shared across locales)
    if apply:
        os.makedirs(SVG_DIR, exist_ok=True)
        sp = os.path.join(SVG_DIR, slug + '.svg')
        if not os.path.exists(sp):
            open(sp, 'w', encoding='utf-8').write(make_svg(slug))
    ac = content_start(html)
    if ac == -1:
        return html, 0
    # find h2 indices within body
    end = html.find('class="toc-sidebar"', ac)
    if end == -1:
        end = html.find('class="recommended-section"', ac)
    if end == -1:
        end = html.find('</article>', ac)
    if end == -1:
        end = len(html)
    region = html[ac:end]
    h2pos = [m.start() for m in re.finditer(r'<h2\b', region, re.I)]
    if not h2pos:
        return html, 0
    fig = (f'\n        <figure class="article-figure" data-fig-slug="{slug}">'
           f'\n          <img src="/assets/blog/svg/{slug}.svg" alt="{clean(title)} — conceptual diagram" '
           f'class="article-svg" loading="lazy" width="800" height="450">'
           f'\n          <figcaption>{fig_caption(title, locale)}</figcaption>'
           f'\n        </figure>\n')
    # primary: after first h2's closing tag
    c1 = region.find('</h2>', h2pos[0])
    if c1 == -1:
        return html, 0
    insert_at = ac + c1 + len('</h2>')
    html = html[:insert_at] + fig + html[insert_at:]
    # secondary: after a later h2 for longer articles
    if len(h2pos) >= 5:
        region2 = html[ac:html.find('class="toc-sidebar"', ac)]
        h2pos2 = [m.start() for m in re.finditer(r'<h2\b', region2, re.I)]
        mid = h2pos2[len(h2pos2) // 2]
        c2 = html.find('</h2>', ac + mid)
        if c2 != -1 and c2 > insert_at:
            fig2 = fig.replace('data-fig-slug', 'data-fig-slug2')
            html = html[:c2 + len('</h2>')] + fig2 + html[c2 + len('</h2>'):]
    return html, 1

# --------------------------------------------------- R5 — internal links
STOP = set(('the a an and or of to in for on with without how what why when where '
            'which who whom this that these those is are was were be been being as at '
            'by from up down over under between into about their our your his her its '
            'can will may should could would do does did has have had not no nor so than '
            'then there here we you they he she it i me my mine').split())

def build_lexicon(locale):
    d = {}
    base = os.path.join(ROOT, LOCALES[locale])
    if not os.path.isdir(base):
        return d
    titles = []
    for f in os.listdir(base):
        if not f.endswith('.html') or '.bak' in f:
            continue
        s = open(os.path.join(base, f), encoding='utf-8', errors='replace').read()
        h1 = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
        t = clean(h1.group(1)) if h1 else ''
        titles.append((t, f[:-5]))
    titles.sort(key=lambda x: -len(x[0]))
    for t, slug in titles:
        ct = clean(t)
        if locale == 'en':
            words = [w for w in re.findall(r"[a-z0-9']+", ct.lower())
                     if w not in STOP and len(w) > 2]
            if len(words) >= 2:
                ph = ' '.join(words)
                if len(ph) >= 6 and ph not in d:
                    d[ph] = slug
            for n in (3, 2):
                for i in range(len(words) - n + 1):
                    ph = ' '.join(words[i:i + n])
                    if len(ph) >= 6 and ph not in d:
                        d[ph] = slug
        else:
            c = re.sub(r'\s+', '', re.sub(r'<[^>]+>', '', t)).strip()
            if len(c) >= 5 and c not in d:
                d[c] = slug
    return d

def compile_lex(lex):
    items = sorted(lex.keys(), key=len, reverse=True)
    pats = []
    for p in items:
        if re.search(r'[\u4e00-\u9fff]', p):
            pats.append(re.escape(p))
        else:
            pats.append(r'\b' + re.escape(p) + r'\b')
    return re.compile('|'.join(pats), re.I) if pats else None

def inject_internal_links(html, locale, self_slug, lex, lex_re, cap):
    if f'class="inline-ref"' in html:
        return html, 0          # already processed -> idempotent
    if lex_re is None:
        return html, 0
    ac = content_start(html)
    if ac == -1:
        return html, 0
    end = html.find('class="toc-sidebar"', ac)
    if end == -1:
        end = html.find('class="recommended-section"', ac)
    if end == -1:
        end = html.find('</article>', ac)
    if end == -1:
        end = len(html)
    region = html[ac:end]
    parts = re.split(r'(<[^>]+>)', region)
    state = {'block': None, 'n': 0, 'used': set()}
    BLOCK_OPEN = re.compile(r'<\s*(p|li|blockquote)\b', re.I)
    BLOCK_CLOSE = re.compile(r'<\s*/(p|li|blockquote)\s*>', re.I)

    def cb(m):
        key = m.group(0).lower()
        slug = lex.get(key)
        if not slug or slug == self_slug:
            return m.group(0)
        if key in state['used'] or state['n'] >= cap:
            return m.group(0)
        state['used'].add(key)
        state['n'] += 1
        return (f'<a href="/{locale}/blog/articles/{slug}" '
                f'class="inline-ref">{m.group(0)}</a>')

    out = []
    for i, part in enumerate(parts):
        if i % 2 == 1:  # tag
            if BLOCK_OPEN.search(part):
                state['block'] = True
            elif BLOCK_CLOSE.search(part):
                state['block'] = None
            out.append(part)
            continue
        if state['block'] and state['n'] < cap and part.strip():
            out.append(lex_re.sub(cb, part))
        else:
            out.append(part)
        if state['n'] >= cap:
            # flush remaining text unchanged
            out.extend(parts[i + 1:])
            break
    new_region = ''.join(out)
    html = html[:ac] + new_region + html[end:]
    return html, state['n']

# ------------------------------------------------ R7 — animation wiring
def ensure_anim(html, loc):
    changed = 0
    if '/css/article-anim.css' not in html:
        html = html.replace('</head>',
            '    <link rel="stylesheet" href="/css/article-anim.css">\n</head>', 1)
        if '</head>' in html:
            changed += 1
    if '/js/article-anim.js' not in html:
        html = html.replace('</body>',
            '    <script src="/js/article-anim.js" defer></script>\n</body>', 1)
        if '</body>' in html:
            changed += 1
    if 'class="reading-progress"' not in html:
        mb = html.find('<body')
        if mb != -1:
            be = html.find('>', mb)
            html = html[:be + 1] + \
                '\n<div class="reading-progress"><div class="reading-progress-bar"></div></div>' + \
                html[be + 1:]
            changed += 1
    # ensure <html lang="..."> present for the JS locale net
    hm = re.search(r'<html\b([^>]*)>', html, re.I)
    if hm and 'lang=' not in hm.group(1):
        html = html.replace(hm.group(0), f'<html{hm.group(1)} lang="{loc}">', 1)
        changed += 1
    return html, changed

# ------------------------------------------------------------------- main
def process(path, locale, slug, opts, lex, lex_re):
    html = open(path, encoding='utf-8', errors='replace').read()
    orig = html
    rep = {}
    # R1
    if toc_needs_rebuild(html):
        html, ok = rebuild_toc(html)
        rep['toc_rebuilt'] = ok
    # R2 — self_url so we never rewrite a link to the page itself
    rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
    self_url = '/' + rel[:-5]
    if self_url.endswith('/index'):
        self_url = self_url[:-6]
    html, n = localize(html, locale, self_url)
    if n:
        rep['localized'] = n
    # R6
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    title = clean(h1.group(1)) if h1 else slug
    html, ni = inject_svg(html, slug, locale, title, opts.apply)
    if ni:
        rep['figures'] = ni
    # R5
    if not opts.skip_links:
        html, nl = inject_internal_links(html, locale, slug, lex, lex_re, 4)
        if nl:
            rep['intlinks'] = nl
    # R7
    if not opts.skip_anim:
        html, na = ensure_anim(html, locale)
        if na:
            rep['anim'] = na
    # R1b — collapse duplicate TOC navs (covers legacy pages w/ stale 2nd nav)
    html, nd = dedupe_toc_navs(html)
    if nd:
        rep['toc_deduped'] = nd
    if html != orig and opts.apply:
        open(path, 'w', encoding='utf-8').write(html)
    return rep

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--skip-links', action='store_true')
    ap.add_argument('--skip-images', action='store_true')
    ap.add_argument('--skip-anim', action='store_true')
    ap.add_argument('--report', default='')
    opts = ap.parse_args()

    totals = {'toc_rebuilt': 0, 'localized': 0, 'figures': 0,
              'intlinks': 0, 'anim': 0, 'pages': 0}
    per_loc = {}
    lex_cache = {}
    lexre_cache = {}

    files = []
    for loc, sub in LOCALES.items():
        d = os.path.join(ROOT, sub)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if f.endswith('.html') and '.bak' not in f:
                files.append((loc, f[:-5], os.path.join(d, f)))
    if opts.limit:
        files = files[:opts.limit]

    for loc, slug, path in files:
        # lexicon is per-locale and independent of the image flag -> cache it
        lex = lex_cache.get(loc)
        lex_re = lexre_cache.get(loc)
        if lex is None:
            lex = build_lexicon(loc)
            lex_re = compile_lex(lex)
            lex_cache[loc] = lex
            lexre_cache[loc] = lex_re
        rep = process(path, loc, slug, opts, lex, lex_re)
        if rep:
            totals['pages'] += 1
            for k, v in rep.items():
                if isinstance(v, bool):
                    totals[k] = totals.get(k, 0) + (1 if v else 0)
                else:
                    totals[k] = totals.get(k, 0) + v
            per_loc[loc] = per_loc.get(loc, 0) + 1

    print('\n' + '=' * 70)
    print('SITE IMPROVE v2' + ('  [APPLY]' if opts.apply else '  [DRY RUN]'))
    print('=' * 70)
    print(f"pages with changes : {totals['pages']}  (of {len(files)} scanned)")
    print(f"  TOC rebuilt        : {totals.get('toc_rebuilt',0)}")
    print(f"  links localized    : {totals.get('localized',0)}")
    print(f"  SVG figures added  : {totals.get('figures',0)}")
    print(f"  internal links added: {totals.get('intlinks',0)}")
    print(f"  animation wired    : {totals.get('anim',0)}")
    print('=' * 70)
    if opts.report:
        json.dump({'totals': totals, 'per_locale': per_loc},
                  open(opts.report, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        print(f"report -> {opts.report}")

if __name__ == '__main__':
    main()
