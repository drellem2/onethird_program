"""Does the class on which the lazy AT walk IS a Brown walk stay inside
|L(P)| <= 4, or is it an infinite family?

§9.4 reports the question "undecided ... exactly where |L(P)| <= 4".  The exact
LP in audit_brown.py shows every such case is decided, and decided POSITIVELY.
This file asks the follow-up the deliverable's population cannot see: take
V_k = the ordinal sum of k two-element antichains (n = 2k), whose AT graph is
the hypercube Q_k and whose |L(P)| = 2^k.  Is the lazy AT walk a Brown walk
there?
"""

import sys
from fractions import Fraction

from audit_core import P0, linexts, at_graph
from audit_brown import faces_as_partitions, prod, decide_brown, unreachable_edge_test


def ordinal_sum_of_antichains(k):
    """V_k: elements 0..2k-1; pair i is {2i, 2i+1}, incomparable, and every
    element of pair i is below every element of pair j for i < j."""
    n = 2 * k
    lt = set()
    for i in range(k):
        for j in range(i + 1, k):
            for a in (2 * i, 2 * i + 1):
                for b in (2 * j, 2 * j + 1):
                    lt.add((a, b))
    return P0(n, lt)


def main():
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    print("=" * 78)
    print("AUDIT §9.4 follow-up: is the positive class bounded by |L(P)| <= 4?")
    print("=" * 78)
    print("V_k = ordinal sum of k two-element antichains;  n = 2k,  |L| = 2^k,")
    print("AT graph = the hypercube Q_k.")
    print()
    for k in range(1, kmax + 1):
        P = ordinal_sum_of_antichains(k)
        les, adj = at_graph(P)
        t = unreachable_edge_test(P)
        v, wit = decide_brown(P)
        print("  k=%d  n=%2d  |L(P)|=%3d  AT degree=%d   §9.4 test says: %-24s"
              "  EXACT ANSWER: %s"
              % (k, P.n, len(les), len(adj[0]) if adj else 0, t, v))
        if wit is not None and k <= 3:
            print("        witness has %d faces with positive weight; weights: %s"
                  % (len(wit), sorted({str(w) for _, w in wit})))


if __name__ == "__main__":
    main()
