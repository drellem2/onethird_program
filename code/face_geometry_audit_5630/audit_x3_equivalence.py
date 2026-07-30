#!/usr/bin/env python3
"""mg-5630: is the ADOPTED NEGATIVE CONTROL 3 the same control as the audit's X3,
or a weaker re-implementation wearing its name?  (mayor's target 3.)

Cross-call BOTH implementations plus MY OWN third one, poset by poset, on all
three sign modes, and compare the per-poset booleans -- not the counts.
"""
import sys, os
BASE = "/Users/daniel/.pogo/polecats/5630/code"
sys.path.insert(0, os.path.join(BASE, "face_geometry"))
sys.path.insert(0, os.path.join(BASE, "face_geometry_audit_e0ce"))
sys.path.insert(0, "/private/tmp/claude-501/-Users-daniel--pogo-polecats-5630/"
                   "a170c631-0951-463e-a56b-1265495f4050/scratchpad")

from posets import Poset, all_posets                       # deliverable
from controls import claim1_test                           # deliverable NC3 path
from audit_rebuild import (posets_upto_iso, _claim1_with_signs,
                           linear_extensions as ale)       # mg-e0ce X3 path
import verify as mine                                      # my own, disjoint

MODES = ("true", "allplus", "parity")

def canon(n, rel):
    """Canonical form of a strict order relation, for matching across the three
    poset enumerators (which use different representations and orders)."""
    import itertools
    best = None
    for p in itertools.permutations(range(n)):
        img = tuple(sorted((p[a], p[b]) for (a, b) in rel))
        if best is None or img < best:
            best = img
    return best

# ---- build a common index: canonical relation -> the three representations
audit_by_canon = {}
for n in range(2, 6):
    for rel in posets_upto_iso(n):
        audit_by_canon[(n, canon(n, rel))] = rel

deliv_by_canon = {}
for n in range(2, 6):
    for P in all_posets(n):
        rel = frozenset((a, b) for a in range(n) for b in range(n)
                        if a != b and P.leq(a, b))
        deliv_by_canon[(n, canon(n, rel))] = P

mine_by_canon = {}
for n in range(2, 6):
    for rel in mine.iso_classes(n):
        mine_by_canon[(n, canon(n, rel))] = rel

keys = sorted(set(audit_by_canon) & set(deliv_by_canon) & set(mine_by_canon))
print("posets matched across all three enumerators: %d (2<=n<=5; expect 86)" % len(keys))
print("  audit enum: %d   deliverable enum: %d   mine: %d"
      % (len(audit_by_canon), len(deliv_by_canon), len(mine_by_canon)))

disagree = {m: [] for m in MODES}
le_order_same = 0
for k in keys:
    n = k[0]
    arel, P, mrel = audit_by_canon[k], deliv_by_canon[k], mine_by_canon[k]
    # do the two codebases enumerate L(P) in the same order?  (this is what the
    # (-1)^{facet index} in BOTH parity rules is indexed by)
    from face_complex import linear_extensions as dle
    if list(dle(P)) == list(ale(arel, n)):
        le_order_same += 1
    for m in MODES:
        a = _claim1_with_signs(arel, n, m)                    # mg-e0ce X3
        d = claim1_test(P, sign_mode=m)                       # adopted NC3
        v = mine.claim1(n, mrel, m)[0]                        # mine
        if not (a == d == v):
            disagree[m].append((n, sorted(arel), a, d, v))

print()
print("L(P) enumeration order identical between the two codebases: %d/%d"
      % (le_order_same, len(keys)))
print()
for m in MODES:
    bad = disagree[m]
    print("mode %-8s : per-poset agreement audit-X3 == adopted-NC3 == mine on %d/%d %s"
          % (m, len(keys) - len(bad), len(keys),
             "" if not bad else "  DISAGREEMENTS: %s" % bad[:6]))

# ---- and reproduce the audit's OWN 38/38 on the audit's OWN population,
#      with MY implementation, to check the lines 367-369 reconciliation.
print()
rows = []
for n in (3, 4, 5):
    for rel in posets_upto_iso(n)[:20]:
        k = (n, canon(n, rel))
        mrel = mine_by_canon[k]
        rows.append((n, len(ale(rel, n)),
                     mine.claim1(n, mrel, "true")[0],
                     mine.claim1(n, mrel, "allplus")[0],
                     mine.claim1(n, mrel, "parity")[0]))
print("audit X3 population re-derived: %d posets (5+16+20), |L|>=2 on %d"
      % (len(rows), sum(1 for r in rows if r[1] >= 2)))
print("  MY implementation on THAT population: true pass %d ; allplus pass %d ; "
      "parity rejected %d of %d where |L|>=2   [audit reports: 41, 41, 38 of 38]"
      % (sum(1 for r in rows if r[2]), sum(1 for r in rows if r[3]),
         sum(1 for r in rows if r[1] >= 2 and not r[4]),
         sum(1 for r in rows if r[1] >= 2)))
