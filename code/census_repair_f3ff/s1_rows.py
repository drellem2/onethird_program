"""mg-f3ff s1 -- THE FOUR ROWS, RE-DERIVED FROM THE TREE.

For each row: every successor commit at or before the filing instant, in BOTH
repos, under BOTH clocks, with the chain's generation depth; then the row's
verdict scored against what PREDICTIONS.md (72e36cb, committed before this file
existed) predicted for it.

⚠️ A prediction is never edited because the result disagreed with it.  A
refuted prediction is a RESULT.  This script prints MISS in that case and the
number of misses is part of the deliverable, not a defect of it.

⚠️ AND THE SUMMARY MAY NOT DISAGREE WITH THE ROWS (mg-cf83).  mg-4d3b ran this
file against a repo whose `git fetch` really failed.  The row sections were
right -- verdict UNKNOWN, count `?`, `CHAIN: UNKNOWN`, the reason named -- and
then, IN THE SAME TRANSCRIPT, the summary block printed `n = 4, and all 4 are
now checked against the tree`, `The census was WRONG on 0 of its 4 rows and
RIGHT on 0`, `4 of 4 checked, 0 refuted`, and four rows of `0 / 0`, before
dying on `len(None)`.  A total fetch failure read as a clean, confident,
fully-measured result, in the part a human reads first.

Three rules now hold in this file and each is exercised by the positive control
in `code/summary_guard_cf83/`, against a REAL broken remote:

  1  `?` and `0` are different answers.  `0 if not gens else len(gens)` merged
     them, because `not None` is True.  `cell()` below does not.
  2  No fixed string asserts a count that was not measured.  Every sentence
     carrying a figure has a branch for the case where the figure does not
     exist, and that branch prints UNKNOWN -- not 0.
  3  EVERY SUMMARY FIGURE IS DERIVED FROM `lines`, which is the row sections'
     own output.  Nothing after the row loop re-reads a repo or recomputes from
     a source that can be None, so the summary cannot contradict the rows: if
     the rows say UNKNOWN, the summary says UNKNOWN.
"""
import sys

import lib_f3ff as L


def cell(x):
    """One depth-table cell: `?` when the figure was not measured.

    ⚠️ THIS IS mg-4d3b's F1.  The expression it replaces was
    `0 if not gens else len(gens)`, and `not None` is True, so a repo that
    could not be read rendered as `0 / 0` -- `I could not look` printed as
    `I looked and found none`, in the summary block of the deliverable sent to
    remove exactly that merger.  `generations()` returns None for unreadable
    and [] for a genuinely empty chain; the two must not render alike."""
    return "?" if x is None else str(x)


def score(pred, got):
    """HIT / MISS / UNMEASURED -- a prediction is scored only against a
    measurement.  UNKNOWN is not a wrong prediction, it is no result, and
    printing MISS for it asserts an outcome this run did not observe."""
    if got == "UNKNOWN":
        return "UNMEASURED"
    return "HIT" if pred == got else "MISS"


def show(gen_list, clock):
    n = 0
    for gi, gen in enumerate(gen_list, 1):
        print(f"    generation {gi}  ({len(gen)} commit(s))")
        for label, c, via in gen:
            n += 1
            d = (c.adate if clock == "author" else c.cdate)
            print(f"      {c.sha[:9]}  {d.isoformat()}  {label}")
            print(f"        owner={c.owner or '(none)'}  names={via}")
            print(f"        {c.subject[:150]}")
    return n


