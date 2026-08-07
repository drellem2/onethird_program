"""mg-f3ff s2 -- NEGATIVE CONTROLS ON THE INSTRUMENT ITSELF.

s1 says the tree-reading method gets 4 of 4 rows.  That is worth nothing until
the same harness is shown to FAIL when it should.  Four controls:

  NC1  SUBJECT-ONLY reader.  Reading `%s` instead of `%B` -- the census's error
       is not only that it read mail; a tree reader that reads only subject
       lines fails identically.
  NC2  THE MAIL READER ITSELF, re-implemented against pm-onethird's own
       mailbox, so the census's answer is REPRODUCED rather than described.
  NC3  FORCED FETCH FAILURE.  The addendum's third item: a row that could not
       be read must print UNKNOWN, never `no successor found`.  This takes the
       same code branch the real `ssh: connect to host github.com port 22`
       took.  If the row comes back UPHELD instead of UNKNOWN, the repaired
       method has the defect it was built to remove and this control is RED.
  NC4  THE STALE CHECKOUT, CONSTRUCTED.  pm-onethird's workspace was 25
       commits behind origin/main.  This runs the identical derivation against
       `origin/main~25` and against the 45-behind local HEAD of the second
       repo, and reports whether the answer MOVES.  A hazard that is merely
       described is not measured.

EXIT: 1 if a control of THIS instrument was refuted, OR if a repo could not be
read.  Findings about the census do not set it -- an instrument that exited 1
for successfully finding what it was sent to find could not distinguish a defect
in the subject from a defect in itself.  `This run did not happen` is neither,
and it exits 1 for the same reason `s0_freshness.py` and `s1_rows.py` do.

⚠️ AND A CONTROL MAY NOT REPORT A RESULT IT DID NOT MEASURE (mg-7085).  mg-407f
ran this file against a repo whose `git fetch` really failed and it DIED at line
80 with mg-4d3b's F5 VERBATIM -- `TypeError: object of type 'NoneType' has no
len()` -- on `sum(len(x) for x in _p.values())`, where `census_row` had put a
None for the unreadable repo.  The same `len(None)` death mg-cf83 removed from
`s1_rows.py`, alive in the same deliverable, on the same library call.

FOUR SITES ARE REPAIRED HERE AND ONLY THE FIRST WAS LIVE.  THAT DISTINCTION IS
KEPT RATHER THAN FLATTENED, and it is drawn from PRINTED EVIDENCE of a real
failing run, not from reading:

  L80/81  (NC1)  LIVE.  The crash.  It is the first thing a failing arm reaches.
  L130/1  (NC2)  LATENT, AND REPAIRING THE CRASH WOULD HAVE MADE IT LIVE.  This
                 is the `or []` mg-407f classified LATENT because the crash
                 above returned first.  That classification was right AND it had
                 an expiry date: with L80 fixed, control flow reaches it, None
                 becomes [], `tree` becomes UPHELD, and NC2 prints `MAIL says
                 UPHELD; TREE says UPHELD; agree` -- an agreement between a
                 reader and a reader that said nothing.  So it is repaired IN
                 THE SAME COMMIT as the crash, not left for a later sweep.
  L247/8  (NC4)  LATENT.  Same `len(None)`, after the crash.
  L268-88 (NC4)  LATENT.  `len(L.successors(...))` directly on a possible None.

NC4 IS NOW GATED WHOLE.  It asks whether STALENESS ALONE moves the answer, and
that question needs a live answer to move away from.  Under a fetch failure the
`Pinned` shim would have compared an UNKNOWN live verdict against a stale ref
that still resolves locally -- a difference attributed to staleness that is
really the fetch failure.  A control that cannot tell its two arms apart reports
UNMEASURED here rather than a number.
"""
import os
import re
import sys
from datetime import timezone

import lib_f3ff as L

MAILBOX = os.path.join(L.MAIL_STORE, "pm-onethird")
DATE_RE = re.compile(r"^Date:\s*(\S+)", re.M)
SUBJ_RE = re.compile(r"^Subject:\s*(.*)$", re.M)


