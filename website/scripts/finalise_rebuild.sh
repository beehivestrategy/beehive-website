#!/usr/bin/env bash
# Finalise the rebuilt 2026-09-18 window:
#   1. render any missing social cards
#   2. rebuild manifest, sitemaps and llms.txt from the live file tree
#   3. run the format QA and both site gates
set -u
cd "$(dirname "$0")/.." || exit 1

echo "== social cards =="
python3 scripts/render_cards_pil.py --from 20260918 --only-missing

echo "== manifest =="
python3 - <<'PY'
import json
from pathlib import Path
root = Path('.')
old = json.loads((root / 'blog/articles/manifest.json').read_text())
live = {p.stem for p in (root / 'blog/articles').glob('*.html')}
kept = [a for a in old['articles'] if a['slug'] in live]
old['articles'] = kept
old['totalArticles'] = len(kept)
old['lastUpdated'] = '2026-11-23'
(root / 'blog/articles/manifest.json').write_text(json.dumps(old, ensure_ascii=False, indent=2))
print('manifest entries:', len(kept))
PY

echo "== sitemaps =="
cd .. && python3 _v4/rebuild_sitemaps.py --apply | tail -4 && cd website

echo "== llms.txt =="
python3 scripts/gen_llms_txt.py | tail -2

echo "== format QA =="
python3 scripts/qa_rebuild.py --scan-from 20260918

echo "== design gate =="
cd .. && python3 _v4/verify_v4.py | tail -3

echo "== site gate =="
python3 _v4/verify_site.py | tail -6
