#!/usr/bin/env python3
"""verdictwatch -- THE DELIVERABLE of mg-bf3f.

Reports every work item that reached `done` (or `archived`) whose filer never
received a verdict mail from the worker, ORDERED BY WHEN IT LANDED, so a backlog
can be recovered and not merely alarmed about.

    ./verdictwatch.py --filer pm-onethird
    ./verdictwatch.py --filer pm-onethird --since 2026-08-05 --json
    ./verdictwatch.py                       # every filer

EXIT CODES
  0   no dropped verdicts in the scanned population
  1   at least one dropped verdict          <-- the expected code today
  2   usage error

Exit 1 is not a failure of this program. A detector for this defect that exited
0 on 2026-08-06 would be reporting that eleven-plus verdicts had arrived.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_bf3f as L  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--filer", help="only items filed by this agent")
    ap.add_argument("--since", help="only items that landed on/after this RFC3339 prefix")
    ap.add_argument("--root", help="macguffin root (default $MG_ROOT or ~/.macguffin)")
    ap.add_argument("--json", action="store_true", help="NDJSON, one dropped row per line")
    ap.add_argument("--all", action="store_true", help="print delivered and undecidable rows too")
    ap.add_argument("--quiet", action="store_true", help="counts only")
    a = ap.parse_args(argv)

    res = L.scan(mg=a.root, filer=a.filer, since=a.since)
    rows = res["rows"]
    dropped = [r for r in rows if r["status"] == "DROPPED"]
    undec = [r for r in rows if r["status"] == "UNDECIDABLE"]
    deliv = [r for r in rows if r["status"] == "DELIVERED"]

    if a.json:
        for r in (rows if a.all else dropped):
            print(json.dumps(r, sort_keys=True))
        return 1 if dropped else 0

    scope = a.filer or "ALL FILERS"
    print(f"verdictwatch -- store {res['mg']} -- filer {scope}"
          + (f" -- since {a.since}" if a.since else ""))
    print(f"  landed items scanned : {len(rows)}")
    print(f"  DELIVERED            : {len(deliv)}")
    print(f"  DROPPED              : {len(dropped)}")
    print(f"  UNDECIDABLE          : {len(undec)}   (no polecat-* branch in the result sidecar)")
    for agent, exists in sorted(res["boxes"].items()):
        if not exists:
            print(f"  !! filer {agent} has NO MAILBOX -- every one of its items is dropped by construction")

    if not a.quiet and dropped:
        print()
        print("DROPPED VERDICTS, oldest landing first "
              "(elsewhere = mails this worker sent to somebody who was not the filer):")
        print(f"  {'landed':21} {'item':9} {'filer':13} {'worker':8} {'kind':9} {'elsewhere':>9}  title")
        for r in dropped:
            print(f"  {r['landed'] or '?':21} {r['id']:9} {r['filer']:13} "
                  f"{(r['worker'] or '?'):8} {r['kind']:9} {r['mails_elsewhere']:>9}  {r['title'][:88]}")

    if not a.quiet and a.all:
        if deliv:
            print()
            print("DELIVERED (lead = minutes the verdict mail PRECEDED the landing; negative = arrived after):")
            for r in deliv:
                lead = L.verdict_lead_minutes(r)
                print(f"  {r['landed'] or '?':21} {r['id']:9} lead={str(lead):>8}  "
                      f"{r['verdict_mail']['subject'][:76]}")
        if undec:
            print()
            print("UNDECIDABLE -- worker not resolvable from mg's own store:")
            for r in undec:
                print(f"  {r['landed'] or '?':21} {r['id']:9} {r['filer']:13} {r['title'][:70]}")

    return 1 if dropped else 0


if __name__ == "__main__":
    sys.exit(main())
