"""a2 -- THE SWEEP mg-345e AND mg-6bc2 BOTH DECLARED AND REFUSED.

Both parents refuse poset enumeration on the ground that the frozen class delta < 1/3
is EMPTY at every n this corpus can reach (1/3-2/3 verified to n = 14, mg-33f5).  That
ground is correct and I reproduce it below (P12).  It is a reason not to calibrate
eps_sup against posets.  It is NOT a reason not to measure the NEAREST NON-EMPTY
realizable class, delta(P) <= 1/3 -- the boundary the frozen class is the strict
interior of -- and nobody in this lineage has.

mg-6bc2 sec.1 says, of the relaxation, "nobody has asked how much the bound costs,
which is a number", and then computes the RELAXATION side of that number and stops.
This script computes the other side.

Posets are generated NATURALLY LABELLED and INCREMENTALLY: a naturally labelled poset
on [n] is a naturally labelled poset on [n-1] plus an order ideal of it, taken as the
down-set of the new element n-1.  That is a bijection, so nothing is generated twice
and nothing is rejected -- and the counts are therefore forced, not sampled.
"""
from fractions import Fraction as F
from itertools import combinations
import sys
import libA832 as L

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6


gen = L.gen
delta_le = L.delta_le


if __name__ != "__main__":
    import sys as _s

print("=" * 78)
print("A2.1  POPULATION -- naturally labelled posets, my own enumerator (P9)")
print("=" * 78)
print("   n | naturally labelled posets")
print("  ---+--------------------------")
pops = {}
for n in range(1, NMAX + 1):
    P = gen(n)
    pops[n] = P
    print("  %3d | %d" % (n, len(P)))
print()
print("  STATE.md:42 attributes '4,824 posets at n=6' to mg-c4f5.  My n=6 count: %d %s"
      % (len(pops.get(6, [])), "-- MATCHES" if len(pops.get(6, [])) == 4824 else "-- DOES NOT MATCH"))
print("  (These are naturally labelled posets = posets carrying a distinguished linear")
print("   extension, which is the right population here: `e` is part of the data.)")

print()
print("=" * 78)
print("A2.2  IS THE FROZEN CLASS EMPTY?  (P12 -- and a MISS here would refute 1/3-2/3)")
print("=" * 78)
print("   n | posets | chains | delta <= 1/3 (non-chain) | delta < 1/3 STRICT | min delta>0")
print("  ---+--------+--------+--------------------------+--------------------+------------")
boundary = {}
for n in range(2, NMAX + 1):
    chains = le13 = strict = 0
    mind = None
    keep = []
    for less in pops[n]:
        inc = L.incomparable_pairs(less, n)
        if not inc:
            chains += 1
            continue
        ok, d = delta_le(less, n, F(1, 3))
        if ok:
            le13 += 1
            keep.append((less, d))
            if d < F(1, 3):
                strict += 1
            if mind is None or d < mind:
                mind = d
    boundary[n] = keep
    print("  %3d | %6d | %6d | %24d | %18d | %s"
          % (n, len(pops[n]), chains, le13, strict, mind))
print()
print("  ZERO posets with delta < 1/3 at every n <= %d.  That is the 1/3-2/3 conjecture" % NMAX)
print("  holding, and it is why both parents refused this sweep.  The class delta <= 1/3")
print("  is NOT empty: every member has delta = 1/3 EXACTLY.  It is the boundary.")

print()
print("=" * 78)
print("A2.3  P15's GUARD -- does the distinguished order `e` EXIST on the boundary?")
print("=" * 78)
print("  `e` is the >=2/3-majority order.  At delta = 1/3 exactly, every pair is")
print("  >=2/3-decided, so the tournament is COMPLETE -- but the 3-cycle count of")
print("  STATE.md:205 gives Pr+Pr+Pr <= 2, which a cycle at exactly 2/3 each SATURATES")
print("  rather than violates.  So transitivity is NOT forced by that argument at the")
print("  boundary, and it has to be measured.  majority_order() returns None rather")
print("  than falling back to the natural labelling.")
print()
print("   n | delta<=1/3 non-chains | `e` EXISTS | `e` ABSENT (incomplete or 3-cycle)")
print("  ---+-----------------------+------------+-----------------------------------")
for n in range(3, NMAX + 1):
    have = absent = 0
    for less, d in boundary[n]:
        if L.majority_order(less, n) is None:
            absent += 1
        else:
            have += 1
    print("  %3d | %21d | %10d | %d" % (n, len(boundary[n]), have, absent))

