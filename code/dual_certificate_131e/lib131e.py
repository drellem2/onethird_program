"""mg-131e -- DUAL CERTIFICATES for the `<=` direction of mg-200d's disjunctive value.

WHAT IS BEING CERTIFIED, stated so it cannot be over-read.

mg-200d's number is a MAX OVER BRANCHES.  For each subset `C` of pairs declared comparable it
solves an LP over the measures on the permutations that flip no pair of `C`, subject to the
flip caps `q_ij <= 1/3` on the incomparable pairs `I` and to PER-SLOT ADJACENCY SYMMETRY on
those same pairs, and reports the maximum over all `2^C(n,2)` branches.  So

    the `<=` direction  ==  `val(C) <= (n-1)/3` FOR EVERY BRANCH `C`,

and a certificate of it is a FAMILY of dual certificates, one per branch, covering the
infeasible branches too -- not one certificate.

THE CERTIFICATE OBJECT.  mg-200d's branch LP is, in `lp200d.build`'s own rows,

    max  sum_p mu_p inv(p)
    s.t. sum_p mu_p = 1                                   (rhs 1, sense `==`)
         q_ij(mu) <= 1/3          for ij in I active      (rhs 1/3, sense `<=`)
         (bwd - fwd)_{ij,k}(mu) = 0   for ij in I, slot k (rhs 0, sense `==`)
         mu >= 0

A dual certificate is a vector `y`, one entry per row, with

    y_i >= 0 on every `<=` row,  y_i <= 0 on every `>=` row,  y_i free on every `==` row,
    and   sum_i y_i A_ij >= c_j   for EVERY column j.

`verify_dual` checks exactly those two things by direct arithmetic over `Fraction`s and
returns the bound `y . b`.  It calls no simplex.  The soundness is three lines and is worth
writing out because the whole deliverable rests on it:

    for a `<=` row with y_i >= 0:  y_i (A_i mu) <= y_i b_i
    for an `==` row (y_i free):    y_i (A_i mu)  = y_i b_i
    so  sum_j mu_j (sum_i y_i A_ij) <= y . b,  and since mu >= 0 and sum_i y_i A_ij >= c_j,
        c . mu <= sum_j mu_j (sum_i y_i A_ij) <= y . b.

This holds whether or not the branch is primal-feasible: on an infeasible branch it is a true
statement about an empty set and CERTIFIES NOTHING.  `branch_class` exists so that vacuous
certificates are never counted as evidence (PREDICTIONS P12).

THE ROWS ARE mg-200d's, NOT MINE.  `branch_lp` calls `lp200d.build` directly.  A certificate
for a re-derived row set would certify a different LP than the one whose value is in question,
which is why the ticket says to use mg-200d's formulation and not to re-derive one.
"""

import os
import sys
from fractions import Fraction as F
from itertools import combinations, permutations

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "perslot_symmetry_200d"))

from lp200d import (CAP, Infeasible, build, flips, inv_count, pairs_of,  # noqa: E402
                    slot_adjacencies, solve_max)


# ---------------------------------------------------------------- the branch LP

def branch_columns(n, comparable):
    """The columns of branch `comparable`: permutations flipping no comparable pair."""
    comp = frozenset(comparable)
    return [p for p in permutations(range(n)) if not (flips(p) & comp)]


def branch_lp(n, comparable, form="slot_eq"):
    """(perms, rows, c) for mg-200d's branch LP.  Rows come from `lp200d.build` verbatim."""
    keep = branch_columns(n, comparable)
    if not keep:
        raise Infeasible("no permutation respects the declared comparabilities")
    perms, rows = build(n, form, frozenset(comparable), perms=keep)
    c = [F(inv_count(p)) for p in perms]
    return perms, rows, c


def row_kind(row):
    """'sum', 'cap' or 'sym' -- which of the three families a built row belongs to."""
    coeffs, sense, rhs = row
    if sense == "==" and rhs == 1:
        return "sum"
    if sense == "<=" and rhs == CAP:
        return "cap"
    return "sym"


