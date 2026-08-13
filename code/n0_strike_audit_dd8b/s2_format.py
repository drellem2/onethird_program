#!/usr/bin/env python3
"""mg-dd8b s2 — the strike-format reference standard, recorded BEFORE mg-24fb writes a byte.

My brief says:

    "CHECK THE FORMAT MATCHES mg-2df8's. mg-2df8 already struck neighbouring sentences
     in OneThird-LIBweak-mg-c3ca.md. Two strike formats in one file is a defect in its
     own right. Compare them directly."

That instruction presumes there is ONE format in the file to match. This script tests
that presumption instead of inheriting it. It is run against the PRE-mg-24fb file so
that the reference standard is a measurement taken before the thing being measured
against it exists — it cannot be back-fitted.

Two structures are counted separately, because conflating them is how "one format"
gets asserted:

    STRIKE      the ~~struck text~~ itself
    MARKER      the bracketed/parenthesised annotation naming the supersession
"""

import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import libdd8b as L  # mg-20ee: the corpus is read AT A DECLARED COMMIT

TARGETS = [
    "docs/OneThird-LIBweak-mg-c3ca.md",
    "docs/OneThird-Literature-LowerBound-MinimalCounterexample-mg-33f5.md",
]

# Marker openers seen in this corpus. Kept deliberately as three SEPARATE patterns so
# the script reports which shape each site uses rather than smoothing them into one.
MARKER_SHAPES = [
    ("A: **[NAME — mg-XXXX, on <src> §N.**  (bracket, em-dash, 'on', closing '.**')",
     r"\*\*\[([A-Z][A-Z0-9 '’\-]+?)\s+—\s+(mg-[0-9a-f]{4})\s*,\s*on\s+([^.]*?)\.\*\*"),
    # NOTE — INSTRUMENT DEFECT FOUND BY MY OWN FIRST RUN AND FIXED HERE, NOT TUNED AWAY.
    # The first version of this pattern was `[^:\]]*?` between the em-dash and the
    # colon. That is greedy across the `.**` that ENDS a shape-A marker, so shape A's
    # site :52 also matched shape B on the strength of a colon 60 words later, and the
    # script reported 2 shape-B sites where there is 1. Excluding `*` from the run
    # confines the match to the marker's own head, which is the thing that
    # distinguishes the shapes. Recorded because a shape census that silently
    # double-counts is exactly the instrument error this audit is about.
    ("B: **[NAME — <who>: ...]**            (bracket, em-dash, COLON)",
     r"\*\*\[([A-Z][A-Z0-9 '’\-]+?)\s+—\s+([^:\]*]*?):"),
    ("C: > **NAME (mg-XXXX, ...) — ...**    (blockquote, PARENTHESES, no bracket)",
     r"^\s*>\s*\*\*([A-Z][A-Z0-9 '’\-]+?)\s*\((mg-[0-9a-f]{4})[^)]*\)\s*—"),
]

STRIKE = r"~~(.+?)~~"
ANY_MARKER_OPEN = r"\*\*\[([A-Z][A-Z0-9 '’\-]{3,}?)\s"


def closers(text):
    """How does each bracketed marker CLOSE? Three variants exist and they differ."""
    found = []
    for m in re.finditer(r"\*\*\[", text):
        start = m.start()
        window = text[start:start + 4000]
        # first of the three closing shapes to appear
        cands = []
        for lbl, pat in [("**]**", r"\*\*\]\*\*"), ("**]", r"\*\*\](?!\*)"),
                         ("]**", r"(?<!\*)\]\*\*"), ("]", r"(?<![\*])\](?!\*)")]:
            mm = re.search(pat, window)
            if mm:
                cands.append((mm.start(), lbl))
        cands.sort()
        lineno = text[:start].count("\n") + 1
        found.append((lineno, cands[0][1] if cands else "<UNCLOSED>"))
    return found


