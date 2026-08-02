#!/usr/bin/env python3
"""
X.com (Twitter) Auto-Post Script for Beehive Strategy Blog

Posts a tweet with a link to new blog articles. Uses X API v2 with
OAuth 1.0a User Context (tokens don't expire, unlike LinkedIn's 60-day limit).

Free tier: 500 posts/month — more than enough for blog cross-posting.

Usage:
  # Post tweet for specific article by slug
  python3 scripts/x_post.py --slug what-is-conversational-bi

  # Post tweets for articles changed in the latest git commit
  python3 scripts/x_post.py --git-diff

  # Post tweets from the last N commits
  python3 scripts/x_post.py --git-diff --commits 3

  # Dry run (show what would be posted without tweeting)
  python3 scripts/x_post.py --dry-run

Environment variables:
  X_API_KEY            - X.com API Key (Consumer Key)
  X_API_KEY_SECRET     - X.com API Key Secret (Consumer Secret)
  X_ACCESS_TOKEN       - X.com Access Token
  X_ACCESS_TOKEN_SECRET - X.com Access Token Secret

Get these at: https://developer.x.com/en/portal/dashboard
  1. Create a Project and App
  2. Set User authentication settings to "Read and Write"
  3. Generate Access Token and Secret
  4. Use OAuth 1.0a User Context tokens
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# --- Configuration ---
X_API_BASE = "https://api.x.com/2"
SITE_BASE_URL = "https://www.beehivestrategy.com"
BLOG_DIR = Path(__file__).parent.parent / "blog" / "articles"
MAX_TWEET_LENGTH = 280  # X.com character limit

# Hashtag suggestions based on article keywords
HASHTAG_MAP = {
    "conversational bi": "#ConversationalBI",
    "ai analytics": "#AI",
    "enterprise bi": "#BusinessIntelligence",
    "data democratisation": "#Data",
    "mcp": "#MCP",
    "model context protocol": "#MCP",
    "data governance": "#DataGovernance",
    "ai governance": "#AIGovernance",
    "enterprise ai": "#EnterpriseAI",
    "rag": "#RAG",
    "retail analytics": "#RetailAnalytics",
    "manufacturing": "#Manufacturing",
    "predictive maintenance": "#PredictiveMaintenance",
    "ai strategy": "#AIStrategy",
    "data strategy": "#DataStrategy",
    "compliance": "#Compliance",
    "gdpr": "#GDPR",
    "pipl": "#PIPL",
    "data privacy": "#DataPrivacy",
    "cybersecurity": "#Cybersecurity",
    "text-to-sql": "#TextToSQL",
    "semantic layer": "#SemanticLayer",
    "data catalog": "#DataCatalog",
    "ai agents": "#AIAgents",
    "agentic ai": "#AgenticAI",
    "vector database": "#VectorDB",
    "llm": "#LLM",
    "digital transformation": "#DigitalTransformation",
    "business intelligence": "#BI",
    "self-service analytics": "#SelfServiceAnalytics",
}

DEFAULT_HASHTAGS = ["#AI", "#DataAnalytics", "#BusinessIntelligence"]


def get_credentials():
    """Get X.com API credentials from environment."""
    creds = {
        "api_key": os.environ.get("X_API_KEY"),
        "api_secret": os.environ.get("X_API_KEY_SECRET"),
        "access_token": os.environ.get("X_ACCESS_TOKEN"),
        "access_token_secret": os.environ.get("X_ACCESS_TOKEN_SECRET"),
    }

    missing = [k for k, v in creds.items() if not v]
    if missing:
        print("ERROR: Missing X.com API credentials:")
        for k in missing:
            env_var = f"X_{k.upper()}" if "api" in k else f"X_{k.upper()}"
            print(f"  {env_var}")
        print("\nGet these at: https://developer.x.com/en/portal/dashboard")
        sys.exit(1)

    return creds


def get_posted_articles():
    """Load previously posted article URLs to avoid duplicates."""
    state_file = Path(__file__).parent / ".x_posted.json"
    if state_file.exists():
        try:
            return set(json.loads(state_file.read_text()))
        except json.JSONDecodeError:
            pass
    return set()


def save_posted_state(posted_urls):
    """Save posted articles state to prevent duplicates."""
    state_file = Path(__file__).parent / ".x_posted.json"
    state_file.write_text(json.dumps(list(posted_urls), indent=2))


def parse_article(html_path):
    """
    Parse a blog article HTML file and extract data for X.com posting.

    Returns dict with: title, url, description, hashtags
    """
    html_content = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract title
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else html_path.stem
    title = re.sub(r"\s*[|\-]\s*Beehive Strategy.*$", "", title)

    # Extract canonical URL
    canonical_tag = soup.find("link", attrs={"rel": "canonical"})
    url = canonical_tag["href"] if canonical_tag else f"{SITE_BASE_URL}/blog/articles/{html_path.stem}"

    # Extract meta description for tweet text
    desc_tag = soup.find("meta", attrs={"name": "description"})
    description = desc_tag["content"] if desc_tag else ""

    # Extract hashtags from keywords
    keywords_tag = soup.find("meta", attrs={"name": "keywords"})
    hashtags = []
    if keywords_tag:
        raw_keywords = [k.strip().lower() for k in keywords_tag["content"].split(",")]
        for kw in raw_keywords:
            if kw in HASHTAG_MAP and HASHTAG_MAP[kw] not in hashtags:
                hashtags.append(HASHTAG_MAP[kw])
            if len(hashtags) >= 3:  # Max 3 hashtags to keep tweet readable
                break
    if not hashtags:
        hashtags = DEFAULT_HASHTAGS[:3]

    return {
        "title": title,
        "url": url,
        "description": description,
        "hashtags": hashtags,
    }


def craft_tweet(article_data):
    """
    Craft a tweet from article data.
    Format: Hook + title + URL + hashtags
    Stays within 280 character limit.
    """
    title = article_data["title"]
    url = article_data["url"]
    description = article_data["description"]
    hashtags = " ".join(article_data["hashtags"])

    # Use description as hook if it's short enough, otherwise use title
    # Tweet structure: [hook/title] + [URL] + [hashtags]
    url_len = len(url) + 1  # +1 for space
    hashtag_len = len(hashtags) + 1  # +1 for space

    # Start with a hook based on the description
    if description and len(description) > 20:
        # Use first sentence as hook
        first_sentence = description.split(".")[0] + "."
        hook = first_sentence
    else:
        hook = ""

    # Build tweet, trimming to fit
    remaining = MAX_TWEET_LENGTH - url_len - hashtag_len

    if hook:
        if len(hook) + len(title) + 2 <= remaining:
            # Hook + title
            tweet_text = f"{hook}\n\n{title}"
        elif len(hook) <= remaining - 5:
            # Just hook, truncate if needed
            tweet_text = hook[:remaining - 3] + "..." if len(hook) > remaining else hook
        else:
            # Fallback to title only
            tweet_text = title[:remaining - 3] + "..." if len(title) > remaining else title
    else:
        tweet_text = title[:remaining - 3] + "..." if len(title) > remaining else title

    tweet = f"{tweet_text}\n{url}\n{hashtags}"

    # Final safety check
    if len(tweet) > MAX_TWEET_LENGTH:
        # Truncate the text part, keeping URL and hashtags
        text_budget = MAX_TWEET_LENGTH - url_len - hashtag_len
        tweet_text = title[:text_budget - 3] + "..."
        tweet = f"{tweet_text}\n{url}\n{hashtags}"

    return tweet


def post_to_x(creds, tweet_text, dry_run=False):
    """Post a tweet using X API v2 with OAuth 1.0a."""
    if dry_run:
        print(f"\n[DRY RUN] Would post tweet:")
        print(f"  Length: {len(tweet_text)} chars")
        print(f"  Content: {tweet_text}")
        return True

    # Use OAuth 1.0a User Context via requests-oauthlib
    # Fallback to manual signing if requests_oauthlib not available
    try:
        from requests_oauthlib import OAuth1

        auth = OAuth1(
            creds["api_key"],
            creds["api_secret"],
            creds["access_token"],
            creds["access_token_secret"],
        )

        payload = {
            "text": tweet_text,
        }

        resp = requests.post(
            f"{X_API_BASE}/tweets",
            auth=auth,
            json=payload,
            timeout=30,
        )

        if resp.status_code == 201:
            data = resp.json()
            tweet_id = data.get("data", {}).get("id", "unknown")
            print(f"  Posted tweet ID: {tweet_id}")
            return True
        else:
            print(f"  ERROR: API returned {resp.status_code}")
            print(f"  Response: {resp.text[:500]}")
            return False

    except ImportError:
        # Fallback: use curl with manual OAuth signing
        print("  NOTE: requests-oauthlib not installed, using curl fallback")
        return post_to_x_curl(creds, tweet_text)


def post_to_x_curl(creds, tweet_text):
    """Fallback: post tweet using curl with Python OAuth signing."""
    # Build a simple curl command using the X API
    # This uses the Bearer token approach as fallback
    import urllib.parse

    # Escape tweet text for JSON
    escaped_text = json.dumps(tweet_text)

    # Use Python's urllib for the request
    import urllib.request

    # We need to sign the request properly with OAuth 1.0a
    # Use the hmac-based approach
    import hashlib
    import hmac
    import base64
    import secrets
    from urllib.parse import quote

    method = "POST"
    url = f"{X_API_BASE}/tweets"
    params = {
        "include_entities": "true",
    }

    # OAuth parameters
    oauth_params = {
        "oauth_consumer_key": creds["api_key"],
        "oauth_nonce": secrets.token_hex(16),
        "oauth_signature_method": "HMAC-SHA256",
        "oauth_timestamp": str(int(time.time())),
        "oauth_token": creds["access_token"],
        "oauth_version": "1.0",
    }

    # Create signature base string
    all_params = {**params, **oauth_params}
    sorted_params = sorted(all_params.items())
    param_string = "&".join([f"{quote(k, safe='')}={quote(v, safe='')}" for k, v in sorted_params])
    base_string = f"{method}&{quote(url, safe='')}&{quote(param_string, safe='')}"

    # Create signing key
    signing_key = f"{quote(creds['api_secret'], safe='')}&{quote(creds['access_token_secret'], safe='')}"

    # Generate signature
    signature = base64.b64encode(
        hmac.new(signing_key.encode(), base_string.encode(), hashlib.sha256).digest()
    ).decode()

    oauth_params["oauth_signature"] = signature

    # Build Authorization header
    auth_header = "OAuth " + ", ".join(
        [f'{quote(k, safe="")}="{quote(v, safe="")}"' for k, v in sorted(oauth_params.items())]
    )

    # Make request
    data = json.dumps({"text": tweet_text}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": auth_header,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status == 201:
                data = json.loads(response.read())
                tweet_id = data.get("data", {}).get("id", "unknown")
                print(f"  Posted tweet ID: {tweet_id}")
                return True
            else:
                print(f"  ERROR: HTTP {response.status}")
                return False
    except urllib.error.HTTPError as e:
        print(f"  ERROR: HTTP {e.code}")
        print(f"  Response: {e.read().decode()[:500]}")
        return False
    except Exception as e:
        print(f"  ERROR: {e}")
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
        article_files = [f for f in files if f.startswith("blog/articles/") and f.endswith(".html")]
        return [Path(f) for f in article_files]
    except subprocess.CalledProcessError:
        return []


def main():
    parser = argparse.ArgumentParser(description="Post Beehive Strategy blog articles to X.com")
    parser.add_argument("--slug", help="Article slug (filename without .html)")
    parser.add_argument("--git-diff", action="store_true", help="Post tweets for articles from recent git commits")
    parser.add_argument("--commits", type=int, default=1, help="Number of commits to check (with --git-diff)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be posted without tweeting")
    args = parser.parse_args()

    if not any([args.slug, args.git_diff, args.dry_run]):
        parser.print_help()
        sys.exit(1)

    # Get credentials (skip in dry run)
    creds = get_credentials() if not args.dry_run else None

    # Get existing posts to avoid duplicates
    posted_urls = get_posted_articles()

    # Determine which articles to post
    articles_to_post = []

    if args.slug:
        article_path = BLOG_DIR / f"{args.slug}.html"
        if article_path.exists():
            articles_to_post = [article_path]
        else:
            print(f"ERROR: Article not found: {article_path}")
            sys.exit(1)

    elif args.git_diff:
        articles_to_post = get_git_changed_files(args.commits)
        if not articles_to_post:
            print("No new articles found in recent commits")
            return

    elif args.dry_run:
        # Show last 3 articles that would be posted
        articles_to_post = sorted(BLOG_DIR.glob("*.html"))[-3:]

    print(f"\n{'='*60}")
    print(f"X.com Auto-Post — Beehive Strategy")
    print(f"{'='*60}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'POST'}")
    print(f"Articles to process: {len(articles_to_post)}")
    print(f"Previously posted (skip duplicates): {len(posted_urls)}")
    print(f"{'='*60}\n")

    posted_count = 0
    skipped_count = 0
    failed_count = 0

    for article_path in articles_to_post:
        slug = article_path.stem
        print(f"Processing: {slug}")

        try:
            article_data = parse_article(article_path)
        except Exception as e:
            print(f"  ERROR: Failed to parse article: {e}")
            failed_count += 1
            continue

        # Check for duplicates
        if article_data["url"] in posted_urls:
            print(f"  SKIP: Already posted to X.com")
            skipped_count += 1
            continue

        # Craft tweet
        tweet_text = craft_tweet(article_data)

        # Post
        if args.dry_run:
            success = post_to_x(creds, tweet_text, dry_run=True)
        else:
            success = post_to_x(creds, tweet_text)

        if success:
            posted_count += 1
            if not args.dry_run:
                posted_urls.add(article_data["url"])
                save_posted_state(posted_urls)
                # Rate limit: wait 2 seconds between posts
                if len(articles_to_post) > 1:
                    time.sleep(2)
        else:
            failed_count += 1

    # Summary
    print(f"\n{'='*60}")
    print(f"Summary: {posted_count} posted, {skipped_count} skipped, {failed_count} failed")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
