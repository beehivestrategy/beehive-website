#!/usr/bin/env python3
"""
Dev.to Auto-Publish Script for Beehive Strategy Blog

Publishes English blog articles to Dev.to with canonical URL pointing back
to beehivestrategy.com. Avoids duplicates by checking existing articles.

Usage:
  # Publish specific article by slug
  python3 scripts/devto_publish.py --slug what-is-conversational-bi

  # Publish articles changed in the latest git commit
  python3 scripts/devto_publish.py --git-diff

  # Publish articles from the last N commits
  python3 scripts/devto_publish.py --git-diff --commits 3

Environment variables:
  DEVTO_API_KEY  - Dev.to API key (required)
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

import requests
from bs4 import BeautifulSoup

try:
    import html2text
except ImportError:
    print("ERROR: html2text not installed. Run: pip install html2text")
    sys.exit(1)

# --- Configuration ---
DEVTO_API_BASE = "https://dev.to/api"
SITE_BASE_URL = "https://www.beehivestrategy.com"
BLOG_DIR = Path(__file__).parent.parent / "blog" / "articles"
MAX_TAGS = 4  # Dev.to allows max 4 tags
MAX_TITLE_LENGTH = 100  # Dev.to title limit

# Tag mapping: normalize article keywords to valid Dev.to tags
TAG_MAPPING = {
    "conversational bi": "ai",
    "ai analytics": "ai",
    "enterprise bi": "business",
    "data democratisation": "data",
    "natural language analytics": "ai",
    "mcp": "programming",
    "model context protocol": "programming",
    "data governance": "datascience",
    "ai governance": "ai",
    "conversational analytics": "ai",
    "enterprise ai": "ai",
    "data quality": "data",
    "data mesh": "architecture",
    "rag": "ai",
    "retail analytics": "analytics",
    "manufacturing": "productivity",
    "predictive maintenance": "ai",
    "ai strategy": "ai",
    "data strategy": "data",
    "compliance": "security",
    "gdpr": "security",
    "pipl": "security",
    "data privacy": "privacy",
    "cybersecurity": "security",
    "text-to-sql": "sql",
    "semantic layer": "data",
    "data catalog": "data",
    "data lineage": "data",
    "ai agents": "ai",
    "agentic ai": "ai",
    "vector database": "database",
    "fine-tuning": "machinelearning",
    "llm": "ai",
    "change management": "business",
    "digital transformation": "business",
    "kpi": "analytics",
    "dashboard": "analytics",
    "self-service analytics": "analytics",
    "business intelligence": "analytics",
}

# Default tags if no mapping found
DEFAULT_TAGS = ["ai", "data", "analytics"]


def get_api_key():
    """Get Dev.to API key from environment."""
    key = os.environ.get("DEVTO_API_KEY")
    if not key:
        print("ERROR: DEVTO_API_KEY environment variable not set")
        sys.exit(1)
    return key


def get_published_articles(api_key):
    """
    Fetch all published and unpublished articles from Dev.to.
    Returns dict mapping canonical_url -> article_id.
    """
    headers = {"api-key": api_key}
    canonical_map = {}

    for status in ["published", "unpublished"]:
        try:
            resp = requests.get(
                f"{DEVTO_API_BASE}/articles/me/{status}",
                headers=headers,
                timeout=30,
            )
            resp.raise_for_status()
            for article in resp.json():
                canonical = article.get("canonical_url", "")
                if canonical:
                    canonical_map[canonical] = article["id"]
        except requests.RequestException as e:
            print(f"WARNING: Could not fetch {status} articles: {e}")

    print(f"Found {len(canonical_map)} existing articles on Dev.to")
    return canonical_map


def parse_article(html_path):
    """
    Parse a blog article HTML file and extract content for Dev.to.

    Returns dict with: title, description, body_markdown, canonical_url,
                      tags, cover_image, published_date
    """
    html_content = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract title
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else html_path.stem
    # Clean up title (remove site name suffix if present)
    title = re.sub(r"\s*[|\-]\s*Beehive Strategy.*$", "", title)
    if len(title) > MAX_TITLE_LENGTH:
        title = title[:MAX_TITLE_LENGTH - 3] + "..."

    # Extract meta description
    desc_tag = soup.find("meta", attrs={"name": "description"})
    description = desc_tag.get("content", "") if desc_tag else ""

    # Extract canonical URL
    canonical_tag = soup.find("link", rel="canonical")
    canonical_url = canonical_tag.get("href", "") if canonical_tag else ""
    if canonical_url and not canonical_url.startswith("http"):
        canonical_url = SITE_BASE_URL + canonical_url

    # Extract cover image
    og_image_tag = soup.find("meta", property="og:image")
    cover_image = og_image_tag.get("content", "") if og_image_tag else ""

    # Extract tags from meta keywords
    keywords_tag = soup.find("meta", attrs={"name": "keywords"})
    keywords = []
    if keywords_tag:
        keywords = [k.strip().lower() for k in keywords_tag.get("content", "").split(",")]

    # Map keywords to Dev.to tags
    devto_tags = []
    for kw in keywords:
        if kw in TAG_MAPPING:
            tag = TAG_MAPPING[kw]
            if tag not in devto_tags:
                devto_tags.append(tag)
        # Also check partial matches
        for map_key, map_val in TAG_MAPPING.items():
            if map_key in kw and map_val not in devto_tags:
                devto_tags.append(map_val)
                break

    # Fallback to default tags
    if not devto_tags:
        devto_tags = DEFAULT_TAGS[:]

    # Limit to MAX_TAGS
    devto_tags = devto_tags[:MAX_TAGS]

    # Extract article content
    content_div = soup.find("div", class_="article-content")
    if not content_div:
        print(f"WARNING: No article-content div found in {html_path.name}")
        return None

    # Remove footer and navigation from content
    for selector in ["article-footer", "article-nav", "share-buttons", "related-reading"]:
        elements = content_div.find_all(class_=selector)
        for el in elements:
            el.decompose()

    # Convert relative URLs to absolute
    for tag in content_div.find_all(["img", "a"]):
        for attr in ["src", "href"]:
            val = tag.get(attr, "")
            if val and not val.startswith(("http", "//", "data:", "#")):
                tag[attr] = SITE_BASE_URL + ("/" + val.lstrip("/"))

    # Convert HTML to Markdown
    h2t = html2text.HTML2Text()
    h2t.body_width = 0  # Don't wrap lines
    h2t.ignore_images = False
    h2t.ignore_links = False
    h2t.ignore_emphasis = False
    h2t.skip_internal_links = False
    h2t.inline_links = True
    h2t.protect_links = True

    body_markdown = h2t.handle(str(content_div))

    # Clean up markdown
    # Remove excessive blank lines
    body_markdown = re.sub(r"\n{3,}", "\n\n", body_markdown)
    # Strip leading/trailing whitespace
    body_markdown = body_markdown.strip()

    # Add original article link at the bottom
    if canonical_url:
        body_markdown += f"\n\n---\n\n*This article was originally published on [Beehive Strategy]({canonical_url}). Visit our [blog]({SITE_BASE_URL}/blog) for more insights on AI-powered analytics.*\n"

    # Extract publish date from JSON-LD or meta
    published_date = ""
    article_tag = soup.find("meta", property="article:published_time")
    if article_tag:
        published_date = article_tag.get("content", "")

    return {
        "title": title,
        "description": description,
        "body_markdown": body_markdown,
        "canonical_url": canonical_url,
        "tags": devto_tags,
        "cover_image": cover_image,
        "published_date": published_date,
        "slug": html_path.stem,
    }


def publish_to_devto(api_key, article_data, dry_run=False, auto_publish=False):
    """Publish an article to Dev.to.

    Args:
        api_key: Dev.to API key
        article_data: Parsed article data dict
        dry_run: If True, show what would be published without posting
        auto_publish: If True, publish immediately (published=true). If False, save as draft.
    """
    if dry_run:
        status = "PUBLISHED" if auto_publish else "DRAFT"
        print(f"\n[DRY RUN] Would publish as {status}:")
        print(f"  Title: {article_data['title']}")
        print(f"  Canonical: {article_data['canonical_url']}")
        print(f"  Tags: {article_data['tags']}")
        print(f"  Cover: {article_data['cover_image']}")
        print(f"  Body length: {len(article_data['body_markdown'])} chars")
        return True

    headers = {
        "api-key": api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "article": {
            "title": article_data["title"],
            "body_markdown": article_data["body_markdown"],
            "published": auto_publish,  # True = publish immediately, False = draft
            "tags": article_data["tags"],
            "canonical_url": article_data["canonical_url"],
        }
    }

    # Add cover image if available
    if article_data["cover_image"]:
        payload["article"]["main_image"] = article_data["cover_image"]

    try:
        resp = requests.post(
            f"{DEVTO_API_BASE}/articles",
            headers=headers,
            json=payload,
            timeout=60,
        )

        if resp.status_code == 201:
            result = resp.json()
            article_id = result.get("id")
            article_url = result.get("url", "unknown")
            status_label = "PUBLISHED" if auto_publish else "Draft"
            print(f"  SUCCESS: Published as {status_label} (ID: {article_id})")
            print(f"  URL: {article_url}")
            if not auto_publish:
                print(f"  Status: Draft (review and publish on Dev.to)")
            return True
        else:
            print(f"  ERROR: Dev.to API returned {resp.status_code}")
            print(f"  Response: {resp.text[:500]}")
            return False

    except requests.RequestException as e:
        print(f"  ERROR: Request failed: {e}")
        return False


def get_git_changed_articles(commits=1):
    """Get list of article HTML files changed in the last N commits."""
    try:
        result = subprocess.run(
            ["git", "log", f"-{commits}", "--name-only", "--pretty=format:", "--diff-filter=A", "blog/articles/"],
            capture_output=True,
            text=True,
            cwd=str(BLOG_DIR.parent.parent),
        )
        files = [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
        # Filter for .html files in blog/articles/
        articles = [f for f in files if f.startswith("blog/articles/") and f.endswith(".html")]
        return articles
    except Exception as e:
        print(f"WARNING: Could not get git diff: {e}")
        return []


def main():
    parser = argparse.ArgumentParser(description="Publish Beehive Strategy blog to Dev.to")
    parser.add_argument("--slug", help="Article slug (filename without .html)")
    parser.add_argument("--git-diff", action="store_true", help="Publish articles from recent git commits")
    parser.add_argument("--commits", type=int, default=1, help="Number of commits to check (default: 1)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be published without posting")
    parser.add_argument("--all", action="store_true", help="Process all articles (use with --dry-run first)")
    parser.add_argument("--publish", action="store_true", help="Auto-publish immediately (default: save as draft)")
    args = parser.parse_args()

    api_key = get_api_key()

    # Determine which articles to process
    article_paths = []

    if args.slug:
        # Single article mode
        path = BLOG_DIR / f"{args.slug}.html"
        if not path.exists():
            print(f"ERROR: Article not found: {path}")
            sys.exit(1)
        article_paths = [path]
    elif args.git_diff:
        # Git diff mode
        changed = get_git_changed_articles(args.commits)
        if not changed:
            print("No new articles found in recent commits.")
            return
        article_paths = [BLOG_DIR.parent.parent / f for f in changed if (BLOG_DIR.parent.parent / f).exists()]
    elif args.all:
        # All articles mode
        article_paths = sorted(BLOG_DIR.glob("*.html"))
    else:
        parser.print_help()
        sys.exit(1)

    if not article_paths:
        print("No articles to process.")
        return

    print(f"Processing {len(article_paths)} article(s)...")

    # Get existing Dev.to articles to avoid duplicates
    if not args.dry_run:
        existing = get_published_articles(api_key)
    else:
        existing = {}

    published_count = 0
    skipped_count = 0
    failed_count = 0

    for path in article_paths:
        print(f"\n--- Processing: {path.name} ---")

        # Parse the article
        article_data = parse_article(path)
        if not article_data:
            print("  SKIP: Could not parse article")
            failed_count += 1
            continue

        print(f"  Title: {article_data['title']}")
        print(f"  Canonical: {article_data['canonical_url']}")

        # Check for duplicates
        if article_data["canonical_url"] in existing:
            existing_id = existing[article_data["canonical_url"]]
            print(f"  SKIP: Already published on Dev.to (ID: {existing_id})")
            skipped_count += 1
            continue

        # Publish
        success = publish_to_devto(api_key, article_data, dry_run=args.dry_run, auto_publish=args.publish)
        if success:
            published_count += 1
            # Add to existing to prevent duplicates in same batch
            existing[article_data["canonical_url"]] = "new"
        else:
            failed_count += 1

    # Summary
    print(f"\n{'='*50}")
    print(f"SUMMARY: {published_count} published, {skipped_count} skipped, {failed_count} failed")
    if not args.dry_run and published_count > 0:
        if args.publish:
            print(f"\nNOTE: Articles were PUBLISHED on Dev.to.")
            print(f"View them at: https://dev.to/beehivestrategy")
        else:
            print(f"\nNOTE: Articles were saved as DRAFTS on Dev.to.")
            print(f"Review and publish them at: https://dev.to/dashboard")


if __name__ == "__main__":
    main()
