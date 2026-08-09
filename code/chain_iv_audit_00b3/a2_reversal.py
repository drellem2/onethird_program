"""a2 — TICKET ITEM 1: THE STRATIFICATION REVERSAL, ATTACKED.

The ticket's question is precise: `Is the monotonicity real across all six bands, or does
it depend on band boundaries chosen after seeing the data?  A reversal that is an artefact
of binning would invert the conclusion back to "chain IV dies".`

Four attacks, in increasing order of how hard they are to blame on a choice:

  (R1)  reproduce mg-81ff's seven bands exactly, from my own sweep
  (R2)  re-bin the SAME population at ten uniform widths — does monotonicity survive?
  (R3)  re-bin at EQUAL COUNT, which removes the one confound mg-81ff itself names
        (a minimum over more posets falls for free)
  (R4)  remove bins entirely: for EVERY threshold t, is min c below t at least min c
        above t?  There are as many tests as there are distinct gaps.

and then the thing that should be quoted instead of a band table: a single bin-free
number per n.
"""

import sweep as S
import lib00b3 as L

BANDS = [(0.00, 0.06), (0.06, 0.10), (0.10, 0.20), (0.20, 0.30),
         (0.30, 0.50), (0.50, 0.70), (0.70, 1.01)]
TH49 = 40 / 49
TH80 = 0.80

rows = {n: S.informative(S.load(n)) for n in (4, 5, 6, 7)}


def minc(rs):
    return min(S.c_of(r) for r in rs)


print("=" * 78)
print("a2 — IS THE REVERSAL REAL, OR IS IT THE BINS?")
print("=" * 78)

print("""
------------------------------------------------------------------------------
(R1) mg-81ff's SEVEN BANDS, RE-DERIVED
------------------------------------------------------------------------------""")
print("  gap band            n=6 posets   min c      n=7 posets   min c")
for lo, hi in BANDS:
    a = [r for r in rows[6] if lo <= r[1] < hi]
    b = [r for r in rows[7] if lo <= r[1] < hi]
    print("  [%.2f, %.2f)        %6d   %.6f      %6d   %.6f"
          % (lo, hi, len(a), minc(a), len(b), minc(b)))
print("""
  ALL FOURTEEN min c VALUES REPRODUCE EXACTLY, to every printed digit, on an instrument
  sharing no line with mg-81ff's.  So does the top band's break of the pattern, which
  mg-81ff printed rather than dropped.

  TWO OF THE FOURTEEN COUNTS DIFFER BY ONE, AND THE REASON IS THE FINDING'S OWN FRAGILITY
  CLASS: I get 1035 / 1259 at n = 6 in [0.20,0.30) / [0.30,0.50) where mg-81ff has
  1034 / 1260; the totals agree at 4069.  One poset — relations
  [(0,2),(0,4),(0,5),(1,2),(1,4),(1,5),(3,4),(3,5)] — has lambda_2 EXACTLY 3/10, which I
  certified rather than inferred (the exact test says lambda_2 > 3/10 is FALSE and
  lambda_2 > 3/10 - 10^-12 is TRUE).  It sits on a band edge, so which half-open band it
  lands in is decided by the last bit of whichever eigenroutine ran.  Its c is 0.785714
  and it is nobody's minimum, so NOTHING in the reading moves.  It is reported because a
  boundary that a rounding error can move is the exact hazard this section is testing.""")

print("""
------------------------------------------------------------------------------
(R2) THE SAME POPULATION, RE-BINNED AT TEN UNIFORM WIDTHS
------------------------------------------------------------------------------
  `Monotone` is a property of a partition.  If it survives only mg-81ff's partition it is
  a property of the partition and not of the posets.""")
print("   width   n   bands   adjacent pairs violating   worst rise   of those, both bands < 0.30")
for w in (0.50, 0.25, 0.20, 0.125, 0.10, 0.05, 0.04, 0.025, 0.02, 0.01):
    for n in (6, 7):
        edges = []
        x = 0.0
        while x < 1.01 + 1e-12:
            edges.append(x)
            x += w
        edges.append(1.01)
        vals = []
        for lo, hi in zip(edges[:-1], edges[1:]):
            b = [r for r in rows[n] if lo <= r[1] < hi]
            if b:
                vals.append((lo, hi, minc(b), len(b)))
        v = [(vals[i], vals[i + 1]) for i in range(len(vals) - 1)
             if vals[i + 1][2] > vals[i][2] + 1e-12]
        worst = max((b[2] - a[2] for a, b in v), default=0.0)
        low = [(a, b) for a, b in v if b[1] <= 0.30]
        print("   %.3f   %d   %5d   %11d of %-11d   %.4f       %d"
              % (w, n, len(vals), len(v), len(vals) - 1, worst, len(low)))
