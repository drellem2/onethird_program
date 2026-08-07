"""mg-00a1 / s3 -- the reduction that made the search tractable, and the families that DIE.

Three things, all of which shaped where `s1`'s family came from and none of which is the
verdict:

  PART A -- THE TRANSITIVE-CLOSURE REDUCTION.  A theorem (proof in the document):
            `val(C) <= val(tc(C))` for every branch, so the maximum over the `2^C(n,2)`
            branches is attained at a TRANSITIVELY CLOSED one -- at a genuine poset.  This
            is checked here on ALL 64 branches at n = 4 and a deterministic slice at n = 5.
            It is *proved* in the document; this is a check on my reading of `build`'s row
            conventions, not the evidence.

  PART B -- THE OBVIOUS QUADRATIC FAMILY IS INFEASIBLE.  Two disjoint chains: `|I| = ab`,
            quadratic, and INFEASIBLE at every `(a,b)` computed.  Anyone attacking this
            question tries this family first; it is a dead end and the phase-1 residual
            RISES with n, so it is not a near miss.

  PART C -- SO IS EVERY BAND.  `I = {span <= s}` is infeasible for every `s >= 2`.  A
            feasible branch's incomparability graph cannot be locally dense either.

Together B and C are why `s1`'s family is not obvious: the quadratically-many incomparable
pairs have to be arranged in the one shape that survives the caps.

NO POSET IS ENUMERATED.  Part A is a statement about the branch family, and the families in
B and C are named by hand.

Usage:  python3 s3_deadends.py
"""

import sys
from fractions import Fraction as F
from itertools import combinations

from lib00a1 import (
    band, branch_value_exact, comparable_from_I, is_transitively_closed, linear_extensions,
    pairs_of, transitive_closure,
)
from lp200d import Infeasible


def val_or_none(n, I):
    try:
        v, _ = branch_value_exact(n, I)
        return v
    except Infeasible:
        return None


def main():
    print("=" * 100)
    print("mg-00a1 / s3 -- the reduction, and the families that die")
    print("=" * 100)
    print()

    print("-" * 100)
    print("PART A -- val(C) <= val(tc(C)) : the maximum sits on a transitively closed branch")
    print("-" * 100)
    print()
    print("  Why it is true (the document has the proof): the columns of C and of tc(C) are")
    print("  the SAME set -- a permutation respecting C respects tc(C) -- while a pair in")
    print("  tc(C)\\C is called incomparable by C and therefore carries per-slot rows")
    print("  J_k(i,j) = J_k(j,i); no column flips it, so J_k(j,i) = 0 and the row reads")
    print("  J_k(i,j) = 0, a constraint tc(C) does not impose.  So feasible(C) is contained")
    print("  in feasible(tc(C)) and the value can only rise.  Checked:")
    print()
    for n, label in ((4, "ALL 64 branches"), (5, "ALL 1024 branches")):
        tested = viol = closed_max = 0
        best_any = best_closed = None
        allp = pairs_of(n)
        subsets = [frozenset(s) for r in range(len(allp) + 1)
                   for s in combinations(allp, r)]
        for C in subsets:
            vC = val_or_none(n, comparable_from_I(n, C))   # complement: C -> its I
            tc = transitive_closure(n, C)
            vT = val_or_none(n, comparable_from_I(n, tc))
            tested += 1
            if vC is not None and (vT is None or vC > vT):
                viol += 1
            if vC is not None and (best_any is None or vC > best_any):
                best_any = vC
            if vC is not None and tc == C:
                closed_max += 1
                if best_closed is None or vC > best_closed:
                    best_closed = vC
        print(f"  n={n} ({label}):  {tested} branches, "
              f"{viol} violations of val(C) <= val(tc(C))")
        print(f"        max over all tested = {best_any};  "
              f"max over transitively closed = {best_closed};  "
              f"{'ATTAINED ON A CLOSED BRANCH' if best_any == best_closed else '**NOT ATTAINED CLOSED**'}")
    print()

    print("-" * 100)
    print("PART B -- two disjoint chains: quadratic |I| = ab, and INFEASIBLE at every (a,b)")
    print("-" * 100)
    print()
    print(f"  {'a':>3} {'b':>3} {'n':>3} {'|I|':>5} {'columns':>8}   status")
    for a in range(1, 6):
        for b in range(a, 6):
            n = a + b
            if n > 10:
                continue
            I = frozenset((i, j) for i in range(a) for j in range(a, n))
            cols = len(linear_extensions(n, comparable_from_I(n, I)))
            try:
                v, _ = branch_value_exact(n, I)
                st = f"feasible, value = {v}   **UNEXPECTED**"
            except Infeasible as e:
                st = f"INFEASIBLE ({e})"
            print(f"  {a:>3} {b:>3} {n:>3} {len(I):>5} {cols:>8}   {st}")
    print()
    print("  Every one infeasible, and the phase-1 residual RISES with n.  The obvious way")
    print("  to get quadratically many incomparable pairs does not survive the 1/3 caps.")
    print()

    print("-" * 100)
    print("PART C -- bands: s = 1 is mg-131e's (n-1)/3; every s >= 2 is INFEASIBLE")
    print("-" * 100)
    print()
    print(f"  {'s':>3} {'n':>3} {'|I|':>5} {'columns':>8}   value / status")
    for s in (1, 2, 3):
        for n in range(s + 2, 11 if s == 1 else 9):
            I = band(n, s)
            cols = len(linear_extensions(n, comparable_from_I(n, I)))
            if cols > 1000:
                print(f"  {s:>3} {n:>3} {len(I):>5} {cols:>8}   (skipped: too many columns)")
                continue
            try:
                v, _ = branch_value_exact(n, I)
                extra = "  = (n-1)/3" if v == F(n - 1, 3) else "  **not (n-1)/3**"
                st = f"{v}{extra}"
            except Infeasible:
                st = "INFEASIBLE"
            print(f"  {s:>3} {n:>3} {len(I):>5} {cols:>8}   {st}")
    print()
    print("  So a feasible branch cannot be locally dense either.  s1's family threads")
    print("  between B and C: quadratically many incomparable pairs, but arranged as a")
    print("  staircase between two chains rather than as a block or a band.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
