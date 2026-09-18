#!/usr/bin/env python3
"""Peek structure of gaps_audit.json + deep_audit.json (read-only)."""
import json

g = json.load(open('gaps_audit.json'))
print("gaps type:", type(g).__name__)
if isinstance(g, dict):
    for k, v in g.items():
        print(" ", k, type(v).__name__, (len(v) if hasattr(v, '__len__') else v))
        if isinstance(v, dict):
            for k2, v2 in list(v.items())[:3]:
                print("    ", k2, type(v2).__name__,
                      (len(v2) if hasattr(v2, '__len__') else v2), str(v2)[:120])
elif isinstance(g, list):
    print("  first item:", json.dumps(g[0], ensure_ascii=False)[:300])

d = json.load(open('deep_audit.json'))
print("\ndeep keys:", list(d.keys()))
s = d.get('summary', {})
print("summary keys:", list(s.keys()))
pl = s.get('per_lang', {})
for lang, st in pl.items():
    print(f"per_lang[{lang}]:", json.dumps(st, ensure_ascii=False)[:500])
sc = s.get('severity_counts', {})
for lang, sv in sc.items():
    print(f"severity[{lang}]:", json.dumps(sv, ensure_ascii=False)[:300])
