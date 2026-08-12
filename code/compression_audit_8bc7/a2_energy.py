"""a2 -- sections 2 and 3 of compression.tex, in exact rational arithmetic.

Section 2:  f|_F = a_F + sum_j c_{B_j} Z_j  with Z_j iid Bernoulli(1/2), hence
            Var(f | C_o) = (1/4) sum_j c_{B_j}^2  with NO covariance terms.
Section 3:  E_o(f) = (2/(n-1)) E Var(f | C_o),   and  (*)  E_BK = (2/(n-1))(EVar_o + EVar_e),
            and  (**) the Rayleigh quotient that follows.

pm-onethird's read is that all of this is correct and that section 3's "exactly" is TRUE
rather than a hidden overclaim.  This arm settles it by computing both sides exactly -- the
left side from the CHAIN (a sum over legal adjacent transpositions, which knows nothing about
cubes) and the right side from the FOLIATIONS -- and comparing them as rationals.  Not a
tolerance: an equality.

The controls matter more than the equalities here.  N3 in particular feeds the same machinery
a DEGREE-2 statistic and requires the identity to BREAK: an identity that also holds off its
stated scope is either trivial or wrongly scoped, and the note's scope line ("exact for every
pair-orientation linear statistic", :152) is exactly what N3 measures.
"""

from fractions import Fraction
from itertools import combinations
import random
import sys

from lib8bc7 import (banner, verdict, gen_posets_exhaustive, random_poset, linear_extensions,
                     groups_o, groups_e, swap_positions, fibers, incomparable_pairs,
                     linear_stat, variance, expected_cond_variance, bk_energy, random_c,
                     legal_at, swap_at)

rng = random.Random(20260812)


def population():
    for n in range(2, 6):
        for lt in gen_posets_exhaustive(n):
            yield (n, lt)
    for n in (6, 7):
        for _ in range(40):
            yield (n, random_poset(n, rng.choice([0.15, 0.3, 0.5]), rng))


def affine_form_check(n, lt, c, vals, LEs, groups):
    """Section 2's first claim, as a set of exact equalities: on each fiber f IS the affine
    function of the block-orientation bits, with the block coefficient equal to c_{B_j}."""
    idx = {L: k for k, L in enumerate(LEs)}
    bad = 0
    for key, members in fibers(LEs, groups).items():
        blocks = []
        for blk in key:
            if len(blk) == 2:
                a, b = blk
                if (a, b) not in lt and (b, a) not in lt:
                    blocks.append((a, b))          # a < b as labels; Z = 1{a before b}
        base = None
        for L in members:
            pos = [0] * n
            for k, v in enumerate(L):
                pos[v] = k
            z = tuple(1 if pos[a] < pos[b] else 0 for (a, b) in blocks)
            if all(t == 0 for t in z):
                base = vals[idx[L]]
        for L in members:
            pos = [0] * n
            for k, v in enumerate(L):
                pos[v] = k
            z = [1 if pos[a] < pos[b] else 0 for (a, b) in blocks]
            want = base + sum(c[(a, b)] * zi for (a, b), zi in zip(blocks, z))
            if vals[idx[L]] != want:
                bad += 1
    return bad


def quarter_sum_check(n, lt, c, vals, LEs, groups, mutate=None):
    """Section 2's boxed claim: Var(f | C = F) = (1/4) sum_{j in D(F)} c_{B_j}^2, fiberwise."""
    idx = {L: k for k, L in enumerate(LEs)}
    bad = 0
    for key, members in fibers(LEs, groups).items():
        m = sum(vals[idx[L]] for L in members) / Fraction(len(members))
        got = sum((vals[idx[L]] - m) ** 2 for L in members) / Fraction(len(members))
        s = Fraction(0)
        for blk in key:
            if len(blk) == 2:
                a, b = blk
                if (a, b) not in lt and (b, a) not in lt:
                    s += c[(a, b)] ** 2
        want = s / 4 if mutate != "N2" else s / 2
        if got != want:
            bad += 1
    return bad


def degree2_stat(n, lt, LEs, pairs, rng):
    """A statistic that is NOT a pair-orientation linear statistic: a product of two
    orientation indicators.  Used by control N3."""
    if len(pairs) < 2:
        return None
    (x1, y1), (x2, y2) = rng.sample(pairs, 2)
    out = []
    for L in LEs:
        pos = [0] * n
        for k, v in enumerate(L):
            pos[v] = k
        out.append(Fraction(1) if (pos[x1] < pos[y1]) and (pos[x2] < pos[y2]) else Fraction(0))
    return out


