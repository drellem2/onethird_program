"""mg-d39d, independent audit of mg-a806.

Target: the clause ledger row B6 KEEPS through the mg-a806 repair --

    "not a Brown walk on 2/5 at n=3, 11/16 at n=4, 55/63 at n=5,
     INCLUDING ALL ANTICHAINS n >= 3"     (label: PROVEN-by-computation)

The populations named are n <= 5, so the antichain clause is a universal in `n`
carried by three instances (A_3, A_4, A_5).  `run_lrb.py` loops `range(2, 6)`
and mg-86a3's n = 6 pass is restricted to |L(P)| <= 14, so A_6 (|L| = 720) is
outside every population the row cites.

This file does two things:

  1. runs the §9.4 sufficient test on A_6 directly -- one `n` past everything
     the row rests on;
  2. checks the two-line proof that makes the clause a THEOREM for every
     n >= 3, by verifying its combinatorial core on n = 3..7.

Own code throughout: chambers are permutations, faces are ordered set
partitions, x.c is refinement.

Run:  python3 audit_antichain_scope.py
"""

import itertools
import sys


def ordered_set_partitions(n):
    """every ordered partition of [n] = every face of F(A_n)"""
    elts = list(range(n))

    def rec(remaining):
        if not remaining:
            yield []
            return
        rem = sorted(remaining)
        first = rem[0]
        others = rem[1:]
        for k in range(len(others) + 1):
            for extra in itertools.combinations(others, k):
                block = frozenset((first,) + extra)
                rest = set(remaining) - block
                for tail in rec(rest):
                    yield [block] + tail

    # rec above fixes the smallest remaining element into the FIRST block,
    # which enumerates unordered partitions; permute the blocks for ordered.
    seen = set()
    for part in rec(set(elts)):
        for perm in itertools.permutations(range(len(part))):
            op = tuple(part[i] for i in perm)
            if op not in seen:
                seen.add(op)
                yield op


def act(x, c):
    """x . c : refine the chamber c (a word) by the ordered partition x"""
    pos = {v: i for i, v in enumerate(c)}
    out = []
    for B in x:
        out.extend(sorted(B, key=lambda v: pos[v]))
    return tuple(out)


def at_neighbours(c):
    out = set()
    for i in range(len(c) - 1):
        d = list(c)
        d[i], d[i + 1] = d[i + 1], d[i]
        out.add(tuple(d))
    return out


def sufficient_test_antichain(n, verbose=True):
    chambers = list(itertools.permutations(range(n)))
    nbr = {c: at_neighbours(c) for c in chambers}
    faces = list(ordered_set_partitions(n))
    candidates = []
    for x in faces:
        ok = True
        for c in chambers:
            d = act(x, c)
            if d != c and d not in nbr[c]:
                ok = False
                break
        if ok:
            candidates.append(x)
    reachable = set()
    for x in candidates:
        for c in chambers:
            d = act(x, c)
            if d != c:
                reachable.add((c, d))
    edges = set()
    for c in chambers:
        for d in nbr[c]:
            edges.add((c, d))
    unreachable = edges - reachable
    if verbose:
        print("A_%d : |L|=%4d  faces=%6d  candidate faces=%d %s"
              % (n, len(chambers), len(faces), len(candidates),
                 [tuple(sorted(B) for B in x) for x in candidates]
                 if len(candidates) <= 3 else ""))
        print("      directed AT edges=%d  reachable by a candidate=%d"
              "  UNREACHABLE=%d  ->  %s"
              % (len(edges), len(reachable), len(unreachable),
                 "NOT a Brown walk" if unreachable else "undecided by this test"))
    return len(candidates), len(unreachable)


def proof_core(n):
    """The two-line proof, checked mechanically.

    Claim: for n >= 3 the ONLY candidate face is the identity face ([n]).
    Reason: given a face x with k >= 2 blocks, take the chamber c that lists
    the blocks in REVERSE x-order.  Then x.c inverts every cross-block pair, so
    inv(x.c, c) = sum_{i<j} |B_i||B_j| >= n-1 >= 2, hence x.c is neither c nor
    an AT neighbour of c.  This checks the arithmetic bound on every ordered
    partition, and checks that the witness chamber really does that.
    """
    worst_min = None
    bad = 0
    for x in ordered_set_partitions(n):
        if len(x) == 1:
            continue
        cross = 0
        sizes = [len(B) for B in x]
        for i in range(len(sizes)):
            for j in range(i + 1, len(sizes)):
                cross += sizes[i] * sizes[j]
        # the reversing witness
        c = []
        for B in reversed(x):
            c.extend(sorted(B))
        c = tuple(c)
        d = act(x, c)
        pos = {v: i for i, v in enumerate(c)}
        inv = sum(1 for a in range(n) for b in range(a + 1, n)
                  if pos[d[a]] > pos[d[b]])
        if inv != cross:
            bad += 1
        if worst_min is None or cross < worst_min:
            worst_min = cross
    return worst_min, bad


def main():
    print("=" * 78)
    print("1.  the §9.4 sufficient test on A_6 -- one n past every population")
    print("    ledger row B6 cites (run_lrb.py stops at n=5; mg-86a3's n=6")
    print("    pass is capped at |L(P)| <= 14 and A_6 has |L| = 720)")
    print("=" * 78)
    for n in (3, 4, 5, 6):
        sufficient_test_antichain(n)
    print()
    print("=" * 78)
    print("2.  the clause is not merely computational: it is a two-line THEOREM")
    print("    for every n >= 3.  Checked mechanically on n = 3..7:")
    print("    min over all k>=2 ordered partitions of sum_{i<j}|B_i||B_j|,")
    print("    and whether the reversing chamber realises exactly that many")
    print("    inversions (>= 2 means x.c is not c and not an AT neighbour).")
    print("=" * 78)
    for n in range(3, 8):
        mn, bad = proof_core(n)
        print("    n=%d  min cross-block pairs = %d (>=2: %s)   witness mismatches = %d"
              % (n, mn, mn >= 2, bad))
    print()
    print("    => for every n >= 3 the identity face is the ONLY candidate, so")
    print("       no AT edge is reachable and the lazy AT walk is NOT a Brown")
    print("       walk on A_n.  The row's 'including all antichains n >= 3' is")
    print("       TRUE and is a theorem; the label PROVEN-by-computation on a")
    print("       n <= 5 population is the wrong one in BOTH directions.")


if __name__ == "__main__":
    main()
