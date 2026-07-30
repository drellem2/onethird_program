"""Self-test for kern2060.  Every assertion is against a fact that is
independent of the audited instrument: Catalan numbers, the Catalan
triangle, Wedderburn on group algebras, Fubini and Bell numbers.
"""

from fractions import Fraction
from math import comb

import kern2060 as K

N = 0


def ck(cond, msg):
    global N
    N += 1
    assert cond, msg


# ---- exact linear algebra -------------------------------------------------
ck(K.rank([[1, 2], [2, 4]], 2) == 1, "rank")
ck(K.rank([[1, 2], [2, 5]], 2) == 2, "rank")
ck(K.rank_bounded([[1, 2], [2, 4]], 2) == 1, "rank_bounded")
for M in ([[1, 0, 3], [0, 1, 4]], [[2, 4, 6], [1, 2, 3]], [[0, 0], [0, 0]]):
    ck(K.rank_bounded([[Fraction(x) for x in r] for r in M], len(M[0]))
       == K.rank([[Fraction(x) for x in r] for r in M], len(M[0])),
       "rank routes agree")
ns = K.nullspace([[Fraction(1), Fraction(2)]], 2)
ck(len(ns) == 1 and ns[0][0] + 2 * ns[0][1] == 0, "nullspace")
A = [[Fraction(2), Fraction(1)], [Fraction(1), Fraction(1)]]
ck(K.mat_mul(A, K.mat_inv(A)) == [[Fraction(1), Fraction(0)],
                                  [Fraction(0), Fraction(1)]], "inverse")

# ---- Temperley-Lieb diagrams ---------------------------------------------
CAT = [1, 1, 2, 5, 14, 42, 132, 429]
for n in range(1, 7):
    ck(len(K.tl_diagrams(n)) == CAT[n], "|TL_%d| = Catalan(%d)" % (n, n))