def label_rows(n, comparable, rows):
    """Human labels for the rows, in `build`'s own order: sum, then caps, then symmetry.

    `build` emits the cap rows over `pairs_of(n)` skipping comparable pairs AND skipping any
    pair no column flips (`if col:`), then the symmetry rows over `pairs_of(n)` x slots,
    skipping comparable pairs and identically-zero rows.  Reconstructing the labels by
    replaying that order is checked against `row_kind` in the selftest.
    """
    labels = []
    for r in rows:
        labels.append(row_kind(r))
    return labels


# ---------------------------------------------------------------- the verifier

class DualCheck:
    """Result of verifying a dual vector.  Truthy iff the certificate is valid."""

    def __init__(self, ok, bound, sign_violations, column_violations, ncols):
        self.ok = ok
        self.bound = bound
        self.sign_violations = sign_violations
        self.column_violations = column_violations
        self.ncols = ncols

    def __bool__(self):
        return self.ok

    def __repr__(self):
        return (f"DualCheck(ok={self.ok}, bound={self.bound}, "
                f"sign_viol={len(self.sign_violations)}, "
                f"col_viol={len(self.column_violations)}/{self.ncols})")


def verify_dual(rows, c, y):
    """Check a dual vector by DIRECT ARITHMETIC.  No simplex is involved.

    `rows` as `lp200d.build` emits them: [(coeffs_dict, sense, rhs)].  `c` the objective over
    columns.  `y` one Fraction per row.  Returns a `DualCheck`; `bound` is `y . b`, which is a
    valid upper bound on the primal max exactly when `ok`.
    """
    assert len(y) == len(rows), f"{len(y)} multipliers for {len(rows)} rows"
    ncols = len(c)
    sign_viol = []
    for i, (_, sense, _) in enumerate(rows):
        if sense == "<=" and y[i] < 0:
            sign_viol.append((i, sense, y[i]))
        if sense == ">=" and y[i] > 0:
            sign_viol.append((i, sense, y[i]))

    acc = [F(0)] * ncols
    for i, (coeffs, _, _) in enumerate(rows):
        yi = y[i]
        if yi:
            for j, v in coeffs.items():
                acc[j] += yi * v
    col_viol = [(j, acc[j], c[j]) for j in range(ncols) if acc[j] < c[j]]

    bound = sum(y[i] * rows[i][2] for i in range(len(rows)))
    return DualCheck(not sign_viol and not col_viol, bound, sign_viol, col_viol, ncols)


# ---------------------------------------------------------------- named dual families

def trivial_dual(rows):
    """lambda = 0, t = 1 on every cap row, s = 0.  Feasible in EVERY branch (H2).

    Objective `|I_active|/3`, where `I_active` counts the incomparable pairs that some column
    actually flips -- `build` writes no cap row for the others, so they cost nothing.  This is
    the `refined` form of the trivial dual: the unrefined one is the same vector.
    """
    return [F(1) if row_kind(r) == "cap" else F(0) for r in rows]


def n_cap_rows(rows):
    return sum(1 for r in rows if row_kind(r) == "cap")


# ---------------------------------------------------------------- the dual solver

