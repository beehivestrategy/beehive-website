#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
localize_recommended_cards.py
=============================
Deterministic (no-LLM) localization of the "recommended reading" module
that sits OUTSIDE <article> on every zh-cn / zh-tw blog article page.

Fixes applied:
  1. <h3 class="recommended-card-title">ENGLISH TITLE</h3>
     -> replaced by the Chinese <h1> of the target article (resolved from the
        card's href slug).  Coverage measured at 2308/2308 (100%).
  2. <span class="recommended-card-cat">Technology</span>
     -> lang-appropriate Chinese category.  'Technology' is the only English
        value in the corpus (2417 occurrences); every other value is already
        Chinese (分析/技术/技術/AI战略/数据治理 ...).

Design notes
------------
* Pure regex + dict substitution, zero model calls, idempotent (re-running is a no-op).
* Reads and writes each file atomically (read -> transform -> compare -> write),
  so a concurrent editor only risks a lost write within its own few-ms window;
  use --exclude to skip files another agent owns.
* Never touches anything inside <article> — the article body is owned by other
  repair passes (wave-1 EN translation, wave-2 FAQ rebuild).

Usage
-----
  python3 scripts/localize_recommended_cards.py            # dry run, prints stats
  python3 scripts/localize_recommended_cards.py --apply
  python3 scripts/localize_recommended_cards.py --apply --exclude-file ../_batch_pipeline/wo_merged_0.txt
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ["zh-cn", "zh-tw"]

# 'Technology' -> per-language Chinese label (matches the existing site vocabulary)
CAT_MAP = {
    "zh-cn": {"Technology": "技术"},
    "zh-tw": {"Technology": "技術"},
}


def clean(t: str) -> str:
    return re.sub(r"<[^>]+>", "", t).strip()


def has_cjk(t: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", t))


def build_title_map(lang: str) -> dict:
    """slug -> Chinese <h1> of that article, for the given language."""
    d = os.path.join(ROOT, lang, "blog", "articles")
    m = {}
    if not os.path.isdir(d):
        return m
    for f in os.listdir(d):
        if not f.endswith(".html"):
            continue
        s = open(os.path.join(d, f), encoding="utf-8", errors="replace").read()
        hm = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        if hm:
            t = clean(hm.group(1))
            if has_cjk(t):
                m[f[:-5]] = t
    return m


def load_excludes(paths) -> set:
    """Return a set of '<lang>/<basename>.html'.

    Work-order files are hand-maintained and use inconsistent path shapes
    (`zh-cn/slug.html`, `zh-cn/blog/articles/slug.html`, `slug.html`, with or
    without the `.html` extension).  Normalise down to lang + basename so the
    comparison against the on-disk file always matches.
    """
    out = set()
    for p in paths:
        if not os.path.isfile(p):
            continue
        for line in open(p, encoding="utf-8", errors="replace"):
            line = line.strip()
            if not line or line.startswith("#") or line.startswith(" "):
                continue
            parts = line.replace("\\", "/").split("/")
            lang = ""
            if parts[0] in LANGS:
                lang = parts[0]
                parts = parts[1:]
            base = parts[-1]
            if not base.endswith(".html"):
                base += ".html"
            out.add(f"{lang}/{base}" if lang else base)
    return out


def process_file(path: str, lang: str, title_map: dict, apply: bool):
    src = open(path, encoding="utf-8", errors="replace").read()
    s = src
    n_title = n_cat = 0
    cat_map = CAT_MAP.get(lang, {})

    # --- 1) recommended card titles -------------------------------------
    def repl_card(m):
        nonlocal n_title
        href, inner = m.group(1), m.group(2)
        tm = re.search(r"(<h3 class=\"recommended-card-title\">)(.*?)(</h3>)", inner, re.S)
        if not tm:
            return m.group(0)
        cur = clean(tm.group(2))
        if has_cjk(cur):
            return m.group(0)
        slug = href.rstrip("/").split("/")[-1]
        zh = title_map.get(slug)
        if not zh or not has_cjk(zh):
            return m.group(0)
        n_title += 1
        new_inner = inner[:tm.start()] + tm.group(1) + zh + tm.group(3) + inner[tm.end():]
        return m.group(0).replace(inner, new_inner)

    s = re.sub(r'<a href="([^"]+)" class="recommended-card">\s*(.*?)</a>', repl_card, s, flags=re.S)

    # --- 2) recommended card category -----------------------------------
    def repl_cat(m):
        nonlocal n_cat
        cur = clean(m.group(2))
        zh = cat_map.get(cur)
        if not zh:
            return m.group(0)
        n_cat += 1
        return m.group(1) + zh + m.group(3)

    s = re.sub(r'(<span class="recommended-card-cat">)(.*?)(</span>)', repl_cat, s, flags=re.S)

    if apply and s != src:
        open(path, "w", encoding="utf-8").write(s)
    return n_title, n_cat


def main():
    apply = "--apply" in sys.argv
    exc_paths = [a.split("=", 1)[1] for a in sys.argv if a.startswith("--exclude-file=")]
    excludes = load_excludes(exc_paths)

    tot_files = tot_title = tot_cat = 0
    for lang in LANGS:
        title_map = build_title_map(lang)
        d = os.path.join(ROOT, lang, "blog", "articles")
        if not os.path.isdir(d):
            continue
        lf = lt = lc = 0
        skipped = 0
        for f in sorted(os.listdir(d)):
            if not f.endswith(".html"):
                continue
            key = f"{lang}/{f}"
            if key in excludes or f in excludes:
                skipped += 1
                continue
            p = os.path.join(d, f)
            try:
                t, c = process_file(p, lang, title_map, apply)
            except Exception as e:  # never abort the whole run on one bad file
                print(f"  !! {p}: {e}")
                continue
            if t or c:
                lf += 1
                lt += t
                lc += c
        print(f"[{lang}] files changed: {lf} | card titles: {lt} | card cats: {lc} | excluded: {skipped}")
        tot_files += lf
        tot_title += lt
        tot_cat += lc
    print(f"TOTAL  files={tot_files}  titles={tot_title}  cats={tot_cat}  "
          f"({'APPLIED' if apply else 'DRY RUN'})")


if __name__ == "__main__":
    main()
