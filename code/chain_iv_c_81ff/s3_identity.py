#!/usr/bin/env python3
"""s3 — THE CURRENCY.  `c` (chain IV) and `C_3^gap` (chain II) are ONE unknown.

The ticket's premise is that chain (IV) never spends the Cheeger square, so its demand
is `1 - (1-eps_leak)/c -> 0.20` against chain (III)'s `0.02` — ten times weaker, turning
a 50x wall into a 5x one.  The arithmetic of that is `mg-76b2` section 6 and it is right.
What this script establishes is what the arithmetic COSTS, and it is not free:

  (I1) AN EXACT IDENTITY.  On every poset,  c = (1 - C_3^gap * gap) / (1 - gap).  The
       two constants are not two unknowns; they are one quantity in two currencies,
       related through the poset's own gap.  Verified exactly, every poset n <= 7.

  (I2) AND THE DEMANDS COINCIDE.  Evaluated self-consistently — the reconciliation
       `mg-01ea` landed — chain (IV)'s demand is ALGEBRAICALLY EQUAL to chain (II)'s:

           eps_dem^(IV)  =  eps_leak / C_3^gap  =  eps_dem^(II).      [PROVEN, 2 lines]

       So the 10x that chain (IV) buys over chain (III) is the 10x chain (II) ALREADY
       BUYS.  Chain (IV) is not a fourth route to a cheaper constant.  It is chain (II)
       with the constant written the other way up.

  (I3) WHAT `0.20` COSTS.  `eps_dem^(IV) = 0.20` requires `c = 1` EXACTLY, which by (I1)
       is `C_3^gap = 1` EXACTLY — a prefix indicator that IS a minimiser of the Rayleigh
       quotient.  That is the `C_3 = 1` whose gap-form reading `mg-94c3` measured FALSE
       at 1023 of 1032 posets, rising.  `0.20` is the value at the extreme point, not a
       value any measurement supports.

  (I4) NEGATIVE CONTROL.  A chain (IV) mis-derived so that it DOES pay a Cheeger square
       must fail the plug-back while the correct one passes, so (I2) is not vacuous.

  (I5) THE 5x REFRAMING, PRICED.  What the wall is, as a function of the one unknown.
"""

from fractions import Fraction as F

from lib81ff import all_posets, EPS_LEAK, EPS_SPEC, C_THRESH_SELF, C_THRESH_EXIST

fail = 0


def check(cond, msg):
    global fail
    if not cond:
        fail += 1
        print(f"    FAIL: {msg}")
    else:
        print(f"    ok:   {msg}")


print("=" * 78)
print("s3 — `c` AND `C_3^gap` ARE ONE UNKNOWN IN TWO CURRENCIES")
print("=" * 78)

# --------------------------------------------------------------------- (I1)
print()
print("-" * 78)
print("(I1) THE IDENTITY, EXACTLY, ON EVERY POSET n <= 7")
print("-" * 78)
print()
print("  C_3^gap(P) := min_k Q_k / gap          (chain (II)'s constant; the gap-form)")
print("  c(P)       := (1 - min_k Q_k) / (1-gap) (chain (IV)'s; the literal form)")
print("  =>  c = (1 - C_3^gap * gap) / (1 - gap)        and       C_3^gap = min_k Q_k / gap")
print()
print("  Checked as an EXACT RATIONAL identity at every primitive poset n <= 7.  THE GAP")
print("  USED IS ANY RATIONAL, NOT THE TRUE lambda_2, AND THAT IS THE POINT: the identity")
print("  is FORMAL — it says only that min_k Q_k determines both constants once the gap is")
print("  fixed, so pushing an exact eigenvalue through it would test the eigenroutine and")
print("  not the identity.  The rational used is the float bracketed to 1e-6, and both")
print("  sides are then exact `Fraction` arithmetic.")
tot = bad = 0
for n in range(3, 8):
    for P in all_posets(n):
        if not P.is_primitive() or not P.connected():
            continue
        tot += 1
        mq, _k = P.min_prefix_Q()
        lam2, _v = P.fiedler()
        g = F(lam2).limit_denominator(10 ** 6)
        if g <= 0 or g >= 1:
            continue
        gamma = mq / g
        c_from_gamma = (1 - gamma * g) / (1 - g)
        c_direct = (1 - mq) / (1 - g)
        if c_from_gamma != c_direct:
            bad += 1
check(bad == 0, f"{tot} primitive posets n<=7: the identity holds exactly, {bad} failures")
print()
print("  AND THE EXACT-EIGENVALUE VERSION, on the smaller population where it is cheap:")
totE = badE = 0
for n in range(3, 7):
    for P in all_posets(n):
        if not P.is_primitive() or not P.connected():
            continue
        totE += 1
        mq, _k = P.min_prefix_Q()
        lo, hi = P.lambda2_bracket(F(1, 10 ** 9))
        for g in (lo, hi):
            if not (0 < g < 1):
                continue
            if (1 - (mq / g) * g) / (1 - g) != (1 - mq) / (1 - g):
                badE += 1
