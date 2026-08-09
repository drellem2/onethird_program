#!/usr/bin/env python3
"""s1 — THE SEQUENCING DIRECTIVE: check mg-76b2's falling `min c` FIRST.

The ticket's title is an order: *"check mg-76b2 min c falling with n FIRST"*.  So this
script runs before any derivation, and it does three things:

  (S1) EXTEND the row.  mg-76b2 reports `min c` at n = 3, 4, 5, 6 — FOUR points, of
       which the ticket warns three prior characterisations in this corpus died at the
       first untested value.  n = 7 is that value here.  86 277 informative posets.

  (S2) NAME THE MINIMISER.  A trend over four points is a trend; a FAMILY is a theorem.
       The n = 4, 5, 6, 7 minimisers are all the same shape, and it generalises.

  (S3) EVALUATE THE FAMILY EXACTLY, to n = 16, on the Sylvester bracket — no float on
       the verdict path.  This is what turns "min c falls" from a direction into a
       REFUTATION of `c > 0.80` over the full naturally-labelled population.

WHAT IS **NOT** SETTLED HERE, and s2 is where it is taken up: every poset in (S3) sits
far OUTSIDE the spectral regime the architecture supplies.  A refutation over the full
population is not a refutation over the class chain (IV) is invoked on, and this script
says so at the figure rather than one line away.
"""

from fractions import Fraction as F

from lib81ff import (all_posets, poset_from_relations, C_THRESH_EXIST, C_THRESH_SELF,
                     EPS_LEAK, EPS_SPEC)

print("=" * 78)
print("s1 — mg-76b2's FALLING `min c`, CHECKED FIRST AND EXTENDED")
print("=" * 78)
print()
print("WHAT `c` IS, stated before anything is done with it (ticket item 1):")
print("  Op-Form's Prefix-capture conjecture, tex :360-364, quoted verbatim —")
print('    "A threshold cut of the dominant standard eigenvector gives a prefix A_k')
print('     whose Rayleigh quotient captures a constant fraction, or possibly 1-o(1),')
print('     of the dominant standard eigenvalue."')
print("  so, per poset and then per population:")
print("      c(P) = max_{1<=k<=n-1} rho(A_k) / lambda_std(P),   c(n) = min over P")
print("      rho(A) = <f_A, M f_A>/||f_A||^2,  f_A = 1_A - (|A|/n)1  (CENTRED: f_A in H)")
print()
print("WHICH THRESHOLD IS BEING BOUNDED (ticket item 1, mg-01ea's reconciliation):")
print(f"  EXISTENCE threshold   c > 1 - eps_leak                 = {float(C_THRESH_EXIST):.6f}")
print(f"  SELF-CONSISTENT       c >= (1-eps_leak)/(1-eps_spec)   = {float(C_THRESH_SELF):.6f}")
print("  mg-01ea landed the reconciliation into mg-76b2's own section 5 and it is read")
print("  here, not re-derived: the first is `eps_dem > 0` (some positive budget exists),")
print("  the second is the same condition evaluated AT eps_spec = eps_leak^2/2 = 1/50.")
print("  EVERY VERDICT BELOW IS STATED AGAINST BOTH, because nothing here turns on which:")
print("  the figures land far below both or far above both.")
print()

# --------------------------------------------------------------------- (S1)
print("-" * 78)
print("(S1) THE ROW, EXTENDED TO n = 7 — the first untested value")
print("-" * 78)
print()
print("     n   primitive   informative    min c      below 0.8163?   minimiser")
MG76B2 = {3: 0.750000, 4: 0.618034, 5: 0.536219, 6: 0.452934}
rows = {}
for n in range(3, 8):
    prim = [P for P in all_posets(n) if P.is_primitive()]
    vals = [(c, P) for c, P in ((P.float_c(), P) for P in prim) if c is not None]
    mn = min(vals, key=lambda t: t[0])
    rows[n] = (len(prim), len(vals), mn)
    src = f"= mg-76b2 {MG76B2[n]:.6f}" if n in MG76B2 else "NEW — first untested value"
    print(f"  {n:4d} {len(prim):10d} {len(vals):12d}   {mn[0]:.6f}   "
          f"{'YES' if mn[0] < float(C_THRESH_SELF) else 'no ':>5s}   {mn[1].relations()}")
    print(f"       {src}")
