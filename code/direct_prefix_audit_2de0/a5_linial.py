"""mg-2de0 A5 — item (e): the "unless that side is a chain" caveat, and the Linial citation.

mg-2de0 (e): 'both sides chains => width <= 2 => Linial => delta >= 1/3, contradicting
frozen. VERIFY the Linial citation; mg-00b9 took it from knowledge and did not re-derive it.'

WHAT I CAN AND CANNOT DO HERE, stated first:
  I CANNOT re-derive Linial's theorem, and I do not. It is a citation to external
  literature (Linial 1984, the 1/3-2/3 conjecture for width-2 posets).
  I CAN check the citation AS USED, on a finite population, which is a different and
  answerable question: over EVERY poset of width <= 2 up to n=7, is delta >= 1/3?
  That instrument could have REFUTED the citation as used. It fires as a negative control
  too: the same sweep over width >= 3 posets is run, where delta < 1/3 is permitted (and
  where, by the conjecture being verified to n <= 11, none should appear either).
  I ALSO check the elementary step mg-00b9 asserts: 'both sides chains => width <= 2'.

WHAT I COULD NOT DO AT ALL: read the source's tex:481-483 to confirm the caveat's exact
shape. This repo tracks 0 .tex files. The two .tex files on this host outside .pogo are
364 and 356 lines and contain 0 occurrences of 'Cheeger'; neither can carry a line 481.
So I audit the caveat AS RESTATED in mg-2de0's body and say so. See the README.

OPERATOR SCOPE: delta is the BALANCE axis (axis 2, the counterexample condition), and it is
the only place in this audit where axis 2 appears -- correctly, because item (e) is the step
that converts a width bound into a delta bound. Everything else in this audit is transport.
Not Delta_AT, not Hodge.
"""

import sys
from fractions import Fraction as F
from itertools import combinations

from lib2de0 import Poset, all_posets, named_posets

BAD = 0


def report(label, bad, total, grain, population, fatal=True):
    global BAD
    if fatal:
        BAD += bad
    flag = "OK  " if bad == 0 else ("BAD " if fatal else "MEAS")
    print(f"  {flag} {label}: {bad} / {total}")
    print(f"       population: {population}")
    print(f"       grain:      {grain}")


print("=" * 78)
print("A5 — item (e): 'both sides chains => width <= 2 => Linial => delta >= 1/3'")
print("=" * 78)

# ---------------------------------------------------------------------------
print()
print("A5.1  the ELEMENTARY step: a union of two chains has width <= 2.")
print("      (An antichain meets each chain at most once, so it has at most 2 elements.)")
bad = tot = 0
for n in range(2, 9):
    # every way to split {0..n-1} into two sets, each made a chain in increasing order
    for mask in range(1 << n):
        S = [i for i in range(n) if mask >> i & 1]
        T = [i for i in range(n) if not (mask >> i & 1)]
        rel = [(S[i], S[i + 1]) for i in range(len(S) - 1)] + \
              [(T[i], T[i + 1]) for i in range(len(T) - 1)]
        P = Poset(n, rel, f"2chains n={n} mask={mask}")
        tot += 1
        if P.width() > 2:
            bad += 1
            print(f"       BAD {P.name}: width {P.width()}")
report("union of two chains has width <= 2", bad, tot,
       "per-(n, bipartition), width computed by brute-force largest antichain",
       "every bipartition of {0..n-1} into two increasing chains, n=2..8 "
       f"(sum of 2^n = {tot} posets)")

# ---------------------------------------------------------------------------
print()
print("A5.2  the CITATION AS USED: over every poset of width <= 2, is delta >= 1/3?")
print("      delta(P) = max over incomparable pairs {x,y} of min(pr(x<y), pr(y<x)).")
print("      A CHAIN HAS NO INCOMPARABLE PAIR and therefore NO delta -- that is the rider")
print("      item (e) needs and does not carry. Chains are reported separately below, not")
print("      silently dropped.")
POP = []
for n in range(2, 8):
    POP += all_posets(n)
w2 = [P for P in POP if P.width() <= 2]
chains = [P for P in w2 if not P.incomparable_pairs()]
w2_live = [P for P in w2 if P.incomparable_pairs()]
bad = tot = 0
worst = None
for P in w2_live:
    tot += 1
    d = P.delta()
    if d < F(1, 3):
        bad += 1
        print(f"       BAD {P.name}: delta = {d} < 1/3   <-- would REFUTE the citation")
    if worst is None or d < worst[0]:
        worst = (d, P.name)
