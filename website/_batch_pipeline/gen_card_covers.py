#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_card_covers.py — text-free, per-article abstract covers for the blog index cards.

Why: the old covers baked each article's title into the image, which duplicated
the title printed in the card body. The index therefore hid every <img> and used
one shared CSS arc. This generator makes a DISTINCT, title-free image per slug so
every card looks different without repeating any text. Language-neutral: the image
has no words, so all three locales share the same file.

Deterministic: same slug -> same image (sha256-derived parameters).
Usage:
  python3 gen_card_covers.py --sample          # 12-image contact sheet for review
  python3 gen_card_covers.py --apply            # render all slugs to assets/blog/cards
"""
import hashlib
import math
import re
import sys
from pathlib import Path
from PIL import Image, ImageDraw

WEB = Path(__file__).resolve().parents[1]
INDEX = WEB / "blog.html"
OUT = WEB / "assets" / "blog" / "cards"
W, H, S = 600, 200, 2  # logical size, 2x supersample for antialiasing

BG = (247, 249, 254)        # --surface-2
GRID = (233, 238, 250)
BORDER = (197, 206, 230)    # --border-2
LINE = (184, 205, 253)      # accent @ ~0.28 on light ground
WASH = (239, 244, 255)      # accent @ ~0.07
ACCENT = (15, 98, 254)      # --accent
WHITE = (255, 255, 255)


def slug_list():
    s = INDEX.read_text(encoding="utf-8")
    slugs = re.findall(r"/assets/blog/covers/en/([^\"]+)\.jpg", s)
    seen, out = set(), []
    for x in slugs:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def params(slug):
    b = hashlib.sha256(slug.encode("utf-8")).digest()
    return lambda i, m: b[i % len(b)] % m


def render(slug):
    p = params(slug)
    proto = p(0, 8)
    im = Image.new("RGB", (W * S, H * S), BG)
    d = ImageDraw.Draw(im)
    sc = lambda v: int(v * S)

    # shared ground: faint plotting grid + left blue rule
    for x in range(0, W, 25):
        d.line([sc(x), 0, sc(x), sc(H)], fill=GRID, width=1)
    for y in range(0, H, 25):
        d.line([0, sc(y), sc(W), sc(y)], fill=GRID, width=1)
    d.rectangle([0, 0, sc(3), sc(H)], fill=ACCENT)

    if proto == 0:  # concentric arcs
        cx, cy = 380 + p(1, 120), 100 + p(2, 60) - 30
        base = 40 + p(3, 28)
        n = 2 + p(4, 3)
        hi = p(8, n)
        for k in range(n):
            r = base + k * (24 + p(5, 10))
            start = p(6 + k, 4) * 28
            span = 110 + p(7 + k, 110)
            col = ACCENT if k == hi else LINE
            d.arc([sc(cx - r), sc(cy - r), sc(cx + r), sc(cy + r)],
                  start, start + span, fill=col, width=sc(3 if k == hi else 1))

    elif proto == 1:  # data bars
        n = 7 + p(1, 6)
        gap = 540 / n
        hi = p(9, n)
        for k in range(n):
            x = 40 + k * gap
            wd = int(gap * 0.5)
            hgt = 32 + p(2 + k, 120)
            col = ACCENT if k == hi else BORDER
            d.rectangle([sc(x), sc(178 - hgt), sc(x + wd), sc(178)], fill=col)

    elif proto == 2:  # dot matrix
        for i in range(9):
            for j in range(3):
                x, y = 60 + i * 58, 46 + j * 50
                r = 3 + p(3 + i * 3 + j, 4)
                if p(11 + i * 3 + j, 5) == 0:
                    col, r = ACCENT, r + 2
                elif p(12 + i * 3 + j, 3) == 0:
                    col = LINE
                else:
                    col = BORDER
                d.ellipse([sc(x - r), sc(y - r), sc(x + r), sc(y + r)], fill=col)

    elif proto == 3:  # parallel hatch
        ang = 20 + p(1, 40)
        n = 9 + p(2, 6)
        hi = p(13, n)
        dy = int(60 * math.tan(math.radians(ang)))
        for k in range(n):
            x0 = 40 + k * 60
            col = ACCENT if k == hi else LINE
            d.line([sc(x0), sc(180), sc(x0 + dy), sc(20)],
                   fill=col, width=sc(3 if k == hi else 1))

    elif proto == 4:  # node graph
        n = 4 + p(1, 4)
        pts = [(60 + p(2 + k * 2, 480), 30 + p(3 + k * 2, 140)) for k in range(n)]
        for a in range(n):
            for b2 in range(a + 1, n):
                if p(20 + a * 10 + b2, 3) == 0:
                    d.line([sc(pts[a][0]), sc(pts[a][1]), sc(pts[b2][0]), sc(pts[b2][1])],
                           fill=LINE, width=sc(1))
        hi = p(21, n)
        for k, (x, y) in enumerate(pts):
            r = 9 if k == hi else 5
            col = ACCENT if k == hi else BORDER
            d.ellipse([sc(x - r), sc(y - r), sc(x + r), sc(y + r)], fill=col)

    elif proto == 5:  # stacked sheets (echo of the hero plate)
        ox, oy = 210 + p(1, 70), 18 + p(2, 34)
        for k, (dx, dy, rot) in enumerate(((0, 0, 0), (15, -9, 5), (30, -18, 10))):
            x, y = ox + dx + p(3 + k, 10), oy + dy
            wd, hgt = 145 + p(4 + k, 28), 92 + p(5 + k, 18)
            skew = int(hgt * math.tan(math.radians(rot)))
            poly = [(x, y), (x + wd, y + skew), (x + wd, y + hgt + skew), (x, y + hgt)]
            d.polygon([(sc(a), sc(b)) for a, b in poly],
                      fill=(WASH if k == 2 else WHITE),
                      outline=(ACCENT if k == 0 else BORDER))
        d.rectangle([sc(ox + 14), sc(oy + 30), sc(ox + 90), sc(oy + 38)], fill=LINE)

    elif proto == 6:  # radial ticks
        cx, cy = 405, 172
        base, n = 72 + p(1, 26), 14 + p(2, 8)
        hi = p(15, n)
        for k in range(n):
            a = math.pi - k * math.pi / (n - 1)
            r2 = base + (22 if k == hi else 11)
            x1, y1 = cx + base * math.cos(a), cy - base * math.sin(a)
            x2, y2 = cx + r2 * math.cos(a), cy - r2 * math.sin(a)
            col = ACCENT if k == hi else BORDER
            d.line([sc(x1), sc(y1), sc(x2), sc(y2)], fill=col, width=sc(3 if k == hi else 1))

    else:  # wave lines
        for w in range(2 + p(1, 2)):
            amp = 20 + p(2 + w, 30)
            freq = 1 + p(3 + w, 3) / 10
            phase = p(4 + w, 6)
            col = ACCENT if w == 0 else LINE
            pts = []
            for x in range(40, 580, 8):
                y = 100 + amp * math.sin((x / 60) * freq + phase)
                pts.append((sc(x), sc(int(y))))
            d.line(pts, fill=col, width=sc(3 if w == 0 else 1))

    return im.resize((W, H), Image.LANCZOS)


def main():
    slugs = slug_list()
    mode = "--apply" if "--apply" in sys.argv else "--sample"
    print("slugs:", len(slugs), "mode:", mode)
    if mode == "--sample":
        picks = [slugs[0], slugs[1], slugs[2], slugs[3], slugs[5], slugs[8],
                 slugs[13], slugs[21], slugs[34], slugs[55], slugs[89], slugs[144]]
        sheet = Image.new("RGB", (4 * 300, 3 * 132), (255, 255, 255))
        for i, s in enumerate(picks):
            im = render(s)
            sheet.paste(im.resize((300, 100)), ((i % 4) * 300, (i // 4) * 132))
        out = Path("/tmp/card_cover_contact.jpg")
        sheet.save(out, quality=90)
        print("contact sheet:", out)
    else:
        OUT.mkdir(parents=True, exist_ok=True)
        for i, s in enumerate(slugs):
            render(s).save(OUT / (s + ".jpg"), quality=86, optimize=True)
            if (i + 1) % 200 == 0:
                print("  rendered", i + 1)
        print("done:", len(slugs), "->", OUT)


if __name__ == "__main__":
    main()
