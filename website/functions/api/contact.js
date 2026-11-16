// Cloudflare Pages Function — website contact form, real online delivery.
// Route: POST /api/contact
//
// Design notes:
//   * No KV / no database. The enquiry is delivered as email only, nothing is
//     stored on the site (this matches the privacy wording on /contact).
//   * The notification to our inbox is REQUIRED: if delivery fails the caller
//     gets a 500 and the UI shows an error, so a "sent" confirmation is honest.
//   * The visitor acknowledgement is best-effort and never blocks the result.
//   * Optional bindings (set as Pages secrets on each project):
//       CONTACT_TO_EMAIL   default account@beehivestrategy.com
//       CONTACT_FROM_EMAIL default noreply@beehivestrategy.com
//       CONTACT_FROM_NAME  default "Beehive Strategy"

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

async function mailchannels(msg) {
  const res = await fetch('https://api.mailchannels.net/tx/v1/send', {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'User-Agent': 'BeehiveContact/1.0' },
    body: JSON.stringify(msg),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error('mailchannels ' + res.status + ' ' + text.slice(0, 160));
  }
  return res;
}

function noticeText(lead, lang) {
  const head = {
    en: 'New website enquiry (Beehive Strategy)',
    'zh-cn': '网站新咨询（蜂启咨询）',
    'zh-hk': '網站新諮詢（蜂啟諮詢）',
  }[lang] || 'New website enquiry (Beehive Strategy)';
  const tail = {
    en: '\n\nReply directly to this email to reach the sender.',
    'zh-cn': '\n\n直接回复此邮件即可联系发件人。',
    'zh-hk': '\n\n直接回覆此郵件即可聯絡發件人。',
  }[lang] || '\n\nReply directly to this email to reach the sender.';
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

function receiptText(lead) {
  const body = {
    en: [
      'Thanks for reaching out to Beehive Strategy.',
      '',
      'We received your enquiry ("' + lead.topic + '") and will reply within one business day.',
      '',
      'Quick reminder of what you sent:',
      lead.message,
      '',
      '— Beehive Strategy',
      'account@beehivestrategy.com | https://www.beehivestrategy.com',
    ].join('\n'),
    'zh-cn': [
      '感谢联系蜂启咨询。',
      '',
      '我们已收到你的咨询（' + lead.topic + '），会在一个工作日内回复。',
      '',
      '你提交的内容：',
      lead.message,
      '',
      '—— 蜂启咨询',
      'account@beehivestrategy.com | https://www.beehivestrategy.com',
    ].join('\n'),
    'zh-hk': [
      '感謝聯絡蜂啟諮詢。',
      '',
      '我們已收到你的諮詢（' + lead.topic + '），會在一個工作日內回覆。',
      '',
      '你提交的內容：',
      lead.message,
      '',
      '—— 蜂啟諮詢',
      'account@beehivestrategy.com | https://www.beehivestrategy.com',
    ].join('\n'),
  };
  return body[lead.lang] || body.en;
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

    // Minimum validation — required fields and a believable email.
    if (!lead.name || !lead.email || !lead.message || !EMAIL_RE.test(lead.email)) {
      return json({ ok: false, error: 'invalid fields' }, 400);
    }
    if (lead.message.length < 10) {
      return json({ ok: false, error: 'message too short' }, 400);
    }

    const to = clean(E.CONTACT_TO_EMAIL, 160) || DEFAULT_TO;
    const from = {
      email: clean(E.CONTACT_FROM_EMAIL, 160) || DEFAULT_FROM_EMAIL,
      name: clean(E.CONTACT_FROM_NAME, 120) || DEFAULT_FROM_NAME,
    };

    try {
      await mailchannels({
        personalizations: [{ to: [{ email: to }] }],
        from,
        reply_to: { email: lead.email, name: lead.name },
        subject: '[' + lead.id + '] Website enquiry: ' + lead.topic + ' — ' + lead.company,
        content: [{ type: 'text/plain', value: noticeText(lead, lead.lang) }],
      });
    } catch (e) {
      console.error('contact notice delivery failed:', e.message);
      return json({ ok: false, error: 'delivery failed' }, 500);
    }

    // Receipt is a courtesy: never turn a successfully delivered lead into an error.
    try {
      await mailchannels({
        personalizations: [{ to: [{ email: lead.email, name: lead.name }] }],
        from,
        reply_to: { email: to, name: from.name },
        subject: {
          en: 'We received your enquiry — Beehive Strategy',
          'zh-cn': '我们已收到你的咨询 — 蜂启咨询',
          'zh-hk': '我們已收到你的諮詢 — 蜂啟諮詢',
        }[lead.lang] || 'We received your enquiry — Beehive Strategy',
        content: [{ type: 'text/plain', value: receiptText(lead) }],
      });
    } catch (e) {
      console.error('contact receipt delivery failed:', e.message);
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
