"""mg-f3ff s4 -- THE CHAIN READER MEASURED AGAINST AN INDEPENDENT LIST.

s1 reports row 1's chain as 3 generations / 10 commits (strict) and 7 / 81
(loose).  Neither number has been checked against anything outside this
instrument, and a bracket both of whose ends I chose is not a measurement.

There IS an independent enumeration: mg-e35b's own polecat, working before
mg-f3ff existed, listed the row-1 chain BY SHA in its commit message (5f542f0).
That list was produced by a different agent, from a different brief, with no
knowledge of this instrument.  This section:

  1. EXTRACTS the shas from 5f542f0's message rather than transcribing them --
     a hand-typed ground truth is a ground truth I could have typed to agree
     with my own output.  The hand list from the mg-f3ff ticket body is ALSO
     recorded, and any disagreement between the two is printed rather than
     resolved silently.
  2. Scores strict and loose against it: what each finds, what each misses,
     what each adds.

EXIT: 1 if this instrument cannot read 5f542f0, OR if the chain it scores could
not be measured.  A low score is a FINDING about my chain reader and does not
set it.

⚠️ THE GUARD WAS ONE REPO NARROWER THAN THE THING IT GUARDED (mg-7085).  It
checked `fm[REPOS[0]].unknown` and returned 1 -- but `generations()` returns
None if ANY repo of the list is unknown.  So under a PARTIAL fetch failure --
repo 1 readable, repo 2 not, which is the commonest arm of all and the one a
half-broken network produces -- this file walked past its own guard, printed a
ground truth, and then died at the scoring loop on

    TypeError: 'NoneType' object is not iterable

which is `len(None)` in a new costume: the same refusal to treat None as a list,
caught by `for gen in gens` instead of by `len`.  FOUND BY RUNNING THE MIXED ARM,
not by reading the guard -- reading it is exactly what makes it look sufficient.

⚠️ AND THE MIXED ARM WAS UNMEASURED BY EVERY PRIOR TICKET.  s4 is one of the
three scripts mg-407f recorded as never run in any arm.  It was not known-good;
it was unmeasured, and this is what was under it.
"""
import re
import sys

import lib_f3ff as L

VERDICT_COMMIT = "5f542f0"
ROW1_PARENT = "mg-fcf1"
ROW1_INSTANT = "2026-07-31T04:13:24Z"

# Transcribed BY HAND from the mg-f3ff ticket body's quotation of mg-e35b's
# verdict.  Kept only to be CHECKED against the extraction below; it is never
# the source of a number in this section.
HAND = ["8fc5111", "f024985", "de54c3a", "1d922a1", "5cae82c",
        "c7f9673", "b6bc2ef", "0fb0e00", "bfd7948"]
HAND_TICKETS = ["mg-8a12", "mg-da45", "mg-a806"]

SHA_RE = re.compile(r"\b([0-9a-f]{7,40})\b")


