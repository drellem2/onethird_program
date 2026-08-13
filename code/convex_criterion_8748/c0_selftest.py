#!/usr/bin/env python3
"""c0 — THE CONTROLS, run before anything is claimed.

Five things, and the fifth is the one that matters:

  c0.1  CROSS-CHECK.  `linear_extensions` agrees with `lib0fc6`'s at every labelled poset
        `n <= 5`.  This is the only place in this instrument that reads a prior library, and it
        is read as a SECOND IMPLEMENTATION rather than as a dependency.

  c0.2  THE PROJECTION MACHINERY IS WHAT IT SAYS.  Conditional-expectation matrices are
        symmetric and idempotent in exact rationals, and they average what they claim to.

  c0.3  PLANTED WORLDS FOR THE DETECTOR.  Six partition families whose answer is known by hand
        — nested, nested-in-the-other-order, equal, transverse, transverse-but-agreeing-on-most-
        blocks, and a family nested at one end and transverse at the other.  The detector must
        get all six right, and it must get the TRANSVERSE ones right: a detector that says
        'nested' to everything would pass a suite made only of filtrations.

  c0.4  A WRONG-DIRECTION WORLD.  A family that IS nested, handed to the detector with the
        claim that it is transverse.  The detector must contradict the claim.  Without this the
        suite cannot tell a working detector from one that echoes its input.

  c0.5  THE TWO ROUTES AGREE — the cheap partition-refinement route and the expensive operator
        route `Pi_a Pi_b = Pi_a`.  `PREDICTIONS.md` P3.  THIS IS THE CLAIM THAT THE CRITERION IS
        CHEAP TO CHECK, and if it fails the criterion survives only in its expensive form.
"""
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "compression2_scope_0fc6"))
import lib8748 as L  # noqa: E402

# ---------------------------------------------------------------- c0.1 cross-check

L.banner("c0.1  CROSS-CHECK — L(P) against mg-0fc6's independent library")
try:
    import lib0fc6 as O  # noqa: E402
    mismatch = checked = 0
    for n in (3, 4, 5):
        for lt in L.all_posets(n):
            if set(L.linear_extensions(n, lt)) != set(O.linear_extensions(n, lt)):
                mismatch += 1
            checked += 1
    L.verdict(mismatch == 0 and checked > 0,
              "L(P) agrees with lib0fc6 at every labelled poset n <= 5",
              f"{checked} posets, {mismatch} disagreements")
except ImportError:                                             # pragma: no cover
    L.verdict(False, "lib0fc6 importable for the cross-check",
              "REFUSED — the second implementation is not on the path")

# ---------------------------------------------------------------- c0.2 the machinery

L.banner("c0.2  THE PROJECTION MACHINERY IS WHAT IT SAYS")
parts = [(0, 0, 1, 1, 2, 2), (0, 1, 2, 3, 4, 5), (0, 0, 0, 0, 0, 0), (0, 0, 1, 1, 1, 2)]
ok_sym = ok_idem = True
for p in parts:
    Pi = L.cond_exp_matrix(p)
    ok_sym &= L.is_symmetric(Pi)
    ok_idem &= L.mateq(L.matmul(Pi, Pi), Pi)
L.verdict(ok_sym, "every conditional expectation is symmetric", f"{len(parts)} partitions")
L.verdict(ok_idem, "every conditional expectation is idempotent — exact rationals")
Pi = L.cond_exp_matrix((0, 0, 1, 1, 2, 2))
f = [Fraction(x) for x in (1, 3, 10, 20, 7, 7)]
L.verdict(L.apply_mat(Pi, f) == [Fraction(2), Fraction(2), Fraction(15), Fraction(15),
                                 Fraction(7), Fraction(7)],
          "and it averages over blocks, checked against a hand-computed value")
L.verdict(L.is_projection(L.identity(6)) and not L.is_projection(
    L.lincomb([L.identity(6)], [Fraction(2)])),
          "is_projection accepts I and refuses 2I — the predicate is not constant")

# ---------------------------------------------------------------- c0.3 planted worlds

