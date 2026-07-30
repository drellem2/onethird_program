"""SELF-TEST for mg-a4ef.

The instrument this repair ships is a DETECTOR, and a detector's self-test has
to do two things a numerical self-test does not: show that it fires on what it
must catch, and show that it does NOT fire on the things that look like it.
Roughly half the assertions below are the second kind, because every defect
this file's own author put into it during the day was a false positive or a
missed line, never a wrong number.

Anchored to fixtures with hand-computed answers, not to the repository, so a
change to the repository cannot make this pass by accident.

    python3 code/species_repair_a4ef/selftesta4ef.py
"""

import re
import sys

from kerna4ef import (flat, scan, _offsets, _mask_scaffold, NAMES_A_REPAIR,
                      NEGATES, DECLARED_TABLE, WINDOW, TABLE_REACH)
from stricken_a4ef import CORRECTIONS, TREES, EXCLUDE

n = 0


def eq(got, want, what):
    global n
    n += 1
    assert got == want, "%s: got %r want %r" % (what, got, want)


def ok(cond, what):
    global n
    n += 1
    assert cond, what


# ---------------------------------------------------------------------------
# 1.  flat()
# ---------------------------------------------------------------------------
eq(flat("a  b\n c"), "a b c", "flat collapses runs")
eq(flat("> quoted\n> text"), "quoted text", "flat strips blockquote markers")
eq(flat(">> deep\n>> quote"), "deep quote", "flat strips nested markers")
eq(flat("   leading"), "leading", "flat drops leading space")
eq(flat("a\n\n\nb"), "a b", "flat collapses blank lines")

# ---------------------------------------------------------------------------
# 2.  the offset -> line map.  This is where the two defects were.
# ---------------------------------------------------------------------------
f, m = _offsets("one\ntwo\nthree\n")
eq(f, "one two three ", "offsets flattens")
eq(m[0], 1, "first char is line 1")
eq(m[f.index("two")], 2, "'two' is line 2")
eq(m[f.index("three")], 3, "'three' is line 3")

# a 40-line preamble then the target: the reported line must be 41, not 1.
src = "\n".join("# filler %d" % i for i in range(40)) + "\nTARGET here\n"
f, m = _offsets(src)
eq(m[f.index("TARGET")], 41, "line map survives a long preamble")

# ---------------------------------------------------------------------------
# 3.  print()-scaffold masking, and that it PRESERVES LINE COUNTS.
# ---------------------------------------------------------------------------
py = ('print("alpha beta")\n'
      'print("gamma delta")\n')
masked = _mask_scaffold(py)
eq(len(masked), len(py), "masking preserves length")
eq(masked.count("\n"), py.count("\n"), "masking preserves newline COUNT")
flatpy, mpy = _offsets(py)
ok("beta gamma" in flatpy, "a sentence split across two print()s rejoins")
eq(mpy[flatpy.index("gamma")], 2, "and the second line is still line 2")

# implicit string concatenation
py2 = 'print("alpha "\n      "beta")\n'
flat2, m2 = _offsets(py2)
ok("alpha beta" in flat2, "implicit concatenation rejoins")
eq(m2[flat2.index("beta")], 2, "and keeps its line")

# %-formatting between the two prints
py3 = 'print("alpha %d" % k)\nprint("beta")\n'
flat3, m3 = _offsets(py3)
ok("alpha" in flat3 and "beta" in flat3, "%-formatted print still scanned")
eq(m3[flat3.index("beta")], 2, "and keeps its line")

# a 30-line body then the wrapped sentence: the exact shape of t6:149
body = "\n".join('print("filler %d")' % i for i in range(30))
py4 = (body + '\n'
       'print("  IS mu_{S,T}, and T5 measured it against every Hopf")\n'
       'print("  monoid axiom with 0 failures on 4399 basis elements.")\n')
hits = scan(py4, CORRECTIONS[1][3], CORRECTIONS[1][4])
eq([h[0] for h in hits], [31], "the wrapped X3 sentence is ONE hit at line 31")
eq(hits[0][1], True, "and unmarked it is ASSERTED")