def main():
    L.banner("mg-f3ff s4 -- the chain reader vs mg-e35b's own independent list")
    fm = L.fetch_all()
    L.print_freshness(fm)
    repo = fm[L.REPOS[0][0]]
    if repo.unknown:
        print("  UNKNOWN: onethird_program could not be read.  This section is")
        print("  UNKNOWN, not empty.")
        print("== s4 exit: 1 ==")
        return 1
    # ⚠️ THE SECOND GUARD, WHICH IS THE ONE THAT WAS MISSING.  The extraction
    # below needs only repo 1; the SCORING needs `generations()`, which ranges
    # over EVERY repo of the list and returns None if any is unknown.  The two
    # have different populations and now have different guards, so the mixed arm
    # is measured rather than walked past.
    chain_unreadable = [lab for lab, f in fm.items() if f.unknown]

    cs = L.git_log(repo.path, VERDICT_COMMIT, extra=["-1"])
    if not cs:
        print(f"  UNKNOWN: {VERDICT_COMMIT} could not be read.")
        print("== s4 exit: 1 ==")
        return 1
    v = cs[0]
    print(f"  independent list source: {v.sha[:9]}  {v.adate.isoformat()}")
    print(f"    {v.subject[:150]}")
    print()

    # -- 1. extract, and check the extraction against the hand list ---------
    found = []
    for m in SHA_RE.finditer(v.body):
        s = m.group(1)
        r = L._run(["git", "-C", repo.path, "rev-parse", "--verify", "-q",
                    f"{s}^{{commit}}"])
        if r.returncode == 0:
            full = r.stdout.strip()
            if full != v.sha and full not in found:
                found.append(full)
    print(f"  EXTRACTED from the message body: {len(found)} resolvable commit sha(s)")
    for f in found:
        c = L.git_log(repo.path, f, extra=["-1"])[0]
        print(f"    {f[:9]}  {c.adate.isoformat()}  owner={c.owner or '(none)'}")

    print()
    short = {f[:7] for f in found}
    missing_from_extract = [h for h in HAND if h not in short]
    extra_in_extract = [f[:7] for f in found if f[:7] not in HAND]
    print("  CROSS-CHECK of the extraction against the hand transcription:")
    print(f"    hand list: {len(HAND)} sha(s); extraction: {len(found)}")
    print(f"    in the hand list but NOT extracted: {missing_from_extract or 'none'}")
    print(f"    extracted but NOT in the hand list: {extra_in_extract or 'none'}")
    if missing_from_extract or extra_in_extract:
        print("    ⚠️ THE TWO DISAGREE.  Printed, not reconciled.  The EXTRACTION is")
        print("       what s4 scores against, because it is read from the tree; the")
        print("       hand list is kept so the disagreement is visible.")
    else:
        print("    The two agree exactly.")
    print()

    # -- 2. score strict and loose against the extracted list --------------
    T = L.utc(ROW1_INSTANT)
    truth = set(found)
    # mg-e35b also names mg-a806 by TICKET, not by sha.  Add its pre-instant
    # commits, so the ground truth is the list as the verdict meant it.
    for tid in HAND_TICKETS:
        for c in L.git_log(repo.path, repo.ref, grep=tid):
            if c.owner == tid and c.adate and c.adate <= T:
                truth.add(c.sha)
    print(f"  GROUND TRUTH: {len(truth)} commit(s) -- the extracted shas plus the")
    print(f"  pre-instant commits of the tickets the verdict names by id "
          f"({', '.join(HAND_TICKETS)}).")
    print()

    for mode in ("strict", "loose"):
        gens = L.generations(fm, ROW1_PARENT, T, mode=mode)
        if gens is None:
            # ⚠️ THIS IS THE CRASH SITE.  It was `mine = {... for gen in gens ...}`
            # with no branch, and `gens` is None whenever ANY repo is unknown.
            # The count is not defended with an `or []` -- it is NOT TAKEN.
            print(f"  {mode.upper()} chain: UNMEASURED -- the chain reader ranges over")
            print(f"    EVERY repo of the list and {', '.join(chain_unreadable)} could")
            print("    not be read.  NO hit / miss / added count is printed at all.")
            print(f"    A reader that read nothing misses the whole ground truth, and")
            print(f"    that figure -- which would be the worst score this section can")
            print("    print -- is a fact about the fetch and not about the reader.")
            print()
            continue
        mine = {c.sha for gen in gens for _lab, c, _via in gen}
        hit = truth & mine
        missed = truth - mine
        added = mine - truth
        print(f"  {mode.upper()} chain: {len(gens)} generation(s), {len(mine)} commit(s)")
        print(f"    of the {len(truth)} ground-truth commits it finds {len(hit)}, "
              f"MISSES {len(missed)}")
        for s in sorted(missed):
            c = L.git_log(repo.path, s, extra=["-1"])[0]
            print(f"      MISSED  {s[:9]}  owner={c.owner or '(none)'}  "
                  f"{c.subject[:100]}")
        print(f"    and adds {len(added)} commit(s) the verdict did not name")
        for s in sorted(added)[:6]:
            c = L.git_log(repo.path, s, extra=["-1"])[0]
            print(f"      ADDED   {s[:9]}  owner={c.owner or '(none)'}  "
                  f"{c.subject[:100]}")
        if len(added) > 6:
            print(f"      ... and {len(added) - 6} more")
        print()

    print("-" * 78)
    print("WHAT THIS SAYS ABOUT THE CHAIN READER -- AND IT IS NOT FLATTERING")
    print("-" * 78)
    # ⚠️ RULE 2.  Every sentence below asserts a measured comparison between the
    # two modes and the independent list.  On the mixed arm neither mode ran, so
    # the paragraph is branched rather than printed as a standing finding.
    if chain_unreadable:
        print("  UNMEASURED THIS RUN.  Both modes returned UNKNOWN, so there is no")
        print("  bracket to report and the finding below is NOT restated as though")
        print("  this run had reproduced it.  It stands on the runs that took it --")
        print(f"  see out_s4_crosscheck.txt -- and not on this one.")
        print()
        print("== s4 exit: 1 (the chain could not be measured; a low score would be")
        print("   a finding about this reader, but no score was taken) ==")
        return 1
    print("  The two modes bracket the independent list from OPPOSITE SIDES and")
    print("  NEITHER contains it.  The strict reader misses real successor commits")
    print("  because this arc's convention does not put the ancestor's ticket id in")
    print("  the subject of every descendant; the loose reader contains them but")
    print("  buries them among citations.  So `3 generations` and `7 generations`")
    print("  are both wrong as a count of the chain, and s1's headline for row 1")
    print("  should be read as a BRACKET and not as either endpoint.")
    print()
    print("  ⚠️ THIS DOES NOT MOVE ANY ROW VERDICT.  REFUTED/UPHELD is decided by")
    print("     the generation-1 successor count, which is a direct grep of the")
    print("     parent id and does not use the chain descent at all.  The defect is")
    print("     in the DEPTH figure, not in the census answer.  Saying so is not a")
    print("     defence of the depth figure; it is the scope of the damage, stated.")
    print()
    print("  This is blind spot B3 (`a successor whose message names neither P nor")
    print("  any ticket that descends from P`) biting on the population, found by")
    print("  cross-checking against a list this instrument did not produce.  It is")
    print("  recorded as the second defect of this instrument, after s3's weak-rule")
    print("  false positive.")
    print()
    print("== s4 exit: 0 (a low score is a finding about this reader, not a crash) ==")
    return 0


if __name__ == "__main__":
    sys.exit(main())
