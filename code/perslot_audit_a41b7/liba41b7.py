"""liba41b7 — mg-41b7's independent audit library for mg-200d.

Written from the mathematics, not from `lp6bc2.py` or `lp200d.py`.  Nothing in this
file is imported from, copied from, or derived from either.  The ONLY contact this
audit has with `mg-200d`'s code is in `a4_rowcheck.py`, where its rows are read in
order to ASSERT that mine are its rows.  That is an assertion, not a dependency:
every number this audit reports is produced by the code below.

Exact rationals everywhere.  There is no float in this file.

Conventions, stated once and used without variation
---------------------------------------------------
* A permutation is a tuple `s` of length `n` over `{0,...,n-1}` giving the
  ARRANGEMENT: `s[k]` is the element sitting in slot `k` (0-indexed).  So `s` is
  the one-line word, and `s = (0,1,...,n-1)` is the reference order `e`.
* `pos(s, x)` is the slot holding `x`.
* A pair `{a,b}` with `a < b` is FLIPPED by `s` when `pos(s,b) < pos(s,a)`.
  `inv(s)` is the number of flipped pairs, i.e. inversions against `e`.
* `J_k(x,y) = mu{ s : s[k] = x and s[k+1] = y }` for `k = 0,...,n-2`.
  This is the PER-SLOT adjacency function.  `J(x,y) = sum_k J_k(x,y)` is the
  AGGREGATE one.
"""

from fractions import Fraction as F

# ---------------------------------------------------------------------------
# combinatorics (mine)
# ---------------------------------------------------------------------------


def perms(n):
    """All arrangements of 0..n-1, by insertion.  Not itertools."""
    out = [()]
    for x in range(n):
        nxt = []
        for p in out:
            for i in range(len(p) + 1):
                nxt.append(p[:i] + (x,) + p[i:])
        out = nxt
    return sorted(out)


def pos(s, x):
    return s.index(x)


def inv(s):
    """Inversions of the arrangement `s` against e = (0,1,...,n-1)."""
    n = len(s)
    c = 0
    for a in range(n):
        for b in range(a + 1, n):
            if pos(s, b) < pos(s, a):
                c += 1
    return c


def pairs(n):
    return [(a, b) for a in range(n) for b in range(a + 1, n)]


# ---------------------------------------------------------------------------
# rows
# ---------------------------------------------------------------------------
#
# A row is (coeffs, sense, rhs) with coeffs a dict {var_index: Fraction},
# sense in {"<=", ">=", "="}, rhs a Fraction.  Variables are indexed by the
# position of the permutation in `perms(n)`.


def row_normalisation(n, P):
    return ({j: F(1) for j in range(len(P))}, "=", F(1))


def rows_pairbias(n, P, cap=F(1, 3)):
    """P(pair {a,b} flipped against e) <= cap, for every pair."""
    rows = []
    for (a, b) in pairs(n):
        c = {}
        for j, s in enumerate(P):
            if pos(s, b) < pos(s, a):
                c[j] = F(1)
        rows.append((c, "<=", cap))
    return rows


def _slot_adj_index(n, P):
    """adj[k][(x,y)] = list of permutation indices with s[k]=x, s[k+1]=y."""
    adj = [dict() for _ in range(n - 1)]
    for j, s in enumerate(P):
        for k in range(n - 1):
            adj[k].setdefault((s[k], s[k + 1]), []).append(j)
    return adj


def rows_perslot_symmetry(n, P, slots=None, pairset=None):
    """J_k(x,y) - J_k(y,x) = 0, one row per (slot, unordered pair).

    `slots` restricts the slots imposed (default all of 0..n-2);
    `pairset` restricts the unordered pairs imposed (default all).
    """
    adj = _slot_adj_index(n, P)
    slots = range(n - 1) if slots is None else slots
    pairset = pairs(n) if pairset is None else pairset
    rows = []
    for k in slots:
        for (x, y) in pairset:
            c = {}
            for j in adj[k].get((x, y), []):
                c[j] = c.get(j, F(0)) + F(1)
            for j in adj[k].get((y, x), []):
                c[j] = c.get(j, F(0)) - F(1)
            c = {j: v for j, v in c.items() if v != 0}
            if not c:
                continue          # 0 = 0 carries no information; emitting it would
                                  # only add a phase-1 artificial and make row-by-row
                                  # comparison with another builder spuriously differ
            rows.append((c, "=", F(0)))
    return rows


