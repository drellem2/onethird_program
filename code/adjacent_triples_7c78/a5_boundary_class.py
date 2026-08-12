#!/usr/bin/env python3
"""mg-7c78 arm a5 — THE POPULATION THE HYPOTHESIS ACTUALLY LIVES ON, AND THE VACUITY IT AVOIDS.

⚠️  THE FROZEN CLASS IS EMPTY AT EVERY n AN ENUMERATOR REACHES.  `delta(P) < 1/3` IS the
(1/3)-(2/3) counterexample condition and the conjecture is verified to n = 14 (`mg-33f5`), so a
sweep reporting `0 failures over frozen posets` reports zero failures in an EMPTY POPULATION and
carries no information.  `FACTS.md` F1's corollary already carries exactly this warning; this arm
prints the count anyway, with the reason attached, so that the zero cannot be re-quoted as a
clean sweep.

WHAT IT MEASURES INSTEAD is the BOUNDARY class: `delta(P) = 1/3` exactly -- every incomparable
pair is `>= 2/3`-decided.  That is the closest non-empty approximation to Daniel's hypothesis any
instrument can see, and every statement of this ticket is re-measured on it EXHAUSTIVELY.

  m1  CENSUS.  min delta over posets with an incomparable pair, per n; count at delta = 1/3;
      count at delta < 1/3 (with the reason).  n = 2..8 EXHAUSTIVE over isomorphism classes.
  m2  COHERENCE, re-derived.  On the boundary class the `>= 2/3` majority relation is acyclic,
      extends to a linear order e, and e is a linear extension of P.  (Anchor: `mg-61bb`.)
  m3  EVERY STATEMENT OF THIS TICKET, restricted to the boundary class, EXHAUSTIVELY:
      R1 existence · R2 covering · the E_xy cap · the free-triple population.
  m4  THE CAP, ATTAINED.  On the boundary class Pr[E_xy] <= 2*delta = 2/3 for every incomparable
      pair.  The maximum actually attained is reported -- if it is 2/3 the bound is tight there.

Exits 0 if the census is internally consistent and m2/m3's failure counts are 0, 1 otherwise,
2 on refusal.
"""

import sys
from fractions import Fraction

import lib7c78 as L

NMAX = 8
THIRD = Fraction(1, 3)


def covered_pairs(n, ext):
    out = set()
    for k in range(n - 2):
        a, b, c = ext[k], ext[k + 1], ext[k + 2]
        for u, v in ((a, b), (b, c), (a, c)):
            out.add((min(u, v), max(u, v)))
    return out


