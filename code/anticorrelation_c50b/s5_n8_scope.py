"""s5 -- THE n = 8 RESULT RESTATED AT ITS ACTUAL SCOPE, AND (L*) AT n = 8.

A DEFECT OF MY OWN, CAUGHT AND KEPT.  `s3_n8.py` printed

    "(F)  FAILS at 3589 of 2600369 primitive   [EXACT on every survivor]"
    "(M#) FAILS at 0 of 2600369 primitive"

and BOTH lines state the wrong population.  s3's stage-1 screen keeps a poset only when
f* > 0.85 AND c#_UB > 0.85, so a poset where (M#) fails while (F) is comfortable
(c# = 1.1, f* = 0.4) is screened OUT and never reaches stage 2.  The counts are over
SURVIVORS, not over the 2600369.  This is PREDICTIONS.md E9 -- a screened population read
as an enumerated one -- committed by me, in my own instrument, at the one place where
the population changes underfoot.

WHAT IS EXHAUSTIVE AND WHAT IS NOT, at n = 8:

  EXHAUSTIVE and EXACT:
    * BOTH ROUTES FAIL at 0 of 2600369.  Both failing forces min(c#,f*) > 1 > 0.85 and
      c#_UB >= c#, so every both-failing poset survives the screen.  None did.
    * c_or(8) = max_P min(c#,f*) = 0.943649.  Every excluded poset provably has
      min(c#,f*) <= min(c#_UB, f*) <= 0.85 < 0.943649.
    * the population 2800472 / 2600369.

  NOT a census, and relabelled here:
    * "(F) fails at 3589" is a LOWER BOUND on the (F)-failure count at n = 8: it counts
      the (F)-failures that ALSO have c#_UB > 0.85.
    * "(M#) fails at 0" says only that no n = 8 poset has (M#) failing AND f* > 0.85.
      It says NOTHING about (M#)'s failure count at n = 8, which this ticket did not
      compute and does not claim.
"""
import pickle, math, sys
from fractions import Fraction
from libc50b import Poset, height, mu_exhaustive

N = 8
with open("out_s3_survivors.pkl", "rb") as fh:
    surv = pickle.load(fh)
print("=" * 78)
print("S5.  n = 8 AT ITS ACTUAL SCOPE, AND (L*) THERE")
print("=" * 78)
print("  survivors of the stage-1 screen: %d" % len(surv))

Ffail = []
for dn in surv:
    P = Poset(dn, N)
    if P.F_fails():
        Ffail.append(P)
print("  of which (F) FAILS at: %d   <-- a LOWER BOUND on the n=8 (F)-failure count,"
      % len(Ffail))
print("                              not a census (see this file's docstring)")

cert = 0
worst_rd = 0.0
min_uM = (float("inf"), None)
hh = {}
for P in Ffail:
    ub = P.mu_upper()[0]
    if P.gap_ge(ub * P.Delta()):
        cert += 1
    g = P.gamma_float()
    d = float(P.Delta())
    mu, _ = mu_exhaustive(P)
    worst_rd = max(worst_rd, mu / g * d)
    disc = d * d - 2 * g
    ts = d - math.sqrt(disc) if disc > 0 else None
    uM = mu / ts if ts and ts > 0 else 0.0
    if uM < min_uM[0]:
        min_uM = (uM, P.dn)
    h = height(P.dn, N)
    hh[h] = hh.get(h, 0) + 1

print()
print("  *** (L*) AT n = 8 ***")
print("  (L*)  M^2 > 2 gamma  ==>  mu_pref * Delta_P <= gamma")
print("  CERTIFIED EXACTLY (integer PSD test) at %d of %d      %s"
      % (cert, len(Ffail), "ALL" if cert == len(Ffail) else "*** NOT ALL ***"))
print("  max rho*Delta over that set (float measurement) = %.6f" % worst_rd)
print("  heights of that set: %s" % dict(sorted(hh.items())))
print()
print("  *** THE DISJUNCTION MARGIN AT n = 8 ***")
print("  min u_M = mu_pref/t* over the same set = %.6f   (margin %.1f%%)"
      % (min_uM[0], 100 * (1 - min_uM[0])))
print("  attained at dn = %s" % (min_uM[1],))
print("""
  READING.  Every (F)-failure reachable by the screen at n = 8 satisfies (L*), on
  integers.  Since the screen provably contains every both-failing poset, (L*) on this
  set is enough to give the disjunction at n = 8 -- again by ONE sufficient condition
  rather than by 2600369 separate checks.
""")
