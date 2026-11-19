#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_article_heroes.py — diverse, on-brand conceptual hero diagrams for every article.

Why: site_improve_v2.py:make_svg() produced only 8 templates sharing ONE
background (same gradient + two fixed ellipses) and one low-sat palette, so
~830/1101 diagrams looked identical at a glance ("repeat pattern").

This generator keeps the SAME visual language (light editorial ground, thin
IBM-blue/muted teal/gold strokes, class="svg-draw" for the reveal animation,
800x450, "Beehive Strategy · conceptual diagram" footer) but multiplies the
dimensions of variation:

  - 16 structural prototypes (vs 8)
  - topic-driven prototype weighting from articleSection (20+ sections)
  - 5 background patterns (grid / dot / diagonal / corner-arc / plain-gradient)
  - palette pairs drawn from a wider, still-muted set, deterministically per slug
  - varying focal position, orientation, density, element count

Deterministic: same slug (+ optional section) -> same SVG.
Language-neutral: no words except the fixed brand footer, so all locales share it.
Only REPLACES existing assets/blog/svg/<slug>.svg — never touches HTML structure.

Usage:
  python3 gen_article_heroes.py --sample          # contact sheet for review
  python3 gen_article_heroes.py --apply           # regenerate all 1098 diagrams
"""
import hashlib
import math
import os
import random
import re
import sys
from pathlib import Path

WEB = Path(__file__).resolve().parents[1]
ROOT = WEB
SVG_DIR = WEB / "assets" / "blog" / "svg"
ART_DIRS = [WEB / "blog" / "articles", WEB / "zh-cn" / "blog" / "articles",
            WEB / "zh-hk" / "blog" / "articles"]

W, H, M = 800, 450, 60

# Muted editorial palette (light ground, dark ink) — consistent with accenture.css
INK = "#0e2a3b"
SLATE = "#5b7083"
MIST = "#e8eef0"
TEAL = "#2B9E8B"
GOLD = "#d4a843"
AQUA = "#6cc4b4"
BLUE = "#0F62FE"
BLUE_L = "#9dbcfb"
STEEL = "#7d94a6"
PLUM = "#8e7bb5"
CORAL = "#d18b6a"
SAGE = "#6fa287"

PAIRS = [
    (TEAL, GOLD), (BLUE, AQUA), (STEEL, GOLD), (PLUM, AQUA),
    (CORAL, BLUE_L), (SAGE, GOLD), (TEAL, BLUE_L), (BLUE, GOLD),
    (PLUM, GOLD), (STEEL, AQUA), (SAGE, BLUE_L), (TEAL, CORAL),
]

# topic -> preferred prototype families (semantic resonance, still varied by seed)
SECTION_PROTO = {
    "Technology":        [0, 5, 8, 12, 14],
    "AI Strategy":       [1, 6, 9, 13, 15],
    "AI Regulation":     [2, 7, 10, 13],
    "Data Governance":   [3, 8, 11, 14],
    "Conversational BI": [4, 9, 12, 15],
    "Analytics":         [4, 8, 11, 15],
    "Industry":          [5, 10, 13, 14],
    "Strategy":          [1, 6, 9, 13],
    "Manufacturing":     [5, 10, 12, 14],
    "Retail":            [4, 7, 11, 15],
    "Financial Services":[6, 8, 11, 13],
    "Digital Transformation":[1, 6, 12, 15],
    "Enterprise AI":     [0, 5, 9, 14],
    "AI Governance":     [2, 7, 10, 13],
    "Data Strategy":     [3, 8, 11, 14],
}
DEFAULT_PROTOS = list(range(16))

PROTOS = [
    "nodes", "funnel", "layers", "flow", "chat", "circuit", "roadmap",
    "shield", "sankey", "matrix", "gauge", "hierarchy", "scatter",
    "loop", "stack", "radar",
]


def seed_of(slug):
    return int(hashlib.md5(slug.encode("utf-8")).hexdigest()[:8], 16)


def section_for(slug):
    """Read articleSection from any locale's article page (first match)."""
    for d in ART_DIRS:
        p = d / (slug + ".html")
        if p.exists():
            m = re.search(r'"articleSection"\s*:\s*"([^"]+)"',
                          p.read_text(encoding="utf-8", errors="ignore"))
            if m:
                return m.group(1)
    return ""


