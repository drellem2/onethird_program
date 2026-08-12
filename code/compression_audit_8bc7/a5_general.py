"""a5 -- the finding this audit adds: (*) is the EQUALITY CASE of an operator inequality
that holds on the whole of L^2, not only on the linear-statistic subspace V.

Claim (mine, not the note's).  With M = 2I - Pi_o - Pi_e,

        <f, (I - P_BK) f>  >=  (2/(n-1)) <f, M f>      for EVERY f in L^2(L(P)),

with equality exactly when f is affine (degree <= 1) on every fiber of BOTH foliations.

Why it is true.  On one fiber the odd part of the Dirichlet form is the cube Dirichlet form,
which acts on the Fourier mode chi_S with eigenvalue 2|S|; the corresponding part of M acts
with eigenvalue 2 for every S =/= 0.  Since 2|S| >= 2 with equality iff |S| = 1, the odd part
dominates fiberwise, and likewise the even part.  Section 3's "degree one on every cube"
(compression.tex:108) is exactly the |S| = 1 case.

Why it matters for section 4.  pm-onethird's (B) is right that V is not invariant (a3.2), so
(***) does not license reading section 4's "small eigenvalues of 2I - Pi_o - Pi_e" as a
statement about the subspace the reduction lives on.  This inequality repairs that: the
full-space eigenvalue bounds the TRUE BK gap from below, for every f, with no assumption that
the extremal function is linear.  The direction is the one the (1/3)-(2/3) program needs.  It
is also potentially LOSSY, and 5.3 measures by how much.

Every PSD verdict here is exact rational Schur reduction.  No float is on a verdict path.
"""

from fractions import Fraction
import random
import sys

from lib8bc7 import (banner, verdict, gen_posets_exhaustive, random_poset, linear_extensions,
                     groups_o, groups_e, fibers, incomparable_pairs, linear_stat, random_c,
                     psd_exact, jacobi_eigenvalues, swap_at, legal_at, variance, bk_energy,
                     expected_cond_variance)
from a3_operator import pi_matrix, bk_matrix, basis_V

rng = random.Random(31337)


def difference_matrix(LEs, n, lt, k=None):
    """D = (I - P_BK) - k*(2I - Pi_o - Pi_e), default k = 2/(n-1).  Exact rationals."""
    if k is None:
        k = Fraction(2, n - 1)
    N = len(LEs)
    Mo, Me = pi_matrix(LEs, groups_o(n)), pi_matrix(LEs, groups_e(n))
    Bk = bk_matrix(LEs, n, lt)
    return [[Bk[i][j] - k * ((2 if i == j else 0) - Mo[i][j] - Me[i][j])
             for j in range(N)] for i in range(N)]


def rank_exact(A):
    M = [row[:] for row in A]
    rows, cols = len(M), len(M[0])
    r = 0
    for c in range(cols):
        p = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        r += 1
        if r == rows:
            break
    return r


def fiber_affine_dim(LEs, n, lt):
    """dim of the space of functions that are affine on every fiber of BOTH foliations.

    Computed as the null space dimension of the constraint system: on each fiber of each
    foliation, every Fourier coefficient of order >= 2 must vanish.  Realised concretely by
    requiring, for every 2x2 sub-square of a fiber (two block-flips), that the alternating
    sum f(00) - f(01) - f(10) + f(11) be zero -- that IS the order-2 coefficient, and the
    higher orders follow from the order-2 ones vanishing on every sub-cube.
    """
    idx = {L: k for k, L in enumerate(LEs)}
    N = len(LEs)
    rows = []
    for groups in (groups_o(n), groups_e(n)):
        pos = [g[0] for g in groups if len(g) == 2]
        for L in LEs:
            for a in range(len(pos)):
                for b in range(a + 1, len(pos)):
                    p, q = pos[a], pos[b]
                    if not (legal_at(L, p, lt) and legal_at(L, q, lt)):
                        continue
                    L1, L2 = swap_at(L, p), swap_at(L, q)
                    L3 = swap_at(L1, q)
                    row = [Fraction(0)] * N
                    row[idx[L]] += 1
                    row[idx[L1]] -= 1
                    row[idx[L2]] -= 1
                    row[idx[L3]] += 1
                    if any(x != 0 for x in row):
                        rows.append(row)
    if not rows:
        return N
    return N - rank_exact(rows)


