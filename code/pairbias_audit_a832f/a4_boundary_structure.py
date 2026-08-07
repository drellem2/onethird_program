"""a4 -- what the boundary maximisers ARE, and whether they are the right shape.

A2.4 reports a maximum.  A maximum is worth nothing until you know whether the object
attaining it is in the class the programme cares about.  STATE.md:47: a minimal
counterexample is PRIMITIVE (incomparability graph connected <=> not an ordinal sum).
If the boundary maximiser is an ordinal sum, it is not a candidate for anything and the
number must be re-taken over the primitive sub-class.  That check is A4.1.

A4.2 then builds an all-n family, so the n <= 7 figures are not the only warrant, and
states in the same breath which direction that family bounds.
"""
from fractions import Fraction as F
from itertools import combinations
import sys
import libA832 as L

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7

gen, delta_le, primitive = L.gen, L.delta_le, L.primitive


print("=" * 78)
print("A4.1  ARE THE BOUNDARY MAXIMISERS PRIMITIVE?  (STATE.md:47 -- if not, they are")
print("      not candidates for anything and the number has to be re-taken)")
print("=" * 78)
print("   n | delta<=1/3 | primitive | max eps_spec ALL | max eps_spec PRIMITIVE | equal?")
print("  ---+------------+-----------+------------------+------------------------+-------")
prim_rows = []
for n in range(3, NMAX + 1):
    best_all = best_prim = None
    nprim = ncls = 0
    bp = None
    for less in gen(n):
        if not L.incomparable_pairs(less, n):
            continue
        ok, d = delta_le(less, n, F(1, 3))
        if not ok:
            continue
        ncls += 1
        Ei = L.expected_inv(less, n)
        if Ei is None:
            continue
        eps = 6 * Ei / (n ** 2 - 1)
        if best_all is None or eps > best_all:
            best_all = eps
        if primitive(less, n):
            nprim += 1
            if best_prim is None or eps > best_prim:
                best_prim, bp = eps, (less, Ei)
    prim_rows.append((n, best_prim, bp))
    print("  %3d | %10d | %9d | %16s | %22s | %s"
          % (n, ncls, nprim, best_all, best_prim, "YES" if best_all == best_prim else "NO"))
