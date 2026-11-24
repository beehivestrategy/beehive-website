#!/usr/bin/env python3
"""Render 1200x630 social cards for rebuilt articles with Pillow.

The approved card carries the article title, its summary, a visual derived from
the article's own workflow, and the Beehive Strategy footer. This renderer
reads those from the generated page so the card always matches the article.

Usage: python3 scripts/render_cards_pil.py [--from 20260918] [--only-missing]
"""
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
LANG_DIRS = {
    "en": ROOT / "blog/articles",
    "zh-cn": ROOT / "zh-cn/blog/articles",
    "zh-hk": ROOT / "zh-hk/blog/articles",
}
OUT_DIRS = {k: ROOT / f"assets/blog/social/{k}" for k in LANG_DIRS}
W, H = 1200, 630
BLUE, DEEP, INK, MUTED, WASH = "#0F62FE", "#0043CE", "#101828", "#5A6478", "#F4F8FF"

FONT_CANDIDATES = [
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
]
LATIN = "/System/Library/Fonts/Helvetica.ttc"


def load_font(size: int, cjk: bool) -> ImageFont.FreeTypeFont:
    path = (FONT_CANDIDATES[0] if cjk else LATIN)
    try:
        return ImageFont.truetype(path, size, index=0)
    except OSError:
        return ImageFont.truetype(FONT_CANDIDATES[-1], size)


def wrap(draw, text: str, font, max_width: int, max_lines: int) -> list[str]:
    """Wrap by words for Latin text and by characters for CJK."""
    cjk = bool(re.search(r"[\u4e00-\u9fff]", text))
    units = list(text) if cjk else text.split()
    joiner = "" if cjk else " "
    lines, current = [], ""
    for unit in units:
        probe = f"{current}{joiner}{unit}" if current else unit
        if draw.textlength(probe, font=font) <= max_width:
            current = probe
        else:
            if current:
                lines.append(current)
            current = unit
            if len(lines) == max_lines - 1:
                break
    if current:
        lines.append(current)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
    return lines


def extract(page: Path) -> dict:
    text = page.read_text(errors="ignore")
    title = re.search(r'<h1 class="ar-title">(.*?)</h1>', text, re.S)
    desc = re.search(r'<meta name="description" content="(.*?)"', text, re.S)
    steps = re.findall(r'<div class="ar-flow-step"><b>[^<]*</b><strong>(.*?)</strong>', text, re.S)[:5]
    kicker = re.search(r'<span class="ar-kicker">(.*?)</span>', text, re.S)
    return {
        "title": html.unescape(title.group(1)).strip() if title else page.stem,
        "desc": html.unescape(desc.group(1)).strip() if desc else "",
        "steps": [html.unescape(s).strip() for s in steps],
        "kicker": html.unescape(kicker.group(1)).strip() if kicker else "Beehive Strategy",
    }


def render(meta: dict, out: Path) -> None:
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    cjk = bool(re.search(r"[\u4e00-\u9fff]", meta["title"]))
    f_kick = load_font(22, cjk)
    f_title = load_font(56, cjk)
    f_desc = load_font(26, cjk)
    f_step = load_font(21, cjk)
    f_brand = load_font(24, cjk)

    # brand bar
    d.rectangle([0, 0, W, 10], fill=BLUE)
    d.text((64, 46), "BEEHIVE STRATEGY", font=f_kick, fill=BLUE)

    # title and summary
    y = 104
    for line in wrap(d, meta["title"], f_title, W - 128, 3):
        d.text((64, y), line, font=f_title, fill=INK)
        y += 68
    y += 12
    for line in wrap(d, meta["desc"], f_desc, W - 128, 3):
        d.text((64, y), line, font=f_desc, fill=MUTED)
        y += 36

    # workflow strip derived from the article
    steps = meta["steps"] or []
    if steps:
        top = 470
        cols = len(steps)
        gap = 16
        box_w = (W - 128 - gap * (cols - 1)) / cols
        for i, label in enumerate(steps):
            x = 64 + i * (box_w + gap)
            d.rounded_rectangle([x, top, x + box_w, top + 84], radius=10, fill=WASH, outline="#D6E2FF")
            d.text((x + 14, top + 12), f"{i + 1:02d}", font=f_step, fill=BLUE)
            for j, line in enumerate(wrap(d, label, f_step, int(box_w) - 28, 2)):
                d.text((x + 14, top + 36 + j * 24), line, font=f_step, fill=INK)

    d.line([64, H - 54, W - 64, H - 54], fill="#E3EAF9", width=1)
    d.text((64, H - 40), "beehivestrategy.com", font=f_brand, fill=DEEP)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "JPEG", quality=82, optimize=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", default="20260918")
    ap.add_argument("--only-missing", action="store_true")
    args = ap.parse_args()
    total = 0
    for lang, folder in LANG_DIRS.items():
        for page in sorted(folder.glob("*.html")):
            suffix = page.stem[-8:]
            if not (suffix.isdigit() and suffix >= args.start):
                continue
            out = OUT_DIRS[lang] / f"{page.stem}.jpg"
            if args.only_missing and out.exists():
                continue
            render(extract(page), out)
            total += 1
        print(lang, "done")
    print("cards:", total)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
