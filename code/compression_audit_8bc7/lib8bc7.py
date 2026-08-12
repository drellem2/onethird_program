"""lib8bc7 -- independent instrument for the mg-8bc7 audit of docs/imports/compression.tex.

Imports NOTHING from this repository.  The whole point of the audit is an independent
derivation of the note's claims; reusing the corpus's poset / linear-extension code would
make agreement a second reading of one implementation rather than a check.  Standard
library only (fractions, itertools) -- this host has no numpy, so every eigenvalue in the
measurement arms is computed by the Jacobi routine at the bottom of this file, and every
VERDICT is decided in exact rational arithmetic with no float on its path.

Conventions, fixed once here so the arms cannot drift:

  * A poset on n elements is carried as `lt`, a frozenset of ordered pairs (i, j) meaning
    i <_P j, transitively closed and antisymmetric.  Elements are the integers 0..n-1.
  * A linear extension L is a tuple (L[0], ..., L[n-1]) of elements, position-indexed
    from 0.  The note writes L = (x_1, ..., x_n), 1-indexed; the translation is
    x_k = L[k-1], and the note's tau_i (swapping positions i, i+1) is `swap_at(L, i-1)`.
  * I(P) is the set of incomparable pairs (x, y) with x < y as integer labels.  A
    pair-orientation linear statistic is f(L) = a + sum_{(x,y) in I(P)} c[(x,y)]
    * 1{x <_L y}, exactly the note's section 2 form with the canonical orientation.
"""

from fractions import Fraction
from itertools import combinations, product
import math
import random

# --------------------------------------------------------------------------------------
# posets
# --------------------------------------------------------------------------------------


def transitive_closure(n, pairs):
    """Floyd-Warshall closure of a strict relation.  Returns a set of (i, j)."""
    rel = set(pairs)
    for k in range(n):
        for i in range(n):
            if (i, k) in rel:
                for j in range(n):
                    if (k, j) in rel:
                        rel.add((i, j))
    return rel


def is_strict_order(n, rel):
    """Irreflexive, antisymmetric, transitive."""
    for (i, j) in rel:
        if i == j or (j, i) in rel:
            return False
    for (i, j) in rel:
        for (k, l) in rel:
            if j == k and (i, l) not in rel:
                return False
    return True


def gen_posets_exhaustive(n):
    """Every labeled poset on 0..n-1, as a frozenset of strict relations.

    Enumerates all 3^C(n,2) assignments of {<, >, incomparable} to unordered pairs and
    keeps the transitive ones.  Practical to n = 5 (3^10 = 59049 candidates).
    """
    pairs = list(combinations(range(n), 2))
    for choice in product((0, 1, 2), repeat=len(pairs)):
        rel = set()
        for (a, b), c in zip(pairs, choice):
            if c == 1:
                rel.add((a, b))
            elif c == 2:
                rel.add((b, a))
        if is_strict_order(n, rel):
            yield frozenset(rel)


def random_poset(n, p, rng):
    """A random labeled poset: relate i<j (in a random ground permutation) w.p. p, close."""
    perm = list(range(n))
    rng.shuffle(perm)
    pairs = []
    for a in range(n):
        for b in range(a + 1, n):
            if rng.random() < p:
                pairs.append((perm[a], perm[b]))
    return frozenset(transitive_closure(n, pairs))


def dual(n, lt):
    """P^op -- every relation reversed."""
    return frozenset((j, i) for (i, j) in lt)


def incomparable_pairs(n, lt):
    """I(P): unordered incomparable pairs, carried as (x, y) with x < y as labels."""
    return [(x, y) for x, y in combinations(range(n), 2)
            if (x, y) not in lt and (y, x) not in lt]


# --------------------------------------------------------------------------------------
# linear extensions and the BK adjacent-transposition graph
# --------------------------------------------------------------------------------------


def linear_extensions(n, lt):
    preds = [set() for _ in range(n)]
    for (i, j) in lt:
        preds[j].add(i)
    out = []
    placed = set()
    seq = []

    def rec():
        if len(seq) == n:
            out.append(tuple(seq))
            return
        for v in range(n):
            if v not in placed and preds[v] <= placed:
                placed.add(v)
                seq.append(v)
                rec()
                seq.pop()
                placed.discard(v)

    rec()
    return out


def swap_at(L, i):
    """tau_{i+1} in the note's 1-indexed naming: swap positions i, i+1 of L."""
    M = list(L)
    M[i], M[i + 1] = M[i + 1], M[i]
    return tuple(M)


def legal_at(L, i, lt):
    """The swap at positions (i, i+1) is legal iff those two elements are incomparable."""
    a, b = L[i], L[i + 1]
    return (a, b) not in lt and (b, a) not in lt


