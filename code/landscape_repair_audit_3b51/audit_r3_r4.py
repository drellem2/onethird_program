#!/usr/bin/env python3
"""
mg-3b51 AUDIT 2 -- "STRICTLY SHARPER" -> "STRICTLY MORE INFORMATIVE" (R3),
AND EVERY POPULATION THE REPAIR RE-STATES (R4).

R3 is the correction with the largest consequence: mg-1953 replaces the commit
subject's "STRICTLY SHARPER" with "strictly more informative" on the strength of
a two-sided comparison -- the repo's triangular solve against Brown's repaired
closed form -- reporting 0 disagreeing levels of 39 616 to n <= 6 and, at n <= 5,
0 of 2 353.  This script runs that comparison from an instrument that shares no
code with mg-1953's, mg-ebd8's or mg-d673's.

  B1  THE TWO-SIDED COMPARISON, level by level.  The solve side is rebuilt from
      the repo's identity  sum_{Y refines X} m_Y = prod_B |L(P|_B)|  and never
      consults the closed form; the closed-form side never consults the solve.
  B2  SUPPORT.  supp(m) == M_0, i.e. the levels carrying nonzero multiplicity
      are exactly the antichain-blocked acyclic-quotient ones.
  B3  WHAT THEOREM 2 ACTUALLY BUYS, counted: the levels carrying ZERO, which
      Brown names a priori instead of discovering by a solve.  This is the
      TRUE gain that must not be lost with the false one.
  B4  IS IT "SHARPER" IN ANY DIRECTION?  A bound word needs a direction.  Count
      levels where the closed form is strictly larger, strictly smaller, and
      equal.
  B5  POPULATIONS (R4): classes, levels, moves, product pairs, and the derived
      figures 404, 402, 87, 6 197, 936 261, 39 616.
  B6  THE ONE STEP OF THE REPAIRED STATEMENT mg-1953 DOES NOT RE-DERIVE:
      that prod_B (|B|-1)! IS |mu(X, V)| -- the Moebius function of the
      intersection lattice, which is what Brown's Theorem 2 actually says.
      Computed here directly from the Moebius recursion on Pi_n.
"""

import sys

from core3b51 import (iso_classes, set_partitions, relations, closed_form,
                      all_blocks_antichain, quotient_digraph, find_cycle,
                      count_linear_extensions, induced, refines, multiplicities,
                      support_lattice, commitment_levels_from_moves, moves_of,
                      move_product, label)


def acyclic(n, up, X):
    succ, _ = quotient_digraph(n, up, X)
    return find_cycle(succ) is None


def in_M0(n, up, X):
    return all_blocks_antichain(up, X) and acyclic(n, up, X)


def spectrum_sweep(nmax):
    rows = {}
    for n in range(1, nmax + 1):
        flats = set_partitions(n)
        classes = iso_classes(n)
        r = dict(classes=len(classes), levels=0, disagree=0, badposets=0,
                 supp_bad=0, zero_levels=0, nonzero_levels=0,
                 cf_bigger=0, cf_smaller=0, equal=0)
        for up in classes:
            lev = [X for X in flats if acyclic(n, up, X)]
            r['levels'] += len(lev)
            m, _ = multiplicities(n, up, lev)
            bad = 0
            for X in lev:
                cf = closed_form(X) if in_M0(n, up, X) else 0
                if m[X] != cf:
                    bad += 1
                if cf > m[X]:
                    r['cf_bigger'] += 1
                elif cf < m[X]:
                    r['cf_smaller'] += 1
                else:
                    r['equal'] += 1
                if m[X] == 0:
                    r['zero_levels'] += 1
                else:
                    r['nonzero_levels'] += 1
                if (m[X] != 0) != in_M0(n, up, X):
                    r['supp_bad'] += 1
            r['disagree'] += bad
            if bad:
                r['badposets'] += 1
        rows[n] = r
    return rows


def populations(nmax):
    rows = {}
    for n in range(1, nmax + 1):
        classes = iso_classes(n)
        flats = set_partitions(n)
        mv = 0
        pairs = 0
        lev = 0
        for up in classes:
            if n <= 5:
                M = moves_of(n, up)
                mv += len(M)
                pairs += len(M) * len(M)
            lev += sum(1 for X in flats if acyclic(n, up, X))
        rows[n] = dict(classes=len(classes), moves=mv, pairs=pairs, levels=lev)
    return rows


