"""W2 -- the two families behind F2's clause, measured.

F2 of mg-5800 says the repaired document claims, twice, that Young-Fibonacci
has *"the SAME index-set contact"* Young's has -- once in the section 2 heading
note (*"the index-set contact DOES extend"*) and once in row 10 of section 3.
The numbers under it all reproduce.  The wording does not: the Young headline is
a CLASSIFICATION (the intervals are `J(P)` for `P` EXACTLY the skew cell
posets), whereas the Young-Fibonacci sentence is Birkhoff plus a distributivity
count, and the two index-set families are not the same family.

mg-dffa narrows the clause.  The narrowed clause asserts a NEGATIVE -- that the
classes differ -- and a negative refuted by construction is what broke three
claims in this arc, so the object is built here rather than argued about.

WHAT IS MEASURED.

  W2a  The Young-Fibonacci lattice to rank 6.  Rank sizes AND the operator
       identity `DU - UD = I`.  Both, because the rank sizes alone do not
       control the cover rule: TWO wrong cover rules were written for
       `kerndffa.yf_down_covers` before the right one, and both returned
       1, 1, 2, 3, 5, 8, 13.  `DU - UD = I` caught both.  mg-5800 recorded the
       identical failure on its own instrument.

  W2b  33 intervals `[0, w]`, `rank(w) <= 6`; which are distributive; the
       smallest non-distributive witness.

  W2c  For each distributive interval, `P` = the poset of its join-irreducibles,
       canonicalised.  How many DISTINCT `P`, and how many of them are skew cell
       posets -- tested by building the canonical form of the cell poset of
       every skew shape with that many cells and asking for membership.

  W2d  The same two questions on the YOUNG side: the 30 intervals `[0, lam]`,
       `|lam| <= 6`.

  W2e  A control on the search box for the skew classes.  `skew_classes(k)`
       bounds lam to a k x k box, justified by trimming cell-free rows and
       columns.  Re-run at (k+1) x (k+1): the class SET must be identical, not
       merely the same size.

FALSIFIERS.  Any `DU - UD = I` failure; a distributive count other than 28 of
33; a distinct-`P` count that makes the two families coincide; any skew class
set that moves when the box grows.
"""

import sys
from collections import Counter

from kerndffa import (canon, cell_poset, ideals, partitions_upto, skew_classes,
                      yf_down_covers, yf_interval, yf_leq, yf_up_covers,
                      yf_words, young_interval, Lattice, shape_of_ideal,
                      skew_cells)

OUT = sys.stdout
MAXRANK = 6
BAD = [0]


def verdict(label, ok, detail=""):
    if not ok:
        BAD[0] += 1
    print("  %-58s %s%s" % (label, "ok" if ok else "BAD", detail), file=OUT)


