#!/usr/bin/env python3
"""
mg-1df8 / CHECK 3 — THE QUANTIFIER GAP MUST SIT WITH THE CLAIM.

This is the check the ticket says the whole failure turned on: the operative
form and the limit form were BOTH in STATE.md, ONE ROW APART, and joining them
was left to the reader.  A cross-reference is explicitly NOT enough.

So the test is CONTIGUITY, and my PREDICTIONS.md P15 bound me to it before I
opened the file:

    "I will fix the (LIB-weak) introduction site by line number first, quote the
     contiguous byte range of that row / cell / bullet verbatim, and score
     checks 2-4 AGAINST THAT QUOTED RANGE ALONE.  Anything found outside it is
     reported as 'present elsewhere, does not discharge', never as a pass."

STATE.md is written one-logical-unit-per-line (a ledger row is one line, a
blockquote paragraph is one line, an axis bullet is one line, a mermaid edge
label is one line).  So the contiguous unit IS the line, and the test is
mechanical: for each line mentioning (LIB-weak), does THAT LINE carry the
quantifier?

GUARD AGAINST MY OWN INSTRUMENT (the lesson mg-94c3 filed: a regex tuned until
it returns 0 is unfalsifiable).  Every site is ALSO printed for reading by hand,
and the negative controls below assert the detector FAILS on text that should
fail it.

Target: STATE.md at 491d42c79f7628c18cb7a5d197faa9f4600cd6c1
"""

import re
import subprocess
import sys

SHA = "491d42c79f7628c18cb7a5d197faa9f4600cd6c1"

# The two things the ticket demands AT THE CLAIM.  Written before the scan and
# deliberately NOT tuned: each is a disjunction of the plain ways English says
# the thing, not a pattern reverse-engineered from what the file happens to say.
DEMAND_A = [                    # "it does not supply the operative form"
    r"does \*?not\*? supply",
    r"not the (constant )?form",
    r"NOT the weakest",
    r"is the stronger",
    r"is \*?stronger\*? than",
    r"closes the \*\*limit\*\*",
    r"closes \*\*row 8 as phrased\*\*",
]
DEMAND_B = [                    # "the gap is a QUANTIFIER"
    r"quantifier",
    r"only for `?n ≥ N₀",
    r"n ≥ N₀",
    r"NO `?N₀`? WORKS FOR THE CLASS",
    r"no `?N₀`? works for the class",
    r"holds only for",
    r"fails at finite `?n",
]
DEMAND_C = [                    # "they differ IN KIND, not by a constant"
    r"differ IN KIND",
    r"differ \*?in kind\*?",
    r"not a constant",
    r"NOT A CONSTANT",
]
# A cross-reference ALONE must not count.  Detected so it can be reported as
# insufficient, per the ticket's own instruction.
XREF = [r"\(row 8", r"see §", r"§ \*The single lemma", r"earlier in this cell"]


def hits(patterns, text):
    return [p for p in patterns if re.search(p, text)]


def main():
    raw = subprocess.run(["git", "show", f"{SHA}:STATE.md"],
                         capture_output=True, text=True, check=True).stdout
    lines = raw.split("\n")
    print(f"STATE.md @ {SHA}")
    print(f"{len(lines)} lines, {len(raw)} bytes\n")

    sites = [(i + 1, l) for i, l in enumerate(lines) if "LIB-weak" in l]
    print(f"(LIB-weak) appears on {len(sites)} lines: "
          f"{[n for n, _ in sites]}\n")

    verdicts = {}
    for lineno, text in sites:
        a, b, c = hits(DEMAND_A, text), hits(DEMAND_B, text), hits(DEMAND_C, text)
        x = hits(XREF, text)
        ok = bool(a) and bool(b) and bool(c)
        # A site that is ONLY a cross-reference fails by the ticket's own rule.
        xref_only = bool(x) and not (a and b and c)
        verdicts[lineno] = ok
        print("=" * 78)
        print(f"SITE line {lineno}   —   {'CARRIES THE GAP' if ok else 'INCOMPLETE'}")
        print("=" * 78)
        print(f"  A  'does not supply the operative form' : "
              f"{a if a else 'ABSENT'}")
        print(f"  B  'the gap is a QUANTIFIER'            : "
              f"{b if b else 'ABSENT'}")
        print(f"  C  'differ IN KIND / not a constant'    : "
              f"{c if c else 'ABSENT'}")
        print(f"  X  cross-references present             : "
              f"{x if x else 'none'}")
        if xref_only:
            print("  >> CROSS-REFERENCE ONLY — by the ticket's own rule this "
                  "DOES NOT DISCHARGE.")
        print()

    # ------------------------------------------------------------------ NC
    print("=" * 78)
    print("NEGATIVE CONTROLS — the detector must FAIL on text that should fail.")
    print("=" * 78)
    ncs = [
        ("NC1 the pre-correction wording (the actual defect, from 21ee93f's "
         "parent f85a4e8-era text)",
         "Sufficient conditions, one-way: **(B) ⟹ LIB ⟹ (LIB-weak) ⟹ "
         "(LIB-const)**, where `E[inv_e] = o(n²)`.",
         False),
        ("NC2 a pure cross-reference, which is what already existed and failed",
         "(LIB-weak) is discussed in row 8 — see § *The single lemma to prove*.",
         False),
        ("NC3 a constant-flavoured gloss (the misreading the ticket fears)",
         "(LIB-weak) and (LIB-const) differ by a constant factor of 6.",
         False),
        ("NC4 the real row-8 text, which must PASS",
         lines[114], True),
    ]
    nc_pass = 0
    for label, text, want in ncs:
        a, b, c = hits(DEMAND_A, text), hits(DEMAND_B, text), hits(DEMAND_C, text)
        got = bool(a) and bool(b) and bool(c)
        ok = (got == want)
        nc_pass += ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
        print(f"          detector says carries-the-gap = {got}, "
              f"expected {want}")
    print(f"\n  {nc_pass}/{len(ncs)} negative controls behave as required.")
    if nc_pass != len(ncs):
        print("  !! DETECTOR IS NOT TRUSTWORTHY — do not read the site table "
              "above as evidence.")
        sys.exit(1)

    # ------------------------------------------------------------------ SUM
    print()
    print("=" * 78)
    print("SUMMARY — CHECK 3")
    print("=" * 78)
    carried = [n for n, v in verdicts.items() if v]
    missing = [n for n, v in verdicts.items() if not v]
    print(f"  sites carrying the gap IN THEIR OWN CONTIGUOUS UNIT: {carried}")
    print(f"  sites NOT carrying it                              : {missing}")
    print("""
  READ BY HAND, NOT TUNED AWAY — every site that the detector marks INCOMPLETE
  is quoted in full in the deliverable and judged in prose, because a detector
  that returns 0 misses by construction is unfalsifiable (mg-94c3's lesson).""")
    for n in missing:
        print(f"\n  --- line {n} verbatim ---")
        print("  " + lines[n - 1][:900])


if __name__ == "__main__":
    main()
