"""mg-131e -- controls.  Exits 1 on any failure.

The load-bearing object in this instrument is `verify_dual`.  Everything else can be wrong
and be caught; if the VERIFIER is wrong, every certificate in D1 is a certificate for
nothing.  So the controls here are weighted towards it, and half of them are MUTATIONS: a
check that only ever passes is not a check, which is `mg-200d`'s own defect #1 in this
corpus's memory.
"""

import sys
from fractions import Fraction as F

from lib131e import (Infeasible, active_pairs, all_branches, branch_class, branch_columns,
                     branch_lp, budgeted_dual, cap_pairs_of_branch, consecutive_dual,
                     consecutive_pairs, row_kind, solve_dual, trivial_dual, verify_dual)
from lp200d import flips, inv_count, measure_report, pairs_of, relaxation
from d3_refutation import WITNESSES, is_transitive

FAILS = []


def check(name, cond, detail=""):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{('  -- ' + detail) if detail else ''}")
    if not cond:
        FAILS.append(name)


print("=" * 80)
print("S1  The verifier against a HAND-SOLVED LP whose answer is known without a solver.")
print("=" * 80)
# max 2x + 3y  s.t.  x + y <= 1,  x,y >= 0.   Optimum 3 at (0,1).  Dual: y1 = 3.
rows = [({0: F(1), 1: F(1)}, "<=", F(1))]
c = [F(2), F(3)]
check("valid dual y=(3) verifies with bound 3", bool(verify_dual(rows, c, [F(3)])) and
      verify_dual(rows, c, [F(3)]).bound == 3)
check("SLACK dual y=(4) also verifies, with the weaker bound 4",
      bool(verify_dual(rows, c, [F(4)])) and verify_dual(rows, c, [F(4)]).bound == 4)
check("MUTATION: y=(2) is REJECTED (it would 'prove' 2 < 3)",
      not verify_dual(rows, c, [F(2)]))
check("MUTATION: a NEGATIVE multiplier on a `<=` row is REJECTED",
      not verify_dual(rows, c, [F(-3)]))

print()
print("=" * 80)
print("S2  mg-200d's headline reproduced on this worktree (control -- if this fails,")
print("    nothing else in the instrument is readable).")
print("=" * 80)
for n, want in ((3, F(2, 3)), (4, F(1)), (5, F(4, 3))):
    best = None
    for C in all_branches(n):
        try:
            v, _ = relaxation(n, "slot_eq", comparable=C)
        except Infeasible:
            continue
        if best is None or v > best:
            best = v
    check(f"n={n}: disjunctive per-slot max = {want}", best == want, f"got {best}")

print()
print("=" * 80)
print("S3  The TRIVIAL dual is feasible in EVERY branch (PREDICTIONS H2/P2).  It is a")
print("    proof, so a failure here is a sign-convention bug in me (P13), not in H2.")
print("=" * 80)
for n in (3, 4):
    bad = 0
    for C in all_branches(n):
        perms, rws, cc = branch_lp(n, C)
        if not verify_dual(rws, cc, trivial_dual(rws)).ok:
            bad += 1
    check(f"n={n}: trivial dual verifies on all {2 ** len(pairs_of(n))} branches", bad == 0,
          f"{bad} failures")

print()
print("=" * 80)
print("S4  MUTATION on a real branch: a certificate that is valid must STOP being valid")
print("    when a single multiplier is nudged the wrong way.")
print("=" * 80)
n = 4
C = frozenset({(0, 2), (0, 3), (1, 3)})
perms, rws, cc = branch_lp(n, C)
y = trivial_dual(rws)
check("the trivial dual is valid here", bool(verify_dual(rws, cc, y)))
capi = [i for i, r in enumerate(rws) if row_kind(r) == "cap"]
y2 = list(y)
y2[capi[0]] -= F(1, 100)
check("MUTATION: shaving 1/100 off one cap multiplier is REJECTED",
      not verify_dual(rws, cc, y2))
y3 = list(y)
y3[capi[0]] = F(-1)
check("MUTATION: a negative cap multiplier is REJECTED on sign grounds",
      verify_dual(rws, cc, y3).sign_violations != [])
y4 = list(y)
y4[0] += F(1)
check("adding 1 to lambda stays valid but WEAKENS the bound by exactly 1",
      verify_dual(rws, cc, y4).ok and
      verify_dual(rws, cc, y4).bound == verify_dual(rws, cc, y).bound + 1)

