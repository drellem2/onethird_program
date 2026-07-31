"""Self-test for `lib56dc` -- every rule pinned in BOTH senses.

A fixture that only shows what a rule catches says nothing about what it lets
through, and this arc's whole subject is rules whose reach was never measured
in the second direction.  So every rule below has at least one row it must
match and one it must not, and the grain functions have a row where the two
grains DIFFER -- because a test in which sites and executions coincide would
pass under a parser that could not tell them apart.

This file is also a member of the population `t6`-style checks range over, and
that is deliberate: an instrument that exempts its own self-test has a
population defined by a filename.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib56dc as M

BAD = 0
CHECKS = 0


def ck(label, got, want):
    global BAD, CHECKS
    CHECKS += 1
    ok = got == want
    if not ok:
        BAD += 1
    print("  %-58s %s" % (label, "ok" if ok else "*** got %r want %r ***"
                          % (got, want)))


M.bar("SELFTEST mg-56dc -- both senses, every rule")

M.hdr("1  count_rows -- the printed-count SHAPE, and what is NOT one")

ck("a label and a trailing integer is a count row",
   M.count_rows("      pipelines in the file          12\n"),
   [(1, "pipelines in the file", [12])])
ck("two columns give two integers on one row",
   M.count_rows("      bee07a1   ERREXIT     19   26\n"),
   [(1, "bee07a1   ERREXIT", [19, 26])])
ck("a SENTENCE is not a count row",
   M.count_rows("  There are 12 pipelines in this file, and each one is read.\n"),
   [])
ck("a bare number with no label is not a count row",
   M.count_rows("      12\n"), [])
ck("a label with no number is not a count row",
   M.count_rows("      pipelines in the file\n"), [])

M.hdr("2  grain_of -- SITE, EXECUTION, BOTH, NONE, and WHERE it was found")

ck("`executions` on the label is EXECUTION/label",
   M.grain_of("discarded git diff EXECUTIONS"), ("EXECUTION", "label"))
ck("`source lines` on the label is SITE/label",
   M.grain_of("pipeline SOURCE LINES"), ("SITE", "label"))
ck("a label naming both grains is BOTH",
   M.grain_of("source lines and their executions"), ("BOTH", "label"))
ck("no grain word anywhere is NONE",
   M.grain_of("the widened total"), ("NONE", "-"))
ck("a grain word one line up is found, and SAID to be",
   M.grain_of("...outside it", ["executing sites naming a `*.sh`   43"]),
   ("SITE", "prev"))
ck("a grain word only in a column header 4 lines up is `header`",
   M.grain_of("bee07a1   EITHER",
              ["", "", "revision   clause   files   pipelines", ""]),
   ("SITE", "header"))
ck("a line with a DIGIT is not a column header",
   M.grain_of("bee07a1   EITHER",
              ["", "", "19  26  files", ""]), ("NONE", "-"))

M.hdr("3  the loop expander -- SITES and EXECUTIONS must DIFFER")

LOOP = """#!/bin/sh
for pair in "a x" \\
            "b y" \\
            "c z"; do
    base=${pair%% *}
    n=$(git diff "$base..HEAD" | wc -c)
    echo "$n"
done
"""
FLAT = """#!/bin/sh
python3 a.py | tee out_a.txt
python3 b.py | tee out_b.txt
"""
DOLLAR = """#!/bin/sh
for d in $DIRS; do
    n=$(git diff "$d" | wc -c)
done
"""
ck("a 3-item loop header expands to 3 literal items",
   [len(i) if i else None for _v, i, _f, _l in M.for_loops(LOOP)], [3])
ck("...over 1 pipeline SOURCE LINE", len(M.pipeline_sites(LOOP, "git diff")), 1)
ck("...which is 3 EXECUTIONS -- the two grains differ",
   len(M.pipeline_executions(LOOP, "git diff")), 3)
ck("outside any loop, sites and executions coincide",
   (len(M.pipeline_sites(FLAT, "| tee")),
    len(M.pipeline_executions(FLAT, "| tee"))), (2, 2))
ck("a `$VAR` loop is NOT statically expandable",
   [i for _v, i, _f, _l in M.for_loops(DOLLAR)], [None])
ck("...and its pipeline is one row with iteration None, never counted as 1",
   [it for _l, it, _b, _t in M.pipeline_executions(DOLLAR, "git diff")], [None])
ck("a `|` inside quotes is not a pipe",
   M.pipeline_sites("grep 'A|B' f.txt\n"), [])
ck("a commented pipeline is not a pipeline",
   M.pipeline_sites("# python3 a.py | tee o.txt\n"), [])

M.hdr("4  exec_site_rows vs exec_sites -- ROWS and SITES must differ")

rows_ = [("f.py", 10, "a.sh", True), ("f.py", 10, "b.sh", True),
         ("g.py", 20, "a.sh", False)]
ck("three rows over two distinct sites", (len(rows_), len(M.exec_sites(rows_))),
   (3, 2))
ck("one site naming one script is one row and one site",
   len(M.exec_sites([("f.py", 1, "a.sh", True)])), 1)

M.hdr("5  figures -- the threshold is a PARAMETER, and the two copies differ")

ck("`small=2` keeps 3, which is lib7522's rule", M.figures("x 3 y", 2), [3])
ck("`small=3` drops 3, which is lib70c7's rule", M.figures("x 3 y", 3), [])
ck("both keep 4", (M.figures("x 4 y", 2), M.figures("x 4 y", 3)), ([4], [4]))
ck("a `:`-prefixed number is a line reference, not a figure",
   M.figures("s3_figure.py:154", 2), [])
ck("`on line 89` is a reference, not a figure",
   M.figures("with its figure on line 89", 2), [])
ck("a comma'd figure survives", M.figures("10,483 rows", 2), [10483])

M.hdr("6  THIS TREE'S OWN RUNNER -- no pipeline, every step guarded")

runner = M.read("%s/run_all.sh" % M.TREE, None)
ck("pipelines of any kind in run_all.sh", len(M.pipeline_sites(runner)), 0)
steps = [l for l in runner.splitlines() if l.startswith("run ")]
ck("steps, each invoked through the `run` helper", len(steps), 6)
ck("the helper reads its own status with an explicit guard",
   'python3 -B "$_p" > "$_o" 2>&1 || {' in runner, True)

print()
M.bar("selftest56dc TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts a rule of `lib56dc` that answers")
print("wrongly in either direction on a fixture written here.  It ranges over")
print("6 rules and %d assertions, counted rather than written down.  It does"
      % CHECKS)
print("NOT establish that the rules are the RIGHT rules for the question --")
print("that is what the probes' controls against pre-repair commits are for.")
sys.exit(1 if BAD else 0)
