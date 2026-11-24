#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_article_upgrade.py — roll the v6 article experience onto every
published article, in all three languages.

What it does, per article page:

 1. DIAGRAM — the abstract decorative hero is replaced by a diagram derived
    from the article's own content (bar chart / comparison matrix / workflow
    / capability layers / concept map), rendered per locale so the labels are
    in the reader's language. The old generic SVG stays as the fallback for
    articles whose body yields no diagram.

 2. AUTHOR — the byline and JSON-LD author are set to the company
    (Beehive Strategy), not an individual.

 3. SHARE — the sidebar share row is rebuilt with LinkedIn, X, WhatsApp,
    Facebook and Copy link, and the page gains whatever script it was
    missing so the buttons actually work.

 4. SOCIAL CARD — og:image / twitter:image now point at a dedicated
    1200x630 card with the headline baked in, so a link shared into
    Facebook, X, LinkedIn or WhatsApp shows the article title instead of an
    abstract shape.

The patch is idempotent: re-running it changes nothing.

Usage:
  python3 apply_article_upgrade.py --check
  python3 apply_article_upgrade.py --apply
  python3 apply_article_upgrade.py --apply --sample 20
"""
import html
import json
import re
import sys
from pathlib import Path

WEB = Path(__file__).resolve().parents[1]
ROOT = WEB.parent

LOCALES = {"en": "", "zh-cn": "zh-cn/", "zh-hk": "zh-hk/"}

RE_MAIN = re.search
RE_OG_IMG = re.compile(
    r'<meta\s+property="og:image"\s+content="([^"]*)"[^>]*>')
RE_TW_IMG = re.compile(
    r'<meta\s+name="twitter:image"\s+content="([^"]*)"[^>]*>')
RE_OG_TITLE = re.compile(r'<meta\s+property="og:title"\s+content="([^"]*)"[^>]*>')
RE_TW_TITLE = re.compile(r'<meta\s+name="twitter:title"\s+content="([^"]*)"[^>]*>')
RE_OG_DESC = re.compile(
    r'<meta\s+property="og:description"\s+content="([^"]*)"[^>]*>')
RE_TW_DESC = re.compile(
    r'<meta\s+name="twitter:description"\s+content="([^"]*)"[^>]*>')
RE_OG_URL = re.compile(r'<meta\s+property="og:url"\s+content="([^"]*)"[^>]*>')
RE_CANON = re.compile(r'<link\s+rel="canonical"\s+href="([^"]*)"[^>]*>')
RE_TITLE = re.compile(r"<title>([\s\S]*?)</title>", re.I)
RE_SECTION = re.compile(r'"articleSection"\s*:\s*"([^"]*)"')
RE_AUTHOR_JSONLD = re.compile(
    r'"author"\s*:\s*\{[^}]*\}', re.S)
RE_ARTICLE_TAG = re.compile(
    r'<article\b[^>]*class="article-content"[^>]*>', re.I)
RE_FIGURE = re.compile(
    r'<figure class="article-figure"[\s\S]*?</figure>', re.I)
RE_HERO_FIGURE = re.compile(
    r'<figure class="article-hero"[\s\S]*?</figure>', re.I)
RE_SIDE_SHARE = re.compile(
    r'<div class="sidebar-share">[\s\S]*?</div>\s*</div>', re.I)
RE_SHARE_BTN_BLOCK = re.compile(
    r'<div class="sidebar-share">[\s\S]*?(?=<div class="sidebar-card">|</aside>)',
    re.I)
RE_SCRIPT_SRC = re.compile(r'<script src="(/js/[^"]+)"')

ICONS = {
    "linkedin": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-4 0v7h-4v-7a6 6 0 016-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>',
    "x": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4l11.733 16h4.267l-11.733-16zM4 20l6.768-6.768M13.232 10.768L20 4"/></svg>',
    "whatsapp": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.4 8.4 0 01-12.6 7.3L3 20.5l1.8-5.2A8.4 8.4 0 1121 11.5z"/><path d="M8.5 9.5c0 3 2.5 5.5 5.5 5.5"/></svg>',
    "facebook": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 8h3V4h-3a4 4 0 00-4 4v2H7v4h3v6h4v-6h3l1-4h-4V9a1 1 0 011-1z"/></svg>',
    "copy": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a1 1 0 01-1-1V4a1 1 0 011-1h10a1 1 0 011 1v1"/></svg>',
}

LABELS = {
    "en": {"linkedin": "Share on LinkedIn", "x": "Share on X",
           "whatsapp": "Share on WhatsApp", "facebook": "Share on Facebook",
           "copy": "Copy link", "heading": "Share this article",
           "copied": "Link copied to clipboard!"},
    "zh-cn": {"linkedin": "分享到领英", "x": "分享到 X",
              "whatsapp": "分享到 WhatsApp", "facebook": "分享到 Facebook",
              "copy": "复制链接", "heading": "分享这篇文章",
              "copied": "链接已复制"},
    "zh-hk": {"linkedin": "分享到領英", "x": "分享到 X",
              "whatsapp": "分享到 WhatsApp", "facebook": "分享到 Facebook",
              "copy": "複製連結", "heading": "分享這篇文章",
              "copied": "連結已複製"},
}


def social_url(locale, slug):
    prefix = "" if locale == "en" else ("/zh-cn/" if locale == "zh-cn"
                                         else "/zh-hk/")
    return ("https://www.beehivestrategy.com/assets/blog/social/" + locale +
            "/" + slug + ".jpg?v=20261121.01")


def canonical_url(locale, slug):
    prefix = {"en": "", "zh-cn": "/zh-cn", "zh-hk": "/zh-hk"}[locale]
    return "https://www.beehivestrategy.com" + prefix + "/blog/articles/" + slug


def build_share_block(locale):
    L = LABELS[locale]
    btns = []
    for key in ("linkedin", "x", "whatsapp", "facebook", "copy"):
        extra = ''
        if key == "copy":
            extra = ' data-copy-msg="%s"' % L["copied"]
        btns.append(
            '<button class="article-share-btn" id="share-%s" '
            'aria-label="%s" title="%s"%s>%s</button>'
            % (key, L[key], L[key], extra, ICONS[key]))
    return ('<div class="sidebar-share">' + "".join(btns) + "</div>")


def patch_social_meta(s, locale, slug):
    """Point og/twitter at the dedicated share card; keep title/desc in sync."""
    img = social_url(locale, slug)
    canon = canonical_url(locale, slug)

    tm = RE_TITLE.search(s)
    title = html.unescape(tm.group(1)).strip() if tm else ""
    title = re.sub(r"\s*[|｜]\s*Beehive Strategy\s*$", "", title).strip()

    dm = RE_OG_DESC.search(s) or RE_TW_DESC.search(s)
    desc = html.unescape(dm.group(1)).strip() if dm else ""

    # og:image / twitter:image -> share card
    if RE_OG_IMG.search(s):
        s = RE_OG_IMG.sub(
            lambda m: '<meta property="og:image" content="%s">' % img, s)
    else:
        anchor = RE_OG_URL.search(s) or RE_CANON.search(s)
        block = ('<meta property="og:image" content="%s">'
                 '<meta property="og:image:width" content="1200">'
                 '<meta property="og:image:height" content="630">'
                 '<meta property="og:image:alt" content="%s">'
                 % (img, html.escape(title, quote=True)))
        if anchor:
            s = s[:anchor.end()] + block + s[anchor.end():]
        else:
            head_end = s.find("</head>")
            s = s[:head_end] + block + s[head_end:]

    if RE_TW_IMG.search(s):
        s = RE_TW_IMG.sub(
            lambda m: '<meta name="twitter:image" content="%s">' % img, s)
    else:
        s = s.replace(
            '<meta name="twitter:image" content="%s">' % img,
            '<meta name="twitter:image" content="%s">' % img)
        if "twitter:image" not in s:
            s = s.replace(
                '<meta property="og:image" content="%s">' % img,
                '<meta property="og:image" content="%s">'
                '<meta name="twitter:image" content="%s">' % (img, img), 1)

    # title / description / url
    if title:
        if RE_OG_TITLE.search(s):
            s = RE_OG_TITLE.sub(
                lambda m: '<meta property="og:title" content="%s">'
                % html.escape(title, quote=True), s)
        if RE_TW_TITLE.search(s):
            s = RE_TW_TITLE.sub(
                lambda m: '<meta name="twitter:title" content="%s">'
                % html.escape(title, quote=True), s)
    if desc:
        if RE_OG_DESC.search(s):
            s = RE_OG_DESC.sub(
                lambda m: '<meta property="og:description" content="%s">'
                % html.escape(desc, quote=True), s)
        if RE_TW_DESC.search(s):
            s = RE_TW_DESC.sub(
                lambda m: '<meta name="twitter:description" content="%s">'
                % html.escape(desc, quote=True), s)
    if RE_OG_URL.search(s):
        s = RE_OG_URL.sub(
            lambda m: '<meta property="og:url" content="%s">' % canon, s)
    return s


def patch_author(s, locale):
    """Byline + JSON-LD author = the company."""
    # JSON-LD: replace a Person author with the Organization
    def repl(m):
        return ('"author": {"@type": "Organization", "name": "Beehive Strategy", '
                '"url": "https://www.beehivestrategy.com"}')
    if RE_AUTHOR_JSONLD.search(s):
        s = RE_AUTHOR_JSONLD.sub(repl, s)
    else:
        # no author key at all -> add one next to publisher
        s = s.replace('"publisher": {',
                      '"author": {"@type": "Organization", "name": "Beehive Strategy", '
                      '"url": "https://www.beehivestrategy.com"},\n    "publisher": {',
                      1)
    # visible byline: replace any individual name with the company
    s = re.sub(r'(class="article-meta-text"[^>]*>)([\s\S]{0,240}?)(</div>)',
               lambda m: m.group(1) + re.sub(
                   r'Kenneth Kwok|郭家威|創辦人[^·]*|创办人[^·]*',
                   'Beehive Strategy', m.group(2)) + m.group(3), s)
    return s


def patch_share(s, locale, insert_card):
    """Rebuild the share row and make sure the share script is present.

    `insert_card` decides whether a NEW sidebar card is added. It MUST be
    the same decision for all three languages, otherwise the <main>
    structure signature diverges and the trilingual gate fails. The caller
    therefore decides it once from the English page.
    """
    block = build_share_block(locale)
    if RE_SHARE_BTN_BLOCK.search(s):
        s = RE_SHARE_BTN_BLOCK.sub(block, s, count=1)
    elif insert_card:
        # no sidebar share row: add one at the end of the sidebar
        if "</aside>" in s:
            s = s.replace("</aside>",
                          '<div class="sidebar-card"><div class="sidebar-heading">'
                          '%s</div>%s</div></aside>'
                          % (LABELS[locale]["heading"], block), 1)
    # ensure article.js is loaded so the buttons work
    if "/js/article.js" not in s:
        m = RE_SCRIPT_SRC.search(s)
        if m:
            s = s[:m.start()] + '<script src="/js/article.js?v=20261121.01"></script>' + s[m.start():]
    return s


def patch_diagram(s, locale, slug):
    """Swap the generic SVG for the content-derived, per-locale diagram."""
    if not (WEB / ("assets/blog/svg/%s/%s.svg" % (locale, slug))).exists():
        return s
    new_ref = "/assets/blog/svg/%s/%s.svg?v=20261121.01" % (locale, slug)
    # point every existing figure/hero at the new diagram
    s = re.sub(r'/assets/blog/svg/(?:[a-z-]+/)?[^"\'\s>]+?\.svg(?:\?v=[^"\'\s>]*)?',
               new_ref, s)
    return s


def process(path, locale, slug, apply_, insert_card=None):
    s = path.read_text(encoding="utf-8", errors="ignore")
    orig = s
    s = patch_diagram(s, locale, slug)
    s = patch_author(s, locale)
    s = patch_share(s, locale,
                    insert_card if insert_card is not None
                    else not RE_SHARE_BTN_BLOCK.search(s))
    s = patch_social_meta(s, locale, slug)
    changed = s != orig
    if changed and apply_:
        path.write_text(s, encoding="utf-8")
    return changed


def main():
    argv = sys.argv[1:]
    apply_ = "--apply" in argv
    sample = None
    if "--sample" in argv:
        sample = int(argv[argv.index("--sample") + 1])

    # Process article-by-article across all three languages together, so the
    # <main> structure signature stays identical in every locale (Gate 10).
    en_dir = WEB / "blog" / "articles"
    slugs = sorted(p.stem for p in en_dir.glob("*.html"))
    if sample:
        slugs = slugs[:sample]

    total = 0
    changed = 0
    per_locale = {loc: 0 for loc in LOCALES}
    for slug in slugs:
        # One decision for the whole article: does the English page already
        # carry a share row? If not, all three locales get the same new card.
        en_path = WEB / "blog" / "articles" / (slug + ".html")
        en_src = en_path.read_text(encoding="utf-8", errors="ignore")
        insert_card = not RE_SHARE_BTN_BLOCK.search(en_src)

        for locale, prefix in LOCALES.items():
            p = WEB / prefix / "blog" / "articles" / (slug + ".html")
            if not p.exists():
                continue
            if process(p, locale, slug, apply_, insert_card):
                per_locale[locale] += 1
                changed += 1
            total += 1
    for loc, n in per_locale.items():
        print("%s: %d pages updated" % (loc, n))
    print("total changed:", changed, "of", total)
    if not apply_:
        print("(dry run — nothing written)")


if __name__ == "__main__":
    main()