def background(rnd, a1, a2):
    """Pick one of five subtle grounds; returns raw SVG string."""
    kind = rnd.randrange(5)
    parts = []
    # base gradient with variable direction + muted stops
    x2 = rnd.choice([0, 1, 0.4])
    y2 = rnd.choice([1, 0, 0.6])
    stops = rnd.choice([
        ("#f7fafb", "#eaf2f3"), ("#f8fafc", "#eef1f8"),
        ("#f7faf9", "#e9f1ee"), ("#f9fafc", "#edf0f6"),
    ])
    parts.append(
        f'<defs><linearGradient id="bg" x1="0" y1="0" x2="{x2}" y2="{y2}">'
        f'<stop offset="0" stop-color="{stops[0]}"/>'
        f'<stop offset="1" stop-color="{stops[1]}"/></linearGradient></defs>'
        f'<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>')
    if kind == 0:  # plotting grid
        step = rnd.choice([40, 50, 60])
        for x in range(0, W, step):
            parts.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{MIST}" stroke-width="1"/>')
        for y in range(0, H, step):
            parts.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{MIST}" stroke-width="1"/>')
    elif kind == 1:  # dot field
        step = rnd.choice([28, 36, 44])
        for x in range(step // 2, W, step):
            for y in range(step // 2, H, step):
                parts.append(f'<circle cx="{x}" cy="{y}" r="1.6" fill="{MIST}"/>')
    elif kind == 2:  # diagonal hatch band
        off = rnd.randint(-120, 120)
        for k in range(-3, 14):
            x = off + k * 70
            parts.append(f'<line x1="{x}" y1="{H}" x2="{x+180}" y2="0" stroke="{MIST}" stroke-width="2"/>')
    elif kind == 3:  # corner arcs (variable position)
        c = rnd.choice([("0", "0"), (W, "0"), ("0", H), (W, H)])
        for r in (90, 140, 190):
            parts.append(f'<circle cx="{c[0]}" cy="{c[1]}" r="{r}" fill="none" '
                         f'stroke="{MIST}" stroke-width="1.5"/>')
    else:  # plain + soft wash blob at varying corner
        cx = rnd.choice([int(W * .2), int(W * .8)])
        cy = rnd.choice([int(H * .2), int(H * .8)])
        parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rnd.randint(110,180)}" '
                     f'ry="{rnd.randint(80,130)}" fill="{a2}" opacity="0.10"/>')
    return "".join(parts)