def main():
    ok = True
    banner("a2.1-a2.5  sections 2 and 3, exact rational equality on both sides")
    nposet = ntest = 0
    bad = {"2.1_affine": 0, "2.2_quarter": 0, "3.1_Eo": 0, "3.2_Ee": 0, "3.3_star": 0,
           "3.4_starstar": 0}
    for n, lt in population():
        LEs = linear_extensions(n, lt)
        pairs = incomparable_pairs(n, lt)
        if not pairs:
            continue
        nposet += 1
        go, ge = groups_o(n), groups_e(n)
        for _ in range(2):
            c = random_c(pairs, rng)
            a = Fraction(rng.randint(-3, 3))
            vals = linear_stat(n, lt, a, c, LEs)
            ntest += 1
            bad["2.1_affine"] += affine_form_check(n, lt, c, vals, LEs, go)
            bad["2.1_affine"] += affine_form_check(n, lt, c, vals, LEs, ge)
            bad["2.2_quarter"] += quarter_sum_check(n, lt, c, vals, LEs, go)
            bad["2.2_quarter"] += quarter_sum_check(n, lt, c, vals, LEs, ge)

            Eo = bk_energy(vals, LEs, n, lt, positions=swap_positions(go))
            Ee = bk_energy(vals, LEs, n, lt, positions=swap_positions(ge))
            Vo = expected_cond_variance(vals, LEs, go)
            Ve = expected_cond_variance(vals, LEs, ge)
            k = Fraction(2, n - 1)
            if Eo != k * Vo:
                bad["3.1_Eo"] += 1
            if Ee != k * Ve:
                bad["3.2_Ee"] += 1
            E = bk_energy(vals, LEs, n, lt)
            if E != k * (Vo + Ve):
                bad["3.3_star"] += 1
            V = variance(vals)
            if V != 0 and E / V != k * (Vo + Ve) / V:
                bad["3.4_starstar"] += 1
    print(f"  {nposet} posets with at least one incomparable pair, {ntest} statistics tested")
    ok &= verdict(bad["2.1_affine"] == 0,
                  "2.1  f|_F = a_F + sum_j c_{B_j} Z_j  on every fiber of both foliations",
                  f"{bad['2.1_affine']} violations")
    ok &= verdict(bad["2.2_quarter"] == 0,
                  "2.2  Var(f|C=F) = (1/4) sum c^2 exactly -- no covariance terms",
                  f"{bad['2.2_quarter']} violations")
    ok &= verdict(bad["3.1_Eo"] == 0, "3.1  E_o(f) = (2/(n-1)) E Var(f|C_o)  EXACTLY",
                  f"{bad['3.1_Eo']} violations")
    ok &= verdict(bad["3.2_Ee"] == 0, "3.2  E_e(f) = (2/(n-1)) E Var(f|C_e)  EXACTLY",
                  f"{bad['3.2_Ee']} violations")
    ok &= verdict(bad["3.3_star"] == 0, "3.3  (*)  E_BK = (2/(n-1))(EVar_o + EVar_e)  EXACTLY",
                  f"{bad['3.3_star']} violations")
    ok &= verdict(bad["3.4_starstar"] == 0, "3.4  (**) the Rayleigh quotient follows",
                  f"{bad['3.4_starstar']} violations")

    banner("a2.C  controls")
    # N1: the constant.  2/(n-1) -> 1/(n-1) must break (*) wherever there is any energy.
    hits = seen = 0
    for n, lt in list(population())[:400]:
        LEs = linear_extensions(n, lt)
        pairs = incomparable_pairs(n, lt)
        if not pairs:
            continue
        seen += 1
        c = random_c(pairs, rng)
        vals = linear_stat(n, lt, Fraction(0), c, LEs)
        E = bk_energy(vals, LEs, n, lt)
        rhs = Fraction(1, n - 1) * (expected_cond_variance(vals, LEs, groups_o(n))
                                    + expected_cond_variance(vals, LEs, groups_e(n)))
        if E != rhs and E != 0:
            hits += 1
    ok &= verdict(hits > 0, "N1  constant 2/(n-1) -> 1/(n-1) breaks (*)", f"{hits}/{seen} posets")

    # N2: (1/4) sum c^2 -> (1/2) sum c^2 must break section 2's boxed identity.
    hits = seen = 0
    for n, lt in list(population())[:400]:
        LEs = linear_extensions(n, lt)
        pairs = incomparable_pairs(n, lt)
        if not pairs:
            continue
        seen += 1
        c = random_c(pairs, rng)
        vals = linear_stat(n, lt, Fraction(0), c, LEs)
        if quarter_sum_check(n, lt, c, vals, LEs, groups_o(n), mutate="N2") > 0:
            hits += 1
    ok &= verdict(hits > 0, "N2  (1/4) sum c^2 -> (1/2) sum c^2 breaks section 2",
                  f"{hits}/{seen} posets")

    # N3: THE SCOPE CONTROL.  A degree-2 statistic must BREAK (*), and must break it in the
    # direction E_BK > RHS -- see a6 for why that direction is a theorem and not an accident.
    broke = same = greater = 0
    for n, lt in list(population())[:600]:
        LEs = linear_extensions(n, lt)
        pairs = incomparable_pairs(n, lt)
        if len(pairs) < 2:
            continue
        vals = degree2_stat(n, lt, LEs, pairs, rng)
        E = bk_energy(vals, LEs, n, lt)
        rhs = Fraction(2, n - 1) * (expected_cond_variance(vals, LEs, groups_o(n))
                                    + expected_cond_variance(vals, LEs, groups_e(n)))
        if E != rhs:
            broke += 1
            if E > rhs:
                greater += 1
        else:
            same += 1
    ok &= verdict(broke > 0,
                  "N3  a DEGREE-2 statistic breaks (*) -- the scope line at :152 is real",
                  f"{broke} broke, {same} still exact, and {greater}/{broke} broke with E_BK > RHS")

    # N4: adding coefficients on COMPARABLE pairs must NOT break anything (those indicators
    # are constants on L(P)).  A control that must refuse to fire.
    hits = seen = 0
    for n, lt in list(population())[:300]:
        LEs = linear_extensions(n, lt)
        pairs = incomparable_pairs(n, lt)
        comp = [(x, y) for x, y in combinations(range(n), 2) if (x, y) in lt or (y, x) in lt]
        if not pairs or not comp:
            continue
        seen += 1
        c = random_c(pairs + comp, rng)
        vals = linear_stat(n, lt, Fraction(0), c, LEs)
        E = bk_energy(vals, LEs, n, lt)
        rhs = Fraction(2, n - 1) * (expected_cond_variance(vals, LEs, groups_o(n))
                                    + expected_cond_variance(vals, LEs, groups_e(n)))
        if E != rhs:
            hits += 1
    ok &= verdict(hits == 0,
                  "N4  coefficients on COMPARABLE pairs do not disturb (*) [REFUSES CORRECTLY]",
                  f"{hits}/{seen} posets broke")

    # N5: SCOPE, not a defect.  The constant 2/(n-1) is tied to the normalization the note
    # states at :106 ("choosing one of the (n-1) adjacent positions uniformly").  Under the
    # lazy variant -- draw a position, then swap with probability 1/2 -- the Dirichlet form
    # halves while E Var(f|C) does not, and the constant becomes 1/(n-1).  Section 3 states
    # its normalization; section 4's (***) reuses P_BK without restating it, so the constant
    # travels only as far as that sentence does.
    hits = seen = 0
    for n, lt in list(population())[:300]:
        LEs = linear_extensions(n, lt)
        pairs = incomparable_pairs(n, lt)
        if not pairs:
            continue
        seen += 1
        c = random_c(pairs, rng)
        vals = linear_stat(n, lt, Fraction(0), c, LEs)
        lazy = bk_energy(vals, LEs, n, lt) / 2          # the lazy chain's Dirichlet form
        rhs = Fraction(1, n - 1) * (expected_cond_variance(vals, LEs, groups_o(n))
                                    + expected_cond_variance(vals, LEs, groups_e(n)))
        if lazy != rhs:
            hits += 1
    ok &= verdict(hits == 0,
                  "N5  under the LAZY normalization the constant is 1/(n-1), not 2/(n-1)",
                  f"{hits}/{seen} posets disagree -- the constant is normalization-dependent")

    print()
    print("a2 VERDICT:", "sections 2 and 3 CONFIRMED" if ok
          else "SECTIONS 2/3 REFUTED OR INSTRUMENT BROKEN")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
