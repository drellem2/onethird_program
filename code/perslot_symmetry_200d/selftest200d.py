"""mg-200d selftest.  Exits 1 on any failure.

The controls that matter are S3, S5 and S7: they test the symmetry forms against REAL
posets (hand-named relations, uniform on their linear extensions), because the whole
finding of this instrument is that one family of forms is satisfied by real posets and
another is not.  S7 is the mutation: a deliberately reversed surrogate must FAIL on a real
poset, or S5 is passing vacuously.
"""

import sys
from fractions import Fraction as F
from itertools import permutations

from lp200d import (CAP, Infeasible, inv_count, relaxation, measure_report,
                    uniform_le_measure, solve_max, eps_spec)

fails = []


def check(name, ok, detail=""):
    print(f"  [{'ok ' if ok else 'FAIL'}] {name}{('  -- ' + detail) if detail else ''}")
    if not ok:
        fails.append(name)


# ---- hand-named relations on {0..n-1}, all with the identity as a linear extension.
POSETS = {
    "antichain n=3":   (3, set()),
    "chain n=3":       (3, {(0, 1), (1, 2), (0, 2)}),
    "V n=3 (0<1,0<2)": (3, {(0, 1), (0, 2)}),
    "L n=3 (0<2,1<2)": (3, {(0, 2), (1, 2)}),
    "antichain n=4":   (4, set()),
    "chain n=4":       (4, {(a, b) for a in range(4) for b in range(4) if a < b}),
    "2+2 n=4":         (4, {(0, 1), (2, 3)}),
    "N n=4":           (4, {(0, 1), (0, 3), (2, 3)}),
    "diamond n=4":     (4, {(0, 1), (0, 2), (0, 3), (1, 3), (2, 3)}),
}

print("=" * 74)
print("S0  simplex correctness on a hand-solved LP")
print("=" * 74)
# max 3x+2y s.t. x+y<=4, x+3y<=6, x<=3  ->  x=3,y=1, value 11
v, x = solve_max(2, [({0: F(1), 1: F(1)}, "<=", F(4)),
                     ({0: F(1), 1: F(3)}, "<=", F(6)),
                     ({0: F(1)}, "<=", F(3))], [F(3), F(2)])
check("S0a  inequality LP value 11", v == 11, f"got {v}, x={x}")
# equality + >= : max x s.t. x+y = 5, y >= 2  -> x = 3
v2, x2 = solve_max(2, [({0: F(1), 1: F(1)}, "==", F(5)),
                       ({1: F(1)}, ">=", F(2))], [F(1), F(0)])
check("S0b  two-phase LP value 3", v2 == 3, f"got {v2}, x={x2}")
# infeasible: x <= 1 and x >= 2
try:
    solve_max(1, [({0: F(1)}, "<=", F(1)), ({0: F(1)}, ">=", F(2))], [F(1)])
    check("S0c  infeasibility detected", False, "no exception raised")
except Infeasible:
    check("S0c  infeasibility detected", True)

print()
print("=" * 74)
print("S1  baseline reproduces mg-6bc2's theorem  (max E[inv] = C(n,2)/3)")
print("=" * 74)
for n in (3, 4, 5):
    val, mu = relaxation(n, "none")
    tgt = F(n * (n - 1), 6)
    rep = measure_report(n, mu)
    check(f"S1  n={n}  max E[inv] = C(n,2)/3 = {tgt}", val == tgt, f"got {val}")
    check(f"S1  n={n}  eps_spec = n/(n+1)", eps_spec(n, val) == F(n, n + 1),
          f"got {eps_spec(n, val)}")
    check(f"S1  n={n}  optimiser is a PROBABILITY measure", rep["mass"] == 1,
          f"mass {rep['mass']}")

print()
print("=" * 74)
print("S2  H7: mg-6bc2's n=3 optimiser is sub-probability, and completing it")
print("    turns its reported 0 AGGREGATE violations into 4")
print("=" * 74)
sub = {(0, 2, 1): F(1, 3), (1, 2, 0): F(1, 3)}
r_sub = measure_report(3, sub)
check("S2a  mg-6bc2's reported support has mass 2/3", r_sub["mass"] == F(2, 3),
      f"mass {r_sub['mass']}")
