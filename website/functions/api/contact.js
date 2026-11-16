// Cloudflare Pages Function — legacy /api/contact route.
//
// Contact delivery was moved client-side (2026-11-16): the three contact pages
// POST directly to the activated FormSubmit AJAX endpoint. That keeps delivery
// on the visitor's own IP. Cloudflare Worker egress IPs are shared and were
// consistently rate-limited by FormSubmit (HTTP 429), so proxying from here is
// intentionally disabled.
//
// This route is retained only so an old caller / bookmark gets a clear answer
// instead of a misleading 404 or a failing 500. It is not used by the site.

function json(o, status = 200, extra = {}) {
  return new Response(JSON.stringify(o), {
    status,
    headers: Object.assign(
      { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
      extra
    ),
  });
}

export async function onRequestPost() {
  return json(
    {
      ok: false,
      error: 'deprecated',
      message: 'Contact delivery is handled by the form on /contact. Please use that form.',
    },
    410
  );
}

// Anything other than POST gets a clean 405 instead of a Pages 404.
export async function onRequest() {
  return json({ ok: false, error: 'method not allowed' }, 405, { Allow: 'POST' });
}
