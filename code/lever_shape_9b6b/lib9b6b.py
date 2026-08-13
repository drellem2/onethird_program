#!/usr/bin/env python3
"""mg-9b6b — shared machinery for PRICING THE DENSITY-CEILING DIAL END TO END.

`mg-0b96` priced ONE point of it: a constant ceiling `D = D_needed ≈ 2e-2` is the conjecture on
`{d > D}` and is worth 84 unreached orders.  This directory prices the WHOLE dial, because the
family is not uniform in `D` and the interesting ends are the two `mg-0b96` did not evaluate:

    D = 1 − ⌈(n−1)/2⌉/C(n,2)      the PROVABLE end (F26, kind U) ................ worth nothing
    D = D_needed(n) = ε_dem·(n+1)/n   the ROW 8 end (mg-0b96 §3) ................ worth 84 orders
    D = 4⌊n/3⌋/(n(n−1))           the DATA end (F23, the boundary class) ........ worth ALL orders

Everything is exact `Fraction`.  Nothing here is a measurement ON the frozen class: that class is
empty at every `n` any enumerator reaches, which is the subject of `e2` rather than a caveat on it.

IMPORTS, AND WHAT THAT COSTS.  `lib6ff4` supplies enumeration, `count_ext`, `p_before` and the
canonical form; `lib0b96` supplies `EPS_DEM`, `density` and `d_needed`.  Both are controlled
primitives of this estate and `e0` re-checks the parts this directory's verdicts stand on —
against OEIS A000112, against brute-force enumeration of `L(P)`, and against a hand-built table.
⚠️  THE COST IS NAMED RATHER THAN GLOSSED: `e2`'s agreement with `docs/FACTS.md` F23 is computed
through `lib6ff4`, which is the library `mg-6ff4` measured F23 with.  That agreement is therefore a
CONSISTENCY CHECK ON THIS ARM, NOT AN INDEPENDENT CORROBORATION OF F23, and `e2` says so at the
table.  Where independence would have been the point — `mg-3da1`'s shape — this directory is not
making a second measurement of somebody else's number; it is reading a frontier neither directory
computed, and the shared enumerator moves both readings of it the same way.
"""

import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "code", "boundary_epsilon_6ff4"))
sys.path.insert(0, os.path.join(ROOT, "code", "frozen_density_0b96"))

import lib6ff4 as L                                                       # noqa: E402
import lib0b96 as X                                                       # noqa: E402

THIRD = Fraction(1, 3)
HALF = Fraction(1, 2)
EPS_DEM = X.EPS_DEM                       # 2e-2, mg-e35c's repaired value, imported not re-typed


# ------------------------------------------------------------------------------------------------
# the two coordinates
# ------------------------------------------------------------------------------------------------


def density(n, down):
    """`d(P) = m/C(n,2)`, exact.  Delegates so that no second definition can drift from mg-0b96's."""
    return X.density(n, down)


def delta_exact(n, down):
    """`δ(P) = max over incomparable pairs of min(p, 1−p)`, exact, or `None` for a chain.

    NO EARLY EXIT.  `lib6ff4.delta_at_most` abandons a poset the moment one pair beats a bound,
    which is what makes an `n = 9` frozen sweep affordable and is exactly wrong here: the whole
    subject is the VALUE of `δ` across the population, not its membership of one class."""
    inc = L.incomparable_pairs(n, down)
    if not inc:
        return None
    total = L.count_ext(n, down)
    best = Fraction(0)
    for (i, j) in inc:
        p = L.p_before(n, down, i, j, total)
        b = min(p, 1 - p)
        if b > best:
            best = b
    return best


def table(nmax, classes=None):
    """{n: [(d, δ, is_primitive, down) over every isomorphism class that is not a chain]}, exact.

    A chain has no incomparable pair, so `δ` is not defined on it and `d = 0`; chains are dropped
    and counted separately by the caller rather than folded in at `δ = 0`, which would put a
    fictitious member at the bottom of every envelope.

    COMPUTED ONCE PER ARM.  The `δ` sweep at `n = 8` is most of this suite's wall-clock, and an
    arm that recomputes it per section pays it per section — which is how the first draft of `e1`
    ran for four minutes to print eleven lines."""
    if classes is None:
        classes = L.all_classes(nmax)
    out = {}
    for n in range(2, nmax + 1):
        rows = []
        for down in classes[n]:
            dl = delta_exact(n, down)
            if dl is None:
                continue
            rows.append((density(n, down), dl, L.is_primitive(n, down), down))
        out[n] = rows
    return out


def frontier(tab):
    """{n: [(d, δ)]} — `table`'s first two columns, which is what the two readings consume."""
    return {n: [(d, dl) for (d, dl, _, _) in rows] for n, rows in tab.items()}


