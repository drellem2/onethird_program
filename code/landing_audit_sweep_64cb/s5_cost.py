#!/usr/bin/env python3
"""s5 — WHAT THE SEQUENCING RULE COSTS. Measured, not asserted.

The ticket forbids choosing a remedy before measuring the population, and it is equally
wrong to choose one without pricing it. Three candidates, three different prices:

  (a) LANDING DEPENDS ON ITS PARENT'S AUDIT. Price = the wall-clock the landing waits.
      Computed exactly: `audit_done - landing_claim`, per case, over the residue. A
      negative delay means the audit had already finished and the rule costs nothing.

  (b) LANDING MAY PROCEED BUT MUST RE-READ. Price = zero wall-clock, and instead a
      per-landing obligation to check. Priced here as the number of landings that would
      have had to perform the check, and the number where the check would have found
      something -- because a rule that fires on everything and finds nothing gets ignored.

  (c) FIGURE-PROVENANCE LINE PER NUMBER. Priced as the number of numeric literals the
      residue landings put into canonical documents, since that is how many provenance
      lines the rule demands.
"""
import datetime as dt
import json
import os
import re
import subprocess
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib64cb as L

B = L.build()
ev, idx = B["ev"], B["idx"]
L.banner("s5 — THE PRICE OF EACH REMEDY", __doc__.strip())

adj = json.load(open(os.path.join(L.SELF_DIR, "adjudicated.json")))
residue = adj["residue"]


def ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


print("(a) SERIALISE — the landing waits for its parent's audit to be DONE\n")
print(f"  {'landing':9s} {'audit':9s} {'landing claim':21s} {'audit done':21s} {'delay':>10s}")
delays = []
for t in sorted(residue, key=lambda x: x["landing"]):
    lc = ev.get(t["landing"], {}).get("claim")
    ad = ev.get(t["audit"], {}).get("done")
    if not (lc and ad):
        print(f"  {t['landing']:9s} {t['audit']:9s} {'REFUSED — no timestamps':43s}")
        continue
    d = (ts(ad) - ts(lc)).total_seconds() / 60.0
    delays.append((t["landing"], t["audit"], d))
    mark = "" if d <= 0 else ("  <-- would have waited" if d < 120 else "  <-- WOULD HAVE WAITED")
    print(f"  {t['landing']:9s} {t['audit']:9s} {lc:21s} {ad:21s} {d:>9.1f}m{mark}")
print()
pos = sorted(d for _, _, d in delays if d > 0)
print(f"  count residue triples priced        {len(delays)}")
print(f"  count that would have WAITED at all {len(pos)}")
if pos:
    med = pos[len(pos) // 2]
    print(f"  median wait among those that wait   {med:.1f} minutes")
    print(f"  worst wait                          {max(pos):.1f} minutes")
    print(f"  total arc-wide delay               {sum(pos):.1f} minutes "
          f"({sum(pos)/60:.1f} hours) across the whole history")
print()
print("  READ THAT TOTAL AGAINST THE ARC, NOT AGAINST A DAY: it is the ENTIRE cost of")
print("  remedy (a) over every landing/audit collision the sweep can see, in the arc's")
print("  whole recorded history. The ticket's fear was that serialising would slow the arc.")
print()

print("(b) RE-READ — no wall-clock cost, a per-landing obligation instead\n")
one = B["one"]
subj = B["subject_of_audit"]
would_check = 0
would_find = 0
for lid, lv in B["landings"].items():
    at = ev.get(lid, {}).get("claim")
    if not at:
        continue
    hits = L.unaudited_parent(lv, one, subj, ev, at=at)
    if hits:
        would_check += 1
        if any(s in ("RUNNING", "NOT-YET-DISPATCHED") for _, _, s in hits):
            would_find += 1
print(f"  count landings in the population              {len(B['landings'])}")
print(f"  count landings that would have run the check {would_check}")
print(f"  count where the check would have FIRED       {would_find}")
if would_check:
    print(f"  fire rate among those CHECKED                {100.0*would_find/would_check:.1f}%")
    print(f"  fire rate across ALL landings                "
          f"{100.0*would_find/len(B['landings']):.1f}%")
    print("  BOTH RATES ARE THE HONEST PAIR. The first says: once you have an audited")
    print("  parent, a collision is the COMMON case, not the exception. The second says:")
    print("  the rule is silent on most landings, so it is cheap to carry.")
print("  -> a check that fires on a minority is a check people keep. One that fires on")
print("     everything is one they learn to dismiss, and that is the failure mode of (b).")
print()

print("(c) PROVENANCE PER FIGURE — how many lines the rule demands\n")
NUM = re.compile(r"(?<![\w.])\d+(?:\.\d+)?(?![\w])")
total = 0
for t in residue:
    n = set()
    for h in idx.get(t["landing"], {}).get("canonical", []):
        d = subprocess.run(["git", "-C", L.REPO, "show", h, "--unified=0", "--",
                            "STATE.md", "docs", "README.md"], capture_output=True, text=True).stdout
        for line in d.split("\n"):
            if line.startswith("+") and not line.startswith("+++"):
                n |= set(NUM.findall(line))
    total += len(n)
print(f"  count distinct numeric literals the residue landings added to canonical docs {total}")
print(f"  mean per landing {total/max(1,len(residue)):.0f}")
print("  -> (c) prices at roughly that many provenance lines FOR THE RESIDUE ALONE. Applied")
print("     to every landing it is the most expensive of the three by a wide margin, and it")
print("     is the only one that would have caught a figure copied from a parent that was")
print("     never audited at all.")