check("S2b  on that sub-measure, aggregate violations = 0",
      len(r_sub["agg_eq_violations"]) == 0, f"{r_sub['agg_eq_violations']}")
check("S2c  on that sub-measure, per-slot violations = 4",
      len(r_sub["slot_eq_violations"]) == 4, f"{len(r_sub['slot_eq_violations'])}")
full = dict(sub)
full[(0, 1, 2)] = F(1, 3)
r_full = measure_report(3, full)
check("S2d  completed to mass 1, E[inv] is unchanged at 1", r_full["E_inv"] == 1,
      f"{r_full['E_inv']}")
check("S2e  completed, aggregate violations > 0  (H7's substance)",
      len(r_full["agg_eq_violations"]) > 0,
      f"{[(x, y) for (x, y) in r_full['agg_eq_violations']]}")
check("S2f  ... and the count is 2 unordered pairs, NOT the 4 H7 predicted",
      len(r_full["agg_eq_violations"]) == 2,
      f"{len(r_full['agg_eq_violations'])} -- H7 is REFUTED on the number, kept as written")


def mg6bc2_aggregate_count(n, mu):
    """mg-6bc2's own aggregate predicate, transcribed from lp6bc2.py:measure_stats.

    It iterates the ORDERED adjacency keys actually present, so its unit is ordered pairs
    -- while its per-slot predicate (v2_optimiser.py) iterates x<y only.  The two columns
    of its §5 table are therefore not in the same unit.
    """
    adj = {}
    for p, w in mu.items():
        for k in range(n - 1):
            adj[(p[k], p[k + 1])] = adj.get((p[k], p[k + 1]), F(0)) + w
    return [(x, y) for (x, y) in adj
            if adj.get((x, y), F(0)) != adj.get((y, x), F(0))]


check("S2g  under mg-6bc2's OWN ordered predicate the completed count is 3, not 4",
      len(mg6bc2_aggregate_count(3, full)) == 3,
      f"{mg6bc2_aggregate_count(3, full)}")
check("S2h  its aggregate predicate counts ORDERED pairs and its per-slot predicate "
      "counts x<y -- different units in one table",
      len(mg6bc2_aggregate_count(3, sub)) == 0
      and len(r_sub["slot_eq_violations"]) == 4)

print()
print("=" * 74)
print("S3  H2: the LITERAL forms hold for uniform L(P) iff P is an antichain")
print("=" * 74)
for name, (n, rel) in POSETS.items():
    mu = uniform_le_measure(n, rel)
    rep = measure_report(n, mu)
    is_anti = (len(rel) == 0)
    ok_slot = (len(rep["slot_eq_violations"]) == 0)
    ok_agg = (len(rep["agg_eq_violations"]) == 0)
    check(f"S3  {name:18s} literal per-slot holds = {ok_slot} (antichain = {is_anti})",
          ok_slot == is_anti, f"{len(rep['slot_eq_violations'])} violations")
    check(f"S3  {name:18s} literal aggregate holds = {ok_agg} (antichain = {is_anti})",
          ok_agg == is_anti, f"{len(rep['agg_eq_violations'])} violations")

print()
print("=" * 74)
print("S4  H4: the literal PER-SLOT form is INFEASIBLE at n=3")
print("=" * 74)
try:
    v, mu = relaxation(3, "slot_eq")
    check("S4  literal per-slot at n=3 is infeasible", False, f"solved to {v}")
except Infeasible as e:
    check("S4  literal per-slot at n=3 is infeasible", True, str(e))
# and the reason: the six equalities force the uniform measure, whose flips are 1/2
unif = {p: F(1, 6) for p in permutations(range(3))}
ru = measure_report(3, unif)
check("S4b  uniform on S_3 satisfies the literal per-slot form",
      len(ru["slot_eq_violations"]) == 0)
