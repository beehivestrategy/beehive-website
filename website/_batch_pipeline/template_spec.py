"""
Blog article DESIGN TEMPLATE spec — the canonical structure every rewritten
article must follow so the batch pipeline preserves the site's design system.

Source of truth: the 5 GSC pillar articles (what-is-data-fabric.html etc.)
which were hand-built to the agreed standard.

EN target: 2,500-3,500 words (floor 2,500), article-content body only.
zh-CN / zh-TW target: 3,500-5,000 CJK chars (floor 3,500).

The wrapper (header nav, sidebar, footer, JSON-LD @graph, hreflang, og:*,
lang switcher) is NEVER touched by the rewrite. Only the inner HTML of
<div class="article-content"> ... </article> is regenerated.
"""

# ---------------------------------------------------------------------------
# Required H2 STRUCTURE (order matters). Every rewritten article must contain
# these sections (drop "Related Articles" if the manifest has no related set,
# but keep FAQ + CTA). The deeper-dive sections (comparison / architecture /
# mid-market / AI-grounding / roadmap) are REQUIRED for EN to reach the word
# floor; for shorter topics combine into fewer but still substantive sections.
# ---------------------------------------------------------------------------
EN_REQUIRED_SECTIONS = [
    ("What is {topic}? — A Concise Definition", "definition + why it matters now"),
    ("How Does {topic} Work?", "mechanics / architecture overview"),
    ("Key Components of {topic}", "enumerate 4-6 building blocks"),
    ("Why {topic} Matters for Enterprises", "business value, risk, ROI framing"),
    ("Common Use Cases", "3-5 industry use cases incl. retail/ecom, finance, manufacturing, supply chain, real estate, professional services"),
    ("How {topic} Fits into Beehive Strategy's Approach", "tie to MCP conversational BI, 2-week deploy, IM channels"),
    ("Getting Started with {topic}", "first 3 steps a leader can take"),
    ("{topic} vs Alternatives (Data Mesh / Lake / Traditional ETL / etc.)", "comparison table or prose"),
    ("Core Architecture Components", "deeper technical breakdown"),
    ("{topic} for Mid-Market and Resource-Constrained Teams", "practical, lower-cost path"),
    ("How {topic} Grounds AI and Large Language Models", "AI/LLM relevance"),
    ("A Phased 90-Day Implementation Roadmap", "30/60/90 day plan"),
    ("Frequently Asked Questions", "4-6 Q&A, also emitted as FAQPage JSON-LD"),
]

# Body must end with the CTA block (do not remove):
#   <div class="cta-content reveal"> ... Book a demo ... </div>
# and the FAQ block:
#   <div class="faq-section"> ... <div class="faq-item"> ... </div> ... </div>

DESIGN_RULES = {
    "wrapper_untouched": True,
    "only_article_content_rewritten": True,
    "cta_block_required": True,
    "faq_required": True,
    "faq_jsonld_required": True,   # inject <script type="application/ld+json"> FAQPage
    "balanced_divs": True,
    "h2_min_count": 8,
    "en_word_floor": 2500,
    "en_word_target": 3500,
    "cjk_floor": 3500,
    "cjk_target": 5000,
    "no_placeholder_text": True,   # no "Lorem", "TODO", "TBD", "coming soon"
    "internal_links": "keep existing related-article links where present",
    "tone": "authoritative, practitioner, enterprise-B2B, concrete examples",
    "brand": "Beehive Strategy — MCP-driven conversational BI, 2-week enterprise deploy, IM channels (WeCom/DingTalk/Feishu/WhatsApp/Telegram/Teams/WeChat)",
    "cta_text": "Book a demo",
}

def slug_to_topic(slug):
    """Best-effort human title from slug for template section titles."""
    s = slug.replace("-", " ")
    return s[:1].upper() + s[1:]
