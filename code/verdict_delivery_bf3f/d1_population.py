#!/usr/bin/env python3
"""D1 -- THE POPULATION. How many verdicts were actually dropped, and to whom.

pm-onethird's ticket says ELEVEN. Eleven is the count of drops pm-onethird
NOTICED. This section measures the population the predicate defines, publishes
the false-positive control that the number depends on, and sizes what the
detector cannot reach.

Exit 0 -- this section reports; it does not assert a threshold.
"""
import os
import re
import sys
import collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_bf3f as L  # noqa: E402

# The 21 items I established BY HAND, outside this repository, before any script
# of this instrument existed (PREDICTIONS.md M3). P2 says none of them may be
# reported as DROPPED. They are pasted here as a literal so that the control is
# an INDEPENDENT list and not something this code derived from itself.
HAND_DELIVERED = """mg-3946 mg-97fb mg-132a mg-330a mg-cd04 mg-a74f mg-e35b mg-9a19
mg-fcb2 mg-9d7b mg-65eb mg-d075 mg-b2af mg-1d03 mg-8af0 mg-aaf4 mg-0ba7 mg-76d0
mg-bf79 mg-5854 mg-03d1""".split()

# The four pm-onethird named in the ticket as landing in ONE EVENING.
TICKET_FOUR = ["mg-ec63", "mg-6e58", "mg-0120", "mg-5f7c"]
# The three it names from earlier.
TICKET_EARLIER = ["mg-d53d", "mg-ba2a", "mg-1abe"]


