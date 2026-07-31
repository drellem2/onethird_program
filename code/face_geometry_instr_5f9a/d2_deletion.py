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

WHAT mg-c4c8 FOUND IN THIS FILE, and it is why the file was rewritten A THIRD
TIME (mg-64b6).

  OPEN 1 -- THE GRAIN ERROR RECURRED ONE LEVEL FINER, exactly where mg-e7bc
  predicted it would.  mg-9220 did not cut the inert return, it MERGED it: the
  two returns became TWO CLAUSES of one condition, `m != len(B) or
  any(len(A[i]) != len(B[i]) for i in range(m))`.  DELETING THE FIRST CLAUSE
  ALONE MOVED NOT ONE BYTE -- the artifact byte-identical at 23,684, exit 0,
  every row green.  Gate -> return -> clause is three rungs of one regress, and
  chasing them by hand means the next generation finds sub-clause.

  THE RUNG IS REMOVED RATHER THAN DESCENDED.  The two clauses said one thing --
  A and B do not have the same row-shape profile -- and `absorb_trace` now says
  it with one comparison and no boolean operator, so there is nothing under
  that `return` to delete alone.  The section PER CLAUSE reads the clause
  population out of the tree, deletes each ALONE, and states the FINEST UNIT
  the test perturbs beside every result; the two clauses this commit removed
  are swept against the pinned commit that still has them, which reproduces
  mg-c4c8's finding and is the sweep's positive control at once.

  OPEN 2 -- THE DECLARED UNIT UNDERSTATED ITS OWN PATCH ON 8 OF 11.  mg-9220's
  declarations were WRITTEN; eight said "one `return` statement" for a patch
  that removed the `return` together with the `if` that guarded it, and one of
  those removed a two-clause condition as well.  THE DECLARATION IS NOW
  DERIVED: `kern5f9a.unit_removed` parses the tree before and after each
  patch and reports what went, so the sentence a reader consults is a function
  of the patch and cannot be smaller than it.  Nothing in the mutation table
  states a size.  mg-9220's eleven sentences are kept verbatim as the specimen
  and the section THE DECLARATION THAT WAS WRITTEN runs the comparison, which
  goes red on the eight -- the real defect, not a hook built to make a check
  fire.  Four AFTER patches are also NARROWED to remove the `return` alone
  (`pass` in its place, the `if` left standing), so mutation and declaration
  are the same size by construction as well as by measurement.

  AND THE LAST SECTION ENUMERATES THE WAYS THIS REPAIR COULD BE THE DEFECT IT
  REPAIRS -- a derived declaration has a grain, a sweep has a grain, a pin has
  a provenance -- with each branch either checked by a claim here or given the
  reason it cannot arise.

WHAT mg-0b07 FOUND IN THIS FILE, and it is why the file was rewritten A FOURTH
TIME (mg-f7e1).

  `clause` WAS NOT THE FLOOR, AND THE PREVIOUS ANSWER HAD REMOVED THE HANDLE
  RATHER THAN THE RUNG.  mg-64b6 wrote the `shape` condition as `[len(row) for
  row in A] != [len(row) for row in B]` and this file reported, correctly, that
  `absorb_trace` had 0 deciding clauses left and that the regress therefore
  stopped by construction.  A list comparison IS a disjunction -- true when the
  LENGTHS differ or a common index does -- so the ORDER half was still there,
  and mg-0b07 perturbed it: width half standing, order half gone, artifact
  BYTE-IDENTICAL at 23,695, exit 0, every row green.  Rung two's sentence with
  `clause` replaced by `sub-condition`, one spelling further down.

  THE SUBTRACTION MOVE IS MADE ON THE IMPLICITNESS, NOT ON THE CONDITION.  The
  guard now spells its disjunction with an `or`, so both halves are operands
  the ENUMERATED sweep already runs deletes individually -- no new technique,
  two more rows in a table that was already there.  The sweep measures the
  width clause CHANGES/exit 1 and the ORDER clause BYTE-IDENTICAL/exit 0, and
  the second result is PRINTED AS AN UNCOVERED CLAUSE on the line it is read
  on, with the difference between INERT and UNCOVERED stated: the order half
  moves decisions on real inputs, and nothing in `controls.py` reaches it.

  AND THE BOUND OF THE INSTRUMENT IS STATED BESIDE THE TEST, because respelling
  does not terminate -- `any(a != b for ...)` is a disjunction over rows with no
  operator either.  The section THE BOUND OF THIS INSTRUMENT counts, from the
  tree, the deciding conditions that are compounds this sweep cannot delete out
  of, and carries a total that does not depend on the list of forms it knows
  about.  DELETION ESTABLISHES COVERAGE DOWN TO EXPLICIT BOOLEAN OPERANDS AND NO
  FURTHER.  A green line that a reader takes for more than that is the defect;
  the number is the remedy.

EVERY CLAIM PRINTS WHAT WOULD MAKE IT ANSWER DIFFERENTLY (mg-d0e2's added
requirement).  "Can this check fire?" is necessary and not sufficient: both
vacuous checks this repository produced in one afternoon could fire in
principle, and each was blind to the specific defect it was read as guarding.
Naming the change forces the question of whether that change is the failure.

Nothing under ../face_geometry is written: every mutation is applied to a copy
in a temporary directory, and every battery run captures stdout rather than
tee-ing it.
"""

import ast
import collections
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kern5f9a import (                                              # noqa: E402
    BAR, FG, PRE_REPAIR_REF, TWO_RETURN_REF, apply_edits, condition_census,
    deciding_clauses, drop_clause, finest_unit, head, implicit_disjunctions,
    load_module, mutate_tree, run_controls, source_at, tree_with_source,
    unit_removed, write_ref_tree,
)

SCORE = []

HERE = os.path.dirname(os.path.abspath(__file__))
POSITIVE_CONTROL = os.path.join(HERE, "positive_control_all_fail.txt")

NEW_FILES = ["face_complex.py", "posets.py", "controls.py", "run_probe.py"]
PRE_FILES = ["face_complex.py", "posets.py", "controls.py"]

MARKERS = ("[PASS]", "[FAIL]", "[CANNOT FAIL]")

# ----------------------------------------------------------------- this tree
# EACH OF THESE REMOVES A `return` AND LEAVES THE `if` THAT GUARDED IT STANDING
# (mg-64b6).  mg-9220's versions deleted the guard with its return -- one return
# and one `if`, declared as "one `return` statement" -- which is mg-c4c8's F2:
# the patch was a larger unit than the sentence beside it.  Substituting `pass`
# for the return alone makes the mutation and its declaration the same size BY
# CONSTRUCTION rather than by proofreading, which is the fix that audit named as
# preferable.  Every artifact verdict and exit code is unchanged by the
# narrowing; mg-c4c8's H1 ran exactly these four (its returns #46, #47, #48 and
# #50, each replaced by `pass`) and reports the same verdicts the wider patches
# gave.
NEW_DIAG = ('face_complex.py',
            '            return Trace(False, "diagonal", 0)\n',
            '            pass\n')
NEW_MAG = ('face_complex.py',
           '                return Trace(False, "magnitude", 0)\n',
           '                pass\n')
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
# The two mg-d0e2 found invisible.  THE SHAPE GATE IS ONE `return` GUARDED BY A
# TWO-CLAUSE DISJUNCTION: mg-9220 merged the two returns this mutation used to
# delete together (deleting the first of them ALONE moved not one byte,
# mg-e7bc), mg-64b6 rewrote the merged two-clause condition as a single
# comparison of row-shape profiles (deleting its first CLAUSE alone moved not
# one byte either, mg-c4c8), and mg-0b07 found that the comparison was STILL a
# disjunction with its order half unperturbable -- so the `or` is back, spelled
# (mg-f7e1), and the two halves are swept individually below.  This patch
# removes exactly the `return`, and the sweep is what speaks for the condition.
NEW_SHAPE = ('face_complex.py',
             '        return Trace(False, "shape", 0)\n',
             '        pass\n')

# THE TEXT THIS COMMIT REPLACES, as a computed mutation rather than a new pin.
# The equivalence that has to hold is between two spellings of one condition, and
# both are in this tree: the live one, and this patch's result.  A pin would be a
# third thing with a provenance of its own to check (see the MERGED_REF walk
# below for what that costs); an anchor that must occur exactly once is checked
# by `mutate_tree` on every run.
RESPELL_BACK = ('face_complex.py',
                '    shape_A = [len(row) for row in A]\n'
                '    shape_B = [len(row) for row in B]\n'
                '    if len(shape_A) != len(shape_B) or any(\n'
                '            a != b for a, b in zip(shape_A, shape_B)):\n',
                '    if [len(row) for row in A] != [len(row) for row in B]:\n')
NEW_PARITY = ('face_complex.py',
              '                    return Trace(False, "parity", signs_read)\n',
              '                    pass\n')

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

# EVERY MUTATION, WITH THE TREE IT RUNS ON AND WHAT IT IS AIMED AT -- AND NO
# UNIT.  The unit is DERIVED (mg-64b6): `declared` below computes it from this
# patch and this tree, so the sentence a reader consults cannot be a smaller
# thing than the patch.  mg-9220 wrote the units by hand and 8 of its 11
# understated their own patches (mg-c4c8 F2); the shipped sentences are kept
# verbatim in `UNITS_AS_SHIPPED` and the section THE DECLARATION THAT WAS
# WRITTEN runs the comparison on them.
#
# The REF and the FILES live here too, beside the patch, because the declaration
# is only honest if it is computed from the source the battery actually mutates:
# two places naming the tree is two places that can disagree, which is this
# file's own defect wearing a different hat.
#
# The `aim` is NOT a size.  It says what the mutation is for; every quantity on
# the result line is computed.  A wrong aim is possible and nothing here catches
# it -- catching it would be a parse of English, which is the apparatus this
# repair removes rather than adds.
MUTATIONS = [
    ("BEFORE-1", PRE_REPAIR_REF, PRE_FILES, [PRE_DIAG],
     "the s_i^2 = 1 gate of the PRE-REPAIR predicate -- mg-1c80's M2, the "
     "deletion that regenerated the artifact byte-identically"),
    ("BEFORE-2", PRE_REPAIR_REF, PRE_FILES, [PRE_MAG],
     "the |s_i s_j| = 1 gate of the same tree -- mg-1c80's M1"),
    ("AFTER-1", None, NEW_FILES, [NEW_DIAG], "gate `diagonal` of `absorb_trace`"),
    ("AFTER-2", None, NEW_FILES, [NEW_MAG], "gate `magnitude`"),
    ("AFTER-3", None, NEW_FILES, [NEW_ORDER],
     "the ORDER of two gates: row i's magnitudes tested before row i's "
     "diagonal, nothing deleted"),
    ("AFTER-4", None, NEW_FILES, [NEW_SIGNS],
     "the counter that reports how many signs the union-find read"),
    ("AFTER-5", None, NEW_FILES, [NEW_SHAPE],
     "gate `shape` -- the branch mg-d0e2 found invisible, whose two returns "
     "mg-9220 merged, whose two clauses mg-64b6 rewrote as one comparison, and "
     "whose disjunction mg-f7e1 spelled back out with an operator"),
    ("AFTER-6", None, NEW_FILES, [NEW_PARITY],
     "the `parity` contradiction branch -- the other branch mg-d0e2 found "
     "invisible"),
    ("R1", TWO_RETURN_REF, NEW_FILES, [OLD_SHAPE_1],
     "the FIRST of the pinned tree's two `shape` returns, alone -- mg-e7bc's "
     "finding, reproduced against the tree it is about"),
    ("R2", TWO_RETURN_REF, NEW_FILES, [OLD_SHAPE_2], "the SECOND of them, alone"),
    ("R3", TWO_RETURN_REF, NEW_FILES, [OLD_SHAPE_1, OLD_SHAPE_2],
     "BOTH of them together, which is what AFTER-5 did until mg-9220.  KEPT "
     "DELIBERATELY as the specimen"),
]

SPECIMEN_TAGS = ("R3",)
"""The mutation that removes two returns, kept rather than fixed.

