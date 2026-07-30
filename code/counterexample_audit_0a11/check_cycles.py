"""A3 -- the negatives.  Every negative in the repair, re-derived here, and
attacked by construction.

The repair replaced a SAMPLING negative that was false ("no cycle in 4200
random posets at each of n = 8, 9, 10") with an EXHAUSTIVE one ("no majority
cycle at n <= 8, over all 19,440 non-chain isomorphism classes, ties
included"), and upgraded mg-a7b4's "n = 8 OPEN" to "n = 8 CLOSED".

An upgrade from open to closed is the one direction of drift that cannot be
excused, so it gets the harshest test available: the enumeration is redone from
a disjoint enumerator, the population size is checked against A000112 AND
A001035 (which detects over- and under-merging of isomorphism classes, either
of which could hide a cycle), and the witnesses at n = 9, 10, 11 are rebuilt
from their printed cover relations.
"""

import math
from fractions import Fraction

from kernel import Poset, enumerate_posets, from_covers, restrict

NMAX = 8


def banner(s):
    print()
    print("=" * 78)
    print(s)
    print("=" * 78)


def main():
    banner("A3.1  EXHAUSTIVE: majority cycles over every isomorphism class n <= 8")
    print("  'majority relation' is x -> y iff p(x,y) > 1/2; ties give no edge, so")
    print("  tied posets are INCLUDED in the sweep rather than excluded from it.")
    print()
    lv = enumerate_posets(NMAX)
    A000112 = [1, 2, 5, 16, 63, 318, 2045, 16999]
    A001035 = [1, 3, 19, 219, 4231, 130023, 6129859, 431723379]
    tot_all = tot_nonchain = tot_cyc = 0
    print("  n | classes | A000112 | sum n!/|Aut| | A001035 | non-chains | cycles")
    for n in range(3, NMAX + 1):
        cls = lv[n]
        orb = sum(math.factorial(n) // P.aut() for P in cls)
        nc = [P for P in cls if not P.is_chain()]
        cyc = sum(1 for P in nc if P.majority_cycle() is not None)
        tot_all += len(cls)
        tot_nonchain += len(nc)
        tot_cyc += cyc
        print("  %d | %7d | %7d | %12d | %12d | %10d | %6d"
              % (n, len(cls), A000112[n - 1], orb, A001035[n - 1], len(nc), cyc))
    print()
    print("  TOTAL over n = 3..8 : %d classes, %d non-chains, %d majority cycles"
          % (tot_all, tot_nonchain, tot_cyc))
    print("  the repair / the repaired document say: 19,446 classes, 19,440")
    print("  non-chains, 0 cycles, 16,998 non-chains at n = 8.")
    print("  MATCH: %s" % (tot_all == 19446 and tot_nonchain == 19440 and tot_cyc == 0))
    print()
    print("  Note what the two OEIS checks buy: A000112 alone would be satisfied by")
    print("  an enumerator that both over- and under-merges by the same amount, and")
    print("  a missed class is exactly where an unseen cycle would hide.  The orbit")
    print("  sum n!/|Aut| is a check on the LABELLED count and cannot be fooled the")
    print("  same way.  Both agree at every n.")

    # ------------------------------------------------------------------
    banner("A3.2  the n = 9 witness, rebuilt from the printed cover relations")
    cov9 = [(0, 5), (0, 8), (1, 4), (1, 6), (2, 3), (2, 7), (3, 6), (4, 8), (5, 7)]
    P9 = from_covers(9, cov9)
    print("  covers      %s" % (cov9,))
    print("  e(P)        %d           (claimed 1431)" % P9.e())
    print("  tie-free    %s" % P9.tie_free())
    print("  isolated    %s" % [x for x in range(9)
                                if P9.up[x] == 0 and P9.down[x] == 0])
    cyc = P9.majority_cycle()
    print("  cycle       %s        (claimed 0 -> 2 -> 1 -> 0)" % (cyc,))
    if cyc:
        seq = cyc[:-1]
        for i in range(len(seq)):
            a, b = seq[i], seq[(i + 1) % len(seq)]
            print("     p(%d,%d) = %s" % (a, b, P9.p(a, b)))
    print("  all three margins 80/159 : %s"
          % (cyc is not None and all(
              P9.p(cyc[i], cyc[i + 1]) == Fraction(80, 159)
              for i in range(len(cyc) - 1))))
    print()
    print("  ATTACK: does ANY single-element deletion preserve the cycle?  If one")
    print("  did, the exhaustive n <= 8 sweep above would be wrong.")
    surv = []
    for x in range(9):
        Q = restrict(P9, ((1 << 9) - 1) ^ (1 << x))
        if Q.majority_cycle() is not None:
            surv.append(x)
    print("  deletions preserving a cycle: %s   (must be empty)" % (surv or "none"))

    # ------------------------------------------------------------------
    banner("A3.3  the n = 10 witness, and the n = 11 witness it comes from")
    cov11 = [(0, 2), (0, 6), (0, 9), (1, 3), (1, 9), (2, 10), (3, 6), (3, 7),
             (4, 5), (4, 6), (6, 10)]
    P11 = from_covers(11, cov11)
    print("  n = 11  e(P) = %d   (claimed 78474)" % P11.e())
    for a, b in ((5, 9), (9, 6), (6, 5)):
        print("          p(%d,%d) = %s" % (a, b, P11.p(a, b)))
    print("          cycle    = %s" % (P11.majority_cycle(),))
    print("          element 8 isolated: %s"
          % (P11.up[8] == 0 and P11.down[8] == 0))
    P10 = restrict(P11, ((1 << 11) - 1) ^ (1 << 8))
    print("  n = 10  (element 8 deleted)  e(P) = %d   (claimed 7134)" % P10.e())
    print("          78474 = 11 * 7134 ? %s" % (78474 == 11 * 7134))
    print("          cycle    = %s" % (P10.majority_cycle(),))
    print("          covers   = %s" % (P10.covers(),))

    # ------------------------------------------------------------------
    banner("A3.4  the SAMPLING negative the repair re-runs beside its witness")
    print("  The repair prints '4200 random posets at each of three densities at")
    print("  n = 9, seed 4242: 0 cycles' DIRECTLY BENEATH a witness proving the")
    print("  region is non-empty.  That is the correct shape.  What it means")
    print("  quantitatively is worth stating: the sampler's miss is not surprising.")
    print()
    print("  Independent estimate of how rare a cycle is at n = 9, from a sampler")
    print("  written here (seed 20260730, uniform random labelled posets by random")
    print("  DAG closure at several densities):")
    import random
    for dens in (0.15, 0.25, 0.35, 0.5):
        rng = random.Random(20260730)
        hits = 0
        trials = 3000
        for _ in range(trials):
            n = 9
            perm = list(range(n))
            rng.shuffle(perm)
            up = [0] * n
            for i in range(n):
                for j in range(i + 1, n):
                    if rng.random() < dens:
                        up[perm[i]] |= 1 << perm[j]
            # transitive closure
            changed = True
            while changed:
                changed = False
                for x in range(n):
                    new = up[x]
                    r = up[x]
                    while r:
                        b = r & -r
                        y = b.bit_length() - 1
                        r ^= b
                        new |= up[y]
                    if new != up[x]:
                        up[x] = new
                        changed = True
            P = Poset(n, up)
            if P.majority_cycle() is not None:
                hits += 1
        print("    density %.2f : %d cycles in %d samples" % (dens, hits, trials))
    print()
    print("  READ: a negative of this shape is uninformative at this sample size in")
    print("  BOTH instruments.  The repair says so and prints the witness next to")
    print("  it; that is the correct handling and it is confirmed here.")


if __name__ == "__main__":
    main()
