"""a4 — THE OPERATOR SIDE: identity (8), what kind of family this is, and the convex combination.

Three things, in the order they matter to the ticket's addendum:

  a4.1  identity (8) — "one BK edge maps to one local move at one scale" — verified exactly.
        It is the claim the note's own last paragraph calls the promising one.

  a4.2  IS THIS mg-8d66's FAMILY?  The ticket forbids applying mg-8d66 by analogy, and the
        answer measured here is that it MUST NOT be applied: the scale partition is a partition
        of BK edges by the LCA of the swapped ELEMENTS, not by word POSITION, and its fibers
        are NOT cubes.  mg-8d66's ceiling is a statement about cube foliations from
        non-adjacent position classes and does not reach this object.

  a4.3  THE CONVEX COMBINATION (the ticket's question 2).  Two different answers for the two
        different notes, because they are two different KINDS of family:
          - compression.tex's C_o, C_e are TRANSVERSE: a convex combination of them is NOT a
            projection, exactly as the ticket suspects.
          - compression2's scales are NESTED (a filtration): Var decomposes EXACTLY by scale,
            and a convex combination of the increments IS well defined and canonical — it is a
            multiplier, diagonal in the scale decomposition.

`lib8d66` is imported HERE ON PURPOSE, as a second implementation of the BK objects, and is the
only place in this instrument that reads a prior library.  a4.0 cross-checks it against mine.
"""
import sys
import os
from fractions import Fraction

HERE = __file__.rsplit("/", 1)[0]
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "compression_kfoliation_8d66"))
import lib0fc6 as L  # noqa: E402
import lib8d66 as K  # noqa: E402  — SECOND IMPLEMENTATION, imported deliberately

# ---------------------------------------------------------------- a4.0 cross-check

L.banner("a4.0  CROSS-CHECK against mg-8d66's independent library")
mismatch = 0
checked = 0
for n in (3, 4, 5):
    for lt in L.all_posets(n):
        mine = set(L.linear_extensions(n, lt))
        # lib8d66 represents the relation as a SET OF PAIRS where mine is a matrix; the
        # conversion is here so that the two really are independent implementations.
        theirs = set(K.linear_extensions(
            n, {(i, j) for i in range(n) for j in range(n) if lt[i][j]}))
        checked += 1
        if mine != theirs:
            mismatch += 1
L.verdict(mismatch == 0, "L(P) agrees with lib8d66 at every labelled poset n <= 5",
          f"{checked} posets, {mismatch} disagreements")

# ---------------------------------------------------------------- a4.1  identity (8)

L.banner("a4.1  (8)  one BK edge -> ONE word, changed by ONE adjacent AC <-> CA")
for n in (4, 6, 8):
    nodes = L.dyadic_nodes(n)
    bad_count = bad_shape = bad_lca = 0
    total = 0
    # at n = 6, 8 the antichain has 720 / 40320 extensions; the larger ones are represented by
    # posets with a few relations so the arm stays under a second without losing the structure.
    posets = L.all_posets(n) if n <= 4 else [
        L.tclose(n, [(i, i + 1) for i in range(0, n - 1, 2)]),
        L.tclose(n, [(0, 1), (1, 2)]),
        L.tclose(n, [(0, n - 1)])]
    for lt in posets:
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        star = LEs[0]
        for Lx in LEs:
            W = L.merge_words(Lx, star, nodes)
            for p in L.bk_edges(Lx, n, lt):
                total += 1
                Ly = L.swap(Lx, p)
                W2 = L.merge_words(Ly, star, nodes)
                diff = [i for i in range(len(nodes)) if W[i] != W2[i]]
                if len(diff) != 1:
                    bad_count += 1
                    continue
                i = diff[0]
                a, b = W[i], W2[i]
                # exactly one adjacent transposition, and it must be AC <-> CA
                d = [t for t in range(len(a)) if a[t] != b[t]]
                if len(d) != 2 or d[1] != d[0] + 1 or a[d[0]] == a[d[1]]:
                    bad_shape += 1
                if L.lca_node(Lx[p], Lx[p + 1], star, nodes) != nodes[i]:
                    bad_lca += 1
    L.verdict(bad_count == 0, f"n={n}: exactly ONE word changes", f"{total} BK edges")
    L.verdict(bad_shape == 0, f"n={n}: and it changes by ONE adjacent AC<->CA", f"{total} edges")
    L.verdict(bad_lca == 0, f"n={n}: and that node is the LCA of the swapped pair",
              f"{total} edges")

