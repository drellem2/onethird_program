"""T5 -- what a branching graph would have to index, measured.

A branching graph / Bratteli diagram records the multiplicities with which the
irreducibles of A_k restrict to A_{k-1}.  Brown 2000 says of this class of
semigroups, in his own abstract and introduction, that their irreducible
representations "can be worked out explicitly (they are all 1-dimensional)".

Measured here directly from the multiplication table, without using that
theorem: in characteristic zero the radical of a finite-dimensional algebra is
the radical of the trace form (Dickson), so

    dim kF(P)/rad kF(P) = rank of the Gram matrix  G[x][y] = tr(L_{x.y}),

and for a band tr(L_s) = #{z in F(P) : s.z = z}, which is a counting problem.
The measurement is: that rank equals |AC(P)| on every poset tested.

Consequence, and it is the whole point of the test: the semisimple quotient has
|AC(P)| one-dimensional blocks, so a Bratteli diagram built from this algebra
carries no multiplicity data at all -- its vertex set is the support lattice and
every branching multiplicity available is 0 or 1 by construction.
"""

import sys
from core_af28 import poset_classes, moves_from_chains, move_product, AC, rank_exact

OUT = sys.stdout


def gram(F):
    idx = {x: i for i, x in enumerate(F)}
    m = len(F)
    prod = [[0] * m for _ in range(m)]
    for i, x in enumerate(F):
        for j, y in enumerate(F):
            prod[i][j] = idx[move_product(x, y)]
    fix = [0] * m
    for i in range(m):
        fix[i] = sum(1 for j in range(m) if prod[i][j] == j)
    return [[fix[prod[i][j]] for j in range(m)] for i in range(m)]


def t5(maxn=6, cap=1200):
    print("=" * 78, file=OUT)
    print("T5  dim kF(P)/rad = |AC(P)|, and hence all irreducibles are", file=OUT)
    print("    1-dimensional: measured from the multiplication table via the", file=OUT)
    print("    trace form.  Size cap on |F(P)|: %d (skips are listed, not hidden)."
          % cap, file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    print("   n  classes  tested  skipped   rank(G) != |AC(P)|", file=OUT)
    skipped = []
    total_bad = 0
    for n in range(1, maxn + 1):
        cls = poset_classes(n)
        tested = bad = 0
        sk = 0
        for up in cls:
            F = moves_from_chains(up)
            if len(F) > cap:
                sk += 1
                skipped.append((n, len(F)))
                continue
            G = gram(F)
            r = rank_exact(G)
            a = len(AC(up, F))
            tested += 1
            if r != a:
                bad += 1
                print("      BAD n=%d |F|=%d rank=%d |AC|=%d" % (n, len(F), r, a), file=OUT)
        total_bad += bad
        print("  %2d  %7d  %6d  %7d   %18d" % (n, len(cls), tested, sk, bad), file=OUT)
    print(file=OUT)
    if skipped:
        print("  Skipped (|F(P)| over the cap), listed in full:", file=OUT)
        from collections import Counter
        for (n, size), c in sorted(Counter(skipped).items()):
            print("      n=%d  |F(P)|=%d  x%d" % (n, size, c), file=OUT)
    else:
        print("  Nothing skipped.", file=OUT)
    print(file=OUT)
    print("  How far from semisimple, since that is the hypothesis the", file=OUT)
    print("  Okounkov-Vershik programme runs on (an inductive family of", file=OUT)
    print("  SEMISIMPLE algebras): dim kF(P) = |F(P)|, dim rad = |F(P)|-|AC(P)|.", file=OUT)
    print("   n   P            |F(P)|   |AC(P)|   dim rad   rad / dim", file=OUT)
    for n in range(2, maxn + 1):
        for name, up in (("antichain", tuple([0] * n)),
                         ("chain", tuple(sum(1 << k for k in range(i + 1, n))
                                         for i in range(n)))):
            F = moves_from_chains(up)
            a = len(AC(up, F))
            print("  %2d   %-10s %7d   %7d   %7d   %8.3f"
                  % (n, name, len(F), a, len(F) - a, (len(F) - a) / len(F)), file=OUT)
    print(file=OUT)
    print("  Reading: the semisimple quotient of kF(P) is a product of |AC(P)|", file=OUT)
    print("  copies of the field.  Whatever branching graph one builds from this", file=OUT)
    print("  family, its vertices are the elements of a support lattice and its", file=OUT)
    print("  edge multiplicities are not the invariant the programme is about.", file=OUT)
    print(file=OUT)
    return total_bad, len(skipped)


if __name__ == "__main__":
    bad, sk = t5()
    print("=" * 78, file=OUT)
    print("SUMMARY t_lrb_reps: %d bad, %d classes skipped over the size cap"
          % (bad, sk), file=OUT)
    print("=" * 78, file=OUT)
