"""mg-6bc2 — the marginal-relaxation LP, in exact rationals.

WHAT IS BEING COMPUTED, stated so it cannot be over-read.

The feasible set is EVERY probability measure mu on S_n subject to one family of
constraints: for each pair i<j, Pr_mu[j precedes i] <= 1/3, where the reference
order e is the identity.  That set is the MARGINAL RELAXATION -- it is exactly
"what a proof knows if it knows only the per-pair flip probabilities and uses
linearity of expectation".  It is strictly larger than the set of linear-extension
measures of frozen posets: it contains abstract distributions that no poset
realises (the two-atom law is one).  So an upper bound proved from it is valid for
every frozen poset, and a MAXIMISER in it is a witness that no argument using only
this information can do better.

NO POSETS ARE ENUMERATED HERE.  The refusal mg-345e declared is kept.

Exact rational simplex (Bland's rule, so it terminates).  Standard form
max c'x s.t. Ax <= b, x >= 0, b >= 0 -- the origin is feasible, so phase 1 is
unnecessary.
"""

from fractions import Fraction as F
from itertools import permutations


# ---------------------------------------------------------------- combinatorics

def inv_count(p):
    """Inversions of p against the identity: pairs i<j with j before i."""
    n = len(p)
    pos = [0] * n
    for k, x in enumerate(p):
        pos[x] = k
    return sum(1 for i in range(n) for j in range(i + 1, n) if pos[j] < pos[i])


def footrule(p):
    """Spearman footrule sum_x |pos(x) - rank_e(x)|, e = identity."""
    return sum(abs(k - x) for k, x in enumerate(p))


def flipped_pairs(p):
    """Set of pairs (i,j), i<j, that p places out of order."""
    n = len(p)
    pos = [0] * n
    for k, x in enumerate(p):
        pos[x] = k
    return {(i, j) for i in range(n) for j in range(i + 1, n) if pos[j] < pos[i]}


def adjacent_ordered_pairs(p):
    """Ordered pairs (x,y) with x immediately preceding y in p."""
    return {(p[k], p[k + 1]) for k in range(len(p) - 1)}


# ---------------------------------------------------------------- exact simplex

def simplex_max(A, b, c):
    """max c'x s.t. Ax <= b, x >= 0, with b >= 0.  Returns (value, x).

    Dense tableau, Fractions, Bland's rule.  m constraints, n variables.
    """
    m, n = len(A), len(c)
    # tableau rows: [A | I | b]; objective row: [-c | 0 | 0]
    T = [list(A[i]) + [F(1) if j == i else F(0) for j in range(m)] + [b[i]]
         for i in range(m)]
    obj = [-ci for ci in c] + [F(0)] * m + [F(0)]
    basis = [n + i for i in range(m)]

    while True:
        # Bland: lowest-index column with negative reduced cost
        piv_col = None
        for j in range(n + m):
            if obj[j] < 0:
                piv_col = j
                break
        if piv_col is None:
            break
        # ratio test, Bland tie-break on lowest basis index
        piv_row, best = None, None
        for i in range(m):
            if T[i][piv_col] > 0:
                r = T[i][-1] / T[i][piv_col]
                if best is None or r < best or (r == best and basis[i] < basis[piv_row]):
                    best, piv_row = r, i
        if piv_row is None:
            raise RuntimeError("unbounded -- cannot happen here, sum mu <= 1 is present")
        # pivot
        pv = T[piv_row][piv_col]
        T[piv_row] = [v / pv for v in T[piv_row]]
        for i in range(m):
            if i != piv_row and T[i][piv_col] != 0:
                f = T[i][piv_col]
                T[i] = [a - f * bb for a, bb in zip(T[i], T[piv_row])]
        if obj[piv_col] != 0:
            f = obj[piv_col]
            obj = [a - f * bb for a, bb in zip(obj, T[piv_row])]
        basis[piv_row] = piv_col

    x = [F(0)] * n
    for i in range(m):
        if basis[i] < n:
            x[basis[i]] = T[i][-1]
    return obj[-1], x


# ---------------------------------------------------------------- the two LPs

def relaxation_lp(n, objective, cap=F(1, 3)):
    """Max E[objective] over measures on S_n with every pair-flip prob <= cap.

    objective: a function S_n -> int (inv_count or footrule).
    Returns (optimum, optimiser as {perm: mass}).
    """
    perms = list(permutations(range(n)))
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    pidx = {p: k for k, p in enumerate(pairs)}

    # constraints: one per pair (<= cap), plus sum mu <= 1
    A, b = [], []
    rows = [[F(0)] * len(perms) for _ in pairs]
    for col, p in enumerate(perms):
        for q in flipped_pairs(p):
            rows[pidx[q]][col] = F(1)
    A.extend(rows)
    b.extend([cap] * len(pairs))
    A.append([F(1)] * len(perms))
    b.append(F(1))

    c = [F(objective(p)) for p in perms]
    val, x = simplex_max(A, b, c)
    support = {perms[k]: x[k] for k in range(len(perms)) if x[k] != 0}
    return val, support


# ---------------------------------------------------------------- witnesses

def two_atom(n, p=F(1, 3)):
    """(1-p) * identity  +  p * reversal."""
    ident = tuple(range(n))
    rev = tuple(reversed(range(n)))
    return {ident: F(1) - p, rev: p}


def hierarchical(n, levels=3, mass=F(1, 3)):
    """Level ell: 2^ell blocks, each internally half-rotated.  Disjoint flip-sets.

    Only defined cleanly when n is divisible by 2^levels.
    """
    atoms = {}
    for ell in range(levels):
        nb = 2 ** ell
        bs = n // nb
        if bs < 2:
            continue
        perm = []
        for blk in range(nb):
            base = blk * bs
            half = bs // 2
            # half-rotation inside the block: second half first
            perm.extend(range(base + half, base + bs))
            perm.extend(range(base, base + half))
        atoms[tuple(perm)] = atoms.get(tuple(perm), F(0)) + mass
    return atoms


def measure_stats(n, mu):
    """(E[inv], E[footrule], max pair-flip prob, adjacency-symmetry violated?)."""
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    q = {pr: F(0) for pr in pairs}
    ei = ef = F(0)
    adj = {}
    for p, w in mu.items():
        ei += w * inv_count(p)
        ef += w * footrule(p)
        for pr in flipped_pairs(p):
            q[pr] += w
        for op in adjacent_ordered_pairs(p):
            adj[op] = adj.get(op, F(0)) + w
    asym = [(x, y) for (x, y) in adj if adj.get((x, y), F(0)) != adj.get((y, x), F(0))]
    return ei, ef, max(q.values()), asym