# ------------------------------------------------------------------------------------------------
# the two readings of the same table
# ------------------------------------------------------------------------------------------------


def ceiling_at(rows, s, strict=False):
    """`G(s) = max{ d(P) : δ(P) ≤ s }` — the (R)-shaped object: a density ceiling under a BALANCE
    hypothesis.  `strict=True` reads the hypothesis as `δ < s`, which is what `frozen` is.

    Returns `(members, max_d_or_None)`.  `None` means the hypothesis class is EMPTY, which is a
    different answer from `0` and is never printed as one — the distinction is the arm's subject.
    An epsilon-below-`s` threshold would say the same thing at these populations and would be a
    float in the one place this directory cannot afford one."""
    hit = [d for (d, dl) in rows if (dl < s if strict else dl <= s)]
    return len(hit), (max(hit) if hit else None)


def envelope_at(rows, t):
    """`F(t) = min{ δ(P) : d(P) ≥ t }` — the density-to-balance reading, `mg-0b96` §6's `f`.
    Returns `(members, min_delta_or_None)`."""
    hit = [dl for (d, dl) in rows if d >= t]
    return len(hit), (min(hit) if hit else None)


def staircase(rows, reading):
    """The compressed step list of `ceiling_at` / `envelope_at` over the attained thresholds."""
    if reading == "envelope":
        xs = sorted({d for (d, _) in rows})
        f = envelope_at
    else:
        xs = sorted({dl for (_, dl) in rows})
        f = ceiling_at
    steps, prev = [], object()
    for x in xs:
        _, v = f(rows, x)
        if v != prev:
            steps.append((x, v))
            prev = v
    return steps


# ------------------------------------------------------------------------------------------------
# the three ends of the dial
# ------------------------------------------------------------------------------------------------


def d_provable(n):
    """F26's ceiling: `1 − ⌈(n−1)/2⌉/C(n,2)`.  Kind `U`, proved for every finite poset.

    `⌈(n−1)/2⌉` is spelled `n // 2`, which is the same integer at every `n ≥ 1` and needs no
    negative-floor idiom to say so; `e0` T2 checks the two spellings against each other rather
    than letting the identity ride on a comment."""
    return 1 - Fraction(n // 2, n * (n - 1) // 2)


def d_needed(n, eps=EPS_DEM):
    """Row 8's ceiling: `ε_dem·(n+1)/n`.  Delegates to mg-0b96 so the two cannot drift."""
    return X.d_needed(n, eps)


def d_boundary(n):
    """F23's closed form: `max{ d(P) : δ(P) = 1/3 } = 4⌊n/3⌋/(n(n−1))`.

    ⚠️  `FP`, exhaustive `n = 3…9` (mg-6ff4).  Every use of this function ABOVE `n = 9` is an
    EXTRAPOLATION of a closed form, and every arm that does it says so on the line that does it."""
    return Fraction(4 * (n // 3), n * (n - 1))


def eps_sup(n, d):
    """`ε_sup = d·n/(n+1)` (mg-0e8c, STATE.md row 8).  Delegates to mg-0b96."""
    return X.eps_sup(n, d)


def primitive_floor(n):
    """`d ≥ 2/n` — primitivity forces `m ≥ n−1` (STATE.md ledger row 2)."""
    return Fraction(2, n)


# ------------------------------------------------------------------------------------------------
# the statement family, and its two readings
# ------------------------------------------------------------------------------------------------


def one_D(rows, D, beta=THIRD):
    """`(1_D)` at balance threshold `beta`: every `beta`-frozen poset has `d ≤ D`.

    Returns `(hypothesis_members, counterexamples)`.  The hypothesis is `δ < beta` STRICT, which is
    `STATE.md`'s definition of frozen at `beta = 1/3`."""
    hyp = [(d, dl) for (d, dl) in rows if dl < beta]
    return len(hyp), [(d, dl) for (d, dl) in hyp if d > D]


def two_D(rows, D, beta=THIRD):
    """`(2_D)` at balance threshold `beta`: every poset with `d > D` has `δ ≥ beta`."""
    hyp = [(d, dl) for (d, dl) in rows if d > D]
    return len(hyp), [(d, dl) for (d, dl) in hyp if dl < beta]


def s_f(rows, D, beta=THIRD):
    """`S_f` — mg-0b96 §6's escape hatch, at the STEP `f = beta·1[d ≥ D]`: every poset satisfies
    `δ ≥ f(d)`.  The `≥ D` is the whole difference from `two_D`'s `> D` and is one density quantum
    `1/C(n,2)`; `e1` measures that quantum rather than waving at it."""
    return len(rows), [(d, dl) for (d, dl) in rows if d >= D and dl < beta]
