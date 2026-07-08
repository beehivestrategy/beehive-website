# COMPLETE TRANSLATABLE STRINGS EXTRACTION REPORT (Part 1 of 4)
## Beehive Strategy Website — 3-Language Setup (EN, zh-CN, zh-TW)

**Source directory:** `/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website/`

**Files analyzed:**
- `index.html`, `about.html`, `solution.html`, `services.html`, `industries.html`
- `case-studies.html`, `pricing.html`, `contact.html`, `privacy.html`, `terms.html`, `cookies.html`
- `blog/index.html`, `blog/articles/what-is-mcp-model-context-protocol-explained.html`
- `blog/articles/manifest.json`

---

## SECTION 1: SHARED HEADER / NAV STRINGS (appear on ALL pages)

All pages share the same header/nav structure. Variations:
- The `active` class on the current page's nav-link
- Blog nav link href: `/blog` on main pages, `/` on blog pages
- Image path prefix: `assets/` on root pages, `../assets/` on blog pages

### 1.1 Logo / Brand

| # | English Text | File(s) | Classification |
|---|---|---|---|
| 1 | `Beehive Strategy Home` (aria-label) | ALL pages | Shared (header) |
| 2 | `Beehive Strategy Logo` (alt text) | ALL pages | Shared (header) |

### 1.2 Desktop Navigation Links (also duplicated in mobile menu)

| # | English Text | File(s) | Classification |
|---|---|---|---|
| 3 | `Solution` | ALL pages | Shared (header) |
| 4 | `Services` | ALL pages | Shared (header) |
| 5 | `Industries` | ALL pages | Shared (header) |
| 6 | `Case Studies` | ALL pages | Shared (header) |
| 7 | `Pricing` | ALL pages | Shared (header) |
| 8 | `About` | ALL pages | Shared (header) |
| 9 | `Blog` | ALL pages | Shared (header) |
| 10 | `Book a Demo` (nav CTA button) | ALL pages | Shared (header) |

### 1.3 Language Switcher

| # | English Text | File(s) | Classification |
|---|---|---|---|
| 11 | `Switch language` (aria-label) | ALL pages | Shared (header) |
| 12 | `EN` (current-lang-label) | ALL pages | Shared (header) |
| 13 | `English` | ALL pages | Shared (header) |
| 14 | `简体中文` | ALL pages | Shared (header) — already in Chinese |
| 15 | `繁體中文` | ALL pages | Shared (header) — already in Chinese |
| 16 | `EN` (lang-code for English) | ALL pages | Shared (header) |
| 17 | `简` (lang-code for zh-CN) | ALL pages | Shared (header) |
| 18 | `繁` (lang-code for zh-TW) | ALL pages | Shared (header) |

### 1.4 Mobile Menu / Navigation Aria

| # | English Text | File(s) | Classification |
|---|---|---|---|
| 19 | `Toggle menu` (aria-label) | ALL pages | Shared (header) |
| 20 | `Main navigation` (aria-label) | ALL pages | Shared (header) |

### 1.5 Back to Top

| # | English Text | File(s) | Classification |
|---|---|---|---|
| 21 | `Back to top` (aria-label) | ALL pages | Shared (footer) |

---

## SECTION 2: SHARED FOOTER STRINGS (ALL pages, with variations)

### Footer Variations:
- **index.html**: LinkedIn + Email only (no GitHub)
- **about, solution, services, industries, case-studies, pricing, contact**: LinkedIn + GitHub + Email
- **privacy, terms, cookies**: Email only (no LinkedIn, no GitHub)
- **blog/index.html**: LinkedIn + GitHub + Email

### 2.1 Brand Description

| # | English Text | File(s) | Classification |
|---|---|---|---|
| 22 | `Enterprise AI & data analytics consulting. We deliver MCP-powered conversational intelligence that transforms how businesses interact with their data.` | ALL pages | Shared (footer) |

### 2.2 Social Links (aria-labels)

| # | English Text | File(s) | Classification |
|---|---|---|---|
| 23 | `LinkedIn` (aria-label) | index, about, solution, services, industries, case-studies, pricing, contact, blog/index | Shared (footer) |
| 24 | `GitHub` (aria-label) | about, solution, services, industries, case-studies, pricing, contact, blog/index | Shared (footer) |
| 25 | `Email` (aria-label) | ALL pages | Shared (footer) |

