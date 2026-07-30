"""Controls for the repair instrument, including ones that FIRE.

Everything the repair asserts is produced by this directory, so the directory has
to be certified from outside itself.  Two kinds of check appear below:

  POSITIVE controls -- an independently computable quantity, checked.  Where a
  route exists outside the repository the external sequence is used (A000112,
  A001035, A000670); where the alternative is a slower route, the slow route is
  run and compared (brute-force linear extensions, brute-force block orderings,
  the level-lattice inversion the target's instrument uses, the actual transition
  matrix).

  NEGATIVE controls -- deliberate mutations, run to confirm the positive controls
  can fail.  A control that has never failed is not known to be a control.  Each
  mutation is applied to a copy, the affected check is re-run, and the run aborts
  unless the check FAILS.
"""

import sys
from fractions import Fraction
from itertools import permutations

import levels
import poset as P_
from levels import (all_levels, all_partitions, is_level, m_table, m_by_inversion,
                   qmass, qfrac, block_digraph, interval_masks)
from poset import (all_posets, canonical, canonical_bruteforce, e_all_subsets,
                   from_covers, induced, make, pair_probs, tie_free, lstar,
                   delta_of)
from walk import (all_moves, linear_extensions, transition_matrix, lambdas,
                  multiplicities, power_sums_agree, topological_orders)

A000112 = [1, 1, 2, 5, 16, 63, 318, 2045, 16999]      # posets up to isomorphism
A001035 = [1, 1, 3, 19, 219, 4231, 130023, 6129859]   # labelled posets
A000670 = [1, 1, 3, 13, 75, 541, 4683]                # ordered set partitions

FAILURES = []


def check(name, ok, detail=""):
    print("  %-6s %s%s" % ("PASS" if ok else "FAIL", name,
                           ("   " + detail) if detail else ""))
    if not ok:
        FAILURES.append(name)
    return ok


def expect_fail(name, ok, detail=""):
    """A negative control: the underlying check must NOT pass."""
    print("  %-6s %s%s" % ("PASS" if not ok else "FAIL", name,
                           ("   " + detail) if detail else ""))
    if ok:
        FAILURES.append("negative control did not fire: " + name)
    return not ok


def automorphisms(P):
    n = P.n
    count = 0
    for perm in permutations(range(n)):
        ok = True
        for i in range(n):
            for j in range(n):
                if bool(P.up[i] >> j & 1) != bool(P.up[perm[i]] >> perm[j] & 1):
                    ok = False
                    break
            if not ok:
                break
        if ok:
            count += 1
    return count


