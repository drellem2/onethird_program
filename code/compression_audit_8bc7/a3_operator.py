"""a3 -- section 4 of compression.tex, and mg-8bc7's question (B).

(***) at :192 reads   (I - P_BK) f = (2/(n-1)) (2I - Pi_o - Pi_e) f   "for a linear statistic".

pm-onethird's worry: Pi_o f sends the incomparable-block coefficients to 1/2 and is not
obviously a pair-orientation linear statistic again, so if V (the linear-statistic subspace)
is not invariant then (***) is a statement about a QUADRATIC FORM on V and not an operator
identity, and section 4's "small eigenvalues of 2I - Pi_o - Pi_e" would then be about the
full space rather than the one the reduction licenses.

This arm separates the three questions the worry runs together:

  3.1  is (***) a pointwise identity of FUNCTIONS on V, or only an equality of quadratic
       forms?  (Pointwise is strictly stronger, and it is what is checked here -- exactly.)
  3.2  is V invariant under Pi_o, Pi_e, M = 2I - Pi_o - Pi_e, or (I - P_BK)?
  3.3  the smallest certificate of non-invariance, exhibited in full rather than counted.
  3.4  the spectral consequence: three Rayleigh minima measured and ordered --
         (2/(n-1)) lam_2(M)  [full space]   <=   lam_2(I - P_BK)  [full space]
                                            <=   min over V_0     [what the reduction licenses]
       Which of these section 4's phrase names, and whether the direction is the useful one.

Eigenvalues here are floats from the Jacobi routine in lib8bc7 and are MEASUREMENTS.  Every
VERDICT row (3.1, 3.2, 3.3) is decided in exact rational arithmetic.
"""

from fractions import Fraction
import random
import sys

from lib8bc7 import (banner, verdict, gen_posets_exhaustive, random_poset, linear_extensions,
                     groups_o, groups_e, fibers, incomparable_pairs, linear_stat, variance,
                     cond_expectation, bk_apply, random_c, in_span, legal_at, swap_at,
                     jacobi_eigenvalues, gen_eig_min, expected_cond_variance, bk_energy)

rng = random.Random(4041999)


def basis_V(n, lt, LEs):
    """A spanning set for V: the constant and the |I(P)| orientation indicators."""
    pairs = incomparable_pairs(n, lt)
    B = [[Fraction(1)] * len(LEs)]
    for (x, y) in pairs:
        col = []
        for L in LEs:
            pos = [0] * n
            for k, v in enumerate(L):
                pos[v] = k
            col.append(Fraction(1) if pos[x] < pos[y] else Fraction(0))
        B.append(col)
    return B, pairs


def pi_matrix(LEs, groups):
    idx = {L: k for k, L in enumerate(LEs)}
    N = len(LEs)
    Mx = [[Fraction(0)] * N for _ in range(N)]
    for key, fib in fibers(LEs, groups).items():
        w = Fraction(1, len(fib))
        for L in fib:
            for L2 in fib:
                Mx[idx[L]][idx[L2]] = w
    return Mx


def bk_matrix(LEs, n, lt):
    idx = {L: k for k, L in enumerate(LEs)}
    N = len(LEs)
    Mx = [[Fraction(0)] * N for _ in range(N)]
    for L in LEs:
        i0 = idx[L]
        for i in range(n - 1):
            L2 = swap_at(L, i) if legal_at(L, i, lt) else L
            Mx[i0][idx[L2]] += Fraction(1, n - 1)
    for i in range(N):
        for j in range(N):
            Mx[i][j] = -Mx[i][j]
        Mx[i][i] += 1
    return Mx


def population(nmax=5, samples=(6,)):
    for n in range(2, nmax + 1):
        for lt in gen_posets_exhaustive(n):
            yield (n, lt)
    for n in samples:
        for _ in range(40):
            yield (n, random_poset(n, rng.choice([0.15, 0.3, 0.5]), rng))


