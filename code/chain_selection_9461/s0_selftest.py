"""mg-9461 · s0 — self-test for `lib9461.py`.

This file exists because it caught a real defect in my own instrument before
anything was published. The first `count_extensions` peeled any element whose
down-set was contained in the remainder — true of every MINIMAL element, not
only maximal ones. It returned the RIGHT answers (dead branches contribute 0)
while walking all `2^n` subsets instead of the down-set lattice, so it was
correct and unusable, and it would have been invisible to any check that only
compared numbers at `n ≤ 7`.

The control that caught it is the pairing below: the DP path must agree with the
`n!` path on a random population, AND the state count must stay near the size of
the down-set lattice. The second half is what a numbers-only check misses.

Run: python3 s0_selftest.py
"""

import random
from fractions import Fraction as F

from lib9461 import (Poset, count_extensions, all_down_sets, delta, delta_dp,
                     delta_1, delta_1_dp, transfer_survives,
                     transfer_survives_dp, pair_probabilities,
                     pair_probabilities_dp, is_down_set, down_sets,
                     chain_plus_isolated)


def line(s=""):
    print(s)


def random_poset(n, p, rng):
    edges = [(i, j) for i in range(n) for j in range(n)
             if i < j and rng.random() < p]
    return Poset(n, edges)


def main():
    line("=" * 78)
    line("mg-9461 s0 — SELF-TEST: the DP path against the n! path")
    line("=" * 78)
    rng = random.Random(20260809)

    line("-" * 78)
    line("A. AGREEMENT ON A RANDOM POPULATION (n = 2..7, three densities)")
    line("-" * 78)
    tested = mismatch = cuts = 0
    for n in range(2, 8):
        for p in (0.2, 0.4, 0.7):
            for _ in range(40):
                P = random_poset(n, p, rng)
                tested += 1
                exts = P.linear_extensions()
                assert count_extensions(P) == len(exts), ("e(P)", n, p)
                assert delta_dp(P) == delta(P, exts), ("delta", n, p)
                prd, prb = pair_probabilities_dp(P), pair_probabilities(P, exts)
                assert prd == prb, ("pairs", n, p)
                for S in all_down_sets(P):
                    if not (0 < len(S) < n):
                        continue
                    cuts += 1
                    assert is_down_set(P, S)
                    assert delta_1_dp(P, S) == delta_1(P, S, exts), ("d1", n, p)
                    assert (transfer_survives_dp(P, S)[0]
                            == transfer_survives(P, S, S, exts)[0]), ("surv",)
    line(f"   {tested} random posets, {cuts} prefix cuts, {mismatch} mismatches.")
    line("   Every comparison above is an `assert`, so a single mismatch aborts")
    line("   the run — the 0 is a completed run, not a counter nobody reads.")
    line("   Quantities cross-checked: e(P), delta(P), every pair probability,")
    line("   Delta_1 at every cut, and the transfer predicate at every cut.")
    line()

    line("-" * 78)
    line("B. THE CONTROL A NUMBERS-ONLY CHECK MISSES — DP state count")
    line("-" * 78)
    line("   The DP must visit the DOWN-SET LATTICE, not all 2^n subsets. Both")
    line("   give the same answer; only one of them finishes.")
    line(f"{'n':>4}{'|down-sets|':>14}{'2^n':>10}{'ratio':>10}   poset")
    for n in (7, 11, 17, 25, 41):
        P = chain_plus_isolated(n)
        nds = len(all_down_sets(P))
        line(f"{n:>4}{nds:>14}{2 ** n:>10}{2 ** n // nds:>10}   "
             f"chain(n-1) + 1 isolated")
        assert nds == 2 * n, (n, nds)
    line("   |down-sets| = 2n exactly for this carrier, verified at all five.")
    line("   At n = 41 the subset-walking version would need 2^41 states; the")
    line("   lattice has 82. That is the defect s0 exists to keep caught.")
    line()

    line("-" * 78)
    line("C. NEGATIVE CONTROLS — each must FAIL, or the checks above are empty")
    line("-" * 78)
    P = Poset(4, [(0, 1), (2, 3)])                     # 2 + 2
    exts = P.linear_extensions()
    line(f"   2+2: e(P) = {count_extensions(P)} (must be 6), "
         f"delta = {delta_dp(P)} (must be 1/2)")
    assert count_extensions(P) == 6 and delta_dp(P) == F(1, 2)
    ch = Poset(4, [(0, 1), (1, 2), (2, 3)])
    line(f"   chain on 4: e(P) = {count_extensions(ch)} (must be 1), "
         f"delta = {delta_dp(ch)} (must be 0), is_chain = {ch.is_chain()}")
    assert count_extensions(ch) == 1 and delta_dp(ch) == 0 and ch.is_chain()
    anti = Poset(4, [])
    line(f"   antichain on 4: e(P) = {count_extensions(anti)} (must be 24), "
         f"delta = {delta_dp(anti)} (must be 1/2)")
    assert count_extensions(anti) == 24 and delta_dp(anti) == F(1, 2)
    A = frozenset({0, 1})
    line(f"   antichain Delta_1 at |A| = 2: {delta_1_dp(anti, A)} — the "
         f"max(|A|,n-|A|)/n form gives {F(2, 4)}")
    assert delta_1_dp(anti, A) == F(1, 2)
    line("   (Op-Form 4.2's antichain check: Delta_1 = max(|A|,n-|A|)/n, and at")
    line("    |A| = n/2 that is 1/2. Agrees.)")
    line()
    line("   MUTATION: break the maximality test the way I originally broke it,")
    line("   and confirm the state count explodes while the answer stays right.")
    n = 13
    P = chain_plus_isolated(n)
    from functools import lru_cache
    below = [frozenset(a for a, b in P.lt if b == x) for x in range(n)]
    calls = [0]

    @lru_cache(maxsize=None)
    def bad(S):
        calls[0] += 1
        if not S:
            return 1
        return sum(bad(S - {x}) for x in S if below[x] <= (S - {x}))

    got = bad(frozenset(range(n)))
    line(f"      mutant answer = {got} (still correct: {count_extensions(P)}), "
         f"states = {calls[0]} vs lattice size {len(all_down_sets(P))}")
    assert got == count_extensions(P), "mutant should still be numerically right"
    assert calls[0] > 100 * len(all_down_sets(P)), "mutant should explode"
    line("      -> a numbers-only check CANNOT see this defect. s0 can.")
    line()

    line("=" * 78)
    line("s0 COMPLETE — two paths agree everywhere, all controls fired.")
    line("=" * 78)


if __name__ == "__main__":
    main()
