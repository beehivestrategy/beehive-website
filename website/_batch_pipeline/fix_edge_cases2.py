#!/usr/bin/env python3
"""
fix_edge_cases2.py — Removes duplicate content that was incorrectly left behind
after the first fix_edge_cases.py run.

Current state: [moved content] → conclusion → [DUPLICATE content] → FAQ → nav → key-takeaways → </article>
Fix: remove the duplicate content between conclusion section end and FAQ section start.
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

    # Find the conclusion H2
    h2s = list(re.finditer(r'<h2\s+id="([^"]+)"', body))
    conclusion = None
    for m in h2s:
        if 'conclusion' in m.group(1):
            conclusion = m
            break
    if not conclusion:
        print("  SKIP: no conclusion")
        return False

    # Find the FAQ section start
    faq_start = body.find('<section class="faq-section"')
    if faq_start == -1:
        faq_start = body.find('<div class="faq-section"')
    if faq_start == -1:
        print("  SKIP: no FAQ section")
        return False

    # Find H2s between conclusion and FAQ that are duplicates (same IDs appear before conclusion)
    after_conclusion = [m for m in h2s if m.start() > conclusion.start() and m.start() < faq_start
                        and 'key-takeaways' not in m.group(1) and 'conclusion' not in m.group(1)]

    if not after_conclusion:
        print("  SKIP: no duplicate H2s found")
        return False

    # Check which of these have duplicates before the conclusion
    before_ids = {m.group(1) for m in h2s if m.start() < conclusion.start()
                  and 'key-takeaways' not in m.group(1) and 'conclusion' not in m.group(1)}

    duplicates = [m for m in after_conclusion if m.group(1) in before_ids]

    if not duplicates:
        print("  SKIP: no duplicate IDs found")
        return False

    # Remove the block from the first duplicate H2 to the FAQ section start
    first_dup_line_start = html.rfind('\n', 0, duplicates[0].start()) + 1
    block_to_remove = html[first_dup_line_start:faq_start]

    # Clean up: remove the block and any trailing whitespace
    new_html = html[:first_dup_line_start] + html[faq_start:]

    with open(path, 'w', encoding="utf-8") as f:
        f.write(new_html)

    print(f"  FIXED: removed {len(duplicates)} duplicate sections")
    return True


def main():
    for filename in TARGET_ARTICLES:
        print(f"Processing: {filename}")
        fix_article(filename)


if __name__ == "__main__":
    main()
