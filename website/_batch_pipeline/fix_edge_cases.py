#!/usr/bin/env python3
"""
fix_edge_cases.py — Targeted fix for 2 articles where the FAQ section is inside
the <article> tag, making the generic fix_post_conclusion.py too aggressive.

These articles have: conclusion → [misplaced H2s] → FAQ section → nav → key-takeaways → </article>
We only move the misplaced H2s before the conclusion, leaving FAQ/nav/key-takeaways in place.
"""
import re, os

ARTICLES_DIR = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/blog/articles"

TARGET_ARTICLES = [
    "architecture-of-an-enterprise-ai-agent.html",
    "the-ai-maturity-model-where-does-your-organization-stand.html",
]


def fix_article(filename):
    path = os.path.join(ARTICLES_DIR, filename)
    html = open(path, encoding="utf-8").read()

    article_end = html.rfind('</article>')
    body = html[:article_end]

    # Find boundary: first key-takeaways or conclusion H2
    h2s = list(re.finditer(r'<h2\s+id="([^"]+)"', body))
    boundary = None
    for m in h2s:
        if 'key-takeaways' in m.group(1) or 'conclusion' in m.group(1):
            boundary = m
            break
    if not boundary:
        print("  SKIP: no boundary")
        return False

    # Find the FAQ section start (it's the anchor for where template content begins)
    faq_start = body.find('<section class="faq-section"')
    if faq_start == -1:
        faq_start = body.find('<div class="faq-section"')
    if faq_start == -1:
        print("  SKIP: no FAQ section found")
        return False

    # Find all H2s between boundary and FAQ section that are NOT key-takeaways/conclusion
    misplaced = [m for m in h2s if m.start() > boundary.start() and m.start() < faq_start
                 and 'key-takeaways' not in m.group(1) and 'conclusion' not in m.group(1)]

    if not misplaced:
        print("  SKIP: no misplaced H2s between boundary and FAQ")
        return False

    # Extract the misplaced content block (from first misplaced H2 line to FAQ section start)
    first_misplaced_line_start = html.rfind('\n', 0, misplaced[0].start()) + 1
    misplaced_block = html[first_misplaced_line_start:faq_start].strip()

    # Get boundary line start (where to insert the moved content)
    boundary_line_start = html.rfind('\n', 0, boundary.start()) + 1

    # Rebuild:
    # [content before boundary] + [misplaced content] + [boundary section + rest with misplaced block removed]
    original_before = html[:boundary_line_start]
    # Remove the misplaced block from the rest of the HTML
    rest_with_misplaced = html[boundary_line_start:]
    rest_clean = rest_with_misplaced[:first_misplaced_line_start - boundary_line_start] + rest_with_misplaced[faq_start:]

    new_html = original_before + misplaced_block + '\n\n' + rest_clean

    with open(path, 'w', encoding="utf-8") as f:
        f.write(new_html)

    print(f"  FIXED: moved {len(misplaced)} sections before {boundary.group(1)}")
    return True


def main():
    for filename in TARGET_ARTICLES:
        print(f"Processing: {filename}")
        fix_article(filename)


if __name__ == "__main__":
    main()
