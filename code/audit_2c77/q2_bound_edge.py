"""q2_bound_edge.py -- THE BOUND, PROBED AT ITS EDGE, FROM OUTSIDE.

The narrowed sentence is

    DELETION REACHES THE TOP-LEVEL BOOLEAN OPERANDS OF THE DECIDING CONDITIONS
    IN THE FILES THIS SWEEP VISITS, AND NOTHING ELSE

and reading it beside the sweep's source and finding them to agree is not a
check.  Two sentences by one author agree; that is what authorship does.

SO THE BOUND IS PROBED, NOT READ.  It draws a boundary with three clauses, and
each clause is tested by MOVING AN OPERAND ACROSS IT and asking the sweep's own
population function -- `kern5f9a.deciding_clauses`, which is the function
`d2_deletion.py` enumerates and mutates -- what it now sees:

    top-level ............. one operand added NESTED inside a deciding
                            condition; the sweep must not see it
    of the deciding
    conditions ............ one operand added to an `if` whose body does not
                            return; the sweep must not see it
    in the files this
    sweep visits .......... one operand added to posets.py, at the top level
                            of a deciding condition; the sweep must not see it

and one operand added INSIDE all three clauses, which the sweep MUST see -- a
boundary demonstrated only from the outside cannot tell `excluded` from
`invisible`.

AND THEN THE `AND NOTHING ELSE` HALF, WHICH IS THE HALF A SENTENCE CANNOT
SETTLE.  Every one of the sweep's rows is applied and the operand multiset of
the result is differenced against the original.  A row that removed something
outside the bound would show up as a second entry in that difference.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import ast
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "face_geometry_instr_5f9a"))

import lib2c77 as L                                              # noqa: E402
import kern5f9a as K                                             # noqa: E402

R = L.Report(
    selfpop="every source read and parse this script performs, the "
            "requirement that each of the 4 perturbations really apply and "
            "leave a file that still parses, and the requirement that the "
            "unperturbed sweep population not be empty",
    findpop="the sweep's enumerated clause population under 4 perturbations, "
            "one per clause of the narrowed bound plus one inside it, each "
            "scored against what the bound says the sweep reaches and against "
            "the column the shipped classifier files it in; and the operand "
            "multiset difference produced by every one of the sweep's own "
            "rows, against the `AND NOTHING ELSE` clause")

L.banner("Q2", "THE NARROWED BOUND, PROBED AT ITS EDGE")

FACE = L.read_worktree(L.FACE_REL)
POSETS = L.read_worktree(L.POSETS_REL)
BASE_SOURCES = {"face_complex.py": FACE, "posets.py": POSETS}

base_clauses = K.deciding_clauses(FACE)
R.check(len(base_clauses) > 0,
        "the unperturbed sweep population is empty; every row below would be "
        "a comparison against nothing")

# ---------------------------------------------------------------------------
L.rule("(i) THE FOUR PERTURBATIONS, EACH ONE OPERAND, EACH APPLIED ONCE")
print("""   Every edit is made with a replace-exactly-once that refuses on 0
   occurrences and on many, and the result is required to parse.  A
   perturbation that silently did nothing would make the sweep's count
   hold for the wrong reason -- which is the reading a boundary probe
   must never make.

   Nothing is written into code/face_geometry/.  Each perturbed source
   is held in memory and handed to the sweep's own functions.""")
print()

PROBES = [
    ("INSIDE the bound",
     "face_complex.py",
     "        return a == b or (a, b) in self.less\n",
     "        return a == b or (a, b) in self.less or a is b\n",
     "a third operand at the TOP LEVEL of a deciding condition, in the swept "
     "file",
     True, "swept"),
    ("outside: not top-level",
     "face_complex.py",
     "    return [m for m in order_ideals(P) if m != 0 and m != full]\n",
     "    return [m for m in order_ideals(P) if m != 0 and m != full "
     "and m >= 0]\n",
     "a third operand NESTED under a comprehension inside a deciding "
     "condition",
     False, "not swept: nested"),
    ("outside: not a deciding condition",
     "face_complex.py",
     "            if (mask >> b) & 1 and not ((mask >> a) & 1):\n",
     "            if (mask >> b) & 1 and not ((mask >> a) & 1) and P.n >= 0:\n",
     "a third operand in an `if` whose body assigns and breaks and does not "
     "return",
     False, None),
    ("outside: not a swept file",
     "posets.py",
     "            if b == c and (a, d) not in rel:\n",
     "            if b == c and (a, d) not in rel and a != d:\n",
     "a third operand at the TOP LEVEL of a condition, in a file the sweep "
     "does not visit",
     # MISS #3, KEPT.  This column first read `None`.  PREDICTIONS.md had it
     # right -- `not swept: file` -- and the script encoded it wrong, so the
     # first run booked a finding against the repair for something the repair
     # gets right.  The bound excludes this operand from the SWEEP, which is
     # what the 11 measures; the CENSUS still places it, because posets.py is
     # one of the census's two files.  Those are different questions and the
     # first version of this row conflated them.
     False, "not swept: file"),
]

