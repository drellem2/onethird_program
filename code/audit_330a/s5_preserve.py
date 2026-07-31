"""s5_preserve.py -- WHAT MUST STILL BE THERE.

A repair is not only what it changed.  Five things this arc paid for are
scored here, and a repair that dropped any of them would be a regression that
no count of the two repaired sites would show:

  (i)   THE FOURTH INPUT THAT IS NEITHER CASE -- `one-sided`, a kern-alone
        bend.  Scored precisely because the two named cases (cancelling,
        conspiring) read as a partition and are not one.
  (ii)  THE SECOND CONSPIRING PAIR OF A DIFFERENT SHAPE -- `conspiring-B`, a
        BOOLEAN default of False that ADDS AN ABSENT VERTEX, against
        `conspiring-A`'s INTEGER default of 0 that SHIFTS A VALUE.  Two
        instances of one shape are one instance.
  (iii) THE EDGE PROBE -- one operand moved across each clause of the
        narrowed bound: 11 -> 12 inside all three clauses, and 11, 11, 11
        outside.
  (iv)  `AND NOTHING ELSE` AT 11 OF 11, WITH 0 FROM OUTSIDE.
  (v)   AND THE ONE FILE THE REPAIR TOUCHED THAT ALL FOUR REST ON:
        kern5f9a.py.  The claim is that the edit is a COMMENT.  Checked at
        the PARSED-MODULE grain, not by reading the diff -- a diff says what
        changed in the text and the question is what changed in the program.

(i)-(iv) are re-measured by RUNNING mg-2c77's own q1 and q2, unmodified, and
reading their published rows.  dfa263c touched no file in code/audit_2c77/,
so the risk is not that the probes were edited -- it is that the SUBJECT
moved under them.  That is why (v) is here and why the runs are runs.

Nothing here writes into code/audit_2c77/ or code/face_geometry_instr_5f9a/.
q1 and q2 write no files; each is run in a clone and its stdout captured.
"""

import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib330a as L                                          # noqa: E402

C2C77_DIR = "code/audit_2c77"
KERN5F9A = "code/face_geometry_instr_5f9a/kern5f9a.py"

R = L.Report(
    selfpop="every clone, git read, source read, AST parse and subprocess "
            "run this script performs, plus the requirement that each "
            "foreign script produce a scoreable transcript and that every "
            "row this script scores be FOUND in the output it parses -- a "
            "row this script could not locate is a fact about this script "
            "and is never scored as agreement",
    findpop="the 4 inputs mg-2c77's q1 scores and the 3-row verdict each "
            "gets; the 2 conspiring pairs, scored for whether they are of "
            "DIFFERENT shape; the 5 rows of q2's edge probe and the column "
            "each falls in; q2's `AND NOTHING ELSE` row count and its "
            "outside count; and the parsed module of kern5f9a.py before and "
            "after the only edit dfa263c made to it")

L.banner("S5", "WHAT MUST STILL BE THERE -- THE PRESERVED FIVE")

# ---------------------------------------------------------------------------
L.rule("(v-first) THE ONE FILE THE REPAIR TOUCHED THAT ALL OF THESE REST ON")
# ---------------------------------------------------------------------------

print("""   Done FIRST, because if kern5f9a.py's program changed then every
   row below is about a different subject and the agreement would be
   the wrong kind of agreement.

   dfa263c's commit message says `The kern5f9a edit is a comment: the
   parsed modules are compared and are identical.`  Checked here at the
   PARSED-MODULE grain rather than by reading the diff: a diff says
   what changed in the TEXT, and the question is what changed in the
   PROGRAM.
""")

before = L.show_or_empty(L.REPAIR_8D5E + "^", KERN5F9A)
after = L.show_or_empty(L.REPAIR_8D5E, KERN5F9A)
head = L.read_worktree(KERN5F9A)
R.selfgate(bool(before) and bool(after),
           "kern5f9a.py could not be read at dfa263c or its parent")

print("   text sha, before dfa263c vs after : %s"
      % ("differs" if L.sha(before) != L.sha(after) else "identical"))
try:
    d_before = ast.dump(ast.parse(before))
    d_after = ast.dump(ast.parse(after))
    d_head = ast.dump(ast.parse(head))
except SyntaxError as exc:
    R.selferr("kern5f9a.py does not parse at one of the three revisions: %s"
              % exc)
    d_before = d_after = d_head = None

