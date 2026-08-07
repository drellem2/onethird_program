"""mg-eaa1 A1 -- AUDIT CHECK 2: is the certified program the RIGHT program?

A dual certificate for an INFEASIBLE program is vacuous and looks exactly like a clean
result.  mg-200d's theorem says the LITERAL all-pairs formulation IS infeasible -- per-slot
symmetry on EVERY pair holds for uniform L(P) iff P is an antichain, and no antichain is in
M_n.  So the single cheapest way for mg-131e to have produced an impressive-looking nothing
is to have certified that program.  This script decides it, four ways:

  A1.1  MY row builder against mg-200d's, on the branches that matter.  A certificate is a
        certificate FOR A ROW SET.  If my rows differ from the ones mg-131e verified against,
        nothing I say downstream transfers.  Multiset AND order are compared.
  A1.2  The LITERAL program (comparable = {}) at n = 3,4,5, on MY simplex.  Expected:
        INFEASIBLE.  This is the trap, computed rather than trusted.
  A1.3  The branches mg-131e reports as ATTAINING at n = 3,4,5: non-empty comparable set,
        primal-FEASIBLE, and attaining exactly (n-1)/3.
  A1.4  mg-200d's published witnesses, checked by SUBSTITUTION in my own arithmetic -- mass,
        caps, comparable-pairs-unflipped, per-slot symmetry, objective.  No solver.
"""

import sys
from fractions import Fraction as F

import lib_eaa1 as L

NS = [int(a) for a in sys.argv[1:]] or [3, 4, 5]

# The attaining branches and witnesses AS PUBLISHED by mg-200d (out_v2_n34.txt, out_v2_n5.txt)
# and echoed by mg-131e's d1.  Transcribed here by hand so that the check is a check.
ATTAINING = {
    3: (frozenset({(0, 2)}),
        {(0, 1, 2): F(1, 3), (0, 2, 1): F(1, 3), (1, 0, 2): F(1, 3)}),
    4: (frozenset({(0, 2), (0, 3), (1, 3)}),
        {(0, 1, 2, 3): F(1, 3), (0, 2, 1, 3): F(1, 3), (1, 0, 3, 2): F(1, 3)}),
    5: (frozenset({(0, 2), (0, 3), (1, 4), (2, 4)}),
        {(0, 1, 2, 3, 4): F(1, 3), (0, 2, 1, 4, 3): F(1, 3), (1, 0, 3, 2, 4): F(1, 3)}),
}

# The other three branches mg-131e's d1 reports as also attaining 4/3 at n = 5.
EXTRA_ATTAINING_5 = [
    frozenset({(0, 2), (0, 3), (0, 4), (1, 4), (2, 4)}),
    frozenset({(0, 2), (0, 3), (1, 3), (1, 4), (2, 4)}),
    frozenset({(0, 2), (0, 3), (0, 4), (1, 3), (1, 4), (2, 4)}),
]

fails = []


def ok(cond, msg):
    print(f"  [{'OK ' if cond else 'FAIL'}] {msg}")
    if not cond:
        fails.append(msg)
    return cond


print("=" * 86)
print("A1.1  MY ROW BUILDER vs mg-200d's `lp200d.build` -- same program or not")
print("=" * 86)
probe = []
for n in NS:
    probe.append((n, frozenset()))                       # the LITERAL all-pairs program
    probe.append((n, ATTAINING[n][0]))                   # the attaining branch
    probe.append((n, frozenset(L.consecutive(n))))       # NOTE: this names the COMPARABLE set
    probe.append((n, frozenset(pr for pr in L.all_pairs(n) if pr not in L.consecutive(n))))
if 6 in NS or True:
    cons6 = set(L.consecutive(6))
    I6 = cons6 | {(1, 4)}
    probe.append((6, frozenset(pr for pr in L.all_pairs(6) if pr not in I6)))
