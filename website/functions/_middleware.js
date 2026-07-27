// Cloudflare Pages middleware: redirect bare domain to www + security headers + agent discovery + markdown negotiation

// Map URL paths to markdown files
function getMarkdownPath(pathname) {
  const mdMap = {
    '/': '/index.md',
    '/index.html': '/index.md',
    '/about': '/about.md',
    '/services': '/services.md',
    '/industries': '/industries.md',
    '/case-studies': '/case-studies.md',
  };
  return mdMap[pathname] || null;
}

// Basic HTML-to-Markdown conversion for pages without .md files
function htmlToMarkdown(html) {
  const titleMatch = html.match(/<title>([^<]+)<\/title>/i);
  const descMatch = html.match(/<meta\s+name="description"\s+content="([^"]+)"/i);

  let md = '';
  if (titleMatch || descMatch) {
    md += '---\n';
    if (titleMatch) md += `title: ${titleMatch[1]}\n`;
    if (descMatch) md += `description: ${descMatch[1]}\n`;
    md += '---\n\n';
  }
  if (titleMatch) {
    md += `# ${titleMatch[1]}\n\n`;
  }

  // Extract main content area
  const mainMatch = html.match(/<main[^>]*>([\s\S]*?)<\/main>/i);
  let content = mainMatch ? mainMatch[1] : html;

  // Strip non-content elements
  content = content
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<nav[\s\S]*?<\/nav>/gi, '')
    .replace(/<footer[\s\S]*?<\/footer>/gi, '')
    .replace(/<header[\s\S]*?<\/header>/gi, '')
    .replace(/<noscript[\s\S]*?<\/noscript>/gi, '')
    .replace(/<svg[\s\S]*?<\/svg>/gi, '')
    .replace(/<form[\s\S]*?<\/form>/gi, '');

  // Convert HTML elements to markdown
  content = content
    .replace(/<h1[^>]*>([\s\S]*?)<\/h1>/gi, '\n# $1\n\n')
    .replace(/<h2[^>]*>([\s\S]*?)<\/h2>/gi, '\n## $1\n\n')
    .replace(/<h3[^>]*>([\s\S]*?)<\/h3>/gi, '\n### $1\n\n')
    .replace(/<h4[^>]*>([\s\S]*?)<\/h4>/gi, '\n#### $1\n\n')
    .replace(/<h5[^>]*>([\s\S]*?)<\/h5>/gi, '\n##### $1\n\n')
    .replace(/<p[^>]*>([\s\S]*?)<\/p>/gi, '$1\n\n')
    .replace(/<li[^>]*>([\s\S]*?)<\/li>/gi, '- $1\n')
    .replace(/<a[^>]*href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/gi, '[$2]($1)')
    .replace(/<strong[^>]*>([\s\S]*?)<\/strong>/gi, '**$1**')
    .replace(/<b>([\s\S]*?)<\/b>/gi, '**$1**')
    .replace(/<em[^>]*>([\s\S]*?)<\/em>/gi, '*$1*')
    .replace(/<i>([\s\S]*?)<\/i>/gi, '*$1*')
    .replace(/<code[^>]*>([\s\S]*?)<\/code>/gi, '`$1`')
    .replace(/<pre[^>]*>([\s\S]*?)<\/pre>/gi, '\n```\n$1\n```\n\n')
    .replace(/<blockquote[^>]*>([\s\S]*?)<\/blockquote>/gi, '\n> $1\n\n')
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<hr\s*\/?>/gi, '\n---\n\n')
    .replace(/<[^>]+>/g, '')
    .replace(/&mdash;/g, '\u2014')
    .replace(/&ndash;/g, '\u2013')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&nbsp;/g, ' ')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/\n{3,}/g, '\n\n\n')
    .trim();

  return md + content;
}

