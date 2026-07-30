"""mg-04a8 part 4 -- RUN THE AUDITOR'S OWN DELETION TEST AGAINST THE REPAIR.

mg-d0e2 wrote `code/face_geometry_audit_d0e2/e1_deletion.py` specifically so it
would NOT be the subject's instrument: its nine mutations are re-derived from the
source text of `absorb_trace` rather than imported from `d2_deletion.py`, and its
README says in terms that running the subject's own test learns only that the
test is deterministic.  That file is the strongest available evidence about this
repair, and it costs one subprocess to use it.  So it is run here, unmodified,
and what it says is scored.

WHY IT IS RUN HERE RATHER THAN EDITED THERE.  Its committed transcripts are that
audit's record of its own run against the tree it audited, and this repair does
not rewrite them -- the same treatment mg-5f9a gave mg-1c80's `a6_mutations.py`.
But there is a difference worth stating: `a6_mutations.py` degraded to
`<-- MISSED` and still exited 0, while `e1_deletion.py` EXITS 1 against this
tree.  A script in the repository that exits 1 is a landmine unless somebody has
written down why, so the why is scored below rather than left in a paragraph.

TWO OF ITS PREDICTIONS MISSED AGAINST mg-04a8, AND BOTH MISSES WERE THE REPAIR.
It predicted that deleting the `shape` gate would leave the artifact
byte-identical, because when it was written nothing in the battery had a shape
mismatch; against mg-04a8 it changed the artifact and failed a row.  Its `parity`
prediction was the one MISS it recorded against mg-5f9a -- predicted changed,
observed identical -- and it observed changed.  A prediction that misses because
the code was repaired between its registration and its run is the outcome that
item was asking for.

AND AGAINST THIS TREE IT NO LONGER APPLIES AT ALL (mg-9220), which is scored
below rather than left to be discovered.  Its FIRST mutation deletes the two
`shape` returns TOGETHER, as one anchor of seven lines.  mg-e7bc found that
deleting the first of those two ALONE left the artifact byte-identical -- so the
bundled result was a claim about the PAIR and about neither member -- and
mg-9220 merged them into one condition.  The seven-line anchor no longer occurs,
`kernd0e2.apply_edits` raises, and the script stops before its first battery.
mg-e7bc's own `g2_deletion.py` stops in the same place for the same reason.

BOTH ARE THEREFORE RUN TWICE: against this tree, where each reports `anchor
occurs 0 times` and names the text this commit deleted; and against the PINNED
COMMIT each was written for, materialised whole with `git archive`, where each
still says exactly what its committed transcript says.  Nothing either audit
measured is withdrawn -- it is a statement about the tree it measured, and it is
RE-RUN there rather than quoted.  The alternative, re-anchoring two audits'
mutation tables to this tree's source, was not taken: their committed
transcripts are their record of their own runs, the same treatment mg-5f9a gave
mg-1c80's `a6_mutations.py` and mg-04a8 gave this file's subject.

WHAT THIS COSTS, STATED PLAINLY.  After this commit no INDEPENDENTLY WRITTEN
deletion instrument applies to the live tree; the per-return table in
`d2_deletion.py` is this lineage's own.  That is the price of removing the text
they were anchored to, and it is the price the ticket asked for -- a statement
that does nothing is deleted, not watched.  Re-anchoring either audit would buy
the independence back and is available to whoever wants it.

THIS FILE'S CLAIMS WOULD DIFFER UNDER: either constructed-pair row being removed
from `controls.py`, or its expected value being taken from the predicate instead
of from brute force -- both restore the state where those two deletions moved
nothing.  And under any OTHER claim of that audit going broken against this tree,
which would mean this repair disturbed something the audit had verified.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kern5f9a import BAR, TWO_RETURN_REF, head                      # noqa: E402

SCORE = []

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
AUDIT = os.path.normpath(os.path.join(HERE, "..", "face_geometry_audit_d0e2"))
AUDIT_E7BC = os.path.normpath(os.path.join(HERE, "..",
                                           "face_geometry_audit_e7bc"))

# The commit mg-e7bc audited, and the commit mg-e7bc IS.  Each audit's mutations
# are re-run against the tree it was written for, whole.
E7BC_REF = "9d712be"

# The seven-line anchor mg-d0e2's first mutation carries, and the four-line one
# mg-e7bc's carries.  Both name the two-return `shape` gate mg-9220 merged.  They
# are written here so the claim below is about THIS text and not about "something
# failed to apply".
GONE_ANCHOR = '    if m != len(B):\\n        return Trace(False, "shape", 0)'


def archive(ref):
    """Materialise a whole commit and return its root.  A pinned re-run needs the
    audit's own scripts as well as the tree they mutate: running THIS tree's copy
    of an audit against THAT tree's sources would be a third thing again."""
    tmp = tempfile.mkdtemp(prefix="mg9220-ref-")
    tar = subprocess.run(["git", "archive", ref], cwd=REPO,
                         stdout=subprocess.PIPE)
    if tar.returncode != 0:
        raise SystemExit("cannot archive %s" % ref)
    x = subprocess.run(["tar", "-x", "-C", tmp], input=tar.stdout)
    if x.returncode != 0:
        raise SystemExit("cannot unpack %s" % ref)
    return tmp