check(badE == 0,
      f"{totE} primitive posets n<=6 on the Sylvester bracket: {badE} failures")
print()
print("  max C_3^gap by n — mg-76b2 s3 (C2)/(C3)'s row, reproduced and EXTENDED to n=7:")
print("     n     max C_3^gap    mg-76b2")
MG = {3: 1.500000, 4: 1.472917, 5: 1.989522, 6: 2.386087}
for n in range(3, 8):
    best = None
    for P in all_posets(n):
        if not P.is_primitive() or not P.connected():
            continue
        mq, _k = P.min_prefix_Q()
        lam2, _v = P.fiedler()
        if lam2 <= 1e-12:
            continue
        r = float(mq) / lam2
        if best is None or r > best:
            best = r
    src = f"{MG[n]:.6f}" if n in MG else "NEW"
    print(f"  {n:4d}     {best:.6f}     {src}")
    if n in MG:
        check(abs(best - MG[n]) < 5e-6, f"n={n}: max C_3^gap matches mg-76b2")
print()
print("  RISING: 1.500, 1.473, 1.990, 2.386, 3.075.  This is the SAME measurement as")
print("  s1's falling `min c`, read in the other currency — and it is measured on the")
print("  same out-of-regime population, so it is a DIRECTION in both currencies and a")
print("  verdict in neither.  Quoting one of them as evidence and not the other would be")
print("  quoting one number twice.")

# --------------------------------------------------------------------- (I2)
print()
print("-" * 78)
print("(I2) THE DEMANDS COINCIDE — chain (IV) IS chain (II)")
print("-" * 78)
print()
print("  THE TWO LINES.  Chain (IV): eps_dem = 1 - (1-eps_leak)/c.  Self-consistently the")
print("  budget IS the gap, eps = eps_dem, and c = (1 - g*eps)/(1 - eps) by (I1) with")
print("  g := C_3^gap.  Substitute:")
print()
print("      1 - eps  =  (1-eps_leak)/c  =  (1-eps_leak)(1-eps)/(1 - g*eps)")
print("      =>  1 - g*eps  =  1 - eps_leak          [divide by (1-eps) != 0]")
print("      =>  eps        =  eps_leak / g          =  chain (II)'s eps_dem.   QED")
print()
print("  Verified numerically over a grid of g, against BOTH chains' own formulae as")
print("  mg-76b2 section 6 writes them:")
print()
print("      g      eps_dem^(II)=eps_leak/g    c=(1-g*eps)/(1-eps)    eps_dem^(IV)")
for g in [F(1), F(3, 2), F(2), F(2386, 1000), F(3075, 1000), F(5), F(10), F(20)]:
    dem2 = EPS_LEAK / g
    c = (1 - g * dem2) / (1 - dem2)
    dem4 = 1 - (1 - EPS_LEAK) / c
    print(f"   {float(g):6.3f}      {float(dem2):.6f}                 {float(c):.6f}"
          f"             {float(dem4):.6f}")
    check(dem4 == dem2, f"g={float(g):.3f}: eps_dem^(IV) == eps_dem^(II) exactly")
print()
print("  >>> CHAIN (IV) DOES NOT BUY A WEAKER DEMAND THAN CHAIN (II).  It buys exactly")
print("      chain (II)'s demand, in a currency where the SAME unknown is written 1/x")
print("      instead of x.  The `10x` in the ticket's framing is chain (II)-or-(IV)")
print("      against chain (III), and mg-9461 already priced it: `the chain choice is")
print("      worth 2/eps_leak = 10x and no more`.")
print()
print("  WHAT CHAIN (IV) *DOES* BUY, and it is real: a WEAKER HYPOTHESIS.  Chain (II)")
print("  assumes min_k Q_k <= g * gap — a RELATIVE bound that forces min_k Q_k -> 0 with")
print("  the gap.  Chain (IV) assumes min_k Q_k <= 1 - c(1-gap) — an ABSOLUTE bound that")
print("  permits min_k Q_k ~ 1-c however small the gap gets.  On the class {gap<=eps_spec}")
print("  the two hypotheses deliver the same conclusion, but (IV)'s is strictly easier to")
print("  prove.  THAT is chain (IV)'s advantage, and it is an advantage in PROVABILITY,")
print("  not in the constant.")