check("S4c  ... and its pair flips are 1/2 > 1/3", ru["max_flip"] == F(1, 2),
      f"{ru['max_flip']}")

print()
print("=" * 74)
print("S5  H5: the SURROGATE forms are SOUND -- satisfied by every hand-named poset")
print("=" * 74)
for name, (n, rel) in POSETS.items():
    rep = measure_report(n, uniform_le_measure(n, rel))
    check(f"S5  {name:18s} J_k(y,x) <= J_k(x,y)", not rep["slot_le_violations"],
          f"{len(rep['slot_le_violations'])} violations")
    check(f"S5  {name:18s} J(y,x)   <= J(x,y)", not rep["agg_le_violations"],
          f"{len(rep['agg_le_violations'])} violations")

print()
print("=" * 74)
print("S6  the DISJUNCTIVE branch is exactly what realisability gives: for every")
print("    hand-named poset, its own comparability branch contains its own measure")
print("=" * 74)
for name, (n, rel) in POSETS.items():
    mu = uniform_le_measure(n, rel)
    rep = measure_report(n, mu)
    comp = {(x, y) for (x, y) in rel}
    # its measure must satisfy: comparable pairs never flipped, incomparable pairs symmetric
    bad_flip = [pr for pr in comp if pr not in rep["zero_flip_pairs"]]
    bad_sym = [(pr, k) for (pr, k) in rep["slot_eq_violations"] if pr not in comp]
    check(f"S6  {name:18s} comparable pairs have flip 0", not bad_flip, f"{bad_flip}")
    check(f"S6  {name:18s} incomparable pairs are per-slot symmetric", not bad_sym,
          f"{bad_sym}")

print()
print("=" * 74)
print("S7  MUTATION -- the reversed surrogate J_k(x,y) <= J_k(y,x) must FAIL on a real")
print("    poset, or S5 is passing vacuously")
print("=" * 74)
n_mut, rel_mut = POSETS["chain n=3"]
mu = uniform_le_measure(n_mut, rel_mut)
J = {}
for p, w in mu.items():
    for k in range(n_mut - 1):
        J[(k, p[k], p[k + 1])] = J.get((k, p[k], p[k + 1]), F(0)) + w
rev_bad = [((x, y), k) for x in range(n_mut) for y in range(x + 1, n_mut)
           for k in range(n_mut - 1)
           if J.get((k, x, y), F(0)) > J.get((k, y, x), F(0))]
check("S7a  reversed per-slot surrogate FAILS on the chain", len(rev_bad) > 0,
      f"{len(rev_bad)} violations -- the check is not vacuous")
rep_anti = measure_report(3, uniform_le_measure(3, set()))
check("S7b  ... and the antichain, which satisfies BOTH directions, is not in M_n",
      rep_anti["max_flip"] > CAP, f"max flip {rep_anti['max_flip']}")


print()
print("=" * 74)
print("S8  SOLVER INVARIANCE -- the headline values must not depend on pivot order")
print("=" * 74)
from itertools import permutations as _perms
from lp200d import build, solve_max, pairs_of


def value_with_orders(n, comp, row_rev, col_rev):
    """Same LP, constraint rows and/or columns reversed -> a different pivot sequence."""
    allp = [p for p in _perms(range(n))
            if not (set((i, j) for i in range(n) for j in range(i + 1, n)
                        if p.index(j) < p.index(i)) & set(comp))]
    if col_rev:
        allp = allp[::-1]
    perms, rows = build(n, "slot_eq", frozenset(comp), perms=allp)
    if row_rev:
        rows = rows[::-1]
    c = [F(inv_count(p)) for p in perms]
    v, _ = solve_max(len(perms), rows, c)
    return v


CASES = [(4, [(0, 2), (0, 3), (1, 3)], F(1)),
         (5, [(x, y) for (x, y) in pairs_of(5) if y - x > 1], F(4, 3))]
for n, comp, expect in CASES:
    vals = {(rr, cr): value_with_orders(n, comp, rr, cr)
            for rr in (False, True) for cr in (False, True)}
    check(f"S8  n={n} branch value {expect} under all 4 row/column orderings",
          set(vals.values()) == {expect}, f"{sorted(set(map(str, vals.values())))}")

