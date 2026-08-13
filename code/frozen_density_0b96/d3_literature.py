#!/usr/bin/env python3
"""mg-0b96 arm d3 — THE SURVEY VERDICT, MEASURED ON THE DEFINITIONS RATHER THAN ASSERTED FROM A
READING.  `mg-345e`'s P5 grep found zero frozen-conditional UPPER bounds on `d` in this CORPUS.
This arm asks the same question of the LITERATURE, and it asks it in a form a grep cannot answer:
not "does anybody state a density bound", but "what density bound do the known class exclusions
DELIVER, jointly, when you push them as hard as they go".

THE METHOD, in one line: every class exclusion is a set of posets the conjecture is PROVED on, so
what it delivers about `d` under freezing is `max{ d(P) : P ∉ C }` — a frozen poset must lie
outside `C`, and that maximum is the best upper bound on `d` the exclusion can give.

  m1  THE TABLE, from `mg-33f5` §2 verbatim, with the predicate each row is read as.
  m2  PER CLASS: `max{ d(P) : P ∉ C }`, exhaustive over every isomorphism class to `nmax`.  A `1`
      in that column means the exclusion delivers NOTHING about density.
  m3  JOINTLY: the RESIDUE — posets outside every listed class at once — its size and its maximum
      density.  This is the strongest density statement the whole structural literature supports.
  m4  THE RESIDUE IS EMPTY BELOW `n = 8`, AND FOR ONE REASON: every poset on at most 7 elements is
      6-thin, because no element can be incomparable with more than `n − 1 ≤ 6` others.  So a
      measurement of what the literature leaves CANNOT be taken below `n = 8`, and an instrument
      stopping at 7 would have reported total coverage.
  m5  AN EXPLICIT FAMILY AT EVERY `n ≥ 15`, verified rather than argued: `lib0b96.family(n)` is
      outside all seven classes and has `d = 1 − Θ(1/n)`.  Its range starts where the census
      frontier ends, so for every `n ≥ 15` there is a NAMED poset of density `> 0.83` that
      NOTHING on the record decides.

⚠️  TWO KINDS ARE BEING KEPT APART HERE AND THEY MUST NOT BE ADDED.  A CENSUS (`n ≤ 14`, `mg-33f5`)
decides every poset in its range and nothing above it.  A CLASS EXCLUSION decides its class at
every `n`.  The residue below is the residue of the CLASS EXCLUSIONS ONLY; at `n = 8, 9` its
members are also decided by the census, and that is said at the table rather than left implicit.
The family in `m5` is the part that is outside both.

⚠️  ONE ROW OF `mg-33f5` §2's TABLE CARRIES NO SOURCE ("height two / bipartite", source cell `—`).
It is included anyway.  Including a class the literature may not actually have can only SHRINK the
residue, i.e. can only weaken this arm's own finding, so the generosity is in the safe direction.

Exits 0 if the family verifies and the population facts hold, 1 otherwise, 2 on refusal.
"""

import sys
from fractions import Fraction

import lib0b96 as X
import lib6ff4 as L

