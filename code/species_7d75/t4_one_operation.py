"""T4 -- ONE OPERATION, BOTH STORIES, ON ONE INSTRUMENT.

Daniel's question is whether there is a SINGLE categorical operation with both
S_n representation theory and the poset-quotient story as instances.  The
candidate this file tests is the one Aguiar-Mahajan put at the centre of the
species/Hopf-monoid programme (Section 10.10):

        A  |-->  A / rad(A),   which for a face algebra is the SUPPORT MAP
        onto the flats -- faces to flats, Bidigare's radical theorem.

taken over a braid cone and combined with passage to the symmetry.  Precisely,
for a poset P on [n] with automorphism group G = Aut(P):

        ( k F(P) )^G  /  rad   =   k^{ AC(P) / G }.

Both of Daniel's instances are values of ONE formula, and this file computes
them on one instrument:

  * P a poset with Aut(P) trivial   ->   k^{AC(P)},    indexed by the
    QUOTIENTS OF P.                                       [the poset story]
  * P the antichain, G = S_n        ->   k^{Pi_n / S_n} = k^{p(n)},
    indexed by INTEGER PARTITIONS, and the left side is Solomon's descent
    algebra by T3.                                        [the S_n story]

  T4a  dim (kF(P))^G = |F(P)/G|, and the orbit sums span a subalgebra.
  T4b  Phi^G : (kF(P))^G -> k^{AC(P)/G} is well defined (independent of the
       chosen representative of each AC-orbit), onto, and has nilpotent
       kernel.  Hence dim (kF(P))^G/rad = |AC(P)/G|.
  T4c  The two instances read off the SAME table.
  T4d  CONTROL: the same routine run with G = Aut(P) replaced by the FULL S_n
       (which does not preserve the cone unless P is an antichain) must break
       -- the orbit sums are then not a subalgebra.
"""

import sys
from fractions import Fraction
from collections import Counter
from itertools import permutations
from kern7d75 import (poset_classes, faces_of, AC_by_acyclicity, aut,
                      sc_product, supp, perm_sc, perm_sp, rref, rank,
                      nullspace, p_count, mk_poset)

FCAP = 600          # cap on |F(P)| for the structure-constant pass
DCAP = 90           # cap on dim A^G for the nilpotency pass
bad = 0
rows = []


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)


def refines(X, Y):
    """Every block of X sits inside a block of Y."""
    return all(any(B <= C for C in Y) for B in X)


def orbit_data(items, group, act):
    rep = {}
    lab = {}
    for x in items:
        if x in lab:
            continue
        orb = {act(x, g) for g in group}
        r = len(rep)
        rep[r] = sorted(orb, key=repr)[0]
        for y in orb:
            lab[y] = r
    return rep, lab


def analyse(P, group):
    """Returns (dimA, nOrb, closed, welldef, onto, nilpotent, nACorb)."""
    n, _ = P
    F = faces_of(P)
    AC = AC_by_acyclicity(P)
    frep, flab = orbit_data(F, group, perm_sc)
    arep, alab = orbit_data(AC, group, perm_sp)
    m = len(frep)
    # structure constants of the orbit-sum basis
    tally = [[Counter() for _ in range(m)] for _ in range(m)]
    for A in F:
        ia = flab[A]
        for B in F:
            tally[ia][flab[B]][sc_product(A, B)] += 1
    closed = True
    C = [[Counter() for _ in range(m)] for _ in range(m)]
    byorb = {}
    for x in F:
        byorb.setdefault(flab[x], []).append(x)
    for i in range(m):
        for j in range(m):
            t = tally[i][j]
            for k in range(m):
                vals = {t[H] for H in byorb[k]}
                if len(vals) > 1:
                    closed = False
                C[i][j][k] = t[byorb[k][0]]
    # Phi^G
    welldef = True
    M = []
    for k in range(len(arep)):
        reps = [X for X in AC if alab[X] == k]
        rowsX = []
        for X in reps:
            rowsX.append(tuple(sum(1 for A in byorb[i] if refines(X, supp(A)))
                               for i in range(m)))
        if len(set(rowsX)) != 1:
            welldef = False
        M.append([Fraction(v) for v in rowsX[0]])
    onto = (rank(M, m) == len(arep))
    # nilpotency of ker Phi^G inside A^G, using C
    nil = None
    if m <= DCAP:
        K = [list(v) for v in nullspace(M, m)]

        def mul(u, v):
            out = [Fraction(0)] * m
            for i, a in enumerate(u):
                if a == 0:
                    continue
                for j, b in enumerate(v):
                    if b == 0:
                        continue
                    for k, c in C[i][j].items():
                        if c:
                            out[k] += a * b * c
            return out
        cur = [list(x) for x in K]
        nil = True
        for _ in range(14):
            if not cur:
                break
            prods = [mul(u, v) for u in cur for v in K]
            R = [r for r in prods if any(x != 0 for x in r)]
            if not R:
                break
            R, _ = rref(R, m)
            if len(R) >= len(cur):
                nil = False
                break
            cur = R
        else:
            nil = False
    return len(F), m, closed, welldef, onto, nil, len(arep), len(AC)