def main():
    ok = True

    banner("a3.1  is (***) a POINTWISE identity on V, or only a quadratic form?")
    ptwise_bad = form_bad = 0
    ntest = 0
    for n, lt in population():
        LEs = linear_extensions(n, lt)
        pairs = incomparable_pairs(n, lt)
        if not pairs:
            continue
        go, ge = groups_o(n), groups_e(n)
        for _ in range(2):
            c = random_c(pairs, rng)
            vals = linear_stat(n, lt, Fraction(rng.randint(-3, 3)), c, LEs)
            ntest += 1
            lhs = bk_apply(vals, LEs, n, lt)
            po = cond_expectation(vals, LEs, go)
            pe = cond_expectation(vals, LEs, ge)
            k = Fraction(2, n - 1)
            rhs = [k * (2 * f - a - b) for f, a, b in zip(vals, po, pe)]
            if lhs != rhs:
                ptwise_bad += 1
            # the weaker reading, for contrast: equality of the quadratic forms only
            N = len(LEs)
            q1 = sum(f * g for f, g in zip(vals, lhs)) / Fraction(N)
            q2 = sum(f * g for f, g in zip(vals, rhs)) / Fraction(N)
            if q1 != q2:
                form_bad += 1
    ok &= verdict(ptwise_bad == 0,
                  "(***) holds POINTWISE as an equality of functions, for every linear f",
                  f"{ptwise_bad}/{ntest} violations")
    ok &= verdict(form_bad == 0, "(***) therefore also holds as a quadratic form on V",
                  f"{form_bad}/{ntest} violations")

    banner("a3.2  is V invariant?  Pi_o V, Pi_e V, M V, (I-P_BK) V  vs  V")
    counts = {"Pi_o": [0, 0], "Pi_e": [0, 0], "M": [0, 0], "I-P_BK": [0, 0]}
    for n, lt in population(nmax=5, samples=()):
        LEs = linear_extensions(n, lt)
        pairs = incomparable_pairs(n, lt)
        if not pairs:
            continue
        B, _ = basis_V(n, lt, LEs)
        go, ge = groups_o(n), groups_e(n)
        c = random_c(pairs, rng)
        vals = linear_stat(n, lt, Fraction(0), c, LEs)
        po = cond_expectation(vals, LEs, go)
        pe = cond_expectation(vals, LEs, ge)
        k = Fraction(2, n - 1)
        cand = {
            "Pi_o": po,
            "Pi_e": pe,
            "M": [k * (2 * f - a - b) for f, a, b in zip(vals, po, pe)],
            "I-P_BK": bk_apply(vals, LEs, n, lt),
        }
        for name, vec in cand.items():
            counts[name][1] += 1
            if in_span(B, vec):
                counts[name][0] += 1
    for name, (inside, tot) in counts.items():
        print(f"  {name:8s}: image lands back in V at {inside}/{tot} (poset, f) pairs"
              f"  -> {'INVARIANT on this population' if inside == tot else 'NOT INVARIANT'}")
    ok &= verdict(all(v[0] < v[1] for v in counts.values()),
                  "V is NOT invariant under ANY of the four -- pm-onethird's (B) premise CONFIRMED")

    banner("a3.3  the smallest certificate of non-invariance, exhibited in full")
    # n = 3 antichain, f = 1{0 <_L 1}.  Printed so the claim can be checked by hand.
    n, lt = 3, frozenset()
    LEs = linear_extensions(n, lt)
    B, pairs = basis_V(n, lt, LEs)
    c = {(0, 1): Fraction(1), (0, 2): Fraction(0), (1, 2): Fraction(0)}
    vals = linear_stat(n, lt, Fraction(0), c, LEs)
    po = cond_expectation(vals, LEs, groups_o(n))
    print(f"  P = antichain on {{0,1,2}};  f(L) = 1{{0 <_L 1}};  C_o blocks = {groups_o(n)}")
    print(f"  {'L':<12}{'f':>6}{'Pi_o f':>9}   {'1{0<1}':>7}{'1{0<2}':>8}{'1{1<2}':>8}")
    for k, L in enumerate(LEs):
        row = "".join(str(x) for x in L)
        ind = [str(B[j + 1][k]) for j in range(3)]
        print(f"  {row:<12}{str(vals[k]):>6}{str(po[k]):>9}   {ind[0]:>7}{ind[1]:>8}{ind[2]:>8}")
    ok &= verdict(in_span(B, vals), "f itself IS in V [REFUSES CORRECTLY]")
    ok &= verdict(not in_span(B, po), "Pi_o f is NOT in V -- exact Gaussian elimination")
    print("  by hand: alpha=0 (from 210), beta=1 (201), delta=0 (120), gamma=1/2 (102)")
    print("           forces Pi_o f(012) = 3/2, but the table says 1/2.  No solution.")

    banner("a3.4  the spectral consequence -- three Rayleigh minima, MEASURED (floats)")
    print("  Predicted ordering, from (***) plus Cauchy interlacing:")
    print("    (2/(n-1)) lam_2(M)   <=   lam_2(I - P_BK)   <=   min over V_0  =  (2/(n-1)) lam_2^V(M)")
    print()
    print(f"  {'poset':<26}{'(2/(n-1))lam2(M)':>18}{'lam2(I-P_BK)':>15}{'min over V_0':>15}"
          f"{'lossy?':>9}")
    rows = []
    order_bad = 0
    ident_bad = 0
    pool = [(n, lt) for n, lt in population(nmax=4, samples=())]
    pool += [(5, lt) for lt in [random_poset(5, 0.3, rng) for _ in range(25)]]
    for n, lt in pool:
        LEs = linear_extensions(n, lt)
        pairs = incomparable_pairs(n, lt)
        if not pairs or len(LEs) < 3 or len(LEs) > 60:
            continue
        Mo, Me = pi_matrix(LEs, groups_o(n)), pi_matrix(LEs, groups_e(n))
        N = len(LEs)
        Mm = [[(2 if i == j else 0) - Mo[i][j] - Me[i][j] for j in range(N)] for i in range(N)]
        Bk = bk_matrix(LEs, n, lt)
        k = 2.0 / (n - 1)
        lam_M = jacobi_eigenvalues([[float(x) for x in r] for r in Mm])[1]
        lam_BK = jacobi_eigenvalues([[float(x) for x in r] for r in Bk])[1]
        # min over V_0 of <f, M f>/Var(f): centre the basis, drop dependencies, solve
        Bv, _ = basis_V(n, lt, LEs)
        W = []
        for col in Bv[1:]:
            m = sum(col) / Fraction(N)
            w = [x - m for x in col]
            if any(x != 0 for x in w) and not in_span(W, w):
                W.append(w)
        if not W:
            continue
        A = [[sum(a * s for a, s in zip(wi, [sum(Mm[p][q] * wj[q] for q in range(N))
                                             for p in range(N)])) / N for wj in W] for wi in W]
        Bm = [[sum(a * b for a, b in zip(wi, wj)) / N for wj in W] for wi in W]
        ev = gen_eig_min([[float(x) for x in r] for r in A], [[float(x) for x in r] for r in Bm])
        if ev is None:
            continue
        lam_V = ev[0]
        lo, mid, hi = k * lam_M, lam_BK, k * lam_V
        if not (lo <= mid + 1e-9 and mid <= hi + 1e-9):
            order_bad += 1
        rows.append((n, lo, mid, hi))
    for n, lo, mid, hi in rows[:14]:
        tag = "" if abs(lo - mid) < 1e-9 else f"{mid / lo:.3f}x" if lo > 1e-12 else "inf"
        print(f"  {'n=' + str(n) + ' (sampled)':<26}{lo:>18.6f}{mid:>15.6f}{hi:>15.6f}{tag:>9}")
    print(f"  ... {len(rows)} posets measured in total")
    ok &= verdict(order_bad == 0, "the predicted ordering holds at every measured poset",
                  f"{order_bad}/{len(rows)} violations")
    strict = sum(1 for _, lo, mid, hi in rows if mid > lo + 1e-9)
    tight = sum(1 for _, lo, mid, hi in rows if abs(mid - hi) < 1e-9)
    worst = max((mid / lo for _, lo, mid, hi in rows if lo > 1e-12), default=float("nan"))
    print(f"  section 4's full-space quantity is STRICTLY below the BK gap at {strict}/{len(rows)}"
          f" posets; worst ratio lam_2(I-P_BK) / ((2/(n-1))lam_2(M)) = {worst:.4f}")
    print(f"  the BK gap is attained by a LINEAR statistic (min over V_0 = lam_2(I-P_BK)) at"
          f" {tight}/{len(rows)} posets")

    print()
    print("a3 VERDICT:", "section 4 read settled" if ok else "INSTRUMENT BROKEN OR READ REFUTED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
