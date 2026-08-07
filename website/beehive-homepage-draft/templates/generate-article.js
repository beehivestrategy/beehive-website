#!/usr/bin/env node
/**
 * Beehive Strategy — Blog Article Generator
 *
 * Generates a static blog article HTML file from a JSON config and the
 * blog-article-template.html template. Keeps layout, styling, and interactions
 * identical across every new article.
 *
 * Usage:
 *   node generate-article.js example-article.json
 *   node generate-article.js path/to/your-article.json
 */

const fs = require('fs');
const path = require('path');

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function kebabCase(str) {
  return String(str)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function buildTocLinks(toc) {
  return toc
    .map(
      (item) =>
        `                    <a href="#${item.id}" class="toc-link">${escapeHtml(item.label)}</a>`
    )
    .join('\n');
}

function buildArticleContent(contentBlocks) {
  const lines = [];

  for (const block of contentBlocks) {
    switch (block.type) {
      case 'h2':
        lines.push(`            <h2 id="${block.id}">${block.text}</h2>`);
        break;

      case 'p':
        lines.push(`            <p>${block.text}</p>`);
        break;

      case 'ul':
        lines.push('            <ul>');
        for (const item of block.items) {
          lines.push(`                <li>${item}</li>`);
        }
        lines.push('            </ul>');
        break;

      case 'ol':
        lines.push('            <ol>');
        for (const item of block.items) {
          lines.push(`                <li>${item}</li>`);
        }
        lines.push('            </ol>');
        break;

      case 'stats':
        lines.push('            <div class="article-stat-row">');
        for (const stat of block.items) {
          lines.push('                <div class="article-stat-card">');
          lines.push(`                    <div class="article-stat-value">${escapeHtml(stat.value)}</div>`);
          lines.push(`                    <div class="article-stat-label">${escapeHtml(stat.label)}</div>`);
          lines.push('                </div>');
        }
        lines.push('            </div>');
        break;

      case 'quote':
        lines.push('            <blockquote>');
        lines.push(`                <p>${block.text}</p>`);
        if (block.cite) {
          lines.push(`                <cite>${escapeHtml(block.cite)}</cite>`);
        }
        lines.push('            </blockquote>');
        break;

      case 'html':
        // Allows raw HTML injection for advanced layouts (tables, images, etc.)
        lines.push(String(block.html));
        break;

      default:
        console.warn(`Unknown content block type: ${block.type}`);
    }
  }

  return lines.join('\n');
}

function buildFaqSection(faq) {
  if (!faq || faq.length === 0) {
    return '';
  }

  const lines = [];
  lines.push('            <section class="faq-section" id="faq" aria-label="Frequently Asked Questions">');
  lines.push('                <h2 class="faq-section-title">');
  lines.push('                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>');
  lines.push('                    Frequently Asked Questions');
  lines.push('                </h2>');
  lines.push('                <div class="faq-list">');

  faq.forEach((item, index) => {
    lines.push('                    <div class="faq-item">');
    lines.push('                        <button class="faq-question" aria-expanded="false">');
    lines.push('                            <span class="faq-question-text">');
    lines.push(`                                <span class="faq-number">${index + 1}</span>`);
    lines.push(`                                <span>${escapeHtml(item.question)}</span>`);
    lines.push('                            </span>');
    lines.push('                            <svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>');
    lines.push('                        </button>');
    lines.push('                        <div class="faq-answer" role="region">');
    lines.push('                            <div class="faq-answer-inner">');
    lines.push(`                                ${escapeHtml(item.answer)}`);
    lines.push('                            </div>');
    lines.push('                        </div>');
    lines.push('                    </div>');
  });

  lines.push('                </div>');
  lines.push('            </section>');

  return lines.join('\n');
}

function buildFaqSchema(faq) {
  if (!faq || faq.length === 0) {
    return '';
  }

  const mainEntity = faq.map((item) => ({
    '@type': 'Question',
    name: item.question,
    acceptedAnswer: {
      '@type': 'Answer',
      text: item.answer,
    },
  }));

  // Include a leading comma because this is inserted inside a JSON array
  return ',\n    ' + JSON.stringify({ '@type': 'FAQPage', mainEntity }, null, 2).split('\n').join('\n    ');
}

function buildTags(tags) {
  return tags
    .map((tag) => `                    <span class="article-tag-pill">${escapeHtml(tag)}</span>`)
    .join('\n');
}

function buildArticleTagsMeta(tags) {
  return tags
    .map((tag) => `    <meta property="article:tag" content="${escapeHtml(tag)}">`)
    .join('\n');
}

function buildSidebarRelated(items) {
  return items
    .map(
      (item) =>
        `                    <a href="${item.url}" class="sidebar-related-card">\n` +
        `                        <h4 class="sidebar-related-title">${escapeHtml(item.title)}</h4>\n` +
        `                        <span class="sidebar-related-meta">${escapeHtml(item.readTime)}</span>\n` +
        `                    </a>`
    )
    .join('\n');
}

function buildRecommendedArticles(items) {
  return items
    .map((item) => {
      return (
        `            <a href="${item.url}" class="recommended-card">\n` +
        `                <img src="${item.image}" alt="" class="recommended-card-image" loading="lazy">\n` +
        `                <div class="recommended-card-body">\n` +
        `                    <span class="recommended-card-cat">${escapeHtml(item.category)}</span>\n` +
        `                    <h3 class="recommended-card-title">${escapeHtml(item.title)}</h3>\n` +
        `                    <p class="recommended-card-excerpt">${escapeHtml(item.excerpt)}</p>\n` +
        `                    <div class="recommended-card-meta">\n` +
        `                        <span>${escapeHtml(item.readTime)}</span>\n` +
        `                        <span aria-hidden="true">&middot;</span>\n` +
        `                        <span>${escapeHtml(item.date)}</span>\n` +
        `                    </div>\n` +
        `                </div>\n` +
        `            </a>`
      );
    })
    .join('\n');
}

function buildCtaStats(stats) {
  return stats
    .map(
      (stat) =>
        `                    <div class="article-cta-stat">\n` +
        `                        <div class="article-cta-stat-value">${escapeHtml(stat.value)}</div>\n` +
        `                        <div class="article-cta-stat-label">${escapeHtml(stat.label)}</div>\n` +
        `                    </div>`
    )
    .join('\n');
}

function replacePlaceholders(template, values) {
  // Use a regex that matches {{KEY}} placeholders
  return template.replace(/\{\{([A-Z_]+)\}\}/g, (match, key) => {
    if (key in values) {
      return values[key];
    }
    console.warn(`Placeholder {{${key}}} not found in config`);
    return match;
  });
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

function main() {
  const configPath = process.argv[2];

  if (!configPath) {
    console.error('Error: Please provide a JSON config file.\n');
    console.error('Usage: node generate-article.js <config.json>');
    process.exit(1);
  }

  const resolvedConfigPath = path.resolve(configPath);
  if (!fs.existsSync(resolvedConfigPath)) {
    console.error(`Error: Config file not found: ${resolvedConfigPath}`);
    process.exit(1);
  }

  const config = JSON.parse(fs.readFileSync(resolvedConfigPath, 'utf-8'));

  const templatePath = path.join(__dirname, 'blog-article-template.html');
  if (!fs.existsSync(templatePath)) {
    console.error(`Error: Template file not found: ${templatePath}`);
    process.exit(1);
  }

  const template = fs.readFileSync(templatePath, 'utf-8');

  // Derive values from config
  const tocLinks = buildTocLinks(config.toc);
  const articleContent = buildArticleContent(config.content);
  const faqSection = buildFaqSection(config.faq);
  const faqSchema = buildFaqSchema(config.faq);
  const tags = buildTags(config.tags);
  const articleTagsMeta = buildArticleTagsMeta(config.tags);
  const sidebarRelated = buildSidebarRelated(config.sidebarRelated);
  const recommendedArticles = buildRecommendedArticles(config.recommended);
  const ctaStats = buildCtaStats(config.cta.stats);

  const values = {
    TITLE: escapeHtml(config.title),
    META_DESCRIPTION: escapeHtml(config.metaDescription),
    CANONICAL_URL: escapeHtml(config.canonicalUrl),
    OG_IMAGE: escapeHtml(config.ogImage),
    PUBLISHED_DATE_ISO: config.publishedDateIso,
    MODIFIED_DATE_ISO: config.modifiedDateIso,
    CATEGORY: escapeHtml(config.category),
    H1: config.h1,
    BREADCRUMB_TITLE: escapeHtml(config.breadcrumbTitle || config.title),
    AUTHOR_NAME: escapeHtml(config.authorName),
    AUTHOR_INITIALS: escapeHtml(config.authorInitials),
    PUBLISHED_DATE_DISPLAY: escapeHtml(config.publishedDateDisplay),
    READ_TIME: escapeHtml(config.readTime),
    KEYWORDS_CSV: config.keywords.map((k) => escapeHtml(k)).join(', '),
    TOC_LINKS: tocLinks,
    ARTICLE_CONTENT: articleContent,
    FAQ_SECTION: faqSection,
    FAQ_SCHEMA: faqSchema,
    TAGS: tags,
    ARTICLE_TAGS_META: articleTagsMeta,
    SIDEBAR_RELATED: sidebarRelated,
    RECOMMENDED_ARTICLES: recommendedArticles,
    CTA_TITLE: config.cta.title,
    CTA_DESCRIPTION: config.cta.description,
    CTA_STATS: ctaStats,
    SHARE_TITLE: escapeHtml(config.title),
  };

  const html = replacePlaceholders(template, values);

  const outputDir = path.resolve(path.dirname(resolvedConfigPath), config.outputDir || '../pages');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const outputFilename = config.slug ? `${config.slug}.html` : path.basename(configPath, '.json') + '.html';
  const outputPath = path.join(outputDir, outputFilename);

  fs.writeFileSync(outputPath, html, 'utf-8');
  console.log(`Article generated: ${outputPath}`);
}

main();
