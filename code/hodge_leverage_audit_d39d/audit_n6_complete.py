"""mg-d39d, independent audit of mg-a806.

Target: the population attached to ledger row B6' -- the repaired scope clause.

  B6' claim column : "Delta_AT is a Brown walk on an infinite family
                      (|L(P)| = 2^k, unbounded) and NOT OTHERWISE ON ANY POSET
                      TESTED WITH |L(P)| >= 5"
  B6' label column : "PROVEN-by-computation for the negative half
                      (n <= 5 complete, plus n = 6 at |L(P)| <= 14)"

mg-86a3's `out_n6_brown.txt` says in its own first line: "(skipped 214 larger)".
So 214 of the 318 posets at n = 6 are outside every population B6' cites, and
the untested region is the LARGE-|L(P)| one -- precisely where the replacement
clause makes its universal-sounding claim.

The §9.4 sufficient test is cheap enough to close that region: it needs only
face enumeration and the refinement action, no LP.  Wherever it fires the poset
is decided NEGATIVE outright.  This runs it on all 318 posets at n = 6, so the
n = 6 level is either completed or a genuine gap is exhibited.

Poset enumeration and the face complex are the ones rebuilt in `audit_gpp.py`
(no code shared with `code/hodge_leverage/`).

Run:  python3 audit_n6_complete.py
"""

import itertools
import sys

from audit_gpp import all_posets, down_sets


def linear_extensions(n, rel):
    below = {x: set() for x in range(n)}
    for (a, b) in rel:
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


def compatible_ordered_partitions(n, rel):
    """faces of F(P): ordered partitions (B_1..B_k) with a <_P b => block(a) <=
    block(b).  Built as chains of order ideals, which is the same object."""
    ids = [m for m in down_sets(n, rel)]
    full = (1 << n) - 1
    out = []

    def rec(prev, blocks):
        if prev == full:
            out.append(tuple(blocks))
            return
        for m in ids:
            if m == prev or (prev & m) != prev:
                continue
            rec(m, blocks + [frozenset(x for x in range(n)
                                       if ((m & ~prev) >> x) & 1)])

    rec(0, [])
    return out


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


def cover_string(n, rel):
    rel = set(rel)
    cov = []
    for (a, b) in sorted(rel):
        if not any((a, c) in rel and (c, b) in rel for c in range(n)):
            cov.append("%d<%d" % (a, b))
    return " ".join(cov)


def sufficient_test(n, rel):
    L = linear_extensions(n, rel)
    m = len(L)
    idx = {c: i for i, c in enumerate(L)}
    nbr = {c: set() for c in L}
    nedges = 0
    for c in L:
        for d in L:
            if at_adjacent(c, d):
                nbr[c].add(d)
                nedges += 1
    if nedges == 0:
        return "vacuous", m, 0
    faces = compatible_ordered_partitions(n, rel)
    reachable = set()
    ncand = 0
    for x in faces:
        ok = True
        img = []
        for c in L:
            d = act(x, c)
            if d != c and d not in nbr[c]:
                ok = False
                break
            img.append((c, d))
        if not ok:
            continue
        ncand += 1
        for (c, d) in img:
            if d != c:
                reachable.add((c, d))
    total = set()
    for c in L:
        for d in nbr[c]:
            total.add((c, d))
    if total - reachable:
        return "NOT", m, ncand
    return "undecided", m, ncand


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    P = all_posets(nmax)
    for n in range(2, nmax + 1):
        counts = {"NOT": 0, "undecided": 0, "vacuous": 0}
        undec = []
        for rel in P[n]:
            verdict, m, ncand = sufficient_test(n, rel)
            counts[verdict] += 1
            if verdict == "undecided":
                undec.append((m, cover_string(n, rel), ncand))
        print("n=%d  posets=%3d   NOT a Brown walk: %3d   vacuous: %2d   "
              "undecided by this test: %2d"
              % (n, len(P[n]), counts["NOT"], counts["vacuous"],
                 counts["undecided"]))
        for (m, cs, ncand) in sorted(undec):
            print("      undecided: |L(P)|=%3d  candidate faces=%-4d  %s"
                  % (m, ncand, cs))
        sys.stdout.flush()


if __name__ == "__main__":
    main()
