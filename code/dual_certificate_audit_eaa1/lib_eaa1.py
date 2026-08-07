"""mg-eaa1 -- INDEPENDENT audit instrument for mg-131e's dual certificates.

WHAT THIS FILE IS FOR.  mg-131e produced dual certificates for the `<=` direction of
mg-200d's disjunctive per-slot value at n = 3,4,5, and then refuted the conjecture those
certificates existed to support, at n = 6.  This file re-derives the objects from scratch so
that the audit's PASS/FAIL does not run through any line of mg-131e's or mg-200d's code.

SIGN AND ROW CONVENTIONS, FIXED HERE BEFORE mg-131e's CERTIFICATE FORMAT WAS OPENED
(PREDICTIONS P15 guard (i)).  The branch program for a comparable set `C` at size `n` is

    variables   x_p >= 0,  p in K(C) = { permutations flipping no pair of C }
    maximise    sum_p inv(p) x_p
    subject to
      (N)              sum_p x_p                                = 1
      (Q_ij)           sum_{p : p flips (i,j)} x_p             <= 1/3     for (i,j) not in C
                       ... emitted only when some p in K flips (i,j)
      (S_{(x,y),k})    sum_p ( [p has y at k, x at k+1]
                               - [p has x at k, y at k+1] ) x_p = 0       for (x,y) not in C,
                       ... emitted only when the coefficient vector is not identically zero

The dual variable of (N) is `lam` (FREE), of each (Q_ij) is `t_ij >= 0`, of each
(S_{(x,y),k}) is `s_{(x,y),k}` (FREE).  A DUAL CERTIFICATE is a vector `y` over the rows with

    y_i >= 0 on every `<=` row,   y_i free on every `==` row,
    and    sum_i y_i A_ij >= c_j    for EVERY column j.

Its bound is `y . b`.  Soundness, in three lines, so nothing here rests on a library:
    `<=` row, y_i >= 0 :  y_i (A_i x) <= y_i b_i        (x >= 0)
    `==` row, y_i free :  y_i (A_i x)  = y_i b_i
    so  c.x <= sum_j x_j (sum_i y_i A_ij) <= y.b.
This is true whether or not the branch is primal-feasible.  On an infeasible branch it bounds
a maximum over the empty set and certifies NOTHING; `classify_branch` exists so that such
certificates are never counted as evidence.

INDEPENDENCE.  Every combinatorial primitive below (`inv`, `flipped_pairs`, `adjacencies`) is
written here from the definition; the simplex is written here; `verify_dual` is pure Fraction
arithmetic and calls nothing.  `rows_agree_with_lp200d` is the ONE place mg-200d's builder is
touched, and it is touched only to ASSERT that the program I certify is the same program
mg-131e certified -- which is the point of audit check 2.  If that assertion ever failed, my
verdict about mg-131e's numbers would be about a different LP and would be worthless.
"""

from fractions import Fraction as F
from itertools import combinations, permutations

CAP = F(1, 3)


# ------------------------------------------------------------------ combinatorics
# Written from the definitions.  Deliberately not lp200d's formulations.

def positions(p):
    """pos[v] = index of value v in p."""
    pos = [0] * len(p)
    for idx in range(len(p)):
        pos[p[idx]] = idx
    return pos


def inv(p):
    """#{ (i,j) : i < j and p places j before i }, e = identity."""
    pos = positions(p)
    total = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if pos[j] < pos[i]:
                total += 1
    return total


def flipped_pairs(p):
    """The set of pairs (i,j), i<j, that p inverts.  Determines p uniquely."""
    pos = positions(p)
    out = set()
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if pos[j] < pos[i]:
                out.add((i, j))
    return out


def adjacencies(p):
    """Ordered adjacency triples (slot, first, second) for slot = 0 .. n-2."""
    return [(k, p[k], p[k + 1]) for k in range(len(p) - 1)]


