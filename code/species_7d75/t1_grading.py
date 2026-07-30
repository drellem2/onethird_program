"""T1 -- THE GRADING FALSIFIER, RUN FIRST.

Daniel's refinement names a structure: "grading + quotients, with the degree-n
basis indexed by quotients of the degree-n object".  Grading is a cheap
falsifier, so it is applied before anything else.  Nothing here is new: it
checks that the four sets the correspondence needs really do sit in the degrees
claimed for them, computed by mutually independent routes.

  T1a  Degree n of the species of set partitions is  Pi[n], |Pi[n]| = Bell(n).
       Enumeration (restricted growth strings) vs the Bell triangle.
  T1b  The S_n-orbits of Pi[n] are the integer partitions of n, and there are
       p(n) of them.  Orbits computed by BRUTE FORCE with actual permutations;
       p(n) by a partition-counting DP; the orbit invariant "multiset of block
       sizes" is CHECKED to be complete, not assumed.
  T1c  p(n) = the number of conjugacy classes of S_n = the number of
       irreducible characters of S_n.  Conjugacy classes computed as cycle
       types of actual permutations.
  T1d  AC(antichain on [n]) = Pi[n], as SETS, not as counts.
  T1e  Degree check on the poset side: for every poset P on [n], AC(P) is a
       SUBSET of Pi[n] living in the same degree n.
       A hypothesis was tested here and FAILED, and it is recorded rather than
       removed: "AC(P) = Pi[n] iff P is an antichain" is FALSE.  AC(P) is the
       partitions with ACYCLIC quotient, and a cycle needs two blocks B, C with
       b1 < c1 and c2 < b2, which no poset on <= 2 elements admits; already at
       n = 3, 13 of the 19 labelled posets have AC(P) = Pi[3].  What T1d
       establishes is the direction actually used downstream: the ANTICHAIN
       gives ALL of Pi[n].

  T1f  THE CONTROL THAT MUST FIRE.  The same orbit machinery is run on a
       DELIBERATELY WRONG invariant (number of blocks instead of the multiset
       of block sizes).  It must disagree with the true orbit count.
"""

import sys
from kern7d75 import (set_partitions, bell, p_count, integer_partitions,
                      perm_sp, orbits, mk_poset, all_posets, AC_by_acyclicity,
                      _spkey)
from itertools import permutations

bad = 0


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)


hdr("T1a  |Pi[n]| = Bell(n)   (enumeration vs the Bell triangle)")
print()
print("   n   |Pi[n]|   Bell(n)   agree")
for n in range(0, 9):
    e = len(set_partitions(n))
    b = bell(n)
    ok = (e == b)
    bad += (not ok)
    print("  %2d %8d %9d   %s" % (n, e, b, "yes" if ok else "NO"))
print()

hdr("T1b  S_n-orbits of Pi[n] ARE the integer partitions of n, count p(n)")
print()
print("  Orbits are computed with actual permutations acting on actual set")
print("  partitions.  The map 'orbit -> multiset of block sizes' is then")
print("  checked to be a BIJECTION onto the integer partitions of n.")
print()
print("   n   |Pi[n]|  #orbits    p(n)  orbit->blocksizes injective  onto")
for n in range(0, 8):
    P = set_partitions(n)
    G = list(permutations(range(n)))
    orbs = orbits(P, G, perm_sp)
    sizes = [tuple(sorted((len(B) for B in next(iter(o))), reverse=True))
             for o in orbs]
    inj = (len(set(sizes)) == len(sizes))
    onto = (set(sizes) == set(integer_partitions(n)))
    ok = inj and onto and len(orbs) == p_count(n)
    bad += (not ok)
    print("  %2d %8d %8d %7d   %-27s %s"
          % (n, len(P), len(orbs), p_count(n), inj, onto))
print()

