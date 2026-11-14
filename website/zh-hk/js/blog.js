/**
 * 蜂啟諮詢 Blog — Article listing & pagination
 * Loads articles from manifest.json and renders them dynamically
 */

(function() {
  'use strict';

  const ARTICLES_PER_PAGE = 9;
  let currentPage = 1;
  let allArticles = [];

  async function loadManifest() {
    try {
      const response = await fetch('articles/manifest.json');
      if (!response.ok) throw new Error('Manifest not found');
      return await response.json();
    } catch (e) {
      console.warn('Blog manifest not yet available:', e.message);
      return [];
    }
  }

  function formatDate(dateStr) {
    const d = new Date(dateStr);
    return d.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }

  function readingTimeLabel(minutes) {
    if (minutes < 1) return '< 1 min read';
    return minutes + ' min read';
  }

  function renderArticleCard(article) {
    const dateFormatted = formatDate(article.date);
    const readTime = readingTimeLabel(article.readingTime || 5);
    const excerpt = article.excerpt || article.description || '';

    return `
      <article class="blog-card reveal" itemscope itemtype="https://schema.org/BlogPosting">
        <a href="articles/${article.slug}.html" class="blog-card-link" itemprop="url">
          <div class="blog-card-image" aria-hidden="true">
            <span class="blog-card-category">${article.category || 'Insights'}</span>
          </div>
          <div class="blog-card-body">
            <meta itemprop="datePublished" content="${article.date}">
            <meta itemprop="wordCount" content="${article.wordCount || 800}">
            <div class="blog-card-meta">
              <time datetime="${article.date}" itemprop="datePublished">${dateFormatted}</time>
              <span class="blog-card-dot" aria-hidden="true">&middot;</span>
              <span>${readTime}</span>
            </div>
            <h2 class="blog-card-title" itemprop="headline">${article.title}</h2>
            <p class="blog-card-excerpt" itemprop="description">${excerpt}</p>
            <div class="blog-card-footer">
              <span class="blog-card-author" itemprop="author">蜂啟諮詢</span>
              <span class="blog-card-readmore">Read more &rarr;</span>
            </div>
          </div>
        </a>
      </article>
    `;
  }

  function renderPagination(totalPages, current) {
    if (totalPages <= 1) return '';
    let html = '<nav aria-label="Blog pagination"><ul class="pagination-list">';
    for (let i = 1; i <= totalPages; i++) {
      if (i === current) {
        html += `<li><span class="pagination-page active" aria-current="page">${i}</span></li>`;
      } else {
        html += `<li><a href="#page-${i}" class="pagination-page" data-page="${i}">${i}</a></li>`;
      }
    }
    html += '</ul></nav>';
    return html;
  }

  function renderEmptyState() {
    return `
      <div style="text-align: center; padding: var(--space-16) 0;">
        <h2 style="color: var(--color-text); margin-bottom: var(--space-4);">No Articles Yet</h2>
        <p style="color: var(--color-text-muted);">Our blog is being set up. Check back soon for fresh insights on MCP, AI analytics, and enterprise intelligence.</p>
        <a href="../index.html#contact" class="btn btn-primary" style="margin-top: var(--space-6);">Talk to Us Instead</a>
      </div>
    `;
  }

  async function init() {
    const container = document.getElementById('blog-list-container');
    if (!container) return;

    const manifest = await loadManifest();
    allArticles = manifest.articles || [];

    if (allArticles.length === 0) {
      container.innerHTML = renderEmptyState();
      return;
    }

    // Sort by date descending
    allArticles.sort((a, b) => new Date(b.date) - new Date(a.date));

    const totalPages = Math.ceil(allArticles.length / ARTICLES_PER_PAGE);
    const start = (currentPage - 1) * ARTICLES_PER_PAGE;
    const pageArticles = allArticles.slice(start, start + ARTICLES_PER_PAGE);

    container.innerHTML = pageArticles.map(renderArticleCard).join('');

    const paginationEl = document.getElementById('blog-pagination');
    if (paginationEl) {
      paginationEl.innerHTML = renderPagination(totalPages, currentPage);
      paginationEl.querySelectorAll('.pagination-page[data-page]').forEach(link => {
        link.addEventListener('click', function(e) {
          e.preventDefault();
          currentPage = parseInt(this.dataset.page, 10);
          init();
          window.scrollTo({ top: document.getElementById('blog-list').offsetTop - 80, behavior: 'smooth' });
        });
      });
    }

    // Trigger reveal animations
    if (window.RevealManager) {
      window.RevealManager.refresh();
    }
  }

  document.addEventListener('DOMContentLoaded', init);
})();