def all_pairs(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def footrule(p):
    return sum(abs(k - v) for k, v in enumerate(p))


# ------------------------------------------------------------------ the branch program

def columns(n, C):
    """K(C): the permutations flipping no declared-comparable pair."""
    Cs = frozenset(C)
    return [p for p in permutations(range(n)) if not (flipped_pairs(p) & Cs)]


def columns_consecutive_branch(n):
    """K(C) for the CONSECUTIVE-PAIRS branch, generated directly instead of by filtering n!.

    A permutation flips only pairs (i,i+1) exactly when its inversion set is a set of
    consecutive pairs no two of which overlap -- i.e. it is a product of disjoint adjacent
    transpositions.  (If i<j were flipped with j > i+1 the pair (i,j) is non-consecutive; and
    two overlapping adjacent transpositions compose to a 3-cycle, which flips (i,i+2).)  So
    the columns are indexed by the matchings of the path on n vertices: Fibonacci-many, not
    n!.  `program_consecutive` asserts this against `columns` wherever n! is affordable.
    """
    out = []

    def rec(k, p):
        if k >= n - 1:
            out.append(tuple(p))
            return
        rec(k + 1, p)                     # leave slot k alone
        p[k], p[k + 1] = p[k + 1], p[k]   # or swap it with slot k+1
        rec(k + 2, p)
        p[k], p[k + 1] = p[k + 1], p[k]

    rec(0, list(range(n)))
    return sorted(out)


def program(n, C, cap=CAP, perms=None):
    """(perms, rows, c, labels) for the branch program of comparable set `C`.

    rows are (coeffs: {col -> Fraction}, sense, rhs); labels are parallel and name each row
    ('sum',) / ('cap', pair) / ('sym', pair, slot).  Emission order is: sum, caps in
    all_pairs order, symmetry in (pair, slot) order -- chosen to match lp200d.build so that a
    multiplier vector is index-comparable across the two builders without any re-ordering.
    """
    Cs = frozenset(C)
    if perms is None:
        perms = columns(n, C)
    if not perms:
        return [], [], [], []
    N = len(perms)
    fl = [flipped_pairs(p) for p in perms]
    ad = [set(adjacencies(p)) for p in perms]

    rows, labels = [], []
    rows.append(({j: F(1) for j in range(N)}, "==", F(1)))
    labels.append(("sum",))

    for pr in all_pairs(n):
        if pr in Cs:
            continue
        col = {j: F(1) for j in range(N) if pr in fl[j]}
        if col:
            rows.append((col, "<=", F(cap)))
            labels.append(("cap", pr))

    for (x, y) in all_pairs(n):
        if (x, y) in Cs:
            continue
        for k in range(n - 1):
            coeffs = {}
            for j in range(N):
                v = F(0)
                if (k, y, x) in ad[j]:
                    v += 1
                if (k, x, y) in ad[j]:
                    v -= 1
                if v:
                    coeffs[j] = v
            if coeffs:
                rows.append((coeffs, "==", F(0)))
                labels.append(("sym", (x, y), k))

    c = [F(inv(p)) for p in perms]
    return perms, rows, c, labels


def _canon(perms, rows):
    """Rows keyed by PERMUTATION rather than column index, so two builders can be compared
    without depending on either one's column ordering."""
    out = []
    for coeffs, sense, rhs in rows:
        out.append((tuple(sorted((perms[j], v) for j, v in coeffs.items())), sense, F(rhs)))
    return out


def rows_agree_with_lp200d(n, C, form="slot_eq"):
    """(same_as_multiset, same_in_order, mine, theirs) against mg-200d's own builder.

    This is the ONLY call into mg-200d's code in this audit, and it exists to make audit
    check 2 -- 'is the certified program the right program?' -- answerable rather than
    asserted.  A dual certificate is a certificate FOR A ROW SET; if my row set differed from
    the one mg-131e verified against, nothing I say about their multipliers would transfer.
    """
    import os
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    p200 = os.path.join(here, "..", "perslot_symmetry_200d")
    if p200 not in sys.path:
        sys.path.insert(0, p200)
    from lp200d import build as build200

    mine_perms, mine_rows, _, _ = program(n, C)
    if not mine_perms:
        return None, None, None, None
    keep = [p for p in permutations(range(n)) if not (flipped_pairs(p) & frozenset(C))]
    their_perms, their_rows = build200(n, form, frozenset(C), perms=keep)
    a, b = _canon(mine_perms, mine_rows), _canon(their_perms, their_rows)
    same_multiset = sorted(map(repr, a)) == sorted(map(repr, b))
    same_order = a == b
    return same_multiset, same_order, a, b


# ------------------------------------------------------------------ the dual verifier
# PURE ARITHMETIC.  No simplex is reachable from here.

class Cert:
    def __init__(self, ok, bound, sign_bad, col_bad, ncols):
        self.ok, self.bound = ok, bound
        self.sign_bad, self.col_bad, self.ncols = sign_bad, col_bad, ncols

    def __bool__(self):
        return self.ok

    def __repr__(self):
        return (f"Cert(ok={self.ok}, bound={self.bound}, sign_bad={len(self.sign_bad)}, "
                f"col_bad={len(self.col_bad)}/{self.ncols})")


def verify_dual(rows, c, y):
    """Substitution check of a dual vector against a row set.  Returns a `Cert`."""
    if len(y) != len(rows):
        raise ValueError(f"{len(y)} multipliers for {len(rows)} rows")
    sign_bad = []
    for i, (_, sense, _) in enumerate(rows):
        if sense == "<=" and y[i] < 0:
            sign_bad.append((i, sense, y[i]))
        if sense == ">=" and y[i] > 0:
            sign_bad.append((i, sense, y[i]))
    acc = [F(0)] * len(c)
    for i, (coeffs, _, _) in enumerate(rows):
        if y[i]:
            for j, v in coeffs.items():
                acc[j] += y[i] * v
    col_bad = [(j, acc[j], c[j]) for j in range(len(c)) if acc[j] < c[j]]
    bound = sum(y[i] * rows[i][2] for i in range(len(rows)))
    return Cert(not sign_bad and not col_bad, bound, sign_bad, col_bad, len(c))


def trivial_dual(rows, labels):
    """lam = 0, t = 1 on every cap row, s = 0.  The n-indexed candidate mg-131e names."""
    return [F(1) if lab[0] == "cap" else F(0) for lab in labels]


# ------------------------------------------------------------------ primal substitution

def check_measure(n, mu, C, cap=CAP):
    """Is `mu` a feasible point of the branch program for comparable set `C`?

    Pure arithmetic on the measure itself -- this is the check that makes a LOWER bound
    believable without a solver.  Returns a dict of named booleans plus the diagnostics.
    """
    Cs = frozenset(C)
    mass = sum(mu.values())
    q = {pr: F(0) for pr in all_pairs(n)}
    J = {}
    for p, w in mu.items():
        for pr in flipped_pairs(p):
            q[pr] += w
        for trip in adjacencies(p):
            J[trip] = J.get(trip, F(0)) + w
    e_inv = sum(w * inv(p) for p, w in mu.items())

    def g(k, x, y):
        return J.get((k, x, y), F(0))

    sym_bad = [((x, y), k) for (x, y) in all_pairs(n) if (x, y) not in Cs
               for k in range(n - 1) if g(k, x, y) != g(k, y, x)]
    comp_flipped = sorted(pr for pr in Cs if q[pr] != 0)
    over_cap = sorted(pr for pr in all_pairs(n) if pr not in Cs and q[pr] > cap)
    checks = {
        "nonnegative masses": all(w >= 0 for w in mu.values()),
        "total mass is exactly 1": mass == 1,
        "no comparable pair carries flip mass": not comp_flipped,
        "every incomparable flip probability <= 1/3": not over_cap,
        "per-slot symmetry on every incomparable pair": not sym_bad,
    }
    return {"checks": checks, "ok": all(checks.values()), "E_inv": e_inv, "mass": mass,
            "q": q, "sym_violations": sym_bad, "comparable_flipped": comp_flipped,
            "over_cap": over_cap, "max_flip": max(q.values()) if q else F(0)}


def is_transitive(C):
    """(x<y and y<w) => x<w on the declared comparable set."""
    Cs = set(C)
    return all((x, w) in Cs for (x, y) in Cs for (z, w) in Cs if y == z)


# ------------------------------------------------------------------ exact simplex
# Written here.  Used ONLY to (a) reproduce values and (b) FIND candidate duals.  Nothing
# this audit concludes rests on it: every certificate it produces is then re-checked by
# `verify_dual`, and every measure by `check_measure`, neither of which can see it.

class NoSolution(Exception):
    pass


class Unbounded(Exception):
    pass


def _standardise(nvars, rows):
    """(tableau, basis, ncols, artificials).  b >= 0, slacks then artificials appended."""
    norm = []
    for coeffs, sense, rhs in rows:
        rhs = F(rhs)
        if rhs < 0:
            coeffs = {k: -F(v) for k, v in coeffs.items()}
            rhs, sense = -rhs, {"<=": ">=", ">=": "<=", "==": "=="}[sense]
        norm.append((coeffs, sense, rhs))
    nslack = sum(1 for _, s, _ in norm if s != "==")
    nart = sum(1 for _, s, _ in norm if s != "<=")
    ncols = nvars + nslack + nart
    T, basis, arts = [], [], []
    s_at, a_at = nvars, nvars + nslack
    for coeffs, sense, rhs in norm:
        row = [F(0)] * (ncols + 1)
        for k, v in coeffs.items():
            row[k] = F(v)
        row[-1] = rhs
        if sense == "<=":
            row[s_at] = F(1)
            basis.append(s_at)
            s_at += 1
        elif sense == ">=":
            row[s_at] = F(-1)
            s_at += 1
            row[a_at] = F(1)
            basis.append(a_at)
            arts.append(a_at)
            a_at += 1
        else:
            row[a_at] = F(1)
            basis.append(a_at)
            arts.append(a_at)
            a_at += 1
        T.append(row)
    return T, basis, ncols, set(arts)


def _reduced(T, basis, ncols, cost):
    """Reduced-cost row for a MINIMISATION objective `cost` (length ncols)."""
    z = list(cost) + [F(0)]
    for i, b in enumerate(basis):
        if z[b]:
            f = z[b]
            for j in range(ncols + 1):
                if T[i][j]:
                    z[j] -= f * T[i][j]
    return z


def _run(T, basis, ncols, z, banned):
    """Primal simplex to optimality, Bland's rule (index-smallest entering and leaving)."""
    while True:
        enter = None
        for j in range(ncols):
            if j not in banned and z[j] < 0:
                enter = j
                break
        if enter is None:
            return
        leave, best = None, None
        for i in range(len(T)):
            a = T[i][enter]
            if a > 0:
                r = T[i][-1] / a
                if best is None or r < best or (r == best and basis[i] < basis[leave]):
                    best, leave = r, i
        if leave is None:
            raise Unbounded()
        pv = T[leave][enter]
        if pv != 1:
            T[leave] = [v / pv for v in T[leave]]
        prow = T[leave]
        for i in range(len(T)):
            if i != leave and T[i][enter]:
                f = T[i][enter]
                T[i] = [a - f * b for a, b in zip(T[i], prow)]
        if z[enter]:
            f = z[enter]
            for j in range(ncols + 1):
                if prow[j]:
                    z[j] -= f * prow[j]
        basis[leave] = enter


def lp_max(nvars, rows, c):
    """max c'x over {x >= 0 : rows}.  Returns (value, x).  Raises NoSolution / Unbounded."""
    T, basis, ncols, arts = _standardise(nvars, rows)
    banned = set()
    if arts:
        cost = [F(0)] * ncols
        for j in arts:
            cost[j] = F(1)
        z = _reduced(T, basis, ncols, cost)
        _run(T, basis, ncols, z, banned)
        if -z[-1] != 0:
            raise NoSolution(f"phase-1 residual {-z[-1]}")
        for i, b in enumerate(basis):
            if b in arts:
                piv = next((j for j in range(ncols) if j not in arts and T[i][j] != 0), None)
                if piv is not None:
                    pv = T[i][piv]
                    if pv != 1:
                        T[i] = [v / pv for v in T[i]]
                    prow = T[i]
                    for r in range(len(T)):
                        if r != i and T[r][piv]:
                            f = T[r][piv]
                            T[r] = [a - f * b2 for a, b2 in zip(T[r], prow)]
                    basis[i] = piv
        banned = set(arts)
    cost = [F(0)] * ncols
    for k in range(nvars):
        cost[k] = -F(c[k])
    z = _reduced(T, basis, ncols, cost)
    _run(T, basis, ncols, z, banned)
    x = [F(0)] * nvars
    for i, b in enumerate(basis):
        if b < nvars:
            x[b] = T[i][-1]
    return z[-1], x


def branch_value(n, C):
    """(value, measure) of the branch program, or raise NoSolution."""
    perms, rows, c, _ = program(n, C)
    if not perms:
        raise NoSolution("no column survives the comparabilities")
    val, x = lp_max(len(perms), rows, c)
    return val, {perms[j]: x[j] for j in range(len(perms)) if x[j] != 0}


def classify_branch(n, C):
    """'empty' / 'infeasible' / 'zero' / 'positive', with the value when there is one."""
    if not columns(n, C):
        return "empty", None, None
    try:
        val, mu = branch_value(n, C)
    except NoSolution:
        return "infeasible", None, None
    return ("positive" if val > 0 else "zero"), val, mu


# ------------------------------------------------------------------ finding duals

def _layout(rows):
    """One nonneg variable per `<=` row; a (u,v) split per free row.  Returns (idx, nvars)."""
    idx, nv = [], 0
    for _, sense, _ in rows:
        if sense == "<=":
            idx.append(("+", nv))
            nv += 1
        else:
            idx.append(("f", nv))
            nv += 2
    return idx, nv


def _terms(idx, i, coef):
    kind, base = idx[i]
    return {base: coef} if kind == "+" else {base: coef, base + 1: -coef}


def find_dual(rows, c, budget):
    """A dual `y` that is feasible AND has `y . b <= budget`, or None if none exists.

    A pure FEASIBILITY problem, so it terminates even where the dual optimum is -infinity
    (which is exactly what happens on a primal-infeasible branch).  Anything it returns is
    handed to `verify_dual`, which shares no code with it.
    """
    idx, nv = _layout(rows)
    drows = []
    for j in range(len(c)):
        coeffs = {}
        for i, (rc, _, _) in enumerate(rows):
            a = rc.get(j)
            if a:
                for k, v in _terms(idx, i, a).items():
                    coeffs[k] = coeffs.get(k, F(0)) + v
        drows.append(({k: v for k, v in coeffs.items() if v}, ">=", F(c[j])))
    ocoef = {}
    for i, (_, _, rhs) in enumerate(rows):
        if rhs:
            for k, v in _terms(idx, i, F(rhs)).items():
                ocoef[k] = ocoef.get(k, F(0)) + v
    drows.append(({k: v for k, v in ocoef.items() if v}, "<=", F(budget)))
    try:
        _, x = lp_max(nv, drows, [F(0)] * nv)
    except (NoSolution, Unbounded):
        return None
    y = []
    for i in range(len(rows)):
        kind, base = idx[i]
        y.append(x[base] if kind == "+" else x[base] - x[base + 1])
    return y


def dual_min(rows, c):
    """min y.b over dual-feasible y.  Raises Unbounded when the primal is infeasible."""
    idx, nv = _layout(rows)
    drows = []
    for j in range(len(c)):
        coeffs = {}
        for i, (rc, _, _) in enumerate(rows):
            a = rc.get(j)
            if a:
                for k, v in _terms(idx, i, a).items():
                    coeffs[k] = coeffs.get(k, F(0)) + v
        drows.append(({k: v for k, v in coeffs.items() if v}, ">=", F(c[j])))
    obj = [F(0)] * nv
    for i, (_, _, rhs) in enumerate(rows):
        if rhs:
            for k, v in _terms(idx, i, -F(rhs)).items():
                obj[k] += v
    val, x = lp_max(nv, drows, obj)
    y = []
    for i in range(len(rows)):
        kind, base = idx[i]
        y.append(x[base] if kind == "+" else x[base] - x[base + 1])
    return -val, y


def all_branches(n):
    prs = all_pairs(n)
    for r in range(len(prs) + 1):
        for comp in combinations(prs, r):
            yield frozenset(comp)


def active_pairs(n, C, perms=None):
    """Incomparable pairs some surviving column actually flips -- the ones carrying a cap."""
    seen = set()
    for p in (columns(n, C) if perms is None else perms):
        seen |= flipped_pairs(p)
    return sorted(pr for pr in seen if pr not in frozenset(C))


def consecutive(n):
    return [(i, i + 1) for i in range(n - 1)]


def fence(n):
    """mg-200d's 3-atom lower-bound construction, rebuilt from its description:
    identity, the even-index adjacent matching, and the odd-index adjacent matching."""
    def matching(start):
        p = list(range(n))
        for k in range(start, n - 1, 2):
            p[k], p[k + 1] = p[k + 1], p[k]
        return tuple(p)
    atoms = [tuple(range(n)), matching(1), matching(0)]
    return {a: F(1, 3) for a in atoms}


def uniform_linear_extensions(n, relation):
    """Uniform measure on the linear extensions of ONE named relation.  A control only --
    no poset is enumerated and no transitivity is imposed anywhere in this audit."""
    lin = [p for p in permutations(range(n))
           if all(positions(p)[x] < positions(p)[y] for (x, y) in relation)]
    if not lin:
        return {}
    w = F(1, len(lin))
    return {p: w for p in lin}


def eps_spec(n, e_inv):
    """The architecture's normalisation: E[inv_e] <= (eps_spec/6)(n^2 - 1)."""
    return 6 * F(e_inv) / (n * n - 1)
