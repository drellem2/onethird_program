"""mg-131e D3 -- THE VERDICT: mg-200d's `<=` direction is FALSE at n = 6.

D1 certifies `val <= (n-1)/3` at n = 3, 4 and 5.  This script shows the same statement fails
at n = 6 and at every n from 6 to 10 that was checked, by EXHIBITING A FEASIBLE MEASURE that
beats it.  A feasible primal point is a LOWER bound on the branch optimum and needs no solver
to be believed: the witnesses below are hard-coded, and every property that makes one count is
re-checked here by direct arithmetic through `lp200d.measure_report` -- mg-200d's own
diagnostic, which contains no simplex.  Delete the LP entirely and this file still runs.

WHAT IS REFUTED, EXACTLY.  mg-200d's conjecture is that the maximum over branches of the
per-slot disjunctive LP equals `(n-1)/3`, i.e. `eps_spec = 2/(n+1)`.  The `>=` half is a
theorem (its 3-atom fence, checked at n = 3..20).  The `<=` half is what D1 certifies at
n = 3,4,5 and what dies here: at n = 6 the branch

    I = {(0,1),(1,2),(2,3),(3,4),(4,5)}  U  {(1,4)}

carries a feasible measure with `E[inv] = 11/6 > 5/3 = (n-1)/3`, so the maximum over branches
is at least `11/6` and `eps_spec >= 11/35 > 2/7`.

WHAT IS *NOT* REFUTED, AND MUST NOT BE READ INTO THIS.

 1. Nothing here touches the frozen-poset conjecture.  The disjunctive value is an UPPER bound
    on it; showing the upper bound is larger than believed weakens the bound, it does not make
    the underlying statement false.
 2. Nothing here refutes mg-200d's `Theta(n^2) -> Theta(n)` headline.  Every value below is
    still linear in n.  What dies is the CONSTANT, i.e. the exact formula, and with it the
    conjecture that would have been the LIB residual.
 3. Nothing here is an upper bound at n >= 6.  Each number is a lower bound found on a NAMED
    branch, so the true n = 6 maximum may be larger still.  The exhaustive n = 6 value is not
    computed and is not claimed (the ticket forbids extending the brute force, and 32768
    branches over 720 columns would not have fitted anyway).

THE BRANCH IS A REAL COMPARABILITY PATTERN.  mg-200d's branch family is a strict superset of
the comparability patterns of posets, because transitivity is never imposed -- which is what
keeps its value an upper bound, and which would have made a refutation on a non-transitive
branch much less interesting.  The n = 6 refuting branch's comparable set IS transitive, and
this file checks that rather than asserting it.  So the refutation is not an artefact of the
relaxation's slack over transitivity.
"""

import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "perslot_symmetry_200d"))

from lp200d import eps_spec, flips, inv_count, measure_report, pairs_of


# The witnesses.  Each is (chords, measure): the branch is `I = consecutive pairs U chords`,
# everything else comparable.  Found by mg-200d's LP on that branch, then FROZEN here so that
# re-checking them involves no solver at all.
WITNESSES = {
    6: (
        [(1, 4)],   # chords beyond the consecutive pairs;  value 11/6
        {
            (0, 1, 2, 3, 5, 4): F(1, 6),
            (0, 1, 3, 2, 5, 4): F(1, 6),
            (0, 2, 1, 4, 3, 5): F(1, 6),
            (0, 2, 4, 1, 3, 5): F(1, 6),
            (1, 0, 2, 3, 4, 5): F(1, 6),
            (1, 0, 3, 2, 4, 5): F(1, 6),
        }),
    7: (
        [(1, 4), (2, 5)],   # chords beyond the consecutive pairs;  value 20/9
        {
            (0, 1, 2, 3, 4, 5, 6): F(1, 9),
            (0, 1, 2, 4, 3, 5, 6): F(1, 9),
            (0, 1, 3, 5, 2, 4, 6): F(1, 9),
            (0, 2, 1, 3, 5, 4, 6): F(1, 9),
            (0, 2, 1, 4, 3, 6, 5): F(1, 9),
            (0, 2, 4, 1, 3, 6, 5): F(1, 9),
            (1, 0, 2, 3, 4, 6, 5): F(1, 9),
            (1, 0, 3, 2, 4, 5, 6): F(1, 9),
            (1, 0, 3, 2, 5, 4, 6): F(1, 9),
        }),
    8: (
        [(1, 4), (3, 6)],   # chords beyond the consecutive pairs;  value 8/3
        {
            (0, 1, 2, 3, 5, 4, 7, 6): F(1, 6),
            (0, 1, 3, 2, 5, 4, 6, 7): F(1, 6),
            (0, 2, 1, 4, 3, 6, 5, 7): F(1, 6),
            (0, 2, 4, 1, 6, 3, 5, 7): F(1, 6),
            (1, 0, 2, 3, 4, 5, 7, 6): F(1, 6),
            (1, 0, 3, 2, 4, 5, 6, 7): F(1, 6),
        }),
    9: (
        [(1, 4), (2, 5), (3, 6), (4, 7)],   # chords beyond the consecutive pairs;  value 28/9
        {
            (0, 1, 2, 3, 4, 5, 6, 8, 7): F(1, 9),
            (0, 1, 2, 4, 3, 5, 7, 6, 8): F(1, 9),
            (0, 1, 3, 5, 2, 7, 4, 6, 8): F(1, 9),
            (0, 2, 1, 3, 5, 4, 7, 6, 8): F(1, 9),
            (0, 2, 1, 4, 3, 6, 5, 8, 7): F(1, 9),
            (0, 2, 4, 1, 6, 3, 5, 8, 7): F(1, 9),
            (1, 0, 2, 3, 4, 6, 5, 7, 8): F(1, 9),
            (1, 0, 3, 2, 4, 5, 6, 7, 8): F(1, 9),
            (1, 0, 3, 2, 5, 4, 6, 7, 8): F(1, 9),
        }),
    10: (
        [(1, 4), (3, 6), (5, 8)],   # chords beyond the consecutive pairs;  value 7/2
        {
            (0, 1, 2, 3, 5, 4, 7, 6, 9, 8): F(1, 6),
            (0, 1, 3, 2, 5, 4, 6, 7, 9, 8): F(1, 6),
            (0, 2, 1, 4, 3, 6, 5, 8, 7, 9): F(1, 6),
            (0, 2, 4, 1, 6, 3, 8, 5, 7, 9): F(1, 6),
            (1, 0, 2, 3, 4, 5, 7, 6, 8, 9): F(1, 6),
            (1, 0, 3, 2, 4, 5, 6, 7, 8, 9): F(1, 6),
        }),
}


