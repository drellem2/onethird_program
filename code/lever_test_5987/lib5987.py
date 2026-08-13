#!/usr/bin/env python3
"""mg-5987 — shared machinery for RUNNING mg-9b6b's THREE-STEP LEVER TEST ON `(B-cov)` AND `(EQ)`.

`mg-9b6b` priced the density dial end to end and closed residual `(R)` as a lever.  Its test is
three steps and it is mechanical enough to run on any candidate:

    1. is the hypothesis `frozen`?  then the population is empty at every reachable `n`;
    2. does it imply the target on a class?  then it is the conjecture restricted, and the price
       is the orders it delivers;
    3. if it is a graded family, what does the WHOLE dial do?

This directory runs it on the two residuals `mg-9b6b` §8 left untouched:

    (B-cov)_C   frozen  ⟹  Σ_x C_x ≤ C · E[inv_e]        C_x = Σ_{y≠z} Cov(s_xy, s_xz)
    (EQ)_C      frozen  ⟹  max_x |E[pos_σ x] − rank_e x| ≤ C

Both are frozen-conditional, so step 1 applies to both at once and the interesting outcome is at
steps 2 and 3.  THE PRICE IS COMPUTED IN THE SAME CURRENCY `mg-9b6b` USED — orders of the
conjecture delivered by the contrapositive — so the three residuals can be read off one table.

⚠️  THE ONE COORDINATE THAT IS NOT HYPOTHESIS-FREE, AND IT IS WHY THIS DIRECTORY HAS A READING
    ARGUMENT WHERE `mg-9b6b` HAD NONE.  `d(P)` is defined at every poset, so `mg-0b96` and
    `mg-9b6b` could evaluate the `(1_D)` dial off the frozen class without choosing anything.
    `(EQ)` and `(B-cov)` both name `e`, and `STATE.md`'s glossary defines `e` as *the >2/3-majority
    order* — which is total exactly when `δ(P) ≤ 1/3`, i.e. exactly on the class that is empty.
    So off-class the reference order is a CHOICE, and `STATE.md`'s own `λ_std` row records that the
    choice is load-bearing (`λ_std` moves by up to `1/3` across reference orders, mg-c4f5).  Every
    reading is therefore priced here rather than one being assumed: `g1` measures the envelope over
    ALL reference orders, and every verdict is stated at the end of the envelope that is most
    favourable to the lever.

IMPORTS, AND WHAT THAT COSTS.  `lib6ff4` supplies enumeration, `count_ext`, `p_before`,
`majority_order` and the canonical form; `lib0b96` supplies `EPS_DEM` and `density`; `lib9b6b`
supplies `d_needed` and `primitive_floor`, so the `(R)` control column is computed by the library
that published the figure it reproduces and is a CONSISTENCY CHECK ON THIS ARM rather than an
independent corroboration of `mg-9b6b`.  `g0` re-checks every imported primitive this directory's
verdicts stand on — against OEIS A000112, against brute-force enumeration of `L(P)`, and against a
hand table — because an import whose controls live in another directory is unchecked from here.
"""

import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "code", "boundary_epsilon_6ff4"))
sys.path.insert(0, os.path.join(ROOT, "code", "frozen_density_0b96"))
sys.path.insert(0, os.path.join(ROOT, "code", "lever_shape_9b6b"))

import lib6ff4 as L                                                       # noqa: E402
import lib0b96 as X                                                       # noqa: E402
import lib9b6b as V                                                       # noqa: E402

THIRD = Fraction(1, 3)
TWO_THIRDS = Fraction(2, 3)
EPS_DEM = X.EPS_DEM                       # 2e-2, mg-e35c's repaired value, imported not re-typed


# ------------------------------------------------------------------------------------------------
# the joint law of the pair indicators — everything below is a function of these
# ------------------------------------------------------------------------------------------------


def density(n, down):
    """`d(P) = m/C(n,2)`.  Delegates to mg-0b96 so no second definition can drift from the one
    `(R)`'s whole price was computed with — this directory's `(R)` column has to be comparable."""
    return X.density(n, down)


def joint_before(n, down, y, z, x, total):
    """`Pr[y ≺_σ x and z ≺_σ x]`, exact, WITHOUT enumerating `L(P)`.

    Adds `y < x` and then `z < x` by transitive closure and counts extensions of the result.  The
    second addition needs a case split that is easy to get wrong and is the reason this is a
    function rather than two lines at the call site: adding `y < x` can make `z` COMPARABLE to `x`
    (exactly when `z ≤ y`), and calling `_closure_with` on a comparable pair is out of contract."""
    d = down
    for w in (y, z):
        if L.is_below(d, w, x):
            continue                                   # already forced — contributes no constraint
        if L.is_below(d, x, w):
            return Fraction(0)                         # forced the other way — the event is empty
        d = L._closure_with(n, d, w, x)
    return Fraction(L.count_ext(n, d), total)


