#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_article_heroes.py — SINGLE SOURCE for every blog diagram (v4).

v4 (2026-11-20, Kenneth): index covers must be the SAME conceptual diagram as
the article hero, with MORE pattern variety, still on the site's light
IBM-blue editorial palette. So:
  - 28 structural prototypes (was 16)
  - 8 subtle pattern grounds (was 5)
  - brand palette: IBM blue primary + muted teal/gold/steel/aqua (no plum/coral)
  - position-aware prototype rotation: no two adjacent cards share a prototype
  - every one of the 1,141 index slugs gets a hero SVG (40 were missing)
  - card covers are rendered FROM these SVGs (see render_hero_covers.js)

Deterministic: same slug (+ section) -> same SVG.
Language-neutral: only the fixed brand footer text.
Only writes assets/blog/svg/<slug>.svg — never touches HTML.

Usage:
  python3 gen_article_heroes.py --sample
  python3 gen_article_heroes.py --apply
"""
import hashlib
import math
import random
import re
import sys
from pathlib import Path

WEB = Path(__file__).resolve().parents[1]
SVG_DIR = WEB / "assets" / "blog" / "svg"
CARD_DIR = WEB / "assets" / "blog" / "cards"
INDEX = WEB / "blog" / "index.html"
ART_DIRS = [WEB / "blog" / "articles", WEB / "zh-cn" / "blog" / "articles",
            WEB / "zh-hk" / "blog" / "articles"]

W, H, M = 800, 450, 60

# Site palette (accenture.css :root) — blue-led, muted supporting tones only
INK = "#101828"
SLATE = "#4A5568"
MIST = "#dfe5f5"        # --border
GRID = "#eef2fb"        # near-invisible grid (--bl-grid-line over white)
TEAL = "#2B9E8B"
GOLD = "#d4a843"
AQUA = "#6cc4b4"
BLUE = "#0F62FE"        # --accent
BLUE_D = "#0043CE"      # --accent-strong
BLUE_L = "#8fb0ff"
STEEL = "#7d94a6"

PAIRS = [
    (BLUE, AQUA), (BLUE, GOLD), (BLUE_D, BLUE_L), (STEEL, AQUA),
    (TEAL, GOLD), (BLUE, STEEL), (BLUE_D, AQUA), (TEAL, BLUE_L),
]

SECTION_PROTO = {
    "Technology":        [0, 5, 8, 12, 14, 16, 22],
    "AI Strategy":       [1, 6, 9, 13, 15, 17, 23],
    "AI Regulation":     [2, 7, 10, 13, 18, 24],
    "Data Governance":   [3, 8, 11, 14, 19, 26],
    "Conversational BI": [4, 9, 12, 15, 20, 25],
    "Analytics":         [4, 8, 11, 15, 20, 22],
    "Industry":          [5, 10, 13, 14, 21, 26],
    "Strategy":          [1, 6, 9, 13, 17, 23],
    "Manufacturing":     [5, 10, 12, 14, 21, 27],
    "Retail":            [4, 7, 11, 15, 19, 25],
    "Financial Services":[6, 8, 11, 13, 18, 24],
    "Digital Transformation":[1, 6, 12, 15, 17, 22],
    "Enterprise AI":     [0, 5, 9, 14, 16, 27],
    "AI Governance":     [2, 7, 10, 13, 18, 24],
    "Data Strategy":     [3, 8, 11, 14, 19, 26],
}
DEFAULT_PROTOS = list(range(28))

PROTOS = [
    "nodes", "funnel", "layers", "flow", "chat", "circuit", "roadmap",
    "shield", "sankey", "matrix", "gauge", "hierarchy", "scatter",
    "loop", "stack", "radar", "braid", "checklist", "bridges", "orbits",
    "terraces", "signals", "wave stacks", "grid path", "pulse rings",
    "stagger", "radial bars", "lanes",
]

# Adjacent-card guard: step coprime with 28 -> cycle all 28 before repeating.
POS_STEP, POS_OFFSET = 11, 5


def seed_of(slug):
    return int(hashlib.md5(slug.encode("utf-8")).hexdigest()[:8], 16)


def index_positions():
    """Slug -> ordinal position in the EN archive index (SSOT for adjacency)."""
    s = INDEX.read_text(encoding="utf-8")
    slugs = list(dict.fromkeys(re.findall(r"/assets/blog/cards/([^\"]+)\.jpg", s)))
    return {slug: i for i, slug in enumerate(slugs)}


def section_for(slug):
    for d in ART_DIRS:
        p = d / (slug + ".html")
        if p.exists():
            m = re.search(r'"articleSection"\s*:\s*"([^"]+)"',
                          p.read_text(encoding="utf-8", errors="ignore"))
            if m:
                return m.group(1)
    return ""


def choose_proto(slug, section="", position=None):
    """Position-driven in the index (no adjacent repeats); topic-weighted elsewhere."""
    if position is not None:
        return (position * POS_STEP + POS_OFFSET) % 28
    pool = SECTION_PROTO.get(section, DEFAULT_PROTOS)
    return pool[seed_of(slug) % len(pool)]


def background(rnd, a1, a2):
    kind = rnd.randrange(8)
    parts = []
    x2 = rnd.choice([0, 1, 0.4])
    y2 = rnd.choice([1, 0, 0.6])
    stops = rnd.choice([
        ("#ffffff", "#f0f4fe"), ("#fbfcff", "#f4f7fe"),
        ("#ffffff", "#eaf2f3"), ("#fafcff", "#eef1f8"),
    ])
    parts.append(
        f'<defs><linearGradient id="bg" x1="0" y1="0" x2="{x2}" y2="{y2}">'
        f'<stop offset="0" stop-color="{stops[0]}"/>'
        f'<stop offset="1" stop-color="{stops[1]}"/></linearGradient></defs>'
        f'<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>')
    if kind == 0:  # plotting grid
        step = rnd.choice([36, 48, 60])
        for x in range(0, W, step):
            parts.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{GRID}" stroke-width="1"/>')
        for y in range(0, H, step):
            parts.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{GRID}" stroke-width="1"/>')
    elif kind == 1:  # dot field
        step = rnd.choice([26, 34, 44])
        for x in range(step // 2, W, step):
            for y in range(step // 2, H, step):
                parts.append(f'<circle cx="{x}" cy="{y}" r="1.6" fill="{MIST}"/>')
    elif kind == 2:  # faint diagonal hatch
        off = rnd.randint(-140, 140)
        for k in range(-2, 14):
            x = off + k * 76
            parts.append(f'<line x1="{x}" y1="{H}" x2="{x+190}" y2="0" stroke="{GRID}" stroke-width="2"/>')
    elif kind == 3:  # corner arcs
        c = rnd.choice([("0", "0"), (W, "0"), ("0", H), (W, H)])
        for r in (90, 140, 190):
            parts.append(f'<circle cx="{c[0]}" cy="{c[1]}" r="{r}" fill="none" '
                         f'stroke="{MIST}" stroke-width="1.5"/>')
    elif kind == 4:  # soft wash blob
        cx = rnd.choice([int(W * .2), int(W * .8)])
        cy = rnd.choice([int(H * .2), int(H * .8)])
        parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rnd.randint(110,180)}" '
                     f'ry="{rnd.randint(80,130)}" fill="{a2}" opacity="0.08"/>')
    elif kind == 5:  # vertical rules
        step = rnd.choice([40, 56, 72])
        for x in range(step // 2, W, step):
            parts.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{GRID}" stroke-width="2"/>')
    elif kind == 6:  # nested corner squares
        cx, cy = rnd.choice([(0, 0), (W, 0), (0, H), (W, H)])
        for r in (70, 120, 170, 220):
            parts.append(f'<rect x="{cx-r if cx==0 else cx}" y="{cy-r if cy==0 else cy}" '
                         f'width="{r}" height="{r}" fill="none" stroke="{GRID}" stroke-width="1.5"/>')
    else:  # tick rail
        y = rnd.choice([54, H - 54])
        for x in range(M, W - M, 28):
            parts.append(f'<line x1="{x}" y1="{y-7}" x2="{x}" y2="{y+7}" stroke="{MIST}" stroke-width="1.5"/>')
    return "".join(parts)


def proto_shapes(idx, rnd, a1, a2):
    p = PROTOS[idx]
    out = []

    if p == "nodes":
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

    elif p == "funnel":
        rows = rnd.randint(3, 5)
        for i in range(rows):
            wd = (W - 2 * M) * (1 - i * (0.10 + (i % 2) * 0.04))
            x = (W - wd) / 2
            y = 80 + i * (250 // rows)
            h = 52
            out.append(f'<path d="M{x:.0f} {y} L{x+wd:.0f} {y} L{x+wd-22:.0f} {y+h} L{x+22:.0f} {y+h} Z" '
                       f'fill="{a1 if i % 2 == 0 else a2}" opacity="{0.88-i*0.10:.2f}" '
                       f'class="svg-draw" pathLength="1" stroke="{INK}" stroke-width="1"/>')

    elif p == "layers":
        n = rnd.randint(3, 5)
        for i in range(n):
            y = 82 + i * (250 // n)
            off = i * rnd.choice([10, 14, 18])
            out.append(f'<rect x="{M+off}" y="{y}" width="{W-2*M-2*off}" height="{rnd.randint(46,58)}" '
                       f'rx="12" fill="{a1 if i%2==0 else a2}" opacity="0.9" '
                       f'class="svg-draw" pathLength="1" stroke="{INK}" stroke-width="1"/>')

    elif p == "flow":
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

    elif p == "chat":
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

    elif p == "circuit":
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

    elif p == "roadmap":
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
                       f'fill="{GRID}" stroke="{a2}" stroke-width="1"/>')

    elif p == "shield":
        cx, cy = W / 2, H / 2 - 10
        out.append(f'<path d="M{cx} {cy-120} L{cx+110} {cy-80} L{cx+110} {cy+20} '
                   f'Q{cx+110} {cy+100} {cx} {cy+130} Q{cx-110} {cy+100} {cx-110} {cy+20} '
                   f'L{cx-110} {cy-80} Z" fill="{a1}" opacity="0.18" stroke="{a1}" '
                   f'stroke-width="3" class="svg-draw" pathLength="1"/>')
        for i in range(rnd.randint(2, 4)):
            y = cy - 50 + i * 40
            out.append(f'<line x1="{cx-60}" y1="{y}" x2="{cx+60}" y2="{y}" '
                       f'stroke="{a2}" stroke-width="4" class="svg-draw" pathLength="1"/>')

    elif p == "sankey":
        n = rnd.randint(3, 4)
        for i in range(n):
            y0 = 90 + i * 70
            spread = rnd.randint(20, 60)
            out.append(f'<path d="M{M} {y0} C{W*0.45:.0f} {y0} {W*0.55:.0f} {y0+spread} '
                       f'{W-M} {y0+spread}" fill="none" stroke="{a1 if i%2==0 else a2}" '
                       f'stroke-width="{rnd.randint(10,20)}" opacity="0.7" '
                       f'class="svg-draw" pathLength="1"/>')

    elif p == "matrix":
        rows, cols = rnd.randint(4, 6), rnd.randint(6, 9)
        cw = (W - 2 * M) / cols
        ch = (H - 140) / rows
        for i in range(rows):
            for j in range(cols):
                v = rnd.random()
                col = a1 if v > 0.66 else (a2 if v > 0.36 else GRID)
                out.append(f'<rect x="{M+j*cw:.0f}" y="{80+i*ch:.0f}" width="{cw-4:.0f}" '
                           f'height="{ch-4:.0f}" rx="4" fill="{col}" '
                           f'opacity="{0.5+v*0.5:.2f}" class="svg-draw" pathLength="1"/>')

    elif p == "gauge":
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

    elif p == "hierarchy":
        out.append(f'<rect x="{W/2-55:.0f}" y="80" width="110" height="46" rx="10" '
                   f'fill="{a1}" stroke="{INK}" stroke-width="1.2" class="svg-draw" pathLength="1"/>')
        n = rnd.randint(3, 5)
        gap = (W - 2 * M) / n
        for i in range(n):
            x = M + i * gap + gap / 2
            out.append(f'<line x1="{W/2:.0f}" y1="126" x2="{x:.0f}" y2="230" stroke="{MIST}" stroke-width="2"/>')
            out.append(f'<rect x="{x-45:.0f}" y="230" width="90" height="44" rx="9" '
                       f'fill="{a2 if i%2 else a1}" stroke="{INK}" stroke-width="1" class="svg-draw" pathLength="1"/>')

    elif p == "scatter":
        n = rnd.randint(12, 20)
        pts = [(rnd.randint(M + 20, W - M - 20), rnd.randint(90, H - M - 10)) for _ in range(n)]
        out.append(f'<line x1="{M}" y1="{H-M}" x2="{W-M}" y2="{H-M}" stroke="{SLATE}" stroke-width="2"/>')
        out.append(f'<line x1="{M}" y1="{H-M}" x2="{M}" y2="80" stroke="{SLATE}" stroke-width="2"/>')
        for k, (x, y) in enumerate(pts):
            r = rnd.randint(6, 12)
            out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{a1 if k%3 else a2}" '
                       f'opacity="0.85" class="svg-draw" pathLength="1"/>')

    elif p == "loop":
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

    elif p == "stack":
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

    elif p == "radar":
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

    elif p == "braid":
        y0, amp = H * 0.46, rnd.randint(38, 66)
        for k in range(3):
            pts = []
            for x in range(M, W - M, 12):
                y = y0 + amp * math.sin((x - M) / 92.0 + k * 2.1)
                pts.append(f"{x},{y:.1f}")
            out.append(f'<polyline points="{" ".join(pts)}" fill="none" '
                       f'stroke="{a1 if k%2==0 else a2}" stroke-width="7" opacity="0.8" '
                       f'class="svg-draw" pathLength="1"/>')

    elif p == "checklist":
        n = rnd.randint(4, 6)
        y = 78
        for i in range(n):
            x = M + rnd.randint(0, 26)
            out.append(f'<rect x="{x}" y="{y}" width="26" height="26" rx="6" fill="{GRID}" '
                       f'stroke="{a1 if i%2==0 else a2}" stroke-width="2.5" class="svg-draw" pathLength="1"/>')
            out.append(f'<line x1="{x+6}" y1="{y+13}" x2="{x+11}" y2="{y+18}" stroke="{a2}" stroke-width="3"/>')
            out.append(f'<line x1="{x+11}" y1="{y+18}" x2="{x+21}" y2="{y+7}" stroke="{a2}" stroke-width="3"/>')
            wd = rnd.randint(230, 430)
            out.append(f'<rect x="{x+42}" y="{y+7}" width="{wd}" height="12" rx="6" fill="{MIST}" opacity="0.9"/>')
            y += 50

    elif p == "bridges":
        n = rnd.randint(3, 5)
        for i in range(n):
            y = 96 + i * 62
            sag = rnd.randint(24, 56)
            out.append(f'<path d="M{M} {y} Q{W/2:.0f} {y+sag} {W-M} {y}" fill="none" '
                       f'stroke="{a1 if i%2==0 else a2}" stroke-width="{rnd.randint(6,11)}" '
                       f'class="svg-draw" pathLength="1" opacity="0.78"/>')
            out.append(f'<circle cx="{M}" cy="{y}" r="5" fill="{INK}" opacity="0.3"/>')
            out.append(f'<circle cx="{W-M}" cy="{y}" r="5" fill="{INK}" opacity="0.3"/>')

    elif p == "orbits":
        cx, cy = W / 2, H / 2 - 8
        for k, rx in enumerate([rnd.randint(90, 120), rnd.randint(150, 180), rnd.randint(220, 250)]):
            ry = rx * rnd.uniform(0.5, 0.72)
            out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry:.0f}" fill="none" '
                       f'stroke="{a1 if k==1 else MIST}" stroke-width="{3 if k==1 else 1.5}"/>')
        for k in range(rnd.randint(3, 5)):
            a = rnd.uniform(0, 2 * math.pi)
            rx = rnd.randint(90, 230)
            x = cx + rx * math.cos(a)
            y = cy + rx * 0.6 * math.sin(a)
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.randint(8,14)}" '
                       f'fill="{a2}" stroke="{INK}" stroke-width="1" class="svg-draw" pathLength="1"/>')

    elif p == "terraces":
        n = rnd.randint(4, 7)
        for i in range(n):
            y = 84 + i * (250 // n)
            wd = (W - 2 * M) * (0.55 + 0.45 * (1 - i / n))
            x = M + (i % 2) * rnd.randint(10, 46)
            out.append(f'<rect x="{x:.0f}" y="{y}" width="{wd:.0f}" height="{rnd.randint(24,34)}" '
                       f'rx="7" fill="{a1 if i%3 else a2}" opacity="0.85" '
                       f'class="svg-draw" pathLength="1"/>')

    elif p == "signals":
        cy = H * 0.52
        for k in range(rnd.randint(4, 7)):
            x = M + 46 + k * ((W - 2 * M - 92) / 6)
            h = rnd.randint(60, 210)
            out.append(f'<line x1="{x:.0f}" y1="{cy-h/2:.0f}" x2="{x:.0f}" y2="{cy+h/2:.0f}" '
                       f'stroke="{a1 if k%2 else a2}" stroke-width="{rnd.randint(8,16)}" '
                       f'stroke-linecap="round" class="svg-draw" pathLength="1"/>')
        out.append(f'<line x1="{M}" y1="{cy:.0f}" x2="{W-M}" y2="{cy:.0f}" stroke="{MIST}" stroke-width="2"/>')

    elif p == "wave stacks":
        for k in range(rnd.randint(3, 5)):
            base = 108 + k * 56
            amp = rnd.randint(16, 34)
            pts = []
            for x in range(M, W - M, 10):
                y = base + amp * math.sin((x - M) / 78.0 + k * 0.9)
                pts.append(f"{x},{y:.1f}")
            out.append(f'<polyline points="{" ".join(pts)}" fill="none" '
                       f'stroke="{a1 if k==0 else a2}" stroke-width="{5 if k==0 else 3}" '
                       f'opacity="0.8" class="svg-draw" pathLength="1"/>')

    elif p == "grid path":
        cols, rows = rnd.randint(5, 8), rnd.randint(4, 6)
        cw = (W - 2 * M) / cols
        ch = (H - 140) / rows
        for x in range(cols):
            for y in range(rows):
                out.append(f'<rect x="{M+x*cw:.0f}" y="{80+y*ch:.0f}" width="{cw-4:.0f}" '
                           f'height="{ch-4:.0f}" rx="4" fill="{GRID}" stroke="{MIST}" stroke-width="1"/>')
        y = rnd.randrange(rows)
        for x in range(cols):
            ny = max(0, min(rows - 1, y + rnd.choice([-1, 0, 0, 1])))
            out.append(f'<rect x="{M+x*cw+2:.0f}" y="{80+ny*ch+2:.0f}" width="{cw-8:.0f}" '
                       f'height="{ch-8:.0f}" rx="4" fill="{a1 if x%2 else a2}" '
                       f'class="svg-draw" pathLength="1" opacity="0.85"/>')
            y = ny

    elif p == "pulse rings":
        cx, cy = W / 2, H / 2 - 12
        for k in range(rnd.randint(3, 5)):
            r = 52 + k * rnd.randint(32, 46)
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" '
                       f'stroke="{a1 if k%2 else a2}" stroke-width="{rnd.randint(5,10)}" '
                       f'opacity="{0.82-k*0.12:.2f}" class="svg-draw" pathLength="1"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="14" fill="{a2}" stroke="{INK}" stroke-width="1.5"/>')

    elif p == "stagger":
        n = rnd.randint(5, 8)
        gap = (W - 2 * M) / n
        for i in range(n):
            x = M + i * gap
            y = rnd.randint(90, 170)
            out.append(f'<rect x="{x:.0f}" y="{y}" width="{gap*0.62:.0f}" height="{rnd.randint(120,210)}" '
                       f'rx="9" fill="{a1 if i%2==0 else a2}" opacity="0.86" '
                       f'class="svg-draw" pathLength="1" stroke="{INK}" stroke-width="0.8"/>')

    elif p == "radial bars":
        cx, cy = W / 2, H / 2 - 10
        n = rnd.randint(16, 26)
        for i in range(n):
            a = -math.pi / 2 + i * 2 * math.pi / n
            r0 = rnd.randint(70, 100)
            r1 = r0 + rnd.randint(40, 110)
            x1, y1 = cx + r0 * math.cos(a), cy + r0 * math.sin(a)
            x2, y2 = cx + r1 * math.cos(a), cy + r1 * math.sin(a)
            out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                       f'stroke="{a1 if i%3 else a2}" stroke-width="7" stroke-linecap="round" '
                       f'class="svg-draw" pathLength="1"/>')

    else:  # lanes
        n = rnd.randint(3, 5)
        for i in range(n):
            y = 96 + i * 62
            out.append(f'<rect x="{M}" y="{y}" width="{W-2*M}" height="24" rx="12" fill="{GRID}"/>')
            x = M + rnd.randint(30, 260)
            wd = rnd.randint(120, 320)
            out.append(f'<rect x="{x}" y="{y}" width="{wd}" height="24" rx="12" '
                       f'fill="{a1 if i%2==0 else a2}" class="svg-draw" pathLength="1" opacity="0.88"/>')
            out.append(f'<circle cx="{x+wd}" cy="{y+12}" r="15" fill="{a2}" stroke="{INK}" stroke-width="1"/>')
    return out


def make_svg(slug, section="", position=None):
    seed = seed_of(slug)
    rnd = random.Random(seed)
    idx = choose_proto(slug, section, position)
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
    """All archive slugs with section; union of index + articles + orphan SVGs."""
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
    idx = INDEX.read_text(encoding="utf-8")
    card_slugs = list(dict.fromkeys(re.findall(r"/assets/blog/cards/([^\"]+)\.jpg", idx)))
    for slug in card_slugs:
        if slug not in slugs:
            slugs[slug] = section_for(slug)
    for p in SVG_DIR.glob("*.svg"):
        slugs.setdefault(p.stem, "")
    return slugs


def main():
    mode = "--apply" if "--apply" in sys.argv else "--sample"
    slugs = slug_sections()
    pos = index_positions()
    print("slugs:", len(slugs), "indexed:", len(pos), "mode:", mode)
    if mode == "--sample":
        items = sorted(slugs.items())
        picks = [items[i] for i in range(0, len(items), max(1, len(items) // 28))][:28]
        cols = 4
        cw, ch = 400, 245
        from PIL import Image, ImageDraw
        sheet = Image.new("RGB", (cols * cw, ((len(picks) + cols - 1) // cols) * ch), "white")
        for i, (slug, sec) in enumerate(picks):
            svg = make_svg(slug, sec, pos.get(slug))
            try:
                import io
                import cairosvg
                png = cairosvg.svg2png(bytestring=svg.encode(), output_width=cw - 10, output_height=225)
                im = Image.open(io.BytesIO(png)).convert("RGB")
                sheet.paste(im, ((i % cols) * cw + 5, (i // cols) * ch))
            except Exception:
                ImageDraw.Draw(sheet).text(
                    ((i % cols) * cw + 10, (i // cols) * ch + 10),
                    f"{PROTOS[choose_proto(slug, sec, pos.get(slug))]} | {sec[:14]}", fill="black")
        out = Path("/tmp/article_hero_contact.png")
        sheet.save(out)
        print("contact sheet:", out)
    else:
        SVG_DIR.mkdir(parents=True, exist_ok=True)
        for i, (slug, sec) in enumerate(sorted(slugs.items())):
            (SVG_DIR / (slug + ".svg")).write_text(
                make_svg(slug, sec, pos.get(slug)), encoding="utf-8")
            if (i + 1) % 200 == 0:
                print("  rendered", i + 1)
        print("done:", len(slugs), "->", SVG_DIR)


if __name__ == "__main__":
    main()
