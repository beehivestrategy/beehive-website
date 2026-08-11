#!/usr/bin/env python3
"""
Daily Article Generator for Beehive Strategy Blog

Uses OpenRouter API (free models) to generate SEO-optimised blog articles
and create HTML files for the static website.

Usage:
  python3 scripts/generate_daily_article.py [--dry-run] [--topic "AI Strategy"]

Environment variables:
  OPENROUTER_API_KEY - OpenRouter API key (required)
  OPENROUTER_MODEL   - Model to use (default: meta-llama/llama-3.3-70b-instruct:free)
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from html import escape

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests")
    sys.exit(1)

# --- Configuration ---
SITE_BASE_URL = "https://www.beehivestrategy.com"
BLOG_DIR = Path(__file__).parent.parent / "blog" / "articles"
BLOG_CN_DIR = Path(__file__).parent.parent / "zh-cn" / "blog" / "articles"
BLOG_TW_DIR = Path(__file__).parent.parent / "zh-tw" / "blog" / "articles"
BLOG_INDEX = Path(__file__).parent.parent / "blog.html"
SITEMAP = Path(__file__).parent.parent / "sitemap.xml"
SITEMAP_EN = Path(__file__).parent.parent / "sitemap-blog-en.xml"
SITEMAP_ZHCN = Path(__file__).parent.parent / "sitemap-blog-zhcn.xml"
SITEMAP_ZHTW = Path(__file__).parent.parent / "sitemap-blog-zhtw.xml"
SITEMAP_INDEX = Path(__file__).parent.parent / "sitemap-index.xml"
FEED_XML = Path(__file__).parent.parent / "blog" / "feed.xml"

# OpenRouter config
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = os.environ.get("OPENROUTER_MODEL", "nvidia/nemotron-3-super-120b-a12b:free")

# Fallback free models (tried in order if primary fails)
FALLBACK_MODELS = [
    "nvidia/nemotron-3-super-120b-a12b:free",
    "google/gemma-4-31b-it:free",
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    "google/gemma-4-26b-a4b-it:free",
    "openai/gpt-oss-20b:free",
]

# Article topics rotation (ensures variety)
TOPICS = [
    "Conversational BI and natural language analytics for enterprise decision-making",
    "AI governance frameworks for enterprise data platforms",
    "Data mesh architecture and federated governance",
    "RAG (Retrieval-Augmented Generation) for enterprise knowledge management",
    "MCP (Model Context Protocol) for AI agent integration",
    "Semantic layer design for self-service analytics",
    "Data quality automation and observability",
    "AI strategy roadmap from pilot to production",
    "Vector databases and embeddings for enterprise search",
    "Text-to-SQL transformation in modern BI platforms",
    "Predictive analytics for supply chain optimisation",
    "Data democratisation and self-service analytics adoption",
    "Agentic AI workflows for enterprise automation",
    "Data catalog and lineage tracking for compliance",
    "Real-time data streaming for AI-powered decisions",
    "Edge computing for AI at scale",
    "Privacy-preserving analytics and differential privacy",
    "MLOps and production AI system reliability",
    "Small language models for cost-effective enterprise AI",
    "AI ethics and bias detection in training data",
]

# Company info
COMPANY_EN = "Beehive Strategy Limited"
COMPANY_CN = "深圳蜂启咨询有限公司"
AUTHOR_NAME = "Kenneth Kwok"
AUTHOR_TITLE = "Founder & CEO"
PUBLISH_TIME = "09:00:00+08:00"


def get_api_key():
    """Get OpenRouter API key from environment."""
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("ERROR: OPENROUTER_API_KEY environment variable not set")
        print("Get a free key at: https://openrouter.ai/keys")
        sys.exit(1)
    return key


def call_openrouter(api_key, prompt, temperature=0.7, model=None):
    """Call OpenRouter API for text generation, with fallback models."""
    models_to_try = [model or DEFAULT_MODEL] + [m for m in FALLBACK_MODELS if m != (model or DEFAULT_MODEL)]
    
    for try_model in models_to_try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://www.beehivestrategy.com",
            "X-Title": "Beehive Strategy Article Generator",
        }
        payload = {
            "model": try_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
        }

        try:
            resp = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=120)
            
            if resp.status_code == 404:
                print(f"  Model {try_model} unavailable, trying next...")
                continue
            
            resp.raise_for_status()
            data = resp.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

            # Strip markdown code blocks if present
            if content.startswith("```json"):
                content = re.sub(r"^```json\n?", "", content)
                content = re.sub(r"\n?```$", "", content)
            elif content.startswith("```"):
                content = re.sub(r"^```\n?", "", content)
                content = re.sub(r"\n?```$", "", content)

            if try_model != (model or DEFAULT_MODEL):
                print(f"  Used fallback model: {try_model}")
            return content
        except requests.RequestException as e:
            if hasattr(e, "response") and e.response is not None and e.response.status_code == 404:
                print(f"  Model {try_model} unavailable, trying next...")
                continue
            print(f"ERROR: OpenRouter API call failed with {try_model}: {e}")
            if hasattr(e, "response") and e.response is not None:
                print(f"Response: {e.response.text[:500]}")
            continue
    
    print("ERROR: All models failed")
    return None


def generate_article_content(api_key, topic, dry_run=False):
    """Generate article content using AI."""
    today = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")

    prompt = f"""You are a top-tier enterprise Data & AI consultant writing for the Beehive Strategy blog.
