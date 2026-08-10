#!/usr/bin/env python3
"""s2 — THE COLLISIONS, one line each, under both readings.

A collision is a (landing, parent, audit) triple where the landing's interval and the
audit-of-its-parent's interval overlap. The ticket's near-miss is one row of this table.

The two readings are printed TOGETHER on every row rather than in two tables, because the
interesting rows are the ones where they DISAGREE: a triple that is CONCURRENT on wall and
AUDIT-BEFORE on write is a merge-queue overlap, not a reading overlap, and calling it the
same finding is E3 committed.
"""
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib64cb as L

B = L.build()
L.banner("s2 — COLLISIONS", __doc__.strip())

tr = B["triples"]
idx = B["idx"]
one = B["one"]


def short(iv):
    if iv is L.REFUSED:
        return "     REFUSED     "
    return f"{iv[0][5:16]}..{iv[1][11:16]}"


def emit(rows, title):
    print(title)
    print(f"  {'landing':9s} {'parent':9s} {'audit':9s} {'tier':9s} {'wall':12s} {'write':12s}")
    for t in rows:
        tier = "STATE.md" if t["state"] else "docs-only"
        print(f"  {t['landing']:9s} {t['parent']:9s} {t['audit']:9s} {tier:9s} "
              f"{t['wall']:12s} {t['write']:12s}")
    print(f"  count rows in them {len(rows)}")
    print()


conc_wall = [t for t in tr if t["wall"] == "CONCURRENT"]
conc_write = [t for t in tr if t["write"] == "CONCURRENT"]
conc_either = [t for t in tr if "CONCURRENT" in (t["wall"], t["write"])]
conc_both = [t for t in tr if t["wall"] == t["write"] == "CONCURRENT"]

emit(conc_wall, "A. CONCURRENT under the WALL reading (spawn to merge)")
emit(conc_write, "B. CONCURRENT under the WRITE reading (first to last commit)")
emit(conc_both, "C. CONCURRENT under BOTH — the rows no reading can explain away")
emit([t for t in conc_either if t not in conc_both],
     "D. CONCURRENT under ONE reading only — each of these is a WEAKER finding")

print("E. AUDIT-AFTER — the landing was built on a parent whose audit had NOT RUN YET")
print("   (a different defect from the ticket's: not a race, a FAN-OUT. See s5.)")
aft = [t for t in tr if t["wall"] == "AUDIT-AFTER"]
emit(aft, "")

print("F. DETAIL for every row that is CONCURRENT under either reading")
for t in conc_either:
    lv, av = one[t["landing"]], one.get(t["audit"])
    print(f"  --- {t['landing']}  (parent {t['parent']}, audit {t['audit']}) ---")
    print(f"      landing : {lv['title'][:100]}")
    if av:
        print(f"      audit   : {av['title'][:100]}")
    print(f"      landing wall  {short(t['l_wall'])}   write {short(t['l_write'])}")
    print(f"      audit   wall  {short(t['a_wall'])}   write {short(t['a_write'])}")
    print(f"      verdicts: wall={t['wall']} write={t['write']}  "
          f"STATE.md={'yes' if t['state'] else 'no'}")
    print(f"      landing canonical commits: {idx[t['landing']]['canonical']}")
    print(f"      landing declared depends : {sorted(L.parents_depends_only(lv)) or 'NONE'}")
    print()

json.dump([{k: v for k, v in t.items()} for t in conc_either],
          open(os.path.join(L.SELF_DIR, "collisions.json"), "w"), indent=1, default=str)
print(f"count CONCURRENT under either reading {len(conc_either)}")
print(f"count CONCURRENT under both readings  {len(conc_both)}")
print(f"count AUDIT-AFTER                     {len(aft)}")
