"""mg-66a6 AUDIT, targets 1 and 4: the exhaustive sweeps the note leans on, and
in particular the EXACT SCOPE of what "verified to five elements" covers.

Reproduced independently here:
  * the poset counts 1/3/19/219/4231 (labelled) and 1/2/5/16/63 (classes)
  * the band identities x.x=x, x.y.x=x.y, closure, on every labelled poset
  * levels == acyclic quotients, on every labelled poset up to 5 elements
  * the sign-imbalance census, Delta_AT . ONE = 0, AT connectivity
  * the section-8 lazy-adjacent-transposition boundary counts
"""

import sys
from fractions import Fraction

from audit_lib import (all_labelled_posets, iso_classes, canon, poset, moves,
                       levels, acyclic_partitions, product, lstr, mstr,
                       orderings, act, at_graph, at_laplacian, sgn, connected,
                       mat_vec, set_partitions, quotient_acyclic, rank_Q,
                       multiplicities)
from itertools import permutations

FAIL = []
CHECKS = [0]


def check(label, got, want):
    CHECKS[0] += 1
    ok = got == want
    print("  [%s] %s" % ("OK " if ok else "FAIL", label))
    if not ok:
        print("        note says : %r" % (want,))
        print("        recomputed: %r" % (got,))
        FAIL.append(label)
    return ok


print(__doc__)
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 5

print("=" * 78)
print("SECTION A -- how many posets there are")
print("=" * 78)
LAB = {}
CLS = {}
for n in range(1, NMAX + 1):
    LAB[n] = all_labelled_posets(n)
    CLS[n] = iso_classes(n)
    print("  n=%d: %d labelled, %d isomorphism classes"
          % (n, len(LAB[n]), len(CLS[n])))
want_lab = {1: 1, 2: 3, 3: 19, 4: 219, 5: 4231}
want_cls = {1: 1, 2: 2, 3: 5, 4: 16, 5: 63}
check("labelled poset counts 1/3/19/219/4231",
      [len(LAB[n]) for n in range(1, NMAX + 1)],
      [want_lab[n] for n in range(1, NMAX + 1)])
check("isomorphism class counts 1/2/5/16/63",
      [len(CLS[n]) for n in range(1, NMAX + 1)],
      [want_cls[n] for n in range(1, NMAX + 1)])

print()
print("=" * 78)
print("SECTION B -- the band identities, exhaustively (note section 2 table)")
print("=" * 78)
note_band = {
    2: dict(posets=3, moves=7, pairs=17, triples=43),
    3: dict(posets=19, moves=121, pairs=865, triples=6949),
    4: dict(posets=219, moves=4399, pairs=109121, triples=None),
    5: dict(posets=63, moves=5757, pairs=922073, triples=None),
}
for n in range(2, NMAX + 1):
    pool = CLS[n] if n == 5 else LAB[n]
    nmov = npair = 0
    bad_idem = bad_xyx = bad_clos = 0
    ntrip = bad_assoc = 0
    for P in pool:
        MV = moves(P)
        S = set(MV)
        nmov += len(MV)
        for x in MV:
            if product(x, x) != x:
                bad_idem += 1
        for x in MV:
            for y in MV:
                npair += 1
                xy = product(x, y)
                if product(xy, x) != xy:
                    bad_xyx += 1
                if xy not in S:
                    bad_clos += 1
        if n <= 3:
            for x in MV:
                for y in MV:
                    xy = product(x, y)
                    for z in MV:
                        ntrip += 1
                        if product(xy, z) != product(x, product(y, z)):
                            bad_assoc += 1
    nb = note_band[n]
    label = "classes" if n == 5 else "labelled posets"
    print("  n=%d over %d %s: %d moves, %d pairs%s"
          % (n, len(pool), label, nmov, npair,
             ", %d triples" % ntrip if ntrip else ""))
    check("n=%d: the note's move total %d" % (n, nb["moves"]), nmov,
          nb["moves"])
    check("n=%d: the note's pair total %d" % (n, nb["pairs"]), npair,
          nb["pairs"])
    check("n=%d: 0 failures of x.x = x" % n, bad_idem, 0)
    check("n=%d: 0 failures of x.y.x = x.y" % n, bad_xyx, 0)
    check("n=%d: 0 failures of closure" % n, bad_clos, 0)
    if nb["triples"]:
        check("n=%d: the note's triple total %d" % (n, nb["triples"]), ntrip,
              nb["triples"])
        check("n=%d: 0 failures of associativity" % n, bad_assoc, 0)

print()
print("=" * 78)
print("SECTION C -- levels == acyclic quotients, on EVERY labelled poset")
print("=" * 78)
for n in range(1, NMAX + 1):
    agree = 0
    bad = []
    for P in LAB[n]:
        if sorted(map(lstr, levels(P))) == sorted(map(lstr,
                                                     acyclic_partitions(P))):
            agree += 1
        else:
            bad.append(P)
    print("  n=%d: %d of %d labelled posets agree" % (n, agree, len(LAB[n])))
    check("n=%d: %d of %d, 0 disagreements" % (n, want_lab[n], want_lab[n]),
          (agree, len(LAB[n]), len(bad)), (want_lab[n], want_lab[n], 0))

print()
print("  SCOPE NOTE.  This is the whole of the evidence for the acyclic-cut")
print("  description.  n=6 is NOT covered here and is not covered by the")
print("  note either.")

