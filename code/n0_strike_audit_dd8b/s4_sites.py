#!/usr/bin/env python3
"""mg-dd8b s4 — resolve the INHERITED line numbers against today's file.

mg-24fb's ticket body hands me a candidate set:

    "mg-5ce3 reports the 'unspecified N_0' reading at :15, :137, :148, :165, :255, :260"
    in OneThird-Literature-LowerBound-MinimalCounterexample-mg-33f5.md
    plus OneThird-LIBweak-mg-c3ca.md:100

I hold those numbers before counting (exposure H2 in PREDICTIONS.md), so my count is not
blind. What IS independent is whether each number lands on the thing it claims to.

This script does one job: for every inherited number, print what is actually on that line
today, and say whether the primary term is there. It also asks whether the file could have
DRIFTED — a wrong line number and a stale line number are different defects with different
fixes, and only git can tell them apart.
"""

import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import libdd8b as L  # mg-20ee: the corpus is read AT A DECLARED COMMIT

INHERITED = {
    "docs/OneThird-Literature-LowerBound-MinimalCounterexample-mg-33f5.md":
        [15, 137, 148, 165, 255, 260],
    "docs/OneThird-LIBweak-mg-c3ca.md": [100],
}

TERM = re.compile(r"unspecified", re.IGNORECASE)


def git(*a):
    return subprocess.run(["git", "-C", REPO] + list(a),
                          capture_output=True, text=True).stdout.strip()


def main():
    rc = 0
    for rel, nums in INHERITED.items():
        lines = L.read_at(rel).split("\n")

        print()
        print("#" * 78)
        print(f"# {rel}")
        print("#" * 78)

        # --- could the numbers have drifted? ---
        log = L.log_at(rel)
        print(f"\n  COMMITS TOUCHING THIS FILE ON origin/main: {len(log)}")
        for l in log:
            print(f"    {l}")
        if len(log) == 1:
            print("    => the file has ONE commit, so NO line can have drifted since it")
            print("       was written. A wrong number here is a MIS-CITATION, not staleness.")

        # --- resolve each inherited number ---
        print(f"\n  INHERITED NUMBERS RESOLVED AGAINST TODAY'S FILE:")
        for n in nums:
            body = lines[n - 1] if 0 < n <= len(lines) else "<OUT OF RANGE>"
            hits = TERM.findall(body)
            mark = "HIT " if hits else "MISS"
            if not hits:
                rc = 1
            short = body.strip()
            if len(short) > 150:
                short = short[:150] + "…"
            print(f"    {mark} :{n:<4} ({len(hits)} occurrence(s))  | {short}")
            if not hits:
                # where IS the nearest occurrence?
                near = [i + 1 for i, l in enumerate(lines)
                        if TERM.search(l) and abs(i + 1 - n) <= 3]
                if near:
                    print(f"          nearest occurrence(s) within 3 lines: {near}")
                    for m in near:
                        s = lines[m - 1].strip()
                        print(f"            :{m}  | {s[:140]}")

        # --- my own enumeration, both units ---
        mine = []
        for i, l in enumerate(lines, start=1):
            for _ in TERM.finditer(l):
                mine.append(i)
        my_lines = sorted(set(mine))
        print(f"\n  MY OWN ENUMERATION (primary term, no judgement applied):")
        print(f"    {len(mine)} OCCURRENCES on {len(my_lines)} LINES: {my_lines}")
        inh = set(nums)
        print(f"    lines I have that the inherited set does NOT: "
              f"{sorted(set(my_lines) - inh)}")
        print(f"    lines the inherited set has that I do NOT:    "
              f"{sorted(inh - set(my_lines))}")
    return rc


if __name__ == "__main__":
    print(L.stamp("s4_sites.py"), end="")
    sys.exit(main())
