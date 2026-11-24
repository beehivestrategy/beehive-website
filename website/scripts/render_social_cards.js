#!/usr/bin/env node
/**
 * render_social_cards.js — 1200x630 social share cards per article.
 *
 * WHY (Kenneth, 2026-11-21):
 *   The old og:image was the same light conceptual diagram used on the page.
 *   It had NO headline, so a link pasted into Facebook / X / LinkedIn /
 *   WhatsApp showed an abstract blue shape with no idea what the post was
 *   about. A share card has one job: say what it is, at a glance.
 *
 *   This renders a dedicated card per locale:
 *     - the localised title (from the page's own <title>)
 *     - the section / topic eyebrow
 *     - a one-line summary
 *     - the article's own diagram as the visual, so the card and the page
 *       show the same artwork
 *     - brand mark + domain
 *
 *   Output: assets/blog/social/<locale>/<slug>.jpg  (1200x630)
 *
 * Usage:
 *   NODE_PATH=<workspace>/node_modules node render_social_cards.js [--sample N]
 */
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const WEB = path.resolve(__dirname, '..');
const MANIFEST = path.join(__dirname, 'social_manifest.json');
const OUT_ROOT = path.join(WEB, 'assets', 'blog', 'social');
const SVG_DIR = path.join(WEB, 'assets', 'blog', 'svg');

const W = 1200, H = 630;

// --- palette (accenture.css :root) ---------------------------------------
const INK = '#101828';
const SLATE = '#4A5568';
const MUTED = '#8B94A8';
const BLUE = '#0F62FE';
const BLUE_D = '#0043CE';
const WASH = '#F0F4FE';

const LATIN = 'system-ui,-apple-system,Segoe UI,Helvetica,Arial,sans-serif';
const CJK = 'system-ui,-apple-system,PingFang SC,Hiragino Sans GB,Microsoft YaHei,Noto Sans CJK SC,Helvetica,Arial,sans-serif';
const FONT = CJK;

