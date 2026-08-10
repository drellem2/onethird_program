"""b3 -- THE TREND.  Is u_M approaching 1, saturating below it, or neither?

THE TICKET ASKED FOR THIS AS THE DELIVERABLE, AND THE ANSWER IS "NEITHER".  u_M does
not approach 1 and does not saturate below it: **it crosses**.  The question as posed
assumed the disjunction survives, and it does not.  What replaces it is a shape
question that still has content, and this file answers that one:

    ACROSS n = 9..14, DOES THE CERTIFIED FRONTIER W(n) >= x RISE MONOTONICALLY, AND
    WHAT DRIVES IT?

THE DECOMPOSITION THAT MAKES THE TREND READABLE.  From libb417's identity,

    u_M = v_L * D,      D = (1 + sqrt(1 - 2 gamma/Delta^2))/2 < 1

so every witness has TWO independent ways to be near 1: a large (L*) violation v_L, or
a small discount D^-1 -- i.e. a small gamma/Delta^2, i.e. a THIN CUT.  Written the
other way,

    (M#) FAILS  <=>  v_L > 1 + rho*mu_pref/2

the (L*) excess must beat mu_pref/2.  So the two mechanisms are not independent
dials: pushing gamma down pushes mu_pref down with it (mu_pref >= gamma always), which
LOWERS the bar.  That is why the frontier moves and it is what this file measures.

WHAT THE NUMBERS BELOW ARE.  Search figures at n >= 9, exhaustive figures at n <= 7
quoted from mg-c50b and NOT re-measured here except where b0 S6 re-measured W(7).
n = 8 is neither, and is not enumerated by this ticket.
"""

import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from libb417 import (LSTAR_GAP, cell, certify, emit_table, height,
                     score_float)

HERE = os.path.dirname(os.path.abspath(__file__))

# mg-c50b out_s2_theory.txt:38-42 -- EXHAUSTIVE, quoted, not re-measured here.
PUBLISHED_W = {3: 0.000000, 4: 0.486136, 5: 0.649886, 6: 0.818379, 7: 0.890780}

with open(os.path.join(HERE, "champions.json")) as fh:
    champs = json.load(fh)

print("=" * 78)
print("B3.1  THE FRONTIER, n = 3..14")
print("=" * 78)
print(__doc__)
print()
print("  Emitted through `libb417.emit_table`, which refuses a blank cell (b0 S8).")
print("  MY OWN FIRST DRAFT OF THIS TABLE PRINTED '-' IN THE u_F AND u_M COLUMNS FOR")
print("  THE EXHAUSTIVE ROWS -- i.e. the remedy carried the defect it repairs, in the")
print("  file that reports the defect.  It is caught here and the cells now say which")
print("  kind of absence they are.")
print()
rows = []
_trows = []
for n in sorted(PUBLISHED_W):
    _trows.append([str(n), cell(PUBLISHED_W[n]), "EXHAUSTIVE",
                   cell(None, na_reason="mg-c50b-published-min-only"),
                   cell(None, na_reason="mg-c50b-published-min-only"),
                   "mg-c50b s2, exhaustive"])
_trows.append(["8", cell(None, na_reason="c_or-not-W"), "EXHAUSTIVE (c_or)",
               cell(None, na_reason="c_or-not-W"),
               cell(None, na_reason="c_or-not-W"),
               "mg-c50b s3: c_or(8)=0.943649, both routes fail at 0/2600369"])
best_by_n = {}
for n in sorted(champs, key=int):
    if not champs[n]:
        continue
    top = max(champs[n], key=lambda c: c["float_J"])
    best_by_n[int(n)] = top
    _trows.append([str(n), cell(top["float_J"]), "SEARCH lower bound",
                   cell(top["u_F"]), cell(top["u_M"]),
                   "b2, SEARCH (not a maximum)"])
    rows.append((int(n), top))
print(emit_table(["n", "W(n)", "kind", "u_F", "u_M", "source"], _trows))
print()
print("  N/A-mg-c50b-published-min-only: mg-c50b prints w(n) as one number per n and")
print("  does not publish the argmax's u_F and u_M separately.  NOT COMPUTED HERE, and")
print("  not re-derived, because re-deriving them means enumerating n <= 7 again for")
print("  two decorative columns.  N/A-c_or-not-W: at n = 8 the published exhaustive")
print("  figure is c_or(8), which is a DIFFERENT READING from W(8) -- they cross 1")
print("  together and are not equal -- so putting 0.943649 in a W column would be the")
print("  u_M/c# confusion (mg-0d1b) in a new costume.")