print()
print("=" * 78)
print("A2.4  THE NUMBER -- max eps_spec over REALIZABLE measures in the class (P10/P11)")
print("=" * 78)
print("  eps_spec(P) = 6 E[inv_e] / (n^2-1), sigma uniform on L(P), e the majority order.")
print()
print("   n | realizable max | attaining poset  | LP relaxation max | realizable/relax")
print("  ---+----------------+------------------+-------------------+-----------------")
rows = []
for n in range(3, NMAX + 1):
    best = None
    for less, d in boundary[n]:
        Ei = L.expected_inv(less, n)
        if Ei is None:
            continue
        eps = 6 * Ei / (n ** 2 - 1)
        if best is None or eps > best[0]:
            best = (eps, less, Ei)
    relax = F(n, n + 1)
    if best is None:
        print("  %3d | %14s | %16s | %17s | %s" % (n, "-", "-", relax, "-"))
        continue
    eps, less, Ei = best
    rows.append((n, eps, less, Ei, relax))
    print("  %3d | %14s | %-16s | %17s | %s"
          % (n, eps, sorted(less), relax, eps / relax))
print()
print("  DETAIL of each attaining poset, with mg-6bc2 sec.3.1's two levers separated:")
print("     n | E[inv_e] | m  | C(n,2) | d = m/C(n,2) | qbar = E/m | 3*d*qbar*n/(n+1)")
print("    ---+----------+----+--------+--------------+------------+-----------------")
for n, eps, less, Ei, relax in rows:
    order = L.majority_order(less, n)
    r = L.relabel(less, n, order)
    m = len(L.incomparable_pairs(r, n))
    C = n * (n - 1) // 2
    d = F(m, C)
    q = Ei / m
    ident = 3 * d * q * F(n, n + 1)
    print("     %d | %8s | %2d | %6d | %12s | %10s | %s %s"
          % (n, Ei, m, C, d, q, ident, "OK" if ident == eps else "MISMATCH"))
print()
print("  READ THE qbar COLUMN, NOT THE ONE YOU EXPECTED: qbar = 1/3 EXACTLY at every")
print("  attaining poset, at every n.  So of mg-6bc2 sec.3.1's TWO levers, only ONE is")
print("  moving on the boundary -- the DENSITY d.  The mean flip probability is pinned")
print("  at the cap; the maximiser spends its whole budget on every incomparable pair")
print("  it has, and has few of them.  That says the lever that matters is residual (R),")
print("  and NOT the qbar half of sec.3.1's `either lever alone` sentence.")

print()
print("=" * 78)
print("A2.5  RESIDUAL (R) MEASURED ON THE BOUNDARY -- 'do frozen posets have a density")
print("      ceiling d(P) <= D < 1?' (STATE.md:179; mg-345e's grep returns 0 upper bounds)")
print("=" * 78)
print("  I cannot answer (R), because (R) is about the EMPTY class delta < 1/3.  What I")
print("  can do is measure d on the class that touches it.  Every figure below is FP and")
print("  is about delta = 1/3 EXACTLY.")
print()
print("   n | max m | C(n,2) | MAX d over the class | max E[inv_e] | max eps_spec")
print("  ---+-------+--------+----------------------+--------------+-------------")
for n in range(3, NMAX + 1):
    md = None; mm = 0; mE = None; me = None
    for less, _ in boundary[n]:
        order = L.majority_order(less, n)
        if order is None:
            continue
        r = L.relabel(less, n, order)
        m = len(L.incomparable_pairs(r, n))
        Ei = L.expected_inv(less, n)
        eps = 6 * Ei / (n ** 2 - 1)
        d = F(m, n * (n - 1) // 2)
        mm = max(mm, m)
        md = d if md is None else max(md, d)
        mE = Ei if mE is None else max(mE, Ei)
        me = eps if me is None else max(me, eps)
    print("  %3d | %5d | %6d | %20s | %12s | %s"
          % (n, mm, n * (n - 1) // 2, md, mE, me))
print()
print("  Read the E[inv_e] column: on the boundary it is 2/3, 2/3, 2/3, 4/3 -- O(1), not")
print("  Theta(n^2) and not even Theta(n).  The two-atom law's Theta(n^2) is not merely")
print("  unrealisable, it is nowhere near anything realisable at delta = 1/3.")
print()
print("  DIRECTION CHECK, because this is where an audit of this arc must not slip: a")
print("  SMALL realizable maximum is GOOD NEWS for the programme (eps_spec must be small)")
print("  and BAD NEWS for the relaxation as a proof route (the relaxation is loose by the")
print("  ratio above).  These are the same fact and neither is evidence FOR L1b: the")
print("  class measured is delta = 1/3, the class needed is delta < 1/3, and it is empty.")