L.banner("c0.3  PLANTED WORLDS — the detector against six answers known by hand")
WORLDS = [
    ("nested: halves inside quarters",     (0, 0, 0, 0, 1, 1, 1, 1), (0, 0, 1, 1, 2, 2, 3, 3), "a<b"),
    ("nested the other way round",         (0, 0, 1, 1, 2, 2, 3, 3), (0, 0, 0, 0, 1, 1, 1, 1), "b<a"),
    ("equal (relabelled blocks)",          (0, 0, 1, 1, 2, 2, 3, 3), (3, 3, 2, 2, 1, 1, 0, 0), "equal"),
    ("transverse: rows against columns",   (0, 0, 0, 0, 1, 1, 1, 1), (0, 1, 0, 1, 0, 1, 0, 1), "transverse"),
    ("transverse but nearly nested",       (0, 0, 0, 0, 1, 1, 1, 1), (0, 0, 0, 1, 1, 1, 1, 1), "transverse"),
    ("point partition under everything",   (0, 0, 1, 1, 2, 2, 3, 3), tuple(range(8)),          "a<b"),
]
allright = True
for label, a, b, want in WORLDS:
    got = L.nestedness(a, b)
    allright &= (got == want)
    L.verdict(got == want, f"{label}", f"want {want}, got {got}")
L.verdict(sum(1 for *_r, w in WORLDS if w == "transverse") >= 2,
          "and at least two of the worlds are TRANSVERSE — the suite is not all filtrations",
          f"{sum(1 for *_r, w in WORLDS if w == 'transverse')} of {len(WORLDS)}")

# ---------------------------------------------------------------- c0.4 wrong direction

L.banner("c0.4  WRONG-DIRECTION WORLD — a nested family CLAIMED to be transverse")
a = (0, 0, 0, 0, 1, 1, 1, 1)
b = (0, 0, 1, 1, 2, 2, 3, 3)
claim = "transverse"
got = L.nestedness(a, b)
L.verdict(got != claim,
          "the detector CONTRADICTS the claim it was handed", f"claimed {claim}, measured {got}")
L.note("Without this row the suite cannot distinguish a detector from an echo.  It is the",
       "same construction mg-602d's c1 uses for the concepts gate and for the same reason.")

# ---------------------------------------------------------------- c0.5 the two routes

L.banner("c0.5  THE CHEAP ROUTE AND THE EXPENSIVE ROUTE AGREE  (PREDICTIONS.md P3)")


def all_partitions(N):
    """Every set partition of `{0..N-1}` in restricted-growth-string form."""
    out = []
    rgs = [0] * N

    def rec(i, mx):
        if i == N:
            out.append(tuple(rgs))
            return
        for v in range(mx + 1):
            rgs[i] = v
            rec(i + 1, max(mx, v + 1))

    rec(0, 0)
    return out


for N in (4, 5):
    parts = all_partitions(N)
    Pis = {p: L.cond_exp_matrix(p) for p in parts}
    disagree = 0
    nested_cnt = 0
    total = 0
    for a in parts:
        for b in parts:
            total += 1
            cheap = L.refines(a, b)                       # b refines a  <=>  Ran Pi_a ⊆ Ran Pi_b
            Pa, Pb = Pis[a], Pis[b]
            expensive = L.mateq(L.matmul(Pa, Pb), Pa) and L.mateq(L.matmul(Pb, Pa), Pa)
            if cheap != expensive:
                disagree += 1
            nested_cnt += cheap
    L.verdict(disagree == 0,
              f"N={N}: refinement == (Pi_a Pi_b = Pi_b Pi_a = Pi_a) at every ordered pair",
              f"{total} pairs ({len(parts)} partitions), {disagree} disagreements")
    L.verdict(0 < nested_cnt < total,
              f"N={N}: and the predicate is NOT constant on that population",
              f"nested at {nested_cnt} of {total}")

L.note("P3 CONFIRMED at N = 4, 5 EXHAUSTIVE over all set partitions (15 and 52 of them).",
       "The criterion can be checked on the PARTITIONS, in one pass, without ever forming a",
       "matrix — which is the whole content of the claim that it is cheap.  ⚠️ Nothing above",
       "N = 5 is checked here; the equivalence is PROVED (PREDICTIONS.md R2 and c2.4) and",
       "these rows are corroboration, not the warrant.")

sys.exit(L.finish())