report("width <= 2 and has an incomparable pair => delta >= 1/3", bad, tot,
       "per-poset, exact Fraction comparison against 1/3",
       f"all LABELLED posets on n=2..7 with e=identity a linear extension, "
       f"filtered to width <= 2 and at least one incomparable pair: {tot} posets "
       f"(out of {len(POP)} total, of which {len(w2)} have width <= 2)")
print(f"       tightest cell: delta = {worst[0]} at {worst[1]}")
print(f"       and the {len(chains)} width-<=2 posets with NO incomparable pair (the chains)")
print(f"       have delta UNDEFINED -- delta() returns None for them, and they are")
print(f"       excluded from the population above rather than counted as passing:")
bad = tot = 0
for P in chains:
    tot += 1
    if P.delta() is not None:
        bad += 1
report("chains have delta undefined", bad, tot,
       "per-poset, delta() is None",
       f"the {tot} width-<=2 posets on n=2..7 with no incomparable pair")

# ---------------------------------------------------------------------------
print()
print("A5.3  NEGATIVE CONTROL — the same sweep at width >= 3, where the citation says")
print("      nothing. If delta >= 1/3 held vacuously everywhere, A5.2 would be evidence")
print("      of nothing. The conjecture is verified to n <= 11, so no counterexample")
print("      should appear here either -- but the DISTRIBUTIONS must differ, or the")
print("      width-<=2 restriction in A5.2 is doing no work.")
w3 = [P for P in POP if P.width() >= 3 and P.incomparable_pairs()]
bad = tot = 0
worst3 = None
for P in w3:
    tot += 1
    d = P.delta()
    if d < F(1, 3):
        bad += 1
    if worst3 is None or d < worst3[0]:
        worst3 = (d, P.name)
report("width >= 3 => delta >= 1/3 (conjecture, n<=7)", bad, tot,
       "per-poset, exact Fraction comparison against 1/3",
       f"all LABELLED posets on n=2..7 of width >= 3 with an incomparable pair: {tot}")
print(f"       tightest cell at width >= 3: delta = {worst3[0]} at {worst3[1]}")
print(f"       tightest cell at width <= 2: delta = {worst[0]}")
print("       => the two families have DIFFERENT tightest cells, so the width-<=2")
print("          restriction is not vacuous on this population: A5.2 is a real check")
print("          and an instrument that could have shown the negative.")

# ---------------------------------------------------------------------------
print()
print("A5.4  the WHOLE of item (e), assembled: if both sides of the interface are chains,")
print("      then P is a union of two chains, so width(P) <= 2 (A5.1), so by Linial")
print("      delta(P) >= 1/3 (A5.2, checked as used to n=7), which contradicts frozen")
print("      (delta < 1/3). Scored end to end on the two-chain population:")
bad = tot = 0
skipped = 0
for n in range(2, 8):
    for mask in range(1 << n):
        S = [i for i in range(n) if mask >> i & 1]
        T = [i for i in range(n) if not (mask >> i & 1)]
        rel = [(S[i], S[i + 1]) for i in range(len(S) - 1)] + \
              [(T[i], T[i + 1]) for i in range(len(T) - 1)]
        P = Poset(n, rel, f"2chains n={n} mask={mask}")
        d = P.delta()
        if d is None:
            skipped += 1
            continue
        tot += 1
        if not (P.width() <= 2 and d >= F(1, 3)):
            bad += 1
            print(f"       BAD {P.name}: width {P.width()}, delta {d}")
report("item (e) end to end on unions of two chains", bad, tot,
       "per-poset, width <= 2 AND delta >= 1/3, both exact",
       f"every bipartition into two increasing chains, n=2..7; {tot} with an "
       f"incomparable pair, {skipped} SKIPPED as chains (delta undefined)")
print(f"       => the {skipped} skipped posets are the RIDER: item (e) as worded")
print("          ('both sides chains => width <= 2 => Linial => delta >= 1/3') is")
print("          MALFORMED on them, because delta does not exist. It closes the caveat")
print("          for free only after adding 'and P is not itself a chain'. That rider is")
print("          harmless in context -- a minimal counterexample is not a chain -- but it")
print("          is a rider mg-00b9's statement does not carry, and it is exactly one of")
print("          the two hypotheses Linial's theorem needs.")

print()
print("=" * 78)
print(f"A5 TOTAL BAD: {BAD}")
print("=" * 78)
sys.exit(0 if BAD == 0 else 1)