# --------------------------------------------------------------------- (I3)
print()
print("-" * 78)
print("(I3) WHAT `eps_dem = 0.20` COSTS")
print("-" * 78)
print()
c1 = F(1)
print(f"  eps_dem^(IV) = 1 - (1-eps_leak)/c = eps_leak = {float(EPS_LEAK)}  requires  c = 1 EXACTLY.")
print("  By (I1), c = 1  <=>  min_k Q_k = gap  <=>  C_3^gap = 1 EXACTLY: some prefix's")
print("  centred indicator IS a minimiser of the Rayleigh quotient over H.")
print()
print("  THAT IS THE `C_3 = 1` WHOSE GAP-FORM READING IS ALREADY MEASURED FALSE.")
print("  STATE.md row :164 and mg-94c3 section 3: over the 1032 primitive posets")
print("  exhibiting L2's first disjunct, C_3^gap exceeds 1 at 1023 of them.  So c < 1 on")
print("  1023 of 1032, and eps_dem^(IV) < 0.20 on all of them.")
print()
print("  HOW MUCH LESS IS THE WHOLE QUESTION, and it is NOT settled by that measurement,")
print("  because 1023/1032 is measured OUT OF REGIME exactly as s1's family is.  On the")
print("  two families that DO reach the regime (s2 R3), c = 0.99990 and 0.99996, giving")
for cc in [F(9998969, 10 ** 7), F(9999555, 10 ** 7)]:
    print(f"      c = {float(cc):.7f}   ->   eps_dem^(IV) = {float(1 - (1-EPS_LEAK)/cc):.6f}")
print("  — i.e. essentially the full 0.20.  THE TICKET'S PREMISE SURVIVES ON THE ONLY")
print("  POSETS ANYONE HAS EXHIBITED INSIDE THE REGIME.  It is not established, because")
print("  two families are not a class.")

# --------------------------------------------------------------------- (I4)
print()
print("-" * 78)
print("(I4) NEGATIVE CONTROL — a chain (IV) that DOES pay the Cheeger square must fail")
print("-" * 78)
print()
print("  The mis-derivation: read the literal conjecture through Cheeger's hard half, so")
print("  the deliverable is Phi <= sqrt(2(1 - c(1-eps_spec))) instead of 1 - c(1-eps_spec).")
print("  Its demand solves sqrt(2(1-c(1-eps))) = eps_leak, i.e. eps_dem_bad = ")
print("  (1 - (1-eps_leak^2/2)/c).  If (I2) were vacuous arithmetic this would also")
print("  reproduce eps_leak/g; it must not.")
agree = disagree = 0
for g in [F(1), F(3, 2), F(2), F(5), F(10)]:
    dem2 = EPS_LEAK / g
    c = (1 - g * dem2) / (1 - dem2)
    dem_bad = 1 - (1 - EPS_LEAK ** 2 / 2) / c
    if dem_bad == dem2:
        agree += 1
    else:
        disagree += 1
    print(f"   g={float(g):5.2f}   correct eps_dem = {float(dem2):.6f}   "
          f"square-paying variant = {float(dem_bad):.6f}   "
          f"{'AGREES (bad)' if dem_bad == dem2 else 'differs (good)'}")
check(agree == 0 and disagree == 5,
      f"the square-paying variant disagrees at all {disagree} grid points — (I2) is not vacuous")

# --------------------------------------------------------------------- (I5)
print()
print("-" * 78)
print("(I5) THE WALL, PRICED IN THE ONE UNKNOWN")
print("-" * 78)
print()
print("  The supply side is eps_sup = 1 (pair bias, PROVEN, and an EQUALITY for the")
print("  information it consumes — mg-6bc2 Claim 3.1).  The distance to the wall is")
print("  eps_sup / eps_dem, and by (I2) that is g / eps_leak = 5g:")
print()
print("      C_3^gap = g       eps_dem = eps_leak/g      wall factor = 5g")
for g in [F(1), F(3, 2), F(2386, 1000), F(3075, 1000), F(10)]:
    print(f"        {float(g):6.3f}              {float(EPS_LEAK/g):.6f}                {float(5*g):6.2f}x")
print()
print("  SO THE 5x REFRAMING IS THE g = 1 ROW, AND ONLY THAT ROW.  It is the best case of")
print("  the one unknown, not a property of chain (IV).  At the largest g this corpus has")
print("  measured (3.075, n = 7, out of regime) the wall is 15x; at g = 10 — the value at")
print("  which chain (IV) stops closing at all — it is 50x, which is chain (III)'s figure.")
print("  The Cheeger square is not avoided by chain (IV); it is REFINANCED, and g is the")
print("  interest rate.")
print()
print("=" * 78)
print(f"s3 VERDICT: {'ALL CHECKS PASS' if fail == 0 else str(fail) + ' FAILURES'} — "
      "chain (IV)'s c and chain (II)'s C_3^gap are one unknown;")
print("their demands are algebraically equal; and `eps_dem = 0.20` is the g = 1 extreme,")
print("not a figure any measurement in this corpus supports.")
print("=" * 78)