Write a professional, compelling, and actionable SEO article about: {topic}

The article must be:
- 1000-1500 words
- Targeted at enterprise leaders and decision-makers
- Include practical insights and actionable recommendations
- Use British English spelling
- Include at least 3 sections with headings
- Include 2-3 FAQs

Generate the article in JSON format (NO markdown, NO backticks):
{{
  "slug": "kebab-case-url-slug-max-60-chars",
  "title": "Compelling Article Title (max 60 chars)",
  "description": "Meta description for SEO (max 155 chars)",
  "keywords": "comma-separated, seo, keywords, max, 6",
  "category": "one of: Conversational BI, AI Strategy, Data Governance, AI Governance, Data Quality, Analytics, Machine Learning",
  "lead": "2-3 sentence article lead paragraph that hooks the reader",
  "tldr": "Key statistics or takeaways with sources (1-2 sentences)",
  "sections": [
    {{
      "heading": "Section Heading",
      "content": "Full section content as HTML (use <p>, <h3>, <ul>, <li>, <blockquote>, <table> tags as needed). Write 2-4 paragraphs per section."
    }}
  ],
  "faqs": [
    {{
      "question": "Relevant FAQ question?",
      "answer": "Clear, professional answer (2-3 sentences)"
    }}
  ]
}}

Today's date is {today}. Return ONLY valid JSON."""

    if dry_run:
        # Return a minimal mock for testing
        return {
            "slug": f"dry-run-article-{today}",
            "title": f"Dry Run: {topic[:40]}",
            "description": f"Dry run article about {topic}",
            "keywords": "ai, analytics, dry run",
            "category": "AI Strategy",
            "lead": "This is a dry run article for testing.",
            "tldr": "Dry run - no actual content generated.",
            "sections": [{"heading": "Test Section", "content": "<p>Test content.</p>"}],
            "faqs": [{"question": "Test?", "answer": "Yes."}],
        }

    print(f"Generating article about: {topic}")
    raw = call_openrouter(api_key, prompt, temperature=0.7)

    if not raw:
        print("ERROR: Failed to generate article content")
        return None

    try:
        article = json.loads(raw)
        print(f"Generated: {article.get('title', 'Unknown')}")
        return article
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse AI response as JSON: {e}")
        print(f"Raw response (first 500 chars): {raw[:500]}")
        return None


def translate_article(api_key, article, target_lang, dry_run=False):
    """Translate article content to target language."""
    if dry_run:
        return article  # Return as-is for dry run

    lang_name = {
        "zh-CN": "Simplified Chinese (zh-CN)",
        "zh-TW": "Traditional Chinese (zh-TW)",
    }.get(target_lang, target_lang)

    prompt = f"""You are an expert technical translator. Translate the following JSON article into {lang_name}.
Maintain the EXACT JSON structure and keys. Only translate the string values.
Do NOT translate the "slug" field.
Use professional enterprise terminology appropriate for {lang_name} audiences.

Article JSON:
{json.dumps(article, ensure_ascii=False, indent=2)}

Return ONLY valid JSON without markdown formatting."""

    print(f"Translating to {target_lang}...")
    raw = call_openrouter(api_key, prompt, temperature=0.3)

    if not raw:
        print(f"WARNING: Translation to {target_lang} failed, using English")
        return article

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print(f"WARNING: Failed to parse {target_lang} translation, using English")
        return article


