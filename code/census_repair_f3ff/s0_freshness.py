"""mg-f3ff s0 -- WHICH TREE.  Fetch every repo, resolve origin/main, state the
sha, and measure how far behind each checkout was when this run started.

This section exists because the ticket's addendum says the instrument it told
me to switch to has its own version of the defect the ticket is about: a
`git log --grep` against a checkout 25 commits stale reports `no successor`
with the authority of having read the tree.  So freshness is a MEASUREMENT
here, printed with the numbers, and not a precondition anyone is trusted to
have met.

Exit is 1 only if a repo could not be read at all -- that is a fact about this
instrument.  Findings about the census do not set it.
"""
import sys

import lib_f3ff as L


def main():
    L.banner("mg-f3ff s0 -- WHICH TREE: fetch, resolve, and state the staleness")
    fm = L.fetch_all()
    L.print_freshness(fm)

    print(L.POPULATION)
    print()
    print(L.BLIND_SPOTS)
    print()

    print("THE FOUR ROWS OF THE CENSUS UNDER REPAIR")
    print("  row  dropped-verdict  filed (UTC)           parent    parent's `repo:` field")
    for n, row, filed, parent in L.ROWS:
        repo = "one_third_width_three" if row == "mg-fccb" else "onethird_program"
        print(f"   {n}   {row}         {filed}  {parent}  {repo}")
    print()
    print("  Each row's TITLE asserts of its parent some form of `no landing commit`")
    print("  / `no successor`.  s1 re-derives all four from the tree.")
    print()

    bad = sum(1 for f in fm.values() if f.unknown)
    if bad:
        print(f"  {bad} repo(s) UNKNOWN -- s1 will print UNKNOWN rows, not empty ones.")
    print(f"== s0 exit: {1 if bad else 0} ==")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
