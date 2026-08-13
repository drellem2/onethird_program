#!/usr/bin/env python3
"""mg-d3f3 a2 -- IS "TRIPWIRE" THE HONEST WORD?  (PREDICTIONS.md P3)

V6b's row name, printed verbatim into every transcript, asserts:

    "NEGATIVE CONTROL 4 prints 210 formatted values and NO COUNT HAS BEEN ADDED
     OR REMOVED since this table was written ... A TRIPWIRE: it does not check
     that the 12 entries above are the right ones, only that THE SET OF PRINTED
     VALUES HAS NOT MOVED underneath them"

and `verify_e35b.py`'s own docstring says of V6b "RED when a count is added or
removed at the source", and of V6c "a count cannot be added to the artifact
without moving V6b".

WHAT IS ACTUALLY MEASURED is `census(controls_src) == CENSUS_DECLARED`, where
`CENSUS_DECLARED` is a seven-field dict of MULTIPLICITIES:
{specifiers, d, s, fstrings, format_calls, str_calls, nonliteral_mod}.  That is
not "the set of printed values"; it is the multiset of conversion TYPES in one
function.  Two edits separate the name from the measurement, and both are inside
the artifact the sentence is about:

  Y1  ADD AND REMOVE.  Delete one `%d`-bearing print inside
      `negative_control_incidence` and add a different one.  A count was removed
      and a count was added; the multiset is unchanged.  Predicted: V6b green.

  Y2  OUT OF POPULATION.  Add a printed count to `negative_control_construction`
      -- a SIBLING section of the same file whose output is in the same
      artifact.  `controls.py`'s `main()` calls ten sections and
      `controls_output.txt` is all ten.  V6b's population is one of them.
      Predicted: a count is added to the artifact and V6b does not move, which
      contradicts the docstring's claim for V6c word for word.

  Y3  THE WRONG-DIRECTION CONTROL.  Add a printed count INSIDE
      `negative_control_incidence` -- mg-8af0's own C2.  Predicted: V6b red.
      Without Y3, Y1 and Y2 would be equally consistent with a census that never
      fires at all.

WHAT THIS IS NOT.  It is not a claim that the row should have caught these.  A
tripwire on one function is a reasonable instrument and the population is stated
inside `census()`'s docstring, correctly, twice.  It is a claim about the ROW
NAME -- the sentence that reaches the transcript and that a reader scores the
repair by.  "No count has been added or removed" is a stronger sentence than the
row can support, in a repair whose entire subject is a row name that was not its
measurement.

Exit 0 iff the three cells come out as predicted.
"""

import ast
import re
import sys

import lib_d3f3 as L

FN = "negative_control_incidence"
SIBLING = "negative_control_construction"
_SPEC = re.compile(r"%[-#0 +]*[0-9*]*(?:\.[0-9*]+)?([diouxXeEfFgGcrsa%])")


def _fn(src, name):
    return next(f for f in ast.walk(ast.parse(src))
                if isinstance(f, ast.FunctionDef) and f.name == name)


def _one_d_print(src, anchors):
    """A top-level `print("... %d ..." % ...)` in FN, not carrying an anchor."""
    fn = _fn(src, FN)
    for st in fn.body:
        if not (isinstance(st, ast.Expr) and isinstance(st.value, ast.Call)
                and getattr(st.value.func, "id", None) == "print"):
            continue
        args = st.value.args
        if len(args) != 1 or not isinstance(args[0], ast.BinOp):
            continue
        if not isinstance(args[0].op, ast.Mod):
            continue
        if not isinstance(args[0].left, ast.Constant):
            continue
        lit = args[0].left.value
        if [c for c in _SPEC.findall(lit) if c != "%"] != ["d"]:
            continue
        if any(lit[:30] in a or a[:20] in lit for a in anchors):
            continue
        return st.lineno, st.end_lineno, lit
    raise LookupError("no single-%d print available to move")


def y1_add_and_remove(src, anchors):
    lo, hi, lit = _one_d_print(src, anchors)
    lines = src.splitlines(keepends=True)
    fn = _fn(src, FN)
    at = fn.body[-1].end_lineno
    new = ('    print("    * A COUNT ADDED BY mg-d3f3 a2/Y1, carrying exactly '
           'one %d as the one it replaces did" % (len(ps),))\n')
    lines.insert(at, new)
    del lines[lo - 1:hi]                     # after the insert, `at` > `hi`
    return "".join(lines), lit


