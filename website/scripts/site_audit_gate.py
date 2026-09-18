#!/usr/bin/env python3
"""
Beehive Strategy — Site Audit Gate (pre-deploy quality gate)

Consolidates the 2026-09-03 deep audit into ONE repeatable check that can be run
before every deploy. Any metric that gets WORSE than the recorded baseline fails
the gate (exit 1), so batch-generation regressions (stale TOC blocks, wrong-locale
links, slug-derived card titles, missing images) are caught before they reach prod.

Usage
-----
  python3 site_audit_gate.py                    # run, compare vs baseline (if any)
  python3 site_audit_gate.py --write-baseline   # record current numbers as baseline
  python3 site_audit_gate.py --emit-fixlist     # also write exact file lists per defect
  python3 site_audit_gate.py --json             # machine-readable summary

Exit codes
----------
  0 = pass (no regression)      1 = FAIL (regression)      2 = no baseline recorded
"""

import os
import re
import sys
import json
import argparse

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT_DIR = os.path.abspath(os.path.join(ROOT, '..', 'gsc_out'))
BASELINE = os.path.join(OUT_DIR, 'site_audit_baseline.json')

SKIP_DIRS = {'_chrome', 'scripts', 'functions', 'node_modules', 'templates',
             'beehive-homepage', 'beehive-homepage-draft', '_batch_pipeline',
             'seo-audit-reports', 'assets', 'css', 'js', '.git'}

LOCALES = {'en': 'blog/articles', 'zh-cn': 'zh-cn/blog/articles',
           'zh-tw': 'zh-tw/blog/articles'}

# ---------- helpers ----------
HREF_RE = re.compile(r'<a\b[^>]*href="([^"]*)"', re.I)
ANCHOR_RE = re.compile(r'href="#([^"]+)"')
ID_RE = re.compile(r'\bid="([^"]+)"')
IMG_RE = re.compile(r'<img\b[^>]*>', re.I)
SRC_RE = re.compile(r'\bsrc="([^"]*)"')
ALT_RE = re.compile(r'\balt="([^"]*)"')
H2_RE = re.compile(r'<h2\b[^>]*\bid="([^"]+)"')
GEN_ID_RE = re.compile(r'^sec-\d+$')
SWITCHER_RE = re.compile(r'<div class="lang-switcher"[^>]*>.*?</div>\s*</div>', re.S)
CTA_RE = re.compile(r'<div class="article-cta-actions">(.*?)</div>', re.S)
REC_BLOCK_RE = re.compile(r'<div class="recommended-grid">(.*?)</div>\s*</section>', re.S)
CARD_RE = re.compile(r'<a href="([^"]+)" class="recommended-card">(.*?)</a>', re.S)
CARD_TITLE_RE = re.compile(r'class="recommended-card-title">(.*?)</h3>', re.S)


def read(p):
    try:
        with open(p, encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return ''


def strip_tags(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s)).strip()


def is_asset(h):
    return (h.startswith(('/assets', '/css', '/js', '/images', '/img', '/favicon'))
            or h.startswith(('#', 'mailto:', 'tel:'))
            or h.endswith(('.xml', '.txt', '.png', '.jpg', '.jpeg',
                           '.svg', '.ico', '.webp', '.pdf')))


def iter_articles():
    for loc, sub in LOCALES.items():
        d = os.path.join(ROOT, sub)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if fn.endswith('.html') and '.bak' not in fn:
                yield loc, fn[:-5], os.path.join(d, fn)


def iter_all_pages():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith('.html') and '.bak' not in fn:
                p = os.path.join(dirpath, fn)
                rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
                loc = 'zh-cn' if rel.startswith('zh-cn/') else (
                    'zh-tw' if rel.startswith('zh-tw/') else 'en')
                yield loc, rel, p


def body_slice(html):
    s = html.find('id="article-content"')
    if s == -1:
        # newer template: <article class="article"> / <main role="main">
        for tag in ('<main role="main">', '<article class="article">'):
            j = html.find(tag)
            if j != -1:
                s = html.find('>', j) + 1
                break
    if s == -1:
        return ''
    e = html.find('class="toc-sidebar"', s)
    if e == -1:
        e = html.find('class="recommended-section"', s)
    if e == -1:
        e = html.find('</article>', s)
    return html[s:e if e != -1 else len(html)]


# ---------- the four checks ----------

