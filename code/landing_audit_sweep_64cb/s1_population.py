#!/usr/bin/env python3
"""s1 — THE POPULATION. How many landings, how many audits, how many triples.

This is the count the ticket says nobody has asked for. It is reported under BOTH
interval readings (wall = spawn-to-merge, write = first-to-last commit author date)
because they disagree, and reporting only the wider one would overstate the arc's
exposure by exactly the merge-queue time.
"""
import collections
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib64cb as L

B = L.build()
L.banner("s1 — POPULATION", __doc__.strip())

one, idx, ev = B["one"], B["idx"], B["ev"]
print(f"count  onethird work items                     {len(one)}")
print(f"count  of them, STRICT audits                  {len(B['audits'])}")
print(f"count  of them, landing by TITLE               "
      f"{sum(1 for v in one.values() if L.is_landing_by_title(v))}")
print(f"count  of them, landing by GIT (canonical doc) {len(B['landings'])}")
print(f"count  of them, touching STATE.md              "
      f"{sum(1 for k in B['landings'] if idx[k]['state'])}")
print(f"count  distinct audited parents                {len(B['subject_of_audit'])}")
print()

# The two readings of `landing` are NOT the same set, and the overlap is the honest
# statement of how much either one is doing on its own.
by_title = {k for k, v in one.items() if L.is_landing_by_title(v)}
by_git = set(B["landings"])
print("THE TWO READINGS OF `LANDING` DISAGREE, AND BY HOW MUCH:")
print(f"  count  title-only (git never saw a canonical-doc commit) {len(by_title - by_git)}")
print(f"  count  git-only   (never said LAND in its title)         {len(by_git - by_title)}")
print(f"  count  both                                              {len(by_title & by_git)}")
print("  -> the title reading MISSES {} landings the git reading finds. Using it alone"
      .format(len(by_git - by_title)))
print("     would have reported this arc as ~5x safer than it is.")
print()

tr = B["triples"]
print(f"count  landing/parent/audit triples            {len(tr)}")
print()

for reading in ("wall", "write"):
    print(f"--- BUCKETS UNDER THE `{reading.upper()}` READING ---")
    c = collections.Counter()
    for t in tr:
        tier = "STATE.md" if t["state"] else "docs-only"
        c[(t[reading], tier)] += 1
    tiers = ("STATE.md", "docs-only")
    verdicts = ("CONCURRENT", "AUDIT-AFTER", "AUDIT-BEFORE", L.REFUSED)
    print(f"  {'verdict':16s} {'STATE.md':>9s} {'docs-only':>10s} {'total':>7s}")
    for v in verdicts:
        row = [c[(v, t)] for t in tiers]
        print(f"  count {v:16s} {row[0]:>4d} {row[1]:>10d} {sum(row):>7d}")
    print(f"  count {'ALL':16s} {sum(c[(v,'STATE.md')] for v in verdicts):>4d} "
          f"{sum(c[(v,'docs-only')] for v in verdicts):>10d} {len(tr):>7d}")
    print()

print("WHAT THE DENOMINATOR ACTUALLY IS (E8, filed in advance):")
nref_wall = sum(1 for t in tr if t["wall"] is not L.REFUSED)
nref_write = sum(1 for t in tr if t["write"] is not L.REFUSED)
print(f"  count  triples timeable on wall  {nref_wall} of {len(tr)}")
print(f"  count  triples timeable on write {nref_write} of {len(tr)}")
print("  A CONCURRENT count must be read against the TIMEABLE denominator, not against")
print("  the triple count, and never against the 624-item population.")
print()

print("THE GATE ALREADY EXISTS — count of onethird items that DECLARE a dependency:")
dep = [v for v in one.values() if L.parents_depends_only(v)]
print(f"  count  items with a non-empty depends: field  {len(dep)}")
audit_dep = [v for v in dep if L.is_audit(v)]
print(f"  count  of those that are audits              {len(audit_dep)}")
land_dep = [v for v in dep if v["id"] in by_git and not L.is_audit(v)]
print(f"  count  of those that are git-landings        {len(land_dep)}")
print("  -> the asymmetry is the finding: the arc gates AUDITS on their parents and does")
print("     NOT gate LANDINGS on the audits. mg-5cba/mg-8d63 is that asymmetry in one pair.")