The same treatment `vacuous_check_as_shipped` gives the shipped label check: the
defect is kept where it can be run, because a bundled deletion whose result was
read one level down is easier to recognise beside the un-bundled pair than in a
paragraph about it.  It is excluded from the at-most-one claim BY NAME, so a new
mutation that bundles two returns is BROKEN rather than quietly tolerated.
"""

# mg-9220's DECLARATIONS, VERBATIM, kept as the specimen for the section that
# measures them -- the treatment `vacuous_check_as_shipped` gives the shipped
# label check and `R3` gives the bundled deletion.  The triple beside each is
# mg-c4c8's H4 READING of that sentence: what the sentence would have to remove
# for the declaration to be exact, written down by that audit beside the prose it
# read.  It is QUOTED here, not re-derived: a machine reading of English is a
# claim, and re-inventing one would be this file grading its own homework.
UNITS_AS_SHIPPED = [
    ("BEFORE-1", (0, 0, 1),
     "one CLAUSE of a compound condition (`or A[i][i] != B[i][i]`); the "
     "`return` it guards stays and still answers on the other clause"),
    ("BEFORE-2", (1, 0, 0), "one `return` statement -- the magnitude gate"),
    ("AFTER-1", (1, 0, 0), "one `return` statement -- gate `diagonal`"),
    ("AFTER-2", (1, 0, 0), "one `return` statement -- gate `magnitude`"),
    ("AFTER-3", (0, 0, 0),
     "NO statement: the ORDER of two gates, both returns kept"),
    ("AFTER-4", (0, 1, 0),
     "one statement, and not a `return`: the `signs_read += 1` counter"),
    ("AFTER-5", (1, 0, 0),
     "one `return` statement -- gate `shape`, which is ONE return since "
     "mg-9220 merged the two"),
    ("AFTER-6", (1, 0, 0),
     "one `return` statement -- the `parity` contradiction branch"),
    ("R1", (1, 0, 0),
     "one `return` statement -- the FIRST of the pinned tree's two `shape` "
     "returns"),
    ("R2", (1, 0, 0), "one `return` statement -- the SECOND of them"),
    ("R3", (2, 0, 0),
     "TWO `return` statements -- the PAIR, which is what AFTER-5 removed until "
     "mg-9220.  KEPT DELIBERATELY as the specimen"),
]

# THE PATCHES THOSE SENTENCES WERE WRITTEN FOR, kept with them.  Four of the
# eleven are narrower now (mg-64b6 substitutes `pass` for the return instead of
# deleting the guarded `if`), so measuring the shipped sentences against
# TODAY's patches would report this commit's improvement as mg-9220's defect.
# The comparison below therefore applies mg-9220's own patch text.
SHIPPED_PATCHES = {
    "AFTER-1": [('face_complex.py',
                 '        if A[i][i] != B[i][i]:\n'
                 '            return Trace(False, "diagonal", 0)\n', '')],
    "AFTER-2": [('face_complex.py',
                 '            if abs(A[i][j]) != abs(B[i][j]):\n'
                 '                return Trace(False, "magnitude", 0)\n',
                 '            pass\n')],
    "AFTER-5": [('face_complex.py',
                 '    m = len(A)\n'
                 '    if m != len(B) or any(len(A[i]) != len(B[i]) '
                 'for i in range(m)):\n'
                 '        return Trace(False, "shape", 0)\n'
                 '    for i in range(m):\n',
                 '    m = len(A)\n'
                 '    for i in range(m):\n')],
    "AFTER-6": [('face_complex.py',
                 '            if ri == rj:\n'
                 '                if pi ^ pj != need:\n'
                 '                    return Trace(False, "parity", '
                 'signs_read)\n'
                 '            else:\n',
                 '            if ri == rj:\n'
                 '                pass\n'
                 '            else:\n')],
}

# The tree mg-9220's AFTER patches applied to: the last commit whose
# `absorb_trace` has a two-CLAUSE `shape` condition -- which is mg-9220's own
# repair commit, the one that created the condition mg-c4c8 then found the
# first clause of inert.  Pinned for the reason `PRE_REPAIR_REF` gives, and
# checked against the history below rather than asserted: that is the floor
# item mg-c4c8 ran on `TWO_RETURN_REF`, applied to the pin this commit adds.
MERGED_REF = "b6bc2ef"


def source_for(tag):
    """The exact source text `tag`'s patch is applied to."""
    for name, ref, _files, _edits, _aim in MUTATIONS:
        if name == tag:
            return source_at(ref)
    raise SystemExit("%s: no MUTATIONS entry" % tag)


def entry(tag):
    for row in MUTATIONS:
        if row[0] == tag:
            return row
    raise SystemExit("%s: no MUTATIONS entry -- a deletion result with no "
                     "patch beside it is what mg-e7bc found (mg-9220)" % tag)


def declared(tag):
    """THE DECLARED UNIT, DERIVED FROM THE PATCH (mg-c4c8 OPEN 2).

    Not written down and not checked against the patch afterwards: computed
    from it, by parsing the tree before and after the mutation.  A declaration
    that is computed cannot disagree with the patch, and it is correct at
    whatever grain the patch operates at without anyone deciding in advance
    which grain that is -- which is what ends the gate -> return -> clause
    regress rather than descending it one more rung.
    """
    _name, ref, _files, edits, _aim = entry(tag)
    return unit_removed(source_at(ref), edits)

