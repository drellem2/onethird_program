#!/usr/bin/env python3
"""s0 — forced arms. Every classifier in lib64cb, including THREE it must REJECT.

A selftest that only feeds a classifier things it should accept measures nothing: a
function returning True unconditionally would pass it and would score this ticket's
population at every triple in the arc. The rejection arms are the load-bearing half.

Exit 0 iff every arm holds.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib64cb as L

FAIL = []


def arm(name, got, want):
    ok = got == want
    print(f"  [{'ok ' if ok else 'FAIL'}] {name}\n         got={got!r}\n        want={want!r}")
    if not ok:
        FAIL.append(name)


L.banner("s0 — SELFTEST", __doc__.strip())

items = L.load_items()
ev = L.load_events()
idx = L.commit_index(L.load_commits())

print("A. is_audit — THREE ACCEPTS AND THREE REJECTS")
# ACCEPT: strict audits.
for i in ("mg-5cba", "mg-2eed", "mg-3bb9"):
    arm(f"A.accept {i} ({items[i]['title'][:52]}...)", L.is_audit(items[i]), True)
# REJECT: tagged `audit` but LANDINGS of an audit's consequences. A classifier keyed on
# the bare `audit` tag calls each of these its own auditor.
for i in ("mg-1319", "mg-a806"):
    arm(f"A.reject {i} tags={items[i]['tags']}", L.is_audit(items[i]), False)
# REJECT: the parent under audit is not an audit.
arm("A.reject mg-789d (the audited PARENT)", L.is_audit(items["mg-789d"]), False)
print()

print("B. parents — the seed pair, and a control that must be EMPTY")
arm("B.landing mg-8d63 -> {mg-789d}", L.parents(items["mg-8d63"]), {"mg-789d"})
arm("B.audit   mg-5cba -> {mg-789d}", L.parents(items["mg-5cba"]), {"mg-789d"})
# An emptiness control: an item whose depends is empty, whose tags carry no -followup,
# and whose prose window names nobody. The interval that must stay empty.
synth = dict(id="mg-0000", depends="[]", tags="[onethird]", body="# x\nno parent here at all\n")
arm("B.control synthetic item -> EMPTY", L.parents(synth), set())
print()

print("C. is_canonical — the wide reading must still REJECT code/")
arm("C.STATE.md", L.is_canonical("STATE.md"), True)
arm("C.docs/x.md", L.is_canonical("docs/OneThird-LStar-mg-789d.md"), True)
arm("C.README.md", L.is_canonical("README.md"), True)
arm("C.reject code/", L.is_canonical("code/audit_5cba/a1_witness.py"), False)
arm("C.reject a bare out_*.txt at root", L.is_canonical("out_s4_theorem_and_quantifier.txt"), False)
print()

print("D. overlaps / relation — all four verdicts, and REFUSED must PROPAGATE")
A = ("2026-08-10T04:00:00Z", "2026-08-10T06:00:00Z")
B = ("2026-08-10T05:00:00Z", "2026-08-10T07:00:00Z")
C = ("2026-08-10T06:00:00Z", "2026-08-10T08:00:00Z")
Z = ("2026-08-10T01:00:00Z", "2026-08-10T02:00:00Z")
arm("D.overlap", L.overlaps(A, B), True)
arm("D.touching-endpoints do NOT overlap", L.overlaps(A, C), False)
arm("D.CONCURRENT", L.relation(A, B), "CONCURRENT")
arm("D.AUDIT-AFTER", L.relation(A, C), "AUDIT-AFTER")
arm("D.AUDIT-BEFORE", L.relation(A, Z), "AUDIT-BEFORE")
# The one that matters: a missing timestamp must NOT become "no collision".
arm("D.REFUSED propagates through overlaps", L.overlaps(L.REFUSED, B), L.REFUSED)
arm("D.REFUSED propagates through relation", L.relation(L.REFUSED, B), L.REFUSED)
arm("D.REFUSED on the AUDIT side too", L.relation(A, L.REFUSED), L.REFUSED)
print()

print("E. wall_interval — the ZERO-LENGTH refusal, on a live instance")
arm("E.mg-845e claim==done -> REFUSED (not 'no overlap')",
    L.wall_interval(ev, "mg-845e"), L.REFUSED)
arm("E.mg-8d63 is a real interval",
    isinstance(L.wall_interval(ev, "mg-8d63"), tuple), True)
arm("E.an item with no events -> REFUSED", L.wall_interval(ev, "mg-zzzz"), L.REFUSED)
print()

print("F. the RULE, asked at a HISTORICAL instant")
one = {k: v for k, v in items.items() if L.is_onethird(v)}
subj = {}
import collections
subj = collections.defaultdict(set)
for a in one.values():
    if L.is_audit(a):
        for p in L.parents(a):
            subj[p].add(a["id"])
# At mg-8d63's own claim time, mg-5cba was RUNNING. That is the whole ticket in one call.
at = ev["mg-8d63"]["claim"]
got = L.unaudited_parent(items["mg-8d63"], one, subj, ev, at=at)
arm(f"F.mg-8d63 at its claim {at}: mg-5cba RUNNING",
    [g for g in got if g[1] == "mg-5cba"], [("mg-789d", "mg-5cba", "RUNNING")])
# And AFTER mg-5cba finished, the same call says DONE -- the rule must be able to PASS,
# not only to refuse, or it is a function that blocks everything.
after = "2026-08-10T23:59:59Z"
got2 = L.unaudited_parent(items["mg-8d63"], one, subj, ev, at=after)
arm("F.same landing after the audit finished: DONE (the rule can PASS)",
    [g for g in got2 if g[1] == "mg-5cba"], [("mg-789d", "mg-5cba", "DONE")])
# A control that must read EMPTY: an item with no parent has no audit to wait on.
arm("F.control synthetic no-parent item -> []",
    L.unaudited_parent(synth, one, subj, ev, at=at), [])
print()

print("=" * 78)
if FAIL:
    print(f"s0 REFUSES: {len(FAIL)} arm(s) failed: {FAIL}")
    sys.exit(1)
print("s0: all arms hold.")