def main():
    print("=" * 78)
    print("CONTROLS -- code/counterexample_repair_dea5/")
    print("=" * 78)
    print(__doc__.strip())

    print()
    print("C1  enumeration up to isomorphism against A000112 (external)")
    got = [len(all_posets(n)) for n in range(0, 9)]
    check("C1", got == A000112[:9], "%s" % got)

    print()
    print("C2  the LABELLED count as an orbit sum, against A001035 (external).")
    print("    sum over classes of n!/|Aut(P)| detects over- AND under-merging of")
    print("    isomorphism classes, which a class count alone cannot.")
    fact = [1]
    for k in range(1, 9):
        fact.append(fact[-1] * k)
    got2 = []
    for n in range(0, 8):
        tot = 0
        for P in all_posets(n):
            tot += fact[n] // automorphisms(P) if n else 1
        got2.append(tot)
    check("C2", got2 == A001035[:8], "%s" % got2)

    print()
    print("C3  the canonical form against brute force over all n! relabellings")
    ok = True
    for n in range(1, 6):
        ps = all_posets(n)
        a = set(canonical(P) for P in ps)
        b = set(canonical_bruteforce(P) for P in ps)
        if len(a) != len(ps) or len(b) != len(ps):
            ok = False
    # and: two posets share a brute-force form iff they share ours
    for n in (4, 5):
        ps = []
        for P in all_posets(n):
            ps.append(P)
        # build every relabelling of every class and check the two agree
        for P in ps:
            for perm in list(permutations(range(n)))[:24]:
                up = [0] * n
                for i in range(n):
                    for j in range(n):
                        if P.up[perm[i]] >> perm[j] & 1:
                            up[i] |= 1 << j
                Q = make(n, up)
                if (canonical(Q) == canonical(P)) != \
                        (canonical_bruteforce(Q) == canonical_bruteforce(P)):
                    ok = False
    check("C3", ok, "n <= 5, and 24 relabellings of every class at n = 4, 5")

    print()
    print("C4  e(P|_S) for EVERY subset, against direct enumeration of L(P|_S)")
    bad = tot = 0
    for n in (3, 4, 5):
        for P in all_posets(n):
            e = e_all_subsets(P)
            for S in range(1 << n):
                tot += 1
                if e[S] != len(linear_extensions(induced(P, S))):
                    bad += 1
    check("C4", bad == 0, "%d (poset, subset) pairs, %d bad" % (tot, bad))

    print()
    print("C5  p(x,y) against direct counting over the enumerated L(P)")
    bad = tot = 0
    for n in (3, 4, 5):
        for P in all_posets(n):
            L = linear_extensions(P)
            probs = pair_probs(P)
            for (x, y), p in probs.items():
                tot += 1
                cnt = sum(1 for s in L if s.index(x) < s.index(y))
                if p != Fraction(cnt, len(L)):
                    bad += 1
    check("C5", bad == 0, "%d pairs, %d bad" % (tot, bad))

    print()
    print("C6  'level' = 'acyclic quotient' against brute force over block ORDERS:")
    print("    a partition is a level iff SOME ordering of its blocks is a move.")
    bad = tot = 0
    for n in (3, 4, 5):
        for P in all_posets(n):
            for X in all_partitions((1 << n) - 1):
                tot += 1
                adj = block_digraph(P, X)
                brute = len(topological_orders(len(X), adj)) > 0
                if is_level(P, X) != brute:
                    bad += 1
    check("C6", bad == 0, "%d (poset, partition) pairs, %d bad" % (tot, bad))

    print()
    print("C7  THE FACTORISATION LEMMA of levels.py, against the level-lattice")
    print("    inversion the target's instrument uses: m_X = prod_B M(P|_B) for")
    print("    every level of every poset.")
    bad = tot = 0
    cache = {}
    for n in (3, 4, 5):
        for P in all_posets(n):
            Mm, cache = m_table(P, cache)
            direct = m_by_inversion(P)
            for X, mv in direct.items():
                tot += 1
                prod = 1
                for B in X:
                    prod *= Mm[B]
                if prod != mv:
                    bad += 1
    check("C7", bad == 0, "%d levels, %d bad" % (tot, bad))

    print()
    print("C8  sum over levels of m_X = e(P), and every m_X >= 0")
    bad = tot = neg = 0
    for n in (3, 4, 5, 6, 7):
        for P in all_posets(n):
            Mm, cache = m_table(P, cache)
            s = 0
            for X in all_levels(P):
                prod = 1
                for B in X:
                    prod *= Mm[B]
                if prod < 0:
                    neg += 1
                s += prod
            tot += 1
            if s != e_all_subsets(P)[(1 << n) - 1]:
                bad += 1
    check("C8", bad == 0 and neg == 0,
          "%d posets, %d with wrong total, %d negative multiplicities" % (tot, bad, neg))

    print()
    print("C9  the M != 0 PRUNE drops no positive-multiplicity level: the pruned")
    print("    enumeration and the full one give the same multiplicity total.")
    bad = tot = 0
    for n in (3, 4, 5, 6):
        for P in all_posets(n):
            Mm, cache = m_table(P, cache)
            full = 0
            for X in all_levels(P):
                prod = 1
                for B in X:
                    prod *= Mm[B]
                full += prod
            pruned = sum(m for _, m in levels.positive_levels(P, Mm))
            tot += 1
            if full != pruned:
                bad += 1
    check("C9", bad == 0, "%d posets, %d disagreements" % (tot, bad))

    print()
    print("C9b the CONVEXITY prune drops no level: count_levels with and without it")
    bad = tot = 0
    for n in (3, 4, 5, 6):
        for P in all_posets(n):
            tot += 1
            if levels.count_levels(P, prune=True) != levels.count_levels(P, prune=False):
                bad += 1
    check("C9b", bad == 0, "%d posets, %d disagreements" % (tot, bad))

    print()
    print("C10 the SPECTRUM against the actual transition matrix, exactly")
    bad = tot = 0
    for n in (3, 4):
        for P in all_posets(n):
            if P.is_chain():
                continue
            mv = all_moves(P)
            w = [Fraction(1, len(mv))] * len(mv)
            M, L = transition_matrix(P, mv, w)
            ok, k, tr, want = power_sums_agree(M, lambdas(P, mv, w),
                                               multiplicities(P, cache))
            tot += 1
            if not ok:
                bad += 1
    check("C10", bad == 0, "%d non-chain posets at n <= 4, %d bad" % (tot, bad))

    print()
    print("C11 move counts: the antichain against A000670 (external), the chain")
    print("    against 2^(n-1)")
    ok = True
    for n in range(1, 6):
        if len(all_moves(make(n, [0] * n))) != A000670[n]:
            ok = False
    for n in range(2, 6):
        if len(all_moves(from_covers(n, [(i, i + 1) for i in range(n - 1)]))) != 2 ** (n - 1):
            ok = False
    check("C11", ok, "n <= 5")

    print()
    print("C12 qmass and qfrac against a slow independent route: m from the")
    print("    level-lattice inversion, summed over the interval partitions of L*")
    print("    found by filtering ALL levels rather than by the composition DP.")
    bad = tot = 0
    for n in (4, 5, 6):
        for P in all_posets(n):
            probs = pair_probs(P)
            if not probs or not tie_free(probs):
                continue
            order = lstar(P, probs)
            if order is None:
                continue
            e = e_all_subsets(P)
            Mm, cache = m_table(P, cache, e)
            fast = qmass(P, order, Mm, e[(1 << n) - 1])
            iv = set(interval_masks(order).values())
            direct = m_by_inversion(P)
            slow = Fraction(sum(mv for X, mv in direct.items()
                                if all(B in iv for B in X)),
                            e[(1 << n) - 1])
            tot += 1
            if fast != slow:
                bad += 1
            if qfrac(P, order) != Fraction(1 << (n - 1), len(direct)):
                bad += 1
    check("C12", bad == 0, "%d posets, %d disagreements" % (tot, bad))

    print()
    print("=" * 78)
    print("NEGATIVE CONTROLS -- each mutation must make a check above FAIL")
    print("=" * 78)

    print()
    print("N1  drop the acyclicity requirement from 'level' (call every partition a")
    print("    level).  C6 must fail.")
    orig = levels.is_level
    try:
        levels.is_level = lambda P, blocks: True
        bad = 0
        for P in all_posets(4):
            for X in all_partitions(15):
                adj = block_digraph(P, X)
                if levels.is_level(P, X) != (len(topological_orders(len(X), adj)) > 0):
                    bad += 1
        expect_fail("N1", bad == 0, "%d disagreements under the mutation" % bad)
    finally:
        levels.is_level = orig

    print()
    print("N2  replace M(R) by e(R) in the factorisation lemma.  C7 must fail.")
    bad = 0
    for P in all_posets(4):
        e = e_all_subsets(P)
        direct = m_by_inversion(P)
        for X, mv in direct.items():
            prod = 1
            for B in X:
                prod *= e[B]
            if prod != mv:
                bad += 1
    expect_fail("N2", bad == 0, "%d mismatches under the mutation" % bad)

    print()
    print("N3  compute qmass on the intervals of a FIXED labelling instead of L*.")
    print("    The two must differ on some poset -- otherwise L* is not load-bearing")
    print("    in the statistic and section 4 measures nothing about L*.")
    diff = same = 0
    for n in (5, 6):
        for P in all_posets(n):
            probs = pair_probs(P)
            if not probs or not tie_free(probs):
                continue
            order = lstar(P, probs)
            if order is None:
                continue
            e = e_all_subsets(P)
            Mm, cache = m_table(P, cache, e)
            a = qmass(P, order, Mm, e[(1 << n) - 1])
            b = qmass(P, list(range(n)), Mm, e[(1 << n) - 1])
            if a != b:
                diff += 1
            else:
                same += 1
    expect_fail("N3", diff == 0, "%d posets where the two differ, %d where they agree"
                % (diff, same))

    print()
    print("N4  a poset with a majority TIE must be refused a unique L*.")
    tied = 0
    refused = 0
    for P in all_posets(5):
        probs = pair_probs(P)
        if not probs or tie_free(probs):
            continue
        tied += 1
        if lstar(P, probs) is None:
            refused += 1
    expect_fail("N4", refused != tied,
                "%d tied posets, %d refused an L*" % (tied, refused))

    print()
    print("=" * 78)
    if FAILURES:
        print("FAILURES: %d" % len(FAILURES))
        for f in FAILURES:
            print("   " + f)
        return 1
    print("ALL CONTROLS PASS, AND ALL FOUR NEGATIVE CONTROLS FIRE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
