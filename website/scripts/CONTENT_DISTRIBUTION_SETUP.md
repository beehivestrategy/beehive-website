# Content Distribution Setup Guide

Zero-cost cross-platform content distribution for Beehive Strategy blog articles.

## Architecture Overview

```
New Blog Article (HTML)
        |
        v
  GitHub Actions (daily 09:00 HKT or on push)
        |
        +---> Dev.to (API, draft mode)
        +---> Medium (API, draft mode)
        +---> X.com (API, live tweet)
        +---> LinkedIn (via Zapier RSS, live post)
```

All articles are published as **drafts** on Dev.to and Medium (manual review before publishing).
X.com posts go live immediately. LinkedIn posts via Zapier RSS feed go live immediately.

## Required GitHub Secrets

Go to: GitHub repo → Settings → Secrets and variables → Actions → New repository secret

### 1. Dev.to (already configured)
| Secret Name | Value | Where to Get |
|-------------|-------|-------------|
| `DEVTO_API_KEY` | Your Dev.to API key | https://dev.to/settings/extensions → DEV Community API Keys |

### 2. Medium
| Secret Name | Value | Where to Get |
|-------------|-------|-------------|
| `MEDIUM_API_KEY` | Integration token | https://medium.com/me/settings → Integration Tokens → Get token |
| `MEDIUM_AUTHOR_ID` | Your author ID | Run: `curl -H "Authorization: Bearer YOUR_TOKEN" https://api.medium.com/v1/me` → look for `data.id` |

**Note:** Medium's API is officially deprecated (Jan 2023) but still operational. Tokens don't expire.

### 3. X.com (Twitter)
| Secret Name | Value | Where to Get |
|-------------|-------|-------------|
| `X_API_KEY` | Consumer API Key | https://developer.x.com/en/portal/dashboard |
| `X_API_KEY_SECRET` | Consumer API Secret | Same as above |
| `X_ACCESS_TOKEN` | Access Token | Same (generate under "Keys and tokens") |
| `X_ACCESS_TOKEN_SECRET` | Access Token Secret | Same as above |

**Setup steps:**
1. Go to https://developer.x.com/en/portal/dashboard
2. Create a Project (any name) and an App
3. Under "User authentication settings":
   - Set App permissions to **Read and Write**
   - Set Type of App to **Web App, Automated App or Bot**
   - Set App info (any callback URL works)
4. Under "Keys and tokens":
   - Generate **Consumer Keys** (API Key + Secret)
   - Generate **Authentication Tokens** (Access Token + Secret)
5. Add all 4 values as GitHub Secrets

**Free tier limits:** 500 posts/month (plenty for blog cross-posting).
**Token expiry:** None — OAuth 1.0a tokens don't expire.

### 4. LinkedIn (via Zapier — no GitHub Secrets needed)

LinkedIn's API requires OAuth tokens that expire every 60 days, making GitHub Actions automation
impractical without manual maintenance. Instead, use Zapier's free tier for zero-maintenance automation.

**Setup steps:**
1. Go to https://zapier.com and create a free account
2. Create a new Zap:
   - **Trigger:** RSS by Zapier → New Item in Feed
   - **Feed URL:** `https://www.beehivestrategy.com/blog/feed.xml`
   - **Action:** LinkedIn → Create Share Update
   - **Content:** Map the RSS item title + link to the LinkedIn post
3. Set polling frequency (15 min on free tier)

**Free tier limits:** 100 tasks/month (100 auto-posts), 15-min polling.
**No token expiry issues** — Zapier handles LinkedIn OAuth refresh automatically.

## Workflow Triggers

The unified workflow (`.github/workflows/cross-post.yml`) runs on:

1. **Schedule:** Daily at 09:00 HKT (01:00 UTC)
2. **Push:** When new HTML files are added to `blog/articles/` on the main branch
3. **Manual:** Via GitHub Actions tab → "Run workflow" with mode selection:
   - `git-diff`: Publish articles from recent git commits
   - `slug`: Publish a specific article by slug
   - `dry-run`: Preview what would be published without posting

## Scripts

| Script | Platform | Description |
|--------|----------|-------------|
| `scripts/devto_publish.py` | Dev.to | HTML → Markdown → Dev.to API (draft) |
| `scripts/medium_publish.py` | Medium | HTML → Markdown → Medium API (draft) |
| `scripts/x_post.py` | X.com | HTML → Tweet text → X API v2 (live) |

## Duplicate Prevention

Each script tracks published articles via local state files:
- `scripts/.medium_published.json` — Medium article URLs
- `scripts/.x_posted.json` — X.com posted URLs
- Dev.to uses API-based duplicate checking (canonical URL match)

State files are committed to the repo after each run to persist across workflow executions.

## Content Flow

1. Blog article is created/updated in `blog/articles/`
2. Article is committed and pushed to the `main` branch
3. GitHub Actions workflow triggers automatically
4. Each platform receives the content:
   - **Dev.to:** Full article as Markdown draft with canonical URL
   - **Medium:** Full article as Markdown draft with canonical URL
   - **X.com:** Tweet with article title, description hook, URL, and hashtags
   - **LinkedIn:** Post with article title and URL (via Zapier RSS)
5. Review drafts on Dev.to and Medium dashboards, then publish manually

## Manual Testing

Test each script locally before relying on GitHub Actions:

```bash
# Dev.to dry run
DEVTO_API_KEY=your_key python3 scripts/devto_publish.py --dry-run

# Medium dry run
MEDIUM_API_KEY=your_key MEDIUM_AUTHOR_ID=your_id python3 scripts/medium_publish.py --dry-run

# X.com dry run (no credentials needed)
python3 scripts/x_post.py --dry-run

# Publish specific article
DEVTO_API_KEY=your_key python3 scripts/devto_publish.py --slug why-text-to-sql-transforms-enterprise-analytics
```

## Platform Status Summary

| Platform | API Status | Free Tier | Token Expiry | Automation |
|----------|-----------|-----------|-------------|------------|
| Dev.to | Active | Unlimited | No expiry | GitHub Actions |
| Medium | Deprecated but working | Unlimited | No expiry | GitHub Actions |
| X.com | Active | 500 posts/month | No expiry | GitHub Actions |
| LinkedIn | Active | 150 posts/day | 60 days | Zapier (free) |

## Other Channels to Consider

### Hashnode (Free, API available)
- Create account at https://hashnode.com
- API docs: https://apidocs.hashnode.com
- Similar to Dev.to — publish as draft with canonical URL
- Good for developer audience overlap with Dev.to

### Substack (Free, no API)
- No API for automated publishing
- Could use email-to-post feature (each Substack has a secret email)
- Could forward RSS to email via free service

### Reddit (Free, API available)
- Post to relevant subreddits (r/artificial, r/datascience, r/businessintelligence)
- API: OAuth2 with 60-day token expiry (same issue as LinkedIn)
- Risk: subreddit-specific rules on self-promotion

### Hacker News (Free, no official API)
- Manual submission only
- Could use Y Combinator's undocumented API (risky)
- Best for occasional high-quality posts, not automation
