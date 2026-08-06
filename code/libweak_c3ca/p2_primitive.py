"""P2 — P1's critical family, restricted to the population the architecture
actually admits: PRIMITIVE posets.

Why this pass exists.  P1's delta = 1/3 witnesses are ordinal sums of V
gadgets.  STATE.md rows 1-2 say `lambda_std = 1 <=> ordinal sum <=>
incomparability graph disconnected`, and a minimal counterexample is
PRIMITIVE (incomparability graph connected).  So P1's critical family is
exactly the class the wall excludes, and its E_maj readout is not evidence
about anything on the critical path.  This pass re-reads it on the primitive
population.

POPULATION: every naturally labelled poset on n elements, n = 3..6, that is
            PRIMITIVE (incomparability graph connected on all n vertices).
GRAIN:      one naturally labelled poset.
"""

import sys
from itertools import combinations

from lib_c3ca import delta_and_emaj, naturally_labelled_posets

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6
EPS = 1e-12


def primitive(n, pairs):
    """Incomparability graph connected on all n vertices."""
    adj = [set() for _ in range(n)]
    for x, y in combinations(range(n), 2):
        if (x, y) not in pairs:
            adj[x].add(y)
            adj[y].add(x)
    seen = {0}
    stack = [0]
    while stack:
        v = stack.pop()
        for w in adj[v]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return len(seen) == n


print("P2 — the critical family on the PRIMITIVE population")
print("POPULATION: naturally labelled posets on n elements that are primitive")
print("            (incomparability graph connected).  GRAIN: one such poset.")
print()

for n in range(3, NMAX + 1):
    rows = []
    for pairs in naturally_labelled_posets(n):
        delta, emaj, m = delta_and_emaj(n, pairs)
        if delta is None:
            continue
        rows.append((delta, emaj, m, primitive(n, pairs), sorted(pairs)))

    allmin = min(r[0] for r in rows)
    prim = [r for r in rows if r[3]]
    primmin = min(r[0] for r in prim) if prim else None

    print(f"n = {n}:  {len(rows)} non-chain posets, {len(prim)} of them primitive")
    print(f"  min delta, whole population : {allmin:.9f}")
    print(f"  min delta, PRIMITIVE only   : {primmin:.9f}"
          f"   ({'== 1/3' if abs(primmin - 1/3) < 1e-9 else 'STRICTLY ABOVE 1/3'})")

    crit_all = [r for r in rows if abs(r[0] - allmin) < EPS]
    crit_prim = [r for r in prim if abs(r[0] - primmin) < EPS]
    ba = max(crit_all, key=lambda r: r[1])
    bp = max(crit_prim, key=lambda r: r[1])
    print(f"  critical family, whole pop  : {len(crit_all)} posets, "
          f"max E_maj = {ba[1]:.6f}  (E_maj/n^2 = {ba[1]/n/n:.6f}), "
          f"{'primitive' if ba[3] else 'DECOMPOSABLE'}")
    print(f"  critical family, PRIMITIVE  : {len(crit_prim)} posets, "
          f"max E_maj = {bp[1]:.6f}  (E_maj/n^2 = {bp[1]/n/n:.6f})")
    print(f"    witness: {bp[4]}")
    # how much E_maj can a primitive poset carry while staying near-frozen?
    for thr in (1 / 3 + 1e-9, 0.36, 0.40):
        band = [r for r in prim if r[0] <= thr + EPS]
        if band:
            b = max(band, key=lambda r: r[1])
            print(f"  primitive with delta <= {thr:.4f}: {len(band):5d} posets, "
                  f"max E_maj = {b[1]:.6f}  (E_maj/n^2 = {b[1]/n/n:.6f})")
        else:
            print(f"  primitive with delta <= {thr:.4f}: 0 posets")
    print()

print("== control: the ordinal sum of k V gadgets (P1's own critical witness) ==")
print("   delta = 1/3 exactly, E_maj = (2/3)k = (2/9)n exactly — a delta = 1/3")
print("   family with E[inv_e] = Theta(n), i.e. LIB, not merely (LIB-weak).")
for k in (1, 2, 3, 4):
    n = 3 * k
    pairs = set()
    for b in range(k):
        base = 3 * b
        # block: base < base+1, base+2 free within the block
        pairs.add((base, base + 1))
        # ordinal sum: everything in earlier blocks below everything later
        for earlier in range(base):
            for later in range(base, base + 3):
                pairs.add((earlier, later))
    delta, emaj, m = delta_and_emaj(n, pairs)
    print(f"  k={k}  n={n:2d}: delta = {delta:.9f}  E_maj = {emaj:.6f}"
          f"  (hand: {2*k/3:.6f})  E_maj/n = {emaj/n:.6f}  primitive = {primitive(n, pairs)}")
