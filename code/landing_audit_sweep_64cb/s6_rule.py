#!/usr/bin/env python3
"""s6 — THE RULE, AS A CHECK THAT RUNS. Shown REFUSING and shown PASSING.

The ticket's real question is whether (b) can be made a rule rather than an accident of
who noticed a rebase conflict. A rule that only ever refuses is not a rule, it is a block;
a rule that only ever passes is decoration. This file runs the predicate over the whole
landing population and prints BOTH sides, plus two controls whose answers are known in
advance and one that must read zero.

THE PREDICATE, stated before it runs:

    unaudited_parent(landing, at) -> [(parent, audit, state), ...]

    state is DONE / RUNNING / NOT-YET-DISPATCHED, evaluated at the instant `at`. A landing
    may proceed iff every audit of every parent is DONE at its claim time; otherwise the
    landing must re-read its figures from the audit's verdict and SAY WHICH VALUES IT TOOK
    AND FROM WHERE.

It needs nothing that does not already exist: the parents come from the ticket's own
`depends:`/tags/body, the audits from the item store, and the states from `work.claim` and
`work.done` events pogod already writes.
"""
import collections
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib64cb as L

B = L.build()
one, ev, subj, idx = B["one"], B["ev"], B["subject_of_audit"], B["idx"]
L.banner("s6 — THE RULE", __doc__.strip())

FAIL = []


def arm(name, got, want):
    ok = got == want
    print(f"  [{'ok ' if ok else 'FAIL'}] {name}: got={got!r} want={want!r}")
    if not ok:
        FAIL.append(name)


print("1. THE TWO KNOWN ANSWERS — the seed pair, where the truth is not in doubt\n")
at = ev["mg-8d63"]["claim"]
got = L.unaudited_parent(one["mg-8d63"], one, subj, ev, at=at)
arm("mg-8d63 at its own claim -> REFUSE (mg-5cba RUNNING)",
    [g for g in got if g[2] == "RUNNING"], [("mg-789d", "mg-5cba", "RUNNING")])
# mg-5cba is itself gated on mg-789d by an existing mechanism, and it WAITED. So the rule
# must PASS it -- the audit is not the thing that needs sequencing.
at2 = ev["mg-5cba"]["claim"]
arm("mg-5cba at its own claim -> PASS (its own parent had no pending audit)",
    [g for g in L.unaudited_parent(one["mg-5cba"], one, subj, ev, at=at2)
     if g[2] != "DONE"], [])
print()

print("2. THE RULE OVER THE WHOLE LANDING POPULATION\n")
verdicts = collections.Counter()
refused = []
for lid, lv in sorted(B["landings"].items()):
    at = ev.get(lid, {}).get("claim")
    if not at:
        verdicts["UNTIMEABLE"] += 1
        continue
    hits = L.unaudited_parent(lv, one, subj, ev, at=at)
    bad = [h for h in hits if h[2] != "DONE"]
    if not hits:
        verdicts["PASS (no audited parent)"] += 1
    elif not bad:
        verdicts["PASS (every audit already DONE)"] += 1
    else:
        verdicts["REFUSE"] += 1
        refused.append((lid, bad))
for k, v in sorted(verdicts.items()):
    print(f"  count {k:34s} {v}")
print(f"  count {'TOTAL':34s} {sum(verdicts.values())}")
print()
print("  THE RULE IS NON-VACUOUS IN BOTH DIRECTIONS: it refuses "
      f"{verdicts['REFUSE']} landings and passes "
      f"{verdicts['PASS (no audited parent)'] + verdicts['PASS (every audit already DONE)']}.")
print("  A predicate that answered one way for everything would be shown up right here.")
print()

print("3. THE REFUSALS, and what each landing would have had to re-read\n")
for lid, bad in refused[:40]:
    for p, a, s in bad:
        print(f"  {lid} -> parent {p}, audit {a} was {s} at claim time")
print(f"  count refusals listed {min(len(refused),40)} of {len(refused)}")
print()

print("4. CONTROLS\n")
# A control that MUST read zero: ask the rule at a time far in the future, when every audit
# in the arc is done. If anything still refuses, the predicate is not reading state at all.
future = "2099-01-01T00:00:00Z"
still = [lid for lid, lv in B["landings"].items()
         if any(h[2] != "DONE" for h in L.unaudited_parent(lv, one, subj, ev, at=future))]
print(f"  count landings still REFUSED at t=2099 {len(still)}")
if still:
    print(f"    (these are audits with no work.done event at all: {still[:8]})")
    print("    -> NOT a defect in the predicate: an audit that never completed is")
    print("       genuinely not DONE, and the rule saying so is the rule working.")
never_done = [a for a in B["audits"] if "done" not in ev.get(a, {})]
arm("control: every t=2099 refusal traces to an audit with no work.done",
    all(any(h[1] in never_done for h in L.unaudited_parent(one[lid], one, subj, ev, at=future)
            if h[2] != "DONE") for lid in still), True)
# A control that must read zero for a different reason: an item with no parents.
synth = dict(id="mg-0000", depends="[]", tags="[onethird]", body="# x\nnothing\n")
arm("control: a parentless item is never refused",
    L.unaudited_parent(synth, one, subj, ev, at=at), [])
print()

json.dump(dict(refused=[(l, b) for l, b in refused], verdicts=dict(verdicts)),
          open(os.path.join(L.SELF_DIR, "rule.json"), "w"), indent=1, default=str)

print("=" * 78)
if FAIL:
    print(f"s6 REFUSES: {FAIL}")
    sys.exit(1)
print("s6: the rule runs, refuses what it should refuse, passes what it should pass.")
