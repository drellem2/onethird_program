"""Audit of the deliverable's SECTION 2 (Theorem 1, the majority relation) and the
majority-cycle witness, rebuilt from the cover relations printed in the document.
"""

from fractions import Fraction

from kernel import (Poset, count_extensions_augmented, find_cycle,
                    majority_relation, pair_data, posets_up_to_iso,
                    restriction_counts)
from records import build_all

print("=" * 78)
print("B1  THEOREM 1, as an implication, tested on every poset n<=7 that has the")
print("    hypothesis available -- and on the hypothesis WEAKENED to 'every pair has")
print("    a majority', which is what the document says does NOT give transitivity.")
print("=" * 78)

for n in range(3, 8):
    try:
        recs = build_all(n)
    except Exception as exc:                                  # n=7 may be building
        print("n=%d unavailable (%s)" % (n, exc))
        continue
    frozen = [r for r in recs if r.delta is not None and r.delta < Fraction(1, 3)]
    tiefree = [r for r in recs if r.delta is not None and r.tie_free]
    cyc = [r for r in tiefree if not r.maj_acyclic]
    print("n=%d: %4d posets | %4d with EVERY pair decided (majority exists) | "
          "%d of those have a majority CYCLE | %d frozen (counterexamples)"
          % (n, len(recs), len(tiefree), len(cyc), len(frozen)))

print()
print("Reading: the second column is the population where the WEAKER hypothesis holds.")
print("The third is 0 at every n<=7, which is exactly what the document says must not")
print("be read as evidence for Theorem 1.")

print()
print("=" * 78)
print("B2  THE n=11 MAJORITY-CYCLE WITNESS, rebuilt from the covers in the document")
print("=" * 78)
COVERS = "0<2 0<6 0<9 1<3 1<9 2<10 3<6 3<7 4<5 4<6 6<10"
rels = [tuple(int(t) for t in c.split("<")) for c in COVERS.split()]
P11 = Poset.from_relations(11, rels)
e = restriction_counts(P11)[(1 << 11) - 1]
print("covers      : %s" % COVERS)
print("e(P)        : %d      (document says 78474 -- %s)"
      % (e, "AGREES" if e == 78474 else "DISAGREES"))
claimed = {(5, 9): Fraction(597, 1189), (9, 6): Fraction(599, 1189),
           (6, 5): Fraction(1784, 3567)}
ok = True
for (x, y), want in claimed.items():
    got = Fraction(count_extensions_augmented(P11, x, y), e)
    print("p(%d,%d)      : %s = %.5f   document says %s  -> %s"
          % (x, y, got, float(got), want, "AGREES" if got == want else "DISAGREES"))
    ok = ok and got == want
_, _, ps = pair_data(P11)
edges, tf, ac, _ = majority_relation(P11, ps)
adj = [0] * 11
for (a, b) in edges:
    adj[a] |= 1 << b
cyc = find_cycle(11, adj)
print("tie-free    : %s ; majority relation acyclic: %s" % (tf, ac))
print("cycle found : %s" % (cyc,))
print("every element present? isolated elements: %s"
      % [x for x in range(11) if P11.up[x] == 0 and P11.dn[x] == 0])

print()
print("B2a  IS THE WITNESS REALLY ELEVEN ELEMENTS?  Delete the isolated element and")
print("     recompute: p(x,y) cannot change, so the cycle survives on n=10.")
keep = [x for x in range(11) if not (P11.up[x] == 0 and P11.dn[x] == 0)]
if len(keep) < 11:
    relab = {x: i for i, x in enumerate(keep)}
    r2 = [(relab[a], relab[b]) for (a, b) in rels]
    P10 = Poset.from_relations(len(keep), r2)
    e10 = restriction_counts(P10)[(1 << len(keep)) - 1]
    _, _, ps10 = pair_data(P10)
    edges10, tf10, ac10, _ = majority_relation(P10, ps10)
    adj10 = [0] * len(keep)
    for (a, b) in edges10:
        adj10[a] |= 1 << b
    print("     n=%d, e(P)=%d, tie-free=%s, acyclic=%s, cycle=%s"
          % (len(keep), e10, tf10, ac10, find_cycle(len(keep), adj10)))
    print("     e(11-elt)/e(10-elt) = %s (inserting a free element into %d slots)"
          % (Fraction(e, e10), 11))
