"""lib145f -- mg-145f's instrument for the CONSUMER ENUMERATION of the cube-foliation
energy identity (docs/imports/compression.tex sections 1-3).

WHAT THIS FILE IS FOR, stated first because it decides what is and is not a verdict here.
mg-145f asks whether ANY target in this programme can be fed by the identity

    E Var(f | C_o) = (1/4) sum_{j in D(C_o)} c_{B_j}^2        (compression.tex :95-100)
    E_BK(f)        = (2/(n-1)) ( E Var(f|C_o) + E Var(f|C_e) )    (:145, "(*)")

for f a pair-orientation linear statistic.  Answering that needs the identity's OUTPUT MAP
pinned exactly -- what function of the linear-extension measure the identity actually emits --
because "reachable by the machinery" is otherwise a matter of taste.  Everything on a verdict
path in this file is exact rational arithmetic.

INDEPENDENCE.  Posets, linear extensions, the two block systems, the fibers, the conditional
variances, the BK Dirichlet form and the adjacency probabilities are all built here from
scratch.  `lib409a` (mg-409a's W4 instrument) is imported by ONE arm, e0, and ONLY as a
cross-check of this file's constructions against a second implementation.  No verdict in
e1..e5 routes through it.  Same discipline mg-409a applied to `lib8bc7`, and for the same
reason: mg-409a's own D5 records that sharing one library makes downstream arms non-
independent witnesses of each other.

NO FLOAT ANYWHERE.  Unlike mg-409a this file has no eigenvalue path at all: nothing here needs
one.  Every number printed is a Fraction or an integer.
"""

from fractions import Fraction
from itertools import combinations, product

# --------------------------------------------------------------------------------------
# posets -- built from the axioms, not imported
# --------------------------------------------------------------------------------------


def transitive_closure(pairs):
    rel = set(pairs)
    changed = True
    while changed:
        changed = False
        for (a, b) in list(rel):
            for (c, d) in list(rel):
                if b == c and (a, d) not in rel:
                    rel.add((a, d))
                    changed = True
    return frozenset(rel)


def is_strict_order(rel):
    for (a, b) in rel:
        if a == b or (b, a) in rel:
            return False
    for (a, b) in rel:
        for (c, d) in rel:
            if b == c and (a, d) not in rel:
                return False
    return True


def all_posets(n):
    """Every labelled poset on 0..n-1.  3^C(n,2) candidates; practical to n = 5."""
    prs = list(combinations(range(n), 2))
    for choice in product((0, 1, 2), repeat=len(prs)):
        rel = set()
        for (a, b), c in zip(prs, choice):
            if c == 1:
                rel.add((a, b))
            elif c == 2:
                rel.add((b, a))
        cl = transitive_closure(rel)
        if cl == frozenset(rel) and is_strict_order(cl):
            yield cl


def _lcg(seed):
    s = seed & 0xFFFFFFFF
    while True:
        s = (1103515245 * s + 12345) & 0x7FFFFFFF
        yield s


def sample_posets(n, k, seed):
    """k random labelled posets on n elements, deterministic, no `random` import.

    Draws a random tournament-free orientation of a random subset of pairs and closes it;
    keeps it only if the closure adds nothing (so the drawn relation IS the poset).
    """
    prs = list(combinations(range(n), 2))
    gen = _lcg(seed)
    out, seen, tries = [], set(), 0
    while len(out) < k and tries < 400 * k:
        tries += 1
        rel = set()
        for (a, b) in prs:
            r = next(gen) % 3
            if r == 1:
                rel.add((a, b))
            elif r == 2:
                rel.add((b, a))
        cl = transitive_closure(rel)
        if cl != frozenset(rel) or not is_strict_order(cl):
            continue
        if cl in seen:
            continue
        seen.add(cl)
        out.append(cl)
    return out


def antichain(n):
    return frozenset()