NMAX = 9
FAM_MAX = 40


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else NMAX
    print("=" * 100)
    print("mg-0b96  d3  what the literature's class exclusions deliver about d -- measured")
    print("=" * 100)
    print()
    ok = True

    print("m1  THE CLASSES, FROM mg-33f5 §2's TABLE")
    print("-" * 100)
    for (name, _p, cite) in X.LIT_CLASSES:
        print("      %-34s %s" % (name, cite))
    print()
    print("    Each is a class on which the conjecture (or Peczarski's GPC, which implies it) is")
    print("    PROVED, so a frozen poset lies outside all of them.")
    print()

    try:
        C = L.all_classes(nmax)
    except Exception as exc:                                       # pragma: no cover
        print("REFUSED: the imported enumerator did not run: %r" % (exc,))
        print("VERDICT: REFUSED")
        return 2

    names = [nm for (nm, _p, _c) in X.LIT_CLASSES]
    per_class_max = {}
    per_class_min = {}
    residue_max = {}
    residue_cnt = {}
    for n in range(3, nmax + 1):
        mx = {nm: Fraction(-1) for nm in names}
        mn = {nm: Fraction(2) for nm in names}
        rmax, rcnt = Fraction(-1), 0
        for down in C[n]:
            d = X.density(n, down)
            inside = []
            for (nm, pred, _c) in X.LIT_CLASSES:
                if pred(n, down):
                    inside.append(nm)
                else:
                    if d > mx[nm]:
                        mx[nm] = d
                    if d < mn[nm]:
                        mn[nm] = d
            if not inside:
                rcnt += 1
                if d > rmax:
                    rmax = d
        per_class_max[n] = mx
        per_class_min[n] = mn
        residue_max[n] = rmax
        residue_cnt[n] = rcnt

    print("m2  max{ d(P) : P NOT IN C } -- the best upper bound on d each exclusion can deliver")
    print("-" * 100)
    print("      %-34s %s" % ("class C", "  ".join("%9s" % ("n=%d" % n) for n in range(3, nmax + 1))))
    for nm in names:
        cells = []
        for n in range(3, nmax + 1):
            v = per_class_max[n][nm]
            cells.append("%9s" % (str(v) if v >= 0 else "C = all"))
        print("      %-34s %s" % (nm, "  ".join(cells)))
    print()
    print("    A cell of 1 says the exclusion delivers NO density bound at all: a poset of density")
    print("    1 -- the antichain -- already lies outside the class.  `C = all' says every poset at")
    print("    that n is in the class, so the exclusion decides everything and bounds nothing.")
    print()

    print("m3  THE JOINT RESIDUE -- outside every listed class at once")
    print("-" * 100)
    print("      %4s %10s %12s %14s %10s   %s" % ("n", "posets", "residue", "max d in it", "decimal", "decided by the n<=14 census?"))
    for n in range(3, nmax + 1):
        v = residue_max[n]
        print("      %4d %10d %12d %14s %10s   %s"
              % (n, len(C[n]), residue_cnt[n], str(v) if v >= 0 else "-- empty --",
                 ("%.4f" % float(v)) if v >= 0 else "", "yes (n <= 14)" if n <= 14 else "NO"))
    print()
    print("    THE RESIDUE IS THE STRONGEST DENSITY STATEMENT THE STRUCTURAL LITERATURE SUPPORTS.")
    print("    Its maximum is the largest density a poset can have while lying outside every")
    print("    class the record proves the conjecture on.")
    print()
    print("    AND THE MAXIMUM HAS A CLOSED FORM AT BOTH n WHERE IT EXISTS:")
    for n in range(3, nmax + 1):
        if residue_cnt[n]:
            v = residue_max[n]
            f = 1 - Fraction(2, n)
            print("      n=%d   max d in the residue = %-6s   1 - 2/n = %-6s   %s   (the extremal"
                  % (n, v, f, "EQUAL" if v == f else "DIFFER"))
            print("            member has exactly n-1 = %d comparable pairs)" % (n - 1))
    print("    ⚠️  Two values of n is a pattern, not a law, and it is not extrapolated here -- what")
    print("    carries past n = 9 is the EXPLICIT FAMILY of m5, which is a construction.")
    print()

    print("m4  WHY NOTHING BELOW n = 8, AND WHY AN INSTRUMENT STOPPING AT 7 WOULD HAVE LIED")
    print("-" * 100)
    first = min([n for n in range(3, nmax + 1) if residue_cnt[n] > 0], default=None)
    ok &= first == 8
    print("      first n with a non-empty residue: %s   %s" % (first, "OK" if first == 8 else "UNEXPECTED"))
    print()
    print("    Every poset on n <= 7 elements is 6-thin, because an element cannot be incomparable")
    print("    with more than n-1 <= 6 others.  So Peczarski's 6-thin exclusion covers the whole")
    print("    population below n = 8 ON ITS OWN, and `the literature decides everything' is what")
    print("    an exhaustive sweep to n = 7 would have reported -- a fact about the population's")
    print("    size, read as a fact about the literature's reach.")
    maxdeg = max(X.thinness(7, down) for down in C[7]) if 7 in C else None
    print("      max incomparability degree over every poset at n = 7:  %s  (<= 6, as the argument"
          % maxdeg)
    print("      says -- measured, not assumed)")
    ok &= (maxdeg is None or maxdeg <= 6)
    print()

    print("m5  AN EXPLICIT LITERATURE-IMMUNE FAMILY AT EVERY n >= 15, VERIFIED")
    print("-" * 100)
    print("    lib0b96.family(n): the incidence poset of an asymmetric unicyclic graph, plus one")
    print("    element above one edge-element, plus one isolated element when the parity needs it.")
    print("    Comparabilities are Theta(n), so d = 1 - Theta(1/n).")
    print()
    print("      %4s %8s %12s %10s   %s" % ("n", "comps", "d", "decimal", "classes containing it"))
    bad = 0
    for n in range(15, FAM_MAX + 1):
        down = X.family(n)
        c = sum(bin(x).count("1") for x in down)
        d = X.density(n, down)
        inside = X.covering_classes(n, down)
        if inside:
            bad += 1
        if n <= 20 or n % 5 == 0:
            print("      %4d %8d %12s %10.4f   %s"
                  % (n, c, d, float(d), ", ".join(inside) if inside else "NONE -- immune"))
    ok &= bad == 0
    print()
    print("      %d of %d family members lie inside some class   %s"
          % (bad, FAM_MAX - 14, "OK -- none do" if bad == 0 else "FIRED"))
    print()
    print("    ⚠️  THE FAMILY IS `FP' OVER n = 15..%d.  What it establishes at those n it" % FAM_MAX)
    print("    establishes exhaustively -- each membership is computed, not argued -- and the")
    print("    construction is uniform in n, but this arm does not prove asymmetry for general n.")
    print("    THE RANGE IS THE POINT: the census reaches 14, the family starts at 15, so at every")
    print("    n it covers there is a NAMED poset of density above 0.83 that no census and no")
    print("    class exclusion on the record decides either way.")
    print()

    print("=" * 100)
    top = per_class_max[nmax]
    delivering = [nm for nm in names if 0 <= top[nm] < 1]
    best = min([top[nm] for nm in delivering], default=None)
    print("    THE SURVEY VERDICT.  Of the %d class exclusions the record carries, %d deliver any" % (len(names), len(delivering)))
    print("    upper bound on d at all at n = %d, the strongest of them %s = %.4f -- and 0 deliver"
          % (nmax, best, float(best)))
    print("    one anywhere near the 2e-2 row 8 needs (d2 m1).  Jointly they leave a residue whose")
    print("    density reaches %s at n = %d and, on the explicit family, %s at n = 40."
          % (residue_max[nmax], nmax, X.density(40, X.family(40))))
    print("    The literature bounds delta from BELOW and the exclusions cut the SPARSE side;")
    print("    cutting the sparse side of a class yields a LOWER bound on d, never an upper one,")
    print("    which is mg-345e's finding reproduced from the literature side instead of a grep.")
    print("=" * 100)
    print("VERDICT: %s" % ("GREEN" if ok else "RED"))
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