def profile(n, down):
    """Everything the two residuals are functions of, exact, at one poset.

    Returns a dict with

        total   |L(P)|
        inc     {x: [y ∥ x]}
        p       {(y,x): Pr[y ≺_σ x]} over ordered incomparable pairs
        h       [E[pos_σ x]] — 1-indexed positions, so `Σ h = n(n+1)/2`
        diag    [Σ_{y ∥ x} p(1−p)] — the variance DIAGONAL, `mg-dcae`'s free term under (H)
        C       [C_x = Σ_{y≠z} Cov(s_xy, s_xz)] — `docs/FACTS.md` F11's same-side covariance
        var     [Var(pos_σ x)] = diag + C, by the definition of the two summands

    `s_xy = 1[y ≺_σ x]`, so `pos_σ(x) = 1 + Σ_{y≠x} s_xy` and the decomposition is the ordinary
    variance-of-a-sum.  COMPARABLE `y` CONTRIBUTE NOTHING: `s_xy` is then constant, so its variance
    and all its covariances vanish — which is why both sums run over `inc[x]` alone and not over
    all `y`, and `g0` checks that reduction against a brute-force `L(P)` sweep rather than trusting
    it."""
    total = L.count_ext(n, down)
    inc = {x: [y for y in range(n) if y != x and not L.comparable(down, x, y)] for x in range(n)}
    p = {}
    for x in range(n):
        for y in inc[x]:
            p[(y, x)] = L.p_before(n, down, y, x, total)
    h, diag, C = [], [], []
    for x in range(n):
        below = sum(1 for y in range(n) if y != x and L.is_below(down, y, x))
        h.append(Fraction(1 + below) + sum(p[(y, x)] for y in inc[x]))
        diag.append(sum(p[(y, x)] * (1 - p[(y, x)]) for y in inc[x]))
        c = Fraction(0)
        for i, y in enumerate(inc[x]):
            for z in inc[x][i + 1:]:
                c += 2 * (joint_before(n, down, y, z, x, total) - p[(y, x)] * p[(z, x)])
        C.append(c)
    return dict(total=total, inc=inc, p=p, h=h, diag=diag, C=C,
                var=[diag[x] + C[x] for x in range(n)])


# ------------------------------------------------------------------------------------------------
# reference orders — the choice `mg-9b6b` never had to make
# ------------------------------------------------------------------------------------------------


def rank_of(ext):
    """1-indexed rank vector of a linear extension given in position order."""
    r = [0] * len(ext)
    for pos, v in enumerate(ext):
        r[v] = pos + 1
    return r


def barycentric(n, h):
    """The reference order that sorts by `h(x) = E[pos_σ x]`, ties broken by label.

    IT IS ALWAYS A LINEAR EXTENSION: `x < y` in `P` forces `h(x) < h(y)`, because every extension
    puts `x` before `y`.  It is defined at every poset, which is exactly what the majority order is
    not, and `g1` measures — rather than asserts — that it is also the reading MOST FAVOURABLE to
    both levers, i.e. the one minimising the bias over all reference orders."""
    return tuple(sorted(range(n), key=lambda x: (h[x], x)))


def majority_reference(n, down, prof, beta=THIRD):
    """(e, fully_decided) for `STATE.md`'s own `e` — the majority order at threshold `1 − β`.

    `fully_decided` is True iff EVERY incomparable pair is `(1−β)`-decided, which at `β = 1/3` is
    `δ(P) ≤ 1/3` verbatim.  That equivalence is the whole of step 1 in one line: the notation
    `rank_e` refers only where the hypothesis holds, so the glossary's *"reference, not a choice"*
    is a statement ABOUT THE FROZEN CLASS and becomes a choice the moment anybody evaluates it
    anywhere a census can go.

    PARAMETRISED RATHER THAN CALLED THROUGH `lib6ff4.majority_order`, which hard-codes `2/3`,
    because `g0`'s wrong-direction control needs the SAME construction on a class that is not
    empty — and `g0` §10 checks that at `β = 1/3` this returns `lib6ff4`'s answer exactly, so the
    parametrisation is not a second definition that can drift from the estate's."""
    adj = [[i != j and L.is_below(down, i, j) for j in range(n)] for i in range(n)]
    unori = 0
    for (x, y) in L.incomparable_pairs(n, down):
        p = prof["p"][(x, y)]
        if max(p, 1 - p) >= 1 - beta:
            if p >= 1 - p:
                adj[x][y] = True
            else:
                adj[y][x] = True
        else:
            unori += 1
    indeg = [sum(1 for i in range(n) if adj[i][j]) for j in range(n)]
    order, avail = [], [j for j in range(n) if indeg[j] == 0]
    while avail:
        j = min(avail)
        avail.remove(j)
        order.append(j)
        for k in range(n):
            if adj[j][k]:
                indeg[k] -= 1
                if indeg[k] == 0:
                    avail.append(k)
    return (tuple(order) if len(order) == n else None), (unori == 0)


