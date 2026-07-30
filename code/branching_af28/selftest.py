"""Self-test for the mg-af28 battery.

Every number that appears in `docs/OneThird-Branching-Graphs-Where-This-Lives.md`
is asserted here against a freshly computed value, plus the external certificates
(A000112 for posets, ordered Bell / Bell for the antichain, the hook length
formula for SYT).  If the document and the instruments drift, this fails loudly.
"""

import sys
from core_af28 import (poset_classes, moves_from_chains, moves_bruteforce, AC,
                       linear_extensions, ideals_of, partitions, conj,
                       cell_poset, sub_shapes, hook_length_formula, canon,
                       skew_cell_poset, skew_shape_classes,
                       young_fibonacci, move_product, act)

N = 0
FAIL = []


def check(name, got, want):
    global N
    N += 1
    if got != want:
        FAIL.append("%-58s got %r want %r" % (name, got, want))
        print("  FAIL %-54s got %r want %r" % (name, got, want))
    else:
        print("  ok   %-54s %r" % (name, got))


def antichain(n):
    return tuple([0] * n)


def chain(n):
    return tuple(sum(1 << k for k in range(i + 1, n)) for i in range(n))


def main():
    print("=" * 78)
    print("SELF-TEST for code/branching_af28")
    print("=" * 78)
    print()

    print("-- enumeration certificates ------------------------------------------")
    check("poset classes n=1..6 (A000112)",
          [len(poset_classes(n)) for n in range(1, 7)], [1, 2, 5, 16, 63, 318])
    check("moves per n, total over classes (repo's own 1,5,37,397,5757)",
          [sum(len(moves_from_chains(p)) for p in poset_classes(n))
           for n in range(1, 6)], [1, 5, 37, 397, 5757])
    check("|F(antichain_n)| = ordered Bell A000670",
          [len(moves_from_chains(antichain(n))) for n in range(1, 6)],
          [1, 3, 13, 75, 541])
    check("|AC(antichain_n)| = Bell A000110",
          [len(AC(antichain(n))) for n in range(1, 6)], [1, 2, 5, 15, 52])
    check("|F(chain_n)| = 2^(n-1)",
          [len(moves_from_chains(chain(n))) for n in range(1, 7)],
          [1, 2, 4, 8, 16, 32])
    check("|L(chain_n)| = 1",
          [len(linear_extensions(chain(n))) for n in range(1, 7)], [1] * 6)
    check("|L(antichain_n)| = n!",
          [len(linear_extensions(antichain(n))) for n in range(1, 6)],
          [1, 2, 6, 24, 120])
    print()

    print("-- T0 anchor: the two definitions of a move agree ---------------------")
    bad = 0
    for n in range(1, 6):
        for p in poset_classes(n):
            if set(moves_bruteforce(p)) != set(moves_from_chains(p)):
                bad += 1
    check("P-compatible ordered set partitions == chains in J(P), n<=5, bad", bad, 0)
    print()

    print("-- T1: J(D_lambda) = [0,lambda] and maximal chains = SYT --------------")
    nlam = 0
    bad_iso = bad_syt = 0
    for n in range(1, 8):
        for lam in partitions(n):
            nlam += 1
            up, cells = cell_poset(lam)
            if len(ideals_of(up)) != len(sub_shapes(lam)):
                bad_iso += 1
            if len(linear_extensions(up)) != hook_length_formula(lam):
                bad_syt += 1
    check("partitions tested to n=7", nlam, 44)
    check("|J(D_lambda)| != |[0,lambda]| count", bad_iso, 0)
    check("e(D_lambda) != f^lambda (hook length formula) count", bad_syt, 0)
    check("f^(3,2,1) = 16", hook_length_formula((3, 2, 1)), 16)
    check("f^(4,2,1) = 35", hook_length_formula((4, 2, 1)), 35)
    check("sum_lambda (f^lambda)^2 = n! for n=6",
          sum(hook_length_formula(l) ** 2 for l in partitions(6)), 720)
    print()

    print("-- T2: straight and skew shape posets among all posets ----------------")
    shp = [len({canon(cell_poset(lam)[0]) for lam in partitions(n)})
           for n in range(1, 9)]
    check("STRAIGHT shape-poset classes n=1..8", shp, [1, 1, 2, 3, 4, 6, 8, 12])
    check("straight shape posets at n=6 out of 318", (shp[5], 318), (6, 318))
    # mg-41aa, X1 of mg-6ad0's audit: the class "J(P) is an interval of Young's
    # lattice" is the SKEW shapes, not the straight ones, and nothing in this
    # directory used to test the difference.  n <= 6 only; n = 7, 8 cost minutes
    # and hours under this file's n! canonical form and are cited in T2 with
    # their provenance.
    skw = [len(skew_shape_classes(n)) for n in range(1, 7)]
    check("SKEW shape-poset classes n=1..6", skw, [1, 2, 5, 11, 26, 62])
    check("skew shape posets at n=6 out of 318", (skw[5], 318), (62, 318))
    check("at n <= 3 EVERY poset is a skew shape poset",
          skw[:3], [len(poset_classes(n)) for n in range(1, 4)])
    check("the 2-element antichain is a skew shape but not a straight one",
          (canon(skew_cell_poset((2, 1), (1,))[0]) == canon((0, 0)),
           canon((0, 0)) in {canon(cell_poset(l)[0]) for l in partitions(2)}),
          (True, False))
    print()

    print("-- T3: differential condition -----------------------------------------")
    from t_branching import updown_report, young_lattice
    e, rk, cv = young_lattice(8)
    r_full, ok_full, r_tr, ok_tr, mr = updown_report("Y", e, rk, cv)
    check("Young's lattice to rank 8: differential below the top, r", r_tr, 1)
    check("Young's lattice to rank 8: differential on the whole truncation",
          ok_full, False)
    ranks, cov = young_fibonacci(8)
    el = [w for r in sorted(ranks) for w in ranks[r]]
    rk2 = {w: sum(w) for w in el}
    _, okf2, rt2, okt2, _ = updown_report("YF", el, rk2, cov)
    check("Young-Fibonacci to rank 8: differential below the top, r", rt2, 1)
    check("Young-Fibonacci rank sizes are Fibonacci",
          [len(ranks[r]) for r in range(0, 8)], [1, 1, 2, 3, 5, 8, 13, 21])
    passers = 0
    for n in range(2, 7):
        for up in poset_classes(n):
            ids = ideals_of(up)
            rank = {I: bin(I).count("1") for I in ids}
            covers = {I: [J for J in ids if rank[J] == rank[I] + 1 and I & J == I]
                      for I in ids}
            _, okf, _, okt, _ = updown_report("J", ids, rank, covers)
            if okf or okt:
                passers += 1
    check("posets 2<=n<=6 whose J(P) is differential (either sense)", passers, 0)
    print()

    print("-- T5: dim kF(P)/rad = |AC(P)| ----------------------------------------")
    from t_lrb_reps import gram
    from core_af28 import rank_exact
    bad5 = tested5 = 0
    for n in range(1, 6):
        for up in poset_classes(n):
            F = moves_from_chains(up)
            tested5 += 1
            if rank_exact(gram(F)) != len(AC(up, F)):
                bad5 += 1
    check("classes tested at n<=5 (all of them)", tested5, 87)
    check("rank of the trace form != |AC(P)|, count", bad5, 0)
    print()

    print("-- T6: no non-identity invertible move --------------------------------")
    bad6 = 0
    for n in range(1, 6):
        for up in poset_classes(n):
            le = linear_extensions(up)
            for x in moves_from_chains(up):
                img = {act(x, c) for c in le}
                if len(img) == len(le) and any(act(x, c) != c for c in le):
                    bad6 += 1
    check("moves acting bijectively but not as the identity, n<=5", bad6, 0)
    print()

    print("-- T7: concatenation is a non-unital semigroup homomorphism -----------")
    from t_branching import disjoint_union, shift_move
    unital = cases = badhom = 0
    for np_ in range(1, 4):
        for nq in range(1, 4):
            for upP in poset_classes(np_):
                for upQ in poset_classes(nq):
                    cases += 1
                    R = disjoint_union(upP, upQ)
                    FR = set(moves_from_chains(R))
                    FP, FQ = moves_from_chains(upP), moves_from_chains(upQ)
                    for x in FP:
                        for y in FQ:
                            if x + shift_move(y, np_) not in FR:
                                badhom += 1
                    if (((1 << np_) - 1,) + shift_move(((1 << nq) - 1,), np_)
                            == ((1 << (np_ + nq)) - 1,)):
                        unital += 1
    check("concatenation lands outside F(P+Q), count", badhom, 0)
    check("pairs (P,Q) with |P|,|Q| <= 3", cases, 64)
    check("of those, concatenation unital", unital, 0)
    print()

    print("=" * 78)
    print("%d assertions, %d failures" % (N, len(FAIL)))
    print("=" * 78)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
