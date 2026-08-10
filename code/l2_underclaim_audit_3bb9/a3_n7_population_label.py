"""a3 — the LABEL mg-b58d's repair 3 put on the two `n = 7` populations, checked against
the code that produced them.

Repair 3 exists because §4.2's `n = 7` row was a different sample from §4.1's and §4.3's and
that was unstated.  The repaired labels read:

    §4   "`sample_posets(7, 90)` (40 primitive) feeds §4.2, and `sample_posets(7, 200)`
          (106 primitive) feeds §4.1 and §4.3"
    §4.1 "106 primitive of 200 drawn"          §4.2 "40 primitive of 90 drawn"
    §4.3 "106 primitive of 200 drawn"          §8.1 item 3 "draw / primitive: 200 / 106, 90 / 40"

But `b1_footrule.py:73`, `b2_census.py:138` and `b5_trend.py:48` all evaluate

    named_posets(7) + sample_posets(7, k)

so the population is the NAMED FAMILIES UNION the draw.  This script asks lib28ff itself how
many posets that is and where the primitive ones come from.  It uses mg-28ff's own
`named_posets`/`sample_posets`, which is the point: a label is checked against its own code.
"""
import sys
sys.path.insert(0, "../l2_conditionality_28ff")
import lib28ff as L                                       # noqa: E402

print("=" * 92)
print("a3  the `n = 7` population labels, against `lib28ff`'s own generators")
print("=" * 92)
named = L.named_posets(7)
np_prim = sum(1 for P in named if P.is_primitive())
print()
print(f"named_posets(7):            {len(named):>4} posets, {np_prim:>4} primitive")
for k, sections in ((90, "§4.2 (b2_census.py:138)"), (200, "§4.1, §4.3 (b1_footrule.py:73, b5_trend.py:48)")):
    samp = L.sample_posets(7, k)
    both = named + samp
    s_prim = sum(1 for P in samp if P.is_primitive())
    b_prim = sum(1 for P in both if P.is_primitive())
    seen = {}
    dups = []
    for P in both:
        key = frozenset(P.rel)
        if key in seen:
            dups.append(P)
        seen[key] = P
    d_prim = sum(1 for P in dups if P.is_primitive())
    print()
    print(f"  {sections}")
    print(f"    sample_posets(7, {k}):      {len(samp):>4} posets, {s_prim:>4} primitive")
    print(f"    named + sample (the population actually evaluated):"
          f" {len(both):>4} entries, {b_prim:>4} primitive")
    print(f"    duplicate entries: {len(dups)} (primitive among them: {d_prim});"
          f" DISTINCT posets {len(seen)}")
    print(f"    -> the document's \"{b_prim} primitive of {k} drawn\" attributes to the DRAW a")
    print(f"       primitive count that the draw supplies {s_prim} of; the remaining"
          f" {b_prim - s_prim} come from the")
    print(f"       NAMED FAMILIES, which are chosen, not drawn.  Population size is"
          f" {len(both)}, not {k}.")
print()
print("Corroboration from inside the same document: §3 reports the footrule identity")
print("machine-checked at \"all 5230 posets `n <= 6` and 98 at `n = 7`\" — 98 IS")
print("len(named_posets(7)) + len(sample_posets(7, 90)), i.e. §3 states the union size")
print("correctly while §4/§4.1/§4.2/§4.3/§8.1 state the draw size instead.")
print("=" * 92)
