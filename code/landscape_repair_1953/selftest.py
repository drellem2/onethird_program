#!/usr/bin/env python3
"""
mg-1953 REPAIR instrument -- SELF-TEST.

Asserts (a) the enumeration against externally-known sequences, so a silent
regression in the poset machinery cannot pass, and (b) every headline number
mg-1953 writes into docs/OneThird-Landscape-Where-This-Lives.md.  A failure
here means the document and the instruments have drifted apart.

Run to n = 5 by default (~3 s); pass 6 for the full range (~30 s).
"""

import sys

from core1953 import (iso_classes, set_partitions, linear_extensions,
                      blocks_are_antichains, quotient_is_acyclic,
                      meets_the_open_order_cone, transitive_closure, label)
from closed_form_outside_AC import analyse, multiplicity
from repaired_claims import (check_R2, check_R3, check_R4, feasible_words,
                             F_of_P, phi, greedy_product, product)

FAILURES = []


def check(name, got, want):
    ok = got == want
    print("  %-58s %-14s %s" % (name, got, "OK" if ok else "FAIL want %s" % (want,)))
    if not ok:
        FAILURES.append(name)


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print("mg-1953 self-test, n <= %d" % nmax)
    print()

    print("EXTERNAL SEQUENCES -- the enumeration is not self-certified")
    A000112 = {1: 1, 2: 2, 3: 5, 4: 16, 5: 63, 6: 318}       # posets up to iso
    A000670 = {1: 1, 2: 3, 3: 13, 4: 75, 5: 541}             # ordered Bell
    A000522 = {1: 2, 2: 5, 3: 16, 4: 65, 5: 326}             # sum n!/(n-k)!
    for n in range(1, nmax + 1):
        check("A000112 isomorphism classes at n=%d" % n,
              len(iso_classes(n)), A000112[n])
    for n in range(1, min(nmax, 5) + 1):
        check("A000670 |F(antichain)| at n=%d" % n,
              len(F_of_P(n, frozenset())), A000670[n])
        check("A000522 |free LRB| at n=%d" % n,
              len(feasible_words(n, frozenset())), A000522[n])
    print()

    print("R1 -- the closed form OUTSIDE AC(P) (the repaired clause)")
    want_doc_bad = {2: 0, 3: 0, 4: 1, 5: 10, 6: 101}
    want_spurious = {2: 0, 3: 0, 4: 1, 5: 18, 6: 455}
    for n in range(2, nmax + 1):
        s = analyse(n)
        check("n=%d posets where the ORIGINAL rule breaks Brown's (10)" % n,
              s['doc_sum_bad'], want_doc_bad[n])
        check("n=%d posets where the REPAIRED rule breaks Brown's (10)" % n,
              s['rep_sum_bad'], 0)
        check("n=%d spurious flats under the ORIGINAL rule" % n,
              s['spurious'], want_spurious[n])
        check("n=%d M_0 (built geometrically) != original rule" % n,
              s['geom_vs_doc_bad'], want_doc_bad[n])
        check("n=%d M_0 (built geometrically) != REPAIRED rule" % n,
              s['geom_vs_rep_bad'], 0)
        check("n=%d CONTROL: original rule restricted to AC(P)" % n,
              s['doc_sum_bad_onAC'], 0)
    print()

    print("R1c -- the witness, named in the document")
    rel = transitive_closure(4, {(0, 2), (1, 3)})            # P = {a<c, b<d}
    flats = set_partitions(4)
    e = len(linear_extensions(4, rel))
    doc = sum(multiplicity(X) for X in flats if blocks_are_antichains(rel, X))
    rep = sum(multiplicity(X) for X in flats
              if blocks_are_antichains(rel, X) and quotient_is_acyclic(rel, X))
    spur = [X for X in flats if blocks_are_antichains(rel, X)
            and not quotient_is_acyclic(rel, X)]
    check("P = {a<c, b<d}: |L(P)|", e, 6)
    check("P = {a<c, b<d}: sum m under the ORIGINAL rule", doc, 7)
    check("P = {a<c, b<d}: sum m under the REPAIRED rule", rep, 6)
    check("P = {a<c, b<d}: the spurious flat", [label(X) for X in spur], ["ad|bc"])
    check("P = {a<c, b<d}: does that flat meet U?",
          meets_the_open_order_cone(rel, spur[0]), False)
    print()

    print("R2 -- E8: homomorphic image, proper for n >= 3")
    for n in range(2, min(nmax, 5) + 1):
        rows = check_R2(n)
        N = len(rows)
        check("n=%d the word->move map is a HOMOMORPHISM" % n,
              sum(r['hom'] for r in rows), N)
        check("n=%d its image lies in F(P)" % n,
              sum(r['image_inside'] for r in rows), N)
        check("n=%d its image is closed under the product" % n,
              sum(r['image_closed'] for r in rows), N)
        check("n=%d the map is INJECTIVE (must be 0 -- never)" % n,
              sum(r['injective'] for r in rows), 0)
        check("n=%d the image is a PROPER submonoid" % n,
              sum(r['proper'] for r in rows), 0 if n == 2 else N)
    print()

    print("R3 -- 'sharper' as a two-sided comparison (must be 0 everywhere)")
    want_levels = {2: 4, 3: 24, 4: 206, 5: 2353, 6: 37029}
    want_zero = {2: 1, 3: 11, 4: 125, 5: 1674, 6: 28988}
    for n in range(2, nmax + 1):
        s = check_R3(n)
        check("n=%d levels" % n, s['levels'], want_levels[n])
        check("n=%d DISAGREEING levels (repo solve vs Brown)" % n,
              s['disagreements'], 0)
        check("n=%d levels named zero a priori" % n,
              s['zero_levels'], want_zero[n])
    print()

    print("R4 -- the populations the corrected sentences are about")
    want_moves = {1: 1, 2: 5, 3: 37, 4: 397, 5: 5757}
    want_pairs = {1: 1, 2: 13, 3: 321, 4: 13853, 5: 922073}
    cum_cls = cum_pairs = cum_moves = 0
    for n in range(1, nmax + 1):
        r = check_R4(n)
        cum_cls += r['classes']
        cum_pairs += r['pairs']
        cum_moves += r['moves']
        if n <= 5:
            check("n=%d moves" % n, r['moves'], want_moves[n])
            check("n=%d product pairs" % n, r['pairs'], want_pairs[n])
        if n == 5:
            check("n <= 5 classes (document said 63)", cum_cls, 87)
            check("n <= 5 product pairs (document said 922 073)",
                  cum_pairs, 936261)
            check("n <= 5 moves", cum_moves, 6197)
        if n == 6:
            check("2 <= n <= 6 classes, E3's population (said 405)",
                  cum_cls - 1, 404)
            check("3 <= n <= 6 classes, P2's population (said 405)",
                  cum_cls - 1 - 2, 402)
    print()

    if FAILURES:
        print("SELF-TEST FAILED: %d checks" % len(FAILURES))
        for f in FAILURES:
            print("   %s" % f)
        return 1
    print("SELF-TEST PASSED -- every number the document carries is reproduced.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
