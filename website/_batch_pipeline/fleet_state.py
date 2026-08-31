#!/usr/bin/env python3
"""Fleet state check for the blog GEO/SEO rewrite.
Prints JSON: done/partial/pending batch lists + recommended next wave.
Run from anywhere: python3 fleet_state.py
"""
import os, glob, json
from datetime import datetime

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
LANGS = {"en": "blog/articles", "cn": "zh-cn/blog/articles", "tw": "zh-tw/blog/articles"}
CUTOFF = datetime(2026, 8, 27, 1, 30)  # fleet start; files modified after this = processed

def mt(p):
    try: return datetime.fromtimestamp(os.path.getmtime(p))
    except: return None

batch_dir = os.path.join(ROOT, "_batch_pipeline/batches")
batch_files = sorted(glob.glob(os.path.join(batch_dir, "batch_*.txt")))

slug2batch = {}
for bf in batch_files:
    for line in open(bf, encoding="utf-8"):
        s = line.strip()
        if s: slug2batch[s] = os.path.basename(bf)

# aggregate per batch: count slugs whose all 3 language files were modified after CUTOFF
from collections import defaultdict
full_count = defaultdict(int)
partial_count = defaultdict(int)
for slug, bf in slug2batch.items():
    files = [os.path.join(ROOT, LANGS[l], slug + ".html") for l in ("en", "cn", "tw")]
    after = [mt(f) for f in files if mt(f) and mt(f) >= CUTOFF]
    if len(after) == 3: full_count[bf] += 1
    elif len(after) > 0: partial_count[bf] += 1

total_slugs = len(set(slug2batch.values()))  # not used; per-batch full check below
status = {}
for bf in [os.path.basename(b) for b in batch_files]:
    # each batch file is expected to hold ~18 slugs; DONE only if ALL its slugs fully after cutoff
    # determine expected slug count for this batch
    exp = sum(1 for s, b in slug2batch.items() if b == bf)
    if full_count[bf] == exp: status[bf] = "DONE"
    elif full_count[bf] + partial_count[bf] > 0: status[bf] = "PARTIAL"
    else: status[bf] = "PENDING"

done = [b for b, s in status.items() if s == "DONE"]
partial = [b for b, s in status.items() if s == "PARTIAL"]
pending = [b for b, s in status.items() if s == "PENDING"]

# next wave: next up to 3 batches (numeric order) not DONE
order = sorted(status.keys())
next_wave = [b for b in order if status[b] != "DONE"][:3]

# last write across all articles
allf = []
for d in LANGS.values():
    allf += glob.glob(os.path.join(ROOT, d, "*.html"))
latest = max((mt(f) for f in allf if mt(f)), default=None)
now = datetime.now()
mins_since_write = int((now - latest).total_seconds() / 60) if latest else 9999

out = {
    "total": len(status),
    "done": done,
    "partial": partial,
    "pending": pending,
    "done_count": len(done),
    "next_wave": next_wave,
    "mins_since_last_write": mins_since_write,
    "all_done": len(done) == len(status),
}
print(json.dumps(out, indent=2))