def generate_html_article(article, lang="en", date_str=None):
    """Generate full HTML article from article data."""
    if date_str is None:
        date_str = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")

    slug = article["slug"]
    title = escape(article["title"])
    description = escape(article["description"])
    keywords = escape(article["keywords"])
    category = escape(article.get("category", "AI Strategy"))
    lead = article.get("lead", description)
    tldr = article.get("tldr", "")
    sections = article.get("sections", [])
    faqs = article.get("faqs", [])

    # Determine language-specific paths
    if lang == "en":
        lang_prefix = ""
        lang_code = "en"
        lang_label = "EN"
        lang_attr = "en"
        dir_attr = "ltr"
        og_locale = "en_US"
        company = COMPANY_EN
    elif lang == "zh-CN":
        lang_prefix = "/zh-cn"
        lang_code = "zh-cn"
        lang_label = "简"
        lang_attr = "zh-CN"
        dir_attr = "ltr"
        og_locale = "zh_CN"
        company = COMPANY_CN
    elif lang == "zh-TW":
        lang_prefix = "/zh-tw"
        lang_code = "zh-tw"
        lang_label = "繁"
        lang_attr = "zh-TW"
        dir_attr = "ltr"
        og_locale = "zh_TW"
        company = COMPANY_CN
    else:
        lang_prefix = ""
        lang_code = "en"
        lang_label = "EN"
        lang_attr = "en"
        dir_attr = "ltr"
        og_locale = "en_US"
        company = COMPANY_EN

    canonical = f"{SITE_BASE_URL}{lang_prefix}/blog/articles/{slug}"
    publish_datetime = f"{date_str}T{PUBLISH_TIME}"

    # Build sections HTML
    sections_html = ""
    for section in sections:
        sections_html += f"\n          <h2>{escape(section['heading'])}</h2>\n          {section['content']}\n"

    # Build FAQs HTML
    faqs_html = ""
    faq_jsonld = []
    for faq in faqs:
        faqs_html += f'\n          <div class="faq-item">\n            <h3 class="faq-question">{escape(faq["question"])}</h3>\n            <p class="faq-answer">{escape(faq["answer"])}</p>\n          </div>'
        faq_jsonld.append({
            "@type": "Question",
            "name": faq["question"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["answer"]
            }
        })

    # Build FAQ JSON-LD
    faq_jsonld_str = ""
    if faq_jsonld:
        faq_jsonld_str = ",\n    {\n      \"@type\": \"FAQPage\",\n      \"mainEntity\": " + json.dumps(faq_jsonld, ensure_ascii=False, indent=6) + "\n    }"

    # Build keywords for article tags
    kw_list = [k.strip() for k in keywords.split(",")]
    article_tags_html = "\n".join(
        f'      <span class="article-tag">{escape(k)}</span>' for k in kw_list[:5]
    )

    html = f"""<!DOCTYPE html>
<html lang="{lang_attr}" dir="{dir_attr}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">

  <title>{title} | Beehive Strategy</title>
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keywords}">
  <meta name="author" content="{company}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">

  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="en" href="{SITE_BASE_URL}/blog/articles/{slug}">
  <link rel="alternate" hreflang="zh-CN" href="{SITE_BASE_URL}/zh-cn/blog/articles/{slug}">
  <link rel="alternate" hreflang="zh-TW" href="{SITE_BASE_URL}/zh-tw/blog/articles/{slug}">
  <link rel="alternate" hreflang="x-default" href="{SITE_BASE_URL}/blog/articles/{slug}">

  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Beehive Strategy">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:locale" content="{og_locale}">
  <meta property="article:published_time" content="{publish_datetime}">
  <meta property="article:author" content="Beehive Strategy">
  <meta property="article:section" content="{category}">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@beehivestrategy">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">

  <link rel="alternate" type="application/rss+xml" title="Beehive Strategy Blog RSS Feed" href="{SITE_BASE_URL}/blog/feed.xml">

  <meta name="theme-color" content="#0a0e0d">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32x32.png">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/styles.css?v=20260804">

  <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "BlogPosting",
      "headline": "{title}",
      "description": "{description}",
      "datePublished": "{publish_datetime}",
      "dateModified": "{publish_datetime}",
      "articleSection": "{category}",
      "keywords": "{keywords}",
      "inLanguage": "{lang_attr}",
      "author": {{
        "@type": "Person",
        "name": "{AUTHOR_NAME}",
        "url": "{SITE_BASE_URL}/about",
        "jobTitle": "{AUTHOR_TITLE}"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "{company}",
        "url": "{SITE_BASE_URL}"
      }},
      "mainEntityOfPage": {{
        "@type": "WebPage",
        "@id": "{canonical}"
      }}
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE_BASE_URL}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Blog", "item": "{SITE_BASE_URL}/blog/" }},
        {{ "@type": "ListItem", "position": 3, "name": "{title}", "item": "{canonical}" }}
      ]
    }}{faq_jsonld_str}
  ]
}}
  </script>
</head>
<body>
  <div class="scroll-progress" id="scroll-progress" aria-hidden="true"></div>
  <header class="header" id="header" role="banner">
    <div class="header-inner">
      <a href="/" class="logo" aria-label="Beehive Strategy Home">
        <img src="/assets/images/beehive-logo.png" alt="Beehive Strategy Logo" width="144" height="36" loading="eager">
      </a>
      <nav class="nav-desktop" role="navigation" aria-label="Main navigation">
        <a href="{lang_prefix}/solution" class="nav-link">Solution</a>
        <a href="{lang_prefix}/services" class="nav-link">Services</a>
        <a href="{lang_prefix}/industries" class="nav-link">Industries</a>
        <a href="{lang_prefix}/case-studies" class="nav-link">Case Studies</a>
        <a href="{lang_prefix}/pricing" class="nav-link">Pricing</a>
        <a href="{lang_prefix}/about" class="nav-link">About</a>
        <a href="{lang_prefix}/blog" class="nav-link active">Blog</a>
      </nav>
      <div class="nav-cta">
        <div class="lang-switcher" id="lang-switcher">
          <button class="lang-switcher-btn" id="lang-switcher-btn" aria-label="Switch language" aria-expanded="false">
            <span>{lang_label}</span>
          </button>
          <div class="lang-switcher-dropdown" role="menu">
            <a href="/blog/articles/{slug}" role="menuitem" class="{'active' if lang == 'en' else ''}" data-lang="en"><span>English</span></a>
            <a href="/zh-cn/blog/articles/{slug}" role="menuitem" class="{'active' if lang == 'zh-CN' else ''}" data-lang="zh-cn"><span>简体中文</span></a>
            <a href="/zh-tw/blog/articles/{slug}" role="menuitem" class="{'active' if lang == 'zh-TW' else ''}" data-lang="zh-tw"><span>繁體中文</span></a>
          </div>
        </div>
        <a href="{lang_prefix}/contact" class="btn btn-primary">Book a Demo</a>
      </div>
      <div class="nav-mobile">
        <button class="hamburger" id="hamburger" aria-label="Toggle menu" aria-expanded="false">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </header>

  <div class="mobile-menu" id="mobile-menu" aria-hidden="true">
    <a href="{lang_prefix}/solution">Solution</a>
    <a href="{lang_prefix}/services">Services</a>
    <a href="{lang_prefix}/industries">Industries</a>
    <a href="{lang_prefix}/case-studies">Case Studies</a>
    <a href="{lang_prefix}/pricing">Pricing</a>
    <a href="{lang_prefix}/about">About</a>
    <a href="{lang_prefix}/blog">Blog</a>
    <a href="{lang_prefix}/contact" class="btn btn-primary btn-lg">Book a Demo</a>
  </div>

  <nav aria-label="Breadcrumb" class="breadcrumb-nav">
    <div class="container">
      <ol>
        <li><a href="{SITE_BASE_URL}/">Home</a></li>
        <li><a href="{SITE_BASE_URL}{lang_prefix}/blog">Blog</a></li>
        <li aria-current="page">{title}</li>
      </ol>
    </div>
  </nav>

  <main role="main">
    <article class="article">
      <div class="container">
        <div class="article-content">
          <p class="article-lead">{lead}</p>
          <div class="article-tldr"><strong>Key Statistics:</strong> {tldr}</div>
          {sections_html}
          {faqs_html if faqs_html else ''}
        </div>

        <footer class="article-footer">
          <div class="article-tags">
{article_tags_html}
          </div>
          <nav class="article-nav">
            <a href="{lang_prefix}/blog" class="btn btn-secondary">&larr; Back to All Articles</a>
          </nav>
        </footer>
      </div>
    </article>
  </main>

  <footer class="site-footer">
    <div class="container">
      <p>&copy; {datetime.now().year} {company}. All rights reserved.</p>
    </div>
  </footer>

  <script src="/js/main.js"></script>
</body>
</html>"""

    return html