# THE REGISTERED EXPECTATION, written before the runs.  The fail-set is the half
# that makes the label check non-vacuous: it says WHICH rows must read [FAIL],
# by a substring of the row's own text, so a mutation that ought to break a row
# and does not is a BROKEN claim rather than a stable pair of labels.
PREDICTIONS = [
    ("BEFORE-1", "pre-repair tree: delete the s_i^2 = 1 gate (mg-1c80's M2)",
     "artifact BYTE-IDENTICAL, exit 0 -- the finding this landing answers"),
    ("BEFORE-2", "pre-repair tree: delete the |s_i s_j| = 1 gate (mg-1c80's M1)",
     "artifact CHANGES, exit 1 -- that gate is what forbids I4's antichains"),
    ("AFTER-1*", "this tree: delete the s_i^2 = 1 gate's RETURN, `if` kept",
     "artifact CHANGES, exit 0, NO row fails -- no decision moves, the trace does"),
    ("AFTER-2", "this tree: delete the |s_i s_j| = 1 gate's RETURN, `if` kept",
     "artifact CHANGES, exit 1, the brute-force instrument row fails (*)"),
    ("AFTER-3*", "this tree: test row i's magnitudes BEFORE row i's diagonal",
     "artifact CHANGES, exit 0, NO row fails -- same answers, different trace"),
    ("AFTER-4", "this tree: stop counting the signs the union-find reads",
     "artifact CHANGES, exit 0, NO row fails"),
    ("AFTER-5", "this tree: delete the ONE `shape` return, `if` kept (mg-d0e2 O1)",
     "artifact CHANGES, exit 1, the `shape` branch row fails -- it was invisible"),
    ("AFTER-6", "this tree: delete the `parity` contradiction RETURN (ditto)",
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
# THE CLAUSE SWEEP'S REGISTERED EXPECTATIONS, keyed by (function, kind, index)
# so the table cannot be silently re-ordered under them, and a clause with no
# entry is BROKEN rather than skipped.  (changes?, exit, why).
#
# NINE OF THESE ELEVEN WERE RUN BY mg-c4c8's H2 on the tree mg-64b6 started
# from, and every one was BYTE-IDENTICAL at exit 0.  That is said here rather
# than presented as foresight.
#
# AND SO WERE THE TWO NEW ONES, BY mg-0b07, BEFORE THE OPERATOR EXISTED (its p3,
# rows S2 and S1).  That audit perturbed the one-comparison condition's two
# MEANINGS by splicing each half in alone; this commit spells them as two
# OPERANDS, so the same two experiments are now deletions of clauses and the sweep
# runs them without being told they exist.  Registering the numbers that audit
# published is not foresight and is not offered as any: what is new here is that
# the sweep REACHES them.  If they came back other than as registered, the
# spelling would not be equivalent to the comparison and the section below --
# which measures exactly that -- would go red with them.
CLAUSE_PRED = {
    ("absorb_trace", "guard", 0): (False, 0,
                                   "mg-0b07 p3 S2, the ORDER half: no pair in "
                                   "the battery has len(A) != len(B) without "
                                   "also being ragged, so the width clause "
                                   "rejects them unaided.  UNCOVERED, NOT "
                                   "INERT -- cut it and the predicate answers "
                                   "ABSORBABLE for a 2x2 against a three-row B "
                                   "whose first two rows are 2 wide"),
    ("absorb_trace", "guard", 1): (True, 1,
                                   "mg-0b07 p3 S1, the WIDTH half: the `shape` "
                                   "row's second constructed pair is RAGGED at "
                                   "the same order, and nothing else rejects "
                                   "it"),
    ("gate_violations", "guard", 0): (False, 0,
                                      "mg-c4c8 H1 #52: this return is inert "
                                      "WHOLE, so no clause of its guard can "
                                      "move the artifact"),
    ("gate_violations", "guard", 1): (False, 0, "ditto -- inert whole"),
    ("diagonal_moves", "guard", 0): (False, 0,
                                     "mg-c4c8 H1 #54: inert whole, for the "
                                     "same reason -- controls.py's own shape "
                                     "guard `continue`s first"),
    ("diagonal_moves", "guard", 1): (False, 0, "ditto -- inert whole"),
    ("Poset.leq", "value", 0): (False, 0,
                                "mg-c4c8 H1 #2: no call site in the battery"),
    ("Poset.leq", "value", 1): (False, 0, "ditto -- no call site"),
    ("Poset.comparable", "value", 0): (False, 0,
                                       "mg-c4c8 H1 #3: inert whole"),
    ("Poset.comparable", "value", 1): (False, 0, "ditto -- inert whole"),
    ("Poset.comparable", "value", 2): (False, 0, "ditto -- inert whole"),
}

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


def run_case(tag, desc, baseline, base_code, want_change, want_exit,
             want_fail_subs, baseline_cannot=()):
    """Run `tag`'s mutation and score it.  The tree, the files and the patch all
    come from `MUTATIONS`, so the source the declaration is derived from is the
    source the battery runs on -- and that is CHECKED here rather than asserted:
    the mutated file is read back off disk and compared with the text the
    declaration was computed from."""
    _name, ref, tree_files, edits, aim = entry(tag)
    if ref is not None:
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
    src = source_at(ref)
    unit = unit_removed(src, edits)
    on_disk = open(os.path.join(cwd, edits[0][0])).read()
    same_tree = on_disk == apply_edits(src, edits)
    # THE GRANULARITY IS PRINTED WHERE THE RESULT IS READ (mg-e7bc, mg-9220),
    # AND IT IS DERIVED FROM THE PATCH RATHER THAN WRITTEN (mg-c4c8, mg-64b6).
    # "The artifact changes when X is deleted" is a claim about X at the size X
    # was deleted at.  AFTER-5 used to remove two `return`s and be read as a
    # statement about each; then it removed a return, an `if` and a two-clause
    # condition and declared "one `return` statement".  Both readings are
    # impossible to make silently once the size is computed from the patch and
    # printed on the line the result is read on.
    claim("%s -- %s: artifact %s (predicted %s), exit %d (predicted %d)  "
          "[UNIT REMOVED, DERIVED FROM THE PATCH: %s]"
          % (tag, desc, "CHANGES" if changed else "BYTE-IDENTICAL",
             "CHANGES" if want_change else "BYTE-IDENTICAL", code, want_exit,
             unit.text),
          changed == want_change and code == want_exit and same_tree,
          "deleting a gate that no row's answer depends on -- which is what "
          "AFTER-5 and AFTER-6 used to be, and what BEFORE-1 still is.  AND "
          "under this line being read at a granularity finer than the unit "
          "above, which is why the FINEST UNIT is printed with it",
          "%d bytes out vs %d baseline; unmutated baseline exited %d.  AIMED "
          "AT: %s.  FINEST UNIT THIS LINE PERTURBS: %s.  The file the battery "
          "ran on %s the source this unit was derived from"
          % (len(out), len(baseline), base_code, aim, finest_unit(unit),
             "IS byte-for-byte" if same_tree else "DIFFERS FROM"))
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
    print("(repaired by mg-64b6: PER CLAUSE, and the unit DERIVED from the "
          "patch rather than written)")
    print(BAR)
    print("\nPREDICTIONS, registered before the runs:")
    for tag, desc, pred in PREDICTIONS:
        print("   %-9s %-62s %s" % (tag, desc, pred))
    print("\n   (*) %s's fail-set was registered as %r and that was WRONG: %s."
          % MISREGISTERED)
    print("       The registration above is the corrected one; the miss is kept "
          "here rather than\n       edited away, and the label check below is "
          "what caught it.")

    head("THE UNIT EVERY MUTATION REMOVES -- DERIVED FROM ITS OWN PATCH")
    print("mg-e7bc: the deletion test was applied at the granularity of a GATE "
          "and read at\nthe granularity of a RETURN.  mg-9220 required every "
          "mutation to DECLARE its unit,\nand wrote the declarations: 8 of the "
          "11 then said 'one `return` statement' for a\npatch that removed the "
          "`return` TOGETHER WITH THE `if` THAT GUARDS IT, one of them\nwith a "
          "two-clause condition inside (mg-c4c8 F2).  A declaration that "
          "understates\nits patch makes the deletion evidence look finer-"
          "grained than it is, and it does so\ninvisibly, because the "
          "declaration is what a reader consults instead of the diff.\n")
    print("NOTHING IN THE TABLE BELOW IS WRITTEN DOWN.  Each row is computed by "
          "parsing the\ntree the mutation runs on, before and after its own "
          "patch.  A computed declaration\nCANNOT disagree with its patch, and "
          "it is correct at whatever grain the patch\noperates at -- which is "
          "what ends the gate -> return -> clause regress instead of\n"
          "descending it one more rung.  `nodes` is every syntax-tree node the "
          "patch removes,\nof any kind: the three named units are three CHOSEN "
          "grains and `nodes` is the\nchannel that has none, so a patch that "
          "removes syntax none of the three names is\nvisible here rather than "
          "reported as 0/0/0.\n")
    print("   %-9s %-4s %-4s %-4s %-6s %s"
          % ("tag", "ret", "stmt", "cls", "nodes", "derived declaration"))
    multi, unnamed = [], []
    derived = [(t, declared(t)) for t, _r, _f, _e, _a in MUTATIONS]
    graded = [(t, u) for t, u in derived if t not in SPECIMEN_TAGS]
    for tag, u in derived:
        if u.returns > 1 and tag not in SPECIMEN_TAGS:
            multi.append((tag, u.returns))
        if u.nodes != 0 and (u.returns, u.statements, u.clauses) == (0, 0, 0):
            unnamed.append((tag, u.nodes))
        print("   %-9s %-4d %-4d %-4d %-6d %s%s"
              % (tag, u.returns, u.statements, u.clauses, u.nodes,
                 "SPECIMEN -- " if tag in SPECIMEN_TAGS else "", u.text))
    claim("no mutation in this file removes more than one `return` statement, "
          "the specimen %s aside -- %d of %d remove exactly one, %d remove none "
          "(a clause, an ordering and a counter), %d remove more"
          % (", ".join(SPECIMEN_TAGS),
             sum(1 for _t, u in graded if u.returns == 1), len(graded),
             sum(1 for _t, u in graded if u.returns == 0), len(multi)),
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
             dict(derived)[SPECIMEN_TAGS[0]].returns))
    # AND THE DECLARATION'S OWN GRAIN, which is this file's version of the
    # defect it repairs: `returns`, `statements` and `clauses` are three chosen
    # units, so a patch that removes something finer than a clause -- an
    # operand, a comprehension, an argument -- reports 0/0/0 and understates
    # itself exactly as mg-9220's sentences did.
    claim("AND THE DECLARATION IS NOT COARSER THAN ITS OWN PATCH: every "
          "mutation that removes syntax at all removes some `return`, "
          "statement or clause -- %d of %d, with %d removing no syntax at all "
          "(a reordering removes none)"
          % (len(derived) - len(unnamed)
             - sum(1 for _t, u in derived if u.nodes == 0),
             len(derived), sum(1 for _t, u in derived if u.nodes == 0)),
          not unnamed,
          "a mutation that deletes a clause of a comparison, an argument, or "
          "any sub-expression the three named grains do not name.  It would "
          "print 0 return, 0 statement, 0 clause with a nonzero node count -- "
          "which is THIS declaration understating THIS patch, the defect "
          "mg-c4c8 found one level up, and the reason the node count is here "
          "rather than the three units alone",
          "mutations with nodes removed but nothing named: %s"
          % ("; ".join("%s removes %d node(s)" % (t, n) for t, n in unnamed)
             if unnamed else "none"))

    head("THE DECLARATION THAT WAS WRITTEN, AND WHAT ITS PATCHES REMOVED")
    print("mg-9220's eleven sentences, VERBATIM, against the patches they were "
          "written for --\nthe specimen treatment this file already gives the "
          "vacuous label check and the\nbundled deletion R3.  The triple beside "
          "each sentence is mg-c4c8's H4 reading of\nit, quoted: what that "
          "sentence would have to remove for the declaration to be\nexact.  The "
          "measured column is computed here.\n")
    print("   %-9s %-12s %-12s %s"
          % ("tag", "WRITTEN", "MEASURED", "verdict (r/s/c)"))
    shipped_rows = []
    for tag, reading, sentence in UNITS_AS_SHIPPED:
        _n, ref, _f, edits, _a = entry(tag)
        # The tree mg-9220's patch was written for.  Its AFTER patches applied
        # to a tree whose `shape` gate had a two-CLAUSE condition; this one
        # does not, and measuring its sentences against a tree they were never
        # written for would report this commit's rewrite as their defect.
        if tag.startswith("AFTER"):
            ref = MERGED_REF
        edits = SHIPPED_PATCHES.get(tag, edits)
        u = unit_removed(source_at(ref), edits)
        got = (u.returns, u.statements, u.clauses)
        shipped_rows.append((tag, reading, got, sentence))
        print("   %-9s %-12s %-12s %s"
              % (tag, "%d/%d/%d" % reading, "%d/%d/%d" % got,
                 "exact" if got == reading else "*** UNDERSTATES ***"))
    understating = [r for r in shipped_rows if r[1] != r[2]]
    claim("THE WRITTEN DECLARATIONS UNDERSTATE THEIR OWN PATCHES ON %d OF %d, "
          "REPRODUCED HERE FROM THIS REPOSITORY'S OWN CODE rather than quoted "
          "from the audit: %s.  This is the mismatch the derived declaration "
          "above cannot produce, shown firing on the real defect that motivated "
          "it and not on a hook built to make it fire"
          % (len(understating), len(shipped_rows),
             ", ".join(r[0] for r in understating)),
          len(understating) == 8,
          "mg-9220's sentences being edited, or the patches they were written "
          "for changing under them.  Both are kept frozen here: the four "
          "patches this commit narrowed are applied from SHIPPED_PATCHES, so "
          "the comparison is about mg-9220's work and not about this commit's",
          "; ".join("%s wrote %s and removed %s"
                    % (t, "%d/%d/%d" % w, "%d/%d/%d" % g)
                    for t, w, g, _s in understating))
    # AND THE PROPERTY THAT MAKES THE DERIVATION A FIX rather than a correction:
    # widen a patch and the declaration widens with it, with no sentence edited.
    wide = [('face_complex.py',
             '        return Trace(False, "shape", 0)\n', '        pass\n'),
            ('face_complex.py',
             '            return Trace(False, "diagonal", 0)\n',
             '            pass\n')]
    live = source_at(None)
    narrow_u, wide_u = unit_removed(live, [wide[0]]), unit_removed(live, wide)
    claim("AND THE DERIVED DECLARATION TRACKS THE PATCH: AFTER-5's patch widened "
          "to take out a second `return` declares %d returns instead of %d, "
          "with nothing edited anywhere -- %r becomes %r"
          % (wide_u.returns, narrow_u.returns,
             narrow_u.text[:46], wide_u.text[:46]),
          wide_u.returns == narrow_u.returns + 1
          and wide_u.labels != narrow_u.labels,
          "the declaration ceasing to be a function of the patch -- which is "
          "the state every hand-written declaration is in.  mg-9220's sentence "
          "for AFTER-5 says 'one `return` statement' and goes on saying it "
          "under the widened patch above, which is the whole of mg-c4c8's "
          "OPEN 2 in one line",
          "narrow: %s || widened: %s" % (narrow_u.text, wide_u.text))

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
    run_case("BEFORE-1", "delete the s_i^2 = 1 gate", base_out, base_code,
             want_change=False, want_exit=0, want_fail_subs=None)
    run_case("BEFORE-2", "delete the |s_i s_j| = 1 gate", base_out, base_code,
             want_change=True, want_exit=1, want_fail_subs=None)

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

    a1 = run_case("AFTER-1", "delete the s_i^2 = 1 gate's return",
                  new_base, new_code, True, 0, [], base_cannot)
    run_case("AFTER-2", "delete the |s_i s_j| = 1 gate's return",
             new_base, new_code, True, 1,
             ["the union-find absorbability decision agrees with brute force"],
             base_cannot)
    a3 = run_case("AFTER-3", "magnitudes before the diagonal",
                  new_base, new_code, True, 0, [], base_cannot)
    run_case("AFTER-4", "stop counting signs read",
             new_base, new_code, True, 0, [], base_cannot)
    a5 = run_case("AFTER-5", "delete the one `shape` return",
                  new_base, new_code, True, 1,
                  ["the predicate's `shape` branch"], base_cannot)
    a6 = run_case("AFTER-6", "delete the `parity` contradiction branch",
                  new_base, new_code, True, 1,
                  ["the predicate's `parity` branch"], base_cannot)
    # AFTER-5'S SITE, SAID WHERE AFTER-5 IS READ (mg-0b07 B1).  The FINEST UNIT
    # on the line above is the finest unit of the PATCH and is exact.  The
    # finest unit of the SITE is smaller, and a reader who takes the one for the
    # other reads this line as covering the condition it leaves standing.
    shape_guard = [cl for cl in deciding_clauses(source_at(None))
                   if cl.func == "absorb_trace"]
    print("   AFTER-5's SITE, WHICH IS NOT ITS PATCH: the `return` it removes "
          "is guarded by a\n   condition of %d clause(s) -- %s.  This line "
          "covers neither of them; each is\n   deleted alone in the section PER "
          "CLAUSE below, where one of the two comes back\n   BYTE-IDENTICAL and "
          "is printed as NOT COVERED.\n"
          % (len(shape_guard),
             "; ".join("`%s`" % " ".join((cl.source or "").split())
                       for cl in shape_guard)))

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
                  two_base, two_code, False, 0, None)
    run_case("R2", "delete ONLY the second `shape` return (ragged rows)",
             two_base, two_code, True, 1, None)
    run_case("R3", "delete BOTH, as AFTER-5 used to",
             two_base, two_code, True, 1, None)
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

    head("AND NEITHER REWRITE QUIETLY NARROWED THE GATE")
    print("The first return was not cut, it was MERGED into the second's "
          "condition (mg-9220),\nand the two clauses of that condition were then "
          "rewritten as ONE comparison of the\ntwo row-shape profiles "
          "(mg-64b6).  Cutting a clause is not the same edit as saying\nthe same "
          "thing without one, and the difference is measured rather than argued: "
          "the\nthree pairs below separate them, and R1's battery run cannot see "
          "any of them.  Three\nimplementations are loaded side by side -- the "
          "pinned tree's two-return\n`absorb_trace`, this tree's one-clause one, "
          "and the pinned one with its first\nreturn CUT and nothing put in its "
          "place.  The merged two-clause form joins them in\nthe PER CLAUSE "
          "section below.\n")
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

    # ------------------------------------------------------------------------
    head("PER CLAUSE -- the level below a `return`, and the last one here")
    print("mg-c4c8: the granularity error recurred ONE LEVEL FINER, in the "
          "statement mg-9220\nwrote.  The two returns became TWO CLAUSES of one "
          "condition, and DELETING THE FIRST\nCLAUSE ALONE MOVED NOT ONE BYTE -- "
          "the same sentence as mg-e7bc's with `return`\nreplaced by `clause`.  "
          "Gate -> return -> clause is three rungs of one regress.\n")
    print("mg-0b07: AND THAT WAS NOT THE FLOOR EITHER.  mg-64b6 answered the "
          "third rung by\nwriting the condition as one comparison of two lists "
          "and reporting 0 clauses left.\nA list comparison IS a disjunction -- "
          "true when the LENGTHS differ or a common\nindex does -- so the ORDER "
          "half survived with no operand to delete, and taking it\nout with the "
          "width half standing left the artifact BYTE-IDENTICAL at 23,695, exit "
          "0.\nMERGING HAD REMOVED THE HANDLE, NOT THE RUNG.\n")
    print("SO THE OPERATOR IS BACK, AND THAT IS THE SUBTRACTION MOVE APPLIED TO "
          "THE\nIMPLICITNESS (mg-f7e1).  Both halves are now operands this "
          "sweep deletes one at a\ntime, so a level the instrument could not see "
          "became one it can -- and what it\nsees is printed, including where it "
          "sees nothing.  The sweep is over the\nENUMERATED clauses of the "
          "predicate layer, so a clause added tomorrow is swept\nwithout anyone "
          "adding it to a list, and a clause with no registered prediction is\n"
          "BROKEN here rather than skipped.  What deletion CANNOT reach is "
          "counted in the\nnext section rather than left as the reader's "
          "assumption.\n")
    live_src = source_at(None)
    live_clauses = deciding_clauses(live_src)
    poset_src = source_at(None, "posets.py")
    poset_clauses = deciding_clauses(poset_src)
    print("  population, read from the tree: %d clause(s) in face_complex.py, "
          "which is\n  mg-c4c8's H2 population and the file every mutation in "
          "this instrument patches" % len(live_clauses))
    for cl in live_clauses:
        print("      %-24s %-6s clause %d of %d   %s"
              % (cl.func, cl.kind, cl.index + 1, cl.total, cl.source))
    print("  NOT SWEPT, and named rather than left out silently: posets.py has "
          "%d more\n  deciding clause(s) (%s).  They are outside the predicate "
          "layer this deletion\n  test mutates, and no claim here covers them."
          % (len(poset_clauses),
             ", ".join("%s c%d" % (cl.func, cl.index + 1)
                       for cl in poset_clauses)))
    print("\nPREDICTIONS, registered before the runs.  Nine of these eleven "
          "were run by\nmg-c4c8's H2 and every one was IDENTICAL; the two on "
          "`absorb_trace` were run by\nmg-0b07's p3 as perturbations of the "
          "one-comparison condition's two MEANINGS,\nbefore either was an "
          "operand.  Both facts are said here rather than presented as\n"
          "foresight.  mg-c4c8's own two clauses, which mg-64b6 removed, are "
          "run below\nagainst the PINNED tree that still has them.\n")
    for key in sorted(CLAUSE_PRED):
        ch, ex, why = CLAUSE_PRED[key]
        print("   %-24s %-6s c%d  %-10s exit %d   (%s)"
              % (key[0], key[1], key[2] + 1,
                 "CHANGES" if ch else "IDENTICAL", ex, why))
    print()
    print("   %-24s %-6s %-4s %-10s %-5s %-6s %s"
          % ("function", "kind", "cls", "artifact", "exit", "match",
             "what the result establishes about the clause"))
    sweep, sweep_hits = [], 0
    for cl in live_clauses:
        key = (cl.func, cl.kind, cl.index)
        if key not in CLAUSE_PRED:
            sweep.append((key, None, None, False))
            print("   %-24s %-6s %-4d NO PREDICTION REGISTERED"
                  % (cl.func, cl.kind, cl.index + 1))
            continue
        want_change, want_exit, _why = CLAUSE_PRED[key]
        out, code = run_controls(tree_with_source(
            "face_complex.py", drop_clause(live_src, cl), NEW_FILES))
        changed = out != new_base
        ok = (changed == want_change) and (code == want_exit)
        sweep_hits += ok
        sweep.append((key, changed, code, ok))
        # WHAT THE RESULT ESTABLISHES, on the line the result is read on
        # (mg-0b07).  A sweep that prints only IDENTICAL/CHANGES is read as
        # coverage in both directions, and it is coverage in one: a clause whose
        # deletion moves nothing has been REACHED by the test and not COVERED by
        # it, and the two are one column apart.
        print("   %-24s %-6s %-4d %-10s %-5d %-6s %s"
              % (cl.func, cl.kind, cl.index + 1,
                 "CHANGES" if changed else "IDENTICAL", code,
                 "match" if ok else "MISS",
                 "the battery covers this clause"
                 if changed else "NOT COVERED -- deletion establishes nothing "
                 "about it"))
    claim("THE CLAUSE SWEEP RAN ON THE ENUMERATED POPULATION: %d clause(s) of "
          "the predicate layer, each deleted ALONE with the rest of its "
          "condition and its statement left standing, %d of %d predictions "
          "matched" % (len(sweep), sweep_hits, len(sweep)),
          sweep_hits == len(sweep) and len(sweep) > 0,
          "a clause appearing in the predicate layer with no prediction beside "
          "it -- which is BROKEN here rather than skipped, because a population "
          "read from the tree and a table of expectations written by hand are "
          "two things that can disagree, and the tree is the one that is right",
          "; ".join("%s %s c%d %s"
                    % (k[0], k[1], k[2] + 1,
                       "-" if ch is None else ("CHANGES" if ch else "IDENTICAL"))
                    for k, ch, _c, _ok in sweep))
    fc_bool = sum(1 for cl in live_clauses if cl.func == "absorb_trace")
    nested = [cl for cl in live_clauses + poset_clauses
              if isinstance(cl.node.values[cl.index], ast.BoolOp)]
    fc_rows = [(k, ch, c) for k, ch, c, _ok in sweep if k[0] == "absorb_trace"]
    uncovered = [k for k, ch, _c in fc_rows if ch is False]
    claim("`absorb_trace`'S `shape` GUARD IS SWEPT AT %d CLAUSE(S), AND %d OF "
          "THEM THE BATTERY CANNOT SEE.  mg-64b6 reported 0 clauses here and "
          "the regress stopping by construction; that count was exact and the "
          "conclusion was wrong, because the comparison it counted was itself a "
          "disjunction (mg-0b07).  The operator is back, both halves are "
          "deleted individually above, and the half no pair reaches is NAMED: "
          "%s"
          % (fc_bool, len(uncovered),
             ", ".join("clause %d" % (k[2] + 1) for k in uncovered) or "none"),
          fc_bool == 2 and len(fc_rows) == 2 and len(uncovered) == 1,
          "a pair reaching the order half being added to `controls.py` -- at "
          "which point clause 1 goes CHANGES, its registered prediction MISSES, "
          "and this claim goes red saying so.  That is the intended way for it "
          "to fail: the number it states is the coverage, not a target.  It "
          "also goes red if the operator is merged away again, which would "
          "return the sweep to reporting 0 clauses at a site that has two",
          "clauses in `absorb_trace`: %d (%s); in `gate_violations`: %d; in "
          "`diagonal_moves`: %d (mg-c4c8 F3's two functions, whose returns are "
          "inert WHOLE and which no commit in this lineage has touched)"
          % (fc_bool,
             "; ".join("c%d %s" % (k[2] + 1, "CHANGES" if ch else "IDENTICAL")
                       for k, ch, _c in fc_rows),
             sum(1 for cl in live_clauses if cl.func == "gate_violations"),
             sum(1 for cl in live_clauses if cl.func == "diagonal_moves")))
    claim("AND THE UNCOVERED CLAUSE IS UNCOVERED AND NOT INERT, which is the "
          "distinction mg-9220's merge turned on and this sweep would otherwise "
          "blur: `%s` decides pairs the battery does not contain, so it cannot "
          "be deleted as a statement that does nothing"
          % (live_clauses[[cl.func for cl in live_clauses].index(
              "absorb_trace")].source if fc_bool else "-"),
          bool(uncovered) and any(cl.func == "absorb_trace"
                                  for cl in live_clauses),
          "that clause becoming genuinely inert -- which would need the width "
          "half to subsume it, and it does not: `zip` stops at the shorter "
          "profile.  The three separator pairs in the section above are the "
          "measurement, and they are run against a brute force rather than "
          "against the predicate",
          "the pairs that separate them are printed in AND NEITHER REWRITE "
          "QUIETLY NARROWED THE GATE above; an inert clause would be removed "
          "here rather than reported, which is what mg-9220 did with the inert "
          "`return`")
    claim("and THE SWEEP'S OWN GRAIN is the tree's: %d of the %d clauses are "
          "themselves boolean expressions, so 'top-level clause' and 'clause' "
          "name the same thing on this population"
          % (len(nested), len(sweep)),
          not nested,
          "a condition of the form `a or (b and c)`, where deleting the second "
          "top-level clause removes two.  The sweep would then be one rung "
          "coarser than the tree it reads -- which is the defect this whole "
          "lineage is about, committed by the instrument written to close it",
          "nested boolean clauses: %s"
          % ("; ".join("%s c%d" % (cl.func, cl.index + 1) for cl in nested)
             if nested else "none"))

    print("\nAND THE SAME SWEEP ON THE TREE THAT STILL HAS THE TWO CLAUSES.  A "
          "sweep in which\nnothing ever goes red is a sweep nobody has tested, "
          "and after this commit the live\ntree has no clause whose deletion "
          "moves anything.  So the two clauses mg-c4c8\nfound are swept at the "
          "pinned commit that has them -- which is both this sweep's\npositive "
          "control and mg-c4c8's F1, reproduced rather than quoted.\n")
    merged_dir, merged_sha = write_ref_tree(NEW_FILES, MERGED_REF)
    merged_base, merged_code = run_controls(merged_dir)
    merged_src = source_at(MERGED_REF)
    merged_clauses = [cl for cl in deciding_clauses(merged_src)
                      if cl.func == "absorb_trace"]
    claim("%s (%s) -- the two-CLAUSE tree regenerates its own artifact, so the "
          "rows below are against a baseline of its own"
          % (MERGED_REF, merged_sha[:7]),
          merged_code == 0 and len(merged_base) > 0,
          "that ref moving, or that tree ceasing to be reproducible",
          "%d bytes regenerated, exit %d; `absorb_trace` has %d deciding "
          "clause(s) there and %d here"
          % (len(merged_base), merged_code, len(merged_clauses), fc_bool))
    # AND THE PIN IS WHAT ITS COMMENT SAYS, walked rather than asserted.  This
    # is the check mg-c4c8 ran on TWO_RETURN_REF as its floor item -- a pinned
    # measurement is worthless if the pin names a different tree than the
    # sentence beside it -- applied here to the pin this commit introduces,
    # because a new pin is a new instance of exactly that exposure.
    hist = subprocess.run(
        ["git", "log", "--format=%H", "--",
         "code/face_geometry/face_complex.py"],
        cwd=repo, capture_output=True, text=True).stdout.split()
    two_clause = []
    for sha in hist:
        try:
            cls = [c for c in deciding_clauses(source_at(sha))
                   if c.func == "absorb_trace"]
        except Exception:                                       # noqa: BLE001
            continue
        if len(cls) == 2:
            two_clause.append(sha)
    resolved = subprocess.run(["git", "rev-parse", MERGED_REF], cwd=repo,
                              capture_output=True, text=True).stdout.strip()
    claim("AND THE PIN IS WHAT IT SAYS IT IS: of the %d commits that ever "
          "touched face_complex.py, %d has/have a two-CLAUSE `shape` condition "
          "in `absorb_trace`, and the NEWEST of them is %s -- which is what %s "
          "resolves to"
          % (len(hist), len(two_clause),
             two_clause[0][:12] if two_clause else "none", MERGED_REF),
          bool(two_clause) and two_clause[0] == resolved,
          "a later commit reintroducing a two-clause condition, or this pin "
          "being moved to an ancestor.  Either makes the rows above "
          "measurements about a tree the sentence beside them does not "
          "describe -- mg-c4c8's floor item, applied to the pin this commit "
          "adds rather than only to the one it inherited",
          "newest two-clause commit %s; pin resolves to %s; %d two-clause "
          "commit(s) in all"
          % (two_clause[0][:12] if two_clause else "none", resolved[:12],
             len(two_clause)))
    mrows = []
    for cl in merged_clauses:
        root, _s = write_ref_tree(NEW_FILES, MERGED_REF)
        with open(os.path.join(root, "face_complex.py"), "w") as fh:
            fh.write(drop_clause(merged_src, cl))
        out, code = run_controls(root)
        mrows.append((cl, out != merged_base, code, len(out)))
        print("   %-24s clause %d of %d (%s): %-10s exit %d  %d bytes"
              % (cl.func, cl.index + 1, cl.total, cl.source,
                 "CHANGES" if out != merged_base else "BYTE-IDENTICAL", code,
                 len(out)))
    first_inert = mrows and not mrows[0][1] and mrows[0][2] == 0
    second_bites = len(mrows) > 1 and mrows[1][1] and mrows[1][2] == 1
    claim("mg-c4c8's F1 REPRODUCES AT ITS OWN COMMIT: on %s the `shape` "
          "condition has two clauses; deleting the FIRST alone leaves the "
          "artifact BYTE-IDENTICAL at %d bytes, exit 0, and deleting the SECOND "
          "alone CHANGES it, exit 1.  The pair was load-bearing and neither "
          "clause was shown to be -- which is why this commit rewrote the "
          "condition instead of measuring it again"
          % (MERGED_REF, mrows[0][3] if mrows else 0),
          bool(first_inert and second_bites),
          "that ref moving.  AND THIS IS THE SWEEP'S FIRING PATH: the row that "
          "goes red here is produced by the real defect, on the real tree that "
          "had it, not by a corruption built to make a check fire",
          "; ".join("clause %d: %s exit %d" % (cl.index + 1,
                                               "CHANGES" if ch else "IDENTICAL",
                                               code)
                    for cl, ch, code, _b in mrows))

    print("\nWHAT THE FIRST CLAUSE DID, and what the rewrite did to it.  The "
          "clause is not\ninert as a PREDICATE -- cut from the live condition "
          "mg-c4c8 measured it moving\n1,608 decisions.  So it could not be "
          "deleted, and it is not deleted: the\ncondition says the same thing "
          "with no operand to delete.  Both forms are asked\nthe same questions "
          "here, over a population indexed by SHAPE PROFILE, which is what\nthe "
          "condition reads.\n")
    merged_fc = load_module(os.path.join(merged_dir, "face_complex.py"),
                            "fc_merged")
    shapes = [()]
    for a in range(4):
        shapes.append((a,))
        for b in range(4):
            shapes.append((a, b))
            for c in range(4):
                shapes.append((a, b, c))
    profile_mats = [[[((i + j + rule) % 3) - 1 for j in range(w)]
                     for i, w in enumerate(sh)]
                    for sh in shapes for rule in (0, 1)]
    same_outcome = n_pairs = 0
    differ = []
    for A in profile_mats:
        for B in profile_mats:
            n_pairs += 1
            o, n = ask(merged_fc.absorb_trace, A, B), ask(new_fc.absorb_trace,
                                                          A, B)
            same_outcome += (o == n)
            if o != n and len(differ) < 4:
                differ.append(([len(r) for r in A], [len(r) for r in B], o, n))
    claim("THE ONE-CLAUSE CONDITION IS THE TWO-CLAUSE CONDITION: over %d pairs "
          "across %d shape profiles the merged form and this tree's form agree "
          "on the OUTCOME -- decision, gate label and raised exception -- on %d "
          "of %d.  Not 'the same decision': the same answer, by all three "
          "channels" % (n_pairs, len(shapes), same_outcome, n_pairs),
          same_outcome == n_pairs,
          "either form being changed.  This is a stronger statement than the "
          "one mg-9220's merge could make -- that merge moved 126 gate labels "
          "and made a partial function total (mg-c4c8 F5) -- and it has to be, "
          "because a rewrite made to stop a deletion test descending must not "
          "buy that with a behaviour change nobody asked for",
          "population: every row-width tuple of length 0..3 with widths 0..3, "
          "filled two ways -- %d matrices, crossed with itself.  It is indexed "
          "by SHAPE because that is what the condition reads; the entry-indexed "
          "population above cannot separate two shapes that differ in a row "
          "width nobody enumerated.  %s"
          % (len(profile_mats),
             "disagreements: %s" % differ if differ else "no disagreement"))

    # ------------------------------------------------------------------------
    head("THE RESPELLING MOVED NOTHING -- the two texts, asked the same "
         "questions")
    print("mg-f7e1 replaced one comparison of two row-shape profiles with the "
          "`or` that\ncomparison means.  That is a claim about a REWRITE, and "
          "this lineage has one rule\nabout those: measure it.  The patch below "
          "turns the live condition back into\nmg-64b6's text -- an anchor that "
          "must occur exactly once -- and the battery is run\non the result.\n")
    old_dir = mutate_tree([RESPELL_BACK], NEW_FILES)
    old_out, old_code = run_controls(old_dir)
    old_fc = load_module(os.path.join(old_dir, "face_complex.py"), "fc_onecmp")
    claim("THE ONE-COMPARISON FORM REGENERATES THIS TREE'S ARTIFACT BYTE FOR "
          "BYTE: %d bytes, exit %d, against %d and %d live.  The `or` and the "
          "list comparison are the same predicate on everything this battery "
          "asks"
          % (len(old_out), old_code, len(new_base), new_code),
          old_out == new_base and old_code == new_code,
          "either spelling deciding a pair the other does not, which would make "
          "this commit a change to the predicate rather than to its text.  "
          "mg-9220's merge DID move 126 gate labels and make a partial function "
          "total (mg-c4c8 F5); this one is required to move nothing, and the "
          "requirement is checked rather than intended")
    same3 = n3 = 0
    differ3 = []
    for A in profile_mats:
        for B in profile_mats:
            n3 += 1
            o, n = ask(old_fc.absorb_trace, A, B), ask(new_fc.absorb_trace, A, B)
            same3 += (o == n)
            if o != n and len(differ3) < 4:
                differ3.append(([len(r) for r in A], [len(r) for r in B], o, n))
    claim("and over the SAME %d pairs across %d shape profiles the two "
          "spellings agree on decision, gate label AND raised exception on %d "
          "of %d" % (n3, len(shapes), same3, n3),
          same3 == n3,
          "`zip` truncating where the list comparison does not -- which is "
          "exactly the risk this rewrite runs, since the order clause is what "
          "stands in for the length half of `!=`.  Drop `len(shape_A) != "
          "len(shape_B)` and this claim does NOT go red (the artifact is "
          "byte-identical, which is the finding); drop the `zip` guard's "
          "counterpart in the comparison and it does",
          "population indexed by SHAPE PROFILE, %d matrices crossed with "
          "itself.  %s"
          % (len(profile_mats),
             "disagreements: %s" % differ3 if differ3 else "no disagreement"))

    # ------------------------------------------------------------------------
    head("THE BOUND OF THIS INSTRUMENT -- what deletion reaches, and what it "
         "does not")
    print("DELETION ESTABLISHES COVERAGE DOWN TO EXPLICIT BOOLEAN OPERANDS AND "
          "NO FURTHER.\nThat sentence is the whole of mg-0b07's second option "
          "and it is worth nothing as a\npromise, so it is a count.  Four "
          "generations of this file each reported a floor and\neach was one "
          "spelling above the real one; the reason the fifth does not is not "
          "that\nsomebody looked harder, it is that the limit is now MEASURED "
          "and printed beside\nthe green rows rather than inferred from them.\n")
    print("A condition can package several decisions with no operator to "
          "delete: `a < b < c`,\n`[..] != [..]`, `x in S`, `any(...)`.  The "
          "sweep above reaches the operands of `or`\nand `and` and nothing "
          "else.  Below, both populations are read out of the tree.\n")
    print("   %-18s %-6s %-5s %-8s %-9s %s"
          % ("file", "conds", "bool", "operands", "compounds", "expr nodes"))
    for fname in ("face_complex.py", "posets.py"):
        c = condition_census(source_at(None, fname))
        print("   %-18s %-6d %-5d %-8d %-9d %d" % ((fname,) + c))
    fc_census = condition_census(live_src)
    fc_imp = implicit_disjunctions(live_src)
    ps_imp = implicit_disjunctions(poset_src)
    forms = collections.Counter(c.form for c in fc_imp)
    print("\n   the compounds, named -- each is a decision this sweep cannot "
          "delete out of:")
    for fname, pop in (("face_complex.py", fc_imp), ("posets.py", ps_imp)):
        for c in pop:
            print("      %-16s %-24s %-6s %-11s %s"
                  % (fname, c.func, c.kind, c.form,
                     " ".join((c.source or "").split())[:44]))
    claim("THE SWEEP DELETES %d OPERAND(S) OUT OF %d DECIDING CONDITION(S) IN "
          "face_complex.py, AND %d COMPOUND(S) IN THOSE CONDITIONS HAVE NO "
          "OPERAND TO DELETE (%s); posets.py adds %d more, which no claim here "
          "covers.  This is the instrument's bound, stated beside its results: "
          "a green row above covers the clause it names and says nothing about "
          "any decision packed inside that clause"
          % (fc_census[2], fc_census[0], fc_census[3],
             ", ".join("%d %s" % (n, f) for f, n in sorted(forms.items())),
             len(ps_imp)),
          fc_census[3] > 0 and fc_census[2] > 0,
          "every deciding condition becoming a plain boolean expression, at "
          "which point the bound would be vacuous and this claim would say so "
          "by counting 0 compounds.  NOT under the forms being renamed: the "
          "population is enumerated from the tree, and the totals beside it do "
          "not depend on the names",
          "face_complex.py: %d deciding conditions, %d of them boolean, %d "
          "deletable operands, %d unreachable compounds, %d expression nodes in "
          "all.  THE LAST NUMBER HAS NO GRAIN -- it counts every node in every "
          "deciding condition and depends on no classification, so a compound "
          "in a form this file does not know about is inside it anyway, which "
          "is the treatment `unit_removed` gives its own three chosen units"
          % fc_census)
    at_shape = [c for c in fc_imp if c.func == "absorb_trace"]
    old_imp = [c for c in implicit_disjunctions(apply_edits(live_src,
                                                            [RESPELL_BACK]))
               if c.func == "absorb_trace"]
    claim("AND THE CENSUS SEPARATES THE TWO SPELLINGS, so it is measuring the "
          "thing it claims to: on mg-64b6's text `absorb_trace`'s guard is an "
          "unreachable compound (%s) and on this tree it is an `or` with two "
          "deletable operands, with %s left inside the second one -- which is "
          "why the bound is stated and not declared closed"
          % (", ".join(c.form for c in old_imp) or "none",
             ", ".join(c.form for c in at_shape) or "nothing"),
          any(c.form == "sequence" for c in old_imp)
          and not any(c.form == "sequence" for c in at_shape)
          and any(c.form == "quantifier" for c in at_shape),
          "the census reporting the same thing for both texts, which would mean "
          "it cannot see the difference this commit is.  Both readings are of "
          "source text produced in this run: the second is `apply_edits` of the "
          "live source with the same patch the battery ran on above",
          "one-comparison guard: %s || this tree's guard: %s"
          % ("; ".join("%s %s" % (c.form, " ".join((c.source or "").split()))
                       for c in old_imp) or "no compound",
             "; ".join("%s %s" % (c.form, " ".join((c.source or "").split()))
                       for c in at_shape) or "no compound"))
    print("\nWHAT THIS BOUND DOES NOT SAY.  It does not say the uncovered "
          "compounds are wrong,\nor that anything is untested: `absorb_trace` "
          "is checked against a brute force over\nall 2^m sign vectors by a "
          "scored row, and its six returns are individually\ndeletable and "
          "individually visible.  It says what the DELETION EVIDENCE reaches, "
          "so\nthat a reader who wants to know whether a sub-decision is "
          "covered can read the\nanswer instead of assuming it from a green "
          "run.\n")

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

    head("THE WAYS THIS REPAIR COULD BE THE DEFECT IT REPAIRS")
    print("A grain fix has a grain.  A declared unit is a declaration.  Every "
          "remedy in this\nlineage so far has been an artifact of the same kind "
          "as the defect and has\ninherited it: the per-gate test read per "
          "return, the per-return test bit on a\nPAIR OF CLAUSES, and the "
          "declaration invented to make grain self-describing\nunderstated its "
          "own patch on 8 of 11.  So the branches are enumerated here and\n"
          "each is either checked or given the reason it cannot arise.  Where "
          "the check is\nelsewhere in this file it is named rather than "
          "repeated.\n")
    for n, (what, where) in enumerate(SELF_DEFECT_BRANCHES, 1):
        print("  %d. %s\n     %s\n" % (n, what, where))
    checked = [b for b in SELF_DEFECT_BRANCHES if b[1].startswith("CHECKED")]
    claim("the enumeration above is printed with the run, and %d of its %d "
          "branches are checked BY A CLAIM IN THIS FILE rather than by a "
          "sentence -- the %d that are not carry the reason they cannot be"
          % (len(checked), len(SELF_DEFECT_BRANCHES),
             len(SELF_DEFECT_BRANCHES) - len(checked)),
          len(checked) >= 10 and len(SELF_DEFECT_BRANCHES) == 12,
          "nothing: this claim is a pointer to the branches above, and it is "
          "scored so that the list travels with the transcript instead of "
          "living in a document beside it.  The claims that do the work are "
          "the ones named in each branch.  The two counts are computed from "
          "the list rather than written beside it, for the reason every other "
          "number in this file is",
          "branches checked by a claim: the node-count claim (1), the "
          "read-back in every run_case (2), the nested-clause claim (3), the "
          "pinned sweep (4), the shape-profile equivalence (5), the sub-clause "
          "regress (7, answered wrongly by mg-64b6 and re-answered here), the "
          "four narrowed patches (8), the expression-node total (9), the NOT "
          "COVERED marker on the sweep's own rows (10), the respelling "
          "equivalence (11), the uncovered-not-inert claim (12).  Branches "
          "with a stated reason instead: the aim strings (6).  Branch 9 "
          "carries a stated RESIDUE as well as a check, which is the honest "
          "shape for a limit that has a limit")

    print("\n" + BAR)
    print("%d claim(s) scored; %d BROKEN." % (len(SCORE), SCORE.count(False)))
    print(BAR)
    return 1 if not all(SCORE) else 0