def y1b_add_and_remove(src):
    """Y1 again, with the collateral removed: the sentence stays, the COUNT goes.

    Y1 deleted a whole `print`, and that print carried the phrase V5's hedge row
    anchors on -- so the verifier exited 1 for a reason that had nothing to do
    with the census.  Y1b removes only the COUNT: the `%d` becomes literal text
    and its operand is dropped, so every anchor in the sentence survives.  A new
    single-`%d` print is added at the end of the section.  Net: one printed count
    removed, one added, and the seven-field census unchanged.
    """
    old = "it covered exactly the %d pairs"
    new = "it covered exactly the (count removed by mg-d3f3 a2/Y1b) pairs"
    assert src.count(old) == 1
    src = src.replace(old, new).replace("          % tot_gauge)\n", "          )\n", 1)
    fn = _fn(src, FN)
    lines = src.splitlines(keepends=True)
    lines.insert(fn.body[-1].end_lineno,
                 '    print("    * A COUNT ADDED BY mg-d3f3 a2/Y1b to replace '
                 'the one removed above: %d posets" % (len(ps),))\n')
    return "".join(lines)


def y2_out_of_population(src):
    fn = _fn(src, SIBLING)
    lines = src.splitlines(keepends=True)
    at = fn.body[-1].end_lineno
    lines.insert(at, '    print("    * A COUNT ADDED BY mg-d3f3 a2/Y2, in a '
                     'SIBLING section: %d of %d posets" % (len(ps) - 1, len(ps)))\n')
    return "".join(lines)


def y3_inside(src):
    fn = _fn(src, FN)
    lines = src.splitlines(keepends=True)
    at = fn.body[-1].end_lineno
    lines.insert(at, '    print("    * A COUNT ADDED BY mg-d3f3 a2/Y3, inside '
                     'the section: %d of %d posets" % (len(ps) - 1, len(ps)))\n')
    return "".join(lines)


def run(mutate):
    sb = L.Sandbox()
    src = sb.read("face_geometry/controls.py")
    out = mutate(src)
    extra = None
    if isinstance(out, tuple):
        out, extra = out
    sb.write("face_geometry/controls.py", out)
    art, rc = sb.regenerate()
    code, rows, _ = sb.verify()
    sb.close()
    return art, rc, code, rows, extra