# ---------------------------------------------------------------------------
# 4.  the three exoneration routes, each separately
# ---------------------------------------------------------------------------
X3PATS, X3OWN = CORRECTIONS[1][3], CORRECTIONS[1][4]
BARE = ("T5 measured it against every Hopf monoid axiom with 0 failures\n"
        "on 4399 basis elements.\n")

eq([a for _, a in scan(BARE, X3PATS, X3OWN)], [True], "bare is asserted")

for marker, why in [
        ("corrected mg-6f61: per column.", "names a repair (6f61)"),
        ("corrected mg-a4ef: per column.", "names a repair (a4ef)"),
        ("That sentence is STRICKEN.", "negates outright"),
        ("It no longer holds.", "negates outright"),
        ("What it measures is CLOSURE, and only closure.", "own negation")]:
    eq([a for _, a in scan(BARE + marker, X3PATS, X3OWN)], [False],
       "exonerated: %s" % why)

# ... and the phrases that must NOT exonerate: this is the false negative
# w3_scope.py recorded against itself and c4_scope.py reproduced against
# itself.
for disarmer, why in [
        ("It is not the framework this ticket is about.", "generic 'is not'"),
        ("This is REPAIRED elsewhere.", "bare REPAIRED"),
        ("It used to be a problem here.", "bare 'used to'"),
        ("Nothing here is wrong.", "generic reassurance")]:
    eq([a for _, a in scan(BARE + disarmer, X3PATS, X3OWN)], [True],
       "NOT disarmed by: %s" % why)

# distance: a marker beyond WINDOW lines must not reach
far = BARE + "\n" * (WINDOW + 3) + "corrected mg-a4ef.\n"
eq([a for _, a in scan(far, X3PATS, X3OWN)], [True],
   "a marker %d lines away does not reach" % (WINDOW + 3))
near = BARE + "\n" * (WINDOW - 2) + "corrected mg-a4ef.\n"
eq([a for _, a in scan(near, X3PATS, X3OWN)], [False],
   "a marker inside the window does reach")

# ---------------------------------------------------------------------------
# 5.  the declared-table route, and its limits
# ---------------------------------------------------------------------------
tbl = ('STRICKEN = [\n'
       '    ("x", "T5 measured it against every Hopf monoid axiom with 0\n'
       '     failures on 4399 basis elements"),\n'
       ']\n')
eq([a for _, a in scan(tbl, X3PATS, X3OWN)], [False],
   "inside a declared STRICKEN table is a declaration, not an assertion")

tbl2 = tbl.replace("STRICKEN", "NOTES")
eq([a for _, a in scan(tbl2, X3PATS, X3OWN)], [True],
   "a table with an undeclared name is NOT exonerated")

# out of reach: TABLE_REACH lines of padding between header and string
far_tbl = ('STRICKEN = [\n' + '    # pad\n' * (TABLE_REACH + 2)
           + '    "T5 measured it against every Hopf monoid axiom with 0'
             ' failures on 4399 basis elements",\n]\n')
eq([a for _, a in scan(far_tbl, X3PATS, X3OWN)], [True],
   "beyond TABLE_REACH the table header does not exonerate")

ok(DECLARED_TABLE.match("FORBIDDEN = ["), "FORBIDDEN is a declared table")
ok(DECLARED_TABLE.match("STRICKEN_FIXTURES = ["), "so is STRICKEN_FIXTURES")
ok(not DECLARED_TABLE.match("  STRICKEN = ["), "but not when indented")

