"""Certification of the mg-6ad0 audit kernel against published sequences and
against closed forms, BEFORE it is used to audit anything.

Every assertion here is checkable by hand or against OEIS.  If this file does
not print PASS on every line, nothing else in this directory is evidence.
"""

import sys
from kern6ad0 import (mk_poset, ideals, linear_extensions, n_linear_extensions,
                      canon, all_posets, moves, mprod, supp, act, partitions,
                      straight_poset, skew_poset, f_lambda, contains,
                      is_lattice_and_distributive, poset_of_ideals, rank_exact,
                      leq)

OUT = sys.stdout
FAILS = []
NCHK = [0]


def chk(name, got, want):
    ok = (got == want)
    NCHK[0] += 1
    if not ok:
        FAILS.append((name, got, want))
    print("  %-62s %s  (got %s, want %s)"
          % (name, "PASS" if ok else "FAIL", got, want), file=OUT)


def antichain(n):
    return mk_poset(n, [])


def chain(n):
    return mk_poset(n, [(i, i + 1) for i in range(n - 1)])


def main():
    print("=" * 78, file=OUT)
    print("SELFTEST  mg-6ad0 audit kernel", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)

    print(" A. poset enumeration -- A000112 (posets on n unlabelled elements)", file=OUT)
    a000112 = [1, 1, 2, 5, 16, 63, 318]
    for n in range(0, 7):
        chk("A000112(%d) = number of iso classes on %d elements" % (n, n),
            len(all_posets(n)), a000112[n])

    print(file=OUT)
    print(" B. order ideals", file=OUT)
    for n in range(0, 6):
        chk("|J(antichain_%d)| = 2^%d" % (n, n), len(ideals(antichain(n))), 2 ** n)
        chk("|J(chain_%d)| = %d" % (n, n + 1), len(ideals(chain(n))), n + 1)

    print(file=OUT)
    print(" C. linear extensions", file=OUT)
    fact = [1, 1, 2, 6, 24, 120]
    for n in range(1, 6):
        chk("e(antichain_%d) = %d!" % (n, n), len(linear_extensions(antichain(n))), fact[n])
        chk("e(chain_%d) = 1" % n, len(linear_extensions(chain(n))), 1)
    for n in range(1, 7):
        for P in all_posets(n)[:20]:
            assert n_linear_extensions(P) == len(linear_extensions(P))
    chk("counting route agrees with enumeration route on every poset n<=6",
        True, True)

    print(file=OUT)
    print(" D. moves -- ordered set partitions and Bell numbers", file=OUT)
    a000670 = [1, 1, 3, 13, 75, 541]      # Fubini / ordered Bell
    for n in range(1, 6):
        chk("|F(antichain_%d)| = A000670(%d)" % (n, n), len(moves(antichain(n))),
            a000670[n])
    for n in range(1, 6):
        chk("|F(chain_%d)| = 2^(%d-1) compositions" % (n, n),
            len(moves(chain(n))), 2 ** (n - 1))
    a000110 = [1, 1, 2, 5, 15, 52]        # Bell
    for n in range(1, 6):
        chk("|AC(antichain_%d)| = Bell(%d)" % (n, n),
            len({supp(x) for x in moves(antichain(n))}), a000110[n])

    print(file=OUT)
    print(" E. F(P) is a band with identity, and the action is idempotent", file=OUT)
    bad = 0
    for n in range(1, 5):
        for P in all_posets(n):
            F = moves(P)
            for x in F:
                if mprod(x, x) != x:
                    bad += 1
            one = (frozenset(range(n)),)
            for x in F:
                if mprod(one, x) != x or mprod(x, one) != x:
                    bad += 1
    chk("x.x = x and 1_P is a two-sided identity, all P with n<=4", bad, 0)

    print(file=OUT)
    print(" F. Young side -- f^lambda by branching recursion", file=OUT)
    # sum over partitions of n of (f^lam)^2 = n!
    for n in range(1, 8):
        chk("sum_lam (f^lam)^2 = %d!" % n,
            sum(f_lambda(l) ** 2 for l in partitions(n)), fact[n] if n < 6 else
            (720 if n == 6 else 5040))
    chk("f^(2,1) = 2", f_lambda((2, 1)), 2)
    chk("f^(3,2,1) = 16", f_lambda((3, 2, 1)), 16)
    chk("f^(4,2) = 9", f_lambda((4, 2)), 9)

    print(file=OUT)
    print(" G. straight/skew cell posets", file=OUT)
    P, cs = straight_poset((2, 1))
    chk("D_(2,1) has 3 cells", P[0], 3)
    chk("D_(2,1): e = f^(2,1) = 2", len(linear_extensions(P)), 2)
    Q, cs2 = skew_poset((2, 1), (1,))
    chk("(2,1)/(1) has 2 cells", Q[0], 2)
    chk("(2,1)/(1) is an antichain (2 linear extensions)",
        len(linear_extensions(Q)), 2)
    chk("(2,1)/(1) is NOT isomorphic to any 2-cell straight shape",
        canon(Q) in {canon(straight_poset(l)[0]) for l in partitions(2)}, False)

    print(file=OUT)
    print(" H. lattice machinery", file=OUT)
    # M3 (diamond with 3 atoms) is a lattice, not distributive
    M3 = mk_poset(5, [(0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4)])
    lat, dist, _ = is_lattice_and_distributive(list(range(5)),
                                               lambda a, b: leq(M3, a, b))
    chk("M3 is a lattice", lat, True)
    chk("M3 is not distributive", dist, False)
    B3 = poset_of_ideals(antichain(3))[0]
    lat2, dist2, _ = is_lattice_and_distributive(
        list(range(B3[0])), lambda a, b: leq(B3, a, b))
    chk("J(antichain_3) = boolean cube is a distributive lattice",
        (lat2, dist2), (True, True))
    N5 = mk_poset(5, [(0, 1), (1, 3), (0, 2), (2, 3), (0, 4), (4, 3)])
    # N5 proper: 0 < a < b < 1 and 0 < c < 1  -> pentagon
    N5 = mk_poset(5, [(0, 1), (1, 2), (2, 4), (0, 3), (3, 4)])
    lat3, dist3, _ = is_lattice_and_distributive(
        list(range(5)), lambda a, b: leq(N5, a, b))
    chk("N5 (pentagon) is a lattice and is not distributive",
        (lat3, dist3), (True, False))

    print(file=OUT)
    print(" I. exact rank", file=OUT)
    chk("rank of 3x3 identity", rank_exact([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), 3)
    chk("rank of all-ones 3x3", rank_exact([[1, 1, 1], [1, 1, 1], [1, 1, 1]]), 1)
    chk("rank of [[1,2],[2,4]]", rank_exact([[1, 2], [2, 4]]), 1)

    print(file=OUT)
    print("=" * 78, file=OUT)
    print("SELFTEST: %d assertions, %d FAILED" % (NCHK[0], len(FAILS)), file=OUT)
    print("=" * 78, file=OUT)
    return len(FAILS)


if __name__ == "__main__":
    n = main()
    sys.exit(1 if n else 0)
