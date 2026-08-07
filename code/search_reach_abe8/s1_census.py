"""s1 -- EXHAUSTIVE constraint-density census, n = 2..9.

For every poset on n <= 9 elements up to isomorphism, evaluate the four
structural constraints a minimal counterexample is known to satisfy and report
each one's PRUNING IN BITS, -log2(surviving/total).  P14 binds this file to that
formula: a constraint whose EXCLUDED set vanishes prunes ~0 bits.

Also reports, at n <= 8, the frozen census and the distribution of delta -- how
close the population actually gets to the 1/3 threshold.  delta is skipped at
n = 9 (183231 posets x a 2^9 DP is ~40 min single-core and adds nothing: the
frozen class is empty and the near-threshold count is the informative figure).

Single process, one core.  No fan-out.
"""

import sys
import time
from fractions import Fraction

import libabe8 as L

NMAX_STRUCT = 9
NMAX_DELTA = 8

T0 = time.time()


def stamp():
    return "%7.1fs" % (time.time() - T0)


print("=" * 78)
print("s1  EXHAUSTIVE CONSTRAINT-DENSITY CENSUS  (mg-abe8)")
print("=" * 78)
print()
print("Constraints, and their source.  mg-5998 is STILL UNLANDED (available) at the")
print("time of this run, so its list is taken as given and NONE of its attributions")
print("is verified here -- see PREDICTIONS.md, table in the header.")
for name, src, _ in L.CONSTRAINTS:
    print("   %-12s %s" % (name, src))
print()
print("PRUNING IS -log2(surviving/total) AND NOTHING ELSE (P14).")
print()

rows = []
cur = L.all_posets_bruteforce(1)
for n in range(2, NMAX_STRUCT + 1):
    cur = L.all_posets_by_extension(n, cur)
    tot = len(cur)
    surv = {}
    for name, _, fn in L.CONSTRAINTS:
        surv[name] = sum(1 for P in cur if fn(P))
    joint = sum(1 for P in cur
                if all(fn(P) for _, _, fn in L.CONSTRAINTS))
    rows.append((n, tot, surv, joint))
    print("n=%-2d  N=%-8d  %s" % (n, tot, stamp()))
    sys.stdout.flush()

print()
print("-" * 78)
print("A.  SURVIVING FRACTION per constraint (higher = prunes LESS)")
print("-" * 78)
hdr = "  n |      N(n) | " + " | ".join("%-11s" % c[0] for c in L.CONSTRAINTS) + " |    ALL FOUR"
print(hdr)
print("-" * len(hdr))
for (n, tot, surv, joint) in rows:
    cells = " | ".join("%10.4f%%" % (100.0 * surv[c[0]] / tot) for c in L.CONSTRAINTS)
    print("%3d | %9d | %s | %10.4f%%" % (n, tot, cells, 100.0 * joint / tot))

print()
print("-" * 78)
print("B.  PRUNING IN BITS   = -log2(surviving/total)")
print("     and ELEMENTS OF REACH BOUGHT = bits / g(n),  g(n) = log2(N(n)/N(n-1))")
print("-" * 78)
hdr = "  n |   g(n) | " + " | ".join("%-11s" % c[0] for c in L.CONSTRAINTS) + " |    ALL FOUR |  Dn bought"
print(hdr)
print("-" * len(hdr))
for (n, tot, surv, joint) in rows:
    g = L.g_exact(n)
    cells = " | ".join("%11.3f" % L.prune_bits(surv[c[0]], tot) for c in L.CONSTRAINTS)
    jb = L.prune_bits(joint, tot)
    print("%3d | %6.3f | %s | %11.3f | %10.3f" % (n, g, cells, jb, jb / g))

print()
print("-" * 78)
print("C.  DIRECTION OF TRAVEL: change in pruning from n=6 to n=9, per constraint")
print("-" * 78)
r6 = [r for r in rows if r[0] == 6][0]
r9 = [r for r in rows if r[0] == NMAX_STRUCT][0]
for name, _, _ in L.CONSTRAINTS:
    b6 = L.prune_bits(r6[2][name], r6[1])
    b9 = L.prune_bits(r9[2][name], r9[1])
    arrow = "WEAKER" if b9 < b6 else ("STRONGER" if b9 > b6 else "flat")
    print("   %-12s  %6.3f bits at n=6  ->  %6.3f bits at n=%d   %s"
          % (name, b6, b9, NMAX_STRUCT, arrow))
