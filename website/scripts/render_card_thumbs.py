#!/usr/bin/env python3
"""Render index card thumbnails from the article's own process diagram.

The article pages and the social cards show a five-step process diagram derived
from the article. Legacy index cards instead used abstract pattern art. This
renderer reproduces that same diagram at 600x315 so the index matches the
article a reader lands on.

Usage:
  python3 scripts/render_card_thumbs.py --from 20260918            # rebuilt window
  python3 scripts/render_card_thumbs.py --all                      # every article
  python3 scripts/render_card_thumbs.py --sample <slug> --out /tmp/x.jpg
"""
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
LANGS = {"en": ROOT / "blog/articles", "zh-cn": ROOT / "zh-cn/blog/articles",
         "zh-hk": ROOT / "zh-hk/blog/articles"}
CARDS = ROOT / "assets/blog/cards"
W, H = 600, 315
BLUE, DEEP, INK, MUTED, WASH = "#0F62FE", "#0043CE", "#101828", "#5A6478", "#F4F8FF"
FONTS = ["/System/Library/Fonts/Hiragino Sans GB.ttc",
         "/System/Library/Fonts/STHeiti Medium.ttc",
         "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"]


def font(size: int, cjk: bool) -> ImageFont.FreeTypeFont:
    path = FONTS[0] if cjk else "/System/Library/Fonts/Helvetica.ttc"
    try:
        return ImageFont.truetype(path, size, index=0)
    except OSError:
        return ImageFont.truetype(FONTS[-1], size)


def wrap(draw, text: str, f, max_w: int, max_lines: int) -> list[str]:
    """Wrap text, adding an ellipsis when it cannot fit in max_lines."""
    cjk = bool(re.search(r"[\u4e00-\u9fff]", text))
    units = list(text) if cjk else text.split()
    joiner = "" if cjk else " "
    lines, cur, truncated = [], "", False
    for idx, u in enumerate(units):
        probe = f"{cur}{joiner}{u}" if cur else u
        if draw.textlength(probe, font=f) <= max_w:
            cur = probe
        else:
            if cur:
                lines.append(cur)
            cur = u
            if len(lines) == max_lines:
                truncated = True
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    elif cur:
        truncated = True
    if truncated and lines:
        last = lines[-1]
        while draw.textlength(last + "…", font=f) > max_w and len(last) > 1:
            last = last[:-1]
        lines[-1] = last.rstrip() + "…"
    return lines[:max_lines]


def svg_steps(slug: str) -> list[str]:
    """Legacy articles have no flow markup, but their diagram SVG carries labels."""
    svg = ROOT / "assets/blog/svg/en" / f"{slug}.svg"
    if not svg.exists():
        return []
    raw = svg.read_text(errors="ignore")
    texts = [html.unescape(re.sub(r"<[^>]+>", "", t)).strip()
             for t in re.findall(r"<text[^>]*>(.*?)</text>", raw, re.S)]
    labels = [t for t in texts[1:] if t and not re.fullmatch(r"\d+", t)]
    return labels[:5]


def extract(page: Path) -> dict:
    text = page.read_text(errors="ignore")
    steps = re.findall(r'<div class="ar-flow-step"><b>[^<]*</b><strong>(.*?)</strong>', text, re.S)[:5]
    if not steps:
        steps = svg_steps(page.stem)
    title = re.search(r'<h1 class="ar-title">(.*?)</h1>', text, re.S)
    return {
        "steps": [html.unescape(s).strip() for s in steps],
        "title": html.unescape(title.group(1)).strip() if title else page.stem,
    }


def render(meta: dict, out: Path) -> None:
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    cjk = bool(re.search(r"[\u4e00-\u9fff]", meta["title"]))
    f_num = font(15, cjk)
    f_step = font(11, cjk)
    f_brand = font(12, cjk)

    d.rectangle([0, 0, W, 5], fill=BLUE)
    d.text((22, 18), "BEEHIVE STRATEGY", font=f_brand, fill=BLUE)

    steps = meta["steps"][:5] or ["Context", "Data", "Model", "Answer", "Proof"]
    top, gap = 96, 10
    n = len(steps)
    box_w = (W - 44 - gap * (n - 1)) / n
    box_h = 132
    for i, label in enumerate(steps):
        x = 22 + i * (box_w + gap)
        d.rounded_rectangle([x, top, x + box_w, top + box_h], radius=8,
                            fill=WASH, outline="#D6E2FF", width=1)
        d.text((x + 10, top + 10), f"{i + 1:02d}", font=f_num, fill=BLUE)
        for j, line in enumerate(wrap(d, label, f_step, int(box_w) - 20, 3)):
            d.text((x + 10, top + 36 + j * 17), line, font=f_step, fill=INK)
        if i < n - 1:
            ax = x + box_w + 1
            d.line([ax, top + box_h / 2, ax + gap - 3, top + box_h / 2], fill=BLUE, width=2)

    d.line([22, H - 30, W - 22, H - 30], fill="#E3EAF9", width=1)
    d.text((22, H - 24), "beehivestrategy.com", font=f_brand, fill=DEEP)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "JPEG", quality=86, optimize=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--sample", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    if args.sample:
        for folder in LANGS.values():
            page = folder / f"{args.sample}.html"
            if page.exists():
                render(extract(page), Path(args.out or "/tmp/card_sample.jpg"))
                print("wrote", args.out or "/tmp/card_sample.jpg")
                return 0
        raise SystemExit("sample not found")

    # Card images live at one shared path per slug, so they are rendered from the
    # English source to stay identical on every language index.
    total = 0
    for page in LANGS["en"].glob("*.html"):
        suffix = page.stem[-8:]
        if not args.all and not (args.start and suffix.isdigit() and suffix >= args.start):
            continue
        text = page.read_text(errors="ignore")
        if 'class="ar-flow-step"' not in text and not (ROOT / "assets/blog/svg/en" / f"{page.stem}.svg").exists():
            continue  # neither flow markup nor a diagram to fall back to
        render(extract(page), CARDS / f"{page.stem}.jpg")
        total += 1
    print("cards:", total)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
