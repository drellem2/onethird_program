"""p1_bound.py -- OPEN 1: THE BOUND, NARROWED TO THE SWEEP, AND ALL 17 CLASSIFIED.

mg-eaef found the stated bound WIDER than the sweep it describes, in two ways:

  E5  `DELETION ESTABLISHES COVERAGE DOWN TO EXPLICIT BOOLEAN OPERANDS AND NO
      FURTHER` is read as `every explicit boolean operand is on the reached
      side`.  4 of face_complex.py's 15 are on NEITHER side of the census --
      not in `operands`, because their condition is not a `BoolOp`, and not in
      `compounds`, because the form filter skips `or` and `and` BY NAME.

  E4  The `operands` column read 2 for posets.py, under a heading that said
      `operands the sweep deletes`, and the sweep deletes 0 there.

THE REPAIR IS TWO THINGS AND NEITHER IS A NEW TECHNIQUE.  The sentence is
narrowed to what the sweep actually reaches, and every explicit boolean operand
is put in exactly one NAMED column -- with `not determined` printed as a column
rather than left as an empty cell, because an empty cell is the absence of an
answer and that absence is exactly the ambiguity a stated bound exists to
remove.

WHAT THIS SCRIPT MEASURES, in order:

  (i)   the sentence, enumerated from the tree: the wide one gone from every
        LIVE site, the narrow one present, and the copies that are quotations
        of history named as such rather than silently left out
  (ii)  all 17 operands in exactly one named column, with the population
        re-derived by an independent walk
  (iii) the `swept` column against the sweep's OWN rows -- name by name, not
        count by count -- and posets.py contributing 0
  (iv)  the 4 nested operands DELETED ONE AT A TIME against the control
        battery: mg-eaef's E2 re-derived, and the reason the narrowing is
        necessary rather than cosmetic
  (v)   the control demonstrated where the defect is still present: the same
        classification run on bfd7948's sources, and the repaired classifier
        with its nested column DELETED

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..",
    "face_geometry_instr_5f9a")))

import lib69d1 as L                                              # noqa: E402
import kern5f9a as K                                             # noqa: E402

R = L.Report(
    selfpop="every git read and source read this script performs, the "
            "requirement that each of the 4 nested deletions really apply, "
            "and the requirement that the baseline artifact be non-empty "
            "before any comparison is made",
    findpop="the 2 written forms of the bound sentence over every live site "
            "in the tree, the 17 explicit boolean operands of the census's "
            "two files against the 4 named columns, the `swept` column "
            "against the sweep's own enumerated rows, the 4 nested operands "
            "deleted one at a time against the control battery, and the "
            "classifier with one column deleted")

# The two forms.  The wide one is the defect; the narrow one is the repair.
WIDE = "DELETION ESTABLISHES COVERAGE DOWN TO EXPLICIT BOOLEAN OPERANDS AND NO"
NARROW = "DELETION REACHES THE TOP-LEVEL BOOLEAN OPERANDS OF THE DECIDING"

# A copy of the WIDE sentence is a QUOTATION OF HISTORY, not a live assertion,
# iff a correcting marker stands within CORRECTION_WINDOW lines of it in the
# same file.  An audit's record of what it found is not a claim the tree is
# making now, and rewriting it would delete the evidence this repair rests on.
#
# THE DISCRIMINATOR IS A PROXIMITY TEST AND NOT A PATH LIST, deliberately: a
# path list would have to name d2_deletion.py, face_complex.py and run_all.sh,
# which are the three files the sentence was LIVE in, and the check would be
# vacuous by construction.
#
# AND ITS OWN BOUND, STATED: this cannot tell a quotation from an assertion
# that happens to cite the ticket nearby.  It is a test for `the correction
# travels with the copy`, which is the property that matters to a reader, and
# it is not a test for authorial intent.  Widen the window and it weakens;
# CORRECTION_WINDOW is printed with the result so the reader can price it.
#
# The third marker is the audit's own finding text.  A committed transcript
# quotes the sentence INSIDE the finding that refutes it, on the same line, and
# carries no ticket id anywhere near -- a transcript names its ticket in a
# banner hundreds of lines up.  `NAMES A FLOOR IT DOES NOT REACH` is a
# refutation standing beside the copy, which is the property being tested, and
# it is not a path exemption: no file this repair had to narrow contains it.
CORRECTION_MARKERS = ("mg-69d1", "mg-eaef", "NAMES A FLOOR IT DOES NOT REACH",
                      "names a floor it does not reach")
CORRECTION_WINDOW = 25

L.banner("P1", "THE BOUND, NARROWED TO THE SWEEP, AND ALL 17 CLASSIFIED")
print("""
mg-eaef E5 and E4.  A bound stated wider than its evidence is the printed-extent
defect wearing the remedy for the printed-extent defect: the fix for an unstated
limit is a stated one, and a stated limit that over-claims is worse than none,
because it is read as a guarantee.
""")

# ---------------------------------------------------------------------------
L.rule("(i) THE SENTENCE, ENUMERATED FROM THE TREE RATHER THAN QUOTED")
print("""   A bound written in four places is four bounds.  Every copy is found
   with `git grep` over the WORKING TREE, untracked files included, so a
   copy this script did not remember is still in the population.  A site
   that QUOTES the old sentence in order to correct it is not a site
   that ASSERTS it; the two are told apart by whether a correcting
   marker stands within %d lines of the copy, in the same file.""" %
      CORRECTION_WINDOW)
print()
wide_sites = L.grep(WIDE)
narrow_sites = L.grep(NARROW)
print("   THE NARROW SENTENCE -- `%s ...`:" % NARROW[:56])
for path, lineno in narrow_sites:
    print("     %-56s line %s" % (path, lineno))
print()


def corrected_near(path, lineno):
    """Does a correcting marker stand within the window, in this file?"""
    try:
        lines = L.read_worktree(path).splitlines()
    except (IOError, OSError):                              # pragma: no cover
        return False
    i = int(lineno) - 1
    lo, hi = max(0, i - CORRECTION_WINDOW), i + CORRECTION_WINDOW + 1
    window = "\n".join(lines[lo:hi])
    return any(m in window for m in CORRECTION_MARKERS)


print("   THE WIDE SENTENCE -- `%s ...`:" % WIDE[:56])
live_wide = []
for path, lineno in wide_sites:
    quoting = corrected_near(path, lineno)
    if not quoting:
        live_wide.append((path, lineno))
    print("     %-56s line %-5s %s"
          % (path, lineno,
             "correction within %d lines" % CORRECTION_WINDOW if quoting
             else "*** LIVE ASSERTION"))
print()
print("   %d copy/copies of the wide sentence, %d of them live assertions; "
      "%d copy/copies\n   of the narrow one." % (len(wide_sites),
                                                 len(live_wide),
                                                 len(narrow_sites)))
print()
R.check(bool(narrow_sites),
        "the narrow sentence is not in the tree; there is nothing to score "
        "and every row below is withdrawn")
R.gate(not live_wide,
       "the bound is still stated WIDER than the sweep at %d site(s): %s.  "
       "Read as written it promises that every explicit boolean operand is on "
       "the reached side, and 6 of 17 are not"
       % (len(live_wide), ", ".join("%s:%s" % s for s in live_wide)))
print()

# ---------------------------------------------------------------------------
L.rule("(ii) ALL 17 OPERANDS, IN EXACTLY ONE NAMED COLUMN")
print("""   `boolean_operands` applies NO filter: it walks every deciding
   condition for `ast.BoolOp` and takes every value of every one.  That
   is what neither of the two previous columns did -- `deciding_clauses`
   asks whether the CONDITION IS a `BoolOp`, and `implicit_disjunctions`
   skips the forms `or` and `and` by name -- and it is why an `or`
   nested under a comprehension was in neither.

   `not determined` is a COLUMN and not an omission.  Nothing lands
   there on this tree, and it is printed anyway: a column that only
   appears when it is non-empty is a column a reader cannot rely on.""")
print()
FILES = ("face_complex.py", "posets.py")
sources = {f: K.source_at(None, f) for f in FILES}
cols = K.operand_columns(sources, L.SWEEP_FILES)
print("   the sweep's file population, read out of d2_deletion.py's own "
      "SWEEP_FILES: %s" % ", ".join(L.SWEEP_FILES))
print()
print("   %-18s %-6s %-16s %-18s %-15s %s"
      % (("file",) + tuple(K.OPERAND_COLUMNS) + ("all",)))
per_file = {}
for fname in FILES:
    row = [len([o for o in cols[c] if o.file == fname])
           for c in K.OPERAND_COLUMNS]
    per_file[fname] = row
    print("   %-18s %-6d %-16d %-18d %-15d %d"
          % ((fname,) + tuple(row) + (sum(row),)))
allrow = [len(cols[c]) for c in K.OPERAND_COLUMNS]
print("   %-18s %-6d %-16d %-18d %-15d %d"
      % (("ALL",) + tuple(allrow) + (sum(allrow),)))
print()
print("   the %d this sweep does NOT delete, named -- a count of what is "
      "uncovered that\n   cannot be pointed at is the same silence as no count "
      "at all:" % (sum(allrow) - allrow[0]))
for col in K.OPERAND_COLUMNS[1:]:
    for o in cols[col]:
        print("      %-16s %-24s %-6s %-18s %s"
              % (o.file, o.func, o.kind, col,
                 " ".join((o.source or "").split())[:40]))
print()
total = K.operand_columns_total(sources)
print("   population re-derived by an INDEPENDENT walk : %d" % total)
print("   sum of the four columns                     : %d" % sum(allrow))
R.gate(sum(allrow) == total and total > 0,
       "the classification is not total: %d operand(s) walked, %d placed in a "
       "column.  An operand in no column is an empty cell, which is the "
       "absence of an answer and not a third state"
       % (total, sum(allrow)))
R.gate(all(len(K.boolean_operands(sources[f], f)) == sum(per_file[f])
           for f in FILES),
       "the per-file rows do not add up to their own file's walked "
       "population, so the ALL row is right only by cancellation")
R.check("not determined" in cols,
        "the `not determined` column is absent from the classifier; an "
        "operand that cannot be placed would fall out of the table rather "
        "than being printed")
print()

# ---------------------------------------------------------------------------
L.rule("(iii) THE `swept` COLUMN AGAINST THE SWEEP'S OWN ROWS")
print("""   Not count against count.  mg-eaef's E4 was a count that matched
   nothing: `operands` read 2 for posets.py and the sweep deleted 0
   there, and both numbers were about "operands".  Here the swept
   column is compared to the sweep's ENUMERATED rows function by
   function and text by text.""")
print()
swept_named = sorted((o.func, o.kind, " ".join((o.source or "").split()))
                     for o in cols["swept"])
sweep_named = sorted((cl.func, cl.kind, " ".join((cl.source or "").split()))
                     for f in L.SWEEP_FILES
                     for cl in K.deciding_clauses(K.source_at(None, f)))
print("   %-24s %-6s %s" % ("function", "kind", "operand text"))
for func, kind, text in sweep_named:
    mark = "" if (func, kind, text) in swept_named else "   *** NOT IN COLUMN"
    print("     %-22s %-6s %s%s" % (func, kind, text[:36], mark))
print()
print("   sweep rows %d / `swept` column %d / identical as sets of (function, "
      "kind, text): %s" % (len(sweep_named), len(swept_named),
                           "yes" if swept_named == sweep_named else "NO"))
ps_swept = len([o for o in cols["swept"] if o.file == "posets.py"])
ps_all = len([o for o in cols["not swept: file"] if o.file == "posets.py"])
print("   posets.py: %d operand(s), %d in `swept`, %d in `not swept: file` -- "
      "the row E4\n   was about" % (ps_swept + ps_all, ps_swept, ps_all))
R.gate(swept_named == sweep_named and bool(swept_named),
       "the `swept` column and the sweep's own rows are not the same "
       "operands: column %d, sweep %d.  A bound derived from a second "
       "population is a bound that can be wider than the evidence"
       % (len(swept_named), len(sweep_named)))
R.gate(ps_swept == 0,
       "posets.py contributes %d operand(s) to `swept` and the sweep does not "
       "visit posets.py at all" % ps_swept)
print()

# ---------------------------------------------------------------------------
L.rule("(iv) THE 4 NESTED OPERANDS, DELETED ONE AT A TIME")
print("""   This is what makes the narrowing necessary rather than cosmetic.
   mg-eaef's E2 measured it and its own registered prediction was
   BYTE-IDENTICAL on all four -- on the assumption that what the sweep
   skips is what the battery cannot see.  Re-derived here from the
   tree, on this tree, with an EMPTY-BASELINE GUARD: a mutation that
   produced no artifact at all would otherwise compare `IDENTICAL` to
   another failure, which is the one reading a deletion test must never
   make.""")
print()
FG_FILES = ["face_complex.py", "posets.py", "controls.py", "run_probe.py"]
base_dir = K.mutate_tree([], FG_FILES)
base_out, base_rc = K.run_controls(base_dir)
ok_base = R.check(
    bool(base_out.strip()),
    "the unmutated control battery produced no output; every comparison below "
    "would read IDENTICAL for the wrong reason and section (iv) is withdrawn")
print("   baseline artifact: %d bytes, exit %d" % (len(base_out), base_rc))
print()
nested = cols["not swept: nested"]
changed = 0
if ok_base:
    print("   %-16s %-40s %-14s %s"
          % ("function", "operand deleted", "artifact", "exit"))
    for o in nested:
        text = " ".join((o.source or "").split())
        src = K.source_at(None, o.file)
        try:
            cut = K.drop_boolean_operand(src, o)
        except Exception as e:                              # pragma: no cover
            R.selferr("the nested operand %s / %s could not be deleted (%s); "
                      "its row is DROPPED rather than counted as passing"
                      % (o.func, text[:40], e))
            continue
        if cut == src:
            R.selferr("deleting %s / %s left the source unchanged; the row "
                      "below would report on a mutation that never happened"
                      % (o.func, text[:40]))
            continue
        d = K.tree_with_source(o.file, cut, FG_FILES)
        out, rc = K.run_controls(d)
        if not out.strip():
            R.selferr("the battery produced NO output with %s / %s deleted; "
                      "comparing two failures reads IDENTICAL and that row is "
                      "DROPPED" % (o.func, text[:40]))
            continue
        same = out == base_out
        changed += 0 if same else 1
        print("     %-14s %-40s %-14s %d"
              % (o.func, text[:40], "IDENTICAL" if same else "CHANGES", rc))
    print()
    print("   %d of %d nested operands CHANGE the artifact when deleted alone."
          % (changed, len(nested)))
    R.gate(changed == len(nested) and bool(nested),
           "only %d of %d nested operands change the artifact; the rest are "
           "inert, and an inert operand should be DELETED rather than reported "
           "as uncovered (mg-9220's move).  This finding would mean the "
           "narrowing is about operands that do nothing"
           % (changed, len(nested)))
print()

# ---------------------------------------------------------------------------
L.rule("(v) THE CONTROL, WHERE THE DEFECT IS STILL PRESENT")
print("""   Two directions, because a control demonstrated only against a
   repaired tree cannot tell `not covered` apart from `not coverable`.

   FIRST: the same classification run on bfd7948's sources -- the commit
   that STATED the wide bound.  The tree has not changed; what changed
   is that the answer is now printed for all of them.  The old pair of
   columns is recomputed there and the operands in NEITHER are counted.

   SECOND: the classifier with one column DELETED.  If removing `not
   swept: nested` leaves the totality claim green, the column was never
   what made it true.""")
print()
WIDE_REV = "bfd7948"
old_sources = {f: K.source_at(WIDE_REV, f) for f in FILES}
print("   %-18s %-8s %-10s %-11s %-9s %s"
      % ("file", "rev", "operands", "in operands", "in compounds", "in NEITHER"))
neither_then = neither_now = 0
for label, rev, srcs in (("bfd7948", WIDE_REV, old_sources),
                         ("HEAD", "HEAD", sources)):
    for fname in FILES:
        src = srcs[fname]
        ops = K.boolean_operands(src, fname)
        in_operands = len(K.deciding_clauses(src))
        in_compounds = len(K.implicit_disjunctions(src))
        # The two columns as they stood: an operand is in `operands` iff its
        # BoolOp IS the deciding condition, and no operand is ever in
        # `compounds`, which skips `or` and `and` by name.
        neither = len([o for o in ops if not o.top])
        if label == "bfd7948":
            neither_then += neither
        else:
            neither_now += neither
        print("   %-18s %-8s %-10d %-11d %-9d %d"
              % (fname, label, len(ops), in_operands, in_compounds, neither))
print()
print("   at bfd7948 the two columns left %d operand(s) in neither, and the "
      "tree at HEAD\n   leaves the same %d -- the SOURCE did not change.  What "
      "changed is that all %d\n   are now printed in a named column."
      % (neither_then, neither_now, sum(allrow)))
R.gate(neither_then > 0,
       "the pre-repair pair of columns leaves 0 operands in neither at "
       "bfd7948, so this repair is about a defect that is not there and the "
       "control is vacuous")
print()
short_cols = {c: v for c, v in cols.items() if c != "not swept: nested"}
short_sum = sum(len(v) for v in short_cols.values())
print("   with `not swept: nested` deleted from the classifier:")
print("     columns %d, sum %d, independent walk %d, total: %s"
      % (len(short_cols), short_sum, total,
         "still holds" if short_sum == total else "GOES RED"))
R.gate(short_sum != total,
       "deleting the `not swept: nested` column leaves the totality claim "
       "green, so that column is not what makes it true and the claim would "
       "not have caught the 4 operands it was added for")
print()

L.finish(R)
