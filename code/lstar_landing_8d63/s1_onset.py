#!/usr/bin/env python3
"""s1 -- THE ONSET OF `rho*Delta > 1`, MEASURED RATHER THAN QUOTED.

WHY THIS SCRIPT EXISTS.  mg-8d63 is the landing ticket for mg-789d's refutation of (L*).
Its second, independent correction is the ONSET of `rho*Delta > 1`: the corpus said the
phenomenon starts at n = 10 (mg-c50b Section 4, chain(n-1)+point, correctly labelled
FAMILY), and mg-789d replaced that with "it occurs from n = 6".

A landing that carries a corrected number by QUOTING its source has not checked it.  This
script measures the onset directly, over ALL primitive posets at n = 2..6, and the answer
is NEITHER of the two: `rho*Delta > 1` first occurs at **n = 5**, at 6 of 275 primitive
posets, max 1.027118.

PRIORITY, STATED HERE RATHER THAN IN A FOOTNOTE.  mg-5cba's independent audit of mg-789d
found the same onset and LANDED FIRST (5c0849a), certifying all six n = 5 witnesses in
EXACT RATIONALS and certifying mu_pref*Delta <= gamma at EVERY primitive poset of n = 3 and
n = 4 -- so n = 5 is exactly the onset and not merely the smallest sighting.  That is
strictly stronger than what this float sweep establishes.  What this script adds is (a) a
third independent reproduction, on mg-789d's OWN instrument, agreeing to six places; (b)
the cross-thread provenance in the paragraph below, which mg-5cba does not report; and (c)
control C3, which is about the defect CLASS rather than the number.

WHY mg-789d GOT n = 6.  Its own s2 section 2.4 measures exactly two values of n -- 6 and 7 --
because that section's question was whether the (F) hypothesis is what turns the routes on,
and the (F)-failing set is empty below n = 7.  n = 6 is the smallest n it looked at, not the
smallest n where the phenomenon occurs.  The figure it published is right; the word "from"
is not.

INDEPENDENT AGREEMENT, AND IT PREDATES BOTH.  The whole column measured here already exists
in this corpus under a different name: mg-28ff's cell `V10` IS `rho*Delta_P`
(`docs/OneThird-L2-Conditionality-mg-28ff.md:279`, and mg-29fe's audit table at :366 spells
the identification out).  `code/l2_audit_29fe/out_s3_counterfactual.txt` reports the V10
maxima 0.500000 / 0.666667 / 0.904508 / 1.027118 / 1.156724 at n = 2..6 and states in as
many words that V10 "first exceeds 1 at n = 5, at 6 of 275 primitive posets at n=5".  So
the corpus held the refuting datum for the n = 10 statement, in a document neither mg-c50b
nor mg-789d had reason to read as being about (L*).  This script reproduces that column on
mg-789d's instrument, which shares no code with mg-29fe's.

WHAT IS AND IS NOT MEASURED HERE.  Populations are naturally-labelled primitive posets on
[n] -- the same population mg-789d and mg-c50b use, and the labelling matters (gamma, Delta,
mu_pref and M all move with it).  n = 2..6 is EXHAUSTIVE.  n = 7 is not run: it is 86278
posets and roughly an hour on this instrument, and it cannot change an onset already
established at n = 5.  Nothing here touches (L*) itself, whose hypothesis is that (F) FAILS
-- and (F) fails at NO poset below n = 7.  The onset of `rho*Delta > 1` and the refutation
of (L*) are two different facts and this script measures only the first.

CONTROL.  A run whose sole output is "the number I expected" has not been checked either.
Arm C1 re-derives mg-789d's own published n = 6 maximum (1.15672, its section 4) and arm C2
re-derives mg-c50b's FAMILY statement -- chain(n-1)+point crossing 1 at n = 10 and reaching
1.078 at n = 16 -- because that sentence is TRUE as a family statement and this landing must
not be read as striking a true sentence.  If C2 failed, the correction would be a
contradiction rather than a widening.

THE MIRROR DEFECT, AND IT IS THE ONE THIS SCRIPT IS MOST LIKELY TO COMMIT.  The defect being
corrected is PUBLISHING THE SMALLEST n SOMEBODY LOOKED AT AS THE SMALLEST n WHERE THE THING
HAPPENS.  A sweep that starts at n = 3 and reports "onset at n = 5" is one primitive poset
away from committing exactly that: n = 2 has a primitive poset (the 2-antichain) and this
script's first draft did not look at it.  Arm C3 therefore runs the sweep down to its own
FLOOR and prints what the floor is and why -- n = 1 is refused, not skipped, because gamma = 0
there and rho = mu_pref/gamma does not exist.  The onset claim is only as good as C3.
"""

import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "lstar_789d"))

from lib789d import P789, gen_posets, fam_chain_plus_points  # noqa: E402


def bar(title):
    print("=" * 78)
    print(title)
    print("=" * 78)


