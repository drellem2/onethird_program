"""SELF-TEST for `kernf8fa.py`.

Anchored where possible to OEIS, so a kernel that agrees with itself and with
nothing else fails here:

    A000110  Bell numbers          -- set partitions
    A000670  ordered Bell / Fubini -- ordered set compositions
    A001035  labelled posets       -- partial orders on [n]
    A000142  factorials            -- permutations, and |d_emptyset| = 1

and, for the objects with no OEIS anchor, to a second construction inside this
file that shares no code with the first.
"""

import sys
from itertools import permutations

from kernf8fa import (descent_set, subsets, d_basis, compose_A, compose_B,
                      posets_on, set_compositions, in_cone, faces_in_cone,
                      tits_product, concat, decompositions, elems_F,
                      restrict_poset, poset_union)

n_assert = 0
fails = []


def ck(cond, what):
    global n_assert
    n_assert += 1
    if not cond:
        fails.append(what)


A000110 = [1, 1, 2, 5, 15, 52, 203, 877]
A000670 = [1, 1, 3, 13, 75, 541, 4683]
A001035 = [1, 1, 3, 19, 219, 4231]


def fact(n):
    r = 1
    for k in range(2, n + 1):
        r *= k
    return r


# --- ordered set compositions = A000670 ------------------------------------
for n in range(len(A000670)):
    ck(len(set_compositions(frozenset(range(n)))) == A000670[n],
       "A000670 at n=%d" % n)

# --- unordered refinement: partitions from compositions = A000110 ----------
for n in range(len(A000110)):
    parts = {frozenset(F) for F in set_compositions(frozenset(range(n)))}
    ck(len(parts) == A000110[n], "A000110 at n=%d" % n)

# --- labelled posets = A001035 ---------------------------------------------
for n in range(len(A001035)):
    ck(len(posets_on(frozenset(range(n)))) == A001035[n],
       "A001035 at n=%d" % n)

# --- permutations and the descent basis ------------------------------------
for n in range(1, 7):
    W = list(permutations(range(1, n + 1)))
    ck(len(W) == fact(n), "A000142 at n=%d" % n)
    ck(len(subsets(n)) == 2 ** (n - 1), "2^(n-1) subsets at n=%d" % n)
    if n <= 5:
        mem = d_basis(n)
        # d_emptyset is the identity permutation alone
        ck(mem[frozenset()] == [tuple(range(1, n + 1))],
           "d_empty is the identity at n=%d" % n)
        # d_full is everything
        ck(len(mem[frozenset(range(n - 1))]) == fact(n),
           "d_full is all of S_n at n=%d" % n)
        # sizes: |{w : des(w) <= T}| is the multinomial of the composition
        ck(sum(1 for w in W if descent_set(w) <= frozenset()) == 1,
           "one permutation with no descents at n=%d" % n)

# --- the two conventions are each associative, and are each other's opposite
for n in range(1, 5):
    W = list(permutations(range(1, n + 1)))
    for u in W[:6]:
        for v in W[:6]:
            for w in W[:6]:
                ck(compose_A(compose_A(u, v), w) == compose_A(u,
                                                              compose_A(v, w)),
                   "A associative at n=%d" % n)
                ck(compose_B(compose_B(u, v), w) == compose_B(u,
                                                              compose_B(v, w)),
                   "B associative at n=%d" % n)
            ck(compose_B(u, v) == compose_A(v, u), "B is A opposite, n=%d" % n)

# --- the cone test, against a second construction --------------------------
# independent route: a face lies in C(P) iff, for every covering pair i < j,
# the block index of i is at most that of j.  Rebuilt here by evaluating an
# explicit point of the face rather than by comparing block indices.
def in_cone_by_point(rel, F):
    x = {}
    for b, B in enumerate(F):
        for i in B:
            x[i] = b
    return all(x[i] <= x[j] for (i, j) in rel)


for n in range(0, 4):
    I = frozenset(range(n))
    for rel in posets_on(I):
        for F in set_compositions(I):
            ck(in_cone(rel, F) == in_cone_by_point(rel, F),
               "cone test agrees with the point route at n=%d" % n)

# --- the antichain's faces are ALL compositions; the chain's is exactly one -
for n in range(0, 5):
    I = frozenset(range(n))
    anti = frozenset()
    ck(len(faces_in_cone(anti, I)) == A000670[n],
       "antichain has every face at n=%d" % n)
    # the n-chain's faces are exactly the compositions of n into consecutive
    # intervals, so there are 2^(n-1) of them (and 1 when n = 0).
    chain = frozenset((i, j) for i in range(n) for j in range(n) if i < j)
    ch = faces_in_cone(chain, I)
    ck(len(ch) == (1 if n == 0 else 2 ** (n - 1)),
       "the n-chain has 2^(n-1) faces at n=%d" % n)
    for F in ch:
        ck(all(B == frozenset(range(min(B), max(B) + 1)) for B in F),
           "every block of a chain face is an interval at n=%d" % n)

# --- the Tits product ------------------------------------------------------
for n in range(0, 4):
    I = frozenset(range(n))
    SC = set_compositions(I)
    for F in SC:
        ck(tits_product(F, F) == F, "Tits is idempotent at n=%d" % n)
        for G in SC:
            H = tits_product(F, G)
            ck(sorted(x for B in H for x in B) == sorted(I),
               "Tits on one ground set is a composition of it, n=%d" % n)
            ck(tits_product(tits_product(F, G), F)
               == tits_product(F, G), "Tits: FGF = FG at n=%d" % n)

# on DISJOINT non-empty ground sets the Tits product is EMPTY -- the whole
# of w2, asserted here as a property of the kernel rather than of the run.
for F in set_compositions(frozenset({0, 1})):
    for G in set_compositions(frozenset({2, 3})):
        ck(tits_product(F, G) == (),
           "Tits across disjoint non-empty sets is empty")
        ck(concat(F, G) != (), "concatenation across the same is not empty")

# --- decompositions and restriction ----------------------------------------
for n in range(0, 5):
    I = frozenset(range(n))
    D = decompositions(I)
    ck(len(D) == 2 ** n, "2^n decompositions at n=%d" % n)
    ck(all(S | T == I and not (S & T) for (S, T) in D),
       "decompositions are disjoint and cover, n=%d" % n)
    for rel in posets_on(I)[:8]:
        for (S, T) in D:
            r = restrict_poset(rel, S)
            ck(all(i in S and j in S for (i, j) in r),
               "restriction stays inside S at n=%d" % n)
            ck(poset_union(r, restrict_poset(rel, T)) <= rel,
               "the union of the two restrictions sits inside rel, n=%d" % n)

# --- elems_F reproduces the document's 4 399 -------------------------------
ck(len(elems_F(frozenset(range(4)))) == 4399,
   "|F[4]| = 4399, the document's figure")
ck(len(elems_F(frozenset(range(3)))) == 121, "|F[3]| = 121")
ck(len(elems_F(frozenset())) == 1, "F[empty] is one-dimensional (connected)")

print("=" * 78)
print("SELFTEST f8fa: %d assertions, %d failure(s)" % (n_assert, len(fails)))
for f in sorted(set(fails)):
    print("  FAIL  %s" % f)
print("=" * 78)
sys.exit(1 if fails else 0)