### 2.3 Footer Column Headings

| # | English Text | File(s) | Classification |
|---|---|---|---|
| 26 | `Product` | ALL pages | Shared (footer) |
| 27 | `Industries` | ALL pages | Shared (footer) |
| 28 | `Company` | ALL pages | Shared (footer) |

### 2.4 Footer Product Links

| # | English Text | File(s) | Classification |
|---|---|---|---|
| 29 | `Platform` | ALL pages | Shared (footer) |
| 30 | `Services` (footer link) | ALL pages | Shared (footer) |
| 31 | `AI Agents` | ALL pages | Shared (footer) |
| 32 | `Case Studies` (footer link) | ALL pages | Shared (footer) |
| 33 | `Pricing` (footer link) | ALL pages | Shared (footer) |
| 34 | `Blog` (footer link) | ALL pages | Shared (footer) |

### 2.5 Footer Industries Links

| # | English Text | File(s) | Classification |
|---|---|---|---|
| 35 | `Retail & E-Commerce` | ALL pages | Shared (footer) |
| 36 | `Financial Services` | ALL pages | Shared (footer) |
| 37 | `Manufacturing` | ALL pages | Shared (footer) |
| 38 | `Professional Services` | ALL pages | Shared (footer) |
| 39 | `Real Estate` | ALL pages | Shared (footer) |

### 2.6 Footer Company Links

| # | English Text | File(s) | Classification |
|---|---|---|---|
| 40 | `About Us` | ALL pages | Shared (footer) |
| 41 | `Contact` | ALL pages | Shared (footer) |
| 42 | `FAQ` | ALL pages | Shared (footer) |
| 43 | `Careers` | ALL pages | Shared (footer) |

### 2.7 Copyright & Legal Links

| # | English Text | File(s) | Classification |
|---|---|---|---|
| 44 | `© 2026 Beehive Strategy Co., Ltd. All rights reserved.` | ALL pages | Shared (footer) |
| 45 | `Privacy Policy` | ALL pages | Shared (footer) |
| 46 | `Terms of Service` | ALL pages | Shared (footer) |
| 47 | `Cookie Policy` | ALL pages | Shared (footer) |

### 2.8 Shared Meta Values (appear in head of ALL or most pages)

| # | English Text | File(s) | Classification |
|---|---|---|---|
| 48 | `Beehive Strategy` (og:site_name) | ALL pages | Shared (meta) |
| 49 | `Beehive Strategy Co., Ltd.` (meta author) | ALL pages | Shared (meta) |
| 50 | `Beehive Strategy — MCP-Powered Conversational BI` (og:image:alt) | ALL pages | Shared (meta) |
| 51 | `Shenzhen, Guangdong, China` (geo.placename) | ALL pages | Shared (meta) |

---

## SECTION 3: SHARED BLOG ARTICLE TEMPLATE STRINGS

From `blog/articles/what-is-mcp-model-context-protocol-explained.html` (template pattern for all articles).

### 3.1 Breadcrumb