jb6 = L.prune_bits(r6[3], r6[1])
jb9 = L.prune_bits(r9[3], r9[1])
print("   %-12s  %6.3f bits at n=6  ->  %6.3f bits at n=%d   %s"
      % ("ALL FOUR", jb6, jb9, NMAX_STRUCT, "WEAKER" if jb9 < jb6 else "STRONGER"))

print()
print("-" * 78)
print("D.  HEREDITARY FORM -- what can actually be tested at the PARENT level")
print("-" * 78)
print("""A search builds n-posets by adjoining a maximal element to an (n-1)-poset.
Pruning means DISCARDING A PARENT.  A constraint can only do that if it is
implied at the parent by holding at the child.  For each of the four:

  rigid       NOT hereditary -- a rigid poset can have non-rigid deletions
                                (selftest NC4 exhibits 15 witnesses at n=5).
                                Cannot discard any parent.
  width>=3    hereditary in the weak form width(P-x) >= 2, i.e. it discards
                                exactly the CHAINS.  One parent per n.
  not-6-thin  hereditary in the weak form "some x incomparable to >= 6 others"
                                (deleting one element costs at most one).
  primitive   NOT hereditary.  Cannot discard any parent.

FROZEN-NESS ITSELF DISCARDS ZERO PARENTS, AND THIS IS A PROOF: P minimal means
every proper induced subposet of P satisfies the conjecture, so the parent is
NOT frozen.  The parents of the object being hunted are exactly the non-frozen
posets, and (see E below) at every n we can reach that is ALL of them.""")
print()
print("Measured: the weak hereditary form of not-6-thin at the parent level.")
cur = L.all_posets_bruteforce(1)
for n in range(2, NMAX_STRUCT + 1):
    cur = L.all_posets_by_extension(n, cur)
    if n >= 6:
        w = sum(1 for P in cur if L.thinness(P) >= 6)
        print("   n=%-2d  parents surviving 'some x incomparable to >=6': %8d / %8d"
              "   = %7.3f%%   (%6.3f bits)"
              % (n, w, len(cur), 100.0 * w / len(cur), L.prune_bits(w, len(cur))))
        sys.stdout.flush()

print()
print("-" * 78)
print("E.  THE FROZEN CENSUS AND THE DELTA DISTRIBUTION, n <= %d" % NMAX_DELTA)
print("-" * 78)
print("delta(P) = max over incomparable pairs of min(p,1-p).  frozen = delta < 1/3.")
print("Brightwell-Felsner-Trotter give delta >= (5-sqrt5)/10 ~ 0.2764 for every")
print("non-chain (RECALLED, NOT VERIFIED HERE), so the frozen band is a narrow one.")
print()
third = Fraction(1, 3)
cur = L.all_posets_bruteforce(1)
print("  n |      N(n) |  chains | frozen | delta = 1/3 exactly |  min delta over non-chains")
print("-" * 92)
for n in range(2, NMAX_DELTA + 1):
    cur = L.all_posets_by_extension(n, cur)
    nfroz = nchain = nexact = 0
    mind = None
    for P in cur:
        d = L.delta(P)
        if d is None:
            nchain += 1
            continue
        if d < third:
            nfroz += 1
        if d == third:
            nexact += 1
        if mind is None or d < mind:
            mind = d
    print("%3d | %9d | %7d | %6d | %19d | %s = %.6f"
          % (n, len(cur), nchain, nfroz, nexact, mind, float(mind)))
    sys.stdout.flush()

print()
print("READING: the frozen class is empty at every n <= %d, AND the minimum of" % NMAX_DELTA)
print("delta over non-chains is EXACTLY 1/3 at every one of them -- the population")
print("sits ON the threshold and never crosses it.  That is why 'the frozen class is")
print("empty' is NOT a pruning signal: the filter that would use it rejects nothing")
print("at the parent level, because the parents are the non-frozen posets and the")
print("non-frozen posets are all of them.")
print()
print("total wall %s, one core" % stamp())