def rows_aggregate_symmetry(n, P, pairset=None):
    """J(x,y) - J(y,x) = 0 summed over ALL slots, one row per unordered pair."""
    adj = _slot_adj_index(n, P)
    pairset = pairs(n) if pairset is None else pairset
    rows = []
    for (x, y) in pairset:
        c = {}
        for k in range(n - 1):
            for j in adj[k].get((x, y), []):
                c[j] = c.get(j, F(0)) + F(1)
            for j in adj[k].get((y, x), []):
                c[j] = c.get(j, F(0)) - F(1)
        c = {j: v for j, v in c.items() if v != 0}
        if not c:
            continue
        rows.append((c, "=", F(0)))
    return rows


def objective_inv(n, P):
    return {j: F(inv(s)) for j, s in enumerate(P) if inv(s) != 0}


# ---------------------------------------------------------------------------
# exact two-phase simplex, Bland's rule
# ---------------------------------------------------------------------------
#
# max c.x subject to the rows, x >= 0.  Returns a dict with an explicit
# `status` in {"optimal", "infeasible", "unbounded"} -- an INFEASIBLE system and
# a feasible system whose optimum is 0 are DIFFERENT return values here, which is
# the whole point of brief item 4.


class LPResult(object):
    def __init__(self, status, value=None, x=None, y=None, phase1=None, pivots=None):
        self.status = status
        self.value = value
        self.x = x          # primal, dict var -> Fraction
        self.y = y          # dual, list over rows
        self.phase1 = phase1  # phase-1 optimum (0 iff feasible)
        self.pivots = pivots

    def __repr__(self):
        return "LPResult(%s, value=%s, phase1=%s)" % (self.status, self.value, self.phase1)


