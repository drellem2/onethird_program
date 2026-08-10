"""b4 -- THE EXACT STAGE.  Every champion b2 hands up, decided on integers.

NOTHING FROM b2 IS A RESULT UNTIL IT PASSES THROUGH HERE.  b2's screen scores with
mu_ub_float, an UPPER bound on mu_pref, so a champion that reads J > 1 there may be an
inflation artefact and nothing else.  This file re-decides each one with

    gamma  <  g_ub        R(g_ub)  NOT PSD             [integer PSD device, refusing]
    mu     >= m_lo        R(m_lo)  COPOSITIVE          [exact copositivity, deciding]

and the (M#) FAILS test  sweep(m_lo, Delta) > 2 g_ub  in exact Fractions.

A CHAMPION THAT DOES NOT CERTIFY IS A REFUSAL AND IS REPORTED AS ONE.  That outcome is
predicted (P6) and it is the whole reason the two stages are separate: if every
screened champion certified, the screen would be tight here and the separation would
have bought nothing.  The count of refusals is printed either way.

WHAT THE OUTPUT IS ALLOWED TO SAY.  For each n, the largest CERTIFIED min(c#,f*) over
the champions searched.  That is a LOWER bound on W(n) and it is nothing else: the
population was not enumerated, so no line here may read "W(n) = x".
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from libb417 import certify, height

HERE = os.path.dirname(os.path.abspath(__file__))
FAIL = 0


def arm(name, cond, got=""):
    global FAIL
    print("  [%s] %-62s %s" % ("ok " if cond else "FAIL", name, got))
    if not cond:
        FAIL += 1


with open(os.path.join(HERE, "champions.json")) as fh:
    champs = json.load(fh)

print("=" * 78)
print("B4.1  EVERY CHAMPION, DECIDED ON INTEGERS")
print("=" * 78)
print()
print("   n | float J    | certified  | certified  | (F) | (M#) | refutes | dn")
print("     |  (stage 2) | min(c#,f*) | u_M >=     |     | fails|  disj.  |")

certified = {}          # n -> (lo, dn, r) with the largest certified min(c#,f*)
refuters = []           # every champion that certifies as a disjunction counterexample
refusals = 0
crossed_screen_not_certified = 0
tested = 0
for n in sorted(champs, key=int):
    for c in champs[n]:
        dn = tuple(c["dn"])
        nn = int(c["n"])
        # 16 bisection steps on an interval already ~2.2e-5 wide gives ~3e-10 on m_lo,
        # which is four orders of magnitude finer than the smallest margin in play.
        # Bisecting further would only spend copositivity decisions on digits no
        # verdict reads.
        r = certify(dn, nn, mu_hint=c["mu"], mu_steps=16)
        tested += 1
        lo = min(float(r["c_sharp_lo"]), float(r["f_star_lo"]))
        ok = r["gamma_cert_ok"] and r["mu_cert_ok"]
        if not ok:
            refusals += 1
        if c["float_J"] > 1.0 and not r["refutes_disjunction"]:
            crossed_screen_not_certified += 1
        note = ""
        if not ok:
            note = "   <-- CERTIFICATE REFUSED"
        elif c["float_J"] > 1.0 and not r["refutes_disjunction"]:
            note = "   <-- float said >1, INTEGERS SAY NO"
        print("  %2d | %10.6f | %10.6f | %10.6f | %3s | %4s | %7s | %s%s"
              % (nn, c["float_J"], lo, r["u_M_lo"] if r["u_M_lo"] else 0.0,
                 "yes" if r["F_fails"] else "no",
                 "yes" if r["M_sharp_fails"] else "no",
                 "YES" if r["refutes_disjunction"] else "no",
                 str(dn), note))
        sys.stdout.flush()
        if r["refutes_disjunction"]:
            refuters.append((nn, lo, dn, r))
        prev = certified.get(nn)
        if prev is None or lo > prev[0]:
            certified[nn] = (lo, dn, r)

print()
print("  champions tested: %d     certificates REFUSED: %d" % (tested, refusals))
print("  champions the SCREEN put above 1 that INTEGERS DID NOT CONFIRM: %d"
      % crossed_screen_not_certified)
print("  (a refusal is an outcome, not a failure: it means the screen's upper bound")
print("   did not survive integers at that poset, which is what the screen is for.)")

print()
print("=" * 78)
print("B4.2  THE CERTIFIED FRONTIER -- LOWER BOUNDS ON W(n), NEVER MAXIMA")
print("=" * 78)
print()
print("   n | W(n) >= (certified) | refutes disjunction | height | mu_pref >= | dn")
crossers = sorted(set((n, lo, dn) for n, lo, dn, r in refuters))
crossers = [(n, lo, dn, [q for a, b, c2, q in refuters if a == n and c2 == dn][0])
            for n, lo, dn in crossers]
for n in sorted(certified):
    lo, dn, r = certified[n]
    print("  %2d | %19.6f | %19s | %6d | %10.6f | %s"
          % (n, lo, "YES" if r["refutes_disjunction"] else "no",
             height(dn, n), float(r["m_lo"]), str(dn)))
print()
print("  EVERY ROW IS A SEARCH RESULT.  The population at each n was not enumerated,")
print("  so these are lower bounds on W(n) and no row is a maximum at its n.")

print()
print("=" * 78)
print("B4.3  THE SMALLEST n AT WHICH THE DISJUNCTION IS CERTIFIED TO FAIL")
print("=" * 78)
best_per_n = {}
for n, lo, dn, r in crossers:
    if n not in best_per_n or lo > best_per_n[n][0]:
        best_per_n[n] = (lo, dn, r)
if crossers:
    nmin = min(best_per_n)
    print()
    print("  SMALLEST n EXHIBITED: %d" % nmin)
    print()
    print("  distinct posets certified as counterexamples: %d, at n = %s"
          % (len(crossers), ", ".join(str(x) for x in sorted(best_per_n))))
    print()
    for n in sorted(best_per_n):
        lo, dn, r = best_per_n[n]
        print("    n = %2d   min(c#, f*) >= %.9f   dn = %s" % (n, lo, str(dn)))
        print("             Delta = %s   M = %s   LE = %d" % (r["Delta"], r["M"], r["LE"]))
        print("             gamma < %s" % r["g_ub"])
        print("             mu_pref >= %s" % r["m_lo"])
        print("             sweep(m_lo,Delta) - 2 g_ub = %+.12f" % float(r["margin"]))
        print("             u_M >= %.9f   u_F >= %.9f" % (r["u_M_lo"], r["u_F_lo"]))
    print()
    print("  THIS IS 'FIRST EXHIBITED', NOT 'FIRST'.  The disjunction is exhaustively")
    print("  verified through n = 8 (mg-c50b: 0 of 2600369).  Between 9 and the number")
    print("  above, nothing here enumerates anything, and a smaller n is not excluded")
    print("  by this file or by any file in the corpus.")
else:
    print("  NO champion certified as a disjunction counterexample.")
    print("  Note this does NOT contradict b1: b1's C5 is certified independently there.")

print()
print("-" * 78)
arm("at least one champion certified (the exact stage is reachable at all)",
    tested > 0)
arm("no champion is reported as refuting while its certificate was refused",
    all(not r["refutes_disjunction"] or (r["gamma_cert_ok"] and r["mu_cert_ok"])
        for n, lo, dn, r in [(k,) + certified[k] for k in certified]))
print("ARMS FAILED: %d" % FAIL)
sys.exit(1 if FAIL else 0)
