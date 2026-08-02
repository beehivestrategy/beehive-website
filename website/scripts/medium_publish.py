#!/usr/bin/env python3
"""
Medium Auto-Publish Script for Beehive Strategy Blog

Publishes English blog articles to Medium as drafts with canonical URL pointing
back to beehivestrategy.com. Avoids duplicates by checking existing articles.

NOTE: Medium's API is officially deprecated (Jan 2023) but endpoints still
remain operational. Integration tokens can be generated at:
  https://medium.com/me/settings → Integration Tokens

Usage:
  # Publish specific article by slug
  python3 scripts/medium_publish.py --slug what-is-conversational-bi

  # Publish articles changed in the latest git commit
  python3 scripts/medium_publish.py --git-diff

  # Publish articles from the last N commits
  python3 scripts/medium_publish.py --git-diff --commits 3

  # Dry run (show what would be published without posting)
  python3 scripts/medium_publish.py --dry-run

  # Publish all articles (use with caution)
  python3 scripts/medium_publish.py --all

Environment variables:
  MEDIUM_API_KEY  - Medium integration token (required)
  MEDIUM_AUTHOR_ID - Medium author ID (required, e.g. abc123def456)
                     Get it by running: curl -H "Authorization: Bearer TOKEN" https://api.medium.com/v1/me
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

try:
    import html2text
except ImportError:
    print("ERROR: html2text not installed. Run: pip install html2text")
    sys.exit(1)

# --- Configuration ---
MEDIUM_API_BASE = "https://api.medium.com/v1"
SITE_BASE_URL = "https://www.beehivestrategy.com"
BLOG_DIR = Path(__file__).parent.parent / "blog" / "articles"
MAX_TAGS = 5  # Medium allows max 5 tags
MAX_TITLE_LENGTH = 100  # Medium title limit

# Tag mapping: normalize article keywords to Medium-friendly tags
TAG_MAPPING = {
    "conversational bi": "Artificial Intelligence",
    "ai analytics": "Artificial Intelligence",
    "enterprise bi": "Business Intelligence",
    "data democratisation": "Data Science",
    "natural language analytics": "Artificial Intelligence",
    "mcp": "Programming",
    "model context protocol": "Programming",
    "data governance": "Data",
    "ai governance": "Artificial Intelligence",
    "conversational analytics": "Artificial Intelligence",
    "enterprise ai": "Artificial Intelligence",
    "data quality": "Data",
    "data mesh": "Technology",
    "rag": "Machine Learning",
    "retail analytics": "Analytics",
    "manufacturing": "Technology",
    "predictive maintenance": "Machine Learning",
    "ai strategy": "Artificial Intelligence",
    "data strategy": "Data",
    "compliance": "Regulation",
    "gdpr": "Privacy",
    "pipl": "Privacy",
    "data privacy": "Privacy",
    "cybersecurity": "Cybersecurity",
    "text-to-sql": "Programming",
    "semantic layer": "Data",
    "data catalog": "Data",
    "data lineage": "Data",
    "ai agents": "Artificial Intelligence",
    "agentic ai": "Artificial Intelligence",
    "vector database": "Database",
    "fine-tuning": "Machine Learning",
    "llm": "Machine Learning",
    "change management": "Management",
    "digital transformation": "Technology",
    "kpi": "Analytics",
    "dashboard": "Analytics",
    "self-service analytics": "Analytics",
    "business intelligence": "Business Intelligence",
}

# Default tags if no mapping found
DEFAULT_TAGS = ["Artificial Intelligence", "Data", "Analytics"]


def get_api_key():
    """Get Medium API key from environment."""
    key = os.environ.get("MEDIUM_API_KEY")
    if not key:
        print("ERROR: MEDIUM_API_KEY environment variable not set")
        print("Get your token at: https://medium.com/me/settings → Integration Tokens")
        sys.exit(1)
    return key


def get_author_id(api_key):
    """Get Medium author ID from environment or API."""
    author_id = os.environ.get("MEDIUM_AUTHOR_ID")
    if author_id:
        return author_id

    # Fetch from API
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        resp = requests.get(f"{MEDIUM_API_BASE}/me", headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        author_id = data["data"]["id"]
        print(f"Retrieved Medium author ID: {author_id}")
        print(f"Set MEDIUM_AUTHOR_ID env var to skip this API call in future")
        return author_id
    except (requests.RequestException, KeyError) as e:
        print(f"ERROR: Could not fetch Medium author ID: {e}")
        print("Set MEDIUM_AUTHOR_ID environment variable manually")
        sys.exit(1)


def get_published_articles(api_key, author_id):
    """
    Fetch all published and draft articles from Medium.
    Returns set of canonical URLs to avoid duplicates.
    """
    headers = {"Authorization": f"Bearer {api_key}"}
    canonical_urls = set()

    # Medium API doesn't have a direct "list my articles" endpoint
    # We use the publications endpoint to check for existing articles
    try:
        resp = requests.get(
            f"{MEDIUM_API_BASE}/users/{author_id}/publications",
            headers=headers,
            timeout=30,
        )
        if resp.ok:
            pubs = resp.json().get("data", [])
            print(f"Found {len(pubs)} Medium publications")
    except requests.RequestException:
        pass

    # Track via a local state file for reliable duplicate prevention
    state_file = Path(__file__).parent / ".medium_published.json"
    if state_file.exists():
        try:
            canonical_urls = set(json.loads(state_file.read_text()))
            print(f"Found {len(canonical_urls)} previously published articles (local state)")
        except json.JSONDecodeError:
            pass

    return canonical_urls


def save_published_state(canonical_urls):
    """Save published articles state to prevent duplicates."""
    state_file = Path(__file__).parent / ".medium_published.json"
    state_file.write_text(json.dumps(list(canonical_urls), indent=2))


def parse_article(html_path):
    """
    Parse a blog article HTML file and extract content for Medium.

    Returns dict with: title, description, content_format, content,
                      canonical_url, tags, cover_image
    """
    html_content = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract title
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else html_path.stem
    title = re.sub(r"\s*[|\-]\s*Beehive Strategy.*$", "", title)
    if len(title) > MAX_TITLE_LENGTH:
        title = title[:MAX_TITLE_LENGTH - 3] + "..."

    # Extract meta description
    desc_tag = soup.find("meta", attrs={"name": "description"})
    description = desc_tag["content"] if desc_tag else ""

    # Extract canonical URL
    canonical_tag = soup.find("link", attrs={"rel": "canonical"})
    canonical_url = canonical_tag["href"] if canonical_tag else f"{SITE_BASE_URL}/blog/articles/{html_path.stem}"

    # Extract cover image
    og_image = soup.find("meta", attrs={"property": "og:image"})
    cover_image = og_image["content"] if og_image else ""

    # Extract tags from keywords
    keywords_tag = soup.find("meta", attrs={"name": "keywords"})
    tags = []
    if keywords_tag:
        raw_keywords = [k.strip().lower() for k in keywords_tag["content"].split(",")]
        for kw in raw_keywords:
            if kw in TAG_MAPPING and TAG_MAPPING[kw] not in tags:
                tags.append(TAG_MAPPING[kw])
            if len(tags) >= MAX_TAGS:
                break
    if not tags:
        tags = DEFAULT_TAGS[:MAX_TAGS]

    # Extract article body content
    article_content = soup.find("div", class_="article-content")
    if not article_content:
        article_content = soup.find("article")
    if not article_content:
        article_content = soup.find("main")

    if article_content:
        # Remove non-content elements
        for selector in ["footer", "nav", "script", "style", "noscript",
                         ".article-footer", ".article-nav", ".share-buttons",
                         ".related-reading", ".faq-section", ".article-meta"]:
            for el in article_content.select(selector):
                el.decompose()

        # Convert relative URLs to absolute
        for img in article_content.find_all("img"):
            src = img.get("src", "")
            if src.startswith("/"):
                img["src"] = SITE_BASE_URL + src

        for a in article_content.find_all("a"):
            href = a.get("href", "")
            if href.startswith("/"):
                a["href"] = SITE_BASE_URL + href

        # Convert HTML to Markdown
        h = html2text.HTML2Text()
        h.body_width = 0  # No line wrapping
        h.ignore_links = False
        h.ignore_images = False
        body_markdown = h.handle(str(article_content))
        body_markdown = body_markdown.strip()
    else:
        body_markdown = description

    # Add canonical source attribution
    body_markdown += f"\n\n---\n*Originally published at [{canonical_url}]({canonical_url})*\n"

    return {
        "title": title,
        "content_format": "markdown",
        "content": body_markdown,
        "canonical_url": canonical_url,
        "tags": tags,
        "publish_status": "draft",  # Always draft for manual review
        "license": "all-rights-reserved",
        "description": description,
        "cover_image": cover_image,
    }


def publish_to_medium(api_key, author_id, article_data, dry_run=False):
    """Publish a single article to Medium."""
    if dry_run:
        print(f"\n[DRY RUN] Would publish to Medium:")
        print(f"  Title: {article_data['title']}")
        print(f"  Tags: {article_data['tags']}")
        print(f"  Canonical: {article_data['canonical_url']}")
        print(f"  Content length: {len(article_data['content'])} chars")
        return True

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    payload = {
        "title": article_data["title"],
        "contentFormat": article_data["content_format"],
        "content": article_data["content"],
        "canonicalUrl": article_data["canonical_url"],
        "tags": article_data["tags"],
        "publishStatus": article_data["publish_status"],
        "license": article_data["license"],
    }

    try:
        resp = requests.post(
            f"{MEDIUM_API_BASE}/users/{author_id}/posts",
            headers=headers,
            json=payload,
            timeout=60,
        )

        if resp.status_code == 201:
            data = resp.json().get("data", {})
            article_url = data.get("url", "unknown")
            print(f"  Published as draft: {article_url}")
            return True
        else:
            print(f"  ERROR: API returned {resp.status_code}")
            print(f"  Response: {resp.text[:500]}")
            return False

    except requests.RequestException as e:
        print(f"  ERROR: Request failed: {e}")
        return False


def get_git_changed_files(commits=1):
    """Get list of HTML files changed in recent git commits."""
    try:
        result = subprocess.run(
            ["git", "log", f"-{commits}", "--name-only", "--pretty=format:", "--diff-filter=A"],
            capture_output=True, text=True, check=True,
            cwd=Path(__file__).parent.parent,
        )
        files = [f.strip() for f in result.stdout.split("\n") if f.strip()]
        # Filter to blog articles only
        article_files = [f for f in files if f.startswith("blog/articles/") and f.endswith(".html")]
        return [Path(f) for f in article_files]
    except subprocess.CalledProcessError:
        return []


def main():
    parser = argparse.ArgumentParser(description="Publish Beehive Strategy blog articles to Medium")
    parser.add_argument("--slug", help="Article slug (filename without .html)")
    parser.add_argument("--git-diff", action="store_true", help="Publish articles from recent git commits")
    parser.add_argument("--commits", type=int, default=1, help="Number of commits to check (with --git-diff)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be published without posting")
    parser.add_argument("--all", action="store_true", help="Publish all articles (use with caution)")
    args = parser.parse_args()

    if not any([args.slug, args.git_diff, args.dry_run, args.all]):
        parser.print_help()
        sys.exit(1)

    # Get credentials (skip in dry run)
    if args.dry_run:
        api_key = "dry-run"
        author_id = "dry-run"
    else:
        api_key = get_api_key()
        author_id = get_author_id(api_key)

    # Get existing articles to avoid duplicates
    existing_urls = get_published_articles(api_key, author_id)

    # Determine which articles to publish
    articles_to_publish = []

    if args.slug:
        article_path = BLOG_DIR / f"{args.slug}.html"
        if article_path.exists():
            articles_to_publish = [article_path]
        else:
            print(f"ERROR: Article not found: {article_path}")
            sys.exit(1)

    elif args.git_diff:
        articles_to_publish = get_git_changed_files(args.commits)
        if not articles_to_publish:
            print("No new articles found in recent commits")
            return

    elif args.all:
        articles_to_publish = sorted(BLOG_DIR.glob("*.html"))
        print(f"Found {len(articles_to_publish)} total articles")

    elif args.dry_run:
        # Show last 3 articles that would be published
        articles_to_publish = sorted(BLOG_DIR.glob("*.html"))[-3:]

    print(f"\n{'='*60}")
    print(f"Medium Auto-Publish — Beehive Strategy")
    print(f"{'='*60}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'PUBLISH'}")
    print(f"Articles to process: {len(articles_to_publish)}")
    print(f"Existing articles (skip duplicates): {len(existing_urls)}")
    print(f"{'='*60}\n")

    published_count = 0
    skipped_count = 0
    failed_count = 0

    for article_path in articles_to_publish:
        slug = article_path.stem
        print(f"Processing: {slug}")

        try:
            article_data = parse_article(article_path)
        except Exception as e:
            print(f"  ERROR: Failed to parse article: {e}")
            failed_count += 1
            continue

        # Check for duplicates
        if article_data["canonical_url"] in existing_urls:
            print(f"  SKIP: Already published on Medium")
            skipped_count += 1
            continue

        # Publish
        success = publish_to_medium(api_key, author_id, article_data, dry_run=args.dry_run)

        if success:
            published_count += 1
            if not args.dry_run:
                existing_urls.add(article_data["canonical_url"])
                save_published_state(existing_urls)
        else:
            failed_count += 1

    # Summary
    print(f"\n{'='*60}")
    print(f"Summary: {published_count} published, {skipped_count} skipped, {failed_count} failed")
    if published_count > 0 and not args.dry_run:
        print(f"Review your drafts at: https://medium.com/me/stories/drafts")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
