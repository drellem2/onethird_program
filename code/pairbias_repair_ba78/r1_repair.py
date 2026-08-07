"""mg-ba78 R1 -- reproduce mg-6bc2's section 5 numbers, then repair them.

Prints, for every (n, objective) mg-6bc2 published:

  * the mass the LP actually returned, and the deficit;
  * that COMPLETING the measure moves neither objective and keeps the cap --
    i.e. the theorem is untouched, checked rather than asserted;
  * the PUBLISHED aggregate/per-slot pair, reproduced through mg-6bc2's own
    predicate on the uncompleted measure (so a difference below is a difference
    of predicate and measure, not of arithmetic);
  * the REPAIRED pair, both columns on UNORDERED pairs of a probability measure,
    with the (pair, slot) count kept as a third, separately labelled column;
  * the nesting check aggregate-violated ⊆ per-slot-violated.
"""

import sys

from lib_ba78 import OBJECTIVES, row

NS = [int(a) for a in sys.argv[1:]] or [3, 4, 5, 6]

print("=" * 78)
print("R1  mg-6bc2 SECTION 5, REPRODUCED THEN REPAIRED")
print("    defect 1: the LP normalises with `sum mu <= 1`, so it returns a")
print("              SUB-probability measure and the diagnostics ran on it")
print("    defect 2: the aggregate predicate iterated ORDERED adjacency keys,")
print("              the per-slot one iterated x < y -- two units, one table")
print("=" * 78)

rows = {}
bad = []

for n in NS:
    print(f"\n{'-' * 78}\nn = {n}")
    for name, obj in OBJECTIVES:
        r = row(n, obj)
        rows[(n, name)] = r
        print(f"\n  max {name} = {r['opt']}")
        print(f"    mass returned by the LP      = {r['mass_raw']}"
              f"   ({'SUB-PROBABILITY' if r['mass_raw'] != 1 else 'already a probability measure'})")
        print(f"    mass after completion        = {r['mass_done']}"
              f"   support {r['support_raw']} -> {r['support_done']} permutations")
        print(f"    E[inv]  before -> after      = {r['E_inv_raw']} -> {r['E_inv_done']}"
              f"   {'UNCHANGED' if r['E_inv_raw'] == r['E_inv_done'] else 'MOVED  <-- THEOREM AFFECTED'}")
        print(f"    E[F]    before -> after      = {r['E_F_raw']} -> {r['E_F_done']}"
              f"   {'UNCHANGED' if r['E_F_raw'] == r['E_F_done'] else 'MOVED  <-- THEOREM AFFECTED'}")
        print(f"    max flip prob after          = {r['maxflip_done']}"
              f"   {'<= 1/3, still feasible' if r['maxflip_done'] <= __import__('fractions').Fraction(1, 3) else 'INFEASIBLE'}")
        print(f"    PUBLISHED  aggregate = {r['pub_aggregate']:>3} ordered keys"
              f"      per-slot = {r['pub_per_slot']:>3} (pair,slot)s   <- two units")
        print(f"    REPAIRED   aggregate = {r['agg_pairs']:>3} / {r['n_pairs']} unordered pairs"
              f"   per-slot = {r['ps_pairs']:>3} / {r['n_pairs']} unordered pairs")
        print(f"               per-slot (finer) = {r['ps_pair_slots']} / {r['n_pair_slots']} (pair,slot)s")
        print(f"    nesting aggregate ⊆ per-slot : {'OK' if r['nested'] else 'FAILED'}")
        if r['E_inv_raw'] != r['E_inv_done'] or r['E_F_raw'] != r['E_F_done']:
            bad.append(f"objective moved at n={n} {name}")
        if not r['nested']:
            bad.append(f"nesting failed at n={n} {name}")

print("\n" + "=" * 78)
print("REPAIRED SECTION 5 TABLE -- every count is UNORDERED PAIRS of a")
print("PROBABILITY measure; the (pair,slot) column is a different unit and says so")
print("=" * 78)
hdr = (f"{'n':>3} | {'pairs':>5} | {'inv agg':>7} {'inv p-s':>7} | "
       f"{'F agg':>7} {'F p-s':>7} | {'inv p-s (pair,slot)':>19} {'F p-s (pair,slot)':>17}")
print(hdr)
print("-" * len(hdr))
for n in NS:
    ri = rows[(n, "E[inv_e]")]
    rf = rows[(n, "E[footrule]")]
    print(f"{n:>3} | {ri['n_pairs']:>5} | {ri['agg_pairs']:>7} {ri['ps_pairs']:>7} | "
          f"{rf['agg_pairs']:>7} {rf['ps_pairs']:>7} | "
          f"{ri['ps_pair_slots']:>19} {rf['ps_pair_slots']:>17}")

print("\n" + "=" * 78)
print("WHAT MOVED AGAINST WHAT mg-6bc2 PUBLISHED")
print("=" * 78)
print(f"{'n':>3} | {'published agg (ordered keys, sub-prob)':>38} | "
      f"{'repaired agg (unordered pairs, prob)':>36}")
for n in NS:
    ri = rows[(n, "E[inv_e]")]
    print(f"{n:>3} | {ri['pub_aggregate']:>38} | {ri['agg_pairs']:>36}")

print()
if bad:
    print(f"R1 FAILED: {bad}")
    sys.exit(1)
print("R1 OK -- completion moved no objective value and broke no feasibility,")
print("         and the two repaired columns nest at every (n, objective).")
sys.exit(0)