if d_before is not None:
    print("   PARSED MODULE, before vs after    : %s"
          % ("IDENTICAL" if d_before == d_after else "*** DIFFERS"))
    print("   PARSED MODULE, after vs HEAD      : %s"
          % ("IDENTICAL" if d_after == d_head else "*** DIFFERS"))
    R.gate(d_before == d_after,
           "dfa263c changed the PARSED MODULE of kern5f9a.py, not only a "
           "comment -- every preserved row below is about a different "
           "program from the one that was measured")
    R.gate(d_after == d_head,
           "kern5f9a.py's parsed module has changed between dfa263c and "
           "HEAD, so the preservation checks below do not range over the "
           "tree the repair shipped")

    nb = len([1 for n in ast.walk(ast.parse(before))])
    print("   ast nodes in the module           : %d (unchanged)" % nb)

# ---------------------------------------------------------------------------
L.rule("(i)+(ii) THE FOUR INPUTS -- q1_reason.py, RE-RUN UNMODIFIED")
# ---------------------------------------------------------------------------

print("""   `cancelling` and `conspiring` are the two cases the corrected
   reason NAMES, and two named cases read as a partition.  q1 scores a
   FOURTH input that is neither -- a kern-alone bend -- precisely
   because of that, and a SECOND conspiring pair of a different SHAPE,
   because two instances of one shape are one instance.

   dfa263c touched no file in %s.  So the risk here is not that the
   probe was edited; it is that the subject moved under it.  q1 is
   RUN.
""" % C2C77_DIR)

tree = L.clone_at("HEAD")
q1_out = q2_out = ""
try:
    d = os.path.join(tree, C2C77_DIR)
    rc1, q1_out = L.run_py("q1_reason.py", d, timeout=3600)
    print("   q1_reason.py, re-run at HEAD : exit %d" % rc1)
    rc2, q2_out = L.run_py("q2_bound_edge.py", d, timeout=3600)
    print("   q2_bound_edge.py, re-run at HEAD : exit %d" % rc2)
finally:
    L.rm_tree(tree)

NAMES = ("cancelling", "conspiring-A", "conspiring-B", "one-sided")
print("\n   THE FOUR INPUTS, EACH LOOKED FOR BY NAME IN q1's OWN OUTPUT:")
present = {}
for n in NAMES:
    present[n] = (n in q1_out)
    print("   %-16s %s" % (n, "present" if present[n] else "*** ABSENT"))
R.gate(all(present.values()),
       "q1 no longer scores %s -- an input this arc paid for has been dropped"
       % ", ".join(n for n in NAMES if not present[n]))
R.gate(present.get("one-sided", False),
       "THE FOURTH INPUT THAT IS NEITHER CASE is gone.  It exists because "
       "`cancelling` and `conspiring` read as a partition and are not one; "
       "without it the two named cases go back to looking exhaustive")
R.gate(present.get("conspiring-B", False),
       "THE SECOND CONSPIRING PAIR is gone.  conspiring-A is an INTEGER "
       "default that shifts a value and conspiring-B a BOOLEAN default that "
       "adds an absent vertex; with only one of them, one shape stands for "
       "the class")

print("\n   AND THE ROWS EACH INPUT GETS, verbatim from q1's own output.\n"
      "   A name being present is not the same as a row being scored:")
rows = [ln for ln in q1_out.splitlines()
        if any(n in ln for n in NAMES)
        and ("MOVED" in ln or "IDENTICAL" in ln or "of 3" in ln)]
R.selfgate(bool(rows),
           "no scored row for any of the four inputs was found in q1's "
           "output; a row this script could not locate is never scored as "
           "agreement")
for ln in rows:
    print("     %s" % ln.strip()[:100])

print("\n   AND THE SHAPES ARE DIFFERENT, checked in q1's OWN source rather\n"
      "   than in its output -- two inputs with different names and the\n"
      "   same construction are one input twice:")
q1_src = L.read_worktree(C2C77_DIR + "/q1_reason.py")
lib_src = L.read_worktree(C2C77_DIR + "/lib2c77.py")
shape_a = [ln.strip() for ln in (q1_src + lib_src).splitlines()
           if "conspire" in ln and "def " in ln]