def onset_sweep(nmin=2, nmax=6):
    """max rho*Delta over all primitive posets on [n], n = nmin..nmax.  EXHAUSTIVE."""
    rows = []
    for n in range(nmin, nmax + 1):
        t0 = time.time()
        best, argm, over, tot = 0.0, None, 0, 0
        for dn in gen_posets(n):
            P = P789(dn, n)
            if not P.primitive():
                continue
            tot += 1
            v = P.summary_float()["rhoD"]
            if v > 1.0:
                over += 1
            if v > best:
                best, argm = v, dn
        rows.append((n, tot, best, argm, over, time.time() - t0))
    return rows


bar("S1.1  THE ONSET, EXHAUSTIVE OVER PRIMITIVE POSETS")
print("  rho = mu_pref/gamma;  Delta = Delta_P.  Population: naturally labelled")
print("  primitive posets on [n].  Every row below is a MAXIMUM over its n, not a search.")
print()
print("   n | primitive |  max rho*Delta | posets with rho*Delta > 1 | argmax")
rows = onset_sweep(2, 6)
for n, tot, best, argm, over, dt in rows:
    print("  %2d | %9d |      %8.6f | %25d | %s   (%ds)"
          % (n, tot, best, over, argm, dt))
print()

first = next((n for n, tot, best, argm, over, dt in rows if over > 0), None)
print("  ONSET: rho*Delta > 1 first occurs at n = %s." % first)
print("  The corpus said n = 10 (mg-c50b Section 4, FAMILY) and then n = 6 (mg-789d Section 4).")
print("  Both are wrong as ONSET statements, and n = 6 is wrong by one value of n.")
print()

bar("S1.2  CONTROL C1 -- mg-789d's OWN PUBLISHED n = 6 MAXIMUM")
n6 = [r for r in rows if r[0] == 6][0]
print("  mg-789d Section 4 publishes  max rho*Delta = 1.15672 over all 4070 at n = 6.")
print("  measured here               : %8.6f over %d primitive" % (n6[2], n6[1]))
ok1 = abs(n6[2] - 1.15672) < 5e-6 and n6[1] == 4070
print("  %s" % ("PASS  agrees to every printed digit." if ok1 else "FAIL  DISAGREES."))
print()

bar("S1.3  CONTROL C2 -- mg-c50b's FAMILY STATEMENT IS TRUE, AND STAYS TRUE")
print("  mg-c50b Section 4: on chain(n-1) + one isolated point, rho*Delta_P crosses 1")
print("  at n = 10 and reaches 1.078 at n = 16.  That sentence carries the word FAMILY")
print("  and is CORRECT.  What this landing corrects is its use as an ONSET.")
print()
print("   n | rho*Delta on chain(n-1)+point")
fam = {}
for n in (8, 9, 10, 12, 16):
    dn, nn = fam_chain_plus_points(n - 1, 1)
    P = P789(dn, nn)
    fam[n] = P.summary_float()["rhoD"]
    print("  %2d |   %8.5f" % (n, fam[n]))
ok2 = fam[9] <= 1.0 < fam[10] and abs(fam[16] - 1.078) < 5e-4
print()
print("  %s" % ("PASS  crosses 1 between n = 9 and n = 10, and reaches 1.078 at n = 16."
                if ok2 else "FAIL  the family statement does NOT reproduce."))
print()

bar("S1.4  CONTROL C3 -- THIS SCRIPT'S OWN FLOOR, WHICH IS THE MIRROR DEFECT")
print("  The defect being corrected is a smallest-n-looked-at published as an onset.")
print("  So: what is the smallest n THIS sweep looked at, and is anything below it?")
print()
nmin = rows[0][0]
print("  sweep floor                 : n = %d, with %d primitive poset(s), max rho*Delta %.6f"
      % (nmin, rows[0][1], rows[0][2]))
print("  n = 1                       : REFUSED, not skipped -- LE = 1, gamma = 0, and")
print("                                rho = mu_pref/gamma does not exist.  There is no")
print("                                value of rho*Delta at n = 1 to be above or below 1.")
try:
    P1 = P789((0,), 1)
    g1 = P1.gamma_float()
    print("                                measured: gamma(n=1) = %.6f" % g1)
    ok3 = (nmin == 2) and (rows[0][2] <= 1.0) and (g1 == 0.0)
except Exception as exc:                                        # pragma: no cover
    print("                                measured: n = 1 raises %s" % type(exc).__name__)
    ok3 = (nmin == 2) and (rows[0][2] <= 1.0)
print()
print("  %s" % ("PASS  the sweep bottoms out at the smallest n where rho*Delta EXISTS, and"
                "\n        rho*Delta <= 1 there, so n = 5 is an onset and not a floor artefact."
                if ok3 else "FAIL  the floor is not established -- the onset claim is not earned."))
print()

bar("S1.5  VERDICT")
print("  onset over primitive posets           : n = %s   (6 of 275, max 1.027118)" % first)
print("  onset on the chain+point FAMILY       : n = 10  (mg-c50b, TRUE as stated)")
print("  the two are different questions and this landing separates them.")
print()
print("  NOT MEASURED HERE: n >= 7 (an onset at n = 5 cannot be moved by a larger n);")
print("  (L*) itself (its hypothesis needs (F) to FAIL, which happens at no n <= 6).")
ok = ok1 and ok2 and ok3 and first == 5
print()
print("  ALL ARMS PASS" if ok else "  SOME ARM FAILED")
sys.exit(0 if ok else 1)