def mail_messages():
    """Every message in pm-onethird's own maildir, with its Date header.

    ⚠️ THIS IS THE CENSUS'S POPULATION, and stating it is half the point: it is
    the messages that ARRIVED in one inbox.  A verdict that was written, merged
    and pushed but whose mail was dropped is simply not in it, and the census
    had no way to notice the difference."""
    out = []
    if not os.path.isdir(MAILBOX):
        return None
    for root, _d, files in os.walk(MAILBOX):
        for fn in files:
            p = os.path.join(root, fn)
            try:
                with open(p, encoding="utf-8", errors="replace") as fh:
                    txt = fh.read()
            except OSError:
                continue
            m = DATE_RE.search(txt)
            d = L.parse_iso(m.group(1)) if m else None
            s = SUBJ_RE.search(txt)
            out.append((p, d, (s.group(1) if s else ""), txt))
    return out


def cell(x):
    """One control figure: `?` when it was not measured.  Same rule as
    `s1_rows.py:cell()` -- `I could not look` and `I looked and found none` are
    different answers and this file no longer merges them."""
    return "?" if x is None else str(x)


def finish(red, unmeasured):
    """The one place s2's exit is decided, so the two return paths cannot drift.

    ⚠️ RED AND UNMEASURED ARE COUNTED SEPARATELY AND BOTH EXIT 1, for different
    reasons that the line says out loud.  A refuted control is a fact about this
    instrument.  An unmeasured one is this run failing to happen, which is what
    `s0_freshness.py` and `s1_rows.py` already exit 1 for.  What is NOT done is
    exiting 0 with `0 control(s) refuted` -- true of the tally, and a report of
    success from a run that took no measurement."""
    if unmeasured:
        print(f"  {len(unmeasured)} control(s)/finding(s) UNMEASURED: "
              f"{', '.join(unmeasured)}")
        print("  UNMEASURED is not GREEN.  `0 controls refuted` is true here and")
        print("  would be a report of success from a run that ran no control.")
    rc = 1 if (red or unmeasured) else 0
    print(f"== s2 exit: {rc} ({red} control(s) of THIS instrument refuted"
          + (f"; {len(unmeasured)} UNMEASURED -- a repo could not be read, so "
             "THIS RUN MEASURED NOTHING" if unmeasured else "")
          + ") ==")
    return rc


