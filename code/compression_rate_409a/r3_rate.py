"""r3 -- THE RATE, if alpha_n is read the other way: uniform over posets at each n.

r1/r2 read `alpha_n` per-poset.  The note writes it with a subscript n and no poset, which
reads as a constant valid at every poset on n elements.  Under THAT reading the ceiling is
much lower than 1, and it is available in closed form with no eigensolver at all.

  THEOREM (S3 of the README, proved by hand, re-derived exactly here).
  On the antichain A_n, EVERY centred position statistic f_w(L) = sum_x w_x pos_L(x) -- a
  pair-orientation linear statistic in the note's own sense, with c_xy = w_y - w_x -- has

        E_BK(f_w)/Var(f_w) = 12/(n^3 - n)      and     R_M(f_w) = 6/(n(n+1)),

  INDEPENDENTLY OF w.  Hence  alpha_n <= alpha(A_n) <= 6/(n(n+1)) = Theta(n^-2).

Consequence, which is the "true but useless" outcome the ticket asked to be tested for:
through W2's repair a uniform alpha_n = Theta(n^-2) yields gap_BK = Omega(n^-3) -- the order
Bubley-Dyer already gives for the mixing of this chain at EVERY poset (cited in this repo at
docs/audit-stage-process.md:211).  Against the bar of r2 (a constant >= 2) it is short by
Theta(n^2).
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib409a as L  # noqa: E402

ok = True

# --------------------------------------------------------------------------------------
L.banner("r3.1  the antichain closed form, EXACT, and independent of the test weights")

print("    n |  R_BK(f_w)  =  12/(n^3-n)  |  R_M(f_w)  =  6/(n(n+1))  | weight vectors agreeing")
for n in range(3, 8):
    LEs = L.linear_extensions(n, L.antichain(n))
    ws = [[Fraction(i) - Fraction(n - 1, 2) for i in range(n)],
          [Fraction(1)] * (n - 1) + [Fraction(1 - n)],
          [Fraction(3), Fraction(-1)] + [Fraction(-2)] * (n - 2),
          [Fraction((-1) ** i) for i in range(n)] if n % 2 == 0 else
          [Fraction(2), Fraction(-1)] + [Fraction(0)] * (n - 3) + [Fraction(-1)]]
    predB = Fraction(12, n ** 3 - n)
    predM = Fraction(6, n * (n + 1))
    agree = 0
    for w in ws:
        if sum(w) != 0:
            continue
        f = L.position_stat(LEs, {i: w[i] for i in range(n)})
        if L.variance(f) == 0:
            continue
        rb = L.rayleigh_BK(f, LEs, n, L.antichain(n))
        rm = L.rayleigh_M(f, LEs, n)
        if rb == predB and rm == predM:
            agree += 1
        else:
            ok &= L.verdict(False, f"n={n} closed form FAILS", f"{rb} vs {predB}")
    print("  %3d |  %24s  |  %23s  | %d" % (n, str(predB), str(predM), agree))
    ok &= L.verdict(agree >= 3, f"n={n}: >=3 independent weight vectors give the same value")

# --------------------------------------------------------------------------------------
L.banner("r3.2  and the true alpha(A_n) is no larger -- Jacobi, measurement only")

print("    n |  measured alpha(A_n)  |  closed-form bound 6/(n(n+1))  |  1 - cos(pi/n)")
import math  # noqa: E402
for n in (3, 4, 5):
    LEs = L.linear_extensions(n, L.antichain(n))
    a = L.alpha_measured(LEs, n)
    b = Fraction(6, n * (n + 1))
    c = 1.0 - math.cos(math.pi / n)
    print("  %3d |  %19s  |  %28s  |  %s"
          % (n, L.frac(a, 9), L.frac(b, 9), L.frac(c, 9)))
    ok &= L.verdict(a <= float(b) + 1e-9, f"  alpha(A_{n}) <= 6/(n(n+1))")
print()
print("  The third column is what Aldous' spectral gap theorem (Caputo-Liggett-Richthammer)")
print("  predicts for this chain on the antichain: gap = (2-2cos(pi/n))/(n-1), so")
print("  ((n-1)/2)*gap = 1-cos(pi/n).  IT IS READ FROM THE LITERATURE, NOT PROVED HERE, and")
print("  no verdict in this directory depends on it; the closed-form bound above is self-")
print("  contained and is what carries the Theta(n^-2) claim.")

# --------------------------------------------------------------------------------------
L.banner("r3.3  is the antichain the minimiser?  min alpha over posets, per n")

print("    n |  population           |  min alpha  |  alpha(A_n)  |  posets within 1e-9 of min")
for n, label, posets in ((3, "exhaustive", list(L.all_posets(3))),
                         (4, "exhaustive", list(L.all_posets(4))),
                         (5, "sampled(60,seed=909)", L.sample_posets(5, 60, 909))):
    vals = []
    for lt in posets:
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        vals.append(L.alpha_measured(LEs, n))
    best = min(vals)
    ties = sum(1 for v in vals if v <= best + 1e-9)
    aA = L.alpha_measured(L.linear_extensions(n, L.antichain(n)), n)
    print("  %3d |  %-20s |  %9s  |  %10s  |  %d of %d"
          % (n, label, L.frac(best, 6), L.frac(aA, 6), ties, len(vals)))
    ok &= L.verdict(abs(best - aA) < 1e-9,
                    f"  n={n}: the population minimum equals alpha(A_{n})")
print()
print("  THE ANTICHAIN IS NOT THE UNIQUE MINIMISER -- the value 6/(n(n+1)) is shared by a")
print("  large tie class (at n=4, the argmin by raw float is the single-relation poset")
print("  {(1,3)}, differing from A_4 in the 16th digit).  That makes the closed form more")
print("  useful, not less: it is not a property of one exotic poset.")
print("  n=5 is a SAMPLE, not a sweep, and the antichain is NOT in it -- the row says the")
print("  sampled minimum coincides with alpha(A_5), not that nothing smaller exists.")

# --------------------------------------------------------------------------------------
L.banner("r3 VERDICT")
print("  Under the uniform-in-poset reading, alpha_n <= 6/(n(n+1)) = Theta(n^-2), by a hand")
print("  computation on the antichain.  Through W2's repair that yields gap_BK = Omega(n^-3),")
print("  which is the order this chain is ALREADY known to have at every poset (Bubley-Dyer,")
print("  n^3 log n mixing).  TRUE, AND USELESS: it is Theta(n^2) below the bar of r2.")
sys.exit(0 if ok else 1)
