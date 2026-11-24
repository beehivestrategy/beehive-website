#!/usr/bin/env node
/**
 * render_covers_v5.js — replace the old dark, title-baked article cover JPGs
 * (assets/blog/covers/{en,zh-cn,zh-tw}/<slug>.jpg) with the SAME light conceptual
 * diagram used by the article hero + index card (v4 system).
 *
 * Why: the old covers baked the English/Chinese title into the image, so the
 * article page showed the title twice (image + H1) and clashed with the new
 * light IBM-blue editorial theme. The diagram is language-neutral, so all three
 * locale directories receive the identical clean image — no baked text, no
 * duplicate title, and the cover now matches the card + body hero.
 *
 * Zero HTML touched: every article already references covers/<lang>/<slug>.jpg
 * in its og:image / twitter:image / JSON-LD / <figure class="article-hero">.
 *
 * Usage: NODE_PATH=<workspace>/node_modules node render_covers_v5.js [--sample N]
 */
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const WEB = path.resolve(__dirname, '..');
const SVG_DIR = path.join(WEB, 'assets', 'blog', 'svg');
const COVER_DIR = path.join(WEB, 'assets', 'blog', 'covers');
const LANGS = ['en', 'zh-cn', 'zh-tw'];
const W = 1200, H = 630;

function slugs() {
  return fs.readdirSync(SVG_DIR)
    .filter(f => f.endsWith('.svg'))
    .map(f => f.slice(0, -4))
    .sort();
}

async function render(slug) {
  const src = fs.readFileSync(path.join(SVG_DIR, slug + '.svg'));
  const buf = await sharp(src, { density: 220 })
    .resize(W, H, { fit: 'cover', position: 'centre' })
    .jpeg({ quality: 90, mozjpeg: true })
    .toBuffer();
  for (const lang of LANGS) {
    fs.writeFileSync(path.join(COVER_DIR, lang, slug + '.jpg'), buf);
  }
}

(async () => {
  const list = slugs();
  const s = process.argv.indexOf('--sample');
  const targets = s >= 0 ? list.slice(0, parseInt(process.argv[s + 1] || '16', 10)) : list;
  console.log('slugs:', list.length, 'langs:', LANGS.length, 'targets:', targets.length);
  let done = 0;
  for (const slug of targets) {
    await render(slug);
    done++;
    if (done % 200 === 0) console.log('  rendered', done);
  }
  console.log('done:', done, 'covers ->', COVER_DIR);
})().catch(e => { console.error('FAIL', e.message); process.exit(1); });
