"""mg-eaa1 -- controls for this audit's own instrument.  Exits 1 on any failure.

An audit that reports PASS is only worth the controls under it.  Seven groups, three of them
MUTATIONS, plus a hand-solved LP the solver is checked against and a positive control that the
verifier can reject.
"""

import sys
from fractions import Fraction as F
from itertools import permutations

import lib_eaa1 as L

fails = []


def ok(cond, msg):
    print(f"  [{'OK ' if cond else 'FAIL'}] {msg}")
    if not cond:
        fails.append(msg)


print("S1  combinatorics: inv == |flipped_pairs|, and the inversion set determines the perm")
for n in (4, 5):
    bad = [p for p in permutations(range(n)) if L.inv(p) != len(L.flipped_pairs(p))]
    ok(not bad, f"n={n}: inv(p) == |flipped_pairs(p)| for all {n}! perms")
    masks = {frozenset(L.flipped_pairs(p)) for p in permutations(range(n))}
    ok(len(masks) == len(list(permutations(range(n)))),
       f"n={n}: distinct perms have distinct inversion sets ({len(masks)} of "
       f"{len(list(permutations(range(n))))})")

print("\nS2  CROSS-IMPLEMENTATION: my primitives vs mg-200d's, on every permutation at n=5")
sys.path.insert(0, "../perslot_symmetry_200d")
import lp200d as P  # noqa: E402
bad = []
for p in permutations(range(5)):
    if L.inv(p) != P.inv_count(p):
        bad.append(("inv", p))
    if L.flipped_pairs(p) != P.flips(p):
        bad.append(("flips", p))
    if set(L.adjacencies(p)) != P.slot_adjacencies(p):
        bad.append(("adj", p))
    if L.footrule(p) != P.footrule(p):
        bad.append(("footrule", p))
ok(not bad, f"all four primitives agree with lp200d on all 120 perms at n=5 "
            f"({len(bad)} disagreements)")

print("\nS3  MY SIMPLEX reproduces the BASELINE mg-6bc2/mg-200d theorem: max E[inv] over M_n")
for n in (3, 4, 5):
    perms = list(permutations(range(n)))
    N = len(perms)
    fl = [L.flipped_pairs(p) for p in perms]
    rows = [({j: F(1) for j in range(N)}, "==", F(1))]
    for pr in L.all_pairs(n):
        rows.append(({j: F(1) for j in range(N) if pr in fl[j]}, "<=", F(1, 3)))
    val, _ = L.lp_max(N, rows, [F(L.inv(p)) for p in perms])
    ok(val == F(n * (n - 1), 6),
       f"n={n}: max E[inv] over M_n = {val} = C(n,2)/3 = {F(n * (n - 1), 6)}"
       f"   [eps_spec = {L.eps_spec(n, val)} = n/(n+1) = {F(n, n + 1)}]")

print("\nS4  A HAND-SOLVED LP, so the solver is checked against arithmetic and not itself")
# max 3a + 2b  s.t.  a + b = 1,  a <= 1/3,  a,b >= 0.   Optimum: a = 1/3, b = 2/3, value 7/3.
val, x = L.lp_max(2, [({0: F(1), 1: F(1)}, "==", F(1)), ({0: F(1)}, "<=", F(1, 3))],
                  [F(3), F(2)])
ok(val == F(7, 3) and x == [F(1, 3), F(2, 3)],
   f"hand LP: value {val} (hand: 7/3), x = {x} (hand: [1/3, 2/3])")
val2, y = L.dual_min([({0: F(1), 1: F(1)}, "==", F(1)), ({0: F(1)}, "<=", F(1, 3))],
                     [F(3), F(2)])
ok(val2 == F(7, 3) and L.verify_dual(
    [({0: F(1), 1: F(1)}, "==", F(1)), ({0: F(1)}, "<=", F(1, 3))], [F(3), F(2)], y).ok,
   f"hand LP dual: min y.b = {val2} = 7/3, y = {y} (hand: lam = 2, t = 1)")

print("\nS5  THE TRIVIAL DUAL's ALGEBRAIC STEP, checked rather than trusted:")
print("    every column of every branch has flips(p) contained in I_active, which is WHY")
print("    the dual constraint holds with equality and the bound is |I_active|/3.")
for n in (3, 4):
    bad = 0
    for C in L.all_branches(n):
        cols = L.columns(n, C)
        if not cols:
            continue
        act = set(L.active_pairs(n, C))
        for p in cols:
            if not (L.flipped_pairs(p) <= act):
                bad += 1
    ok(bad == 0, f"n={n}: flips(p) subset I_active on every column of every branch "
                 f"({bad} exceptions)")

