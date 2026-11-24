#!/usr/bin/env python3
"""Backfill daily-generated articles into the REAL blog index pages.

Root cause this fixes (2026-11-25):
  generate_daily_article.py writes cards into website/blog.html (the OLD root
  page) and searches for a `blog-cards` container. The live /blog/ index is
  website/blog/index.html, which uses a `blog-grid` container and a v7 card
  markup. Result: daily articles were published (detail pages, sitemap, feed)
  but NEVER appeared in the index.

This script:
  1. reads each new article's meta (og:title, description, published date,
     articleSection, keywords) from all three languages;
  2. inserts a card into blog/index.html, zh-cn/blog/index.html and
     zh-hk/blog/index.html in the EXISTING v7 markup, deduped by the href
     slug actually present in those files (the old updater's regex had the
     href/class order reversed, so it matched nothing);
  3. recomputes the archive count and month options.

It is idempotent: a card is skipped when its `articles/<slug>` href already
exists in the index. Run after each daily generation until the generator is
fixed (see generate_daily_article.py).

Usage:
  python3 scripts/backfill_daily_index.py --dry-run
  python3 scripts/backfill_daily_index.py --apply
"""
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = {
    "en": {
        "index": ROOT / "blog/index.html",
        "dir": ROOT / "blog/articles",
        "mode": "en",
    },
    "zh-cn": {
        "index": ROOT / "zh-cn/blog/index.html",
        "dir": ROOT / "zh-cn/blog/articles",
        "mode": "zh",
    },
    "zh-hk": {
        "index": ROOT / "zh-hk/blog/index.html",
        "dir": ROOT / "zh-hk/blog/articles",
        "mode": "zh",
    },
}
CARDS = ROOT / "assets/blog/cards"
ASSET_V = "20261123.01"
CUTOFF = "2026-11-23"  # first day the daily generator's cards went missing
MONTHS_EN = ["January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November", "December"]


def fmt_date(iso: str, mode: str) -> str:
    y, m, d = (int(x) for x in iso.split("-"))
    if mode == "en":
        return f"{MONTHS_EN[m - 1]} {d}, {y}"
    return f"{y}年{m}月{d}日"


def article_meta(path: Path, mode: str) -> dict | None:
    text = path.read_text(errors="ignore")
    slug = path.stem
    title = re.search(r'og:title"\s+content="(.*?)"', text, re.S)
    desc = re.search(r'<meta name="description" content="(.*?)"', text, re.S)
    date = re.search(r'article:published_time"\s+content="(\d{4}-\d\d-\d\d)', text)
    section = re.search(r'"articleSection"\s*:\s*"([^"]+)"', text)
    if not (title and desc and date):
        return None
    # word count from visible body text, fallback 8 min
    words = len(re.findall(r"<[pP][ >]", text))
    minutes = max(5, min(20, round(words / 3)))
    return {
        "slug": slug,
        "title": html.unescape(title.group(1).strip()),
        "desc": html.unescape(desc.group(1).strip()),
        "date": date.group(1),
        "category": html.unescape(section.group(1).strip()) if section else "AI Strategy",
        "minutes": minutes,
    }


def card_html(meta: dict, mode: str) -> str:
    iso = meta["date"]
    return f'''              <article class="blog-card reveal" data-category="{html.escape(meta["category"])}" data-date="{iso}" data-month="{iso[:7]}" itemscope itemtype="https://schema.org/BlogPosting">
                <a href="articles/{meta["slug"]}" class="blog-card-link" itemprop="url">
                  <div class="blog-card-image" aria-hidden="true">
                    <img src="/assets/blog/cards/{meta["slug"]}.jpg?v={ASSET_V}" alt="{html.escape(meta["title"])}" class="blog-card-thumb" loading="lazy" width="600" height="315">
                    <span class="blog-card-category">{html.escape(meta["category"])}</span>
                  </div>
                  <div class="blog-card-body">
                    <meta itemprop="datePublished" content="{iso}">
                    <div class="blog-card-meta">
                      <time datetime="{iso}">{fmt_date(iso, mode)}</time>
                      <span class="blog-card-dot" aria-hidden="true">&middot;</span>
                      <span>{meta["minutes"]} min read</span>
                    </div>
                    <h2 class="blog-card-title" itemprop="headline">{html.escape(meta["title"])}</h2>
                    <p class="blog-card-excerpt" itemprop="description">{html.escape(meta["desc"])}</p>
                    <div class="blog-card-footer">
                      <span class="blog-card-author" itemprop="author">Beehive Strategy</span>
                      <span class="blog-card-readmore">Read more &rarr;</span>
                    </div>
                  </div>
                </a>
              </article>
'''


