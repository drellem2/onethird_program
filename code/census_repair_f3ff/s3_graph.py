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
"""
import os
import sys

import lib_f3ff as L


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

    p8_gain, p9_rows, p10_rows = {}, {}, []
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
            continue

        direct = (L.successors(fm[L.REPOS[0][0]], parent, T) or []) + \
                 (L.successors(fm[L.REPOS[1][0]], parent, T) or [])
        direct_sha = {c.sha for c in direct}
        extra = [(lab, c) for lab, c in before if c.sha not in direct_sha]
        p8_gain[n] = len(extra)
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
        p9_rows[n] = only_after
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
        if strong:
            p10_rows.append(n)
        print()

    print("=" * 78)
    print("SCORING s3 AGAINST PREDICTIONS.md (72e36cb)")
    print("=" * 78)
    g1 = p8_gain.get(1, 0)
    print(f"  P8  predicted: the ticket graph finds >= 1 successor commit on ROW 1")
    print(f"      that the direct parent-id grep does not.   OBSERVED: {g1}")
    print(f"      P8: {'HIT' if g1 >= 1 else '*** MISS ***'}")
    print(f"      (per-row graph-only gain: "
          + ", ".join(f"row {k}={v}" for k, v in sorted(p8_gain.items())) + ")")
    print()
    hit9 = p9_rows.get(3) and p9_rows.get(4)
    print("  P9  predicted: on rows 3 and 4 the graph names successor TICKETS whose")
    print("      commits are ALL authored after the filing instant, so those rows are")
    print("      upheld on commits and a ticket-only census would report them refuted.")
    print(f"      OBSERVED: row 3 {'yes' if p9_rows.get(3) else 'no'}, "
          f"row 4 {'yes' if p9_rows.get(4) else 'no'}")
    print(f"      P9: {'HIT' if hit9 else '*** MISS or PARTIAL ***'}")
    print()
    print("  P10 predicted: at least one row was already refuted BY THE POLECAT SENT TO")
    print("      WORK IT, in that polecat's own commit message, before mg-f3ff existed --")
    print("      row 1 is known to be, and a SECOND was predicted.")
    print(f"      OBSERVED (STRONG rule -- the polecat's own commit names a successor")
    print(f"      the tree independently found): rows {p10_rows or 'none'}")
    print(f"      P10: {'HIT' if len(p10_rows) >= 2 else '*** MISS ***'}"
          f"  -- {len(p10_rows)} row(s), predicted >= 2 (row 1 known, a second predicted)")
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
    print("== s3 exit: 0 (findings do not set this instrument's exit) ==")
    return 0


if __name__ == "__main__":
    sys.exit(main())