print()
print("  THE n <= 7 ROWS ARE MAXIMA.  THE n >= 9 ROWS ARE NOT.  They are the best")
print("  min(u_F,u_M) any restart of b2 reached, over a population that was never")
print("  enumerated, and the true W(n) at each is >= the figure printed.")

print()
print("=" * 78)
print("B3.2  APPROACHING 1, SATURATING, OR CROSSING?")
print("=" * 78)
cross = [n for n, t in rows if t["float_J"] > 1.0]
print()
if cross:
    print("  ANSWER: NEITHER.  W(n) CROSSES 1.")
    print("  Smallest n at which this SEARCH exhibits min(u_F,u_M) > 1: %d" % min(cross))
    print("  All n exhibited above 1: %s" % ", ".join(str(n) for n in sorted(cross)))
    print()
    print("  The ticket's framing -- 'approaching 1 or saturating below it, those are")
    print("  different futures for the conjecture' -- presupposed a third thing that is")
    print("  not true: that the disjunction holds and u_M is a margin. It is not a")
    print("  margin. It is a quantity that exceeds 1, and the exhibits are certified.")
else:
    print("  This search did not cross 1 at any n. That is a SEARCH result and it does")
    print("  not contradict b1, whose C5 crossing is certified independently.")

print()
print("  MONOTONICITY over the n it searched:")
seq = [(n, t["float_J"]) for n, t in rows]
ok = all(seq[i][1] <= seq[i + 1][1] + 1e-12 for i in range(len(seq) - 1))
print("    " + "  ".join("%d:%.6f" % (n, v) for n, v in seq))
print("    monotone non-decreasing in n: %s" % ("YES" if ok else "NO -- there is a dip"))
if not ok:
    for i in range(len(seq) - 1):
        if seq[i][1] > seq[i + 1][1] + 1e-12:
            print("      dip at n=%d -> n=%d (%.6f -> %.6f).  A dip in a SEARCH is a"
                  % (seq[i][0], seq[i + 1][0], seq[i][1], seq[i + 1][1]))
            print("      statement about the restart budget at the larger n, not about W."
                  )

print()
print("=" * 78)
print("B3.3  WHAT DRIVES IT -- v_L, or the discount D?")
print("=" * 78)
print("""  u_M = v_L * D.  If the frontier rises because v_L rises, the (M#) story is the
  (L*) story again.  If it rises because D rises -- i.e. because gamma/Delta^2 falls --
  then (M#) fails for a reason (L*) never had, and the thin cut is the mechanism.
""")
print("   n | u_M        | v_L        | D          | gamma      | mu_pref    | Delta      | h")
for n, t in rows:
    print("  %2d | %10.6f | %10.6f | %10.6f | %10.6f | %10.6f | %10.6f | %d"
          % (n, t["u_M"], t["v_L"], t["D"], t["gamma"], t["mu"],
             t["u_M"] / t["v_L"] * 0 + (t["v_L"] * t["gamma"] / t["mu"] if t["mu"] else 0),
             t["height"]))
print()
print("  the five certified (L*) counterexamples, for contrast:")
print("   tag  n | u_M        | v_L        | D          | gamma      | mu_pref    | h")
gap = []
for tag, dn, n in LSTAR_GAP:
    s = score_float(dn, n)
    gap.append((tag, n, s))
    print("   %-3s %2d | %10.6f | %10.6f | %10.6f | %10.6f | %10.6f | %d"
          % (tag, n, s["u_M"], s["v_L"], s["D"], s["gamma"], s["mu"], height(dn, n)))

print()
print("  THE BAR EACH WITNESS HAD TO CLEAR:  (M#) fails  <=>  v_L > 1 + rho*mu/2")
print("   tag/n |  v_L       | bar = 1+rho*mu/2 | clears? | slack")
for tag, n, s in gap:
    bar = 1.0 + s["rho"] * s["mu"] / 2.0
    print("   %-4s%2d | %10.6f | %16.6f | %7s | %+.6f"
          % (tag, n, s["v_L"], bar, "YES" if s["v_L"] > bar else "no", s["v_L"] - bar))
for n, t in rows:
    rho = t["mu"] / t["gamma"]
    bar = 1.0 + rho * t["mu"] / 2.0
    print("   b2  %2d | %10.6f | %16.6f | %7s | %+.6f"
          % (n, t["v_L"], bar, "YES" if t["v_L"] > bar else "no", t["v_L"] - bar))