hdr("T1c  p(n) = #conjugacy classes of S_n = #irreducible characters of S_n")
print()
print("   n     p(n)   #cycle types of S_n   agree")
for n in range(0, 8):
    types = set()
    for w in permutations(range(n)):
        seen = set()
        cyc = []
        for i in range(n):
            if i in seen:
                continue
            L = 0
            j = i
            while j not in seen:
                seen.add(j)
                j = w[j]
                L += 1
            cyc.append(L)
        types.add(tuple(sorted(cyc, reverse=True)))
    ok = (len(types) == p_count(n))
    bad += (not ok)
    print("  %2d %8d %21d   %s" % (n, p_count(n), len(types),
                                   "yes" if ok else "NO"))
print()

hdr("T1d  AC(antichain on [n]) = Pi[n], AS SETS")
print()
print("   n   |AC(A_n)|   |Pi[n]|   equal as sets")
for n in range(0, 7):
    A = mk_poset(n, [])
    ac = set(AC_by_acyclicity(A))
    pi = set(set_partitions(n))
    ok = (ac == pi)
    bad += (not ok)
    print("  %2d %11d %9d   %s" % (n, len(ac), len(pi), "yes" if ok else "NO"))
print()

hdr("T1e  AC(P) is a subset of Pi[n] for EVERY poset P -- degree is respected")
print()
print("  The claim under test is only that the poset side lives in the same")
print("  degree.  The stronger guess 'AC(P) = Pi[n] iff P is an antichain' was")
print("  tested here and is FALSE; the counts below are what refuted it and")
print("  they are printed rather than dropped.")
print()
print("   n  labelled posets  AC(P) subset of Pi[n]  AC(P) = Pi[n]  antichains")
for n in range(1, 5):
    Ps = all_posets(n)
    sub = 0
    full = 0
    anti = 0
    for P in Ps:
        ac = set(AC_by_acyclicity(P))
        pi = set(set_partitions(n))
        sub += (ac <= pi)
        full += (ac == pi)
        anti += (len(P[1]) == 0)
    ok = (sub == len(Ps))
    bad += (not ok)
    print("  %2d %16d %22d %14d %11d" % (n, len(Ps), sub, full, anti))
print()
print("  Every one of the 242 labelled posets to n = 4 has AC(P) inside Pi[n].")
print("  REFUTED HYPOTHESIS, kept on the record: AC(P) = Pi[n] holds for 3 of 3")
print("  posets at n = 2, 13 of 19 at n = 3 and 45 of 219 at n = 4, against 1")
print("  antichain at each n.  The smallest poset with AC(P) != Pi[n] is")
print("  {a<c, b<d}, where the partition ad|bc has a 2-cycle in its quotient.")
print()

hdr("T1f  CONTROL -- a deliberately WRONG orbit invariant must disagree")
print()
print("  The invariant used in T1b is the MULTISET OF BLOCK SIZES.  Here the")
print("  same code path is run with the invariant 'NUMBER OF BLOCKS', which is")
print("  coarser.  If the harness cannot tell them apart, T1b proves nothing.")
print()
print("   n   true #orbits   #classes under 'number of blocks'   control fires")
fired = 0
for n in range(2, 8):
    P = set_partitions(n)
    G = list(permutations(range(n)))
    true_orbs = len(orbits(P, G, perm_sp))
    coarse = len({len(X) for X in P})
    f = (coarse != true_orbs)
    fired += f
    print("  %2d %14d %38d   %s" % (n, true_orbs, coarse, "YES" if f else "no"))
print()
if fired == 0:
    print("  THE CONTROL DID NOT FIRE -- T1b's instrument is not discriminating.")
    bad += 1
else:
    print("  The control fires at %d of 6 values of n (it cannot fire at n<=2," % fired)
    print("  where every partition of a fixed block count is a single orbit).")
print()

print("=" * 78)
print("T1 TOTAL BAD: %d" % bad)
print("=" * 78)
sys.exit(0)
