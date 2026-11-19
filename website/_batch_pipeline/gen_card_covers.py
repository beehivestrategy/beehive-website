#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_card_covers.py — text-free, per-article abstract covers for the blog index cards.

Why: the old covers baked each article's title into the image, which duplicated
the title printed in the card body. The index therefore hid every <img> and used
one shared CSS arc. This generator makes a DISTINCT, title-free image per slug so
every card looks different without repeating any text. Language-neutral: the image
has no words, so all three locales share the same file.

v3 (2026-11-20): user reported "repeat pattern" — the old v2 had only 8 prototypes
and adjacent cards often shared one. Now:
  - 16 structural prototypes (vs 8)
  - prototype index derived from the slug's POSITION in the index, cycling so no
    adjacent card shares a prototype (period-16 permutation)
  - 6 muted palette families + 4 ground styles, chosen by slug hash
  - varying focal position / density / orientation within each prototype

Deterministic: same slug at same position -> same image (sha256-derived params).
Usage:
  python3 gen_card_covers.py --sample          # contact sheet for review
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
BORDER = (197, 206, 230)
LINE = (184, 205, 253)
WASH = (239, 244, 255)
ACCENT = (15, 98, 254)      # --accent IBM blue
WHITE = (255, 255, 255)

# muted palette families: (accent, secondary, line, fill) — all light-ground safe
PALETTES = [
    ((15, 98, 254),   (184, 205, 253), (222, 232, 253), (239, 244, 255)),  # IBM blue
    ((43, 158, 139),  (140, 205, 190), (206, 232, 225), (236, 246, 243)),  # teal
    ((142, 123, 181), (190, 178, 216), (224, 217, 239), (244, 241, 250)),  # plum
    ((212, 168, 67),  (228, 200, 135), (240, 228, 196), (250, 245, 233)),  # gold
    ((209, 139, 106), (226, 182, 160), (242, 218, 205), (251, 243, 238)),  # coral
    ((111, 162, 135), (168, 202, 182), (216, 232, 222), (240, 247, 243)),  # sage
]


def slug_list():
    # The index now points at /assets/blog/cards/<slug>.jpg (v2+); older
    # revisions pointed at /assets/blog/covers/en/<slug>.jpg. Support both,
    # falling back to the on-disk cards dir so the generator stays rerunnable.
    s = INDEX.read_text(encoding="utf-8")
    slugs = re.findall(r"/assets/blog/(?:covers/en|cards)/([^\"]+)\.jpg", s)
    seen, out = set(), []
    for x in slugs:
        if x not in seen:
            seen.add(x)
            out.append(x)
    if not out and OUT.exists():
        out = sorted(p.stem for p in OUT.glob("*.jpg"))
    return out


def params(slug):
    b = hashlib.sha256(slug.encode("utf-8")).digest()
    return lambda i, m: b[i % len(b)] % m


# 16-prototype permutation ordering: consecutive positions never repeat a family.
# We derive proto as (position * 7 + seed_offset) % 16 with a coprime step so a
# full cycle visits all 16 before repeating, guaranteeing no adjacent duplicates.
def proto_for(slug, position):
    # Pure position-driven permutation: step 7 is coprime with 16, so every
    # card in a run of 16 has a unique prototype and NO two adjacent cards
    # share one. Slug hash still varies everything *inside* the prototype.
    return (position * 7 + 3) % 16


def ground(d, pal, kind, p):
    accent, secondary, line, fill = pal
    if kind == 0:      # full grid
        for x in range(0, W, 25):
            d.line([x * S, 0, x * S, H * S], fill=GRID, width=1)
        for y in range(0, H, 25):
            d.line([0, y * S, W * S, y * S], fill=GRID, width=1)
    elif kind == 1:    # dot field
        for x in range(20, W, 24):
            for y in range(20, H, 24):
                d.ellipse([x * S - 2, y * S - 2, x * S + 2, y * S + 2], fill=line)
    elif kind == 2:    # sparse vertical rules
        step = 20 + p(1, 16)
        for x in range(step, W, step):
            d.line([x * S, 0, x * S, H * S], fill=GRID, width=1)
    else:              # plain with corner wash
        d.ellipse([W * S - 90 * S, -40 * S, W * S + 40 * S, 120 * S], fill=fill)