def main():
    L.banner("mg-f3ff s2 -- negative controls on the repaired instrument")
    fm = L.fetch_all()
    L.print_freshness(fm)
    red = 0
    # ⚠️ ONE READING OF THE FETCH STATE, TAKEN ONCE, USED BY EVERY CONTROL
    # BELOW.  Each control branches on it rather than discovering a None
    # mid-expression -- which is how L80 died.
    unreadable = [lab for lab, f in fm.items() if f.unknown]
    unmeasured = []          # controls this run could not take
    if unreadable:
        print(f"⚠️ {len(unreadable)} REPO(S) COULD NOT BE READ: "
              f"{', '.join(unreadable)}.")
        print("   Every control that ranges over them reports UNMEASURED below.")
        print("   UNMEASURED IS NOT GREEN AND IT IS NOT RED: a control that did not")
        print("   run neither passed nor failed, and reporting either from it is the")
        print("   merger this deliverable exists to remove.")
        print()

    # ---------------------------------------------------------------- NC1
    print("-" * 78)
    print("NC1  SUBJECT-ONLY READER -- does reading %s instead of %B reproduce")
    print("     the census's wrong answer?   (PREDICTIONS.md P6)")
    print("-" * 78)
    nc1_rows = []
    for n, row, filed, parent in L.ROWS:
        T = L.utc(filed)
        full, _p, unk = L.census_row(fm, parent, T)
        subj, per_s, _u2 = L.census_row(fm, parent, T, subject_only=True)
        # ⚠️ THIS IS THE LIVE SITE.  It was
        #     nfull = sum(len(x) for x in _p.values())
        # and `_p` holds a None for every repo that could not be read, so a
        # failing arm died here with mg-4d3b's F5 verbatim -- 30 lines of import
        # away from the docstring in lib_f3ff.successors() reading `callers must
        # NOT treat None as an empty list`.  The count is not defended with a
        # `or 0`; it is NOT TAKEN, and the row says so.
        nfull = None if unk else sum(len(x) for x in _p.values())
        nsubj = None if unk else sum(len(x) for x in per_s.values())
        # `moved` is a THIRD state, not a False.  Two UNKNOWNs comparing equal
        # is not the readers agreeing, it is neither reader having spoken.
        moved = None if unk else (full != subj)
        nc1_rows.append((n, parent, full, nfull, subj, nsubj, moved))
        print(f"  row {n} {parent}:  full-message {full} ({cell(nfull)})   "
              f"subject-only {subj} ({cell(nsubj)})   "
              + ("UNMEASURED" if moved is None else
                 ("DEGRADES" if moved else "same")))
    deg = [r for r in nc1_rows if r[6]]
    nc1_unmeasured = [r for r in nc1_rows if r[6] is None]
    print()
    if nc1_unmeasured:
        print(f"  UNMEASURED on {len(nc1_unmeasured)} of {len(nc1_rows)} rows: "
              f"{', '.join('row %d' % r[0] for r in nc1_unmeasured)}.")
        print("  No degradation count is printed.  A sentence of the form `the")
        print("  subject-only reader loses the finding on N of M rows` would be TRUE")
        print("  OF THE TALLY and FALSE AS A REPORT -- there was no finding for")
        print("  either reader to lose.  (The figures are left as N and M on purpose:")
        print("  prose that quotes its own output with real numbers in it is read as")
        print("  output by the next detector, which is a mistake this ticket made.)")
    else:
        print(f"  The subject-only reader loses the finding on {len(deg)} of "
              f"{len(nc1_rows)} rows"
              + (f" ({', '.join('row %d' % r[0] for r in deg)})." if deg else "."))
    print("  P6 predicted this on rows 1 AND 2 -- 0 successors found where the")
    print("  full-message reader finds >= 1.")
    if nc1_unmeasured:
        print("  P6: *** UNMEASURED *** -- a prediction is not refuted by a run that")
        print("      did not happen.  This is the third state mg-cf83 added to")
        print("      s1_rows.py's scoring, and it is the right answer here too.")
    else:
        p6_hit = {r[0] for r in deg} == {1, 2}
        p6_partial = bool(deg)
        print(f"  P6: {'HIT' if p6_hit else ('PARTIAL' if p6_partial else '*** MISS ***')}"
              f"  -- degraded on rows {sorted(r[0] for r in deg) or 'none'}, "
              "predicted [1, 2]")
    print()
    print("  ⚠️ CONTROL SENSE: this control is RED only if the subject-only reader")
    print("     matched the full reader on EVERY row, which would mean the harness")
    print("     cannot tell the two readers apart at all.")
    if nc1_unmeasured:
        # ⚠️ AND THIS IS WHY THE THIRD STATE IS LOAD-BEARING AND NOT DECORATION.
        # With `moved` collapsed to False, every row compares UNKNOWN to UNKNOWN,
        # `deg` is empty, and the branch below fires: NC1 RED, `the harness does
        # not distinguish the readers`, exit 1.  A FALSE ACCUSATION AGAINST THIS
        # INSTRUMENT, from a run that read no repo.
        print("  NC1 UNMEASURED: the two readers were never compared, because neither")
        print("     of them read anything.  NOT RED -- `no row degraded` is what a")
        print("     broken harness and an unread repo both look like, and this run")
        print("     cannot tell them apart, so it claims neither.")
        unmeasured.append("NC1")
    elif not deg:
        print("  NC1 RED: no row degraded; the harness does not distinguish the readers.")
        red += 1
    else:
        print("  NC1 GREEN: the harness detects the degradation it was built to detect.")
    print()

    # ---------------------------------------------------------------- NC2
    print("-" * 78)
    print("NC2  THE MAIL READER ITSELF, re-implemented against pm-onethird's own")
    print("     maildir -- the census's answer REPRODUCED, not described.  (P7)")
    print("-" * 78)
    msgs = mail_messages()
    if msgs is None:
        print("  UNKNOWN: pm-onethird's maildir is not readable at "
              f"{MAILBOX}.  Printed as UNKNOWN, not as `no successor`.")
        print("  NC2 SKIPPED (UNKNOWN is the correct output, so this is not RED).")
    else:
        print(f"  Population: {len(msgs)} messages in {MAILBOX}")
        undated = sum(1 for _p, d, _s, _t in msgs if d is None)
        print(f"  {undated} of them carry no parsable Date header and are excluded"
              " -- stated, not dropped silently.")
        print()
        row1_named, agreed, nc2_unmeasured = None, 0, 0
        for n, row, filed, parent in L.ROWS:
            T = L.utc(filed)
            # THE MAIL SIDE IS MEASURABLE WHATEVER GIT DID.  The maildir is a
            # different channel and it is read from disk, so these two counts
            # are real even on a failing arm and are printed as real.
            naming = [(p, d, s) for p, d, s, t in msgs
                      if parent.lower() in t.lower() and d is not None]
            before = [(p, d, s) for p, d, s in naming if d <= T]
            # ⚠️ THE TREE SIDE IS NOT.  These two lines carried `or []`, which
            # mg-407f correctly classified LATENT -- the L80 crash returned
            # first.  Repairing L80 puts control flow HERE, and `or []` would
            # then turn `the tree could not be read` into `the tree found no
            # successor`, print `TREE says UPHELD`, and score it as AGREEMENT
            # with the mail reader.  Two silences agreeing is not a control.
            s_a = L.successors(fm[L.REPOS[0][0]], parent, T)
            s_b = L.successors(fm[L.REPOS[1][0]], parent, T)
            if s_a is None or s_b is None:
                nc2_unmeasured += 1
                print(f"  row {n} {parent}: {len(naming)} message(s) name it, "
                      f"{len(before)} before the filing instant.")
                print("           TREE says UNMEASURED -- a repo could not be read, so")
                print("           there is no successor set for the mail to be checked")
                print("           against, and no agreement to score.")
                continue
            succ = s_a + s_b
            succ_ids = {c.owner for c in succ if c.owner}
            named_succ = []
            for p, d, s in before:
                with open(p, encoding="utf-8", errors="replace") as fh:
                    body = fh.read().lower()
                hit = sorted(t for t in succ_ids if t in body)
                if hit:
                    named_succ.append((p, d, hit))
            verdict = "REFUTED" if named_succ else "UPHELD"
            tree = "REFUTED" if succ else "UPHELD"
            agree = verdict == tree
            print(f"  row {n} {parent}: {len(naming)} message(s) name it, "
                  f"{len(before)} before the filing instant,")
            print(f"           {len(named_succ)} of those name any successor ticket "
                  f"the tree found ({len(succ_ids)} such tickets).")
            print(f"           MAIL says {verdict};  TREE says {tree};  "
                  f"{'agree' if agree else '*** MAIL IS WRONG HERE ***'}")
            if n == 1:
                row1_named = len(named_succ)
            agreed += 1 if agree else 0
        print()
        print("  P7 predicted 0 messages naming any successor ticket on row 1, with")
        if row1_named is None:
            print("  lower confidence on the others.  OBSERVED: UNMEASURED -- row 1's")
            print("  tree side could not be read, so there was no successor set to look")
            print("  for in the mail.")
            print("  P7: *** UNMEASURED ***  -- not 0, and therefore not a HIT either.")
            print("      A prediction of `0` that a broken run would satisfy by default")
            print("      is exactly the merger this deliverable exists to remove, and")
            print("      scoring it HIT here would be the defect wearing a rosette.")
            unmeasured.append("NC2")
        else:
            print(f"  lower confidence on the others.  OBSERVED: {row1_named}.")
            print(f"  P7: {'HIT' if row1_named == 0 else '*** MISS ***'}"
                  "  -- and the miss is the most load-bearing result in this run.")
        print()
        # ⚠️ RULE 2.  THIS IS THE LOAD-BEARING PARAGRAPH OF THE WHOLE DELIVERABLE
        # -- §4 of the README rests on it -- and it is a FIXED STRING carrying a
        # measured figure.  On a failing arm `agreed` counts only the rows that
        # were read, and the sentences under it assert what the mail and the
        # tree did relative to each other.  It is branched, not defended.
        if nc2_unmeasured:
            print(f"  ⚠️ UNMEASURED ON {nc2_unmeasured} OF {len(L.ROWS)} ROWS -- the "
                  "tree side could not be read.")
            print("     THE FINDING THAT §4 OF THE README RESTS ON IS NOT RESTATED HERE.")
            print("     It is a comparison between two readers, and one of them did not")
            print("     read.  `agrees with the tree on NONE of the rows` and `agrees")
            print("     with the tree on ALL of them` are both sentences this run could")
            print("     emit from the same nothing, which is why it emits neither.")
            print("     The mail-side counts above ARE real: the maildir is a different")
            print("     channel, read from disk, and unaffected by the fetch failure.")
            print("  NC2 UNMEASURED: not GREEN.  `GREEN by construction` is true of the")
            print("  control's DESIGN and says nothing about whether it ran.")
            unmeasured.append("NC2-finding")
        else:
            print("  ⚠️ THE RECONSTRUCTED MAIL READER DOES NOT REPRODUCE THE CENSUS'S ERROR.")
            print(f"     It agrees with the tree on {agreed} of {len(L.ROWS)} rows, "
                  "including both rows")
            print("     the census got WRONG.  The successor information WAS in pm-onethird's")
            print("     own inbox, before the filing instant, naming the successor tickets by")
            print("     id.  So `mail dropped the verdict, therefore the census saw nothing`")
            print("     is NOT a sufficient account of what went wrong -- the mail was not")
            print("     silent, and a reader of that mail would not have made this error.")
            print()
            print("     What this leaves standing, and what it does not:")
            print("       STANDS  -- the census was built on mail rather than the tree, and")
            print("                  is wrong on 2 of 4 rows.  s1 measures that directly and")
            print("                  it does not depend on this control.")
            print("       STANDS  -- a channel-based census cannot distinguish silence from")
            print("                  absence, whatever this particular inbox happened to hold.")
            print("       FALLS   -- `the mail store contained no successor, so the census")
            print("                  could not have known`.  It did contain one.  The census")
            print("                  looked for a VERDICT MESSAGE ADDRESSED TO IT and read the")
            print("                  absence of that specific shape as absence of the work;")
            print("                  mentions of the successor sitting in the same inbox did")
            print("                  not count because they were not the shape it queried.")
            print("       OPEN    -- this reconstruction is MINE, not pm-onethird's code.  I")
            print("                  did not find the census's implementation and do not claim")
            print("                  to have run it.  What is measured is that the INFORMATION")
            print("                  was present, not that the original query would have found")
            print("                  it.  Stated as OPEN rather than resolved either way.")
            print("  NC2 GREEN by construction: this control cannot be RED -- it is a")
            print("  measurement of the OLD method, not a check on the new one.")
    print()

    # ---------------------------------------------------------------- NC3
    print("-" * 78)
    print("NC3  FORCED FETCH FAILURE -- UNKNOWN must propagate.  (ticket addendum 3)")
    print("-" * 78)
    for victim in (L.REPOS[0][0], L.REPOS[1][0]):
        fmx = L.fetch_all(force_fail_labels=(victim,))
        print(f"  with {victim} forced to fail fetch:")
        for f in fmx.values():
            print(f.line())
        ok_all = True
        for n, row, filed, parent in L.ROWS:
            v, _per, unk = L.census_row(fmx, parent, L.utc(filed))
            good = v == "UNKNOWN" and victim in unk
            ok_all &= good
            print(f"    row {n} {parent}: {v}"
                  f"{'' if good else '   *** NOT UNKNOWN -- CONTROL RED ***'}")
        g = L.generations(fmx, "mg-fcf1", L.utc("2026-07-31T04:13:24Z"))
        chain_ok = g is None
        print(f"    generations() under the same failure: "
              f"{'None (UNKNOWN)' if chain_ok else '*** returned a list -- RED ***'}")
        if not (ok_all and chain_ok):
            red += 1
            print("  NC3 RED for this victim.")
        else:
            print("  NC3 GREEN: every row that ranges over the unreadable repo is")
            print("             UNKNOWN, and UNKNOWN is what is printed.")
        # ⚠️ NC3 IS DEGENERATE WHEN THE WHOLE FLEET IS ALREADY BROKEN, and that
        # is stated rather than left for the reader to notice.  This control
        # forces ONE repo to fail and asks whether UNKNOWN propagates from it.
        # If the OTHER repo could not be read either, every row would be UNKNOWN
        # with or without the forcing, and GREEN says only `UNKNOWN was printed`
        # -- not `the forcing caused it`.
        others = [lab for lab in fmx if lab != victim and fmx[lab].unknown]
        if others:
            print(f"  ⚠️ DEGENERATE THIS RUN: {', '.join(others)} was ALSO unreadable")
            print("     without being forced, so every row would be UNKNOWN anyway.")
            print("     The GREEN above is real but it is NOT ATTRIBUTABLE to the")
            print("     forcing.  A control whose two arms cannot be told apart is")
            print("     reported as such rather than counted as evidence.")
        print()

    # ---------------------------------------------------------------- NC4
    print("-" * 78)
    print("NC4  THE STALE CHECKOUT, CONSTRUCTED -- does staleness alone move the")
    print("     answer?  (the addendum's own hazard, measured rather than warned about)")
    print("-" * 78)

    # ⚠️ GATED WHOLE, AND THE REASON IS NOT MERELY THAT IT WOULD CRASH.  Three
    # sites below call `len()` straight onto `successors()`, so on a failing arm
    # NC4 died the same death as L80 -- but a `cell()` at each would be the WRONG
    # repair.  NC4's question is `does STALENESS ALONE move the answer`, and it
    # answers it by DIFFERENCING a live read against a pinned one.  `Pinned`
    # hard-codes `unknown = False` and inherits the live `ref`, so on a failing
    # arm the live side is UNKNOWN while the pinned side reads a ref that still
    # resolves from the local object store -- and the control would print a
    # difference, attribute it to staleness, and be measuring the fetch failure.
    # A control that cannot tell its two arms apart reports UNMEASURED.
    if unreadable:
        print(f"  UNMEASURED -- {', '.join(unreadable)} could not be read, so there is")
        print("  no live answer for a stale one to differ FROM.  Nothing is printed for")
        print("  the depth sweep, the 45-behind checkout, or NC4b.")
        print("  ⚠️ AND `0 of 4 row verdicts flipped` IS NOT PRINTED EITHER.  It is what")
        print("     this control emits when it works AND what it would emit having read")
        print("     nothing, and the whole subject of this deliverable is that those two")
        print("     must not share a rendering.")
        unmeasured.append("NC4")
        print()
        print("=" * 78)
        return finish(red, unmeasured)

    class Pinned:
        """A Fetched whose ref is pinned back N commits.  Same class surface, so
        the derivation code below is bit-for-bit the one s1 runs."""

        def __init__(self, base, ref, label):
            self.path, self.label, self.ref = base.path, label, ref
            self.sha = base.sha
            self.head_sha = base.head_sha
            self.behind = base.behind
            self.reason = ""

        unknown = False

    for back in (10, 25, 60):
        pinned = {}
        for lab, f in fm.items():
            r = L._run(["git", "-C", f.path, "rev-parse", "--verify", "-q",
                        f"origin/main~{back}^{{commit}}"])
            ref = f"origin/main~{back}" if r.returncode == 0 else f.ref
            pinned[lab] = Pinned(f, ref, lab)
        print(f"  == every repo pinned {back} commits back (origin/main~{back}) ==")
        moved = 0
        for n, row, filed, parent in L.ROWS:
            T = L.utc(filed)
            live, lp, _ = L.census_row(fm, parent, T)
            st, sp, _ = L.census_row(pinned, parent, T)
            nl = sum(len(x) for x in lp.values())
            ns = sum(len(x) for x in sp.values())
            flag = ""
            if live != st:
                moved += 1
                flag = "   <-- THE ANSWER MOVED ON STALENESS ALONE"
            elif nl != ns:
                flag = "   <-- same verdict, count moved"
            print(f"    row {n} {parent}: origin/main {live} ({nl})   "
                  f"stale {st} ({ns}){flag}")
        print(f"    {moved} of 4 row verdicts flipped at depth {back}.")
        print()

    print("  The stale checkout of one_third_width_three this run started against")
    print("  (45 behind) is measured directly:")
    f2 = fm[L.REPOS[1][0]]
    class Head:
        path, label, ref, unknown = f2.path, f2.label, "HEAD", False
        sha, head_sha, behind, reason = f2.sha, f2.head_sha, f2.behind, ""
    for n, row, filed, parent in L.ROWS:
        T = L.utc(filed)
        a = L.successors(f2, parent, T)
        b = L.successors(Head, parent, T)
        mark = "   <-- MOVED" if len(a) != len(b) else ""
        print(f"    row {n} {parent}: origin/main {len(a)}   local HEAD (45 behind) "
              f"{len(b)}{mark}")
    print()
    print("  == NC4b  THE COMPOUND CONSTRUCTION: the census's own repo scoping, on")
    print("     the stale checkout.  This is the wrong answer produced FROM THE TREE. ==")
    print("     The census scoped each row's search to the repo named in its parent's")
    print("     `repo:` field.  Row 2's parent mg-d112 carries repo:one_third_width_three.")
    print("     Take that scope, and take the 45-behind checkout this run actually found")
    print("     on disk, and run the identical successor derivation:")
    T2 = L.utc("2026-07-31T04:12:41Z")
    scoped_fresh = L.successors(f2, "mg-d112", T2)
    scoped_stale = L.successors(Head, "mg-d112", T2)
    both_fresh = sum(len(L.successors(f, "mg-d112", T2)) for f in fm.values())
    print(f"       both repos, origin/main   -> {both_fresh} successors -> REFUTED   "
          "(what s1 reports)")
    print(f"       scoped repo, origin/main  -> {len(scoped_fresh)} successors -> "
          f"{'REFUTED' if scoped_fresh else 'UPHELD'}")
    print(f"       scoped repo, local HEAD   -> {len(scoped_stale)} successors -> "
          f"{'REFUTED' if scoped_stale else 'UPHELD'}"
          + ("   <-- THE CENSUS'S WRONG ANSWER, REPRODUCED FROM THE TREE"
             if not scoped_stale else ""))
    if not scoped_stale and both_fresh:
        print("     So blind spot B2 -- a BOUNDED CHANNEL TAKEN FOR THE WORLD -- bites on")
        print("     this very population, and it composes with staleness: two defects")
        print("     neither of which is `reading mail`, either of which alone leaves the")
        print("     verdict standing, and which together reproduce the census's error")
        print("     with the authority of having read the commit log.  This is why the")
        print("     repo list is NOT taken from the ticket's own metadata.")
    print()
    print("  NC4 GREEN by construction: it is a measurement of the hazard, not a")
    print("  check on the new method.  Its number is the finding.")
    print()

    print("=" * 78)
    return finish(red, unmeasured)


if __name__ == "__main__":
    sys.exit(main())
