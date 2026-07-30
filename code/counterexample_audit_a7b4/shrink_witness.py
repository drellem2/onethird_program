"""How small can a majority-cycle witness be?

The document exhibits one at n = 11 and reports that a random search found none at
n = 8, 9, 10.  Its own witness has an ISOLATED element, so it is an n = 10 witness
already.  This script pushes further: delete elements from the witness, and search
random posets at n = 8, 9 with a larger budget, to price that negative.
"""

import random
import sys
from fractions import Fraction

from kernel import (Poset, find_cycle, majority_relation, pair_data,
                    restriction_counts)

COVERS = "0<2 0<6 0<9 1<3 1<9 2<10 3<6 3<7 4<5 4<6 6<10"
BASE = [tuple(int(t) for t in c.split("<")) for c in COVERS.split()]


def has_cycle(P):
    _, _, ps = pair_data(P)
    edges, tf, ac, _ = majority_relation(P, ps)
    if ac:
        return None
    adj = [0] * P.n
    for (a, b) in edges:
        adj[a] |= 1 << b
    return find_cycle(P.n, adj)


def restrict(P, keep):
    relab = {x: i for i, x in enumerate(sorted(keep))}
    rels = [(relab[a], relab[b]) for a in range(P.n) for b in range(P.n)
            if (P.up[a] >> b) & 1 and a in relab and b in relab]
    return Poset.from_relations(len(keep), rels)


P = Poset.from_relations(11, BASE)
print("start: n=11, cycle %s" % (has_cycle(P),))

cur = P
while True:
    best = None
    for x in range(cur.n):
        keep = [y for y in range(cur.n) if y != x]
        Q = restrict(cur, keep)
        c = has_cycle(Q)
        if c is not None:
            best = (Q, c, x)
            break
    if best is None:
        break
    cur, c, x = best
    print("deleted an element -> n=%d, e(P)=%d, cycle %s"
          % (cur.n, restriction_counts(cur)[(1 << cur.n) - 1], c))
print("smallest witness reached by single-element deletion: n=%d" % cur.n)
print("  covers: %s" % cur.covers_string())
_, _, ps = pair_data(cur)
_, tf, ac, _ = majority_relation(cur, ps)
print("  tie-free=%s acyclic=%s e(P)=%d"
      % (tf, ac, restriction_counts(cur)[(1 << cur.n) - 1]))
print("  the three cycle edges and their margins:")
adj = [0] * cur.n
edges, _, _, _ = majority_relation(cur, ps)
for (a, b) in edges:
    adj[a] |= 1 << b
cyc = find_cycle(cur.n, adj)
if cyc:
    for i in range(len(cyc) - 1):
        a, b = cyc[i], cyc[i + 1]
        key = (a, b) if (a, b) in ps else (b, a)
        p = ps[key] if key == (a, b) else 1 - ps[key]
        print("    %d -> %d   p = %s = %.5f" % (a, b, p, float(p)))

print()
print("random search at n = 8 and n = 9, larger budget than the document's 4200")
rng = random.Random(11223344)
for n in (8, 9):
    found = 0
    tries = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
    for t in range(tries):
        rels = []
        for a in range(n):
            for b in range(a + 1, n):
                if rng.random() < 0.30:
                    rels.append((a, b))
        try:
            Q = Poset.from_relations(n, rels)
        except ValueError:
            continue
        if has_cycle(Q) is not None:
            found += 1
            if found == 1:
                print("  n=%d: CYCLE FOUND after %d tries: %s" % (n, t, Q.covers_string()))
    print("  n=%d: %d cycles in %d random posets" % (n, found, tries))
