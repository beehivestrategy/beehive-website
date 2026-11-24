#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_article_diagrams.py — CONTENT-DERIVED article diagrams (v6).

Why this exists (Kenneth, 2026-11-21):
  The v4/v5 blog diagrams were abstract decorative shapes (radar, sankey,
  funnel) that looked consistent but said nothing about the article they
  sat in. The brief is a real graph / flowchart / chart / workflow *related
  to the article*. So every diagram is now derived from the article's own
  content:

    numeric table      -> BAR CHART of the real numbers
    comparison table   -> COMPARISON MATRIX of the real rows
    ordered list       -> WORKFLOW of the real steps
    bullet list        -> CAPABILITY LAYERS of the real items
    otherwise          -> CONCEPT MAP of the real H2 headings

Each diagram is generated per locale from that locale's own article body, so
the labels are in the reader's language (EN / zh-CN / zh-HK) with no
translation layer needed.

Output: assets/blog/svg/<locale>/<slug>.svg   (800x450, IBM-blue palette)
Never touches HTML.

Usage:
  python3 gen_article_diagrams.py --sample 20
  python3 gen_article_diagrams.py --apply
  python3 gen_article_diagrams.py --check
"""
import html
import json
import re
import sys
from pathlib import Path

WEB = Path(__file__).resolve().parents[1]
SVG_ROOT = WEB / "assets" / "blog" / "svg"

LOCALES = {
    "en": "",
    "zh-cn": "zh-cn/",
    "zh-hk": "zh-hk/",
}

# --- palette (matches accenture.css :root + legacy-bridge v5) ---------------
INK = "#101828"
SLATE = "#4A5568"
MUTED = "#8B94A8"
MIST = "#dfe5f5"
GRID = "#eef2fb"
BLUE = "#0F62FE"
BLUE_D = "#0043CE"
BLUE_L = "#8fb0ff"
WASH = "#f0f4fe"

W, H = 800, 450
M = 60

LATIN = "system-ui,-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
CJK = ("system-ui,-apple-system,PingFang SC,Hiragino Sans GB,"
       "Microsoft YaHei,Noto Sans CJK SC,Helvetica,Arial,sans-serif")
FONT = CJK  # CJK-capable stack also renders Latin fine

# --- HTML extraction --------------------------------------------------------
RE_MAIN = re.compile(r"<main\b[^>]*>([\s\S]*?)</main>", re.I)
RE_ARTICLE_BLOCK = re.compile(
    r'<article\b([^>]*)>([\s\S]*)', re.I)
# Where the article body ends when the tags are never closed.
RE_ARTICLE_END = re.compile(
    r'</?(?:footer|recommended-section|article-nav|script)\b', re.I)
RE_TABLE = re.compile(r"<table[^>]*>([\s\S]*?)</table>", re.I)
RE_TH = re.compile(r"<th[^>]*>([\s\S]*?)</th>", re.I)
RE_TD = re.compile(r"<td[^>]*>([\s\S]*?)</td>", re.I)
RE_TR = re.compile(r"<tr[^>]*>([\s\S]*?)</tr>", re.I)
RE_OL = re.compile(r"<ol[^>]*>([\s\S]*?)</ol>", re.I)
RE_UL = re.compile(r"<ul[^>]*>([\s\S]*?)</ul>", re.I)
RE_LI = re.compile(r"<li[^>]*>([\s\S]*?)</li>", re.I)
RE_H2 = re.compile(r"<h2\b[^>]*>([\s\S]*?)</h2>", re.I)
RE_BOLD = re.compile(r"<(?:strong|b)\b[^>]*>([\s\S]*?)</(?:strong|b)>", re.I)
RE_NUM = re.compile(r"(\d+(?:\.\d+)?)\s*%")

# Inline icons are often self-closing (<svg ... />), so a plain
# "<svg ...>...</svg>" pattern would swallow the rest of the article.
SKIP_BLOCK = re.compile(
    r"<script\b[\s\S]*?</script>"
    r"|<style\b[\s\S]*?</style>"
    # Inline icons appear as a bare <svg ...> (never closed) or a paired
    # <svg ...>...</svg>. The paired branch is tempered so it cannot run
    # past a block-level tag to a LATER </svg> — otherwise an unclosed
    # chevron icon swallows every heading after it.
    r"|<svg\b[^>]*>(?:(?!</?(?:h[1-6]|p|div|section|article|main|footer|table|ul|ol|aside|nav)\b)[\s\S])*?</svg>"
    r"|<svg\b[^>]*>"
    r"|<figure\b[\s\S]*?</figure>"
    r"|<nav\b[\s\S]*?</nav>"
    r"|<aside\b[\s\S]*?</aside>", re.I)


def text_of(frag):
    t = re.sub(r"<[^>]+>", " ", frag)
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def body_of(path):
    s = path.read_text(encoding="utf-8", errors="ignore")
    m = RE_MAIN.search(s)
    if m:
        b = m.group(1)
    else:
        # Some older article pages open <main> without ever closing it.
        # Fall back to the article body block so the article still gets a
        # content-derived diagram instead of falling back to the generic one.
        m2 = RE_ARTICLE_BLOCK.search(s)
        if not m2 or "article-content" not in m2.group(1):
            return ""
        rest = m2.group(2)
        # 32 legacy article pages never close <article>/<main>; cut the body
        # at the first trailing block that can only follow the prose.
        em = RE_ARTICLE_END.search(rest)
        b = rest[:em.start()] if em else rest
    b = SKIP_BLOCK.sub(" ", b)
    return b


def parse_table(tbl):
    """Return (header, body_rows). The header row is kept separate so a
    numeric column can be detected from the DATA rows only — including the
    header in that test makes every numeric table look non-numeric."""
    header = []
    rows = []
    for tr in RE_TR.findall(tbl):
        cells = [text_of(c) for c in RE_TD.findall(tr)]
        if not cells:
            ths = [text_of(c) for c in RE_TH.findall(tr)]
            if ths and not header:
                header = ths
            continue
        if cells and any(cells):
            rows.append(cells)
    return header, rows


def table_header(tbl):
    ths = [text_of(t) for t in RE_TH.findall(tbl)]
    return ths if ths else []


def list_items(block, ordered):
    out = []
    for li in RE_LI.findall(block):
        lead = RE_BOLD.search(li)
        label = text_of(lead.group(1)) if lead else ""
        body = text_of(li)
        if label:
            # keep the bold lead, drop it from the body tail
            rest = body[len(label):].lstrip(" .—–-:，、") if body.startswith(label) else body
        else:
            rest = body
        out.append({"label": label, "text": rest or body})
    return out


def clip(s, n):
    s = (s or "").strip()
    return s if len(s) <= n else s[:n - 1].rstrip() + "…"


# Localised chrome for the diagram frames. The DATA comes from the article;
# only these labels are per-locale.
TITLES = {
    "en": {"bar": "By the numbers", "workflow": "How it works",
           "layers": "What it takes", "concept": "The shape of the topic",
           "topic": "TOPIC"},
    "zh-cn": {"bar": "关键数据", "workflow": "运作方式",
              "layers": "落地前提", "concept": "主题结构",
              "topic": "主题"},
    "zh-hk": {"bar": "關鍵數據", "workflow": "運作方式",
              "layers": "落地前提", "concept": "主題結構",
              "topic": "主題"},
}


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# --- text metrics -----------------------------------------------------------
# SVG has no auto-layout, so we measure ourselves. CJK glyphs are full-width,
# Latin averages ~0.52em. Good enough to prevent overflow and clipping.
def char_w(ch, size):
    o = ord(ch)
    if (0x2E80 <= o <= 0x9FFF) or (0xF900 <= o <= 0xFAFF) or \
       (0xFF00 <= o <= 0xFF60) or (0x3000 <= o <= 0x303F):
        return size * 1.0
    if ch in "iljI.,:;'|!()[]":
        return size * 0.30
    if ch in "mwMW@":
        return size * 0.86
    if ch == " ":
        return size * 0.28
    return size * 0.53


def text_w(s, size):
    return sum(char_w(c, size) for c in (s or ""))


def fit(s, size, max_w):
    """Truncate to fit max_w, appending an ellipsis when cut."""
    s = (s or "").strip()
    if text_w(s, size) <= max_w:
        return s
    out = ""
    for ch in s:
        if text_w(out + ch + "…", size) > max_w:
            break
        out += ch
    return (out.rstrip() + "…") if out else ""


def wrap(s, size, max_w, max_lines=4):
    """Greedy wrap that respects CJK (break anywhere) and Latin (break on space)."""
    s = re.sub(r"\s+", " ", (s or "").strip())
    if not s:
        return []
    tokens = []
    buf = ""
    for ch in s:
        if char_w(ch, size) >= size * 0.9:      # CJK -> own token
            if buf:
                tokens.append(buf)
                buf = ""
            tokens.append(ch)
        elif ch == " ":
            if buf:
                tokens.append(buf)
                buf = ""
        else:
            buf += ch
    if buf:
        tokens.append(buf)

    lines, cur = [], ""
    for t in tokens:
        cand = (cur + " " + t).strip() if cur and t != " " else cur + t
        if text_w(cand, size) <= max_w or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = t
            if len(lines) >= max_lines:
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    if len(lines) == max_lines:
        last = lines[-1]
        if text_w(last, size) > max_w:
            lines[-1] = fit(last, size, max_w)
    return lines


# --- diagram model ----------------------------------------------------------
def candidates(body):
    """All diagram specs this body can support, in priority order.

    Each candidate is (type, structural_index, spec). The structural index
    identifies WHICH table / list was used, so another locale can be matched
    to the same position even when its content shape differs.
    """
    out = []

    for ti, tbl in enumerate(RE_TABLE.findall(body)):
        header, rows = parse_table(tbl)
        if len(rows) < 3:
            continue
        # numeric column -> bar chart (data rows only)
        for col in range(1, len(rows[0])):
            vals = []
            ok = True
            for r in rows:
                if col >= len(r):
                    ok = False
                    break
                m = RE_NUM.search(r[col])
                if not m:
                    ok = False
                    break
                vals.append(float(m.group(1)))
            if ok and len(vals) >= 3 and max(vals) > 0:
                labels = [r[0] for r in rows]
                out.append(("bar", ti, {
                    "type": "bar",
                    "title": None,          # filled per locale
                    "labels": [clip(l, 26) for l in labels],
                    "values": vals,
                    "axis": clip(header[col] if col < len(header) else "", 26),
                }))
                break
        # multi-column comparison -> matrix
        if len(rows[0]) >= 3 and len(header) >= 3:
            # ragged tables: keep only rows that carry all three columns
            wide = [r for r in rows if len(r) >= 3]
            if len(wide) >= 3:
                out.append(("matrix", ti, {
                    "type": "matrix",
                    "title": clip(header[1], 22),
                    "subtitle": clip(header[2], 22),
                    "rows": [clip(r[0], 30) for r in wide],
                    "left": [clip(r[1], 34) for r in wide],
                    "right": [clip(r[2], 34) for r in wide],
                }))

    for oi, block in enumerate(RE_OL.findall(body)):
        items = list_items(block, True)
        if len(items) >= 3:
            out.append(("workflow", oi, {
                "type": "workflow",
                "title": None,
                "steps": [(clip(i["label"] or i["text"], 30),
                           clip(i["text"], 78)) for i in items[:5]],
            }))

    best, best_i = [], -1
    for ui, block in enumerate(RE_UL.findall(body)):
        items = list_items(block, False)
        if len(items) > len(best):
            best, best_i = items, ui
    if len(best) >= 3:
        layers = []
        for i in best[:4]:
            label = i["label"]
            body_txt = i["text"]
            # Chinese lists rarely use a bold lead-in: when the "detail"
            # repeats the label, show the text once.
            if not label or body_txt.startswith(label):
                label = ""
                body_txt = i["text"]
            layers.append((clip(label, 28), clip(body_txt, 70)))
        out.append(("layers", best_i, {
            "type": "layers",
            "title": None,
            "layers": layers,
        }))

    h2s = [clip(text_of(h), 40) for h in RE_H2.findall(body)]
    if len(h2s) >= 3:
        out.append(("concept", 0, {
            "type": "concept",
            "title": None,
            "nodes": h2s[:5],
        }))
    return out


# Fallback chain when a locale is missing the EN article's structure.
FALLBACK = {
    "bar":    ["bar", "matrix", "workflow", "layers", "concept"],
    "matrix": ["matrix", "workflow", "layers", "concept"],
    "workflow": ["workflow", "layers", "concept"],
    "layers": ["layers", "workflow", "concept"],
    "concept": ["concept"],
}


def choose(cands, want_type=None, want_index=None):
    """Pick a candidate, preferring the EN article's type and position."""
    if not cands:
        return None
    if want_type:
        same = [c for c in cands if c[0] == want_type]
        if same:
            if want_index is not None:
                exact = [c for c in same if c[1] == want_index]
                if exact:
                    return exact[0]
            return same[0]
        for alt in FALLBACK.get(want_type, []):
            pool = [c for c in cands if c[0] == alt]
            if pool:
                return pool[0]
    return cands[0]


