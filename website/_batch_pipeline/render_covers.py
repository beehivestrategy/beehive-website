#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_covers.py — Regenerate Beehive Strategy blog OG/article covers.

Design goals (vs. the old monotone template):
  * Brand-consistent: deep teal/near-black gradient, gold accent, honeycomb (Beehive) motif.
  * Editorial hierarchy: wordmark + category pill + large bold title + data-viz accent.
  * One asset, two uses: serves as OG image AND the on-page article hero.

Render path: build a standalone HTML per slug, screenshot with headless Chrome
to a 1200x630 JPG. No external network needed (system fonts).

Usage:
  python3 render_covers.py            # render the PRIORITY slugs below
  python3 render_covers.py slug1 slug2 ...
"""
import os, re, sys, html, subprocess, shutil

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
ART = os.path.join(ROOT, "blog", "articles")
COVER_EN = os.path.join(ROOT, "assets", "blog", "covers", "en")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

PRIORITY = [
    "real-time-data-streaming-conversational-analytics-platform",
    "what-is-mcp-model-context-protocol-explained",
    "semantic-layer-conversational-bi-self-service-analytics",
    "self-service-bi-maturity-model-2025",
    "data-marketplace-enterprise-data-monetization-strategy",
    "quantum-machine-learning-hype-vs-reality-for-business-a-2026-update",
    "conversational-analytics-nlg-automated-insight-reports",
]

# ---- honeycomb SVG (Beehive motif), reused as decorative layers -------------
HEX_MARK = (
    '<svg class="mark" viewBox="0 0 40 44" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M20 1 L37 11 V31 L20 43 L3 31 V11 Z" stroke="#d4a843" stroke-width="3" fill="rgba(212,168,67,0.12)"/>'
    '<path d="M20 11 L29 16.5 V27.5 L20 33 L11 27.5 V16.5 Z" stroke="#2B9E8B" stroke-width="2" fill="none"/></svg>'
)
HEX_BIG = (
    '<svg class="bighex" viewBox="0 0 200 220" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M100 5 L185 60 V170 L100 215 L15 170 V60 Z" stroke="#2B9E8B" stroke-width="2" fill="none"/>'
    '<path d="M100 35 L160 70 V150 L100 185 L40 150 V70 Z" stroke="#d4a843" stroke-width="1.5" fill="none"/></svg>'
)
SPARK = (
    '<svg class="spark" viewBox="0 0 340 46" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<polyline points="0,38 45,30 90,33 135,18 180,22 225,10 270,15 315,5 340,9" stroke="#d4a843" stroke-width="2.5" fill="none"/>'
    '<polyline points="0,38 45,30 90,33 135,18 180,22 225,10 270,15 315,5 340,9 340,46 0,46" fill="rgba(212,168,67,0.08)" stroke="none"/>'
    '<circle cx="315" cy="5" r="4" fill="#2B9E8B"/></svg>'
)

CSS = """
@page { size: 1200px 630px; }
* { margin:0; padding:0; box-sizing:border-box; }
html,body { width:1200px; height:630px; }
body {
  position:relative; overflow:hidden; width:1200px; height:630px;
  background:
    radial-gradient(1100px 620px at 88% 12%, rgba(43,158,139,0.22), transparent 60%),
    radial-gradient(900px 520px at 8% 112%, rgba(212,168,67,0.10), transparent 55%),
    linear-gradient(135deg, #0a0e0d 0%, #0c1a18 46%, #091312 100%);
  color:#ffffff;
  font-family:'Helvetica Neue', Helvetica, Arial, 'PingFang SC', sans-serif;
}
.hexgrid { position:absolute; inset:0; opacity:0.05; }
.wordmark { position:absolute; top:40px; left:56px; display:flex; align-items:center; gap:14px; }
.mark { width:34px; height:38px; display:block; }
.wm-text { font-size:21px; font-weight:700; letter-spacing:0.14em; color:#eef3f4; }
.wm-sub  { font-size:10px; letter-spacing:0.32em; color:#2B9E8B; font-weight:700; margin-top:3px; }
.pill { position:absolute; top:152px; left:56px; display:inline-block; background:#d4a843; color:#0a0e0d;
        font-size:14px; font-weight:700; letter-spacing:0.10em; text-transform:uppercase;
        padding:8px 18px; border-radius:999px; }
.title { position:absolute; top:212px; left:56px; right:56px; max-width:920px;
         font-size:54px; line-height:1.12; font-weight:700; color:#ffffff; letter-spacing:-0.01em; }
.title .hl { color:#5fd0bd; }
.rule { position:absolute; left:56px; bottom:70px; width:1088px; height:2px;
        background:linear-gradient(90deg, rgba(212,168,67,0.95), rgba(43,158,139,0.18)); }
.spark { position:absolute; left:56px; bottom:84px; width:360px; height:46px; }
.foot { position:absolute; right:56px; bottom:44px; font-size:12px; color:rgba(238,243,244,0.5);
        letter-spacing:0.10em; }
.bighex { position:absolute; right:-90px; top:-90px; width:300px; height:330px; opacity:0.06; }
"""

TEMPLATE = """<!doctype html><html lang="en"><head><meta charset="utf-8"><style>{css}</style></head>
<body>
  <div class="hexgrid">{hexgrid}</div>
  {bighex}
  <div class="wordmark">{mark}<div><div class="wm-text">BEEHIVE STRATEGY</div><div class="wm-sub">DATA &amp; AI ADVISORY</div></div></div>
  <div class="pill">{category}</div>
  <div class="title">{title}</div>
  <div class="rule"></div>
  {spark}
  <div class="foot">beehivestrategy.com &middot; Enterprise AI &amp; Analytics</div>
</body></html>"""


def wrap_title(title, max_chars=29, max_lines=4):
    words = title.split()
    lines, i = [], 0
    while i < len(words) and len(lines) < max_lines:
        line = words[i]; i += 1
        while i < len(words) and len(line) + 1 + len(words[i]) <= max_chars:
            line += " " + words[i]; i += 1
        lines.append(line)
    if i < len(words) and len(lines) == max_lines:
        last = lines[-1]
        if len(last) > max_chars - 1:
            lines[-1] = last[:max_chars - 2].rstrip() + "\u2026"
    return "<br>".join(html.escape(l) for l in lines)


def highlight(title_html):
    # gentle accent: colour the word "AI" or the final token cluster; keep simple -> no-op wrap safe
    return title_html


def parse_article(slug):
    path = os.path.join(ART, slug + ".html")
    with open(path, encoding="utf-8", errors="replace") as f:
        txt = f.read()
    m = re.search(r"<title>(.*?)</title>", txt, re.S)
    title = m.group(1).strip() if m else slug
    title = re.sub(r"\s+", " ", title)
    c = re.search(r'<meta property="article:section" content="([^"]*)"', txt)
    category = c.group(1).strip() if c else "Insights"
    return title, category


def build_html(slug):
    title, category = parse_article(slug)
    # small honeycomb grid pattern (repeating hex outlines) as faint background
    hex_cell = ('<svg width="120" height="104" viewBox="0 0 120 104"><path d="M60 2 L116 32 V72 L60 102 L4 72 V32 Z" '
                'stroke="#2B9E8B" stroke-width="1.5" fill="none"/></svg>')
    grid = "".join(hex_cell for _ in range(72))
    t = wrap_title(title)
    return TEMPLATE.format(css=CSS, hexgrid=grid, bighex=HEX_BIG, mark=HEX_MARK,
                           category=html.escape(category), title=highlight(t), spark=SPARK)


def render(slug):
    htm = build_html(slug)
    tmp = f"/tmp/cover_{slug}.html"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(htm)
    out = os.path.join(COVER_EN, slug + ".jpg")
    cmd = [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu",
           "--force-device-scale-factor=1", "--hide-scrollbars",
           f"--window-size=1200,630", f"--screenshot={out}", f"file://{tmp}"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        print(f"  [FAIL] {slug}: chrome rc={r.returncode}\n{r.stderr[-300:]}", file=sys.stderr)
        return None
    return out


def verify(out):
    try:
        from PIL import Image
        with Image.open(out) as im:
            return im.size
    except Exception:
        return None


def main():
    if not shutil.which(CHROME) and not os.path.exists(CHROME):
        print("Chrome not found at", CHROME, file=sys.stderr); sys.exit(1)
    slugs = sys.argv[1:] or PRIORITY
    print(f"Rendering {len(slugs)} cover(s)...")
    for slug in slugs:
        out = render(slug)
        if out:
            sz = verify(out)
            fsize = os.path.getsize(out) if os.path.exists(out) else 0
            print(f"  [OK] {slug}: {out}  bytes={fsize}  dim={sz}")
        else:
            print(f"  [ERR] {slug}")


if __name__ == "__main__":
    main()
