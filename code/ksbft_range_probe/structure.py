"""structure.py -- recurring structure among low-delta posets (mg-2912, Q5).

For every distinct record tagged min_delta in the given .jsonl files with
delta < THRESH, tabulate: width; whether delta is attained at an END pair
(the pair {v1,v2} or {v_{n-1},v_n} in height order); whether the attaining
end element has exactly one incomparable (so delta = d_1 = M-candidate);
whether delta == M; whether d is antisymmetric (d_i = -d_{n+1-i}, a proxy for
self-duality); and whether the poset contains a BFT triple of Lemma-3.2 shape.
EMPIRICAL: the population is the top-K lists probe.cpp kept, NOT all posets.
"""
import json, sys
from collections import Counter
from fractions import Fraction

THRESH = Fraction(sys.argv[1])
seen = set(); rows = []
for f in sys.argv[2:]:
    for line in open(f):
        o = json.loads(line)
        if o["tag"] not in ("min_delta", "search_delta"): continue
        r = o["rec"]; k = tuple(r["down"])
        if k in seen: continue
        seen.add(k)
        e = int(r["e"]); dl = Fraction(int(r["delta_num"]), e)
        if dl >= THRESH: continue
        down = r["down"]; n = len(down); ordr = r["ord"]; pos = {v: i + 1 for i, v in enumerate(ordr)}
        inc = lambda a, b: a != b and not (down[a] >> b & 1) and not (down[b] >> a & 1)
        d = [Fraction(int(r["S"][v]), e) - (i + 1) for i, v in enumerate(ordr)]
        M = Fraction(int(r["M_num"]), e)
        # all attaining pairs: recompute from exact module
        import exact
        res = exact.analyse(down)
        ends = []
        for (a, b) in res["pairs"]:
            s = sorted((pos[a], pos[b]))
            ends.append(s == [1, 2] or s == [n - 1, n])
        v1, vn = ordr[0], ordr[-1]
        uniq = sum(inc(v1, u) for u in range(n)) == 1 and sum(inc(vn, u) for u in range(n)) == 1
        anti = all(d[i] == -d[n - 1 - i] for i in range(n))
        rows.append(dict(n=n, pi=r["pi"], w=r["width"], delta=dl, end_all=all(ends), end_any=any(ends),
                         uniq=uniq, dM=(dl == M), anti=anti, struct=r["nstruct"] > 0))
print(f"records with delta < {THRESH} (= {float(THRESH):.4f}): {len(rows)}")
for key in ["w", "end_all", "end_any", "uniq", "dM", "anti", "struct"]:
    print(f"  {key:8s}", dict(sorted(Counter(r[key] for r in rows).items())))
print("  by (pi, width):", dict(sorted(Counter((r['pi'], r['w']) for r in rows).items())))
