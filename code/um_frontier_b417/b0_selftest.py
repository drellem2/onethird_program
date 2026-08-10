"""b0 -- CONTROLS.  Nothing downstream may be believed until this file passes.

The load-bearing arms, in the order they would fail:

  S1  The four published u_M figures reproduce EXACTLY.  If they do not, this tree is
      computing something else and every number in it is about a different object.
  S2  The identity u_M = v_L * D holds at the whole n <= 6 primitive population.  The
      trend section is organised around it, so it is checked and not asserted.
  S3  THE SCREEN'S DIRECTION.  mu_ub >= mu_pref at every primitive poset of n <= 6, in
      BOTH directions -- mg-789d's own D1 was a one-sided control read as two-sided
      (it scored max(mu_ub - mu_exact), blind to mu_ub < mu_exact).  Scored here as
      max and MIN of the difference.
  S4  PLANTED WORLDS for the certifier, five of them, including the two that matter:
      a poset where (M#) HOLDS must be REFUSED, and a poset where u_M > 1 but (F)
      HOLDS must not be called a disjunction counterexample.
  S5  THE CERTIFICATES ARE RE-ASSERTED, NOT INHERITED (E6).  A deliberately bad m_lo
      and a deliberately bad g_ub are fed in and the routine must say so.
  S6  W(7) = 0.890780 reproduces from this tree's own objective against mg-c50b's
      exhaustive figure -- an end-to-end control on a number computed by somebody else
      on code sharing no line with this.
  S7  The move set produces only naturally-labelled, transitively-closed posets.
  S8  A TABLE THAT CANNOT HAVE A BLANK CELL.  The dash in mg-5cba's u_M column is the
      finding of this ticket, so the emitter that would have printed it is planted
      against six blank renderings and must refuse all six.
"""

import math
import os
import sys
import time
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from libb417 import (LSTAR_GAP, BlankCell, P5, P789, cell, certify, close_natural,
                     emit_table, gamma_float, height, lifts, mu_pref_float,
                     neighbours, scalars, score_float, score_screen, tstar)
from lib5cba import gen_posets

FAIL = 0


def arm(name, cond, got=""):
    global FAIL
    print("  [%s] %-62s %s" % ("ok " if cond else "FAIL", name, got))
    if not cond:
        FAIL += 1


print("=" * 78)
print("S1  THE FOUR PUBLISHED u_M FIGURES, REPRODUCED")
print("=" * 78)
print("  mg-5cba out_a1_witness.txt / docs audit table:")
PUB = {"C1": 0.943486, "C2": 0.947534, "C3": 0.981830, "C4": 0.958326}
for tag, dn, n in LSTAR_GAP:
    s = score_float(dn, n)
    if tag in PUB:
        arm("%s n=%d: u_M = %.6f reproduces mg-5cba's published figure" % (tag, n, s["u_M"]),
            abs(s["u_M"] - PUB[tag]) < 5e-7, "%.6f vs %.6f" % (s["u_M"], PUB[tag]))
    else:
        arm("%s n=%d: u_M = %.6f -- THE CELL mg-5cba LEFT BLANK, NOW COMPUTED"
            % (tag, n, s["u_M"]), s["u_M"] > 1.0, "and it is ABOVE 1")
arm("the blank cell is the only one above 1",
    score_float(*LSTAR_GAP[4][1:3])["u_M"] > 1
    and all(score_float(d, n)["u_M"] < 1 for t, d, n in LSTAR_GAP[:4]))

print()
print("=" * 78)
print("S2  THE IDENTITY  u_M = v_L * D,  D = (1 + sqrt(1 - 2 gamma/Delta^2))/2")
print("=" * 78)
worst = 0.0
cnt = 0
t0 = time.time()
for n in range(3, 7):
    for dn in gen_posets(n):
        p = P5(dn, n)
        if not p.primitive():
            continue
        g = gamma_float(p)
        if g <= 1e-13:
            continue
        mu, _ = mu_pref_float(p)
        if mu is None:
            continue
        s = scalars(float(p.Delta()), float(p.M()), g, mu)
        if s["D"] is None or s["u_M"] == 0.0:
            continue
        cnt += 1
        worst = max(worst, abs(s["v_L"] * s["D"] - s["u_M"]))
