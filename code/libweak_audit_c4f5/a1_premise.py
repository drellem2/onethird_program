#!/usr/bin/env python3
"""a1_premise — AUDIT TARGET 1, the premise. Does (LIB-weak) close L1b as stated?

The premise is: `E[inv_e] = o(n^2)` for frozen P  ==>  `lambda_std -> 1`.
It runs entirely through mg-210d's master bound, which mg-c3ca explicitly did NOT
re-derive ("I did not re-derive the mg-210d master bound", Sec.7).  So this file
re-derives it -- by hand in the audit document, and NUMERICALLY here, on every
naturally labelled poset up to n = 7.

TWO SEPARATE QUESTIONS, kept apart on purpose:
  A. is the master bound TRUE, at the constant claimed, and sharp where claimed?
  B. is `lambda_std` even a well-defined function of the poset?  The bound relates
     lambda_std(L) to E[inv_L] for the SAME reference linear extension L.  If
     lambda_std moves with L, then "frozen ==> lambda_std -> 1" is only well posed
     because freezing makes the reference canonical -- a hypothesis STATE.md's glossary
     line for lambda_std does not carry.
"""
import sys
from fractions import Fraction
from itertools import permutations
import lib_c4f5 as L

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
TOL = 1e-9      # THE ONLY TOLERANCE IN THIS AUDIT. It exists because lambda_std needs
                # an eigenvalue and eigenvalues are float. Every other number is exact.

print("=" * 78)
print("a1_premise -- AUDIT TARGET 1: does (LIB-weak) close L1b as stated?")
print("POPULATION: every naturally labelled poset on n elements (A006455).")
print("GRAIN: one naturally labelled poset.  TOLERANCE: %g, eigenvalues only." % TOL)
print("=" * 78)

print()
print("-" * 78)
print("A. THE MASTER BOUND, TESTED  --  1-lambda_std <= 3E[F]/(n^2-1) <= 6E[inv_L]/(n^2-1)")
print("-" * 78)
print("%3s %8s %10s %10s %12s %12s %s" %
      ("n", "posets", "viol_F", "viol_inv", "worst_slack_F", "n_equality", "equality cases"))
tot_v_f = tot_v_i = 0
eq_examples = {}
for n in range(2, NMAX + 1):
    cnt = vf = vi = 0
    worst = None
    neq = 0
    eqs = []
    for P in L.gen_natural_posets(n):
        a = L.analyse(P)
        lam, _ = L.lambda_std_from_T(a["T"])
        gap = 1.0 - lam
        bF = 3.0 * float(a["footrule"]) / (n * n - 1)
        bI = 6.0 * float(a["inv"]) / (n * n - 1)
        cnt += 1
        if gap > bF + TOL:
            vf += 1
        if gap > bI + TOL:
            vi += 1
        slack = bF - gap
        if worst is None or slack < worst:
            worst = slack
        if abs(slack) < 1e-7:
            neq += 1
            if len(eqs) < 3:
                eqs.append(a["up"])
    tot_v_f += vf
    tot_v_i += vi
    eq_examples[n] = eqs
    print("%3d %8d %10d %10d %12.2e %12d %s" % (n, cnt, vf, vi, worst, neq, eqs))
print()
print("TOTAL VIOLATIONS: footrule form %d, inversion form %d" % (tot_v_f, tot_v_i))
print("P1 predicted 0 and 0.")

print()
print("-" * 78)
print("A2. WHICH posets achieve equality in the footrule form?")
print("-" * 78)
print("mg-210d Sec.2.4 claims equality AT THE ANTICHAIN.  Checked here as an `only if`,")
print("which mg-210d does not claim and which I predicted (P1) would hold:")
for n in range(2, min(NMAX, 6) + 1):
    hits = []
    for P in L.gen_natural_posets(n):
        a = L.analyse(P)
        lam, _ = L.lambda_std_from_T(a["T"])
        bF = 3.0 * float(a["footrule"]) / (n * n - 1)
        if abs(bF - (1.0 - lam)) < 1e-7:
            hits.append(a["up"])
    isanti = [h for h in hits if all(u == 0 for u in h)]
    print("  n=%d : %d equality cases, %d of them the antichain, others: %s"
          % (n, len(hits), len(isanti), [h for h in hits if any(h)][:4]))

