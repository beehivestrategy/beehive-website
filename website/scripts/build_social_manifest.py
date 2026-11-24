#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_social_manifest.py — extract per-locale article metadata for social cards.

Reads every published article page (EN / zh-CN / zh-HK) and writes
website/scripts/social_manifest.json with, per locale:

    slug, title, description, section, date, url, figure

The title/description come from the page's own <title> and meta description
(already localised), so a shared link shows the reader a card in their own
language. The figure points at the article's conceptual diagram, which the
social card reuses as its visual panel — so the shared card and the article
body show the same artwork.

Usage:
  python3 build_social_manifest.py            # write manifest
  python3 build_social_manifest.py --check    # report only, no write
"""
import html
import json
import re
import sys
from pathlib import Path

WEB = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "social_manifest.json"

# locale id -> (directory prefix, slug dir)
LOCALES = {
    "en": "",
    "zh-cn": "zh-cn/",
    "zh-hk": "zh-hk/",
}

RE_TITLE = re.compile(r"<title>([\s\S]*?)</title>", re.I)
RE_DESC = re.compile(
    r'<meta\s+name="description"\s+content="([^"]*)"', re.I)
RE_SECTION = re.compile(r'"articleSection"\s*:\s*"([^"]*)"')
RE_DATE = re.compile(r'"datePublished"\s*:\s*"([^"]*)"')
RE_CANON = re.compile(r'<link\s+rel="canonical"\s+href="([^"]*)"', re.I)
RE_FIG = re.compile(r'/assets/blog/svg/([^"\' )]+?)\.svg')
RE_ARTICLE = re.compile(r'<article\b[^>]*class="[^"]*article-content[^"]*"',
                         re.I)

BRAND_SUFFIX = re.compile(r"\s*[|｜]\s*Beehive Strategy\s*$", re.I)


def clean(t):
    """Unescape HTML entities once (manifest holds plain text)."""
    return html.unescape(t).strip()


def strip_brand(t):
    return BRAND_SUFFIX.sub("", t).strip()


def pick_section(s, fallback=""):
    m = RE_SECTION.search(s)
    if m:
        return clean(m.group(1))
    m = RE_SECTION.search(fallback)
    return clean(m.group(1)) if m else ""


def main():
    check = "--check" in sys.argv
    manifest = {}

    for loc, prefix in LOCALES.items():
        art_dir = WEB / prefix / "blog" / "articles"
        if not art_dir.is_dir():
            print("skip (missing dir):", art_dir)
            continue
        entries = {}
        for p in sorted(art_dir.glob("*.html")):
            slug = p.stem
            s = p.read_text(encoding="utf-8", errors="ignore")

            tm = RE_TITLE.search(s)
            if not tm:
                continue
            title = strip_brand(clean(tm.group(1)))
            if not title:
                continue

            dm = RE_DESC.search(s)
            desc = clean(dm.group(1)) if dm else ""

            cm = RE_CANON.search(s)
            url = cm.group(1).strip() if cm else \
                "https://www.beehivestrategy.com/" + (
                    prefix + "blog/articles/" + slug).replace("//", "/")

            dt = RE_DATE.search(s)
            date = dt.group(1)[:10] if dt else ""

            # the conceptual diagram that belongs to this article
            fm = RE_FIG.search(s)
            figure = fm.group(1) if fm else slug

            entries[slug] = {
                "slug": slug,
                "title": title,
                "description": desc,
                "section": pick_section(s),
                "date": date,
                "url": url,
                "figure": figure,
            }
        manifest[loc] = entries
        print(f"{loc}: {len(entries)} articles")

    if check:
        for loc in LOCALES:
            e = manifest.get(loc, {})
            miss = sum(1 for v in e.values() if not v["title"])
            print(f"  {loc}: {len(e)} entries, {miss} without title")
        return

    OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=0),
                   encoding="utf-8")
    print("wrote", OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