arm("u_M = v_L * D at every primitive poset with Delta^2 > 2 gamma, n <= 6",
    worst < 1e-9, "%d posets, worst |v_L*D - u_M| = %.3e  (%.0fs)" % (cnt, worst, time.time() - t0))

print()
print("=" * 78)
print("S3  THE SCREEN'S DIRECTION -- BOTH WAYS (mg-789d's D1, not repeated)")
print("=" * 78)
hi = -1e9
lo = 1e9
cnt = 0
t0 = time.time()
for n in range(3, 7):
    for dn in gen_posets(n):
        p = P5(dn, n)
        if not p.primitive():
            continue
        q = P789(dn, n)
        if q.gamma_float() <= 1e-13:
            continue
        mu_exact, _ = mu_pref_float(p)
        mu_ub = q.mu_ub_float()[0]
        if mu_exact is None or mu_ub == float("inf"):
            continue
        cnt += 1
        d = mu_ub - mu_exact
        hi = max(hi, d)
        lo = min(lo, d)
arm("mu_ub >= mu_pref at every primitive poset n <= 6 (min difference >= 0)",
    lo > -1e-9, "%d posets, min %+.3e, max %+.3e  (%.0fs)" % (cnt, lo, hi, time.time() - t0))
arm("the screen is not merely equal to the truth (it does inflate somewhere)",
    hi > 1e-9, "max inflation %+.3e" % hi)

print()
print("=" * 78)
print("S4  PLANTED WORLDS FOR THE CERTIFIER")
print("=" * 78)
print("""  W1  C1 (n=9): (M#) HOLDS.  The FAILS certifier must REFUSE.
  W2  C5 (n=12): (M#) FAILS.  The FAILS certifier must FIRE.
  W3  a poset with u_M > 1 where (F) HOLDS.  Must NOT be called a counterexample to the
      disjunction -- E3, the error that turns this ticket into a non-result.
  W4  a NON-PRIMITIVE poset.  Must be refused before any scalar is taken from it.
  W5  a poset with Delta^2 <= 2 gamma, where (M#) CANNOT fail whatever mu_pref is.
""")
c1 = certify(*LSTAR_GAP[0][1:3])
arm("W1  C1: (M#) FAILS certificate REFUSES", not c1["M_sharp_fails"])
arm("W1  C1: (F) fails there all the same (it IS in the (F)-failing set)", c1["F_fails"])
arm("W1  C1: does not refute the disjunction", not c1["refutes_disjunction"])
c5 = certify(*LSTAR_GAP[4][1:3])
arm("W2  C5: (M#) FAILS certificate FIRES", c5["M_sharp_fails"])
arm("W2  C5: refutes the disjunction", c5["refutes_disjunction"])

# W3 -- find, exhaustively at n = 7, a poset with u_M > 1.  mg-c50b reports 4 of them.
# THE n = 7 SWEEP IS RUN ONCE and serves both W3 and S6: it is 86278 primitive posets
# with a 2^6-face mu_pref each, and running it twice would be eleven minutes spent
# proving that a loop is deterministic.
t0 = time.time()
w3 = []
N7_BEST, N7_ARG, N7_PRIM = -1.0, None, 0
for dn in gen_posets(7):
    p = P5(dn, 7)
    if not p.primitive():
        continue
    N7_PRIM += 1
    g = gamma_float(p)
    if g <= 1e-13:
        continue
    mu, _ = mu_pref_float(p)
    if mu is None:
        continue
    s = scalars(float(p.Delta()), float(p.M()), g, mu)
    if s["J"] > N7_BEST:
        N7_BEST, N7_ARG = s["J"], dn
    if s["u_M"] > 1.0:
        w3.append((dn, s))