def analyse(body):
    """Backward-compatible single-spec view of a body."""
    c = candidates(body)
    return c[0][2] if c else None


# --- SVG rendering ----------------------------------------------------------
def svg_open(bg_kind=0):
    stops = [("#ffffff", "#f0f4fe"), ("#fafcff", "#eef1f8"),
             ("#ffffff", "#f4f7fe"), ("#fbfcff", "#f0f4fe")][bg_kind % 4]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'role="img" preserveAspectRatio="xMidYMid meet">',
        f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0.4" y2="1">'
        f'<stop offset="0" stop-color="{stops[0]}"/>'
        f'<stop offset="1" stop-color="{stops[1]}"/></linearGradient></defs>',
        f'<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>',
    ]
    step = 48
    for x in range(0, W, step):
        parts.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" '
                     f'stroke="{GRID}" stroke-width="1"/>')
    for y in range(0, H, step):
        parts.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" '
                     f'stroke="{GRID}" stroke-width="1"/>')
    return "".join(parts)


def txt(x, y, s, size=15, fill=SLATE, weight=400, anchor="start",
        family=None, spacing=None):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    f = f' font-family="{family or FONT}"'
    w = f' font-weight="{weight}"' if weight != 400 else ""
    sp = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" '
            f'fill="{fill}"{f}{w}{a}{sp}>{esc(s)}</text>')