for ln in shape_a:
    print("     %s" % ln[:96])

# DEFECT #4 OF THIS INSTRUMENT, KEPT.  The first version of this check asked
# whether the substring "False" or "bool" occurred on a line whose text
# contained both "conspire" and a capital "B", and printed `not found by this
# reader` -- a reader that answers "I don't know" and a reader that answers
# "no" are different things, and printing the first where a gate wants the
# second is how a check becomes decoration.  Replaced with a read of the two
# constructions' actual BODIES.


def body_of(src, fname):
    """The source segment of `fname`'s body, or "" if it is not defined."""
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == fname:
            return "\n".join(src.splitlines()[node.lineno - 1:node.end_lineno])
    return ""


print("     the two constructions' BODIES, read by ast:")
SHAPES = {}
for fname in ("conspire_a_kern", "conspire_b_kern"):
    body = body_of(lib_src, fname)
    SHAPES[fname] = body
    R.selfgate(bool(body),
               "%s is not defined in lib2c77.py -- the shape cannot be read"
               % fname)
    for ln in body.splitlines():
        print("       %s" % ln.strip()[:92])

a_body, b_body = SHAPES.get("conspire_a_kern", ""), \
    SHAPES.get("conspire_b_kern", "")
a_int = any(ch.isdigit() for ch in a_body.split("=")[-1]) \
    and "True" not in a_body and "False" not in a_body
b_bool = ("True" in b_body or "False" in b_body)
print("     conspiring-A's default is an INTEGER  : %s" % ("yes" if a_int
                                                           else "NO"))
print("     conspiring-B's default is a BOOLEAN   : %s" % ("yes" if b_bool
                                                           else "NO"))
print("     and the two bodies are different text : %s"
      % ("yes" if a_body and b_body and a_body != b_body else "*** NO"))
R.gate(a_int and b_bool and a_body != b_body,
       "the two conspiring pairs are not of DIFFERENT shape: A's default "
       "reads as %s and B's as %s.  Two instances of one shape are one "
       "instance, and the second pair was built precisely so that one shape "
       "would not stand for the class"
       % ("integer" if a_int else "not an integer",
          "boolean" if b_bool else "not a boolean"))

c1b = body_of(lib_src, "conspire_b_c1")
adds_vertex = "vertices()" in c1b and ("+ (" in c1b or "+ [" in c1b)
print("     and conspiring-B's c1 half ADDS a vertex rather than shifting a\n"
      "     value : %s" % ("yes" if adds_vertex else "*** NOT SEEN"))
R.gate(adds_vertex,
       "conspiring-B's c1 half no longer ADDS an absent vertex -- the shape "
       "that distinguishes it from conspiring-A's value shift is gone")

R.gate(rc1 == 0,
       "mg-2c77's q1_reason.py, re-run unmodified at HEAD, exits %d where "
       "its committed transcript records TOTAL BAD: 0 -- the four inputs no "
       "longer score as they did" % rc1)

# ---------------------------------------------------------------------------
L.rule("(iii)+(iv) THE EDGE PROBE, AND `AND NOTHING ELSE`")
# ---------------------------------------------------------------------------

print("""   One operand moved across each clause of the narrowed bound.  The
   published rows are: unperturbed 11; INSIDE all three clauses 12;
   and 11, 11, 11 for the three probes outside.  A bound whose edge
   was never crossed is a bound nobody measured.
""")

# DEFECT #5 OF THIS INSTRUMENT, KEPT.  The first version of this section
# asked only whether the substrings "11" and "12" occurred anywhere in q2's
# output, and printed `yes / yes`.  That is a check that cannot fail: q2
# prints dozens of numbers and two of them are two digits.  A gate whose red
# is unreachable is decoration, and it is the same defect as a comparison of
# a predicate with itself -- the thing this whole audit is about.  Replaced
# with a read of q2's OWN five rows, each matched by the label q2 gives it
# and each scored against the value the brief names.
EXPECT = [("the sweep's enumerated rows on the unperturbed tree", 11, "-"),
          ("INSIDE the bound", 12, "swept"),
          ("outside: not top-level", 11, "not swept: nested"),
          ("outside: not a deciding condition", 11, "NO COLUMN"),
          ("outside: not a swept file", 11, "not swept: file")]

print("   %-42s %-6s %-6s %s" % ("q2's own row label", "want", "got",
                                 "column"))