N7_SECS = time.time() - t0
print("  n=7 exhaustive: %d primitive, %d with u_M > 1   (%.0fs)"
      % (N7_PRIM, len(w3), N7_SECS))
arm("W3  mg-c50b's count of (M#)-failing posets at n=7 reproduces", len(w3) == 4,
    "%d vs 4" % len(w3))
arm("W3  (F) HOLDS at every one of them -- u_M > 1 is NOT a disjunction event",
    all(s["u_F"] <= 1.0 for dn, s in w3),
    "max u_F there = %.6f" % max(s["u_F"] for dn, s in w3) if w3 else "")
for dn, s in w3:
    cw = certify(dn, 7)
    arm("W3  %s: (M#) fails but the disjunction is NOT refuted" % (str(dn),),
        cw["M_sharp_fails"] and not cw["refutes_disjunction"],
        "u_M %.6f u_F %.6f" % (s["u_M"], s["u_F"]))

cnp = certify((0, 0, 0), 3)   # antichain on 3: leak(A_k) > 0 fails? -- checked below
arm("W4  a non-primitive input is refused or handled without a verdict",
    (cnp.get("verdict") == "NOT PRIMITIVE") or (cnp["primitive"] is True),
    str(cnp.get("verdict", "primitive")))
notprim = None
for dn in gen_posets(5):
    p = P5(dn, 5)
    if not p.primitive():
        notprim = dn
        break
if notprim is not None:
    cnp = certify(notprim, 5)
    arm("W4  an actually non-primitive poset gets verdict NOT PRIMITIVE",
        cnp.get("verdict") == "NOT PRIMITIVE", str(notprim))

w5 = None
for dn in gen_posets(5):
    p = P5(dn, 5)
    if not p.primitive():
        continue
    g = gamma_float(p)
    if g > 1e-13 and float(p.Delta()) ** 2 <= 2 * g:
        w5 = (dn, p, g)
        break
if w5 is not None:
    dn, p, g = w5
    s = scalars(float(p.Delta()), float(p.M()), g, mu_pref_float(p)[0])
    arm("W5  Delta^2 <= 2 gamma  =>  u_M is 0 (M# cannot fail), not +inf",
        s["u_M"] == 0.0 and tstar(float(p.Delta()), g) is None, str(dn))
    cw = certify(dn, 5)
    arm("W5  and the certifier does not call it a counterexample",
        not cw["M_sharp_fails"])
else:
    arm("W5  a Delta^2 <= 2 gamma poset exists at n=5 to plant", False, "none found")

print()
print("=" * 78)
print("S5  THE CERTIFICATES ARE RE-ASSERTED, NOT INHERITED (E6)")
print("=" * 78)
print("""  lib5cba.mu_bracket only ever RAISES its low end; if no midpoint passes, the `lo`
  it returns is the untested float-derived seed.  A certificate that inherits that is a
  float wearing a Fraction's clothes.  Fed a seed that is deliberately TOO HIGH, the
  routine must come back refused rather than confident.
""")
dn5, n5 = LSTAR_GAP[4][1], LSTAR_GAP[4][2]
p5 = P5(dn5, n5)
bad_mu = Fraction(9, 100)          # far above the true mu_pref ~ 0.06558
arm("mu_ge(a deliberately too-high m_lo) is False -- the copositivity test refuses",
    p5.mu_ge(bad_mu) is False, "m_lo = %s" % bad_mu)
bad_g = Fraction(1, 1000)          # far below the true gamma ~ 0.06170
arm("gamma_ge(a deliberately too-low g_ub) is True -- so it is NOT an upper bound",
    p5.gamma_ge(bad_g) is True, "g_ub = %s" % bad_g)
cbad = certify(dn5, n5, mu_hint=0.09)
arm("certify() with a poisoned mu hint does not produce a false certificate",
    (not cbad["mu_cert_ok"]) or cbad["m_lo"] <= Fraction(657, 10000),
    "mu_cert_ok=%s m_lo=%.9f" % (cbad["mu_cert_ok"], float(cbad["m_lo"])))