def footer(s):
    return txt(M, H - 20, "Beehive Strategy", 12, MUTED)


def render_bar(spec, bg):
    parts = [svg_open(bg)]
    labels = spec["labels"]
    values = spec["values"]
    n = len(values)
    plot_l, plot_r = M + 150, W - M - 30
    plot_t, plot_b = 96, H - 78
    mx = max(values) or 1
    gap = 16
    bw = (plot_r - plot_l - gap * (n - 1)) / n
    parts.append(txt(M, 62, fit(spec["title"], 19, 380), 19, INK, 700))
    if spec.get("axis"):
        parts.append(txt(plot_r, 62, fit(spec["axis"], 12, 160), 12, MUTED,
                         400, "end"))
    parts.append(f'<line x1="{plot_l}" y1="{plot_b}" x2="{plot_r}" y2="{plot_b}" '
                 f'stroke="{MIST}" stroke-width="1.5"/>')
    for g in range(1, 4):
        gy = plot_b - (plot_b - plot_t) * g / 4
        parts.append(f'<line x1="{plot_l}" y1="{gy:.0f}" x2="{plot_r}" '
                     f'y2="{gy:.0f}" stroke="{GRID}" stroke-width="1"/>')
        parts.append(txt(plot_l - 8, gy + 4, f"{mx * g / 4:.0f}%", 11, MUTED,
                         400, "end"))
    for i, v in enumerate(values):
        x = plot_l + i * (bw + gap)
        bh = (plot_b - plot_t) * (v / mx)
        col = BLUE if i % 2 == 0 else BLUE_D
        parts.append(f'<rect x="{x:.0f}" y="{plot_b - bh:.0f}" width="{bw:.0f}" '
                     f'height="{bh:.0f}" rx="4" fill="{col}"/>')
        parts.append(txt(x + bw / 2, plot_b - bh - 8, f"{v:g}%", 12, INK, 700,
                         "middle"))
        # category label wrapped under the bar
        lines = wrap(labels[i], 10.5, bw, max_lines=2)
        for li, ln in enumerate(lines):
            parts.append(txt(x + bw / 2, plot_b + 20 + li * 13, ln, 10.5, SLATE,
                             400, "middle"))
    parts.append(footer(spec["title"]))
    parts.append("</svg>")
    return "".join(parts)


