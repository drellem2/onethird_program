#!/usr/bin/env python3
"""a2_maths — AUDIT TARGET 2: the parent's own mathematics, BY RE-DERIVATION.

Two results are proved in mg-c3ca and are its actual mathematical content:
  Sec.1  the mass-profile IFF:  (LIB-weak) <=> for every alpha>0, #{x: m_x >= alpha n} = o(n)
  Sec.4  Prop 4.1 the entropy price: E[inv_e] <= eps n^2  =>  e(P) <= 2 C(2 eps n^2 + n, n)

Both are re-derived by hand in the audit document.  This file does the thing reading
cannot do: instantiates them on every poset in the population and looks for a violation,
and then measures HOW MUCH ROOM the inequality has, because an inequality that is loose
by three orders of magnitude has been confirmed as an inequality and not as an argument.
"""
import sys
from fractions import Fraction
from math import comb, log
import lib_c4f5 as L

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7

print("=" * 78)
print("a2_maths -- the parent's Sec.1 IFF and Sec.4 Prop 4.1, re-derived numerically")
print("POPULATION: every naturally labelled poset on n elements.  GRAIN: one poset.")
print("EXACT: everything here is Fraction/int arithmetic.  No tolerance.")
print("=" * 78)

print()
print("-" * 78)
print("A. Sec.1 -- the identity the IFF runs on: sum_x m_x = 2 E[inv]")
print("-" * 78)
worst = Fraction(0)
tot = 0
for n in range(2, NMAX + 1):
    for P in L.gen_natural_posets(n):
        a = L.analyse(P)
        d = abs(sum(a["m"]) - 2 * a["inv"])
        if d > worst:
            worst = d
        tot += 1
print("  posets checked: %d      max |sum m_x - 2E[inv]| = %s" % (tot, worst))
print("  (already in the selftest at n<=6; repeated here at the audit's own NMAX)")

print()
print("-" * 78)
print("B. Sec.1 -- BOTH DIRECTIONS OF THE IFF, as finite-n inequalities")
print("-" * 78)
print("The proof is two Markov steps.  At finite n they are these two inequalities,")
print("and if either failed the iff would be wrong:")
print("   (=>)  #{x : m_x >= alpha n}  <=  2 E[inv] / (alpha n)")
print("   (<=)  sum_x m_x  <=  #{x : m_x >= alpha n} * n  +  alpha n * n")
bad_fwd = bad_bwd = 0
tested = 0
for n in range(2, NMAX + 1):
    for P in L.gen_natural_posets(n):
        a = L.analyse(P)
        for alpha in (Fraction(1, 10), Fraction(1, 4), Fraction(1, 2), Fraction(9, 10)):
            k = sum(1 for v in a["m"] if v >= alpha * n)
            if Fraction(k) > 2 * a["inv"] / (alpha * n):
                bad_fwd += 1
            if sum(a["m"]) > Fraction(k * n) + alpha * n * n:
                bad_bwd += 1
            tested += 1
print("  %d (poset, alpha) instances;  (=>) violations %d ;  (<=) violations %d"
      % (tested, bad_fwd, bad_bwd))
print("  P4 predicted 0 and 0.")

print()
print("-" * 78)
print("C. Sec.1 -- THE QUANTIFIER IN THE Sec.3 TABLE (P4's predicted defect)")
print("-" * 78)
print("Sec.1 states the iff correctly:")
print('    (LIB-weak) <=> for every alpha>0, #{x : m_x >= alpha n} = o(n).')
print("Sec.3's table states its NEGATION as:")
print('    "#{x : m_x >= alpha n} = Omega(n) for some alpha > 0"')
print("The correct negation of `= o(n)` is `is NOT o(n)`, i.e. limsup count/n > 0,")
print("which permits a SUBSEQUENCE.  Omega(n) as normally read demands it at EVERY n.")
print("This is strictly stronger than the negation, so the table's row is a slightly")
print("stronger claim than the section it cites.  Consequence: NONE for the verdict --")
print("a (LIB-weak) violator along a subsequence is still a violator.")
print("  VERDICT: substance CONFIRMED, one quantifier written too strongly. NO CONSEQUENCE.")

