"""Self-test for kern_d330.  Every assertion is counted and the count is
printed, so "all passed" has a population beside it.

Nothing here reads the target.  It checks that this audit's own kernel is
right before the kernel is used to check anything else.
"""

import random
import sys
from fractions import Fraction

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from kern_d330 import (binom, half_diagrams, _noncrossing_matchings, pairing,
                       gram, rank, vertex_set, dims_render, pairs_render,
                       cell_dims)

N = 0
BAD = 0


def ok(cond, msg):
    global N, BAD
    N += 1
    if not cond:
        BAD += 1
        print("  BAD: " + msg)


def catalan(n):
    return binom(2 * n, n) // (n + 1)


print("=" * 74)
print("SELFTEST  kern_d330 --- mg-d330's own kernel, before it is used")
print("=" * 74)

# --- non-crossing matchings -------------------------------------------------
for k in range(0, 6):
    ms = _noncrossing_matchings(list(range(2 * k)))
    ok(len(ms) == catalan(k),
       "non-crossing perfect matchings of %d points: %d, Catalan says %d"
       % (2 * k, len(ms), catalan(k)))
    for m in ms:
        ok(sorted(x for pr in m for x in pr) == list(range(2 * k)),
           "a matching is not a partition of the points")
        ok(not any(i < a < j < b for (i, j) in m for (a, b) in m),
           "a matching crosses")

# --- half-diagram counts ----------------------------------------------------
for n in range(1, 9):
    for p in range(n // 2 + 1):
        hd = half_diagrams(n, p)
        want = binom(n, p) - binom(n, p - 1)
        ok(len(hd) == want,
           "half-diagrams on %d points with %d arcs: %d, formula says %d"
           % (n, p, len(hd), want))
        for (arcs, defs) in hd:
            ok(len(arcs) == p, "wrong arc count")
            ok(len(defs) == n - 2 * p, "wrong defect count")
            ok(not any(i < d < j for (i, j) in arcs for d in defs),
               "an arc encloses a defect")
    ok(sum(d * d for d in cell_dims(n)) == catalan(n),
       "sum of squares of the cell dimensions at n=%d is not Catalan(%d)" % (n, n))

# --- the form ---------------------------------------------------------------
for n in range(1, 7):
    for p in range(n // 2 + 1):
        for beta in (3, 2, 1, 0):
            g = gram(n, p, beta)
            ok(all(g[i][j] == g[j][i] for i in range(len(g))
                   for j in range(len(g))),
               "the Gram matrix at (%d,%d,%d) is not symmetric" % (n, p, beta))
            # REMOVED DURING CONSTRUCTION and replaced: the first version of
            # this assertion was written `... or True`, which cannot fail.  A
            # checker that cannot fire is the defect this whole arc is about,
            # and it would have been counted in the assertion total.  The real
            # statement is that every entry is 0 or a non-negative power of
            # beta, which is what the form's definition allows.
            powers = {Fraction(beta) ** k for k in range(n + 1)}
            ok(all(x == 0 or x in powers for row in g for x in row),
               "a Gram entry at (%d,%d,%d) is neither 0 nor a power of beta"
               % (n, p, beta))
            r = rank(g)
            ok(0 <= r <= len(g),
               "rank out of range at (%d,%d,%d)" % (n, p, beta))

# --- rank against a brute-force determinant route ---------------------------
def det(m):
    m = [row[:] for row in m]
    k = len(m)
    d = Fraction(1)
    for c in range(k):
        piv = next((i for i in range(c, k) if m[i][c] != 0), None)
        if piv is None:
            return Fraction(0)
        if piv != c:
            m[c], m[piv] = m[piv], m[c]
            d = -d
        d *= m[c][c]
        inv = Fraction(1) / m[c][c]
        for i in range(c + 1, k):
            f = m[i][c] * inv
            m[i] = [a - f * b for (a, b) in zip(m[i], m[c])]
    return d


rng = random.Random(20260730)
for _ in range(60):
    k = rng.randint(1, 4)
    m = [[Fraction(rng.randint(-3, 3)) for _ in range(k)] for _ in range(k)]
    full = det(m) != 0
    ok((rank(m) == k) == full,
       "rank disagrees with the determinant on a %dx%d matrix" % (k, k))

# --- semisimplicity at the generic parameter --------------------------------
for n in range(1, 7):
    vs = vertex_set(n, 3)
    ok([d for (p, d) in vs] == cell_dims(n),
       "at beta = 3 the tower is semisimple, so dim L must equal dim V at n=%d"
       % n)
    ok([p for (p, d) in vs] == list(range(len(vs))),
       "the live labels at beta = 3, n = %d are not a run from 0" % n)

# --- the renderings ---------------------------------------------------------
ok(dims_render(((0, 1), (1, 1))) == dims_render(((0, 1), (2, 1))),
   "the dimensions-only rendering must NOT separate a gapped label set from "
   "an ungapped one --- that is the whole point of e1 (iv)")
ok(pairs_render(((0, 1), (1, 1))) != pairs_render(((0, 1), (2, 1))),
   "the labelled rendering must separate them")
ok(len(((0, 1), (1, 1))) == len(((0, 1), (2, 1))),
   "and a count must not separate them either")
for a in [((0, 1),), ((0, 1), (1, 2)), ((0, 1), (1, 4), (2, 5))]:
    ok(dims_render(a) == "[" + ",".join(str(d) for (_, d) in a) + "]",
       "dims_render is not the dimensions, p ascending")

print()
print("selftest: %d assertions, %d bad" % (N, BAD))
print("TOTAL BAD: %d" % BAD)
sys.exit(1 if BAD else 0)