def render_matrix(spec, bg):
    parts = [svg_open(bg)]
    parts.append(txt(M, 58, fit(spec["title"], 19, 300), 19, INK, 700))
    parts.append(txt(M, 78, fit(spec["subtitle"], 13, 300), 13, BLUE, 600))
    top = 106
    col_l, col_r = M + 190, W - M
    box_w = 168
    rows = spec["rows"]
    rh = 46
    for i, row in enumerate(rows):
        y = top + i * rh
        if i % 2 == 0:
            parts.append(f'<rect x="{M - 10}" y="{y - 22}" width="{W - 2 * M + 20}" '
                         f'height="{rh}" rx="6" fill="#ffffff" opacity="0.72"/>')
        parts.append(txt(M, y, fit(row, 12.5, 176), 12.5, INK, 600))
        parts.append(txt(col_l, y, fit(spec["left"][i], 12, 150), 12, SLATE))
        parts.append(f'<line x1="{col_l - 12}" y1="{y - 5}" x2="{col_l - 12}" '
                     f'y2="{y + 7}" stroke="{MIST}" stroke-width="1.5"/>')
        parts.append(f'<rect x="{col_r - box_w}" y="{y - 17}" width="{box_w}" '
                     f'height="26" rx="6" fill="{WASH}" stroke="{BLUE_L}" '
                     f'stroke-width="1"/>')
        parts.append(txt(col_r - box_w + 10, y,
                         fit(spec["right"][i], 11.5, box_w - 20), 11.5, BLUE_D,
                         600))
    parts.append(footer(spec["title"]))
    parts.append("</svg>")
    return "".join(parts)


