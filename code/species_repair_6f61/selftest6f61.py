"""selftest6f61 -- the repair kernel, certified against things known in advance.

Nothing in r1/r2/r3 is worth reading if the kernel underneath is wrong, and
the kernel here is a THIRD implementation of objects two other directories
already build.  Agreement with them is the evidence; so the anchors below are
external -- OEIS sequences, closed forms, and small cases that can be checked
by hand -- rather than anything either predecessor computes.

  A000112  posets up to isomorphism            1, 1, 2, 5, 16, 63
  A001035  labelled posets                     1, 1, 3, 19, 219, 4231
  A000670  ordered set partitions (faces)      1, 1, 3, 13, 75, 541
  A000110  set partitions (flats)              1, 1, 2, 5, 15, 52
  A000142  |Aut(antichain on [n])| = n!        1, 1, 2, 6, 24, 120
"""

import sys

from kern6f61 import (AC_by_acyclicity, AC_by_support, aut_group, bits,
                      canonical, compositions_on, concat, faces_on,
                      is_lower_set, partitions_on, popcount, posets_on,
                      quotient_acyclic, restrict_face, restrict_part,
                      restrict_poset, submasks, supp, union_poset)

n_assert = 0


def eq(a, b, what):
    global n_assert
    n_assert += 1
    if a != b:
        print("SELFTEST FAILED: %s -- got %r, expected %r" % (what, a, b))
        sys.exit(1)


def true(a, what):
    eq(bool(a), True, what)


# ---- bitmask helpers --------------------------------------------------------
eq(bits(0b1011), [0, 1, 3], "bits")
eq(popcount(0b1011), 3, "popcount")
eq(len(submasks(0b1111)), 16, "submasks of a 4-set")
eq(submasks(0), [0], "submasks of the empty set")

# ---- posets -----------------------------------------------------------------
A001035 = [1, 1, 3, 19, 219]
A000112 = [1, 1, 2, 5, 16]
for n in range(0, 5):
    g = (1 << n) - 1
    Ps = posets_on(g, n)
    eq(len(Ps), A001035[n], "A001035 labelled posets at n=%d" % n)
    eq(len({canonical(P, g, n) for P in Ps}), A000112[n],
       "A000112 poset classes at n=%d" % n)

# the enumeration returns TRANSITIVELY CLOSED, IRREFLEXIVE relations only
for n in range(0, 5):
    g = (1 << n) - 1
    for P in posets_on(g, n):
        for i in range(n):
            true(not (P[i] >> i) & 1, "irreflexive")
            for j in bits(P[i]):
                for k in bits(P[j]):
                    true((P[i] >> k) & 1, "transitivity i<j<k => i<k")
                true(not (P[j] >> i) & 1, "antisymmetry")

# the 3-chain has exactly 1 automorphism, the 3-antichain exactly 6
g3 = 0b111
chain3 = None
anti3 = None
for P in posets_on(g3, 3):
    r = sum(popcount(u) for u in P)
    if r == 3:
        chain3 = P
    if r == 0:
        anti3 = P
eq(len(aut_group(chain3, g3, 3)), 1, "|Aut(3-chain)| = 1")
eq(len(aut_group(anti3, g3, 3)), 6, "|Aut(3-antichain)| = 3!")
for n in range(1, 5):
    g = (1 << n) - 1
    fact = 1
    for k in range(2, n + 1):
        fact *= k
    eq(len(aut_group(tuple([0] * n), g, n)), fact,
       "A000142 |Aut(antichain)| at n=%d" % n)

# ---- faces and flats --------------------------------------------------------
A000670 = [1, 1, 3, 13, 75, 541]
A000110 = [1, 1, 2, 5, 15, 52]
for n in range(0, 6):
    g = (1 << n) - 1
    eq(len(compositions_on(g)), A000670[n], "A000670 faces at n=%d" % n)
    eq(len(partitions_on(g)), A000110[n], "A000110 flats at n=%d" % n)

# every composition is a disjoint cover of its ground set, in block order
for n in range(0, 5):
    g = (1 << n) - 1
    for F in compositions_on(g):
        seen = 0
        for B in F:
            true(B != 0, "no empty block")
            eq(B & seen, 0, "blocks disjoint")
            seen |= B
        eq(seen, g, "blocks cover the ground set")

# the ANTICHAIN's faces are all compositions; the CHAIN's are exactly one
for n in range(0, 5):
    g = (1 << n) - 1
    eq(len(faces_on(tuple([0] * n), g)), A000670[n],
       "antichain: every composition is a face, n=%d" % n)
ch = [0] * 4
for i in range(4):
    for j in range(i + 1, 4):
        ch[i] |= 1 << j
eq(len(faces_on(tuple(ch), 0b1111)), 8,
   "the 4-chain's faces are its 2^(n-1) interval compositions")

# ---- AC(P), by two routes, on every poset to n <= 4 -------------------------
for n in range(0, 5):
    g = (1 << n) - 1
    pi = set(partitions_on(g))
    for P in posets_on(g, n):
        a1 = AC_by_support(P, g)
        a2 = AC_by_acyclicity(P, g)
        eq(a1, a2, "AC by support == AC by acyclicity")
        true(a1 <= pi, "AC(P) is a set of partitions of the ground set")
    eq(AC_by_support(tuple([0] * n), g), pi,
       "AC(antichain) = Pi[n] at n=%d" % n)

# the 3-chain loses exactly {a,c}|{b}, and nothing else
lost = set(partitions_on(g3)) - AC_by_support(chain3, g3)
eq(len(lost), 1, "the 3-chain loses exactly one partition")
eq(sorted(sorted(popcount(B) for B in X) for X in lost), [[1, 2]],
   "and it has block sizes {2,1}")
true(not quotient_acyclic(chain3, list(lost)[0], g3),
     "that partition's quotient really does have a cycle")

# ---- the operations ---------------------------------------------------------
eq(concat(((1,), (2,))[0:1], ((4,),)), ((1,), (4,)), "concat")
eq(restrict_face(((0b0011), (0b1100)), 0b0101), (0b0001, 0b0100),
   "restrict_face drops empty blocks")
eq(restrict_part(frozenset([0b0011, 0b1100]), 0b0001), frozenset([0b0001]),
   "restrict_part")
eq(restrict_poset(tuple([0b1110, 0, 0, 0]), 0b0011, 4), (0b0010, 0, 0, 0),
   "restrict_poset")
true(is_lower_set(tuple([0b0010, 0, 0, 0]), 0b0001, 4),
     "{0} is a lower set of 0<1")
true(not is_lower_set(tuple([0b0010, 0, 0, 0]), 0b0010, 4),
     "{1} is not a lower set of 0<1")
eq(union_poset((1, 0, 0, 0), (0, 0, 8, 0), 4), (1, 0, 8, 0), "union_poset")

print("selftest6f61 OK -- %d assertions" % n_assert)
sys.exit(0)
