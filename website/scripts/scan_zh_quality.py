#!/usr/bin/env python3
"""Scan zh-cn article pages for content-quality defects (2026-09-01).

Detects:
  1. EXACT duplicate paragraphs within the same page (kept >= 2 occurrences,
     len > 40 chars after tag-strip) — the "content is just a mess" pathology.
  2. Duplicate H2 sections (same normalized heading appears 2+ times).
  3. English-leak paragraphs (mostly-Latin body text in a zh page; excludes
     <code> blocks, legit short tech terms).
  4. FAQ defects (added 2026-09-01 after these slipped past rules 1-3):
     a) faq-section widget heading still carries English ("Frequently Asked
        Questions常见问题") — invisible to rule 3 because CJK is present.
     b) FAQ question text contains the raw article slug
        ("企业应如何从real time data streaming...获得战略价值？").
     c) page renders more than one <section class="faq-section"> component
        (duplicate widget with duplicate ids).

Usage:
  python3 scripts/scan_zh_quality.py            # summary only (zh-cn)
  python3 scripts/scan_zh_quality.py --all      # scan zh-cn + zh-tw
  python3 scripts/scan_zh_quality.py --verbose  # list every defect
Exit code 0 always (report tool).
"""
import re
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
ZH = ROOT / "zh-cn" / "blog" / "articles"
VERBOSE = "--verbose" in sys.argv
ALL_LANGS = "--all" in sys.argv

P_RE = re.compile(r"<p[^>]*>(.*?)</p>", re.S)
H2_RE = re.compile(r"<h2[^>]*>(.*?)</h2>", re.S)
TAG_RE = re.compile(r"<[^>]+>")


def clean(s: str) -> str:
    s = re.sub(r"&nbsp;|&amp;|&lt;|&gt;|&quot;", " ", s)
    s = TAG_RE.sub("", s)
    return re.sub(r"\s+", " ", s).strip()


def latin_ratio(s: str) -> float:
    letters = [c for c in s if c.isalpha()]
    if not letters:
        return 0.0
    latin = [c for c in letters if ord(c) < 0x2E80]
    return len(latin) / len(letters)


def scan_file(path: Path):
    try:
        html = path.read_text(encoding="utf-8")
    except Exception as e:
        return {"error": str(e)}

    body_m = re.search(r"<article[^>]*>(.*?)</article>", html, re.S)
    body = body_m.group(1) if body_m else html

    defects = {"dup_paras": [], "dup_h2": [], "en_leak": [],
               "faq_en_title": [], "faq_slug": [], "faq_multi": [], "error": None}

    # --- FAQ defects (scanned on the whole file: the widget can sit outside <article>)
    faq_sections = re.findall(r'<section class="faq-section".*?</section>', html, re.S)
    if len(faq_sections) > 1:
        defects["faq_multi"].append(len(faq_sections))
    for m in re.finditer(r'<h2 class="faq-section-title">(.*?)</h2>', html, re.S):
        t = clean(m.group(1))
        if re.search(r"[A-Za-z]{4,}", t):
            defects["faq_en_title"].append(t[:60])
    for m in re.finditer(r'<span class="faq-question-text">(.*?)</span>\s*<svg', html, re.S):
        t = clean(m.group(1))
        # raw slug = 3+ lowercase ascii words separated by spaces or hyphens
        if re.search(r"[a-z]+[ -][a-z]+[ -][a-z]+", t):
            defects["faq_slug"].append(t[:70])

    paras = [clean(p) for p in P_RE.findall(body)]
    paras = [t for t in paras if len(t) > 40]
    c = Counter(paras)
    for t, n in c.items():
        if n > 1:
            defects["dup_paras"].append((t[:60], n))

    h2s = [clean(h) for h in H2_RE.findall(body)]
    hc = Counter(h2s)
    for t, n in hc.items():
        if n > 1 and len(t) > 3:
            defects["dup_h2"].append((t[:60], n))

    # English leak: paragraph in zh page that is mostly Latin
    for m in P_RE.finditer(body):
        t = clean(m.group(1))
        if len(t) < 60 or "<code" in m.group(1):
            continue
        # skip paragraphs containing CJK entirely
        if any(0x4E00 <= ord(ch) <= 0x9FFF for ch in t):
            continue
        if latin_ratio(t) > 0.85 and sum(ch.isalpha() for ch in t) > 40:
            defects["en_leak"].append(t[:70])

    return defects