print()
print("-" * 78)
print("D. Sec.4 Prop 4.1 -- the entropy price, instantiated")
print("-" * 78)
print("Claim: E[inv_e] <= eps n^2  ==>  e(P) <= 2 * C(2 eps n^2 + n, n).")
print("Instantiated at eps = E[inv]/n^2, i.e. e(P) <= 2 * C(floor(2E[inv]) + n, n).")
print("NOTE the reference order: Prop 4.1's coding counts inversions of sigma against e")
print("OVER ALL PAIRS, and inv_e counts only INCOMPARABLE pairs.  They coincide only")
print("because e is a linear extension (P6).  Tested with L = the natural labelling,")
print("which IS a linear extension, so the identification is legitimate here.")
print()
print("%3s %8s %8s %14s %14s" % ("n", "posets", "viol", "median ratio", "min ratio"))
for n in range(2, NMAX + 1):
    viol = 0
    ratios = []
    cnt = 0
    for P in L.gen_natural_posets(n):
        a = L.analyse(P)
        K = 2 * a["inv"]                       # Markov threshold, exact Fraction
        Kf = int(K) if K == int(K) else int(K) + 1
        rhs = 2 * comb(Kf + n, n)
        cnt += 1
        if a["eP"] > rhs:
            viol += 1
        ratios.append(rhs / a["eP"])
    ratios.sort()
    print("%3d %8d %8d %14.4g %14.4g"
          % (n, cnt, viol, ratios[len(ratios) // 2], ratios[0]))
print()
print("  P5 predicted 0 violations and a median ratio > 1e3 at n=7.")
print("  Read the ratio column as the honest statement of what this check is: the bound")
print("  is a CONSISTENCY check at this size, not a sharpness check.  A bound loose by")
print("  three orders of magnitude cannot be falsified by a population this small, and")
print("  saying `0 violations` without the ratio would overstate what was tested.")

print()
print("-" * 78)
print("E. Sec.4 -- WHERE Prop 4.1 IS TIGHT, i.e. is it ever within a factor 10?")
print("-" * 78)
for n in range(2, min(NMAX, 7) + 1):
    best = None
    for P in L.gen_natural_posets(n):
        a = L.analyse(P)
        K = 2 * a["inv"]
        Kf = int(K) if K == int(K) else int(K) + 1
        r = 2 * comb(Kf + n, n) / a["eP"]
        if best is None or r < best[0]:
            best = (r, a["up"], a["eP"], float(a["inv"]))
    print("  n=%d tightest ratio %.4g at up=%s (e(P)=%d, E[inv]=%.4g)"
          % (n, best[0], best[1], best[2], best[3]))
print("  (the chain is the tightest case: E[inv]=0, e(P)=1, rhs=2 -> ratio 2)")

print()
print("-" * 78)
print("F. Sec.4's ASYMPTOTIC FORM, checked as arithmetic rather than instantiated")
print("-" * 78)
print("e(P)/n! <= 2 (2 e^2 eps + e^2/n)^n.  Derivation re-done here:")
print("  C(a,n) <= (ea/n)^n with a = 2 eps n^2 + n  gives  (2 e eps n + e)^n")
print("  n! >= (n/e)^n")
print("  ratio <= 2 (2 e eps n + e)^n / (n/e)^n = 2 (2 e^2 eps + e^2/n)^n     [matches]")
import math
E = math.e
for n in (10, 100, 1000):
    for eps in (0.1, 0.01, 0.001):
        v = 2 * E * eps * n + E
        lhs = 2 * (v / (n / E)) ** 1
        print("    n=%5d eps=%-7g  base 2e^2*eps + e^2/n = %.6g   (<1 iff the bound bites)"
              % (n, eps, 2 * E * E * eps + E * E / n))
print("  The bound bites (base < 1) only once 2e^2 eps < 1, i.e. eps < %.5g." % (1 / (2 * E * E)))
print("  So Prop 4.1 is VACUOUS for eps >= %.5g -- true but empty." % (1 / (2 * E * E)))
print("  mg-c3ca does not state this threshold.  It does not need to (its claim is the")
print("  eps->0 contrapositive), but a reader could take `the entropy price` as a bound")
print("  that bites at the frozen value, and freezing gives only eps < 1/6 = %.4g." % (1 / 6))
print("  1/6 = 0.1667 > %.5g, so AT THE UNCONDITIONAL FROZEN VALUE PROP 4.1 SAYS NOTHING."
      % (1 / (2 * E * E)))

print()
print("=" * 78)
print("a2_maths done.")
print("=" * 78)
