"""d1bound.py -- numerical check of PROVEN claim P4 (mg-2912):
for P with connected G(P), n >= 2, pi(P) <= D:  M >= d_1 >= P[v_1 not first] >= 1/(D+1).
Checked (a) over EVERY poset on n <= 7 elements with connected G (generated
here independently of probe.cpp, by brute force over relations), and (b) over
every record in the given .jsonl files.  Exact arithmetic.
"""
import json, sys
from fractions import Fraction
from itertools import combinations
import exact

def all_posets(n):
    # every transitively closed strict order on {0..n-1} with the natural labelling
    # (each iso class appears at least once; that is enough for a universal check)
    pairs = [(a, b) for a in range(n) for b in range(a + 1, n)]
    seen = set()
    for mask in range(1 << len(pairs)):
        down = [0] * n
        for k, (a, b) in enumerate(pairs):
            if mask >> k & 1:
                down[b] |= 1 << a
        if any(down[b] >> a & 1 and (down[a] & ~down[b]) for a in range(n) for b in range(n)):
            continue  # not transitively closed
        t = tuple(down)
        if t not in seen:
            seen.add(t); yield list(down)

def connected(down):
    n = len(down); seen = {0}; st = [0]
    while st:
        v = st.pop()
        for u in range(n):
            if u not in seen and exact.incomparable(down, u, v):
                seen.add(u); st.append(u)
    return len(seen) == n

def check(down):
    r = exact.analyse(down)
    v1 = r["ord"][0]; e = r["e"]; B = r["B"]
    d1 = r["d"][0]
    n = len(down)
    first = exact.dp_first(down, v1)
    pnf = 1 - Fraction(first, e)
    D = r["pi"]
    ok = r["M"] >= d1 >= pnf >= Fraction(1, D + 1)
    return ok, float(d1 * (D + 1)), (d1 == Fraction(1, D + 1))

if __name__ == "__main__":
    tot = bad = tight = 0; worst = 9
    for n in range(2, int(sys.argv[1]) + 1):
        for down in all_posets(n):
            if not connected(down): continue
            ok, ratio, t = check(down); tot += 1; bad += not ok; tight += t; worst = min(worst, ratio)
    # NEGATIVE control: the same loop must catch a false claim (1/D in place of 1/(D+1))
    planted = sum(1 for n in range(2, int(sys.argv[1]) + 1) for down in all_posets(n)
                  if connected(down) and not exact.analyse(down)["d"][0] >= Fraction(1, max(1, exact.rng(down))))
    print(f"(neg) NEGATIVE CONTROL: planted false bound d1 >= 1/D: {planted} violations "
          + ("CAUGHT" if planted else "MISSED") + " (must be > 0)")
    if planted == 0: bad += 1
    print(f"(a) all connected-G posets n<=%s (labelled; each iso class >=1 time): {tot} checked, {bad} violations, "
          f"min d1*(pi+1) = {worst:.6f}, equality cases {tight}" % sys.argv[1])
    seen = set(); tot = bad = 0; worst = 9
    for f in sys.argv[2:]:
        for l in open(f):
            rec = json.loads(l)["rec"]; k = tuple(rec["down"])
            if k in seen: continue
            seen.add(k)
            ok, ratio, t = check(rec["down"]); tot += 1; bad += not ok; worst = min(worst, ratio)
    print(f"(b) extreme/search records: {tot} checked, {bad} violations, min d1*(pi+1) = {worst:.6f}")
    sys.exit(1 if bad else 0)