def proto_shapes(idx, rnd, a1, a2):
    """Return list of SVG element strings for prototype idx."""
    p = PROTOS[idx]
    out = []
    S = lambda v: int(v)

    if p == "nodes":  # network graph
        n = rnd.randint(5, 9)
        pts = [(rnd.randint(M + 20, W - M - 20), rnd.randint(90, H - M)) for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, min(i + 4, n)):
                out.append(f'<line x1="{pts[i][0]}" y1="{pts[i][1]}" x2="{pts[j][0]}" '
                           f'y2="{pts[j][1]}" stroke="{MIST}" stroke-width="2"/>')
        for k, (x, y) in enumerate(pts):
            r = rnd.randint(9, 16)
            out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{a1 if k%3 else a2}" '
                       f'class="svg-draw" pathLength="1" stroke="{INK}" stroke-width="1.5"/>')

    elif p == "funnel":  # funnel / refinement
        rows = rnd.randint(3, 5)
        for i in range(rows):
            wd = (W - 2 * M) * (1 - i * (0.10 + (i % 2) * 0.04))
            x = (W - wd) / 2
            y = 80 + i * (250 // rows)
            h = 52
            out.append(f'<path d="M{x:.0f} {y} L{x+wd:.0f} {y} L{x+wd-22:.0f} {y+h} L{x+22:.0f} {y+h} Z" '
                       f'fill="{a1 if i % 2 == 0 else a2}" opacity="{0.88-i*0.10:.2f}" '
                       f'class="svg-draw" pathLength="1" stroke="{INK}" stroke-width="1"/>')

    elif p == "layers":  # stacked layers
        n = rnd.randint(3, 5)
        for i in range(n):
            y = 82 + i * (250 // n)
            off = i * rnd.choice([10, 14, 18])
            out.append(f'<rect x="{M+off}" y="{y}" width="{W-2*M-2*off}" height="{rnd.randint(46,58)}" '
                       f'rx="12" fill="{a1 if i%2==0 else a2}" opacity="0.9" '
                       f'class="svg-draw" pathLength="1" stroke="{INK}" stroke-width="1"/>')

    elif p == "flow":  # directed flow with arrowheads
        n = rnd.randint(3, 5)
        y = 150 + rnd.randint(-30, 30)
        gap = (W - 2 * M) / (n - 1)
        xs = [M + i * gap for i in range(n)]
        for i in range(n - 1):
            out.append(f'<line x1="{xs[i]+34:.0f}" y1="{y}" x2="{xs[i+1]-34:.0f}" y2="{y}" '
                       f'stroke="{MIST}" stroke-width="4"/>')
            out.append(f'<polygon points="{xs[i+1]-34:.0f},{y-6} {xs[i+1]-22:.0f},{y} '
                       f'{xs[i+1]-34:.0f},{y+6}" fill="{a2}"/>')
        for i, x in enumerate(xs):
            out.append(f'<rect x="{x-34:.0f}" y="{y-30}" width="68" height="60" rx="10" '
                       f'fill="{a1 if i%2==0 else a2}" stroke="{INK}" stroke-width="1.2" '
                       f'class="svg-draw" pathLength="1"/>')

    elif p == "chat":  # conversational turns
        n = rnd.randint(3, 5)
        y = 70
        for i in range(n):
            left = (i % 2 == 0)
            bw = rnd.randint(200, 320)
            x = M + (0 if left else W - M - bw)
            out.append(f'<rect x="{x}" y="{y+i*64}" width="{bw}" height="46" rx="14" '
                       f'fill="{a1 if left else a2}" opacity="0.92" '
                       f'class="svg-draw" pathLength="1" stroke="{INK}" stroke-width="1"/>')
            for k in range(rnd.randint(2, 4)):
                out.append(f'<circle cx="{x+24+k*16}" cy="{y+i*64+23}" r="3.5" fill="{INK}" opacity="0.35"/>')

    elif p == "circuit":  # grid circuit
        rows = rnd.randint(4, 6)
        cols = rnd.randint(7, 10)
        for i in range(rows):
            y = 80 + i * (270 // (rows - 1))
            out.append(f'<line x1="{M}" y1="{y}" x2="{W-M}" y2="{y}" stroke="{MIST}" stroke-width="2"/>')
        for i in range(cols):
            x = M + i * (W - 2 * M) / (cols - 1)
            out.append(f'<line x1="{x:.0f}" y1="80" x2="{x:.0f}" y2="{80+270}" stroke="{MIST}" stroke-width="2"/>')
        for i in range(cols):
            for j in range(rows):
                if rnd.random() < 0.55:
                    x = M + i * (W - 2 * M) / (cols - 1)
                    y = 80 + j * (270 // (rows - 1))
                    out.append(f'<rect x="{x-6:.0f}" y="{y-6:.0f}" width="12" height="12" '
                               f'fill="{a1 if (i+j)%2==0 else a2}" class="svg-draw" pathLength="1"/>')

    elif p == "roadmap":  # milestone timeline
        y = H * 0.55
        out.append(f'<line x1="{M}" y1="{y:.0f}" x2="{W-M}" y2="{y:.0f}" stroke="{SLATE}" '
                   f'stroke-width="3" class="svg-draw" pathLength="1"/>')
        n = rnd.randint(3, 5)
        for i in range(n):
            x = M + (W - 2 * M) * i / (n - 1)
            up = (i % 2 == 0)
            out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="13" fill="{a1 if i%2==0 else a2}" '
                       f'stroke="{INK}" stroke-width="1.5"/>')
            ly = y - 60 if up else y + 24
            out.append(f'<line x1="{x:.0f}" y1="{(y-13) if up else (y+13):.0f}" x2="{x:.0f}" '
                       f'y2="{(y-40) if up else (y+40):.0f}" stroke="{AQUA}" stroke-width="2"/>')
            out.append(f'<rect x="{x-32:.0f}" y="{ly:.0f}" width="64" height="30" rx="8" '
                       f'fill="{MIST}" stroke="{a2}" stroke-width="1"/>')

    elif p == "shield":  # compliance / guardrail
        cx, cy = W / 2, H / 2 - 10
        out.append(f'<path d="M{cx} {cy-120} L{cx+110} {cy-80} L{cx+110} {cy+20} '
                   f'Q{cx+110} {cy+100} {cx} {cy+130} Q{cx-110} {cy+100} {cx-110} {cy+20} '
                   f'L{cx-110} {cy-80} Z" fill="{a1}" opacity="0.18" stroke="{a1}" '
                   f'stroke-width="3" class="svg-draw" pathLength="1"/>')
        for i in range(rnd.randint(2, 4)):
            y = cy - 50 + i * 40
            out.append(f'<line x1="{cx-60}" y1="{y}" x2="{cx+60}" y2="{y}" '
                       f'stroke="{a2}" stroke-width="4" class="svg-draw" pathLength="1"/>')

    elif p == "sankey":  # flow distribution
        n = rnd.randint(3, 4)
        for i in range(n):
            y0 = 90 + i * 70
            spread = rnd.randint(20, 60)
            out.append(f'<path d="M{M} {y0} C{W*0.45:.0f} {y0} {W*0.55:.0f} {y0+spread} '
                       f'{W-M} {y0+spread}" fill="none" stroke="{a1 if i%2==0 else a2}" '
                       f'stroke-width="{rnd.randint(10,20)}" opacity="0.7" '
                       f'class="svg-draw" pathLength="1"/>')

    elif p == "matrix":  # heatmap grid
        rows, cols = rnd.randint(4, 6), rnd.randint(6, 9)
        cw = (W - 2 * M) / cols
        ch = (H - 140) / rows
        for i in range(rows):
            for j in range(cols):
                v = rnd.random()
                col = a1 if v > 0.66 else (a2 if v > 0.36 else MIST)
                out.append(f'<rect x="{M+j*cw:.0f}" y="{80+i*ch:.0f}" width="{cw-4:.0f}" '
                           f'height="{ch-4:.0f}" rx="4" fill="{col}" '
                           f'opacity="{0.5+v*0.5:.2f}" class="svg-draw" pathLength="1"/>')

    elif p == "gauge":  # radial gauge / meter
        cx, cy = W / 2, H * 0.62
        r = rnd.randint(120, 150)
        n = rnd.randint(9, 14)
        filled = rnd.randint(2, n - 2)
        for i in range(n):
            a = math.pi - i * math.pi / (n - 1)
            x1 = cx + r * math.cos(a); y1 = cy - r * math.sin(a)
            x2 = cx + (r + 26) * math.cos(a); y2 = cy - (r + 26) * math.sin(a)
            out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                       f'stroke="{a1 if i < filled else MIST}" stroke-width="8" '
                       f'class="svg-draw" pathLength="1"/>')

    elif p == "hierarchy":  # org / tree
        out.append(f'<rect x="{W/2-55:.0f}" y="80" width="110" height="46" rx="10" '
                   f'fill="{a1}" stroke="{INK}" stroke-width="1.2" class="svg-draw" pathLength="1"/>')
        n = rnd.randint(3, 5)
        gap = (W - 2 * M) / n
        for i in range(n):
            x = M + i * gap + gap / 2
            out.append(f'<line x1="{W/2:.0f}" y1="126" x2="{x:.0f}" y2="230" '
                       f'stroke="{MIST}" stroke-width="2"/>')
            out.append(f'<rect x="{x-45:.0f}" y="230" width="90" height="44" rx="9" '
                       f'fill="{a2 if i%2 else a1}" stroke="{INK}" stroke-width="1" '
                       f'class="svg-draw" pathLength="1"/>')

    elif p == "scatter":  # scatter with trend
        n = rnd.randint(12, 20)
        pts = [(rnd.randint(M + 20, W - M - 20), rnd.randint(90, H - M - 10)) for _ in range(n)]
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        out.append(f'<line x1="{M}" y1="{H-M}" x2="{W-M}" y2="{H-M}" stroke="{SLATE}" stroke-width="2"/>')
        out.append(f'<line x1="{M}" y1="{H-M}" x2="{M}" y2="80" stroke="{SLATE}" stroke-width="2"/>')
        for k, (x, y) in enumerate(pts):
            r = rnd.randint(6, 12)
            out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{a1 if k%3 else a2}" '
                       f'opacity="0.85" class="svg-draw" pathLength="1"/>')

    elif p == "loop":  # cyclical process
        cx, cy = W / 2, H / 2 - 10
        r = rnd.randint(100, 130)
        n = rnd.randint(4, 6)
        for i in range(n):
            a0 = -math.pi / 2 + i * 2 * math.pi / n
            a_end = a0 + 2 * math.pi / n * 0.72
            x0 = cx + r * math.cos(a0); y0 = cy + r * math.sin(a0)
            x1 = cx + r * math.cos(a_end); y1 = cy + r * math.sin(a_end)
            out.append(f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}" '
                       f'fill="none" stroke="{a1 if i%2==0 else a2}" stroke-width="14" '
                       f'class="svg-draw" pathLength="1"/>')

    elif p == "stack":  # stacked columns
        n = rnd.randint(4, 6)
        gap = (W - 2 * M) / n
        for i in range(n):
            x = M + i * gap + gap * 0.15
            wd = gap * 0.7
            y = H - 80
            for k in range(rnd.randint(2, 4)):
                h = rnd.randint(24, 56)
                y -= h
                out.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{wd:.0f}" height="{h}" '
                           f'fill="{a1 if (i+k)%2==0 else a2}" opacity="0.9" '
                           f'class="svg-draw" pathLength="1" stroke="{INK}" stroke-width="0.8"/>')

    else:  # radar
        cx, cy = W / 2, H / 2 - 10
        r = rnd.randint(110, 140)
        n = rnd.randint(5, 8)
        for ring in (0.4, 0.7, 1.0):
            pts = " ".join(f"{cx+r*ring*math.cos(-math.pi/2+i*2*math.pi/n):.1f},"
                           f"{cy+r*ring*math.sin(-math.pi/2+i*2*math.pi/n):.1f}" for i in range(n))
            out.append(f'<polygon points="{pts}" fill="none" stroke="{MIST}" stroke-width="1.5"/>')
        vals = [rnd.uniform(0.35, 1.0) for _ in range(n)]
        pts = " ".join(f"{cx+r*v*math.cos(-math.pi/2+i*2*math.pi/n):.1f},"
                       f"{cy+r*v*math.sin(-math.pi/2+i*2*math.pi/n):.1f}" for i, v in enumerate(vals))
        out.append(f'<polygon points="{pts}" fill="{a1}" opacity="0.28" stroke="{a1}" '
                   f'stroke-width="2.5" class="svg-draw" pathLength="1"/>')
    return out


