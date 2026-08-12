"""r2 -- THE BAR.  What does the (1/3)-(2/3) route actually require of alpha_n?

The note never says.  This arm derives it from the one place in the programme that consumes
a BK-chain number -- Theorem E, STATE.md row 6, `U`/proven, proved at
one_third_width_three/step8.tex sections G1.1-G1.3 -- and then checks every link of the
derivation exactly on this instrument.

THE CHAIN, and every link is verified below:

  (L1)  (*) at a pair indicator:   R_M(f_xy) = ((n-1)/2) * E_BK(f_xy)/Var(f_xy)     [exact]
  (L2)  alpha(P) <= R_M(f_xy)      for every incomparable pair                      [Rayleigh]
  (L3)  sum_{x||y} E_BK(f_xy) <= 1/2                            [step8.tex Step 1, re-derived]
  (L4)  Theorem E: a gamma-counterexample has a pair with E_BK/Var <= 2/(gamma n)

  =>    alpha(P) <= (n-1)/(gamma n)   for every gamma-counterexample P.

W2's repair turns a lower bound on alpha into a lower bound on the BK gap, so the ONLY way
the compression can bite is to CONTRADICT that cap, i.e. to prove

        THE BAR:   alpha_n > (n-1)/(gamma n)  ->  1/gamma >= 3   (gamma <= 1/3, strict).

r1 measured the ceiling: alpha_n <= 1.  1 < 2 <= (n-1)/(gamma n) for every n >= 3.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib409a as L  # noqa: E402

ok = True

POPS = [(3, "exhaustive", list(L.all_posets(3))),
        (4, "exhaustive", list(L.all_posets(4))),
        (5, "exhaustive", list(L.all_posets(5))),
        (6, "sampled(120,seed=409)", L.sample_posets(6, 120, 409)),
        (7, "sampled(40,seed=1409)", L.sample_posets(7, 40, 1409))]

# --------------------------------------------------------------------------------------
L.banner("r2.1  (L1)  R_M(f_xy) = ((n-1)/2) * R_BK(f_xy) at every incomparable pair -- EXACT")

pairs_tested = 0
bad = 0
for n, label, posets in POPS:
    if n >= 7:
        posets = posets[:12]
    for lt in posets:
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        for (x, y) in L.incomparable(n, lt):
            f = L.pair_indicator(n, lt, LEs, x, y)
            rm = L.rayleigh_M(f, LEs, n)
            rb = L.rayleigh_BK(f, LEs, n, lt)
            if rm is None or rb is None:
                continue
            pairs_tested += 1
            if rm != Fraction(n - 1, 2) * rb:
                bad += 1
ok &= L.verdict(bad == 0, f"exact at all {pairs_tested} (poset, incomparable pair) instances")

# --------------------------------------------------------------------------------------
L.banner("r2.2  (L3)  sum over incomparable pairs of E_BK(f_xy) <= 1/2 -- EXACT")
print("  step8.tex Step 1, re-derived here on an implementation that has never seen it.")

worst = Fraction(0)
worst_at = None
cnt = 0
for n, label, posets in POPS:
    if n >= 7:
        posets = posets[:12]
    mx = Fraction(0)
    for lt in posets:
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        tot = sum(L.bk_energy(L.pair_indicator(n, lt, LEs, x, y), LEs, n, lt)
                  for (x, y) in L.incomparable(n, lt))
        cnt += 1
        if tot > mx:
            mx = tot
        if tot > worst:
            worst, worst_at = tot, (n, len(LEs))
    ok &= L.verdict(mx <= Fraction(1, 2), f"n={n} {label}: max sum = {mx} <= 1/2")
print(f"  ({cnt} posets; the sup 1/2 is approached when almost every adjacent pair is"
      f" incomparable -- largest seen {worst} at n={worst_at[0]})")

# --------------------------------------------------------------------------------------
L.banner("r2.3  (L2)  the measured alpha never exceeds the pair-witness bound")

bad = 0
checked = 0
tight = 0
for n, label, posets in POPS[:2] + [(5, "sampled(50)", L.sample_posets(5, 50, 77))]:
    for lt in posets:
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        inc = L.incomparable(n, lt)
        if not inc:
            continue
        best = None
        for (x, y) in inc:
            r = L.rayleigh_M(L.pair_indicator(n, lt, LEs, x, y), LEs, n)
            if r is not None and (best is None or r < best):
                best = r
        if best is None:
            continue
        a = L.alpha_measured(LEs, n)
        checked += 1
        if a > float(best) + 1e-9:
            bad += 1
        if abs(a - float(best)) < 1e-9:
            tight += 1
ok &= L.verdict(bad == 0, f"alpha <= min_pair R_M(f_xy) at all {checked} posets")
print(f"  (the pair witness is TIGHT -- equal to alpha -- at {tight} of {checked})")

# --------------------------------------------------------------------------------------
L.banner("r2.4  THE BAR against THE CEILING")

print("  Theorem E (step8.tex Lemma frozen-pair-existence + Theorem G1):")
print("      a gamma-counterexample on n elements has an incomparable pair with")
print("      E_BK(f_xy)/Var(f_xy) <= lambda(gamma,n) = 2/(gamma n),   gamma in (0, 1/3].")
print()
print("  Through (L1)+(L2) that is a CAP on alpha:   alpha(P) <= (n-1)/(gamma n).")
print("  W2's repair gives  gap_BK >= (2/(n-1)) alpha, so a contradiction needs the cap")
print("  VIOLATED:          alpha_n > (n-1)/(gamma n)  =  THE BAR.")
print()
print("     n  |  BAR at gamma=1/3  |  BAR at gamma=1/4  |  BAR at gamma=1/6  |  CEILING")
print("  -------+--------------------+--------------------+--------------------+---------")
for n in (3, 4, 5, 6, 8, 12, 20, 100, 1000):
    row = "  %6d |" % n
    for g in (Fraction(1, 3), Fraction(1, 4), Fraction(1, 6)):
        row += "  %17s |" % L.frac(Fraction(n - 1, 1) / (g * n), 6)
    row += "     1"
    print(row)
print()
print("  sup_n sup_{gamma<=1/3} of the bar is 3;  inf over n>=3 at gamma=1/3 is 2.")

bar_min = min(Fraction(n - 1, 1) / (Fraction(1, 3) * n) for n in range(3, 2000))
ok &= L.verdict(bar_min >= 2, "the bar is >= 2 for every n >= 3 even at the most generous"
                              " gamma = 1/3", f"min = {bar_min}")
ok &= L.verdict(Fraction(1) < bar_min, "THE CEILING (1) IS BELOW THE BAR (>= 2)",
                "shortfall factor >= 2, rising to 3")

# --------------------------------------------------------------------------------------
L.banner("r2.5  the same statement without Theorem E's hypotheses, measured directly")
print("  For EVERY poset (no counterexample hypothesis at all), the ratio-of-sums bound")
print("  alpha <= ((n-1)/2) * sum E / sum Var holds; here is how much slack there is.")

print("     n |  posets |  max alpha  |  max ((n-1)/2)*sumE/sumVar  | violations")
for n, label, posets in POPS[:3]:
    if n == 5:
        posets = L.sample_posets(5, 60, 909)
    mx_a = 0.0
    mx_b = Fraction(0)
    viol = 0
    cnt = 0
    for lt in posets:
        LEs = L.linear_extensions(n, lt)
        inc = L.incomparable(n, lt)
        if len(LEs) < 2 or not inc:
            continue
        sE = sum(L.bk_energy(L.pair_indicator(n, lt, LEs, x, y), LEs, n, lt) for x, y in inc)
        sV = sum(L.variance(L.pair_indicator(n, lt, LEs, x, y)) for x, y in inc)
        if sV == 0:
            continue
        b = Fraction(n - 1, 2) * sE / sV
        a = L.alpha_measured(LEs, n)
        cnt += 1
        mx_a = max(mx_a, a)
        mx_b = max(mx_b, b)
        if a > float(b) + 1e-9:
            viol += 1
    print("  %4d | %7d |  %9s  |  %25s  | %d" % (n, cnt, L.frac(mx_a, 6), L.frac(mx_b, 6), viol))
    ok &= L.verdict(viol == 0, f"  n={n}: no violation of the ratio-of-sums cap")

L.banner("r2 VERDICT")
print("  THE REQUIRED RATE IS NOT A RATE.  alpha_n must EXCEED (n-1)/(gamma n), a CONSTANT")
print("  between 2 and 3 -- it does not decay with n at all.  The ceiling from r1 is 1.")
print("  The compression route is short by a factor of at least 2, and asymptotically 3.")
sys.exit(0 if ok else 1)