print()
print("=" * 74)
print("S9  EXACTNESS OF eps_spec -- the check that would have caught the float path")
print("    (mg-41b7's audit note, repaired under mg-a1fe)")
print("=" * 74)
# Before the repair, eps_spec computed 6*e_inv/(n^2-1) with no conversion, so a plain
# Python int for e_inv returned a FLOAT.  It did not bite: measure_report accumulates
# E_inv from F(0), and every live call site passed a Fraction.  That is a CONVENTION HELD
# BY THE CALLERS, not a property of the function -- which is what these checks make it.
for e_int in (1, 2, 3):
    v = eps_spec(5, e_int)
    check(f"S9a  eps_spec(5, {e_int}) with a PYTHON INT returns a Fraction, not a float",
          isinstance(v, F), f"returned {v!r} of type {type(v).__name__}")

# The type is the symptom; this is the bite.  6/15 = 2/5 is NOT a dyadic rational, so the
# float path is not merely differently-typed here, it is a DIFFERENT NUMBER -- and this
# corpus compares exact rationals for EQUALITY.
check("S9b  eps_spec(4, 1) == 2/5 EXACTLY (a non-dyadic value, where float != rational)",
      eps_spec(4, 1) == F(2, 5), f"got {eps_spec(4, 1)!r}")
check("S9c  eps_spec(5, 1) == 1/4 and eps_spec(5, 2) == 1/2",
      eps_spec(5, 1) == F(1, 4) and eps_spec(5, 2) == F(1, 2),
      f"got {eps_spec(5, 1)!r}, {eps_spec(5, 2)!r}")

# MUTATION -- the pre-repair expression, run inline.  If this stops being a float that
# misses 2/5, S9a-S9c are testing nothing and the hazard they guard has ceased to exist.
pre_repair = 6 * 1 / (4 * 4 - 1)
check("S9d  MUTATION: the unconverted 6*e_inv/(n^2-1) IS a float and MISSES 2/5 -- so "
      "S9a-S9c are not vacuous",
      isinstance(pre_repair, float) and F(pre_repair) != F(2, 5),
      f"{pre_repair!r} -> {F(pre_repair)}")

# The Fraction path is unchanged, and the old convention still holds where it always did.
check("S9e  the Fraction path is untouched: eps_spec(n, C(n,2)/3) == n/(n+1) at n=3,4,5",
      all(eps_spec(n, F(n * (n - 1), 6)) == F(n, n + 1) for n in (3, 4, 5)))
check("S9f  measure_report's E_inv is a Fraction on int weights, zero weights and the "
      "empty measure -- the convention that USED to be the only guard",
      {type(measure_report(3, dict(a))["E_inv"]).__name__
       for a in ({}, {(0, 1, 2): 1, (2, 1, 0): 2}, {(0, 1, 2): 0},
                 {(0, 1, 2): F(1, 2), (2, 1, 0): F(1, 2)})} == {"Fraction"})

# NOT CLAIMED, and asserted so nobody reads more into the F() than it gives: converting
# the argument makes the RETURN TYPE a property of the function.  It does not launder a
# float ARGUMENT back into the rational the caller meant -- F(0.4) is the exact value of
# the double 0.4, which is not 2/5.  Keeping floats out of e_inv is still the caller's job.
v_float = eps_spec(4, 0.4)
check("S9g  a FLOAT argument still returns a Fraction but NOT the exact rational -- the "
      "conversion is a type guarantee, not a laundering",
      isinstance(v_float, F) and v_float != F(4, 25) and eps_spec(4, F(2, 5)) == F(4, 25),
      f"got {v_float}")

print()
print("=" * 74)
print(f"selftest: {'ALL PASS' if not fails else str(len(fails)) + ' FAILURES'}")
for f_ in fails:
    print(f"   FAILED: {f_}")
print("=" * 74)
sys.exit(1 if fails else 0)
