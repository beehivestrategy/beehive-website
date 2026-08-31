#!/usr/bin/env python3
"""
fix_lang_relative_links.py

Repairs broken relative links inside the zh-CN and zh-TW article trees.

BUG
---
Article files under zh-cn/ and zh-TW/ contain links written WITHOUT a leading
slash, e.g.

    <a href="zh-cn/contact">     (inside /zh-tw/blog/articles/foo.html)

Because there is no <base> tag anywhere on the site, that resolves against the
current directory:

    /zh-tw/blog/articles/zh-cn/contact     -> 404

Root pages (zh-tw/index.html etc.) already use the correct root-relative form
("/zh-tw/contact"), so this only affects the generated article files.

FIX
---
1. href="zh-cn/X"  ->  href="/<pagelang>/X"
2. href="zh-tw/X"  ->  href="/<pagelang>/X"
3. bare href="page" (contact|solution|services|pricing|about|case-studies|
   industries|blog)  ->  href="/<pagelang>/page"

where <pagelang> is the language of the FILE being edited, not the language in
the link. This simultaneously fixes the 404 and the language mismatch (a
Traditional-Chinese page linking to a Simplified-Chinese destination).

Already-correct links (href="/zh-cn/...") are left untouched. Absolute URLs,
mailto:, tel:, and in-page anchors are left untouched.

USAGE
    python3 fix_lang_relative_links.py        # dry run, prints a summary
    python3 fix_lang_relative_links.py --apply
"""

import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent  # .../website

# Pages that appear as bare relative links (no language prefix at all).
BARE_PAGES = (
    "contact", "solution", "solutions", "services", "pricing",
    "about", "case-studies", "industries", "blog", "index",
)

# href="zh-cn/..." or href="zh-tw/..." with NO leading slash.
PREFIXED = re.compile(r'href="(zh-cn|zh-tw)/')

# href="contact" etc. - bare, no slash, no scheme, no anchor.
BARE = re.compile(
    r'href="(?!\/|#|https?:|mailto:|tel:|zh-cn\/|zh-tw\/|\.\.?)'
    r'(' + "|".join(BARE_PAGES) + r')(\.html)?"'
)


def fix_file(path: pathlib.Path, lang: str) -> tuple[int, list[tuple[str, str]]]:
    """Return (number_of_replacements, [(before, after), ...])."""
    original = path.read_text(encoding="utf-8")
    text = original
    changes: list[tuple[str, str]] = []
    target = "/" + lang

    def sub_prefixed(m: re.Match) -> str:
        before = m.group(0)
        after = 'href="' + target + "/"
        changes.append((before, after))
        return after

    def sub_bare(m: re.Match) -> str:
        before = m.group(0)
        after = 'href="' + target + "/" + m.group(1) + (m.group(2) or "") + '"'
        changes.append((before, after))
        return after

    text = PREFIXED.sub(sub_prefixed, text)
    text = BARE.sub(sub_bare, text)

    if text != original:
        return len(changes), changes
    return 0, []


def main() -> None:
    apply = "--apply" in sys.argv
    total_files = 0
    total_repl = 0
    per_lang: dict[str, dict[str, int]] = {}
    samples: list[tuple[str, str, str]] = []

    for lang in ("zh-cn", "zh-tw"):
        stats = {"files": 0, "repl": 0}
        for path in sorted((ROOT / lang).rglob("*.html")):
            n, changes = fix_file(path, lang)
            if not n:
                continue
            stats["files"] += 1
            stats["repl"] += n
            if len(samples) < 8:
                for before, after in changes[:1]:
                    samples.append((lang, before, after))
            if apply:
                # recompute and write
                text = path.read_text(encoding="utf-8")
                text = PREFIXED.sub(lambda m: 'href="/' + lang + "/", text)
                text = BARE.sub(
                    lambda m: 'href="/' + lang + "/" + m.group(1)
                    + (m.group(2) or "") + '"',
                    text,
                )
                path.write_text(text, encoding="utf-8")
        per_lang[lang] = stats
        total_files += stats["files"]
        total_repl += stats["repl"]

    print(f"{'[DRY RUN] ' if not apply else ''}files changed: {total_files}, "
          f"links repaired: {total_repl}")
    for lang, s in per_lang.items():
        print(f"  {lang}: {s['files']} files, {s['repl']} links")
    print("\nsample replacements (before -> after):")
    for lang, before, after in samples:
        print(f"  [{lang}] {before}  ->  {after}")


if __name__ == "__main__":
    main()
