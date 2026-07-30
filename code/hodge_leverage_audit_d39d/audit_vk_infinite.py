"""mg-d39d, independent audit of mg-a806.

Target: the support for the MAJOR correction mg-a806 landed.

§0 claim 3:   "the positive class contains the INFINITE family V_k"
§9.4:         "So the positive class is UNBOUNDED in |L(P)|"
ledger B6:    "the INFINITE family V_k (|L(P)| = 2^k) is positive for every k
               TESTED"
ledger B6':   claim column "an infinite family (|L(P)| = 2^k, unbounded)";
              label column "PROVEN for the V_k half ... positivity verified by
              exact LP for k <= 4"
STATE.md:     "the infinite family V_k ... |L(P)| = 2^k unbounded ... is
               positive for every k tested"

The evidence cited everywhere is `out_brown_family.txt`: k = 1, 2, 3, 4.
Four instances.  "Infinite" and "unbounded" are quantified over all k.

This file supplies what the deliverable did not: an explicit witness, in exact
rational arithmetic, valid for EVERY k, together with a machine check of it at
k = 1..8 (|L(P)| up to 256, sixteen times the largest instance either document
verified).

The witness, and it is one line:

    faces:   for each level i and each of the two orders (a,b) of that level's
             pair, the P-compatible ordered partition
                 ( L_0 u ... u L_{i-1},  {a},  {b},  L_{i+1} u ... u L_{k-1} )
             -- 2k of them, each acting on a chamber by forcing coordinate i;
             plus the identity face (P).
    weights: 1/(2(n-1)) = 1/(2(2k-1)) on each of the 2k collapses,
             and (k-1)/(2k-1) on the identity face.

    Then sum_x w(x) T_x = P_lazy exactly, because from any chamber c exactly one
    of the two faces at level i flips coordinate i (probability 1/(2(n-1)), the
    lazy AT edge probability) and the other fixes c, and the weights sum to 1
    with (k-1)/(2k-1) >= 0 for every k >= 1.

Run:  python3 audit_vk_infinite.py
"""

import itertools
from fractions import Fraction


def V_k(k):
    """ordinal sum of k two-element antichains; n = 2k"""
    n = 2 * k
    less = set()
    for i in range(k):
        for j in range(i + 1, k):
            for a in (2 * i, 2 * i + 1):
                for b in (2 * j, 2 * j + 1):
                    less.add((a, b))
    return n, less


def linear_extensions(n, less):
    below = {x: set() for x in range(n)}
    for (a, b) in less:
        below[b].add(a)
    out = []

    def rec(used, word):
        if len(word) == n:
            out.append(tuple(word))
            return
        for x in range(n):
            if x in used:
                continue
            if below[x] <= used:
                rec(used | {x}, word + [x])

    rec(set(), [])
    return out


def is_compatible(less, ordered_partition):
    """the ordered partition is P-compatible iff a <_P b forces a's block index
    to be <= b's"""
    idx = {}
    for i, B in enumerate(ordered_partition):
        for v in B:
            idx[v] = i
    return all(idx[a] <= idx[b] for (a, b) in less)


def act(x, c):
    pos = {v: i for i, v in enumerate(c)}
    out = []
    for B in x:
        out.extend(sorted(B, key=lambda v: pos[v]))
    return tuple(out)


def at_adjacent(c, d):
    if c == d:
        return False
    diff = [i for i in range(len(c)) if c[i] != d[i]]
    return (len(diff) == 2 and diff[1] == diff[0] + 1
            and c[diff[0]] == d[diff[1]] and c[diff[1]] == d[diff[0]])


def main():
    print("=" * 78)
    print("V_k IS A BROWN WALK FOR EVERY k -- explicit witness, exact rationals")
    print("(the deliverable and STATE.md say 'positive for every k TESTED' and")
    print(" k tested = 1,2,3,4, while calling the family INFINITE / UNBOUNDED)")
    print("=" * 78)
    print("  k    n   |L(P)|   AT graph = Q_k   witness weights sum to 1   "
          "sum_x w(x) T_x == P_lazy")
    for k in range(1, 9):
        n, less = V_k(k)
        L = linear_extensions(n, less)
        m = len(L)
        lidx = {c: i for i, c in enumerate(L)}
        # AT graph and the lazy walk
        deg = [0] * m
        for i, c in enumerate(L):
            for j, d in enumerate(L):
                if at_adjacent(c, d):
                    deg[i] += 1
        hyper = all(g == k for g in deg) and m == 2 ** k
        p_edge = Fraction(1, 2 * (n - 1))
        Plazy = [[Fraction(0) for _ in range(m)] for _ in range(m)]
        for i, c in enumerate(L):
            hold = Fraction(1)
            for j, d in enumerate(L):
                if at_adjacent(c, d):
                    Plazy[i][j] = p_edge
                    hold -= p_edge
            Plazy[i][i] = hold
        # the witness
        faces, weights = [], []
        for i in range(k):
            lower = frozenset(range(0, 2 * i))
            upper = frozenset(range(2 * i + 2, n))
            a, b = 2 * i, 2 * i + 1
            for (u, v) in ((a, b), (b, a)):
                x = [B for B in (lower, frozenset([u]), frozenset([v]), upper) if B]
                assert is_compatible(less, x), "witness face is not P-compatible"
                faces.append(tuple(x))
                weights.append(p_edge)
        faces.append((frozenset(range(n)),))
        weights.append(Fraction(k - 1, 2 * k - 1))
        tot = sum(weights)
        # sum_x w(x) T_x
        M = [[Fraction(0) for _ in range(m)] for _ in range(m)]
        for x, w in zip(faces, weights):
            for i, c in enumerate(L):
                M[i][lidx[act(x, c)]] += w
        ok = all(M[i][j] == Plazy[i][j] for i in range(m) for j in range(m))
        nonneg = all(w >= 0 for w in weights)
        print("  %d   %2d   %6d   %-15s   %-24s   %s"
              % (k, n, m, hyper, "%s (nonneg: %s)" % (tot == 1, nonneg), ok))

    print()
    print("=" * 78)
    print("So V_k is positive for EVERY k, by a witness that is uniform in k --")
    print("a one-line proof, not four data points.  Both directions are wrong")
    print("in the landed text:")
    print("  * 'positive for every k TESTED' and 'PROVEN ... for k <= 4' are")
    print("    UNDER-claims -- the statement is a theorem;")
    print("  * 'the positive class is UNBOUNDED' / 'the INFINITE family V_k' are")
    print("    OVER-claims relative to the evidence actually cited (k <= 4),")
    print("    and they carry the MAJOR finding: 'genuine counterexamples, an")
    print("    infinite family of them, not a coverage gap'.")
    print("=" * 78)


if __name__ == "__main__":
    main()
