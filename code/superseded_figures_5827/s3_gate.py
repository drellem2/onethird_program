#!/usr/bin/env python3
"""s3 — THE GATE (mg-5827). Scan the tracked corpus at the index and fail on any flat-text site.

This is the step a runner or a pre-merge check would call. It prints every bucket with a count,
so a PASS is a statement about a population whose size is printed rather than a green tick over
an unknown denominator.

Exit 1 if any DEFECT.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib5827 as L                                                  # noqa: E402


def main() -> int:
    reg = L.Registry.load()
    files = L.tracked_files()
    occs = L.scan(reg=reg)

    print(L.banner("THE POPULATION THIS GATE ACTUALLY SEARCHED"))
    print("  tracked text files scanned : %d" % len(files))
    print("  registry entries           : %d  (%s)"
          % (len(reg.entries), ", ".join(e["id"] for e in reg.entries)))
    print("  regexes                    : %d" % sum(len(e["patterns"]) for e in reg.entries))
    print("  declared authorities       : %d" % len(reg.authorities))
    print()
    import subprocess as _sp
    all_tracked = [n for n in _sp.run(["git", "ls-files", "-z"], capture_output=True)
                   .stdout.decode("utf-8", "replace").split("\0") if n]
    dropped = [n for n in all_tracked if L.excluded_from_population(n)]
    non_text = [n for n in all_tracked
                if not n.endswith(L.TEXT_SUFFIXES) and not L.excluded_from_population(n)]
    print()
    print("  WHAT WAS NOT SEARCHED, SIZED RATHER THAN OMITTED:")
    print("    tracked files of a non-text suffix : %d" % len(non_text))
    print("    this instrument's own transcripts  : %d  %s"
          % (len(dropped), sorted(dropped)))
    print("    (the transcripts are OUT OF THE POPULATION, not merely exempt — they record")
    print("     every occurrence the gate finds, so leaving them in made the census grow with")
    print("     the number of times anyone had run it. See lib5827.excluded_from_population.)")
    print()
    print("  A PASS below is a statement about THESE %d files and THESE %d registry entries."
          % (len(files), len(reg.entries)))
    print("  It is not a statement that the corpus contains no stale figures.")

    L.emit("GATE SCAN @ index", occs)

    print(L.banner("DIRECTION OF EACH REGISTERED ERROR"))
    print("  Size is not the whole story. A stale figure that makes things look BETTER and one")
    print("  that makes them look WORSE fail differently.")
    for e in reg.entries:
        n = len([o for o in occs if o.entry_id == e["id"]])
        print("\n  %-22s occurrences=%d" % (e["id"], n))
        print("    %s -> %s   (%s)" % (e["superseded"], e["repaired"], e["corrected_by"]))
        print("    DIRECTION: %s" % e["direction"])

    return L.main_exit(occs)


if __name__ == "__main__":
    sys.exit(main())
