"""b1 -- THE WITNESS.  The DISJUNCTION is FALSE, and the counterexample was already
committed, already certified, and already published -- IN TWO HALVES NOBODY MULTIPLIED.

*** PENDING INDEPENDENT RE-CERTIFICATION -- READ THIS BEFORE QUOTING ANYTHING BELOW ***

  The certifier used here is `lib5cba.py`, UNMODIFIED.  That is the audited exact
  instrument of this thread -- and it is also, now, THE AUDITED INSTRUMENT AUDITING
  ITSELF: a programme-level negative resting on the one certifier, which has never
  itself been audited.  pm-onethird has filed **mg-5e82**, an independent audit ranked
  ahead of this ticket, requiring the devices REBUILT on an instrument that is not
  lib5cba, lib789d or libc50b.

  Until mg-5e82 returns, every verdict in this file is CERTIFIED-PENDING-AUDIT.  The
  exposure is not uniform and the ranking is stated so an auditor can spend its budget:

    (i)   COPOSITIVITY of R(m_lo), i.e. mu_pref >= m_lo.  THIS IS THE ONE.  The hard
          direction; no exhibited vector can produce it; lib5cba decides singular faces
          by exact Fourier-Motzkin where mg-789d REFUSES them, which no other
          instrument in this arc does.
    (ii)  PSD REFUSAL of R(g_ub), i.e. gamma < g_ub.  Weaker exposure: refusing PSD
          needs ONE exhibited vector with c'Rc < 0.
    (iii) the Fraction arithmetic sweep(m_lo,Delta) > 2*g_ub.  INDEPENDENTLY CONFIRMED
          already -- arm B1.3 below re-runs it from mg-5cba's published decimals alone,
          and pm-onethird reproduced it by hand to seven significant figures.  That
          narrows step (iii) ONLY: it says nothing about whether the two bounds it
          consumes are right, and both are lib5cba outputs.

  And Delta, M and LE agreeing across lib5cba, lib789d and libc50b is THREE
  IMPLEMENTATIONS OF ONE READING of the transport DP, not three independent
  derivations.  It is reported here as corroboration and not as independence.

THE FINDING IS A BLANK TABLE CELL.

  mg-5cba certified FIVE (L*) counterexamples, not four.  Its audit table
  (docs/OneThird-LStar-mg-5cba-IndependentAudit.md:58-64) has a `u_M` column:

      C1 n=9   0.943486
      C2 n=9   0.947534
      C3 n=10  0.981830
      C4 n=11  0.958326
      C5 n=12  ---            <-- THE DASH

  STATE.md then publishes "(M#) HOLDS at 4 of 4" with those four figures.  That
  sentence is true of the four it names, and it names four because the fifth cell was
  blank.  My own ticket inherits it: "u_M = 0.981830 at n=10 is the closest any (M#)
  witness has come to failing."  It is not the closest.  It is the closest OF THE FOUR
  THAT WERE COMPUTED.

  Both inputs to the missing cell were published for that exact poset, by mg-5cba, in
  `code/audit_5cba/out_a5_scope.txt:51-53`:

      gamma in [0.061699260, 0.061699262]        mu_pref >= 0.065579592

  and Delta = 195/196.  From those three published numbers,

      t* = Delta - sqrt(Delta^2 - 2 gamma)  <=  0.064079274  <  0.065579592  <=  mu_pref

  so (M#) FAILS, and (F) fails there too (mg-5cba: v_F = 1.077029).  The multiplication
  is four lines of arithmetic on figures that have been on main since mg-5cba landed.

WHAT THIS ARM DOES.  It does not re-derive that reasoning from prose.  It runs the
exact certifier in the FAILS direction at all five posets and prints the u_M column
whole, so the dash is filled by an integer certificate rather than by an argument.

THE DIRECTIONS, WHICH ARE OPPOSITE FOR THE TWO CLAIMS (E5).

    (M#) HOLDS  needs  mu from ABOVE and gamma from BELOW  -- mg-5cba's direction at C1-C4
    (M#) FAILS  needs  mu from BELOW and gamma from ABOVE  -- and mu from below is the
                       hard direction, requiring exact COPOSITIVITY, which is the trap
                       mg-51f4 named.  No exhibited vector can do it.

  Both are run at all five.  A poset should certify exactly one of them, and the arm
  FAILS if any poset certifies both or neither -- a certifier that can say yes to a
  question and to its negation is not one.
"""

import math
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from libb417 import (LSTAR_GAP, N8_ARGMAX, cell, certify, emit_table,
                     height, score_float)

FAIL = 0


