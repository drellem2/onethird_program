"""mg-f3ff s3 -- THE TICKET-REFERENCE GRAPH, and what the four polecats were
actually sent to do.

Three questions the brief asks that s1 does not answer:

  (a) `and for any ticket whose body names it` -- does descending through the
      WORK STORE buy coverage a direct grep of the parent id in commit
      messages does not?  (PREDICTIONS.md P8)
  (b) on the two UPHELD rows, do successor TICKETS exist whose COMMITS all
      postdate the filing instant -- i.e. is it the commit date, not the
      ticket's existence, that makes those rows true?  (P9)
  (c) were the polecats sent to re-land work that already existed, and how
      much of what they did was duplicate?  (brief item 1)

⚠️ THE GRAPH IS A SECOND READER, NOT A REPLACEMENT.  It ranges over the work
store, which is a THIRD channel with its own silence: a ticket deleted from
~/.macguffin/work is invisible to it though its commits remain in the tree
(blind spot B8).  Reported as a union with the tree reader, never instead of it.

⚠️ AND THE SCORING BLOCK MAY NOT DISAGREE WITH THE ROWS (mg-7085).  mg-407f ran
this file against a repo whose `git fetch` really failed.  The row sections were
right -- four of them printed `UNKNOWN -- a repo could not be read.` -- and then,
TWELVE LINES BELOW THE LAST OF THEM, the scoring block printed `OBSERVED: 0` and
scored P8, P9 and P10 as MISS.  P9 and P10 FLIPPED HIT -> MISS with nothing
changed but whether a repo could be read, and the script EXITED 0.  A total fetch
failure was published as a scoreboard.

The spelling was the reason mg-cf83's sweep missed it.  Its ticket said to grep
`0 if not gens`, which finds the site already repaired in `s1_rows.py` AND
NOTHING ELSE.  The live merger here was spelled `p8_gain.get(1, 0)` -- a DICT
DEFAULT on an accumulator the `continue` above never populated, which is the same
None-becomes-zero merger wearing different syntax.  `p9_rows.get(3)` returning
None and rendering as `no` is the same one again.

The three rules mg-cf83 established for `s1_rows.py` now hold here too:

  1  `?` and `0` are different answers.  An unmeasured figure renders as
     UNMEASURED, never as 0 and never as `no`.
  2  No fixed string asserts a count that was not measured.  Every sentence
     carrying a figure has a branch for the figure not existing.
  3  EVERY SCOREBOARD FIGURE IS A FOLD OVER `lines`, which is the row sections'
     own output.  A row that could not be read appends an UNMEASURED entry
     rather than appending nothing, so the scoring block has no independent
     source it can contradict the rows from.

And the exit agrees with `s1_rows.py`: 1 when a repo could not be read, because
`this run did not happen` is not a finding about the census.
"""
import os
import sys

import lib_f3ff as L


def cell(x):
    """One scoreboard figure: `?` when it was not measured.

    ⚠️ The expression this replaces was `p8_gain.get(1, 0)`.  The accumulator is
    never written for a row the loop `continue`d past, so the dict default made
    `I could not look` print as `I looked and found none` -- mg-4d3b's F1 in a
    second spelling, in the deliverable sent to remove it."""
    return "?" if x is None else str(x)


def yesno(v):
    """A yes/no cell that has a third state.

    ⚠️ `no` and `not measured` are different answers.  `p9_rows.get(3)` returning
    None and rendering as `no` is `p8_gain.get(1, 0)` again in boolean clothing:
    a dict default answering for a row nobody read."""
    return "UNMEASURED" if v is None else ("yes" if v else "no")


def score(pred_met, measured):
    """HIT / MISS / UNMEASURED.

    A prediction is scored only against a measurement.  `measured` is False when
    a row the prediction ranges over could not be read; printing MISS then
    asserts an outcome this run did not observe.

    ⚠️ THE ASYMMETRY IS DELIBERATE AND IS NOT A LOOPHOLE.  A threshold already
    met by rows that WERE read is a HIT whatever the unread rows hold -- more
    evidence cannot un-meet a `>=`.  A threshold NOT met is only a MISS if
    everything it ranges over was read.  So HIT survives partial measurement and
    MISS does not, and callers pass `measured` accordingly."""
    if pred_met:
        return "HIT"
    return "MISS" if measured else "UNMEASURED"


def children_of(parent, files):
    """Tickets whose FILE TEXT names `parent`.  Not `tags: [<parent>-followup]`
    -- that convention is followed by some tickets and not others, and a rule
    that depends on a convention measures the convention."""
    out = []
    for tid, path in files.items():
        if tid == parent:
            continue
        if parent.lower() in L.ticket_text(path).lower():
            out.append(tid)
    return sorted(out)


