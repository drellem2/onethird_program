#!/usr/bin/env python3
"""agg.py (mg-9268) -- aggregate aud split transcripts (split by DFS index of
depth-S nodes).  Depths < S are identical in every slice (taken once, and
CHECKED identical); depths >= S are summed.  Verdict only if every slice
0..M-1 is present once, each printed RESULT CLEAN, no FATAL, frontier 0.
usage: agg.py part files..."""
import re, sys
rows = {}; top = None; idx = []; M = S = None; res = []; lptry = 0; viol = 0; maxst = 0; maxp = 0
for f in sys.argv[1:]:
    txt = open(f).read()
    m = re.search(r"split=(\d+)/(\d+)@(\d+)", txt); i, M, S = map(int, m.groups()); idx.append(i)
    r = re.search(r"RESULT (\S+) D=(\d+)", txt); res.append(r.group(1) if r and "FATAL" not in txt else "BROKEN"); D = r.group(2) if r else "?"
    t = {}
    for l in txt.splitlines():
        if l.startswith("depth"):
            v = l.split(); d = int(v[1]); vals = [int(v[j]) for j in (3, 5, 7, 9, 11)]
            if d < S: t[d] = vals
            else:
                if d == S: vals[3] = vals[3] if d not in rows else 0   # cut-prunes at depth S are made by depth S-1 parents, seen by every slice
                rows[d] = [a + b for a, b in zip(rows.get(d, [0] * 5), vals)]
    if top is None: top = t
    assert top == t, f"shallow rows differ in {f}"
    m = re.search(r"lptry (\d+) maxstates (\d+) maxpairs (\d+) violations (\d+)", txt)
    lptry += int(m.group(1)); maxst = max(maxst, int(m.group(2))); maxp = max(maxp, int(m.group(3))); viol += int(m.group(4))
allr = dict(top); allr.update(rows); tot = fr = deep = 0
print(f"# aud D={D}: {len(idx)} slices of {M}, split at depth {S}")
print("# depth        nodes         cert           lp          cut  frontier")
for d in sorted(allr):
    n, c, l, cu, f = allr[d]; tot += n; fr += f; deep = d if n else deep
    print(f"depth {d:2d} {n:12d} {c:12d} {l:12d} {cu:12d} {f:9d}")
print(f"# total nodes {tot}; deepest {deep}; LP attempts {lptry}; max cut-layer states {maxst}; max pairs {maxp}; violations {viol}")
ok = sorted(idx) == list(range(M)) and all(r == "CLEAN" for r in res) and fr == 0 and viol == 0
print(f"# slices complete: {sorted(idx) == list(range(M))}; all CLEAN: {all(r == 'CLEAN' for r in res)}")
print(f"VERDICT D={D}:", "CLEAN" if ok else "NOT ESTABLISHED")
