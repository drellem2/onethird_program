"""mg-ba78 R2 -- WHICH defect moved WHICH number.

Two defects were reported together, so "the number changed" does not say which
one changed it.  This crosses them: {uncompleted, completed} x {ordered-key
predicate, unordered-pair predicate}, four cells per (n, objective).  Reading
the 2x2 says, per n, whether the published figure was wrong because of the
missing mass, because of the unit, or both.

The answer is a clean split and it is worth having in the record, because the
two defects have different reach:

  * DEFECT 1 (sub-probability) bites at n = 3 ONLY.  That is the one that flips
    the headline, and it flips it from 0 -- the value that made the aggregate
    form look inert.
  * DEFECT 2 (unit) bites at EVERY n, including n = 3.  It is the one that makes
    the section 5 table a comparison rather than two unrelated columns.
"""

import sys
from fractions import Fraction as F

from lib_ba78 import (
    OBJECTIVES, aggregate_violated_pairs, complete, lp_as_published,
    published_aggregate_count, total_mass,
)

NS = [int(a) for a in sys.argv[1:]] or [3, 4, 5, 6]

print("=" * 78)
print("R2  DEFECT ISOLATION -- the 2x2 of {measure} x {predicate}")
print("    rows: the measure the diagnostic ran on")
print("    cols: ORDERED adjacency keys (mg-6bc2's) vs UNORDERED pairs (repaired)")
print("=" * 78)

verdicts = []

for n in NS:
    for name, obj in OBJECTIVES:
        _, raw = lp_as_published(n, obj)
        done = complete(n, raw)
        cell = {
            ("raw", "ordered"): published_aggregate_count(n, raw),
            ("raw", "unordered"): len(aggregate_violated_pairs(n, raw)),
            ("done", "ordered"): published_aggregate_count(n, done),
            ("done", "unordered"): len(aggregate_violated_pairs(n, done)),
        }
        mass_short = total_mass(raw) != F(1)
        d1 = cell[("raw", "unordered")] != cell[("done", "unordered")]
        d2 = cell[("done", "ordered")] != cell[("done", "unordered")]
        verdicts.append((n, name, cell[("raw", "ordered")],
                         cell[("done", "unordered")], mass_short, d1, d2))

        print(f"\n  n = {n},  max {name}   (LP mass {total_mass(raw)})")
        print(f"    {'':<26}{'ORDERED keys':>14}{'UNORDERED pairs':>18}")
        print(f"    {'sub-probability (as run)':<26}"
              f"{cell[('raw', 'ordered')]:>14}{cell[('raw', 'unordered')]:>18}"
              f"    <- top-left is what mg-6bc2 published")
        print(f"    {'completed (repaired)':<26}"
              f"{cell[('done', 'ordered')]:>14}{cell[('done', 'unordered')]:>18}"
              f"    <- bottom-right is what it should have said")
        print(f"    defect 1 (missing mass) moves this number: {'YES' if d1 else 'no'}")
        print(f"    defect 2 (wrong unit)   moves this number: {'YES' if d2 else 'no'}")

print("\n" + "=" * 78)
print("SUMMARY")
print("=" * 78)
print(f"{'n':>3} {'objective':<14} {'published':>9} {'repaired':>9} "
      f"{'mass<1':>7} {'d1 bites':>9} {'d2 bites':>9}")
for n, name, pub, rep, ms, d1, d2 in verdicts:
    print(f"{n:>3} {name:<14} {pub:>9} {rep:>9} "
          f"{('YES' if ms else 'no'):>7} {('YES' if d1 else 'no'):>9} "
          f"{('YES' if d2 else 'no'):>9}")

n3 = [v for v in verdicts if v[0] == 3]
rest = [v for v in verdicts if v[0] != 3]
print()
print(f"defect 1 bites at n = 3 in {sum(1 for v in n3 if v[5])} of {len(n3)} cells,"
      f" and at n > 3 in {sum(1 for v in rest if v[5])} of {len(rest)}")
print(f"defect 2 bites at n = 3 in {sum(1 for v in n3 if v[6])} of {len(n3)} cells,"
      f" and at n > 3 in {sum(1 for v in rest if v[6])} of {len(rest)}")
print()
print("Reading it precisely, because both defects touch n = 3 and only one of")
print("them can move the headline:")
print("  * ONLY DEFECT 1 CAN MOVE THE n = 3 NUMBER OFF ZERO.  The unordered")
print("    predicate on the UNCOMPLETED measure still reads 0, so the unit fix")
print("    alone would have left `the aggregate form excludes nothing` standing.")
print("    Completing the measure is what turns 0 into a violation; the unit")
print("    then decides whether it is reported as 3 or as 2.")
print("  * AT n > 3 the measure was already at mass 1, so the entire change in")
print("    the section 5 column is defect 2 -- and it is there at every n.")
sys.exit(0)