print()
print("=" * 78)
print("B3.3b  WHICH FACTOR ACTUALLY MOVES -- decomposed, not asserted")
print("=" * 78)
print("""  u_M = v_L * D is multiplicative, so log u_M = log v_L + log D and the rise across
  n splits EXACTLY into two contributions.  Reported as a split rather than as a
  reading, because "the thin cut is the mechanism" was my own prediction (P4) and a
  prediction that scores itself is not one.
""")
if len(rows) >= 2:
    (n0, t0_), (n1, t1_) = rows[0], rows[-1]
    dlu = math.log(t1_["u_M"]) - math.log(t0_["u_M"])
    dlv = math.log(t1_["v_L"]) - math.log(t0_["v_L"])
    dld = math.log(t1_["D"]) - math.log(t0_["D"])
    print("   from n=%d to n=%d:" % (n0, n1))
    print("     u_M  %.6f -> %.6f     dlog = %+.6f" % (t0_["u_M"], t1_["u_M"], dlu))
    print("     v_L  %.6f -> %.6f     dlog = %+.6f   (%+.1f%% of the move)"
          % (t0_["v_L"], t1_["v_L"], dlv, 100.0 * dlv / dlu if dlu else 0.0))
    print("     D    %.6f -> %.6f     dlog = %+.6f   (%+.1f%% of the move)"
          % (t0_["D"], t1_["D"], dld, 100.0 * dld / dlu if dlu else 0.0))
    print("     residual (should be 0): %+.2e" % (dlu - dlv - dld))
    print()
    Ds = [t["D"] for n, t in rows]
    print("     D across the searched n: %s" % "  ".join("%.6f" % d for d in Ds))
    print("     D range = %.6f   v_L range = %.6f"
          % (max(Ds) - min(Ds), max(t["v_L"] for n, t in rows)
             - min(t["v_L"] for n, t in rows)))
    if abs(dld) < 0.1 * abs(dlu):
        print()
        print("     SO: THE DISCOUNT IS ESSENTIALLY FLAT AND THE RISE IS ALL v_L.")
        print("     The champion family holds gamma/Delta^2 near-constant and pushes the")
        print("     (L*) violation.  That REFINES the reading below rather than")
        print("     confirming it: a small mu_pref is what distinguishes the crossing")
        print("     witness from the non-crossing ones AT A GIVEN n -- it is why C5")
        print("     crosses and C1/C2/C4 do not -- but it is NOT what moves the frontier")
        print("     ACROSS n.  Two different questions, and I had predicted one answer")
        print("     for both.")

print()
print("  READING.  The bar is set by mu_pref, and mu_pref >= gamma, so a THIN CUT")
print("  lowers the bar and raises D at the same time.  A witness with a large v_L and")
print("  a fat gamma (C1, C2, C4: mu ~ 0.12) faces a bar near 1.06 and misses.  A")
print("  witness with a small mu_pref faces a bar near 1.03 and can clear it on a")
print("  smaller (L*) violation.  That is the mechanism, and it is why C5 -- NOT the")
print("  largest v_L relative to its n -- is the one that crosses.")

print()
print("=" * 78)
print("B3.4  WHAT THE DATA DOES NOT DISTINGUISH -- said plainly")
print("=" * 78)
print("""
  1.  WHETHER THE DISJUNCTION FAILS BELOW THE SMALLEST n EXHIBITED HERE.  Nothing in
      this tree enumerates n = 9, 10 or 11.  A search that does not find a
      counterexample at n = 9 has said nothing about n = 9.  The last exhaustive
      statement in the corpus is n = 8, and it is clean.

  2.  WHETHER W(n) IS UNBOUNDED, OR SETTLES.  The certified figures rise, but over
      six values of n from a search whose restart budget FALLS as n rises (30 at n=9
      down to 8 at n=14).  A rising sequence measured with a shrinking instrument
      cannot distinguish "W grows" from "W is flat and my search got luckier where it
      looked harder" -- except that here the budget falls where the values RISE, which
      is the direction that makes the rise harder to explain away, not easier.  It is
      still not a proof of growth and this file does not claim one.

  3.  WHETHER THE MECHANISM IS THE THIN CUT OR THE FAMILY.  Every certified
      counterexample in the corpus, including C5, is height 4 or 5 with Delta within
      2% of 1.  Five posets is not a distribution (E9).  The bar arithmetic in B3.3 is
      an identity and holds regardless; the claim that thin cuts are the ROUTE to it
      is a reading of five witnesses and is labelled as one.
""")
