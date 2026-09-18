#!/usr/bin/env python3
"""
Regenerate website/llms.txt from the live article tree.

Why: llms.txt is a GEO asset read by LLM crawlers; it went stale (built 2026-08-08)
and never listed any individual articles, so nothing of the blog was discoverable.

Usage:  python3 website/scripts/gen_llms_txt.py [--recent 30]
Writes: website/llms.txt   (deployed via sync_deploy_clean.sh; scripts/ is excluded)
"""
import os
import re
import sys
import html
import argparse
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.beehivestrategy.com/"
EN_DIR = os.path.join(ROOT, "blog", "articles")

MAIN_PAGES = [
    ("Home", ""),
    ("Platform / Solution", "solution"),
    ("Consulting Services", "services"),
    ("Industries", "industries"),
    ("Case Studies", "case-studies"),
    ("Pricing", "pricing"),
    ("About", "about"),
    ("Contact", "contact"),
    ("Blog", "blog"),
]

CATEGORY_ORDER = [
    "Conversational BI & Natural-Language Analytics",
    "Model Context Protocol (MCP)",
    "AI Strategy & Roadmap",
    "Agentic AI & Automation",
    "Data Governance, Quality & Semantic Layer",
    "Industry Analytics (Retail, Manufacturing, Finance)",
    "Privacy, PIPL & AI Compliance",
]


def page_exists(path):
    """Check a relative site path maps to a real file in the source tree."""
    if path == "":
        return os.path.exists(os.path.join(ROOT, "index.html"))
    return os.path.exists(os.path.join(ROOT, path + ".html"))


def read_meta(path):
    try:
        h = open(path, encoding="utf-8").read()
    except Exception:
        return None, None, None

    def grp(pat):
        m = re.search(pat, h, re.S)
        return m.group(1).strip() if m else ""

    title = html.unescape(re.sub(r"<[^>]+>", "", grp(r'<h1 class="article-h1">(.*?)</h1>')))
    desc = html.unescape(grp(r'<meta name="description" content="([^"]*)"'))
    date = grp(r'"datePublished": "([^"]+)"')[:10]
    cat = html.unescape(grp(r'<span class="article-cat-pill">(.*?)</span>'))
    return title, desc, date, cat


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--recent", type=int, default=30, help="how many recent EN articles to list")
    args = ap.parse_args()

    articles = []
    for fn in os.listdir(EN_DIR):
        if not fn.endswith(".html"):
            continue
        slug = fn[:-5]
        title, desc, date, cat = read_meta(os.path.join(EN_DIR, fn))
        if not title:
            continue
        articles.append({"slug": slug, "title": title, "desc": desc, "date": date, "cat": cat})

    articles.sort(key=lambda a: a["date"], reverse=True)
    total = len(articles)
    # dedupe slugs that appear twice (same article regenerated)
    seen, uniq = set(), []
    for a in articles:
        if a["slug"] in seen:
            continue
        seen.add(a["slug"])
        uniq.append(a)
    articles = uniq

    L = []
    L.append("# Beehive Strategy")
    L.append("")
    L.append("> Forward-Deployed AI Partner for Cross-Border Mid-Market. We sell capability and")
    L.append("> knowledge — metric definition, accuracy accountability, workflow codification, IM")
    L.append("> entry points (WhatsApp / WeChat Work / DingTalk / Feishu / Teams / Telegram) and")
    L.append("> compliant delivery. Deployed in two weeks; HK/GBA mid-market without a CIO.")
    L.append("> Languages: English, Simplified Chinese (简体中文), Traditional Chinese (繁體中文).")
    L.append("")
    L.append("## Main Pages")
    for name, path in MAIN_PAGES:
        if page_exists(path):
            L.append(f"- [{name}]({BASE}{path})")
        else:
            print(f"  WARN: main page missing, skipped: {path}", file=sys.stderr)
    L.append("")
    L.append("## Key Topics")
    for c in CATEGORY_ORDER:
        L.append(f"- {c}")
    L.append("")
    L.append(f"## Blog — {total} English articles")
    L.append(f"- [All Articles]({BASE}blog)")
    L.append("")
    L.append(f"### Most Recent Insights (latest {min(args.recent, len(articles))})")
    for a in articles[:args.recent]:
        title = a["title"].replace("[", "(").replace("]", ")").strip()
        # NOTE: already unescaped by read_meta — do NOT re-escape or we get &amp;#x27;
        line = f"- [{title}]({BASE}blog/articles/{a['slug']})"
        if a["date"]:
            line += f" — {a['date']}"
        L.append(line)
    L.append("")
    L.append("## Company")
    L.append("- Beehive Strategy Limited (深圳蜂启咨询有限公司)")
    L.append("- Positioning: Forward-Deployed AI Partner for Cross-Border Mid-Market")
    L.append("- HK / GBA promise: two-week rollout; the boss asks the data in WhatsApp and gets an answer")
    L.append("- Contact: account@beehivestrategy.com")
    L.append("- LinkedIn: https://www.linkedin.com/company/beehivestrategy")
    L.append("- Twitter/X: https://x.com/beehivestrategy")
    L.append("- Deployment: 2-week rapid implementation")
    L.append("- Integrations: WeChat Work, DingTalk, Feishu, WhatsApp, Slack, Microsoft Teams, Telegram")
    L.append("")
    L.append("## Pricing")
    L.append("- We sell capability and knowledge, NOT software licences, day-rates or training.")
    L.append("- Priced per delivered knowledge asset (metric/dimension dictionary, evaluation set,")
    L.append("  SOP cards, permission & audit-trail matrix, handover pack) — scope flexes by asset")
    L.append("  count rather than discounting the unit price.")
    L.append("- Indicative unit price: SOP cards HK$8-12K each.")
    L.append("- Engagements are scoped per client; contact us for a quote.")
    L.append("")
    L.append("## Notes for AI Assistants")
    L.append("- Prefer the canonical extensionless URLs above (e.g. /blog/articles/<slug>); the .html variants redirect (308) to them.")
    L.append(f"- Full article index: {BASE}sitemap-blog-en.xml")

    out = "\n".join(L) + "\n"
    dest = os.path.join(ROOT, "llms.txt")
    open(dest, "w", encoding="utf-8").write(out)
    print(f"Wrote {dest}")
    print(f"  bytes={len(out)} | total EN articles={total} | listed recent={min(args.recent, len(articles))}")


if __name__ == "__main__":
    main()