def two_block_ordinal_sum(n):
    """Z_n: ordinal sum of n/2 two-element antichains.  mg-409a's alpha = 1 witness."""
    assert n % 2 == 0
    rel = set()
    for j in range(n // 2):
        for i in range(j):
            for a in (2 * i, 2 * i + 1):
                for b in (2 * j, 2 * j + 1):
                    rel.add((a, b))
    return transitive_closure(rel)


def incomparable_pairs(n, lt):
    return [(a, b) for a, b in combinations(range(n), 2)
            if (a, b) not in lt and (b, a) not in lt]


# --------------------------------------------------------------------------------------
# linear extensions
# --------------------------------------------------------------------------------------


def linear_extensions(n, lt):
    below = [set() for _ in range(n)]
    for (i, j) in lt:
        below[j].add(i)
    out, placed, seq = [], set(), []

    def rec():
        if len(seq) == n:
            out.append(tuple(seq))
            return
        for v in range(n):
            if v not in placed and below[v] <= placed:
                placed.add(v)
                seq.append(v)
                rec()
                seq.pop()
                placed.discard(v)

    rec()
    return out


def adj_swap(L, i):
    M = list(L)
    M[i], M[i + 1] = M[i + 1], M[i]
    return tuple(M)


def swap_legal(L, i, lt):
    a, b = L[i], L[i + 1]
    return (a, b) not in lt and (b, a) not in lt


# --------------------------------------------------------------------------------------
# the two checkerboard block systems -- compression.tex :14 (C_o) and :47 (C_e)
# --------------------------------------------------------------------------------------


def odd_blocks(n):
    """C_o = (I_2, I_4, ...): position blocks {0,1},{2,3},... plus a trailing singleton
    when n is odd.  Its internal edges are tau_0, tau_2, ... (the note's tau_1, tau_3, ...
    in 1-indexed positions)."""
    g = [(2 * j, 2 * j + 1) for j in range(n // 2)]
    if n % 2 == 1:
        g.append((n - 1,))
    return g


def even_blocks(n):
    """C_e = (I_1, I_3, ...): {0}, then {1,2},{3,4},... plus a trailing singleton when n is
    even.  Its internal edges are tau_1, tau_3, ..."""
    g = [(0,)] + [(2 * j + 1, 2 * j + 2) for j in range((n - 1) // 2)]
    if n % 2 == 0 and n >= 2:
        g.append((n - 1,))
    return g


def block_starts(groups):
    """The position i such that (i, i+1) is a 2-block of this system."""
    return [g[0] for g in groups if len(g) == 2]


def fiber_key(L, groups):
    return tuple(tuple(sorted(L[p] for p in g)) for g in groups)


def fibers(LEs, groups):
    out = {}
    for k, L in enumerate(LEs):
        out.setdefault(fiber_key(L, groups), []).append(k)
    return out


# --------------------------------------------------------------------------------------
# statistics on L(P)
# --------------------------------------------------------------------------------------


def positions(LEs):
    return [{v: i for i, v in enumerate(L)} for L in LEs]


def pair_orientation_stat(LEs, c):
    """f(L) = sum_{(x,y) in c} c[(x,y)] * 1{x <_L y}.  Keys are ordered (x, y), x < y."""
    pos = positions(LEs)
    out = []
    for p in pos:
        s = Fraction(0)
        for (x, y), cc in c.items():
            if p[x] < p[y]:
                s += cc
        out.append(Fraction(s))
    return out


def position_weight_stat(LEs, w):
    """f(L) = sum_x w[x] pos_L(x).  A pair-orientation linear statistic with
    c_xy = w[y] - w[x] (up to an additive constant); used as an independent generator."""
    out = []
    for L in LEs:
        out.append(sum(Fraction(w[v]) * i for i, v in enumerate(L)))
    return out


def mean(vals):
    return sum(vals) / Fraction(len(vals))


def variance(vals):
    m = mean(vals)
    return sum((v - m) ** 2 for v in vals) / Fraction(len(vals))


def covariance(u, v):
    mu, mv = mean(u), mean(v)
    return sum((a - mu) * (b - mv) for a, b in zip(u, v)) / Fraction(len(u))


def e_cond_var(vals, LEs, groups):
    """E Var(f | C) = <f, (I - Pi) f>, exactly.  The WITHIN-fiber half of the variance."""
    N = len(LEs)
    tot = Fraction(0)
    for _, idxs in fibers(LEs, groups).items():
        m = sum(vals[k] for k in idxs) / Fraction(len(idxs))
        tot += Fraction(len(idxs), N) * (
            sum((vals[k] - m) ** 2 for k in idxs) / Fraction(len(idxs)))
    return tot


def cond_expectation(vals, LEs, groups):
    """Pi f -- the fiber-averaged function.  Var of THIS is the BETWEEN-fiber half."""
    out = [None] * len(LEs)
    for _, idxs in fibers(LEs, groups).items():
        m = sum(vals[k] for k in idxs) / Fraction(len(idxs))
        for k in idxs:
            out[k] = m
    return out


def bk_energy(vals, LEs, n, lt):
    """E_BK(f) = 1/(2(n-1)N) sum_L sum_i legal (f(tau_i L) - f(L))^2 -- compression.tex :106
    ("choosing one of the n-1 adjacent positions uniformly")."""
    idx = {L: k for k, L in enumerate(LEs)}
    N = len(LEs)
    tot = Fraction(0)
    for L in LEs:
        fL = vals[idx[L]]
        for i in range(n - 1):
            if swap_legal(L, i, lt):
                tot += (vals[idx[adj_swap(L, i)]] - fL) ** 2
    return tot / Fraction(2 * (n - 1) * N)


# --------------------------------------------------------------------------------------
# THE OUTPUT MAP -- adjacency probabilities.  This is what the identity emits.
# --------------------------------------------------------------------------------------


def adjacency_probs(n, lt, LEs):
    """A_o[(x,y)], A_e[(x,y)] for every incomparable pair {x,y}, x < y:

        A_o[{x,y}] = Pr_L[ {x,y} is a 2-block of C_o ]  = Pr[ {L_2j, L_2j+1} = {x,y} ]
        A_e[{x,y}] = Pr_L[ {x,y} is a 2-block of C_e ]  = Pr[ {L_2j+1, L_2j+2} = {x,y} ]

    A_o + A_e = Pr[x, y adjacent], since every adjacent position pair (i, i+1) belongs to
    exactly one of the two systems (by the parity of i).
    """
    N = len(LEs)
    inc = incomparable_pairs(n, lt)
    A_o = {p: Fraction(0) for p in inc}
    A_e = {p: Fraction(0) for p in inc}
    so, se = set(block_starts(odd_blocks(n))), set(block_starts(even_blocks(n)))
    for L in LEs:
        for i in range(n - 1):
            key = (L[i], L[i + 1]) if L[i] < L[i + 1] else (L[i + 1], L[i])
            if key not in A_o:
                continue                      # comparable pair: never a free block
            if i in so:
                A_o[key] += Fraction(1, N)
            elif i in se:
                A_e[key] += Fraction(1, N)
    return A_o, A_e


def all_pair_adjacency(n, LEs):
    """Pr[{x,y} adjacent] for EVERY pair, comparable or not.  Used by e3: these sum to
    exactly n-1 over all pairs, which is the identity's only density-facing relation."""
    N = len(LEs)
    A = {p: Fraction(0) for p in combinations(range(n), 2)}
    for L in LEs:
        for i in range(n - 1):
            key = (L[i], L[i + 1]) if L[i] < L[i + 1] else (L[i + 1], L[i])
            A[key] += Fraction(1, N)
    return A


def machinery_output(n, lt, LEs, c):
    """(E Var(f|C_o), E Var(f|C_e)) computed the IDENTITY's way: (1/4) sum c^2 A."""
    A_o, A_e = adjacency_probs(n, lt, LEs)
    vo = sum(Fraction(c.get(p, 0)) ** 2 * A_o[p] for p in A_o) / 4
    ve = sum(Fraction(c.get(p, 0)) ** 2 * A_e[p] for p in A_e) / 4
    return vo, ve


# --------------------------------------------------------------------------------------
# programme-native quantities the enumeration tests against
# --------------------------------------------------------------------------------------


def pair_up_prob(n, lt, LEs):
    """p[(x,y)] = Pr[x <_L y] for every incomparable pair, x < y."""
    N = len(LEs)
    inc = incomparable_pairs(n, lt)
    p = {q: Fraction(0) for q in inc}
    for L in LEs:
        pos = {v: i for i, v in enumerate(L)}
        for (x, y) in inc:
            if pos[x] < pos[y]:
                p[(x, y)] += Fraction(1, N)
    return p


def delta(n, lt, LEs):
    """delta(P) = max over incomparable pairs of min(p, 1-p).  0 if P is a chain."""
    p = pair_up_prob(n, lt, LEs)
    if not p:
        return Fraction(0)
    return max(min(v, 1 - v) for v in p.values())


def majority_order(n, lt, LEs):
    """The distinguished order e: sort by E[pos].  For a frozen poset this is canonical;
    used here only as a reference for E[inv_e], and its choice is declared at every use."""
    N = len(LEs)
    epos = {v: Fraction(0) for v in range(n)}
    for L in LEs:
        for i, v in enumerate(L):
            epos[v] += Fraction(i, N)
    return sorted(range(n), key=lambda v: (epos[v], v))


def expected_inv(n, lt, LEs, e=None):
    """E[inv_e] -- the (LIB) quantity.  Counts incomparable pairs flipped against e."""
    if e is None:
        e = majority_order(n, lt, LEs)
    rank = {v: i for i, v in enumerate(e)}
    p = pair_up_prob(n, lt, LEs)
    tot = Fraction(0)
    for (x, y), pv in p.items():
        tot += (1 - pv) if rank[x] < rank[y] else pv
    return tot


def density(n, lt):
    """d(P) = m / C(n,2), the incomparability density.  Residual (R)'s quantity."""
    m = len(incomparable_pairs(n, lt))
    return Fraction(m, n * (n - 1) // 2)


def position_matrix(n, LEs):
    """T[x][i] = Pr[pos_L(x) = i].  lambda_std's object (STATE.md glossary)."""
    N = len(LEs)
    T = [[Fraction(0)] * n for _ in range(n)]
    for L in LEs:
        for i, v in enumerate(L):
            T[v][i] += Fraction(1, N)
    return T


# --------------------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------------------


def banner(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


def verdict(ok, label, extra=""):
    print(("  PASS  " if ok else "  FAIL  ") + label + (("   " + extra) if extra else ""))
    return ok


def fr(x, d=9):
    if isinstance(x, Fraction) and x.denominator == 1:
        return str(x.numerator)
    return f"{float(x):.{d}f}"