def update_blog_index(article, date_str):
    """Add new article card to the blog index page."""
    if not BLOG_INDEX.exists():
        print(f"WARNING: Blog index not found at {BLOG_INDEX}")
        return

    html = BLOG_INDEX.read_text(encoding="utf-8")
    slug = article["slug"]
    title = escape(article["title"])
    description = escape(article["description"])
    category = escape(article.get("category", "AI Strategy"))

    # Create article card HTML
    card_html = f"""
    <article class="blog-card" data-date="{date_str}" data-category="{category.lower()}">
      <a href="/blog/articles/{slug}" class="blog-card-link">
        <div class="blog-card-content">
          <span class="blog-card-category">{category}</span>
          <h3 class="blog-card-title">{title}</h3>
          <p class="blog-card-excerpt">{description}</p>
          <time class="blog-card-date" datetime="{date_str}T{PUBLISH_TIME}">{date_str}</time>
        </div>
      </a>
    </article>"""

    # Insert after the first article card (newest first)
    # Look for the blog-cards container
    pattern = r'(<div[^>]*class="[^"]*blog-cards[^"]*"[^>]*>)'
    match = re.search(pattern, html)
    if match:
        insert_pos = match.end()
        html = html[:insert_pos] + "\n" + card_html + html[insert_pos:]
        BLOG_INDEX.write_text(html, encoding="utf-8")
        print(f"  Added article card to blog index")
    else:
        print(f"  WARNING: Could not find blog-cards container in index")


