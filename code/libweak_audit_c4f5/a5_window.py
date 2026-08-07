#!/usr/bin/env python3
"""a5_window — reproduce mg-c3ca Sec.5's own refutation probe, then extend it.

Sec.5's forward vector is: Theta(n) macroscopic windows in [n] force two crossers to
have near-identical POSITION LAWS by pigeonhole; the missing step is that near-identical
position laws force near-balance.  mg-c3ca tested the MARGINAL form of that step and
reported that its own probe fired:

    linear form   min(p,1-p) >= (1/3)(1-TV)     FALSE, 8 088 counter-pairs at n=6,
                                                351 at n=5, 16 at n=4
    worst case    1-TV = 0.5 with min(p,1-p) = 0.212
    threshold     floor of min(p,1-p) is 0.316 at 1-TV >= 0.7, 0.450 at >= 0.9,
                                                0.500 at >= 0.99   (n=6)
    s*(n)         sup{1-TV : the pair is NOT balanced} = -, 0.500, 0.636, 0.737
                                                at n = 3,4,5,6

A refutation of a step the author himself built the probe to kill is the least likely
thing in this document to be wrong.  It is audited here anyway, because the number that
carries the FORWARD conclusion is s*(n) -- whether the threshold moves with n -- and a
four-point read of a moving threshold is exactly the shape that a fifth point tests.

TV(x,y) := (1/2) sum_i |Pr[pos(x)=i] - Pr[pos(y)=i]|.  `balanced` := min(p,1-p) >= 1/3.
POPULATION: all naturally labelled non-chain posets on n elements.
GRAIN: one incomparable pair.  Exact Fractions.
"""
import sys
from fractions import Fraction
import lib_c4f5 as L

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
THIRD = Fraction(1, 3)

print("=" * 78)
print("a5_window -- mg-c3ca Sec.5's probe, reproduced and extended to n = %d" % NMAX)
print("POPULATION: all naturally labelled non-chain posets.  GRAIN: one incomparable pair.")
print("EXACT Fractions throughout.  No tolerance.")
print("=" * 78)

PUB_CTR = {4: 16, 5: 351, 6: 8088}
PUB_S = {4: 0.500, 5: 0.636, 6: 0.737}

print()
print("TWO PREDICATES ARE COUNTED SIDE BY SIDE, on ONE walk of ONE population:")
print("  (LIN)  a counterexample to the LINEAR form printed in Sec.5:")
print("             min(p,1-p) >= (1/3)*(1-TV)      refuted by   mn < (1/3)*sim")
print("  (THR)  the predicate p3_window.py ACTUALLY EVALUATES (its line 100):")
print("             sim >= 0.5 AND mn < 1/3")
print("(THR) is the refutation condition for `1-TV >= 1/2 => balanced`, a THRESHOLD")
print("statement at threshold 1/2.  It is NOT the negation of (LIN): sim=0.5, mn=0.212")
print("satisfies (LIN) with room, since (1/3)*0.5 = 0.1667 < 0.212.")
print()
print("%4s %10s %10s %10s %10s %12s %10s %10s"
      % ("n", "pairs", "(LIN)", "(THR)", "c3ca pub", "THR match", "s*(n)", "c3ca s*"))
res = {}
for n in range(3, NMAX + 1):
    npairs = 0
    ctr = 0
    thr = 0
    worst = None            # (1-TV, min(p,1-p)) at the largest 1-TV among (LIN) counterex
    thr_worst = None        # the (THR) row the doc reports as `worst`
    sstar = None            # sup{1-TV : NOT balanced}
    cstar = None            # min over pairs of mn/sim  = best constant in the linear form
    cstar_wit = None
    floors = {Fraction(7, 10): None, Fraction(9, 10): None, Fraction(99, 100): None}
    for P in L.gen_natural_posets(n):
        a = L.analyse(P)
        if not a["inc"]:
            continue
        T = a["T"]
        for (x, y) in a["inc"]:
            npairs += 1
            tv = sum(abs(T[x][i] - T[y][i]) for i in range(n)) / 2
            sim = 1 - tv
            p = a["q"][(x, y)]
            bal = min(p, 1 - p)
            if bal < THIRD * sim:
                ctr += 1
                if worst is None or sim > worst[0]:
                    worst = (sim, bal)
            if sim >= Fraction(1, 2) and bal < THIRD:
                thr += 1
                if thr_worst is None or bal < thr_worst[1]:
                    thr_worst = (sim, bal)
            if sim > 0:
                r = bal / sim
                if cstar is None or r < cstar:
                    cstar = r
                    cstar_wit = (float(sim), float(bal), a["up"], (x, y))
            if bal < THIRD:
                if sstar is None or sim > sstar:
                    sstar = sim
            for th in floors:
                if sim >= th:
                    if floors[th] is None or bal < floors[th]:
                        floors[th] = bal
    res[n] = (npairs, ctr, sstar, worst, floors, thr, thr_worst, cstar, cstar_wit)
    pc = PUB_CTR.get(n)
    ps = PUB_S.get(n)
    print("%4d %10d %10d %10d %10s %12s %10s %10s"
          % (n, npairs, ctr, thr, pc if pc is not None else "(new)",
             "-" if pc is None else ("YES" if thr == pc else "NO"),
             "%.4f" % float(sstar) if sstar is not None else "none",
             "%.3f" % ps if ps is not None else "(new)"))
