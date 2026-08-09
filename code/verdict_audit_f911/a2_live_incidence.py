#!/usr/bin/env python3
"""mg-f911 A2 -- how often do A1's two constructed defects actually occur?

A1 proved both are CONSTRUCTIBLE. That is not the same claim as "they happen".
This arc's standing target says a negative needs its candidate space, so each
defect gets its denominator measured on the live store rather than asserted.

  DEFECT-O (over-report): a verdict signed with the `polecat-<name>` branch
    spelling is in the box and is still called DROPPED.
    CANDIDATE SPACE = every message in a filer's mailbox. Count those whose
    `From:` is a `polecat-*` spelling.

  DEFECT-U (under-report): any mail from worker to filer is credited as a
    verdict, whatever it says.
    CANDIDATE SPACE = every DELIVERED row. Classify the crediting message by
    whether it looks like a verdict at all.

Read-only. Touches nothing.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "verdict_delivery_bf3f"))
import lib_bf3f as L  # noqa: E402

MG = L.root(None)
FILER = "pm-onethird"


def main():
    print(f"  store: {MG}")
    print(f"  filer under audit: {FILER}")
    res = L.scan(mg=MG, filer=FILER)
    rows = res["rows"]
    deliv = [r for r in rows if r["status"] == "DELIVERED"]
    drop = [r for r in rows if r["status"] == "DROPPED"]
    undec = [r for r in rows if r["status"] == "UNDECIDABLE"]
    print(f"  landed rows: {len(rows)}   DELIVERED {len(deliv)}  "
          f"DROPPED {len(drop)}  UNDECIDABLE {len(undec)}")

    print()
    print("=" * 78)
    print("A2.1  DEFECT-O, over-report: verdicts signed with the branch spelling")
    print("=" * 78)
    msgs, exists = L.load_mailbox(MG, FILER)
    print(f"  CANDIDATE SPACE = every message in {FILER}'s mailbox: {len(msgs)}")
    polecat_from = [m for m in msgs if m["from"].startswith("polecat-")]
    print(f"  messages whose From: is a `polecat-*` branch spelling : {len(polecat_from)}")
    for m in polecat_from[:10]:
        print(f"    {m['date']:21} from={m['from']:22} {m['subject'][:60]}")
    if not polecat_from:
        print("    -> ZERO. DEFECT-O is CONSTRUCTIBLE BUT HAS NEVER OCCURRED in this")
        print("       mailbox. It is a latent trap, not a live miscount, and the")
        print("       reported DROPPED figure is NOT inflated by it today.")

    # The other half of the same trap: does any DROPPED row have a message in the
    # box from a sender that merely SPELLS its worker differently?
    print()
    print("  Cross-check -- for every DROPPED row, is there ANY message in the box")
    print("  whose From: contains the worker's 4-hex id? (a drop with a near-name")
    print("  sender present is a candidate over-report by some other spelling)")
    suspect = []
    for r in drop:
        m = re.match(r"^mg-([0-9a-f]{4})$", r["id"])
        if not m:
            continue
        hexid = m.group(1)
        for msg in msgs:
            if hexid in msg["from"] and msg["from"] not in (r["worker_names"] or []):
                suspect.append((r["id"], msg["from"], msg["subject"][:50]))
    print(f"  suspect (drop + near-name sender in box): {len(suspect)}")
    for s in suspect[:10]:
        print(f"    {s[0]}  from={s[1]}  {s[2]}")
    if not suspect:
        print("    -> ZERO. No DROPPED row has a message in the box from any sender")
        print("       carrying its id under a spelling the resolver missed.")

    print()
    print("=" * 78)
    print("A2.2  DEFECT-U, under-report: is the crediting message a VERDICT?")
    print("=" * 78)
    print(f"  CANDIDATE SPACE = every DELIVERED row: {len(deliv)}")
    # Deliberately crude and stated as such: a subject is verdict-shaped if it
    # says so. The point is not to classify perfectly, it is to find out whether
    # the detector is crediting messages that make no claim to be verdicts.
    VERDICTY = re.compile(r"verdict|VERDICT|finding|CONFIRMED|REFUTED|audit|AUDIT|"
                          r"result|landed|merged|repair|done", re.I)
    verdicty, other = [], []
    for r in deliv:
        subj = (r["verdict_mail"] or {}).get("subject", "")
        (verdicty if VERDICTY.search(subj) else other).append((r["id"], subj))
    print(f"  crediting message reads as verdict-shaped : {len(verdicty)}")
    print(f"  crediting message does NOT                : {len(other)}")
    for iid, subj in other:
        print(f"    {iid}  {subj[:88]}")
    print()
    print("  NOTE ON THIS CLASSIFIER: it reads SUBJECTS with a keyword regex. It is")
    print("  evidence about how many credits are obviously verdicts, and it is NOT a")
    print("  ruling on the others -- a verdict can carry a subject that says nothing.")
    print("  What it establishes is the DIRECTION of the bound, not a corrected count.")

    # How many DELIVERED rows rest on more than one message? If the worker wrote
    # several times, the row is credited by the FIRST, which need not be a verdict.
    multi = [r for r in deliv if (r["verdict_mail"] or {}).get("n", 1) > 1]
    print()
    print(f"  DELIVERED rows credited where the worker sent >1 message: {len(multi)}")
    print("  (the row is credited by the EARLIEST message, sorted by date -- so a")
    print("   worker that asked a question first and filed its verdict later is")
    print("   credited, and dated, by the QUESTION)")
    for r in multi[:12]:
        vm = r["verdict_mail"]
        print(f"    {r['id']}  n={vm['n']}  credited by {vm['date']}  {vm['subject'][:56]}")

    print()
    print("=" * 78)
    print("A2.3  THE SILENTLY EXCLUDED -- items the predicate never reaches")
    print("=" * 78)
    print("  lib_bf3f.scan() does `if not f: continue` -- an item with no `creator:`")
    print("  in its frontmatter is dropped from the population with no bucket and no")
    print("  count. That is the shape this arc keeps finding, so it gets measured.")
    items = L.load_items(MG)
    land = L.load_landings(MG)
    landed_ids = [i for i in items if i in land]
    nocreator = [i for i in landed_ids if not items[i]["creator"]]
    print(f"  landed items on disk        : {len(landed_ids)}")
    print(f"  of those with NO creator:   : {len(nocreator)}")
    if nocreator:
        for i in nocreator[:20]:
            print(f"    {i}  {items[i]['title'][:70]}")
    else:
        print("    -> ZERO today. The exclusion is real in the code and EMPTY in this")
        print("       store, so it costs nothing now and is a live trap if any tool")
        print("       ever writes an item without a creator line.")

    # And landings with no item file at all -- the reverse hole.
    orphan = [i for i in land if i not in items]
    print()
    print(f"  landing events with NO item file on disk: {len(orphan)}")
    if orphan:
        for i in sorted(orphan)[:20]:
            print(f"    {i}  landed {land[i]['ts']} kind={land[i]['kind']}")
        print("    -> these landed and are INVISIBLE to the detector: it enumerates")
        print("       FILES and joins events onto them, so an item whose file is gone")
        print("       is not dropped, not delivered, and not undecidable. It is absent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
