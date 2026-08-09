"""s5 — THE THEOREM'S SECOND BRANCH.

mg-28ff's THEOREM (§2) has two cases:
    Phi*_pref^2 <= R(g)(2 Delta_P - R(g))   when R(g) <= Delta_P
    Phi*_pref^2 <= Delta_P^2                otherwise.

But the HYPOTHESIS it derives, (M#), is stated in §2 and §4.2 with ONE case only:
    (M#)  mu_pref (2 Delta_P - mu_pref) <= 2(1 - lambda_std)
    c#(P) = mu_pref (2 Delta_P - mu_pref) / (2(1-lambda_std)).

When mu_pref > Delta_P the map t -> t(2Delta-t) is DECREASING, so the one-case form
UNDERSTATES the bound the theorem actually delivers: the truth there is Delta_P^2, and
mu(2Delta-mu) < Delta^2.  So (M#) AS WRITTEN can hold at a poset where the theorem does
NOT deliver C_3 = 1.  This script measures whether that gap bites on n <= 6.

MY OWN DEFECT, WHICH IS WHY THIS SCRIPT EXISTS: s3's V11 omitted the same branch.  It was
caught by my V11 disagreeing with mg-28ff's c# at n = 2 (I got 0.000000, the parent
0.125000) - the parent's INSTRUMENT implements the branch even though its DOCUMENT does
not state it.  I audited a formula-vs-branch mismatch and shipped one.
"""
import time
from fractions import Fraction as F
from lib29fe import (all_natural_posets, is_decomposable, Poset, bracket_gap,
                     bracket_mu_pref)

ITERS = 34
print("=" * 92)
print("s5  the theorem's second branch — does omitting it change anything at n <= 6?")
print("=" * 92)
print(f"{'n':>3} {'prim':>6} {'c# BRANCHED':>12} {'c# 1-case':>11} {'differ?':>8} "
      f"{'mu>Delta at':>12} {'V01 branched':>13} {'V01 fails':>10} {'c_or=min(c#,f*)':>16}")
for n in range(2, 7):
    t0 = time.time()
    prim = [r for r in all_natural_posets(n) if not is_decomposable(n, r)]
    fl = n * n // 4
    mb = m1 = None; over = 0; v01mx = None; v01f = 0; cor = None
    argb = None
    for rel in prim:
        P = Poset(n, rel)
        glo, ghi = bracket_gap(P, iters=ITERS)
        mlo, mhi = bracket_mu_pref(P, iters=ITERS)
        D = P.Delta
        # branched c#: use the bracket end that makes it an UPPER bound
        def csharp(mu, g):
            return (mu * (2 * D - mu) if mu <= D else D * D) / (2 * g)
        hb = max(csharp(mlo, glo), csharp(mhi, glo))
        h1 = (mhi * (2 * D - mhi)) / (2 * glo)
        h1 = max(h1, (mlo * (2 * D - mlo)) / (2 * glo))
        if mlo > D:
            over += 1
        if mb is None or hb > mb:
            mb, argb = hb, sorted(rel)
        if m1 is None or h1 > m1:
            m1 = h1
        # V01: Delta -> 1, keep -E(h).  Branch at mu > 1.
        v01 = (mhi * (2 - mhi) if mhi <= 1 else F(1)) / (2 * glo)
        v01lo = (mlo * (2 - mlo) if mlo <= 1 else F(1)) / (2 * ghi)
        if v01mx is None or v01 > v01mx:
            v01mx = v01
        if v01lo > 1:
            v01f += 1
        fs = (P.EDF / (2 * fl)) ** 2 / (2 * glo)
        both = min(hb, fs)
        if cor is None or both > cor:
            cor = both
    print(f"{n:>3} {len(prim):>6} {float(mb):>12.6f} {float(m1):>11.6f} "
          f"{'YES' if abs(float(mb-m1))>1e-9 else 'no':>8} {over:>12} "
          f"{float(v01mx):>13.6f} {v01f:>10} {float(cor):>16.6f}  ({time.time()-t0:.0f}s)")
print()
print("mg-28ff §4.2's published c#: 0.125000 0.500000 0.636846 0.803289 0.943151")
print("q51f4's independently computed c_or:      0.250 0.306 0.551 0.754 at n=3..6")
print("=" * 92)