def solve_dual(rows, c, cap_ub=None):
    """min y.b over dual-feasible y.  Returns (value, y) in exact rationals.

    Encoded for `lp200d.solve_max` (which wants `max` over nonneg variables) by splitting the
    free multipliers as `u - v` with `u,v >= 0` and maximising `-(y.b)`.  The result is then
    handed straight back to `verify_dual`, so a bug in this encoding cannot produce a
    certificate that passes: the verifier shares no code with it.

    `cap_ub`, if given, adds `t_ij <= cap_ub` -- used only to keep the search bounded when the
    branch is primal-infeasible and the true dual optimum is -infinity.
    """
    m = len(rows)
    # variable layout: for each row, either one nonneg var (sense `<=`) or a (u,v) pair.
    idx = []
    nv = 0
    for _, sense, _ in rows:
        if sense == "<=":
            idx.append(("+", nv))
            nv += 1
        elif sense == ">=":
            idx.append(("-", nv))
            nv += 1
        else:
            idx.append(("f", nv))
            nv += 2

    def expand(i, coef):
        """Contribution of row i's multiplier, times `coef`, as {var: value}."""
        kind, base = idx[i]
        if kind == "+":
            return {base: coef}
        if kind == "-":
            return {base: -coef}
        return {base: coef, base + 1: -coef}

    drows = []
    ncols = len(c)
    for j in range(ncols):
        coeffs = {}
        for i, (rc, _, _) in enumerate(rows):
            a = rc.get(j)
            if a:
                for k, v in expand(i, a).items():
                    coeffs[k] = coeffs.get(k, F(0)) + v
        coeffs = {k: v for k, v in coeffs.items() if v != 0}
        drows.append((coeffs, ">=", F(c[j])))
    if cap_ub is not None:
        for i, (_, sense, _) in enumerate(rows):
            if sense == "<=":
                kind, base = idx[i]
                drows.append(({base: F(1)}, "<=", F(cap_ub)))
        # free multipliers also need a box or the LP can run away on infeasible branches
        for i, (_, sense, _) in enumerate(rows):
            if sense == "==":
                kind, base = idx[i]
                drows.append(({base: F(1)}, "<=", F(cap_ub)))
                drows.append(({base + 1: F(1)}, "<=", F(cap_ub)))

    obj = [F(0)] * nv
    for i, (_, _, rhs) in enumerate(rows):
        for k, v in expand(i, -F(rhs)).items():
            obj[k] += v

    val, x = solve_max(nv, drows, obj)
    y = []
    for i in range(m):
        kind, base = idx[i]
        if kind == "+":
            y.append(x[base])
        elif kind == "-":
            y.append(-x[base])
        else:
            y.append(x[base] - x[base + 1])
    return -val, y


# ---------------------------------------------------------------- branch bookkeeping

def branch_class(n, comparable, form="slot_eq"):
    """Classify a branch: 'empty' / 'infeasible' / 'zero' / 'positive', with its value.

    'empty'      -- no column survives the comparabilities at all
    'infeasible' -- columns exist but the constraint system has no solution
    'zero'       -- feasible with optimum 0
    'positive'   -- feasible with optimum > 0

    A dual certificate on an 'empty' or 'infeasible' branch is VACUOUS: it bounds a maximum
    over the empty set.  Counting those as evidence of a pattern is PREDICTIONS P12.
    """
    from lp200d import relaxation
    try:
        val, mu = relaxation(n, form, comparable=frozenset(comparable))
    except Infeasible:
        if not branch_columns(n, comparable):
            return "empty", None, None
        return "infeasible", None, None
    return ("positive" if val > 0 else "zero"), val, mu


def all_branches(n):
    prs = pairs_of(n)
    for r in range(len(prs) + 1):
        for comp in combinations(prs, r):
            yield frozenset(comp)


def incomparable(n, comparable):
    return [p for p in pairs_of(n) if p not in comparable]


# ---------------------------------------------------------------- structural helpers

def active_pairs(n, comparable):
    """Incomparable pairs that SOME column of the branch actually flips."""
    seen = set()
    for p in branch_columns(n, comparable):
        seen |= flips(p)
    return sorted(seen)


def consecutive_pairs(n):
    return [(i, i + 1) for i in range(n - 1)]


def descent_stats(n, mu):
    """(E[inv], E[des], E[compAsc], E[incAsc]) for a measure, given the branch is implicit."""
    ei = sum(w * inv_count(p) for p, w in mu.items())
    return ei


# ---------------------------------------------------------------- named certificate tiers
#
# tier 0 is `trivial_dual` above.  These are tiers 1 and 2; see `d1_certificates.py` for
# what the tiering is FOR -- the tier a branch needs is the finding, not the certificate.

