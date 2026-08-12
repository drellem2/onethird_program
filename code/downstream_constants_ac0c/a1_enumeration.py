"""mg-ac0c `a1` — THE ENUMERATION. Every step and every constant between L1b's conclusion
and the final contradiction, one row each, with its status, its value-or-hole, its scope and
its source.

**This is the ticket's deliverable even if nothing else gets done**, which is why it is `a1`
and why it depends on nothing but `libac0c`.
"""

import libac0c as L

print("=" * 100)
print("a1 §A — THE ENUMERATION: L1b's conclusion → the contradiction")
print("=" * 100)
print()

for r in L.ROWS:
    print(f"[{r.key}] {r.step:<18} {r.what}")
    print(f"      STATUS : {r.status}")
    print(f"      VALUE  : {r.value_str()}")
    print(f"      SCOPE  : {r.scope}")
    print(f"      SOURCE : {r.source}")
    if r.hole:
        print(f"      PIN/HOLE: {r.hole}")
    print()

print("=" * 100)
print("a1 §B — CENSUS by status")
print("=" * 100)
total = len(L.ROWS)
print(f"  rows: {total}")
for s in L.ORDER:
    ks = [r.key for r in L.ROWS if r.status == s]
    print(f"    {s:<10} {len(ks):>2}   rows {' '.join(ks) if ks else '—'}")

print()
proved_uncond = [r for r in L.ROWS if r.status == L.PROVED]
print(f"  PROVED UNCONDITIONALLY: {len(proved_uncond)} of {total} "
      f"= {100*len(proved_uncond)//total}%")
print(f"  NOT proved unconditionally: {total - len(proved_uncond)} of {total}")

print()
print("=" * 100)
print("a1 §C — THE HOLES: every row whose status is ABSENT, and whether it GATES the chain")
print("=" * 100)
for r in L.ROWS:
    if r.status == L.ABSENT:
        print(f"  [{r.key}] {r.what}")
        print(f"        {r.hole}")
        print()

print("=" * 100)
print("a1 §D — WEAKEST KIND IN THE SET (STATE.md's standing rule, :107)")
print("=" * 100)
present = [s for s in L.ORDER if any(r.status == s for r in L.ROWS)]
print(f"  statuses present, strongest first: {' ≻ '.join(present)}")
print(f"  WEAKEST KIND IN THIS ENUMERATION: {present[-1]}")
print("  Any prose aggregating these rows must state that kind. A sentence saying the")
print("  downstream of L1b is 'proved' over this set is FALSE however true each row is")
print("  individually.")
