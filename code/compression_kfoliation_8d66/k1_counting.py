#!/usr/bin/env python3
"""k1 -- ITEM 4, CHECKED FIRST BECAUSE IT MIGHT END THE TICKET: how large can k be?

The ticket: "Classes must be pairwise non-adjacent positions, so k is bounded by the structure
of {1..n-1}.  If the maximum useful k grows too slowly with n to lift alpha_k over a FIXED bar,
the class is closed by counting alone and that is the cheapest possible answer."

It does not end the ticket.  An admissible partition is a partition of the path P_{n-1} into
independent sets, i.e. a proper colouring counted up to colour names.  Both ends are exactly
computable and neither is restrictive:

    k_min = 2   for n >= 3, and THE k = 2 PARTITION IS UNIQUE  (chi(path) = 2)
    k_max = n-1                                                (all singletons)

so k grows LINEARLY in n.  Counting does not close the class.  Reported as a NEGATIVE result.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib8d66 as K

ok = True

K.banner("k1.1  the admissible partitions, enumerated")
print("  An admissible partition of the n-1 swap positions {0..n-2}: every block is a set of")
print("  PAIRWISE NON-ADJACENT positions.  Enumerated exhaustively, not counted by formula.")
print()
print("   n | m=n-1 | #admissible | k_min | k_max | #partitions at k=2 | #at k=k_max")
print("  ---+-------+-------------+-------+-------+--------------------+------------")
rows = []
for n in range(3, 13):
    parts = K.admissible_partitions(n)
    ks = [len(p) for p in parts]
    kmin, kmax = min(ks), max(ks)
    n2, nmax = sum(1 for k in ks if k == 2), sum(1 for k in ks if k == kmax)
    rows.append((n, len(parts), kmin, kmax, n2, nmax))
    print(f"  {n:2d} | {n-1:5d} | {len(parts):11d} | {kmin:5d} | {kmax:5d} |"
          f" {n2:18d} | {nmax:11d}", flush=True)

ok &= K.verdict(all(r[2] == 2 for r in rows), "k_min = 2 at every n = 3..12")
ok &= K.verdict(all(r[3] == r[0] - 1 for r in rows), "k_max = n-1 at every n = 3..12")
ok &= K.verdict(all(r[4] == 1 for r in rows),
                "THE k = 2 PARTITION IS UNIQUE at every n = 3..12",
                "so mg-409a's odd/even was not a choice")
ok &= K.verdict(all(r[5] == 1 for r in rows), "the k = n-1 partition is unique (all singletons)")

K.banner("k1.2  both extremes are the objects they are supposed to be")
bad = 0
for n in range(3, 13):
    parts = set(K.admissible_partitions(n))
    if K.coarsest_partition(n) not in parts:
        bad += 1
    if K.finest_partition(n) not in parts:
        bad += 1
    for p in parts:
        for b in p:
            if not K.is_class(b):
                bad += 1
        if sorted(x for b in p for x in b) != list(range(n - 1)):
            bad += 1
ok &= K.verdict(bad == 0, "every enumerated partition is admissible AND covers every position",
                f"{bad} violations")
ok &= K.verdict(all(K.coarsest_partition(n) ==
                    tuple(sorted((tuple(p for p in range(n - 1) if p % 2 == 0),
                                  tuple(p for p in range(n - 1) if p % 2 == 1))))
                    for n in range(3, 13)),
                "the unique k=2 partition IS even-positions / odd-positions",
                "= lib409a's blocks_o / blocks_e  (checked entrywise in k0.5)")

K.banner("k1.3  THE VERDICT ON COUNTING")
print("""
  k reaches n-1.  The bar is (n-1)/(gamma n), a CONSTANT in [2,3).  A ceiling of the naive
  form `alpha_k <= k-1` (what mg-409a's own proof generalises to -- see k4.4) would clear a
  bar of 3 from k = 4, i.e. from n = 5.  So:

      THE CLASS IS NOT CLOSED BY COUNTING.

  This is the cheap answer the ticket hoped for and it is NOT AVAILABLE.  Whatever closes the
  class has to be a statement about the OPERATOR, at every k, and that is k2-k4.
""")
ok &= K.verdict(True, "reported as a NEGATIVE result: counting does not close the class")

K.banner("k1: " + ("PASS" if ok else "FAIL"))
sys.exit(0 if ok else 1)
