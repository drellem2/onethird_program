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
    BAR, FG, PRE_REPAIR_REF, head, mutate_tree, run_controls, write_ref_tree,
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
# The two mg-d0e2 found invisible.  Both returns of the shape gate go together:
# they are one gate, and deleting one of two would leave the other answering.
NEW_SHAPE = ('face_complex.py',
             '    m = len(A)\n'
             '    if m != len(B):\n'
             '        return Trace(False, "shape", 0)\n'
             '    for i in range(m):\n'
             '        if len(A[i]) != len(B[i]):\n'
             '            return Trace(False, "shape", 0)\n'
             '        if A[i][i] != B[i][i]:\n',
             '    m = len(A)\n'
             '    for i in range(m):\n'
             '        if A[i][i] != B[i][i]:\n')
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
    ("AFTER-5", "this tree: delete BOTH `shape` returns (mg-d0e2 OUTSTANDING 1)",
     "artifact CHANGES, exit 1, the `shape` branch row fails -- it was invisible"),
    ("AFTER-6", "this tree: delete the `parity` contradiction branch (ditto)",
     "artifact CHANGES, exit 1, the `parity` branch row fails -- ditto"),
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


def run_case(tag, desc, tree_files, edits, baseline, base_code,
             want_change, want_exit, want_fail_subs, baseline_cannot=()):
    if tree_files is PRE_FILES:
        root, _sha = write_ref_tree(tree_files)
        for fname, old, new in edits:
            path = os.path.join(root, fname)
            text = open(path).read()
            if text.count(old) != 1:
                raise SystemExit("%s: anchor occurs %d times in %s's %s"
                                 % (tag, text.count(old), PRE_REPAIR_REF, fname))
            with open(path, "w") as fh:
                fh.write(text.replace(old, new))
        cwd = root
    else:
        cwd = mutate_tree(edits, tree_files)
    out, code = run_controls(cwd)
    changed = out != baseline
    claim("%s -- %s: artifact %s (predicted %s), exit %d (predicted %d)"
          % (tag, desc, "CHANGES" if changed else "BYTE-IDENTICAL",
             "CHANGES" if want_change else "BYTE-IDENTICAL", code, want_exit),
          changed == want_change and code == want_exit,
          "deleting a gate that no row's answer depends on -- which is what "
          "AFTER-5 and AFTER-6 used to be, and what BEFORE-1 still is",
          "%d bytes out vs %d baseline; unmutated baseline exited %d"
          % (len(out), len(baseline), base_code))
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
    print(BAR)
    print("\nPREDICTIONS, registered before the runs:")
    for tag, desc, pred in PREDICTIONS:
        print("   %-9s %-62s %s" % (tag, desc, pred))
    print("\n   (*) %s's fail-set was registered as %r and that was WRONG: %s."
          % MISREGISTERED)
    print("       The registration above is the corrected one; the miss is kept "
          "here rather than\n       edited away, and the label check below is "
          "what caught it.")

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
    a5 = run_case("AFTER-5", "delete both `shape` returns", NEW_FILES,
                  [NEW_SHAPE], new_base, new_code, True, 1,
                  ["the predicate's `shape` branch"], base_cannot)
    a6 = run_case("AFTER-6", "delete the `parity` contradiction branch",
                  NEW_FILES, [NEW_PARITY], new_base, new_code, True, 1,
                  ["the predicate's `parity` branch"], base_cannot)

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
