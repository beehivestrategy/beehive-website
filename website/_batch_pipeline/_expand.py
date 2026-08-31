#!/usr/bin/env python3
"""Insert a prose block into an article body, right before the FAQ section.
Usage: _expand.py <file> <prose_file> [marker]
Reports word count (EN) or CJK char count (zh) before/after.
Never touches <head>, <footer>, share buttons.
"""
import sys, re

def count_en(text):
    return len(re.findall(r"[A-Za-z0-9']+", text))

def count_cjk(text):
    return len(re.findall(r"[\u3400-\u9fff\uf900-\ufaff\uff00-\uffef]", text))

def body_region(text):
    # Count only within <article id="article-content"> ... up to FAQ marker.
    m = re.search(r'<article id="article-content">', text)
    start = m.start() if m else 0
    return text[start:]

def main():
    file = sys.argv[1]
    prose_file = sys.argv[2]
    marker = sys.argv[3] if len(sys.argv) > 3 else '<section class="faq-section"'
    with open(file, encoding="utf-8") as f:
        html = f.read()
    with open(prose_file, encoding="utf-8") as f:
        prose = f.read().strip()
    # determine language by file path
    is_zh = ("/zh-cn/" in file) or ("/zh-tw/" in file)
    cnt = count_cjk if is_zh else count_en
    before = cnt(body_region(html))
    idx = html.find(marker)
    if idx == -1:
        print(f"MARKER NOT FOUND in {file}")
        sys.exit(2)
    # insert before marker, with a leading newline
    html = html[:idx] + "\n" + prose + "\n\n" + html[idx:]
    with open(file, "w", encoding="utf-8") as f:
        f.write(html)
    after = cnt(body_region(html))
    print(f"{file}\n  before={before}  after={after}  (+{after-before})  {'CJK' if is_zh else 'words'}")

if __name__ == "__main__":
    main()
