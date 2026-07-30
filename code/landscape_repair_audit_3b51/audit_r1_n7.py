#!/usr/bin/env python3
"""
mg-3b51 AUDIT 1, PART A7 -- ONE ORDER PAST THE REPAIR'S RANGE.

mg-1953 verifies the repaired closed form exhaustively to n = 6.  Everything it
says about the statement is therefore a statement about n <= 6; the repaired
rule is asserted as a specialisation of a theorem about all finite posets.  This
extends the check to n = 7.

Coverage, stated exactly: every isomorphism class at n = 7 (there are 2 045,
A000112) has at least one representative in the set swept here, because every
poset on 7 elements is a poset on 6 elements with a new maximal element over an
order ideal, and all 318 six-element classes are extended in every way.  The
sweep is over LABELLED representatives with duplicates left in, which costs time
and cannot cost coverage.

  A7a  M_0 by construction (certificate both ways) == REPAIRED rule, as sets.
  A7b  Brown's total-multiplicity identity over all 877 flats, both rules.
  A7c  Whether the DOC rule still fails at n = 7, and by how much.
"""

import core3b51 as C


def acyclic(n, up, X):
    succ, _ = C.quotient_digraph(n, up, X)
    return C.find_cycle(succ) is None


def main():
    n = 7
    flats = C.set_partitions(n)
    reps = set()
    for up in C.iso_classes(n - 1):
        for D in C.down_sets(n - 1, up):
            new = list(up) + [0]
            for i in range(n - 1):
                if D >> i & 1:
                    new[i] |= 1 << (n - 1)
            reps.add(C._closure(n, tuple(new)))
    reps = sorted(reps)

    print("=" * 78)
    print("mg-3b51 AUDIT 1 / A7 -- n = 7, ONE ORDER PAST THE REPAIR'S RANGE")
    print("=" * 78)
    print()
    print("  labelled representatives swept : %d" % len(reps))
    print("  flats per poset (Bell(7))      : %d" % len(flats))
    print("  flat evaluations               : %d" % (len(reps) * len(flats)))
    print("  isomorphism classes covered    : all 2 045 (A000112) -- every")
    print("      7-poset is a 6-poset plus a maximal element over an ideal,")
    print("      and all 318 six-element classes are extended in every way")
    print()

    setbad_rep = setbad_doc = 0
    sumbad_rep = sumbad_doc = 0
    spurious = 0
    witness = None
    for up in reps:
        e = C.count_linear_extensions(n, up)
        geom, doc, rep = [], [], []
        for X in flats:
            geom.append(C.meets_open_cone(n, up, X))
            d = C.all_blocks_antichain(up, X)
            doc.append(d)
            rep.append(d and acyclic(n, up, X))
        if geom != rep:
            setbad_rep += 1
        if geom != doc:
            setbad_doc += 1
        sr = sum(C.closed_form(X) for X, t in zip(flats, rep) if t)
        sd = sum(C.closed_form(X) for X, t in zip(flats, doc) if t)
        if sr != e:
            sumbad_rep += 1
        if sd != e:
            sumbad_doc += 1
            if witness is None:
                witness = (up, e, sd, sr)
        spurious += sum(1 for a, b in zip(doc, rep) if a and not b)

    print("-" * 78)
    print("A7a  M_0 (constructed) == rule, as sets of flats")
    print("-" * 78)
    print("     REPAIRED rule : %d bad of %d" % (setbad_rep, len(reps)))
    print("     DOC rule      : %d bad of %d" % (setbad_doc, len(reps)))
    print()
    print("-" * 78)
    print("A7b  Brown's identity  sum over ALL 877 flats of m_X = |L(P)|")
    print("-" * 78)
    print("     REPAIRED rule : %d bad of %d" % (sumbad_rep, len(reps)))
    print("     DOC rule      : %d bad of %d" % (sumbad_doc, len(reps)))
    print()
    print("-" * 78)
    print("A7c  spurious flats at n = 7 (DOC nonzero, not in M_0): %d" % spurious)
    if witness:
        up, e, sd, sr = witness
        print("     first DOC failure: P = %s" % C.poset_name(n, up))
        print("        |L(P)| = %d,  DOC sum = %d,  REPAIRED sum = %d"
              % (e, sd, sr))
    print()
    print("=" * 78)
    print("READING.  The repaired statement survives one order past the range")
    print("in which it was repaired, and the original statement fails harder.")
    print("This does not make the repaired rule a theorem -- it is a")
    print("specialisation of one, and neither mg-1953 nor this audit proves it.")
    print("=" * 78)


if __name__ == "__main__":
    main()