print()
print("=" * 78)
print("S6  END-TO-END: W(7) AGAINST mg-c50b's EXHAUSTIVE 0.890780")
print("=" * 78)
print("  from the SAME n=7 sweep as W3 -- one pass, two arms (see the note there).")
arm("primitive count at n=7 is mg-c50b's 86278", N7_PRIM == 86278, str(N7_PRIM))
arm("W(7) = 0.890780 reproduces on this tree's own objective",
    abs(N7_BEST - 0.890780) < 5e-7,
    "%.6f at %s  (%.0fs)" % (N7_BEST, str(N7_ARG), N7_SECS))
arm("and the argmax is mg-c50b's (0, 0, 3, 7, 15, 3, 1)",
    N7_ARG == (0, 0, 3, 7, 15, 3, 1), str(N7_ARG))

print()
print("=" * 78)
print("S7  THE MOVE SET")
print("=" * 78)
tot = 0
bad = 0
for tag, dn, n in LSTAR_GAP:
    nb = neighbours(dn, n)
    tot += len(nb)
    for d2 in nb:
        if any(d2[i] >> i for i in range(n)):
            bad += 1
            continue
        for i in range(n):
            m = d2[i]
            while m:
                j = (m & -m).bit_length() - 1
                m &= m - 1
                if d2[j] & ~d2[i]:
                    bad += 1
        if d2 == dn:
            bad += 1
arm("every neighbour is naturally labelled, transitively closed, and different",
    bad == 0, "%d neighbours over the 5 gap witnesses, %d bad" % (tot, bad))
L = lifts(LSTAR_GAP[2][1], 10)
arm("lifts of an n=10 poset are all n=11 and all naturally labelled",
    all(nl == 11 and all(d[i] >> i == 0 for i in range(11)) for d, nl in L),
    "%d lifts" % len(L))

print()
print("=" * 78)
print("S8  A TABLE THAT CANNOT HAVE A BLANK CELL")
print("=" * 78)
print("""  THE DASH IS THE FINDING OF THIS TICKET, so it gets a control of its own.
  mg-5cba's audit table printed four u_M values and one dash; the dash meant NOT
  COMPUTED and read as NOT APPLICABLE; STATE.md turned it into "(M#) HOLDS at 4 of 4".
  A BLANK BECAME A BOUND, and it stood on main until this ticket multiplied the two
  halves printed either side of it.

  `emit_table` refuses any cell rendering as '', '-', '--', '---' or an em/en dash.
  A value that was not computed must say NOT-COMPUTED; one that is inapplicable must
  say N/A-<reason> and the reason is not optional.
""")
for bad in ("", " ", "-", "--", "---", "\u2014"):
    try:
        emit_table(["tag", "u_M"], [["C5", bad]])
        arm("planted blank %r is REFUSED" % bad, False, "it rendered")
    except BlankCell as e:
        arm("planted blank %r is REFUSED" % bad, True, str(e)[:44])
try:
    out = emit_table(["tag", "u_M"], [["C1", cell(0.943486)], ["C5", cell(None)]])
    arm("a genuinely uncomputed cell renders LOUD, not blank",
        "NOT-COMPUTED" in out, out.splitlines()[-1].strip())
except BlankCell:
    arm("a genuinely uncomputed cell renders LOUD, not blank", False)
try:
    out = emit_table(["tag", "x"], [["W5", cell(None, na_reason="Delta2-le-2gamma")]])
    arm("an inapplicable cell renders with its REASON attached",
        "N/A-Delta2-le-2gamma" in out, out.splitlines()[-1].strip())
except BlankCell:
    arm("an inapplicable cell renders with its REASON attached", False)
try:
    emit_table(["a", "b"], [["x"]])
    arm("a short row is REFUSED (a missing cell is a blank cell)", False)
except BlankCell as e:
    arm("a short row is REFUSED (a missing cell is a blank cell)", True, str(e)[:44])

print()
print("-" * 78)
print("ARMS FAILED: %d" % FAIL)
sys.exit(1 if FAIL else 0)