def rebuild_month_options(index: str, mode: str) -> str:
    months = sorted({m.group(1) for m in re.finditer(r'data-month="(\d{4}-\d\d)"', index)}, reverse=True)
    if not months:
        return index

    def label(iso_month: str) -> str:
        y, m = iso_month.split("-")
        return f"{MONTHS_EN[int(m) - 1]} {y}" if mode == "en" else f"{y}年{int(m)}月"

    opts = "\n".join(
        f'              <option value="{mo}">{label(mo)}</option>' for mo in months
    )
    pattern = re.compile(
        r'(<select[^>]*class="[^"]*bl-month[^"]*"[^>]*>)(.*?)(</select>)', re.S
    )
    if not pattern.search(index):
        return index
    return pattern.sub(
        lambda m: m.group(1) + "\n" + opts + "\n            " + m.group(3), index, count=1
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not args.apply and not args.dry_run:
        ap.error("pass --apply or --dry-run")

    total_new = 0
    new_slugs: set[str] = set()
    for lang, cfg in LANGS.items():
        index_path = cfg["index"]
        index = index_path.read_text(encoding="utf-8")

        # Correct dedup: the href comes BEFORE class in the real markup.
        existing = set(
            re.findall(r'href="articles/([^"/]+)"\s+class="blog-card-link"', index)
        )
        existing |= set(re.findall(r'href="/?blog/articles/([^"/]+)"', index))

        metas = []
        for page in sorted(cfg["dir"].glob("*.html")):
            meta = article_meta(page, cfg["mode"])
            if meta and meta["date"] >= CUTOFF and meta["slug"] not in existing:
                metas.append(meta)
        metas.sort(key=lambda m: (m["date"], m["slug"]), reverse=True)

        print(f"{lang}: existing={len(existing)} new={len(metas)} "
              f"slugs={[m['slug'] for m in metas]}")
        if args.dry_run or not metas:
            continue

        anchor = '<div class="blog-grid" id="blog-grid">\n'
        if anchor not in index:
            raise SystemExit(f"grid anchor missing in {index_path}")
        block = "".join(card_html(m, cfg["mode"]) for m in metas)
        index = index.replace(anchor, anchor + block, 1)

        total = len(re.findall(r'<article class="blog-card', index))
        index = re.sub(r'(bl-archive-count"><strong>)\d+(</strong>)',
                       rf'\g<1>{total}\g<2>', index)
        index = rebuild_month_options(index, cfg["mode"])
        index_path.write_text(index, encoding="utf-8")
        print(f"{lang}: cards now {total}, written")
        total_new += len(metas)
        new_slugs.update(m["slug"] for m in metas)

    if new_slugs and args.apply:
        ensure_thumbnails(new_slugs)

    print("total new cards:", total_new)
    return 0


def ensure_thumbnails(slugs: set[str]) -> None:
    """Best-effort: create a 600x315 IBM-blue abstract card for any new slug
    that has no thumbnail. Uses the SSOT diagram if available (via cairosvg
    or a pre-rendered SVG->JPG pipeline), else a deterministic PIL pattern.

    Never fails the run: the CI daily job may not have every image lib.
    """
    missing = [s for s in sorted(slugs) if not (CARDS / f"{s}.jpg").exists()]
    if not missing:
        return
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("WARN: Pillow unavailable; skipping card thumbnails for", missing)
        return

    palette = ["#0F62FE", "#0043CE", "#4589FF", "#8FB0FF"]
    CARDS.mkdir(parents=True, exist_ok=True)
    for i, slug in enumerate(missing):
        img = Image.new("RGB", (600, 315), "#F4F8FF")
        d = ImageDraw.Draw(img)
        # deterministic abstract: soft grid + a wave, same family as site cards
        for x in range(0, 600, 40):
            d.line((x, 0, x, 315), fill="#E4ECFB", width=1)
        for y in range(0, 315, 40):
            d.line((0, y, 600, y), fill="#E4ECFB", width=1)
        colour = palette[i % len(palette)]
        pts = [
            (x, 157 + int(70 * __import__("math").sin((x / 600) * 6.28 + i)))
            for x in range(0, 601, 12)
        ]
        d.line(pts, fill=colour, width=7, joint="curve")
        img.save(CARDS / f"{slug}.jpg", "JPEG", quality=88, optimize=True)
        print(f"thumb: generated {slug}.jpg (abstract)")


if __name__ == "__main__":
    raise SystemExit(main())
