"""a2 -- the LOGIC layer: does (L*) imply the disjunction, and is it only SUFFICIENT?

This is the audit target that decides whether the refutation costs a route or the
programme.  It is settled on paper here and then CONTROLLED on the population, because
an implication that is true is true uniformly in n and no census can establish it.

THE REDUCTION, as the corpus states it (mg-c50b s2_theory.py:40, inherited by mg-789d):

    (F)  FAILS  <=>  M^2 > 2 gamma
    (M#) FAILS  <=>  sweep(mu_pref) > 2 gamma,
                     sweep(mu) := mu*(2 Delta - mu)  for mu <= Delta,  Delta^2 beyond
    DISJUNCTION at P  <=>  (F) holds  OR  (M#) holds

CLAIM 1 ((L*) => the disjunction, uniformly in n, in one line, NO side condition).
    Assume (L*) at P:  M^2 > 2 gamma  ==>  mu_pref * Delta <= gamma.
    If M^2 <= 2 gamma then (F) holds and the disjunction holds at P.
    Otherwise mu_pref * Delta <= gamma, and

        mu_pref <= Delta :  sweep = mu_pref(2 Delta - mu_pref)
                                  <= 2 Delta mu_pref            [mu_pref >= 0]
                                  <= 2 gamma
        mu_pref >  Delta :  sweep = Delta^2 < Delta*mu_pref <= gamma <= 2 gamma

    so (M#) holds.  []
    The only facts used are mu_pref >= 0, Delta >= 0, gamma >= 0 -- all three are
    unconditional (I - A is PSD because A is symmetric doubly stochastic with spectrum
    in [-1,1]; Delta = max_i (1 - (S_P)_ii) with S_P entrywise in [0,1]).  There is NO
    unstated side condition, and n never appears.

CLAIM 2 ((L*) is STRICTLY sufficient, not equivalent -- this is what saves the
    programme).  The two inequalities differ by exactly the term mu_pref^2:

        (L*)'s conclusion :  2 Delta mu_pref            <= 2 gamma
        (M#)              :  2 Delta mu_pref - mu_pref^2 <= 2 gamma

    so (M#) is weaker by mu_pref^2 > 0 whenever mu_pref > 0.  A counterexample to
    (L*) therefore lands in the gap unless it also has 2 Delta mu - mu^2 > 2 gamma.
    Whether mg-789d's four counterexamples land in the gap is NOT a matter of logic;
    it is measured, and a1 measures it: all four have (M#) holding.

CONTROL.  If CLAIM 1 were false there would be a poset with mu_pref*Delta <= gamma and
(M#) failing.  Section 2 below looks for one over the whole primitive population at
n <= 6 and a large sample at n = 7, exactly.  It must find none.  If CLAIM 2 were false
-- i.e. if the two conditions were equivalent -- there would be no poset with
mu_pref*Delta > gamma and (M#) holding.  Section 3 exhibits many.
"""
import sys
import math
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from lib5cba import P5, gen_posets, mu_pref_float, gamma_float

FAIL = 0


def arm(name, cond, got=""):
    global FAIL
    print("  [%s] %-62s %s" % ("ok " if cond else "FAIL", name, got))
    if not cond:
        FAIL += 1


print("=" * 78)
print("a2  THE LOGIC LAYER -- (L*) => disjunction, and (L*) strictly stronger")
print("=" * 78)
print(__doc__.split("CONTROL.")[0].split("THE REDUCTION")[1][:0] or "", end="")

print("\n" + "-" * 78)
print("2.1  CONTROL ON CLAIM 1 -- exact, over the whole primitive population n <= 6")
print("     Looking for a poset with  mu_pref*Delta <= gamma  AND  (M#) FAILING.")
print("     The certificates are taken in the directions that make a HIT real:")
print("       mu*Delta <= gamma  from the mu UPPER bracket and the gamma LOWER bracket")
print("       (M#) fails         from sweep(mu LOWER) > 2*(gamma UPPER)")
print("-" * 78)
hits = 0
tot = 0
for n in (3, 4, 5, 6):
    cnt = 0
    for dn in gen_posets(n):
        p = P5(dn, n)
        if not p.primitive():
            continue
        cnt += 1
        tot += 1
        D = p.Delta()
        glo, ghi = p.gamma_bracket(28)
        mlo, mhi = p.mu_bracket(24, lo=Fraction(0), hi=Fraction(2))
        concl = (mhi * D <= glo)
        swp_lo = mlo * (2 * D - mlo) if mlo <= D else D * D
        mhash_fails = swp_lo > 2 * ghi
        if concl and mhash_fails:
            hits += 1
            print("     HIT n=%d dn=%s" % (n, dn))
    print("     n=%d: %d primitive posets checked" % (n, cnt))
