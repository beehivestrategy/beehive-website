# Trae Prompt: Build Beehive Strategy Website Version 2

Use the exported package `beehive-strategy-v1-export.zip` as the design reference and source material. Build a production-ready version 2 of the Beehive Strategy website.

## Brand Context

Beehive Strategy is an enterprise AI company that delivers conversational BI and AI agent solutions. Business users ask questions in natural language (e.g., in WeChat Work / Slack) and get instant data insights without SQL or dashboards.

Key value propositions:
- Connects to 50+ data sources
- Natural language interface, zero code required
- Deploys in ~2 weeks
- Delivers 3x average ROI within the first year

## Deliverables from the Export Package

The zip contains the complete v1 design project:

```
beehive-homepage-draft/
├── beehive-homepage-draft.design   # Trae Design canvas source
├── colors_and_type-draft.css       # Brand tokens, colors, typography
├── pages/                          # 11 static HTML pages
│   ├── index.html                  # Homepage
│   ├── solution.html               # Solution overview
│   ├── services.html               # Services
│   ├── industries.html             # Industries
│   ├── case-studies.html           # Case studies
│   ├── pricing.html                # Pricing
│   ├── about.html                  # About us
│   ├── contact.html                # Contact / demo booking
│   ├── blog-index.html             # Blog listing
│   ├── blog-article.html           # Blog article template
│   └── conversational-analytics-energy-sector.html
└── assets/                         # Images, logos, hero backgrounds
```

## Version 2 Goals

1. **Preserve the visual design**: dark theme, teal primary (#2B9E8B), gold accent (#d4a843), Geist/Outfit typography, hero overlays, subtle particle canvas animations.
2. **Convert to a maintainable codebase**: use Next.js (App Router) + React + TypeScript + Tailwind CSS.
3. **Create reusable components**: Header, Footer, Hero, FeatureCard, CaseStudyCard, PricingCard, BlogCard, CtaSection, ParticleCanvas.
4. **Keep all 11 pages** with the same URLs/routes and content.
5. **Make it responsive** for desktop, tablet, and mobile.
6. **Move design tokens** from `colors_and_type-draft.css` into Tailwind config / CSS variables.
7. **Refactor hero sections** into a shared `Hero` component that accepts:
   - background image
   - title, subtitle, badge
   - alignment (left / center)
   - optional right-side visual (e.g., chat mockup on homepage)
   - overlay + particle canvas enabled by default
8. **Static export**: the final build should be exportable as static HTML (`next export` or equivalent).
9. **Optimize images**: keep the same assets, but place them in `/public/assets/` and use Next.js `<Image>` where appropriate.
10. **Clean up hardcoded colors**: replace any hardcoded hex/rgba values with Tailwind classes or CSS variables from the token file.
11. **Preserve interactions**: mobile menu, smooth scroll, particle canvas animation.
12. **Accessibility**: semantic HTML, aria labels, keyboard-navigable buttons/links.

## Suggested Project Structure

```
beehive-strategy-v2/
├── app/
│   ├── layout.tsx
│   ├── page.tsx                    # /
│   ├── solution/page.tsx           # /solution
│   ├── services/page.tsx           # /services
│   ├── industries/page.tsx         # /industries
│   ├── case-studies/page.tsx       # /case-studies
│   ├── pricing/page.tsx            # /pricing
│   ├── about/page.tsx              # /about
│   ├── contact/page.tsx            # /contact
│   ├── blog/page.tsx               # /blog
│   └── blog/
│       └── conversational-analytics-energy-sector/page.tsx
├── components/
│   ├── Header.tsx
│   ├── Footer.tsx
│   ├── Hero.tsx
│   ├── ParticleCanvas.tsx
│   ├── FeatureCard.tsx
│   ├── PricingCard.tsx
│   ├── CaseStudyCard.tsx
│   ├── BlogCard.tsx
│   └── CtaSection.tsx
├── styles/
│   └── globals.css
├── public/
│   └── assets/                     # copy all v1 images here
├── tailwind.config.ts
├── next.config.js
└── package.json
```

## Design Tokens (from `colors_and_type-draft.css`)

```css
--color-primary: #2B9E8B;
--color-primary-light: #3dd4b0;
--color-primary-dark: #1e7a6b;
--color-accent: #d4a843;
--color-accent-light: #f0d78c;
--color-accent-dark: #b8922f;
--color-bg: #0a0e0d;
--color-bg-alt: #111816;
--color-text: #f0f0f0;
--color-text-secondary: #8a9e96;
--color-border: rgba(255, 255, 255, 0.08);
```

Map these to Tailwind theme colors and CSS variables.

## Important Implementation Notes

- The v1 HTML uses Tailwind CDN v4 and inline `<style>` blocks. Convert the inline page styles into component-scoped Tailwind classes or a global stylesheet.
- The hero overlay CSS is:
  ```css
  background:
    radial-gradient(ellipse 90% 80% at 50% 50%, rgba(10,14,13,0.32) 0%, rgba(10,14,13,0.70) 55%, rgba(10,14,13,0.88) 100%),
    linear-gradient(90deg, rgba(10,14,13,0.92) 0%, rgba(10,14,13,0.72) 30%, rgba(10,14,13,0.35) 60%, transparent 100%);
  ```
- The particle canvas should be a client component (`"use client"`) and rendered inside each hero.
- Keep the chat mockup on the homepage exactly as designed.
- Maintain the `data-dom-id` attributes for any elements that had them in v1 (e.g., nav CTA buttons).

## Success Criteria

- All 11 routes render correctly with the same content and visual hierarchy as v1.
- No visual regressions: dark theme, hero images, overlays, particles, text shadows, glow effects.
- Build passes (`next build`) and static export completes without errors.
- Code is typed with TypeScript and follows component-based architecture.
- All links between pages work.
- Mobile menu opens/closes and all pages are responsive.
