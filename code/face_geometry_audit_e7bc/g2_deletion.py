"""mg-e7bc G2 -- THE DELETION TEST, APPLIED BY THIS AUDIT, both directions.

mg-d0e2 ran nine mutations against mg-5f9a and reported that seven moved the
artifact and TWO MOVED NOTHING: the `shape` returns and the `parity`
contradiction branch.  mg-04a8 says all nine now bite.  This file does not read
that claim off `out_d4_auditor_rerun.txt`, and it does not import mg-d0e2's
mutation table either: the eleven edits are re-derived in `kerne7bc` from the
current source text of `absorb_trace`, `gate_violations` and `diagonal_moves`.

BOTH DIRECTIONS ARE REPORTED AND NEITHER IS A FAILURE BY ITSELF.  "Deleted and
identical" is a fact about which gate the bytes depend on.  What would be a
defect is an artifact SENTENCE naming a gate as the reason while the bytes do
not move when it goes -- which is mg-1c80's finding and this lineage's subject.

WHICH ROUTE mg-04a8 TOOK ON THE TWO, and the ticket allows exactly two.  It
could INSTRUMENT them, or it could state that no gate decides them WITH THE
REASON -- and writing an explanation for either instead would be a fourth
generation of "a reason it does not have".  Which route was taken is decided
below by measurement, not by reading the commit message: if the branches are
instrumented there are rows in the artifact that FAIL when the branch goes, and
exactly which row fails is printed.

AND TWO MUTATIONS NO TICKET'S LIST NAMES -- THIS AUDIT'S FLOOR-NOT-SCOPE ITEM.
The `shape` gate has TWO `return` statements.  mg-04a8 deletes them TOGETHER,
on the stated ground that "they are one gate, and deleting one of two would
leave the other answering".  That is an assertion about which branch its two
constructed pairs actually reach, and an assertion about an unreached branch is
the exact defect this lineage keeps re-finding one level down.  So each return
is deleted ALONE, and the two are reported separately.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kerne7bc import (BAR, DEL_DIAG_FROM_VIOLATIONS, DEL_DIAGONAL,   # noqa: E402
                      DEL_MAG_FROM_VIOLATIONS, DEL_MAGNITUDE, DEL_PARITY,
                      DEL_SHAPE, DEL_SIGNS_READ, FC, FINDINGS, INVERT_ROUTING,
                      SCORE, SHAPE_1, SHAPE_2, SWAP_ORDER, ART, claim, finding,
                      head, read, run_battery, scored_rows)

# (tag, label, edits, predicted CHANGED, predicted exit, why)
# Every prediction here was written before the corresponding run.
CASES = [
    ("D1", "delete gate 'shape' (BOTH returns)", DEL_SHAPE, True, 1,
     "mg-d0e2 measured BYTE-IDENTICAL/0 here; mg-04a8 added a row whose "
     "constructed pairs reach it, so the row must now fail"),
    ("D2", "delete gate 'diagonal'", DEL_DIAGONAL, True, 0,
     "294 of 297 biting pairs violate both forced gates, so no ANSWER moves -- "
     "but the trace label the artifact prints does"),
    ("D3", "delete gate 'magnitude'", DEL_MAGNITUDE, True, 1,
     "3 pairs in row I4 violate magnitude alone; the union-find-vs-brute-force "
     "instrument row should catch the change"),
    ("D4", "delete gate 'parity' (the contradiction branch)", DEL_PARITY, True,
     1, "mg-d0e2 measured BYTE-IDENTICAL/0 here; the new constructed pair is "
     "built to be rejected AT that branch"),
    ("D5", "stop counting signs_read", DEL_SIGNS_READ, True, 0,
     "the sign count is what the section's sentences now rest on, so it must "
     "be load-bearing on the bytes"),
    ("D6", "swap the two forced gates' order", SWAP_ORDER, True, 0,
     "same answers, different trace -- the artifact says the split depends on "
     "the order, so it must move when the order does"),
    ("D7", "delete 'diagonal' from gate_violations", DEL_DIAG_FROM_VIOLATIONS,
     True, 0, "the 'both forced gates violated' counts are printed"),
    ("D8", "delete 'magnitude' from gate_violations", DEL_MAG_FROM_VIOLATIONS,
     True, 0, "same from the other side, and row I4's 'the ONLY one violated' "
     "sentence is computed there"),
    ("D9", "invert diagonal_moves (the routing)", INVERT_ROUTING, True, 1,
     "the routing row scores the split, so inverting it must break a row"),
    ("E1*", "MINE: delete ONLY the FIRST `shape` return (m != len(B))",
     SHAPE_1, False, 0,
     "the 2x2-against-3x3 pair falls through to the SECOND return, which "
     "answers False at gate 'shape' just the same -- so nothing moves"),
    ("E2*", "MINE: delete ONLY the SECOND `shape` return (ragged rows)",
     SHAPE_2, True, 1,
     "the RAGGED pair has len(A) == len(B), so the first return never sees it; "
     "with the second gone it should reach the parity system and be ACCEPTED, "
     "against a brute force that rejects it"),
]

WERE_INVISIBLE = ("D1", "D4")


def labels(text):
    return [m for m, _ in scored_rows(text)]


def main():
    print(BAR)
    print("mg-e7bc G2 -- the deletion test, run by this audit, on this tree")
    print(BAR)
    print("\nPREDICTIONS, registered before the runs:")
    print("   %-5s %-58s %-16s %s" % ("tag", "mutation", "artifact", "exit"))
    for tag, label, _e, pc, pe, _w in CASES:
        print("   %-5s %-58s %-16s %d"
              % (tag, label[:58], "CHANGES" if pc else "BYTE-IDENTICAL", pe))
    print("\n   (*) E1 and E2 are this audit's own and no list in the ticket "
          "names them.")

    head("BASELINE")
    base, base_code = run_battery({}, "base")
    committed = read(ART).encode()
    claim(base == committed and base_code == 0,
          "controls.py regenerates its committed artifact byte for byte and "
          "exits 0 -- %d bytes" % len(base),
          "any edit to controls.py, face_complex.py or posets.py that is not "
          "followed by regenerating controls_output.txt.  Without this line "
          "every 'CHANGED' below could be a stale committed file rather than a "
          "mutation",
          "%d regenerated, %d committed, exit %d"
          % (len(base), len(committed), base_code))
    base_labels = labels(base.decode())
    print("  baseline row labels: %d rows -- %d PASS, %d CANNOT FAIL, %d FAIL"
          % (len(base_labels), base_labels.count("[PASS]"),
             base_labels.count("[CANNOT FAIL]"), base_labels.count("[FAIL]")))

    head("THE DELETION TEST -- BOTH DIRECTIONS, one line per mutation")
    print("   %-5s %-58s %7s %16s %5s %s"
          % ("tag", "mutation", "bytes", "verdict", "exit", "vs prediction"))
    results, misses = {}, []
    for tag, label, edits, pc, pe, _why in CASES:
        out, code = run_battery({FC: edits}, tag)
        changed = out != base
        ok = (changed == pc) and (code == pe)
        results[tag] = (out, code, changed)
        if not ok:
            misses.append((tag, label, changed, code, pc, pe))
        print("   %-5s %-58s %7d %16s %5d %s"
              % (tag, label[:58], len(out),
                 "CHANGED" if changed else "BYTE-IDENTICAL", code,
                 "MATCH" if ok else "*** MISS ***"))

    print("\nPREDICTION SCORE -- %d of %d matched.  Misses, kept as written:"
          % (len(CASES) - len(misses), len(CASES)))
    for tag, label, ch, code, pc, pe in misses:
        print("   MISS %-5s %-50s observed %s/exit %d, predicted %s/exit %d"
              % (tag, label[:50], "changed" if ch else "identical", code,
                 "changed" if pc else "identical", pe))
    if not misses:
        print("   none")

    head("PER GATE, BOTH DIRECTIONS -- deleted-and-changed, deleted-and-identical")
    changed_tags = [t for t, _l, _e, _pc, _pe, _w in CASES
                    if results[t][2] and not t.endswith("*")]
    identical_tags = [t for t, _l, _e, _pc, _pe, _w in CASES
                      if not results[t][2] and not t.endswith("*")]
    print("  DELETED AND CHANGED   (%d of the 9 mg-d0e2 ran): %s"
          % (len(changed_tags), ", ".join(changed_tags)))
    print("  DELETED AND IDENTICAL (%d of the 9): %s"
          % (len(identical_tags), ", ".join(identical_tags) or "none"))
    claim(len(changed_tags) == 9,
          "THE DELETION TEST BITES ON %d OF THE 9 mg-d0e2 RAN, measured by "
          "this audit's own mutations against a baseline it generated itself.  "
          "mg-d0e2 measured 7 of 9 against mg-5f9a" % len(changed_tags),
          "either constructed-pair row leaving controls.py, or its expected "
          "value being taken from `absorb_trace` instead of from "
          "`absorbable_bruteforce` -- G3 makes the second change and reports "
          "what happens to D1 and D4",
          "identical on: %s" % (", ".join(identical_tags) or "none"))

    head("THE TWO THAT MOVED NOTHING -- INSTRUMENTED, OR EXPLAINED?")
    print("The ticket allows two routes and forbids a third.  Instrumenting the")
    print("branch means a scored row FAILS when it is deleted; writing an")
    print("explanation instead means the artifact gains a sentence and no row")
    print("moves.  Which happened is read off the rows, not off the commit.\n")
    for tag in WERE_INVISIBLE:
        out, code, changed = results[tag]
        rows = scored_rows(out.decode())
        failing = [n for m, n in rows if m == "[FAIL]"]
        label = [c[1] for c in CASES if c[0] == tag][0]
        claim(changed and code == 1 and len(failing) == 1,
              "%s (%s) -- which left the artifact BYTE-IDENTICAL under mg-d0e2 "
              "-- now CHANGES it (%d -> %d bytes), exits %d, and EXACTLY ONE "
              "row fails: %r"
              % (tag, label, len(base), len(out), code,
                 (failing[0][:72] if failing else "NONE")),
              "the constructed pair for that branch no longer reaching it.  "
              "The route taken was INSTRUMENTATION -- a row that fails -- and "
              "not an explanation: an explanation would leave the row count "
              "and every label where they are, and this deletion moves one",
              "%d row(s) fail; %d rows scored" % (len(failing), len(rows)))
        finding(not (changed and code == 1),
                "%s is still invisible to the deletion test" % tag)

    art = read(ART)
    for gate in ("shape", "parity"):
        sent = "the predicate's `%s` branch" % gate
        n = sum(1 for _m, name in scored_rows(art) if sent in name)
        claim(n == 1,
              "and the artifact carries exactly %d SCORED ROW for the `%s` "
              "branch -- it is a row, not a paragraph" % (n, gate),
              "the row being demoted to a `measured, not scored` bullet, which "
              "is where this repository puts sentences it does not want scored "
              "-- and which would make the branch invisible again while "
              "leaving the artifact looking fuller")

    head("FLOOR, NOT SCOPE -- THE `shape` GATE HAS TWO RETURNS AND ONE IS COVERED")
    print("mg-04a8 deletes both together and says in `d2_deletion.py`: \"Both")
    print("returns of the shape gate go together: they are one gate, and")
    print("deleting one of two would leave the other answering.\"  That is an")
    print("assertion about which return the constructed pairs reach.  Here it")
    print("is measured by deleting each alone.\n")
    e1_out, e1_code, e1_changed = results["E1*"]
    e2_out, e2_code, e2_changed = results["E2*"]
    print("   FIRST  return  `if m != len(B)`            -> %s, exit %d"
          % ("CHANGED" if e1_changed else "BYTE-IDENTICAL", e1_code))
    print("   SECOND return  `if len(A[i]) != len(B[i])` -> %s, exit %d"
          % ("CHANGED" if e2_changed else "BYTE-IDENTICAL", e2_code))
    claim(e2_changed and e2_code == 1,
          "the SECOND `shape` return is covered: deleting it alone changes the "
          "artifact and exits %d" % e2_code,
          "the ragged constructed pair being dropped or made non-ragged -- it "
          "is the only input in the whole battery whose rows are of unequal "
          "length")
    finding(not e1_changed,
            "THE FIRST `shape` RETURN IS STILL INVISIBLE.  Deleting `if m != "
            "len(B): return Trace(False, \"shape\", 0)` ALONE leaves the "
            "artifact BYTE-IDENTICAL at %d bytes, every row green, exit %d -- "
            "which is exactly the state mg-d0e2 found the whole `shape` gate "
            "in.  Cause, measured: the pair built for it is 2x2 against 3x3, "
            "and with the first return gone it falls into the loop where "
            "len(A[0]) = 2 != 3 = len(B[0]) fires the SECOND return, returning "
            "False at gate 'shape' identically.  So the row's clause 'the 2 "
            "built to be REJECTED return at the `shape` gate on 2 of 2' is "
            "satisfied by ONE of the two returns doing all the work.  mg-04a8 "
            "ASSERTED this bundling was safe (\"deleting one of two would leave "
            "the other answering\") and that sentence is true -- but it is the "
            "reason the branch is uncovered, not a reason it need not be: a "
            "pair with len(A) != len(B) and NO ragged row (e.g. 2x2 against "
            "3x3 with B square) would separate them"
            % (len(e1_out), e1_code))

    print("\n" + BAR)
    print("%d claim(s) scored; %d BROKEN.  %d FINDING(s)."
          % (len(SCORE), SCORE.count(False), len(FINDINGS)))
    for f in FINDINGS:
        print("  FINDING: %s" % f)
    print(BAR)
    return 1 if not all(SCORE) else 0


if __name__ == "__main__":
    sys.exit(main())
