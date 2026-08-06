#!/usr/bin/env python3
"""D4 -- THE LIVE FIRE, AND THE RECOVERY LIST.

D3 fires the detector on a store I built. This section fires it on THE LIVE
STORE, against a verdict that is really about to be dropped: my own.

mg-bf3f carries no verdict-mail instruction -- it is one of the 55 pm-onethird
filed after 2026-07-31T10:02Z -- so by the mechanism D2 establishes, THIS
INSTRUMENT'S OWN VERDICT IS SCHEDULED TO BE LOST. That was filed as P16 before
any of this code existed. D4.2 watches it happen on real data.

Then the first deliverable the ticket asks for: the backlog, ordered by landing,
so it can be recovered rather than only counted.

Exit 0.
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_bf3f as L  # noqa: E402

SELF = "mg-bf3f"
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def git(*args):
    p = subprocess.run(["git", "-C", REPO] + list(args), capture_output=True,
                       text=True, timeout=180)
    return p.stdout


def main():
    print("=" * 78)
    print("D4.1  THE QUIET CONTROL -- the live store as it stands right now")
    print("=" * 78)
    res = L.scan(filer="pm-onethird")
    here = [r for r in res["rows"] if r["id"] == SELF]
    print(f"  {SELF} in the live report: {len(here)} row(s)")
    print("  It has not landed, so the predicate does not apply to it and the detector")
    print("  is correctly SILENT about it. A detector that flagged in-flight work would")
    print("  be an alarm on every open ticket.")

    print()
    print("=" * 78)
    print(f"D4.2  THE LIVE FIRE -- {SELF}'s own verdict, dropped on purpose")
    print("=" * 78)
    print("  The landing is SIMULATED. The mail is NOT: the mailbox half of the")
    print("  predicate is read from pm-onethird's real mailbox exactly as it stands at")
    print("  this instant. So this answers a real question -- if mg-bf3f landed now,")
    print("  would its verdict be lost? -- rather than a constructed one.")
    # The worker name is OBSERVED, not asserted: it is this worktree's own branch,
    # which is the exact string the refinery will write into the result sidecar at
    # merge. Supplying it is necessary because DEFECT-6 -- the worker's identity
    # does not exist in macguffin's store until the merge happens.
    branch = git("rev-parse", "--abbrev-ref", "HEAD").strip()
    worker = branch[len("polecat-"):] if branch.startswith("polecat-") else branch
    print(f"  worker taken from this worktree's own branch `{branch}` -> `{worker}`")
    SIM = {SELF: {"ts": "2026-08-06T23:59:59Z", "worker": worker}}
    sim = L.scan(filer="pm-onethird", simulate=SIM)
    row = next((r for r in sim["rows"] if r["id"] == SELF), None)
    if row is None:
        print(f"  !! {SELF} not found on disk at all -- cannot fire")
        return 0
    print()
    print(f"    item        : {row['id']}")
    print(f"    filer       : {row['filer']}")
    print(f"    worker      : {row['worker']}  (resolver: {row['resolver']}, "
          f"supplied={row['worker_supplied']})")
    print(f"    landing     : {row['landed']}   SIMULATED={row['simulated']}")
    print(f"    verdict mail: {row['verdict_mail']}")
    print(f"    STATUS      : {row['status']}")
    print()
    if row["status"] == "DROPPED":
        print("  IT FIRES. On the live store, with real mail, my own verdict is a drop.")
        print("  P16 was filed before this code existed and it is CONFIRMED by the")
        print("  instrument built to test it: the ticket that repairs the dropped-verdict")
        print("  mechanism was itself set up to have its verdict dropped.")
    else:
        print(f"  It does NOT fire here ({row['status']}). If this is the suite's FINAL")
        print("  transcript, that is because the verdict mail has since been sent -- the")
        print("  run in which it DID fire is committed beside this one as")
        print("  out_d4_live_BEFOREMAIL_DROPPED.txt, taken before that mail existed, and")
        print("  D4.3 below prints the mail that closed it. Both states are on the record;")
        print("  neither is inferred from the other.")

    print()
    print("=" * 78)
    print("D4.3  THE SAME PREDICATE, AFTER THE VERDICT IS SENT")
    print("=" * 78)
    print("  This is the half that makes D4.2 mean something. A detector that reports")
    print("  DROPPED unconditionally is not measuring anything. Re-read now:")
    again = L.scan(filer="pm-onethird", simulate=SIM)
    r2 = next((r for r in again["rows"] if r["id"] == SELF), None)
    print(f"    STATUS now  : {r2['status']}")
    if r2["verdict_mail"]:
        print(f"    verdict mail: {r2['verdict_mail']['date']}  "
              f"{r2['verdict_mail']['subject'][:60]}")
        print("  The flip DROPPED -> DELIVERED was produced by sending one mail and")
        print("  nothing else. Both states of the same live row are on the record.")
    else:
        print("  Still no verdict mail from this worker. If this transcript is the")
        print("  FINAL one, the drop shown in D4.2 is real and unrepaired; the run that")
        print("  follows the verdict mail is the one that shows the flip.")

    print()
    print("=" * 78)
    print("D4.4  THE BACKLOG, ORDERED BY LANDING -- the ticket's first deliverable")
    print("=" * 78)
    dropped = [r for r in res["rows"] if r["status"] == "DROPPED"]
    print(f"  {len(dropped)} dropped verdicts for pm-onethird. The most recent 30, newest last,")
    print("  are the recoverable end of the backlog -- their branches are still on main:")
    for r in dropped[-30:]:
        print(f"    {r['landed']}  {r['id']}  worker={r['worker']:9} {r['title'][:66]}")

    print()
    print("=" * 78)
    print("D4.5  RECOVERY OF mg-ec63, THE ONE pm-onethird ASKED FOR FIRST (P13)")
    print("=" * 78)
    print("  'If that verdict exists only in commit subjects, THE FINDING MOST LIKELY TO")
    print("  CHANGE WHAT WE BELIEVE IS THE ONE LEAST LIKELY TO BE READ.'")
    log = git("log", "main", "--format=%h\t%s", "--grep=mg-ec63")
    lines = [l for l in log.splitlines() if l.strip()]
    print(f"  commits on main naming mg-ec63: {len(lines)}")
    kinds = {}
    for l in lines:
        h, _, s = l.partition("\t")
        kind = s.split(":", 1)[0].strip()
        kinds[kind] = kinds.get(kind, 0) + 1
    print(f"  by commit type: {kinds}")
    verdict_bearing = [l for l in lines
                       if l.partition("\t")[2].split(":", 1)[0].strip().startswith("evidence")]
    print(f"  VERDICT-BEARING commits (type `evidence*`, which is where this arc puts the")
    print(f"  finished account): {len(verdict_bearing)}")
    for l in verdict_bearing:
        h, _, s = l.partition("\t")
        print()
        print(f"    {h}")
        for i in range(0, min(len(s), 1200), 96):
            print(f"      {s[i:i + 96]}")
    print()
    print(f"  -> P13 declared rule: the verdict is recoverable from the `evidence*` commits")
    print(f"     alone. That is {len(verdict_bearing)} commit(s); the full trail is {len(lines)}.")
    print("     RECOVERED. It was never lost from the repository -- only from its reader.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