def scrub(text):
    """Absolute paths out of anything printed into the transcript.

    A traceback carries the checkout it ran in.  This file's transcript is
    committed and compared byte-for-byte by mg-e7bc's g4, so a path would make
    it reproducible only in the directory it was first run in -- a re-run
    failure that says nothing about the code (mg-a318 found this shape).
    """
    return text.replace(REPO, "<repo>")


def run_script(cwd, script, root=None):
    p = subprocess.run([sys.executable, script], cwd=cwd,
                       capture_output=True, text=True)
    out = scrub(p.stdout + p.stderr)
    if root:
        out = out.replace(root, "<pinned>")
    return out, p.returncode

# The two mg-d0e2 found invisible.  Named here so the claim below is about them
# and not about "nine lines all said CHANGED".
WERE_INVISIBLE = ("delete gate 'shape'", "delete gate 'parity'")

LINE = re.compile(r"^  (delete gate '\w+'|delete '\w+' from gate_violations|"
                  r"stop counting signs_read|swap the two forced gates' order|"
                  r"invert diagonal_moves \(the routing\))\s+"
                  r"bytes\s+(\d+) ->\s+(\d+)\s+(CHANGED|BYTE-IDENTICAL)\s+"
                  r"exit (\d+)", re.M)


def claim(text, ok, differs_under, detail=""):
    SCORE.append(ok)
    print("  [%s] %s" % ("HOLDS " if ok else "BROKEN", text))
    if detail:
        print("        " + detail)
    print("        WOULD DIFFER UNDER: %s" % differs_under)


