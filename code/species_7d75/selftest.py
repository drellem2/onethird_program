"""Self-test for code/species_7d75.  Every assertion is against a value that is
known independently of this code, or is a cross-check between two routes
inside it.  If any assertion fires, no output in this directory should be
believed."""

import sys
from itertools import permutations
from fractions import Fraction
from kern7d75 import (set_partitions, set_compositions, sc_product, supp,
                      bell, p_count, integer_partitions, compositions,
                      mk_poset, all_posets, poset_classes, aut, faces_of,
                      AC_by_acyclicity, AC_by_support, linear_extensions,
                      orbits, perm_sp, perm_sc, rank, nullspace)
from hopf7d75 import (posets_on, faces_on, is_lower_set, elems_F, elems_AC,
                      mu_F, de_F, decompositions)

n = 0


def ck(cond, msg):
    global n
    n += 1
    if not cond:
        print("SELFTEST FAILED: %s" % msg)
        sys.exit(1)


# --- counting primitives against published sequences -------------------------
ck([len(set_partitions(i)) for i in range(8)] == [1, 1, 2, 5, 15, 52, 203, 877],
   "Bell numbers A000110")
ck([bell(i) for i in range(8)] == [1, 1, 2, 5, 15, 52, 203, 877],
   "Bell triangle agrees with the enumeration")
ck([len(set_compositions(i)) for i in range(6)] == [1, 1, 3, 13, 75, 541],
   "ordered Bell / Fubini numbers A000670")
ck([p_count(i) for i in range(10)] == [1, 1, 2, 3, 5, 7, 11, 15, 22, 30],
   "partition numbers A000041")
ck([len(integer_partitions(i)) for i in range(10)]
   == [1, 1, 2, 3, 5, 7, 11, 15, 22, 30], "partition enumerator agrees")
ck([len(compositions(i)) for i in range(1, 7)] == [1, 2, 4, 8, 16, 32],
   "compositions of n number 2^(n-1)")
ck([len(all_posets(i)) for i in range(1, 5)] == [1, 3, 19, 219],
   "labelled posets A001035")
ck([len(poset_classes(i)) for i in range(1, 6)] == [1, 2, 5, 16, 63],
   "unlabelled posets A000112")

# --- the band structure ------------------------------------------------------
for k in (2, 3):
    SC = set_compositions(k)
    for F in SC:
        ck(sc_product(F, F) == F, "the Tits product is idempotent")
        for G in SC:
            ck(sc_product(sc_product(F, G), F) == sc_product(F, G),
               "left regular band identity xyx = xy")
            ck(sc_product(sc_product(F, G), G) == sc_product(F, G),
               "associativity witness")

# --- F(P) and AC(P), two routes ---------------------------------------------
for k in range(1, 5):
    for P in poset_classes(k):
        F = faces_of(P)
        ck(set(AC_by_acyclicity(P)) == set(AC_by_support(P)),
           "AC(P): acyclic-quotient route = support-of-F(P) route")
        chambers = [x for x in F if all(len(B) == 1 for B in x)]
        ck(len(chambers) == len(linear_extensions(P)),
           "the chambers of F(P) are the linear extensions of P")
        ck(all(sc_product(a, b) in set(F) for a in F for b in F),
           "F(P) is closed under the Tits product")
A = mk_poset(4, [])
ck(len(faces_of(A)) == 75 and len(AC_by_acyclicity(A)) == 15,
   "at the antichain, F(P) = Sigma_n and AC(P) = Pi_n")
ck(len(aut(A)) == 24, "Aut(antichain on [4]) = S_4")
ck(len(aut(mk_poset(4, [(0, 1), (1, 2), (2, 3)]))) == 1,
   "Aut(4-chain) is trivial")

# --- orbits ------------------------------------------------------------------
for k in range(1, 7):
    G = list(permutations(range(k)))
    ck(len(orbits(set_partitions(k), G, perm_sp)) == p_count(k),
       "S_n-orbits of set partitions number p(n)")
    ck(len(orbits(set_compositions(k), G, perm_sc)) == 2 ** (k - 1),
       "S_n-orbits of set compositions number 2^(n-1)")

# --- linear algebra ----------------------------------------------------------
M = [[1, 2, 3], [2, 4, 6], [1, 0, 1]]
ck(rank(M, 3) == 2, "rank")
ck(len(nullspace(M, 3)) == 1, "nullspace dimension = 3 - rank")
ns = nullspace(M, 3)[0]
ck(all(sum(Fraction(a) * b for a, b in zip(row, ns)) == 0 for row in M),
   "nullspace vectors are annihilated")

# --- the Hopf-monoid layer ---------------------------------------------------
I = frozenset(range(3))
ck(len(posets_on(I)) == 19, "posets_on agrees with all_posets")
ck(len(elems_F(frozenset())) == 1 and len(elems_AC(frozenset())) == 1,
   "both species are connected")
rel = frozenset([(0, 1)])
ck(is_lower_set(rel, frozenset([0])) and not is_lower_set(rel, frozenset([1])),
   "lower sets")
ck(len(decompositions(I)) == 8, "decompositions of a 3-set")
els = set(elems_F(I))
for (S, T) in decompositions(I):
    for x in set(elems_F(S)):
        for y in set(elems_F(T)):
            ck(mu_F(x, y) in els, "mu closes in F")
ck(set(faces_on(frozenset([0, 1]), frozenset([(0, 1)])))
   == {(frozenset([0, 1]),), (frozenset([0]), frozenset([1]))},
   "faces_on on the 2-chain, explicitly: the reversed chamber is absent")

print("selftest: %d assertions, all pass" % n)
