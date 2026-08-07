---
name: seo-geo-audit
description: Audits a website for SEO and Generative Engine Optimization (GEO) readiness across Google AI Overviews, ChatGPT citations, Perplexity sources, and Gemini. Generates actionable reports with priority-ranked fixes.
---

# SEO/GEO Audit Skill

## Instructions

When the user provides a website URL, perform a comprehensive SEO and GEO audit:

1. **Technical SEO Check**: Verify robots.txt, sitemap.xml, canonical tags, schema markup, page speed, mobile-friendliness
2. **GEO Readiness**: Check for llms.txt, AI bot permissions, structured data (FAQPage, BlogPosting, HowTo), quote-worthy content, and .md page versions
3. **Content Analysis**: Audit title lengths, meta descriptions with CTAs, internal linking, keyword cannibalisation, content freshness
4. **Authority Signals**: Check backlinks, brand mentions, Google Business Profile, community engagement metrics
5. **AI Citation Potential**: Evaluate content format (listicles, definitions, how-to guides, statistics), factual claims, and source-worthy formatting

## Output Format

Generate a structured report with:
- Overall SEO score (0-100)
- GEO readiness score (0-100)
- Priority-ranked action items (P0/P1/P2)
- Estimated impact for each fix
- Timeline to first AI search citations

## Key Metrics

- Title truncation rate (titles >65 chars)
- Meta description CTA coverage
- Schema markup completeness
- FAQ content coverage
- Internal link density
- AI crawler permission status
