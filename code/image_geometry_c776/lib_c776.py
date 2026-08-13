"""mg-c776 — THE IMAGE OF `P -> pi(Unif(L(P)))` INSIDE THE MARGINAL BODY.  Independent core.

`mg-8b32`'s `C4` states the target: the image is a finite set of points inside a body measured
there to be full-dimensional, and characterising it is what `STATE.md` row 8's *"every route
below 1 must add a realizability fact"* becomes once the fiber-level questions are closed.  This
file is the arithmetic that target needs, re-derived from the definitions.

WHAT IS RE-DERIVED AND WHY.  Nothing here imports `lib0fc6` and nothing OUTSIDE `c0_selftest.py`
imports `lib8b32`.  `c0` imports it deliberately and in one place: two implementations that
share no reasoning agreeing on 238 posets is evidence, and it is the only use of `lib8b32` in
this directory.  The poset enumerator here is a DIFFERENT algorithm from `lib8b32`'s (extension
by a new element against a filter of `3^C(n,2)` states) and the marginal map is a DIFFERENT
algorithm (a forward/backward down-set DP against enumeration of `L(P)`), so `c0`'s agreement is
not two spellings of one routine.

EXACT ARITHMETIC.  Every marginal is a `Fraction` and every count an `int`.  The only floats in
this directory are printed beside the exact statement they illustrate; no verdict reads one.

NOTATION, fixed once and matching `docs/FACTS.md`:

    `P`               a strict partial order on `{0..n-1}`, held as `up[x]` = bitmask of `y > x`
    `L(P)`            its linear extensions, `e(P) = |L(P)|`
    `pi_xy`           `Pr[x before y]` under `Unif(L(P))`; `pi_xy = 1` iff `x <_P y` (mg-8b32 T1)
    `M_n`             the MARGINAL BODY — the image of the simplex on `S_n` under `pi`, i.e. the
                      linear ordering polytope `conv{ pi(delta_sigma) : sigma in S_n }`.
                      `mg-0fc6` writes `M_n(eta)` for a set of MEASURES; the image this ticket
                      asks about lives one level down, among their marginal vectors, and `b4.3`
                      already says "`M_n`'s marginal body".  This file always means the body.
    `R_n`             the IMAGE, `{ pi(Unif(L(P))) : P a poset on n elements }`, a subset of `M_n`
    `delta(P)`        `max_{x || y} min(pi_xy, pi_yx)` — `STATE.md:42`.  `delta < 1/3` is FROZEN
    `d(P)`            the incomparability density `m / C(n,2)`, `m` = number of incomparable pairs
"""

from fractions import Fraction
from itertools import combinations, permutations
import sys

# ------------------------------------------------------------------ posets


def all_posets(n):
    """Every LABELLED strict partial order on `{0..n-1}`, as `up` = tuple of bitmask rows.

    BY EXTENSION, NOT BY FILTERING.  A poset on `[n]` is a poset on `[n-1]` plus a choice of the
    down-set `D` of elements below the new element and the up-set `U` of elements above it, and
    transitivity is EXACTLY: `D` down-closed, `U` up-closed, and `D x U` already in the order.
    Each poset on `[n]` arises from its own restriction to `[n-1]` and from no other, so this is
    a bijection and not a search — which is why it reaches `n = 6` (130 023 posets) where
    filtering `3^15 = 14.3M` triples does not.  Checked against OEIS A001035 in `c0`.
    """
    ps = [(0,)]
    for k in range(2, n + 1):
        ps = _extend(ps, k)
    return ps


def _extend(posets, n):
    out = []
    full = (1 << (n - 1)) - 1
    for up in posets:
        dn = [0] * (n - 1)
        for x in range(n - 1):
            for y in range(n - 1):
                if up[x] >> y & 1:
                    dn[y] |= 1 << x
        for D in range(1 << (n - 1)):
            ok = True
            for x in range(n - 1):
                if D >> x & 1 and (dn[x] & ~D):
                    ok = False
                    break
            if not ok:
                continue
            allowed = full & ~D
            for x in range(n - 1):
                if D >> x & 1:
                    allowed &= up[x]          # every element below the new one is below every
            for U in range(1 << (n - 1)):     # element above it, or transitivity fails
                if U & ~allowed:
                    continue
                bad = False
                for y in range(n - 1):
                    if U >> y & 1 and (up[y] & ~U):
                        bad = True
                        break
                if bad:
                    continue
                new = list(up) + [U]
                for x in range(n - 1):
                    if D >> x & 1:
                        new[x] |= 1 << (n - 1)
                out.append(tuple(new))
    return out


