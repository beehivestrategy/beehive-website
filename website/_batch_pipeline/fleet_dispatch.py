#!/usr/bin/env python3
"""Fleet dispatcher decision script (read-mostly; only cleans in_flight).
Run: python3 fleet_dispatch.py
Outputs JSON: {all_done, done_count, next_wave, should_launch, in_flight, reason}
The caller (agent/automation) launches next_wave, then writes dispatch_state.json
with last_launch=now and in_flight = cleaned + successfully_launched batches.
"""
import os, glob, json, time
from datetime import datetime
from collections import defaultdict

ROOT = "/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
LANGS = {"en": "blog/articles", "cn": "zh-cn/blog/articles", "tw": "zh-tw/blog/articles"}
CUTOFF = datetime(2026, 8, 27, 1, 30)
PIPELINE = os.path.join(ROOT, "_batch_pipeline")
STATE_PATH = os.path.join(PIPELINE, "dispatch_state.json")
GATE_SECONDS = 2100  # 35 min between waves

def mt(p):
    try: return datetime.fromtimestamp(os.path.getmtime(p))
    except: return None

batch_files = sorted(glob.glob(os.path.join(PIPELINE, "batches", "batch_*.txt")))
slug2batch = {}
for bf in batch_files:
    for line in open(bf, encoding="utf-8"):
        s = line.strip()
        if s: slug2batch[s] = os.path.basename(bf)

full_count = defaultdict(int)
partial_count = defaultdict(int)
for slug, bf in slug2batch.items():
    files = [os.path.join(ROOT, LANGS[l], slug + ".html") for l in ("en", "cn", "tw")]
    after = [mt(f) for f in files if mt(f) and mt(f) >= CUTOFF]
    if len(after) == 3: full_count[bf] += 1
    elif len(after) > 0: partial_count[bf] += 1

status = {}
for bf in [os.path.basename(b) for b in batch_files]:
    exp = sum(1 for s, b in slug2batch.items() if b == bf)
    if full_count[bf] == exp: status[bf] = "DONE"
    elif full_count[bf] + partial_count[bf] > 0: status[bf] = "PARTIAL"
    else: status[bf] = "PENDING"

# load + clean in_flight
state = {"last_launch": 0.0, "in_flight": {}}
if os.path.exists(STATE_PATH):
    try: state = json.load(open(STATE_PATH))
    except: pass
inflight = state.get("in_flight", {})
now = time.time()
cleaned = {}
for b, t in inflight.items():
    if status.get(b) == "DONE":
        continue  # finished -> free
    if now - t > 7200:
        continue  # stale (>2h) -> assume finished/failed, let re-audit catch
    cleaned[b] = t
# write back cleaned in_flight (preserve last_launch)
json.dump({"last_launch": state.get("last_launch", 0.0), "in_flight": cleaned}, open(STATE_PATH, "w"))

order = sorted(status.keys())
next_wave = [b for b in order if status[b] != "DONE" and b not in cleaned][:3]
done = [b for b, s in status.items() if s == "DONE"]
all_done = len(done) == len(status)
last_launch = state.get("last_launch", 0.0)
should = (now - last_launch) > GATE_SECONDS
reason = "all_done" if all_done else ("cooldown" if not should else ("no_pending" if not next_wave else "ready"))

print(json.dumps({
    "all_done": all_done,
    "done_count": len(done),
    "total": len(status),
    "next_wave": next_wave,
    "should_launch": should and bool(next_wave) and not all_done,
    "in_flight": list(cleaned.keys()),
    "reason": reason,
}, indent=2))