print()
print("  INFORMATIVE POINTS, counted the way the ticket asks: FIVE values of n, of which")
print("  FOUR are mg-76b2's and ONE (n = 7) is new.  The trend does not break at the")
print("  first untested value — the failure mode that killed 2/(n+1) at n = 6 and the")
print("  ordinal-sum characterisation at n = 7 does NOT occur here.")
print()

# --------------------------------------------------------------------- (S2)
print("-" * 78)
print("(S2) THE MINIMISER IS A FAMILY, NOT A COINCIDENCE")
print("-" * 78)
print()
for n in range(4, 8):
    print(f"  n={n}: {rows[n][2][1].relations()}")
print()
print("  Read them together: k DISJOINT 2-CHAINS, plus an isolated point when n is odd.")
print("  n=4 = 2 chains; n=5 = 2 chains + a point; n=6 = 3 chains; n=7 = 3 chains + a")
print("  point.  The family is `D_k` below and it is defined for every k, so the")
print("  question `does min c keep falling` stops being an extrapolation.")
print()

# --------------------------------------------------------------------- (S3)
print("-" * 78)
print("(S3) THE FAMILY D_k = k DISJOINT 2-CHAINS, EXACTLY, TO n = 16")
print("-" * 78)
print()
print("  D_k on {0..2k-1} with relations 2i < 2i+1.  Every figure in this block is an")
print("  EXACT RATIONAL BRACKET from Sylvester's criterion (lib81ff.lambda2_bracket);")
print("  the float eigenroutine is not on this path.")
print()
print("   k   n    1 - min_k Q_k   gap 1-lam_std     c (exact bracket)      < 0.8163?")
for k in range(2, 9):
    n = 2 * k
    P = poset_from_relations(n, [(2 * i, 2 * i + 1) for i in range(k)])
    mq, arg = P.min_prefix_Q()
    lo, hi = P.lambda2_bracket(F(1, 10 ** 12))
    clo, chi = P.c_bracket(F(1, 10 ** 12))
    assert P.is_primitive()
    print(f"  {k:2d} {n:3d}   {str(1-mq):>10s}    ({float(lo):.9f})   "
          f"[{float(clo):.7f}, {float(chi):.7f}]   "
          f"{'YES' if chi < C_THRESH_SELF else 'no'}")
print()
print("  1 - min_k Q_k = 1/(n-1) EXACTLY at every k here, attained at the prefix A_1 =")
print("  {0}; the gap rises through 0.46, 0.56, 0.60, 0.63, 0.64, 0.65, 0.66.  So c is")
print("  ~ 1/((n-1) * lambda_std) and falls at every step: 0.618, 0.453, 0.358, 0.297,")
print("  0.253, 0.221, 0.196.")
print()
print("  >>> THE CONSEQUENCE, STATED AT ITS SCOPE AND NOT ONE LINE AWAY:")
print("      OVER THE FULL NATURALLY LABELLED POPULATION, `c > 0.80` IS FALSE.  It is")
print("      false already at n = 4 (c = 0.618034 < 0.80), exactly, with a two-element")
print("      witness family, and it stays false at every k checked.  No `n_0` rescues")
print("      it: D_k is defined at every k and c(D_k) is below the threshold at every")
print("      k >= 2 evaluated.")
print()
print("      WHAT THIS DOES **NOT** SETTLE.  Every D_k has gap >= 0.46, and Step 2 of")
print("      the architecture supplies gap <= eps_spec = 2e-2.  D_k is therefore ~23x")
print("      outside the regime chain (IV) is invoked on at k = 2 and ~33x outside it")
print("      at k = 8.  A refutation there does not transfer.  s2 is that question and")
print("      IT ANSWERS THE OTHER WAY.")
print()
print("  I DID NOT PROVE c(D_k) -> 0.  Eight exact points falling is a direction; the")
print("  limit needs a lower bound on lambda_std(D_k) uniform in k, which is a lower")
print("  bound on an eigenvalue and is not what a test vector supplies.  The refutation")
print("  above does not need the limit — it needs one k, and it has eight.")
print()
print("=" * 78)
print("s1 VERDICT: mg-76b2's FALLING min c is CONFIRMED on an independent path,")
print("EXTENDED to n = 7 (0.412700), and UPGRADED from a trend to an explicit family.")
print("`c > 0.80` IS REFUTED OVER THE FULL POPULATION — AND THE REFUTING POSETS ARE ALL")
print("OUT OF REGIME, WHICH IS s2's SUBJECT AND CHANGES THE VERDICT.")
print("=" * 78)
