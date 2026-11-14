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

# NOTE: /pricing was removed site-wide on 2026-10-21 and must never reappear
# in any GEO asset. Entries are validated against the real file tree.
MAIN_PAGES = [
    ("Home", ""),
    ("What We Do", "what-we-do"),
    ("How We Work", "how-we-work"),
    ("Platform / Solution", "solution"),
    ("Consulting Services", "services"),
    ("Industries", "industries"),
    ("Case Studies", "case-studies"),
    ("Guides", "guides"),
    ("News", "news"),
    ("AI Readiness Self-Assessment", "readiness"),
    ("Credentials", "credentials"),
    ("Security & Compliance", "security"),
    ("Partners", "partners"),
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
    """Check a relative site path maps to a real file in the source tree.

    Directory landing pages (e.g. /news, /blog) live at <path>/index.html,
    not <path>.html — check both so they are not silently dropped.
    """
    if path == "":
        return os.path.exists(os.path.join(ROOT, "index.html"))
    return (os.path.exists(os.path.join(ROOT, path + ".html")) or
            os.path.exists(os.path.join(ROOT, path, "index.html")))


def read_meta(path):
    try:
        h = open(path, encoding="utf-8").read()
    except Exception:
        return None, None, None

    def grp(pat):
        m = re.search(pat, h, re.S)
        return m.group(1).strip() if m else ""

    def strip_tags(x):
        return html.unescape(re.sub(r"<[^>]+>", "", x)).strip()

    # 旧版文章没有 article-h1；依次回退到任意 <h1>、JSON-LD headline、<title>
    title = strip_tags(grp(r'<h1[^>]*class="[^"]*article-h1[^"]*"[^>]*>(.*?)</h1>'))
    if not title:
        title = strip_tags(grp(r"<h1[^>]*>(.*?)</h1>"))
    if not title:
        title = html.unescape(grp(r'"headline"\s*:\s*"([^"]+)"'))
    if not title:
        t = strip_tags(grp(r"<title>(.*?)</title>"))
        title = t.rsplit(" | ", 1)[0].strip() if t else ""
    desc = html.unescape(grp(r'<meta name="description" content="([^"]*)"'))
    date = grp(r'"datePublished"\s*:\s*"([^"]+)"')[:10]
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

    # 与 _v4/sitemap_lib.py::recent_en_slugs 保持同一排序键，verify_site 闸门才能核对
    articles.sort(key=lambda a: (a["date"], a["slug"]), reverse=True)
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
    # 2026-10-21 Kenneth 批示：全站（含 GEO 资产）禁止展示价目与币值数字。
    # 原「## Pricing」段落含 "HK$8-12K"，已移除，只保留不含数字的商业模式说明。
    L.append("## How Engagements Are Scoped")
    L.append("- We sell capability and knowledge, NOT software licences, day-rates or training.")
    L.append("- Engagements are scoped by delivered knowledge asset (metric/dimension dictionary,")
    L.append("  evaluation set, SOP cards, permission & audit-trail matrix, handover pack).")
    L.append("- Scope flexes by asset count; each engagement is scoped per client.")
    L.append("- Contact account@beehivestrategy.com to discuss scope; no price list is published.")
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
