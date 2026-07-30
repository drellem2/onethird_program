#!/usr/bin/env python3
"""
mg-3b51 AUDIT -- SELF-TEST.

Two jobs, and the second is the one that matters:

  (a) certify this instrument against externally-known sequences, so that a
      silent regression in the poset or partition machinery cannot pass;

  (b) CROSS-VALIDATE THE TWO INDEPENDENT DECISION PROCEDURES for "does the flat
      X meet the open order cone U?".  This audit's primary route is numeric
      construction with a certificate both ways (longest-path potentials,
      verified against the defining equations and inequalities; a directed
      block-cycle on the negative side).  mg-1953's route is an exhaustive
      search over the |X|! orderings of the blocks.  Both are implemented here
      and compared flat by flat.  If they ever disagree, every number in this
      audit is suspect and the run fails loudly.

  (c) assert every number this audit's document carries.

Run with no argument for n <= 5 (~4 s); pass 6 for the full range (~25 s).
"""

import sys

import core3b51 as C
from audit_r1_offAC import sweep, acyclic, rule_doc, rule_rep
from audit_r3_r4 import spectrum_sweep, populations, moebius_pi

FAIL = []


def check(name, got, want):
    ok = got == want
    print("  %-62s %-12s %s" % (name, got, "OK" if ok else "FAIL want %s" % (want,)))
    if not ok:
        FAIL.append(name)


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print("mg-3b51 audit self-test, n <= %d" % nmax)
    print()

    print("(a) EXTERNAL SEQUENCES -- the enumeration is not self-certified")
    A000112 = {1: 1, 2: 2, 3: 5, 4: 16, 5: 63, 6: 318}
    A000110 = {1: 1, 2: 2, 3: 5, 4: 15, 5: 52, 6: 203}       # Bell
    A000670 = {1: 1, 2: 3, 3: 13, 4: 75, 5: 541}             # ordered Bell
    A000522 = {1: 2, 2: 5, 3: 16, 4: 65, 5: 326}             # sum n!/(n-k)!
    for n in range(1, nmax + 1):
        check("A000112 poset isomorphism classes at n=%d" % n,
              len(C.iso_classes(n)), A000112[n])
        check("A000110 set partitions (flats) at n=%d" % n,
              len(C.set_partitions(n)), A000110[n])
    from audit_r2_e8 import feasible_words
    for n in range(1, min(nmax, 5) + 1):
        anti = tuple(0 for _ in range(n))
        check("A000670 |F(antichain)| at n=%d" % n,
              len(C.moves_of(n, anti)), A000670[n])
        check("A000522 |greedoid band at the antichain| at n=%d" % n,
              len(feasible_words(n, anti)), A000522[n])
    print()

    print("(b) THE TWO DECISION PROCEDURES FOR 'X MEETS U', CROSS-VALIDATED")
    for n in range(1, min(nmax, 5) + 1):
        flats = C.set_partitions(n)
        bad = 0
        cells = 0
        for up in C.iso_classes(n):
            for X in flats:
                cells += 1
                if C.meets_open_cone(n, up, X) != \
                        C.meets_open_cone_bruteforce(n, up, X):
                    bad += 1
        check("n=%d constructive vs |X|!-search disagreements (of %d flats)"
              % (n, cells), bad, 0)
    print()

    print("(b2) AC(P) BY TWO ROUTES -- acyclic quotient vs supports of moves")
    for n in range(1, min(nmax, 5) + 1):
        bad = 0
        for up in C.iso_classes(n):
            a = sorted(C.support_lattice(n, up))
            b = C.commitment_levels_from_moves(n, up)
            if a != b:
                bad += 1
        check("n=%d posets where the two AC(P) routes disagree" % n, bad, 0)
    print()

    print("(c) EVERY NUMBER THIS AUDIT'S DOCUMENT CARRIES")
    want_docbad = {2: 0, 3: 0, 4: 1, 5: 10, 6: 101}
    want_spur = {2: 0, 3: 0, 4: 1, 5: 18, 6: 455}
    for n in range(2, nmax + 1):
        res, tot = sweep(n, want_offAC=True)
        check("n=%d posets where the ORIGINAL rule breaks Brown's identity" % n,
              res['DOC (mg-ebd8)']['sumbad'], want_docbad[n])
        check("n=%d posets where the REPAIRED rule breaks Brown's identity" % n,
              res['REPAIRED (mg-1953)']['sumbad'], 0)
        check("n=%d ORIGINAL rule != M_0 (constructed), as sets" % n,
              res['DOC (mg-ebd8)']['setbad'], want_docbad[n])
        check("n=%d REPAIRED rule != M_0 (constructed), as sets" % n,
              res['REPAIRED (mg-1953)']['setbad'], 0)
        check("n=%d spurious flats under the ORIGINAL rule" % n,
              res['DOC (mg-ebd8)']['spurious'], want_spur[n])
        check("n=%d disagreeing flats that lie INSIDE AC(P)" % n, tot['on'], 0)
        check("n=%d disagreeing flats that lie OUTSIDE AC(P)" % n,
              tot['off'], want_spur[n])
    check("total flats at n=6 (318 classes x 203)", 318 * 203, 64554)
    print()

    print("    the witness, on the auditor's labels")
    up = (1 << 3, 1 << 2, 0, 0)                    # a<d, b<c
    flats4 = C.set_partitions(4)
    check("P={a<d,b<c}: |L(P)|", C.count_linear_extensions(4, up), 6)
    check("P={a<d,b<c}: ORIGINAL rule sums to",
          sum(C.closed_form(X) for X in flats4 if rule_doc(4, up, X)), 7)
    check("P={a<d,b<c}: REPAIRED rule sums to",
          sum(C.closed_form(X) for X in flats4 if rule_rep(4, up, X)), 6)
    check("P={a<d,b<c}: the spurious flat",
          [C.label(X, 4) for X in flats4
           if rule_doc(4, up, X) and not rule_rep(4, up, X)], ["ac|bd"])
    up2 = (1 << 2, 1 << 3, 0, 0)                   # a<c, b<d -- mg-1953's label
    check("P={a<c,b<d}: ORIGINAL rule sums to",
          sum(C.closed_form(X) for X in flats4 if rule_doc(4, up2, X)), 7)
    check("P={a<c,b<d}: the spurious flat",
          [C.label(X, 4) for X in flats4
           if rule_doc(4, up2, X) and not rule_rep(4, up2, X)], ["ad|bc"])
    print()

    print("    R3 -- the two-sided comparison and the true gain")
    rows = spectrum_sweep(nmax)
    want_lev = {2: 4, 3: 24, 4: 206, 5: 2353, 6: 37029}
    want_zero = {2: 1, 3: 11, 4: 125, 5: 1674, 6: 28988}
    for n in range(2, nmax + 1):
        check("n=%d levels" % n, rows[n]['levels'], want_lev[n])
        check("n=%d disagreeing levels (solve vs closed form)" % n,
              rows[n]['disagree'], 0)
        check("n=%d levels where supp(m) != M_0" % n, rows[n]['supp_bad'], 0)
        check("n=%d levels carrying zero" % n, rows[n]['zero_levels'],
              want_zero[n])
        check("n=%d levels where the closed form is LARGER" % n,
              rows[n]['cf_bigger'], 0)
        check("n=%d levels where the closed form is SMALLER" % n,
              rows[n]['cf_smaller'], 0)
    check("levels, 2 <= n <= %d, total" % nmax,
          sum(rows[n]['levels'] for n in range(2, nmax + 1)),
          sum(want_lev[n] for n in range(2, nmax + 1)))
    print()

    print("    R4 -- the populations")
    pop = populations(min(nmax, 6))
    check("classes 2 <= n <= %d (E3's population)" % min(nmax, 6),
          sum(pop[n]['classes'] for n in pop if n >= 2),
          404 if nmax >= 6 else 86)
    check("classes 3 <= n <= %d (item 5's population)" % min(nmax, 6),
          sum(pop[n]['classes'] for n in pop if n >= 3),
          402 if nmax >= 6 else 84)
    check("classes n <= 5 (E1's population)",
          sum(pop[n]['classes'] for n in pop if n <= 5), 87)
    check("moves n <= 5 total", sum(pop[n]['moves'] for n in pop if n <= 5),
          6197)
    check("product pairs n <= 5 total",
          sum(pop[n]['pairs'] for n in pop if n <= 5), 936261)
    check("product pairs n = 5 row", pop[5]['pairs'], 922073)
    check("levels n <= 5 TOTAL (not 2 353 -- that is the n = 5 ROW)",
          sum(pop[n]['levels'] for n in pop if n <= 5), 2588)
    check("levels 2 <= n <= 5 total",
          sum(pop[n]['levels'] for n in pop if 2 <= n <= 5), 2587)
    print()

    print("    the Moebius step mg-1953 does not re-derive")
    for n in range(1, min(nmax, 6) + 1):
        flats, mu = moebius_pi(n)
        check("n=%d flats where |mu(0,X)| != prod (|B|-1)!" % n,
              sum(1 for X in flats if abs(mu[X]) != C.closed_form(X)), 0)
    print()

    print("    R2 -- the E8 replacement")
    from audit_r2_e8 import band_product, phi
    for n in range(1, min(nmax, 5) + 1):
        classes = C.iso_classes(n)
        hom = inj = proper = into = 0
        for up in classes:
            W = feasible_words(n, up)
            F = set(C.moves_of(n, up))
            img = {phi(n, w) for w in W}
            into += (img <= F)
            hom += all(phi(n, band_product(n, up, w, v))
                       == C.move_product(phi(n, w), phi(n, v))
                       for w in W for v in W)
            inj += (len(img) == len(W))
            proper += (img != F)
        check("n=%d phi is a monoid homomorphism" % n, hom, len(classes))
        check("n=%d image of phi lies in F(P)" % n, into, len(classes))
        check("n=%d phi is injective" % n, inj, 0)
        check("n=%d image is a PROPER submonoid" % n, proper,
              len(classes) if n >= 3 else 0)
    print()

    if FAIL:
        print("SELF-TEST FAILED -- %d assertion(s):" % len(FAIL))
        for f in FAIL:
            print("   %s" % f)
        sys.exit(1)
    print("SELF-TEST PASSED -- every number this audit carries is reproduced.")


if __name__ == "__main__":
    main()
