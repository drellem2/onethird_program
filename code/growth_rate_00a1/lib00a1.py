"""mg-00a1 -- the TRUE GROWTH of the disjunctive per-slot value.

WHAT IS BEING DECIDED, stated so it cannot be over-read.

`mg-131e` refuted `eps_spec = 2/(n+1)` at `n = 6` and named its own successor question,
deliberately unanswered: is the disjunctive per-slot value `c*n + O(1)` (Daniel's route
survives with `c` in place of `1/3`) or superlinear (the route is dead)?  This file answers
it by CONSTRUCTION.

  THEOREM (s1).  For every even `n = 2m >= 4` there is an explicit measure, feasible in the
  disjunctive per-slot relaxation on an explicit TRANSITIVELY CLOSED branch, with

        E[inv] = n(n+5)/36.

  With the trivial dual's `val <= |I_active|/3 <= n(n-1)/6` this pins the growth at
  THETA(n^2).  The answer is SUPERLINEAR and the route is dead.

Two things this file is NOT.

  * It is NOT an upper-bound instrument.  Every value it computes on a NAMED branch is a
    LOWER bound on the maximum over branches (`mg-131e`'s warning, kept).  A lower bound
    that is superlinear settles the growth CLASS from below; the true maximum can only be
    larger, which does not disturb the verdict.  It would disturb a LINEAR verdict, which
    is exactly why this asymmetry is stated at every site.

  * It does NOT touch the frozen-poset conjecture or (LIB).  The disjunctive value is an
    UPPER bound on the object of interest.  Showing an upper bound is bigger than believed
    WEAKENS THE BOUND and says nothing about the statement underneath.  What dies is this
    route as a wall-breaker, not the wall.

The formulation and the row builder are `mg-200d`'s (`lp200d.build`), USED, NOT RE-DERIVED.
The verification path in `s1` contains NO SIMPLEX AT ALL: `lp200d.measure_report` recomputes
mass, flip probabilities, and per-slot symmetry from the measure by direct `Fraction`
arithmetic, and every claim of `s1` is checked against it.
"""

import sys, os
from fractions import Fraction as F
from itertools import product

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "perslot_symmetry_200d"))

from lp200d import (                                    # noqa: E402
    build, flips, inv_count, measure_report, pairs_of, relaxation, Infeasible, solve_max,
)

CAP = F(1, 3)


# ------------------------------------------------------------------ branch bookkeeping

def comparable_from_I(n, I):
    """The branch's comparable set, i.e. the complement of the incomparable set `I`."""
    return frozenset(p for p in pairs_of(n) if p not in I)


def transitive_closure(n, C):
    """Closure of the comparable relation `C` inside the natural order on [n]."""
    C = set(C)
    changed = True
    while changed:
        changed = False
        for (i, k) in list(C):
            for (k2, j) in list(C):
                if k2 == k and (i, j) not in C:
                    C.add((i, j))
                    changed = True
    return frozenset(C)


def is_transitively_closed(n, C):
    return transitive_closure(n, C) == frozenset(C)


def linear_extensions(n, C, limit=None):
    """The branch's COLUMNS: permutations flipping no pair of `C`.

    Generated directly rather than by filtering all `n!`, which is what makes `n >= 10`
    reachable at all.  `selftest00a1` checks it against the brute-force filter.
    """
    preds = [[] for _ in range(n)]
    for (i, j) in C:
        preds[j].append(i)
    out, used, cur = [], [False] * n, []

    def rec():
        if len(cur) == n:
            out.append(tuple(cur))
            return limit is not None and len(out) >= limit
        for x in range(n):
            if used[x] or any(not used[q] for q in preds[x]):
                continue
            used[x] = True
            cur.append(x)
            if rec():
                return True
            cur.pop()
            used[x] = False
        return False

    rec()
    return out


def branch_value_exact(n, I):
    """Exact rational value of the branch with incomparable set `I`.  Raises Infeasible."""
    C = comparable_from_I(n, I)
    keep = linear_extensions(n, C)
    if not keep:
        raise Infeasible("no permutation respects the declared comparabilities")
    perms, rows = build(n, "slot_eq", C, perms=keep)
    val, x = solve_max(len(perms), rows, [F(inv_count(p)) for p in perms])
    return val, {perms[k]: x[k] for k in range(len(perms)) if x[k] != 0}


