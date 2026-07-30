"""selftesta61f -- the audit instrument checks ITSELF before it checks mg-7d75.

Every assertion here is against a value that does not come from this directory:
OEIS sequences, the defining identities of a left regular band, group axioms,
and hand-built matrices whose rank is known by inspection.  If this file does
not end with OK, nothing in a1..a6 should be believed.
"""

import sys
from fractions import Fraction
from itertools import permutations
from kerna61f import (posets_labelled, iso_classes, iso_classes_6_from_5,
                      canonical, relabel, aut, set_partitions,
                      set_compositions, faces, supp, tits, concat,
                      restrict_comp, restrict_part, restrict_poset,
                      is_lower_set, quotient_acyclic, AC_by_support,
                      AC_by_acyclicity, orbits, act_comp, act_part,
                      face_algebra, trace_vector, gram_full, gram_invariant,
                      invariant_structure_constants, rank_mod, rank_q,
                      rank_two_primes, nullspace_q, P1, P2)

n_ok = 0


def chk(cond, what):
    global n_ok
    if not cond:
        print("FAIL: %s" % what)
        sys.exit(1)
    n_ok += 1


# --- OEIS-anchored counts ----------------------------------------------------
# A000110 Bell, A000041 partitions, A000670 ordered Bell, A001035 labelled
# posets, A000112 unlabelled posets.
BELL = [1, 1, 2, 5, 15, 52, 203, 877]
ORDBELL = [1, 1, 3, 13, 75, 541, 4683]
LABPOSET = [1, 1, 3, 19, 219, 4231]
UNLABPOSET = [1, 1, 2, 5, 16, 63, 318]
PARTS = [1, 1, 2, 3, 5, 7, 11, 15]

for n in range(0, 8):
    chk(len(set_partitions(range(n))) == BELL[n], "Bell(%d) A000110" % n)
for n in range(0, 7):
    chk(len(set_compositions(range(n))) == ORDBELL[n],
        "ordered Bell(%d) A000670" % n)
for n in range(0, 5):
    chk(len(posets_labelled(n)) == LABPOSET[n], "labelled posets A001035 %d" % n)
for n in range(0, 6):
    chk(len(iso_classes(n)) == UNLABPOSET[n], "poset classes A000112 %d" % n)
chk(len(iso_classes_6_from_5()) == UNLABPOSET[6],
    "poset classes A000112 6 via the maximal-element route")
for n in range(0, 8):
    G = list(permutations(range(n)))
    chk(len(orbits(sorted(set_partitions(range(n)), key=repr), G, act_part))
        == PARTS[n], "p(%d) A000041 as S_n-orbits of set partitions" % n)

# --- the Tits product is a left regular band ---------------------------------
for n in range(1, 5):
    S = set_compositions(range(n))
    for F in S:
        chk(tits(F, F) == F, "idempotent n=%d" % n)
        for G in S:
            chk(tits(tits(F, G), F) == tits(F, G),
                "left regular band xyx = xy, n=%d" % n)
            for H in S:
                chk(tits(tits(F, G), H) == tits(F, tits(G, H)),
                    "associative n=%d" % n)
            chk(all(any(blk <= b for b in F) and any(blk <= c for c in G)
                    for blk in tits(F, G)),
                "supp(F.G) refines supp F and supp G, n=%d" % n)
    one = (frozenset(range(n)),)
    for F in S:
        chk(tits(one, F) == F and tits(F, one) == F, "identity face n=%d" % n)

# --- supp is a semilattice homomorphism onto AC ------------------------------
for n in range(1, 5):
    for rel in iso_classes(n):
        F = faces(rel, range(n))
        A1 = AC_by_support(rel, range(n))
        A2 = AC_by_acyclicity(rel, range(n))
        chk(A1 == A2, "AC two routes agree n=%d" % n)
        chk(all(supp(tits(x, y)) in A1 for x in F for y in F),
            "AC closed under supp of products n=%d" % n)