| # | English Text | File(s) | Classification |
|---|---|---|---|
| 52 | `Home` (breadcrumb link) | blog/articles/*.html, blog/index.html, about, solution, services, industries, case-studies, pricing, contact | Shared (breadcrumb) |
| 53 | `Blog` (breadcrumb link) | blog/articles/*.html, blog/index.html | Shared (blog template) |

### 3.2 Article Header

| # | English Text | File(s) | Classification |
|---|---|---|---|
| 54 | `By Beehive Strategy` (article author) | blog/articles/*.html | Shared (blog template) |
| 55 | `Beehive Strategy` (blog card author) | blog/index.html (all 51 cards) | Shared (blog template) |
| 56 | `min read` (reading time suffix, e.g. "8 min read") | blog/articles/*.html, blog/index.html | Shared (blog template) |

### 3.3 Article Footer / Tags

| # | English Text | File(s) | Classification |
|---|---|---|---|
| 57 | `Tags` (tags section heading) | blog/articles/*.html | Shared (blog template) |

### 3.4 Share Section

| # | English Text | File(s) | Classification |
|---|---|---|---|
| 58 | `Share this article` (share heading) | blog/articles/*.html | Shared (blog template) |
| 59 | `Share on LinkedIn` | blog/articles/*.html | Shared (blog template) |
| 60 | `Share on X` | blog/articles/*.html | Shared (blog template) |

### 3.5 Article Navigation

| # | English Text | File(s) | Classification |
|---|---|---|---|
| 61 | `← Back to All Articles` | blog/articles/*.html | Shared (blog template) |

### 3.6 Blog Article CTA Section

| # | English Text | File(s) | Classification |
|---|---|---|---|
| 62 | `See MCP in Action` (CTA heading — specific to MCP article, pattern shared) | blog/articles/*.html | Shared (blog template pattern) |
| 63 | `Book a Free Demo` (CTA button) | blog/articles/*.html, blog/index.html | Shared (blog template) |
| 64 | `Explore the Platform` (CTA secondary button) | blog/articles/*.html, solution | Shared (blog template) |

### 3.7 Blog Card Shared Strings

| # | English Text | File(s) | Classification |
|---|---|---|---|
| 65 | `Read more →` | blog/index.html (all 51 cards) | Shared (blog template) |

---

## SECTION 4: INDEX PAGE-SPECIFIC STRINGS

**File:** `index.html`

### 4.1 Meta Tags

| # | English Text | Classification |
|---|---|---|
| 66 | `Beehive Strategy \| MCP-Powered Enterprise Conversational BI Platform` (title) | Page-specific (meta) |
| 67 | `Beehive Strategy builds MCP-powered conversational BI platforms for enterprises. Ask your data questions in natural language via WeChat Work, DingTalk, and Feishu. Deploy in 2 weeks.` (description) | Page-specific (meta) |
| 68 | `Beehive Strategy \| MCP-Powered Conversational BI Platform` (og:title) | Page-specific (meta) |
| 69 | `MCP-powered conversational BI for enterprises. Ask your data in natural language via WeChat Work, DingTalk, and Feishu. Deploy in 2 weeks.` (og:description) | Page-specific (meta) |
| 70 | `Beehive Strategy \| MCP-Powered Conversational BI` (twitter:title) | Page-specific (meta) |
| 71 | `Enterprise conversational BI platform powered by MCP. Ask data questions in natural language, deploy in 2 weeks.` (twitter:description) | Page-specific (meta) |

### 4.2 Hero Section

| # | English Text | Classification |
|---|---|---|
| 72 | `MCP-Powered Enterprise Intelligence` (hero badge) | Page-specific |
| 73 | `Ask Your Data Anything` (hero h1 part 1) | Page-specific |
| 74 | `Get Answers Everywhere` (hero h1 part 2, gradient) | Page-specific |
| 75 | `Deploy a conversational BI platform in 2 weeks. Connect 50+ data sources, deliver answers through WeChat Work, DingTalk, and Feishu — with enterprise-grade security built in.` (hero subtitle) | Page-specific |
| 76 | `Book a Demo` (hero primary button) | Page-specific |
| 77 | `See How It Works` (hero secondary button) | Page-specific |

### 4.3 Hero Stats

| # | English Text | Classification |
|---|---|---|
| 78 | `2 weeks` (stat value) | Page-specific |
| 79 | `Average deployment time` (stat label) | Page-specific |
| 80 | `50+` (stat value) | Page-specific |
| 81 | `Data source connectors` (stat label) | Page-specific |
| 82 | `3x` (stat value) | Page-specific |
| 83 | `Faster insights` (stat label) | Page-specific |
| 84 | `0%` (stat value) | Page-specific |
| 85 | `Data leaves your infrastructure` (stat label) | Page-specific |

### 4.4 Social Proof Section

| # | English Text | Classification |
|---|---|---|
| 86 | `Trusted by Enterprise Teams Across Asia` | Page-specific |
| 87 | `12+` (stat value) | Page-specific |
| 88 | `Enterprise clients` (stat label) | Page-specific |
| 89 | `50+` (stat value) | Page-specific |
| 90 | `Data source connectors` (stat label, repeated) | Page-specific |
| 91 | `5` (stat value) | Page-specific |
| 92 | `Industries served` (stat label) | Page-specific |
| 93 | `99.9%` (stat value) | Page-specific |
| 94 | `Platform uptime` (stat label) | Page-specific |

### 4.5 Mission Section

| # | English Text | Classification |
|---|---|---|
| 95 | `Our Mission` (section label) | Page-specific |
| 96 | `We believe data should work for people — not the other way around.` (mission heading) | Page-specific |
| 97 | `Most enterprise data sits in dashboards no one opens, reports no one reads, and tools no one has time to learn. Beehive Strategy changes that. We turn your data into a conversation — ask in plain English, get instant answers, and make decisions where you already work: in WeChat Work, DingTalk, and Feishu.` (mission para 1) | Page-specific |
| 98 | `No dashboards. No SQL. No waiting. Just answers.` (mission para 2) | Page-specific |

### 4.6 How It Works Section

| # | English Text | Classification |
|---|---|---|
| 99 | `How It Works` (section label) | Page-specific |
| 100 | `From Data to Decision in One Conversation` (section heading) | Page-specific |
| 101 | `Three steps. Two weeks. Zero dashboards.` (section subheading) | Page-specific |
| 102 | `Ask` (flow node 1 title) | Page-specific |
| 103 | `Type your question in natural language — no SQL, no formulas, no training required.` | Page-specific |
| 104 | `Connect` (flow node 2 title) | Page-specific |
| 105 | `The MCP semantic layer connects to 50+ data sources and translates your question into governed, secure queries.` | Page-specific |
| 106 | `Answer` (flow node 3 title) | Page-specific |
| 107 | `Get charts, tables, and insights delivered directly in WeChat Work, DingTalk, or Feishu — in seconds.` | Page-specific |

### 4.7 Case Study Showcase Section

| # | English Text | Classification |
|---|---|---|
| 108 | `Proven Results` (section label) | Page-specific |
| 109 | `Real Outcomes from Real Deployments` (section heading) | Page-specific |
| 110 | `Retail & E-Commerce` (case study label) | Page-specific |
| 111 | `3x` (metric value) | Page-specific |
| 112 | `Faster decision-making` (metric label) | Page-specific |
| 113 | `40%` (metric value) | Page-specific |
| 114 | `Reduction in reporting backlog` (metric label) | Page-specific |
| 115 | `Read the case study →` (link) | Page-specific |

### 4.8 Testimonial Section

| # | English Text | Classification |
|---|---|---|
| 116 | `What Our Clients Say` (section label) | Page-specific |
| 117 | `"We replaced three reporting tools and an entire analyst team's worth of manual work with one conversational interface. Our executives get answers in seconds, not days."` (quote) | Page-specific |
| 118 | `VP of Data Strategy, Leading Retail Group` (attribution) | Page-specific |

### 4.9 Comparison Table Section

| # | English Text | Classification |
|---|---|---|
| 119 | `Why Beehive` (section label) | Page-specific |
| 120 | `Built Different, Built Better` (section heading) | Page-specific |
| 121 | `Feature` (table column header) | Page-specific |
| 122 | `Traditional BI` (table column header) | Page-specific |
| 123 | `Beehive Strategy` (table column header) | Page-specific |
| 124 | `Deployment time` (row label) | Page-specific |
| 125 | `6–12 months` (table cell) | Page-specific |
| 126 | `2 weeks` (table cell) | Page-specific |
| 127 | `Interface` (row label) | Page-specific |
| 128 | `Dashboards & reports` (table cell) | Page-specific |
| 129 | `Conversational (natural language)` (table cell) | Page-specific |
| 130 | `Delivery channel` (row label) | Page-specific |
| 131 | `Separate BI tool` (table cell) | Page-specific |
| 132 | `WeChat Work, DingTalk, Feishu` (table cell) | Page-specific |
| 133 | `Data governance` (row label) | Page-specific |
| 134 | `Manual, siloed` (table cell) | Page-specific |
| 135 | `Built-in RBAC & audit trails` (table cell) | Page-specific |
| 136 | `Time to insight` (row label) | Page-specific |
| 137 | `Hours to days` (table cell) | Page-specific |
| 138 | `Seconds` (table cell) | Page-specific |
| 139 | `Training required` (row label) | Page-specific |
| 140 | `Extensive (SQL, tool-specific)` (table cell) | Page-specific |
| 141 | `None (natural language)` (table cell) | Page-specific |

### 4.10 Industries Teaser Section

| # | English Text | Classification |
|---|---|---|
| 142 | `Industries` (section label) | Page-specific |
| 143 | `Solutions for Every Sector` (section heading) | Page-specific |
| 144 | `Retail & E-Commerce` (card heading) | Page-specific |
| 145 | `Real-time inventory, sales intelligence, and customer journey analytics.` | Page-specific |
| 146 | `Financial Services` (card heading) | Page-specific |
| 147 | `Risk monitoring, compliance reporting, and portfolio analytics.` | Page-specific |
| 148 | `Manufacturing` (card heading) | Page-specific |
| 149 | `Predictive maintenance, quality control, and supply chain optimisation.` | Page-specific |
| 150 | `Professional Services` (card heading) | Page-specific |
| 151 | `Utilisation tracking, profitability analysis, and project intelligence.` | Page-specific |
| 152 | `Real Estate` (card heading) | Page-specific |
| 153 | `Portfolio performance, market analytics, and tenant insights.` | Page-specific |
| 154 | `View All Industries →` (link) | Page-specific |

### 4.11 Blog Teaser Section

| # | English Text | Classification |
|---|---|---|
| 155 | `Latest Insights` (section label) | Page-specific |
| 156 | `From the Blog` (section heading) | Page-specific |
| 157 | `What Is MCP? The Model Context Protocol Explained for Enterprise Leaders` (teaser title) | Page-specific |
| 158 | `Why 73% of Enterprise AI Projects Fail — And How MCP Fixes It` (teaser title) | Page-specific |
| 159 | `Building a Semantic Layer: The Secret to Self-Service Analytics` (teaser title) | Page-specific |
| 160 | `Read more →` (teaser link) | Page-specific |
| 161 | `View All Articles →` (link) | Page-specific |

### 4.12 CTA Section

| # | English Text | Classification |
|---|---|---|
| 162 | `Ready to See Your Data in Chat?` (CTA heading) | Page-specific |
| 163 | `Book a free demo and watch your data answer questions in real-time. Deploy in 2 weeks, not 2 quarters.` (CTA para) | Page-specific |
| 164 | `Book a Free Demo` (CTA primary button) | Page-specific |
| 165 | `See How It Works` (CTA secondary button) | Page-specific |

### 4.13 JSON-LD Structured Data (index.html)

| # | English Text | Classification |
|---|---|---|
| 166 | `Beehive Strategy Co., Ltd.` (Organization name) | Shared (structured data) |
| 167 | `蜂启咨询有限公司` (Organization alternateName) | Shared (structured data) — already Chinese |
| 168 | `Beehive Strategy \| MCP-Powered Enterprise Conversational BI Platform` (WebPage name) | Page-specific (structured data) |
| 169 | `Beehive Strategy builds MCP-powered conversational BI platforms for enterprises. Ask your data questions in natural language via WeChat Work, DingTalk, and Feishu. Deploy in 2 weeks.` (WebPage description) | Page-specific (structured data) |
| 170 | `MCP-Powered Conversational BI Platform` (SoftwareApplication name) | Page-specific (structured data) |
| 171 | `Enterprise conversational BI platform with 50+ data connectors, natural language query, and IM-native delivery.` (description) | Page-specific (structured data) |
| 172 | `Conversational BI` (applicationCategory) | Page-specific (structured data) |
| 173 | `Business Intelligence` (applicationSubCategory) | Page-specific (structured data) |
| 174 | `WeChat Work` (featureList) | Page-specific (structured data) |
| 175 | `DingTalk` (featureList) | Page-specific (structured data) |
| 176 | `Feishu` (featureList) | Page-specific (structured data) |
| 177 | `50+ Data Connectors` (featureList) | Page-specific (structured data) |
| 178 | `Natural Language Query` (featureList) | Page-specific (structured data) |
| 179 | `RBAC & Audit Trails` (featureList) | Page-specific (structured data) |
| 180 | `Real-time Analytics` (featureList) | Page-specific (structured data) |
| 181 | `Deploy in 2 Weeks` (featureList) | Page-specific (structured data) |
| 182 | `Enterprise-Grade Security` (featureList) | Page-specific (structured data) |
| 183 | `Shenzhen, Guangdong, China` (place) | Shared (structured data) |
| 184 | `5.0` (aggregateRating ratingValue) | Page-specific (structured data) |
| 185 | `12` (aggregateRating reviewCount) | Page-specific (structured data) |