def render_workflow(spec, bg):
    parts = [svg_open(bg)]
    parts.append(txt(M, 58, fit(spec["title"], 19, 380), 19, INK, 700))
    steps = spec["steps"]
    n = len(steps)
    gap = 16
    box_w = (W - 2 * M - gap * (n - 1)) / n
    y0, bh = 108, 196
    for i, (label, body) in enumerate(steps):
        x = M + i * (box_w + gap)
        col = BLUE if i % 2 == 0 else BLUE_D
        parts.append(f'<rect x="{x:.0f}" y="{y0}" width="{box_w:.0f}" '
                     f'height="{bh}" rx="10" fill="#ffffff" stroke="{MIST}" '
                     f'stroke-width="1.5"/>')
        parts.append(f'<rect x="{x:.0f}" y="{y0}" width="{box_w:.0f}" '
                     f'height="4" rx="2" fill="{col}"/>')
        parts.append(f'<circle cx="{x + 20:.0f}" cy="{y0 + 30:.0f}" r="13" '
                     f'fill="{col}"/>')
        parts.append(txt(x + 20, y0 + 35, str(i + 1), 13, "#ffffff", 700,
                         "middle"))
        # step title wrapped to 2 lines beside the number badge
        title_lines = wrap(label, 12.5, box_w - 62, max_lines=2)
        for li, ln in enumerate(title_lines):
            parts.append(txt(x + 40, y0 + 26 + li * 15, ln, 12.5, INK, 700))
        # body wrapped to 4 lines under the badge
        body_lines = wrap(body, 10.5, box_w - 28, max_lines=4)
        for li, ln in enumerate(body_lines):
            parts.append(txt(x + 14, y0 + 66 + li * 15, ln, 10.5, SLATE))
        if i < n - 1:
            ax = x + box_w + 2
            parts.append(f'<path d="M{ax:.0f} {y0 + bh / 2:.0f} '
                         f'l{11} 7 l-11 7 z" fill="{BLUE_L}"/>')
    parts.append(footer(spec["title"]))
    parts.append("</svg>")
    return "".join(parts)


def render_layers(spec, bg):
    parts = [svg_open(bg)]
    parts.append(txt(M, 58, fit(spec["title"], 19, 380), 19, INK, 700))
    layers = spec["layers"]
    n = len(layers)
    top = 92
    lh = (H - 92 - 44) / n
    for i, (label, body) in enumerate(layers):
        y = top + i * lh
        col = [BLUE, BLUE_D, BLUE_L, "#6f9bff"][i % 4]
        parts.append(f'<rect x="{M}" y="{y:.0f}" width="{W - 2 * M}" '
                     f'height="{lh - 12:.0f}" rx="9" fill="#ffffff" '
                     f'stroke="{MIST}" stroke-width="1.5"/>')
        parts.append(f'<rect x="{M}" y="{y:.0f}" width="5" '
                     f'height="{lh - 12:.0f}" rx="2.5" fill="{col}"/>')
        parts.append(txt(M + 20, y + 26, fit(label, 13.5, 300), 13.5, INK, 700))
        parts.append(txt(M + 20, y + 46, fit(body, 11.5, W - 2 * M - 40), 11.5,
                         SLATE))
    parts.append(footer(spec["title"]))
    parts.append("</svg>")
    return "".join(parts)