def arm(name, cond, got=""):
    global FAIL
    print("  [%s] %-64s %s" % ("ok " if cond else "FAIL", name, got))
    if not cond:
        FAIL += 1


print("=" * 78)
print("B1.1  THE u_M COLUMN, WHOLE -- five rows, five values, no dash")
print("=" * 78)
print(__doc__)
print()
print("  THE TABLE BELOW IS EMITTED BY `libb417.emit_table`, WHICH REFUSES A BLANK CELL.")
print("  A value that was not computed prints as NOT-COMPUTED, in the column, where a")
print("  reader scanning for a hole hits it.  That is the whole repair (b0 arm S8).")
print()
results = []
_rows = []
for tag, dn, n in LSTAR_GAP:
    c = certify(dn, n)
    results.append((tag, dn, n, c))
    _rows.append([tag, str(n), str(c["Delta"]),
                  cell(float(c["g_ub"]), "%.9f"),
                  cell(float(c["m_lo"]), "%.9f"),
                  cell(c["v_L_lo"]),
                  cell(c["u_M_lo"], na_reason="Delta2-le-2gamma"),
                  "(M#) FAILS" if c["M_sharp_fails"] else "(M#) holds"])
    sys.stdout.flush()
print(emit_table(["", "n", "Delta", "gamma <", "mu_pref >=", "v_L >=", "u_M >=",
                  "verdict"], _rows))

print()
print("=" * 78)
print("B1.2  THE CERTIFICATE AT EACH, ON INTEGERS")
print("=" * 78)
for tag, dn, n, c in results:
    print()
    print("  %s  n=%d   dn = %s" % (tag, n, str(dn)))
    print("    LE = %d   height = %d   primitive = %s   naturally labelled = %s   "
          "transitively closed = %s"
          % (c["LE"], height(dn, n), c["primitive"], c["natural"], c["transitive"]))
    print("    Delta = %s   M = %s" % (c["Delta"], c["M"]))
    print("    gamma < g_ub  = %s" % c["g_ub"])
    print("                  = %.12f          [R(g_ub) NOT PSD]" % float(c["g_ub"]))
    print("    mu_pref >= m_lo = %s" % c["m_lo"])
    print("                    = %.12f        [R(m_lo) COPOSITIVE]" % float(c["m_lo"]))
    arm("%s: the gamma certificate is re-asserted, not inherited from a bracket" % tag,
        c["gamma_cert_ok"])
    arm("%s: the mu certificate is re-asserted, not inherited from a bracket" % tag,
        c["mu_cert_ok"])
    arm("%s: (F) FAILS  (gamma < M^2/2, R NOT PSD)" % tag, c["F_fails"])
    sw, g2 = c["sweep_lo"], 2 * c["g_ub"]
    print("    sweep(m_lo, Delta) = %.12f      2*g_ub = %.12f" % (float(sw), float(g2)))
    print("    margin sweep - 2 g_ub = %+.12f" % float(c["margin"]))
    if c["M_sharp_fails"]:
        print("    *** (M#) FAILS -- CERTIFIED ON INTEGERS ***")
        print("        c# >= %.9f    f* >= %.9f" % (float(c["c_sharp_lo"]),
                                                    float(c["f_star_lo"])))
        print("        u_M >= %.9f   u_F >= %.9f" % (c["u_M_lo"], c["u_F_lo"]))
    else:
        print("    (M#) HOLDS here (the FAILS certificate refuses, as it must)")
    arm("%s: exactly one of {(M#) FAILS, (M#) HOLDS} certifies" % tag,
        c["M_sharp_fails"] != c["M_sharp_holds"],
        "fails=%s holds=%s" % (c["M_sharp_fails"], c["M_sharp_holds"]))
    if c["refutes_disjunction"]:
        print("    *** THIS POSET REFUTES THE DISJUNCTION: (F) FAILS AND (M#) FAILS ***")
    sys.stdout.flush()

print()
print("=" * 78)
print("B1.3  THE ARITHMETIC, DONE FROM mg-5cba's PUBLISHED FIGURES ALONE")
print("=" * 78)
print("""  This block uses NOTHING from this tree's own computation.  It takes the three
  numbers mg-5cba printed for C5 in out_a5_scope.txt and multiplies them.  If this
  block and B1.2 disagree, one of them is wrong and the disagreement is the finding.
""")
PUB_DELTA = Fraction(195, 196)
PUB_GAMMA_UB = Fraction(61699262, 10 ** 9)      # "gamma in [0.061699260,0.061699262]"
PUB_MU_LO = Fraction(65579592, 10 ** 9)         # "mu_pref >= 0.065579592"
fD, fg, fm = float(PUB_DELTA), float(PUB_GAMMA_UB), float(PUB_MU_LO)
ts_ub = fD - math.sqrt(fD * fD - 2 * fg)
print("    Delta = 195/196 = %.12f" % fD)
print("    gamma <= %.9f   (mg-5cba out_a5_scope.txt:51)" % fg)
print("    mu    >= %.9f   (mg-5cba out_a5_scope.txt:51)" % fm)
print("    t* = Delta - sqrt(Delta^2 - 2 gamma) <= %.9f" % ts_ub)
arm("mu_pref > t*  from mg-5cba's own two published bounds", fm > ts_ub,
    "%.9f > %.9f" % (fm, ts_ub))