# ------------------------------------------------------------------ the named families

def consecutive(n):
    """`mg-131e`'s branch: only the `n-1` consecutive pairs are incomparable."""
    return frozenset((i, i + 1) for i in range(n - 1))


def band(n, s):
    """All pairs of span `<= s` incomparable.  `s = 1` is `consecutive`."""
    return frozenset((i, j) for (i, j) in pairs_of(n) if j - i <= s)


def two_chains(a, b):
    """Two disjoint chains `{0..a-1}` and `{a..a+b-1}`: the obvious quadratic-|I| family."""
    C = set()
    for lo, hi in ((0, a), (a, a + b)):
        for i in range(lo, hi):
            for j in range(i + 1, hi):
                C.add((i, j))
    return comparable_from_I(a + b, frozenset()), frozenset(C)


def staircase_I(n):
    """THE FAMILY.  Incomparable set of the staircase two-chain poset, `n = 2m` (or 2m+1).

    Named by hand, not enumerated.  In poset terms: the evens `E = {0,2,..}` are a chain,
    the odds `O = {1,3,..}` are a chain, and

        2k < 2l+1   iff   l >= k+1,        no odd is ever below an even,

    plus, when `n` is odd, a top element `n-1` above everything.  Equivalently the
    incomparable set is the consecutive pairs together with every `(odd i, even j)` chord
    with `j >= i+3` and `j <= 2m-2`.  `|I| = m(m+1)/2` -- QUADRATIC in `n`.
    """
    m = n // 2
    I = set((i, i + 1) for i in range(2 * m - 1))
    for i in range(1, 2 * m, 2):
        for j in range(4, 2 * m - 1, 2):
            if j >= i + 3:
                I.add((i, j))
    return frozenset(I)


# ------------------------------------------------------------------ THE WITNESS

def _cascade(m, t):
    """`A_t`: place `t+1` evens, then alternate odd/even, then the tail.

    In lattice-path coordinates (`R` = next even, `U` = next odd) this is `R^(t+1)` then
    `UR UR ...` until the evens run out, then `U^*`.  `inv(A_t) = t(m-t) + t(t-1)/2`.
    """
    steps, e, o = [], 0, 0
    for _ in range(min(t + 1, m)):
        steps.append("R")
        e += 1
    while o < m:
        steps.append("U")
        o += 1
        if e < m:
            steps.append("R")
            e += 1
    while e < m:
        steps.append("R")
        e += 1
    out, e, o = [], 0, 0
    for s in steps:
        if s == "R":
            out.append(2 * e)
            e += 1
        else:
            out.append(2 * o + 1)
            o += 1
    return tuple(out)


def _fence(m, S):
    """The identity with block `k` (the pair `2k, 2k+1`) transposed for every `k in S`."""
    out = []
    for k in range(m):
        out += [2 * k + 1, 2 * k] if k in S else [2 * k, 2 * k + 1]
    return tuple(out)