print()
print("       [finding] P4 CONFIRMED.  (8) is exact.  It is the note's sharpest claim and it")
print("                 survives contact with the definitions.")

# ---------------------------------------------------------------- a4.2  is it mg-8d66's family?

L.banner("a4.2  IS THE SCALE PARTITION AN ADMISSIBLE k-FOLIATION?  (it is not)")
n = 8
lt = L.antichain(n)
nodes = L.dyadic_nodes(n)
LEs = L.linear_extensions(n, lt)
star = tuple(range(n))
# (i) the scale label is NOT a function of the word POSITION
by_pos = {}
by_scale = {}
for Lx in LEs[:4000]:
    for p in L.bk_edges(Lx, n, lt):
        nd = L.lca_node(Lx[p], Lx[p + 1], star, nodes)
        lev = 0
        lo, mid, hi = nd
        size = hi - lo
        lev = {n: 0, n // 2: 1, n // 4: 2, n // 8: 3}.get(size, -1)
        by_pos.setdefault(p, set()).add(lev)
        by_scale.setdefault(lev, set()).add(p)
multi_pos = [p for p, s in by_pos.items() if len(s) > 1]
multi_scale = [s for s, ps in by_scale.items() if len(ps) > 1]
L.verdict(len(multi_pos) > 0,
          "the same POSITION carries edges of several SCALES — the partition is not by position",
          f"positions with >1 scale: {sorted(multi_pos)}")
L.verdict(len(multi_scale) > 0,
          "the same SCALE occurs at several POSITIONS",
          f"scales spread over positions: { {k: sorted(v) for k, v in by_scale.items()} }")

# (ii) the scale fibers are NOT cubes
sizes = {}
for Lx in LEs:
    W = L.merge_words(Lx, star, nodes)
    for i, nd in enumerate(nodes):
        key = (i, tuple(w for j, w in enumerate(W) if j != i))
        sizes.setdefault(key, 0)
        sizes[key] += 1
nonpow2 = [s for s in sizes.values() if s & (s - 1)]
L.verdict(len(nonpow2) > 0,
          "some scale fibers have NON-POWER-OF-2 size, so they are not cubes",
          f"{len(nonpow2)} of {len(sizes)} fibers; sizes seen: "
          f"{sorted(set(sizes.values()))[:8]}")
print()
print("       [finding] P9 CONFIRMED.  mg-8d66's ceiling is about partitions of the n-1 word")
print("                 POSITIONS into non-adjacent classes, whose fibers are cubes by")
print("                 construction.  This is a partition of EDGES by the LCA of the swapped")
print("                 ELEMENTS, and its fibers are monotone-path lattices (the note's own")
print("                 'median graph').  mg-8d66 DOES NOT apply to it and must not be quoted")
print("                 at it.")

# ---------------------------------------------------------------- a4.3  convex combinations


def cond_exp_matrix(LEs, blocks):
    """Conditional expectation onto the sigma-algebra generated by `blocks(L)`, as a matrix."""
    N = len(LEs)
    idx = {Lx: i for i, Lx in enumerate(LEs)}
    groups = {}
    for Lx in LEs:
        groups.setdefault(blocks(Lx), []).append(idx[Lx])
    M = [[Fraction(0)] * N for _ in range(N)]
    for g in groups.values():
        w = Fraction(1, len(g))
        for i in g:
            for j in g:
                M[i][j] = w
    return M


def matmul(A, B):
    N = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(N)) for j in range(N)] for i in range(N)]


def mateq(A, B):
    return all(A[i][j] == B[i][j] for i in range(len(A)) for j in range(len(A)))


def lincomb(mats, coeffs):
    N = len(mats[0])
    return [[sum(c * M[i][j] for c, M in zip(coeffs, mats)) for j in range(N)] for i in range(N)]


L.banner("a4.3a  compression.tex's C_o, C_e are TRANSVERSE: a convex combination is NOT a projection")
n = 5
found = 0
notproj = 0
for lt in L.all_posets(n)[:400]:
    LEs = L.linear_extensions(n, lt)
    if len(LEs) < 4:
        continue
    Po = cond_exp_matrix(LEs, lambda Lx: tuple(frozenset(Lx[i:i + 2]) for i in range(0, n - 1, 2)))
    Pe = cond_exp_matrix(LEs, lambda Lx: (Lx[0],) + tuple(frozenset(Lx[i:i + 2])
                                                          for i in range(1, n - 1, 2)))
    if mateq(Po, Pe):
        continue
    found += 1
    M = lincomb([Po, Pe], [Fraction(1, 2), Fraction(1, 2)])
    if not mateq(matmul(M, M), M):
        notproj += 1
    if found >= 40:
        break