def is_transitive(comp):
    """Is the comparable set already a strict partial order?  (x<y and y<w) => x<w."""
    return all((x, w) in comp for (x, y) in comp for (z, w) in comp if y == z)


def main():
    print("=" * 84)
    print("D3  THE VERDICT -- mg-200d's `<=` direction is FALSE at n = 6.")
    print("    Every line is a FEASIBLE MEASURE checked by direct arithmetic, i.e. a LOWER bound")
    print("    on the branch optimum.  A lower bound above (n-1)/3 refutes; it never confirms.")
    print("=" * 84)

    allok = True
    refuted = []
    for n in sorted(WITNESSES):
        chords, mu = WITNESSES[n]
        cons = [(i, i + 1) for i in range(n - 1)]
        I = set(cons) | set(chords)
        C = frozenset(pr for pr in pairs_of(n) if pr not in I)
        target = F(n - 1, 3)
        rep = measure_report(n, mu)

        flipped = set()
        for p in mu:
            flipped |= flips(p)
        checks = {
            "is a probability measure": rep["mass"] == 1,
            "flip caps <= 1/3": rep["max_flip"] <= F(1, 3),
            "no COMPARABLE pair ever flipped": not (flipped & C),
            "per-slot symmetry holds on every pair of I":
                not [v for v in rep["slot_eq_violations"] if v[0] in I],
            "E[inv] recomputed from the atoms":
                rep["E_inv"] == sum(w * inv_count(p) for p, w in mu.items()),
        }
        ok = all(checks.values())
        allok = allok and ok
        beats = rep["E_inv"] > target
        if beats:
            refuted.append(n)

        print(f"\n### n = {n}   branch I = consecutive U {chords}"
              f"   |I| = {len(I)}   atoms {len(mu)}")
        print(f"    E[inv] = {rep['E_inv']} = {float(rep['E_inv']):.4f}"
              f"   against (n-1)/3 = {target} = {float(target):.4f}"
              f"   -> {'REFUTES' if beats else 'does not beat'}   excess = {rep['E_inv'] - target}")
        print(f"    eps_spec = {eps_spec(n, rep['E_inv'])} = {float(eps_spec(n, rep['E_inv'])):.6f}"
              f"   against the conjectured 2/(n+1) = {F(2, n + 1)} = {float(F(2, n + 1)):.6f}")
        for k, v in checks.items():
            print(f"      [{'OK ' if v else 'BAD'}] {k}")
        print(f"      [{'OK ' if is_transitive(C) else '!! '}] the comparable set is TRANSITIVE"
              f" -- a genuine poset comparability pattern, not a non-transitive branch")
        q = {pr: sum(w for p, w in mu.items() if pr in flips(p)) for pr in pairs_of(n)}
        print(f"      flip probabilities: "
              + ", ".join(f"{pr}={q[pr]}" for pr in sorted(q) if q[pr]))

    print()
    print("=" * 84)
    print(f"ALL WITNESS CHECKS PASS: {allok}")
    print(f"(n-1)/3 is BEATEN at n = {refuted}")
    print("So `max over branches = (n-1)/3` -- the `<=` direction D1 certifies at n = 3,4,5 --")
    print("is FALSE from n = 6 on.  The three exact points were a small-n coincidence.")
    print()
    print("The excess is not a rounding wobble and it GROWS.  On the periodic sub-family")
    print("chords = {(2j+1, 2j+4)}, the value is (5n-8)/12 at n = 6, 8, 10 -- checked, and")
    print("compare (n-1)/3 = (4n-4)/12.  The gap (n-4)/12 is LINEAR in n, so this is not a")
    print("boundary effect that a slightly different constant would absorb.")
    print("=" * 84)


if __name__ == "__main__":
    main()