print()
print("=" * 78)
print("SECTION D -- the sign census (note section 6c)")
print("=" * 78)
note_bal = {2: (2, 1, 1), 3: (5, 3, 2), 4: (16, 11, 5), 5: (63, 44, 19)}
for n in range(2, NMAX + 1):
    bal = notbal = 0
    badconn = badone = 0
    for P in CLS[n]:
        ords = orderings(P)
        imb = sum(sgn(w) for w in ords)
        if imb == 0:
            bal += 1
        else:
            notbal += 1
        A = at_graph(P, ords)
        if not connected(A):
            badconn += 1
        L = at_laplacian(P, ords)
        if any(v != 0 for v in mat_vec(L, [1] * len(ords))):
            badone += 1
    print("  n=%d: %d classes, %d balanced, %d not"
          % (n, len(CLS[n]), bal, notbal))
    check("n=%d: the note's balanced/not split %s" % (n, note_bal[n][1:]),
          (len(CLS[n]), bal, notbal), note_bal[n])
    check("n=%d: AT graph connected on every class" % n, badconn, 0)
    check("n=%d: Delta_AT . ONE = 0 on every class" % n, badone, 0)

print()
print("  labelling-independence of 'imbalance vanishes':")
for n in range(2, min(NMAX, 4) + 1):
    bad = 0
    for P in CLS[n]:
        base = sum(sgn(w) for w in orderings(P))
        nn, R = P
        for p in permutations(range(nn)):
            Q = (nn, frozenset((p[a], p[b]) for (a, b) in R))
            imb = sum(sgn(w) for w in orderings(Q))
            if (imb == 0) != (base == 0):
                bad += 1
            # the stronger statement the note makes: it is multiplied by the
            # sign of the relabelling
            if imb != sgn(p) * base:
                bad += 1
    check("n=%d: imbalance multiplies by sgn(relabelling), over all "
          "relabellings of every class" % n, bad, 0)

chain = poset(3, [(0, 1), (1, 2)])
check("a chain has one linear extension", len(orderings(chain)), 1)
check("and (with this increasing labelling) imbalance +1",
      sum(sgn(w) for w in orderings(chain)), 1)
chain_rev = poset(3, [(2, 1), (1, 0)])
print("  NOTE: the same chain labelled decreasingly has imbalance %d"
      % sum(sgn(w) for w in orderings(chain_rev)))
for n in range(2, min(NMAX, 6) + 1):
    anti = poset(n, [])
    check("antichain on %d: imbalance 0" % n,
          sum(sgn(w) for w in orderings(anti)), 0)

print()
print("=" * 78)
print("SECTION E -- the section-8 boundary counts (lazy AT walk)")
print("=" * 78)
note_b = {2: (0, 1, 1), 3: (2, 1, 2), 4: (11, 1, 4), 5: (55, 1, 7)}
for n in range(2, NMAX + 1):
    notin = vac = undec = 0
    for P in CLS[n]:
        ords = orderings(P)
        if len(ords) == 1:
            vac += 1
            continue
        A = at_graph(P, ords)
        idx = {c: i for i, c in enumerate(ords)}
        needed = {(i, j) for i in range(len(ords)) for j in range(len(ords))
                  if A[i][j]}
        supplied = set()
        for x in moves(P):
            usable = True
            for c in ords:
                d = act(x, c)
                if d != c and not A[idx[c]][idx[d]]:
                    usable = False
                    break
            if usable:
                for c in ords:
                    d = act(x, c)
                    if d != c:
                        supplied.add((idx[c], idx[d]))
        if needed - supplied:
            notin += 1
        else:
            undec += 1
    print("  n=%d: %d provably not / %d vacuous / %d undecided"
          % (n, notin, vac, undec))
    check("n=%d: the note's boundary row %s" % (n, note_b[n]),
          (notin, vac, undec), note_b[n])

print()
print("  the antichain specifically:")
for n in range(3, min(NMAX, 5) + 1):
    P = poset(n, [])
    ords = orderings(P)
    A = at_graph(P, ords)
    idx = {c: i for i, c in enumerate(ords)}
    needed = {(i, j) for i in range(len(ords)) for j in range(len(ords))
              if A[i][j]}
    usable = []
    for x in moves(P):
        ok = True
        for c in ords:
            d = act(x, c)
            if d != c and not A[idx[c]][idx[d]]:
                ok = False
                break
        if ok:
            usable.append(x)
    supplied = set()
    for x in usable:
        for c in ords:
            d = act(x, c)
            if d != c:
                supplied.add((idx[c], idx[d]))
    print("     n=%d: %d needed edges, %d usable move(s) %s, %d supplied"
          % (n, len(needed), len(usable), [mstr(x) for x in usable],
             len(supplied)))
    check("n=%d antichain: exactly one usable move and it is the do-nothing "
          "move" % n, [mstr(x) for x in usable],
          ["(" + "".join("abcde"[e] for e in range(n)) + ")"])
    check("n=%d antichain: supplies 0 of the %d needed edges"
          % (n, {3: 12, 4: 72, 5: 480}[n]),
          (len(supplied), len(needed)), (0, {3: 12, 4: 72, 5: 480}[n]))

print()
print("=" * 78)
print("%d checks, %d FAILURES" % (CHECKS[0], len(FAIL)))
for f in FAIL:
    print("  FAILED: %s" % f)
print("=" * 78)
sys.exit(1 if FAIL else 0)