print("\nS6  MUTATIONS -- the checkers must REJECT.  Three of them.")
n = 6
I = list(L.consecutive(n)) + [(1, 4)]
C = frozenset(pr for pr in L.all_pairs(n) if pr not in set(I))
MU = {(0, 1, 2, 3, 5, 4): F(1, 6), (0, 1, 3, 2, 5, 4): F(1, 6), (0, 2, 1, 4, 3, 5): F(1, 6),
      (0, 2, 4, 1, 3, 5): F(1, 6), (1, 0, 2, 3, 4, 5): F(1, 6), (1, 0, 3, 2, 4, 5): F(1, 6)}
ok(L.check_measure(n, MU, C)["ok"], "positive control: the n=6 witness passes unmutated")

m1 = dict(MU)
m1.pop((1, 0, 2, 3, 4, 5))
r1 = L.check_measure(n, m1, C)
ok(not r1["ok"] and not r1["checks"]["total mass is exactly 1"]
   and not r1["checks"]["per-slot symmetry on every incomparable pair"],
   f"MUTATION 1 (delete an atom): rejected on BOTH mass and per-slot symmetry "
   f"({len(r1['sym_violations'])} symmetry violations)")

m2 = dict(MU)
m2[(2, 1, 0, 3, 5, 4)] = F(0)          # a zero-mass atom must change nothing
r2 = L.check_measure(n, m2, C)
ok(r2["ok"] and r2["E_inv"] == F(11, 6),
   "CONTROL (add a zero-mass atom): still passes and E[inv] is unchanged -- the checker "
   "is not keyed on the atom LIST")

m3 = {(0, 1, 2, 3, 5, 4): F(1, 2), (0, 1, 3, 2, 5, 4): F(1, 2)}
r3 = L.check_measure(n, m3, C)
ok(not r3["ok"] and r3["checks"]["total mass is exactly 1"]
   and not r3["checks"]["every incomparable flip probability <= 1/3"],
   f"MUTATION 2 (a mass-1 measure that BREAKS the cap): rejected on the cap and NOT on "
   f"mass -- over_cap = {r3['over_cap']}")

m4 = dict(MU)
m4[(0, 2, 1, 4, 3, 5)] = F(1, 12)
m4[(3, 0, 1, 2, 4, 5)] = F(1, 12)      # flips (0,3),(1,3),(2,3): (0,3) and (2,3) are COMPARABLE
r4 = L.check_measure(n, m4, C)
ok(not r4["ok"] and not r4["checks"]["no comparable pair carries flip mass"],
   f"MUTATION 3 (mass on a COMPARABLE flip): rejected -- "
   f"comparable pairs flipped = {r4['comparable_flipped']}")

print("\nS7  THE SOLVER's FAILURE MODES are distinguished, not collapsed")
try:
    L.lp_max(1, [({0: F(1)}, "<=", F(1)), ({0: F(1)}, ">=", F(2))], [F(1)])
    ok(False, "an infeasible system was solved")
except L.NoSolution:
    ok(True, "an infeasible system raises NoSolution (x <= 1 and x >= 2)")
except L.Unbounded:
    ok(False, "an infeasible system raised Unbounded")
try:
    L.lp_max(1, [({0: F(1)}, ">=", F(1))], [F(1)])
    ok(False, "an unbounded system was solved")
except L.Unbounded:
    ok(True, "an unbounded system raises Unbounded (max x s.t. x >= 1)")

print("\nS8  WEAK DUALITY holds numerically wherever both objects exist")
bad = 0
for n in (3, 4):
    for C in L.all_branches(n):
        perms, rows, c, labels = L.program(n, C)
        if not perms:
            continue
        cert = L.verify_dual(rows, c, L.trivial_dual(rows, labels))
        try:
            val, _ = L.branch_value(n, C)
        except L.NoSolution:
            continue
        if val > cert.bound:
            bad += 1
ok(bad == 0, f"primal optimum <= trivial dual bound on every feasible branch at n=3,4 "
             f"({bad} violations)")

print()
print(f"SELFTEST RESULT: {'ALL CONTROLS PASS' if not fails else str(len(fails)) + ' FAILURES'}")
for f in fails:
    print("   FAILED:", f)
sys.exit(1 if fails else 0)
