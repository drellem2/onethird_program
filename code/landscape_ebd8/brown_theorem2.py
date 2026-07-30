#!/usr/bin/env python3
"""
IDENTIFICATION CHECK 2, not new mathematics.

Claim being tested: the programme's spectral result for the face-driven walks
on L(P) is Brown's Theorem 2 applied to the order cone -- not merely Brown's
Theorem 1 (the general left-regular-band theorem) plus work of our own.

  Brown, "Semigroups, rings, and Markov chains", J. Theoret. Probab. 13 (2000)
  871-938, arXiv:math/0006145.

  Section 4.1 sets up a CONVEX SET OF CHAMBERS D of an arrangement A, cut out
  by sign conditions sigma_i = + on a subset J of the hyperplanes, with
  U = intersection of the open halfspaces H_i^+.  G is the subsemigroup of
  faces with sigma_i(G) >= 0 for all i in J; its chambers are D.  G_0 is the
  set of faces lying in the OPEN set U.  M_0 is the set of flats X that
  intersect U.

  THEOREM 2 (Brown).  For any probability distribution {w_G} on G the
  transition matrix of the walk on D is diagonalizable, with an eigenvalue
        lambda_X = sum over G subset of X of w_G
  for each X in M_0, of multiplicity  |mu(X, V)|.

Specialisation to a poset P on [n]:
    A  = braid arrangement,   faces = ordered set partitions of [n]
    U  = { x : x_i < x_j whenever i < j in P }      (the open order cone)
    G  = the P-compatible ordered set partitions    (the programme's "moves")
    D  = the linear extensions of P                 (the programme's states)
    M_0 = { partitions pi : every block is an ANTICHAIN of P, and the
            quotient P/pi is acyclic }
    |mu(X,V)| = prod over blocks B of X of (|B| - 1)!      (interval [X,V] in
            Pi_n is a product of partition lattices Pi_{|B|})

So Brown's Theorem 2 predicts, in CLOSED FORM:

    m_X = prod_{B in X} (|B| - 1)!   if every block of X is an antichain of P
                                     and P/X is acyclic
        = 0                          otherwise.

The programme instead SOLVES the triangular counting identity
    sum_{Y refines X, Y in AC(P)} m_Y = prod_{B in X} |L(P|_B)|
from the finest level upwards, and reads off which levels carry multiplicity.
This script computes m_X BOTH ways and compares them.

Tested predictions
------------------
  B1  the two multiplicity functions agree at every level of AC(P);
  B2  the support of m (levels with m_X != 0) is exactly M_0;
  B3  sum over all levels of m_X = |L(P)|  (Brown's (10) at X = discrete);
  B4  the antichain closed form m_X = prod (|B|-1)! is the specialisation of
      B1 to P with no relations -- i.e. M_0 = Pi_n there.

Self-contained; shares no code with the rest of the repository.  Exact integer
arithmetic.
"""

import itertools
import sys

from identify_lattice import (transitive_closure, iso_classes, set_partitions,
                              acyclic_quotient, linear_extensions, refines,
                              block_of, is_connected)


def factorial(k):
    r = 1
    for i in range(2, k + 1):
        r *= i
    return r


def induced_linear_extension_count(n, rel, block):
    """|L(P restricted to block)|."""
    elts = sorted(block)
    idx = {x: i for i, x in enumerate(elts)}
    m = len(elts)
    sub = {(idx[a], idx[b]) for (a, b) in rel if a in block and b in block}
    return len(linear_extensions(m, sub))


def all_blocks_antichains(rel, pi):
    """Every block of pi is an antichain of P."""
    for b in pi:
        for (x, y) in rel:
            if x in b and y in b:
                return False
    return True


def programme_multiplicities(n, rel, AC):
    """Solve  sum_{Y refines X} m_Y = prod_B |L(P|_B)|  over AC(P), from the
    finest level upwards.  This is the programme's own recipe."""
    order = sorted(range(len(AC)), key=lambda i: len(AC[i]), reverse=True)  # finest first
    m = {}
    for i in order:
        X = AC[i]
        rhs = 1
        for b in X:
            rhs *= induced_linear_extension_count(n, rel, b)
        s = 0
        for j in order:
            if j == i:
                continue
            if refines(AC[j], X):
                s += m[j]
        m[i] = rhs - s
    return m


def brown_multiplicities(rel, AC):
    """Brown Theorem 2 in closed form on the same index set."""
    out = {}
    for i, X in enumerate(AC):
        if all_blocks_antichains(rel, X):
            p = 1
            for b in X:
                p *= factorial(len(b) - 1)
            out[i] = p
        else:
            out[i] = 0
    return out


