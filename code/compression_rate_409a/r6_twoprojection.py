"""r6 -- DOES THE TWO-PROJECTION LITERATURE SETTLE IT?  (pm-onethird's 14:05 re-scope.)

W3 (mg-623a) named the live references: Qian, arXiv:2201.12500 (two-component Gibbs samplers
via the theory of two projections) and arXiv:2304.02109 (Solidarity of Gibbs samplers: the
spectral gap, AAP 2025).  This arm checks what that theory actually delivers for THIS
operator, by computing the object it reduces to.

HALMOS (1969), specialised to M = 2I - Pi_o - Pi_e on 1-perp.  Write Q_o = Pi_o - P_1 and
Q_e = Pi_e - P_1 for the two projections with the constants removed.  In the generic part the
pair is unitarily 2x2 blocks indexed by the principal angles theta_k, on which the spectrum
of M is 1 -/+ cos theta_k; on Ran Q_o ^ Ker Q_e and Ker Q_o ^ Ran Q_e it is 1; on
Ker Q_o ^ Ker Q_e it is 2; on Ran Q_o ^ Ran Q_e it is 0, and r1.1 showed THAT PART IS EMPTY
for every poset.  Hence, exactly,

        alpha(P) = 1 - cos(theta_min),      cos(theta_min) = sqrt(lam_max(Q_o Q_e Q_o)),

with alpha = 1 when the generic part is empty.  Checked below to 1e-14.

WHAT THAT IS WORTH, WHICH IS THE POINT OF THE ARM: the identification is EXACT and it is
STANDARD, so the reformulation is real -- and it cannot help, because 1 - cos theta <= 1 is an
identity.  THE LITERATURE CANNOT RAISE alpha ABOVE THE CEILING OF r1, BECAUSE THE CEILING IS
A PROPERTY OF THE OBJECT AND NOT OF OUR ARGUMENTS ABOUT IT.
"""

import math
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib409a as L  # noqa: E402

ok = True


def q_matrices(LEs, n):
    """Q_o, Q_e: the two conditional-expectation projections with the constants removed.

    FLOAT.  This whole arm is a measurement -- it checks that a published identification of
    alpha holds on our operator; no verdict in this directory rests on it.
    """
    N = len(LEs)
    out = []
    for g in (L.blocks_o(n), L.blocks_e(n)):
        A = [[-1.0 / N] * N for _ in range(N)]
        for _, idxs in L.fiber_map(LEs, g).items():
            w = 1.0 / len(idxs)
            for a in idxs:
                row = A[a]
                for b in idxs:
                    row[b] += w
        out.append(A)
    return out


def matmul(A, B):
    N = len(A)
    Bt = [[B[k][j] for k in range(N)] for j in range(N)]
    return [[sum(x * y for x, y in zip(A[i], Bt[j])) for j in range(N)] for i in range(N)]


def cos_theta_min(LEs, n):
    Qo, Qe = q_matrices(LEs, n)
    S = matmul(matmul(Qo, Qe), Qo)
    ev = L.jacobi_eigenvalues(S)
    return math.sqrt(max(0.0, ev[-1]))


L.banner("r6.1  alpha(P) = 1 - cos(theta_min)  --  Halmos, verified on this instrument")

print("   n |  population        |  posets |  max |alpha - (1 - cos theta_min)|")
worst_all = 0.0
for n, label, posets in ((3, "exhaustive", list(L.all_posets(3))),
                         (4, "exhaustive", list(L.all_posets(4))),
                         (5, "sampled(25,seed=6409), |L|<=60", L.sample_posets(5, 25, 6409))):
    worst = 0.0
    cnt = 0
    for lt in posets:
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2 or len(LEs) > 60:
            continue
        cnt += 1
        d = abs(L.alpha_measured(LEs, n) - (1.0 - cos_theta_min(LEs, n)))
        worst = max(worst, d)
    worst_all = max(worst_all, worst)
    print("  %3d |  %-18s |  %6d |  %.3e" % (n, label, cnt, worst))
    ok &= L.verdict(worst < 1e-11, f"  n={n}: the two-projection identification is exact")

L.banner("r6.2  the principal angles at the two extremal families")

# A_6 has 720 linear extensions and this arm is O(N^3) in pure Python, so the antichain
# column stops at n = 5.  Z_n stays cheap (2^(n/2) linear extensions) and runs further.
for name, n, lt in (("A_4", 4, L.antichain(4)), ("A_5", 5, L.antichain(5)),
                    ("Z_4", 4, L.two_block_ordinal_sum(4)),
                    ("Z_6", 6, L.two_block_ordinal_sum(6)),
                    ("Z_8", 8, L.two_block_ordinal_sum(8))):
    if True:
        LEs = L.linear_extensions(n, lt)
        c = cos_theta_min(LEs, n)
        th = math.degrees(math.acos(min(1.0, max(-1.0, c))))
        print("  %-5s  cos theta_min = %s   theta_min = %6.2f deg   alpha = %s"
              % (name, L.frac(c, 6), th, L.frac(1.0 - c, 6)))
print()
print("  Z_n is the DEGENERATE case of the theory: Ran Q_o = {0}, there is no generic part,")
print("  every angle is pi/2, and alpha = 1 -- the largest a principal-angle bound can ever")
print("  return.  A_n is the generic case and its angle closes as n grows.")

L.banner("r6 VERDICT -- what the literature settles, and what it cannot")
print("  SETTLES (and W3 was right that it is off-the-shelf):")
print("    * the FORM.  alpha = 1 - cos theta_min, exactly, by Halmos 1969; Qian")
print("      (arXiv:2201.12500) applies precisely this to two-component Gibbs samplers and,")
print("      per its abstract, reduces the intractable questions to matrix algebra.")
print("    * POSITIVITY.  arXiv:2304.02109 (AAP 2025) proves solidarity: if one scan order")
print("      has a gap, all do, and polynomial scaling is preserved.  For us that is already")
print("      free -- r1.1 gets alpha > 0 from connectivity of the fiber graph in one line.")
print("  CANNOT SETTLE:")
print("    * ANY VALUE ABOVE 1.  1 - cos theta <= 1 is an identity, so no theorem about")
print("      principal angles, published or future, can put alpha over r2's bar of >= 2.")
print("    * A CONSTANT.  Solidarity transfers positivity and polynomial scaling, not")
print("      constants; and Wilson (arXiv:math/0102193 S7, quoted by W3) already priced the")
print("      sweep decomposition at a factor of about two on the UPPER bound only.")
print()
print("  CAVEAT, STATED: the two arXiv items were read at ABSTRACT level only (WebFetch,")
print("  2026-08-12).  Nothing above depends on their contents -- the ceiling is proved in")
print("  r1 and the bar in r2, both on this machine.")
sys.exit(0 if ok else 1)