def e_inv(n, down, rank, prof):
    """`E[inv_e(σ)]` — expected incomparable pairs flipped against the reference given by `rank`."""
    tot = Fraction(0)
    for a in range(n):
        for b in range(a + 1, n):
            if L.comparable(down, a, b):
                continue
            tot += prof["p"][(b, a)] if rank[a] < rank[b] else prof["p"][(a, b)]
    return tot


# ------------------------------------------------------------------------------------------------
# the two residuals, as numbers
# ------------------------------------------------------------------------------------------------


def bias(n, prof, rank):
    """`(EQ)`'s quantity at one poset and one reference: `max_x |E[pos_σ x] − rank_e x|`."""
    return max(abs(prof["h"][x] - rank[x]) for x in range(n))


def cov_total(prof):
    """`(B-cov)`'s numerator `Σ_x C_x`.  REFERENCE-FREE — this is the half of `(B-cov)` that can be
    evaluated without choosing anything, and the reading argument touches only its denominator."""
    return sum(prof["C"])


def rho(n, down, prof, rank):
    """`(B-cov)`'s quantity: `Σ_x C_x / E[inv_e]`.  `None` at a chain, where the denominator is 0."""
    den = e_inv(n, down, rank, prof)
    return None if den == 0 else cov_total(prof) / den


def envelope(n, down, prof, quantity):
    """(min, argmin-is-barycentric, max) of a per-reference quantity over ALL linear extensions.

    Controls only, and quadratic in `|L(P)|` by design: the point of the envelope is that no
    reading can escape it, so it must be taken over the whole set rather than over a shortlist."""
    lo = hi = None
    lo_at_bary = False
    bary = barycentric(n, prof["h"])
    for ext in L.linear_extensions(n, down):
        v = quantity(rank_of(ext))
        if v is None:
            continue
        if lo is None or v < lo:
            lo, lo_at_bary = v, (ext == bary)
        elif v == lo and ext == bary:
            lo_at_bary = True
        if hi is None or v > hi:
            hi = v
    return lo, lo_at_bary, hi


# ------------------------------------------------------------------------------------------------
# the population
# ------------------------------------------------------------------------------------------------


def primitives(classes, n):
    """Non-chain primitive isomorphism classes at order `n`.

    WHY PRIMITIVE IS THE RIGHT POPULATION AND NOT A CONVENIENCE: a minimal counterexample is
    primitive (`STATE.md` glossary), so *the conjecture at order `n`, given it below `n`* has to be
    proven only over the primitives — which is exactly what makes `mg-9b6b`'s orders currency
    meaningful, and is why `mg-9b6b` priced `(1_D)` against `primitive_floor` rather than against
    the whole population.  `g2` prices over BOTH populations so the choice is visible."""
    return [d for d in classes[n] if L.incomparable_pairs(n, d) and L.is_primitive(n, d)]


def non_chains(classes, n):
    return [d for d in classes[n] if L.incomparable_pairs(n, d)]


# ------------------------------------------------------------------------------------------------
# the explicit family — a closed form, at every `n`, and not a census
# ------------------------------------------------------------------------------------------------


def zigzag(n):
    """`Z_n`: `x_i < x_j` iff `j − i ≥ 2`.  The incomparable pairs are exactly the consecutive ones.

    PRIMITIVE AT EVERY `n ≥ 2`: its incomparability graph is the path `x_1 — x_2 — … — x_n`, which
    is connected, and `STATE.md`'s glossary makes connectedness of that graph the definition.  This
    is the family that carries every verdict in this directory past the reachable population, in
    exactly the role `mg-9b6b` §3's ordinal sums played there — with the difference that ordinal
    sums are NOT primitive, which is the objection `mg-f5be` raised and `mg-9b6b` conceded.  This
    family is immune to it."""
    return tuple(sum(1 << k for k in range(n) if i - k >= 2) for i in range(n))


