// Cloudflare Pages Function: readiness leads viewer for Kenneth.
// Protected by ?key=<READINESS_VIEW_KEY>. Reads READINESS_KV, newest first.
export async function onRequestGet({ request, env }) {
  const url = new URL(request.url);
  const key = env.READINESS_VIEW_KEY || 'change-me';
  if (url.searchParams.get('key') !== key) {
    return new Response('401 unauthorized', { status: 401 });
  }
  if (!env.READINESS_KV) {
    return new Response('READINESS_KV not bound', { status: 500 });
  }
  let list;
  try {
    list = await env.READINESS_KV.list();
  } catch (e) {
    return new Response('KV error: ' + e.message, { status: 500 });
  }
  const leads = [];
  for (const k of list.keys) {
    const v = await env.READINESS_KV.get(k.name);
    if (v) { try { leads.push(JSON.parse(v)); } catch {} }
  }
  leads.sort((a, b) => (b.ts || '').localeCompare(a.ts || ''));

  const rows = leads.map((l) => {
    const ax = (l.axes || []).map((x, i) =>
      esc((l.labels && l.labels[i]) || ('Axis ' + (i + 1))) + ': ' + esc(x)).join('<br>');
    return '<tr><td>' + esc(l.ts) + '</td><td>' + esc(l.email) + '</td><td>' +
      esc(l.overall) + '</td><td>' + esc(l.tier) + '</td><td>' + esc(l.weakest) +
      '</td><td>' + ax + '</td></tr>';
  }).join('') || '<tr><td colspan="6">No leads yet</td></tr>';

  const html = '<!doctype html><html lang="en"><head><meta charset="utf-8">' +
    '<meta name="robots" content="noindex"><title>AI Readiness Leads</title><style>' +
    'body{font-family:system-ui,sans-serif;background:#f5f7f8;padding:24px;color:#16202A;margin:0}' +
    'h1{color:#0B2B33;font-size:20px;font-weight:600}p{color:#5b6b63;font-size:13px}' +
    'table{border-collapse:collapse;width:100%;background:#fff;font-size:12px}' +
    'th,td{border:1px solid #dce1e4;padding:6px 8px;text-align:left;vertical-align:top}' +
    'th{background:#0B2B33;color:#fff}' +
    '</style></head><body><h1>AI Readiness Leads (' + leads.length + ')</h1>' +
    '<p>Newest first. Key-gated; do not share this URL.</p>' +
    '<table><thead><tr><th>Time</th><th>Email</th><th>Score</th><th>Band</th>' +
    '<th>Fix first</th><th>Axes</th></tr></thead><tbody>' + rows + '</tbody></table></body></html>';

  return new Response(html, { headers: { 'content-type': 'text/html; charset=utf-8' } });
}

function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"]/g, (c) =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}
