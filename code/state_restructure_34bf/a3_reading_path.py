#!/usr/bin/env python3
"""mg-34bf acceptance (c): the three A3 sites that disagreed under mg-1319 can be read in
sequence in under a minute.

The three sites are the ones `STATE.md` itself names at the "three incompatible ways in one
commit" paragraph: the mg-276d ledger row, Appendix A's *"STEP 4d HAS NOW FIRED AT ..."*
paragraph, and template step 4d.  This script locates all three in the CURRENT file, prints
what each of them now asserts about the count, and times the sequence at 250 wpm.

Before the restructure the first site was a 13,190-byte single table cell whose step-4d
clause began at byte 1,161 and ran, interleaved with the row's mathematics, to byte 4,800 --
so "read the three in sequence" meant reading a 13 KB cell to find one clause in it.

Run from the repo root:  python3 code/state_restructure_34bf/a3_reading_path.py
"""
import re, subprocess, sys

WPM = 250
BASE = "60f4dac0be109513c75ba6985694ec1a0eb4e8d3"


def words(s):
    return len(re.sub(r"\s+", " ", s).strip().split(" "))


def main():
    new = open("STATE.md", encoding="utf-8").read()
    lines = new.split("\n")
    old_lines = subprocess.run(["git", "show", f"{BASE}:STATE.md"], capture_output=True,
                               text=True, check=True).stdout.split("\n")

    # --- site 1: the step-4d clause in the mg-276d ledger row -------------------------
    row_i = next(i for i, l in enumerate(lines) if "GREEN · PROVEN, all finite posets" in l)
    m = re.search(r"\*\*⚠️ STEP 4d DID FIRE HERE.*?\)\. ", lines[row_i], re.S)
    site1 = m.group(0)
    hist = "docs/state-history/attempt-mg-276d.md"
    h1 = open(hist, encoding="utf-8").read()
    h1_sec = h1[h1.index("### H1 —"):h1.index("### H2 —")]

    # what the same clause cost to reach before
    old_row = next(l for l in old_lines if "GREEN · PROVEN, all finite posets" in l)
    old_start = old_row.index("After **five consecutive over-wide generalisations**")
    old_end = old_row.index("**The mathematics.**")

    # --- site 2: Appendix A's tally paragraph ------------------------------------------
    s2_i = next(i for i, l in enumerate(lines) if l.startswith("**STEP 4d HAS NOW FIRED AT"))
    site2 = lines[s2_i]
    # --- site 3: template step 4d ------------------------------------------------------
    s3_i = next(i for i, l in enumerate(lines) if l.startswith("> **4d. GENERALISATION AUDIT."))
    site3 = lines[s3_i]

    # the count-bearing assertion at each site
    a2 = site2[:site2.index("**", site2.index("FIRED AT"))] + "**"
    a3 = re.search(r"\*\*NINE firings AT LEAST.*?tally\*\*", site3).group(0)

    print("THE THREE A3 SITES, IN READING ORDER\n")
    rows = [
        (f"1a  STATE.md:{row_i+1}  ledger row (mg-276d) — the step-4d clause, now the "
         f"SECOND sentence of the cell", site1),
        (f"1b  {hist}  §H1 — the relocated text, if you want it", h1_sec),
        (f"2   STATE.md:{s2_i+1}  Appendix A — first tally heading", a2),
        (f"3   STATE.md:{s3_i+1}  Appendix A — template step 4d, count clause", a3),
    ]
    tot_min = tot_all = 0
    for label, text in rows:
        w = words(text)
        print(f"  {label}\n      {w:>5} words   {w/WPM*60:>6.1f} s @ {WPM} wpm")
        tot_all += w
        if not label.startswith("1b"):
            tot_min += w
    print()
    print(f"  minimum sequence (1a, 2, 3 — the three assertions themselves): "
          f"{tot_min} words, {tot_min/WPM*60:.1f} s")
    print(f"  with the relocated history read in full (1a, 1b, 2, 3)      : "
          f"{tot_all} words, {tot_all/WPM*60:.1f} s")
    print()
    print("WHAT SITE 1 NOW ASSERTS ABOUT THE COUNT")
    num = re.search(r"(?i)\b(five|six|seven|eight|nine|ten)\b", site1)
    print(f"  states or quotes a firing count: {'YES — ' + num.group(0) if num else 'NO'}")
    print(f"  Only sites 2 and 3 carry a number, and they are {abs(s3_i - s2_i)} lines apart in")
    print("  one file, so a recount cannot leave them disagreeing across two documents.")
    if num:
        raise SystemExit("FAIL — the ledger row hard-codes a count that Appendix A recounts.")
    print()
    print("BEFORE (base commit)")
    print(f"  the same clause sat inside a {len(old_row):,}-byte single table cell,")
    print(f"  starting at byte {old_start:,} and running to byte {old_end:,} of it;")
    print(f"  reaching it meant reading {words(old_row[:old_start])} words of the row first.")
    ok = tot_min / WPM * 60 < 60
    print()
    print("PASS — the three assertions read in sequence in under a minute." if ok else
          "FAIL — the minimum sequence exceeds a minute.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