for n, C in probe:
    same_ms, same_ord, mine, theirs = L.rows_agree_with_lp200d(n, C)
    if same_ms is None:
        print(f"  n={n} |C|={len(C)}: no column survives -- both builders decline")
        continue
    ok(bool(same_ms), f"n={n} |C|={len(C)}: row MULTISETS identical "
                      f"({len(mine)} rows mine, {len(theirs)} theirs)")
    ok(bool(same_ord), f"n={n} |C|={len(C)}: row ORDER identical too "
                       f"(so a multiplier vector is index-comparable)")

print()
print("=" * 86)
print("A1.2  THE LITERAL ALL-PAIRS PROGRAM (comparable = {}) -- mg-200d says INFEASIBLE.")
print("      A dual certificate for THIS would look clean and mean nothing.")
print("=" * 86)
for n in NS:
    kind, val, _ = L.classify_branch(n, frozenset())
    ok(kind == "infeasible",
       f"n={n}: literal per-slot program on ALL pairs is {kind.upper()}"
       f"{'' if val is None else f' (value {val})'}  -- expected infeasible")

print()
print("=" * 86)
print("A1.3  THE BRANCHES mg-131e REPORTS AS ATTAINING -- feasible, disjunctive, attaining")
print("=" * 86)
for n in NS:
    C, _ = ATTAINING[n]
    target = F(n - 1, 3)
    kind, val, mu = L.classify_branch(n, C)
    ok(len(C) > 0, f"n={n}: certified branch has a NON-EMPTY comparable set "
                   f"({sorted(C)}) -- it is the DISJUNCTIVE program, not the literal one")
    ok(kind == "positive", f"n={n}: that branch is primal-FEASIBLE with a positive value "
                           f"(class={kind})")
    ok(val == target, f"n={n}: my own simplex gives val = {val}, target (n-1)/3 = {target}")
    ok(L.is_transitive(C) == (n < 5),
       f"n={n}: comparable set transitive = {L.is_transitive(C)} "
       f"(mg-200d reports transitive at n=3,4 and NOT at n=5)")
for C in EXTRA_ATTAINING_5:
    kind, val, _ = L.classify_branch(5, C)
    ok(kind == "positive" and val == F(4, 3),
       f"n=5 extra attaining branch {sorted(C)}: class={kind} val={val} (expect positive 4/3)")

print()
print("=" * 86)
print("A1.4  mg-200d's WITNESSES BY SUBSTITUTION -- no solver anywhere in this block")
print("=" * 86)
for n in NS:
    C, mu = ATTAINING[n]
    rep = L.check_measure(n, mu, C)
    for k, v in rep["checks"].items():
        ok(v, f"n={n}: {k}")
    ok(rep["E_inv"] == F(n - 1, 3),
       f"n={n}: E[inv] of the witness = {rep['E_inv']} = (n-1)/3 = {F(n - 1, 3)}"
       f"   [eps_spec = {L.eps_spec(n, rep['E_inv'])}, conjectured 2/(n+1) = {F(2, n + 1)}]")

print()
print("=" * 86)
print("A1.5  THE >= DIRECTION, SEPARATELY -- mg-200d's 3-atom fence rebuilt from its")
print("      DESCRIPTION (identity + the two adjacent matchings) and checked on the")
print("      CONSECUTIVE-PAIRS branch at n = 3..12.  This is a LOWER bound and nothing else.")
print("=" * 86)
for n in range(3, 13):
    I = set(L.consecutive(n))
    C = frozenset(pr for pr in L.all_pairs(n) if pr not in I)
    mu = L.fence(n)
    rep = L.check_measure(n, mu, C)
    ok(rep["ok"] and rep["E_inv"] == F(n - 1, 3),
       f"n={n:2d}: fence is feasible on the consecutive branch and E[inv] = {rep['E_inv']}"
       f" = (n-1)/3")

print()
print("=" * 86)
print(f"A1 RESULT: {'ALL CHECKS PASS' if not fails else str(len(fails)) + ' FAILURES'}")
for f in fails:
    print("   FAILED:", f)
print("=" * 86)
sys.exit(1 if fails else 0)
