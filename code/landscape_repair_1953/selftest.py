#!/usr/bin/env python3
"""
mg-1953 REPAIR instrument -- SELF-TEST, IN BOTH DIRECTIONS.

The constants below are transcribed from
docs/OneThird-Landscape-Where-This-Lives.md.  This file asserts them against
BOTH sides, so a drift on either side fails:

  instruments -> constants   the enumeration against externally-known
                             sequences (A000112, A000522, A000670), so a
                             silent regression in the poset machinery cannot
                             pass, and every headline number section 8 writes,
                             recomputed here.

  constants -> document      document_figures.py READS the markdown and
                             extracts the same figures from the sentences and
                             table rows carrying them; every one is asserted
                             against the same constant.  An edit to a number
                             in the document, or a rewrite that deletes the
                             sentence a figure lives in, FAILS HERE.

The second direction was missing until mg-aec7 added it on mg-3b51's A3: the
self-test was billed as failing "if the document and the instruments ever
drift apart" while never reading the document, so an edit to the document
passed silently.  Its coverage is bounded and the boundary is stated in
document_figures.py -- the listed figures, not the whole file.

Run to n = 5 by default (~3 s); pass 6 for the full range (~30 s).  The
document direction runs in full at every nmax; where a constant it pins has
not itself been recomputed at this nmax, that is printed rather than assumed.
"""

import sys

import document_figures
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


def check_doc(name, want):
    """Assert a figure READ OUT OF THE DOCUMENT against the constant."""
    got = DOC_FIGURES.get(name)
    if got is None:
        print("  %-58s %-14s %s"
              % (name, "NOT FOUND", "FAIL -- the sentence carrying it is gone"))
        FAILURES.append("document: %s" % name)
        return
    ok = got == want
    print("  %-58s %-30s %s"
          % ("%s (%s)" % (name, document_figures.where(name)),
             " ".join(str(g) for g in got),
             "OK" if ok else "FAIL want %s" % (want,)))
    if not ok:
        FAILURES.append("document: %s" % name)


# ---------------------------------------------------------------------------
# THE CONSTANTS.  Transcribed from the document; asserted against the
# instruments below and against the document itself in the final stage.
# ---------------------------------------------------------------------------
A000112 = {1: 1, 2: 2, 3: 5, 4: 16, 5: 63, 6: 318}       # posets up to iso
A000670 = {1: 1, 2: 3, 3: 13, 4: 75, 5: 541}             # ordered Bell
A000522 = {1: 2, 2: 5, 3: 16, 4: 65, 5: 326}             # sum n!/(n-k)!

WANT_DOC_BAD = {2: 0, 3: 0, 4: 1, 5: 10, 6: 101}
WANT_SPURIOUS = {2: 0, 3: 0, 4: 1, 5: 18, 6: 455}
WANT_LEVELS = {1: 1, 2: 4, 3: 24, 4: 206, 5: 2353, 6: 37029}
WANT_ZERO = {2: 1, 3: 11, 4: 125, 5: 1674, 6: 28988}
WANT_MOVES = {1: 1, 2: 5, 3: 37, 4: 397, 5: 5757}
WANT_PAIRS = {1: 1, 2: 13, 3: 321, 4: 13853, 5: 922073}

CLASSES_2_TO_6 = sum(A000112[n] for n in range(2, 7))        # 404, E3
CLASSES_3_TO_6 = sum(A000112[n] for n in range(3, 7))        # 402, P2
CLASSES_TO_5 = sum(A000112[n] for n in range(1, 6))          # 87, E1
PAIRS_TO_5 = sum(WANT_PAIRS[n] for n in range(1, 6))         # 936 261, E1
MOVES_TO_5 = sum(WANT_MOVES[n] for n in range(1, 6))         # 6 197
# R3's population is 2 <= n <= 6 -- check_R3's own range, the same range E3's
# 404 classes are counted over, and the by-n list the document prints beside
# the total starts at n = 2.  (n = 1 contributes the one trivial level.)
LEVELS_2_TO_6 = sum(WANT_LEVELS[n] for n in range(2, 7))     # 39 616, R3
FLATS_AT_6 = 203 * A000112[6]                                # Bell(6) x classes