def witness(n):
    """THE EXPLICIT FEASIBLE MEASURE.  `E[inv] = n(n+5)/36` for even `n = 2m >= 4`.

    Two parts, and the split is forced rather than tuned:

      CASCADE, total mass 1/3.  `A_1 .. A_{m-1}`, each at `w = 1/(3(m-1))`.  These carry the
      quadratically many chord inversions.  `A_t` and `A_{t-1}` supply the two 2-step routes
      through every corner at diagonal distance `t`, so the cascade balances per-slot
      symmetry AGAINST ITSELF at every distance `>= 2`.

      FENCE, total mass 2/3.  Products of disjoint transpositions of the blocks
      `(2k, 2k+1)`, distributed as `2/3` times a symmetric two-state Markov chain on
      `{in, out}^m` with `P[same as previous] = 1/(m-1)`.  It exists to supply the ONE route
      the cascade cannot -- the `UR` route at diagonal distance 1, which `A_0` would have
      supplied and `A_0` is excluded because it would breach the cap.

    The Markov parameter is not fitted: `P[in] = 1/2` is what distance-0 symmetry forces
    (and it puts the block pairs exactly AT the cap), and `P[out,out] = 1/(2(m-1))` is what
    distance-1 symmetry forces against the cascade weight `w`.  `p = 1/(m-1) <= 1` for every
    `m >= 2`, so the measure is nonnegative at every `n`.

    For ODD `n` the even construction on `[0, n-1)` is used and `n-1` is appended as a top
    element: it is comparable to everything, so it is never flipped and carries no symmetry
    row, and `E[inv] = (n-1)(n+4)/36`.
    """
    if n % 2:
        return {p + (n - 1,): w for p, w in witness(n - 1).items()}
    m = n // 2
    if m < 2:
        raise ValueError("n >= 4")
    mu = {}
    w = F(1, 3 * (m - 1))
    for t in range(1, m):
        key = _cascade(m, t)
        mu[key] = mu.get(key, F(0)) + w
    p = F(1, m - 1)
    for bits in product((0, 1), repeat=m):
        pr = F(1, 2)
        for k in range(1, m):
            pr *= p if bits[k] == bits[k - 1] else 1 - p
        key = _fence(m, frozenset(k for k in range(m) if bits[k]))
        mu[key] = mu.get(key, F(0)) + F(2, 3) * pr
    return {k: v for k, v in mu.items() if v != 0}


def witness_target(n):
    """The closed form the construction attains.  A THEOREM, not a fit -- see the document."""
    return F(n * (n + 5), 36) if n % 2 == 0 else F((n - 1) * (n + 4), 36)


# ------------------------------------------------------------------ arithmetic verification

def verify_measure(n, mu, I):
    """Check a measure against a branch BY DIRECT ARITHMETIC.  No simplex in this path.

    Returns a dict of findings; `ok` is True only if every check passes.  A caller that
    reports a value without consulting `ok` is reporting an unchecked number.
    """
    C = comparable_from_I(n, I)
    rep = measure_report(n, mu)
    flipped = set()
    for p in mu:
        flipped |= flips(p)
    sym_bad = [v for v in rep["slot_eq_violations"] if v[0] in I]
    comp_bad = sorted(flipped & C)
    over_cap = rep["max_flip"] > CAP
    negative = sorted(p for p, v in mu.items() if v < 0)
    return {
        "mass": rep["mass"],
        "E_inv": rep["E_inv"],
        "max_flip": rep["max_flip"],
        "sym_violations_on_I": sym_bad,
        "comparable_pairs_flipped": comp_bad,
        "negative_atoms": negative,
        "atoms": len(mu),
        "ok": (rep["mass"] == 1 and not over_cap and not sym_bad
               and not comp_bad and not negative),
    }


def expected_descents(n, mu):
    """`E[des]`.  Every descent sits on an incomparable pair, and per-slot symmetry forces
    `E[des] = E[asc_I]` with `E[des] + E[asc_I] <= n-1`, so `E[des] <= (n-1)/2` -- `mg-131e`'s
    H6, re-derived not new.  It is recorded here because it shows WHY the obvious linear-
    looking bound was never a bound: `inv >= des` pointwise runs the wrong way, and on the
    witness the two diverge by an unbounded factor.
    """
    tot = F(0)
    for p, w in mu.items():
        tot += w * sum(1 for k in range(n - 1) if p[k] > p[k + 1])
    return tot


def eps_spec(n, e_inv):
    """`mg-200d`'s normalisation: `E[inv_e] <= (eps_spec/6)(n^2-1)`."""
    return 6 * F(e_inv) / (n * n - 1)


def trivial_dual_bound(n, I):
    """`mg-131e`'s H2, a THEOREM: `val <= |I_active|/3`, active = some column flips it.

    This is the whole upper-bound side used here.  It gives `val <= n(n-1)/6` unconditionally,
    which together with `witness` pins the growth at `Theta(n^2)`.
    """
    C = comparable_from_I(n, I)
    keep = linear_extensions(n, C)
    active = set()
    for p in keep:
        active |= flips(p)
    return F(len(active), 3), len(active)