def audit():
    """Single pass over all pages; returns metrics + per-file defect lists."""
    m = {
        'pages_total': 0, 'articles': 0,
        'toc_links': 0, 'toc_broken': 0, 'toc_pages_broken': 0,
        'toc_pages_all_dead': 0, 'generic_id_pages': 0, 'generic_id_links': 0,
        'cta_leak_links': 0, 'cta_leak_pages': 0,
        'rec_wrong_locale': 0, 'rec_dup_cards': 0, 'rec_dup_pages': 0,
        'rec_pages_empty': 0, 'rec_slug_titles': 0, 'rec_no_alt': 0,
        'body_images': 0, 'body_img_no_alt': 0, 'articles_zero_img': 0,
        'leak_root_links': 0, 'leak_root_pages': 0,
        'body_links': 0, 'body_link_targets': 0, 'orphans': 0,
    }
    fix = {'toc': [], 'cta': [], 'rec_locale': [], 'generic_id': []}
    targets = set()
    en_slugs = set()

    # ---- articles ----
    for loc, slug, p in iter_articles():
        html = read(p)
        if not html:
            continue
        m['articles'] += 1
        if loc == 'en':
            en_slugs.add(slug)
        rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
        ids = set(ID_RE.findall(html))
        body = body_slice(html)

        # C1 — TOC integrity
        tocs = re.findall(r'<nav class="toc-links">(.*?)</nav>', html, re.S)
        if tocs:
            anchors = []
            for t in tocs:
                anchors += ANCHOR_RE.findall(t)
            m['toc_links'] += len(anchors)
            broken = [a for a in anchors if a not in ids]
            if broken:
                m['toc_broken'] += len(broken)
                m['toc_pages_broken'] += 1
                fix['toc'].append({'file': rel, 'locale': loc,
                                   'broken': len(broken), 'total': len(anchors)})
                if len(broken) == len(anchors):
                    m['toc_pages_all_dead'] += 1

        h2ids = H2_RE.findall(html)
        if h2ids:
            gen = [i for i in h2ids if GEN_ID_RE.match(i)]
            if len(gen) > len(h2ids) / 2:
                m['generic_id_pages'] += 1
                m['generic_id_links'] += len(gen)
                fix['generic_id'].append({'file': rel, 'locale': loc,
                                          'count': len(gen)})

        # C2a — CTA language leak
        cta = CTA_RE.search(html)
        if cta:
            bad = []
            for h in HREF_RE.findall(cta.group(1)):
                if not h.startswith('/'):
                    continue
                if loc == 'en':
                    if h.startswith(('/zh-cn/', '/zh-tw/')):
                        bad.append(h)
                elif not h.startswith('/' + loc + '/'):
                    bad.append(h)
            if bad:
                m['cta_leak_pages'] += 1
                m['cta_leak_links'] += len(bad)
                fix['cta'].append({'file': rel, 'locale': loc, 'hrefs': bad})

        # C2b — recommended cards
        rb = REC_BLOCK_RE.search(html)
        if rb:
            cards = CARD_RE.findall(rb.group(1))
            if not cards:
                m['rec_pages_empty'] += 1
            seen = {}
            for href, inner in cards:
                mm = re.match(r'^/(zh-cn|zh-tw)?/?blog/articles/', href)
                if mm:
                    cl = mm.group(1) or 'en'
                    if cl != loc:
                        m['rec_wrong_locale'] += 1
                        fix['rec_locale'].append(
                            {'file': rel, 'page_locale': loc,
                             'card_locale': cl, 'href': href})
                seen[href] = seen.get(href, 0) + 1
                t = CARD_TITLE_RE.search(inner)
                if t:
                    txt = strip_tags(t.group(1))
                    if txt and ' ' in txt and txt == txt.title():
                        m['rec_slug_titles'] += 1
            dups = sum(v - 1 for v in seen.values() if v > 1)
            if dups:
                m['rec_dup_cards'] += dups
                m['rec_dup_pages'] += 1

        # C3 — internal links in body
        links = HREF_RE.findall(body)
        internal = [h for h in links
                    if h.startswith('/') or 'beehivestrategy.com' in h]
        m['body_links'] += len(internal)
        for h in internal:
            mm = re.search(r'/blog/articles/([a-z0-9\-]+)', h)
            if mm:
                targets.add(mm.group(1))

        # C4 — images in body
        imgs = IMG_RE.findall(body)
        m['body_images'] += len(imgs)
        if not imgs:
            m['articles_zero_img'] += 1

    m['body_link_targets'] = len(targets)
    m['orphans'] = len(en_slugs - targets)

    # ---- all pages: root-absolute links inside localized pages ----
    for loc, rel, p in iter_all_pages():
        m['pages_total'] += 1
        html = read(p)
        if not html or loc == 'en':
            continue
        # drop the language switcher (legitimately points at other locales)
        html_nc = SWITCHER_RE.sub('', html)
        bad = [h for h in HREF_RE.findall(html_nc)
               if h.startswith('/') and not h.startswith('/' + loc + '/')
               and not is_asset(h)]
        if bad:
            m['leak_root_pages'] += 1
            m['leak_root_links'] += len(bad)

    # ---- images with empty alt (all pages) ----
    for loc, rel, p in iter_all_pages():
        html = read(p)
        for tag in IMG_RE.findall(html):
            a = ALT_RE.search(tag)
            if not a or not a.group(1).strip():
                m['rec_no_alt'] += 1

    return m, fix


# ---------- gate logic ----------