def make_svg(slug, section=""):
    seed = seed_of(slug)
    rnd = random.Random(seed)
    # topic-weighted prototype choice, but still varied within topic
    pool = SECTION_PROTO.get(section, DEFAULT_PROTOS)
    idx = pool[seed % len(pool)]
    a1, a2 = PAIRS[(seed // 7) % len(PAIRS)]
    bg = background(random.Random(seed ^ 0x5bd1e995), a1, a2)
    shapes = proto_shapes(idx, rnd, a1, a2)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'role="img" preserveAspectRatio="xMidYMid meet">'
        + bg + "".join(shapes) +
        f'<text x="{M}" y="{H-22}" font-family="system-ui,Segoe UI,Arial,sans-serif" '
        f'font-size="13" fill="{SLATE}">Beehive Strategy · conceptual diagram</text>'
        f'</svg>')


def slug_sections():
    """All slugs referenced by articles, with their section."""
    slugs = {}
    for d in ART_DIRS:
        for p in d.glob("*.html"):
            txt = p.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"/assets/blog/svg/([^\"]+)\.svg", txt)
            if not m:
                continue
            slug = m.group(1)
            sm = re.search(r'"articleSection"\s*:\s*"([^"]+)"', txt)
            slugs.setdefault(slug, sm.group(1) if sm else "")
    # include orphan svg files too
    for p in SVG_DIR.glob("*.svg"):
        slugs.setdefault(p.stem, "")
    return slugs