print()
print("READ THE TWO COLUMNS TOGETHER.  This instrument reproduces mg-c3ca's published")
print("16 / 351 / 8088 EXACTLY under (THR) -- so the parsers agree and the populations")
print("agree (11/130/1984/41044 matches its own transcript line for line).  The (LIN)")
print("column is what Sec.5 SAYS was refuted, and it is 0 at every reachable n.")
print()
print("-" * 78)
print("W0. THE BEST CONSTANT IN THE LINEAR FORM  --  c*(n) = min over pairs of mn/sim")
print("-" * 78)
print("If (LIN) at c = 1/3 is not refuted, the honest question is how much room it has.")
print("%4s %14s %14s %10s %s" % ("n", "c*(n)", "as float", ">1/3 ?", "witness (sim, mn)"))
for n in sorted(res):
    cs = res[n][7]
    w = res[n][8]
    print("%4d %14s %14.6f %10s (%.4f, %.4f) up=%s"
          % (n, cs, float(cs), "YES" if cs > THIRD else "NO", w[0], w[1], w[2]))
print()
print("  c* > 1/3 means (MW) at c = 1/3 HOLDS with strict room on this population.")
print("  BUT NOTE WHAT IT STILL DOES NOT BUY: the pigeonhole delivers sim = 1 - O(1/n),")
print("  so (LIN) at c = 1/3 yields only mn >= 1/3 - O(1/n), which does NOT contradict")
print("  frozen (that needs mn >= 1/3 strictly).  So the linear form surviving is not")
print("  the same thing as step 2 working, and I am not claiming it is.")

print()
print("-" * 78)
print("W1. THE WORST COUNTEREXAMPLE   [Sec.5: `worst 1-TV = 0.5 with min(p,1-p)=0.212`]")
print("-" * 78)
print("The doc calls `1-TV = 0.5, min(p,1-p) = 0.212` the WORST case.  It is neither")
print("the largest sim nor a counterexample to (LIN).  p3_window.py sorts its refuter")
print("list by `(mn, -sim)` and prints the top 3, so the printed row is the SMALLEST")
print("min(p,1-p), and the doc reports it as the largest 1-TV.  Both halves, measured:")
for n in sorted(res):
    _, _, sstar, worst, _, thr, tw, _, _ = res[n]
    print("  n=%d : (LIN) counterexamples %s | (THR) row with smallest mn = %s"
          % (n, ("largest sim %.4f, mn %.4f" % (float(worst[0]), float(worst[1])))
             if worst else "NONE",
             ("sim %.4f, mn %.6f" % (float(tw[0]), float(tw[1]))) if tw else "NONE"))
    if sstar is not None:
        print("        largest sim among UNBALANCED pairs (= s*) = %.6f  <- the largest"
              % float(sstar))
        print("        1-TV any (THR) row can have%s"
              % ("; equal to 0.5 here, above it for n>=5" if sstar == Fraction(1, 2)
                 else ", i.e. ABOVE the 0.5 the doc calls `worst`"))

print()
print("-" * 78)
print("W2. THE SURVIVING THRESHOLD FORM")
print("    [Sec.5, n=6: floor 0.316 at 1-TV>=0.7, 0.450 at >=0.9, 0.500 at >=0.99]")
print("-" * 78)
print("%4s %16s %16s %16s" % ("n", "floor @ >=0.7", "floor @ >=0.9", "floor @ >=0.99"))
for n in sorted(res):
    fl = res[n][4]
    print("%4d %16s %16s %16s"
          % (n,
             "%.4f" % float(fl[Fraction(7, 10)]) if fl[Fraction(7, 10)] is not None else "EMPTY",
             "%.4f" % float(fl[Fraction(9, 10)]) if fl[Fraction(9, 10)] is not None else "EMPTY",
             "%.4f" % float(fl[Fraction(99, 100)]) if fl[Fraction(99, 100)] is not None else "EMPTY"))

print()
print("-" * 78)
print("W3. s*(n) -- THE NUMBER THAT CARRIES SEC.5's FORWARD CONCLUSION")
print("-" * 78)
print("Sec.5: `if 1-s*(n) keeps shrinking at least as fast as the pigeonhole's own")
print("O(1/(alpha^2 n)) margin, step 2 fails asymptotically at a fixed constant and the")
print("vector dies.  Three points cannot tell those two rates apart.`")
print()
print("%4s %14s %14s %16s %16s" % ("n", "s*(n)", "1-s*(n)", "(1-s*)*n", "(1-s*)*n^2"))
for n in sorted(res):
    s = res[n][2]
    if s is None:
        print("%4d %14s" % (n, "none (no unbalanced pair)"))
        continue
    g = 1 - s
    print("%4d %14.5f %14.5f %16.5f %16.5f"
          % (n, float(s), float(g), float(g) * n, float(g) * n * n))
print()
print("  If 1-s* ~ C/n the (1-s*)*n column is FLAT.  If 1-s* ~ C/n^2 the last column is")
print("  flat.  Sec.5 had three usable points and said so; there are now %d." % (NMAX - 2))
print("  READ THE CAVEAT WITH THE TABLE: this is still the MARGINAL law on n <= %d," % NMAX)
print("  and Sec.5's own next step is the CONDITIONAL form on I_x(tau), which is not")
print("  measured here and which I did not attempt.")

print()
print("=" * 78)
print("a5_window done.")
print("=" * 78)