print()
print("-" * 78)
print("A3. THE IMPLICATION ITSELF, made quantitative rather than asserted")
print("-" * 78)
print("(LIB-weak) says E[inv_e]/n^2 -> 0.  Through the master bound that is")
print("1-lambda_std <= 6(E[inv_e]/n^2)(n^2/(n^2-1)) -> 0.  The map is monotone and")
print("explicit, so the implication is arithmetic.  Tabulated so the constant is visible:")
print("  %-28s %-28s" % ("if E[inv_e]/n^2 <=", "then 1-lambda_std <= (n large)"))
for eps in (1e-1, 1e-2, 2e-2/6, 1e-3, 1e-4):
    print("  %-28.6g %-28.6g" % (eps, 6 * eps))
print()
print("So (LIB-weak) => lambda_std -> 1 : CONFIRMED, and it is ONE division.")
print("The content is entirely in the master bound, which mg-c3ca did not re-derive.")

print()
print("-" * 78)
print("B. IS lambda_std A FUNCTION OF THE POSET?  (P2)")
print("-" * 78)
print("The master bound is proved for a poset RELABELLED by a chosen reference linear")
print("extension L.  Sweep every linear extension of every poset and ask whether the")
print("value moves.  STATE.md:40 defines lambda_std with no reference order in it.")
print()
print("%3s %8s %10s %14s %s" % ("n", "posets", "L-dep", "max spread", "witness"))
for n in range(3, min(NMAX, 6) + 1):
    ndep = 0
    best = 0.0
    wit = None
    seen_iso = set()
    for P in L.gen_natural_posets(n):
        les = L.linear_extensions(P)
        if len(les) < 2:
            continue
        vals = []
        for e in les:
            perm = [0] * n
            for i, x in enumerate(e):
                perm[x] = i
            Q = L.relabel(P, perm)
            aq = L.analyse(Q)
            lam, _ = L.lambda_std_from_T(aq["T"])
            vals.append(lam)
        spread = max(vals) - min(vals)
        if spread > 1e-6:
            ndep += 1
            if spread > best:
                best = spread
                wit = (P[1], round(min(vals), 6), round(max(vals), 6))
    print("%3d %8s %10d %14.6f %s" % (n, "-", ndep, best, wit))
print()
print("P2 predicted L-dependence is REAL with a witness at n<=6.")

print()
print("-" * 78)
print("B2. AND WHAT THE MASTER BOUND LOOKS LIKE AT THE MAJORITY ORDER e")
print("-" * 78)
print("For a frozen poset e exists and is a linear extension, so the right reading of")
print("the bound is 1-lambda_std(e) <= 6E[inv_e]/(n^2-1).  E_maj = E[inv_e] is the")
print("MINIMUM of E[inv_L] over reference orders -- but lambda_std(e) is not the")
print("minimum of lambda_std(L), so the two minima are not taken together.  Checked:")
n = 5
better = worse = same = 0
for P in L.gen_natural_posets(n):
    a = L.analyse(P)
    mo = L.majority_order(a)
    if mo is None or not L.is_linear_extension(P, mo):
        continue
    les = L.linear_extensions(P)
    lams = []
    for e in les:
        perm = [0] * n
        for i, x in enumerate(e):
            perm[x] = i
        aq = L.analyse(L.relabel(P, perm))
        lam, _ = L.lambda_std_from_T(aq["T"])
        lams.append((lam, e))
    permo = [0] * n
    for i, x in enumerate(mo):
        permo[x] = i
    amo = L.analyse(L.relabel(P, permo))
    lam_mo, _ = L.lambda_std_from_T(amo["T"])
    mx = max(l for l, _ in lams)
    if lam_mo > mx - 1e-9:
        better += 1
    elif lam_mo < mx - 1e-6:
        worse += 1
    else:
        same += 1
print("  n=5, posets with a majority linear extension:")
print("  lambda_std(e) is the MAXIMUM over reference orders : %d" % better)
print("  lambda_std(e) is strictly BELOW the maximum        : %d" % worse)
print()
print("  (If e were not the maximiser, `lambda_std -> 1` at e would be a WEAKER")
print("   conclusion than at the best reference order -- worth knowing which way it")
print("   points, since the architecture wants lambda_std LARGE.)")

print()
print("=" * 78)
print("a1_premise done.")
print("=" * 78)
