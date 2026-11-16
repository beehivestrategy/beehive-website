// Cloudflare Pages Function — website contact form, real online delivery.
// Route: POST /api/contact
//
// Delivery backend: Cloudflare Email Service REST API (kept inside the existing
// Cloudflare account — no third-party mail vendor, nothing stored on the site).
//
// Required Pages secret (set on each of dev / staging / prod):
//   EMAIL_API_TOKEN  Cloudflare API token with Account > Email Sending: Edit
//
// Optional bindings:
//   EMAIL_ACCOUNT_ID   Cloudflare account id (defaults to the Beehive account)
//   CONTACT_TO_EMAIL   default account@beehivestrategy.com
//   CONTACT_FROM_EMAIL default noreply@beehivestrategy.com (domain must be
//                      onboarded in Cloudflare Email Service)
//   CONTACT_FROM_NAME  default "Beehive Strategy"
//
// Note: visitor auto-receipts are intentionally NOT sent. Sending to arbitrary
// recipient addresses requires Workers Paid; the on-page confirmation covers it.

const DEFAULT_ACCOUNT_ID = '537289925c54a4fb0beef535ae0a6158';
const DEFAULT_TO = 'account@beehivestrategy.com';
const DEFAULT_FROM_EMAIL = 'noreply@beehivestrategy.com';
const DEFAULT_FROM_NAME = 'Beehive Strategy';
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

async function sendEmail(env, opts) {
  const token = clean(env.EMAIL_API_TOKEN, 400);
  if (!token) throw new Error('EMAIL_API_TOKEN not configured');

  const account = clean(env.EMAIL_ACCOUNT_ID, 64) || DEFAULT_ACCOUNT_ID;
  const endpoint = 'https://api.cloudflare.com/client/v4/accounts/' +
                   account + '/email/sending/send';

  const res = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + token,
      'content-type': 'application/json',
      'User-Agent': 'BeehiveContact/2.0',
    },
    body: JSON.stringify({
      to: opts.to,
      from: { address: opts.from, name: opts.fromName },
      reply_to: opts.replyTo,
      subject: opts.subject,
      text: opts.text,
    }),
  });

  let body = {};
  try { body = await res.json(); } catch (_) { /* keep empty */ }
  if (!res.ok || body.success === false) {
    const detail = (body.errors || []).map(function (e) {
      return e.code + ': ' + e.message;
    }).join('; ');
    throw new Error('email service ' + res.status + ' ' +
                    (detail || res.statusText || 'request failed'));
  }
  return body;
}

function noticeText(lead) {
  const head = {
    en: 'New website enquiry (Beehive Strategy)',
    'zh-cn': '网站新咨询（蜂启咨询）',
    'zh-hk': '網站新諮詢（蜂啟諮詢）',
  }[lead.lang] || 'New website enquiry (Beehive Strategy)';
  const tail = {
    en: '\n\nReply directly to this email to reach the sender.',
    'zh-cn': '\n\n直接回复此邮件即可联系发件人。',
    'zh-hk': '\n\n直接回覆此郵件即可聯絡發件人。',
  }[lead.lang] || '\n\nReply directly to this email to reach the sender.';
  return [
    head,
    '',
    'ID:      ' + lead.id,
    'Time:    ' + lead.ts,
    'Name:    ' + lead.name,
    'Company: ' + lead.company,
    'Email:   ' + lead.email,
    'Topic:   ' + lead.topic,
    'Lang:    ' + lead.lang,
    '',
    lead.message,
    tail,
  ].join('\n');
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
      await sendEmail(E, {
        to: clean(E.CONTACT_TO_EMAIL, 160) || DEFAULT_TO,
        from: clean(E.CONTACT_FROM_EMAIL, 160) || DEFAULT_FROM_EMAIL,
        fromName: clean(E.CONTACT_FROM_NAME, 120) || DEFAULT_FROM_NAME,
        replyTo: lead.email,
        subject: '[' + lead.id + '] Website enquiry: ' + lead.topic + ' — ' + lead.company,
        text: noticeText(lead),
      });
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
