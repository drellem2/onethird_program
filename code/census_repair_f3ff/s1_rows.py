"""mg-f3ff s1 -- THE FOUR ROWS, RE-DERIVED FROM THE TREE.

For each row: every successor commit at or before the filing instant, in BOTH
repos, under BOTH clocks, with the chain's generation depth; then the row's
verdict scored against what PREDICTIONS.md (72e36cb, committed before this file
existed) predicted for it.

⚠️ A prediction is never edited because the result disagreed with it.  A
refuted prediction is a RESULT.  This script prints MISS in that case and the
number of misses is part of the deliverable, not a defect of it.
"""
import sys

import lib_f3ff as L


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

    verdicts, misses, lines = {}, [], []
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
        gen_counts[n] = (0 if not gens else len(gens),
                         0 if not gens else sum(len(g) for g in gens),
                         0 if not loose else len(loose),
                         0 if not loose else sum(len(g) for g in loose))

        pred = L.PREDICTED[n]
        got = verdicts[n]
        ok = pred == got
        if not ok:
            misses.append(n)
        print()
        print(f"  PREDICTED (72e36cb, before any script existed): {pred}"
              f"    OBSERVED: {got}    {'HIT' if ok else '*** MISS ***'}")
        print(f"  (P{n} was disclosed as NOT BLIND: a hand grep had already shown this.)")
        print()
        g = gen_counts.get(n, (0, 0, 0, 0))
        lines.append((n, row, parent, got, pred, ok, g[0], g[1], g[2], g[3]))

    print("=" * 78)
    print("THE CENSUS'S ACCURACY, WITH THE DENOMINATOR NAMED")
    print("=" * 78)
    print("  Population: the FOUR DROPPED VERDICT tickets pm-onethird filed between")
    print("  2026-07-31T04:12:41Z and 04:22:50Z.  Not a sample of a larger set -- the")
    print("  whole census.  n = 4, and all 4 are now checked against the tree.")
    print()
    print("  row  ticket    parent    premise `no successor` is   strict gens/commits"
          "   loose gens/commits   predicted")
    for n, row, parent, got, pred, ok, g, c, lg, lc in lines:
        print(f"   {n}   {row}   {parent}   {got:<24}   {g:>6} / {c:<9}"
              f"   {lg:>5} / {lc:<8}   {pred}{'' if ok else '  <-- MISS'}")
    ref = sum(1 for x in lines if x[3] == "REFUTED")
    up = sum(1 for x in lines if x[3] == "UPHELD")
    unk = sum(1 for x in lines if x[3] == "UNKNOWN")
    print()
    print(f"  REFUTED {ref} of 4.  UPHELD {up} of 4.  UNKNOWN {unk} of 4.")
    print(f"  The census was WRONG on {ref} of its 4 rows and RIGHT on {up}.")
    print()
    print("  The brief's own figure was `1-of-1 refuted so far on a population of 4`,")
    print("  with 3 rows unchecked.  That figure is now SUPERSEDED, not contradicted:")
    print(f"  4 of 4 checked, {ref} refuted.  `{ref} of 4 wrong` and `4 of 4 wrong` are")
    print("  different claims and this does not round toward either.")
    print()
    print(f"  Predictions scored: {4 - len(misses)} of 4 hit"
          + (f", MISSES on row(s) {', '.join(map(str, misses))}" if misses else ", 0 missed"))
    print("  (P1-P4 were disclosed as not blind; hitting them is a weak claim and is")
    print("   stated as such in PREDICTIONS.md.)")
    print()
    print("== s1 exit: 0 (findings about the census do not set this instrument's exit) ==")
    return 0


if __name__ == "__main__":
    sys.exit(main())