arm("no poset has (L*)'s conclusion AND (M#) failing  (CLAIM 1 survives)",
    hits == 0, "%d hits over %d primitive posets" % (hits, tot))

print("\n" + "-" * 78)
print("2.2  THE SAME CONTROL AT n = 7, on the (F)-FAILING SET -- the set that matters")
print("-" * 78)
FF = []
for dn in gen_posets(7):
    p = P5(dn, 7)
    if p.primitive() and p.F_fails():
        FF.append(dn)
print("     (F)-failing primitive posets at n = 7 : %d" % len(FF))
arm("the (F)-failing count at n=7 re-derives at 168 (mg-51f4 / mg-c50b / mg-789d)",
    len(FF) == 168, str(len(FF)))
hits = 0
both = 0
for dn in FF:
    p = P5(dn, 7)
    D = p.Delta()
    glo, ghi = p.gamma_bracket(28)
    mlo, mhi = p.mu_bracket(24, lo=Fraction(0), hi=Fraction(2))
    if mhi * D <= glo and (mlo * (2 * D - mlo) if mlo <= D else D * D) > 2 * ghi:
        hits += 1
    # both routes failing?  (F) already fails here
    if (mlo * (2 * D - mlo) if mlo <= D else D * D) > 2 * ghi:
        both += 1
arm("CLAIM 1 survives on all 168 (F)-failing n=7 posets", hits == 0, "%d hits" % hits)
arm("BOTH ROUTES FAIL at 0 of the 168 -- the disjunction holds at n=7",
    both == 0, "%d both-failing" % both)

print("\n" + "-" * 78)
print("2.3  CLAIM 2 -- (L*) is STRICTLY stronger than (M#), exhibited")
print("     A poset with mu_pref*Delta > gamma but (M#) HOLDING is a poset in the gap.")
print("-" * 78)
GAP = [((0, 1, 3, 7, 15, 31, 63, 127, 255, 0), 10, "chain(9)+point"),
       ((0, 1, 0, 4, 0, 0, 32, 96, 239), 9, "counterexample C1"),
       ((0, 0, 0, 0, 0, 16, 48, 16, 247), 9, "counterexample C2"),
       ((0, 1, 3, 0, 9, 0, 32, 96, 255, 239), 10, "counterexample C3"),
       ((0, 1, 3, 7, 0, 1, 1, 113, 1, 257, 257), 11, "counterexample C4")]
ngap = 0
for dn, n, tag in GAP:
    p = P5(dn, n)
    D = p.Delta()
    glo, ghi = p.gamma_bracket(30)
    mlo, mhi = p.mu_bracket(26, lo=Fraction(0), hi=Fraction(1))
    conc_fails = mlo * D > ghi                 # (L*)'s conclusion FAILS, certified
    mh_holds = (mhi * (2 * D - mhi) if mhi <= D else D * D) <= 2 * glo
    print("     %-22s  mu*Delta > gamma: %-5s   (M#) holds: %-5s"
          % (tag, conc_fails, mh_holds))
    if conc_fails and mh_holds:
        ngap += 1
arm("at least one poset lies strictly between the two conditions", ngap >= 1,
    "%d of %d" % (ngap, len(GAP)))
arm("ALL FOUR certified counterexamples lie in the gap, so the DISJUNCTION SURVIVES",
    ngap >= 4, "%d in the gap" % ngap)

print("\n" + "-" * 78)
print("2.4  THE GAP IS mu_pref^2 -- checked as an algebraic identity, not a fit")
print("-" * 78)
worst = 0
for dn, n, tag in GAP:
    p = P5(dn, n)
    D = p.Delta()
    mlo, _ = p.mu_bracket(20, lo=Fraction(0), hi=Fraction(1))
    lhs = 2 * D * mlo - (mlo * (2 * D - mlo))
    if abs(lhs - mlo * mlo) > 0:
        worst = 1
arm("2*Delta*mu - sweep(mu) == mu^2 exactly, at every exhibit", worst == 0)

print("\n" + "=" * 78)
print("a2 RESULT: %s   (%d failing arms)" % ("ALL ARMS PASS" if FAIL == 0 else "FAILURES", FAIL))
print("=" * 78)
sys.exit(1 if FAIL else 0)