def main():
    print(BAR)
    print("mg-04a8 part 4 -- mg-d0e2's own deletion test, unmodified")
    print("(mg-9220: run against THIS tree, where it no longer applies, and "
          "against the")
    print(" PINNED commit it was written for, where it still says what it said)")
    print(BAR)

    if not os.path.isdir(AUDIT):
        raise SystemExit("cannot find %s" % AUDIT)
    head("AGAINST THIS TREE -- where the text its first mutation names is gone")
    print("mg-9220 merged `absorb_trace`'s two `shape` returns into one.  This")
    print("audit's first mutation deletes both as a single seven-line anchor,")
    print("which is the granularity mg-e7bc found the result being read below.")
    print("A mutation that cannot be applied is reported as such and not as a")
    print("pass -- `kernd0e2.apply_edits` raises for exactly that reason, and")
    print("the raise is that kernel working.\n")
    out, live_code = run_script(AUDIT, "e1_deletion.py")
    print("--- its transcript, verbatim " + "-" * 48)
    print(out.rstrip())
    print("--- end of its transcript " + "-" * 51)
    print()
    rows = LINE.findall(out)
    claim("it stops at its FIRST mutation with `anchor occurs 0 times`, naming "
          "the two-return `shape` gate this commit merged; %d of its 9 "
          "mutations ran, and it exits %d" % (len(rows), live_code),
          len(rows) == 0 and live_code != 0
          and "anchor occurs 0 times" in out and GONE_ANCHOR in out,
          "the merged condition being split back into two returns, which is the "
          "only thing that would make this anchor apply again.  NOT under this "
          "audit being edited -- it is not, and the pinned re-run below is what "
          "keeps its measurement alive",
          "exit %d; the anchor it names is %s" % (live_code, GONE_ANCHOR))
    claim("and its BASELINE claims ran before it stopped: it regenerated this "
          "tree's artifact byte for byte, so the abort is the mutation and not "
          "the tree",
          "reproduces its committed artifact byte for byte" in out
          and "[BROKEN]" not in out.split("DELETION TEST")[0],
          "this tree's controls_output.txt going stale, which would make the "
          "abort ambiguous between a missing anchor and a broken tree",
          "; ".join(l.strip() for l in out.split("\n")
                    if l.strip().startswith("[OK") or
                    l.strip().startswith("[BROKEN")) or "no baseline lines")

    head("AGAINST THE PINNED COMMIT IT WAS WRITTEN FOR -- nothing is withdrawn")
    print("%s, materialised whole.  This is the run mg-04a8 published, re-run"
          % TWO_RETURN_REF)
    print("rather than quoted: 9 of 9 CHANGED, including the two mg-d0e2 found")
    print("invisible.  It is a statement about THAT tree, and it stays true of")
    print("it whatever this commit does.\n")
    pinned_root = archive(TWO_RETURN_REF)
    pout, pcode = run_script(os.path.join(pinned_root, "code",
                                          "face_geometry_audit_d0e2"),
                             "e1_deletion.py", pinned_root)
    rows = LINE.findall(pout)
    claim("its nine mutations all ran and were parsed at %s -- %d of 9"
          % (TWO_RETURN_REF, len(rows)),
          len(rows) == 9,
          "that audit's transcript format changing, which would make every "
          "claim below silently vacuous rather than wrong",
          "; ".join("%s %s->%s %s exit %s" % (n, a, b, c, d)
                    for n, a, b, c, d in rows))
    changed = [n for n, _a, _b, c, _d in rows if c == "CHANGED"]
    claim("THE DELETION TEST NOW BITES ON %d OF 9 -- at %s, RE-RUN here and not "
          "quoted; against this tree the same script does not apply.  mg-d0e2 "
          "measured 7 of 9 against mg-5f9a" % (len(changed), TWO_RETURN_REF),
          len(changed) == 9,
          "either of the two constructed-pair rows leaving controls.py at that "
          "commit, which cannot happen -- it is a commit.  This line is here "
          "because the live run above can no longer make it, and a measurement "
          "that stops being runnable and is quoted instead is how a figure goes "
          "stale (mg-8e30)")
    for name in WERE_INVISIBLE:
        hit = [r for r in rows if r[0] == name]
        ok = bool(hit) and hit[0][3] == "CHANGED" and hit[0][4] == "1"
        claim("%r -- which left the artifact BYTE-IDENTICAL at 20738 bytes "
              "before mg-04a8 -- %s the artifact (%s -> %s bytes) at %s and "
              "exits %s"
              % (name, hit[0][3].lower() if hit else "?",
                 hit[0][1] if hit else "?", hit[0][2] if hit else "?",
                 TWO_RETURN_REF, hit[0][4] if hit else "?"), ok,
              "the constructed pair for that branch no longer reaching it -- "
              "which is what `absorb_trace` returning a different gate on it "
              "would mean, and what the row in controls.py scores directly")
    claim("AND THE GATE-LEVEL LINE IS EXACTLY THE ONE mg-e7bc TOOK APART: "
          "%r at %s deletes TWO `return` statements in one anchor, so its "
          "CHANGED is a claim about the pair.  The per-return split is in "
          "d2_deletion.py, section PER RETURN"
          % (WERE_INVISIBLE[0], TWO_RETURN_REF),
          any(r[0] == WERE_INVISIBLE[0] for r in rows),
          "that mutation being split per return in the audit itself, which "
          "would make this line unnecessary rather than wrong")

    head("mg-e7bc's OWN DELETION TEST -- the audit that found the granularity")
    print("It stops in the same place for the same reason: its D1 deletes the")
    print("same two returns.  Its E1 and E2 -- the per-return split that is this")
    print("commit's subject -- are re-run at %s below.\n" % E7BC_REF)
    e7_live, e7_live_code = run_script(AUDIT_E7BC, "g2_deletion.py")
    claim("against this tree it stops at D1 with `anchor occurs 0 times` and "
          "exits %d -- the same merged text, named by a second instrument"
          % e7_live_code,
          e7_live_code != 0 and "anchor occurs 0 times" in e7_live
          and "D1/face_complex.py" in e7_live,
          "the merged condition being split back into two returns.  Two "
          "independent instruments naming the same absent anchor is what makes "
          "this a fact about the source text rather than about either of them",
          e7_live.strip().split("\n")[-1][:160])
    e7_root = archive(E7BC_REF)
    e7_out, e7_code = run_script(os.path.join(e7_root, "code",
                                              "face_geometry_audit_e7bc"),
                                 "g2_deletion.py", e7_root)
    e1_line = [l for l in e7_out.split("\n") if l.strip().startswith("E1*")
               and "BYTE-IDENTICAL" in l]
    e2_line = [l for l in e7_out.split("\n") if l.strip().startswith("E2*")
               and "CHANGED" in l]
    claim("at %s its OWN per-return split reproduces: E1 (first `shape` return "
          "alone) BYTE-IDENTICAL, E2 (second alone) CHANGED.  That is the "
          "finding this commit answers, measured on the tree it is about "
          "rather than taken from its transcript" % E7BC_REF,
          len(e1_line) >= 1 and len(e2_line) >= 1,
          "that audit's table changing.  If this ever failed, the finding "
          "mg-9220 acted on would be unsupported and the merge below would have "
          "no reason",
          "; ".join(l.strip()[:110] for l in (e1_line + e2_line)[:2])
          or "E1/E2 result lines not found; exit %d" % e7_code)
    for root in (pinned_root, e7_root):
        shutil.rmtree(root, ignore_errors=True)

    head("AND THE REST OF THAT AUDIT, AGAINST THIS TREE -- every script named")
    print("Four scripts, and each is stated rather than left to be found.  g4 is")
    print("NOT run here: it re-runs THIS file, and this file running it would not")
    print("terminate.  Its own run_all.sh runs it.\n")
    for script, want_zero, why in (
            ("g1_positive_control.py", True,
             "its `pc_all_pass.txt` control is REGENERATED by this commit -- it "
             "is a derived copy of controls_output.txt and its own claim says a "
             "control describing a previous artifact tests nothing about this "
             "one.  Its FINDING (the deleted-row corruption) is untouched and "
             "does not set its exit status"),
            ("g3_differs_under.py", False,
             "it aborts on the same absent anchor: its `s1` mutation is the "
             "FIRST `shape` return, alone -- the very experiment that produced "
             "the finding this commit acts on.  It also freezes '56 claims "
             "across four scripts', a figure this commit moves.  Both are "
             "stale numbers about a tree that has changed, not retreats")):
        txt, code = run_script(AUDIT_E7BC, script)
        n = re.search(r"(\d+) claim\(s\) scored; (\d+) BROKEN", txt)
        claim("%s against this tree: exit %d (expected %s).  %s"
              % (script, code, "0" if want_zero else "nonzero", why),
              (code == 0) == want_zero,
              "g1 going red for any reason other than a stale derived control, "
              "or g3 going green -- the second would mean the anchor came back",
              "%s; last line: %r"
              % (n.group(0) if n else "no claim tally",
                 txt.strip().split("\n")[-1][:120]))

    head("AND WHY IT EXITS 1 AT THE PINNED COMMIT, WHICH IS NOT A FAILURE")
    out = pout
    broken = re.search(r"^E1 claims broken: (\d+)$", out, re.M)
    n_broken = int(broken.group(1)) if broken else -1
    row_claim = re.search(r"^  \[BROKEN\] the unmutated battery scores (\d+) rows",
                          out, re.M)
    claim("exactly %d claim of that audit is BROKEN at %s, and it is its ROW "
          "COUNT: it asserts 41, the number it measured at 5988134, and that "
          "tree has %s -- the two constructed-pair rows mg-04a8 added"
          % (n_broken, TWO_RETURN_REF, row_claim.group(1) if row_claim else "?"),
          n_broken == 1 and row_claim is not None
          and row_claim.group(1) == "43",
          "any OTHER claim of that audit going broken -- that would mean the "
          "repair disturbed something the audit had verified, and it is the "
          "reason this is scored rather than asserted in prose",
          "its exit status is %d; a frozen count measured against a tree that "
          "has since gained rows is a stale number, not a refutation" % pcode)
    head("AND WHAT THE REST OF THAT AUDIT SAYS -- did anything retreat?")
    for script, want_broken, why in (
            ("e2_parity.py", 0,
             "it re-derives where the predicate returns over all four "
             "populations, and the 297/306/82/172 split and the 57-of-297 "
             "disagreement are untouched by this repair"),
            ("e3_seams.py", 2,
             "its two remaining BROKEN claims are FROZEN LITERALS of the same "
             "kind as its row count -- it asserts the artifact says 'lines "
             "scanned: 62' and '40 row names among them', and the artifact now "
             "says 64 and 42.  Both are computed live by the row itself and "
             "both are correct: there are exactly 64 lines above it and 43 "
             "scored rows of which it is one")):
        p = subprocess.run([sys.executable, script], cwd=AUDIT,
                           capture_output=True, text=True)
        txt = p.stdout + p.stderr
        m = re.search(r"claims broken: (\d+)", txt)
        n = int(m.group(1)) if m else -1
        claim("%s: %d claim(s) broken against this tree (expected %d).  %s"
              % (script, n, want_broken, why), n == want_broken,
              "a claim of that audit about the MATHEMATICS or about the "
              "predicate's behaviour going broken -- that would be this repair "
              "disturbing something already verified, and it is the difference "
              "between a stale figure and a retreat",
              "exit %d; %s" % (p.returncode, (m.group(0) if m else "unparsed")))
    art = open(os.path.join(HERE, "..", "face_geometry",
                            "controls_output.txt")).read()
    claim("and the two extents those frozen literals disagree with are printed "
          "LIVE by the row that owns them, and are right: 'lines scanned: 64' "
          "with 64 lines above it, '42 row names' with 43 scored rows of which "
          "it is one",
          "lines scanned: 64 (the whole artifact above this row; 42 row names"
          in art
          and len([l for l in art.split("\n")[:art.split("\n").index(
              [x for x in art.split("\n") if "lines scanned: 64" in x][0])]]) == 64,
          "a checker printing an extent it did not measure -- the mg-a4ef/"
          "mg-7dd3 defect.  These two move whenever a row is added, which is "
          "how this repair moved them")

    claim("and the number it was frozen against is the one mg-5f9a PUBLISHED as "
          "43 while the artifact carried 41 (mg-d0e2's F3).  The artifact now "
          "genuinely carries 43, so the old figure is right for the wrong "
          "reason and is corrected at its sites rather than left to be read as "
          "confirmation",
          "43 rows -- lines whose marker STARTS the line" in out
          or (row_claim is not None and row_claim.group(1) == "43"),
          "the row population changing again without the doc sites being "
          "re-derived, which is the mg-8e30 defect (a figure measured before "
          "the edit that moved it)")

    print("\n" + BAR)
    print("%d claim(s) scored; %d BROKEN." % (len(SCORE), SCORE.count(False)))
    print(BAR)
    return 1 if not all(SCORE) else 0


if __name__ == "__main__":
    sys.exit(main())
