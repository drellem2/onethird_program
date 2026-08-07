"""mg-131e D1 -- THE DUAL CERTIFICATES for mg-200d's `<=` direction at n = 3, 4, 5.

The `<=` direction is `val(C) <= (n-1)/3` for EVERY branch `C`, so the certificate is a
family covering all `2^C(n,2)` branches, not one certificate.  Each branch is discharged by a
dual vector `y` that

  * satisfies the sign conditions and `sum_i y_i A_ij >= c_j` on every column, checked by
    DIRECT ARITHMETIC in `lib131e.verify_dual`, which calls no simplex, and
  * has `y . b <= (n-1)/3`.

Certificates are searched in TIERS, cheapest first, and the tier a branch needs is the whole
point: a branch discharged at tier 0 is discharged by a formula that is a THEOREM at every n,
and one that needs tier 2 is discharged by a number a solver found at this n only.

  tier 0  TRIVIAL      lambda = 0, t = 1 on every cap row, s = 0.  Bound |I_active|/3.
                       Dual-feasible in EVERY branch at EVERY n -- proved, not computed.
  tier 1  CONSECUTIVE  t = indicator of the pairs (i,i+1), lambda minimised, s free.
                       Bound (#consecutive pairs in I)/3 + lambda.  Also a formula in n.
  tier 2  SOLVER       any dual with objective <= (n-1)/3, found by LP.  NOT a formula.

For the primal-FEASIBLE branches the exact dual optimum is also computed and checked against
mg-200d's primal optimum -- strong duality across two independently written LP runs, which is
the strongest available control on the whole construction.

A dual on a primal-INFEASIBLE branch is VACUOUS: it bounds a maximum over the empty set.
Those are counted separately and never used as evidence of a pattern (PREDICTIONS P12).
"""

import sys
import time
from fractions import Fraction as F

from lib131e import (active_pairs, all_branches, branch_class, branch_lp, budgeted_dual,
                     consecutive_dual, incomparable, solve_dual, trivial_dual, verify_dual)
from lp200d import pairs_of

NS = [int(a) for a in sys.argv[1:]] or [3, 4, 5]


# ------------------------------------------------------------------ the run

print("=" * 82)
print("D1  DUAL CERTIFICATES for the `<=` direction of mg-200d's disjunctive value.")
print("    Every branch is discharged by a dual vector verified by DIRECT ARITHMETIC")
print("    (lib131e.verify_dual -- no simplex).  The TIER a branch needs is the finding.")
print("=" * 82)

for n in NS:
    target = F(n - 1, 3)
    t0 = time.time()
    tiers = {0: 0, 1: 0, 2: 0, "none": 0}
    cls = {}
    tier_by_class = {}
    worst_certified = F(0)
    attaining = []
    strong_duality_checked = 0
    nbranch = 0
    hard = []

    print(f"\n### n = {n}   target (n-1)/3 = {target}   branches 2^C(n,2) = {2 ** len(pairs_of(n))}")
    for C in all_branches(n):
        nbranch += 1
        perms, rows, c = branch_lp(n, C)
        kind, val, mu = branch_class(n, C)
        cls[kind] = cls.get(kind, 0) + 1

        tier, y = None, None
        y0 = trivial_dual(rows)
        chk0 = verify_dual(rows, c, y0)
        assert chk0.ok, f"TRIVIAL DUAL FAILED at n={n} C={sorted(C)}: {chk0}"   # PREDICTIONS P2
        if chk0.bound <= target:
            tier, y, chk = 0, y0, chk0
        else:
            y1 = consecutive_dual(n, C, rows, c)
            if y1 is not None:
                chk1 = verify_dual(rows, c, y1)
                assert chk1.ok, f"consecutive dual not feasible at n={n} C={sorted(C)}"
                if chk1.bound <= target:
                    tier, y, chk = 1, y1, chk1
            if tier is None:
                y2 = budgeted_dual(rows, c, target)
                if y2 is None:
                    tier, y, chk = "none", None, None
                else:
                    chk2 = verify_dual(rows, c, y2)
                    assert chk2.ok, f"budgeted dual not feasible at n={n} C={sorted(C)}"
                    tier, y, chk = 2, y2, chk2
        tiers[tier] = tiers.get(tier, 0) + 1
        tier_by_class[(kind, tier)] = tier_by_class.get((kind, tier), 0) + 1
        if tier != "none":
            assert chk.bound <= target, (sorted(C), chk.bound)
            worst_certified = max(worst_certified, chk.bound)
        if tier == 2 and kind in ("zero", "positive"):
            hard.append((sorted(C), kind, val, chk0.bound))

        if kind in ("zero", "positive"):
            dval, dy = solve_dual(rows, c)
            dchk = verify_dual(rows, c, dy)
            assert dchk.ok and dchk.bound == dval
            assert dval == val, f"STRONG DUALITY FAILED n={n} C={sorted(C)}: {dval} vs {val}"
            strong_duality_checked += 1
            if val == target:
                attaining.append((sorted(C), len(incomparable(n, C)),
                                  len(active_pairs(n, C)), chk0.bound, tier))

    print(f"  branches visited                : {nbranch}")
    print(f"  primal classes                  : " +
          ", ".join(f"{k}={v}" for k, v in sorted(cls.items())))
    print(f"  strong duality (dual opt == mg-200d's primal opt) checked on : "
          f"{strong_duality_checked} feasible branches, 0 failures")
    print(f"  certificate tier needed         : "
          f"tier0(trivial, a theorem at all n)={tiers.get(0,0)}  "
          f"tier1(consecutive, a formula in n)={tiers.get(1,0)}  "
          f"tier2(solver, no formula)={tiers.get(2,0)}  none={tiers.get('none',0)}")
    print(f"  every branch certified at <= {target} : "
          f"{'YES' if tiers.get('none', 0) == 0 else 'NO'}"
          f"   (max certified bound over branches = {worst_certified})")
    print("  tier x primal class (a tier-2 certificate on an INFEASIBLE branch is VACUOUS):")
    for key in sorted(tier_by_class, key=str):
        print(f"      {str(key):28s} {tier_by_class[key]}")
    print(f"  FEASIBLE branches needing tier 2 (the ONLY informative hard cases): {len(hard)}")
    for row in hard:
        print(f"      C={row[0]}  {row[1]}  val={row[2]}  trivial bound={row[3]}")
    print(f"  branches attaining the max {target}: {len(attaining)}")
    for cc, ni, na, tb, tr in attaining:
        print(f"      C={cc}  |I|={ni} active={na}  trivial bound={tb}  tier={tr}")
    print(f"  [{time.time() - t0:.1f}s]")
    sys.stdout.flush()

print()
print("=" * 82)
print("READ THIS BEFORE QUOTING ANY NUMBER ABOVE.  These certificates prove `<= (n-1)/3` at")
print("n = 3, 4 and 5 ONLY.  D3 shows the same statement is FALSE at n = 6, so the tier")
print("counts here are a description of three points, not the beginning of a proof.")
print("=" * 82)