def render_concept(spec, bg):
    parts = [svg_open(bg)]
    parts.append(txt(M, 58, fit(spec["title"], 19, 380), 19, INK, 700))
    nodes = spec["nodes"]
    n = len(nodes)
    import math
    cx, cy = W / 2, H / 2 + 16
    parts.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="46" fill="{WASH}" '
                 f'stroke="{BLUE_L}" stroke-width="2"/>')
    parts.append(txt(cx, cy - 4, spec.get("topic_label", "TOPIC"), 11, BLUE, 700, "middle"))
    parts.append(txt(cx, cy + 16, fit(nodes[0], 11, 76), 11, INK, 600, "middle"))
    rest = nodes[1:]
    if rest:
        k = len(rest)
        for i, nlab in enumerate(rest):
            ang = -math.pi / 2 + i * (2 * math.pi / k)
            nx = cx + math.cos(ang) * 195
            ny = cy + math.sin(ang) * 118
            parts.append(f'<line x1="{cx:.0f}" y1="{cy:.0f}" x2="{nx:.0f}" '
                         f'y2="{ny:.0f}" stroke="{MIST}" stroke-width="2"/>')
            parts.append(f'<rect x="{nx - 95:.0f}" y="{ny - 21:.0f}" '
                         f'width="190" height="42" rx="8" fill="#ffffff" '
                         f'stroke="{BLUE_L}" stroke-width="1.5"/>')
            for li, ln in enumerate(wrap(nlab, 11.5, 172, max_lines=2)):
                parts.append(txt(nx, ny - 1 + li * 13, ln, 11.5, INK, 600,
                                 "middle"))
    parts.append(footer(spec["title"]))
    parts.append("</svg>")
    return "".join(parts)


RENDERERS = {
    "bar": render_bar,
    "matrix": render_matrix,
    "workflow": render_workflow,
    "layers": render_layers,
    "concept": render_concept,
}


def build(body, seed, locale="en"):
    """Return (spec, svg) with the locale's own frame titles applied."""
    cands = candidates(body)
    if not cands:
        return None, None
    spec = dict(cands[0][2])
    t = TITLES.get(locale, TITLES["en"])
    if spec.get("title") is None:
        spec["title"] = t.get(spec["type"], "")
    spec["topic_label"] = t.get("topic", "TOPIC")
    return spec, RENDERERS[spec["type"]](spec, seed % 4)


def main():
    argv = sys.argv[1:]
    apply_ = "--apply" in argv
    check = "--check" in argv
    sample = None
    if "--sample" in argv:
        sample = int(argv[argv.index("--sample") + 1])

    # EN is the structural source of truth: the diagram TYPE is decided from
    # the English body (which carries the richest tables/lists), then every
    # locale renders the same type using its OWN labels. A locale missing the
    # English structure falls back along FALLBACK so the page still has a
    # relevant diagram rather than an empty slot.
    en_dir = WEB / "blog" / "articles"
    en_cands = {}
    for p in sorted(en_dir.glob("*.html")):
        b = body_of(p)
        if b:
            en_cands[p.stem] = candidates(b)

    stats = {}
    written = 0
    for loc, prefix in LOCALES.items():
        art_dir = WEB / prefix / "blog" / "articles"
        out_dir = SVG_ROOT / loc
        if not art_dir.is_dir():
            continue
        files = sorted(art_dir.glob("*.html"))
        if sample:
            files = files[:sample]
        types = {}
        for i, p in enumerate(files):
            body = body_of(p)
            if not body:
                continue
            ref = en_cands.get(p.stem)
            want_type, want_index = None, None
            if ref:
                want_type, want_index = ref[0][0], ref[0][1]
            picked = choose(candidates(body), want_type, want_index)
            if not picked:
                types["none"] = types.get("none", 0) + 1
                continue
            spec = dict(picked[2])
            t = TITLES.get(loc, TITLES["en"])
            if spec.get("title") is None:
                spec["title"] = t.get(spec["type"], "")
            spec["topic_label"] = t.get("topic", "TOPIC")
            key = spec["type"] + ("" if want_type == spec["type"]
                                  else " (fallback)")
            types[key] = types.get(key, 0) + 1
            if apply_:
                svg = RENDERERS[spec["type"]](spec, i % 4)
                out_dir.mkdir(parents=True, exist_ok=True)
                (out_dir / (p.stem + ".svg")).write_text(svg, encoding="utf-8")
                written += 1
        stats[loc] = types
        print(f"{loc}: " + ", ".join(f"{k}={v}" for k, v in sorted(types.items())))

    if apply_:
        print("written:", written, "svg files")
    elif check:
        print("(check only — no files written)")


if __name__ == "__main__":
    main()