def fib(k, _memo={0: 0, 1: 1}):
    """`F_0 = 0`, `F_1 = 1`.  Iterative, exact, memoised."""
    if k not in _memo:
        a, b = _memo[max(_memo)], None
        for j in range(max(_memo) + 1, k + 1):
            _memo[j] = _memo[j - 1] + _memo[j - 2]
    return _memo[k]


def zigzag_closed_form(n):
    """The whole profile of `Z_n` in closed form, WITHOUT any poset machinery.

    `L(Z_n)` is in bijection with the matchings of the path on `n` vertices: the only incomparable
    pairs are consecutive, so a linear extension is the identity with a set of PAIRWISE
    NON-ADJACENT adjacent transpositions applied.  Hence

        |L(Z_n)| = F_{n+1},   q_i = Pr[the pair (i, i+1) is transposed] = F_i · F_{n−i} / F_{n+1}

    with `q_0 = q_n = 0`, and then everything else is arithmetic in the `q`:

        h(x_i) − i = q_i − q_{i−1}                     so the barycentric order is the identity
        C_{x_i}   = 2 · q_i · q_{i−1}                  ⟹  Σ_x C_x = 2 Σ_i q_i q_{i−1}
        E[inv_e]  = Σ_i q_i

    `C_{x_i} = 2 q_i q_{i−1}` is worth its own line because it DERIVES the FKG/XYZ sign instead of
    measuring it: the two events *`(i−1,i)` untransposed* and *`(i,i+1)` transposed* satisfy the
    second implying the first, so the covariance is `q_i(1 − (1 − q_{i−1})) = q_i q_{i−1} ≥ 0` —
    `docs/FACTS.md` F11's *"`C_x > 0` at 555 of 555"* with a reason attached, on a family F11's
    population does not reach.  `g0` checks this whole function against `profile()` term by term."""
    q = [Fraction(0)] + [Fraction(fib(i) * fib(n - i), fib(n + 1)) for i in range(1, n)] \
        + [Fraction(0)]
    b = [q[i] - q[i - 1] for i in range(1, n + 1)]
    C = [2 * q[i] * q[i - 1] for i in range(1, n + 1)]
    return dict(ext=fib(n + 1), q=q, bias=max(abs(v) for v in b),
                cov=sum(C), inv=sum(q), rho=sum(C) / sum(q))


def antichain(n):
    """`A_n`, the family that makes both hypotheses load-bearing rather than decorative."""
    return tuple(0 for _ in range(n))


def antichain_closed_form(n):
    """`A_n` in closed form: `bias = (n−1)/2`, `ρ = (n−2)/3`, both UNBOUNDED.

        pos_σ(x) is uniform on {1..n}   ⟹   h ≡ (n+1)/2,  Var = (n²−1)/12
        rank_e x = the label            ⟹   max_x |h − rank| = (n−1)/2
        diag_x = (n−1)/4                ⟹   C_x = (n²−1)/12 − (n−1)/4 = (n−1)(n−2)/12
        E[inv_e] = C(n,2)/2             ⟹   ρ = (n−2)/3

    Every reference order gives the same bias, because `h` is constant and any rank vector is a
    permutation of `1..n` — so this witness does NOT depend on the reading argument, which is the
    only reason step 1 can be settled before step 2 chooses one."""
    return dict(bias=Fraction(n - 1, 2), rho=Fraction(n - 2, 3),
                cov=Fraction(n * (n - 1) * (n - 2), 12), inv=Fraction(n * (n - 1), 4))


# ------------------------------------------------------------------------------------------------
# the price, in `mg-9b6b`'s currency
# ------------------------------------------------------------------------------------------------


def delivers(floor_by_n, C):
    """Orders whose WHOLE primitive population is settled by the contrapositive at dial value `C`.

    `floor_by_n[n]` is `min{ Q(P) : P primitive non-chain at order n }` for the residual's own
    quantity `Q`.  The statement *`frozen ⟹ Q ≤ C`* is by contraposition *`Q > C ⟹ the conjecture
    at P`*, so it delivers order `n` outright exactly when every primitive at `n` has `Q > C`."""
    return sorted(n for n, f in floor_by_n.items() if f > C)


def coverage(values, C):
    """(settled, population) at dial value `C` — the REFINEMENT `mg-9b6b`'s counter cannot make.

    The orders counter is binary per order and returns 0 both for a statement that settles nothing
    and for one that settles all but a single poset at every order.  Those are not the same object
    and the difference is the whole question this directory was filed to answer, so the fraction is
    reported beside the count everywhere."""
    return sum(1 for v in values if v is not None and v > C), len(values)