print("    => u_M >= %.9f" % (fm / ts_ub))
sweep_pub = PUB_MU_LO * (2 * PUB_DELTA - PUB_MU_LO)
arm("exact: sweep(mu_lo,Delta) > 2 gamma_ub on the PUBLISHED rationals",
    sweep_pub > 2 * PUB_GAMMA_UB,
    "%+.12f" % float(sweep_pub - 2 * PUB_GAMMA_UB))
c5 = [c for t, d, n, c in results if t == "C5"][0]
arm("this block and B1.2 agree that (M#) FAILS at C5",
    (sweep_pub > 2 * PUB_GAMMA_UB) == c5["M_sharp_fails"])

print()
print("=" * 78)
print("B1.4  THE NEGATIVE CONTROL -- the n=8 argmax, where (L*) HOLDS")
print("=" * 78)
print("""  mg-5cba certified (L*) HOLDS at the n = 8 search argmax (0.968818 < 1).  If the
  FAILS certifier fires there, it fires on anything.  n = 8 IS NOT ENUMERATED: this is
  ONE poset, named by mg-5cba, run as a control.
""")
dn8, n8 = N8_ARGMAX
c8 = certify(dn8, n8)
print("    dn = %s   Delta = %s   M = %s" % (str(dn8), c8["Delta"], c8["M"]))
print("    gamma < %.12f   mu_pref >= %.12f" % (float(c8["g_ub"]), float(c8["m_lo"])))
print("    v_L >= %.6f    u_M >= %.6f" % (c8["v_L_lo"], c8["u_M_lo"]))
arm("n=8 argmax: (F) FAILS there (it is in the (F)-failing set)", c8["F_fails"])
arm("n=8 argmax: (M#) does NOT fail -- the certifier REFUSES", not c8["M_sharp_fails"])
arm("n=8 argmax: (M#) HOLDS, certified in its own direction", c8["M_sharp_holds"])
arm("n=8 argmax: does NOT refute the disjunction", not c8["refutes_disjunction"])

print()
print("=" * 78)
print("B1.5  THE VERDICT")
print("=" * 78)
ref = [(t, n) for t, d, n, c in results if c["refutes_disjunction"]]
print("  posets in the (L*)-gap population that REFUTE THE DISJUNCTION: %d of %d"
      % (len(ref), len(results)))
for t, n in ref:
    print("      %s at n = %d" % (t, n))
print()
if ref:
    print("  *** THE DISJUNCTION IS FALSE. ***")
    print("  max_P min(c#, f*) >= %.9f at n = 12, certified on integers."
          % float(c5["c_sharp_lo"]))
    print()
    print("  WHAT THIS KILLS: the uniform-in-n disjunction (F) or (M#), hence the route")
    print("  to C_3 = 1 that ran through it.  (L*) was SUFFICIENT for that disjunction;")
    print("  the disjunction was said to survive (L*)'s refutation.  It does not -- the")
    print("  SAME FIVE POSETS kill both, and the fifth was never asked.")
    print()
    print("  WHAT THIS DOES NOT KILL: C_3 = 1.  A dead route is a dead route.")
    print()
    print("  WHAT IS UNTOUCHED: the n <= 8 enumerations.  Both routes fail at 0 of")
    print("  2600369 at n = 8 and c_or(8) = 0.943649 (mg-c50b, exhaustive).  What died")
    print("  is uniformity in n, not the small-n record.")
    print()
    print("  WHAT THIS FILE DOES NOT SETTLE: n = 9, 10, 11.  The four certified (L*)")
    print("  witnesses there all have u_M < 1, so the (L*)-gap population alone puts the")
    print("  smallest EXHIBITED n at 12.  Whether the disjunction already fails BELOW 12")
    print("  is a search question, it is asked in b2, decided on integers in b4, and this")
    print("  file must not be read as an answer to it in either direction.")

print()
print("-" * 78)
print("ARMS FAILED: %d" % FAIL)
sys.exit(1 if FAIL else 0)