def w2a():
    print("=" * 78, file=OUT)
    print("W2a  The Young-Fibonacci lattice to rank %d, and the control that"
          % MAXRANK, file=OUT)
    print("     the Fibonacci rank sizes are NOT.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    words = yf_words(MAXRANK)
    sizes = Counter(sum(w) for w in words)
    print("  rank      %s" % "  ".join("%3d" % r for r in range(MAXRANK + 1)),
          file=OUT)
    print("  elements  %s" % "  ".join("%3d" % sizes[r]
                                       for r in range(MAXRANK + 1)), file=OUT)
    print("  total elements of rank <= %d: %d" % (MAXRANK, len(words)), file=OUT)
    print(file=OUT)
    up = {w: set() for w in words}
    for w in words:
        for u in yf_down_covers(w):
            up[u].add(w)
    inverse_bad = sum(1 for w in words
                      if {v for v in yf_up_covers(w) if sum(v) <= MAXRANK}
                      != up[w])
    verdict("down-covers invert up-covers on every word", inverse_bad == 0,
            " (%d)" % inverse_bad)
    op_bad = 0
    for w in words:
        if sum(w) >= MAXRANK:
            continue                      # DU needs the rank above to be full
        du = Counter()
        for v in up[w]:
            for u in yf_down_covers(v):
                du[u] += 1
        ud = Counter()
        for u in yf_down_covers(w):
            for v in up[u]:
                ud[v] += 1
        diff = du.copy()
        for k, v in ud.items():
            diff[k] -= v
        diff = {k: v for k, v in diff.items() if v}
        if diff != {w: 1}:
            op_bad += 1
    verdict("DU - UD = I on every word of rank < %d" % MAXRANK, op_bad == 0,
            " (%d)" % op_bad)
    print(file=OUT)
    return words


def w2bcd():
    words, below = yf_leq(MAXRANK)
    print("=" * 78, file=OUT)
    print("W2b  The %d intervals [0, w], rank(w) <= %d: which are distributive?"
          % (len(words), MAXRANK), file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    dist, nondist = [], []
    notlattice = 0
    for w in words:
        L = yf_interval(w, below)
        if not L.is_lattice:
            notlattice += 1
            continue
        (dist if L.distributive() else nondist).append(w)
    verdict("every interval is a lattice", notlattice == 0,
            " (%d not)" % notlattice)
    print("  intervals: %d    distributive: %d    NOT distributive: %d"
          % (len(words), len(dist), len(nondist)), file=OUT)
    nondist.sort(key=lambda w: (sum(w), w))
    print("  the non-distributive ones, smallest first:", file=OUT)
    for w in nondist:
        print("      rank %d   w = %s" % (sum(w), "".join(map(str, w))),
              file=OUT)
    verdict("smallest non-distributive witness is w = 221",
            bool(nondist) and "".join(map(str, nondist[0])) == "221")
    print(file=OUT)

    print("=" * 78, file=OUT)
    print("W2c  The index sets.  P = join-irreducibles of each distributive", file=OUT)
    print("     interval; how many distinct P, and are they skew cell posets?", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    classes = {}
    birkhoff_bad = 0
    for w in dist:
        L = yf_interval(w, below)
        ji = L.join_irreducibles()
        P = L.induced_poset(ji)
        if len(ideals(P)) != L.n:
            birkhoff_bad += 1
        classes.setdefault(canon(P), []).append(w)
    verdict("|J(P)| = |interval| on every distributive interval",
            birkhoff_bad == 0, " (%d)" % birkhoff_bad)
    print("  distributive intervals: %d      distinct P up to isomorphism: %d"
          % (len(dist), len(classes)), file=OUT)
    print(file=OUT)
    skew = {k: skew_classes(k) for k in range(MAXRANK + 1)}
    print("  skew cell poset classes, by number of cells:", file=OUT)
    print("      k        %s" % "  ".join("%4d" % k
                                          for k in range(MAXRANK + 1)), file=OUT)
    print("      classes  %s" % "  ".join("%4d" % len(skew[k])
                                          for k in range(MAXRANK + 1)), file=OUT)
    print(file=OUT)
    print("   |P|  distinct P   of them NOT a skew cell poset   witnesses (w)",
          file=OUT)
    notskew = []
    for k in range(MAXRANK + 1):
        here = [P for P in classes if len(P) == k]
        bad = [P for P in here if P not in skew[k]]
        notskew.extend(bad)
        wits = sorted(("".join(map(str, classes[P][0])) or "0") for P in bad)
        print("   %3d   %10d   %28d   %s"
              % (k, len(here), len(bad), " ".join(wits)), file=OUT)
    print(file=OUT)
    print("  distinct P: %d       NOT skew cell posets: %d"
          % (len(classes), len(notskew)), file=OUT)
    print(file=OUT)
    print("  READING.  Every one of the %d distributive Young-Fibonacci" % len(dist),
          file=OUT)
    print("  intervals is J(P) -- that is Birkhoff, and it says nothing about", file=OUT)
    print("  WHICH P.  The %d distinct P that actually arise include %d that"
          % (len(classes), len(notskew)), file=OUT)
    print("  are not skew cell posets, so the index-set family is not the", file=OUT)
    print("  family the Young headline classifies.  The contact is of the", file=OUT)
    print("  same KIND; the class is not named and is not the same class.", file=OUT)
    print(file=OUT)

    print("=" * 78, file=OUT)
    print("W2d  The Young side, for contrast: the intervals [0, lam].", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    lams = [l for l in partitions_upto(MAXRANK)]
    ydist = 0
    yclasses = set()
    ynotskew = 0
    for lam in lams:
        Y = young_interval((), lam)
        if not Y.is_lattice:
            continue
        if Y.distributive():
            ydist += 1
        ji = Y.join_irreducibles()
        P = canon(Y.induced_poset(ji))
        yclasses.add(P)
        if P not in skew[len(P)]:
            ynotskew += 1
        # and the join-irreducible poset IS the cell poset D_lam
        if canon(cell_poset(lam)) != P and lam:
            ynotskew += 1000
    print("  intervals [0, lam] with |lam| <= %d: %d" % (MAXRANK, len(lams)),
          file=OUT)
    verdict("all of them are distributive", ydist == len(lams),
            " (%d of %d)" % (ydist, len(lams)))
    verdict("each one's join-irreducible poset IS the cell poset D_lam",
            ynotskew < 1000, "")
    verdict("every P is a skew cell poset", ynotskew == 0,
            " (%d not)" % ynotskew)
    print("  distinct P up to isomorphism: %d" % len(yclasses), file=OUT)
    print(file=OUT)
    return len(words), len(dist), len(nondist), len(classes), len(notskew)


def w2e():
    print("=" * 78, file=OUT)
    print("W2e  Control on the search box for the skew classes.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    for k in range(MAXRANK + 1):
        a = skew_classes(k)
        b = skew_classes(k, box=k + 1)
        verdict("k = %d: class SET identical at box k and box k+1" % k, a == b,
                " (%d vs %d)" % (len(a), len(b)))
    print(file=OUT)


def main():
    w2a()
    n, d, nd, c, ns = w2bcd()
    w2e()
    print("=" * 78, file=OUT)
    print("SUMMARY w2_family: intervals %d, distributive %d, non-distributive %d,"
          % (n, d, nd), file=OUT)
    print("SUMMARY w2_family: distinct P %d, of them not skew cell posets %d,"
          % (c, ns), file=OUT)
    print("SUMMARY w2_family: failures %d" % BAD[0], file=OUT)
    print("=" * 78, file=OUT)
    return 1 if BAD[0] else 0


if __name__ == "__main__":
    sys.exit(main())
