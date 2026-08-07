"""mg-ba78 -- self-test.  Positive AND negative controls, declared exit value 0.

A repair whose self-test only checks the repaired number is a vacuous pass: it
cannot tell a fixed predicate from a predicate that happens to agree.  So every
check below either asserts a value computed BY HAND before this instrument
existed, or is a MUTATION that must move a number in a stated direction.

The hand values, written out before any of this ran (n = 3, inv-optimiser):

  the LP returns mass 1/3 on (0,2,1) and 1/3 on (1,2,0) -- total 2/3, and the
  identity is absent because inv(identity) = 0 gives the simplex no reason to
  place the remaining third anywhere.  Completing it on the identity:

    adjacency masses A(0,1)=1/3  A(1,2)=2/3  A(0,2)=1/3  A(2,1)=1/3  A(2,0)=1/3
    unordered:  {0,1}: 1/3 vs 0     VIOLATED
                {1,2}: 2/3 vs 1/3   VIOLATED
                {0,2}: 1/3 vs 1/3   ok
    -> 2 of 3 unordered pairs, and the violated set is exactly {(0,1), (1,2)}.

    slot masses  J_0(0,1)=J_0(0,2)=J_0(1,2)=1/3;  J_1(1,2)=J_1(2,1)=J_1(2,0)=1/3
    k = 0: all three pairs one-directional  -> 3 violations
    k = 1: {1,2} balanced, {0,2} one-sided  -> 1 violation
    -> 4 (pair, slot)s, and 3 of 3 unordered pairs violated at some slot.
"""

import sys
from fractions import Fraction as F
from itertools import permutations

from lib_ba78 import (
    aggregate_violated_pairs, complete, expect, footrule, inv_count,
    lp_as_published, max_flip_prob, per_slot_violated_pair_slots,
    per_slot_violated_pairs, published_aggregate_count, total_mass, two_atom,
)

fails = []


def check(name, got, want):
    ok = got == want
    print(f"  {'PASS' if ok else 'FAIL'}  {name}: got {got}, want {want}")
    if not ok:
        fails.append(name)


print("T1  the defect is real and reproduces -- the LP returns a sub-probability measure")
val3, raw3 = lp_as_published(3, inv_count)
check("n=3 LP optimum", val3, F(1))
check("n=3 LP returned mass", total_mass(raw3), F(2, 3))
check("n=3 identity absent from the support", tuple(range(3)) in raw3, False)
for n in (4, 5, 6):
    check(f"n={n} LP mass is already 1 (defect 1 does NOT bite here)",
          total_mass(lp_as_published(n, inv_count)[1]), F(1))

print("T2  completion is a no-op on the theorem -- checked, not asserted")
for n in (3, 4, 5, 6):
    for obj in (inv_count, footrule):
        _, raw = lp_as_published(n, obj)
        done = complete(n, raw)
        check(f"n={n} mass after completion", total_mass(done), F(1))
        check(f"n={n} E[inv] unmoved by completion",
              expect(done, inv_count), expect(raw, inv_count))
        check(f"n={n} E[F] unmoved by completion",
              expect(done, footrule), expect(raw, footrule))
        check(f"n={n} still feasible after completion",
              max_flip_prob(n, done) <= F(1, 3), True)

print("T3  the repaired n=3 diagnostics, against the hand values in the docstring")
d3 = complete(3, raw3)
check("n=3 aggregate-violated pairs (set)", aggregate_violated_pairs(3, d3),
      [(0, 1), (1, 2)])
check("n=3 aggregate-violated count", len(aggregate_violated_pairs(3, d3)), 2)
check("n=3 per-slot violated (pair,slot)s",
      per_slot_violated_pair_slots(3, d3),
      [((0, 1), 0), ((0, 2), 0), ((0, 2), 1), ((1, 2), 0)])
check("n=3 per-slot violated pairs", len(per_slot_violated_pairs(3, d3)), 3)

print("T4  MUTATION -- withhold the completion and mg-6bc2's published 0 comes back")
check("uncompleted n=3, ordered predicate = the published 0",
      published_aggregate_count(3, raw3), 0)
check("uncompleted n=3, UNORDERED predicate is ALSO 0 -- so the unit fix alone "
      "would not have moved the headline",
      len(aggregate_violated_pairs(3, raw3)), 0)
check("completed n=3, ordered predicate = 3, not 2 -- so the unit fix is not "
      "cosmetic either", published_aggregate_count(3, d3), 3)

print("T5  MUTATION -- reproduce every published section 5 aggregate figure")
# mg-6bc2's table, transcribed from out_v2_optimiser.txt at 90d19e7 / e1f7bb2
PUBLISHED = {(3, "inv"): 0, (4, "inv"): 6, (5, "inv"): 8, (6, "inv"): 10,
             (3, "F"): 0, (4, "F"): 6, (5, "F"): 8, (6, "F"): 17}
for (n, key), want in sorted(PUBLISHED.items()):
    obj = inv_count if key == "inv" else footrule
    _, raw = lp_as_published(n, obj)
    check(f"published aggregate n={n} {key}", published_aggregate_count(n, raw), want)

print("T6  the two repaired columns NEST, and the inclusion is strict somewhere")
strict = 0
for n in (3, 4, 5, 6):
    for key, obj in (("inv", inv_count), ("F", footrule)):
        done = complete(n, lp_as_published(n, obj)[1])
        agg = set(aggregate_violated_pairs(n, done))
        ps = set(per_slot_violated_pairs(n, done))
        check(f"n={n} {key}: aggregate ⊆ per-slot", agg <= ps, True)
        if agg < ps:
            strict += 1
check("the inclusion is STRICT in at least one cell (the columns are not the "
      "same number renamed)", strict > 0, True)

print("T7  NEGATIVE CONTROL -- a measure that must violate NEITHER form")
# uniform on S_n is symmetric under every transposition of labels, so every
# adjacency mass is balanced at every slot.  If the detectors fire here they
# are not detecting asymmetry.
uni = {p: F(1, 24) for p in permutations(range(4))}
check("uniform: aggregate violations", len(aggregate_violated_pairs(4, uni)), 0)
check("uniform: per-slot violations", len(per_slot_violated_pair_slots(4, uni)), 0)
check("uniform is a probability measure", total_mass(uni), F(1))
check("uniform is INFEASIBLE for the frozen cap (so it is a control, not a "
      "witness)", max_flip_prob(4, uni), F(1, 2))

print("T8  NEGATIVE CONTROL -- a measure that must violate BOTH forms")
ta = two_atom(5)
check("two-atom: aggregate violations > 0",
      len(aggregate_violated_pairs(5, ta)) > 0, True)
check("two-atom: per-slot violations > 0",
      len(per_slot_violated_pair_slots(5, ta)) > 0, True)

print("T9  NEGATIVE CONTROL -- completing a measure that is already complete "
      "must change nothing")
check("complete(two-atom) is the same measure", complete(5, ta), ta)

print("T10 NEGATIVE CONTROL -- completion must REFUSE a super-probability measure")
try:
    complete(3, {(0, 1, 2): F(2)})
    check("complete() rejects mass > 1", "no exception", "ValueError")
except ValueError:
    check("complete() rejects mass > 1", "ValueError", "ValueError")

print()
if fails:
    print(f"SELFTEST FAILED: {fails}")
    sys.exit(1)
print("SELFTEST OK -- 10 blocks, 5 of them negative controls or mutations")
sys.exit(0)
