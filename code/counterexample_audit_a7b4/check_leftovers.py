"""Loose ends: the named false-positive poset, the one-sided filter figure, the
majority-cycle sweep over ALL posets (not only the tie-free ones), the e(P)=3
tautology behind section 4's control, and the cost claim of section 6.
"""

import time
from fractions import Fraction

from kernel import (Lattice, Poset, count_topological_sorts, levels_of,
                    majority_relation, multiplicities, pair_data,
                    posets_up_to_iso, quotient_adj, restriction_counts,
                    find_cycle)
from records import build_all, build

NS = range(3, 8)
REC = {n: build_all(n) for n in NS}


def head(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


head("L1  THE POSET THE DOCUMENT NAMES AS THE FALSE POSITIVE")
doc_covers = "0<2 0<3 1<2 2<4 3<4 3<5"
rels = [tuple(int(t) for t in c.split("<")) for c in doc_covers.split()]
P = Poset.from_relations(6, rels)
lat6 = Lattice(6)
r = build(P, lat6)
print("covers %s" % doc_covers)
print("  delta      = %s   (document says 5/14 -- %s)"
      % (r.delta, "AGREES" if r.delta == Fraction(5, 14) else "DISAGREES"))
print("  delta_walk = %s   (document says 12/37 -- %s)"
      % (r.delta_walk, "AGREES" if r.delta_walk == Fraction(12, 37) else "DISAGREES"))
print("  primitive  = %s ; e(P) = %d" % (r.primitive, r.e))
print("  so delta_walk < 1/3 <= delta: %s"
      % (r.delta_walk < Fraction(1, 3) <= r.delta))
# is it isomorphic to the one my sweep found, or its dual?
from kernel import canonical_key  # noqa: E402
mine = Poset.from_relations(6, [(2, 0), (2, 1), (3, 0), (4, 2), (4, 3), (5, 3)])
dual = Poset.from_relations(6, [(b, a) for (a, b) in rels])
print("  my sweep's witness is the SAME poset up to isomorphism: %s"
      % (canonical_key(P) == canonical_key(mine)))
print("  ... its DUAL is: %s   (delta and delta_walk are dual-invariant)"
      % (canonical_key(dual) == canonical_key(mine)))

head("L2  THE ONE-SIDED FILTER FIGURE ('retains 0.5% of the primitive population')")
for n in (6, 7):
    prim = [q for q in REC[n] if not q.chain and q.primitive]
    dmin = min(q.delta for q in prim)
    ext = [q for q in prim if q.delta == dmin]
    t = max(q.delta_walk for q in ext)
    keep = sum(1 for q in prim if q.delta_walk <= t)
    print("  n=%d: t = max delta_walk over the %d extremal posets = %s ; retained"
          " %d of %d = %.1f%%" % (n, len(ext), t, keep, len(prim),
                                  100.0 * keep / len(prim)))

head("L3  MAJORITY CYCLES OVER *ALL* POSETS n<=7 (ties included, not only tie-free)")
tot = cyc = tied = 0
prev = None
for n in range(1, 8):
    prev = posets_up_to_iso(n, prev)
    if n < 3:
        continue
    c = t = 0
    for Q in prev:
        _, _, ps = pair_data(Q)
        edges, tf, ac, _ = majority_relation(Q, ps)
        if not tf:
            t += 1
        if not ac:
            c += 1
    print("  n=%d: %d posets, %d with a tied pair, %d with a majority CYCLE"
          % (n, len(prev), t, c))
    tot += len(prev)
    cyc += c
    tied += t
print("  TOTAL n=3..7: %d posets, %d with a majority cycle  (document: 0 of 2447 -- %s)"
      % (tot, cyc, "AGREES" if (tot, cyc) == (2447, 0) else "DISAGREES"))

head("L4  WHY SECTION 4's e(P)-CONTROL IS VACUOUS AT e = 3")
print("Claim: a NON-CHAIN poset with e(P) = 3 has delta = 1/3 EXACTLY, so every")
print("member of the e = 3 control group is delta-extremal by construction and the")
print("reported tie carries no information.  Proof: for an incomparable pair the two")
print("augmented counts are positive integers summing to 3, hence {1,2}, so")
print("min(p,1-p) = 1/3 for EVERY pair.  Checked:")
for n in NS:
    g = [q for q in REC[n] if not q.chain and q.e == 3]
    print("  n=%d: %d non-chain posets with e(P)=3 ; all have delta = 1/3: %s"
          % (n, len(g), all(q.delta == Fraction(1, 3) for q in g)))

head("L5  THE COST CLAIM: is (Q(P), m) really more expensive than delta?")
prev = posets_up_to_iso(1)
for k in range(2, 8):
    prev = posets_up_to_iso(k, prev)
pop7 = prev
lat7 = Lattice(7)
sample = pop7[:60]
t0 = time.time()
for Q in sample:
    pair_data(Q)                      # this is what delta needs
t_delta = time.time() - t0
t0 = time.time()
for Q in sample:
    e = restriction_counts(Q)
    lv = levels_of(Q, lat7)
    multiplicities(Q, lat7, lv, e)
t_qm = time.time() - t0
print("  %d posets at n=7: delta route %.2fs ; (Q(P), m) route %.2fs ; ratio %.1fx"
      % (len(sample), t_delta, t_qm, t_qm / t_delta))
print("  (the document says I4 'costs strictly more to compute than delta does';")
print("   this is the measurement, on one implementation, of that claim)")
