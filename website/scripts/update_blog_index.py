#!/usr/bin/env python3
"""Add the rebuilt 2026-09-18 window to the three blog index pages.

Keeps the approved v7 layout untouched: the script only inserts article cards
into the existing grid, updates the archive count, adds any missing month option
and writes the 600x315 thumbnails the cards expect.

Idempotent: a card is skipped when its href is already present.

Usage: python3 scripts/update_blog_index.py [--from 20260918] [--dry-run]
"""
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
LANGS = {
    "en": {"index": ROOT / "blog/index.html", "dir": ROOT / "blog/articles", "href": "articles/",
           "date_fmt": "en"},
    "zh-cn": {"index": ROOT / "zh-cn/blog/index.html", "dir": ROOT / "zh-cn/blog/articles",
              "href": "articles/", "date_fmt": "zh"},
    "zh-hk": {"index": ROOT / "zh-hk/blog/index.html", "dir": ROOT / "zh-hk/blog/articles",
              "href": "articles/", "date_fmt": "zh"},
}
SOCIAL = {k: ROOT / f"assets/blog/social/{k}" for k in LANGS}
CARDS = ROOT / "assets/blog/cards"
ASSET_V = "20261123.01"

# The filter buttons use the existing taxonomy; map the rebuilt categories onto it.
CATEGORY_MAP = {
    "Strategy": "Strategy",
    "Data": "Data Strategy",
    "Governance": "AI Governance",
    "Delivery": "Professional Services",
    "Industry": "Industry",
}

MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December"]


def fmt_date(iso: str, mode: str) -> str:
    y, m, d = (int(x) for x in iso.split("-"))
    if mode == "en":
        return f"{MONTHS_EN[m - 1]} {d}, {y}"
    return f"{y}年{m}月{d}日"


def article_meta(path: Path, mode: str) -> dict:
    text = path.read_text(errors="ignore")
    title = re.search(r'<h1 class="ar-title">(.*?)</h1>', text, re.S)
    desc = re.search(r'<meta name="description" content="(.*?)"', text, re.S)
    date = re.search(r'article:published_time"\s+content="(\d{4}-\d\d-\d\d)', text)
    kicker = re.search(r'<span class="ar-kicker">(.*?)</span>', text, re.S)
    eyebrow = re.search(r'<nav class="ar-eyebrow".*?</nav>', text, re.S)
    label = ""
    if eyebrow:
        parts = re.findall(r"<span[^>]*>(.*?)</span>", eyebrow.group(), re.S)
        label = html.unescape(parts[-1]).strip() if parts else ""
    body = re.search(r'<article class="ar-body".*?</article>', text, re.S)
    plain = re.sub(r"<[^>]+>", " ", body.group()) if body else ""
    if mode == "en":
        words = len(re.findall(r"[A-Za-z0-9]+(?:[’'\-][A-Za-z0-9]+)*", plain))
        minutes = max(3, round(words / 220))
    else:
        chars = len(re.findall(r"[\u4e00-\u9fff]", plain))
        minutes = max(3, round(chars / 400))
    return {
        "slug": path.stem,
        "title": html.unescape(title.group(1)).strip() if title else path.stem,
        "desc": html.unescape(desc.group(1)).strip() if desc else "",
        "date": date.group(1) if date else "2026-09-18",
        "category": CATEGORY_MAP.get(
            label or (html.unescape(kicker.group(1)).split("·")[0].strip() if kicker else ""),
            "Strategy"),
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


def thumb(slug: str, lang: str) -> bool:
    src = SOCIAL[lang] / f"{slug}.jpg"
    if not src.exists():
        return False
    out = CARDS / f"{slug}.jpg"
    if out.exists():
        return True
    CARDS.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as img:
        img.resize((600, 315), Image.LANCZOS).save(out, "JPEG", quality=84, optimize=True)
    return True



def rebuild_month_options(index: str, mode: str) -> str:
    """Recompute every month option label from the cards that actually exist."""
    from collections import Counter
    counts = Counter(re.findall(r'data-month="(\d{4}-\d{2})"', index))
    select = re.search(r'(<select[^>]*blog-month-filter[^>]*>)(.*?)(</select>)', index, re.S)
    if not select:
        return index
    all_label = "All months" if mode == "en" else "全部月份"
    options = [f'<option value="all">{all_label}</option>']
    for month in sorted(counts, reverse=True):
        y, m = month.split("-")
        label = f"{MONTHS_EN[int(m) - 1]} {y}" if mode == "en" else f"{y}年{int(m)}月"
        options.append(f'<option value="{month}">{label} ({counts[month]})</option>')
    body = "\n                ".join(options)
    return index[:select.start(2)] + "\n                " + body + "\n              " + index[select.start(3):]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", default="20260918")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    for lang, cfg in LANGS.items():
        mode = cfg["date_fmt"]
        metas = []
        for page in cfg["dir"].glob("*.html"):
            text = page.read_text(errors="ignore")
            m = re.search(r'article:published_time"\s+content="(\d{4}-\d\d-\d\d)', text)
            if m and m.group(1) >= "2026-09-18":
                metas.append(article_meta(page, mode))
        metas.sort(key=lambda m: (m["date"], m["slug"]), reverse=True)

        index = cfg["index"].read_text()
        existing = set(re.findall(r'class="blog-card-link"[^>]*href="[^"]*?([^"/]+)"', index))
        new = [m for m in metas if m["slug"] not in existing]

        missing_thumb = [m["slug"] for m in new if not (CARDS / f"{m['slug']}.jpg").exists()]
        print(f"{lang}: window={len(metas)} new_cards={len(new)} thumbs_to_build={len(missing_thumb)}")
        if args.dry_run:
            continue

        for m in new:
            thumb(m["slug"], lang)

        if new:
            block = "".join(card_html(m, mode) for m in new)
            anchor = '<div class="blog-grid" id="blog-grid">\n'
            if anchor not in index:
                raise SystemExit(f"grid anchor missing in {cfg['index']}")
            index = index.replace(anchor, anchor + block, 1)

        total = len(re.findall(r'<article class="blog-card', index))
        index = re.sub(r'(bl-archive-count"><strong>)\d+(</strong>)', rf'\g<1>{total}\g<2>', index)

        index = rebuild_month_options(index, mode)
        cfg["index"].write_text(index)
        print(f"{lang}: cards now {total}, index written")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
