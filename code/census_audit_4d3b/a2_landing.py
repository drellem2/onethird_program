"""mg-4d3b a2 -- THE OTHER PREMISE.  `no landing commit` is a claim two of the
four row titles make, and mg-f3ff's instrument cannot express it.

`lib_f3ff.successors()` drops every commit whose owner IS the parent, with the
comment `the parent's own work is not its successor`.  As a definition of
SUCCESSOR that is right and this audit does not dispute it.  But the census's
rows do not only say `no successor` -- rows 1 and 2 say, in their titles,
`no landing commit, no successor`, and the parent's own landing commit is
exactly the object that exclusion removes.  So the deliverable's headline
figure -- `2 of 4` -- is the accuracy of the census on ONE of the two premises
it filed, offered as the accuracy of the census.

This section measures the other one.  For each row: commits OWNED BY the
parent, at or before the filing instant.  A non-empty answer means the parent's
verdict WAS committed and findable in the tree by its own ticket id at the
moment pm-onethird recorded it as having no landing commit.

⚠️ THE HONEST QUALIFICATION, WRITTEN BEFORE THE NUMBERS (P15 of PREDICTIONS.md):
rows 3 and 4's titles say ONLY `no successor`.  A landing commit does not
contradict THEIR titles.  So the finding here, if it lands, is:
  * a MEASUREMENT defect for rows 1 and 2 -- their stated premise is
    unmeasured by the instrument built to check it; and
  * a PRESENTATION defect for rows 3 and 4 -- README §1's `their briefs were
    sound` is a verdict wider than the measurement under it.
Those are different sizes of finding and this section will not merge them.

EXIT: 1 only if a repo is UNKNOWN.
"""
import sys

import lib4d3b as L


def main():
    L.banner("mg-4d3b a2 -- the premise mg-f3ff's instrument cannot express")
    repos = L.open_repos()
    L.freshness(repos)
    if any(r.unknown for r in repos):
        print("  UNKNOWN -- a repo could not be read.  No landing figure is printed,")
        print("  because a landing count taken over part of the population is not a")
        print("  count.  This is the rule mg-f3ff's addendum 3 asks for, applied to")
        print("  the auditor.")
        print("== a2 exit: 1 ==")
        return 1

    print(__doc__.split("⚠️")[1].split("EXIT:")[0].strip())
    print()

    landed = {}
    for n, row, filed, parent, premise in L.ROWS:
        T = L.utc(filed)
        print("-" * 78)
        print(f"ROW {n}: {row} asserts of {parent}: \"{premise}\"")
        print("-" * 78)
        lc = L.landings(repos, parent, T)
        landed[n] = lc
        print(f"  commits OWNED BY {parent}, authored <= {filed}: {len(lc)}")
        for c in lc:
            print(f"      {c.sha[:9]}  {c.adate.isoformat()}  {c.repo}")
            print(f"        {c.subject[:130]}")
        after = [c for c in (L.landings(repos, parent, L.utc("2030-01-01T00:00:00Z")) or [])
                 if c.adate > T]
        print(f"  ...and {len(after)} more owned by {parent} AFTER the filing instant")
        claims_landing = "no landing commit" in premise
        if lc:
            if claims_landing:
                print(f"  >>> THE TITLE'S `no landing commit` CLAUSE IS **FALSE**: "
                      f"{len(lc)} landing commit(s) existed at the filing instant.")
            else:
                print(f"  >>> The title does not claim `no landing commit`, so nothing in")
                print(f"      it is contradicted.  But {len(lc)} landing commit(s) existed,")
                print(f"      which is what README §1's `their briefs were sound` ranges")
                print(f"      over and what its measurement cannot see.")
        else:
            print(f"  >>> 0 landing commits.  Nothing to report on this row.")
        print()

    print("=" * 78)
    print("THE SECOND ACCURACY FIGURE, WITH ITS DENOMINATOR NAMED")
    print("=" * 78)
    claim_rows = [n for n, _r, _f, _p, prem in L.ROWS if "no landing commit" in prem]
    false_rows = [n for n in claim_rows if landed[n]]
    all_landed = [n for n in landed if landed[n]]
    print(f"  Rows whose TITLE asserts `no landing commit`: {len(claim_rows)}  {claim_rows}")
    print(f"  Of those, rows where a landing commit DID exist: {len(false_rows)}  {false_rows}")
    print(f"  Rows (of all 4) whose parent owned >=1 commit at the filing instant:"
          f" {len(all_landed)}  {all_landed}")
    print()
    print("  So the census carries TWO premises and mg-f3ff measured ONE:")
    print(f"    `no successor`      -- wrong on 2 of 4   (mg-f3ff's figure; a1 reproduces it)")
    print(f"    `no landing commit` -- wrong on {len(false_rows)} of {len(claim_rows)} rows that assert it")
    print(f"                           and false-in-fact on {len(all_landed)} of 4 parents")
    print()
    print("  ⚠️ `2 of 4` IS NOT WRONG.  It is right about the premise it names, and")
    print("     README §1's column header names it (`premise \\`no successor\\` is`).")
    print("     What is not right is the paragraph under it, which offers `2 of 4` as")
    print("     THE ACCURACY OF THE CENSUS and says of rows 3 and 4 `their briefs")
    print("     were sound`.  Soundness is a verdict on the whole brief; the")
    print("     measurement under it covers one clause of the title.")
    print()
    print("  P6 SCORING:")
    print(f"    predicted: all 4 parents own >=1 commit at or before their instant")
    print(f"    observed : {len(all_landed)} of 4  ->"
          f" {'HIT' if len(all_landed) == 4 else 'MISS'}")
    print("    (half NOT BLIND: D5 of PREDICTIONS.md already had rows 3 and 4 by hand.")
    print("     Rows 1 and 2 were blind.)")
    print()
    print("  P15 SCORING -- my own pre-filed most-likely error:")
    if len(false_rows) == len(claim_rows) and claim_rows:
        print("    P15 does NOT fire in its strong form.  Both rows that assert")
        print("    `no landing commit` do have landing commits, so this is a")
        print("    MEASUREMENT finding on rows 1 and 2, not only a presentation one.")
    else:
        print("    P15 FIRES.  The rows asserting the clause do not have landing")
        print("    commits, so the finding is presentational and is reported as such.")
    print("\n== a2 exit: 0 ==")
    return 0


if __name__ == "__main__":
    sys.exit(main())
