#!/usr/bin/env node
/**
 * render_hero_covers.js — render each article hero SVG into its matching
 * archive card cover (assets/blog/cards/<slug>.jpg).
 *
 * v4 (2026-11-20): index covers are the SAME diagram as the article hero,
 * not a separate abstract cover system. 600x315 matches the CSS aspect ratio.
 * Deterministic, language-neutral, no HTML touched.
 *
 * Usage: NODE_PATH=<workspace>/node_modules node render_hero_covers.js [--sample N]
 */
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const WEB = path.resolve(__dirname, '..');
const INDEX = path.join(WEB, 'blog', 'index.html');
const SVG_DIR = path.join(WEB, 'assets', 'blog', 'svg');
const CARD_DIR = path.join(WEB, 'assets', 'blog', 'cards');
const W = 600, H = 315;

function slugs() {
  const html = fs.readFileSync(INDEX, 'utf8');
  return [...new Set([...html.matchAll(/\/assets\/blog\/cards\/([^"']+)\.jpg/g)].map(m => m[1]))];
}

async function render(slug) {
  const src = path.join(SVG_DIR, slug + '.svg');
  const out = path.join(CARD_DIR, slug + '.jpg');
  if (!fs.existsSync(src)) throw new Error('missing hero SVG: ' + slug);
  // fit:cover + centre crop: SVG is 800x450 (16:9), card is 600x315 (~1.9:1).
  // Crop preserves the true proportions; only ~22px top/bottom is trimmed.
  await sharp(fs.readFileSync(src), { density: 220 })
    .resize(W, H, { fit: 'cover', position: 'centre' })
    .jpeg({ quality: 88, mozjpeg: true })
    .toFile(out);
  return out;
}

(async () => {
  const list = slugs();
  const sampleIdx = process.argv.indexOf('--sample');
  const targets = sampleIdx >= 0 ? list.slice(0, parseInt(process.argv[sampleIdx + 1] || '16', 10)) : list;
  console.log('slugs:', list.length, 'targets:', targets.length);
  let done = 0;
  for (const slug of targets) {
    await render(slug);
    done++;
    if (done % 200 === 0) console.log('  rendered', done);
  }
  console.log('done:', done, '->', CARD_DIR);
})().catch(e => { console.error('FAIL', e.message); process.exit(1); });
