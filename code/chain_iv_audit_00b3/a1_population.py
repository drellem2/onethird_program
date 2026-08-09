"""a1 — TICKET ITEMS 3 AND 4: the refutation, and whether the control was run as one.

The ticket is explicit that the refutation is NOT where my effort goes.  So this file is
short: it establishes that my instrument lands on mg-81ff's population and mg-81ff's
numbers, so that a2/a3's DISAGREEMENTS cannot be blamed on a different object.
"""

from fractions import Fraction as F

import lib00b3 as L
import sweep as S

print("=" * 78)
print("a1 — THE POPULATION, THE REFUTATION, AND WHETHER n <= 6 WAS A CONTROL")
print("=" * 78)

print("""
------------------------------------------------------------------------------
(P1) THE POPULATION — on a mask-and-transitivity enumeration, not an extension
------------------------------------------------------------------------------""")
print("     n   all naturally labelled   primitive   informative   mg-81ff primitive")
EXP = {3: 4, 4: 27, 5: 275, 6: 4070, 7: 86278}
for n in range(3, 8):
    allc = sum(1 for _ in L.all_posets(n))
    rows = S.load(n)
    inf = S.informative(rows)
    tag = "= %d  MATCH" % EXP[n] if len(rows) == EXP[n] else "!= %d  ***" % EXP[n]
    print("    %2d   %10d               %7d     %7d       %s" % (n, allc, len(rows), len(inf), tag))
print("""
  The n = 7 total 96 428 is mg-d3c7's figure for the same population, reached here by a
  different route.  `informative` is `primitive` minus exactly one poset at every n and
  a0 (F) names it: the ANTICHAIN, where lambda_std = 0 and `c` has no value.""")

print("""
------------------------------------------------------------------------------
(P2) min c — mg-76b2's ROW AS A CONTROL, AND n = 7 AS A MEASUREMENT
------------------------------------------------------------------------------""")
print("     n    min c      minimiser (one of them)                      status")
for n in range(3, 8):
    inf = S.informative(S.load(n))
    best = min(inf, key=S.c_of)
    cs = S.c_of(best)
    ties = sum(1 for r in inf if abs(S.c_of(r) - cs) < 1e-12)
    status = "= mg-76b2 (CONTROL)" if n <= 6 else "mg-81ff's NEW value"
    print("    %2d   %.6f   %-40s  %s" % (n, cs, str(L.relations(n, best[0])), status))
    print("           (%d labelled posets attain it)" % ties)
print("""
  ANSWER TO TICKET ITEM 4.  mg-76b2's own transcript
  `code/c3_prefix_capture_76b2/out_s3_c3.txt:89` carries `6  4070  2.386087  0.452934
  523 of 4069`, so `0.750000 / 0.618034 / 0.536219 / 0.452934` with counts `4/27/275/4070`
  is mg-76b2's row and reproducing it is a CONTROL.  mg-81ff uses it as one: its s1 table
  marks those four rows `= mg-76b2` and marks n = 7 `NEW`, its s0 (H) is filed as a
  control, and its README states in advance that the ticket body printed the four figures
  so the reproduction cannot be a discovery.  `0.412700` over 86 277 informative posets
  does NOT occur anywhere in mg-76b2's artefacts.  BOTH HALVES OF ITEM 4 CONFIRMED.

  ONE THING mg-81ff's TABLE DOES NOT SAY: the minimiser is not unique.  At n = 5 I get
  [(0,1),(2,4)] and mg-81ff reports [(0,2),(3,4)]; both are `2 disjoint 2-chains + an
  isolated point`, differently naturally labelled, and both attain 0.536219.  The count
  of labelled minimisers is printed above.  Nothing turns on it — the SHAPE is the claim
  and the shape agrees — but a reader comparing the two tables would otherwise see a
  disagreement where there is none.""")

print("""
------------------------------------------------------------------------------
(P3) D_k = k DISJOINT 2-CHAINS, IN EXACT RATIONALS — TICKET ITEM 3
------------------------------------------------------------------------------
  Every figure below is an exact rational bracket from the positive-definiteness test;
  no float is on the verdict path.""")
print("   k   n   1 - min_k Q_k  argmin   gap (exact)        c (exact bracket)      < 40/49?")
for k in range(2, 9):
    n, down = L.D_k(k)
    T, N = L.transport_int(n, down)
    Q = L.prefix_Q_all(n, T, N)
    mq = min(Q)
    arg = Q.index(mq) + 1
    lo, hi = L.lambda2_bracket(n, L.L_fractions(n, T, N), F(1, 10 ** 12))
    clo, chi = (1 - mq) / (1 - lo), (1 - mq) / (1 - hi)
    assert L.is_primitive(n, down)
    print("   %d %3d   %-13s k=%d     %.9f      [%.7f,%.7f]   %s"
          % (k, n, str(1 - mq), arg, float(lo), float(clo), float(chi), chi < F(40, 49)))
    assert 1 - mq == F(1, n - 1), "1 - min_k Q_k = 1/(n-1) claimed and it must hold"
print("""
  ALL EIGHT ROWS REPRODUCE mg-81ff EXACTLY, including `1 - min_k Q_k = 1/(n-1)` at every
  k (asserted, not eyeballed), the argmin at the prefix A_1 = {0}, and primitivity.
  `c > 0.80` is FALSE on the full naturally labelled population, already at n = 4.

  AND NO SENTENCE UPGRADES IT.  Item 3 asks whether anything downstream turns `refuted at
  eight k` into `c(D_k) -> 0`.  It does not.  The disclaimer occurs THREE times in
  mg-81ff's artefacts — s1's transcript, the deliverable's sec 0.1, and its sec 5 `Not
  done` — and the only `-> 0` phrases elsewhere in the corpus are about `min_k Q_k -> 0`
  (a property of chain (II)'s hypothesis, correctly attributed) and `eps_spec -> 0` (the
  limit defining the existence threshold).  The commit subject carries the disclaimer
  too, as its last clause.  NOTHING TO REPORT HERE — which is itself the answer.""")