def solve(nvars, rows, obj, maximise=True):
    m = len(rows)
    # --- normalise: rhs >= 0
    norm = []
    flipped = []
    for (c, sense, b) in rows:
        if b < 0:
            c = {j: -v for j, v in c.items()}
            b = -b
            sense = {"<=": ">=", ">=": "<=", "=": "="}[sense]
            flipped.append(True)
        else:
            flipped.append(False)
        norm.append((c, sense, b))

    # --- column layout: [0, nvars) structural | slacks | artificials
    slack_col = {}
    art_col = {}
    ncol = nvars
    for i, (c, sense, b) in enumerate(norm):
        if sense == "<=":
            slack_col[i] = ncol
            ncol += 1
        elif sense == ">=":
            slack_col[i] = ncol   # surplus, coefficient -1
            ncol += 1
    for i, (c, sense, b) in enumerate(norm):
        if sense in (">=", "="):
            art_col[i] = ncol
            ncol += 1

    # --- dense tableau
    T = [[F(0)] * (ncol + 1) for _ in range(m)]
    for i, (c, sense, b) in enumerate(norm):
        Ti = T[i]
        for j, v in c.items():
            Ti[j] = F(v)
        if sense == "<=":
            Ti[slack_col[i]] = F(1)
        elif sense == ">=":
            Ti[slack_col[i]] = F(-1)
        if i in art_col:
            Ti[art_col[i]] = F(1)
        Ti[ncol] = F(b)

    basis = []
    for i, (c, sense, b) in enumerate(norm):
        basis.append(art_col[i] if i in art_col else slack_col[i])

    # identity column of row i, used later to read the dual off the objective row
    ident_col = [art_col[i] if i in art_col else slack_col[i] for i in range(m)]

    pivots = [0]

    def _pivot(T, basis, r, cc):
        piv = T[r][cc]
        Tr = T[r]
        if piv != 1:
            T[r] = Tr = [v / piv for v in Tr]
        for i in range(len(T)):
            if i == r:
                continue
            f = T[i][cc]
            if f != 0:
                Ti = T[i]
                for j in range(len(Ti)):
                    if Tr[j] != 0:
                        Ti[j] -= f * Tr[j]
                Ti[cc] = F(0)
        basis[r] = cc
        pivots[0] += 1

    def _run(cost, allowed):
        """minimise `cost` (dict col->Fraction) over the current tableau.

        Bland's rule.  `allowed` is a set of columns permitted to enter.
        Returns the objective row (reduced costs z_j - c_j) and the value.
        """
        # objective row: z_j - c_j for all columns, plus value in last slot
        z = [F(0)] * (ncol + 1)
        for i in range(m):
            cb = cost.get(basis[i], F(0))
            if cb != 0:
                Ti = T[i]
                for j in range(ncol + 1):
                    if Ti[j] != 0:
                        z[j] += cb * Ti[j]
        for j in range(ncol):
            z[j] -= cost.get(j, F(0))
        while True:
            enter = None
            for j in sorted(allowed):
                if z[j] > 0:                       # minimisation: z_j - c_j > 0 improves
                    enter = j
                    break
            if enter is None:
                return z
            # ratio test, Bland tie-break on the smallest basis index
            leave = None
            best = None
            for i in range(m):
                if T[i][enter] > 0:
                    ratio = T[i][ncol] / T[i][enter]
                    if best is None or ratio < best or (ratio == best and basis[i] < basis[leave]):
                        best = ratio
                        leave = i
            if leave is None:
                return None                        # unbounded
            _pivot(T, basis, leave, enter)
            # recompute reduced costs from scratch is O(m*ncol); update instead
            f = z[enter]
            if f != 0:
                Tr = T[leave]
                for j in range(ncol + 1):
                    if Tr[j] != 0:
                        z[j] -= f * Tr[j]
                z[enter] = F(0)

    # ---- phase 1
    p1val = F(0)
    if art_col:
        cost1 = {c: F(1) for c in art_col.values()}
        allowed1 = set(range(ncol))
        z1 = _run(cost1, allowed1)
        if z1 is None:
            return LPResult("unbounded_phase1")
        p1val = z1[ncol]
        if p1val != 0:
            return LPResult("infeasible", phase1=p1val, pivots=pivots[0])
        # drive artificials out of the basis where possible
        arts = set(art_col.values())
        for i in range(m):
            if basis[i] in arts:
                for j in range(ncol):
                    if j not in arts and T[i][j] != 0:
                        _pivot(T, basis, i, j)
                        break
    else:
        arts = set()

    # ---- phase 2: minimise -c  (so that a max problem is handled uniformly)
    sgn = F(-1) if maximise else F(1)
    cost2 = {j: sgn * F(v) for j, v in obj.items()}
    allowed2 = set(range(ncol)) - arts
    z2 = _run(cost2, allowed2)
    if z2 is None:
        return LPResult("unbounded", phase1=p1val, pivots=pivots[0])

    x = {}
    for i in range(m):
        if basis[i] < nvars and T[i][ncol] != 0:
            x[basis[i]] = T[i][ncol]
    value = sgn * z2[ncol]

    # ---- dual, read off the objective row under the identity columns
    y = []
    for i in range(m):
        yi = sgn * z2[ident_col[i]]
        if flipped[i]:
            yi = -yi
        y.append(yi)
    return LPResult("optimal", value=value, x=x, y=y, phase1=p1val, pivots=pivots[0])


# ---------------------------------------------------------------------------
# independent verification of an LP answer (does not trust the simplex)
# ---------------------------------------------------------------------------


def check_primal(nvars, rows, obj, x, value):
    """Verify x >= 0, x satisfies every row, and obj.x == value.  Exact."""
    errs = []
    for j, v in x.items():
        if v < 0:
            errs.append("x[%d] = %s < 0" % (j, v))
    for i, (c, sense, b) in enumerate(rows):
        lhs = sum((F(v) * x.get(j, F(0)) for j, v in c.items()), F(0))
        if sense == "<=" and lhs > b:
            errs.append("row %d: %s > %s" % (i, lhs, b))
        if sense == ">=" and lhs < b:
            errs.append("row %d: %s < %s" % (i, lhs, b))
        if sense == "=" and lhs != b:
            errs.append("row %d: %s != %s" % (i, lhs, b))
    got = sum((F(v) * x.get(j, F(0)) for j, v in obj.items()), F(0))
    if got != value:
        errs.append("objective %s != reported %s" % (got, value))
    return errs