def run(rel):
    text = L.read_at(rel)
    lines = text.split("\n")

    print()
    print("#" * 78)
    print(f"# {rel}   ({len(lines)} lines)")
    print("#" * 78)

    # --- strikes ---
    strikes = []
    for i, line in enumerate(lines, start=1):
        for m in re.finditer(STRIKE, line):
            strikes.append((i, m.group(1)))
    print(f"\n  STRIKES (~~...~~): {len(strikes)} OCCURRENCES on "
          f"{len({s[0] for s in strikes})} LINES")
    for ln, body in strikes:
        b = body if len(body) <= 90 else body[:90] + "…"
        print(f"    :{ln}  ~~{b}~~")

    # --- markers, by shape ---
    print(f"\n  MARKER SHAPES:")
    shape_hits = {}
    for label, pat in MARKER_SHAPES:
        hits = []
        for m in re.finditer(pat, text, re.MULTILINE):
            ln = text[:m.start()].count("\n") + 1
            hits.append((ln, m.group(1).strip()))
        shape_hits[label] = hits
        print(f"    {len(hits)}  {label}")
        for ln, name in hits:
            print(f"         :{ln}  {name!r}")

    distinct_shapes = sum(1 for v in shape_hits.values() if v)
    print(f"\n  DISTINCT MARKER SHAPES PRESENT IN THIS FILE: {distinct_shapes}")

    # --- closing delimiters ---
    cl = closers(text)
    if cl:
        print(f"\n  CLOSING DELIMITER of each bracketed marker:")
        for ln, c in cl:
            print(f"    :{ln}  closes with  {c}")
        variants = sorted({c for _, c in cl})
        print(f"    DISTINCT CLOSING DELIMITERS: {len(variants)}  {variants}")

    # --- who authored each marker ---
    print(f"\n  AUTHOR ATTRIBUTION inside markers:")
    for m in re.finditer(r"\*\*\[[^\]]{0,200}?(mg-[0-9a-f]{4})", text):
        ln = text[:m.start()].count("\n") + 1
        print(f"    :{ln}  attributes to {m.group(1)}")

    return distinct_shapes, len(strikes)


def positive_control():
    """Prove the shape detectors fire on planted instances of all three shapes."""
    planted = "\n".join([
        "text ~~struck bit~~ **replacement**.",
        "**[ROW REFERENCE REPAIRED — mg-2df8, on mg-c4f5 §6.** prose here.**]**",
        "**[SUPERSEDED INPUT REPAIRED — mg-e35c F5, landed mg-5827: prose here.]**",
        "> **CORRECTED AT SOURCE (mg-55f2, landing mg-65f5's §1.5) — prose here.**",
    ])
    print()
    print("#" * 78)
    print("# POSITIVE CONTROL — one planted instance of each shape")
    print("#" * 78)
    ok = True
    for label, pat in MARKER_SHAPES:
        n = len(re.findall(pat, planted, re.MULTILINE))
        good = n >= 1
        ok = ok and good
        print(f"  {'PASS' if good else 'FAIL':4}  shape {label.split(':')[0]} found {n}")
    n_strike = len(re.findall(STRIKE, planted))
    print(f"  {'PASS' if n_strike == 1 else 'FAIL':4}  strike detector found {n_strike}")
    ok = ok and n_strike == 1
    print(f"\n  {'POSITIVE CONTROL PASSED' if ok else 'POSITIVE CONTROL FAILED'}")
    return ok


def main():
    ok = positive_control()
    results = {}
    for rel in TARGETS:
        results[rel] = run(rel)
    print()
    print("=" * 78)
    print("VERDICT ON THE BRIEF'S PRESUMPTION")
    print("=" * 78)
    for rel, (shapes, nstrike) in results.items():
        print(f"  {os.path.basename(rel)}")
        print(f"     distinct marker shapes: {shapes}     strikes: {nstrike}")
    print()
    print("  My brief says 'Two strike formats in one file is a defect in its own right'")
    print("  and directs me to make mg-24fb match mg-2df8's. Read the numbers above")
    print("  before accepting that there is a single format to match.")
    print("=" * 78)
    return 0 if ok else 1


if __name__ == "__main__":
    print(L.stamp("s2_format.py"), end="")
    sys.exit(main())
