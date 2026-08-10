"""a4 -- STEP D.  BOTH routes fail at the same poset, and by how much.

(F) failing here is already known -- mg-5cba published it.  The NEW claim is that
(M#) fails at the SAME poset, and that is what makes the disjunction false.

THE DEFINITIONS, taken from the corpus and then USED rather than paraphrased:

    (F)   holds  <=>  gamma >= M^2/2                       f* := M^2/(2*gamma) <= 1
    (M#)  holds  <=>  2*Delta*mu_pref - mu_pref^2 <= 2*gamma
                                                           c# := sweep/(2*gamma) <= 1
    sweep(mu,Delta) := 2*Delta*mu - mu^2
    t*    := Delta - sqrt(Delta^2 - 2*gamma)               u_M := mu_pref/t*

    (M#) fails <=> c# > 1 <=> u_M > 1     -- the equivalence is DERIVED below, not
    quoted, because two of the three published figures are stated in one form and one
    in the other.

ONE STEP THAT IS NOT AUTOMATIC, and the ticket's own summary states it in a form that
does not carry it.  The chain

    mu_pref >= m_lo   and   sweep(m_lo,Delta) > 2*g_ub > 2*gamma   ==>   (M#) fails

needs sweep to be NONDECREASING between m_lo and mu_pref.  sweep(mu) = 2*Delta*mu -
mu^2 rises on [0,Delta] and FALLS after it, so `m_lo <= Delta` -- which is the
condition as the work item states it -- is not by itself enough: what is needed is
`mu_pref <= Delta`.  Under the corpus's own clamped reading of the sweep (its §2
survival proof evaluates `sweep = Delta^2` when `mu_pref > Delta`) the stated
condition IS sufficient, so this is a seam between two readings and not an error.
This arm removes the question instead of adjudicating it: a3.2 certifies
mu_pref <= Delta with an exhibited vector, so the verdict holds under EITHER reading,
and both are evaluated below and shown to agree here.
"""
import sys
from fractions import Fraction as Fr
from common5e82 import G_UB, M_LO, build, banner, isqrt_frac
import lib5e82 as L

ok = True


def check(label, got, want):
    global ok
    good = got == want
    ok = ok and good
    print("  [%s] %-58s got=%s want=%s" % ("ok " if good else "FAIL", label, got, want))


banner("a4  STEP D -- BOTH ROUTES FAIL AT THE SAME POSET")
P = build()
D, M = P.Delta, P.M
print("  Delta = %s   M = %s   LE = %d" % (D, M, P.LE))
print("  gamma   <  g_ub = %d/%d = %.15f    [a2, PSD refusal]" % (G_UB.numerator, G_UB.denominator, float(G_UB)))
print("  mu_pref >= m_lo = %d/%d = %.15f    [a3, copositivity]" % (M_LO.numerator, M_LO.denominator, float(M_LO)))
print()

banner("a4.1  ROUTE (F)")
half = M * M / 2
print("  M^2/2 = %s = %.15f" % (half, float(half)))
print("  g_ub  =                    %.15f" % float(G_UB))
check("g_ub < M^2/2, hence gamma < M^2/2", G_UB < half, True)
print("  ==> (F) FAILS.")
print("  f* = M^2/(2*gamma) > (M^2/2)/g_ub = %.9f" % float(half / G_UB))
check("f* > 1", half / G_UB > 1, True)
print()

banner("a4.2  ROUTE (M#) -- THE NEW CLAIM")
sweep_lo = 2 * D * M_LO - M_LO * M_LO
print("  sweep(m_lo,Delta) = 2*Delta*m_lo - m_lo^2")
print("                    = %s" % sweep_lo)
print("                    = %.15f" % float(sweep_lo))
print("  2*g_ub            = %.15f" % float(2 * G_UB))
margin = sweep_lo - 2 * G_UB
print()
print("  EXACT MARGIN sweep - 2*g_ub =")
print("    %s" % margin)
print("    = %.12f" % float(margin))
print("  cb417 reports              +0.002790801218")
check("the margin is positive", margin > 0, True)
check("the margin agrees with cb417 to 12 places",
      "%.12f" % float(margin), "0.002790801218")