print()
print("=" * 80)
print("S5  CROSS-BRANCH control: a certificate for one branch must not be accepted for")
print("    another.  Without this, 'verified' could mean 'verified against the wrong LP'.")
print("=" * 80)
Ca = frozenset({(0, 2), (0, 3), (1, 3)})
Cb = frozenset({(0, 3)})
pa, ra, ca = branch_lp(4, Ca)
pb, rb, cb = branch_lp(4, Cb)
ya = trivial_dual(ra)
check("row counts differ, so the vectors are not interchangeable",
      len(ra) != len(rb), f"{len(ra)} vs {len(rb)}")
try:
    verify_dual(rb, cb, ya)
    ok = False
except AssertionError:
    ok = True
check("verify_dual REFUSES a multiplier vector of the wrong length", ok)

print()
print("=" * 80)
print("S6  STRONG DUALITY across two independently written LP runs: the dual optimum from")
print("    `solve_dual` must equal mg-200d's primal optimum from `relaxation`, on every")
print("    feasible branch at n = 3 and n = 4.")
print("=" * 80)
for n in (3, 4):
    tested = bad = 0
    for C in all_branches(n):
        kind, val, _ = branch_class(n, C)
        if kind not in ("zero", "positive"):
            continue
        perms, rws, cc = branch_lp(n, C)
        dv, dy = solve_dual(rws, cc)
        tested += 1
        if dv != val or not verify_dual(rws, cc, dy).ok:
            bad += 1
    check(f"n={n}: dual opt == primal opt on all {tested} feasible branches", bad == 0,
          f"{bad} mismatches")

print()
print("=" * 80)
print("S7  The D3 witnesses: every refutation check must be MUTATION-SENSITIVE.  A witness")
print("    with a broken mass, a broken cap or a broken symmetry must be caught.")
print("=" * 80)
n6, mu6 = 6, dict(WITNESSES[6][1])
rep = measure_report(n6, mu6)
check("the shipped n=6 witness passes: mass 1, cap 1/3, E[inv] = 11/6",
      rep["mass"] == 1 and rep["max_flip"] <= F(1, 3) and rep["E_inv"] == F(11, 6))
bad_mass = dict(mu6)
k0 = sorted(bad_mass)[0]
bad_mass[k0] = bad_mass[k0] + F(1, 100)
check("MUTATION: mass 1 + 1/100 is caught", measure_report(n6, bad_mass)["mass"] != 1)
bad_cap = {sorted(mu6)[0]: F(1, 2), sorted(mu6)[1]: F(1, 2)}
check("MUTATION: a 1/2-1/2 measure breaks the flip cap",
      measure_report(n6, bad_cap)["max_flip"] > F(1, 3))
cons6 = set(consecutive_pairs(6)) | {(1, 4)}
drop = dict(mu6)
drop.pop(sorted(drop)[0])
tot = sum(drop.values())
drop = {p: w / tot for p, w in drop.items()}
r2 = measure_report(6, drop)
check("MUTATION: deleting one atom breaks per-slot symmetry on I",
      [v for v in r2["slot_eq_violations"] if v[0] in cons6] != [])

print()
print("=" * 80)
print("S8  The refuting branches are genuine comparability patterns, and the refutation")
print("    is checked to be strict, not a tie.")
print("=" * 80)
for n in sorted(WITNESSES):
    chords, mu = WITNESSES[n]
    I = set(consecutive_pairs(n)) | set(chords)
    C = frozenset(pr for pr in pairs_of(n) if pr not in I)
    rep = measure_report(n, mu)
    flipped = set()
    for p in mu:
        flipped |= flips(p)
    check(f"n={n}: witness feasible, comparable set transitive, E[inv] > (n-1)/3",
          rep["mass"] == 1 and rep["max_flip"] <= F(1, 3) and not (flipped & C)
          and not [v for v in rep["slot_eq_violations"] if v[0] in I]
          and is_transitive(C) and rep["E_inv"] > F(n - 1, 3),
          f"E[inv]={rep['E_inv']} vs {F(n - 1, 3)}")

print()
print("=" * 80)
print("S9  The cap-row labelling used by the consecutive dual must line up with the rows")
print("    `lp200d.build` actually emitted -- an off-by-one here silently relabels every")
print("    multiplier in D1's tier 1.")
print("=" * 80)
for n in (3, 4):
    bad = 0
    for C in all_branches(n):
        perms, rws, cc = branch_lp(n, C)
        caps = cap_pairs_of_branch(n, C)
        if sum(1 for r in rws if row_kind(r) == "cap") != len(caps):
            bad += 1
        for pr in caps:
            if not any(pr in flips(p) for p in perms):
                bad += 1
    check(f"n={n}: cap-row count matches the replayed cap-pair list on every branch",
          bad == 0, f"{bad} mismatches")

print()
print("=" * 80)
if FAILS:
    print(f"FAILURES: {len(FAILS)}")
    for f in FAILS:
        print("   -", f)
    sys.exit(1)
print("ALL CONTROLS PASS")
print("=" * 80)