def main():
    L.banner("mg-f3ff s1 -- the four rows re-derived from the commit log")
    fm = L.fetch_all()
    L.print_freshness(fm)

    verdicts, misses, unscored, lines = {}, [], [], []
    gen_counts = {}
    for n, row, filed, parent in L.ROWS:
        T = L.utc(filed)
        print("-" * 78)
        print(f"ROW {n}: {row} filed {filed} -- asserts of {parent}: no successor")
        print("-" * 78)

        for clock in ("author", "committer"):
            v, per_repo, unk = L.census_row(fm, parent, T, clock=clock)
            tot = "?" if unk else sum(len(x) for x in per_repo.values())
            per = "  ".join(
                f"{lab}={'UNKNOWN' if s is None else len(s)}"
                for lab, s in per_repo.items())
            print(f"  {clock:<9} clock: {v:<8} {tot} successor commit(s)   [{per}]")
            if unk:
                print(f"    UNKNOWN because these repos could not be read: {', '.join(unk)}")
            if clock == "author":
                verdicts[n] = v

        print()
        gens = L.generations(fm, parent, T, clock="author", mode="strict")
        loose = L.generations(fm, parent, T, clock="author", mode="loose")
        if gens is None:
            print("  CHAIN: UNKNOWN -- a repo could not be read.")
        elif not gens:
            print("  CHAIN: none.  0 generations, 0 successor commits before the filing")
            print("         instant.  The row's premise is TRUE AS WRITTEN.")
        else:
            print(f"  CHAIN (strict -- ancestor named in the SUBJECT from gen 2 on):")
            print(f"    {len(gens)} generation(s), {sum(len(g) for g in gens)} commit(s), "
                  f"all authored before {filed}:")
            show(gens, "author")
            print()
            print(f"  CHAIN (loose -- ancestor named anywhere in the message): "
                  f"{len(loose)} generation(s), {sum(len(g) for g in loose)} commit(s).")
            print("    The gap between the two is blind spot B7 -- MENTION IS NOT DESCENT --")
            print("    measured on this very population rather than merely listed.  The loose")
            print("    reader compounds citations into 'generations' and reports the")
            print("    neighbourhood as a chain.  The strict figure is the one this row")
            print("    reports; the loose figure is its upper bound.")
        # ⚠️ None (unreadable) is carried as None, NOT flattened to 0.  `not
        # gens` was True for both None and [], which is mg-4d3b's F1.
        gen_counts[n] = (None if gens is None else len(gens),
                         None if gens is None else sum(len(g) for g in gens),
                         None if loose is None else len(loose),
                         None if loose is None else sum(len(g) for g in loose))

        pred = L.PREDICTED[n]
        got = verdicts[n]
        sc = score(pred, got)
        if sc == "MISS":
            misses.append(n)
        elif sc == "UNMEASURED":
            unscored.append(n)
        tag = {"HIT": "HIT",
               "MISS": "*** MISS ***",
               "UNMEASURED": "*** UNMEASURED -- the row could not be read, so "
                             "this is NOT a miss ***"}[sc]
        print()
        print(f"  PREDICTED (72e36cb, before any script existed): {pred}"
              f"    OBSERVED: {got}    {tag}")
        print(f"  (P{n} was disclosed as NOT BLIND: a hand grep had already shown this.)")
        print()
        g = gen_counts.get(n, (None, None, None, None))
        lines.append((n, row, parent, got, pred, sc, g[0], g[1], g[2], g[3]))

    # ----------------------------------------------------------------------
    # THE SUMMARY BLOCK.  ⚠️ RULE 3 OF THE DOCSTRING IS ENFORCED BY WHAT IS IN
    # SCOPE HERE: every figure below is a fold over `lines`, which the row
    # sections above printed.  No repo is re-read, no library call that can
    # return None is made, and no sentence carrying a count lacks a branch for
    # the count not existing.
    # ----------------------------------------------------------------------
    ref = sum(1 for x in lines if x[3] == "REFUTED")
    up = sum(1 for x in lines if x[3] == "UPHELD")
    unk = sum(1 for x in lines if x[3] == "UNKNOWN")
    n_rows = len(lines)
    measured = n_rows - unk
    unk_rows = ", ".join(str(x[0]) for x in lines if x[3] == "UNKNOWN")

    print("=" * 78)
    print("THE CENSUS'S ACCURACY, WITH THE DENOMINATOR NAMED")
    print("=" * 78)
    if unk:
        print("  ⚠️ THIS RUN DID NOT MEASURE THE CENSUS.  Read no figure below as one.")
        print()
    print("  Population: the FOUR DROPPED VERDICT tickets pm-onethird filed between")
    print("  2026-07-31T04:12:41Z and 04:22:50Z.  Not a sample of a larger set -- the")
    if unk:
        print(f"  whole census.  n = {n_rows}, and {measured} of {n_rows} are checked against the tree:")
        print(f"  ROW(S) {unk_rows} ARE UNKNOWN because a repo they range over could not be")
        print("  read.  An unchecked row is not a row that was checked and found empty,")
        print("  and it is not counted as checked here.")
    else:
        print(f"  whole census.  n = {n_rows}, and all {n_rows} are now checked against the tree.")
    print()
    print("  row  ticket    parent    premise `no successor` is   strict gens/commits"
          "   loose gens/commits   predicted")
    for n, row, parent, got, pred, sc, g, c, lg, lc in lines:
        mark = {"HIT": "", "MISS": "  <-- MISS",
                "UNMEASURED": "  <-- UNMEASURED"}[sc]
        print(f"   {n}   {row}   {parent}   {got:<24}   {cell(g):>6} / {cell(c):<9}"
              f"   {cell(lg):>5} / {cell(lc):<8}   {pred}{mark}")
    print()
    print(f"  REFUTED {ref} of {n_rows}.  UPHELD {up} of {n_rows}.  UNKNOWN {unk} of {n_rows}.")
    if unk:
        print("    ^ these are counts of VERDICT VALUES.  A 0 there is not a finding")
        print("      that nothing was refuted; it is the absence of a verdict to count.")
        print(f"  The census was WRONG on UNKNOWN of its {n_rows} rows and RIGHT on UNKNOWN.")
        print(f"  Neither slot is zero -- {unk} row(s) returned no measurement, and a")
        print("  count taken over part of the population is not a count.  Before")
        print("  mg-cf83 this sentence carried two zeros under exactly this failure,")
        print("  which reads as a finished result and was computed from nothing.")
    else:
        print(f"  The census was WRONG on {ref} of its {n_rows} rows and RIGHT on {up}.")
    print()
    print("  The brief's own figure was `1-of-1 refuted so far on a population of 4`,")
    if unk:
        print("  with 3 rows unchecked.  THIS RUN DOES NOT SUPERSEDE IT: "
              f"{measured} of {n_rows} checked,")
        print("  refuted UNKNOWN.  A figure is superseded by a figure, and there is")
        print("  none here to do it with.")
    else:
        print("  with 3 rows unchecked.  That figure is now SUPERSEDED, not contradicted:")
        print(f"  {measured} of {n_rows} checked, {ref} refuted.  `{ref} of 4 wrong` and "
              "`4 of 4 wrong` are")
        print("  different claims and this does not round toward either.")
    print()
    print("-" * 78)
    print("SUB-CLAUSES OF P2 AND P5, SCORED SEPARATELY -- a prediction can be right")
    print("about the verdict and wrong about the detail, and both are recorded.")
    print("-" * 78)
    T2 = L.utc("2026-07-31T04:12:41Z")
    print("  P2 said row 2 is refuted in BOTH repos.")
    # ⚠️ THE GUARD IS ROW 2's OWN VERDICT, printed above, and not a fresh read.
    # This is where mg-4d3b's F5 killed the script: `len(L.successors(...))`
    # on None, 30 lines from the docstring saying callers must not treat None
    # as an empty list.  Gating on the row's verdict makes the crash
    # unreachable AND makes this sub-clause unable to disagree with the row.
    per2 = ({lab: L.successors(fm[lab], "mg-d112", T2) for lab, _ in L.REPOS}
            if verdicts.get(2) != "UNKNOWN" else
            {lab: None for lab, _ in L.REPOS})
    if any(s is None for s in per2.values()):
        print("    UNMEASURED -- row 2 came back UNKNOWN above, so there are no")
        print("    per-repo successor counts for mg-d112 and none are printed.  `0 in")
        print("    both repos` would be the census's own defect, printed by the")
        print("    instrument built to repair it.")
        print("  P2 also said those successors were `all authored on 2026-07-29, two days")
        print("    before the row was filed`.")
        print("    P2 sub-clause: UNMEASURED -- there is no successor set to date.")
    else:
        s2 = [c for lab, _ in L.REPOS for c in per2[lab]]
        per_repo_ok = all(len(per2[lab]) > 0 for lab, _ in L.REPOS)
        days = sorted({c.adate.date().isoformat() for c in s2})
        all_29 = days == ["2026-07-29"]
        print(f"    OBSERVED: "
              + ", ".join(f"{lab}={len(per2[lab])}" for lab, _ in L.REPOS)
              + f"   {'HIT' if per_repo_ok else '*** MISS ***'}")
        print("  P2 also said those successors were `all authored on 2026-07-29, two days")
        print("    before the row was filed`.")
        print(f"    OBSERVED: {len(s2)} successor(s) across {len(days)} distinct author "
              f"date(s): {', '.join(days)}")
        print(f"    P2 sub-clause: {'HIT' if all_29 else '*** MISS ***'}"
              + ("" if all_29 else
                 "  -- the `all` is false; 954c29e (mg-6a2f) is 2026-07-30."))
        if not all_29:
            print("    The sub-clause is NOT rewritten to match.  P2's headline (REFUTED in")
            print("    both repos) stands and its detail does not, and a prediction that is")
            print("    two-thirds right is recorded as two-thirds right.")
    print()
    print("  P5 said: 2 of 4 correct / 2 of 4 refuted on a population of 4, and the")
    print("    brief's `1-of-1 refuted on a population of 4` SUPERSEDED to 4-of-4")
    print("    checked, 2 refuted.")
    if unk:
        print(f"    OBSERVED: UNKNOWN -- {unk} of {n_rows} rows unreadable, so `refuted`,")
        print("    `upheld` and the supersession are all unmeasured.   *** UNMEASURED ***")
        print("    A prediction is not refuted by a run that did not happen.")
    else:
        p5 = (ref == 2 and up == 2 and unk == 0)
        print(f"    OBSERVED: {ref} refuted, {up} upheld, {unk} unknown, n={n_rows}.   "
              f"{'HIT' if p5 else '*** MISS ***'}")
    print()
    hits = n_rows - len(misses) - len(unscored)
    if len(unscored) == n_rows:
        # ⚠️ NOT `0 of 4 hit, 0 missed`.  Both zeros would be true of the
        # tally and false as a report: a run that read no repo has no hit
        # rate, and printing one in the shape of a result is the defect this
        # file was repaired for.
        print(f"  Predictions scored: NONE -- all {n_rows} rows UNMEASURED "
              f"({', '.join(map(str, unscored))}).")
        print("  A run that could not read a repo has no hit rate to report.")
    elif unscored:
        print(f"  Predictions scored: {hits} of {n_rows} hit, {len(misses)} missed, "
              f"{len(unscored)} UNMEASURED on row(s) {', '.join(map(str, unscored))}.")
        print("  A prediction whose row could not be read is neither hit nor missed,")
        print("  and is not folded into either total.")
    else:
        print(f"  Predictions scored: {hits} of {n_rows} hit"
              + (f", MISSES on row(s) {', '.join(map(str, misses))}" if misses else ", 0 missed"))
    print("  (P1-P4 were disclosed as not blind; hitting them is a weak claim and is")
    print("   stated as such in PREDICTIONS.md.)")
    print()
    # ⚠️ EXIT.  Findings about the census still do not set it -- 2 of 4 rows
    # wrong exits 0, as run_all.sh documents.  `I could not read a repo` is not
    # a finding about the census, it is this run failing to happen, and it
    # exits 1 for the same reason s0_freshness.py does.
    rc = 1 if unk else 0
    print(f"== s1 exit: {rc} ("
          + ("a repo could not be read, so THIS RUN MEASURED NOTHING; findings "
             "about the census still do not set this exit"
             if unk else
             "findings about the census do not set this instrument's exit")
          + ") ==")
    return rc


if __name__ == "__main__":
    sys.exit(main())