print()
print("  THE THREE SIDE CONDITIONS")
check("m_lo <= Delta", M_LO <= D, True)
# mu_pref <= Delta is the one the chain actually needs, and it must be EXHIBITED here
# rather than cited: my first draft wrote this as check(..., True, True), a clause that
# cannot fail, inside the arm whose whole subject is a bound nobody computed.  Any
# c >= 0 gives an upper bound on mu_pref; the standard basis vectors are the cheapest.
ubs = [(P.Q[k][k] / P.N[k][k], k) for k in range(P.m)]
mu_ub, kbest = min(ubs)
print("  mu_pref <= Q_kk/N_kk at k=%d (i.e. at c = e_%d >= 0) = %.15f"
      % (kbest, kbest, float(mu_ub)))
check("mu_pref <= Delta, by that exhibited vector", mu_ub <= D, True)
check("Delta^2 > 2*g_ub  (so t* is real)", D * D > 2 * G_UB, True)
print()
print("  BOTH READINGS OF `sweep`, evaluated:")
print("    unclamped  2*D*mu - mu^2            at m_lo: %.15f" % float(sweep_lo))
clamped = 2 * D * min(M_LO, D) - min(M_LO, D) ** 2
print("    clamped    at min(mu,Delta)         at m_lo: %.15f" % float(clamped))
check("the two readings agree here (because m_lo < Delta)", sweep_lo, clamped)
print()
print("  ==> 2*Delta*mu_pref - mu_pref^2 >= sweep(m_lo,Delta) > 2*g_ub > 2*gamma")
print("  ==> (M#) FAILS.")
print("  c# = sweep/(2*gamma) > sweep(m_lo)/(2*g_ub) = %.9f" % float(sweep_lo / (2 * G_UB)))
check("c# > 1", sweep_lo / (2 * G_UB) > 1, True)
print()

banner("a4.3  THE PUBLISHED FIGURES")
cs = sweep_lo / (2 * G_UB)
fs = half / G_UB
print("  min(c#, f*) >= %.9f      cb417 reports 1.022616164" % float(min(cs, fs)))
check("min(c#,f*) agrees to 9 places", "%.9f" % float(min(cs, fs)), "1.022616164")
check("min(c#,f*) > 1  -- BOTH ROUTES FAIL", min(cs, fs) > 1, True)
print()
disc = D * D - 2 * G_UB
slo, shi = isqrt_frac(disc)
# gamma < g_ub  =>  Delta^2-2gamma > disc  =>  sqrt bigger  =>  t* smaller than this
tstar_ub = D - slo
print("  t* = Delta - sqrt(Delta^2 - 2*gamma)")
print("     < Delta - sqrt(Delta^2 - 2*g_ub) < %.15f     (an UPPER bound on t*)" % float(tstar_ub))
check("sqrt bracket verified by squaring", slo * slo <= disc <= shi * shi, True)
uM = M_LO / tstar_ub
print("  u_M = mu_pref/t* >= m_lo/that = %.9f      cb417 reports 1.023413503" % float(uM))
check("u_M agrees to 9 places", "%.9f" % float(uM), "1.023413503")
check("u_M > 1", uM > 1, True)
check("mu_pref > t*, the direct form of the (M#) failure", M_LO > tstar_ub, True)
print()
print("  THE TWO FORMS AGREE, and here is why rather than that they do:")
print("  sweep(mu) - 2*gamma = -(mu - t*)(mu - t**) with t** = Delta + sqrt(Delta^2-2gamma),")
print("  so for mu in (t*, t**) the sweep exceeds 2*gamma.  mu_pref <= Delta < t**, so")
print("  c# > 1  <=>  mu_pref > t*  <=>  u_M > 1.")
tstar_lo_ish = D + slo
check("mu_pref <= Delta < t** (so the second root is not in play)", D < tstar_lo_ish, True)
print()

banner("a4.4  THE SAME VERDICT FROM THE DECIMALS mg-5cba PUBLISHED ON MAIN")
from common5e82 import G_UB_PUBLISHED, M_LO_PUBLISHED
sw2 = 2 * D * M_LO_PUBLISHED - M_LO_PUBLISHED * M_LO_PUBLISHED
m2 = sw2 - 2 * G_UB_PUBLISHED
print("  using only  gamma <= 0.061699262  and  mu_pref >= 0.065579592  (both on main):")
print("    sweep - 2*gamma_ub = %.10f" % float(m2))
check("the counterexample is already implied by the PUBLISHED decimals", m2 > 0, True)
print("  pm-onethird's own hand check reports +0.0027907976; this arm gets %.10f" % float(m2))
print()
banner("a4 VERDICT: %s" % ("ALL ARMS SATISFACTORY" if ok else "*** AN ARM FAILED ***"))
sys.exit(0 if ok else 1)