DOC_FIGURES = document_figures.extract()


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print("mg-1953 self-test, n <= %d" % nmax)
    print()

    print("EXTERNAL SEQUENCES -- the enumeration is not self-certified")
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
    flats_at_6 = 0
    for n in range(2, nmax + 1):
        s = analyse(n)
        if n == 6:
            flats_at_6 = s['flats']
        check("n=%d posets where the ORIGINAL rule breaks Brown's (10)" % n,
              s['doc_sum_bad'], WANT_DOC_BAD[n])
        check("n=%d posets where the REPAIRED rule breaks Brown's (10)" % n,
              s['rep_sum_bad'], 0)
        check("n=%d spurious flats under the ORIGINAL rule" % n,
              s['spurious'], WANT_SPURIOUS[n])
        check("n=%d M_0 (built geometrically) != original rule" % n,
              s['geom_vs_doc_bad'], WANT_DOC_BAD[n])
        check("n=%d M_0 (built geometrically) != REPAIRED rule" % n,
              s['geom_vs_rep_bad'], 0)
        # R1d.  NOT A CONTROL -- it cannot fail while the repaired rule passes.
        # Asserted because the document states it as an identity, and a stated
        # identity should be exhibited.  mg-3b51 A1.
        check("n=%d R1d IDENTITY (not a control): doc & AC(P) != repaired" % n,
              s['doc_ne_rep_onAC'], 0)
        check("n=%d R1d, its consequence: original rule summed on AC(P)" % n,
              s['doc_sum_bad_onAC'], 0)
    if nmax >= 6:
        check("n=6 flats evaluated (Bell(6) x 318)", flats_at_6, FLATS_AT_6)
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
    for n in range(2, nmax + 1):
        s = check_R3(n)
        check("n=%d levels" % n, s['levels'], WANT_LEVELS[n])
        check("n=%d DISAGREEING levels (repo solve vs Brown)" % n,
              s['disagreements'], 0)
        check("n=%d levels named zero a priori" % n,
              s['zero_levels'], WANT_ZERO[n])
    print()

    print("R4 -- the populations the corrected sentences are about")
    cum_cls = cum_pairs = cum_moves = 0
    for n in range(1, nmax + 1):
        r = check_R4(n)
        cum_cls += r['classes']
        cum_pairs += r['pairs']
        cum_moves += r['moves']
        if n <= 5:
            check("n=%d moves" % n, r['moves'], WANT_MOVES[n])
            check("n=%d product pairs" % n, r['pairs'], WANT_PAIRS[n])
        if n == 5:
            check("n <= 5 classes (document said 63)", cum_cls, CLASSES_TO_5)
            check("n <= 5 product pairs (document said 922 073)",
                  cum_pairs, PAIRS_TO_5)
            check("n <= 5 moves", cum_moves, MOVES_TO_5)
        if n == 6:
            check("2 <= n <= 6 classes, E3's population (said 405)",
                  cum_cls - 1, CLASSES_2_TO_6)
            check("3 <= n <= 6 classes, P2's population (said 405)",
                  cum_cls - 1 - 2, CLASSES_3_TO_6)
    print()

    # -----------------------------------------------------------------------
    # THE OTHER DIRECTION.  Everything above compares the INSTRUMENTS with the
    # constants.  This compares the DOCUMENT with the same constants, by
    # reading it.  mg-3b51 A1/A3.
    # -----------------------------------------------------------------------
    print("THE DOCUMENT ITSELF -- figures read out of %s"
          % document_figures.DOCUMENT.split("/docs/")[-1])
    if nmax < 6:
        print("  (constants for n = 6 are pinned by the document here but were")
        print("   not recomputed at nmax = %d -- run with 6 for both sides)" % nmax)
    levels_by_n = tuple(WANT_LEVELS[n] for n in range(2, 7))

    check_doc("s0 E1 populations", (CLASSES_TO_5, PAIRS_TO_5, CLASSES_TO_5))
    check_doc("s0 Brown levels", (WANT_LEVELS[6],))
    check_doc("s2 two-sided comparison", (LEVELS_2_TO_6, levels_by_n))
    check_doc("s2 levels named zero",
              (WANT_ZERO[6], WANT_LEVELS[6], WANT_ZERO[5], WANT_LEVELS[5]))
    check_doc("s3.2 n=6 row", (A000112[6], WANT_LEVELS[6], A000112[6]))
    check_doc("s3.3 n<=5 total row",
              (CLASSES_TO_5, MOVES_TO_5, CLASSES_TO_5, PAIRS_TO_5))
    check_doc("s3.3 move counts",
              (tuple(WANT_MOVES[n] for n in range(1, 6)),))
    check_doc("R1a geometric vs the two rules",
              (A000112[6],
               WANT_DOC_BAD[4], A000112[4],
               WANT_DOC_BAD[5], A000112[5],
               WANT_DOC_BAD[6], A000112[6]))
    check_doc("R1b flats and spurious", (FLATS_AT_6, WANT_SPURIOUS[6]))
    check_doc("R1c the witness", (6, 7))
    check_doc("R1d the identity",
              (CLASSES_2_TO_6, CLASSES_2_TO_6, A000112[6]))
    check_doc("R2 E8 columns", (A000112[5], A000112[5], A000112[5]))
    check_doc("R2 band vs F(P) at the antichain",
              (A000522[2], A000670[2], A000522[3], A000670[3]))
    check_doc("R3 two-sided comparison",
              (LEVELS_2_TO_6, levels_by_n, CLASSES_2_TO_6))
    check_doc("R3 levels named zero",
              (WANT_ZERO[6], WANT_LEVELS[6], WANT_ZERO[5], WANT_LEVELS[5]))
    check_doc("R4 the corrected populations",
              (CLASSES_2_TO_6, CLASSES_3_TO_6))
    check_doc("R4 rebuilt populations",
              (tuple(A000112[n] for n in range(1, 7)),
               tuple(WANT_MOVES[n] for n in range(1, 6)),
               MOVES_TO_5,
               tuple(WANT_LEVELS[n] for n in range(1, 7)),
               tuple(WANT_PAIRS[n] for n in range(1, 6)),
               PAIRS_TO_5))
    print()

    if FAILURES:
        print("SELF-TEST FAILED: %d checks" % len(FAILURES))
        for f in FAILURES:
            print("   %s" % f)
        return 1
    print("SELF-TEST PASSED -- every number the document carries is reproduced,")
    print("and every figure listed in document_figures.py was found IN the")
    print("document and agrees.  Both directions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