def chain_subrelations(n):
    """Every poset `P` on `{0..n-1}` with `x <_P y  ==>  x < y` numerically.

    THE RESTRICTION IS EXACT, NOT A SAMPLE, and it is `mg-8b32` `b1.3`'s: if `x <_P y` then
    `pi_xy = 1 > 1/2`, so the majority order `L*` — when it is a total order at all — is a linear
    extension of `P`, and relabelling `L*` to the identity puts every poset with a coherent `L*`
    among these.  `c3` VERIFIES that every boundary poset has a coherent `L*` exhaustively at
    `n <= 6` before using the restriction at `n = 7`; it is not assumed.
    """
    out = []
    up = [0] * n
    def rec(x):
        if x < 0:
            out.append(tuple(up))
            return
        cand = list(range(x + 1, n))
        for mask in range(1 << len(cand)):
            u = 0
            for i, y in enumerate(cand):
                if mask >> i & 1:
                    u |= 1 << y
            ok = True
            for y in cand:
                if u >> y & 1 and (up[y] & ~u):
                    ok = False
                    break
            if not ok:
                continue
            up[x] = u
            rec(x - 1)
        up[x] = 0
    rec(n - 1)
    return out


def down_rows(up, n):
    dn = [0] * n
    for x in range(n):
        for y in range(n):
            if up[x] >> y & 1:
                dn[y] |= 1 << x
    return dn


def is_strict_order(up, n):
    for x in range(n):
        if up[x] >> x & 1:
            return False
        for y in range(n):
            if up[x] >> y & 1:
                if up[y] >> x & 1:
                    return False
                if up[y] & ~up[x]:
                    return False
    return True


def linexts(up, n):
    """`L(P)` by direct recursion, as a sorted tuple of permutations.  `c0` checks it against
    filtering all of `S_n`, and the DP below against this."""
    dn = down_rows(up, n)
    out = []
    order = []
    used = 0
    def rec():
        nonlocal used
        if len(order) == n:
            out.append(tuple(order))
            return
        for x in range(n):
            if used >> x & 1 or (dn[x] & ~used):
                continue
            used |= 1 << x
            order.append(x)
            rec()
            order.pop()
            used &= ~(1 << x)
    rec()
    return tuple(sorted(out))


# ------------------------------------------------------------------ the marginal map


def _fg(up, n):
    """Forward/backward down-set counts.  `f[S]` = linear extensions of `P|S` for a down-set `S`;
    `g[S]` = completions of `S` to the whole ground set.  `e(P) = f[full] = g[0]`."""
    dn = down_rows(up, n)
    N = 1 << n
    isdown = bytearray(N)
    for S in range(N):
        ok = 1
        for x in range(n):
            if S >> x & 1 and (dn[x] & ~S):
                ok = 0
                break
        isdown[S] = ok
    f = [0] * N
    g = [0] * N
    f[0] = 1
    for S in range(N):
        if not isdown[S] or not f[S]:
            continue
        for x in range(n):
            if S >> x & 1 or (dn[x] & ~S):
                continue
            f[S | 1 << x] += f[S]
    full = N - 1
    g[full] = 1
    for S in range(full - 1, -1, -1):
        if not isdown[S]:
            continue
        t = 0
        for x in range(n):
            if S >> x & 1 or (dn[x] & ~S):
                continue
            t += g[S | 1 << x]
        g[S] = t
    return isdown, f, g


def e_and_marginals(up, n):
    """`(e(P), pi)` with EVERY ordered pair present, exact.

    `#{sigma in L(P) : y before x}` is summed over the moment `x` is placed: each extension has
    exactly one down-set `S` immediately before `x` enters, so `f[S] * g[S + x]` counts it once
    for every `y` already in `S`.  That is a partition of `L(P)`, so the count is exact and not
    an inclusion-exclusion.  Checked against enumeration of `L(P)` in `c0`.
    """
    isdown, f, g = _fg(up, n)
    dn = down_rows(up, n)
    N = 1 << n
    cnt = {}
    for S in range(N):
        if not isdown[S] or not f[S]:
            continue
        for x in range(n):
            if S >> x & 1 or (dn[x] & ~S):
                continue
            w = f[S] * g[S | 1 << x]
            if not w:
                continue
            for y in range(n):
                if S >> y & 1:
                    cnt[(y, x)] = cnt.get((y, x), 0) + w
    e = f[N - 1]
    pi = {}
    for x in range(n):
        for y in range(n):
            if x != y:
                pi[(x, y)] = Fraction(cnt.get((x, y), 0), e)
    return e, pi


def marg_of_measure(mu, n):
    """`pi` of an arbitrary measure on `S_n` (a dict `permutation -> Fraction`)."""
    pi = {(x, y): Fraction(0) for x in range(n) for y in range(n) if x != y}
    for sig, w in mu.items():
        if not w:
            continue
        pos = [0] * n
        for t, x in enumerate(sig):
            pos[x] = t
        for x, y in pi:
            if pos[x] < pos[y]:
                pi[(x, y)] += w
    return pi


