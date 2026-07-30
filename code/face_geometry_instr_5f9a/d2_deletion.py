"""mg-5f9a part 2 -- THE DELETION TEST, run on BOTH sides of the repair.
REPAIRED BY mg-04a8, which is the second half of this file's story.

This is the test that caught the last version, so it is the test this one has to
pass.  mg-1c80 stated it as: REMOVE THE GATE THE EXPLANATION NAMES AS DECISIVE
AND CONFIRM THE ARTIFACT CHANGES.  If it does not, the named gate is not what
the code is doing.

BOTH SIDES, because half of it is asking to be believed.  The BEFORE half runs
the PRE-REPAIR tree (pinned commit, see `kern5f9a.PRE_REPAIR_REF`), deletes its
diagonal gate, and checks the artifact against that commit's committed
`controls_output.txt` -- mg-1c80's M2, re-run here rather than quoted.  The
AFTER half does the corresponding deletions on this tree.

PREDICTIONS ARE PRINTED BEFORE THE RESULTS and were written before the runs.

WHAT mg-d0e2 FOUND IN THIS FILE, and it is why the file was rewritten.

  OUTSTANDING 1 -- the deletion test bit on 7 of the 9 mutations that audit ran,
  and TWO moved not one byte: the `shape` returns and the `parity` contradiction
  branch.  Nothing this battery constructs reached either.  The two branches are
  now exercised by two new rows in `controls.py` against an enumerated brute
  force, and the two deletions are AFTER-5 and AFTER-6 below.  9 of 9.

  OUTSTANDING 2 -- THIS FILE'S OWN "every scored row keeps its label" CHECK WAS
  VACUOUS.  It extracted rows by substring and compared `a.split(" ")[1]`; row
  lines are indented, so that token was the empty string for every row and the
  check compared '' with '' 43 times.  mg-d0e2 ran it verbatim on an artifact in
  which EVERY ROW READ [FAIL] and it reported "43 rows, 0 label change(s)" and
  HELD.

  THE CAUSE IS NOT THE PARSING BUG.  The check measured the STABILITY of the
  labels between two runs, and stability is what a wrong label has too.  A
  mutation that ought to break a row, against a battery too blind to notice, is
  indistinguishable under a stability test from a mutation that broke nothing:
  both leave the labels where they were.  So the labels are now compared against
  an EXPECTED VALUE DERIVED THREE OTHER WAYS -- the fail-set registered beside
  each mutation before it ran, the process exit status (which `summarise`
  computes from the tallies, not from the printed rows), and the summary block
  the battery prints at the bottom.  `vacuous_check_as_shipped` below keeps the
  old code as a specimen and `positive_control_all_fail.txt` keeps the artifact
  it passed on; the last section runs both on it, and the repaired check goes
  red where the shipped one held.

WHAT mg-e7bc FOUND IN THIS FILE, and it is why the file was rewritten AGAIN.

  THE DELETION TEST WAS APPLIED AT THE GRANULARITY OF A GATE AND READ AT THE
  GRANULARITY OF A RETURN.  `absorb_trace`'s `shape` gate had TWO `return`
  statements.  AFTER-5 deleted them TOGETHER -- with the note "they are one
  gate, and deleting one of two would leave the other answering" -- the artifact
  changed, and the gate was booked as covered.  That sentence is TRUE, and it is
  precisely why the branch stayed uncovered: DELETING THE FIRST ONE ALONE left
  the artifact BYTE-IDENTICAL at 23,680 bytes, every row green, exit 0.  The
  2x2-against-3x3 pair falls into the loop and the SECOND return answers False
  at gate "shape" identically.

  SO THE TEST PROVED THE PAIR WAS LOAD-BEARING AND PROVED NOTHING ABOUT EITHER
  RETURN.  "Deleting X changes the artifact" is a claim about X AT THE
  GRANULARITY X WAS DELETED AT, and nothing finer.  It is the same error one
  level down that broke mg-db09, where equality of one statistic was taken for
  identity of a structure.

  BOTH HALVES ARE FIXED HERE.  Every mutation now declares THE UNIT IT REMOVES,
  the number of `return` statements it removes is COUNTED FROM ITS OWN PATCH
  TEXT rather than asserted, and a claim requires that no mutation removes more
  than one.  The unit is printed beside every result, so a reader of a line
  saying CHANGES can see what was taken out.  And the inert return is GONE:
  mg-9220 merged the two into one total condition in `face_complex.py`, so this
  tree has one `shape` return and AFTER-5 removes exactly it.  REMOVAL, NOT
  DETECTION -- no row was added to `controls.py` to notice the first return
  being reached, because a statement that does nothing is deleted rather than
  watched.  The section PER RETURN below reproduces the finding against the
  pinned two-return tree, and the section after it measures that the merge did
  not quietly narrow the gate.

EVERY CLAIM PRINTS WHAT WOULD MAKE IT ANSWER DIFFERENTLY (mg-d0e2's added
requirement).  "Can this check fire?" is necessary and not sufficient: both
vacuous checks this repository produced in one afternoon could fire in
principle, and each was blind to the specific defect it was read as guarding.
Naming the change forces the question of whether that change is the failure.

Nothing under ../face_geometry is written: every mutation is applied to a copy
in a temporary directory, and every battery run captures stdout rather than
tee-ing it.
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kern5f9a import (                                              # noqa: E402
    BAR, FG, PRE_REPAIR_REF, TWO_RETURN_REF, head, load_module, mutate_tree,
    run_controls, write_ref_tree,
)

SCORE = []

HERE = os.path.dirname(os.path.abspath(__file__))
POSITIVE_CONTROL = os.path.join(HERE, "positive_control_all_fail.txt")

NEW_FILES = ["face_complex.py", "posets.py", "controls.py", "run_probe.py"]
PRE_FILES = ["face_complex.py", "posets.py", "controls.py"]

MARKERS = ("[PASS]", "[FAIL]", "[CANNOT FAIL]")

# ----------------------------------------------------------------- this tree
NEW_DIAG = ('face_complex.py',
            '        if A[i][i] != B[i][i]:\n'
            '            return Trace(False, "diagonal", 0)\n',
            '')
NEW_MAG = ('face_complex.py',
           '            if abs(A[i][j]) != abs(B[i][j]):\n'
           '                return Trace(False, "magnitude", 0)\n',
           '            pass\n')
NEW_ORDER = ('face_complex.py',
             '        if A[i][i] != B[i][i]:\n'
             '            return Trace(False, "diagonal", 0)\n'
             '        for j in range(m):\n'
             '            if abs(A[i][j]) != abs(B[i][j]):\n'
             '                return Trace(False, "magnitude", 0)\n',
             '        for j in range(m):\n'
             '            if abs(A[i][j]) != abs(B[i][j]):\n'
             '                return Trace(False, "magnitude", 0)\n'
             '        if A[i][i] != B[i][i]:\n'
             '            return Trace(False, "diagonal", 0)\n')
NEW_SIGNS = ('face_complex.py',
             '            signs_read += 1\n',
             '            pass\n')
# The two mg-d0e2 found invisible.  THE SHAPE GATE IS ONE `return` NOW: mg-9220
# merged the two this mutation used to delete together, because deleting the
# first of them ALONE moved not one byte (mg-e7bc).  So this patch removes ONE
# return statement and the claim it licenses is a claim about that statement.
NEW_SHAPE = ('face_complex.py',
             '    m = len(A)\n'
             '    if m != len(B) or any(len(A[i]) != len(B[i]) '
             'for i in range(m)):\n'
             '        return Trace(False, "shape", 0)\n'
             '    for i in range(m):\n',
             '    m = len(A)\n'
             '    for i in range(m):\n')
NEW_PARITY = ('face_complex.py',
              '            if ri == rj:\n'
              '                if pi ^ pj != need:\n'
              '                    return Trace(False, "parity", signs_read)\n'
              '            else:\n',
              '            if ri == rj:\n'
              '                pass\n'
              '            else:\n')

# --------------------------------------------------- the pre-repair tree
PRE_DIAG = ('face_complex.py',
            '        if len(A[i]) != len(B[i]) or A[i][i] != B[i][i]:\n'
            '            return False\n',
            '        if len(A[i]) != len(B[i]):\n'
            '            return False\n')
PRE_MAG = ('face_complex.py',
           '            if abs(A[i][j]) != abs(B[i][j]):\n'
           '                return False\n',
           '            pass\n')

# ------------------------------------- the TWO-RETURN tree (mg-04a8, pinned)
# The granularity finding is a fact about a tree in which the `shape` gate has
# two `return` statements.  This tree has one, so the finding is reproduced
# against `TWO_RETURN_REF` rather than quoted from mg-e7bc's transcript.  Each
# of these removes exactly ONE return; the third removes the pair, which is what
# AFTER-5 used to do.
OLD_SHAPE_1 = ('face_complex.py',
               '    m = len(A)\n'
               '    if m != len(B):\n'
               '        return Trace(False, "shape", 0)\n'
               '    for i in range(m):\n',
               '    m = len(A)\n'
               '    for i in range(m):\n')
OLD_SHAPE_2 = ('face_complex.py',
               '        if len(A[i]) != len(B[i]):\n'
               '            return Trace(False, "shape", 0)\n'
               '        if A[i][i] != B[i][i]:\n',
               '        if A[i][i] != B[i][i]:\n')

# THE UNIT EACH MUTATION REMOVES, named beside it.  This is the second half of
# mg-e7bc's fix: a deletion result is a claim about the unit that was deleted,
# so the unit has to be written where the result is read.  `returns_removed`
# below COUNTS the return statements from the patch text; the string says what
# kind of thing went, since three of these remove no return at all.
UNITS = [
    ("BEFORE-1", PRE_DIAG,
     "one CLAUSE of a compound condition (`or A[i][i] != B[i][i]`); the "
     "`return` it guards stays and still answers on the other clause"),
    ("BEFORE-2", PRE_MAG, "one `return` statement -- the magnitude gate"),
    ("AFTER-1", NEW_DIAG, "one `return` statement -- gate `diagonal`"),
    ("AFTER-2", NEW_MAG, "one `return` statement -- gate `magnitude`"),
    ("AFTER-3", NEW_ORDER,
     "NO statement: the ORDER of two gates, both returns kept"),
    ("AFTER-4", NEW_SIGNS,
     "one statement, and not a `return`: the `signs_read += 1` counter"),
    ("AFTER-5", NEW_SHAPE,
     "one `return` statement -- gate `shape`, which is ONE return since "
     "mg-9220 merged the two"),
    ("AFTER-6", NEW_PARITY,
     "one `return` statement -- the `parity` contradiction branch"),
    ("R1", OLD_SHAPE_1,
     "one `return` statement -- the FIRST of the pinned tree's two `shape` "
     "returns"),
    ("R2", OLD_SHAPE_2,
     "one `return` statement -- the SECOND of them"),
    ("R3", ('face_complex.py', OLD_SHAPE_1[1] + OLD_SHAPE_2[1],
            OLD_SHAPE_1[2] + OLD_SHAPE_2[2]),
     "TWO `return` statements -- the PAIR, which is what AFTER-5 removed until "
     "mg-9220.  KEPT DELIBERATELY as the specimen"),
]

SPECIMEN_TAGS = ("R3",)
"""The mutation that removes two returns, kept rather than fixed.