# THE WAYS THIS REPAIR COULD BE THE DEFECT IT REPAIRS (mg-64b6).
#
# A grain fix has a grain; a declared unit is a declaration; a pin has a
# provenance.  Every remedy in this lineage so far has been an artifact of the
# same kind as the defect and has inherited it, so the branches are enumerated
# and each is either CHECKED by a claim in this file -- named in the branch --
# or given the reason it cannot arise.  The counts in the claim that prints this
# are computed from the list, for the reason every other number here is.
SELF_DEFECT_BRANCHES = [
        ("The DERIVED DECLARATION has a grain of its own -- `return`, "
         "statement and clause are three CHOSEN units, and a patch that "
         "removes something finer (an operand, an argument, a comprehension) "
         "would print 0/0/0 and understate itself exactly as mg-9220's "
         "sentences did.",
         "CHECKED: every declaration carries `nodes`, the count with no grain "
         "-- every syntax node the patch removes -- and the claim in section 1 "
         "goes red on any mutation with nodes removed and nothing named."),
        ("The declaration could be computed from a DIFFERENT TREE than the one "
         "the battery runs, which is the provenance version of the same "
         "defect: a true sentence about a tree nobody measured.",
         "CHECKED, in every `run_case`: the mutated file is read back OFF DISK "
         "from the directory the battery ran in and compared byte-for-byte "
         "with the text the declaration was derived from.  A mismatch makes "
         "that case's claim BROKEN."),
        ("The CLAUSE SWEEP could be one rung coarser than the tree it reads: "
         "`a or (b and c)` has two top-level clauses and three.",
         "CHECKED: the sweep counts clauses that are themselves boolean "
         "expressions and goes red if any exists (none do)."),
        ("The clause sweep could be a check NOBODY HAS SEEN GO RED, since "
         "after this commit no clause deletion in the predicate layer moves "
         "the artifact.",
         "CHECKED: the same sweep is run against %s, which still has the two "
         "clauses, and it goes red exactly where mg-c4c8 said -- the firing "
         "path is the real defect on the real tree that had it, not a "
         "corruption built to make a check fire." % MERGED_REF),
        ("The population that says the rewrite changed nothing could be blind "
         "to what the rewrite touches, which is what mg-9220's 7,921 pairs "
         "were: every ragged member had rows at least as long as its order, "
         "so the totality change was invisible to it (mg-c4c8 F5).",
         "CHECKED: the equivalence above is measured over a population indexed "
         "by SHAPE PROFILE -- every row-width tuple of length 0..3 -- because "
         "shape is what the condition reads, and it compares the raised "
         "exception as well as the decision and the gate."),
        ("The `aim` strings beside each mutation are prose and could acquire a "
         "size that contradicts the derived unit.",
         "NOT CHECKED, and it cannot be without parsing English -- which is "
         "the apparatus this repair removes rather than adds.  The reason it "
         "is survivable: nothing computes from an aim, the derived unit is "
         "printed on the same line, and the aim names the mutation's PURPOSE "
         "rather than its size."),
        ("The regress could continue below a clause -- an operand of `!=`, a "
         "call, a name.  THIS BRANCH WAS ANSWERED WRONGLY BY mg-64b6 AND THE "
         "ANSWER IS KEPT HERE SO THE CORRECTION IS VISIBLE: 'CANNOT ARISE FOR "
         "THE DELETION TEST -- deleting an operand of a comparison does not "
         "leave a condition, so there is no smaller DELETION at this site.'  "
         "The reason is TRUE and mg-0b07 checked it.  The conclusion does not "
         "follow: it answers 'can anything smaller be DELETED', and the "
         "question this lineage is about is 'can anything smaller be PERTURBED "
         "and go unseen'.  At that very site the two came apart -- the list "
         "comparison's order half was perturbable, uncovered, and had no "
         "operand.",
         "CHECKED, ON THE SECOND ATTEMPT.  The condition is spelled with an "
         "operator so both halves are deletable and both are swept; the "
         "compounds that remain BELOW a clause are counted in THE BOUND OF "
         "THIS INSTRUMENT; and mg-0b07's own perturbation experiment -- which "
         "is not a deletion and is not this file's -- is re-run unmodified "
         "against this tree in d4_auditor_rerun.py."),
        ("THE BOUND ITSELF HAS A BOUND.  `_compound_form` names four ways to "
         "package several decisions with no operator (`or`/`and`, chained, "
         "sequence, membership, quantifier); a fifth form nobody has thought "
         "of counts 0 there exactly as the list comparison counted 0 in the "
         "clause census.  The remedy for an unstated limit is a limit that "
         "can itself be understated.",
         "CHECKED, AND THE CHECK IS NARROWER THAN THE BRANCH -- said plainly.  "
         "`condition_census` reports EXPRESSION NODES IN ALL, an absolute "
         "count over every deciding condition that depends on no "
         "classification, so an unnamed form is inside a printed number rather "
         "than outside every number; and unlike `unit_removed`'s `nodes` it is "
         "a total and not a difference, so mg-0b07's B4 (a size-preserving "
         "substitution hiding in a net) cannot arise for it.  THE RESIDUE: "
         "that total bounds how much is there and does not name what.  A form "
         "nobody names is still not named."),
        ("The bound could be stated in a document beside the run rather than "
         "in it, which is how an instrument's limit becomes something a reader "
         "of the transcript has to already know.",
         "CHECKED: the census, the named compounds and the NOT COVERED marker "
         "are printed in this transcript, and the marker is on the same line "
         "as the sweep result it qualifies rather than in a paragraph above "
         "it."),
        ("The respelling could buy a visible clause with a BEHAVIOUR CHANGE -- "
         "`zip` truncates where `!=` compares lengths, so an order difference "
         "could be lost in the rewrite that was meant only to expose it.",
         "CHECKED TWICE: the one-comparison text is reconstructed by patch in "
         "this run and regenerates the artifact byte for byte, and both forms "
         "are asked decision, gate label and raised exception over the "
         "shape-profile population."),
        ("The uncovered clause could be reported as UNCOVERED when it is "
         "really INERT, which is a category error with a different remedy: an "
         "inert clause should be deleted (mg-9220's move) and only an "
         "uncovered one should be reported.",
         "CHECKED: the separator pairs are run against a brute force that "
         "enumerates every sign vector, and the claim beside the sweep states "
         "which of the two the clause is.  A clause that turned out inert "
         "would be removed here rather than named."),
        ("The four narrowed AFTER patches could have changed what the deletion "
         "test measures while making the declarations exact.",
         "CHECKED: the artifact verdict and exit code of every one is "
         "unchanged, and mg-c4c8's H1 ran the same four narrow patches "
         "independently and reports the same verdicts."),
]


if __name__ == "__main__":
    sys.exit(main())