print("""
  >>> STRICT MONOTONICITY IS NOT A PROPERTY OF THE POPULATION.  At width 0.01 half the
      adjacent pairs violate it at both n.  And the violations are NOT confined to the
      near-antichain tail mg-81ff discloses: 10 of them (n = 6) and 7 (n = 7) have BOTH
      bands below gap 0.30, i.e. inside the low-gap region the reading rests on.  The
      largest of those is n = 6, [0.130,0.140) min c 0.824256 -> [0.140,0.150) 0.874508.

      SO THE WORD `monotonically` IN THE HEADLINE IS CARRIED BY THE CHOICE OF SIX BANDS.
      What follows tests whether anything survives it.""")

print("""
------------------------------------------------------------------------------
(R3) EQUAL-COUNT BANDS — the one confound mg-81ff names, removed
------------------------------------------------------------------------------
  mg-81ff sec 3(b): `it is confounded with population size (a min over more posets falls
  for free)`.  It applies that to the n-comparison.  It applies with EQUAL force to the
  band comparison — the lowest band holds 14 posets at n = 6 and the [0.10,0.20) band
  holds 1350 — and mg-81ff does not apply it there.  So: hold the count exactly fixed.""")
for n in (6, 7):
    for B in (4, 6, 8, 10):
        rs = sorted(rows[n], key=lambda r: r[1])
        m = len(rs)
        step = m / B
        vals = []
        for b in range(B):
            ch = rs[int(b * step):int((b + 1) * step)]
            vals.append((ch[0][1], ch[-1][1], len(ch), minc(ch)))
        viol = sum(1 for i in range(B - 1) if vals[i + 1][3] > vals[i][3] + 1e-12)
        print("   n=%d  %2d equal-count bands of %5d:  violations %d of %d"
              % (n, B, vals[0][2], viol, B - 1))
        if viol:
            for i in range(B - 1):
                if vals[i + 1][3] > vals[i][3] + 1e-12:
                    print("        gap [%.4f,%.4f] min c %.6f  ->  [%.4f,%.4f] min c %.6f"
                          % (vals[i][0], vals[i][1], vals[i][3],
                             vals[i + 1][0], vals[i + 1][1], vals[i + 1][3]))
print("""
  >>> THE CONFOUND DOES NOT EXPLAIN IT.  With the count held exactly equal, monotone at
      4, 6 and 8 bands at BOTH n and at 10 bands at n = 7.  The single violation, at
      n = 6 with 10 bands, is 0.807852 -> 0.813616, a rise of 0.006.""")

print("""
------------------------------------------------------------------------------
(R4) NO BINS AT ALL — every threshold, not seven of them
------------------------------------------------------------------------------
  For each t, compare min c on {gap < t} with min c on {gap >= t}.  The reversal says the
  first is at least the second.  There is one test per distinct gap and no boundary is
  chosen by anybody.""")
for n in (5, 6, 7):
    rs = sorted(rows[n], key=lambda r: r[1])
    cs = [S.c_of(r) for r in rs]
    m = len(rs)
    pre = [1e9] * (m + 1)
    for i in range(m):
        pre[i + 1] = min(pre[i], cs[i])
    suf = [1e9] * (m + 1)
    for i in range(m - 1, -1, -1):
        suf[i] = min(suf[i + 1], cs[i])
    bad = []
    tested = 0
    for i in range(1, m):
        if rs[i][1] == rs[i - 1][1]:
            continue
        tested += 1
        if pre[i] < suf[i] - 1e-12:
            bad.append(rs[i][1])
    gmin = min(rows[n], key=S.c_of)[1]
    print("   n=%d: %6d distinct thresholds, %3d violate; the lowest violating t is %.6f"
          % (n, tested, len(bad), min(bad) if bad else float("nan")))
    print("        the global minimiser's OWN gap is %.6f — above it the test is trivially"
          % gmin)
    print("        false, so the content is: THE REVERSAL HOLDS AT EVERY THRESHOLD BELOW %.4f."
          % min(bad))
