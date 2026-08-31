#!/usr/bin/env python3
"""
fix_dup_faq.py — Fixes articles with duplicate FAQ sections and post-conclusion content.

Problems fixed:
1. Duplicate FAQ: injection script added <div class="faq-section"> that duplicates
   the proper <section class="faq-section" id="faq"> later in the article.
2. Post-conclusion content: new H2 sections were injected after key-takeaways/conclusion,
   breaking article flow. They should appear before key-takeaways.

Strategy:
- Find the boundary: first H2 with id="key-takeaways" or id="conclusion"
- Extract everything between that boundary and </article>
- Remove the duplicate <div class="faq-section">...</div> block
- Split extracted content: key-takeaways/conclusion stays; other H2 sections move before boundary
"""
import re, os

ARTICLES_DIR = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/blog/articles"

DUP_FAQ_ARTICLES = [
    "case-study-consultancy-cut-reporting-time-mcp-bi.html",
    "cfo-guide-ai-budget-allocation.html",
    "data-quality-automation-from-reactive-to-proactive-part-2.html",
    "event-driven-architecture-for-ai-agent-orchestration-a-2026-update.html",
    "explainable-ai-in-analytics-making-black-boxes-transparent-a-2026-update.html",
    "real-time-data-streaming-for-ai-powered-decision-making-part-2.html",
    "the-future-of-work-ai-augmented-decision-making.html",
]


def fix_article(filename):
    path = os.path.join(ARTICLES_DIR, filename)
    html = open(path, encoding="utf-8").read()

    article_end = html.rfind('</article>')
    if article_end == -1:
        print("  SKIP: no </article> found")
        return False

    # Find boundary: first occurrence of key-takeaways or conclusion H2
    boundary_match = None
    boundary_pos = None
    for pattern in [r'<h2\s+id="key-takeaways"', r'<h2\s+id="conclusion"']:
        m = re.search(pattern, html[:article_end])
        if m and (boundary_pos is None or m.start() < boundary_pos):
            boundary_match = m
            boundary_pos = m.start()

    if boundary_pos is None:
        print("  SKIP: no key-takeaways/conclusion boundary found")
        return False

    # Find the line start of the boundary
    boundary_line_start = html.rfind('\n', 0, boundary_pos) + 1

    # Extract content from boundary to </article>
    misplaced_block = html[boundary_line_start:article_end]

    # Remove duplicate <div class="faq-section">...</div> block
    dup_faq_pattern = r'<div\s+class="faq-section">.*?</div>'
    dup_faq_match = re.search(dup_faq_pattern, misplaced_block, re.DOTALL)
    faq_removed = False
    if dup_faq_match:
        misplaced_block = misplaced_block[:dup_faq_match.start()] + misplaced_block[dup_faq_match.end():]
        faq_removed = True

    # Remove standalone <h2>Frequently Asked Questions</h2>
    misplaced_block = re.sub(r'<h2>\s*Frequently Asked Questions\s*</h2>\s*', '', misplaced_block)

    # Split into lines to find the separation point
    lines = misplaced_block.split('\n')

    # Find first H2 that is NOT key-takeaways or conclusion — that's where misplaced content starts
    split_idx = None
    for i, line in enumerate(lines):
        h2_match = re.search(r'<h2\s+id="', line)
        if h2_match and 'key-takeaways' not in line and 'conclusion' not in line:
            split_idx = i
            break

    if split_idx is None:
        # No misplaced content to move — just remove the dup FAQ if it was found
        if faq_removed:
            original_before = html[:boundary_line_start]
            article_rest = html[article_end:]
            new_html = original_before + misplaced_block.strip() + '\n' + article_rest
            with open(path, 'w', encoding="utf-8") as f:
                f.write(new_html)
            print("  FIXED: removed dup FAQ only (no content to move)")
            return True
        else:
            print("  SKIP: no misplaced content and no dup FAQ found")
            return False

    # keep_block = key-takeaways + conclusion sections (lines 0 to split_idx)
    # move_block = misplaced new sections (lines split_idx onward)
    keep_block = '\n'.join(lines[:split_idx]).rstrip()
    move_block = '\n'.join(lines[split_idx:]).strip()

    if not move_block:
        print("  SKIP: no content to move")
        return False

    # Rebuild: [content before boundary] + [moved content] + [keep block] + </article> + [rest]
    original_before = html[:boundary_line_start]
    article_rest = html[article_end:]  # includes </article> and everything after

    new_html = original_before + move_block + '\n\n' + keep_block + '\n' + article_rest

    with open(path, 'w', encoding="utf-8") as f:
        f.write(new_html)

    moved_lines = len(lines) - split_idx
    print(f"  FIXED: removed dup FAQ={faq_removed}, moved {moved_lines} lines before boundary")
    return True


def main():
    fixed = 0
    for filename in DUP_FAQ_ARTICLES:
        print(f"Processing: {filename}")
        if fix_article(filename):
            fixed += 1
    print(f"\nDone: {fixed}/{len(DUP_FAQ_ARTICLES)} articles fixed")


if __name__ == "__main__":
    main()