export async function onRequest(context) {
  const url = new URL(context.request.url);

  // Redirect beehivestrategy.com (without www) to www.beehivestrategy.com
  if (url.hostname === 'beehivestrategy.com') {
    url.hostname = 'www.beehivestrategy.com';
    return Response.redirect(url.toString(), 301);
  }

  // Handle CORS preflight for .well-known paths
  if (url.pathname.startsWith('/.well-known/') && context.request.method === 'OPTIONS') {
    return new Response(null, {
      status: 204,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '86400',
      },
    });
  }

  // Markdown content negotiation (Markdown for Agents)
  // When Accept: text/markdown is requested, return a markdown version of the page
  const acceptHeader = context.request.headers.get('Accept') || '';
  if (acceptHeader.includes('text/markdown') && context.request.method === 'GET') {
    const securityHeaders = {
      'Strict-Transport-Security': 'max-age=63072000; includeSubDomains; preload',
      'X-Frame-Options': 'SAMEORIGIN',
      'X-Content-Type-Options': 'nosniff',
      'Referrer-Policy': 'strict-origin-when-cross-origin',
      'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
      'Access-Control-Allow-Origin': '*',
      'Vary': 'Accept',
    };

    // First, try to serve a pre-built .md file
    const mdPath = getMarkdownPath(url.pathname);
    if (mdPath) {
      try {
        const mdUrl = new URL(mdPath, url.origin);
        const mdResponse = await fetch(mdUrl.toString());
        if (mdResponse.ok) {
          const mdContent = await mdResponse.text();
          const tokenEstimate = Math.ceil(mdContent.length / 4);
          return new Response(mdContent, {
            status: 200,
            headers: {
              ...securityHeaders,
              'Content-Type': 'text/markdown; charset=utf-8',
              'x-markdown-tokens': tokenEstimate.toString(),
            },
          });
        }
      } catch (e) {
        // Fall through to HTML conversion
      }
    }

    // For pages without .md files, convert HTML to markdown on the fly
    const htmlResponse = await context.next();
    if (htmlResponse.ok) {
      const contentType = htmlResponse.headers.get('Content-Type') || '';
      if (contentType.includes('text/html')) {
        const html = await htmlResponse.text();
        const markdown = htmlToMarkdown(html);
        if (markdown && markdown.length > 50) {
          const tokenEstimate = Math.ceil(markdown.length / 4);
          return new Response(markdown, {
            status: 200,
            headers: {
              ...securityHeaders,
              'Content-Type': 'text/markdown; charset=utf-8',
              'x-markdown-tokens': tokenEstimate.toString(),
            },
          });
        }
      }
    }

    // If markdown conversion failed, return the HTML response with security headers
    const fallbackHeaders = new Headers(htmlResponse.headers);
    Object.entries(securityHeaders).forEach(([k, v]) => fallbackHeaders.set(k, v));
    return new Response(htmlResponse.body, {
      status: htmlResponse.status,
      statusText: htmlResponse.statusText,
      headers: fallbackHeaders,
    });
  }

  const response = await context.next();

  // Add security headers to all responses
  const newHeaders = new Headers(response.headers);
  newHeaders.set('Strict-Transport-Security', 'max-age=63072000; includeSubDomains; preload');
  newHeaders.set('X-Frame-Options', 'SAMEORIGIN');
  newHeaders.set('X-Content-Type-Options', 'nosniff');
  newHeaders.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  newHeaders.set('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');

  // Set Cache-Control for HTML pages served via clean URLs
  // (Cloudflare _headers only matches *.html paths; Functions responses need explicit headers)
  const contentType = newHeaders.get('Content-Type') || '';
  if (contentType.includes('text/html')) {
    newHeaders.set('Cache-Control', 'public, max-age=3600');
  }

  // Add CORS headers for .well-known paths
  if (url.pathname.startsWith('/.well-known/')) {
    newHeaders.set('Access-Control-Allow-Origin', '*');
    newHeaders.set('Access-Control-Allow-Methods', 'GET, OPTIONS');
    newHeaders.set('Access-Control-Allow-Headers', 'Content-Type');
  }

  // Add Link headers for homepage to advertise agent discovery endpoints
  const isHomepage = url.pathname === '/' || url.pathname === '/index.html';
  if (isHomepage) {
    const existingLink = newHeaders.get('Link') || '';
    const discoveryLinks = [
      '</.well-known/api-catalog>; rel="api-catalog"',
      '</.well-known/agent-skills/index.json>; rel="describedby"',
      '</.well-known/mcp/server-card.json>; rel="service-desc"',
      '</.well-known/oauth-protected-resource>; rel="auth-resource"',
      '</.well-known/oauth-authorization-server>; rel="auth-server"',
      '</.well-known/agent-card.json>; rel="agent-card"',
      '</llms.txt>; rel="describedby"',
      '</auth.md>; rel="service-doc"',
    ];
    const separator = existingLink ? ', ' : '';
    newHeaders.set('Link', existingLink + separator + discoveryLinks.join(', '));
  }

  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: newHeaders,
  });
}
