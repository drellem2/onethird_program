#!/usr/bin/env python3
"""s2 — THE RETROSPECTIVE: why did mg-2860 miss the fifth site? (mg-5827)

mg-2860 swept four sites for exactly this class on 2026-08-06 and missed at least a fifth. The
two edits are already landed. This step answers the question underneath them, and it answers it
by MEASUREMENT rather than by reading the commit message and believing it.

The hypothesis: mg-2860 did not search. It executed a FIXED LIST supplied by its own ticket,
scoped to a SINGLE FILE, for a DIFFERENT defect class than the one that bit.

Exit 0 always. This step reports; it does not gate.
"""
from __future__ import annotations

import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib5827 as L                                                  # noqa: E402

SWEEP = "f85a4e8"            # mg-2860's landing commit
BASE = "f85a4e8~1"           # the tree mg-2860 was looking at (f758468)
SITES = ["STATE.md:13", "STATE.md:21", "STATE.md:57", "STATE.md:62", "STATE.md:86"]


def head(t):
    print(L.banner(t))


def main() -> int:
    reg = L.Registry.load()

    head("1. WHAT mg-2860 SAID IT DID — its own commit message, verbatim")
    msg = subprocess.run(["git", "log", "-1", "--format=%B", SWEEP],
                         capture_output=True).stdout.decode("utf-8", "replace")
    for phrase in ["FOUR SITES, FIVE LINES, NOTHING ELSE",
                   "outside what this ticket lists",
                   "are NOT carried"]:
        print("  %-42s : %s" % ("contains %r" % phrase[:34],
                                "YES" if phrase in msg else "NO"))
    for line in msg.splitlines():
        if "FOUR SITES" in line or "outside what this ticket" in line:
            print("      > " + line.strip())

    head("2. WHAT IT ACTUALLY TOUCHED — the diff, not the prose")
    files = subprocess.run(["git", "show", "--name-only", "--format=", SWEEP],
                           capture_output=True).stdout.decode().split()
    stat = subprocess.run(["git", "show", "--shortstat", "--format=", SWEEP],
                          capture_output=True).stdout.decode().strip()
    print("  files touched : %s" % (files or "(none)"))
    print("  shortstat     : %s" % stat)
    print()
    print("  THE SWEEP TOUCHED %d FILE(S). Its five named sites are all in that one file." % len(files))
    print("  A sweep whose entire footprint is one file cannot have searched a corpus.")

    head("3. WHAT A SEARCH WOULD HAVE FOUND AT THE SAME COMMIT")
    print("  Same registry, same rules, pointed at mg-2860's own base tree %s." % BASE)
    occs = L.scan(rev=BASE, reg=reg)
    L.emit("SCAN @ %s (mg-2860's base tree)" % BASE, occs, limit=None)

    d = L.defects(occs)
    in_state = [o for o in d if o.path == "STATE.md"]
    out_state = [o for o in d if o.path != "STATE.md"]
    by_file: dict[str, int] = {}
    for o in d:
        by_file[o.path] = by_file.get(o.path, 0) + 1

    head("4. THE ANSWER")
    print("  Flat-text sites at mg-2860's base commit : %d" % len(d))
    print("    inside  STATE.md (the file it swept)   : %d" % len(in_state))
    print("    OUTSIDE STATE.md (never looked at)     : %d" % len(out_state))
    print()
    for path in sorted(by_file):
        print("    %-58s %d" % (path, by_file[path]))
    print()
    print("  THE LIST IS THE DEFECT.")
    print("  mg-2860's five sites were supplied by its ticket, which named them by line number")
    print("  in one file. It landed all five correctly -- there are %d flat-text sites left" % len(in_state))
    print("  inside STATE.md, so it was RIGHT about its own file. The whole of the miss is the")
    print("  FILE BOUNDARY. It never asked whether the superseded input was quoted anywhere")
    print("  else, because nothing asked it to and nothing could have told it.")
    print()
    print("  It also swept a DIFFERENT CLASS. Its subject was which FORM leads -- the limit")
    print("  `lambda_std -> 1` versus the constant `1 - lambda_std <= eps_spec`. The numeric")
    print("  budget was a rider its ticket added ('WHILE YOU ARE THERE'), which it landed")
    print("  correctly INTO STATE.md while never looking OUT of it. So the sweep that is")
    print("  accused of missing this class was not sweeping for it.")
    print()
    print("  AND IT WILL MISS THE SIXTH. A ticket-supplied list of line numbers has no way to")
    print("  grow. The sixth site will be found the same way the fifth was: by whoever happens")
    print("  to read the right document.")

    head("5. THE SAME QUESTION ASKED OF THE LANDING COMMIT")
    occs_after = L.scan(rev=SWEEP, reg=reg)
    d_after = L.defects(occs_after)
    print("  Flat-text sites immediately AFTER mg-2860 landed : %d" % len(d_after))
    print("  Change across the sweep                          : %+d" % (len(d_after) - len(d)))
    print()
    print("  The sweep moved the count by %d. That is the measurement of what it swept."
          % (len(d_after) - len(d)))

    head("6. WHAT THIS RETROSPECTIVE DOES NOT ESTABLISH")
    print("  * It does not show mg-2860 was WRONG to scope itself to its ticket. It was")
    print("    obedient, it said so in terms, and it declared the fifth site it declined")
    print("    ('adding (LIB-weak) there would be a fifth site and is outside what this")
    print("    ticket lists'). The defect is in the mechanism, not in the worker.")
    print("  * It measures with THIS registry, which was written after the fact and with")
    print("    knowledge of where the sites were. It is not a blind re-run. The count at")
    print("    %s is what a search WOULD have found had the registry existed, not" % BASE)
    print("    what mg-2860 could have found with what it had.")
    print("  * It says nothing about defect classes the registry cannot express -- see the")
    print("    DECLARED LIMITS section of README.md, and in particular that the (A) SPREAD")
    print("    contradiction repaired by this same ticket is INVISIBLE to this instrument.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