# direction: 'lower' = fewer is better (a rise is a regression)
RULES = [
    ('toc_broken',          'TOC 死链总数',              'lower'),
    ('toc_pages_broken',    '含死链 TOC 的页面数',        'lower'),
    ('toc_pages_all_dead',  'TOC 全部失效的页面数',       'lower'),
    ('generic_id_pages',    '用 sec-N 占位 id 的页面数',  'lower'),
    ('cta_leak_pages',      'CTA 语言错误页面数',         'lower'),
    ('cta_leak_links',      'CTA 语言错误链接数',         'lower'),
    ('rec_wrong_locale',    '推荐卡语言错误数',           'lower'),
    ('rec_dup_cards',       '重复推荐卡数',               'lower'),
    ('rec_slug_titles',     'slug 直转标题数',            'lower'),
    ('leak_root_pages',     '含跨语言链接页面数',         'lower'),
    ('leak_root_links',     '跨语言链接总数',             'lower'),
    ('orphans',             '0 入链孤儿文章数',           'lower'),
    ('body_images',         '正文图片总数',               'higher'),
    ('body_link_targets',   '正文内链去重目标数',         'higher'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write-baseline', action='store_true')
    ap.add_argument('--emit-fixlist', action='store_true')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--no-gate', action='store_true',
                    help='report only, always exit 0')
    args = ap.parse_args()

    print('Scanning site ...', flush=True)
    m, fix = audit()

    os.makedirs(OUT_DIR, exist_ok=True)

    if args.emit_fixlist:
        fp = os.path.join(OUT_DIR, 'fix_list_2026-09-03.json')
        with open(fp, 'w', encoding='utf-8') as f:
            json.dump(fix, f, ensure_ascii=False, indent=2)
        print(f'  fix list -> {fp}')
        # human-readable per-category file lists
        for cat, items in fix.items():
            if not items:
                continue
            txt = os.path.join(OUT_DIR, f'fixlist_{cat}.txt')
            with open(txt, 'w', encoding='utf-8') as f:
                for it in items:
                    f.write(it['file'] + '\n')
            print(f'  {cat}: {len(items)} files -> {os.path.basename(txt)}')

    if args.write_baseline:
        with open(BASELINE, 'w', encoding='utf-8') as f:
            json.dump(m, f, ensure_ascii=False, indent=2)
        print(f'\nBASELINE written -> {BASELINE}')

    if args.json:
        print(json.dumps(m, ensure_ascii=False, indent=2))
        return 0

    base = None
    if os.path.exists(BASELINE):
        with open(BASELINE, encoding='utf-8') as f:
            base = json.load(f)

    print('\n' + '=' * 78)
    print('SITE AUDIT GATE — beehivestrategy.com')
    print('=' * 78)
    print(f"\npages={m['pages_total']}  articles={m['articles']}\n")
    hdr = f"{'metric':34} {'now':>9} {'baseline':>9} {'delta':>9}  status"
    print(hdr)
    print('-' * len(hdr))

    failures = []
    for key, label, direction in RULES:
        now = m[key]
        if base is None:
            b, d, st = '—', '—', 'no-baseline'
        else:
            b = base.get(key)
            if b is None:
                b, d, st = '—', '—', 'new'
            else:
                d = now - b
                if d == 0:
                    st = 'ok'
                elif direction == 'lower':
                    st = 'FAIL' if d > 0 else 'improved'
                else:
                    st = 'FAIL' if d < 0 else 'improved'
                if st == 'FAIL':
                    failures.append((label, b, now, d))
        print(f'{label:34} {now:9} {str(b):>9} '
              f'{(str(d) if d != "—" else "—"):>9}  {st}')

    print('\n--- headline numbers ---')
    print(f"  TOC 死链           : {m['toc_broken']}  "
          f"(占 {100.0*m['toc_broken']/max(1,m['toc_links']):.1f}% of {m['toc_links']})")
    print(f"  TOC 全死页面       : {m['toc_pages_all_dead']}")
    print(f"  CTA 语言错误       : {m['cta_leak_pages']} 页 / {m['cta_leak_links']} 链接")
    print(f"  推荐卡语言错误     : {m['rec_wrong_locale']}")
    print(f"  正文图片           : {m['body_images']}  "
          f"({m['articles_zero_img']} 篇文章 0 图)")
    print(f"  正文内链目标/孤儿  : {m['body_link_targets']} 目标 / "
          f"{m['orphans']} 孤儿")

    if base is None:
        print('\n⚠️  no baseline recorded — run with --write-baseline to enable gating')
        return 2

    if failures:
        print('\n❌ GATE FAIL — regressions detected:')
        for label, b, now, d in failures:
            print(f'   {label}: {b} -> {now} ({d:+d})')
        return 0 if args.no_gate else 1

    print('\n✅ GATE PASS — no regression vs baseline')
    return 0


if __name__ == '__main__':
    sys.exit(main())