def _split_layout(rows):
    """Variable layout for the dual: one nonneg var per `<=` row, a (u,v) pair per `==`."""
    idx, nv = [], 0
    for _, sense, _ in rows:
        if sense == "<=":
            idx.append(("+", nv))
            nv += 1
        else:
            idx.append(("f", nv))
            nv += 2
    return idx, nv


def _expand(idx, i, coef):
    kind, base = idx[i]
    return {base: coef} if kind == "+" else {base: coef, base + 1: -coef}


def _dual_rows(rows, c, idx, nv, fixed=None):
    """Dual feasibility rows over the layout, with `fixed[i]` multipliers substituted out."""
    drows = []
    for j in range(len(c)):
        coeffs, const = {}, F(0)
        for i, (rc, _, _) in enumerate(rows):
            a = rc.get(j)
            if not a:
                continue
            if fixed is not None and fixed[i] is not None:
                const += fixed[i] * a
            else:
                for k, v in _expand(idx, i, a).items():
                    coeffs[k] = coeffs.get(k, F(0)) + v
        drows.append(({k: v for k, v in coeffs.items() if v}, ">=", F(c[j]) - const))
    return drows


def _objective_row(rows, idx, nv, fixed=None):
    """The dual objective `y . b` as (coeff dict over vars, constant)."""
    coeffs, const = {}, F(0)
    for i, (_, _, rhs) in enumerate(rows):
        if not rhs:
            continue
        if fixed is not None and fixed[i] is not None:
            const += fixed[i] * F(rhs)
        else:
            for k, v in _expand(idx, i, F(rhs)).items():
                coeffs[k] = coeffs.get(k, F(0)) + v
    return {k: v for k, v in coeffs.items() if v}, const


def budgeted_dual(rows, c, budget):
    """tier 2: any dual with `y . b <= budget`.  A feasibility LP, not an optimisation."""
    idx, nv = _split_layout(rows)
    drows = _dual_rows(rows, c, idx, nv)
    ocoef, oconst = _objective_row(rows, idx, nv)
    drows.append((ocoef, "<=", F(budget) - oconst))
    try:
        _, x = solve_max(nv, drows, [F(0)] * nv)
    except Infeasible:
        return None
    y = []
    for i in range(len(rows)):
        kind, base = idx[i]
        y.append(x[base] if kind == "+" else x[base] - x[base + 1])
    return y


def cap_pairs_of_branch(n, comparable):
    """The pairs carrying a cap row, in `lp200d.build`'s own emission order."""
    fs = [flips(p) for p in branch_columns(n, comparable)]
    out = []
    for pr in pairs_of(n):
        if pr in comparable:
            continue
        if any(pr in f for f in fs):
            out.append(pr)
    return out


def consecutive_dual(n, comparable, rows, c):
    """tier 1: t := indicator of the consecutive pairs, lambda minimised, s free.

    Returns `y`, or None when no such dual exists at all on this branch (the consecutive-pair
    multipliers then cannot be completed by ANY choice of lambda and s).
    """
    caps = cap_pairs_of_branch(n, comparable)
    fixed = [None] * len(rows)
    ci = 0
    for i, r in enumerate(rows):
        if row_kind(r) == "cap":
            pr = caps[ci]
            ci += 1
            fixed[i] = F(1) if pr[1] == pr[0] + 1 else F(0)
    assert ci == len(caps), f"{ci} cap rows against {len(caps)} cap pairs"
    idx, nv = _split_layout(rows)
    drows = _dual_rows(rows, c, idx, nv, fixed)
    obj = [F(0)] * nv
    for k, v in _expand(idx, 0, F(-1)).items():
        obj[k] += v
    try:
        _, x = solve_max(nv, drows, obj)
    except Infeasible:
        return None
    y = []
    for i in range(len(rows)):
        if fixed[i] is not None:
            y.append(fixed[i])
        else:
            kind, base = idx[i]
            y.append(x[base] if kind == "+" else x[base] - x[base + 1])
    return y