missing = []
for label, want, col in EXPECT:
    row = None
    for ln in q2_out.splitlines():
        if label in ln:
            row = ln.strip()
    if row is None:
        missing.append(label)
        print("   %-42s %-6d %-6s %s" % (label, want, "***", "ROW NOT FOUND"))
        continue
    nums = [int(t) for t in row.replace(":", " ").split() if t.isdigit()]
    got = nums[0] if len(nums) == 1 else (nums[-1] if nums else None)
    ok = got == want
    print("   %-42s %-6d %-6s %s"
          % (label, want, got if got is not None else "-",
             ("%s" % col) + ("" if ok else "   *** EXPECTED %d" % want)))
    R.gate(ok,
           "q2's row %r prints %s where the published edge probe records %d "
           "-- the bound's edge no longer crosses where it was measured to "
           "cross" % (label, got, want))
    if col != "-":
        R.gate(col in row,
               "q2's row %r no longer files in the column %r -- the probe "
               "still counts but is classified somewhere else" % (label, col))

R.selfgate(not missing,
           "%d of q2's 5 edge-probe rows were not found in its output by "
           "label: %s.  A row this script could not locate is a fact about "
           "this script and is never scored as agreement"
           % (len(missing), "; ".join(missing)))

nothing = [ln.strip() for ln in q2_out.splitlines()
           if "NOTHING ELSE" in ln or "11 of 11" in ln
           or "removed an operand" in ln.lower()]
print("\n   `AND NOTHING ELSE`, verbatim from q2's own output:")
R.selfgate(bool(nothing),
           "no `AND NOTHING ELSE` row was found in q2's output; the clause "
           "is never scored as holding on a row this script could not find")
for ln in nothing:
    print("     %s" % ln[:100])

R.gate(rc2 == 0,
       "mg-2c77's q2_bound_edge.py, re-run unmodified at HEAD, exits %d "
       "where its committed transcript records TOTAL BAD: 0 -- the edge "
       "probe or the `AND NOTHING ELSE` clause no longer holds" % rc2)

# ---------------------------------------------------------------------------
L.rule("(vi) THE PREDICTIONS FILES, AND THE MISSES KEPT AS WRITTEN")
# ---------------------------------------------------------------------------

print("""   `PREDICTIONS committed before any script exists, and misses kept
   as written.`  Two claims, and only the first is checkable by
   reading: the second is checkable only by finding misses that are
   still there.
""")

pred = "code/repair_8d5e/PREDICTIONS.md"
pred_rev = L.my_first_introducing(pred, "#") or L.my_last_touching(pred)
first_pred = [h for h in L.git("log", "--format=%H", "--reverse", "--", pred)
              .split() if h]
R.selfgate(bool(first_pred), "%s has no history" % pred)
if first_pred:
    intro = first_pred[0]
    print("   %s introduced at : %s" % (pred, intro[:8]))
    print("     subject          : %s" % L.subject(intro)[:76])
    scripts = ["code/repair_8d5e/%s" % s for s in
               ("r1_anchor.py", "r2_kernel_half.py", "r3_term.py",
                "r4_self.py", "lib8d5e.py", "selftest_8d5e.py")]
    at_intro = [s for s in scripts if L.show_or_empty(intro, s)]
    print("     scripts of this instrument existing at that commit : %d of %d"
          % (len(at_intro), len(scripts)))
    for s in at_intro:
        print("        *** %s" % s)
    R.gate(not at_intro,
           "%d script(s) of mg-8d5e's own instrument already existed at the "
           "commit that introduced its PREDICTIONS.md (%s): %s -- the "
           "predictions were not committed before any script existed"
           % (len(at_intro), intro[:8], ", ".join(at_intro)))

pred_src = L.read_worktree(pred)
misses = [ln.strip() for ln in pred_src.splitlines()
          if "MISS" in ln or "miss" in ln.lower() and "kept" in ln.lower()]
print("\n   lines of %s naming a miss : %d" % (pred, len(misses)))
for ln in misses[:14]:
    print("     %s" % ln[:98])
R.gate(len(misses) > 0,
       "mg-8d5e's PREDICTIONS.md records no misses at all, and its own "
       "commit message says `with four misses kept and what was wrong "
       "beside each` -- the record and the summary disagree")

R.done()