def update_sitemap(slug, date_str):
    """Add new article URLs to sitemap.xml and all sub-sitemaps."""
    urls = [
        f"{SITE_BASE_URL}/blog/articles/{slug}",
        f"{SITE_BASE_URL}/zh-cn/blog/articles/{slug}",
        f"{SITE_BASE_URL}/zh-tw/blog/articles/{slug}",
    ]

    # Update legacy combined sitemap.xml
    if SITEMAP.exists():
        xml = SITEMAP.read_text(encoding="utf-8")
        new_entries = ""
        for url in urls:
            new_entries += f"""
  <url>
    <loc>{url}</loc>
    <lastmod>{date_str}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>"""
        xml = xml.replace("</urlset>", new_entries + "\n</urlset>")
        SITEMAP.write_text(xml, encoding="utf-8")
        print(f"  Added 3 URLs to sitemap.xml")

    # Build hreflang alternates for sub-sitemaps
    alternates_xml = ""
    for lang_code, url in [("en", urls[0]), ("zh-CN", urls[1]), ("zh-TW", urls[2])]:
        alternates_xml += f'\n    <xhtml:link rel="alternate" hreflang="{lang_code}" href="{url}"/>'
    alternates_xml += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{urls[0]}"/>'

    # Update each sub-sitemap with proper hreflang annotations
    sub_sitemaps = [
        (SITEMAP_EN, urls[0]),
        (SITEMAP_ZHCN, urls[1]),
        (SITEMAP_ZHTW, urls[2]),
    ]

    for sitemap_path, url in sub_sitemaps:
        if sitemap_path.exists():
            xml = sitemap_path.read_text(encoding="utf-8")
            entry = f"""
  <url>
    <loc>{url}</loc>
    <lastmod>{date_str}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>{alternates_xml}
  </url>"""
            xml = xml.replace("</urlset>", entry + "\n</urlset>")
            sitemap_path.write_text(xml, encoding="utf-8")

    # Update sitemap-index.xml lastmod dates
    if SITEMAP_INDEX.exists():
        xml = SITEMAP_INDEX.read_text(encoding="utf-8")
        xml = re.sub(r"<lastmod>\d{4}-\d{2}-\d{2}</lastmod>", f"<lastmod>{date_str}</lastmod>", xml)
        SITEMAP_INDEX.write_text(xml, encoding="utf-8")

    print(f"  Added URLs to all sub-sitemaps with hreflang annotations")