// --- text metrics (mirrors gen_article_diagrams.py) -----------------------
function charW(ch, size) {
  const o = ch.codePointAt(0);
  if ((o >= 0x2E80 && o <= 0x9FFF) || (o >= 0xF900 && o <= 0xFAFF) ||
      (o >= 0xFF00 && o <= 0xFF60) || (o >= 0x3000 && o <= 0x303F)) return size;
  if ('iljI.,:;\'!|()[]'.includes(ch)) return size * 0.30;
  if ('mwMW@'.includes(ch)) return size * 0.86;
  if (ch === ' ') return size * 0.28;
  return size * 0.53;
}
function textW(s, size) {
  let w = 0;
  for (const ch of (s || '')) w += charW(ch, size);
  return w;
}
function esc(s) {
  return (s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
function fit(s, size, maxW) {
  s = (s || '').trim();
  if (textW(s, size) <= maxW) return s;
  let out = '';
  for (const ch of s) {
    if (textW(out + ch + '…', size) > maxW) break;
    out += ch;
  }
  return out.trim() + '…';
}
function wrap(s, size, maxW, maxLines) {
  s = (s || '').replace(/\s+/g, ' ').trim();
  if (!s) return [];
  const tokens = [];
  let buf = '';
  for (const ch of s) {
    if (charW(ch, size) >= size * 0.9) {
      if (buf) { tokens.push(buf); buf = ''; }
      tokens.push(ch);
    } else if (ch === ' ') {
      if (buf) { tokens.push(buf); buf = ''; }
    } else buf += ch;
  }
  if (buf) tokens.push(buf);
  const lines = [];
  let cur = '';
  for (const t of tokens) {
    const cand = cur && t !== ' ' ? cur + ' ' + t : cur + t;
    if (textW(cand, size) <= maxW || !cur) cur = cand;
    else { lines.push(cur); cur = t; if (lines.length >= maxLines) break; }
  }
  if (cur && lines.length < maxLines) lines.push(cur);
  if (lines.length === maxLines) lines[lines.length - 1] = fit(lines[lines.length - 1], size, maxW);
  return lines;
}
function txt(x, y, s, size, fill, weight, anchor) {
  const a = anchor && anchor !== 'start' ? ` text-anchor="${anchor}"` : '';
  const w = weight && weight !== 400 ? ` font-weight="${weight}"` : '';
  return `<text x="${Math.round(x)}" y="${Math.round(y)}" font-family="${FONT}" font-size="${size}" fill="${fill}"${w}${a}>${esc(s)}</text>`;
}

// --- card layout -----------------------------------------------------------
// Left column carries the message; right column carries the artwork.
function cardSvg(entry, locale, diagramSvg) {
  const parts = [];
  parts.push(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">`);
  parts.push(`<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#F0F4FE"/>
  </linearGradient></defs>`);
  parts.push(`<rect width="${W}" height="${H}" fill="url(#bg)"/>`);
  // Soft corner wash instead of a grid: the grid cost ~2x the JPEG size for
  // 3,633 cards and added no meaning at thumbnail size.
  parts.push(`<circle cx="${W - 40}" cy="30" r="260" fill="${BLUE}" opacity="0.045"/>`);
  parts.push(`<circle cx="${W - 190}" cy="${H - 20}" r="180" fill="${BLUE_D}" opacity="0.035"/>`);
  // blue accent bar top-left
  parts.push(`<rect x="0" y="0" width="10" height="${H}" fill="${BLUE}"/>`);

  const L = 72, RIGHT = 700;

  // eyebrow: section + date
  const eyebrowParts = [];
  if (entry.section) eyebrowParts.push(entry.section);
  if (entry.date) eyebrowParts.push(entry.date);
  parts.push(txt(L, 96, fit(eyebrowParts.join('  ·  '), 20, RIGHT - L), 20, BLUE, 600));

  // title
  const titleLines = wrap(entry.title, 52, RIGHT - L, 3);
  let ty = 168;
  for (const ln of titleLines) {
    parts.push(txt(L, ty, ln, 52, INK, 700));
    ty += 62;
  }

  // summary
  let sy = ty + 16;
  if (entry.description) {
    for (const ln of wrap(entry.description, 24, RIGHT - L - 40, 2)) {
      parts.push(txt(L, sy, ln, 24, SLATE));
      sy += 32;
    }
  }

  // rule + brand footer — pinned to the bottom so every card in a set
  // shares the same baseline regardless of description length
  const ruleY = H - 118;
  parts.push(`<rect x="${L}" y="${ruleY}" width="120" height="6" rx="3" fill="${BLUE}"/>`);
  parts.push(txt(L, ruleY + 54, 'Beehive Strategy', 26, INK, 600));
  parts.push(txt(L, ruleY + 86, 'beehivestrategy.com', 22, MUTED));

  // artwork panel on the right
  if (diagramSvg) {
    const inner = diagramSvg.replace(/^[\s\S]*?<svg[^>]*>/, '').replace(/<\/svg>\s*$/, '');
    const panelX = 720, panelY = 96, panelW = 408, panelH = 300;
    parts.push(`<g transform="translate(${panelX},${panelY}) scale(${panelW / 800},${panelH / 450})">${inner}</g>`);
    parts.push(`<rect x="${panelX - 6}" y="${panelY - 6}" width="${panelW + 12}" height="${panelH + 12}" rx="14" fill="none" stroke="#DFE5F5" stroke-width="2"/>`);
  }

  parts.push('</svg>');
  return parts.join('');
}

// --- main ------------------------------------------------------------------
(async () => {
  const manifest = JSON.parse(fs.readFileSync(MANIFEST, 'utf8'));
  const sampleIdx = process.argv.indexOf('--sample');
  const sampleN = sampleIdx >= 0 ? parseInt(process.argv[sampleIdx + 1] || '8', 10) : 0;
  const onlyMissing = process.argv.includes('--only-missing');

  let total = 0;
  for (const [locale, entries] of Object.entries(manifest)) {
    const outDir = path.join(OUT_ROOT, locale);
    fs.mkdirSync(outDir, { recursive: true });
    const slugs = Object.keys(entries).sort();
    const targets = sampleN ? slugs.slice(0, sampleN) : slugs;
    let n = 0;
    for (const slug of targets) {
      const e = entries[slug];
      if (onlyMissing && fs.existsSync(path.join(outDir, slug + '.jpg'))) continue;
      // prefer the locale's own diagram; fall back to EN
      let diagram = null;
      const locSvg = path.join(SVG_DIR, locale, slug + '.svg');
      const enSvg = path.join(SVG_DIR, 'en', slug + '.svg');
      const src = fs.existsSync(locSvg) ? locSvg : (fs.existsSync(enSvg) ? enSvg : null);
      if (src) diagram = fs.readFileSync(src, 'utf8');

      const svg = cardSvg(e, locale, diagram);
      // density 72 = 1:1 for SVG user units -> exactly 1200x630, which is
      // what og:image:width/height declare and what every platform expects.
      await sharp(Buffer.from(svg), { density: 72 })
        .resize(W, H, { fit: 'fill' })
        .jpeg({ quality: 82, mozjpeg: true })
        .toFile(path.join(outDir, slug + '.jpg'));
      n++; total++;
    }
    console.log(locale + ':', n, 'cards');
  }
  console.log('done:', total, 'social cards ->', OUT_ROOT);
})().catch(e => { console.error('FAIL', e); process.exit(1); });
