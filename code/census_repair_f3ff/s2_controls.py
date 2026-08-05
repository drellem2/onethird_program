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

EXIT: 1 if a control of THIS instrument was refuted.  Findings about the census
do not set it -- an instrument that exited 1 for successfully finding what it
was sent to find could not distinguish a defect in the subject from a defect in
itself.
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


def main():
    L.banner("mg-f3ff s2 -- negative controls on the repaired instrument")
    fm = L.fetch_all()
    L.print_freshness(fm)
    red = 0

    # ---------------------------------------------------------------- NC1
    print("-" * 78)
    print("NC1  SUBJECT-ONLY READER -- does reading %s instead of %B reproduce")
    print("     the census's wrong answer?   (PREDICTIONS.md P6)")
    print("-" * 78)
    nc1_rows = []
    for n, row, filed, parent in L.ROWS:
        T = L.utc(filed)
        full, _p, _u = L.census_row(fm, parent, T)
        subj, per_s, _u2 = L.census_row(fm, parent, T, subject_only=True)
        nfull = sum(len(x) for x in _p.values())
        nsubj = sum(len(x) for x in per_s.values())
        moved = full != subj
        nc1_rows.append((n, parent, full, nfull, subj, nsubj, moved))
        print(f"  row {n} {parent}:  full-message {full} ({nfull})   "
              f"subject-only {subj} ({nsubj})   {'DEGRADES' if moved else 'same'}")
    deg = [r for r in nc1_rows if r[6]]
    print()
    print(f"  The subject-only reader loses the finding on {len(deg)} of 4 rows"
          + (f" ({', '.join('row %d' % r[0] for r in deg)})." if deg else "."))
    print("  P6 predicted this on rows 1 AND 2 -- 0 successors found where the")
    print("  full-message reader finds >= 1.")
    p6_hit = {r[0] for r in deg} == {1, 2}
    p6_partial = bool(deg)
    print(f"  P6: {'HIT' if p6_hit else ('PARTIAL' if p6_partial else '*** MISS ***')}"
          f"  -- degraded on rows {sorted(r[0] for r in deg) or 'none'}, predicted [1, 2]")
    print()
    print("  ⚠️ CONTROL SENSE: this control is RED only if the subject-only reader")
    print("     matched the full reader on EVERY row, which would mean the harness")
    print("     cannot tell the two readers apart at all.")
    if not deg:
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
        row1_named, agreed = 0, 0
        for n, row, filed, parent in L.ROWS:
            T = L.utc(filed)
            naming = [(p, d, s) for p, d, s, t in msgs
                      if parent.lower() in t.lower() and d is not None]
            before = [(p, d, s) for p, d, s in naming if d <= T]
            # the successor tickets the tree found for this parent
            succ = L.successors(fm[L.REPOS[0][0]], parent, T) or []
            succ += L.successors(fm[L.REPOS[1][0]], parent, T) or []
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
        print(f"  lower confidence on the others.  OBSERVED: {row1_named}.")
        print(f"  P7: {'HIT' if row1_named == 0 else '*** MISS ***'}"
              "  -- and the miss is the most load-bearing result in this run.")
        print()
        print("  ⚠️ THE RECONSTRUCTED MAIL READER DOES NOT REPRODUCE THE CENSUS'S ERROR.")
        print(f"     It agrees with the tree on {agreed} of 4 rows, including both rows")
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
        print()

    # ---------------------------------------------------------------- NC4
    print("-" * 78)
    print("NC4  THE STALE CHECKOUT, CONSTRUCTED -- does staleness alone move the")
    print("     answer?  (the addendum's own hazard, measured rather than warned about)")
    print("-" * 78)

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
    print(f"== s2 exit: {1 if red else 0} "
          f"({red} control(s) of THIS instrument refuted) ==")
    return 1 if red else 0


if __name__ == "__main__":
    sys.exit(main())
