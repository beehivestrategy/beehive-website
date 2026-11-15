// Cloudflare Pages Function: AI-readiness self-assessment lead capture.
// Mirrors playbook/mortgage-lead-form/functions/api/lead.js.
//   - KV (READINESS_KV) is authoritative: store FIRST so no lead is ever lost.
//   - Emails are best-effort; a mail failure must NOT drop the lead.
// Deploy prerequisites (set on the Pages project, not in this file):
//   * KV namespace bound as READINESS_KV
//   * var/secret LEAD_TO_EMAIL  -> Kenneth's inbox for lead notices
//   * var/secret FROM_EMAIL     -> verified MailChannels sender on beehivestrategy.com
//   * var/secret FROM_NAME      -> e.g. "Beehive Strategy"
//   * var/secret READINESS_VIEW_KEY -> shared secret for /readiness-leads viewer

function json(o, s = 200) {
  return new Response(JSON.stringify(o), {
    status: s,
    headers: { 'content-type': 'application/json' },
  });
}

const AXES_FALLBACK = ['Data', 'Governance', 'Access', 'Adoption', 'Monitoring', 'Ownership'];

async function mailchannels(env, msg) {
  const res = await fetch('https://api.mailchannels.net/tx/v1/send', {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'User-Agent': 'BeehiveReadiness/1.0' },
    body: JSON.stringify(msg),
  });
  if (!res.ok) {
    const t = await res.text().catch(() => '');
    throw new Error('mailchannels ' + res.status + ' ' + t.slice(0, 120));
  }
}

function axisLines(axes, labels) {
  const out = [];
  const n = Math.max((axes || []).length, (labels || []).length, AXES_FALLBACK.length);
  for (let i = 0; i < n; i++) {
    const name = (labels && labels[i]) || AXES_FALLBACK[i] || ('Axis ' + (i + 1));
    const val = (axes && axes[i] != null && !isNaN(axes[i])) ? axes[i] : '-';
    out.push('  ' + name + ': ' + val + ' / 100');
  }
  return out.join('\n');
}

export async function onRequestPost({ request, env }) {
  try {
    const data = await request.json();
    const email = (data.email || '').trim();
    if (!email || email.indexOf('@') < 0 || email.indexOf('.') < 0) {
      return json({ ok: false, error: 'invalid email' }, 400);
    }

    const axes = Array.isArray(data.axes) ? data.axes.map((x) => parseInt(x, 10)) : [];
    const labels = Array.isArray(data.labels) ? data.labels.map((x) => String(x).slice(0, 40)) : [];
    const overall = parseInt(data.overall, 10);
    const id = 'rd_' + Date.now() + '_' + Math.random().toString(36).slice(2, 7);
    const lead = {
      id,
      ts: new Date().toISOString(),
      email: email.slice(0, 160),
      overall: isNaN(overall) ? null : overall,
      weakest: (data.weakest || '').toString().slice(0, 80),
      tier: (data.tier || '').toString().slice(0, 80),
      axes,
      labels,
      answers: Array.isArray(data.answers) ? data.answers.slice(0, 40) : [],
    };

    // KV is authoritative — store first so no lead is lost.
    if (env.READINESS_KV) {
      await env.READINESS_KV.put(id, JSON.stringify(lead));
    } else {
      console.error('READINESS_KV not bound; lead not persisted:', id);
    }

    // Lead notice to Kenneth (best-effort).
    try {
      await mailchannels(env, {
        personalizations: [{ to: [{ email: env.LEAD_TO_EMAIL || 'kenkwok@beehivestrategy.com' }] }],
        from: { email: env.FROM_EMAIL || 'noreply@beehivestrategy.com', name: env.FROM_NAME || 'Beehive Readiness' },
        subject: 'AI readiness lead: ' + lead.email + (lead.tier ? ' (' + lead.tier + ')' : ''),
        content: [{ type: 'text/plain', value:
'新 AI 就绪度自评 Lead (' + id + ')\n' +
'时间:   ' + lead.ts + '\n' +
'邮箱:   ' + lead.email + '\n' +
'总分:   ' + (lead.overall == null ? '-' : lead.overall) + ' / 100\n' +
'分层:   ' + (lead.tier || '-') + '\n' +
'最弱轴: ' + (lead.weakest || '-') + '\n' +
'各维度:\n' + axisLines(axes, labels) + '\n\n' +
'\u2192 \u8bf7\u7528\u5176\u90ae\u7bb1\u8ddf\u8fdb\uff0c\u5f15\u7528\u5176\u753b\u50cf\u3002' }],
      });
    } catch (e) { console.error('lead email failed:', e.message); }

    // Report back to the user (best-effort).
    try {
      await mailchannels(env, {
        personalizations: [{ to: [{ email: lead.email }] }],
        from: { email: env.FROM_EMAIL || 'noreply@beehivestrategy.com', name: env.FROM_NAME || 'Beehive Strategy' },
        subject: data.subject || 'Your AI readiness profile',
        content: [{ type: 'text/plain', value:
'Your AI readiness profile (Beehive Strategy)\n\n' +
'Overall: ' + (lead.overall == null ? '-' : lead.overall) + ' / 100\n' +
'Band:    ' + (lead.tier || '-') + '\n' +
'Fix first: ' + (lead.weakest || '-') + '\n\n' +
'Score by axis:\n' + axisLines(axes, labels) + '\n\n' +
'This is a self-assessment, not an audit \u2014 it shows where to look first.\n' +
'If it points to a deployment, the next step is a diagnostic call where the\n' +
'smallest useful scope is agreed in writing:\n' +
'https://www.beehivestrategy.com/contact\n\n' +
'\u2014 Beehive Strategy' }],
      });
    } catch (e) { console.error('report email failed:', e.message); }

    return json({ ok: true, id });
  } catch (e) {
    return json({ ok: false, error: String(e).slice(0, 200) }, 500);
  }
}