def main():
    dirs = [ZH]
    if ALL_LANGS:
        dirs.append(ROOT / "zh-tw" / "blog" / "articles")
    files = []
    for d in dirs:
        files.extend(sorted(d.glob("*.html")))
    dup_files, h2_files, leak_files = [], [], []
    faq_title_files, faq_slug_files, faq_multi_files = [], [], []
    total_dup_paras, total_leaks, total_slugs = 0, 0, 0
    for f in files:
        d = scan_file(f)
        if d.get("error"):
            print("ERR", f.name, d["error"])
            continue
        if d["dup_paras"]:
            dup_files.append((f.name, d["dup_paras"]))
            total_dup_paras += sum(n for _, n in d["dup_paras"]) - len(d["dup_paras"])
        if d["dup_h2"]:
            h2_files.append((f.name, d["dup_h2"]))
        if d["en_leak"]:
            leak_files.append((f.name, d["en_leak"]))
            total_leaks += len(d["en_leak"])
        if d["faq_en_title"]:
            faq_title_files.append((f.name, d["faq_en_title"]))
        if d["faq_slug"]:
            faq_slug_files.append((f.name, d["faq_slug"]))
            total_slugs += len(d["faq_slug"])
        if d["faq_multi"]:
            faq_multi_files.append((f.name, d["faq_multi"]))

    print(f"scanned: {len(files)} articles ({'zh-cn + zh-tw' if ALL_LANGS else 'zh-cn'})")
    print(f"files with duplicate paragraphs: {len(dup_files)} (excess paras: {total_dup_paras})")
    print(f"files with duplicate H2 sections: {len(h2_files)}")
    print(f"files with english-leak paragraphs: {len(leak_files)} (leaked paras: {total_leaks})")
    print(f"files with English in FAQ widget title: {len(faq_title_files)}")
    print(f"files with raw slug inside FAQ question: {len(faq_slug_files)} (questions: {total_slugs})")
    print(f"files with duplicate FAQ component: {len(faq_multi_files)}")

    if VERBOSE:
        print("\n===== DUPLICATE PARAGRAPHS =====")
        for name, dups in dup_files:
            print(f"\n[{name}]")
            for t, n in sorted(dups, key=lambda x: -x[1]):
                print(f"  {n}x  {t}")
        print("\n===== DUPLICATE H2 =====")
        for name, dups in h2_files:
            print(f"[{name}] {dups}")
        print("\n===== ENGLISH LEAKS =====")
        for name, leaks in leak_files:
            print(f"\n[{name}]")
            for t in leaks[:4]:
                print(f"  - {t}")
        print("\n===== FAQ DEFECTS =====")
        for name, t in faq_title_files:
            print(f"[en-title] {name}: {t[:2]}")
        for name, s in faq_slug_files:
            print(f"[slug] {name}")
            for q in s[:4]:
                print(f"  - {q}")
        for name, n in faq_multi_files:
            print(f"[multi] {name}: {n} faq components")
    else:
        if dup_files:
            print("\ntop dup files:", [n for n, _ in sorted(dup_files, key=lambda x: -sum(n2 for _, n2 in x[1]))[:8]])
        if leak_files:
            print("leak files (first 12):", [n for n, _ in leak_files[:12]])
        if faq_title_files:
            print("faq en-title files (first 12):", [n for n, _ in faq_title_files[:12]])
        if faq_slug_files:
            print("faq slug files:", [n for n, _ in faq_slug_files])
        if faq_multi_files:
            print("faq multi-component files:", [n for n, _ in faq_multi_files])


if __name__ == "__main__":
    main()
