"""mg-200d — the marginal relaxation with ADJACENCY SYMMETRY imposed, exact rationals.

WHAT IS BEING COMPUTED, stated so it cannot be over-read.

The base feasible set is `mg-6bc2`'s `M_n`: every probability measure `mu` on `S_n` with
`Pr_mu[j precedes i] <= 1/3` for each pair `i < j`, the reference order `e` being the
identity.  This file adds ADJACENCY-SYMMETRY information to it, in five forms, and the
distinction between them is the whole finding:

  LITERAL forms   -- `J_k(x,y) = J_k(y,x)` (per-slot) or `J(x,y) = J(y,x)` (aggregate)
                     imposed on EVERY pair.  These are what the ticket asks for verbatim
                     and they are UNSOUND: they hold for `uniform L(P)` only when `P` is an
                     antichain (any cover `x <. y` gives `J_k(x,y) > 0 = J_k(y,x)`), and no
                     antichain is in `M_n` (all its flips are 1/2).  Computed anyway,
                     because the number is the evidence that they are unsound.

  SURROGATE forms -- `J_k(y,x) <= J_k(x,y)` (per-slot) or `J(y,x) <= J(x,y)` (aggregate).
                     Valid for EVERY poset with `e` a linear extension: comparable pairs
                     give `J_k(y,x) = 0`, incomparable pairs give equality.  Branch-free.

  DISJUNCTIVE form -- for each pair independently, EITHER `q_xy = 0` (comparable; realised
                     by deleting the columns that flip it) OR symmetry on that pair
                     (incomparable).  This is exactly what realisability forces, with no
                     slack, and the maximum over the `2^C(n,2)` branches is a valid upper
                     bound for every frozen poset.

NO POSET IS ENUMERATED HERE.  `mg-345e`'s and `mg-6bc2`'s refusal is kept, and the
disjunctive form does not break it: no poset is constructed, transitivity is never imposed
(so the branch family is a strict SUPERSET of the comparability patterns of real posets,
which is what makes the maximum an upper bound), and every branch is a set of measures on
`S_n`.  See `README.md` and the document's `§7`.

The simplex is an independent two-phase implementation (Bland's rule, exact `Fraction`s).
It shares no code with `mg-6bc2`'s `lp6bc2.py`, which is single-phase and requires `b >= 0`
with the origin feasible -- a form that cannot express `Sum mu = 1` or any equality.
"""

from fractions import Fraction as F
from itertools import permutations

CAP = F(1, 3)


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


def flips(p):
    """Pairs (i,j), i<j, that p places out of order (j before i)."""
    n = len(p)
    pos = [0] * n
    for k, x in enumerate(p):
        pos[x] = k
    return {(i, j) for i in range(n) for j in range(i + 1, n) if pos[j] < pos[i]}


def slot_adjacencies(p):
    """{(k, x, y)} with x at slot k and y at slot k+1."""
    return {(k, p[k], p[k + 1]) for k in range(len(p) - 1)}