def check_dual(nvars, rows, obj, y, value):
    """Verify the dual of  max c.x s.t. rows, x >= 0.

    Dual feasibility:  sign(y_i) per sense, and  sum_i y_i a_ij >= c_j for every j.
    Strong duality:    sum_i y_i b_i == value.
    A dual passing this is a PROOF that the primal optimum is <= value.
    """
    errs = []
    colsum = [F(0)] * nvars
    for i, (c, sense, b) in enumerate(rows):
        yi = y[i]
        if sense == "<=" and yi < 0:
            errs.append("y[%d] = %s < 0 on a <= row" % (i, yi))
        if sense == ">=" and yi > 0:
            errs.append("y[%d] = %s > 0 on a >= row" % (i, yi))
        if yi != 0:
            for j, v in c.items():
                colsum[j] += yi * F(v)
    for j in range(nvars):
        if colsum[j] < F(obj.get(j, 0)):
            errs.append("dual col %d: %s < c_j = %s" % (j, colsum[j], obj.get(j, 0)))
    bt = sum((y[i] * F(rows[i][2]) for i in range(len(rows))), F(0))
    if bt != value:
        errs.append("b.y = %s != value %s" % (bt, value))
    return errs


# ---------------------------------------------------------------------------
# measure helpers (for exhibiting witnesses)
# ---------------------------------------------------------------------------


def measure_from_atoms(n, atoms):
    """atoms: dict {arrangement tuple: Fraction} -> dict {var index: Fraction}."""
    P = perms(n)
    idx = {s: j for j, s in enumerate(P)}
    return {idx[s]: F(w) for s, w in atoms.items() if F(w) != 0}


def report(n, x, P=None):
    """Diagnostics of a measure: mass, E[inv], flip probabilities, J_k asymmetry."""
    P = P or perms(n)
    mass = sum(x.values(), F(0))
    einv = sum((F(inv(P[j])) * v for j, v in x.items()), F(0))
    flips = {}
    for (a, b) in pairs(n):
        flips[(a, b)] = sum((v for j, v in x.items() if pos(P[j], b) < pos(P[j], a)), F(0))
    adj = _slot_adj_index(n, P)
    slot_viol = {}
    for k in range(n - 1):
        for (a, b) in pairs(n):
            u = sum((x.get(j, F(0)) for j in adj[k].get((a, b), [])), F(0))
            v = sum((x.get(j, F(0)) for j in adj[k].get((b, a), [])), F(0))
            if u != v:
                slot_viol[(k, a, b)] = (u, v)
    agg_viol = {}
    for (a, b) in pairs(n):
        u = sum((x.get(j, F(0)) for k in range(n - 1) for j in adj[k].get((a, b), [])), F(0))
        v = sum((x.get(j, F(0)) for k in range(n - 1) for j in adj[k].get((b, a), [])), F(0))
        if u != v:
            agg_viol[(a, b)] = (u, v)
    return dict(mass=mass, einv=einv, flips=flips,
                slot_violations=slot_viol, agg_violations=agg_viol)


def eps_spec(n, einv):
    """The currency the programme reports in: 6 E[inv_e] / (n^2 - 1)."""
    return F(6) * F(einv) / F(n * n - 1)


def report_atoms(n, atoms):
    """Same diagnostics as `report`, computed DIRECTLY from a sparse atom list.

    `report` indexes into `perms(n)` and so cannot be used past n ~ 9.  This one is
    O(#atoms * n^2) and is what the (n-1)/3 construction is checked with at n up to 20.
    """
    mass = sum((F(w) for w in atoms.values()), F(0))
    einv = sum((F(w) * inv(s) for s, w in atoms.items()), F(0))
    flips = {}
    for (a, b) in pairs(n):
        flips[(a, b)] = sum((F(w) for s, w in atoms.items()
                             if pos(s, b) < pos(s, a)), F(0))
    J = {}
    for s, w in atoms.items():
        for k in range(n - 1):
            key = (k, s[k], s[k + 1])
            J[key] = J.get(key, F(0)) + F(w)
    slot_viol = {}
    for k in range(n - 1):
        for (a, b) in pairs(n):
            u = J.get((k, a, b), F(0))
            v = J.get((k, b, a), F(0))
            if u != v:
                slot_viol[(k, a, b)] = (u, v)
    return dict(mass=mass, einv=einv, flips=flips, slot_violations=slot_viol)