The same treatment `vacuous_check_as_shipped` gives the shipped label check: the
defect is kept where it can be run, because a bundled deletion whose result was
read one level down is easier to recognise beside the un-bundled pair than in a
paragraph about it.  It is excluded from the at-most-one claim BY NAME, so a new
mutation that bundles two returns is BROKEN rather than quietly tolerated.
"""


def returns_removed(edit):
    """How many `return` statements this (file, old, new) patch takes out.

    Counted from the patch text, not declared.  A mutation that removes two is
    a mutation whose result licenses a claim about the PAIR and about neither
    member -- which is exactly what AFTER-5 was before mg-9220, and the reason
    this function exists rather than a sentence saying the same thing.
    """
    _f, old, new = edit
    def n(text):
        return sum(1 for ln in text.split("\n")
                   if ln.strip().startswith("return "))
    return n(old) - n(new)

# THE REGISTERED EXPECTATION, written before the runs.  The fail-set is the half
# that makes the label check non-vacuous: it says WHICH rows must read [FAIL],
# by a substring of the row's own text, so a mutation that ought to break a row
# and does not is a BROKEN claim rather than a stable pair of labels.
PREDICTIONS = [
    ("BEFORE-1", "pre-repair tree: delete the s_i^2 = 1 gate (mg-1c80's M2)",
     "artifact BYTE-IDENTICAL, exit 0 -- the finding this landing answers"),
    ("BEFORE-2", "pre-repair tree: delete the |s_i s_j| = 1 gate (mg-1c80's M1)",
     "artifact CHANGES, exit 1 -- that gate is what forbids I4's antichains"),
    ("AFTER-1*", "this tree: delete the s_i^2 = 1 gate from `absorb_trace`",
     "artifact CHANGES, exit 0, NO row fails -- no decision moves, the trace does"),
    ("AFTER-2", "this tree: delete the |s_i s_j| = 1 gate from `absorb_trace`",
     "artifact CHANGES, exit 1, the brute-force instrument row fails (*)"),
    ("AFTER-3*", "this tree: test row i's magnitudes BEFORE row i's diagonal",
     "artifact CHANGES, exit 0, NO row fails -- same answers, different trace"),
    ("AFTER-4", "this tree: stop counting the signs the union-find reads",
     "artifact CHANGES, exit 0, NO row fails"),
    ("AFTER-5", "this tree: delete the ONE `shape` return (mg-d0e2 OUTSTANDING 1)",
     "artifact CHANGES, exit 1, the `shape` branch row fails -- it was invisible"),
    ("AFTER-6", "this tree: delete the `parity` contradiction branch (ditto)",
     "artifact CHANGES, exit 1, the `parity` branch row fails -- ditto"),
    ("R1", "PINNED two-return tree: delete ONLY the FIRST `shape` return",
     "artifact BYTE-IDENTICAL, exit 0 -- mg-e7bc's finding, reproduced"),
    ("R2", "PINNED two-return tree: delete ONLY the SECOND `shape` return",
     "artifact CHANGES, exit 1 -- the return that was doing all the work"),
    ("R3", "PINNED two-return tree: delete BOTH, as AFTER-5 used to",
     "artifact CHANGES, exit 1 -- true of the PAIR, and of neither member"),
]

# (*) AFTER-2'S FAIL-SET WAS REGISTERED WRONG THE FIRST TIME, and the corrected
# registration is above.  It was registered as "row I4 fails", from mg-d0e2's
# note that three of row I4's pairs violate the magnitude gate ALONE.  The run
# says otherwise: row I4 still passes on 61/61 with `absorb == 0` intact, because
# with the magnitude gate gone those three pairs go on to the SIGN SYSTEM and are
# rejected there instead -- the answer does not move, only the gate that produces
# it.  What fails is the union-find-versus-brute-force instrument row, 291 of 306.
# The miss is recorded rather than edited away: a prediction quietly rewritten
# after its run is not a prediction, and the label check below is what caught it
# -- under the shipped stability check this registration would never have been
# tested at all.
MISREGISTERED = ("AFTER-2", "row I4 fails",
                 "row I4 passes on 61/61; the union-find-vs-brute-force "
                 "instrument row fails on 291/306")


def claim(text, ok, differs_under, detail=""):
    """Score one claim of this instrument's own.

    `differs_under` is not decoration.  mg-d0e2's requirement, after two vacuous
    checks in one afternoon: state what change would make this claim answer
    differently.  A claim whose author cannot name one is measuring something
    invariant under the failure it is read as guarding.
    """
    SCORE.append(ok)
    print("  [%s] %s" % ("HOLDS " if ok else "BROKEN", text))
    if detail:
        print("        " + detail)
    print("        WOULD DIFFER UNDER: %s" % differs_under)


# ---------------------------------------------------------------- row parsing
def scored_rows(text):
    """(label, name) for every line whose FIRST non-space characters are a score
    marker.

    A ROW IS A LINE THAT STARTS WITH ITS MARKER.  The shipped version of this
    file selected lines by `"[PASS]" in l`, which also catches the prose bullets
    under "measured, not scored" that quote a marker mid-sentence -- that is
    mg-d0e2's F3, the reason "43 rows" was published for an artifact carrying 41.
    """
    rows = []
    for ln in text.split("\n"):
        s = ln.strip()
        for m in MARKERS:
            if s.startswith(m):
                rows.append((m, s[len(m):].strip()))
                break
    return rows


def summary_block(text):
    """(fail names, cannot-fail names) as the battery's BOTTOM LINE reports them.

    A SECOND CHANNEL, and that is the whole point of reading it.  `controls.check`
    prints the row lines; `controls.summarise` builds this block from the tallies
    those calls accumulated.  An artifact whose rows have been edited -- by a
    corruption, a bad merge, or a hand -- disagrees with its own summary, and the
    check below is what notices.  Names are truncated at 75 chars by `summarise`,
    so matching is by prefix.
    """
    fails, cannots, mode = [], [], None
    for ln in text.split("\n"):
        if ln.startswith("CONTROLS FAILED:"):
            mode = fails
            continue
        if ln.startswith("CONTROLS: 0 failures, but"):
            mode = cannots
            continue
        if ln.startswith("   - ") and mode is not None:
            mode.append(ln[5:].rstrip().rstrip("."))
            continue
        if mode is not None and ln and not ln.startswith("   - "):
            mode = None
    return fails, cannots


def expected_labels(text, exit_code, registered_fail_subs, baseline_cannot):
    """The label every scored row OUGHT to carry, derived WITHOUT looking at the
    labels.

    Four inputs, none of them the row markers being checked:
      * `registered_fail_subs` -- substrings naming the rows this mutation was
        predicted to break, written down before the run;
      * `exit_code` -- the process's status, which `summarise` computes from the
        FAIL tally;
      * the summary block, which lists the failing rows from that same tally;
      * `baseline_cannot` -- the CANNOT FAIL rows, taken from the UNMUTATED run's
        summary block.  They have to come from there: `summarise` returns as soon
        as anything failed, so on a failing run it never prints the CANNOT FAIL
        list at all and that channel is silent exactly when it is needed.  Taking
        the set from the baseline also means a mutation that MOVED a row between
        [PASS] and [CANNOT FAIL] shows up as a mismatch -- which is right, since
        every prediction below says the mutation makes no scoring change.

    Returns (expected list, notes).  This is the repair mg-d0e2 asked for: the
    shipped check compared the mutant's labels with the BASELINE's, so a label
    that was wrong in both runs passed, and a mutation that should have broken a
    row but did not looked exactly like one that broke nothing.
    """
    rows = scored_rows(text)
    fails, _cannots = summary_block(text)
    expected, notes = [], []
    for _label, name in rows:
        by_summary_fail = any(name.startswith(f[:75].rstrip(".")) or
                              f.startswith(name[:75]) for f in fails)
        by_registered = any(sub in name for sub in registered_fail_subs)
        by_cannot = any(name.startswith(c[:75].rstrip(".")) or
                        c.startswith(name[:75]) for c in baseline_cannot)
        if by_summary_fail or by_registered:
            expected.append("[FAIL]")
        elif by_cannot:
            expected.append("[CANNOT FAIL]")
        else:
            expected.append("[PASS]")
    notes.append("%d row(s) named in this run's summary FAIL list, %d CANNOT "
                 "FAIL row(s) carried from the unmutated run, %d named by the "
                 "registered prediction"
                 % (len(fails), len(baseline_cannot), len(registered_fail_subs)))
    notes.append("exit %d, and the battery exits 1 exactly when some row FAILs"
                 % exit_code)
    return expected, notes


def check_labels(tag, text, exit_code, registered_fail_subs, baseline_cannot):
    """The repaired check.  Returns (ok, message, notes).

    EACH REGISTERED SUBSTRING MUST NAME EXACTLY ONE ROW.  Without that clause the
    check has the shipped one's disease in a new place: a registration naming a
    row that does not exist matches nothing, contributes no expectation, and the
    check passes -- which is exactly the state AFTER-5 and AFTER-6 were in before
    the two rows they name were written.  A prediction that cannot be located is
    not a weaker prediction, it is none.
    """
    rows = scored_rows(text)
    expected, notes = expected_labels(text, exit_code, registered_fail_subs,
                                      baseline_cannot)
    wrong = [(name, got, want) for (got, name), want in zip(rows, expected)
             if got != want]
    fails, _ = summary_block(text)
    exit_agrees = (exit_code == 1) == (len(fails) > 0)
    n_fail_rows = sum(1 for lab, _ in rows if lab == "[FAIL]")
    consistent = (n_fail_rows == len(fails))
    hits = [sum(1 for _lab, name in rows if sub in name)
            for sub in registered_fail_subs]
    located = all(h == 1 for h in hits) and len(rows) > 0
    ok = not wrong and exit_agrees and consistent and located
    msg = ("%s: %d scored row(s); every label equals the independently derived "
           "expectation (%d mismatch(es)); %d row(s) read [FAIL] and the summary "
           "block lists %d; exit %d %s; each of the %d registered row name(s) "
           "matches exactly one row (%s)"
           % (tag, len(rows), len(wrong), n_fail_rows, len(fails), exit_code,
              "agrees" if exit_agrees else "DISAGREES",
              len(registered_fail_subs),
              ", ".join(str(h) for h in hits) if hits else "none registered"))
    if wrong:
        msg += " || first mismatch: %r reads %s, expected %s" % (
            wrong[0][0][:60], wrong[0][1], wrong[0][2])
    return ok, msg, notes


def vacuous_check_as_shipped(base_text, mut_text):
    """mg-5f9a's own check, KEPT VERBATIM AS THE SPECIMEN.

    Not called by any scored claim except the one that demonstrates it holding on
    the broken artifact.  Two defects in four lines: rows are selected by
    substring (so prose bullets quoting a marker are counted as rows), and the
    label is taken as `a.split(" ")[1]` of a line that begins with two spaces --
    which is the empty string, always, for every row in either text.

    Returns (holds, message) reproducing exactly what it printed.
    """
    base_rows = [l for l in base_text.split("\n") if "[PASS]" in l
                 or "[CANNOT FAIL]" in l or "[FAIL]" in l]
    mut_rows = [l for l in mut_text.split("\n") if "[PASS]" in l
                or "[CANNOT FAIL]" in l or "[FAIL]" in l]
    changes = sum(a.split(" ")[1] != b.split(" ")[1]
                  for a, b in zip(base_rows, mut_rows))
    holds = (len(base_rows) == len(mut_rows)
             and all(a.split(" ")[1] == b.split(" ")[1]
                     for a, b in zip(base_rows, mut_rows)))
    return holds, ("every scored row keeps its label and its condition -- "
                   "%d rows, %d label change(s)" % (len(base_rows), changes))


def flip_all_rows(text):
    """Every scored row's marker replaced by [FAIL], and nothing else touched.

    THE POSITIVE CONTROL, generated rather than stored so it cannot silently
    describe a different artifact than the one shipped.  The bottom-line summary
    is deliberately left alone: that is what makes the file a corrupted artifact
    rather than a failing run, and it is exactly the disagreement between the two
    channels that the repaired check is supposed to find.
    """
    out = []
    for ln in text.split("\n"):
        s = ln.lstrip()
        indent = ln[:len(ln) - len(s)]
        hit = None
        for m in MARKERS:
            if s.startswith(m):
                hit = m
                break
        out.append(indent + "[FAIL]" + s[len(hit):] if hit else ln)
    return "\n".join(out)


def unit_of(tag):
    """The unit named for `tag` in UNITS, and the number of `return` statements
    its patch removes.  A tag with no entry is a programming error here, not a
    result to be printed without one."""
    for name, edit, unit in UNITS:
        if name == tag:
            return unit, returns_removed(edit)
    raise SystemExit("%s: no UNITS entry -- a deletion result with no unit "
                     "named beside it is what mg-e7bc found (mg-9220)" % tag)


def run_case(tag, desc, tree_files, edits, baseline, base_code,
             want_change, want_exit, want_fail_subs, baseline_cannot=(),
             ref=PRE_REPAIR_REF):
    if tree_files is PRE_FILES or ref != PRE_REPAIR_REF:
        root, _sha = write_ref_tree(tree_files, ref)
        for fname, old, new in edits:
            path = os.path.join(root, fname)
            text = open(path).read()
            if text.count(old) != 1:
                raise SystemExit("%s: anchor occurs %d times in %s's %s"
                                 % (tag, text.count(old), ref, fname))
            with open(path, "w") as fh:
                fh.write(text.replace(old, new))
        cwd = root
    else:
        cwd = mutate_tree(edits, tree_files)
    out, code = run_controls(cwd)
    changed = out != baseline
    unit, n_ret = unit_of(tag)
    # THE GRANULARITY IS PRINTED WHERE THE RESULT IS READ (mg-e7bc, mg-9220).
    # "The artifact changes when X is deleted" is a claim about X at the size X
    # was deleted at.  AFTER-5 used to remove two `return`s and be read as a
    # statement about each of them; the unit and the return count are carried
    # into the claim text so that reading cannot be made again silently.
    claim("%s -- %s: artifact %s (predicted %s), exit %d (predicted %d)  "
          "[UNIT REMOVED: %s]"
          % (tag, desc, "CHANGES" if changed else "BYTE-IDENTICAL",
             "CHANGES" if want_change else "BYTE-IDENTICAL", code, want_exit,
             unit),
          changed == want_change and code == want_exit,
          "deleting a gate that no row's answer depends on -- which is what "
          "AFTER-5 and AFTER-6 used to be, and what BEFORE-1 still is.  AND "
          "under this line being read at a granularity finer than the %d "
          "`return` statement(s) the patch takes out" % n_ret,
          "%d bytes out vs %d baseline; unmutated baseline exited %d; the "
          "patch removes %d `return` statement(s)"
          % (len(out), len(baseline), base_code, n_ret))
    if want_fail_subs is not None:
        ok, msg, notes = check_labels(tag, out, code, want_fail_subs,
                                      baseline_cannot)
        claim(msg, ok,
              "a row reading [FAIL] that the registered prediction and the "
              "summary block do not name, or a row this mutation was predicted "
              "to break still reading [PASS].  NOT under a label that is merely "
              "the same as the baseline's -- that is the shipped check, and it "
              "holds on an artifact where every row reads [FAIL]",
              "; ".join(notes))
    return out


def main():
    print(BAR)
    print("mg-5f9a part 2 -- the deletion test, before and after")
    print("(repaired by mg-04a8: two more deletions, and a label check that is "
          "not a stability test)")
    print("(repaired by mg-9220: PER RETURN, not per gate, with the unit "
          "printed beside every result)")
    print(BAR)
    print("\nPREDICTIONS, registered before the runs:")
    for tag, desc, pred in PREDICTIONS:
        print("   %-9s %-62s %s" % (tag, desc, pred))
    print("\n   (*) %s's fail-set was registered as %r and that was WRONG: %s."
          % MISREGISTERED)
    print("       The registration above is the corrected one; the miss is kept "
          "here rather than\n       edited away, and the label check below is "
          "what caught it.")

    head("THE UNIT EVERY MUTATION REMOVES -- counted from its own patch text")
    print("mg-e7bc: the deletion test was applied at the granularity of a GATE "
          "and read at\nthe granularity of a RETURN.  A result line says "
          "\"deleting X changes the artifact\";\nthat is a claim about X AT THE "
          "SIZE X WAS DELETED AT and about nothing finer.  So\nthe size is "
          "counted here, printed beside every result below, and required to be "
          "at\nmost one `return` -- because a patch that removes two licenses a "
          "claim about the\nPAIR and about neither member, which is exactly what "
          "AFTER-5 was.\n")
    print("   %-9s %-4s %s" % ("tag", "ret", "unit removed"))
    multi = []
    graded = [(t, e, u) for t, e, u in UNITS if t not in SPECIMEN_TAGS]
    for tag, edit, unit in UNITS:
        n = returns_removed(edit)
        if n > 1 and tag not in SPECIMEN_TAGS:
            multi.append((tag, n))
        print("   %-9s %-4d %s%s"
              % (tag, n, "SPECIMEN -- " if tag in SPECIMEN_TAGS else "", unit))
    claim("no mutation in this file removes more than one `return` statement, "
          "the specimen %s aside -- %d of %d remove exactly one, %d remove none "
          "(a clause, an ordering and a counter), %d remove more"
          % (", ".join(SPECIMEN_TAGS),
             sum(1 for _t, e, _u in graded if returns_removed(e) == 1),
             len(graded),
             sum(1 for _t, e, _u in graded if returns_removed(e) == 0),
             len(multi)),
          not multi,
          "any mutation bundling two returns again, other than the named "
          "specimen.  Before mg-9220 AFTER-5 removed TWO and this claim would "
          "have been BROKEN -- which is the point: the bundling was invisible "
          "because nothing counted it",
          "multi-return mutations outside the specimen: %s; the specimen "
          "removes %d and is kept so the bundled deletion can be run beside "
          "the un-bundled pair"
          % ("; ".join("%s removes %d" % (t, n) for t, n in multi)
             if multi else "none",
             returns_removed([e for t, e, _u in UNITS
                              if t in SPECIMEN_TAGS][0])))

    head("BEFORE -- the PRE-REPAIR tree, where mg-1c80 found the artifact unmoved")
    base_dir, pre_sha = write_ref_tree(PRE_FILES)
    repo = os.path.abspath(os.path.join(FG, "..", ".."))
    pre_art = subprocess.run(
        ["git", "show", "%s:code/face_geometry/controls_output.txt" % PRE_REPAIR_REF],
        cwd=repo, capture_output=True, text=True).stdout
    base_out, base_code = run_controls(base_dir)
    claim("%s (%s) -- its committed controls_output.txt regenerates from its own "
          "sources" % (PRE_REPAIR_REF, pre_sha[:7]),
          base_out == pre_art and len(base_out) == 17964,
          "this ref moving, or that tree's battery ceasing to be reproducible.  "
          "Before mg-04a8 the ref was `main`, and after mg-5f9a merged this "
          "claim read 'this tree regenerates from itself' -- true under every "
          "possible defect, and the deletion below no longer even applied",
          "%d bytes regenerated, %d committed, exit %d"
          % (len(base_out), len(pre_art), base_code))
    run_case("BEFORE-1", "delete the s_i^2 = 1 gate", PRE_FILES, [PRE_DIAG],
             base_out, base_code, want_change=False, want_exit=0,
             want_fail_subs=None)
    run_case("BEFORE-2", "delete the |s_i s_j| = 1 gate", PRE_FILES, [PRE_MAG],
             base_out, base_code, want_change=True, want_exit=1,
             want_fail_subs=None)

    head("AFTER -- this tree, where the gate label is emitted by the code path")
    new_dir = mutate_tree([], NEW_FILES)
    new_base, new_code = run_controls(new_dir)
    committed = open(os.path.join(FG, "controls_output.txt")).read()
    claim("this tree's controls_output.txt regenerates byte-identically",
          new_base == committed,
          "any edit to controls.py, face_complex.py or posets.py that is not "
          "followed by regenerating the committed artifact",
          "%d bytes regenerated, %d committed, exit %d"
          % (len(new_base), len(committed), new_code))
    # The CANNOT FAIL set, read from the unmutated run's summary block, and used
    # as the expected value for every mutant below (see `expected_labels`).
    _, base_cannot = summary_block(new_base)
    ok, msg, notes = check_labels("BASELINE", new_base, new_code, [], base_cannot)
    claim(msg, ok,
          "any row reading [FAIL] in an unmutated run, or a summary block that "
          "disagrees with the rows above it",
          "; ".join(notes))

    a1 = run_case("AFTER-1", "delete the s_i^2 = 1 gate", NEW_FILES, [NEW_DIAG],
                  new_base, new_code, True, 0, [], base_cannot)
    run_case("AFTER-2", "delete the |s_i s_j| = 1 gate", NEW_FILES, [NEW_MAG],
             new_base, new_code, True, 1,
             ["the union-find absorbability decision agrees with brute force"],
             base_cannot)
    a3 = run_case("AFTER-3", "magnitudes before the diagonal", NEW_FILES,
                  [NEW_ORDER], new_base, new_code, True, 0, [], base_cannot)
    run_case("AFTER-4", "stop counting signs read", NEW_FILES, [NEW_SIGNS],
             new_base, new_code, True, 0, [], base_cannot)
    a5 = run_case("AFTER-5", "delete the one `shape` return", NEW_FILES,
                  [NEW_SHAPE], new_base, new_code, True, 1,
                  ["the predicate's `shape` branch"], base_cannot)
    a6 = run_case("AFTER-6", "delete the `parity` contradiction branch",
                  NEW_FILES, [NEW_PARITY], new_base, new_code, True, 1,
                  ["the predicate's `parity` branch"], base_cannot)

    head("PER RETURN, NOT PER GATE -- the same test one level down")
    print("AFTER-5 above removes ONE return, because there is one.  There were "
          "TWO until\nmg-9220, and AFTER-5 removed them together: the artifact "
          "changed, exit 1, one row\nfailed, and the gate was booked as covered. "
          " That result is a claim about the\nPAIR.  Below, each of the two is "
          "deleted ALONE against the tree that has them\n(%s, pinned for the "
          "reason PRE_REPAIR_REF gives -- this tree has nothing left to\ndelete "
          "one of).  Predictions were registered above.\n" % TWO_RETURN_REF)
    two_dir, two_sha = write_ref_tree(NEW_FILES, TWO_RETURN_REF)
    two_base, two_code = run_controls(two_dir)
    claim("%s (%s) -- the two-return tree regenerates its own artifact, so the "
          "three results below are against a baseline of its own and not this "
          "tree's" % (TWO_RETURN_REF, two_sha[:7]),
          two_code == 0 and len(two_base) > 0,
          "that ref moving, or that tree ceasing to be reproducible.  Its "
          "artifact is NOT this tree's: mg-9220 edited one row's text, so "
          "comparing against the live committed file would report a difference "
          "this section is not about",
          "%d bytes regenerated, exit %d" % (len(two_base), two_code))
    r1 = run_case("R1", "delete ONLY the first `shape` return (m != len(B))",
                  NEW_FILES, [OLD_SHAPE_1], two_base, two_code, False, 0,
                  None, ref=TWO_RETURN_REF)
    run_case("R2", "delete ONLY the second `shape` return (ragged rows)",
             NEW_FILES, [OLD_SHAPE_2], two_base, two_code, True, 1,
             None, ref=TWO_RETURN_REF)
    run_case("R3", "delete BOTH, as AFTER-5 used to", NEW_FILES,
             [OLD_SHAPE_1, OLD_SHAPE_2], two_base, two_code, True, 1,
             None, ref=TWO_RETURN_REF)
    claim("THE GRANULARITY FINDING REPRODUCES: on the two-return tree the PAIR "
          "is load-bearing (R3 CHANGES) and the FIRST RETURN IS NOT (R1 leaves "
          "%d bytes, byte-identical).  R3 is the result AFTER-5 used to print, "
          "and it never entitled anyone to R1's line" % len(r1),
          r1 == two_base,
          "a pair in `controls.py` with len(A) != len(B) and no ragged row -- "
          "a 2x2 against a three-row B whose first two rows are 2 wide would "
          "separate the two returns.  NO SUCH PAIR WAS ADDED (mg-9220): the "
          "inert return was deleted instead, because a statement that does "
          "nothing is removed rather than watched",
          "R1 %d bytes vs %d baseline; the 2x2-against-3x3 pair falls into the "
          "loop and the SECOND return answers False at gate 'shape' identically"
          % (len(r1), len(two_base)))

    head("AND THE MERGE DID NOT QUIETLY NARROW THE GATE")
    print("The first return was not cut, it was MERGED into the second's "
          "condition.  Cutting\nit is not the same edit: the three pairs below "
          "separate them, and R1's battery run\ncannot see any of them.  Three "
          "implementations are loaded side by side -- the\npinned tree's two-"
          "return `absorb_trace`, this tree's merged one, and the pinned one\n"
          "with its first return CUT and nothing put in its place.\n")
    two_fc = load_module(os.path.join(two_dir, "face_complex.py"), "fc_two")
    new_fc = load_module(os.path.join(new_dir, "face_complex.py"), "fc_new")
    cut_dir, _sha = write_ref_tree(NEW_FILES, TWO_RETURN_REF)
    p = os.path.join(cut_dir, "face_complex.py")
    txt = open(p).read()
    _f, old, new = OLD_SHAPE_1
    open(p, "w").write(txt.replace(old, new, 1))
    cut_fc = load_module(p, "fc_cut")

    def ask(fn, A, B):
        try:
            tr = fn(A, B)
            return (tr.absorbable, tr.gate)
        except Exception as exc:                        # noqa: BLE001
            return ("raised", type(exc).__name__)

    SEPARATORS = [
        ("an empty A against a 1x1 B", [], [[1]]),
        ("a 1x1 A against an empty B", [[1]], []),
        ("2x2 against a THREE-row B whose first two rows are 2 wide",
         [[0, 1], [1, 0]], [[0, 1], [1, 0], [0, 0]]),
    ]
    lines = []
    agree_merge = separated = 0
    for why, A, B in SEPARATORS:
        o, n, c = (ask(two_fc.absorb_trace, A, B), ask(new_fc.absorb_trace, A, B),
                   ask(cut_fc.absorb_trace, A, B))
        agree_merge += (o == n)
        separated += (o != c)
        lines.append("%s: two returns %s, merged %s, first return CUT %s"
                     % (why, o, n, c))
    claim("WHAT THE DELETED RETURN DID, on %d pairs the battery does not "
          "contain: the merged gate answers as the two returns did on %d of "
          "%d, and CUTTING the first instead of merging it changes the answer "
          "on %d of %d"
          % (len(SEPARATORS), agree_merge, len(SEPARATORS), separated,
             len(SEPARATORS)),
          agree_merge == len(SEPARATORS) and separated == len(SEPARATORS),
          "the merged condition losing its `m != len(B)` half, which is the "
          "cut.  This is the answer to \"remove it, or show what it does\": it "
          "does nothing the battery can see, and these three are what it does",
          "; ".join(lines))

    # And the same question asked over a population rather than three cases.
    ENTRIES = (0, 1, -1)
    mats = [[]]
    for m in (1, 2):
        for bits in range(len(ENTRIES) ** (m * m)):
            flat, b = [], bits
            for _k in range(m * m):
                flat.append(ENTRIES[b % len(ENTRIES)])
                b //= len(ENTRIES)
            mats.append([flat[i * m:(i + 1) * m] for i in range(m)])
    mats.append([[0, 1], [1, 0], [0, 0]])          # 3 rows, 2 wide
    mats.append([[0, 1, 0], [1, 0]])               # ragged
    mats.append([[0, 1], [1, 0, 0]])               # ragged the other way
    mats.append([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
    same_dec = same_gate = pairs = cut_moved = 0
    gate_moved = []
    for A in mats:
        for B in mats:
            pairs += 1
            o, n, c = (ask(two_fc.absorb_trace, A, B),
                       ask(new_fc.absorb_trace, A, B),
                       ask(cut_fc.absorb_trace, A, B))
            same_dec += (o[0] == n[0])
            same_gate += (o == n)
            if o != n:
                gate_moved.append((o, n))
            cut_moved += (o[0] != c[0])
    ragged_only = all(o[1] in ("diagonal", "magnitude") and n[1] == "shape"
                      for o, n in gate_moved)
    claim("over %d constructed pairs: the merged gate gives the SAME DECISION "
          "on %d of %d, the same (decision, gate) on %d, and the %d that move "
          "are all RAGGED pairs relabelled %r -> 'shape' -- which is what "
          "`gate_violations` and `priority_gate` always said about them.  "
          "Cutting the first return instead moves the DECISION on %d"
          % (pairs, same_dec, pairs, same_gate, len(gate_moved),
             sorted({o[1] for o, _n in gate_moved}) or "-", cut_moved),
          same_dec == pairs and ragged_only and cut_moved > 0,
          "a decision moving, which would make the merge a change to the "
          "predicate rather than to its text.  The population is every matrix "
          "over {0,1,-1} of order <= 2 plus four ragged and rectangular ones, "
          "crossed with itself -- built here, not taken from the battery, "
          "which has no ragged pair at all",
          "%d pairs; %d (decision, gate) moves; the battery's artifact is "
          "byte-identical across the merge, which is the same statement over "
          "the population that matters to the rows" % (pairs, len(gate_moved)))

    head("WHAT MOVED, AND WHAT DID NOT")
    for tag, out in (("AFTER-1", a1), ("AFTER-3", a3)):
        moved = [i for i, (a, b) in enumerate(zip(new_base.split("\n"),
                                                  out.split("\n"))) if a != b]
        claim("%s: the lines that DID move are the ones reporting where the "
              "predicate went -- %d line(s)" % (tag, len(moved)),
              len(moved) > 0,
              "a trace label that stops depending on the code path -- which is "
              "the whole defect mg-1c80 found, and what BEFORE-1 still shows",
              "; ".join("line %d" % (i + 1) for i in moved[:6]))
    for tag, out in (("AFTER-5", a5), ("AFTER-6", a6)):
        rows = scored_rows(out)
        failing = [n for lab, n in rows if lab == "[FAIL]"]
        claim("%s: exactly %d row fails, and it is the row built for that branch "
              "-- %r" % (tag, len(failing), (failing[0][:64] if failing else "")),
              len(failing) == 1,
              "the constructed pairs no longer reaching that branch, or the row "
              "scoring the predicate against itself instead of against brute "
              "force.  Before mg-04a8 these two deletions changed NOTHING: 20738 "
              "bytes in, 20738 identical bytes out, every row green")

    head("THE POSITIVE CONTROL -- an artifact in which every row reads [FAIL]")
    print("mg-d0e2 built it, ran the shipped check on it, and the shipped check")
    print("HELD.  It is kept and committed here because a check nobody has seen")
    print("go red on a broken input is a check nobody has tested.\n")
    broken = flip_all_rows(committed)
    claim("the committed positive control is exactly the committed artifact with "
          "every scored row's marker replaced by [FAIL], and nothing else",
          os.path.exists(POSITIVE_CONTROL)
          and open(POSITIVE_CONTROL).read() == broken,
          "controls_output.txt changing without this file being regenerated -- "
          "a positive control that describes a previous artifact is testing "
          "nothing about this one",
          "%d bytes; %d of its %d rows read [FAIL]"
          % (len(broken), sum(1 for lab, _ in scored_rows(broken)
                              if lab == "[FAIL]"), len(scored_rows(broken))))
    held, what = vacuous_check_as_shipped(committed, broken)
    claim("THE SHIPPED CHECK, VERBATIM, ON THAT ARTIFACT: %r, HOLDS = %s"
          % (what, held), held,
          "nothing available to a corruption of the artifact.  It compares "
          "`a.split(' ')[1]` of two indented lines -- '' against '' -- so its "
          "answer is fixed by the INDENTATION and cannot depend on any label.  "
          "This claim is scored TRUE because the defect is real: it is the one "
          "claim in this file that would be BROKEN if the defect had been "
          "imagined",
          "reproduces mg-d0e2's F2 from this repository's own code rather than "
          "quoting the audit")
    ok, msg, notes = check_labels("POSITIVE CONTROL", broken, 0, [], base_cannot)
    claim("THE REPAIRED CHECK ON THE SAME ARTIFACT GOES RED: %s" % msg, not ok,
          "the repaired check reverting to a comparison against the baseline's "
          "own labels, or to a substring row scan.  Either restores the shipped "
          "behaviour and this claim is the thing that notices",
          "; ".join(notes))

    head("A CONTROL ON THE REPAIRED CHECK -- three inputs, exercised directly")
    print("The positive control above shows it going red on a corrupted artifact.")
    print("These show it saying YES when it should, and red for each of the two")
    print("other ways a label claim can be wrong.  No battery is run: the check is")
    print("a pure function of (text, exit code, registration).\n")
    green = check_labels("c1", new_base, new_code, [], base_cannot)[0]
    stale = check_labels("c2", new_base, new_code,
                         ["I4 the facet enumeration"], base_cannot)[0]
    absent = check_labels("c3", new_base, new_code,
                          ["a row this artifact does not contain"],
                          base_cannot)[0]
    claim("on the unmutated artifact with nothing registered it says YES (%s); "
          "with a row registered as failing that did NOT fail it goes red (%s); "
          "with a registration naming no row at all it goes red (%s)"
          % (green, stale, absent),
          green and not stale and not absent,
          "the check losing either half.  The second case is the wrong-but-"
          "stable label -- the mutation did not break the row it was predicted "
          "to break, and the shipped stability check calls that a pass because "
          "the label did not move.  The third is a prediction that cannot be "
          "located, which reads as a prediction and is not one")

    print("\n" + BAR)
    print("%d claim(s) scored; %d BROKEN." % (len(SCORE), SCORE.count(False)))
    print(BAR)
    return 1 if not all(SCORE) else 0


if __name__ == "__main__":
    sys.exit(main())