print("   the sweep's file population, read out of d2_deletion.py's own "
      "SWEEP_FILES: %s" % ", ".join(L.SWEEP_FILES))
print("   the sweep's enumerated rows on the unperturbed tree               : "
      "%d" % len(base_clauses))
print()
print("   %-32s %-10s %-8s %-9s %s"
      % ("probe", "file", "sweep", "expected", "column the classifier files "
         "it in"))
for label, fname, old, new, why, inside, want_col in PROBES:
    sources = dict(BASE_SOURCES)
    try:
        sources[fname] = L.replace_once(BASE_SOURCES[fname], old, new)
        ast.parse(sources[fname])
    except (ValueError, SyntaxError) as e:
        R.selferr("the `%s` perturbation did not apply (%s); its row is "
                  "DROPPED rather than counted as agreeing" % (label, e))
        continue
    n = len(K.deciding_clauses(sources["face_complex.py"]))
    want = len(base_clauses) + 1 if inside else len(base_clauses)
    # where does the new operand land?  Difference the classifier's columns
    # before and after, by span-free identity: the column whose count grew.
    before = K.operand_columns(BASE_SOURCES, L.SWEEP_FILES)
    after = K.operand_columns(sources, L.SWEEP_FILES)
    grew = [c for c in K.OPERAND_COLUMNS
            if len(after[c]) > len(before[c])]
    got_col = grew[0] if len(grew) == 1 else (
        "NO COLUMN" if not grew else "+".join(grew))
    print("   %-32s %-10s %-8d %-9d %s"
          % (label, fname, n, want, got_col))
    R.gate(n == want,
           "the `%s` probe moved the sweep's enumerated population to %d when "
           "the bound says %d: %s.  The bound and the sweep disagree at their "
           "edge" % (label, n, want, why))
    R.gate(got_col == (want_col or "NO COLUMN"),
           "the `%s` probe -- %s -- was filed under `%s` and the bound puts "
           "it in `%s`" % (label, why, got_col, want_col or "NO COLUMN"))
print()
print("""   READ THE THIRD ROW.  An operand added to an `if` that does not return
   is invisible to the sweep, which the bound says correctly, AND it is in
   NO COLUMN of the census beside the bound.  That is the thing the sweep
   does not cover which the BOUND excludes and the CENSUS does not account
   for -- q3 counts how many of them the tree already has.""")
print()

# ---------------------------------------------------------------------------
L.rule("(ii) `AND NOTHING ELSE` -- EVERY SWEEP ROW APPLIED, AND DIFFERENCED")
print("""   The second half of the bound is a claim about what deletion does
   NOT touch, and no sentence settles it.  Each of the sweep's own rows
   is applied with `drop_clause` and the resulting operand multiset is
   differenced against the unperturbed one.  A row that removed an
   operand from outside the bound would appear here as a second entry.

   The multiset is keyed on (function, operand text) rather than on a
   source span, because a deletion shifts every span after it and a
   span key would report the whole tail of the file as changed.""")
print()


def multiset(src, fname):
    c = collections.Counter()
    for o in L.all_boolean_operands(src, fname):
        c[(o["func"], " ".join((o["text"] or "").split()))] += 1
    return c


base_ms = multiset(FACE, "face_complex.py")
inside_spans = {(o["func"], " ".join((o["text"] or "").split()))
                for o in L.deciding_boolean_operands(FACE, "face_complex.py")
                if o["top"]}
print("   %-24s %-6s %-4s %-46s %s"
      % ("function", "kind", "cls", "the operand the row removes",
         "other operands lost"))
extra_losses = []
for cl in base_clauses:
    try:
        mutated = K.drop_clause(FACE, cl)
        ast.parse(mutated)
    except (ValueError, SyntaxError) as e:
        R.selferr("the sweep row %s/%s/%d would not apply (%s); it is DROPPED "
                  "rather than counted as touching nothing"
                  % (cl.func, cl.kind, cl.index, e))
        continue
    lost = base_ms - multiset(mutated, "face_complex.py")
    keys = sorted(lost.elements())
    outside_lost = [k for k in keys if k not in inside_spans]
    print("   %-24s %-6s %-4d %-46s %s"
          % (cl.func, cl.kind, cl.index + 1,
             " ".join((cl.source or "").split())[:46],
             ", ".join("%s/%s" % k for k in outside_lost) or "none"))
    if outside_lost:
        extra_losses.append((cl.func, cl.kind, cl.index, outside_lost))
print()
print("   %d sweep row(s) applied; %d of them removed an operand from outside "
      "the\n   bound." % (len(base_clauses), len(extra_losses)))
R.gate(not extra_losses,
       "the `AND NOTHING ELSE` half does not hold: %d sweep row(s) removed an "
       "operand that is not a top-level operand of a deciding condition -- %s"
       % (len(extra_losses),
          "; ".join("%s/%s/c%d loses %s"
                    % (f, k, i + 1, ", ".join("%s/%s" % x for x in ol))
                    for f, k, i, ol in extra_losses)))
print()

L.finish(R)
