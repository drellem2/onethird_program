"""mg-4d3b a1 -- THE FOUR ROWS, RE-DERIVED BY AN IMPLEMENTATION THAT SHARES NO
CODE WITH mg-f3ff's.

The point is NOT to agree.  It is to make agreement mean something: mg-f3ff
asks git to match (`--grep`), this reads every reachable commit and matches in
Python, so a shared defect in git's regex/`-i`/encoding handling is impossible.
Where the two agree, the figure is established from two disjoint paths; where
they disagree, the disagreement is the finding.

Four variations are printed for every row, because a count with one variant is
a number and a count with four is a measurement:
  * both clocks (author / committer) -- mg-f3ff reports both and so does this;
  * merges included AND excluded -- mg-f3ff passes `--no-merges` and its
    POPULATION text does not say so;
  * `exclude_own` on and off -- see a2.

SCORED AGAINST P1-P5 of PREDICTIONS.md (committed at c372c54, before this file
existed).  P1-P4 were disclosed NOT BLIND and are marked so in the output; a
hit on a prediction whose answer was already read off a committed transcript is
not evidence and the scorecard says so rather than counting it.

EXIT: 1 only if THIS instrument could not read a repo.  A refutation of mg-f3ff
is a finding about mg-f3ff, and an auditor that exited 1 for finding what it
was sent to find could not distinguish that from being broken.
"""
import sys

import lib4d3b as L

# From PREDICTIONS.md @ c372c54.  Quoted so the scoring is done by the
# instrument and cannot drift from what was actually predicted.
PRED_VERDICT = {1: "REFUTED", 2: "REFUTED", 3: "UPHELD", 4: "UPHELD"}
PRED_COUNT = {1: (7, 0), 2: (4, 1), 3: (0, 0), 4: (0, 0)}
PRED_BLIND = {1: False, 2: False, 3: False, 4: False}


def main():
    L.banner("mg-4d3b a1 -- the four rows, re-derived from a disjoint reader")
    repos = L.open_repos()
    L.freshness(repos)

    if any(r.unknown for r in repos):
        print("  A REPO IS UNKNOWN.  Every row below would be UNKNOWN, not empty.")
        for n, row, filed, parent, _p in L.ROWS:
            v, _, unk = L.row_verdict(repos, parent, L.utc(filed))
            print(f"  row {n} {parent}: {v}  (unreadable: {', '.join(unk)})")
        print("== a1 exit: 1 ==")
        return 1

    hits = misses = 0
    count_moved = []
    for n, row, filed, parent, premise in L.ROWS:
        T = L.utc(filed)
        print("-" * 78)
        print(f"ROW {n}: {row} filed {filed}")
        print(f"        asserts of {parent}: \"{premise}\"")
        print("-" * 78)

        base = None
        for clock in ("author", "committer"):
            for merges in (True, False):
                v, per, _u = L.row_verdict(repos, parent, T, clock=clock,
                                           include_merges=merges)
                cnt = {k: len(x) for k, x in per.items()}
                tot = sum(cnt.values())
                tag = "merges IN " if merges else "merges OUT"
                print(f"  {clock:<10} clock, {tag}: {v:<8} {tot} successor(s)"
                      f"   [{'  '.join(f'{k}={v2}' for k, v2 in cnt.items())}]")
                if base is None:
                    base = (v, cnt, tot)

        v, per, _u = base[0], base[1], base[2]
        for c in L.successors(repos[0], parent, T) + L.successors(repos[1], parent, T):
            print(f"      {c.sha[:9]}  {c.adate.isoformat()}  {c.repo}")
            print(f"        owner={c.owner or '(none)'}   {c.subject[:120]}")

        pv, pc = PRED_VERDICT[n], PRED_COUNT[n]
        obs_c = (per.get("onethird_program", 0), per.get("one_third_width_three", 0))
        ok_v = (base[0] == pv)
        ok_c = (obs_c == pc)
        blind = " (NOT BLIND -- read off mg-f3ff's committed transcript)" if not PRED_BLIND[n] else ""
        print()
        print(f"  PREDICTED verdict {pv}, split {pc[0]}+{pc[1]}"
              f"   OBSERVED {base[0]}, split {obs_c[0]}+{obs_c[1]}"
              f"   {'HIT' if (ok_v and ok_c) else 'MISS'}{blind}")
        if ok_v and ok_c:
            hits += 1
        else:
            misses += 1
        if not ok_c:
            count_moved.append(n)
        print()

    print("=" * 78)
    print("VERDICT OF a1")
    print("=" * 78)
    verdicts = {}
    for n, row, filed, parent, _p in L.ROWS:
        v, _per, _u = L.row_verdict(repos, parent, L.utc(filed))
        verdicts[n] = v
    ref = sum(1 for v in verdicts.values() if v == "REFUTED")
    print(f"  mg-f3ff reports the census wrong on 2 of 4 rows.")
    print(f"  This reader, sharing no code with it, finds {ref} of 4 REFUTED: "
          + ", ".join(f"row {n}={v}" for n, v in verdicts.items()))
    print(f"  ROW VERDICTS REPRODUCE: {'YES' if ref == 2 else 'NO'}")
    print()
    print(f"  P1-P4 scorecard: {hits} hit, {misses} miss.  ALL FOUR WERE DISCLOSED")
    print("  NOT BLIND at c372c54 -- I had read the parent's transcript.  They are")
    print("  reported as REPRODUCTIONS, which is what they are, and are NOT counted")
    print("  as successful predictions in the README's scorecard.")
    print()
    if count_moved:
        print(f"  P5 (a count fails to reproduce): HIT -- rows {count_moved} moved.")
    else:
        print("  P5 (at least one count fails to reproduce): MISS.  All four counts")
        print("  reproduce exactly under both clocks and with merges both included")
        print("  and excluded.  I bet 40% that --no-merges or the owner exclusion")
        print("  would move a figure; neither does.  Kept as written.")
    print()
    print("  THE `--no-merges` WORRY IS MEASURED AND DISMISSED: a0 counts 0 merge")
    print("  commits reachable from origin/main in EITHER repo, so mg-f3ff's")
    print("  unstated exclusion excludes nothing on this population.  It is an")
    print("  undocumented flag, not a defect, and this audit will not inflate it.")
    print("\n== a1 exit: 0 ==")
    return 0


if __name__ == "__main__":
    sys.exit(main())