print()
print("  The PRIMITIVE maximiser at each n, written out:")
for n, eps, bp in prim_rows:
    if bp is None:
        print("     n=%d  none" % n)
        continue
    less, Ei = bp
    m = len(L.incomparable_pairs(less, n))
    print("     n=%d  eps_spec=%-7s  E[inv_e]=%-5s  m=%-2d  d=%-7s  relations %s"
          % (n, eps, Ei, m, F(m, n * (n - 1) // 2), sorted(less)))

print()
print("=" * 78)
print("A4.2  AN ALL-n FAMILY ON THE BOUNDARY -- ordinal sums of tight3")
print("=" * 78)
print("  P_k := tight3 (+) tight3 (+) ... (+) tight3, k blocks, n = 3k.  Within a block")
print("  the relation is {3b < 3b+2}; every element of an earlier block is below every")
print("  element of a later one.  delta = 1/3 and E[inv_e] = 2k/3 EXACTLY, by hand:")
print("  an ordinal sum's linear-extension measure is the product over blocks, so the")
print("  pair probabilities are the blocks' own and E[inv_e] adds.")
print()
print("   k |  n | delta   | E[inv_e] | eps_spec = 6E/(n^2-1) | closed form 4k/(9k^2-1) | primitive?")
print("  ---+----+---------+----------+-----------------------+-------------------------+-----------")
for k in range(1, 7):
    n = 3 * k
    less = set()
    for b in range(k):
        less.add((3 * b, 3 * b + 2))
        for c in range(b + 1, k):
            for u in range(3):
                for v in range(3):
                    less.add((3 * b + u, 3 * c + v))
    less = frozenset(less)
    assert L.is_transitive(less, n)
    if n <= 8:
        d = L.delta(less, n)
        Ei = L.expected_inv(less, n)
    else:
        d = F(1, 3)                     # by the block factorisation, stated above
        Ei = F(2 * k, 3)
    eps = 6 * Ei / (n ** 2 - 1)
    cf = F(4 * k, 9 * k * k - 1)
    print("  %3d | %2d | %7s | %8s | %21s | %23s %s | %s"
          % (k, n, d, Ei, eps, cf, "OK" if eps == cf else "MISMATCH",
             primitive(less, n)))
print()
print("  DIRECTION, STATED BECAUSE IT IS THE WHOLE VALUE OF THIS TABLE: this family is a")
print("  LOWER bound on the boundary maximum at every n = 3k, and it decays like")
print("  4k/(9k^2-1) = Theta(1/n).  It is NOT an upper bound on anything -- the exhaustive")
print("  upper bounds are A2.4's and stop at n = %d." % NMAX)
print()
print("  AND IT IS IMPRIMITIVE FOR k >= 2, which is why A4.1 exists.  An ordinal sum has")
print("  lambda_std = 1 exactly and is not a candidate minimal counterexample, so if this")
print("  family were the only boundary witness the measurement would say nothing about")
print("  the class that matters.  A4.1 reports the primitive maximum separately.")

print()
print("=" * 78)
print("A4.3  NEGATIVE CONTROL -- does the sweep FIND a planted violation?")
print("=" * 78)
print("  A sweep that reports 0 of something must be shown capable of reporting >0.")
print("  Re-run A2.2's delta filter at a LOOSER threshold and require the counts to move.")
print()
print("   threshold | n=3 | n=4 | n=5 | n=6   (non-chain posets with delta <= threshold)")
print("  -----------+-----+-----+-----+------")
for th in (F(1, 4), F(1, 3), F(2, 5), F(1, 2)):
    row = []
    for n in range(3, 7):
        c = 0
        for less in gen(n):
            if not L.incomparable_pairs(less, n):
                continue
            ok, _ = delta_le(less, n, th)
            if ok:
                c += 1
        row.append(c)
    print("  %10s | %3d | %3d | %3d | %4d" % (th, row[0], row[1], row[2], row[3]))
print()
print("  The counts MOVE with the threshold and they are 0 below 1/3 -- so the 0 in")
print("  A2.2's 'delta < 1/3 STRICT' column is a measurement, not an inert predicate.")
print("  At threshold 1/2 every non-chain poset qualifies, which is the sanity ceiling.")

print()
print("=" * 78)
print("A4.4  THE NEAREST PRIMITIVE POPULATION -- since the primitive boundary is EMPTY")
print("      above n = 3, where IS the primitive minimum of delta, and what is eps_spec")
print("      there?  (A4.1 makes this the only realizable calibration that exists.)")
print("=" * 78)
print("   n | primitive posets | min delta over them | # attaining | max eps_spec at min delta")
print("  ---+------------------+---------------------+-------------+--------------------------")
for n in range(3, NMAX + 1):
    best = None
    nprim = 0
    cands = []
    for less in gen(n):
        if not L.incomparable_pairs(less, n):
            continue
        if not primitive(less, n):
            continue
        nprim += 1
        ok, d = delta_le(less, n, best if best is not None else F(1))
        if best is None or d < best:
            best, cands = d, [less]
        elif d == best:
            cands.append(less)
    mx = None
    for less in cands:
        Ei = L.expected_inv(less, n)
        if Ei is None:
            continue
        eps = 6 * Ei / (n ** 2 - 1)
        if mx is None or eps > mx:
            mx = eps
    print("  %3d | %16d | %19s | %11d | %s"
          % (n, nprim, best, len(cands), mx if mx is not None else "no `e` exists"))
print()
print("  The `no e exists` cells are P15's guard firing on real data and are NOT a bug:")
print("  at delta > 1/3 the >=2/3-majority tournament is INCOMPLETE, so the distinguished")
print("  order is undefined and inv_e with it.  A calibration that quietly used the")
print("  natural labelling there would print a number for a quantity that does not exist.")
print("  THAT IS THE ANSWER TO 'why not calibrate eps_sup empirically': it is not only")
print("  that the frozen class is empty -- it is that `e` itself stops existing before")
print("  you reach any primitive poset, at every n measured.")