def analyse(n):
    parts = list(set_partitions(n))
    stats = {'classes': 0, 'B1_bad': 0, 'B2_bad': 0, 'B3_bad': 0,
             'levels': 0, 'nonzero_levels': 0}
    for rel in iso_classes(n):
        stats['classes'] += 1
        AC = [pi for pi in parts if acyclic_quotient(n, rel, pi)]
        stats['levels'] += len(AC)

        mp = programme_multiplicities(n, rel, AC)
        mb = brown_multiplicities(rel, AC)

        # B1
        if any(mp[i] != mb[i] for i in range(len(AC))):
            stats['B1_bad'] += 1
            print("  B1 FAIL n=%d rel=%s" % (n, sorted(rel)), file=sys.stderr)
            for i in range(len(AC)):
                if mp[i] != mb[i]:
                    print("     level %s programme=%d brown=%d"
                          % (["".join(str(x) for x in sorted(b)) for b in AC[i]],
                             mp[i], mb[i]), file=sys.stderr)

        # B2: support of m == M_0 (blocks antichains; acyclicity already holds on AC)
        supp_prog = {i for i in range(len(AC)) if mp[i] != 0}
        M0 = {i for i, X in enumerate(AC) if all_blocks_antichains(rel, X)}
        stats['nonzero_levels'] += len(supp_prog)
        if supp_prog != M0:
            stats['B2_bad'] += 1
            print("  B2 FAIL n=%d rel=%s" % (n, sorted(rel)), file=sys.stderr)

        # B3: total = |L(P)|
        if sum(mp.values()) != len(linear_extensions(n, rel)):
            stats['B3_bad'] += 1
            print("  B3 FAIL n=%d rel=%s" % (n, sorted(rel)), file=sys.stderr)
    return stats


def antichain_check(nmax):
    print()
    print("B4 -- the antichain specialisation (the repo's section 7 formula)")
    print("  m_X = prod_B (|B|-1)!  on every partition, and M_0 = Pi_n")
    print("  %-4s %-9s %-14s %-16s" % ("n", "|Pi_n|", "sum m_X", "n! ?"))
    for n in range(2, nmax + 1):
        parts = list(set_partitions(n))
        rel = frozenset()
        AC = [pi for pi in parts if acyclic_quotient(n, rel, pi)]
        mp = programme_multiplicities(n, rel, AC)
        mb = brown_multiplicities(rel, AC)
        agree = all(mp[i] == mb[i] for i in range(len(AC)))
        tot = sum(mp.values())
        nf = factorial(n)
        print("  %-4d %-9d %-14s %-16s" % (
            n, len(AC), "%d %s" % (tot, "OK" if tot == nf else "MISMATCH"),
            "%d  closed form %s" % (nf, "agrees" if agree else "DISAGREES")))


def worked_example():
    """The repo's worked example P = {a<b, c<d}, which is also Brown's own
    illustration in section 4.1 (braid arrangement in R^4, U given by two
    inequalities, six chambers)."""
    n = 4
    # 0=a, 1=b, 2=c, 3=d ; a<b and c<d
    rel = transitive_closure(n, {(0, 1), (2, 3)})
    names = "abcd"
    parts = list(set_partitions(n))
    AC = [pi for pi in parts if acyclic_quotient(n, rel, pi)]
    mp = programme_multiplicities(n, rel, AC)
    mb = brown_multiplicities(rel, AC)
    les = linear_extensions(n, rel)
    print()
    print("The worked example P = {a<b, c<d}: %d levels, %d linear extensions"
          % (len(AC), len(les)))
    print("  (Brown section 4.1 illustrates Theorem 2 on exactly this configuration:")
    print("   braid arrangement in R^4, U given by two inequalities, six chambers.)")
    print()
    print("  %-14s %-12s %-12s %-10s %-8s" %
          ("level", "programme", "Brown |mu|", "blocks", "in M_0"))
    for i, X in enumerate(AC):
        lbl = "|".join("".join(names[x] for x in sorted(b)) for b in X)
        anti = all_blocks_antichains(rel, X)
        print("  %-14s %-12d %-12d %-10s %-8s%s" %
              (lbl, mp[i], mb[i],
               "x".join(str(len(b)) for b in X),
               "yes" if anti else "no",
               "" if mp[i] == mb[i] else "   <-- MISMATCH"))
    print()
    print("  sum of multiplicities = %d   (|L(P)| = %d)  %s"
          % (sum(mp.values()), len(les),
             "OK" if sum(mp.values()) == len(les) else "MISMATCH"))
    print("  Brown's six chambers 1234,1324,1342,3124,3142,3412 vs ours: %d states"
          % len(les))


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    print("=" * 78)
    print("IDENTIFICATION CHECK 2: is the programme's spectral result")
    print("BROWN'S THEOREM 2 (walks on a CONVEX SET of chambers)?")
    print("Brown, J. Theoret. Probab. 13 (2000) 871-938, arXiv:math/0006145.")
    print("The closed form m_X = prod_B (|B|-1)! * [every block an antichain]")
    print("is read off Brown; the programme's m_X is solved from its own")
    print("counting identity.  Nothing is fitted.")
    print("=" * 78)
    print()
    print("%-4s %-9s %-9s %-22s %-16s %-16s" %
          ("n", "classes", "levels", "B1 closed form = solved",
           "B2 support = M_0", "B3 total = |L(P)|"))
    for n in range(2, nmax + 1):
        s = analyse(n)
        print("%-4d %-9d %-9d %-22s %-16s %-16s" % (
            n, s['classes'], s['levels'],
            "%d bad of %d" % (s['B1_bad'], s['classes']),
            "%d bad of %d" % (s['B2_bad'], s['classes']),
            "%d bad of %d" % (s['B3_bad'], s['classes'])))

    antichain_check(min(nmax, 6))
    worked_example()
    print()
    print("=" * 78)
    print("If every column reads 0 bad, the programme's multiplicity rule is")
    print("Brown's Theorem 2 specialised to the order cone, and Brown's closed")
    print("form is STRICTLY MORE INFORMATIVE than the triangular solve: it")
    print("names the spectrum-carrying levels outright.")
    print("=" * 78)


if __name__ == '__main__':
    main()