def unif(S):
    S = list(S)
    return {sig: Fraction(1, len(S)) for sig in S}


def forced_poset(pi, n):
    """`P(pi) = {(x,y) : pi_xy = 1}` — mg-8b32's `T1`, cited and used, not re-proved here."""
    up = [0] * n
    for (x, y), v in pi.items():
        if v == 1:
            up[x] |= 1 << y
    return tuple(up)


def retract(pi, n):
    """`r(pi) := pi(Unif(L(P(pi))))` — the map whose FIXED POINTS are the image (`c1`)."""
    return e_and_marginals(forced_poset(pi, n), n)[1]


# ------------------------------------------------------------------ the hypothesis


def incomparable_pairs(up, n):
    return [(x, y) for x, y in combinations(range(n), 2)
            if not (up[x] >> y & 1) and not (up[y] >> x & 1)]


def delta_and_flip(up, n, cap=None):
    """`(delta(P), sum of flips, m)`, with an early abort once `delta` exceeds `cap`.

    THE ABORT IS AN OPTIMISATION AND NOTHING ELSE: `c0` checks the capped and uncapped routes
    agree on every poset at `n <= 5`, because a filter that is the only thing able to see its own
    population is this estate's standing defect (`mg-8b32` §2) and a fast path is exactly where
    it hides.
    """
    e, pi = e_and_marginals(up, n)
    dmax = Fraction(0)
    tot = Fraction(0)
    m = 0
    for x, y in incomparable_pairs(up, n):
        m += 1
        p = pi[(x, y)]
        mn = p if p < 1 - p else 1 - p
        tot += mn
        if mn > dmax:
            dmax = mn
            if cap is not None and dmax > cap:
                return dmax, tot, m
    return dmax, tot, m


def lstar(pi, n):
    """The majority order `L*`, or `None` if the majority tournament is not a total order.
    Reads the marginal vector and nothing else."""
    half = Fraction(1, 2)
    wins = [0] * n
    for x, y in combinations(range(n), 2):
        if pi[(x, y)] > half:
            wins[x] += 1
        elif pi[(x, y)] < half:
            wins[y] += 1
        else:
            return None
    order = sorted(range(n), key=lambda x: -wins[x])
    for i in range(n):
        for j in range(i + 1, n):
            if pi[(order[i], order[j])] <= half:
                return None
    return tuple(order)


def eps_spec(flip_sum, n):
    """`STATE.md` row 8's units: `eps_spec = 6 E[inv_e] / (n^2 - 1)`, and `E[inv_e]` is the sum of
    the flips.  The ceiling on the pair-marginal information set is `n/(n+1)` (`mg-6bc2` Claim
    3.1, `mg-0fc6` `a3.3`), CITED — this directory does not re-derive it."""
    return Fraction(6, 1) * flip_sum / (n * n - 1)


# ------------------------------------------------------------------ points of the body


def rank_over_Q(rows):
    """Exact rank by Gaussian elimination over `Q`.  Used once, in `c3.4`, to decide whether the
    marginal map restricted to `L(P)` has a non-trivial kernel — the same question `lib8b32`'s
    `kernel_basis` answers by a different construction, and deliberately not that code."""
    rows = [list(map(Fraction, r)) for r in rows]
    if not rows:
        return 0
    ncols = len(rows[0])
    r = 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = Fraction(1) / rows[r][c]
        rows[r] = [v * inv for v in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
        if r == len(rows):
            break
    return r


def rand_body_point(rng, n, k):
    """An exact point of `M_n`: a convex combination of `k` permutation vectors with rational
    weights.  Every point of `M_n` is of this form, so this samples the body itself and not a
    proxy for it."""
    perms = list(permutations(range(n)))
    picks = [perms[rng.randrange(len(perms))] for _ in range(k)]
    ws = [rng.randrange(1, 12) for _ in picks]
    tot = sum(ws)
    mu = {}
    for sig, w in zip(picks, ws):
        mu[sig] = mu.get(sig, Fraction(0)) + Fraction(w, tot)
    return mu, marg_of_measure(mu, n)


def linf(pi, rho, n):
    return max(abs(pi[k] - rho[k]) for k in pi)


# ------------------------------------------------------------------ transcript helpers

_FAILED = []


def banner(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


def verdict(ok, label, extra=""):
    print(f"  [{'GREEN' if ok else 'RED  '}] {label}" + (f"   {extra}" if extra else ""))
    if not ok:
        _FAILED.append(label)
    return ok


def note(s):
    print(f"       {s}")


def finish():
    print()
    if _FAILED:
        print(f"RESULT: RED — {len(_FAILED)} check(s) failed")
        for f in _FAILED:
            print(f"  - {f}")
        sys.exit(1)
    print("RESULT: GREEN — all checks passed")
    sys.exit(0)