def main():
    mode = "--apply" if "--apply" in sys.argv else "--sample"
    slugs = slug_sections()
    print("slugs:", len(slugs), "mode:", mode)
    if mode == "--sample":
        # spread across sections and prototypes
        items = sorted(slugs.items())
        picks = [items[i] for i in range(0, len(items), max(1, len(items) // 24))][:24]
        cols = 4
        cw, ch = 400, 245
        sheet = Image.new("RGB", (cols * cw, ((len(picks) + cols - 1) // cols) * ch), "white")
        for i, (slug, sec) in enumerate(picks):
            svg = make_svg(slug, sec)
            try:
                import cairosvg
                png = cairosvg.svg2png(bytestring=svg.encode(), output_width=cw - 10, output_height=225)
                import io
                im = Image.open(io.BytesIO(png)).convert("RGB")
                sheet.paste(im, ((i % cols) * cw + 5, (i // cols) * ch))
            except Exception:
                draw = ImageDraw.Draw(sheet)
                draw.text(((i % cols) * cw + 10, (i // cols) * ch + 10),
                          f"{PROTOS[SECTION_PROTO.get(sec, DEFAULT_PROTOS)[seed_of(slug) % len(SECTION_PROTO.get(sec, DEFAULT_PROTOS))]]} | {sec[:14]}",
                          fill="black")
        out = Path("/tmp/article_hero_contact.png")
        sheet.save(out)
        print("contact sheet:", out)
    else:
        SVG_DIR.mkdir(parents=True, exist_ok=True)
        for i, (slug, sec) in enumerate(sorted(slugs.items())):
            (SVG_DIR / (slug + ".svg")).write_text(make_svg(slug, sec), encoding="utf-8")
            if (i + 1) % 200 == 0:
                print("  rendered", i + 1)
        print("done:", len(slugs), "->", SVG_DIR)


if __name__ == "__main__":
    from PIL import Image, ImageDraw
    main()