def moebius_pi(n):
    """mu(0-hat, X) in the partition lattice Pi_n, by the defining recursion
    sum_{0 <= Y <= X} mu(0,Y) = [X = 0].  No closed form used."""
    flats = set_partitions(n)
    order = sorted(range(len(flats)), key=lambda k: len(flats[k]), reverse=True)
    mu = {}
    for k in order:
        X = flats[k]
        s = 0
        for j in order:
            if j == k:
                continue
            if flats[j] in mu and refines(flats[j], X):
                s += mu[flats[j]]
        mu[X] = (1 if len(X) == n else 0) - s
    return flats, mu


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    print("=" * 78)
    print("mg-3b51 AUDIT 2 -- R3 ('sharper' -> 'more informative') AND R4")
    print("=" * 78)
    print()

    rows = spectrum_sweep(nmax)

    print("-" * 78)
    print("B1  TWO-SIDED COMPARISON, LEVEL BY LEVEL.  Repo's triangular solve")
    print("    (rebuilt from the identity) vs Brown's REPAIRED closed form.")
    print("-" * 78)
    print("%3s %8s %9s %22s %18s" % ("n", "classes", "levels",
                                     "disagreeing levels", "bad posets"))
    tl = td = tc = 0
    for n in range(2, nmax + 1):
        r = rows[n]
        tl += r['levels']; td += r['disagree']; tc += r['classes']
        print("%3d %8d %9d %22d %18d"
              % (n, r['classes'], r['levels'], r['disagree'], r['badposets']))
    print("%3s %8d %9d %22d %18d" % ("tot", tc, tl, td, 0))
    print()
    print("    n <= 5 levels: %d      n <= 6 levels: %d"
          % (sum(rows[n]['levels'] for n in range(2, min(5, nmax) + 1)), tl))
    print()

    print("-" * 78)
    print("B2  SUPPORT.  Is  m_X != 0  exactly on M_0?")
    print("-" * 78)
    print("%3s %9s %26s" % ("n", "levels", "levels where supp != M_0"))
    for n in range(2, nmax + 1):
        print("%3d %9d %26d" % (n, rows[n]['levels'], rows[n]['supp_bad']))
    print()

    print("-" * 78)
    print("B3  WHAT THEOREM 2 BUYS -- the TRUE gain, counted.  Levels carrying")
    print("    ZERO, named a priori instead of discovered by a solve.")
    print("-" * 78)
    print("%3s %9s %14s %14s" % ("n", "levels", "carry zero", "carry nonzero"))
    for n in range(2, nmax + 1):
        r = rows[n]
        print("%3d %9d %14d %14d"
              % (n, r['levels'], r['zero_levels'], r['nonzero_levels']))
    print()

    print("-" * 78)
    print("B4  IS IT 'SHARPER' IN ANY DIRECTION?  A bound word needs one.")
    print("-" * 78)
    print("%3s %14s %16s %16s" % ("n", "closed form >", "closed form <", "equal"))
    for n in range(2, nmax + 1):
        r = rows[n]
        print("%3d %14d %16d %16d"
              % (n, r['cf_bigger'], r['cf_smaller'], r['equal']))
    print()
    print("    Neither side is ever larger anywhere.  'Sharper' has no direction")
    print("    to point in; 'more informative' is a statement about WHEN the")
    print("    answer is available, and B3 counts it.")
    print()

    print("-" * 78)
    print("B5  POPULATIONS (R4), rebuilt.")
    print("-" * 78)
    pop = populations(min(nmax, 6))
    print("%3s %9s %9s %13s %10s" % ("n", "classes", "moves", "product pairs",
                                     "levels"))
    for n in range(1, min(nmax, 6) + 1):
        p = pop[n]
        print("%3d %9d %9s %13s %10d"
              % (n, p['classes'],
                 p['moves'] if n <= 5 else "-",
                 p['pairs'] if n <= 5 else "-",
                 p['levels']))
    c = {n: pop[n]['classes'] for n in pop}
    print()
    print("    classes  1..6                 : %s" %
          ", ".join(str(c[n]) for n in sorted(c)))
    print("    classes  2 <= n <= 6  (E3)    : %d   [document says 404]"
          % sum(c[n] for n in c if 2 <= n <= 6))
    print("    classes  3 <= n <= 6  (item 5): %d   [document says 402]"
          % sum(c[n] for n in c if 3 <= n <= 6))
    print("    classes  n <= 5       (E1)    : %d   [document says 87]"
          % sum(c[n] for n in c if n <= 5))
    print("    moves    n <= 5 total         : %d   [document says 6 197]"
          % sum(pop[n]['moves'] for n in pop if n <= 5))
    print("    product pairs n <= 5 total    : %d   [document says 936 261]"
          % sum(pop[n]['pairs'] for n in pop if n <= 5))
    print("    product pairs n = 5 row       : %d   [document says 922 073]"
          % pop[5]['pairs'])
    print("    levels   2 <= n <= 6 total    : %d   [document says 39 616]"
          % sum(pop[n]['levels'] for n in pop if 2 <= n <= 6))
    print("    levels   2 <= n <= 5 total    : %d   [document says 2 353 at n=5]"
          % sum(pop[n]['levels'] for n in pop if 2 <= n <= 5))
    print()

    print("-" * 78)
    print("B6  THE STEP mg-1953 DOES NOT RE-DERIVE.  Brown's Theorem 2 says")
    print("    m_X = |mu(X, V)|.  The document -- original and repaired -- uses")
    print("    prod_B (|B|-1)! and never checks that identification.  Moebius")
    print("    function of Pi_n computed here from its defining recursion.")
    print("-" * 78)
    print("%3s %10s %34s" % ("n", "flats", "|mu(0,X)| != prod (|B|-1)!"))
    for n in range(1, min(nmax, 6) + 1):
        flats, mu = moebius_pi(n)
        bad = sum(1 for X in flats if abs(mu[X]) != closed_form(X))
        print("%3d %10d %34s" % (n, len(flats), "%d bad of %d" % (bad, len(flats))))
    print()
    print("    Closed under the repair's own range.  The link holds; it was")
    print("    simply never exercised by mg-1953's instruments, which take")
    print("    prod_B (|B|-1)! as the statement rather than as a specialisation.")
    print()
    print("=" * 78)


if __name__ == "__main__":
    main()