def main():
    R = L.Report("mg-d3f3 a2 -- the V6b row name against the V6b measurement")
    before = L.tree_digest(L.real_tree_paths())

    sys.path.insert(0, L.REPAIR)
    from verify_e35b import TABLE, CENSUS_DECLARED                # noqa: E402
    anchors = [a for *_, a in TABLE]
    base_art = open(L.PROBE + "/controls_output.txt").read()

    R.note("V6b's declared value, in full, because the finding is about its "
           "SHAPE: %s" % CENSUS_DECLARED)
    R.note("it is a multiset of conversion TYPES, so any edit preserving the "
           "type counts preserves the row.")
    print()

    # ---------------- Y1 -------------------------------------------------
    art, art_rc, code, rows, removed = run(lambda s: y1_add_and_remove(s, anchors))
    R.check("a2.1 Y1 ADD AND REMOVE -- one %%d-bearing count deleted from "
            "`%s` and a different one added: V6a, V6b, V6c and V6d are ALL "
            "GREEN (population: the four V6 rows; grain: one row)" % FN,
            all(L.row(rows, t) for t in ("V6a", "V6b", "V6c", "V6d")),
            "red: %s; the removed sentence was %r; the artifact moved by %d "
            "bytes and the census by 0"
            % ([r[:36] for r in L.reds(rows)] or "none",
               removed[:56], abs(len(art) - len(base_art))))
    R.note("PREDICTION MISS, KEPT AS WRITTEN.  P3a predicted the verifier would "
           "exit 0 on Y1.  It exits %d.  The V6 half of the prediction is what "
           "a2.1 scores and it held; the exit code did not, because the print "
           "Y1 deleted happened to carry the phrase V5's HEDGE row anchors on "
           "(\"WHAT IS IN THE REMAINDER IS NOW STATED\").  That is a real red "
           "and it is not the census's: a literal-anchor row elsewhere in the "
           "file caught the collateral, not the count.  Y1b below removes the "
           "collateral and leaves the claim." % code)

    # ---------------- Y1b, the same claim without the collateral ---------
    _, _, code1b, rows1b, _ = run(y1b_add_and_remove)
    R.check("a2.1b Y1b -- the count alone removed (its `%d` made literal text, "
            "its operand dropped) and a new single-`%d` count added: the "
            "verifier exits 0 with all rows green, so a count WAS added and a "
            "count WAS removed and nothing in the file says so (P3a, cleanly)",
            code1b == 0 and not L.reds(rows1b),
            "exit %d, red: %s"
            % (code1b, [r[:36] for r in L.reds(rows1b)] or "none"))
    R.count("specifiers V6b measures under Y1/Y1b",
            CENSUS_DECLARED["specifiers"],
            "FORCED", "FORCED BY THE CONSTRUCTION: both are built to preserve "
            "the multiset, so this row could not have come out otherwise and is "
            "not offered as evidence -- the evidence is the exit code beside it")

    # ---------------- Y2 -------------------------------------------------
    art2, _, code2, rows2, _ = run(y2_out_of_population)
    added_reaches = "A COUNT ADDED BY mg-d3f3 a2/Y2" in art2
    R.check("a2.2 Y2 OUT OF POPULATION -- a count added to the sibling section "
            "`%s` REACHES the artifact and moves none of V6a/V6b/V6c/V6d; "
            "verifier exit 0 (P3b)" % SIBLING,
            added_reaches and code2 == 0
            and all(L.row(rows2, t) for t in ("V6a", "V6b", "V6c", "V6d")),
            "the new count is %sin controls_output.txt; exit %d, red: %s"
            % ("" if added_reaches else "NOT ", code2,
               [r[:36] for r in L.reds(rows2)] or "none"))
    R.note("THE SENTENCE THIS CONTRADICTS, verbatim from verify_e35b.py's V6c "
           "row: \"so a count CANNOT be added to the artifact without moving "
           "V6b\".  Y2 adds one and V6b does not move.  The claim is true of "
           "`negative_control_incidence` and false of the artifact, and the row "
           "says artifact.")

    # ---------------- Y3, the wrong-direction control --------------------
    _, _, code3, rows3, _ = run(y3_inside)
    R.check("a2.3 Y3 (WRONG DIRECTION) -- the SAME count added INSIDE the "
            "section does turn V6b red and exits 1, so Y1 and Y2 are not "
            "reporting a census that never fires",
            code3 == 1 and not L.row(rows3, "V6b"),
            "exit %d, red: %s" % (code3, [r[:36] for r in L.reds(rows3)]))

    # ---------------- the sections the artifact actually holds ------------
    src = open(L.PROBE + "/controls.py").read()
    mainfn = _fn(src, "main")
    called = [c.func.id for c in ast.walk(mainfn)
              if isinstance(c, ast.Call) and getattr(c.func, "id", None)
              and _has_def(src, c.func.id)]
    R.count("sections main() calls into the artifact", len(called), "COULD MOVE",
            "a section added to or removed from main() moves it; V6b's "
            "population is 1 of them (%s)" % FN)
    R.check("a2.4 the artifact is the output of more than one section, which is "
            "why Y2 exists", len(called) > 1, ", ".join(called))

    print()
    R.note("VERDICT ON THE WORD.  \"TRIPWIRE\" is honest about the MECHANISM -- "
           "it fires on a change rather than proving a correspondence, and the "
           "row says so.  It is not honest about the SCOPE, and the scope is "
           "the half a reader scores the repair by.  The repair for this is one "
           "clause, not a redesign: the population belongs in the row name.  "
           "That is a recommendation, not an edit -- nothing here is changed.")

    after = L.tree_digest(L.real_tree_paths())
    R.check("a2.5 nothing under code/ was written",
            all(before[k] == after.get(k) for k in before),
            "moved: %s" % (sorted(k for k in before
                                  if before[k] != after.get(k)) or "none"))
    return R.finish()


def _has_def(src, name):
    return re.search(r"^def %s\(" % re.escape(name), src, re.M) is not None


if __name__ == "__main__":
    sys.exit(main())