# ---------------------------------------------------------------------------
# 6.  the patterns themselves -- each must fire on its own sentence and NOT
#     on the corrected form.  This is the half that would have caught the
#     first version's fourteen false positives.
# ---------------------------------------------------------------------------
STRICKEN_FIXTURES = {
    "X1": "Smallest witness with AC(P) != Pi[n]: P = {a<c, b<d}, where ad|bc.",
    "X3": BARE,
    "X6a": "a cone cut out by inequalities of the form y(i) <= y(j) for i, j.",
    "X6b": "the cone y(i) <= y(j).",
    "X7": ("Recall from Section 17.4 that K-bar(Pi) is the algebra of "
           "symmetric functions in noncommuting variables."),
    "X4": "T3d: four candidate identifications, three are controls.",
    "X5": "control (ii) fires hard on 1442 closure failures.",
    "X2a": "The identity of 2.3 is measured, not proved.",
    "X2b": "Read Saliola and Commins before quoting 2.3 as a measurement.",
    "X2c": "It was not located stated in that generality.",
    "Y2": "the left side is Solomon's descent algebra by T3.",
}
CORRECTED_FIXTURES = {
    "X1": "The smallest is the 3-ELEMENT CHAIN; {a<c, b<d} IS a witness.",
    "X3": "T5 measures CLOSURE on 4399 basis elements.",
    "X6a": "a cone cut out by inequalities of the form y(i) >= y(j) for i, j.",
    "X6b": "the cone y(i) >= y(j).",
    "X7": ("Recall from Section 17.4 that K(Pi*) is the algebra of "
           "symmetric functions in noncommuting variables."),
    "X4": "T3d: the four columns are two statements, each computed twice.",
    "X5": "control (ii) fires on a type mismatch, not a near miss.",
    "X2a": "The identity of 2.3 is a corollary, PROVED in three lines.",
    "X2b": "Section 10 item 2 is CLOSED and its errand withdrawn.",
    "X2c": "It IS located, as a corollary.",
    "Y2": "the left side is anti-isomorphic to Solomon's descent algebra.",
}
for cid, label, _doc, pats, own in CORRECTIONS:
    hits = [a for _, a in scan(STRICKEN_FIXTURES[cid], pats, own)]
    ok(hits and all(hits), "%s fires on its own sentence" % cid)
    hits = [a for _, a in scan(CORRECTED_FIXTURES[cid], pats, own) if a]
    eq(hits, [], "%s does NOT fire on the corrected form" % cid)

# every row is well formed
for row in CORRECTIONS:
    eq(len(row), 5, "every correction row has five fields")
    ok(isinstance(row[3], list) and row[3], "%s has patterns" % row[0])
    ok(isinstance(row[4], str) and row[4], "%s has an own-negation" % row[0])
    for p in row[3]:
        re.compile(p)
        n += 1
    re.compile(row[4])
eq(len({r[0] for r in CORRECTIONS}), len(CORRECTIONS), "ids are unique")
eq(len(CORRECTIONS), 11, "eleven corrections: 10 from check_doc plus Y2")
eq(len(TREES), 4, "four code trees")
ok("stricken_a4ef.py" in EXCLUDE, "the list module is excluded")
eq(len(EXCLUDE), 5, "the exclusion list is FIVE named files and no pattern")
ok("out_t6_fock_and_record.txt" not in EXCLUDE,
   "a committed output is NOT excluded -- that is the defect being closed")

# ---------------------------------------------------------------------------
# 7.  the marker regexes in isolation
# ---------------------------------------------------------------------------
for s in ["mg-6f61", "mg-f8fa", "mg-a61f", "mg-73df", "mg-a4ef", "MG-A4EF"]:
    ok(NAMES_A_REPAIR.search(s), "%s names a repair" % s)
for s in ["mg-1953", "mg-af28", "repaired", "REPAIRED"]:
    ok(not NAMES_A_REPAIR.search(s), "%s does NOT name one of these" % s)
for s in ["refuted", "STRICKEN", "WITHDRAWN", "is FALSE",
          "no longer holds", "used to say", "does not hold"]:
    ok(NEGATES.search(s), "%r negates" % s)
for s in ["is not the framework", "used to", "no longer", "REPAIRED"]:
    ok(not NEGATES.search(s), "%r does NOT negate on its own" % s)

print("selftesta4ef OK -- %d assertions" % n)
sys.exit(0)
