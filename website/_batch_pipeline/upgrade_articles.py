#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
upgrade_articles.py — Apply the new content layout to a set of EN article pages.

For each slug:
  1. Insert a full-width <figure class="article-hero"> (the new cover) right
     before the article header container.
  2. Remove the duplicated <figure data-fig-slug2="..."> block.
  3. Add class="article-lead" to the first <p> inside .article-content.

Idempotent: skips steps already applied. Backs up originals to /tmp.
"""
import os, re, html, shutil, sys

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
ART = os.path.join(ROOT, "blog", "articles")

SLUGS = [
    "real-time-data-streaming-conversational-analytics-platform",
    "what-is-mcp-model-context-protocol-explained",
    "semantic-layer-conversational-bi-self-service-analytics",
    "self-service-bi-maturity-model-2025",
    "data-marketplace-enterprise-data-monetization-strategy",
    "quantum-machine-learning-hype-vs-reality-for-business-a-2026-update",
    "conversational-analytics-nlg-automated-insight-reports",
]


def parse_title(slug):
    with open(os.path.join(ART, slug + ".html"), encoding="utf-8", errors="replace") as f:
        txt = f.read()
    m = re.search(r"<title>(.*?)</title>", txt, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else slug


def upgrade(slug):
    path = os.path.join(ART, slug + ".html")
    with open(path, encoding="utf-8", errors="replace") as f:
        txt = f.read()
    orig = txt
    log = []

    # 1) Hero insertion
    if '<figure class="article-hero">' not in txt:
        marker = '<div class="container">\n    <section class="article-header">'
        if marker in txt:
            alt = html.escape(parse_title(slug), quote=True)
            hero = (f'<figure class="article-hero">\n'
                    f'  <img src="/assets/blog/covers/en/{slug}.jpg" alt="{alt}">\n'
                    f'</figure>\n\n')
            txt = txt.replace(marker, hero + marker, 1)
            log.append("hero+")
        else:
            log.append("hero?NO-MARKER")

    # 2) Remove duplicate figure (data-fig-slug2)
    if 'data-fig-slug2' in txt:
        pat = re.compile(r'\n\s*<figure class="article-figure" data-fig-slug2=.*?</figure>\s*\n', re.DOTALL)
        new, n = pat.subn('\n', txt)
        if n:
            txt = new
            log.append(f"dedupe({n})")
        else:
            log.append("dedupe?NO-MATCH")

    # 3) Lead class on first <p> in article-content
    if 'article-lead' not in txt:
        idx = txt.find('<article class="article-content"')
        if idx != -1:
            m = re.search(r'<p(?![^>]*\bclass=)', txt[idx:])
            if m:
                pos = idx + m.start()
                txt = txt[:pos] + '<p class="article-lead"' + txt[pos + 2:]
                log.append("lead+")
            else:
                log.append("lead?NO-P")
        else:
            log.append("lead?NO-ARTICLE")

    if txt != orig:
        os.makedirs("/tmp/article_backup", exist_ok=True)
        shutil.copy(path, os.path.join("/tmp/article_backup", slug + ".html"))
        with open(path, "w", encoding="utf-8") as f:
            f.write(txt)
        # verify
        with open(path, encoding="utf-8") as f:
            after = f.read()
        dup = after.count('data-fig-slug2')
        hero = after.count('<figure class="article-hero">')
        lead = after.count('article-lead')
        fig = after.count('class="article-svg"')
        print(f"  [OK] {slug}: {', '.join(log)} | hero={hero} dedupe_left={dup} lead={lead} svg_figs={fig}")
    else:
        print(f"  [--] {slug}: no changes ({', '.join(log) or 'already done'})")


def main():
    slugs = sys.argv[1:] or SLUGS
    for s in slugs:
        upgrade(s)


if __name__ == "__main__":
    main()
