// Cloudflare Pages Function — website contact form, real online delivery.
// Route: POST /api/contact
//
// Delivery backend: FormSubmit free AJAX endpoint. No vendor account, no API
// key, no Pages secret required. The destination alias below was activated for
// account@beehivestrategy.com on 2026-11-16; the alias hides the real mailbox
// from page source and from bots.
//
// Optional bindings:
//   CONTACT_FORM_ALIAS   override the FormSubmit alias
//   CONTACT_SITE_ORIGIN  override the Referer origin sent to FormSubmit
//
// Note: visitor auto-receipts are intentionally not sent. The on-page
// confirmation covers that, and FormSubmit autoresponses are unavailable on
// AJAX submissions anyway.

const DEFAULT_ALIAS = '114b9ba47196273827dca2508099c239';
const DEFAULT_SITE_ORIGIN = 'https://www.beehivestrategy.com';
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function json(o, status = 200, extra = {}) {
  return new Response(JSON.stringify(o), {
    status,
    headers: Object.assign({ 'content-type': 'application/json; charset=utf-8',
                             'cache-control': 'no-store' }, extra),
  });
}

function clean(value, max) {
  return (value == null ? '' : String(value)).trim().slice(0, max);
}

async function deliver(request, env, lead, subject) {
  const alias = clean(env.CONTACT_FORM_ALIAS, 120) || DEFAULT_ALIAS;
  const origin = clean(env.CONTACT_SITE_ORIGIN, 200) || DEFAULT_SITE_ORIGIN;
  const endpoint = 'https://formsubmit.co/ajax/' + encodeURIComponent(alias);

  const res = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'accept': 'application/json',
      // FormSubmit rejects requests without a web-page Referer. In a Worker
      // there is no browser Referer, so supply the canonical site origin.
      'referer': origin.replace(/\/+$/, '') + '/contact',
      'origin': origin,
      'User-Agent': 'BeehiveContact/3.0',
    },
    body: JSON.stringify({
      name: lead.name,
      company: lead.company,
      email: lead.email,
      topic: lead.topic,
      lang: lead.lang,
      message: lead.message,
      id: lead.id,
      time: lead.ts,
      _replyto: lead.email,
      _subject: subject,
    }),
  });

  let body = {};
  try { body = await res.json(); } catch (_) { /* keep empty */ }
  const ok = res.ok && (body.success === true || body.success === 'true');
  if (!ok) {
    throw new Error('formsubmit ' + res.status + ' ' +
                    (body.message || body.error || res.statusText || 'request failed'));
  }
  return body;
}

function noticeSubject(lead) {
  return '[' + lead.id + '] Website enquiry: ' + lead.topic + ' — ' + lead.company;
}

export async function onRequestPost({ request, env }) {
  const E = env || {};
  try {
    const ctype = request.headers.get('content-type') || '';
    if (!ctype.toLowerCase().includes('application/json')) {
      return json({ ok: false, error: 'unsupported media type' }, 415, { Allow: 'POST' });
    }

    let data;
    try { data = await request.json(); }
    catch (_) { return json({ ok: false, error: 'invalid json' }, 400); }

    // Honeypot: humans never fill this hidden field. Pretend success for bots.
    if (data && clean(data.website, 200)) return json({ ok: true });

    if (!data || typeof data !== 'object') {
      return json({ ok: false, error: 'invalid payload' }, 400);
    }

    const lead = {
      id: 'ct_' + Date.now() + '_' + Math.random().toString(36).slice(2, 7),
      ts: new Date().toISOString(),
      name: clean(data.name, 120),
      company: clean(data.company, 160) || '-',
      email: clean(data.email, 160).toLowerCase(),
      topic: clean(data.topic, 120) || 'General enquiry',
      message: clean(data.message, 5000),
      lang: ['en', 'zh-cn', 'zh-hk'].indexOf(clean(data.lang, 10)) >= 0
        ? clean(data.lang, 10) : 'en',
    };

    if (!lead.name || !lead.email || !lead.message || !EMAIL_RE.test(lead.email)) {
      return json({ ok: false, error: 'invalid fields' }, 400);
    }
    if (lead.message.length < 10) {
      return json({ ok: false, error: 'message too short' }, 400);
    }

    try {
      await deliver(request, E, lead, noticeSubject(lead));
    } catch (e) {
      console.error('contact delivery failed:', e.message);
      return json({ ok: false, error: 'delivery failed' }, 500);
    }

    return json({ ok: true, id: lead.id });
  } catch (e) {
    console.error('contact handler error:', e && e.message ? e.message : e);
    return json({ ok: false, error: 'internal error' }, 500);
  }
}

// Anything other than POST gets a clean 405 instead of a Pages 404.
export async function onRequest() {
  return json({ ok: false, error: 'method not allowed' }, 405, { Allow: 'POST' });
}