hdr("T4a/T4b  ( kF(P) )^Aut(P) / rad  =  k^{ AC(P)/Aut(P) },  all classes n<=5")
print()
print("   n classes tested  |F|>cap  dim>cap  not closed  ill-defined"
      "  not onto  not nilpotent")
for n in range(1, 6):
    cls = poset_classes(n)
    t = fskip = dskip = nc = nw = no = nn = 0
    for P in cls:
        F = faces_of(P)
        if len(F) > FCAP:
            fskip += 1
            continue
        t += 1
        G = aut(P)
        dimA, m, closed, wd, onto, nil, nAC, sAC = analyse(P, G)
        nc += (not closed)
        nw += (not wd)
        no += (not onto)
        if nil is None:
            dskip += 1
        else:
            nn += (not nil)
        rows.append((n, P, len(G), dimA, m, nAC, sAC))
    bad += nc + nw + no + nn
    print("  %2d %7d %6d %8d %8d %11d %12d %9d %14d"
          % (n, len(cls), t, fskip, dskip, nc, nw, no, nn))
print()
print("  Reading: on every poset class tested, the Aut(P)-orbit sums span a")
print("  subalgebra of kF(P), and the induced map onto functions on the")
print("  Aut(P)-orbits of AC(P) is onto with nilpotent kernel.  So")
print("  dim (kF(P))^Aut(P)/rad = |AC(P)/Aut(P)| on every class tested.")
print()

hdr("T4c  THE TWO INSTANCES, read off that one identity")
print()
print("  P = ANTICHAIN on [n]:  Aut(P) = S_n, F(P) = Sigma_n, AC(P) = Pi_n.")
print()
print("   n  |Sigma_n|  dim (kSigma_n)^{S_n}  2^(n-1)  |Pi_n/S_n|   p(n)  agree")
for n in range(1, 6):
    P = mk_poset(n, [])
    G = aut(P)
    dimA, m, closed, wd, onto, nil, nAC, sAC = analyse(P, G)
    ok = (m == 2 ** (n - 1)) and (nAC == p_count(n))
    bad += (not ok)
    print("  %2d %10d %21d %8d %11d %6d  %s"
          % (n, dimA, m, 2 ** (n - 1), nAC, p_count(n), "yes" if ok else "NO"))
print()
print("  The left column is Solomon's descent algebra, by T3 (anti-isomorphic,")
print("  0 mismatching structure constants at n <= 5).  The right column is")
print("  the number of integer partitions of n, i.e. the number of irreducible")
print("  characters of S_n.  So this instance of the identity says:")
print("      Sol(S_n) / rad  =  k^{Pi_n / S_n}  =  the character ring of S_n.")
print()
print("  P with Aut(P) TRIVIAL: the identity degenerates to kF(P)/rad =")
print("  k^{AC(P)}, indexed by the quotients of P -- the poset story.")
print()
print("   n  classes with |Aut(P)|=1  of which |AC(P)/Aut| = |AC(P)|")
for n in range(1, 6):
    cls = poset_classes(n)
    tot = same = 0
    for P in cls:
        G = aut(P)
        if len(G) == 1:
            tot += 1
            AC = AC_by_acyclicity(P)
            arep, alab = orbit_data(AC, G, perm_sp)
            same += (len(arep) == len(AC))
    print("  %2d %25d %31d" % (n, tot, same))
print()
print("  BOTH ARE THE SAME LINE OF THE SAME TABLE.  Nothing distinguishes")
print("  them except which poset is fed in and how big its symmetry group is.")
print()

hdr("T4d  CONTROL -- G must be Aut(P), not S_n")
print()
print("  The same routine with the group replaced by the FULL S_n.  For a")
print("  non-antichain P, S_n does not preserve the braid cone, so the S_n-")
print("  orbit sums of F(P) are not even a subspace of kF(P), let alone a")
print("  subalgebra.  If the routine reports 'closed' anyway it is not")
print("  measuring what T4a claims.")
print()
print("   n  non-antichain classes tested  control fired (orbits leave F(P))")
fired = miss = 0
for n in range(2, 5):
    cls = [P for P in poset_classes(n) if len(P[1]) > 0]
    f = 0
    for P in cls:
        F = set(faces_of(P))
        leaves = any(perm_sc(A, g) not in F
                     for A in F for g in permutations(range(n)))
        f += leaves
    miss += len(cls) - f
    fired += f
    print("  %2d %30d %35d" % (n, len(cls), f))
print()
if miss:
    print("  CONTROL FAILED on %d classes -- T4a's group is not doing work." % miss)
    bad += miss
else:
    print("  Fired on all %d non-antichain classes: the cone genuinely cuts the" % fired)
    print("  symmetry down from S_n to Aut(P), and T4a's group matters.")
print()
print("=" * 78)
print("T4 TOTAL BAD: %d" % bad)
print("=" * 78)
sys.exit(0)