def main():
    res = L.scan(filer="pm-onethird")
    rows = res["rows"]
    by = collections.defaultdict(list)
    for r in rows:
        by[r["status"]].append(r)

    print("=" * 78)
    print("D1.1  pm-onethird's population under the declared predicate")
    print("=" * 78)
    print(f"  landed items          : {len(rows)}")
    print(f"  DELIVERED             : {len(by['DELIVERED'])}")
    print(f"  DROPPED               : {len(by['DROPPED'])}")
    print(f"  UNDECIDABLE           : {len(by['UNDECIDABLE'])}")
    print()
    print("  THE TICKET SAYS ELEVEN. The predicate says "
          f"{len(by['DROPPED'])}. Eleven is what was NOTICED.")

    print()
    print("=" * 78)
    print("D1.2  FALSE-POSITIVE CONTROL (P2) -- 21 items hand-verified as delivered")
    print("=" * 78)
    dropped_ids = {r["id"] for r in by["DROPPED"]}
    bad = [i for i in HAND_DELIVERED if i in dropped_ids]
    seen = {r["id"] for r in rows}
    absent = [i for i in HAND_DELIVERED if i not in seen]
    print(f"  hand-verified delivered : {len(HAND_DELIVERED)}")
    print(f"  of those reported DROPPED: {len(bad)}   {bad}")
    print(f"  of those not in scope    : {len(absent)}  {absent}")
    print(f"  -> P2 {'HOLDS' if not bad else 'REFUTED'}")

    print()
    print("=" * 78)
    print("D1.3  THE SEVEN THE TICKET NAMES -- are they all in the report?")
    print("=" * 78)
    for label, ids in (("four in one evening", TICKET_FOUR), ("earlier", TICKET_EARLIER)):
        for i in ids:
            r = next((x for x in rows if x["id"] == i), None)
            state = r["status"] if r else "NOT LANDED / NOT FOUND"
            print(f"  {label:20} {i}  -> {state}")

    print()
    print("=" * 78)
    print("D1.4  THE CRUDE DETECTOR IS WRONG IN BOTH DIRECTIONS")
    print("=" * 78)
    print("  Crude rule: 'no message in the filer's mailbox mentions the item id'.")
    msgs, _ = L.load_mailbox(L.root(), "pm-onethird")
    mentioned = set()
    for m in msgs:
        mentioned.update(re.findall(r"mg-[0-9a-f]{4}", m["text"]))
    crude = {r["id"] for r in rows if r["id"] not in mentioned}
    strict = dropped_ids
    print(f"  crude reports  : {len(crude)}")
    print(f"  strict reports : {len(strict)}")
    print(f"  crude MISSES (dropped, but the id is mentioned by somebody else): {len(strict - crude)}")
    print(f"  crude INVENTS  (id unmentioned, but the worker did mail the filer): {len(crude - strict)}")
    ex = sorted(strict - crude)[:6]
    print(f"  examples of the miss: {ex}")
    print("  The mention is usually mayor's dispatch note or a LATER ticket citing the id.")
    print("  A mention is not a verdict. This is why the predicate keys on the WORKER.")

    print()
    print("=" * 78)
    print("D1.5  WHAT THIS DETECTOR CANNOT REACH, SIZED")
    print("=" * 78)
    print(f"  UNDECIDABLE (no polecat-* branch in the sidecar): {len(by['UNDECIDABLE'])}")
    for r in by["UNDECIDABLE"]:
        print(f"     {r['landed']}  {r['id']}  {r['title'][:64]}")
    nobox = [a for a, e in res["boxes"].items() if not e]
    print(f"  filers with no mailbox at all: {len(nobox)} {nobox}")
    print("  A verdict delivered by commit subject, docs/ file or out-of-band relay is")
    print("  invisible here and is counted DROPPED. That polarity is deliberate: the")
    print("  ticket's complaint is precisely that a commit subject is not delivery.")

    print()
    print("=" * 78)
    print("D1.6  EVERY FILER, not only pm-onethird (P3)")
    print("=" * 78)
    allres = L.scan()
    tally = collections.defaultdict(lambda: collections.Counter())
    for r in allres["rows"]:
        tally[r["filer"]][r["status"]] += 1
    print(f"  {'filer':16} {'landed':>7} {'delivered':>10} {'dropped':>8} {'undec':>7}")
    for f, c in sorted(tally.items(), key=lambda kv: -sum(kv[1].values())):
        tot = sum(c.values())
        if tot < 2:
            continue
        print(f"  {f:16} {tot:>7} {c['DELIVERED']:>10} {c['DROPPED']:>8} {c['UNDECIDABLE']:>7}")
    others = [f for f, c in tally.items() if f != "pm-onethird" and c["DROPPED"] > 0]
    print(f"  -> filers other than pm-onethird with at least one dropped verdict: {len(others)}")
    print(f"  -> P3 {'HOLDS' if others else 'REFUTED'}")

    print()
    print("  DEFECT-3 OF THIS INSTRUMENT, CORRECTED IN PLACE RATHER THAN PUBLISHED:")
    print("  `mg new --help` says the creator field is per-agent only since mg-ddf4;")
    print("  items filed before that record the UNIX USER, which was `daniel` for every")
    print("  agent on this box. So the `daniel` row above is not Daniel's dropped")
    print("  verdicts -- it is mostly CREATOR UNKNOWN, and reporting it as Daniel's")
    print("  would be this arc's own defect: a number that is true of a population")
    print("  nobody meant.")
    items = L.load_items(L.root())
    CUT = "2026-07-30T05:00:00Z"
    pre = post = 0
    for r in allres["rows"]:
        if r["filer"] != "daniel":
            continue
        cr = (items.get(r["id"]) or {}).get("created") or ""
        if cr < CUT:
            pre += 1
        else:
            post += 1
    print(f"  items whose creator reads `daniel`, filed BEFORE {CUT} (identity unknown): {pre}")
    print(f"  ... filed after it (genuinely Daniel)                                    : {post}")
    dn = tally.get("daniel", collections.Counter())["DROPPED"]
    print(f"  -> raw daniel dropped count: {dn}. P3 predicted >= 20: "
          f"{'HOLDS' if dn >= 20 else 'REFUTED'} -- but it HOLDS ON A POPULATION I")
    print("     cannot attribute, so the honest reading of P3 is that it holds on mayor")
    print(f"     ({tally.get('mayor', collections.Counter())['DROPPED']} dropped) and pm-pogo "
          f"({tally.get('pm-pogo', collections.Counter())['DROPPED']}), which ARE attributable.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