def population(nmax=5, cap=48):
    """EVERY labeled poset to n = 4, then n = 5 down to the |L(P)| cap.

    An earlier version shuffled the whole n<=5 list and truncated, which left 2 of the 19
    posets at n = 3 in the population -- a sample presented as a sweep.  The small n are
    cheap; there is no reason not to take all of them.
    """
    for n in range(2, 5):
        for lt in gen_posets_exhaustive(n):
            if len(linear_extensions(n, lt)) <= cap:
                yield (n, lt)
    if nmax >= 5:
        for lt in gen_posets_exhaustive(5):
            if len(linear_extensions(5, lt)) <= cap:
                yield (5, lt)


def main():
    ok = True

    banner("a5.1  is (I - P_BK) - (2/(n-1))(2I - Pi_o - Pi_e) positive semidefinite?")
    print("  EXACT rational Schur reduction on the full |L(P)| x |L(P)| matrix.")
    pool = [(n, lt) for n, lt in population()]
    small = [p for p in pool if p[0] <= 4]
    big = [p for p in pool if p[0] == 5]
    rng.shuffle(big)
    pool = small + big[:400]          # all of n <= 4, sampled at n = 5
    bad = 0
    tested = 0
    ncap = {}
    for n, lt in pool:
        LEs = linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        tested += 1
        ncap[n] = ncap.get(n, 0) + 1
        if not psd_exact(difference_matrix(LEs, n, lt)):
            bad += 1
    print(f"  population: {tested} posets ({', '.join(f'n={k}: {v}' for k, v in sorted(ncap.items()))}),"
          f" |L(P)| capped at 48 for the exact PSD test")
    ok &= verdict(bad == 0, "(I - P_BK) >= (2/(n-1)) M  as an operator, on the FULL space",
                  f"{bad}/{tested} violations")

    banner("a5.2  the equality case: which f attain it?")
    kbad = vbad = 0
    dimrows = []
    for n, lt in pool[:120]:
        LEs = linear_extensions(n, lt)
        pairs = incomparable_pairs(n, lt)
        if len(LEs) < 2 or not pairs:
            continue
        D = difference_matrix(LEs, n, lt)
        N = len(LEs)
        # every linear statistic must be in ker D  (this is exactly (*) )
        for _ in range(2):
            v = linear_stat(n, lt, Fraction(0), random_c(pairs, rng), LEs)
            q = sum(v[i] * sum(D[i][j] * v[j] for j in range(N)) for i in range(N))
            if q != 0:
                vbad += 1
        d_ker = N - rank_exact([row[:] for row in D])
        d_aff = fiber_affine_dim(LEs, n, lt)
        Bv, _ = basis_V(n, lt, LEs)
        d_V = rank_exact([row[:] for row in Bv])
        if d_ker != d_aff:
            kbad += 1
        dimrows.append((n, N, d_V, d_ker, d_aff))
    ok &= verdict(vbad == 0, "every linear statistic attains equality -- (*) is the equality case",
                  f"{vbad} violations")
    ok &= verdict(kbad == 0,
                  "ker D = {f affine on every fiber of BOTH foliations}, EXACTLY",
                  f"{kbad}/{len(dimrows)} posets where the two dimensions differ")
    bigger = sum(1 for _, _, dV, dk, _ in dimrows if dk > dV)
    print(f"  dim ker D > dim V at {bigger}/{len(dimrows)} posets: being affine on every fiber")
    print("  is WEAKER than being a pair-orientation linear statistic, so the equality case of")
    print("  the inequality is a strictly larger space than the note's scope line names.")
    print(f"  {'n':>3}{'|L(P)|':>8}{'dim V':>8}{'dim ker D':>11}{'dim affine':>12}")
    for row in dimrows[:8]:
        print(f"  {row[0]:>3}{row[1]:>8}{row[2]:>8}{row[3]:>11}{row[4]:>12}")

    banner("a5.3  controls")
    # C1: the reverse inequality must FAIL somewhere, else the two operators are equal and
    # the finding is vacuous.
    rev_fail = 0
    seen = 0
    for n, lt in pool[:200]:
        LEs = linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        seen += 1
        D = difference_matrix(LEs, n, lt)
        negD = [[-x for x in row] for row in D]
        if not psd_exact(negD):
            rev_fail += 1
    ok &= verdict(rev_fail > 0,
                  "C1  the REVERSE inequality fails -- the two operators are not equal",
                  f"{rev_fail}/{seen} posets")

    # C2: the constant 2 is optimal -- raising it to 5/2 must break PSD.
    broke = 0
    seen = 0
    for n, lt in pool[:200]:
        LEs = linear_extensions(n, lt)
        if len(LEs) < 2 or not incomparable_pairs(n, lt):
            continue
        seen += 1
        if not psd_exact(difference_matrix(LEs, n, lt, k=Fraction(5, 2 * (n - 1)))):
            broke += 1
    ok &= verdict(broke > 0, "C2  constant 2/(n-1) -> (5/2)/(n-1) breaks PSD: 2 is optimal",
                  f"{broke}/{seen} posets")

    # C3: lowering it to 1/(n-1) must NOT break PSD (a weaker true statement) -- a control
    # that must refuse to fire, so C2 is not just "any change breaks it".
    broke = 0
    seen = 0
    for n, lt in pool[:200]:
        LEs = linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        seen += 1
        if not psd_exact(difference_matrix(LEs, n, lt, k=Fraction(1, n - 1))):
            broke += 1
    ok &= verdict(broke == 0, "C3  a SMALLER constant stays PSD [REFUSES CORRECTLY]",
                  f"{broke}/{seen} posets")

    banner("a5.4  how lossy is the full-space bound?  (floats: MEASUREMENT, not verdict)")
    print(f"  {'n':>3}{'|L(P)|':>8}{'lam2(I-P_BK)':>15}{'(2/(n-1))lam2(M)':>18}{'ratio':>9}")
    worst = 0.0
    rows = []
    for n, lt in pool:
        LEs = linear_extensions(n, lt)
        if len(LEs) < 3 or len(LEs) > 24 or not incomparable_pairs(n, lt):
            continue
        N = len(LEs)
        Mo, Me = pi_matrix(LEs, groups_o(n)), pi_matrix(LEs, groups_e(n))
        Mm = [[float((2 if i == j else 0) - Mo[i][j] - Me[i][j]) for j in range(N)]
              for i in range(N)]
        Bk = [[float(x) for x in row] for row in bk_matrix(LEs, n, lt)]
        lam_M = jacobi_eigenvalues(Mm)[1] * 2.0 / (n - 1)
        lam_BK = jacobi_eigenvalues(Bk)[1]
        if lam_M > 1e-12:
            rows.append((n, N, lam_BK, lam_M, lam_BK / lam_M))
            worst = max(worst, lam_BK / lam_M)
    rows.sort(key=lambda r: -r[4])
    for r in rows[:8]:
        print(f"  {r[0]:>3}{r[1]:>8}{r[2]:>15.6f}{r[3]:>18.6f}{r[4]:>9.4f}")
    print(f"  {len(rows)} posets measured; worst overstatement of the loss = {worst:.4f}x")
    print("  i.e. on this population section 4's full-space quantity is never more than")
    print(f"  {worst:.3f}x below the true BK gap -- the route is valid and mildly lossy here.")

    print()
    print("a5 VERDICT:", "operator inequality CONFIRMED" if ok else "REFUTED OR INSTRUMENT BROKEN")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