def render(slug, position=0):
    p = params(slug)
    proto = proto_for(slug, position)
    pal = PALETTES[p(1, len(PALETTES))]
    accent, secondary, line, fill = pal
    im = Image.new("RGB", (W * S, H * S), BG)
    d = ImageDraw.Draw(im)
    sc = lambda v: int(v * S)
    ground(d, pal, p(2, 4), p)

    # left blue rule (accent of the chosen palette)
    d.rectangle([0, 0, sc(3), sc(H)], fill=accent)

    if proto == 0:      # concentric arcs
        cx, cy = 380 + p(3, 120), 100 + p(4, 60) - 30
        base = 40 + p(5, 28)
        n = 2 + p(6, 3)
        hi = p(7, n)
        for k in range(n):
            r = base + k * (24 + p(8, 10))
            start = p(9 + k, 4) * 28
            span = 110 + p(12 + k, 110)
            col = accent if k == hi else line
            d.arc([sc(cx - r), sc(cy - r), sc(cx + r), sc(cy + r)],
                  start, start + span, fill=col, width=sc(3 if k == hi else 2))

    elif proto == 1:    # data bars
        n = 7 + p(3, 6)
        gap = 540 / n
        hi = p(9, n)
        for k in range(n):
            x = 40 + k * gap
            wd = int(gap * 0.5)
            hgt = 32 + p(10 + k, 120)
            col = accent if k == hi else fill
            d.rectangle([sc(x), sc(178 - hgt), sc(x + wd), sc(178)], fill=col)

    elif proto == 2:    # dot matrix
        cols = 7 + p(3, 4)
        rows = 3
        gapx = 520 / cols
        for i in range(cols):
            for j in range(rows):
                x, y = 50 + i * gapx, 46 + j * 50
                r = 3 + p(20 + i * 3 + j, 5)
                v = p(40 + i * 3 + j, 6)
                col = accent if v == 0 else (line if v <= 2 else fill)
                d.ellipse([sc(x - r), sc(y - r), sc(x + r), sc(y + r)], fill=col)

    elif proto == 3:    # parallel hatch
        ang = 18 + p(3, 46)
        n = 8 + p(4, 7)
        hi = p(5, n)
        dy = int(60 * math.tan(math.radians(ang)))
        gap = 560 / n
        for k in range(n):
            x0 = 30 + k * gap
            col = accent if k == hi else line
            d.line([sc(x0), sc(182), sc(x0 + dy), sc(18)],
                   fill=col, width=sc(3 if k == hi else 2))

    elif proto == 4:    # node graph
        n = 4 + p(3, 4)
        pts = [(50 + p(4 + k * 2, 480), 28 + p(5 + k * 2, 140)) for k in range(n)]
        for a in range(n):
            for b2 in range(a + 1, n):
                if p(20 + a * 10 + b2, 3) == 0:
                    d.line([sc(pts[a][0]), sc(pts[a][1]), sc(pts[b2][0]), sc(pts[b2][1])],
                           fill=line, width=sc(2))
        hi = p(30, n)
        for k, (x, y) in enumerate(pts):
            r = 9 if k == hi else 5
            col = accent if k == hi else secondary
            d.ellipse([sc(x - r), sc(y - r), sc(x + r), sc(y + r)], fill=col)

    elif proto == 5:    # stacked sheets
        ox, oy = 200 + p(3, 90), 16 + p(4, 40)
        for k, (dx, dy, rot) in enumerate(((0, 0, 0), (16, -9, 5), (32, -18, 10))):
            x, y = ox + dx + p(5 + k, 12), oy + dy
            wd, hgt = 145 + p(8 + k, 30), 92 + p(11 + k, 20)
            skew = int(hgt * math.tan(math.radians(rot)))
            poly = [(x, y), (x + wd, y + skew), (x + wd, y + hgt + skew), (x, y + hgt)]
            d.polygon([(sc(a), sc(b)) for a, b in poly],
                      fill=(fill if k == 2 else WHITE),
                      outline=(accent if k == 0 else secondary))
        d.rectangle([sc(ox + 14), sc(oy + 30), sc(ox + 90), sc(oy + 38)], fill=line)

    elif proto == 6:    # radial ticks
        cx, cy = 405, 172
        base, n = 68 + p(3, 30), 12 + p(4, 10)
        hi = p(5, n)
        for k in range(n):
            a = math.pi - k * math.pi / (n - 1)
            r2 = base + (24 if k == hi else 11)
            x1, y1 = cx + base * math.cos(a), cy - base * math.sin(a)
            x2, y2 = cx + r2 * math.cos(a), cy - r2 * math.sin(a)
            col = accent if k == hi else secondary
            d.line([sc(x1), sc(y1), sc(x2), sc(y2)], fill=col, width=sc(3 if k == hi else 2))

    elif proto == 7:    # wave lines
        for w in range(2 + p(3, 3)):
            amp = 18 + p(4 + w, 34)
            freq = 1 + p(7 + w, 4) / 10
            phase = p(10 + w, 6)
            col = accent if w == 0 else line
            pts = []
            for x in range(40, 580, 8):
                y = 100 + amp * math.sin((x / 60) * freq + phase)
                pts.append((sc(x), sc(int(y))))
            d.line(pts, fill=col, width=sc(3 if w == 0 else 2))

    elif proto == 8:    # chevrons / arrows
        n = 4 + p(3, 4)
        gap = 520 / n
        for k in range(n):
            x = 60 + k * gap
            y = 100 + (k % 2) * 30 - 15
            wd, hgt = 40 + p(5 + k, 20), 28
            col = accent if k == p(2, n) else fill
            d.line([sc(x), sc(y), sc(x + wd / 2), sc(y + hgt), sc(x + wd), sc(y)],
                   fill=col, width=sc(4))

    elif proto == 9:    # concentric squares
        cx, cy = 380 + p(3, 100), 100
        n = 3 + p(4, 3)
        for k in range(n):
            r = 24 + k * (22 + p(5, 8))
            col = accent if k == n - 1 else (line if k % 2 else fill)
            d.rectangle([sc(cx - r), sc(cy - r * 0.7), sc(cx + r), sc(cy + r * 0.7)],
                        outline=col, width=sc(3 if k == n - 1 else 2))

    elif proto == 10:   # progress steps
        n = 5 + p(3, 4)
        gap = 540 / n
        filled = p(4, n)
        for k in range(n):
            x = 40 + k * gap
            wd = gap - 12
            hgt = 26 + p(5 + k, 20)
            col = accent if k <= filled else fill
            d.rounded_rectangle([sc(x), sc(178 - hgt), sc(x + wd), sc(178)],
                                radius=sc(6), fill=col)

    elif proto == 11:   # flow curve (bezier-like polyline)
        n = 5 + p(3, 4)
        pts = []
        for k in range(n):
            x = 50 + k * (520 / (n - 1))
            y = 100 + int(45 * math.sin(k * 1.1 + p(4, 6)))
            pts.append((sc(x), sc(y)))
        d.line(pts, fill=accent, width=sc(4), joint="curve")
        for k, (x, y) in enumerate(pts):
            r = 7 if k == p(2, n) else 4
            d.ellipse([x - sc(r), y - sc(r), x + sc(r), y + sc(r)], fill=secondary)

    elif proto == 12:   # barbell / comparison
        cy = 100 + p(3, 20) - 10
        for k in range(3 + p(4, 3)):
            x = 70 + k * (460 / (2 + p(4, 3)))
            half = 40 + p(5 + k, 30)
            d.line([sc(x - half), sc(cy), sc(x + half), sc(cy)], fill=line, width=sc(2))
            d.ellipse([sc(x - half - 7), sc(cy - 7), sc(x - half + 7), sc(cy + 7)], fill=secondary)
            d.ellipse([sc(x + half - 7), sc(cy - 7), sc(x + half + 7), sc(cy + 7)], fill=accent)

    elif proto == 13:   # grid blocks (varying occupancy)
        cols, rows = 8 + p(3, 3), 3
        cw, chh = 540 / cols, 44
        for i in range(cols):
            for j in range(rows):
                if p(20 + i * 3 + j, 4) < 2:
                    x, y = 40 + i * cw, 30 + j * chh
                    col = accent if p(40 + i * 3 + j, 6) == 0 else (secondary if (i + j) % 3 == 0 else fill)
                    d.rectangle([sc(x), sc(y), sc(x + cw - 6), sc(y + chh - 6)],
                                fill=col, outline=None)

    elif proto == 14:   # radiating lines from focal point
        fx, fy = 150 + p(3, 300), 100 + p(4, 60) - 30
        n = 9 + p(5, 7)
        for k in range(n):
            a = -math.pi / 2 + k * 2 * math.pi / n
            length = 60 + p(6 + k, 90)
            x2, y2 = fx + length * math.cos(a), fy + length * math.sin(a)
            col = accent if k == p(2, n) else line
            d.line([sc(fx), sc(fy), sc(x2), sc(y2)], fill=col, width=sc(2))

    else:               # proto 15: nested diamonds
        cx, cy = 380 + p(3, 100), 100
        n = 3 + p(4, 2)
        for k in range(n):
            r = 30 + k * 30
            col = accent if k == n - 1 else (line if k % 2 else fill)
            pts = [(sc(cx), sc(cy - r)), (sc(cx + r), sc(cy)),
                   (sc(cx), sc(cy + r)), (sc(cx - r), sc(cy))]
            d.line(pts + [pts[0]], fill=col, width=sc(3 if k == n - 1 else 2))

    return im.resize((W, H), Image.LANCZOS)


def main():
    slugs = slug_list()
    mode = "--apply" if "--apply" in sys.argv else "--sample"
    print("slugs:", len(slugs), "mode:", mode)
    if mode == "--sample":
        # one sample per prototype, spread by position
        picks = [(i, slugs[i * 7 % len(slugs)]) for i in range(16)]
        sheet = Image.new("RGB", (4 * 300, 4 * 132), (255, 255, 255))
        for i, (pos, s) in enumerate(picks):
            im = render(s, pos)
            sheet.paste(im.resize((300, 100)), ((i % 4) * 300, (i // 4) * 132))
        out = Path("/tmp/card_cover_contact.jpg")
        sheet.save(out, quality=90)
        print("contact sheet:", out)
    else:
        OUT.mkdir(parents=True, exist_ok=True)
        for i, s in enumerate(slugs):
            render(s, i).save(OUT / (s + ".jpg"), quality=86, optimize=True)
            if (i + 1) % 200 == 0:
                print("  rendered", i + 1)
        print("done:", len(slugs), "->", OUT)


if __name__ == "__main__":
    main()
