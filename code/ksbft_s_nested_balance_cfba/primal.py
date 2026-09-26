"""primal.py (mg-cfba): candidate lemma 'PRIMAL nested balance' (a balanced pair with comparable DOWN-sets
only; the prefix-determined half of NB).  Random naturally labelled posets n=4..10, indecomposable, and
their duals.  Reports the first failures (a failure of primal-only NB is a positive control that the
PNB column can fire; the dual of a primal failure is then covered by the dual half)."""
import random
from fam import closure, run, connected, fmt, rng
from longtail import dual
rnd = random.Random(7)
ps = []
for _ in range(20000):
    n = rnd.randint(4, 10); q = rnd.choice([0.2, 0.35, 0.5, 0.65])
    dn = [0] * n
    for j in range(n):
        for i in range(j):
            if rnd.random() < q: dn[j] |= 1 << i
    dn = closure(dn)
    if connected(dn) and n >= 3: ps.append(dn)
res = run(ps)
pf = [(d, r) for d, r in zip(ps, res) if r["pflag"] != "PNB"]
print(f"random indecomposable posets n=4..10: {len(ps)}; NB failures {sum(r['flag'] != 'NB' for r in res)}; primal-only failures {len(pf)}")
seen = set()
for d, r in sorted(pf, key=lambda t: len(t[0])):
    if len(seen) >= 4: break
    if tuple(d) in seen: continue
    seen.add(tuple(d))
    rd = run([dual(d)])[0]
    print(f"  PNB fails: n={r['n']} range={rng(d)} delta={r['delta']:.5f} deltaN={r['deltaN']:.5f} deltaP={r['deltaP']:.5f} | {fmt(d)} ; its dual: deltaP={rd['deltaP']:.5f} {rd['pflag']}")