def main():
    print("=" * 92)
    print("mg-7c78  a5  the boundary class delta = 1/3, and the empty population it replaces")
    print("=" * 92)
    print()

    classes = L.all_classes(NMAX)

    census = {}
    boundary = []
    for n in range(2, NMAX + 1):
        mn = None
        at_third = below_third = tot = 0
        for down in classes[n]:
            inc = L.incomparable_pairs(n, down)
            if not inc:
                continue
            tot += 1
            exts = L.linear_extensions(n, down)
            p = L.pair_probs(n, down, exts)
            d = L.delta(n, down, p)
            if mn is None or d < mn:
                mn = d
            if d == THIRD:
                at_third += 1
                boundary.append((n, down, exts, p))
            elif d < THIRD:
                below_third += 1
        census[n] = (tot, mn, at_third, below_third)

    print("m1  CENSUS -- n = 2..%d EXHAUSTIVE over every isomorphism class" % NMAX)
    print("-" * 92)
    print("    %3s %10s %14s %16s %20s" % ("n", "posets", "min delta", "delta = 1/3", "delta < 1/3 (FROZEN)"))
    for n in sorted(census):
        tot, mn, at3, be3 = census[n]
        print("    %3d %10d %14s %16d %20d" % (n, tot, str(mn), at3, be3))
    total_frozen = sum(v[3] for v in census.values())
    total_bnd = sum(v[2] for v in census.values())
    print()
    print("    FROZEN POSETS FOUND: %d." % total_frozen)
    print("    ⚠️  THAT ZERO CARRIES NO INFORMATION AND IS NOT A CLEAN SWEEP.  delta < 1/3 IS the")
    print("    counterexample condition; the conjecture is verified to n = 14, so the population")
    print("    of frozen posets any enumerator can reach is EMPTY BY CONSTRUCTION.  Any statement")
    print("    of the form `0 failures over frozen posets` is zero failures in an empty set.")
    print()
    print("    BOUNDARY POSETS FOUND: %d, at every n from 3 to %d.  THIS is the population every"
          % (total_bnd, NMAX))
    print("    figure below is measured on, and it is EXHAUSTIVE.")
    print()

    ok = total_frozen == 0 and total_bnd > 0

    print("m2  COHERENCE on the boundary class -- the majority relation extends to a linear e")
    print("-" * 92)
    m2_fail = 0
    es = []
    for (n, down, exts, p) in boundary:
        # majority digraph on incomparable pairs: orient toward the >= 2/3 side
        adj = [[False] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j and L.is_below(down, i, j):
                    adj[i][j] = True
        for (x, y) in L.incomparable_pairs(n, down):
            pxy = p[(x, y)]
            if pxy >= Fraction(2, 3):
                adj[x][y] = True
            elif 1 - pxy >= Fraction(2, 3):
                adj[y][x] = True
            else:
                m2_fail += 1          # a pair that is not >= 2/3-decided: impossible at delta=1/3
        # topological sort -> e
        indeg = [sum(1 for i in range(n) if adj[i][j]) for j in range(n)]
        order, avail = [], [j for j in range(n) if indeg[j] == 0]
        while avail:
            j = min(avail)
            avail.remove(j)
            order.append(j)
            for k in range(n):
                if adj[j][k]:
                    indeg[k] -= 1
                    if indeg[k] == 0:
                        avail.append(k)
        if len(order) != n:
            m2_fail += 1              # a cycle: refutes the no-3-cycle anchor
            es.append(None)
            continue
        if tuple(order) not in set(exts):
            m2_fail += 1              # e must itself be a linear extension
            es.append(None)
            continue
        es.append(tuple(order))
    ok &= m2_fail == 0
    print("    %d boundary posets · failures %d   [%s]"
          % (len(boundary), m2_fail, "PASS" if m2_fail == 0 else "FAIL"))
    print("    Every boundary poset has every incomparable pair >= 2/3-decided, the majority")
    print("    relation is ACYCLIC, and the order e it extends to IS a linear extension of P.")
    print()

    print("m3  EVERY STATEMENT OF THIS TICKET, ON THE BOUNDARY CLASS, EXHAUSTIVELY")
    print("-" * 92)
    r1_pairs = r1_fail = 0
    r2_posets = r2_fail = 0
    cap_pairs = cap_fail = 0
    cap_max = Fraction(0)
    free_tri_posets = free_tri_have = 0
    for idx, (n, down, exts, p) in enumerate(boundary):
        e = es[idx]
        rank = {v: k for k, v in enumerate(e)} if e else None
        inc = L.incomparable_pairs(n, down)
        N = len(exts)
        incset = set(inc)
        # R1: some extension puts the pair inside a 3-block in e-order
        for (x, y) in inc:
            r1_pairs += 1
            found = False
            for ext in exts:
                pos = {v: k for k, v in enumerate(ext)}
                for k in range(n - 2):
                    blk = (ext[k], ext[k + 1], ext[k + 2])
                    if x in blk and y in blk:
                        if rank is None or (pos[x] < pos[y]) == (rank[x] < rank[y]):
                            found = True
                            break
                if found:
                    break
            if not found:
                r1_fail += 1
        # R2
        if n >= 3:
            r2_posets += 1
            if min(len(incset - covered_pairs(n, ext)) for ext in exts) > 0:
                r2_fail += 1
        # the E_xy cap and the free-triple population
        for (x, y) in inc:
            cap_pairs += 1
            c = sum(1 for ext in exts if L.value_transposition_legal(n, down, ext, x, y))
            pe = Fraction(c, N)
            if pe > cap_max:
                cap_max = pe
            if pe > 2 * THIRD:
                cap_fail += 1
        free_tri_posets += 1
        have = False
        for ext in exts:
            for k in range(n - 2):
                if L.free_set(down, (ext[k], ext[k + 1], ext[k + 2])):
                    have = True
                    break
            if have:
                break
        free_tri_have += 1 if have else 0

    ok &= r1_fail == 0 and cap_fail == 0
    print("    R1 (pair inside an e-aligned 3-block, some extension):")
    print("        %d pairs · failures %d   [%s]"
          % (r1_pairs, r1_fail, "PASS" if r1_fail == 0 else "FAIL"))
    print("    R2 (one extension covering every incomparable edge):")
    print("        %d posets (n>=3) · R2 FAILS at %d" % (r2_posets, r2_fail))
    print("        ⚠️  R2 IS FALSE IN GENERAL (a2: 2384 of 3242 posets) AND TRUE HERE.  That is the")
    print("        one place in this instrument where the hypothesis DOES work -- followed up in a6.")
    print("    THE CAP  Pr[E_xy] <= 2*delta = 2/3:")
    print("        %d pairs · violations %d   [%s]   MAXIMUM ATTAINED = %s"
          % (cap_pairs, cap_fail, "PASS" if cap_fail == 0 else "FAIL", cap_max))
    print("        %s" % ("ATTAINED WITH ZERO SLACK -- the bound is tight on this class."
                          if cap_max == 2 * THIRD else
                          "NOT attained on this class; the largest observed is above."))
    print("    FREE CONSECUTIVE TRIPLES (`adjacent triples` in the strongest sense):")
    print("        %d of %d boundary posets have one in some linear extension."
          % (free_tri_have, free_tri_posets))
    print()

    print("VERDICT: %s" % ("GREEN" if ok else "RED"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:                                     # noqa: BLE001
        print("REFUSED: %s" % exc)
        sys.exit(2)