def commits_owned_by(fm, tids, instant):
    """Every commit owned by one of `tids`, split by whether it lands before or
    after `instant`.  The split IS the answer to (b)."""
    before, after = [], []
    if any(f.unknown for f in fm.values()):
        return None, None
    for label, f in fm.items():
        for tid in tids:
            for c in L.git_log(f.path, f.ref, grep=tid):
                if c.owner != tid:
                    continue
                if c.adate is None:
                    continue
                (before if c.adate <= instant else after).append((label, c))
    before.sort(key=lambda t: t[1].adate)
    after.sort(key=lambda t: t[1].adate)
    return before, after


def main():
    L.banner("mg-f3ff s3 -- the ticket-reference graph and the duplicate-work question")
    fm = L.fetch_all()
    L.print_freshness(fm)

    files = L.ticket_files()
    print(f"  work store: {L.WORK_STORE}, {len(files)} ticket file(s) readable.")
    print("  ⚠️ This is a THIRD channel with its own silence (blind spot B8): a")
    print("     deleted ticket is absent here though its commits remain in the tree.")
    print()

    # ⚠️ RULE 3.  `lines` is the row sections' own output and is the ONLY source
    # the scoring block reads.  A row that could not be read appends an
    # UNMEASURED entry rather than appending nothing: the old loop `continue`d
    # without recording anything, and every figure below was then read out of an
    # accumulator that had no key for that row -- which is what made a dict
    # default able to speak for a row nobody measured.
    lines = []
    for n, row, filed, parent in L.ROWS:
        T = L.utc(filed)
        print("-" * 78)
        print(f"ROW {n}: {row} / parent {parent}")
        print("-" * 78)

        kids = children_of(parent, files)
        print(f"  (a) tickets whose body names {parent}: {len(kids)}")
        print(f"      {', '.join(kids) if kids else '(none)'}")

        before, after = commits_owned_by(fm, kids, T)
        if before is None:
            print("      UNKNOWN -- a repo could not be read.")
            print("      This row contributes NO FIGURE to the scoring block below.")
            print("      It is recorded as UNMEASURED, not skipped: a row the loop")
            print("      passes over silently is a row a default value can answer for.")
            print()
            lines.append((n, row, parent, None, None, None))
            continue

        direct = (L.successors(fm[L.REPOS[0][0]], parent, T) +
                  L.successors(fm[L.REPOS[1][0]], parent, T))
        # ⚠️ THE `or []` THAT STOOD ON THESE TWO LINES IS GONE, AND IT WAS NOT
        # THE LIVE DEFECT.  mg-407f classified it LATENT by PRINTED EVIDENCE
        # from a real failing run, not by reading: the `continue` above returns
        # first, so in no arm either of us ran did it ever merge a None into an
        # empty list.  It is removed anyway, because an idiom whose safety rests
        # on a `continue` twelve lines up is one edit from being the live one --
        # and removed rather than guarded, so that if the invariant ever breaks
        # this raises loudly instead of quietly printing a 0.
        direct_sha = {c.sha for c in direct}
        extra = [(lab, c) for lab, c in before if c.sha not in direct_sha]
        print()
        print(f"      commits owned by those tickets, authored <= {filed}: {len(before)}")
        print(f"      of which the direct parent-id grep already had: "
              f"{len(before) - len(extra)}")
        print(f"      NEW, found only via the ticket graph: {len(extra)}")
        for lab, c in extra[:12]:
            print(f"        {c.sha[:9]}  {c.adate.isoformat()}  {lab}  owner={c.owner}")
            print(f"          {c.subject[:140]}")
        if len(extra) > 12:
            print(f"        ... and {len(extra) - 12} more (truncated in this")
            print(f"            transcript; the count above is the full figure, not a cap)")

        print()
        print(f"  (b) commits owned by those tickets authored AFTER {filed}: {len(after)}")
        for lab, c in after[:8]:
            print(f"        {c.sha[:9]}  {c.adate.isoformat()}  {lab}  owner={c.owner}")
            print(f"          {c.subject[:140]}")
        if len(after) > 8:
            print(f"        ... and {len(after) - 8} more")
        only_after = bool(kids) and not before and bool(after)
        if only_after:
            print()
            print(f"      >>> {len(kids)} successor TICKET(S) EXIST for {parent}, and every")
            print(f"          one of their commits is authored AFTER the filing instant.")
            print("          So this row is UPHELD ON COMMITS while a ticket-only census")
            print("          would have reported it REFUTED.  THE COMMIT DATE, NOT THE")
            print("          TICKET'S EXISTENCE, IS WHAT MAKES THIS ROW TRUE.")

        print()
        print(f"  (c) what {row}'s own polecat committed, and whether it was duplicate:")
        own = []
        for lab, f in fm.items():
            for c in L.git_log(f.path, f.ref, grep=row):
                if c.owner == row.lower():
                    own.append((lab, c))
        own.sort(key=lambda t: t[1].adate or t[1].cdate)
        print(f"      {len(own)} commit(s) owned by {row}.")
        pre = len(direct)
        if pre:
            print(f"      {pre} successor commit(s) ALREADY EXISTED when {row} was filed.")
            print(f"      So its polecat was dispatched on a premise the tree already")
            print(f"      contradicted.  Whether its {len(own)} commit(s) DUPLICATE that")
            print("      work is not decidable from commit metadata -- see the verdict")
            print("      note below; this section reports the overlap, not a judgement.")
        else:
            print("      0 successor commits existed at filing: nothing to duplicate.")
        # P10: did the row's own polecat record the correction in its own message?
        #
        # TWO RULES, because the first one I wrote was wrong and the wrong one is
        # kept beside it.  WEAK is a keyword flag; it fires on row 4, where the
        # word `premise` is about the mathematics and there is no census premise
        # to correct at all -- a false positive of my own instrument, on 1 of the
        # 3 rows it flags.  STRONG requires the polecat's own commit to NAME a
        # successor the tree independently found -- a citation cannot be a
        # coincidence of vocabulary.
        marks = ("no successor", "successor", "premise", "landing commit")
        weak = [(lab, c) for lab, c in own
                if any(m in c.body.lower() for m in marks)]
        cited = {t for t in (c.owner for c in direct) if t}
        cited |= {c.sha[:7] for c in direct}
        strong = [(lab, c) for lab, c in own
                  if any(t in c.body.lower() for t in cited)]
        print(f"      WEAK flag (premise vocabulary anywhere): {len(weak)} commit(s)")
        for lab, c in weak[:4]:
            print(f"        {c.sha[:9]}  {c.subject[:140]}")
        print(f"      STRONG flag (names a successor the tree found): "
              f"{len(strong)} commit(s)")
        for lab, c in strong[:4]:
            print(f"        {c.sha[:9]}  {c.subject[:140]}")
            for ln in c.body.splitlines():
                if any(t in ln.lower() for t in cited) or "premise" in ln.lower():
                    print(f"          | {ln.strip()[:130]}")
        print()
        # ⚠️ RULE 3.  The row's OWN figures, recorded where they were printed.
        lines.append((n, row, parent, len(extra), only_after, bool(strong)))

    # ----------------------------------------------------------------------
    # THE SCORING BLOCK.  ⚠️ RULE 3 IS ENFORCED BY WHAT IS IN SCOPE HERE: every
    # figure below is a fold over `lines`, which the row sections above printed.
    # No repo is re-read, no accumulator is indexed with a default, and no
    # sentence carrying a count lacks a branch for the count not existing.
    # ----------------------------------------------------------------------
    p8_gain = {n: g for n, _r, _p, g, _o, _s in lines}
    p9_rows = {n: o for n, _r, _p, _g, o, _s in lines}
    p10_rows = [n for n, _r, _p, _g, _o, s in lines if s]
    unmeasured = [n for n, _r, _p, g, _o, _s in lines if g is None]

    print("=" * 78)
    print("SCORING s3 AGAINST PREDICTIONS.md (72e36cb)")
    print("=" * 78)
    if unmeasured:
        print(f"  ⚠️ THIS RUN DID NOT MEASURE THE GRAPH ON ROW(S) "
              f"{', '.join(map(str, unmeasured))}.  A repo they range over could")
        print("     not be read.  Read no figure below as one for those rows: there")
        print("     is no number under them, and UNMEASURED is printed where the")
        print("     number would go.")
        print()
    g1 = p8_gain.get(1)
    print(f"  P8  predicted: the ticket graph finds >= 1 successor commit on ROW 1")
    print(f"      that the direct parent-id grep does not.   OBSERVED: "
          + ("UNMEASURED -- row 1 could not be read" if g1 is None else str(g1)))
    s8 = score(g1 is not None and g1 >= 1, g1 is not None)
    print(f"      P8: {'HIT' if s8 == 'HIT' else '*** ' + s8 + ' ***'}")
    print(f"      (per-row graph-only gain: "
          + ", ".join(f"row {k}={cell(v)}" for k, v in sorted(p8_gain.items())) + ")")
    if unmeasured:
        print("      `?` above is a row that was NOT READ, not a row whose gain is 0.")
    print()
    m9 = p9_rows.get(3) is not None and p9_rows.get(4) is not None
    print("  P9  predicted: on rows 3 and 4 the graph names successor TICKETS whose")
    print("      commits are ALL authored after the filing instant, so those rows are")
    print("      upheld on commits and a ticket-only census would report them refuted.")
    print(f"      OBSERVED: row 3 {yesno(p9_rows.get(3))}, "
          f"row 4 {yesno(p9_rows.get(4))}")
    s9 = score(m9 and p9_rows.get(3) and p9_rows.get(4), m9)
    print(f"      P9: {'HIT' if s9 == 'HIT' else '*** ' + s9 + ' ***'}")
    print()
    print("  P10 predicted: at least one row was already refuted BY THE POLECAT SENT TO")
    print("      WORK IT, in that polecat's own commit message, before mg-f3ff existed --")
    print("      row 1 is known to be, and a SECOND was predicted.")
    print(f"      OBSERVED (STRONG rule -- the polecat's own commit names a successor")
    print(f"      the tree independently found): rows {p10_rows or 'none'}"
          + (f"   (of {len(lines) - len(unmeasured)} of {len(lines)} rows read)"
             if unmeasured else ""))
    # `>= 2` already met by the rows that WERE read is a HIT whatever the unread
    # rows hold; not met is a MISS only if every row was read.  See score().
    s10 = score(len(p10_rows) >= 2, not unmeasured)
    print(f"      P10: {'HIT' if s10 == 'HIT' else '*** ' + s10 + ' ***'}"
          + (f"  -- {len(p10_rows)} row(s), predicted >= 2 (row 1 known, a second "
             "predicted)" if s10 != "UNMEASURED" else
             f"  -- {len(p10_rows)} row(s) found on the "
             f"{len(lines) - len(unmeasured)} row(s) that were read, and the "
             f"threshold is 2; the unread row(s) could carry the rest, so this is "
             "NOT a miss"))
    # ⚠️ RULE 2.  The paragraph below carries three measured figures -- `fires on
    # row 4`, `0 successor commits`, `1 of the 3 rows it flags`.  It is a FIXED
    # STRING, so under a fetch failure it asserted all three from a run that
    # counted none of them.  It is now branched on whether the rows were read.
    if unmeasured:
        print("      ⚠️ A DEFECT OF THIS SECTION IS RECORDED IN THE README AND IS NOT")
        print("         RESTATED HERE WITH ITS FIGURES: the WEAK keyword rule fires on a")
        print("         row where `premise` is about the mathematics.  WHICH row and on")
        print("         HOW MANY of the rows it flags are counts, and this run did not")
        print("         take them.  Both rules are still printed per row above, for the")
        print("         rows that were read.")
    else:
        print("      ⚠️ A DEFECT OF THIS SECTION, KEPT: the WEAK keyword rule I wrote first")
        print("         fires on row 4, where `premise` is about the mathematics and there")
        print("         are 0 successor commits for it to be about -- a false positive on 1")
        print("         of the 3 rows it flags.  Both rules are printed above; the STRONG")
        print("         one is what P10 is scored on, and the weak one is kept rather than")
        print("         deleted because a discarded rule that was wrong is evidence too.")
    print("      ⚠️ STILL NOT A READING.  The STRONG rule proves a citation, not an")
    print("         intent.  The quoted lines are printed so the reader scores the")
    print("         meaning; s3 claims only that the citation is there.")
    print()
    # ⚠️ EXIT, AND IT NOW AGREES WITH s1_rows.py.  Findings about the census
    # still do not set it -- a graph-only gain of 0 on every row exits 0.  `I
    # could not read a repo` is not a finding about the census, it is this run
    # failing to happen, and it exits 1 for the same reason s0_freshness.py and
    # s1_rows.py do.  Before mg-7085 this line was the fixed string `exit: 0`
    # under every arm, so a total fetch failure reported success.
    rc = 1 if unmeasured else 0
    print(f"== s3 exit: {rc} ("
          + (f"row(s) {', '.join(map(str, unmeasured))} could not be read, so THIS "
             "RUN MEASURED NOTHING ON THEM; findings about the census still do "
             "not set this exit"
             if unmeasured else
             "findings do not set this instrument's exit")
          + ") ==")
    return rc


if __name__ == "__main__":
    sys.exit(main())
