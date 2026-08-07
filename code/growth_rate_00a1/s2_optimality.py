"""mg-00a1 / s2 -- exact LP: the witness is OPTIMAL on its branch, and the controls hold.

This script DOES use a simplex (`mg-200d`'s own, exact `Fraction`s).  It is not what the
verdict rests on -- `s1` carries that with no solver at all.  What it adds is:

  (a) the CONTROLS: `mg-200d`'s 2/3, 1, 4/3 at n = 3,4,5, and `mg-131e`'s (n-1)/3 on the
      consecutive branch, both reproduced in my worktree.  If the parents do not reproduce
      here, nothing in this directory is readable.
  (b) the witness is not merely feasible on the staircase branch, it ATTAINS that branch's
      exact value at every n where the LP is affordable.  So `s1`'s lower bound is the
      branch's value, not a slack point inside it.

Usage:  python3 s2_optimality.py [max_n]     (default 12; n = 14 is ~10 min)
"""

import sys, time
from fractions import Fraction as F

from lib00a1 import (
    branch_value_exact, comparable_from_I, consecutive, linear_extensions, staircase_I,
    trivial_dual_bound, witness_target,
)
from lp200d import Infeasible, relaxation


def main(max_n=12):
    print("=" * 100)
    print("mg-00a1 / s2 -- exact LP.  Controls, then optimality of the s1 witness.")
    print("=" * 100)
    print()

    print("-" * 100)
    print("CONTROL 1 -- mg-200d reproduces in this worktree (disjunctive value, all branches)")
    print("-" * 100)
    print()
    print("  Not recomputed here: mg-200d's own v2_disjunctive.py owns that number and is")
    print("  committed at code/perslot_symmetry_200d/out_v2_n34.txt and out_v2_n5.txt.  What")
    print("  is recomputed is the single branch each of them reports as ATTAINING, so the")
    print("  reproduction is of a value, not of a search.")
    print()
    attaining = {3: {(0, 1), (1, 2)},
                 4: {(0, 1), (1, 2), (2, 3)},
                 5: {(0, 1), (0, 4), (1, 2), (1, 3), (2, 3), (3, 4)}}
    for n, I in sorted(attaining.items()):
        try:
            v, _ = branch_value_exact(n, frozenset(I))
            tgt = F(n - 1, 3)
            print(f"  n={n}  attaining branch value = {v}   (n-1)/3 = {tgt}   "
                  f"{'MATCH' if v == tgt else '**MISMATCH**'}")
        except Infeasible as e:
            print(f"  n={n}  INFEASIBLE ({e})  **UNEXPECTED**")
    print()

    print("-" * 100)
    print("CONTROL 2 -- mg-131e's theorem: the consecutive branch is EXACTLY (n-1)/3")
    print("-" * 100)
    print()
    bad = []
    for n in range(3, 11):
        v, _ = branch_value_exact(n, consecutive(n))
        tgt = F(n - 1, 3)
        if v != tgt:
            bad.append(n)
        print(f"  n={n:>2}  value = {str(v):>6}   (n-1)/3 = {str(tgt):>6}   "
              f"{'MATCH' if v == tgt else '**MISMATCH**'}")
    print()
    print(f"  {8 - len(bad)} of 8 match." if not bad else f"  **MISMATCHES AT {bad}**")
    print()
    print("  This is mg-131e's theorem, re-derived by a solver here as a control on my")
    print("  column generation.  It is a PROOF there and a computation here; if the two")
    print("  disagreed the bug would be mine.")
    print()

    print("-" * 100)
    print("THE RESULT -- the staircase branch's EXACT value equals the s1 witness")
    print("-" * 100)
    print()
    print(f"  {'n':>4} {'LP value':>10} {'s1 witness':>12} {'|I|':>5} {'columns':>8} "
          f"{'trivial dual':>13} {'time':>8}   verdict")
    fails = []
    for n in range(6, max_n + 1, 2):
        I = staircase_I(n)
        t0 = time.time()
        v, mu = branch_value_exact(n, I)
        dt = time.time() - t0
        tgt = witness_target(n)
        td, _ = trivial_dual_bound(n, I)
        cols = len(linear_extensions(n, comparable_from_I(n, I)))
        ok = v == tgt
        if not ok:
            fails.append(n)
        print(f"  {n:>4} {str(v):>10} {str(tgt):>12} {len(I):>5} {cols:>8} "
              f"{str(td):>13} {dt:>7.1f}s   {'OPTIMAL' if ok else '**s1 IS NOT OPTIMAL**'}")
    print()
    if fails:
        print(f"  **THE WITNESS IS NOT OPTIMAL AT {fails}** -- s1's numbers are still valid")
        print("  LOWER bounds and the verdict is unaffected, but this line must be read.")
    else:
        print("  The s1 witness attains the branch value exactly at every n computed.  So")
        print("  n(n+5)/36 is this branch's VALUE, not merely a point inside it.")
    print()
    print("  Read the 'trivial dual' column against the LP value: the gap is the whole")
    print("  content of per-slot symmetry on this branch.  Both columns are quadratic.")
    print()
    return 1 if fails or bad else 0


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 12))