def pairs_of(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


# ---------------------------------------------------------------- exact simplex

class Infeasible(Exception):
    """The constraint system has no solution -- reported, never swallowed."""


def _pivot(T, obj, piv_row, piv_col, basis):
    pv = T[piv_row][piv_col]
    if pv != 1:
        T[piv_row] = [v / pv for v in T[piv_row]]
    prow = T[piv_row]
    for i, row in enumerate(T):
        if i != piv_row:
            f = row[piv_col]
            if f:
                T[i] = [a - f * b for a, b in zip(row, prow)]
    f = obj[piv_col]
    if f:
        for j in range(len(obj)):
            if prow[j]:
                obj[j] -= f * prow[j]
    basis[piv_row] = piv_col


def _optimise(T, obj, basis, ncols, allowed):
    """Primal simplex to optimality on the current tableau.  Bland's rule."""
    m = len(T)
    while True:
        piv_col = None
        for j in range(ncols):
            if allowed[j] and obj[j] < 0:
                piv_col = j
                break
        if piv_col is None:
            return
        piv_row, best = None, None
        for i in range(m):
            a = T[i][piv_col]
            if a > 0:
                r = T[i][-1] / a
                if best is None or r < best or (r == best and basis[i] < basis[piv_row]):
                    best, piv_row = r, i
        if piv_row is None:
            raise RuntimeError("unbounded -- cannot happen, Sum mu = 1 is present")
        _pivot(T, obj, piv_row, piv_col, basis)


def solve_max(nvars, rows, c):
    """max c'x  s.t.  rows, x >= 0.   rows = [(coeffs_dict, sense, rhs)], sense in <=,>=,==.

    coeffs_dict maps variable index -> Fraction.  Returns (value, x) with exact Fractions.
    Raises Infeasible if the system has no solution.
    """
    # --- normalise to b >= 0, attach slack/surplus, mark rows needing an artificial
    norm = []
    for coeffs, sense, rhs in rows:
        if rhs < 0:
            coeffs = {k: -v for k, v in coeffs.items()}
            rhs = -rhs
            sense = {"<=": ">=", ">=": "<=", "==": "=="}[sense]
        norm.append((coeffs, sense, F(rhs)))

    nslack = sum(1 for _, s, _ in norm if s in ("<=", ">="))
    nart = sum(1 for _, s, _ in norm if s in (">=", "=="))
    ncols = nvars + nslack + nart
    m = len(norm)

    T = [[F(0)] * (ncols + 1) for _ in range(m)]
    basis = [None] * m
    si, ai = nvars, nvars + nslack
    art_cols = []
    for i, (coeffs, sense, rhs) in enumerate(norm):
        row = T[i]
        for k, v in coeffs.items():
            row[k] = F(v)
        row[-1] = rhs
        if sense == "<=":
            row[si] = F(1)
            basis[i] = si
            si += 1
        elif sense == ">=":
            row[si] = F(-1)
            si += 1
            row[ai] = F(1)
            basis[i] = ai
            art_cols.append(ai)
            ai += 1
        else:
            row[ai] = F(1)
            basis[i] = ai
            art_cols.append(ai)
            ai += 1

    allowed = [True] * ncols

    # --- phase 1: minimise the artificial total (= maximise its negative)
    if nart:
        obj = [F(0)] * (ncols + 1)
        for j in art_cols:
            obj[j] = F(1)
        # price out the basic artificials
        for i in range(m):
            if basis[i] in art_cols:
                for j in range(ncols + 1):
                    if T[i][j]:
                        obj[j] -= T[i][j]
        _optimise(T, obj, basis, ncols, allowed)
        if -obj[-1] != 0:
            raise Infeasible(f"phase-1 residual {-obj[-1]}")
        # drive any artificial still basic (at value 0) out of the basis
        for i in range(m):
            if basis[i] in art_cols:
                piv = None
                for j in range(ncols):
                    if j not in art_cols and T[i][j] != 0:
                        piv = j
                        break
                if piv is None:
                    continue          # redundant row; leave it, the artificial is pinned at 0
                _pivot(T, obj, i, piv, basis)
        for j in art_cols:
            allowed[j] = False

    # --- phase 2
    obj = [F(0)] * (ncols + 1)
    for k, v in enumerate(c):
        obj[k] = -F(v)
    for i in range(m):
        b = basis[i]
        if b is not None and obj[b] != 0:
            f = obj[b]
            for j in range(ncols + 1):
                if T[i][j]:
                    obj[j] -= f * T[i][j]
    _optimise(T, obj, basis, ncols, allowed)

    x = [F(0)] * nvars
    for i in range(m):
        if basis[i] is not None and basis[i] < nvars:
            x[basis[i]] = T[i][-1]
    return obj[-1], x


# ---------------------------------------------------------------- constraint builders

def build(n, form, comparable=frozenset(), perms=None, cap=CAP):
    """Rows for the relaxation on `perms`, under one adjacency-symmetry `form`.

    form:
      'none'          -- baseline `M_n` only
      'slot_eq'       -- J_k(x,y) = J_k(y,x)   on every non-comparable pair   (LITERAL)
      'agg_eq'        -- J(x,y)   = J(y,x)     on every non-comparable pair   (LITERAL)
      'slot_le'       -- J_k(y,x) <= J_k(x,y)  on every non-comparable pair   (SURROGATE)
      'agg_le'        -- J(y,x)   <= J(x,y)    on every non-comparable pair   (SURROGATE)

    `comparable` is the set of pairs declared comparable in this branch; those pairs carry
    no symmetry row (a comparable pair is entitled to be asymmetric) and their flipping
    columns are expected to be absent from `perms` already.
    """
    if perms is None:
        perms = list(permutations(range(n)))
    N = len(perms)
    rows = [({k: F(1) for k in range(N)}, "==", F(1))]

    flipsets = [flips(p) for p in perms]
    for (i, j) in pairs_of(n):
        if (i, j) in comparable:
            continue
        col = {k: F(1) for k in range(N) if (i, j) in flipsets[k]}
        if col:
            rows.append((col, "<=", cap))

    if form == "none":
        return perms, rows

    adj = [slot_adjacencies(p) for p in perms]

    def jslot(k_slot, x, y):
        return {c: F(1) for c in range(N) if (k_slot, x, y) in adj[c]}

    for (x, y) in pairs_of(n):
        if (x, y) in comparable:
            continue
        if form in ("slot_eq", "slot_le"):
            spans = [(k,) for k in range(n - 1)]
        else:
            spans = [tuple(range(n - 1))]
        for span in spans:
            fwd, bwd = {}, {}
            for k_slot in span:
                for c in jslot(k_slot, x, y):
                    fwd[c] = fwd.get(c, F(0)) + 1
                for c in jslot(k_slot, y, x):
                    bwd[c] = bwd.get(c, F(0)) + 1
            coeffs = dict(bwd)
            for c, v in fwd.items():
                coeffs[c] = coeffs.get(c, F(0)) - v
            coeffs = {c: v for c, v in coeffs.items() if v != 0}
            if not coeffs:
                continue
            sense = "==" if form.endswith("_eq") else "<="
            rows.append((coeffs, sense, F(0)))
    return perms, rows


def relaxation(n, form="none", objective=inv_count, comparable=frozenset(), cap=CAP):
    """(value, {perm: mass}) for the relaxation.  Raises Infeasible when empty."""
    allperms = list(permutations(range(n)))
    if comparable:
        keep = [p for p in allperms if not (flips(p) & comparable)]
    else:
        keep = allperms
    if not keep:
        raise Infeasible("no permutation respects the declared comparabilities")
    perms, rows = build(n, form, comparable, perms=keep, cap=cap)
    c = [F(objective(p)) for p in perms]
    val, x = solve_max(len(perms), rows, c)
    return val, {perms[k]: x[k] for k in range(len(perms)) if x[k] != 0}


# ---------------------------------------------------------------- diagnostics

def measure_report(n, mu):
    """Facts about a measure, all computed on the FULL measure (mass must be 1)."""
    total = sum(mu.values())
    q = {pr: F(0) for pr in pairs_of(n)}
    J = {}
    ei = ef = F(0)
    for p, w in mu.items():
        ei += w * inv_count(p)
        ef += w * footrule(p)
        for pr in flips(p):
            q[pr] += w
        for (k, x, y) in slot_adjacencies(p):
            J[(k, x, y)] = J.get((k, x, y), F(0)) + w

    def g(k, x, y):
        return J.get((k, x, y), F(0))

    slot_bad = [((x, y), k) for (x, y) in pairs_of(n) for k in range(n - 1)
                if g(k, x, y) != g(k, y, x)]
    agg_bad = [(x, y) for (x, y) in pairs_of(n)
               if sum(g(k, x, y) for k in range(n - 1))
               != sum(g(k, y, x) for k in range(n - 1))]
    slot_le_bad = [((x, y), k) for (x, y) in pairs_of(n) for k in range(n - 1)
                   if g(k, y, x) > g(k, x, y)]
    agg_le_bad = [(x, y) for (x, y) in pairs_of(n)
                  if sum(g(k, y, x) for k in range(n - 1))
                  > sum(g(k, x, y) for k in range(n - 1))]
    return {
        "mass": total, "E_inv": ei, "E_footrule": ef,
        "max_flip": max(q.values()) if q else F(0),
        "zero_flip_pairs": sorted(pr for pr, v in q.items() if v == 0),
        "slot_eq_violations": slot_bad, "agg_eq_violations": agg_bad,
        "slot_le_violations": slot_le_bad, "agg_le_violations": agg_le_bad,
    }


def eps_spec(n, e_inv):
    """The architecture's normalisation:  E[inv_e] <= (eps_spec/6)(n^2-1)."""
    return 6 * e_inv / (n * n - 1)


def uniform_le_measure(n, relation):
    """Uniform measure on the linear extensions of a relation given as a set of (x,y), x<y.

    Used ONLY by the selftest, to check the symmetry forms against real posets.  It builds
    the linear extensions of ONE hand-named relation; it does not enumerate posets.
    """
    lin = [p for p in permutations(range(n))
           if all(p.index(x) < p.index(y) for (x, y) in relation)]
    w = F(1, len(lin))
    return {p: w for p in lin}