L.verdict(found > 0 and notproj == found,
          "(Pi_o + Pi_e)/2 is NOT idempotent at every poset where the two differ",
          f"{notproj} of {found} posets")
print("       [answer to the ticket's question 2] CORRECT AS SUSPECTED, for compression.tex's")
print("       family.  A convex combination of transverse conditional expectations is a")
print("       self-adjoint operator with spectrum in [0,1], not a compression: there is no")
print("       sigma-algebra it is the conditional expectation of.  That is FINE if what is")
print("       wanted is the quadratic form — and note that the programme ALREADY uses exactly")
print("       this object: mg-8d66's kI - sum_i Pi_i is k(I - the equal-weight convex")
print("       combination), so 'combine compressions convexly' is not a new degree of freedom")
print("       on that family, it is the one already priced there.")

L.banner("a4.3b  compression2's scales are NESTED — a FILTRATION, and Var decomposes exactly")
n = 4
lt = L.antichain(n)
LEs = L.linear_extensions(n, lt)
star = LEs[0]
nodes = L.dyadic_nodes(n)
levels = {}
for nd in nodes:
    lo, mid, hi = nd
    levels.setdefault(hi - lo, []).append(nd)
order = sorted(levels.keys(), reverse=True)   # coarsest (root) first


def flag_upto(k):
    keep = [nd for sz in order[:k] for nd in levels[sz]]

    def f(Lx):
        return L.merge_words(Lx, star, keep)
    return f


Pis = [cond_exp_matrix(LEs, flag_upto(k)) for k in range(len(order) + 1)]
nested = all(mateq(matmul(Pis[a], Pis[b]), Pis[min(a, b)])
             for a in range(len(Pis)) for b in range(len(Pis)))
L.verdict(nested, "Pi_a Pi_b = Pi_min(a,b) — the family is a FILTRATION, not a transverse pair",
          f"{len(Pis)} levels at n={n}")
L.verdict(mateq(Pis[-1], [[Fraction(1) if i == j else Fraction(0) for j in range(len(LEs))]
                          for i in range(len(LEs))]),
          "the finest level is the IDENTITY — the encoding is lossless as an operator too")

# exact variance decomposition by scale
import random  # noqa: E402
random.seed(0)
worst = Fraction(0)
for trial in range(5):
    f = [Fraction(random.randint(-9, 9)) for _ in LEs]
    N = len(LEs)
    mean = sum(f) / N
    var = sum((x - mean) ** 2 for x in f) / N
    tot = Fraction(0)
    for k in range(len(Pis) - 1):
        g = [sum(Pis[k + 1][i][j] * f[j] for j in range(N)) for i in range(N)]
        h = [sum(Pis[k][i][j] * f[j] for j in range(N)) for i in range(N)]
        tot += sum((g[i] - h[i]) ** 2 for i in range(N)) / N
    worst = max(worst, abs(var - tot))
L.verdict(worst == 0, "Var(f) = sum over SCALES of the martingale increments, EXACTLY",
          f"5 random f, max |Var - sum| = {worst}")

# the convex combination on THIS family
incs = [lincomb([Pis[k + 1], Pis[k]], [Fraction(1), Fraction(-1)]) for k in range(len(Pis) - 1)]
lams = [Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)][:len(incs)]
while len(lams) < len(incs):
    lams.append(Fraction(0))
M = lincomb(incs, lams)
commutes = all(mateq(matmul(M, P), matmul(P, M)) for P in Pis)
L.verdict(commutes, "a weighted combination of the SCALE INCREMENTS commutes with every Pi_k",
          "it is a MULTIPLIER, diagonal in the scale decomposition")
L.verdict(not mateq(matmul(M, M), M),
          "it is still not idempotent unless every weight is 0 or 1 (as expected)")
print()
print("       [answer to the ticket's question 2, second half] ON compression2's FAMILY THE")
print("       CONVEX-COMBINATION STEP IS SOUND AND CANONICAL.  The increments are mutually")
print("       ORTHOGONAL projections, so sum_l lambda_l (Pi_{l+1} - Pi_l) is exactly a")
print("       Littlewood-Paley multiplier: it commutes with the filtration, its spectrum is")
print("       {lambda_l}, and Var splits across scales with no cross terms.  This is a REAL")
print("       structural difference from compression.tex's transverse pair, and it is the one")
print("       place Daniel's stated design is better than the objects the closed arc used.")

sys.exit(L.finish())