# --------------------------------------------------------------------------------------
# the two compressions
# --------------------------------------------------------------------------------------


def groups_o(n):
    """Position groups of C_o = (I_2, I_4, ...): {p0,p1}, {p2,p3}, ..., trailing singleton
    iff n is odd.  Swaps inside these groups sit at the note's odd positions 1, 3, 5, ..."""
    g = [(2 * j, 2 * j + 1) for j in range(n // 2)]
    if n % 2 == 1:
        g.append((n - 1,))
    return g


def groups_e(n):
    """Position groups of C_e = (I_1, I_3, ...): leading singleton {p0}, then {p1,p2},
    {p3,p4}, ..., trailing singleton iff n is even.  Swaps sit at positions 2, 4, ..."""
    g = [(0,)] + [(2 * j + 1, 2 * j + 2) for j in range((n - 1) // 2)]
    if n % 2 == 0 and n >= 2:
        g.append((n - 1,))
    return g


def swap_positions(groups):
    """0-indexed left positions of the swaps that live inside these groups."""
    return [g[0] for g in groups if len(g) == 2]


def fiber_key(L, groups):
    """The compressed state: each group as an unordered set, in order."""
    return tuple(tuple(sorted(L[p] for p in g)) for g in groups)


def fibers(LEs, groups):
    """dict: compressed state -> list of linear extensions above it."""
    out = {}
    for L in LEs:
        out.setdefault(fiber_key(L, groups), []).append(L)
    return out


# --------------------------------------------------------------------------------------
# functions on L(P)
# --------------------------------------------------------------------------------------


def linear_stat(n, lt, a, c, LEs):
    """Evaluate a pair-orientation linear statistic at every LE.  Returns a list of
    Fractions aligned with LEs.  `c` maps (x, y) in I(P) -> Fraction."""
    vals = []
    for L in LEs:
        pos = [0] * n
        for k, v in enumerate(L):
            pos[v] = k
        t = a
        for (x, y), cxy in c.items():
            if pos[x] < pos[y]:
                t += cxy
        vals.append(t)
    return vals


def random_c(pairs, rng, lo=-6, hi=6):
    return {p: Fraction(rng.randint(lo, hi), rng.randint(1, 4)) for p in pairs}


def cond_expectation(vals, LEs, groups):
    """Pi f = E[f | C].  Returns a list aligned with LEs."""
    idx = {L: k for k, L in enumerate(LEs)}
    out = [None] * len(LEs)
    for key, fib in fibers(LEs, groups).items():
        m = sum(vals[idx[L]] for L in fib) / Fraction(len(fib))
        for L in fib:
            out[idx[L]] = m
    return out


def expected_cond_variance(vals, LEs, groups):
    """E Var(f | C) = <f, (I - Pi) f> under the uniform measure, exactly."""
    idx = {L: k for k, L in enumerate(LEs)}
    N = len(LEs)
    tot = Fraction(0)
    for key, fib in fibers(LEs, groups).items():
        m = sum(vals[idx[L]] for L in fib) / Fraction(len(fib))
        v = sum((vals[idx[L]] - m) ** 2 for L in fib) / Fraction(len(fib))
        tot += Fraction(len(fib), N) * v
    return tot


def variance(vals):
    N = len(vals)
    m = sum(vals) / Fraction(N)
    return sum((v - m) ** 2 for v in vals) / Fraction(N)


def bk_energy(vals, LEs, n, lt, positions=None):
    """Dirichlet form of the BK chain P = (1/(n-1)) sum_i tau_i (tau_i = identity when the
    swap is illegal), i.e. <f, (I - P) f> under uniform pi:

        E(f) = 1/(2(n-1)N) * sum_L sum_i (f(tau_i L) - f(L))^2.

    `positions` restricts the inner sum to a subset of the n-1 adjacent positions, which is
    how E_o and E_e are read off; the 1/(n-1) normalization is NOT rescaled when it is,
    because the note's chain always draws from all n-1 positions.
    """
    idx = {L: k for k, L in enumerate(LEs)}
    N = len(LEs)
    if positions is None:
        positions = range(n - 1)
    tot = Fraction(0)
    for L in LEs:
        fL = vals[idx[L]]
        for i in positions:
            if legal_at(L, i, lt):
                tot += (vals[idx[swap_at(L, i)]] - fL) ** 2
    return tot / Fraction(2 * (n - 1) * N)


def bk_apply(vals, LEs, n, lt):
    """(I - P_BK) f, pointwise."""
    idx = {L: k for k, L in enumerate(LEs)}
    out = []
    for L in LEs:
        fL = vals[idx[L]]
        s = Fraction(0)
        for i in range(n - 1):
            M = swap_at(L, i) if legal_at(L, i, lt) else L
            s += vals[idx[M]] - fL
        out.append(-s / Fraction(n - 1))
    return out


# --------------------------------------------------------------------------------------
# exact linear algebra (verdict paths only)
# --------------------------------------------------------------------------------------


def in_span(basis, target):
    """Is `target` in the span of `basis` (lists of Fractions of equal length)?

    Exact Gaussian elimination.  Returns True/False.
    """
    rows = [list(b) for b in basis]
    tgt = list(target)
    m = len(tgt)
    piv_cols = []
    r = 0
    for col in range(m):
        p = None
        for k in range(r, len(rows)):
            if rows[k][col] != 0:
                p = k
                break
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        pv = rows[r][col]
        rows[r] = [x / pv for x in rows[r]]
        for k in range(len(rows)):
            if k != r and rows[k][col] != 0:
                f = rows[k][col]
                rows[k] = [x - f * y for x, y in zip(rows[k], rows[r])]
        piv_cols.append(col)
        r += 1
        if r == len(rows):
            break
    for row, col in zip(rows, piv_cols):
        if tgt[col] != 0:
            f = tgt[col]
            tgt = [x - f * y for x, y in zip(tgt, row)]
    return all(x == 0 for x in tgt)


def psd_exact(A):
    """Is the symmetric rational matrix A positive semidefinite?

    Exact symmetric (Schur-complement) reduction: A is PSD iff at every step the pivot is
    > 0 and the Schur complement is PSD, or the pivot is 0 and its whole row vanishes.
    No float touches this, so it can carry a verdict.
    """
    M = [[Fraction(x) for x in row] for row in A]
    n = len(M)
    for k in range(n):
        d = M[k][k]
        if d < 0:
            return False
        if d == 0:
            # Only the REMAINING submatrix may be inspected: columns < k have already been
            # eliminated in the rows but not in the (symmetric) rows above, so scanning the
            # full row reports a spurious non-PSD.  Caught by a0.3's rank-1 case (D1).
            for j in range(k, n):
                if M[k][j] != 0 or M[j][k] != 0:
                    return False
            continue
        for i in range(k + 1, n):
            if M[i][k] != 0:
                f = M[i][k] / d
                for j in range(k + 1, n):
                    M[i][j] -= f * M[k][j]
                M[i][k] = Fraction(0)
    return True


# --------------------------------------------------------------------------------------
# float eigenvalues (MEASUREMENT paths only -- never a verdict)
# --------------------------------------------------------------------------------------


def jacobi_eigenvalues(A, sweeps=100, tol=1e-13):
    """Eigenvalues of a symmetric float matrix by cyclic Jacobi.  Returns sorted list."""
    n = len(A)
    a = [[float(A[i][j]) for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = math.sqrt(sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j))
        if off < tol:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-18:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = (1 if theta >= 0 else -1) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p] = c * akp - s * akq
                    a[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k] = c * apk - s * aqk
                    a[q][k] = s * apk + c * aqk
    return sorted(a[i][i] for i in range(n))


def cholesky(B):
    """Lower-triangular Cholesky of a float SPD matrix, or None if it is not SPD."""
    n = len(B)
    Lm = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = B[i][j] - sum(Lm[i][k] * Lm[j][k] for k in range(j))
            if i == j:
                if s <= 1e-12:
                    return None
                Lm[i][i] = math.sqrt(s)
            else:
                Lm[i][j] = s / Lm[j][j]
    return Lm


def gen_eig_min(A, B):
    """Smallest generalized eigenvalue of A v = lam B v for symmetric A, SPD B (floats)."""
    Lm = cholesky(B)
    if Lm is None:
        return None
    n = len(A)
    # solve L Y = A  then  L Z^T = Y^T  giving Z = L^-1 A L^-T
    Y = [[0.0] * n for _ in range(n)]
    for j in range(n):
        for i in range(n):
            Y[i][j] = (A[i][j] - sum(Lm[i][k] * Y[k][j] for k in range(i))) / Lm[i][i]
    Z = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            Z[i][j] = (Y[i][j] - sum(Z[i][k] * Lm[j][k] for k in range(j))) / Lm[j][j]
    S = [[(Z[i][j] + Z[j][i]) / 2 for j in range(n)] for i in range(n)]
    return jacobi_eigenvalues(S)


# --------------------------------------------------------------------------------------
# reporting helpers
# --------------------------------------------------------------------------------------


def banner(title):
    print("=" * 86)
    print(title)
    print("=" * 86)


def verdict(ok, label, extra=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}{(' -- ' + extra) if extra else ''}")
    return ok
