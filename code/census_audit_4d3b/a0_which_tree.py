"""mg-4d3b a0 -- WHICH TREE.  Fetch, resolve, state the sha and the staleness.

mg-f3ff's addendum makes this load-bearing: a `git log --grep` against a stale
checkout returns the same `no successor` for a completely different reason, and
returns it with the authority of having read the tree.  So freshness is
measured here and RE-MEASURED by every other section of this audit -- a
freshness measured once and imported is a claim, not an observation.

This section also asserts something mg-f3ff did not have to: that reaching
repo 1 through THIS WORKTREE gives the same `origin/main` as reaching it
through /Users/daniel/research/onethird_program.  They share `.git`, so they
must -- but "must" is the word that precedes every finding in this arc.

EXIT: 1 if a repo could not be read, or if the two paths to repo 1 disagree.
Findings ABOUT mg-f3ff do not set it.
"""
import sys

import lib4d3b as L


def main():
    L.banner("mg-4d3b a0 -- WHICH TREE: fetch, resolve, state the staleness")
    repos = L.open_repos()
    L.freshness(repos)

    print(__doc__.split("EXIT:")[0].strip())
    print()

    print("-" * 78)
    print("CROSS-PATH CHECK -- worktree vs source repo for repo 1")
    print("-" * 78)
    src = L.Repo("onethird_program(src)", L.SRC1)
    bad = 0
    if src.unknown or repos[0].unknown:
        print(f"  UNKNOWN on one side: worktree={repos[0].reason or 'ok'} "
              f"src={src.reason or 'ok'}")
        bad += 1
    else:
        agree = src.sha == repos[0].sha
        bad += L.check("worktree origin/main == source repo origin/main", agree,
                       f"{repos[0].sha[:12]} vs {src.sha[:12]}")
    print()

    print("-" * 78)
    print("THE POPULATION OF THIS AUDIT, AND WHAT IT CANNOT SEE")
    print("-" * 78)
    print(L.__doc__.split("WHAT THIS AUDIT RANGES OVER")[1].rstrip())
    print()

    print("-" * 78)
    print("THE FOUR ROWS UNDER AUDIT, WITH THE PREMISE EACH TITLE ACTUALLY ASSERTS")
    print("-" * 78)
    print(f"  {'row':<4}{'ticket':<10}{'filed (UTC)':<24}{'parent':<10}premise asserted in the TITLE")
    for n, row, filed, parent, premise in L.ROWS:
        print(f"  {n:<4}{row:<10}{filed:<24}{parent:<10}{premise}")
    print()
    print("  ⚠️ TWO OF THE FOUR TITLES ASSERT TWO PREMISES.  mg-f3ff measures one")
    print("     of them ('no successor').  a2 measures the other.")
    print()

    for r in repos:
        if r.unknown:
            bad += 1
            print(f"  {r.label} UNKNOWN -- every downstream row is UNKNOWN, not empty.")
        else:
            n = len(r.commits())
            nm = len(r.commits(include_merges=False))
            print(f"  {r.label:<22} {n} commit(s) reachable, {n - nm} of them merges")
            print(f"  {'':<22} (mg-f3ff reads the {nm} non-merge commits; its POPULATION")
            print(f"  {'':<22}  text does not say so.  a1 measures whether it matters.)")

    print(f"\n== a0 exit: {1 if bad else 0} ==")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