def update_feed(article, date_str):
    """Add new article to RSS feed."""
    if not FEED_XML.exists():
        print(f"WARNING: Feed not found at {FEED_XML}")
        return

    xml = FEED_XML.read_text(encoding="utf-8")
    slug = article["slug"]
    title = escape(article["title"])
    description = escape(article["description"])
    canonical = f"{SITE_BASE_URL}/blog/articles/{slug}"
    pub_date = f"{date_str}T{PUBLISH_TIME}"

    new_item = f"""
    <item>
      <title>{title}</title>
      <link>{canonical}</link>
      <guid isPermaLink="true">{canonical}</guid>
      <description>{description}</description>
      <pubDate>{pub_date}</pubDate>
    </item>"""

    # Insert after <channel> opening or before first <item>
    if "<item>" in xml:
        xml = xml.replace("<item>", new_item + "\n    <item>", 1)
    else:
        xml = xml.replace("</channel>", new_item + "\n  </channel>")

    FEED_XML.write_text(xml, encoding="utf-8")
    print(f"  Added article to RSS feed")


def main():
    parser = argparse.ArgumentParser(description="Generate daily SEO article for Beehive Strategy blog")
    parser.add_argument("--dry-run", action="store_true", help="Generate without calling API or writing files")
    parser.add_argument("--topic", help="Specific topic to write about (default: rotated from list)")
    parser.add_argument("--no-translate", action="store_true", help="Skip Chinese translations")
    args = parser.parse_args()

    api_key = None if args.dry_run else get_api_key()

    # Determine topic
    if args.topic:
        topic = args.topic
    else:
        # Rotate based on day of year
        day_of_year = datetime.now().timetuple().tm_yday
        topic = TOPICS[day_of_year % len(TOPICS)]

    print(f"=== Daily Article Generation ===")
    print(f"Topic: {topic}")
    print(f"Model: {DEFAULT_MODEL}")
    print()

    # Generate English article
    article = generate_article_content(api_key, topic, dry_run=args.dry_run)
    if not article:
        print("FAILED: Could not generate article")
        sys.exit(1)

    # Validate slug
    slug = article.get("slug", "")
    if not slug or not re.match(r"^[a-z0-9-]+$", slug):
        # Generate slug from title
        slug = re.sub(r"[^a-z0-9]+", "-", article.get("title", "article").lower()).strip("-")[:60]
        article["slug"] = slug

    # Check for duplicate slug
    en_path = BLOG_DIR / f"{slug}.html"
    if en_path.exists():
        print(f"WARNING: Article already exists: {slug}. Adding date suffix.")
        date_suffix = datetime.now().strftime("%Y%m%d")
        slug = f"{slug}-{date_suffix}"
        article["slug"] = slug
        en_path = BLOG_DIR / f"{slug}.html"

    date_str = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")

    print(f"\nSlug: {slug}")
    print(f"Date: {date_str}")

    if args.dry_run:
        print(f"\n[DRY RUN] Would create:")
        print(f"  - {en_path}")
        print(f"  - {BLOG_CN_DIR}/{slug}.html")
        print(f"  - {BLOG_TW_DIR}/{slug}.html")
        print(f"  - Update blog index, sitemap, feed.xml")
        print(f"\nArticle title: {article.get('title', 'Unknown')}")
        print(f"Description: {article.get('description', 'N/A')}")
        return

    # Generate English HTML
    print("\n--- Generating English article ---")
    en_html = generate_html_article(article, lang="en", date_str=date_str)
    en_path.parent.mkdir(parents=True, exist_ok=True)
    en_path.write_text(en_html, encoding="utf-8")
    print(f"  Created: {en_path}")

    # Generate Chinese translations
    if not args.no_translate:
        for lang, lang_dir in [("zh-CN", BLOG_CN_DIR), ("zh-TW", BLOG_TW_DIR)]:
            print(f"\n--- Generating {lang} article ---")
            translated = translate_article(api_key, article, lang)
            html = generate_html_article(translated, lang=lang, date_str=date_str)
            lang_dir.mkdir(parents=True, exist_ok=True)
            (lang_dir / f"{slug}.html").write_text(html, encoding="utf-8")
            print(f"  Created: {lang_dir}/{slug}.html")

    # Update blog index, sitemap, feed
    print("\n--- Updating site files ---")
    update_blog_index(article, date_str)
    update_sitemap(slug, date_str)
    update_feed(article, date_str)

    print(f"\n=== SUCCESS: Article '{article['title']}' generated ===")
    print(f"URL: {SITE_BASE_URL}/blog/articles/{slug}")


if __name__ == "__main__":
    main()
