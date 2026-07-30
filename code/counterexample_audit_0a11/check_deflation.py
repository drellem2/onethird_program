"""A6 -- the DEFLATION (repair section 5), and the beyond-brief material.

Section 5 is not one of the repair's four asks.  It is material the repair
added, it points in the deflationary direction, and by the mg-0a11 standing
("material added beyond the brief is the highest-yield target") it gets checked
in full rather than accepted because it is modest.

Three claims:

  D1  every member of the three non-vacuous groups attains its maximum qmass at
      L*, over ALL of its linear extensions;
  D2  the members whose best linear extension reaches qmass = 1 are exactly the
      extremal ones -- 1 of 7, 3 of 13, 6 of 20;
  D3  "L* maximises qmass" is FALSE in general: L* attains the max for 14 of 16
      at n = 5, 83 of 88 at n = 6, 583 of 669 at n = 7, and the max is unique
      for 13 / 59 / 309.  (Two of 671 posets at n = 7 are skipped for cost,
      e(P) > 400.)

qmass(L) for an arbitrary linear extension L is well defined by the same
formula: the interval partitions of L are levels, and qmass(L) is their
multiplicity mass over e(P).
"""

import math
from fractions import Fraction

from kernel import (Poset, enumerate_posets, interval_partitions, level_data,
                    qstats)

NMAX = 7
COST_CAP = 400


def banner(s):
    print()
    print("=" * 78)
    print(s)
    print("=" * 78)


def linear_extensions(P):
    out = []
    full = (1 << P.n) - 1

    def rec(S, acc):
        if S == full:
            out.append(tuple(acc))
            return
        for x in range(P.n):
            if (S >> x) & 1:
                continue
            if P.down[x] & ~S:
                continue
            acc.append(x)
            rec(S | (1 << x), acc)
            acc.pop()

    rec(0, [])
    return out


def qmass_all(P):
    """(qmass(L) for every L, index of L*, e(P)) with m computed once."""
    levels, m = level_data(P)
    tot = P.e()
    vals = []
    for L in linear_extensions(P):
        s = 0
        for X in interval_partitions(list(L)):
            if X in levels:
                s += m[X]
        vals.append(Fraction(s, tot))
    return vals, linear_extensions(P), tot


def in_population(P):
    return (not P.is_chain() and P.tie_free()
            and P.majority_cycle() is None)


def main():
    lv = enumerate_posets(NMAX)

    banner("A6.D1/D2  inside the three non-vacuous groups: is L* needed at all?")
    print("  n | e | N  | k | max over ALL L reaches 1 | of those extremal | L* is argmax")
    for n in (6, 7):
        grp = [P for P in lv[n] if in_population(P) and P.e() == 9]
        if not grp:
            continue
        reach = ext_reach = argmax = 0
        for P in grp:
            vals, Ls, tot = qmass_all(P)
            star = tuple(P.Lstar())
            i = Ls.index(star)
            mx = max(vals)
            if mx == 1:
                reach += 1
                if P.delta() == Fraction(1, 3):
                    ext_reach += 1
            if vals[i] == mx:
                argmax += 1
        k = sum(1 for P in grp if P.delta() == Fraction(1, 3))
        print("  %d | 9 | %2d | %d | %24d | %17d | %d of %d"
              % (n, len(grp), k, reach, ext_reach, argmax, len(grp)))
    print()
    print("  (the n = 8 group is the n = 7 group with a cut element adjoined --")
    print("   see check_independence.py -- so it is not listed separately here)")

    banner("A6.D3  'L* maximises qmass' over the whole population")
    print("  repair reports: 14 of 16, 83 of 88, 583 of 669; unique 13 / 59 / 309")
    print()
    print("  n | tested | skipped (e > %d) | L* attains max | max is unique" % COST_CAP)
    for n in range(5, NMAX + 1):
        pop = [P for P in lv[n] if in_population(P)]
        tested = skipped = attains = unique = 0
        for P in pop:
            if P.e() > COST_CAP:
                skipped += 1
                continue
            tested += 1
            vals, Ls, tot = qmass_all(P)
            star = tuple(P.Lstar())
            i = Ls.index(star)
            mx = max(vals)
            if vals[i] == mx:
                attains += 1
            if sum(1 for v in vals if v == mx) == 1:
                unique += 1
        print("  %d | %6d | %16d | %14d | %d"
              % (n, tested, skipped, attains, unique))


if __name__ == "__main__":
    main()
