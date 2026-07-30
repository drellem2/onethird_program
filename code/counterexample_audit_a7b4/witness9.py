"""Verify the n = 9 majority-cycle witness found by this audit, and search for a
smaller one.  The document reports 'no cycle in 4200 random posets at each of
n = 8, 9, 10'; this prices that negative.
"""

import random
import sys
from fractions import Fraction

from kernel import (Poset, find_cycle, majority_relation, pair_data,
                    restriction_counts, canonical_key)

W9 = "0<5 0<8 1<4 1<6 2<3 2<7 3<6 4<8 5<7"


def cycle_of(P):
    _, _, ps = pair_data(P)
    edges, tf, ac, _ = majority_relation(P, ps)
    if ac:
        return None, ps, tf
    adj = [0] * P.n
    for (a, b) in edges:
        adj[a] |= 1 << b
    return find_cycle(P.n, adj), ps, tf


def show(P, label):
    cyc, ps, tf = cycle_of(P)
    e = restriction_counts(P)[(1 << P.n) - 1]
    print("%s: n=%d  e(P)=%d  tie-free=%s  covers %s"
          % (label, P.n, e, tf, P.covers_string()))
    if cyc is None:
        print("    no majority cycle")
        return False
    print("    majority %d-cycle %s" % (len(cyc) - 1, " -> ".join(map(str, cyc))))
    for i in range(len(cyc) - 1):
        a, b = cyc[i], cyc[i + 1]
        key = (a, b) if (a, b) in ps else (b, a)
        p = ps[key] if key == (a, b) else 1 - ps[key]
        print("      p(%d,%d) = %-12s = %.5f   %s"
              % (a, b, p, float(p),
                 "INSIDE the forbidden band [1/3,2/3]"
                 if Fraction(1, 3) <= p <= Fraction(2, 3) else "outside the band"))
    return True


rels = [tuple(int(t) for t in c.split("<")) for c in W9.split()]
P9 = Poset.from_relations(9, rels)
show(P9, "AUDIT WITNESS n=9")
print("    isolated elements: %s"
      % [x for x in range(9) if P9.up[x] == 0 and P9.dn[x] == 0])

print()
print("shrink by single-element deletion:")
cur = P9
while True:
    nxt = None
    for x in range(cur.n):
        keep = sorted(y for y in range(cur.n) if y != x)
        relab = {y: i for i, y in enumerate(keep)}
        rl = [(relab[a], relab[b]) for a in range(cur.n) for b in range(cur.n)
              if (cur.up[a] >> b) & 1 and a in relab and b in relab]
        Q = Poset.from_relations(len(keep), rl)
        c, _, _ = cycle_of(Q)
        if c is not None:
            nxt = Q
            break
    if nxt is None:
        print("    no single deletion keeps a cycle; stopped at n=%d" % cur.n)
        break
    cur = nxt
    show(cur, "  shrunk")

print()
print("random search at n = 8 across several edge densities")
tries = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
rng = random.Random(987654321)
found8 = []
for dens in (0.20, 0.25, 0.30, 0.35, 0.40, 0.45):
    hits = 0
    for t in range(tries):
        rl = [(a, b) for a in range(8) for b in range(a + 1, 8) if rng.random() < dens]
        try:
            Q = Poset.from_relations(8, rl)
        except ValueError:
            continue
        c, _, _ = cycle_of(Q)
        if c is not None:
            hits += 1
            if hits == 1:
                found8.append(Q)
    print("  density %.2f : %d cycles in %d random posets" % (dens, hits, tries))
if found8:
    show(found8[0], "SMALLEST FOUND n=8")
else:
    print("  no n=8 witness found in %d random posets across 6 densities" % (6 * tries))
