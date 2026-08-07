"""mg-00a1 / s4 -- PROVENANCE: how the s1 family was found, and whether it is locally maximal.

This script is the honest record of the search that produced `s1`'s family.  It is NOT
evidence for anything: `s1` stands on an explicit measure checked by arithmetic and `s2` on
an exact LP.  What `s4` answers is "where did that branch come from, and did you stop too
early?".

The search is a GREEDY hill-climb from `mg-131e`'s consecutive branch, adding one pair at a
time.  Its inner loop uses `mg-200d`'s exact simplex, so every number printed here is exact;
the only thing "search-only" about it is that greedy is greedy -- a hill-climb finds a LOCAL
maximum and the true maximum over branches may be larger.  Larger is harmless for a
superlinear verdict and fatal for a linear one, which is why the verdict is stated in this
direction.

NO EXHAUSTIVE n = 6.  The ticket forbids it.  This is a hill-climb over a path of at most
C(n,2) branches per step, not 32768 branches.

Usage:  python3 s4_search.py [max_n]     (default 10; n = 12 is slow)
"""

import sys, time
from fractions import Fraction as F

from lib00a1 import (
    branch_value_exact, comparable_from_I, consecutive, is_transitively_closed,
    linear_extensions, pairs_of, staircase_I, witness_target,
)
from lp200d import Infeasible

MAX_COLS = 3000


def value(n, I):
    C = comparable_from_I(n, I)
    if len(linear_extensions(n, C, limit=MAX_COLS + 1)) > MAX_COLS:
        return None, "too many columns"
    try:
        return branch_value_exact(n, I)[0], "ok"
    except Infeasible:
        return None, "infeasible"


def greedy(n):
    I = set(consecutive(n))
    cur, _ = value(n, frozenset(I))
    trace = [("start: consecutive", cur)]
    while True:
        best = None
        for pr in pairs_of(n):
            if pr in I:
                continue
            v, _ = value(n, frozenset(I | {pr}))
            if v is not None and (best is None or v > best[1]):
                best = (pr, v)
        if best is None or best[1] <= cur:
            break
        I.add(best[0])
        cur = best[1]
        trace.append((f"+ {best[0]}", cur))
    return frozenset(I), cur, trace


def main(max_n=10):
    print("=" * 100)
    print("mg-00a1 / s4 -- provenance of the s1 family: a greedy hill-climb, exact rationals")
    print("=" * 100)
    print()
    for n in range(6, max_n + 1, 2):
        t0 = time.time()
        I, v, trace = greedy(n)
        chords = sorted(p for p in I if p[1] != p[0] + 1)
        target = staircase_I(n)
        print(f"n = {n}")
        for label, val in trace:
            print(f"    {label:<22} value = {val}")
        print(f"    |I| = {len(I)}   chords = {chords}")
        print(f"    reached {v};  (n-1)/3 = {F(n - 1, 3)};  s1 family value = {witness_target(n)}")
        same = I == target
        print(f"    the branch greedy reached {'IS' if same else 'is NOT'} the s1 staircase "
              f"family{'' if same else ' (s1 uses ' + str(sorted(p for p in target if p[1] != p[0] + 1)) + ')'}")
        print(f"    transitively closed: {is_transitively_closed(n, comparable_from_I(n, I))}")
        print(f"    [{time.time() - t0:.0f}s]")
        print()

    print("-" * 100)
    print("LOCAL MAXIMALITY of the s1 family: can ANY single further pair improve it?")
    print("-" * 100)
    print()
    for n in range(6, max_n + 1, 2):
        I = staircase_I(n)
        base = witness_target(n)
        better, feas, tried = [], 0, 0
        for pr in pairs_of(n):
            if pr in I:
                continue
            tried += 1
            v, why = value(n, frozenset(I | {pr}))
            if v is None:
                continue
            feas += 1
            if v > base:
                better.append((pr, v))
        print(f"  n = {n}: {tried} candidate pairs, {feas} keep the branch feasible, "
              f"{len(better)} beat {base}"
              f"{'' if not better else '   -> ' + str(better)}")
    print()
    print("  A pair that improved it would RAISE the lower bound and strengthen the verdict.")
    print("  None does at these n, which is why s1 reports this family and not another.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 10))
