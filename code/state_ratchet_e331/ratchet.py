#!/usr/bin/env python3
"""mg-e331 — THE RATCHET.  This is the thing that ASKS whether STATE.md grew, at the landing.

WHAT WAS WRONG.  Twice, a real piece of work cut this file down and nothing held the result:

    mg-34bf  2026-07-30   192,898 ->  164,577 B    78% of the cut undone in   8.5 hours
    mg-ea0e  2026-08-06   186,710 ->   32,772 B    59% of the cut undone in  95.3 hours

Both cuts were correct and both were measured. The second one landed against a stated target
of under 6,000 words, achieved 4,658, and STATE.md grew back the SAME DAY. A restructure with
no mechanism holding its target is a one-off cleanup wearing the language of a fix: the work
is spent, the arc records a success, and the file is back within days.

AND THE COST IS NOT ONLY THE FILE.  mg-9bc2 was authorised to DELETE STATE.md's rendered HTML
twin on the premise that "STATE.md is now 4,658 words and readable, which was the entire
problem the HTML may have been solving". That premise was false when it was written — the
file was 16,861 words by then — and mg-9bc2 caught it at the last moment. A regression nobody
measures does not merely undo the fix; it silently invalidates later decisions reasoned from
it. That is what a report nobody reads cannot prevent and what a blocking gate can.

WHAT THIS IS, PRECISELY.  A comparison of STATE.md's word count against ONE DECLARED NUMBER
in CEILING.json, which carries the reason it is what it is. RED IS EITHER DIRECTION, which is
mg-724a's rule and not a new one:

    ABOVE-CEILING      the file grew past the declared ceiling — the regression itself.
    SLACK-UNRATCHETED  the file is materially BELOW the ceiling and the ceiling was left
                       where it was. This is the half that makes it a RATCHET and not a cap.
                       A cut that is not banked is mg-34bf and mg-ea0e again, and this is the
                       instrument saying so at the landing that should have banked it.

WHAT IT DOES ON RED: it exits 1, `code/state_ratchet_e331/run_all.sh` propagates that, and
`./build.sh` at the repository root — which the refinery runs as this repository's quality
gate — fails the merge request. The branch does not land. It BLOCKS; it does not notify.
mg-be37's finding was that a detector firing into a log with no addressee is
indistinguishable from one that never fired, and a blocked merge cannot be.

IT IS ITSELF A CONTROL and fires its own falsification on every run (§3), including the
guard that matters most here: a probe expecting ABOVE is UNFALSIFIABLE, never CAUGHT, if the
real file is already above — otherwise this ratchet would report itself healthy on precisely
the day it stopped working.

EXITS: 0 within the band · 1 the ratchet fired · 2 REFUSED, or a hole in its own controls.
DECISION LINE: `RATCHET VERDICT: ...`, printable only by reaching the end of the reasoning.
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_e331 as L                     # noqa: E402
import negative_control_e331 as NC       # noqa: E402


def main():
    t0 = time.time()
    print("=" * 92)
    print("mg-e331 — STATE.md SIZE RATCHET")
    print("=" * 92)
    print()

    # ---- §1 -------------------------------------------------------------------------------
    print("§1  THE SUBJECT, MEASURED — the WORKING TREE, not a commit")
    print("-" * 92)
    try:
        text = L.read_state()
        m = L.measure(text)
        raw = open(L.CEILING_PATH, encoding="utf-8").read()
        ceiling = L.parse_ceiling(raw, L.CEILING_PATH)
    except L.Refusal as exc:
        print()
        print("REFUSED while reading the subject or the declared ceiling:")
        for line in str(exc).splitlines():
            print("  " + line)
        print()
        print("RATCHET VERDICT: REFUSED — this ratchet did not reach a decision, so nothing")
        print("above is evidence about the branch.  A control that maps 'could not tell' onto")
        print("'nothing wrong' is the defect this line of work exists to remove.")
        return 2
    print("  path              %s" % os.path.relpath(L.STATE, L.ROOT))
    print("  words             %d      <- THE GATED QUANTITY (len(text.split()))" % m["words"])
    print("  bytes             %d" % m["bytes"])
    print("  lines             %d" % m["lines"])
    print("  longest line      %d chars" % m["max_line_chars"])
    print("  lines over 2000   %d" % m["lines_over_2000"])
    print()
    print("  The gated quantity is WORDS because mg-ea0e's target was in words.  It is a")
    print("  PROXY for what a reader must read and not the thing itself: a future editor who")
    print("  reformats a table can move it without changing the reading burden.  The other")
    print("  five numbers are RECORDED here so that a regression is diagnosable and not")
    print("  merely detected — the longest line and the over-2000 count are what turned out")
    print("  to distinguish this file's two growth mechanisms (out_p1_growth.txt §1.4).")
    print()

    # ---- §2 -------------------------------------------------------------------------------
    print("§2  THE DECLARED CEILING")
    print("-" * 92)
    print("  file              %s" % os.path.relpath(L.CEILING_PATH, L.ROOT))
    print("  words_ceiling     %d" % ceiling["words_ceiling"])
    print("  tighten_below     %d" % ceiling["tighten_below"])
    print("  set_by            %s   at %d words" % (ceiling["set_by"], ceiling["set_at_words"]))
    print("  observed          %d  (%+d against the ceiling)"
          % (m["words"], m["words"] - ceiling["words_ceiling"]))
    print()
    for line in _wrap(ceiling["why"], 86):
        print("  " + line)
    print()

    # ---- §3 -------------------------------------------------------------------------------
    print("§3  CAN THIS RATCHET FAIL, AND CAN IT REFUSE?  Probes against THIS run's values")
    print("-" * 92)
    tp = time.time()
    probes = NC.run(m["words"], ceiling, raw)
    tp = time.time() - tp
    width = max(len(p[1]) for p in probes)
    for pid, what, status, detail in probes:
        print("  %-4s %-*s  %-14s  %s" % (pid, width, what, status, detail[:44]))
    caught, holes, unfals, expl, bounds = NC.summarise(probes)
    print()
    print("  %d of %d probes CAUGHT; %d BOUNDARY (a transition, checked but NOT counted as a"
          % (caught, len(probes), bounds))
    print("  falsification); %d explained-unfalsifiable; %d hole(s)/setup failure(s); %d"
          % (expl, holes, unfals))
    print("  UNEXPLAINED unfalsifiable.  %.3fs." % tp)
    print()

    status, detail = L.verdict(m["words"], ceiling)

    # ---- decision --------------------------------------------------------------------------
    print("=" * 92)
    # An explained-unfalsifiable probe is a FACT ABOUT THE SUBJECT, not a hole — see D4 in
    # negative_control_e331.py, which is the worst defect this ticket produced and the one the
    # positive control existed to find.  The explanation is only ever available when the
    # subject is itself RED, so the guard below is what stops it from being an escape hatch:
    # on a GREEN tree, nothing explains a falsification probe that could not fail.
    if holes or unfals or (expl and status == L.GREEN):
        print("RATCHET VERDICT: BROKEN — %d hole(s) or unexplained unfalsifiable probe(s) in"
              % (holes + unfals + (expl if status == L.GREEN else 0)))
        print("this ratchet's own falsification.  It is not evidence about the branch, and it")
        print("is NOT a green one.")
        if expl and status == L.GREEN:
            print()
            print("  AND THE SPECIFIC FAILURE IS THE DANGEROUS ONE: %d probe(s) could not fail"
                  % expl)
            print("  while the subject reads GREEN.  Nothing explains that.  A probe satisfied")
            print("  by a green input is a probe that will still be satisfied on the day the")
            print("  input stops being green.")
        print("=" * 92)
        return 2

    if status != L.GREEN:
        print("RATCHET VERDICT: RED — %s: %s" % (status, detail))
        print("=" * 92)
        print()
        print(L.REMEDY)
        print("THE ONE-LINE DIFF, WRITTEN OUT so nobody has to work it out from the message:")
        print()
        print('    "words_ceiling": %d,        (was %d)'
              % (m["words"], ceiling["words_ceiling"]))
        print('    "tighten_below": %d,        (was %d)'
              % (max(m["words"] - 500, 0), ceiling["tighten_below"]))
        print('    "set_at_words": %d,         (was %d)'
              % (m["words"], ceiling["set_at_words"]))
        print()
        print("...in code/state_ratchet_e331/CEILING.json, IN THIS COMMIT, with a sentence")
        print("appended to `why` saying what moved and why it could not live in")
        print("docs/state-history/.  Copying those three numbers without writing the sentence")
        print("is available and is the whole failure mode this instrument has: see E1 in")
        print("PREDICTIONS.md, filed before any of this was built.")
        return 1

    print("RATCHET VERDICT: GREEN — %s." % detail)
    print("This ratchet was shown able to fire in both directions and to refuse in %d worlds,"
          % sum(1 for p in probes if p[0] in ("N7", "N8", "N9", "N10", "N11", "N12", "N14")))
    print("on this run, against these values.  %.2fs total." % (time.time() - t0))
    print("=" * 92)
    return 0


def _wrap(text, width):
    words, line, out = text.split(), "", []
    for w in words:
        if len(line) + len(w) + 1 > width:
            out.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    if line:
        out.append(line)
    return out


if __name__ == "__main__":
    sys.exit(main())
