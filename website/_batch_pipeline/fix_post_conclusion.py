#!/usr/bin/env python3
"""
fix_post_conclusion.py — Moves H2 sections that appear after key-takeaways/conclusion
to BEFORE the key-takeaways section, restoring correct article flow.

This is a broader fix for all articles where the injection script placed new content
after the conclusion instead of before it.
"""
import re, os, glob

ARTICLES_DIR = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/blog/articles"


def fix_article(path):
    html = open(path, encoding="utf-8").read()

    article_end = html.rfind('</article>')
    if article_end == -1:
        return False, "no </article>"

    body = html[:article_end]

    # Find all H2 id positions
    h2_iter = list(re.finditer(r'<h2\s+id="([^"]+)"', body))

    # Find boundary: first key-takeaways or conclusion
    boundary_match = None
    for m in h2_iter:
        if 'key-takeaways' in m.group(1) or 'conclusion' in m.group(1):
            boundary_match = m
            break

    if boundary_match is None:
        return False, "no boundary"

    boundary_pos = boundary_match.start()
    boundary_line_start = html.rfind('\n', 0, boundary_pos) + 1

    # Find all H2s after boundary that are NOT key-takeaways or conclusion
    misplaced_h2s = []
    for m in h2_iter:
        if m.start() > boundary_pos and 'key-takeaways' not in m.group(1) and 'conclusion' not in m.group(1):
            misplaced_h2s.append(m)

    if not misplaced_h2s:
        return False, "no misplaced content"

    # Extract everything from boundary_line_start to article_end
    block = html[boundary_line_start:article_end]

    # Find the first misplaced H2 line in the block
    first_misplaced = misplaced_h2s[0]
    first_misplaced_line_start = html.rfind('\n', 0, first_misplaced.start()) + 1
    # Adjust relative to block
    split_pos = first_misplaced_line_start - boundary_line_start

    keep_block = block[:split_pos].rstrip()
    move_block = block[split_pos:].strip()

    if not move_block:
        return False, "empty move block"

    # Rebuild: [before boundary] + [moved content] + [keep block] + [</article> + rest]
    original_before = html[:boundary_line_start]
    article_rest = html[article_end:]

    new_html = original_before + move_block + '\n\n' + keep_block + '\n' + article_rest

    with open(path, 'w', encoding="utf-8") as f:
        f.write(new_html)

    return True, f"moved {len(misplaced_h2s)} sections"


def main():
    files = sorted(glob.glob(os.path.join(ARTICLES_DIR, "*.html")))
    fixed = 0
    skipped = 0

    for path in files:
        fname = os.path.basename(path)
        ok, msg = fix_article(path)
        if ok:
            print(f"  FIXED: {fname} — {msg}")
            fixed += 1
        else:
            if msg != "no boundary" and msg != "no misplaced content":
                print(f"  SKIP: {fname} — {msg}")
            skipped += 1

    print(f"\nDone: {fixed} fixed, {skipped} skipped (no issues)")


if __name__ == "__main__":
    main()