print("""
  >>> BIN-FREE, THE REVERSAL HOLDS.  Every split below gap ~0.56 (n=6) / ~0.60 (n=7)
      confirms it, which is the whole range between the regime (0.02) and the family that
      does the refuting (0.46+).""")

print("""
------------------------------------------------------------------------------
(R5) WHAT SHOULD BE QUOTED INSTEAD OF A BAND TABLE — ONE NUMBER PER n
------------------------------------------------------------------------------
  The largest gap cap under which the whole population still satisfies each threshold.
  No bins, no boundaries, exactly one number, and it is the number the architecture
  actually asks for.  The budget is eps_spec = 0.020.""")
print("      n   smallest gap    min c >= 40/49 for gap <=   ... >= 0.80 for gap <=   "
      "chain (IV) CLOSES (max min_k Q_k <= 1/5) for gap <=")
for n in (4, 5, 6, 7):
    rs = sorted(rows[n], key=lambda r: r[1])
    run = 1e9
    c49 = c80 = None
    for r in rs:
        run = min(run, S.c_of(r))
        if c49 is None and run < TH49:
            c49 = r[1]
        if c80 is None and run < TH80:
            c80 = r[1]
    runq = -1
    cq = None
    for r in rs:
        runq = max(runq, float(r[2]))
        if cq is None and runq > 0.2:
            cq = r[1]
    print("     %2d    %.6f        %.6f                    %.6f                 %.6f"
          % (n, rs[0][1], c49, c80, cq))
print("""
  >>> AND THIS IS WHERE mg-81ff's OWN sec 3(b) CAVEAT BITES HARDEST, IN A FORM THAT IS
      NOT CONFOUNDED WITH POPULATION SIZE, BECAUSE IT IS NOT A MINIMUM OVER A BAND BUT A
      THRESHOLD CROSSING.  Both columns FALL monotonically with n:

          c >= 40/49 safe up to gap   0.400  ->  0.172  ->  0.160  ->  0.132   (n=4..7)
          chain (IV) closes up to gap 0.226  ->  0.105  ->  0.095  ->  0.090

      against a budget of 0.020.  So the margin is 6.6x (c-form) and 4.5x (closing form)
      at n = 7 and it has been shrinking at every step.  It is decelerating and four
      points decide nothing — mg-81ff says exactly that and it is right — but this is the
      bin-free form of the caveat and it is sharper than the two-and-three-point version
      the deliverable prints.

  >>> AND ONE THING THE BAND TABLE HIDES BY BEING IN THE WRONG CURRENCY.  mg-81ff sec 1.2
      establishes that chain (IV) closes on a poset IFF min_k Q_k <= eps_leak = 1/5, and
      that `c >= 40/49` is that condition re-parametrised AT gap = eps_spec.  Away from
      that point the two are NOT the same, and the c-form is the LOOSER of the two: at
      gap = 0.10 the closing condition allows min_k Q_k up to 0.200 while `c >= 40/49`
      allows 0.265.  The consequence is visible in mg-81ff's own sec 3(a) table and is
      not remarked on there: at n = 7, max min_k Q_k over {gap <= 0.10} is 0.22436, ABOVE
      the 0.2 its own column header names as the closing condition — i.e. there is a
      poset only 5x outside the budget on which chain (IV) does not close, while the
      band table's min c at the same cap, 0.858894, reads comfortably safe.""")

VERDICT = """
==============================================================================
a2 VERDICT — TICKET ITEM 1.  THE REVERSAL IS REAL AND IS NOT AN ARTEFACT OF THE
BINS: it survives equal-count re-binning, which removes the only confound named
against it, and it survives with no bins at all at every threshold below 0.56
(n=6) / 0.60 (n=7).  `chain IV dies` is NOT the version that should have been
published.  BUT `min c rises MONOTONICALLY across the six bands` is carried by
those six bands: at uniform width 0.01 half the adjacent pairs violate it, 10 and
7 of them with both bands inside the low-gap region.  The claim that survives is
DIRECTIONAL, and the bin-free crossings of (R5) are what should be quoted for it.
==============================================================================
"""
print(VERDICT)