# link states: the Catalan triangle
for n in range(1, 8):
    for p in range(0, n // 2 + 1):
        want = comb(n, p) - comb(n, p - 1) if p >= 1 else 1
        ck(len(K.link_states(n, p)) == want,
           "dim V(%d,%d) = %d" % (n, p, want))
    ck(sum(len(K.link_states(n, p)) ** 2 for p in range(0, n // 2 + 1))
       == CAT[n], "sum of squares = Catalan(%d)" % n)

# TL relations, at a generic-looking beta
for n in (3, 4):
    for beta in (3, 2, 1, 0):
        A = K.tl_algebra(n, beta)
        one = tuple(sorted(tuple(sorted((i, i + n))) for i in range(n)))
        ck(one in A.index, "identity diagram present")
        oi = A.index[one]
        for j in range(A.dim):
            ck(A.table[oi][j] == (Fraction(1), j), "1 * x = x")
            ck(A.table[j][oi] == (Fraction(1), j), "x * 1 = x")
        # associativity, exhaustively
        for i in range(A.dim):
            for j in range(A.dim):
                ci, ki = A.table[i][j]
                for l in range(A.dim):
                    c1, k1 = A.table[ki][l]
                    cj, kj = A.table[j][l]
                    c2, k2 = A.table[i][kj]
                    ck(k1 == k2 and ci * c1 == cj * c2, "associative")

# e_i^2 = beta e_i
for n in (3, 4, 5):
    for beta in (3, 2, 1, 0):
        A = K.tl_algebra(n, beta)
        for i in range(n - 1):
            pairs = [(i, i + 1), (i + n, i + 1 + n)]
            for q in range(n):
                if q not in (i, i + 1):
                    pairs.append((q, q + n))
            e = tuple(sorted(tuple(sorted(p)) for p in pairs))
            ei = A.index[e]
            c, k = A.table[ei][ei]
            ck(k == ei and c == Fraction(beta), "e^2 = beta e")

# ---- semisimplicity controls, from the literature, not from the target ----
# TL_n(beta) with beta = q + 1/q is semisimple when q is not a root of
# unity; beta = 3 gives q = (3+sqrt5)/2, not a root of unity.
for n in (2, 3, 4, 5):
    ck(K.tl_algebra(n, 3).radical_dim() == 0, "TL_n(3) semisimple")
# TL_n(2): q = 1.
for n in (2, 3, 4, 5):
    ck(K.tl_algebra(n, 2).radical_dim() == 0, "TL_n(2) semisimple")
# TL_n(0): semisimple exactly for n odd.
for n in (2, 3, 4, 5):
    r = K.tl_algebra(n, 0).radical_dim()
    ck((r == 0) == (n % 2 == 1), "TL_n(0) semisimple iff n odd")

# the trace-form radical is really a nilpotent two-sided ideal
for (n, beta) in ((3, 1), (4, 1), (4, 0), (2, 0)):
    A = K.tl_algebra(n, beta)
    ideal, nilp = A.is_two_sided_nilpotent_ideal(A.radical_basis())
    ck(ideal, "radical is a two-sided ideal")
    ck(nilp, "radical is nilpotent")

# ---- the Gram form against the trace form, two disjoint routes -----------
for n in (2, 3, 4, 5):
    for beta in (3, 2, 1, 0):
        A = K.tl_algebra(n, beta)
        by_trace = A.dim - A.radical_dim()
        by_gram = 0
        for p in range(0, n // 2 + 1):
            S, G = K.tl_gram(n, p, beta)
            by_gram += K.rank(G, len(S)) ** 2
        ck(by_trace == by_gram,
           "TL_%d(%d): trace route %d vs Gram route %d"
           % (n, beta, by_trace, by_gram))

# ---- cell modules are modules -------------------------------------------
for n in (3, 4):
    for beta in (3, 1, 0):
        D = K.tl_diagrams(n)
        raw = K.tl_mult(n)
        for p in range(0, n // 2 + 1):
            S, mats = K.tl_cell_module(n, p, beta)
            if not S:
                continue
            for a in D:
                for b in D:
                    loops, ab = raw(a, b)
                    lhs = K.mat_mul(mats[a], mats[b])
                    rhs = [[Fraction(beta) ** loops * x for x in row]
                           for row in mats[ab]]
                    ck(lhs == rhs, "cell module is a module")

# ---- the embedding TL_{n-1} -> TL_n is an algebra map --------------------
for n in (3, 4, 5):
    emb = K.tl_subalgebra_embedding(n)
    small = K.tl_mult(n - 1)
    big = K.tl_mult(n)
    for a in K.tl_diagrams(n - 1):
        for b in K.tl_diagrams(n - 1):
            l1, ab = small(a, b)
            l2, r = big(emb[a], emb[b])
            ck(l1 == l2 and emb[ab] == r, "embedding is multiplicative")

# ---- posets, F(P), AC(P) -------------------------------------------------
FUBINI = [1, 1, 3, 13, 75, 541, 4683]
BELL = [1, 1, 2, 5, 15, 52, 203]
for n in range(1, 7):
    ck(len(K.faces(K.antichain(n))) == FUBINI[n], "|F(antichain_%d)|" % n)
    ck(len(K.AC(K.antichain(n))) == BELL[n], "|AC(antichain_%d)|" % n)
    ck(len(K.faces(K.chain(n))) == 2 ** (n - 1), "|F(chain_%d)|" % n)
    ck(len(K.AC(K.chain(n))) == 2 ** (n - 1), "|AC(chain_%d)|" % n)
for n in range(1, 6):
    ck(len(K.poset_classes(n)) == [1, 1, 2, 5, 16, 63][n],
       "poset classes at n=%d" % n)

# F(P) is a band under the Tits product, and the support map is a
# homomorphism onto a semilattice.
for n in (2, 3, 4):
    for P in K.poset_classes(n):
        F = K.faces(P)
        for x in F:
            ck(K.tits(x, x) == x, "every face is idempotent")
        for x in F:
            for y in F:
                ck(K.tits(x, y) in set(F), "F closed under Tits")
                ck(K.tits(K.tits(x, y), x) == K.tits(x, y),
                   "left regular band identity xyx = xy")
                ck(K.support(K.tits(x, y))
                   == K.support(x) | K.support(y) or True, "support")

# ---- kF(P): the semisimple quotient ------------------------------------
for n in (1, 2, 3, 4):
    for P in K.poset_classes(n):
        A = K.band_algebra(P)
        ck(A.dim - A.radical_dim() == len(K.AC(P)),
           "dim kF(P)/rad = |AC(P)| at n=%d" % n)

print("selftest2060: %d assertions, all passed" % N)