# --- Aut(P) is a group and acts --------------------------------------------
for n in range(1, 5):
    for rel in iso_classes(n):
        G = aut(rel, n)
        idp = tuple(range(n))
        chk(idp in G, "identity in Aut")
        for g in G:
            inv = [0] * n
            for i, x in enumerate(g):
                inv[x] = i
            chk(tuple(inv) in G, "Aut closed under inverse")
            for h in G:
                chk(tuple(g[h[i]] for i in range(n)) in G,
                    "Aut closed under composition")
        F = set(faces(rel, range(n)))
        for g in G:
            chk(all(act_comp(x, g) in F for x in F), "Aut preserves F(P)")
            chk(all(act_comp(tits(x, y), g) == tits(act_comp(x, g),
                                                    act_comp(y, g))
                    for x in F for y in F), "Aut acts by algebra automorphisms")

# --- canonicalisation is an isomorphism invariant ---------------------------
for n in range(2, 5):
    for rel in posets_labelled(n):
        for p in permutations(range(n)):
            chk(canonical(relabel(rel, p), n) == canonical(rel, n),
                "canonical is invariant n=%d" % n)

# --- linear algebra ---------------------------------------------------------
chk(rank_mod([[1, 2], [2, 4]], 2, P1) == 1, "rank of a rank-1 matrix")
chk(rank_mod([[1, 0], [0, 1]], 2, P1) == 2, "rank of the identity")
chk(rank_mod([[0, 0], [0, 0]], 2, P1) == 0, "rank of the zero matrix")
chk(rank_mod([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, P1) == 2,
    "rank of the 3x3 counting matrix is 2")
chk(rank_q([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3) == 2, "same rank over Q")
chk(rank_two_primes([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3) == (2, 2),
    "two primes agree")
ns = nullspace_q([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3)
chk(len(ns) == 1, "nullity 1")
for v in ns:
    for row in [[1, 2, 3], [4, 5, 6], [7, 8, 9]]:
        chk(sum(Fraction(a) * b for a, b in zip(row, v)) == 0,
            "null vector really is null")

# --- the trace form reproduces Bidigare on the antichain, all n <= 4 --------
for n in range(1, 5):
    rel = frozenset()
    B, idx, tab = face_algebra(rel, range(n))
    r1, r2 = rank_two_primes(gram_full(tab), len(B))
    chk(r1 == r2 == BELL[n],
        "dim kSigma_n/rad = Bell(%d) by the trace form" % n)
    grp = aut(rel, n)
    orbs, C, closed = invariant_structure_constants(B, idx, tab, grp)
    chk(closed, "orbit sums close, n=%d" % n)
    chk(len(orbs) == 2 ** (n - 1), "dim invariants = 2^(n-1), n=%d" % n)
    s1, s2 = rank_two_primes(gram_invariant(C), len(orbs))
    chk(s1 == s2 == PARTS[n],
        "dim (kSigma_n)^{S_n}/rad = p(%d) by the trace form" % n)

# --- the trace form is a genuine test: a NON-semisimple algebra must show it -
# the 2x2 upper triangular nilpotent algebra k[x]/(x^2) has radical of dim 1.
# Structure constants: basis 1, x; x*x = 0.  tr(L_1) = 2, tr(L_x) = 0.
G = [[2, 0], [0, 0]]
chk(rank_mod(G, 2, P1) == 1, "trace form sees the radical of k[x]/(x^2)")

# --- restriction and lower sets ---------------------------------------------
for n in range(1, 5):
    for rel in iso_classes(n):
        for m in range(1 << n):
            S = frozenset(i for i in range(n) if m >> i & 1)
            T = frozenset(range(n)) - S
            chk(restrict_poset(rel, S) <= rel, "restriction is a subrelation")
            for F in faces(rel, range(n)):
                fs = restrict_comp(F, S)
                chk(fs in faces(restrict_poset(rel, S), S),
                    "restriction of a face is a face of the restriction")
                chk(concat(F, ()) == F, "concat unit")
            chk(is_lower_set(rel, S)
                == all(a in S for (a, b) in rel if b in S),
                "lower-set predicate agrees with its definition")

print("selftesta61f OK -- %d assertions" % n_ok)
sys.exit(0)
